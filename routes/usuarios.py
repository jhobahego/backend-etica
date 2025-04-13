from fastapi import APIRouter, HTTPException, status, Body
from fastapi.responses import JSONResponse, Response
from fastapi.encoders import jsonable_encoder
from typing import List

from models.Usuario import Usuario, ActualizarUsuario
from config.db import conn

usuario = APIRouter()

@usuario.get("/empleados", response_description="Empleados listados", response_model=List[Usuario])
async def obtener_usuarios():
    usuarios = await conn["empleados"].find().to_list(1000)
    return usuarios

@usuario.get("/empleados/{num_cedula}", response_description="Empleado obtenido", response_model=Usuario)
async def obtener_usuario_por_cedula(num_cedula: str):
    usuario = await conn["empleados"].find_one({"num_cedula": num_cedula})
    if usuario is not None:
        return usuario

    raise HTTPException(
        status_code=404, detail=f"Empleado con cedula {num_cedula} no encontrado"
    )

@usuario.post("/empleados", response_description="Empleado guardado", response_model=Usuario)
async def guardar_usuario(usuario: Usuario = Body(...)):
    usuarios = await obtener_usuarios()
    if any(u["num_cedula"] == usuario.num_cedula for u in usuarios):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Empleado con esta cedula ya registrado"
        )

    usuario = jsonable_encoder(usuario)

    nuevo_usuario = await conn["empleados"].insert_one(usuario)
    usuario_creado = await conn["empleados"].find_one({"_id": nuevo_usuario.inserted_id})

    return JSONResponse(status_code=status.HTTP_201_CREATED, content=usuario_creado)

@usuario.put("/empleados/{usuario_id}", response_description="Empleado actualizado", response_model=Usuario)
async def actualizar_usuario(usuario_id: str, usuario: ActualizarUsuario = Body(...)):
    usuario_dict = {datos: valor for datos, valor in usuario.model_dump().items()
                   if valor is not None}
    if len(usuario_dict) >= 1:
        update_result = await conn["empleados"].update_one({"_id": usuario_id}, {"$set": usuario_dict})

        if update_result.modified_count == 1:
            usuario_actualizado = await conn["empleados"].find_one({"_id": usuario_id})
            if usuario_actualizado is not None:
                return usuario_actualizado

    usuario_existente = await conn["empleados"].find_one({"_id": usuario_id})
    if usuario_existente is not None:
        return usuario_existente

    raise HTTPException(
        status_code=404, detail=f"Empleado con id: {usuario_id} no encontrado")


@usuario.delete("/empleados/{usuario_id}", response_description="Empleado eliminado")
async def eliminar_usuario_por_id(usuario_id: str):
    usuario_eliminado = await conn["empleados"].delete_one({"_id": usuario_id})
    if usuario_eliminado.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=404, detail=f"Empleado con id {usuario_id} no encontrado")
