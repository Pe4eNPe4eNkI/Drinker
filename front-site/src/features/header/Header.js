import React from 'react';
import ReactModal from 'react-modal';
import { useState } from 'react';
import { UseSelector, useSelector } from 'react-redux/es/hooks/useSelector';
import styles from './Header.module.css';
import cart from './ShoppingCart.svg';
import user from './UserSquare.svg';
import bear_back from './HeaderColorStrip.jpg';
import logo from './logo.png';
import Modal from '../modal/Modal';
import Category from './user/category/Category';
import Separate from '../separate/Separate';
import RightSide from './user/right_side/RightSide';
import { selectUserLogin } from './headerSlice';
import StartButtons from './start_buttons/StartButton';

function Header() {
  const [mode, setMode] = useState('none');
  const is_login = useSelector(selectUserLogin);

  return (
    <>
    <div className={styles.container}>
      <div className={styles.inner}>
        <div className={styles.logo}>
          <img src={logo}/>
        </div>
        <div className={styles.title}>Drink bear, drinker!</div>
        <div className={styles.nav}>
          <div className={styles.ico} onClick={(e)=>setMode('cart')}>
            <img src={cart}/>
          </div>
          <div className={styles.ico} onClick={(e)=>setMode('user')}>
            <img src={user}/>
          </div>
        </div>
      </div>
    </div>
    <div className={styles.back}>
      <img src={bear_back}/>
      <div className={styles.top}></div>
    </div>

    <ReactModal 
        isOpen={mode == 'cart'}
        onRequestClose={()=>setMode('none')}
        className="Modal"
        overlayClassName="Overlay"
    >
      <Modal ico={cart} close={()=>setMode('none')}>
        {is_login ? 'a' : <StartButtons/>}
      </Modal>
    </ReactModal>

    <ReactModal 
        isOpen={mode == 'user'}
        onRequestClose={()=>setMode('none')}
        className="Modal"
        overlayClassName="Overlay"
    >
      <Modal ico={user} close={() => setMode('none')}>
        {
          is_login ? <>
            <Separate>
              <Category/>
              <RightSide/>
            </Separate>
          </> :
          <StartButtons/>
        }
      </Modal>
    </ReactModal>
    </>
  );
}

export default Header;