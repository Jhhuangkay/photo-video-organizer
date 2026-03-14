# Video Support Setup Guide

## What's New

Your `photo_organizer.py` now supports both photos AND videos!

### Supported Video Formats
- .MOV (iPhone default)
- .MP4
- .M4V
- .AVI
- .3GP

## Installation

### 1. Install exiftool (Required for videos)

```bash
brew install exiftool
```

### 2. Verify installation

```bash
exiftool -ver
```

You should see a version number (e.g., 12.76).

## How It Works

The enhanced script:

1. **Detects file type** - Automatically uses the right metadata extractor:
   - Photos (JPG, HEIC, PNG, etc.) → Pillow/EXIF
   - Videos (MOV, MP4, etc.) → exiftool

2. **Extracts GPS & date** - Works the same for both:
   - GPS coordinates from video metadata
   - Creation date from video metadata

3. **Organizes together** - Photos and videos from the same location/date go in the same folder:
   ```
   Europe/Netherlands/Amsterdam/2021-11-24_Dam_Square/
     ├── IMG_3443.HEIC
     ├── IMG_3444.MOV
     └── IMG_3445.JPG
   ```

## Testing

To test with a video file:

```bash
# Test if exiftool can read your video
exiftool -GPSLatitude -GPSLongitude -CreateDate your_video.MOV

# Run the organizer
source venv/bin/activate
python photo_video_organizer.py
```

## What If exiftool Isn't Installed?

If exiftool is not installed:
- Photos will still work perfectly
- Videos will be moved to "Uncategorized/No_GPS" folder
- You'll see a warning in the console

## Performance

- Video metadata extraction is fast (< 0.1 seconds per video)
- No video transcoding or processing happens
- Only metadata is read, files are copied/moved as-is
