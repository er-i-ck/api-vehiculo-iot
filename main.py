from fastapi import FastAPI
from routers import (
    vehiculo_router, 
    movimiento_router, 
    historial_router, 
    ws_router,
    comando_router,      # NUEVO
    demo_crud_router,    # NUEVO
    estado_router        # NUEVO
)

app = FastAPI(
    title="API Vehículo IoT",
    description="API para controlar los estados y movimientos de un vehículo IoT",
    version="1.0.0"
)

# Conectar todas las rutas
app.include_router(vehiculo_router.router)
app.include_router(movimiento_router.router)
app.include_router(historial_router.router)
app.include_router(ws_router.router)
app.include_router(comando_router.router)
app.include_router(demo_crud_router.router)
app.include_router(estado_router.router)

@app.get("/")
def read_root():
    return {"mensaje": "Servidor FastAPI funcionando con los 21 SPs integrados"}