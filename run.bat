@echo off
cd /d C:\api-vehiculo-iot
call .venv\Scripts\activate
uvicorn main:app --host 0.0.0.0 --port 8000
