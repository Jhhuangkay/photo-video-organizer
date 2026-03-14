# Quick Start: Social Media Automation

## 🚀 3-Step Process

### Step 1: Organize Photos (5 minutes)

```bash
# Transfer iPhone photos to ~/Desktop/Photos
# Then run:
python photo_video_organizer.py
```

**Output:** Photos organized by location in `~/Desktop/Photos_Organized/`

### Step 2: Generate Posts (1 minute)

```bash
python travel_post_generator.py
```

**Output:** 
- Posts generated in `~/Desktop/Travel_Posts/`
- Open `~/Desktop/Travel_Posts/preview.html` to see all posts

### Step 3: Review & Post (Daily)

```bash
python post_reviewer.py
```

**Workflow:**
1. Review post → 2. Click "Copy Caption" → 3. Click "Open Facebook/Instagram" → 4. Paste & upload → 5. Click "Approve"

## 📋 Example

**Your Photos:**
```
Photos_Organized/
└── Europe/Netherlands/Amsterdam/2021-11-24_Dam_Square/
    ├── IMG_3443.HEIC
    ├── IMG_3444.MOV
    └── IMG_3445.JPG
```

**Generated Post:**
```
Exploring Dam Square in Amsterdam, Netherlands. 🇪🇺

探索荷蘭阿姆斯特丹的Dam Square。🇪🇺

#Amsterdam #Netherlands #Travel #TravelPhotography #Wanderlust #Explore #EuropeTravel #DamSquare

📸 3 photos selected
📅 Scheduled for tomorrow at 10:00 AM
```

## ⚙️ Configuration (Optional)

Edit `travel_post_generator.py`:

```python
POSTS_PER_DAY = 1  # Change to 2 for twice daily
START_DATE = datetime.now()  # Or set specific date
```

## 🎯 Daily Routine

1. Open `post_reviewer.py`
2. Review today's post
3. Copy caption
4. Post to Facebook/Instagram
5. Mark as "Approved"
6. Done! (2 minutes)

## 💡 Tips

- Generate all posts at once (takes 1 minute)
- Review and post daily (takes 2 minutes)
- Edit captions if needed
- Posts are saved offline - no internet needed for generation

## 📊 What You Get

For 50 travel locations:
- 50 professional posts
- Bilingual captions (EN + ZH)
- 200+ photos/videos selected
- 50-day posting schedule
- All ready for review

## ✅ That's It!

Simple, offline, and you control everything. Perfect for building your travel social media! 🌍✈️
