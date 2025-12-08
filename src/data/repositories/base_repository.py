from typing import Generic, TypeVar, Type, Optional, Sequence
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import interfaces
from src.core.database import Base

ModelType = TypeVar("ModelType", bound=Base)

class BaseRepository(Generic[ModelType]):
    """
    Repositorios Genérico que  implementa el CRUD básico.
    ModelType: Es la clase del modelo (ej: Empresa, Empleado).
    """

    def __init__(self, session: AsyncSession, model: Type[ModelType]):
        self.session = session
        self.model = model

    async def get_all(self) -> Sequence[ModelType]:
        """Obtiene todos los registros de la tabla"""
        # Ejecuta: SELECT * FROM tabla
        result = await self.session.execute(select(self.model))
        return result.scalars().all()

    async def get_by_id(
            self,
            id: int,
            options: Optional[Sequence[interfaces.MapperOption]] = None
            ) -> Optional[ModelType]:
        """Busca por ID"""
        query = select(self.model).where(self.model.id == id)

        if options:
            query = query.options(*options)

        result = await self.session.execute(query)
        return result.scalars().first()

    async def delete(self, id: int) -> bool:
        """Borra por ID"""
        # Primero verificamos si existe
        obj = await self.get_by_id(id)
        if obj:
            await self.session.delete(obj)
            await self.session.commit()
            return True
        return False
