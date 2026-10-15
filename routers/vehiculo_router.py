from fastapi import APIRouter
from services.vehiculo_service import VehiculoService

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])
servicio = VehiculoService()

@router.get("/")
def obtener_todos_los_vehiculos():
    """Ejecuta sp_obtener_vehiculos para listar todos los vehículos registrados"""
    return servicio.obtener_vehiculos()

from models.schemas import VehiculoCreate, VehiculoUpdate

@router.post("/")
def crear_vehiculo(vehiculo: VehiculoCreate):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_crear_vehiculo', (vehiculo.nombre, vehiculo.modelo, vehiculo.descripcion, vehiculo.microcontrolador))
        conexion.commit()
        return {"status": "success", "mensaje": "Vehículo creado"}
    finally:
        conexion.close()

@router.get("/{id_vehiculo}")
def obtener_vehiculo(id_vehiculo: int):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.callproc('sp_obtener_vehiculo', (id_vehiculo,))
        for result in cursor.stored_results(): return result.fetchone()
    finally:
        conexion.close()

@router.put("/{id_vehiculo}")
def actualizar_vehiculo(id_vehiculo: int, vehiculo: VehiculoUpdate):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_actualizar_vehiculo', (id_vehiculo, vehiculo.nombre, vehiculo.modelo, vehiculo.descripcion, vehiculo.microcontrolador, vehiculo.activo))
        conexion.commit()
        return {"status": "success"}
    finally:
        conexion.close()

@router.delete("/{id_vehiculo}")
def eliminar_vehiculo(id_vehiculo: int):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_eliminar_vehiculo', (id_vehiculo,))
        conexion.commit()
        return {"status": "success"}
    finally:
        conexion.close()