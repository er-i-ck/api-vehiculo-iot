# API Vehículo IoT - Backend Grúa RC

Este proyecto es el backend en FastAPI para el control y monitoreo de una grúa RC IoT, alojado en AWS EC2 y conectado a una base de datos MySQL en AWS RDS.

## Arquitectura y Seguridad
* **Framework:** FastAPI (Python)
* **Infraestructura:** Amazon EC2 (Windows Server) + Amazon RDS (MySQL)
* **Seguridad:** Conexión HTTPS y WSS mediante proxy inverso y DuckDNS. Las credenciales de base de datos están protegidas mediante variables de entorno (`.env`).
* **Patrón de Diseño:** Programación Orientada a Objetos (POO), con separación estricta en Routers, Services y Models. Todos los endpoints operan exclusivamente con métodos `GET` y `POST` para garantizar compatibilidad IoT.

## Endpoints HTTP y Stored Procedures

La lógica de negocio delegada a MySQL mediante 21 Stored Procedures.

### 1. Vehículos y Comandos
* `GET /vehiculos/` -> `sp_obtener_vehiculos`
* `POST /vehiculos/` (Crear) -> `sp_crear_vehiculo`
* `POST /vehiculos/actualizar/{id}` -> `sp_actualizar_vehiculo`
* `POST /vehiculos/eliminar/{id}` -> `sp_eliminar_vehiculo`
* `GET /comandos/vehiculo/{id}` -> `sp_obtener_comandos_vehiculo`
* `POST /comandos/` (Crear) -> `sp_crear_comando`

### 2. Movimientos y Estado
* `POST /movimientos/` -> Ejecuta transacción segura:
  1. `sp_actualizar_estado`
  2. `sp_registrar_historial`
* `GET /historial/{id_vehiculo}` -> `sp_obtener_historial_vehiculo` (Límite de 10 registros descendentes).

### 3. Gestión de DEMOs
* `GET /gestion-demos/vehiculo/{id}` -> `sp_obtener_demos`
* `POST /gestion-demos/` -> `sp_crear_demo`
* `POST /gestion-demos/movimientos` -> `sp_agregar_movimiento_demo`
* `POST /gestion-demos/iniciar` -> Inicia secuencia asíncrona (`BackgroundTasks`).
* `POST /gestion-demos/cancelar` -> Interrumpe el ciclo de ejecución en memoria.

## Eventos WebSocket (WSS)

La API soporta conexiones persistentes y simultáneas aisladas por `id_vehiculo`.
**URL de conexión:** `wss://tu-dominio.duckdns.org/ws/{id_vehiculo}`

### JSONs de Transmisión
1. **Movimiento Manual:**
   `{"evento": "NUEVO_MOVIMIENTO", "id_vehiculo": 1, "id_comando": 2, "origen": "API"}`
2. **Secuencia DEMO:**
   * Inicio: `{"evento": "INICIO_DEMO", "id_vehiculo": 1}`
   * Paso: `{"evento": "MOVIMIENTO_DEMO", "comando": "AVANZAR", "duracion_ms": 2000, "pausa_ms": 400}`
   * Cancelación: `{"evento": "DEMO_CANCELADA", "id_vehiculo": 1}`
   * Fin: `{"evento": "FIN_DEMO", "id_vehiculo": 1}`