# Web-Based Post Reviewer Guide

## 🌐 Why Web Version?

Your Python installation doesn't have tkinter (GUI library), so I created a web-based version that runs in your browser instead!

## 🚀 How to Use

### Start the Server

```bash
python post_reviewer_web.py
```

This will:
1. Start a local web server
2. Automatically open your browser
3. Load all your posts

### Interface

**Navigation:**
- ◀ Previous / Next ▶ buttons
- Post counter (Post 1 of 6)
- 🔄 Reload button

**Post Details (Left Side):**
- Post information (ID, schedule, location)
- Caption editor (bilingual)
- Hashtags editor
- Media files list

**Actions (Right Side):**
- Status badge
- ✅ Approve button
- ❌ Reject button
- 📋 Copy Caption button
- 🌐 Facebook button
- 📸 Instagram button

### Workflow

1. **Review** - Read the post details
2. **Edit** - Modify caption/hashtags if needed
3. **Copy** - Click "Copy Caption"
4. **Open** - Click "Facebook" or "Instagram"
5. **Post** - Paste caption and upload media
6. **Approve** - Click "Approve" to mark as done
7. **Next** - Automatically moves to next post

### Features

✅ **No Installation** - Just Python, no extra libraries
✅ **Browser-Based** - Works in any modern browser
✅ **Auto-Save** - Changes saved automatically
✅ **Mobile-Friendly** - Responsive design
✅ **Fast** - Lightweight and quick

## 🎯 Quick Actions

### Copy Caption
1. Click "📋 Copy Caption"
2. Caption + hashtags copied to clipboard
3. Ready to paste!

### Post to Facebook
1. Click "Copy Caption"
2. Click "🌐 Facebook"
3. Create new post
4. Paste caption
5. Upload photos from media list
6. Post!

### Post to Instagram
1. Click "Copy Caption"
2. Click "📸 Instagram"
3. Create new post
4. Upload photos from media list
5. Paste caption
6. Post!

## 💡 Tips

- **Keep Server Running** - Don't close the terminal while reviewing
- **Refresh Page** - If posts don't load, refresh the browser
- **Edit Freely** - All changes are saved automatically
- **Multiple Tabs** - Can open multiple posts in different tabs

## 🛑 Stop the Server

Press `Ctrl+C` in the terminal to stop the server.

## 🔧 Troubleshooting

### Port Already in Use
If port 8080 is busy, edit `post_reviewer_web.py`:
```python
PORT = 8081  # Change to different port
```

### Browser Doesn't Open
Manually open: http://localhost:8080

### Posts Not Loading
1. Check posts exist: `ls ~/Desktop/Photos/Travel_Posts/posts/`
2. Reload the page
3. Check terminal for errors

## 📊 Comparison

| Feature | Web Version | GUI Version |
|---------|-------------|-------------|
| Installation | ✅ No extra libs | ❌ Needs tkinter |
| Interface | Browser | Desktop app |
| Mobile | ✅ Works | ❌ Desktop only |
| Speed | Fast | Fast |
| Editing | ✅ Yes | ✅ Yes |

## ✅ Advantages

- **No tkinter required** - Works with any Python
- **Cross-platform** - Works on Mac, Linux, Windows
- **Modern UI** - Clean, responsive design
- **Easy to use** - Familiar browser interface
- **Shareable** - Can access from other devices on network

## 🎉 That's It!

The web version does everything the GUI version does, but runs in your browser. Perfect solution for systems without tkinter!

```bash
# Start reviewing your posts
python post_reviewer_web.py
```

Happy posting! 🌍✈️📸
