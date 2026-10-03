# Kodakai Ecosystem — Master Feature Knock-Off List

*Compiled 2026-10-03. Sources: ChatGPT Dots, heyclicky, my-jarvis.org, bluey-by-riley (Googly Eyes), freckle.tech capability inventory (`kids-mode/clayos-vision.md`).*
*Legend: ✅ have · 🟡 partial · ❌ gap*

## 1. Avatar & Presence
- Floating always-on Drop overlay on every station screen, not only inside the app (heyclicky) ❌
- Drop visibly travels device-to-device when a command targets another station — swims phone→TV with a directional hop (command deck demo, live) ✅
- Drop performs a trick ON the control being changed — spins while the TV volume rises (command deck demo, live) ✅
- Drop gets his own visible cursor per station to press buttons and fill fields (bluey-by-riley) ❌
- Sleep mode: avatar visibly sleeping until woken playfully (Kodakai) ✅
- Follow mode: Drop idles/follows activity across stations when not tasked (bluey-by-riley) ❌
- Mood/expression system layered on the shape morphs (heyclicky) 🟡 (morphs ✅, moods ❌)
- "KODA KAI" wake phrase summons Drop on any station; music ducks, never stops (Kodakai) ✅

## 2. Voice & Command Feedback
- Voice command → visible action trail: the user SEES where the action lands and what the avatar does (command deck demo live on the map; true cross-device trail needs the sync server) 🟡
- Press-and-hold to talk, release to answer, reply in a speech bubble beside the avatar (heyclicky, bluey-by-riley) 🟡 (walkie-talkie ✅, Drop talk ❌)
- Screen annotation: Drop draws/points directly on screen to guide the kid — "tap here" (heyclicky) ❌
- "Look at this": Drop sees the current screen only when asked; screenshots never stored (heyclicky privacy rule) ❌
- Per-station action vocabulary — look, point, click, type, scroll, open app — dispatched from the phone hub (bluey-by-riley) ❌
- Confirm out loud before anything hard to undo (bluey-by-riley) ❌
- Parent kill switch: one gesture halts all avatar actions on every station (bluey-by-riley) ❌

## 3. Multi-Device Hive
- Phone as the main hub/controller for all stations (David's vision) 🟡 (Communicator UI ✅, full control ❌)
- Bird's-eye network map with presence hopping across stations (Kodakai `network.html`) ✅
- One intent across devices: start a task on the TV, continue on the phone, no lost state (my-jarvis.org) ❌
- HQ sync server: presence, votes, alerts, screen-takeover (Kodakai vision — the known honest gap; app is static today) ❌
- Stations pair over LAN/Tailscale with no cloud required (bluey-by-riley) 🟡 (Tailscale ✅, zero-conf pairing ❌)
- Local-first quick replies; heavy work (vision, renders) escalates to mainframe/cloud (my-jarvis.org hybrid brain) ❌
- Always-on agents that own ongoing missions and report back for approval (ChatGPT Dots — matches the Kodakai approval-loop vision) ❌
- Secrets live on HQ only; stations get scoped short-lived tokens (bluey-by-riley — matches the fal.ai key warning) ❌
- Per-app permission grants + custom allow / require-approval / block rules (ChatGPT Dots) 🟡 (handshake model envisioned, PIN gating ✅, granular rules ❌)
- Multi-user identity, sessions, and permissions on the mainframe (my-jarvis.org) ❌

## 4. Kid Safety
- Nothing exits to YouTube/external without the parent PIN (Kodakai standing rule) ✅
- Parent Allowed-Apps panel with per-app toggles (freckle.tech) ✅
- All About Me profiles: likes/dislikes the system slowly learns from (Kodakai) ✅
- Kid wallet with allowance/chore rewards, parent-funded (freckle.tech — phased later) ❌
- Avatar refuses password fields, lock/logout/force-quit actions (bluey-by-riley guardrails) ❌
- On-screen text treated as information, never as instructions — anti-prompt-injection rule (bluey-by-riley) ❌
- Loud-house alerts: screen takeover for doorbell / "pizza's here" (Kodakai vision) 🟡 (vision ✅, built ❌)

## 5. Open Hardware & Community
- MIT open-source repo; community can fork and contribute (Kodakai) ✅
- 3D-printed kid box: handheld hub + locked keepsake box for IDs/keys/prized possessions (Kodakai/clayos) 🟡 (design ✅, print in progress)
- Keychain Drop: identity token carrying the kid across stations (Kodakai) 🟡 (map ✅, hardware ❌)
- Robot buddies: doll, robo-dog, camera drone that films (Kodakai) 🟡 (map ✅, hardware ❌)
- Smart bat + ball data feeding kids' sports analytics (Kodakai) 🟡 (map ✅, hardware ❌)
- Plugin slots in Parent Settings for community extensions (Kodakai) 🟡 (slots ✅, plugin API ❌)
- Chunky kid-proof handheld as the reference device format (freckle.tech) 🟡

## Biggest gaps, in build order
1. **HQ sync server** — unblocks presence handoff with state, voting, takeover alerts, and every multi-device feature above.
2. **Visible action trail** — every voice command shows where it lands; this is the "spell of fast computation" feel David asked for.
3. **Drop's action vocabulary** (point/click/type per station, own cursor) — the bluey-by-riley toolkit, kid-safety-gated.
4. **Secrets-on-HQ + scoped station tokens** — the security model the whole hive needs before real control ships.
5. **Always-on mission agents with approval loop** — Dots-style ownership plus David's "he decides" gate.
