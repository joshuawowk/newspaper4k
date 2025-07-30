#!/usr/bin/env python3
"""
🚀 Quick Setup Script for NRI NOW Scraper

This script sets up everything needed to run the NRI NOW scraper.
"""

import subprocess
import sys
import os

def install_requirements():
    """Install required packages"""
    print("📦 Installing required packages...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("✅ Requirements installed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def check_chrome():
    """Check if Chrome is installed"""
    print("🌐 Checking for Chrome browser...")
    try:
        # Try to find Chrome in common locations
        chrome_paths = [
            r"C:\Program Files\Google\Chrome\Application\chrome.exe",
            r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/usr/bin/google-chrome",
            "/usr/bin/chromium-browser"
        ]
        
        for path in chrome_paths:
            if os.path.exists(path):
                print(f"✅ Chrome found at: {path}")
                return True
        
        print("⚠️  Chrome not found in common locations")
        print("   Please install Chrome browser manually")
        return False
    except Exception as e:
        print(f"❌ Error checking Chrome: {e}")
        return False

def main():
    """Main setup function"""
    print("🥷 NRI NOW Stealth Scraper Setup")
    print("=" * 40)
    
    # Install requirements
    if not install_requirements():
        return False
    
    # Check Chrome
    check_chrome()
    
    print("\n" + "=" * 40)
    print("🎉 Setup complete!")
    print("\n🚀 Quick start commands:")
    print("   # Latest articles")
    print("   python stealth_scraper.py --minimized --max-articles 5")
    print("\n   # Search articles")
    print("   python stealth_scraper.py --minimized --search \"fire\" --max-articles 10")
    print("\n📖 See README.md for more examples!")
    
    return True

if __name__ == "__main__":
    main()
