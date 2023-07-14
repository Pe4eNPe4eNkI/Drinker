import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    mode: 'order',
    accountType: 'courier',
    info: {
        name: 'aa',
        surname: 'bb',
        middlename: 'cc',
        phone: '+12345456',
    },
    passport: {
        number: '5717 924567',
        date: '18.17.2019',
    },
    cards: [
        {
            number: '2018 5643 3245 3484',
        },
        {
            number: '3418 5643 6545 6784',
        },
        {
            number: '2056 5643 3675 6734',
        }
    ]
}

export const userSlice = createSlice({
    name: 'user',
    initialState,
    reducers: {
        setMode: (state, action) => {state.mode = action.payload},
    },
});

export const {setMode} = userSlice.actions;
export const selectMode = (state) => state.user.mode;
export const selectInfo = (state) => state.user.info;
export const selectPassport = (state) => state.user.passport;
export const selectCards = (state) => state.user.cards;
export const selectAccType = (state) => state.user.accountType;

export default userSlice.reducer;