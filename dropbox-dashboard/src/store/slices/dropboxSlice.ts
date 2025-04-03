// src/store/slices/dropboxSlice.ts
import { createSlice, createAsyncThunk, PayloadAction } from '@reduxjs/toolkit';
import { DropboxData, DropboxLocation } from '../../types';
import { fetchDropboxById, fetchLocations } from '../../services/api';

interface DropboxState {
  currentDropbox: DropboxData | null;
  locations: DropboxLocation[];
  loading: boolean;
  error: string | null;
  loadingLocations: boolean;
  errorLocations: string | null;
}

const initialState: DropboxState = {
  currentDropbox: null,
  locations: [],
  loading: false,
  error: null,
  loadingLocations: false,
  errorLocations: null,
};

export const fetchDropboxData = createAsyncThunk(
  'dropbox/fetchData',
  async (dropboxId: number) => {
    const response = await fetchDropboxById(dropboxId);
    return response;
  }
);

export const fetchDropboxLocations = createAsyncThunk(
  'dropbox/fetchLocations',
  async () => {
    const response = await fetchLocations();
    return response;
  }
);

const dropboxSlice = createSlice({
  name: 'dropbox',
  initialState,
  reducers: {},
  extraReducers: (builder) => {
    builder
      .addCase(fetchDropboxData.pending, (state) => {
        state.loading = true;
        state.error = null;
      })
      .addCase(fetchDropboxData.fulfilled, (state, action: PayloadAction<DropboxData>) => {
        state.loading = false;
        state.currentDropbox = action.payload;
      })
      .addCase(fetchDropboxData.rejected, (state, action) => {
        state.loading = false;
        state.error = action.error.message || 'Failed to fetch dropbox data';
      })
      .addCase(fetchDropboxLocations.pending, (state) => {
        state.loadingLocations = true;
        state.errorLocations = null;
      })
      .addCase(fetchDropboxLocations.fulfilled, (state, action: PayloadAction<DropboxLocation[]>) => {
        state.loadingLocations = false;
        state.locations = action.payload;
      })
      .addCase(fetchDropboxLocations.rejected, (state, action) => {
        state.loadingLocations = false;
        state.errorLocations = action.error.message || 'Failed to fetch locations';
      });
  },
});

export default dropboxSlice.reducer;

export{}