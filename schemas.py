from pydantic import BaseModel
from datetime import date
from typing import Optional, List

# ---------------- HISTORIAL ----------------
class HistorialTareaBase(BaseModel):
    descripcion: Optional[str] = None
    # Aceptamos "fecha" desde el frontend pero la normalizamos en CRUD a fecha_registro
    fecha: Optional[date] = None
    fecha_registro: Optional[date] = None
    etapa_procesal: Optional[str] = None
    fecha_limite: Optional[date] = None
    requiere_retiro_copias: Optional[bool] = False

class HistorialTareaCreate(HistorialTareaBase):
    pass

class HistorialTarea(HistorialTareaBase):
    id: int
    tarea_id: int

    class Config:
        from_attributes = True

# ---------------- TAREAS ----------------
class TareaBase(BaseModel):
    cliente: Optional[str] = None
    # Compat: en DB la columna es "tarea"; aceptamos "descripcion" desde el frontend
    tarea: Optional[str] = None
    descripcion: Optional[str] = None
    asunto: Optional[str] = None
    tarea_pendiente: Optional[str] = None

    estructura_procesal: Optional[str] = None
    rol_procesal: Optional[str] = None
    juzgado: Optional[str] = None
    iue: Optional[str] = None
    nunc: Optional[str] = None

    fecha_registro: Optional[date] = None
    fecha_ultima_actividad: Optional[date] = None
    fecha_notificacion: Optional[date] = None
    fecha_limite: Optional[date] = None
    etapa_procesal: Optional[str] = None
    fecha_formalizacion: Optional[date] = None

    tipo_tarea: Optional[str] = None
    fecha_inicio: Optional[date] = None
    ultima_actividad: Optional[date] = None
    estado: Optional[str] = None

class TareaCreate(TareaBase):
    pass

class TareaUpdate(TareaBase):
    pass

class Tarea(TareaBase):
    id: int
    historial: List[HistorialTarea] = []

    class Config:
        from_attributes = True
