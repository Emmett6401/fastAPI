REM filepath: d:\DEV_23\restAPI2\run_server.bat
@echo off
set PYTHONPATH=%cd%\src
uvicorn main:app --reload --host 0.0.0.0 --port 8080
