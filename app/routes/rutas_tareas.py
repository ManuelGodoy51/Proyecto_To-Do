from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends, Query
from app.models.database import SessionLocal
from app.models.modelo_tareas import Tareas

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/guardar")
def Crear_tarea(tarea_data : dict, db : SessionLocal = Depends(get_db)):
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
def Listar_tareas(usuario: str = Query(None), estado: str = Query(None), db : SessionLocal = Depends(get_db)):
    if not usuario and not estado:
        tareas = db.query(Tareas).all()
    elif usuario and not estado:
        tareas = db.query(Tareas).filter(Tareas.usuario == usuario).all()
        if not tareas:
            raise HTTPException(status_code=404, detail="El usuario no posee tareas.")
    elif estado and not usuario:
        tareas = db.query(Tareas).filter(Tareas.estado == estado).all()
        if not tareas:
            raise HTTPException(status_code=404, detail="No existen tareas creadas con este estado.")
    elif usuario and estado:
        tareas = db.query(Tareas).filter(Tareas.usuario == usuario, Tareas.estado == estado).all()
        if not tareas:
            raise HTTPException(status_code=404, detail="El usuario no posee tareas con ese estado.")

    return tareas

@router.put("/editar_tarea")
def Editar_tareas(tarea_id: int, usuario: str, data: dict, db : SessionLocal = Depends(get_db)):

    if usuario == "" or usuario is None:
        raise HTTPException(status_code=404, detail="El usuario es in campo requerido")
    elif tarea_id is None:
        raise HTTPException(status_code=422, detail="El id es un campo requerido")
    else:

        existe_tarea = db.query(Tareas).filter(Tareas.id == tarea_id, Tareas.usuario == usuario).first()
        if not existe_tarea:
            raise HTTPException(status_code=404, detail="No existe la tarea")

        try:
            if "fecha_vencimiento" in data:
                fecha_vencimiento_str = data["fecha_vencimiento"]
                data["fecha_vencimiento"] = datetime.strptime(fecha_vencimiento_str, "%Y-%m-%d").date()

        except ValueError as e:
            raise HTTPException(status_code=400, detail="Error en el formato de fecha vencimiento")

        for key, value in data.items():
            setattr(existe_tarea, key, value)

        db.commit()
        db.refresh(existe_tarea)

    return existe_tarea


@router.delete("/eliminar")
def Eliminar_tarea(tarea_id: int, usuario: str, db : SessionLocal = Depends(get_db)):
    existe_tarea = db.query(Tareas).filter(Tareas.id == tarea_id, Tareas.usuario == usuario).first()
    if existe_tarea is None:
        raise HTTPException(status_code=404, detail="No existe la tarea")

    db.delete(existe_tarea)
    db.commit()

    return {"message": "Tarea eliminada satisfactoriamente"}