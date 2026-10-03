# Shadow Drop — Koda Kai lives on the desktop

The first real helper: a 3D animated Drop that lives on the Shadow PC desktop,
not in a browser tab. Transparent, always-on-top, alive.

## What he does (v1)

- **Floats** bottom-right of the desktop, gentle bob
- **Blinks** every few seconds, **looks around** on his own
- **Waves** when clicked, with a speech bubble
- **Points with his own cursor** — a drawn cursor independent of the real
  pointer (bluey-by-riley style), glides to any screen coordinate
- **Speaks** lines sent remotely, announces caption-batch milestones
- **Draggable** anywhere on screen

## Files

- `shadow-drop/drop-overlay.py` — the overlay (Python + tkinter, stdlib only)
- `assets/char/drop-idle.png`, `drop-wave.png`, `drop-point.png` — 3D frames

## Remote control channel (Kodakai → Shadow over SSH)

- `C:\Users\Public\Muse\drop-say.txt` — Drop speaks the line, then clears it
- `C:\Users\Public\Muse\drop-cmd.txt` — one command per line:
  `wave` · `bounce` · `point X Y` · `say <text>` · `hide` · `show`
- `C:\Users\Public\Muse\drop\drop-status.txt` — heartbeat (`alive <epoch>`),
  written every 30s so HQ can verify he's on the interactive desktop

## Launch

Runs in the **interactive session** (session 1), not session 0 — GUI apps
launched from SSH land in session 0 and can never show a window.

- Scheduled task `\MuseDrop` — AtLogOn for user `muse`, auto-starts every login
- Manual session-1 launch: `PsExec.exe -accepteula -i 1 -d pythonw.exe drop-overlay.py`
- Kill hung session-0 copies: `Get-Process -Name pythonw | Stop-Process -Force`

## Status

- 2026-10-03: v1 deployed to `C:\Users\Public\Muse\drop\`, heartbeat confirmed
  in session 1. Screenshot verification pending.
- Next: phone → Shadow WebSocket handoff (HQ sync server), real helper actions
  (open apps, guide through windows), voice lines.
