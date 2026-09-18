# NPC 뒤로 걷기 / 사격 정면 증상 인수인계

작성일: 2026-09-18  
목적: 다른 PC 또는 다른 Codex/GPT 대화에서 NPC 보행 방향 문제를 그대로 이어서 점검하기 위한 문서

## 1. 현재 결론

코드 원인과 자동화 회귀는 확보했고 최종 화면 확인이 남았다.

현재 확인된 사용자 증상은 다음과 같다.

- 적 NPC가 이동할 때 몸이 실제 속도 반대 방향을 보던 현상은 자동화에서 Shotgun `worstDot=-1.000`, 최대 1.56~3.95초 연속 역방향으로 재현됐다.
- 순찰·수색·추적의 몸 Yaw를 실제 수평 속도 기준으로 통일한 뒤 실제 맵 회귀는 4회 연속 통과했다.
- 멈춤·재출발에는 `Paused` 영구 정체, 순찰 Task가 전투 MoveTo를 취소하는 소유권 충돌, 성공한 동일 부분 경로를 다시 요청하는 세 경로가 있었고 각각 방지 로직을 넣었다.
- 최종 Editor Build와 관련 회귀는 통과했다. 이후 사용자 화면에서 Shotgun만 느린 주기로 다시 돌았고, 실제 실행 로그에서 Shotgun의 추가 `Gun` 컴포넌트가 Rifle을 물리적으로 막는 두 번째 원인을 확인해 수정했다. 수동 화면 확인 전에는 시각적 해결 완료로 판정하지 않는다.

이 문서는 자동화 수정 근거와 남은 수동 확인을 함께 전달하는 인수인계 문서다. 아래의 `확인된 사실`, `추정`, `다음 점검`을 구분해서 읽는다.

## 2. 확인된 사실

### 2.1 에셋 연결

적 소총/샷건 NPC는 프로젝트 애니메이션 블루프린트를 사용한다.

| 대상 | 에셋 |
|---|---|
| 적 소총 NPC | `/Game/Drone/AI/Blueprints/BP_NPC_Hostile_Rifle` |
| 적 샷건 NPC | `/Game/Drone/AI/Blueprints/BP_NPC_Hostile_Shotgun` |
| 적 공용 AnimBP | `/Game/Drone/AI/Animation/ABP_NPC_Rifle_Greybox` |
| 적 이동 BlendSpace | `/Game/Drone/AI/Animation/BS_NPC_Rifle_Locomotion` |
| 아군 기본 NPC | `/Game/Drone/AI/Blueprints/BP_NPC_Friendly_Base` |
| 아군 기본 AnimBP | `/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed` |

프로젝트 BlendSpace에는 전진/후진/좌우 방향 샘플이 있고, 후진 샘플은 `MF_Rifle_Walk_Bwd`, `MF_Rifle_Jog_Bwd` 계열이다. 적 NPC의 메시에는 에셋 축 보정으로 보이는 `Yaw=-90` 상대 회전이 있으나, 사격 시 정면을 올바르게 보는 현상 때문에 이것을 현재 주원인으로 확정하지 않는다.

### 2.2 실제 코드에서 확인된 회전/이동 설정

`ADroneNPCCharacter`의 기본 이동 설정은 다음과 같다.

- `bUseControllerRotationYaw = false`
- `CharacterMovement->bUseControllerDesiredRotation = false`
- `CharacterMovement->bOrientRotationToMovement = true`
- 기본 회전 속도는 360도/초

즉 일반 이동에서는 `CharacterMovement`가 속도 방향으로 몸을 돌리는 구조다. 단, 대응 상태에서는 AI Controller가 드론 조준 방향 또는 추적 방향으로 몸/컨트롤 회전을 직접 바꿀 수 있다.

`ADroneNPCAIController`는 다음 회전 소유권을 갖는다.

