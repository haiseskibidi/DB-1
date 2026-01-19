import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { api } from '../services/api'
import Header from '../components/Header'
import './RecipePage.css'

function RecipePage() {
  const { id } = useParams()
  const [recipe, setRecipe] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadRecipe()
  }, [id])

  const loadRecipe = async () => {
    setLoading(true)
    try {
      const data = await api.getRecipe(id)
      setRecipe(data)
    } catch (error) {
      console.error('Ошибка загрузки:', error)
    } finally {
      setLoading(false)
    }
  }

  if (loading) return <div className="loading">Загрузка...</div>
  if (!recipe) return <div className="error">Рецепт не найден</div>

  return (
    <div className="page-container">
      <Header />
      <div className="recipe-page">
        {recipe.image_url && (
          <div className="recipe-detail-image">
            <img src={recipe.image_url} alt={recipe.title} />
          </div>
        )}
        <div className="recipe-header">
           <Link to="/" className="back-link">← Назад</Link>
           <h1>{recipe.title}</h1>
           <span className="category-badge">{recipe.category}</span>
        </div>

        <div className="info-grid">
           <div className="info-item">
             <strong>Время приготовления:</strong>
             <p>{recipe.cooking_time || 'Не указано'}</p>
           </div>
           <div className="info-item">
             <strong>Сложность:</strong>
             <p>{recipe.difficulty || 'Не указана'}</p>
           </div>
        </div>

        <div className="section">
           <h3>Описание</h3>
           <p className="description-text">{recipe.description}</p>
        </div>

        <div className="section">
           <h3>Ингредиенты</h3>
           <ul className="ingredients-list">
             {recipe.ingredients.map(ing => (
               <li key={ing.id}>{ing.name}</li>
             ))}
           </ul>
        </div>

        <div className="section">
           <h3>Источники</h3>
           <div className="sources-list">
             {recipe.sources.map(s => (
               <a key={s.id} href={s.source_url} target="_blank" className="source-link">
                 {s.source_name} ↗
               </a>
             ))}
           </div>
        </div>
      </div>
    </div>
  )
}

export default RecipePage
