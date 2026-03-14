#!/usr/bin/env python3
"""
Travel Post Generator
Automatically generates social media posts from organized photos/videos.
Creates posts offline for manual review before posting.
"""

import os
import json
import random
from pathlib import Path
from datetime import datetime, timedelta
from collections import defaultdict

# ===== Configuration =====
ORGANIZED_PHOTOS_DIR = os.path.expanduser("~/Desktop/Photos/Photos_Organized")
OUTPUT_DIR = os.path.expanduser("~/Desktop/Photos/Travel_Posts")
POSTS_PER_DAY = 1
START_DATE = datetime.now()  # When to start posting schedule

# ===== Travel Content Templates =====

# Professional, engaging captions (longer versions)
CAPTION_TEMPLATES = {
    "en": [
        "Exploring the beautiful {landmark} in {city}, {country}. This place truly captures the essence of the city with its stunning architecture and vibrant atmosphere. Every corner tells a story, and I'm grateful to experience it firsthand. {emoji}",
        
        "A memorable day at {landmark} in {city}! The energy here is incredible, and the views are absolutely breathtaking. It's moments like these that remind me why I love traveling and discovering new places. {emoji}",
        
        "Discovering the beauty of {landmark} in {city}, {country}. Walking through this iconic location, I'm amazed by the rich history and culture that surrounds every detail. Definitely a highlight of my journey! {emoji}",
        
        "{city}'s iconic {landmark} never disappoints. From the stunning scenery to the warm local atmosphere, this place has left a lasting impression on me. Can't wait to come back and explore more! {emoji}",
        
        "Wandering through {landmark} in beautiful {city}. There's something magical about this place – the perfect blend of history, culture, and natural beauty. Every moment here feels like a scene from a postcard. {emoji}",
        
        "Captured this unforgettable moment at {landmark}, {city}. The atmosphere here is simply enchanting, and I'm so glad I had the chance to experience it. These are the memories that make traveling so special. {emoji}",
        
        "The stunning {landmark} in {city}, {country}. Standing here, I'm reminded of how diverse and beautiful our world is. This location offers a perfect mix of culture, history, and breathtaking views. {emoji}",
        
        "Another amazing day exploring {landmark} in {city}! The local charm and incredible scenery make this place truly special. Feeling grateful for these travel experiences and the memories they create. {emoji}",
        
        "Lost in the beauty of {landmark}, {city}. This place exceeded all my expectations with its stunning views and rich cultural heritage. It's destinations like this that fuel my passion for travel and exploration. {emoji}",
        
        "Soaking in the atmosphere at {landmark} in {city}, {country}. The combination of historical significance and natural beauty here is simply remarkable. Every visit reveals something new and fascinating. {emoji}",
    ],
    "zh": [
        "探索{country}{city}美麗的{landmark}。這個地方以其令人驚嘆的建築和充滿活力的氛圍真正捕捉了城市的精髓。每個角落都訴說著一個故事，我很感激能親身體驗。{emoji}",
        
        "在{city}的{landmark}度過難忘的一天！這裡的能量令人難以置信，景色絕對令人嘆為觀止。正是這樣的時刻提醒我為什麼熱愛旅行和發現新地方。{emoji}",
        
        "發現{country}{city}{landmark}的美麗。漫步在這個標誌性的地方，我對每個細節所蘊含的豐富歷史和文化感到驚嘆。絕對是我旅程的亮點！{emoji}",
        
        "{city}標誌性的{landmark}從不讓人失望。從令人驚嘆的風景到溫暖的當地氛圍，這個地方給我留下了深刻的印象。迫不及待想再次回來探索更多！{emoji}",
        
        "漫步在美麗的{city}{landmark}。這個地方有一種神奇的魔力——歷史、文化和自然美景的完美融合。這裡的每一刻都像明信片上的場景。{emoji}",
        
        "在{city}的{landmark}捕捉到這個難忘的時刻。這裡的氛圍簡直令人著迷，我很高興有機會體驗它。這些是讓旅行如此特別的回憶。{emoji}",
        
        "{country}{city}令人驚嘆的{landmark}。站在這裡，我想起了我們的世界是多麼多樣和美麗。這個地方完美融合了文化、歷史和令人嘆為觀止的景色。{emoji}",
        
        "又一個探索{city}{landmark}的美好日子！當地的魅力和令人難以置信的風景使這個地方真正特別。感激這些旅行經歷和它們創造的回憶。{emoji}",
        
        "沉醉在{city}{landmark}的美景中。這個地方以其令人驚嘆的景色和豐富的文化遺產超出了我所有的期望。正是這樣的目的地激發了我對旅行和探索的熱情。{emoji}",
        
        "沉浸在{country}{city}{landmark}的氛圍中。這裡歷史意義和自然美景的結合簡直令人矚目。每次訪問都會發現新的和迷人的東西。{emoji}",
    ]
}

