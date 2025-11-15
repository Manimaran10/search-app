import { Link, useLocation } from "react-router-dom";
import "../styles/global.css";

export default function Navbar() {
  const location = useLocation();

  return (
    <nav className="sidebar">
      <div className="sidebar-content">
        <div className="nav-item">
          <Link to="/" className={`nav-link ${location.pathname === '/' ? 'active' : ''}`}>
            <span className="nav-icon">🏠</span>
            Home
          </Link>
        </div>
        <div className="nav-item">
          <Link to="/knowledge" className={`nav-link ${location.pathname === '/knowledge' ? 'active' : ''}`}>
            <span className="nav-icon">📚</span>
            Knowledge Base
          </Link>
        </div>
      </div>
    </nav>
  );
}
