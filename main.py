from fastapi import FastAPI
from fastapi.responses import JSONResponse
from routers import tareas

class CustomJSONResponse(JSONResponse):
    media_type = "application/json; charset=utf-8"

app = FastAPI(default_response_class=CustomJSONResponse)

app.include_router(tareas.router)