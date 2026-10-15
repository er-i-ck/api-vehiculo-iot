from fastapi import APIRouter, HTTPException
from database.connection import Database
from models.schemas import ComandoCreate, ComandoUpdate

router = APIRouter(prefix="/comandos", tags=["Comandos"])
db = Database()

@router.post("/")
def crear_comando(comando: ComandoCreate):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_crear_comando', (comando.id_vehiculo, comando.nombre, comando.codigo, comando.descripcion))
        conexion.commit()
        return {"status": "success", "mensaje": "Comando creado"}
    finally:
        conexion.close()

@router.get("/vehiculo/{id_vehiculo}")
def obtener_comandos(id_vehiculo: int):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor(dictionary=True)
        cursor.callproc('sp_obtener_comandos_vehiculo', (id_vehiculo,))
        resultados = []
        for result in cursor.stored_results():
            resultados.extend(result.fetchall())
        return resultados
    finally:
        conexion.close()

@router.put("/{id_comando}")
def actualizar_comando(id_comando: int, comando: ComandoUpdate):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_actualizar_comando', (id_comando, comando.nombre, comando.codigo, comando.descripcion, comando.activo))
        conexion.commit()
        return {"status": "success", "mensaje": "Comando actualizado"}
    finally:
        conexion.close()

@router.delete("/{id_comando}")
def eliminar_comando(id_comando: int):
    conexion = db.get_connection()
    try:
        cursor = conexion.cursor()
        cursor.callproc('sp_eliminar_comando', (id_comando,))
        conexion.commit()
        return {"status": "success", "mensaje": "Comando eliminado"}
    finally:
        conexion.close()