#!/usr/bin/env python3
"""
iPhone Photo & Video Organizer (Hybrid Mode)
Auto-classify photos and videos into Continent/Country/City/Date_Landmark structure.

=== Setup ===

1. Make sure Python 3.8+ is installed:
   python3 --version

2. Install required packages:
   pip install Pillow reverse_geocoder pycountry pillow-heif scikit-learn numpy requests

   - Pillow: Read image EXIF metadata
   - reverse_geocoder: Offline reverse geocoding (GPS coords -> country/city)
   - pycountry: Convert country codes to full country names
   - pillow-heif: Enable HEIC/HEIF support (default iPhone photo format)
   - scikit-learn: DBSCAN clustering for grouping nearby photos
   - numpy: Numerical operations for clustering
   - requests: HTTP client for Nominatim landmark lookups

3. Install exiftool for video support:
   brew install exiftool

4. Place photos/videos in the source folder (default ~/Desktop/Photos), or change SOURCE_DIR below.

4. Run:
   python3 photo_organizer.py

5. Output structure example:
   Asia/Japan/Tokyo/2024-03-15_Asakusa/
   Asia/Japan/Tokyo/2024-03-15_Shinjuku/
   Asia/Japan/Tokyo/2024-03-16_Shibuya/
   Uncategorized/Screenshots/
   Uncategorized/No_GPS/2024-01-15/
   Uncategorized/No_GPS/2024-02-20/

6. Default mode is COPY (originals untouched). Set COPY_MODE = False to move instead.

=== Notes ===
- Supports both photos (JPG, HEIC, PNG, etc.) and videos (MOV, MP4, M4V)
- Videos require exiftool to be installed (brew install exiftool)
- Photos/videos without GPS are organized by date in Uncategorized/No_GPS/YYYY-MM-DD/
- If no EXIF date exists, file modification date is used as fallback
- ~100K photos should take a few minutes for classification + file copy
- Nominatim API has a 1 req/sec rate limit; results are cached so duplicate locations are only queried once
- DBSCAN clusters photos within ~200m of each other by default (adjustable via CLUSTER_RADIUS_KM)
- Screenshot detection: filename contains "screenshot", or matches iPhone screen resolution with no camera make
- Duplicate filenames get auto-numbered, no overwrites
- Progress printed every 500 photos
- Supported formats: JPG, JPEG, PNG, HEIC, HEIF, TIFF, BMP, GIF, WEBP, MOV, MP4, M4V, AVI, 3GP
"""

import os
import shutil
import sys
import time
import json
import re
import hashlib
import subprocess
from pathlib import Path
from datetime import datetime

# HEIC/HEIF support (default iPhone photo format)
import pillow_heif
pillow_heif.register_heif_opener()

from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import reverse_geocoder as rg
import pycountry
import numpy as np
from sklearn.cluster import DBSCAN
import requests

# ===== Configuration =====
SOURCE_DIR = os.path.expanduser("~/Desktop/Photos/Afsluitdijk")            # Source photo folder
OUTPUT_DIR = os.path.expanduser("~/Desktop/Photos/Photos_Organized")  # Destination folder
CACHE_FILE = os.path.expanduser("~/Desktop/Photos/Photos_Organized/.nominatim_cache.json")
COPY_MODE = True              # True = copy (keep originals), False = move
CLUSTER_RADIUS_KM = 0.2      # DBSCAN radius in km (~200m) for grouping nearby photos
MIN_CLUSTER_SIZE = 1          # Minimum photos to form a cluster
NOMINATIM_USER_AGENT = "photo-organizer/1.0"  # Required by Nominatim usage policy
SUPPORTED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".heic", ".heif", ".tiff", ".bmp", ".gif", ".webp"}
VIDEO_EXTENSIONS = {".mov", ".mp4", ".m4v", ".avi", ".3gp"}  # Video formats

# Country code -> Continent lookup
COUNTRY_TO_CONTINENT = {}