- `UpdatePursuitFacing`: 개인화기 Pursue에서는 `bOrientRotationToMovement=false`로 두고 Controller 한 곳이 계산된 최종 사거리 정지점을 향해 몸 Yaw를 보간한다. Pursue의 `bRequestedMoveUseAcceleration`은 Blueprint 값 `bUseAccelerationForPersonalWeaponPursuitMoves`를 따르며 기본은 `false`다. 순찰·수색 등 비추적 이동은 요청 가속을 유지하고 의미 있는 실제 속도 방향으로 몸과 Controller Yaw를 보간한다. 정지한 전투 상태에서는 드론 조준/엄폐 방향 로직이 회전을 맡는다.
- `UpdatePersonalWeaponFacing`: `DroneDetected`/`UseCover`에서 개인 무기 조준 방향으로 회전을 적용한다. 이동 속도가 있는 동안에는 몸 회전 적용을 건너뛸 수 있다.
- `UpdateDroneGaze`: 전투/수색 상태의 시선 방향을 갱신한다. 순찰 상태에는 적용하지 않는다.

수정 전에는 몸이 드론을 보는 동안 경로 이동이 다른 방향으로 계속되어 실제 역방향 보행이 발생할 수 있었다. 이후 모든 이동을 실제 속도로 보정하는 단계에서는 Shotgun Pursue가 가까운 경로 Segment를 따라 3초 안에 300° 이상 도는 새 피드백이 재현됐다. 최종 구현은 Drone 자체에 큰 허용 반경을 주는 대신 실제 무기 사거리 안의 지상 정지점을 계산하고 작은 도착 반경으로 MoveTo한다. Pursue의 몸과 Bone Gaze는 순간적인 짧은 코너가 아니라 이 공통 최종 목표를 보며, 이동은 Nav가 담당한다. 일반 순찰에는 요청 가속을 유지하고 Pursue에만 기본 직접 요청 속도를 적용한다. 조준 중 이동용 전용 스트레이프 애니메이션은 이번 범위에 포함하지 않았다.

### 2.3 최근 적용된 순찰 태스크 보정

`Source/Drone/AI/DroneNPCPatrolStateTreeTasks.cpp`에 다음 보정이 들어가 있다.

- 순찰 슬롯으로 이동을 시작할 때 목적지 방향을 바라보도록 Pawn/Controller 회전을 초기화한다.
- 순찰 슬롯에 도착했을 때 Smart Object 슬롯의 `Yaw`로 다시 몸을 돌리지 않는다. 슬롯의 Yaw는 터렛/상호작용 방향일 수 있으므로 순찰 보행 방향에 사용하지 않는다.
- PathFollowing 상태가 일시적으로 `Idle`이 되는 경우 즉시 실패하고 슬롯을 반납하지 않는다.
- 같은 목적지에 0.25초 간격으로 재시도하며, 2초 이상 실제 이동하지 못할 때만 실패한다.
- 이 보정은 순찰의 정지/재시작 및 슬롯 방향에 의한 역방향 시작 가능성을 줄인다. `MoveToMGTurret`, `MoveToCover` 등 대응 상태의 슬롯 정렬은 별도 로직을 사용한다.

### 2.4 발사체 충돌 문제는 별도 수정됨

소총/샷건 발사체가 NPC Pawn을 Block하여 NPC가 `stuck` 상태가 되는 문제도 있었다. `DroneNPCProjectile.cpp`에서 프로젝트 NPC를 불필요하게 막지 않도록 수정했다.

이전에는 다음과 같은 로그가 있었다.

```text
BP_NPC_Hostile_Shotgun_C_0 is stuck and failed to move!
Actor: BP_ShotgunPelletProjectile_C_35
```

수정 후 `NPCPerceptionSearchPIE`, `NPCBaseRoutinesPIE`에서 해당 stuck 로그 없이 성공했다. 이 발사체 수정만으로 역방향 보행이 해결된 것은 아니며, 최종적으로는 1절의 속도 기반 몸 Yaw와 MoveTo 소유권 수정까지 적용해 실제 맵 회귀 4/4 Green을 확인했다.

