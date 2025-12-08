"""
Fix Navigation Script for BigShort Knowledge Base
- Removes grand_parent from all articles
- Updates nav_order based on Intercom's _structure.json
- Updates parent names to match new flattened structure
- Fixes internal links
"""

import os
import json
import re
from pathlib import Path

# Paths
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DOCS_DIR = ROOT_DIR / "docs"
STRUCTURE_FILE = ROOT_DIR / "intercom_export" / "_structure.json"

# Mapping of Intercom collection IDs to folder names and parent titles
COLLECTION_MAP = {
    "11138833": {"folder": "getting-started", "parent": "Getting Started"},
    "11138938": {"folder": "strategy", "parent": "Strategy"},
    "11138946": {"folder": "indicators-and-features", "parent": "Indicators & Features"},
    "11139270": {"folder": "general", "parent": "General"},
    "11337275": {"folder": "discord-community", "parent": "Discord Community"},
    "11728897": {"folder": "bigresearch", "parent": "BigResearch"},
}

def load_structure():
    """Load the Intercom structure file."""
    with open(STRUCTURE_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def extract_article_slug(url):
    """Extract the article slug from an Intercom URL."""
    # URL format: https://help.bigshort.com/en/articles/10279633-getting-started-with-bigshort-new-users
    match = re.search(r'/articles/\d+-(.+)$', url)
    if match:
        return match.group(1)
    return None

def normalize_title(title):
    """Normalize a title for matching."""
    # Remove special characters and lowercase
    normalized = re.sub(r'[^\w\s]', '', title.lower())
    normalized = re.sub(r'\s+', ' ', normalized).strip()
    return normalized

def get_nav_order_map(structure):
    """Build a mapping of article titles to their nav_order based on Intercom order."""
    nav_orders = {}
    
    for collection_id, collection in structure.items():
        if collection_id not in COLLECTION_MAP:
            continue
        
        folder = COLLECTION_MAP[collection_id]["folder"]
        
        for idx, article in enumerate(collection["articles"], start=1):
            title = article["title"]
            normalized = normalize_title(title)
            nav_orders[(folder, normalized)] = idx
            # Also store by original title
            nav_orders[(folder, title.lower())] = idx
    
    return nav_orders

def update_frontmatter(content, parent_name, nav_order=None):
    """Update the YAML frontmatter of a markdown file."""
    # Split frontmatter and content
    if not content.startswith('---'):
        return content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content
    
    frontmatter = parts[1]
    body = parts[2]
    
    # Remove grand_parent line
    frontmatter = re.sub(r'\ngrand_parent:.*\n', '\n', frontmatter)
    
    # Update parent if present
    frontmatter = re.sub(r'parent:.*', f'parent: {parent_name}', frontmatter)
    
    # Update nav_order if provided
    if nav_order is not None:
        frontmatter = re.sub(r'nav_order:.*', f'nav_order: {nav_order}', frontmatter)
    
    return f'---{frontmatter}---{body}'

def fix_internal_links(content):
    """Fix internal links to use new paths."""
    # Fix links like [text](/docs/getting-started/...) to [text](/getting-started/...)
    content = re.sub(r'\]\(/docs/', '](/', content)
    return content

def process_articles():
    """Process all article files."""
    structure = load_structure()
    nav_orders = get_nav_order_map(structure)
    
    updated_files = []
    
    for collection_id, info in COLLECTION_MAP.items():
        folder = info["folder"]
        parent = info["parent"]
        folder_path = DOCS_DIR / folder
        
        if not folder_path.exists():
            print(f"Warning: Folder not found: {folder_path}")
            continue
        
        print(f"\nProcessing: {folder}")
        
        for md_file in folder_path.glob("*.md"):
            if md_file.name == "index.md":
                continue
            
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract title from frontmatter for nav_order lookup
            title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
            if title_match:
                title = title_match.group(1).strip()
                normalized_title = normalize_title(title)
                
                # Look up nav_order
                nav_order = nav_orders.get((folder, normalized_title))
                if nav_order is None:
                    nav_order = nav_orders.get((folder, title.lower()))
                
                if nav_order is None:
                    print(f"  Warning: No nav_order found for '{title}' in {folder}")
            else:
                nav_order = None
            
            # Update content
            new_content = update_frontmatter(content, parent, nav_order)
            new_content = fix_internal_links(new_content)
            
            if new_content != content:
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                updated_files.append(md_file.name)
                print(f"  Updated: {md_file.name}" + (f" (nav_order: {nav_order})" if nav_order else ""))
    
    return updated_files

def main():
    print("=" * 60)
    print("BigShort KB Navigation Fixer")
    print("=" * 60)
    
    if not STRUCTURE_FILE.exists():
        print(f"Error: Structure file not found: {STRUCTURE_FILE}")
        return
    
    updated = process_articles()
    
    print("\n" + "=" * 60)
    print(f"Complete! Updated {len(updated)} files.")
    print("=" * 60)

if __name__ == "__main__":
    main()

