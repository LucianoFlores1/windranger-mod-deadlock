import requests
import os
import zipfile

url = "https://gamebanana.com/dl/1853780"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}

dest_zip = "windranger_gt.zip"
print(f"Downloading from {url}...")

with requests.get(url, headers=headers, stream=True) as r:
    r.raise_for_status()
    total = int(r.headers.get('content-length', 0))
    downloaded = 0
    with open(dest_zip, 'wb') as f:
        for chunk in r.iter_content(chunk_size=65536):
            if chunk:
                f.write(chunk)
                downloaded += len(chunk)
                if total > 0 and downloaded % (1024 * 1024 * 5) < 65536:
                    print(f"Downloaded {downloaded / 1024 / 1024:.1f} MB / {total / 1024 / 1024:.1f} MB")

print("Download complete! File size:", os.path.getsize(dest_zip))

print("Extracting...")
extract_dir = "extracted_mod"
with zipfile.ZipFile(dest_zip, 'r') as zip_ref:
    zip_ref.extractall(extract_dir)

print("Files in extracted zip:")
for root, dirs, files in os.walk(extract_dir):
    for f in files:
        full_path = os.path.join(root, f)
        rel_path = os.path.relpath(full_path, extract_dir)
        print("  ", rel_path, f"({os.path.getsize(full_path):,} bytes)")
