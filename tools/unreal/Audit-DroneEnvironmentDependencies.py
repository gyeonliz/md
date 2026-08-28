"""Report project-owned dependencies added to the three central environment maps.

This script never saves assets. It is intentionally separate from the strict
validator so a teammate map change can be inspected before the allow-list is
updated.
"""

from __future__ import annotations

import json
from collections import deque

import unreal


ENVIRONMENTS = {
    "Battlefield": ("/Game/Drone/Maps/Lvl_Battlefield", "/Game/Battlefield"),
    "MilitaryCamp": ("/Game/Drone/Maps/Lvl_MilitaryCamp", "/Game/FC_MilitaryCamp"),
    "MilitaryBase": ("/Game/Drone/Maps/Lvl_MilitaryBase", "/Game/MillitaryBase"),
}


def dependency_options() -> unreal.AssetRegistryDependencyOptions:
    return unreal.AssetRegistryDependencyOptions(
        include_soft_package_references=True,
        include_hard_package_references=True,
        include_searchable_names=False,
        include_soft_management_references=False,
        include_hard_management_references=False,
    )


def transitive_dependencies(registry, root_package: str, options) -> set[str]:
    visited: set[str] = set()
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
report = {}

for name, (map_package, vendor_root) in ENVIRONMENTS.items():
    world = unreal.EditorAssetLibrary.load_asset(map_package)
    if world is None or world.get_class().get_name() != "World":
        raise RuntimeError(f"Environment map failed to load: {map_package}")

    dependencies = transitive_dependencies(registry, map_package, options)
    external = sorted(
        package
        for package in dependencies
        if package.startswith("/Game/")
        and package != map_package
        and not package.startswith(vendor_root + "/")
    )
    external_assets = []
    for package in external:
        assets = registry.get_assets_by_package_name(package, True) or []
        external_assets.append(
            {
                "package": package,
                "classes": sorted({str(asset.asset_class_path) for asset in assets}),
                "missing": not bool(assets),
            }
        )

    report[name] = {
        "map": map_package,
        "external_dependency_count": len(external_assets),
        "external_dependencies": external_assets,
    }

unreal.log("DRONE_ENVIRONMENT_DEPENDENCY_AUDIT_JSON_BEGIN")
unreal.log(json.dumps(report, ensure_ascii=False, indent=2))
unreal.log("DRONE_ENVIRONMENT_DEPENDENCY_AUDIT_JSON_END")
