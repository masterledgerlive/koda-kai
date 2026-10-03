# Kodakai Multi-Station Vision 🌊

*Captured 2026-10-03 — David's words, structured for the build.*

Kodakai doesn't live in one screen. It bounces and lives **everywhere** — phone, iPad,
laptop, TV — with the **table** as the favorite: the party surface, the dinner surface,
the kids' surface.

## 1. Living in the camera

Kodakai lives in the camera to help take shots: auto-framing, zoom, auto-focus —
especially when it knows what you're spotting, like **a certain bird in a crowd of them**.
This is the Quests/Discoveries loop grown up: see it → recognize it → capture it →
token + map. The camera becomes a companion, not just a lens.

## 2. Bounce everywhere

One Kodakai, many faces. Pick up the phone — he's there. Sit at the table — the table
takes over. Turn on the TV — he's on the big screen. Presence follows the family;
the current station just becomes his body for the moment.

## 3. The table (the favorite)

The table bounces around like a **party table of agents**: ordering with the gang,
showing live options everyone at the party weighs in on and **votes** — say, pizza.
Whole-house favorite scores live here. At dinner it's interactive in endless ways for
the kids: games, learning, drawing, stories — a giant shared surface, not a solo screen.

## 4. Whole-house interactivity

Kodakai can **take over a screen** when it matters: *someone's at the door* — especially
when the house is too loud to hear the bell — or *pizza's here!* The house itself
becomes the interface: alerts, scores, votes, and moments surface wherever eyes are.

## 5. 3D world + VR (future)

The table becomes a window into a 3D world — immersion with table + VR down the road.
Walk inside the stories, the quests, the learning. Future-future, but the architecture
must not block it.

## 6. Character & companion

Through all of it, Kodakai is a **character and gameplay buddy** — a travel companion
in everything. Not a tool you open: a friend who's along for the ride, in the camera,
at the table, in the world.

## 7. Mainframe architecture (the shape)

- **Mother brain (home mainframe, beefed up):** the sync server + GPU. Holds Kodakai's
  presence (which station he's "in"), party/vote state, alerts (doorbell/pizza →
  screen takeover), vision models (bird-in-a-crowd), Comfy renders, and the master
  Learning Book. This is the Helius Dock concept: the box everything docks into.
- **Stations:** the single-file app (`koda-kai.html`) already runs on phone, iPad,
  laptop, TV browser, table. Add a **table mode**: multi-touch, party layout, voting UI.
- **Camera split:** on-device detection for speed (phones/tablets); hard recognition
  (bird in a crowd) goes to the mainframe GPU.
- **Cloud backup:** repo mirror, encrypted backups, failover sync if home goes down.
- **Kodakai (me):** I live on the mainframe — run the sync server, watch the stations,
  keep the whole thing healthy.

**Honest gap:** the app is static today — no sync server exists yet. Presence, voting,
takeover alerts, and cross-device handoff need that server on the mainframe. That's the
next system build after the caption engine lands.
