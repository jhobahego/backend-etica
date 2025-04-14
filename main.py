from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from decouple import config

from routes.usuarios import usuario
from routes.auth import auth

app = FastAPI()

app.include_router(usuario)
app.include_router(auth)

FRONTEND_URL = config("FRONTEND_URL")

app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def home():
    return RedirectResponse(url="/docs")