# Emojis by continent
CONTINENT_EMOJIS = {
    "Europe": ["🇪🇺", "✨", "🏰", "🌍"],
    "Asia": ["🌏", "🎎", "🏯", "✨"],
    "North America": ["🌎", "🗽", "🌟", "✨"],
    "South America": ["🌎", "🌴", "🎉", "✨"],
    "Africa": ["🌍", "🦁", "🌅", "✨"],
    "Oceania": ["🌏", "🏖️", "🌊", "✨"],
    "Antarctica": ["🐧", "❄️", "🌨️", "✨"],
}

# Hashtags by location
def generate_hashtags(continent, country, city, landmark):
    """Generate relevant hashtags for the location."""
    tags = []
    
    # City and country
    tags.append(f"#{city.replace(' ', '').replace('-', '')}")
    tags.append(f"#{country.replace(' ', '').replace('-', '')}")
    
    # Generic travel tags
    tags.extend(["#Travel", "#TravelPhotography", "#Wanderlust", "#Explore"])
    
    # Continent-specific
    if continent == "Europe":
        tags.append("#EuropeTravel")
    elif continent == "Asia":
        tags.append("#AsiaTravel")
    elif continent == "North America":
        tags.append("#NorthAmerica")
    
    # Landmark if available
    if landmark and landmark != "spot":
        clean_landmark = landmark.replace('_', '').replace('-', '')
        if len(clean_landmark) < 30:  # Reasonable hashtag length
            tags.append(f"#{clean_landmark}")
    
    return tags[:8]  # Limit to 8 hashtags


def generate_caption(location_info, language="en"):
    """Generate a professional, concise caption."""
    template = random.choice(CAPTION_TEMPLATES[language])
    emoji = random.choice(CONTINENT_EMOJIS.get(location_info["continent"], ["✨"]))
    
    caption = template.format(
        landmark=location_info["landmark"],
        city=location_info["city"],
        country=location_info["country"],
        emoji=emoji
    )
    
    return caption


def scan_organized_photos(base_dir):
    """
    Scan organized photo directory and extract location information.
    Returns list of locations with their photos/videos.
    """
    locations = []
    base_path = Path(base_dir)
    
    if not base_path.exists():
        print(f"Error: Directory not found: {base_dir}")
        return locations
    
    # Scan structure: Continent/Country/City/Date_Landmark/
    for continent_dir in base_path.iterdir():
        if not continent_dir.is_dir() or continent_dir.name == "Uncategorized":
            continue
        
        continent = continent_dir.name
        
        for country_dir in continent_dir.iterdir():
            if not country_dir.is_dir():
                continue
            
            country = country_dir.name
            
            for city_dir in country_dir.iterdir():
                if not city_dir.is_dir():
                    continue
                
                city = city_dir.name
                
                for location_dir in city_dir.iterdir():
                    if not location_dir.is_dir():
                        continue
                    
                    # Parse date and landmark from folder name: "2021-11-24_Dam_Square"
                    folder_name = location_dir.name
                    parts = folder_name.split('_', 1)
                    
                    if len(parts) == 2:
                        date_str, landmark = parts
                        landmark = landmark.replace('_', ' ')
                    else:
                        date_str = parts[0]
                        landmark = city  # Fallback to city name
                    
                    # Get all media files
                    media_files = []
                    for ext in ['.jpg', '.jpeg', '.png', '.heic', '.heif', '.mov', '.mp4', '.m4v']:
                        media_files.extend(list(location_dir.glob(f'*{ext}')))
                        media_files.extend(list(location_dir.glob(f'*{ext.upper()}')))
                    
                    if media_files:
                        locations.append({
                            "continent": continent,
                            "country": country,
                            "city": city,
                            "landmark": landmark,
                            "date": date_str,
                            "folder": str(location_dir),
                            "media_files": [str(f) for f in media_files],
                            "media_count": len(media_files)
                        })
    
    return locations


