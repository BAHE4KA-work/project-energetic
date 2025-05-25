import React, { useState } from 'react';
import styles from './FilterPanel.module.css';

import filter from "../../assets/icons/Group.svg"
import down from "../../assets/icons/down.svg"
import up from "../../assets/icons/up.svg"
import high from "../../assets/icons/marker.svg"
import medium from "../../assets/icons/marker (1).svg"
import check from "../../assets/icons/check (1).svg"

interface FilterPanelProps {
  onApply?: (filters: any) => void;

}

const streetOptions = ['Улица 1', 'Улица 2', 'Улица 3', 'Улица 4', 'Улица 5'];

export const FilterPanel: React.FC<FilterPanelProps> = ({ onApply }) => {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [selectedStreet, setSelectedStreet] = useState('Улица');
  const [filters, setFilters] = useState({
    riskRed: false,
    riskYellow: false,
    statusConfirmed: false,
    mining: false,
  });

  const toggleCheckbox = (key: string) => {
    setFilters((prev) => ({ ...prev, [key]: !prev[key] }));
  };

  const handleApply = () => {
    onApply(filters);
  };

  return (
    <div className={styles.panel}>
        <div className={styles.header}>
            <img src={filter} alt="filter" />
            <span>Фильтры</span>
        </div>

        <div className={styles.dropdown}>
            <div className={styles.buttonCont}>
                <button onClick={() => setDropdownOpen(!dropdownOpen)} className={styles.dropdownButton}>
                    {selectedStreet} <img src={dropdownOpen ? up : down}/>
                </button>
            </div>
            {dropdownOpen && (
            <div className={`${styles.dropdownList} ${dropdownOpen ? styles.open : styles.closed}`}>
                    {streetOptions.map((street) => (
                    <div
                        key={street}
                        className={styles.dropdownItem}
                        onClick={() => {
                        setSelectedStreet(street);
                        setDropdownOpen(false);
                        }}
                    >
                        {street}
                    </div>
                ))}
            </div>
            )}
        </div>

        <div className={styles.section}>
            <div className={styles.label}>Уровень риска</div>
           <label className={styles.checkboxRow}>
                <div className={styles.checkboxText}>
                    <img src={high} />
                    <span>Явные нарушения</span>
                </div>
                <input
                    type="checkbox"
                    className={styles.customCheckbox}
                    checked={filters.riskRed}
                    onChange={() => toggleCheckbox('riskRed')}
                />
            </label>
            <label className={styles.checkboxRow}>
                <div className={styles.checkboxText}>
                    <img src={medium} />
                    <span>Подозрительные отклонения</span>
                </div>
                <input
                    type="checkbox"
                    className={styles.customCheckbox}
                    checked={filters.riskYellow}
                    onChange={() => toggleCheckbox('riskYellow')}
                />
            </label>
        </div>

        <div className={styles.section}>
            <div className={styles.label}>Статус</div>
            <label className={styles.checkboxRow}>
                <div className={styles.checkboxTextB}>
                    <span>Подтверждённый статус</span>
                </div>
                <input
                    type="checkbox"
                    className={styles.customCheckbox}
                    checked={filters.statusConfirmed}
                    onChange={() => toggleCheckbox('statusConfirmed')}
                />
            </label>
            
        </div>

        <div className={styles.section}>
            <div className={styles.label}>Подозрительная активность</div>
            <label className={styles.checkboxRow}>
                <div className={styles.checkboxTextB}>
                    <span>Признаки майнинга</span>
                </div>
                <input
                    type="checkbox"
                    className={styles.customCheckbox}
                    checked={filters.mining}
                    onChange={() => toggleCheckbox('mining')}
                />
            </label>
      </div>

      <button className={styles.applyBtn} onClick={handleApply}>
        <img src={check}/>
        <span className={styles.applyBtnText}>Применить</span>
      </button>
    </div>
  );
};
