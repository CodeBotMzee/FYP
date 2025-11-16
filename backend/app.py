"""
Flask backend for deepfake detection system.
Main application file with routes, database initialization, and CORS configuration.
"""
from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from models import db, User, Image, Video, CameraDetection, DetectionHistory
from auth import auth_bp, init_limiter
from detection import detection_bp
from datetime import datetime
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configuration from environment variables
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///deepfake_detection.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['MAX_CONTENT_LENGTH'] = 100 * 1024 * 1024  # 100MB max request size

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Log JWT configuration for debugging (don't log the actual key for security)
import sys
jwt_secret = app.config.get('JWT_SECRET_KEY', '')
print(f"[INIT] JWT_SECRET_KEY configured: {bool(jwt_secret)}", file=sys.stderr, flush=True)
print(f"[INIT] JWT_SECRET_KEY length: {len(jwt_secret)}", file=sys.stderr, flush=True)
if jwt_secret:
    print(f"[INIT] JWT_SECRET_KEY preview: {jwt_secret[:10]}...{jwt_secret[-10:]}", file=sys.stderr, flush=True)

# Initialize rate limiter
init_limiter(app)

# Configure CORS for frontend
frontend_url = os.getenv('FRONTEND_URL', 'http://localhost:5173')
CORS(app, resources={
    r"/api/*": {
        "origins": [frontend_url],
        "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "expose_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True
    }
})

# Add request logging middleware for debugging
@app.before_request
def log_request_info():
    """Log incoming requests for debugging authentication issues."""
    import sys
    if request.path.startswith('/api/') and request.method != 'OPTIONS':
        auth_header = request.headers.get('Authorization', 'None')
        print(f"[REQUEST] {request.method} {request.path}", file=sys.stderr, flush=True)
        if auth_header != 'None':
            print(f"[REQUEST] Authorization header: {auth_header[:80]}...", file=sys.stderr, flush=True)
        else:
            print(f"[REQUEST] Authorization header: MISSING", file=sys.stderr, flush=True)

# Register blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(detection_bp, url_prefix='/api/detect')


# Create upload directories on startup
def create_upload_directories():
    """Create necessary upload directories if they don't exist."""
    directories = [
        'uploads/images',
        'uploads/videos',
        'uploads/camera'
    ]
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"[INIT] Created directory: {directory}")

# Initialize database
def init_database():
    """Initialize database tables."""
    with app.app_context():
        db.create_all()
        print("[INIT] Database tables created successfully")

# History & Stats Routes
@app.route('/api/history', methods=['GET'])
@jwt_required()
def get_history():
    """
    Get all detection history for the current user.
    Requires: JWT token in Authorization header
    Returns: {success, history: []}
    """
    try:
        # This will only execute if @jwt_required() passes
        user_id = int(get_jwt_identity())
        print(f"[HISTORY] ✓ Token validated, user_id: {user_id}")
        
        print(f"[HISTORY] Fetching history for user ID: {user_id}")
        
        # Get all detection history for the authenticated user only
        history = DetectionHistory.query.filter_by(user_id=user_id)\
            .order_by(DetectionHistory.detection_time.desc())\
            .all()
        
        history_list = [h.to_dict() for h in history]
        
        print(f"[HISTORY] Found {len(history_list)} records")
        
        return jsonify({
            'success': True,
            'history': history_list,
            'count': len(history_list)
        }), 200
        
    except Exception as e:
        print(f"[HISTORY ERROR] Failed to fetch history: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to fetch history'
        }), 500

@app.route('/api/stats', methods=['GET'])
@jwt_required()
def get_stats():
    """
    Get detection statistics for the current user.
    Requires: JWT token in Authorization header
    Returns: {success, total_detections, fake_count, real_count, accuracy}
    """
    try:
        # This will only execute if @jwt_required() passes
        user_id = int(get_jwt_identity())
        print(f"[STATS] ✓ Token validated, user_id: {user_id}")
        
        print(f"[STATS] Fetching stats for user ID: {user_id}")
        
        # Get all detections for the authenticated user only
        all_detections = DetectionHistory.query.filter_by(user_id=user_id).all()
        
        total_detections = len(all_detections)
        fake_count = sum(1 for d in all_detections if d.is_fake)
        real_count = total_detections - fake_count
        
        # Calculate average confidence as a proxy for "accuracy"
        if total_detections > 0:
            avg_confidence = sum(d.confidence_score for d in all_detections) / total_detections
            accuracy = round(avg_confidence, 2)
        else:
            accuracy = 0.0
        
        stats = {
            'total_detections': total_detections,
            'fake_count': fake_count,
            'real_count': real_count,
            'accuracy': accuracy
        }
        
        print(f"[STATS] Stats: {stats}")
        
        return jsonify({
            'success': True,
            **stats
        }), 200
        
    except Exception as e:
        print(f"[STATS ERROR] Failed to fetch stats: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to fetch statistics'
        }), 500

