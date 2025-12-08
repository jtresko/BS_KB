"""
Prepare Intercom export for Jekyll/GitHub Pages
- Downloads all images from Intercom CDN
- Creates Jekyll-compatible folder structure
- Updates markdown files with local image paths
- Adds proper Jekyll front matter for just-the-docs theme
"""

import os
import re
import json
import time
import hashlib
import requests
from pathlib import Path
from urllib.parse import urlparse, unquote

# Paths
SCRIPT_DIR = Path(__file__).parent
REPO_ROOT = SCRIPT_DIR.parent
EXPORT_DIR = REPO_ROOT / "intercom_export"
DOCS_DIR = REPO_ROOT / "docs"
ASSETS_DIR = REPO_ROOT / "assets" / "images" / "help"

# Request settings
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
}
DELAY_BETWEEN_REQUESTS = 0.3

# Collection order and metadata
COLLECTIONS = {
    "01 - Getting Started": {
        "title": "Getting Started",
        "nav_order": 1,
        "description": "Everything you need to get going with BigShort"
    },
    "02 - Strategy": {
        "title": "Strategy",
        "nav_order": 2,
        "description": "How to use BigShort for profit"
    },
    "03 - Indicators & Features": {
        "title": "Indicators & Features",
        "nav_order": 3,
        "description": "Deep dives into BigShort indicators"
    },
    "04 - General": {
        "title": "General",
        "nav_order": 4,
        "description": "Everything else"
    },
    "05 - Discord Community": {
        "title": "Discord Community",
        "nav_order": 5,
        "description": "All things Discord"
    },
    "06 - BigResearch": {
        "title": "BigResearch",
        "nav_order": 6,
        "description": "Books and research to make you a better trader"
    }
}


def sanitize_filename(name):
    """Convert a string to a safe filename."""
    name = re.sub(r'[<>:"/\\|?*]', '', name)
    name = name.strip()
    if len(name) > 80:
        name = name[:80]
    return name


def get_image_filename(url, index=0):
    """Generate a unique filename for an image."""
    # Try to get original filename from URL
    parsed = urlparse(url)
    path = unquote(parsed.path)
    
    # Extract filename from path
    if '/' in path:
        original_name = path.split('/')[-1]
    else:
        original_name = path
    
    # Clean up the name
    original_name = re.sub(r'[<>:"/\\|?*]', '', original_name)
    
    # If no good name, create one from hash
    if not original_name or len(original_name) < 3:
        url_hash = hashlib.md5(url.encode()).hexdigest()[:8]
        original_name = f"image_{url_hash}.png"
    
    # Ensure it has an extension
    if '.' not in original_name:
        original_name += ".png"
    
    return original_name


def download_image(url, save_path):
    """Download an image from URL to local path."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=30, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        return True
    except Exception as e:
        print(f"    Error downloading {url[:50]}...: {e}")
        return False


def extract_image_urls(content):
    """Extract all image URLs from markdown content."""
    # Match markdown image syntax: ![alt](url) and also just URLs in links
    patterns = [
        r'!\[([^\]]*)\]\(([^)]+)\)',  # ![alt](url)
        r'\[!\[([^\]]*)\]\(([^)]+)\)\]\(([^)]+)\)',  # [![alt](url)](link)
    ]
    
    urls = []
    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            if isinstance(match, tuple):
                for item in match:
                    if item.startswith('http') and 'intercom' in item.lower():
                        urls.append(item)
            elif match.startswith('http') and 'intercom' in match.lower():
                urls.append(match)
    
    return list(set(urls))


def create_jekyll_frontmatter(title, parent, nav_order, description=None):
    """Create Jekyll front matter for just-the-docs theme."""
    fm = f"""---
title: "{title}"
layout: default
parent: {parent}
nav_order: {nav_order}
"""
    if description:
        fm += f'description: "{description}"\n'
    fm += "---\n\n"
    return fm


def create_collection_index(collection_name, metadata):
    """Create an index page for a collection."""
    return f"""---
title: {metadata['title']}
layout: default
nav_order: {metadata['nav_order']}
has_children: true
---

# {metadata['title']}

{metadata['description']}

