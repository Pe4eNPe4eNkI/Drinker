import React from 'react';
import styles from './OrderList.module.css';

function OrderList({children}) {
    return (
        <div className={styles.container}>
            {children}
        </div>
    );
}

export default OrderList;