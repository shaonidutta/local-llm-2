import React, { useState } from 'react';

const OutputDisplay = ({ output, metadata = {} }) => {
  const [copied, setCopied] = useState(false);

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(output);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    } catch (err) {
      console.error('Failed to copy text:', err);
      // Fallback for older browsers
      const textArea = document.createElement('textarea');
      textArea.value = output;
      document.body.appendChild(textArea);
      textArea.select();
      try {
        document.execCommand('copy');
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      } catch (fallbackErr) {
        console.error('Fallback copy failed:', fallbackErr);
      }
      document.body.removeChild(textArea);
    }
  };

  const formatTime = (seconds) => {
    if (seconds < 1) return `${(seconds * 1000).toFixed(0)}ms`;
    return `${seconds.toFixed(1)}s`;
  };

  const formatTimestamp = (timestamp) => {
    if (!timestamp) return '';
    try {
      return new Date(timestamp).toLocaleString();
    } catch {
      return timestamp;
    }
  };

  if (!output) return null;

  return (
    <div className="output-container">
      <div className="output-header">
        <h3>📝 Generated Content</h3>
        <button
          className={`copy-button ${copied ? 'copied' : ''}`}
          onClick={handleCopy}
          title="Copy to clipboard"
        >
          {copied ? '✅ Copied!' : '📋 Copy'}
        </button>
      </div>
      
      <div className="output-display">
        {output}
      </div>
      
      {metadata && (
        <div className="output-meta">
          <div>
            {metadata.time_taken && (
              <span>⚡ Generated in {formatTime(metadata.time_taken)}</span>
            )}
            {metadata.temperature !== undefined && (
              <span style={{ marginLeft: '15px' }}>
                🌡️ Temperature: {metadata.temperature}
              </span>
            )}
          </div>
          <div>
            {metadata.timestamp && (
              <span style={{ fontSize: '12px', color: '#999' }}>
                {formatTimestamp(metadata.timestamp)}
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  );
};

export default OutputDisplay;
