const API_BASE_URL = 'http://localhost:5000'; // Ensure this matches the Flask server's URL

export interface SearchResult {
  id: number;
  title: string;
  url: string;
  description: string;
  tags: string[];
}

interface UploadResponse {
  message: string;
}

// Function to search for results based on a query
export async function searchResults(query: string): Promise<SearchResult[]> {
  try {
    query = query.toLowerCase();
    const response = await fetch(`${API_BASE_URL}/query`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ query }),
    });
    if (!response.ok) {
      throw new Error('Search request failed');
    }
    return await response.json();
  } catch (error) {
    console.error('Search error:', error);
    throw error;
  }
}


// Function to upload a document
export async function uploadDocument(formData: FormData): Promise<UploadResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/upload`, {
      method: 'POST',
      body: formData,
    });
    
    if (!response.ok) {
      throw new Error('Upload failed');
    }

    const data = await response.json();
    return data as UploadResponse;
  } catch (error) {
    console.error('Upload error:', error);
    throw error;
  }
}
