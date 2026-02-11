#!/usr/bin/env python3
"""Build script to auto-generate blog navigation."""

import json
from pathlib import Path

def load_posts():
    with open('posts.json', 'r') as f:
        return json.load(f)['posts']

def generate_nav(current_file, posts):
    other_posts = [p for p in posts if p['file'] != current_file]
    links = "\n".join([f'<li><a href="./{p["file"]}">{p["title"]}</a></li>' for p in other_posts])
    
    return f'''<div id="blog-nav" style="max-width: 60em; margin: 2em auto; padding: 1em; border-top: 1px solid #eee;">
<h3>Other Posts</h3>
<ul>
{links}
</ul>
<p><a href="./about.html">&larr; Back to Blog</a></p>
</div>'''

def update_file(filepath, posts):
    with open(filepath, 'r') as f:
        content = f.read()
    
    new_nav = generate_nav(filepath.name, posts)
    
    # Insert before postamble
    if '<div id="blog-nav"' not in content:
        content = content.replace(
            '<div id="postamble" class="status">',
            new_nav + '\n<div id="postamble" class="status">'
        )
        print(f"Added nav to: {filepath}")
    else:
        print(f"Nav already exists in: {filepath}")
    
    with open(filepath, 'w') as f:
        f.write(content)

def main():
    posts = load_posts()
    for post in posts:
        filepath = Path(post['file'])
        if filepath.exists():
            update_file(filepath, posts)
        else:
            print(f"Warning: {filepath} not found")
    print("\nDone!")

if __name__ == '__main__':
    main()
