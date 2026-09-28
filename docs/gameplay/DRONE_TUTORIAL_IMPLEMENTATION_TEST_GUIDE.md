# Drone Tutorial 구현·테스트 가이드

기준일: 2026-09-29. Figma `Project:Droner`의 Tutorial 8개 훈련을 기준으로 작성했다. Figma 원본은 수정하지 않았으며, 아래에서 구현 완료와 후속 작업을 구분한다.

## 1. 목표와 안전 경계

최종 Tutorial 순서는 다음과 같다.

1. 1-1 호버링
2. 1-2 전진
3. 1-3 회전
4. 1-4 게이트 자유비행
5. 2 자폭 드론
6. 3 드랍 드론
7. 4-1 UGV 적 NPC 처치
8. 4-2 고정형 포탑 처치

각 수업은 `조작키·목표 브리핑 → 시작 → 플레이 → 클리어 타임 → 다음 수업` 구조로 만든다. 마지막에는 Tutorial 전체 완료 UI를 표시한다.

작업 중 다음 경계는 지킨다.

- Production `/Game/Drone/Maps/Lvl_DroneTraining`은 팀원 작업 보호 대상이다. 자동 생성·저장·덮어쓰기에 사용하지 않는다.
- 기능은 `/Game/Drone/Maps/TestMap`에서 먼저 검증한다.
- 목표 규칙은 Level Blueprint에 직접 쌓지 않고 `UDroneMissionDefinition` Data Asset에 둔다.
- 맵 Actor는 안정적인 Actor Tag로 Mission Rule과 연결한다.
- 구매 에셋은 외형만 교체한다. 판정·체력·입력·Mission Flow는 프로젝트 코드가 소유한다.
- 수치와 입력은 Greybox 기본값이다. 사용자가 화면에서 확인하기 전 최종값으로 확정하지 않는다.

## 2. 현재 있는 것과 없는 것

| 항목 | 현재 상태 |
|---|---|
| 호버링 | `DA_Mission_Tutorial_Hover`, `BP_TutorialHoverZone`, 3초 판정과 귀환까지 있음 |
| 전진 | `DA_Mission_Tutorial_Forward`와 공용 Trigger Station 구현 |
| 회전 | `ADroneTutorialHeadingZone`, `BP_TutorialHeadingZone`, `DA_Mission_Tutorial_Heading` 구현 |
| 게이트 | `ADroneTrainingCourse`, Ring 4개, 순서·정방향 판정과 `DA_Mission_Tutorial_GateFlight` 연결 |
| 자폭 | `DA_Mission_Tutorial_FPV`, Arm/Disarm, 충돌 피해와 표적 파괴까지 있음 |
| 드랍 | `DA_Mission_Tutorial_Payload`, 투하·적중·귀환과 예비 Carryable까지 있음 |
| UGV 이동/시점 | 지면 추종, 차체 이동, 상부 `Turret`/`Turret_Swivel` 조준, 총·유탄 Muzzle Anchor까지 있음 |
| UGV 무장 | `UDroneGroundWeaponComponent`, 직사 총탄과 중력·반경 피해 유탄 구현 |
| 적 NPC/고정포탑 | 체력 100 NPC, 자동포탑과 공용 Damage Target 기반은 있음 |
| 공통 Mission UI | 현재 목표·진행·역할 안내와 성공/실패·재시도·로비 복귀는 있음 |
| Tutorial 전용 UI | 단계별 브리핑, 클리어 타임, 전체 8개 진행도·완료 UI는 없음 |
| 전체 환경 | 현재 맵은 평면 Greybox다. Figma의 Warehouse 메모는 아직 미반영 |

현재 기능 시험 맵은 다음 두 개를 구분한다.

- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialMissionTest`: Tutorial 8개 독립 Mission Flow와 Station 시험
- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest`: Gate/Lap·역할 기능·HUD 시험

전체 8개 Station은 `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialMissionTest`에 통합했다. 별도 `Lvl_DroneTutorialFullCourseTest` 맵은 만들지 않았다.

## 3. 공통 구현 구조

### C++가 담당할 것

