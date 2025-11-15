# Frontend Documentation - Deepfake Detection System

React application with modern UI for deepfake detection.

## 📋 Overview

The frontend provides:
- User authentication (login/signup)
- Image and video upload
- Real-time camera detection
- Detection history and statistics
- Responsive design with dark mode

## � Setup

### 1. Install Dependencies
```bash
cd frontend
npm install
```

**Dependencies:**
- React 18 - UI library
- React Router - Navigation
- Axios - HTTP client
- Tailwind CSS - Styling
- Lucide React - Icons
- react-webcam - Camera access

**Time:** 2-3 minutes

### 2. Configure Environment
Create `.env` file:
```
VITE_API_URL=http://localhost:5000/api
```

### 3. Start Development Server
```bash
npm run dev
```
Application runs at: `http://localhost:5173`

## 📁 File Structure

```
frontend/src/
├── components/
│   ├── Auth/
│   │   ├── Login.jsx           # Login form
│   │   └── Signup.jsx          # Registration form
│   ├── Dashboard/
│   │   ├── Dashboard.jsx       # Main dashboard
│   │   ├── StatsCard.jsx       # Statistics card
│   │   └── RecentHistory.jsx   # Recent detections
│   ├── Camera/
│   │   └── CameraDetection.jsx # Webcam detection
│   ├── Upload/
│   │   ├── ImageUpload.jsx     # Image upload
│   │   ├── VideoUpload.jsx     # Video upload
│   │   └── ResultDisplay.jsx   # Detection results
│   ├── History/
│   │   └── HistoryList.jsx     # Detection history
│   └── Layout/
│       ├── MainLayout.jsx      # Layout wrapper
│       ├── Navbar.jsx          # Top navigation
│       └── Sidebar.jsx         # Side navigation
├── services/
│   └── api.js                  # Axios API service
├── utils/
│   └── auth.js                 # Auth helpers
├── App.jsx                     # Main app with routing
├── main.jsx                    # React entry point
└── index.css                   # Tailwind styles
```

## 🎨 Components

### Authentication

#### Login.jsx
- Email/password form
- JWT token storage
- Redirect to dashboard on success
- Error handling

#### Signup.jsx
- Username, email, password form
- Validation
- Auto-login after registration

### Dashboard

#### Dashboard.jsx
- Welcome message
- Statistics cards (4 metrics)
- Recent detections (last 5)
- Quick action buttons

#### StatsCard.jsx
- Reusable stat display
- Icon, label, value
- Color variants (blue, green, red, purple)

#### RecentHistory.jsx
- Table of recent detections
- Type, result, confidence, date
- Link to full history

### Upload

#### ImageUpload.jsx
- Drag & drop zone
- File selector
- Image preview
- Upload progress
- Result display

#### VideoUpload.jsx
- File selector
- Video preview player
- Upload progress
- Processing indicator
- Result display

#### ResultDisplay.jsx
- Verdict badge (Real/Fake)
- Confidence percentage
- Progress bar
- Timestamp
- Action buttons

### Camera

#### CameraDetection.jsx
- Webcam preview (640x480)
- Start/Stop detection
- Auto-capture every 2 seconds
- Result overlay
- Session counter
- Save detection

### History

#### HistoryList.jsx
- Filterable table
- Search by date
- Filter by type (image/video/camera)
- Filter by result (fake/real)
- Pagination (10 per page)
- View details modal

### Layout

#### MainLayout.jsx
- Wrapper for protected pages
- Navbar + Sidebar + Content
- Dark mode state management

#### Navbar.jsx
- User info display
- Dark mode toggle
- Logout button

#### Sidebar.jsx
- Navigation links
- Active route highlighting
- Icons for each page

## 🔌 API Service

### api.js

**Axios Instance:**
```javascript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' }
});
```

**Request Interceptor:**
```javascript
// Adds JWT token to all requests
api.interceptors.request.use(config => {
  const token = getToken();
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});
```

**Response Interceptor:**
```javascript
// Handles 401 errors (expired token)
api.interceptors.response.use(
  response => response,
  error => {
    if (error.response?.status === 401) {
      logout();
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);
```

**API Methods:**
```javascript
// Authentication
auth.register(username, email, password)
auth.login(username, password)
auth.getMe()

// Detection
detection.detectImage(imageFile)
detection.detectVideo(videoFile)
detection.detectCamera(base64Image)

// History
history.getAll()
stats.getStats()
```

## 🔐 Authentication

### auth.js Utilities

```javascript
// Token management
saveToken(token)        // Store JWT in localStorage
getToken()              // Retrieve JWT
removeToken()           // Clear JWT

// User management
saveUser(user)          // Store user data
getCurrentUser()        // Get user data
isAuthenticated()       // Check if logged in
logout()                // Clear all auth data
```

### Protected Routes

```javascript
// ProtectedRoute.jsx
const ProtectedRoute = ({ children }) => {
  if (!isAuthenticated()) {
    return <Navigate to="/login" replace />;
  }
  return children;
};
```

