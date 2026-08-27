"""Create or validate the AI-NPC-01 NPC Blueprints and dedicated Greybox map.

The script owns only the exact Blueprint assets and map listed below. Create mode
refuses to replace an existing map so hand-edited level work is never overwritten.
Set DRONE_NPC_GREYBOX_VALIDATE_ONLY=1 for a read-only fresh-process check.
"""

from __future__ import annotations

import os
import traceback

import unreal


PREFIX = "DRONE_NPC_GREYBOX"
BLUEPRINT_FOLDER = "/Game/Drone/AI/Blueprints"
MAP_PATH = "/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox"
NPC_NATIVE_PATH = "/Script/Drone.DroneNPCCharacter"
SPAWN_NATIVE_PATH = "/Script/Drone.DroneNPCSpawnPoint"
NAVIGATION_FLOOR_NATIVE_PATH = "/Script/Drone.DroneNPCNavigationFloor"
GAME_MODE_PATH = "/Game/Drone/Prototype/Blueprints/BP_DronePrototypeGameMode"
MANNY_MESH_PATH = "/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple"
UNARMED_ANIM_PATH = "/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed"

NPC_SPECS = (
    {
        "name": "Hostile_Rifle",
        "faction": unreal.DroneNPCFaction.HOSTILE,
        "weapon": unreal.DroneNPCWeaponType.RIFLE,
        "can_use_mg": True,
    },
    {
        "name": "Hostile_Shotgun",
        "faction": unreal.DroneNPCFaction.HOSTILE,
        "weapon": unreal.DroneNPCWeaponType.SHOTGUN,
        "can_use_mg": False,
    },
    {
        "name": "Friendly_Base",
        "faction": unreal.DroneNPCFaction.FRIENDLY,
        "weapon": unreal.DroneNPCWeaponType.UNARMED,
        "can_use_mg": False,
    },
)

NPC_PLACEMENTS = (
    ("NPC_Hostile_Rifle_01", "Hostile_Rifle", (900.0, -650.0, 96.0), 180.0),
    ("NPC_Hostile_Shotgun_01", "Hostile_Shotgun", (900.0, 650.0, 96.0), 180.0),
    ("NPC_Friendly_Base_01", "Friendly_Base", (-900.0, -450.0, 96.0), 0.0),
    ("NPC_Friendly_Base_02", "Friendly_Base", (-900.0, 450.0, 96.0), 0.0),
)

STATION_PLACEMENTS = (
    ("Station_EnemyPatrol_A", "EnemyPatrol", (700.0, -1200.0, 0.0), 0.0),
    ("Station_EnemyPatrol_B", "EnemyPatrol", (1450.0, -650.0, 0.0), 90.0),
    ("Station_EnemyPatrol_C", "EnemyPatrol", (1450.0, 650.0, 0.0), 180.0),
    ("Station_Guard_A", "Guard", (2050.0, 0.0, 0.0), 180.0),
    ("Station_MGTurret_A", "MGTurret", (2300.0, 0.0, 0.0), 180.0),
    ("Station_FriendlyPatrol_A", "FriendlyBasePatrol", (-700.0, -1100.0, 0.0), 0.0),
    ("Station_FriendlyPatrol_B", "FriendlyBasePatrol", (-1450.0, -450.0, 0.0), 90.0),
    ("Station_FriendlyPatrol_C", "FriendlyBasePatrol", (-1450.0, 650.0, 0.0), 180.0),
    ("Station_Ambient_A", "Ambient", (-2100.0, -650.0, 0.0), 0.0),
    ("Station_Ambient_B", "Ambient", (-2100.0, 650.0, 0.0), 180.0),
)

SUPPORT_LABELS = {
    "PlayerStart_NPCGreybox",
    "Greybox_Ground",
    "NavigationFloor_NPCGreybox",
    "NavMeshBounds_NPCGreybox",
    "DirectionalLight_NPCGreybox",
    "SkyLight_NPCGreybox",
    "SkyAtmosphere_NPCGreybox",
}


