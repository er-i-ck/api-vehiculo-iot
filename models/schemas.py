from pydantic import BaseModel

class MovimientoIndividual(BaseModel):
    id_vehiculo: int
    id_comando: int
    origen: str = "API-FastAPI"