### 2.5 Shotgun 추가 Gun 컴포넌트 충돌과 순찰 회전

후속 수동 PIE의 실제 로그에서 다음 충돌이 확인됐다.

```text
BP_NPC_Hostile_Rifle_C_0 is stuck and failed to move!
Actor: BP_NPC_Hostile_Shotgun_C_0 Component:Gun
```

자동 계측에서도 Shotgun BP의 추가 `Gun` Primitive가 `collision=3 overlap=1 nav=1`로 나타났다. 외형용 부착물이 Pawn 이동과 Nav 장애물이 되어 두 순찰 경로가 교차할 때 Rifle을 막고 회피 회전을 유발한 것이다.

현재 `ADroneNPCCharacter::EnforceVisualOnlyCollision`은 Construction과 BeginPlay에서 이동 Capsule을 제외한 모든 Primitive를 다음처럼 복구한다.

- Collision: `NoCollision`
- Generate Overlap Events: `false`
- Can Ever Affect Navigation: `false`

이 규칙은 팀원이 역할 BP에 별도 Gun/Mesh 컴포넌트를 추가해도 동일하게 적용된다. 런타임 PIE 자동화도 Capsule 외 Primitive가 위 계약을 지키는지 검사한다.

동시에 순찰 중 몸은 50~100cm 단위로 바뀌는 `GetImmediateMoveDestination()`이 아니라 현재 예약된 최종 Smart Object 슬롯을 향하도록 했다. `NPCBaseRoutinesPIE`에는 시작 후 100cm 진행하기 전에 몸이 누적 300도 이상 회전하면 실패하는 회귀가 있다. 최신 빌드에서 `NPCBaseRoutinesPIE`, `NPCGreyboxPIE`, `ShotgunSystemsTestMapPIE`가 모두 성공했고 `stuck` 로그가 없다.

## 3. 런타임 연결 세팅

### 3.1 테스트 맵

우선 아래 맵에서 재현한다.

```text
/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox
```

이 맵은 적 순찰, Smart Object 슬롯, 드론 감지, 소총/샷건 대응을 확인하기 위한 맵이다. 기본 생성 맵이나 별도의 샷건 전용 맵에서만 확인하면 순찰 StateTree와 Smart Object 연결을 놓칠 수 있다.

### 3.2 NPC Blueprint 연결

각 NPC Blueprint의 핵심 연결은 다음과 같다.

```text
NPC Character
 ├─ AIControllerClass: ADroneNPCAIController
 ├─ Auto Possess AI: Placed in World or Spawned
 ├─ AI Perception: Sight 설정 포함
 ├─ SmartObject User/Reservation 컴포넌트
 ├─ WeaponVisualComponent / 무기 부착
 └─ SkeletalMeshComponent
       └─ Animation Mode: Use Animation Blueprint
```

적 소총/샷건 NPC의 Skeletal Mesh는 `ABP_NPC_Rifle_Greybox`를 사용하고, 아군 기본 NPC는 `ABP_Unarmed`를 사용한다. 적 샷건 NPC가 소총용 AnimBP를 공유하는 것은 현재 회색박스 단계의 의도된 연결이며, 샷건 전용 자세/반동 애니메이션은 아직 별도 확정하지 않았다.

### 3.3 AI Perception 기본값

현재 코드/설정 기준의 Sight 기본값은 다음과 같다.

- 감지 반경: 4000 cm
- 시야 상실 반경: 4500 cm
- 주변 시야각: 70도
- 최대 감지 나이: 3초

실제 Blueprint 인스턴스에서 값이 덮어써졌는지 확인한다. 값 자체를 임의로 변경하기 전에 현재 NPC의 `ResponseState`와 Perception 이벤트를 먼저 기록한다.

