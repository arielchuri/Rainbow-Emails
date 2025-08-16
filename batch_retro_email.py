#!/usr/bin/env python3
"""
Batch Retro Email Generator
Processes multiple recipients from a text file, prompts for personalized content,
and creates email drafts or sends emails.

Usage: python3 batch_retro_email.py "Subject Line" recipients.txt [--send|--drafts]
"""

import sys
import subprocess
import tempfile
import webbrowser
from pathlib import Path
import argparse
from urllib.parse import quote
from retro_email import process_markdown_to_retro_html

def read_recipients(file_path):
    """Read email addresses from text file (one per line)."""
    recipients = []
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            email = line.strip()
            if email and '@' in email:  # Basic email validation
                recipients.append(email)
    return recipients

def get_personalized_content(recipient):
    """Prompt user for personalized content for a specific recipient."""
    print(f"\n📧 Recipient: {recipient}")
    print("Enter personalized content (supports markdown - **bold**, *italic*, [links](url)):")
    print("Press Enter twice to finish, or 'skip' to use no personalization:")
    
    lines = []
    empty_count = 0
    
    while empty_count < 2:
        try:
            line = input()
            if line.lower().strip() == 'skip':
                return None
            if line == '':
                empty_count += 1
            else:
                empty_count = 0
            lines.append(line)
        except KeyboardInterrupt:
            print("\n❌ Batch processing cancelled")
            sys.exit(1)
    
    # Remove trailing empty lines
    while lines and lines[-1] == '':
        lines.pop()
    
    content = '\n'.join(lines).strip()
    return content if content else None

def create_email_draft(recipient, html_content, subject="Update from Ariel"):
    """Create email draft using mailto URL."""
    # Create mailto URL with HTML content
    # Note: Most email clients don't support HTML in mailto, so we'll use a different approach
    
    # For now, we'll open the email client with recipient and subject
    # The user will need to paste the HTML content manually
    mailto_url = f"mailto:{recipient}?subject={quote(subject)}"
    
    print(f"🔗 Opening email client for {recipient}...")
    print("📋 HTML content is in clipboard - paste with Ctrl+V")
    
    try:
        # Try to open default email client
        if sys.platform.startswith('linux'):
            subprocess.run(['xdg-open', mailto_url])
        elif sys.platform.startswith('darwin'):  # macOS
            subprocess.run(['open', mailto_url])
        elif sys.platform.startswith('win'):  # Windows
            subprocess.run(['start', mailto_url], shell=True)
        else:
            print(f"Mailto URL: {mailto_url}")
    except Exception as e:
        print(f"Could not open email client automatically: {e}")
        print(f"Manual mailto URL: {mailto_url}")

def copy_html_to_clipboard(html_content):
    """Copy HTML content to clipboard."""
    try:
        process = subprocess.Popen(
            ['wl-copy', '--type', 'text/html'],
            stdin=subprocess.PIPE,
            text=True
        )
        process.communicate(input=html_content)
        return process.returncode == 0
    except Exception:
        return False

def send_email_betterbird(recipient, subject, html_content):
    """Send email using Betterbird/Thunderbird compose window with HTML body."""
    import time
    
    try:
        # Copy HTML to clipboard
        copy_html_to_clipboard(html_content)
        
        # Try Betterbird first, then Thunderbird
        for client in ['betterbird', 'thunderbird']:
            try:
                # Open compose window
                cmd = [
                    client,
                    '-compose',
                    f'to={recipient},subject={subject},format=html'
                ]
                subprocess.run(cmd, check=True)
                print(f"📧 Opened {client.title()} compose window for {recipient}")
                
                # Wait for compose window to open
                time.sleep(3)
                
                # Navigate to message body and paste HTML content
                try:
                    # Switch to US layout, paste, then back to Dvorak
                    subprocess.run(['setxkbmap', 'us'], check=True)
                    time.sleep(0.1)
                    subprocess.run(['xdotool', 'key', 'ctrl+v'], check=True)
                    time.sleep(0.1)
                    subprocess.run(['setxkbmap', 'us', '-variant', 'dvorak'], check=True)
                    print("✅ HTML content pasted into message body automatically")
                except (subprocess.CalledProcessError, FileNotFoundError):
                    print("💡 xdotool not found - install with: sudo apt install xdotool")
                    print("💡 HTML content is in clipboard - paste with Ctrl+V in message body")
                
                break
            except (subprocess.CalledProcessError, FileNotFoundError):
                continue
        else:
            # Neither client found, fallback to mailto
            raise Exception("Neither Betterbird nor Thunderbird found")
    except Exception as e:
        print(f"Could not open email client: {e}")
        print("💡 Tip: HTML is in clipboard, paste with Ctrl+V in email body")
        # Fallback to mailto
        create_email_draft(recipient, html_content, subject)

def main():
    parser = argparse.ArgumentParser(description='Generate batch retro emails from recipient list')
    parser.add_argument('subject', help='Email subject line')
    parser.add_argument('recipients_file', help='Text file with email addresses (one per line)')
    parser.add_argument('--send', action='store_true', help='Try to send emails directly via email client')
    parser.add_argument('--drafts', action='store_true', help='Create email drafts (default behavior)')
    
    args = parser.parse_args()
    
    # Check if recipients file exists
    recipients_file = Path(args.recipients_file)
    if not recipients_file.exists():
        print(f"❌ Recipients file not found: {recipients_file}")
        return 1
    
    # Check if email-input.md exists
    email_input = Path('./email-input.md')
    if not email_input.exists():
        print("❌ email-input.md not found")
        print("Create this file with your base email content (use {{top}} for personalized content)")
        return 1
    
    # Read recipients
    try:
        recipients = read_recipients(recipients_file)
        if not recipients:
            print("❌ No valid email addresses found in recipients file")
            return 1
    except Exception as e:
        print(f"❌ Error reading recipients file: {e}")
        return 1
    
    print(f"📋 Found {len(recipients)} recipients")
    print("🎮 Starting batch retro email generation...")
    
    # Read base email content
    with open(email_input, 'r', encoding='utf-8') as f:
        base_content = f.read()
    
    processed_count = 0
    
    for i, recipient in enumerate(recipients, 1):
        print(f"\n{'='*60}")
        print(f"Processing {i}/{len(recipients)}: {recipient}")
        print('='*60)
        
        # Get personalized content
        personalized_content = get_personalized_content(recipient)
        
        # Generate HTML
        html_content = process_markdown_to_retro_html(base_content, personalized_content)
        
        # Copy to clipboard
        if copy_html_to_clipboard(html_content):
            print("✅ HTML copied to clipboard")
        else:
            print("⚠️  Could not copy to clipboard")
        
        # Handle email creation/sending
        if args.send:
            send_email_betterbird(recipient, args.subject, html_content)
        else:
            create_email_draft(recipient, html_content, args.subject)
        
        processed_count += 1
        
        # Ask if user wants to continue (except for last recipient)
        if i < len(recipients):
            print(f"\nPress Enter to continue to next recipient, or 'q' to quit...")
            try:
                user_input = input().strip().lower()
                if user_input in ['q', 'quit', 'exit']:
                    break
            except KeyboardInterrupt:
                print("\n❌ Batch processing cancelled")
                break
    
    print(f"\n🎉 Processed {processed_count}/{len(recipients)} recipients")
    return 0

if __name__ == '__main__':
    sys.exit(main())