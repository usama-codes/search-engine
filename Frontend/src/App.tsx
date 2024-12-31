import React, { useState } from 'react';
import { SearchBar } from './components/SearchBar';
import { SearchResults } from './components/SearchResults';
import { FileUpload } from './components/FileUpload';
import { Search } from 'lucide-react';
import { searchResults as searchApi, SearchResult } from './services/api';

export default function App() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<SearchResult[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const data = await searchApi(query);
      setResults(data);
    } catch (err) {
      setError('Failed to fetch search results. Please try again.');
      setResults([]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="container mx-auto px-4 py-8">
        <div className="absolute top-4 right-4">
          <FileUpload />
        </div>
        
        <header className="flex flex-col items-center mb-12">
          <div className="flex items-center gap-3 mb-8">
            <Search className="w-10 h-10 text-blue-600" />
            <h1 className="text-4xl font-bold text-gray-900">Search Engine</h1>
          </div>
          <SearchBar
            query={query}
            setQuery={setQuery}
            onSearch={handleSearch}
          />
        </header>
        
        <main className="max-w-3xl mx-auto">
          <SearchResults
            results={results}
            loading={loading}
            error={error}
            query={query}
          />
        </main>
      </div>
    </div>
  );
}