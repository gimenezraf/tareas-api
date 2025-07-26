from pydantic import BaseModel
from typing import Optional
from datetime import date
from datetime import datetime
from pydantic import BaseModel
from typing import Optional

class HistorialTareaCreate(BaseModel):
    descripcion: str
    fecha: Optional[datetime] = None

class HistorialTareaResponse(BaseModel):
    id: int
    tarea_id: int
    descripcion: str
    fecha: datetime

    class Config:
        orm_mode = True

class TareaBase(BaseModel):
    cliente: str
    asunto: str
    tipo: str  # "judicial" o "no_judicial"
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

class Tarea(TareaBase):
    id: int

    class Config:
        orm_mode = True  # si estás usando Pydantic v1