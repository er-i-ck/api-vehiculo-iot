from fastapi import APIRouter, BackgroundTasks
from database.connection import Database
from models.schemas import DemoCreate, DemoUpdate, MovimientoDemoCreate
from pydantic import BaseModel
from services.demo_service import DemoService

router = APIRouter(prefix="/gestion-demos", tags=["Gestión de DEMOs"])
db = Database()

# Instanciamos el servicio de ejecución
servicio_demo = DemoService()

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

# MODIFICADO: DELETE -> POST
@router.post("/eliminar/{id_demo}")
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

class MovimientoDemoUpdate(BaseModel):
    id_comando: int
    orden: int
    duracion_ms: int
    pausa_ms: int

# MODIFICADO: PUT -> POST
@router.post("/actualizar/{id_demo}")
def actualizar_demo(id_demo: int, demo: DemoUpdate):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_actualizar_demo', (id_demo, demo.nombre, demo.descripcion, demo.activo))
        conexion.commit()
        return {"status": "success"}
    finally:
        conexion.close()

# MODIFICADO: PUT -> POST
@router.post("/movimientos/actualizar/{id_demo_movimiento}")
def actualizar_movimiento(id_demo_movimiento: int, mov: MovimientoDemoUpdate):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_actualizar_movimiento_demo', (id_demo_movimiento, mov.id_comando, mov.orden, mov.duracion_ms, mov.pausa_ms))
        conexion.commit()
        return {"status": "success"}
    finally:
        conexion.close()

# MODIFICADO: DELETE -> POST
@router.post("/movimientos/eliminar/{id_demo_movimiento}")
def eliminar_movimiento(id_demo_movimiento: int):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_eliminar_movimiento_demo', (id_demo_movimiento,))
        conexion.commit()
        return {"status": "success"}
    finally:
        conexion.close()

# ==========================================
# ENDPOINT PARA EJECUTAR LA DEMO (PUNTO 8)
# ==========================================
class IniciarDemoRequest(BaseModel):
    id_vehiculo: int
    id_demo: int

@router.post("/iniciar", tags=["Ejecución de DEMOs"])
async def iniciar_demo(request: IniciarDemoRequest, background_tasks: BackgroundTasks):
    """
    Inicia una secuencia DEMO asíncrona en segundo plano para no bloquear la API.
    """
    background_tasks.add_task(
        servicio_demo.ejecutar_demo, 
        request.id_vehiculo, 
        request.id_demo
    )
    
    return {
        "status": "success", 
        "mensaje": f"Secuencia DEMO {request.id_demo} encolada y ejecutándose para el vehículo {request.id_vehiculo}."
    }

class CancelarDemoRequest(BaseModel):
    id_vehiculo: int

@router.post("/cancelar", tags=["Ejecución de DEMOs"])
def cancelar_demo(request: CancelarDemoRequest):
    """
    Detiene inmediatamente una secuencia DEMO en curso para un vehículo.
    """
    exito = servicio_demo.cancelar_demo(request.id_vehiculo)
    if exito:
        return {"status": "success", "mensaje": f"Señal de cancelación enviada al vehículo {request.id_vehiculo}."}
    return {"status": "warning", "mensaje": "No había ninguna secuencia DEMO ejecutándose para este vehículo."}