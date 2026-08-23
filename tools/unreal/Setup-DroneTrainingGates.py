"""Create and validate the TUT-02 Blueprint Gate and Training Map placement.

Run only in UnrealEditor-Cmd with PythonScriptPlugin enabled. The script is
idempotent for the four explicitly labelled TUT-02 Greybox Gates.
"""

from __future__ import annotations

import sys

import unreal


PREFIX = "DRONE_TUT02_SETUP"
MAP_PATH = "/Game/Drone/Tutorial/Maps/Lvl_DroneTraining"
GATE_BP_PATH = "/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingGate"
COURSE_ID = unreal.Name("DroneTrainingCourse")
GATE_FRACTIONS = (0.10, 0.35, 0.60, 0.85)
EXPECTED_LABELS = tuple(f"TUT_Gate_{index:02d}" for index in range(len(GATE_FRACTIONS)))


def log(message: str) -> None:
    unreal.log(f"{PREFIX}|{message}")


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def asset_name(path: str) -> str:
    return path.rsplit("/", 1)[-1]


def asset_folder(path: str) -> str:
    return path.rsplit("/", 1)[0]


def create_or_load_gate_blueprint(
    editor_assets: unreal.EditorAssetSubsystem,
    gate_native: unreal.Class,
) -> unreal.Blueprint:
    if editor_assets.does_asset_exist(GATE_BP_PATH):
        blueprint = editor_assets.load_asset(GATE_BP_PATH)
        require(isinstance(blueprint, unreal.Blueprint), "Existing Gate asset is not a Blueprint")
        log(f"REUSED_ASSET|{GATE_BP_PATH}")
    else:
        factory = unreal.BlueprintFactory()
        factory.set_editor_property("parent_class", gate_native)
        blueprint = unreal.AssetToolsHelpers.get_asset_tools().create_asset(
            asset_name(GATE_BP_PATH),
            asset_folder(GATE_BP_PATH),
            unreal.Blueprint.static_class(),
            factory,
            overwrite_existing=False,
        )
        require(blueprint is not None, f"Could not create {GATE_BP_PATH}")
        log(f"CREATED_ASSET|{GATE_BP_PATH}")

    require(
        unreal.BlueprintEditorLibrary.get_blueprint_parent_class(blueprint) == gate_native,
        "BP_DroneTrainingGate has the wrong native parent",
    )
    unreal.BlueprintEditorLibrary.compile_blueprint(blueprint)
    require(
        blueprint.get_editor_property("status") == unreal.BlueprintStatus.BS_UP_TO_DATE,
        "BP_DroneTrainingGate did not compile cleanly",
    )
    require(
        editor_assets.save_loaded_asset(blueprint, only_if_is_dirty=False),
        "Could not save BP_DroneTrainingGate",
    )
    return blueprint


def actor_is_a(actor: unreal.Actor, native_class: unreal.Class) -> bool:
    return bool(
        actor
        and native_class
        and unreal.MathLibrary.class_is_child_of(actor.get_class(), native_class)
    )


def find_single_course(
    actors: unreal.EditorActorSubsystem,
    course_native: unreal.Class,
) -> unreal.Actor:
    courses = [actor for actor in actors.get_all_level_actors() if actor_is_a(actor, course_native)]
    require(len(courses) == 1, f"Training Map must contain exactly one Course; found {len(courses)}")
    return courses[0]


def find_or_spawn_gate(
    actors: unreal.EditorActorSubsystem,
    gate_class: unreal.Class,
    gate_native: unreal.Class,
    label: str,
) -> unreal.Actor:
    matches = [
        actor
        for actor in actors.get_all_level_actors()
        if actor.get_actor_label() == label and actor_is_a(actor, gate_native)
    ]
    require(len(matches) <= 1, f"Duplicate labelled Gate actors: {label}")
    if matches:
        return matches[0]

    gate = actors.spawn_actor_from_class(gate_class, unreal.Vector(), unreal.Rotator())
    require(gate is not None, f"Could not spawn {label}")
    gate.set_actor_label(label)
    log(f"SPAWNED_ACTOR|{label}")
    return gate


