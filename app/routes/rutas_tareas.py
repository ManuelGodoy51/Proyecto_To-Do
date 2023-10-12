from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query
from app.database import SessionLocal
from app.models.modelo_tareas import Tareas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/guardar")
def crear_tarea(tarea_data : dict, db : SessionLocal = Depends(get_db)):

    match tarea_data:
        case _ if "usuario" not in tarea_data:
            raise HTTPException(status_code = 400, detail = "El usuario es requerido")
        case _ if "titulo" not in tarea_data:
            raise HTTPException(status_code = 400, detail = "El titulo es requerido")
        case _ if "descripcion" not in tarea_data:
            raise HTTPException(status_code = 400, detail = "La descripcion es requerido")
        case _ if "fecha_vencimiento" not in tarea_data:
            raise HTTPException(status_code = 400, detail = "La fecha de vencimiento es requerido")
        case _ if "estado" not in tarea_data:
            raise HTTPException(status_code = 400, detail = "El estado es requerido")

    fecha_vencimiento_str = tarea_data["fecha_vencimiento"]
    tarea_data["fecha_vencimiento"] = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d").date()

    db_tarea = Tareas(**tarea_data)
    db.add(db_tarea)
    db.commit()
    db.refresh(db_tarea)
    return db_tarea

@router.get("/lista")
def Listar_tareas(usuario: str, estado: str = Query(None), db : SessionLocal = Depends(get_db)):
    if usuario == None or usuario == "":
        raise HTTPException(status_code=400, detail="El usuario es requerido")
    else:
        if estado == None or estado == "":
            print("Entre")
            tareas = db.query(Tareas).filter(Tareas.usuario == usuario).all()
        else:
            tareas = db.query(Tareas).filter(Tareas.usuario == usuario, Tareas.estado == estado).all()

    return tareas