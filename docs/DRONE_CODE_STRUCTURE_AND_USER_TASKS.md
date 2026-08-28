# Drone 현재 코드 구조와 사용자 확인 작업

기준일: 2026-08-28 (Asia/Seoul)

이 문서는 현재 Unreal `drone` 저장소를 직접 확인한 결과를 정리한다. 모든 소스 경로는 이 저장소 루트를 기준으로 적는다.

TUT-03 완료 기능 Commit은 `551e287`이다. 공유 main은 AI-FRIEND-01 Merge `2fcfb04`이며, NPC Smart Object 기반, Definition·Station BP 6쌍, 역할별 NPC BP, 전용 Greybox 맵과 Hostile/Friendly 기본 이동 StateTree까지 구성돼 있다. 팀원 환경 맵·재질 변경과 정리 Merge `888414f`도 보존한다. 환경 Map은 후보 공간이며 Tutorial 기본 실행 구조를 바꾸지 않는다.

NavigationArrows 최소 이식 Commit `5a052c8`은 `fb1d7ad`로 main에 병합됐다. 자산은 main에 있지만 프로젝트 소유 Widget Host는 아직 구현하지 않았으므로 화면에 나타나지 않는 것이 정상이다.

## 현재 검증 기준선

| 검증 항목 | 현재 확인 결과 |
|---|---|
| `DroneEditor Win64 Development` | Build 성공 |
| `Drone.Tutorial` Automation | 7/7 통과 |
| `Drone.AI` Automation | 7/7 통과, 경고·오류 0 |
| 전체 `Drone.` Automation | 23/23 통과. 22개 무경고 성공, 기존 PIE RecastNavMesh 경고 포함 성공 1개 |
| `CompileAllBlueprints` | Blueprint Errors 0, Blueprint warnings 0, failed load 0. 별도 Summary에 기존 Battlefield Pose GUID와 MCP 고지 경고 유지 |
| 현재 에셋 이식 재검증 | FPV 전용 1/1, Blueprint 0/0/0, 스테이징 선택 자산·현재 Integration 금지 의존성 0, 이식 13개 LFS와 fsck 통과 |
| 기존 Standalone 시각 기록 | FPV 외형, 고정 추적 Camera, 실제 WBP HUD, Cyan 안내선, Current/Inactive Gate 표시 확인 |
| 사용자 수동 확인 | Training 두 Lap 비교 HUD, OilRig Map Check·화면·성능, Ground Drone/MG·NPC·Raw Drone 외형을 확인할 차례 |

현재 main의 `UDroneTrainingLapRecorderComponent`는 Segment/Lap 원본 뒤 TUT-04B 비교 결과도 만든다. 첫 성공은 기준 기록, 이후 성공은 현재 시도를 제외한 이전 평균과 Best를 사용한다. HUD에 이전 완주 평균·Best·시간 Delta·속도 Delta가 표시되며 계산은 Blueprint에 중복하지 않는다. 실제 두 Lap 표시 확인 전까지 TUT-04의 수동 판정은 남아 있다.

## 1. 런타임 연결 구조

### Training Map 전체 흐름

```text
/Game/Drone/Maps/Lvl_DroneTraining
│
├─ WorldSettings
│  └─ BP_DronePrototypeGameMode
│     ├─ BP_DroneFPVIntegration Spawn·Possess
│     │  ├─ CollisionComponent (Sphere Root)
│     │  ├─ VisualMeshComponent
│     │  ├─ CameraBoom → FollowCamera
│     │  ├─ UFloatingPawnMovement
│     │  └─ UDroneTelemetryComponent
│     │     └─ OnTelemetryUpdated Snapshot Event
│     │
│     └─ BP_DronePrototypePlayerController
│        └─ WBP_DroneFlightHUD 생성·재사용
│           └─ 현재 Possess Pawn의 Telemetry Event 구독
│
├─ BP_DroneTrainingCourse 1개
│  └─ ADroneTrainingCourse
│     ├─ CourseSpline
│     ├─ 비충돌 안내용 SplineMesh Segment
│     ├─ CourseId
│     ├─ OrderedGates[4]
│     ├─ UDroneTrainingGateSequenceComponent
│     │  ├─ 현재 통과할 Gate 위치
│     │  ├─ 순서·방향·중복 통과 판정
│     │  ├─ Gate Visual State 갱신
│     │  ├─ OnGateAccepted(Gate, Actor, Count, Location)
│     │  ├─ OnSequenceReset
│     │  └─ OnSequenceReconfigured
│     └─ UDroneTrainingLapRecorderComponent
│        ├─ Idle → Recording → Completed
│        ├─ Telemetry 10Hz 위치 표본으로 실제 이동 거리 누적
│        ├─ Segment/Lap 시간·거리·평균 속도 기록
│        ├─ 이전 평균·Best·Segment 비교 결과 생성
│        └─ OnLapStarted / OnSegmentRecorded / OnLapCompleted / OnLapComparisonReady
│
└─ BP_DroneTrainingGate 4개
   └─ ADroneTrainingGate
      ├─ GateRoot
      ├─ GateTrigger (Box, QueryOnly, Pawn Overlap)
      └─ RingVisualSegment 16개 (표시 전용, NoCollision)
```

실제 Asset 테스트는 Training Map에 다음 구성이 저장되어 있음을 확인한다.

- `BP_DronePrototypeGameMode` WorldSettings Override
- `PlayerStart` 정확히 1개
- 미리 배치된 Prototype Pawn 0개
- `BP_DroneTrainingCourse` 정확히 1개
- `BP_DroneTrainingGate` 정확히 4개
- Course의 `OrderedGates` 배열에 네 Gate가 중복 없이 명시적으로 연결됨
- Course가 native `GateSequenceComponent`와 `LapRecorderComponent`를 각각 한 개 소유함
- 네 Gate의 `CourseId`가 Course와 같음
- Gate의 `GateIndex`가 배열 위치 `0, 1, 2, 3`과 같음
- 각 Gate가 비음수가 아닌 `SegmentDistance` 메타데이터를 저장함
- 저장된 `RecastNavMesh` Actor가 PIE에서 존재함
- `/Game/ThirdPerson`, `/Game/Variant_` Actor를 Training Map에 직접 배치하지 않음

### Pawn·Input·HUD 연결

```text
IMC_DronePrototype
├─ IA_DronePrototype_Move
├─ IA_DronePrototype_Altitude
├─ IA_DronePrototype_Yaw
├─ IA_DronePrototype_Look
└─ IA_DronePrototype_CameraPitchRate

BP_DroneFPVIntegration
├─ ADronePrototypePawn native 기능·Input 계약
├─ CollisionComponent (Sphere Root)
├─ VisualMeshComponent (FPV Body, NoCollision)
├─ FPVRotorA~D (NoCollision)
├─ DroneEngineLoop (44.1 kHz Cue)
└─ UDroneTelemetryComponent
   └─ FDroneTelemetrySnapshot
      ├─ SpeedKilometersPerHour
      ├─ AltitudeMeters
      ├─ VerticalSpeedMetersPerSecond
      └─ HeadingDegrees

BP_DronePrototypePlayerController
└─ WBP_DroneFlightHUD
   ├─ SpeedValueText
   ├─ AltitudeValueText
   ├─ VerticalSpeedValueText
   └─ HeadingValueText
```

Prototype Pawn이 Input Mapping Context를 로컬 Player에 한 번 적용하고, UnPossess 또는 EndPlay에서 자신이 적용한 Context를 제거한다. PlayerController는 HUD를 한 개만 만들고 Pawn이 바뀌면 Widget을 다시 만들지 않고 Telemetry Source만 교체한다.

