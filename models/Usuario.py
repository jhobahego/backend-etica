from typing import Optional
from pydantic import Field, BaseModel, ConfigDict
from enum import Enum

from models.Id import PyObjectId


class RolesUsuario(str, Enum):
    USUARIO = "usuario"
    ADMIN = "admin"


class Usuario(BaseModel):
    usuario_id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    nombres: str
    num_cedula: int
    salario: float
    pension_descontada: Optional[bool] = Field(default=False)
    salud_descontada: Optional[bool] = Field(default=False)
    rol: RolesUsuario = Field(default=RolesUsuario.USUARIO)
    hashed_password: str

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
                "rol": "usuario",
                "hashed_password": "password",
            }
        },
    )


class ActualizarUsuario(BaseModel):
    nombres: Optional[str] = None
    salario: Optional[float] = None
    pension_descontada: Optional[bool] = None
    salud_descontada: Optional[bool] = None

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        json_schema_extra={
            "example": {
                "nombres": "Jane Doe",
                "salario": 1230000.0,
                "pension_descontada": False,
                "salud_descontada": True,
            }
        },
    )
