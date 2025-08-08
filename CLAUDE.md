# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a retro computer-styled email generation system that converts Markdown content from `2025/mynews_*.md` files into HTML emails with colorful retro computer aesthetics. The generated HTML is automatically copied to the clipboard for pasting into email clients.

## Core Commands

### Generate Retro Email (Primary Workflow)
```bash
python3 retro_email.py [top_content]
```

**Quick Usage Examples:**
```bash
# Basic usage - copy to clipboard (always uses ./email-input.md)
python3 retro_email.py

# With top content (supports markdown formatting with rainbow colors)
python3 retro_email.py "Hi **Sarah**! Hope you're *doing well*."

# Generate with preview file for testing
python3 retro_email.py --preview

# Save to file instead of clipboard
python3 retro_email.py "**Update** from [SparkLabs](https://example.com)" --save output.html
```

### Legacy Newsletter System (Deprecated)
```bash
python3 generate_newsletter.py <markdown_file> [-t template.html] [-c constants.md] [-o output.html]
```

### Dependencies
```bash
pip install markdown
sudo apt install wl-clipboard  # For clipboard functionality
```

## Architecture & Structure

### Core Components

1. **Retro Email Generator (`retro_email.py`)**
   - Always uses `./email-input.md` as source file
   - Converts Markdown to retro computer-styled HTML
   - Dynamically assigns random SparkLabs colors to elements
   - Optional top content with markdown formatting and rainbow colors
   - Automatically copies to clipboard via `wl-copy`

2. **Legacy Newsletter System (Deprecated)**
   - `generate_newsletter.py` - Full newsletter template system
   - `template.html` - Master HTML template  
   - `constants.md` - Global configuration defaults

### Key Features

**Retro Computer Aesthetic**:
- Monospace fonts (Courier New, Monaco, Lucida Console)
- Terminal/CRT styling with scan lines effect
- Random SparkLabs colors for borders, text highlights, and links
- ASCII art decorative borders
- Glowing text effects and blinking cursor

**Dynamic Color System**: Each generation applies random colors from SparkLabs palette:
- `#ec5999` (dragonfruit), `#ff595e` (fire), `#f7802b` (mandarin)
- `#ffca3a` (gold), `#8ac926` (leaf), `#1aa5c4` (aqua)
- `#21a9f5` (sky), `#7f5fad` (plum)

**Workflow Integration**: 
- Processes `{{top}}` placeholders in markdown
- Always uses `./email-input.md` as source file
- Optional top content parameter with markdown support
- Direct clipboard integration for email clients
- Optional preview generation for testing

### File Organization

```
/
├── retro_email.py          # Main retro email generator
├── email-input.md         # Fixed source file (always used)
├── preview.html           # Generated preview (optional)
└── [DEPRECATED]/          
    ├── generate_newsletter.py
    ├── template.html
    ├── constants.md
    └── 2025/mynews_*.md   # Old email content files
```

## Content Creation Workflow

1. **Edit Source File**: Write content in `./email-input.md`
2. **Use Top Placeholder**: Include `{{top}}` where top content should appear (optional)
3. **Generate Email**: Run `python3 retro_email.py [top_content]`
4. **Paste into Email**: Content is copied to clipboard, paste directly (Ctrl+V)

## Markdown Content Structure

Content files should be simple markdown with:
- `{{top}}` placeholder for top content (optional)
- Standard markdown formatting (links, **bold**, *italic*)  
- No headers needed - content flows naturally
- Personal, conversational tone

Example structure:
```markdown
{{top}}

I have been busy.
I am working on [some project](https://example.com).

Please think of me if you hear about opportunities in **Product Design**.

Carry on,
Ariel Churi
```

**Top Content Examples:**
- `python3 retro_email.py "Hi **Sarah**!"`
- `python3 retro_email.py "**Update** from [SparkLabs](https://example.com)"`
- `python3 retro_email.py "*Quick note* - hope you're doing well!"`