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
    # Crear automáticamente una entrada en el historial si la tarea tiene actividad inicial
    if tarea.ultima_actividad and tarea.fecha_ultima_actividad:
        db_evento = HistorialTarea(
            tarea_id=db_tarea.id,
            descripcion=tarea.ultima_actividad,
            fecha=tarea.fecha_ultima_actividad
        )
        db.add(db_evento)
        db.commit()
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

    db_tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if db_tarea and (not db_tarea.fecha_ultima_actividad or db_evento.fecha.date() > db_tarea.fecha_ultima_actividad):
        db_tarea.ultima_actividad = db_evento.descripcion
        db_tarea.fecha_ultima_actividad = db_evento.fecha.date()
        db.commit()
        db.refresh(db_tarea)

    return db_evento

# Obtener historial por tarea
def obtener_historial_por_tarea(db: Session, tarea_id: int):
    return (
        db.query(HistorialTarea)
        .filter(HistorialTarea.tarea_id == tarea_id)
        .order_by(HistorialTarea.fecha.desc())
        .all()
    )

def editar_evento_historial(db: Session, evento_id: int, datos: HistorialTareaCreate):
    evento = db.query(HistorialTarea).filter(HistorialTarea.id == evento_id).first()
    if not evento:
        return None

    evento.descripcion = datos.descripcion
    evento.fecha = datos.fecha
    db.commit()
    db.refresh(evento)

    # Actualizar la tarea si este evento es ahora el más reciente
    db_tarea = db.query(Tarea).filter(Tarea.id == evento.tarea_id).first()
    evento_mas_reciente = db.query(HistorialTarea).filter(
        HistorialTarea.tarea_id == evento.tarea_id
    ).order_by(HistorialTarea.fecha.desc()).first()

    if db_tarea and evento_mas_reciente and evento_mas_reciente.id == evento.id:
        db_tarea.ultima_actividad = evento.descripcion
        db_tarea.fecha_ultima_actividad = evento.fecha
        db.commit()
        db.refresh(db_tarea)

    return evento