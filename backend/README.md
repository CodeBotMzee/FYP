# Backend Documentation - Deepfake Detection System

Flask REST API with ML-based deepfake detection.

## 📋 Overview

The backend provides:
- RESTful API endpoints
- JWT authentication
- ML model integration (HuggingFace)
- SQLite database
- File upload handling
- Video frame extraction

## 🚀 Setup

### 1. Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

**Dependencies:**
- Flask - Web framework
- SQLAlchemy - Database ORM
- JWT-Extended - Authentication
- PyTorch - ML framework (~1.5GB)
- Transformers - HuggingFace library (~500MB)
- OpenCV - Video processing
- Pillow - Image processing

**Total Size:** ~2GB | **Time:** 5-10 minutes

### 2. Download ML Model (Optional)
```bash
python download_model.py
```
Downloads model (~400MB) to avoid delay on first detection.

### 3. Start Server
```bash
python app.py
```
Server runs at: `http://localhost:5000`

## 📁 File Structure

```
backend/
├── app.py              # Main Flask app, routes, CORS
├── models.py           # SQLAlchemy database models
├── auth.py             # Authentication endpoints
├── detection.py        # Detection endpoints
├── ml_model.py         # ML model handler
├── download_model.py   # Model download script
├── requirements.txt    # Python dependencies
└── uploads/            # File storage (auto-created)
    ├── images/
    ├── videos/
    └── camera/
```

## 🗄 Database Models

### User
```python
id: Integer (Primary Key)
username: String (Unique)
email: String (Unique)
password_hash: String
created_at: DateTime
```

### Image
```python
id: Integer (Primary Key)
user_id: Integer (Foreign Key)
filename: String
file_path: String
file_size: Integer
upload_date: DateTime
is_fake: Boolean
confidence_score: Float
processing_status: String
model_used: String
processed_at: DateTime
```

### Video
```python
id: Integer (Primary Key)
user_id: Integer (Foreign Key)
filename: String
file_path: String
file_size: Integer
duration: Float
upload_date: DateTime
is_fake: Boolean
confidence_score: Float
processing_status: String
model_used: String
processed_at: DateTime
thumbnail_path: String
```

### CameraDetection
```python
id: Integer (Primary Key)
user_id: Integer (Foreign Key)
detection_date: DateTime
is_fake: Boolean
confidence_score: Float
frame_path: String
```

### DetectionHistory
```python
id: Integer (Primary Key)
user_id: Integer (Foreign Key)
detection_type: String (image/video/camera)
content_id: Integer
is_fake: Boolean
confidence_score: Float
detection_time: DateTime
model_version: String
```

## 🔌 API Endpoints

### Authentication

#### Register User
```http
POST /api/auth/register
Content-Type: application/json

{
  "username": "john_doe",
  "email": "john@example.com",
  "password": "password123"
}

Response: 201
{
  "success": true,
  "message": "User registered successfully",
  "user": {
    "id": 1,
    "username": "john_doe",
    "email": "john@example.com"
  }
}
```

#### Login
```http
POST /api/auth/login
Content-Type: application/json

{
  "username": "john_doe",
  "password": "password123"
}

Response: 200
{
  "success": true,
  "access_token": "eyJ0eXAiOiJKV1QiLCJhbGc...",
  "user": {...}
}
```

#### Get Current User
```http
GET /api/auth/me
Authorization: Bearer <token>

Response: 200
{
  "success": true,
  "user": {...}
}
```

### Detection

#### Get Available Models
```http
GET /api/detect/models

Response: 200
{
  "success": true,
  "models": [
    {
      "key": "dima806",
      "name": "Dima806 Deepfake Detector",
      "description": "General purpose detection"
    },
    ...
  ]
}
```

#### Detect Image
```http
POST /api/detect/image
Authorization: Bearer <token>
Content-Type: multipart/form-data

Form Data:
- image: <file>
- model: "dima806" (optional, default: "dima806")

Response: 200
{
  "success": true,
  "is_fake": false,
  "confidence": 87.45,
  "image_id": 1,
  "model_used": "Dima806 Deepfake Detector"
}
```

#### Detect Video
```http
POST /api/detect/video
Authorization: Bearer <token>
Content-Type: multipart/form-data

Form Data:
- video: <file>
- model: "deep-fake-v2" (optional, default: "dima806")

Response: 200
{
  "success": true,
  "is_fake": true,
  "confidence": 92.31,
  "video_id": 1,
  "model_used": "Deep Fake Detector v2"
}
```

#### Detect Camera Frame
```http
POST /api/detect/camera
Authorization: Bearer <token>
Content-Type: application/json

{
  "image": "data:image/jpeg;base64,/9j/4AAQ...",
  "model": "deep-fake-v2" (optional, default: "deep-fake-v2")
}

Response: 200
{
  "success": true,
  "is_fake": false,
  "confidence": 81.67,
  "model_used": "Deep Fake Detector v2"
}
```

