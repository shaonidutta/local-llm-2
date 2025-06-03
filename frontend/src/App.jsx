import React, { useState, useEffect } from 'react';
import InputBox from './components/InputBox';
import TemperatureSlider from './components/TemperatureSlider';
import Loader from './components/Loader';
import OutputDisplay from './components/OutputDisplay';
import StatusIndicator from './components/StatusIndicator';
import { generateText } from './api';
import './index.css';

function App() {
  const [prompt, setPrompt] = useState('');
  const [temperature, setTemperature] = useState(0.7);
  const [loading, setLoading] = useState(false);
  const [output, setOutput] = useState('');
  const [metadata, setMetadata] = useState({});
  const [error, setError] = useState('');

  // Load saved settings from localStorage
  useEffect(() => {
    const savedTemperature = localStorage.getItem('ai-writer-temperature');
    if (savedTemperature) {
      setTemperature(parseFloat(savedTemperature));
    }
  }, []);

  // Save temperature to localStorage when it changes
  useEffect(() => {
    localStorage.setItem('ai-writer-temperature', temperature.toString());
  }, [temperature]);

  const handleGenerate = async () => {
    if (!prompt.trim()) {
      setError('Please enter a prompt before generating.');
      return;
    }

    setLoading(true);
    setOutput('');
    setError('');
    setMetadata({});

    try {
      const response = await generateText(prompt, temperature, 200);
      setOutput(response.output);
      setMetadata({
        time_taken: response.time_taken,
        temperature: response.temperature,
        timestamp: response.timestamp,
        prompt: response.prompt
      });
    } catch (err) {
      setError(err.message || 'Failed to generate text. Please try again.');
      console.error('Generation error:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && (e.ctrlKey || e.metaKey)) {
      e.preventDefault();
      handleGenerate();
    }
  };

  const clearAll = () => {
    setPrompt('');
    setOutput('');
    setError('');
    setMetadata({});
  };

  const canGenerate = prompt.trim().length > 0 && !loading;

  return (
    <div className="container" onKeyDown={handleKeyPress}>
      <StatusIndicator />
      
      <div className="card">
        <div className="header">
          <h1>🤖 Local AI Writer</h1>
          <p>Generate creative content using Llama3 running locally on your machine</p>
        </div>

        <form onSubmit={(e) => { e.preventDefault(); handleGenerate(); }}>
          <InputBox
            prompt={prompt}
            setPrompt={setPrompt}
            disabled={loading}
            maxLength={1000}
          />

          <TemperatureSlider
            temperature={temperature}
            setTemperature={setTemperature}
            disabled={loading}
          />

          <div style={{ display: 'flex', gap: '10px', marginBottom: '20px' }}>
            <button
              type="submit"
              className="generate-button"
              disabled={!canGenerate}
              style={{ flex: 1 }}
            >
              {loading ? '🔄 Generating...' : '✨ Generate Content'}
            </button>
            
            {(output || error) && (
              <button
                type="button"
                onClick={clearAll}
                disabled={loading}
                style={{
                  padding: '15px 20px',
                  background: '#f8f9fa',
                  border: '1px solid #e1e5e9',
                  borderRadius: '10px',
                  cursor: 'pointer',
                  fontSize: '14px'
                }}
              >
                🗑️ Clear
              </button>
            )}
          </div>

          <div style={{ fontSize: '14px', color: '#666', textAlign: 'center', marginBottom: '20px' }}>
            💡 Tip: Press Ctrl+Enter (Cmd+Enter on Mac) to generate quickly
          </div>
        </form>

        {loading && <Loader message="Generating your content..." />}

        {error && (
          <div className="error-message">
            <strong>❌ Error:</strong> {error}
          </div>
        )}

        {output && (
          <OutputDisplay
            output={output}
            metadata={metadata}
          />
        )}

        {!loading && !output && !error && (
          <div style={{ 
            textAlign: 'center', 
            padding: '40px 20px', 
            color: '#999',
            fontSize: '16px'
          }}>
            <div style={{ fontSize: '48px', marginBottom: '15px' }}>📝</div>
            <div>Enter a prompt above to start generating creative content!</div>
            <div style={{ fontSize: '14px', marginTop: '10px' }}>
              Try: "Write a blog intro about AI", "Create a tweet about coffee", or "Tell a short story about space"
            </div>
          </div>
        )}
      </div>

      <div style={{ 
        textAlign: 'center', 
        marginTop: '20px', 
        color: 'rgba(255, 255, 255, 0.8)',
        fontSize: '14px'
      }}>
        <div>🔒 100% Local • 🚀 Powered by Llama3 • 📊 All data stays on your machine</div>
      </div>
    </div>
  );
}

export default App;
