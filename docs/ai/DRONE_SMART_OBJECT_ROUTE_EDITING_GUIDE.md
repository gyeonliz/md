# Drone Smart Object 동선·배치 수정 가이드

기준일: 2026-09-15 (Asia/Seoul)

이 문서는 팀원이 Unreal Editor에서 NPC 순찰·생활·엄폐·유인 기관총 지점을 안전하게 배치하고 동선을 조정하기 위한 작업 절차다. 코드 구조 전체는 [`DRONE_SMART_OBJECT_NPC_GUIDE.md`](DRONE_SMART_OBJECT_NPC_GUIDE.md)를 참고하고, 실제 맵 배치는 이 문서를 먼저 따른다.

## 1. 먼저 알아둘 현재 동선 규칙

현재 Smart Object 동선은 **스플라인을 따라 순서대로 이동하는 경로가 아니다**.

```text
NPC 역할에 맞는 Activity Tag 설정
→ 검색 반경 안의 비어 있는 Slot 조회
→ 현재 위치에서 가장 가까운 지점 Claim
→ NavMesh 이동
→ 대기 또는 사용
→ Release
→ 직전 완료 지점 주변을 우선 피하고 다시 검색
```

- 순찰점을 옮기면 NPC가 선택할 수 있는 지점망이 바뀐다.
- `1 → 2 → 3`처럼 고정된 방문 순서는 현재 보장하지 않는다.
- 한 Slot은 한 NPC만 Claim/Occupied할 수 있다.
- 직전 지점 회피 기본 반경은 `250cm`다. 다른 지점이 없으면 같은 지점을 다시 쓸 수 있다.
- 고정 순서가 필요하면 향후 `RouteId`, `OrderIndex`, 다음 지점 참조를 가진 별도 Route 기능을 구현해야 한다. 현재 Actor Label의 번호는 정리용이며 실행 순서를 만들지 않는다.

## 2. 맵과 파일 소유권

| 목적 | 사용할 맵/폴더 | 규칙 |
|---|---|---|
| NPC·Smart Object·유인/무인 포탑 기능 시험 | `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox` | AI 전용 시험 맵. 기능 회귀와 배치 실험에 사용 |
| Tutorial Ring·HUD·Mission Rule 시험 | `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest` | 튜토리얼 시스템 전용. NPC 동선 시험을 섞지 않음 |
| 실제 Tutorial 환경 제작 | `/Game/Drone/Maps/Lvl_DroneTraining` | 현재 팀원 담당 Production Map. 담당자 합의 없이 저장·복제·자동 배치하지 않음 |

같은 `.umap`을 두 명이 동시에 수정하면 Git에서 내용을 합칠 수 없다. 작업 전 담당자를 정하고, 맵 수정자는 시작 전에 Pull하고 종료 후 변경된 `.umap` 하나를 명확히 알린다.

## 3. 배치할 Blueprint 찾기

경로: `/Game/Drone/AI/SmartObjects/Blueprints`

| 용도 | 배치 Blueprint | 실제 Activity |
|---|---|---|
| 적 순찰 | `BP_SO_EnemyPatrol` | `EnemyPatrol` |
| 아군 기지 순찰 | `BP_SO_FriendlyBasePatrol` | `FriendlyBasePatrol` |
| 생활·대기 | `BP_SO_Ambient` | `Ambient` |
| 경계 | `BP_SO_Guard` | `Guard` |
| 엄폐 | `BP_SO_Cover` | `Cover` |
| 병사가 잡는 유인 기관총 | `BP_SO_MGTurret` | `MGTurret` |

차량 장착형 `BP_AutoTurret_Vehicle`과 설치형 `BP_AutoTurret_Emplaced`는 무인 자동포탑이다. 둘은 유인 기관총의 회전·발사 기반만 재사용하며 Smart Object Definition이 없으므로 NPC가 Claim하지 않는다.

## 4. 순찰·생활 지점을 이동하는 방법

1. 담당 맵을 열고 `World Outliner`에서 `Station_` 또는 `BP_SO_`로 검색한다.
2. 옮길 Actor를 선택하고 `W`로 이동, `E`로 Yaw를 회전한다.
3. Cyan 화살표의 `+X`가 NPC가 지점에 도착해 바라볼 방향이다.
4. 지면에 붙이되 바닥 Collision 아래로 묻히지 않게 한다.
5. `P`를 눌러 NPC 시작점부터 새 위치까지 녹색 NavMesh가 연결되는지 확인한다.
6. 같은 종류의 지점은 `Alt+Drag`로 복제한다.
7. Actor Label은 `Station_역할_번호`로 정리한다. 예: `Station_EnemyPatrol_01`.
8. 최소 2개, 권장 3개 이상을 배치해야 왕복·분산 동선이 보인다.
9. PIE에서 실제 이동을 확인한 뒤 **본인이 담당한 맵만** 저장한다.

### 좋은 배치 간격