def log(message: str) -> None:
    unreal.log(f"{PREFIX}|{message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def bp_path(name: str) -> str:
    return f"{BLUEPRINT_FOLDER}/BP_NPC_{name}"


def asset_name(path: str) -> str:
    return path.rsplit("/", 1)[1]


def asset_folder(path: str) -> str:
    return path.rsplit("/", 1)[0]


def compile_blueprint(blueprint: unreal.Blueprint) -> None:
    unreal.BlueprintEditorLibrary.compile_blueprint(blueprint)
    require(
        blueprint.get_editor_property("status") == unreal.BlueprintStatus.BS_UP_TO_DATE,
        f"Blueprint did not compile cleanly: {blueprint.get_path_name()}",
    )


def create_or_load_blueprint(
    editor_assets: unreal.EditorAssetSubsystem,
    path: str,
    parent_class: unreal.Class,
) -> unreal.Blueprint:
    if editor_assets.does_asset_exist(path):
        blueprint = editor_assets.load_asset(path)
        require(isinstance(blueprint, unreal.Blueprint), f"Existing asset is not a Blueprint: {path}")
        require(
            unreal.BlueprintEditorLibrary.get_blueprint_parent_class(blueprint) == parent_class,
            f"Existing Blueprint has the wrong parent: {path}",
        )
        log(f"REUSED_BLUEPRINT|{path}")
    else:
        factory = unreal.BlueprintFactory()
        factory.set_editor_property("parent_class", parent_class)
        blueprint = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            asset_name(path),
            asset_folder(path),
            unreal.Blueprint.static_class(),
            factory,
            overwrite_existing=False,
        )
        require(blueprint is not None, f"Could not create Blueprint: {path}")
        log(f"CREATED_BLUEPRINT|{path}")
    compile_blueprint(blueprint)
    return blueprint


def save_asset(editor_assets: unreal.EditorAssetSubsystem, asset: unreal.Object) -> None:
    require(
        editor_assets.save_loaded_asset(asset, only_if_is_dirty=False),
        f"Could not save asset: {asset.get_path_name()}",
    )


def configure_npc_blueprint(
    editor_assets: unreal.EditorAssetSubsystem,
    blueprint: unreal.Blueprint,
    spec: dict[str, object],
    manny_mesh: unreal.SkeletalMesh,
    anim_blueprint: unreal.AnimBlueprint,
) -> None:
    cdo = unreal.get_default_object(blueprint.generated_class())
    require(cdo is not None, f"NPC CDO is unavailable: {blueprint.get_path_name()}")

    profile = unreal.DroneNPCProfile(
        faction=spec["faction"],
        weapon_type=spec["weapon"],
        can_use_mg_turret=spec["can_use_mg"],
    )
    profile_component = cdo.get_npc_profile_component()
    require(profile_component is not None, f"Profile Component missing: {blueprint.get_path_name()}")
    profile_component.set_profile(profile)

    # AI-NPC-01은 세 역할을 같은 Manny Greybox 외형으로 표시한다. 실제 Soldier/Insurgent
    # 채택과 무기 손 위치·Animation 교체는 AI-VIS-01에서 별도로 판정한다.
    mesh = cdo.get_component_by_class(unreal.SkeletalMeshComponent)
    require(mesh is not None, f"Character Mesh Component missing: {blueprint.get_path_name()}")
    mesh.set_skeletal_mesh_asset(manny_mesh)
    mesh.set_relative_location(unreal.Vector(0.0, 0.0, -90.0), False, False)
    mesh.set_relative_rotation(unreal.Rotator(pitch=0.0, yaw=-90.0, roll=0.0), False, False)
    mesh.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    mesh.set_editor_property("generate_overlap_events", False)
    mesh.set_animation_mode(unreal.AnimationMode.ANIMATION_BLUEPRINT)
    mesh.set_anim_instance_class(anim_blueprint.generated_class())

    save_asset(editor_assets, blueprint)
    compile_blueprint(blueprint)


def validate_npc_blueprint(
    blueprint: unreal.Blueprint,
    spec: dict[str, object],
    npc_native: unreal.Class,
    manny_mesh: unreal.SkeletalMesh,
    anim_blueprint: unreal.AnimBlueprint,
) -> None:
    require(
        unreal.BlueprintEditorLibrary.get_blueprint_parent_class(blueprint) == npc_native,
        f"NPC Blueprint parent mismatch: {blueprint.get_path_name()}",
    )
    compile_blueprint(blueprint)
    cdo = unreal.get_default_object(blueprint.generated_class())
    profile_component = cdo.get_npc_profile_component()
    profile = profile_component.get_profile()
    require(profile.faction == spec["faction"], f"NPC Faction mismatch: {blueprint.get_path_name()}")
    require(profile.weapon_type == spec["weapon"], f"NPC Weapon mismatch: {blueprint.get_path_name()}")
    require(
        profile.can_use_mg_turret == spec["can_use_mg"],
        f"NPC MG permission mismatch: {blueprint.get_path_name()}",
    )
    mesh = cdo.get_component_by_class(unreal.SkeletalMeshComponent)
    require(mesh is not None, f"Character Mesh Component missing: {blueprint.get_path_name()}")
    require(mesh.get_skeletal_mesh_asset() == manny_mesh, f"NPC Greybox Mesh mismatch: {blueprint.get_path_name()}")
    require(
        mesh.get_editor_property("anim_class") == anim_blueprint.generated_class(),
        f"NPC Anim Blueprint mismatch: {blueprint.get_path_name()}",
    )


