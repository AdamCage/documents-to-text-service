import React, { useState } from 'react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';
import './App.css';

const DOCUMENT_TYPES = {
  '100': 'Паспорт РФ',
  '101': 'СНИЛС',
  '102': 'Заграничный паспорт РФ',
  '0': 'Прочий документ'
};

const App = () => {
  const [file, setFile] = useState(null);
  const [fileType, setFileType] = useState('image');
  const [useLLM, setUseLLM] = useState(false);
  const [extractedText, setExtractedText] = useState('');
  const [llmText, setLlmText] = useState('');
  const [loading, setLoading] = useState(false);
  const [documentType, setDocumentType] = useState('100');

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
    setExtractedText('');
    setLlmText('');
  };

  const handleFileTypeChange = (e) => {
    setFileType(e.target.value);
    setFile(null);
    setExtractedText('');
    setLlmText('');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!file) return;

    const docTypeCode = parseInt(documentType, 10);
    if (isNaN(docTypeCode)) {
      console.error('Некорректный тип документа');
      return;
    }
  
    const formData = new FormData();
    formData.append('id', uuidv4());
    formData.append('user_id', 'user-id');
    formData.append('content_type', file.type);
    formData.append('file', file);
    formData.append('document_type_code', docTypeCode.toString()); // Переносим параметр в FormData
  
    // Формируем полный URL эндпоинта
    const baseEndpoint = fileType === 'image' 
      ? 'extract_text_from_image' 
      : 'extract_text_from_pdf';
    
    const fullEndpoint = useLLM 
      ? `${baseEndpoint}_with_llm_correction`
      : baseEndpoint;
  
    setLoading(true);
    setExtractedText('');
    setLlmText('');
  
    try {
      const response = await axios.post(
        `http://127.0.0.1:80/api/v1/${fullEndpoint}`,
        formData,
        {
          headers: {
            'Content-Type': 'multipart/form-data; charset=utf-8', // Явно указываем кодировку
          },
          // params: {} // Убираем query-параметры
        }
      );
  
      // Обработка ответа с учетом кодировки
      const decoder = new TextDecoder('utf-8');

      setExtractedText(response.data.extracted_text);
  
    if (response.data.llm_corrected_text) {
      try {
        // Прямое присвоение текста
        const llmText = response.data.llm_corrected_text;
        // Попытка форматирования JSON
        try {
          const parsed = JSON.parse(llmText);
          setLlmText(JSON.stringify(parsed, null, 2));
        } catch {
          setLlmText(llmText);
        }
      } catch (error) {
        console.error('LLM text error:', error);
        setLlmText('Error processing LLM response');
      }
    }
    } catch (error) {
      console.error('Error extracting text:', error);
      if (error.response) {
        console.error('Response data:', error.response.data);
        console.error('Response status:', error.response.status);
      }
    } finally {
      setLoading(false);
    }
  };

  const renderFilePreview = () => {
    if (!file) return null;
    const fileURL = URL.createObjectURL(file);

    if (fileType === 'image') {
      return <img src={fileURL} alt="Preview" style={previewStyle} />;
    }
    return (
      <iframe
        src={fileURL}
        title="PDF Preview"
        style={{ ...previewStyle, border: 'none' }}
      />
    );
  };

  return (
    <div className="container">
      <div className="left-panel">
        <h2>Upload File</h2>
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label>Тип документа:</label>
            <select 
              value={documentType}
              onChange={(e) => setDocumentType(e.target.value)}
              className="select-style"
            >
              {Object.entries(DOCUMENT_TYPES).map(([code, name]) => (
                <option key={code} value={code}>{name}</option>
              ))}
            </select>
          </div>

          {/* Выбор типа файла */}
          <div style={formGroupStyle}>
            <label>File Type:</label>
            <select 
              value={fileType} 
              onChange={handleFileTypeChange}
              style={selectStyle}
            >
              <option value="image">Image</option>
              <option value="pdf">PDF</option>
            </select>
          </div>

          {/* Переключатель LLM */}
          <div style={formGroupStyle}>
            <label>
              <input
                type="checkbox"
                checked={useLLM}
                onChange={(e) => setUseLLM(e.target.checked)}
                style={checkboxStyle}
              />
              Use LLM Correction
            </label>
          </div>

          {/* Поле загрузки файла */}
          <div style={formGroupStyle}>
            <input
              type="file"
              onChange={handleFileChange}
              accept={fileType === 'image' ? 'image/*' : 'application/pdf'}
              style={fileInputStyle}
            />
          </div>

          <button 
            type="submit" 
            disabled={loading}
            style={buttonStyle}
          >
            {loading ? 'Processing...' : 'Extract Text'}
          </button>
        </form>

        {/* Превью файла */}
        <div style={previewContainerStyle}>
          <h3>File Preview</h3>
          <div style={previewWrapperStyle}>
            {renderFilePreview()}
          </div>
        </div>
      </div>

      {/* Правая панель результатов */}
      <div style={rightPanelStyle}>
        {loading ? (
          <div style={loaderStyle}>
            <div className="spinner"></div>
          </div>
        ) : (
          <>
            {/* Raw Text Section */}
            <div style={textSectionStyle}>
              <h3>Raw Extracted Text</h3>
              <pre style={textPreStyle}>
                {extractedText || 'No text extracted'}
              </pre>
            </div>

            {/* LLM Text Section - Always visible when LLM is enabled */}
            {useLLM && (
              <div style={textSectionStyle}>
                <h3>LLM Corrected Text</h3>
                <pre style={textPreStyle}>
                  {llmText || (loading ? 'Processing...' : 'No LLM correction')}
                </pre>
              </div>
            )}
          </>
        )}
      </div>
    </div>
  );
};