Browse the articles below to learn more.
"""


def process_markdown_content(content, image_map, collection_folder):
    """Process markdown content - update image URLs and clean up."""
    
    # Remove the old YAML front matter if present
    if content.startswith('---'):
        end_fm = content.find('---', 3)
        if end_fm != -1:
            content = content[end_fm + 3:].strip()
    
    # Replace image URLs with local paths
    for old_url, new_path in image_map.items():
        # Handle both standalone images and linked images
        content = content.replace(old_url, new_path)
    
    # Clean up some common issues
    # Remove empty links that just wrap images
    content = re.sub(r'\[(\!\[[^\]]*\]\([^)]+\))\]\([^)]+\)', r'\1', content)
    
    # Fix double line breaks
    content = re.sub(r'\n{4,}', '\n\n\n', content)
    
    # Clean up weird characters
    content = content.replace('​', '')  # Zero-width space
    
    return content


def process_collection(collection_folder, collection_meta):
    """Process all articles in a collection."""
    source_dir = EXPORT_DIR / collection_folder
    target_dir = DOCS_DIR / collection_meta['title'].lower().replace(' ', '-').replace('&', 'and')
    images_dir = ASSETS_DIR / collection_meta['title'].lower().replace(' ', '-').replace('&', 'and')
    
    if not source_dir.exists():
        print(f"  Skipping {collection_folder} - not found")
        return
    
    # Create target directories
    target_dir.mkdir(parents=True, exist_ok=True)
    images_dir.mkdir(parents=True, exist_ok=True)
    
    print(f"\nProcessing: {collection_meta['title']}")
    
    # Create collection index page
    index_content = create_collection_index(collection_folder, collection_meta)
    index_path = target_dir / "index.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    print(f"  Created index: {index_path.name}")
    
    # Process each markdown file
    md_files = sorted(source_dir.glob("*.md"))
    
    for nav_order, md_file in enumerate(md_files, start=1):
        print(f"  Processing: {md_file.name[:50]}...")
        
        # Read content
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title from old front matter or filename
        title_match = re.search(r'^title:\s*["\']?([^"\'\n]+)["\']?', content, re.MULTILINE)
        if title_match:
            title = title_match.group(1).strip()
        else:
            title = md_file.stem
        
        # Find all image URLs
        image_urls = extract_image_urls(content)
        image_map = {}
        
        # Download images
        for idx, url in enumerate(image_urls):
            img_filename = get_image_filename(url, idx)
            # Add article prefix to avoid conflicts
            article_prefix = sanitize_filename(md_file.stem)[:20]
            img_filename = f"{article_prefix}_{img_filename}"
            img_path = images_dir / img_filename
            
            # Jekyll path (relative to site root)
            jekyll_path = f"/assets/images/help/{collection_meta['title'].lower().replace(' ', '-').replace('&', 'and')}/{img_filename}"
            
            if not img_path.exists():
                time.sleep(DELAY_BETWEEN_REQUESTS)
                if download_image(url, img_path):
                    print(f"    Downloaded: {img_filename}")
                else:
                    print(f"    Failed: {img_filename}")
                    continue
            
            image_map[url] = jekyll_path
        
        # Process content
        new_content = process_markdown_content(content, image_map, collection_folder)
        
        # Add Jekyll front matter
        front_matter = create_jekyll_frontmatter(
            title=title,
            parent=collection_meta['title'],
            nav_order=nav_order
        )
        
        final_content = front_matter + new_content
        
        # Save to target directory
        target_file = target_dir / md_file.name
        with open(target_file, 'w', encoding='utf-8') as f:
            f.write(final_content)


def create_help_index():
    """Create main help center index page."""
    content = """---
title: Help Center
layout: default
nav_order: 2
has_children: true
---

# BigShort Help Center

Welcome to the BigShort Help Center! Here you'll find guides, tutorials, and documentation to help you get the most out of BigShort.

## Quick Links

- **[Getting Started](/docs/getting-started/)** - New to BigShort? Start here!
- **[Strategy](/docs/strategy/)** - Learn profitable trading strategies
- **[Indicators & Features](/docs/indicators-and-features/)** - Deep dives into our tools
- **[General](/docs/general/)** - Account management and more
- **[Discord Community](/docs/discord-community/)** - Connect with other traders
- **[BigResearch](/docs/bigresearch/)** - Books and research resources

---

Browse the sections below to find what you're looking for, or use the search bar above.
"""
    
    docs_dir = DOCS_DIR
    docs_dir.mkdir(parents=True, exist_ok=True)
    
    index_path = docs_dir / "index.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f"Created main help index: {index_path}")


def main():
    print("=" * 60)
    print("Preparing Intercom Export for Jekyll/GitHub Pages")
    print("=" * 60)
    
    # Create directories
    DOCS_DIR.mkdir(parents=True, exist_ok=True)
    ASSETS_DIR.mkdir(parents=True, exist_ok=True)
    
    # Create main help index
    create_help_index()
    
    # Process each collection
    for folder_name, metadata in COLLECTIONS.items():
        process_collection(folder_name, metadata)
    
    print("\n" + "=" * 60)
    print("Done!")
    print(f"Documentation created in: {DOCS_DIR}")
    print(f"Images downloaded to: {ASSETS_DIR}")
    print("=" * 60)


if __name__ == "__main__":
    main()

