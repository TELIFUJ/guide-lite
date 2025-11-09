import csv, json, pathlib, os

ROOT = pathlib.Path(__file__).resolve().parents[1]
OUT  = ROOT / "data/games_full.json"

from scripts.providers.provider_snapshot import snapshot_lookup
from scripts.providers.provider_manual import manual_lookup
from scripts.providers.provider_api import api_lookup_by_bgg

NEEDED = ["bgg_id","name","year_published","min_players","max_players",
          "min_playtime","max_playtime","mechanics","categories","thumbnail","image"]

def coverage(d): 
    return sum(1 for k in NEEDED if d.get(k)) / len(NEEDED)

def merge(base, extra):
    if not extra: return base
    out = dict(base)
    def merge_list(a, b):
        aset = set([i.strip() for i in (a or "").split(";") if i.strip()])
        bset = set([i.strip() for i in (b or "").split(";") if i.strip()])
        return ";".join(sorted(aset | bset))
    for k,v in extra.items():
        if k in ("mechanics","categories"):
            out[k] = merge_list(out.get(k,""), v)
        elif not out.get(k) and v:
            out[k] = v
    return out

def fallback(bgg_id, seed):
    for getter in (snapshot_lookup, api_lookup_by_bgg, manual_lookup):
        try:
            extra = getter(bgg_id)
        except Exception:
            extra = None
        seed = merge(seed, extra)
        if coverage(seed) >= 0.8: break
    return seed

def load_ids():
    ids = set()
    for p in [ROOT/"data/snapshots/games_snapshot.csv", ROOT/"data/manual_min.csv"]:
        if p.exists():
            with p.open("r", encoding="utf-8") as f:
                for r in csv.DictReader(f):
                    if r.get("bgg_id"): ids.add(int(r["bgg_id"]))
    return sorted(ids)

def main():
    result = []
    for bid in load_ids():
        item = {"bgg_id": bid}
        item = fallback(bid, item)
        if coverage(item) >= 0.8:
            result.append(item)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(result, ensure_ascii=False, indent=2), "utf-8")
    print(f"OK: {len(result)} items → {OUT}")

if __name__ == "__main__":
    main()
