from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.usuarios import usuario

app = FastAPI()

app.include_router(usuario)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "https://6467d957af410b0cb2767d0e--taupe-melba-0df3aa.netlify.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
