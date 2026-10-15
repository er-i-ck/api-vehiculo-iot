from database.connection import Database
from fastapi import HTTPException
from models.schemas import MovimientoIndividual

class MovimientoService:
    def __init__(self):
        self.db = Database()

    def registrar_movimiento(self, mov: MovimientoIndividual):
        conexion = self.db.get_connection()
        if not conexion:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        try:
            conexion.start_transaction()
            cursor = conexion.cursor()
            
            # 1. Actualiza el estado actual del vehículo (vehículo, comando, conectado=1)
            cursor.callproc('sp_actualizar_estado', (mov.id_vehiculo, mov.id_comando, 1))
            
            # 2. Guarda el movimiento en la bitácora
            cursor.callproc('sp_registrar_historial', (mov.id_vehiculo, mov.id_comando, mov.origen))
            
            conexion.commit() # Confirmar cambios en AWS
            return {"status": "success", "mensaje": "Movimiento registrado y estado actualizado"}
            
        except Exception as e:
            conexion.rollback() # Si algo falla, deshace los cambios
            raise HTTPException(status_code=400, detail=f"Error al registrar movimiento: {str(e)}")
        finally:
            cursor.close()
            conexion.close()