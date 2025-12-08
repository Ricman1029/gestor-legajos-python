from datetime import date
from typing import Optional
from sqlalchemy import String, Date, ForeignKey, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.core.database import Base

class Empleado(Base):
    __tablename__ = "empleados"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    # Obligatorio: Sin empresa no hay empleado
    empresa_id: Mapped[int] = mapped_column(ForeignKey("empresas.id"), nullable=False)

    # --- DATOS PERSONALES ---
    nombre: Mapped[str] = mapped_column(String(50), nullable=False)
    apellido: Mapped[str] = mapped_column(String(50), nullable=False)
    dni: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    cuil: Mapped[str] = mapped_column(String(20), nullable=False, unique=True)
    sexo: Mapped[str] = mapped_column(String(20), nullable=False)
    nacionalidad: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_nacimiento: Mapped[date] = mapped_column(Date, nullable=False)

    # --- DATOS LABORALES ---
    numero_legajo: Mapped[str] = mapped_column(String(50), nullable=False)
    fecha_ingreso: Mapped[date] = mapped_column(Date, nullable=False)
    fecha_egreso: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    sueldo: Mapped[float] = mapped_column(Float, nullable=False)
    categoria_id: Mapped[int] = mapped_column(ForeignKey("categorias.id"), nullable=False)
    categoria_rel: Mapped["Categoria"] = relationship(back_populates="empleados")
    obra_social: Mapped[str] = mapped_column(String(100), nullable=False)

    # --- DOMICILIO ---
    calle: Mapped[str] = mapped_column(String(100), nullable=False)
    numero: Mapped[str] = mapped_column(String(50), nullable=False)
    piso: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    depto: Mapped[Optional[str]] = mapped_column(String(10), nullable=True)
    localidad: Mapped[str] = mapped_column(String(100), nullable=False)
    provincia: Mapped[str] = mapped_column(String(100), nullable=False)
    codigo_postal: Mapped[str] = mapped_column(String(50), nullable=False)
    telefono: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    empresa: Mapped["Empresa"] = relationship(back_populates="empleados")

    def __repr__(self):
        return f"<Empleado(apellido='{self.apellido}', dni='{self.dni}')>"
