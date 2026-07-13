import urllib.request
import urllib.parse
import json
import os

# Mapping of database filenames to their exact Wikimedia Commons File Titles
file_titles = {
    'haiti-earthquake.jpg': 'Haitian national palace earthquake.jpg',
    'katrina.jpg': 'Katrina 2005-08-28 1700Z.jpg',
    'indonesia-tsunami.jpg': 'Aceh 2004 tsunami standing mosque USGS.jpg',
    'antarctica.jpg': 'AmundsenScottSuedpolStation.jpg',
    'blackhole.jpg': 'Black hole - Messier 87.jpg',
    'bigbang.jpg': 'CMB Timeline300 no WMAP.jpg'
}

static_dir = 'static'
os.makedirs(static_dir, exist_ok=True)

headers = {
    'User-Agent': 'TerraVaultAcademicPlatform/1.0 (https://github.com/Uraj777/TerraVault; contact: rajutkarsh1910@gmail.com) Python-urllib/3.13'
}

def get_wikimedia_direct_url(title):
    """Query the Wikimedia API to get the current direct file URL."""
    api_url = "https://commons.wikimedia.org/w/api.php?action=query&titles=" + urllib.parse.quote("File:" + title) + "&prop=imageinfo&iiprop=url&format=json"
    try:
        req = urllib.request.Request(api_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        pages = data.get('query', {}).get('pages', {})
        for page_id, page_data in pages.items():
            if 'imageinfo' in page_data and len(page_data['imageinfo']) > 0:
                return page_data['imageinfo'][0]['url']
    except Exception as e:
        print(f"API query failed for '{title}': {e}")
    return None

for filename, title in file_titles.items():
    direct_url = get_wikimedia_direct_url(title)
    if not direct_url:
        print(f"Could not find direct URL for '{title}' through Wikimedia API.")
        continue
        
    filepath = os.path.join(static_dir, filename)
    try:
        print(f"Downloading iconic '{filename}' from direct CDN: {direct_url}...")
        req = urllib.request.Request(direct_url, headers=headers)
        with urllib.request.urlopen(req) as response:
            with open(filepath, 'wb') as out_file:
                out_file.write(response.read())
        print(f"Successfully updated '{filename}' with exact iconic image.")
    except Exception as e:
        print(f"Failed to download '{filename}': {e}")

print("Wikimedia download run completed!")
