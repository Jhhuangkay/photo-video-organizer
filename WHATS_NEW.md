# What's New - Latest Updates

## ✓ Video Support Added
- Supports MOV, MP4, M4V, AVI, 3GP files
- Uses exiftool for video metadata extraction
- Videos organized alongside photos by location

**Install:** `brew install exiftool`

## ✓ Fallback Date Feature
- Photos/videos without GPS now organized by date
- Uses file modification date if no EXIF date exists
- Structure: `Uncategorized/No_GPS/YYYY-MM-DD/`

**Example:**
```
Before: All no-GPS files in one folder
After:  Uncategorized/No_GPS/2024-01-15/
        Uncategorized/No_GPS/2024-02-20/
        Uncategorized/No_GPS/2024-03-13/
```

## ✓ HEIC Support Fixed
- Updated to use `getexif()` for modern Pillow compatibility
- Properly handles iPhone HEIC/HEIF photos
- GPS and date extraction working perfectly

## ✓ Better File Naming
- Renamed from `photo_organizer.py` to `photo_video_organizer.py`
- More accurately describes what it does

## Complete Feature List

### Organization
- ✓ GPS-based: Continent/Country/City/Date_Landmark/
- ✓ Date-based: Uncategorized/No_GPS/YYYY-MM-DD/
- ✓ Screenshot detection: Uncategorized/Screenshots/
- ✓ Location clustering: Groups nearby photos with DBSCAN
- ✓ Landmark names: Queries OpenStreetMap for place names

### File Support
- ✓ Photos: JPG, JPEG, PNG, HEIC, HEIF, TIFF, BMP, GIF, WEBP
- ✓ Videos: MOV, MP4, M4V, AVI, 3GP
- ✓ Mixed: Photos and videos organized together

### Smart Features
- ✓ Duplicate handling: Auto-numbers duplicate filenames
- ✓ Safe mode: COPY by default (originals untouched)
- ✓ Progress tracking: Shows progress every 500 files
- ✓ Caching: Landmark queries cached to minimize API calls
- ✓ Offline geocoding: Country/city lookup works offline

## Quick Start

```bash
# One-time setup
source venv/bin/activate
pip install -r requirements.txt
brew install exiftool

# Run
python photo_video_organizer.py
```

## Testing

```bash
# Test photo support (HEIC)
python test_heic.py

# Test video support
python test_video_support.py

# Test no-GPS organization
python test_no_gps_organization.py
```

## Configuration

Edit `photo_video_organizer.py`:

```python
SOURCE_DIR = "~/Desktop/Photos"              # Where your files are
OUTPUT_DIR = "~/Desktop/Photos_Organized"    # Where to organize them
COPY_MODE = True                             # True=copy, False=move
CLUSTER_RADIUS_KM = 0.2                      # Grouping distance (200m)
```

## Documentation

- `README.md` - Full documentation
- `QUICK_START.md` - Quick start guide
- `INSTALLATION_CHECKLIST.md` - Setup checklist
- `VIDEO_SUPPORT_SUMMARY.md` - Video feature details
- `FALLBACK_DATE_FEATURE.md` - Date fallback details
- `HEIC_FIX_SUMMARY.md` - HEIC support fix details

## What's Fixed

### Issue: HEIC files not working
**Fixed:** Updated to use `getexif()` instead of `_getexif()`

### Issue: Videos not supported
**Fixed:** Added exiftool integration for video metadata

### Issue: No-GPS files all in one folder
**Fixed:** Now organized by date in separate folders

### Issue: Files without EXIF date
**Fixed:** Falls back to file modification date

## Performance

- ~100K photos: Few minutes
- Video metadata: ~0.05 seconds per file
- Landmark queries: Cached (1 req/sec rate limit)
- No video transcoding: Files copied as-is

## Next Steps

1. Install exiftool: `brew install exiftool`
2. Configure SOURCE_DIR and OUTPUT_DIR
3. Run: `python photo_video_organizer.py`
4. Check output in `~/Desktop/Photos_Organized/`

Enjoy your organized media library! 📸🎥
