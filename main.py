from fastapi import FastAPI
from app.models import modelo_tareas
from app.database import engine
from app.routes import rutas_tareas

modelo_tareas.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(rutas_tareas.router, prefix="/tareas", tags=["tareas"])