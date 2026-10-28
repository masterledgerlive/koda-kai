#!/usr/bin/env python3
"""
Historian -> God's Eye View history-layer feed adapter.

Reads the historian seed records (schema v1, ~/workspace/koda-kai-historian/timeline/seed/*.json)
and emits ONE feed file in the shape the God's Eye View history layer consumes
(same field family as map-feed/globe-prototype-data.json, extended with the
full evidence trail so nothing on the map loses its receipts).

Rules enforced here (HISTORIAN-DOCTRINE.md + TIMELINE-WORLDMAP-VISION.md):
- No record without sources enters the feed.
- No record without a real lat/lon is pinned. Unpinned records are counted
  and listed, never given invented coordinates.
- Evidence grade drives visual weight and layer:
    VERIFIED / CORROBORATED / CLAIMED -> layer "real"
    DEBUNKED                           -> layer "fake"   (kept visible, with refutation)
    SPECULATION                        -> layer "whatif" (never presented as fact)
  Compound/split grades keep their full raw text in `grade_raw`; the base
  grade is the first grade token and decides weight/layer.
- Media stays exactly where the record places it; reconstructions stay
  labeled as reconstructions (carried through untouched).

Usage: python3 build-history-feed.py
Output: ../feed/history-feed.json  (+ a summary on stdout)
"""
import json
import glob
import os
import re
import sys
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
SEED_DIR = os.path.expanduser("~/workspace/koda-kai-historian/timeline/seed")
OUT = os.path.join(HERE, "..", "feed", "history-feed.json")

WEIGHT = {
    "VERIFIED": 1.0,
    "CORROBORATED": 0.75,
    "CLAIMED": 0.5,
    "DEBUNKED": 0.6,   # refuted, but the refutation must be findable on the map
    "SPECULATION": 0.3,
    "UNVERIFIABLE": 0.2,
}
LAYER = {
    "VERIFIED": "real",
    "CORROBORATED": "real",
    "CLAIMED": "real",
    "UNVERIFIABLE": "real",
    "DEBUNKED": "fake",
    "SPECULATION": "whatif",
}
GRADE_TOKEN = re.compile(r"VERIFIED|CORROBORATED|CLAIMED|SPECULATION|DEBUNKED|UNVERIFIABLE")


def parse_year(value):
    """Seed dates: '-2100' (BCE), '1621', '1621-09-21', '1884-10'. Year or None."""
    if value is None:
        return None
    s = str(value).strip()
    m = re.match(r"^(-?\d{1,6})", s)
    if not m:
        return None
    try:
        return int(m.group(1))
    except ValueError:
        return None


def base_grade(raw):
    if not raw:
        return None
    m = GRADE_TOKEN.search(str(raw))
    return m.group(0) if m else None


def main():
    files = sorted(glob.glob(os.path.join(SEED_DIR, "*.json")))
    feed, unpinned, sourceless = [], [], []
    for path in files:
        with open(path) as fh:
            rec = json.load(fh)
        if not rec.get("sources"):
            sourceless.append(rec.get("id", os.path.basename(path)))
            continue
        geo = rec.get("geo") or {}
        lat, lon = geo.get("lat"), geo.get("lon")
        # 85 seed records use lat=0/lon=0 as a PLACEHOLDER for "no location"
        # (precision unknown/none, e.g. "N/A (telling, not an event)").
        # 0,0 is in the Gulf of Guinea — pinning them there would fabricate
        # geography, so placeholders count as unpinned, same as missing geo.
        if (lat is None or lon is None or (lat == 0 and lon == 0)
                or not isinstance(lat, (int, float)) or not isinstance(lon, (int, float))
                or not (-90 <= lat <= 90) or not (-180 <= lon <= 180)):
            unpinned.append(rec.get("id", os.path.basename(path)))
            continue
        grade = base_grade(rec.get("evidence_grade"))
        year_start = parse_year(rec.get("date_earliest"))
        year_end = parse_year(rec.get("date_latest")) or year_start
        feed.append({
            "id": rec.get("id"),
            "title": rec.get("title"),
            "claim": rec.get("claim"),
            "tracks": rec.get("tracks", []),
            "year": year_start,
            "year_end": year_end,
            "date_earliest": rec.get("date_earliest"),
            "date_latest": rec.get("date_latest"),
            "date_confidence": rec.get("date_confidence"),
            "lat": lat,
            "lon": lon,
            "place": geo.get("place_name"),
            "geo_precision": geo.get("precision"),
            "geo_anchor": geo.get("anchor"),
            "grade": grade,
            "grade_raw": rec.get("evidence_grade"),
            "grade_reason": rec.get("grade_reason"),
            "weight": WEIGHT.get(grade, 0.2),
            "layer": LAYER.get(grade, "real"),
            "earliest_attestation": rec.get("earliest_attestation"),
            "sources": rec.get("sources", []),
            "media": rec.get("media", []),
            "competing_hypotheses": rec.get("competing_hypotheses", []),
            "falsifiability": rec.get("falsifiability"),
            "status": rec.get("status", "active"),
        })
    feed.sort(key=lambda r: (r["year"] is None, r["year"] or 0))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w") as fh:
        json.dump(feed, fh, ensure_ascii=False, indent=1)
    print(f"seed files:        {len(files)}")
    print(f"feed records:      {len(feed)}")
    print(f"unpinned (no geo): {len(unpinned)}  -> listed in feed build log, never invented")
    print(f"sourceless:        {len(sourceless)}")
    print("by grade:", dict(Counter(r["grade"] for r in feed)))
    print("by layer:", dict(Counter(r["layer"] for r in feed)))
    years = [r["year"] for r in feed if r["year"] is not None]
    print(f"year span:         {min(years)} .. {max(years)}")
    print("unpinned ids:", ", ".join(unpinned[:10]), "..." if len(unpinned) > 10 else "")
    print(f"wrote: {os.path.normpath(OUT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