def _build_continent_map():
    """Build ISO 3166 country code to continent mapping."""
    continent_map = {
        "AF": "Africa", "AX": "Europe", "AL": "Europe", "DZ": "Africa",
        "AS": "Oceania", "AD": "Europe", "AO": "Africa", "AI": "North America",
        "AQ": "Antarctica", "AG": "North America", "AR": "South America",
        "AM": "Asia", "AW": "North America", "AU": "Oceania",
        "AT": "Europe", "AZ": "Asia", "BS": "North America",
        "BH": "Asia", "BD": "Asia", "BB": "North America",
        "BY": "Europe", "BE": "Europe", "BZ": "North America",
        "BJ": "Africa", "BM": "North America", "BT": "Asia",
        "BO": "South America", "BA": "Europe", "BW": "Africa",
        "BR": "South America", "BN": "Asia", "BG": "Europe",
        "BF": "Africa", "BI": "Africa", "KH": "Asia",
        "CM": "Africa", "CA": "North America", "CV": "Africa",
        "KY": "North America", "CF": "Africa", "TD": "Africa",
        "CL": "South America", "CN": "Asia", "CO": "South America",
        "KM": "Africa", "CG": "Africa", "CD": "Africa",
        "CR": "North America", "CI": "Africa", "HR": "Europe",
        "CU": "North America", "CY": "Europe", "CZ": "Europe",
        "DK": "Europe", "DJ": "Africa", "DM": "North America",
        "DO": "North America", "EC": "South America", "EG": "Africa",
        "SV": "North America", "GQ": "Africa", "ER": "Africa",
        "EE": "Europe", "ET": "Africa", "FJ": "Oceania",
        "FI": "Europe", "FR": "Europe", "GA": "Africa",
        "GM": "Africa", "GE": "Asia", "DE": "Europe",
        "GH": "Africa", "GR": "Europe", "GL": "North America",
        "GD": "North America", "GT": "North America", "GN": "Africa",
        "GW": "Africa", "GY": "South America", "HT": "North America",
        "HN": "North America", "HK": "Asia", "HU": "Europe",
        "IS": "Europe", "IN": "Asia", "ID": "Asia",
        "IR": "Asia", "IQ": "Asia", "IE": "Europe",
        "IL": "Asia", "IT": "Europe", "JM": "North America",
        "JP": "Asia", "JO": "Asia", "KZ": "Asia",
        "KE": "Africa", "KI": "Oceania", "KP": "Asia",
        "KR": "Asia", "KW": "Asia", "KG": "Asia",
        "LA": "Asia", "LV": "Europe", "LB": "Asia",
        "LS": "Africa", "LR": "Africa", "LY": "Africa",
        "LI": "Europe", "LT": "Europe", "LU": "Europe",
        "MO": "Asia", "MK": "Europe", "MG": "Africa",
        "MW": "Africa", "MY": "Asia", "MV": "Asia",
        "ML": "Africa", "MT": "Europe", "MH": "Oceania",
        "MR": "Africa", "MU": "Africa", "MX": "North America",
        "FM": "Oceania", "MD": "Europe", "MC": "Europe",
        "MN": "Asia", "ME": "Europe", "MA": "Africa",
        "MZ": "Africa", "MM": "Asia", "NA": "Africa",
        "NR": "Oceania", "NP": "Asia", "NL": "Europe",
        "NZ": "Oceania", "NI": "North America", "NE": "Africa",
        "NG": "Africa", "NO": "Europe", "OM": "Asia",
        "PK": "Asia", "PW": "Oceania", "PS": "Asia",
        "PA": "North America", "PG": "Oceania", "PY": "South America",
        "PE": "South America", "PH": "Asia", "PL": "Europe",
        "PT": "Europe", "PR": "North America", "QA": "Asia",
        "RO": "Europe", "RU": "Europe", "RW": "Africa",
        "SA": "Asia", "SN": "Africa", "RS": "Europe",
        "SC": "Africa", "SL": "Africa", "SG": "Asia",
        "SK": "Europe", "SI": "Europe", "SB": "Oceania",
        "SO": "Africa", "ZA": "Africa", "ES": "Europe",
        "LK": "Asia", "SD": "Africa", "SR": "South America",
        "SZ": "Africa", "SE": "Europe", "CH": "Europe",
        "SY": "Asia", "TW": "Asia", "TJ": "Asia",
        "TZ": "Africa", "TH": "Asia", "TL": "Asia",
        "TG": "Africa", "TO": "Oceania", "TT": "North America",
        "TN": "Africa", "TR": "Asia", "TM": "Asia",
        "TV": "Oceania", "UG": "Africa", "UA": "Europe",
        "AE": "Asia", "GB": "Europe", "US": "North America",
        "UY": "South America", "UZ": "Asia", "VU": "Oceania",
        "VE": "South America", "VN": "Asia", "WS": "Oceania",
        "YE": "Asia", "ZM": "Africa", "ZW": "Africa",
    }
    COUNTRY_TO_CONTINENT.update(continent_map)

