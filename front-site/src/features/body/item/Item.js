import React, {ReactComponent} from 'react';
import styles from './Item.module.css';
import { ReactComponent as Plus } from './Vector.svg';

function Item({
    name,
    price,
    img,
}) {
    return (
        <div className={styles.container}>
            <div className={styles.img}>
                <img src={img}/>
            </div>
            <div className={styles.name}>{name}</div>
            <div className={styles.price}>{price}&#8381;</div>
            <div className={styles.addWrapp}>
                <div className={styles.add}>
                    <Plus style={{stroke: '#A5390B'}}/>
                </div>
            </div>
        </div>
    );
}

export default Item;