### 3.4 StateTree와 Smart Object

주요 StateTree는 다음과 같다.

```text
적 순찰: /Game/Drone/AI/StateTrees/ST_NPC_HostilePatrol
아군 기지 루틴: /Game/Drone/AI/StateTrees/ST_NPC_FriendlyBaseRoutine
```

적 순찰의 기본 흐름은 다음과 같다.

```text
ClaimEnemyPatrolSlot
 → MoveToPatrolSlot
 → WaitAtPatrolSlot
 → ReleasePatrolSlot
 → 다시 Claim
```

감지 이후에는 Patrol이 아닌 대응 StateTree 경로로 전환될 수 있다.

```text
DroneDetected
 → PursueDrone 또는 MoveToMGTurret / MoveToCover
 → UseMGTurret / UseCover / Search
 → Return 또는 Patrol
```

Smart Object Activity Tag 예시는 다음과 같다.

```text
Drone.SmartObject.Activity.EnemyPatrol
Drone.SmartObject.Activity.FriendlyBasePatrol
Drone.SmartObject.Activity.Ambient
Drone.SmartObject.Activity.Cover
Drone.SmartObject.Activity.MGTurret
```

순찰 슬롯의 `Yaw`는 순찰 보행 방향으로 사용하지 않는다. 터렛/엄폐 슬롯은 상호작용 방향을 위해 슬롯 Yaw 정렬을 사용할 수 있으므로, 문제 재현 시 순찰 이동과 대응 이동을 분리해서 기록한다.

## 4. 왜 사격 시 정면을 보는데 보행은 뒤로 보이는가

사격 방향과 보행 애니메이션 방향은 같은 값에서 나오지 않을 수 있다.

```text
사격 방향
  = 무기 조준점 / 드론 위치 / Controller의 조준 회전

보행 방향
  = CharacterMovement 속도 벡터
  + Pawn Actor Rotation
  + AnimBP의 Speed/Direction 입력
```

따라서 다음 두 상황을 구분해야 한다.

1. `ActorForward`와 `VelocityDirection`의 내적이 음수다.
   - 실제 Pawn 몸이 이동 속도의 반대 방향을 보고 있다.
   - 대응 상태의 조준 회전과 경로 이동 회전의 소유권 충돌 가능성이 높다.

2. `ActorForward`와 `VelocityDirection`의 내적은 양수인데 애니메이션만 후진 샘플이다.
   - 실제 이동은 정상인데 AnimBP의 `Direction` 계산, 부호, 기준 회전, BlendSpace 연결이 잘못되었을 가능성이 높다.

AnimBP 그래프의 BlendSpace 핀 연결은 Python 점검만으로 링크를 확정하지 못했다. Actor 전방/실제 속도 자동화는 최종 Green이므로, 수동 화면에서 애니메이션만 역방향으로 보일 경우 `ABP_NPC_Rifle_Greybox`를 직접 Debug하여 `Speed`, `Direction`, BlendSpace의 X/Y 입력을 확인한다.

## 5. 다음 담당자가 반드시 기록할 값

PIE에서 문제 NPC를 선택하고 다음 값을 같은 프레임에 기록한다.

```text
ResponseState
PathFollowingStatus
ActorLocation
ActorRotation.Yaw
ActorForwardVector
Velocity
VelocityDirection
Dot(ActorForwardVector, VelocityDirection)
AnimBP Speed
AnimBP Direction
BlendSpace X
BlendSpace Y
현재 StateTree State
현재 Smart Object 슬롯 태그/슬롯 Yaw
```

간단한 판정 기준:

