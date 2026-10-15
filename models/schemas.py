from pydantic import BaseModel
from typing import Optional

# Vehículos
class VehiculoCreate(BaseModel):
    nombre: str
    modelo: str
    descripcion: str
    microcontrolador: str

class VehiculoUpdate(VehiculoCreate):
    activo: bool

# Movimientos y Comandos
class MovimientoIndividual(BaseModel):
    id_vehiculo: int
    id_comando: int
    origen: str = "API-FastAPI"

class ComandoCreate(BaseModel):
    id_vehiculo: int
    nombre: str
    codigo: int
    descripcion: str

class ComandoUpdate(BaseModel):
    nombre: str
    codigo: int
    descripcion: str
    activo: bool

# Demos
class DemoCreate(BaseModel):
    id_vehiculo: int
    nombre: str
    descripcion: str

class DemoUpdate(BaseModel):
    nombre: str
    descripcion: str
    activo: bool

class MovimientoDemoCreate(BaseModel):
    id_demo: int
    id_comando: int
    orden: int
    duracion_ms: int
    pausa_ms: int