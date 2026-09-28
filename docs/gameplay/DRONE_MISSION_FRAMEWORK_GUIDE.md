# Mission 통합 프레임워크·NPC 이동 애니메이션 가이드

기준일: 2026-09-24. 로컬 구현 상태이며 커밋·푸시는 수행하지 않았다. Production `/Game/Drone/Maps/Lvl_DroneTraining`은 수정하지 않았다.

## 이번에 준비된 것

Story Mission을 만들 때 매번 Level Blueprint에 목표 판정을 새로 짜지 않도록 `/Game/Drone/Mission`에 재사용 Blueprint 묶음을 만들었다.

| Blueprint | 역할 |
|---|---|
| `Blueprints/Managers/BP_DroneMissionManager` | 선택한 Mission Definition의 순서형 목표, 진행 수량, 제한 시간, 성공·실패, Story Fact를 관리한다 |
| `Blueprints/Managers/BP_DroneMissionPlayerController` | 출격 Drone과 위 Manager를 생성하고 Mission HUD·결과 Flow를 연결한다 |
| `Blueprints/Managers/BP_DroneMissionGameMode` | Story/Test Mission 맵에서 위 PlayerController를 사용하게 하는 GameMode다 |
| `Blueprints/Triggers/BP_MissionObjectiveTrigger` | Box Overlap을 Mission Objective Event로 보고한다 |
| `Blueprints/Triggers/BP_MissionFailureTrigger` | 허용한 Actor가 Box에 들어오면 Mission을 실패시킨다 |
| `Blueprints/Triggers/BP_MissionReturnZone` | 현재 출격한 플레이어 Drone의 귀환을 보고한다 |
| `Blueprints/Targets/BP_MissionDamageTarget` | 기본 체력 100, 피해·사망 Delegate와 파괴 연출 Event를 가진 교체 가능한 Greybox 표적이다 |
| `Blueprints/Tutorial/BP_TutorialHoverZone` | 영역 안에서 저속·수평 상태를 연속 유지하면 `Hover Maintained` 목표를 보고한다 |

Blueprint는 빈 표시용 껍데기가 아니다. 공통 판정은 C++ 부모 클래스에 있고 각 BP는 맵 배치와 기본값 조정을 위한 프로젝트 자산이다. Mesh, VFX, Sound, 최종 Mission 수치와 연출은 파생 BP 또는 Instance에서 설정한다.

## 폴더 계약

```text
/Game/Drone/Mission
└─ Blueprints
   ├─ Managers
   │  ├─ BP_DroneMissionManager
   │  ├─ BP_DroneMissionPlayerController
   │  └─ BP_DroneMissionGameMode
   ├─ Triggers
   │  ├─ BP_MissionObjectiveTrigger
   │  ├─ BP_MissionFailureTrigger
   │  └─ BP_MissionReturnZone
   ├─ Targets
      └─ BP_MissionDamageTarget
   └─ Tutorial
      └─ BP_TutorialHoverZone

/Game/Drone/Data/Missions
└─ DA_Mission_...              # 목표 순서와 Mission 데이터

/Game/Drone/Maps/TestMap       # 기능 시험 맵
/Game/Drone/Maps/Story         # 향후 실제 Story 맵 후보; 최종 명칭은 현재 미정
```

Mission의 규칙과 맵 배치를 분리한다. 예를 들어 “차량 파괴 1회”는 Mission Definition의 Objective Rule이고, 어떤 차량·경로·위치인지는 맵 Actor와 Actor Tag가 담당한다.

## 새 Mission 맵 연결 순서

