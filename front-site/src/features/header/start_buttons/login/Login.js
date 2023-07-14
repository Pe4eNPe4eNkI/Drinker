import React from 'react';
import styles from './Login.module.css';
import { auth } from '../../headerSlice';
import { useDispatch } from 'react-redux';
import { useState } from 'react';


function Login({back}) {
    const [login, setLogin] = useState('');
    const [password, setPass] = useState('');
    const dispatch = useDispatch();
    return ( <>
        <div className={styles.text}>Login</div>
        <div><input type='text' value={login} onChange={(e)=>setLogin(e.target.value)} placeholder='login'/></div>
        <div><input type='password' value={password} onChange={(e)=>setPass(e.target.value)} placeholder='password'/></div>
        <button className='button' onClick={(e)=>dispatch(auth({login, password}))}>LogIn</button>
        <button className='button' onClick={back}>Back</button>
    </> );
}

export default Login;