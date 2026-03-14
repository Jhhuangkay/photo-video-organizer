#!/usr/bin/env python3
"""Test if all required packages are installed."""

import sys

packages = [
    "PIL",
    "reverse_geocoder",
    "pycountry",
    "pillow_heif",
    "sklearn",
    "numpy",
    "requests"
]

print("Testing package imports...")
print("-" * 40)

missing = []
for pkg in packages:
    try:
        __import__(pkg)
        print(f"✓ {pkg}")
    except ImportError:
        print(f"✗ {pkg} - NOT INSTALLED")
        missing.append(pkg)

print("-" * 40)
if missing:
    print(f"\nMissing packages: {', '.join(missing)}")
    print("\nInstall with:")
    print("  source venv/bin/activate")
    print("  pip install -r requirements.txt")
    sys.exit(1)
else:
    print("\n✓ All packages installed successfully!")
    print("\nYou can now run:")
    print("  python photo_organizer.py")
