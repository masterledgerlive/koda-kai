// Pose bridge core — glasses-bridge
//
// Pure logic for the POSE-CONTRACT.md wire format: validation, local->geo
// conversion against a registered map anchor, per-participant throttling
// with stale-drop, and 1 Hz session recording. No sockets here on purpose:
// the WebSocket relay is a thin shell over this file, so everything that
// can be wrong about the MATH and the CONTRACT is testable offline.
//
// Coordinate frame note (POSE-CONTRACT.md): MultiSet/Unity local frame is
// left-handed, x = right, y = up, z = forward (away from viewer at origin
// heading). The ENU conversion below treats local +z as the map's "north
// reference direction" rotated by the registration's north_offset_deg.
// The sign convention MUST be proven on the first live test (walk north in
// the room, check the globe) and this comment updated with the result.

export const METERS_PER_DEG_LAT = 111320;

export function metersPerDegLon(latDeg) {
  return METERS_PER_DEG_LAT * Math.cos((latDeg * Math.PI) / 180);
}

/**
 * Convert a MultiSet local pose position to ENU meters relative to the
 * map origin, applying the registration's north offset.
 * local: {x_m, y_m, z_m}; returns {east_m, north_m, up_m}.
 */
export function localToEnu(local, northOffsetDeg) {
  const t = ((northOffsetDeg ?? 0) * Math.PI) / 180;
  const cos = Math.cos(t);
  const sin = Math.sin(t);
  // Local +z (forward) points along the map's north reference; local +x is
  // 90 deg clockwise from it (east when the offset is 0).
  const north_m = local.z_m * cos - local.x_m * sin;
  const east_m = local.z_m * sin + local.x_m * cos;
  return { east_m, north_m, up_m: local.y_m ?? 0 };
}

/** ENU meters + anchor -> WGS84 geo. Small-area approximation (room scale). */
export function enuToGeo(enu, anchor) {
  const lat = anchor.origin_lat + enu.north_m / METERS_PER_DEG_LAT;
  const lon =
    anchor.origin_lon + enu.east_m / metersPerDegLon(anchor.origin_lat);
  const alt_m = (anchor.origin_alt_m ?? 0) + (enu.up_m ?? 0);
  return { lat, lon, alt_m };
}

export function localToGeo(local, anchor) {
  return enuToGeo(localToEnu(local, anchor.north_offset_deg ?? 0), anchor);
}

const SOURCES = new Set(['rayban-multiset', 'phone-multiset', 'phone-ar']);

function isNum(v) {
  return typeof v === 'number' && Number.isFinite(v);
}

/**
 * Validate a glasses.pose message against POSE-CONTRACT.md v1.
 * Returns { ok: true } or { ok: false, errors: [...] }.
 * A sender-stamped `geo` is NOT trusted: validation accepts its presence
 * but the bridge always recomputes geo from local + anchor.
 */
export function validatePose(msg) {
  const errors = [];
  if (msg === null || typeof msg !== 'object') {
    return { ok: false, errors: ['message is not an object'] };
  }
  if (msg.type !== 'glasses.pose') errors.push('type must be "glasses.pose"');
  if (msg.v !== 1) errors.push('v must be 1');
  if (!msg.session_id || typeof msg.session_id !== 'string')
    errors.push('session_id missing');
  if (!msg.participant_id || typeof msg.participant_id !== 'string')
    errors.push('participant_id missing');
  if (!SOURCES.has(msg.source))
    errors.push('source must be rayban-multiset | phone-multiset | phone-ar');
  if (!msg.ts || Number.isNaN(Date.parse(msg.ts)))
    errors.push('ts must be an ISO timestamp');
  if (!msg.map_code || typeof msg.map_code !== 'string')
    errors.push('map_code missing');
  const l = msg.local;
  if (!l || !isNum(l.x_m) || !isNum(l.y_m) || !isNum(l.z_m) || !isNum(l.yaw_deg))
    errors.push('local must carry numeric x_m, y_m, z_m, yaw_deg');
  if (typeof msg.through_wall !== 'boolean')
    errors.push('through_wall must be boolean');
  return errors.length ? { ok: false, errors } : { ok: true };
}

