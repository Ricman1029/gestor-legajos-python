from sqlalchemy import String, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List
from src.core.database import Base

class Convenio(Base):
    __tablename__ = "convenios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    # Relaciones
    categorias: Mapped[List["Categoria"]] = relationship(back_populates="convenio", cascade="all, delete-orphan")
    empresas: Mapped[List["Empresa"]] = relationship(back_populates="convenio_rel")

    def __repr__(self):
        return self.nombre

class Categoria(Base):
    __tablename__ = "categorias"

    __table_args__ = (
            UniqueConstraint("nombre", "convenio_id", name="uq_categoria_por_convenio"),
            )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), nullable=False)
    convenio_id: Mapped["Convenio"] = mapped_column(ForeignKey("convenios.id"), nullable=False)

    convenio: Mapped["Convenio"] = relationship(back_populates="categorias")
    empleados: Mapped[List["Empleado"]] = relationship(back_populates="categoria_rel")

    def __repr__(self):
        return self.nombre
