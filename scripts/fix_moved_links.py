"""
Fix Internal Links After Hierarchy Reorganization

Updates internal links to point to new subcategory paths.
"""

import os
import re
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
DOCS_DIR = ROOT_DIR / "docs"

# Mapping of old paths to new paths (article slugs that moved)
PATH_UPDATES = {
    # Strategy subcategories
    "/strategy/Using Short Exempt (SE) for Swing Trading/": "/strategy/user-strategies/Using Short Exempt (SE) for Swing Trading/",
    "/strategy/Sergius' Cumulative Volume Swing Trading Strategy/": "/strategy/user-strategies/Sergius' Cumulative Volume Swing Trading Strategy/",
    "/strategy/Z3 the 3 Bar Reversal strategy by @Zedamonator/": "/strategy/user-strategies/Z3 the 3 Bar Reversal strategy by @Zedamonator/",
    "/strategy/Kchun and Tae's 'Exhaustion Reversal' Signal/": "/strategy/user-strategies/Kchun and Tae's 'Exhaustion Reversal' Signal/",
    "/strategy/Joe from Cup of Joe Trading Explains his Premarket Strategy (video)/": "/strategy/user-strategies/Joe from Cup of Joe Trading Explains his Premarket Strategy (video)/",
    "/strategy/Honey Badger Success Stories/": "/strategy/user-strategies/Honey Badger Success Stories/",
    
    "/strategy/Trading $SPY Profitably with BigShort/": "/strategy/trading-walkthroughs/Trading $SPY Profitably with BigShort/",
    "/strategy/Trading a $HIMS Reversal/": "/strategy/trading-walkthroughs/Trading a $HIMS Reversal/",
    "/strategy/An Unexpected $SPY Reversal/": "/strategy/trading-walkthroughs/An Unexpected $SPY Reversal/",
    "/strategy/Trading a volatile $PLTR with 12 hours warning/": "/strategy/trading-walkthroughs/Trading a volatile $PLTR with 12 hours warning/",
    "/strategy/With vs. Without BigShort/": "/strategy/trading-walkthroughs/With vs. Without BigShort/",
    "/strategy/Using Daily Timeframe to Swing Trade Through a Crash/": "/strategy/trading-walkthroughs/Using Daily Timeframe to Swing Trade Through a Crash/",
    "/strategy/Trading Dual Honey Badger Days - 3.21.25 and 3.24.25/": "/strategy/trading-walkthroughs/Trading Dual Honey Badger Days - 3.21.25 and 3.24.25/",
    
    "/strategy/Tae's Corner SPY - Jan 15, 2025/": "/strategy/taes-corner/Tae's Corner SPY - Jan 15, 2025/",
    "/strategy/Tae's Corner SPY - Jan 14, 2025/": "/strategy/taes-corner/Tae's Corner SPY - Jan 14, 2025/",
    "/strategy/Tae's Corner SPY - Nov 20, 2024/": "/strategy/taes-corner/Tae's Corner SPY - Nov 20, 2024/",
    "/strategy/Tae's Corner SPY - Sept. 25, 2024/": "/strategy/taes-corner/Tae's Corner SPY - Sept. 25, 2024/",
    "/strategy/Tae's Corner SPY - Sept. 20, 2024/": "/strategy/taes-corner/Tae's Corner SPY - Sept. 20, 2024/",
    "/strategy/Free Money Day - SPY 4.23.25/": "/strategy/taes-corner/Free Money Day - SPY 4.23.25/",
    
    # Getting Started subcategories
    "/getting-started/Quickstart for Day Traders/": "/getting-started/quickstart-guides/Quickstart for Day Traders/",
    "/getting-started/Quickstart for Swing Traders/": "/getting-started/quickstart-guides/Quickstart for Swing Traders/",
    
    "/getting-started/Understanding the Seasonality Tab/": "/getting-started/platform-tabs/Understanding the Seasonality Tab/",
    "/getting-started/Dashboard & Top 10s/": "/getting-started/platform-tabs/Dashboard & Top 10s/",
    "/getting-started/SF Segregated Tab/": "/getting-started/platform-tabs/SF Segregated Tab/",
    "/getting-started/DarkFlow Tab/": "/getting-started/platform-tabs/DarkFlow Tab/",
    "/getting-started/Understanding the UltraFlow Tab/": "/getting-started/platform-tabs/Understanding the UltraFlow Tab/",
    "/getting-started/Looking at the OptionFlow Tab/": "/getting-started/platform-tabs/Looking at the OptionFlow Tab/",
    "/getting-started/SmartFlow Tab/": "/getting-started/platform-tabs/SmartFlow Tab/",
    "/getting-started/Training Tab/": "/getting-started/platform-tabs/Training Tab/",
}

def fix_links_in_content(content):
    """Replace old paths with new paths."""
    changes = []
    
    for old_path, new_path in PATH_UPDATES.items():
        if old_path in content:
            content = content.replace(old_path, new_path)
            changes.append(f"  {old_path[:40]}... -> {new_path[:40]}...")
    
    return content, changes

def process_files():
    """Process all markdown files."""
    total_files = 0
    updated_files = 0
    all_changes = []
    
    for md_file in DOCS_DIR.rglob("*.md"):
        total_files += 1
        
        with open(md_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        new_content, changes = fix_links_in_content(content)
        
        if changes:
            print(f"\n{md_file.relative_to(ROOT_DIR)}:")
            for change in changes:
                print(change)
            all_changes.extend(changes)
            
            with open(md_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_files += 1
    
    return total_files, updated_files, len(all_changes)

def main():
    print("=" * 60)
    print("BigShort Internal Link Fixer (Post-Hierarchy)")
    print("=" * 60)
    
    total, updated, changes = process_files()
    
    print(f"\n{'='*60}")
    print(f"Processed {total} files")
    print(f"Updated {updated} files")
    print(f"Total link changes: {changes}")
    print("=" * 60)

if __name__ == "__main__":
    main()

