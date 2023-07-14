import React from 'react';
import styles from './AddItem.module.css';
import { useDispatch } from 'react-redux';
import { putItem } from '../bodySlice';
import { useState } from 'react';

function AddItem() {
    const [name, setName] = useState('');
    const [price, setPrice] = useState('');
    const [url, setUrl] = useState('');
    const dis = useDispatch();
    return (
        <div className={styles.container}>
            <input type='text' value={name} onChange={(e)=>setName(e.target.value)} placeholder='Наименование'/>
            <input type='text' value={price} onChange={(e)=>setPrice(e.target.value)} placeholder='Цена'/>
            <input type='text' value={url} onChange={(e)=>setUrl(e.target.value)} placeholder='ULR'/>
            <button onClick={()=> {
                dis(putItem({
                    name, price, image_url: url
                }))
            }}>Создать</button>
        </div>
    );
}

export default AddItem;