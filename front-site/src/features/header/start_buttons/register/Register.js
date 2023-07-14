import React from 'react';
import styles from './Register.module.css';
import { useState } from 'react';
import { useDispatch } from 'react-redux';
import { register } from '../../headerSlice';

function Register({back}) {
    const [login, setLogin] = useState('');
    const [pass1, setPass1] = useState('');
    const [pass2, setPass2] = useState('');
    const dispatch = useDispatch();
    return ( <>
        <div>Register</div>
        <div><input type='text' value={login} onChange={(e)=>setLogin(e.target.value)} placeholder='login'/></div>
        <div><input type='password' value={pass1} onChange={(e)=>setPass1(e.target.value)} placeholder='password'/></div>
        <div><input type='password' value={pass2} onChange={(e)=>setPass2(e.target.value)} placeholder='repeat password'/></div>
        <button className='button' onClick={()=>{
            if (pass1 == pass2) {
                dispatch(register({login, password: pass1}));
            }
        }}>Register</button>
        <button className='button' onClick={back}>Back</button>
    </> );
}

export default Register;