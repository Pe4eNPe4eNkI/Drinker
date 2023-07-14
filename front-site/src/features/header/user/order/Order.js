import React from 'react';
import styles from './Order.module.css';

function Order({
    id, 
    status,
    time,
    curier,
    cart
}) {
    const order = [
        {
            name: 'sdfsfg',
            price: 12,
            count: 3,
        },
        {
            name: 'aaa',
            price: 4,
            count: 4,
        },
        {
            name: 'sdf',
            price: 1,
            count: 2,
        },
        {
            name: 'fgh',
            price: 123,
            count: 3,
        },
    ]
    return (
        <div className={styles.container}>
            <div className={styles.title}>Заказ №{id}</div>
            <div className={styles.info}>Статус: {status}</div>
            <div className={styles.info}>Время заказа: {time}</div>
            <div className={styles.curier}>Курьер: {curier}</div>
            <div className={styles.orderTitle}>Информация о заказе</div>
            <div className={styles.order}>
                {order.map(({name, price, count}) =>
                    <div
                        className={styles.item}
                    >{name}, {price}&#8381;, x {count}</div>
                )}
            </div>
            <div className={styles.result}>
                <div>Итог</div>
                <div>{order.reduce((ac, {price})=>ac+=parseFloat(price), 0)}&#8381;</div>
            </div>
        </div>
    );
}

export default Order;