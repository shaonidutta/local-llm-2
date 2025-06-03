#!/bin/bash

echo "========================================"
echo "    Starting Local AI Writer"
echo "========================================"
echo

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_error() {
    echo -e "${RED}❌${NC} $1"
}

print_success() {
    echo -e "${GREEN}✅${NC} $1"
}

print_info() {
    echo -e "${BLUE}🚀${NC} $1"
}

# Check if setup has been run
if [ ! -d "backend/venv" ]; then
    print_error "Backend not set up. Please run setup.sh first."
    exit 1
fi

if [ ! -d "frontend/node_modules" ]; then
    print_error "Frontend not set up. Please run setup.sh first."
    exit 1
fi

print_info "Starting Local AI Writer..."
echo

# Function to start backend
start_backend() {
    echo "Starting backend server..."
    cd backend
    source venv/bin/activate
    uvicorn app:app --reload --host 0.0.0.0 --port 8000
}

# Function to start frontend
start_frontend() {
    echo "Starting frontend server..."
    cd frontend
    npm start
}

# Check if we're in a terminal that supports background processes
if [ -t 1 ]; then
    echo "Starting backend in background..."
    start_backend &
    BACKEND_PID=$!
    
    # Wait a moment for backend to start
    sleep 3
    
    echo "Starting frontend..."
    start_frontend &
    FRONTEND_PID=$!
    
    echo
    print_success "Both servers are starting..."
    echo
    echo "Backend: http://localhost:8000"
    echo "Frontend: http://localhost:3000"
    echo "API Docs: http://localhost:8000/docs"
    echo
    echo "Press Ctrl+C to stop both servers"
    
    # Wait for user to stop
    trap "echo; echo 'Stopping servers...'; kill $BACKEND_PID $FRONTEND_PID 2>/dev/null; exit" INT
    wait
else
    echo "Please run the following commands in separate terminals:"
    echo
    echo "Terminal 1 (Backend):"
    echo "cd backend && source venv/bin/activate && uvicorn app:app --reload"
    echo
    echo "Terminal 2 (Frontend):"
    echo "cd frontend && npm start"
fi
