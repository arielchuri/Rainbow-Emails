#!/usr/bin/env python3
"""
Rainbow Email Generator
Converts markdown to retro computer-styled HTML using rainbow color sequence
Usage: python3 rainbow_email.py <name> <markdown_file>
"""

import sys
import markdown
import subprocess
from pathlib import Path
import argparse

def get_rainbow_sparklab_colors():
    """Get SparkLabs colors ordered in proper rainbow sequence (ROYGBIV+Pink)."""
    return [
        '#ff595e',  # fire (red)
        '#f7802b',  # mandarin (orange)  
        '#d4a017',  # darker gold (yellow)
        '#6b9c1a',  # leaf (green)
        # '#1aa5c4',  # aqua (blue-green/cyan)
        '#11aea4',  # aqua (blue-green/cyan)
        '#21a9f5',  # sky (blue)
        '#7f5fad',  # plum (violet/purple)
        '#ec5999'   # dragonfruit (pink)
    ]

def get_retro_styles():
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

def process_markdown_to_rainbow_html(markdown_content, recipient_name):
    """Convert markdown to styled HTML with word-by-word rainbow coloring."""
    # Replace {{name}} placeholder
    markdown_content = markdown_content.replace('{{name}}', recipient_name)
    
    # Convert markdown to HTML
    md = markdown.Markdown(extensions=['extra'])
    html_content = md.convert(markdown_content)
    
    # Get components
    styles = get_retro_styles()
    colors = get_rainbow_sparklab_colors()
    
    # Track color position in rainbow sequence
    color_index = 0
    
    def get_next_color():
        """Get the next color in rainbow sequence."""
        nonlocal color_index
        color = colors[color_index % len(colors)]
        color_index += 1
        return color
    
    # Add rainbow colors to elements in sequence
    import re
    
    # Add colored hr elements
    def replace_hr(match):
        color = get_next_color()
        return f'<hr style="border-bottom: 2px dotted {color};">'
    html_content = re.sub(r'<hr>', replace_hr, html_content)
    
    # Remove paragraph color styling - we'll handle text coloring differently
    html_content = re.sub(r'<p[^>]*>', '<p>', html_content)
    
    # Now process ALL elements in sequential rainbow order
    def colorize_all_elements(html_content):
        """Process all text elements (spans, strong, em, links) in rainbow order."""
        import re
        from html.parser import HTMLParser
        
        class RainbowParser(HTMLParser):
            def __init__(self):
                super().__init__()
                self.result = []
                self.tag_stack = []
            
            def handle_starttag(self, tag, attrs):
                if tag == 'strong':
                    color = get_next_color()
                    self.result.append(f'<strong style="color: {color}; font-weight: 600;">')
                    self.tag_stack.append('strong')
                elif tag == 'em':
                    color = get_next_color()
                    self.result.append(f'<em style="color: {color};">')
                    self.tag_stack.append('em')
                elif tag == 'a':
                    # Get href from attrs
                    href = ''
                    for attr_name, attr_value in attrs:
                        if attr_name == 'href':
                            href = attr_value
                            break
                    
                    # Each link element gets only ONE color from the sequence
                    link_color = get_next_color()
                    self.result.append(f'<a href="{href}" style="color: {link_color}; text-decoration: underline; text-decoration-style: wavy; text-decoration-color: {link_color}; text-decoration-thickness: 1px;">')
                    self.tag_stack.append('a')
                else:
                    self.result.append(self.get_starttag_text())
            
            def handle_endtag(self, tag):
                if tag in ['strong', 'em', 'a'] and self.tag_stack and self.tag_stack[-1] == tag:
                    self.tag_stack.pop()
                self.result.append(f'</{tag}>')
            
            def handle_data(self, data):
                if self.tag_stack and self.tag_stack[-1] in ['strong', 'em', 'a']:
                    # Text inside formatted tags - don't wrap in span
                    self.result.append(data)
                else:
                    # Regular text - wrap in colored span
                    if data.strip():  # Only colorize non-empty text
                        color = get_next_color()
                        self.result.append(f'<span style="color: {color};">{data}</span>')
                    else:  # Preserve whitespace as-is
                        self.result.append(data)
        
        parser = RainbowParser()
        parser.feed(html_content)
        return ''.join(parser.result)
    
    html_content = colorize_all_elements(html_content)
    
    # Build full HTML
    full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Rainbow Email</title>
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
            print("🌈 Rainbow email copied to clipboard!")
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
    parser = argparse.ArgumentParser(description='Generate rainbow-sequenced email from markdown')
    parser.add_argument('name', help='Recipient name to replace {{name}} placeholder')
    parser.add_argument('markdown_file', help='Markdown file to process')
    parser.add_argument('--save', '-s', help='Save HTML to file instead of copying to clipboard')
    parser.add_argument('--preview', '-p', action='store_true', help='Also save preview.html for browser testing')
    
    args = parser.parse_args()
    
    # Use specified markdown file
    md_file = Path(args.markdown_file)
    
    if not md_file.exists():
        print(f"✗ Markdown file not found: {md_file}")
        return 1
    
    # Read and process markdown
    with open(md_file, 'r', encoding='utf-8') as f:
        markdown_content = f.read()
    
    # Generate rainbow HTML
    html_content = process_markdown_to_rainbow_html(markdown_content, args.name)
    
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
        with open('rainbow_preview.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        print("🌈 Rainbow preview saved as rainbow_preview.html")
    
    print(f"🌈 Rainbow email generated for: {args.name}")
    return 0

if __name__ == '__main__':
    sys.exit(main())
