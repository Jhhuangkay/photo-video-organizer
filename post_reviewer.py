#!/usr/bin/env python3
"""
Post Reviewer & Publisher
Simple GUI tool to review and publish travel posts to Facebook and Instagram.
"""

import json
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from pathlib import Path
from PIL import Image, ImageTk
import webbrowser

# ===== Configuration =====
POSTS_DIR = Path.home() / "Desktop" / "Travel_Posts" / "posts"
SCHEDULE_FILE = Path.home() / "Desktop" / "Travel_Posts" / "posting_schedule.json"


class PostReviewerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Travel Post Reviewer")
        self.root.geometry("900x700")
        
        self.posts = []
        self.current_index = 0
        
        self.setup_ui()
        self.load_posts()
        
    def setup_ui(self):
        """Setup the user interface."""
        # Top frame - Navigation
        nav_frame = ttk.Frame(self.root, padding="10")
        nav_frame.pack(fill=tk.X)
        
        ttk.Button(nav_frame, text="◀ Previous", command=self.prev_post).pack(side=tk.LEFT, padx=5)
        
        self.post_label = ttk.Label(nav_frame, text="Post 0 of 0", font=("Arial", 12, "bold"))
        self.post_label.pack(side=tk.LEFT, padx=20)
        
        ttk.Button(nav_frame, text="Next ▶", command=self.next_post).pack(side=tk.LEFT, padx=5)
        
        ttk.Button(nav_frame, text="🔄 Reload", command=self.load_posts).pack(side=tk.RIGHT, padx=5)
        
        # Main content frame
        content_frame = ttk.Frame(self.root, padding="10")
        content_frame.pack(fill=tk.BOTH, expand=True)
        
        # Left side - Post details
        left_frame = ttk.Frame(content_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Post info
        info_frame = ttk.LabelFrame(left_frame, text="Post Information", padding="10")
        info_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.info_text = scrolledtext.ScrolledText(info_frame, height=6, wrap=tk.WORD, font=("Arial", 10))
        self.info_text.pack(fill=tk.BOTH, expand=True)
        
        # Caption
        caption_frame = ttk.LabelFrame(left_frame, text="Caption (Bilingual)", padding="10")
        caption_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        self.caption_text = scrolledtext.ScrolledText(caption_frame, height=8, wrap=tk.WORD, font=("Arial", 11))
        self.caption_text.pack(fill=tk.BOTH, expand=True)
        
        # Hashtags
        hashtag_frame = ttk.LabelFrame(left_frame, text="Hashtags", padding="10")
        hashtag_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.hashtag_text = tk.Text(hashtag_frame, height=2, wrap=tk.WORD, font=("Arial", 10))
        self.hashtag_text.pack(fill=tk.BOTH, expand=True)
        
        # Media list
        media_frame = ttk.LabelFrame(left_frame, text="Media Files", padding="10")
        media_frame.pack(fill=tk.BOTH, expand=True)
        
        self.media_listbox = tk.Listbox(media_frame, font=("Arial", 9))
        self.media_listbox.pack(fill=tk.BOTH, expand=True)
        self.media_listbox.bind('<Double-Button-1>', self.open_media_file)
        
        # Right side - Actions
        right_frame = ttk.Frame(content_frame, width=250)
        right_frame.pack(side=tk.RIGHT, fill=tk.Y)
        right_frame.pack_propagate(False)
        
        # Status
        status_frame = ttk.LabelFrame(right_frame, text="Status", padding="10")
        status_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.status_label = ttk.Label(status_frame, text="Pending Review", font=("Arial", 11, "bold"))
        self.status_label.pack()
        
        # Edit buttons
        edit_frame = ttk.LabelFrame(right_frame, text="Edit", padding="10")
        edit_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(edit_frame, text="✏️ Edit Caption", command=self.edit_caption, width=20).pack(pady=5)
        ttk.Button(edit_frame, text="📝 Edit JSON", command=self.edit_json, width=20).pack(pady=5)
        ttk.Button(edit_frame, text="📁 Open Folder", command=self.open_folder, width=20).pack(pady=5)
        
        # Action buttons
        action_frame = ttk.LabelFrame(right_frame, text="Actions", padding="10")
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        ttk.Button(action_frame, text="✅ Approve", command=self.approve_post, width=20, 
                  style="Accent.TButton").pack(pady=5)
        ttk.Button(action_frame, text="❌ Reject", command=self.reject_post, width=20).pack(pady=5)
        ttk.Button(action_frame, text="⏭️ Skip", command=self.next_post, width=20).pack(pady=5)
        
        # Publish buttons
        publish_frame = ttk.LabelFrame(right_frame, text="Publish (Manual)", padding="10")
        publish_frame.pack(fill=tk.X)
        
        ttk.Label(publish_frame, text="Copy caption and post manually:", 
                 wraplength=200, font=("Arial", 9)).pack(pady=5)
        
        ttk.Button(publish_frame, text="📋 Copy Caption", command=self.copy_caption, width=20).pack(pady=5)
        ttk.Button(publish_frame, text="🌐 Open Facebook", command=self.open_facebook, width=20).pack(pady=5)
        ttk.Button(publish_frame, text="📸 Open Instagram", command=self.open_instagram, width=20).pack(pady=5)
        
        # Bottom status bar
        self.status_bar = ttk.Label(self.root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
    def load_posts(self):
        """Load all posts from JSON files."""
        if not POSTS_DIR.exists():
            messagebox.showerror("Error", f"Posts directory not found: {POSTS_DIR}\n\nPlease run travel_post_generator.py first!")
            return
        
        self.posts = []
        for post_file in sorted(POSTS_DIR.glob("*.json")):
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    post = json.load(f)
                    post['_file'] = post_file
                    self.posts.append(post)
            except Exception as e:
                print(f"Error loading {post_file}: {e}")
        
        if self.posts:
            self.current_index = 0
            self.display_post()
            self.status_bar.config(text=f"Loaded {len(self.posts)} posts")
        else:
            messagebox.showwarning("No Posts", "No posts found. Please run travel_post_generator.py first!")
    
    def display_post(self):
        """Display current post."""
        if not self.posts:
            return
        
        post = self.posts[self.current_index]
        
        # Update navigation label
        self.post_label.config(text=f"Post {self.current_index + 1} of {len(self.posts)}")
        
        # Display post info
        self.info_text.delete(1.0, tk.END)
        info = f"""Post ID: {post['post_id']}
Scheduled: {post['scheduled_date']} at {post['scheduled_time']}
Location: {post['location']['landmark']}, {post['location']['city']}, {post['location']['country']}
Original Date: {post['location']['original_date']}
Platforms: {', '.join(post['platforms'])}"""
        self.info_text.insert(1.0, info)
        self.info_text.config(state=tk.DISABLED)
        
        # Display caption
        self.caption_text.delete(1.0, tk.END)
        self.caption_text.insert(1.0, post['caption']['combined'])
        
        # Display hashtags
        self.hashtag_text.delete(1.0, tk.END)
        self.hashtag_text.insert(1.0, ' '.join(post['hashtags']))
        
        # Display media files
        self.media_listbox.delete(0, tk.END)
        for media in post['media']:
            filename = Path(media).name
            self.media_listbox.insert(tk.END, filename)
        
        # Update status
        status = post.get('status', 'pending_review').replace('_', ' ').title()
        self.status_label.config(text=status)
        
        # Update status bar
        self.status_bar.config(text=f"Viewing: {post['location']['city']}, {post['location']['country']}")
    
    def next_post(self):
        """Go to next post."""
        if self.current_index < len(self.posts) - 1:
            self.current_index += 1
            self.display_post()
    
    def prev_post(self):
        """Go to previous post."""
        if self.current_index > 0:
            self.current_index -= 1
            self.display_post()
    
    def save_current_post(self):
        """Save current post to file."""
        if not self.posts:
            return
        
        post = self.posts[self.current_index]
        
        # Update caption from text widget
        post['caption']['combined'] = self.caption_text.get(1.0, tk.END).strip()
        
        # Update hashtags
        hashtags_text = self.hashtag_text.get(1.0, tk.END).strip()
        post['hashtags'] = [tag.strip() for tag in hashtags_text.split() if tag.strip().startswith('#')]
        
        # Save to file
        with open(post['_file'], 'w', encoding='utf-8') as f:
            json.dump(post, f, ensure_ascii=False, indent=2)
    
    def approve_post(self):
        """Approve current post."""
        if not self.posts:
            return
        
        self.save_current_post()
        self.posts[self.current_index]['status'] = 'approved'
        
        with open(self.posts[self.current_index]['_file'], 'w', encoding='utf-8') as f:
            json.dump(self.posts[self.current_index], f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("Approved", "Post approved! ✅")
        self.next_post()
    
    def reject_post(self):
        """Reject current post."""
        if not self.posts:
            return
        
        self.posts[self.current_index]['status'] = 'rejected'
        
        with open(self.posts[self.current_index]['_file'], 'w', encoding='utf-8') as f:
            json.dump(self.posts[self.current_index], f, ensure_ascii=False, indent=2)
        
        messagebox.showinfo("Rejected", "Post rejected ❌")
        self.next_post()
    
    def edit_caption(self):
        """Enable caption editing."""
        self.caption_text.config(state=tk.NORMAL)
        self.caption_text.focus()
        messagebox.showinfo("Edit Mode", "Caption is now editable. Click 'Approve' to save changes.")
    
    def edit_json(self):
        """Open JSON file in default editor."""
        if not self.posts:
            return
        
        post_file = self.posts[self.current_index]['_file']
        webbrowser.open(str(post_file))
    
    def open_folder(self):
        """Open media folder in Finder/Explorer."""
        if not self.posts:
            return
        
        folder = self.posts[self.current_index]['folder']
        webbrowser.open(f"file://{folder}")
    
    def open_media_file(self, event):
        """Open selected media file."""
        selection = self.media_listbox.curselection()
        if not selection:
            return
        
        index = selection[0]
        media_file = self.posts[self.current_index]['media'][index]
        webbrowser.open(f"file://{media_file}")
    
    def copy_caption(self):
        """Copy caption to clipboard."""
        caption = self.caption_text.get(1.0, tk.END).strip()
        hashtags = self.hashtag_text.get(1.0, tk.END).strip()
        full_text = f"{caption}\n\n{hashtags}"
        
        self.root.clipboard_clear()
        self.root.clipboard_append(full_text)
        self.status_bar.config(text="Caption copied to clipboard! ✓")
        messagebox.showinfo("Copied", "Caption and hashtags copied to clipboard!\n\nYou can now paste it on Facebook or Instagram.")
    
    def open_facebook(self):
        """Open Facebook in browser."""
        webbrowser.open("https://www.facebook.com/")
        self.status_bar.config(text="Opened Facebook")
    
    def open_instagram(self):
        """Open Instagram in browser."""
        webbrowser.open("https://www.instagram.com/")
        self.status_bar.config(text="Opened Instagram")


def main():
    """Main entry point."""
    root = tk.Tk()
    app = PostReviewerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
