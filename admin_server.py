#!/usr/bin/env python3
"""Minimal admin interface for Hugo blog - using only stdlib."""

import hashlib
import json
import os
import re
import subprocess
import cgi
from urllib.parse import unquote_plus
from datetime import datetime
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler

# Configuration
PASSWORD_HASH = "ab81c9510a22302a9127cdf226e78664736f3bb3cca1bb9e0fcb0e2e9e7d2b5e"
CONTENT_DIR = Path("/home/amitav-krishna/html_blog/hugo-site/content/posts")
HUGO_SITE_DIR = Path("/home/amitav-krishna/html_blog/hugo-site")
POSTS_JSON = Path("/home/amitav-krishna/html_blog/posts.json")
IMAGES_DIR = Path("/home/amitav-krishna/html_blog/hugo-site/static/images")

BASE_STYLE = '''
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: system-ui, -apple-system, sans-serif;
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background: #f5f5f5;
        }}
        h1 {{ margin-bottom: 20px; color: #333; }}
        .form-group {{ margin-bottom: 15px; }}
        label {{ display: block; margin-bottom: 5px; font-weight: 500; color: #555; }}
        input[type="text"], input[type="password"] {{
            width: 100%;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }}
        textarea {{
            width: 100%;
            min-height: 400px;
            padding: 10px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-family: monospace;
            font-size: 14px;
            line-height: 1.5;
        }}
        textarea.content {{ min-height: 500px; }}
        button {{
            background: #0066cc;
            color: white;
            padding: 12px 24px;
            border: none;
            border-radius: 4px;
            cursor: pointer;
            font-size: 16px;
        }}
        button:hover {{ background: #0052a3; }}
        .btn-secondary {{
            background: #666;
            margin-left: 10px;
        }}
        .btn-secondary:hover {{ background: #444; }}
        .error {{ color: #c00; margin-top: 10px; padding: 10px; background: #fee; border-radius: 4px; }}
        .success {{ color: #0a0; margin-top: 10px; padding: 10px; background: #efe; border-radius: 4px; }}
        .hint {{ color: #666; font-size: 12px; margin-top: 4px; }}
        .meta-section {{
            background: #fff;
            padding: 15px;
            border-radius: 4px;
            margin-bottom: 15px;
            border: 1px solid #ddd;
        }}
        .meta-section h3 {{
            margin-bottom: 10px;
            color: #555;
            font-size: 14px;
            text-transform: uppercase;
        }}
        .nav-links {{
            margin-bottom: 20px;
            padding: 10px;
            background: #fff;
            border-radius: 4px;
            border: 1px solid #ddd;
        }}
        .nav-links a {{
            margin-right: 15px;
            color: #0066cc;
            text-decoration: none;
        }}
        .nav-links a:hover {{
            text-decoration: underline;
        }}
        .image-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
            gap: 20px;
            margin-top: 20px;
        }}
        .image-item {{
            background: #fff;
            border: 1px solid #ddd;
            border-radius: 4px;
            padding: 10px;
            text-align: center;
        }}
        .image-item img {{
            max-width: 100%;
            max-height: 150px;
            object-fit: cover;
            border-radius: 4px;
        }}
        .image-item .filename {{
            margin-top: 10px;
            font-size: 12px;
            color: #666;
            word-break: break-all;
        }}
        .image-item .copy-btn {{
            margin-top: 5px;
            padding: 5px 10px;
            font-size: 12px;
        }}
        input[type="file"] {{
            padding: 10px;
            border: 2px dashed #ddd;
            border-radius: 4px;
            width: 100%;
        }}
'''

HTML_FORM = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>{title}</title>
    <style>{style}</style>
