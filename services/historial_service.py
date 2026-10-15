from database.connection import Database
from fastapi import HTTPException

class HistorialService:
    def __init__(self):
        self.db = Database()

    def obtener_ultimos_movimientos(self, id_vehiculo: int):
        conexion = self.db.get_connection()
        if not conexion:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        try:
            cursor = conexion.cursor(dictionary=True)
            # Llamamos al SP de la bitácora pasándole el ID del vehículo
            cursor.callproc('sp_obtener_historial', (id_vehiculo,))
            
            resultados = []
            for result in cursor.stored_results():
                resultados.extend(result.fetchall())
                
            # REGLA DE NEGOCIO: Devolver como máximo los 10 más recientes
            return resultados[:10]
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()
            conexion.close()