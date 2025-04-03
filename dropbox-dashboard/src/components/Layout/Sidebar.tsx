// src/components/Layout/Sidebar.tsx
import React from 'react';
import { Link, useParams } from 'react-router-dom';

// Define dropbox data
const dropboxes = [
  { id: 1, name: 'Alpha', location: 'Main Entrance', status: 'active', newItems: 2 },
  { id: 2, name: 'Beta', location: 'Secondary Location', status: 'active', newItems: 1 },
  { id: 3, name: 'Gamma', location: 'Remote Access', status: 'inactive', newItems: 0 }
];

// Define navigation items
const navItems = [
  { id: 'overview', name: 'Overview', icon: 'chart-pie' },
  { id: 'activity', name: 'Activity Log', icon: 'clock' },
  { id: 'security', name: 'Security', icon: 'shield-check' },
  { id: 'settings', name: 'Settings', icon: 'cog' }
];

const Sidebar: React.FC = () => {
  const { dropboxId } = useParams<{ dropboxId: string }>();
  const currentId = Number(dropboxId);
  
  return (
    <div className="h-screen w-64 bg-gray-900 border-r border-gray-800 flex flex-col">
      {/* Logo and Brand - optional if already in navbar */}
      <div className="p-4 border-b border-gray-800">
        <h2 className="text-xl font-bold text-white">DropTrack</h2>
        <p className="text-xs text-gray-400">Monitoring System</p>
      </div>
      
      {/* Dropboxes Section */}
      <div className="p-4">
        <div className="flex items-center justify-between mb-4">
          <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider">Dropboxes</h3>
          <button className="p-1 rounded-md text-gray-400 hover:text-blue-400 transition-colors">
            <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
            </svg>
          </button>
        </div>
        
        <div className="space-y-1">
          {dropboxes.map((box) => (
            <Link
              key={box.id}
              to={`/dashboard/${box.id}`}
              className={`flex items-center px-3 py-2 rounded-lg transition-all duration-200 group ${
                currentId === box.id
                  ? 'bg-blue-600 text-white'
                  : 'text-gray-300 hover:bg-gray-800'
              }`}
            >
              <div className={`w-2 h-2 rounded-full mr-3 ${
                box.status === 'active' 
                  ? 'bg-green-400 animate-pulse' 
                  : 'bg-gray-500'
              }`}></div>
              <div className="flex-1">
                <div className="flex items-center justify-between">
                  <span className="font-medium">Box {box.name}</span>
                  {box.newItems > 0 && (
                    <span className={`px-1.5 py-0.5 rounded-full text-xs font-bold ${
                      currentId === box.id ? 'bg-white/20' : 'bg-blue-500/20 text-blue-400'
                    }`}>
                      {box.newItems}
                    </span>
                  )}
                </div>
                <p className="text-xs opacity-70">{box.location}</p>
              </div>
            </Link>
          ))}
        </div>
      </div>
      
      {/* Navigation Section */}
      <div className="p-4 mt-4">
        <h3 className="text-sm font-bold text-gray-400 uppercase tracking-wider mb-4">Navigation</h3>
        <div className="space-y-1">
          {navItems.map((item) => (
            <Link
              key={item.id}
              to={`/dashboard/${dropboxId || 1}/${item.id}`}
              className="flex items-center px-3 py-2 text-gray-300 rounded-lg hover:bg-gray-800 transition-colors group"
            >
              <IconForNav name={item.icon} />
              <span className="ml-3">{item.name}</span>
              
              {/* Subtle accent line on hover */}
              <span className="ml-auto w-0 group-hover:w-5 h-0.5 bg-blue-500 transition-all duration-300 opacity-0 group-hover:opacity-100"></span>
            </Link>
          ))}
        </div>
      </div>
      
      {/* System Status */}
      <div className="mt-auto p-4 border-t border-gray-800">
        <div className="bg-gray-800 rounded-lg p-3">
          <div className="flex items-center mb-2">
            <div className="w-2 h-2 rounded-full bg-green-400 mr-2"></div>
            <span className="text-sm text-gray-300">All Systems Operational</span>
          </div>
          <div className="flex items-center justify-between text-xs">
            <span className="text-gray-500">Last update: 5m ago</span>
            <Link to="/status" className="text-blue-400 hover:text-blue-300">Details</Link>
          </div>
        </div>
      </div>
    </div>
  );
};

// Helper component for navigation icons
const IconForNav: React.FC<{ name: string }> = ({ name }) => {
  switch (name) {
    case 'chart-pie':
      return (
        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 3.055A9.001 9.001 0 1020.945 13H11V3.055z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M20.488 9H15V3.512A9.025 9.025 0 0120.488 9z" />
        </svg>
      );
    case 'clock':
      return (
        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
        </svg>
      );
    case 'shield-check':
      return (
        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
        </svg>
      );
    case 'cog':
      return (
        <svg className="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
        </svg>
      );
    default:
      return null;
  }
};

export default Sidebar;