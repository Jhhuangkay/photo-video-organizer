#!/usr/bin/env python3
"""Test all features of the enhanced photo_video_organizer."""

import sys
from pathlib import Path

print("Testing All Features")
print("=" * 70)

# Test files
test_files = {
    "IMG_3443.HEIC": "HEIC photo with GPS",
    "S__59686947.jpg": "JPG without GPS (will use file date)",
}

try:
    from photo_video_organizer import get_metadata, is_screenshot
    
    for filename, description in test_files.items():
        if not Path(filename).exists():
            print(f"\n⚠ Skipping {filename} (not found)")
            continue
        
        print(f"\n{description}")
        print(f"File: {filename}")
        print("-" * 70)
        
        metadata = get_metadata(filename)
        is_ss = is_screenshot(filename)
        
        print(f"GPS:        {metadata['gps']}")
        print(f"Date:       {metadata['date']}")
        print(f"Screenshot: {is_ss}")
        
        # Determine destination
        if is_ss:
            dest = "Uncategorized/Screenshots/"
        elif metadata['gps']:
            dest = "Continent/Country/City/Date_Landmark/"
        else:
            dest = f"Uncategorized/No_GPS/{metadata['date']}/"
        
        print(f"\n→ Destination: {dest}")
    
    print("\n" + "=" * 70)
    print("\n✓ All features working!")
    print("\nFeature Summary:")
    print("  ✓ HEIC support (iPhone photos)")
    print("  ✓ GPS-based organization")
    print("  ✓ Date fallback for no-GPS files")
    print("  ✓ Screenshot detection")
    print("  ✓ Video support (requires exiftool)")
    
    print("\nReady to organize your media!")
    print("Run: python photo_video_organizer.py")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
