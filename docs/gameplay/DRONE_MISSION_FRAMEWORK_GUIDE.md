# Mission 통합 프레임워크·NPC 이동 애니메이션 가이드

기준일: 2026-10-02 새벽(C PC). Catalog·직접 Play 연결을 최신화했고 아래 기존 2026-09-24 자산/검증 기록은 당시 범위로 보존한다. 로컬 구현 상태이며 커밋·푸시는 수행하지 않았다. Production `/Game/Drone/Maps/Lvl_DroneTraining`은 수정하지 않았다.

2026-10-02 새벽 후속(C PC, ec2e88f + 로컬 미커밋, Claude 구현·Codex 문서 반영): Mission DA `Mission Definition|Progression → NextMissionId`로 Story M1 골든타임→M2 인터셉트→M3 베일브레이커→M4 엔드게임(끝)을 연결했다. 성공 결과 [다음]·로비 순서가 연결을 따르며 M2→M3 결과 분기는 현재 미정이다. 튜토리얼 8개 연결·시간·완료 UI는 [튜토리얼 가이드 5절](DRONE_TUTORIAL_IMPLEMENTATION_TEST_GUIDE.md#5-tutorial-전용-ui-구현)을 따른다.

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
3. Mission Definition DA를 `/Game/Drone/Data/Missions`(하위 폴더 포함)에 만들고 고유 `MissionId`, `MissionMap`, `LobbyCategory`, 허용/기본 기체와 `ObjectiveRules`·시작/성공/실패 규칙을 지정한다. **C++ 기본 목록을 수정하지 않아도 로비 Catalog에 자동 등록된다.**
4. 맵에 필요한 Trigger와 Damage Target을 배치한다.
5. Rule에 `TargetId`를 썼다면 대상 Actor의 `Details → Actor → Tags`에 정확히 같은 Name을 넣는다.
6. Front-end에서 해당 Mission을 선택해 맵에 진입하고 Drone을 선택한다.
7. PlayerController가 Drone과 `BP_DroneMissionManager`를 자동 생성한다. Manager를 맵에 따로 배치하지 않는다.
8. 시험 맵을 직접 Play하려면 `ADroneMissionTestEntry`를 부모로 하는 BP를 맵에 배치하고 `DefaultTestMission`에 DA를 지정한다. 이 Entry는 로비에서 선택한 활성 미션을 덮어쓰지 않는다. **Production 맵에서는 사용하지 않는다.** 직접 Play 목표·결과와 Front-end 선택/출격 흐름을 각각 확인한다.

`EnsureDefaultCatalog`는 기존 C++ 기본 목록(Drone 5·Mission 14)을 먼저 등록한 뒤 Asset Registry로 `/Game/Drone/Data/Drones`와 `/Game/Drone/Data/Missions`의 하위 폴더까지 탐색해 미등록 Definition을 추가한다. 잘못된 DA·ID 중복은 기존 Catalog를 유지하고 `LogDrone` 경고만 남긴다. 로비 정렬은 NextMissionId 연결 순서(연결 없는 미션은 MissionId순, GetMissionIdsInLobbyOrder)이며 `Drone.Build.cs`에 Runtime `AssetRegistry` 의존성을 추가했다.

### 설정 위치 표

| 무엇 | 어디서 | 항목 |
|---|---|---|
| 미션 이름·설명·지역·난이도·썸네일·로비 탭(Story/Tutorial/Racing) | `/Game/Drone/Data/Missions/DA_Mission_*` | DisplayName, LobbyDescription, RegionText, DifficultyText, Thumbnail, LobbyCategory |
| 미션 ↔ 맵 연결 | 같은 DA | `MissionMap` (출격 시 열리는 맵) |
| 출격 가능 기체·기본 기체 | 같은 DA | AllowedDroneIds, DefaultDroneId (`/Game/Drone/Data/Drones/DA_Drone_*`의 DroneId) |
| 목표 순서·제한 시간·대상 | 같은 DA | ObjectiveRules(ObjectiveId, Description, Event, RequiredProgress, TimeLimitSeconds, TargetId, StoryFactCondition/Id), InitialObjectives, SuccessRuleId, FailureRuleId |
| 브리핑 영상/Sequence | 같은 DA | BriefingAsset(비면 정적 브리핑) |
| 스토리 분기 | 같은 DA | StoryFactsGrantedOnSuccess / RemovedOnSuccess |
| 미션 맵의 게임 규칙 | 미션 맵 World Settings | GameMode Override = `BP_DroneMissionGameMode` (Manager·PlayerController 자동 생성, Manager를 따로 배치하지 않음) |
| 맵 안 목표·실패·귀환 지점 | 미션 맵에 배치 | `BP_MissionObjectiveTrigger`, `BP_MissionFailureTrigger`(TriggerAction, ObjectiveEvent, ActorPolicy, RequiredActorTag, bTriggerOnce), `BP_MissionReturnZone`, `BP_MissionDamageTarget`(MaximumHealth 기본 100; Actor Tags = Rule의 TargetId) |
| 맵 직접 Play 시 미션 | 시험 맵에 배치 | `ADroneMissionTestEntry`의 DefaultTestMission (Production 맵 금지) |
| 로비 그림·버튼 이미지·소리·목록 줄바꿈 | `/Game/Drone/FrontEnd/UI/WBP_DroneFrontEndRoot` Class Defaults | TitleBackground/Overlay/Logo, Button*Texture, ButtonHover/ClickSound, MissionButtonLabelWrapWidth(기본 270) |
| 로비 맵 | `/Game/Drone/Maps/Lvl_DroneFrontEnd` | GameMode `BP_DroneFrontEndGameMode` |

### 2026-10-01 밤 검증 범위

- C PC HEAD `ec2e88f` + STATUS 밤 절의 미커밋 Source/테스트. 작업 도구 Claude, 문서 반영 Codex. Editor 종료 후 Build Succeeded(`Saved/Automation/ClaudeCatalog/build.log`).
- NullRHI Flow 전체 + Mission 전체 + HoverMissionPIE + IndependentMapEntryPIE 15/15 Success(`ClaudeCatalog/test.log`). `CatalogAutoRegistration`은 두 폴더 Definition의 동일 Asset 등록·폴더 밖 Mission 없음·재호출 개수 유지를 확인한다. 미션 14·버튼 4/9/1 비교는 하한 비교로 변경했다.
- `LobbyLayoutStabilityPIE`는 렌더 전용 진단이다. 이번 NullRHI 로그의 Fail(samples=0)은 화면 표본이 없어 판정 불가이며 15/15 대상에서 제외한다. 앞선 렌더 Success를 이번 NullRHI 결과로 혼동하지 않는다.
- 수동 확인 대기: 새 DA를 하나 만들어 실제 사용자 흐름에서 로비에 뜨는지, 로비 1280/1920.
- BUILD-PACKAGE-01(2026-10-02 C PC Claude): Config/DefaultGame.ini Asset Manager의 DroneMission(/Game/Drone/Data/Missions)·DroneDefinition(/Game/Drone/Data/Drones) AlwaysCook와 MissionMap Soft 참조 맵 쿠킹 설정 구현. NullRHI PackagingPrimaryAssets Success(미션 14·기체 5 AlwaysCook·모든 미션 맵 존재), ClaudePackaging/test.log. 실제 패키징·패키지에서 미션 진입은 미실행/확인 대기.

## 브리핑 대사 (2026-10-02 새벽, C PC)

작업 도구 Claude, 문서 반영 Codex. Mission DA의 `BriefingLines` 배열 순서대로 하단 고정 높이 자막을 표시한다. 배열이 비어 있으면 자막 영역을 숨기고 기존 정적 브리핑을 사용한다.

| DA 칸 | 입력법 |
|---|---|
| Speaker | 말하는 사람(Story 현재 “허브”) |
| Text | 자막 원문 |
| Voice | 음성 SoundWave/SoundCue 등 USoundBase 자산을 연결. 현재 음원 없음·빈 슬롯은 자막만 표시 |
| DurationSeconds | 0이면 음성 길이 또는 글자 수로 자동 산정, 양수면 해당 줄 시간 직접 지정 |
| StoryFactCondition / StoryFactId | Always 등 조건과 Story Fact ID. 미정 분기를 임의 결정하지 않음 |

1. `/Game/Drone/Data/Missions/DA_Mission_*`을 열어 BriefingLines 항목을 순서대로 추가하고 Speaker·Text를 입력한다.
2. 음원이 준비되면 프로젝트에 가져온 음성 자산을 각 줄 Voice 슬롯에 연결한다. 실제 소리·길이·자막 동기화는 사람이 확인한다.
3. 조건이 필요한 줄만 StoryFactCondition·StoryFactId를 지정한다. M3 첫 줄 “오마르는 처리됐다…”는 `Story.TargetEliminated`가 있을 때만 표시한다.
4. FrontEnd Root(`/Game/Drone/FrontEnd/UI/WBP_DroneFrontEndRoot`) Class Defaults의 `BriefingSecondsPerCharacter=0.075`, `BriefingMinLineSeconds=2.5`, `BriefingMaxLineSeconds=9`를 조정한다.
5. FrontEnd 시작→Story 미션 선택→브리핑에서 자동 진행·패드 Y/Tab 건너뛰기·마지막 줄 유지·화면 이탈 시 정지를 확인한다. 월드 타이머로 진행한다.

Figma Slide 34/42/43/44 원문(Codex research 2026-10-01)을 Story 4개에 입력했다: M1 4·M2 4·M3 5·M4 6줄, 화자 허브. M3 조건 없으면 첫 줄을 빼 4줄이다. 반대 분기 M3 첫 대사는 Figma 원문이 없어 비워 두었고 M2→M3 분기는 현재 미정이다. 튜토리얼 브리핑 대사는 미입력, 음원은 없음, 진입 1회 시네마틱 완료 근거 없음. 재출격 시 재생 여부도 현재 미정이다.

NullRHI `Drone.Flow.BriefingLinesPIE` Success(첫 줄·화자, 자동 진행, Y/Tab, 마지막 줄, 정지, M3 조건 없는 4줄), 근거 `C:\URproject\drone\Saved\Automation\ClaudeBriefing\test2.log`. 자막 가독성·속도·실제 음성은 수동 확인 대기다.

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

## 실패 처리와 체크포인트

2026-10-01 밤 후속, C PC Unreal `ec2e88f` + 로컬 미커밋. 작업 도구 Claude, 문서 반영 Codex. MISSION-CHECKPOINT-01 실패 재출격은 구현됨·자동 검증 완료이며 실제 추락/재출격 체감은 수동 확인 대기다.

| 설정 | 위치 | 의미 |
|---|---|---|
| `FailureResponse` | `/Game/Drone/Data/Missions/DA_Mission_*` | 결과 화면 또는 체크포인트에서 재출격 |
| `MaxCheckpointRestarts` | 같은 미션 DA | 0 = 제한 없음, 횟수를 다 쓰면 기존 실패 결과 화면 |

기체 파괴·현재 목표 제한 시간 초과·실패 Trigger는 같은 실패 경로를 쓴다. 재출격은 맵을 다시 열지 않고 완료 목표·부서진 표적을 유지한다. 마지막 체크포인트(없으면 처음 출격 위치)에 같은 기체 종류·조작 방식으로 새 기체를 띄워 빙의하고 Director를 재연결하며 옛 기체를 제거한다. 현재 목표 제한 시간만 다시 센다.

| DA 분류 | 확정 실패 처리(Figma 기준, Claude 지시서) | 재출격 제한 |
|---|---|---|
| Tutorial Hover·Forward·Heading·GateFlight·Payload·FPV·UGV_NPC·UGV_Turret | 체크포인트 재출격 | 0(무제한) |
| Story GoldenTime(M1)·VeilBreaker(M3)·Endgame(M4) | 체크포인트 재출격 | 0(무제한) |
| Story Intercept(M2)·Tutorial_Training·Racing_Circuit | 결과 화면 | 0(무제한 설정, 결과 화면 방식) |

### Actor 배치법

1. 미션 맵의 Place Actors에서 `DroneMissionCheckpoint`를 검색해 직접 배치한다.
2. `CheckpointId`를 지정하고, 특정 목표 진행 중에만 활성화하려면 `RequiredObjectiveId`를 해당 목표 ID로 맞춘다.
3. `bActivateOnce`로 한 번만 활성화할지 조정한다. 플레이어 기체가 지나가면 재출격 위치가 갱신된다.
4. `RestartHeightOffset`(기본 150cm)을 조정하고 화살표를 재출격 방향으로 돌린다. 방향은 Yaw만 사용한다.
5. 해당 미션 DA의 FailureResponse·횟수 제한을 확인하고 추락/시간 초과/실패 Trigger를 각각 확인한다. 팀원 Production Training 맵을 시험용으로 덮어쓰지 않는다.

아직 실제 맵에 체크포인트 Actor를 배치하지 않았다. 현재 재출격은 첫 출격 위치를 쓴다. M1 예시: 정보단말 회수 구현 뒤 픽업 지점에 Actor를 배치하고 진행 목표 ID·방향·높이를 맞춘다. 정보단말 회수와 픽업 지점 배치가 완료됐다는 뜻은 아니다. 재출격 때 브리핑 재생은 MISSION-BRIEFING-02 뒤이며 여부는 현재 미정이다(Figma M1은 “브리핑 재생 포함”, 자막 시스템 구현·음원 없음). 스토리 충돌·레이싱 방식도 현재 미정이다.

### 검증과 수동 확인

- NullRHI `Drone.Mission.CheckpointRestartPIE` Success: 다른 목표용 체크포인트 무시·1회 갱신·파괴→재출격 2회(새 기체/빙의/Director 재연결/옛 기체 제거/300cm 이내/방향 90°), 세 번째 파괴→실패 결과. `Saved/Automation/ClaudeCheckpoint/test1.log`.
- `Drone.Mission.FailureResponseData` Success, 전체 `Drone.*` NullRHI 80개 중 Success 73·실패 7(기존 NPC 개수 4·렌더 전용 진단 1·Production Training 2). 패드 2개는 렌더링 필요 경고로 건너뜀. `Saved/Automation/ClaudeCheckpoint/full.log`.
- 수동 확인 대기: 재출격 방식 튜토리얼에서 출격 후 추락해 같은 기체/조작으로 첫 출격 위치에 돌아오는지, 완료 목표·부서진 표적 유지·현재 목표 시간 재설정과 체감을 확인한다. 체크포인트 맵 배치 뒤 중간 지점 재출격도 별도 확인한다. `PC / 패드 / 맵 / 입력 / 기대 / 결과`를 기록한다.
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

2026-09-24 당시 기록(현재 Catalog 14개·Tutorial 8수업 독립 맵이며 현행 가이드를 우선): 현재 Production 성격의 저장 Mission Definition은 기존 Training 하나이고, 별도로 호버링·물자 전달·FPV 표적 타격용 Test Tutorial Definition 3개를 추가했다. Story Mission 1~4가 플레이 가능한 상태가 된 것은 아니다. 다음 Story 개발은 Mission 1의 작은 Vertical Slice부터 진행한다.

## Tutorial Mission 시험 맵

`/Game/Drone/Maps/TestMap/Lvl_DroneTutorialMissionTest`는 새 Mission BP 기반을 실제 Flow로 확인하는 공용 Greybox 맵이다. Production Training 맵과 분리되어 있다.

| Mission Definition | 허용 기체 | 목표 순서 |
|---|---|---|
| `DA_Mission_Tutorial_Hover` | Scout | 3초 안정 호버 → 귀환 |
| `DA_Mission_Tutorial_Payload` | Drop | 지정 표적 물자 투하 → 귀환 |
| `DA_Mission_Tutorial_FPV` | FPV Strike | Arm 후 표적 파괴; 자폭 기체이므로 별도 귀환 없음 |

호버링 기본 판정은 속도 `75cm/s` 이하, 수직속도 `40cm/s` 이하, Pitch/Roll `15°` 이하를 `3초` 연속 유지하는 것이다. 영역을 나가거나 조건을 벗어나면 기본적으로 시간이 0으로 초기화된다. 이는 최종 난도가 아니라 `BP_TutorialHoverZone`의 Class Defaults 또는 배치 Instance에서 조정할 Greybox 값이다. 상시 Tick은 사용하지 않으며 플레이어 Drone이 Box와 겹친 동안에만 기본 `0.1초` Timer가 동작한다.

로비 Mission 목록에는 기존 Training과 위 세 Test Tutorial이 모두 표시된다. 각 Tutorial은 허용 기체가 하나뿐이라 Drone 선택 화면에서 해당 역할만 선택할 수 있다.

### 수동 플레이 순서 — 2026-09-24 당시 기록(현재 수업은 독립 TestMap/Tutorial 맵, [현행 가이드](DRONE_TUTORIAL_IMPLEMENTATION_TEST_GUIDE.md) 5절·[테스트 순서](DRONE_TEST_MAP_GUIDE.md) 우선)

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
