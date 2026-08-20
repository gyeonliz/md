"""Create or validate the asset-neutral Drone Prototype P1 assets in UE 5.8.

Create mode is the default. Set DRONE_PROTOTYPE_VALIDATE_ONLY=1 for a fresh-process,
read-only validation pass. The script never overwrites or deletes an existing asset.
"""

from __future__ import annotations

import os
import traceback

import unreal


ACTION_FOLDER = "/Game/Drone/Prototype/Input/Actions"
INPUT_FOLDER = "/Game/Drone/Prototype/Input"
BLUEPRINT_FOLDER = "/Game/Drone/Prototype/Blueprints"
MAP_FOLDER = "/Game/Drone/Prototype/Maps"

ASSET_PATHS = {
    "move": f"{ACTION_FOLDER}/IA_DronePrototype_Move",
    "altitude": f"{ACTION_FOLDER}/IA_DronePrototype_Altitude",
    "yaw": f"{ACTION_FOLDER}/IA_DronePrototype_Yaw",
    "look": f"{ACTION_FOLDER}/IA_DronePrototype_Look",
    "imc": f"{INPUT_FOLDER}/IMC_DronePrototype",
    "pawn_bp": f"{BLUEPRINT_FOLDER}/BP_DronePrototypePawn",
    "game_mode_bp": f"{BLUEPRINT_FOLDER}/BP_DronePrototypeGameMode",
    "map": f"{MAP_FOLDER}/Lvl_DronePrototype",
}

EXPECTED_ACTOR_LABELS = {
    "PlayerStart_Prototype",
    "Greybox_Ground",
    "Takeoff_Pad",
    "Grid_X_Negative",
    "Grid_X_Center",
    "Grid_X_Positive",
    "Grid_Y_Negative",
    "Grid_Y_Center",
    "Grid_Y_Positive",
    "Altitude_Marker_500",
    "Altitude_Marker_1000",
    "Collision_Wall",
    "Corridor_Wall_Left",
    "Corridor_Wall_Right",
    "Sight_Blocker",
    "Mission_Target",
    "Return_Area",
    "Patrol_Point_A",
    "Patrol_Point_B",
    "Turret_Pad",
    "DirectionalLight_Prototype",
    "SkyLight_Prototype",
    "SkyAtmosphere_Prototype",
}

EXPECTED_MAPPINGS = {
    ("move", "W"): ("InputModifierSwizzleAxis",),
    ("move", "S"): ("InputModifierNegate", "InputModifierSwizzleAxis"),
    ("move", "A"): ("InputModifierNegate",),
    ("move", "D"): (),
    ("altitude", "SpaceBar"): (),
    ("altitude", "LeftControl"): ("InputModifierNegate",),
    ("yaw", "E"): (),
    ("yaw", "Q"): ("InputModifierNegate",),
    ("look", "Mouse2D"): (),
}


def log(message: str) -> None:
    unreal.log(f"DRONE_SETUP|{message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def asset_name(path: str) -> str:
    return path.rsplit("/", 1)[1]


def asset_folder(path: str) -> str:
    return path.rsplit("/", 1)[0]


def class_name(value: unreal.Object) -> str:
    return value.get_class().get_name()


def key_name(value: unreal.Key) -> str:
    return str(value.get_editor_property("key_name"))


def make_key(name: str) -> unreal.Key:
    value = unreal.Key()
    value.set_editor_property("key_name", unreal.Name(name))
    require(unreal.InputLibrary.key_is_valid(value), f"Invalid Unreal input key: {name}")
    return value


def make_negate_x(outer: unreal.Object) -> unreal.InputModifierNegate:
    modifier = unreal.InputModifierNegate(outer=outer)
    modifier.set_editor_properties({"x": True, "y": False, "z": False})
    return modifier


def make_swizzle_yxz(outer: unreal.Object) -> unreal.InputModifierSwizzleAxis:
    modifier = unreal.InputModifierSwizzleAxis(outer=outer)
    modifier.set_editor_property("order", unreal.InputAxisSwizzle.YXZ)
    return modifier


def create_data_asset(path: str, asset_class: unreal.Class) -> unreal.DataAsset:
    factory = unreal.DataAssetFactory()
    factory.set_editor_property("data_asset_class", asset_class)
    created = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name(path),
        asset_folder(path),
        asset_class,
        factory,
        overwrite_existing=False,
    )
    require(created is not None, f"Could not create data asset: {path}")
    log(f"CREATED_ASSET|{path}")
    return created


