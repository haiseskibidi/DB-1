import { Link } from 'react-router-dom'
import './Header.css'

function Header() {
  return (
    <header className="header">
      <div className="container">
        <div className="header-content">
          <div className="logo">
            <Link to="/">
              <h1>🍳 CulinaryDB</h1>
            </Link>
          </div>
          <nav className="nav">
            <Link to="/" className="nav-link">Поиск</Link>
            <Link to="/stats" className="nav-link">Статистика</Link>
          </nav>
        </div>
      </div>
    </header>
  )
}

export default Header