# Drone Smart Object NPC 준비·사용 가이드

기준일: 2026-09-03 (Asia/Seoul)

이 문서는 적군 순찰과 드론 발견 대응, 소총·샷건 분기, 기지 아군 NPC의 생활·순찰 이동, 한 명만 사용하는 MG Turret을 같은 기반 위에 구성하기 위한 실전 가이드다.

현재 공유 기준선 `2d6a459`에는 **MG·체력·사망 교대·Cover·Drone 파괴 교전 종료·Rifle/Shotgun 탄창과 Smart Object 도착 방향 보강**까지 반영돼 있다. `ST_NPC_HostilePatrol`은 MGTurret을 먼저 시도하고 실패한 Hostile은 Cover 1-Slot으로 이동해 개인 무기로 대응한다. 사수가 사망하면 Cover 병사가 자기 Slot을 놓고 빈 MG를 재Claim할 수 있다. Cover도 없으면 제자리 개인 무기로 대응하며, 실종 Event 뒤에는 모든 Slot을 정리하고 3초 Search 후 순찰로 복귀한다. Drone이 파괴되면 Search 없이 즉시 전투 자원을 정리하고 Patrol로 돌아간다. 예비 탄약·재장전 시간·생활/전투 Animation·FX·SFX와 최종 사망 연출은 아직 완성된 기능이 아니다.

## 바로 찾는 수정 위치

Smart Object는 하나의 파일만 고치는 기능이 아니다. **장소**, **검색·예약 규칙**, **행동 순서**, **맵 배치**를 분리해 수정한다.

| 바꾸려는 내용 | 수정 위치 | 조정 방법 |
|---|---|---|
| 지점의 월드 위치·방향 | `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox` 또는 적용할 실제 맵 | 배치된 `BP_SO_*` Actor를 이동·회전한다. Cyan 화살표 `+X`가 NPC 도착 방향이다 |
| Mesh와 NPC 대기 위치 사이 Offset | `/Game/Drone/AI/SmartObjects/Blueprints/BP_SO_*` | Blueprint Viewport에서 상속된 `SmartObjectComponent`의 상대 Location·Rotation을 조정한다. `SlotFacingPreview`가 같이 움직인다 |
| Slot 수·Activity Tag·Behavior | `/Game/Drone/AI/SmartObjects/Definitions/SO_Def_*` | Definition Editor의 Slots에서 수정한다. 현재 프로젝트 계약은 역할별 Slot 1개·Activity Tag 1개다 |
| 역할·Definition·MG Mesh 연결 | `/Game/Drone/AI/SmartObjects/Blueprints/BP_SO_*` | Class Defaults의 `Activity`, Smart Object Definition, MG Mesh를 맞춘다 |
| MG 사거리·발사 간격·피해·총구 Offset | `BP_SO_MGTurret` Class Defaults | `Drone > AI > MG`의 Range, Cooldown, Damage, Muzzle Offset을 조정한다 |
| AI의 Smart Object 검색 범위 | `Source/Drone/AI/DroneSmartObjectReservationComponent.h` | `SearchRadius`, `SearchHalfHeight` 기본값을 수정한다. 역할별 차이가 필요하면 Controller Blueprint 분리를 먼저 한다 |
| 순찰 재선택 회피 거리 | `Source/Drone/AI/DroneNPCAIController.h` | `PatrolRepeatAvoidanceRadius`를 조정한다 |
| 도착 허용 반경·대기·재시도 시간 | `/Game/Drone/AI/StateTrees/ST_NPC_HostilePatrol`, `ST_NPC_FriendlyBaseRoutine` | 해당 Native Task 노드의 `AcceptanceRadius`, `WaitDuration`, `RetryInterval`을 조정한다 |
| MG/Cover 우선순위와 실패 분기 | `/Game/Drone/AI/StateTrees/ST_NPC_HostilePatrol` | State와 Transition을 조정한다. Native Task Struct 이름·순서는 검증 도구 계약과 같이 갱신한다 |
| 검색·Claim·Occupied·Release 코드 | `DroneSmartObjectReservationComponent.*`, `DroneNPCAIController.*` | 예약 Handle은 Component 한 곳에서만 소유한다. Blueprint에 별도 Claim 로직을 중복하지 않는다 |
| Station 구조·MG Trace | `DroneSmartObjectStation.*` | Station Component 구조와 MG Pivot·Trace·Damage 공용 규칙을 수정한다 |
| Definition/BP 생성·정합성 검사 | `md/tools/unreal/Setup-DroneSmartObjectStations.py` | 새 역할을 추가할 때 `SPECS`와 Tag Enum을 함께 갱신한다 |

### 에디터에서 지점 하나 조정하는 순서

1. 적용할 맵을 열고 World Outliner에서 `Station_*` 또는 배치한 `BP_SO_*`를 선택한다.
2. `W/E`로 Actor 전체 위치와 Yaw를 조정한다. Cyan 화살표가 NPC가 도착해 바라볼 방향이다.
3. 외형은 그대로 두고 NPC가 서는 위치만 옮겨야 하면 대응 `BP_SO_*`를 열고 `SmartObjectComponent` 상대 Transform을 조정한다.
4. `SlotFacingPreview`는 `SmartObjectComponent`의 자식이므로 실제 Slot Offset과 함께 움직이는지 Viewport에서 확인한다.
5. MG는 `MGTurretAimPivot`이 회전축, `StationMesh`가 외형, `SmartObjectComponent`가 병사가 서는 위치다. 세 Component의 역할을 섞지 않는다.
6. `P` 키로 NPC 시작 위치부터 Slot까지 녹색 NavMesh가 끊기지 않는지 확인한다.
7. PIE에서 NPC가 Slot에 도착한 뒤 Cyan 화살표 방향으로 회전하는지 확인한다. 이번 보완부터 순찰·아군 활동·Cover·MG 모두 예약 Slot Yaw를 적용한다.
8. 이동 실패 시 Actor를 지면 위로 조금 올리는 방식으로 숨기지 말고 NavMesh 경계, 장애물 Collision, Acceptance Radius를 순서대로 확인한다.

### 여러 지점 배치와 복제