1. 기존 Production Training 맵이 아닌 별도 Story 또는 Test 맵을 연다.
2. `World Settings → GameMode Override`를 `BP_DroneMissionGameMode`로 지정한다.
3. Mission Definition Data Asset의 `ObjectiveRules`에 목표를 실행 순서대로 추가한다.
4. 맵에 필요한 Trigger와 Damage Target을 배치한다.
5. Rule에 `TargetId`를 썼다면 대상 Actor의 `Details → Actor → Tags`에 정확히 같은 Name을 넣는다.
6. 일반 Front-end의 Mission 선택 경로로 해당 Definition/맵에 진입해 Drone을 선택한다.
7. PlayerController가 Drone과 `BP_DroneMissionManager`를 자동 생성한다. Manager를 맵에 따로 배치하지 않는다.

맵을 Play 버튼으로 직접 실행하면 활성 Mission Definition이 없어 전체 Mission Flow가 시작되지 않을 수 있다. Trigger의 크기·충돌만 확인하는 직접 실행과, Front-end를 거쳐 목표 완료·결과 화면까지 확인하는 Mission 실행을 구분한다.

## 목표 Trigger 사용법

`BP_MissionObjectiveTrigger`를 배치하고 Box 크기를 조정한다. Class Defaults 또는 Instance Details의 `Drone|Mission|Trigger` 항목에서 다음을 정한다.

| 설정 | 사용법 |
|---|---|
| `Trigger Action` | 일반 목표 진행은 `Report Objective Event` |
| `Objective Event` | 현재 지원 Event 중 해당 목표와 같은 값을 선택한다 |
| `Actor Policy` | 플레이어 Drone만 허용하려면 `Active Player Drone`, 특정 차량은 `Actor With Required Tag`, 연출 호출은 `Any Actor` |
| `Required Actor Tag` | `Actor With Required Tag`일 때 들어오는 Actor에 있어야 할 Tag |
| `Use Overlapping Actor As Event Actor` | 켜면 들어온 차량/Drone의 Tag를 Rule `TargetId`와 대조하고, 끄면 Trigger 자신의 Actor Tag를 대조한다 |
| `Trigger Once` | 기본 On. 같은 Actor가 Box 경계에서 흔들려도 한 번만 보고한다 |

현재 Objective Event는 `Training Lap`, `Recon Scan`, `Payload Delivered`, `Target Destroyed`, `Jamming Exited`, `Jammer Disabled`, `Return To Base`, `Hover Maintained`, `Manual`이다. 미션에 새 종류가 필요하면 기존 Event를 억지로 재사용하지 않고 `EDroneMissionObjectiveEvent`와 실제 발생 지점을 함께 확장한다.

Box Overlap 없이 Sequencer나 다른 BP에서 진행할 때는 `Try Activate Mission Trigger`를 호출한다. Director를 이미 들고 있는 시스템은 `Activate Mission Trigger With Director`를 사용할 수 있다.

## 실패 Trigger 사용법

`BP_MissionFailureTrigger`는 기본적으로 `Fail Mission + Actor With Required Tag + Trigger Once`다.

이동 차량의 기지 도착 실패 예시:

1. 목표 차량 Actor Tag에 `Mission2.TargetVehicle`을 넣는다.
2. 도착 지점에 `BP_MissionFailureTrigger`를 놓는다.
3. Trigger의 `Required Actor Tag`도 `Mission2.TargetVehicle`로 설정한다.
4. 차량이 먼저 파괴되면 Health/Target Destroyed 경로로 목표가 완료된다.
5. 살아 있는 차량이 Trigger에 먼저 도착하면 Director가 Mission 실패를 한 번만 처리한다.

최종 차량 Tag·도착 위치·제한 시간은 아직 미정이며 실제 Mission 2 Data Asset을 만들 때 확정한다.

## 귀환 Zone 사용법

단순 귀환은 `BP_MissionReturnZone`을 우선 사용한다. Box 크기와 Actor Tags를 설정하고 Mission Rule의 Event를 `Return To Base`로 맞춘다. `TargetId`가 비어 있으면 모든 귀환 Zone을 허용하고, 값이 있으면 Zone의 Actor Tag와 일치해야 한다.

