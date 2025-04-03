// src/components/Map/DropboxMap.tsx
import React, { useEffect, useRef } from 'react';
import L from 'leaflet';
import { DropboxLocation } from '../../types';
import 'leaflet/dist/leaflet.css';

interface DropboxMapProps {
  locations: DropboxLocation[];
}

const DropboxMap: React.FC<DropboxMapProps> = ({ locations }) => {
  const mapRef = useRef<HTMLDivElement>(null);
  const leafletMap = useRef<L.Map | null>(null);
  
  useEffect(() => {
    if (mapRef.current && !leafletMap.current) {
      // Initialize map
      leafletMap.current = L.map(mapRef.current).setView([37.7749, -122.4194], 13);
      
      // Add tile layer
      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
      }).addTo(leafletMap.current);
      
      // Add custom CSS class for styling
      leafletMap.current.getContainer().classList.add('hs-leaflet');
    }
    
    // Add markers for each dropbox location
    if (leafletMap.current) {
      // Clear existing markers
      leafletMap.current.eachLayer((layer) => {
        if (layer instanceof L.Marker) {
          leafletMap.current?.removeLayer(layer);
        }
      });
      
      locations.forEach(location => {
        const marker = L.marker([location.lat, location.lng]).addTo(leafletMap.current!);
        
        marker.bindPopup(`
          <div>
            <h3 class="font-semibold">Dropbox #${location.id}</h3>
            <p>${location.address}</p>
            <a href="/dashboard/${location.id}" class="text-blue-600 hover:underline">View Dashboard</a>
          </div>
        `);
      });
    }
    
    return () => {
      if (leafletMap.current) {
        leafletMap.current.remove();
        leafletMap.current = null;
      }
    };
  }, [locations]);
  
  return (
    <div className="h-[500px] w-full">
      <div ref={mapRef} className="h-full w-full rounded border-2 border-gray-300"></div>
    </div>
  );
};

export default DropboxMap;

export{}