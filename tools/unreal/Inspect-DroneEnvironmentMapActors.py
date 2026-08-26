"""Inspect named environment-map actors before deciding whether to remove them."""

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

label_prefixes = tuple(
    prefix.strip()
    for prefix in os.environ.get("DRONE_ENV_ACTOR_PREFIXES", "").split(",")
    if prefix.strip()
)
if not label_prefixes:
    raise RuntimeError("DRONE_ENV_ACTOR_PREFIXES must contain at least one label prefix")

map_path = ENVIRONMENT_MAPS[selected_name]
world = unreal.EditorLoadingAndSavingUtils.load_map(map_path)
if world is None:
    raise RuntimeError(f"Failed to load environment map: {map_path}")

actor_subsystem = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
records = []
for actor in actor_subsystem.get_all_level_actors():
    label = actor.get_actor_label()
    if not label.startswith(label_prefixes):
        continue
    components = []
    for component in actor.get_components_by_class(unreal.ActorComponent):
        component_record = {
            "name": component.get_name(),
            "class": component.get_class().get_path_name(),
        }
        if isinstance(component, unreal.StaticMeshComponent):
            mesh = component.get_editor_property("static_mesh")
            component_record["static_mesh"] = (
                mesh.get_path_name() if mesh is not None else None
            )
        components.append(component_record)
    records.append(
        {
            "label": label,
            "name": actor.get_name(),
            "class": actor.get_class().get_path_name(),
            "components": components,
        }
    )

unreal.log("DRONE_ENVIRONMENT_ACTOR_INSPECTION_JSON_BEGIN")
unreal.log(json.dumps(records, ensure_ascii=False, indent=2))
unreal.log("DRONE_ENVIRONMENT_ACTOR_INSPECTION_JSON_END")
