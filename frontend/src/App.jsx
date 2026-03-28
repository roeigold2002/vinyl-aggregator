import React from 'react'
import SearchInput from './components/SearchInput'
import ResultsList from './components/ResultsList'
import { useSearch } from './hooks/useSearch'
import './styles/globals.css'

function App() {
  const { results, loading, error, query, search, setQuery } = useSearch()

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1>🎵 Vinyl Record Aggregator</h1>
          <p>Search and compare vinyl records across Israeli stores</p>
        </div>
      </header>

      <main className="app-main">
        <div className="search-section">
          <SearchInput
            value={query}
            onChange={setQuery}
            onSearch={search}
            loading={loading}
          />
        </div>

        <div className="results-section">
          <ResultsList
            results={results}
            loading={loading}
            error={error}
          />
        </div>
      </main>

      <footer className="app-footer">
        <p>Find the best vinyl records at the best prices across Israeli stores</p>
      </footer>
    </div>
  )
}

export default App
