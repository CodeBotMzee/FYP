@echo off
echo ========================================
echo Deepfake Detection - Docker Setup
echo ========================================
echo.

echo [1/3] Checking Docker...
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ERROR: Docker not found!
    echo Please install Docker Desktop from: https://www.docker.com/products/docker-desktop
    pause
    exit /b 1
)
echo ✓ Docker found
echo.

echo [2/3] Checking environment file...
if not exist ".env" (
    echo Creating .env from .env.example...
    copy .env.example .env
    echo.
    echo ⚠ IMPORTANT: Edit .env and change SECRET_KEY and JWT_SECRET_KEY
    echo Press any key to continue after editing .env...
    pause
)
echo ✓ Environment file exists
echo.

echo [3/3] Starting Docker containers...
docker-compose up -d
if %errorlevel% neq 0 (
    echo ERROR: Failed to start containers
    echo Check the error messages above
    pause
    exit /b 1
)
echo.

echo ========================================
echo ✓ Docker containers started!
echo ========================================
echo.
echo Services:
echo - Frontend: http://localhost:5173
echo - Backend:  http://localhost:5000
echo - Health:   http://localhost:5000/api/health
echo.
echo View logs: docker-compose logs -f
echo Stop:      docker-compose down
echo.
pause