def configure_training_map(
    editor_assets: unreal.EditorAssetSubsystem,
    gate_blueprint: unreal.Blueprint,
    course_native: unreal.Class,
    gate_native: unreal.Class,
) -> None:
    level_editor = unreal.get_editor_subsystem(unreal.LevelEditorSubsystem)
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    require(level_editor is not None, "LevelEditorSubsystem is unavailable")
    require(actors is not None, "EditorActorSubsystem is unavailable")
    require(level_editor.load_level(MAP_PATH), f"Could not load {MAP_PATH}")

    course = find_single_course(actors, course_native)
    spline = course.get_component_by_class(unreal.SplineComponent)
    require(spline is not None, "Training Course has no SplineComponent")
    spline_length = float(spline.get_spline_length())
    require(spline_length > 0.0, "Training Course Spline has no length")

    gate_class = gate_blueprint.generated_class()
    require(gate_class is not None, "BP_DroneTrainingGate generated Class is unavailable")

    configured_gates: list[unreal.Actor] = []
    for gate_index, fraction in enumerate(GATE_FRACTIONS):
        distance = spline_length * fraction
        location = spline.get_location_at_distance_along_spline(
            distance,
            unreal.SplineCoordinateSpace.WORLD,
        )
        rotation = spline.get_rotation_at_distance_along_spline(
            distance,
            unreal.SplineCoordinateSpace.WORLD,
        )
        gate = find_or_spawn_gate(
            actors,
            gate_class,
            gate_native,
            EXPECTED_LABELS[gate_index],
        )
        gate.set_actor_location(location, False, False)
        gate.set_actor_rotation(rotation, False)
        gate.set_editor_property("course_id", COURSE_ID)
        gate.set_editor_property("gate_index", gate_index)
        gate.set_editor_property("segment_distance", distance)
        configured_gates.append(gate)

    # 이 명시적 배열의 위치가 Gate 순서의 단일 기준이다.
    course.set_editor_property("course_id", COURSE_ID)
    course.set_editor_property("ordered_gates", configured_gates)

    # 이전 실패 실행에서 남은 TUT_Gate_* Actor만 정확한 대상에 한해 정리한다.
    extra_gates = [
        actor
        for actor in actors.get_all_level_actors()
        if actor_is_a(actor, gate_native)
        and actor.get_actor_label().startswith("TUT_Gate_")
        and actor.get_actor_label() not in EXPECTED_LABELS
    ]
    if extra_gates:
        extra_labels = [gate.get_actor_label() for gate in extra_gates]
        actors.destroy_actors(extra_gates)
        for label in extra_labels:
            log(f"REMOVED_EXTRA_ACTOR|{label}")

    require(level_editor.save_current_level(), "Could not save the populated Training Map")
    log(f"SAVED_MAP|{MAP_PATH}")


def validate_training_map(
    gate_blueprint: unreal.Blueprint,
    course_native: unreal.Class,
    gate_native: unreal.Class,
) -> None:
    actors = unreal.get_editor_subsystem(unreal.EditorActorSubsystem)
    require(actors is not None, "EditorActorSubsystem is unavailable")
    course = find_single_course(actors, course_native)
    placed_gates = [actor for actor in actors.get_all_level_actors() if actor_is_a(actor, gate_native)]
    require(len(placed_gates) == len(EXPECTED_LABELS), f"Expected four Gate actors; found {len(placed_gates)}")

    ordered_gates = list(course.get_editor_property("ordered_gates"))
    require(len(ordered_gates) == len(EXPECTED_LABELS), "Course OrderedGates must contain four actors")
    require(
        len({gate.get_path_name() for gate in ordered_gates}) == len(ordered_gates),
        "Course OrderedGates contains duplicates",
    )

    for gate_index, gate in enumerate(ordered_gates):
        require(gate in placed_gates, f"Ordered Gate {gate_index} is not placed in the Training Map")
        require(gate.get_class() == gate_blueprint.generated_class(), f"Gate {gate_index} does not use BP_DroneTrainingGate")
        require(gate.get_editor_property("course_id") == COURSE_ID, f"Gate {gate_index} CourseId mismatch")
        require(gate.get_editor_property("gate_index") == gate_index, f"Gate {gate_index} index mismatch")
        distance = float(gate.get_editor_property("segment_distance"))
        require(distance >= 0.0, f"Gate {gate_index} SegmentDistance must be non-negative")

    require(course.get_editor_property("course_id") == COURSE_ID, "CourseId mismatch")
    require({gate.get_actor_label() for gate in placed_gates} == set(EXPECTED_LABELS), "Gate labels mismatch")
    log("VALIDATION_OK")


def main() -> None:
    editor_assets = unreal.get_editor_subsystem(unreal.EditorAssetSubsystem)
    require(editor_assets is not None, "EditorAssetSubsystem is unavailable")
    gate_native = unreal.load_class(None, "/Script/Drone.DroneTrainingGate")
    course_native = unreal.load_class(None, "/Script/Drone.DroneTrainingCourse")
    require(gate_native is not None, "Native DroneTrainingGate Class is unavailable")
    require(course_native is not None, "Native DroneTrainingCourse Class is unavailable")

    gate_blueprint = create_or_load_gate_blueprint(editor_assets, gate_native)
    configure_training_map(editor_assets, gate_blueprint, course_native, gate_native)
    validate_training_map(gate_blueprint, course_native, gate_native)
    log("CREATED_OK")


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:  # Unreal's commandlet must surface a non-zero script result.
        unreal.log_error(f"{PREFIX}|FAILED|{exc}")
        raise