### NPC·Smart Object 준비 구조

```text
ADroneNPCSpawnPoint 또는 맵 직접 배치
└─ ADroneNPCCharacter
   ├─ UDroneNPCProfileComponent
   │  ├─ Faction: Neutral / Friendly / Hostile
   │  ├─ Weapon: Unarmed / Rifle / Shotgun
   │  └─ Hostile의 MG 사용 가능 여부
   └─ USmartObjectUserComponent
      └─ ADroneNPCAIController
         ├─ UStateTreeAIComponent
         │  ├─ Hostile: ST_NPC_HostilePatrol
         │  └─ Friendly: ST_NPC_FriendlyBaseRoutine
         ├─ UAIPerceptionComponent + Sight
         └─ UDroneSmartObjectReservationComponent
            └─ Activity Tag로 가장 가까운 빈 Slot Claim·Release

ADroneSmartObjectStation
└─ USmartObjectComponent
   └─ Smart Object Definition Asset
      ├─ EnemyPatrol / Guard
      ├─ FriendlyBasePatrol / Ambient
      ├─ Cover
      └─ MGTurret 1-Slot
```

Hostile은 `ST_NPC_HostilePatrol`에서 EnemyPatrol만 검색하고 Friendly는 `ST_NPC_FriendlyBaseRoutine`에서 FriendlyBasePatrol/Ambient를 번갈아 검색한다. 두 Tree 모두 Smart Object Runtime 초기화 뒤 Claim·NavMesh 이동·대기·해제를 반복하며 1-Slot 배타 예약과 직전 지점 회피를 사용한다. `ADronePrototypePawn` 감지 시 Hostile 이동과 예약을 안전하게 중단하지만 Search·공격 상태로 전환하지는 않는다. `Rifle`과 `Shotgun` Profile 및 분기 Getter는 준비됐지만 실제 발사·Damage·Animation은 아직 없다.

Definition·Station Blueprint 6쌍과 역할별 NPC Blueprint 3종, Spawn Point BP, 전용 Greybox 맵, Hostile/Friendly StateTree가 생성됐다. Profile·Possess·역할 Tag·NavMesh 투영에 더해 Hostile 2명과 Friendly 2명이 각각 2회 이상 완료하고 서로 다른 2지점 이상을 방문하도록 자동 검증했다. Friendly는 Base Patrol과 Ambient를 모두 방문한다. 후속 감지·점유 순서는 [`DRONE_SMART_OBJECT_NPC_GUIDE.md`](DRONE_SMART_OBJECT_NPC_GUIDE.md)를 따른다.

## 2. 디렉터리와 클래스 책임

### 현재 Drone 기능 소스

```text
Source/Drone/
├─ AI/
│  ├─ DroneAITypes.h
│  ├─ DroneAITags.h/.cpp
│  ├─ DroneNPCProfileComponent.h/.cpp
│  ├─ DroneNPCCharacter.h/.cpp
│  ├─ DroneNPCAIController.h/.cpp
│  ├─ DroneNPCSpawnPoint.h/.cpp
│  ├─ DroneNPCNavigationFloor.h/.cpp
│  ├─ DroneNPCPatrolStateTreeTasks.h/.cpp
│  ├─ DroneAIStateTreeAuthoringLibrary.h/.cpp
│  ├─ DroneSmartObjectStation.h/.cpp
│  ├─ DroneSmartObjectReservationComponent.h/.cpp
│  └─ Tests/
│     ├─ DroneSmartObjectFoundationTest.cpp
│     └─ DroneNPCGreyboxAssetTest.cpp
├─ Prototype/
│  ├─ DronePrototypeGameMode.h/.cpp
│  ├─ DronePrototypePawn.h/.cpp
│  ├─ DronePrototypePlayerController.h/.cpp
│  └─ Tests/
│     ├─ DroneFPVIntegrationAssetTest.cpp
│     ├─ DronePrototypeDefaultsTest.cpp
│     ├─ DronePrototypePIEInputLifecycleTest.cpp
│     └─ DronePrototypeSpawnPossessTest.cpp
├─ Telemetry/
│  ├─ DroneTelemetryTypes.h
│  ├─ DroneTelemetryComponent.h/.cpp
│  └─ Tests/DroneTelemetryTest.cpp
├─ UI/
│  ├─ DroneFlightHUDWidget.h/.cpp
│  └─ Tests/
│     ├─ DroneFlightHUDBlueprintAssetTest.cpp
│     └─ DroneFlightHUDTest.cpp
└─ Tutorial/
   ├─ DroneTrainingCourse.h/.cpp
   ├─ DroneTrainingGateTypes.h
   ├─ DroneTrainingGate.h/.cpp
   ├─ DroneTrainingGateSequenceComponent.h/.cpp
   ├─ DroneTrainingRecordTypes.h
   ├─ DroneTrainingLapRecorderComponent.h/.cpp
   └─ Tests/
      ├─ DroneTrainingCourseTest.cpp
      ├─ DroneTrainingGateSequenceTest.cpp
      ├─ DroneTrainingRecordCalculationTest.cpp
      ├─ DroneTrainingLapRecorderTest.cpp
      ├─ DroneTrainingAssetTest.cpp
      └─ DroneTrainingPIESmokeTest.cpp
```

### 핵심 클래스 책임

