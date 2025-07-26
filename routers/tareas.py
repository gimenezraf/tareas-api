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

@router.delete("/tareas/{tarea_id}", response_model=schemas.Tarea)
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    tarea = crud.obtener_tarea(db, tarea_id=tarea_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return crud.eliminar_tarea(db, tarea_id=tarea_id)

@router.put("/tareas/{tarea_id}", response_model=schemas.Tarea)
def actualizar_tarea(tarea_id: int, tarea: schemas.TareaCreate, db: Session = Depends(get_db)):
    tarea_actualizada = crud.actualizar_tarea(db, tarea_id, tarea)
    if tarea_actualizada is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea_actualizada

@router.get("/tareas/{tarea_id}", response_model=schemas.Tarea)
def obtener_tarea_por_id(tarea_id: int, db: Session = Depends(get_db)):
    tarea = crud.obtener_tarea(db, tarea_id=tarea_id)
    if tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return tarea