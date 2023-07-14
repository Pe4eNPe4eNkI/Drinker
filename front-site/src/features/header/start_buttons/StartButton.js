import React, { useState } from 'react';
import styles from './StartButton.module.css';
import Login from './login/Login';
import Register from './register/Register';

function StartButtons() {
    const [mode, setMode] = useState('fork');
    let answer = <div>null</div>;

    if (mode == 'fork') {
        answer = <div className={styles.container}>
            <button className="button" onClick={(e)=>setMode('login')}>LogIn</button>
            <button className="button" onClick={(e)=>setMode('register')}>Register</button>
        </div>;
    } else if (mode == 'login') {
        answer = <div className={styles.container}>
            <Login back={()=>setMode('fork')}/>
        </div>;
    } else if (mode == 'register') {
        answer = <div className={styles.container}>
            <Register back={()=>setMode('fork')}/>
        </div>;
    }

    return (
        <>{answer}</>
    );
}

export default StartButtons;