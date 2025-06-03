#!/bin/bash

echo "========================================"
echo "    Local AI Writer Setup Script"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅${NC} $1"
}

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_info() {
    echo -e "${BLUE}🔧${NC} $1"
}

print_success() {
    echo -e "${GREEN}🎉${NC} $1"
}

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        print_error "Python is not installed or not in PATH"
        echo "Please install Python 3.9+ from https://python.org"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    print_error "Node.js is not installed or not in PATH"
    echo "Please install Node.js from https://nodejs.org"
    exit 1
fi

print_status "Python and Node.js are installed"
echo

# Setup backend
print_info "Setting up backend..."
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
$PYTHON_CMD -m venv venv
if [ $? -ne 0 ]; then
    print_error "Failed to create virtual environment"
    exit 1
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt
if [ $? -ne 0 ]; then
    print_error "Failed to install Python dependencies"
    exit 1
fi

print_status "Backend setup complete"
echo

# Setup frontend
print_info "Setting up frontend..."
cd ../frontend

# Install Node.js dependencies
echo "Installing Node.js dependencies..."
npm install
if [ $? -ne 0 ]; then
    print_error "Failed to install Node.js dependencies"
    exit 1
fi

print_status "Frontend setup complete"
echo

# Go back to root directory
cd ..

print_success "Setup complete!"
echo
echo "Next steps:"
echo "1. Download the model: cd backend && source venv/bin/activate && python download_model.py"
echo "2. Start backend: cd backend && source venv/bin/activate && uvicorn app:app --reload"
echo "3. Start frontend: cd frontend && npm start"
echo
echo "The application will be available at http://localhost:3000"
echo