def spawn_actor(
    actors: unreal.EditorActorSubsystem,
    actor_class: unreal.Class,
    label: str,
    location: tuple[float, float, float],
    yaw: float = 0.0,
) -> unreal.Actor:
    actor = actors.spawn_actor_from_class(
        actor_class,
        unreal.Vector(*location),
        unreal.Rotator(pitch=0.0, yaw=yaw, roll=0.0),
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
) -> unreal.StaticMeshActor:
    actor = spawn_actor(actors, unreal.StaticMeshActor, label, location)
    actor.set_actor_scale3d(unreal.Vector(*scale))
    component = actor.get_component_by_class(unreal.StaticMeshComponent)
    require(component is not None and component.set_static_mesh(mesh), f"Could not assign Mesh: {label}")
    return actor


def create_map(
    editor_assets: unreal.EditorAssetSubsystem,
    npc_blueprints: dict[str, unreal.Blueprint],
) -> None:
    require(not editor_assets.does_asset_exist(MAP_PATH), f"Refusing to overwrite existing map: {MAP_PATH}")

    level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    worlds = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    require(level_editor is not None and actors is not None and worlds is not None, "Editor subsystems unavailable")
    require(level_editor.new_level(MAP_PATH, False), f"Could not create map: {MAP_PATH}")

    world = worlds.get_editor_world()
    require(world is not None, "New NPC Greybox World is unavailable")
    game_mode = editor_assets.load_asset(GAME_MODE_PATH)
    require(isinstance(game_mode, unreal.Blueprint), f"GameMode Blueprint unavailable: {GAME_MODE_PATH}")
    world.get_world_settings().set_editor_property("default_game_mode", game_mode.generated_class())

    cube = unreal.load_asset("/Engine/BasicShapes/Cube.Cube")
    require(isinstance(cube, unreal.StaticMesh), "Engine Cube is unavailable")
    spawn_actor(actors, unreal.PlayerStart, "PlayerStart_NPCGreybox", (-2600.0, 0.0, 180.0), 0.0)
    # Engine Cube는 기본 100 cm 크기이므로 X/Y 배율 64/52가 각각
    # -3200~3200, -2600~2600을 덮는다. 시각 메시와 내비게이션용
    # Blocking Volume을 분리해 명령행 PIE에서도 충돌 수집이 일관되게 한다.
    ground = spawn_mesh(actors, cube, "Greybox_Ground", (0.0, 0.0, -50.0), (64.0, 52.0, 1.0))
    ground_component = ground.get_component_by_class(unreal.StaticMeshComponent)
    require(ground_component is not None, "Greybox Ground Component is unavailable")
    ground_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)
    navigation_floor_class = unreal.load_class(None, NAVIGATION_FLOOR_NATIVE_PATH)
    require(navigation_floor_class is not None, "Native Navigation Floor class is unavailable")
    spawn_actor(
        actors,
        navigation_floor_class,
        "NavigationFloor_NPCGreybox",
        (0.0, 0.0, -50.0),
    )

    nav_bounds = spawn_actor(
        actors,
        unreal.NavMeshBoundsVolume,
        "NavMeshBounds_NPCGreybox",
        (0.0, 0.0, 500.0),
    )
    nav_bounds.set_actor_scale3d(unreal.Vector(32.0, 26.0, 10.0))

    for label, spec_name, location, yaw in NPC_PLACEMENTS:
        spawn_actor(actors, npc_blueprints[spec_name].generated_class(), label, location, yaw)

    for label, station_name, location, yaw in STATION_PLACEMENTS:
        station_bp = editor_assets.load_asset(
            f"/Game/Drone/AI/SmartObjects/Blueprints/BP_SO_{station_name}"
        )
        require(isinstance(station_bp, unreal.Blueprint), f"Station Blueprint unavailable: {station_name}")
        spawn_actor(actors, station_bp.generated_class(), label, location, yaw)

    spawn_actor(
        actors,
        unreal.DirectionalLight,
        "DirectionalLight_NPCGreybox",
        (0.0, 0.0, 1800.0),
        -30.0,
    ).set_actor_rotation(unreal.Rotator(pitch=-50.0, yaw=-30.0, roll=0.0), False)
    spawn_actor(actors, unreal.SkyLight, "SkyLight_NPCGreybox", (0.0, 0.0, 1000.0))
    spawn_actor(actors, unreal.SkyAtmosphere, "SkyAtmosphere_NPCGreybox", (0.0, 0.0, 0.0))

    require(level_editor.save_current_level(), f"Could not save populated map: {MAP_PATH}")
    log(f"CREATED_MAP|{MAP_PATH}")


