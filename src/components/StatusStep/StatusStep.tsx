import React from 'react';
import styles from './StatusStep.module.css';

import startIconDone from '../../assets/icons/Frame 40104.svg';
import connectorIconPending from '../../assets/icons/Frame 40104 (1).svg';
import connectorIconConfirmed from '../../assets/icons/Frame 40104 (2).svg';
import connectorIconDone from '../../assets/icons/Frame 40104 (3).svg';
import endIconPending from '../../assets/icons/Frame 40104 (4).svg';
import endIconConfirmed from '../../assets/icons/Frame 40104 (5).svg';

interface StatusStepProps {
  stepType: 'start' | 'connector' | 'end';
  status: 'pending' | 'confirmed' | 'done';  // ожидание, подтверждено, пройдено
  text: string;
  time?: string; // отображается только при confirmed и done
  consumption?: string;
  communicationChannel?: string;
  executor?: string;
  executionDate?: string;
  violation?: string;
  recommendedTariff?: string;
  controlDate?: string;
}

export const StatusStep: React.FC<StatusStepProps> = ({
  stepType,
  status,
  text,
  time,
  consumption,
  communicationChannel,
  executor,
  executionDate,
  violation,
  recommendedTariff,
  controlDate,
}) => {
  // Выбор иконки в зависимости от stepType и status
  const getIcon = () => {
    if (stepType === 'start') {
      return <img className={styles.startIcon} src={startIconDone} alt="Start icon done" />;
    }
    if (stepType === 'connector') {
      if (status === 'pending') return <img src={connectorIconPending} alt="Connector pending" />;
      if (status === 'confirmed') return <img src={connectorIconConfirmed} alt="Connector confirmed" />;
      if (status === 'done') return <img src={connectorIconDone} alt="Connector done" />;
    }
    if (stepType === 'end') {
      if (status === 'pending') return <img src={endIconPending} alt="End pending" />;
      if (status === 'confirmed' || status === 'done') return <img src={endIconConfirmed} alt="End confirmed/done" />;
    }
    return null;
  };

  // Выбор цвета текста: фиолетовый для ожидания, черный для подтверждено/пройдено
  const textColorClass = status === 'pending' ? styles.textConfirmedDone : styles.textPending;  

  // Показывать время только для confirmed или done
  const showTime = status === 'confirmed' || status === 'done';

  return (
    <div className={styles.container}>
      <div>{getIcon()}</div>
      <div className={styles.content}>
        <div className={`${styles.text} ${textColorClass}`}>
          {text}
          {showTime && time && <span className={styles.time}>{time}</span>}
        </div>

        {/* Дополнительная информация */}
        <div className={styles.extraInfo}>
          {consumption && <p><b>Потребление:</b> {consumption}</p>}
          {communicationChannel && <p><b>Канал связи:</b> {communicationChannel}</p>}
          {executor && <p><b>Исполнитель:</b> {executor}</p>}
          {executionDate && <p><b>Дата выполнения:</b> {executionDate}</p>}
          {violation && <p><b>Нарушение:</b> {violation}</p>}
          {recommendedTariff && <p><b>Рекомендуемый тариф:</b> {recommendedTariff}</p>}
          {controlDate && <p><b>Дата контрольная:</b> {controlDate}</p>}
        </div>
      </div>
    </div>
  );
};