- 반복 가능한 판정: 호버 안정성, 목표 Heading, 총·유탄 피해, 클리어 시간
- Mission 사건 전달: `ReportObjectiveEvent`
- 체력·죽음·중복 완료 방지
- 입력 Action을 현재 Drone Capability에 따라 한 곳에서 분기
- 자동화에서 읽을 수 있는 Getter와 안정적인 상태

### Blueprint가 담당할 것

- Box 크기, 위치, 목표 방향과 허용 오차
- Mesh, Material, Niagara, Sound와 안내 표식
- WBP 레이아웃과 애니메이션
- 맵에 배치한 Instance의 Tag와 수치 조정

### Data Asset이 담당할 것

각 수업은 독립 `UDroneMissionDefinition`으로 먼저 만든다. 독립 실행·재시도·자동화가 안정된 뒤 전체 8개 순차 진행 Controller를 붙인다.

필수 필드는 다음과 같다.

| 필드 | 설정 원칙 |
|---|---|
| `MissionId` | 저장 뒤 바꾸지 않는 안정적인 ID |
| `MissionMap` | Test Map을 먼저 지정 |
| `AllowedDroneIds` | 해당 수업에서 선택 가능한 기체만 넣음 |
| `DefaultDroneId` | 허용 목록 안의 한 기체 |
| `ObjectiveRules` | 실제 완료 순서대로 배열에 추가 |
| `Event` | 실제 발생 사건과 같은 열거형 |
| `TargetId` | 비우거나 맵 Actor Tag와 정확히 일치 |
| `RequiredProgress` | 필요한 횟수. 기본 1 |
| `TimeLimitSeconds` | 0이면 무제한. 처음에는 넉넉하게 잡음 |
| `SuccessRuleId`/`FailureRuleId` | Tutorial 공통 Rule ID를 사용하되 최종 명칭은 데이터에서 관리 |

## 4. 수업별 구현 방법

### 1-1 호버링 — 현재 구현 검증

왜 필요한가: 상승·하강 뒤 기체를 안정적으로 유지하는 기본 조작을 확인한다.

- 담당 클래스: `ADroneTutorialHoverZone`
- Blueprint: `/Game/Drone/Mission/Blueprints/Tutorial/BP_TutorialHoverZone`
- Data Asset: `DA_Mission_Tutorial_Hover`
- 기본 판정: 전체 속도 75cm/s 이하, 수직 속도 40cm/s 이하, Pitch/Roll 15도 이하를 3초 연속 유지
- Event: `HoverMaintained`
- Tag: `Tutorial.Hover.Zone`

Editor 시험:

1. FrontEnd에서 `튜토리얼 1 - 호버링`을 선택한다.
2. Scout만 선택 가능한지 확인한다.
3. Hover Zone 안에서 입력을 놓고 3초 유지한다.
4. 흔들리거나 Zone을 나가면 시간이 초기화되는지 확인한다.
5. 완료 뒤 Return Zone에 들어가 성공 화면을 확인한다.

정상 결과는 `호버 목표 완료 → 귀환 목표 활성화 → 성공 화면`이 한 번씩만 발생하는 것이다.

### 1-2 전진 — 공용 Trigger로 먼저 구현

왜 필요한가: 단순 입력 존재가 아니라 전진해서 지정 위치에 도달하는 동작을 검증한다.

새 C++ 클래스 없이 공용 Trigger로 구현했다.

1. `DA_Mission_Tutorial_Forward`를 만든다.
2. Scout만 허용한다.
3. Rule Event는 `Manual / Blueprint`, TargetId는 `Tutorial.Forward.Goal`로 둔다.
4. 맵에 `BP_MissionObjectiveTrigger`를 시작점 전방에 배치한다.
5. Trigger Actor Tag에 `Tutorial.Forward.Goal`을 넣는다.
6. Trigger 설정은 `Report Objective Event`, `Manual`, `Active Player Drone`, `Use Overlapping Actor As Event Actor = false`, `Trigger Once = true`로 둔다.

첫 시험에서는 전방 15~25m 정도에 큰 Box를 두고 고도 유지까지 요구하지 않는다. 전진 완료가 안정된 뒤 중간 Gate나 고도 범위를 추가한다.

