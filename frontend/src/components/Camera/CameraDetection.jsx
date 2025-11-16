import { useState, useRef, useCallback } from 'react';
import Webcam from 'react-webcam';
import { Camera, Play, Square, Loader, CheckCircle, XCircle } from 'lucide-react';
import { detectionAPI } from '../../services/api';
import ModelSelector from '../ModelSelector';

const CameraDetection = () => {
  const webcamRef = useRef(null);
  const [isDetecting, setIsDetecting] = useState(false);
  const [currentResult, setCurrentResult] = useState(null);
  const [detectionCount, setDetectionCount] = useState(0);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState('');
  const [selectedModel, setSelectedModel] = useState('dima806');
  const intervalRef = useRef(null);

  const captureAndDetect = useCallback(async () => {
    if (!webcamRef.current || processing) return;

    setProcessing(true);
    setError('');

    try {
      // Capture frame as base64
      const imageSrc = webcamRef.current.getScreenshot();
      
      if (!imageSrc) {
        setError('Failed to capture frame');
        setProcessing(false);
        return;
      }

      // Send to API
      const response = await detectionAPI.detectCamera(imageSrc, selectedModel);

      if (response.success) {
        setCurrentResult(response);
        setDetectionCount((prev) => prev + 1);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Detection failed');
    } finally {
      setProcessing(false);
    }
  }, [processing, selectedModel]);

  const startDetection = () => {
    setIsDetecting(true);
    setDetectionCount(0);
    setCurrentResult(null);
    
    // Capture and detect every 2 seconds
    intervalRef.current = setInterval(() => {
      captureAndDetect();
    }, 2000);
  };

  const stopDetection = () => {
    setIsDetecting(false);
    if (intervalRef.current) {
      clearInterval(intervalRef.current);
      intervalRef.current = null;
    }
  };

  const videoConstraints = {
    width: 640,
    height: 480,
    facingMode: 'user',
  };

  return (
    <div className="p-6 max-w-5xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 dark:text-white mb-2">Live Camera Detection</h1>
        <p className="text-gray-600 dark:text-gray-400">Real-time deepfake detection from your webcam</p>
      </div>

      {/* Model Selector */}
      <div className="mb-6">
        <ModelSelector 
          selectedModel={selectedModel}
          onModelChange={setSelectedModel}
          disabled={isDetecting}
        />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Camera Feed */}
        <div className="lg:col-span-2">
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <div className="relative bg-black rounded-lg overflow-hidden">
              <Webcam
                ref={webcamRef}
                audio={false}
                screenshotFormat="image/jpeg"
                videoConstraints={videoConstraints}
                className="w-full"
              />
              
              {/* Processing Overlay */}
              {processing && (
                <div className="absolute inset-0 bg-black bg-opacity-50 flex items-center justify-center">
                  <div className="bg-white rounded-lg p-4 flex items-center space-x-3">
                    <Loader className="w-6 h-6 text-primary animate-spin" />
                    <span className="font-semibold text-gray-900">Processing...</span>
                  </div>
                </div>
              )}

              {/* Result Overlay */}
              {currentResult && isDetecting && (
                <div className="absolute top-4 left-4 right-4">
                  <div
                    className={`p-4 rounded-lg shadow-lg ${
                      currentResult.is_fake
                        ? 'bg-red-500 bg-opacity-90'
                        : 'bg-green-500 bg-opacity-90'
                    }`}
                  >
                    <div className="flex items-center justify-between text-white">
                      <div className="flex items-center space-x-2">
                        {currentResult.is_fake ? (
                          <XCircle className="w-6 h-6" />
                        ) : (
                          <CheckCircle className="w-6 h-6" />
                        )}
                        <span className="font-bold text-lg">
                          {currentResult.is_fake ? 'FAKE DETECTED' : 'AUTHENTIC'}
                        </span>
                      </div>
                      <span className="font-bold text-lg">
                        {currentResult.confidence.toFixed(1)}%
                      </span>
                    </div>
                  </div>
                </div>
              )}

              {/* Detection Status */}
              {isDetecting && (
                <div className="absolute bottom-4 left-4">
                  <div className="bg-red-500 text-white px-3 py-1 rounded-full flex items-center space-x-2 animate-pulse">
                    <div className="w-2 h-2 bg-white rounded-full"></div>
                    <span className="text-sm font-semibold">LIVE</span>
                  </div>
                </div>
              )}
            </div>

            {/* Controls */}
            <div className="mt-4 flex space-x-3">
              {!isDetecting ? (
                <button
                  onClick={startDetection}
                  className="flex-1 bg-gradient-to-r from-green-500 to-green-600 hover:from-green-600 hover:to-green-700 text-white py-3 rounded-lg font-semibold transition-all duration-200 flex items-center justify-center shadow-md hover:shadow-lg"
                >
                  <Play className="w-5 h-5 mr-2" />
                  Start Detection
                </button>
              ) : (
                <button
                  onClick={stopDetection}
                  className="flex-1 bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white py-3 rounded-lg font-semibold transition-all duration-200 flex items-center justify-center shadow-md hover:shadow-lg"
                >
                  <Square className="w-5 h-5 mr-2" />
                  Stop Detection
                </button>
              )}
            </div>

            {/* Error Message */}
            {error && (
              <div className="mt-4 p-3 bg-red-50 border border-red-200 rounded-lg">
                <p className="text-sm text-red-700">{error}</p>
              </div>
            )}
          </div>
        </div>

        {/* Stats Panel */}
        <div className="space-y-4">
          {/* Detection Counter */}
          <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
            <div className="flex items-center justify-between mb-4">
              <h3 className="font-bold text-gray-900">Session Stats</h3>
              <Camera className="w-5 h-5 text-primary" />
            </div>
            <div className="space-y-3">
              <div>
                <p className="text-sm text-gray-600 mb-1">Detections</p>
                <p className="text-3xl font-bold text-gray-900">{detectionCount}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-1">Status</p>
                <span
                  className={`inline-block px-3 py-1 rounded-full text-sm font-semibold ${
                    isDetecting
                      ? 'bg-green-100 text-green-700'
                      : 'bg-gray-100 text-gray-700'
                  }`}
                >
                  {isDetecting ? 'Active' : 'Inactive'}
                </span>
              </div>
            </div>
          </div>

          {/* Current Result */}
          {currentResult && (
            <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
              <h3 className="font-bold text-gray-900 mb-4">Latest Result</h3>
              <div className="space-y-3">
                <div>
                  <p className="text-sm text-gray-600 mb-2">Verdict</p>
                  <div
                    className={`flex items-center space-x-2 px-3 py-2 rounded-lg ${
                      currentResult.is_fake
                        ? 'bg-red-100 text-red-700'
                        : 'bg-green-100 text-green-700'
                    }`}
                  >
                    {currentResult.is_fake ? (
                      <XCircle className="w-5 h-5" />
                    ) : (
                      <CheckCircle className="w-5 h-5" />
                    )}
                    <span className="font-semibold">
                      {currentResult.is_fake ? 'Fake' : 'Real'}
                    </span>
                  </div>
                </div>
                <div>
                  <p className="text-sm text-gray-600 mb-2">Confidence</p>
                  <div className="flex items-center space-x-2">
                    <div className="flex-1 bg-gray-200 rounded-full h-2">
                      <div
                        className={`h-full rounded-full ${
                          currentResult.is_fake ? 'bg-red-500' : 'bg-green-500'
                        }`}
                        style={{ width: `${currentResult.confidence}%` }}
                      ></div>
                    </div>
                    <span className="text-sm font-bold text-gray-900">
                      {currentResult.confidence.toFixed(1)}%
                    </span>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Instructions */}
          <div className="bg-blue-50 rounded-xl p-4 border border-blue-200">
            <h4 className="font-semibold text-blue-900 mb-2">Instructions</h4>
            <ul className="text-sm text-blue-700 space-y-1">
              <li>• Allow camera access when prompted</li>
              <li>• Click "Start Detection" to begin</li>
              <li>• Analysis runs every 2 seconds</li>
              <li>• Results appear in real-time</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CameraDetection;
