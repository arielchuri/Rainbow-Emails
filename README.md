# Newsletter Setup

Simple, fast-loading email newsletter template for networking and job search.

## Files

- `template.html` - Main template with placeholder variables
- `example.html` - Sample newsletter showing how to use the template
- `generate.py` - Python script to create new newsletters from template

## How to Create a New Newsletter

### Option 1: Manual (Quick)
1. Copy `template.html` to a new file (e.g., `newsletter-2025-02.html`)
2. Replace all `{{PLACEHOLDER}}` variables with your content:
   - `{{NEWSLETTER_TITLE}}` - Newsletter name
   - `{{DATE}}` - Publication date
   - `{{ISSUE_NUMBER}}` - Issue number
   - `{{PERSONAL_NOTE}}` - Optional personal message
   - `{{SECTION_X_TITLE}}` and `{{SECTION_X_CONTENT}}` - Main content sections
   - `{{CTA_TEXT}}` and `{{CTA_LINK}}` - Call to action
   - `{{CONTACT_INFO}}`, `{{PORTFOLIO_LINK}}`, `{{LINKEDIN_LINK}}`, `{{UNSUBSCRIBE_LINK}}` - Footer info

### Option 2: Using Python Script
```bash
python generate.py
```
Follow the prompts to create a new newsletter.

## Design Features

- **Email-optimized**: Inline CSS for maximum compatibility
- **Responsive**: Works on mobile and desktop
- **Fast loading**: Minimal CSS, no external dependencies
- **Accessible**: Good contrast, semantic HTML
- **Brand consistent**: Uses your portfolio's color scheme (deeppink/hotpink accents)

## Adding Images

The template supports several image layouts:

### Full-width featured image:
```html
<div class="image-section">
    <img src="your-image-url.jpg" alt="Description" />
    <p class="image-caption">Optional caption</p>
</div>
```

### Inline image (text wraps around):
```html
<img src="your-image-url.jpg" alt="Description" class="image-inline" />
<p>Your text content here...</p>
```

### Two-column image grid:
```html
<div class="image-grid">
    <div class="image-grid-item">
        <img src="image1.jpg" alt="Description 1" />
        <p class="image-caption">Caption 1</p>
    </div>
    <div class="image-grid-item">
        <img src="image2.jpg" alt="Description 2" />
        <p class="image-caption">Caption 2</p>
    </div>
</div>
```

### Image hosting options:
- **GitHub**: Upload to a public repo and use raw URLs
- **Cloud storage**: Google Drive, Dropbox (with direct links)
- **CDN services**: Imgur, Cloudinary
- **Your website**: Host on your portfolio site

### Best practices:
- Optimize images (keep under 500KB for fast loading)
- Use descriptive alt text for accessibility
- Test in multiple email clients
- Consider fallback text for blocked images

## Customization

The template uses your portfolio's aesthetic:
- Clean typography with system fonts
- Deeppink accent color
- Simple, professional layout
- Personal note section for networking touch
- Responsive image handling