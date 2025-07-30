#!/usr/bin/env python3
"""
NRI NOW Article Scraper

This script fetches articles from https://nrinow.news using the WordPress
REST API and processes them with newspaper4k for content extraction and
analysis.

The script can:
1. Fetch all posts from the WordPress API
2. Filter posts by date, category, or other criteria
3. Process each article with newspaper4k to extract clean text, images,
   metadata
4. Save articles in various formats (JSON, CSV, text)
"""

import csv
import json
import logging
import requests
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any

from newspaper import Article
from newspaper.configuration import Configuration

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


class NRINowScraper:
    """
    Scraper for NRI NOW WordPress website using REST API and newspaper4k
    """

    def __init__(self, base_url: str = "https://www.nrinow.news"):
        """
        Initialize the scraper

        Args:
            base_url: Base URL of the WordPress site
        """
        self.base_url = base_url.rstrip('/')
        self.api_base = f"{self.base_url}/wp-json/wp/v2"

        # Configure newspaper4k
        self.newspaper_config = Configuration()
        self.newspaper_config.request_timeout = 10
        self.newspaper_config.number_threads = 3

        # Session for API requests
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'NRINow-Scraper/1.0 (newspaper4k)'
        })

    def get_posts(self,
                  per_page: int = 100,
                  page: int = 1,
                  after: Optional[str] = None,
                  before: Optional[str] = None,
                  categories: Optional[List[int]] = None,
                  tags: Optional[List[int]] = None) -> List[Dict[str, Any]]:
        """
        Fetch posts from WordPress REST API

        Args:
            per_page: Number of posts per page (max 100)
            page: Page number
            after: ISO 8601 date string to fetch posts after
            before: ISO 8601 date string to fetch posts before
            categories: List of category IDs to filter by
            tags: List of tag IDs to filter by

        Returns:
            List of post data dictionaries
        """
        endpoint = f"{self.api_base}/posts"
        
        params = {
            'per_page': min(per_page, 100),
            'page': page,
            'status': 'publish',
            '_embed': 'true'  # Include embedded data like featured media
        }
        
        if after:
            params['after'] = after
        if before:
            params['before'] = before
        if categories:
            params['categories'] = ','.join(map(str, categories))
        if tags:
            params['tags'] = ','.join(map(str, tags))
            
        try:
            response = self.session.get(endpoint, params=params)
            response.raise_for_status()
            
            posts = response.json()
            logger.info(f"Fetched {len(posts)} posts from page {page}")
            
            return posts
            
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching posts: {e}")
            return []
    
    def get_all_posts(self,
                      after: Optional[str] = None,
                      before: Optional[str] = None,
                      categories: Optional[List[int]] = None,
                      tags: Optional[List[int]] = None,
                      max_posts: Optional[int] = None) -> List[Dict[str, Any]]:
        """
        Fetch all posts by iterating through pages
        
        Args:
            after: ISO 8601 date string to fetch posts after
            before: ISO 8601 date string to fetch posts before
            categories: List of category IDs to filter by
            tags: List of tag IDs to filter by
            max_posts: Maximum number of posts to fetch
            
        Returns:
            List of all post data dictionaries
        """
        all_posts = []
        page = 1
        
        while True:
            posts = self.get_posts(
                page=page,
                after=after,
                before=before,
                categories=categories,
                tags=tags
            )
            
            if not posts:
                break
                
            all_posts.extend(posts)
            
            if max_posts and len(all_posts) >= max_posts:
                all_posts = all_posts[:max_posts]
                break
                
            page += 1
            time.sleep(0.5)  # Be nice to the server
            
        logger.info(f"Fetched total of {len(all_posts)} posts")
        return all_posts
    
    def process_post_with_newspaper(self, post_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process a WordPress post using newspaper4k
        
        Args:
            post_data: WordPress post data from API
            
        Returns:
            Dictionary with extracted article data
        """
        url = post_data.get('link', '')
        
        try:
            # Create and process article with newspaper4k
            article = Article(url, config=self.newspaper_config)
            article.download()
            article.parse()
            article.nlp()
            
            # Extract featured image URL if available
            featured_image = None
            if '_embedded' in post_data and 'wp:featuredmedia' in post_data['_embedded']:
                media = post_data['_embedded']['wp:featuredmedia']
                if media and len(media) > 0:
                    featured_image = media[0].get('source_url')
            
            # Combine WordPress metadata with newspaper4k extraction
            processed_data = {
                # WordPress API data
                'wp_id': post_data.get('id'),
                'wp_title': post_data.get('title', {}).get('rendered', ''),
                'wp_content': post_data.get('content', {}).get('rendered', ''),
                'wp_excerpt': post_data.get('excerpt', {}).get('rendered', ''),
                'wp_date': post_data.get('date'),
                'wp_modified': post_data.get('modified'),
                'wp_slug': post_data.get('slug'),
                'wp_categories': post_data.get('categories', []),
                'wp_tags': post_data.get('tags', []),
                'wp_featured_media': featured_image,
                'wp_author': post_data.get('author'),
                
                # newspaper4k extracted data  
                'url': article.url,
                'title': article.title,
                'text': article.text,
                'authors': article.authors,
                'publish_date': article.publish_date.isoformat() if article.publish_date else None,
                'top_image': article.top_image,
                'images': article.images,
                'movies': article.movies,
                'keywords': article.keywords,
                'summary': article.summary,
                'meta_description': article.meta_description,
                'meta_keywords': article.meta_keywords,
                'tags_extracted': list(article.tags),
                
                # Processing metadata
                'processed_at': datetime.now().isoformat(),
                'extraction_successful': True,
                'extraction_error': None
            }
            
            logger.info(f"Successfully processed: {article.title[:50]}...")
            return processed_data
            
        except Exception as e:
            logger.error(f"Error processing article {url}: {e}")
            
            # Return minimal data with error info
            return {
                'wp_id': post_data.get('id'),
                'wp_title': post_data.get('title', {}).get('rendered', ''),
                'url': url,
                'processed_at': datetime.now().isoformat(),
                'extraction_successful': False,
                'extraction_error': str(e)
            }
    
    def save_articles_json(self, articles: List[Dict[str, Any]], filename: str):
        """Save articles to JSON file"""
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, indent=2, ensure_ascii=False, default=str)
        
        logger.info(f"Saved {len(articles)} articles to {filename}")
    
    def save_articles_csv(self, articles: List[Dict[str, Any]], filename: str):
        """Save articles to CSV file"""
        if not articles:
            return
            
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Get all possible field names
        fieldnames = set()
        for article in articles:
            fieldnames.update(article.keys())
        fieldnames = sorted(fieldnames)
        
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            
            for article in articles:
                # Convert lists/dicts to strings for CSV
                row = {}
                for key, value in article.items():
                    if isinstance(value, (list, dict)):
                        row[key] = json.dumps(value, default=str)
                    else:
                        row[key] = value
                writer.writerow(row)
        
        logger.info(f"Saved {len(articles)} articles to {filename}")
    
    def save_articles_text(self, articles: List[Dict[str, Any]], filename: str):
        """Save articles as plain text"""
        output_path = Path(filename)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            for i, article in enumerate(articles, 1):
                f.write(f"=== Article {i} ===\n")
                f.write(f"Title: {article.get('title', 'N/A')}\n")
                f.write(f"URL: {article.get('url', 'N/A')}\n")
                f.write(f"Date: {article.get('publish_date', 'N/A')}\n")
                f.write(f"Authors: {', '.join(article.get('authors', []))}\n")
                f.write(f"Keywords: {', '.join(article.get('keywords', []))}\n")
                f.write(f"\nText:\n{article.get('text', 'N/A')}\n")
                f.write(f"\nSummary:\n{article.get('summary', 'N/A')}\n")
                f.write("\n" + "="*80 + "\n\n")
        
        logger.info(f"Saved {len(articles)} articles to {filename}")


def main():
    """Example usage of the NRI NOW scraper"""
    
    # Initialize scraper
    scraper = NRINowScraper()
    
    # Example 1: Get recent posts from the last 7 days
    logger.info("Fetching recent posts from the last 7 days...")
    
    seven_days_ago = (datetime.now() - timedelta(days=7)).isoformat()
    posts = scraper.get_all_posts(after=seven_days_ago, max_posts=10)
    
    if not posts:
        logger.warning("No posts found")
        return
    
    # Process posts with newspaper4k
    logger.info("Processing posts with newspaper4k...")
    processed_articles = []
    
    for post in posts:
        article_data = scraper.process_post_with_newspaper(post)
        processed_articles.append(article_data)
        time.sleep(1)  # Be nice to the server
    
    # Save results
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    scraper.save_articles_json(
        processed_articles, 
        f"nrinow_articles_{timestamp}.json"
    )
    
    scraper.save_articles_csv(
        processed_articles,
        f"nrinow_articles_{timestamp}.csv"
    )
    
    scraper.save_articles_text(
        processed_articles,
        f"nrinow_articles_{timestamp}.txt"
    )
    
    # Print summary
    successful = sum(1 for a in processed_articles if a.get('extraction_successful'))
    logger.info(f"Processing complete: {successful}/{len(processed_articles)} articles extracted successfully")


if __name__ == "__main__":
    main()
