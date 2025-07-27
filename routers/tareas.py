from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas

router = APIRouter()

@router.get("/tareas", response_model=list[schemas.Tarea])
def listar_tareas(db: Session = Depends(get_db)):
    return crud.obtener_todas_las_tareas(db)

@router.get("/tareas/{tarea_id}", response_model=schemas.Tarea)
def obtener_tarea(tarea_id: int, db: Session = Depends(get_db)):
    db_tarea = crud.obtener_tarea_por_id(db, tarea_id)
    if db_tarea is None:
        raise HTTPException(status_code=404, detail="Tarea no encontrada")
    return db_tarea

@router.post("/tareas", response_model=schemas.Tarea)
def crear_tarea(tarea: schemas.TareaCreate, db: Session = Depends(get_db)):
    return crud.crear_tarea(db, tarea)

@router.put("/tareas/{tarea_id}", response_model=schemas.Tarea)
def actualizar_tarea(tarea_id: int, tarea: schemas.TareaCreate, db: Session = Depends(get_db)):
    return crud.actualizar_tarea(db, tarea_id, tarea)

@router.delete("/tareas/{tarea_id}")
def eliminar_tarea(tarea_id: int, db: Session = Depends(get_db)):
    crud.eliminar_tarea(db, tarea_id)
    return {"mensaje": "Tarea eliminada"}

@router.get("/tareas/{tarea_id}/historial", response_model=list[schemas.HistorialTarea])
def obtener_historial(tarea_id: int, db: Session = Depends(get_db)):
    return crud.obtener_historial_por_tarea(db, tarea_id)

@router.post("/tareas/{tarea_id}/historial", response_model=schemas.HistorialTarea)
def agregar_historial(tarea_id: int, evento: schemas.HistorialTareaCreate, db: Session = Depends(get_db)):
    return crud.agregar_evento_historial(db, tarea_id, evento)
