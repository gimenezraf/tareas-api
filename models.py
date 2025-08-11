from sqlalchemy import Column, Integer, String, Date, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from datetime import date
from database import Base

# MODELOS SQLALCHEMY
class Tarea(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key=True, index=True)
    cliente = Column(String, nullable=True)
    # título/descripcion corta de la tarea (coincide con frontend)
    tarea = Column(String, nullable=True)
    asunto = Column(String, nullable=True)
    tarea_pendiente = Column(String, nullable=True)

    # Procesal / judicial
    estructura_procesal = Column(String, nullable=True)
    rol_procesal = Column(String, nullable=True)
    juzgado = Column(String, nullable=True)  # antes sede_judicial
    iue = Column(String, nullable=True)
    nunc = Column(String, nullable=True)

    # Fechas
    fecha_registro = Column(Date, default=date.today)
    fecha_ultima_actividad = Column(Date, nullable=True)
    fecha_notificacion = Column(Date, nullable=True)
    # Usamos fecha_limite general (coincide con tu tabla existente)
    fecha_limite = Column(Date, nullable=True)
    etapa_procesal = Column(String, nullable=True)
    fecha_formalizacion = Column(Date, nullable=True)

    tipo_tarea = Column(String, nullable=True)
    fecha_inicio = Column(Date, nullable=True)
    ultima_actividad = Column(Date, nullable=True)
    estado = Column(String, nullable=True)

    historial = relationship(
        "HistorialTarea",
        back_populates="tarea",
        cascade="all, delete-orphan",
        order_by="desc(HistorialTarea.fecha_registro)"
    )


class HistorialTarea(Base):
    __tablename__ = "historial_tareas"  # nombre real en Railway

    id = Column(Integer, primary_key=True, index=True)
    tarea_id = Column(Integer, ForeignKey("tareas.id"), nullable=False, index=True)
    descripcion = Column(String, nullable=False)

    # Campo de fecha principal alineado con la BD
    fecha_registro = Column(Date, nullable=False, default=date.today)

    # Campos opcionales por etapa
    etapa_procesal = Column(String, nullable=True)
    fecha_limite = Column(Date, nullable=True)
    requiere_retiro_copias = Column(Boolean, default=False, nullable=False)

    tarea = relationship("Tarea", back_populates="historial")
