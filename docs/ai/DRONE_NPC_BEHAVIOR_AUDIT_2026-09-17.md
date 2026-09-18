# NPC 행동 로직 집중 감사 — 2026-09-17

## 결론

사용자가 보고한 몸/머리 떨림·애니메이션 중첩의 화면 원인은 아직 확인하지 못했다. 실제 코드에서 개인화기 교전 시간의 중복 누적 경로를 확인해 최소 수정했다. 관련 자동화 전체는 통과하지 않았다. Shotgun PIE의 MoveTo 요청 수 검사가 실패했으며 추가 요청이 정상 복구인지 중복인지 미확정이다.

## 확인한 계약과 경로

- StateTree: Patrol → 감지 Event → MG Claim/Move/Hold(운용), 실패 시 Cover Claim/Move/Use 또는 DroneDetected 개인화기 대체. Lost → SearchLastKnownLocation → 순찰 Claim. PursueDrone은 별도 StateTree 노드가 아니라 Controller ResponseState다. 별도 Disengaged/Return enum은 없으며 리시 포기는 Patrol 및 다음 Tick Tree 재시작으로 처리한다.
- 최소 유지 기본 1초는 MG/Cover 태스크의 일시 실패 회복과 MG 재할당 중단 허용 조건이다. 모든 StateTree 전환이나 Fire/Pursue에 무조건 1초를 강제하는 계약은 아니다. 사망·파괴·Lost 확정 정리는 지연하지 않는다.
- 개인화기: 실제 3D 사거리 안이면 즉시 StopMovement/Fire, 밖 판정 0.2초 지속 시 Pursue. 과거 문서의 100cm 공간 hysteresis는 폐기된 기준이다. 리시 3,000cm, 무진행 2.5초, 재경로 주기 0.35초/거리 150cm, 포기 후 3초 cooldown 및 원점 반경 85% 재진입 조건.
- 회전: Character BeginPlay에서 controller-yaw/desired-rotation을 끈다. Pursue 중에는 Controller가 속도 방향 Yaw를 쓰고 orient-to-movement를 끈다. 나머지 이동은 CharacterMovement, 정지 개인화기는 Controller의 3° 정지/6° 시작 hysteresis, MG 운용은 Operator Anchor 정렬이다. 과거 문서의 '추적도 CharacterMovement만 작성'은 현재 소스와 다르다. 이 분리만으로 실제 프레임 순서/역할 BP의 중복 제어 부재가 증명되지는 않는다.
- Gaze: 몸 회전 뒤 로컬 각도를 구하고 yaw/pitch 제한·보간. Pursue는 속도 방향, Search는 마지막 위치. 현재 Bone Gaze에는 3° zero snap이 없으며 작은 잔여 오차도 보간한다.
- Animation: NativeUpdateAnimation은 Controller 값을 읽어 spine/neck/head에 분배한다. 생성 코드의 Component Space Modify Bone 직렬 연결을 확인했다. Character는 AddUniqueDynamic 발사/재장전 바인딩, 동일 Sequence 재생 중 재시작 방지, Dynamic Montage slot/blend 경로를 사용한다. Reload는 즉시 완료 이벤트를 보내므로 사격 표현과 시간상 인접할 수 있으나 화면 중첩 결함으로 판정하지 않았다. 저장 AnimBP의 전체 EventGraph/slot/blend 가중치와 실제 포즈는 이번 실행에서 직접 검증하지 않았다.
- MG 사망: 점유 해제 후 생존 가능 NPC에 재할당 예약. 재시도 간격 0.75초/최대 15초. 무인 자동포탑은 NPC Smart Object 점유와 별도다.

## 입증한 결함과 수정

`Source/Drone/AI/DroneNPCAIController.cpp`:

`Tick → UpdateMGTurretReassignmentRetry → (최소 유지시간 중) MaintainCurrentResponseStateAction → UpdatePersonalWeaponEngagement(WorldDelta)` 이후 같은 Tick의 일반 경로가 `UpdatePersonalWeaponEngagement(DeltaSeconds)`를 다시 호출했다. 조건이 유지되면 사거리 밖 확인, 무진행, 재경로 시간이 한 프레임에 두 번 진행될 수 있었다. MG 재할당 타이머 자체가 두 번 호출되는 문제가 아니다.

개인화기 상태의 Maintain 분기만 유효성 확인으로 바꾸고 시간·사격·이동 갱신은 Controller Tick에 맡겼다. StateTree 최초 Enter의 `UpdatePersonalWeaponEngagement(0)`는 보존했다. MG/Cover 유지 행동은 바꾸지 않았다.