_build_continent_map()


# ===== Nominatim Cache =====

_nominatim_cache = {}


def _load_cache():
    """Load Nominatim query cache from disk."""
    global _nominatim_cache
    try:
        if os.path.exists(CACHE_FILE):
            with open(CACHE_FILE, "r", encoding="utf-8") as f:
                _nominatim_cache = json.load(f)
            print(f"  Loaded {len(_nominatim_cache)} cached landmark lookups.")
    except Exception:
        _nominatim_cache = {}


def _save_cache():
    """Persist Nominatim query cache to disk."""
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w", encoding="utf-8") as f:
            json.dump(_nominatim_cache, f, ensure_ascii=False)
    except Exception:
        pass


def _cache_key(lat, lon):
    """Generate a cache key by rounding coords to ~11m precision (4 decimal places)."""
    return f"{lat:.4f},{lon:.4f}"


def query_landmark(lat, lon):
    """
    Query Nominatim for a human-readable landmark/place name.
    Returns a short name like 'Eiffel Tower', 'Shinjuku Station', or a neighborhood name.
    Results are cached to minimize API calls.
    """
    key = _cache_key(lat, lon)
    if key in _nominatim_cache:
        return _nominatim_cache[key]

    try:
        url = "https://nominatim.openstreetmap.org/reverse"
        params = {
            "lat": lat,
            "lon": lon,
            "format": "jsonv2",
            "zoom": 18,  # High zoom = more specific (building/POI level)
            "accept-language": "en",
        }
        headers = {"User-Agent": NOMINATIM_USER_AGENT}
        resp = requests.get(url, params=params, headers=headers, timeout=10)
        resp.raise_for_status()
        data = resp.json()

        name = _extract_landmark_name(data)
        _nominatim_cache[key] = name
        time.sleep(1.1)  # Respect Nominatim rate limit (1 req/sec)
        return name

    except Exception:
        _nominatim_cache[key] = None
        return None


def _extract_landmark_name(data):
    """
    Extract the most useful short name from Nominatim response.
    Priority: tourism/attraction name > building name > neighbourhood > suburb > road.
    """
    # The 'name' field often has the POI/landmark name
    name = data.get("name")
    if name and name != data.get("display_name"):
        return _sanitize_folder_name(name)

    # Fall back to address components
    addr = data.get("address", {})
    for field in ["tourism", "attraction", "building", "amenity", "shop",
                  "neighbourhood", "suburb", "quarter", "hamlet"]:
        val = addr.get(field)
        if val:
            return _sanitize_folder_name(val)

    # Last resort: road name
    road = addr.get("road")
    if road:
        return _sanitize_folder_name(road)

    return None


def _sanitize_folder_name(name):
    """Remove or replace characters that are invalid in folder names."""
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*]', "-", name)
    name = re.sub(r'\s+', " ", name)
    # Truncate very long names
    if len(name) > 60:
        name = name[:60].rstrip()
    return name


