@echo off
echo ========================================================
echo  Starting Vulnerable Demo API Target on http://localhost:8001
echo ========================================================
cd /d "%~dp0backend"
call .\venv\Scripts\activate
cd /d "%~dp0demo-api"
python -m uvicorn app.main:app --host 127.0.0.1 --port 8001 --reload
pause
