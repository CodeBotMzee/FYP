"""
Script to download and cache the HuggingFace model.
Run this before starting the server to avoid delays on first request.
"""
from ml_model import get_detector
import sys

def download_model():
    """Download and cache the deepfake detection model."""
    print("=" * 60)
    print("DOWNLOADING DEEPFAKE DETECTION MODEL")
    print("=" * 60)
    print()
    print("Model: dima806/deepfake_vs_real_image_detection")
    print("This may take a few minutes on first run...")
    print()
    
    try:
        # Get detector instance and load model
        detector = get_detector()
        detector.load_model()
        
        print()
        print("=" * 60)
        print("✓ MODEL DOWNLOADED AND CACHED SUCCESSFULLY")
        print("=" * 60)
        print()
        print(f"Device: {detector.device}")
        print(f"Model: {detector.model_name}")
        print()
        print("You can now start the Flask server with: python app.py")
        print()
        
        return True
        
    except Exception as e:
        print()
        print("=" * 60)
        print("✗ MODEL DOWNLOAD FAILED")
        print("=" * 60)
        print()
        print(f"Error: {str(e)}")
        print()
        print("Troubleshooting:")
        print("1. Check your internet connection")
        print("2. Ensure you have enough disk space")
        print("3. Try: pip install --upgrade transformers torch")
        print()
        return False

if __name__ == "__main__":
    success = download_model()
    sys.exit(0 if success else 1)
