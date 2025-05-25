import React from 'react';
import styles from './ConsumptionCard.module.css';

interface Props {
  type: 'average' | 'maximum';
  value: number;
}

export const ConsumptionCard: React.FC<Props> = ({ type, value }) => {
  const title =
    type === 'average' ? 'Среднесуточное потребление' : 'Максимальное потребление';

  return (
    <div className={styles.card}>
      <div className={styles.label}>{title}</div>
      <div className={styles.value}>{value} кВт*ч</div>
    </div>
  );
};
