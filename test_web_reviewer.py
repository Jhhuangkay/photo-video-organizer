#!/usr/bin/env python3
"""Test if web reviewer can start."""

from pathlib import Path

POSTS_DIR = Path.home() / "Desktop" / "Photos" / "Travel_Posts" / "posts"

print("Testing Web Reviewer Setup")
print("=" * 60)

print(f"\nPosts directory: {POSTS_DIR}")
print(f"Exists: {POSTS_DIR.exists()}")

if POSTS_DIR.exists():
    posts = list(POSTS_DIR.glob("*.json"))
    print(f"Found {len(posts)} post files")
    
    if posts:
        print("\nSample post files:")
        for post in posts[:3]:
            print(f"  - {post.name}")
        
        print("\n✓ Ready to start web reviewer!")
        print("\nRun: python post_reviewer_web.py")
    else:
        print("\n❌ No post files found!")
        print("Run: python travel_post_generator.py")
else:
    print("\n❌ Posts directory not found!")
    print("Run: python travel_post_generator.py")
