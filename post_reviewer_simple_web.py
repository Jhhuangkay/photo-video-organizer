#!/usr/bin/env python3
"""
Simple Web Post Reviewer
Generates a static HTML file you can open in your browser.
No server needed!
"""

import json
from pathlib import Path
import webbrowser

POSTS_DIR = Path.home() / "Desktop" / "Photos" / "Travel_Posts" / "posts"
OUTPUT_FILE = Path.home() / "Desktop" / "Photos" / "Travel_Posts" / "reviewer.html"


def load_posts():
    """Load all posts from JSON files."""
    posts = []
    if not POSTS_DIR.exists():
        return posts
    
    for post_file in sorted(POSTS_DIR.glob("*.json")):
        try:
            with open(post_file, 'r', encoding='utf-8') as f:
                post = json.load(f)
                post['_file'] = str(post_file)
                posts.append(post)
        except Exception as e:
            print(f"Error loading {post_file}: {e}")
    
    return posts


def create_reviewer_html(posts):
    """Create interactive HTML reviewer."""
    
    # Embed posts data as JavaScript
    posts_json = json.dumps(posts, ensure_ascii=False)
    
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Travel Post Reviewer</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background: #f0f2f5; }}
        .header {{ background: #1877f2; color: white; padding: 20px; text-align: center; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .container {{ max-width: 1000px; margin: 20px auto; padding: 0 20px; }}
        .nav {{ background: white; padding: 20px; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .nav-buttons button {{ margin: 0 5px; padding: 10px 20px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; font-weight: 500; }}
        .btn-primary {{ background: #1877f2; color: white; }}
        .btn-secondary {{ background: #e4e6eb; color: #050505; }}
        button:hover {{ opacity: 0.9; }}
        button:disabled {{ opacity: 0.5; cursor: not-allowed; }}
        .counter {{ font-size: 18px; font-weight: bold; color: #1877f2; }}
        .post-card {{ background: white; border-radius: 8px; padding: 25px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); margin-bottom: 20px; }}
        .section {{ margin-bottom: 20px; }}
        .section-title {{ font-size: 12px; font-weight: bold; color: #65676b; margin-bottom: 8px; text-transform: uppercase; letter-spacing: 0.5px; }}
        .info-box {{ background: #f0f2f5; padding: 15px; border-radius: 6px; font-size: 14px; line-height: 1.8; }}
        .caption-box {{ width: 100%; min-height: 120px; padding: 15px; border: 1px solid #ddd; border-radius: 6px; font-size: 15px; line-height: 1.6; font-family: inherit; resize: vertical; }}
        .hashtags {{ color: #1877f2; font-size: 14px; padding: 10px; background: #f0f2f5; border-radius: 6px; }}
        .media-list {{ background: #f0f2f5; padding: 15px; border-radius: 6px; }}
        .media-item {{ padding: 8px; font-size: 13px; color: #65676b; border-bottom: 1px solid #e4e6eb; }}
        .media-item:last-child {{ border-bottom: none; }}
        .status-badge {{ display: inline-block; padding: 6px 14px; border-radius: 12px; font-size: 13px; font-weight: bold; }}
        .status-pending {{ background: #fff3cd; color: #856404; }}
        .status-approved {{ background: #d4edda; color: #155724; }}
        .status-rejected {{ background: #f8d7da; color: #721c24; }}
        .actions {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 10px; margin-top: 20px; }}
        .action-btn {{ padding: 12px; border: none; border-radius: 6px; font-size: 14px; font-weight: bold; cursor: pointer; }}
        .btn-approve {{ background: #42b72a; color: white; }}
        .btn-reject {{ background: #f02849; color: white; }}
        .btn-copy {{ background: #1877f2; color: white; }}
        .btn-link {{ background: #e4e6eb; color: #050505; }}
        .success-msg {{ background: #d4edda; color: #155724; padding: 12px; border-radius: 6px; margin: 10px 0; display: none; }}
        .success-msg.show {{ display: block; }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📸 Travel Post Reviewer</h1>
    </div>
    
    <div class="container">
        <div class="nav">
            <div class="nav-buttons">
                <button class="btn-secondary" onclick="prevPost()" id="prevBtn">◀ Previous</button>
                <button class="btn-secondary" onclick="nextPost()" id="nextBtn">Next ▶</button>
            </div>
            <div class="counter" id="counter">Post 1 of {len(posts)}</div>
        </div>
        
        <div id="successMsg" class="success-msg"></div>
        
        <div class="post-card">
            <div class="section">
                <div class="section-title">Post Information</div>
                <div class="info-box" id="postInfo"></div>
            </div>
            
            <div class="section">
                <div class="section-title">Status</div>
                <span class="status-badge status-pending" id="statusBadge">Pending Review</span>
            </div>
            
            <div class="section">
                <div class="section-title">Caption (Bilingual - Editable)</div>
                <textarea class="caption-box" id="captionText"></textarea>
            </div>
            
            <div class="section">
                <div class="section-title">Hashtags</div>
                <div class="hashtags" id="hashtagsText"></div>
            </div>
            
            <div class="section">
                <div class="section-title">Media Files</div>
                <div class="media-list" id="mediaList"></div>
            </div>
            
            <div class="actions">
                <button class="action-btn btn-copy" onclick="copyCaption()">📋 Copy Caption</button>
                <button class="action-btn btn-link" onclick="openFolder()">📁 Open Folder</button>
                <button class="action-btn btn-link" onclick="openFacebook()">🌐 Facebook</button>
                <button class="action-btn btn-link" onclick="openInstagram()">📸 Instagram</button>
                <button class="action-btn btn-approve" onclick="approvePost()">✅ Approve & Next</button>
                <button class="action-btn btn-reject" onclick="rejectPost()">❌ Reject & Next</button>
            </div>
        </div>
    </div>
    
    <script>
        // Embedded posts data
        const posts = {posts_json};
        let currentIndex = 0;
        
        function displayPost() {{
            if (posts.length === 0) {{
                document.getElementById('postInfo').textContent = 'No posts found';
                return;
            }}
            
            const post = posts[currentIndex];
            
            // Update counter
            document.getElementById('counter').textContent = `Post ${{currentIndex + 1}} of ${{posts.length}}`;
            
            // Update buttons
            document.getElementById('prevBtn').disabled = currentIndex === 0;
            document.getElementById('nextBtn').disabled = currentIndex === posts.length - 1;
            
            // Update info
            const info = `Post ID: ${{post.post_id}}
Scheduled: ${{post.scheduled_date}} at ${{post.scheduled_time}}
Location: ${{post.location.landmark}}, ${{post.location.city}}, ${{post.location.country}}
Original Date: ${{post.location.original_date}}
Platforms: ${{post.platforms.join(', ')}}`;
            document.getElementById('postInfo').textContent = info;
            
            // Update status
            const status = post.status.replace('_', ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
            const badge = document.getElementById('statusBadge');
            badge.textContent = status;
            badge.className = 'status-badge status-' + post.status.split('_')[0];
            
            // Update caption
            document.getElementById('captionText').value = post.caption.combined;
            
            // Update hashtags
            document.getElementById('hashtagsText').textContent = post.hashtags.join(' ');
            
            // Update media list
            const mediaHtml = post.media.map(m => {{
                const filename = m.split('/').pop();
                return `<div class="media-item">📎 ${{filename}}</div>`;
            }}).join('');
            document.getElementById('mediaList').innerHTML = mediaHtml;
        }}
        
        function nextPost() {{
            if (currentIndex < posts.length - 1) {{
                currentIndex++;
                displayPost();
            }}
        }}
        
        function prevPost() {{
            if (currentIndex > 0) {{
                currentIndex--;
                displayPost();
            }}
        }}
        
        function showMessage(msg) {{
            const msgEl = document.getElementById('successMsg');
            msgEl.textContent = msg;
            msgEl.classList.add('show');
            setTimeout(() => msgEl.classList.remove('show'), 3000);
        }}
        
        function approvePost() {{
            posts[currentIndex].status = 'approved';
            showMessage('✅ Post approved!');
            displayPost();
            setTimeout(() => {{
                if (currentIndex < posts.length - 1) nextPost();
            }}, 500);
        }}
        
        function rejectPost() {{
            posts[currentIndex].status = 'rejected';
            showMessage('❌ Post rejected');
            displayPost();
            setTimeout(() => {{
                if (currentIndex < posts.length - 1) nextPost();
            }}, 500);
        }}
        
        function copyCaption() {{
            const caption = document.getElementById('captionText').value;
            const hashtags = document.getElementById('hashtagsText').textContent;
            const fullText = caption + '\\n\\n' + hashtags;
            
            navigator.clipboard.writeText(fullText).then(() => {{
                showMessage('📋 Caption copied to clipboard!');
            }}).catch(err => {{
                // Fallback: show text to copy manually
                alert('Copy this text:\\n\\n' + fullText);
            }});
        }}
        
        function openFolder() {{
            const post = posts[currentIndex];
            window.open('file://' + post.folder, '_blank');
        }}
        
        function openFacebook() {{
            window.open('https://www.facebook.com/', '_blank');
        }}
        
        function openInstagram() {{
            window.open('https://www.instagram.com/', '_blank');
        }}
        
        // Keyboard shortcuts
        document.addEventListener('keydown', (e) => {{
            if (e.key === 'ArrowLeft') prevPost();
            if (e.key === 'ArrowRight') nextPost();
            if (e.key === 'c' && e.ctrlKey) copyCaption();
        }});
        
        // Initialize
        displayPost();
    </script>
</body>
</html>
"""
    
    return html


def main():
    """Main function."""
    print("Simple Web Post Reviewer")
    print("=" * 60)
    
    if not POSTS_DIR.exists():
        print(f"\n❌ Posts directory not found: {POSTS_DIR}")
        print("Please run travel_post_generator.py first!")
        return
    
    print(f"\nLoading posts from: {POSTS_DIR}")
    posts = load_posts()
    
    if not posts:
        print("❌ No posts found!")
        return
    
    print(f"✓ Loaded {len(posts)} posts")
    
    print(f"\nGenerating reviewer HTML...")
    html = create_reviewer_html(posts)
    
    print(f"✓ Saving to: {OUTPUT_FILE}")
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"\n✓ Done! Opening in browser...")
    webbrowser.open(f'file://{OUTPUT_FILE}')
    
    print(f"\n" + "=" * 60)
    print("Reviewer opened in your browser!")
    print("\nFeatures:")
    print("  • Navigate: Previous/Next buttons or ← → arrow keys")
    print("  • Copy: Click 'Copy Caption' button")
    print("  • Approve/Reject: Updates status and moves to next")
    print("  • Open folder/social media: Click respective buttons")
    print("\nNote: This is a static HTML file. Changes are shown but not saved.")
    print("Use simple_reviewer.py for saving changes to posts.")


if __name__ == "__main__":
    main()