def compile_blueprint(blueprint: unreal.Blueprint) -> None:
    unreal.BlueprintEditorLibrary.compile_blueprint(blueprint)
    status = blueprint.get_editor_property("status")
    require(
        status == unreal.BlueprintStatus.BS_UP_TO_DATE,
        f"Blueprint did not compile cleanly: {blueprint.get_path_name()} ({status})",
    )


def create_blueprint(path: str, parent_class: unreal.Class) -> unreal.Blueprint:
    factory = unreal.BlueprintFactory()
    factory.set_editor_property("parent_class", parent_class)
    created = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
        asset_name(path),
        asset_folder(path),
        unreal.Blueprint.static_class(),
        factory,
        overwrite_existing=False,
    )
    require(created is not None, f"Could not create Blueprint: {path}")
    compile_blueprint(created)
    log(f"CREATED_ASSET|{path}")
    return created


def save_asset(editor_assets: unreal.EditorAssetSubsystem, value: unreal.Object) -> None:
    require(
        editor_assets.save_loaded_asset(value, only_if_is_dirty=False),
        f"Could not save asset: {value.get_path_name()}",
    )


def mapping(
    context: unreal.InputMappingContext,
    action: unreal.InputAction,
    key: str,
    modifiers: list[unreal.InputModifier],
) -> unreal.EnhancedActionKeyMapping:
    result = unreal.EnhancedActionKeyMapping()
    result.set_editor_property("action", action)
    result.set_editor_property("key", make_key(key))
    result.set_editor_property("modifiers", modifiers)
    result.set_editor_property("triggers", [])
    return result


def spawn_actor(
    actors: unreal.EditorActorSubsystem,
    actor_class: unreal.Class,
    label: str,
    location: tuple[float, float, float],
    rotation: tuple[float, float, float] = (0.0, 0.0, 0.0),
) -> unreal.Actor:
    actor = actors.spawn_actor_from_class(
        actor_class,
        unreal.Vector(*location),
        unreal.Rotator(pitch=rotation[0], yaw=rotation[1], roll=rotation[2]),
    )
    require(actor is not None, f"Could not spawn map actor: {label}")
    actor.set_actor_label(label)
    return actor


def spawn_mesh(
    actors: unreal.EditorActorSubsystem,
    mesh: unreal.StaticMesh,
    label: str,
    location: tuple[float, float, float],
    scale: tuple[float, float, float],
    collision: bool = True,
) -> unreal.StaticMeshActor:
    actor = spawn_actor(actors, unreal.StaticMeshActor, label, location)
    actor.set_actor_scale3d(unreal.Vector(*scale))
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    require(component is not None, f"StaticMeshComponent missing: {label}")
    require(component.set_static_mesh(mesh), f"Could not assign mesh: {label}")
    if not collision:
        component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    return actor


