# API Vehículo IoT (Excavadora RC) - Práctica 2.5

Esta API RESTful fue desarrollada con Python y el framework FastAPI, aplicando principios de Programación Orientada a Objetos (POO). Su objetivo principal es la gestión, registro y transmisión en tiempo real de los comandos y estados enviados a un Vehículo IoT (Excavadora de construcción controlada por microcontrolador ESP8266).

El sistema se conecta de forma segura a una base de datos MySQL alojada en la nube mediante Amazon RDS (`vehiculo_iot`), integrando una arquitectura modular basada en los 21 procedimientos almacenados (Stored Procedures) para garantizar la seguridad e integridad de las transacciones.

## Requisitos Previos

Para ejecutar este proyecto en un entorno local, necesitas tener instalado:
- Python 3.10 o superior.
- Git instalado en tu computadora.
- Credenciales de acceso a la instancia activa de Amazon RDS (base de datos `vehiculo_iot`).

## Instalación y Ejecución Local (Entorno de Desarrollo)

Sigue estos pasos para levantar el servidor en tu máquina local:

1. **Clonar este repositorio:**
   ```bash
   git clone https://github.com/er-i-ck/api-vehiculo-iot.git
   cd api-vehiculo-iot
Crear y activar el entorno virtual:

Bash
python -m venv .venv
# En Windows (PowerShell o Símbolo del sistema):
.\.venv\Scripts\activate
# En macOS o Linux:
source .venv/bin/activate
Instalar las dependencias:

Bash
pip install -r requirements.txt
Configurar las variables de entorno:

Copia el archivo de ejemplo y renómbralo a .env:

Bash
cp .env.example .env
Abre el archivo .env y reemplaza los valores genéricos con las credenciales reales de tu instancia de Amazon RDS.

Importante: El archivo .env está excluido en el .gitignore por seguridad. Nunca subas tus credenciales o contraseñas de AWS a GitHub.

Ejecutar el servidor local:

Bash
uvicorn main:app --reload
Documentación de Endpoints HTTP (Swagger UI)
Una vez que el servidor local esté corriendo, puedes explorar la documentación interactiva de la API, ver los modelos de datos y probar los endpoints (GET, POST, PUT, DELETE) organizados por categorías directamente desde tu navegador:

http://localhost:8000/docs

Monitoreo en Tiempo Real (WebSockets)
Swagger UI no soporta pruebas de conexiones WebSockets de forma nativa. Para monitorear el estado y los comandos del vehículo en tiempo real, utiliza una herramienta como Thunder Client, Hoppscotch o Postman.

URL de Conexión WebSocket: ws://localhost:8000/ws/{id_vehiculo}

Ejemplo de conexión: ws://localhost:8000/ws/1

Eventos Transmitidos por el Servidor
El servidor emitirá eventos JSON a todos los clientes conectados al vehículo bajo diferentes escenarios:

1. Movimiento Individual
Se emite automáticamente a todos los clientes que monitorean un vehículo cuando se registra con éxito una petición HTTP POST en el endpoint /movimientos/ (el cual coordina de forma transaccional sp_actualizar_estado y sp_registrar_historial).

JSON
{
  "evento": "NUEVO_MOVIMIENTO",
  "id_vehiculo": 1,
  "id_comando": 1,
  "origen": "THUNDER_CLIENT"
}
2. Ejecución de Rutina DEMO
Al iniciar una secuencia automática enviando un POST al endpoint /demos/iniciar, el servidor consulta sp_obtener_movimientos_demo y transmite la siguiente secuencia en tiempo real. Se respetan estrictamente los tiempos de duracion_ms y pausa_ms configurados en la base de datos, actualizando el estado en vivo (sp_actualizar_estado) sin agregar registros al historial general (historial_comandos).

Evento de Inicio:

JSON
{
  "evento": "INICIO_DEMO",
  "id_vehiculo": 1
}
Mensaje por cada Movimiento (Transmitido secuencialmente según la rutina programada):

JSON
{
  "evento": "MOVIMIENTO_DEMO",
  "comando": "AVANZAR",
  "duracion_ms": 2000,
  "pausa_ms": 400
}
Evento de Finalización:

JSON
{
  "evento": "FIN_DEMO",
  "id_vehiculo": 1
}