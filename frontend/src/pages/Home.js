import React, { useState } from "react";
import "../styles/home.css";

export default function Home() {
  const [searchQuery, setSearchQuery] = useState("");
  const [searchResults, setSearchResults] = useState([]);
  const [isLoading, setIsLoading] = useState(false);

  const handleSearch = async () => {
    if (!searchQuery.trim()) return;
    setIsLoading(true);
    try {
      const response = await fetch('/api/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ q: searchQuery })
      });
      const data = await response.json();
      setSearchResults(data.data.results || []);
    } catch (error) {
      console.error("Search error:", error);
      setSearchResults([]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') handleSearch();
  };

  return (
    <div className="main-content">
      <div className="home-container">
        <div className="welcome-section">
          <h1 className="welcome-title">Welcome to Knowledge Hub!</h1>
          <p className="welcome-subtitle">AI Search to your workforce</p>
        </div>

        {/* Search Results Display */}
        {searchResults.length > 0 && (
          <div className="search-results">
            <h3>Search Results</h3>
            {searchResults.map((result) => (
              <div key={result.id} className="result-card">
                <div className="result-content">
                  <p>{result.content}</p>
                </div>
                <div className="result-categories">
                  <span className="category-item">
                    <strong>Topic:</strong> {result.categories.topic}
                  </span>
                  <span className="category-item">
                    <strong>Project:</strong> {result.categories.project}
                  </span>
                  <span className="category-item">
                    <strong>Team:</strong> {result.categories.team}
                  </span>
                  {result.categories.citation && (
                    <a href={result.categories.citation} target="_blank" rel="noopener noreferrer" className="citation-link">
                      View Source
                    </a>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* Search Interface */}
        <div className="search-section">
          <div className="search-container">
            <input 
              className="search-input" 
              type="text" 
              placeholder="What do you want to search?"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={handleKeyPress}
            />
            <button 
              className="search-btn" 
              onClick={handleSearch}
              disabled={isLoading}
            >
              {isLoading ? "🔄" : "🔍"}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
