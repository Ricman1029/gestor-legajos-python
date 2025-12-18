from sqlalchemy import select
from sqlalchemy.orm import joinedload, selectinload
from src.domain.schemas.parametricos_schema import ArtCreate, CategoriaCreate, ConvenioCreate, ObraSocialCreate, SindicatoCreate
from src.data.repositories.base_repository import BaseRepository
from src.data.models.parametricos_model import Convenio, Categoria, Art, ObraSocial, Sindicato

class SindicatoRepository(BaseRepository[Sindicato]):
    def __init__(self, session):
        super().__init__(session, Sindicato)

    async def create(self, sindicato: SindicatoCreate) -> Sindicato:
        db_sindicato = Sindicato(**sindicato.model_dump())
        self.session.add(db_sindicato)
        await self.session.commit()
        await self.session.refresh(db_sindicato)
        return db_sindicato

class ConvenioRepository(BaseRepository[Convenio]):
    def __init__(self, session):
        super().__init__(session, Convenio)

    async def create(self, convenio: ConvenioCreate) -> Convenio:
        db_convenio = Convenio(**convenio.model_dump())
        self.session.add(db_convenio)
        await self.session.commit()
        await self.session.refresh(db_convenio)
        return db_convenio

    async def get_all_con_sindicato(self):
        stmt = select(Convenio).options(selectinload(Convenio.sindicato_rel))
        result = await self.session.execute(stmt)
        return result.scalars().all()

class CategoriaRepository(BaseRepository[Categoria]):
    def __init__(self, session):
        super().__init__(session, Categoria)

    async def create(self, categoria: CategoriaCreate) -> Categoria:
        db_categoria = Categoria(**categoria.model_dump())
        self.session.add(db_categoria)
        await self.session.commit()
        await self.session.refresh(db_categoria)
        return db_categoria

    async def get_by_convenio(self, convenio_id: int):
        result = await self.session.execute(
                select(Categoria).where(Categoria.convenio_id == convenio_id)
                )
        return result.scalars().all()

class ArtRepository(BaseRepository[Art]):
    def __init__(self, session):
        super().__init__(session, Art)

    async def create(self, art: ArtCreate) -> Art:
        db_art = Art(**art.model_dump())
        self.session.add(db_art)
        await self.session.commit()
        await self.session.refresh(db_art)
        return db_art

class ObraSocialRepository(BaseRepository[ObraSocial]):
    def __init__(self, session):
        super().__init__(session, ObraSocial)

    async def create(self, obra_social: ObraSocialCreate) -> ObraSocial:
        db_obra_social = ObraSocial(**obra_social.model_dump())
        self.session.add(db_obra_social)
        await self.session.commit()
        await self.session.refresh(db_obra_social)
        return db_obra_social
