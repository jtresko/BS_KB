"""
Intercom Help Center Scraper for BigShort
Extracts all public articles and preserves hierarchical structure.
"""

import requests
from bs4 import BeautifulSoup
import os
import re
import json
import time
from urllib.parse import urljoin, urlparse
from pathlib import Path
import html2text

BASE_URL = "https://help.bigshort.com/en/"
OUTPUT_DIR = Path(__file__).parent.parent / "intercom_export"
DELAY_BETWEEN_REQUESTS = 0.5  # Be nice to the server

# Initialize html2text converter
h2t = html2text.HTML2Text()
h2t.ignore_links = False
h2t.ignore_images = False
h2t.body_width = 0  # Don't wrap lines


def sanitize_filename(name):
    """Convert a string to a safe filename."""
    # Remove or replace invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.strip()
    # Limit length
    if len(name) > 100:
        name = name[:100]
    return name


def get_page(url, retries=3):
    """Fetch a page with retries."""
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    for i in range(retries):
        try:
            response = requests.get(url, headers=headers, timeout=30)
            response.raise_for_status()
            return response.text
        except Exception as e:
            print(f"  Retry {i+1}/{retries} for {url}: {e}")
            time.sleep(2)
    return None


def extract_collections(soup):
    """Extract collection structure from the main help center page."""
    collections = []
    
    # Look for collection containers - Intercom typically uses these patterns
    # Pattern 1: Look for collection links
    collection_links = soup.select('a[href*="/collections/"]')
    
    if collection_links:
        seen = set()
        for link in collection_links:
            href = link.get('href', '')
            if href and href not in seen:
                seen.add(href)
                title = link.get_text(strip=True)
                if title:
                    collections.append({
                        'title': title,
                        'url': urljoin(BASE_URL, href),
                        'sections': []
                    })
    
    # Pattern 2: Look for collection cards/blocks
    if not collections:
        cards = soup.select('[class*="collection"], [class*="card"], [class*="category"]')
        for card in cards:
            link = card.find('a')
            if link and link.get('href'):
                title = card.get_text(strip=True)[:100]
                href = link.get('href')
                if '/collections/' in href or '/articles/' not in href:
                    collections.append({
                        'title': title,
                        'url': urljoin(BASE_URL, href),
                        'sections': []
                    })
    
    return collections


def extract_sections_and_articles(collection_url):
    """Extract sections and articles from a collection page."""
    html = get_page(collection_url)
    if not html:
        return [], []
    
    soup = BeautifulSoup(html, 'html.parser')
    sections = []
    articles = []
    
    # Look for section headings
    section_elements = soup.select('[class*="section"], h2, h3')
    
    # Look for article links
    article_links = soup.select('a[href*="/articles/"]')
    
    seen_urls = set()
    for link in article_links:
        href = link.get('href', '')
        full_url = urljoin(BASE_URL, href)
        if full_url not in seen_urls and '/articles/' in href:
            seen_urls.add(full_url)
            title = link.get_text(strip=True)
            if title:
                articles.append({
                    'title': title,
                    'url': full_url
                })
    
    return sections, articles


def extract_article_content(url):
    """Extract the content of a single article."""
    html = get_page(url)
    if not html:
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Try to find the article content using common Intercom selectors
    content_selectors = [
        'article',
        '[class*="article-content"]',
        '[class*="article__content"]',
        '[class*="content-body"]',
        '.intercom-article-content',
        'main',
        '[role="main"]'
    ]
    
    article_content = None
    for selector in content_selectors:
        article_content = soup.select_one(selector)
        if article_content:
            break
    
    if not article_content:
        # Fallback: get body content
        article_content = soup.find('body')
    
    # Extract title
    title = None
    title_elem = soup.find('h1') or soup.find('title')
    if title_elem:
        title = title_elem.get_text(strip=True)
    
    # Get HTML content
    html_content = str(article_content) if article_content else ""
    
    # Convert to markdown
    markdown_content = h2t.handle(html_content)
    
    return {
        'title': title,
        'url': url,
        'html': html_content,
        'markdown': markdown_content
    }


