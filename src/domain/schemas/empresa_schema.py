from typing import Optional
from pydantic import BaseModel, Field, ConfigDict, field_validator

class EmpresaBase(BaseModel):
    """Campos compartidos entre creación y lectura"""
    razon_social: str = Field(..., min_length=2, max_length=100)
    cuit: str
    numero_ieric: Optional[str] = None
    convenio: str

    # Ubicación
    calle: str = Field(..., min_length=2)
    numero: str
    piso: Optional[str] = None
    depto: Optional[str] = None
    localidad: str = Field(..., min_length=2)
    provincia: str = Field(..., min_length=2)
    codigo_postal: str = Field(..., min_length=2)

    # Contacto
    telefono: Optional[str]
    mail: str = Field(..., min_length=5)

    # --- VALIDACIONES DE NEGOCIO ---
    @field_validator("cuit")
    @classmethod
    def validar_cuit(cls, v: str) -> str:
        # Limpiamos guiones por si el usuario los pone
        limpio = v.replace("-", "").replace(" ", "")
        if not limpio.isdigit():
            raise ValueError("El CUIT debe contener solo números")
        if len(limpio) != 11:
            raise ValueError("El CUIT debe tener 11 dígitos")
        return limpio

class EmpresaCreate(EmpresaBase):
    """Schema para CREAR una empresa (No tiene ID todavía)"""
    pass

class EmpresaUpdate(BaseModel):
    """
    Schema para ACTUALIZAR. Todos los campos son opcionales.
    Si envias solo el teléfono, solo se actualiza el teléfono.
    """
    razon_social: Optional[str] = None
    cuit: Optional[str] = None
    convenio: Optional[str] = None
    calle: Optional[str] = None
    numero: Optional[str] = None
    localidad: Optional[str] = None
    provincia: Optional[str] = None
    codigo_postal: Optional[str] = None
    telefono: Optional[str] = None
    mail: Optional[str] = None

class EmpresaSchema(EmpresaBase):
    """
    Schema para LEER/DEVOLVER datos a la UI.
    Ya incluye el ID que generó la base de datos.
    """
    id: int

    # Esto le dice a Pydantic: "Aceptá objetos de SQLAlchemy y convertilos a JSON automáticamente"
    model_config = ConfigDict(from_attributes=True)