| 클래스·구조체 | 담당 책임 | 담당하지 않는 책임 |
|---|---|---|
| `ADronePrototypeGameMode` | Prototype Pawn과 PlayerController의 native 기본 Class 제공 | Mission·Lap·점수 규칙 |
| `ADronePrototypePawn` | Enhanced Input Binding, 이동, 고도 이동, Actor Yaw, Camera Pitch, Component 소유 | HUD 생성, Gate 순서 판정, 최종 비행 물리 |
| `UDroneTelemetryComponent` | 0.1초 기본 Timer와 즉시 갱신으로 Telemetry Snapshot 계산·Broadcast, Lap Recorder의 위치 표본 주기 제공 | 화면 배치, Lap 계산, 지형 AGL 계산 |
| `ADronePrototypePlayerController` | 로컬 HUD 한 개의 생성·재사용·정리, Possess Pawn과 Telemetry 연결 | Telemetry 수치 계산, HUD Designer 외형 |
| `UDroneFlightHUDWidget` | Snapshot 표시 문자열 생성, C++↔WBP TextBlock 연결, native fallback | Pawn 검색 Tick, 비행 수치 계산, Gate 안내 UI |
| `ADroneTrainingCourse` | Spline·안내선, `CourseId`, 명시적 `OrderedGates`, Sequence와 Lap Recorder Component 소유 | Trigger 감지, 방향 수학, 결과 UI |
| `ADroneTrainingGate` | Ring Visual, Box Trigger, 진입 위치 보존, 이탈 시 Sequence에 통과 시도 전달 | 현재 Gate 결정, 순서 진행, Lap 기록 |
| `UDroneTrainingGateSequenceComponent` | 구성 검증, 현재 Gate, 순서·방향·중복 판정, Visual State, 승인 Actor·위치를 포함한 `OnGateAccepted`, Reset·Reconfigure Event | Visual Mesh 생성, Overlap 감지, 시간·점수·SaveGame |
| `UDroneTrainingLapRecorderComponent` | Gate 0 시작, Segment/Lap 완료, World Game Time, Telemetry 10Hz 위치 거리, 평균 속도, 실행 중 성공 History와 Blueprint Event | 이전 평균·Best 비교, 점수, UMG, SaveGame, Multiplayer |
| `FDroneTrainingSegmentRecord` | 이전 정상 Gate부터 현재 Gate까지 Index·시간·실제 이동 거리·평균 속도 보관 | 비교·표시 문자열 |
| `FDroneTrainingLapRecord` | Gate 0부터 마지막 Gate까지 완료 여부·총시간·총거리·평균 속도·Segment 배열 보관 | 영구 저장·점수 |
| `FDroneTelemetrySnapshot` | HUD와 후속 기록 계층에 전달하는 비행 수치 묶음 | 자체 갱신·표시 |
| `EDroneTrainingGatePassResult` | 통과 성공 또는 거부 이유 표현 | 사용자 메시지 표시 |
| `EDroneTrainingGateVisualState` | `Inactive`, `Current`, `Completed` 상태 표현 | Lap 상태 표현 |
| `EDroneTrainingLapRecordState` | `Idle`, `Recording`, `Completed` 기록 상태 표현 | Gate 시각 상태 표현 |
| `FDroneNPCProfile` | NPC의 Friendly/Hostile 역할, Rifle/Shotgun 장비 종류와 MG 사용 가능 여부 | 최종 진영 설정, 무기 수치·피해·Animation |
| `ADroneNPCCharacter` | 프로젝트 소유 NPC Character, Profile과 Smart Object User Component 소유 | 외형·Animation 확정, 행동 의사결정 |
| `ADroneNPCAIController` | StateTree·Sight·예약 Component 소유, 역할별 Tree 시작, Hostile/Friendly 다음 Slot Claim과 방문 기록, 드론 감지 안전 중단·무기 분기 제공 | Search, Rifle/Shotgun/MG 발사 구현 |
| `FDroneStateTree*PatrolSlotTask` | Hostile/Friendly Claim, 공용 NavMesh Move·Wait, 역할별 Release 실행 | Search·사격·Animation |
| `UDroneSmartObjectReservationComponent` | Activity/User Tag로 빈 Slot 검색·Claim·Release, 직전 위치 반경 회피 검색 | Animation, StateTree 상태 선택 |
| `UDroneAIStateTreeAuthoringLibrary` | Editor에서 Hostile 순찰·Friendly 기지 루틴 StateTree 생성 및 Schema/상태/Task 검증 | 런타임 의사결정, 기존 Asset 덮어쓰기 |
| `ADroneSmartObjectStation` | Definition이 연결될 프로젝트 소유 Host와 방향 Preview, Authoring Tool용 Definition·Mesh 연결 함수 | Interaction StateTree와 NPC 행동 실행 |
| `ADroneNPCSpawnPoint` | NPC Class·Profile·수·간격에 따른 명시적 Spawn | NPC의 순찰 위치와 행동 선택 |
| `ADroneNPCNavigationFloor` | Greybox에서 BlockAll 충돌과 Navigation Relevant 바닥을 제공 | 최종 환경 Mesh·대규모 맵 NavMesh 성능 정책 |

### Smart Object Asset

```text
Content/Drone/AI/SmartObjects/
├─ Definitions/
│  ├─ SO_Def_EnemyPatrol.uasset
│  ├─ SO_Def_FriendlyBasePatrol.uasset
│  ├─ SO_Def_Ambient.uasset
│  ├─ SO_Def_Guard.uasset
│  ├─ SO_Def_Cover.uasset
│  └─ SO_Def_MGTurret.uasset
└─ Blueprints/
   ├─ BP_SO_EnemyPatrol.uasset
   ├─ BP_SO_FriendlyBasePatrol.uasset
   ├─ BP_SO_Ambient.uasset
   ├─ BP_SO_Guard.uasset
   ├─ BP_SO_Cover.uasset
   └─ BP_SO_MGTurret.uasset
```

각 Definition은 Slot 1개·해당 Activity Tag·Gameplay Interaction Behavior 1개를 가진다. Definition의 Interaction StateTree는 아직 비어 있고 MG Blueprint에만 `MG_Turret_SK` 후보 Mesh가 연결돼 있다. Hostile 순찰은 별도 Controller StateTree `/Game/Drone/AI/StateTrees/ST_NPC_HostilePatrol`이 실행한다.

### NPC 역할·Greybox Asset

```text
Content/Drone/AI/Blueprints/
├─ BP_NPC_Hostile_Rifle.uasset
├─ BP_NPC_Hostile_Shotgun.uasset
├─ BP_NPC_Friendly_Base.uasset
└─ BP_NPCSpawnPoint.uasset

Content/Drone/AI/StateTrees/
├─ ST_NPC_HostilePatrol.uasset
└─ ST_NPC_FriendlyBaseRoutine.uasset

Content/Drone/Maps/
└─ Lvl_NPCSmartObjectGreybox.umap
```

맵에는 Rifle 1명, Shotgun 1명, Friendly 2명과 Smart Object Station 10개가 있다. Manny Simple·`ABP_Unarmed`은 기능 배치 확인용 임시 외형이다. Soldier/Insurgent 후보 중 최종 선택은 아직 미정이다.

### 중앙 Map Asset

```text
Content/Drone/Maps/
├─ Lvl_DroneTraining.umap
├─ Lvl_DronePrototype.umap
├─ Lvl_NPCSmartObjectGreybox.umap
├─ Lvl_DronePackShowcase.umap
└─ Lvl_DronePackShowcase_BuiltData.uasset
```

### Tutorial Asset

```text
Content/Drone/Tutorial/
├─ Blueprints/
│  ├─ BP_DroneTrainingCourse.uasset
│  └─ BP_DroneTrainingGate.uasset
└─ Materials/
   └─ M_DroneTrainingGuide.uasset
```

`M_DroneTrainingGuide`는 Course 안내선과 Gate Ring이 함께 사용한다. 자동화에서는 Opaque, Unlit, Spline Mesh Usage를 확인한다.

### Prototype Asset

```text
Content/Drone/Prototype/
├─ Blueprints/
│  ├─ BP_DronePrototypeGameMode.uasset
│  ├─ BP_DronePrototypePawn.uasset
│  └─ BP_DronePrototypePlayerController.uasset
├─ Input/
│  ├─ IMC_DronePrototype.uasset
│  └─ Actions/
│     ├─ IA_DronePrototype_Move.uasset
│     ├─ IA_DronePrototype_Altitude.uasset
│     ├─ IA_DronePrototype_Yaw.uasset
│     ├─ IA_DronePrototype_Look.uasset
│     └─ IA_DronePrototype_CameraPitchRate.uasset
└─ UI/
   └─ WBP_DroneFlightHUD.uasset
```

### 기존 C++ Template·Variant 영역

다음 C++ 영역과 대응 `/Game/ThirdPerson`, 세 `/Game/Variant_*` 비맵 Content는 저장소에 남아 있지만 현재 Drone Tutorial 실행 흐름으로 사용한다고 판단하면 안 된다. Content Root 전체 삭제는 범위가 넓어 `909f6a3`에서 62개를 복구했고, Unreal 생성 기본 Map 4개만 삭제 상태다.

```text
Source/Drone/DroneCharacter.*
Source/Drone/DroneGameMode.*
Source/Drone/DronePlayerController.*
Source/Drone/Variant_Combat/
Source/Drone/Variant_Platforming/
Source/Drone/Variant_SideScrolling/
```

`Config/DefaultEngine.ini`의 Game·Editor 시작 Map은 `/Game/Drone/Maps/Lvl_DroneTraining`, 전역 GameMode는 프로젝트 소유 `BP_DronePrototypeGameMode`를 가리킨다. 세 제작 Map의 현재 구조와 추가 규칙은 [`DRONE_CONTENT_FOLDER_GUIDE.md`](DRONE_CONTENT_FOLDER_GUIDE.md)를 따른다. Variant에 AI·StateTree 코드가 남아 있다는 사실은 Enemy AI MVP가 구현됐다는 뜻이 아니다.

