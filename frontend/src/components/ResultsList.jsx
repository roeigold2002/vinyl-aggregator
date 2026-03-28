import React, { useState } from 'react'
import PriceComparison from './PriceComparison'
import '../styles/components.css'

export const ResultsList = ({ results, loading, error }) => {
  const [expandedId, setExpandedId] = useState(null)

  if (loading) {
    return <div className="loading">Loading results...</div>
  }

  if (error) {
    return <div className="error">Error: {error}</div>
  }

  if (results.length === 0) {
    return <div className="no-results">No records found. Try a different search.</div>
  }

  return (
    <div className="results-container">
      <div className="results-count">Found {results.length} records</div>
      
      <div className="results-list">
        {results.map((record) => (
          <div key={record.id} className="result-item">
            <div className="result-header" onClick={() => setExpandedId(expandedId === record.id ? null : record.id)}>
              <div className="result-cover">
                {record.cover_art_url ? (
                  <img 
                    src={record.cover_art_url} 
                    alt={record.album}
                    onError={(e) => e.target.src = '/placeholder.jpg'}
                  />
                ) : (
                  <div className="placeholder-cover">No Image</div>
                )}
              </div>
              
              <div className="result-info">
                <h3 className="result-artist">{record.artist}</h3>
                <h2 className="result-album">{record.album}</h2>
                <p className="result-title">{record.title}</p>
                {record.format && <span className="badge">{record.format}</span>}
              </div>
              
              <div className="result-price">
                <div className="min-price">From ₪{record.min_price.toFixed(2)}</div>
                <div className="store-count">{record.prices.length} store{record.prices.length !== 1 ? 's' : ''}</div>
                <div className="expand-indicator">
                  {expandedId === record.id ? '▼' : '▶'}
                </div>
              </div>
            </div>
            
            {expandedId === record.id && (
              <PriceComparison prices={record.prices} />
            )}
          </div>
        ))}
      </div>
    </div>
  )
}

export default ResultsList
