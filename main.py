from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers import tareas

class CustomJSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

from fastapi.middleware.cors import CORSMiddleware

origins = [
    "https://tareas-frontend-kwhq.vercel.app",  # Dominio del frontend en Vercel
]

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Solo permite este origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app = FastAPI(default_response_class=CustomJSONResponse)

app.include_router(tareas.router)