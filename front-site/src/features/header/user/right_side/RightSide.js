import React from 'react';
import { useSelector } from 'react-redux';
import { selectMode } from '../userSlice';
import OrderList from '../order_list/OrderList';
import Edit from '../edit/Edit';

function RightSide() {
    const mode = useSelector(selectMode);
    return (<>
        {mode == 'order' ? <OrderList/> : <Edit/>}
    </>);
}

export default RightSide;  