# POSE CONTRACT — glasses/phones → bridge → God's Eye View

The wire format between a see-through-walls session (MultiSet VPS poses) and
the God's Eye View `glassesLive` layer. Version 1, 2026-10-26.

**Implementation status (2026-10-27):** the bridge's pure core exists and is
tested — `bridge-core.mjs` (validation, local→geo anchor conversion,
10 Hz/stale-500 ms gate, 1 Hz session recorder) with `bridge-core.test.mjs`
at **10/10 passing** under `node --test`. The WebSocket relay shell and the
globe-side `glassesLive` layer remain to be built; the local-frame sign
convention in the conversion is still flagged in the code as *to be proven
on the first live walk* (walk north in the room, watch the globe).

## Flow

```
Ray-Ban glasses ──video──► iPhone companion (MultisetRayBanTracking)
                                  │ localize vs MultiSet map (~1 Hz relocalize)
                                  ▼ pose ~20 Hz (MultipeerConnectivity)
Phone(s) ── Unity MultiplayerSample ── pose (Netcode/UTP, LAN)
                                  │
                                  ▼
                        POSE BRIDGE (local WebSocket relay, LAN-first)
                                  │ applies the map's geo anchor
                                  ▼
              God's Eye View · src/layers/glassesLive (avatar / skeleton)
                                  │
                                  └─► session record → historian present-day
                                      layer + sleuth case evidence (on stop)
```

## Message: `glasses.pose`

```json
{
  "type": "glasses.pose",
  "v": 1,
  "session_id": "sess-2026-10-26-livingroom-01",
  "participant_id": "avatar-david",
  "display_name": "David (glasses)",
  "source": "rayban-multiset",
  "ts": "2026-10-26T06:40:00.000Z",
  "map_code": "MAP_XXXXXXXX",
  "local": { "x_m": 1.24, "y_m": 1.62, "z_m": -3.10, "yaw_deg": 87.5 },
  "geo": { "lat": 27.92448, "lon": -82.72055, "alt_m": 14.2 },
  "through_wall": false,
  "quality": { "localized": true, "relocalized_ms_ago": 420 }
}
```

- `source` ∈ `rayban-multiset` | `phone-multiset` | `phone-ar` (future).
- `participant_id` is a session pseudonym chosen by the participant.
  Never a legal name, phone number, or account id by default.
- `geo` is computed by the bridge from `local` + the map's registered geo
  anchor (see INTEGRATION-PLAN.md §3). Senders may include `geo: null`;
  the bridge is the only component trusted to stamp coordinates.
- `through_wall` is computed by the *viewer's* client in upstream's design
  (raycast vs the CollisionMesh). For the globe layer the bridge computes it
  per registered viewer viewpoint when one is set; otherwise it carries the
  host's value. The field means "occluded from the current viewpoint,"
  never a property of the person.
- Rate: poses arrive ~20 Hz from the glasses flow; the bridge throttles
  globe updates to 10 Hz per participant and drops (never queues) stale
  poses older than 500 ms.

## Map registration record

```json
{
  "map_code": "MAP_XXXXXXXX",
  "label": "Living room, Oak Street",
  "origin_lat": 27.92448, "origin_lon": -82.72055, "origin_alt_m": 12.0,
  "north_offset_deg": 0.0,
  "registered_by": "David",
  "consent_scope": "household-session-only",
  "created": "2026-10-26"
}
```

Local → geo conversion (ENU, small-area approximation — a room, not a county):
`east_m = x*cos(north) − z*sin(north)`, `north_m = x*sin(north) + z*cos(north)`
(signs verified against Unity's left-handed frame on the first live test and
recorded here when proven), then
`lat = origin_lat + north_m / 111320`,
`lon = origin_lon + east_m / (111320 * cos(origin_lat))`.

## Session record (what gets kept)

On session stop, the bridge writes one record: session id, map code,
participants (pseudonyms), start/stop, pose count, and a downsampled track
(1 Hz) per participant — into the historian present-day feed and, when David
opens one, a sleuth case file. **Raw 20 Hz poses and glasses video are not
kept** unless David says so for that session. Nothing leaves the LAN unless
David approves that session for public watch.
