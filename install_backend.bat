@echo off
echo ========================================
echo Backend Installation Script
echo ========================================
echo.

echo [1/3] Installing Python dependencies...
cd backend
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo ✓ Dependencies installed
echo.

echo [2/3] Downloading ML model...
echo This may take 2-3 minutes...
python download_model.py
if %errorlevel% neq 0 (
    echo WARNING: Model download failed
    echo The model will download on first detection request
    echo.
)
echo.

echo [3/3] Testing setup...
python -c "import torch; print('PyTorch:', torch.__version__); print('CUDA Available:', torch.cuda.is_available())"
echo.

echo ========================================
echo ✓ Backend Installation Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Run: python app.py
echo 2. Backend will start at http://localhost:5000
echo.
pause
