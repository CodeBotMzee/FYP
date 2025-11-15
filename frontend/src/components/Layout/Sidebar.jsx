import React from 'react';
import { NavLink } from 'react-router-dom';
import { LayoutDashboard, Camera, Upload, History, Image, Video } from 'lucide-react';

/**
 * Sidebar Component
 * Side navigation menu with links to all pages
 */
const Sidebar = () => {
  const navItems = [
    { path: '/dashboard', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/camera', icon: Camera, label: 'Camera Detection' },
    { path: '/upload/image', icon: Image, label: 'Upload Image' },
    { path: '/upload/video', icon: Video, label: 'Upload Video' },
    { path: '/history', icon: History, label: 'History' }
  ];

  return (
    <aside className="w-64 bg-white dark:bg-gray-800 shadow-md border-r border-gray-200 dark:border-gray-700 min-h-screen">
      <nav className="p-4 space-y-2">
        {navItems.map((item) => (
          <NavLink
            key={item.path}
            to={item.path}
            className={({ isActive }) =>
              `flex items-center space-x-3 px-4 py-3 rounded-lg transition-colors ${
                isActive
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-700 dark:text-gray-300 hover:bg-gray-100 dark:hover:bg-gray-700'
              }`
            }
          >
            <item.icon size={20} />
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;
