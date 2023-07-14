import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { Fetch } from "../../app/fetch";


export const auth = createAsyncThunk(
    'header/auth',
    async ({
        login, password
    }) => {
        let json;
        try {
            json = await Fetch({
                method: 'POST',
                url: 'auth',
                args: {
                    login,
                    password,
                },
            })
        } catch (err) {
            console.dir(err);
        }

        return {id: json.account_id, type: json.type};
    }
);

export const register = createAsyncThunk(
    'header/register',
    async ({
        login, password
    }) => {
        let json;
        try {
            json = await Fetch({
                method: 'PUT',
                url: 'register',
                args: {
                    login, password,
                },
            });
        } catch (err) {
            console.dir(err);
        }

        return json.account_id;
    }
);

export const getUser = createAsyncThunk(
    'header/getUser',
    async (user_id) => {
        let json;
        try {
            json = await Fetch({
                method: 'POST',
                url: 'user/get',
                args: {
                    user_id,
                }
            });
        } catch (err) {console.log(err)}

        return json.user;
    }
)


const initialState = {
    user_is_login: false,
    user_id: 0,
    acc_type: 'user',
    cards:[],
    passport:{
        serial: 0,
        number: 0
    },
    birth: '1212',
    verified: true,
    cart_id: 0,
};

export const headerSlice = createSlice({
    name: 'header',
    initialState,
    reducers: {
        setUserLogin: (state, action) => {state.user_is_login = action.payload},
        logOut: (state) => {state.user_is_login = false;}
    },
    extraReducers: (builder) => {
        builder.addCase(register.fulfilled, (state,action)=> {
            state.user_is_login = true;
            state.user_id = action.payload;
        })
        .addCase(auth.fulfilled, (state, action)=> {
            state.user_is_login = true;
            state.acc_type = action.payload.type;
            state.user_id = action.payload.id;
        })
        .addCase(getUser.fulfilled, (state, action) => {
            state.cards = action.payload.cards;
            state.passport = action.payload.passport;
            state.birth = action.payload.birth;
            state.verified = action.payload.verified;
            state.cart_id = action.payload.cart_id;
        })
    }
});

export const {setUserLogin} = headerSlice.actions;
export const selectUserLogin = (state) => state.header.user_is_login;
export const selectUserID = (state) => state.header.user_id;
export const selectAccType = (state) => state.header.acc_type;
export const selectCartID = (state) => state.header.cart_id;

export default headerSlice.reducer;