import { useState, useEffect } from 'react'
import { api } from '../services/api'
import Header from '../components/Header'
import './StatsPage.css'

function StatsPage() {
  const [stats, setStats] = useState(null)

  useEffect(() => {
    api.getStats().then(setStats).catch(console.error)
  }, [])

  if (!stats) return <div className="loading">Загрузка...</div>

  return (
    <div className="page-container">
      <Header />
      <div className="stats-page">
        <h1>Статистика базы данных</h1>
        
        <div className="stats-grid">
          <div className="stat-card">
            <h3>Всего рецептов</h3>
            <div className="number">{stats.total_recipes}</div>
          </div>
          <div className="stat-card">
            <h3>Категорий</h3>
            <div className="number">{stats.total_categories}</div>
          </div>
        </div>

        <div className="charts-section">
          <div className="chart-col">
            <h3>По источникам</h3>
            <ul className="stats-list">
              {Object.entries(stats.recipes_by_source).map(([name, count]) => (
                <li key={name}>
                  <span>{name}</span>
                  <strong>{count}</strong>
                </li>
              ))}
            </ul>
          </div>

          <div className="chart-col">
            <h3>Топ категорий</h3>
            <ul className="stats-list">
              {stats.top_categories.map((c, i) => (
                <li key={i}>
                  <span>{c.category}</span>
                  <strong>{c.count}</strong>
                </li>
              ))}
            </ul>
          </div>

          <div className="chart-col">
            <h3>Популярные ингредиенты</h3>
            <ul className="stats-list">
              {stats.top_ingredients.map((c, i) => (
                <li key={i}>
                  <span>{c.ingredient}</span>
                  <strong>{c.count}</strong>
                </li>
              ))}
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default StatsPage