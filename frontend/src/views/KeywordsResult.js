import React, { useState, useEffect } from 'react'
import { GoogleGenerativeAI } from '@google/generative-ai'
import ReactMarkdown from 'react-markdown' // Import react-markdown

function KeywordsResult({ result }) {
  const keywords = result.results || []
  const [articleStructure, setArticleStructure] = useState(null)

  useEffect(() => {
    const generateArticleStructure = async () => {
      if (!result.main_keyword || !keywords.length) {
        return // Handle missing data gracefully
      }

      // Initialize GoogleGenerativeAI with your API key (replace with yours)
      const genAI = new GoogleGenerativeAI(import.meta.env.VITE_API_KEY) // Use environment variable

      try {
        const model = await genAI.getGenerativeModel({ model: 'gemini-1.5-flash' }) // Specify the model

        const prompt = `act as seo specialist, I want to write an article about, the ${result.main_keyword}. I want the article to have some of these keywords: ${keywords.join(', ')}. Give me the article outline i should use`

        // Use `generateText` for text generation
        const result2 = await model.generateContent(prompt)
        const response = await result2.response
        setArticleStructure(response.text)
      } catch (error) {
        console.error('Error generating article structure:', error)
      }
    }

    generateArticleStructure()
  }, [result]) // Re-run useEffect when result changes

  return (
    <>
      <h2 className="h1topk">Top Keywords</h2>
      <div>
        <ul className="kwul">
          {keywords.map((keyword, index) => (
            <li key={index} className="kwli">
              {keyword}
            </li>
          ))}
        </ul>
      </div>
      {articleStructure && (
        <div>
          <h2 className="geminih2"> Suggested Points to Write Your Article </h2>
          <div className="gemini">
            {/* Use react-markdown to render the article structure */}
            <ReactMarkdown>{articleStructure}</ReactMarkdown>
          </div>
        </div>
      )}
      <style>{`
        .article-structure {
          margin-top: 20px;
          padding: 20px;
          background-color: #f5f5f5;
          border-radius: 5px;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          font-family: Arial, sans-serif;
          font-size: 1.5rem;
        }
        .geminih2 {
          margin: 25px 0;
          text-align: center;
        }
        .gemini{
          text-align: center;
        }
        .gemini ul {
          list-style-type: none;
        }
      `}</style>
    </>
  )
}

export default KeywordsResult



/* import React, { useState, useEffect } from 'react'
import { GoogleGenerativeAI } from '@google/generative-ai'
import ReactHtmlParser from 'html-react-parser'

function KeywordsResult({ result }) {
  const keywords = result.results || []
  const [articleStructure, setArticleStructure] = useState(null)

  useEffect(() => {
    const generateArticleStructure = async () => {
      if (!result.main_keyword || !keywords.length) {
        return // Handle missing data gracefully
      }

      // Initialize GoogleGenerativeAI with your API key (replace with yours)
      const genAI = new GoogleGenerativeAI(import.meta.env.VITE_API_KEY) // Use environment variable

      try {
        const model = await genAI.getGenerativeModel({ model: 'gemini-1.5-flash' }) // Specify the model

        const prompt = `act as seo specialist, I want to write an article about, the ${result.main_keyword}. I want the article to have some of these keywords: ${keywords.join(', ')}. Give me the article outline i should use`



        // Use `generateText` for text generation
        const result2 = await model.generateContent(prompt)
        const response = await result2.response
        setArticleStructure(response.text)
      } catch (error) {
        console.error('Error generating article structure:', error)
      }
    }

    generateArticleStructure()
  }, [result]) // Re-run useEffect when result changes

  return (
    <>
      <h2 className="h1topk">Top Keywords</h2>
      <div>
        <ul className="kwul">
          {keywords.map((keyword, index) => (
            <li key={index} className="kwli">
              {keyword}
            </li>
          ))}
        </ul>
      </div>
      {articleStructure && (
        <div>
          <h2 className="geminih2"> Suggested Points to Write Your Article </h2>
          <div className="gemini">
            <pre>{ReactHtmlParser(articleStructure)}</pre>
          </div>
        </div>
      )}
      <style>{`
        .article-structure {
          margin-top: 20px;
          padding: 20px;
          background-color: #f5f5f5;
          border-radius: 5px;
          box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
          font-family: Arial, sans-serif;
          font-size: 1.5rem;
        }
        .geminih2 {
          margin: 25px 0;
          text-align: center;
        }
        .gemini{
          text-align: center;
        }
        .gemini ul {
          list-style-type: none;
        }
      `}</style>
    </>
  )
}

export default KeywordsResult

/*import React, { useState, useEffect } from 'react'
import { GoogleGenerativeAI } from '@google/generative-ai'
import parse from 'html-react-parser'

function KeywordsResult({ result }) {
  const keywords = result.results || []
  const [articleStructure, setArticleStructure] = useState(null)

  useEffect(() => {
    const generateArticleStructure = async () => {
      if (!result.main_keyword || !keywords.length) {
        return // Handle missing data gracefully
      }

      // Initialize GoogleGenerativeAI with your API key (replace with yours)
      const genAI = new GoogleGenerativeAI('AIzaSyDNU6Xov5UIYApMYy9YgSCYnPMAEe9tLck') // Use environment variable

      try {
        const model = await genAI.getGenerativeModel({ model: 'gemini-1.5-flash' }) // Specify the model

        const prompt = `act as seo specialist, I want to write an article about, the ${result.main_keyword}. I want the article to have some of these keywords: ${keywords.join(', ')}. Give me the article main points i should talk about.
        return html structure as example <h2> main poinr </h2> <ul> <li> one or 2 points about this main point </li> </ul>with only the tags i should put inside the body, don't include body tag or head tag or html tag`

        // Use `generateText` for text generation
        const result2 = await model.generateContent(prompt)
        const response = await result2.response
        setArticleStructure(response.text)
      } catch (error) {
        console.error('Error generating article structure:', error)
      }
    }

    generateArticleStructure()
  }, [result]) // Re-run useEffect when result changes

  return (
    <>
      <h2 className="h1topk">Top Keywords</h2>
      <div>
        <ul className="kwul">
          {keywords.map((keyword, index) => (
            <li key={index} className="kwli">
              {keyword}
            </li>
          ))}
        </ul>
      </div>
      {articleStructure && (
        <div>
          <pre>{parse(articleStructure)}</pre>
        </div>
      )}
    </>
  )
}

export default KeywordsResult
*/

/*import React from 'react'

function KeywordsResult({ result }) {
  const keywords = result.results || []

  return (
    <>
      <h2 className="h1topk">Top Keywords</h2>
      <div>
        <ul className="kwul">
          {keywords.map((keyword, index) => (
            <li key={index} className="kwli">
              {keyword}
            </li>
          ))}
        </ul>
      </div>
    </>
  )
}

export default KeywordsResult*/
