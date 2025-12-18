import logging
from sqlalchemy import text
from src.core.database import engine, Base
from src.data.models import Empresa, Empleado

async def create_tables():
    """
    Crea las tablas en la base de datos si no existen.
    Es equivalente a un 'CREATE TABLE IF NOT EXISTS'
    """
    logging.info("Inicializando base de datos...")
    async with engine.begin() as conn:
        await conn.execute(text("PRAGMA journal_mode=WAL;"))
        await conn.run_sync(Base.metadata.create_all)
    logging.info("Tablas verificadas/creadas con éxito.")
