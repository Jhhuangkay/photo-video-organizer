# Quick Start Guide

## First Time Setup

```bash
# 1. Activate virtual environment
source venv/bin/activate

# 2. Install Python packages (if not already done)
pip install -r requirements.txt

# 3. Install exiftool for video support
brew install exiftool

# 4. Test everything works
python test_heic.py          # Test photo support
python test_video_support.py  # Test video support
```

## Running the Organizer

```bash
# Activate environment
source venv/bin/activate

# Run the organizer
python photo_video_organizer.py
```

## What It Does

1. Scans `~/Desktop/Photos` for photos and videos
2. Extracts GPS coordinates and dates
3. Groups nearby photos/videos into clusters
4. Queries landmark names for each cluster
5. Organizes into: `Continent/Country/City/Date_Landmark/`
6. Copies files (originals stay untouched)

## Example Output Structure

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
│               ├── IMG_3450.HEIC
│               └── VID_3451.MOV
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
        ├── 2024-01-15/
        │   └── downloaded_photo.jpg
        └── 2024-03-13/
            └── edited_photo.jpg
```

## Smart Features

- **GPS-based organization**: Photos/videos with GPS → Continent/Country/City/Date_Landmark/
- **Date fallback**: No GPS? Organized by date in Uncategorized/No_GPS/YYYY-MM-DD/
- **Screenshot detection**: Screenshots go to Uncategorized/Screenshots/
- **Clustering**: Nearby photos grouped together with landmark names

## Customization

Edit these variables in `photo_video_organizer.py`:

```python
SOURCE_DIR = "~/Desktop/Photos"              # Where your files are
OUTPUT_DIR = "~/Desktop/Photos_Organized"    # Where to organize them
COPY_MODE = True                             # True=copy, False=move
CLUSTER_RADIUS_KM = 0.2                      # Grouping distance (200m)
```

## Troubleshooting

### "exiftool not found"
```bash
brew install exiftool
```

### "No module named 'pillow_heif'"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### Videos not being organized
- Check if exiftool is installed: `exiftool -ver`
- Check if video has GPS data: `exiftool -GPSLatitude -GPSLongitude your_video.MOV`
- Videos without GPS go to `Uncategorized/No_GPS/`
