# Drone Smart Object NPC 준비·사용 가이드

기준일: 2026-08-27 (Asia/Seoul)

이 문서는 적군 순찰과 드론 발견 대응, 소총·샷건 분기, 기지 아군 NPC의 생활·순찰 이동, 한 명만 사용하는 MG Turret을 같은 기반 위에 구성하기 위한 실전 가이드다.

현재 단계는 **C++ 기반, Smart Object Definition·Station Blueprint 6쌍, 역할별 NPC Blueprint, 전용 Greybox 맵을 준비한 상태**다. NPC 4명의 Profile·Possess·Activity Tag·NavMesh 투영까지 자동 검증했다. StateTree, 실제 순찰·아군 이동, 무기 사격·피해·Animation은 아직 완성된 기능이 아니다. 아래 순서대로 작은 동작 단위로 만들고 PIE에서 확인한 뒤 다음 카드로 넘어간다.

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

소총·샷건 분기는 준비됐지만 실제 발사 로직은 아직 없다. Controller의 `UsesRifle()`과 `UsesShotgun()`을 StateTree 전환 조건이나 Blueprint 조건으로 사용할 수 있다.

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
│  ├─ ST_NPC_Hostile
│  ├─ ST_NPC_Friendly
│  └─ ST_Interaction_MGTurret
└─ Weapons/
   ├─ Rifle/
   └─ Shotgun/
```

외형 후보는 다음 ThirdParty 자산을 열어 Skeleton·Animation 호환성을 직접 확인한 뒤 프로젝트 Blueprint의 Mesh에 연결한다.

- Modular Soldier: 적 또는 아군 외형 후보
- Modular Insurgents: 적 또는 아군 외형 후보
- MG Turret Mesh: `/Game/Drone/ThirdParty/GroundDroneKit/Meshes/Alt_Turrets/MG_Turret/MG_Turret_SK`

외형 후보만 이식된 상태이므로 특정 외형을 적·아군으로 확정하지 않는다. Animation Blueprint와 무기 손 위치도 아직 검증 전이다.

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
- Interaction StateTree는 의도적으로 비어 있다. `AI-PATROL-01`·`AI-FRIEND-01`에서 행동을 만든 뒤 연결한다.
- 여섯 Blueprint는 모두 `ADroneSmartObjectStation` 자식이며, 대응 Definition과 `Activity`가 연결됐다.
- `BP_SO_MGTurret`에만 Ground Drone Kit의 `MG_Turret_SK` 후보 Mesh를 연결했다.

따라서 현재 Asset은 검색·Claim 계약을 검사할 수 있지만, 맵에 배치하는 것만으로 NPC가 이동·대기하지는 않는다. 실제 이동 실행은 후속 StateTree Task가 담당한다.

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
- 실제 Claim·이동·해제는 `AI-PATROL-01` 이후 PIE에서 판정한다.

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

경로는 `/Game/Drone/AI/Blueprints`다. 현재 Mesh와 Animation은 Manny Simple·`ABP_Unarmed` 임시 Greybox이므로 최종 외형이 아니다. Soldier/Insurgent 후보 중 실제 역할별 외형 선택은 `AI-VIS-01`에서 자산을 직접 확인한 뒤 결정한다.

StateTree Asset이 비어 있는 동안 Controller의 자동 StateTree 시작은 꺼져 있다. StateTree Event도 StateTree가 실행 중일 때만 전달하므로, 현재 단계에서 빈 Asset 때문에 PIE 오류가 반복되지 않는다.

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

### 적 StateTree `ST_NPC_Hostile`

첫 버전의 상태는 다음 정도로 제한한다.

```text
Root
├─ Patrol
│  ├─ FindAndClaimEnemyPatrol
│  ├─ MoveToSlot
│  ├─ WaitOrGuard
│  └─ ReleaseSlot
├─ DroneDetected
│  ├─ TryMGTurret
│  │  ├─ FindAndClaimMG
│  │  ├─ MoveToMG
│  │  └─ UseMG
│  └─ PersonalWeapon
│     ├─ RifleFire
│     └─ ShotgunFire
├─ Search
└─ ReturnToPatrol
```

- `Drone.AI.Event.DroneDetected`가 오면 Patrol에서 DroneDetected로 전환한다.
- `PrepareMGTurretSearch()`가 false면 바로 PersonalWeapon으로 간다.
- MG 검색에 실패해도 PersonalWeapon으로 내려가야 한다.
- `UsesRifle()`과 `UsesShotgun()`으로 사격 Task를 분기한다.
- `Drone.AI.Event.DroneLost`가 오면 Search로 이동하고, 정해진 시간 또는 탐색 완료 뒤 ReturnToPatrol로 간다.
- 상태가 성공·실패·중단되는 모든 경로에서 예약을 해제한다.

### 아군 StateTree `ST_NPC_Friendly`

```text
Root
└─ BaseRoutine
   ├─ FindAndClaimFriendlyActivity
   ├─ MoveToSlot
   ├─ WaitOrAmbient
   ├─ ReleaseSlot
   └─ Repeat
