import React from 'react';
import TopBar from './top_bar/TopBar';
import styles from './Body.module.css';
import Separate from '../separate/Separate';
import Gallery from './gallery/Gallery';
import Category from './category/Category';
import { useSelector } from 'react-redux';
import { selectAccType } from '../header/headerSlice';
import Courier from './courier/Courier';

function Body() {
    const accType = useSelector(selectAccType);

    return (
        <>
        {
            accType == 'courier'
            ?
            <Courier/>
            :
            <div className={styles.container}>
                <TopBar/>
                <Separate>
                    <Category/>
                    <Gallery/>
                </Separate>
            </div>
        }
        </>
    );
}

export default Body;