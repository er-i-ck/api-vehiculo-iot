from fastapi import APIRouter
from services.vehiculo_service import VehiculoService

router = APIRouter(prefix="/vehiculos", tags=["Vehículos"])
servicio = VehiculoService()

@router.get("/")
def obtener_todos_los_vehiculos():
    """Ejecuta sp_obtener_vehiculos para listar todos los vehículos registrados"""
    return servicio.obtener_vehiculos()