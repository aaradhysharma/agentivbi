#!/usr/bin/env python3
"""
agentivBI Startup Script
This script helps you set up and run the agentivBI application.
"""

import os
import sys
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is 3.8 or higher"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version.split()[0]}")
    return True

def check_requirements():
    """Check if requirements are installed"""
    try:
        import flask
        import pandas
        import plotly
        import openai
        print("✅ Required packages are installed")
        return True
    except ImportError as e:
        print(f"❌ Missing required package: {e.name}")
        print("   Run: pip install -r requirements.txt")
        return False

def check_env_file():
    """Check if .env file exists and has required variables"""
    env_file = Path('.env')
    if not env_file.exists():
        print("❌ .env file not found")
        print("   1. Copy env_template.txt to .env")
        print("   2. Add your OpenAI API key to the .env file")
        return False
    
    # Read .env file and check for required variables
    env_content = env_file.read_text()
    if 'OPENAI_API_KEY=your_openai_api_key_here' in env_content:
        print("❌ OpenAI API key not set in .env file")
        print("   Please edit .env and add your OpenAI API key")
        return False
    
    print("✅ Environment file configured")
    return True

def install_requirements():
    """Install requirements if user chooses to"""
    response = input("Would you like to install requirements now? (y/n): ").lower()
    if response == 'y':
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Requirements installed successfully")
            return True
        except subprocess.CalledProcessError:
            print("❌ Failed to install requirements")
            return False
    return False

def create_env_file():
    """Create .env file from template"""
    response = input("Would you like to create a .env file from template? (y/n): ").lower()
    if response == 'y':
        try:
            with open('env_template.txt', 'r') as template:
                with open('.env', 'w') as env_file:
                    env_file.write(template.read())
            print("✅ .env file created from template")
            print("   Please edit .env and add your OpenAI API key")
            return True
        except Exception as e:
            print(f"❌ Failed to create .env file: {e}")
            return False
    return False

def main():
    """Main startup function"""
    print("🚀 agentivBI Startup Checker")
    print("=" * 40)
    
    # Check prerequisites
    checks_passed = 0
    total_checks = 3
    
    if check_python_version():
        checks_passed += 1
    
    if check_requirements():
        checks_passed += 1
    else:
        if install_requirements():
            checks_passed += 1
    
    if check_env_file():
        checks_passed += 1
    else:
        if create_env_file():
            print("   You still need to edit .env with your OpenAI API key")
    
    print("\n" + "=" * 40)
    print(f"Setup Status: {checks_passed}/{total_checks} checks passed")
    
    if checks_passed == total_checks:
        print("🎉 All checks passed! Starting agentivBI...")
        print("\n📖 Quick Start Guide:")
        print("   1. Open http://localhost:5000 in your browser")
        print("   2. Upload two CSV/Excel files")
        print("   3. Use natural language to join tables or create charts")
        print("\n📁 Sample data files are available in the sample_data/ folder")
        print("\n🚀 Starting application...")
        
        # Start the application
        try:
            os.system("python app.py")
        except KeyboardInterrupt:
            print("\n👋 agentivBI stopped")
    else:
        print("\n❌ Please fix the issues above before starting the application")
        print("\n📚 For help, check the README.md file")

if __name__ == "__main__":
    main() 