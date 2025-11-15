@echo off
echo ========================================
echo Fixing Tailwind CSS Configuration
echo ========================================
echo.

echo Installing @tailwindcss/postcss...
call npm install --save-dev @tailwindcss/postcss

echo.
echo ✓ Tailwind CSS fixed!
echo.
echo Restart the dev server:
echo npm run dev
echo.
pause
