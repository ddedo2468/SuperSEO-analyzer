import React, { useContext } from 'react'
import { AuthContext } from '../context/AuthContext'
import { Link } from 'react-router-dom'
import logo from '../assets/images/logo.png'

const Navbar = () => {
  const { logout } = useContext(AuthContext)

  return (
    <nav className="navbar">
      <div className="nav-left">
        <img src={logo} alt="Logo" className="nav-logo" />
        <span className="nav-title">SEO Analyzer</span>
      </div>
      <ul className="nav-links">
        <li className="nav-item">
          <Link to="/home" className="nav-button">
            Home
          </Link>
        </li>
        <li className="nav-item">
          <button className="nav-button" onClick={logout}>
            Sign Out
          </button>
        </li>
      </ul>
    </nav>
  )
}
export default Navbar
