import React from 'react';

const Loader = ({ message = "Generating your content..." }) => {
  return (
    <div className="loader">
      <div className="spinner"></div>
      <div>
        <div style={{ fontSize: '16px', fontWeight: '600', marginBottom: '5px' }}>
          {message}
        </div>
        <div style={{ fontSize: '14px', color: '#999' }}>
          This may take a few moments depending on your hardware
        </div>
      </div>
    </div>
  );
};

export default Loader;
