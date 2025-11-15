import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Image, Video, Activity, CheckCircle, XCircle, Target } from 'lucide-react';
import StatsCard from './StatsCard';
import RecentHistory from './RecentHistory';
import { statsAPI, historyAPI } from '../../services/api';
import { auth } from '../../utils/auth';

const Dashboard = () => {
  const navigate = useNavigate();
  const user = auth.getUser();
  const [stats, setStats] = useState({
    total_detections: 0,
    fake_count: 0,
    real_count: 0,
    accuracy: 0,
  });
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [statsResponse, historyResponse] = await Promise.all([
        statsAPI.getStats(),
        historyAPI.getAll(),
      ]);

      if (statsResponse.success) {
        setStats(statsResponse);
      }

      if (historyResponse.success) {
        setHistory(historyResponse.history);
      }
    } catch (error) {
      console.error('Failed to fetch dashboard data:', error);
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    {
      title: 'Camera Detection',
      description: 'Start live detection',
      icon: Camera,
      color: 'bg-blue-500',
      path: '/camera',
    },
    {
      title: 'Upload Image',
      description: 'Analyze an image',
      icon: Image,
      color: 'bg-green-500',
      path: '/upload/image',
    },
    {
      title: 'Upload Video',
      description: 'Analyze a video',
      icon: Video,
      color: 'bg-purple-500',
      path: '/upload/video',
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary"></div>
      </div>
    );
  }

  return (
    <div className="p-6 space-y-6">
      {/* Welcome Section */}
      <div className="bg-gradient-to-r from-blue-500 to-indigo-600 rounded-xl shadow-lg p-8 text-white">
        <h1 className="text-3xl font-bold mb-2">Welcome back, {user?.username}! 👋</h1>
        <p className="text-blue-100">Monitor and analyze media for deepfake detection</p>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Detections"
          value={stats.total_detections}
          icon={Activity}
          color="blue"
        />
        <StatsCard
          title="Fake Detected"
          value={stats.fake_count}
          icon={XCircle}
          color="red"
        />
        <StatsCard
          title="Real Content"
          value={stats.real_count}
          icon={CheckCircle}
          color="green"
        />
        <StatsCard
          title="Avg Confidence"
          value={`${stats.accuracy.toFixed(1)}%`}
          icon={Target}
          color="purple"
        />
      </div>

      {/* Quick Actions */}
      <div>
        <h2 className="text-2xl font-bold text-gray-900 mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action) => (
            <button
              key={action.path}
              onClick={() => navigate(action.path)}
              className="bg-white rounded-xl shadow-md p-6 border border-gray-200 hover:shadow-lg transition text-left group"
            >
              <div className={`${action.color} w-12 h-12 rounded-lg flex items-center justify-center mb-4 group-hover:scale-110 transition`}>
                <action.icon className="w-6 h-6 text-white" />
              </div>
              <h3 className="text-lg font-bold text-gray-900 mb-1">{action.title}</h3>
              <p className="text-gray-600 text-sm">{action.description}</p>
            </button>
          ))}
        </div>
      </div>

      {/* Recent History */}
      <RecentHistory history={history} />
    </div>
  );
};

export default Dashboard;
