import React from 'react';
import { UseSelector, useSelector } from 'react-redux/es/hooks/useSelector';
import styles from './TopBar.module.css';
import search from './SearchMagnifyingGlass.svg';
import { selectTag, setSearch, selectSearch } from '../bodySlice';
import { useDispatch } from 'react-redux';

function whatShow(tag) {
    let ans = '';

    switch(tag) {
        case 'a':
            ans = 'ПИВО';
            break;
        case 'b':
            ans = 'ЛИКЕР';
            break;
        case 'none':
            ans = 'ВСЕ';
            break;
    }

    return ans;
}

function TopBar() {
    const dispatch = useDispatch();
    const tag = useSelector(selectTag);
    const search_val = useSelector(selectSearch);
    return (
        <>
        <div className={styles.topBar}>
            <div className={styles.title}>Категории</div>
            <div className={styles.whatSearch}>Показано: {whatShow(tag)}</div>
            <div className={styles.searchWrapp}>
                <div className={styles.search}>
                    <div className={styles.searchIco}>
                        <img src={search}/>
                    </div>
                    <input className={styles.searchInput}
                           value={search_val}
                           placeholder='поиск'
                           onChange={(e) => dispatch(setSearch(e.target.value))}
                           />
                </div>
            </div>
        </div>
        <div className={styles.underline}></div>
        </>
    );
}

export default TopBar;