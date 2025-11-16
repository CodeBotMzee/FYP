"""
Quick test script to verify model switching functionality.
Run this to ensure all models can be loaded correctly.
"""
import sys
sys.path.insert(0, 'backend')

from ml_model import get_detector, get_available_models

def test_models():
    """Test that all models can be initialized."""
    print("=" * 60)
    print("TESTING MODEL SWITCHING FUNCTIONALITY")
    print("=" * 60)
    
    # Get available models
    models = get_available_models()
    print(f"\n✓ Found {len(models)} available models:")
    for key, info in models.items():
        print(f"  - {key}: {info['name']}")
    
    # Test each model initialization (without loading)
    print("\n" + "=" * 60)
    print("TESTING MODEL INITIALIZATION")
    print("=" * 60)
    
    for model_key in models.keys():
        try:
            print(f"\n[{model_key}] Initializing detector...")
            detector = get_detector(model_key)
            print(f"✓ {model_key}: Initialized successfully")
            print(f"  - Model: {detector.model_name}")
            print(f"  - Device: {detector.device}")
            print(f"  - Processor Type: {detector.processor_type}")
        except Exception as e:
            print(f"✗ {model_key}: Failed - {str(e)}")
    
    print("\n" + "=" * 60)
    print("TEST COMPLETE")
    print("=" * 60)
    print("\nNote: Models are not loaded yet (lazy loading).")
    print("They will be downloaded and loaded on first detection request.")
    print("\nTo pre-download all models, run:")
    print("  python backend/download_all_models.py")

if __name__ == '__main__':
    test_models()
