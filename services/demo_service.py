import asyncio
from database.connection import Database
from services.ws_manager import manager
from fastapi import HTTPException

class DemoService:
    def __init__(self):
        self.db = Database()

    async def ejecutar_demo(self, id_vehiculo: int, id_demo: int):
        conexion = self.db.get_connection()
        if not conexion:
            raise HTTPException(status_code=500, detail="Error de BD")
        
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.callproc('sp_obtener_movimientos_demo', (id_demo,))
            
            movimientos = []
            for result in cursor.stored_results():
                movimientos.extend(result.fetchall())
                
            if not movimientos:
                return {"mensaje": "No hay movimientos en esta DEMO"}

            # 1. Avisar que empieza la DEMO
            await manager.send_message({"evento": "INICIO_DEMO", "id_vehiculo": id_vehiculo}, id_vehiculo)

            # 2. Recorrer cada movimiento
            for mov in movimientos:
                # Actualizar el estado en RDS (SIN llamar al historial)
                cursor.callproc('sp_actualizar_estado', (id_vehiculo, mov['id_comando'], 1))
                conexion.commit()

                # Avisar por WebSocket
                await manager.send_message({
                    "evento": "MOVIMIENTO_DEMO",
                    "comando": mov['comando'],
                    "duracion_ms": mov['duracion_ms'],
                    "pausa_ms": mov['pausa_ms']
                }, id_vehiculo)

                # Pausar la ejecución el tiempo que dura el movimiento + la pausa
                tiempo_total_segundos = (mov['duracion_ms'] + mov['pausa_ms']) / 1000.0
                await asyncio.sleep(tiempo_total_segundos)

            # 3. Avisar que terminó
            await manager.send_message({"evento": "FIN_DEMO", "id_vehiculo": id_vehiculo}, id_vehiculo)
            
            return {"status": "success", "mensaje": "Secuencia DEMO finalizada"}
            
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))
        finally:
            cursor.close()
            conexion.close()