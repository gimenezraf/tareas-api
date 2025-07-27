from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import tareas

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://tareas-frontend-kwhq.vercel.app"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(tareas.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}