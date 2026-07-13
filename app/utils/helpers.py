import re
import unicodedata

def slugify(text):
    """Generate a URL-friendly slug from text."""
    if not text:
        return ""
    text = unicodedata.normalize('NFKD', text).encode('ascii', 'ignore').decode('ascii')
    text = re.sub(r'[^\w\s-]', '', text).strip().lower()
    return re.sub(r'[-\s]+', '-', text)

def calculate_reading_time(text):
    """Calculate average reading time in minutes (based on 200 wpm)."""
    if not text:
        return 1
    # Strip HTML tags
    clean_text = re.sub('<[^<]+?>', '', text)
    words = clean_text.split()
    return max(1, round(len(words) / 200))

def generate_toc(html_content):
    """Extract h2 and h3 headings to build a Table of Contents list."""
    if not html_content:
        return []
    # Find h2 and h3 elements
    headings = re.findall(r'<(h[23])>(.*?)</\1>', html_content)
    toc = []
    for tag, content in headings:
        clean_text = re.sub('<[^<]+?>', '', content).strip()
        slug = slugify(clean_text)
        toc.append({
            'tag': tag,
            'text': clean_text,
            'slug': slug
        })
    return toc

def inject_header_ids(html_content):
    """Inject id attributes into h2/h3 elements based on their text content for anchor links."""
    if not html_content:
        return ""
    
    def replace_heading(match):
        tag = match.group(1)
        content = match.group(2)
        clean_text = re.sub('<[^<]+?>', '', content).strip()
        slug = slugify(clean_text)
        return f'<{tag} id="{slug}">{content}</{tag}>'
        
    return re.sub(r'<(h[23])>(.*?)</\1>', replace_heading, html_content)
