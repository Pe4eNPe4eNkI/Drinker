import { configureStore } from '@reduxjs/toolkit';
import counterReducer from '../features/counter/counterSlice';
import bodyReducer from '../features/body/bodySlice';
import headerReducer from '../features/header/headerSlice';
import userReducer from '../features/header/user/userSlice';
import courierReducer from '../features/body/courier/courierSlice';

export const store = configureStore({
  reducer: {
    counter: counterReducer,
    body: bodyReducer,
    header: headerReducer,
    user: userReducer,
    courier: courierReducer,
  },
});
