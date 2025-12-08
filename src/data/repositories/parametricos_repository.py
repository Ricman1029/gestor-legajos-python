from sqlalchemy import select
from sqlalchemy.orm import joinedload
from src.data.repositories.base_repository import BaseRepository
from src.data.models.parametricos_model import Convenio, Categoria

class ConvenioRepository(BaseRepository[Convenio]):
    def __init__(self, session):
        super().__init__(session, Convenio)

class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, session):
        super().__init__(session, Categoria)

    async def get_by_convenio(self, convenio_id: int):
        result = await self.session.execute(
                select(Categoria).where(Categoria.convenio_id == convenio_id)
                )
        return result.scalars().all()
