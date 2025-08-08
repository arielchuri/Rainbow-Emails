A script to make colorful emails.

# Workflow

1. Write your email in the file _email-input.md_ in markdown format or plain text.
2. you can put this in your email: {{top}}. It will be replaced with whatever you want when you run the script.
3. type _python retro_email.py --preview_ in the terminal and it will put the html version of _email-input.md_ in the clipboard and make preview.html so you can see what it looks like. 
  (you may need to type _python3_)
4. If you type _python retro_email.py "Hi **Amy!** Hope you are well."_ it will replace _{{top}}, wherever it is in the file.
