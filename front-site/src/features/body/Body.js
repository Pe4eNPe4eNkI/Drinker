import React from 'react';
import TopBar from './top_bar/TopBar';
import styles from './Body.module.css';
import Separate from '../separate/Separate';
import Gallery from './gallery/Gallery';
import Category from './category/Category';

function Body() {
    return (
        <div className={styles.container}>
            <TopBar/>
            <Separate>
                <Category/>
                <Gallery/>
            </Separate>
        </div>
    );
}

export default Body;