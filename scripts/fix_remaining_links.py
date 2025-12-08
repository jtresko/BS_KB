"""
Fix remaining broken links after article export.
"""

import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DOCS_DIR = ROOT_DIR / "docs"

# Link replacements
REPLACEMENTS = [
    # BigFour article - now exists locally
    (
        r'\[([^\]]*BigFour[^\]]*)\]\(https://(?:intercom\.help/bigshort|help\.bigshort\.com)/en/articles/11002762[^\)]*\)',
        r'[\1](/indicators-and-features/The BigFour BigShort Indicators/)'
    ),
    # 404 articles - remove the link but keep the text
    (
        r'\[([^\]]+)\]\(https://(?:intercom\.help/bigshort|help\.bigshort\.com)/en/articles/10697642[^\)]*\)',
        r'\1'  # Just the link text, no link
    ),
    (
        r'\[([^\]]+)\]\(https://(?:intercom\.help/bigshort|help\.bigshort\.com)/en/articles/10630102[^\)]*\)',
        r'\1'  # Just the link text, no link
    ),
]

def fix_links_in_file(filepath):
    """Fix links in a single file."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    original = content
    changes = []
    
    for pattern, replacement in REPLACEMENTS:
        matches = re.findall(pattern, content)
        if matches:
            content = re.sub(pattern, replacement, content)
            changes.append(f"  Fixed {len(matches)} link(s) matching pattern")
    
    if content != original:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        return True, changes
    
    return False, []

def main():
    print("=" * 60)
    print("Fixing Remaining Broken Links")
    print("=" * 60)
    
    updated = 0
    
    for md_file in DOCS_DIR.rglob("*.md"):
        changed, changes = fix_links_in_file(md_file)
        if changed:
            print(f"\n{md_file.relative_to(ROOT_DIR)}:")
            for change in changes:
                print(change)
            updated += 1
    
    print(f"\n{'='*60}")
    print(f"Updated {updated} files")
    print("=" * 60)

if __name__ == "__main__":
    main()

