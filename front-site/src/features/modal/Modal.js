import React from 'react';
import styles from './Modal.module.css';
import { ReactComponent as Close } from './close.svg';

function Modal({children, ico, close}) {
    return (
        <>
        <div className={styles.top}>
            <div className={styles.ico}>
                <img src={ico}/>
            </div>
            <div className={styles.ico} onClick={close}>
                <Close style={{stroke: '#000', fill: '#A5390B'}}/>
            </div>
        </div>
        <div className={styles.line}></div>
        <div className={styles.data}>
            {children}
        </div>
        </>
    );
}

export default Modal;