부정 시험:

- Trigger 옆을 지나가면 완료되지 않아야 한다.
- 다른 Actor가 들어가도 완료되지 않아야 한다.
- 완료 뒤 다시 들어가도 두 번 진행되지 않아야 한다.

### 1-3 회전 — 목표 Heading Actor 추가

왜 필요한가: 위치 Trigger만으로는 실제 Yaw 회전을 배웠는지 확인할 수 없다.

구현 클래스는 `ADroneTutorialHeadingZone`이다.

헤더에 둘 값:

- `UBoxComponent* HeadingBox`
- `TargetHeadingDegrees`
- `HeadingToleranceDegrees`
- `RequiredHoldSeconds`
- `EvaluationIntervalSeconds`
- `bResetProgressWhenMisaligned`
- 진행·완료 Delegate와 Getter

CPP 동작:

1. 현재 출격한 플레이어 Drone만 허용한다.
2. Box 안에서 Drone Yaw와 목표 Heading의 최단 각도 차이를 계산한다.
3. 허용 오차 안에서 일정 시간을 유지하면 한 번만 완료한다.
4. 상시 Tick 대신 Box Overlap 중 Timer만 사용한다.
5. 완료 시 Director에 회전 전용 Event를 보고한다.

Event를 새로 만들면 `EDroneMissionObjectiveEvent`의 마지막에 `HeadingAligned`를 추가한다. 기존 저장 Asset의 열거형 숫자를 지키기 위해 중간에 끼워 넣지 않는다.

Blueprint `BP_TutorialHeadingZone`에서는 화살표 Mesh와 목표 방향 색만 설정한다. 기본 후보는 목표 90도, 허용 오차 8도, 유지 1초이며 최종값은 수동 확인 뒤 조정한다.

### 1-4 게이트 자유비행 — 기존 Course 재사용

왜 필요한가: 전진·고도·회전을 한 코스에서 조합한다.

- 담당 클래스: `ADroneTrainingCourse`, `ADroneTrainingGate`
- Event: `TrainingLap`
- Data Asset 후보: `DA_Mission_Tutorial_GateFlight`
- 허용 기체: Scout

맵 설정:

1. `BP_DroneTrainingCourse` 한 개를 배치한다.
2. Spline과 Ring별 Handle을 편집한다.
3. Gate 로컬 `+X`가 진행 방향을 향하는지 확인한다.
4. Mission Rule을 `TrainingLap`, RequiredProgress 1로 설정한다.

현재 Director는 맵에서 처음 찾은 유효 Course 한 개의 Lap Recorder를 구독한다. 같은 맵에 여러 Course를 넣으면 어떤 Course가 선택될지 명시적이지 않으므로, 수업 맵에는 우선 Course 하나만 둔다. 여러 Course가 필요해지면 Mission Definition에 Course ID를 추가하고 Director가 ID로 찾도록 먼저 확장한다.

### 2 자폭 드론 — 현재 구현 검증

- Data Asset: `DA_Mission_Tutorial_FPV`
- 기체: `Drone.FPVStrike.Greybox`
- Event: `TargetDestroyed`
- Target Tag: `Tutorial.FPV.Target`
- 표적: `BP_MissionDamageTarget`, 기본 체력 100
- 임시 조작: Primary로 Arm, Secondary로 Disarm, 충분한 속도로 충돌

시험할 항목:

1. Arm 전 저속·고속 충돌은 자폭 완료가 되지 않는다.
2. Arm 뒤 최소 충돌 속도 이상에서 폭발·피해가 발생한다.
3. 표적 체력이 0이 되면 목표가 한 번 완료된다.
4. 희생형 기체이므로 별도 귀환 목표가 없다.
5. 다른 Tag의 Damage Target 파괴는 현재 목표를 완료하지 않는다.

### 3 드랍 드론 — 현재 구현 검증

- Data Asset: `DA_Mission_Tutorial_Payload`
- 기체: `Drone.Drop.Greybox`
- Event: `PayloadDelivered`
- Target Tag: `Tutorial.Payload.Target`
- 임시 조작: Primary 투하/근처 화물 적재, Secondary 탑뷰

