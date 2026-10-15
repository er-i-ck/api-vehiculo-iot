from database.connection import Database
from fastapi import HTTPException

class VehiculoService:
    def __init__(self):
        self.db = Database()

    def obtener_vehiculos(self):
        conexion = self.db.get_connection()
        if not conexion:
            raise HTTPException(status_code=500, detail="Error de conexión a la base de datos")
        
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.callproc('sp_obtener_vehiculos') # Llamamos al Stored Procedure
            
            # Obtener los resultados del SP
            resultados = []
            for result in cursor.stored_results():
                resultados.extend(result.fetchall())
                
            return resultados
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()
            conexion.close()