import React from 'react';
import { UseSelector, useSelector } from 'react-redux/es/hooks/useSelector';
import styles from './Gallery.module.css';
import Item from '../item/Item';
import { selectItems } from '../bodySlice';

function Gallery() {
    const items = useSelector(selectItems);

    return (
        <div className={styles.container}>
            {items.map(({name, price, img, id}) => <Item key={id} name={name} price={price} img={img}/>)}
        </div>
    );
}

export default Gallery;