시험할 항목:

1. 허용 기체가 Drop 하나인지 확인한다.
2. 표적 밖에 떨어뜨리면 목표가 완료되지 않는다.
3. 지정 Target에 적중하면 귀환 목표로 넘어간다.
4. 예비 Carryable을 다시 적재·투하할 수 있다.
5. Return Zone 진입 뒤 성공 화면이 한 번만 나온다.

### 4-1 UGV 적 NPC 처치 — 무장 기반부터 구현

현재 UGV에는 `GroundGunMuzzleAnchor`, `GroundGrenadeMuzzleAnchor`와 실제 플레이어 무장이 연결되어 있다.

구현된 C++ 구성:

- `UDroneGroundWeaponComponent`: 탄약, 발사 간격, 사거리, 피해, Projectile Class와 Primary/Secondary 발사 진입점
- `ADronePlayerProjectile`: 플레이어 공격용 충돌·피해 Projectile
- `ADronePlayerProjectile`: Direct 총탄과 Radial 유탄 모드를 함께 소유

NPC 전용 `UDroneNPCWeaponComponent`를 UGV에 그대로 붙이지 않는다. 이 Component는 AI Target과 연사 Timer 계약을 가지고 있으므로 플레이어 입력·Muzzle·무기 전환과 분리한다. Projectile의 공통 이동·충돌 코드는 후속으로 공용 부모에 추출할 수 있다.

Pawn 연결:

1. `GroundDrive` Capability일 때 Ground Weapon을 활성화한다.
2. 기존 `TriggerPrimaryRoleAbility`에서 UGV Primary를 총 발사로 분기한다.
3. `TriggerSecondaryRoleAbility`에서 UGV Secondary를 유탄으로 분기한다.
4. 총은 `GroundGunMuzzleAnchor`, 유탄은 `GroundGrenadeMuzzleAnchor` Transform을 사용한다.
5. 카메라가 아니라 상부 조준 Pivot의 Forward를 발사 방향 기준으로 사용한다.

Mission 설정:

- Data Asset 후보: `DA_Mission_Tutorial_UGV_NPC`
- Event: `TargetDestroyed`
- TargetId: `Tutorial.UGV.NPC`
- 대상: 별도 시험용 적 NPC 한 명, Actor Tag 일치

NPC에는 이미 `UDroneHealthComponent`가 있다. Mission 시작 전에 배치된 대상은 Director가 자동 등록한다. Mission 시작 뒤 Spawn한 NPC라면 `Register Objective Target`을 호출해야 한다.

### 4-2 고정형 포탑 처치

Figma에서도 4-1과 합칠지는 미정이므로 처음에는 별도 Data Asset으로 만든다.

- Data Asset 후보: `DA_Mission_Tutorial_UGV_Turret`
- Event: `TargetDestroyed`
- TargetId: `Tutorial.UGV.Turret`
- 대상: 전용 체력 포탑 또는 `BP_MissionDamageTarget`에 포탑 Visual을 적용한 Greybox

첫 단계에서는 포탑이 반격하지 않아도 된다. `UGV 조준 → 실제 Projectile 명중 → 체력 감소 → 파괴 목표 완료`를 먼저 검증한다. 그 뒤 자동포탑 탐지·반격을 켜서 전투 난도를 추가한다.

## 5. Tutorial 전용 UI 구현

기존 `UDroneMissionObjectiveWidget`과 `UDroneMissionResultWidget`은 유지한다. Tutorial 전용 표현은 Blueprint Widget 또는 얇은 C++ 부모로 추가한다.

권장 WBP:

| Widget | 역할 |
|---|---|
| `WBP_TutorialBriefing` | 수업 이름, 목표, 조작키, 시작 버튼 |
| `WBP_TutorialLessonResult` | 클리어 시간, 재시도, 다음 수업 |
| `WBP_TutorialProgress` | 현재 `n/8`, 완료 수업 표시 |
| `WBP_TutorialComplete` | 전체 완료, 로비 복귀 |

Widget Tick에서 Mission 상태나 Pawn을 매번 찾지 않는다. Director의 `OnMissionSnapshotChanged`, 결과 Delegate와 역할 Component Delegate를 구독한다.