def crawl_help_center():
    """Main function to crawl the entire help center."""
    print(f"Starting crawl of {BASE_URL}")
    print(f"Output directory: {OUTPUT_DIR}")
    
    # Create output directory
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    print(f"Created output directory")
    
    # Get main page
    main_html = get_page(BASE_URL)
    if not main_html:
        print("Failed to fetch main page!")
        return
    
    soup = BeautifulSoup(main_html, 'html.parser')
    
    # Save main page HTML for debugging
    with open(OUTPUT_DIR / "_main_page.html", 'w', encoding='utf-8') as f:
        f.write(main_html)
    
    # Extract all links first to understand structure
    all_links = []
    for link in soup.find_all('a', href=True):
        href = link.get('href')
        text = link.get_text(strip=True)
        if href and ('collections' in href or 'articles' in href):
            all_links.append({
                'href': urljoin(BASE_URL, href),
                'text': text
            })
    
    # Save links for reference
    with open(OUTPUT_DIR / "_all_links.json", 'w', encoding='utf-8') as f:
        json.dump(all_links, f, indent=2)
    
    print(f"Found {len(all_links)} content links")
    
    # Group by collections
    collections = {}
    standalone_articles = []
    
    for link_data in all_links:
        href = link_data['href']
        text = link_data['text']
        
        if '/collections/' in href:
            # This is a collection
            collection_id = re.search(r'/collections/(\d+)', href)
            if collection_id:
                cid = collection_id.group(1)
                if cid not in collections:
                    collections[cid] = {
                        'url': href,
                        'title': text,
                        'articles': []
                    }
        elif '/articles/' in href:
            standalone_articles.append(link_data)
    
    print(f"Found {len(collections)} collections")
    
    # Crawl each collection
    for cid, collection in collections.items():
        print(f"\nProcessing collection: {collection['title']}")
        time.sleep(DELAY_BETWEEN_REQUESTS)
        
        # Get collection page
        col_html = get_page(collection['url'])
        if col_html:
            col_soup = BeautifulSoup(col_html, 'html.parser')
            
            # Find articles in this collection
            for link in col_soup.find_all('a', href=True):
                href = link.get('href')
                if href and '/articles/' in href:
                    full_url = urljoin(BASE_URL, href)
                    title = link.get_text(strip=True)
                    if title and full_url not in [a['url'] for a in collection['articles']]:
                        collection['articles'].append({
                            'url': full_url,
                            'title': title
                        })
            
            print(f"  Found {len(collection['articles'])} articles")
    
    # Save structure
    with open(OUTPUT_DIR / "_structure.json", 'w', encoding='utf-8') as f:
        json.dump(collections, f, indent=2)
    
    # Now extract each article
    all_articles = []
    
    for cid, collection in collections.items():
        collection_name = sanitize_filename(collection['title']) or f"collection_{cid}"
        collection_dir = OUTPUT_DIR / collection_name
        collection_dir.mkdir(parents=True, exist_ok=True)
        
        print(f"\nExtracting articles from: {collection_name}")
        
        for article in collection['articles']:
            print(f"  - {article['title'][:50]}...")
            time.sleep(DELAY_BETWEEN_REQUESTS)
            
            content = extract_article_content(article['url'])
            if content:
                # Save markdown
                filename = sanitize_filename(article['title']) or 'untitled'
                md_path = collection_dir / f"{filename}.md"
                
                # Add frontmatter
                frontmatter = f"""---
title: "{content['title'] or article['title']}"
source: "{article['url']}"
collection: "{collection['title']}"
---

"""
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(frontmatter + content['markdown'])
                
                # Also save HTML
                html_dir = collection_dir / "_html"
                html_dir.mkdir(exist_ok=True)
                html_path = html_dir / f"{filename}.html"
                with open(html_path, 'w', encoding='utf-8') as f:
                    f.write(content['html'])
                
                all_articles.append({
                    'collection': collection['title'],
                    'title': content['title'],
                    'url': article['url'],
                    'saved_to': str(md_path)
                })
    
    # Handle standalone articles
    if standalone_articles:
        misc_dir = OUTPUT_DIR / "_miscellaneous"
        misc_dir.mkdir(exist_ok=True)
        
        print("\nExtracting standalone articles...")
        
        seen_urls = set()
        for article in standalone_articles:
            if article['href'] in seen_urls:
                continue
            seen_urls.add(article['href'])
            
            print(f"  - {article['text'][:50]}...")
            time.sleep(DELAY_BETWEEN_REQUESTS)
            
            content = extract_article_content(article['href'])
            if content:
                filename = sanitize_filename(article['text']) or 'untitled'
                md_path = misc_dir / f"{filename}.md"
                
                frontmatter = f"""---
title: "{content['title'] or article['text']}"
source: "{article['href']}"
---

"""
                with open(md_path, 'w', encoding='utf-8') as f:
                    f.write(frontmatter + content['markdown'])
    
    # Save summary
    summary = {
        'total_collections': len(collections),
        'total_articles': len(all_articles),
        'articles': all_articles
    }
    with open(OUTPUT_DIR / "_summary.json", 'w', encoding='utf-8') as f:
        json.dump(summary, f, indent=2)
    
    print(f"\n{'='*50}")
    print(f"Extraction complete!")
    print(f"Collections: {len(collections)}")
    print(f"Articles: {len(all_articles)}")
    print(f"Output directory: {OUTPUT_DIR}")


if __name__ == "__main__":
    crawl_help_center()

