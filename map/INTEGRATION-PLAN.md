# INTEGRATION PLAN — one map, every layer

*2026-10-26 · Base repos: bilawalsidhu/gods-eye-view @ a3a1988, bilawalsidhu/see-through-walls @ 6feb9da (both MIT, cloned under `../vendor/bilawalsidhu/`)*

## 1. The stack

```
                        ┌─────────────────────────────────────────────┐
  WATCH / EXPLORE  ───► │  GOD'S EYE VIEW globe (Cesium, browser)     │
                        │  upstream layers: flights · ships · sats ·  │
                        │  quakes · fires · CCTV · traffic · weather  │
                        └──────▲──────────────▲──────────────▲────────┘
                               │              │              │
              ┌────────────────┴───┐  ┌───────┴────────┐  ┌──┴───────────────┐
              │ HISTORY layer (new)│  │ GLASSES layer  │  │ SLEUTH layer     │
              │ src/layers/history │  │ glassesLive    │  │ case pins, votes │
              │ historian seed     │  │ MultiSet poses │  │ proof-of-evidence│
              │ 1,186 pinned recs  │  │ Ray-Ban + phone│  │                  │
              └────────────────────┘  └────────────────┘  └──────────────────┘
```

God's Eye View's own architecture is the reason this works cleanly: **every
feed is a separate module under `src/layers/`** (verified in the checkout:
`aircraft/`, `earthquakes/`, `cctv/`, … each with `index.js` / `model.js` /
`source.js` / `records.js`). Our additions follow that exact pattern instead
of forking the globe's core — so upstream upgrades keep merging in, which is
what David asked for ("as everyone has been adding and upgrading all the new
features on top").

## 2. History layer — the true timeline, drawn where the words and pictures put it

**Source of truth:** historian seed records, schema v1
(`~/workspace/koda-kai-historian/timeline/seed/*.json`, 1,294 records) — every
record already carries its claim, sources, earliest attestation, competing
hypotheses, falsifiability line, evidence grade, and geo pin.

**Adapter (built + run 2026-10-26):** `scripts/build-history-feed.py` →
`feed/history-feed.json`. Verified output:

- **1,186 records pinned** — year span **−800,000 → 2026**
- By grade: CORROBORATED 577 · VERIFIED 188 · DEBUNKED 321 · CLAIMED 81 · SPECULATION 19
- By layer: **real 846 · fake 321 · whatif 19**
- **108 records deliberately NOT pinned:** 25 with no geo, 83–85 whose seed geo
  is the 0,0 placeholder for "no location" (a telling, a synthesis argument, a
  hemisphere claim). 0,0 is a real place in the Gulf of Guinea; the map never
  invents geography. (Two region records at 0,−60 for hemisphere-wide Americas
  claims are kept — that's their recorded pin, precision `region`.)
- **0 records dropped for missing sources** — the seed's "no record without
  sources" rule already holds upstream of the adapter.

**Mapping (seed → globe):**

| Seed field | Globe rendering |
|---|---|
| `geo.lat/lon`, `place_name` | Pin exactly there — "by the words on the pages or real pictures": the record's textual/archaeological anchor is the pin; precision (`exact/city/region`) controls the pin's halo, never a silently exact dot |
| `date_earliest/date_latest` | Time-slider span; the record exists on the map only inside its span |
| `evidence_grade` | Visual **weight**: VERIFIED 1.0 · CORROBORATED 0.75 · CLAIMED 0.5 · SPECULATION 0.3 (per TIMELINE-WORLDMAP-VISION: grade = prominence) |
| grade DEBUNKED | `fake` layer — visible in its own color with the refutation attached, never deleted |
| grade SPECULATION | `whatif` layer — counterfactual branches, always labeled speculation |
| `media[]` | Real photos / drawings / reconstructions pinned at the record's geo; `kind` is displayed — a reconstruction is never dressed as a photograph |
| `sources[]`, `earliest_attestation`, `competing_hypotheses`, `falsifiability` | The pin's detail card, verbatim — the receipt travels with the dot |
| `tracks[]` | Filter chips (biblical, ancient-near-east, egypt, philosophy, abrahamic-offshoots, world-history, science-tech) — tracks sit side by side, never force-merged |

**Time behavior:** present-first. At "Now" the globe is God's Eye View live;
scrubbing back fades live feeds out and history in (the existing globe
prototype already proves this interaction with 23 starter records —
`map-feed/globe-prototype-data.json`; the history layer replaces that starter
set with the full 1,186).

**Sleuth feed-in:** a history pin is a sleuth PLACE anchor. Case events pinned
to the same coordinates inherit the place's whole graded past — what is
verified about that ground, what was faked about it, and what would prove a
new claim wrong.

## 3. Glasses layer — see-through-walls as live map data

**What Bilawal built (from the repo README, verified in the checkout):**

- MultiSet VPS: a space is scanned once and uploaded as a **map**; every
  device localizes against that shared map, so all devices agree on one
  coordinate frame.
- Each device streams its **pose** (position + direction) many times a second;
  every participant renders everyone else as an avatar at their real position.
- The map's downloaded 3D mesh + a `CollisionMesh` layer + a raycast decides
  **through-wall**: line-of-sight blocked → avatar becomes a glowing skeleton.
- **Flow 1 — phone ↔ phone** (Unity app, iOS/Android, same Wi-Fi, host IP).
- **Flow 2 — iPhone + Ray-Ban Meta glasses:** glasses don't run Unity; the
  `Multiset-RayBan-Tracking` Xcode companion app (in the repo, Swift) pairs
  with the glasses via Meta's Wearables DAT, streams glasses video to the
  iPhone, localizes it against the MultiSet map (~1 re-localization/sec),
  and forwards the pose to the Unity host at **~20 Hz** over
  MultipeerConnectivity.

**Our bridge (the new work): `glasses-bridge/`**

1. **Map registration.** Each MultiSet map gets a geo anchor record:
   `{ mapCode, origin_lat, origin_lon, origin_alt_m, north_offset_deg,
   registered_by, consent_scope }`. Local MultiSet coordinates (meters,
   Unity frame) rotate by `north_offset_deg` into ENU, then convert to
   lat/lon. Without a registration, poses stay local-only and never touch
   the globe — deliberate fail-closed.
2. **Pose relay.** A small local WebSocket relay accepts pose messages in
   the `POSE-CONTRACT.md` schema (~20 Hz, LAN-first, same network rule as
   upstream) and rebroadcasts to God's Eye View.
3. **`src/layers/glassesLive` (new globe layer).** Renders each session
   participant as a labeled avatar billboard at their geo pose, with a short
   fading trail; `through_wall: true` renders the skeleton style. Session
   area renders as a small local inset (the scanned room) when zoomed in —
   the globe stays truthful about scale.
4. **God's Eye watch mode.** Anyone watching the globe sees the glasses
   session working live — the wearer walking, the skeleton swap through the
   wall — which is David's stated purpose for the layer. **Default: local
   network only.** Any public stream is a separate, per-session,
   exact-word approval from David, with participants' consent recorded in
   the session record.

**What the glasses data also feeds:**

- **Sleuth:** a session is a receipted event — who was where in the scanned
  space, when, with localization quality attached. Poses are evidence-grade
  data (timestamped, sourced, quality-labeled), not vibes.
- **Historian (present-day layer):** consented session recordings become
  present-day records on the timeline's leading edge — real pictures, real
  places, graded like everything else.

## 4. Combined build — both data sets, one test

**David's call 2026-10-26: phones-first (Android / Flow 1)**, Ray-Ban Flow 2
after. Full detail: `FLOW1-RUNBOOK.md`; prepared Unity project:
`flow1-unity-project/`. Test rig: two phones in a scanned room at the house;
the Ray-Bans join in Flow 2 with David's own pair as the test hardware.

- [ ] MultiSet developer account + credentials — **free tier confirmed**
      (developer.multiset.ai, no card, 1,000 localization calls for the life
      of the account; Lite $99/mo only when shipping — not without David's
      word). Credentials entered in the apps / vault, never in chat.
- [ ] Scan a test room with the MultiSet Mapping App (**any ARKit iPhone or
      ARCore Android**, LiDAR optional — David's iPhone can scan) → map
      Active → mapCode; georeference to WGS 84 in the portal if available
      (poses then arrive as GeoPose — the bridge's preferred anchor).
- [ ] Flow 1: two phones, avatar + skeleton swap verified in the room
      (Unity **6000.3.11f1+** — current SDK v1.15.2 floor, supersedes
      Bilawal README's 6000.0.36f1; SDK cloned + sample scene verified).
- [ ] Flow 2: Ray-Bans via companion app (gate list in §5)
- [ ] Pose relay → globe: watch the same session on God's Eye View, avatar
      moving on the photorealistic globe at the house's coordinates
- [ ] Record one session (local only) as the first glasses-layer timeline
      record + sleuth case demo

## 5. Honest gates & blockers (checked, not guessed)

- **Mac required for Flow 2.** `MultisetRayBanTracking` is an Xcode project
  (iOS 17+, Xcode 15+); there is no Windows/Linux build path for it, and the
  Shadow PC is Windows. Flow 1's Unity app also needs a Mac to ship to
  iPhone (Android build from Windows is possible). *Open question for David:
  is there a Mac in the house, or do we start Android/Flow-1-first?*
- **MultiSet credentials required.** No credentials, no localization — the
  apps fail closed. Free developer signup is David's to do (his account).
- **Meta DAT terms.** Flow 2 needs Meta AI app **Developer Mode** on and a
  DAT setup for camera access from the glasses (per the repo README). Our
  earlier research (2026-10-23) found DAT 1.0 stable since 2026-09-30 for
  Ray-Ban Gen 1/2, with iOS companion routes workable via the paired iPhone —
  the repo's companion app is exactly that route.
- **God's Eye View keys are optional at start.** Keyless run = Esri imagery,
  live flights/ships/sats/quakes/cameras included. Photorealistic 3D needs a
  Google Maps key (own key + billing, metered) **or** a Cesium ion token
  (free Community tier, personal/non-commercial). Keys go in the app's
  POWER UP panel, never in chat. No key purchase without David's exact word.
- **License carve-outs ride along.** God's Eye View code is MIT, but bundled
  third-party data is not (e.g. TeleGeography CC BY-NC-SA — non-commercial;
  FL511 Florida CCTV is personal-use-only and off by default). Our layers
  inherit upstream's `DATA_SOURCES.md` attributions intact.
- **Upstream is moving fast** (2,078 commits, #1 GitHub Trending). Our
  checkouts are shallow; before each build session, `git pull` and re-run
  the adapter — the history feed is data, so upstream UI changes can't
  break it.

## 6. Standing gates (all layers)

- Nothing public without David's exact per-item approval.
- Glasses layer: consenting participants only, avatar names they choose,
  no face recognition, no named-person search, no tracking anyone who
  isn't in the session. Family data follows the doctrine's release rule
  (PUBLIC or zero-proof), privacy by default.
- No spend (keys, MultiSet tiers, Unity/Meta fees) without David's exact
  word on the exact item and cost.
