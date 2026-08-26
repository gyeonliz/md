"""Read-only dependency and class audit for the NavigationArrows vendor pack.

Run this inside a disposable Unreal Engine 5.8 staging project while the vendor
files still live under /Game/NavigationArrows.  The JSON markers make the
result easy to extract from an Unreal commandlet log.
"""

import json
import unreal


SOURCE_ROOT = "/Game/NavigationArrows"
TARGET_ROOT = "/Game/Drone/ThirdParty/NavigationArrows"

SOURCE_RELATIVE_PACKAGES = {
    "Blueprints/NavigationArrow",
    "Blueprints/NavigationArrowExampleActor",
    "Demo/Demo",
    "Demo/Demo_BuiltData",
    "Icons/NewTransparentArrow",
    "Icons/TransparentArrow",
    "Icons/TransparentCircle",
    "InfoStructs/ImageInfo",
    "InfoStructs/MovementInfo",
    "InfoStructs/TextInfo",
    "Meshes/ExampleMesh",
}

TARGET_RELATIVE_PACKAGES = {
    "Blueprints/NavigationArrow",
    "Icons/NewTransparentArrow",
    "Icons/TransparentArrow",
    "InfoStructs/ImageInfo",
    "InfoStructs/MovementInfo",
    "InfoStructs/TextInfo",
}


def path_name(value):
    """Return a stable Unreal object path without leaking Python repr details."""
    if value is None:
        return None
    try:
        return value.get_path_name()
    except Exception:
        return str(value)


def dependencies(registry, package_name, *, hard, soft):
    """Read package references with hard/soft categories kept separate."""
    options = unreal.AssetRegistryDependencyOptions(
        include_soft_package_references=soft,
        include_hard_package_references=hard,
        include_searchable_names=False,
        include_soft_management_references=False,
        include_hard_management_references=False,
    )
    values = registry.get_dependencies(package_name, options) or []
    return sorted(str(value) for value in values)


def referencers(registry, package_name):
    """Return package referencers using the explicit UE 5.8 options argument."""
    options = unreal.AssetRegistryDependencyOptions(
        include_soft_package_references=True,
        include_hard_package_references=True,
        include_searchable_names=False,
        include_soft_management_references=False,
        include_hard_management_references=False,
    )
    values = registry.get_referencers(package_name, options) or []
    return sorted(str(value) for value in values)


def blueprint_details(package_name, asset):
    """Collect Blueprint metadata defensively across Blueprint asset subclasses."""
    details = {}

    try:
        details["status"] = str(asset.get_editor_property("status"))
    except Exception:
        details["status"] = None

    try:
        details["parent_class"] = path_name(asset.get_editor_property("parent_class"))
    except Exception:
        details["parent_class"] = None

    generated_class = unreal.EditorAssetLibrary.load_blueprint_class(package_name)
    details["generated_class"] = path_name(generated_class)
    if generated_class is None:
        return details

    if details["parent_class"] is None:
        try:
            details["parent_class"] = path_name(generated_class.get_super_class())
        except Exception:
            pass

    default_object = unreal.get_default_object(generated_class)
    details["default_object_class"] = path_name(default_object.get_class())

    components = []
    if isinstance(default_object, unreal.Actor):
        for component in default_object.get_components_by_class(unreal.ActorComponent):
            entry = {
                "name": component.get_name(),
                "class": path_name(component.get_class()),
            }
            if isinstance(component, unreal.PrimitiveComponent):
                entry.update(
                    {
                        "collision_enabled": str(component.get_collision_enabled()),
                        "generate_overlap_events": bool(component.generate_overlap_events),
                        "can_ever_affect_navigation": bool(
                            component.can_ever_affect_navigation
                        ),
                        "simulate_physics": bool(component.is_simulating_physics()),
                    }
                )
            components.append(entry)
    details["actor_components"] = components
    return details


registry = unreal.AssetRegistryHelpers.get_asset_registry()
registry.wait_for_completion()

target_asset_data = registry.get_assets_by_path(TARGET_ROOT, recursive=True) or []
audit_root = TARGET_ROOT if target_asset_data else SOURCE_ROOT
expected_relative_packages = (
    TARGET_RELATIVE_PACKAGES if audit_root == TARGET_ROOT else SOURCE_RELATIVE_PACKAGES
)

asset_data_items = sorted(
    registry.get_assets_by_path(audit_root, recursive=True) or [],
    key=lambda item: str(item.package_name),
)

assets = []
load_failures = []
external_game_dependencies = set()

for asset_data in asset_data_items:
    package_name = str(asset_data.package_name)
    hard_dependencies = dependencies(registry, package_name, hard=True, soft=False)
    soft_dependencies = dependencies(registry, package_name, hard=False, soft=True)
    all_dependencies = sorted(set(hard_dependencies + soft_dependencies))

    for dependency in all_dependencies:
        if dependency.startswith("/Game/") and not dependency.startswith(
            audit_root + "/"
        ):
            external_game_dependencies.add(dependency)

    loaded_asset = asset_data.get_asset()
    if loaded_asset is None:
        load_failures.append(package_name)

    entry = {
        "package": package_name,
        "asset": str(asset_data.asset_name),
        "registry_class": str(asset_data.asset_class_path),
        "loaded_class": path_name(loaded_asset.get_class()) if loaded_asset else None,
        "hard_dependencies": hard_dependencies,
        "soft_dependencies": soft_dependencies,
        "referencers": referencers(registry, package_name),
    }

    if loaded_asset is not None and "Blueprint" in entry["registry_class"]:
        entry["blueprint"] = blueprint_details(package_name, loaded_asset)

    assets.append(entry)

result = {
    "audit_root": audit_root,
    "asset_count": len(assets),
    "assets": assets,
    "load_failures": load_failures,
    "external_game_dependencies": sorted(external_game_dependencies),
}

unreal.log("NAVIGATION_ARROWS_AUDIT_JSON_BEGIN")
unreal.log(json.dumps(result, ensure_ascii=False, indent=2))
unreal.log("NAVIGATION_ARROWS_AUDIT_JSON_END")

actual_relative_packages = {
    entry["package"][len(audit_root) + 1 :] for entry in assets
}
if actual_relative_packages != expected_relative_packages:
    raise RuntimeError(
        "NavigationArrows package set mismatch: "
        f"expected={sorted(expected_relative_packages)}, "
        f"actual={sorted(actual_relative_packages)}"
    )
if load_failures:
    raise RuntimeError(f"NavigationArrows load failures: {load_failures}")
