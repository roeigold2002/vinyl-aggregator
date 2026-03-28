import React from 'react'
import '../styles/components.css'

export const SearchInput = ({ value, onChange, onSearch, loading }) => {
  const handleSubmit = (e) => {
    e.preventDefault()
    if (value.trim()) {
      onSearch(value)
    }
  }

  return (
    <form className="search-form" onSubmit={handleSubmit}>
      <div className="search-container">
        <input
          type="text"
          className="search-input"
          placeholder="Search for records, artists, albums..."
          value={value}
          onChange={(e) => onChange(e.target.value)}
          disabled={loading}
        />
        <button
          type="submit"
          className="search-button"
          disabled={loading || !value.trim()}
        >
          {loading ? 'Searching...' : 'Search'}
        </button>
      </div>
    </form>
  )
}

export default SearchInput
