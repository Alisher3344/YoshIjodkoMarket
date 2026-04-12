@echo off
echo ========================================
echo   Maktab Market — Ishga tushirish
echo ========================================

echo.
echo [1/2] Backend server ishga tushmoqda...
start "Backend" cmd /k "cd server && npm start"

echo.
echo [2/2] Frontend ishga tushmoqda...
timeout /t 2 /noisy >nul
start "Frontend" cmd /k "npm run dev"

echo.
echo ========================================
echo   Sayt: http://localhost:5173
echo   API:  http://localhost:5000/api
echo ========================================
pause
