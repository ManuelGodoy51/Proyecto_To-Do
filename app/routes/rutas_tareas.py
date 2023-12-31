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
   """
    En este módulo la manera correcta de ingresar una nueva tarea es la siguiente:

    {
        "titulo": "Título de la tarea",
        "usuario": "usuario",
        "descripcion": "Descripción de la tarea",
        "fecha_vencimiento": "2023-10-30",
        "estado": "Estado de la tarea"
    }

    La tabla en la base de datos es la siguiente, con estos tamaños en los campos:
    - usuario = String(length=20)
    - titulo = String(length=40)
    - descripcion = String(length=150)
    - fecha_vencimiento = Date
    - estado = String(length=100
    """
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
    """
        En este módulo se pueden listar todas las tareas, o bien se puede filtrar por estado y/o usuario.
    """
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
    """
         En este módulo se puede editar toda la tarea como tambien solo el estado de dicha tarea, y para ello es necesario contar con el id y el usuario de la tarea.
         Para realizar el editado de la tarea completa es de la siguiente forma:

         {
            "titulo": "Título de la tarea",
            "descripcion": "Descripción de la tarea",
            "fecha_vencimiento": "2023-10-30",
            "estado": "Estado de la tarea"
         }

         y para editar el estadom es asi:

         {
            "estado": "Estado de la tarea"
         }
    """
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
    """
         En este módulo se puede eliminar la tarea y para ello es necesario el id y el usuario de la tarea:
    """
    existe_tarea = db.query(Tareas).filter(Tareas.id == tarea_id, Tareas.usuario == usuario).first()
    if existe_tarea is None:
        raise HTTPException(status_code=404, detail="No existe la tarea")

    db.delete(existe_tarea)
    db.commit()

    return {"message": "Tarea eliminada satisfactoriamente"}