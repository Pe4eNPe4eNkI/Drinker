import { configureStore } from '@reduxjs/toolkit';
import counterReducer from '../features/counter/counterSlice';
import bodyReducer from '../features/body/bodySlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    body: bodyReducer,
  },
});
