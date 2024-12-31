import React, { useRef, useState } from 'react';
import { Upload } from 'lucide-react';
import { uploadDocument } from '../services/api';

export function FileUpload() {
  const fileInputRef = useRef<HTMLInputElement>(null);
  const [uploading, setUploading] = useState(false);

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (!file) return;

    if (!file.name.endsWith('.csv') && !file.name.endsWith('.json')) {
      alert('Please select a .csv or .json file');
      return;
    }

    setUploading(true);
    try {
      const formData = new FormData();
      formData.append('file', file);
      const response = await uploadDocument(formData);
      alert(response.message || 'Document uploaded successfully!');
    } catch (error) {
      if (error instanceof Error) {
        alert(error.message);
      } else {
        alert('Failed to upload document. Please try again.');
      }
    } finally {
      setUploading(false);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
    }
  };

  return (
    <div className="flex items-center gap-2">
      <input
        type="file"
        ref={fileInputRef}
        accept=".csv,.json"
        onChange={handleFileChange}
        className="hidden"
      />
      <button
        onClick={handleUploadClick}
        disabled={uploading}
        className={`p-2 bg-blue-600 text-white rounded-full transition-colors ${
          uploading 
            ? 'opacity-75 cursor-not-allowed' 
            : 'hover:bg-blue-700'
        }`}
        title="Upload Document"
      >
        <Upload className={`w-5 h-5 ${uploading ? 'animate-bounce' : ''}`} />
      </button>
    </div>
  );
}