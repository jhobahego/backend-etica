from fastapi import APIRouter, HTTPException, status, Body, Depends
from fastapi.responses import Response
from fastapi.encoders import jsonable_encoder
from typing import List

from models.Usuario import Usuario, ActualizarUsuario, RolesUsuario
from config.db import conn
from auth import get_password_hash
from config.deps import get_current_user, check_super_user, require_role


usuario = APIRouter()

@usuario.get("/empleados", response_description="Empleados listados", response_model=List[Usuario])
async def obtener_usuarios(current_user: Usuario = Depends(require_role(["admin"]))):
    usuarios_dict = await conn["empleados"].find().to_list(1000)
    usuarios = []
    
    for usuario_dict in usuarios_dict:
        try:
            # Asegurarnos de que los tipos de datos son correctos
            processed_dict = {
                "_id": str(usuario_dict["_id"]) if "_id" in usuario_dict else None,
                "nombres": str(usuario_dict.get("nombres", "")),
                "num_cedula": int(usuario_dict.get("num_cedula", 0)),
                "salario": float(usuario_dict.get("salario", 0.0)),
                "hashed_password": str(usuario_dict.get("hashed_password", "")),
                "pension_descontada": bool(usuario_dict.get("pension_descontada", False)),
                "salud_descontada": bool(usuario_dict.get("salud_descontada", False)),
                "rol": str(usuario_dict.get("rol", RolesUsuario.USUARIO))
            }

            # Validar que los campos requeridos no están vacíos
            if processed_dict["nombres"] and processed_dict["hashed_password"]:
                usuarios.append(Usuario(**processed_dict))
        except (ValueError, TypeError):
            # Si hay un error con un usuario, lo saltamos y continuamos con el siguiente
            continue
    
    return usuarios


# Obtener usuario por id
@usuario.get("/empleados/{usuario_id}", response_description="Empleado obtenido", response_model=Usuario)
async def obtener_usuario_por_id(usuario_id: str, current_user: Usuario = Depends(get_current_user)):    
    usuario_dict = await conn["empleados"].find_one({"_id": usuario_id})
    if usuario_dict is None:
        raise HTTPException(
            status_code=404, detail=f"Empleado con id: {usuario_id} no encontrado"
        )
    
    # Convertir el diccionario a un objeto Usuario
    try:
        # Asegurarnos de que los tipos de datos son correctos
        processed_dict = {
            "_id": str(usuario_dict["_id"]) if "_id" in usuario_dict else None,
            "nombres": str(usuario_dict.get("nombres", "")),
            "num_cedula": int(usuario_dict.get("num_cedula", 0)),
            "salario": float(usuario_dict.get("salario", 0.0)),
            "hashed_password": str(usuario_dict.get("hashed_password", "")),
            "pension_descontada": bool(usuario_dict.get("pension_descontada", False)),
            "salud_descontada": bool(usuario_dict.get("salud_descontada", False)),
            "rol": str(usuario_dict.get("rol", RolesUsuario.USUARIO))
        }

        # Validar que los campos requeridos no están vacíos
        if not processed_dict["nombres"] or not processed_dict["hashed_password"]:
            raise ValueError("Faltan campos requeridos en el usuario")

        return Usuario(**processed_dict)
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar datos del usuario: {str(e)}"
        )


