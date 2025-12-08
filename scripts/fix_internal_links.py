"""
Fix internal links in Jekyll docs - convert Intercom URLs to local Jekyll paths
"""

import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"

# Build dynamic link mappings from actual file structure
def build_link_mappings():
    """Scan docs directory and build mappings from article IDs to local paths."""
    mappings = {}
    
    # Map common article IDs to their Jekyll paths
    # Format: "article-id-slug" -> "jekyll-path"
    known_mappings = {
        # Getting Started
        "10354276": ("getting-started", "Understanding the Seasonality Tab"),
        "10362301": ("getting-started", "SF Segregated Tab"),
        "10279633": ("getting-started", "Getting Started with BigShort - New Users"),
        
        # Indicators & Features
        "10361455": ("indicators-and-features", "Understanding SmartFlow and MomoFlow Indicators"),
        "10280483": ("indicators-and-features", "Understanding Dark Pools and DarkFlow in BigShort"),
        "10354751": ("indicators-and-features", "Net Option Flow A Complete Guide"),
        "10279839": ("indicators-and-features", "Similarity Search (SimSearch)"),
        "10354308": ("indicators-and-features", "What is Short Exempt (SE)"),
        
        # Strategy
        "10284188": ("strategy", "What is a Honey Badger Day and How To Trade It"),
    }
    
    for article_id, (folder, title) in known_mappings.items():
        # Create the Jekyll-compatible URL
        # just-the-docs uses the file path structure
        mappings[article_id] = f"/docs/{folder}/{title}/"
    
    return mappings


LINK_MAPPINGS = build_link_mappings()


def fix_links_in_file(filepath):
    """Fix Intercom links in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    
    # Find and replace Intercom links
    def replace_link(match):
        full_url = match.group(0)
        article_path = match.group(1)
        
        # Extract article ID (first part before the dash-separated title)
        article_id = article_path.split('-')[0]
        
        # Try to find a mapping
        if article_id in LINK_MAPPINGS:
            return LINK_MAPPINGS[article_id]
        
        # Keep original if no mapping found
        return full_url
    
    # Match both intercom.help and help.bigshort.com URLs
    pattern = r'https?://(?:intercom\.help/bigshort|help\.bigshort\.com)/en/articles/([^\s\)\]]+)'
    content = re.sub(pattern, replace_link, content)
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True
    return False


def find_all_intercom_links(content):
    """Find all Intercom help links in content."""
    pattern = r'https?://(?:intercom\.help/bigshort|help\.bigshort\.com)/en/articles/([^\s\)\]]+)'
    return re.findall(pattern, content)


def main():
    print("Fixing internal links in Jekyll docs...")
    print(f"Known mappings: {len(LINK_MAPPINGS)}")
    
    # First, scan for all unique Intercom links
    all_links = set()
    for md_file in DOCS_DIR.rglob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        links = find_all_intercom_links(content)
        all_links.update(links)
    
    print(f"\nFound {len(all_links)} unique Intercom links:")
    for link in sorted(all_links):
        article_id = link.split('-')[0]
        status = "✓" if article_id in LINK_MAPPINGS else "✗"
        print(f"  {status} {link}")
    
    # Now fix the links
    print("\nFixing links...")
    fixed_count = 0
    for md_file in DOCS_DIR.rglob("*.md"):
        if fix_links_in_file(md_file):
            print(f"  Fixed: {md_file.name}")
            fixed_count += 1
    
    print(f"\nDone! Fixed {fixed_count} files.")
    
    # Report remaining Intercom links
    print("\nChecking for remaining Intercom links...")
    remaining = set()
    for md_file in DOCS_DIR.rglob("*.md"):
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        links = find_all_intercom_links(content)
        remaining.update(links)
    
    if remaining:
        print(f"  {len(remaining)} links still point to Intercom (no mapping found)")
    else:
        print("  All Intercom links have been replaced!")


if __name__ == "__main__":
    main()
