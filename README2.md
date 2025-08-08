# Retro Email Generator

A Python script that converts Markdown files to colorful, retro-styled HTML emails using SparkLabs design aesthetics. Automatically copies the result to your clipboard for easy pasting into email clients.

## Quick Start

```bash
# Generate email for specific recipient
python3 retro_email.py "Sarah Johnson" 2025/mynews_08-07.md

# Generate with preview file for testing
python3 retro_email.py "Mike Chen" 2025/mynews_08-15.md --preview

# Save to file instead of clipboard
python3 retro_email.py "Alex Rivera" my_message.md --save output.html
```

## Installation

### Dependencies
```bash
pip install markdown
sudo apt install wl-clipboard  # For clipboard functionality
```

### Make Script Executable
```bash
chmod +x retro_email.py
```

## Usage

```
python3 retro_email.py <recipient_name> <markdown_file> [options]
```

**Arguments:**
- `recipient_name` - Name to replace `{{name}}` placeholder in markdown
- `markdown_file` - Path to markdown file to process

**Options:**
- `--preview`, `-p` - Also save as `preview.html` for browser testing
- `--save FILE`, `-s FILE` - Save to specified file instead of clipboard
- `--help`, `-h` - Show help message

## Design Features

### Retro Computer Aesthetic
- **Monospace fonts**: Cross-platform font stack (Consolas, Monaco, Courier New, etc.)
- **SparkLabs colors**: Random color assignment from brand palette
- **Wavy underlines**: Thin wavy underlines that turn solid on hover
- **No backgrounds**: Clean email-friendly styling

### Dynamic Color System
Each email generation randomizes colors from the SparkLabs palette:
- `#ec5999` (dragonfruit) 
- `#ff595e` (fire)
- `#f7802b` (mandarin)
- `#8ac926` (leaf)
- `#1aa5c4` (aqua)
- `#21a9f5` (sky) 
- `#7f5fad` (plum)

**Note**: Yellow/gold colors excluded for better text readability.

### Element Styling
- **Paragraphs**: Each `<p>` gets random SparkLabs color
- **Links**: Random text + underline colors, wavy → solid hover effect
- **Strong text**: Random colors with 600 font weight
- **Emphasis**: Random colors with italic styling  
- **Rules**: Dotted borders in random colors

## Content Structure

### Markdown Format
Create simple markdown files with:
- `{{name}}` placeholder for recipient name
- Standard markdown formatting (`**bold**`, `*italic*`, `[links](url)`)
- Natural paragraph flow (no special headers required)

### Example Content
```markdown
Hi {{name}}! - Hope you are well.

I have been busy working on [exciting project](https://example.com).
The **portfolio** has seen some big updates.

Please think of me if you hear about opportunities in **Product Design**.

Carry on,
Ariel Churi
+1 (646) 490-4576
```

## Workflow

1. **Create markdown file** with your message content
2. **Run the script** with recipient name and file path
3. **Paste into email client** (Ctrl+V) - HTML is already in clipboard
4. **Send** your colorful, personalized email

## Email Client Compatibility

### What Works Everywhere
- Monospace fonts
- Random SparkLabs colors
- Wavy underlines
- Bold and italic text
- Basic styling

### Progressive Enhancement
- **Hover effects**: Work in web browsers, ignored in most email clients
- **Advanced underlines**: Fall back gracefully in older clients
- **Font stack**: Ensures monospace display across platforms

## File Organization

```
/
├── retro_email.py          # Main generator script
├── 2025/                   # Year folder for content
│   ├── mynews_08-07.md    # Email content files
│   └── mynews_08-15.md
├── preview.html           # Generated preview (when using --preview)
└── README2.md            # This documentation
```

## Tips

- **Test first**: Use `--preview` to check styling in browser before sending
- **Batch creation**: Create multiple markdown files for different recipients
- **Color variety**: Each generation creates unique color combinations
- **Personal touch**: Use conversational tone and `{{name}}` placeholder for warmth

## Troubleshooting

**Clipboard not working?**
- Install `wl-clipboard`: `sudo apt install wl-clipboard`
- Use `--save` option as alternative

**Colors look wrong?**
- Check browser/email client support for CSS text decoration
- Preview in different clients to verify appearance

**Font not monospace?**
- Font stack provides fallbacks for different systems
- Most systems will use Consolas, Monaco, or Courier New

**Markdown not converting?**
- Ensure `markdown` package installed: `pip install markdown`
- Check file path and permissions