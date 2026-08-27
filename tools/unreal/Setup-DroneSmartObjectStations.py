"""Create or validate the AI-SO-01 Smart Object Definitions and Station Blueprints.

The script owns only the exact assets listed in SPECS. Existing assets are reused after
type/parent checks, then brought back to the documented one-slot contract. Set
DRONE_SMART_OBJECT_VALIDATE_ONLY=1 for a read-only validation pass.
"""

from __future__ import annotations

import os
import traceback

import unreal


PREFIX = "DRONE_SO_SETUP"
DEFINITION_FOLDER = "/Game/Drone/AI/SmartObjects/Definitions"
BLUEPRINT_FOLDER = "/Game/Drone/AI/SmartObjects/Blueprints"
STATION_NATIVE_PATH = "/Script/Drone.DroneSmartObjectStation"
MG_MESH_PATH = "/Game/Drone/ThirdParty/GroundDroneKit/Meshes/Alt_Turrets/MG_Turret/MG_Turret_SK"

SPECS = (
    {
        "name": "EnemyPatrol",
        "tag": "Drone.SmartObject.Activity.EnemyPatrol",
        "activity": unreal.DroneSmartObjectActivity.ENEMY_PATROL,
    },
    {
        "name": "FriendlyBasePatrol",
        "tag": "Drone.SmartObject.Activity.FriendlyBasePatrol",
        "activity": unreal.DroneSmartObjectActivity.FRIENDLY_BASE_PATROL,
    },
    {
        "name": "Ambient",
        "tag": "Drone.SmartObject.Activity.Ambient",
        "activity": unreal.DroneSmartObjectActivity.AMBIENT,
    },
    {
        "name": "Guard",
        "tag": "Drone.SmartObject.Activity.Guard",
        "activity": unreal.DroneSmartObjectActivity.GUARD,
    },
    {
        "name": "Cover",
        "tag": "Drone.SmartObject.Activity.Cover",
        "activity": unreal.DroneSmartObjectActivity.COVER,
    },
    {
        "name": "MGTurret",
        "tag": "Drone.SmartObject.Activity.MGTurret",
        "activity": unreal.DroneSmartObjectActivity.MG_TURRET,
    },
)


def log(message: str) -> None:
    unreal.log(f"{PREFIX}|{message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def definition_path(spec: dict[str, object]) -> str:
    return f"{DEFINITION_FOLDER}/SO_Def_{spec['name']}"


def blueprint_path(spec: dict[str, object]) -> str:
    return f"{BLUEPRINT_FOLDER}/BP_SO_{spec['name']}"


def asset_name(path: str) -> str:
    return path.rsplit("/", 1)[1]


def asset_folder(path: str) -> str:
    return path.rsplit("/", 1)[0]


def tag_container(tag_name: str) -> unreal.GameplayTagContainer:
    # ImportText를 쓰면 Native Gameplay Tag를 문자열 오타 없이 정확한 Struct로 만든다.
    value = unreal.GameplayTagContainer()
    value.import_text(f'(GameplayTags=((TagName="{tag_name}")))')
    require(tag_name in value.export_text(), f"Could not build Gameplay Tag container: {tag_name}")
    return value


def compile_blueprint(blueprint: unreal.Blueprint) -> None:
    unreal.BlueprintEditorLibrary.compile_blueprint(blueprint)
    require(
        blueprint.get_editor_property("status") == unreal.BlueprintStatus.BS_UP_TO_DATE,
        f"Blueprint did not compile cleanly: {blueprint.get_path_name()}",
    )


def save_asset(editor_assets: unreal.EditorAssetSubsystem, asset: unreal.Object) -> None:
    require(
        editor_assets.save_loaded_asset(asset, only_if_is_dirty=False),
        f"Could not save asset: {asset.get_path_name()}",
    )


def create_or_load_definition(
    editor_assets: unreal.EditorAssetSubsystem,
    spec: dict[str, object],
) -> unreal.SmartObjectDefinition:
    path = definition_path(spec)
    existing = editor_assets.load_asset(path) if editor_assets.does_asset_exist(path) else None
    if existing is not None:
        require(
            isinstance(existing, unreal.SmartObjectDefinition),
            f"Existing asset is not a SmartObjectDefinition: {path}",
        )
        log(f"REUSED_DEFINITION|{path}")
        return existing

    factory = unreal.DataAssetFactory()
    factory.set_editor_property("data_asset_class", unreal.SmartObjectDefinition.static_class())
    created = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name(path),
        asset_folder(path),
        unreal.SmartObjectDefinition.static_class(),
        factory,
        overwrite_existing=False,
    )
    require(created is not None, f"Could not create SmartObjectDefinition: {path}")
    log(f"CREATED_DEFINITION|{path}")
    return created


def configure_definition(
    editor_assets: unreal.EditorAssetSubsystem,
    definition: unreal.SmartObjectDefinition,
    spec: dict[str, object],
) -> None:
    # AI-SO-01은 검색·Claim 가능한 최소 Definition을 만든다. 실제 Interaction
    # StateTree는 AI-PATROL-01/AI-FRIEND-01에서 이 Behavior에 연결한다.
    behavior = unreal.GameplayInteractionSmartObjectBehaviorDefinition(outer=definition)
    # Slot Struct의 필드는 BlueprintReadOnly라 생성 뒤 수정할 수 없고 생성자에서 채워야 한다.
    slot = unreal.SmartObjectSlotDefinition(
        activity_tags=tag_container(str(spec["tag"])),
        behavior_definitions=[behavior],
    )

    definition.set_editor_property("slots", [slot])
    save_asset(editor_assets, definition)


