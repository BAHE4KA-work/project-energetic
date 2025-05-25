import React from 'react';
import styles from './AnomalyCard.module.css';

interface AnomalyCardProps {
  type: 'critical' | 'suspicious';
  value: number;
}

export const AnomalyCard: React.FC<AnomalyCardProps> = ({ type, value }) => {
  const isCritical = type === 'critical';
  const label = isCritical ? 'Явные нарушения' : 'Подозрительные отклонения';

  return (
    <div className={styles.card}>
      <span className={styles.label}>{label}</span>
      <div className={styles.valueWrapper}>
        <div className={isCritical ? styles.redCircle : styles.yellowCircle}></div>
        <span className={styles.value}>{value.toLocaleString()}</span>
      </div>
    </div>
  );
};
