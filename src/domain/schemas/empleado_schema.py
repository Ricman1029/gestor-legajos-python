from datetime import date
from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class EmpleadoBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    apellido: str = Field(..., min_length=2)
    dni: str
    cuil: str
    sexo: str
    nacionalidad: str
    fecha_nacimiento: date

    # Laborales
    numero_legajo: str
    fecha_ingreso: date
    fecha_egreso: Optional[date] = None
    sueldo: float = Field(..., gt=0)
    categoria: str
    obra_social: str
    
    # Domicilio
    calle: str
    numero: str
    piso: Optional[str] = None
    depto: Optional[str] = None
    localidad: str
    provincia: str
    telefono: Optional[str]

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
    categoria: Optional[str] = None
    obra_social: Optional[str] = None
    
    # Domicilio
    calle: Optional[str] = None
    numero: Optional[str] = None
    piso: Optional[str] = None
    depto: Optional[str] = None
    localidad: Optional[str] = None
    provincia: Optional[str] = None
    telefono: Optional[str] = None

class EmpleadoSchema(EmpleadoBase):
    """Lo devolvemos a la UI"""
    id: int
    empresa_id: int

    model_config = ConfigDict(from_attributes=True)
