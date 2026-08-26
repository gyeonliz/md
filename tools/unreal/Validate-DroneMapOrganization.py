"""Validate the centralized Drone map folder after template cleanup."""

import json
import unreal


EXPECTED_ASSETS = {
    "/Game/Drone/Maps/Lvl_DronePrototype": "World",
    "/Game/Drone/Maps/Lvl_DroneTraining": "World",
    "/Game/Drone/Maps/Lvl_DronePackShowcase": "World",
    "/Game/Drone/Maps/Lvl_DronePackShowcase_BuiltData": "MapBuildDataRegistry",
}

REMOVED_ROOTS = (
    "/Game/ThirdPerson",
    "/Game/Variant_Combat",
    "/Game/Variant_Platforming",
    "/Game/Variant_SideScrolling",
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

remaining_removed_roots = {
    root: [str(item.package_name) for item in registry.get_assets_by_path(root, recursive=True) or []]
    for root in REMOVED_ROOTS
}
remaining_removed_roots = {
    root: packages for root, packages in remaining_removed_roots.items() if packages
}
if remaining_removed_roots:
    raise RuntimeError(f"Removed template assets remain: {remaining_removed_roots}")

old_assets_still_present = [
    package_name
    for package_name in REMOVED_ASSET_PATHS
    if unreal.EditorAssetLibrary.does_asset_exist(package_name)
]
if old_assets_still_present:
    raise RuntimeError(f"Old map paths still exist: {old_assets_still_present}")

result = {
    "central_map_assets": loaded,
    "removed_roots_absent": list(REMOVED_ROOTS),
    "old_map_paths_absent": list(REMOVED_ASSET_PATHS),
}

unreal.log("DRONE_MAP_ORGANIZATION_VALIDATION_JSON_BEGIN")
unreal.log(json.dumps(result, ensure_ascii=False, indent=2))
unreal.log("DRONE_MAP_ORGANIZATION_VALIDATION_JSON_END")