</head>
<body>
    <div class="nav-links">
        <a href="/admin">New Post</a>
        <a href="/admin/upload">Upload Images</a>
        <a href="/admin/images-list">View Images</a>
    </div>
    <h1>{heading}</h1>
    {message}
    <form method="POST" action="{action}">
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" name="password" required>
        </div>
        
        <div class="meta-section">
            <h3>Post Metadata</h3>
            <div class="form-group">
                <label for="title">Title</label>
                <input type="text" id="title" name="title" value="{post_title}" placeholder="My Awesome Post" required>
            </div>
            {slug_field}
            {date_field}
            <div class="form-group">
                <label for="tags">Tags (comma-separated)</label>
                <input type="text" id="tags" name="tags" value="{tags}" placeholder="python, tutorial, guide">
            </div>
            <div class="form-group">
                <label>
                    <input type="checkbox" name="draft" value="true" {draft_checked}>
                    Mark as draft (don't publish yet)
                </label>
            </div>
        </div>
        
        <div class="form-group">
            <label for="content">Content (Markdown)</label>
            <textarea id="content" name="content" class="content" placeholder="# Hello World\n\nWrite your post here in Markdown..." required>{content}</textarea>
        </div>
        
        <button type="submit">{button_text}</button>
        <a href="/posts/{slug}.html" class="btn-secondary" style="text-decoration:none;display:inline-block;">View Post</a>
    </form>
</body>
</html>'''

UPLOAD_FORM = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Upload Images</title>
    <style>{style}</style>
</head>
<body>
    <div class="nav-links">
        <a href="/admin">New Post</a>
        <a href="/admin/upload">Upload Images</a>
        <a href="/admin/images-list">View Images</a>
    </div>
    <h1>Upload Images</h1>
    {message}
    <form method="POST" action="/admin/upload" enctype="multipart/form-data">
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" name="password" required>
        </div>
        <div class="form-group">
            <label for="files">Select Images (you can select multiple)</label>
            <input type="file" id="files" name="files" multiple accept="image/*" required>
            <div class="hint">Hold Ctrl (or Cmd) to select multiple files</div>
        </div>
        <button type="submit">Upload Images</button>
    </form>
</body>
</html>'''

IMAGES_LIST = '''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Image Library</title>
    <style>{style}</style>
    <script>
        function copyMarkdown(filename) {{
            const markdown = `![Description](/images/${{filename}})`;
            navigator.clipboard.writeText(markdown).then(() => {{
                alert('Markdown copied: ' + markdown);
            }});
        }}
    </script>
</head>
<body>
    <div class="nav-links">
        <a href="/admin">New Post</a>
        <a href="/admin/upload">Upload Images</a>
        <a href="/admin/images-list">View Images</a>
    </div>
    <h1>Image Library</h1>
    {message}
    <form method="POST" action="/admin/images-list" style="margin-bottom: 20px;">
        <div class="form-group">
            <label for="password">Password</label>
            <input type="password" id="password" name="password" required style="width: 200px; display: inline-block;">
            <button type="submit">Authenticate</button>
        </div>
    </form>
    {images}
</body>
</html>'''


def verify_password(password: str) -> bool:
    """Check password against SHA256 hash."""
    password = password.strip()
    hashed = hashlib.sha256(password.encode()).hexdigest()
    return hashed == PASSWORD_HASH


def slugify(text: str) -> str:
    """Convert title to URL-friendly slug."""
    text = text.lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[-\s]+', '-', text)
    return text.strip('-')


def parse_post(filepath: Path) -> dict:
    """Parse a markdown post file to extract frontmatter and content."""
    content = filepath.read_text()
    
    if not content.startswith('---'):
        return {
            'title': filepath.stem.replace('-', ' ').title(),
            'date': '',
            'tags': '',
            'draft': False,
            'content': content
        }
    
    end_match = re.search(r'\n---\s*\n', content[3:])
    if not end_match:
        return {
            'title': filepath.stem.replace('-', ' ').title(),
            'date': '',
            'tags': '',
            'draft': False,
            'content': content
        }
    
    frontmatter_text = content[3:3+end_match.start()]
    body = content[3+end_match.end():]
    
    meta = {}
    for line in frontmatter_text.strip().split('\n'):
        if ':' in line:
            key, value = line.split(':', 1)
            meta[key.strip()] = value.strip().strip('"').strip("'")
    
    tags = meta.get('tags', [])
    if isinstance(tags, str):
        if tags.startswith('['):
            tags = tags.strip('[]').replace('"', '').replace("'", '')
        tags = tags
    
    return {
        'title': meta.get('title', filepath.stem.replace('-', ' ').title()),
        'date': meta.get('date', ''),
        'tags': tags if isinstance(tags, str) else ', '.join(tags) if tags else '',
        'draft': meta.get('draft', 'false').lower() == 'true',
        'content': body
    }


def rebuild_hugo():
    """Rebuild Hugo site."""
    try:
        hugo_bin = os.path.expanduser("~/bin/hugo")
        if not os.path.exists(hugo_bin):
            hugo_bin = "hugo"
        result = subprocess.run(
            [hugo_bin],
            cwd=HUGO_SITE_DIR,
            capture_output=True,
            text=True,
            timeout=30
        )
        if result.returncode != 0:
            print(f"Hugo rebuild warning: {result.stderr}")
            return False, result.stderr
        return True, ""
    except Exception as e:
        print(f"Hugo rebuild failed: {e}")
        return False, str(e)


def git_commit(file_path: Path, message: str) -> bool:
    """Commit a file to git."""
    try:
        git_dir = file_path.parent
        while git_dir != git_dir.parent:
            if (git_dir / ".git").exists():
                break
            git_dir = git_dir.parent
        
        result = subprocess.run(
            ["git", "add", str(file_path)],
            cwd=git_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            print(f"Git add warning: {result.stderr}")
        
        if POSTS_JSON.exists():
            subprocess.run(
                ["git", "add", str(POSTS_JSON)],
                cwd=git_dir,
                capture_output=True,
                text=True
            )
        
        result = subprocess.run(
            ["git", "commit", "-m", message],
            cwd=git_dir,
            capture_output=True,
            text=True
        )
        if result.returncode != 0:
            if "nothing to commit" in result.stdout or "nothing to commit" in result.stderr:
                return True
            print(f"Git commit warning: {result.stderr}")
            return False
        return True
    except Exception as e:
        print(f"Git commit failed: {e}")
        return False


def create_post(title: str, slug: str, content: str, tags: str = "", draft: bool = False) -> tuple[bool, str]:
    """Create a new blog post."""
    if not slug:
        slug = slugify(title)
    
    filename = f"{slug}.md"
    filepath = CONTENT_DIR / filename
    
    if filepath.exists():
        return False, f"A post with slug '{slug}' already exists"
    
    tags_list = [t.strip().lower() for t in tags.split(',') if t.strip()]
    tags_yaml = ', '.join(f'"{t}"' for t in tags_list)
    
    now = datetime.now()
    frontmatter = f'''---
title: "{title}"
date: {now.isoformat()}
draft: {str(draft).lower()}
tags: [{tags_yaml}]
---

'''
    
    try:
        filepath.write_text(frontmatter + content)
    except Exception as e:
        return False, f"Failed to write file: {e}"
    
    success, error = rebuild_hugo()
    if not success:
        return False, f"Hugo rebuild failed: {error}"
    
    try:
        with open(POSTS_JSON, 'r') as f:
            data = json.load(f)
        
        html_file = f"{slug}.html"
        data['posts'].append({
            'title': title,
            'file': html_file
        })
        
        with open(POSTS_JSON, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to update posts.json: {e}")
    
    git_commit(filepath, f"Add post: {title}")
    
    return True, f"Post published! View at /posts/{slug}.html"


def update_post(slug: str, title: str, content: str, tags: str = "", draft: bool = False, date: str = "") -> tuple[bool, str]:
    """Update an existing blog post."""
    filename = f"{slug}.md"
    filepath = CONTENT_DIR / filename
    
    if not filepath.exists():
        return False, f"Post '{slug}' not found"
    
    existing = parse_post(filepath)
    
    tags_list = [t.strip().lower() for t in tags.split(',') if t.strip()]
    tags_yaml = ', '.join(f'"{t}"' for t in tags_list)
    
    date_str = date.strip() if date else existing.get('date', '')
    if not date_str:
        date_str = datetime.now().isoformat()
    
    frontmatter = f'''---
title: "{title}"
date: {date_str}
draft: {str(draft).lower()}
tags: [{tags_yaml}]
---

'''
    
    try:
        filepath.write_text(frontmatter + content)
    except Exception as e:
        return False, f"Failed to write file: {e}"
    
    success, error = rebuild_hugo()
    if not success:
        return False, f"Hugo rebuild failed: {error}"
    
    try:
        with open(POSTS_JSON, 'r') as f:
            data = json.load(f)
        
        for post in data['posts']:
            if post['file'] == f"{slug}.html":
                post['title'] = title
                break
        
        with open(POSTS_JSON, 'w') as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"Failed to update posts.json: {e}")
    
    git_commit(filepath, f"Update post: {title}")
    
    return True, f"Post updated! View at /posts/{slug}.html"


class AdminHandler(BaseHTTPRequestHandler):
    def send_html(self, html: str, status: int = 200):
        """Send HTML response."""
        self.send_response(status)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html.encode())
    
    def parse_multipart(self, content_type: str, post_data: bytes) -> dict:
        """Parse multipart form data."""
        result = {'files': [], 'fields': {}}
        
        # Extract boundary
        boundary = None
        for part in content_type.split(';'):
            if 'boundary=' in part:
                boundary = part.split('=', 1)[1].strip('"\'')
                break
        
        if not boundary:
            return result
        
        boundary_bytes = f'--{boundary}'.encode()
        parts = post_data.split(boundary_bytes)
        
        for part in parts:
            part = part.strip(b'\r\n')
            if not part or part == b'--':
                continue
            
            # Split headers and body
            if b'\r\n\r\n' in part:
                headers, body = part.split(b'\r\n\r\n', 1)
            else:
                continue
            
            headers_str = headers.decode('utf-8', errors='replace')
            
            # Check if file or field
            if 'filename=' in headers_str:
                # Extract filename
                filename_match = re.search(r'filename="([^"]+)"', headers_str)
                if filename_match:
                    filename = filename_match.group(1)
                    # Remove trailing -- if present
                    body = body.rstrip(b'\r\n--')
                    result['files'].append({'filename': filename, 'data': body})
            else:
                # Regular field
                name_match = re.search(r'name="([^"]+)"', headers_str)
                if name_match:
                    name = name_match.group(1)
                    result['fields'][name] = body.decode('utf-8', errors='replace').strip()
        
        return result
    
    def render_form(self, title: str, heading: str, action: str, 
                   post_title: str = "", slug: str = "", date: str = "", tags: str = "", 
                   draft: bool = False, content: str = "", 
                   message: str = "", button_text: str = "Publish Post",
                   is_edit: bool = False):
        """Render the form HTML."""
        slug_field = ''
        if not is_edit:
            slug_field = '''<div class="form-group">
                <label for="slug">URL Slug (optional)</label>
                <input type="text" id="slug" name="slug" placeholder="my-awesome-post">
                <div class="hint">Leave blank to auto-generate from title</div>
            </div>'''
        
        date_field = ''
        if is_edit:
            date_field = f'''<div class="form-group">
                <label for="date">Date</label>
                <input type="text" id="date" name="date" value="{date.replace('"', '&quot;')}" placeholder="2026-05-19T10:00:00">
                <div class="hint">ISO format date (e.g., 2026-05-19T10:00:00)</div>
            </div>'''
        
        draft_checked = 'checked' if draft else ''
        
        html = HTML_FORM.format(
            title=title,
            style=BASE_STYLE,
            heading=heading,
            message=message,
            action=action,
            post_title=post_title.replace('"', '&quot;'),
            slug_field=slug_field,
            date_field=date_field,
            tags=tags,
            draft_checked=draft_checked,
            content=content.replace('</textarea>', '&lt;/textarea&gt;'),
            button_text=button_text,
            slug=slug
        )
        return html
    
    def do_GET(self):
        path = self.path
        
        if path == '/admin':
            html = self.render_form(
                title="Admin - New Post",
                heading="New Blog Post",
                action="/admin",
                button_text="Publish Post"
            )
            self.send_html(html)
            return
        
        if path == '/admin/upload':
            html = UPLOAD_FORM.format(style=BASE_STYLE, message='')
            self.send_html(html)
            return
        
        if path == '/admin/images-list':
            html = IMAGES_LIST.format(
                style=BASE_STYLE,
                message='<p style="color: #666;">Enter password to view images</p>',
                images=''
            )
            self.send_html(html)
            return
        
        match = re.match(r'/admin/posts/(.+)\.html$', path)
        if match:
            slug = match.group(1)
            filepath = CONTENT_DIR / f"{slug}.md"
            
            if not filepath.exists():
                self.send_html(f'<h1>Post not found</h1><p>No post with slug "{slug}"</p><a href="/admin">Back to admin</a>', 404)
                return
            
            post = parse_post(filepath)
            html = self.render_form(
                title=f"Edit - {post['title']}",
                heading=f"Edit: {post['title']}",
                action=f"/admin/posts/{slug}.html",
                post_title=post['title'],
                slug=slug,
                date=post['date'],
                tags=post['tags'],
                draft=post['draft'],
                content=post['content'],
                button_text="Update Post",
                is_edit=True
            )
            self.send_html(html)
            return
        
        self.send_response(404)
        self.end_headers()
    
    def do_POST(self):
        path = self.path
        content_type = self.headers.get('Content-Type', '')
        content_length = int(self.headers.get('Content-Length', 0))
        
        if content_length > 0:
            post_data = self.rfile.read(content_length)
        else:
            post_data = b''
        
        # Handle multipart form data (file uploads)
        if 'multipart/form-data' in content_type:
            parsed = self.parse_multipart(content_type, post_data)
            params = parsed['fields']
            files = parsed['files']
        else:
            # Regular form data
            params = {}
            for pair in post_data.decode('utf-8').split('&'):
                if '=' in pair:
                    key, value = pair.split('=', 1)
                    params[unquote_plus(key)] = unquote_plus(value)
            files = []
        
        password = params.get('password', '').strip()
        
        if not verify_password(password):
            if path == '/admin':
                html = self.render_form(
                    title="Admin - New Post",
                    heading="New Blog Post",
                    action="/admin",
                    message='<div class="error">Invalid password</div>'
                )
                self.send_html(html, 401)
            elif path == '/admin/upload':
                html = UPLOAD_FORM.format(
                    style=BASE_STYLE,
                    message='<div class="error">Invalid password</div>'
                )
                self.send_html(html, 401)
            elif path == '/admin/images-list':
                html = IMAGES_LIST.format(
                    style=BASE_STYLE,
                    message='<div class="error">Invalid password</div>',
                    images=''
                )
                self.send_html(html, 401)
            else:
                self.send_html('<div class="error">Invalid password</div>', 401)
            return
        
        # Handle upload
        if path == '/admin/upload':
            if not files:
                html = UPLOAD_FORM.format(
                    style=BASE_STYLE,
                    message='<div class="error">No files selected</div>'
                )
                self.send_html(html, 400)
                return
            
            IMAGES_DIR.mkdir(parents=True, exist_ok=True)
            uploaded = []
            
            for file_info in files:
                filename = file_info['filename']
                # Sanitize filename
                filename = re.sub(r'[^\w\-\.]', '_', filename)
                filepath = IMAGES_DIR / filename
                
                try:
                    filepath.write_bytes(file_info['data'])
                    uploaded.append(filename)
                except Exception as e:
                    print(f"Failed to save {filename}: {e}")
            
            if uploaded:
                message = f'<div class="success">✓ Uploaded {len(uploaded)} file(s): {", ".join(uploaded)}</div>'
            else:
                message = '<div class="error">Failed to upload files</div>'
            
            html = UPLOAD_FORM.format(style=BASE_STYLE, message=message)
            self.send_html(html)
            return
        
        # Handle images list
        if path == '/admin/images-list':
            IMAGES_DIR.mkdir(parents=True, exist_ok=True)
            image_files = sorted([f for f in IMAGES_DIR.iterdir() if f.is_file()])
            
            if not image_files:
                images_html = '<p>No images uploaded yet.</p>'
            else:
                images_html = '<div class="image-grid">'
                for img_path in image_files:
                    img_url = f"/images/{img_path.name}"
                    images_html += f'''
                    <div class="image-item">
                        <img src="{img_url}" alt="{img_path.name}">
                        <div class="filename">{img_path.name}</div>
                        <button class="copy-btn" onclick="copyMarkdown('{img_path.name}')">Copy Markdown</button>
                    </div>'''
                images_html += '</div>'
            
            html = IMAGES_LIST.format(
                style=BASE_STYLE,
                message='',
                images=images_html
            )
            self.send_html(html)
            return
        
        # New post
        if path == '/admin':
            title = params.get('title', '').strip()
            slug = params.get('slug', '').strip()
            content = params.get('content', '')
            tags = params.get('tags', '')
            draft = params.get('draft', '') == 'true'
            
            if not title or not content:
                html = self.render_form(
                    title="Admin - New Post",
                    heading="New Blog Post",
                    action="/admin",
                    message='<div class="error">Title and content are required</div>'
                )
                self.send_html(html, 400)
                return
            
            success, message = create_post(title, slug, content, tags, draft)
            
            if success:
                slug = slug or slugify(title)
                html = self.render_form(
                    title="Admin - New Post",
                    heading="New Blog Post",
                    action="/admin",
                    message=f'<div class="success">✓ {message}</div>',
                    slug=slug
                )
                self.send_html(html)
            else:
                html = self.render_form(
                    title="Admin - New Post",
                    heading="New Blog Post",
                    action="/admin",
                    message=f'<div class="error">Error: {message}</div>'
                )
                self.send_html(html, 400)
            return
        
        # Update post
        match = re.match(r'/admin/posts/(.+)\.html$', path)
        if match:
            slug = match.group(1)
            title = params.get('title', '').strip()
            content = params.get('content', '')
            tags = params.get('tags', '')
            date = params.get('date', '')
            draft = params.get('draft', '') == 'true'
            
            if not title or not content:
                post = parse_post(CONTENT_DIR / f"{slug}.md")
                html = self.render_form(
                    title=f"Edit - {post['title']}",
                    heading=f"Edit: {post['title']}",
                    action=f"/admin/posts/{slug}.html",
                    post_title=post['title'],
                    slug=slug,
                    date=post['date'],
                    tags=post['tags'],
                    draft=post['draft'],
                    content=post['content'],
                    message='<div class="error">Title and content are required</div>',
                    button_text="Update Post",
                    is_edit=True
                )
                self.send_html(html, 400)
                return
            
            success, message = update_post(slug, title, content, tags, draft, date)
            
            post = parse_post(CONTENT_DIR / f"{slug}.md")
            if success:
                html = self.render_form(
                    title=f"Edit - {title}",
                    heading=f"Edit: {title}",
                    action=f"/admin/posts/{slug}.html",
                    post_title=title,
                    slug=slug,
                    date=date or post['date'],
                    tags=tags,
                    draft=draft,
                    content=content,
                    message=f'<div class="success">✓ {message}</div>',
                    button_text="Update Post",
                    is_edit=True
                )
                self.send_html(html)
            else:
                html = self.render_form(
                    title=f"Edit - {title}",
                    heading=f"Edit: {title}",
                    action=f"/admin/posts/{slug}.html",
                    post_title=title,
                    slug=slug,
                    date=date or post['date'],
                    tags=tags,
                    draft=draft,
                    content=content,
                    message=f'<div class="error">Error: {message}</div>',
                    button_text="Update Post",
                    is_edit=True
                )
                self.send_html(html, 400)
            return
        
        self.send_response(404)
        self.end_headers()
    
    def log_message(self, format, *args):
        pass


if __name__ == '__main__':
    CONTENT_DIR.mkdir(parents=True, exist_ok=True)
    IMAGES_DIR.mkdir(parents=True, exist_ok=True)
    
    server = HTTPServer(('127.0.0.1', 4569), AdminHandler)
    print("Admin server running on http://127.0.0.1:4569")
    server.serve_forever()
