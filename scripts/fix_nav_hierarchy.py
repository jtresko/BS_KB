"""
Fix navigation hierarchy for just-the-docs theme.
Adds grand_parent: Help Center to all articles.
"""

import re
from pathlib import Path

DOCS_DIR = Path(__file__).parent.parent / "docs"

# Collection folders and their parent titles
COLLECTIONS = {
    "getting-started": "Getting Started",
    "strategy": "Strategy",
    "indicators-and-features": "Indicators & Features",
    "general": "General",
    "discord-community": "Discord Community",
    "bigresearch": "BigResearch"
}


def fix_article_frontmatter(filepath, parent_title):
    """Add grand_parent to article front matter."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Check if it already has grand_parent
    if 'grand_parent:' in content:
        return False
    
    # Find the front matter and add grand_parent after parent
    pattern = r'(---\n.*?parent:\s*' + re.escape(parent_title) + r'.*?\n)(.*?---)'
    
    def add_grand_parent(match):
        before = match.group(1)
        after = match.group(2)
        return before + 'grand_parent: Help Center\n' + after
    
    new_content = re.sub(pattern, add_grand_parent, content, flags=re.DOTALL)
    
    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        return True
    return False


def main():
    print("Fixing navigation hierarchy...")
    
    fixed_count = 0
    
    for folder_name, parent_title in COLLECTIONS.items():
        folder_path = DOCS_DIR / folder_name
        if not folder_path.exists():
            print(f"  Skipping {folder_name} - not found")
            continue
        
        print(f"\nProcessing: {parent_title}")
        
        for md_file in folder_path.glob("*.md"):
            # Skip index files
            if md_file.name == "index.md":
                continue
            
            if fix_article_frontmatter(md_file, parent_title):
                print(f"  Fixed: {md_file.name}")
                fixed_count += 1
    
    print(f"\nDone! Fixed {fixed_count} files.")


if __name__ == "__main__":
    main()

