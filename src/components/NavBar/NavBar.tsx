import React, { useState, useEffect, useRef } from 'react'
import styles from './NavBar.module.css'

import devBoard from "../../assets/icons/Vector (2).svg"
import kpi from "../../assets/icons/analysis.svg"
import kpiActive from "../../assets/icons/analysis (1).svg"
import users from "../../assets/icons/users.svg"
import usersActiveI from "../../assets/icons/users (1).svg"
import setting from "../../assets/icons/package-search (1).svg"
import settingActive from "../../assets/icons/package-search (2).svg"

type Tab = 'KPI' | 'Потребители' | 'ТНС-Монитор'

interface NavBarProps {
  initialActive?: Tab
  onActiveChange?: (activeTab: Tab) => void
}

export const NavBar: React.FC<NavBarProps> = ({ initialActive = 'Потребители', onActiveChange }) => {
  const [activeTab, setActiveTab] = useState<Tab>(initialActive)
  const [highlightStyle, setHighlightStyle] = useState<{ left: number; width: number }>({ left: 0, width: 0 })

  const containerRef = useRef<HTMLDivElement>(null)
  const buttonsRef = useRef<Partial<Record<Tab, HTMLButtonElement | null>>>({})

  useEffect(() => {
    onActiveChange?.(activeTab)
  }, [activeTab, onActiveChange])

  const updateHighlight = () => {
    const button = buttonsRef.current[activeTab]
    const container = containerRef.current
    if (button && container) {
      const containerRect = container.getBoundingClientRect()
      const buttonRect = button.getBoundingClientRect()
      setHighlightStyle({
        left: buttonRect.left - containerRect.left,
        width: buttonRect.width,
      })
    }
  }

  useEffect(() => {
    updateHighlight()
    window.addEventListener('resize', updateHighlight)
    return () => window.removeEventListener('resize', updateHighlight)
  }, [activeTab])

  const tabs: Tab[] = ['KPI', 'Потребители', 'ТНС-Монитор']

  const getIcon = (tab: Tab, active: boolean) => {
    switch(tab) {
      case 'KPI': return <img src={active ? kpiActive : kpi} alt={tab} />
      case 'Потребители': return <img src={active ? usersActiveI : users} alt={tab} />
      case 'ТНС-Монитор': return <img src={active ? settingActive : setting} alt={tab} />
      default: return null
    }
  }

  return (
    <div className={styles.navbar} ref={containerRef}>
      <div className={styles.iconCircle}>
        <img src={devBoard} alt="devBoard" />
      </div>

      {/* Плашка-подсветка */}
      <div
        className={styles.highlight}
        style={{
          width: highlightStyle.width,
          transform: `translateX(${highlightStyle.left}px)`,
        }}
      />

      {tabs.map((tab) => {
        const isActive = activeTab === tab
        return (
          <button
            key={tab}
            ref={(el) => (buttonsRef.current[tab] = el)}
            className={`${styles.tabButton} ${isActive ? styles.active : ''}`}
            onClick={() => setActiveTab(tab)}
            type="button"
          >
            {getIcon(tab, isActive)}
            <span>{tab}</span>
          </button>
        )
      })}
    </div>
  )
}
