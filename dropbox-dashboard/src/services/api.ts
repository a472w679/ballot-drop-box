// src/services/api.ts
import { DropboxData, DropboxLocation } from '../types';

// Simulated API responses
const mockDropboxData: Record<number, DropboxData> = {
  1: {
    id: 1,
    envelopeData: [
      {
        id: 1,
        date: '2025-04-01',
        code39: 'ABC123456789',
        imb: '0123456789012345678901',
        streetAddress: '123 Main St',
        city: 'San Francisco',
        zipCode: '94105',
        status: 'Delivered'
      },
      {
        id: 2,
        date: '2025-04-02',
        code39: 'DEF987654321',
        imb: '9876543210987654321098',
        streetAddress: '456 Market St',
        city: 'San Francisco',
        zipCode: '94103',
        status: 'In Transit'
      }
    ],
    mediaFiles: [
      { name: 'recording_2025-04-01_10-30-45.webm', size: '15.2 MB', time: '10:30:45' },
      { name: 'recording_2025-04-02_14-22-16.webm', size: '18.7 MB', time: '14:22:16' }
    ]
  },
  2: {
    id: 2,
    envelopeData: [
      {
        id: 3,
        date: '2025-04-01',
        code39: 'GHI555666777',
        imb: '1122334455667788990011',
        streetAddress: '789 Mission St',
        city: 'San Francisco',
        zipCode: '94107',
        status: 'Delivered'
      }
    ],
    mediaFiles: [
      { name: 'recording_2025-04-01_09-15-33.webm', size: '12.6 MB', time: '09:15:33' }
    ]
  },
  3: {
    id: 3,
    envelopeData: [],
    mediaFiles: []
  }
};

const mockLocations: DropboxLocation[] = [
  { id: 1, lat: 37.7749, lng: -122.4194, address: '123 Main St, San Francisco, CA 94105' },
  { id: 2, lat: 37.7833, lng: -122.4167, address: '456 Market St, San Francisco, CA 94103' },
  { id: 3, lat: 37.7694, lng: -122.4862, address: '789 Mission St, San Francisco, CA 94107' }
];

export const fetchDropboxById = async (id: number): Promise<DropboxData> => {
  return new Promise((resolve, reject) => {
    setTimeout(() => {
      const data = mockDropboxData[id];
      if (data) {
        resolve(data);
      } else {
        reject(new Error(`Dropbox with id ${id} not found`));
      }
    }, 500);
  });
};

export const fetchLocations = async (): Promise<DropboxLocation[]> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      resolve(mockLocations);
    }, 500);
  });
};

export const exportCSV = async (dropboxId: number): Promise<Blob> => {
  return new Promise((resolve) => {
    setTimeout(() => {
      const csvContent = 'date,code39,imb,streetAddress,city,zipCode,status\n' +
        '2025-04-01,ABC123456789,0123456789012345678901,123 Main St,San Francisco,94105,Delivered\n' +
        '2025-04-02,DEF987654321,9876543210987654321098,456 Market St,San Francisco,94103,In Transit';
      
      const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
      resolve(blob);
    }, 300);
  });
};

export{}