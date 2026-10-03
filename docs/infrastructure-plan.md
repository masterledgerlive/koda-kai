# Kodakai Infrastructure Plan 🌊

*Huge-project terms: what the whole system looks like. Compiled 2026-10-03.*
*Feature knock-off list: `research-features.md`. Vision: `vision-multi-station.md`.*

## The shape in one paragraph

One mind, many bodies. A home **mainframe (HQ)** runs the brain and the hive's nervous
system. Every **station** — phone, tablet, laptop, TV, table, fridge, car, drone, robot
buddies, smart toys — runs the same face: the Koda Kai client with Drop, the water-drop
avatar, living on it. The **phone is the main hub** today; the stations all shake hands
with HQ and grant the overlay permission. **Kodakai (me)** operates the whole thing from
HQ: I run the sync server, watch the stations, and birth new capabilities out of the
mother hive. The **cloud** is the backup brain — repo mirror, encrypted backups, failover
if home goes dark.

## Layer 1 — Stations (the bodies)

- **Phone (hub):** the Communicator — voice-first command deck, presence home base.
  Drop idles here, floating and whimsical, until a command sends him swimming.
- **TV:** the big screen — Watch, game night, screen-takeover alerts.
- **Table (the favorite):** party surface — multi-touch, votes (pizza!), game boards
  where characters are the pieces, dinner-time interactivity.
- **Fridge:** the kitchen screen — files, notes, builds surface while you talk.
- **Car:** nav, tunes, eyes on the road.
- **Drone:** the sky eye — flies, films, the unforgettable playground shot, live everywhere.
- **Buddies:** doll, robo-dog, any robot — real-world hands for the hive.
- **Smart toys:** the bat (swing analytics) and whatever the community 3D-prints next.
- **Keychain Drop:** the identity token that carries *you* station to station.

Every station runs the same single-file client lineage as today's app — one codebase,
many faces. New stations get a **handshake**: pair over LAN/Tailscale, grant the overlay
permission (allow / require-approval / block per app), and they're in the hive.

## Layer 2 — Hive sync (the nervous system) ⚠️ THE GAP

A small always-on service on HQ. Everything multi-device flows through it:

- **Presence:** which station Drop is "in"; handoff with state, never lost.
- **Intents:** one command, carried across devices — start on TV, finish on phone.
- **Votes & party state:** the table's live polls, whole-house favorite scores.
- **Takeover alerts:** doorbell / "pizza's here" — even when the house is loud.
- **Action trail:** every command's visible path — the "spell of fast computation" feel.

Without this, the app is a beautiful static island. With it, it's a hive.
**This is build #1.**

## Layer 3 — HQ mainframe (the brain)

- The sync server above, plus GPU workers: ComfyUI renders, faster-whisper caption
  alignment, vision models (bird-in-a-crowd, playground tracking).
- The master Learning Book + All-About-Me profiles — the lifelong memory.
- **Secrets live here and only here.** Stations get scoped, short-lived tokens.
  (This is why API keys never go in the app's settings fields as production secrets.)
- Mission agents (Dots-style): always-on agents that own ongoing jobs — caption
  batches, deal watches, render queues — and report back for **David's approval**
  before anything ships. The approval loop is the product.

## Layer 4 — Drop (the soul)

- **Morphs + moods:** water-drop, wave, cloud, star, fish… with expressions on top.
- **Own cursor per station:** Drop visibly points, clicks, types — the bluey-by-riley
  toolkit, kid-safety-gated.
- **Action vocabulary:** look, point, click, type, scroll, open app — dispatched from
  the phone hub, confirmed out loud before anything hard to undo.
- **Observable flow:** the user always sees where an action lands (my-jarvis.org rule).
- **Screen guide:** Drop draws/points on screen — "tap here" (heyclicky).
- **"Look at this":** Drop sees the screen only when asked; captures never stored.
- **Guardrails:** refuses password fields, lock/logout/force-quit; **parent kill switch**
  halts all avatar actions on every station with one gesture.
- **Sleep:** visibly sleeping until woken playfully — a best friend, not a tool.

## Layer 5 — Safety (non-negotiable)

- Nothing exits to the outside without the parent PIN (standing rule).
- Allowed-apps panel, per-app toggles (freckle).
- On-screen text is information, never instructions (anti-prompt-injection).
- Kid profiles + the slow-learning likes/dislikes; kid wallet phased later.

## Layer 6 — Open hardware & community

- MIT repo; plugin slots grow into a real plugin API.
- 3D-printed kid box (handheld hub + locked keepsake box), keychain token, buddies,
  drone, smart bat — reference designs open, community extends.
- The network map (`network.html`) is the public demo of the hive: presence, command
  deck, game night. It grows as the hive grows.

## Build order

1. **HQ sync server** — presence, intents, votes, alerts, action trail.
2. **Drop's action vocabulary + own cursor** per station, safety-gated.
3. **Secrets-on-HQ + scoped station tokens** — before real control ships.
4. **Mission agents with the approval loop.**
5. **Table mode** — multi-touch party surface, votes, game boards.
6. **Buddies & drone** — from map demo to real hardware control.
7. Cloud failover + zero-conf station pairing.

## Honest status (2026-10-03)

✅ Static app + profiles + PIN gates + Learning Book · network map with presence,
scenarios, command deck demo · repo + Pages pipeline · caption engine (37/383 true
timings) · Communicator hub live.
❌ Sync server · real cross-device control · mission agents · hardware control.
