#!/usr/bin/env python3
"""
Rainbow Email Generator
Converts markdown to rainbow computer-styled HTML and copies to clipboard
Usage: python3 rainbow_email.py [top_content]
"""

import sys
import markdown
import subprocess
import random
from pathlib import Path
import argparse

def get_random_sparklab_color():
    """Get a random color from SparkLabs palette."""
    colors = [
        '#ec5999',  # dragonfruit
        '#ff595e',  # fire  
        '#f7802b',  # mandarin
        '#ffca3a',  # gold
        '#8ac926',  # leaf
        '#1aa5c4',  # aqua
        '#21a9f5',  # sky
        '#7f5fad'   # plum
    ]
    return random.choice(colors)

def get_sparklab_colors():
    """Get list of SparkLabs colors with darker variants for text."""
    return [
        '#ec5999',  # dragonfruit
        '#ff595e',  # fire  
        '#f7802b',  # mandarin
        '#6b9c1a',  # leaf (darker green)
        '#1aa5c4',  # aqua
        '#21a9f5',  # sky
        '#7f5fad',  # plum
        '#d4a017'   # darker gold (readable yellow)
    ]

def get_rainbow_styles():
    """Generate CSS for email styling with SparkLabs colors."""
    return '''
<style>
body {
    font-family: 'Consolas', 'Monaco', 'Courier New', 'Liberation Mono', 'DejaVu Sans Mono', 'Bitstream Vera Sans Mono', 'Courier', monospace;
    line-height: 1.6;
    margin: 0;
    padding: 20px;
    font-size: 16px;
    color: #27181f;
}

p {
    margin: 15px 0;
}

hr {
    border: none;
    margin: 2rem 0;
}

strong {
    font-weight: bold;
}

em {
    font-style: italic;
}

a {
    text-decoration: underline;
    text-decoration-style: wavy;
    text-decoration-thickness: 1px;
}

a:hover {
    text-decoration-style: solid !important;
    text-decoration-thickness: 1px !important;
}
</style>
'''

def process_markdown_to_rainbow_html(markdown_content, top_content=None):
    """Convert markdown to styled HTML."""
    # Replace {{top}} placeholder if provided
    if top_content:
        # Convert top_content markdown to HTML for colorization
        md_temp = markdown.Markdown(extensions=['extra'])
        top_html = md_temp.convert(top_content)
        # Remove surrounding <p> tags if present
        top_html = top_html.strip()
        if top_html.startswith('<p>') and top_html.endswith('</p>'):
            top_html = top_html[3:-4]
        
        # Apply rainbow colors to the top content
        colors = get_sparklab_colors()
        
        def colorize_top_content(html_content):
            """Apply rainbow colors to top content elements."""
            import re
            last_color = None
            
            def get_different_color(avoid_color=None):
                available_colors = [c for c in colors if c != avoid_color] if avoid_color else colors
                return random.choice(available_colors)
            
            # Color strong elements
            def replace_strong(match):
                nonlocal last_color
                color = get_different_color(last_color)
                last_color = color
                return f'<span style="color: {color}; font-weight: 600;">{match.group(1)}</span>'
            html_content = re.sub(r'<strong>(.*?)</strong>', replace_strong, html_content)
            
            # Color em elements
            def replace_em(match):
                nonlocal last_color
                color = get_different_color(last_color)
                last_color = color
                return f'<span style="color: {color}; font-style: italic;">{match.group(1)}</span>'
            html_content = re.sub(r'<em>(.*?)</em>', replace_em, html_content)
            
            # Color links
            def replace_link(match):
                nonlocal last_color
                link_color = get_different_color(last_color)
                last_color = link_color
                underline_color = get_different_color(last_color)
                last_color = underline_color
                href = match.group(1)
                text = match.group(2)
                return f'<a href="{href}" style="color: {link_color}; text-decoration: underline; text-decoration-style: wavy; text-decoration-color: {underline_color}; text-decoration-thickness: 1px;">{text}</a>'
            html_content = re.sub(r'<a href="([^"]*)"[^>]*>(.*?)</a>', replace_link, html_content)
            
            # If no special formatting found, apply a random color to the entire content
            if not re.search(r'<(strong|em|a)', html_content):
                color = get_different_color(last_color)
                html_content = f'<span style="color: {color};">{html_content}</span>'
            
            return html_content
        
        top_html = colorize_top_content(top_html)
        markdown_content = markdown_content.replace('{{top}}', top_html)
    else:
        # Remove {{top}} placeholder if no content provided
        markdown_content = markdown_content.replace('{{top}}', '')
    
    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['extra'])
    html_content = md.convert(markdown_content)
    
    # Get components
    styles = get_rainbow_styles()
    colors = get_sparklab_colors()
    
    # Track last used color to avoid repetition
    last_color = None
    
    def get_different_color(avoid_color=None):
        """Get a random color that's different from the last one used."""
        available_colors = [c for c in colors if c != avoid_color] if avoid_color else colors
        return random.choice(available_colors)
    
    # Add random colors to elements similar to generate_newsletter.py
    import re
    
    # Add colored hr elements
    def replace_hr(match):
        nonlocal last_color
        color = get_different_color(last_color)
        last_color = color
        return f'<hr style="border-bottom: 2px dotted {color};">'
    html_content = re.sub(r'<hr>', replace_hr, html_content)
    
    # Add colors to strong elements  
    def replace_strong(match):
        nonlocal last_color
        color = get_different_color(last_color)
        last_color = color
        return f'<strong style="color: {color}; font-weight: 600;">{match.group(1)}</strong>'
    html_content = re.sub(r'<strong>(.*?)</strong>', replace_strong, html_content)
    
    # Add colors to em elements
    def replace_em(match):
        nonlocal last_color
        color = get_different_color(last_color)
        last_color = color
        return f'<em style="color: {color};">{match.group(1)}</em>'
    html_content = re.sub(r'<em>(.*?)</em>', replace_em, html_content)
    
    # Add colors to links with thin wavy underlines
    def replace_link(match):
        nonlocal last_color
        link_color = get_different_color(last_color)
        last_color = link_color
        underline_color = get_different_color(last_color)
        last_color = underline_color
        href = match.group(1)
        text = match.group(2)
        return f'<a href="{href}" style="color: {link_color}; text-decoration: underline; text-decoration-style: wavy; text-decoration-color: {underline_color}; text-decoration-thickness: 1px;">{text}</a>'
    html_content = re.sub(r'<a href="([^"]*)"[^>]*>(.*?)</a>', replace_link, html_content)
    
    # Add random colors to paragraphs
    def replace_paragraph(match):
        nonlocal last_color
        color = get_different_color(last_color)
        last_color = color
        content = match.group(1)
        return f'<p style="color: {color};">{content}</p>'
    html_content = re.sub(r'<p>(.*?)</p>', replace_paragraph, html_content, flags=re.DOTALL)
    
    # Build full HTML
    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email</title>
    {styles}
