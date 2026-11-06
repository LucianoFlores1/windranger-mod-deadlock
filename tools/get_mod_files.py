import requests
import json

url = "https://gamebanana.com/apiv11/Mod/660434/ProfilePage"
headers = {"User-Agent": "Mozilla/5.0"}
r = requests.get(url, headers=headers)
data = r.json()

print("Mod Name:", data.get('_sName'))
print("Description:", data.get('_sDescription'))
files = data.get('_aFiles', [])
print(f"Files count: {len(files)}")
for f in files:
    print("File:", f.get('_sFile'), "URL:", f.get('_sDownloadUrl'), "Size:", f.get('_nFilesize'))