def create_assets() -> None:
    editor_assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    require(editor_assets is not None, "EditorAssetSubsystem is unavailable")

    existing = [
        path
        for path in ASSET_PATHS.values()
        if editor_assets.does_asset_exist(path) or editor_assets.does_directory_exist(path)
    ]
    require(
        not existing,
        "Refusing to overwrite existing Prototype assets: " + ", ".join(existing),
    )

    pawn_native = unreal.load_class(None, "/Script/Drone.DronePrototypePawn")
    game_mode_native = unreal.load_class(None, "/Script/Drone.DronePrototypeGameMode")
    require(pawn_native is not None, "Native DronePrototypePawn class is unavailable; build C++ first")
    require(game_mode_native is not None, "Native DronePrototypeGameMode class is unavailable; build C++ first")

    actions = {
        "move": create_data_asset(ASSET_PATHS["move"], unreal.InputAction.static_class()),
        "altitude": create_data_asset(ASSET_PATHS["altitude"], unreal.InputAction.static_class()),
        "yaw": create_data_asset(ASSET_PATHS["yaw"], unreal.InputAction.static_class()),
        "look": create_data_asset(ASSET_PATHS["look"], unreal.InputAction.static_class()),
    }
    actions["move"].set_editor_property("value_type", unreal.InputActionValueType.AXIS2D)
    actions["altitude"].set_editor_property("value_type", unreal.InputActionValueType.AXIS1D)
    actions["yaw"].set_editor_property("value_type", unreal.InputActionValueType.AXIS1D)
    actions["look"].set_editor_property("value_type", unreal.InputActionValueType.AXIS2D)

    context = create_data_asset(ASSET_PATHS["imc"], unreal.InputMappingContext.static_class())
    mappings = [
        mapping(context, actions["move"], "W", [make_swizzle_yxz(context)]),
        mapping(context, actions["move"], "S", [make_negate_x(context), make_swizzle_yxz(context)]),
        mapping(context, actions["move"], "A", [make_negate_x(context)]),
        mapping(context, actions["move"], "D", []),
        mapping(context, actions["altitude"], "SpaceBar", []),
        mapping(context, actions["altitude"], "LeftControl", [make_negate_x(context)]),
        mapping(context, actions["yaw"], "E", []),
        mapping(context, actions["yaw"], "Q", [make_negate_x(context)]),
        mapping(context, actions["look"], "Mouse2D", []),
    ]
    mapping_data = unreal.InputMappingContextMappingData()
    mapping_data.set_editor_property("mappings", mappings)
    context.set_editor_property("default_key_mappings", mapping_data)

    for action in actions.values():
        save_asset(editor_assets, action)
    save_asset(editor_assets, context)

    pawn_blueprint = create_blueprint(ASSET_PATHS["pawn_bp"], pawn_native)
    pawn_cdo = unreal.get_default_object(pawn_blueprint.generated_class())
    pawn_cdo.set_editor_properties(
        {
            "prototype_mapping_context": context,
            "move_action": actions["move"],
            "altitude_action": actions["altitude"],
            "yaw_action": actions["yaw"],
            "look_action": actions["look"],
        }
    )
    placeholder_mesh = unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
    require(placeholder_mesh is not None, "Engine Cube placeholder mesh is unavailable")
    visual = pawn_cdo.get_editor_property("visual_mesh_component")
    require(visual is not None, "Prototype Pawn VisualMeshComponent is unavailable")
    require(visual.set_static_mesh(placeholder_mesh), "Could not assign Pawn placeholder mesh")
    visual.set_relative_scale3d(unreal.Vector(1.4, 0.8, 0.25))
    save_asset(editor_assets, pawn_blueprint)

    game_mode_blueprint = create_blueprint(ASSET_PATHS["game_mode_bp"], game_mode_native)
    game_mode_cdo = unreal.get_default_object(game_mode_blueprint.generated_class())
    game_mode_cdo.set_editor_property("default_pawn_class", pawn_blueprint.generated_class())
    require(
        game_mode_cdo.get_editor_property("player_controller_class") == unreal.PlayerController.static_class(),
        "Prototype GameMode must keep the base APlayerController to avoid template IMC duplication",
    )
    save_asset(editor_assets, game_mode_blueprint)

    level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    editor_worlds = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    require(level_editor is not None, "LevelEditorSubsystem is unavailable")
    require(editor_actors is not None, "EditorActorSubsystem is unavailable")
    require(editor_worlds is not None, "UnrealEditorSubsystem is unavailable")
    require(level_editor.new_level(ASSET_PATHS["map"], False), "Could not create non-partitioned Prototype map")
    log(f"CREATED_ASSET|{ASSET_PATHS['map']}")

    world = editor_worlds.get_editor_world()
    require(world is not None, "New Prototype editor world is unavailable")
    world_settings = world.get_world_settings()
    require(world_settings is not None, "Prototype WorldSettings is unavailable")
    world_settings.set_editor_property("default_game_mode", game_mode_blueprint.generated_class())

    cube = unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
    cylinder = unreal.load_asset("/Engine/BasicShapes/Cylinder.Cylinder")
    require(cube is not None and cylinder is not None, "Engine BasicShapes are unavailable")

    spawn_actor(editor_actors, unreal.PlayerStart, "PlayerStart_Prototype", (0.0, 0.0, 150.0))
    spawn_mesh(editor_actors, cube, "Greybox_Ground", (0.0, 0.0, -50.0), (60.0, 40.0, 1.0))
    spawn_mesh(editor_actors, cylinder, "Takeoff_Pad", (0.0, 0.0, 5.0), (2.0, 2.0, 0.1))

    for label, location, scale in (
        ("Grid_X_Negative", (0.0, -1000.0, 2.0), (60.0, 0.05, 0.02)),
        ("Grid_X_Center", (0.0, 0.0, 2.0), (60.0, 0.05, 0.02)),
        ("Grid_X_Positive", (0.0, 1000.0, 2.0), (60.0, 0.05, 0.02)),
        ("Grid_Y_Negative", (-2000.0, 0.0, 2.0), (0.05, 40.0, 0.02)),
        ("Grid_Y_Center", (0.0, 0.0, 2.0), (0.05, 40.0, 0.02)),
        ("Grid_Y_Positive", (2000.0, 0.0, 2.0), (0.05, 40.0, 0.02)),
    ):
        spawn_mesh(editor_actors, cube, label, location, scale, collision=False)

    spawn_mesh(editor_actors, cube, "Altitude_Marker_500", (1200.0, -1200.0, 250.0), (0.3, 0.3, 5.0))
    spawn_mesh(editor_actors, cube, "Altitude_Marker_1000", (1700.0, -1200.0, 500.0), (0.3, 0.3, 10.0))
    spawn_mesh(editor_actors, cube, "Collision_Wall", (2200.0, 0.0, 300.0), (0.5, 8.0, 6.0))
    spawn_mesh(editor_actors, cube, "Corridor_Wall_Left", (900.0, 900.0, 200.0), (8.0, 0.5, 4.0))
    spawn_mesh(editor_actors, cube, "Corridor_Wall_Right", (900.0, 1600.0, 200.0), (8.0, 0.5, 4.0))
    spawn_mesh(editor_actors, cube, "Sight_Blocker", (3200.0, -1200.0, 500.0), (1.0, 10.0, 10.0))
    spawn_mesh(editor_actors, cube, "Mission_Target", (4300.0, 0.0, 100.0), (1.5, 1.5, 1.5))
    spawn_mesh(editor_actors, cylinder, "Return_Area", (-1200.0, 0.0, 5.0), (3.0, 3.0, 0.1))
    spawn_actor(editor_actors, unreal.TargetPoint, "Patrol_Point_A", (2700.0, 900.0, 100.0))
    spawn_actor(editor_actors, unreal.TargetPoint, "Patrol_Point_B", (3800.0, 900.0, 100.0))
    spawn_mesh(editor_actors, cylinder, "Turret_Pad", (3300.0, 1200.0, 10.0), (2.0, 2.0, 0.2))

    spawn_actor(
        editor_actors,
        unreal.DirectionalLight,
        "DirectionalLight_Prototype",
        (0.0, 0.0, 2000.0),
        (-45.0, -30.0, 0.0),
    )
    spawn_actor(editor_actors, unreal.SkyLight, "SkyLight_Prototype", (0.0, 0.0, 1000.0))
    spawn_actor(editor_actors, unreal.SkyAtmosphere, "SkyAtmosphere_Prototype", (0.0, 0.0, 0.0))

    require(level_editor.save_current_level(), "Could not save populated Prototype map")
    log("CREATED_OK")


