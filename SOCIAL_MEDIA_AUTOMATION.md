# Social Media Automation System

Complete workflow for creating travel posts from your organized photos.

## 🎯 Overview

```
Step 1: Organize Photos          Step 2: Generate Posts         Step 3: Review & Post
photo_video_organizer.py    →    travel_post_generator.py   →   post_reviewer.py
                                                                  (GUI Tool)
```

## 📋 Complete Workflow

### Step 1: Organize Your Photos

```bash
# Run the photo organizer first
python photo_video_organizer.py
```

This creates:
```
Photos_Organized/
├── Europe/Netherlands/Amsterdam/2021-11-24_Dam_Square/
├── Asia/Japan/Tokyo/2024-03-15_Shibuya/
└── ...
```

### Step 2: Generate Travel Posts

```bash
# Generate posts from organized photos
python travel_post_generator.py
```

This creates:
```
Travel_Posts/
├── posts/
│   ├── 2021-11-24_amsterdam_0.json
│   ├── 2024-03-15_tokyo_1.json
│   └── ...
├── posting_schedule.json
├── summary.json
└── preview.html  ← Open this to review all posts
```

### Step 3: Review & Publish

**Option A: Web Version (Recommended - No tkinter needed)**
```bash
python post_reviewer_web.py
```
Opens in your browser automatically at http://localhost:8080

**Option B: GUI Version (Requires tkinter)**
```bash
python post_reviewer.py
```

Features (both versions):
- ✅ Review each post
- ✏️ Edit captions
- 📋 Copy to clipboard
- 🌐 Open Facebook/Instagram
- ✓ Approve/Reject posts

## 🎨 What Gets Generated

### Example Post

**Location:** Europe/Netherlands/Amsterdam/2021-11-24_Dam_Square/

**Generated Caption (Bilingual):**
```
Exploring Dam Square in Amsterdam, Netherlands. 🇪🇺

探索荷蘭阿姆斯特丹的Dam Square。🇪🇺

#Amsterdam #Netherlands #Travel #TravelPhotography #Wanderlust #Explore #EuropeTravel #DamSquare
```

**Media:** 4-5 best photos/videos from that location

**Schedule:** Daily posts (configurable)

## ⚙️ Configuration

### travel_post_generator.py

```python
# Where your organized photos are
ORGANIZED_PHOTOS_DIR = "~/Desktop/Photos_Organized"

# Where to save generated posts
OUTPUT_DIR = "~/Desktop/Travel_Posts"

# How many posts per day
POSTS_PER_DAY = 1

# When to start the posting schedule
START_DATE = datetime.now()
```

## 📝 Post Structure

Each post includes:

```json
{
  "post_id": "2021-11-24_amsterdam_0",
  "scheduled_date": "2024-03-20",
  "scheduled_time": "10:00:00",
  "location": {
    "continent": "Europe",
    "country": "Netherlands",
    "city": "Amsterdam",
    "landmark": "Dam Square",
    "original_date": "2021-11-24"
  },
  "caption": {
    "en": "Exploring Dam Square in Amsterdam, Netherlands. 🇪🇺",
    "zh": "探索荷蘭阿姆斯特丹的Dam Square。🇪🇺",
    "combined": "English\n\nChinese"
  },
  "hashtags": ["#Amsterdam", "#Netherlands", "#Travel", ...],
  "media": ["path/to/photo1.jpg", "path/to/photo2.jpg", ...],
  "status": "pending_review",
  "platforms": ["facebook", "instagram"]
}
```

## 🖥️ Post Reviewer GUI

### Features

**Navigation:**
- Previous/Next buttons
- Post counter (Post 1 of 50)
- Reload button

**Post Information:**
- Post ID
- Scheduled date/time
- Location details
- Original photo date
- Target platforms

**Caption Editor:**
- Bilingual captions (English + Traditional Chinese)
- Editable text area
- Professional, concise style

**Hashtags:**
- Auto-generated relevant tags
- Editable

**Media List:**
- Shows all selected photos/videos
- Double-click to open file
- 4-5 media files per post

**Actions:**
- ✅ Approve - Mark as ready to post
- ❌ Reject - Skip this post
- ⏭️ Skip - Move to next without decision
- ✏️ Edit Caption - Enable editing
- 📝 Edit JSON - Open in text editor
- 📁 Open Folder - View original photos

**Publishing:**
- 📋 Copy Caption - Copy to clipboard
- 🌐 Open Facebook - Open in browser
- 📸 Open Instagram - Open in browser

### Workflow

1. Review post details
2. Check caption and hashtags
3. View selected media
4. Edit if needed
5. Click "Copy Caption"
6. Click "Open Facebook" or "Open Instagram"
7. Paste and upload media manually
8. Click "Approve" to mark as posted

## 📊 Generated Content

### Caption Templates

**English (8 variations):**
- "Exploring {landmark} in {city}, {country}. {emoji}"
- "A memorable day at {landmark}, {city}. {emoji}"
- "Discovering the beauty of {landmark} in {city}, {country}. {emoji}"
- And more...

