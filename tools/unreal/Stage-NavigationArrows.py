"""Move the six selected NavigationArrows packages inside a disposable stage.

The source files must first be copied to /Game/NavigationArrows without changing
their relative paths.  Unreal performs these moves so serialized references are
updated; moving the .uasset files in Explorer would not do that safely.
"""

import json
import unreal


SOURCE_ROOT = "/Game/NavigationArrows"
TARGET_ROOT = "/Game/Drone/ThirdParty/NavigationArrows"

# Dependencies are moved before the Widget Blueprint that consumes them.
MOVES = [
    ("Icons/NewTransparentArrow", "Icons/NewTransparentArrow"),
    ("Icons/TransparentArrow", "Icons/TransparentArrow"),
    ("InfoStructs/ImageInfo", "InfoStructs/ImageInfo"),
    ("InfoStructs/MovementInfo", "InfoStructs/MovementInfo"),
    ("InfoStructs/TextInfo", "InfoStructs/TextInfo"),
    ("Blueprints/NavigationArrow", "Blueprints/NavigationArrow"),
]


def asset_path(root, relative_path):
    return f"{root}/{relative_path}"


for relative_source, relative_target in MOVES:
    source = asset_path(SOURCE_ROOT, relative_source)
    target = asset_path(TARGET_ROOT, relative_target)
    if not unreal.EditorAssetLibrary.does_asset_exist(source):
        raise RuntimeError(f"Required source asset is missing: {source}")
    if unreal.EditorAssetLibrary.does_asset_exist(target):
        raise RuntimeError(f"Target asset already exists: {target}")

if not unreal.EditorAssetLibrary.make_directory(TARGET_ROOT):
    if not unreal.EditorAssetLibrary.does_directory_exist(TARGET_ROOT):
        raise RuntimeError(f"Could not create target directory: {TARGET_ROOT}")

moved = []
for relative_source, relative_target in MOVES:
    source = asset_path(SOURCE_ROOT, relative_source)
    target = asset_path(TARGET_ROOT, relative_target)
    if not unreal.EditorAssetLibrary.rename_asset(source, target):
        raise RuntimeError(f"Could not move {source} to {target}")
    moved.append({"source": source, "target": target})

# Source demo assets can become dirty when their references are updated.
if not unreal.EditorAssetLibrary.save_directory(
    TARGET_ROOT, only_if_is_dirty=False, recursive=True
):
    raise RuntimeError(f"Could not save target directory: {TARGET_ROOT}")
if not unreal.EditorAssetLibrary.save_directory(
    SOURCE_ROOT, only_if_is_dirty=True, recursive=True
):
    raise RuntimeError(f"Could not save changed source referencers: {SOURCE_ROOT}")

registry = unreal.AssetRegistryHelpers.get_asset_registry()
registry.wait_for_completion()
registry.scan_paths_synchronous([SOURCE_ROOT, TARGET_ROOT], force_rescan=True)

dependency_options = unreal.AssetRegistryDependencyOptions(
    include_soft_package_references=True,
    include_hard_package_references=True,
    include_searchable_names=False,
    include_soft_management_references=False,
    include_hard_management_references=False,
)

target_assets = sorted(
    str(item.package_name)
    for item in (registry.get_assets_by_path(TARGET_ROOT, recursive=True) or [])
)
forbidden_dependencies = {}
for package_name in target_assets:
    dependencies = registry.get_dependencies(package_name, dependency_options) or []
    forbidden = sorted(
        str(value)
        for value in dependencies
        if str(value).startswith(SOURCE_ROOT + "/")
    )
    if forbidden:
        forbidden_dependencies[package_name] = forbidden

result = {
    "moved": moved,
    "target_assets": target_assets,
    "forbidden_source_dependencies": forbidden_dependencies,
}

unreal.log("NAVIGATION_ARROWS_STAGE_JSON_BEGIN")
unreal.log(json.dumps(result, ensure_ascii=False, indent=2))
unreal.log("NAVIGATION_ARROWS_STAGE_JSON_END")

if len(target_assets) != len(MOVES):
    raise RuntimeError(
        f"Expected {len(MOVES)} target assets, found {len(target_assets)}"
    )
if forbidden_dependencies:
    raise RuntimeError(
        f"Moved assets still depend on the source root: {forbidden_dependencies}"
    )
