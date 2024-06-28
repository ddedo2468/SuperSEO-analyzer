import React, { useState, useEffect, useContext } from 'react'
import axios from 'axios'
import { AuthContext } from '../context/AuthContext'
import AnalysisResult from './AnalysisResult' // Assuming you have created this component
import api from '../api'

const SearchHistory = () => {
  const { token } = useContext(AuthContext) // Use the AuthContext to get the token
  const [data, setData] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)
  const [result, setResult] = useState(null)

  const handleRetrieve = async (urlToRetrieve) => {
    try {
      const response = await api.get(`api/${urlToRetrieve}`, {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`,
        },
      })
      setResult(response.data)
    } catch (error) {
      console.error('Failed to retrieve URL:', error)
    }
  }

  useEffect(() => {
    const fetchData = async () => {
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/', {
          headers: {
            Authorization: `Bearer ${token}`, // Include the token in the headers
          },
        })
        setData(response.data)
      } catch (error) {
        console.error('Error fetching data:', error)
        setError(error)
      } finally {
        setLoading(false)
      }
    }

    fetchData()
  }, [token]) // Ensure useEffect runs again if the token changes

  if (loading) {
    return <div>Loading...</div>
  }

  if (error) {
    return <div>Error: {error.message}</div>
  }

  return (
    <div>
      <h1 className="urlh">Search History</h1>
      <table className="table-container">
        <thead>
          <tr>
            <th>
              <h1>URL</h1>
            </th>
            <th>
              <h1>Analyze Time</h1>
            </th>
          </tr>
        </thead>
        <tbody>
          {data.map((urlData, index) => (
            <tr key={index}>
              <td>
                <button className="TableLink" onClick={() => handleRetrieve(urlData.url)}>
                  {urlData.url}
                </button>
              </td>
              <td>{new Date().toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
      {error && <p className="error">{error}</p>}
      {result && <AnalysisResult result={result} />}
    </div>
  )
}

export default SearchHistory
