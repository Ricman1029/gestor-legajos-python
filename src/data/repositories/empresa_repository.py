from typing import Optional
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from src.data.repositories.base_repository import BaseRepository
from src.data.models.empresa_model import Empresa
from src.domain.schemas.empresa_schema import EmpresaCreate, EmpresaUpdate
from src.data.models.parametricos_model import Convenio

class EmpresaRepository(BaseRepository[Empresa]):
    def __init__(self, session):
        # Inicializamos el padre diciéndole: "Yo manejo el modelo Empresa"
        super().__init__(session, Empresa)

    async def get_para_edicion(self, id_empresa: int) -> Optional[Empresa]:
        return await self.get_by_id(
                id_empresa,
                options=[
                    selectinload(Empresa.convenios),
                    selectinload(Empresa.art_rel),
                    ]
                )

    async def create(self, schema: EmpresaCreate) -> Empresa:
        """
        Recibe el Schema validado, lo convierte a Modelo y lo guarda.
        """
        datos = schema.model_dump()
        ids_convenios = datos.pop("convenios_ids", [])

        empresa = Empresa(**datos)

        if ids_convenios:
            stm = select(Convenio).where(Convenio.id.in_(ids_convenios))
            result = await self.session.execute(stm)
            objetos_convenio = result.scalars().all()

            empresa.convenios = list(objetos_convenio)

        self.session.add(empresa)
        await self.session.commit()
        await self.session.refresh(empresa, attribute_names=["convenios", "art_rel"])
        return empresa

    async def update(self, id: int, schema: EmpresaUpdate) -> Optional[Empresa]:
        empresa = await self.get_para_edicion(id)
        if not empresa:
            return None

        datos = schema.model_dump(exclude_unset=True)

        if "convenios_ids" in datos:
            ids_convenios = datos.pop("convenios_ids")

            stm = select(Convenio).where(Convenio.id.in_(ids_convenios))
            result = await self.session.execute(stm)
            nuevos_convenios = result.scalars().all()

            empresa.convenios = list(nuevos_convenios)

        for key, value in datos.items():
            setattr(empresa, key, value)

        self.session.add(empresa)
        await self.session.commit()
        await self.session.refresh(empresa)
        return empresa


