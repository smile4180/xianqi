@echo off
setlocal
cd /d "%~dp0.."
if not exist ".venv\Scripts\python.exe" (
  echo Virtual environment missing. Follow README setup instructions first.
  exit /b 1
)
".venv\Scripts\python.exe" app_server.py
exit /b %errorlevel%
