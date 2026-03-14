# 📸 Travel Social Media Automation System

Automatically organize your travel photos by location and generate professional bilingual social media posts for Facebook and Instagram.

## ✨ Features

### 🗺️ Smart Photo Organization
- GPS-based organization (Continent/Country/City/Date/Landmark)
- Supports HEIC (iPhone), MOV, MP4, JPG, PNG formats
- Date fallback for photos without GPS
- Smart clustering to group nearby photos
- Automatic landmark detection via OpenStreetMap
- Screenshot detection and separation

### 📝 Automated Post Generation
- Bilingual captions (English + Traditional Chinese)
- Engaging 2-3 sentence captions per language
- Relevant hashtags (8 per post)
- Smart photo selection (4-5 best per location)
- Daily posting schedule
- Visual preview with actual images
- Works completely offline (no API keys needed)

### 🌐 Interactive Web Reviewer
- Clean web interface (opens in browser)
- Navigate with buttons or arrow keys
- Edit captions inline
- One-click copy to clipboard
- Quick links to Facebook and Instagram
- Approve/reject workflow
- Mobile-friendly design

## 🚀 Quick Start

### Installation

1. Clone the repository:
```bash
git clone https://github.com/YOURUSERNAME/travel-social-media-automation.git
cd travel-social-media-automation
```

2. Create virtual environment:
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Install exiftool (for video support):
```bash
# macOS
brew install exiftool

# Ubuntu/Debian
sudo apt-get install libimage-exiftool-perl

# Windows
# Download from https://exiftool.org/
```

### Usage

#### Step 1: Organize Your Photos
```bash
python photo_video_organizer.py
```
- Place your iPhone photos in `~/Desktop/Photos/`
- Script organizes them to `~/Desktop/Photos_Organized/`
- Structure: `Continent/Country/City/Date_Landmark/`

#### Step 2: Generate Posts
```bash
python travel_post_generator.py
```
- Scans organized photos
- Generates bilingual captions and hashtags
- Creates posting schedule
- Output: `~/Desktop/Photos/Travel_Posts/`

#### Step 3: Review & Post (Daily)
```bash
python post_reviewer_simple_web.py
```
- Opens interactive web interface
- Review today's post
- Copy caption and post to social media
- Mark as approved

## 📖 Example Output

### Organized Photos
```
Photos_Organized/
├── Europe/
│   └── Netherlands/
│       └── Amsterdam/
│           └── 2021-11-24_Dam_Square/
│               ├── IMG_1234.jpg
│               ├── IMG_1235.jpg
│               └── IMG_1236.MOV
└── Asia/
    └── Japan/
        └── Tokyo/
            └── 2024-03-15_Shibuya/
                ├── IMG_5678.HEIC
                └── IMG_5679.jpg
```

### Generated Post
```
Exploring the beautiful Dam Square in Amsterdam, Netherlands. This place 
truly captures the essence of the city with its stunning architecture and 
vibrant atmosphere. Every corner tells a story, and I'm grateful to 
experience it firsthand. 🇪🇺

探索荷蘭阿姆斯特丹美麗的Dam Square。這個地方以其令人驚嘆的建築和
充滿活力的氛圍真正捕捉了城市的精髓。每個角落都訴說著一個故事，
我很感激能親身體驗。🇪🇺

#Amsterdam #Netherlands #Travel #TravelPhotography #Wanderlust #Explore 
#EuropeTravel #DamSquare

Photos: IMG_1234.jpg, IMG_1235.jpg, IMG_1236.MOV
Scheduled: 2026-03-13
```

## 🎯 Complete Workflow

### One-Time Setup
1. Transfer photos from iPhone to `~/Desktop/Photos/`
2. Run organizer: `python photo_video_organizer.py`
3. Generate posts: `python travel_post_generator.py`

### Daily Routine (2 minutes)
1. Run reviewer: `python post_reviewer_simple_web.py`
2. Review caption and photos
3. Click "📋 Copy Caption"
4. Click "🌐 Facebook" or "📸 Instagram"
5. Paste caption and upload photos
6. Click "✅ Approve & Next"

## ⚙️ Configuration

### Photo Organizer
Edit `photo_video_organizer.py`:
```python
SOURCE_DIR = "~/Desktop/Photos"
OUTPUT_DIR = "~/Desktop/Photos_Organized"
COPY_MODE = True  # True=copy, False=move
CLUSTER_RADIUS_KM = 0.2  # Grouping distance
```

### Post Generator
Edit `travel_post_generator.py`:
```python
ORGANIZED_PHOTOS_DIR = "~/Desktop/Photos_Organized"
OUTPUT_DIR = "~/Desktop/Travel_Posts"
POSTS_PER_DAY = 1  # Daily posts
START_DATE = datetime.now()  # Start date
```

## 📚 Documentation

- [Complete System Guide](FINAL_SYSTEM_GUIDE.md) - Comprehensive overview
- [Social Media Automation](SOCIAL_MEDIA_AUTOMATION.md) - Detailed documentation
- [Quick Start Guide](SOCIAL_MEDIA_QUICK_START.md) - Get started fast
- [Web Reviewer Guide](WEB_REVIEWER_GUIDE.md) - Reviewer interface details

## 🛠️ Technical Details

### Supported Formats
- **Images:** JPG, JPEG, PNG, HEIC, HEIF
- **Videos:** MOV, MP4, M4V, AVI, 3GP

### Dependencies
- Pillow - Image processing
- pillow-heif - HEIC support
- reverse_geocoder - Offline geocoding
- pycountry - Country data
- scikit-learn - Clustering algorithm
- numpy - Numerical operations
- requests - API calls

### System Requirements
- Python 3.8+
- exiftool (for video metadata)
- 100MB+ disk space
- Internet connection (for OpenStreetMap landmark queries)

## 💡 Tips

### For Best Results
1. Transfer photos with "Export Unmodified Originals" to preserve metadata
2. Keep original filenames
3. Review captions before posting
4. Customize captions to add personal touch
5. Post consistently for audience growth

### Keyboard Shortcuts (Reviewer)
- `←` Previous post
- `→` Next post

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenStreetMap Nominatim for landmark data
- reverse_geocoder for offline location lookup
- pillow-heif for HEIC support

## 📧 Contact

For questions or suggestions, please open an issue on GitHub.

---

**Built with ❤️ for travelers who want to share their adventures** ✈️📸🌏

*No API keys needed • Works offline • Full control • Professional results*
