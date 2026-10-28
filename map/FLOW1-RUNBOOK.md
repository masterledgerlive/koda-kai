# FLOW 1 RUNBOOK — phones-first, see-through-walls on Android

*David's call 2026-10-26: phones-first (Android / Flow 1) before the Ray-Ban
Flow 2 build. Everything below is verified against the actual repos and
MultiSet's own docs (cited inline), not memory.*

## The shape of Flow 1 (upstream, verified)

Two (or more) phones, each running the Unity **MultiPlayerSample** app in the
same scanned space, on the **same Wi-Fi**. One phone is **Host**, the other
joins by typing the host's IP. Both localize against the same MultiSet map;
then each sees the other as an avatar at their real position — and when the
other person steps behind a wall that's in the map mesh, their avatar turns
into a **glowing skeleton**. (bilawalsidhu/see-through-walls README, Flow 1;
scene + scripts verified present in MultiSet Unity SDK v1.15.2 clone:
`Samples~/Scenes/MultiplayerSample/` — MultiplayerManager,
MapMeshColliderSetup, SingleFrameLocalizationManager, NetworkUI,
PlayerPrefab.)

Transport: Unity Netcode over UTP (SDK depends on
`com.unity.netcode.gameobjects 2.9.2`). No cloud relay — LAN only.

## Phase 0 — accounts (David, ~15 min, all free)

- [ ] **MultiSet developer account** — free at developer.multiset.ai, **no
      credit card** (MultiSet pricing FAQ, checked 2026-10-26). Free plan:
      1,000 localization API calls for the life of the account, watermark in
      app, maps carry over if upgraded later. Paid starts at Lite $99/mo —
      **not needed to build/test, and not to be bought without David's word.**
      Create credentials in the portal → the `clientSecret` is shown **once**
      → save it straight into the Secure Vault.
- [ ] **Unity account + Personal license** — free. Needed to activate the
      editor on whichever machine builds (this VM headless, or Shadow PC).
      David signs in once; Muse never sees the password.

## Phase 1 — scan the room (David + phone, ~10 min)

The MultiSet **Mapping App** runs on **any ARKit iPhone or ARCore Android**
(LiDAR optional — MultiSet mapping instructions, docs.multiset.ai). David's
iPhone can do the scan even though the session phones are Android.

- [ ] Install MultiSet Mapping App, sign in with the developer account.
- [ ] Scan the test room: stay **1–5 m** from surfaces, slow continuous
      pace, landscape, vary viewpoints (never repeat the same viewpoint),
      tilt up/down for ceiling/floor, walk corridors **both directions**,
      favor textured walls/furniture; keep mirrors, glass, blank walls and
      moving people out of frame center.
- [ ] Upload; wait for the map to go **Active** in the portal; copy its
      **mapCode**. (Optional but valuable for our globe: georeference the
      map to WGS 84 in the portal — MultiSet then returns GeoPose/WGS 84
      poses, which is exactly the anchor our God's Eye bridge wants.)

## Phase 2 — build the Android app (prepared, ~30–60 min first run)

Prepared project: **`flow1-unity-project/`** (next door to this file) —
version pinned to **Unity 6000.3.11f1**, SDK in the manifest,
CollisionMesh layer pre-created, and an editor script that applies every
Android setting (OpenGLES3 only, IL2CPP, ARM64, MT rendering, min API 26,
unsafe code) from one menu click.

Version warning (caught in prep): Bilawal's README says Unity 6000.0.36f1+;
the **current SDK (v1.15.2) requires 6000.3.11f1+** — its package.json pins
it and its troubleshooter rejects lower. Use 6000.3.11f1 or a later 6000.3
patch.

- [ ] Install Unity Hub + Unity 6000.3.x with **Android Build Support**
      (SDK/NDK/OpenJDK modules) on the build machine; sign in (Phase 0).
- [ ] Open `flow1-unity-project/`; let Package Manager resolve the SDK.
- [ ] Import Sample Scenes (Package Manager → MultiSet-SDK → Samples).
- [ ] Menu **Koda Kai → Apply Flow 1 Android Settings**, then
      **Koda Kai → Set MultiPlayerSample As Build Scene**.
- [ ] XR Plug-in Management → Android → check **ARCore** (manual).
- [ ] Paste credentials into `MultiSetConfig.asset` (Inspector); set the
      Phase-1 **mapCode** on `SingleFrameLocalizationManager`.
- [ ] Build APK (IL2CPP/ARM64) and install on both phones (USB or
      `adb install`). Phones: **ARCore-supported, Android API 26+**,
      camera permission granted on first launch.

## Phase 3 — the session (the proof)

- [ ] Both phones on the **same Wi-Fi**.
- [ ] Each person enters a display name (avatar name — session pseudonym).
- [ ] Phone A: **Start Host**. Phone B: type A's IP → **Start Client** →
      "Connected to host."
- [ ] Both: point camera around, trigger localization. **Nobody sees
      anybody until both devices have localized.**
- [ ] Walk the room. Test the wall: one person steps behind the mapped
      wall → skeleton on the other screen. **That swap is the pass/fail
      of the whole build.**
- [ ] Bridge step (ours): poses out of MultiplayerManager → pose relay →
      God's Eye `glassesLive` layer (POSE-CONTRACT.md) — after the
      in-room proof, not before.

## Device reality check (the one open question)

Flow 1 needs **two session devices in the room**. David's phone is an
iPhone; an iPhone build of this same app still needs a Mac to compile, which
is what phones-first was avoiding. So the second device matters:

- **Best case:** a second ARCore Android in the house → pure Flow 1.
- **One-Android case:** run the second player from the **Unity Editor**
  (the SDK ships simulator controls — `SimulatorControls.inputactions` in
  the sample Resources) on the build machine, same Wi-Fi, while the one
  Android phone plays live. The editor player can't localize against the
  VPS map the way a camera can, so this proves networking/avatars but is a
  *partial* proof — the two-phone run stays the real gate. To be verified
  in the editor, not promised.
- The household's older G1-era phones from the mesh project are **not**
  candidates: no ARCore, far below API 26 in practice.

## Costs & gates summary

- Money so far: **$0**. Free MultiSet tier (1,000 calls) + free Unity
  Personal. Watermark on Free is fine for a test.
- No credentials in chat, ever — portal → vault → Inspector.
- Session data stays on the LAN; participants are household members under
  names they pick. Nothing streams publicly (God's Eye watch is local
  first; public = David's per-session word, unchanged).
