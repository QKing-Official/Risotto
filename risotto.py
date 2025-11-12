#!/usr/bin/env python3
"""
Risotto - A simple static documentation site generator
Converts Markdown files to HTML with configurable styling and theme switching
"""

import os
import json
import re
import base64
from pathlib import Path
from typing import Dict, List, Optional
import argparse

# Icons since emojis are ugly for this
DEFAULT_LOGO_LIGHT = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiMyNTYzZWIiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNNCAxOS41di0xNUEyLjUgMi41IDAgMCAxIDYuNSAySDIwdjIwSDYuNWEyLjUgMi41IDAgMCAxIDAtNUgyMCIvPjwvc3ZnPg=="
DEFAULT_LOGO_DARK = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIzMiIgaGVpZ2h0PSIzMiIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiMzYjgyZjYiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNNCAxOS41di0xNUEyLjUgMi41IDAgMCAxIDYuNSAySDIwdjIwSDYuNWEyLjUgMi41IDAgMCAxIDAtNUgyMCIvPjwvc3ZnPg=="
DEFAULT_ICON_SUN = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmNTllMGIiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48Y2lyY2xlIGN4PSIxMiIgY3k9IjEyIiByPSI0Ii8+PHBhdGggZD0iTTEyIDJ2MiIvPjxwYXRoIGQ9Ik0xMiAyMHYyIi8+PHBhdGggZD0ibTQuOTMgNC45MyAxLjQxIDEuNDEiLz48cGF0aCBkPSJtMTcuNjYgMTcuNjYgMS40MSAxLjQxIi8+PHBhdGggZD0iTTIgMTJoMiIvPjxwYXRoIGQ9Ik0yMCAxMmgyIi8+PHBhdGggZD0ibTYuMzQgMTcuNjYtMS40MSAxLjQxIi8+PHBhdGggZD0ibTE5LjA3IDQuOTMtMS40MSAxLjQxIi8+PC9zdmc+"
DEFAULT_ICON_MOON = "data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSJub25lIiBzdHJva2U9IiNmNTllMGIiIHN0cm9rZS13aWR0aD0iMiIgc3Ryb2tlLWxpbmVjYXA9InJvdW5kIiBzdHJva2UtbGluZWpvaW49InJvdW5kIj48cGF0aCBkPSJNMTIgM2E2IDYgMCAwIDAgOSA5IDkgOSAwIDEgMS05LTlaIi8+PC9zdmc+"


class RisottoConfig:
    # Just the config.risotto setup, dont mind the mess that's here
    def __init__(self, config_path: str = "config.risotto"):
        self.config = self._load_config(config_path)
    
    def _load_config(self, path: str) -> Dict:
        defaults = {
            "site_name": "Documentation",
            "site_title": "Documentation",
            "description": "Documentation site built with Risotto",
            "favicon": None,
            "logo": {
                "light": DEFAULT_LOGO_LIGHT,
                "dark": DEFAULT_LOGO_DARK
            },
            "theme_icons": {
                "light": DEFAULT_ICON_SUN,
                "dark": DEFAULT_ICON_MOON
            },
            "colors": {
                "light": {
                    "primary": "#2563eb",
                    "secondary": "#64748b",
                    "background": "#ffffff",
                    "text": "#1e293b",
                    "sidebar": "#f8fafc"
                },
                "dark": {
                    "primary": "#3b82f6",
                    "secondary": "#94a3b8",
                    "background": "#0f172a",
                    "text": "#e2e8f0",
                    "sidebar": "#1e293b"
                }
            },
            "output_dir": "site",
            "home_page": "index.md"
        }
        
        if os.path.exists(path):
            with open(path, 'r') as f:
                user_config = json.load(f)
                if "colors" in user_config:
                    if "light" in user_config["colors"]:
                        defaults["colors"]["light"].update(user_config["colors"]["light"])
                    if "dark" in user_config["colors"]:
                        defaults["colors"]["dark"].update(user_config["colors"]["dark"])
                    user_config.pop("colors")
                if "logo" in user_config:
                    if isinstance(user_config["logo"], dict):
                        defaults["logo"].update(user_config["logo"])
                    user_config.pop("logo")
                if "theme_icons" in user_config:
                    if isinstance(user_config["theme_icons"], dict):
                        defaults["theme_icons"].update(user_config["theme_icons"])
                    user_config.pop("theme_icons")
                defaults.update(user_config)
        
        return defaults
    
    def get(self, key: str, default=None):
        return self.config.get(key, default)


