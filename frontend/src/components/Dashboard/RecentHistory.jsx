import { CheckCircle, XCircle, Image, Video, Camera } from 'lucide-react';

const RecentHistory = ({ history }) => {
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

  return (
    <div className="bg-white rounded-xl shadow-md p-6 border border-gray-200">
      <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Detections</h2>
      
      {history.length === 0 ? (
        <p className="text-gray-500 text-center py-8">No detections yet</p>
      ) : (
        <div className="space-y-3">
          {history.slice(0, 5).map((item) => (
            <div
              key={item.id}
              className="flex items-center justify-between p-4 bg-gray-50 rounded-lg hover:bg-gray-100 transition"
            >
              <div className="flex items-center space-x-4">
                <div className="text-gray-600">
                  {getTypeIcon(item.detection_type)}
                </div>
                <div>
                  <p className="font-medium text-gray-900 capitalize">
                    {item.detection_type} Detection
                  </p>
                  <p className="text-sm text-gray-500">{formatDate(item.detection_time)}</p>
                </div>
              </div>
              
              <div className="flex items-center space-x-3">
                <span className="text-sm font-semibold text-gray-700">
                  {item.confidence_score.toFixed(1)}%
                </span>
                {item.is_fake ? (
                  <div className="flex items-center space-x-1 px-3 py-1 bg-red-100 text-red-700 rounded-full">
                    <XCircle className="w-4 h-4" />
                    <span className="text-sm font-semibold">Fake</span>
                  </div>
                ) : (
                  <div className="flex items-center space-x-1 px-3 py-1 bg-green-100 text-green-700 rounded-full">
                    <CheckCircle className="w-4 h-4" />
                    <span className="text-sm font-semibold">Real</span>
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
};

export default RecentHistory;
