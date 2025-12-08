"""
Setup Proper Navigation Hierarchy for BigShort KB

This script creates sub-category index files and updates article front matter
to match the Intercom help center hierarchy with sub-sections.

Based on: https://help.bigshort.com/en/
"""

import os
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DOCS_DIR = ROOT_DIR / "docs"

# Define the complete hierarchy structure
# Format: category -> { subcategories: { name: [article_titles] }, top_level: [article_titles] }
HIERARCHY = {
    "strategy": {
        "parent_title": "Strategy",
        "top_level": [
            "What is a Honey Badger Day and How To Trade It",
            "Trading Ascending and Descending Triangles with BigShort",
            "Head and Shoulders Patterns with BigShort",
            "Support Breakout Trades with BigShort",
        ],
        "subcategories": {
            "User Strategies": {
                "nav_order": 5,
                "description": "Community-contributed trading strategies",
                "articles": [
                    "Using Short Exempt (SE) for Swing Trading",
                    "Sergius' Cumulative Volume Swing Trading Strategy",
                    "Z3: The 3 Bar Reversal Strategy by @Zedamonator",
                    "Kchun and Tae's 'Exhaustion Reversal' Signal",
                    "Joe from Cup of Joe Trading Explains his Premarket Strategy (video)",
                    "Honey Badger Success Stories",
                ]
            },
            "Trading Walkthroughs": {
                "nav_order": 12,
                "description": "Step-by-step trading examples",
                "articles": [
                    "Trading $SPY Profitably with BigShort",
                    "Trading a $HIMS Reversal",
                    "An Unexpected $SPY Reversal",
                    "Trading a volatile $PLTR with 12 hours warning",
                    "With vs. Without BigShort",
                    "Using Daily Timeframe to Swing Trade Through a Crash",
                    "Trading Dual Honey Badger Days - 3.21.25 and 3.24.25",
                ]
            },
            "Tae's Corner": {
                "nav_order": 20,
                "description": "Insights and wisdom from BigShort's founder",
                "articles": [
                    "Tae's Corner: SPY - Jan 15, 2025",
                    "Tae's Corner: SPY - Jan 14, 2025",
                    "Tae's Corner: SPY - Nov 20, 2024",
                    "Tae's Corner: SPY - Sept. 25, 2024",
                    "Tae's Corner: SPY - Sept. 20, 2024",
                    "Free Money Day - SPY 4.23.25",
                ]
            }
        }
    },
    "getting-started": {
        "parent_title": "Getting Started",
        "top_level": [
            "Getting Started with BigShort - New Users",
            "Will I Make Money",
            "Why You Should Rethink Setting Stop Losses and Hanging Limit Orders",
            "Why We Don't Trade Power Hour",
            "How Do I Find Good Trades",
            "Exiting Trades",
        ],
        "subcategories": {
            "Quickstart Guides": {
                "nav_order": 7,
                "description": "Fast-track guides for different trading styles",
                "articles": [
                    "Quickstart for Day Traders",
                    "Quickstart for Swing Traders",
                ]
            },
            "Platform Tabs": {
                "nav_order": 9,
                "description": "Understanding each tab in BigShort",
                "articles": [
                    "Understanding the Seasonality Tab",
                    "Dashboard & Top 10s",
                    "SF Segregated Tab",
                    "DarkFlow Tab",
                    "Understanding the UltraFlow Tab",
                    "Looking at the OptionFlow Tab",
                    "SmartFlow Tab",
                    "Training Tab",
                ]
            }
        }
    }
}

def normalize_title(title):
    """Normalize title for matching."""
    # Remove special chars, lowercase
    return re.sub(r'[^\w\s]', '', title.lower()).strip()

def find_article_file(folder_path, target_title):
    """Find the article file that matches the target title."""
    normalized_target = normalize_title(target_title)
    
    for md_file in folder_path.glob("*.md"):
        if md_file.name == "index.md":
            continue
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Extract title from front matter
        title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
        if title_match:
            file_title = title_match.group(1).strip()
            if normalize_title(file_title) == normalized_target:
                return md_file, content
            # Also check filename
            if normalize_title(md_file.stem) == normalized_target:
                return md_file, content
    
    # Fuzzy match - check if target is contained in file title
    for md_file in folder_path.glob("*.md"):
        if md_file.name == "index.md":
            continue
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        title_match = re.search(r'title:\s*["\']?([^"\'\n]+)["\']?', content)
        if title_match:
            file_title = title_match.group(1).strip()
            norm_file = normalize_title(file_title)
            norm_target = normalized_target
            
            # Check substring match
            if norm_target[:20] in norm_file or norm_file[:20] in norm_target:
                return md_file, content
    
    return None, None

def slugify(name):
    """Convert a name to a URL-friendly slug."""
    slug = name.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'\s+', '-', slug)
    return slug

