"""Read-only audit for centralized maps and retained template support assets.

Run from UnrealEditor-Cmd against the Drone project.  The script reports
dependencies of project maps and external referencers of each restored
template root. It never changes or saves an asset.
"""

import json
import unreal


PROJECT_MAPS = (
    "/Game/Drone/Maps/Lvl_DronePrototype",
    "/Game/Drone/Maps/Lvl_DroneTraining",
    "/Game/Drone/Maps/Lvl_DronePackShowcase",
    "/Game/Drone/Maps/Lvl_Battlefield",
    "/Game/Drone/Maps/Lvl_MilitaryCamp",
    "/Game/Drone/Maps/Lvl_MilitaryBase",
)

TEMPLATE_ROOTS = (
    "/Game/ThirdPerson",
    "/Game/Variant_Combat",
    "/Game/Variant_Platforming",
    "/Game/Variant_SideScrolling",
)


def dependency_options():
    return unreal.AssetRegistryDependencyOptions(
        include_soft_package_references=True,
        include_hard_package_references=True,
        include_searchable_names=False,
        include_soft_management_references=False,
        include_hard_management_references=False,
    )


registry = unreal.AssetRegistryHelpers.get_asset_registry()
registry.wait_for_completion()
options = dependency_options()

map_dependencies = {}
for map_package in PROJECT_MAPS:
    dependencies = registry.get_dependencies(map_package, options) or []
    map_dependencies[map_package] = sorted(
        str(package)
        for package in dependencies
        if str(package).startswith(TEMPLATE_ROOTS)
    )

root_results = {}
for template_root in TEMPLATE_ROOTS:
    assets = sorted(
        registry.get_assets_by_path(template_root, recursive=True) or [],
        key=lambda item: str(item.package_name),
    )
    outside_referencers = {}
    for asset_data in assets:
        package_name = str(asset_data.package_name)
        referencers = registry.get_referencers(package_name, options) or []
        outside = sorted(
            str(package)
            for package in referencers
            if not str(package).startswith(template_root + "/")
        )
        if outside:
            outside_referencers[package_name] = outside

    root_results[template_root] = {
        "asset_count": len(assets),
        "outside_referencers": outside_referencers,
    }

result = {
    "project_map_dependencies_on_template_roots": map_dependencies,
    "restored_template_roots": root_results,
}

unreal.log("DRONE_CONTENT_CLEANUP_AUDIT_JSON_BEGIN")
unreal.log(json.dumps(result, ensure_ascii=False, indent=2))
unreal.log("DRONE_CONTENT_CLEANUP_AUDIT_JSON_END")
