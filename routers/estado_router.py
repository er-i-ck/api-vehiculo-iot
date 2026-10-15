from fastapi import APIRouter
from database.connection import Database

router = APIRouter(prefix="/estado", tags=["Estado del Vehículo"])
db = Database()

@router.get("/{id_vehiculo}")
def obtener_estado(id_vehiculo: int):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.callproc('sp_obtener_estado', (id_vehiculo,))
        for result in cursor.stored_results(): return result.fetchall()
    finally:
        conexion.close()