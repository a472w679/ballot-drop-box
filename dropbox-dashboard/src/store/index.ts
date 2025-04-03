// src/store/index.ts
import { configureStore } from '@reduxjs/toolkit';
import dropboxReducer from './slices/dropboxSlice';

const store = configureStore({
  reducer: {
    dropbox: dropboxReducer,
  },
});

export type RootState = ReturnType<typeof store.getState>;
export type AppDispatch = typeof store.dispatch;

export default store;
export{}