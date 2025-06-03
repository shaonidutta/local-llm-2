import React from 'react';

const TemperatureSlider = ({ temperature, setTemperature, disabled = false }) => {
  const handleChange = (e) => {
    setTemperature(parseFloat(e.target.value));
  };

  const getTemperatureDescription = (temp) => {
    if (temp <= 0.3) return 'Focused & Deterministic';
    if (temp <= 0.7) return 'Balanced Creativity';
    return 'Highly Creative & Varied';
  };

  const getTemperatureColor = (temp) => {
    if (temp <= 0.3) return '#3498db';
    if (temp <= 0.7) return '#f39c12';
    return '#e74c3c';
  };

  return (
    <div className="form-group">
      <label htmlFor="temperature-slider">
        🌡️ Creativity Level: {temperature.toFixed(1)}
      </label>
      <div className="temperature-container">
        <span style={{ fontSize: '14px', color: '#666' }}>0.0</span>
        <input
          id="temperature-slider"
          type="range"
          min="0"
          max="1"
          step="0.1"
          value={temperature}
          onChange={handleChange}
          disabled={disabled}
          className="temperature-slider"
          style={{
            background: `linear-gradient(to right, #e1e5e9 0%, ${getTemperatureColor(temperature)} ${temperature * 100}%, #e1e5e9 ${temperature * 100}%)`
          }}
        />
        <span style={{ fontSize: '14px', color: '#666' }}>1.0</span>
      </div>
      <div 
        className="temperature-description"
        style={{ 
          fontSize: '14px', 
          color: getTemperatureColor(temperature),
          fontWeight: '600',
          textAlign: 'center',
          marginTop: '8px'
        }}
      >
        {getTemperatureDescription(temperature)}
      </div>
      <div style={{ fontSize: '12px', color: '#999', marginTop: '5px' }}>
        Lower values produce more focused, predictable text. Higher values increase creativity and variation.
      </div>
    </div>
  );
};

export default TemperatureSlider;
