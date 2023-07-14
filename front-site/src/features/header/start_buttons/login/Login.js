import React from 'react';
import styles from './Login.module.css';

function Login({back}) {
    return ( <>
        <div className={styles.text}>Login</div>
        <div><input type='text' placeholder='login'/></div>
        <div><input type='password' placeholder='password'/></div>
        <button className='button'>LogIn</button>
        <button className='button' onClick={back}>Back</button>
    </> );
}

export default Login;