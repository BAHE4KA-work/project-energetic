import React from 'react';
import styles from './StatsCard.module.css';

import userIcon from '../../assets/icons/users (3).svg';
import anomalyIcon from '../../assets/icons/bx-error.svg';
import fixIcon from '../../assets/icons/hammer-sickle.svg';

interface StatsCardProps {
  type: 'users' | 'anomalias' | 'fixed';
  value: number;
}

const typeMap = {
  users: {
    label: 'Количество потребителей',
    icon: userIcon,
  },
  anomalias: {
    label: 'Выявленные аномалии',
    icon: anomalyIcon,
  },
  fixed: {
    label: 'Устраненные нарушения',
    icon: fixIcon,
  },
};

export const StatsCard: React.FC<StatsCardProps> = ({ type, value }) => {
  const { label, icon } = typeMap[type];

  return (
    <div className={styles.card}>
      <div className={styles.label}>{label}</div>
      <div className={styles.valueBlock}>
        <img src={icon} alt={type} />
        <span className={styles.value}>{value.toLocaleString('ru-RU')}</span>
      </div>
    </div>
  );
};