```

Friendly는 전투 분기를 넣지 않는다. 처음에는 이동과 대기만 확인하고, 대화·작업·경례 같은 행동은 Animation 자산을 확인한 뒤 Activity와 Interaction을 추가한다.

## 9. 소총과 샷건 구현 경계

현재 준비된 것은 **NPC의 무기 종류 선택과 StateTree 분기 조건**까지다. 다음 항목은 아직 구현되지 않았다.

- 공용 Weapon Component 또는 Weapon Actor
- 발사 간격, 탄창, 재장전
- 소총 단일 Hitscan
- 샷건 다중 Pellet과 Spread
- 드론 Damage 적용과 피격 판정
- 사거리·명중률·난이도 수치
- Aim Offset, 발사 Montage, Motion Warping
- Muzzle Flash, 탄흔, 소리
- 아군 오사 방지와 팀 판정

권장 구현 순서는 다음과 같다.

1. 무기 공용 인터페이스: `CanFire`, `StartFire`, `StopFire`, `Reload`
2. AI가 보는 단일 Target Actor와 Aim Point 계약
3. Rifle: 단일 Trace 한 발과 Cooldown
4. Shotgun: 같은 Trigger에서 여러 Pellet Trace와 Spread
5. 표적이 드론인지, 사거리 안인지, 시야가 막히지 않았는지 검사
6. Damage와 실패 처리
7. Animation·FX·SFX 연결
8. Data Asset으로 수치 분리

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

현재 Reservation Component는 Owner의 EndPlay와 Controller의 UnPossess에서 예약을 해제한다. 이후 실제 StateTree Task를 만들 때는 상태 Exit·Task Failed·Task Stopped에서도 반드시 해제해야 한다. 점유자가 사망한 뒤 다른 AI가 이어서 Claim할 수 있는지 별도 자동화와 PIE로 검증한다.

## 11. 단계별 작업 카드

각 카드는 1~3시간 안에 끝내고 완료 조건을 직접 확인한다.

| 카드 | 작업 | 완료 조건 |
|---|---|---|
| `AI-SO-00` | Plugin·Tag·Profile·Reservation·Station C++ 기반 | Build와 기반 자동화 통과 |
| `AI-SO-01` | Smart Object Definition 6종과 Station BP 생성 | **Done** — 6쌍 생성, Slot·Activity·Definition·MG Mesh 자동 검증 통과 |
| `AI-NPC-01` | 적 Rifle·Shotgun·아군 BP와 시험 맵 배치 | **Done** — 4명 Profile·Possess·Activity Tag·NavMesh 투영 검증 |
| `AI-PATROL-01` | 적 순찰 StateTree | 3개 지점을 반복 이동하고 예약 해제 |
| `AI-FRIEND-01` | 아군 BaseRoutine StateTree | 아군 2명이 생활 지점을 겹치지 않고 순환 |
| `AI-PER-01` | 드론 Sight·Event PIE 검증 | 감지 시 순찰 중단, 놓치면 Search 전환 |
| `AI-WPN-01` | 공용 Weapon 계약 | Rifle·Shotgun이 같은 AI 호출 경로 사용 |
| `AI-WPN-02` | Rifle Greybox 발사 | 단일 Trace, 사거리·시야·Cooldown 검증 |
| `AI-WPN-03` | Shotgun Greybox 발사 | Pellet·Spread 분리, 단일 발사 판정 검증 |
| `AI-MG-01` | MG Claim·Move | 두 AI 중 한 명만 MG에 도착 |
| `AI-MG-02` | MG Occupy·Aim·Fire·Release | 사망·중단 뒤 다음 AI가 재점유 |
| `AI-COVER-01` | 비점유 병사 엄폐 | MG 실패 병사가 Cover 지점 사용 |
| `AI-VIS-01` | 외형·Animation 연결 | T Pose·손 위치·Root Motion 문제 없음 |

`AI-SO-00 → AI-SO-01 → AI-NPC-01`은 완료했다. 다음은 `AI-PATROL-01 → AI-FRIEND-01 → AI-PER-01` 순서다. 사격은 이동·예약과 드론 감지가 안정된 뒤 Rifle부터 붙이고 Shotgun을 같은 계약의 두 번째 구현으로 추가한다.

### Asset 재검증 명령

다른 PC에서 Pull한 뒤 Asset의 저장된 연결을 다시 확인할 때 문서 저장소 루트에서 실행한다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\unreal\Invoke-DroneSmartObjectSetup.ps1 -Mode Validate -ProjectPath C:\URproject\drone\Drone.uproject
```