1. Content Browser의 대응 `BP_SO_*`를 맵으로 끌어 놓는다.
2. 같은 역할은 `Alt+Drag`로 복제하고 Actor Label을 `Station_역할_번호` 형식으로 정리한다.
3. Patrol은 최소 2개, 권장은 3개 이상 배치한다. 한 개뿐이면 재선택 회피 뒤 같은 지점을 다시 사용한다.
4. MG와 Cover는 Slot 1개가 동시 사용자 1명을 뜻한다. 두 명을 받으려면 Station Actor를 두 개 배치하는 방식을 우선 사용한다.
5. 같은 Blueprint의 모든 배치에 공통 Offset이 필요하면 Blueprint의 `SmartObjectComponent`를 수정한다. 특정 한 곳만 다른 구조라면 Definition을 변형하기보다 프로젝트 소유 Child Blueprint를 만든다.
6. 배치 후 `Validate`를 실행하고, 행동 변경까지 했다면 관련 PIE 자동화와 화면 확인을 함께 수행한다.

### Definition 수정 시 주의

- `Activity` Enum은 사람용 표시이고 실제 검색 기준은 Definition Slot의 Activity Tag다. 둘을 반드시 같은 역할로 맞춘다.
- `Invoke-DroneSmartObjectSetup.ps1 -Mode Validate`는 읽기 중심 정합성 검사다.
- `-Mode Create`는 관리 대상 6개 Definition의 Slot 배열과 Blueprint 기본 연결을 다시 기록한다. 수동 Slot Offset·다중 Slot·Behavior를 넣은 뒤에는 의도적으로 재생성할 때만 사용한다.
- 현재 실행 Wrapper는 문서 저장소와 같은 상위 폴더의 `drone/Drone.uproject`를 기본 경로로 자동 계산한다. 다른 복제본을 검사할 때만 `-ProjectPath`를 명시한다.

```powershell
cd D:\JGY\project\md
powershell -ExecutionPolicy Bypass -File .\tools\unreal\Invoke-DroneSmartObjectSetup.ps1 -Mode Validate
```

## 1. 이번 구조로 만들 동작

### 적 NPC

```text
Enemy Patrol Smart Object 검색·예약
→ NavMesh를 따라 이동
→ 지점에서 경계·대기
→ 예약 해제 후 다음 지점 탐색
→ 드론 발견
→ 현재 순찰 예약 해제
→ MG 사용 가능 여부 확인
   ├─ 빈 MG 있음: MG 예약 → 이동 → 점유 → 사격
   └─ 빈 MG 없음: 장비에 따라 Rifle 또는 Shotgun 사격
→ 드론을 놓침
→ 수색
→ 순찰 복귀
```

### 기지 아군 NPC

```text
Friendly Base Patrol 또는 Ambient Smart Object 검색·예약
→ NavMesh를 따라 이동
→ 대기·관찰·생활 Animation
→ 예약 해제
→ 다음 지점 탐색
```

`Friendly`는 프로젝트 내부 역할 구분 이름이다. 국가·군·세계관 설정을 확정하지 않는다. 아군 NPC는 현재 계획상 드론 감지를 전투 전환 조건으로 사용하지 않는다.

## 2. Spawn과 Smart Object를 분리하는 이유

Smart Object는 NPC를 생성하는 장치가 아니다.

- `ADroneNPCSpawnPoint`: 어느 NPC를 몇 명, 어느 간격으로 생성할지 담당한다.
- `ADroneNPCCharacter`: 외형·Animation Blueprint가 올라가는 프로젝트 소유 Character다.
- `ADroneNPCAIController`: StateTree, AI Perception, Smart Object 예약을 관리한다.
- `ADroneSmartObjectStation`: 순찰·대기·엄폐·MG처럼 NPC가 사용할 장소를 맵에 표시한다.
- `Smart Object Definition`: 실제 Slot 위치, Activity Tag, 사용 Behavior를 정의한다.

이렇게 나누면 NPC 수를 바꿔도 순찰 경로를 다시 만들 필요가 없고, 한 장소를 여러 AI가 동시에 사용하지 못하도록 예약 상태를 일관되게 관리할 수 있다.

```text
맵에 직접 배치 또는 ADroneNPCSpawnPoint
                  │
                  ▼
        ADroneNPCCharacter
          ├─ NPC Profile
          └─ Smart Object User
                  │ Possess
                  ▼
       ADroneNPCAIController
          ├─ StateTree
          ├─ AI Perception Sight
          └─ Reservation Component
                  │ Search / Claim / Release
                  ▼
 ADroneSmartObjectStation + Smart Object Definition
```

## 3. 현재 추가된 C++ 기반

### 역할과 무기

`FDroneNPCProfile`이 아래 값을 소유한다.

- Faction: `Neutral`, `Friendly`, `Hostile`
- Weapon Type: `Unarmed`, `Rifle`, `Shotgun`
- `bCanUseMGTurret`: 적 NPC가 드론 발견 뒤 MG 후보를 검색할 수 있는지

`UDroneNPCWeaponComponent`가 Rifle·Shotgun 공통 `CanFire/StartFire/StopFire/Reload`와 Target Actor·Aim Point를 관리한다. Controller의 `UsesRifle()`과 `UsesShotgun()`은 분류 API로 남기되, AI 발사 요청은 같은 경로를 사용한다. Rifle은 4,000cm·0.25초·발당 10 Damage·30발 탄창, Shotgun은 1,600cm·0.9초·8 Pellet·6도 반각·적중 Pellet당 8 Damage·8발 탄창을 Greybox 기본값으로 사용한다. Volley 한 번은 Pellet 수와 무관하게 Shell 한 발만 소모한다. 예비 탄약·재장전 시간과 최종 밸런스는 아직 미정이다.

### Smart Object Activity

다음 Native Gameplay Tag를 공통 계약으로 사용한다.

| 목적 | Activity Tag |
|---|---|
| 적 순찰 | `Drone.SmartObject.Activity.EnemyPatrol` |
| 기지 아군 순찰 | `Drone.SmartObject.Activity.FriendlyBasePatrol` |
| 생활·대기 | `Drone.SmartObject.Activity.Ambient` |
| 경계 | `Drone.SmartObject.Activity.Guard` |
| 엄폐 | `Drone.SmartObject.Activity.Cover` |
| MG | `Drone.SmartObject.Activity.MGTurret` |

NPC Profile은 아래 User Tag를 자동으로 만든다.

- `Drone.AI.Faction.Friendly`
- `Drone.AI.Faction.Hostile`
- `Drone.AI.Weapon.Rifle`
- `Drone.AI.Weapon.Shotgun`
- `Drone.AI.Role.MGTurretOperator`

드론 감지 이벤트는 다음 두 Tag로 StateTree에 전달한다.

- `Drone.AI.Event.DroneDetected`
- `Drone.AI.Event.DroneLost`

`RequiredActivityTags`가 비어 있으면 예약 검색이 실패하도록 만들었다. 필터가 준비되지 않은 아군이 적 순찰이나 MG를 우연히 점유하는 문제를 막기 위한 안전장치다.

