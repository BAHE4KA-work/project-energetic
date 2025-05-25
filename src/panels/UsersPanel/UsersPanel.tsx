import React, { useState } from 'react';
import styles from './UsersPanel.module.css';
import users from "../../assets/icons/Vector.svg";
import upload from "../../assets/icons/Vector (1).svg";
import { UserRow } from '../../components/UserRow/UserRow';
import { FilterPanel } from '../../components/FilterPanel/FilterPanel';
import { SelectedUser } from '../../components/SelectedUser/SelectedUser';

import { usersData } from '../../mocks/UserInfo';

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

  recommendations: string[];  // Новое поле
}


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

export const UsersPanel: React.FC = () => {
  const [selectedUser, setSelectedUser] = useState<User | null>(null);

  const onUserClick = (user: User) => {
    setSelectedUser(user);
  };

  const onBackClick = () => {
    setSelectedUser(null);
};

  return (
    <>
      {selectedUser ? (
        <SelectedUser user={selectedUser} onBackClick={() => setSelectedUser(null)}/>
      ) : (
        <div className={styles.container}>
          <div className={styles.containerTable}>
            <div className={styles.unloadTableCont}>
              <div className={styles.tittleCont}>
                <img src={users} alt="Users" />
                <span className={styles.tittle}>Таблица потребителей</span>
              </div>
              <button type='button' className={styles.uploadTable}>
                <img src={upload} alt="Upload" />
                <span className={styles.uploadText}>Выгрузить таблицу</span>
              </button>
            </div>
            <div className={styles.tableHeader}>
              <div className={styles.status}>Статус</div>
              <div className={styles.name}>ФИО</div>
              <div className={styles.inn}>ИНН</div>
              <div className={styles.address}>Адрес</div>
              <div className={styles.avgConsumption}>Среднесуточное <br /> потребление</div>
              <div className={styles.risk}>Уровень <br /> риска</div>
            </div>

            <div className={styles.UserRowCont}>
              {usersData.map((user, idx) => (
                <UserRow
                  key={idx}
                  {...user}
                  onClick={() => onUserClick(user)}
                />
              ))}
            </div>
          </div>

          <FilterPanel  />
        </div>
      )}
    </>
  );
};
