import React from 'react';
import { SearchResult as SearchResultComponent } from './SearchResult';
import { LoadingSpinner } from './LoadingSpinner';
import { ErrorMessage } from './ErrorMessage';
import { NoResults } from './NoResults';
import type { SearchResult } from '../services/api';

interface SearchResultsProps {
  results: SearchResult[];
  loading: boolean;
  error: string | null;
  query: string;
}

export function SearchResults({ results, loading, error, query }: SearchResultsProps) {
  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;
  
  return (
    <div className="space-y-4">
      {results.length > 0 ? (
        results.map((result) => (
          <SearchResultComponent
            key={result.id}
            title={result.title}
            url={result.url}
            description={result.description}
            tags={result.tags}
          />
        ))
      ) : (
        <NoResults query={query} />
      )}
    </div>
  );
}