클리어 시간은 Widget이 직접 재지 않는다. Mission 시작 시각과 성공 시각을 Runtime 데이터에서 계산해 결과 Struct로 전달한다. Best 기록 영속화는 화면과 수치가 확정된 뒤 `USaveGame`으로 추가한다.

전체 8개 진행 관리 클래스는 아직 없다. 독립 수업 검증이 끝난 뒤 `UDroneTutorialProgressSubsystem` 또는 기존 `UDroneGameFlowSubsystem`의 Tutorial 전용 데이터로 추가한다. 둘을 동시에 만들지 말고 GameInstance 수명의 소유자 한 곳만 선택한다.

## 6. Test Map 구성 순서

현재 통합 Course Test Map은 다음 원칙으로 평면 Greybox를 구성했다.

1. 바닥, PlayerStart, Directional Light, Sky Light만 둔다.
2. 8개 Station을 충분히 떨어뜨려 배치한다.
3. 각 Station 바닥에 이름과 Actor Tag를 표시한다.
4. NavMesh가 필요한 UGV/NPC 구역만 NavMesh Bounds를 둔다.
5. 모든 표시 Mesh는 Collision과 Navigation 영향을 끈다.
6. Mission Actor와 표적만 필요한 Collision을 가진다.
7. 기능 검증 뒤 Warehouse 벽·기둥·표지판을 추가한다.

권장 공간 구분:

```text
[Spawn/Briefing]
  ├─ Scout: Hover → Forward → Heading → Gate Course
  ├─ FPV: Arm → Damage Target
  ├─ Drop: Carryable → Payload Target → Return
  └─ UGV: Drive → NPC Target → Fixed Turret Target
```

하나의 맵을 여러 Mission Definition이 공유할 때 PlayerStart가 하나면 항상 같은 위치에서 시작한다. 역할별 시작 위치가 필요하면 임의 Teleport를 Level Blueprint에 넣지 말고, Mission ID/Drone ID Tag로 선택하는 프로젝트 소유 Spawn Point Actor를 별도 작업으로 만든다.

## 7. 테스트 계층

### A. Build

새 C++를 추가했으면 Editor를 닫고 `DroneEditor Win64 Development`를 빌드한다. Live Coding 성공만으로 완료 처리하지 않는다.

### B. Asset·Map 검증

Editor를 닫은 상태에서 실행한다.

```powershell
cd C:\URproject\drone
.\Tools\AssetMigration\Invoke-DroneTutorialMissionTest.ps1 -Mode Validate
```

배치를 도구 기준으로 다시 만들 때만 `-Mode Rebuild`를 쓴다. `Rebuild`는 전용 `DroneTutorialMissionTest.Owned` Tag Actor만 대상으로 하며 Production Training 맵에는 사용하지 않는다.

완료 기준:

- Map Check `0 errors / 0 warnings`
- Mission Data Asset Validation 성공
- GameMode가 `BP_DroneMissionGameMode`
- Actor Tag와 Rule TargetId가 일치

### C. 기존 자동화

Session Frontend에서 다음 테스트를 실행한다.

- `Drone.Tutorial.MissionLessonsTestMap`
- `Drone.Mission.FrameworkAssets`
- `Drone.Mission.ObjectiveRules`
- `Drone.Flow.Contract`
- `Drone.Flow.FrontEndContract`
- `Drone.Flow.FrontEndPIE`

새 수업마다 다음 자동화를 추가한다.

1. 판정 단위 테스트: 허용 범위, 경계값, 초기화, 중복 완료 방지
2. Asset 테스트: BP/DA 로드, 부모 Class, 기본값
3. Map 테스트: 필요한 Actor 수, Tag, GameMode, MissionMap 경로
4. PIE 테스트: 실제 입력/Overlap/Projectile로 한 번 완료되는지

자동화는 성공 경로만 보지 않는다. 잘못된 Tag, 잘못된 기체, 역방향 Gate, 범위 밖 Heading, Arm 전 충돌, 빗나간 Payload, 벽에 막힌 Projectile도 확인한다.

