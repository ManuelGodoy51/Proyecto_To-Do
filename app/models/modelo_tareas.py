from datetime import datetime

from sqlalchemy import Column, Integer, String, TIMESTAMP, Date
from app.models.database import Base

class Tareas(Base):
    __tablename__ = "tareas"

    id = Column(Integer, primary_key = True, index = True)
    usuario = Column(String(length=20), index = True, nullable = False)
    titulo = Column(String(length=40), index = True, nullable = False)
    descripcion = Column(String(length=150), index = True, nullable = False)
    fecha_vencimiento = Column(Date, nullable = False)
    fecha_creacion = Column(TIMESTAMP, default=datetime.utcnow, nullable = False)
    estado = Column(String(length=100), index = True, nullable = False)