def create_subcategory_index(category_folder, subcat_name, subcat_info, parent_title):
    """Create an index.md file for a subcategory."""
    slug = slugify(subcat_name)
    subcat_folder = category_folder / slug
    subcat_folder.mkdir(exist_ok=True)
    
    index_content = f"""---
title: {subcat_name}
layout: default
parent: {parent_title}
nav_order: {subcat_info['nav_order']}
has_children: true
---

# {subcat_name}

{subcat_info['description']}
"""
    
    index_path = subcat_folder / "index.md"
    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(index_content)
    
    print(f"  Created subcategory: {subcat_name}")
    return subcat_folder

def update_article_frontmatter(content, parent, grand_parent, nav_order):
    """Update an article's front matter with new parent hierarchy."""
    # Parse existing front matter
    if not content.startswith('---'):
        return content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content
    
    frontmatter = parts[1]
    body = parts[2]
    
    # Update or add parent
    if 'parent:' in frontmatter:
        frontmatter = re.sub(r'parent:.*', f'parent: {parent}', frontmatter)
    else:
        frontmatter = frontmatter.rstrip() + f'\nparent: {parent}\n'
    
    # Update or add grand_parent
    if 'grand_parent:' in frontmatter:
        frontmatter = re.sub(r'grand_parent:.*', f'grand_parent: {grand_parent}', frontmatter)
    else:
        frontmatter = frontmatter.rstrip() + f'\ngrand_parent: {grand_parent}\n'
    
    # Update nav_order
    if 'nav_order:' in frontmatter:
        frontmatter = re.sub(r'nav_order:.*', f'nav_order: {nav_order}', frontmatter)
    else:
        frontmatter = frontmatter.rstrip() + f'\nnav_order: {nav_order}\n'
    
    return f'---{frontmatter}---{body}'

def move_article_to_subcategory(src_path, dest_folder, content, parent, grand_parent, nav_order):
    """Move an article file to a subcategory folder and update its front matter."""
    new_content = update_article_frontmatter(content, parent, grand_parent, nav_order)
    
    dest_path = dest_folder / src_path.name
    
    # Write to new location
    with open(dest_path, 'w', encoding='utf-8') as f:
        f.write(new_content)
    
    # Remove from old location if different
    if src_path != dest_path and src_path.exists():
        src_path.unlink()
    
    return dest_path

def update_top_level_article(content, parent_title, nav_order):
    """Update a top-level article to have correct parent (no grand_parent)."""
    if not content.startswith('---'):
        return content
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        return content
    
    frontmatter = parts[1]
    body = parts[2]
    
    # Update parent
    if 'parent:' in frontmatter:
        frontmatter = re.sub(r'parent:.*', f'parent: {parent_title}', frontmatter)
    else:
        frontmatter = frontmatter.rstrip() + f'\nparent: {parent_title}\n'
    
    # Remove grand_parent if present
    frontmatter = re.sub(r'\ngrand_parent:.*', '', frontmatter)
    
    # Update nav_order
    if 'nav_order:' in frontmatter:
        frontmatter = re.sub(r'nav_order:.*', f'nav_order: {nav_order}', frontmatter)
    else:
        frontmatter = frontmatter.rstrip() + f'\nnav_order: {nav_order}\n'
    
    return f'---{frontmatter}---{body}'

def process_category(category_slug, category_info):
    """Process a category and organize its subcategories."""
    category_folder = DOCS_DIR / category_slug
    parent_title = category_info['parent_title']
    
    print(f"\n{'='*60}")
    print(f"Processing: {parent_title}")
    print(f"{'='*60}")
    
    if not category_folder.exists():
        print(f"  Warning: Folder not found: {category_folder}")
        return
    
    # Process top-level articles first
    print(f"\n  Top-level articles:")
    for idx, article_title in enumerate(category_info.get('top_level', []), start=1):
        file_path, content = find_article_file(category_folder, article_title)
        if file_path:
            new_content = update_top_level_article(content, parent_title, idx)
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"    Updated: {file_path.name} (nav_order: {idx})")
        else:
            print(f"    Warning: Not found - {article_title}")
    
    # Process subcategories
    for subcat_name, subcat_info in category_info.get('subcategories', {}).items():
        print(f"\n  Subcategory: {subcat_name}")
        
        # Create subcategory folder and index
        subcat_folder = create_subcategory_index(
            category_folder, subcat_name, subcat_info, parent_title
        )
        
        # Move/update articles in this subcategory
        for idx, article_title in enumerate(subcat_info['articles'], start=1):
            file_path, content = find_article_file(category_folder, article_title)
            if file_path:
                dest_path = move_article_to_subcategory(
                    file_path, subcat_folder, content,
                    parent=subcat_name,
                    grand_parent=parent_title,
                    nav_order=idx
                )
                print(f"    Moved: {file_path.name} -> {dest_path.relative_to(DOCS_DIR)}")
            else:
                print(f"    Warning: Not found - {article_title}")

def main():
    print("=" * 60)
    print("BigShort KB Hierarchy Setup")
    print("=" * 60)
    
    for category_slug, category_info in HIERARCHY.items():
        process_category(category_slug, category_info)
    
    print(f"\n{'='*60}")
    print("Complete!")
    print("=" * 60)

if __name__ == "__main__":
    main()

