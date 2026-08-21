"""Update existing Drone Prototype input assets to the confirmed camera/gamepad contract."""

from __future__ import annotations

import importlib.util
import pathlib
import traceback

import unreal


def load_setup_module():
    setup_path = pathlib.Path(__file__).with_name("Setup-DronePrototype.py")
    spec = importlib.util.spec_from_file_location("drone_prototype_setup", setup_path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load setup helpers: {setup_path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def main() -> None:
    setup = load_setup_module()
    editor_assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    setup.require(editor_assets is not None, "EditorAssetSubsystem is unavailable")

    existing_required = (
        "move",
        "altitude",
        "yaw",
        "look",
        "imc",
        "pawn_bp",
        "game_mode_bp",
        "map",
    )
    missing = [
        setup.ASSET_PATHS[name]
        for name in existing_required
        if not editor_assets.does_asset_exist(setup.ASSET_PATHS[name])
    ]
    setup.require(not missing, "Missing existing Prototype assets: " + ", ".join(missing))

    actions = {
        name: unreal.load_asset(setup.ASSET_PATHS[name])
        for name in ("move", "altitude", "yaw", "look")
    }
    camera_pitch_path = setup.ASSET_PATHS["camera_pitch_rate"]
    camera_pitch_rate = unreal.load_asset(camera_pitch_path)
    if camera_pitch_rate is None:
        camera_pitch_rate = setup.create_data_asset(camera_pitch_path, unreal.InputAction.static_class())
    actions["camera_pitch_rate"] = camera_pitch_rate

    actions["move"].set_editor_property("value_type", unreal.InputActionValueType.AXIS2D)
    actions["altitude"].set_editor_property("value_type", unreal.InputActionValueType.AXIS1D)
    actions["yaw"].set_editor_property("value_type", unreal.InputActionValueType.AXIS1D)
    actions["look"].set_editor_property("value_type", unreal.InputActionValueType.AXIS2D)
    actions["camera_pitch_rate"].set_editor_property("value_type", unreal.InputActionValueType.AXIS1D)

    context = unreal.load_asset(setup.ASSET_PATHS["imc"])
    setup.require(context is not None, "Prototype Input Mapping Context is unavailable")
    mapping_data = unreal.InputMappingContextMappingData()
    mapping_data.set_editor_property("mappings", setup.build_mappings(context, actions))
    context.set_editor_property("default_key_mappings", mapping_data)

    for action in actions.values():
        setup.save_asset(editor_assets, action)
    setup.save_asset(editor_assets, context)

    pawn_blueprint = unreal.load_asset(setup.ASSET_PATHS["pawn_bp"])
    setup.require(pawn_blueprint is not None, "Prototype Pawn Blueprint is unavailable")
    pawn_cdo = unreal.get_default_object(pawn_blueprint.generated_class())
    pawn_cdo.set_editor_property("camera_pitch_rate_action", camera_pitch_rate)
    setup.compile_blueprint(pawn_blueprint)
    setup.save_asset(editor_assets, pawn_blueprint)

    setup.validate_assets()
    setup.log("CONTROLS_UPDATED_OK")


try:
    main()
except Exception as error:
    unreal.log_error(f"DRONE_CONTROL_UPDATE|FAILED|{error}")
    unreal.log_error(traceback.format_exc())
    raise
