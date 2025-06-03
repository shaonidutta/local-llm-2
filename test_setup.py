#!/usr/bin/env python3
"""
Test script to verify the Local AI Writer setup.
Run this after completing the setup to ensure everything is working.
"""

import sys
import os
import subprocess
import importlib.util
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.9+"""
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro} (OK)")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} (Need 3.9+)")
        return False

def check_package(package_name):
    """Check if a Python package is installed"""
    try:
        spec = importlib.util.find_spec(package_name)
        if spec is not None:
            print(f"✅ {package_name} (installed)")
            return True
        else:
            print(f"❌ {package_name} (not found)")
            return False
    except ImportError:
        print(f"❌ {package_name} (import error)")
        return False

def check_node():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"✅ Node.js {version} (OK)")
            return True
        else:
            print("❌ Node.js (not found)")
            return False
    except FileNotFoundError:
        print("❌ Node.js (not found)")
        return False

def check_directory_structure():
    """Check if required directories and files exist"""
    required_paths = [
        "backend/requirements.txt",
        "backend/app.py",
        "backend/inference.py",
        "backend/download_model.py",
        "frontend/package.json",
        "frontend/src/App.jsx",
        "frontend/src/api.js",
        "README.md"
    ]
    
    all_exist = True
    for path in required_paths:
        if Path(path).exists():
            print(f"✅ {path}")
        else:
            print(f"❌ {path} (missing)")
            all_exist = False
    
    return all_exist

def check_virtual_env():
    """Check if virtual environment exists"""
    venv_path = Path("backend/venv")
    if venv_path.exists():
        print("✅ Virtual environment (exists)")
        return True
    else:
        print("❌ Virtual environment (not found)")
        return False

def check_node_modules():
    """Check if Node.js modules are installed"""
    node_modules_path = Path("frontend/node_modules")
    if node_modules_path.exists():
        print("✅ Node.js modules (installed)")
        return True
    else:
        print("❌ Node.js modules (not found)")
        return False

def main():
    """Main test function"""
    print("🧪 Local AI Writer Setup Test")
    print("=" * 40)
    
    all_checks_passed = True
    
    print("\n📋 Checking Python environment...")
    all_checks_passed &= check_python_version()
    
    print("\n📋 Checking directory structure...")
    all_checks_passed &= check_directory_structure()
    
    print("\n📋 Checking virtual environment...")
    all_checks_passed &= check_virtual_env()
    
    print("\n📋 Checking Node.js...")
    all_checks_passed &= check_node()
    
    print("\n📋 Checking Node.js modules...")
    all_checks_passed &= check_node_modules()
    
    if os.path.exists("backend/venv"):
        print("\n📋 Checking Python packages in virtual environment...")
        # This is a simplified check - in practice you'd activate the venv first
        required_packages = ['fastapi', 'uvicorn', 'torch', 'transformers']
        for package in required_packages:
            # Note: This won't work properly without activating venv first
            print(f"📦 {package} (check manually in activated venv)")
    
    print("\n" + "=" * 40)
    if all_checks_passed:
        print("🎉 All basic checks passed!")
        print("\nNext steps:")
        print("1. Activate virtual environment:")
        print("   Windows: backend\\venv\\Scripts\\activate")
        print("   Linux/Mac: source backend/venv/bin/activate")
        print("2. Download model: python backend/download_model.py")
        print("3. Start backend: uvicorn backend.app:app --reload")
        print("4. Start frontend: cd frontend && npm start")
    else:
        print("❌ Some checks failed. Please review the setup instructions.")
        print("\nCommon fixes:")
        print("- Run setup.bat (Windows) or setup.sh (Linux/Mac)")
        print("- Ensure Python 3.9+ and Node.js are installed")
        print("- Check that all files were created correctly")

if __name__ == "__main__":
    main()
