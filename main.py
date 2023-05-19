from fastapi import FastAPI
from routes.usuarios import usuario

app = FastAPI()

app.include_router(usuario)