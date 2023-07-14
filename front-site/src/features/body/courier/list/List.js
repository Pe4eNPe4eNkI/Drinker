import React from 'react';
import styles from './List.module.css';
import { useSelector } from 'react-redux';
import { selectOnWayOrders, selectAssemblingOrders } from '../courierSlice';
import Item from '../item/Item';

function List({type}) {
    const onWay = useSelector(selectOnWayOrders);
    const assembling = useSelector(selectAssemblingOrders);

    return ( <div className={styles.container}>
        {
            type == 'onWay'
            ?
            onWay.map(elem => <Item elem={elem}/>)
            :
            assembling.map(elem => <Item elem={elem}/>)
        }
    </div> );
}

export default List;