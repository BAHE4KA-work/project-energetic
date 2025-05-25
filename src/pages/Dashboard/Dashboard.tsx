import React, { useState } from 'react';
import { Header } from '../../components/Header/Header';
import { UsersPanel } from '../../panels/UsersPanel/UsersPanel';

import styles from "./dashboard.module.css"
import { KpiPanel } from '../../panels/KpiPanel/KpiPanel';
import { MonitorPanel } from '../../panels/MonitorPanel/MonitorPanel';

import { usersData } from '../../mocks/UserInfo';

export const Dashboard = () => {
  const [activeTab, setActiveTab] = useState<'KPI' | 'Потребители' | 'ТНС-Монитор'>('Потребители');

  const renderContent = () => {
    switch (activeTab) {
      case 'KPI':
        return <KpiPanel />;
        // return "KpiPanel"
      case 'Потребители':
        return <UsersPanel />;
      case 'ТНС-Монитор':
        return <MonitorPanel users={usersData} />;
        // return "ТНС-Монитор"
    }
  };

  return (
    <div className={styles.Cont}>
      <Header onActiveChange={setActiveTab} />
      <div>{renderContent()}</div>
    </div>
  );
};
