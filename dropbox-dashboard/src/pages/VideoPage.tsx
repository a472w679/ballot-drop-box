// src/pages/VideoPage.tsx
import React from 'react';
import { useParams, Link } from 'react-router-dom';

const VideoPage: React.FC = () => {
  const { videoName } = useParams<{ videoName: string }>();
  
  return (
    <div className="max-w-4xl mx-auto text-center">
      <h1 className="text-4xl font-bold text-blue-600 mb-6">{videoName}</h1>
      
      <div className="bg-white p-6 rounded-lg shadow-lg">
        <video 
          className="w-full rounded" 
          controls
          src={`/api/videos/${videoName}`} 
        >
          <source src={`/api/videos/${videoName}`} type="video/webm" />
          Your browser does not support the video tag.
        </video>
        
        <div className="mt-4 flex justify-between">
          <Link 
            to={`/dashboard/${1}`} 
            className="px-4 py-2 bg-gray-200 text-gray-700 rounded hover:bg-gray-300 transition"
          >
            Back to Dashboard
          </Link>
          
          <a 
            href={`/api/videos/${videoName}?download=true`}
            download
            className="px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
          >
            Download Video
          </a>
        </div>
      </div>
    </div>
  );
};

export default VideoPage;