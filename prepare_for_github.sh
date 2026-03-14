#!/bin/bash
# Prepare repository for GitHub upload

echo "Preparing repository for GitHub..."
echo "=================================="

# Rename README for GitHub
if [ -f "README_GITHUB.md" ]; then
    echo "✓ Renaming README_GITHUB.md to README.md"
    mv README_GITHUB.md README.md
fi

# Check if git is initialized
if [ ! -d ".git" ]; then
    echo "✓ Initializing git repository"
    git init
else
    echo "✓ Git repository already initialized"
fi

# Show what will be committed
echo ""
echo "Files to be committed:"
echo "====================="
git add -n .

echo ""
echo "Files that will be ignored:"
echo "=========================="
git status --ignored | grep "^!!" || echo "(none)"

echo ""
echo "Next steps:"
echo "==========="
echo "1. Review the files above"
echo "2. Run: git add ."
echo "3. Run: git commit -m 'Initial commit: Photo & Video Organizer'"
echo "4. Create repository on GitHub"
echo "5. Run: git remote add origin https://github.com/yourusername/photo-video-organizer.git"
echo "6. Run: git branch -M main"
echo "7. Run: git push -u origin main"
echo ""
echo "See GITHUB_SETUP.md for detailed instructions!"
