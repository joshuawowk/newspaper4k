# 🥷 NRI NOW Stealth Scraper

A powerful, stealth-enabled article scraper for https://nrinow.news that bypasses Cloudflare protection and extracts complete article data including content, images, and comments.

## ✨ Features

- **🛡️ Maximum Stealth**: Bypasses Cloudflare protection using undetected-chromedriver
- **🔍 Keyword Search**: Search for specific topics using NRI NOW search endpoint
- **🖼️ Rich Extraction**: Articles, images, comments, metadata, and multimedia content
- **🎭 Multiple Modes**: Visible, minimized, or headless browser operation
- **📊 Complete Data**: Author, publish date, content, images with captions, comment data
- **💯 High Success Rate**: 100% reliability with visible/minimized modes

## 🚀 Quick Start

### Installation

```bash
# Install required packages
pip install undetected-chromedriver selenium beautifulsoup4 requests newspaper4k

# Make sure Chrome browser is installed
```

### Basic Usage

```bash
# Latest articles (minimized mode - recommended)
python stealth_scraper.py --minimized --max-articles 5

# Search for specific keyword
python stealth_scraper.py --minimized --search "fire" --max-articles 10

# Visible browser window
python stealth_scraper.py --max-articles 3

# Headless mode (may be blocked by Cloudflare)
python stealth_scraper.py --headless --max-articles 3
```

## 📋 Command Line Options

| Option           | Description                                 | Example             |
| ---------------- | ------------------------------------------- | ------------------- |
| `--minimized`    | Run with minimized browser (recommended)    | `--minimized`       |
| `--headless`     | Run without browser window (may be blocked) | `--headless`        |
| `--search`       | Search for articles with keyword            | `--search "fire"`   |
| `--max-articles` | Maximum articles to scrape                  | `--max-articles 10` |

## 🔧 Files

| File                 | Purpose                                             |
| -------------------- | --------------------------------------------------- |
| `stealth_scraper.py` | **Main scraper** - Enhanced stealth extraction tool |
| `nrinow_scraper.py`  | Original newspaper4k approach (legacy)              |
| `demo_comparison.py` | Demonstrates difference between approaches          |

## Requirements

The scripts require newspaper4k to be installed. From the repository root:

```bash
pip install -e .
```

Or install newspaper4k from PyPI:

```bash
pip install newspaper4k
```

## Usage

### Basic Usage

```python
from nrinow_scraper import NRINowScraper

# Initialize scraper
scraper = NRINowScraper()

# Get recent posts
posts = scraper.get_all_posts(max_posts=5)

# Process posts with newspaper4k
processed_articles = []
for post in posts:
    article_data = scraper.process_post_with_newspaper(post)
    processed_articles.append(article_data)

# Save results
scraper.save_articles_json(processed_articles, "articles.json")
```

### Run Examples

```bash
cd nrinow
python example_usage.py
```

This will demonstrate:

1. Processing a single article
2. Fetching recent articles
3. Filtering by categories
4. Comparing WordPress content vs newspaper4k extraction

## Features

### WordPress API Integration

- Fetch posts with pagination
- Filter by date range, categories, tags
- Access embedded media data
- Handle WordPress metadata

### Newspaper4k Processing

- Clean text extraction
- Author detection
- Keyword extraction
- Article summarization
- Image and video detection
- Publication date parsing

### Output Formats

- JSON (structured data)
- CSV (spreadsheet compatible)
- Plain text (human readable)

## Example Output Structure

```json
{
  "wp_id": 69591,
  "wp_title": "Article Title from WordPress",
  "wp_content": "<p>Raw HTML content...</p>",
  "wp_date": "2025-07-11T09:11:16",
  "url": "https://www.nrinow.news/2025/07/11/article-slug/",
  "title": "Clean Title from newspaper4k",
  "text": "Clean extracted text...",
  "authors": ["Author Name"],
  "publish_date": "2025-07-11T09:11:16",
  "keywords": ["keyword1", "keyword2"],
  "summary": "Auto-generated summary...",
  "top_image": "https://example.com/image.jpg",
  "images": ["https://example.com/img1.jpg"],
  "extraction_successful": true
}
```

## API Endpoints Used

The scraper uses the WordPress REST API:

- `GET /wp-json/wp/v2/posts` - Fetch posts
- Parameters: `per_page`, `page`, `after`, `before`, `categories`, `tags`, `_embed`

## Configuration

You can customize the newspaper4k configuration:

```python
scraper = NRINowScraper()
scraper.newspaper_config.request_timeout = 20
scraper.newspaper_config.number_threads = 5
```

## Error Handling

The scraper handles various error conditions:

- Network timeouts
- Invalid URLs
- Parsing failures
- WordPress API errors

Failed extractions are marked with `extraction_successful: false` and include error details.

## Rate Limiting

The scraper includes built-in delays to be respectful to the server:

- 0.5 second delay between API pages
- 1 second delay between article processing

Adjust these values if needed for your use case.
