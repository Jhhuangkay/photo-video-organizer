# Installation Checklist

## ✓ Already Done

- [x] Virtual environment created (`venv/`)
- [x] Python packages installed (Pillow, reverse_geocoder, etc.)
- [x] HEIC photo support working
- [x] Code updated to support videos

## ⚠ You Need To Do

### Install exiftool (Required for video support)

```bash
brew install exiftool
```

### Verify installation

```bash
exiftool -ver
```

Expected output: Version number like `12.76`

## Testing Your Setup

### 1. Test Photo Support (HEIC)
```bash
source venv/bin/activate
python test_heic.py
```

Expected: ✓ GPS and date extracted from IMG_3443.HEIC

### 2. Test Video Support
```bash
python test_video_support.py
```

Expected: ✓ exiftool found and working

### 3. Test Full Workflow (Optional)
```bash
# Create a test folder with a few photos/videos
mkdir -p ~/Desktop/Photos_Test
cp IMG_3443.HEIC ~/Desktop/Photos_Test/
# Copy a video if you have one

# Edit photo_video_organizer.py temporarily:
# SOURCE_DIR = "~/Desktop/Photos_Test"
# OUTPUT_DIR = "~/Desktop/Photos_Test_Organized"

# Run organizer
python photo_video_organizer.py
```

## Ready to Use!

Once exiftool is installed, you're ready to organize your photos and videos:

```bash
source venv/bin/activate
python photo_video_organizer.py
```

## Quick Reference

| File | Purpose |
|------|---------|
| `photo_video_organizer.py` | Main script - organize photos & videos |
| `test_heic.py` | Test HEIC photo support |
| `test_video_support.py` | Test video support |
| `requirements.txt` | Python dependencies |
| `README.md` | Full documentation |
| `QUICK_START.md` | Quick start guide |
| `VIDEO_SUPPORT_SUMMARY.md` | What changed for video support |

## Configuration

Edit these in `photo_video_organizer.py`:

```python
SOURCE_DIR = "~/Desktop/Photos"              # Your photos/videos location
OUTPUT_DIR = "~/Desktop/Photos_Organized"    # Where to organize them
COPY_MODE = True                             # True=copy, False=move
CLUSTER_RADIUS_KM = 0.2                      # Grouping distance (200m)
```

## Support

If something doesn't work:

1. Check exiftool is installed: `exiftool -ver`
2. Check Python packages: `pip list | grep -i pillow`
3. Check for errors: Run test scripts above
4. Read the error messages - they usually tell you what's missing!
