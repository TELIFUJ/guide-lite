import csv, pathlib
SNAP = pathlib.Path(__file__).resolve().parents[2] / "data/snapshots/games_snapshot.csv"

def snapshot_lookup(bgg_id:int):
    if not SNAP.exists(): return None
    with SNAP.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if str(bgg_id) == r.get("bgg_id"):
                return r
    return None
