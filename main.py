from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from routers import tareas

class CustomJSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

origins = [
    "https://tareas-frontend-kwhq.vercel.app",  # Dominio del frontend en Vercel
]

# Solo una vez se debe crear la instancia de FastAPI
app = FastAPI(default_response_class=CustomJSONResponse)

# Agregar CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Solo permite el frontend desde Vercel
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir el router de tareas
app.include_router(tareas.router)