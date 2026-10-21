from fastapi import WebSocket
from typing import List, Dict

class ConnectionManager:
    def __init__(self):
        # Guarda las conexiones activas separadas por id_vehiculo
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, id_vehiculo: int):
        await websocket.accept()
        # Forzamos a entero para evitar problemas de tipos
        vid = int(id_vehiculo)
        if vid not in self.active_connections:
            self.active_connections[vid] = []
        self.active_connections[vid].append(websocket)

    def disconnect(self, websocket: WebSocket, id_vehiculo: int):
        vid = int(id_vehiculo)
        if vid in self.active_connections:
            if websocket in self.active_connections[vid]:
                self.active_connections[vid].remove(websocket)

    async def send_message(self, message: dict, id_vehiculo: int):
        vid = int(id_vehiculo)
        print(f"\n[DEBUG WSS] Buscando enviar a vehículo ID: {vid}")
        print(f"[DEBUG WSS] Vehículos conectados ahora mismo: {list(self.active_connections.keys())}")
        
        if vid in self.active_connections:
            for connection in self.active_connections[vid]:
                await connection.send_json(message)
                print("[DEBUG WSS] ✅ Mensaje inyectado al cliente WebSocket exitosamente")
        else:
            print(f"[DEBUG WSS] ❌ ERROR: El vehículo {vid} no está en la memoria.")
        print("-" * 30)

# Instancia global para usarla en toda la app
manager = ConnectionManager()