- 너무 가까운 지점 여러 개는 사실상 같은 동선처럼 보인다.
- 좁은 문, 계단, 차량, 엄폐물 바로 안쪽은 Capsule과 NavMesh가 겹치지 않는지 확인한다.
- 두 NPC가 같은 통로를 반복해서 막으면 지점을 통로 중앙이 아니라 통과 후 열린 공간에 둔다.
- 순찰점 사이에 벽이 있어도 NavMesh가 연결돼 있으면 우회한다. 직선 이동만 원하면 장애물과 NavMesh부터 정리한다.

## 5. 위치는 그대로 두고 NPC가 서는 곳만 조정하기

모든 배치 Actor에 공통으로 적용할 Offset이면 대응 `BP_SO_*`를 열어 Viewport에서 상속된 `SmartObjectComponent`의 상대 Location·Rotation을 조정한다.

- `SlotFacingPreview`는 `SmartObjectComponent`의 자식이므로 Cyan 화살표도 함께 이동해야 한다.
- 특정 맵의 한 지점만 다르게 만들려고 공용 Blueprint를 바꾸지 않는다.
- 예외 지점이 꼭 필요하면 `/Game/Drone` 아래에 프로젝트 소유 Child Blueprint를 만든다.
- Definition의 Slot 수·Activity Tag까지 바꾸는 작업은 전체 검색 계약에 영향을 주므로 코드 담당자와 먼저 합의한다.

## 6. 유인 기관총 위치·접근 조정

`BP_SO_MGTurret`만 병사가 점유하는 포탑이다.

### 포탑 구성

```text
MGTurretBaseMount               고정 하단부
└─ MGTurretYawPivot             좌우 회전 몸체
   ├─ MGTurretOperatorAnchor    사수의 후방 위치·몸 방향
   └─ MGTurretAimPivot          포신 상하 회전
      └─ MGTurretMuzzle         발사 위치
```

`BP_SO_MGTurret`의 Class Defaults에서 다음 값을 조정한다.

- `MGTurret Operator Distance`: 사수와 포탑 사이 앞뒤 거리
- `MGTurret Operator Lateral Offset`: 좌우 Offset
- `MGTurret Operator Vertical Offset`: 높이 Offset
- `Range`, `Cooldown`, `Damage`, `Projectile Speed`, `Spread`: 전투 시험값

`ST_NPC_HostilePatrol`의 `Move To Reserved MG Turret` Task에서는 다음 값을 조정할 수 있다.

- `Acceptance Radius`: NavMesh 이동 목표 허용 반경
- `Operator Snap Radius`: 충분히 접근했지만 장애물 모서리에서 이동이 끝나지 않을 때 정확한 Anchor로 최종 정렬하는 반경
- `Stall Timeout Seconds`: 실제 이동이 없다고 판단하기까지의 시간
- `Minimum Progress Distance`: 정지 감시를 초기화할 최소 이동 거리
- `Max Repath Attempts`: 한 Claim 안에서 경로를 다시 요청할 횟수

기본 `Operator Snap Radius=250cm`는 Greybox 장애물을 고려한 시험값이다. 최종 포탑 Mesh와 엄폐물 배치가 정해지면 화면에서 순간이동처럼 보이지 않는 최소값으로 낮춘다.

사망한 사수가 Slot을 놓은 뒤 다른 MG 가능 적은 기본 `0.75초` 간격, 최대 `15초` 동안 재Claim을 시도한다. 이 값은 파생 AI Controller Blueprint의 `Drone > AI > MG > Reassignment`에서 바꿀 수 있다.

## 7. StateTree에서 행동 시간 조정하기

경로: `/Game/Drone/AI/StateTrees`

- 적: `ST_NPC_HostilePatrol`
- 아군: `ST_NPC_FriendlyBaseRoutine`

StateTree를 열고 해당 Task를 선택하면 Details에서 `AcceptanceRadius`, 대기 시간, 재시도 시간을 조정할 수 있다. 상태나 Transition 구조를 바꿀 때는 다음 계약을 유지한다.

- 적 기본: `Claim Patrol → Move → Wait → Release`
- 적 드론 감지: `Claim MG → Move MG → Use MG`; 실패하면 `Claim Cover`; 그것도 실패하면 제자리 개인화기
- 아군 기본: `FriendlyBasePatrol/Ambient Claim → Move → Wait → Release`
- 감지 실종·사망·이동 실패 시 잡고 있던 Slot을 Release

StateTree 구조를 바꾸면 저장만 하지 말고 Compile 성공과 자동화 검증까지 수행한다.

### 상태가 빠르게 왕복할 때

`ADroneNPCAIController`에는 공통 `Minimum Response State Duration Seconds`가 있고 기본값은 `1.0초`다. MG·Cover 이동/사용 중 예약이나 사격 시작이 한 프레임 실패하면 즉시 다른 상태로 넘어가지 않고, 이 시간 동안 현재 상태에서 다음을 다시 점검한다.

- `DroneDetected`: 개인화기 사격이 꺼졌으면 다시 시작
- `MoveToMGTurret`, `MoveToCover`: Drone 감지와 Slot 예약이 아직 유효한지 확인
- `Hold/UseMGTurret`: 점유 시작 또는 포탑 조준·사격을 재시도
- `UseCover`: Occupied 상태와 개인화기 사격을 재확인
- `Search`: 마지막 감지 위치가 유효한지 확인

