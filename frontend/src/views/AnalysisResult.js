import React from 'react'

function AnalysisResult({ result }) {
  const keywords = result.key_words || {}

  return (
    <div className="container3">
      <h2 className="resh2">Results</h2>
      <p className="resurl">
        URL: <a href={result.url}>{result.url}</a>
      </p>

      <div className="group1">
        {/* Title Check */}
        <div
          className={`resultcard ${result.title_exist === true ? (result.title_length >= 55 && result.title_length <= 70 ? 'pass' : 'warning') : 'error'}`}
        >
          <div className="resultcard-details">
            <p className="text-title">Title check</p>
            <span>
              {result.title_exist === true
                ? result.title_length >= 55 && result.title_length <= 70
                  ? 'Passed'
                  : 'Warning'
                : "Didn't Pass"}
            </span>
            <p className="text-body">
              {result.title_exist === true
                ? result.title_length >= 55 && result.title_length <= 70
                  ? 'Good job, your page has a title and it is between 55 to 70 characters'
                  : 'Your title length should be between 55 to 70 characters'
                : 'Your page should have a title and it should be between 55 to 70 characters'}
            </p>
          </div>
        </div>

        {/* Description Check */}
        <div className={`resultcard ${result.description_exist === true ? 'pass' : 'error'}`}>
          <div className="resultcard-details">
            <p className="text-title">Description Check</p>
            <span>{result.description_exist === true ? 'Passed' : "Didn't Pass"}</span>
            <p className="text-body">
              {result.description_exist === true
                ? 'Your page contains a meta description'
                : "Your page doesn't contain a meta description"}
            </p>
          </div>
        </div>

        {/* H1 Tag Check */}
        <div
          className={`resultcard ${result.h1_exist === true ? (result.h1_count === true ? 'pass' : 'warning') : 'error'}`}
        >
          <div className="resultcard-details">
            <p className="text-title">H1 Tag Check</p>
            <span>
              {result.h1_exist === true
                ? result.h1_count === true
                  ? 'Passed'
                  : 'Warning'
                : "Didn't Pass"}
            </span>
            <p className="text-body">
              {result.h1_exist === true
                ? result.h1_count === true
                  ? 'Good job, your page contains only 1 h1 tag'
                  : "It's recommended for SEO to have only 1 (h1) tag in your page"
                : 'Your page should contain 1 (h1) tag'}
            </p>
          </div>
        </div>
      </div>
      <div className="group2">
        {/* H Tags Check */}
        <div className={`resultcard ${result.h_tags_order === true ? 'pass' : 'error'}`}>
          <div className="resultcard-details">
            <p className="text-title">H Tags Check</p>
            <span>{result.h_tags_order === true ? 'Passed' : 'Not Passed'}</span>
            <p className="text-body">
              {result.h_tags_order === true
                ? 'The h tags are in correct order (h1, h2, h3..etc)'
                : 'Your h tags should be ordered (h1, h2, h3..etc)'}
            </p>
          </div>
        </div>

        <div className={`resultcard ${result.img_alt === true ? 'pass' : 'error'}`}>
          <div className="resultcard-details">
            <p className="text-title">Image Alt Check</p>
            <span>{result.img_alt === true ? 'Passed' : 'Not Passed'}</span>
            <p className="text-body">It's recommended to have alt tags for all the images</p>
          </div>
        </div>
        <div className="resultcard">
          <div className="resultcard-details">
            <p className="text-title">Key Words</p>
            {Object.entries(keywords)
              .slice(0, 5)
              .map(([key, value], index) => (
                <p key={index} className="text-body">{`${key}: ${value}`}</p>
              ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default AnalysisResult
