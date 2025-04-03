// src/App.tsx
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Provider } from 'react-redux';
import store from './store';
import Navbar from './components/Layout/Navbar';
import HomePage from './pages/HomePage';
import DashboardPage from './pages/DashboardPage';
import MapPage from './pages/MapPage';
import VideoPage from './pages/VideoPage';

const App: React.FC = () => {
  return (
    <Provider store={store}>
      <Router>
        <div className="min-h-screen bg-gray-100">
          <Navbar />
          <main className="py-4">
            <Routes>
              <Route path="/" element={<HomePage />} />
              <Route path="/dashboard/:dropboxId" element={<DashboardPage />} />
              <Route path="/map" element={<MapPage />} />
              <Route path="/video/:videoName" element={<VideoPage />} />
            </Routes>
          </main>
        </div>
      </Router>
    </Provider>
  );
};

export default App;