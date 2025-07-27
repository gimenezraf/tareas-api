from sqlalchemy.orm import Session
from models import Tarea, HistorialTarea
from schemas import TareaCreate, TareaUpdate, HistorialTareaCreate
from datetime import datetime

# Crear una nueva tarea
def crear_tarea(db: Session, tarea: TareaCreate):
    db_tarea = Tarea(**tarea.dict())
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

# Obtener todas las tareas
def obtener_todas_las_tareas(db: Session):
    return db.query(Tarea).all()

# Obtener una tarea por ID
def obtener_tarea_por_id(db: Session, tarea_id: int):
    return db.query(Tarea).filter(Tarea.id == tarea_id).first()

# Actualizar una tarea
def actualizar_tarea(db: Session, tarea_id: int, tarea: TareaUpdate):
    db_tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if db_tarea:
        for key, value in tarea.dict(exclude_unset=True).items():
            setattr(db_tarea, key, value)
        db.commit()
        db.refresh(db_tarea)
    return db_tarea

# Eliminar una tarea
def eliminar_tarea(db: Session, tarea_id: int):
    db_tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if db_tarea:
        db.delete(db_tarea)
        db.commit()
    return db_tarea

# Agregar evento al historial
def agregar_evento_historial(db: Session, tarea_id: int, evento: HistorialTareaCreate):
    db_evento = HistorialTarea(
        tarea_id=tarea_id,
        descripcion=evento.descripcion,
        fecha=evento.fecha or datetime.utcnow()
    )
    db.add(db_evento)
    db.commit()
    db.refresh(db_evento)
    return db_evento

# Obtener historial por tarea
def obtener_historial_por_tarea(db: Session, tarea_id: int):
    return (
        db.query(HistorialTarea)
        .filter(HistorialTarea.tarea_id == tarea_id)
        .order_by(HistorialTarea.fecha.desc())
        .all()
    )