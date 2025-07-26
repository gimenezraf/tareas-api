from sqlalchemy import Column, Integer, String, Date, Boolean, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

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
    dias_para_retirar_copias = Column(Integer, nullable=True)
    fecha_limite_retirar_copias = Column(Date, nullable=True)
    fecha_limite_acto = Column(Date, nullable=True)

    # Estado y vencimientos
    estado = Column(String, default="pendiente")
    vencida = Column(Boolean, default=False)

    # Relación con historial
    historial = relationship("HistorialTarea", back_populates="tarea", cascade="all, delete-orphan")


class HistorialTarea(Base):
    __tablename__ = "historial_tareas"

    id = Column(Integer, primary_key=True, index=True)
    tarea_id = Column(Integer, ForeignKey("tareas.id"), nullable=False)
    descripcion = Column(String, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow)

    tarea = relationship("Tarea", back_populates="historial")