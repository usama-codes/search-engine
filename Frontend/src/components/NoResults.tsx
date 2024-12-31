import React from 'react';

interface NoResultsProps {
  query: string;
}

export function NoResults({ query }: NoResultsProps) {
  return (
    <div className="text-center py-8">
      <p className="text-gray-600">
        {query ? 'No results found. Try a different search term.' : 'Enter a search term to begin'}
      </p>
    </div>
  );
}