`VALIDATION_OK`가 출력되면 6쌍의 형식·부모 Class·Slot Tag·Definition·MG Mesh 연결이 일치한다. `Create` 모드는 정확한 12개 Asset을 재구성하는 유지보수용이며 일반 작업에서는 실행할 필요가 없다.

NPC 역할 Blueprint와 Greybox 맵까지 다시 확인할 때는 다음 명령을 사용한다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\unreal\Invoke-DroneNPCGreyboxSetup.ps1 -Mode Validate -ProjectPath C:\URproject\drone\Drone.uproject
```

이 검증은 역할 Profile, AI Controller Possess, 역할 Tag, NPC 4명과 Station 10개 배치, Navigation Floor, Recast 설정, NPC 시작 위치의 NavMesh 투영을 확인한다. `BuildNavigation` 모드는 생성 자산을 수리하거나 Navigation을 다시 저장해야 할 때만 사용한다.

## 12. 첫 PIE 검증 체크리스트

- [x] Smart Objects와 Gameplay Interactions Plugin 활성 상태를 프로젝트 설정과 자동화로 확인
- [x] NPC 4명 시작 위치가 NavMesh에 투영되는지 자동화로 확인
- [x] Hostile Rifle 1명, Hostile Shotgun 1명, Friendly 2명 Possess 확인
- [ ] 적이 EnemyPatrol/Guard만 사용
- [ ] 아군이 FriendlyBasePatrol/Ambient만 사용
- [ ] 같은 1-Slot 지점을 두 NPC가 동시에 사용하지 않음
- [ ] 드론이 보이지 않을 때 적 순찰 유지
- [ ] 드론이 Sight에 들어오면 Hostile만 순찰 예약 해제
- [ ] Friendly는 드론을 봐도 전투 상태로 바뀌지 않음
- [ ] MG 사용 가능 적만 MG를 검색
- [ ] Rifle과 Shotgun 상태 분기가 Profile과 일치
- [ ] 드론을 놓치면 Search를 거쳐 순찰 복귀
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
- `Lvl_NPCSmartObjectGreybox`의 NPC 4명·Station 10개·Navigation Floor
- Profile·Possess·Activity Tag·NavMesh 투영 자동화
- Game/Editor Build, NPC 전용 2/2, 전체 `Drone.` 20/20, Blueprint 0/0/0, LFS 검증

### 아직 구현·수동 검증 필요

- 실제 Hostile/Friendly StateTree 자산과 이동 Task
- 최종 NPC 외형·Skeleton·Animation Blueprint 선택과 연결
- Rifle·Shotgun 발사·피해·Animation·FX·SFX
- MG 승하차·조준·사격 Animation과 Turret 제어
- Cover·Search·Return 실제 행동
- 전용 Greybox 맵에서 실제 순찰·아군 이동·드론 감지 동작 확인
- 최종 맵에 NPC와 Smart Object 배치

UE 5.8.1에서 `Gameplay Interactions`는 Experimental 표기가 있는 Plugin이다. 프로젝트에 제한적으로 사용하되 엔진 업데이트 때 API 변경 가능성을 확인하고, 핵심 역할·예약 규칙은 프로젝트 C++와 테스트에 남긴다.
