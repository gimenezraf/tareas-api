from models import Tarea, HistorialTarea
# Importar estructuras_procesales para el bloque extra:
from estructuras import estructuras_procesales
# Suposición: función crear_tarea a agregar al final el bloque solicitado
# (Esta función no existe en el fragmento, pero la instrucción indica modificarla)

# Si la función crear_tarea ya existe, añadir al final, antes del return:

# ... código de crear_tarea ...

# --- INICIO BLOQUE A AGREGAR AL FINAL DE crear_tarea ---
    from estructuras import estructuras_procesales

    if nueva_tarea.estructura_procesal:
        etapas = estructuras_procesales.get(nueva_tarea.estructura_procesal.lower())
        if etapas:
            primera_etapa = etapas[0]
            fecha_base = nueva_tarea.fecha_notificacion or nueva_tarea.fecha_registro
            if primera_etapa["tipo_plazo"] == "habiles":
                fecha_limite = sumar_dias_habiles_uy(fecha_base, primera_etapa["plazo"])
            else:
                fecha_limite = sumar_dias_corridos(fecha_base, primera_etapa["plazo"])

            evento_inicial = HistorialTarea(
                tarea_id=nueva_tarea.id,
                descripcion=primera_etapa["nombre"],
                etapa_procesal=primera_etapa["nombre"],
                fecha=fecha_base,
                fecha_limite=fecha_limite
            )
            db.add(evento_inicial)
            db.commit()
            db.refresh(evento_inicial)

            # Actualizar tarea con los datos del primer evento
            nueva_tarea.etapa_procesal = evento_inicial.etapa_procesal
            nueva_tarea.fecha_limite_acto = evento_inicial.fecha_limite
            db.add(nueva_tarea)
            db.commit()
            db.refresh(nueva_tarea)
# --- FIN BLOQUE A AGREGAR ---
from sqlalchemy import Column, Integer, String, Date, ForeignKey
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

    historial = relationship("HistorialTarea", back_populates="tarea", cascade="all, delete-orphan")


class HistorialTarea(Base):
    __tablename__ = "historial_tarea"

    id = Column(Integer, primary_key=True, index=True)
    tarea_id = Column(Integer, ForeignKey("tareas.id"))
    descripcion = Column(String)
    fecha = Column(Date)
    etapa_procesal = Column(String, nullable=True)
    fecha_limite = Column(Date, nullable=True)

    tarea = relationship("Tarea", back_populates="historial")


# Funciones para sumar días hábiles y corridos en Uruguay
import holidays
from datetime import timedelta

# Lista de feriados en Uruguay
feriados_uy = holidays.Uruguay()

def es_habil(date_obj):
    return date_obj.weekday() < 5 and date_obj not in feriados_uy

def sumar_dias_habiles_uy(fecha_inicio, dias):
    contador = 0
    fecha_actual = fecha_inicio
    while contador < dias:
        fecha_actual += timedelta(days=1)
        if es_habil(fecha_actual):
            contador += 1
    return fecha_actual

def sumar_dias_corridos(fecha_inicio, dias):
    return fecha_inicio + timedelta(days=dias)


# Nueva función auxiliar para actualizar etapa_procesal y fecha_limite
def actualizar_etapa_y_limite(db, tarea, evento):
    # Ejemplo de lógica (adaptar según lo que esté en tareas.py)
    # Si el evento tiene etapa_procesal y fecha_limite, respetarlos
    if evento.etapa_procesal is not None and evento.fecha_limite is not None:
        tarea.etapa_procesal = evento.etapa_procesal
        tarea.fecha_limite_acto = evento.fecha_limite
    else:
        # Si no, asignar valores por defecto o calculados
        # Por ejemplo, asignar etapa_procesal según descripción o fecha
        # Esta lógica debe ser la que estaba en el router agregar_historial
        # Aquí un ejemplo genérico:
        tarea.etapa_procesal = evento.descripcion or tarea.etapa_procesal
        # Para fecha_limite, podría ser sumar días hábiles o corridos desde fecha del evento
        if evento.fecha:
            tarea.fecha_limite_acto = sumar_dias_habiles_uy(evento.fecha, 5)
            evento.fecha_limite = tarea.fecha_limite_acto
        else:
            evento.fecha_limite = tarea.fecha_limite_acto

    db.add(tarea)
    db.commit()
    db.refresh(tarea)
    db.refresh(evento)


# Suposición: función agregar_evento_historial ya existe, se modifica para incluir llamada a actualizar_etapa_y_limite
def agregar_evento_historial(db, tarea_id, evento):
    from models import Tarea, HistorialTarea  # Ajustar import según estructura real

    tarea = db.query(Tarea).filter(Tarea.id == tarea_id).first()
    if not tarea:
        return None

    evento_db = HistorialTarea(
        tarea_id=tarea_id,
        descripcion=evento.descripcion,
        fecha=evento.fecha,
        etapa_procesal=evento.etapa_procesal,
        fecha_limite=evento.fecha_limite
    )
    db.add(evento_db)
    db.commit()
    db.refresh(evento_db)

    # Actualizar etapa_procesal y fecha_limite tanto en tarea como en evento
    actualizar_etapa_y_limite(db, tarea, evento_db)

    return evento_db


# Suposición: función editar_evento_historial ya existe, se modifica para permitir actualizar etapa_procesal y fecha_limite
def editar_evento_historial(db, evento_id, datos):
    from models import HistorialTarea  # Ajustar import según estructura real

    evento = db.query(HistorialTarea).filter(HistorialTarea.id == evento_id).first()
    if not evento:
        return None

    if datos.descripcion is not None:
        evento.descripcion = datos.descripcion
    if datos.fecha is not None:
        evento.fecha = datos.fecha
    if datos.etapa_procesal is not None:
        evento.etapa_procesal = datos.etapa_procesal
    if datos.fecha_limite is not None:
        evento.fecha_limite = datos.fecha_limite

    db.add(evento)
    db.commit()
    db.refresh(evento)

    # Actualizar tarea también si es necesario
    tarea = evento.tarea
    if tarea:
        actualizar_etapa_y_limite(db, tarea, evento)

    return evento