import React from 'react';
import styles from './TopBar.module.css';
import search from './SearchMagnifyingGlass.svg';
import { selectTag, setSearch, selectSearch } from '../bodySlice';
import { useDispatch, useSelector } from 'react-redux';
import { selectAccType } from '../../header/user/userSlice';
import { useState } from 'react';
import ReactModal from 'react-modal';
import Modal from '../../modal/Modal';
import plus from './plus.svg';
import AddItem from '../addItem/AddItem';

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
    const [mode, setMode] = useState('none')
    const dispatch = useDispatch();
    const tag = useSelector(selectTag);
    const accType = useSelector(selectAccType);
    const search_val = useSelector(selectSearch);

    return (
        <>
        <ReactModal 
            isOpen={mode == 'add'}
            onRequestClose={()=>setMode('none')}
            className="Modal"
            overlayClassName="Overlay"
        >
        <Modal ico={plus} close={() => setMode('none')}>
            <AddItem/>
        </Modal>
        </ReactModal>
        <div className={styles.topBar}>
            <div className={styles.title}>Категории</div>
            <div className={styles.whatSearch}>Показано: {whatShow(tag)}</div>
            {accType == 'admin' && <div className={styles.admin}><button onClick={()=>setMode('add')}>Добавить товар</button></div>}
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