## 3. C++와 Blueprint·Editor의 경계

### C++에서 고정하는 부분

- Pawn Component 구조와 이동·Camera 입력 함수
- Input Action Binding과 Mapping Context 적용·제거 수명주기
- Telemetry 단위 변환, Timer, Snapshot Event
- PlayerController의 HUD 생성·재사용·Delegate 정리
- HUD 표시 문자열 형식과 C++↔WBP TextBlock 이름 계약
- Course 안내선 재생성과 Collision·Overlap·Physics·Navigation 비간섭 규칙
- Gate Trigger의 Pawn Overlap 설정
- Gate Ring Visual의 NoCollision·NoOverlap·NoPhysics·NoNavigation 규칙
- Gate 구성 유효성 검사
- 순서·정방향·중복 통과 판정
- `Inactive → Current → Completed` 상태 전환
- 정상 통과 때 Gate·통과 Actor·승인 수·승인 위치를 포함한 `OnGateAccepted` Broadcast
- Sequence Reset과 Reconfigure Event 및 부분 기록 정리 수명주기
- Gate 0부터 마지막 Gate까지 World Game Time 기반 Segment/Lap 기록
- Telemetry 10Hz 위치 표본과 Gate 승인 끝점을 합산한 3차원 실제 이동 거리
- Segment/Lap 평균 속도 계산과 실행 중 성공 History
- `OnLapStarted`, `OnSegmentRecorded`, `OnLapCompleted` Blueprint Event

위 규칙은 BP나 Level 저장값이 잘못 바뀌어도 Construction 또는 BeginPlay에서 다시 적용되는 항목이 있다. 특히 Course 표시선과 Gate Visual의 Collision을 Editor에서 임의로 켜지 않는다.

### Blueprint와 Editor에서 조정하는 부분

- `BP_DronePrototypePawn`에 IMC와 Input Action Asset 연결
- `BP_DronePrototypeGameMode`의 BP Pawn·BP PlayerController Class 선택
- `BP_DronePrototypePlayerController`의 `WBP_DroneFlightHUD` Class 선택
- WBP Designer의 위치·크기·색·폰트
- Course Spline Point와 Tangent 편집
- Course Actor의 `CourseId`와 `OrderedGates` 배열
- Gate Actor의 위치·회전
- Gate별 `CourseId`, `GateIndex`, `SegmentDistance`
- Gate Radius, Ring Thickness, Trigger 크기, 상태별 색, Mesh·Material 같은 Greybox 외형값
- 후속 TUT-04에서 Lap Recorder의 Blueprint Event와 Getter를 사용하는 결과 UI 외형

현재 Gate와 기록 규칙을 위해 BP Event Graph에 별도의 Overlap·순서·시간·거리 계산을 다시 만들 필요가 없다. 실제 Trigger Delegate, Gate 판정과 기록 계산은 native C++에 있다. Blueprint는 배치·참조·외형과 TUT-04 표시 계층으로 유지한다.

### 반드시 지킬 데이터 계약

1. `OrderedGates` 배열 위치가 유일한 통과 순서다.
2. 첫 Gate의 배열 위치와 `GateIndex`는 `0`이다. `1`부터 시작하지 않는다.
3. 각 `GateIndex`는 자신의 배열 위치와 정확히 같아야 한다.
4. 한 Gate를 배열에 두 번 넣지 않는다.
5. Course와 모든 Gate의 `CourseId`가 같아야 한다.
6. `SegmentDistance`는 비음수 배치 메타데이터다. TUT-02의 순서 판정과 TUT-03의 실제 이동 거리 계산에는 사용하지 않는다.
7. Gate Actor의 로컬 `+X`가 유일한 정방향이다. Actor 회전이 바뀌면 World 정방향도 함께 바뀐다.

1~7의 Sequence 구성 계약을 어기면 전체 구성이 Invalid Configuration이 되고 Gate 진행이 시작되지 않는다.

기록 계층에는 다음 규칙이 추가된다.

- 한 Lap은 Gate 0을 통과한 같은 Drone만 이어서 기록한다. 중간에 다른 Drone이 승인되면 Sequence에 멀티플레이 규칙을 추가하지 않고 현재 부분 기록만 폐기한다.
- 현재 네 Gate Map에서 Gate 0은 출발선이며 기록 Segment는 `0→1`, `1→2`, `2→3`의 세 개다.

## 4. Gate 통과 흐름

### 초기 구성

1. Course의 `OnConstruction` 또는 `BeginPlay`가 실행된다.
2. Course가 Spline 표시선을 재생성하고 비간섭 규칙을 적용한다.
3. Course가 `CourseId`와 `OrderedGates`를 Sequence Component에 전달한다.
4. Sequence는 빈 CourseId, 빈 배열, null Gate, 중복 Gate, CourseId 불일치, GateIndex 불일치를 검사한다.
5. 구성이 유효하면 각 Gate에 자신을 담당 Sequence로 연결한다.
6. Gate 0은 `Current`, 나머지는 `Inactive`가 된다.

### 실제 Overlap 처리

```text
Drone이 GateTrigger에 들어감
→ BeginOverlap
→ ADronePrototypePawn인지 확인
→ 최초 Entry World Location 저장

Drone이 GateTrigger를 완전히 빠져나감
→ EndOverlap
→ 저장한 Entry Location 회수
→ 현재 Exit World Location과 함께 Sequence에 전달
→ TryAcceptTraversal 판정
```

중요한 점은 Trigger에 들어오는 순간이 아니라 완전히 빠져나와 `EndOverlap`이 발생할 때 통과가 판정된다는 것이다. Trigger 안에서 멈추면 아직 통과로 기록되지 않는다.

### 판정 순서

`TryAcceptTraversal`은 다음 순서로 검사한다.

1. Sequence 구성이 유효한가
2. 통과 Actor가 `ADronePrototypePawn` 또는 그 BP 자식인가
3. Gate가 현재 Sequence의 `OrderedGates`에 들어 있는가
4. 이미 완료한 Gate인가
5. 현재 기대하는 배열 위치의 Gate인가
6. Gate 평면을 로컬 `+X` 방향으로 관통했는가

정방향 판정의 현재 C++ 기준은 다음과 같다.

- Entry와 Exit 사이 이동 거리가 최소 1 cm 이상
- Entry가 Gate 중심 기준 Forward 반대편 1 cm 바깥
- Exit가 Gate 중심 기준 Forward 앞쪽 1 cm 바깥
- 이동 선분과 Gate 평면의 교차점이 원형 Trigger aperture 안쪽

Box Trigger는 Overlap 수집용이라 모서리가 원 바깥으로 튀어나오지만, 최종 판정은 교차점을 Gate local space로 바꿔 YZ 원형 반경을 다시 검사한다. 따라서 Box 모서리만 지나거나 같은 쪽으로 되돌아가면 정상 관통으로 인정하지 않는다. Actor Scale을 바꾸더라도 같은 local aperture 기준을 사용하므로 화면 Ring·Trigger와 판정 크기가 함께 변한다.

### 판정 결과

| 결과 | 의미 | 진행 변화 |
|---|---|---|
| `Accepted` | 현재 Gate를 정방향으로 정상 통과 | 정확히 한 칸 진행 |
| `InvalidActor` | Prototype Drone이 아닌 Actor | 없음 |
| `InvalidConfiguration` | Course·Gate 배열 계약 오류 | 없음 |
| `GateNotInSequence` | 현재 Course 목록에 없는 Gate | 없음 |
| `WrongOrder` | 아직 차례가 아닌 미래 Gate | 없음 |
| `WrongDirection` | 역방향, 평면 미관통, 원형 aperture 밖, 이동량 부족 | 없음 |
| `AlreadyCompleted` | 이미 끝난 Gate 재통과 | 없음 |

