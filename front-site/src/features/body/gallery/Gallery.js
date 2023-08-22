import React from 'react';
import { useSelector } from 'react-redux/es/hooks/useSelector';
import styles from './Gallery.module.css';
import Item from '../item/Item';
import { selectItems } from '../bodySlice';
import { useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { getItems } from '../bodySlice';
import { getUser } from '../../header/headerSlice';
import { selectUserID } from '../../header/headerSlice';

function Gallery() {
    const dispatch = useDispatch();
    const items = useSelector(selectItems);
    const userID = useSelector(selectUserID);

    useEffect(()=>{
        dispatch(getItems());
    }, []);

    useEffect(()=>{
        dispatch(getUser(userID));
    }, [userID])

    return (
        <div className={styles.container}>
            {items.map(({name, price, image_url, id}) => <Item key={id} id={id} name={name} price={price} img={image_url}/>)}
        </div>
    );
}

export default Gallery;