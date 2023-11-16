from typing import Optional
from pydantic import Field, BaseModel, ConfigDict
from models.Id import PyObjectId


class Usuario(BaseModel):
    usuario_id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    nombres: str
    num_cedula: str
    salario: float
    pension_descontada: Optional[bool] = Field(default=False)
    salud_descontada: Optional[bool] = Field(default=False)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "nombres": "Jane Doe",
                "num_cedula": "1015722525",
                "salario": 1230000.0,
                "pension_descontada": False,
                "salud_descontada": True,
            }
        },
    )


class ActualizarUsuario(BaseModel):
    nombres: Optional[str] = None
    num_cedula: Optional[str] = None
    salario: Optional[float] = None
    pension_descontada: Optional[bool] = None
    salud_descontada: Optional[bool] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "nombres": "Jane Doe",
                "num_cedula": "1015722525",
                "salario": 1230000.0,
                "pension_descontada": False,
                "salud_descontada": True,
            }
        },
    )