def select_best_media(media_files, max_count=5):
    """
    Select best media files for posting.
    Prioritizes photos over videos, spreads selection across the set.
    """
    # Separate photos and videos
    photos = [f for f in media_files if not any(f.lower().endswith(ext) for ext in ['.mov', '.mp4', '.m4v'])]
    videos = [f for f in media_files if any(f.lower().endswith(ext) for ext in ['.mov', '.mp4', '.m4v'])]
    
    selected = []
    
    # Select photos first (up to 4)
    if photos:
        photo_count = min(4, len(photos), max_count)
        # Spread selection across the set
        step = len(photos) // photo_count if photo_count > 0 else 1
        selected.extend([photos[i * step] for i in range(photo_count)])
    
    # Add one video if available and space permits
    if videos and len(selected) < max_count:
        selected.append(videos[0])
    
    return selected[:max_count]


def generate_posts(locations, start_date, posts_per_day=1):
    """
    Generate post schedule from locations.
    Returns list of posts with scheduling information.
    """
    posts = []
    current_date = start_date
    
    # Sort locations by date
    locations_sorted = sorted(locations, key=lambda x: x["date"])
    
    for idx, location in enumerate(locations_sorted):
        # Select media for this post
        selected_media = select_best_media(location["media_files"])
        
        # Generate captions in both languages
        caption_en = generate_caption(location, "en")
        caption_zh = generate_caption(location, "zh")
        
        # Generate hashtags
        hashtags = generate_hashtags(
            location["continent"],
            location["country"],
            location["city"],
            location["landmark"]
        )
        
        # Create post
        post = {
            "post_id": f"{location['date']}_{location['city'].replace(' ', '_').lower()}_{idx}",
            "scheduled_date": current_date.strftime("%Y-%m-%d"),
            "scheduled_time": "10:00:00",  # Default posting time
            "location": {
                "continent": location["continent"],
                "country": location["country"],
                "city": location["city"],
                "landmark": location["landmark"],
                "original_date": location["date"]
            },
            "caption": {
                "en": caption_en,
                "zh": caption_zh,
                "combined": f"{caption_en}\n\n{caption_zh}"
            },
            "hashtags": hashtags,
            "media": selected_media,
            "media_count": len(selected_media),
            "status": "pending_review",
            "platforms": ["facebook", "instagram"],
            "folder": location["folder"]
        }
        
        posts.append(post)
        
        # Increment date for next post
        current_date += timedelta(days=1 / posts_per_day)
    
    return posts


def save_posts(posts, output_dir):
    """Save generated posts to JSON files for review."""
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Save individual post files
    posts_dir = output_path / "posts"
    posts_dir.mkdir(exist_ok=True)
    
    for post in posts:
        post_file = posts_dir / f"{post['post_id']}.json"
        with open(post_file, 'w', encoding='utf-8') as f:
            json.dump(post, f, ensure_ascii=False, indent=2)
    
    # Save master schedule
    schedule_file = output_path / "posting_schedule.json"
    with open(schedule_file, 'w', encoding='utf-8') as f:
        json.dump(posts, f, ensure_ascii=False, indent=2)
    
    # Create summary
    summary = {
        "total_posts": len(posts),
        "date_range": {
            "start": posts[0]["scheduled_date"] if posts else None,
            "end": posts[-1]["scheduled_date"] if posts else None
        },
        "locations": len(set(p["location"]["city"] for p in posts)),
        "countries": len(set(p["location"]["country"] for p in posts)),
        "total_media": sum(p["media_count"] for p in posts),
        "generated_at": datetime.now().isoformat()
    }
    
    summary_file = output_path / "summary.json"
    with open(summary_file, 'w', encoding='utf-8') as f:
        json.dump(summary, f, ensure_ascii=False, indent=2)
    
    return summary