`Source/Drone/AI/Tests/DroneNPCEngagementMaintenanceTest.cpp` 추가:

임시 Editor World에서 유지 함수와 실제 Controller Tick을 순서대로 호출하여 사거리 확인 0.05초, 무진행 +0.05초, 재경로 -0.05초를 검사한다. live MG 사망/StateTree 재시도 전체를 새 테스트가 직접 구동하는 것은 아니다.

## 실행 결과

- 기존 `Saved/Automation/NPCWeatherAudit/BaselineAI/index.json`: NPCGreyboxAssets, NPCPerceptionSearchPIE, PersonalWeaponEngagementPolicy 3/3 성공 확인.
- 기존 `BaselineShotgun/index.json`: ShotgunSystemsTestMap, ShotgunSystemsTestMapPIE 2/2 성공 확인. 기준선 자체는 재실행하지 않았다.
- 변경 전 로컬 Python 시간 누적 모델: 0.05초 프레임에 두 경로가 0.10초를 누적함을 확인. 소스 연결 확인 + 산술 모델이며 변경 전 UE Red 또는 화면 재현은 아니다.
- DroneEditor Win64 Development Build **1회 성공**, 종료 0. 비권장 MSVC 버전 및 Engine deprecated API 경고 존재.
- 관련 필터 **1회**: `Drone.AI.PersonalWeaponMaintenanceTiming+Drone.AI.NPCPerceptionSearchPIE+Drone.AI.ShotgunSystemsTestMapPIE`, unattended/NullRHI.
  - PersonalWeaponMaintenanceTiming: 성공, 빈 Native Character의 hand_r/Mesh 경고 7건.
  - NPCPerceptionSearchPIE: 성공, 보고서 경고 0. 예상 Recast 경고 억제 기록 있음.
  - ShotgunSystemsTestMapPIE: **실패**, `A stationary pursuit target does not restart the active MoveTo path` 기대 2/실제 3. 오류 1건. 실행 종료 코드 0이어도 전체 성공이 아니다.
- 새 결과: `Saved/Automation/NPCBehaviorAudit/index.json`, 로그: `Saved/Logs/NPCBehaviorAudit.log`.
- 추가 빌드·재실행, 수동 렌더 PIE, 맵/에셋 저장, Production Training 접근, MCP 설치/연결, Git commit/push/pull/브랜치 변경은 하지 않았다.

## 남은 실패와 정확한 후속 관측

MoveTo 정책에는 이미 활성 Moving/Paused 경로 + 150cm 미만 목표 변화이면 재요청하지 않는 가드가 있다. 중단된 경로는 같은 목표라도 재요청한다. 실패 테스트는 0.45초 동안 요청 수가 불변인지 비교하지만 중간 PathFollowing 상태/요청 종료 이유를 기록하지 않는다. 이번 결과만으로 정상 복구를 막는 추가 가드를 넣거나 테스트 기대값을 완화하지 않았다.

추가 빌드/실행을 별도로 허용받은 후, 개인화기의 실제 `MoveToLocation` 호출 직전/직후에 한정해 world time/frame, ResponseState, 이전/새 RequestID, PathFollowing 상태, path valid/partial, 이전 projected goal/새 goal/2D 편차, 요청 결과 및 이전 요청 완료/abort 사유를 기록한다. 실패한 pursuit PIE만 실행해 NavMesh 갱신/경로 종료 시점과 비교한다. 이번 실행에서는 이 계측을 추가하거나 실행하지 않았다.

## 사용자 수동 PIE 최소 절차 (저장 금지)

1. `/Game/Drone/Maps/TestMap/Lvl_DroneShotgunSystemsTest`에서 PIE. 살아 있는 Shotgun 한 명과 Drone을 기준으로 녹화한다. 거리 표식은 지면 거리이므로 실제 3D 거리를 함께 확인한다.
2. 사거리 안에서 정면 좌우 ±1~2°, 이후 ±7°로 움직이고 정지한다. 몸 Yaw, Controller yaw, 수평 velocity/acceleration, movement 회전 플래그, DroneLookRotation/Alpha, spine_03/neck_01/head 회전과 Montage 이름·position·weight를 같은 시각에 관찰한다. AnimBP Debug Filter는 해당 PIE NPC를 선택한다.
3. 1,590↔1,610cm를 짧게 왕복한 뒤 밖에 0.2초 이상 유지하고, 다시 안으로 들어온다. ResponseState/경과시간/추적 시작 수/MoveTo 요청 수와 StateTree 실제 활성 노드를 구분해 기록한다. state가 고정인데 bone만 떨리는지, transition과 함께 pose가 리셋되는지 구분한다.
4. `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox` 새 PIE에서 MG 사수 점유 후 사망시키고 생존 MG 가능 NPC를 관찰한다. 최소 유지/재할당/개인화기 전환과 Anchor 정렬을 같은 녹화에 남긴다.
5. 장애물 뒤 0.5초 가림/복귀, 1초 넘는 가림, Search 종료 및 리시 밖 포기 후 순찰 복귀를 비교한다. 감지/lost 횟수, 실제 활성 StateTree 노드와 ResponseState를 기록한다. 종료 후 Keep Simulation Changes/Save를 사용하지 않는다.

