from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database import get_db
import crud
import schemas
from models import HistorialTarea
from datetime import timedelta
from crud import sumar_dias_habiles_uy, sumar_dias_corridos

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
    db_evento = crud.agregar_evento_historial(db, tarea_id, evento)

    # Si el evento agregado tiene una etapa procesal reconocida dentro de la estructura,
    # actualizar el nombre de la tarea y su fecha límite
    tarea = crud.obtener_tarea_por_id(db, tarea_id)
    if tarea and tarea.estructura_procesal:
        from estructuras import estructuras_procesales
        etapas = estructuras_procesales.get(tarea.estructura_procesal.lower())
        if etapas:
            for etapa in etapas:
                if etapa["nombre"].lower() in (evento.descripcion or "").lower():
                    fecha_base = evento.fecha
                    if etapa["tipo_plazo"] == "habiles":
                        nueva_fecha_limite = crud.sumar_dias_habiles_uy(fecha_base, etapa["plazo"])
                    else:
                        nueva_fecha_limite = crud.sumar_dias_corridos(fecha_base, etapa["plazo"])
                    tarea.fecha_limite_acto = nueva_fecha_limite
                    tarea.etapa_procesal = etapa["nombre"]
                    evento.fecha_limite = nueva_fecha_limite
                    db.add(tarea)
                    db.add(db_evento)
                    db.commit()
                    db.refresh(tarea)
                    db.refresh(db_evento)
                    break

    return db_evento


# Nuevo endpoint para editar un evento del historial
@router.put("/historial/{evento_id}", response_model=schemas.HistorialTarea)
def editar_historial(evento_id: int, datos: schemas.HistorialTareaCreate, db: Session = Depends(get_db)):
    evento = crud.editar_evento_historial(db, evento_id, datos)
    if not evento:
        raise HTTPException(status_code=404, detail="Evento no encontrado")
    return evento
