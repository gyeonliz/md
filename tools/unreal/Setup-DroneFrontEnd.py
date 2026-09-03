"""Create or validate the FLOW-02 Front-end Blueprint host and map."""

from __future__ import annotations

import os
import traceback

import unreal


PREFIX = "DRONE_FRONTEND"
VALIDATE_ONLY = os.environ.get("DRONE_FRONTEND_VALIDATE_ONLY") == "1"
WIDGET_PATH = "/Game/Drone/FrontEnd/UI/WBP_DroneFrontEndRoot"
CONTROLLER_PATH = "/Game/Drone/FrontEnd/Blueprints/BP_DroneFrontEndPlayerController"
GAME_MODE_PATH = "/Game/Drone/FrontEnd/Blueprints/BP_DroneFrontEndGameMode"
MAP_PATH = "/Game/Drone/Maps/Lvl_DroneFrontEnd"


def log(message: str) -> None:
    unreal.log(f"{PREFIX}|{message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def asset_name(path: str) -> str:
    return path.rsplit("/", 1)[-1]


def asset_folder(path: str) -> str:
    return path.rsplit("/", 1)[0]


def create_blueprint(path: str, parent_class: unreal.Class) -> unreal.Blueprint:
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", parent_class)
    blueprint = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name(path),
        asset_folder(path),
        unreal.Blueprint,
        factory,
        overwrite_existing=False,
    )
    require(blueprint is not None, f"Could not create Blueprint: {path}")
    log(f"CREATED|{path}")
    return blueprint


def create_widget_blueprint(path: str, parent_class: unreal.Class) -> unreal.WidgetBlueprint:
    factory = unreal.WidgetBlueprintFactory()
    factory.set_editor_property("parent_class", parent_class)
    blueprint = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name(path),
        asset_folder(path),
        None,
        factory,
        overwrite_existing=False,
    )
    require(blueprint is not None, f"Could not create Widget Blueprint: {path}")
    log(f"CREATED|{path}")
    return blueprint


def save_asset(editor_assets: unreal.EditorAssetSubsystem, asset: unreal.Object) -> None:
    require(
        editor_assets.save_loaded_asset(asset, only_if_is_dirty=False),
        f"Could not save asset: {asset.get_path_name()}",
    )


def create_assets(editor_assets: unreal.EditorAssetSubsystem) -> None:
    existing = [
        path
        for path in (WIDGET_PATH, CONTROLLER_PATH, GAME_MODE_PATH, MAP_PATH)
        if editor_assets.does_asset_exist(path)
    ]
    require(not existing, "Refusing to overwrite existing Front-end assets: " + ", ".join(existing))

    widget_native = unreal.load_class(None, "/Script/Drone.DroneFrontEndRootWidget")
    controller_native = unreal.load_class(None, "/Script/Drone.DroneFrontEndPlayerController")
    game_mode_native = unreal.load_class(None, "/Script/Drone.DroneFrontEndGameMode")
    require(widget_native is not None, "Native Front-end Widget class is unavailable; build C++ first")
    require(controller_native is not None, "Native Front-end Controller class is unavailable; build C++ first")
    require(game_mode_native is not None, "Native Front-end GameMode class is unavailable; build C++ first")

    widget_blueprint = create_widget_blueprint(WIDGET_PATH, widget_native)
    save_asset(editor_assets, widget_blueprint)

    controller_blueprint = create_blueprint(CONTROLLER_PATH, controller_native)
    controller_cdo = unreal.get_default_object(controller_blueprint.generated_class())
    controller_cdo.set_editor_property("front_end_widget_class", widget_blueprint.generated_class())
    save_asset(editor_assets, controller_blueprint)

    game_mode_blueprint = create_blueprint(GAME_MODE_PATH, game_mode_native)
    game_mode_cdo = unreal.get_default_object(game_mode_blueprint.generated_class())
    game_mode_cdo.set_editor_property("player_controller_class", controller_blueprint.generated_class())
    game_mode_cdo.set_editor_property("default_pawn_class", None)
    save_asset(editor_assets, game_mode_blueprint)

    level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_worlds = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    require(level_editor is not None, "LevelEditorSubsystem is unavailable")
    require(editor_worlds is not None, "UnrealEditorSubsystem is unavailable")
    require(level_editor.new_level(MAP_PATH, False), "Could not create Front-end map")
    world = editor_worlds.get_editor_world()
    require(world is not None, "Front-end editor world is unavailable")
    world.get_world_settings().set_editor_property(
        "default_game_mode", game_mode_blueprint.generated_class()
    )
    require(level_editor.save_current_level(), "Could not save Front-end map")
    log(f"CREATED|{MAP_PATH}")
    log("CREATED_OK")


def validate_assets(editor_assets: unreal.EditorAssetSubsystem) -> None:
    widget_blueprint = editor_assets.load_asset(WIDGET_PATH)
    controller_blueprint = editor_assets.load_asset(CONTROLLER_PATH)
    game_mode_blueprint = editor_assets.load_asset(GAME_MODE_PATH)
    world = editor_assets.load_asset(MAP_PATH)
    require(widget_blueprint is not None, f"Widget Blueprint is missing: {WIDGET_PATH}")
    require(controller_blueprint is not None, f"Controller Blueprint is missing: {CONTROLLER_PATH}")
    require(game_mode_blueprint is not None, f"GameMode Blueprint is missing: {GAME_MODE_PATH}")
    require(world is not None, f"Front-end map is missing: {MAP_PATH}")

    widget_native = unreal.load_class(None, "/Script/Drone.DroneFrontEndRootWidget")
    controller_native = unreal.load_class(None, "/Script/Drone.DroneFrontEndPlayerController")
    game_mode_native = unreal.load_class(None, "/Script/Drone.DroneFrontEndGameMode")
    require(
        unreal.MathLibrary.class_is_child_of(widget_blueprint.generated_class(), widget_native),
        "Widget parent class mismatch",
    )
    require(
        unreal.MathLibrary.class_is_child_of(controller_blueprint.generated_class(), controller_native),
        "Controller parent class mismatch",
    )
    require(
        unreal.MathLibrary.class_is_child_of(game_mode_blueprint.generated_class(), game_mode_native),
        "GameMode parent class mismatch",
    )

    controller_cdo = unreal.get_default_object(controller_blueprint.generated_class())
    require(
        controller_cdo.get_editor_property("front_end_widget_class") == widget_blueprint.generated_class(),
        "Controller Widget Class mismatch",
    )
    game_mode_cdo = unreal.get_default_object(game_mode_blueprint.generated_class())
    require(game_mode_cdo.get_editor_property("default_pawn_class") is None, "Front-end must not spawn a Pawn")
    require(
        game_mode_cdo.get_editor_property("player_controller_class")
        == controller_blueprint.generated_class(),
        "GameMode Controller Class mismatch",
    )
    require(
        world.get_world_settings().get_editor_property("default_game_mode")
        == game_mode_blueprint.generated_class(),
        "Front-end map GameMode mismatch",
    )
    log(
        "VALIDATED|widget=1|controller=1|game_mode=1|map=1|default_pawn=none|"
        "native_fallback=ready"
    )
    log("VALIDATION_OK")


def main() -> None:
    editor_assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    require(editor_assets is not None, "EditorAssetSubsystem is unavailable")
    if not VALIDATE_ONLY:
        create_assets(editor_assets)
    validate_assets(editor_assets)


try:
    main()
except Exception as error:
    log(f"FAILED|{error}")
    unreal.log_error(traceback.format_exc())
    raise