# ===== EXIF Helpers =====

def get_exif_data(filepath):
    """
    Extract GPS coords and date from photo EXIF.
    Returns dict with keys: 'gps' (lat, lon) or None, 'date' (YYYY-MM-DD str) or None.
    """
    result = {"gps": None, "date": None}
    try:
        img = Image.open(filepath)
        # Use getexif() for compatibility with HEIC and newer Pillow versions
        exif_data = img.getexif() if hasattr(img, 'getexif') else img._getexif()
        if not exif_data:
            return result

        gps_info = {}
        for tag_id, value in exif_data.items():
            tag = TAGS.get(tag_id, tag_id)
            if tag == "GPSInfo":
                # Handle both dict and IFD (Image File Directory) types
                if hasattr(value, 'items'):
                    for gps_tag_id, gps_value in value.items():
                        gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                        gps_info[gps_tag] = gps_value
                else:
                    # For getexif(), GPSInfo is an IFD tag ID, need to get it separately
                    gps_ifd = exif_data.get_ifd(tag_id)
                    for gps_tag_id, gps_value in gps_ifd.items():
                        gps_tag = GPSTAGS.get(gps_tag_id, gps_tag_id)
                        gps_info[gps_tag] = gps_value
            elif tag == "DateTimeOriginal" or tag == "DateTime":
                if result["date"] is None:
                    try:
                        dt = datetime.strptime(str(value), "%Y:%m:%d %H:%M:%S")
                        result["date"] = dt.strftime("%Y-%m-%d")
                    except (ValueError, TypeError):
                        pass

        # Parse GPS
        if gps_info:
            lat = gps_info.get("GPSLatitude")
            lat_ref = gps_info.get("GPSLatitudeRef")
            lon = gps_info.get("GPSLongitude")
            lon_ref = gps_info.get("GPSLongitudeRef")

            if all([lat, lat_ref, lon, lon_ref]):
                def to_decimal(dms):
                    d, m, s = [float(x) for x in dms]
                    return d + m / 60.0 + s / 3600.0

                lat_dec = to_decimal(lat)
                lon_dec = to_decimal(lon)
                if lat_ref == "S":
                    lat_dec = -lat_dec
                if lon_ref == "W":
                    lon_dec = -lon_dec
                result["gps"] = (lat_dec, lon_dec)

    except Exception:
        pass
    return result


