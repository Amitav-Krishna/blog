#!/bin/bash
# Daily git push script for blog

cd /home/amitav-krishna/html_blog

# Check if there are commits to push
if git rev-parse --abbrev-ref HEAD@{upstream} > /dev/null 2>&1; then
    LOCAL=$(git rev-parse @)
    REMOTE=$(git rev-parse @{u})
    
    if [ "$LOCAL" != "$REMOTE" ]; then
        echo "Pushing commits..."
        git push origin main 2>&1
        echo "Push complete at $(date)"
    else
        echo "Nothing to push at $(date)"
    fi
else
    echo "No upstream set or other error"
fi
