# Sprite Runtime 🛰️

*The real build behind "Koda Kai jumps around and does things."*
*David's brief, 2026-10-03: a copy of the program lives on every device; Koda Kai
floats on, becomes it, controls it; the phone sends a little sprite that executes
with visible animation — at Bluey grade.*

## What happened to the phone-controller build

The Shadow "Kodakai Communicator" (port 8098, touch + talk relay) was the
**prototype**: one copy, one machine. It proved the concept. It did not scale —
every new device would need its own custom build.

The sprite runtime is its evolution: **one small program, copied onto every
device**. The GitHub repo held the whole spec (personality, abilities,
infrastructure plan); this is the implementation starting.

## How it works

1. **One script per device.** `sprite/drop-agent.js` — include it on any page and
   that page becomes a *station*. Drop lives there, rendered from the real
   character art (not emoji).
2. **The phone is main communication.** It sends commands over the HQ bus:
   `{to:'tv', from:'phone', type:'cmd', action:'volume-up'}`.
3. **The sprite travels visibly.** A little Drop swims from the sender to the
   target — squash, stretch, arc, landing. You see the trip.
4. **The station executes.** The target's *own* agent runs its action handler —
   volume bar rises, screen plays, bell rings — with animation, then reports home:
   `{to:'phone', type:'done', action:'volume-up', station:'tv'}`.
5. **Nobody fakes it.** The phone never animates the TV. Each station performs
   its own actions. The demo's travel visual and the execution are driven by the
   same bus messages the real deployment uses.

## Transport

- **Today:** `BroadcastChannel('koda-hq')` — real cross-tab messaging, zero server.
- **Tomorrow:** WebSocket to the HQ sync server on Shadow. Same message shape;
  the agents don't get rewritten, the bus gets swapped.

## Bluey grade (the motion bar)

Every move follows the animation principles, applied to the real Drop art:

- **Squash & stretch** — the body deforms along the motion, never slides rigid.
- **Anticipation** — a crouch before every swim, a wind-up before every trick.
- **Follow-through** — landings settle with a soft bounce, never a dead stop.
- **Blink** — the eyes blink on their own timer. He's alive when idle.
- **Reaction beats** — "On it! ✨" before acting, a spin trick after, "Done! ✔"
  to close. Every command is a tiny performance.

This is the floor, not the ceiling. New moves go in the moves list
(`docs/personality-and-abilities.md`); the runtime is where they get performed.

## Demo

`sprite-demo.html` — phone panel sends, sprite swims across, TV station executes
(volume / play / dinner bell) and reports home. Both agents run the real
`drop-agent.js`.

## Build order from here

1. ✅ Sprite runtime + motion system + demo (this)
2. Standalone station pages (`tv.html`, …) for real cross-tab/device proof
3. HQ sync server on Shadow (WebSocket) — presence, intents, action trail
4. Scoped station tokens (security) — stations prove who they are
5. Real device actions behind the demo handlers (actual volume, actual playback)
