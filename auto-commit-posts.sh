#!/bin/bash
# Auto-stage and commit changes to content/posts

cd /home/amitav-krishna/html_blog

# Check if there are changes in content/posts
if git diff --quiet hugo-site/content/posts/ && git diff --cached --quiet hugo-site/content/posts/; then
    exit 0
fi

# Stage content/posts changes
git add hugo-site/content/posts/

# Create commit with timestamp
COMMIT_MSG="Auto-commit posts: $(date '+%Y-%m-%d %H:%M:%S')"
git commit -m "$COMMIT_MSG"

echo "Auto-committed posts at $(date)"