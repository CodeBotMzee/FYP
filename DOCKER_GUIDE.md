# 🐳 Docker Setup Guide

Complete Docker setup for running the entire Deepfake Detection System with one command.

## 📋 What's Included

- **Backend:** Flask API with ML model
- **Frontend:** React application
- **Database:** SQLite (persistent volume)
- **ML Model Cache:** HuggingFace model cache (persistent volume)
- **File Uploads:** Persistent storage for uploaded files

## 🚀 Quick Start

### 1. Install Docker

**Windows:**
- Download Docker Desktop: https://www.docker.com/products/docker-desktop

**Mac:**
```bash
brew install --cask docker
```

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

### 2. Configure Environment

Copy the example environment file:
```bash
cp .env.example .env
```

Edit `.env` and change the secret keys:
```env
SECRET_KEY=your-unique-secret-key-here
JWT_SECRET_KEY=your-unique-jwt-secret-here
```

### 3. Start Everything

```bash
docker-compose up -d
```

This will:
- Build backend and frontend images
- Start both containers
- Create persistent volumes
- Set up networking

### 4. Access Application

- **Frontend:** http://localhost:5173
- **Backend API:** http://localhost:5000
- **API Health:** http://localhost:5000/api/health

## 📦 Docker Commands

### Start Services
```bash
# Start in background
docker-compose up -d

# Start with logs
docker-compose up

# Start specific service
docker-compose up backend
docker-compose up frontend
```

### Stop Services
```bash
# Stop all services
docker-compose down

# Stop and remove volumes (WARNING: deletes data)
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs

# Follow logs
docker-compose logs -f

# Specific service
docker-compose logs backend
docker-compose logs frontend

# Last 100 lines
docker-compose logs --tail=100
```

### Restart Services
```bash
# Restart all
docker-compose restart

# Restart specific service
docker-compose restart backend
docker-compose restart frontend
```

### Rebuild Images
```bash
# Rebuild all
docker-compose build

# Rebuild specific service
docker-compose build backend
docker-compose build frontend

# Rebuild and start
docker-compose up -d --build
```

### Execute Commands in Container
```bash
# Backend shell
docker-compose exec backend bash

# Frontend shell
docker-compose exec frontend sh

# Run Python command in backend
docker-compose exec backend python download_model.py

# Check backend logs
docker-compose exec backend cat /app/logs/app.log
```

## 📁 Docker Files Explained

### docker-compose.yml
Main orchestration file that defines:
- Services (backend, frontend)
- Networks
- Volumes
- Environment variables
- Port mappings

### backend/Dockerfile
Backend container configuration:
- Base image: Python 3.10
- Installs system dependencies
- Installs Python packages
- Copies application code
- Exposes port 5000

### frontend/Dockerfile
Frontend container configuration:
- Base image: Node 18
- Installs npm dependencies
- Copies application code
- Exposes port 5173

### .dockerignore
Files to exclude from Docker build:
- node_modules
- __pycache__
- .git
- *.db
- uploads/

## 🗄 Persistent Volumes

### backend-uploads
Stores uploaded images and videos
```bash
# View volume
docker volume inspect deepfake-detection_backend-uploads

# Backup volume
docker run --rm -v deepfake-detection_backend-uploads:/data -v $(pwd):/backup alpine tar czf /backup/uploads-backup.tar.gz /data
```

### backend-db
Stores SQLite database
```bash
# View volume
docker volume inspect deepfake-detection_backend-db

# Backup database
docker-compose exec backend cp deepfake_detection.db /tmp/
docker cp deepfake-backend:/tmp/deepfake_detection.db ./backup.db
```

### huggingface-cache
Stores ML model cache
```bash
# View volume
docker volume inspect deepfake-detection_huggingface-cache

# Clear cache (will re-download model)
docker volume rm deepfake-detection_huggingface-cache
```

## 🌐 Networking

Services communicate through `deepfake-network`:

```
Frontend (5173) → Backend (5000) → Database
```

### Access Between Services
```javascript
// Frontend to Backend
fetch('http://backend:5000/api/health')

// Backend to Frontend (CORS)
FRONTEND_URL=http://frontend:5173
```

## ⚙️ Environment Variables

### Root .env
```env
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URI=sqlite:///deepfake_detection.db
BACKEND_PORT=5000
FRONTEND_PORT=5173
```

### backend/.env
```env
FLASK_ENV=development
FLASK_DEBUG=True
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URI=sqlite:///deepfake_detection.db
HOST=0.0.0.0
PORT=5000
FRONTEND_URL=http://localhost:5173
MODEL_NAME=dima806/deepfake_vs_real_image_detection
DEVICE=cpu
MAX_IMAGE_SIZE=10485760
MAX_VIDEO_SIZE=104857600
JWT_EXPIRY_HOURS=24
```

### frontend/.env
```env
VITE_API_URL=http://localhost:5000/api
```

## 🔧 Customization

### Change Ports

Edit `docker-compose.yml`:
```yaml
services:
  backend:
    ports:
      - "8000:5000"  # Host:Container
  frontend:
    ports:
      - "3000:5173"
```

