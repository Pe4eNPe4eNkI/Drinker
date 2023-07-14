import React from 'react';
import styles from './Register.module.css';

function Register({back}) {
    return ( <>
        <div>Register</div>
        <div><input type='text' placeholder='login'/></div>
        <div><input type='password' placeholder='password'/></div>
        <div><input type='password' placeholder='repeat password'/></div>
        <button className='button'>Register</button>
        <button className='button' onClick={back}>Back</button>
    </> );
}

export default Register;