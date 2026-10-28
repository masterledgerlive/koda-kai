// Koda Kai — Flow 1 (see-through-walls, phones-first) project setup.
// Applies every deterministic Android setting MultiSet + Bilawal's sample
// require, so the editor session starts from "import sample" instead of a
// settings scavenger hunt. Settings source:
//   - MultiSet docs, Unity SDK Building Steps (Android): OpenGLES3 only
//     (Vulkan unsupported), Multithreaded Rendering, IL2CPP, ARM64,
//     Allow Unsafe Code, package name.
//   - MultiSet SDK README: min API level 26, ARCore device required.
//   - Bilawal README step 3: a User Layer named exactly "CollisionMesh".
// NOT done here (version-sensitive APIs, two manual clicks each — the
// script logs them as a checklist instead of guessing):
//   - XR Plug-in Management -> Android -> check "ARCore"
//   - Entering MultiSet credentials + map code (David's own account,
//     entered in the Inspector — never in source control or chat).
using UnityEditor;
using UnityEngine;

public static class Flow1Setup
{
    const string BundleId = "com.kodakai.seethroughwalls";
    const int CollisionLayerIndex = 8; // first User Layer slot

    [MenuItem("Koda Kai/Apply Flow 1 Android Settings")]
    public static void ApplyAndroidSettings()
    {
        EnsureCollisionMeshLayer();

        EditorUserBuildSettings.SwitchActiveBuildTarget(
            BuildTargetGroup.Android, BuildTarget.Android);

        PlayerSettings.companyName = "Koda Kai";
        PlayerSettings.productName = "Koda Kai See-Through Walls";
        PlayerSettings.SetApplicationIdentifier(
            BuildTargetGroup.Android, BundleId);
        PlayerSettings.Android.minSdkVersion = AndroidApiLevel.AndroidApiLevel26;
        PlayerSettings.SetScriptingBackend(
            BuildTargetGroup.Android, ScriptingImplementation.IL2CPP);
        PlayerSettings.Android.targetArchitectures = AndroidArchitecture.ARM64;
        PlayerSettings.MTRendering = true;
        PlayerSettings.SetMobileMTRendering(BuildTargetGroup.Android, true);
        PlayerSettings.allowUnsafeCode = true;

        // OpenGLES3 only — Vulkan is NOT supported by the MultiSet SDK.
        PlayerSettings.SetUseDefaultGraphicsAPIs(BuildTarget.Android, false);
        PlayerSettings.SetGraphicsAPIs(
            BuildTarget.Android,
            new[] { UnityEngine.Rendering.GraphicsDeviceType.OpenGLES3 });

        AssetDatabase.SaveAssets();
        Debug.Log(
            "[Flow1] Android settings applied: OpenGLES3, IL2CPP, ARM64, " +
            "MT rendering, min API 26, unsafe code, bundle " + BundleId + ".\n" +
            "[Flow1] MANUAL, still required:\n" +
            "  1. Edit > Project Settings > XR Plug-in Management: enable it, " +
            "then under Android check ARCore.\n" +
            "  2. Import the sample: Package Manager > MultiSet-SDK > Samples " +
            "> Sample Scenes > Import.\n" +
            "  3. Koda Kai menu > Set MultiPlayerSample As Build Scene.\n" +
            "  4. In the imported MultiSetConfig.asset, paste David's MultiSet " +
            "clientId + clientSecret (from his developer.multiset.ai account).\n" +
            "  5. In MultiPlayerSample scene, SingleFrameLocalizationManager: " +
            "set the SAME mapCode (or mapsetCode) on every device.");
    }

    [MenuItem("Koda Kai/Set MultiPlayerSample As Build Scene")]
    public static void SetBuildScene()
    {
        var guids = AssetDatabase.FindAssets("MultiPlayerSample t:Scene");
        if (guids.Length == 0)
        {
            Debug.LogError("[Flow1] MultiPlayerSample scene not found. " +
                "Import Sample Scenes from the MultiSet-SDK package first.");
            return;
        }
        var path = AssetDatabase.GUIDToAssetPath(guids[0]);
        EditorBuildSettings.scenes = new[]
        {
            new EditorBuildSettingsScene(path, true)
        };
        Debug.Log("[Flow1] Build scene set to " + path);
    }

    static void EnsureCollisionMeshLayer()
    {
        var assets = AssetDatabase.LoadAllAssetsAtPath(
            "ProjectSettings/TagManager.asset");
        if (assets == null || assets.Length == 0)
        {
            Debug.LogError("[Flow1] TagManager.asset not found.");
            return;
        }
        var so = new SerializedObject(assets[0]);
        var layers = so.FindProperty("layers");
        if (layers == null || layers.arraySize <= CollisionLayerIndex)
        {
            Debug.LogError("[Flow1] TagManager layers array unexpected shape.");
            return;
        }
        var slot = layers.GetArrayElementAtIndex(CollisionLayerIndex);
        if (slot.stringValue != "CollisionMesh")
        {
            var was = slot.stringValue;
            slot.stringValue = "CollisionMesh";
            so.ApplyModifiedProperties();
            Debug.Log("[Flow1] CollisionMesh layer set at index " +
                CollisionLayerIndex + " (was: '" + was + "').");
        }
        else
        {
            Debug.Log("[Flow1] CollisionMesh layer already present.");
        }
    }
}