최소시간이 지난 뒤에도 조건이 회복되지 않았을 때만 기존 StateTree 실패 Transition을 따른다. 사망, Drone 파괴, `DroneSightLossGracePeriod` 뒤 확정된 Lost는 자원 정리가 우선이므로 최소시간을 기다리지 않는다.

이 값은 상태 왕복을 가리기 위해 크게 올리는 용도가 아니다. 기본 `1.0초`를 기준으로 먼저 NavMesh, Slot 예약, 탄약/표적 유효성 문제를 고치고, 필요할 때만 Controller Blueprint에서 `Drone > AI > State Stability`를 조정한다. `0`은 안정화 대기를 끈다.

## 8. Editor에서 빠르게 확인할 항목

1. `P`: 녹색 NavMesh가 NPC 시작점과 모든 목적지에 이어지는가.
2. Cyan 화살표: 순찰·생활·Cover 도착 방향이 의도와 맞는가.
3. MG의 Green Operator Anchor: 포탑 뒤 지면 위에 있는가.
4. PIE: 같은 1-Slot에 두 NPC가 동시에 서지 않는가.
5. 적 2명: 한 지점만 반복하지 않고 서로 다른 지점을 방문하는가.
6. 아군 2명: FriendlyBasePatrol과 Ambient를 모두 사용하는가.
7. 사수 사망: 유인 MG만 Free가 되고 다른 적이 이어받는가.
8. 무인포탑: NPC가 접근하거나 점유하지 않고 스스로 표적을 찾는가.

## 9. 검증 명령

Editor를 종료한 뒤 문서 저장소에서 실행한다.

```powershell
cd D:\JGY\project\md

powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\unreal\Invoke-DroneSmartObjectSetup.ps1 -Mode Validate -ProjectPath D:\JGY\project\drone\Drone.uproject

powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\unreal\Invoke-DroneNPCGreyboxSetup.ps1 -Mode Validate -ProjectPath D:\JGY\project\drone\Drone.uproject

powershell.exe -NoProfile -ExecutionPolicy Bypass -File tools\unreal\Invoke-DroneHostilePerceptionStateTreeSetup.ps1 -Mode Validate -ProjectPath D:\JGY\project\drone\Drone.uproject
```

자동화의 핵심 회귀는 `Drone.AI.NPCPerceptionSearchPIE`다. 유인 MG 1개 점유, 다른 적의 Cover/제자리 사격 Fallback, 사수 사망 뒤 재점유, DroneLost/Search/Patrol 복귀를 확인한다.

## 10. 문제가 생겼을 때

| 현상 | 먼저 확인할 것 | 수정 방향 |
|---|---|---|
| NPC가 지점을 못 찾음 | Definition Activity Tag, NPC 역할 Tag, 검색 반경 | Tag를 맞추고 검색 영역 안으로 이동 |
| NPC가 제자리에서 멈춤 | `P` NavMesh, 목적지 바닥 높이, 장애물 Collision | NavMesh 연결과 Capsule 통과 폭부터 수정 |
| NPC가 엉뚱한 순서로 이동 | 현재는 최근접 빈 Slot 방식 | 번호 변경으로 해결되지 않음. 고정 Route 기능 별도 구현 필요 |
| 같은 곳만 반복 | 다른 지점 수와 간격, 직전 회피 반경 | 최소 2~3개 지점을 충분히 떨어뜨림 |
| 도착 뒤 방향이 반대 | Actor Yaw와 Cyan 화살표 | Actor를 Yaw 회전. Mesh만 돌리지 않음 |
| MG 앞이나 옆에 섬 | Operator Distance/Lateral/Vertical, Green Anchor | `BP_SO_MGTurret` Class Defaults 조정 |
| MG 근처에서 계속 걷기만 함 | Operator Snap Radius, Stall Timeout, 주변 Collision | Snap 반경은 최소한으로 올리고 장애물 배치를 함께 수정 |
| 자동포탑을 병사가 잡으려 함 | 잘못된 Definition 연결 여부 | 자동포탑에는 Smart Object Definition을 연결하지 않음 |
| Git에서 `.umap` 충돌 | 두 명이 같은 맵을 수정했는지 | 한쪽 맵을 선택해야 함. 맵 담당자를 사전에 분리 |

## 11. 팀 인계 체크리스트

- [ ] 수정한 맵과 Actor Label 목록을 적었다.
- [ ] Production `Lvl_DroneTraining` 담당자 동의를 받았다.
- [ ] `P` NavMesh 연결을 확인했다.
- [ ] Cyan/Green 화살표 방향을 확인했다.
- [ ] 유인 MG 1개와 무인포탑 2종을 구분했다.
- [ ] StateTree Compile 오류가 없다.
- [ ] 관련 Validate와 자동화가 통과했다.
- [ ] PIE 화면에서 겹침·멈춤·순간이동 체감을 확인했다.
- [ ] 변경된 `.umap`, `.uasset`, 코드 파일을 팀원에게 알렸다.
- [ ] 미확인 항목은 Done이 아니라 `수동 확인 대기`로 기록했다.
