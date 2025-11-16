# 🛡️ Deepfake Detection System

AI-powered web application for detecting deepfake images and videos using machine learning.

## ✨ Features

- 📸 **Image Detection** - Upload and analyze images for deepfake manipulation
- 🎥 **Video Detection** - Analyze videos frame-by-frame
- 📷 **Camera Detection** - Real-time webcam analysis
- 🧠 **Multiple AI Models** - Choose from 3 different detection models
- 📊 **Dashboard** - View statistics and detection history
- 🌓 **Dark Mode** - Modern, professional UI with dark mode support

## 🛠 Tech Stack

**Backend:** Flask, PyTorch, HuggingFace Transformers, SQLAlchemy, SQLite  
**Frontend:** React 18, Vite, Tailwind CSS, React Router  
**ML Models:** 
- dima806/deepfake_vs_real_image_detection (Default)
- prithivMLmods/Deep-Fake-Detector-v2-Model
- prithivMLmods/open-deepfake-detection

## 📁 Project Structure

```
deepfake-detection/
├── backend/           # Flask API + ML models
├── frontend/          # React application
└── docker-compose.yml # Docker setup
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

**Option 2: Manual**
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

1. **Choose Model** - Select from 3 AI detection models
2. **Upload** - Select an image, video, or use your camera
3. **Analyze** - AI model processes the content using deep learning
4. **Results** - Get instant feedback with confidence scores
5. **History** - Track all your detections in the dashboard

## 🧠 Model Switching

Choose from 3 AI models via dropdown in the UI:
- **Dima806** - General purpose (default)
- **Deep Fake v2** - Advanced ViT-based detector
- **Open Deepfake** - SigLIP-based detector

Pre-download models (optional):
```bash
cd backend
python download_all_models.py
```

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
