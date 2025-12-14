from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class EmpleadoBase(BaseModel):
    # Personal
    nombre: str = Field(..., min_length=2)
    apellido: str = Field(..., min_length=2)
    dni: str = Field(..., min_length=2)
    cuil: str = Field(..., min_length=2)
    sexo: str = Field(..., min_length=2)
    nacionalidad: str = Field(..., min_length=2)
    fecha_nacimiento: date
    estado_civil: Optional[str] = None

    # Laborales
    numero_legajo: str = Field(..., min_length=1)
    fecha_ingreso: date
    fecha_egreso: Optional[date] = None
    sueldo: float = Field(..., gt=0)
    categoria_id: int = Field(..., gt=0, description="ID de la Categoria")
    obra_social_id: int = Field(..., gt=0, description="ID de la Obra Social")
    
    # Domicilio
    calle: str = Field(..., min_length=2)
    numero: str = Field(..., min_length=2)
    piso: Optional[str] = None
    depto: Optional[str] = None
    localidad: str = Field(..., min_length=2)
    provincia: str = Field(..., min_length=2)
    codigo_postal: str = Field(..., min_length=2)

    # Contacto
    telefono: Optional[str] = None
    mail: Optional[str] = None

    @field_validator("dni")
    @classmethod
    def validar_dni(cls, v: str) -> str:
        if not v.isdigit():
            raise ValueError("El DNI debe ser numérico")
        if len(v) < 7 or len(v) > 8:
            raise ValueError("DNI inválido (7 u 8 dígitos)")
        return v

    @field_validator("fecha_egreso")
    @classmethod
    def validar_fechas(cls, v: Optional[date], info):
        # Validar fechas cruzadas (egreso > ingreso) es complejo en Pydantic V2
        # Lo vamos a hacer mas adelante
        return v

class EmpleadoCreate(EmpleadoBase):
    """Necesitamos saber a qué empresa pertenece al crearlo"""
    empresa_id: int

class EmpleadoUpdate(BaseModel):
    """campos opcionales para edición"""

    nombre: Optional[str] = None
    apellido: Optional[str] = None
    dni: Optional[str] = None
    cuil: Optional[str] = None
    sexo: Optional[str] = None
    nacionalidad: Optional[str] = None
    fecha_nacimiento: Optional[date] = None

    # Laborales
    numero_legajo: Optional[str] = None
    fecha_ingreso: Optional[date] = None
    fecha_egreso: Optional[date] = None
    sueldo: Optional[float] = None
    categoria_id: Optional[int] = None
    obra_social: Optional[str] = None
    
    # Domicilio
    calle: Optional[str] = None
    numero: Optional[str] = None
    piso: Optional[str] = None
    depto: Optional[str] = None
    localidad: Optional[str] = None
    provincia: Optional[str] = None
    codigo_postal: Optional[str] = None
    telefono: Optional[str] = None
    mail: Optional[str] = None

class EmpleadoSchema(EmpleadoBase):
    """Lo devolvemos a la UI"""
    id: int
    empresa_id: int

    model_config = ConfigDict(from_attributes=True)
