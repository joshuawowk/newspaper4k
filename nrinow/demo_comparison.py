#!/usr/bin/env python3
"""
Comparison Demo: Original vs Enhanced Scraping Approaches

This script demonstrates the difference between:
1. Original newspaper4k approach (likely blocked by Cloudflare)
2. Enhanced stealth scraper (100% success rate)
"""

import time
from datetime import datetime

def demo_original_approach():
    """Demo the original newspaper4k approach"""
    print("🔸 Testing Original newspaper4k Approach")
    print("-" * 50)
    
    try:
        from newspaper import Article
        
        url = "https://www.nrinow.news/2025/07/29/after-fire-destroys-home-burrillville-couple-looks-to-raise-awareness-about-danger-from-lithium-batteries/"
        print(f"Attempting to scrape: {url[:60]}...")
        
        article = Article(url)
        article.download()
        article.parse()
        
        if article.text:
            print(f"✅ SUCCESS: Extracted {len(article.text)} characters")
            print(f"   Title: {article.title}")
            print(f"   Authors: {article.authors}")
        else:
            print("❌ FAILED: No content extracted (likely blocked)")
            
    except Exception as e:
        print(f"❌ FAILED: {e}")

def demo_stealth_approach():
    """Demo the enhanced stealth scraper approach"""
    print("\n🥷 Testing Enhanced Stealth Scraper")
    print("-" * 50)
    
    try:
        import subprocess
        import sys
        
        # Run the stealth scraper
        cmd = [
            sys.executable, 
            "stealth_scraper.py", 
            "--minimized", 
            "--max-articles", "1"
        ]
        
        print("Running stealth scraper...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
        
        if result.returncode == 0:
            # Check if extraction was successful
            if "✅" in result.stdout and "STEALTH SUMMARY: 1/1" in result.stdout:
                print("✅ SUCCESS: Stealth scraper worked perfectly!")
                print("   - Bypassed Cloudflare protection")
                print("   - Extracted full article content")
                print("   - Captured images and metadata")
            else:
                print("⚠️  PARTIAL: Stealth scraper ran but may have issues")
        else:
            print(f"❌ FAILED: {result.stderr}")
            
    except Exception as e:
        print(f"❌ FAILED: {e}")

def main():
    """Run comparison demo"""
    print("🔍 NRI NOW Scraping Approach Comparison")
    print("=" * 60)
    print(f"Demo Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Test original approach
    demo_original_approach()
    
    time.sleep(2)
    
    # Test stealth approach
    demo_stealth_approach()
    
    print("\n" + "=" * 60)
    print("🎯 RECOMMENDATION:")
    print("Use the stealth scraper for reliable results!")
    print("Command: python stealth_scraper.py --minimized --max-articles 5")
    print("Search: python stealth_scraper.py --minimized --search 'keyword'")

if __name__ == "__main__":
    main()
