import React, {ReactComponent} from 'react';
import styles from './Item.module.css';
import { ReactComponent as Plus } from './Vector.svg';
import { useDispatch, useSelector } from 'react-redux';
import { addToCart } from '../bodySlice';
import { selectCartID } from '../../header/headerSlice';

function Item({
    name,
    price,
    img,
    id,
}) {
    const cart_id = useSelector(selectCartID);
    const dispatch = useDispatch();

    return (
        <div className={styles.container}>
            <div className={styles.img}>
                <img src={img}/>
            </div>
            <div className={styles.name}>{name}</div>
            <div className={styles.price}>{price}&#8381;</div>
            <div className={styles.addWrapp}>
                <div className={styles.add} onClick={()=>dispatch(addToCart({
                    item_id: id,
                    cart_id,
                    count: 1,
                }))}>
                    <Plus style={{stroke: '#A5390B'}}/>
                </div>
            </div>
        </div>
    );
}

export default Item;