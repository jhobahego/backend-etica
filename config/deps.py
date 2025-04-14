from typing import List
from fastapi import Depends, HTTPException, status
from models.Usuario import Usuario, RolesUsuario
from auth import oauth2_scheme, verify_token, verify_password
from config.db import conn
from decouple import config


async def get_current_user(token: str = Depends(oauth2_scheme)) -> Usuario:
    """
    Dependency para obtener el usuario actual a partir del token JWT.
    Verifica si el usuario es un superusuario basado en las variables de entorno.
    Raises:
        HTTPException: Si el token es inválido o el usuario no existe
    Returns:
        Usuario: El usuario autenticado
    """
    payload = verify_token(token)
    sub = payload.get("sub")
    if not sub:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No se pudo validar las credenciales",
            headers={"WWW-Authenticate": "Bearer"},
        )

    num_cedula = int(sub)
    
    user_dict = await conn["empleados"].find_one({"num_cedula": num_cedula})
    if user_dict is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = Usuario(**user_dict)

    user = await check_super_user(user)

    return user


async def check_super_user(user: Usuario) -> Usuario:
    """
    Verifica si el usuario debe ser un superusuario basado en las variables de entorno.
    Si coincide la cédula y la contraseña, actualiza su rol a admin.
    Args:
        user: Usuario a verificar
    Returns:
        Usuario: El mismo usuario, potencialmente con rol actualizado a admin
    """
    try:
        super_user_cedula = int(config('SUPER_USER_CEDULA'))
        super_user_password = str(config('SUPER_USER_PASSWORD'))

        if user.num_cedula == super_user_cedula:
            # Si la cédula coincide, verificamos la contraseña
            if verify_password(str(super_user_password), str(user.hashed_password)):
                # Actualizar el rol a admin si no lo es ya
                if user.rol != RolesUsuario.ADMIN:
                    await conn["empleados"].update_one(
                        {"num_cedula": user.num_cedula},
                        {"$set": {"rol": RolesUsuario.ADMIN}}
                    )
                    user.rol = RolesUsuario.ADMIN
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error al verificar superusuario",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    return user


def require_role(required_roles: List[str]):
    """
    Dependency factory para requerir roles específicos.
    Args:
        required_roles: Lista de roles permitidos
    Returns:
        Dependency que verifica si el usuario tiene uno de los roles requeridos
    """
    async def role_checker(current_user: Usuario = Depends(get_current_user)):
        if current_user.rol not in required_roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No tiene permisos suficientes para realizar esta acción"
            )
        return current_user

    return role_checker
