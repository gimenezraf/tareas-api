from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship, declarative_base
from datetime import date

Base = declarative_base()

# MODELOS SQLALCHEMY
class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, nullable=True)
    descripcion = Column(String)
    asunto = Column(String, nullable=True)
    tarea_pendiente = Column(String, nullable=True)
    estructura_procesal = Column(String, nullable=True)
    rol_procesal = Column(String, nullable=True)
    sede_judicial = Column(String, nullable=True)
    fecha_registro = Column(Date, default=date.today)
    fecha_ultima_actividad = Column(Date, nullable=True)
    fecha_notificacion = Column(Date, nullable=True)
    fecha_limite_acto = Column(Date, nullable=True)
    etapa_procesal = Column(String, nullable=True)
    fecha_formalizacion = Column(Date, nullable=True)
    iue = Column(String, nullable=True)
    nunc = Column(String, nullable=True)

    historial = relationship("HistorialTarea", back_populates="tarea", cascade="all, delete-orphan")


class HistorialTarea(Base):
    __tablename__ = "historial_tarea"

    id = Column(Integer, primary_key=True, index=True)
    tarea_id = Column(Integer, ForeignKey("tareas.id"))
    descripcion = Column(String)
    fecha = Column(Date)
    etapa_procesal = Column(String, nullable=True)
    fecha_limite = Column(Date, nullable=True)
    requiere_retiro_copias = Column(Boolean, default=False)

    tarea = relationship("Tarea", back_populates="historial")
