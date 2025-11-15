# 🚀 Complete Setup Guide

Choose your preferred setup method.

## Method 1: Docker (Easiest) 🐳

**Best for:** Quick setup, consistent environment, easy deployment

### Prerequisites
- Docker Desktop installed
- 4GB RAM available
- 5GB disk space

### Steps

1. **Install Docker**
   - Windows/Mac: Download from https://www.docker.com/products/docker-desktop
   - Linux: `curl -fsSL https://get.docker.com -o get-docker.sh && sudo sh get-docker.sh`

2. **Setup Environment**
   ```bash
   # Copy environment file
   cp .env.example .env
   
   # Edit .env and change these:
   SECRET_KEY=your-unique-secret-key-here
   JWT_SECRET_KEY=your-unique-jwt-secret-here
   ```

3. **Start Everything**
   ```bash
   # Windows
   docker-start.bat
   
   # Mac/Linux
   docker-compose up -d
   ```

4. **Access Application**
   - Frontend: http://localhost:5173
   - Backend: http://localhost:5000
   - Health Check: http://localhost:5000/api/health

5. **View Logs**
   ```bash
   # Windows
   docker-logs.bat
   
   # Mac/Linux
   docker-compose logs -f
   ```

6. **Stop Everything**
   ```bash
   # Windows
   docker-stop.bat
   
   # Mac/Linux
   docker-compose down
   ```

**Advantages:**
- ✅ One command to start everything
- ✅ No dependency conflicts
- ✅ Consistent environment
- ✅ Easy to reset/cleanup
- ✅ Includes database and ML model

**See DOCKER_GUIDE.md for detailed Docker documentation**

---

## Method 2: Automated Scripts (Windows) 🪟

**Best for:** Windows users who prefer local installation

### Prerequisites
- Python 3.8+ installed
- Node.js 16+ installed
- 8GB RAM
- 5GB disk space

### Steps

1. **Install Backend**
   ```bash
   install_backend.bat
   ```
   This will:
   - Install Python dependencies (~2GB)
   - Download ML model (~400MB)
   - Test setup

2. **Install Frontend** (new terminal)
   ```bash
   install_frontend.bat
   ```
   This will:
   - Install Node dependencies (~300MB)
   - Test setup

3. **Start Backend** (terminal 1)
   ```bash
   run_backend.bat
   ```

4. **Start Frontend** (terminal 2)
   ```bash
   run_frontend.bat
   ```

5. **Access Application**
   - Frontend: http://localhost:5173
   - Backend: http://localhost:5000

**Advantages:**
- ✅ Automated installation
- ✅ Local development
- ✅ Easy debugging
- ✅ Direct file access

---

## Method 3: Manual Setup 🛠

**Best for:** Developers who want full control

### Backend Setup

1. **Navigate to backend**
   ```bash
   cd backend
   ```

2. **Create virtual environment** (recommended)
   ```bash
   python -m venv venv
   
   # Activate
   # Windows:
   venv\Scripts\activate
   # Mac/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```
   Time: 5-10 minutes | Size: ~2GB

4. **Setup environment**
   ```bash
   cp .env.example .env
   # Edit .env and change SECRET_KEY and JWT_SECRET_KEY
   ```

5. **Download ML model** (optional but recommended)
   ```bash
   python download_model.py
   ```
   Time: 2-3 minutes | Size: ~400MB

6. **Start server**
   ```bash
   python app.py
   ```
   Server runs at: http://localhost:5000

### Frontend Setup

1. **Navigate to frontend** (new terminal)
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```
   Time: 2-3 minutes | Size: ~300MB

3. **Setup environment**
   ```bash
   cp .env.example .env
   # Verify VITE_API_URL=http://localhost:5000/api
   ```

4. **Start development server**
   ```bash
   npm run dev
   ```
   Application runs at: http://localhost:5173

**Advantages:**
- ✅ Full control over setup
- ✅ Can use virtual environments
- ✅ Easy to customize
- ✅ Better for development

---

## Verification

After setup, verify everything works:

### 1. Check Backend
```bash
curl http://localhost:5000/api/health
```
Should return:
```json
{
  "success": true,
  "message": "Deepfake Detection API is running"
}
```

### 2. Check Frontend
Open browser: http://localhost:5173
Should see login page

### 3. Test Full Flow
1. Click "Sign Up"
2. Create account: username, email, password
3. Login with credentials
4. Should redirect to dashboard
5. Try uploading a test image

---

## Troubleshooting

### Docker Issues

**Port already in use:**
```bash
# Change ports in docker-compose.yml
ports:
  - "8000:5000"  # Backend
  - "3000:5173"  # Frontend
```

**Container won't start:**
```bash
# Check logs
docker-compose logs backend
docker-compose logs frontend

# Rebuild
docker-compose up -d --build
```

**Out of memory:**
- Docker Desktop → Settings → Resources → Memory
- Increase to 4GB or more

### Backend Issues

**Port 5000 in use:**
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Mac/Linux
lsof -ti:5000 | xargs kill -9
```

**Module not found:**
```bash
pip install -r requirements.txt
```

**Model download fails:**
- Check internet connection
- Try manual download: `python download_model.py`
- Use VPN if blocked in your region

### Frontend Issues

**Port 5173 in use:**
- Vite will auto-assign next available port

**npm install fails:**
```bash
npm cache clean --force
rm -rf node_modules package-lock.json
npm install
```

**Can't connect to backend:**
- Verify backend is running
- Check .env has correct API URL
- Check browser console for CORS errors

---

## System Requirements

### Minimum
- **CPU:** Dual-core 2.0 GHz
- **RAM:** 4GB
- **Disk:** 5GB free
- **OS:** Windows 10, macOS 10.15, Ubuntu 20.04

### Recommended
- **CPU:** Quad-core 3.0 GHz
- **RAM:** 8GB
- **Disk:** 10GB free
- **GPU:** NVIDIA GPU with CUDA (optional, 4-8x faster)
- **OS:** Windows 11, macOS 12+, Ubuntu 22.04

---

## Next Steps

After successful setup:

1. **Read Documentation**
   - `README.md` - Project overview
   - `backend/README.md` - Backend details
   - `frontend/README.md` - Frontend details
   - `DOCKER_GUIDE.md` - Docker details (if using Docker)

2. **Test Features**
   - Create account
   - Upload test image
   - Upload test video
   - Try camera detection
   - View history

3. **Prepare for Demo**
   - Collect sample images (real and fake)
   - Prepare sample videos
   - Practice workflow
   - Note any issues

---

## Quick Reference

### Docker Commands
```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Rebuild
docker-compose up -d --build
```

### Manual Commands
```bash
# Backend
cd backend
python app.py

# Frontend
cd frontend
npm run dev
```

### Access URLs
- Frontend: http://localhost:5173
- Backend: http://localhost:5000
- API Health: http://localhost:5000/api/health

---

## Support

**Setup Issues:**
1. Check error messages
2. Review troubleshooting section
3. Verify prerequisites installed
4. Check system requirements

**Still stuck?**
- Check logs (Docker or terminal)
- Verify all steps completed
- Try clean reinstall
- Check firewall/antivirus settings

---

**Choose your method and get started!** 🚀

**Recommended:** Docker for easiest setup
**Alternative:** Manual for development