정상 통과하면 다음 처리가 이어진다.

```text
NextExpectedGatePosition + 1
→ 이전 Gate = Completed
→ 다음 Gate = Current
→ 나머지 Gate = Inactive
→ OnGateAccepted(Gate, PassingActor, AcceptedGateCount, AcceptedWorldLocation) Broadcast
```

마지막 Gate를 통과하면 모든 Gate가 `Completed`가 되고 `GetCurrentGate()`는 null, `GetCurrentGateIndex()`는 `INDEX_NONE`이 된다. TUT-03 Recorder는 이 승인 Event로 Lap 원본 기록을 완성하지만, 아직 결과 UI나 평가 화면은 띄우지 않는다.

### Segment/Lap 기록 흐름

```text
Gate 0 정상 승인
→ Lap Recorder = Recording
→ World Game Time과 승인 위치를 Lap·첫 Segment 시작점으로 저장
→ 같은 Drone의 기존 Telemetry 10Hz Event 구독

Telemetry Event
→ 직전 World 위치부터 현재 World 위치까지 3차원 거리 누적

Gate 1~마지막 Gate 정상 승인
→ 승인 위치를 정확한 마지막 표본으로 추가
→ 이전 정상 Gate부터 현재 Gate까지 Segment 확정
→ ElapsedSeconds / TravelDistanceMeters / AverageSpeedKilometersPerHour 계산
→ OnSegmentRecorded Broadcast

마지막 Gate 정상 승인
→ Lap 총시간·총거리·평균 속도와 Segment 배열 확정
→ 실행 중 SuccessfulLaps에 성공 기록 1개 추가
→ Recorder = Completed
→ OnLapCompleted Broadcast
```

시간은 Gate 승인 시점의 World Game Time 차이로 계산한다. 거리는 Gate에 저장된 `SegmentDistance`나 Spline 길이가 아니라, Gate 0 승인 뒤 Telemetry의 기본 0.1초 주기마다 얻은 Drone World 위치 사이의 거리를 합산한다. 각 Gate 승인 위치도 마지막 표본으로 추가하므로 Segment 경계가 10Hz 표본 사이에 있어도 끝점을 놓치지 않는다. 평균 속도는 `실제 이동 거리 ÷ 시간`을 km/h로 변환한 값이다.

`ResetSequence()`는 Gate 진행과 진행 중인 Lap을 Gate 0·`Idle`로 되돌린다. 아직 완료하지 않은 시간·거리·Segment는 폐기하지만, 같은 실행에서 이미 완료한 `SuccessfulLaps` History는 유지한다. 반대로 Gate 배열이나 Course 구성을 다시 적용하면 서로 다른 코스 기록이 섞이지 않도록 성공 History까지 비운다. Recorder와 Sequence는 별도 Tick을 사용하지 않으며, Pawn·Course 종료와 활성 Drone 파괴 때 Delegate를 정리한다.

Blueprint에서 사용할 수 있는 현재 데이터 경계는 다음과 같다.

- 상태·준비 여부: `GetRecordState`, `IsRecordingReady`, `IsLapRecording`
- 진행 중 값: `GetCurrentLapElapsedSeconds`, `GetCurrentSegmentElapsedSeconds`, 현재 Lap·Segment 이동 거리
- 성공 기록: `HasCompletedLap`, `GetSuccessfulLapCount`, `GetSuccessfulLaps`, `GetLastCompletedLap`
- Event: `OnLapStarted`, `OnSegmentRecorded`, `OnLapCompleted`

이 API가 준비됐다는 것은 TUT-04 UI가 연결될 수 있다는 뜻이지, 현재 결과 Widget이 이미 존재한다는 뜻은 아니다.

### Visual과 Trigger의 분리

| 구성 | 현재 규칙 |
|---|---|
| Gate Actor | Trigger를 사용하므로 Actor Collision Enabled |
| `GateTrigger` | `QueryOnly`, `WorldDynamic`, Pawn만 `Overlap`, 다른 채널 Ignore |
| `GateTrigger` | Overlap 생성 On, Physics Off, Navigation 영향 Off, 게임 화면에서는 숨김 |
| Ring Visual 16개 | Collision Off, Overlap Off, Physics Off, Navigation 영향 Off |
| Course Spline·안내선 | Collision Off, Overlap Off, Physics Off, Navigation 영향 Off |

Gate Actor의 Collision이 켜져 있는 것은 Ring이 Drone을 막는다는 뜻이 아니다. 판정용 Box Trigger만 Query Overlap에 참여하며 Ring Mesh는 비충돌이다.

### 상태별 기본 색

| 상태 | 기본 색 | 의미 |
|---|---|---|
| `Inactive` | 어두운 남색 `(0.02, 0.08, 0.18, 1)` | 아직 차례가 아님 |
| `Current` | 밝은 녹색 `(0.10, 1.00, 0.18, 1)` | 지금 통과할 Gate |
| `Completed` | Cyan `(0.02, 0.70, 1.00, 1)` | 정상 통과 완료 |

Ring은 Engine Cube 16개로 원을 근사한 Greybox다. 기본 Radius는 220 cm, Ring Thickness는 24 cm다. Trigger 기본 Half Depth는 60 cm, Y·Z Half Size는 175 cm다. 최종 아트나 최종 난이도 수치로 확정된 값은 아니다.

## 5. 현재 구현과 미구현

### 기존 main과 현재 AI 기능 Branch에 구현된 것

- 별도 Prototype Drone Pawn과 Enhanced Input
- 전후·좌우·상승·하강·Yaw·Camera Pitch 조작
- Telemetry Snapshot과 WBP Flight HUD
- 별도 `Lvl_DroneTraining`
- 비충돌 Spline Course 안내선
- 실제 `BP_DroneTrainingGate`
- Training Map에 배치된 Greybox Gate 4개
- Course의 명시적 `OrderedGates[4]`
- CourseId·GateIndex·중복 Gate 구성 검증
- Prototype Drone만 허용하는 Box Trigger
- 정방향 평면 관통 판정
- Gate 순서 판정
- 완료 Gate 중복 통과 방지
- `Inactive`, `Current`, `Completed` Visual 전환
- Sequence Reset 함수
- Reset 시 진행 중인 BeginOverlap 기록 폐기
- Gate 또는 Course가 먼저 파괴돼도 Sequence 유효성·역참조를 안전하게 정리
- 통과 Actor와 승인 위치를 포함하는 정상 통과 경계 Event `OnGateAccepted`
- Sequence의 Reset·Reconfigure Event
- Course가 소유하는 `UDroneTrainingLapRecorderComponent`
- Gate 0 승인 시 Lap 시작, 마지막 Gate 승인 시 Lap 완료
- World Game Time 기반 Gate별 Segment Time과 전체 Lap Time
- Telemetry 기본 10Hz World 위치 표본과 Gate 승인 끝점을 이용한 실제 3차원 이동 거리
- Segment/Lap 평균 속도와 `FDroneTrainingSegmentRecord`, `FDroneTrainingLapRecord`
- `Idle`, `Recording`, `Completed` 기록 상태
- 실행 중 성공 Lap History와 Reset 시 성공 History 보존
- `OnLapStarted`, `OnSegmentRecorded`, `OnLapCompleted` Blueprint Event
- Gate Trigger·Ring·Course 안내선의 Collision·Navigation 안전 규칙
- 순수 계산, native World, 실제 Asset, 실제 PIE를 포함한 Tutorial 자동화 6개
- Smart Objects·Gameplay Interactions 모듈 연결
- NPC Friendly/Hostile, Unarmed/Rifle/Shotgun, MG 허용 Profile
- 적 순찰·아군 기지 순찰·생활·경계·엄폐·MG Activity Tag
- NPC Character·AI Controller·Spawn Point·Smart Object Station C++ 기반
- Activity Tag 기반 가장 가까운 빈 Smart Object Slot Claim·Release
- Drone Prototype의 Sight 감지 대상 등록과 Hostile용 Detected/Lost StateTree Event
- Hostile `ST_NPC_HostilePatrol`과 Native Claim·Move·Wait·Release Task
- Hostile 2명의 EnemyPatrol 반복 이동·직전 지점 우선 회피·방문 기록
- Friendly `ST_NPC_FriendlyBaseRoutine`과 Base Patrol/Ambient 교대·Fallback·방문 기록
- Hostile/Friendly 4명의 역할별 이동과 Smart Object 1-Slot 배타 Claim
- 감지·이동 실패·UnPossess 경로의 예약 해제

