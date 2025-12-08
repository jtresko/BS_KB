"""
Update Image Paths in Articles

This script:
1. Reads the image mapping file created by scrape_images.py
2. Updates all markdown files in docs/ to use local image paths
3. Also fixes any remaining Intercom URLs to local paths

Usage:
    python update_image_paths.py
    python update_image_paths.py --dry-run
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
MAPPING_FILE = ROOT_DIR / "intercom_export" / "_image_mapping.json"

def load_mapping():
    """Load the image mapping file."""
    if not MAPPING_FILE.exists():
        print(f"Warning: No mapping file found at {MAPPING_FILE}")
        return {}
    
    with open(MAPPING_FILE, 'r', encoding='utf-8') as f:
        mappings = json.load(f)
    
    # Create URL to local path dictionary
    url_map = {}
    for mapping in mappings:
        url_map[mapping['original_url']] = mapping['web_path']
    
    return url_map

def find_and_replace_images(content, url_map):
    """Find all image references and replace with local paths."""
    changes = []
    
    # Pattern for markdown images: ![alt](url)
    md_pattern = r'!\[([^\]]*)\]\(([^)]+)\)'
    
    def replace_md_image(match):
        alt = match.group(1)
        url = match.group(2)
        
        # Check if URL is in mapping
        if url in url_map:
            new_path = url_map[url]
            changes.append(f"  Replaced: {url[:50]}... -> {new_path}")
            return f'![{alt}]({new_path})'
        
        # Check for Intercom image URLs that should be local
        if 'intercom' in url.lower() or 'downloads.intercomcdn' in url.lower():
            changes.append(f"  WARNING: Unmapped Intercom image: {url[:80]}...")
        
        return match.group(0)
    
    new_content = re.sub(md_pattern, replace_md_image, content)
    
    # Pattern for HTML images: <img src="url">
    html_pattern = r'<img\s+[^>]*src=["\']([^"\']+)["\'][^>]*>'
    
    def replace_html_image(match):
        full_tag = match.group(0)
        url = match.group(1)
        
        if url in url_map:
            new_path = url_map[url]
            new_tag = full_tag.replace(url, new_path)
            changes.append(f"  Replaced (HTML): {url[:50]}... -> {new_path}")
            return new_tag
        
        if 'intercom' in url.lower() or 'downloads.intercomcdn' in url.lower():
            changes.append(f"  WARNING: Unmapped Intercom HTML image: {url[:80]}...")
        
        return match.group(0)
    
    new_content = re.sub(html_pattern, replace_html_image, new_content)
    
    return new_content, changes

def process_files(dry_run=False):
    """Process all markdown files in docs directory."""
    url_map = load_mapping()
    
    if not url_map:
        print("No URL mappings loaded. Running with empty mapping (will only report warnings).")
    else:
        print(f"Loaded {len(url_map)} image URL mappings.\n")
    
    total_files = 0
    updated_files = 0
    all_changes = []
    
    for md_file in DOCS_DIR.rglob("*.md"):
        total_files += 1
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, changes = find_and_replace_images(content, url_map)
        
        if changes:
            print(f"\n{md_file.relative_to(ROOT_DIR)}:")
            for change in changes:
                print(change)
            all_changes.extend(changes)
            
            if new_content != content:
                if not dry_run:
                    with open(md_file, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                updated_files += 1
    
    print(f"\n{'='*60}")
    print(f"Processed {total_files} files")
    print(f"Updated {updated_files} files")
    print(f"Total changes: {len(all_changes)}")
    if dry_run:
        print("\n[DRY RUN - No files were modified]")
    print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description='Update image paths in markdown files')
    parser.add_argument('--dry-run', action='store_true', help='Preview without modifying files')
    args = parser.parse_args()
    
    print("=" * 60)
    print("BigShort Image Path Updater")
    if args.dry_run:
        print("[DRY RUN MODE]")
    print("=" * 60)
    
    process_files(dry_run=args.dry_run)

if __name__ == "__main__":
    main()

