# NPC 뒤로 걷기 / 사격 정면 증상 인수인계

작성일: 2026-09-18  
목적: 다른 PC 또는 다른 Codex/GPT 대화에서 NPC 보행 방향 문제를 그대로 이어서 점검하기 위한 문서

## 1. 현재 결론

문제는 아직 해결되지 않았다.

현재 확인된 사용자 증상은 다음과 같다.

- 적 NPC가 이동할 때 뒤로 걷거나, 멈췄다가 다시 움직이는 것처럼 보인다.
- 사격할 때는 드론을 향해 앞을 제대로 본다.
- 따라서 현재 작업 가설은 메시/에셋의 단순한 90도 회전 오류가 아니다.
- 사격 방향과 이동 방향 또는 애니메이션 BlendSpace 방향 입력이 서로 다른 상태로 작성되는지 확인해야 한다.

이 문서는 해결 완료 보고서가 아니다. 아래의 `확인된 사실`, `추정`, `다음 점검`을 구분해서 읽는다.

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

- `UpdatePursuitFacing`: 추적 중 속도 방향을 보거나, 드론 조준/엄폐 상태에서 조준 방향을 보도록 `bOrientRotationToMovement`를 바꾼다.
- `UpdatePersonalWeaponFacing`: `DroneDetected`/`UseCover`에서 개인 무기 조준 방향으로 회전을 적용한다. 이동 속도가 있는 동안에는 몸 회전 적용을 건너뛸 수 있다.
- `UpdateDroneGaze`: 전투/수색 상태의 시선 방향을 갱신한다. 순찰 상태에는 적용하지 않는다.

이 구조에서는 몸이 드론을 보는 동안 경로 이동은 다른 방향으로 계속될 수 있다. 그 경우 실제로 뒤로 걷는 것이 정상적인 수학 결과가 될 수 있다. 게임 디자인상 허용할지, 조준 중 이동을 멈추거나 옆걸음으로 제한할지는 아직 결정하지 않았다.

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

수정 후 `NPCPerceptionSearchPIE`, `NPCBaseRoutinesPIE`에서 해당 stuck 로그 없이 성공했다. 이것은 이동 정지 문제의 원인을 하나 줄인 것이며, 현재 사용자가 보고한 “사격은 정면인데 보행은 뒤로 감” 문제를 해결했다는 뜻은 아니다.

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

현재 AnimBP 그래프의 BlendSpace 핀 연결은 Python 점검만으로 링크를 확정하지 못했다. `ABP_NPC_Rifle_Greybox`를 에디터에서 직접 Debug하여 `Speed`, `Direction`, BlendSpace의 X/Y 입력을 확인해야 한다.

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

## 11. OpenCode / Union Alpha / 엔진 연결 세팅

이번 작업을 다른 PC 또는 다른 대화로 넘길 때는 Unreal 코드 작업과 OpenCode 연결을 아래처럼 분리한다.

### 11.1 현재 확인된 OpenCode 상태

| 항목 | 현재 값 |
|---|---|
| OpenCode | `v2.0.5` |
| 실행 파일 | `C:\Users\jkw11\AppData\Roaming\npm\opencode.ps1` |
| 모델 | `openrouter/stealth/union-alpha` |
| 사용자 설정 | `%USERPROFILE%\.config\opencode\opencode.json` |
| 작업 폴더 | `C:\URproject\drone` |

`opencode.json`에는 모델/Provider 선택만 기록되어 있고, API 키 원문은 프로젝트 문서나 Git에 기록하지 않는다. 현재 PC의 인증 정보는 OpenCode의 사용자 자격증명 저장소에 남아 있는 것으로 취급한다.

### 11.2 인증 확인 및 재연결

PowerShell에서 다음 순서로 확인한다.

```powershell
opencode --version
opencode auth list
opencode models | Select-String 'union-alpha|openrouter'
```

인증이 없거나 다른 PC에서 처음 연결할 때는 키를 명령줄 인자로 넣지 말고 대화형 로그인을 사용한다.

```powershell
opencode auth login
```

로그인 화면에서 Provider로 OpenRouter를 선택하고 키를 입력한다. API 키는 이 문서, Git 저장소, PowerShell 명령 기록, 프롬프트 본문에 붙여 넣지 않는다.

### 11.3 NPC 점검 위임 실행

Unreal 프로젝트 루트에서 OpenCode를 실행한다.