def get_video_metadata(filepath):
    """
    Extract GPS coords and date from video using exiftool.
    Returns dict with keys: 'gps' (lat, lon) or None, 'date' (YYYY-MM-DD str) or None.
    """
    result = {"gps": None, "date": None}
    try:
        # Run exiftool to get GPS and date metadata
        cmd = [
            'exiftool',
            '-GPSLatitude',
            '-GPSLongitude',
            '-GPSLatitudeRef',
            '-GPSLongitudeRef',
            '-CreateDate',
            '-CreationDate',
            '-MediaCreateDate',
            '-DateTimeOriginal',
            '-json',
            str(filepath)
        ]

        proc = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if proc.returncode != 0:
            return result

        data = json.loads(proc.stdout)[0]

        # Extract GPS coordinates
        lat_str = data.get('GPSLatitude')
        lon_str = data.get('GPSLongitude')
        lat_ref = data.get('GPSLatitudeRef', 'N')
        lon_ref = data.get('GPSLongitudeRef', 'E')

        if lat_str and lon_str:
            # Parse coordinates (format: "52 deg 4' 36.50\" N" or decimal)
            def parse_coord(coord_str):
                # Try decimal format first
                try:
                    return float(coord_str)
                except (ValueError, TypeError):
                    pass

                # Parse DMS format: "52 deg 4' 36.50\" N"
                import re
                match = re.match(r"(\d+)\s*deg\s*(\d+)'\s*([\d.]+)\"", str(coord_str))
                if match:
                    d, m, s = match.groups()
                    return float(d) + float(m) / 60.0 + float(s) / 3600.0
                return None

            lat = parse_coord(lat_str)
            lon = parse_coord(lon_str)

            if lat is not None and lon is not None:
                if lat_ref == 'S':
                    lat = -lat
                if lon_ref == 'W':
                    lon = -lon
                result["gps"] = (lat, lon)

        # Extract date (try multiple fields)
        for date_field in ['CreateDate', 'CreationDate', 'MediaCreateDate', 'DateTimeOriginal']:
            date_str = data.get(date_field)
            if date_str:
                try:
                    # Handle various date formats
                    for fmt in ["%Y:%m:%d %H:%M:%S", "%Y-%m-%d %H:%M:%S", "%Y:%m:%d", "%Y-%m-%d"]:
                        try:
                            dt = datetime.strptime(date_str.split('.')[0].split('+')[0].strip(), fmt)
                            result["date"] = dt.strftime("%Y-%m-%d")
                            break
                        except ValueError:
                            continue
                    if result["date"]:
                        break
                except Exception:
                    continue

    except (subprocess.TimeoutExpired, subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        pass

    return result


def get_metadata(filepath):
    """
    Universal metadata extractor for both photos and videos.
    Returns dict with keys: 'gps' (lat, lon) or None, 'date' (YYYY-MM-DD str) or None.
    Falls back to file modification date if no EXIF/metadata date is found.
    """
    ext = Path(filepath).suffix.lower()
    if ext in VIDEO_EXTENSIONS:
        result = get_video_metadata(filepath)
    else:
        result = get_exif_data(filepath)

    # Fallback: Use file modification date if no date in metadata
    if result["date"] is None:
        try:
            file_path = Path(filepath)
            mtime = file_path.stat().st_mtime
            result["date"] = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d")
        except Exception:
            result["date"] = "Unknown_Date"

    return result




def is_screenshot(filepath):
    """Detect if a file is a screenshot based on filename keywords or iPhone screen resolution + no camera make."""
    name = Path(filepath).stem.lower()
    if "screenshot" in name or "螢幕快照" in name or "截圖" in name:
        return True
    try:
        img = Image.open(filepath)
        w, h = img.size
        screenshot_sizes = {
            (1170, 2532), (2532, 1170),
            (1179, 2556), (2556, 1179),
            (1290, 2796), (2796, 1290),
            (1125, 2436), (2436, 1125),
            (1242, 2688), (2688, 1242),
            (828, 1792), (1792, 828),
            (750, 1334), (1334, 750),
            (1080, 1920), (1920, 1080),
            (640, 1136), (1136, 640),
            (1284, 2778), (2778, 1284),
        }
        if (w, h) in screenshot_sizes:
            exif = img.getexif() if hasattr(img, 'getexif') else img._getexif()
            if exif:
                make = None
                for tag_id, value in exif.items():
                    if TAGS.get(tag_id) == "Make":
                        make = value
                        break
                if make is None:
                    return True
    except Exception:
        pass
    return False


def get_country_name(cc):
    """Convert country code to full country name using pycountry."""
    try:
        country = pycountry.countries.get(alpha_2=cc)
        if country:
            return country.name
    except Exception:
        pass
    return cc


# ===== Clustering =====

def cluster_photos_by_location(photo_entries):
    """
    Group photos by GPS proximity using DBSCAN.
    Input: list of dicts with 'gps' key as (lat, lon).
    Returns: list of cluster labels (int), where -1 = noise/singleton assigned to nearest cluster.
    """
    coords = np.array([p["gps"] for p in photo_entries])

    # Convert km radius to approximate degrees for DBSCAN eps
    # 1 degree latitude ~ 111 km
    eps_deg = CLUSTER_RADIUS_KM / 111.0

    clustering = DBSCAN(eps=eps_deg, min_samples=MIN_CLUSTER_SIZE, metric="euclidean").fit(coords)
    labels = clustering.labels_

    # Assign noise points (-1) to the nearest cluster
    if len(set(labels)) > 1 or -1 in labels:
        cluster_centers = {}
        for label in set(labels):
            if label == -1:
                continue
            mask = labels == label
            cluster_centers[label] = coords[mask].mean(axis=0)

        if cluster_centers:
            for i, label in enumerate(labels):
                if label == -1:
                    # Find nearest cluster center
                    min_dist = float("inf")
                    nearest = 0
                    for cl, center in cluster_centers.items():
                        dist = np.linalg.norm(coords[i] - center)
                        if dist < min_dist:
                            min_dist = dist
                            nearest = cl
                    labels[i] = nearest

    return labels.tolist()


def get_cluster_landmark(photo_entries, labels):
    """
    For each cluster, query Nominatim using the cluster centroid to get a landmark name.
    Returns dict: cluster_label -> landmark_name (str or None).
    """
    coords = np.array([p["gps"] for p in photo_entries])
    cluster_names = {}

    unique_labels = sorted(set(labels))
    total_clusters = len(unique_labels)
    print(f"  Querying landmarks for {total_clusters} location clusters...")

    for idx, label in enumerate(unique_labels):
        mask = np.array(labels) == label
        centroid = coords[mask].mean(axis=0)
        lat, lon = centroid[0], centroid[1]

        name = query_landmark(lat, lon)
        cluster_names[label] = name

        if (idx + 1) % 20 == 0:
            print(f"    Landmark progress: {idx + 1}/{total_clusters}")

    return cluster_names


# ===== Main Organizer =====

def organize_photos():
    """Main entry point: scan, classify, cluster, and organize all photos."""
    source = Path(SOURCE_DIR)
    output = Path(OUTPUT_DIR)

    if not source.exists():
        print(f"Error: Source folder not found: {SOURCE_DIR}")
        print(f"  Please verify the path or update SOURCE_DIR in this script.")
        sys.exit(1)

    _load_cache()

    # Phase 1: Scan all photos and extract EXIF data
    print("Phase 1: Scanning photos and reading EXIF data...\n")
    all_photos = []
    no_gps_photos = []
    screenshot_photos = []

    photo_files = [f for f in source.rglob("*")
                   if f.is_file() and f.suffix.lower() in (SUPPORTED_EXTENSIONS | VIDEO_EXTENSIONS)]
    total = len(photo_files)
    print(f"  Found {total} photos and videos.\n")

    for i, photo in enumerate(photo_files, 1):
        metadata = get_metadata(str(photo))

        if metadata["gps"]:
            all_photos.append({
                "path": photo,
                "gps": metadata["gps"],
                "date": metadata["date"] or "Unknown_Date",
            })
        elif is_screenshot(str(photo)):
            screenshot_photos.append(photo)
        else:
            # Store no-GPS photos with their date for organization
            no_gps_photos.append({
                "path": photo,
                "date": metadata["date"] or "Unknown_Date",
            })

        if i % 2000 == 0 or i == total:
            print(f"  Scanned: {i}/{total} ({i*100//total}%)")

    print(f"\n  GPS located (photos/videos): {len(all_photos)}")
    print(f"  Screenshots: {len(screenshot_photos)}")
    print(f"  No GPS: {len(no_gps_photos)}\n")

    # Phase 2: Reverse geocode to get country/city for each photo
    print("Phase 2: Reverse geocoding (offline)...")
    if all_photos:
        gps_list = [p["gps"] for p in all_photos]
        geo_results = rg.search(gps_list)
        for p, geo in zip(all_photos, geo_results):
            cc = geo.get("cc", "Unknown")
            city = geo.get("name", "Unknown")
            p["country_code"] = cc
            p["country"] = _sanitize_folder_name(get_country_name(cc))
            p["city"] = _sanitize_folder_name(city)
            p["continent"] = COUNTRY_TO_CONTINENT.get(cc, "Other")
    print("  Done.\n")

    # Phase 3: Group by city+date, then cluster within each group
    print("Phase 3: Clustering by location within each city+date group...")
    from collections import defaultdict
    city_date_groups = defaultdict(list)
    for p in all_photos:
        key = (p["continent"], p["country"], p["city"], p["date"])
        city_date_groups[key].append(p)

    # For each group, run DBSCAN clustering and query landmarks
    total_landmark_queries = 0
    for key, photos in city_date_groups.items():
        continent, country, city, date = key

        if len(photos) == 1:
            # Single photo: query landmark directly
            lat, lon = photos[0]["gps"]
            name = query_landmark(lat, lon)
            total_landmark_queries += 1
            folder_suffix = name if name else "spot"
            photos[0]["subfolder"] = os.path.join(continent, country, city, f"{date}_{folder_suffix}")
        else:
            # Multiple photos: cluster then name each cluster
            labels = cluster_photos_by_location(photos)
            cluster_names = get_cluster_landmark(photos, labels)
            total_landmark_queries += len(set(labels))

            # Count photos per cluster to create unique folder names
            cluster_count = defaultdict(int)
            for label in labels:
                cluster_count[label] += 1

            # Assign subfolder to each photo
            label_folder_map = {}
            seen_names = defaultdict(int)
            for label in sorted(set(labels)):
                name = cluster_names.get(label)
                folder_name = name if name else f"spot_{label + 1}"
                # Handle duplicate landmark names within same city+date
                seen_names[folder_name] += 1
                if seen_names[folder_name] > 1:
                    folder_name = f"{folder_name}_{seen_names[folder_name]}"
                label_folder_map[label] = os.path.join(
                    continent, country, city, f"{date}_{folder_name}"
                )

            for p, label in zip(photos, labels):
                p["subfolder"] = label_folder_map[label]

    print(f"  Processed {len(city_date_groups)} city+date groups.")
    print(f"  Total landmark queries: {total_landmark_queries}\n")

    # Save cache after all landmark queries
    _save_cache()

    # Phase 4: Copy/move files
    print("Phase 4: Organizing files...\n")
    stats = {"gps": 0, "screenshot": 0, "no_gps": 0, "error": 0}

    def copy_or_move(src, dest_dir_path, stats_key):
        dest_dir_path.mkdir(parents=True, exist_ok=True)
        dest_file = dest_dir_path / src.name
        if dest_file.exists():
            stem, suffix = src.stem, src.suffix
            counter = 1
            while dest_file.exists():
                dest_file = dest_dir_path / f"{stem}_{counter}{suffix}"
                counter += 1
        try:
            if COPY_MODE:
                shutil.copy2(str(src), str(dest_file))
            else:
                shutil.move(str(src), str(dest_file))
            stats[stats_key] += 1
        except Exception as e:
            stats["error"] += 1
            print(f"  Warning: Failed to process {src.name} - {e}")

    # GPS photos
    for i, p in enumerate(all_photos, 1):
        dest_dir = output / p["subfolder"]
        copy_or_move(p["path"], dest_dir, "gps")
        if i % 500 == 0 or i == len(all_photos):
            print(f"  Processing: {i}/{len(all_photos)} ({i*100//len(all_photos)}%)")

    # Screenshots
    for s in screenshot_photos:
        copy_or_move(s, output / "Uncategorized" / "Screenshots", "screenshot")

    # No GPS - organize by date
    for item in no_gps_photos:
        date_folder = item["date"]
        dest_dir = output / "Uncategorized" / "No_GPS" / date_folder
        copy_or_move(item["path"], dest_dir, "no_gps")

    print(f"\nDone!")
    print(f"  GPS located:  {stats['gps']}")
    print(f"  Screenshots:  {stats['screenshot']}")
    print(f"  No GPS data:  {stats['no_gps']}")
    print(f"  Errors:       {stats['error']}")
    print(f"\n  Output: {OUTPUT_DIR}")


if __name__ == "__main__":
    organize_photos()
