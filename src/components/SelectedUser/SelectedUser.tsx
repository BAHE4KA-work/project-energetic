import React from 'react';
import styles from './SelectedUser.module.css';

import userIcon from "../../assets/icons/user.svg"
import local from "../../assets/icons/local-two.svg"
import arrow from "../../assets/icons/arrow-down-right.svg"
import warning from "../../assets/icons/bx-error (1).svg"
import error from "../../assets/icons/bx-error-circle.svg"
import time from "../../assets/icons/time (1).svg"

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

  history: string[]; // добавляем поле с историей событий
}


interface UserDetailPanelProps {
  user: User;
  onBackClick: () => void;
}

export const SelectedUser: React.FC<UserDetailPanelProps> = ({ user, onBackClick }) => {
    return (
        <div className={styles.container}>
            <div className={styles.lpartCont}>
                <div className={styles.detailPanel}>
                    <div className={styles.infoCont}>
                        <img src={userIcon}/>
                        <div className={styles.infoText}>
                            <span className={styles.name}>{user.name}</span>
                            <span className={styles.address}> <img src={local}/>Адрес: {user.address}</span>
                            <span>ИНН: {user.inn}</span>
                            <span>Категория: физ. лицо</span>
                            <span>ИНН: {user.inn}</span>
                            {/* Добавьте дополнительные поля, если нужно */}
                        </div>
                    </div>
                    <button onClick={onBackClick} className={styles.backButton}>
                        Таблица потребителей <img src={arrow}/>
                    </button>
                </div>
                <div className={styles.lossPanel}>
                    <ul className={styles.lossList}>
                        <li>
                        Среднее потребление: {user.averageConsumptionValue} кВт·ч/день
                        <span className={styles.damageMultiplier}>В {user.damageMultiplier} раза выше нормы</span>
                        </li>
                        <li>Коэффициент заполненности: {user.fillRate}</li>
                        <li>Действующий тариф: {user.tariff} ₽/кВт·ч</li>
                    </ul>
                    <div className={styles.totalDamage}>
                        Ущерб: <b>{user.damagePerMonth.toLocaleString()} ₽/мес</b> ({user.damagePerYear.toLocaleString()} ₽/год)
                    </div>
                </div>
                <div className={styles.risks}>
                    <div className={styles.risksHeader}>
                        <img src={warning} alt="Warning" />
                        <span>Нарушения и риски</span>
                    </div>
                    <div className={styles.risksList}>
                        <span>{user.businessInfo}</span>
                        <span className={styles.mining}>Вероятность майнинга: {user.miningProbability}</span>
                        <span>{user.nightLoad}</span>
                        <span>{user.seasonalityAbsence}</span>
                    </div>
                </div>
                <div className={styles.recommendationsPanel}>
                    <div className={styles.recommendationsHeader}>
                        <img src={error} alt="error" />
                        <h3>Рекомендации</h3>
                    </div>
                    <ol className={styles.recommendationsList}>
                        {user.recommendations.map((rec, i) => (
                        <li key={i}>{rec}</li>
                        ))}
                    </ol>
                </div>
            </div>
            <div className={styles.historyCont}>
                <div className={styles.historyPanel}>
                    <span className={styles.tittleCont}>
                        <span className={styles.tittle}><img src={time} alt='clock'/>История</span> 
                    </span>
                    <ul className={styles.textCont}>
                        {user.history.map((event, i) => (
                        <li key={i}>{event}</li>
                        ))}
                    </ul>                  
                </div>
            </div>
        </div>
    );
};
