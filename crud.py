from sqlalchemy.orm import Session
from models import Tarea
from schemas import TareaCreate

def crear_tarea(db: Session, tarea: TareaCreate):
    db_tarea = Tarea(**tarea.dict())
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

def obtener_tareas(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Tarea).offset(skip).limit(limit).all()

def obtener_tarea(db: Session, tarea_id: int):
    return db.query(Tarea).filter(Tarea.id == tarea_id).first()

def eliminar_tarea(db: Session, tarea_id: int):
    tarea = obtener_tarea(db, tarea_id)
    if tarea:
        db.delete(tarea)
        db.commit()
    return tarea

def actualizar_tarea(db: Session, tarea_id: int, tarea_data: TareaCreate):
    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if tarea:
        for key, value in tarea_data.dict().items():
            setattr(tarea, key, value)
        db.commit()
        db.refresh(tarea)
    return tarea