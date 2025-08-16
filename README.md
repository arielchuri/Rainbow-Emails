# Retro Email Generator

Two Python scripts for creating colorful, retro computer-styled HTML emails from Markdown content.
Markdown is converted to colorful HTML for insertion into eMails.
As each eMail is created, you can add a personalized message.

On Linux, Thunderbird can send each one automatically.
Fork this repository and have AI walk you through adapting it to your operating system.

## Setup

### Install Dependencies
```bash
pip install markdown
sudo apt install wl-clipboard  # For clipboard functionality
sudo apt install xdotool       # For batch email automation (optional)
```

### Check Email Clients
For batch processing, install **Thunderbird**.

## Tool 1: Single Email (`retro_email.py`)

### Step-by-Step Instructions

1. **Write your email content**
   - Edit `email-input.md` with your message in Markdown format
   - Use `{{top}}` placeholder where personalized content should go

2. **Basic generation**
   ```bash
   python3 retro_email.py
   ```
   - Converts `email-input.md` to colorful HTML
   - Copies HTML to clipboard automatically
   - Paste into email client with Ctrl+V

3. **With personalized top content**
   ```bash
   python3 retro_email.py "Hi **Sarah**! Hope you're *doing well*."
   ```
   - Replaces `{{top}}` with your personalized message
   - Supports **bold**, *italic*, and [links](url)

4. **Generate preview file**
   ```bash
   python3 retro_email.py --preview
   ```
   - Creates `preview.html` to view in browser
   - Also copies to clipboard

5. **Save to file**
   ```bash
   python3 retro_email.py "Hello!" --save my_email.html
   ```
   - Saves HTML to specified file instead of clipboard

## Tool 2: Batch Processing (`batch_retro_email.py`)

### Step-by-Step Instructions

1. **Create recipient list**
   - Make a text file (e.g., `recipients.txt`) with one email per line:
   ```
   sarah@example.com
   john@company.org
   mary@startup.io
   ```

2. **Prepare base email**
   - Write your template in `email-input.md`
   - Include `{{top}}` where personal content goes

3. **Run batch processor**
   ```bash
   python3 batch_retro_email.py "Subject Line" recipients.txt
   ```

4. **For each recipient, the script will:**
   - Show recipient email address
   - Prompt: "Enter personalized content (supports markdown):"
   - You type personalized message (supports **bold**, *italic*, [links](url))
   - Press Enter twice to finish, or type 'skip' for no personalization
   - Generate HTML and copy to clipboard
   - Open email client with recipient and subject pre-filled
   - Auto-paste HTML content (if xdotool available)
   - Ask if you want to continue to next recipient

5. **Options:**
   ```bash
   # Create drafts (default)
   python3 batch_retro_email.py "Monthly Update" recipients.txt --drafts
   
   # Try to send directly
   python3 batch_retro_email.py "Newsletter" recipients.txt --send
   ```

## Example Files

### email-input.md
```markdown
{{top}}

**Check** out my latest _work_ at [my portfolio](https://example.com).

Carry on,  
Ariel
```

### recipients.txt
```
friend1@example.com
colleague@company.org
contact@startup.io
```

