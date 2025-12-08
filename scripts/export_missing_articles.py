"""
Export Missing Articles from Intercom

Exports specific articles that are referenced but missing from the local KB.
"""

import requests
from bs4 import BeautifulSoup
import re
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DOCS_DIR = ROOT_DIR / "docs"

# Missing articles to export
MISSING_ARTICLES = [
    {
        "id": "11002762",
        "url": "https://help.bigshort.com/en/articles/11002762-the-bigfour-bigshort-indicators",
        "title": "The BigFour BigShort Indicators",
        "category": "indicators-and-features",
        "parent": "Indicators & Features",
    },
    {
        "id": "10697642",
        "url": "https://help.bigshort.com/en/articles/10697642-perfectly-reading-spy-with-three-flow-alignment",
        "title": "Perfectly Reading SPY with Three Flow Alignment",
        "category": "strategy",
        "subcategory": "trading-walkthroughs",
        "parent": "Trading Walkthroughs",
        "grand_parent": "Strategy",
    },
    {
        "id": "10630102",
        "url": "https://help.bigshort.com/en/articles/10630102-how-bigshort-trader-jp24-identified-hims-for-a-14-move-today",
        "title": "How BigShort Trader JP24 Identified HIMS for a 14% Move",
        "category": "strategy",
        "subcategory": "trading-walkthroughs",
        "parent": "Trading Walkthroughs",
        "grand_parent": "Strategy",
    },
]

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

def html_to_markdown(soup):
    """Simple HTML to Markdown converter."""
    # Process the content
    markdown = []
    
    for element in soup.descendants:
        if element.name == 'h1':
            markdown.append(f"\n# {element.get_text(strip=True)}\n")
        elif element.name == 'h2':
            markdown.append(f"\n## {element.get_text(strip=True)}\n")
        elif element.name == 'h3':
            markdown.append(f"\n### {element.get_text(strip=True)}\n")
        elif element.name == 'p':
            text = element.get_text(strip=True)
            if text:
                markdown.append(f"\n{text}\n")
        elif element.name == 'li':
            text = element.get_text(strip=True)
            if text:
                markdown.append(f"- {text}\n")
        elif element.name == 'img':
            src = element.get('src', '')
            alt = element.get('alt', '')
            if src:
                markdown.append(f"\n![{alt}]({src})\n")
        elif element.name == 'a' and element.parent.name not in ['h1', 'h2', 'h3', 'p', 'li']:
            href = element.get('href', '')
            text = element.get_text(strip=True)
            if href and text:
                markdown.append(f"[{text}]({href})")
        elif element.name == 'strong' or element.name == 'b':
            if element.parent.name == 'p':
                continue  # handled by parent
        elif element.name == 'em' or element.name == 'i':
            if element.parent.name == 'p':
                continue  # handled by parent
    
    return ''.join(markdown)

def extract_article_content(url):
    """Extract the content of a single article."""
    html = get_page(url)
    if not html:
        return None
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Try to find the article content
    content_selectors = [
        'article',
        '[class*="article-content"]',
        '[class*="article__content"]',
        '.intercom-article-content',
        'main',
    ]
    
    article_content = None
    for selector in content_selectors:
        article_content = soup.select_one(selector)
        if article_content:
            break
    
    if not article_content:
        article_content = soup.find('body')
    
    # Extract title
    title = None
    title_elem = soup.find('h1')
    if title_elem:
        title = title_elem.get_text(strip=True)
    
    # Convert to simple markdown
    markdown_content = html_to_markdown(article_content)
    
    # Clean up
    markdown_content = re.sub(r'\n{3,}', '\n\n', markdown_content)
    
    return {
        'title': title,
        'markdown': markdown_content.strip()
    }

def create_article_file(article_info, content):
    """Create the markdown file for an article."""
    category = article_info['category']
    subcategory = article_info.get('subcategory')
    
    if subcategory:
        folder = DOCS_DIR / category / subcategory
    else:
        folder = DOCS_DIR / category
    
    folder.mkdir(parents=True, exist_ok=True)
    
    # Create filename from title
    filename = article_info['title']
    filename = re.sub(r'[<>:"/\\|?*]', '', filename)
    filename = filename.strip()[:80] + ".md"
    
    filepath = folder / filename
    
    # Build front matter
    if subcategory:
        frontmatter = f"""---
title: "{article_info['title']}"
layout: default
parent: {article_info['parent']}
grand_parent: {article_info['grand_parent']}
nav_order: 99
---

"""
    else:
        frontmatter = f"""---
title: "{article_info['title']}"
layout: default
parent: {article_info['parent']}
nav_order: 99
---

"""
    
    # Write file
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(frontmatter + content['markdown'])
    
    return filepath

def main():
    print("=" * 60)
    print("Exporting Missing Articles from Intercom")
    print("=" * 60)
    
    exported = []
    
    for article in MISSING_ARTICLES:
        print(f"\nExporting: {article['title']}")
        print(f"  URL: {article['url']}")
        
        content = extract_article_content(article['url'])
        
        if content:
            filepath = create_article_file(article, content)
            print(f"  Created: {filepath.relative_to(ROOT_DIR)}")
            exported.append(article)
        else:
            print(f"  ERROR: Failed to fetch article")
        
        time.sleep(0.5)
    
    print(f"\n{'='*60}")
    print(f"Exported {len(exported)} articles")
    print("=" * 60)

if __name__ == "__main__":
    main()