def create_preview_html(posts, output_dir):
    """Create HTML preview of all posts for easy review."""
    output_path = Path(output_dir)
    
    # Calculate summary
    summary = {
        "total_posts": len(posts),
        "start_date": posts[0]["scheduled_date"] if posts else "N/A",
        "end_date": posts[-1]["scheduled_date"] if posts else "N/A",
        "locations": len(set(p["location"]["city"] for p in posts)),
        "countries": len(set(p["location"]["country"] for p in posts))
    }
    
    # Build HTML with summary values directly (avoid .format() conflicts with CSS)
    html = f"""<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Travel Posts Preview</title>
    <style>
        body {{ font-family: Arial, sans-serif; max-width: 900px; margin: 0 auto; padding: 20px; background: #f5f5f5; }}
        .post {{ background: white; margin: 20px 0; padding: 20px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
        .post-header {{ border-bottom: 2px solid #eee; padding-bottom: 10px; margin-bottom: 15px; }}
        .post-id {{ color: #666; font-size: 0.9em; }}
        .schedule {{ color: #1877f2; font-weight: bold; }}
        .location {{ color: #333; font-size: 1.1em; margin: 10px 0; }}
        .caption {{ margin: 15px 0; line-height: 1.6; white-space: pre-wrap; }}
        .hashtags {{ color: #1877f2; margin: 10px 0; }}
        .media-gallery {{ margin: 15px 0; }}
        .media-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 10px; }}
        .media-item {{ position: relative; border-radius: 8px; overflow: hidden; background: #f0f0f0; aspect-ratio: 4/3; }}
        .media-item img {{ width: 100%; height: 100%; object-fit: cover; display: block; }}
        .media-item video {{ width: 100%; height: 100%; object-fit: cover; display: block; background: #000; }}
        .media-label {{ position: absolute; bottom: 0; left: 0; right: 0; background: rgba(0,0,0,0.7); color: white; padding: 5px 8px; font-size: 0.75em; text-overflow: ellipsis; overflow: hidden; white-space: nowrap; }}
        .video-icon {{ position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); font-size: 48px; color: white; text-shadow: 0 2px 4px rgba(0,0,0,0.5); pointer-events: none; }}
        .error-placeholder {{ display: flex; align-items: center; justify-content: center; height: 100%; background: #e9ecef; color: #6c757d; font-size: 0.9em; text-align: center; padding: 10px; }}
        .heic-notice {{ background: #fff3cd; color: #856404; padding: 8px; border-radius: 4px; font-size: 0.85em; margin: 10px 0; }}
        .status {{ display: inline-block; padding: 4px 12px; border-radius: 12px; font-size: 0.85em; }}
        .status-pending {{ background: #fff3cd; color: #856404; }}
        .platforms {{ color: #666; font-size: 0.9em; }}
        h1 {{ color: #1877f2; }}
        .summary {{ background: #e7f3ff; padding: 15px; border-radius: 8px; margin-bottom: 20px; }}
        .error-msg {{ color: #721c24; background: #f8d7da; padding: 10px; border-radius: 4px; margin: 10px 0; }}
    </style>
</head>
<body>
    <h1>📸 Travel Posts Preview</h1>
    <div class="summary">
        <strong>Total Posts:</strong> {summary['total_posts']}<br>
        <strong>Schedule:</strong> {summary['start_date']} to {summary['end_date']}<br>
        <strong>Locations:</strong> {summary['locations']} cities in {summary['countries']} countries
    </div>
    <div class="heic-notice">
        ℹ️ <strong>Note:</strong> HEIC/HEIF images (iPhone format) cannot be displayed in web browsers. They show as placeholders here but will work perfectly when posted to Facebook/Instagram. JPG and PNG images display normally.
    </div>
"""
    
    for post in posts:
        html += f"""
    <div class="post">
        <div class="post-header">
            <div class="post-id">Post ID: {post['post_id']}</div>
            <div class="schedule">📅 Scheduled: {post['scheduled_date']} at {post['scheduled_time']}</div>
            <span class="status status-pending">{post['status'].replace('_', ' ').title()}</span>
        </div>
        
        <div class="location">
            📍 {post['location']['landmark']}, {post['location']['city']}, {post['location']['country']}
        </div>
        
        <div class="caption">
{post['caption']['combined']}
        </div>
        
        <div class="hashtags">
{' '.join(post['hashtags'])}
        </div>
        
        <div class="media-gallery">
            <strong>Media ({post['media_count']} files):</strong>
            <div class="media-grid">
"""
        
        # Add images and videos
        has_heic = False
        for media in post['media']:
            media_path = Path(media)
            filename = media_path.name
            ext = media_path.suffix.lower()
            # Use file:// protocol for local files
            file_url = f"file://{media}"
            
            # Check if it's a video
            is_video = ext in ['.mov', '.mp4', '.m4v', '.avi']
            is_heic = ext in ['.heic', '.heif']
            
            if is_heic:
                has_heic = True
                # HEIC files can't be displayed in browsers
                html += f"""
                <div class="media-item">
                    <div class="error-placeholder">
                        📷 HEIC Image<br>
                        <small>{filename}</small><br>
                        <small style="font-size: 0.75em;">(Not supported in browser)</small>
                    </div>
                </div>
"""
            elif is_video:
                html += f"""
                <div class="media-item">
                    <video controls preload="metadata">
                        <source src="{file_url}" type="video/mp4">
                        Your browser doesn't support video.
                    </video>
                    <div class="video-icon">▶️</div>
                    <div class="media-label">🎥 {filename}</div>
                </div>
"""
            else:
                # Regular image formats (JPG, PNG, etc.)
                html += f"""
                <div class="media-item">
                    <img src="{file_url}" alt="{filename}" loading="lazy" onerror="this.parentElement.innerHTML='<div class=\\"error-placeholder\\">❌ Image not found<br><small>{filename}</small></div>'">
                    <div class="media-label">📷 {filename}</div>
                </div>
"""
        
        html += """
            </div>
"""
        
        # Add HEIC notice if needed
        if has_heic:
            html += """
            <div class="heic-notice">
                ℹ️ HEIC images cannot be displayed in browsers. They will work fine when posted to social media. You can view them by opening the folder.
            </div>
"""
        
        html += f"""
        </div>
        
        <div class="platforms">
            Platforms: {', '.join(post['platforms'])}
        </div>
    </div>
"""
    
    html += """
</body>
</html>
"""
    
    preview_file = output_path / "preview.html"
    with open(preview_file, 'w', encoding='utf-8') as f:
        f.write(html)
    
    return preview_file