### D. 수동 PIE

Mission Flow 전체 확인은 Test Map을 직접 Play하지 않고 `/Game/Drone/Maps/Lvl_DroneFrontEnd`에서 시작한다.

공통 체크:

- 로비에 수업이 표시되는가
- 허용 기체만 선택되는가
- 브리핑 뒤 올바른 맵으로 들어가는가
- 목표 HUD가 현재 Rule과 같은가
- 완료·실패가 한 번만 발생하는가
- Retry가 목표와 Actor 상태를 초기화하는가
- Lobby 복귀 뒤 다음 실행이 오염되지 않는가

### E. 성능 확인

- 호버·Heading 판정은 Overlap 중 저빈도 Timer만 사용한다.
- UI는 Event 기반으로 갱신한다.
- Projectile은 수명과 최대 동시 개수를 제한한다.
- Rain·NPC·Projectile을 함께 켠 최종 Warehouse 맵에서 `stat unit`, `stat game`, `stat gpu`를 비교한다.
- Debug Draw, 진단 로그와 가시화 Actor는 기본 Off로 둔다.

## 8. 기능 하나를 추가할 때의 고정 순서

새 수업은 항상 아래 순서로 작업한다.

1. 왜 필요한지와 완료 조건을 한 문장으로 적는다.
2. 기존 Event/Trigger로 가능한지 먼저 확인한다.
3. 불가능할 때만 새 C++ Actor/Component/Event를 추가한다.
4. Header에 조정값·Getter·Delegate를 추가한다.
5. CPP에 판정·중복 방지·수명주기 정리를 구현한다.
6. Blueprint 자식에서 Visual과 기본값을 설정한다.
7. Test Map에 Actor와 Tag를 배치한다.
8. Mission Definition의 Rule을 연결한다.
9. 단위→Asset→Map→PIE 자동화를 추가한다.
10. FrontEnd부터 수동 플레이한다.
11. 화면 확인 뒤 수치를 조정한다.
12. 문서와 작업 보드를 갱신한다.

## 9. 문제 발생 시 확인 순서

| 증상 | 우선 확인 |
|---|---|
| 목표가 시작되지 않음 | FrontEnd에서 Mission을 선택했는지, Map GameMode가 Mission GameMode인지 |
| Trigger를 지나도 미완료 | Event 종류, Actor Policy, Trigger Once, TargetId와 Actor Tag |
| 다른 표적 파괴로 완료 | 목표 대상 Actor Tag가 중복됐는지 |
| 같은 목표가 두 번 증가 | 같은 Actor 중복 보고, Trigger 중첩, 동적 대상 중복 등록 |
| Gate 완료 안 됨 | 현재 Gate 순서, 로컬 +X 방향, Course 한 개 여부 |
| Heading이 흔들림 | 최단 각도 차이 계산, 허용 오차, 유지 시간, Timer 초기화 |
| UGV 총알이 옆으로 나감 | 차체 Forward가 아니라 상부 Pitch Pivot/Muzzle Anchor Transform을 쓰는지 |
| NPC가 죽어도 미완료 | `UDroneHealthComponent`, Target Tag, Mission 시작 뒤 Spawn 시 Register 호출 |
| Retry 뒤 즉시 완료 | Hover/Heading/Trigger/표적 체력과 Director Binding 초기화 여부 |
| HUD가 오래된 목표 표시 | Widget Delegate 해제·재구독, Snapshot 갱신 여부 |

## 10. 추천 실제 작업 순서

1. 현재 8개 수업을 FrontEnd에서 수동 검증한다.
2. 호버/전진/회전 Trigger 크기와 게이트 위치를 체감에 맞춰 조정한다.
3. UGV 총탄 속도·4발 처치와 유탄 낙차·반경을 화면에서 확인한다.
4. 단계별 브리핑·클리어 타임 UI를 붙인다.
5. 8개 진행도와 전체 완료 UI를 연결한다.
6. 마지막에 Warehouse Greybox를 입히고 전체 회귀·성능 테스트를 한다.

각 단계는 Build, Map Check, 자동화, 수동 PIE가 모두 끝나야 다음 단계로 넘어간다.
