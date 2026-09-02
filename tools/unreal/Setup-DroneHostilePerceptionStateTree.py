"""Upgrade and validate the AI-PER-01 hostile perception StateTree contract."""

from __future__ import annotations

import os
import traceback

import unreal


PREFIX = "DRONE_HOSTILE_PERCEPTION"
ASSET_PATH = "/Game/Drone/AI/StateTrees/ST_NPC_HostilePatrol"


def log(message: str) -> None:
    unreal.log(f"{PREFIX}|{message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def main() -> None:
    validate_only = os.environ.get("DRONE_HOSTILE_PERCEPTION_VALIDATE_ONLY") == "1"
    editor_assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    require(editor_assets is not None, "EditorAssetSubsystem unavailable")
    require(editor_assets.does_asset_exist(ASSET_PATH), f"Missing hostile StateTree: {ASSET_PATH}")

    if not validate_only:
        require(
            unreal.DroneAIStateTreeAuthoringLibrary.upgrade_hostile_patrol_state_tree_for_perception(ASSET_PATH),
            f"Could not safely upgrade hostile perception StateTree: {ASSET_PATH}",
        )
        asset = editor_assets.load_asset(ASSET_PATH)
        require(asset is not None, f"Upgraded StateTree did not load: {ASSET_PATH}")
        require(
            editor_assets.save_loaded_asset(asset, only_if_is_dirty=False),
            f"Could not save hostile perception StateTree: {ASSET_PATH}",
        )
        log(f"UPGRADED|{ASSET_PATH}")

    require(
        unreal.DroneAIStateTreeAuthoringLibrary.validate_hostile_perception_state_tree(ASSET_PATH),
        f"Hostile perception StateTree contract mismatch: {ASSET_PATH}",
    )
    log(f"VALIDATED|{ASSET_PATH}")
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
