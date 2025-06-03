"""
Local inference module for Llama3 model.
Handles model loading, text generation, and optimization.
"""

import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from pathlib import Path
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LlamaInference:
    """Llama3 inference engine with optimizations."""
    
    def __init__(self, model_name="meta-llama/Meta-Llama-3-8B-Instruct"):
        self.model_name = model_name
        self.model = None
        self.tokenizer = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.models_dir = Path("../models")
        
        logger.info(f"🔧 Initializing inference engine on {self.device}")
        self._load_model()
    
    def _load_model(self):
        """Load the model and tokenizer."""
        try:
            logger.info("📥 Loading tokenizer...")
            self.tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                cache_dir=str(self.models_dir),
                padding_side="left"
            )
            
            # Set pad token if not exists
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
            
            logger.info("📥 Loading model with 4-bit quantization...")
            self.model = AutoModelForCausalLM.from_pretrained(
                self.model_name,
                cache_dir=str(self.models_dir),
                torch_dtype=torch.float16,
                device_map="auto",
                load_in_4bit=True,
                trust_remote_code=True
            )
            
            self.model.eval()
            logger.info("✅ Model loaded successfully!")
            
        except Exception as e:
            logger.error(f"❌ Error loading model: {e}")
            raise
    
    def generate_text(self, prompt: str, temperature: float = 0.7, max_new_tokens: int = 200) -> str:
        """
        Generate text from a prompt.
        
        Args:
            prompt: Input text prompt
            temperature: Sampling temperature (0.0 to 1.0)
            max_new_tokens: Maximum number of new tokens to generate
            
        Returns:
            Generated text string
        """
        if not self.model or not self.tokenizer:
            raise RuntimeError("Model not loaded. Call _load_model() first.")
        
        try:
            start_time = time.time()
            
            # Format prompt for Llama3 Instruct
            formatted_prompt = f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n\n{prompt}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n\n"
            
            # Tokenize input
            inputs = self.tokenizer(
                formatted_prompt,
                return_tensors="pt",
                padding=True,
                truncation=True,
                max_length=512
            )
            
            # Move to device
            inputs = {k: v.to(self.device) for k, v in inputs.items()}
            
            # Generate
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=max_new_tokens,
                    temperature=temperature,
                    do_sample=True if temperature > 0 else False,
                    top_p=0.9,
                    repetition_penalty=1.1,
                    pad_token_id=self.tokenizer.eos_token_id,
                    eos_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode response
            full_response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
            
            # Extract only the assistant's response
            if "<|start_header_id|>assistant<|end_header_id|>" in full_response:
                response = full_response.split("<|start_header_id|>assistant<|end_header_id|>")[-1].strip()
            else:
                response = full_response[len(formatted_prompt):].strip()
            
            generation_time = time.time() - start_time
            logger.info(f"⚡ Generated {len(response)} characters in {generation_time:.2f}s")
            
            return response
            
        except Exception as e:
            logger.error(f"❌ Error during generation: {e}")
            return f"Error generating text: {str(e)}"
    
    def get_model_info(self) -> dict:
        """Get information about the loaded model."""
        if not self.model:
            return {"status": "not_loaded"}
        
        return {
            "status": "loaded",
            "model_name": self.model_name,
            "device": self.device,
            "parameters": sum(p.numel() for p in self.model.parameters()),
            "memory_usage": torch.cuda.memory_allocated() if torch.cuda.is_available() else 0
        }

# Global inference engine instance
inference_engine = None

def get_inference_engine():
    """Get or create the global inference engine."""
    global inference_engine
    if inference_engine is None:
        inference_engine = LlamaInference()
    return inference_engine

def generate_text(prompt: str, temperature: float = 0.7, max_new_tokens: int = 200) -> str:
    """Convenience function for text generation."""
    engine = get_inference_engine()
    return engine.generate_text(prompt, temperature, max_new_tokens)
