import os
import re

file_path = r"c:\Users\rehan shaikh\Desktop\heartsint-18.html"
with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find all styles
styles = re.findall(r'<style>(.*?)</style>', content, flags=re.DOTALL | re.IGNORECASE)
css_content = "\n".join(s.strip() for s in styles)

with open(r"c:\Users\rehan shaikh\Desktop\style.css", "w", encoding="utf-8") as f:
    f.write(css_content)

# Find all scripts
scripts = re.findall(r'<script>(.*?)</script>', content, flags=re.DOTALL | re.IGNORECASE)
js_content = "\n".join(s.strip() for s in scripts)

with open(r"c:\Users\rehan shaikh\Desktop\script.js", "w", encoding="utf-8") as f:
    f.write(js_content)

# Replace <style>...</style> and <script>...</script>
new_content = re.sub(r'<style>.*?</style>', '', content, flags=re.DOTALL | re.IGNORECASE)
new_content = re.sub(r'<script>.*?</script>', '', new_content, flags=re.DOTALL | re.IGNORECASE)

# Insert external links
new_content = new_content.replace('</head>', '  <link rel="stylesheet" href="style.css">\n</head>')
new_content = new_content.replace('</body>', '<script src="script.js"></script>\n</body>')

# Remove possible empty lines left over from replacement
new_content = re.sub(r'\n\s*\n', '\n', new_content)

# Overwrite the original file or create a new index.html
with open(file_path, "w", encoding="utf-8") as f:
    f.write(new_content)

print("Files created and original file updated successfully!")