## 🎨 Styling

### Tailwind CSS

**Color Scheme:**
- Primary: Blue (#3B82F6)
- Success/Real: Green (#10B981)
- Danger/Fake: Red (#EF4444)
- Background: Gray (#F9FAFB light, #1F2937 dark)

**Dark Mode:**
```javascript
// Toggle dark mode
const [darkMode, setDarkMode] = useState(false);

useEffect(() => {
  if (darkMode) {
    document.documentElement.classList.add('dark');
  } else {
    document.documentElement.classList.remove('dark');
  }
}, [darkMode]);
```

**Responsive Design:**
```jsx
// Mobile-first approach
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
  {/* Cards */}
</div>
```

## 🛣 Routing

### App.jsx Routes

```javascript
<Routes>
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

  {/* Default redirect */}
  <Route path="/" element={<Navigate to="/dashboard" />} />
</Routes>
```

## 🎥 Camera Detection

### react-webcam Usage

```javascript
import Webcam from 'react-webcam';

const webcamRef = useRef(null);

// Capture frame
const captureFrame = () => {
  const imageSrc = webcamRef.current.getScreenshot();
  // imageSrc is base64 encoded
  return imageSrc;
};

// Render webcam
<Webcam
  ref={webcamRef}
  screenshotFormat="image/jpeg"
  width={640}
  height={480}
/>
```

### Auto-Detection

```javascript
useEffect(() => {
  if (isDetecting) {
    const interval = setInterval(() => {
      const frame = captureFrame();
      detectFrame(frame);
    }, 2000); // Every 2 seconds

    return () => clearInterval(interval);
  }
}, [isDetecting]);
```

## 📊 State Management

### React Hooks Used

**useState:**
```javascript
const [loading, setLoading] = useState(false);
const [error, setError] = useState(null);
const [data, setData] = useState([]);
```

**useEffect:**
```javascript
useEffect(() => {
  fetchData();
}, []); // Run once on mount
```

**useNavigate:**
```javascript
const navigate = useNavigate();
navigate('/dashboard');
```

**useRef:**
```javascript
const webcamRef = useRef(null);
const fileInputRef = useRef(null);
```

## 🔄 Data Flow

### Upload Flow
1. User selects file
2. File validated (type, size)
3. Preview displayed
4. User clicks "Analyze"
5. File sent to API (FormData)
6. Loading state shown
7. Result received
8. Result displayed

### Detection Flow
1. API call with axios
2. Loading state set to true
3. Request sent with JWT token
4. Response received
5. Loading state set to false
6. Success: Display result
7. Error: Show error message

## 🐛 Error Handling

### Try-Catch Pattern
```javascript
const handleUpload = async () => {
  try {
    setLoading(true);
    setError(null);
    
    const result = await api.detection.detectImage(file);
    
    setResult(result.data);
  } catch (err) {
    setError(err.response?.data?.message || 'Upload failed');
  } finally {
    setLoading(false);
  }
};
```

### Error Display
```jsx
{error && (
  <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded">
    {error}
  </div>
)}
```

## 🎓 FYP Defense Points

**React Concepts:**
- Functional components with hooks
- Component composition
- Props and state management
- Lifecycle with useEffect
- Refs for DOM access

**Routing:**
- Client-side routing (React Router)
- Protected routes
- Nested routes with layout
- Programmatic navigation

**API Integration:**
- Axios for HTTP requests
- Interceptors for auth
- Error handling
- Loading states

**UI/UX:**
- Responsive design (mobile-first)
- Dark mode support
- Loading indicators
- Error messages
- Form validation

**Security:**
- JWT token storage
- Protected routes
- Token expiration handling
- Secure file upload

**Performance:**
- Component memoization possible
- Lazy loading routes possible
- Image optimization
- Code splitting with Vite

## 🛠 Build & Deploy

### Development
```bash
npm run dev
```

### Production Build
```bash
npm run build
```
Output: `dist/` folder

### Preview Production Build
```bash
npm run preview
```

## 📝 Key Files Explained

### main.jsx
- React entry point
- Renders App component
- Imports global styles

### App.jsx
- Main application component
- Defines all routes
- Handles authentication flow

### index.css
- Tailwind directives
- Global styles
- Custom CSS if needed

### vite.config.ts
- Vite configuration
- Build settings
- Plugin configuration

## 🎨 Customization

### Change Colors
Edit `tailwind.config.js`:
```javascript
theme: {
  extend: {
    colors: {
      primary: '#3B82F6',
      success: '#10B981',
      danger: '#EF4444'
    }
  }
}
```

### Add New Page
1. Create component in `components/`
2. Add route in `App.jsx`
3. Add navigation link in `Sidebar.jsx`

### Modify API URL
Edit `.env`:
```
VITE_API_URL=https://your-api-url.com/api
```

---

**For backend documentation, see:** `backend/README.md`
