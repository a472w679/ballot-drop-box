// src/pages/MapPage.tsx
import React, { useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import DropboxMap from '../components/Map/DropboxMap';
import { fetchDropboxLocations } from '../store/slices/dropboxSlice';
import { RootState } from '../store';

const MapPage: React.FC = () => {
  const dispatch = useDispatch();
  const { locations, loadingLocations, errorLocations } = useSelector((state: RootState) => state.dropbox);
  
  useEffect(() => {
    dispatch(fetchDropboxLocations() as any);
  }, [dispatch]);
  
  if (loadingLocations) {
    return <div className="flex justify-center items-center h-64">Loading map data...</div>;
  }
  
  if (errorLocations || !locations) {
    return (
      <div className="flex justify-center items-center h-64">
        Error loading map data. Please try again.
      </div>
    );
  }
  
  return (
    <div className="max-w-6xl mx-auto px-4">
      <h1 className="text-2xl font-bold text-blue-600 mb-6">Dropbox Locations</h1>
      <DropboxMap locations={locations} />
    </div>
  );
};

export default MapPage;

export{}