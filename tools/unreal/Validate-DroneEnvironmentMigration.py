"""Validate the three cleaned environment maps migrated into Drone."""

import json
from collections import deque

import unreal


ENVIRONMENTS = {
    "Battlefield": {
        "map": "/Game/Drone/Maps/Lvl_Battlefield",
        "vendor_root": "/Game/Battlefield",
        "compatibility": {
            "/Game/Characters/Heroes/Mannequin/Meshes/SKM_Manny",
            "/Game/Characters/Heroes/Mannequin/Meshes/SKM_Quinn",
        },
        "expected_vendor_assets": 710,
    },
    "MilitaryCamp": {
        "map": "/Game/Drone/Maps/Lvl_MilitaryCamp",
        "vendor_root": "/Game/FC_MilitaryCamp",
        "compatibility": set(),
        "expected_vendor_assets": 593,
    },
    "MilitaryBase": {
        "map": "/Game/Drone/Maps/Lvl_MilitaryBase",
        "vendor_root": "/Game/MillitaryBase",
        "compatibility": {"/Game/Textures/T_Linear_Grad"},
        "expected_vendor_assets": 1414,
    },
}

REMOVED_STARTER_MAPS = (
    "/Game/ThirdPerson/Lvl_ThirdPerson",
    "/Game/Variant_Combat/Lvl_Combat",
    "/Game/Variant_Platforming/Lvl_Platforming",
    "/Game/Variant_SideScrolling/Lvl_SideScrolling",
)


def dependency_options():
    return unreal.AssetRegistryDependencyOptions(
        include_soft_package_references=True,
        include_hard_package_references=True,
        include_searchable_names=False,
        include_soft_management_references=False,
        include_hard_management_references=False,
    )


def transitive_dependencies(registry, root_package, options):
    visited = set()
    queue = deque([root_package])
    while queue:
        package = queue.popleft()
        if package in visited:
            continue
        visited.add(package)
        for dependency in registry.get_dependencies(package, options) or []:
            dependency_name = str(dependency)
            if dependency_name not in visited:
                queue.append(dependency_name)
    return visited


registry = unreal.AssetRegistryHelpers.get_asset_registry()
registry.wait_for_completion()
options = dependency_options()
result = {}

for name, spec in ENVIRONMENTS.items():
    map_package = spec["map"]
    vendor_root = spec["vendor_root"]
    compatibility = spec["compatibility"]
    world = unreal.EditorAssetLibrary.load_asset(map_package)
    if world is None or world.get_class().get_name() != "World":
        raise RuntimeError(f"Environment map failed to load: {map_package}")

    world_settings = world.get_world_settings()
    default_game_mode = world_settings.get_editor_property("default_game_mode")
    if default_game_mode is not None:
        raise RuntimeError(
            f"Vendor GameMode remains on {map_package}: {default_game_mode}"
        )

    dependencies = transitive_dependencies(registry, map_package, options)
    game_dependencies = sorted(
        package for package in dependencies if package.startswith("/Game/")
    )
    missing = sorted(
        package
        for package in game_dependencies
        if not registry.get_assets_by_package_name(package, True)
    )
    if missing:
        raise RuntimeError(f"Missing dependencies for {map_package}: {missing}")

    disallowed = sorted(
        package
        for package in game_dependencies
        if package != map_package
        and not package.startswith(vendor_root + "/")
        and package not in compatibility
    )
    if disallowed:
        raise RuntimeError(
            f"Unexpected external dependencies for {map_package}: {disallowed}"
        )

    vendor_assets = registry.get_assets_by_path(vendor_root, recursive=True) or []
    if len(vendor_assets) != spec["expected_vendor_assets"]:
        raise RuntimeError(
            f"Vendor asset count mismatch for {vendor_root}: "
            f"expected={spec['expected_vendor_assets']}, actual={len(vendor_assets)}"
        )

    result[name] = {
        "map": map_package,
        "vendor_root": vendor_root,
        "vendor_asset_count": len(vendor_assets),
        "game_dependency_count": len(game_dependencies),
        "compatibility_assets": sorted(compatibility),
        "missing_dependency_count": len(missing),
        "unexpected_external_dependency_count": len(disallowed),
    }

starter_maps_still_present = [
    package
    for package in REMOVED_STARTER_MAPS
    if unreal.EditorAssetLibrary.does_asset_exist(package)
]
if starter_maps_still_present:
    raise RuntimeError(f"Starter maps still exist: {starter_maps_still_present}")

unreal.log("DRONE_ENVIRONMENT_MIGRATION_VALIDATION_JSON_BEGIN")
unreal.log(json.dumps(result, ensure_ascii=False, indent=2))
unreal.log("DRONE_ENVIRONMENT_MIGRATION_VALIDATION_JSON_END")
