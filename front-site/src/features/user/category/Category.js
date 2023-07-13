import React, { useState } from 'react';
import styles from './Category.module.css';

function Category() {
    const [mode, setMode] = useState('order');
    const set = (key) => (e) => setMode(key);
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