### 드론 감지

`ADronePrototypePawn`에는 Sight용 `UAIPerceptionStimuliSourceComponent`가 붙어 있고 BeginPlay에 자신을 감지 대상으로 등록한다. `ADroneNPCAIController`는 현재 Prototype 단계에서만 다음 Sight 값을 쓴다.

- Sight Radius: 4000 cm
- Lose Sight Radius: 4500 cm
- Peripheral Vision: 70°
- Max Age: 3초

이 값은 최종 난이도 수치가 아니다. Greybox 감지 시험용이며 맵 규모와 플레이 감각을 확인한 뒤 조정한다.

Hostile Controller가 `ADronePrototypePawn`을 처음 감지하면 현재 Smart Object 예약을 해제하고 `DroneDetected` 이벤트를 보낸다. 시야를 잃으면 `DroneLost` 이벤트를 보낸다. Friendly와 Neutral은 같은 감지 결과로 전투 StateTree에 진입하지 않는다.

## 4. Content 폴더 권장 구조

기존 `/Game/Drone` 프로젝트 소유 경계 안에 다음 폴더를 만든다. 공급사 원본은 `/Game/Drone/ThirdParty`에 그대로 두고, 실제 게임용 Blueprint는 프로젝트 폴더에서 상속·조합한다.

```text
/Game/Drone/AI/
├─ Blueprints/
│  ├─ BP_NPC_Hostile_Rifle
│  ├─ BP_NPC_Hostile_Shotgun
│  ├─ BP_NPC_Friendly_Base
│  └─ BP_NPCSpawnPoint
├─ SmartObjects/
│  ├─ Definitions/
│  │  ├─ SO_Def_EnemyPatrol
│  │  ├─ SO_Def_FriendlyBasePatrol
│  │  ├─ SO_Def_Ambient
│  │  ├─ SO_Def_Guard
│  │  ├─ SO_Def_Cover
│  │  └─ SO_Def_MGTurret
│  └─ Blueprints/
│     ├─ BP_SO_EnemyPatrol
│     ├─ BP_SO_FriendlyBasePatrol
│     ├─ BP_SO_Ambient
│     ├─ BP_SO_Guard
│     ├─ BP_SO_Cover
│     └─ BP_SO_MGTurret
├─ StateTrees/
│  ├─ ST_NPC_HostilePatrol
│  ├─ ST_NPC_FriendlyBaseRoutine
│  └─ ST_Interaction_MGTurret
└─ Weapons/
   ├─ Rifle/
   └─ Shotgun/
```

외형 후보는 다음 ThirdParty 자산을 프로젝트 Blueprint의 Mesh에 연결하기 전에 Skeleton·Animation 호환성을 확인한다.

- Modular Soldier: 적 또는 아군 외형 후보
- Modular Insurgents: 적 또는 아군 외형 후보
- MG Turret Mesh: `/Game/Drone/ThirdParty/GroundDroneKit/Meshes/Alt_Turrets/MG_Turret/MG_Turret_SK`

`AI-VIS-01A` 읽기 전용 감사 결과 Modular Soldier와 Insurgent Skeleton은 현재 Manny Skeleton과 직접 일치하지 않으며, 이식된 두 Root의 Animation Asset은 각각 0개다. 특정 외형을 적·아군으로 확정하지 않았고 Retarget·T Pose·손 위치 검증 전에는 역할 BP에 강제 적용하지 않는다.

현재 프로젝트에는 Manny Skeleton용 Rifle Animation 38개와 FPS Weapon Mesh 70개가 있다. `MM_Rifle_Fire`, `MM_Rifle_Reload`, AR4 Rifle 후보는 정상 로드된다. 이름으로 식별되는 Shotgun Weapon Mesh는 0개이므로 Rifle Mesh를 Shotgun으로 속여 적용하지 않고 실제 후보가 정해질 때까지 기능 전용 Greybox로 유지한다.

## 5. 생성된 Smart Object 지점 확인·사용하기

### 왜 필요한가

순찰점과 생활 지점을 단순 TargetPoint로 만들면 점유 경쟁과 해제 규칙을 별도로 작성해야 한다. Smart Object Slot은 한 NPC가 Claim한 지점을 다른 NPC가 동시에 쓰지 못하게 한다.

### 담당 클래스

- C++ Host: `ADroneSmartObjectStation`
- Editor Asset: Smart Object Definition
- Runtime 예약: `UDroneSmartObjectReservationComponent`

### 현재 생성 결과

`AI-SO-01`에서 다음 12개 Asset을 실제로 생성했다.

| 역할 | Definition | Station Blueprint |
|---|---|---|
| 적 순찰 | `SO_Def_EnemyPatrol` | `BP_SO_EnemyPatrol` |
| 기지 아군 순찰 | `SO_Def_FriendlyBasePatrol` | `BP_SO_FriendlyBasePatrol` |
| 생활·대기 | `SO_Def_Ambient` | `BP_SO_Ambient` |
| 경계 | `SO_Def_Guard` | `BP_SO_Guard` |
| 엄폐 | `SO_Def_Cover` | `BP_SO_Cover` |
| MG | `SO_Def_MGTurret` | `BP_SO_MGTurret` |

- Definition 경로: `/Game/Drone/AI/SmartObjects/Definitions`
- Blueprint 경로: `/Game/Drone/AI/SmartObjects/Blueprints`
- 각 Definition은 정확히 Slot 1개와 해당 Activity Tag 1개를 가진다.
- 각 Slot에는 `Gameplay Interaction Smart Object Behavior Definition`이 1개 들어 있다.
- Definition의 Gameplay Interaction StateTree는 아직 의도적으로 비어 있다. 기본 이동은 Controller가 실행하는 역할별 StateTree와 Reservation Component가 담당하며, Slot 자체 Interaction은 생활 Animation·MG 점유 카드에서 필요할 때 별도로 연결한다.
- 여섯 Blueprint는 모두 `ADroneSmartObjectStation` 자식이며, 대응 Definition과 `Activity`가 연결됐다.
- `BP_SO_MGTurret`에만 Ground Drone Kit의 `MG_Turret_SK` 후보 Mesh를 연결했다.

Station만 맵에 배치한다고 NPC가 자동 생성되지는 않는다. 역할 Profile을 가진 NPC와 NavMesh가 함께 있으면 현재 Controller StateTree가 검색·Claim·이동·대기·해제를 실행한다.

### Editor 확인·배치 절차

