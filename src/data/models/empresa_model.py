from typing import List, Optional
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base 
from src.data.models.parametricos_model import empresa_convenio_asociacion

class Empresa(Base):
    """
    Modelo que representa la tabla 'empresas' en la DB.
    """
    __tablename__ = "empresas"

    # ---IDENTIFICADORES ---
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # ---DATOS FISCALES / LEGALES ---
    razon_social: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    cuit: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    numero_ieric: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    # --- UBICACIÓN ---
    calle: Mapped[str] = mapped_column(String(100), nullable=False)
    numero: Mapped[str] = mapped_column(String(20), nullable=False)
    piso: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    depto: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    localidad: Mapped[Optional[str]] = mapped_column(String(100), nullable=False)
    provincia: Mapped[Optional[str]] = mapped_column(String(100), nullable=False)
    codigo_postal: Mapped[Optional[str]] = mapped_column(String(20), nullable=False)

    # --- CONTACTO ---
    telefono: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    mail: Mapped[Optional[str]] = mapped_column(String(100), nullable=True)

    # --- ART ---
    art_id: Mapped[int] = mapped_column(ForeignKey("arts.id"), nullable=False)
    art_rel: Mapped["Art"] = relationship(back_populates="empresas")

    convenios: Mapped[List["Convenio"]] = relationship(
            secondary=empresa_convenio_asociacion,
            back_populates="empresas"
            )

    empleados: Mapped[List["Empleado"]] = relationship(
            back_populates="empresa",
            cascade="all, delete-orphan"
            )

    def __repr__(self):
        return f"<Empresa(razon_social='{self.razon_social}', cuit='{self.cuit}')>"
