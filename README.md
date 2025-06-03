# Local AI Writer

A simple AI-powered writing application that runs entirely on your local machine using the Llama3 model. Generate creative content like blog introductions, tweets, and stories without relying on external APIs.

## App Type Selected

**AI Writer** - Generate creative text outputs such as blog introductions, tweets, or stories based on user-provided topics.

## Features

- 📝 **Prompt Input Box**: Enter your writing topic or idea
- 🎨 **Creative Output Display**: View generated content with copy functionality
- 🌡️ **Temperature Control**: Adjust creativity level (0.0 = deterministic, 1.0 = very creative)
- ⏳ **Loading Indicator**: Visual feedback during text generation
- 📊 **Output Logging**: All generations saved locally with timestamps
- 🔒 **100% Local**: No data sent to external servers

## Model Used

**Llama3** with 4-bit quantization for optimal performance on consumer hardware.

## System Requirements

- **Python**: 3.9 or higher
- **Node.js**: 14 or higher
- **RAM**: Minimum 8GB (16GB recommended)
- **Storage**: 10GB free space for model weights
- **GPU**: Optional but recommended (CUDA-compatible)

## Quick Setup

### Option 1: Automated Setup (Recommended)

**Windows:**
```bash
cd "assignments/local llm"
setup.bat
```

**Linux/Mac:**
```bash
cd "assignments/local llm"
chmod +x setup.sh start.sh
./setup.sh
```

### Option 2: Manual Setup

### 1. Navigate to Project Directory
```bash
cd "assignments/local llm"
```

### 2. Backend Setup
```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download model (first time only)
python download_model.py
```

### 3. Frontend Setup
```bash
cd ../frontend
npm install
```

## Running the Application

### Option 1: Automated Start (Recommended)

**Windows:**
```bash
start.bat
```

**Linux/Mac:**
```bash
./start.sh
```

### Option 2: Manual Start

### Start Backend Server
```bash
cd backend
# Activate virtual environment if not already active
# Windows: venv\Scripts\activate
# Linux/Mac: source venv/bin/activate
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### Start Frontend (in new terminal)
```bash
cd frontend
npm start
```

The application will open in your browser at `http://localhost:3000`

## How to Use

1. **Enter Your Topic**: Type your writing prompt in the input box
2. **Adjust Temperature**: Use the slider to control creativity (optional)
   - 0.0-0.3: More focused and deterministic
   - 0.4-0.7: Balanced creativity (recommended)
   - 0.8-1.0: Highly creative and varied
3. **Generate**: Click the "Generate" button
4. **View Results**: Generated text appears below with loading indicator
5. **Copy Output**: Use the copy button to save your generated content

## Project Structure

```
assignments/local llm/
├── backend/
│   ├── app.py              # FastAPI application
│   ├── inference.py        # Llama3 model integration
│   ├── download_model.py   # Model setup script
│   ├── requirements.txt    # Python dependencies
│   └── venv/              # Virtual environment (created during setup)
├── frontend/
│   ├── src/
│   │   ├── components/    # React components
│   │   │   ├── InputBox.jsx
│   │   │   ├── TemperatureSlider.jsx
│   │   │   ├── Loader.jsx
│   │   │   ├── OutputDisplay.jsx
│   │   │   └── StatusIndicator.jsx
│   │   ├── App.jsx       # Main application
│   │   ├── api.js        # API communication
│   │   ├── index.js      # React entry point
│   │   └── index.css     # Styles
│   ├── public/
│   │   ├── index.html    # HTML template
│   │   └── manifest.json # PWA manifest
│   ├── package.json      # Node.js dependencies
│   └── node_modules/     # Dependencies (created during setup)
├── models/               # Model weights (created after download)
├── logs/                # Output logs (created automatically)
├── setup.bat            # Windows setup script
├── setup.sh             # Linux/Mac setup script
├── start.bat            # Windows start script
├── start.sh             # Linux/Mac start script
├── test_setup.py        # Setup verification script
├── .gitignore           # Git ignore file
└── README.md            # This file
```

## Output Logging

All generated content is automatically saved to `logs/output_log.txt` with the following format:
```
2024-01-15 14:30:22 | Write a blog intro about AI | 0.7 | [Generated content...]
```

## Troubleshooting

### Model Download Issues
- Ensure stable internet connection for initial model download
- Check available disk space (requires ~10GB)
- Verify Python has write permissions to the models directory

### Performance Issues
- **Slow Generation**: Consider using GPU if available, or reduce max_length parameter
- **Memory Errors**: Close other applications, ensure minimum 8GB RAM available
- **CUDA Errors**: Install appropriate PyTorch version for your GPU

### Connection Issues
- Verify backend is running on port 8000
- Check firewall settings allow local connections
- Ensure CORS is properly configured

## Hardware Optimization

### For Better Performance:
- **GPU**: Install CUDA-compatible PyTorch for faster inference
- **RAM**: 16GB+ recommended for smoother operation
- **SSD**: Faster model loading from solid-state storage

### For Lower-End Hardware:
- Reduce `max_length` parameter in inference.py
- Use smaller batch sizes
- Consider using a smaller quantized model variant

## Development

### Adding New Features
1. Backend changes: Modify `app.py` or `inference.py`
2. Frontend changes: Update components in `src/components/`
3. Test locally before deployment

### API Endpoints
- `POST /generate`: Generate text from prompt
  - Body: `{"prompt": "string", "temperature": float}`
  - Response: `{"output": "string", "time_taken": float}`

## License

MIT License - See LICENSE file for details

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review logs in `logs/output_log.txt`
3. Open an issue on GitHub with system details and error messages
