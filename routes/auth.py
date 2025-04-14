from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from models.Usuario import Usuario
from config.db import conn
from auth import verify_password, create_access_token


auth = APIRouter()

@auth.post("/token")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint para autenticación de usuarios.
    Retorna un token JWT si las credenciales son correctas.
    """
    # Buscar usuario por número de cédula (que usaremos como username)
    user_dict = await conn["empleados"].find_one({"num_cedula": int(form_data.username)})
    if not user_dict:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    user = Usuario(**user_dict)
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales incorrectas",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Crear token de acceso
    access_token = create_access_token(
        data={"sub": str(user.num_cedula), "rol": user.rol}
    )
    
    return {"access_token": access_token, "token_type": "bearer"}