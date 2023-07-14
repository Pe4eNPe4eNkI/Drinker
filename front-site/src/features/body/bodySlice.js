import { createSlice, createAsyncThunk } from "@reduxjs/toolkit";
import { Fetch } from "../../app/fetch";

const initialState = {
    items: [
    ],
    tag: 'none',
    search: '',
};

export const getItems = createAsyncThunk(
    'body/getItems',
    async (amount) => {
        let json;
        try {
            json = await Fetch({
                url: 'gallery',
                method: 'POST',
            });
        } catch (err) {
            console.dir(err);
        }

        return json.items;
    }
)

export const putItem = createAsyncThunk(
    'body/putItem',
    async ({
        name,
        price,
        image_url
    }) => {
            let json;
            try {
                json = await Fetch({
                    method: 'PUT',
                    url: 'items',
                    args: {
                        name,
                        price,
                        image_url,
                        desc: 'aaaa',
                        id_tag: 1,
                    }
                });
            } catch(err) {console.log(err)}

            return json;
        }
);

export const addToCart = createAsyncThunk(
    'addToCart',
    async ({
        item_id,
        cart_id,
        count,
    }) => {
        let json;
        try {
            json = await Fetch({
                method: 'POST',
                url: 'user/cart',
                args: {
                    cart_id,
                    item_id,
                    count,
                }
            })
        } catch(err) {
            console.log(err);
        }

        return json;
    }
)

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
    },
    extraReducers: (builder) => {
        builder
        .addCase(getItems.fulfilled, (state, action) => {
            state.items = action.payload;
        })
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