class MarkdownParser:
    # Just md to html shit
    @staticmethod
    def parse(content: str) -> str:
        html = content
        
        # Headers
        html = re.sub(r'^# (.*?)$', r'<h1>\1</h1>', html, flags=re.MULTILINE)
        html = re.sub(r'^## (.*?)$', r'<h2>\1</h2>', html, flags=re.MULTILINE)
        html = re.sub(r'^### (.*?)$', r'<h3>\1</h3>', html, flags=re.MULTILINE)
        html = re.sub(r'^#### (.*?)$', r'<h4>\1</h4>', html, flags=re.MULTILINE)
        
        # Bold and italic
        html = re.sub(r'\*\*\*(.*?)\*\*\*', r'<strong><em>\1</em></strong>', html)
        html = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', html)
        html = re.sub(r'\*(.*?)\*', r'<em>\1</em>', html)
        html = re.sub(r'___(.*?)___', r'<strong><em>\1</em></strong>', html)
        html = re.sub(r'__(.*?)__', r'<strong>\1</strong>', html)
        html = re.sub(r'_(.*?)_', r'<em>\1</em>', html)
        
        # Code blocks
        html = re.sub(r'```(\w+)?\n(.*?)```', r'<pre><code>\2</code></pre>', html, flags=re.DOTALL)
        html = re.sub(r'`([^`]+)`', r'<code>\1</code>', html)
        
        # Links
        html = re.sub(r'\[(.*?)\]\((.*?)\)', r'<a href="\2">\1</a>', html)
        
        # Lists
        lines = html.split('\n')
        in_ul = False
        in_ol = False
        result = []
        
        for line in lines:
            ul_match = re.match(r'^[\*\-] (.*)$', line)
            ol_match = re.match(r'^\d+\. (.*)$', line)
            
            if ul_match:
                if not in_ul:
                    result.append('<ul>')
                    in_ul = True
                result.append(f'<li>{ul_match.group(1)}</li>')
            elif ol_match:
                if not in_ol:
                    result.append('<ol>')
                    in_ol = True
                result.append(f'<li>{ol_match.group(1)}</li>')
            else:
                if in_ul:
                    result.append('</ul>')
                    in_ul = False
                if in_ol:
                    result.append('</ol>')
                    in_ol = False
                result.append(line)
        
        if in_ul:
            result.append('</ul>')
        if in_ol:
            result.append('</ol>')
        
        html = '\n'.join(result)
        
        # Paragraphs
        paragraphs = html.split('\n\n')
        html_parts = []
        for para in paragraphs:
            para = para.strip()
            if para and not para.startswith('<'):
                html_parts.append(f'<p>{para}</p>')
            else:
                html_parts.append(para)
        
        return '\n'.join(html_parts)


