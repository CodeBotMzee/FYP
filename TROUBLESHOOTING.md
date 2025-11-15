# 🔧 Troubleshooting Guide

Common issues and solutions for the Deepfake Detection System.

## Frontend Issues

### Tailwind CSS PostCSS Error

**Error:**
```
[postcss] It looks like you're trying to use `tailwindcss` directly as a PostCSS plugin.
The PostCSS plugin has moved to a separate package...
```

**Solution:**

**Option 1: Quick Fix (Windows)**
```bash
cd frontend
fix-tailwind.bat
```

**Option 2: Manual Fix**
```bash
cd frontend
npm install --save-dev @tailwindcss/postcss
npm run dev
```

**Option 3: Clean Reinstall**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

---

### Port 5173 Already in Use

**Error:**
```
Port 5173 is already in use
```

**Solution:**
Vite will automatically use the next available port (5174, 5175, etc.)

Or manually kill the process:
```bash
# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5173 | xargs kill -9
```

---

### Module Not Found

**Error:**
```
Cannot find module 'react' or 'axios' or other packages
```

**Solution:**
```bash
cd frontend
npm install
```

If still failing:
```bash
rm -rf node_modules package-lock.json
npm cache clean --force
npm install
```

---

### CORS Errors

**Error:**
```
Access to XMLHttpRequest blocked by CORS policy
```

**Solution:**
1. Ensure backend is running at http://localhost:5000
2. Check frontend/.env has correct API URL:
   ```
   VITE_API_URL=http://localhost:5000/api
   ```
3. Restart both frontend and backend

---

### Camera Not Working

**Error:**
```
Camera access denied or not working
```

**Solution:**
1. Grant browser camera permissions
2. Use HTTPS or localhost only (required by browsers)
3. Try different browser (Chrome recommended)
4. Check if camera is being used by another app

---

## Backend Issues

### Port 5000 Already in Use

**Error:**
```
Address already in use: Port 5000
```

**Solution:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

Or change port in backend/.env:
```env
PORT=8000
```

---

### Module Not Found (Python)

**Error:**
```
ModuleNotFoundError: No module named 'flask' or 'torch'
```

**Solution:**
```bash
cd backend
pip install -r requirements.txt
```

If using virtual environment:
```bash
cd backend
python -m venv venv
# Activate venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
```

---

### Model Download Fails

**Error:**
```
Failed to download model from HuggingFace
```

**Solution:**

**Option 1: Retry**
```bash
cd backend
python download_model.py
```

**Option 2: Increase Timeout**
```bash
export HF_HUB_DOWNLOAD_TIMEOUT=300
python download_model.py
```

**Option 3: Manual Download**
```bash
python -c "from transformers import AutoModel; AutoModel.from_pretrained('dima806/deepfake_vs_real_image_detection')"
```

**Option 4: Use VPN**
If HuggingFace is blocked in your region, use a VPN.

---

### Out of Memory

**Error:**
```
RuntimeError: CUDA out of memory
or
MemoryError
```

**Solution:**

**Option 1: Use CPU**
Edit backend/.env:
```env
DEVICE=cpu
```

**Option 2: Close Other Apps**
Free up RAM by closing unnecessary applications.

**Option 3: Reduce Batch Size**
For video processing, edit ml_model.py to process fewer frames.

---

### Database Locked

**Error:**
```
sqlite3.OperationalError: database is locked
```

**Solution:**
```bash
# Stop backend
# Delete database
cd backend
rm deepfake_detection.db
# Restart backend
python app.py
```

---

### Import Error: dotenv

**Error:**
```
ModuleNotFoundError: No module named 'dotenv'
```

**Solution:**
```bash
cd backend
pip install python-dotenv
```

---

## Docker Issues

### Docker Not Found

**Error:**
```
'docker' is not recognized as an internal or external command
```

**Solution:**
Install Docker Desktop:
- Windows/Mac: https://www.docker.com/products/docker-desktop
- Linux: `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh`

---

### Container Won't Start

**Error:**
```
Container exited with code 1
```

**Solution:**
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild
docker-compose down
docker-compose up -d --build
```

---

### Port Already in Use (Docker)

**Error:**
```
Bind for 0.0.0.0:5000 failed: port is already allocated
```

**Solution:**

**Option 1: Change Ports**
Edit docker-compose.yml:
```yaml
services:
  backend:
    ports:
      - "8000:5000"  # Change 5000 to 8000
  frontend:
    ports:
      - "3000:5173"  # Change 5173 to 3000
```

**Option 2: Kill Process**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

---

### Volume Permission Errors

**Error:**
```
Permission denied when accessing volumes
```

**Solution:**
```bash
# Linux/Mac
sudo chown -R $USER:$USER ./backend/uploads
sudo chown -R $USER:$USER ./backend

