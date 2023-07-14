import React from 'react';
import styles from './Edit.module.css';
import { useSelector } from 'react-redux';
import { selectInfo, selectPassport } from '../userSlice';

function Edit() {
    return (<div className={styles.container}>
        <div className={styles.block}>
            <div>Данные:</div>
            <div><input type='text'/></div>
        </div>
        <div className={styles.block}>
            <div>Паспортные данные:</div>
        </div>
        <div className={styles.block}>
            <div>Карты:</div>
        </div>
    </div>);
}

export default Edit;