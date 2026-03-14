#!/bin/bash
# Setup script for photo_video_organizer.py environment

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -r requirements.txt

echo ""
echo "Setup complete! To use the environment:"
echo "  source venv/bin/activate"
echo "  python photo_video_organizer.py"
