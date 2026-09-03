"""Upgrade the Hostile StateTree for Cover and add two idempotent Greybox Cover stations."""

from __future__ import annotations

import os
import traceback

import unreal


PREFIX = "DRONE_HOSTILE_COVER"
STATE_TREE_PATH = "/Game/Drone/AI/StateTrees/ST_NPC_HostilePatrol"
MAP_PATH = "/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox"
COVER_BLUEPRINT_PATH = "/Game/Drone/AI/SmartObjects/Blueprints/BP_SO_Cover"
COVER_PLACEMENTS = (
    ("Station_Cover_A", (1750.0, -1050.0, 0.0), 150.0),
    ("Station_Cover_B", (1750.0, 1050.0, 0.0), 210.0),
)


def log(message: str) -> None:
    unreal.log(f"{PREFIX}|{message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def configure_state_tree(editor_assets: unreal.EditorAssetSubsystem, validate_only: bool) -> None:
    require(editor_assets.does_asset_exist(STATE_TREE_PATH), f"Missing StateTree: {STATE_TREE_PATH}")
    if not validate_only:
        require(
            unreal.DroneAIStateTreeAuthoringLibrary.upgrade_hostile_mg_turret_state_tree_for_cover(
                STATE_TREE_PATH
            ),
            f"Could not upgrade Hostile Cover StateTree: {STATE_TREE_PATH}",
        )
        state_tree = editor_assets.load_asset(STATE_TREE_PATH)
        require(state_tree is not None, f"Could not load upgraded StateTree: {STATE_TREE_PATH}")
        require(
            editor_assets.save_loaded_asset(state_tree, only_if_is_dirty=False),
            f"Could not save upgraded StateTree: {STATE_TREE_PATH}",
        )
        log(f"UPGRADED_STATE_TREE|{STATE_TREE_PATH}")

    require(
        unreal.DroneAIStateTreeAuthoringLibrary.validate_hostile_cover_state_tree(STATE_TREE_PATH),
        f"Hostile Cover StateTree contract mismatch: {STATE_TREE_PATH}",
    )
    log(f"VALIDATED_STATE_TREE|{STATE_TREE_PATH}")


def configure_cover_stations(
    editor_assets: unreal.EditorAssetSubsystem,
    validate_only: bool,
) -> None:
    level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    require(level_editor is not None and actors is not None, "Editor level subsystems unavailable")
    require(editor_assets.does_asset_exist(MAP_PATH), f"Missing Greybox map: {MAP_PATH}")
    require(level_editor.load_level(MAP_PATH), f"Could not load Greybox map: {MAP_PATH}")

    cover_blueprint = editor_assets.load_asset(COVER_BLUEPRINT_PATH)
    require(isinstance(cover_blueprint, unreal.Blueprint), f"Missing Cover Blueprint: {COVER_BLUEPRINT_PATH}")
    cover_class = cover_blueprint.generated_class()
    by_label = {actor.get_actor_label(): actor for actor in actors.get_all_level_actors()}

    for label, location, yaw in COVER_PLACEMENTS:
        station = by_label.get(label)
        if station is None and not validate_only:
            station = actors.spawn_actor_from_class(
                cover_class,
                unreal.Vector(*location),
                unreal.Rotator(pitch=0.0, yaw=yaw, roll=0.0),
            )
            require(station is not None, f"Could not spawn Cover station: {label}")
            station.set_actor_label(label)
            log(f"CREATED_COVER_STATION|{label}")

        require(station is not None, f"Missing Cover station: {label}")
        require(station.get_class() == cover_class, f"Cover station class mismatch: {label}")
        log(f"VALIDATED_COVER_STATION|{label}")

    if not validate_only:
        require(level_editor.save_current_level(), f"Could not save Greybox map: {MAP_PATH}")
        log(f"SAVED_MAP|{MAP_PATH}")


def main() -> None:
    validate_only = os.environ.get("DRONE_HOSTILE_COVER_VALIDATE_ONLY") == "1"
    editor_assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    require(editor_assets is not None, "EditorAssetSubsystem unavailable")
    configure_state_tree(editor_assets, validate_only)
    configure_cover_stations(editor_assets, validate_only)
    log("VALIDATION_OK")
    if not validate_only:
        log("UPGRADE_OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(f"{PREFIX}|FAILED|{exc}")
        unreal.log_error(traceback.format_exc())
        raise
