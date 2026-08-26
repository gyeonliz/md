"""Load one migrated environment map and run Unreal's Map Check.

Set DRONE_ENV_MAP_TARGET to Battlefield, MilitaryCamp, or MilitaryBase. The
commandlet log is the source of truth for the MapCheck error/warning totals.
"""

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

unreal.SystemLibrary.execute_console_command(world, "MAP CHECK")
unreal.log(f"DRONE_ENVIRONMENT_MAP_CHECK_EXECUTED={map_path}")
