import React from 'react';
import styles from './Item.module.css';

function Item({elem}) {
    return (
        <div className={styles.container}>
            <div>Номер заказа {elem.id}</div>
            <div>Заказал: {elem.user_info.name + ' ' + elem.user_info.surname + ' ' + elem.user_info.middlename}</div>
            <div>По адресу: {elem.address}</div>
            <div>Номер: {elem.user_info.phone}</div>
            <div className={styles.buttons}>
                {elem.status == 'onWay'
                ?
                <>
                    <button>Отмена</button>
                    <button>Доставлен</button>
                </>
                :
                <button>Принять</button>
                }
            </div>
        </div>
    );
}

export default Item;