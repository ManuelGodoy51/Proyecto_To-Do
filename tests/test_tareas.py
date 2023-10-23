import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

#########Crear tareas#########

def test_crear_tarea_json_completo():
    tarea_data = {
        "usuario": "usuario2",
        "titulo": "Tarea de prueba2",
        "descripcion": "Descripción de prueba2",
        "fecha_vencimiento": "2023-10-30",
        "estado": "Pendiente"
    }
    response = client.post("/tareas/guardar", json=tarea_data)
    assert response.status_code == 200
    tarea_creada = response.json()
    assert tarea_creada["usuario"] == tarea_data["usuario"]
    assert tarea_creada["titulo"] == tarea_data["titulo"]
    assert tarea_creada["descripcion"] == tarea_data["descripcion"]
    assert tarea_creada["fecha_vencimiento"] == tarea_data["fecha_vencimiento"]
    assert tarea_creada["estado"] == tarea_data["estado"]
def test_crear_tarea_sin_usuario():
    tarea_data = {
        "titulo": "Tarea de prueba3",
        "descripcion": "Descripción de prueba3",
        "fecha_vencimiento": "2023-11-30",
        "estado": "Pendiente"
    }
    response = client.post("/tareas/guardar", json=tarea_data)
    assert response.status_code == 400
def test_crear_tarea_sin_titulo():
    tarea_data = {
        "usuario": "usuario3",
        "descripcion": "Descripción de prueba3",
        "fecha_vencimiento": "2023-11-30",
        "estado": "Pendiente"
    }
    response = client.post("/tareas/guardar", json=tarea_data)
    assert response.status_code == 400
def test_crear_tarea_sin_descripcion():
    tarea_data = {
        "usuario": "usuario3",
        "titulo": "Tarea de prueba3",
        "fecha_vencimiento": "2023-11-30",
        "estado": "Pendiente"
    }
    response = client.post("/tareas/guardar", json=tarea_data)
    assert response.status_code == 400
def test_crear_tarea_sin_fecha_vencimiento():
    tarea_data = {
        "usuario": "usuario3",
        "titulo": "Tarea de prueba3",
        "descripcion": "Descripción de prueba3",
        "estado": "Pendiente"
    }
    response = client.post("/tareas/guardar", json=tarea_data)
    assert response.status_code == 400
def test_crear_tarea_sin_estado():
    tarea_data = {
        "usuario": "usuario3",
        "titulo": "Tarea de prueba3",
        "descripcion": "Descripción de prueba3",
        "fecha_vencimiento": "2023-11-30"
    }
    response = client.post("/tareas/guardar", json=tarea_data)
    assert response.status_code == 400

#########Listar tareas#########
def test_listar_tareas():
    response = client.get("/tareas/lista")
    assert response.status_code == 200
    tareas = response.json()
    assert isinstance(tareas, list)
def test_listar_tareas_usuario_estado():
    usuario = "Jonathan"
    estado = "Pendiente"
    response = client.get("/tareas/lista", params={"usuario": usuario, "estado": estado})
    assert response.status_code == 200
    tarea = response.json()
    assert isinstance(tarea, list)
def test_listar_tareas_usuario():
    estado = "Realizado"
    response = client.get("/tareas/lista", params={"estado": estado})
    assert response.status_code == 200
    tarea = response.json()
    assert isinstance(tarea, list)
def test_listar_tareas_estado():
    usuario = "Jonathan"
    response = client.get("/tareas/lista", params={"usuario": usuario})
    assert response.status_code == 200
    tarea = response.json()
    assert isinstance(tarea, list)
def test_listar_tareas_usuario_valido_estado_invalidos():
    usuario = "Jonathan"
    estado = "Perdido"
    response = client.get("/tareas/lista", params={"usuario": usuario, "estado": estado})
    assert response.status_code == 404
def test_listar_tareas_usuario_invalido():
    usuario = "Lalo"
    response = client.get("/tareas/lista", params={"usuario": usuario})
    assert response.status_code == 404
def test_listar_tareas_estado_invalido():
    estado = "Perdido"
    response = client.get("/tareas/lista", params={"estado": estado})
    assert response.status_code == 404


#########Editar tareas#########
def test_editar_tarea_completa():
    tarea_id = 6
    usuario = "usuario2"
    tarea_data = {
        "usuario": "usuario2",
        "titulo": "Tarea de prueba4",
        "descripcion": "Descripción de prueba4",
        "fecha_vencimiento": "2024-07-07",
        "estado": "Realizado"
    }
    response = client.put(f"/tareas/editar_tarea?tarea_id={tarea_id}&usuario={usuario}", json=tarea_data)

    assert response.status_code == 200
    tarea_editada = response.json()
    assert tarea_editada["usuario"] == tarea_data["usuario"]
    assert tarea_editada["titulo"] == tarea_data["titulo"]
    assert tarea_editada["descripcion"] == tarea_data["descripcion"]
    assert tarea_editada["fecha_vencimiento"] == tarea_data["fecha_vencimiento"]
    assert tarea_editada["estado"] == tarea_data["estado"]

def test_editar_tarea_estado():
    tarea_id = 3
    usuario = "Manuel"
    tarea_data = {
        "estado": "Completado"
    }
    response = client.put(f"/tareas/editar_tarea?tarea_id={tarea_id}&usuario={usuario}", json=tarea_data)

    assert response.status_code == 200
    tarea_editada = response.json()

    assert tarea_editada["estado"] == tarea_data["estado"]

def test_editar_tarea_sin_usuario():
    tarea_id = 10
    usuario = ""
    tarea_data = {
        "estado": "Completado"
    }
    response = client.put(f"/tareas/editar_tarea?tarea_id={tarea_id}&usuario={usuario}", json=tarea_data)
    assert response.status_code == 404
def test_editar_tarea_sin_id():
    tarea_id = None
    usuario = "usuario2"
    tarea_data = {
        "estado": "Completado"
    }
    response = client.put(f"/tareas/editar_tarea?tarea_id={tarea_id}&usuario={usuario}", json=tarea_data)
    assert response.status_code == 422
def test_editar_tarea_no_existe():
    tarea_id = 100
    usuario = "usuario3"
    tarea_data = {
        "estado": "Pendiente"
    }
    response = client.put(f"/tareas/editar_tarea?tarea_id={tarea_id}&usuario={usuario}", json=tarea_data)
    assert response.status_code == 404
def test_editar_tarea_formato_fecha():
    tarea_id = 6
    usuario = "usuario2"
    tarea_data = {
        "fecha_vencimiento": "23-05-2024"
    }
    response = client.put(f"/tareas/editar_tarea?tarea_id={tarea_id}&usuario={usuario}", json=tarea_data)
    assert response.status_code == 400
def test_eliminar_tarea():
    tarea_id = 17
    usuario = "usuario2"
    response = client.delete(f"/tareas/eliminar?tarea_id={tarea_id}&usuario={usuario}")
    assert response.status_code == 200
def test_eliminar_tarea_falla():
    tarea_id = 100
    usuario = "usuario6"
    response = client.delete(f"/tareas/eliminar?tarea_id={tarea_id}&usuario={usuario}")
    assert response.status_code == 404