`BP_MissionObjectiveTrigger`도 `Return To Base`를 보고하도록 설정할 수 있지만, 플레이어 Drone 귀환만 필요할 때는 의도가 분명한 전용 Return Zone이 낫다.

## 피해·파괴 목표 사용법

`BP_MissionDamageTarget`은 기본 체력 100이며 Unreal의 표준 `Apply Damage`/`Apply Radial Damage` 경로를 받는다.

1. 맵에 BP를 배치한다.
2. `Target Visual`의 Static Mesh를 차량·재머·시설 Greybox 또는 최종 Mesh로 바꾼다.
3. Actor Tags에 Mission Rule `TargetId`와 같은 값을 넣는다.
4. Rule Event를 `Target Destroyed`로 설정한다.
5. Projectile, FPV 자폭 또는 다른 공격이 이 Actor에 실제 Damage를 전달하는지 확인한다.
6. `Mission Target Damaged Visual`과 `Mission Target Destroyed Visual` Event에 Material, Niagara, Sound, 잔해 연출을 연결한다.

기본 사망 규칙은 체력 0에서 한 번만 파괴 처리하고 충돌을 끄며, Greybox 잔해 확인을 위해 Visual은 남긴다. `Hide Visual When Destroyed`를 켜면 파괴 시 Mesh도 숨긴다.

맵 시작 전에 배치된 `UDroneHealthComponent` 대상은 Manager가 자동 등록한다. Mission 시작 뒤 Spawn한 `BP_MissionDamageTarget`도 스스로 등록·해제한다. 다른 동적 Actor에 Health Component만 붙였다면 Spawn 직후 Manager의 `Register Objective Target`, 제거 전 `Unregister Objective Target`을 호출한다.

## Mission 1~4에 조합하는 방법

아래는 구현 조립 순서이며 대상 수량·시간·위치·최종 Story 규칙은 아직 확정값이 아니다.

| Mission | 사용할 기반 | 아직 필요한 콘텐츠/연결 |
|---|---|---|
| Mission 1 구급품 전달 | `Payload Delivered`, Objective Trigger, 제한 시간, Failure Trigger, Return Zone | 부상 요원·구급품·정보 회수 Actor, 실제 맵/Definition, 파괴·이탈 실패 규칙 |
| Mission 2 이동 차량 격파 | Damage Target 또는 Health 차량, Target Destroyed, 목적지 Failure Trigger, Story Fact | 실제 차량 Route/표적 BP, FPV 희생 허용 판정, 잔해 Scan, 실제 맵/Definition |
| Mission 3 재밍 기지 | Jammer Disabled, 광섬유 Drone, Damage Target, AI/포탑, Return Zone | Mission 중 Drone 교대, UGV 무장, 방공망 Actor, 실제 맵/Definition |
| Mission 4 본진 타격 | 순서형 Damage Target/Trigger 조합, AI/포탑, 결과 Flow | 장거리 타격 기능/Sequence, 본진 맵, 엔딩 Cinematic, 실제 Definition |

현재 Production 성격의 저장 Mission Definition은 기존 Training 하나이고, 별도로 호버링·물자 전달·FPV 표적 타격용 Test Tutorial Definition 3개를 추가했다. Story Mission 1~4가 플레이 가능한 상태가 된 것은 아니다. 다음 Story 개발은 Mission 1의 작은 Vertical Slice부터 진행한다.

## Tutorial Mission 시험 맵

`/Game/Drone/Maps/TestMap/Lvl_DroneTutorialMissionTest`는 새 Mission BP 기반을 실제 Flow로 확인하는 공용 Greybox 맵이다. Production Training 맵과 분리되어 있다.

| Mission Definition | 허용 기체 | 목표 순서 |
|---|---|---|
| `DA_Mission_Tutorial_Hover` | Scout | 3초 안정 호버 → 귀환 |
| `DA_Mission_Tutorial_Payload` | Drop | 지정 표적 물자 투하 → 귀환 |
| `DA_Mission_Tutorial_FPV` | FPV Strike | Arm 후 표적 파괴; 자폭 기체이므로 별도 귀환 없음 |

