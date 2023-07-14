import React from 'react';
import { useSelector } from 'react-redux';
import { selectMode } from '../userSlice';
import OrderList from '../order_list/OrderList';

function RightSide() {
    const mode = useSelector(selectMode);
    return (<>
        {mode == 'order' ? <OrderList/> : null}
    </>);
}

export default RightSide;  