# Or run Docker with sudo (not recommended)
sudo docker-compose up -d
```

---

### Out of Disk Space

**Error:**
```
No space left on device
```

**Solution:**
```bash
# Clean up Docker
docker system prune -a --volumes

# Remove unused images
docker image prune -a

# Remove unused volumes
docker volume prune
```

---

### Network Issues

**Error:**
```
Frontend can't connect to backend
```

**Solution:**
1. Check both containers are running:
   ```bash
   docker-compose ps
   ```

2. Check network:
   ```bash
   docker-compose exec frontend ping backend
   ```

3. Verify environment variables:
   ```bash
   docker-compose exec frontend cat .env
   docker-compose exec backend cat .env
   ```

---

## General Issues

### Environment Variables Not Loading

**Error:**
```
SECRET_KEY not found or using default values
```

**Solution:**
1. Ensure .env file exists in correct location
2. Check .env file format (no spaces around =)
   ```env
   SECRET_KEY=your-secret-key
   # NOT: SECRET_KEY = your-secret-key
   ```
3. Restart application after changing .env

---

### File Upload Fails

**Error:**
```
File too large or invalid file type
```

**Solution:**
1. Check file size:
   - Images: Max 10MB
   - Videos: Max 100MB

2. Check file format:
   - Images: JPG, JPEG, PNG
   - Videos: MP4, AVI

3. Increase limits in backend/detection.py:
   ```python
   MAX_IMAGE_SIZE = 20 * 1024 * 1024  # 20MB
   MAX_VIDEO_SIZE = 200 * 1024 * 1024  # 200MB
   ```

---

### JWT Token Expired

**Error:**
```
Token has expired
```

**Solution:**
1. Logout and login again
2. Token expires after 24 hours (default)
3. Change expiry in backend/.env:
   ```env
   JWT_EXPIRY_HOURS=48
   ```

---

### Detection Takes Too Long

**Issue:**
Detection is very slow

**Solution:**

**Option 1: Use GPU**
If you have NVIDIA GPU:
```bash
pip install torch torchvision --index-url https://download.pytorch.org/whl/cu118
```

Edit backend/.env:
```env
DEVICE=cuda
```

**Option 2: Reduce Video Frame Rate**
Edit backend/ml_model.py:
```python
def detect_video(self, video_path: str, fps: int = 0.5):
    # Analyzes 1 frame every 2 seconds instead of every second
```

**Option 3: Pre-download Model**
```bash
cd backend
python download_model.py
```

---

## Quick Fixes

### Complete Reset

**Frontend:**
```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
npm run dev
```

**Backend:**
```bash
cd backend
rm -rf __pycache__ *.db uploads/
pip install -r requirements.txt
python app.py
```

**Docker:**
```bash
docker-compose down -v
docker-compose up -d --build
```

---

### Check Everything is Working

**1. Backend Health:**
```bash
curl http://localhost:5000/api/health
```
Should return:
```json
{"success": true, "message": "Deepfake Detection API is running"}
```

**2. Frontend:**
Open http://localhost:5173
Should see login page

**3. Database:**
```bash
cd backend
ls -la deepfake_detection.db
```
Should exist after first run

**4. ML Model:**
```bash
cd backend
python -c "from ml_model import get_detector; d = get_detector(); d.load_model(); print('Model OK')"
```

---

## Getting Help

If issue persists:

1. **Check Logs:**
   - Backend: Terminal output
   - Frontend: Browser console (F12)
   - Docker: `docker-compose logs -f`

2. **Verify Setup:**
   - All dependencies installed
   - Environment files configured
   - Ports not in use
   - Sufficient disk space and RAM

3. **Try Clean Install:**
   - Delete all generated files
   - Reinstall dependencies
   - Restart services

4. **Check System Requirements:**
   - Python 3.8+
   - Node.js 16+
   - 4GB RAM minimum
   - 5GB disk space

---

## Common Error Messages

| Error | Cause | Solution |
|-------|-------|----------|
| `EADDRINUSE` | Port in use | Kill process or change port |
| `ModuleNotFoundError` | Missing dependency | Run `pip install` or `npm install` |
| `CORS error` | Backend not running | Start backend server |
| `401 Unauthorized` | Invalid/expired token | Login again |
| `413 Payload Too Large` | File too big | Reduce file size |
| `500 Internal Server Error` | Backend error | Check backend logs |
| `Network Error` | Backend unreachable | Check backend is running |
| `CUDA out of memory` | GPU memory full | Use CPU or close apps |

---

**Still having issues?** Check the logs and error messages carefully. Most issues are related to:
- Missing dependencies
- Port conflicts
- Environment configuration
- File permissions

**For FYP demo, use Docker for most reliable setup!** 🐳
