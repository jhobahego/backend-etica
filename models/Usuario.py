from typing import Optional
from pydantic import Field, BaseModel
from bson import ObjectId
from models.Id import PyObjectId


class Usuario(BaseModel):
    usuario_id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    nombres: str
    num_cedula: str
    salario: float
    pension_descontada: Optional[bool] = Field(default=False)
    salud_descontada: Optional[bool] = Field(default=False)

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "nombres": "Jane Doe",
                "num_cedula": "1015722525",
                "salario": 1230000.0,
                "pension_descontada": False,
                "salud_descontada": True,
            }
        }


class ActualizarUsuario(BaseModel):
    nombres: Optional[str]
    num_cedula: Optional[str]
    salario: Optional[float]
    pension_descontada: Optional[bool]
    salud_descontada: Optional[bool]

    class Config:
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        schema_extra = {
            "example": {
                "nombres": "Jane Doe",
                "num_cedula": "1015722525",
                "salario": 1230000.0,
                "pension_descontada": False,
                "salud_descontada": True,
            }
        }