| 관찰값 | 판단 |
|---|---|
| `Dot < 0` | Pawn/AI 회전이 이동 속도의 반대 방향. 대응 상태 회전 소유권 또는 이동 목표 전환을 점검 |
| `Dot > 0`, AnimBP Direction이 약 ±180 | AnimBP Direction 기준 회전/부호/핀 연결 점검 |
| `DroneDetected` 또는 `UseCover`에서 이동 중 | 조준 방향과 경로 방향이 다른 설계인지 먼저 결정 |
| `Patrol`인데 슬롯 Yaw로 몸이 돌아감 | 순찰 태스크 또는 Blueprint에서 슬롯 정렬을 다시 적용하는 연결을 점검 |
| `PathFollowingStatus=Idle`이 반복되고 속도가 0 | Navigation/Smart Object 예약/충돌 문제를 별도로 점검 |

## 6. 에디터에서 재현하고 확인하는 순서

1. Unreal Editor에서 `Lvl_NPCSmartObjectGreybox`를 연다.
2. PIE를 시작한다.
3. 문제가 나타나는 적 NPC를 선택한다.
4. `ABP_NPC_Rifle_Greybox`의 AnimBP Debug 대상에 해당 NPC를 지정한다.
5. NPC가 `Patrol`일 때와 `DroneDetected` 이후를 각각 캡처한다.
6. AnimGraph의 `BS_NPC_Rifle_Locomotion` 노드에서 X/Y 입력을 확인한다.
7. 같은 순간에 ActorForward와 VelocityDirection을 비교한다.
8. `Dot < 0`이면 StateTree/AI Controller 회전 로직을 우선 점검한다.
9. `Dot > 0`인데 후진 애니메이션이면 AnimBP의 Direction 계산을 우선 점검한다.
10. 확인 전에는 StateTree의 상태 전환 간격, 슬롯 Yaw, BlendSpace 샘플을 임의로 여러 개 동시에 바꾸지 않는다.

현재 개발 빌드는 수동 재현용으로 적 NPC마다 0.5초 간격의 진단 로그를 남긴다.

```text
[NPC-STATE] 상태 전환, 감지 대상, Move 상태
[NPC-MOVE] 몸 Yaw, 실제 속도 Yaw/속도, 즉시 Nav 방향, 예약 최종 슬롯 방향/거리
[NPC-COLLISION-FIX] 외형 Primitive에서 복구한 잘못된 충돌·Overlap·Nav 설정
```

맵을 45~60초 실행한 뒤 종료하고 `D:\JGY\project\drone\Saved\Logs\Drone.log`에서 위 태그와 `is stuck and failed to move`를 함께 검색한다. 화면 해결을 확인하면 `bEnableMovementDiagnostics` 기본값을 꺼 로그 비용을 제거한다.

## 7. 자동화 검증 명령

### 빌드

```powershell
& 'C:\Program Files\Epic Games\UE_5.8\Engine\Build\BatchFiles\Build.bat' DroneEditor Win64 Development '-Project=C:\URproject\drone\Drone.uproject' -WaitMutex -NoHotReloadFromIDE
```

### Smart Object 기본 루틴 PIE 테스트

```powershell
$editor='C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor-Cmd.exe'
$project='C:\URproject\drone\Drone.uproject'
& $editor $project /Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox -unattended -nop4 -nullrhi -nosound '-DisablePlugins=ModelContextProtocol,EditorToolset,AutomationTestToolset,UMGToolSet,StateTreeToolset,AIModuleToolset' '-ExecCmds=Automation RunTests Drone.AI.NPCBaseRoutinesPIE' '-TestExit=Automation Test Queue Empty' '-ReportExportPath=C:\URproject\drone\Saved\Automation\PatrolWalkFix2' '-abslog=C:\URproject\drone\Saved\Logs\PatrolWalkFix2.log'
```

최근 결과는 `NPCBaseRoutinesPIE` 성공이다. 단, `-nullrhi` 자동화 테스트는 실제 애니메이션 포즈를 볼 수 없으므로 “시각적으로 앞으로 걷는다”의 증거가 아니다.

## 8. 관련 파일과 로그

Unreal 프로젝트:

```text
C:\URproject\drone
```

