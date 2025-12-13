from pydantic import BaseModel, Field, ConfigDict
from typing import Optional

class ArtBase(BaseModel):
    nombre: str = Field(..., min_length=3)
    telefono: str = Field(..., min_length=6)

class ArtCreate(ArtBase):
    pass

class ArtSchema(ArtBase):
    id: int = Field(..., gt=0)
    model_config = ConfigDict(from_attributes=True)

class SindicatoBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    personeria_gremial: Optional[str] = None

class SindicatoCreate(SindicatoBase):
    pass

class SindicatoSchema(SindicatoBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class ConvenioBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    sindicato_id: int = Field(..., gt=0)

class ConvenioCreate(ConvenioBase):
    pass

class ConvenioSchema(ConvenioBase):
    id: int
    sindicato: Optional[SindicatoSchema] = None
    model_config = ConfigDict(from_attributes=True)

class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=2)
    convenio_id: int = Field(..., gt=0)

class CategoriaCreate(CategoriaBase):
    pass

class CategoriaSchema(CategoriaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
