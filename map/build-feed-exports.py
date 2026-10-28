#!/usr/bin/env python3
"""
Feed exports from the historian history feed (feed/history-feed.json):

1) Globe data — the timeline-world-globe artifact's data-asset schema
   (id/title/claim/grade/year/lat/lon/place/layer), written to
   ~/workspace/koda-kai-historian/map-feed/globe-prototype-data.json,
   the exact file the artifact was built to load. The 23-record starter
   set is backed up first and never silently destroyed.
2) KML — for God's Eye View's upstream geoFileImport / GhostMaps-style
   KML ingestion, and any GIS tool. Styles by evidence grade; every
   placemark description carries grade, grade reason, layer, place,
   date span, claim, and source refs — the receipt travels with the pin.

Usage: python3 build-feed-exports.py [--globe] [--kml]   (default: both)
"""
import json
import os
import shutil
import sys
import xml.etree.ElementTree as ET
from xml.sax.saxutils import escape

HERE = os.path.dirname(os.path.abspath(__file__))
FEED = os.path.join(HERE, "..", "feed", "history-feed.json")
KML_OUT = os.path.join(HERE, "..", "feed", "history-feed.kml")
GLOBE = os.path.expanduser(
    "~/workspace/koda-kai-historian/map-feed/globe-prototype-data.json")
GLOBE_BACKUP = os.path.expanduser(
    "~/workspace/koda-kai-historian/map-feed/globe-prototype-data.starter-23.json")

# KML colors are aabbggrr. Weight by grade, hue by layer family.
STYLE = {
    "VERIFIED": ("verified", "ff00c853"),
    "CORROBORATED": ("corroborated", "ff00acc1"),
    "CLAIMED": ("claimed", "ffffb300"),
    "DEBUNKED": ("debunked", "ff2962ff"),
    "SPECULATION": ("speculation", "ffab47bc"),
    "UNVERIFIABLE": ("unverifiable", "ff9e9e9e"),
}


def load_feed():
    with open(FEED) as fh:
        return json.load(fh)


def build_globe(feed):
    if os.path.exists(GLOBE) and not os.path.exists(GLOBE_BACKUP):
        shutil.copy2(GLOBE, GLOBE_BACKUP)
        print(f"starter set backed up -> {GLOBE_BACKUP}")
    out = [{
        "id": r["id"],
        "title": r["title"],
        "claim": r["claim"],
        "grade": r["grade"],
        "year": r["year"],
        "lat": r["lat"],
        "lon": r["lon"],
        "place": r["place"],
        "layer": r["layer"],
    } for r in feed]
    with open(GLOBE, "w") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(f"globe data: {len(out)} records -> {GLOBE}")


def build_kml(feed):
    parts = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<kml xmlns="http://www.opengis.net/kml/2.2">',
        "<Document>",
        "<name>Koda Kai Historian — evidence-graded timeline (history feed)</name>",
        "<description>Every pin carries its evidence grade and sources. "
        "Layers: real / fake (debunked, kept visible with refutation) / "
        "whatif (speculation, labeled). Generated from feed/history-feed.json.</description>",
    ]
    for grade, (style_id, color) in STYLE.items():
        parts.append(
            f'<Style id="{style_id}"><IconStyle><color>{color}</color>'
            f"<scale>1.0</scale></IconStyle>"
            f"<LabelStyle><color>{color}</color></LabelStyle></Style>")
    folders = {"real": [], "fake": [], "whatif": []}
    for r in feed:
        style_id = STYLE.get(r["grade"], STYLE["UNVERIFIABLE"])[0]
        def ref_of(s):
            if isinstance(s, str):
                return s
            if isinstance(s, dict):
                return s.get("ref", "") or s.get("title", "") or ""
            return ""
        sources = "; ".join(
            ref for ref in (ref_of(s) for s in r.get("sources", [])) if ref)
        desc = (
            f"Grade: {r['grade']} — {r.get('grade_reason') or ''}\n"
            f"Layer: {r['layer']} · Place: {r.get('place') or ''}\n"
            f"Dates: {r.get('date_earliest')} → {r.get('date_latest')} "
            f"(confidence: {r.get('date_confidence')})\n\n"
            f"{r.get('claim') or ''}\n\n"
            f"Earliest attestation: {r.get('earliest_attestation') or ''}\n"
            f"Sources: {sources}\n"
            f"Falsifiability: {r.get('falsifiability') or ''}")
        year = r["year"]
        # KML TimeStamp needs ISO; BCE years can't be expressed — use
        # TimeSpan-free placemarks for BCE and stamp CE records by year.
        when = ""
        if year is not None and year >= 1:
            when = f"<TimeStamp><when>{year:04d}-01-01</when></TimeStamp>"
        pm = (
            "<Placemark>"
            f"<name>{escape(r['title'] or r['id'])}</name>"
            f"<description>{escape(desc)}</description>"
            f"<styleUrl>#{style_id}</styleUrl>"
            f"{when}"
            f"<Point><coordinates>{r['lon']},{r['lat']},0</coordinates></Point>"
            f"<ExtendedData>"
            f'<Data name="grade"><value>{escape(r["grade"] or "")}</value></Data>'
            f'<Data name="layer"><value>{escape(r["layer"])}</value></Data>'
            f'<Data name="year"><value>{year}</value></Data>'
            f'<Data name="weight"><value>{r["weight"]}</value></Data>'
            f"</ExtendedData>"
            "</Placemark>")
        folders[r["layer"]].append(pm)
    for layer, label in (("real", "REAL — evidence-supported timeline"),
                         ("fake", "FAKE — debunked, kept with refutation"),
                         ("whatif", "WHAT-IF — speculation, labeled")):
        parts.append(f"<Folder><name>{label} ({len(folders[layer])})</name>")
        parts.extend(folders[layer])
        parts.append("</Folder>")
    parts.append("</Document></kml>")
    text = "\n".join(parts)
    ET.fromstring(text)  # raises if malformed
    with open(KML_OUT, "w") as fh:
        fh.write(text)
    print(f"kml: {sum(len(v) for v in folders.values())} placemarks "
          f"-> {KML_OUT} ({len(text)/1e6:.2f} MB, XML validated)")


if __name__ == "__main__":
    args = sys.argv[1:]
    feed = load_feed()
    if not args or "--globe" in args:
        build_globe(feed)
    if not args or "--kml" in args:
        build_kml(feed)
