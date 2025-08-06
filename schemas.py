from pydantic import BaseModel
from datetime import date
from typing import Optional, List

class HistorialTareaBase(BaseModel):
    descripcion: str
    fecha: date
    etapa_procesal: Optional[str] = None
    fecha_limite: Optional[date] = None
    requiere_retiro_copias: Optional[bool] = False

class HistorialTareaCreate(HistorialTareaBase):
    pass

class HistorialTarea(HistorialTareaBase):
    id: int
    tarea_id: int
    etapa_procesal: Optional[str] = None
    fecha_limite: Optional[date] = None
    requiere_retiro_copias: Optional[bool] = False

    class Config:
        from_attributes = True

class TareaBase(BaseModel):
    cliente: Optional[str] = None
    descripcion: str
    asunto: Optional[str] = None
    estructura_procesal: Optional[str] = None
    rol_procesal: Optional[str] = None
    sede_judicial: Optional[str] = None
    fecha_registro: Optional[date] = None
    fecha_ultima_actividad: Optional[date] = None
    fecha_notificacion: Optional[date] = None
    fecha_limite_acto: Optional[date] = None
    etapa_procesal: Optional[str] = None
    fecha_formalizacion: Optional[date] = None
    iue: Optional[str] = None
    nunc: Optional[str] = None

class TareaCreate(TareaBase):
    pass

class TareaUpdate(TareaBase):
    pass

class Tarea(TareaBase):
    id: int
    historial: List[HistorialTarea] = []

    class Config:
        from_attributes = True