Update `.env`:
```env
BACKEND_PORT=8000
FRONTEND_PORT=3000
```

### Use PostgreSQL Instead of SQLite

Add to `docker-compose.yml`:
```yaml
services:
  postgres:
    image: postgres:15
    environment:
      POSTGRES_DB: deepfake
      POSTGRES_USER: admin
      POSTGRES_PASSWORD: password
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - deepfake-network

  backend:
    environment:
      - DATABASE_URI=postgresql://admin:password@postgres:5432/deepfake
    depends_on:
      - postgres

volumes:
  postgres-data:
```

### Enable GPU Support

Edit `docker-compose.yml`:
```yaml
services:
  backend:
    deploy:
      resources:
        reservations:
          devices:
            - driver: nvidia
              count: 1
              capabilities: [gpu]
    environment:
      - DEVICE=cuda
```

Requires:
- NVIDIA GPU
- nvidia-docker2 installed

## 🐛 Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker-compose logs backend
docker-compose logs frontend
```

**Common issues:**
- Port already in use
- Missing environment variables
- Build errors

### Port Already in Use

**Find process:**
```bash
# Windows
netstat -ano | findstr :5000

# Linux/Mac
lsof -i :5000
```

**Kill process or change port in docker-compose.yml**

### Model Download Fails

**Manual download:**
```bash
docker-compose exec backend python download_model.py
```

**Check internet connection inside container:**
```bash
docker-compose exec backend ping google.com
```

### Database Locked

**Restart backend:**
```bash
docker-compose restart backend
```

**Reset database:**
```bash
docker-compose down
docker volume rm deepfake-detection_backend-db
docker-compose up -d
```

### Out of Memory

**Increase Docker memory:**
- Docker Desktop → Settings → Resources → Memory
- Increase to 4GB or more

**Use CPU instead of GPU:**
```env
DEVICE=cpu
```

### Frontend Can't Connect to Backend

**Check network:**
```bash
docker-compose exec frontend ping backend
```

**Check CORS settings:**
```bash
docker-compose logs backend | grep CORS
```

**Verify API URL:**
```bash
docker-compose exec frontend cat .env
```

## 📊 Monitoring

### Health Checks

Backend has built-in health check:
```bash
curl http://localhost:5000/api/health
```

Docker health status:
```bash
docker-compose ps
```

### Resource Usage

```bash
# All containers
docker stats

# Specific container
docker stats deepfake-backend
docker stats deepfake-frontend
```

### Disk Usage

```bash
# All Docker resources
docker system df

# Volumes
docker volume ls
```

## 🧹 Cleanup

### Remove Containers
```bash
docker-compose down
```

### Remove Volumes (WARNING: Deletes data)
```bash
docker-compose down -v
```

### Remove Images
```bash
docker-compose down --rmi all
```

### Complete Cleanup
```bash
# Stop and remove everything
docker-compose down -v --rmi all

# Remove unused Docker resources
docker system prune -a --volumes
```

## 🚀 Production Deployment

### Build Production Images

**Backend:**
```dockerfile
FROM python:3.10-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
ENV FLASK_ENV=production
ENV FLASK_DEBUG=False
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

**Frontend:**
```dockerfile
FROM node:18-alpine AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

### Production docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    restart: always
    environment:
      - FLASK_ENV=production
      - FLASK_DEBUG=False
    volumes:
      - backend-uploads:/app/uploads
      - backend-db:/app
    networks:
      - deepfake-network

  frontend:
    build: ./frontend
    restart: always
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - deepfake-network

  nginx:
    image: nginx:alpine
    ports:
      - "443:443"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
      - ./ssl:/etc/nginx/ssl
    depends_on:
      - backend
      - frontend
    networks:
      - deepfake-network
```

## 📝 Best Practices

1. **Always use .env files** - Never hardcode secrets
2. **Use volumes for data** - Persist important data
3. **Monitor logs** - Check for errors regularly
4. **Backup volumes** - Backup database and uploads
5. **Update images** - Keep base images updated
6. **Use health checks** - Monitor service health
7. **Limit resources** - Set memory/CPU limits
8. **Use networks** - Isolate services properly

## 🎓 FYP Docker Concepts

**Containerization:**
- Isolated environments
- Consistent across machines
- Easy deployment

**Docker Compose:**
- Multi-container orchestration
- Service dependencies
- Network management

**Volumes:**
- Persistent data storage
- Shared between containers
- Backup and restore

**Networking:**
- Service discovery
- Internal communication
- Port mapping

**Environment Variables:**
- Configuration management
- Secrets handling
- Environment-specific settings

---

**Quick Commands Reference:**

```bash
# Start
docker-compose up -d

# Stop
docker-compose down

# Logs
docker-compose logs -f

# Restart
docker-compose restart

# Rebuild
docker-compose up -d --build

# Shell access
docker-compose exec backend bash
docker-compose exec frontend sh
```

**Ready to deploy!** 🚀
