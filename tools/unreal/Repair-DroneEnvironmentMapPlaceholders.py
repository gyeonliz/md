"""Remove empty StaticMeshActor placeholders from one migrated environment map.

Set DRONE_ENV_MAP_TARGET to Battlefield, MilitaryCamp, or MilitaryBase before
running this script through UnrealEditor-Cmd. Only the project-owned map copy
under /Game/Drone/Maps is edited; vendor assets remain untouched.
"""

import json
import os

import unreal


ENVIRONMENT_MAPS = {
    "Battlefield": "/Game/Drone/Maps/Lvl_Battlefield",
    "MilitaryCamp": "/Game/Drone/Maps/Lvl_MilitaryCamp",
    "MilitaryBase": "/Game/Drone/Maps/Lvl_MilitaryBase",
}


selected_name = os.environ.get("DRONE_ENV_MAP_TARGET")
if selected_name not in ENVIRONMENT_MAPS:
    raise RuntimeError(
        "DRONE_ENV_MAP_TARGET must be Battlefield, MilitaryCamp, or MilitaryBase"
    )

map_path = ENVIRONMENT_MAPS[selected_name]
world = unreal.EditorLoadingAndSavingUtils.load_map(map_path)
if world is None:
    raise RuntimeError(f"Failed to load environment map: {map_path}")

actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
if actor_subsystem is None:
    raise RuntimeError("EditorActorSubsystem is unavailable")

empty_static_mesh_actors = []
for actor in actor_subsystem.get_all_level_actors():
    components = actor.get_components_by_class(unreal.StaticMeshComponent)
    if components and all(
        component.get_editor_property("static_mesh") is None
        for component in components
    ):
        empty_static_mesh_actors.append(actor)

removed_actor_labels = sorted(
    actor.get_actor_label() for actor in empty_static_mesh_actors
)
if empty_static_mesh_actors and not actor_subsystem.destroy_actors(
    empty_static_mesh_actors
):
    raise RuntimeError(f"Failed to remove empty StaticMeshActor objects: {map_path}")

# Environment maps inherit the Drone project's configured GameMode.
world.get_world_settings().set_editor_property("default_game_mode", None)
if not unreal.EditorAssetLibrary.save_asset(map_path, only_if_is_dirty=False):
    raise RuntimeError(f"Failed to save repaired environment map: {map_path}")

result = {
    "environment": selected_name,
    "map": map_path,
    "removed_empty_static_mesh_actor_count": len(removed_actor_labels),
    "removed_actor_labels": removed_actor_labels,
    "default_game_mode": "None",
}
unreal.log("DRONE_ENVIRONMENT_MAP_REPAIR_JSON_BEGIN")
unreal.log(json.dumps(result, ensure_ascii=False, indent=2))
unreal.log("DRONE_ENVIRONMENT_MAP_REPAIR_JSON_END")
