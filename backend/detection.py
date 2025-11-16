"""
Detection routes and utilities.
Handles image, video, and camera detection endpoints.
FIXED VERSION with proper camera enhancement and model support
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from models import db, Image, Video, CameraDetection, DetectionHistory
from datetime import datetime
import os
import uuid
import base64
from ml_model import detect_deepfake, get_detector, get_available_models

detection_bp = Blueprint('detection', __name__)

# File upload configuration
ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png'}
ALLOWED_VIDEO_EXTENSIONS = {'mp4', 'avi', 'mov'}
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


@detection_bp.route('/models', methods=['GET'])
def get_models():
    """
    Get list of available detection models.
    Returns: {success, models: []}
    """
    try:
        models = get_available_models()
        return jsonify({
            'success': True,
            'models': list(models.values())
        }), 200
    except Exception as e:
        print(f"[MODELS ERROR] Failed to fetch models: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to fetch models'
        }), 500


@detection_bp.route('/image', methods=['POST'])
@jwt_required()
def detect_image():
    """
    Upload and detect deepfake in image.
    Expects: multipart/form-data with 'image' field and optional 'model' field
    Requires: JWT token in Authorization header
    Returns: {success, is_fake, confidence, image_id, model_used}
    """
    try:
        user_id = int(get_jwt_identity())
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        # Get model selection (default to dima806)
        model_key = request.form.get('model', 'dima806')
        
        print(f"[DETECTION] Image upload request from user ID: {user_id}, model: {model_key}")
        
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
        
        # Run detection using ML model with face enhancement
        try:
            is_fake, confidence, model_name = detect_deepfake(
                file_path, 
                file_type='image', 
                model_key=model_key,
                enhance_face=True  # Enable face extraction and enhancement
            )
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
        
        print(f"[DETECTION] Image detection completed: ID {image.id}, Result: {'FAKE' if is_fake else 'REAL'} ({confidence:.2f}%)")
        
        return jsonify({
            'success': True,
            'is_fake': is_fake,
            'confidence': round(confidence, 2),
            'image_id': image.id,
            'model_used': model_name,
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
    Expects: multipart/form-data with 'video' field and optional 'model' field
    Requires: JWT token in Authorization header
    Returns: {success, is_fake, confidence, video_id, model_used, details}
    """
    try:
        user_id = int(get_jwt_identity())
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        # Get model selection (default to dima806)
        model_key = request.form.get('model', 'dima806')
        
        print(f"[DETECTION] Video upload request from user ID: {user_id}, model: {model_key}")
        
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
            duration=None,
            processing_status='processing'
        )
        db.session.add(video)
        db.session.commit()
        
        # Run detection using ML model (extracts and analyzes frames)
        try:
            # Get detector instance for video processing
            detector = get_detector(model_key)
            is_fake, confidence, model_name, details = detector.detect_video(file_path, fps=1)
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
        
        print(f"[DETECTION] Video detection completed: ID {video.id}, Result: {'FAKE' if is_fake else 'REAL'} ({confidence:.2f}%)")
        print(f"[DETECTION] Video details: {details['processed_frames']} frames, {details['fake_frames']} fake, {details['real_frames']} real")
        
        return jsonify({
            'success': True,
            'is_fake': is_fake,
            'confidence': round(confidence, 2),
            'video_id': video.id,
            'model_used': model_name,
            'details': {
                'processed_frames': details['processed_frames'],
                'fake_frames': details['fake_frames'],
                'real_frames': details['real_frames']
            },
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
    Detect deepfake from camera frame (OPTIMIZED VERSION).
    Uses direct bytes processing with face enhancement and stabilization.
    
    Expects: JSON with base64 encoded image and optional 'model' field
    Requires: JWT token in Authorization header
    Returns: {success, is_fake, confidence, model_used}
    """
    try:
        user_id = int(get_jwt_identity())
        if not user_id:
            return jsonify({
                'success': False,
                'message': 'Authentication required'
            }), 401
        
        data = request.get_json()
        
        # Get model selection (default to deep-fake-v2 for camera - works best!)
        model_key = data.get('model', 'deep-fake-v2') if data else 'deep-fake-v2'
        
        print(f"[CAMERA] Detection request from user ID: {user_id}, model: {model_key}")
        
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
            print(f"[CAMERA ERROR] Failed to decode base64 image: {str(e)}")
            return jsonify({
                'success': False,
                'message': 'Invalid image data'
            }), 400
        
        # Run detection directly from bytes (OPTIMIZED - no disk I/O!)
        try:
            detector = get_detector(model_key)
            
            # Use optimized camera detection with face enhancement and stabilization
            is_fake, confidence, model_name = detector.detect_from_bytes(
                image_bytes,
                is_camera=True  # Enables face detection, enhancement, and frame buffering
            )
            
        except Exception as e:
            print(f"[CAMERA ERROR] ML model failed: {str(e)}")
            return jsonify({
                'success': False,
                'message': f'Detection failed: {str(e)}'
            }), 500
        
        # Optionally save frame for history (can be disabled to save space)
        frame_filename = f"{uuid.uuid4().hex}.jpg"
        frame_path = os.path.join('uploads', 'camera', frame_filename)
        
        try:
            os.makedirs(os.path.dirname(frame_path), exist_ok=True)
            with open(frame_path, 'wb') as f:
                f.write(image_bytes)
        except Exception as e:
            print(f"[CAMERA WARNING] Failed to save frame: {str(e)}")
            frame_path = None
        
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
        
        print(f"[CAMERA] Detection completed: ID {camera_detection.id}, Result: {'FAKE' if is_fake else 'REAL'} ({confidence:.2f}%)")
        
        return jsonify({
            'success': True,
            'is_fake': is_fake,
            'confidence': round(confidence, 2),
            'model_used': model_name,
            'message': 'Frame processed successfully'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        print(f"[CAMERA ERROR] Camera detection failed: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Camera detection failed'
        }), 500


@detection_bp.route('/camera/batch', methods=['POST'])
@jwt_required()
def detect_camera_batch():
    """
    Detect multiple camera frames in batch for better performance.
    Useful for processing video clips from camera.
    
    Expects: JSON with array of base64 encoded images
    Returns: {success, results: [{is_fake, confidence}], overall_result}
    """
    try:
        user_id = int(get_jwt_identity())
        data = request.get_json()
        
        model_key = data.get('model', 'deep-fake-v2')
        frames = data.get('frames', [])
        
        if not frames:
            return jsonify({
                'success': False,
                'message': 'No frames provided'
            }), 400
        
        print(f"[CAMERA BATCH] Processing {len(frames)} frames for user {user_id}")
        
        detector = get_detector(model_key)
        results = []
        
        for i, frame_data in enumerate(frames):
            try:
                # Decode frame
                if ',' in frame_data:
                    frame_data = frame_data.split(',')[1]
                image_bytes = base64.b64decode(frame_data)
                
                # Detect
                is_fake, confidence, model_name = detector.detect_from_bytes(
                    image_bytes,
                    is_camera=True
                )
                
                results.append({
                    'frame_index': i,
                    'is_fake': is_fake,
                    'confidence': round(confidence, 2)
                })
                
            except Exception as e:
                print(f"[CAMERA BATCH] Frame {i} failed: {str(e)}")
                results.append({
                    'frame_index': i,
                    'error': str(e)
                })
        
        # Calculate overall result
        valid_results = [r for r in results if 'error' not in r]
        if valid_results:
            fake_count = sum(1 for r in valid_results if r['is_fake'])
            overall_is_fake = fake_count > len(valid_results) / 2
            avg_confidence = sum(r['confidence'] for r in valid_results) / len(valid_results)
        else:
            overall_is_fake = None
            avg_confidence = 0
        
        print(f"[CAMERA BATCH] Completed: {len(valid_results)}/{len(frames)} frames, Overall: {'FAKE' if overall_is_fake else 'REAL'}")
        
        return jsonify({
            'success': True,
            'results': results,
            'overall_result': {
                'is_fake': overall_is_fake,
                'confidence': round(avg_confidence, 2),
                'fake_count': fake_count if valid_results else 0,
                'total_frames': len(valid_results)
            }
        }), 200
        
    except Exception as e:
        print(f"[CAMERA BATCH ERROR] {str(e)}")
        return jsonify({
            'success': False,
            'message': str(e)
        }), 500