### 아직 구현하지 않은 것

- 통과 품질·점수·평가
- Gate 진행 HUD, 다음 Gate 화살표, Wrong Order·Wrong Direction 메시지
- Course HUD, Gate 결과 Toast, Lap 결과 화면
- Spline에서 Gate를 자동 생성하거나 자동 정렬하는 Editor Tool
- Gate 완료와 Mission·귀환·평가 시스템 연결
- SaveGame 또는 기록 저장
- Network Replication과 Multiplayer 권한 처리
- Prototype Pawn 이외의 Drone Class 허용 정책
- 최종 Gate Mesh·VFX·SFX·Animation
- 최종 코스 배치·크기·난이도
- 배터리·통신거리·재밍 같은 후보 시스템
- 감지 후 Search·Return과 순찰 복귀의 PIE 동작
- Rifle 단일 Trace, Shotgun Pellet/Spread, Damage·재장전·Animation·FX·SFX
- MG 이동·한 명 점유·조준·사격과 사망/중단 뒤 재점유
- Cover·Search·Return 실제 행동

TUT-03의 원본 시간·거리·평균 속도와 TUT-04B의 이전 평균·Best·Delta·HUD 표시는 구현됐다. `USaveGame` 영속화와 점수는 아직 구현하지 않았다. `SegmentDistance`는 현재도 배치 메타데이터이며 실제 이동 거리 계산에 사용하지 않는다.

## 6. 사용자가 지금 할 일과 반복하지 않아도 되는 일

### 지금 사용자가 할 일

1. 다른 PC에서는 Unreal 저장소 `main`을 Pull하고 원격 최신 Commit과 일치하는지 확인한다.
2. UE 5.8.1에서 `/Game/Drone/Maps/Lvl_DroneTraining`을 연다.
3. World Outliner에서 Course와 Gate 네 개의 배치가 의도한 비행 경로처럼 보이는지 확인한다.
4. Course의 `OrderedGates` 순서와 실제 공간 배치 순서가 자연스러운지 확인한다.
5. Gate의 크기, 간격, 높이, 색 대비가 직접 조종할 때 읽기 쉬운지 확인한다.
6. PIE에서 Gate 0부터 3까지 정방향으로 한 번 완주한다.
7. Gate 0 통과 뒤 Recorder가 `Recording`, Gate 3 통과 뒤 `Completed`가 되는지 확인한다.
8. 완료 기록이 1개이고 Segment가 `0→1`, `1→2`, `2→3` 세 개인지 확인한다.
9. Lap과 각 Segment의 시간이 0보다 크고, 이동 거리가 실제 비행 경로만큼 누적되며, 평균 속도가 유한한 양수인지 확인한다.
10. 같은 PIE에서 `ResetSequence()`를 실행해 Gate 0이 Current, Recorder가 `Idle`, `IsRecordingReady=true`가 되는지 확인한다.
11. Reset 뒤에도 방금 완료한 성공 Lap 1개가 유지되고, 진행 중 값과 미완료 Segment만 초기화되는지 확인한다.
12. 한 번은 미래 Gate를 먼저 통과하고, 한 번은 현재 Gate를 역방향으로 통과해 Gate 진행과 기록이 바뀌지 않는지 확인한다.
13. 조종 감각상 너무 작음, 너무 큼, 간격 과도, 방향 이해 어려움이 있으면 수치와 체감만 기록한다.
14. FPV Body와 Rotor 4개의 크기·방향·위치가 자연스럽고 Camera를 가리지 않는지 확인한다.
15. 실제 스피커에서 Drone Loop가 한 겹으로 여러 반복 경계를 이어가며 PIE/Standalone 종료 즉시 멈추는지 확인한다.
16. AI 기능이 병합된 뒤 Editor를 재시작하고 Smart Objects와 Gameplay Interactions Plugin 활성 상태를 확인한다.
17. Content Browser에서 생성된 Definition·Station BP 6쌍과 MG Mesh 연결을 확인한다.
18. `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`을 열고 Rifle 1명·Shotgun 1명·Friendly 2명과 Station 10개의 위치·방향이 알아보기 쉬운지 확인한다.
19. Editor에서 `P` 키를 눌러 네 NPC 시작점과 Station 사이에 녹색 NavMesh가 이어지는지 눈으로 확인한다.
20. Manny/Unarmed 외형은 임시임을 전제로 PIE에서 Hostile 2명이 EnemyPatrol 3개 사이를 반복하는지, 서로 겹치거나 제자리만 다시 고르지 않는지 눈으로 확인한다.
21. Friendly 2명이 FriendlyBasePatrol 3개와 Ambient 2개 사이를 이동하고 같은 지점에 동시에 머물지 않는지 눈으로 확인한다.

사용자가 지금 판단해야 하는 것은 플레이할 때의 가독성·조종 난이도, 실제 비행에서 기록값이 자연스럽게 증가하는지, FPV 외형·Camera·소리가 실제 환경에서 자연스러운지다. 정확한 공식과 파일·참조 구조는 자동 검증했지만, Gate 배치와 사람이 체감하는 시간·거리·속도·청감은 직접 확인이 필요하다.

### 반복하지 않아도 되는 일

- `ADroneTrainingGate`와 Sequence Component를 다시 만들 필요 없음
- `BP_DroneTrainingGate`를 새로 생성할 필요 없음
- Training Map에 Gate 네 개를 다시 배치할 필요 없음
- Course의 Ordered Array를 처음부터 다시 연결할 필요 없음
- Course 안내 Material을 새로 만들 필요 없음
- BP Event Graph에 Begin/End Overlap 판정을 중복 구현할 필요 없음
- BP Event Graph나 Tick에서 Lap 시간·거리·평균 속도를 다시 계산할 필요 없음
- Lap Recorder에 별도 Tick이나 Timer를 추가할 필요 없음
- 실제 이동 거리에 Gate의 `SegmentDistance`나 Spline 길이를 대입할 필요 없음
- Gate를 Level에서 검색해 거리순으로 자동 정렬하는 BP를 만들 필요 없음
- GateIndex를 보기 편하다는 이유로 `1~4`로 바꾸면 안 됨
- Ring Mesh에 Block Collision을 켤 필요 없음
- 단순 시각·수동 비행 확인만 했다면 Build·14개 자동화를 매번 다시 돌릴 필요 없음
- Android 설정을 진행할 필요 없음
- Greybox 확인 전에 추가 에셋 구매나 전체 외형 교체를 진행할 필요 없음
- TUT-03 확인 중 비교·Best·결과 UI·Mission UI까지 함께 구현할 필요 없음
- 현재 작업과 무관하게 전역 Default Map을 바꿀 필요 없음
- 역할별 NPC Blueprint와 Greybox 맵을 다시 만들 필요 없음
- Hostile 순찰 StateTree를 BP Event Graph에서 다시 만들 필요 없음
- Friendly BaseRoutine을 BP Event Graph에서 다시 만들 필요 없음
- Hostile이 드론 감지 뒤 아직 Search·사격하지 않는 현상을 현재 단계 오류로 오해할 필요 없음

