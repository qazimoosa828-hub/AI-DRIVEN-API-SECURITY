@echo off
echo ========================================================
echo  Starting FastAPI Security Assessment Backend Server
echo ========================================================
cd /d "%~dp0backend"
if not exist "venv" (
    echo Virtual environment not found. Creating venv...
    python -m venv venv
    call .\venv\Scripts\activate
    pip install -r requirements.txt
) else (
    call .\venv\Scripts\activate
)
echo Starting server on http://localhost:8000
python -m uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
pause
