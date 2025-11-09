import os, requests
API_BASE = os.getenv("EXT_API_BASE", "")
API_KEY  = os.getenv("EXT_API_KEY", "")
UA = "PlayClass-GuideLite/1.0 (contact: your_email)"

def api_lookup_by_bgg(bgg_id:int):
    if not API_BASE or not API_KEY: return None
    r = requests.get(f"{API_BASE}/games",
                     params={"bgg_id": bgg_id, "key": API_KEY},
                     headers={"User-Agent": UA}, timeout=20)
    if r.status_code != 200: return None
    data = r.json()
    return data if isinstance(data, dict) else (data[0] if data else None)
