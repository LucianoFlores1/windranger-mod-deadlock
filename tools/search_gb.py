import requests

# GameBanana search API
url = "https://gamebanana.com/apiv11/Util/Search/Results"
params = {
    "_sSearchString": "Windranger Grey Talon",
    "_nPerpage": 10
}
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

r = requests.get(url, params=params, headers=headers)
print("Status:", r.status_code)
try:
    data = r.json()
    for item in data.get('_aRecords', []):
        print(f"ID: {item.get('_idRow')}, Name: {item.get('_sName')}, Model: {item.get('_sModelName')}")
except Exception as e:
    print("Error:", e, r.text[:300])
