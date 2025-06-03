"""
FastAPI backend for Local AI Writer application.
Provides REST API for text generation using local Llama3 model.
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
import time
import os
import logging
from pathlib import Path
from datetime import datetime
from inference import generate_text, get_inference_engine

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Local AI Writer API",
    description="Local text generation API using Llama3",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Ensure logs directory exists
logs_dir = Path("../logs")
logs_dir.mkdir(exist_ok=True)
log_file = logs_dir / "output_log.txt"

class GenerateRequest(BaseModel):
    """Request model for text generation."""
    prompt: str = Field(..., min_length=1, max_length=1000, description="Text prompt for generation")
    temperature: float = Field(0.7, ge=0.0, le=1.0, description="Sampling temperature")
    max_new_tokens: int = Field(200, ge=10, le=500, description="Maximum new tokens to generate")

class GenerateResponse(BaseModel):
    """Response model for text generation."""
    output: str
    time_taken: float
    prompt: str
    temperature: float
    timestamp: str

class HealthResponse(BaseModel):
    """Health check response."""
    status: str
    model_info: dict
    timestamp: str

def log_generation(prompt: str, temperature: float, output: str, time_taken: float):
    """Log generation to file."""
    try:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"{timestamp} | {prompt[:100]}{'...' if len(prompt) > 100 else ''} | {temperature} | {time_taken:.2f}s | {output[:200]}{'...' if len(output) > 200 else ''}\n"
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(log_entry)
            
        logger.info(f"📝 Logged generation to {log_file}")
    except Exception as e:
        logger.error(f"❌ Error logging generation: {e}")

@app.get("/", response_model=dict)
async def root():
    """Root endpoint."""
    return {
        "message": "Local AI Writer API",
        "version": "1.0.0",
        "endpoints": {
            "generate": "/generate",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        engine = get_inference_engine()
        model_info = engine.get_model_info()
        
        return HealthResponse(
            status="healthy",
            model_info=model_info,
            timestamp=datetime.now().isoformat()
        )
    except Exception as e:
        logger.error(f"❌ Health check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Service unhealthy: {str(e)}")

@app.post("/generate", response_model=GenerateResponse)
async def generate_text_endpoint(request: GenerateRequest):
    """
    Generate text from a prompt using the local Llama3 model.
    
    Args:
        request: Generation request with prompt, temperature, and max_new_tokens
        
    Returns:
        Generated text response with metadata
    """
    try:
        logger.info(f"🔄 Generating text for prompt: {request.prompt[:50]}...")
        
        start_time = time.time()
        
        # Generate text
        output = generate_text(
            prompt=request.prompt,
            temperature=request.temperature,
            max_new_tokens=request.max_new_tokens
        )
        
        time_taken = time.time() - start_time
        timestamp = datetime.now().isoformat()
        
        # Log the generation
        log_generation(request.prompt, request.temperature, output, time_taken)
        
        logger.info(f"✅ Generation completed in {time_taken:.2f}s")
        
        return GenerateResponse(
            output=output,
            time_taken=time_taken,
            prompt=request.prompt,
            temperature=request.temperature,
            timestamp=timestamp
        )
        
    except Exception as e:
        logger.error(f"❌ Error during generation: {e}")
        raise HTTPException(status_code=500, detail=f"Generation failed: {str(e)}")

@app.get("/logs")
async def get_logs(lines: int = 50):
    """
    Get recent log entries.
    
    Args:
        lines: Number of recent lines to return (default: 50)
        
    Returns:
        Recent log entries
    """
    try:
        if not log_file.exists():
            return {"logs": [], "message": "No logs found"}
        
        with open(log_file, "r", encoding="utf-8") as f:
            all_lines = f.readlines()
        
        recent_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
        
        return {
            "logs": [line.strip() for line in recent_lines],
            "total_entries": len(all_lines),
            "showing": len(recent_lines)
        }
        
    except Exception as e:
        logger.error(f"❌ Error reading logs: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to read logs: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    
    logger.info("🚀 Starting Local AI Writer API...")
    logger.info("📍 API will be available at: http://localhost:8000")
    logger.info("📚 API documentation at: http://localhost:8000/docs")
    
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
