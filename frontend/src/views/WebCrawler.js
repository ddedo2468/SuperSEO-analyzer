import React, { useState } from 'react'
import api from '../api'
import KeywordsResult from './KeywordsResult' // Correct import with proper casing
import { Helmet } from 'react-helmet'

function WebCrawler() {
  const [keyword, setKeyword] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)

  const handleSubmit = async (event) => {
    event.preventDefault()
    setError(null) // Reset error state before making a new request
    try {
      const response = await api.post(
        'api/keywords/create/',
        { main_keyword: keyword },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        },
      )
      setResult(response.data)
      setKeyword('') // Clear input field after submission
    } catch (error) {
      console.error('There was an error!', error)
      if (error.response) {
        console.error('Response data:', error.response.data)
        console.error('Response status:', error.response.status)
        console.error('Response headers:', error.response.headers)
        setError(error.response.data.error)
      } else if (error.request) {
        console.error('Request data:', error.request)
        setError('No response received from server.')
      } else {
        console.error('Error message:', error.message)
        setError('An error occurred while setting up the request.')
      }
    }
  }

  return (
    <div>
      <Helmet>
        <title>Web Crawler</title>
      </Helmet>
      <div className="container5">
        <form onSubmit={handleSubmit} className="seo-form urlinput">
          <div className="form__group">
            <h1 className="h1analyzer">Web Crawler</h1>
            <input
              type="text"
              className="form__input"
              placeholder="Enter Main Keyword"
              value={keyword}
              onChange={(e) => setKeyword(e.target.value)}
              required
            />
            <label className="form__label">The main Keyword</label>
            <button type="submit" className="nav-button analyzerbutton">
              Analyze
            </button>
          </div>
        </form>
      </div>
      <div className="containKeys">
        {error && <p className="error">{error}</p>}
        {result && <KeywordsResult result={result} />}
      </div>
    </div>
  )
}

export default WebCrawler
