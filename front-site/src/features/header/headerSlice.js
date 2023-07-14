import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    user_is_login: true,
};

export const headerSlice = createSlice({
    name: 'header',
    initialState,
    reducers: {
        setUserLogin: (state, action) => {state.user_is_login = action.payload}
    }
});

export const {setUserLogin} = headerSlice.actions;
export const selectUserLogin = (state) => state.header.user_is_login;

export default headerSlice.reducer;