@usuario.get("/empleados/{num_cedula}", response_description="Empleado obtenido", response_model=Usuario)
async def obtener_usuario_por_cedula(
    num_cedula: str,
    current_user: Usuario = Depends(get_current_user)
):
    usuario_dict = await conn["empleados"].find_one({"num_cedula": int(num_cedula)})
    if usuario_dict is None:
        raise HTTPException(
            status_code=404, detail=f"Empleado con cedula {num_cedula} no encontrado"
        )
    
    # Convertir el diccionario a un objeto Usuario
    try:
        # Asegurarnos de que los tipos de datos son correctos
        processed_dict = {
            "_id": str(usuario_dict["_id"]) if "_id" in usuario_dict else None,
            "nombres": str(usuario_dict.get("nombres", "")),
            "num_cedula": int(usuario_dict.get("num_cedula", 0)),
            "salario": float(usuario_dict.get("salario", 0.0)),
            "hashed_password": str(usuario_dict.get("hashed_password", "")),
            "pension_descontada": bool(usuario_dict.get("pension_descontada", False)),
            "salud_descontada": bool(usuario_dict.get("salud_descontada", False)),
            "rol": str(usuario_dict.get("rol", RolesUsuario.USUARIO))
        }

        # Validar que los campos requeridos no están vacíos
        if not processed_dict["nombres"] or not processed_dict["hashed_password"]:
            raise ValueError("Faltan campos requeridos en el usuario")

        return Usuario(**processed_dict)
    except (ValueError, TypeError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error al procesar datos del usuario: {str(e)}"
        )


@usuario.post("/empleados", response_description="Empleado guardado", response_model=Usuario)
async def guardar_usuario(usuario: Usuario = Body(...)):
    usuario_existente = await conn["empleados"].find_one({"num_cedula": usuario.num_cedula})

    if usuario_existente is not None:
        raise HTTPException(
            status_code=400, detail=f"Empleado con cedula {usuario.num_cedula} ya existe"
        )

    usuario.hashed_password = get_password_hash(usuario.hashed_password)
    # usuario.rol = RolesUsuario.USUARIO
    
    usuario_dict = jsonable_encoder(usuario)
    nuevo_usuario = await conn["empleados"].insert_one(usuario_dict)
    
    # Recuperar el usuario recién creado directamente de la base de datos
    usuario_creado_dict = await conn["empleados"].find_one({"_id": nuevo_usuario.inserted_id})
    if usuario_creado_dict:
        try:
            # Procesar el diccionario para crear un objeto Usuario
            processed_dict = {
                "_id": str(usuario_creado_dict["_id"]) if "_id" in usuario_creado_dict else None,
                "nombres": str(usuario_creado_dict.get("nombres", "")),
                "num_cedula": int(usuario_creado_dict.get("num_cedula", 0)),
                "salario": float(usuario_creado_dict.get("salario", 0.0)),
                "hashed_password": str(usuario_creado_dict.get("hashed_password", "")),
                "pension_descontada": bool(usuario_creado_dict.get("pension_descontada", False)),
                "salud_descontada": bool(usuario_creado_dict.get("salud_descontada", False)),
                "rol": str(usuario_creado_dict.get("rol", RolesUsuario.USUARIO))
            }
            
            usuario_creado = Usuario(**processed_dict)
            usuario_creado = await check_super_user(usuario_creado)

            return usuario_creado
            
        except (ValueError, TypeError) as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Error al procesar datos del usuario: {str(e)}"
            )
    
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Error al crear el usuario"
    )


@usuario.put("/empleados/{usuario_id}", response_description="Empleado actualizado", response_model=Usuario)
async def actualizar_usuario(
    usuario_id: str,
    usuario: ActualizarUsuario = Body(...),
    current_user: Usuario = Depends(get_current_user)
):
    if current_user.rol != "admin" and str(current_user.usuario_id) != usuario_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="No tiene permisos para actualizar estos datos"
        )

    usuario_dict = {datos: valor for datos, valor in usuario.model_dump().items()
                   if valor is not None}
    
    if len(usuario_dict) >= 1:
        update_result = await conn["empleados"].update_one({"_id": usuario_id}, {"$set": usuario_dict})

        if update_result.modified_count == 1:
            return await obtener_usuario_por_id(usuario_id, current_user)

    return await obtener_usuario_por_id(usuario_id, current_user)


@usuario.delete("/empleados/{usuario_id}", response_description="Empleado eliminado")
async def eliminar_usuario_por_id(
    usuario_id: str,
    current_user: Usuario = Depends(require_role(["admin"]))
):
    usuario_eliminado = await conn["empleados"].delete_one({"_id": usuario_id})
    if usuario_eliminado.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(
        status_code=404, detail=f"Empleado con id {usuario_id} no encontrado")
