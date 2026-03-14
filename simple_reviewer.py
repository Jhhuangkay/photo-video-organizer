#!/usr/bin/env python3
"""
Simple Post Reviewer
Basic command-line interface to review posts.
"""

import json
from pathlib import Path
import webbrowser

POSTS_DIR = Path.home() / "Desktop" / "Photos" / "Travel_Posts" / "posts"

def load_posts():
    """Load all posts."""
    posts = []
    for post_file in sorted(POSTS_DIR.glob("*.json")):
        with open(post_file, 'r', encoding='utf-8') as f:
            post = json.load(f)
            post['_file'] = post_file
            posts.append(post)
    return posts

def display_post(post, index, total):
    """Display a single post."""
    print("\n" + "=" * 70)
    print(f"POST {index + 1} of {total}")
    print("=" * 70)
    
    print(f"\nPost ID: {post['post_id']}")
    print(f"Scheduled: {post['scheduled_date']} at {post['scheduled_time']}")
    print(f"Location: {post['location']['landmark']}, {post['location']['city']}, {post['location']['country']}")
    print(f"Status: {post['status'].replace('_', ' ').title()}")
    
    print(f"\n--- CAPTION ---")
    print(post['caption']['combined'])
    
    print(f"\n--- HASHTAGS ---")
    print(' '.join(post['hashtags']))
    
    print(f"\n--- MEDIA ({post['media_count']} files) ---")
    for i, media in enumerate(post['media'], 1):
        filename = Path(media).name
        print(f"{i}. {filename}")
    
    print(f"\n--- FOLDER ---")
    print(post['folder'])

def save_post(post):
    """Save post to file."""
    with open(post['_file'], 'w', encoding='utf-8') as f:
        json.dump(post, f, ensure_ascii=False, indent=2)

def main():
    """Main function."""
    if not POSTS_DIR.exists():
        print(f"Error: Posts directory not found: {POSTS_DIR}")
        print("Please run travel_post_generator.py first!")
        return
    
    posts = load_posts()
    
    if not posts:
        print("No posts found!")
        return
    
    print(f"\n📸 Simple Post Reviewer")
    print(f"Found {len(posts)} posts")
    
    index = 0
    
    while True:
        post = posts[index]
        display_post(post, index, len(posts))
        
        print("\n" + "-" * 70)
        print("Commands:")
        print("  [n] Next    [p] Previous    [c] Copy caption")
        print("  [f] Open folder    [b] Open Facebook    [i] Open Instagram")
        print("  [a] Approve    [r] Reject    [q] Quit")
        print("-" * 70)
        
        choice = input("\nYour choice: ").lower().strip()
        
        if choice == 'n':
            if index < len(posts) - 1:
                index += 1
            else:
                print("Already at last post")
        
        elif choice == 'p':
            if index > 0:
                index -= 1
            else:
                print("Already at first post")
        
        elif choice == 'c':
            caption = post['caption']['combined']
            hashtags = ' '.join(post['hashtags'])
            full_text = f"{caption}\n\n{hashtags}"
            
            try:
                import pyperclip
                pyperclip.copy(full_text)
                print("✓ Caption copied to clipboard!")
            except ImportError:
                print("\nCaption text (copy manually):")
                print("-" * 70)
                print(full_text)
                print("-" * 70)
        
        elif choice == 'f':
            webbrowser.open(f"file://{post['folder']}")
            print("✓ Opened folder in Finder")
        
        elif choice == 'b':
            webbrowser.open("https://www.facebook.com/")
            print("✓ Opened Facebook")
        
        elif choice == 'i':
            webbrowser.open("https://www.instagram.com/")
            print("✓ Opened Instagram")
        
        elif choice == 'a':
            post['status'] = 'approved'
            save_post(post)
            print("✓ Post approved!")
            if index < len(posts) - 1:
                index += 1
        
        elif choice == 'r':
            post['status'] = 'rejected'
            save_post(post)
            print("✓ Post rejected")
            if index < len(posts) - 1:
                index += 1
        
        elif choice == 'q':
            print("\nGoodbye!")
            break
        
        else:
            print("Invalid choice")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye!")
