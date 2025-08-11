from datetime import date, timedelta
from typing import Optional, Iterable
from sqlalchemy.orm import Session
from sqlalchemy import desc

from models import Tarea, HistorialTarea
from schemas import TareaCreate, TareaUpdate, HistorialTareaCreate

# ---------------- Utilidades de fecha ----------------

def _is_weekend(d: date) -> bool:
    return d.weekday() >= 5  # 5 = sábado, 6 = domingo


def sumar_dias_corridos(fecha_base: date, dias: int) -> date:
    return fecha_base + timedelta(days=dias)


def sumar_dias_habiles_uy(fecha_base: date, dias: int, feriados: Optional[Iterable[date]] = None) -> date:
    feriados = set(feriados or [])
    d = fecha_base
    added = 0
    while added < dias:
        d += timedelta(days=1)
        if _is_weekend(d) or d in feriados:
            continue
        added += 1
    return d

# ---------------- TAREAS ----------------

def _normalize_tarea_payload(data: dict) -> dict:
    # Compatibilidad: descripcion → tarea
    if "tarea" not in data and "descripcion" in data:
        data["tarea"] = data.pop("descripcion")
    # Filtrar solo columnas reales del modelo Tarea
    valid_cols = {c.name for c in Tarea.__table__.columns}
    return {k: v for k, v in data.items() if k in valid_cols}


def obtener_todas_las_tareas(db: Session) -> list[Tarea]:
    return db.query(Tarea).order_by(desc(Tarea.fecha_registro), desc(Tarea.id)).all()


def obtener_tarea_por_id(db: Session, tarea_id: int) -> Optional[Tarea]:
    return db.query(Tarea).filter(Tarea.id == tarea_id).first()


def crear_tarea(db: Session, payload: TareaCreate) -> Tarea:
    data = _normalize_tarea_payload(payload.model_dump(exclude_unset=True))
    tarea = Tarea(**data)
    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return tarea


def actualizar_tarea(db: Session, tarea_id: int, payload: TareaUpdate) -> Optional[Tarea]:
    tarea = obtener_tarea_por_id(db, tarea_id)
    if not tarea:
        return None
    data = _normalize_tarea_payload(payload.model_dump(exclude_unset=True))
    for k, v in data.items():
        setattr(tarea, k, v)
    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    return tarea


def eliminar_tarea(db: Session, tarea_id: int) -> None:
    tarea = obtener_tarea_por_id(db, tarea_id)
    if tarea:
        db.delete(tarea)
        db.commit()

# ---------------- HISTORIAL ----------------

def obtener_historial_por_tarea(db: Session, tarea_id: int) -> list[HistorialTarea]:
    return (
        db.query(HistorialTarea)
        .filter(HistorialTarea.tarea_id == tarea_id)
        .order_by(desc(HistorialTarea.fecha_registro), desc(HistorialTarea.id))
        .all()
    )


def _normalize_fecha_registro(evento: HistorialTareaCreate) -> date:
    # Preferimos fecha_registro si viene, si no cae a fecha (compatibilidad)
    return (evento.fecha_registro or evento.fecha or date.today())


def agregar_evento_historial(db: Session, tarea_id: int, evento: HistorialTareaCreate) -> HistorialTarea:
    fecha_registro = _normalize_fecha_registro(evento)
    h = HistorialTarea(
        tarea_id=tarea_id,
        descripcion=(evento.descripcion or ""),
        fecha_registro=fecha_registro,
        etapa_procesal=evento.etapa_procesal,
        fecha_limite=evento.fecha_limite,
        requiere_retiro_copias=bool(evento.requiere_retiro_copias),
    )
    db.add(h)
    db.commit()
    db.refresh(h)
    return h


def editar_evento_historial(db: Session, evento_id: int, datos: HistorialTareaCreate) -> Optional[HistorialTarea]:
    h = db.query(HistorialTarea).filter(HistorialTarea.id == evento_id).first()
    if not h:
        return None

    data = datos.model_dump(exclude_unset=True)

    # Normalizamos fechas de entrada
    if data.get("fecha") and not data.get("fecha_registro"):
        data["fecha_registro"] = data.pop("fecha")

    for k in ("descripcion", "fecha_registro", "etapa_procesal", "fecha_limite", "requiere_retiro_copias"):
        if k in data:
            setattr(h, k, data[k])

    db.add(h)
    db.commit()
    db.refresh(h)
    return h