코드나 BP·Map Asset을 실제로 수정했다면 그때 Build, Tutorial 테스트, 전체 회귀, Blueprint Compile을 다시 실행한다.

## 7. 추천 코드 읽기 순서

### Gate와 TUT-03 기록 기능을 먼저 이해할 때

1. `Source/Drone/Tutorial/DroneTrainingGateTypes.h`
   - Visual State, Pass Result와 Gate 승인·Reset·Reconfigure Event 계약을 먼저 확인한다.
2. `Source/Drone/Tutorial/DroneTrainingGateSequenceComponent.h`
   - Sequence가 공개하는 상태·함수·Event 계약을 읽는다.
3. `Source/Drone/Tutorial/DroneTrainingGateSequenceComponent.cpp`
   - 구성 검증, 판정 순서, 방향 수학, 상태 전환과 Event 발생 시점을 읽는다.
4. `Source/Drone/Tutorial/DroneTrainingGate.h`
   - Gate가 보관하는 Definition·Visual·Trigger 값을 확인한다.
5. `Source/Drone/Tutorial/DroneTrainingGate.cpp`
   - Ring 생성, Collision 분리, Begin/End Overlap 전달 과정을 읽는다.
6. `Source/Drone/Tutorial/DroneTrainingRecordTypes.h`
   - Segment/Lap 원본 데이터와 `Idle`, `Recording`, `Completed` 상태를 확인한다.
7. `Source/Drone/Tutorial/DroneTrainingLapRecorderComponent.h/.cpp`
   - Gate 0 시작, Telemetry 거리 표본, Segment/Lap 완료, Reset·History·Delegate 수명주기를 읽는다.
8. `Source/Drone/Tutorial/DroneTrainingCourse.h/.cpp`
   - Course가 `OrderedGates`, Sequence와 Lap Recorder를 소유하고 Play 전에 연결하는 순서를 읽는다.

### 검증 의도를 이해할 때

9. `Source/Drone/Tutorial/Tests/DroneTrainingRecordCalculationTest.cpp`
   - cm·초를 km/h로 변환하는 순수 계산과 0·음수·NaN·무한대 방어를 읽는다.
10. `Source/Drone/Tutorial/Tests/DroneTrainingLapRecorderTest.cpp`
    - Gate 0 시작, 꺾인 실제 이동 거리, Segment/Lap 완료, Reset·History·Pawn 파괴·재구성을 읽는다.
11. `Source/Drone/Tutorial/Tests/DroneTrainingGateSequenceTest.cpp`
   - 잘못된 Actor, Wrong Order, Wrong Direction, 중복, 정상 완료, Reset, 실제 Overlap 검증을 읽는다.
12. `Source/Drone/Tutorial/Tests/DroneTrainingAssetTest.cpp`
    - 실제 BP 부모 Class, Map Actor 수, Ordered Array, GateIndex, Recorder와 Collision 계약을 읽는다.
13. `Source/Drone/Tutorial/Tests/DroneTrainingPIESmokeTest.cpp`
    - 실제 BP Pawn·Controller·WBP·Course·Gate·Recorder가 PIE에서 함께 연결되는지 확인한다.
14. `Source/Drone/Tutorial/Tests/DroneTrainingCourseTest.cpp`
    - TUT-01 안내선이 Gate와 Recorder 추가 뒤에도 비행을 막지 않는지 확인한다.

### Drone 전체 데이터 흐름까지 이어서 읽을 때

15. `Source/Drone/Prototype/DronePrototypePawn.h/.cpp`
16. `Source/Drone/Telemetry/DroneTelemetryTypes.h`
17. `Source/Drone/Telemetry/DroneTelemetryComponent.h/.cpp`
18. `Source/Drone/Prototype/DronePrototypePlayerController.h/.cpp`
19. `Source/Drone/UI/DroneFlightHUDWidget.h/.cpp`
20. `Source/Drone/Prototype/DronePrototypeGameMode.h/.cpp`

이 순서는 `Gate 판정 규칙 → Overlap 입력 → 기록 데이터 → Lap Recorder → Course 연결 → 자동화 근거 → Pawn·Telemetry·HUD 실행 경로` 순으로 책임을 따라가게 한다.

## 8. Editor 수동 확인법과 정상 결과

### A. Play 전 Asset 연결 확인

1. UE 5.8.1로 프로젝트를 연다.
2. Content Browser에서 `/Game/Drone/Maps/Lvl_DroneTraining`을 연다.
3. World Outliner에서 `BP_DroneTrainingCourse` Class의 Course Actor를 선택한다.
4. Details에서 `CourseId`가 비어 있지 않은지 확인한다.
5. `OrderedGates` 배열 크기가 4인지 확인한다.
6. 배열의 각 Gate를 차례로 선택해 다음을 확인한다.
   - Course와 같은 `CourseId`
   - `GateIndex`가 `0, 1, 2, 3`
   - 같은 Gate를 중복 참조하지 않음
   - `SegmentDistance`가 0 이상임. 현재 저장값은 배치 메타데이터이며 TUT-03 실제 거리 계산값은 아님
7. 각 Gate Actor를 선택하고 Local Transform 표시로 로컬 빨간 X축 방향을 확인한다. 그 방향만 정방향이다.
8. Course Spline과 Gate 공간 순서가 대체로 같은 진행 방향인지 확인한다.

정상 결과:

- Course 1개와 Ring Gate 4개가 보인다.
- Gate 0은 밝은 녹색 Current, Gate 1~3은 어두운 Inactive로 보인다.
- Cyan Course 안내선이 계속 보인다.
- Map에 미리 배치된 Drone Pawn은 없고 PlayerStart에서 GameMode가 Spawn한다.

### B. 정상 순서 비행 확인

현재 검증된 Keyboard 입력은 다음과 같다.

| 입력 | 동작 |
|---|---|
| `W / S` | 전진 / 후진 |
| `A / D` | 좌 / 우 이동 |
| `Space / Left Ctrl` | 상승 / 하강 |
| `Q / E` | Actor Yaw 음 / 양 방향 |
| Mouse X | Actor Yaw |
| Mouse Y | Camera Pitch |

1. PIE 또는 Standalone을 시작한다.
2. 실제 WBP Flight HUD가 표시되는지 확인한다.
3. 녹색 Gate 0을 향해 접근한다.
4. Gate Actor 로컬 `+X` 방향으로 중앙 Trigger 영역을 완전히 통과한다.
5. Gate 0이 Cyan Completed, Gate 1이 녹색 Current로 바뀌는지 확인한다.
6. 같은 방식으로 Gate 1, 2, 3을 통과한다.

정상 결과:

- Ring Visual이나 Trigger가 Drone 이동을 물리적으로 막지 않는다.
- Gate 하나를 정상 통과할 때 진행이 정확히 한 칸만 바뀐다.
- 방금 통과한 Gate는 Cyan, 다음 Gate는 녹색이 된다.
- 마지막 Gate까지 통과하면 네 Gate가 모두 Cyan이 된다.
- Gate 0 승인 뒤 Lap Recorder는 `Recording`, 마지막 Gate 승인 뒤 `Completed`가 된다.
- 화면에는 아직 Lap Time, 완료 팝업, 비교·점수 화면이 나타나지 않는다. TUT-03은 계산·기록 계층까지이므로 이것이 정상이다.

