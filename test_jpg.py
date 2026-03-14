#!/usr/bin/env python3
"""Test JPG file to see if metadata can be extracted."""

import sys
from pathlib import Path

# Test file
test_file = "S__59686947.jpg"

if not Path(test_file).exists():
    print(f"✗ File not found: {test_file}")
    sys.exit(1)

print(f"Testing: {test_file}")
print("=" * 60)

# Test with photo_video_organizer functions
try:
    from photo_video_organizer import get_metadata, is_screenshot
    
    print("\n1. Testing metadata extraction...")
    metadata = get_metadata(test_file)
    
    print(f"   GPS: {metadata['gps']}")
    print(f"   Date: {metadata['date']}")
    
    if metadata['gps']:
        lat, lon = metadata['gps']
        print(f"   Coordinates: {lat:.6f}°, {lon:.6f}°")
    else:
        print("   ⚠ No GPS data found in this image")
    
    if not metadata['date']:
        print("   ⚠ No date found in this image")
    
    print("\n2. Testing screenshot detection...")
    is_ss = is_screenshot(test_file)
    print(f"   Is screenshot: {is_ss}")
    
    # Try to open with Pillow to see basic info
    print("\n3. Basic image info...")
    from PIL import Image
    img = Image.open(test_file)
    print(f"   Format: {img.format}")
    print(f"   Size: {img.size[0]}x{img.size[1]}")
    print(f"   Mode: {img.mode}")
    
    # Check if it has any EXIF at all
    exif = img.getexif() if hasattr(img, 'getexif') else img._getexif()
    if exif:
        print(f"   EXIF tags found: {len(exif)}")
        
        # Show what EXIF tags are present
        from PIL.ExifTags import TAGS
        print("\n4. Available EXIF tags:")
        for tag_id, value in list(exif.items())[:10]:  # Show first 10
            tag = TAGS.get(tag_id, tag_id)
            print(f"   - {tag}: {str(value)[:50]}")
    else:
        print("   ✗ No EXIF data at all in this image")
    
    print("\n" + "=" * 60)
    
    if not metadata['gps'] and not metadata['date']:
        print("⚠ This image has no GPS or date metadata")
        print("\nPossible reasons:")
        print("  • Photo was edited/processed (metadata stripped)")
        print("  • Downloaded from social media (metadata removed)")
        print("  • Screenshot or screen capture")
        print("  • Taken with GPS disabled")
        print("\nThis file will be moved to: Uncategorized/No_GPS/")
    else:
        print("✓ Image can be organized!")
        
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
