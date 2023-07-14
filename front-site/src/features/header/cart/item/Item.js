import React from 'react';
import styles from './Item.module.css';
import close from './close.svg';
import arrow from './arrow.svg';

function Item({
    name, count, price, img
}) {
    return (
        <div className={styles.container}>
            <div className={styles.img}>
                <img src={img}/>
            </div>
            <div className={styles.block}>
                <div className={styles.price}>{price}&#8381;</div>
                <div className={styles.name}>{name}</div>
            </div>
            <div className={styles.right}>
                <div className={styles.close}>
                    <img src={close}/>
                </div>
                <div className={styles.counter}>
                    <div className={styles.leftArr}><img src={arrow}/></div>
                    <input className={styles.mid} type='text' value={count}/>
                    <div className={styles.rightArr}><img src={arrow}/></div>
                </div>
            </div>
        </div>

    );
}

export default Item;