"""
Intercom Image Scraper for BigShort Knowledge Base

This script:
1. Crawls all articles from the Intercom help center
2. Downloads all images referenced in articles
3. Creates a mapping file to update article markdown files
4. Organizes images by category/article

Usage:
    python scrape_images.py
    python scrape_images.py --dry-run  # Preview without downloading
"""

import requests
from bs4 import BeautifulSoup
import os
import re
import json
import time
import hashlib
from urllib.parse import urljoin, urlparse, unquote
from pathlib import Path
import argparse

# Configuration
BASE_URL = "https://help.bigshort.com/en/"
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
OUTPUT_DIR = ROOT_DIR / "assets" / "images" / "help"
MAPPING_FILE = ROOT_DIR / "intercom_export" / "_image_mapping.json"
STRUCTURE_FILE = ROOT_DIR / "intercom_export" / "_structure.json"
DELAY_BETWEEN_REQUESTS = 0.3

# Category folder mapping
CATEGORY_MAP = {
    "11138833": "getting-started",
    "11138938": "strategy",
    "11138946": "indicators-and-features",
    "11139270": "general",
    "11337275": "discord-community",
    "11728897": "bigresearch",
}

def sanitize_filename(name, max_length=50):
    """Convert a string to a safe filename."""
    # Remove or replace invalid characters
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = re.sub(r'\s+', ' ', name).strip()
    # Limit length
    if len(name) > max_length:
        name = name[:max_length]
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
            return response
        except Exception as e:
            print(f"  Retry {i+1}/{retries} for {url}: {e}")
            time.sleep(2)
    return None

def extract_images_from_html(html_content, base_url):
    """Extract all image URLs from HTML content."""
    soup = BeautifulSoup(html_content, 'html.parser')
    images = []
    
    # Find all img tags
    for img in soup.find_all('img'):
        src = img.get('src') or img.get('data-src')
        if src:
            # Convert relative URLs to absolute
            full_url = urljoin(base_url, src)
            # Filter out icons, logos, etc.
            if any(skip in full_url.lower() for skip in ['icon', 'logo', 'emoji', 'avatar', 'favicon']):
                continue
            images.append({
                'url': full_url,
                'alt': img.get('alt', ''),
            })
    
    # Also check for background images in style attributes
    for elem in soup.find_all(style=True):
        style = elem.get('style', '')
        urls = re.findall(r'url\(["\']?([^"\')]+)["\']?\)', style)
        for url in urls:
            if url.startswith('data:'):
                continue
            full_url = urljoin(base_url, url)
            images.append({
                'url': full_url,
                'alt': '',
            })
    
    return images

def download_image(url, save_path, dry_run=False):
    """Download an image and save it to the specified path."""
    if dry_run:
        print(f"    [DRY RUN] Would download: {url}")
        return True
    
    try:
        response = get_page(url)
        if response and response.status_code == 200:
            save_path.parent.mkdir(parents=True, exist_ok=True)
            with open(save_path, 'wb') as f:
                f.write(response.content)
            return True
    except Exception as e:
        print(f"    Error downloading {url}: {e}")
    return False

def get_image_extension(url, content_type=None):
    """Determine the file extension for an image."""
    # Try to get from URL
    parsed = urlparse(url)
    path = unquote(parsed.path)
    
    # Common extensions
    for ext in ['.png', '.jpg', '.jpeg', '.gif', '.webp', '.svg']:
        if path.lower().endswith(ext):
            return ext
    
    # Try content type
    if content_type:
        type_map = {
            'image/png': '.png',
            'image/jpeg': '.jpg',
            'image/gif': '.gif',
            'image/webp': '.webp',
            'image/svg+xml': '.svg',
        }
        return type_map.get(content_type, '.png')
    
    return '.png'

def generate_image_filename(article_title, image_url, index):
    """Generate a clean filename for an image."""
    # Get extension from URL
    ext = get_image_extension(image_url)
    
    # Create base name from article title
    base_name = sanitize_filename(article_title, max_length=30)
    
    # Try to extract meaningful name from URL
    parsed = urlparse(image_url)
    url_name = Path(unquote(parsed.path)).stem
    url_name = sanitize_filename(url_name, max_length=30)
    
    if url_name and len(url_name) > 5:
        filename = f"{base_name}_{url_name}{ext}"
    else:
        filename = f"{base_name}_{index}{ext}"
    
    return filename

def scrape_article(url, article_title, category_folder, dry_run=False):
    """Scrape images from a single article."""
    print(f"  Processing: {article_title[:50]}...")
    
    response = get_page(url)
    if not response:
        return []
    
    images = extract_images_from_html(response.text, url)
    image_mappings = []
    
    for idx, img_data in enumerate(images, start=1):
        img_url = img_data['url']
        
        # Generate filename
        filename = generate_image_filename(article_title, img_url, idx)
        
        # Create local path
        local_dir = OUTPUT_DIR / category_folder
        local_path = local_dir / filename
        
        # Check if already downloaded
        if local_path.exists() and not dry_run:
            print(f"    Skipping (exists): {filename}")
        else:
            success = download_image(img_url, local_path, dry_run)
            if success:
                print(f"    Downloaded: {filename}")
        
        # Create mapping
        web_path = f"/assets/images/help/{category_folder}/{filename}"
        image_mappings.append({
            'original_url': img_url,
            'local_path': str(local_path),
            'web_path': web_path,
            'article_title': article_title,
            'article_url': url,
        })
        
        time.sleep(DELAY_BETWEEN_REQUESTS)
    
    return image_mappings

def load_structure():
    """Load the Intercom structure file."""
    if not STRUCTURE_FILE.exists():
        print(f"Error: Structure file not found: {STRUCTURE_FILE}")
        return None
    
    with open(STRUCTURE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def main():
    parser = argparse.ArgumentParser(description='Scrape images from Intercom help center')
    parser.add_argument('--dry-run', action='store_true', help='Preview without downloading')
    args = parser.parse_args()
    
    print("=" * 60)
    print("BigShort Intercom Image Scraper")
    if args.dry_run:
        print("[DRY RUN MODE - No files will be downloaded]")
    print("=" * 60)
    
    structure = load_structure()
    if not structure:
        return
    
    all_mappings = []
    
    for collection_id, collection in structure.items():
        category_folder = CATEGORY_MAP.get(collection_id)
        if not category_folder:
            print(f"\nSkipping unknown collection: {collection_id}")
            continue
        
        # Clean up collection title
        title_match = re.match(r'^([^A-Z]+[a-z]+)', collection.get('title', ''))
        collection_name = title_match.group(1) if title_match else collection_id
        
        print(f"\n{'='*60}")
        print(f"Collection: {collection_name} ({category_folder})")
        print(f"{'='*60}")
        
        for article in collection.get('articles', []):
            article_url = article['url']
            article_title = article['title']
            
            mappings = scrape_article(
                article_url, 
                article_title, 
                category_folder, 
                dry_run=args.dry_run
            )
            all_mappings.extend(mappings)
            
            time.sleep(DELAY_BETWEEN_REQUESTS)
    
    # Save mapping file
    if not args.dry_run:
        MAPPING_FILE.parent.mkdir(parents=True, exist_ok=True)
        with open(MAPPING_FILE, 'w', encoding='utf-8') as f:
            json.dump(all_mappings, f, indent=2)
        print(f"\nMapping saved to: {MAPPING_FILE}")
    
    print(f"\n{'='*60}")
    print(f"Complete! Processed {len(all_mappings)} images.")
    print("=" * 60)
    
    if args.dry_run:
        print("\nRun without --dry-run to actually download images.")

if __name__ == "__main__":
    main()

