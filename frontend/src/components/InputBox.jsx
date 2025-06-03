import React from 'react';

const InputBox = ({ prompt, setPrompt, disabled = false, maxLength = 1000 }) => {
  const handleChange = (e) => {
    const value = e.target.value;
    if (value.length <= maxLength) {
      setPrompt(value);
    }
  };

  const remainingChars = maxLength - prompt.length;
  const isNearLimit = remainingChars < 100;

  return (
    <div className="form-group">
      <label htmlFor="prompt-input">
        ✍️ What would you like me to write about?
      </label>
      <div className="input-container">
        <textarea
          id="prompt-input"
          className="prompt-input"
          value={prompt}
          onChange={handleChange}
          disabled={disabled}
          placeholder="Enter your topic here... (e.g., 'Write a blog introduction about artificial intelligence', 'Create a tweet about sustainable living', 'Tell a short story about a time traveler')"
          rows={5}
          maxLength={maxLength}
        />
        <div 
          className="char-counter"
          style={{ 
            color: isNearLimit ? '#e74c3c' : '#999',
            fontWeight: isNearLimit ? '600' : 'normal'
          }}
        >
          {remainingChars} characters remaining
        </div>
      </div>
    </div>
  );
};

export default InputBox;