def main():
    """Main execution function."""
    print("Travel Post Generator")
    print("=" * 60)
    
    # Scan organized photos
    print(f"\n1. Scanning organized photos from: {ORGANIZED_PHOTOS_DIR}")
    locations = scan_organized_photos(ORGANIZED_PHOTOS_DIR)
    print(f"   Found {len(locations)} locations with photos/videos")
    
    if not locations:
        print("\n❌ No locations found. Please run photo_video_organizer.py first!")
        return
    
    # Show summary
    countries = set(loc["country"] for loc in locations)
    cities = set(loc["city"] for loc in locations)
    total_media = sum(loc["media_count"] for loc in locations)
    
    print(f"\n   Summary:")
    print(f"   - Countries: {len(countries)}")
    print(f"   - Cities: {len(cities)}")
    print(f"   - Total media files: {total_media}")
    
    # Generate posts
    print(f"\n2. Generating posts...")
    print(f"   - Posts per day: {POSTS_PER_DAY}")
    print(f"   - Starting from: {START_DATE.strftime('%Y-%m-%d')}")
    
    posts = generate_posts(locations, START_DATE, POSTS_PER_DAY)
    print(f"   Generated {len(posts)} posts")
    
    # Save posts
    print(f"\n3. Saving posts to: {OUTPUT_DIR}")
    summary = save_posts(posts, OUTPUT_DIR)
    print(f"   ✓ Saved {summary['total_posts']} posts")
    print(f"   ✓ Schedule: {summary['date_range']['start']} to {summary['date_range']['end']}")
    
    # Create preview
    print(f"\n4. Creating preview...")
    preview_file = create_preview_html(posts, OUTPUT_DIR)
    print(f"   ✓ Preview created: {preview_file}")
    
    print("\n" + "=" * 60)
    print("✅ Done!")
    print(f"\nNext steps:")
    print(f"1. Open preview: {preview_file}")
    print(f"2. Review all posts")
    print(f"3. Edit posts if needed (JSON files in {OUTPUT_DIR}/posts/)")
    print(f"4. Use the posting tool to publish approved posts")
    print("\nAll posts are saved and ready for your review!")


if __name__ == "__main__":
    main()
