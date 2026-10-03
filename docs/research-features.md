# Research Features — Master Knock-Off List 🔍

*Compiled 2026-10-03 from 5 sources. David's brief: "take a list of the research
and all the items everyone has… start knocking off list."*

---

## 1. ChatGPT "Dots" — https://chatgpt.com/features/dots/

*What it is: OpenAI's always-on agents (GPT-6 Astra). You hand a dot a
responsibility; it keeps working between conversations and brings you decisions.*

- Always-on agents that work between conversations, not just when chatted with
- Starts with ChatGPT memory as context
- Uses Codex + connected tools to do real work
- User picks which apps it can access, what it focuses on, how things get done
- Hand over a big project or small chore; it proactively figures out next steps
- Brings work to review + decisions that need human judgment
- See what it's working on; give feedback; change direction; pause anytime
- Works wherever you work: web, mobile, desktop
- Permission tiers: act alone vs needs approval (user decides)
- Built-in protections: defends against malicious instructions, watches for harmful behavior
- Custom Rules: allow specific actions, require approval, or block them
- Auto-review: actions touching accounts/info get checked; password changes stay human-only

## 2. heyclicky — https://www.heyclicky.com/

*What it is: an AI buddy that lives on your Mac. Hotkey → it sees your screen,
you talk out loud, it walks you through anything or runs agents to do it.*

- Hotkey summons; sees what you see (screen capture ONLY on hotkey, never stored)
- Talk out loud — unlimited voice conversation; dictation
- "Agent" mode: actually does tasks for you (counted separately from talk)
- **Draws right ON your screen** to point the way (annotation overlay)
- Teaches you any tool / walks you through whatever you're stuck on
- Works with anything visible — no plugins or integrations needed
- Privacy model: screenshots never stored; only text summaries kept for context; full account+data delete
- Tiered plans: free talk limits / pro unlimited talk / max power-user agent volume

## 3. JARVIS — https://my-jarvis.org/

*What it is: an autonomous assistant with a hybrid local/cloud brain and a
cross-platform control plane (macOS + Android). Intent in → coordinated
execution across devices.*

- Hybrid brain: local models (Qwen 2.5, Gemma via Ollama) for routine; cloud
  (Vertex AI, Gemini, Claude, DeepSeek, OpenRouter) for heavy reasoning
- Cross-platform control plane: observe interface state, operate apps, coordinate
  workflows desktop ↔ mobile without losing intent
- Token-optimized routing: smallest capable model first, deliberate escalation
- Observable flow: identity → context → routing → inference → execution
- Multi-user server: identity, sessions, permissions, execution paths separated
- Secure auth (Google Cloud) + policy-aware routing ("capability never outruns control")
- Structured outputs; API orchestration endpoint (intent → route → reason → act)
- Release center: macOS / Android / Windows builds from one place
- Start a mission on desktop, continue on mobile — shared tasks, notifications, secure handoff

## 4. bluey-by-riley ("Googly Eyes") — https://github.com/rbrown101010/bluey-by-riley

*What it is: a blueberry character on iPhone that lives under your Mac's screen
and points/acts on the Mac with its OWN big cursor. The closest thing to our
sprite dream that actually exists.*

- Character with **its own cursor** on the target screen (separate from your pointer; yours gets restored)
- Double-tap phone to wake/sleep; press-and-hold to talk (push-to-talk); mic-on-for-context but quiet until asked
- Answers as speech bubble next to its cursor + cartoon chirp sound
- "What's this?" → points at whatever is under YOUR mouse
- Follow mode (tracks your mouse) vs session mode
- Phone↔Mac over WebSocket; Mac mints 10-min client secrets — real API key never leaves the Mac
- Tools: look_at_screen (screenshot + vision → text ids), point_at, point_at_spot (grid), stop_pointing, go_to_sleep
- Full computer use: click, type, press keys, scroll, drag, open apps/URLs — visibly, with its own cursor
- Guardrails: acts only when asked; confirms before irreversible; on-screen text = info, never instructions; refuses password fields / logout / lock / force-quit; kill switch; master on/off toggle
- Keyboard shortcuts: fly-to-mouse, follow, go home, talk test, hide cursor, stop
- Settings: mood, cursor size (48–120pt), glow, phone position
- Bonjour auto-discovery pairing (same Wi-Fi, zero config)

## 5. Freckle — https://freckle.tech/

*What it is: a $199 kid-safe phone (ages 7–13, ships Dec 2026) on custom ClayOS —
no browser/app store/social/YouTube. The screen points kids at activities and
people, not feeds.*

