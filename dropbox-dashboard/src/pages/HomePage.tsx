// src/pages/HomePage.tsx
import React, { useEffect } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import './HomePage.css'; // Import the CSS file with animations

const HomePage: React.FC = () => {
  // Animation variants for consistent effects
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

  // Add futuristic particle background effect
  useEffect(() => {
    const script = document.createElement('script');
    script.src = 'https://cdnjs.cloudflare.com/ajax/libs/particles.js/2.0.0/particles.min.js';
    script.async = true;
    document.body.appendChild(script);

    script.onload = () => {
      // @ts-ignore
      window.particlesJS('particles-js', {
        particles: {
          number: { value: 80, density: { enable: true, value_area: 800 } },
          color: { value: '#3f83f8' },
          shape: { type: 'circle' },
          opacity: { value: 0.2, random: false },
          size: { value: 3, random: true },
          line_linked: { enable: true, distance: 150, color: '#3f83f8', opacity: 0.2, width: 1 },
          move: { enable: true, speed: 1, direction: 'none', random: true, straight: false, out_mode: 'out', bounce: false }
        },
        interactivity: {
          detect_on: 'canvas',
          events: { onhover: { enable: true, mode: 'grab' }, onclick: { enable: true, mode: 'push' } },
          modes: { grab: { distance: 140, line_linked: { opacity: 0.5 } }, push: { particles_nb: 4 } }
        }
      });
    };

    return () => {
      document.body.removeChild(script);
    };
  }, []);

  return (
    <div className="min-h-screen bg-gradient-to-br from-gray-900 via-gray-800 to-black text-white overflow-x-hidden">
      {/* Particles background */}
      <div id="particles-js" className="absolute inset-0 z-0"></div>
      
      {/* Main Content */}
      <div className="relative z-10 max-w-7xl mx-auto px-6 py-16">
        {/* Hero Section */}
        <div className="mb-20 relative">
          <div className="absolute inset-0 bg-blue-600/10 blur-[60px] rounded-full -z-10"></div>
          <motion.div 
            className="max-w-3xl"
            initial="hidden"
            animate="visible"
            variants={fadeIn}
            custom={0}
          >
            <div className="mb-4 inline-flex items-center p-1 pl-4 pr-2 bg-blue-900/30 rounded-full backdrop-blur-sm border border-blue-500/20">
              <span className="text-blue-300 text-sm mr-2">Powered by AI</span>
              <span className="px-2 py-1 bg-blue-500 rounded-full text-xs font-semibold">NEW</span>
            </div>
            
            <h1 className="text-4xl md:text-5xl lg:text-6xl font-bold leading-tight mb-6 bg-clip-text text-transparent bg-gradient-to-r from-blue-300 via-blue-100 to-blue-400">
              Next-Gen Dropbox <br />Monitoring System
            </h1>
            <p className="text-xl text-blue-100/80 mb-8 leading-relaxed">
              Smart tracking with real-time analytics. Our advanced system leverages cutting-edge 
              technology to ensure your deliveries are secure and monitored 24/7.
            </p>
            <div className="flex flex-wrap gap-4">
              <Link 
                to="/dashboard" 
                className="group relative px-8 py-4 bg-blue-600 hover:bg-blue-700 rounded-xl font-medium transition-all duration-300 shadow-lg shadow-blue-500/20 hover:shadow-blue-500/30 overflow-hidden"
              >
                <span className="relative z-10">Go to Dashboard</span>
                <div className="absolute inset-0 -translate-x-full group-hover:translate-x-0 bg-gradient-to-r from-blue-400 to-blue-600 transition-transform duration-500 ease-out z-0"></div>
              </Link>
              <Link 
                to="/tour" 
                className="relative px-8 py-4 bg-transparent hover:bg-white/10 rounded-xl font-medium border border-white/20 backdrop-blur-sm transition-all duration-300 overflow-hidden"
              >
                <span className="relative z-10">Take a Tour</span>
                <div className="absolute inset-0 opacity-0 hover:opacity-10 bg-gradient-to-r from-blue-400 to-purple-600 transition-opacity duration-300 z-0"></div>
              </Link>
            </div>
          </motion.div>
        </div>

        {/* Dropbox Grid */}
        <motion.h2 
          className="text-3xl font-bold mb-8 bg-clip-text text-transparent bg-gradient-to-r from-blue-100 to-blue-300"
          initial="hidden"
          animate="visible"
          variants={fadeIn}
          custom={1}
        >
          Your Dropboxes
        </motion.h2>
        
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
          initial="hidden"
          animate="visible"
          variants={fadeIn}
          custom={2}
        >
          {[1, 2, 3].map((id) => (
            <Link 
              key={id}
              to={`/dashboard/${id}`}
              className="group block"
            >
              <div className="relative bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden hover:bg-gray-800/60 transition-all duration-300 hover:shadow-xl hover:shadow-blue-500/10 h-full">
                {/* Glowing border effect on hover */}
                <div className="absolute inset-0 opacity-0 group-hover:opacity-100 transition-opacity duration-300 pointer-events-none">
                  <div className="absolute inset-0 rounded-2xl border-2 border-blue-400 blur-sm"></div>
                </div>
                
                <div className={`h-24 relative overflow-hidden ${
                  id === 1 ? 'bg-gradient-to-r from-blue-600 to-indigo-700' : 
                  id === 2 ? 'bg-gradient-to-r from-emerald-600 to-cyan-700' :
                  'bg-gradient-to-r from-pink-600 to-purple-700'
                }`}>
                  {/* Animated wave effect */}
                  <div className="absolute left-0 right-0 top-[-10%] h-[50%] w-[200%] animate-wave bg-opacity-20 bg-gradient-to-r from-transparent via-white/5 to-transparent"></div>
                  <div className="absolute left-0 right-0 top-[30%] h-[50%] w-[200%] animate-wave-reverse bg-opacity-10 bg-gradient-to-r from-transparent via-white/5 to-transparent"></div>
                  
                  <div className="absolute inset-0 bg-black/20"></div>
                  <div className="absolute bottom-4 left-4 flex items-center justify-between w-full pr-4">
                    <div className="flex items-center space-x-2">
                      <div className={`h-2 w-2 rounded-full ${id === 3 ? 'bg-gray-400' : 'bg-green-400 animate-pulse'}`}></div>
                      <span className="text-sm font-medium">{id === 3 ? 'Inactive' : 'Active'}</span>
                    </div>
                    <span className="text-sm bg-black/30 px-2 py-1 rounded-full backdrop-blur-sm">
                      Box #{id}
                    </span>
                  </div>
                </div>
                
                <div className="p-6 relative overflow-hidden">
                  {/* Subtle animated gradient background */}
                  <div className="absolute -inset-[100%] bg-gradient-to-r from-blue-500/5 via-transparent to-blue-500/5 animate-[pulse_15s_ease-in-out_infinite] pointer-events-none"></div>
                  
                  <h3 className="text-xl font-bold mb-2 group-hover:text-blue-400 transition-colors">
                    Dropbox {id === 1 ? 'Alpha' : id === 2 ? 'Beta' : 'Gamma'}
                  </h3>
                  <p className="text-gray-400 text-sm mb-4">
                    {id === 1 ? 'Main entrance, high traffic' : 
                     id === 2 ? 'Secondary location, medium traffic' : 
                     'Remote location, monitored weekly'}
                  </p>
                  
                  <div className="flex justify-between items-center">
                    <div className="flex items-center space-x-3">
                      <div className="flex -space-x-2">
                        {Array(id === 1 ? 3 : id === 2 ? 2 : 1).fill(0).map((_, i) => (
                          <div key={i} className="h-8 w-8 rounded-full bg-gray-700 border-2 border-gray-800 flex items-center justify-center text-xs">
                            {['A', 'B', 'C'][i]}
                          </div>
                        ))}
                      </div>
                      <span className="text-sm text-gray-400">
                        {id === 1 ? '2 new' : id === 2 ? '1 new' : '0 new'}
                      </span>
                    </div>
                    <div className="w-7 h-7 flex items-center justify-center rounded-full bg-blue-500/10 group-hover:bg-blue-500 transition-colors duration-300">
                      <svg className="h-4 w-4 text-gray-400 group-hover:text-white transition-colors duration-300" 
                        fill="none" viewBox="0 0 24 24" stroke="currentColor">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 5l7 7-7 7" />
                      </svg>
                    </div>
                  </div>
                </div>
              </div>
            </Link>
          ))}
        </motion.div>

        {/* Stats Section */}
        <motion.h2 
          className="text-3xl font-bold mt-20 mb-8 bg-clip-text text-transparent bg-gradient-to-r from-blue-100 to-blue-300"
          initial="hidden"
          animate="visible"
          variants={fadeIn}
          custom={3}
        >
          Real-Time Analytics
        </motion.h2>
        
        <motion.div 
          className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6"
          initial="hidden"
          animate="visible"
          variants={fadeIn}
          custom={4}
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
            <h3 className="text-3xl font-bold mb-1">128</h3>
            <p className="text-gray-400 text-sm">Envelopes processed</p>
            
            {/* Mini chart line */}
            <div className="mt-4 h-2 bg-gray-700/50 rounded-full overflow-hidden">
              <div className="h-full w-4/5 bg-blue-500 rounded-full"></div>
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
              <span className="text-sm text-gray-400">Delivered</span>
            </div>
            <h3 className="text-3xl font-bold mb-1">112</h3>
            <p className="text-gray-400 text-sm">87.5% success rate</p>
            
            {/* Mini chart line */}
            <div className="mt-4 h-2 bg-gray-700/50 rounded-full overflow-hidden">
              <div className="h-full w-3/4 bg-green-500 rounded-full"></div>
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
              <span className="text-sm text-gray-400">In Transit</span>
            </div>
            <h3 className="text-3xl font-bold mb-1">16</h3>
            <p className="text-gray-400 text-sm">Expected today</p>
            
            {/* Mini chart line */}
            <div className="mt-4 h-2 bg-gray-700/50 rounded-full overflow-hidden">
              <div className="h-full w-1/5 bg-yellow-500 rounded-full"></div>
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
              <span className="text-sm text-gray-400">Activity</span>
            </div>
            <h3 className="text-3xl font-bold mb-1">24%</h3>
            <p className="text-gray-400 text-sm">Increase this week</p>
            
            {/* Mini chart line */}
            <div className="mt-4 h-2 bg-gray-700/50 rounded-full overflow-hidden">
              <div className="h-full w-1/4 bg-purple-500 rounded-full"></div>
            </div>
          </div>
        </motion.div>

        {/* Map & Network Section */}
        <motion.div 
          className="mt-20 bg-gray-800/40 backdrop-blur-sm border border-white/10 rounded-2xl overflow-hidden group"
          initial="hidden"
          animate="visible"
          variants={fadeIn}
          custom={5}
        >
          <div className="p-6 flex flex-col md:flex-row justify-between items-start md:items-center">
            <div>
              <h2 className="text-2xl font-bold mb-2">Dropbox Network</h2>
              <p className="text-gray-400">View all your dropboxes on an interactive map</p>
            </div>
            <Link 
              to="/map" 
              className="mt-4 md:mt-0 inline-flex items-center px-6 py-3 bg-blue-600 hover:bg-blue-700 rounded-xl font-medium transition-all duration-300 relative overflow-hidden group"
            >
              <span className="relative z-10">Open Map</span>
              <div className="absolute inset-0 translate-x-full group-hover:translate-x-0 bg-gradient-to-r from-blue-500 to-blue-600 transition-transform duration-500 ease-out z-0"></div>
              <svg xmlns="http://www.w3.org/2000/svg" className="ml-2 h-5 w-5 relative z-10" viewBox="0 0 20 20" fill="currentColor">
                <path fillRule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
              </svg>
            </Link>
          </div>
          <div className="h-64 bg-gray-900 relative overflow-hidden">
            {/* Futuristic Map Background */}
            <div className="absolute inset-0 opacity-60">
              {/* Grid lines */}
              <div className="absolute inset-0 grid grid-cols-8 grid-rows-6">
                {Array(48).fill(0).map((_, i) => (
                  <div key={i} className="border border-blue-900/30"></div>
                ))}
              </div>
              
              {/* Dropbox Markers */}
              <div className="absolute top-1/4 left-1/4 h-4 w-4 rounded-full bg-blue-500 animate-ping opacity-75"></div>
              <div className="absolute top-1/4 left-1/4 h-3 w-3 rounded-full bg-blue-400"></div>
              
              <div className="absolute top-2/3 left-1/2 h-4 w-4 rounded-full bg-green-500 animate-ping opacity-75"></div>
              <div className="absolute top-2/3 left-1/2 h-3 w-3 rounded-full bg-green-400"></div>
              
              <div className="absolute top-1/3 right-1/4 h-4 w-4 rounded-full bg-purple-500 animate-ping opacity-75"></div>
              <div className="absolute top-1/3 right-1/4 h-3 w-3 rounded-full bg-purple-400"></div>
              
              {/* Connecting lines with animation */}
              <svg className="absolute inset-0 w-full h-full" xmlns="http://www.w3.org/2000/svg">
                <line x1="25%" y1="25%" x2="50%" y2="66%" stroke="rgba(59, 130, 246, 0.5)" strokeWidth="2" strokeDasharray="5,5" className="animate-dash"></line>
                <line x1="50%" y1="66%" x2="75%" y2="33%" stroke="rgba(59, 130, 246, 0.5)" strokeWidth="2" strokeDasharray="5,5" className="animate-dash"></line>
                <line x1="25%" y1="25%" x2="75%" y2="33%" stroke="rgba(59, 130, 246, 0.5)" strokeWidth="2" strokeDasharray="5,5" className="animate-dash"></line>
              </svg>
              
              {/* Radar ping animation */}
              <div className="absolute top-1/4 left-1/4 w-40 h-40 rounded-full border-2 border-blue-500/20 opacity-0 animate-radar"></div>
            </div>
            
            {/* Gradient overlay */}
            <div className="absolute inset-0 bg-gradient-to-t from-gray-900 via-gray-900/80 to-transparent"></div>
            
            {/* Map Controls */}
            <div className="absolute top-4 right-4 bg-gray-800/80 backdrop-blur-sm rounded-lg p-2 flex space-x-2">
              <button className="p-2 hover:bg-gray-700/80 rounded-lg transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 5a1 1 0 011 1v3h3a1 1 0 110 2h-3v3a1 1 0 11-2 0v-3H6a1 1 0 110-2h3V6a1 1 0 011-1z" clipRule="evenodd" />
                </svg>
              </button>
              <button className="p-2 hover:bg-gray-700/80 rounded-lg transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M5 10a1 1 0 011-1h8a1 1 0 110 2H6a1 1 0 01-1-1z" clipRule="evenodd" />
                </svg>
              </button>
              <button className="p-2 hover:bg-gray-700/80 rounded-lg transition-colors">
                <svg xmlns="http://www.w3.org/2000/svg" className="h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M5.05 4.05a7 7 0 119.9 9.9L10 18.9l-4.95-4.95a7 7 0 010-9.9zM10 11a2 2 0 100-4 2 2 0 000 4z" clipRule="evenodd" />
                </svg>
              </button>
            </div>
            
            {/* Live data indicators */}
            <div className="absolute bottom-4 left-4 bg-gray-800/80 backdrop-blur-sm rounded-lg p-2 text-xs text-gray-300 flex items-center">
              <div className="w-2 h-2 rounded-full bg-green-400 animate-pulse mr-2"></div>
              Live data streaming
            </div>
          </div>
        </motion.div>
        
        {/* CTA Section */}
        <motion.div 
          className="mt-20 text-center"
          initial="hidden"
          animate="visible"
          variants={fadeIn}
          custom={6}
        >
          <h2 className="text-3xl font-bold mb-4 bg-clip-text text-transparent bg-gradient-to-r from-blue-100 to-blue-300">Ready to upgrade your delivery system?</h2>
          <p className="text-gray-400 mb-8 max-w-2xl mx-auto">Join thousands of businesses that trust our advanced monitoring technology to keep their deliveries secure.</p>
          <Link 
            to="/signup" 
            className="inline-flex items-center px-8 py-4 bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-500 hover:to-indigo-500 rounded-xl font-medium transition-all duration-300 shadow-lg shadow-blue-500/20 hover:shadow-blue-500/30"
          >
            Get Started Now
            <svg xmlns="http://www.w3.org/2000/svg" className="ml-2 h-5 w-5" viewBox="0 0 20 20" fill="currentColor">
              <path fillRule="evenodd" d="M10.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L12.586 11H5a1 1 0 110-2h7.586l-2.293-2.293a1 1 0 010-1.414z" clipRule="evenodd" />
            </svg>
          </Link>
        </motion.div>
      </div>
      
      {/* Footer space */}
      <div className="h-20"></div>
      
      {/* Add keyframe animations using styled component or create a separate CSS file */}
    </div>
  );
};

// Add this to your src/index.css or create a HomePage.css file
// @keyframes wave {
//   0%, 100% { transform: translateX(-50%); }
//   50% { transform: translateX(0); }
// }

// @keyframes dash {
//   to { stroke-dashoffset: 20; }
// }

// @keyframes radar {
//   0% { transform: scale(0); opacity: 0.6; }
//   100% { transform: scale(1); opacity: 0; }
// }

// .animate-dash {
//   animation: dash 15s linear infinite;
// }

// .animate-radar {
//   animation: radar 3s ease-out infinite;
// }

export default HomePage;