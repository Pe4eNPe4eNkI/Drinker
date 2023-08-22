import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    orders: [
        {
            address: 'iosgnjkdhjkkdgf 56',
            status: 'onWay',
            id: 11,
            user_info: {
                name: 'adfdghd',
                surname: 'sdgdh',
                middlename: 'sdgdh',
                phone: '356567678',
            },
            courier_info: {
                name: '1adfdghd',
                surname: '1sdgdh',
                middlename: '1sdgdh',
                phone: '1356567678',
            }
        },
        {
            address: 'sddddd 526',
            status: 'assembling',
            id: 12,
            user_info: {
                name: '124',
                surname: 'fds',
                middlename: 'sfs',
                phone: '356567678',
            },
            courier_info: {
                name: '1adfdghd',
                surname: '1sdsddgdh',
                middlename: 'sfsf',
                phone: '1367678',
            }
        }
    ]
};

export const courierSlice = createSlice({
    name: 'courier',
    initialState,
    reducers: {

    }
});

export const selectOnWayOrders = (state) => state.courier.orders.filter(({status}) => status == 'onWay');
export const selectAssemblingOrders = (state) => state.courier.orders.filter(({status}) => status == 'assembling');

export default courierSlice.reducer;