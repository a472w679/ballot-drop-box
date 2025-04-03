import React, { useEffect, useState } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { motion } from 'framer-motion';
import Sidebar from '../components/Layout/Sidebar';
import EnvelopeTable from '../components/Dashboard/EnvelopeTable';
import LiveFeed from '../components/Dashboard/LiveFeed';
import { fetchDropboxData } from '../store/slices/dropboxSlice';
import { RootState } from '../store';
import './DashboardPage.css';

const DashboardPage: React.FC = () => {
  const { dropboxId } = useParams<{ dropboxId: string }>();
  const navigate = useNavigate();
  const dispatch = useDispatch();
  const { currentDropbox, loading, error } = useSelector((state: RootState) => state.dropbox);
  const [activeTab, setActiveTab] = useState<string>("overview");
  const [refreshing, setRefreshing] = useState<boolean>(false);
  
  // Animation variants
  const fadeIn = {
    hidden: { opacity: 0, y: 20 },
    visible: (i: number) => ({
      opacity: 1,
      y: 0,
      transition: {
        delay: 0.1 * i,
        duration: 0.7,
        ease: [0.6, 0.05, 0.01, 0.9],
      },
    }),
  };

  // Add particles background effect
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/particles.js/2.0.0/particles.min.js';
    script.async = true;
    document.body.appendChild(script);

    script.onload = () => {
      // @ts-ignore
      window.particlesJS('dashboard-particles-js', {
        particles: {
          number: { value: 40, density: { enable: true, value_area: 800 } },
          color: { value: '#3f83f8' },
          shape: { type: 'circle' },
          opacity: { value: 0.1, random: false },
          size: { value: 3, random: true },
          line_linked: { enable: true, distance: 150, color: '#3f83f8', opacity: 0.1, width: 1 },
          move: { enable: true, speed: 0.5, direction: 'none', random: true, straight: false, out_mode: 'out', bounce: false }
        },
        interactivity: {
          detect_on: 'canvas',
          events: { onhover: { enable: true, mode: 'grab' }, onclick: { enable: true, mode: 'push' } },
          modes: { grab: { distance: 140, line_linked: { opacity: 0.2 } }, push: { particles_nb: 2 } }
        }
      });
    };

    return () => {
      if (script.parentNode) {
        document.body.removeChild(script);
      }
    };
  }, []);
  
  useEffect(() => {
    if (dropboxId) {
      dispatch(fetchDropboxData(Number(dropboxId)) as any);
    }
  }, [dispatch, dropboxId]);
  
  const handleRefresh = async () => {
    if (!dropboxId) return;
    
    setRefreshing(true);
    try {
      await dispatch(fetchDropboxData(Number(dropboxId)) as any);
    } catch (err) {
      console.error("Error refreshing data:", err);
    } finally {
      setRefreshing(false);
    }
  };

  const handleNavigation = (id: number) => {
    navigate(`/dashboard/${id}`);
  };
  
  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white overflow-x-hidden flex">
        <Sidebar />
        <div className="flex-1 p-6 relative">
          <div id="dashboard-particles-js" className="absolute inset-0 z-0"></div>
          <div className="relative z-10 max-w-7xl mx-auto">
            <div className="h-10 w-1/3 mb-6 bg-blue-500/10 animate-pulse rounded-lg"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
              <div className="h-40 bg-blue-500/10 animate-pulse rounded-lg"></div>
              <div className="h-40 bg-blue-500/10 animate-pulse rounded-lg"></div>
            </div>
            <div className="h-64 mb-6 bg-blue-500/10 animate-pulse rounded-lg"></div>
            <div className="h-64 bg-blue-500/10 animate-pulse rounded-lg"></div>
          </div>
        </div>
      </div>
    );
  }
  
  if (error || !currentDropbox) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white overflow-x-hidden flex">
        <Sidebar />
        <div className="flex-1 p-6 relative">
          <div id="dashboard-particles-js" className="absolute inset-0 z-0"></div>
          <div className="relative z-10 max-w-7xl mx-auto">
            <motion.div 
              className="bg-gray-800/40 backdrop-blur-sm border border-red-500/30 rounded-2xl overflow-hidden"
              initial="hidden"
              animate="visible"
              variants={fadeIn}
              custom={0}
            >
              <div className="p-8 flex flex-col items-center justify-center text-center space-y-4">
                <div className="p-4 bg-red-500/20 rounded-full">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-red-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
                  </svg>
                </div>
                <h2 className="text-2xl font-bold text-red-100">Failed to Load Dropbox Data</h2>
                <p className="text-gray-400 max-w-lg">
                  {error || "There was an error loading the dropbox data. Please try again or contact support."}
                </p>
                <div className="flex flex-wrap gap-4 mt-4">
                  <button
                    onClick={() => navigate("/dashboard")}
                    className="px-6 py-3 bg-gray-800/40 hover:bg-gray-700/60 backdrop-blur-sm border border-white/10 rounded-xl font-medium transition-all duration-300"
                  >
                    Return to Dashboard
                  </button>
                  <button
                    onClick={() => window.location.reload()}
                    className="px-6 py-3 bg-gradient-to-r from-red-600 to-red-700 hover:from-red-500 hover:to-red-600 rounded-xl font-medium transition-all duration-300"
                  >
                    Try Again
                  </button>
                </div>
              </div>
            </motion.div>
          </div>
        </div>
      </div>
    );
  }
  
  const { envelopeData = [], mediaFiles = [] } = currentDropbox;
  // Use 'as any' to bypass TypeScript type checking for these properties
  const dropboxStatus = (currentDropbox as any).status || 'active';
  const lastUpdated = (currentDropbox as any).lastUpdated || new Date().toISOString();
  const pendingCount = envelopeData.filter(env => env.status === "pending").length;
  const processedCount = envelopeData.filter(env => env.status === "processed").length;
  const rejectedCount = envelopeData.filter(env => env.status === "rejected").length;
  
  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white overflow-x-hidden flex">
      <Sidebar />
      
      <div className="flex-1 p-6 relative">
        {/* Particles background */}
        <div id="dashboard-particles-js" className="absolute inset-0 z-0"></div>
        
        {/* Main Content */}
        <div className="relative z-10 max-w-7xl mx-auto">
          {/* Header */}
          <motion.div 
            className="mb-8 relative"
            initial="hidden"
            animate="visible"
            variants={fadeIn}
            custom={0}
          >
            <div className="absolute inset-0 bg-blue-600/10 blur-[60px] rounded-full -z-10"></div>
            <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
              <div>
                <div className="mb-2 inline-flex items-center p-1 pl-3 pr-2 bg-blue-900/30 rounded-full backdrop-blur-sm border border-blue-500/20">
                  <span className="text-blue-300 text-sm mr-2">Dropbox #{currentDropbox.id}</span>
                  <span className={`px-2 py-1 ${dropboxStatus === 'active' ? 'bg-green-500' : 'bg-gray-500'} rounded-full text-xs font-semibold`}>
                    {dropboxStatus === "active" ? "LIVE" : dropboxStatus.toUpperCase()}
                  </span>
                </div>
                <h1 className="text-3xl md:text-4xl font-bold leading-tight bg-clip-text text-transparent bg-gradient-to-r from-blue-300 via-blue-100 to-blue-400">
                  Dropbox Dashboard
                </h1>
                <p className="text-blue-100/80 mt-2">
                  Last updated: {new Date(lastUpdated).toLocaleString()}
                </p>
              </div>
              <div className="flex flex-wrap gap-3">
                <button 
                  onClick={handleRefresh} 
                  disabled={refreshing}
                  className="group relative px-6 py-3 bg-transparent hover:bg-white/10 rounded-xl font-medium border border-white/20 backdrop-blur-sm transition-all duration-300 flex items-center"
                >
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    className={`mr-2 h-5 w-5 ${refreshing ? 'animate-spin' : ''}`} 
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke="currentColor"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                  </svg>
                  {refreshing ? 'Refreshing...' : 'Refresh Data'}
                  <div className="absolute inset-0 opacity-0 group-hover:opacity-10 bg-gradient-to-r from-blue-400 to-purple-600 transition-opacity duration-300 z-0 rounded-xl"></div>
                </button>
                <button className="group relative px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-xl font-medium transition-all duration-300 shadow-lg shadow-blue-500/20 hover:shadow-blue-500/30 flex items-center overflow-hidden">
                  <span className="relative z-10">Add Envelope</span>
                  <svg 
                    xmlns="http://www.w3.org/2000/svg" 
                    className="ml-2 h-5 w-5 relative z-10" 
                    fill="none" 
                    viewBox="0 0 24 24" 
                    stroke="currentColor"
                  >
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                  </svg>
                  <div className="absolute inset-0 -translate-x-full group-hover:translate-x-0 bg-gradient-to-r from-blue-400 to-blue-600 transition-transform duration-500 ease-out z-0"></div>
                </button>
              </div>
            </div>
          </motion.div>
          
          {/* Stats Cards */}
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8"
            initial="hidden"
            animate="visible"
            variants={fadeIn}
            custom={1}
          >
            <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:bg-gray-800/60 transition-all duration-300 relative overflow-hidden group">
              {/* Animated border on hover */}
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <div className="absolute inset-0 rounded-2xl border border-blue-400/50"></div>
              </div>
              
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-blue-500/20 rounded-xl">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-blue-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 19v-8.93a2 2 0 01.89-1.664l7-4.666a2 2 0 012.22 0l7 4.666A2 2 0 0121 10.07V19" />
                  </svg>
                </div>
                <span className="text-sm text-gray-400">Total</span>
              </div>
              <h3 className="text-3xl font-bold mb-1">{envelopeData.length}</h3>
              <p className="text-gray-400 text-sm">Total envelopes</p>
              
              {/* Mini chart line */}
              <div className="mt-4 h-2 bg-gray-700/50 rounded-full overflow-hidden">
                <div className="h-full w-full bg-blue-500 rounded-full"></div>
              </div>
            </div>
            
            <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:bg-gray-800/60 transition-all duration-300 relative overflow-hidden group">
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <div className="absolute inset-0 rounded-2xl border border-green-400/50"></div>
              </div>
              
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-green-500/20 rounded-xl">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-green-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <span className="text-sm text-gray-400">Processed</span>
              </div>
              <h3 className="text-3xl font-bold mb-1">{processedCount}</h3>
              <p className="text-gray-400 text-sm">
                {envelopeData.length > 0 
                  ? `${Math.round((processedCount / envelopeData.length) * 100)}% of total`
                  : '0% of total'}
              </p>
              
              {/* Mini chart line */}
              <div className="mt-4 h-2 bg-gray-700/50 rounded-full overflow-hidden">
                <div className="h-full bg-green-500 rounded-full" style={{ 
                  width: envelopeData.length > 0 
                    ? `${(processedCount / envelopeData.length) * 100}%` 
                    : '0%' 
                }}></div>
              </div>
            </div>
            
            <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:bg-gray-800/60 transition-all duration-300 relative overflow-hidden group">
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <div className="absolute inset-0 rounded-2xl border border-yellow-400/50"></div>
              </div>
              
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-yellow-500/20 rounded-xl">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-yellow-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                </div>
                <span className="text-sm text-gray-400">Pending</span>
              </div>
              <h3 className="text-3xl font-bold mb-1">{pendingCount}</h3>
              <p className="text-gray-400 text-sm">Awaiting processing</p>
              
              {/* Mini chart line */}
              <div className="mt-4 h-2 bg-gray-700/50 rounded-full overflow-hidden">
                <div className="h-full bg-yellow-500 rounded-full" style={{ 
                  width: envelopeData.length > 0 
                    ? `${(pendingCount / envelopeData.length) * 100}%` 
                    : '0%' 
                }}></div>
              </div>
            </div>
            
            <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl p-6 hover:bg-gray-800/60 transition-all duration-300 relative overflow-hidden group">
              <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300">
                <div className="absolute inset-0 rounded-2xl border border-purple-400/50"></div>
              </div>
              
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-purple-500/20 rounded-xl">
                  <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-purple-400" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                  </svg>
                </div>
                <span className="text-sm text-gray-400">Media</span>
              </div>
              <h3 className="text-3xl font-bold mb-1">{mediaFiles.length}</h3>
              <p className="text-gray-400 text-sm">Media files captured</p>
              
              {/* Mini chart line */}
              <div className="mt-4 h-2 bg-gray-700/50 rounded-full overflow-hidden">
                <div className="h-full w-full bg-purple-500 rounded-full"></div>
              </div>
            </div>
          </motion.div>
          
          {/* Tabs Navigation */}
          <motion.div 
            className="mb-6 bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-xl p-1 flex overflow-x-auto hide-scrollbar"
            initial="hidden"
            animate="visible"
            variants={fadeIn}
            custom={2}
          >
            <button 
              onClick={() => setActiveTab("overview")}
              className={`flex-1 py-3 px-6 rounded-lg font-medium text-sm transition-all duration-300 ${
                activeTab === "overview" 
                  ? "bg-blue-600 text-white" 
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              Overview
            </button>
            <button 
              onClick={() => setActiveTab("envelopes")}
              className={`flex-1 py-3 px-6 rounded-lg font-medium text-sm transition-all duration-300 ${
                activeTab === "envelopes" 
                  ? "bg-blue-600 text-white" 
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              Envelopes
            </button>
            <button 
              onClick={() => setActiveTab("media")}
              className={`flex-1 py-3 px-6 rounded-lg font-medium text-sm transition-all duration-300 ${
                activeTab === "media" 
                  ? "bg-blue-600 text-white" 
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              Media Files
            </button>
            <button 
              onClick={() => setActiveTab("settings")}
              className={`flex-1 py-3 px-6 rounded-lg font-medium text-sm transition-all duration-300 ${
                activeTab === "settings" 
                  ? "bg-blue-600 text-white" 
                  : "text-gray-400 hover:text-white hover:bg-white/5"
              }`}
            >
              Settings
            </button>
          </motion.div>
          
          {/* Tab Content */}
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.3 }}
          >
            {activeTab === "overview" && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
                {/* Activity Chart */}
                <div className="md:col-span-2 bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden">
                  <div className="p-6 flex justify-between items-center">
                    <h2 className="text-xl font-bold">Activity Timeline</h2>
                    <div className="flex space-x-2">
                      <button className="p-2 bg-gray-700/50 rounded-lg hover:bg-gray-700/80 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
                        </svg>
                      </button>
                      <button className="p-2 bg-gray-700/50 rounded-lg hover:bg-gray-700/80 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13l-3 3m0 0l-3-3m3 3V8m0 13a9 9 0 110-18 9 9 0 010 18z" />
                        </svg>
                      </button>
                    </div>
                  </div>
                  <div className="px-6 pb-6">
                    <div className="h-64 relative bg-gray-900/50 rounded-lg overflow-hidden">
                      {/* Placeholder for chart - in a real app, use recharts or other charting library */}
                      <div className="absolute inset-0 p-4">
                        <div className="h-full flex items-end">
                          {Array(12).fill(0).map((_, i) => (
                            <div key={i} className="flex-1 flex flex-col items-center justify-end">
                              <div className="w-full max-w-[16px] mx-auto rounded-t-sm bg-blue-500/50"
                                style={{ 
                                  height: `${10 + Math.random() * 70}%`,
                                  opacity: i % 3 === 0 ? '1' : '0.6'
                                }}
                              >
                                <div className="h-1/3 w-full rounded-t-sm bg-blue-400/80"></div>
                              </div>
                              <div className="mt-2 text-xs text-gray-500">
                                {['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][i]}
                              </div>
                            </div>
                          ))}
                        </div>
                      </div>
                      
                      {/* Grid lines */}
                      <div className="absolute inset-0 grid grid-rows-4 grid-cols-1">
                        {Array(4).fill(0).map((_, i) => (
                          <div key={i} className="border-t border-white/5 relative">
                            <span className="absolute left-2 top-0 -translate-y-1/2 text-xs text-gray-500">
                              {100 - i * 25}
                            </span>
                          </div>
                        ))}
                      </div>
                      
                      {/* Gradient overlay */}
                      <div className="absolute inset-0 bg-gradient-to-t from-blue-500/5 to-transparent"></div>
                    </div>
                  </div>
                </div>
                
                {/* Recent Activity */}
                <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden">
                  <div className="p-6">
                    <h2 className="text-xl font-bold mb-4">Recent Activity</h2>
                    <div className="space-y-4">
                      {Array(5).fill(0).map((_, i) => (
                        <div key={i} className="flex items-start space-x-3">
                          <div className={`p-2 mt-1 rounded-lg ${
                            i % 3 === 0 ? 'bg-green-500/20' : 
                            i % 3 === 1 ? 'bg-blue-500/20' : 'bg-purple-500/20'
                          }`}>
                            <svg xmlns="http://www.w3.org/2000/svg" className={`h-4 w-4 ${
                              i % 3 === 0 ? 'text-green-400' : 
                              i % 3 === 1 ? 'text-blue-400' : 'text-purple-400'
                            }`} fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              {i % 3 === 0 ? (
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
                              ) : i % 3 === 1 ? (
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 19v-8.93a2 2 0 01.89-1.664l7-4.666a2 2 0 012.22 0l7 4.666A2 2 0 0121 10.07V19" />
                              ) : (
                                <>
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 9a2 2 0 012-2h.93a2 2 0 001.664-.89l.812-1.22A2 20 0110.07 4h3.86a2 2 0 011.664.89l.812 1.22A2 2 0 0016.07 7H17a2 2 0 012 2v9a2 2 0 01-2 2H5a2 2 0 01-2-2V9z" />
                                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M15 13a3 3 0 11-6 0 3 3 0 016 0z" />
                                </>
                              )}
                            </svg>
                          </div>
                          <div className="flex-1">
                            <p className="text-sm text-white mb-1">
                              {i % 3 === 0 ? 'Envelope processed successfully' : 
                               i % 3 === 1 ? 'New envelope added to system' : 
                               'New image captured'}
                            </p>
                            <div className="flex justify-between">
                              <span className="text-xs text-gray-500">
                                {`${5 - i} hour${i !== 4 ? 's' : ''} ago`}
                              </span>
                              <span className="text-xs text-blue-400 hover:text-blue-300 cursor-pointer">View</span>
                            </div>
                          </div>
                        </div>
                      ))}
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {activeTab === "envelopes" && (
              <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden">
                <div className="p-6">
                  <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-4 mb-6">
                    <div>
                      <h2 className="text-xl font-bold">Envelope Data</h2>
                      <p className="text-sm text-gray-400">{envelopeData.length} total records</p>
                    </div>
                    <div className="flex flex-col md:flex-row gap-3">
                      <div className="relative">
                        <input
                          type="text"
                          placeholder="Search envelopes..."
                          className="pl-9 pr-4 py-2 bg-gray-900/50 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-sm w-full"
                        />
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4 text-gray-400 absolute left-3 top-1/2 -translate-y-1/2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                        </svg>
                      </div>
                      <select className="px-3 py-2 bg-gray-900/50 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50 text-sm">
                        <option>All Status</option>
                        <option>Pending</option>
                        <option>Processed</option>
                        <option>Rejected</option>
                      </select>
                    </div>
                  </div>
                  
                  <div className="overflow-hidden rounded-lg border border-white/10">
                    <EnvelopeTable 
                      data={envelopeData} 
                      dropboxId={currentDropbox.id} 
                    />
                  </div>
                  
                  <div className="mt-4 flex flex-col md:flex-row justify-between items-center text-sm text-gray-400 gap-3">
                    <div>Showing 1 to {Math.min(10, envelopeData.length)} of {envelopeData.length} entries</div>
                    <div className="flex space-x-1">
                      <button className="px-3 py-1 bg-gray-900/50 rounded-md">Previous</button>
                      <button className="px-3 py-1 bg-blue-600 text-white rounded-md">1</button>
                      <button className="px-3 py-1 bg-gray-900/50 rounded-md">2</button>
                      <button className="px-3 py-1 bg-gray-900/50 rounded-md">3</button>
                      <button className="px-3 py-1 bg-gray-900/50 rounded-md">Next</button>
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {activeTab === "media" && (
              <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden">
                <div className="p-6">
                  <div className="flex flex-col md:flex-row md:justify-between md:items-center gap-4 mb-6">
                    <div>
                      <h2 className="text-xl font-bold">Media Files</h2>
                      <p className="text-sm text-gray-400">{mediaFiles.length} files captured</p>
                    </div>
                    <div className="flex space-x-2">
                      <button className="p-2 bg-gray-900/50 border border-white/10 rounded-lg hover:bg-gray-800 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                        </svg>
                      </button>
                      <button className="p-2 bg-gray-900/50 border border-white/10 rounded-lg hover:bg-gray-800 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4h13M3 8h9m-9 4h9m5-4v12m0 0l-4-4m4 4l4-4" />
                        </svg>
                      </button>
                      <button className="p-2 bg-gray-900/50 border border-white/10 rounded-lg hover:bg-gray-800 transition-colors">
                        <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M3 4a1 1 0 011-1h16a1 1 0 011 1v2.586a1 1 0 01-.293.707l-6.414 6.414a1 1 0 00-.293.707V17l-4 4v-6.586a1 1 0 00-.293-.707L3.293 7.293A1 1 0 013 6.586V4z" />
                        </svg>
                      </button>
                    </div>
                  </div>
                  
                  <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
                    {/* Replace with actual LiveFeed component implementation */}
                    {mediaFiles.length > 0 ? (
                      <LiveFeed 
                        dropboxId={currentDropbox.id} 
                        mediaFiles={mediaFiles} 
                      />
                    ) : (
                      Array(6).fill(0).map((_, i) => (
                        <div key={i} className="bg-gray-900/50 border border-white/10 rounded-lg p-3 aspect-video flex flex-col">
                          <div className="flex-1 bg-gray-800/50 rounded flex items-center justify-center">
                            <svg xmlns="http://www.w3.org/2000/svg" className="h-12 w-12 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                            </svg>
                          </div>
                          <div className="mt-2 flex justify-between items-center">
                            <div>
                              <h3 className="text-sm font-medium">Image {i + 1}</h3>
                              <p className="text-xs text-gray-500">Today, {new Date().toLocaleTimeString()}</p>
                            </div>
                            <button className="p-1.5 bg-gray-800/80 rounded-full">
                              <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M5 12h.01M12 12h.01M19 12h.01M6 12a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0zm7 0a1 1 0 11-2 0 1 1 0 012 0z" />
                              </svg>
                            </button>
                          </div>
                        </div>
                      ))
                    )}
                  </div>
                  
                  <div className="mt-6 flex justify-center">
                    <button className="px-6 py-3 bg-gray-900/50 border border-white/10 rounded-xl hover:bg-gray-800/80 transition-colors text-blue-400 flex items-center">
                      <svg xmlns="http://www.w3.org/2000/svg" className="mr-2 h-5 w-5" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12" />
                      </svg>
                      Load More Files
                    </button>
                  </div>
                </div>
              </div>
            )}
            
            {activeTab === "settings" && (
              <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
                <div className="lg:col-span-2 bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden">
                  <div className="p-6">
                    <h2 className="text-xl font-bold mb-6">Dropbox Settings</h2>
                    
                    <div className="space-y-6">
                      <div>
                        <label className="block text-sm font-medium text-gray-400 mb-2">Dropbox Name</label>
                        <input 
                          type="text" 
                          className="w-full px-4 py-3 bg-gray-900/50 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                          defaultValue={`Dropbox ${currentDropbox.id}`}
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-400 mb-2">Location</label>
                        <input 
                          type="text" 
                          className="w-full px-4 py-3 bg-gray-900/50 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50"
                          defaultValue="Main Entrance"
                        />
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-400 mb-2">Status</label>
                        <select className="w-full px-4 py-3 bg-gray-900/50 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50">
                          <option value="active" selected={dropboxStatus === "active"}>Active</option>
                          <option value="inactive" selected={dropboxStatus === "inactive"}>Inactive</option>
                          <option value="maintenance" selected={dropboxStatus === "maintenance"}>Maintenance</option>
                        </select>
                      </div>
                      
                      <div>
                        <label className="block text-sm font-medium text-gray-400 mb-2">Notification Settings</label>
                        <div className="space-y-3">
                          <div className="flex items-center justify-between py-3 px-4 bg-gray-900/30 rounded-lg">
                            <div>
                              <h3 className="font-medium">Email Notifications</h3>
                              <p className="text-sm text-gray-500">Receive email alerts for new envelopes</p>
                            </div>
                            <div className="relative inline-block w-12 h-6 rounded-full bg-gray-700">
                              <input type="checkbox" className="peer absolute w-0 h-0 opacity-0" defaultChecked />
                              <span className="absolute cursor-pointer inset-0 rounded-full bg-gray-700 peer-checked:bg-blue-600 transition-colors duration-300"></span>
                              <span className="absolute left-1 top-1 h-4 w-4 rounded-full bg-white peer-checked:left-7 transition-all duration-300"></span>
                            </div>
                          </div>
                          
                          <div className="flex items-center justify-between py-3 px-4 bg-gray-900/30 rounded-lg">
                            <div>
                              <h3 className="font-medium">SMS Alerts</h3>
                              <p className="text-sm text-gray-500">Receive text messages for critical events</p>
                            </div>
                            <div className="relative inline-block w-12 h-6 rounded-full bg-gray-700">
                              <input type="checkbox" className="peer absolute w-0 h-0 opacity-0" />
                              <span className="absolute cursor-pointer inset-0 rounded-full bg-gray-700 peer-checked:bg-blue-600 transition-colors duration-300"></span>
                              <span className="absolute left-1 top-1 h-4 w-4 rounded-full bg-white peer-checked:left-7 transition-all duration-300"></span>
                            </div>
                          </div>
                          
                          <div className="flex items-center justify-between py-3 px-4 bg-gray-900/30 rounded-lg">
                            <div>
                              <h3 className="font-medium">Automated Reports</h3>
                              <p className="text-sm text-gray-500">Receive weekly activity reports</p>
                            </div>
                            <div className="relative inline-block w-12 h-6 rounded-full bg-gray-700">
                              <input type="checkbox" className="peer absolute w-0 h-0 opacity-0" defaultChecked />
                              <span className="absolute cursor-pointer inset-0 rounded-full bg-gray-700 peer-checked:bg-blue-600 transition-colors duration-300"></span>
                              <span className="absolute left-1 top-1 h-4 w-4 rounded-full bg-white peer-checked:left-7 transition-all duration-300"></span>
                            </div>
                          </div>
                        </div>
                      </div>
                      
                      <div className="flex justify-end space-x-3">
                        <button className="px-6 py-3 bg-transparent hover:bg-white/10 rounded-xl font-medium border border-white/20 backdrop-blur-sm transition-all duration-300">
                          Cancel
                        </button>
                        <button className="px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-xl font-medium transition-all duration-300 shadow-lg shadow-blue-500/20 hover:shadow-blue-500/30">
                          Save Changes
                        </button>
                      </div>
                    </div>
                  </div>
                </div>
                
                <div className="bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden">
                  <div className="p-6">
                    <h2 className="text-xl font-bold mb-6">Advanced Options</h2>
                    
                    <div className="space-y-6">
                      <div>
                        <h3 className="font-medium mb-2">Security Level</h3>
                        <div className="space-y-2">
                          <div className="flex items-center">
                            <input type="radio" id="security-standard" name="security" className="mr-3" defaultChecked />
                            <label htmlFor="security-standard">Standard</label>
                          </div>
                          <div className="flex items-center">
                            <input type="radio" id="security-enhanced" name="security" className="mr-3" />
                            <label htmlFor="security-enhanced">Enhanced</label>
                          </div>
                          <div className="flex items-center">
                            <input type="radio" id="security-maximum" name="security" className="mr-3" />
                            <label htmlFor="security-maximum">Maximum</label>
                          </div>
                        </div>
                      </div>
                      
                      <div>
                        <h3 className="font-medium mb-2">Data Retention</h3>
                        <select className="w-full px-4 py-3 bg-gray-900/50 border border-white/10 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500/50">
                          <option>30 days</option>
                          <option>60 days</option>
                          <option selected>90 days</option>
                          <option>180 days</option>
                          <option>1 year</option>
                        </select>
                      </div>
                      
                      <div>
                        <h3 className="font-medium mb-4">Danger Zone</h3>
                        <div className="p-4 border border-red-500/30 rounded-lg bg-red-900/10">
                          <h4 className="text-red-400 font-medium mb-2">Reset Dropbox</h4>
                          <p className="text-sm text-gray-400 mb-3">
                            This will clear all envelope data and media files. This action cannot be undone.
                          </p>
                          <button className="px-4 py-2 bg-red-600/20 hover:bg-red-600/40 border border-red-500/30 text-red-400 rounded-lg text-sm transition-colors">
                            Reset Dropbox
                          </button>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}
          </motion.div>
        </div>
      </div>
    </div>
  );
};

export default DashboardPage;

