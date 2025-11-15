@echo off
echo ========================================
echo Stopping Docker Containers
echo ========================================
echo.

docker-compose down

echo.
echo ✓ Containers stopped
echo.
pause
