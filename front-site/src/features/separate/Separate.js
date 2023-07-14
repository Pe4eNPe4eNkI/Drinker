import React from 'react';
import styles from './Separate.module.css';

function Separate({
    children
}) {
    return (
        <div className={styles.container}>
            {children}
        </div>
    );
}

export default Separate;