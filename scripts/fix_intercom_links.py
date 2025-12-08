"""
Fix Intercom Links in Articles

This script converts Intercom help center links to local documentation paths.

Usage:
    python fix_intercom_links.py
    python fix_intercom_links.py --dry-run
"""

import os
import re
import json
from pathlib import Path
import argparse

# Configuration
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DOCS_DIR = ROOT_DIR / "docs"
STRUCTURE_FILE = ROOT_DIR / "intercom_export" / "_structure.json"

# Mapping of Intercom article IDs to local paths
# Format: article_id -> local_path (without leading /)
ARTICLE_MAP = {}

def load_article_mapping():
    """Build mapping from Intercom URLs to local paths."""
    global ARTICLE_MAP
    
    if not STRUCTURE_FILE.exists():
        print(f"Warning: Structure file not found: {STRUCTURE_FILE}")
        return
    
    with open(STRUCTURE_FILE, 'r', encoding='utf-8') as f:
        structure = json.load(f)
    
    # Category folder mapping
    category_map = {
        "11138833": "getting-started",
        "11138938": "strategy",
        "11138946": "indicators-and-features",
        "11139270": "general",
        "11337275": "discord-community",
        "11728897": "bigresearch",
    }
    
    for collection_id, collection in structure.items():
        folder = category_map.get(collection_id)
        if not folder:
            continue
        
        for article in collection.get('articles', []):
            url = article['url']
            title = article['title']
            
            # Extract article ID from URL
            match = re.search(r'/articles/(\d+)', url)
            if match:
                article_id = match.group(1)
                
                # Find the corresponding local file
                folder_path = DOCS_DIR / folder
                if folder_path.exists():
                    for md_file in folder_path.glob("*.md"):
                        if md_file.name == "index.md":
                            continue
                        # Read front matter to match title
                        with open(md_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                        
                        # Match by title in frontmatter or filename similarity
                        title_in_file = re.search(r'title:\s*["\']?([^"\'\n]+)', content)
                        if title_in_file:
                            file_title = title_in_file.group(1).strip()
                            # Normalize for comparison
                            if normalize_text(file_title) in normalize_text(title) or \
                               normalize_text(title) in normalize_text(file_title):
                                # Create local path
                                slug = md_file.stem
                                local_path = f"/{folder}/{slug}/"
                                ARTICLE_MAP[article_id] = local_path
                                break

def normalize_text(text):
    """Normalize text for comparison."""
    return re.sub(r'[^\w]', '', text.lower())

def convert_intercom_link(url):
    """Convert an Intercom URL to a local path."""
    # Extract article ID
    match = re.search(r'/articles/(\d+)', url)
    if match:
        article_id = match.group(1)
        if article_id in ARTICLE_MAP:
            return ARTICLE_MAP[article_id]
    
    return None

def process_file(file_path, dry_run=False):
    """Process a single markdown file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original_content = content
    changes = []
    
    # Find all Intercom links
    # Pattern: [text](https://intercom.help/bigshort/en/articles/...)
    pattern = r'\[([^\]]+)\]\((https://intercom\.help/bigshort/en/articles/[^\)]+)\)'
    
    def replace_link(match):
        text = match.group(1)
        url = match.group(2)
        
        local_path = convert_intercom_link(url)
        if local_path:
            changes.append(f"  {url[:60]}... -> {local_path}")
            return f'[{text}]({local_path})'
        else:
            changes.append(f"  WARNING: No mapping for {url[:60]}...")
            return match.group(0)
    
    content = re.sub(pattern, replace_link, content)
    
    if content != original_content:
        if not dry_run:
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(content)
        return changes
    
    return []

def main():
    parser = argparse.ArgumentParser(description='Fix Intercom links in markdown files')
    parser.add_argument('--dry-run', action='store_true', help='Preview without modifying files')
    args = parser.parse_args()
    
    print("=" * 60)
    print("BigShort Intercom Link Fixer")
    if args.dry_run:
        print("[DRY RUN MODE]")
    print("=" * 60)
    
    # Load article mapping
    print("\nBuilding article mapping...")
    load_article_mapping()
    print(f"Mapped {len(ARTICLE_MAP)} articles.\n")
    
    # Process all markdown files
    total_files = 0
    updated_files = 0
    all_changes = []
    
    for md_file in DOCS_DIR.rglob("*.md"):
        total_files += 1
        changes = process_file(md_file, dry_run=args.dry_run)
        
        if changes:
            print(f"\n{md_file.relative_to(ROOT_DIR)}:")
            for change in changes:
                print(change)
            all_changes.extend(changes)
            updated_files += 1
    
    print(f"\n{'='*60}")
    print(f"Processed {total_files} files")
    print(f"Updated {updated_files} files")
    print(f"Total link changes: {len(all_changes)}")
    if args.dry_run:
        print("\n[DRY RUN - No files were modified]")
    print("=" * 60)

if __name__ == "__main__":
    main()

