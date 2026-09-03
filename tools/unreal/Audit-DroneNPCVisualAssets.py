"""Read-only audit for the NPC, MG, VFX, and SFX candidates used by AI-VIS-01."""

from __future__ import annotations

import traceback

import unreal


PREFIX = "DRONE_NPC_VISUAL_AUDIT"
ASSETS = {
    "MANNY_GREYBOX": "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple",
    "MODULAR_SOLDIER": "/Game/Drone/ThirdParty/ModularSoldier/Meshes/Body/SKM_Modular_Soldier",
    "INSURGENT_PRESET": "/Game/Drone/ThirdParty/ModularInsurgents/Mesh/SK_Preset1",
    "INSURGENT_BODY": "/Game/Drone/ThirdParty/ModularInsurgents/Mesh/SK_BaseBody",
    "MANNY_RIFLE_FIRE": "/Game/Characters/Mannequins/Anims/Rifle/MM_Rifle_Fire",
    "MANNY_RIFLE_RELOAD": "/Game/Characters/Mannequins/Anims/Rifle/MM_Rifle_Reload",
    "RIFLE_AR4": "/Game/FPS_Weapon_Bundle/Weapons/Meshes/AR4/SK_AR4",
    "MG_TURRET": "/Game/Drone/ThirdParty/GroundDroneKit/Meshes/Alt_Turrets/MG_Turret/MG_Turret_SK",
    "MG_MUZZLE_VFX": "/Game/Drone/ThirdParty/ArmyVFX/Niagara/MuzzleFlash/NS_MuzzleFlash_Tank_Mashingun_1",
    "AUTOCANNON_SFX": "/Game/Drone/ThirdParty/InfantrySFX/Weapons/Cues/Cue_Autocannon01_Cue",
    "BULLET_IMPACT_SFX": "/Game/Drone/ThirdParty/InfantrySFX/Weapons/Cues/Cue_BulletsFlybyAndImpact01_Cue",
}
CONTENT_ROOTS = (
    "/Game/Drone/ThirdParty/ModularSoldier",
    "/Game/Drone/ThirdParty/ModularInsurgents",
    "/Game/Characters/Mannequins/Anims/Rifle",
)
WEAPON_ROOT = "/Game/FPS_Weapon_Bundle/Weapons/Meshes"
SHOTGUN_NAME_MARKERS = ("shotgun", "m870", "mossberg", "spas", "pump_action")


def log(message: str) -> None:
    unreal.log(f"{PREFIX}|{message}")


def object_path(value: object) -> str:
    return value.get_path_name() if value is not None else "None"


def read_property(asset: object, property_name: str) -> object:
    try:
        return asset.get_editor_property(property_name)
    except Exception:
        return None


def main() -> None:
    editor_assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    registry = unreal.AssetRegistryHelpers.get_asset_registry()
    if editor_assets is None or registry is None:
        raise RuntimeError("Editor Asset services are unavailable")

    skeleton_by_label: dict[str, str] = {}
    for label, path in ASSETS.items():
        if not editor_assets.does_asset_exist(path):
            log(f"MISSING|{label}|{path}")
            continue

        asset = editor_assets.load_asset(path)
        if asset is None:
            log(f"LOAD_FAILED|{label}|{path}")
            continue

        skeleton = read_property(asset, "skeleton")
        physics_asset = read_property(asset, "physics_asset")
        skeleton_path = object_path(skeleton)
        if skeleton is not None:
            skeleton_by_label[label] = skeleton_path
        log(
            f"ASSET|{label}|class={asset.get_class().get_name()}|path={path}"
            f"|skeleton={skeleton_path}|physics={object_path(physics_asset)}"
        )

    manny_skeleton = skeleton_by_label.get("MANNY_GREYBOX")
    for label in ("MODULAR_SOLDIER", "INSURGENT_PRESET", "INSURGENT_BODY"):
        candidate_skeleton = skeleton_by_label.get(label)
        direct_match = bool(manny_skeleton and candidate_skeleton == manny_skeleton)
        log(f"MANNY_SKELETON_MATCH|{label}|{int(direct_match)}")

    animation_classes = {"AnimSequence", "AnimMontage", "AnimBlueprint", "BlendSpace"}
    for root in CONTENT_ROOTS:
        animation_packages: list[str] = []
        for data in registry.get_assets_by_path(root, recursive=True):
            class_name = str(data.asset_class_path.asset_name)
            if class_name in animation_classes:
                animation_packages.append(str(data.package_name))
        log(f"ANIMATION_COUNT|{root}|{len(animation_packages)}")
        for package_name in sorted(animation_packages):
            log(f"ANIMATION|{root}|{package_name}")

    # 이름 기반 검색 결과는 실제 역할 확정이 아니라 후보 유무 판단에만 사용한다.
    weapon_meshes: list[str] = []
    shotgun_named_meshes: list[str] = []
    for data in registry.get_assets_by_path(WEAPON_ROOT, recursive=True):
        class_name = str(data.asset_class_path.asset_name)
        if class_name not in {"SkeletalMesh", "StaticMesh"}:
            continue
        package_name = str(data.package_name)
        weapon_meshes.append(package_name)
        normalized_name = package_name.lower()
        if any(marker in normalized_name for marker in SHOTGUN_NAME_MARKERS):
            shotgun_named_meshes.append(package_name)
    log(f"WEAPON_MESH_COUNT|{WEAPON_ROOT}|{len(weapon_meshes)}")
    log(f"SHOTGUN_NAMED_MESH_COUNT|{WEAPON_ROOT}|{len(shotgun_named_meshes)}")
    for package_name in sorted(shotgun_named_meshes):
        log(f"SHOTGUN_NAMED_MESH|{package_name}")

    log("AUDIT_OK")


try:
    main()
except Exception as error:
    log(f"FAILED|{error}")
    unreal.log_error(traceback.format_exc())
    raise
