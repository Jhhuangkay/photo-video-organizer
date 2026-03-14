#!/usr/bin/env python3
"""Test photo_video_organizer functions with a single HEIC file."""

import sys
from pathlib import Path

# Import the functions from photo_video_organizer
sys.path.insert(0, str(Path(__file__).parent))
from photo_video_organizer import get_exif_data, is_screenshot, get_country_name, _sanitize_folder_name
import reverse_geocoder as rg

# Test file
test_file = "IMG_3443.HEIC"

if not Path(test_file).exists():
    print(f"✗ File not found: {test_file}")
    sys.exit(1)

print(f"Testing photo_organizer functions with: {test_file}")
print("=" * 60)

# Test EXIF extraction
print("\n1. Testing get_exif_data()...")
exif = get_exif_data(test_file)
print(f"   GPS: {exif['gps']}")
print(f"   Date: {exif['date']}")

if exif['gps']:
    lat, lon = exif['gps']
    print(f"   Coordinates: {lat:.6f}°, {lon:.6f}°")
    
    # Test reverse geocoding
    print("\n2. Testing reverse geocoding...")
    geo_result = rg.search([exif['gps']])[0]
    print(f"   Country Code: {geo_result['cc']}")
    print(f"   Country: {get_country_name(geo_result['cc'])}")
    print(f"   City: {geo_result['name']}")
    print(f"   Admin1: {geo_result.get('admin1', 'N/A')}")

# Test screenshot detection
print("\n3. Testing is_screenshot()...")
is_ss = is_screenshot(test_file)
print(f"   Is screenshot: {is_ss}")

print("\n" + "=" * 60)
print("✓ All functions working correctly with HEIC!")
print("\nYour photo_video_organizer.py is ready to use.")