# Health check endpoint
@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'success': True,
        'message': 'Deepfake Detection API is running',
        'timestamp': datetime.utcnow().isoformat()
    }), 200

# Test endpoint to verify JWT token
@app.route('/api/test-auth', methods=['GET'])
@jwt_required()
def test_auth():
    """Test endpoint to verify JWT authentication is working."""
    try:
        user_id = int(get_jwt_identity())
        print(f"[TEST-AUTH] Token validated successfully, user_id: {user_id}")
        return jsonify({
            'success': True,
            'message': 'Authentication successful',
            'user_id': user_id
        }), 200
    except Exception as e:
        print(f"[TEST-AUTH ERROR] {str(e)}")
        return jsonify({
            'success': False,
            'message': f'Authentication failed: {str(e)}'
        }), 401

# Debug endpoint to check JWT configuration
@app.route('/api/debug/jwt-info', methods=['GET'])
def jwt_info():
    """Debug endpoint to check JWT configuration (remove in production)."""
    import sys
    jwt_secret = app.config.get('JWT_SECRET_KEY', '')
    print(f"[DEBUG] JWT_SECRET_KEY length: {len(jwt_secret)}", file=sys.stderr, flush=True)
    print(f"[DEBUG] JWT_SECRET_KEY preview: {jwt_secret[:10]}...{jwt_secret[-10:]}", file=sys.stderr, flush=True)
    return jsonify({
        'success': True,
        'jwt_configured': bool(jwt_secret),
        'jwt_length': len(jwt_secret),
        'jwt_preview': f"{jwt_secret[:10]}...{jwt_secret[-10:]}" if jwt_secret else None
    }), 200

# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({
        'success': False,
        'message': 'Endpoint not found'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    return jsonify({
        'success': False,
        'message': 'Internal server error'
    }), 500

@app.errorhandler(413)
def request_entity_too_large(error):
    """Handle file too large errors."""
    return jsonify({
        'success': False,
        'message': 'File too large'
    }), 413

# JWT error handlers
@jwt.expired_token_loader
def expired_token_callback(jwt_header, jwt_payload):
    """Handle expired JWT tokens."""
    print(f"[JWT ERROR] Token expired: {jwt_payload}")
    return jsonify({
        'success': False,
        'message': 'Token has expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
    """Handle invalid JWT tokens."""
    import sys
    import traceback
    print(f"[JWT ERROR] Invalid token: {str(error)}", file=sys.stderr)
    print(f"[JWT ERROR] Error type: {type(error)}", file=sys.stderr)
    traceback.print_exc(file=sys.stderr)
    return jsonify({
        'success': False,
        'message': f'Invalid token: {str(error)}'
    }), 401

@jwt.unauthorized_loader
def missing_token_callback(error):
    """Handle missing JWT tokens."""
    import sys
    auth_header = request.headers.get('Authorization', 'None')
    print(f"[JWT ERROR] Missing/Invalid token", file=sys.stderr, flush=True)
    print(f"[JWT ERROR] Authorization header received: {auth_header[:100] if len(auth_header) > 100 else auth_header}", file=sys.stderr, flush=True)
    print(f"[JWT ERROR] Error: {str(error)}", file=sys.stderr, flush=True)
    print(f"[JWT ERROR] Request path: {request.path}", file=sys.stderr, flush=True)
    print(f"[JWT ERROR] Request method: {request.method}", file=sys.stderr, flush=True)
    return jsonify({
        'success': False,
        'message': 'Authorization token is missing or invalid'
    }), 401

# Preload ML model
def preload_model():
    """Preload the ML model to avoid delays on first request."""
    try:
        print("[INIT] Preloading ML model...")
        from ml_model import get_detector
        detector = get_detector()
        detector.load_model()
        print(f"[INIT] ✓ Model loaded successfully on device: {detector.device}")
    except Exception as e:
        print(f"[INIT] ⚠ Warning: Could not preload model: {str(e)}")
        print("[INIT] Model will be loaded on first detection request")

# Application entry point
if __name__ == '__main__':
    print("=" * 60)
    print("DEEPFAKE DETECTION SYSTEM - BACKEND")
    print("=" * 60)
    
    # Create upload directories
    create_upload_directories()
    
    # Initialize database
    init_database()
    
    # Preload ML model (optional, can be skipped if it fails)
    preload_model()
    
    # Get host and port from environment
    host = os.getenv('HOST', '0.0.0.0')
    port = int(os.getenv('PORT', 5000))
    debug = os.getenv('FLASK_DEBUG', 'True').lower() == 'true'
    
    print("[INIT] Starting Flask server...")
    print(f"[INIT] API available at: http://{host}:{port}")
    print(f"[INIT] Frontend CORS enabled for: {frontend_url}")
    print("=" * 60)
    
    # Run the application
    # Disable reloader in Docker to prevent JWT secret key issues
    app.run(debug=debug, host=host, port=port, use_reloader=False)
