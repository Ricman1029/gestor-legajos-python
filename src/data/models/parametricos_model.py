from sqlalchemy import String, ForeignKey, UniqueConstraint, Table, Column, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List, Optional
from src.core.database import Base

empresa_convenio_asociacion = Table(
        "empresa_convenio_asociacion",
        Base.metadata,
        Column("empresa_id", Integer, ForeignKey("empresas.id"), primary_key=True),
        Column("convenio_id", Integer, ForeignKey("convenios.id"), primary_key=True),
        )
       
class Sindicato(Base):
    __tablename__ = "sindicatos"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    personeria_gremial: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)

    convenios: Mapped[List["Convenio"]] = relationship(back_populates="sindicato_rel")

    def __repr__(self):
        return self.nombre
    
class Convenio(Base):
    __tablename__ = "convenios"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    sindicato_id: Mapped[int] = mapped_column(ForeignKey("sindicatos.id"), nullable=False)
    sindicato_rel: Mapped["Sindicato"] = relationship(back_populates="convenios")

    categorias: Mapped[List["Categoria"]] = relationship(back_populates="convenio", cascade="all, delete-orphan")

    empresas: Mapped[List["Empresa"]] = relationship(
            secondary=empresa_convenio_asociacion,
            back_populates="convenios"
            )

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

class Art(Base):
    __tablename__ = "arts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    telefono: Mapped[str] = mapped_column(String(100), nullable=False)

    # Relación inversa: Una ART tiene muchas empresas
    empresas: Mapped[List["Empresa"]] = relationship(back_populates="art_rel")

    def __repr__(self):
        return self.nombre

class ObraSocial(Base):
    __tablename__ = "obras_sociales"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    codigo: Mapped[Optional[str]] = mapped_column(String(20), nullable=False)

    empleados: Mapped[List["Empleado"]] = relationship(back_populates="obra_social_rel")

    def __repr__(self):
        return self.nombre
