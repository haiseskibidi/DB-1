import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { api } from '../services/api'
import Header from '../components/Header'
import './HomePage.css'

function HomePage() {
  const navigate = useNavigate()
  const [search, setSearch] = useState('')
  const [recipes, setRecipes] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)
  const [page, setPage] = useState(1)
  const [totalPages, setTotalPages] = useState(1)

  useEffect(() => {
    loadStats()
  }, [])

  useEffect(() => {
    doSearch()
  }, [page])

  const loadStats = async () => {
    try {
      const data = await api.getStats()
      setStats(data)
    } catch (e) {
      console.error(e)
    }
  }

  const doSearch = async () => {
    setLoading(true)
    try {
      const data = await api.search({ q: search, limit: 12, page: page })
      setRecipes(data.results)
      setTotalPages(data.pages)
    } catch (e) {
      console.error(e)
    } finally {
      setLoading(false)
    }
  }

  const handleSearch = (e) => {
    e.preventDefault()
    setPage(1) 
    doSearch()
  }

  const handlePrevPage = () => {
    if (page > 1) setPage(p => p - 1)
  }

  const handleNextPage = () => {
    if (page < totalPages) setPage(p => p + 1)
  }

  return (
    <div className="home-page">
      <Header />
      
      <div className="hero-section">
        <h1>Кулинарная Книга</h1>
        <p>Поиск лучших рецептов с RussianFood, Povarenok и 1000.menu</p>
        
        <form onSubmit={handleSearch} className="search-form">
          <input
            type="text"
            placeholder="Например: Борщ, Салат Цезарь..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />
          <button type="submit">Найти</button>
        </form>

        {stats && (
          <div className="stats-badges">
            <span>📚 {stats.total_recipes} рецептов</span>
            <span>🍲 {stats.total_categories} категорий</span>
          </div>
        )}
      </div>

      <div className="results-container">
        {loading ? (
          <div className="loading">Загрузка...</div>
        ) : (
          <>
            <div className="recipes-grid">
              {recipes.map(recipe => (
                <div key={recipe.id} className="recipe-card">
                  <h3>{recipe.title}</h3>
                  <div className="recipe-meta">
                    <span className="category">{recipe.category}</span>
                    <span className="time">⏱ {recipe.cooking_time}</span>
                  </div>
                  <p className="desc">{recipe.description}</p>
                  <div className="card-footer">
                     <span className="source-count">Источников: {recipe.source_count}</span>
                     <Link to={`/recipe/${recipe.id}`} className="details-btn">Подробнее</Link>
                  </div>
                </div>
              ))}
            </div>
            
            {recipes.length > 0 && (
              <div className="pagination">
                <button onClick={handlePrevPage} disabled={page === 1}>← Назад</button>
                <span>Страница {page} из {totalPages}</span>
                <button onClick={handleNextPage} disabled={page === totalPages}>Вперед →</button>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  )
}

export default HomePage