1. `Drone.uproject`의 Plugin 변경을 반영하도록 Editor를 완전히 종료하고 다시 연다.
2. Plugins에서 `Smart Objects`와 `Gameplay Interactions`가 켜졌는지 확인한다.
3. Content Browser에서 위 Definition과 Station Blueprint 6쌍이 보이는지 확인한다.
4. Definition 하나를 열어 Slot 1개, 정확한 Activity Tag와 Gameplay Interaction Behavior가 있는지 확인한다.
5. Station Blueprint의 Class Defaults에서 `Activity`와 Smart Object Definition이 같은 역할인지 확인한다.
6. 시험 맵에 필요한 Station Blueprint를 끌어 놓는다.
7. 화살표가 NPC가 바라볼 방향이 되도록 맵에서 회전한다.
8. `P` 키로 NavMesh가 NPC 위치부터 각 Slot까지 이어지는지 확인한다.
9. MG Blueprint만 Turret Mesh가 보이고 일반 순찰·생활 지점은 Mesh 없이 화살표 Preview만 보이는지 확인한다.
10. StateTree 구현 뒤 Slot Behavior의 비어 있는 StateTree를 해당 Interaction StateTree로 연결한다.

`Activity` enum은 사람이 Blueprint 역할을 확인하기 위한 값이고, 실제 검색 기준은 Definition Slot의 Activity Tag다. 둘이 다르면 검색 결과가 잘못되므로 반드시 같이 맞춘다.

### 현재 단계의 정상 결과

- Smart Object 디버그 화면에서 Slot이 보인다.
- Definition과 Blueprint의 역할·Tag·참조가 일치한다.
- `BP_SO_MGTurret`만 후보 Mesh를 가진다.
- Hostile EnemyPatrol은 `AI-PATROL-01`, FriendlyBasePatrol/Ambient는 `AI-FRIEND-01` PIE로 Claim·이동·해제를 판정했다. MG·Cover Activity는 각 후속 카드에서 따로 판정한다.

### 문제 확인

- 검색 실패: Definition의 Activity Tag와 Controller의 Required Activity Tag 비교
- 아군이 적 지점 사용: Friendly Definition에 EnemyPatrol/MGTurret Tag가 섞였는지 확인
- Slot이 계속 잠김: StateTree 완료·실패·중단 경로 모두에서 `ReleaseReservation()` 호출 확인
- 이동 실패: NavMesh가 Slot까지 연결되는지 `P` 키로 확인
- Definition은 있는데 동작 없음: StateTree 또는 Gameplay Interaction Behavior가 연결됐는지 확인

Gameplay Interaction Task가 Claim Handle의 Occupied/Free 수명주기를 맡는 경우 `MarkReservationOccupied()`를 별도로 중복 호출하지 않는다. 직접 만든 이동·대기 Task에서만 수동 Occupied 전환을 사용한다.

## 6. NPC Blueprint 만들기

### 왜 필요한가

C++ Character에는 공통 수명주기만 두고 외형, Animation Blueprint, 충돌 크기, 역할 Profile은 Blueprint 자식별로 바꾼다.

### 담당 클래스

- C++ Character: `ADroneNPCCharacter`
- C++ Controller: `ADroneNPCAIController`
- 역할 Component: `UDroneNPCProfileComponent`

### Blueprint 절차

1. `ADroneNPCCharacter` 자식 `BP_NPC_Hostile_Rifle`을 만든다.
2. NPC Profile에서 `Faction=Hostile`, `Weapon Type=Rifle`을 설정한다.
3. MG도 사용할 병사만 `Can Use MG Turret`을 켠다.
4. `BP_NPC_Hostile_Shotgun`을 만들고 `Faction=Hostile`, `Weapon Type=Shotgun`으로 설정한다.
5. `BP_NPC_Friendly_Base`를 만들고 `Faction=Friendly`, `Weapon Type=Unarmed`, `Can Use MG Turret=false`로 설정한다.
6. 각 Blueprint의 Mesh와 Animation Blueprint는 후보 Asset을 실제로 열어 Skeleton 호환성을 확인한 뒤 연결한다.
7. Capsule이 발바닥과 캐릭터 체형에 맞는지 Viewport에서 조정한다.
8. 첫 시험은 맵에 NPC Blueprint를 한 명씩 직접 배치한다.
9. 반복 배치가 필요할 때만 `ADroneNPCSpawnPoint` 자식 Blueprint를 사용한다.

Spawn Point의 `Spawn On Begin Play` 기본값은 꺼져 있다. 실수로 PIE마다 NPC가 중복 생성되는 것을 막기 위한 값이다. 자동 생성을 사용할 때 NPC Class, Profile, Count, Spacing을 설정하고 그때만 켠다.

### 현재 생성 결과

| Asset | 설정 | Greybox 배치 |
|---|---|---:|
| `BP_NPC_Hostile_Rifle` | Hostile / Rifle / MG 사용 가능 | 1명 |
| `BP_NPC_Hostile_Shotgun` | Hostile / Shotgun / MG 사용 불가 | 1명 |
| `BP_NPC_Friendly_Base` | Friendly / Unarmed / MG 사용 불가 | 2명 |
| `BP_NPCSpawnPoint` | `ADroneNPCSpawnPoint` Blueprint 자식 | 필요할 때 사용 |

경로는 `/Game/Drone/AI/Blueprints`다. 현재 Mesh와 Animation은 Manny Simple·`ABP_Unarmed` 임시 Greybox이므로 최종 외형이 아니다. Soldier/Insurgent 후보 중 실제 역할별 외형 선택은 `AI-VIS-01B`에서 Retarget과 화면을 확인한 뒤 결정한다.

Controller의 엔진 자동 시작은 꺼져 있고 C++가 Profile에 맞는 Asset을 명시적으로 선택한다. Smart Object Runtime이 준비된 World BeginPlay 뒤 Hostile은 `ST_NPC_HostilePatrol`, Friendly는 `ST_NPC_FriendlyBaseRoutine`을 시작한다.

### 정상 결과

- 배치 또는 Spawn된 Character가 `ADroneNPCAIController`에 Possess된다.
- Hostile Rifle과 Shotgun은 서로 다른 Weapon Type을 가진다.
- Friendly는 FriendlyBasePatrol/Ambient만 기본 검색한다.
- Hostile은 EnemyPatrol/Guard만 기본 검색한다.

### 문제 확인

- Controller가 없음: `Auto Possess AI=Placed in World or Spawned`와 AI Controller Class 확인
- Profile이 전부 기본값: Character Blueprint와 Spawn Point Profile 중 실제 생성 경로를 확인
- 이동하지 않음: StateTree Asset 연결과 NavMesh 확인
- 외형만 T Pose: Skeleton·Animation Blueprint 호환성 확인

