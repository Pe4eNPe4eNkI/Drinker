import React from 'react';
import styles from './Edit.module.css';
import { useSelector } from 'react-redux';
import { selectInfo, selectPassport, selectCards } from '../userSlice';

function Edit() {
    const info = useSelector(selectInfo);
    const passport = useSelector(selectPassport);
    const cards = useSelector(selectCards);

    return (<div className={styles.container}>
        <div className={styles.block}>
            <div>Данные:</div>
            <div><input type='text' placeholder='Имя' value={info.name}/></div>
            <div><input type='text' placeholder='Фамилия' value={info.surname}/></div>
            <div><input type='text' placeholder='Отчество' value={info.middlename}/></div>
            <div><input type='text' placeholder='Телефон' value={info.phone}/></div>
        </div>
        <div className={styles.block}>
            <div>Паспортные данные:</div>
            <div><input type='text' placeholder='Номер' value={passport.number}/></div>
            <div><input type='text' placeholder='Дата' value={passport.date}/></div>
            <button>Отправить</button>
        </div>
        <div className={styles.block}>
            <div>Карты:</div>
            {cards.map(({number}) => <div>{number}</div>)}
        </div>
        <div className={styles.block}>
            <div><input type='text' placeholder='Номер карты'/></div>
            <div><input type='text' placeholder='Дата'/></div>
            <div><input type='text' placeholder='cvv'/></div>
            <button>ОТправить</button>
        </div>
    </div>);
}

export default Edit;