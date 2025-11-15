"""
Detection routes and utilities.
Handles image, video, and camera detection endpoints.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, Image, Video, CameraDetection, DetectionHistory
from datetime import datetime
import os
import uuid
import base64
from ml_model import detect_deepfake, get_detector

detection_bp = Blueprint('detection', __name__)

# File upload configuration
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi'}
MAX_IMAGE_SIZE = 10 * 1024 * 1024  # 10MB
MAX_VIDEO_SIZE = 100 * 1024 * 1024  # 100MB

def allowed_file(filename, allowed_extensions):
    """Check if file has allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def get_file_extension(filename):
    """Extract file extension from filename."""
    return filename.rsplit('.', 1)[1].lower() if '.' in filename else ''

def generate_unique_filename(original_filename):
    """Generate unique filename using UUID."""
    ext = get_file_extension(original_filename)
    return f"{uuid.uuid4().hex}.{ext}"

# The detect_deepfake function is now imported from ml_model.py
# It uses the HuggingFace model: dima806/deepfake_vs_real_image_detection

@detection_bp.route('/image', methods=['POST'])
@jwt_required()
def detect_image():
    """
    Upload and detect deepfake in image.
    Expects: multipart/form-data with 'image' field
    Returns: {success, is_fake, confidence, image_id}
    """
    try:
        user_id = get_jwt_identity()
        print(f"[DETECTION] Image upload request from user ID: {user_id}")
        
        # Check if file is present
        if 'image' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No image file provided'
            }), 400
        
        file = request.files['image']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        # Validate file type
        if not allowed_file(file.filename, ALLOWED_IMAGE_EXTENSIONS):
            return jsonify({
                'success': False,
                'message': f'Invalid file type. Allowed: {", ".join(ALLOWED_IMAGE_EXTENSIONS)}'
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_IMAGE_SIZE:
            return jsonify({
                'success': False,
                'message': f'File too large. Maximum size: {MAX_IMAGE_SIZE // (1024*1024)}MB'
            }), 400
        
        # Generate unique filename and save
        original_filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(original_filename)
        file_path = os.path.join('uploads', 'images', unique_filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        
        print(f"[DETECTION] Image saved: {file_path} ({file_size} bytes)")
        
        # Create database record
        image = Image(
            user_id=user_id,
            filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            processing_status='processing'
        )
        db.session.add(image)
        db.session.commit()
        
        # Run detection using ML model
        try:
            is_fake, confidence, model_name = detect_deepfake(file_path, file_type='image')
        except Exception as e:
            print(f"[DETECTION ERROR] ML model failed: {str(e)}")
            image.processing_status = 'failed'
            db.session.commit()
            return jsonify({
                'success': False,
                'message': f'Detection failed: {str(e)}'
            }), 500
        
        # Update database with results
        image.is_fake = is_fake
        image.confidence_score = confidence
        image.model_used = model_name
        image.processing_status = 'completed'
        image.processed_at = datetime.utcnow()
        
        # Add to detection history
        history = DetectionHistory(
            user_id=user_id,
            detection_type='image',
            content_id=image.id,
            is_fake=is_fake,
            confidence_score=confidence,
            model_version=model_name
        )
        db.session.add(history)
        db.session.commit()
        
        print(f"[DETECTION] Image detection completed: ID {image.id}")
        
        return jsonify({
            'success': True,
            'is_fake': is_fake,
            'confidence': round(confidence, 2),
            'image_id': image.id,
            'message': 'Image processed successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"[DETECTION ERROR] Image detection failed: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Image detection failed'
        }), 500

@detection_bp.route('/video', methods=['POST'])
@jwt_required()
def detect_video():
    """
    Upload and detect deepfake in video.
    Expects: multipart/form-data with 'video' field
    Returns: {success, is_fake, confidence, video_id}
    """
    try:
        user_id = get_jwt_identity()
        print(f"[DETECTION] Video upload request from user ID: {user_id}")
        
        # Check if file is present
        if 'video' not in request.files:
            return jsonify({
                'success': False,
                'message': 'No video file provided'
            }), 400
        
        file = request.files['video']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({
                'success': False,
                'message': 'No file selected'
            }), 400
        
        # Validate file type
        if not allowed_file(file.filename, ALLOWED_VIDEO_EXTENSIONS):
            return jsonify({
                'success': False,
                'message': f'Invalid file type. Allowed: {", ".join(ALLOWED_VIDEO_EXTENSIONS)}'
            }), 400
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_VIDEO_SIZE:
            return jsonify({
                'success': False,
                'message': f'File too large. Maximum size: {MAX_VIDEO_SIZE // (1024*1024)}MB'
            }), 400
        
        # Generate unique filename and save
        original_filename = secure_filename(file.filename)
        unique_filename = generate_unique_filename(original_filename)
        file_path = os.path.join('uploads', 'videos', unique_filename)
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        file.save(file_path)
        
        print(f"[DETECTION] Video saved: {file_path} ({file_size} bytes)")
        
        # Create database record
        video = Video(
            user_id=user_id,
            filename=original_filename,
            file_path=file_path,
            file_size=file_size,
            duration=None,  # TODO: Extract actual duration using ffmpeg
            processing_status='processing'
        )
        db.session.add(video)
        db.session.commit()
        
        # Run detection using ML model (extracts and analyzes frames)
        try:
            is_fake, confidence, model_name = detect_deepfake(file_path, file_type='video')
        except Exception as e:
            print(f"[DETECTION ERROR] ML model failed: {str(e)}")
            video.processing_status = 'failed'
            db.session.commit()
            return jsonify({
                'success': False,
                'message': f'Detection failed: {str(e)}'
            }), 500
        
        # Update database with results
        video.is_fake = is_fake
        video.confidence_score = confidence
        video.model_used = model_name
        video.processing_status = 'completed'
        video.processed_at = datetime.utcnow()
        # TODO: Generate and save thumbnail
        
        # Add to detection history
        history = DetectionHistory(
            user_id=user_id,
            detection_type='video',
            content_id=video.id,
            is_fake=is_fake,
            confidence_score=confidence,
            model_version=model_name
        )
        db.session.add(history)
        db.session.commit()
        
        print(f"[DETECTION] Video detection completed: ID {video.id}")
        
        return jsonify({
            'success': True,
            'is_fake': is_fake,
            'confidence': round(confidence, 2),
            'video_id': video.id,
            'message': 'Video processed successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"[DETECTION ERROR] Video detection failed: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Video detection failed'
        }), 500

@detection_bp.route('/camera', methods=['POST'])
@jwt_required()
def detect_camera():
    """
    Detect deepfake from camera frame.
    Expects: JSON with base64 encoded image
    Returns: {success, is_fake, confidence}
    """
    try:
        user_id = get_jwt_identity()
        print(f"[DETECTION] Camera detection request from user ID: {user_id}")
        
        data = request.get_json()
        
        # Validate input
        if not data or 'image' not in data:
            return jsonify({
                'success': False,
                'message': 'No image data provided'
            }), 400
        
        # Decode base64 image
        try:
            image_data = data['image']
            # Remove data URL prefix if present
            if ',' in image_data:
                image_data = image_data.split(',')[1]
            
            image_bytes = base64.b64decode(image_data)
        except Exception as e:
            print(f"[DETECTION ERROR] Failed to decode base64 image: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Invalid image data'
            }), 400
        
        # Save frame temporarily
        frame_filename = f"{uuid.uuid4().hex}.jpg"
        frame_path = os.path.join('uploads', 'camera', frame_filename)
        os.makedirs(os.path.dirname(frame_path), exist_ok=True)
        
        with open(frame_path, 'wb') as f:
            f.write(image_bytes)
        
        print(f"[DETECTION] Camera frame saved: {frame_path}")
        
        # Run detection using ML model
        try:
            is_fake, confidence, model_name = detect_deepfake(frame_path, file_type='image')
        except Exception as e:
            print(f"[DETECTION ERROR] ML model failed: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'Detection failed: {str(e)}'
            }), 500
        
        # Save to database
        camera_detection = CameraDetection(
            user_id=user_id,
            is_fake=is_fake,
            confidence_score=confidence,
            frame_path=frame_path
        )
        db.session.add(camera_detection)
        
        # Add to detection history
        history = DetectionHistory(
            user_id=user_id,
            detection_type='camera',
            content_id=camera_detection.id,
            is_fake=is_fake,
            confidence_score=confidence,
            model_version=model_name
        )
        db.session.add(history)
        db.session.commit()
        
        print(f"[DETECTION] Camera detection completed: ID {camera_detection.id}")
        
        return jsonify({
            'success': True,
            'is_fake': is_fake,
            'confidence': round(confidence, 2),
            'message': 'Frame processed successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"[DETECTION ERROR] Camera detection failed: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Camera detection failed'
        }), 500
