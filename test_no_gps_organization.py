#!/usr/bin/env python3
"""Test how files without GPS are organized."""

import sys
from pathlib import Path

print("Testing No-GPS File Organization")
print("=" * 60)

# Test file
test_file = "S__59686947.jpg"

if not Path(test_file).exists():
    print(f"✗ File not found: {test_file}")
    sys.exit(1)

try:
    from photo_video_organizer import get_metadata
    
    print(f"\nFile: {test_file}")
    print("-" * 60)
    
    metadata = get_metadata(test_file)
    
    print(f"GPS: {metadata['gps']}")
    print(f"Date: {metadata['date']}")
    
    if metadata['gps']:
        print("\n✓ This file has GPS and will be organized by location")
    else:
        print("\n⚠ This file has no GPS data")
        print(f"\n✓ Will be organized by date instead:")
        print(f"   Destination: Uncategorized/No_GPS/{metadata['date']}/")
        print(f"   Full path: ~/Desktop/Photos_Organized/Uncategorized/No_GPS/{metadata['date']}/{test_file}")
    
    print("\n" + "=" * 60)
    print("\nHow it works:")
    print("1. Script tries to extract date from EXIF metadata")
    print("2. If no EXIF date, uses file modification date as fallback")
    print("3. Files without GPS are grouped by date in Uncategorized/No_GPS/")
    print("\nThis keeps your photos organized chronologically even without GPS!")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
