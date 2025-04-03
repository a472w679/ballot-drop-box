// src/types/index.ts
export interface EnvelopeData {
  id: number;
  date: string;
  code39: string;
  imb: string;
  streetAddress: string;
  city: string;
  zipCode: string;
  status: string;
}

export interface MediaFile {
  name: string;
  size: string;
  time: string;
}

export interface DropboxData {
  id: number;
  envelopeData: EnvelopeData[];
  mediaFiles: MediaFile[];
}

export interface DropboxLocation {
  id: number;
  lat: number;
  lng: number;
  address: string;
}

export{}