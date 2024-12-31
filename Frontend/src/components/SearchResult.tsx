import React from 'react';
import { ExternalLink } from 'lucide-react';

interface SearchResultProps {
  title: string;
  url: string;
  description: string;
  tags: string[];
}

export function SearchResult({ title, url, description, tags }: SearchResultProps) {
  return (
    <div className="bg-white p-6 rounded-lg shadow-sm border border-gray-100 hover:shadow-md transition-shadow">
      <a
        href={url}
        target="_blank"
        rel="noopener noreferrer"
        className="group flex items-center gap-2"
      >
        <h2 className="text-xl font-semibold text-blue-600 group-hover:underline">
          {title}
        </h2>
        <ExternalLink className="w-4 h-4 text-gray-400 group-hover:text-blue-600" />
      </a>
      <p className="text-gray-600 mt-2">{description}</p>
      <div className="flex flex-wrap gap-2 mt-3">
        {tags.map((tag) => (
          <span
            key={tag}
            className="px-3 py-1 text-sm bg-gray-100 text-gray-700 rounded-full hover:bg-gray-200 cursor-pointer"
          >
            {tag}
          </span>
        ))}
      </div>
    </div>
  );
}