#!/usr/bin/env python3
"""
Setup script for Resume Matcher Application
Automates the installation and setup process
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and handle errors"""
    print(f"\n🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed: {e.stderr}")
        return False

def check_python_version():
    """Check if Python version is compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 11):
        print("❌ Python 3.11+ required. Current version:", sys.version)
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} is compatible")
    return True

def main():
    """Main setup function"""
    print("🚀 Resume Matcher Setup Script")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Install packages
    packages = [
        "streamlit",
        "pandas", 
        "numpy",
        "scikit-learn",
        "spacy",
        "pymupdf",
        "plotly"
    ]
    
    print(f"\n📦 Installing {len(packages)} packages...")
    package_string = " ".join(packages)
    
    if not run_command(f"pip install {package_string}", "Installing Python packages"):
        print("\n💡 Alternative installation methods:")
        print("   • Try: pip install --user " + package_string)
        print("   • Try: python -m pip install " + package_string)
        print("   • Use virtual environment (recommended)")
        sys.exit(1)
    
    # Download spaCy model
    if not run_command("python -m spacy download en_core_web_sm", "Downloading spaCy English model"):
        print("\n💡 You can download the model later with:")
        print("   python -m spacy download en_core_web_sm")
    
    # Check if all imports work
    print("\n🔍 Testing imports...")
    try:
        import streamlit
        import pandas
        import numpy
        import sklearn
        import spacy
        import fitz  # PyMuPDF
        import plotly
        print("✅ All packages imported successfully!")
    except ImportError as e:
        print(f"❌ Import test failed: {e}")
        sys.exit(1)
    
    print("\n🎉 Setup completed successfully!")
    print("\n📖 Next steps:")
    print("1. Run the application:")
    print("   streamlit run app.py")
    print("\n2. Open your browser to:")
    print("   http://localhost:8501")
    print("\n3. Start analyzing resumes!")
    print("\n📚 For detailed instructions, see README.md")

if __name__ == "__main__":
    main()