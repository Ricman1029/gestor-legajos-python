import sys
import os
import logging
from pathlib import Path
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase
from src.core.config import BASE_DIR

if getattr(sys, "frozen", False):
    ROOT_DATA = Path(os.path.expanduser("~")) / "Documents" / "GestorLegajos"
else:
    ROOT_DATA = BASE_DIR

DB_FOLDER = ROOT_DATA / "db"
DB_FOLDER.mkdir(parents=True, exist_ok=True)
DB_NAME = "app.db"
DB_PATH = DB_FOLDER / DB_NAME
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
        )

AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False, # Evita que los objetos se desconecten tras un commit
        autoflush=False
        )

# --- CLASE BASE ORMlos (Empresa, Empleado) heredan de acá.
class Base(DeclarativeBase):
    pass

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Generador de contexto asíncrono para la base de datos.
    Abre una sesión, la entrega, y asegura que se cierre al terminar, 
    incluso si ocurre un error.
    """

    async with AsyncSessionLocal() as session:
        try:
            yield session
        except Exception as e:
            await session.rollback() # Si algo falla, deshacemos cambios pendientes
            raise e
        finally:
            await session.close()
