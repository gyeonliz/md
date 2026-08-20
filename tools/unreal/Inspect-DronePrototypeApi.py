"""Read-only UE 5.8 Python API probe for the Drone prototype setup script."""

import unreal


def show(name, value):
    unreal.log(f"DRONE_API|{name}|{value}")


def public_names(value, contains=None):
    names = [name for name in dir(value) if not name.startswith("_")]
    if contains:
        names = [name for name in names if contains.lower() in name.lower()]
    return ",".join(sorted(names))


show("engine_version", unreal.SystemLibrary.get_engine_version())

for class_name in (
    "InputAction",
    "InputMappingContext",
    "InputActionFactory",
    "InputMappingContextFactory",
    "DataAssetFactory",
    "InputModifierNegate",
    "InputModifierSwizzleAxis",
    "BlueprintFactory",
    "BlueprintEditorLibrary",
    "LevelEditorSubsystem",
    "EditorActorSubsystem",
    "UnrealEditorSubsystem",
):
    show(f"class.{class_name}", hasattr(unreal, class_name))

show("enum.InputActionValueType", public_names(unreal.InputActionValueType))
show("enum.InputAxisSwizzle", public_names(unreal.InputAxisSwizzle))
show("InputMappingContext.map_key.doc", unreal.InputMappingContext.map_key.__doc__)
show("LevelEditorSubsystem.new_level.doc", unreal.LevelEditorSubsystem.new_level.__doc__)
show("LevelEditorSubsystem.save_current_level.doc", unreal.LevelEditorSubsystem.save_current_level.__doc__)

pawn_class = unreal.load_class(None, "/Script/Drone.DronePrototypePawn")
game_mode_class = unreal.load_class(None, "/Script/Drone.DronePrototypeGameMode")
show("class.DronePrototypePawn", pawn_class)
show("class.DronePrototypeGameMode", game_mode_class)

pawn_cdo = unreal.get_default_object(pawn_class)
game_mode_cdo = unreal.get_default_object(game_mode_class)
for property_name in (
    "prototype_mapping_context",
    "move_action",
    "altitude_action",
    "yaw_action",
    "look_action",
    "visual_mesh_component",
):
    show(f"DronePrototypePawn.{property_name}", pawn_cdo.get_editor_property(property_name))
show("DronePrototypeGameMode.default_pawn_class", game_mode_cdo.get_editor_property("default_pawn_class"))

visual_mesh_component = pawn_cdo.get_editor_property("visual_mesh_component")
show("VisualMeshComponent.names", public_names(visual_mesh_component, "mesh"))
show("Engine.BasicShapes.Cylinder", unreal.load_asset("/Engine/BasicShapes/Cylinder.Cylinder"))
show("Engine.BasicShapes.Cube", unreal.load_asset("/Engine/BasicShapes/Cube.Cube"))

temporary_action = unreal.InputAction()
temporary_action.set_editor_property("value_type", unreal.InputActionValueType.AXIS2D)
show("InputAction.value_type", temporary_action.get_editor_property("value_type"))

temporary_key = unreal.Key()
temporary_key.set_editor_property("key_name", "W")
show("Key.W", temporary_key)

temporary_context = unreal.InputMappingContext()
temporary_mapping = temporary_context.map_key(temporary_action, temporary_key)
show("EnhancedActionKeyMapping.type", type(temporary_mapping))
show("EnhancedActionKeyMapping.names", public_names(temporary_mapping))
show("EnhancedActionKeyMapping.modifiers", temporary_mapping.get_editor_property("modifiers"))
show("InputMappingContext.names.mapping", public_names(temporary_context, "mapping"))

negate = unreal.InputModifierNegate(outer=temporary_context)
swizzle = unreal.InputModifierSwizzleAxis(outer=temporary_context)
show("InputModifierNegate.names", public_names(negate))
show("InputModifierSwizzleAxis.order", swizzle.get_editor_property("order"))

temporary_mapping.set_editor_property("modifiers", [negate, swizzle])
show("EnhancedActionKeyMapping.modifiers.after", temporary_mapping.get_editor_property("modifiers"))
show("InputMappingContext.default_key_mappings", temporary_context.get_editor_property("default_key_mappings"))

world = unreal.get_editor_subsystem(unreal.UnrealEditorSubsystem).get_editor_world()
show("editor_world", world)
world_settings = world.get_world_settings() if world else None
show("world_settings", world_settings)
show("world_settings.default_game_mode", world_settings.get_editor_property("default_game_mode") if world_settings else None)