def validate_map(
    editor_assets: unreal.EditorAssetSubsystem,
    npc_blueprints: dict[str, unreal.Blueprint],
) -> None:
    level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    worlds = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    require(level_editor is not None and actors is not None and worlds is not None, "Editor subsystems unavailable")
    require(editor_assets.does_asset_exist(MAP_PATH), f"Missing NPC Greybox map: {MAP_PATH}")
    require(level_editor.load_level(MAP_PATH), f"Could not open NPC Greybox map: {MAP_PATH}")

    world = worlds.get_editor_world()
    require(world is not None, "NPC Greybox World is unavailable")
    game_mode = editor_assets.load_asset(GAME_MODE_PATH)
    require(
        world.get_world_settings().get_editor_property("default_game_mode") == game_mode.generated_class(),
        "NPC Greybox map GameMode mismatch",
    )

    level_actors = list(actors.get_all_level_actors())
    by_label = {actor.get_actor_label(): actor for actor in level_actors}
    expected_labels = SUPPORT_LABELS | {value[0] for value in NPC_PLACEMENTS} | {
        value[0] for value in STATION_PLACEMENTS
    }
    missing = sorted(expected_labels - set(by_label))
    require(not missing, "NPC Greybox map is missing actors: " + ", ".join(missing))

    for label, spec_name, _location, _yaw in NPC_PLACEMENTS:
        require(
            by_label[label].get_class() == npc_blueprints[spec_name].generated_class(),
            f"Placed NPC class mismatch: {label}",
        )
    require(
        len([actor for actor in level_actors if isinstance(actor, unreal.NavMeshBoundsVolume)]) == 1,
        "NPC Greybox map must contain exactly one NavMeshBoundsVolume",
    )
    require(
        len([actor for actor in level_actors if isinstance(actor, unreal.PlayerStart)]) == 1,
        "NPC Greybox map must contain exactly one PlayerStart",
    )
    log(f"VALIDATED_MAP|{MAP_PATH}")


def build_navigation() -> None:
    level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    worlds = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem)
    require(level_editor is not None and actors is not None and worlds is not None, "Editor subsystems unavailable")
    require(level_editor.load_level(MAP_PATH), f"Could not open NPC Greybox map: {MAP_PATH}")
    world = worlds.get_editor_world()
    require(world is not None, "NPC Greybox World is unavailable")

    by_label = {actor.get_actor_label(): actor for actor in actors.get_all_level_actors()}
    ground = by_label.get("Greybox_Ground")
    require(isinstance(ground, unreal.StaticMeshActor), "NPC Greybox visual Ground is unavailable")
    ground.set_actor_scale3d(unreal.Vector(64.0, 52.0, 1.0))
    ground_component = ground.get_component_by_class(unreal.StaticMeshComponent)
    require(ground_component is not None, "NPC Greybox visual Ground Component is unavailable")
    ground_component.set_collision_enabled(unreal.CollisionEnabled.NO_COLLISION)

    navigation_floor_class = unreal.load_class(None, NAVIGATION_FLOOR_NATIVE_PATH)
    require(navigation_floor_class is not None, "Native Navigation Floor class is unavailable")
    navigation_floor = by_label.get("NavigationFloor_NPCGreybox")
    if navigation_floor is not None and navigation_floor.get_class() != navigation_floor_class:
        require(actors.destroy_actor(navigation_floor), "Could not replace temporary Navigation Floor")
        navigation_floor = None
        log("REPLACED_NAVIGATION_FLOOR|NavigationFloor_NPCGreybox")
    if navigation_floor is None:
        navigation_floor = spawn_actor(
            actors,
            navigation_floor_class,
            "NavigationFloor_NPCGreybox",
            (0.0, 0.0, -50.0),
        )
        log("CREATED_NAVIGATION_FLOOR|NavigationFloor_NPCGreybox")
    require(navigation_floor.get_class() == navigation_floor_class, "Navigation Floor has the wrong class")
    navigation_floor.set_actor_location(unreal.Vector(0.0, 0.0, -50.0), False, False)

    # UnrealEd의 BUILDPATHS 명령은 Build 메뉴의 Build Paths와 같은 경로를 사용한다.
    # 단, 명령행 에디터에서는 빌드가 비동기로 종료될 수 있으므로
    # 해당 Recast 액터를 Dynamic + 로드 시 재빌드로 저장한다. 실제 타일과
    # NPC 시작점 투영은 C++ PIE 자동화 테스트가 실행 세션에서 확인한다.
    unreal.SystemLibrary.execute_console_command(world, "BUILDPATHS")
    recast_actors = [
        actor
        for actor in actors.get_all_level_actors()
        if actor.get_class().get_path_name() == "/Script/NavigationSystem.RecastNavMesh"
    ]
    recast_count = len(recast_actors)
    require(recast_count > 0, "Build Paths did not create a RecastNavMesh actor")
    for recast in recast_actors:
        recast.set_editor_property("runtime_generation", unreal.RuntimeGenerationType.DYNAMIC)
        recast.set_editor_property("force_rebuild_on_load", True)
    require(level_editor.save_current_level(), f"Could not save navigation data: {MAP_PATH}")
    log(f"BUILT_NAVIGATION|{MAP_PATH}|RECAST={recast_count}|RUNTIME=Dynamic")