</head>
<body>
    {html_content}
</body>
</html>'''
    
    return full_html

def copy_to_clipboard(html_content):
    """Copy HTML content to clipboard using wl-copy."""
    try:
        process = subprocess.Popen(
            ['wl-copy', '--type', 'text/html'],
            stdin=subprocess.PIPE,
            text=True
        )
        process.communicate(input=html_content)
        
        if process.returncode == 0:
            print("✓ Rainbow email copied to clipboard!")
            print("✓ Paste into your email client (Ctrl+V)")
        else:
            print("✗ Failed to copy to clipboard")
            return False
    except FileNotFoundError:
        print("✗ wl-copy not found. Install with: sudo apt install wl-clipboard")
        return False
    except Exception as e:
        print(f"✗ Error copying to clipboard: {e}")
        return False
    
    return True

def main():
    parser = argparse.ArgumentParser(description='Generate rainbow computer-styled email from markdown')
    parser.add_argument('top', nargs='?', help='Optional top content (supports markdown formatting)')
    parser.add_argument('--save', '-s', help='Save HTML to file instead of copying to clipboard')
    parser.add_argument('--preview', '-p', action='store_true', help='Also save preview.html for browser testing')
    
    args = parser.parse_args()
    
    # Always use ./email-input.md as source
    md_file = Path('./email-input.md')
    
    if not md_file.exists():
        print(f"✗ Markdown file not found: {md_file}")
        return 1
    
    # Read and process markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Generate rainbow HTML
    html_content = process_markdown_to_rainbow_html(markdown_content, args.top)
    
    # Handle output
    if args.save:
        with open(args.save, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✓ Saved to: {args.save}")
    else:
        # Copy to clipboard
        if not copy_to_clipboard(html_content):
            return 1
    
    # Save preview if requested
    if args.preview:
        with open('preview.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("✓ Preview saved as preview.html")
    
    if args.top:
        print(f"🌈 Rainbow email generated with top content: {args.top[:30]}{'...' if len(args.top) > 30 else ''}")
    else:
        print("🌈 Rainbow email generated")
    return 0

if __name__ == '__main__':
    sys.exit(main())