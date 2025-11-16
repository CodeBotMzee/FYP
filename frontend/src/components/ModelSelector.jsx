import { useState, useEffect } from 'react';
import { Brain, ChevronDown } from 'lucide-react';
import { detectionAPI } from '../services/api';

const ModelSelector = ({ selectedModel, onModelChange, disabled = false }) => {
  const [models, setModels] = useState([]);
  const [loading, setLoading] = useState(true);
  const [isOpen, setIsOpen] = useState(false);

  useEffect(() => {
    fetchModels();
  }, []);

  const fetchModels = async () => {
    try {
      const response = await detectionAPI.getModels();
      if (response.success) {
        setModels(response.models);
        // Set default model if none selected
        if (!selectedModel && response.models.length > 0) {
          onModelChange(response.models[0].key);
        }
      }
    } catch (error) {
      console.error('Failed to fetch models:', error);
    } finally {
      setLoading(false);
    }
  };

  const selectedModelData = models.find(m => m.key === selectedModel) || models[0];

  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl p-4 border border-gray-200 dark:border-gray-700">
        <div className="animate-pulse flex items-center space-x-3">
          <div className="w-10 h-10 bg-gray-200 dark:bg-gray-700 rounded-lg"></div>
          <div className="flex-1">
            <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-32 mb-2"></div>
            <div className="h-3 bg-gray-200 dark:bg-gray-700 rounded w-48"></div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl border border-gray-200 dark:border-gray-700 shadow-sm">
      <div className="p-4">
        <label className="block text-sm font-semibold text-gray-700 dark:text-gray-300 mb-3">
          Detection Model
        </label>
        
        <div className="relative">
          <button
            type="button"
            onClick={() => !disabled && setIsOpen(!isOpen)}
            disabled={disabled}
            className={`w-full flex items-center justify-between p-3 bg-gray-50 dark:bg-gray-900/50 rounded-lg border border-gray-200 dark:border-gray-700 transition-all duration-200 ${
              disabled 
                ? 'opacity-50 cursor-not-allowed' 
                : 'hover:border-primary-500 dark:hover:border-primary-400 cursor-pointer'
            }`}
          >
            <div className="flex items-center space-x-3">
              <div className="bg-gradient-to-br from-primary-500 to-primary-600 p-2 rounded-lg">
                <Brain className="w-5 h-5 text-white" />
              </div>
              <div className="text-left">
                <p className="font-semibold text-gray-900 dark:text-white text-sm">
                  {selectedModelData?.name || 'Select Model'}
                </p>
                <p className="text-xs text-gray-500 dark:text-gray-400">
                  {selectedModelData?.description || 'Choose a detection model'}
                </p>
              </div>
            </div>
            <ChevronDown 
              className={`w-5 h-5 text-gray-400 transition-transform duration-200 ${
                isOpen ? 'transform rotate-180' : ''
              }`} 
            />
          </button>

          {/* Dropdown Menu */}
          {isOpen && !disabled && (
            <div className="absolute z-10 w-full mt-2 bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg shadow-lg overflow-hidden animate-slide-up">
              {models.map((model) => (
                <button
                  key={model.key}
                  type="button"
                  onClick={() => {
                    onModelChange(model.key);
                    setIsOpen(false);
                  }}
                  className={`w-full p-3 text-left hover:bg-gray-50 dark:hover:bg-gray-700 transition-colors duration-150 ${
                    selectedModel === model.key 
                      ? 'bg-primary-50 dark:bg-primary-900/20 border-l-4 border-primary-500' 
                      : ''
                  }`}
                >
                  <p className="font-semibold text-gray-900 dark:text-white text-sm">
                    {model.name}
                  </p>
                  <p className="text-xs text-gray-500 dark:text-gray-400 mt-1">
                    {model.description}
                  </p>
                </button>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};

export default ModelSelector;