def validate_modifier(modifier: unreal.InputModifier, expected_class: str) -> None:
    require(class_name(modifier) == expected_class, f"Unexpected modifier class: {class_name(modifier)}")
    if expected_class == "InputModifierNegate":
        require(modifier.get_editor_property("x"), "Negate modifier must invert X")
        require(not modifier.get_editor_property("y"), "Negate modifier must not invert Y")
        require(not modifier.get_editor_property("z"), "Negate modifier must not invert Z")
    elif expected_class == "InputModifierSwizzleAxis":
        require(
            modifier.get_editor_property("order") == unreal.InputAxisSwizzle.YXZ,
            "Swizzle modifier must use YXZ",
        )


def validate_assets() -> None:
    editor_assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    require(editor_assets is not None, "EditorAssetSubsystem is unavailable")
    missing = [path for path in ASSET_PATHS.values() if not editor_assets.does_asset_exist(path)]
    require(not missing, "Missing Prototype assets: " + ", ".join(missing))

    # A UWorld must be opened through LevelEditorSubsystem only. Loading the map
    # here as a generic asset would keep a standalone UWorld reference alive and
    # make LoadLevel fail its world-leak guard in a fresh Editor process.
    loaded = {
        name: editor_assets.load_asset(path)
        for name, path in ASSET_PATHS.items()
        if name != "map"
    }
    require(all(value is not None for value in loaded.values()), "One or more Prototype assets did not load")

    expected_types = {
        "move": unreal.InputActionValueType.AXIS2D,
        "altitude": unreal.InputActionValueType.AXIS1D,
        "yaw": unreal.InputActionValueType.AXIS1D,
        "look": unreal.InputActionValueType.AXIS2D,
    }
    for name, expected_type in expected_types.items():
        action = loaded[name]
        require(action.get_editor_property("value_type") == expected_type, f"Wrong Value Type: {name}")
        require(not action.get_editor_property("modifiers"), f"Action-level modifiers must be empty: {name}")
        require(not action.get_editor_property("triggers"), f"Action-level triggers must be empty: {name}")

    action_lookup = {loaded[name].get_path_name(): name for name in expected_types}
    mapping_data = loaded["imc"].get_editor_property("default_key_mappings")
    mappings = list(mapping_data.get_editor_property("mappings"))
    require(len(mappings) == len(EXPECTED_MAPPINGS), f"Expected 9 IMC mappings, found {len(mappings)}")

    actual_keys = set()
    for item in mappings:
        action = item.get_editor_property("action")
        action_id = action_lookup.get(action.get_path_name()) if action else None
        key = key_name(item.get_editor_property("key"))
        require(action_id is not None, f"Unexpected mapping action for key {key}")
        mapping_id = (action_id, key)
        require(mapping_id in EXPECTED_MAPPINGS, f"Unexpected IMC mapping: {mapping_id}")
        require(mapping_id not in actual_keys, f"Duplicate IMC mapping: {mapping_id}")
        actual_keys.add(mapping_id)
        require(not item.get_editor_property("triggers"), f"Mapping triggers must be empty: {mapping_id}")
        modifiers = list(item.get_editor_property("modifiers"))
        expected_modifier_classes = EXPECTED_MAPPINGS[mapping_id]
        require(
            tuple(class_name(modifier) for modifier in modifiers) == expected_modifier_classes,
            f"Wrong modifier order for {mapping_id}",
        )
        for modifier, expected_class in zip(modifiers, expected_modifier_classes):
            validate_modifier(modifier, expected_class)
    require(actual_keys == set(EXPECTED_MAPPINGS), "IMC mapping set is incomplete")

    pawn_native = unreal.load_class(None, "/Script/Drone.DronePrototypePawn")
    game_mode_native = unreal.load_class(None, "/Script/Drone.DronePrototypeGameMode")
    pawn_blueprint = loaded["pawn_bp"]
    game_mode_blueprint = loaded["game_mode_bp"]
    require(
        unreal.BlueprintEditorLibrary.get_blueprint_parent_class(pawn_blueprint) == pawn_native,
        "Prototype Pawn Blueprint has the wrong parent",
    )
    require(
        unreal.BlueprintEditorLibrary.get_blueprint_parent_class(game_mode_blueprint) == game_mode_native,
        "Prototype GameMode Blueprint has the wrong parent",
    )
    compile_blueprint(pawn_blueprint)
    compile_blueprint(game_mode_blueprint)

    pawn_cdo = unreal.get_default_object(pawn_blueprint.generated_class())
    for property_name, asset_id in (
        ("prototype_mapping_context", "imc"),
        ("move_action", "move"),
        ("altitude_action", "altitude"),
        ("yaw_action", "yaw"),
        ("look_action", "look"),
    ):
        require(
            pawn_cdo.get_editor_property(property_name) == loaded[asset_id],
            f"Pawn CDO reference mismatch: {property_name}",
        )
    visual = pawn_cdo.get_editor_property("visual_mesh_component")
    require(visual is not None, "Pawn VisualMeshComponent is missing")
    require(
        visual.get_editor_property("static_mesh") == unreal.load_asset("/Engine/BasicShapes/Cube.Cube"),
        "Pawn placeholder mesh is not the Engine Cube",
    )

    game_mode_cdo = unreal.get_default_object(game_mode_blueprint.generated_class())
    require(
        game_mode_cdo.get_editor_property("default_pawn_class") == pawn_blueprint.generated_class(),
        "Prototype GameMode does not use the BP Prototype Pawn",
    )
    require(
        game_mode_cdo.get_editor_property("player_controller_class") == unreal.PlayerController.static_class(),
        "Prototype GameMode must not use the ThirdPerson PlayerController",
    )

    level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    editor_actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    editor_worlds = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    require(level_editor.load_level(ASSET_PATHS["map"]), "Could not load Prototype map")
    world = editor_worlds.get_editor_world()
    require(world is not None, "Prototype map world is unavailable")
    require(
        world.get_world_settings().get_editor_property("default_game_mode") == game_mode_blueprint.generated_class(),
        "Prototype map has the wrong GameMode Override",
    )

    level_actors = list(editor_actors.get_all_level_actors())
    labels = {actor.get_actor_label() for actor in level_actors}
    require(EXPECTED_ACTOR_LABELS.issubset(labels), "Prototype map is missing required labelled actors")
    player_starts = [actor for actor in level_actors if isinstance(actor, unreal.PlayerStart)]
    require(len(player_starts) == 1, f"Prototype map must contain exactly one PlayerStart; found {len(player_starts)}")
    placed_pawns = [actor for actor in level_actors if isinstance(actor, unreal.Pawn)]
    require(not placed_pawns, "Prototype map must not contain a manually placed Pawn")
    log("VALIDATION_OK")


def main() -> None:
    validate_only = os.environ.get("DRONE_PROTOTYPE_VALIDATE_ONLY") == "1"
    log("MODE|VALIDATE" if validate_only else "MODE|CREATE")
    if validate_only:
        validate_assets()
    else:
        create_assets()
        validate_assets()


try:
    main()
except Exception as error:
    unreal.log_error(f"DRONE_SETUP|FAILED|{error}")
    unreal.log_error(traceback.format_exc())
    raise
