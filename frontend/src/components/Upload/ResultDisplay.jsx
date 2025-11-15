import { CheckCircle, XCircle, AlertTriangle } from 'lucide-react';

const ResultDisplay = ({ result, type }) => {
  if (!result) return null;

  const { is_fake, confidence, message } = result;

  return (
    <div className="mt-6 bg-white rounded-xl shadow-lg p-6 border-2 border-gray-200">
      <h3 className="text-xl font-bold text-gray-900 mb-4">Detection Result</h3>
      
      {/* Verdict Badge */}
      <div className="flex items-center justify-center mb-6">
        {is_fake ? (
          <div className="flex items-center space-x-3 px-6 py-4 bg-red-100 border-2 border-red-300 rounded-xl">
            <XCircle className="w-10 h-10 text-red-600" />
            <div>
              <p className="text-2xl font-bold text-red-700">FAKE DETECTED</p>
              <p className="text-sm text-red-600">This content appears to be manipulated</p>
            </div>
          </div>
        ) : (
          <div className="flex items-center space-x-3 px-6 py-4 bg-green-100 border-2 border-green-300 rounded-xl">
            <CheckCircle className="w-10 h-10 text-green-600" />
            <div>
              <p className="text-2xl font-bold text-green-700">AUTHENTIC</p>
              <p className="text-sm text-green-600">This content appears to be genuine</p>
            </div>
          </div>
        )}
      </div>

      {/* Confidence Score */}
      <div className="mb-4">
        <div className="flex justify-between items-center mb-2">
          <span className="text-sm font-medium text-gray-700">Confidence Score</span>
          <span className="text-lg font-bold text-gray-900">{confidence}%</span>
        </div>
        <div className="w-full bg-gray-200 rounded-full h-4 overflow-hidden">
          <div
            className={`h-full rounded-full transition-all duration-500 ${
              is_fake ? 'bg-red-500' : 'bg-green-500'
            }`}
            style={{ width: `${confidence}%` }}
          ></div>
        </div>
      </div>

      {/* Additional Info */}
      <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 flex items-start">
        <AlertTriangle className="w-5 h-5 text-blue-600 mr-2 flex-shrink-0 mt-0.5" />
        <div>
          <p className="text-sm font-medium text-blue-900 mb-1">Analysis Complete</p>
          <p className="text-sm text-blue-700">{message}</p>
        </div>
      </div>

      {/* Timestamp */}
      <p className="text-xs text-gray-500 mt-4 text-center">
        Analyzed at {new Date().toLocaleString()}
      </p>
    </div>
  );
};

export default ResultDisplay;
