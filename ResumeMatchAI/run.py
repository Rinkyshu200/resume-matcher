#!/usr/bin/env python3
"""
Quick run script for Resume Matcher Application
Usage: python run.py [port]
"""

import subprocess
import sys
import os

def main():
    """Main run function"""
    port = "8501"
    
    # Check if port is provided as argument
    if len(sys.argv) > 1:
        port = sys.argv[1]
    
    print(f"🚀 Starting Resume Matcher on port {port}...")
    print("📂 Working directory:", os.getcwd())
    
    # Check if app.py exists
    if not os.path.exists("app.py"):
        print("❌ app.py not found in current directory")
        print("💡 Make sure you're in the Resume Matcher project folder")
        sys.exit(1)
    
    # Build the command
    command = f"streamlit run app.py --server.port {port}"
    
    print(f"🔄 Running: {command}")
    print(f"🌐 App will be available at: http://localhost:{port}")
    print("💡 Press Ctrl+C to stop the application")
    print("-" * 50)
    
    try:
        # Run the application
        subprocess.run(command, shell=True, check=True)
    except KeyboardInterrupt:
        print("\n👋 Application stopped by user")
    except subprocess.CalledProcessError as e:
        print(f"\n❌ Failed to start application: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Check if all dependencies are installed:")
        print("   python setup.py")
        print("2. Try a different port:")
        print(f"   python run.py {int(port) + 1}")
        print("3. Check if Streamlit is installed:")
        print("   pip install streamlit")

if __name__ == "__main__":
    main()