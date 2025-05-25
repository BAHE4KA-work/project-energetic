import React from 'react';
import styles from './StatsCardSecond.module.css';
import checkIcon from '../../assets/icons/circle-check-big.svg';
import redIconUrl from '../../assets/icons/marker.svg';
import yellowIconUrl from '../../assets/icons/marker (1).svg';

type Type = 'deviation' | 'risk' | 'checks';
type RiskLevel = 'high' | 'medium';

interface RiskCardProps {
  type: Type;
  value: number | string;
  riskLevel?: RiskLevel; // только для типа risk
}

export const StatsCardSecond: React.FC<RiskCardProps> = ({ type, value, riskLevel }) => {
  return (
    <div className={styles.card}>
      {type === 'deviation' && (
        <div className={styles.deviation}>
          <div className={styles.label}>Отклонение от нормы</div>
          <div className={styles.redValue}>{value}%</div>
        </div>
      )}

      {type === 'risk' && (
        <>
          <div className={styles.label}>Уровень риска</div>
          <div className={styles.riskWrapper}>
            <img
              src={riskLevel === 'high' ? redIconUrl : yellowIconUrl}
              className={styles.riskIcon}
              alt="risk"
            />
            <span className={styles.riskText}>
              {riskLevel === 'high' ? 'Явные\nнарушения' : 'Подозрительные\nотклонения'}
            </span>
          </div>
        </>
      )}

      {type === 'checks' && (
        <>
          <div className={styles.label}>Количество проверок</div>
          <div className={styles.riskWrapper}>
            <img src={checkIcon} className={styles.riskIcon} alt="check" />
            <span className={styles.valueText}>{value}</span>
          </div>
        </>
      )}
    </div>
  );
};
