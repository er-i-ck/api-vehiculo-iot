from fastapi import APIRouter
from database.connection import Database
from models.schemas import DemoCreate, DemoUpdate, MovimientoDemoCreate

router = APIRouter(prefix="/gestion-demos", tags=["Gestión de DEMOs"])
db = Database()

@router.post("/")
def crear_demo(demo: DemoCreate):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_crear_demo', (demo.id_vehiculo, demo.nombre, demo.descripcion))
        conexion.commit()
        return {"status": "success", "mensaje": "DEMO creada"}
    finally:
        conexion.close()

@router.get("/vehiculo/{id_vehiculo}")
def obtener_demos(id_vehiculo: int):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.callproc('sp_obtener_demos', (id_vehiculo,))
        for result in cursor.stored_results(): return result.fetchall()
    finally:
        conexion.close()

@router.delete("/{id_demo}")
def eliminar_demo(id_demo: int):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_eliminar_demo', (id_demo,))
        conexion.commit()
        return {"status": "success"}
    finally:
        conexion.close()

@router.post("/movimientos")
def agregar_movimiento(mov: MovimientoDemoCreate):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_agregar_movimiento_demo', (mov.id_demo, mov.id_comando, mov.orden, mov.duracion_ms, mov.pausa_ms))
        conexion.commit()
        return {"status": "success"}
    finally:
        conexion.close()

from pydantic import BaseModel

class MovimientoDemoUpdate(BaseModel):
    id_comando: int
    orden: int
    duracion_ms: int
    pausa_ms: int

@router.put("/{id_demo}")
def actualizar_demo(id_demo: int, demo: DemoUpdate):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_actualizar_demo', (id_demo, demo.nombre, demo.descripcion, demo.activo))
        conexion.commit()
        return {"status": "success"}
    finally:
        conexion.close()

@router.put("/movimientos/{id_demo_movimiento}")
def actualizar_movimiento(id_demo_movimiento: int, mov: MovimientoDemoUpdate):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_actualizar_movimiento_demo', (id_demo_movimiento, mov.id_comando, mov.orden, mov.duracion_ms, mov.pausa_ms))
        conexion.commit()
        return {"status": "success"}
    finally:
        conexion.close()

@router.delete("/movimientos/{id_demo_movimiento}")
def eliminar_movimiento(id_demo_movimiento: int):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_eliminar_movimiento_demo', (id_demo_movimiento,))
        conexion.commit()
        return {"status": "success"}
    finally:
        conexion.close()