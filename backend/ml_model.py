"""
Machine Learning Model Handler for Deepfake Detection
Fixed version with proper model-specific architectures and preprocessing
"""
import torch
from transformers import (
    AutoImageProcessor, 
    AutoModelForImageClassification,
    ViTForImageClassification,
    ViTImageProcessor,
    SiglipForImageClassification
)
from PIL import Image
import cv2
import numpy as np
import os
import io
from typing import Tuple, List, Dict
import logging
from collections import deque

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Available models configuration with correct architectures
AVAILABLE_MODELS = {
    'dima806': {
        'name': 'dima806/deepfake_vs_real_image_detection',
        'display_name': 'Dima806 Deepfake Detector',
        'model_class': 'AutoModelForImageClassification',
        'processor_class': 'AutoImageProcessor',
        'description': 'General purpose deepfake detection',
        'labels': {0: 'Fake', 1: 'Real'}  # 0=Fake, 1=Real
    },
    'deep-fake-v2': {
        'name': 'prithivMLmods/Deep-Fake-Detector-v2-Model',
        'display_name': 'Deep Fake Detector v2 (ViT)',
        'model_class': 'ViTForImageClassification',
        'processor_class': 'ViTImageProcessor',
        'description': 'Vision Transformer based detector',
        'labels': None  # Will use model's id2label
    },
    'open-deepfake': {
        'name': 'prithivMLmods/open-deepfake-detection',
        'display_name': 'Open Deepfake Detection (SigLIP)',
        'model_class': 'SiglipForImageClassification',
        'processor_class': 'AutoImageProcessor',
        'description': 'SigLIP based deepfake detector',
        'labels': {0: 'Fake', 1: 'Real'}  # 0=Fake, 1=Real
    }
}


