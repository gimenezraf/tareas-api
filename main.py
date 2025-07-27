from fastapi import FastAPI
from routers import tareas

app = FastAPI()

app.include_router(tareas.router)

@app.get("/ping")
def ping():
    return {"message": "pong"}