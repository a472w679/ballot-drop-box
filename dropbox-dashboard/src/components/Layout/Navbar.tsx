// src/components/Layout/Navbar.tsx
import React, { useState, useEffect } from 'react';
import { Link, useLocation } from 'react-router-dom';

const Navbar: React.FC = () => {
  const [scrolled, setScrolled] = useState(false);
  const location = useLocation();

  // Handle scroll effect for transparent to solid background
  useEffect(() => {
    const handleScroll = () => {
      if (window.scrollY > 20) {
        setScrolled(true);
      } else {
        setScrolled(false);
      }
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  return (
    <nav 
      className={`fixed top-0 left-0 right-0 z-50 transition-all duration-300 ${
        scrolled ? 'bg-gray-900/90 backdrop-blur-md shadow-lg' : 'bg-transparent'
      }`}
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex justify-between items-center h-16 md:h-20">
          <div className="flex-shrink-0 flex items-center">
            <Link to="/" className="flex items-center group">
              <div className="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center transition-all group-hover:scale-110">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5 text-white" viewBox="0 0 20 20" fill="currentColor">
                  <path d="M3 3a1 1 0 00-1 1v12a1 1 0 001 1h14a1 1 0 001-1V4a1 1 0 00-1-1H3zm0 2h14v10H3V5z" />
                </svg>
              </div>
              <div className="ml-3 flex flex-col">
                <span className="text-lg font-bold text-white tracking-tight">DropTrack</span>
                <span className="text-xs text-blue-400 font-medium -mt-1">Monitoring System</span>
              </div>
            </Link>
          </div>
          
          <div className="hidden md:flex items-center space-x-6">
            <NavLink to="/" active={location.pathname === '/'}>Home</NavLink>
            <NavLink to="/dashboard/:dropboxId" active={location.pathname.includes('/dashboard')}>Dashboard</NavLink>


            
            {/* Notification bell */}
            <button className="relative p-2 text-white hover:text-blue-400 transition-colors">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 17h5l-1.405-1.405A2.032 2.032 0 0118 14.158V11a6.002 6.002 0 00-4-5.659V5a2 2 0 10-4 0v.341C7.67 6.165 6 8.388 6 11v3.159c0 .538-.214 1.055-.595 1.436L4 17h5m6 0v1a3 3 0 11-6 0v-1m6 0H9" />
              </svg>
              <span className="absolute top-1 right-1 h-2 w-2 rounded-full bg-blue-500"></span>
            </button>
            
            {/* User menu */}
            <div className="relative group">
              <button className="flex items-center space-x-2 p-1 rounded-full bg-gray-800 hover:bg-gray-700 transition-colors">
                <div className="h-8 w-8 rounded-full bg-blue-500 overflow-hidden flex items-center justify-center text-white font-medium">
                  <span>JD</span>
                </div>
              </button>
              <div className="absolute right-0 top-full mt-2 w-48 bg-gray-800 rounded-lg shadow-lg py-2 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-300 transform origin-top-right">
                <Link to="/profile" className="block px-4 py-2 text-sm text-gray-100 hover:bg-gray-700">Profile</Link>
                <Link to="/account" className="block px-4 py-2 text-sm text-gray-100 hover:bg-gray-700">Account Settings</Link>
                <div className="border-t border-gray-700 my-1"></div>
                <Link to="/logout" className="block px-4 py-2 text-sm text-red-400 hover:bg-gray-700">Logout</Link>
              </div>
            </div>
          </div>
          
          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button className="p-2 rounded-md text-white hover:text-blue-400 focus:outline-none">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 6h16M4 12h16M4 18h16" />
              </svg>
            </button>
          </div>
        </div>
      </div>
    </nav>
  );
};

// Navigation link component for consistent styling
const NavLink: React.FC<{ to: string; active: boolean; children: React.ReactNode }> = ({ 
  to, 
  active, 
  children 
}) => {
  return (
    <Link
      to={to}
      className={`relative px-1 py-2 text-sm font-medium transition-colors ${
        active ? 'text-blue-400' : 'text-white hover:text-blue-300'
      }`}
    >
      {children}
      <span className={`absolute left-0 right-0 bottom-0 h-0.5 bg-blue-500 transform origin-left transition-transform duration-300 ${
        active ? 'scale-x-100' : 'scale-x-0 group-hover:scale-x-100'
      }`}></span>
    </Link>
  );
};

export default Navbar;