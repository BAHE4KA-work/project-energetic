import React, { useState, useEffect, useRef  } from 'react';
import styles from './KpiPanel.module.css';
import clockIcon from '../../assets/icons/time.svg';
import uploadIcon from '../../assets/icons/upload (1).svg';
import up from '../../assets/icons/up.svg';
import down from '../../assets/icons/down.svg';
import { StatsCard } from '../../components/StatsCard/StatsCard';
import { EnergyLineChart } from '../../components/EnergyLineChart/EnergyLineChart';

import { useInView } from 'react-intersection-observer';
import { AnomalyCard } from '../../components/AnomalyCard/AnomalyCard';
import { ViolationsBarChart } from '../../components/ViolationsBarChart/ViolationsBarChart';
import { DeviationBarChart } from '../../components/DeviationBarChart/DeviationBarChart';
import { SearchInput } from '../../components/SearchInput/SearchInput';
import { StatsCardSecond } from '../../components/StatsCardSecond/StatsCardSecond';
import { ConsumptionCard } from '../../components/ConsumptionCard/ConsumptionCard';
import { MapMarkers } from '../../components/MapMarkers/MapMarkers';

import { data } from '../../mocks/UserCharts';
import { energyData } from '../../mocks/EnergyData';
import { violationsData } from '../../mocks/VolationsData';
import { deviationData } from '../../mocks/DeviationData';


const periods = ['Год', 'Месяц', 'Неделя', 'День'];

interface PointData {
  id: number;
  lat: number;
  lng: number;
  color: 'red' | 'yellow';
  label?: string;
  address: string;
  deviation: number;
  riskLevel: 'high' | 'medium';
  checks: number;
  consumption?: { week: number; consumption: number }[]; // индивидуальные данные
  normalAverage?: number; // линия нормы
  violationDeviation?: { range: string; count: number }[];
  weeklyViolations?: { range: number; count: number }[];
}

export const KpiPanel: React.FC = () => {
  const [dropdownOpen, setDropdownOpen] = useState(false);
  const [selectedPeriod, setSelectedPeriod] = useState('Месяц');
  const [activePoint, setActivePoint] = useState<PointData | null>(null);


  const handleFileUpload = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      console.log('Загружен файл:', file.name);
    }
  };

  const { ref: chartRef, inView: isChartVisible } = useInView({
    
  threshold: 0.3          // 30% элемента должно быть видно
});

const { ref: barChartRef, inView: isBarChartVisible } = useInView({
  triggerOnce: true,
  threshold: 0.3
});

const [chartKey, setChartKey] = useState(0);
const lastActivePointIdRef = useRef<number | null>(null);

useEffect(() => {
  let timeout: ReturnType<typeof setTimeout>;


  if (isChartVisible && activePoint?.id !== lastActivePointIdRef.current) {
    timeout = setTimeout(() => {
      setChartKey(prev => prev + 1);
      lastActivePointIdRef.current = activePoint?.id ?? null;
    }, 150); // чуть сгладить реакцию
  }

  return () => clearTimeout(timeout);
}, [isChartVisible, activePoint]);


const [searchQuery, setSearchQuery] = useState('');


  return (
    <div className={styles.container}>
        <div className={styles.panelBtn}>
        <div className={styles.buttonGroup}>
            <div className={styles.btnInputCont}>
              <div className={styles.dropdownWrapper}>
              <button
                  className={styles.button}
                  type='button'
                  onClick={() => setDropdownOpen(!dropdownOpen)}
              >
                  <img src={clockIcon} alt="icon" />
                  {selectedPeriod}
                  <img src={dropdownOpen ? up : down} alt="arrow" />
              </button>
              {dropdownOpen && (
                  <div className={styles.dropdown}>
                  {periods.map((p) => (
                      <div
                      key={p}
                      className={styles.dropdownItem}
                      onClick={() => {
                          setSelectedPeriod(p);
                          setDropdownOpen(false);
                      }}
                      >
                      {p}
                      </div>
                  ))}
                  </div>
              )}
              </div>

              {activePoint ? (
                <button
                  className={styles.selectedPointBtn}
                  onClick={() => {
                    setActivePoint(null);
                    setSearchQuery('');
                  }}
                >
                  <span>{activePoint.address}</span> ✕
                </button>
              ) : (
                <SearchInput value={searchQuery} onChange={setSearchQuery} />
              )}

            </div>

            <label className={styles.button}>
            <img src={uploadIcon} alt="upload" />
            Выгрузить
            <input
                type="file"
                style={{ display: 'none' }}
                onChange={handleFileUpload}
            />
            </label>
        </div>
        </div>
        
        <div className={styles.MapStatCont}>
            <MapMarkers
              points={data}
              activePointId={activePoint?.id || null}
              onPointClick={(point) => {
                setActivePoint(point);
                setSearchQuery(point.label || '');
              }}
            />

          <div className={styles.statCont}>
            {activePoint ? (
              <>
                <StatsCardSecond type="deviation" value={activePoint.deviation} />
                <StatsCardSecond type="risk" riskLevel={activePoint.riskLevel} />
                <StatsCardSecond type="checks" value={activePoint.checks} />
              </>
            ) : (
              <>
                <StatsCard type="users" value={949000} />
                <StatsCard type="anomalias" value={3520} />
                <StatsCard type="fixed" value={604} />
              </>
            )}
        </div>
        </div>
        <div ref={chartRef} style={{ minHeight: 500 }}>
            {isChartVisible && 
                <div className={styles.graphsContainer}>
                    <div className={styles.graphsCont}>
                        <EnergyLineChart
                          key={chartKey}
                          data={activePoint?.consumption || energyData}
                          normalAverage={activePoint?.normalAverage}
                        />
                        <div className={styles.cardsContainer}>
                          {activePoint ? (
                            <div className={styles.cardsCont}>
                              <ConsumptionCard type="average" value={36} />
                              <ConsumptionCard type="maximum" value={50} />
                            </div>
                          ) : (
                            <div className={styles.cardsCont}>
                              <AnomalyCard type="critical" value={1145} />
                              <AnomalyCard type="suspicious" value={1700} />
                            </div>
                          )}
                        </div>  
                    </div>
                   <div ref={barChartRef}>
                        {isBarChartVisible && (
                            <div className={styles.barChartsCont}>
                                <ViolationsBarChart
                                  data={activePoint?.weeklyViolations ?? violationsData}
                                />
                                <DeviationBarChart
                                  data={activePoint?.violationDeviation || deviationData}
                                  isUserSpecific={!!activePoint}
                                />
                            </div>
                        )}
                    </div>
                </div>}
        </div>

    </div>
  );
};
