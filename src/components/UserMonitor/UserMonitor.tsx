import React, { useState } from 'react';
import styles from './UserMonitor.module.css';

import userIcon from "../../assets/icons/user.svg";
import local from "../../assets/icons/local-two.svg";

interface User {
  status: 'confirmed' | 'notConfirmed';
  name: string;
  inn: string;
  address: string;
  avgConsumption: string;
  riskLevel: 'medium' | 'high';

  averageConsumptionValue: number;
  fillRate: number;
  tariff: number;
  damagePerMonth: number;
  damagePerYear: number;
  damageMultiplier: number;

  businessInfo: string;
  miningProbability: string;
  nightLoad: string;
  seasonalityAbsence: string;

  recommendations: string[];

  history: string[];
}

interface UserMonitorProps {
  user: User;
}

export const UserMonitor: React.FC<UserMonitorProps> = ({ user }) => {
  return (
    <div className={styles.container}>
      <div className={styles.detailPanel}>
        <div className={styles.infoCont}>
          <img src={userIcon} alt="User icon" />
          <div className={styles.infoText}>
            <span className={styles.name}>{user.name}</span>
            <span className={styles.address}>
              <img src={local} alt="Location icon" /> Адрес: {user.address}
            </span>
            <span>ИНН: {user.inn}</span>
            <span>Категория: физ. лицо</span>
            <span>ИНН: {user.inn}</span>
          </div>
        </div>
      </div>
    </div>
  );
};
