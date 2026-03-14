# GitHub Setup Guide

## Step 1: Prepare Your Repository

### Files to Include
✓ Core files:
- `photo_video_organizer.py` - Main script
- `requirements.txt` - Python dependencies
- `README_GITHUB.md` - Main README (rename to README.md)
- `LICENSE` - MIT License
- `.gitignore` - Git ignore rules

✓ Documentation:
- `QUICK_START.md`
- `INSTALLATION_CHECKLIST.md`
- `VIDEO_SUPPORT_SUMMARY.md`
- `FALLBACK_DATE_FEATURE.md`
- `HEIC_FIX_SUMMARY.md`
- `WHATS_NEW.md`

✓ Test scripts:
- `test_heic.py`
- `test_video_support.py`
- `test_no_gps_organization.py`
- `test_all_features.py`
- `test_single_photo.py`
- `test_jpg.py`

✓ Setup scripts:
- `setup_env.sh`

### Files to Exclude (already in .gitignore)
✗ `venv/` - Virtual environment
✗ `*.pyc`, `__pycache__/` - Python cache
✗ Test output files
✗ Sample photos (optional - you can include 1-2 for demo)
✗ `.DS_Store` - macOS files

## Step 2: Initialize Git Repository

```bash
# Navigate to your project directory
cd /path/to/travel_image_classifier

# Rename README for GitHub
mv README_GITHUB.md README.md

# Initialize git repository
git init

# Add all files
git add .

# Create initial commit
git commit -m "Initial commit: Photo & Video Organizer

Features:
- GPS-based organization by location
- Video support (MOV, MP4, etc.)
- Date fallback for files without GPS
- HEIC/HEIF support for iPhone photos
- Smart clustering and landmark detection
- Screenshot detection
- Offline geocoding"

# Check status
git status
```

## Step 3: Create GitHub Repository

### Option A: Using GitHub CLI (gh)

```bash
# Install GitHub CLI if needed
brew install gh  # macOS
# or download from https://cli.github.com/

# Login to GitHub
gh auth login

# Create repository
gh repo create photo-video-organizer --public --source=. --remote=origin --push

# Or for private repository
gh repo create photo-video-organizer --private --source=. --remote=origin --push
```

### Option B: Using GitHub Web Interface

1. Go to https://github.com/new
2. Repository name: `photo-video-organizer`
3. Description: "Automatically organize photos and videos by location and date using GPS metadata"
4. Choose Public or Private
5. Don't initialize with README (we already have one)
6. Click "Create repository"

Then connect your local repo:

```bash
# Add remote
git remote add origin https://github.com/yourusername/photo-video-organizer.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Step 4: Add Repository Details

On GitHub, add:

### Topics/Tags
- `photo-organizer`
- `gps`
- `exif`
- `python`
- `travel`
- `media-organizer`
- `heic`
- `video-organizer`
- `iphone-photos`

### About Section
**Description:** Automatically organize photos and videos by location and date using GPS metadata

**Website:** (optional - your personal site or demo)

## Step 5: Optional Enhancements

### Add a Demo GIF/Screenshot
Create a visual demo showing before/after organization:

```bash
# Add to README.md after the title
![Demo](demo.gif)
```

### Add GitHub Actions (CI/CD)
Create `.github/workflows/test.yml` for automated testing:

```yaml
name: Tests

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python
      uses: actions/setup-python@v2
      with:
        python-version: '3.9'
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    - name: Run tests
      run: |
        python test_all_features.py
```

### Add Badges to README
Add at the top of README.md:

```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![License](https://img.shields.io/badge/license-MIT-green.svg)
![Platform](https://img.shields.io/badge/platform-macOS%20%7C%20Linux%20%7C%20Windows-lightgrey.svg)
```

## Step 6: Sample Photos (Optional)

If you want to include sample photos for testing:

```bash
# Create a samples directory
mkdir samples

# Add 1-2 small sample images (with GPS removed for privacy)
# Update .gitignore to allow samples:
echo "!samples/*.jpg" >> .gitignore
echo "!samples/*.heic" >> .gitignore

git add samples/
git commit -m "Add sample images for testing"
git push
```

## Step 7: Write a Good README

Your README should have:
- ✓ Clear title and description
- ✓ Feature list with emojis
- ✓ Example output structure
- ✓ Quick start guide
- ✓ Installation instructions
- ✓ Usage examples
- ✓ Configuration options
- ✓ Troubleshooting section
- ✓ Contributing guidelines
- ✓ License information

Already done! ✓

## Step 8: Promote Your Project

Share on:
- Reddit: r/python, r/photography, r/travel
- Hacker News
- Twitter/X with hashtags: #python #photography #opensource
- Dev.to or Medium blog post

## Quick Commands Reference

```bash
# Check what will be committed
git status

# Add specific files
git add photo_video_organizer.py README.md

# Commit changes
git commit -m "Your commit message"

# Push to GitHub
git push

# Create a new branch for features
git checkout -b feature-name

# View commit history
git log --oneline

# Tag a release
git tag -a v1.0.0 -m "First release"
git push origin v1.0.0
```

## Versioning

Consider using semantic versioning:
- v1.0.0 - Initial release
- v1.1.0 - Added video support
- v1.2.0 - Added date fallback feature
- v1.2.1 - Bug fixes

## Repository Structure

```
photo-video-organizer/
├── .gitignore
├── LICENSE
├── README.md
├── requirements.txt
├── photo_video_organizer.py
├── setup_env.sh
├── docs/
│   ├── QUICK_START.md
│   ├── INSTALLATION_CHECKLIST.md
│   ├── VIDEO_SUPPORT_SUMMARY.md
│   ├── FALLBACK_DATE_FEATURE.md
│   ├── HEIC_FIX_SUMMARY.md
│   └── WHATS_NEW.md
└── tests/
    ├── test_heic.py
    ├── test_video_support.py
    ├── test_no_gps_organization.py
    ├── test_all_features.py
    ├── test_single_photo.py
    └── test_jpg.py
```

Optional: Organize docs and tests into subdirectories for cleaner structure.

## Done!

Your repository is now ready for GitHub! 🎉

Remember to:
- Keep your README updated
- Respond to issues and PRs
- Tag releases for major updates
- Write good commit messages
- Have fun sharing your work!
