#!/bin/bash

echo "=== Git Status ==="
git status

echo ""
echo "=== Current Branch ==="
git branch

echo ""
echo "=== Recent Commits ==="
git log --oneline -3

echo ""
echo "=== Remote Repository ==="
git remote -v

echo ""
echo "=== Pushing to GitHub ==="
git push origin main

echo ""
echo "=== Push Complete! ==="
echo "Visit: https://github.com/Jhhuangkay/photo-video-organizer"
