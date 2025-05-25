import React from 'react';
import styles from './UserRow.module.css';
import { StatusBadge } from '../StatusBadge/StatusBadge';

import high from "../../assets/icons/marker.svg"
import medium from "../../assets/icons/marker (1).svg"

interface UserRowProps {
  status: 'confirmed' | 'notConfirmed';
  name: string;
  inn: string;
  address: string;
  avgConsumption: string;
  riskLevel: 'medium' | 'high';
  onClick?: () => void;
}

export const UserRow: React.FC<UserRowProps> = ({
  status,
  name,
  inn,
  address,
  avgConsumption,
  riskLevel,
  onClick
}) => {

  return (
    <div className={styles.row} onClick={onClick}>
        <div className={styles.statusIcon}>
            <StatusBadge status={status} />
        </div>
        <div className={`${styles.cell} ${styles.name}`}>{name}</div>
        <div className={`${styles.cell} ${styles.inn}`}>{inn}</div>
        <div className={`${styles.cell} ${styles.address}`}>{address}</div>
        <div className={`${styles.cell} ${styles.avgConsumption}`}>{avgConsumption}</div>
        <div className={`${styles.cell} ${styles.riskLevel}`}>
            <img src={riskLevel === "high" ? high : medium}/>
        </div>
    </div>
  );
};
