from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.usuarios import usuario

app = FastAPI()

app.include_router(usuario)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://programa-contable.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
