from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from models import Tarea

from database import SessionLocal
import crud
import schemas

from models import HistorialTarea
from schemas import HistorialTareaCreate, HistorialTareaResponse

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

@router.get("/tareas/{tarea_id}/historial", response_model=List[HistorialTareaResponse])
def obtener_historial(tarea_id: int, db: Session = Depends(get_db)):
    historial = db.query(HistorialTarea).filter(HistorialTarea.tarea_id == tarea_id).order_by(HistorialTarea.fecha.desc()).all()
    return historial

@router.post("/tareas/{tarea_id}/historial", response_model=HistorialTareaResponse)
def agregar_historial(tarea_id: int, entrada: HistorialTareaCreate, db: Session = Depends(get_db)):
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")

    nuevo_evento = HistorialTarea(tarea_id=tarea_id, descripcion=entrada.descripcion, fecha=entrada.fecha or datetime.utcnow())
    db.add(nuevo_evento)
    db.commit()
    db.refresh(nuevo_evento)
    return nuevo_evento    