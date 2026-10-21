from fastapi import APIRouter
from services.movimiento_service import MovimientoService
from models.schemas import MovimientoIndividual
from services.ws_manager import manager

router = APIRouter(prefix="/movimientos", tags=["Movimientos"])
servicio = MovimientoService()

@router.post("/")
async def registrar_movimiento(movimiento: MovimientoIndividual):
    """Recibe un JSON para ejecutar un movimiento y registrarlo en el historial."""
    
    # Guarda en base de datos
    respuesta = servicio.registrar_movimiento(movimiento)
    
    # Prepara el mensaje en tiempo real
    mensaje_ws = {
        "evento": "NUEVO_MOVIMIENTO",
        "id_vehiculo": movimiento.id_vehiculo,
        "id_comando": movimiento.id_comando,
        "origen": movimiento.origen
    }
    
    # Transmite el mensaje a los clientes de ese vehículo
    await manager.send_message(mensaje_ws, movimiento.id_vehiculo)
        
    return respuesta