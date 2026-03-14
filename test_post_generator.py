#!/usr/bin/env python3
"""Quick test of the post generator."""

from travel_post_generator import scan_organized_photos, generate_posts, create_preview_html
from datetime import datetime
from pathlib import Path

print("Testing Post Generator...")
print("=" * 60)

# Test scanning
ORGANIZED_DIR = Path.home() / "Desktop" / "Photos" / "Photos_Organized"
print(f"\nScanning: {ORGANIZED_DIR}")

locations = scan_organized_photos(str(ORGANIZED_DIR))
print(f"Found {len(locations)} locations")

if locations:
    print("\nSample location:")
    loc = locations[0]
    print(f"  City: {loc['city']}")
    print(f"  Country: {loc['country']}")
    print(f"  Landmark: {loc['landmark']}")
    print(f"  Media files: {loc['media_count']}")
    
    # Test post generation
    print("\nGenerating test posts...")
    posts = generate_posts(locations[:2], datetime.now(), 1)  # Just 2 posts for testing
    print(f"Generated {len(posts)} posts")
    
    if posts:
        print("\nSample post:")
        post = posts[0]
        print(f"  Caption (EN): {post['caption']['en']}")
        print(f"  Caption (ZH): {post['caption']['zh']}")
        print(f"  Hashtags: {' '.join(post['hashtags'][:3])}...")
        print(f"  Media: {post['media_count']} files")
    
    print("\n✓ Post generator is working!")
else:
    print("\n❌ No locations found. Run photo_video_organizer.py first!")
