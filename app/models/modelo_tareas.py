from sqlalchemy import column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Tareas(Base):
    __tablename__ = "tareas"

    id = column(Integer, primary_key = True, index = True)
    usuario = column()
