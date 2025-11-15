@echo off
echo ========================================
echo Deepfake Detection System - Setup Test
echo ========================================
echo.

echo [1/4] Checking Python...
python --version
if %errorlevel% neq 0 (
    echo ERROR: Python not found! Please install Python 3.8+
    pause
    exit /b 1
)
echo ✓ Python found
echo.

echo [2/4] Checking Node.js...
node --version
if %errorlevel% neq 0 (
    echo ERROR: Node.js not found! Please install Node.js 16+
    pause
    exit /b 1
)
echo ✓ Node.js found
echo.

echo [3/4] Checking npm...
npm --version
if %errorlevel% neq 0 (
    echo ERROR: npm not found!
    pause
    exit /b 1
)
echo ✓ npm found
echo.

echo [4/4] Checking project structure...
if not exist "backend\app.py" (
    echo ERROR: backend\app.py not found!
    pause
    exit /b 1
)
if not exist "frontend\package.json" (
    echo ERROR: frontend\package.json not found!
    pause
    exit /b 1
)
echo ✓ Project structure OK
echo.

echo ========================================
echo ✓ All checks passed!
echo ========================================
echo.
echo Next steps:
echo 1. Open TWO terminal windows
echo 2. Terminal 1: cd backend ^&^& pip install -r requirements.txt ^&^& python app.py
echo 3. Terminal 2: cd frontend ^&^& npm install ^&^& npm run dev
echo 4. Open browser: http://localhost:5173
echo.
pause
