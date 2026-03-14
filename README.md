# Photo & Video Organizer

Automatically organize your photos and videos by location and date using GPS metadata. Perfect for iPhone users with thousands of photos from travels!

## ✨ Features

- 📍 **GPS-based organization** - Automatically sorts by Continent/Country/City/Date/Landmark
- 🎥 **Video support** - Handles both photos (HEIC, JPG, PNG) and videos (MOV, MP4)
- 🗺️ **Smart clustering** - Groups nearby photos together with landmark names
- 📅 **Date fallback** - Organizes files without GPS by date
- 🖼️ **Screenshot detection** - Automatically identifies and separates screenshots
- 🔒 **Safe by default** - Copies files (originals untouched)
- ⚡ **Fast** - Processes 100K photos in minutes
- 🌐 **Offline geocoding** - Country/city lookup works without internet

## 📸 Example Output

```
Photos_Organized/
├── Europe/
│   └── Netherlands/
│       └── Amsterdam/
│           ├── 2021-11-24_Dam_Square/
│           │   ├── IMG_3443.HEIC
│           │   ├── IMG_3444.MOV
│           │   └── IMG_3445.JPG
│           └── 2021-11-25_Vondelpark/
│               └── IMG_3450.HEIC
├── Asia/
│   └── Japan/
│       └── Tokyo/
│           └── 2024-03-15_Shibuya/
│               ├── IMG_5001.HEIC
│               └── VID_5002.MOV
└── Uncategorized/
    ├── Screenshots/
    │   └── Screenshot_2024-03-13.png
    └── No_GPS/
        └── 2024-03-13/
            └── downloaded_photo.jpg
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- exiftool (for video support)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/photo-video-organizer.git
cd photo-video-organizer

# Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install Python dependencies
pip install -r requirements.txt

# Install exiftool (macOS)
brew install exiftool

# Install exiftool (Linux)
sudo apt-get install libimage-exiftool-perl

# Install exiftool (Windows)
# Download from https://exiftool.org/
```

### Usage

```bash
# Activate virtual environment
source venv/bin/activate

# Run the organizer
python photo_video_organizer.py
```

By default, it will:
- Read from: `~/Desktop/Photos`
- Write to: `~/Desktop/Photos_Organized`
- Copy files (originals stay untouched)

### Configuration

Edit `photo_video_organizer.py` to customize:

```python
SOURCE_DIR = "~/Desktop/Photos"              # Your photos/videos location
OUTPUT_DIR = "~/Desktop/Photos_Organized"    # Where to organize them
COPY_MODE = True                             # True=copy, False=move
CLUSTER_RADIUS_KM = 0.2                      # Grouping distance (200m)
```

## 📋 Supported Formats

### Photos
JPG, JPEG, PNG, HEIC, HEIF, TIFF, BMP, GIF, WEBP

### Videos
MOV, MP4, M4V, AVI, 3GP

## 🧪 Testing

```bash
# Test photo support (HEIC)
python test_heic.py

# Test video support
python test_video_support.py

# Test no-GPS organization
python test_no_gps_organization.py

# Test all features
python test_all_features.py
```

## 🎯 How It Works

1. **Scan** - Finds all photos and videos in source directory
2. **Extract** - Reads GPS coordinates and dates from metadata
3. **Geocode** - Converts GPS to location names (offline)
4. **Cluster** - Groups nearby photos using DBSCAN algorithm
5. **Landmark** - Queries OpenStreetMap for place names (cached)
6. **Organize** - Copies files to organized folder structure

## 🔧 Advanced Features

### Smart Date Handling
- Tries EXIF date first (DateTimeOriginal, CreateDate)
- Falls back to file modification date if no EXIF
- Organizes no-GPS files by date: `Uncategorized/No_GPS/YYYY-MM-DD/`

### Location Clustering
- Groups photos within 200m of each other (configurable)
- Assigns landmark names to each cluster
- Handles duplicate landmark names intelligently

### Screenshot Detection
- Checks filename for "screenshot" keywords
- Detects iPhone screen resolutions without camera metadata
- Separates to `Uncategorized/Screenshots/`

### Duplicate Handling
- Auto-numbers duplicate filenames
- Never overwrites existing files
- Preserves all your photos

## 📚 Documentation

- [Quick Start Guide](QUICK_START.md) - Get started in 5 minutes
- [Installation Checklist](INSTALLATION_CHECKLIST.md) - Step-by-step setup
- [Video Support](VIDEO_SUPPORT_SUMMARY.md) - Video feature details
- [Date Fallback](FALLBACK_DATE_FEATURE.md) - How date fallback works
- [HEIC Fix](HEIC_FIX_SUMMARY.md) - HEIC support details
- [What's New](WHATS_NEW.md) - Latest updates

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

MIT License - feel free to use this for personal or commercial projects.

## ⚠️ Disclaimer

- Always backup your photos before running any organization tool
- Test with a small batch first
- Default COPY mode is safe (originals untouched)
- File modification dates may change when copying

## 🙏 Acknowledgments

- [reverse_geocoder](https://github.com/thampiman/reverse-geocoder) - Offline geocoding
- [Pillow](https://python-pillow.org/) - Image processing
- [pillow-heif](https://github.com/bigcat88/pillow_heif) - HEIC support
- [exiftool](https://exiftool.org/) - Video metadata extraction
- [OpenStreetMap Nominatim](https://nominatim.org/) - Landmark names

## 💡 Tips

- Run on a copy of your photos first to test
- Use COPY mode (default) until you're confident
- Check `Uncategorized/` folders for files that need manual sorting
- Landmark queries are cached - rerunning is fast
- Works great with iPhone, Android, and camera photos

## 🐛 Troubleshooting

### "exiftool not found"
```bash
brew install exiftool  # macOS
sudo apt-get install libimage-exiftool-perl  # Linux
```

### "No module named 'pillow_heif'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Videos not being organized
- Check if exiftool is installed: `exiftool -ver`
- Check if video has GPS: `exiftool -GPSLatitude -GPSLongitude video.MOV`
- Videos without GPS go to `Uncategorized/No_GPS/YYYY-MM-DD/`

### Photos organized to wrong location
- GPS accuracy varies (especially indoors)
- Check GPS coordinates: `exiftool -GPSLatitude -GPSLongitude photo.jpg`
- Adjust `CLUSTER_RADIUS_KM` if needed

## 📧 Contact

Questions? Issues? Open a GitHub issue or reach out!

---

Made with ❤️ for travelers and photo enthusiasts