호버링 기본 판정은 속도 `75cm/s` 이하, 수직속도 `40cm/s` 이하, Pitch/Roll `15°` 이하를 `3초` 연속 유지하는 것이다. 영역을 나가거나 조건을 벗어나면 기본적으로 시간이 0으로 초기화된다. 이는 최종 난도가 아니라 `BP_TutorialHoverZone`의 Class Defaults 또는 배치 Instance에서 조정할 Greybox 값이다. 상시 Tick은 사용하지 않으며 플레이어 Drone이 Box와 겹친 동안에만 기본 `0.1초` Timer가 동작한다.

로비 Mission 목록에는 기존 Training과 위 세 Test Tutorial이 모두 표시된다. 각 Tutorial은 허용 기체가 하나뿐이라 Drone 선택 화면에서 해당 역할만 선택할 수 있다.

### 수동 플레이 순서

1. `/Game/Drone/Maps/Lvl_DroneFrontEnd`에서 Play한다.
2. 시작 화면을 넘기고 `튜토리얼 1 - 호버링`, `튜토리얼 2 - 물자 전달`, `튜토리얼 3 - FPV 표적 타격` 중 하나를 선택한다.
3. 브리핑을 넘기면 같은 `Lvl_DroneTutorialMissionTest`로 이동하고 해당 기체만 선택할 수 있다.
4. 호버링은 중앙 Hover Pad 상공 Box 안에서 안정 상태를 3초 유지하고 시작점 뒤 Return Pad로 돌아온다.
5. 물자 전달은 Drop Drone으로 노란 Payload 표적까지 이동한다. 임시 조작은 `좌클릭/패드 RB=화물 투하`, `우클릭/패드 LB=탑뷰`다. 표적 적중 뒤 Return Pad로 돌아온다.
6. FPV는 임시 `좌클릭/패드 RB`로 Arm하고 최소 충돌 속도 `600cm/s` 이상으로 떠 있는 표적을 타격한다. `우클릭/패드 LB`는 Disarm이다.

맵의 추가 Carryable은 첫 선적재 화물 투하 이후 재적재를 시험하는 예비 크레이트다. 적재량이 0인 상태에서 300cm 안에서 Primary를 누르면 기체 하단에 붙고 다시 Primary를 누르면 같은 Actor가 투하된다. 이 재적재는 현재 Mission 필수 목표가 아니라 추가 조작 연습이다.

## NPC 걷기 애니메이션

NPC가 이동하면서 서 있는 자세로 미끄러지지 않도록 프로젝트 전용 Idle/Walk/Run 자산을 분리했다.

| NPC | Anim Blueprint | Locomotion Blend Space |
|---|---|---|
| 적 Rifle/Shotgun | `/Game/Drone/AI/Animation/ABP_NPC_Rifle_Greybox` | `/Game/Drone/AI/Animation/BS_NPC_Rifle_Locomotion` |
| 아군 기지 NPC | `/Game/Drone/AI/Animation/ABP_NPC_Unarmed_Greybox` | `/Game/Drone/AI/Animation/BS_NPC_Unarmed_Locomotion` |

적은 Rifle 자세의 Idle/Walk/Run을 유지하고, 아군은 Unarmed Idle/Walk/Run을 쓴다. `BP_NPC_Hostile_Rifle`, `BP_NPC_Hostile_Shotgun`, `BP_NPC_Friendly_Base`의 Mesh `Animation Mode`는 Animation Blueprint이며 각각 위 Anim Class에 연결되어 있다.

Editor에서 확인할 때는 `Lvl_NPCSmartObjectGreybox`를 열고 다음을 본다.

