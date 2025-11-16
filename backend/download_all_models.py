"""
Script to pre-download all available deepfake detection models.
Run this before starting the application to avoid delays on first use.
"""
from ml_model import AVAILABLE_MODELS, DeepfakeDetector
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def download_all_models():
    """Download and cache all available models."""
    print("=" * 60)
    print("DOWNLOADING ALL DEEPFAKE DETECTION MODELS")
    print("=" * 60)
    
    for model_key, model_config in AVAILABLE_MODELS.items():
        try:
            print(f"\n[{model_key}] Downloading: {model_config['display_name']}")
            print(f"Description: {model_config['description']}")
            
            detector = DeepfakeDetector(model_key)
            detector.load_model()
            
            print(f"✓ Successfully loaded {model_config['display_name']}")
            
        except Exception as e:
            print(f"✗ Failed to load {model_config['display_name']}: {str(e)}")
            print("  This model will be downloaded on first use.")
    
    print("\n" + "=" * 60)
    print("MODEL DOWNLOAD COMPLETE")
    print("=" * 60)

if __name__ == '__main__':
    download_all_models()