## 7. NavMesh와 Greybox 배치

1. 시험용 맵에 `NavMeshBoundsVolume`을 놓고 NPC 활동 영역을 전부 덮는다.
2. `P` 키로 녹색 이동 가능 영역을 확인한다.
3. Hostile Rifle 1명, Hostile Shotgun 1명, Friendly 2명을 직접 배치한다.
4. EnemyPatrol 지점 3개를 적 구역에 배치한다.
5. FriendlyBasePatrol 지점 3개와 Ambient 지점 2개를 기지 내부에 배치한다.
6. MG 지점 1개를 적 경계 구역에 배치한다.
7. 드론의 비행 경로가 적 Sight 범위에 들어오면서도 시작 즉시 보이지 않게 지형이나 벽으로 가린다.

처음부터 여러 맵에 퍼뜨리지 않는다. 전용 Greybox 시험 맵 한 곳에서 점유·이동·감지를 통과한 뒤 Battlefield 또는 Military Base 후보 맵에 적용한다.

### 현재 Greybox 맵

전용 맵은 `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`다.

- Hostile Rifle 1명, Hostile Shotgun 1명, Friendly Base 2명
- EnemyPatrol 3개, Guard 1개, MGTurret 1개
- FriendlyBasePatrol 3개, Ambient 2개
- PlayerStart, NavMeshBoundsVolume, 조명·Sky, 시각용 바닥
- NavMesh에 실제로 기여하는 `ADroneNPCNavigationFloor`

`ADroneNPCNavigationFloor`는 `BlockAll` 충돌과 Navigation Relevant 설정을 가진 전용 C++ 바닥이다. 시각용 Plane만으로는 NavMesh가 생기지 않는 경우를 피한다. 현재 MVP 맵은 Recast Runtime Generation을 `Dynamic`, `Force Rebuild On Load`를 활성화해 자동 검증한다. 넓은 최종 맵에 적용할 때는 성능 범위를 다시 측정하고 프로젝트 전역 설정 유지 여부를 결정한다.

## 8. StateTree 구성 순서

### 현재 적 순찰 StateTree `ST_NPC_HostilePatrol`

`AI-PATROL-01`에서 실제로 저장한 첫 버전은 다음 네 상태만 가진다.

```text
HostilePatrol
├─ ClaimEnemyPatrolSlot
├─ MoveToPatrolSlot
├─ WaitAtPatrolSlot
└─ ReleasePatrolSlot
    └─ ClaimEnemyPatrolSlot로 반복
```

- Claim 실패 시 0.5초 간격으로 다시 찾는다.
- 직전에 완료한 지점 반경 250 cm를 우선 피하되 다른 빈 지점이 없으면 일반 검색으로 돌아간다.
- Move는 Pathfinding과 NavMesh Projection을 사용하며 기본 수용 반경은 80 cm다.
- 도착 후 기본 1초 대기하고 방문 횟수·서로 다른 방문 위치를 Controller에 기록한 뒤 Slot을 해제한다.
- Hostile만 Tree를 실행하고 EnemyPatrol Activity만 Claim한다.
- 드론이 감지되면 이동을 멈추고 예약을 해제한 뒤 Claim 단계에서 대기한다. 이 안전 중단은 Search·공격 구현 완료를 뜻하지 않는다.

### 현재 감지·MG 확장 StateTree

`AI-PER-01`부터 `AI-MG-01`까지 진행한 현재 구조는 다음과 같다.

```text
Root
├─ Patrol
│  ├─ FindAndClaimEnemyPatrol
│  ├─ MoveToSlot
│  ├─ WaitOrGuard
│  └─ ReleaseSlot
├─ DroneDetected
│  ├─ ClaimMGTurretSlot
│  ├─ MoveToMGTurret
│  ├─ HoldMGTurretReservation
│  └─ PersonalWeapon Fallback
├─ Search
└─ ReturnToPatrol
```

- `Drone.AI.Event.DroneDetected`가 오면 Patrol에서 DroneDetected로 전환한다.
- `PrepareMGTurretSearch()`가 false면 바로 PersonalWeapon으로 간다.
- MG 검색에 실패해도 PersonalWeapon으로 내려가야 한다.
- Rifle과 Shotgun은 같은 Weapon Component의 Target·Aim Point 계약을 사용한다.
- `Drone.AI.Event.DroneLost`가 오면 Search로 이동하고, 정해진 시간 또는 탐색 완료 뒤 ReturnToPatrol로 간다.
- 상태가 성공·실패·중단되는 모든 경로에서 예약을 해제한다.
- 저장된 이름은 `HoldMGTurretReservation`이지만 Native Task는 현재 Claim을 Occupied로 전환하고 MG 사용·조준·Trace를 실행한다. 기존 Struct 경로와 StateTree 에셋 호환성을 지키기 위해 이름을 즉시 바꾸지 않았다.

### 현재 아군 StateTree `ST_NPC_FriendlyBaseRoutine`

```text
FriendlyBaseRoutine
├─ ClaimFriendlyActivitySlot
├─ MoveToFriendlyActivitySlot
├─ WaitAtFriendlyActivitySlot
└─ ReleaseFriendlyActivitySlot
    └─ ClaimFriendlyActivitySlot로 반복
```

Friendly는 `FriendlyBasePatrol`과 `Ambient`를 번갈아 먼저 시도하며, 선호 종류의 빈 Slot이 없으면 다른 아군 활동을 시도한다. 직전 완료 지점 반경 250 cm를 우선 피하고, Smart Object의 원자적 1-Slot Claim으로 다른 NPC가 이미 잡은 지점을 제외한다. 이동과 대기 Task는 Hostile과 공유하지만 Claim·완료 기록·Release Task는 역할별로 분리했다. Friendly에는 전투 분기를 넣지 않았으며 대화·작업·경례 같은 행동은 Animation 자산을 확인한 뒤 추가한다.

## 9. 소총과 샷건 구현 경계

현재 공용 Weapon 계약, Rifle·Shotgun Greybox Trace, Drone 체력 Damage, 탄창·즉시 Reload와 Blueprint 표현 Event까지 구현됐다. 다음 항목은 아직 구현되지 않았다.

- 예비 탄약·재장전 시간과 최종 사거리·명중률·난이도 수치
- Aim Offset, 발사 Montage, Motion Warping
- Muzzle Flash, 탄흔, 소리
- 아군 오사 방지와 팀 판정

