import urllib.request
import os
import shutil

downloads = {
    'antarctica.jpg': 'https://images.unsplash.com/photo-1608447714925-599deeb5a682?auto=format&fit=crop&w=800&q=80',
    'northpole.jpg': 'https://images.unsplash.com/photo-1589656966895-2f33e7653819?auto=format&fit=crop&w=800&q=80',
    'supernova.jpg': 'https://images.unsplash.com/photo-1462331940025-496dfbfc7564?auto=format&fit=crop&w=800&q=80',
    'blackhole.jpg': 'https://images.unsplash.com/photo-1614730321146-b6fa6a46bcb4?auto=format&fit=crop&w=800&q=80',
    'bigbang.jpg': 'https://images.unsplash.com/photo-1506318137071-a8e063b4bec0?auto=format&fit=crop&w=800&q=80',
    'indonesia-tsunami.jpg': 'https://images.unsplash.com/photo-1482862549707-f63cb32c5fd9?auto=format&fit=crop&w=800&q=80',
    'haiti-earthquake.jpg': 'https://images.unsplash.com/photo-1594897030264-ab7d87efc473?auto=format&fit=crop&w=800&q=80',
    'katrina.jpg': 'https://images.unsplash.com/photo-1508873699372-7aeab60b44ab?auto=format&fit=crop&w=800&q=80',
    'ocean-pollution.jpg': 'https://images.unsplash.com/photo-1621451537084-482c73073a0f?auto=format&fit=crop&w=800&q=80'
}

static_dir = 'static'
os.makedirs(static_dir, exist_ok=True)

# Copy climatechange.jpg to climate-change.jpg if it exists
src_cc = os.path.join(static_dir, 'climatechange.jpg')
dst_cc = os.path.join(static_dir, 'climate-change.jpg')
if os.path.exists(src_cc):
    try:
        shutil.copyfile(src_cc, dst_cc)
        print("Copied climatechange.jpg to climate-change.jpg")
    except Exception as e:
        print(f"Error copying climatechange: {e}")

# Download each exact image (always overwriting)
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}

for filename, url in downloads.items():
    filepath = os.path.join(static_dir, filename)
    try:
        print(f"Downloading exact image for {filename}...")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(filepath, 'wb') as out_file:
                out_file.write(response.read())
        print(f"Successfully downloaded {filename}")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")

print("Image import run completed!")
