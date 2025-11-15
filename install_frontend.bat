@echo off
echo ========================================
echo Frontend Installation Script
echo ========================================
echo.

echo [1/2] Installing Node.js dependencies...
cd frontend
call npm install
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo [2/2] Testing setup...
call npm list react react-router-dom axios
echo.

echo ========================================
echo ✓ Frontend Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run: npm run dev
echo 2. Frontend will start at http://localhost:5173
echo.
pause
