from sqlalchemy import Column, Integer, String, Date, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, nullable=False)
    asunto = Column(String, nullable=False)
    tipo = Column(String, nullable=False)  # "judicial" o "no_judicial"
    fecha_inicio = Column(Date, nullable=False)
    ultima_actividad = Column(String, nullable=True)
    fecha_ultima_actividad = Column(Date, nullable=True)

    # Campos solo para tareas judiciales
    fecha_notificacion = Column(Date, nullable=True)
    dias_para_retirar_copias = Column(Integer, nullable=True)  # ej: 3 días
    fecha_limite_retirar_copias = Column(Date, nullable=True)
    fecha_limite_acto = Column(Date, nullable=True)

    # Estado y vencimientos
    estado = Column(String, default="pendiente")  # pendiente, en curso, finalizada
    vencida = Column(Boolean, default=False)