**Traditional Chinese (8 variations):**
- "探索{country}{city}的{landmark}。{emoji}"
- "在{city}的{landmark}度過難忘的一天。{emoji}"
- "發現{country}{city}{landmark}的美麗。{emoji}"
- And more...

### Emojis by Continent

- Europe: 🇪🇺 ✨ 🏰 🌍
- Asia: 🌏 🎎 🏯 ✨
- North America: 🌎 🗽 🌟 ✨
- South America: 🌎 🌴 🎉 ✨
- Africa: 🌍 🦁 🌅 ✨
- Oceania: 🌏 🏖️ 🌊 ✨

### Hashtag Strategy

Auto-generates 8 relevant hashtags:
1. City name (#Amsterdam)
2. Country name (#Netherlands)
3. Generic travel tags (#Travel, #TravelPhotography, #Wanderlust, #Explore)
4. Continent-specific (#EuropeTravel)
5. Landmark name (#DamSquare)

## 🎯 Media Selection

Smart selection algorithm:
- Prioritizes photos over videos
- Selects 4-5 media files per post
- Spreads selection across available media
- Includes 1 video if available
- Avoids duplicates

## 📅 Posting Schedule

- Daily posts (configurable)
- Starts from today (configurable)
- Chronological by original photo date
- 10:00 AM default posting time
- Generates schedule for all locations

## ✨ Features

### No API Keys Required
- Template-based content generation
- No OpenAI/Claude API needed
- Works completely offline
- Free to use

### Bilingual Support
- English + Traditional Chinese
- Professional, concise style
- Culturally appropriate
- Easy to edit

### Smart Content
- Location-aware captions
- Relevant hashtags
- Appropriate emojis
- Professional tone

### Review Before Posting
- Preview all posts in HTML
- GUI tool for easy review
- Edit captions/hashtags
- Approve/reject workflow

### Manual Posting Control
- Copy caption to clipboard
- Open social media sites
- Upload media manually
- Full control over posting

## 📈 Example Output

For 50 travel locations:
- **50 posts** generated
- **200-250 photos/videos** selected
- **Schedule:** 50 days (1 post/day)
- **Languages:** English + Traditional Chinese
- **Platforms:** Facebook + Instagram

## 🔧 Customization

### Add More Caption Templates

Edit `travel_post_generator.py`:

```python
CAPTION_TEMPLATES = {
    "en": [
        "Your custom template here...",
        # Add more
    ],
    "zh": [
        "你的自定義模板...",
        # Add more
    ]
}
```

### Change Posting Frequency

```python
POSTS_PER_DAY = 2  # Post twice daily
POSTS_PER_DAY = 0.5  # Post every 2 days
```

### Adjust Media Selection

```python
# In select_best_media() function
photo_count = min(6, len(photos), max_count)  # Select up to 6 photos
```

## 🚀 Quick Start

```bash
# 1. Organize photos
python photo_video_organizer.py

# 2. Generate posts
python travel_post_generator.py

# 3. Review in browser
open ~/Desktop/Travel_Posts/preview.html

# 4. Use GUI to review and post
python post_reviewer.py
```

## 📱 Posting to Social Media

### Facebook
1. Click "Copy Caption" in reviewer
2. Click "Open Facebook"
3. Create new post
4. Paste caption
5. Upload photos/videos from media list
6. Post!

### Instagram
1. Click "Copy Caption" in reviewer
2. Click "Open Instagram"
3. Create new post
4. Upload photos/videos from media list
5. Paste caption
6. Post!

## 💡 Tips

1. **Review First:** Always preview posts before approving
2. **Edit Freely:** Captions and hashtags are fully editable
3. **Batch Review:** Review multiple posts at once
4. **Save Progress:** Approved posts are saved automatically
5. **Rerun Safe:** Can regenerate posts anytime

## 🎨 Future Enhancements

Possible additions:
- AI-powered captions (with API key)
- Automatic posting via APIs
- Image filters/editing
- Analytics tracking
- Multi-language support (add more languages)
- Custom templates per location type

## 📝 Files Created

```
Travel_Posts/
├── posts/                          # Individual post JSON files
│   ├── 2021-11-24_amsterdam_0.json
│   ├── 2024-03-15_tokyo_1.json
│   └── ...
├── posting_schedule.json           # Master schedule
├── summary.json                    # Statistics
└── preview.html                    # Visual preview
```

## ✅ Checklist

- [ ] Run photo_video_organizer.py
- [ ] Run travel_post_generator.py
- [ ] Open preview.html to review
- [ ] Run post_reviewer.py
- [ ] Review and approve posts
- [ ] Copy captions and post manually
- [ ] Track posted content

## 🎉 Result

You'll have:
- Professional travel posts
- Bilingual captions
- Relevant hashtags
- Best photos selected
- Organized posting schedule
- Full control over content

Perfect for building your travel social media presence! 🌍✈️📸
