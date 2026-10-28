// Bridge core tests — node --test (Node 24, no dependencies).
// Run: node --test bridge-core.test.mjs
import { test } from 'node:test';
import assert from 'node:assert/strict';
import {
  localToEnu,
  localToGeo,
  validatePose,
  stampPose,
  PoseGate,
  SessionRecorder,
  METERS_PER_DEG_LAT,
} from './bridge-core.mjs';

// Draft anchor near the house (David's own message location, Oct 26) —
// a test fixture, NOT a registered map. Registrations happen on site.
const ANCHOR = {
  map_code: 'MAP_TEST0001',
  origin_lat: 27.924433,
  origin_lon: -82.720565,
  origin_alt_m: 12,
  north_offset_deg: 0,
};

function pose(overrides = {}) {
  return {
    type: 'glasses.pose',
    v: 1,
    session_id: 'sess-test-01',
    participant_id: 'avatar-david',
    display_name: 'David (glasses)',
    source: 'rayban-multiset',
    ts: new Date(1_800_000_000_000).toISOString(),
    map_code: 'MAP_TEST0001',
    local: { x_m: 0, y_m: 1.62, z_m: 0, yaw_deg: 0 },
    geo: null,
    through_wall: false,
    quality: { localized: true, relocalized_ms_ago: 100 },
    ...overrides,
  };
}

test('origin maps to origin', () => {
  const g = localToGeo({ x_m: 0, y_m: 0, z_m: 0 }, ANCHOR);
  assert.equal(g.lat, ANCHOR.origin_lat);
  assert.equal(g.lon, ANCHOR.origin_lon);
  assert.equal(g.alt_m, ANCHOR.origin_alt_m);
});

test('10 m along local +z (north at offset 0) moves latitude only', () => {
  const g = localToGeo({ x_m: 0, y_m: 0, z_m: 10 }, ANCHOR);
  const expected = ANCHOR.origin_lat + 10 / METERS_PER_DEG_LAT;
  assert.ok(Math.abs(g.lat - expected) < 1e-9, `${g.lat} vs ${expected}`);
  assert.equal(g.lon, ANCHOR.origin_lon);
});

test('10 m along local +x (east at offset 0) moves longitude only', () => {
  const enu = localToEnu({ x_m: 10, y_m: 0, z_m: 0 }, 0);
  assert.equal(enu.east_m, 10);
  assert.equal(enu.north_m, 0);
  const g = localToGeo({ x_m: 10, y_m: 0, z_m: 0 }, ANCHOR);
  assert.equal(g.lat, ANCHOR.origin_lat);
  assert.ok(g.lon > ANCHOR.origin_lon);
});

test('north offset 90 deg: local +z now points east', () => {
  const enu = localToEnu({ x_m: 0, y_m: 0, z_m: 10 }, 90);
  assert.ok(Math.abs(enu.east_m - 10) < 1e-9);
  assert.ok(Math.abs(enu.north_m) < 1e-9);
});

test('height adds to altitude', () => {
  const g = localToGeo({ x_m: 0, y_m: 1.62, z_m: 0 }, ANCHOR);
  assert.ok(Math.abs(g.alt_m - 13.62) < 1e-9);
});

test('contract validation accepts the documented shape, rejects drift', () => {
  assert.equal(validatePose(pose()).ok, true);
  assert.equal(validatePose(pose({ source: 'cctv' })).ok, false);
  assert.equal(validatePose(pose({ local: { x_m: 0 } })).ok, false);
  assert.equal(validatePose(pose({ through_wall: 'no' })).ok, false);
  assert.equal(validatePose(null).ok, false);
});

test('stampPose recomputes geo and ignores a lying sender geo', () => {
  const lying = pose({
    geo: { lat: 0, lon: 0, alt_m: 0 },
    local: { x_m: 0, y_m: 1.62, z_m: 5, yaw_deg: 30 },
  });
  const out = stampPose(lying, ANCHOR);
  assert.equal(out.ok, true);
  assert.ok(out.pose.geo.lat > ANCHOR.origin_lat); // 5 m north-ish
  assert.equal(out.pose.geo_source, 'bridge-anchor');
  assert.equal(out.pose.yaw_geo_deg, 30);
});

test('stampPose fails closed on an unregistered map', () => {
  const out = stampPose(pose(), { ...ANCHOR, map_code: 'MAP_OTHER' });
  assert.equal(out.ok, false);
  assert.match(out.errors[0], /fail closed/);
});

test('gate throttles to 10 Hz and drops stale poses', () => {
  const gate = new PoseGate({ hz: 10, staleMs: 500 });
  const t0 = 1_800_000_000_000;
  const fresh = pose({ ts: new Date(t0).toISOString() });
  assert.equal(gate.admit(fresh, t0 + 10), 'send');
  assert.equal(gate.admit(fresh, t0 + 50), 'throttled'); // 40 ms later
  assert.equal(gate.admit(fresh, t0 + 200), 'send'); // 190 ms after send
  const stale = pose({ ts: new Date(t0).toISOString() });
  assert.equal(gate.admit(stale, t0 + 600), 'stale'); // 600 ms old
});

test('recorder downsamples to 1 Hz and keeps no raw stream', () => {
  const rec = new SessionRecorder('sess-test-01', 'MAP_TEST0001');
  const t0 = 1_800_000_000_000;
  for (let i = 0; i < 20; i++) {
    const stamped = stampPose(
      pose({
        ts: new Date(t0 + i * 100).toISOString(),
        local: { x_m: 0, y_m: 1.62, z_m: i * 0.1, yaw_deg: 0 },
      }),
      ANCHOR,
    ).pose;
    rec.observe(stamped, t0 + i * 100);
  }
  const record = rec.stop(new Date(t0 + 2000).toISOString());
  assert.equal(record.pose_count_in, 20);
  // 20 poses over 2 s at 100 ms spacing -> samples at 0 ms and 1000 ms (and 1900 < 2000? no: last sample gate is >=1000 ms after previous, so samples at 0, 1000 — the 1900 ms pose is 900 ms after 1000, skipped)
  const track = record.tracks_1hz['avatar-david'];
  assert.equal(track.length, 2);
  assert.deepEqual(record.participants, ['avatar-david']);
  assert.match(record.retention, /not retained/);
});
