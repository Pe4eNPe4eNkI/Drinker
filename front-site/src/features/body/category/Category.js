import React from 'react';
import { useDispatch, useSelector } from 'react-redux';
import styles from './Category.module.css';
import { setTag, selectTag } from '../bodySlice';

function Category() {
    const dispatch = useDispatch();
    const tag = useSelector(selectTag);
    const set = (tag) => (e) => dispatch(setTag(tag));
    const list = [
        {
            key: 'a',
            value: 'ПИВО',
        },
        {
            key: 'b',
            value: 'ЛИКЕР',
        },
        {
            key: 'c',
            value: 'ВИНО',
        },
        {
            key: 'd',
            value: 'БРЕНДИ',
        },
        {
            key: 'e',
            value: 'КОНЬЯК',
        },
    ];


    return (
        <div className={styles.container}>
            {list.map(({key, value}) =>
            <div
                key={key}
                className={styles.item}
                style={{color: key == tag ? '#000000' : '#878787'}}
                onClick={set(key)}

            >{value}</div>)}
        </div>
    );
}

export default Category;