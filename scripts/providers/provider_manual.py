import csv, pathlib
MAN = pathlib.Path(__file__).resolve().parents[2] / "data/manual_min.csv"

def manual_lookup(bgg_id:int):
    if not MAN.exists(): return None
    with MAN.open("r", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if str(bgg_id) == r.get("bgg_id"):
                return r
    return None
