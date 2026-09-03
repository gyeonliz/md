"""Create or validate the first FLOW-01 Mission/Drone data assets."""

from __future__ import annotations

import os
import traceback

import unreal


PREFIX = "DRONE_FLOW_DATA"
VALIDATE_ONLY = os.environ.get("DRONE_FLOW_DATA_VALIDATE_ONLY") == "1"
DRONE_PATH = "/Game/Drone/Data/Drones/DA_Drone_Scout_Greybox"
MISSION_PATH = "/Game/Drone/Data/Missions/DA_Mission_Tutorial_Training"
PAWN_CLASS_PATH = "/Game/Drone/Prototype/Blueprints/BP_DronePrototypePawn.BP_DronePrototypePawn_C"
MAP_PATH = "/Game/Drone/Maps/Lvl_DroneTraining"
DRONE_ID = unreal.Name("Drone.Scout.Greybox")
MISSION_ID = unreal.Name("Mission.Tutorial.Training")


def log(message: str) -> None:
    unreal.log(f"{PREFIX}|{message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def asset_name(path: str) -> str:
    return path.rsplit("/", 1)[-1]


def asset_folder(path: str) -> str:
    return path.rsplit("/", 1)[0]


def ensure_data_asset(
    editor_assets: unreal.EditorAssetSubsystem,
    path: str,
    asset_class: unreal.Class,
) -> unreal.DataAsset:
    existing = editor_assets.load_asset(path)
    if existing is not None:
        require(existing.get_class() == asset_class, f"Asset class mismatch: {path}")
        return existing
    require(not VALIDATE_ONLY, f"Required FLOW data asset is missing: {path}")

    factory = unreal.DataAssetFactory()
    factory.set_editor_property("data_asset_class", asset_class)
    created = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name(path),
        asset_folder(path),
        asset_class,
        factory,
        overwrite_existing=False,
    )
    require(created is not None, f"Could not create FLOW data asset: {path}")
    log(f"CREATED|{path}")
    return created


def configure_assets(
    editor_assets: unreal.EditorAssetSubsystem,
    drone: unreal.DataAsset,
    mission: unreal.DataAsset,
) -> None:
    pawn_class = unreal.load_class(None, PAWN_CLASS_PATH)
    mission_map = editor_assets.load_asset(MAP_PATH)
    require(pawn_class is not None, f"Prototype Pawn class is missing: {PAWN_CLASS_PATH}")
    require(mission_map is not None, f"Training Map is missing: {MAP_PATH}")

    drone.set_editor_properties(
        {
            "drone_id": DRONE_ID,
            "display_name": "정찰 드론 (훈련용)",
            "description": "첫 Front-end 흐름을 검증하는 Prototype 정찰 드론입니다.",
            "pawn_class": pawn_class,
            "locked": False,
        }
    )
    mission.set_editor_properties(
        {
            "mission_id": MISSION_ID,
            "display_name": "기본 비행 훈련",
            "lobby_description": "Gate 순서와 조작을 익히는 첫 Tutorial Mission입니다.",
            "region_text": "훈련 구역",
            "difficulty_text": "기초",
            "mission_map": mission_map,
            "allowed_drone_ids": [DRONE_ID],
            "default_drone_id": DRONE_ID,
            "initial_objectives": ["Gate 0부터 Gate 3까지 순서대로 통과"],
        }
    )

    require(editor_assets.save_loaded_asset(drone, only_if_is_dirty=False), f"Could not save: {DRONE_PATH}")
    require(editor_assets.save_loaded_asset(mission, only_if_is_dirty=False), f"Could not save: {MISSION_PATH}")


def validate_assets(
    editor_assets: unreal.EditorAssetSubsystem,
    drone: unreal.DataAsset,
    mission: unreal.DataAsset,
) -> None:
    pawn_class = unreal.load_class(None, PAWN_CLASS_PATH)
    mission_map = editor_assets.load_asset(MAP_PATH)
    require(drone.get_editor_property("drone_id") == DRONE_ID, "Drone ID mismatch")
    require(not drone.get_editor_property("locked"), "Greybox Drone must be selectable")
    require(drone.get_editor_property("pawn_class") == pawn_class, "Drone PawnClass mismatch")
    require(bool(drone.is_definition_valid()), "Drone Definition validation failed")

    require(mission.get_editor_property("mission_id") == MISSION_ID, "Mission ID mismatch")
    require(mission.get_editor_property("mission_map") == mission_map, "Mission Map mismatch")
    allowed_ids = list(mission.get_editor_property("allowed_drone_ids"))
    require(allowed_ids == [DRONE_ID], f"Allowed Drone IDs mismatch: {allowed_ids}")
    require(mission.get_editor_property("default_drone_id") == DRONE_ID, "Default Drone ID mismatch")
    require(len(mission.get_editor_property("initial_objectives")) == 1, "Initial objective count mismatch")
    require(bool(mission.is_definition_valid()), "Mission Definition validation failed")
    log(f"VALIDATED_DRONE|{DRONE_PATH}|id={DRONE_ID}")
    log(f"VALIDATED_MISSION|{MISSION_PATH}|id={MISSION_ID}|map={MAP_PATH}|allowed=1")
    log("VALIDATION_OK")


def main() -> None:
    editor_assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    drone_class = unreal.load_class(None, "/Script/Drone.DroneDefinition")
    mission_class = unreal.load_class(None, "/Script/Drone.DroneMissionDefinition")
    require(editor_assets is not None, "Editor Asset Subsystem is unavailable")
    require(drone_class is not None, "DroneDefinition class is unavailable")
    require(mission_class is not None, "DroneMissionDefinition class is unavailable")

    drone = ensure_data_asset(editor_assets, DRONE_PATH, drone_class)
    mission = ensure_data_asset(editor_assets, MISSION_PATH, mission_class)
    if not VALIDATE_ONLY:
        configure_assets(editor_assets, drone, mission)
        log("CREATED_OK")
    validate_assets(editor_assets, drone, mission)


try:
    main()
except Exception as error:
    log(f"FAILED|{error}")
    unreal.log_error(traceback.format_exc())
    raise