1. 적 Rifle/Shotgun이 순찰 중 발을 움직이고 이동속도에 따라 Walk/Run이 바뀌는지 본다.
2. Friendly가 기지 동선을 걸을 때 무장 자세가 아니라 Unarmed 이동을 쓰는지 본다.
3. 정지하면 Idle로 돌아오는지, 이동 시작/정지 경계에서 과도한 발 미끄러짐이 없는지 본다.
4. 적이 드론을 감지했을 때 이동 Anim과 조준/사격 로직이 서로 덮어쓰지 않는지 본다.

Animation Asset 생성·검증은 다음으로 재실행할 수 있다.

```powershell
cd C:\URproject\drone
.\Tools\AssetMigration\Invoke-DroneMissionFramework.ps1
```

이 명령은 Mission Blueprint 묶음과 NPC 이동 자산을 생성/갱신하고 저장 상태를 검증한다. Production Training 맵을 열거나 저장하지 않는다.

## 자동화와 현재 검증 결과

- `Drone.Mission.FrameworkAssets`: Manager/GameMode/Controller 연결, Trigger 기본 정책, Damage Target 체력 100 검증 성공
- `Drone.Mission.ObjectiveRules`: Event·Tag·중복 방지·제한 시간·Story Fact 규칙 검증 성공
- `Drone.Mission.MissionSystemsTestMap`: 기존 Mission 시험 맵 저장 계약 검증 성공
- `Drone.Tutorial.MissionLessonsTestMap`: Test Map, Hover/Payload/FPV/Return Actor Tag와 세 Mission Definition·기체·목표 순서 검증 성공
- `Drone.Flow.Contract`, `Drone.Flow.FrontEndContract`, `Drone.Flow.FrontEndPIE`: 4개 Mission Catalog와 다중 Mission 로비 Flow 검증 성공
- NPC 생성/검증 스크립트: 적 Rifle과 아군 Unarmed Idle/Walk/Run, 각 NPC BP 연결 검증 성공
- `DroneEditor Win64 Development`: 새 C++ 부모 클래스와 동적 Target 등록 코드 Build 성공

기존 `Drone.AI.NPCGreyboxAssets` 종합 테스트는 현재 맵에 추가된 Actor 수와 예전 고정 기대값이 달라 실패한다. 보고된 항목은 Smart Object Station `예상 12/실제 34`, 자동포탑·차량 `예상 1/실제 2`, Rifle/Shotgun `예상 각 1/실제 각 3`, Ground Vehicle Auto Drive 설정이다. 이번 새 애니메이션 생성 실패가 아니며, 다음 AI 맵 정리 때 “정확한 개수 고정” 테스트를 도구 소유 Tag/최소 계약 기준으로 갱신해야 한다.

## 문제가 생기면

- Manager가 없음: 맵 GameMode가 `BP_DroneMissionGameMode`인지, Front-end에서 실제 Mission을 선택하고 Drone까지 출격했는지 확인한다.
- Trigger가 반응하지 않음: Collision Overlap, Actor Policy, Required Actor Tag, 현재 Rule Event를 확인한다.
- 진행 수치가 오르지 않음: Rule `TargetId`와 Event Actor의 Actor Tags가 정확히 같은지 본다.
- 파괴했는데 목표 미완료: 공격이 실제 `Apply Damage`를 호출하는지, 대상에 `UDroneHealthComponent`가 있는지, 동적 Actor를 등록했는지 본다.
- 같은 Box에서 반복 진행: `Trigger Once`가 켜져 있는지, 여러 Trigger가 같은 위치에 겹쳐 있지 않은지 본다.
- NPC가 미끄러짐: NPC Mesh의 Anim Class, Blend Space의 Speed 입력, Character Movement의 실제 Velocity를 확인한다.
- NPC가 뒤로 걸음: 애니메이션보다 먼저 Controller 회전 소유권, `Orient Rotation to Movement`, MoveTo 목적지와 몸 Forward를 확인한다. 사격할 때만 정면이라면 Mesh 장착각보다 이동/AI 회전 계약 문제일 가능성이 높다.
