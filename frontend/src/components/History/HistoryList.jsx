import { useState, useEffect } from 'react';
import { CheckCircle, XCircle, Image, Video, Camera, Filter } from 'lucide-react';
import { historyAPI } from '../../services/api';

const HistoryList = () => {
  const [history, setHistory] = useState([]);
  const [filteredHistory, setFilteredHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [typeFilter, setTypeFilter] = useState('all');
  const [resultFilter, setResultFilter] = useState('all');
  const [modelFilter, setModelFilter] = useState('all');
  const [currentPage, setCurrentPage] = useState(1);
  const itemsPerPage = 10;

  useEffect(() => {
    fetchHistory();
  }, []);

  useEffect(() => {
    applyFilters();
  }, [history, typeFilter, resultFilter, modelFilter]);

  const fetchHistory = async () => {
    try {
      const response = await historyAPI.getAll();
      if (response.success) {
        setHistory(response.history);
      }
    } catch (error) {
      console.error('Failed to fetch history:', error);
    } finally {
      setLoading(false);
    }
  };

  const applyFilters = () => {
    let filtered = [...history];

    // Type filter
    if (typeFilter !== 'all') {
      filtered = filtered.filter((item) => item.detection_type === typeFilter);
    }

    // Result filter
    if (resultFilter !== 'all') {
      const isFake = resultFilter === 'fake';
      filtered = filtered.filter((item) => item.is_fake === isFake);
    }

    // Model filter
    if (modelFilter !== 'all') {
      filtered = filtered.filter((item) => 
        item.model_version && item.model_version.toLowerCase().includes(modelFilter.toLowerCase())
      );
    }

    setFilteredHistory(filtered);
    setCurrentPage(1);
  };

  const getTypeIcon = (type) => {
    switch (type) {
      case 'image':
        return <Image className="w-5 h-5" />;
      case 'video':
        return <Video className="w-5 h-5" />;
      case 'camera':
        return <Camera className="w-5 h-5" />;
      default:
        return <Image className="w-5 h-5" />;
    }
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date.toLocaleString();
  };

  // Pagination
  const indexOfLastItem = currentPage * itemsPerPage;
  const indexOfFirstItem = indexOfLastItem - itemsPerPage;
  const currentItems = filteredHistory.slice(indexOfFirstItem, indexOfLastItem);
  const totalPages = Math.ceil(filteredHistory.length / itemsPerPage);

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="p-6">
      <div className="mb-6">
        <h1 className="text-3xl font-bold text-gray-900 mb-2">Detection History</h1>
        <p className="text-gray-600">View and filter your past detections</p>
      </div>

      {/* Filters */}
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow-md p-6 mb-6 border border-gray-200 dark:border-gray-700">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          {/* Type Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Type
            </label>
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              <option value="all">All Types</option>
              <option value="image">Image</option>
              <option value="video">Video</option>
              <option value="camera">Camera</option>
            </select>
          </div>

          {/* Result Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Result
            </label>
            <select
              value={resultFilter}
              onChange={(e) => setResultFilter(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              <option value="all">All Results</option>
              <option value="fake">Fake</option>
              <option value="real">Real</option>
            </select>
          </div>

          {/* Model Filter */}
          <div>
            <label className="block text-sm font-medium text-gray-700 dark:text-gray-300 mb-2">
              Model
            </label>
            <select
              value={modelFilter}
              onChange={(e) => setModelFilter(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 dark:border-gray-600 bg-white dark:bg-gray-700 text-gray-900 dark:text-white rounded-lg focus:ring-2 focus:ring-primary focus:border-transparent"
            >
              <option value="all">All Models</option>
              <option value="dima806">Dima806 Deepfake Detector</option>
              <option value="deep fake detector v2">Deep Fake Detector v2</option>
              <option value="open deepfake">Open Deepfake Detection</option>
            </select>
          </div>
        </div>
      </div>

      {/* History Table */}
      <div className="bg-white rounded-xl shadow-md border border-gray-200 overflow-hidden">
        {currentItems.length === 0 ? (
          <div className="p-12 text-center">
            <Filter className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <p className="text-gray-500 text-lg">No detections found</p>
          </div>
        ) : (
          <>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead className="bg-gray-50 border-b border-gray-200">
                  <tr>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Type
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Date & Time
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Result
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Confidence
                    </th>
                    <th className="px-6 py-4 text-left text-xs font-semibold text-gray-600 uppercase tracking-wider">
                      Model
                    </th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-gray-200">
                  {currentItems.map((item) => (
                    <tr key={item.id} className="hover:bg-gray-50 transition">
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center space-x-3">
                          <div className="text-gray-600">{getTypeIcon(item.detection_type)}</div>
                          <span className="font-medium text-gray-900 capitalize">
                            {item.detection_type}
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {formatDate(item.detection_time)}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        {item.is_fake ? (
                          <div className="flex items-center space-x-2 px-3 py-1 bg-red-100 text-red-700 rounded-full w-fit">
                            <XCircle className="w-4 h-4" />
                            <span className="text-sm font-semibold">Fake</span>
                          </div>
                        ) : (
                          <div className="flex items-center space-x-2 px-3 py-1 bg-green-100 text-green-700 rounded-full w-fit">
                            <CheckCircle className="w-4 h-4" />
                            <span className="text-sm font-semibold">Real</span>
                          </div>
                        )}
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap">
                        <div className="flex items-center space-x-2">
                          <div className="w-24 bg-gray-200 rounded-full h-2">
                            <div
                              className={`h-full rounded-full ${
                                item.is_fake ? 'bg-red-500' : 'bg-green-500'
                              }`}
                              style={{ width: `${item.confidence_score}%` }}
                            ></div>
                          </div>
                          <span className="text-sm font-semibold text-gray-700">
                            {item.confidence_score.toFixed(1)}%
                          </span>
                        </div>
                      </td>
                      <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-600">
                        {item.model_version || 'N/A'}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>

            {/* Pagination */}
            {totalPages > 1 && (
              <div className="px-6 py-4 bg-gray-50 border-t border-gray-200 flex items-center justify-between">
                <div className="text-sm text-gray-600">
                  Showing {indexOfFirstItem + 1} to{' '}
                  {Math.min(indexOfLastItem, filteredHistory.length)} of{' '}
                  {filteredHistory.length} results
                </div>
                <div className="flex space-x-2">
                  <button
                    onClick={() => setCurrentPage((prev) => Math.max(prev - 1, 1))}
                    disabled={currentPage === 1}
                    className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Previous
                  </button>
                  <button
                    onClick={() => setCurrentPage((prev) => Math.min(prev + 1, totalPages))}
                    disabled={currentPage === totalPages}
                    className="px-4 py-2 border border-gray-300 rounded-lg text-sm font-medium text-gray-700 hover:bg-gray-100 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    Next
                  </button>
                </div>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

export default HistoryList;
