# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a rainbow computer-styled email generation system that converts Markdown content from `email-input.md` into HTML emails with colorful rainbow computer aesthetics. The system includes both single email generation and batch processing for multiple recipients. The generated HTML is automatically copied to the clipboard for pasting into email clients.

## Core Commands

### Generate Rainbow Email (Primary Workflow)
```bash
python3 rainbow_email.py [top_content]
```

**Quick Usage Examples:**
```bash
# Basic usage - copy to clipboard (always uses ./email-input.md)
python3 rainbow_email.py

# With top content (supports markdown formatting with rainbow colors)
python3 rainbow_email.py "Hi **Sarah**! Hope you're *doing well*."

# Generate with preview file for testing
python3 rainbow_email.py --preview

# Save to file instead of clipboard
python3 rainbow_email.py "**Update** from [SparkLabs](https://example.com)" --save output.html
```

### Batch Rainbow Email Processing
```bash
python3 batch_rainbow_email.py "Subject Line" recipients.txt [--send|--drafts]
```

**Quick Usage Examples:**
```bash
# Create email drafts (default)
python3 batch_rainbow_email.py "Monthly Update" recipients.txt

# Try to send emails directly via Thunderbird
python3 batch_rainbow_email.py "Newsletter" recipients.txt --send
```

### Dependencies
```bash
pip install markdown
sudo apt install wl-clipboard  # For clipboard functionality
sudo apt install xdotool       # For batch email automation (optional)
```

**Email Clients for Batch Processing:**
- Betterbird (preferred) or Thunderbird for automated email sending

## Architecture & Structure

### Core Components

1. **Rainbow Email Generator (`rainbow_email.py`)**
   - Always uses `./email-input.md` as source file
   - Converts Markdown to rainbow computer-styled HTML
   - Dynamically assigns random SparkLabs colors to elements
   - Optional top content with markdown formatting and rainbow colors
   - Automatically copies to clipboard via `wl-copy`

2. **Batch Rainbow Email Processor (`batch_rainbow_email.py`)**
   - Processes multiple recipients from text file
   - Prompts for personalized content per recipient
   - Integrates with Thunderbird/Betterbird for automated sending
   - Supports both draft creation and direct sending
   - Auto-pastes HTML content using xdotool

### Key Features

**Rainbow Computer Aesthetic**:
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
├── rainbow_email.py          # Main rainbow email generator
├── batch_rainbow_email.py    # Batch processing for multiple recipients
├── email-input.md           # Fixed source file (always used)
├── preview.html             # Generated preview (optional)
├── recipients_*.txt         # Email recipient lists (excluded from git)
├── recipients_example.txt   # Example recipient file format
└── archive/                 # Deprecated legacy files
    ├── generate_newsletter.py
    ├── template.html
    └── constants.md
```

## Content Creation Workflow

### Single Email Generation
1. **Edit Source File**: Write content in `./email-input.md`
2. **Use Top Placeholder**: Include `{{top}}` where top content should appear (optional)
3. **Generate Email**: Run `python3 rainbow_email.py [top_content]`
4. **Paste into Email**: Content is copied to clipboard, paste directly (Ctrl+V)

### Batch Email Processing
1. **Create Recipient List**: Make `recipients.txt` with one email per line
2. **Prepare Base Content**: Write template in `./email-input.md` with `{{top}}` placeholder
3. **Run Batch Processor**: `python3 batch_rainbow_email.py "Subject" recipients.txt`
4. **Personalize Each Email**: Script prompts for personalized content per recipient
5. **Email Client Integration**: Automatically opens email client and pastes HTML content

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
- `python3 rainbow_email.py "Hi **Sarah**!"`
- `python3 rainbow_email.py "**Update** from [SparkLabs](https://example.com)"`
- `python3 rainbow_email.py "*Quick note* - hope you're doing well!"`