from fastapi import APIRouter, WebSocket, WebSocketDisconnect, BackgroundTasks
from services.ws_manager import manager
from services.demo_service import DemoService
from pydantic import BaseModel

router = APIRouter(tags=["Tiempo Real y DEMOS"])
demo_service = DemoService()

class InicioDemo(BaseModel):
    id_vehiculo: int
    id_demo: int

@router.websocket("/ws/{id_vehiculo}")
async def websocket_endpoint(websocket: WebSocket, id_vehiculo: int):
    await manager.connect(websocket, id_vehiculo)
    try:
        while True:
            # Mantiene la conexión viva esperando mensajes del cliente
            data = await websocket.receive_text()
    except WebSocketDisconnect:
        manager.disconnect(websocket, id_vehiculo)

@router.post("/demos/iniciar")
async def iniciar_demo(datos: InicioDemo, background_tasks: BackgroundTasks):
    """Inicia una secuencia DEMO en segundo plano para no bloquear la API"""
    background_tasks.add_task(demo_service.ejecutar_demo, datos.id_vehiculo, datos.id_demo)
    return {"status": "success", "mensaje": "DEMO iniciada en segundo plano"}