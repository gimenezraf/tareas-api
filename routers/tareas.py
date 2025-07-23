from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from database import SessionLocal
import crud
import schemas

router = APIRouter()

# Dependencia para obtener una sesión de base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/tareas", response_model=schemas.Tarea)
def crear_tarea(tarea: schemas.TareaCreate, db: Session = Depends(get_db)):
    return crud.crear_tarea(db=db, tarea=tarea)

@router.get("/tareas", response_model=List[schemas.Tarea])
def listar_tareas(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return crud.obtener_tareas(db=db, skip=skip, limit=limit)