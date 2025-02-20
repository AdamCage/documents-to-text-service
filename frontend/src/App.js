import React, { useState } from 'react';
import axios from 'axios';
import './App.css'; // Убедитесь, что вы импортируете CSS файл

const App = () => {
  const [file, setFile] = useState(null);
  const [fileType, setFileType] = useState('image');
  const [extractedText, setExtractedText] = useState('');
  const [loading, setLoading] = useState(false); // Состояние загрузки

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleFileTypeChange = (e) => {
    setFileType(e.target.value);
    setFile(null);
    setExtractedText('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const formData = new FormData();
    formData.append('id', 'unique-id');
    formData.append('user_id', 'user-id');
    formData.append('content_type', file.type);
    formData.append('file', file);

    const endpoint = fileType === 'image' 
      ? 'http://localhost:80/api/v1/extract_text_from_image' 
      : 'http://localhost:80/api/v1/extract_text_from_pdf';

    setLoading(true); // Устанавливаем состояние загрузки в true

    try {
      const response = await axios.post(endpoint, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      setExtractedText(response.data.extracted_text);
    } catch (error) {
      console.error('Error extracting text:', error);
    } finally {
      setLoading(false); // Сбрасываем состояние загрузки
    }
  };

  const renderFilePreview = () => {
    if (!file) return null;

    const fileURL = URL.createObjectURL(file);

    if (fileType === 'image') {
      return <img src={fileURL} alt="Preview" style={{ width: '100%', height: '100%', objectFit: 'contain' }} />;
    } else if (fileType === 'pdf') {
      return (
        <iframe
          src={fileURL}
          title="PDF Preview"
          style={{ width: '100%', height: '100%', border: 'none' }}
        />
      );
    }
  };

  return (
    <div style={{ display: 'flex', padding: '20px', height: '100vh' }}>
      <div style={{ width: '50%', marginRight: '20px', overflow: 'hidden' }}>
        <h2>Upload File</h2>
        <form onSubmit={handleSubmit}>
          <select value={fileType} onChange={handleFileTypeChange}>
            <option value="image">Image</option>
            <option value="pdf">PDF</option>
          </select>
          <input type="file" onChange={handleFileChange} accept={fileType === 'image' ? 'image/*' : 'application/pdf'} />
          <button type="submit" disabled={loading}>Extract Text</button>
        </form>
        <div style={{ marginTop: '20px', height: 'calc(100% - 100px)', position: 'relative' }}>
          <h3>File Preview</h3>
          <div style={{ height: '100%', overflow: 'auto' }}>
            {renderFilePreview()}
          </div>
        </div>
        <div style={{ marginTop: '20px' }}>
          <h3>Extracted Text</h3>
          <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>{extractedText}</pre>
        </div>
      </div>
      <div style={{ width: '50%', borderLeft: '1px solid #ccc', paddingLeft: '20px', position: 'relative' }}>
        <h2>Extracted Text</h2>
        {loading ? (
          <div className="loader" style={{ position: 'absolute', top: '50%', left: '50%', transform: 'translate(-50%, -50%)' }}>
            <div className="spinner"></div>
          </div>
        ) : (
          <pre style={{ whiteSpace: 'pre-wrap', wordWrap: 'break-word' }}>{extractedText}</pre>
        )}
      </div>
    </div>
  );
};

export default App;
