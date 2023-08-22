import React from 'react';
import styles from './OrderList.module.css';
import Order from '../order/Order';

function OrderList({children}) {
    return (
        <div className={styles.container}>
            <Order id='12' status='fullfuled' time='12.12.2204' curier='sdffdgdf'/>
            <Order id='12' status='fullfuled' time='12.12.2204' curier='sdffdgdf'/>
            <Order id='12' status='fullfuled' time='12.12.2204' curier='sdffdgdf'/>
        </div>
    );
}

export default OrderList;