class RisottoGenerator:
    # The gen itself    
    def __init__(self, docs_dir: str = "docs", config_path: str = "config.risotto"):
        self.docs_dir = Path(docs_dir)
        self.config = RisottoConfig(config_path)
        self.output_dir = Path(self.config.get("output_dir"))
        self.nav_structure = []
    
    def scan_docs(self) -> tuple[List[Dict], Optional[Path]]:
        structure = []
        home_page_path = None
        
        if not self.docs_dir.exists():
            print(f"Error: Documentation directory '{self.docs_dir}' not found")
            return structure, home_page_path
        
        # Look for home page
        home_page_name = self.config.get("home_page")
        home_candidate = self.docs_dir / home_page_name
        if home_candidate.exists():
            home_page_path = home_candidate
        
        for item_path in sorted(self.docs_dir.iterdir()):
            if item_path.is_dir():
                # This is a category
                category = {
                    "name": item_path.name,
                    "path": item_path,
                    "pages": []
                }
                
                # Get all markdown files in this category
                for page_path in sorted(item_path.glob("*.md")):
                    category["pages"].append({
                        "name": page_path.stem,
                        "path": page_path
                    })
                
                if category["pages"]:
                    structure.append(category)
            elif item_path.suffix == '.md' and item_path.name != home_page_name:
                pass
        
        return structure, home_page_path
    
    def generate_html_template(self, title: str, content: str, nav_html: str, current_page: str = "") -> str:
        # Gen the page!
        light_colors = self.config.get("colors")["light"]
        dark_colors = self.config.get("colors")["dark"]
        site_name = self.config.get("site_name")
        site_title = self.config.get("site_title")
        description = self.config.get("description")
        favicon = self.config.get("favicon")
        logo = self.config.get("logo")
        theme_icons = self.config.get("theme_icons")
        
        favicon_html = f'<link rel="icon" type="image/x-icon" href="{favicon}">' if favicon else ''
        
        return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{description}">
    <title>{title} - {site_title}</title>
    {favicon_html}
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        :root {{
            --primary: {light_colors['primary']};
            --secondary: {light_colors['secondary']};
            --background: {light_colors['background']};
            --text: {light_colors['text']};
            --sidebar: {light_colors['sidebar']};
        }}
        
        [data-theme="dark"] {{
            --primary: {dark_colors['primary']};
            --secondary: {dark_colors['secondary']};
            --background: {dark_colors['background']};
            --text: {dark_colors['text']};
            --sidebar: {dark_colors['sidebar']};
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            line-height: 1.6;
            color: var(--text);
            background: var(--background);
            transition: background-color 0.3s ease, color 0.3s ease;
        }}
        
        .container {{
            display: flex;
            min-height: 100vh;
        }}
        
        .sidebar {{
            width: 280px;
            background: var(--sidebar);
            padding: 2rem 1rem;
            overflow-y: auto;
            border-right: 1px solid color-mix(in srgb, var(--text) 15%, transparent);
            position: fixed;
            height: 100vh;
            transition: background-color 0.3s ease;
        }}
        
        .site-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 2rem;
        }}
        
        .site-title {{
            font-size: 1.5rem;
            font-weight: bold;
            color: var(--primary);
        }}
        
        .site-title a {{
            display: flex;
            align-items: center;
            gap: 0.75rem;
            text-decoration: none;
            color: inherit;
        }}
        
        .site-title a:hover {{
            opacity: 0.8;
        }}
        
        .site-logo {{
            height: 32px;
            width: 32px;
            object-fit: contain;
        }}
        
        [data-theme="light"] .site-logo.light-logo {{
            display: block;
        }}
        
        [data-theme="light"] .site-logo.dark-logo {{
            display: none;
        }}
        
        [data-theme="dark"] .site-logo.light-logo {{
            display: none;
        }}
        
        [data-theme="dark"] .site-logo.dark-logo {{
            display: block;
        }}
        
        .site-title a {{
            color: inherit;
            text-decoration: none;
        }}
        
        .site-title a:hover {{
            opacity: 0.8;
        }}
        
        .theme-toggle {{
            background: none;
            border: none;
            cursor: pointer;
            padding: 0.25rem;
            display: flex;
            align-items: center;
            justify-content: center;
            border-radius: 6px;
            transition: background-color 0.2s;
            width: 36px;
            height: 36px;
        }}
        
        .theme-toggle:hover {{
            background: color-mix(in srgb, var(--primary) 15%, transparent);
        }}
        
        .theme-icon {{
            width: 24px;
            height: 24px;
            object-fit: contain;
        }}
        
        [data-theme="light"] .theme-icon.light-icon {{
            display: block;
        }}
        
        [data-theme="light"] .theme-icon.dark-icon {{
            display: none;
        }}
        
        [data-theme="dark"] .theme-icon.light-icon {{
            display: none;
        }}
        
        [data-theme="dark"] .theme-icon.dark-icon {{
            display: block;
        }}
        
        .nav-category {{
            margin-bottom: 1.5rem;
        }}
        
        .nav-category-title {{
            font-weight: 600;
            margin-bottom: 0.5rem;
            color: var(--secondary);
            text-transform: uppercase;
            font-size: 0.875rem;
            letter-spacing: 0.5px;
        }}
        
        .nav-link {{
            display: block;
            padding: 0.5rem 0.75rem;
            margin-bottom: 0.25rem;
            color: var(--secondary);
            text-decoration: none;
            border-radius: 6px;
            transition: all 0.2s;
            font-size: 0.95rem;
        }}
        
        .nav-link:hover {{
            background: color-mix(in srgb, var(--primary) 15%, transparent);
            color: var(--primary);
        }}
        
        .nav-link.active {{
            background: var(--primary);
            color: white;
            font-weight: 500;
        }}
        
        .content {{
            flex: 1;
            padding: 3rem;
            margin-left: 280px;
            max-width: 1200px;
        }}
        
        h1 {{ 
            color: var(--primary); 
            font-size: 2.5rem;
            margin-top: 0;
            margin-bottom: 1.5rem;
            font-weight: 700;
        }}
        
        h2 {{ 
            margin-top: 2.5rem; 
            margin-bottom: 1rem;
            font-size: 1.875rem;
            color: var(--text);
            font-weight: 600;
            border-bottom: 2px solid color-mix(in srgb, var(--text) 15%, transparent);
            padding-bottom: 0.5rem;
        }}
        
        h3 {{ 
            margin-top: 1.5rem; 
            margin-bottom: 0.75rem;
            font-size: 1.5rem;
            color: var(--text);
            font-weight: 600;
        }}
        
        h4 {{ 
            margin-top: 1rem; 
            margin-bottom: 0.5rem;
            font-size: 1.25rem;
            font-weight: 600;
        }}
        
        p {{ 
            margin-bottom: 1rem;
            font-size: 1.05rem;
        }}
        
        code {{
            background: color-mix(in srgb, var(--text) 10%, transparent);
            color: var(--primary);
            padding: 0.2rem 0.4rem;
            border-radius: 3px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}
        
        pre {{
            background: color-mix(in srgb, var(--text) 95%, transparent);
            color: var(--background);
            padding: 1.25rem;
            border-radius: 8px;
            overflow-x: auto;
            margin: 1.5rem 0;
            line-height: 1.5;
        }}
        
        [data-theme="dark"] pre {{
            background: color-mix(in srgb, var(--background) 80%, black);
            color: var(--text);
        }}
        
        pre code {{
            background: none;
            padding: 0;
            color: inherit;
        }}
        
        ul, ol {{
            margin-left: 2rem;
            margin-bottom: 1rem;
        }}
        
        li {{
            margin-bottom: 0.5rem;
            font-size: 1.05rem;
        }}
        
        a {{
            color: var(--primary);
            text-decoration: none;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        @media (max-width: 768px) {{
            .sidebar {{
                display: none;
            }}
            
            .content {{
                margin-left: 0;
                padding: 1.5rem;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <aside class="sidebar">
            <div class="site-header">
                <div class="site-title">
                    <a href="/index.html">
                        <img src="{logo['light']}" alt="Logo" class="site-logo light-logo">
                        <img src="{logo['dark']}" alt="Logo" class="site-logo dark-logo">
                        <span>{site_name}</span>
                    </a>
                </div>
                <button class="theme-toggle" onclick="toggleTheme()" aria-label="Toggle theme">
                    <img src="{theme_icons['light']}" alt="Switch to dark theme" class="theme-icon light-icon">
                    <img src="{theme_icons['dark']}" alt="Switch to light theme" class="theme-icon dark-icon">
                </button>
            </div>
            <nav>
                {nav_html}
            </nav>
        </aside>
        <main class="content">
            {content}
        </main>
    </div>
    
    <script>
        // Theme management
        function getPreferredTheme() {{
            const stored = localStorage.getItem('theme');
            if (stored) return stored;
            return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
        }}
        
        function setTheme(theme) {{
            document.documentElement.setAttribute('data-theme', theme);
            localStorage.setItem('theme', theme);
        }}
        
        function toggleTheme() {{
            const current = document.documentElement.getAttribute('data-theme') || 'light';
            const next = current === 'light' ? 'dark' : 'light';
            setTheme(next);
        }}
        
        // Initialize theme
        setTheme(getPreferredTheme());
    </script>
</body>
</html>"""
    
    def generate_nav_html(self, structure: List[Dict], current_page: str = "") -> str:
        # Nav shit
        html_parts = []
        
        for category in structure:
            html_parts.append(f'<div class="nav-category">')
            html_parts.append(f'<div class="nav-category-title">{category["name"]}</div>')
            
            for page in category["pages"]:
                page_url = f'{category["name"]}/{page["name"]}.html'
                active_class = ' active' if current_page == page_url else ''
                html_parts.append(f'<a href="/{page_url}" class="nav-link{active_class}">{page["name"]}</a>')
            
            html_parts.append('</div>')
        
        return '\n'.join(html_parts)
    
    def build(self):
        # The build itself
        print("🥘 Risotto - Building documentation site...")
        
        # Scan documentation structure
        structure, home_page_path = self.scan_docs()
        
        # Create output directory
        self.output_dir.mkdir(exist_ok=True)
        
        # Process the home page (Fuck the ones who say they don't need one, it is required!)
        if home_page_path:
            print(f"  Processing home page: {home_page_path.name}")
            with open(home_page_path, 'r', encoding='utf-8') as f:
                md_content = f.read()
            
            html_content = MarkdownParser.parse(md_content)
            nav_html = self.generate_nav_html(structure, "")
            
            # Extract title and other shit
            title_match = re.search(r'<h1>(.*?)</h1>', html_content)
            title = title_match.group(1) if title_match else "Home"
            
            full_html = self.generate_html_template(
                title=title,
                content=html_content,
                nav_html=nav_html,
                current_page=""
            )
            
            with open(self.output_dir / "index.html", 'w', encoding='utf-8') as f:
                f.write(full_html)
            
            print(f"  ✓ Generated index.html")
        else:
            print(f"  ⚠ No home page found (looking for '{self.config.get('home_page')}' in docs/)")
        
        # Process each category page
        page_count = 0
        for category in structure:
            cat_dir = self.output_dir / category["name"]
            cat_dir.mkdir(exist_ok=True)
            
            for page in category["pages"]:
                with open(page["path"], 'r', encoding='utf-8') as f:
                    md_content = f.read()
                
                html_content = MarkdownParser.parse(md_content)
                
                page_url = f'{category["name"]}/{page["name"]}.html'
                nav_html = self.generate_nav_html(structure, page_url)
                
                title_match = re.search(r'<h1>(.*?)</h1>', html_content)
                title = title_match.group(1) if title_match else page["name"]
                
                full_html = self.generate_html_template(
                    title=title,
                    content=html_content,
                    nav_html=nav_html,
                    current_page=page_url
                )
                
                output_path = cat_dir / f'{page["name"]}.html'
                with open(output_path, 'w', encoding='utf-8') as f:
                    f.write(full_html)
                
                page_count += 1
                print(f"  ✓ Generated {page_url}")
        
        print(f"\nDone! Generated home page + {page_count} pages in '{self.output_dir}'")
        print(f"Open {self.output_dir}/index.html in your browser!")


def main():
    # If you read this you probably wanted to check if this code is even quality. It is probably just garbage....
    parser = argparse.ArgumentParser(description="Risotto - Static documentation generator")
    parser.add_argument("--docs", default="docs", help="Documentation source directory")
    parser.add_argument("--config", default="config.risotto", help="Configuration file")
    
    args = parser.parse_args()
    
    generator = RisottoGenerator(docs_dir=args.docs, config_path=args.config)
    generator.build()


if __name__ == "__main__":
    main()
