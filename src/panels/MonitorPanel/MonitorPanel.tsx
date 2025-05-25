import React, { useState } from 'react';
import styles from './MonitorPanel.module.css';

import search from "../../assets/icons/search (1).svg";
import { UserMonitor } from '../../components/UserMonitor/UserMonitor';
import { StatusStep } from '../../components/StatusStep/StatusStep';

interface User {
  status: 'confirmed' | 'notConfirmed';
  name: string;
  inn: string;
  address: string;
  avgConsumption: string;
  riskLevel: 'medium' | 'high';

  // другие поля по необходимости
}

interface MonitorPanelProps {
  users: User[];
}

export const MonitorPanel: React.FC<MonitorPanelProps> = ({ users }) => {
  const [selectedInn, setSelectedInn] = useState<string | null>(null);
  const selectedUser = users.find(user => user.inn === selectedInn) || null;

  const [text, setText] = useState('');
  return (
    <div className={styles.Cont}>
      <div className={styles.container}>
        <div className={styles.searchBar}>
          <img src={search} alt="Поиск" className={styles.icon} />
          <input
            type="text"
            placeholder={"Адрес"}
            className={styles.searchInput}
            value={text}
            onChange={(e) => setText(e.target.value)}
          />
        </div>

        <div className={styles.tableHeader}>
          <div className={styles.columnName}>ФИО</div>
          <div className={styles.columnInn}>ИНН</div>
          <div className={styles.columnAddress}>Адрес</div>
        </div>

        <div className={styles.tableBody}>
          {users.map((user, index) => (
            <div
              key={index}
              className={styles.tableRow}
              onClick={() => setSelectedInn(user.inn)}
              role="button"
              tabIndex={0}
              onKeyPress={(e) => { if (e.key === 'Enter') setSelectedInn(user.inn); }}
            >
              <div className={styles.columnName}>{user.name}</div>
              <div className={styles.columnInn}>{user.inn}</div>
              <div className={styles.columnAddress}>{user.address}</div>
            </div>
          ))}
        </div>

      </div>

      <div className={styles.rpartCont}>
        {selectedUser ? (
          <div className={styles.rpart}>
            <UserMonitor
              user={selectedUser}
              onBackClick={() => setSelectedInn(null)}
            />

            <div className={styles.statusStepCont}>
              <StatusStep stepType='start' status='done' text='Выявлены аномалии' consumption="36 кВт·ч/день при норме 12 кВт·ч/день" time="05.02.2025"/>
              <StatusStep stepType='connector' status='done' text='Направлено уведомление' communicationChannel="Телефон" time="05.02.2025"/>
              <StatusStep stepType='connector' status='confirmed' text='Назначена очная проверка'  executor="Иванов И.И." executionDate="05.02.2025" time="05.02.2025"/>
              <StatusStep stepType='connector' status='pending' text='Подтверждено нарушение'  violation="Повышенная ночная нагрузка" />
              <StatusStep stepType='connector' status='pending' text='Переход на другой тариф'  recommendedTariff="4.28 ₽/кВт·ч" controlDate="10.02.2025" />
              <StatusStep stepType='end' status='pending' text='Контроль через месяц'  controlDate="10.02.2025" />
            </div>
          </div>
          ) : (
            <span className={styles.findUserText}>
              Для показа информации, выберите ячейку в таблице
            </span>
          )}
      </div>
    </div>
  );
};
