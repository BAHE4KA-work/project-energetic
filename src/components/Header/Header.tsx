import React from 'react';
import styles from './Header.module.css';

import logo from '../../assets/icons/Group 2 (1).svg'; // иконка "WE'LL BE 1st"
import avatarDefault from '../../assets/images/Avatar Image.png'; // заглушка, если нет фото
import background from "../../assets/images/Ellipse 1.png"
import { NavBar } from '../NavBar/NavBar';

type Tab = 'KPI' | 'Потребители' | 'ТНС-Монитор'

interface HeaderProps {
  avatarUrl?: string;
  initialActive?: Tab
  onActiveChange?: (activeTab: Tab) => void
  
}

export const Header: React.FC<HeaderProps> = ({avatarUrl, onActiveChange}) => {
  return (
    <header className={styles.header}>
        <div className={styles.shadowCont}><img className={styles.shadow} src={background}/></div>
        <div className={styles.lpart}>
            <div className={styles.left}>
                <img src={logo} alt="logo" className={styles.logo} />
                <span className={styles.title}>WattControl</span>
            </div>

            <NavBar onActiveChange={onActiveChange}/>
        </div>

        <div className={styles.profile}>
            <img
                src={avatarUrl || avatarDefault}
                alt="avatar"
                className={styles.avatar}
            />
        </div>
    </header>
  );
};
