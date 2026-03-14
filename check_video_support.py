#!/usr/bin/env python3
"""Check if video metadata extraction is possible and test it."""

import sys
from pathlib import Path

print("Checking video metadata extraction options...\n")
print("=" * 60)

# Option 1: Try ffmpeg-python (requires ffmpeg installed)
print("\n1. Checking ffmpeg-python...")
try:
    import ffmpeg
    print("   ✓ ffmpeg-python is installed")
    has_ffmpeg = True
except ImportError:
    print("   ✗ ffmpeg-python not installed")
    print("   Install with: pip install ffmpeg-python")
    has_ffmpeg = False

# Option 2: Try pymediainfo (requires libmediainfo)
print("\n2. Checking pymediainfo...")
try:
    from pymediainfo import MediaInfo
    print("   ✓ pymediainfo is installed")
    has_pymediainfo = True
except ImportError:
    print("   ✗ pymediainfo not installed")
    print("   Install with: pip install pymediainfo")
    has_pymediainfo = False

# Option 3: Try exiftool wrapper
print("\n3. Checking exiftool...")
try:
    import subprocess
    result = subprocess.run(['exiftool', '-ver'], 
                          capture_output=True, text=True, timeout=2)
    if result.returncode == 0:
        print(f"   ✓ exiftool is installed (version {result.stdout.strip()})")
        has_exiftool = True
    else:
        has_exiftool = False
except (FileNotFoundError, subprocess.TimeoutExpired):
    print("   ✗ exiftool not installed")
    print("   Install with: brew install exiftool")
    has_exiftool = False

print("\n" + "=" * 60)
print("\nRecommendation:")

if has_exiftool:
    print("✓ Use exiftool - it's already installed and works great for videos!")
    print("\nTo add video support to photo_organizer.py:")
    print("  1. Add video extensions: .mov, .mp4, .m4v")
    print("  2. Use subprocess to call exiftool for metadata extraction")
elif has_ffmpeg:
    print("✓ Use ffmpeg-python - it's already installed")
elif has_pymediainfo:
    print("✓ Use pymediainfo - it's already installed")
else:
    print("Install one of these tools:")
    print("  • exiftool (recommended): brew install exiftool")
    print("  • ffmpeg: brew install ffmpeg && pip install ffmpeg-python")
    print("  • pymediainfo: brew install media-info && pip install pymediainfo")

print("\nWould you like me to create an enhanced version with video support?")
