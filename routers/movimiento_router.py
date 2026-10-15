from fastapi import APIRouter
from services.movimiento_service import MovimientoService
from models.schemas import MovimientoIndividual

router = APIRouter(prefix="/movimientos", tags=["Movimientos"])
servicio = MovimientoService()

@router.post("/")
def registrar_movimiento(movimiento: MovimientoIndividual):
    """Recibe un JSON para ejecutar un movimiento y registrarlo en el historial."""
    return servicio.registrar_movimiento(movimiento)