class DeepfakeDetector:
    """
    Deepfake detection model handler with proper architecture support
    """
    
    def __init__(self, model_key="dima806"):
        """Initialize detector with specific model"""
        if model_key not in AVAILABLE_MODELS:
            logger.warning(f"Unknown model key: {model_key}, defaulting to 'dima806'")
            model_key = 'dima806'
        
        self.model_key = model_key
        self.model_config = AVAILABLE_MODELS[model_key]
        self.model_name = self.model_config['name']
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = None
        self.model = None
        self.is_loaded = False
        self.face_cascade = None
        self.frame_buffer = deque(maxlen=5)  # For camera stabilization
        
        logger.info(f"Initializing: {self.model_config['display_name']} on {self.device}")
        
    def load_model(self):
        """Load model and processor with correct architecture"""
        if self.is_loaded:
            return
        
        try:
            logger.info(f"Loading model: {self.model_name}")
            
            # Load processor based on model type
            processor_class = self.model_config['processor_class']
            if processor_class == 'ViTImageProcessor':
                self.processor = ViTImageProcessor.from_pretrained(self.model_name)
            else:
                self.processor = AutoImageProcessor.from_pretrained(self.model_name)
            
            # Load model based on architecture
            model_class = self.model_config['model_class']
            if model_class == 'ViTForImageClassification':
                self.model = ViTForImageClassification.from_pretrained(self.model_name)
            elif model_class == 'SiglipForImageClassification':
                self.model = SiglipForImageClassification.from_pretrained(self.model_name)
            else:
                self.model = AutoModelForImageClassification.from_pretrained(self.model_name)
            
            # Move to device and set eval mode
            self.model.to(self.device)
            self.model.eval()
            
            # Initialize face detector for camera enhancement
            try:
                self.face_cascade = cv2.CascadeClassifier(
                    cv2.data.haarcascades + 'haarcascade_frontalface_default.xml'
                )
            except:
                logger.warning("Face cascade not available")
            
            self.is_loaded = True
            logger.info(f"✓ Model loaded: {self.model_config['display_name']}")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise Exception(f"Model loading failed: {str(e)}")
    
    def _get_label(self, class_idx: int) -> str:
        """Get label for predicted class index"""
        if self.model_config['labels'] is not None:
            return self.model_config['labels'].get(class_idx, f"Class_{class_idx}")
        elif hasattr(self.model.config, 'id2label'):
            return self.model.config.id2label.get(class_idx, f"Class_{class_idx}")
        else:
            return f"Class_{class_idx}"
    
    def _extract_and_enhance_face(self, image: Image.Image) -> Image.Image:
        """Extract face and enhance quality for better detection"""
        try:
            # Convert PIL to numpy
            img_array = np.array(image)
            
            # Try to detect face
            if self.face_cascade is not None:
                gray = cv2.cvtColor(img_array, cv2.COLOR_RGB2GRAY)
                faces = self.face_cascade.detectMultiScale(gray, 1.3, 5)
                
                if len(faces) > 0:
                    # Get largest face
                    (x, y, w, h) = max(faces, key=lambda f: f[2] * f[3])
                    
                    # Add padding
                    padding = int(w * 0.3)
                    x1 = max(0, x - padding)
                    y1 = max(0, y - padding)
                    x2 = min(img_array.shape[1], x + w + padding)
                    y2 = min(img_array.shape[0], y + h + padding)
                    
                    # Crop face
                    face = img_array[y1:y2, x1:x2]
                    
                    # Enhance contrast
                    lab = cv2.cvtColor(face, cv2.COLOR_RGB2LAB)
                    l, a, b = cv2.split(lab)
                    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
                    l = clahe.apply(l)
                    enhanced = cv2.merge([l, a, b])
                    enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2RGB)
                    
                    return Image.fromarray(enhanced)
            
            return image
            
        except Exception as e:
            logger.debug(f"Face extraction failed: {e}, using original image")
            return image
    
    def detect_image(self, image_path: str, enhance_face: bool = False) -> Tuple[bool, float, str]:
        """
        Detect if an image is a deepfake
        
        Args:
            image_path: Path to image file
            enhance_face: Whether to extract and enhance face
            
        Returns:
            Tuple of (is_fake: bool, confidence: float, model_name: str)
        """
        try:
            if not self.is_loaded:
                self.load_model()
            
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            # Load image
            image = Image.open(image_path).convert('RGB')
            
            # Optionally enhance face
            if enhance_face:
                image = self._extract_and_enhance_face(image)
            
            # Preprocess
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Run inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
            
            # Get predictions
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            predicted_class = probabilities.argmax().item()
            confidence = probabilities[0][predicted_class].item() * 100
            
            # Get label and determine if fake
            label = self._get_label(predicted_class)
            
            # Determine if fake based on label
            is_fake = label.lower() in ['fake', 'deepfake', 'synthetic']
            
            logger.info(f"Detection: {label} ({confidence:.2f}%) - Model: {self.model_key}")
            
            return is_fake, confidence, self.model_config['display_name']
            
        except Exception as e:
            logger.error(f"Detection failed: {str(e)}")
            raise Exception(f"Image detection failed: {str(e)}")
    
    def detect_from_bytes(self, image_bytes: bytes, is_camera: bool = False) -> Tuple[bool, float, str]:
        """
        Detect deepfake from image bytes (for camera/upload)
        
        Args:
            image_bytes: Raw image bytes
            is_camera: True if from camera feed (enables enhancement)
            
        Returns:
            Tuple of (is_fake: bool, confidence: float, model_name: str)
        """
        try:
            if not self.is_loaded:
                self.load_model()
            
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            
            # Enhance if camera feed
            if is_camera:
                image = self._extract_and_enhance_face(image)
            
            # Preprocess
            inputs = self.processor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Run inference
            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
            
            # Get predictions
            probabilities = torch.nn.functional.softmax(logits, dim=-1)
            predicted_class = probabilities.argmax().item()
            confidence_raw = probabilities[0][predicted_class].item()
            
            # Store in buffer for camera stabilization
            if is_camera:
                self.frame_buffer.append({
                    'class': predicted_class,
                    'confidence': confidence_raw
                })
                
                # Average over buffer for stability
                if len(self.frame_buffer) >= 3:
                    avg_class = max(set([f['class'] for f in self.frame_buffer]), 
                                   key=list(f['class'] for f in self.frame_buffer).count)
                    avg_confidence = np.mean([f['confidence'] for f in self.frame_buffer 
                                             if f['class'] == avg_class])
                    predicted_class = avg_class
                    confidence_raw = avg_confidence
            
            confidence = confidence_raw * 100
            
            # Get label
            label = self._get_label(predicted_class)
            is_fake = label.lower() in ['fake', 'deepfake', 'synthetic']
            
            # Apply confidence threshold for camera (reduce false positives)
            if is_camera and confidence < 70:
                # Not confident enough, default to real
                is_fake = False
                confidence = 100 - confidence
            
            logger.info(f"{'Camera' if is_camera else 'Upload'} detection: {label} ({confidence:.2f}%)")
            
            return is_fake, confidence, self.model_config['display_name']
            
        except Exception as e:
            logger.error(f"Detection from bytes failed: {str(e)}")
            raise Exception(f"Detection failed: {str(e)}")
    
    def detect_video(self, video_path: str, fps: int = 1) -> Tuple[bool, float, str, dict]:
        """
        Detect if a video contains deepfakes
        
        Args:
            video_path: Path to video file
            fps: Frames per second to extract
            
        Returns:
            Tuple of (is_fake: bool, confidence: float, model_name: str, details: dict)
        """
        try:
            if not self.is_loaded:
                self.load_model()
            
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video not found: {video_path}")
            
            # Open video
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise Exception("Failed to open video file")
            
            # Get video properties
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            video_fps = int(cap.get(cv2.CAP_PROP_FPS))
            if video_fps == 0:
                video_fps = 30
            
            frame_interval = max(1, video_fps // fps)
            
            logger.info(f"Processing video: {total_frames} frames at {video_fps} FPS")
            
            # Process frames
            frame_results = []
            frame_count = 0
            processed_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % frame_interval == 0:
                    try:
                        # Convert BGR to RGB
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        pil_image = Image.fromarray(frame_rgb)
                        
                        # Enhance face
                        pil_image = self._extract_and_enhance_face(pil_image)
                        
                        # Detect
                        inputs = self.processor(images=pil_image, return_tensors="pt")
                        inputs = {k: v.to(self.device) for k, v in inputs.items()}
                        
                        with torch.no_grad():
                            outputs = self.model(**inputs)
                            logits = outputs.logits
                        
                        probabilities = torch.nn.functional.softmax(logits, dim=-1)
                        predicted_class = probabilities.argmax().item()
                        confidence = probabilities[0][predicted_class].item()
                        
                        label = self._get_label(predicted_class)
                        is_fake_frame = label.lower() in ['fake', 'deepfake', 'synthetic']
                        
                        frame_results.append({
                            'is_fake': is_fake_frame,
                            'confidence': confidence,
                            'frame_number': frame_count,
                            'label': label
                        })
                        
                        processed_count += 1
                        
                    except Exception as e:
                        logger.warning(f"Failed to process frame {frame_count}: {str(e)}")
                
                frame_count += 1
            
            cap.release()
            
            if not frame_results:
                raise Exception("No frames could be processed")
            
            # Aggregate results
            fake_votes = sum(1 for r in frame_results if r['is_fake'])
            real_votes = len(frame_results) - fake_votes
            
            avg_confidence = np.mean([r['confidence'] for r in frame_results]) * 100
            
            is_fake = fake_votes > real_votes
            vote_ratio = max(fake_votes, real_votes) / len(frame_results)
            overall_confidence = vote_ratio * avg_confidence
            
            details = {
                'total_frames': total_frames,
                'processed_frames': processed_count,
                'fake_frames': fake_votes,
                'real_frames': real_votes,
                'frame_results': frame_results[:10]
            }
            
            logger.info(f"Video: {'FAKE' if is_fake else 'REAL'} "
                       f"({fake_votes}/{processed_count} fake, {overall_confidence:.2f}%)")
            
            return is_fake, overall_confidence, self.model_config['display_name'], details
            
        except Exception as e:
            logger.error(f"Video detection failed: {str(e)}")
            raise Exception(f"Video detection failed: {str(e)}")


# Global detector cache
_detector_cache: Dict[str, DeepfakeDetector] = {}


def get_detector(model_key: str = 'dima806') -> DeepfakeDetector:
    """Get or create detector instance (cached)"""
    global _detector_cache
    
    if model_key not in AVAILABLE_MODELS:
        logger.warning(f"Unknown model: {model_key}, using dima806")
        model_key = 'dima806'
    
    if model_key not in _detector_cache:
        _detector_cache[model_key] = DeepfakeDetector(model_key)
    
    return _detector_cache[model_key]


def get_available_models() -> Dict[str, Dict]:
    """Get list of available models"""
    return {
        key: {
            'key': key,
            'name': config['display_name'],
            'description': config['description']
        }
        for key, config in AVAILABLE_MODELS.items()
    }


def detect_deepfake(file_path: str, file_type: str = 'image', 
                    model_key: str = 'dima806', enhance_face: bool = True) -> Tuple[bool, float, str]:
    """
    Main detection function
    
    Args:
        file_path: Path to file
        file_type: 'image' or 'video'
        model_key: Model to use
        enhance_face: Extract and enhance face
        
    Returns:
        Tuple of (is_fake: bool, confidence: float, model_name: str)
    """
    detector = get_detector(model_key)
    
    if file_type == 'video':
        is_fake, confidence, model_name, details = detector.detect_video(file_path)
        return is_fake, confidence, model_name
    else:
        return detector.detect_image(file_path, enhance_face=enhance_face)


def clear_model_cache():
    """Clear all loaded models from memory"""
    global _detector_cache
    _detector_cache.clear()
    logger.info("Model cache cleared")