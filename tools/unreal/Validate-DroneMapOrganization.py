"""Validate centralized Drone maps and the corrected starter-map cleanup."""

import json
import unreal


EXPECTED_ASSETS = {
    "/Game/Drone/Maps/Lvl_DronePrototype": "World",
    "/Game/Drone/Maps/Lvl_DroneTraining": "World",
    "/Game/Drone/Maps/Lvl_DronePackShowcase": "World",
    "/Game/Drone/Maps/Lvl_DronePackShowcase_BuiltData": "MapBuildDataRegistry",
    "/Game/Drone/Maps/Lvl_Battlefield": "World",
    "/Game/Drone/Maps/Lvl_MilitaryCamp": "World",
    "/Game/Drone/Maps/Lvl_MilitaryBase": "World",
}

RESTORED_TEMPLATE_ROOTS = (
    "/Game/ThirdPerson",
    "/Game/Variant_Combat",
    "/Game/Variant_Platforming",
    "/Game/Variant_SideScrolling",
)

REMOVED_STARTER_MAPS = (
    "/Game/ThirdPerson/Lvl_ThirdPerson",
    "/Game/Variant_Combat/Lvl_Combat",
    "/Game/Variant_Platforming/Lvl_Platforming",
    "/Game/Variant_SideScrolling/Lvl_SideScrolling",
)

REMOVED_ASSET_PATHS = (
    "/Game/Drone/Prototype/Maps/Lvl_DronePrototype",
    "/Game/Drone/Tutorial/Maps/Lvl_DroneTraining",
    "/Game/Drone/ThirdParty/DronePack/Map/Map_Demo",
    "/Game/Drone/ThirdParty/DronePack/Map/Map_Demo_BuiltData",
)

registry = unreal.AssetRegistryHelpers.get_asset_registry()
registry.wait_for_completion()

map_folder_assets = registry.get_assets_by_path(
    "/Game/Drone/Maps", recursive=False
) or []
actual_packages = {str(asset_data.package_name) for asset_data in map_folder_assets}
if actual_packages != set(EXPECTED_ASSETS):
    raise RuntimeError(
        "Central map package set mismatch: "
        f"expected={sorted(EXPECTED_ASSETS)}, actual={sorted(actual_packages)}"
    )

loaded = {}
for package_name, expected_class in EXPECTED_ASSETS.items():
    asset = unreal.EditorAssetLibrary.load_asset(package_name)
    if asset is None:
        raise RuntimeError(f"Central map asset failed to load: {package_name}")
    actual_class = asset.get_class().get_name()
    if actual_class != expected_class:
        raise RuntimeError(
            f"Unexpected class for {package_name}: "
            f"expected={expected_class}, actual={actual_class}"
        )
    loaded[package_name] = actual_class

restored_template_roots = {
    root: [str(item.package_name) for item in registry.get_assets_by_path(root, recursive=True) or []]
    for root in RESTORED_TEMPLATE_ROOTS
}
missing_restored_roots = {
    root: packages for root, packages in restored_template_roots.items() if not packages
}
if missing_restored_roots:
    raise RuntimeError(f"Restored template root is empty: {missing_restored_roots}")

starter_maps_still_present = [
    package_name
    for package_name in REMOVED_STARTER_MAPS
    if unreal.EditorAssetLibrary.does_asset_exist(package_name)
]
if starter_maps_still_present:
    raise RuntimeError(f"Starter maps still exist: {starter_maps_still_present}")

old_assets_still_present = [
    package_name
    for package_name in REMOVED_ASSET_PATHS
    if unreal.EditorAssetLibrary.does_asset_exist(package_name)
]
if old_assets_still_present:
    raise RuntimeError(f"Old map paths still exist: {old_assets_still_present}")

result = {
    "central_map_assets": loaded,
    "restored_template_root_asset_counts": {
        root: len(packages) for root, packages in restored_template_roots.items()
    },
    "starter_maps_absent": list(REMOVED_STARTER_MAPS),
    "old_map_paths_absent": list(REMOVED_ASSET_PATHS),
}

unreal.log("DRONE_MAP_ORGANIZATION_VALIDATION_JSON_BEGIN")
unreal.log(json.dumps(result, ensure_ascii=False, indent=2))
unreal.log("DRONE_MAP_ORGANIZATION_VALIDATION_JSON_END")
