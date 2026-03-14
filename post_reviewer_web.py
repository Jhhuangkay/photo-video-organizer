#!/usr/bin/env python3
"""
Post Reviewer - Web Version
Simple web-based interface to review and manage travel posts.
No tkinter required - runs in your browser!
"""

import json
import webbrowser
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import parse_qs, urlparse
import threading
import time

# ===== Configuration =====
POSTS_DIR = Path.home() / "Desktop" / "Photos" / "Travel_Posts" / "posts"
SCHEDULE_FILE = Path.home() / "Desktop" / "Photos" / "Travel_Posts" / "posting_schedule.json"
PORT = 8080


class PostReviewerHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the post reviewer."""
    
    posts = []
    
    @classmethod
    def load_posts(cls):
        """Load all posts from JSON files."""
        cls.posts = []
        if not POSTS_DIR.exists():
            return
        
        for post_file in sorted(POSTS_DIR.glob("*.json")):
            try:
                with open(post_file, 'r', encoding='utf-8') as f:
                    post = json.load(f)
                    post['_file'] = str(post_file)
                    cls.posts.append(post)
            except Exception as e:
                print(f"Error loading {post_file}: {e}")
    
    def do_GET(self):
        """Handle GET requests."""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/':
            self.serve_main_page()
        elif parsed_path.path == '/api/posts':
            self.serve_posts_json()
        elif parsed_path.path == '/api/post':
            query = parse_qs(parsed_path.query)
            post_id = query.get('id', [None])[0]
            self.serve_single_post(post_id)
        else:
            self.send_error(404)
    
    def do_POST(self):
        """Handle POST requests."""
        parsed_path = urlparse(self.path)
        
        if parsed_path.path == '/api/update':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            data = json.loads(post_data.decode('utf-8'))
            self.update_post(data)
        else:
            self.send_error(404)
    
    def serve_main_page(self):
        """Serve the main HTML page."""
        html = """<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Travel Post Reviewer</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif; background: #f0f2f5; }}
        .header {{ background: #1877f2; color: white; padding: 15px 20px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .header h1 {{ font-size: 24px; }}
        .container {{ max-width: 1200px; margin: 20px auto; padding: 0 20px; }}
        .nav {{ background: white; padding: 15px; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .nav-buttons button {{ margin: 0 5px; padding: 8px 16px; border: none; border-radius: 6px; cursor: pointer; font-size: 14px; }}
        .nav-buttons .btn-primary {{ background: #1877f2; color: white; }}
        .nav-buttons .btn-secondary {{ background: #e4e6eb; color: #050505; }}
        .nav-buttons button:hover {{ opacity: 0.9; }}
        .post-counter {{ font-size: 18px; font-weight: bold; color: #1877f2; }}
        .main-content {{ display: grid; grid-template-columns: 2fr 1fr; gap: 20px; }}
        .post-details {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .post-actions {{ background: white; padding: 20px; border-radius: 8px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .section {{ margin-bottom: 20px; }}
        .section-title {{ font-size: 14px; font-weight: bold; color: #65676b; margin-bottom: 10px; text-transform: uppercase; }}
        .info-box {{ background: #f0f2f5; padding: 12px; border-radius: 6px; font-size: 14px; line-height: 1.6; }}
        .caption-box {{ width: 100%; min-height: 150px; padding: 12px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; line-height: 1.6; resize: vertical; }}
        .hashtags-box {{ width: 100%; padding: 10px; border: 1px solid #ddd; border-radius: 6px; font-size: 14px; }}
        .media-list {{ background: #f0f2f5; padding: 12px; border-radius: 6px; max-height: 200px; overflow-y: auto; }}
        .media-item {{ padding: 6px; font-size: 13px; color: #65676b; border-bottom: 1px solid #e4e6eb; }}
        .media-item:last-child {{ border-bottom: none; }}
        .status-badge {{ display: inline-block; padding: 6px 12px; border-radius: 12px; font-size: 12px; font-weight: bold; }}
        .status-pending {{ background: #fff3cd; color: #856404; }}
        .status-approved {{ background: #d4edda; color: #155724; }}
        .status-rejected {{ background: #f8d7da; color: #721c24; }}
        .action-btn {{ width: 100%; padding: 12px; margin: 8px 0; border: none; border-radius: 6px; font-size: 14px; font-weight: bold; cursor: pointer; }}
        .btn-approve {{ background: #42b72a; color: white; }}
        .btn-reject {{ background: #f02849; color: white; }}
        .btn-copy {{ background: #1877f2; color: white; }}
        .btn-link {{ background: #e4e6eb; color: #050505; }}
        .action-btn:hover {{ opacity: 0.9; }}
        .loading {{ text-align: center; padding: 40px; color: #65676b; }}
        @media (max-width: 768px) {{ .main-content {{ grid-template-columns: 1fr; }} }}
    </style>
</head>
<body>
    <div class="header">
        <h1>📸 Travel Post Reviewer</h1>
    </div>
    
    <div class="container">
        <div class="nav">
            <div class="nav-buttons">
                <button class="btn-secondary" onclick="prevPost()">◀ Previous</button>
                <button class="btn-secondary" onclick="nextPost()">Next ▶</button>
                <button class="btn-secondary" onclick="loadPosts()">🔄 Reload</button>
            </div>
            <div class="post-counter" id="postCounter">Loading...</div>
        </div>
        
        <div class="main-content">
            <div class="post-details">
                <div class="section">
                    <div class="section-title">Post Information</div>
                    <div class="info-box" id="postInfo">Loading...</div>
                </div>
                
                <div class="section">
                    <div class="section-title">Caption (Bilingual)</div>
                    <textarea class="caption-box" id="captionText"></textarea>
                </div>
                
                <div class="section">
                    <div class="section-title">Hashtags</div>
                    <input type="text" class="hashtags-box" id="hashtagsText">
                </div>
                
                <div class="section">
                    <div class="section-title">Media Files</div>
                    <div class="media-list" id="mediaList">Loading...</div>
                </div>
            </div>
            
            <div class="post-actions">
                <div class="section">
                    <div class="section-title">Status</div>
                    <span class="status-badge status-pending" id="statusBadge">Pending Review</span>
                </div>
                
                <div class="section">
                    <div class="section-title">Actions</div>
                    <button class="action-btn btn-approve" onclick="approvePost()">✅ Approve</button>
                    <button class="action-btn btn-reject" onclick="rejectPost()">❌ Reject</button>
                    <button class="action-btn btn-copy" onclick="copyCaption()">📋 Copy Caption</button>
                </div>
                
                <div class="section">
                    <div class="section-title">Open Social Media</div>
                    <button class="action-btn btn-link" onclick="openFacebook()">🌐 Facebook</button>
                    <button class="action-btn btn-link" onclick="openInstagram()">📸 Instagram</button>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let posts = [];
        let currentIndex = 0;
        
        async function loadPosts() {{
            try {{
                const response = await fetch('/api/posts');
                posts = await response.json();
                if (posts.length > 0) {{
                    currentIndex = 0;
                    displayPost();
                }} else {{
                    alert('No posts found. Please run travel_post_generator.py first!');
                }}
            }} catch (error) {{
                console.error('Error loading posts:', error);
                alert('Error loading posts. Check console for details.');
            }}
        }}
        
        function displayPost() {{
            if (posts.length === 0) return;
            
            const post = posts[currentIndex];
            
            // Update counter
            document.getElementById('postCounter').textContent = `Post ${{currentIndex + 1}} of ${{posts.length}}`;
            
            // Update info
            const info = `Post ID: ${{post.post_id}}
Scheduled: ${{post.scheduled_date}} at ${{post.scheduled_time}}
Location: ${{post.location.landmark}}, ${{post.location.city}}, ${{post.location.country}}
Original Date: ${{post.location.original_date}}
Platforms: ${{post.platforms.join(', ')}}`;
            document.getElementById('postInfo').textContent = info;
            
            // Update caption
            document.getElementById('captionText').value = post.caption.combined;
            
            // Update hashtags
            document.getElementById('hashtagsText').value = post.hashtags.join(' ');
            
            // Update media list
            const mediaHtml = post.media.map(m => {{
                const filename = m.split('/').pop();
                return `<div class="media-item">📎 ${{filename}}</div>`;
            }}).join('');
            document.getElementById('mediaList').innerHTML = mediaHtml;
            
            // Update status
            const status = post.status.replace('_', ' ').split(' ').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
            const badge = document.getElementById('statusBadge');
            badge.textContent = status;
            badge.className = 'status-badge status-' + post.status.split('_')[0];
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
        
        async function updatePost(updates) {{
            const post = posts[currentIndex];
            Object.assign(post, updates);
            
            try {{
                await fetch('/api/update', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify(post)
                }});
            }} catch (error) {{
                console.error('Error updating post:', error);
            }}
        }}
        
        async function approvePost() {{
            await updatePost({{ status: 'approved' }});
            alert('Post approved! ✅');
            nextPost();
        }}
        
        async function rejectPost() {{
            await updatePost({{ status: 'rejected' }});
            alert('Post rejected ❌');
            nextPost();
        }}
        
        function copyCaption() {{
            const caption = document.getElementById('captionText').value;
            const hashtags = document.getElementById('hashtagsText').value;
            const fullText = caption + '\\n\\n' + hashtags;
            
            navigator.clipboard.writeText(fullText).then(() => {{
                alert('Caption and hashtags copied to clipboard! ✓\\n\\nYou can now paste it on Facebook or Instagram.');
            }}).catch(err => {{
                console.error('Failed to copy:', err);
                alert('Failed to copy. Please copy manually.');
            }});
        }}
        
        function openFacebook() {{
            window.open('https://www.facebook.com/', '_blank');
        }}
        
        function openInstagram() {{
            window.open('https://www.instagram.com/', '_blank');
        }}
        
        // Load posts on page load
        loadPosts();
    </script>
</body>
</html>
"""
        
        self.send_response(200)
        self.send_header('Content-type', 'text/html; charset=utf-8')
        self.end_headers()
        self.wfile.write(html.encode('utf-8'))
    
    def serve_posts_json(self):
        """Serve all posts as JSON."""
        self.send_response(200)
        self.send_header('Content-type', 'application/json; charset=utf-8')
        self.end_headers()
        self.wfile.write(json.dumps(self.posts, ensure_ascii=False).encode('utf-8'))
    
    def serve_single_post(self, post_id):
        """Serve a single post as JSON."""
        post = next((p for p in self.posts if p['post_id'] == post_id), None)
        if post:
            self.send_response(200)
            self.send_header('Content-type', 'application/json; charset=utf-8')
            self.end_headers()
            self.wfile.write(json.dumps(post, ensure_ascii=False).encode('utf-8'))
        else:
            self.send_error(404)
    
    def update_post(self, post_data):
        """Update a post and save to file."""
        try:
            post_file = Path(post_data['_file'])
            with open(post_file, 'w', encoding='utf-8') as f:
                json.dump(post_data, f, ensure_ascii=False, indent=2)
            
            # Update in memory
            for i, p in enumerate(self.posts):
                if p['post_id'] == post_data['post_id']:
                    self.posts[i] = post_data
                    break
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'success': True}).encode('utf-8'))
        except Exception as e:
            self.send_error(500, str(e))
    
    def log_message(self, format, *args):
        """Suppress log messages."""
        pass


def start_server():
    """Start the web server."""
    PostReviewerHandler.load_posts()
    
    server = HTTPServer(('localhost', PORT), PostReviewerHandler)
    print(f"Post Reviewer Web Server")
    print("=" * 60)
    print(f"\n✓ Server started at http://localhost:{PORT}")
    print(f"✓ Loaded {len(PostReviewerHandler.posts)} posts")
    print(f"\nOpening browser...")
    print(f"\nPress Ctrl+C to stop the server")
    
    # Open browser after a short delay
    def open_browser():
        time.sleep(1)
        webbrowser.open(f'http://localhost:{PORT}')
    
    threading.Thread(target=open_browser, daemon=True).start()
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n\nServer stopped.")
        server.shutdown()


if __name__ == "__main__":
    if not POSTS_DIR.exists():
        print(f"Error: Posts directory not found: {POSTS_DIR}")
        print(f"\nPlease run travel_post_generator.py first!")
        exit(1)
    
    start_server()