Blueprint에서는 `NPCWeaponComponent`의 다음 Event에 표현만 연결한다.

- `OnWeaponFired`: `WeaponType`, `TraceStart`, `AimPoint`를 받는다. Rifle은 한 발마다 1회, Shotgun은 Pellet마다가 아니라 Volley마다 1회다.
- `OnReloadCompleted`: `WeaponType`, `CurrentAmmo`, `MagazineCapacity`를 받는다. 실제 Reload 성공 때만 1회다.

Animation Blueprint/Montage, Niagara와 Sound가 없어도 Trace·Damage는 이미 C++에서 작동한다. Event Graph에서 Line Trace, Damage, 탄약 감소를 다시 작성하면 이중 피해와 이중 소모가 생기므로 넣지 않는다.

권장 구현 순서는 다음과 같다.

1. 무기 공용 인터페이스: `CanFire`, `StartFire`, `StopFire`, `Reload`
2. AI가 보는 단일 Target Actor와 Aim Point 계약
3. Rifle: 단일 Trace 한 발과 Cooldown
4. Shotgun: 같은 Trigger에서 여러 Pellet Trace와 Spread
5. 표적이 드론인지, 사거리 안인지, 시야가 막히지 않았는지 검사
6. Damage와 체력 0 정지 처리 — 현재 Greybox 완료
7. Rifle 30발·Shotgun 8발 탄창과 즉시 Reload — 현재 Greybox 완료
8. `OnWeaponFired`·`OnReloadCompleted`에 Animation·FX·SFX 연결 — Event 경계 완료, 실제 표현은 후속
9. Data Asset으로 수치 분리

소총과 샷건의 최종 사거리·연사 속도·Pellet 수·Spread는 현재 미정이다. Greybox 테스트에서 임시값을 기록하고 플레이 결과로 조정한다.

## 10. MG 한 명 점유 규칙

MVP에서는 MG Smart Object Definition에 Slot을 하나만 둔다.

```text
Hostile + CanUseMGTurret
→ MGTurret Activity 검색
→ Claim 성공한 한 명만 이동
→ Slot 도착
→ Occupied
→ 조준·사격
→ DroneLost / Death / Abort / UnPossess
→ Free
```

현재 Reservation Component는 도착한 Claim을 `Occupied`로 전환한다. Station의 `MGTurretAimPivot`은 표적을 바라보고, 6,000cm·0.15초·발당 8 Damage의 Greybox Visibility Trace를 수행한다. DroneLost·Task 실패·UnPossess·EndPlay·사용자 사망에서는 Station 사용자와 Slot을 정리한다. 사망 해제 직후 감지 중인 다른 MG 가능 Hostile에 Event를 보내 재Claim시키는 흐름까지 PIE에서 검증했다.

Cover 분기는 `ClaimCoverSlot → MoveToCover → UseCover` 세 상태다. `UseCover` 진입에서 Slot을 Occupied로 바꾸고 개인 Rifle/Shotgun Timer를 시작한다. DroneLost·이동 실패·사망·MG 재시도 전환에서는 Cover 예약을 해제한다. 현재는 위치 점유와 사격 계약까지이며 Crouch·Lean·벽 방향 판정은 Animation/고급 Cover 카드 범위다.

### 체력·사망 시스템 사용 가이드

왜 필요한가:

- Rifle·Shotgun·MG가 같은 체력 규칙을 사용하고, 무기 코드가 NPC/Drone의 사망 연출까지 결정하지 않게 분리한다.

담당 클래스:

- `UDroneHealthComponent`: 기본 100/100, Damage 감소, `OnHealthChanged`, `OnDeath`, 사망 뒤 Damage 무시
- `ADroneNPCCharacter`: 사망 시 CharacterMovement·충돌·AI 전투를 정지
- `ADronePrototypePawn`: 사망 시 Input Mapping·이동·충돌을 정지
- `UDroneFlightHUDWidget`: Possess Drone의 Health Event를 받아 우측 상단 내구도를 표시

Header/CPP 연결:

- 새 NPC나 Drone C++ Actor에는 `CreateDefaultSubobject<UDroneHealthComponent>`로 Component 하나만 소유한다.
- 외부 피해는 직접 체력을 빼지 말고 `UGameplayStatics::ApplyDamage(Target, Damage, Instigator, Causer, nullptr)`를 사용한다.
- 현재 기본 피해는 Rifle 10, Shotgun 적중 Pellet당 8, MG 8이며 각 Component의 Greybox 설정 함수나 Class Defaults에서 바꿀 수 있다.

Blueprint 설정:

- 기존 `BP_NPC_*`와 `BP_DronePrototypePawn`은 부모 C++에서 Health Component를 상속하므로 새 Component를 중복 추가하지 않는다.
- 피격 Flash·Sound는 Health Component의 `OnHealthChanged`, 사망 Montage·폭발·실패 UI는 `OnDeath` Event에 연결한다.
- 기존 Flight WBP는 C++가 체력 패널을 동적으로 붙이므로 Designer에 `HealthValueText`를 다시 만들 필요가 없다. 최종 외형을 WBP 전용으로 바꾸는 작업은 별도 UI 카드에서 한다.

Editor 테스트:

1. `Lvl_NPCSmartObjectGreybox`에서 PIE한다.
2. 적이 Drone을 맞히면 우측 상단 `기체 내구도`가 100에서 감소하는지 본다.
3. 체력 0에서 Drone 이동·입력이 정지하고 `파괴됨`이 표시되는지 본다.
4. MG 사용 NPC에 `Apply Damage` 100을 호출했을 때 사수가 멈추고 Slot이 다른 MG 가능 적에게 넘어가는지 본다.

정상 결과와 확인 항목:

- 사망 Event는 한 번만 발생하고 추가 Pellet/Trace는 체력을 더 낮추지 않는다.
- NPC는 맵에 남지만 이동·충돌·사격·StateTree·예약이 정지한다.
- Drone도 맵에 남지만 입력·이동·충돌이 정지한다.
- Drone은 `OnDroneDestroyed` Blueprint Event를 한 번 보내고, 감지 중이던 살아 있는 적은 개인 무기·MG·Cover를 정리한 뒤 Search 없이 순찰로 복귀한다.
- 체력이 줄지 않으면 Target에 Health Component가 하나만 있는지, 무기 Trace가 실제 Target을 맞혔는지 확인한다.
- MG 교대가 안 되면 두 번째 Hostile의 `bCanUseMGTurret`, MGTurret Activity User Tag, 빈 Slot 여부와 NavMesh를 확인한다.

## 11. 단계별 작업 카드

