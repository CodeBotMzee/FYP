import { useState, useRef } from 'react';
import { Upload, Video as VideoIcon, X, Loader, Play } from 'lucide-react';
import { detectionAPI } from '../../services/api';
import ResultDisplay from './ResultDisplay';

const VideoUpload = () => {
  const [selectedFile, setSelectedFile] = useState(null);
  const [preview, setPreview] = useState(null);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const fileInputRef = useRef(null);
  const videoRef = useRef(null);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    handleFile(file);
  };

  const handleFile = (file) => {
    if (!file) return;

    // Validate file type
    if (!file.type.startsWith('video/')) {
      setError('Please select a valid video file');
      return;
    }

    // Validate file size (100MB)
    if (file.size > 100 * 1024 * 1024) {
      setError('File size must be less than 100MB');
      return;
    }

    setError('');
    setSelectedFile(file);
    setResult(null);

    // Create preview
    const reader = new FileReader();
    reader.onloadend = () => {
      setPreview(reader.result);
    };
    reader.readAsDataURL(file);
  };

  const handleAnalyze = async () => {
    if (!selectedFile) return;

    setLoading(true);
    setError('');

    try {
      const response = await detectionAPI.detectVideo(selectedFile);
      
      if (response.success) {
        setResult(response);
      }
    } catch (err) {
      setError(err.response?.data?.message || 'Analysis failed. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setSelectedFile(null);
    setPreview(null);
    setResult(null);
    setError('');
    if (fileInputRef.current) {
      fileInputRef.current.value = '';
    }
  };

  return (
    <div className="p-6 max-w-4xl mx-auto">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Video Detection</h1>
        <p className="text-gray-600">Upload a video to analyze for deepfake manipulation</p>
      </div>

      {/* Upload Area */}
      {!preview ? (
        <div
          className="border-2 border-dashed border-gray-300 rounded-xl p-12 text-center hover:border-primary transition cursor-pointer bg-gray-50"
          onClick={() => fileInputRef.current?.click()}
        >
          <Upload className="w-16 h-16 text-gray-400 mx-auto mb-4" />
          <p className="text-lg font-semibold text-gray-700 mb-2">
            Click to select a video file
          </p>
          <p className="text-sm text-gray-500">
            Supports: MP4, AVI (Max 100MB)
          </p>
          <input
            ref={fileInputRef}
            type="file"
            accept="video/*"
            onChange={handleFileSelect}
            className="hidden"
          />
        </div>
      ) : (
        <div className="bg-white rounded-xl shadow-lg p-6 border border-gray-200">
          {/* Video Preview */}
          <div className="relative bg-black rounded-lg overflow-hidden">
            <video
              ref={videoRef}
              src={preview}
              controls
              className="w-full max-h-96"
            >
              Your browser does not support the video tag.
            </video>
            <button
              onClick={handleReset}
              className="absolute top-2 right-2 p-2 bg-red-500 text-white rounded-full hover:bg-red-600 transition"
            >
              <X className="w-5 h-5" />
            </button>
          </div>

          {/* File Info */}
          <div className="mt-4 p-4 bg-gray-50 rounded-lg">
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-3">
                <VideoIcon className="w-5 h-5 text-gray-600" />
                <div>
                  <p className="font-medium text-gray-900">{selectedFile?.name}</p>
                  <p className="text-sm text-gray-500">
                    {(selectedFile?.size / 1024 / 1024).toFixed(2)} MB
                  </p>
                </div>
              </div>
            </div>
          </div>

          {/* Analyze Button */}
          {!result && (
            <button
              onClick={handleAnalyze}
              disabled={loading}
              className="w-full mt-4 bg-primary text-white py-3 rounded-lg font-semibold hover:bg-blue-600 transition disabled:opacity-50 disabled:cursor-not-allowed flex items-center justify-center"
            >
              {loading ? (
                <>
                  <Loader className="w-5 h-5 mr-2 animate-spin" />
                  Analyzing Video... This may take a while
                </>
              ) : (
                <>
                  <Play className="w-5 h-5 mr-2" />
                  Analyze Video
                </>
              )}
            </button>
          )}

          {/* Upload Another Button */}
          {result && (
            <button
              onClick={handleReset}
              className="w-full mt-4 bg-gray-200 text-gray-700 py-3 rounded-lg font-semibold hover:bg-gray-300 transition"
            >
              Upload Another Video
            </button>
          )}
        </div>
      )}

      {/* Error Message */}
      {error && (
        <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-lg">
          <p className="text-sm text-red-700">{error}</p>
        </div>
      )}

      {/* Result Display */}
      {result && <ResultDisplay result={result} type="video" />}
    </div>
  );
};

export default VideoUpload;
