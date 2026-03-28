import { useState, useCallback } from 'react'
import { searchAPI } from '../services/api'

export const useSearch = () => {
  const [results, setResults] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const [query, setQuery] = useState('')

  const search = useCallback(async (searchQuery) => {
    if (!searchQuery.trim()) {
      setResults([])
      return
    }

    setLoading(true)
    setError(null)
    setQuery(searchQuery)

    try {
      const data = await searchAPI.search(searchQuery)
      setResults(data)
    } catch (err) {
      setError(err.message || 'Search failed')
      setResults([])
    } finally {
      setLoading(false)
    }
  }, [])

  return {
    results,
    loading,
    error,
    query,
    search,
    setQuery,
  }
}