각 카드는 1~3시간 안에 끝내고 완료 조건을 직접 확인한다.

| 카드 | 작업 | 완료 조건 |
|---|---|---|
| `AI-SO-00` | Plugin·Tag·Profile·Reservation·Station C++ 기반 | Build와 기반 자동화 통과 |
| `AI-SO-01` | Smart Object Definition 6종과 Station BP 생성 | **Done** — 6쌍 생성, Slot·Activity·Definition·MG Mesh 자동 검증 통과 |
| `AI-NPC-01` | 적 Rifle·Shotgun·아군 BP와 시험 맵 배치 | **Done** — 4명 Profile·Possess·Activity Tag·NavMesh 투영 검증 |
| `AI-PATROL-01` | 적 순찰 StateTree | **Done** — Hostile 2명이 EnemyPatrol Claim·이동·대기·해제, 각 2회 이상·서로 다른 2지점 이상 방문 자동 검증 |
| `AI-FRIEND-01` | 아군 BaseRoutine StateTree | **Done** — 아군 2명이 FriendlyBasePatrol/Ambient를 배타 Claim하고, 각각 두 종류·서로 다른 2지점 이상 방문 |
| `AI-PER-01` | 드론 Sight·Event PIE 검증 | **Done** — Hostile만 감지 시 Claim·이동 중단, 실종 뒤 3초 Search와 순찰 복귀, Friendly 루틴 지속 자동 검증 및 사용자 수동 화면 Pass |
| `AI-WPN-01` | 공용 Weapon 계약 | **Done** — Weapon Component의 공용 호출, 단일 Target·Aim Point 경로, Lost·UnPossess 정리와 Unarmed 거부 자동 검증 |
| `AI-WPN-02` | Rifle Greybox 발사 | **Done** — 단일 Visibility Trace, 장애물·사거리·Cooldown과 공용 계약 회귀 검증 |
| `AI-WPN-03` | Shotgun Greybox 발사 | **Done** — 한 Trigger의 다중 Pellet, 결정적 Spread, 장애물·사거리·Cooldown 검증 |
| `AI-MG-01` | MG Claim·Move | **Done** — MG 운영자 1명만 1-Slot Claim·이동·도착 뒤 유지, Shotgun 개인 무기 Fallback |
| `AI-MG-02` | MG Occupy·Aim·Fire·Release | **Done** — Occupied·Aim·8 Damage Trace·중단/사망 해제·다른 AI 재점유 집중 PIE 통과, 로컬 미커밋 |
| `HP-01` | NPC·Drone Health·Death·HUD | **Done** — 기본 100/100, 사망 1회, 무기 Damage, Drone 정지·내구도 HUD 집중 테스트 통과, 로컬 미커밋 |
| `AI-COVER-01` | MG 실패 병사의 Cover 대응 | **Done** — Cover 1-Slot Claim·Move·Occupied 사격, Map Station 2개, 사망 뒤 Cover→MG 교대 집중 PIE 통과, 로컬 미커밋 |
| `AI-COMBAT-END-01` | Drone 파괴 교전 종료·실패 신호 | **Done** — Blueprint Event 1회, Perception 해제, 개인 무기·MG·Cover 정리, Search 없는 Patrol 복귀 집중 PIE 통과, 로컬 미커밋 |
| `AI-AMMO-01` | Rifle·Shotgun 탄창·재장전 | **Done** — Rifle 30/Shotgun 8, Trace·Volley당 1발, 빈 탄창 정지·거부, 즉시 Reload와 AI 재개 집중 테스트 통과, 로컬 미커밋 |
| `AI-VIS-01A` | 자산 호환성 감사·BP 표현 Event | **Done** — Manny Rifle Animation 38개, Weapon Mesh 70개, 이름 기반 Shotgun Mesh 0개와 서로 다른 NPC Skeleton을 기록. 발사/Reload Event 및 집중 테스트 3/3 통과 |
| `AI-VIS-01B` | 외형·Animation·FX·SFX 연결 | Manny 임시 Rifle과 MG 표현부터 연결해 T Pose·손 위치·Muzzle 기준 확인. Shotgun 실제 Mesh와 최종 역할 외형은 미정 |

`AI-SO-00 → AI-SO-01 → AI-NPC-01 → AI-PATROL-01 → AI-FRIEND-01 → AI-PER-01 → AI-WPN-01 → AI-WPN-02 → AI-WPN-03 → AI-MG-01 → AI-MG-02 → HP-01 → AI-COVER-01 → AI-COMBAT-END-01 → AI-AMMO-01 → AI-VIS-01A`는 코드·에셋과 해당 집중 자동화 기준 완료했다. AI 하위 기능의 다음 후보는 `AI-VIS-01B`지만, 프로젝트 전체 신규 기능 우선순위는 FLOW-01~03 완료 뒤 `FLOW-04~06` Front-end Mission 흐름이다.

### Asset 재검증 명령

다른 PC에서 Pull한 뒤 Asset의 저장된 연결을 다시 확인할 때 문서 저장소 루트에서 실행한다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\unreal\Invoke-DroneSmartObjectSetup.ps1 -Mode Validate -ProjectPath D:\JGY\project\drone\Drone.uproject
```

`VALIDATION_OK`가 출력되면 6쌍의 형식·부모 Class·Slot Tag·Definition·MG Mesh 연결이 일치한다. `Create` 모드는 정확한 12개 Asset을 재구성하는 유지보수용이며 일반 작업에서는 실행할 필요가 없다.

NPC 역할 Blueprint와 Greybox 맵까지 다시 확인할 때는 다음 명령을 사용한다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\unreal\Invoke-DroneNPCGreyboxSetup.ps1 -Mode Validate -ProjectPath D:\JGY\project\drone\Drone.uproject
```

이 검증은 역할 Profile, AI Controller Possess, 역할 Tag, NPC 4명과 Station 10개 배치, Navigation Floor, Recast 설정, NPC 시작 위치의 NavMesh 투영을 확인한다. `BuildNavigation` 모드는 생성 자산을 수리하거나 Navigation을 다시 저장해야 할 때만 사용한다.

Hostile 순찰 StateTree의 Schema·상태 순서·Native Task·컴파일 상태는 다음 읽기 전용 명령으로 확인한다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\unreal\Invoke-DroneHostilePatrolStateTreeSetup.ps1 -Mode Validate -ProjectPath D:\JGY\project\drone\Drone.uproject
```

`Create`는 Asset이 없을 때만 새로 만들며 기존 StateTree는 덮어쓰지 않는다. 일반 Pull·검증에서는 `Validate`만 사용한다.

Friendly 기지 루틴 StateTree도 같은 방식으로 읽기 전용 검증한다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\unreal\Invoke-DroneFriendlyBaseRoutineStateTreeSetup.ps1 -Mode Validate -ProjectPath D:\JGY\project\drone\Drone.uproject
```

