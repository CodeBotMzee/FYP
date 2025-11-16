# 🛡️ Deepfake Detection System

AI-powered web application for detecting deepfake images and videos using machine learning.

## ✨ Features

- 📸 **Image Detection** - Upload and analyze images for deepfake manipulation
- 🎥 **Video Detection** - Analyze videos frame-by-frame
- 📷 **Camera Detection** - Real-time webcam analysis
- 📊 **Dashboard** - View statistics and detection history
- 🌓 **Dark Mode** - Modern, professional UI with dark mode support

## 🛠 Tech Stack

**Backend:** Flask, PyTorch, HuggingFace Transformers, SQLAlchemy, SQLite  
**Frontend:** React 18, Vite, Tailwind CSS, React Router  
**ML Model:** dima806/deepfake_vs_real_image_detection

## 📁 Project Structure

```
deepfake-detection/
├── backend/           # Flask API + ML model
├── frontend/          # React application
├── docker-compose.yml # Docker setup
└── *.bat             # Windows helper scripts
```

## 🚀 Quick Start

### Prerequisites
- **Option 1 (Docker):** Docker and Docker Compose
- **Option 2 (Manual):** Python 3.8+, Node.js 16+, npm

### Installation

**Option 1: Docker (Recommended) 🐳**
```bash
# 1. Copy environment file
cp .env.example .env

# 2. Edit .env and change SECRET_KEY and JWT_SECRET_KEY

# 3. Start everything with one command
docker-compose up -d

# 4. Access application
# Frontend: http://localhost:5173
# Backend: http://localhost:5000
```

**Option 2: Automated (Windows)**
```bash
# Install backend
install_backend.bat

# Install frontend (new terminal)
install_frontend.bat
```

**Option 3: Manual**
```bash
# Backend
cd backend
pip install -r requirements.txt
python download_model.py  # Optional but recommended
python app.py

# Frontend (new terminal)
cd frontend
npm install
npm run dev
```

### Access Application
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## 🎯 How It Works

1. **Upload** - Select an image, video, or use your camera
2. **Analyze** - AI model processes the content using deep learning
3. **Results** - Get instant feedback with confidence scores
4. **History** - Track all your detections in the dashboard

## 🔧 Configuration

Create `.env` files from the examples:
```bash
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

Update the secret keys in `.env` files before running.

## 📝 Development

```bash
# Backend (with auto-reload)
cd backend && python app.py

# Frontend (with hot reload)
cd frontend && npm run dev
```

## 📄 License

Educational project for Final Year Project (FYP)
