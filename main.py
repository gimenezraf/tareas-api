from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from schemas import HistorialTareaResponse, HistorialTareaCreate
from database import get_db
import crud

router = APIRouter()

@router.get("/tareas/{tarea_id}/historial", response_model=List[HistorialTareaResponse])
def obtener_historial(tarea_id: int, db: Session = Depends(get_db)):
    return crud.obtener_historial(db, tarea_id)

@router.post("/tareas/{tarea_id}/historial", response_model=HistorialTareaResponse)
def agregar_historial(tarea_id: int, entrada: HistorialTareaCreate, db: Session = Depends(get_db)):
    return crud.agregar_evento_historial(db, tarea_id, entrada.descripcion)