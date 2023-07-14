import React, { useState } from 'react';
import styles from './Category.module.css';
import { useSelector, useDispatch } from 'react-redux';
import { setMode, selectMode } from '../userSlice';

function Category() {
    const dispatch = useDispatch();
    const mode = useSelector(selectMode);

    const set = (key) => (e) => dispatch(setMode(key));
    const options = [
        {
            key: 'edit',
            value: 'Редактировать',
        },
        {
            key: 'order',
            value: 'История заказов',
        },
        {
            key: 'exit',
            value: 'Выход'
        }
    ];

    return (
        <div className={styles.container}>
            {
                options.map(({key, value}) => 
                <div
                    className={styles.item}
                    style={{color: mode == key ? '#000' : '#afafaf'}}
                    onClick={set(key)}
                >{value}</div>
                )
            }
        </div>
    );
}

export default Category;