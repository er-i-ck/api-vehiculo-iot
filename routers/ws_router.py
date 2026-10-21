from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks
from fastapi.encoders import jsonable_encoder
from services.ws_manager import manager
from services.demo_service import DemoService
from database.connection import Database
from pydantic import BaseModel

router = APIRouter(tags=["Tiempo Real y DEMOS"])
demo_service = DemoService()
db = Database()

class InicioDemo(BaseModel):
    id_vehiculo: int
    id_demo: int

@router.websocket("/ws/{id_vehiculo}")
async def websocket_endpoint(websocket: WebSocket, id_vehiculo: int):
    await manager.connect(websocket, id_vehiculo)
    
    # Consultar y enviar el estado del carrito apenas se conecta el cliente
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.callproc('sp_obtener_estado', (id_vehiculo,))
        estado_actual = []
        for result in cursor.stored_results():
            estado_actual = result.fetchall()
        
        # jsonable_encoder convierte objetos datetime de MySQL a texto válido para JSON
        await websocket.send_json({
            "evento": "ESTADO_ACTUAL",
            "id_vehiculo": id_vehiculo,
            "estado": jsonable_encoder(estado_actual)
        })
    except Exception as e:
        await websocket.send_json({
            "evento": "ERROR_ESTADO",
            "mensaje": str(e)
        })
    finally:
        conexion.close()

    try:
        while True:
            # Mantiene la conexión viva esperando mensajes del cliente
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, id_vehiculo)

#@router.post("/demos/iniciar")
#async def iniciar_demo(datos: InicioDemo, background_tasks: BackgroundTasks):
#    """Inicia una secuencia DEMO en segundo plano para no bloquear la API"""
#    background_tasks.add_task(demo_service.ejecutar_demo, datos.id_vehiculo, datos.id_demo)
#    return {"status": "success", "mensaje": "DEMO iniciada en segundo plano"}