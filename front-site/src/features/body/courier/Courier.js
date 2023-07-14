import React from 'react';
import styles from './Courier.module.css';
import List from './list/List';

function Courier() {
    return (
        <>
            <div className={styles.line}></div>
            <List type='onWay'/>
            <div className={styles.line}></div>
            <List type='assembling'/>
        </>
    );
}

export default Courier;