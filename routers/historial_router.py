from fastapi import APIRouter
from services.historial_service import HistorialService

router = APIRouter(prefix="/historial", tags=["Historial"])
servicio = HistorialService()

@router.get("/{id_vehiculo}")
def obtener_historial(id_vehiculo: int):
    """Consulta el historial del vehículo devolviendo máximo sus 10 movimientos más recientes."""
    return servicio.obtener_ultimos_movimientos(id_vehiculo)