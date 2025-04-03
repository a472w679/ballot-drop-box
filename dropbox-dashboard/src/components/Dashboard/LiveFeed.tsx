// src/components/Dashboard/LiveFeed.tsx
import React, { useState, useEffect } from 'react';
import { MediaFile } from '../../types';
import { Link } from 'react-router-dom';

interface LiveFeedProps {
  dropboxId: number;
  mediaFiles: MediaFile[];
}

const LiveFeed: React.FC<LiveFeedProps> = ({ dropboxId, mediaFiles }) => {
  const [isStreamAvailable, setIsStreamAvailable] = useState<boolean>(false);
  
  useEffect(() => {
    // Simulate checking if stream is available
    const checkStreamAvailability = async () => {
      // In a real app, this would be an API call
      const available = Math.random() > 0.5; // Simulating 50% chance of stream being available
      setIsStreamAvailable(available);
    };
    
    checkStreamAvailability();
    
    // Set up polling to check stream availability
    const interval = setInterval(checkStreamAvailability, 30000);
    
    return () => clearInterval(interval);
  }, [dropboxId]);
  
  return (
    <div>
      <figure className="max-w-lg mt-5">
        {isStreamAvailable ? (
          <video 
            className="h-auto max-w-full rounded-lg" 
            autoPlay 
            muted
            src={`/api/stream/${dropboxId}`} 
          />
        ) : (
          <img 
            className="h-auto max-w-full rounded-lg" 
            src="/images/stream_unavailable.png" 
            alt="Stream unavailable" 
          />
        )}
        <figcaption className="mt-2 text-sm text-center text-gray-500">Live Feed</figcaption>
      </figure>
      
      <div className="max-w-full h-[300px] mt-6">
        <h3 className="font-semibold mb-2">Motion Recordings</h3>
        <ul className="w-full text-sm font-medium text-gray-900 bg-white border border-gray-200 rounded-lg">
          {mediaFiles.map((file, index) => (
            <li key={index} className="w-full px-4 py-2 border-b border-gray-200 rounded-t-lg">
              <Link to={`/video/${file.name}`} className="hover:text-blue-600 transition">
                {file.name} {file.size} {file.time}
              </Link>
            </li>
          ))}
        </ul>
      </div>
    </div>
  );
};

export default LiveFeed;

export{}