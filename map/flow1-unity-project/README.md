# Flow 1 Unity project — pre-configured skeleton

Open this folder as a project in **Unity Hub with Unity 6000.3.11f1 or later**
(6000.3 LTS line — the current MultiSet SDK v1.15.2 pins `6000.3 / 11f1` in
its package.json; Bilawal's README floor of 6000.0.36f1 is stale against the
current SDK and its own troubleshooter demands 6000.3.11f1+).

## What's already done in this skeleton

| Piece | State |
|---|---|
| `ProjectSettings/ProjectVersion.txt` | Pinned to 6000.3.11f1 |
| `Packages/manifest.json` | MultiSet SDK via its official git URL (`https://github.com/MultiSet-AI/multiset-unity-sdk.git`) + standard Unity modules. Unity resolves the SDK's own deps on first open: AR Foundation/ARCore/ARKit 6.3.3, Netcode for GameObjects 2.9.2, Draco, glTFast, AI Navigation |
| `ProjectSettings/TagManager.asset` | User Layer 8 = **CollisionMesh** (Bilawal step 3 — without it the skeleton-through-walls effect silently breaks) |
| `Assets/Editor/Flow1Setup.cs` | Menu **Koda Kai → Apply Flow 1 Android Settings**: switches to Android, OpenGLES3 only (Vulkan unsupported), IL2CPP, ARM64, multithreaded rendering, min API 26, unsafe code, bundle id `com.kodakai.seethroughwalls`, re-verifies the CollisionMesh layer, then logs the short manual remainder. Second menu: **Set MultiPlayerSample As Build Scene** |

## What stays manual (by design)

1. **XR Plug-in Management → Android → ARCore** checkbox (API varies by
   Unity patch; two clicks).
2. **Import the sample:** Package Manager → MultiSet-SDK → Samples →
   Sample Scenes → Import. Scene lands at
   `Assets/Samples/MultiSet-SDK/1.15.2/Sample Scenes/MultiplayerSample/MultiPlayerSample.unity`
   (verified present in the SDK clone, with MultiplayerManager,
   MapMeshColliderSetup, SingleFrameLocalizationManager, PlayerPrefab).
3. **Credentials:** David's MultiSet `clientId`/`clientSecret` go into the
   imported `MultiSetConfig.asset` in the Inspector. Never into this folder,
   git, or chat — the secret is shown once at creation in the MultiSet
   portal; store it in the Secure Vault.
4. **Map code:** the same `mapCode`/`mapsetCode` on every device's
   `SingleFrameLocalizationManager`, from David's scanned map.

## Not in this skeleton

A full `ProjectSettings.asset` — Unity generates it on first open and the
setup script then sets the values that matter. Android SDK/NDK: install via
Unity Hub (Android Build Support module) — Unity manages its own copies.