이 검증은 `FriendlyBaseRoutine`의 Claim·Move·Wait·Release 상태 순서, Native Task 종류와 컴파일 준비 상태를 확인한다. `Create`는 Asset이 없을 때만 사용하며 기존 Asset을 덮어쓰지 않는다.

Hostile 감지·Search 전환까지 포함한 최종 StateTree는 다음 명령으로 확인한다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\unreal\Invoke-DroneHostilePerceptionStateTreeSetup.ps1 -Mode Validate -ProjectPath D:\JGY\project\drone\Drone.uproject
```

MG Claim·Move·Hold 분기까지 포함한 현재 최종 StateTree는 다음 명령으로 확인한다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\unreal\Invoke-DroneHostileMGTurretStateTreeSetup.ps1 -Mode Validate -ProjectPath D:\JGY\project\drone\Drone.uproject
```

일반 Pull 뒤에는 `Validate`만 사용한다. `Upgrade`는 정확한 기존 6-State 감지 Tree에 MG 세 상태를 추가하는 유지보수용이며, 이미 9-State로 업그레이드된 자산에는 변경을 만들지 않는다.

## 12. 첫 PIE 검증 체크리스트

- [x] Smart Objects와 Gameplay Interactions Plugin 활성 상태를 프로젝트 설정과 자동화로 확인
- [x] NPC 4명 시작 위치가 NavMesh에 투영되는지 자동화로 확인
- [x] Hostile Rifle 1명, Hostile Shotgun 1명, Friendly 2명 Possess 확인
- [x] 적 순찰 Tree가 EnemyPatrol만 사용
- [x] 아군이 FriendlyBasePatrol/Ambient만 사용하고 두 종류를 모두 방문
- [x] 같은 1-Slot은 Smart Object 배타 Claim 경로로 예약
- [x] 드론이 보이지 않을 때 Hostile 2명이 각각 2회 이상 순찰하고 서로 다른 2개 이상 지점 방문
- [x] 드론이 Sight Event에 들어오면 Hostile만 순찰 예약 해제
- [x] Friendly는 같은 드론 감지 자극에도 전투 상태로 바뀌지 않고 BaseRoutine 지속
- [x] MG 사용 가능 적만 MG를 검색하고 1-Slot을 Claim·이동
- [x] 도착한 MG를 Occupied로 전환하고 표적 조준·Cooldown Trace 수행
- [x] DroneLost 뒤 MG 사용자와 Occupied Slot 해제
- [x] 드론을 놓치면 마지막 감지 위치 Search를 거쳐 순찰 Claim 재개
- [x] Rifle과 Shotgun이 공용 Weapon 호출과 같은 Target·Aim Point 경로를 사용
- [x] 감지 실종과 UnPossess에서 발사 상태 정리, Friendly·Unarmed 비발사
- [ ] PIE 종료 뒤 남은 Claim이나 중복 Spawn 없음

## 13. 현재 완료와 미완료 판정

### 준비 완료

- Smart Objects와 Gameplay Interactions 모듈 연결
- Faction·Rifle·Shotgun·MG 사용 가능 Profile
- Activity와 AI Event Native Gameplay Tag
- NPC Character·AI Controller·Spawn Point·Smart Object Station 기반
- Activity Tag 기반 가장 가까운 빈 Slot 검색·Claim·Release 기반
- Drone Prototype의 AI Sight 감지 대상 등록
- Hostile 감지/실종 StateTree Event 전달 기반
- Friendly와 Hostile의 기본 Smart Object 검색 범위 분리
- Smart Object Definition·Station Blueprint 6쌍
- 역할별 NPC Blueprint 3종과 Spawn Point Blueprint
- `Lvl_NPCSmartObjectGreybox`의 NPC 4명·Station 12개(기존 10 + Cover 2)·Navigation Floor
- Profile·Possess·Activity Tag·NavMesh 투영 자동화
- Hostile `ST_NPC_HostilePatrol`과 Claim·Move·Wait·Release Native Task
- 직전 지점 우선 회피, 이동 실패·감지·UnPossess 시 예약 해제
- Hostile 2명의 반복 순찰과 Friendly 2명의 Base Patrol/Ambient 반복 이동 PIE 자동화
- Friendly `ST_NPC_FriendlyBaseRoutine`과 역할별 Claim·Release Native Task
- Hostile `DroneDetected`·`SearchLastKnownLocation` State와 감지·실종 Event 전환, Search 성공·실패의 순찰 복귀
- Hostile만 반응하고 Friendly 루틴은 지속되는 `Drone.AI.NPCPerceptionSearchPIE`
- `UDroneNPCWeaponComponent` 공용 호출과 Controller의 단일 Target Actor·Aim Point 전달 계약
- Rifle 단일 Trace와 Shotgun 다중 Pellet·Spread, 장애물·사거리·Cooldown Greybox
- Rifle·Shotgun 동일 경로, Friendly 비발사, Lost 정리를 검증하는 `Drone.AI.WeaponContract`와 NPC Greybox PIE
- MG Claim·Move·Hold Native StateTree Task, 개인 무기 Fallback과 DroneLost 예약 정리
- MG 운영자 1명·예약 1개·도착과 Friendly 비무장을 검증하는 NPC Greybox PIE
- Station Aim Pivot·Blueprint 사용/발사 Event와 MG Greybox Trace
- Game/Editor Build, AI 11/11, 전체 `Drone.` 27/27, Blueprint 0/0/0와 LFS 검증

### 아직 구현·수동 검증 필요

- 최종 NPC 외형·Skeleton·Animation Blueprint 선택과 연결
- Rifle·Shotgun 예비 탄약·재장전 시간·Animation·FX·SFX
- MG 승하차 Animation·FX·SFX와 최종 밸런스
- NPC 래그돌·시체 제거, Drone 폭발·Respawn·Mission 실패 화면
- Cover와 전투 종료 뒤 통합 Return 실제 행동
- 최종 맵에 NPC와 Smart Object 배치

UE 5.8.1에서 `Gameplay Interactions`는 Experimental 표기가 있는 Plugin이다. 프로젝트에 제한적으로 사용하되 엔진 업데이트 때 API 변경 가능성을 확인하고, 핵심 역할·예약 규칙은 프로젝트 C++와 테스트에 남긴다.
