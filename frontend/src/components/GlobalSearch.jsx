import { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';
import { MagnifyingGlassIcon, XMarkIcon } from '@heroicons/react/24/outline';

const GlobalSearch = () => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showResults, setShowResults] = useState(false);
  const searchRef = useRef(null);
  const navigate = useNavigate();

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (searchRef.current && !searchRef.current.contains(event.target)) {
        setShowResults(false);
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => document.removeEventListener('mousedown', handleClickOutside);
  }, []);

  useEffect(() => {
    const searchTimeout = setTimeout(() => {
      if (query.trim().length >= 2) {
        performSearch();
      } else {
        setResults(null);
      }
    }, 300); // Debounce search

    return () => clearTimeout(searchTimeout);
  }, [query]);

  const performSearch = async () => {
    setLoading(true);
    try {
      const response = await axios.get('/api/search/', {
        params: { q: query, limit: 5 }
      });
      setResults(response.data);
      setShowResults(true);
    } catch (error) {
      console.error('Search error:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleResultClick = (type, id) => {
    setShowResults(false);
    setQuery('');
    
    switch(type) {
      case 'property':
        navigate(`/properties/${id}`);
        break;
      case 'transaction':
        navigate('/transactions');
        break;
      case 'material':
        navigate('/materials');
        break;
      case 'document':
        navigate('/documents');
        break;
      default:
        break;
    }
  };

  const clearSearch = () => {
    setQuery('');
    setResults(null);
    setShowResults(false);
  };

  return (
    <div className="relative" ref={searchRef}>
      {/* Search Input */}
      <div className="relative">
        <div className="absolute inset-y-0 left-0 pl-3 flex items-center pointer-events-none">
          <MagnifyingGlassIcon className="h-5 w-5 text-gray-400" />
        </div>
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onFocus={() => query && setShowResults(true)}
          placeholder="Search properties, transactions, materials..."
          className="block w-full pl-10 pr-10 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent"
        />
        {query && (
          <button
            onClick={clearSearch}
            className="absolute inset-y-0 right-0 pr-3 flex items-center"
          >
            <XMarkIcon className="h-5 w-5 text-gray-400 hover:text-gray-600" />
          </button>
        )}
      </div>

      {/* Search Results Dropdown */}
      {showResults && results && results.total > 0 && (
        <div className="absolute z-50 mt-2 w-full bg-white rounded-lg shadow-lg border border-gray-200 max-h-96 overflow-y-auto">
          <div className="p-2">
            <div className="text-sm text-gray-500 px-3 py-2">
              Found {results.total} results for "{results.query}"
            </div>

            {/* Properties */}
            {results.results.properties && results.results.properties.count > 0 && (
              <div className="mb-2">
                <div className="text-xs font-semibold text-gray-500 uppercase px-3 py-1">
                  Properties ({results.results.properties.count})
                </div>
                {results.results.properties.data.map((property) => (
                  <button
                    key={property.id}
                    onClick={() => handleResultClick('property', property.id)}
                    className="w-full text-left px-3 py-2 hover:bg-gray-100 rounded-md"
                  >
                    <div className="font-medium text-gray-900">{property.title}</div>
                    <div className="text-sm text-gray-500">{property.city}, {property.state}</div>
                  </button>
                ))}
              </div>
            )}

            {/* Transactions */}
            {results.results.transactions && results.results.transactions.count > 0 && (
              <div className="mb-2">
                <div className="text-xs font-semibold text-gray-500 uppercase px-3 py-1">
                  Transactions ({results.results.transactions.count})
                </div>
                {results.results.transactions.data.map((transaction) => (
                  <button
                    key={transaction.id}
                    onClick={() => handleResultClick('transaction', transaction.id)}
                    className="w-full text-left px-3 py-2 hover:bg-gray-100 rounded-md"
                  >
                    <div className="font-medium text-gray-900">{transaction.property_title}</div>
                    <div className="text-sm text-gray-500">
                      ${parseFloat(transaction.sale_price).toLocaleString()} - {transaction.status}
                    </div>
                  </button>
                ))}
              </div>
            )}

            {/* Materials */}
            {results.results.materials && results.results.materials.count > 0 && (
              <div className="mb-2">
                <div className="text-xs font-semibold text-gray-500 uppercase px-3 py-1">
                  Materials ({results.results.materials.count})
                </div>
                {results.results.materials.data.map((material) => (
                  <button
                    key={material.id}
                    onClick={() => handleResultClick('material', material.id)}
                    className="w-full text-left px-3 py-2 hover:bg-gray-100 rounded-md"
                  >
                    <div className="font-medium text-gray-900">{material.name}</div>
                    <div className="text-sm text-gray-500">{material.category}</div>
                  </button>
                ))}
              </div>
            )}
          </div>
        </div>
      )}

      {/* No Results */}
      {showResults && results && results.total === 0 && (
        <div className="absolute z-50 mt-2 w-full bg-white rounded-lg shadow-lg border border-gray-200 p-4">
          <div className="text-center text-gray-500">
            No results found for "{results.query}"
          </div>
        </div>
      )}
    </div>
  );
};

export default GlobalSearch;

