"""
Clean up the exported Intercom folders to have cleaner names.
"""

import os
import shutil
from pathlib import Path

OUTPUT_DIR = Path(__file__).parent.parent / "intercom_export"

# Mapping of messy folder names to clean names
FOLDER_MAPPING = {
    "Getting StartedEverything you need to get going.By Matt and 1 other2 authors16 articles": "01 - Getting Started",
    "StrategyHow to use BigShort for profitBy Sara and 1 other2 authors23 articles": "02 - Strategy",
    "Indicators & FeaturesDeep dives into BigShort indicatorsBy Matt and 1 other2 authors7 articles": "03 - Indicators & Features",
    "GeneralEverything elseBy Sara and 1 other2 authors5 articles": "04 - General",
    "Discord CommunityAll things DiscordBy Sara and 1 other2 authors3 articles": "05 - Discord Community",
    "BigResearchBooks and research to make you a better traderBy Matt1 author11 articles": "06 - BigResearch"
}

def cleanup():
    print(f"Cleaning up folder names in {OUTPUT_DIR}")
    
    for old_name, new_name in FOLDER_MAPPING.items():
        old_path = OUTPUT_DIR / old_name
        new_path = OUTPUT_DIR / new_name
        
        if old_path.exists():
            if new_path.exists():
                shutil.rmtree(new_path)
            old_path.rename(new_path)
            print(f"  Renamed: {old_name[:40]}... -> {new_name}")
        else:
            print(f"  Skipping (not found): {old_name[:40]}...")
    
    print("\nDone!")

if __name__ == "__main__":
    cleanup()

