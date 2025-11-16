import { CheckCircle, XCircle, AlertTriangle, Shield, Clock } from 'lucide-react';

const ResultDisplay = ({ result, type }) => {
  if (!result) return null;

  const { is_fake, confidence, message } = result;

  return (
    <div className="mt-8 bg-white dark:bg-gray-800 rounded-2xl shadow-xl p-8 border border-gray-200 dark:border-gray-700 animate-slide-up">
      <div className="flex items-center space-x-3 mb-6">
        <div className="bg-gradient-to-br from-primary-500 to-primary-600 p-2 rounded-lg">
          <Shield className="w-5 h-5 text-white" />
        </div>
        <h3 className="text-2xl font-bold text-gray-900 dark:text-white">Detection Result</h3>
      </div>
      
      {/* Verdict Badge */}
      <div className="flex items-center justify-center mb-8">
        {is_fake ? (
          <div className="relative overflow-hidden flex items-center space-x-4 px-8 py-6 bg-gradient-to-br from-red-50 to-red-100 dark:from-red-900/20 dark:to-red-800/20 border-2 border-red-300 dark:border-red-700 rounded-2xl shadow-lg">
            <div className="absolute top-0 right-0 w-32 h-32 bg-red-500 opacity-10 rounded-full -mr-16 -mt-16"></div>
            <div className="relative bg-red-500 p-3 rounded-xl shadow-lg">
              <XCircle className="w-10 h-10 text-white" />
            </div>
            <div className="relative">
              <p className="text-3xl font-bold text-red-700 dark:text-red-400">FAKE DETECTED</p>
              <p className="text-sm text-red-600 dark:text-red-500 mt-1">This content appears to be manipulated</p>
            </div>
          </div>
        ) : (
          <div className="relative overflow-hidden flex items-center space-x-4 px-8 py-6 bg-gradient-to-br from-green-50 to-emerald-100 dark:from-green-900/20 dark:to-emerald-800/20 border-2 border-green-300 dark:border-green-700 rounded-2xl shadow-lg">
            <div className="absolute top-0 right-0 w-32 h-32 bg-green-500 opacity-10 rounded-full -mr-16 -mt-16"></div>
            <div className="relative bg-green-500 p-3 rounded-xl shadow-lg">
              <CheckCircle className="w-10 h-10 text-white" />
            </div>
            <div className="relative">
              <p className="text-3xl font-bold text-green-700 dark:text-green-400">AUTHENTIC</p>
              <p className="text-sm text-green-600 dark:text-green-500 mt-1">This content appears to be genuine</p>
            </div>
          </div>
        )}
      </div>

      {/* Confidence Score */}
      <div className="mb-6 p-6 bg-gray-50 dark:bg-gray-900/50 rounded-xl border border-gray-200 dark:border-gray-700">
        <div className="flex justify-between items-center mb-3">
          <span className="text-sm font-semibold text-gray-700 dark:text-gray-300">Confidence Score</span>
          <span className="text-2xl font-bold bg-gradient-to-r from-primary-600 to-primary-800 dark:from-primary-400 dark:to-primary-600 bg-clip-text text-transparent">
            {confidence}%
          </span>
        </div>
        <div className="relative w-full bg-gray-200 dark:bg-gray-700 rounded-full h-3 overflow-hidden shadow-inner">
          <div
            className={`h-full rounded-full transition-all duration-1000 ease-out ${
              is_fake 
                ? 'bg-gradient-to-r from-red-500 to-red-600 shadow-lg shadow-red-500/50' 
                : 'bg-gradient-to-r from-green-500 to-emerald-600 shadow-lg shadow-green-500/50'
            }`}
            style={{ width: `${confidence}%` }}
          ></div>
        </div>
        <div className="flex justify-between mt-2 text-xs text-gray-500 dark:text-gray-400">
          <span>0%</span>
          <span>50%</span>
          <span>100%</span>
        </div>
      </div>

      {/* Additional Info */}
      <div className="bg-blue-50 dark:bg-blue-900/20 border border-blue-200 dark:border-blue-800 rounded-xl p-5 flex items-start space-x-3">
        <div className="bg-blue-500 p-2 rounded-lg flex-shrink-0">
          <AlertTriangle className="w-5 h-5 text-white" />
        </div>
        <div className="flex-1">
          <p className="text-sm font-semibold text-blue-900 dark:text-blue-300 mb-1">Analysis Complete</p>
          <p className="text-sm text-blue-700 dark:text-blue-400">{message}</p>
        </div>
      </div>

      {/* Timestamp */}
      <div className="flex items-center justify-center space-x-2 mt-6 text-xs text-gray-500 dark:text-gray-400">
        <Clock className="w-3.5 h-3.5" />
        <span>Analyzed at {new Date().toLocaleString()}</span>
      </div>
    </div>
  );
};

export default ResultDisplay;
