import React, { createContext, useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'

export const AuthContext = createContext()

export const AuthProvider = ({ children }) => {
  const [authState, setAuthState] = useState({
    token: localStorage.getItem('access_token'), // Get token from local storage
    user: null,
  })

  const navigate = useNavigate()

  const login = (data) => {
    setAuthState({
      token: data.access_token,
      user: data.user,
    })
    localStorage.setItem('token', data.access_token)
    navigate('/home')
  }

  const logout = () => {
    console.log('Logging out...')
    setAuthState({
      token: null,
      user: null,
    })
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
    navigate('/login')
  }

  return (
    <AuthContext.Provider value={{ ...authState, login, logout }}>{children}</AuthContext.Provider>
  )
}

export default { AuthContext, AuthProvider }
