import requests

url = "https://gamebanana.com/apiv11/Util/Search/Results"
headers = {"User-Agent": "Mozilla/5.0"}

for query in ["Windranger", "KoT705", "Windrunner"]:
    r = requests.get(url, params={"_sSearchString": query, "_nPerpage": 10}, headers=headers)
    print(f"=== Query: {query} ===")
    data = r.json()
    for item in data.get('_aRecords', []):
        print(f"ID: {item.get('_idRow')}, Name: {item.get('_sName')}, Model: {item.get('_sModelName')}, Submitter: {item.get('_aSubmitter', {}).get('_sName')}")
