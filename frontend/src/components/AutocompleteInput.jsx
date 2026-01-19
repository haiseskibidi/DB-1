import { useState, useEffect, useRef } from 'react'
import './AutocompleteInput.css'

function AutocompleteInput({ value, onChange, suggestions, placeholder, type = 'text' }) {
  const [isOpen, setIsOpen] = useState(false)
  const [filteredSuggestions, setFilteredSuggestions] = useState([])
  const wrapperRef = useRef(null)

  useEffect(() => {
    if (value && suggestions.length > 0) {
      const searchTerm = value.toLowerCase().trim()
      const filtered = suggestions
        .filter(item => {
          const itemLower = item.toLowerCase()
          return itemLower.includes(searchTerm) || itemLower.startsWith(searchTerm)
        })
        .slice(0, 10)
      setFilteredSuggestions(filtered)
      setIsOpen(filtered.length > 0 && value.length > 0)
    } else {
      setIsOpen(false)
    }
  }, [value, suggestions])

  useEffect(() => {
    function handleClickOutside(event) {
      if (wrapperRef.current && !wrapperRef.current.contains(event.target)) {
        setIsOpen(false)
      }
    }
    document.addEventListener('mousedown', handleClickOutside)
    return () => document.removeEventListener('mousedown', handleClickOutside)
  }, [])

  const handleSelect = (suggestion) => {
    onChange({ target: { value: suggestion } })
    setIsOpen(false)
  }

  return (
    <div className={`autocomplete-wrapper ${isOpen ? 'has-suggestions' : ''}`} ref={wrapperRef}>
      <input
        type={type}
        value={value}
        onChange={onChange}
        onFocus={() => value && setIsOpen(filteredSuggestions.length > 0)}
        placeholder={placeholder}
        className="search-input"
      />
      {isOpen && filteredSuggestions.length > 0 && (
        <div className="autocomplete-dropdown">
          {filteredSuggestions.map((suggestion, idx) => (
            <div
              key={idx}
              className="autocomplete-item"
              onClick={() => handleSelect(suggestion)}
            >
              {suggestion}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default AutocompleteInput

