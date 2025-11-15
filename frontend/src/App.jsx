import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
// import { isAuthenticated } from './utils/auth';  // Temporarily disabled

// Auth Components - Temporarily hidden
// import Login from './components/Auth/Login';
// import Signup from './components/Auth/Signup';

// Layout Components
import MainLayout from './components/Layout/MainLayout';

// Dashboard Components
import Dashboard from './components/Dashboard/Dashboard';

// Upload Components
import ImageUpload from './components/Upload/ImageUpload';
import VideoUpload from './components/Upload/VideoUpload';

// Camera Component
import CameraDetection from './components/Camera/CameraDetection';

// History Component
import HistoryList from './components/History/HistoryList';

// AUTHENTICATION TEMPORARILY DISABLED FOR TESTING
// All routes are now accessible without login

function App() {
  return (
    <Router>
      <Routes>
        {/* Root - Redirect to dashboard */}
        <Route path="/" element={<Navigate to="/dashboard" replace />} />

        {/* All Routes with Layout - No authentication required */}
        <Route element={<MainLayout />}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/camera" element={<CameraDetection />} />
          <Route path="/upload/image" element={<ImageUpload />} />
          <Route path="/upload/video" element={<VideoUpload />} />
          <Route path="/history" element={<HistoryList />} />
        </Route>

        {/* 404 - Catch all */}
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
