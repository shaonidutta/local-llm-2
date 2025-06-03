#!/usr/bin/env python3
"""
Model download script for Llama3 8B Instruct model.
This script downloads the model from Hugging Face and prepares it for local inference.
"""

import os
import sys
from pathlib import Path
from transformers import AutoTokenizer, AutoModelForCausalLM
import torch

def check_requirements():
    """Check if required packages are installed."""
    try:
        import transformers
        import torch
        import accelerate
        import bitsandbytes
        print("✅ All required packages are installed.")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e}")
        print("Please run: pip install -r requirements.txt")
        return False

def download_model():
    """Download and cache the Llama3 model."""
    model_name = "meta-llama/Meta-Llama-3-8B-Instruct"
    models_dir = Path("../models")
    models_dir.mkdir(exist_ok=True)
    
    print(f"🔄 Downloading {model_name}...")
    print("This may take a while (several GB download)...")
    
    try:
        # Download tokenizer
        print("📥 Downloading tokenizer...")
        tokenizer = AutoTokenizer.from_pretrained(
            model_name,
            cache_dir=str(models_dir),
            token=None  # You may need a HuggingFace token for gated models
        )
        
        # Download model with 4-bit quantization
        print("📥 Downloading model with 4-bit quantization...")
        model = AutoModelForCausalLM.from_pretrained(
            model_name,
            cache_dir=str(models_dir),
            torch_dtype=torch.float16,
            device_map="auto",
            load_in_4bit=True,
            token=None  # You may need a HuggingFace token for gated models
        )
        
        print("✅ Model downloaded successfully!")
        print(f"📁 Model cached in: {models_dir.absolute()}")
        
        # Test the model
        print("🧪 Testing model...")
        test_prompt = "Hello, how are you?"
        inputs = tokenizer(test_prompt, return_tensors="pt")
        
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=20,
                do_sample=True,
                temperature=0.7,
                pad_token_id=tokenizer.eos_token_id
            )
        
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(f"✅ Test successful! Response: {response}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error downloading model: {e}")
        print("\nTroubleshooting:")
        print("1. Check your internet connection")
        print("2. Ensure you have enough disk space (>10GB)")
        print("3. For gated models, you may need a HuggingFace token")
        print("4. Try running: huggingface-cli login")
        return False

def main():
    """Main function."""
    print("🚀 Llama3 Model Download Script")
    print("=" * 40)
    
    if not check_requirements():
        sys.exit(1)
    
    if download_model():
        print("\n🎉 Setup complete! You can now run the application.")
        print("Next steps:")
        print("1. Start the backend: uvicorn app:app --reload")
        print("2. Start the frontend: cd ../frontend && npm start")
    else:
        print("\n❌ Setup failed. Please check the error messages above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
