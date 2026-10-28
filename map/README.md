# The Map — God's Eye + the true timeline + glasses that see through walls

One map, layered, built in the open by Koda Kai (David Jeffords' historian
system) on top of Bilawal Sidhu's open-source work:

| Layer | What it is | Where it comes from |
|---|---|---|
| **Base globe** | Photorealistic 3D Earth with live public feeds — aircraft, ships, satellites, quakes, fires, public cameras | [bilawalsidhu/gods-eye-view](https://github.com/bilawalsidhu/gods-eye-view) (MIT) — cloned as our base; walkthrough: [God's Eye View Blew Up](https://youtu.be/o_FJ1NIH9yw) |
| **History** | An evidence-graded timeline drawn on the map: **1,186 pinned records, −800,000 → 2026**, every pin carrying its claim, evidence grade, and sources | This repo: `history-feed.json` / `history-feed.kml` / `globe-data.json` |
| **Glasses** | Live poses from phones and Ray-Ban Meta glasses in a scanned room — avatars that turn to skeletons through walls — streamed onto the globe | [bilawalsidhu/see-through-walls](https://github.com/bilawalsidhu/see-through-walls) (MIT) + MultiSet VPS; bridge contract + tested core in this repo |

## The history feed

Generated from the Koda Kai Historian seed (schema v1, one record per claim,
no record without sources) by `build-history-feed.py`:

- **real 846 · fake 321 · whatif 19** — three superposed timelines: the
  evidence-supported record, the debunked claims (kept visible, with their
  refutations attached — a lie with its refutation is worth more than a lie
  quietly deleted), and explicitly labeled speculation.
- Grades: CORROBORATED 577 · VERIFIED 188 · DEBUNKED 321 · CLAIMED 81 ·
  SPECULATION 19. Visual weight follows the grade.
- **108 seed records are deliberately not pinned** — they have no real
  geography (some carry a 0,0 placeholder for "no location"). Coordinates
  are never invented. The map says what it doesn't know.
- `history-feed.kml` loads in Google Earth and in God's Eye View's own
  KML import path; `globe-data.json` is the compact pin set for web globes.

## The glasses bridge

`POSE-CONTRACT.md` is the wire format between a see-through-walls session
(MultiSet VPS poses, ~20 Hz) and the globe's live `glassesLive` layer.
`bridge-core.mjs` is its tested heart (10/10 under `node --test`):
contract validation, local→geo anchor conversion, fail-closed stamping —
an unregistered map passes nothing, and a sender-supplied coordinate is
always recomputed by the bridge, never trusted.

The bright lines, inherited from God's Eye View itself and held by every
layer here: no named-person search, no face recognition, no tracking
anyone who isn't a consenting participant in the session, under a name
they chose. Family and session data stays local by default.

## Flow 1 (phones first)

`FLOW1-RUNBOOK.md` + `flow1-unity-project/` — the prepared Android build of
the multiplayer sample: Unity 6000.3.11f1, MultiSet SDK, the CollisionMesh
layer pre-created, one menu click applying every required Android setting.
`INTEGRATION-PLAN.md` is the full architecture: how the layers stack, the
seed→globe mapping table, the bridge design, and the honest gates.

## Licenses

Our code and docs here: MIT. The history feed is compiled from public
sources; each record names its own sources. Upstream projects keep their
licenses (gods-eye-view code MIT with third-party data carve-outs — see its
DATA_SOURCES.md; the MultiSet Unity SDK is proprietary to MultiSet AI).