def main() -> None:
    editor_assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    require(editor_assets is not None, "EditorAssetSubsystem unavailable")
    npc_native = unreal.load_class(None, NPC_NATIVE_PATH)
    spawn_native = unreal.load_class(None, SPAWN_NATIVE_PATH)
    require(npc_native is not None and spawn_native is not None, "Drone NPC native classes unavailable; build first")

    manny_mesh = unreal.load_asset(MANNY_MESH_PATH)
    anim_blueprint = unreal.load_asset(UNARMED_ANIM_PATH)
    require(isinstance(manny_mesh, unreal.SkeletalMesh), f"Manny Greybox Mesh unavailable: {MANNY_MESH_PATH}")
    require(isinstance(anim_blueprint, unreal.AnimBlueprint), f"Unarmed Anim Blueprint unavailable: {UNARMED_ANIM_PATH}")

    validate_only = os.environ.get("DRONE_NPC_GREYBOX_VALIDATE_ONLY") == "1"
    build_navigation_only = os.environ.get("DRONE_NPC_GREYBOX_BUILD_NAVIGATION") == "1"
    npc_blueprints: dict[str, unreal.Blueprint] = {}
    for spec in NPC_SPECS:
        path = bp_path(str(spec["name"]))
        if validate_only or build_navigation_only:
            blueprint = editor_assets.load_asset(path)
            require(isinstance(blueprint, unreal.Blueprint), f"Missing NPC Blueprint: {path}")
        else:
            blueprint = create_or_load_blueprint(editor_assets, path, npc_native)
            configure_npc_blueprint(editor_assets, blueprint, spec, manny_mesh, anim_blueprint)
        validate_npc_blueprint(blueprint, spec, npc_native, manny_mesh, anim_blueprint)
        npc_blueprints[str(spec["name"])] = blueprint
        log(f"VALIDATED_NPC|{path}")

    spawn_path = f"{BLUEPRINT_FOLDER}/BP_NPCSpawnPoint"
    if validate_only or build_navigation_only:
        spawn_blueprint = editor_assets.load_asset(spawn_path)
        require(isinstance(spawn_blueprint, unreal.Blueprint), f"Missing Spawn Point Blueprint: {spawn_path}")
    else:
        spawn_blueprint = create_or_load_blueprint(editor_assets, spawn_path, spawn_native)
        save_asset(editor_assets, spawn_blueprint)
    require(
        unreal.BlueprintEditorLibrary.get_blueprint_parent_class(spawn_blueprint) == spawn_native,
        "Spawn Point Blueprint parent mismatch",
    )
    compile_blueprint(spawn_blueprint)

    if not validate_only and not build_navigation_only:
        create_map(editor_assets, npc_blueprints)
    if build_navigation_only:
        build_navigation()
    validate_map(editor_assets, npc_blueprints)

    log("VALIDATION_OK")
    if not validate_only and not build_navigation_only:
        log("CREATED_OK")
    if build_navigation_only:
        log("NAVIGATION_OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        unreal.log_error(f"{PREFIX}|FAILED|{exc}")
        unreal.log_error(traceback.format_exc())
        raise
