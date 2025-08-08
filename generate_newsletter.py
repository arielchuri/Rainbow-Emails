#!/usr/bin/env python3
"""
Newsletter Generator Script
Converts markdown newsletter content to HTML using the template.
"""

import re
import markdown
from pathlib import Path
import argparse
import yaml
import random

def extract_frontmatter(content):
    """Extract YAML frontmatter from markdown content."""
    frontmatter_pattern = r'^---\s*\n(.*?)\n---\s*\n(.*)'
    match = re.match(frontmatter_pattern, content, re.DOTALL)
    
    if match:
        frontmatter_yaml = match.group(1)
        markdown_content = match.group(2)
        frontmatter = yaml.safe_load(frontmatter_yaml)
        return frontmatter, markdown_content
    else:
        return {}, content

def process_markdown_content(md_content):
    """Convert markdown to HTML and extract sections."""
    # Configure markdown with extensions
    md = markdown.Markdown(extensions=['extra', 'codehilite'])
    html = md.convert(md_content)
    
    # Process images to add proper styling
    import re
    # Replace standalone image paragraphs with styled image sections
    img_pattern = r'<p><img alt="([^"]*)" src="([^"]*)"(?:\s+title="([^"]*)")?\s*/></p>'
    
    def replace_img(match):
        alt_text = match.group(1)
        src = match.group(2)
        title = match.group(3) or alt_text
        return f'''<div class="image-section">
    <img src="{src}" alt="{alt_text}" />
    <p class="image-caption">{title}</p>
</div>'''
    
    html = re.sub(img_pattern, replace_img, html)
    
    # Split content by headers to extract sections
    sections = []
    current_section = {"title": "", "content": ""}
    
    lines = html.split('\n')
    in_section = False
    
    for line in lines:
        if line.startswith('<h1>') or line.startswith('<h2>'):
            if current_section["title"] or current_section["content"]:
                sections.append(current_section)
            
            # Extract title from header tag
            title = re.sub(r'</?h[12]>', '', line)
            current_section = {"title": title, "content": ""}
            in_section = True
        else:
            if in_section:
                current_section["content"] += line + '\n'
    
    # Add the last section
    if current_section["title"] or current_section["content"]:
        sections.append(current_section)
    
    return sections

def get_random_color(text_safe_only=False):
    """Get a single random color from SparkLabs palette."""
    text_safe_colors = [
        'var(--color-dragonfruit)',
        'var(--color-fire)', 
        'var(--color-mandarin)',
        'var(--color-leaf)',
        'var(--color-aqua)',
        'var(--color-sky)',
        'var(--color-plum)'
    ]
    
    all_colors = text_safe_colors + ['var(--color-gold)']
    
    return random.choice(text_safe_colors if text_safe_only else all_colors)