- Kid-sized rugged hardware: 3.1" square screen, drop-proof, tactile buttons, lanyard attach
- ClayOS: parent-shaped OS — every feature individually on/off; capabilities unlock gradually as kids mature
- Discovery/Curiosity Camera: point at bug/bird/plant → AI identifies it → saved as collectible "Artifacts"/sticker book; parents review in companion app
- Quests: parent-created or pre-set real-world exploration challenges (photograph 3 bugs, etc.)
- Why Chat: answers kids' endless "why?" — sensitive ones routed to parents
- Story Time: kids build their own stories
- Maps for Kids
- Walkie-talkie: two devices tap together → instant voice mode
- Texting/calling: parent-approved contacts only
- Freckle Pay: parent-loaded tap-to-pay wallet with spending limits
- Location tracking + safe zones (alert if child leaves); continuous tracking optional — pitched as independence, not "ankle monitor"
- No data selling, no AI training on kid data (promised; parent app not yet public)

---

## MASTER KNOCK-OFF LIST

*Tags: [have] demoed in Kodakai · [partial] started or simulated · [gap] not yet.*

### Avatar & Presence
- [have] Drop character with real art, visible on every surface
- [have] Transform library (drop/cloud/wave/star/fish/round/storm/rain)
- [have] Word dance / beat moves with visible move names
- [have] Weather transforms: storm cloud w/ cartoon hands + lightning + burn-mark overlay + wipe; rain dance
- [have] Feelings Book: drawings as the language of feeling, replay ("remember you drew that?")
- [partial] Its OWN cursor on target screens (bluey-style) — demos move Drop, no real cursor injection yet
- [partial] Drawing-to-puppet: kid drawings rigged into living characters (planned, image-engine doc)
- [gap] Follow mode: Drop tracks your pointer across the desktop unprompted
- [gap] Mood system (menu-bar-style mood/cursor-size/glow settings)
- [gap] Push-to-talk character: mic-on-for-context, quiet until asked, answers in speech bubble + chirp

### Voice & Command
- [have] Voice commands with visible action trail (command deck demo)
- [have] Bedtime story imagination engine w/ ad-libs; Magic Drop 8-ball w/ real typing
- [partial] Real speech-in/speech-out loop (TTS exists; always-listening not built)
- [gap] Screen-seeing on hotkey: "what's this?" → Drop points at what's under YOUR cursor (heyclicky+bluey)
- [gap] Draw-ON-the-screen annotations to point the way (heyclicky)
- [gap] Always-on agents with approval loop: owns a responsibility, works between chats, brings decisions (dots)
- [gap] Custom Rules: allow / require-approval / block per action (dots)
- [gap] "Why Chat": kid-safe endless-why answerer with sensitive questions routed to parents (freckle)

### Multi-Device
- [have] Sprite runtime: one script per device, phone sends sprite, station executes + reports home (demo)
- [have] Network map: stations as a hive, Drop hops visibly
- [have] Walkie-talkie (in-app)
- [partial] Real HQ sync server on Shadow (spec'd, not built); transport is BroadcastChannel demo today
- [partial] Phone as main hub controlling all stations at once (demo only)
- [gap] Cross-device computer use: click/type/scroll/drag/open apps WITH ITS OWN CURSOR (bluey)
- [gap] Carry a mission desktop→mobile without losing intent (jarvis)
- [gap] Station pairing: zero-config discovery (Bonjour-style) + station tokens
- [gap] Drones / real hardware buddies as stations (visual only today)

### Kid Safety
- [have] PIN-gated parent areas; kid-safe walled app; Learning Book
- [have] Profiles (Kai/Koda/Together/Grown-up) + All About Me
- [gap] Approved-contacts-only communication (freckle)
- [gap] Safe zones + location alerts; optional continuous tracking (freckle)
- [gap] Parent companion controls: per-feature on/off, capabilities unlock with age (freckle ClayOS model)
- [gap] Guardrails: acts only when asked; confirms before irreversible; on-screen text = info never instructions; refuses password fields/lock/force-quit; kill switch (bluey)
- [gap] Privacy posture: no screenshots stored, text-summaries-only context, one-click full delete (heyclicky)
- [gap] No data selling / no AI training on kid data (freckle promise)

### Open Hardware & Community
- [gap] Kid-rugged open hardware: small, drop-proof, lanyard-ready device (freckle)
- [gap] Discovery Camera: point at bug/bird/plant → AI identifies → collectible sticker book / Artifacts (freckle)
- [gap] Parent-created Quests: real-world exploration challenges (freckle)
- [gap] Tap-together walkie-talkie pairing between two devices (freckle)
- [gap] Parent-loaded tap-to-pay wallet with limits (freckle Pay)
- [gap] Maps for Kids
- [gap] Hybrid local/cloud brain: local models for routine, cloud escalation for heavy (jarvis)
- [gap] Token-optimized routing: smallest capable model first (jarvis)
- [gap] Multi-user identity/sessions/permissions separation (jarvis)
- [gap] Community moves list: anyone can define new Drop moves (shimeji-style, from screensaver research)
