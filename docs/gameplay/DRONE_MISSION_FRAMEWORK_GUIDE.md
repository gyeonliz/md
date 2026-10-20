# Mission 통합 프레임워크·NPC 이동 애니메이션 가이드

현재 절차 기준: 2026-10-20 C PC. Mission 규칙·스포이드 대상 연결/나침반·맵 배치·재밍 Radar·첫 수업 계약을 소스와 대조한다. 날짜별 실행 결과는 [STATUS](../../STATUS.md)·[WORKLOG](../history/DRONE_WORKLOG.md)를 따른다. Production `/Game/Drone/Maps/Lvl_DroneTraining`은 시험용으로 수정하지 않는다.

2026-10-02 새벽 후속(C PC, ec2e88f + 로컬 미커밋, Claude 구현·Codex 문서 반영): Mission DA `Mission Definition|Progression → NextMissionId`로 Story M1 골든타임→M2 인터셉트→M3 베일브레이커→M4 엔드게임(끝)을 연결했다. 성공 결과 [다음]·로비 순서가 연결을 따르며 M2→M3 결과 분기는 현재 미정이다. 튜토리얼 8개 연결·시간·완료 UI는 [튜토리얼 가이드 5절](DRONE_TUTORIAL_IMPLEMENTATION_TEST_GUIDE.md#5-tutorial-전용-ui-구현)을 따른다.

현행 Story 표시명은 [CONTEXT의 확정 명칭](../../CONTEXT.md#story-미션-표시명)을 따른다. `DisplayName`·`EnglishTitle` 정리 도구는 이름만 갱신하며 GoldenTime/Intercept/VeilBreaker/Endgame 내부 ID·경로·Story Fact·저장·목표를 보존한다. M3의 내부 `VeilBreaker`는 표시명 `보급 차단 / SUPPLY BREAK`와 달라도 정상이다. 적용·화면 검증 상태는 STATUS를 따르며 명칭 변경만으로 목표·분기를 바꾸지 않는다.

## 이번에 준비된 것

### Story 맵 시작·목표·NPC 배치

Story M1은 `Maps/Lvl_Battlefield`, M2·M3는 원본 MilitaryBase를 보존해 분리한 `Maps/Missions/Lvl_Story02_Intercept`·`Lvl_Story03_VeilBreaker`를 사용한다. M4는 `Maps/Lvl_MilitaryCamp`다. 실제 검증 상태는 STATUS/WORKLOG가 정본이다.

- 출격은 배치된 `SM_helicopter_base*`의 표시 경계 중심 XY·윗면+52cm다. DA `RuntimeStartTransform`은 패드 선택 기준과 출격 Yaw를 제공하며, 패드가 없을 때만 기존 DA/시작 표식/PlayerStart 경로를 사용한다. 첫 LOS의 관찰 시점·후진/착지 예외는 보존한다.
- 맵의 `Drone/MissionStart`에서 패드를 이동하면 다음 출격이 따라간다. M3 사본의 패드만 원래 `M_Start_Mission3` XY의 지면으로 옮겼다. M2·원본 기지를 함께 옮기지 않는다.
- `Drone/MissionTargets/M01`의 `M01_MainTarget_Delivery`는 기존 M_Target XY를 유지하고 Shack의 충돌뿐 아니라 표시 지붕 높이까지 확인해 위로 올렸다. DROP 표기와 나침반으로 찾는다. `Drone/Defense/M01`의 포탑2개는 기존 M_Turret 위치다. 기존 병사6명은 보존했다.
- M2는 `M02_MainTarget_Convoy`에 기존 `BP_DroneVehicleSplineRoute`를 직접 연결한다. 옛 임시 직선60m 차량을 추가하지 않는다. M3는 `M03_MainTarget_Jammer`를 연결하며 기존 재밍 완전 이탈 규칙을 유지한다. 역할 교대·최종 시나리오를 완성한 것은 아니다.
- `Drone/Managers`의 `M01/02/03/04_TargetCompassManager` 인스턴스에서 TargetBindings의 실제 대상 Actor를 스포이드로 교체한다. 목표 판정·표시가 같은 대상을 따른다. 배치 매니저가 전혀 없는 Story에만 런타임 Tag 기반 매니저를 보완 생성한다.
- M4는 기존 고정 포탑 `BP_AutoTurret_Emplaced_C_24/18/14`를 `M04_MainTarget_Turret_01/02/03`으로 구분해 연결했다. 기존 3개 파괴 규칙/제한시간은 현재 기준안이며 최종 기획 수량 확정은 아니다. 새 상대좌표 표적3개를 중복 생성하지 않는다. 기존 NPC27·포탑18개를 보존한다.
- Camp 원본에는 헬기포트가 없어 같은 `SM_helicopter_base_01`을 추가했다. 사용자 확인 위치 `(9700,6500,6105.43cm)`·회전0·Scale0.3을 유지하며 DA 기준 출격점은 `(9700,6500,6212.90cm)`다. 재밍 회피를 위해 포트를 옮기지 않는다. 크기 조정 후 펜스와의 시각적 겹침은 줄였지만 UGV 실제 주행/출발 피격·카메라 흔들림은 수동 확인한다.
- Camp 재밍은 **해당 맵의 Radar8개 인스턴스만** `JammingRadiusCm=2000`(20m), `FullStrengthRadiusCm=400`(4m)로 조정했다. `JammingHalfHeightCm=3000`·출력1·활성 상태는 유지한다. 기존 150m/최대25m의 과도한 중첩을 줄인 기준안이며 M3와 BP 기본값은 바꾸지 않았다. Details → Drone → Jamming → Radar에서 변경하고 실제 JammingBounds·시작 신호100%·시설 근접/이탈을 시험한다.
- 위치 표식은 삭제하지 않는다. M_Start/M_Target/M_Radar/M_Enemy/M_Turret 큐브의 Editor 위치를 보존하고 플레이 중 표시/충돌만 끈다. 실제 적/NPC/포탑을 대신 숨기지 않는다.
- `Drone/Navigation`의 NavMeshBounds는 실제 병사 활동 범위와 지면을 포함한다. Recast `RuntimeGeneration=Dynamic`, `ForceRebuildOnLoad=True`, 타일 생성 동시 작업2개다. **플래그만 바꾸고 저장하면 타일0이 남을 수 있으므로 정식 Build→완료 대기→저장** 후 새 로드에서 검사한다. P로 영역/실제 이동을 확인한다. Volume 밖 이동은 범위를 조정하며 같은 Agent Recast를 중복 배치하지 않는다.

`Tools/AssetMigration/ConfigureStoryMissionLayout.py`는 Editor 종료 후 한 프로세스·한 미션만 처리한다. `DRONE_STORY_LAYOUT_MISSION=1/2/3/4`, Nav 로드 정책만 고칠 때 `DRONE_STORY_LAYOUT_NAV_ONLY=1`을 사용한다. 원본/기존 자산은 `Saved/Backups/CodexMissionLayout_20261020`에 보존한다. M4는 배치 재료 확인을 통과하기 전 저장하지 않으며 메모리 보호를 우회하지 않는다. 팀원 Production Training은 이 도구 대상이 아니다.

Nav 저장 도구는 `Diagnostics.StoryLayout.BakeNavigation`이며 명시적 `-DroneApplyStoryNavigation -DroneLayoutBakeMap=/Game/Drone/Maps/...`가 필요하다. 승인된 Story 한 맵만 Build/EnsureBuildCompletion하고 타일·NPC 투영이 유효할 때 저장한다. 일반 검증에 저장 플래그를 붙이지 않는다. MCP 장시간 요청의 socket_send_failure가 함께 기록된 실행은 기능 assert가 맞아도 전체 Pass로 쓰지 않는다. 최신 실행 수치/정정은 WORKLOG를 따른다.

Story Mission을 만들 때 매번 Level Blueprint에 목표 판정을 새로 짜지 않도록 `/Game/Drone/Mission`에 재사용 Blueprint 묶음을 만들었다.

### 시작 지점을 수동으로 옮기기

1. PIE를 Stop하고 사용할 실제 미션 맵을 연다. Camp는 `Lvl_MilitaryCamp`, M2/3은 위 독립 사본이며 원본 MilitaryBase를 수정하지 않는다.
2. Outliner → `Drone/MissionStart` → 헬기포트를 선택한다. Camp의 액터 이름은 `M04_SM_helicopter_base_01`이다. `F`로 선택 위치를 찾는다.
3. `W`로 이동하거나 Details → Transform → Location XYZ를 입력한다. 철조망/벽과 겹치지 않고 지면 위에 놓는다. Camp 현재 위치 `(9700,6500,6105.43cm)`, Scale0.3은 사용자 확인값이다.
4. 맵을 저장한다. PlayerStart를 옮기는 방식이 아니다. 출격 위치는 패드 표시 경계의 중심 XY·윗면+52cm를 따라가며 실제 기체는 충돌/착지 보정을 더 받을 수 있다.
5. **출발 방향**은 현재 DA의 `Use Runtime Start=True` 때문에 패드 회전보다 `Runtime Start Transform → Rotation → Yaw(Z)`가 우선이다. Camp는 `Data/Missions/DA_Mission_Story_Endgame_Test` → Mission Definition → Runtime Placement에서 변경하고 DA도 저장한다. 패드를 돌리는 것만으로 출발 방향이 바뀐다고 가정하지 않는다.
6. 같은 맵에 패드가 여러 개면 DA Runtime Start Transform의 Location도 원하는 패드 근처로 맞춘다. 이 좌표에 가장 가까운 패드를 고른다. 패드가 하나면 위치 이동만으로 출격점이 따라간다.
7. FrontEnd에서 해당 미션을 다시 출격해 패드 위 시작·방향·벽 겹침/주행·신호·피격을 확인한다. LOS는 BP_LOS 고정 관찰/착지 수업이 별도 예외다.

| Blueprint | 역할 |
|---|---|
| `/Game/Drone/Managers/BP_DroneMissionManager` | 선택한 Mission Definition의 순서형 목표, 진행 수량, 제한 시간, 성공·실패, Story Fact를 관리한다 |
| `/Game/Drone/Managers/BP_DroneMissionTargetManager` | 맵에 직접 배치. 스포이드로 고른 대상과 실제 미션 판정·나침반 마커를 연결한다 |
| `Blueprints/Managers/BP_DroneMissionPlayerController` | 출격 Drone과 위 Manager를 생성하고 Mission HUD·결과 Flow를 연결한다 |
| `Blueprints/Managers/BP_DroneMissionGameMode` | Story/Test Mission 맵에서 위 PlayerController를 사용하게 하는 GameMode다 |
| `Blueprints/Triggers/BP_MissionObjectiveTrigger` | Box Overlap을 Mission Objective Event로 보고한다 |
| `Blueprints/Triggers/BP_MissionFailureTrigger` | 허용한 Actor가 Box에 들어오면 Mission을 실패시킨다 |
| `Blueprints/Triggers/BP_MissionReturnZone` | 현재 출격한 플레이어 Drone의 귀환을 보고한다 |
| `Blueprints/Targets/BP_MissionDamageTarget` | 기본 체력 100, 피해·사망 Delegate와 파괴 연출 Event를 가진 교체 가능한 Greybox 표적이다 |
| `Blueprints/Tutorial/BP_TutorialHoverZone` | 영역 안에서 저속·수평 상태를 연속 유지하면 `Hover Maintained` 목표를 보고한다 |
| `Blueprints/Tutorial/BP_TutorialObserverLesson` | 첫 수업만 고정 관찰 시점에서 이륙→전진→후진→실제 착지4단계를 보고한다 |

Blueprint는 빈 표시용 껍데기가 아니다. 공통 판정은 C++ 부모 클래스에 있고 각 BP는 맵 배치와 기본값 조정을 위한 프로젝트 자산이다. Mesh, VFX, Sound, 최종 Mission 수치와 연출은 파생 BP 또는 Instance에서 설정한다.

## 폴더 계약

```text
/Game/Drone/Managers
├─ BP_DroneMissionManager
└─ BP_DroneMissionTargetManager

/Game/Drone/Mission
└─ Blueprints
   ├─ Managers
   │  ├─ BP_DroneMissionPlayerController
   │  └─ BP_DroneMissionGameMode
   ├─ Triggers
   │  ├─ BP_MissionObjectiveTrigger
   │  ├─ BP_MissionFailureTrigger
   │  └─ BP_MissionReturnZone
   ├─ Targets
      └─ BP_MissionDamageTarget
   └─ Tutorial
      ├─ BP_TutorialHoverZone
      └─ BP_TutorialObserverLesson

/Game/Drone/Data/Missions
└─ DA_Mission_...              # 목표 순서와 Mission 데이터

/Game/Drone/Maps/TestMap       # 기능 시험 맵
/Game/Drone/Maps/Lvl_Battlefield   # M1 역할 확정
/Game/Drone/Maps/Lvl_MilitaryBase  # 원본 지역 보존
/Game/Drone/Maps/Missions/Lvl_Story02_Intercept
/Game/Drone/Maps/Missions/Lvl_Story03_VeilBreaker
/Game/Drone/Maps/Lvl_MilitaryCamp  # M4 역할 확정
```

Mission의 규칙과 맵 배치를 분리한다. “차량 파괴 1회”는 DA의 Objective Rule, 어떤 차량인지는 맵의 스포이드 연결 또는 기존 Actor Tag가 담당한다. Data Asset은 여러 맵에서 공유되므로 맵 액터 스포이드를 DA 안에 넣지 않는다.

## 스포이드 목표 연결과 나침반

필요한 이유는 DA의 Tag 문자열과 맵의 실제 대상을 따로 고치다가 서로 달라지는 일을 줄이기 위해서다. 규칙은 DA에, 월드 액터 참조는 배치한 매니저에 둔다.

담당 클래스는 `ADroneMissionTargetManager`(선택 대상/표시 캐시) → `ADroneMissionDirector`(선택 대상 사건 검증/코스 연결) → `UDroneFlightHUDWidget`(나침반 렌더)다. 헤더에는 편집 가능한 TargetBindings·MissionId·색/표시 옵션을, CPP에는 캐시 갱신·기존 Tag 폴백·방위 계산/마커 숨김을 추가했다. 아래 BP 설정에는 C++ 수정이 필요 없다.

### 바로 사용하는 순서

1. 사용할 미션 맵에 `/Game/Drone/Managers/BP_DroneMissionTargetManager`를 **1개 배치**한다. 기존 `BP_DroneMissionManager`(Director)는 Controller가 만들므로 추가로 배치하지 않는다. 팀원 Production 맵을 시험용으로 저장하지 않는다.
2. 배치한 인스턴스의 **Details → Drone → Mission Targets → Target Bindings**에서 `+`를 누른다. BP Class Defaults가 아닌 레벨 인스턴스에서 설정해야 스포이드가 나온다.
3. DA `ObjectiveRules`에서 바꿀 목표의 **ObjectiveId**를 복사한다. 또는 기존 **TargetId**로 연결해도 된다. 둘 다 쓰면 둘 모두 일치해야 한다. 맵을 여러 미션이 공유하면 매니저의 `MissionId`도 지정한다.
4. 그 항목의 **Targets → + → 스포이드**로 차량/포탑/배달 받침/Trigger/레이더/코스 등 **실제 사건을 보고하는 액터**를 찍는다. 여러 대상이면 배열에 각각 추가한다. 선택 액터에 같은 Tag를 따로 붙이지 않아도 된다.
5. 기본 `bOverrideMissionTarget=True`면 그 목록만 실제 미션 대상으로 인정한다. 이전 Tag를 가진 다른 물체를 파괴해도 진행하지 않는다. 명시적 항목의 Targets가 비어 있으면 잘못된 옛 대상으로 대체하지 않고 진행을 막는다.
6. 출격하면 HUD 상단 나침반에 금색 마름모·거리/이름이 나온다. 정면=중앙(12시), 오른쪽/왼쪽=해당 방위, 표시 범위 밖/뒤=가장자리 방향 표시다. 기체 Yaw 기준으로 기존 나침반 눈금과 같은 좌표계를 쓴다.
7. 대상을 움직이면 마커도 따라가고, HP0/액터 제거·목표 변경/미션 종료 때 해당 마커가 사라지거나 다음 대상으로 바뀐다. 코스 액터는 코스 중심 대신 현재 통과할 Gate를 가리킨다. 코스 스포이드 교체는 실제 Lap Recorder도 같은 코스로 연결한다.

### 모드와 조정값

| 목적 | 설정 |
|---|---|
| 기존 미션 대상으로 나침반만 빠르게 추가 | 매니저만 배치·TargetBindings는 비움. 기본 Follow Current Objective가 현재 Rule TargetId를 자동 해석 |
| 현재 목표를 스포이드 목록으로 교체 | 해당 ObjectiveId/TargetId + Targets, Override Mission Target=True |
| 판정은 유지하고 참고 마커만 표시 | Override Mission Target=False. ObjectiveId/TargetId 둘 다 비우면 미션 진행 중 상시 참고 표식 |
| 미션 없는 별도 시험에서도 수동 마커 표시 | Follow Current Objective=False, MissionId/항목의 ObjectiveId·TargetId 비움, Targets 지정 |
| 이름/색/거리 | 각 항목 MarkerLabel·MarkerColor, 매니저 ShowDistance |
| 표시 수·검색 간격 | 매니저 MaximumMarkers 기본8(1~16), RefreshIntervalSeconds 기본0.5초. HUD 전체16개 상한·중복 대상 제외 |
| HUD 표시/간격 | 실제 HUD WBP Class Defaults: ShowCompassTargets, CompassTargetVerticalOffset. 나침반 가로 배율은 기존 CompassPixelsPerDegree |

명시적 연결은 선택한 액터를 바꾸는 기능이지 임의 StaticMesh에 체력/정찰/투하 기능을 자동 생성하는 기능이 아니다. 파괴 대상에는 `UDroneHealthComponent`·피해 충돌이, 정찰/투하 대상에는 각각 기존 Recon/Payload Target Component가 필요하다. Trigger는 `bUseOverlappingActorAsEventActor`에 따라 자기 자신/진입 액터 중 누가 사건을 보고하는지 맞춰 찍는다. LOS 특수 수업은 복귀/접지 규칙을 그대로 유지한다.

DA에서 **Event·RequiredProgress·TimeLimitSeconds·순서/분기**를 조정한다. 대상3개를 찍어도 RequiredProgress가1이면 하나로 끝난다. RuntimeSpawnActors는 별개라 기존 기본 표적 생성도 끄려면 해당 DA 배치를 함께 조정한다. BP로 런타임 Targets를 바꿨으면 `RefreshTargets()`를 호출하고, 새로 Spawn한 일반 표적의 체력 이벤트는 `Director.RegisterObjectiveTarget()`에 연결한다. 배치형 기존 표적은 출격 때 자동 구독한다.

### 구조·검증·문제 확인

- 헤더/CPP: `ADroneMissionTargetManager`가 레벨 액터 참조/표시 캐시를 소유하고 `ADroneMissionDirector`가 같은 목록으로 사건을 검증한다. `UDroneFlightHUDWidget`의 HudKit Paint가 기존 나침반 위에 그린다. 맵/DA/배치 액터의 Tags를 몰래 수정하지 않는다.
- 테스트 맵: `/Game/Drone/Maps/TestMap/Lvl_MissionCompassTest`. 직접 Play→UGV 선택/출격. 앞 A/B는 태그 없이 스포이드로 연결됐고 뒤 DECOY는 옛 태그가 있지만 대상이 아니다. A/B 파괴 시 진행1/2→성공, 별도 귀환 없음. 데모 DA는 로비 숨김·기존 수업/Story 진행과 분리했다.
- 정상: A 정면 마커·B 우측 마커, 90° 돌면 A는 좌측, A 파괴 후 B만 남고 B 파괴 후 성공/마커0. 실제 손 조종·사격 감도 확인은 자동 순간이동/직접 피해 검사와 별개다.
- 표시가 없으면 Enabled·MissionId/ObjectiveId 철자·Targets(None 여부)·Follow Current Objective·현재 미션 Active 여부·실제 HUD의 HudKit 사용을 확인한다. 대상 삭제/HP0도 표시하지 않는다. 자동 방식은 TargetId가 비어 있으면 임의로 맵의 첫 액터를 고르지 않는다.
- 성능: Actor Tick 없이 목표 사건/Spawn 알림과0.5초 타이머로 캐시한다. HUD는 매니저를1초 간격으로 찾고, 프레임에는 제한된 대상 좌표만 읽는다. 가까운 방향의 이름은 겹치는 글자를 생략하고 마커는 유지한다. 전체 맵 매 프레임 검색·Trace/거리별 재질 생성은 하지 않는다.
- 자동 검사: `Drone.Mission.CompassBearing / TargetPickerBinding / CompassTargetMapPIE.1280 / CompassTargetMapPIE.1920`. 실제 판정·수치는 WORKLOG 정본이다. 생성 도구 `BuildDroneMissionCompassTest.py`는 새 BP/DA/시험장만 만들고 기존 맵/BP를 재생성하지 않는다.

## 새 Mission 맵 연결 순서

1. 기존 Production Training 맵이 아닌 별도 Story 또는 Test 맵을 연다.
2. `World Settings → GameMode Override`를 `BP_DroneMissionGameMode`로 지정한다.
3. Mission Definition DA를 `/Game/Drone/Data/Missions`(하위 폴더 포함)에 만들고 고유 `MissionId`, `MissionMap`, `LobbyCategory`, 허용/기본 기체와 `ObjectiveRules`·시작/성공/실패 규칙을 지정한다. **C++ 기본 목록을 수정하지 않아도 로비 Catalog에 자동 등록된다.**
4. 맵에 필요한 Trigger와 Damage Target을 배치한다.
5. 위 매니저에 스포이드로 대상을 지정하거나, 기존 방식이면 Rule `TargetId`와 같은 Tag를 대상 Actor에 넣는다.
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

기존 Objective Event `Training Lap`, `Recon Scan`, `Payload Delivered`, `Target Destroyed`, `Jamming Exited`, `Jammer Disabled`, `Return To Base`, `Hover Maintained`, `Manual`을 유지하고, 첫 고정 관찰 수업 전용으로 `Tutorial Take Off / Tutorial Forward / Tutorial Backward / Tutorial Landed`를 추가했다. 이4개는 `BP_TutorialObserverLesson`이 순서·조건을 확인해 보고한다. 수업을 단순 Overlap으로 완료시키거나 다른 미션 Event를 억지로 재사용하지 않는다.

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

예외: 새 첫 `기초 조종` 수업(`Mission.Tutorial.Hover`)은 고정 시점·출발점으로 재출격하고 전용4목표를 처음부터 다시 시작한다. 후진/착지 단계만 남긴 채 이륙하지 않은 상태에서 시작하지 않도록 한 수업 전용 규칙이며 다른 미션의 진행 보존 정책은 바꾸지 않는다.

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

### 실제 미션맵 역할·승인된 박스 치환

| 지역 맵 | 확정 역할·작업 대상 | 보존/보류 |
|---|---|---|
| `/Game/Drone/Maps/Lvl_Battlefield` | M1 골든 타임. `M_net`~`M_net8` 모두8개를 원래 위치·폭·높이 기준의 물리 그물로, `M_Target`을 구급품 전달 지점으로 사용 | 기존 적·차량포탑·별도로 배치된 PayloadTarget은 보존 |
| `/Game/Drone/Maps/Lvl_MilitaryBase` | M2 길목 차단·M3 보급 차단. `M_Turret1`은 설치형 무인 자동포탑, **숫자 없는 `M_Radar` 한 개만** 재밍 Radar | `M_Target` 역할 미확정으로 원래 박스 보존. `M_Radar2/3`·`M_Radar_Tower`3개·기존 적/포탑도 임의 삭제/교체하지 않음 |
| `/Game/Drone/Maps/Lvl_MilitaryCamp` | M4 최종 타격 | 확인된 박스 치환 대상 없음. 최종 타격 목표/Sequence는 별도 조립 |

승인 배치 도구는 `Tools/AssetMigration/ApplyStoryMapActors.py`다. 기본 `DRONE_STORY_ACTORS_MODE=audit`는 읽기 목록이며, `apply`만 승인된 Actor를 생성/저장하고 `verify`는 재조회한다. 원본 박스는 삭제하지 않고 `Drone/ArchivedMarkers` 폴더·`Drone.Marker.Archived` Tag로 옮겨 숨김/비충돌 보존한다. 새 Actor는 `Drone.StoryActors.V1`·`SourceMarker.<원래라벨>` Tag로 소유권을 표시해 재실행 중복을 막으며 원본 맵 백업은 `Saved/Automation/CodexStoryActors`에 둔다. 실제 저장·재조회 성공 여부는 STATUS·WORKLOG를 확인한다.

그물은 원래 박스 Scale을 Actor Scale로 복사하지 않고 폭/높이→Corner로 바꾼다. 조정/수동 시험은 [물리 가이드](DRONE_CHAOS_DATAFLOW_PLAN.md#현재-pbd-그물-배치조정)를 따른다. 설치형은 `/Game/Drone/AI/AutomaticTurrets/Blueprints/BP_AutoTurret_Emplaced`로 **병사가 점유하는 MG와 별개**다. Battlefield 전달 표적 Tag는 `Story.M1.Payload.Target`이며 최종 Rule의 TargetId도 정확히 일치시켜야 한다.

**박스 치환 도구와 현재 미션 배치 도구는 별개다.** 현재 DA는 위 Story 맵 표를 따르고, 예전 격리 TestMap은 보존한다. 박스 치환 도구만으로 DA/목표/GameMode/PlayerStart를 바꾸지 않는다. LOS 외 귀환은 넣지 않는다. MilitaryBase의 미확정 `M_Target`을 차량 도착지라고 추정하지 않는다.

### 재밍 Radar BP 설정·시험

`/Game/Drone/Signal/Blueprints/BP_DroneJammingRadar`는 **외형 슬롯이 비어 있는 배치형 Radar**다. BP Components의 `RadarMesh`에 Static Mesh를 넣고 Component 위치·회전·크기를 조정한다. 시설 위치와 기지 범위 중심을 분리하므로 Actor Scale로 범위를 키우지 말고 `Drone > Jamming > Radar`의 아래 값을 쓴다.

| 값 | 조정 방법 |
|---|---|
| `CoverageCenterOffset` | Actor 로컬 기준 기지 범위 중심(cm). Viewport 위치 Widget으로 조정 |
| `JammingRadiusCm` | 수평 원형 영향 반경. 기본15000cm=150m |
| `JammingHalfHeightCm` | 영향 범위 중심 위/아래 높이. 기본3000cm |
| `FullStrengthRadiusCm` | 실제 Radar 시설에 가까워 최대 세기가 되는 반경. 기본2500cm |
| `RefreshIntervalSeconds` | 겹친 Drone 갱신 주기. 기본0.1초 |

맵 Instance 값이 BP 기본값보다 우선이다. MilitaryBase 치환은 표식 분포에서 계산한 기지 중심/반경을 사용하므로 기본150m와 다를 수 있다. 런타임 범위 변경은 `Configure Coverage`, 강도는 부모 `Set Normalized Jamming Strength`, 전원은 `Set Jammer Active`, Mission 무력화는 `Disable Jammer`를 사용한다. 마지막 두 함수의 Off/무력화는 기존 `Jammer Disabled` Event를 보고하므로 단순 외형 토글로 쓰지 않는다. 이 BP에 최종 메시를 넣는 것만으로 자동 파괴/피격 체력이 생기는 것은 아니며, 파괴가 필요하면 별도 피해 처리에서 `Disable Jammer`를 호출하도록 연결한다.

재밍은 **느려지는 효과가 아니다.** 원거리→근거리로 화면 Noise가 강해지고 링크 손실 때 `NO SIGNAL`과 조종 차단을 표시한다. 잔여 속도·중력 등 실제 물리를 강제로0으로 만들지 않는다. 손실/복원 경계는 Drone의 Signal Component `ConnectionLossThreshold`(기본0.95)·`ConnectionRecoveryThreshold`(0.88)로 구분해 경계 떨림을 줄인다. FiberOptic은 재밍 면역이라 Noise/링크 차단을 받지 않는다.

일반 Drone으로 범위 밖→가장자리→시설 근처→범위 밖을 이동해 Noise·NO SIGNAL·복원을 확인한다. 이어 Radar Off→On, FiberOptic 같은 경로를 시험하고 이동 속도 배율이 줄지 않는지 확인한다. 자동화 대상은 `Drone.Signal.StageContract / RadarCoverage / ControlLink`이며 현재 Pass 여부와 화면 검증은 STATUS·WORKLOG를 따른다. 화면/실제 입력은 수동 확인 대기다.

## Tutorial Mission 시험 맵

`/Game/Drone/Maps/TestMap/Lvl_DroneTutorialMissionTest`는 보존된 공용 Greybox 맵이며 Production Training과 분리되어 있다. 현재 첫 수업은 아래 Observer 전용 맵으로 바뀌었고 나머지 수업은 기존 독립 맵을 사용한다. 공용 시험장의 과거 호버 Zone을 고쳐 새 수업을 덮어쓰지 않는다.

| Mission Definition | 허용 기체 | 목표 순서 |
|---|---|---|
| `DA_Mission_Tutorial_Hover` | Scout | 고정 관찰 시점 이륙→전진→후진→착지 (`TestMap/Tutorial/Lvl_Tutorial_Observer_Test`) |
| `DA_Mission_Tutorial_Payload` | Drop | 지정 표적 물자 투하 → 즉시 완료(귀환 없음) |
| `DA_Mission_Tutorial_FPV` | FPV Strike | Arm 후 표적 파괴; 자폭 기체이므로 별도 귀환 없음 |

기존 `BP_TutorialHoverZone`의3초 호버 판정은 별도 기능 시험용으로 보존한다. 새 첫 수업의 BP 위치·4단계 판정값·고정 카메라·접지/후진/재출격 확인은 [Training 가이드의 첫 수업 절](../tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md#첫-수업-고정-관찰-시점-기초-조종)을 따른다. 이전 Hover Zone 수치나 과거 공유맵 수동 순서를 새 첫 수업의 완료 기준으로 재사용하지 않는다.

현재 로비는8수업 ID/순서와 기존 Training을 유지하며 첫 항목을 `기초 조종`으로 표시한다. 허용 기체는 각 DA의 AllowedDroneIds를 따르고 기존 첫 수업 ID를 바꾸거나9번째 수업으로 중복 추가하지 않는다.

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
