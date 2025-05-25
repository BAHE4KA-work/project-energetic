import React from 'react';
import styles from './SearchInput.module.css';
import searchIcon from '../../assets/icons/search.svg';

interface SearchInputProps {
  placeholder?: string;
  value: string;
  onChange: (value: string) => void;
}

export const SearchInput: React.FC<SearchInputProps> = ({ placeholder = 'Адрес', value, onChange }) => {
  return (
    <div className={styles.inputWrapper}>
      <img src={searchIcon} alt="search" className={styles.icon} />
      <input
        className={styles.input}
        type="text"
        placeholder={placeholder}
        value={value}
        onChange={(e) => onChange(e.target.value)}
      />
    </div>
  );
};