def generate_newsletter(markdown_file, template_file, output_file, constants_file='constants.md'):
    """Generate newsletter HTML from markdown and template."""
    
    # Read constants file first (defaults)
    constants = {}
    constants_path = Path(constants_file)
    if constants_path.exists():
        with open(constants_path, 'r', encoding='utf-8') as f:
            constants_content = f.read()
        constants, _ = extract_frontmatter(constants_content)
    
    # Read the markdown file
    with open(markdown_file, 'r', encoding='utf-8') as f:
        md_content = f.read()
    
    # Extract frontmatter and content
    frontmatter, md_body = extract_frontmatter(md_content)
    
    # Merge constants with frontmatter (frontmatter overrides constants)
    merged_vars = {**constants, **frontmatter}
    
    # Process sections
    sections = process_markdown_content(md_body)
    
    # Read the template
    with open(template_file, 'r', encoding='utf-8') as f:
        template_content = f.read()
    
    # Extract personal note (first section if it starts with "Personal Note")
    personal_note = ""
    content_sections = sections.copy()
    
    if sections and "personal note" in sections[0]["title"].lower():
        personal_note = sections[0]["content"].strip()
        content_sections = sections[1:]
    
    # Prepare replacement values (colors handled separately)
    replacements = {
        'NEWSLETTER_TITLE': merged_vars.get('title', 'Newsletter'),
        'DATE': merged_vars.get('date', ''),
        'PERSONAL_NOTE': personal_note,
        'CONTACT_INFO': merged_vars.get('contact_info', 'Creative Technologist & Design Innovator'),
        'PORTFOLIO_LINK': merged_vars.get('portfolio_link', '#'),
        'LINKEDIN_LINK': merged_vars.get('linkedin_link', '#'),
        'CTA_TEXT': merged_vars.get('cta_text', 'Get In Touch'),
        'CTA_LINK': merged_vars.get('cta_link', 'mailto:hello@example.com'),
        'EMAIL_ADDRESS': merged_vars.get('recipient_email', 'subscriber@example.com')
    }
    
    # Add up to 3 sections
    for i in range(3):
        if i < len(content_sections):
            replacements[f'SECTION_{i+1}_TITLE'] = content_sections[i]['title']
            replacements[f'SECTION_{i+1}_CONTENT'] = content_sections[i]['content'].strip()
        else:
            replacements[f'SECTION_{i+1}_TITLE'] = ''
            replacements[f'SECTION_{i+1}_CONTENT'] = ''
    
    # Replace placeholders in template
    result = template_content
    for key, value in replacements.items():
        result = result.replace('{{' + key + '}}', str(value))
    
    # Replace elements with individual random colors using regex
    import re
    
    # Replace each <hr> with individual random colors
    def replace_hr(match):
        return f'<hr style="border: none; border-bottom: 2px dotted {get_random_color()}; margin: 2rem 0;">'
    result = re.sub(r'<hr>', replace_hr, result)
    
    # Replace each <h1> with individual random color
    def replace_h1(match):
        return match.group(0).replace('{{H1_COLOR}}', get_random_color(text_safe_only=True))
    result = re.sub(r'<h1[^>]*>.*?</h1>', replace_h1, result, flags=re.DOTALL)
    
    # Replace each <h2> with individual random colors
    def replace_h2(match):
        return f'<h2>{match.group(1)}</h2>'.replace('<h2>', f'<h2 style="font-weight: 100; font-size: 2rem; text-transform: uppercase; color: {get_random_color(text_safe_only=True)}; margin-bottom: 1rem;">')
    result = re.sub(r'<h2>(.*?)</h2>', replace_h2, result)
    
    # Replace each <h3> with individual random colors (but preserve inline styles)
    def replace_h3_color(match):
        full_tag = match.group(0)
        if 'style=' in full_tag:
            # Replace color in existing style attribute
            return re.sub(r'color: var\(--color-white\)', f'color: var(--color-white)', full_tag)
        else:
            # Add style attribute with random color
            return full_tag.replace('<h3', f'<h3 style="color: {get_random_color(text_safe_only=True)};"')
    result = re.sub(r'<h3[^>]*>.*?</h3>', replace_h3_color, result, flags=re.DOTALL)
    
    # Replace each <strong> (highlight) with individual random colors  
    def replace_strong(match):
        return f'<strong style="color: {get_random_color(text_safe_only=True)}; font-weight: 600;">{match.group(1)}</strong>'
    result = re.sub(r'<strong>(.*?)</strong>', replace_strong, result)
    
    # Replace each <a> with individual random colors, but make CTA a button
    def replace_link(match):
        href = match.group(1)
        text = match.group(2)
        # Check if this is the CTA link
        if 'Get In Touch' in text or 'Connect & Create' in text:
            return f'<a href="{href}" class="cta" style="background-color: {get_random_color()}; color: var(--color-white); display: inline-block; padding: 0.75rem 1.5rem; text-decoration: none; border-radius: 4px; margin: 1rem 0; text-transform: uppercase; font-weight: 600; letter-spacing: 0.1em;">{text}</a>'
        else:
            return f'<a href="{href}" style="color: {get_random_color(text_safe_only=True)}; text-decoration: underline; text-decoration-style: dotted; text-decoration-color: {get_random_color()};">{text}</a>'
    result = re.sub(r'<a href="([^"]*)"[^>]*>(.*?)</a>', replace_link, result)
    
    # Replace header and footer rules with wavy SVG
    def create_wavy_svg(color):
        # Remove var() wrapper and get hex color
        if 'var(--color-' in color:
            color_name = color.replace('var(--color-', '').replace(')', '')
            color_map = {
                'dragonfruit': '%23ec5999',
                'fire': '%23ff595e', 
                'mandarin': '%23f7802b',
                'gold': '%23ffca3a',
                'leaf': '%238ac926',
                'aqua': '%231aa5c4',
                'sky': '%2321a9f5',
                'plum': '%237f5fad'
            }
            hex_color = color_map.get(color_name, '%23ec5999')
        else:
            hex_color = '%23ec5999'
        
        return f"url(\"data:image/svg+xml,<svg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 100 8'><path d='M0,4 Q5,0 10,4 T20,4 T30,4 T40,4 T50,4 T60,4 T70,4 T80,4 T90,4 T100,4' stroke='{hex_color}' fill='none' stroke-width='2'/></svg>\")"
    
    # Replace header rule with wavy SVG
    header_color = get_random_color()
    result = re.sub(r'border-bottom: 2px dotted {{HEADER_RULE_COLOR}}', 
                   f'border-bottom: none; background-image: {create_wavy_svg(header_color)}; background-repeat: repeat-x; background-position: bottom; background-size: auto 8px', result)
    
    # Replace footer rule with wavy SVG  
    footer_color = get_random_color()
    result = re.sub(r'border-top: 2px dotted {{FOOTER_RULE_COLOR}}', 
                   f'border-top: none; background-image: {create_wavy_svg(footer_color)}; background-repeat: repeat-x; background-position: top; background-size: auto 8px', result)
    
    result = re.sub(r'{{PERSONAL_NOTE_COLOR}}', get_random_color(), result)
    result = re.sub(r'{{CTA_COLOR}}', get_random_color(), result)
    
    # Write the output
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(result)
    
    print(f"Newsletter generated: {output_file}")
    return output_file

def main():
    parser = argparse.ArgumentParser(description='Generate newsletter HTML from markdown')
    parser.add_argument('markdown_file', help='Input markdown file')
    parser.add_argument('-t', '--template', default='template.html', help='Template file (default: template.html)')
    parser.add_argument('-c', '--constants', default='constants.md', help='Constants file (default: constants.md)')
    parser.add_argument('-o', '--output', help='Output HTML file (default: newsletter.html)')
    
    args = parser.parse_args()
    
    # Set default output name based on input
    if not args.output:
        input_path = Path(args.markdown_file)
        args.output = input_path.stem + '_newsletter.html'
    
    # Check if files exist
    if not Path(args.markdown_file).exists():
        print(f"Error: Markdown file '{args.markdown_file}' not found")
        return 1
    
    if not Path(args.template).exists():
        print(f"Error: Template file '{args.template}' not found")
        return 1
    
    try:
        generate_newsletter(args.markdown_file, args.template, args.output, args.constants)
        return 0
    except Exception as e:
        print(f"Error generating newsletter: {e}")
        return 1

if __name__ == '__main__':
    exit(main())