### History & Stats

#### Get History
```http
GET /api/history
Authorization: Bearer <token>

Response: 200
{
  "success": true,
  "history": [...],
  "count": 25
}
```

#### Get Statistics
```http
GET /api/stats
Authorization: Bearer <token>

Response: 200
{
  "success": true,
  "total_detections": 25,
  "fake_count": 10,
  "real_count": 15,
  "accuracy": 85.5
}
```

## 🤖 ML Models

### Available Models

**1. Dima806 Deepfake Detector (Default)**
- Model: `dima806/deepfake_vs_real_image_detection`
- Type: AutoModelForImageClassification
- Size: ~400MB
- Best for: General purpose detection

**2. Deep Fake Detector v2**
- Model: `prithivMLmods/Deep-Fake-Detector-v2-Model`
- Type: ViTForImageClassification
- Size: ~350MB
- Best for: Advanced detection with Vision Transformer

**3. Open Deepfake Detection**
- Model: `prithivMLmods/open-deepfake-detection`
- Type: SiglipForImageClassification
- Size: ~450MB
- Best for: SigLIP-based detection

### How It Works

**Image Detection:**
1. Load image with PIL
2. Preprocess with AutoImageProcessor
3. Run inference through model
4. Apply softmax for probabilities
5. Return prediction + confidence

**Video Detection:**
1. Extract frames (1 per second) with OpenCV
2. Analyze each frame
3. Aggregate results (majority voting)
4. Return overall verdict

**Performance:**
- GPU: 0.5-1 second per image
- CPU: 2-4 seconds per image

### Model Caching
Each model loads once and stays in memory for fast inference.

```python
# In ml_model.py
_detector_cache = {}  # Cache per model

def get_detector(model_key='dima806'):
    if model_key not in _detector_cache:
        _detector_cache[model_key] = DeepfakeDetector(model_key)
    return _detector_cache[model_key]
```

### Features
- **Face Detection & Enhancement** - Extracts and enhances faces for better accuracy
- **Frame Stabilization** - Buffers camera frames to reduce false positives

## 🔐 Security

### Password Hashing
```python
from werkzeug.security import generate_password_hash, check_password_hash

# Hashing
password_hash = generate_password_hash(password)

# Verification
is_valid = check_password_hash(password_hash, password)
```

### JWT Tokens
- Tokens expire after 24 hours
- Stored in localStorage on frontend
- Sent in Authorization header: `Bearer <token>`

### File Validation
- Type checking (extensions)
- Size limits (10MB images, 100MB videos)
- Secure filename generation (UUID)

## ⚙️ Configuration

### Environment Variables
```python
SECRET_KEY = 'your-secret-key'  # Change in production
JWT_SECRET_KEY = 'jwt-secret'   # Change in production
DATABASE_URI = 'sqlite:///deepfake_detection.db'
```

### File Limits
```python
MAX_IMAGE_SIZE = 10 * 1024 * 1024   # 10MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB
```

### CORS
```python
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://localhost:5173"],
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})
```

## 🐛 Troubleshooting

### Model Download Fails
```bash
# Increase timeout
export HF_HUB_DOWNLOAD_TIMEOUT=300

# Manual download
python -c "from transformers import AutoModel; AutoModel.from_pretrained('dima806/deepfake_vs_real_image_detection')"
```

### Out of Memory
```python
# In ml_model.py, force CPU
self.device = "cpu"
```

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F

# Linux/Mac
lsof -ti:5000 | xargs kill -9
```

## 📝 Key Concepts for FYP

### REST API Design
- Stateless communication
- JSON request/response
- HTTP status codes (200, 201, 400, 401, 500)
- Resource-based URLs

### ORM (SQLAlchemy)
- Object-Relational Mapping
- Python classes → Database tables
- Relationships (Foreign Keys)
- Query builder

### JWT Authentication
- Stateless authentication
- Token-based (no sessions)
- Payload contains user ID
- Signed with secret key

### ML Integration
- Model loaded once (singleton)
- GPU acceleration if available
- Batch processing for videos
- Error handling for failures

### File Handling
- Multipart form data
- Secure file storage
- UUID for unique names
- Size and type validation

## 🎓 FYP Defense Points

**Architecture:**
- RESTful API design
- Separation of concerns (models, routes, ML)
- Modular structure

**Security:**
- Password hashing (werkzeug)
- JWT authentication
- Input validation
- CORS configuration

**ML Integration:**
- Pre-trained model from HuggingFace
- PyTorch framework
- GPU acceleration
- Model caching for performance

**Database:**
- SQLAlchemy ORM
- Relational design
- Foreign key relationships
- Automatic migrations

**Scalability:**
- Stateless API (can scale horizontally)
- Model caching (reduces load)
- Async processing possible (Celery)

---

**For frontend documentation, see:** `frontend/README.md`
