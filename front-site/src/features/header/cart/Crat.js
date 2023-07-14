import React from 'react';
import styles from './Cart.module.css';
import Item from './item/Item';

function Cart() {
    return (
    <div className={styles.container}>
        <Item price={213} name='adfgdg' count={1} img='https://ak-d.tripcdn.com/images/100r1f000001gor3c9565_W_1000_750_Q80.jpg?proc=source%2ftrip&proc=source%2ftrip'/>
        <div className={styles.bottom}>
            <div className={styles.result}>Итог: 12&#8381;</div>
            <button>Купить</button>
        </div>
    </div>
    );
}

export default Cart;