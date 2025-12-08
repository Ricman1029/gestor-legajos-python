from typing import Optional
from sqlalchemy.orm import selectinload
from src.data.repositories.base_repository import BaseRepository
from src.data.models.empresa_model import Empresa
from src.domain.schemas.empresa_schema import EmpresaCreate, EmpresaUpdate

class EmpresaRepository(BaseRepository[Empresa]):
    def __init__(self, session):
        # Inicializamos el padre diciéndole: "Yo manejo el modelo Empresa"
        super().__init__(session, Empresa)

    async def get_para_edicion(self, id_empresa: int) -> Optional[Empresa]:
        return await self.get_by_id(
                id_empresa,
                options=[
                    selectinload(Empresa.convenio_rel),
                    ]
                )

    async def create(self, schema: EmpresaCreate) -> Empresa:
        """
        Recibe el Schema validado, lo convierte a Modelo y lo guarda.
        """
        # Convertimos Pydantic -> Diccionario -> Modelo SQLAlchemy
        # **schema.model_dump() desempaqueta el diccionario:
        # Empresa(razon_social="...", cuit="...", ...)
        db_obj = Empresa(**schema.model_dump())

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, id: int, schema: EmpresaUpdate) -> Empresa | None:
        db_obj = await self.get_by_id(id)
        if not db_obj:
            return None

        # Actualizamos solo los campos que vienen en el schema (excluimos nulos)
        update_data = schema.model_dump(exclude_unset=True)

        for key, value in update_data.items():
            setattr(db_obj, key, value)

        self.session.add(db_obj)
        await self.session.commit()
        await self.session.refresh(db_obj)
        return db_obj
