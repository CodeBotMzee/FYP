# Deepfake Detection System - FYP

A full-stack web application for detecting deepfake images and videos using machine learning.

## 🎯 Project Overview

This system allows users to:
- Upload images and videos for deepfake detection
- Use real-time camera detection
- View detection history and statistics
- Manage their account with JWT authentication

## 🛠 Technology Stack

### Backend
- **Flask** - Python web framework
- **SQLAlchemy** - Database ORM
- **SQLite** - Database
- **JWT** - Authentication
- **PyTorch + Transformers** - ML model (HuggingFace)
- **OpenCV** - Video processing

### Frontend
- **React 18** - UI framework
- **Vite** - Build tool
- **React Router** - Navigation
- **Axios** - HTTP client
- **Tailwind CSS** - Styling
- **react-webcam** - Camera access

### ML Model
- **Model:** dima806/deepfake_vs_real_image_detection
- **Framework:** HuggingFace Transformers
- **Type:** Binary classification (Real vs Fake)

## 📁 Project Structure

```
deepfake-detection/
├── backend/                 # Flask API
│   ├── app.py              # Main application
│   ├── models.py           # Database models
│   ├── auth.py             # Authentication routes
│   ├── detection.py        # Detection routes
│   ├── ml_model.py         # ML model handler
│   ├── download_model.py   # Model download script
│   ├── requirements.txt    # Python dependencies
│   └── README.md           # Backend documentation
│
├── frontend/               # React application
│   ├── src/
│   │   ├── components/    # React components
│   │   ├── services/      # API services
│   │   ├── utils/         # Helper functions
│   │   └── App.jsx        # Main app component
│   ├── package.json       # Node dependencies
│   └── README.md          # Frontend documentation
│
├── README.md              # This file
├── install_backend.bat    # Backend installer
├── install_frontend.bat   # Frontend installer
├── run_backend.bat        # Start backend
└── run_frontend.bat       # Start frontend
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

## 📖 Documentation

- **Setup Guide:** See `SETUP.md` - Complete setup instructions
- **Backend Documentation:** See `backend/README.md`
- **Frontend Documentation:** See `frontend/README.md`
- **Docker Guide:** See `DOCKER_GUIDE.md`

## 🎓 FYP Key Features

1. **User Authentication**
   - Registration and login with JWT tokens
   - Secure password hashing
   - Protected routes

2. **Image Detection**
   - Upload images (JPG, PNG)
   - ML-based deepfake detection
   - Confidence score display

3. **Video Detection**
   - Upload videos (MP4, AVI)
   - Frame-by-frame analysis
   - Aggregated results

4. **Camera Detection**
   - Real-time webcam capture
   - Live detection results
   - Session tracking

5. **History & Statistics**
   - Complete detection history
   - User statistics dashboard
   - Filterable results

6. **Modern UI/UX**
   - Responsive design
   - Dark mode support
   - Smooth animations

## 🔑 Key Technical Concepts

### Authentication Flow
1. User registers → Password hashed → Stored in database
2. User logs in → Credentials verified → JWT token issued
3. Token sent with each request → Verified by backend
4. Token expires after 24 hours

### Detection Flow
1. User uploads file → Saved to server
2. ML model processes file → Returns prediction
3. Result saved to database → Sent to frontend
4. Frontend displays result with confidence score

### ML Model
- Uses pre-trained HuggingFace model
- Processes images through Vision Transformer
- Returns binary classification (Real/Fake)
- GPU acceleration if available

## 📊 Database Schema

### Users
- id, username, email, password_hash, created_at

### Images
- id, user_id, filename, file_path, is_fake, confidence_score, processed_at

### Videos
- id, user_id, filename, file_path, is_fake, confidence_score, processed_at

### Camera Detections
- id, user_id, is_fake, confidence_score, detection_date

### Detection History
- id, user_id, detection_type, is_fake, confidence_score, detection_time

## 🎯 API Endpoints

### Authentication
- `POST /api/auth/register` - Register user
- `POST /api/auth/login` - Login user
- `GET /api/auth/me` - Get current user

### Detection
- `POST /api/detect/image` - Detect image
- `POST /api/detect/video` - Detect video
- `POST /api/detect/camera` - Detect camera frame

### History
- `GET /api/history` - Get detection history
- `GET /api/stats` - Get user statistics

## 🔧 Configuration

### Environment Variables

**Root .env (for Docker)**
```env
SECRET_KEY=your-super-secret-key-change-this
JWT_SECRET_KEY=your-jwt-secret-key-change-this
DATABASE_URI=sqlite:///deepfake_detection.db
BACKEND_PORT=5000
FRONTEND_PORT=5173
```

**Backend .env**
```env
FLASK_ENV=development
SECRET_KEY=your-secret-key
JWT_SECRET_KEY=your-jwt-secret
DATABASE_URI=sqlite:///deepfake_detection.db
HOST=0.0.0.0
PORT=5000
FRONTEND_URL=http://localhost:5173
```

**Frontend .env**
```env
VITE_API_URL=http://localhost:5000/api
```

## 🐛 Troubleshooting

### Backend Issues
- **Port 5000 in use:** Kill process or change port
- **Model download fails:** Check internet, run `download_model.py`
- **Out of memory:** Use CPU instead of GPU

### Frontend Issues
- **Port 5173 in use:** Vite auto-assigns next port
- **CORS errors:** Ensure backend is running
- **Camera not working:** Check browser permissions

## 📝 Notes for FYP Defense

### What to Explain
1. **Architecture:** Full-stack with REST API
2. **Authentication:** JWT-based security
3. **ML Model:** HuggingFace transformer model
4. **Database:** SQLAlchemy ORM with SQLite
5. **Frontend:** React with modern hooks
6. **Deployment:** Can be deployed to cloud platforms

### Key Points
- Real ML model integration (not mock)
- Secure authentication with password hashing
- RESTful API design
- Responsive UI with dark mode
- Complete CRUD operations
- Error handling throughout

### Demo Flow
1. Show registration and login
2. Upload sample image → Show detection
3. Upload sample video → Show processing
4. Try camera detection
5. Show history and statistics
6. Explain technical architecture

## 👨‍💻 Development

### Run in Development Mode
```bash
# Backend (with auto-reload)
cd backend
python app.py

# Frontend (with hot reload)
cd frontend
npm run dev
```

### Build for Production
```bash
# Frontend
cd frontend
npm run build
```

## 📄 License

Educational project for Final Year Project (FYP).

---

**For detailed technical documentation, see:**
- Backend: `backend/README.md`
- Frontend: `frontend/README.md`
