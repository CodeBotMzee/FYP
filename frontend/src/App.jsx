import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { isAuthenticated } from './utils/auth';

// Auth Components
import Login from './components/Auth/Login';
import Signup from './components/Auth/Signup';

// Layout Components
import MainLayout from './components/Layout/MainLayout';
import ProtectedRoute from './components/ProtectedRoute';

// Dashboard Components
import Dashboard from './components/Dashboard/Dashboard';

// Upload Components
import ImageUpload from './components/Upload/ImageUpload';
import VideoUpload from './components/Upload/VideoUpload';

// Camera Component
import CameraDetection from './components/Camera/CameraDetection';

// History Component
import HistoryList from './components/History/HistoryList';

function App() {
  return (
    <Router>
      <Routes>
        {/* Root - Redirect based on authentication */}
        <Route 
          path="/" 
          element={
            isAuthenticated() ? (
              <Navigate to="/dashboard" replace />
            ) : (
              <Navigate to="/login" replace />
            )
          } 
        />

        {/* Public routes */}
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />

        {/* Protected routes with layout */}
        <Route element={<ProtectedRoute><MainLayout /></ProtectedRoute>}>
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/camera" element={<CameraDetection />} />
          <Route path="/upload/image" element={<ImageUpload />} />
          <Route path="/upload/video" element={<VideoUpload />} />
          <Route path="/history" element={<HistoryList />} />
        </Route>

        {/* 404 - Catch all */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </Router>
  );
}

export default App;