```powershell
Set-Location C:\URproject\drone
opencode run --model openrouter/stealth/union-alpha --title "NPC 보행 방향 점검" "docs/ai/DRONE_NPC_WALK_BACKWARD_HANDOFF_2026-09-18.md와 Source/Drone/AI의 NPC 코드를 읽고, 사격 시 정면을 보지만 보행이 뒤로 보이는 문제를 점검하라. ActorForward와 VelocityDirection의 관계, ResponseState별 회전 소유권, AnimBP Direction 입력을 구분해서 원인과 수정안을 보고하라. 근거 없는 StateTree 재시작이나 테스트 기대값 완화는 하지 말라. 변경 전후 파일과 검증 결과를 보고하라."
```

OpenCode가 실제 파일을 수정하게 할 때도 먼저 위 문서와 `git status --short`를 읽게 한다. Unreal Editor가 열려 있으면 C++ DLL이 잠겨 빌드가 실패할 수 있으므로, 코드 수정/빌드 담당자는 Editor 종료 여부를 먼저 확인한다.

### 11.4 Unreal Editor 직접 실행

OpenCode는 프로젝트 루트에서 실행하고, Unreal Editor는 별도 프로세스로 연다.

```powershell
$editor = 'C:\Program Files\Epic Games\UE_5.8\Engine\Binaries\Win64\UnrealEditor.exe'
$project = 'C:\URproject\drone\Drone.uproject'
& $editor $project
```

Editor에서 아래 맵을 열고 Output Log를 확인한다.

```text
/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox
```

### 11.5 Unreal MCP와 OpenCode의 경계

현재 프로젝트에 확인된 Unreal MCP 설정은 Codex용이다.

```text
C:\URproject\drone\.codex\config.toml
MCP URL: http://127.0.0.1:8000/mcp
```

Unreal Editor의 `ModelContextProtocol` 서버는 `127.0.0.1`에만 열고, `Config/DefaultEditorPerProjectUserSettings.ini`의 자동 시작 설정을 사용한다. MCP는 인증 계층이 없는 실험 기능이므로 LAN/인터넷 주소로 바꾸지 않는다.

연결 확인은 다음 순서다.

1. Unreal Editor를 먼저 실행한다.
2. Output Log에서 `LogModelContextProtocol: Starting MCP server on port 8000`을 찾는다.
3. 같은 PC의 Codex 작업을 `C:\URproject\drone` 루트에서 새로 열거나 재연결한다.
4. MCP Tool 목록에서 `unreal-mcp`와 Current Level 조회가 보이는지 확인한다.

OpenCode가 이 `.codex/config.toml`을 자동으로 읽는다고 가정하지 않는다. OpenCode에서 Unreal MCP를 사용해야 하는 경우에는 OpenCode의 MCP 설정을 별도로 확인하고, 연결되지 않은 상태에서는 파일/명령 기반으로만 작업한다.

### 11.6 API 키 보안 처리

요청에 포함된 API 키 원문은 이 인수인계 문서에 기록하지 않았다. 결제가 막힌 키라도 유출되면 제3자가 사용할 수 있고, 채팅·Git·로그에 남으면 회수가 어렵다. 이미 채팅에 붙여 넣은 키는 사용을 끝낸 뒤 Provider에서 폐기/재발급하는 것이 안전하다.

수신자는 키 문자열을 복사하는 대신 다음 중 하나로 로컬 인증만 구성한다.

- `opencode auth login`에서 대화형으로 입력
- OpenRouter가 안내하는 사용자 환경변수 방식으로 현재 셸에만 설정
- 회사/팀의 비밀 저장소에서 실행 시 주입

어떤 방식이든 키를 `opencode.json`, `service.json`, `.codex/config.toml`, `.env`, Markdown, Git commit에 직접 넣지 않는다.

## 12. OpenCode 작업 완료 기준

OpenCode가 작업을 끝냈다고 보고해도 다음을 별도로 확인한다.

- `git diff`에 실제 원인과 관계없는 대규모 변경이 없는가
- `DroneEditor Win64 Development` 빌드가 성공하는가
- `Patrol`, `DroneDetected`, `MoveToMGTurret`, `MoveToCover`, `Search`를 각각 PIE에서 확인했는가
- Headless 테스트 성공을 시각적 보행 정상 판정으로 잘못 기록하지 않았는가
- API 키나 인증 파일이 `git status`에 나타나지 않는가

OpenCode의 분석 결과는 참고 자료이고, 최종 판정은 실제 PIE 화면에서 `ActorForward`, `VelocityDirection`, AnimBP `Direction`을 같은 프레임에 확인한 결과로 한다.
