from pydantic import BaseModel
from typing import Optional, List
from datetime import date, datetime

class HistorialTareaBase(BaseModel):
    descripcion: str
    fecha: Optional[datetime] = None

class HistorialTareaCreate(HistorialTareaBase):
    pass

class HistorialTarea(HistorialTareaBase):
    id: int
    tarea_id: int

    class Config:
        from_attributes = True

class TareaBase(BaseModel):
    cliente: str
    asunto: str
    tipo: str
    fecha_inicio: date
    ultima_actividad: Optional[str] = None
    fecha_ultima_actividad: Optional[date] = None
    fecha_notificacion: Optional[date] = None
    dias_para_retirar_copias: Optional[int] = None
    fecha_limite_retirar_copias: Optional[date] = None
    fecha_limite_acto: Optional[date] = None
    estado: Optional[str] = "pendiente"
    vencida: Optional[bool] = False

class TareaCreate(TareaBase):
    pass

class TareaUpdate(TareaBase):
    pass

class Tarea(TareaBase):
    id: int
    historial: List[HistorialTarea] = []

    class Config:
        from_attributes = True
