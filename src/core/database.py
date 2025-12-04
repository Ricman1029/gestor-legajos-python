import logging
from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase

# --- CONFIGURACIÓN DE RUTAS ---
# __file__ es el archivo en el que estamos parados: /gestor-legajos-python/src/core/database.py
# parents[0] = src/core
# parents[1] = src
# parents[2] = gestor-legajos-python (La Raíz)
BASE_DIR = Path(__file__).resolve().parents[2]
DB_FOLDER = BASE_DIR / "db"
DB_FOLDER.mkdir(parents=True, exist_ok=True)
DB_NAME = "app.db"
DB_PATH = DB_FOLDER / DB_NAME
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# --- LOGGING ----
# Esto imprime las consultas SQL en la cosola
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)

# --- MOTOR DE BASE DE DATOS (ENGINE) ---
# echo=True hace lo mismo que el logging de arriba, así que lo ponemos en False
# connect_args={"check_same_thread": False} es necesario para SQLite + Asyncio
engine = create_async_engine(
        DATABASE_URL,
        echo=False,
        connect_args={"check_same_thread": False}
        )

# --- FACTORY DE SESIONES ---
# Esto crea las sesiones que usamos para cada transacción
AsyncSessionLocal = async_sessionmaker(
        bind=engine,
        class_=AsyncSession,
        expire_on_commit=False, # Evita que los objetos se desconecten tras un commit
        autoflush=False
        )

# --- CLASE BASE ORM ---
# Todos nuestros modelos (Empresa, Empleado) heredan de acá.
class Base(DeclarativeBase):
    pass

# --- DEPENDENCY INJECTION ---
# Esta función se va a usar cada vez que necesitemos interactuar con la DB.
# Cumple con el principio de Inversión de Depencias
async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """
    Generador de contexto asíncrono para la base de datos.
    Abre una sesión, la entrega, y asegura que se cierre al terminar, 
    incluso si ocurre un error.
    """

    async with AsyncSessionLocal() as session:
        try:
            yield session
            # Acá se podría hacer un commit automático
            # pero es mejor ser explícito en los servicios
        except Exception as e:
            await session.rollback() # Si algo falla, deshacemos cambios pendientes
            raise e
        finally:
            await session.close()
