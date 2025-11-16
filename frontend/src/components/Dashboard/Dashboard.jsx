import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Camera, Image, Video, Activity, CheckCircle, XCircle, Target, Sparkles, TrendingUp } from 'lucide-react';
import StatsCard from './StatsCard';
import RecentHistory from './RecentHistory';
import { statsAPI, historyAPI } from '../../services/api';
import { auth } from '../../utils/auth';

const Dashboard = () => {
  const navigate = useNavigate();
  const [user, setUser] = useState(null);
  const [stats, setStats] = useState({
    total_detections: 0,
    fake_count: 0,
    real_count: 0,
    accuracy: 0,
  });
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Get user from localStorage
    const currentUser = auth.getUser();
    setUser(currentUser);
    
    // Small delay to ensure token is available after navigation
    const timer = setTimeout(() => {
      fetchData();
    }, 200);
    
    return () => clearTimeout(timer);
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
      // If authentication error, the interceptor will handle redirect
      if (error.response?.status === 401) {
        console.error('Authentication failed - token may be invalid or expired');
      }
    } finally {
      setLoading(false);
    }
  };

  const quickActions = [
    {
      title: 'Camera Detection',
      description: 'Real-time analysis',
      icon: Camera,
      gradient: 'from-blue-500 to-blue-600',
      path: '/camera',
    },
    {
      title: 'Upload Image',
      description: 'Analyze single image',
      icon: Image,
      gradient: 'from-green-500 to-emerald-600',
      path: '/upload/image',
    },
    {
      title: 'Upload Video',
      description: 'Analyze video file',
      icon: Video,
      gradient: 'from-purple-500 to-purple-600',
      path: '/upload/video',
    },
  ];

  if (loading) {
    return (
      <div className="flex items-center justify-center h-screen">
        <div className="relative">
          <div className="animate-spin rounded-full h-16 w-16 border-4 border-primary-200"></div>
          <div className="animate-spin rounded-full h-16 w-16 border-t-4 border-primary-600 absolute top-0"></div>
        </div>
      </div>
    );
  }

  return (
    <div className="space-y-8 animate-fade-in">
      {/* Welcome Section */}
      <div className="relative overflow-hidden bg-gradient-to-br from-primary-600 via-primary-700 to-primary-800 rounded-2xl shadow-xl p-8 text-white">
        <div className="absolute top-0 right-0 -mt-4 -mr-4 w-40 h-40 bg-white opacity-5 rounded-full blur-3xl"></div>
        <div className="absolute bottom-0 left-0 -mb-4 -ml-4 w-40 h-40 bg-white opacity-5 rounded-full blur-3xl"></div>
        <div className="relative z-10">
          <div className="flex items-center space-x-2 mb-3">
            <Sparkles className="w-6 h-6 text-yellow-300 animate-pulse" />
            <span className="text-sm font-medium text-primary-100">AI-Powered Detection</span>
          </div>
          <h1 className="text-4xl font-bold mb-2">Welcome back, {user?.username || 'User'}! 👋</h1>
          <p className="text-primary-100 text-lg">Monitor and analyze media for deepfake detection with advanced AI</p>
        </div>
      </div>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatsCard
          title="Total Detections"
          value={stats.total_detections}
          icon={Activity}
          color="blue"
          trend="+12%"
        />
        <StatsCard
          title="Fake Detected"
          value={stats.fake_count}
          icon={XCircle}
          color="red"
          trend="-5%"
        />
        <StatsCard
          title="Real Content"
          value={stats.real_count}
          icon={CheckCircle}
          color="green"
          trend="+8%"
        />
        <StatsCard
          title="Avg Confidence"
          value={`${stats.accuracy.toFixed(1)}%`}
          icon={Target}
          color="purple"
          trend="+2%"
        />
      </div>

      {/* Quick Actions */}
      <div>
        <div className="flex items-center justify-between mb-6">
          <h2 className="text-2xl font-bold text-gray-900 dark:text-white">Quick Actions</h2>
          <TrendingUp className="w-5 h-5 text-gray-400" />
        </div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {quickActions.map((action) => (
            <button
              key={action.path}
              onClick={() => navigate(action.path)}
              className="group relative bg-white dark:bg-gray-800 rounded-2xl shadow-sm hover:shadow-xl transition-all duration-300 p-6 border border-gray-200 dark:border-gray-700 text-left overflow-hidden hover:-translate-y-1"
            >
              <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${action.gradient} opacity-10 rounded-full -mr-16 -mt-16 group-hover:scale-150 transition-transform duration-500`}></div>
              <div className={`relative bg-gradient-to-br ${action.gradient} w-14 h-14 rounded-xl flex items-center justify-center mb-4 shadow-lg group-hover:scale-110 group-hover:rotate-3 transition-all duration-300`}>
                <action.icon className="w-7 h-7 text-white" />
              </div>
              <h3 className="relative text-lg font-bold text-gray-900 dark:text-white mb-1">{action.title}</h3>
              <p className="relative text-gray-600 dark:text-gray-400 text-sm">{action.description}</p>
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
