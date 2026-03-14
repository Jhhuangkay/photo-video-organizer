#!/usr/bin/env python3
"""Test HEIC image reading with the photo organizer's EXIF extraction."""

import sys
from pathlib import Path

# Test imports
try:
    import pillow_heif
    pillow_heif.register_heif_opener()
    from PIL import Image
    from PIL.ExifTags import TAGS, GPSTAGS
    print("✓ All imports successful\n")
except ImportError as e:
    print(f"✗ Import error: {e}")
    print("\nMake sure to install dependencies:")
    print("  source venv/bin/activate")
    print("  pip install -r requirements.txt")
    sys.exit(1)

# Test HEIC file
heic_file = "IMG_3443.HEIC"

if not Path(heic_file).exists():
    print(f"✗ File not found: {heic_file}")
    sys.exit(1)

print(f"Testing: {heic_file}")
print("-" * 60)

try:
    # Open image
    img = Image.open(heic_file)
    print(f"✓ Image opened successfully")
    print(f"  Format: {img.format}")
    print(f"  Size: {img.size[0]}x{img.size[1]}")
    print(f"  Mode: {img.mode}")
    
    # Get EXIF data (use getexif() for HEIC compatibility)
    exif_data = img.getexif() if hasattr(img, 'getexif') else img._getexif()
    
    if not exif_data:
        print("\n✗ No EXIF data found in image")
        sys.exit(0)
    
    print(f"\n✓ EXIF data found ({len(exif_data)} tags)")
    
    # Look for GPS and date info
    has_gps = False
    has_date = False
    
    for tag_id, value in exif_data.items():
        tag = TAGS.get(tag_id, tag_id)
        
        if tag == "GPSInfo":
            has_gps = True
            print(f"\n✓ GPS data found:")
            # Handle both dict and IFD types
            if hasattr(value, 'items'):
                for gps_tag_id, gps_value in value.items():
                    gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    print(f"    {gps_tag}: {gps_value}")
            else:
                # For getexif(), GPSInfo is an IFD tag ID
                gps_ifd = exif_data.get_ifd(tag_id)
                for gps_tag_id, gps_value in gps_ifd.items():
                    gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                    print(f"    {gps_tag}: {gps_value}")
        
        elif tag in ["DateTimeOriginal", "DateTime"]:
            has_date = True
            print(f"\n✓ Date found: {value}")
        
        elif tag == "Make":
            print(f"\n  Camera Make: {value}")
        elif tag == "Model":
            print(f"  Camera Model: {value}")
    
    if not has_gps:
        print("\n⚠ No GPS data in this image")
    if not has_date:
        print("⚠ No date/time data in this image")
    
    print("\n" + "=" * 60)
    print("✓ HEIC support is working correctly!")
    
except Exception as e:
    print(f"\n✗ Error reading HEIC file: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
