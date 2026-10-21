import asyncio
from database.connection import Database
from services.ws_manager import manager
from fastapi import HTTPException

class DemoService:
    # 1. Diccionario global en memoria para controlar qué vehículo está ejecutando una DEMO
    demos_activas = {}

    def __init__(self):
        self.db = Database()

    async def ejecutar_demo(self, id_vehiculo: int, id_demo: int):
        # 2. CONTROL DE SIMULTANEIDAD: Si ya está corriendo, ignoramos la nueva petición
        if DemoService.demos_activas.get(id_vehiculo):
            print(f"[DEMO] El vehículo {id_vehiculo} ya está en movimiento. Ignorando petición duplicada.")
            return

        # Marcamos que el vehículo inició su secuencia
        DemoService.demos_activas[id_vehiculo] = True

        conexion = self.db.get_connection()
        if not conexion:
            DemoService.demos_activas.pop(id_vehiculo, None)
            raise HTTPException(status_code=500, detail="Error de BD")
        
        try:
            cursor = conexion.cursor(dictionary=True)
            cursor.callproc('sp_obtener_movimientos_demo', (id_demo,))
            
            movimientos = []
            for result in cursor.stored_results():
                movimientos.extend(result.fetchall())
                
            if not movimientos:
                DemoService.demos_activas.pop(id_vehiculo, None)
                return {"mensaje": "No hay movimientos en esta DEMO"}

            # Avisar que empieza
            await manager.send_message({"evento": "INICIO_DEMO", "id_vehiculo": id_vehiculo}, id_vehiculo)

            # Recorrer cada movimiento
            for mov in movimientos:
                # 3. CONTROL DE CANCELACIÓN: Si el estado cambió a False, rompemos el ciclo
                if not DemoService.demos_activas.get(id_vehiculo, False):
                    await manager.send_message({"evento": "DEMO_CANCELADA", "id_vehiculo": id_vehiculo}, id_vehiculo)
                    print(f"[DEMO] Secuencia cancelada para el vehículo {id_vehiculo}.")
                    break

                # Actualizar el estado en RDS
                cursor.callproc('sp_actualizar_estado', (id_vehiculo, mov['id_comando'], 1))
                conexion.commit()

                # Avisar por WebSocket (Ajusta 'comando' o 'id_comando' según tu SP)
                await manager.send_message({
                    "evento": "MOVIMIENTO_DEMO",
                    "comando": mov['comando'], 
                    "duracion_ms": mov['duracion_ms'],
                    "pausa_ms": mov['pausa_ms']
                }, id_vehiculo)

                # Pausa asíncrona
                tiempo_total_segundos = (mov['duracion_ms'] + mov['pausa_ms']) / 1000.0
                await asyncio.sleep(tiempo_total_segundos)

            # 4. Avisar que terminó (Solo si completó el ciclo y no fue cancelada)
            if DemoService.demos_activas.get(id_vehiculo):
                await manager.send_message({"evento": "FIN_DEMO", "id_vehiculo": id_vehiculo}, id_vehiculo)
                
        except Exception as e:
            print(f"Error en ejecución de DEMO: {e}")
        finally:
            # 5. Siempre liberar al vehículo al terminar o cancelar
            DemoService.demos_activas.pop(id_vehiculo, None)
            if 'cursor' in locals():
                cursor.close()
            if conexion:
                conexion.close()

    # Función para accionar el freno de mano
    def cancelar_demo(self, id_vehiculo: int):
        if id_vehiculo in DemoService.demos_activas:
            DemoService.demos_activas[id_vehiculo] = False # Apagamos el interruptor
            return True
        return False