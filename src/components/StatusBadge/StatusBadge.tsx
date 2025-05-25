import React from 'react';
import styles from './StatusBadge.module.css';

import checkIcon from '../../assets/icons/check (4).svg';
import crossIcon from '../../assets/icons/x (1).svg';

interface StatusBadgeProps {
  status: 'confirmed' | 'notConfirmed';
}

export const StatusBadge: React.FC<StatusBadgeProps> = ({ status }) => {
  const isConfirmed = status === 'notConfirmed';

  return (
    <div className={`${styles.badge} ${isConfirmed ? styles.confirmed : styles.notConfirmed}`}>
      <img src={isConfirmed ? checkIcon : crossIcon} alt={isConfirmed ? 'Подтверждён' : 'Не подтверждён'} />
    </div>
  );
};
