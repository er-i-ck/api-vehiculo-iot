from fastapi import WebSocket
from typing import List, Dict

class ConnectionManager:
    def __init__(self):
        # Guarda las conexiones activas separadas por id_vehiculo
        self.active_connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, websocket: WebSocket, id_vehiculo: int):
        await websocket.accept()
        if id_vehiculo not in self.active_connections:
            self.active_connections[id_vehiculo] = []
        self.active_connections[id_vehiculo].append(websocket)

    def disconnect(self, websocket: WebSocket, id_vehiculo: int):
        if id_vehiculo in self.active_connections:
            self.active_connections[id_vehiculo].remove(websocket)

    async def send_message(self, message: dict, id_vehiculo: int):
        if id_vehiculo in self.active_connections:
            for connection in self.active_connections[id_vehiculo]:
                await connection.send_json(message)

# Instancia global para usarla en toda la app
manager = ConnectionManager()