"""
Machine Learning Model Handler for Deepfake Detection
Uses HuggingFace transformers with dima806/deepfake_vs_real_image_detection model
"""
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification
from PIL import Image
import cv2
import numpy as np
import os
import io
from typing import Tuple, List
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepfakeDetector:
    """
    Deepfake detection model handler using HuggingFace transformers.
    Caches model in memory for faster inference.
    """
    
    def __init__(self, model_name="dima806/deepfake_vs_real_image_detection"):
        """
        Initialize the deepfake detector.
        
        Args:
            model_name: HuggingFace model identifier
        """
        self.model_name = model_name
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.processor = None
        self.model = None
        self.is_loaded = False
        
        logger.info(f"Initializing DeepfakeDetector on device: {self.device}")
        
    def load_model(self):
        """
        Load the model and processor into memory.
        Called lazily on first detection request.
        """
        if self.is_loaded:
            return
        
        try:
            logger.info(f"Loading model: {self.model_name}")
            
            # Load processor and model
            self.processor = AutoImageProcessor.from_pretrained(self.model_name)
            self.model = AutoModelForImageClassification.from_pretrained(self.model_name)
            
            # Move model to appropriate device
            self.model.to(self.device)
            self.model.eval()  # Set to evaluation mode
            
            self.is_loaded = True
            logger.info("Model loaded successfully")
            
        except Exception as e:
            logger.error(f"Failed to load model: {str(e)}")
            raise Exception(f"Model loading failed: {str(e)}")
    
    def detect_image(self, image_path: str) -> Tuple[bool, float, str]:
        """
        Detect if an image is a deepfake.
        
        Args:
            image_path: Path to the image file
            
        Returns:
            Tuple of (is_fake: bool, confidence: float, model_name: str)
        """
        try:
            # Ensure model is loaded
            if not self.is_loaded:
                self.load_model()
            
            # Load and validate image
            if not os.path.exists(image_path):
                raise FileNotFoundError(f"Image not found: {image_path}")
            
            # Open image with PIL
            image = Image.open(image_path).convert('RGB')
            
            # Preprocess image
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
            
            # Model labels: 0 = Fake, 1 = Real
            is_fake = (predicted_class == 0)
            
            logger.info(f"Detection result: {'FAKE' if is_fake else 'REAL'} (confidence: {confidence:.2f}%)")
            
            return is_fake, confidence, f"{self.model_name}_v1.0"
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Detection failed: {str(e)}")
            raise Exception(f"Image detection failed: {str(e)}")
    
    def detect_video(self, video_path: str, fps: int = 1) -> Tuple[bool, float, str, dict]:
        """
        Detect if a video contains deepfakes by analyzing frames.
        
        Args:
            video_path: Path to the video file
            fps: Frames per second to extract (default: 1)
            
        Returns:
            Tuple of (is_fake: bool, confidence: float, model_name: str, details: dict)
        """
        try:
            # Ensure model is loaded
            if not self.is_loaded:
                self.load_model()
            
            # Validate video file
            if not os.path.exists(video_path):
                raise FileNotFoundError(f"Video not found: {video_path}")
            
            # Open video with OpenCV
            cap = cv2.VideoCapture(video_path)
            if not cap.isOpened():
                raise Exception("Failed to open video file")
            
            # Get video properties
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            video_fps = int(cap.get(cv2.CAP_PROP_FPS))
            
            if video_fps == 0:
                video_fps = 30  # Default fallback
            
            # Calculate frame interval
            frame_interval = max(1, video_fps // fps)
            
            logger.info(f"Processing video: {total_frames} frames at {video_fps} FPS")
            logger.info(f"Extracting 1 frame every {frame_interval} frames")
            
            # Extract and analyze frames
            frame_results = []
            frame_count = 0
            processed_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Process every Nth frame
                if frame_count % frame_interval == 0:
                    try:
                        # Convert BGR to RGB
                        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                        pil_image = Image.fromarray(frame_rgb)
                        
                        # Preprocess and detect
                        inputs = self.processor(images=pil_image, return_tensors="pt")
                        inputs = {k: v.to(self.device) for k, v in inputs.items()}
                        
                        with torch.no_grad():
                            outputs = self.model(**inputs)
                            logits = outputs.logits
                        
                        probabilities = torch.nn.functional.softmax(logits, dim=-1)
                        predicted_class = probabilities.argmax().item()
                        confidence = probabilities[0][predicted_class].item()
                        
                        is_fake_frame = (predicted_class == 0)
                        frame_results.append({
                            'is_fake': is_fake_frame,
                            'confidence': confidence,
                            'frame_number': frame_count
                        })
                        
                        processed_count += 1
                        
                    except Exception as e:
                        logger.warning(f"Failed to process frame {frame_count}: {str(e)}")
                
                frame_count += 1
            
            cap.release()
            
            if not frame_results:
                raise Exception("No frames could be processed from video")
            
            # Aggregate results using weighted voting
            fake_votes = sum(1 for r in frame_results if r['is_fake'])
            real_votes = len(frame_results) - fake_votes
            
            # Calculate average confidence
            avg_confidence = np.mean([r['confidence'] for r in frame_results]) * 100
            
            # Determine overall verdict (majority vote)
            is_fake = fake_votes > real_votes
            
            # Calculate confidence based on vote ratio
            vote_ratio = max(fake_votes, real_votes) / len(frame_results)
            overall_confidence = vote_ratio * avg_confidence
            
            details = {
                'total_frames': total_frames,
                'processed_frames': processed_count,
                'fake_frames': fake_votes,
                'real_frames': real_votes,
                'frame_results': frame_results[:10]  # Include first 10 for reference
            }
            
            logger.info(f"Video detection: {'FAKE' if is_fake else 'REAL'} "
                       f"({fake_votes}/{processed_count} fake frames, confidence: {overall_confidence:.2f}%)")
            
            return is_fake, overall_confidence, f"{self.model_name}_v1.0", details
            
        except FileNotFoundError as e:
            logger.error(f"File not found: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Video detection failed: {str(e)}")
            raise Exception(f"Video detection failed: {str(e)}")
    
    def detect_from_bytes(self, image_bytes: bytes) -> Tuple[bool, float, str]:
        """
        Detect deepfake from image bytes (for camera detection).
        
        Args:
            image_bytes: Raw image bytes
            
        Returns:
            Tuple of (is_fake: bool, confidence: float, model_name: str)
        """
        try:
            # Ensure model is loaded
            if not self.is_loaded:
                self.load_model()
            
            # Convert bytes to PIL Image
            image = Image.open(io.BytesIO(image_bytes)).convert('RGB')
            
            # Preprocess image
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
            
            # Model labels: 0 = Fake, 1 = Real
            is_fake = (predicted_class == 0)
            
            return is_fake, confidence, f"{self.model_name}_v1.0"
            
        except Exception as e:
            logger.error(f"Detection from bytes failed: {str(e)}")
            raise Exception(f"Detection failed: {str(e)}")


# Global detector instance (singleton pattern for model caching)
_detector_instance = None

def get_detector() -> DeepfakeDetector:
    """
    Get or create the global detector instance.
    This ensures the model is loaded only once and reused.
    """
    global _detector_instance
    if _detector_instance is None:
        _detector_instance = DeepfakeDetector()
    return _detector_instance


def detect_deepfake(file_path: str, file_type: str = 'image') -> Tuple[bool, float, str]:
    """
    Main detection function that routes to appropriate detector.
    
    Args:
        file_path: Path to the file
        file_type: Type of file ('image' or 'video')
        
    Returns:
        Tuple of (is_fake: bool, confidence: float, model_name: str)
    """
    detector = get_detector()
    
    if file_type == 'video':
        is_fake, confidence, model_name, details = detector.detect_video(file_path)
        return is_fake, confidence, model_name
    else:
        return detector.detect_image(file_path)