주요 소스:

```text
Source/Drone/AI/DroneNPCCharacter.cpp
Source/Drone/AI/DroneNPCAIController.cpp
Source/Drone/AI/DroneNPCPatrolStateTreeTasks.cpp
Source/Drone/AI/Weapons/DroneNPCProjectile.cpp
Source/Drone/AI/Animation/DroneNPCAnimInstance.cpp
```

에셋 축/AnimBP 점검 로그:

```text
C:\URproject\drone\Saved\Automation\MoonwalkAudit.log
```

최근 순찰 자동화 로그/리포트:

```text
C:\URproject\drone\Saved\Logs\PatrolWalkFix2.log
C:\URproject\drone\Saved\Automation\PatrolWalkFix2\index.json
```

## 9. 현재 Git 상태와 전달 주의사항

이번 점검 시 Unreal 프로젝트에는 커밋하지 않은 변경이 있다. 커밋/푸시는 하지 않았다. 수신자는 `git reset --hard`, 전체 되돌리기, 관련 없는 변경 삭제를 하지 않는다.

현재 변경에는 NPC 회전/순찰 태스크, 발사체 충돌, 날씨/테스트 관련 파일이 함께 포함되어 있을 수 있다. 먼저 `git status --short`와 `git diff -- Source/Drone/AI/DroneNPCPatrolStateTreeTasks.cpp Source/Drone/AI/DroneNPCAIController.cpp`를 확인한 뒤 필요한 부분만 이어서 수정한다.

## 10. 다음 작업의 우선순위

1. PIE에서 `Dot(ActorForward, VelocityDirection)`와 AnimBP `Direction`을 같은 프레임에 확인한다.
2. `Dot < 0`이면 `DroneDetected`, `PursueDrone`, `MoveToCover`, `UseCover`의 회전 소유권과 이동 목표를 정리한다.
3. `Dot > 0`인데 후진 BlendSpace가 선택되면 `ABP_NPC_Rifle_Greybox`의 Direction 계산/핀 연결을 수정한다.
4. 조준 중 이동을 허용할지 결정한다. 허용하면 전진/후진/옆걸음 애니메이션을 의도적으로 연결하고, 허용하지 않으면 조준 상태에서 이동을 정지한다.
5. 수정 후 반드시 `Patrol`, `DroneDetected`, `MoveToMGTurret`, `MoveToCover`, `Search`를 각각 PIE에서 확인한다.

핵심은 StateTree를 계속 재시작시키는 식으로 증상을 숨기지 않는 것이다. 먼저 “실제 속도가 몸의 앞/뒤 중 어느 방향인가”와 “그 속도를 AnimBP가 어떤 Direction으로 읽는가”를 분리해서 확정해야 한다.

## 11. 외부 모델 검증 중단

2026-09-18 실제 호출에서 `Union Alpha`는 테스트 종료 안내만 반환했고, 대체 Router도 잔액·출력 제한 때문에 안정적인 검증 보고서를 만들지 못했다. 사용자 결정에 따라 OpenCode/OpenRouter를 이 NPC 작업의 검증 경로에서 제외했다. 프로젝트 전용 Agent와 모델 설정도 제거했으므로 다른 PC에서 이를 복구하거나 재연결하지 않는다.

이후 완료 기준은 로컬 Unreal 근거만 사용한다.

- `git diff`에 실제 원인과 관계없는 대규모 변경이 없는가
- `DroneEditor Win64 Development` 빌드가 성공하는가
- `Patrol`, `DroneDetected`, `MoveToMGTurret`, `MoveToCover`, `Search`를 각각 PIE에서 확인했는가
- Headless 테스트 성공을 시각적 보행 정상 판정으로 잘못 기록하지 않았는가

최종 판정은 실제 PIE 화면에서 `ActorForward`, `VelocityDirection`, AnimBP `Direction`을 같은 프레임에 확인한 결과로 한다.
