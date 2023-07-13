import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    items: [
        {
            id: 1,
            name: 'aaa',
            price: '123',
            img: 'https://hips.hearstapps.com/del.h-cdn.co/assets/cm/15/11/3200x3272/54f65d39ab05d_-_183341797.jpg?resize=1200:*',
            tag: 'a',
        },
        {
            id: 2,
            name: 'bbb',
            price: '321',
            img: 'https://en.wikiquote.org/wiki/Beer#/media/File:Beer_mug.svg',
            tag: 'b'
        }
    ],
    tag: 'none',
    search: '',
};

export const bodySlice = createSlice({
    name: 'body',
    initialState: initialState,
    reducers: {
        setSearch: (state, action) => {
            state.search = action.payload;
        },
        setTag: (state, action) => {
            if (action.payload == state.tag) {
                state.tag = 'none';
            } else {
                state.tag = action.payload;
            }
        }
    }
});

export const {setSearch, setTag} = bodySlice.actions;

export const selectItems = (state) => state.body.items.filter(item => {
    if (state.body.tag == 'none') {
        return item.name.includes(state.body.search);
    }
    return item.tag == state.body.tag && item.name.includes(state.body.search);
});
export const selectTag = (state) => state.body.tag;
export const selectSearch = (state) => state.body.search;

export default bodySlice.reducer;