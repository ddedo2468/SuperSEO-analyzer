// SEOForm.js
import React, { useState, useEffect } from 'react'
import api from '../api'
import AnalysisResult from './AnalysisResult' // Assuming you have created this component
import { Helmet } from 'react-helmet'

function SEOForm() {
  const [url, setURL] = useState('')
  const [result, setResult] = useState(null)
  const [error, setError] = useState(null)
  const [urls, setUrls] = useState([])

  const handleSubmit = async (event) => {
    event.preventDefault()
    try {
      const response = await api.post(
        'api/create/',
        { url },
        {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('access_token')}`,
          },
        },
      )
      setResult(response.data)
      setURL('') // Clear input field after submission
    } catch (error) {
      console.error('There was an error!', error)
      setError(error.response ? error.response.data.error : 'An error occurred')
    }
  }

  return (
    <div>
      <Helmet>
        <title>SEO Analyzer</title>
      </Helmet>
      <div className="container5">
        <form onSubmit={handleSubmit} className="seo-form urlinput">
          <div className="form__group">
            <h1 className="h1analyzer"> SEO Analyzer </h1>
            <input
              type="text"
              className="form__input"
              placeholder="Enter URL"
              value={url}
              onChange={(e) => setURL(e.target.value)}
              required
            />
            <label className="form__label">Article URL</label>
            <button type="submit" className="nav-button analyzerbutton">
              Analyze
            </button>
          </div>
        </form>
      </div>
      {error && <p className="error">{error}</p>}
      {result && <AnalysisResult result={result} />}
    </div>
  )
}

export default SEOForm
