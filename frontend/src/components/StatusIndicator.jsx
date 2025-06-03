import React, { useState, useEffect } from 'react';
import { checkHealth } from '../api';

const StatusIndicator = () => {
  const [status, setStatus] = useState('checking');
  const [modelInfo, setModelInfo] = useState(null);

  useEffect(() => {
    const checkStatus = async () => {
      try {
        const health = await checkHealth();
        setStatus('connected');
        setModelInfo(health.model_info);
      } catch (error) {
        setStatus('disconnected');
        setModelInfo(null);
      }
    };

    // Check immediately
    checkStatus();

    // Check every 30 seconds
    const interval = setInterval(checkStatus, 30000);

    return () => clearInterval(interval);
  }, []);

  const getStatusText = () => {
    switch (status) {
      case 'checking':
        return '🔄 Checking...';
      case 'connected':
        return '🟢 Connected';
      case 'disconnected':
        return '🔴 Disconnected';
      default:
        return '❓ Unknown';
    }
  };

  const getStatusClass = () => {
    switch (status) {
      case 'connected':
        return 'connected';
      case 'disconnected':
        return 'disconnected';
      default:
        return 'checking';
    }
  };

  return (
    <div 
      className={`status-indicator ${getStatusClass()}`}
      title={modelInfo ? `Model: ${modelInfo.model_name || 'Unknown'}\nStatus: ${modelInfo.status || 'Unknown'}` : 'Backend status'}
    >
      {getStatusText()}
    </div>
  );
};

export default StatusIndicator;
