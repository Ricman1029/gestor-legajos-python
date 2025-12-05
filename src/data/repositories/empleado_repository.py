from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.data.repositories.base_repository import BaseRepository
from src.data.models.empleado_model import Empleado
from src.domain.schemas.empleado_schema import EmpleadoCreate, EmpleadoUpdate

class EmpleadoRepository(BaseRepository[Empleado]):
    def __init__(self, session):
        super().__init__(session, Empleado)

    async def get_all(self):
        query = select(Empleado).options(joinedload(Empleado.empresa))
        result = await self.session.execute(query)
        return result.scalars().all()

    async def create(self, schema: EmpleadoCreate) -> Empleado:
        db_obj = Empleado(**schema.model_dump())
        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, id: int, schema: EmpleadoUpdate) -> Empleado | None:
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None

        update_data = schema.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_obj, key, value)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def get_by_empresa(self, empresa_id: int):
        """Método personalizado: Obtener empleados de una empresa específica"""
        result = await self.session.execute(
                select(Empleado).where(Empleado.empresa_id == empresa_id)
                )
        return result.scalars().all()