화면 떨림 해결, 저장 AnimBP 중복 표현 제거, 전체 관련 회귀 통과는 아직 주장할 수 없다. 기존 사용자 변경 파일은 수정/복원하지 않았다. 초반 도구 호출에 병렬 읽기를 사용한 요청 위반이 있었으며 이후 조사는 순차로 진행했다. 하위 에이전트는 생성하지 않았다.

## 1초 상태 유지에 대한 재확인

현재 `MinimumResponseStateDurationSeconds=1.0`은 매 1초마다 새 행동을 선택하는 타이머가 아니다. `UpdateMGTurretReassignmentRetry()`가 재할당을 시도하기 전과 MG/Cover StateTree Task가 일시 실패할 때만 현재 상태를 유지하며, 그 동안 `MaintainCurrentResponseStateAction()`은 조건을 재확인한다. 정상 상태에서 `StateTreeAIComponent->StartLogic()`를 반복 호출하지 않고, Controller Tick도 StateTree를 재시작하지 않는다.

개인화기 교전은 별도 경로다. 실제 사거리 안이면 즉시 `DroneDetected`/정지·사격, 사거리 밖 판정이 0.2초 지속되면 `PursueDrone`으로 바뀌며, 같은 Pursue 상태에서는 매 프레임 상태를 다시 선택하지 않고 이동·재경로 타이머만 갱신한다. 따라서 현재 코드만으로 “1초마다 행동을 새로 골라서 떤다”고 결론 내릴 근거는 없다. 다만 화면 떨림은 StateTree 전환과 별개로 Controller Yaw, CharacterMovement, Bone Gaze, AnimBP Montage가 동시에 영향을 줄 수 있으므로 PIE에서 실제 활성 StateTree 노드와 ResponseState 경과시간을 함께 확인해야 한다.

## 이어서 적용한 보강

활성 MoveTo 경로 종료와 중복 재요청을 구분할 수 있도록 `IsPersonalWeaponPursuitMoveActive()` 진단 getter를 추가했다. Shotgun PIE 안정성 검사는 실제 `Moving/Paused` 경로가 안정성 구간 시작 시 활성일 때만 “재요청 없음”을 판정하고, 이미 경로가 끝난 경우의 새 요청은 정상 복구 가능성으로 정보 기록한다. 동작을 임의로 차단하거나 기대값을 낮춘 수정은 아니다.

이 보강 뒤 `DroneEditor Win64 Development` 빌드가 성공했다. 기존 Shotgun PIE 실패를 재실행한 것은 아니므로, 자동화 결과는 아직 최종 Green으로 갱신하지 않는다.

## 2026-09-17 후속 화면 증상 안정화 수정

사용자가 보고한 “도리도리 후 옆구리 사격·뒤로 걷기” 경로를 코드에서 다시 대조했다. `DroneDetected`/`UseCover`에서는 Controller의 개인화기 조준 Yaw와 CharacterMovement의 이동방향 Yaw가 동시에 소유자가 될 수 있었고, 사거리 진입 직후 `StopMovement()`만으로는 이전 Pursue 속도가 남을 수 있었다.

수정 내용:

- 실제 사거리 안에서 Fire로 전환할 때 `CharacterMovement->StopMovementImmediately()`로 잔여 수평 속도를 제거한다.
- `DroneDetected`/`UseCover`에서는 `bOrientRotationToMovement`를 끄고 Controller 조준만 몸 Yaw를 담당하게 한다.
- 개인화기 몸 회전은 실제 이동 속도가 남아 있는 동안 개입하지 않는다. Pursue 중에는 이동 벡터 기반 `UpdatePursuitFacing`만 사용한다.