/**
 * Per-participant throttle per the contract: the globe layer receives at
 * most `hz` updates/sec/participant; poses older than `staleMs` (by the
 * receiver's clock) are dropped, never queued.
 */
export class PoseGate {
  constructor({ hz = 10, staleMs = 500 } = {}) {
    this.minIntervalMs = 1000 / hz;
    this.staleMs = staleMs;
    this.lastSentAt = new Map();
  }

  /** Returns 'send' | 'throttled' | 'stale'. nowMs = receiver clock. */
  admit(msg, nowMs) {
    const age = nowMs - Date.parse(msg.ts);
    if (age > this.staleMs) return 'stale';
    const last = this.lastSentAt.get(msg.participant_id) ?? -Infinity;
    if (nowMs - last < this.minIntervalMs) return 'throttled';
    this.lastSentAt.set(msg.participant_id, nowMs);
    return 'send';
  }
}

/**
 * Session recorder: keeps a 1 Hz downsampled track per participant and
 * builds the session record POSE-CONTRACT.md specifies. Raw 20 Hz poses
 * pass through and are NOT retained here.
 */
export class SessionRecorder {
  constructor(sessionId, mapCode) {
    this.session_id = sessionId;
    this.map_code = mapCode;
    this.startedAt = null;
    this.stoppedAt = null;
    this.poseCount = 0;
    this.tracks = new Map(); // participant_id -> [{ts, lat, lon, alt_m}]
    this.lastSampleAt = new Map();
  }

  observe(poseWithGeo, nowMs) {
    if (this.startedAt === null) this.startedAt = poseWithGeo.ts;
    this.poseCount += 1;
    const p = poseWithGeo.participant_id;
    const last = this.lastSampleAt.get(p) ?? -Infinity;
    if (nowMs - last >= 1000) {
      this.lastSampleAt.set(p, nowMs);
      if (!this.tracks.has(p)) this.tracks.set(p, []);
      this.tracks.get(p).push({
        ts: poseWithGeo.ts,
        lat: poseWithGeo.geo.lat,
        lon: poseWithGeo.geo.lon,
        alt_m: poseWithGeo.geo.alt_m,
        through_wall: poseWithGeo.through_wall,
        source: poseWithGeo.source,
      });
    }
  }

  stop(stoppedAtIso) {
    this.stoppedAt = stoppedAtIso;
    return {
      session_id: this.session_id,
      map_code: this.map_code,
      started_at: this.startedAt,
      stopped_at: this.stoppedAt,
      pose_count_in: this.poseCount,
      participants: [...this.tracks.keys()],
      tracks_1hz: Object.fromEntries(this.tracks),
      retention:
        'Raw poses and glasses video are not retained by the bridge; ' +
        'this 1 Hz track is the session record (POSE-CONTRACT.md).',
    };
  }
}

/**
 * The bridge's one trusted transform: validate -> recompute geo from the
 * registered anchor (sender geo ignored) -> return the stamped pose.
 * Returns { ok, pose } or { ok: false, errors }.
 * Fail-closed: an unregistered map_code has no anchor and no pose passes.
 */
export function stampPose(msg, anchor) {
  const v = validatePose(msg);
  if (!v.ok) return { ok: false, errors: v.errors };
  if (!anchor || anchor.map_code !== msg.map_code)
    return { ok: false, errors: ['map_code not registered — fail closed'] };
  const geo = localToGeo(msg.local, anchor);
  return {
    ok: true,
    pose: {
      ...msg,
      geo,
      geo_source: 'bridge-anchor',
      yaw_geo_deg: (msg.local.yaw_deg + (anchor.north_offset_deg ?? 0) + 360) % 360,
    },
  };
}
