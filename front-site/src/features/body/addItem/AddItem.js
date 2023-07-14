import React from 'react';
import styles from './AddItem.module.css';

function AddItem() {
    return (
        <div className={styles.container}>
            <input type='text' placeholder='Наименование'/>
            <input type='text' placeholder='Цена'/>
            <input type='text' placeholder='ULR'/>
            <input type='text' placeholder='tag'/>
            <button>Создать</button>
        </div>
    );
}

export default AddItem;