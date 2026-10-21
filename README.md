# API Vehículo IoT - Backend Grúa RC

Este proyecto es el backend en FastAPI para el control y monitoreo de una grúa RC IoT, alojado en Amazon EC2 y conectado a una base de datos MySQL en Amazon RDS.

## 1. Estructura POO y Arquitectura
El proyecto sigue el paradigma de Programación Orientada a Objetos (POO) y una arquitectura modular para separar responsabilidades:
* `main.py`: Punto de entrada de la aplicación y configuración de FastAPI.
* `routers/`: Controladores que definen las rutas HTTP (Vehículos, Comandos, Historial, Demos).
* `services/`: Clases que contienen la lógica de negocio y el gestor de conexiones concurrentes WebSocket (`ws_manager.py`).
* `models/`: Esquemas de validación de datos usando Pydantic.
* `database/`: Gestión de la conexión a MySQL usando el patrón Singleton para optimizar recursos.

## 2. Requisitos y Dependencias
El proyecto utiliza las siguientes tecnologías clave:
* Python 3.10+
* FastAPI y Uvicorn (Framework web y servidor asíncrono)
* MySQL Connector (Comunicación con base de datos)
* python-dotenv (Manejo de variables de entorno)

Para instalar todas las dependencias necesarias, ejecuta el siguiente comando en tu terminal:
```bash
pip install -r requirements.txt
3. Guía de Ejecución y Despliegue
Para ejecutar este proyecto de forma local o en un servidor EC2:

Clonar el repositorio.

Crear un archivo llamado .env en la raíz del proyecto (este archivo está excluido en el .gitignore por seguridad).

Agregar las credenciales de Amazon RDS dentro del .env:

Fragmento de código
DB_HOST=tu_endpoint_rds.amazonaws.com
DB_USER=tu_usuario
DB_PASSWORD=tu_contraseña
DB_NAME=vehiculo_iot
DB_PORT=3306
Levantar el servidor de forma persistente con Uvicorn:

Bash
uvicorn main:app --host 0.0.0.0 --port 8000 --reload
La documentación interactiva y las pruebas de los endpoints estarán disponibles en la ruta /docs (Swagger UI).

4. Endpoints HTTP (GET/POST) y Stored Procedures
Toda la lógica de negocio se delega a MySQL mediante 21 Stored Procedures. Por estándar de compatibilidad con IoT, todos los endpoints utilizan exclusivamente métodos GET o POST.

Vehículos y Comandos
GET /vehiculos/ -> sp_obtener_vehiculos

POST /vehiculos/ (Crear) -> sp_crear_vehiculo

POST /vehiculos/actualizar/{id} -> sp_actualizar_vehiculo

POST /vehiculos/eliminar/{id} -> sp_eliminar_vehiculo

GET /comandos/vehiculo/{id} -> sp_obtener_comandos_vehiculo

POST /comandos/ (Crear) -> sp_crear_comando

Movimientos y Estado
POST /movimientos/ -> Ejecuta una transacción segura que invoca sp_actualizar_estado y sp_registrar_historial.

GET /historial/{id_vehiculo} -> sp_obtener_historial_vehiculo (Restringido a un máximo de 10 registros en orden descendente).

Gestión de DEMOs
GET /gestion-demos/vehiculo/{id} -> sp_obtener_demos

POST /gestion-demos/ -> sp_crear_demo

POST /gestion-demos/movimientos -> sp_agregar_movimiento_demo

POST /gestion-demos/iniciar -> Ejecuta DEMO asíncrona (BackgroundTasks).

POST /gestion-demos/cancelar -> Interrumpe el ciclo de la secuencia en memoria.

5. Eventos WebSocket (WSS) y Mensajes JSON
La API soporta conexiones persistentes y simultáneas. El gestor de conexiones aísla los mensajes estrictamente por id_vehiculo.URL de conexión WSS: wss://tu-dominio.duckdns.org/ws/{id_vehiculo}

Al establecer conexión, el cliente recibe inmediatamente el último estado guardado. Los eventos transmitidos posteriormente en formato JSON son:

Movimiento Manual:{"evento": "NUEVO_MOVIMIENTO", "id_vehiculo": 1, "id_comando": 2, "origen": "API"}

Ejecución de DEMO Asíncrona:

Inicio: {"evento": "INICIO_DEMO", "id_vehiculo": 1}

Paso iterativo: {"evento": "MOVIMIENTO_DEMO", "comando": "AVANZAR", "duracion_ms": 2000, "pausa_ms": 400}

Cancelación manual: {"evento": "DEMO_CANCELADA", "id_vehiculo": 1}

Conclusión exitosa: {"evento": "FIN_DEMO", "id_vehiculo": 1}


***

**Cómo actualizarlo en GitHub rápidamente:**
Abre la terminal en VS Code y lanza estos 3 comandos para que tu repositorio quede perfecto:
1. `git add README.md`
2. `git commit -m "Se añade documentacion de dependencias, POO y guia de ejecucion en README"`
3. `git push origin main`