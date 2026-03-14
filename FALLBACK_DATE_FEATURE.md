# Fallback Date Feature

## What's New

The script now handles photos/videos without GPS data much better!

## The Problem

Some photos have no GPS data:
- Downloaded from social media (metadata stripped)
- Edited/processed by apps
- Screenshots
- Photos taken with GPS disabled

Previously, these all went into a single `Uncategorized/No_GPS/` folder with no organization.

## The Solution

Now files without GPS are organized by date:

```
Uncategorized/
└── No_GPS/
    ├── 2024-01-15/
    │   ├── downloaded_photo1.jpg
    │   └── downloaded_photo2.jpg
    ├── 2024-02-20/
    │   └── screenshot.png
    └── 2024-03-13/
        └── S__59686947.jpg
```

## How It Works

### Date Extraction Priority

1. **EXIF Date** (preferred)
   - DateTimeOriginal
   - DateTime
   - CreateDate (for videos)

2. **File Modification Date** (fallback)
   - If no EXIF date exists, uses when the file was last modified
   - Better than nothing for organization

3. **Unknown_Date** (last resort)
   - Only if file date extraction fails completely

## Examples

### Example 1: Social Media Download
```
File: IMG_from_instagram.jpg
EXIF Date: None
File Modified: 2024-03-10
→ Organized to: Uncategorized/No_GPS/2024-03-10/
```

### Example 2: Screenshot
```
File: Screenshot_2024-03-13.png
EXIF Date: None
File Modified: 2024-03-13
→ Organized to: Uncategorized/Screenshots/
(Screenshots have their own folder)
```

### Example 3: Edited Photo
```
File: edited_vacation.jpg
EXIF Date: 2023-07-15 (preserved from original)
GPS: None (stripped during editing)
→ Organized to: Uncategorized/No_GPS/2023-07-15/
```

## Benefits

✓ Chronological organization even without GPS
✓ Easy to find photos by date
✓ Better than dumping everything in one folder
✓ Automatic fallback - no configuration needed

## Testing

Test with your file:
```bash
python test_no_gps_organization.py
```

## Output Structure

Complete example:
```
Photos_Organized/
├── Europe/
│   └── Netherlands/
│       └── Amsterdam/
│           └── 2021-11-24_Dam_Square/
│               ├── IMG_3443.HEIC (has GPS)
│               └── IMG_3444.MOV (has GPS)
├── Asia/
│   └── Japan/
│       └── Tokyo/
│           └── 2024-03-15_Shibuya/
│               └── IMG_5001.HEIC (has GPS)
└── Uncategorized/
    ├── Screenshots/
    │   └── Screenshot_2024-03-13.png
    └── No_GPS/
        ├── 2024-01-15/
        │   └── downloaded_photo.jpg (no GPS, has EXIF date)
        ├── 2024-02-20/
        │   └── edited_photo.jpg (no GPS, has EXIF date)
        └── 2024-03-13/
            └── S__59686947.jpg (no GPS, no EXIF, uses file date)
```

## Notes

- File modification date can change if you copy/move files
- For best results, preserve original file dates when transferring photos
- EXIF dates are always preferred when available
- This feature works for both photos and videos