이 변경은 StateTree를 1초마다 재선택하는 수정이 아니라 회전·이동의 단일 소유자를 분리하는 수정이다. 소스 공백 검사는 통과했다. 재빌드는 현재 Unreal Editor Live Coding이 활성화되어 UBT가 거부했으며, 코드 컴파일 결과는 아직 재확인 전이다. Editor를 닫거나 Live Coding을 종료한 뒤 Build/Shotgun PIE를 실행해야 한다.

## Smart Object 맵 테스트의 한계 재확인

`Drone.AI.NPCPerceptionSearchPIE`는 실제 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`를 열지만, 사용자가 보는 실제 플레이를 그대로 검증하는 화면 테스트가 아니다.

- Drone의 Perception Source를 끄고 `BroadcastSight()`로 감지를 수동 주입한다.
- 테스트 시작 시 Shotgun NPC의 Runtime Profile을 임시로 MG 사용 가능으로 바꾼다.
- Hostile 무기 피해를 0으로 낮추고, Rifle/Shotgun 사거리를 `100000cm`로 확장한다.
- 검증은 상태·예약·카운터·Target/AimPoint 계약 중심이며, 실제 플레이 중 이동/애니메이션/발사 자세를 녹화하지 않는다.

따라서 이 테스트의 `Success`는 Smart Object 상태 전이 계약이 통과했다는 뜻이지, 사용자가 원본 맵에서 본 NPC의 실제 시각 행동이 정상이라는 뜻이 아니다. 이번 증상은 원본 Profile·실제 Perception·실제 사거리·AnimBP가 살아 있는 Smart Object 맵 수동 PIE에서 별도로 재현해야 한다. 지금까지 이 조건을 자동화가 대신 검증한 것으로 설명한 것은 부정확했다.

## 최종 재검증 결과 — 2026-09-17

- 에디터 종료 후 `DroneEditor Win64 Development` 최신 빌드 성공.
- 스마트 오브젝트 맵 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox` 전용 자동화 3개를 재실행.
- `NPCBaseRoutinesPIE`, `NPCGreyboxPIE`, `NPCPerceptionSearchPIE`: **3/3 Success**, 실패 0, 미실행 0.
- 결과 보고서: `C:\URproject\drone\Saved\Automation\SmartObjectAudit_Final\index.json`
- 로그: `C:\URproject\drone\Saved\Logs\SmartObjectAudit_Final.log`

초기 연속 실행에서 재현됐던 MG 재할당 실패는 최종 재실행에서 재현되지 않았다. 다만 이 자동화는 수동 감지 주입·런타임 프로필 변경을 포함하므로, 사용자가 본 화면상의 도리도리/옆구리 사격/뒤로 걷기가 해결됐다고 단정하지 않는다. 다음 확인은 원본 스마트 오브젝트 맵에서 실제 Perception과 AnimBP를 켠 수동 PIE다. 임시 진단 로그는 제거했으며 커밋·푸시는 하지 않았다.

## 순찰 중 뒤로 걷기·정지 반복 후속 수정

사용자가 보고한 순찰 중 “고개를 좌우로 돌리며 뒤로 걷고, 움직이다 멈추는” 증상을 로그와 대조한 결과, `BP_ShotgunPelletProjectile`이 `ECC_Pawn`을 Block하고 있어 다른 NPC를 실제 이동 장애물처럼 막는 경로를 확인했다. 수정 전 로그에는 `BP_NPC_Hostile_Shotgun_C_0 is stuck and failed to move`가 기록됐고, 수정 후 순찰/감지 테스트에서는 해당 로그가 사라졌다.

수정:

- `DroneNPCProjectile`이 의도한 표적이 아닌 `ADroneNPCCharacter`를 Sweep Ignore하도록 변경해 NPC 간 탄환이 이동을 막지 않게 했다. 의도한 Drone 표적 충돌과 Damage 판정은 유지한다.
- 감지 진입과 Search 종료에서 `CharacterMovement->StopMovementImmediately()`를 호출해 이전 추적 속도가 순찰 방향에 남지 않게 했다.
- Patrol 상태에서는 전투 대상이 남아 있어도 Combat Gaze를 갱신하지 않도록 제한했다.

검증:

- `DroneEditor Win64 Development` Build 성공.
- `Drone.AI.NPCPerceptionSearchPIE`: Success, 실패 0, `stuck` 로그 없음.
- `Drone.AI.NPCBaseRoutinesPIE`: Success, 실패 0.

실제 화면에서의 최종 확인은 동일 Smart Object 맵 PIE에서 수행한다. 커밋·푸시는 하지 않았다.
