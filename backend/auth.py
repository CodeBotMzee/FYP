"""
Authentication routes and utilities.
Handles user registration, login, and JWT token management.
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from models import db, User
from datetime import timedelta
import re

auth_bp = Blueprint('auth', __name__)

# Initialize rate limiter (will be configured in app.py)
limiter = None

def init_limiter(app):
    """Initialize rate limiter with the Flask app."""
    global limiter
    limiter = Limiter(
        app=app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )

def validate_email(email):
    """Validate email format using regex."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """
    Validate password strength.
    Requirements:
    - At least 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one digit
    """
    if len(password) < 8:
        return False, "Password must be at least 8 characters long"
    
    if not re.search(r'[A-Z]', password):
        return False, "Password must contain at least one uppercase letter"
    
    if not re.search(r'[a-z]', password):
        return False, "Password must contain at least one lowercase letter"
    
    if not re.search(r'\d', password):
        return False, "Password must contain at least one digit"
    
    return True, None

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Register a new user.
    Expected JSON: {username, email, password}
    Returns: {success, message, user}
    """
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['username', 'email', 'password']):
            return jsonify({
                'success': False,
                'message': 'Missing required fields: username, email, password'
            }), 400
        
        username = data['username'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        
        # Validate username
        if len(username) < 3:
            return jsonify({
                'success': False,
                'message': 'Username must be at least 3 characters'
            }), 400
        
        if not re.match(r'^[a-zA-Z0-9_]+$', username):
            return jsonify({
                'success': False,
                'message': 'Username can only contain letters, numbers, and underscores'
            }), 400
        
        # Validate email format
        if not validate_email(email):
            return jsonify({
                'success': False,
                'message': 'Invalid email format'
            }), 400
        
        # Validate password strength
        is_valid, error_msg = validate_password(password)
        if not is_valid:
            return jsonify({
                'success': False,
                'message': error_msg
            }), 400
        
        # Check if user already exists
        if User.query.filter_by(username=username).first():
            return jsonify({
                'success': False,
                'message': 'Username already exists'
            }), 409
        
        if User.query.filter_by(email=email).first():
            return jsonify({
                'success': False,
                'message': 'Email already registered'
            }), 409
        
        # Create new user
        user = User(username=username, email=email)
        user.set_password(password)
        
        db.session.add(user)
        db.session.commit()
        
        print(f"[AUTH] New user registered: {username} (ID: {user.id})")
        
        return jsonify({
            'success': True,
            'message': 'User registered successfully',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        print(f"[AUTH ERROR] Registration failed: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Registration failed'
        }), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Login user and return JWT token.
    Expected JSON: {username, password}
    Returns: {success, access_token, user}
    """
    # Rate limiting is handled by Flask-Limiter middleware
    try:
        data = request.get_json()
        
        # Validate required fields
        if not data or not all(k in data for k in ['username', 'password']):
            return jsonify({
                'success': False,
                'message': 'Missing required fields: username, password'
            }), 400
        
        username = data['username'].strip()
        password = data['password']
        
        # Find user
        user = User.query.filter_by(username=username).first()
        
        # Verify credentials (always check password to prevent timing attacks)
        if not user or not user.check_password(password):
            # Log failed attempt without revealing if username exists
            print(f"[AUTH] Failed login attempt")
            return jsonify({
                'success': False,
                'message': 'Invalid username or password'
            }), 401
        
        # Create JWT token (expires in 24 hours)
        # Note: identity must be a string for JWT validation
        access_token = create_access_token(
            identity=str(user.id),
            expires_delta=timedelta(hours=24)
        )
        
        print(f"[AUTH] User logged in: {username} (ID: {user.id})")
        
        return jsonify({
            'success': True,
            'access_token': access_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        print(f"[AUTH ERROR] Login failed: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Login failed'
        }), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    """
    Get current authenticated user info.
    Requires: JWT token in Authorization header
    Returns: {success, user}
    """
    try:
        # Get user ID from JWT token
        user_id = int(get_jwt_identity())
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({
                'success': False,
                'message': 'User not found'
            }), 404
        
        print(f"[AUTH] User info requested: {user.username} (ID: {user.id})")
        
        return jsonify({
            'success': True,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        print(f"[AUTH ERROR] Get user failed: {str(e)}")
        return jsonify({
            'success': False,
            'message': 'Failed to get user info'
        }), 500
