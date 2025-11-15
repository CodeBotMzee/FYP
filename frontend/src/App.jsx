import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { isAuthenticated } from './utils/auth';

// Auth Components
import Login from './components/Auth/Login';
import Signup from './components/Auth/Signup';

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

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

// Public Route Component (redirect if already logged in)
const PublicRoute = ({ children }) => {
  if (isAuthenticated()) {
    return <Navigate to="/dashboard" replace />;
  }
  
  return children;
};

function App() {
  return (
    <Router>
      <Routes>
        {/* Root - Redirect based on auth status */}
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

        {/* Public Routes */}
        <Route
          path="/login"
          element={
            <PublicRoute>
              <Login />
            </PublicRoute>
          }
        />
        <Route
          path="/signup"
          element={
            <PublicRoute>
              <Signup />
            </PublicRoute>
          }
        />

        {/* Protected Routes with Layout */}
        <Route
          element={
            <ProtectedRoute>
              <MainLayout />
            </ProtectedRoute>
          }
        >
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