### C. TUT-03 기록값과 Reset 확인

현재는 결과 Widget이 없으므로 값은 `BP_DroneTrainingCourse`의 native `LapRecorderComponent`가 공개하는 Getter와 Blueprint Event를 Editor Blueprint Debugger에서 확인한다. 수동 확인을 위해 `OnSegmentRecorded`와 `OnLapCompleted`를 임시 Print String 또는 Breakpoint에 연결했다면 테스트 뒤 저장·Commit하지 않는다. 정확한 계산식은 이미 `Drone.Tutorial.TrainingRecordCalculation`과 `Drone.Tutorial.TrainingLapRecorder` 자동화가 검증한다.

한 번의 4 Gate 정상 Lap에서 확인할 값은 다음과 같다.

1. Gate 0 통과 직후:
   - `GetRecordState = Recording`
   - `IsLapRecording = true`
   - `GetRecordedSegmentCount = 0`
   - 현재 Lap·Segment 시간은 이후 증가하기 시작함
   - 현재 Lap·Segment 이동 거리는 Gate 0 승인 위치에서 `0`으로 시작함
2. Gate 1 통과 직후:
   - `OnSegmentRecorded`가 한 번 발생함
   - Segment `0`, `FromGateIndex=0`, `ToGateIndex=1`
   - 시간과 실제 이동 거리가 0보다 크고 평균 속도가 유한한 값임
3. Gate 2 통과 직후:
   - Segment `1`, `FromGateIndex=1`, `ToGateIndex=2`
4. Gate 3 통과 직후:
   - Segment `2`, `FromGateIndex=2`, `ToGateIndex=3`
   - `OnLapCompleted`가 한 번 발생함
   - `GetRecordState = Completed`
   - `GetSuccessfulLapCount = 1`
   - `GetLastCompletedLap().bCompleted = true`
   - 완료 Lap의 Segment 배열 크기 `3`
   - Lap 시간·거리·평균 속도가 모두 유한하며, 실제로 이동했다면 0보다 큼
   - 세 Segment 시간의 합과 Lap 시간이 거의 같고, 세 Segment 거리의 합과 Lap 거리가 거의 같음

같은 PIE에서 Reset을 확인한다.

1. Course의 `GateSequenceComponent`에서 `ResetSequence()`를 호출한다.
2. Gate 0이 다시 밝은 녹색 `Current`, Gate 1~3이 `Inactive`인지 확인한다.
3. `GetRecordState = Idle`, `IsRecordingReady = true`, `IsLapRecording = false`인지 확인한다.
4. 진행 중 시간·거리와 미완료 Segment가 0으로 초기화됐는지 확인한다.
5. `GetSuccessfulLapCount = 1`과 마지막 완료 Lap 값은 그대로 유지되는지 확인한다.
6. Gate 0을 다시 통과하면 새 Lap이 `Recording`으로 시작되는지 확인한다.

Reset은 새 시도를 시작하는 기능이며 같은 Course 구성의 완료 기록을 삭제하지 않는다. Gate 배열이나 Course 구성을 다시 적용하는 Reconfigure는 비교 기준 자체가 달라지는 경우이므로 성공 History도 비운다.

### D. 실패 흐름 확인

1. 새 PIE를 시작해 Gate 0이 Current인 상태로 만든다.
2. Gate 1 또는 더 뒤의 Gate를 먼저 통과해 본다.
3. Gate 0의 녹색 Current가 유지되는지 확인한다.
4. Gate 0을 로컬 `+X` 반대 방향으로 통과해 본다.
5. Gate 0의 상태가 유지되는지 확인한다.
6. Gate 0을 정상 통과한 뒤 다시 Gate 0을 통과해 본다.
7. Gate 1이 Current인 상태가 그대로 유지되는지 확인한다.

정상 결과:

- 미래 Gate 통과는 진행하지 않는다.
- 역방향 통과는 진행하지 않는다.
- 완료 Gate 중복 통과는 진행하지 않는다.
- 거부된 통과는 `OnGateAccepted`를 발생시키지 않으므로 Lap 상태·Segment 수·누적 거리도 바꾸지 않는다.
- 현재는 실패 이유를 HUD Text로 표시하지 않는다. Visual 상태가 그대로인 것이 유일한 플레이 화면 피드백이다.

### E. Collision·Navigation 확인

1. Gate를 통과할 때 Ring 테두리나 중앙 Box에 걸려 멈추지 않는지 확인한다.
2. Editor에서 Gate의 `GateTrigger` Component를 선택한다.
3. Collision Enabled가 `Query Only`, Pawn Response가 `Overlap`인지 확인한다.
4. Ring의 Static Mesh Component는 `No Collision`인지 확인한다.
5. Navigation 표시를 사용하는 경우 Gate와 Course 안내선 때문에 NavMesh에 구멍이 생기지 않는지 확인한다.

정상 결과:

- Trigger는 Overlap Event만 만들고 Blocking Hit를 만들지 않는다.
- Ring Visual은 Hit·Overlap을 만들지 않는다.
- Gate와 Course 표시 구성요소는 Navigation에 영향을 주지 않는다.

### F. 이상이 있을 때 확인 순서

Gate 색이 전혀 바뀌지 않으면 다음 순서로 본다.

1. Course `OrderedGates`가 4개인지
2. GateIndex가 배열 위치와 같은지
3. CourseId가 모두 같은지
4. Gate를 로컬 `+X` 방향으로 통과했는지
5. Trigger 안에서 멈춘 것이 아니라 완전히 빠져나왔는지
6. 실제 Pawn Class가 `BP_DroneFPVIntegration`인지
7. `GateTrigger`가 QueryOnly·Pawn Overlap인지

Ring이 보이지 않으면 다음을 확인한다.

1. Gate의 Ring Segment Mesh가 설정되어 있는지
2. `M_DroneTrainingGuide`가 연결되어 있는지
3. Gate 상태 색의 밝기와 배경 대비
4. Ring 크기와 Camera 거리

Drone 조작이나 HUD가 나오지 않으면 다음을 확인한다.

1. 현재 Map이 `Lvl_DroneTraining`인지
2. Map WorldSettings가 `BP_DronePrototypeGameMode`인지
3. 실제 Controller와 Pawn이 BP Prototype Class인지
4. `IMC_DronePrototype`과 Input Action이 BP Pawn에 연결되어 있는지
5. BP Controller의 HUD Class가 `WBP_DroneFlightHUD`인지

Gate는 정상 완료되지만 기록이 만들어지지 않으면 다음을 확인한다.

1. Course에 native `LapRecorderComponent`가 존재하는지
2. Gate 0부터 같은 Drone으로 순서대로 통과했는지
3. Gate 사이에서 실제 World Game Time이 0보다 크게 흘렀는지
4. Prototype Drone의 `UDroneTelemetryComponent`가 정상 갱신 중인지
5. 중간에 `ResetSequence`, Course Reconfigure 또는 Pawn 파괴가 발생하지 않았는지
6. 4 Gate 완료 기록의 Segment 수가 `Gate 수 - 1`, 즉 3인지

수동 확인에서 문제가 없으면 TUT-03 사용자 확인 결과를 기록한다. 다음 카드는 현재 실행에 보존된 성공 기록을 이용해 이전 평균·Best·현재 대비 차이를 계산하고 Course HUD·Gate Toast·Lap 결과를 표시하는 `TUT-04 비교·결과 UI`다.