// Стили для компонента
const containerStyle = {
  display: 'flex',
  padding: '20px',
  height: '100vh',
  gap: '20px'
};

const leftPanelStyle = {
  width: '45%',
  padding: '20px',
  borderRight: '1px solid #ddd'
};

const rightPanelStyle = {
  width: '55%',
  padding: '20px',
  display: 'flex',
  flexDirection: 'column',
  gap: '20px',
  height: 'calc(100vh - 40px)',
  overflow: 'auto'
};


const formGroupStyle = {
  marginBottom: '15px'
};

const selectStyle = {
  padding: '8px',
  marginLeft: '10px',
  width: '200px'
};

const checkboxStyle = {
  marginRight: '8px'
};

const fileInputStyle = {
  padding: '8px',
  border: '1px solid #ddd',
  borderRadius: '4px'
};

const buttonStyle = {
  padding: '10px 20px',
  backgroundColor: '#4CAF50',
  color: 'white',
  border: 'none',
  borderRadius: '4px',
  cursor: 'pointer'
};

const previewContainerStyle = {
  marginTop: '20px',
  height: '50vh',
  border: '1px solid #eee',
  borderRadius: '4px',
  padding: '10px'
};

const previewWrapperStyle = {
  height: '100%',
  overflow: 'auto'
};

const previewStyle = {
  width: '100%',
  height: '100%',
  objectFit: 'contain'
};

const loaderStyle = {
  position: 'absolute',
  top: '50%',
  left: '50%',
  transform: 'translate(-50%, -50%)'
};

const textSectionStyle = {
  backgroundColor: '#f5f5f5',
  borderRadius: '8px',
  padding: '15px',
  flex: 1,
  minHeight: '300px',
  display: 'flex',
  flexDirection: 'column'
};


const textPreStyle = {
  whiteSpace: 'pre-wrap',
  wordWrap: 'break-word',
  backgroundColor: 'white',
  padding: '10px',
  borderRadius: '4px',
  flex: 1,
  overflow: 'auto',
  margin: '10px 0'
};

export default App;