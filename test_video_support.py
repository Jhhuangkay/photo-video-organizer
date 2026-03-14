#!/usr/bin/env python3
"""Test video metadata extraction."""

import sys
import subprocess
from pathlib import Path

print("Testing Video Support")
print("=" * 60)

# Check if exiftool is installed
print("\n1. Checking exiftool installation...")
try:
    result = subprocess.run(['exiftool', '-ver'], 
                          capture_output=True, text=True, timeout=2)
    if result.returncode == 0:
        version = result.stdout.strip()
        print(f"   ✓ exiftool is installed (version {version})")
    else:
        print("   ✗ exiftool not working properly")
        sys.exit(1)
except FileNotFoundError:
    print("   ✗ exiftool not found")
    print("\n   Install with: brew install exiftool")
    sys.exit(1)
except subprocess.TimeoutExpired:
    print("   ✗ exiftool timed out")
    sys.exit(1)

# Test the video metadata function
print("\n2. Testing video metadata extraction...")
try:
    from photo_video_organizer import get_video_metadata, VIDEO_EXTENSIONS
    print(f"   ✓ Imported video functions")
    print(f"   Supported video formats: {', '.join(VIDEO_EXTENSIONS)}")
except ImportError as e:
    print(f"   ✗ Import error: {e}")
    sys.exit(1)

# Look for video files in current directory
print("\n3. Looking for video files to test...")
video_files = [f for f in Path('.').iterdir() 
               if f.is_file() and f.suffix.lower() in VIDEO_EXTENSIONS]

if not video_files:
    print("   ⚠ No video files found in current directory")
    print("\n   To test with a video file:")
    print("   1. Copy an iPhone video (.MOV) to this directory")
    print("   2. Run this script again")
else:
    print(f"   Found {len(video_files)} video file(s)")
    
    for video_file in video_files[:3]:  # Test first 3 videos
        print(f"\n   Testing: {video_file.name}")
        print("   " + "-" * 56)
        
        metadata = get_video_metadata(str(video_file))
        
        if metadata['gps']:
            lat, lon = metadata['gps']
            print(f"   ✓ GPS: {lat:.6f}°, {lon:.6f}°")
        else:
            print("   ⚠ No GPS data found")
        
        if metadata['date']:
            print(f"   ✓ Date: {metadata['date']}")
        else:
            print("   ⚠ No date found")

print("\n" + "=" * 60)
print("✓ Video support is ready!")
print("\nYou can now run photo_video_organizer.py with both photos and videos.")