def create_or_load_blueprint(
    editor_assets: unreal.EditorAssetSubsystem,
    station_native: unreal.Class,
    spec: dict[str, object],
) -> unreal.Blueprint:
    path = blueprint_path(spec)
    existing = editor_assets.load_asset(path) if editor_assets.does_asset_exist(path) else None
    if existing is not None:
        require(isinstance(existing, unreal.Blueprint), f"Existing asset is not a Blueprint: {path}")
        blueprint = existing
        log(f"REUSED_BLUEPRINT|{path}")
    else:
        factory = unreal.BlueprintFactory()
        factory.set_editor_property("parent_class", station_native)
        blueprint = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            asset_name(path),
            asset_folder(path),
            unreal.Blueprint.static_class(),
            factory,
            overwrite_existing=False,
        )
        require(blueprint is not None, f"Could not create Station Blueprint: {path}")
        log(f"CREATED_BLUEPRINT|{path}")

    require(
        unreal.BlueprintEditorLibrary.get_blueprint_parent_class(blueprint) == station_native,
        f"Station Blueprint has the wrong parent: {path}",
    )
    compile_blueprint(blueprint)
    return blueprint


def configure_blueprint(
    editor_assets: unreal.EditorAssetSubsystem,
    blueprint: unreal.Blueprint,
    definition: unreal.SmartObjectDefinition,
    spec: dict[str, object],
    mg_mesh: unreal.SkeletalMesh,
) -> None:
    cdo = unreal.get_default_object(blueprint.generated_class())
    require(cdo is not None, f"Station Blueprint CDO is unavailable: {blueprint.get_path_name()}")
    cdo.set_editor_property("activity", spec["activity"])

    cdo.set_smart_object_definition(definition)
    cdo.set_station_skeletal_mesh(mg_mesh if spec["name"] == "MGTurret" else None)

    save_asset(editor_assets, blueprint)


def validate_definition(definition: unreal.SmartObjectDefinition, spec: dict[str, object]) -> None:
    slots = list(definition.get_editor_property("slots"))
    require(len(slots) == 1, f"Definition must have exactly one Slot: {definition.get_path_name()}")
    slot = slots[0]
    require(bool(slot.get_editor_property("enabled")), "Smart Object Slot must start enabled")
    activity_text = slot.get_editor_property("activity_tags").export_text()
    require(str(spec["tag"]) in activity_text, f"Activity Tag mismatch: {definition.get_path_name()}")
    behaviors = list(slot.get_editor_property("behavior_definitions"))
    require(len(behaviors) == 1, f"Definition must have one Gameplay Interaction Behavior: {definition.get_path_name()}")
    require(
        isinstance(behaviors[0], unreal.GameplayInteractionSmartObjectBehaviorDefinition),
        f"Definition Behavior type mismatch: {definition.get_path_name()}",
    )


def validate_blueprint(
    blueprint: unreal.Blueprint,
    definition: unreal.SmartObjectDefinition,
    spec: dict[str, object],
    mg_mesh: unreal.SkeletalMesh,
) -> None:
    compile_blueprint(blueprint)
    cdo = unreal.get_default_object(blueprint.generated_class())
    require(cdo.get_editor_property("activity") == spec["activity"], f"Station Activity mismatch: {blueprint.get_path_name()}")

    require(
        cdo.get_smart_object_definition() == definition,
        f"Station Definition mismatch: {blueprint.get_path_name()}",
    )

    expected_mesh = mg_mesh if spec["name"] == "MGTurret" else None
    require(
        cdo.get_station_skeletal_mesh() == expected_mesh,
        f"Station Mesh mismatch: {blueprint.get_path_name()}",
    )


def main() -> None:
    editor_assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    require(editor_assets is not None, "EditorAssetSubsystem is unavailable")
    station_native = unreal.load_class(None, STATION_NATIVE_PATH)
    require(station_native is not None, "Native DroneSmartObjectStation Class is unavailable")
    mg_mesh = unreal.load_asset(MG_MESH_PATH)
    require(isinstance(mg_mesh, unreal.SkeletalMesh), f"MG Turret Skeletal Mesh is unavailable: {MG_MESH_PATH}")

    validate_only = os.environ.get("DRONE_SMART_OBJECT_VALIDATE_ONLY") == "1"
    definitions: dict[str, unreal.SmartObjectDefinition] = {}
    blueprints: dict[str, unreal.Blueprint] = {}

    for spec in SPECS:
        path = definition_path(spec)
        if validate_only:
            definition = editor_assets.load_asset(path)
            require(isinstance(definition, unreal.SmartObjectDefinition), f"Missing Definition: {path}")
        else:
            definition = create_or_load_definition(editor_assets, spec)
            configure_definition(editor_assets, definition, spec)
        definitions[str(spec["name"])] = definition

        bp_path = blueprint_path(spec)
        if validate_only:
            blueprint = editor_assets.load_asset(bp_path)
            require(isinstance(blueprint, unreal.Blueprint), f"Missing Station Blueprint: {bp_path}")
        else:
            blueprint = create_or_load_blueprint(editor_assets, station_native, spec)
            configure_blueprint(editor_assets, blueprint, definition, spec, mg_mesh)
        blueprints[str(spec["name"])] = blueprint

    for spec in SPECS:
        name = str(spec["name"])
        validate_definition(definitions[name], spec)
        validate_blueprint(blueprints[name], definitions[name], spec, mg_mesh)
        log(f"VALIDATED_PAIR|{definition_path(spec)}|{blueprint_path(spec)}")

    log("VALIDATION_OK")
    if not validate_only:
        log("CREATED_OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(f"{PREFIX}|FAILED|{exc}")
        unreal.log_error(traceback.format_exc())
        raise
