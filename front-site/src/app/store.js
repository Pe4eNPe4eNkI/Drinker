import { configureStore } from '@reduxjs/toolkit';
import counterReducer from '../features/counter/counterSlice';
import bodyReducer from '../features/body/bodySlice';
import headerReducer from '../features/header/headerSlice';
import userReducer from '../features/header/user/userSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    body: bodyReducer,
    header: headerReducer,
    user: userReducer,
  },
});
