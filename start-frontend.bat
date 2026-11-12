@echo off
echo ========================================================
echo  Starting React TypeScript Security Dashboard Frontend
echo ========================================================
cd /d "%~dp0frontend"
echo Starting Vite dev server on http://localhost:5173
call npm run dev
pause
