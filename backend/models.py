"""
Database models for the deepfake detection system.
Defines User, Image, Video, CameraDetection, and DetectionHistory tables.
"""
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    """User model for authentication and tracking detections."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    images = db.relationship('Image', backref='user', lazy=True, cascade='all, delete-orphan')
    videos = db.relationship('Video', backref='user', lazy=True, cascade='all, delete-orphan')
    camera_detections = db.relationship('CameraDetection', backref='user', lazy=True, cascade='all, delete-orphan')
    detection_history = db.relationship('DetectionHistory', backref='user', lazy=True, cascade='all, delete-orphan')
    
    def set_password(self, password):
        """Hash and set user password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verify password against hash."""
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        """Convert user to dictionary (exclude password)."""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Image(db.Model):
    """Image upload and detection results."""
    __tablename__ = 'images'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # in bytes
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_fake = db.Column(db.Boolean, nullable=True)
    confidence_score = db.Column(db.Float, nullable=True)
    processing_status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    model_used = db.Column(db.String(100), nullable=True)
    processed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        """Convert image record to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'upload_date': self.upload_date.isoformat(),
            'is_fake': self.is_fake,
            'confidence_score': self.confidence_score,
            'processing_status': self.processing_status,
            'model_used': self.model_used,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None
        }

class Video(db.Model):
    """Video upload and detection results."""
    __tablename__ = 'videos'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    file_size = db.Column(db.Integer, nullable=False)  # in bytes
    duration = db.Column(db.Float, nullable=True)  # in seconds
    upload_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_fake = db.Column(db.Boolean, nullable=True)
    confidence_score = db.Column(db.Float, nullable=True)
    processing_status = db.Column(db.String(50), default='pending')  # pending, processing, completed, failed
    model_used = db.Column(db.String(100), nullable=True)
    processed_at = db.Column(db.DateTime, nullable=True)
    thumbnail_path = db.Column(db.String(500), nullable=True)
    
    def to_dict(self):
        """Convert video record to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'filename': self.filename,
            'file_path': self.file_path,
            'file_size': self.file_size,
            'duration': self.duration,
            'upload_date': self.upload_date.isoformat(),
            'is_fake': self.is_fake,
            'confidence_score': self.confidence_score,
            'processing_status': self.processing_status,
            'model_used': self.model_used,
            'processed_at': self.processed_at.isoformat() if self.processed_at else None,
            'thumbnail_path': self.thumbnail_path
        }

class CameraDetection(db.Model):
    """Real-time camera detection results."""
    __tablename__ = 'camera_detections'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    detection_date = db.Column(db.DateTime, default=datetime.utcnow)
    is_fake = db.Column(db.Boolean, nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    frame_path = db.Column(db.String(500), nullable=True)
    
    def to_dict(self):
        """Convert camera detection to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'detection_date': self.detection_date.isoformat(),
            'is_fake': self.is_fake,
            'confidence_score': self.confidence_score,
            'frame_path': self.frame_path
        }

class DetectionHistory(db.Model):
    """Unified detection history across all detection types."""
    __tablename__ = 'detection_history'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    detection_type = db.Column(db.String(50), nullable=False)  # image, video, camera
    content_id = db.Column(db.Integer, nullable=True)  # ID of the image/video/camera_detection
    is_fake = db.Column(db.Boolean, nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    detection_time = db.Column(db.DateTime, default=datetime.utcnow, index=True)
    model_version = db.Column(db.String(50), nullable=True)
    
    def to_dict(self):
        """Convert detection history to dictionary."""
        return {
            'id': self.id,
            'user_id': self.user_id,
            'detection_type': self.detection_type,
            'content_id': self.content_id,
            'is_fake': self.is_fake,
            'confidence_score': self.confidence_score,
            'detection_time': self.detection_time.isoformat(),
            'model_version': self.model_version
        }
