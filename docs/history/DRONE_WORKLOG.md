# Drone 개발 진행 기록

기준일: 2026-09-15 (Asia/Seoul)

이 문서는 Drone 개발의 **진행 이력**을 시간순으로 남긴다. 가장 최신의 현재 상태는 [`../WORKBOARD.md`](../../WORKBOARD.md), 확정 구현 순서는 [`DRONE_TUTORIAL_STORY_PLAN.md`](../planning/DRONE_TUTORIAL_STORY_PLAN.md)를 따른다.

## 갱신 규칙

Drone 코드·자산·계획 작업을 진행할 때마다 작업 종료 전에 Markdown을 함께 갱신한다.

1. `WORKBOARD.md`: 현재 단계, 지금 작업 중인 카드, 완료 근거, 남은 조건과 바로 다음 작업
2. `DRONE_WORKLOG.md`: 실제 변경, 검증 결과, 발견한 문제와 다음 행동을 날짜순으로 추가
3. `STATUS.md`: 빌드·테스트·자산 수처럼 검증된 기준선이 달라졌을 때 갱신
4. `CONTEXT.md`: 사용자가 확정한 방향, 장기 규칙과 범위가 달라졌을 때 갱신
5. 계획 문서: 구현 순서, 완료 조건이나 설계가 달라졌을 때 같은 작업에서 갱신

진행률은 근거 없는 전체 백분율로 표시하지 않는다. 대신 `현재 단계`, `통과한 게이트/전체 게이트`, `Doing`, `다음 활성 카드`로 기록한다. 자동화가 통과해도 필수 수동 확인이 남아 있으면 완료로 이동하지 않는다.

## 현재 스냅샷

마지막 갱신: 2026-09-15 — Gate 4변 Frame과 통과 판정 정합화

| 구분 | 현재 상태 |
|---|---|
| 전체 단계 | 경량 Tutorial Systems Test Map 생성·기술 검증 완료. TestMap 수동 Vertical Slice 대기 |
| Unreal 기준선 | 로컬 추적 `main=origin/main=dc655ac`; 개인화기 추적/AI 회귀 Source·Test는 로컬 미커밋 |
| 자동 검증 | Editor Build 성공. 개인화기 정책·Smart Object 기본값·Shotgun PIE·NPC 감지/MG/Search PIE·NPC 역할 자산 5/5 성공 |
| PFN-06 진행도 | 필수 게이트 5/5 Pass, Done |
| 지금 작업 중 | 개인화기 추적·포기와 MG 사망 교대 자동화 완료. Smart Object 맵 화면 회귀 및 기존 TestMap 수동 확인 대기 |
| 차단 조건 | 자동 차단 없음. 팀원 Production Training은 별도 제작 중이므로 수정 금지 |
| 다음 행동 | AI 추적/리시/재점유 화면 확인 → TestMap Gate/HUD → Acro/Shotgun/Weather 체감 확인 |
| 다음 기능 | `TUT-05 완료 → TUT-04 실제 두 Lap → Mission 목표 Rule 데이터화·Jamming` |
| 이후 | Flight 실패 세부 규칙, AI/MG·Jamming과 실제 비주얼 통합 |
| Git 처리 | Unreal `dc655ac`, 문서 `8e4f1cf`가 각각 origin/main과 일치. Source/Test와 이번 문서는 로컬 변경이며 Commit·Push하지 않음 |
| 협업 Git | 15:56 GitHub Desktop 자동 Stash에서 개발 파일만 선택 복구. Stash는 안전 확인 전까지 보존 |

## 2026-09-17 — 개인화기 추적·리시 포기·NPC 회전 안정화 마감

- 같은 Shotgun 병사만 제자리에서 Yaw가 왕복하던 화면 증상을 Rifle과 비교했다. Shotgun은 짧은 사거리 때문에 추적 상태에 들어갔고, 0.35초마다 거의 같은 목적지로 `MoveToLocation`을 다시 발행해 이동/회전을 계속 초기화하는 것이 핵심 원인이었다. 최소 상태 보장시간 자체가 원인은 아니었다.
- `FDroneNPCEngagementPolicy`를 분리해 `Fire / Pursue / Disengage` 결정을 테스트 가능하게 만들었다. 개인화기 사거리 밖에서는 공중 표적을 NavMesh로 투영해 추적하고, 진행 중 목적지가 기본 150cm 이상 바뀐 경우에만 MoveTo를 갱신한다.
- 후속 화면 확인에서 사거리 경계가 애매할 때 다시 왕복하는 증상을 재현했다. 1,590↔1,610cm 반복 입력에서 기존 단일 1,600cm 경계가 Fire/Pursue를 5회 뒤집는 Red를 만들었다. 공간 Hysteresis는 사거리 안에서도 계속 접근하거나 사거리 밖에서 멈추는 구간을 만들므로 최종 폐기했다. 무기 Component와 같은 3D 실제 사거리 안이면 즉시 정지·Fire, 밖 판정이 기본 0.2초 지속될 때만 Pursue한다. 짧은 경계 노이즈는 시간 확인으로 거르고 사거리 안 복귀는 지연하지 않는다.
- 개인화기 교전 상태는 순간 `CanFire` 값이 아니라 거리 정책으로 정한다. 탄창이 비어도 근거리에서 추적 상태로 잘못 빠지지 않고 정지 교전 경로에서 재장전/발사를 다시 시도한다.
- 전투 시작점 기준 기본 3,000cm 리시, 2.5초 무진행 한계, 3초 재감지 Cooldown과 85% 복귀 반경을 추가했다. 범위를 벗어나거나 접근 불가하면 사격·이동·예약을 정리하고 순찰로 복귀한다. 모든 값은 Controller Blueprint Class Defaults에서 조정 가능하다.
- NPC Character는 역할 BP가 저장한 과거 설정과 무관하게 BeginPlay에서 이동 회전 계약을 복구한다. 추적 중에는 Controller가 실제 수평 속도 방향으로 몸 Yaw를 보간하고 Bone Gaze도 같은 이동 벡터를 보며, 정지 사격/엄폐에서만 Drone 방향 몸 Yaw를 사용한다. 이동 경로와 표적 직선 방향이 달라도 몸과 고개가 서로 반대로 선택하지 않는다.
- 리시 포기 중 StateTree를 동기 `RestartLogic()`하던 경로에서 `Reentrant call to StartTree`를 재현했다. 순찰 재시작을 다음 Tick으로 예약해 현재 Task 종료와 분리했다.
- 넓은 PIE 테스트는 수동 Sight 자극을 실제 Perception과 분리하고, 두 Hostile의 리시 안에 시험 Drone을 배치하며, 같은 맵의 무인 자동포탑 피해를 0으로 격리했다. Production Map/Asset은 수정하지 않았다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `Drone.AI.PersonalWeaponEngagementPolicy`, `Drone.AI.SmartObjectFoundationDefaults`, 경계 흔들림·몸/시선 이동 정렬·사거리 진입 즉시 정지를 확장한 `Drone.AI.ShotgunSystemsTestMapPIE`, `Drone.AI.NPCPerceptionSearchPIE`, `Drone.AI.NPCGreyboxAssets`가 최종 `5/5 Success`다. 마지막 넓은 PIE는 감지·MG 경합·개인화기 대체·사수 사망 후 재점유·Lost/Search·순찰 복귀 전체를 통과했고 StateTree 재진입 오류도 0이다.
- 팀원이 `BP_NPC_Friendly_Base` 역할 Mesh를 Manny에서 `/Game/QuantumCharacter/Mesh/SKM_QuantumCharacter`로 변경한 뒤 자산 회귀의 기대값만 옛 경로로 남아 있던 실패를 확인했다. Blueprint/Asset은 수정하지 않고 테스트 기대 경로만 현재 역할 Mesh로 갱신해 `NPCGreyboxAssets`를 Red→Green 전환했다.
- 임시 `[DEBUG-AI-*]` 로그는 모두 제거했고 `git diff --check`는 공백 오류 없이 통과했다. Unreal Editor는 종료 상태이며 Commit·Push는 하지 않았다. 다음 확인은 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`의 Rifle/Shotgun 추적 무떨림·리시 포기·MG 재점유 화면이다.

## 2026-09-15 — Gate 임시 16각 Ring을 Trigger 정합 4변 Frame으로 교체

- 화면에서 16개 Cube 조각의 끝이 튀어나오고 틈이 보이며 붉은 Box Trigger와 경계가 맞지 않는 문제를 확인했다.
- TDD 경계를 `표시 Frame 안쪽 크기 = 실제 Trigger/승인 범위`, `표시되는 변 = 4개`, `기존 3상태 색 유지`로 잡았다. 변경 전 테스트는 표시 16개와 정사각형 모서리 통과 거부를 재현해 실패했다.
- `ADroneTrainingGate`는 기존 Blueprint 직렬화 호환을 위해 16개 Visual Component를 보존하지만 앞의 4개만 상·하·좌·우 Cube Bar로 표시한다. Corner는 겹치거나 벌어지지 않게 맞물리고 Visual Collision/Overlap/Nav는 계속 꺼져 있다.
- `통과 영역 반쪽 크기`가 Frame 안쪽과 Box Trigger를 함께 정하고 `프레임 굵기`가 테두리 굵기/깊이를 정한다. 예전 `GateRadiusCentimeters`는 `Tutorial|Gate|Legacy`의 미사용 호환값으로 남겼다.
- 승인 판정도 원형 반경 검사에서 Actor Local Y/Z 정사각형 검사로 바꿔, 화면 Frame 안쪽 모서리를 통과했는데 실패하는 불일치를 제거했다. 순서·정방향·중복 방지와 `통과 전/현재 목표/통과 후` 색 전환은 변경하지 않았다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `Drone.Tutorial.TrainingGateSequence`와 `Drone.Tutorial.TutorialSystemsTestMap`이 각각 1/1 성공했다. Production `/Game/Drone/Maps/Lvl_DroneTraining`은 열거나 저장하지 않았고 TestMap 화면 확인만 남았다.

## 2026-09-11 — 팀원 Pull·Discard 자동 Stash 복구와 푸시 준비

- GitHub Desktop Pull 중 Hostile Rifle/Shotgun `.uasset` 교체가 Windows의 일시적 파일 점유로 실패했다. 재시도 과정에서 `Discard Changes`를 눌렀지만 Desktop이 직전 변경을 15:56 자동 Stash에 보존한 것을 확인했다.
- 이후 `44303a1` Fast-forward는 성공했다. Training Map SHA-256은 원격 LFS OID `ea66a333...`와 일치하고 Shotgun 9개·STF 492개가 정상 추적된다.
- 자동 Stash 전체에는 Map 삭제와 이미 원격에 들어간 대형 에셋도 함께 있어 그대로 적용하지 않았다. TUT-05 Source/Test 9개와 새 `ConfigureAutomaticTrainingGates.py`만 선택 복구했고 Stash는 삭제하지 않았다.
- 팀원 Hostile Rifle/Shotgun BP는 각각 Modular Insurgents `SK_Preset1`/`SK_Preset2`를 사용한다. 자산 테스트의 Manny 고정을 역할별 실제 Mesh 계약으로 바꿨고 NPC 자산·기본 PIE·Greybox PIE 3개가 통과했다. `NPCPerceptionSearchPIE`의 MG 사망 사수 정리/재점유는 재현되어 별도 실패로 남는다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build는 성공했다. Pull 직후 전체 `Drone.` 40개 중 36개가 성공했고 4개가 실패했다. Mesh 기준 수정 뒤 알려진 실패 테스트는 `NPCPerceptionSearchPIE`, `TrainingAssets`, `TrainingPIESmoke` 3개다.
- 최신 Training Map에는 Gate Actor 18개가 있지만 Course Sequence는 4개다. Recon/Impact/Payload 역할 표적과 Carryable Payload도 모두 0개여서 `TrainingAssets`, `TrainingPIESmoke`가 실패했다. 393MB 원격 맵을 임의 고정 좌표로 다시 저장하지 않고 화면에서 의도와 위치를 확인한 뒤 수정한다.
- `git diff --check`와 새로 받은 LFS Object 전체 `git lfs fsck`는 통과했다. Commit·Push는 하지 않았고, 전체 자동화가 다시 통과하기 전까지 현재 상태를 완전 검증으로 표시하지 않는다.

## 2026-09-11 — TUT-05 Spline 기반 자동 Ring Gate 구현·자동 검증

- 공통 Mission Flow, Drone 선택, 목표 패널, Training Lap 성공과 Drone 사망 실패 연결은 이미 구현된 상태로 확인했다. 이번 작업에서 같은 Flow를 중복 작성하지 않는다.
- `ADroneTrainingCourse`에 자동/수동 Gate 모드를 분리했다. 자동 모드는 수치로 Ring 개수, 균등 분배/고정 간격, 시작·끝 여백, 전체 거리 이동, Index별 거리 이동, 로컬 위치·회전·Scale과 Gate Class를 조정한다.
- 자동 Ring은 `UChildActorComponent`로 Course가 소유하며 현재 Spline 거리의 위치와 접선 회전을 따른다. Spline 또는 수치를 바꿀 때 이전 생성 Component를 Tag로 제거한 뒤 다시 만들어 중복을 막는다.
- 자동 모드는 생성 Ring 배열, 수동 모드는 기존 `OrderedGates`를 Sequence의 단일 기준으로 사용한다. `CourseId`, `GateIndex`, `SegmentDistance`는 기존 Sequence 계약으로 동기화한다.
- `Drone.Tutorial.TrainingCourse`에 5개 자동 Ring 생성, Spline 위치·방향·Index·거리, Sequence 유효성, 반복 재생성 중복 0, 자동 모드 종료 정리를 검사하는 항목을 추가했다.
- 첫 빌드는 `TArray<float>`에 허용되지 않는 `Units` UHT 메타데이터 한 건을 발견해 제거했다. 사용자 Editor 종료 뒤 MSVC 14.51.36257로 `DroneEditor Win64 Development` Build를 통과했다.
- 15:31의 `/Game/Drone/Maps/Lvl_DroneTraining` 검증본은 사용자 조정값인 자동 Ring 14개, 수동 Gate 0개였다. 별도 명령줄 프로세스 재로드에서 Gate Class·개수·Sequence와 수동 Gate 부재를 확인했다.
- 자동 Map 전환 뒤 자산 테스트의 Construction 재실행 포인터와 PIE 복제 시 Child Actor Cache 복원 문제를 발견해, 생성 Component Tag 재검색·정렬로 보강했다. 최종 `Drone.Tutorial` 7/7이 경고·오류 없이 통과했다.
- 전체 Suite에서는 RecastNavMesh 초기화 경고가 선행 Map 상태에 따라 1회 또는 2회 발생하는데 기존 테스트가 정확히 2회로 고정돼 2건이 실패했다. 기능 검증은 유지하고 예상 경고 1회 이상을 허용하도록 바꾼 뒤 전체 `Drone.` 40/40을 통과했다.
- 전체 Blueprint Compile은 실패 0이다. 종료 요약의 29 warnings는 기존 Battlefield Quinn Pose GUID 경고이며 이번 Course/Map 변경의 Blueprint 경고가 아니다. Training Map Check는 0 errors/0 warnings다.
- `git diff --check`, `git lfs fsck`를 통과했고 Unreal Editor와 명령줄 검사 프로세스는 종료 상태다. 코드·Map·테스트·문서는 로컬 미커밋이며 사용자가 Commit/Push한다.
- 이후 사용자가 Training Map을 의도적으로 덮어쓰는 중이라고 알려 현재 Map 변경을 수정·복구하지 않았다. 교체 완료 뒤 최종 Ring 수·Sequence·Map Check와 전체 순서 비행을 다시 확인한다.
- 후속 요청에 따라 `AutomaticGateSplineDistancesCentimeters`와 `AutomaticGateLocalOffsets`를 추가했다. 배열 Index별로 Spline 절대 거리와 X 진행방향/Y 좌우/Z 높이를 직접 지정하며, 항목이 없는 Ring은 기존 균등/고정 배치와 0 위치 보정을 유지한다.
- `ConfigureAutomaticGateOverrides` Blueprint 함수와 5개 Ring의 서로 다른 절대 거리·로컬 위치 자동화 검증을 추가했다. 저장 맵의 Ring 수를 4로 고정하던 자산/PIE 테스트도 2개 이상이며 Course·Sequence 수와 일치하는지를 검사하도록 일반화했다.
- `BP_DroneTrainingGate`에서 `통과 전`, `현재 목표`, `통과 후` 색을 한글 Class Defaults로 편집하고 Blueprint Graph의 `Set Gate State Colors`로 런타임 변경할 수 있게 했다.
- 후속 변경 뒤 MSVC 14.51.36257 Editor Build, Tutorial 7/7, 전체 `Drone.` 40/40, 저장 맵 재로드 `count=14/manual=0`, Map Check 0/0을 통과했다. `BP_DroneTrainingCourse`와 `BP_DroneTrainingGate`를 포함한 전체 Blueprint Compile은 오류 0이며 29 warnings는 기존 Battlefield Quinn Pose GUID다.
- Mission 다음 구현은 목표 종류·필요 수량·제한 시간·대상 ID를 데이터화하고 정찰/투하/파괴/귀환 Event를 Director에 연결한 뒤 Jamming Rule로 확장한다.

## 2026-09-09 — Rotor 외형 회전·Blueprint 튜닝·역할 표적 BP 전환

- `ADronePrototypePawn`이 `DroneRotor` Component Tag 또는 기존 `Rotor` 이름을 가진 Static Mesh를 수집해 Tick에서 회전시키도록 구현했다. 이동·Collision에는 영향을 주지 않으며 사망 시 정지한다. FPV·Scout는 Rotor 4개, Drop은 6개에 Tag를 저장했다.
- 첫 화면 확인에서 Rotor가 자기 자리가 아니라 기체 주위를 크게 공전했다. 공급 Drone Pack의 일부 분리 Mesh는 Asset Pivot이 기체 원점에 있고 날개 Geometry만 떨어져 있기 때문이었다. 회전 전후 Static Mesh Bounds 중심의 Parent-space 위치 차이를 Relative Location으로 상쇄해 각 Rotor가 자기 Bounds 중심에서만 돌도록 수정했다.
- 후속 화면 확인에서 FPV 자폭 Drone의 Rotor 4개가 본체 중앙에 겹친 상태를 확인했다. FPV 전용 Rotor Mesh에는 이미 본체 기준 네 모서리 Geometry 좌표가 들어 있는데 BP Component Location이 반대 Offset을 한 번 더 적용해 중심을 `(0, 0)`으로 상쇄한 것이 원인이었다. FPV Rotor A~D Component Location을 원점으로 복구해 Mesh 내부 좌표대로 네 암 끝에 배치했다.
- Pawn BP Class Defaults에 `Rotor Visual Spin Enabled`, 초당 회전 각도, 로컬 회전축, 교차 방향, Component Tag를 노출했다. 역할별 BP에서 모델 축과 체감에 맞춰 수정할 수 있다.
- `Override Definition Flight Profile In Blueprint`를 켜면 Data Asset 대신 Pawn BP의 Flight Profile로 최대 속도·가속/감속·Yaw·Pitch/Roll·시작 시점·체력 등 비행 프로필을 한 번에 덮어쓸 수 있다. 기본값은 꺼짐이라 기존 DA_Drone 설정을 유지한다.
- NPC Controller BP에는 Sight/Lose Sight 거리, 주변 시야각, 자극 유지시간과 진영 감지 옵션을 노출했다. AnimBP에는 Spine/Neck/Head 시선 회전 분배 비중을 노출했다. 기존 런타임 캐시·안전 상수·상태값은 조정값이 아니므로 내부에 유지한다.
- Training의 Native Recon/Impact/Payload 표적을 `/Game/Drone/Abilities/RoleTargets/BP_RoleTest_*` 3개로 교체했다. 표적 Mesh/Scale과 안내 문구·색·크기·위치·회전을 BP Class Defaults 또는 맵 배치 Instance에서 조정할 수 있다.
- VS 업데이트 뒤 설치된 MSVC 14.51.36231 Toolchain(cl 19.51.36257)으로 `DroneEditor Win64 Development` 전체 Build가 성공했다. 이전 14.38 실패는 UE 5.8 SharedPCH와 구형 컴파일러의 호환 문제였고 프로젝트 코드 오류가 아니었다.
- `FlightProfiles`, `VisualBank`, `RoleDroneAssets`, `TrainingAssets`, `NPCGreyboxAssets`, `NPCPerceptionSearchPIE` 집중 자동화 6/6 성공. Pivot 보정 뒤 `VisualBank`, `RoleDroneAssets` 2/2를 다시 실행해 FPV·Scout·Drop 모두 회전값은 변하고 실제 Rotor Bounds 중심은 0.1cm 오차 안에서 고정됨을 확인했다. FPV 배치 보정 뒤 `FPVAsset`, `VisualBank`, `RoleDroneAssets` 3/3을 다시 통과해 Rotor 중심이 본체에서 20cm 이상 떨어지고 네 사분면에 하나씩 배치됨도 확인했다. 전체 Blueprint 420개는 컴파일 실패 0이며, 종료 요약의 29 warnings는 기존 Battlefield Quinn Pose GUID 불일치다. Training Map Check 0 errors/0 warnings, `git diff --check`, `git lfs fsck`도 통과했다.
- 남은 작업은 Editor에서 Rotor 회전축·교차 방향·속도, 역할 표적 표시, 역할별 기능과 드랍 화물 루프를 화면으로 확인하는 것이다. 수치 보정은 해당 Pawn/Controller/AnimBP/표적 BP의 Class Defaults에서 처리한다.

## 2026-09-09 — 팀원 LFS 자산 복구와 Trello 정리

- GitHub Desktop에서 Stashed Changes Restore를 반복하면 `test1.umap`, `M_Start.uasset: needs merge`, `could not write index`가 발생했다. 첫 Restore가 이미 두 LFS 바이너리 충돌을 만든 상태라 두 번째 적용이 거부된 것이며 Stash 자체는 보존됐다.
- 현재 main의 손상된 277/274-byte 충돌문자 LFS Object는 선택하지 않고 사용자 결정에 따라 팀원 Stash 버전을 보존했다. `test1.umap` 48,817 bytes와 `M_Start.uasset` 11,456 bytes 모두 Unreal Package Magic과 팀원 OID를 확인했다.
- 두 파일만 충돌 해결·Stage한 뒤 사용자가 `ac88992`로 Commit/Push했다. Fetch 뒤 `HEAD=origin/main=ac88992`, 원격 LFS OID 일치와 Clean 작업 트리를 확인했다.
- `.vsconfig`는 공유 가능한 구성요소 목록이지만 Stash의 14.44 Toolset 변경은 UE 5.8 기준에 맞지 않아 제외했다. 기존 14.50 파일을 유지했고 복구 Commit에 포함하지 않았다.
- 지금까지 구현한 기능과 앞으로 할 작업을 Trello List/카드/체크리스트 형식으로 [`DRONE_TRELLO_BOARD_2026-09-09.md`](DRONE_TRELLO_BOARD_2026-09-09.md)에 정리했다.

## 2026-09-08 — DR-DROP-02 맵 배치형 운반 화물

- `ADroneDroppedPayload`에 맵 Pickup, Carried, 투하 상태를 추가하고 Pickup 상태에서는 충돌 투하 판정을 막았다. `UDronePayloadDropComponent`의 Primary는 적재 중이면 투하하고 비어 있으면 300cm 안의 가장 가까운 사용 가능 화물을 한 번 검색한다.
- Pickup 성공 시 맵의 실제 Payload Actor를 `ADronePrototypePawn.PayloadCarryAnchor`에 붙인다. 재투하 때 새 Actor를 복제하지 않고 같은 Actor를 분리해 낙하시키며, 역할 재설정 때 운반 중 화물은 월드 Pickup 상태로 안전하게 돌려놓는다.
- `/Game/Drone/Abilities/Payload/BP_DroneCarryablePayload`를 `ADroneDroppedPayload` 자식으로 생성했다. 외형은 `/Game/FC_MilitaryCamp/Models/MilitaryModels/SM_MilitaryCrate_01`, 시작 상태는 Carryable이며 Training Map `(300, -300, 70)`에 `RoleTest_CarryablePayload` 한 개를 배치했다.
- Mission 역할 안내는 Drop 적재 수가 0이면 `화물 가까이서 좌클릭/RB 적재`, 적재 중이면 `좌클릭/RB 화물 투하`를 표시한다. 탑뷰 우클릭/LB는 유지한다.
- MSVC 14.51.36256 Editor Build가 성공했다. `Drone.Prototype` 7/7, `Drone.Integration` 3/3, `Drone.Tutorial` 7/7, `Drone.Flow` 5/5로 집중 자동화 22/22가 전부 통과했다.
- 생성 Commandlet은 `DRONE_CARRYABLE_PAYLOAD|OK`와 저장 파일을 확인했다. 종료 코드 1은 별도 LFS 충돌 Pointer `test1.umap`, `M_Start.uasset`의 Asset Registry 오류이며 두 파일·`.vsconfig`·`Drone.cpp //test`는 건드리지 않았다. Commit·Push하지 않았다.
- 첫 화면 확인에서 착지 직후 투하물이 사라졌다. 원인은 기존 일반 Payload가 모든 충돌 뒤 0.1초 후 제거되는 공용 처리였다. Carryable 이력이 있는 Actor는 낙하 중 자동 수명을 끄고 착지 후 그 자리에 정지·표시·재적재 가능 상태로 남기며, 일반 1회용 Payload만 기존 제거 규칙을 유지하도록 분리했다. `BP_DroneDropIntegration.PayloadDropComponent.PayloadClass`도 새 크레이트 BP로 바꿔 첫 투하부터 같은 규칙을 사용한다. 수정 Build와 `Drone.Prototype.RoleAbilities`, `Drone.Integration.RoleDroneAssets` 각 1/1이 통과했다.
- 다음은 Front-end→Training에서 Drop을 선택해 선적재 화물을 먼저 투하하고, 크레이트 적재·하단 부착·재투하의 크기와 위치를 화면으로 확인하는 것이다.

## 2026-09-08 — 패드 역할 기능·시점 입력 마무리

- `IA_DronePrototype_PrimaryAbility`에 패드 RB, `SecondaryAbility`에 패드 LB를 추가했다. 역할별 의미는 Mouse와 같으며 정찰 Scan/취소, FPV Arm/Disarm, 드랍 투하/탑뷰로 분기한다.
- 기존 `P` 전용 시점 전환에는 패드 Y를 추가했다. IMC는 18개에서 RB/LB/Y를 더한 총 21 Mapping이다.
- 입력 재생성 스크립트는 Action별 모든 예상 Key를 집합으로 검증하도록 바꿨다. PIE Input Lifecycle은 P/Y, 좌클릭/RB, 우클릭/LB가 각각 정확히 한 번 존재하고 Pawn 소유 Binding이 재시작 3회 동안 중복되지 않는지 검사한다.
- MSVC 14.51.36256 `DroneEditor Win64 Development`가 성공했고, 최종 `Drone.Prototype` 7/7이 통과했다. 직전 동일 변경 묶음의 Integration 3/3, Tutorial 7/7, Flow 5/5 결과도 유지되어 집중 자동화는 22/22다.
- 확인용 Editor는 `/Game/Drone/Maps/Lvl_DroneFrontEnd`로 다시 열었다. 실제 Controller 버튼 압력·모델 크기·폭발/투하 체감은 사용자 수동 확인으로 남긴다.

## 2026-09-08 — DR-ROLE-TARGET-01 역할별 모델·기능 시험장

- 세 Definition이 같은 FPV 외형을 공유하던 임시 상태를 분리했다. Scout는 `/Game/Drone/Integrations/RoleDrones/BP_DroneScoutIntegration`과 DroneSpy 6파트, FPV는 기존 `BP_DroneFPVIntegration` 5파트, Drop은 `BP_DroneDropIntegration`과 Delivery 8파트를 사용한다. 공통 입력·카메라·비행 C++ 기반은 그대로 재사용한다.
- Drop Pawn에 `DroneCarriedPayload` Tag의 임시 Cube 적재물을 달았다. 역할 활성화·재장전 때 보이고 실제 투하하면 즉시 숨는다. `UDronePayloadDropComponent`는 지정 Target이 없거나 이미 완료됐으면 가장 가까운 미완료 `UDronePayloadTargetComponent`를 클릭 시점에 자동 선택한다.
- `ADroneReconRoleTestTarget`, `ADroneImpactRoleTestTarget`, `ADronePayloadRoleTestTarget`을 추가하고 `Lvl_DroneTraining`에 각 1개를 배치했다. 표적에는 역할별 한글 조작 문구가 있고 코스 Gate/안내선 판정과 독립이다.
- FPV 자폭에는 제공 `/Game/Drone/ThirdParty/ArmyVFX` Niagara와 `/Game/Drone/ThirdParty/InfantrySFX` Explosion Cue를 연결했다. Arm/Disarm/Detonate 상태 Event도 UI가 구독한다.
- Mission 목표 Widget은 선택 Pawn을 직접 주입받고 정찰 진행률·완료 수, FPV 안전/무장, Drop 적재/성공/탑뷰 상태를 Event 기반 한글 텍스트로 표시한다. Tick Actor 검색은 추가하지 않았다.
- 재생성 도구 `BuildDroneRoleIntegrations.py`, `BuildDroneRoleTestArena.py`를 추가하고 기존 `BuildDroneFlightProfileAssets.py`를 역할별 Class 매핑으로 갱신했다.
- MSVC 14.51.36256 `DroneEditor Win64 Development` Build 성공. 자동화는 Prototype 7/7, Integration 3/3, Tutorial 7/7, Flow 5/5로 총 22/22 통과했다. Map Check는 Training PIE에서 0 errors/0 warnings다.
- Commandlet 종료 코드는 미해결 `test1.umap`, `M_Start.uasset` LFS 충돌 Pointer 때문에 Asset Registry 오류를 기록할 수 있으나, 기능 스크립트 실행과 관련 테스트는 모두 성공했다. 두 충돌 파일과 `.vsconfig`, `Drone.cpp //test`는 이번 기능 범위에서 건드리지 않았다.
- Commit·Push는 사용자가 수행한다. 다음은 Editor에서 세 모델 크기/방향, 정찰 좌클릭/RB 유지와 우클릭/LB 취소, FPV 좌클릭/RB 무장 후 고속 충돌 폭발, Drop 우클릭/LB 탑뷰와 좌클릭/RB 투하·적재물 소멸을 수동 확인하는 것이다.

## 2026-09-08 — 공유 main 최신화와 Pull/Stash 충돌 감사

- Fetch 결과 Unreal `main=origin/main=63f60c1`, 문서 `main=origin/main=d30e098`로 원격과 일치한다. `63f60c1`은 역할 기능 3종·공통 역할 입력·FLOW-04~08을 58개 변경 파일로 공유한 Commit이다.
- Unreal은 09:20 Fast-forward Pull 직후 자동 복원된 Stash와 Upstream 사이에 `test1.umap`, `M_Start.uasset` 양쪽 추가 충돌이 남았다. Worktree의 두 파일은 `.uasset/.umap` 본문이 아니라 충돌 마커가 삽입된 LFS Pointer라서 그대로 Unreal 저장·Stage·Commit하지 않는다.
- Upstream/HEAD 후보는 `test1.umap` 36,998,062 bytes·`M_Start.uasset` 11,569 bytes이고, Stash 후보는 각각 48,817 bytes·11,456 bytes다. 두 바이너리는 내용 병합이 불가능하므로 보존할 버전을 선택해야 한다.
- `.vsconfig`는 Index 14.44와 Worktree/HEAD 14.50이 서로 다르고 `Drone.cpp`의 `//test`가 Staged로 돌아왔다. 이전 규칙대로 `//test`는 기능 변경과 분리해 제거하고 Toolchain은 실제 설치·빌드 기준으로 하나만 남겨야 한다.
- UE 5.8.2 Editor가 D 드라이브 프로젝트를 정상 로드했다. 수동 로그에서 Front-end→Training Map, FPV Definition 적용과 Pawn Possess까지 확인했고 Fatal/Crash는 없었다.
- 실제 Spawn Class는 `BP_DronePrototypePawn_C_0`이며 `모든 Prototype Input Action이 아직 배정되지 않았다`는 프로젝트 진단이 발생했다. 후속 Asset 대조에서 세 Mission Definition의 Pawn Class가 모두 기본 Prototype을 가리키고 있음이 확정됐다.
- 공유 전 기록의 Flow 5/5·Prototype 7/7·새 PIE 3/3은 보존한다. 현재 PC의 Saved Automation Report는 없으므로 충돌 선택과 역할 입력 연결 수정 뒤 Editor Build, `Drone.Flow`, `Drone.Prototype`, 수동 좌/우 클릭 역할 기능을 다시 검증한다.

## 2026-09-08 — Mission Drone 모델·입력 누락 원인 확정과 수정 준비

- `DA_Drone_Scout_Greybox`, `DA_Drone_FPVStrike_Greybox`, `DA_Drone_Drop_Greybox` 내부 참조를 직접 대조했다. 세 Asset 모두 `BP_DronePrototypePawn`을 참조해 Mission 선택 뒤 기본 Cube/Prototype 표현과 미배정 Input 경고가 재현됐다.
- 실제 Drone Pack 본체·로터 4개·Loop Sound와 Prototype/역할 Input Action은 `/Game/Drone/Integrations/DronePackFPV/BP_DroneFPVIntegration`에 존재한다. 역할 기능 C++ 자체가 사라진 것이 아니라 `ADroneMissionPlayerController::StartSelectedDrone()`이 Definition의 잘못된 `PawnClass`를 그대로 Spawn한 연결 오류다.
- `BuildDroneFlightProfileAssets.py`가 세 Definition 모두 Integration Pawn Class를 명시적으로 저장하도록 수정했다. `Drone.Prototype.FlightProfiles`는 세 Definition의 Class가 정확히 Integration Pawn인지 검사하고, `Drone.Flow.MissionEntryPIE`는 최초 Scout와 재시도 Drop 출격에서 실제 Spawn Class를 검사하도록 강화했다.
- 기존 테스트는 Definition Class가 단지 `ADronePrototypePawn` 하위인지 확인했고 Integration Asset 테스트를 별도로 수행했기 때문에 두 연결이 달라도 통과할 수 있었다. 이번 정확한 Class 검증으로 같은 회귀를 막는다.
- Editor를 종료한 뒤 스크립트를 실행해 세 Data Asset에 Integration Pawn을 실제 저장했다. `DroneEditor Win64 Development`, `Drone.Prototype` 7/7, `Drone.Flow` 5/5, `Drone.Integration.FPVAsset` 1/1이 통과했다. Flight Profile은 세 역할 모두 Integration Class를 생성했고 Mission PIE 3회는 Scout와 재시도 Drop을 매회 Integration Class로 Spawn/Possess했다. 기존 `does not have all prototype Input Actions assigned yet` 경고는 새 Mission 실행 로그에서 0건이다.
- 자동 검증은 모델 Component와 Class 연결을 확인하지만 실제 렌더 화면·스피커·손 조작을 대신하지 않는다. Front-end에서 세 역할을 각각 출격해 외형과 조작을 확인해야 한다. `test1.umap`, `M_Start.uasset` LFS 충돌은 이 수정과 무관하게 남아 있고 Commit·Push는 사용자가 담당한다.

## 2026-09-08 — FLOW-08 새 실행 3회 반복 완료

- `DroneMissionEntryPIE`가 하나의 PIE를 재활용하지 않고 완전히 종료한 뒤 새 PIE를 시작하도록 Lazy Start와 종료 안정화 대기를 추가했다. Engine Start 명령이 생성 즉시 `EndPIE`를 구독해 다음 실행이 조기 실패하던 문제를 실제 실행 차례에 생성하는 방식으로 고쳤다.
- 각 실행은 `Opening→Lobby→Briefing→Training Map→Scout 성공→Retry→Drop Health 0 실패→Lobby`를 끝까지 수행한다. Root Widget 1, Map 요청 1, 선택 전 Drone 0, 출격 뒤 Drone 1·Director 1, Finish Event 1, 로비 복귀 뒤 Drone 0을 검증한다.
- UI 전용 GameMode는 빈 Pawn/HUD Class 대신 비-Drone `ASpectatorPawn`과 기본 HUD를 사용해 `SpawnActor failed because no class was specified` 경고를 0건으로 만들었다.
- 최종 `DroneEditor Win64 Development` Build, `Drone.Flow` 5/5와 `Drone.Prototype` 7/7이 통과했다. 빈 시험 World의 기존 RecastNavMesh 경고만 남았으며 기능 실패는 아니다.
- FLOW-01~08 자동화 게이트를 모두 닫았다. 다음은 Editor 수동 Vertical Slice와 TUT-04 두 Lap 확인이다. Commit·Push하지 않았다.

## 2026-09-08 — DR-ROLE-INPUT-01 공통 역할 입력

- `IA_DronePrototype_PrimaryAbility`, `IA_DronePrototype_SecondaryAbility` Boolean Action을 만들고 `IMC_DronePrototype`과 `BP_DroneFPVIntegration` CDO에 연결했다. Mapping은 기존 16개에서 Mouse 2개와 Gamepad Shoulder 2개, 시점 전환용 패드 Y 1개를 더한 21개가 됐다.
- 최종 키를 확정하지 않고 Greybox 임시값으로 좌클릭/RB=1차, 우클릭/LB=2차를 사용한다. 정찰은 가장 가까운 유효 Target Scan/취소, FPV는 Arm/Disarm, 드랍은 Payload 투하/상단 Camera 전환으로 분기한다.
- 정찰 자동 표적 검색은 클릭 시점에만 World를 한 번 순회하며 Tick에서 Actor를 계속 찾지 않는다. 거리·화각·LOS와 완료 여부는 기존 Scan Component 단일 검증 함수를 재사용한다.
- `Drone.Prototype.RoleAbilities`에서 세 역할 분기와 상태를, `PIEInputLifecycle`에서 두 Action의 Mapping·Pawn 소유 Started Binding·3회 PIE 수명주기를 확인했다. 전체 `Drone.Prototype` 7/7과 `Drone.Flow` 5/5가 재통과했다.
- Training Map에 실제 `UDroneReconScanTargetComponent`와 `UDronePayloadTargetComponent`가 붙은 시험 표식, 역할 상태 HUD는 아직 없다. 이는 `DR-ROLE-TARGET-01`로 분리한다. Commit·Push하지 않았다.

## 2026-09-08 — 역할 기능 3종·FLOW-04~07 완료

- 정찰은 `UDroneReconScanComponent`와 Target Component로 거리·화각·시야선 유지 중 진행하고 이탈 시 취소하며 한 번만 완료한다. FPV는 명시적 Arm과 최소 충돌 속도 뒤 1회 Radial Damage·자기 Health 0을 적용한다. 드랍은 기존 1/3인칭 상태를 복원하는 상단 Camera와 한 발 Payload·목표 접촉·재장전을 사용한다.
- `DA_Drone_Scout_Greybox`, `DA_Drone_FPVStrike_Greybox`, `DA_Drone_Drop_Greybox`의 구현 Capability를 각각 하나씩 활성화했다. `Drone.Prototype.RoleAbilities`와 Flight Profile 검증에서 다른 역할 기능 중첩이 없음을 확인했다.
- Front-end Root에 선택 Mission의 정적 Briefing·초기 목표와 종료 버튼을 추가했다. Controller는 정확히 한 번 선택 `MissionMap`을 열며 URL 전용 `DroneMissionGameMode`로 Map의 기존 Prototype GameMode를 이번 진입에만 덮어쓴다.
- Mission Map의 `UDroneSelectionWidget`은 세 역할 카드, 쉬운/실제 조작형, 안정/균형/고기동을 표시한다. 선택 전에는 비-Drone Spectator만 있고, 확정 뒤 Data Asset Pawn 한 대에 Profile과 이번 설정을 적용해 Possess한다.
- 새 `ADroneMissionDirector`는 출격 뒤 시작 요청을 한 번 소비하고 Data Asset 목표를 `UDroneMissionObjectiveWidget`에 Event로 보낸다. 현재 Training 연결은 Lap 완료=성공, Drone Health 0=실패인 Greybox이며 최종 Story 규칙은 아니다.
- `UDroneMissionResultWidget`의 성공/실패, 같은 Mission 재도전과 Front-end 로비 복귀를 구현했다. 로비 복귀 표지는 새 Front-end Controller가 한 번 소비한다.
- `DroneMissionEntryPIE`가 `Opening→Lobby→Briefing→Training Map→Scout 출격→Success→Retry→Drop 출격→Health 0 Failure→Lobby`를 실제 Map 전환으로 통과했다. `DroneEditor Win64 Development`, `Drone.Flow` 5/5, `Drone.Prototype` 7/7이 성공했다.
- 실제 Trailer Media, 최종 WBP Designer·Preview, 최종 성공/실패 규칙과 손 조작 체감은 미정/수동 대기다. Commit·Push하지 않았다. FLOW-08 결과는 바로 위 최신 절을 따른다.

## 2026-09-08 — Figma 기체 역할·조작 모드 분리

- 사용자 제공 Figma `Project:Droner`를 로그인된 Browser에서 읽기만 했다. 수정·댓글·공유 설정 변경은 하지 않았다.
- 현재 기획 역할로 정찰, 드랍, FPV 자폭, 광섬유, 지상 UGV, 장거리 타격을 확인했다. 최종 확정·완료 목록으로 해석하지 않는다.
- 잘못된 임시 기체 분류 `균형 정찰형/고기동형/안정 관측형`을 역할과 핸들링으로 분리했다.
- `EDroneMissionRole`, `EDroneGameplayCapability`, `EDroneControlMode`, `EDroneHandlingPreset`을 추가했다.
- `UDroneDefinition`에 플레이 가능 여부와 계획/구현 Capability 목록을 추가했다. 구현 기능은 계획 기능의 부분집합이어야 Validation을 통과한다.
- `ADronePrototypePawn`에 쉬운/실제 조작형과 안정/균형/고기동 변경 API·Blueprint Event를 추가했다. 실제 조작형은 낮은 자동 감속/선회 보조, Root Pitch/Roll, Local Up을 사용하는 Greybox이며 실제 모터 물리로 표현하지 않는다.
- Data Asset은 `DA_Drone_Scout_Greybox`, `DA_Drone_FPVStrike_Greybox`, `DA_Drone_Drop_Greybox` 3종으로 정리했다. 이 시점에는 역할 기능을 Planned로 시작했고 같은 날짜 후속 절에서 구현 Capability로 승격했다.
- `DroneEditor Win64 Development` Build 성공. `Drone.Prototype.FlightProfiles` 1/1과 `Drone.Flow` 3/3 성공.
- Unreal 기준 `main=origin/main=dbc0dd8`, 문서 기준 `main=origin/main=aaef93d` 위 로컬 변경이다. Commit·Push하지 않았다.
- 상세 가이드: [`DRONE_TYPES_AND_CONTROL_MODES.md`](../gameplay/DRONE_TYPES_AND_CONTROL_MODES.md)

## 2026-09-04 — DR-DMGFX-01 Drone 피격 본체·카메라 흔들림

- `UDroneHealthComponent`의 Blueprint `OnHealthChanged`는 유지하고 C++ 표현 수신용 Native Event를 추가했다. 모든 무기가 공용 Health Damage를 사용하면 별도 무기 분기 없이 같은 피격 반응을 실행한다.
- `ADronePrototypePawn`은 피해량을 25 Damage에서 최대 강도로 제한하고 작은 피해에는 최소 25% 강도를 준다. 기본 0.30초 동안 본체 최대 6°, Camera View 최대 5cm·1.5°를 18Hz로 흔들며 제곱 감쇠한다.
- 본체 흔들림은 기존 A/D Visual Bank와 합성하고 Camera는 기존 Additive Offset을 보존했다가 종료 시 복원한다. Actor 위치·Collision 회전·이동 속도에는 변화가 없다. 연속 피격은 시간을 다시 시작하고 더 강한 피해 강도를 유지한다.
- 첫 자동화는 Editor 임시 World에서 게임 실행 전용 Delegate 수명주기가 아직 시작되지 않는 차이를 발견했다. Construction·Runtime 모두 같은 Native Health Binding을 보장하도록 수정했고, 최종 `Drone.Prototype.DamageShake`가 Health Damage→흔들림→Camera 복원과 Collision 불변을 통과했다.
- 최종 MSVC 14.51.36256 Editor Build와 `DamageShake`, `VisualBank`, `GroundConformingSuspension`, `AutomaticTurretTargeting`, `NPCGreyboxAssets`, `FlightHUDTelemetryBinding` 6/6이 통과했다. 이어 `NPCPerceptionSearchPIE`에 실제 `UGameplayStatics::ApplyDamage`가 피격 흔들림을 정확히 한 번 늘리고 파괴 뒤 중복 피해는 다시 시작하지 않는 조건을 추가해 1/1 재통과했다. 빈 시험 World의 기존 RecastNavMesh 경고 외 실패는 없다.
- 실제 탄환 피격의 강도·멀미 체감과 연속 피격은 수동 확인 전이다. 방향성 반동, Gamepad 진동, HUD Flash, Sound·Niagara는 후속이며 Commit·Push하지 않았다.

## 2026-09-04 — VEH-GROUND-01 4점 지면 추종·DR-VBANK-01 Drone 외형 Roll

- 완전한 차량 물리 대신 앞좌·앞우·뒤좌·뒤우 네 지점의 Visibility Trace로 굴곡을 읽는 `ADroneGroundConformingVehicle`를 추가했다. 접촉점 세 개 이상에서 평균 높이와 접촉 평면으로 Z·Pitch·Roll을 계산하고 최대 28° 안에서 보간한다. Collision은 Query 전용이고 Chaos Simulation은 사용하지 않는다.
- 임시 Cube Body, Cylinder Wheel 네 개와 `TurretMount`를 분리했다. 수동 `SetDriveInput(-1~1)`과 Controller 없이 왕복하는 Greybox Auto Drive를 제공해 향후 실제 Vehicle AI와 시험 배치를 분리했다.
- `/Game/Drone/Vehicles/Blueprints/BP_GroundConformingVehicle_Greybox`를 만들고 `Lvl_NPCSmartObjectGreybox`의 정적 Carrier를 교체했다. `VehicleRoughRoad_01`~`05` 다섯 굴곡 노면을 추가하고 차량형 자동포탑을 `TurretMount`에 Attach했다.
- `ADronePrototypePawn`에 Collision 자식 `VisualTiltPivot`을 추가했다. 최초 구현은 A/D 좌우 입력만 최대 ±18° Roll했으나 수동 확인에서 전후 기울기 누락과 좌우 방향 반대가 발견됐다. W/S는 최대 ±14° Pitch(전진 기수 아래·후진 기수 위)를 추가하고 A/D Roll 부호를 반전했으며 복합 입력에서는 두 축을 동시에 합성한다. CameraBoom과 Collision은 기존 부모를 유지하며 실제 FPV Integration의 Body·Rotor 네 개를 Pivot 아래로 정리한다. `DroneNoVisualBank` Tag로 개별 Mesh를 제외할 수 있다.
- 보정 뒤 MSVC 14.51.36256 Editor Build가 성공했다. `Drone.Prototype` 5/5가 통과해 Pitch·Roll 방향과 복귀, Camera/Collision 불변, 피격 흔들림 합성, Pawn 기본값, Spawn/Possess 및 새 PIE 3회 입력 수명주기를 재검증했다. Move Action은 조작용 Triggered 1개와 외형 복귀용 Completed/Canceled 각 1개만 Pawn에 연결되는 계약으로 검사한다.
- MSVC 14.51.36256로 `DroneEditor Win64 Development` Build가 성공했다. 첫 실제 Compile에서 lambda capture와 Camera proxy 타입 접근 두 건을 바로잡은 뒤 최종 소스가 통과했다.
- `Drone.Vehicle.GroundConformingSuspension`, `Drone.Prototype.VisualBank`, `Drone.AI.AutomaticTurretTargeting`, `Drone.AI.NPCGreyboxAssets` 집중 4/4가 성공했다. 실제 맵 자산 테스트는 차량 1·Wheel 4·굴곡 노면 5·포탑 Attach와 자동 주행 설정을 확인했다.
- 저장 자산 Validation은 자동포탑 BP 2개와 차량 BP를 재컴파일하고 `MAP_VALIDATION_OK|emplaced=1|vehicle=1|vehicle_attached=true|suspension=4|road=5`, Map Check 0 errors/0 warnings로 종료했다.
- 전체 Blueprint Commandlet는 0 errors, 29 warnings로 성공했다. 경고는 전부 공급사 `/Game/Battlefield/Demo/Characters/Mannequins/Rigs/Poses`의 Manny/Quinn Pose GUID 불일치이며 이번 `/Game/Drone` 자산의 Compile 실패가 아니다.
- 수동 화면 확인은 남았다. 자세한 조정과 보고 형식은 [`DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md`](../gameplay/DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md)를 따른다. Commit·Push는 사용자 요청대로 하지 않았다.

### 진행 중 — VEH-WHEEL-01·DR-CAM-01

- 차량 네 바퀴는 Throttle 표시값이 아니라 프레임 사이 실제 전진축 이동거리와 `WheelRadius`로 회전각을 계산하도록 C++를 작성했다. 전진은 누적각 증가, 후진은 감소하며 반속 이동에서는 회전속도도 절반이 되는 자동화 조건을 추가했다.
- Drone은 기존 FollowCamera 하나를 재사용한다. 3인칭은 CameraBoom이 Collision Root와 500cm Arm을 사용하고, 1인칭은 CameraBoom이 `VisualTiltPivot`에 붙어 Arm 0과 전방 Offset을 사용하므로 이동 Pitch·Roll과 피격 흔들림을 화면도 따른다. 전환 입력은 `P`로 설계했고 Enhanced Input Action·IMC 연결 및 PIE 검증을 이어서 적용한다.
- 최초 Link는 사용자가 실행한 `Drone - 언리얼 에디터`가 모듈 DLL을 잡아 중단됐다. 저장하지 않은 작업 보호를 위해 강제 종료하지 않았고 사용자 저장·종료 뒤 같은 Build를 재개해 성공했다.
- `/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_ToggleView`를 생성하고 `IMC_DronePrototype`의 P에 한 번 매핑했다. 전체 16 Mapping과 `BP_DroneFPVIntegration.ToggleViewAction` 저장을 재실행 가능한 `BuildDroneViewToggleInput.py`로 검증했다.
- 최종 MSVC 14.51.36256 Editor Build, 차량 회전비례·후진 조건 `GroundConformingSuspension` 1/1, P Mapping/Binding 새 PIE 3회와 Camera 추종을 포함한 `Drone.Prototype` 5/5가 성공했다. 빈 시험 World의 기존 Recast 경고 외 실패는 없다.
- 실제 화면에서 바퀴 Mesh 축 방향과 속도 체감, P 전환, FPV 위치·Mesh 가림·멀미 여부를 확인해야 한다. Commit·Push는 하지 않았다.
- 첫 차량 화면 확인에서 실제 이동과 바퀴 구름 방향이 반대인 것이 확인됐다. Greybox Cylinder의 `WheelVisualSpinDirectionMultiplier`를 `-1`에서 `+1`로 바꾸고 BP·맵 배치 Actor에도 같은 값을 저장·검증하도록 생성 도구를 보강했다. 방향 재확인은 남아 있다.
- 축 교정 뒤 MSVC 14.51.36256 Editor Build가 성공했다. 생성 도구의 동일 Cube 재배정 멱등성 오류도 수정한 뒤 차량 BP·맵 Actor를 저장했고, 새 프로세스 `VALIDATION_OK`, Map Check 0/0과 `GroundConformingSuspension` 1/1을 통과했다. 자동화의 유일한 경고는 빈 시험 World의 기존 Recast 경고다.

## 2026-09-04 — AI-AUTO-TURRET-01 설치형·차량형 무인 자동포탑

- 사용자가 요청한 차량 위 무인 포탑과 지면 설치형 자동포탑을 기존 유인 MG 베이스로 구현했다. 유인 MG의 3분할 회전 계층, 정렬 후 발사, Projectile/Trace 선택, Damage·탄속·분산은 한 경로를 공유하고 자동 탐지만 새 계층에서 담당한다.
- `ADroneAutomaticTurret`는 0.2초 간격으로 살아 있는 Prototype Drone을 검색한다. 첫 획득 거리와 더 큰 이탈 거리를 분리하고 Visibility 시야선을 요구해 사거리 경계 깜박임과 벽 너머 획득을 막았다. 표적 사망·이탈·차단 시 내부 MG 사용을 종료한다.
- `ADroneEmplacedAutomaticTurret`와 `ADroneVehicleAutomaticTurret`를 분리했다. 설치형은 높은 받침대와 저속/고피해 기본값, 차량형은 낮은 장착판과 긴 탐지·발사거리/빠른 연사 기본값을 사용한다. 값은 BP Class Defaults에서 교체 가능한 Greybox다.
- 차량형 Actor는 차량 Mesh Socket 또는 부모 Actor에 Attach해서 쓰며, Projectile과 Trace가 Attach Parent/Owner를 무시하도록 공통 MG 발사 경로를 보강했다. 탄환 Source에는 `AutomaticTurret`를 추가해 유인 MG 결과와 분리했다.
- `/Game/Drone/AI/AutomaticTurrets/Blueprints/BP_AutoTurret_Emplaced`, `BP_AutoTurret_Vehicle`를 생성했다. `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox` 우측 `(2600,1600)`에 설치형, `(2600,-1600)`에 차량 Carrier와 차량형을 배치했다. 차량형은 `AutoTurret_VehicleCarrier_Greybox`에 실제 Attach돼 있다.
- 재현용 `Tools/AssetMigration/BuildAutomaticTurretGreybox.py`는 두 BP와 소유 Actor 3개만 생성/검증하며 기존 맵 내용을 덮어쓰지 않는다. 읽기 전용 모드는 `DRONE_AUTO_TURRET_VALIDATE_ONLY=1`이다.
- `DroneEditor Win64 Development` Build 성공. `AutomaticTurretTargeting`, `SmartObjectFoundationDefaults`, `NPCGreyboxAssets` 3/3, 실제 맵 시작·종료 `NPCGreyboxPIE` 1/1이 통과했다. 전용 테스트는 Blocking Box가 시야를 가리면 획득하지 않고 Collision을 끄면 즉시 재획득하는 경로까지 확인했다. 자동화 보고서는 실패 0이며 빈 시험 World의 기존 Crowd/NavMesh 경고 1건만 있다.
- 화면 수동 확인은 남았다. 현재 포탑은 Prototype Drone만 적으로 보고 진영/우선순위·포탑 체력/파괴·최종 차량/포탑 Mesh·FX/SFX는 후속이다. 상세 조정법은 [`DRONE_AUTOMATIC_TURRET_GUIDE.md`](../ai/DRONE_AUTOMATIC_TURRET_GUIDE.md)에 기록했다.

## 2026-09-04 — 팀원 Plugin·Git·LFS 재현성 점검

- 중앙 저장소는 로컬·원격 모두 `6fd0e77`이고 작업 트리가 깨끗하다. 별도 `yook34/main=c845430`은 중앙의 정확한 조상이며 `18 Commit 뒤 / 0 Commit 앞`이지만, 이후 사용자가 팀원 작업 PC는 중앙 `gyeonliz/drone` 권한을 받아 중앙에서 직접 Pull한다고 확인했다. 따라서 이 Fork 상태를 팀원 증상의 원인으로 단정하지 않는다.
- 두 Head 사이에는 총 586개 파일 차이가 있고 그중 Content 520개, Source 61개다. AI, MG, Mission Flow, NPC/무기 Asset이 포함되므로 팀원 PC에서 기능과 화면이 다르게 열리는 직접 원인이 될 수 있다.
- 두 Head의 `Drone.uproject`와 `Plugins` 경로 차이는 0이다. 프로젝트 자체 `Plugins` 폴더와 Git Submodule도 없으므로 현재 확인 범위에는 공유되지 않은 Project Plugin이 없다.
- `Drone.uproject`가 명시한 UE 내장 Plugin 13개를 작업컴 UE 5.8.1 CL 56057345에서 대조했고 모두 존재했다. StateTree·SmartObjects·GameplayInteractions는 Runtime 의존성이고 ModelContextProtocol·Toolset 계열은 Editor 전용이다.
- 최근 Unreal 로그 20개에서 Plugin 로드 실패, `/Script` 누락, Unknown Class, Package Load 실패는 0건이었다. `Binaries`, `Intermediate`, `Saved`, `DerivedDataCache`는 정상적으로 Git 제외되며 PC마다 달라도 정상이다. 단, C++ 변경 뒤 각 PC에서 Project Files 재생성과 Editor Build가 필요하다.
- LFS 추적 Package는 4,563개이고 `git lfs fsck --pointers HEAD`가 통과했으며 중앙으로 Push할 LFS 객체가 없다. 팀원은 중앙 Branch를 Fast-forward한 뒤 `git lfs pull`을 실행해야 실제 Asset 본문을 받는다.
- Water는 현재 UE 설치에 존재하고 최근 로그에서 정상 Mount됐지만 `.uproject`의 직접 선언 목록에는 없다. 동일 5.8.1 환경에서는 현재 오류가 없으며, 팀원 동기화 뒤 Military Map에서 Water 관련 오류가 재현될 때만 명시 의존성 추가를 별도 변경으로 검토한다.
- 팀원 실행 순서는 새 [`DRONE_TEAM_SYNC_PLUGIN_CHECKLIST.md`](../git/DRONE_TEAM_SYNC_PLUGIN_CHECKLIST.md)에 고정했다. 먼저 원격/Commit/LFS를 맞추고, 그 뒤에도 재현될 때만 Plugin·생성 파일 문제로 분리한다.
- 두 번째 정밀 점검에서 `Drone.uproject`, `Config`, `Content`, `Source`, `Tools`, 향후 `Plugins`·`Build`에 Git Untracked/Ignore 필수 파일이 0개이고 외부 Junction/Symlink도 0개임을 확인했다. 현재 제외 대상은 `Binaries`, `Intermediate`, `Saved`, `DerivedDataCache` 등 재생성 항목뿐이다.
- Commit `6fd0e77`을 LFS Smudge 없이 별도 Worktree에 Checkout하자 `Binaries=False`, `Intermediate=False`, 필수 Untracked 0 상태였다. 그 상태에서 MSVC 14.51.36256으로 `DroneEditor Win64 Development`를 처음부터 Build해 `UnrealEditor-Drone.dll` 생성과 Exit Code 0을 확인했다. 검증 Worktree는 즉시 삭제했다. 따라서 DLL을 Git에 올리지 않아도 기능 소스는 재현되지만, 팀원이 Pull 뒤 빌드하지 않으면 기존 DLL 때문에 옛 기능처럼 보일 수 있다.
- Runtime 설정과 Source에는 PC 절대 경로가 없다. `Tools/AssetMigration/ImportRawDroneCandidates.py`만 `C:\에셋` 공급 원본을 가리키므로 이미 이식된 Asset 실행에는 영향이 없지만 다른 PC에서 원본 재수입은 재현되지 않는다.
- `/Script/Fab` 메타데이터가 Project의 Megascans Asset 4개에 남아 있고 작업컴에서는 별도 설치된 Fab 0.0.15 Editor Plugin이 Mount됐다. Fab가 없는 팀원 PC에서는 해당 4개의 재수입 메타데이터 경고 가능성이 있으나, 현재 Drone C++·MG·AI Runtime 기능 누락 원인은 아니다.
- 팀원 화면에서 사격 모션과 기관총 기능이 없다는 보고 뒤 중앙 파일을 재확인했다. 중앙 `6fd0e77`에는 `ABP_NPC_Rifle_Greybox` 473,761 bytes, `BS_NPC_Rifle_Locomotion` 49,269 bytes, 최신 `BP_SO_MGTurret` 26,966 bytes와 `DroneMGTurretStation`, `DroneNPCAnimInstance`, MG StateTree Source가 모두 있다. 이 기능들은 새 C++ 부모와 그 부모를 쓰는 Asset이 한 Commit에 묶여 있다. 팀원이 중앙을 직접 Pull했다면 `Plugins`보다 LFS 파일이 포인터로 남았는지와 Git에서 제외되는 `UnrealEditor-Drone.dll`을 Pull 뒤 새 Source로 재빌드했는지가 우선 확인 대상이다. 팀원 PC 자체 출력 전에는 원인을 확정하지 않는다.

## 2026-09-04 — AI-GAZE-01 감지·추적 시선/고개 회전·AI-MG-03 3분할 조준 기반

- 작업 시작 기준은 Unreal `main=origin/main=46f7f37`, 문서 `main=origin/main=b8799c3`이었다. 이후 사용자가 문서 최신화를 `2cc51f1`로 Commit·Push해 현재 문서 기준은 `main=origin/main=2cc51f1`이다. 작업 시작에는 `Lvl_MilitaryBase.umap`이 수정으로 표시됐지만 직접 수정·체크아웃하지 않았고 최종 내용 비교에서는 Git 변경이 아닌 것으로 정리됐다.
- `ADroneNPCAIController`에 감지 Actor·1초 Sight 유예·Search 마지막 위치를 잇는 독립 Gaze와 Yaw/Pitch 제한·보간을 구현했다. Gameplay AI Focus는 Slot 몸 회전과 경쟁하는 회귀가 확인되어 사용하지 않는다.
- `UDroneNPCAnimInstance`와 Editor 작성 도구를 추가하고 프로젝트 소유 `ABP_NPC_Rifle_Greybox`의 기존 Rifle Pose 뒤에 `spine_03`, `neck_01`, `head` 보정을 20/45/35%로 삽입했다. 사용자 화면 확인에서 좌우 회전 대신 위아래 까딱임만 보인 원인을 Manny Bone 로컬축으로 좁혀 세 Modify Bone을 Bone Space에서 Component Space로 교정·재저장했다. 공급사 AnimBP와 Friendly `ABP_Unarmed`는 건드리지 않았다.
- 감지 중 움직이는 Drone Actor를 계속 바라보고, 1초 유예에는 Gaze를 유지하며, 실종 확정 뒤 Search 중 마지막 위치를 바라본다. Search 완료·Drone 파괴·NPC 사망·UnPossess에서는 정면으로 복귀한다.
- 첫 Greybox 제한은 Yaw `±65°`, Pitch `-25°~+40°`, 추적 보간 `6.0`, 정면 복귀 `3.5` 후보로 기록했다. 최종값은 Rifle/MG/Cover 화면 확인 뒤 역할 BP에서 조정한다.
- 처음 포탑 Pivot을 범용 `ADroneSmartObjectStation`에 넣었던 구조를 수정했다. 범용 Station에서는 포탑 Component와 일체형 `StationMesh`를 제거하고, 새 `ADroneMGTurretStation`에만 `BaseMount → YawPivot → PitchPivot → Muzzle` 및 Engine Cylinder 기반 `BaseMesh / BodyMesh / BarrelMesh` 3개를 만들었다. `BP_SO_MGTurret` 한 개만 전용 부모로 이관했으며 다른 Smart Object는 영향을 받지 않는다.
- 임시 Base 원기둥은 `(0.65, 0.65, 0.40)`, Body는 `(0.45, 0.45, 0.35)`, Barrel은 `(0.12, 0.12, 1.10)`으로 잡았다. Cylinder 포신을 Pitch 90°로 눕혀 +X를 향하게 했고, Base는 고정·Body는 Yaw·Barrel과 Muzzle은 Pitch만 상속한다.
- 첫 통합 PIE에서는 AI Focus가 Slot Yaw를 덮어 MG 안정화가 실패했고, Focus 제거 뒤 통과했다. 3분할 첫 실행에서는 저장 BP의 Pitch Pivot이 옛 부모를 유지해 조준 갱신 2,431회에도 Yaw 오차 24.35°가 고정됐다. MG 전용 `OnConstruction`에서 정확한 Attachment를 복구하고 이미 동작 중인 Controller Tick에서 점유 포탑 조준을 계속 갱신하도록 한 뒤 통과했다.
- 사용자 추가 요구에 따라 처음에는 고정 Base 아래 `MGTurretOperatorAnchor`를 만들었으나, 몸체 회전을 직접 따르라는 최종 요구에 맞춰 Anchor를 `MGTurretYawPivot`의 자식으로 옮겼다. 사수는 기본 120cm 후방의 Anchor에 붙고 몸체가 돌면 후방 위치·몸 방향도 함께 돈다. 별도 `Operator Facing Yaw Offset`은 제거했으며 거리·좌우·높이만 `BP_SO_MGTurret > Class Defaults > Drone|AI|MG|Operator`에서 조정한다. Controller는 포탑 조준을 먼저 갱신한 뒤 같은 프레임에 사수를 정렬해 한 프레임 지연도 피한다. Smart Object Slot은 검색·배타 점유 기준으로만 남긴다.
- MG가 아닌 개인화기 `DroneDetected`·`UseCover` 상태는 몸 Yaw를 기본 초당 180°로 Drone 방향에 돌린 뒤 로컬 Gaze를 계산하도록 바꿨다. MG 이동·점유와 Patrol에는 적용하지 않아 포탑 Operator 방향이나 이동을 덮어쓰지 않는다.
- 첫 Editor Build는 새 지역 변수 `Character`가 `AController::Character`를 가린다는 C4458 한 건으로 멈췄고 변수명을 `CharacterPawn`으로 바로잡았다. 이후 Editor/Game Build 모두 성공했으므로 기능 소스 오류는 남아 있지 않다.
- `DroneEditor Win64 Development`, `Drone Win64 Development`, 저장 AnimBP·MG BP 새 프로세스 검증, Smart Object 6쌍 Validation과 `NPCGreyboxAssets`, `NPCPerceptionSearchPIE`, `SmartObjectFoundationDefaults`, `SmartObjectStationAssets`, `ProjectileBallistics` 집중 5/5가 성공했다. 디버그 계측 제거 뒤 최종 소스 그대로 `NPCPerceptionSearchPIE`를 한 번 더 실행해 11.42초, Exit Code 0으로 재통과했고 PIE 정상 종료까지 확인했다. 수동 화면 확인 전이라 `AI-GAZE-01`과 `AI-MG-03`은 Doing으로 유지한다.
- Operator·개인화기 Facing 추가 뒤 같은 집중 5종을 다시 실행해 5/5가 통과했다. 최종 Yaw 종속 Anchor 구조로 바꾼 뒤에도 MSVC 14.51.36256의 Editor/Game Build, `NPCGreyboxAssets`·`NPCPerceptionSearchPIE`·`ProjectileBallistics`·`SmartObjectFoundationDefaults`·`SmartObjectStationAssets` 5/5, 저장 `BP_SO_MGTurret`과 Smart Object 6쌍 읽기 전용 Validation이 다시 성공했다. 확장 PIE는 MG 사수의 Anchor XY 2cm 이내·몸체 종속 방향 정렬과 개인화기 병사의 Drone 방향 5° 이내 몸 정렬, MG 발사·Cover 사격·Search 회귀를 함께 확인했다.
- 기관총 최종 연결 기준은 새 [`DRONE_MG_TURRET_3PART_GUIDE.md`](../ai/DRONE_MG_TURRET_3PART_GUIDE.md)에 기록했다. `Lvl_MilitaryBase.umap`은 이 작업에서 직접 열거나 덮어쓰지 않았고 최종 Git 변경 목록에도 없다.

## 2026-09-04 — AI-ACCURACY-01 사격 분산·AI-ANIM-TEMP-01 무장 자세 수정

- 기존 Rifle·MG는 목표 중심으로 정확히 발사했고 Shotgun은 중앙 1발과 원뿔 테두리의 결정적 배치였다. 사용자 의도에 맞춰 세 무기 모두 탄환마다 원뿔 내부의 무작위 방향을 고르도록 통일했다.
- 기본 반각은 Rifle `2.5도`, Shotgun `6도`, MG `3.5도`다. 역할 BP Component Details에서 직접 바꾸거나 `ConfigureAccuracyGreybox`, `ConfigureMGTurretAccuracyGreybox` BP Node로 바꿀 수 있으며 0도는 정확 사격이다.
- Projectile과 보존된 즉시 Trace 경로가 같은 분산 규칙을 사용한다. MG Pivot은 표적 중심을 계속 바라보고 탄환 방향만 흔들려 외형 조준과 명중률을 분리했다.
- Rifle 회귀 테스트는 장애물·Damage 계약을 안정적으로 확인하기 위해 0도를 명시한다. 별도 검증은 무작위 Rifle/Shotgun 방향이 설정 원뿔을 벗어나지 않는지 확인한다.
- 첫 임시 연결은 `MM_Rifle_Fire`, `MM_Rifle_Reload`를 `ABP_Unarmed`의 `DefaultSlot`에서 재생했지만, 화면에서 무장 자세가 없고 0.533초 발사 동작을 0.25초마다 재시작해 떨리는 문제가 확인됐다.
- `/Game/Drone/AI/Animation/ABP_NPC_Rifle_Greybox`와 `BS_NPC_Rifle_Locomotion`을 프로젝트 소유 Asset으로 만들었다. Hostile Rifle·Shotgun은 Rifle ADS Idle, 8방향 Walk/Jog와 Rifle Jump를 사용하고 Friendly만 기존 Unarmed를 유지한다.
- 발사 가산 Sequence 기본 Play Rate를 `2.4x`로 설정해 약 0.222초 안에 끝낸다. 역할 BP에서 Fire/Reload Asset·Play Rate를 바꾸거나 임시 재생을 끌 수 있다.
- `DroneEditor Win64 Development` Build 성공. `NPCGreyboxAssets`, `WeaponContract`, `NPCPerceptionSearchPIE` 3/3과 새 Editor 프로세스의 저장된 Rifle Idle·27개 Rifle BlendSpace Sample·Hostile/Friendly AnimBP 분리 검증이 성공했다. 손 위치·총기 정렬과 반복 동작은 화면 육안 재확인이 남았고 전체 자동화·Blueprint 전체 Compile은 반복하지 않았으며 Commit·Push하지 않았다.

## 2026-09-03 — AI-BALLISTIC-01 회피 가능한 Projectile

- 기존 개인 무기와 MG는 발사 즉시 맞는 Visibility Trace였다. 드론이 발사 뒤에도 이동으로 회피할 수 있도록 `ADroneNPCProjectile` 공용 탄환을 추가했다.
- 기본 탄속은 Rifle `4,500 cm/s`, Shotgun `3,500 cm/s`, MG `5,500 cm/s`다. 최종 난이도 값이 아니며 `ConfigureProjectileBallisticsGreybox`와 `ConfigureMGTurretProjectileGreybox` 또는 BP Class Defaults에서 조정한다.
- Projectile은 Actor Tick·Chaos 물리 Simulation 없이 `ProjectileMovementComponent`의 Sweep 충돌을 사용한다. 지정 사거리 비행 시간에 0.25초 여유를 더한 뒤 자동 제거되어 누적되지 않는다.
- Rifle은 탄환 1개, Shotgun은 기존 결정적 Spread 방향마다 탄환을 한 개씩 Spawn한다. 발사자와 MG 사용자는 이동 충돌에서 제외하고, 현재 지정한 Target에 맞았을 때만 기존 Damage를 적용한다.
- Engine 기본 Sphere는 구매 에셋 전 이동 확인용이다. 최종 Mesh/Tracer/Niagara/Sound는 BP 파생 Projectile과 기존 `OnWeaponFired`에서 표현만 연결한다.
- 즉시 Rifle/Shotgun Trace 코드는 삭제하지 않고 `bUseProjectileBallistics=false` 선택 경계로 보존했다. 회귀 테스트는 이 모드를 명시적으로 사용한다.
- 첫 빌드 실패 표시는 소스 오류가 아니라 UnrealBuildTool의 AppData Trace 로그 교체 권한 거부였다. 권한 해소 후 `DroneEditor Win64 Development` Build가 성공했다.
- 추가 충돌 결과 검사에서 Component Delegate의 생성자 연결이 시험 인스턴스에 적용되지 않는 문제를 발견했다. CDO 복제에 의존하지 않는 Actor `NotifyHit` 경계로 교체하고 Rifle/Shotgun Target impact가 무기 적중 카운터까지 돌아오는 것을 재검증했다.
- `Drone.AI.ProjectileBallistics`, `RifleTrace`, `ShotgunTrace`, `WeaponContract`, `NPCPerceptionSearchPIE` 5/5가 성공했다. 전체 `Drone.`·Blueprint 전체 Compile·LFS는 반복하지 않았고 Commit·Push도 하지 않았다.

## 2026-09-03 — FLOW-03 미션 선택·설명·시작 완료

- Flow Subsystem이 등록 Mission ID를 이름순으로 반환하도록 해 로비가 `TMap` 내부 순서나 별도 문자열 목록을 소유하지 않게 했다.
- 현재 한 개의 Training Mission을 `MissionSelectButton`으로 표시하고, 선택 뒤 이름·설명·지역·난이도는 `DA_Mission_Tutorial_Training`에서 읽는다.
- 하단 `StartMissionButton`은 유효한 선택이 있을 때만 활성화되고 `ConfirmSelectedMission()`으로 `MissionTrailer` 상태까지만 전환한다. 실제 영상·Map 이동은 FLOW-04로 남겼다.
- WBP가 최종 Designer를 만들 때 사용할 이름 계약은 `MissionSelectButton`, `MissionSelectButtonText`, `MissionNameText`, `MissionDescriptionText`, `MissionMetaText`, `StartMissionButton`이다. Blueprint는 선택/확정 판정을 중복 구현하지 않는다.
- 최종 Drone Game/Editor Build와 `Drone.Flow` 3/3이 성공했다. PIE에서 잘못된 Mission ID 거부, Definition과 표시 이름·설명 일치, 중복 확정 거부, 같은 Root Widget 1회 생성을 확인했다.
- 이 시점에는 새 Asset을 추가하지 않아 Unreal 변경 경로 수는 26개로 유지했다. Commit·Push하지 않았고 당시 다음 카드는 `FLOW-04`였다. 최신 상태는 문서 상단을 따른다.

## 2026-09-03 — FLOW-02 시작 화면→로비 완료

- `UDroneGameFlowSubsystem::EnsureDefaultCatalog()`을 추가해 첫 Vertical Slice Drone을 먼저, Mission을 다음에 GameInstance 수명 Catalog로 등록한다. 같은 Asset의 반복 호출은 중복 항목을 만들지 않는다.
- 새 `ADroneFrontEndGameMode`는 `DefaultPawnClass=None`, 새 `ADroneFrontEndPlayerController`는 Root Widget 한 개와 UI 입력 수명만 소유한다.
- 새 `UDroneFrontEndRootWidget`은 정적 Opening 대체 화면과 Lobby 패널을 같은 인스턴스에서 전환한다. 실제 영상이 생기면 `FinishOpeningTrailer()`를 Media/Sequencer 종료 Callback에서 호출하고, `ReceiveFrontEndStateDisplayed`에는 Blueprint 표현만 붙인다.
- 실제 `/Game/Drone/FrontEnd/UI/WBP_DroneFrontEndRoot`, BP Controller/GameMode와 `/Game/Drone/Maps/Lvl_DroneFrontEnd`를 만들었다. WBP Designer는 최종 외형 미정이므로 비어 있고 현재는 C++ fallback Layout을 사용한다.
- `GameDefaultMap`을 `Lvl_DroneFrontEnd`로 바꿨지만 `EditorStartupMap`은 기존 Training Map을 유지했다. Front-end Map에서는 Drone 선택 전 Drone Pawn을 Spawn하지 않는다.
- 최초 Front-end Asset Create는 자산 저장까지 성공했으나 Python 검증에서 Generated Class API 이름을 잘못 사용해 종료 코드 3이 났다. `MathLibrary.class_is_child_of`로 검증만 수정한 뒤 새 프로세스 Validate가 성공했으며 생성 Asset은 덮어쓰지 않았다.
- 첫 PIE에서는 UIOnly Focus 대상이 Focusable이 아니어서 실패했다. Root Widget을 Focusable로 만든 뒤 `Drone.Flow.FrontEndPIE` 1/1이 성공했다.
- 최종 확인은 `Drone Win64 Development`, `DroneEditor Win64 Development`, Front-end Asset Validate와 `Drone.Flow` 3/3이다. Root 생성 1회, Opening→Lobby 단일 전환, 두 번째 전환 거부, Mission/Drone Catalog 각 1개, 선택 전 Drone 0대를 확인했다.
- 모든 변경은 로컬 미커밋이며 Commit·Push하지 않았다. 다음 카드는 `FLOW-03`이다.

## 2026-09-03 — FLOW-01 상태·Mission/Drone 데이터 계약 완료

- `UDroneGameFlowSubsystem`에 실행부터 결과까지 8개 상태, Mission/Drone 선택 Snapshot, 잘못된 순서와 중복 요청 거부 규칙을 구현했다.
- `UDroneDefinition`, `UDroneMissionDefinition` Primary Data Asset과 실제 `DA_Drone_Scout_Greybox`, `DA_Mission_Tutorial_Training`을 만들었다. 이는 첫 Greybox 값이며 최종 Drone 종류나 게임 규칙 확정이 아니다.
- `DroneEditor Win64 Development`, 저장 Asset 새 프로세스 Validate와 `Drone.Flow.Contract` 1/1이 통과했다.
- 후속 전투 표현을 위해 NPC Character에 `WeaponVisualComponent`, `WeaponMuzzleComponent`, BP 발사/재장전 표현 Event를 준비했다. 실제 Rifle/Shotgun Mesh·Animation·FX·SFX는 연결하지 않았다.
- 모든 변경은 로컬 미커밋으로 유지했다.

## 2026-09-03 — 프로젝트 통합 기획·개발 현황서

- 새 [`DRONE_PROJECT_PLANNING_BRIEF.md`](../planning/DRONE_PROJECT_PLANNING_BRIEF.md)에 세계관·플레이어 역할, 확정 Front-end 흐름, Tutorial/Story Mission, 한글 UI 수치, 구현/미구현, 폐기/보존, 기술 구조, Map 활용, FLOW-01~08 로드맵, 검증, 역할 분리와 보류 결정을 한 문서로 정리했다.
- 진행상황은 실제 `main=origin/main=6a18210`, Unreal 로컬 Smart Object 변경 8개와 기존 빌드·자동화·수동 미확인 기록을 기준으로 작성했다.
- Figma는 세계관·UI 방향 참고로만 구분하고 사람 Operator 조작이 구현된 것으로 표현하지 않았다.
- 이번 작업은 Markdown만 변경했고 Unreal Build·PIE·Asset 변경은 수행하지 않았다.

## 2026-09-03 — 사람 Operator 폐기와 Front-end Mission Flow 확정

- 사용자가 사람 Player Character 구상을 취소하고 새 흐름을 `게임 실행 → 시작 트레일러 → 로비 → 미션 레벨 선택 → 측면 미션 설명 → 하단 시작 → 미션 트레일러 → Map 진입 → Drone 선택 → Mission 시작 → 측면 목표 UI`로 확정했다.
- 기존 Operator↔Drone Possess/Camera 전환과 로비 NPC 대화 Mission 수령 카드는 폐기했다. 아직 해당 생산 코드를 만들지 않았으므로 제거할 Unreal 구현은 없다.
- 기존 Drone 조작·Telemetry·Tutorial 기록과 적 NPC·Smart Object·Rifle/Shotgun·MG·Cover·체력 기능은 Mission Map 내부 기능으로 재사용한다. 아군 NPC 생활 루틴은 보존하지만 Front-end 선행조건에서는 제외했다.
- 새 최우선 계획 [`DRONE_FRONTEND_MISSION_FLOW_PLAN.md`](../planning/DRONE_FRONTEND_MISSION_FLOW_PLAN.md)에 영속 Flow 상태, Mission/Drone Data Asset, 화면별 책임, Content 경계, `FLOW-00~08` 카드와 3회 반복 검증을 기록했다.
- 첫 Vertical Slice는 기존 `Lvl_DroneTraining`을 한 개 Tutorial Mission으로 등록하고 한 개 Drone만 허용해 흐름을 검증한다. MilitaryCamp·MilitaryBase·Battlefield 연결은 이 골격 뒤에 진행한다.
- Figma `Project:Droner`는 세계관과 UI 분위기 참고용으로 읽었고 수정하지 않았다. 최종 제목 통일은 보류했다.
- 이번 작업은 MD 기준선만 변경했다. Unreal Source·Asset·Build·PIE 결과는 추가하지 않았으며 새 Flow가 구현됐다고 표시하지 않는다.

## 2026-09-03 — AI-SO-TUNE-01 Smart Object 배치·방향 조정 보강

- 실제 수정 위치를 맵 Actor, Station Blueprint, Smart Object Definition, StateTree, C++ Station/Reservation/Controller/Task로 나눠 `DRONE_SMART_OBJECT_NPC_GUIDE.md` 상단에 빠른 표와 Editor 배치 절차를 추가했다.
- `SlotFacingPreview`를 `SmartObjectComponent` 아래에 부착해 Blueprint에서 Slot Offset을 조정할 때 Cyan 화살표도 같은 Transform을 따르게 했다.
- `ADroneNPCAIController::AlignPawnToReservedSlot()`을 추가해 예약 Slot의 Yaw를 Pawn과 Control Rotation에 적용했다. 순찰·아군 활동 공용 이동, Cover, MG 도착 경로에서 호출한다. Pitch/Roll은 지면 Character 기울어짐 방지를 위해 적용하지 않는다.
- Smart Object Foundation 기본 계약에 Preview의 Attach Parent 검증을 추가했다.
- Smart Object Setup Wrapper는 하드코딩된 C 드라이브 경로 대신 문서 저장소와 같은 상위 폴더의 `drone/Drone.uproject`를 자동 계산한다.
- 첫 Build 시 Unreal Editor가 `D:\JGY\project\drone\Drone.uproject`로 실행 중임을 확인해 저장되지 않은 작업 보호를 위해 강제 종료하지 않았다. 사용자 종료 뒤 `DroneEditor Win64 Development` Build가 성공했다.
- `NPCPerceptionSearchPIE`에 Pawn Yaw와 예약 Slot Yaw의 1도 이내 비교를 추가했다. MG 점유와 Cover 점유 경로를 직접 판정하며 `SmartObjectFoundationDefaults`의 Preview Parent 계약과 함께 2/2 성공, 경고·오류 0이다.
- 자동 계산 Wrapper로 Definition/BP 6쌍을 `Validate`해 모두 역할·Tag·Definition·MG Mesh 계약과 일치했다. 이제 Editor 화면에서 Cyan 화살표와 실제 NPC 도착 방향만 확인하면 `AI-SO-TUNE-01`을 Done으로 옮길 수 있다.
- 최종 Git 확인에서 `SO_Def_FriendlyBasePatrol`이 5,493 bytes에서 5,750 bytes로 바뀐 LFS 객체를 확인했다. 사용자 Editor 종료 저장인지 Headless 재직렬화인지 확정할 수 없어 변경을 삭제하지 않고 보존했다. 변경된 Definition 상태로 후속 NPC PIE가 통과했으며 Commit 전 Slot 설정을 Editor에서 확인한다.

## 2026-09-03 — AI-MG-02 Occupy·Aim·Fire·Release 핵심

### 2026-09-03 공유 기준선 재확인

- 사용자가 전투 Greybox와 표현 이벤트 변경을 Commit·Push해 Unreal `main=origin/main=6a18210`, 문서 `main=origin/main=2c99f00`이며 두 작업 트리가 Clean임을 확인했다.
- `6a18210`에는 AI-MG-02, HP-01, AI-COVER-01, AI-COMBAT-END-01, AI-AMMO-01, AI-VIS-01A에 해당하는 코드·StateTree·Greybox Map 변경이 포함된다.
- 각 기능의 단계별 Editor Build와 집중 테스트 결과는 유지한다. 이 대형 Commit 이후 전체 `Drone.` 회귀·Blueprint 전체 Compile·LFS 검증은 새로 실행하지 않았으므로 완료 근거를 과장하지 않는다.
- 다음 구현 후보는 `AI-VIS-01B`: Manny Rifle 임시 표현과 MG FX/SFX 연결이다. Shotgun Mesh와 최종 Soldier/Insurgent 외형은 후보·Retarget 확인 전까지 미정이다.

### AI-VIS-01A 자산 호환성 감사·Blueprint 표현 이벤트

- 새 읽기 전용 `Audit-DroneNPCVisualAssets.py`와 실행 Wrapper로 후보 Asset의 Load, Skeleton, Animation 수량, Weapon Mesh 수량을 반복 감사할 수 있게 했다.
- Manny Rifle Animation은 38개이고 AR4·MG·Niagara Muzzle Flash·Sound Cue 후보는 정상 로드된다. FPS Weapon Mesh는 70개지만 이름으로 식별되는 Shotgun Weapon Mesh는 0개다.
- Modular Soldier/Insurgent는 Manny와 Skeleton이 직접 일치하지 않고 이식된 두 Root의 Animation Asset은 각각 0개다. 따라서 최종 진영 외형과 Retarget 결과를 확인하기 전에는 역할 Blueprint에 강제 적용하지 않았다.
- `UDroneNPCWeaponComponent`에 Blueprint용 `OnWeaponFired(WeaponType, TraceStart, AimPoint)`와 `OnReloadCompleted(WeaponType, CurrentAmmo, Capacity)`를 추가했다. Rifle은 Trace당 1회, Shotgun은 Volley당 1회이며 실패/거절 요청은 방송하지 않는다.
- `DroneEditor Win64 Development`와 WeaponContract·RifleTrace·ShotgunTrace 3/3이 통과했다. 전체 자동화·Blueprint Compile·LFS는 반복하지 않았다.
- `6a18210` Push 전 당시 Unreal 변경은 `git status --porcelain -uall` 기준 30개 파일, 문서 저장소는 12개 파일이며 모두 로컬 미커밋이었다.

### AI-AMMO-01 Rifle·Shotgun 탄창·재장전

- `UDroneNPCWeaponComponent`에 현재 탄약, 장비별 탄창 용량, Blueprint 조회 함수와 시험 설정 함수를 추가했다. 기본 Rifle 30발, Shotgun 8발은 최종 밸런스가 아니다.
- Rifle은 실제 Trace 한 번에 한 발, Shotgun은 Volley 한 번에 Shell 한 발을 소모한다. 장애물에 막혀도 발사한 탄은 소모하지만 사거리·Cooldown으로 거부된 요청은 소모하지 않는다.
- 마지막 탄 뒤 Timer·Target을 정리하고 빈 탄창 발사를 거부한다. `Reload()`는 소모된 탄창만 즉시 채우며, Hostile Controller는 교전 지속 중 빈 탄창이면 Reload 후 같은 공용 발사 경로를 재개한다.
- 예비 탄약, 재장전 시간·Animation·FX·SFX는 이번 카드에 넣지 않았다.
- Editor Build 성공. 한 Editor 실행에서 `NPCPerceptionSearchPIE`, `RifleTrace`, `ShotgunTrace`가 통과했고 Owner 없는 순수 계약 객체의 생존 검사 오류를 수정한 뒤 `WeaponContract` 1/1도 최종 통과했다.
- 전체 테스트·Blueprint Compile·LFS, Commit·Push는 실행하지 않았다.

### AI-COMBAT-END-01 Drone 파괴 교전 종료

- `ADronePrototypePawn`에 BlueprintAssignable `OnDroneDestroyed`와 1회 발생 진단값을 추가했다. Health 사망 Event가 입력·이동·충돌을 끄고 Perception Source를 해제한 뒤 이 신호를 보낸다.
- 현재 Drone을 감지하던 살아 있는 Hostile은 개인 무기, 이동, MG 사용자 상태, Cover/MG 예약, 마지막 감지 위치를 즉시 정리한다. 파괴 표적은 수색하지 않고 기존 StateTree Lost 전환을 이용해 Patrol로 복귀한다.
- 사망한 Hostile과 Friendly는 파괴 응답 대상에서 제외했다. 사망 뒤 추가 Damage도 Health/Drone 파괴 Event를 다시 발생시키지 않는다.
- 구현 중 성공 Sight가 곧바로 Lost로 처리될 수 있던 조건 분기 오류와 StateTree 강제 재시작 시 이전 감지 Event가 남던 문제를 집중 PIE에서 발견해 수정했다.
- 최종 `DroneEditor Win64 Development`와 확장 `Drone.AI.NPCPerceptionSearchPIE` 1/1이 통과했다. 테스트는 기존 MG·Cover·사망 교대·Search 복귀 뒤 재교전, Drone 파괴, 모든 전투 자원 해제, Patrol 복귀와 Event 1회를 연속 검증한다.
- 전체 테스트·Blueprint 전체 Compile·LFS는 반복하지 않았고, Commit·Push도 하지 않았다.

### AI-COVER-01 MG 실패 병사 엄폐 대응

- Hostile StateTree에 `ClaimCoverSlot`, `MoveToCover`, `UseCover`를 추가해 총 12개 상태로 확장했다. MG Claim 실패는 Cover로 가고 Cover도 실패하면 기존 DroneDetected 개인 무기 상태로 내려간다.
- Controller에 Cover 1-Slot Claim·NavMesh 이동 완료·Occupied·개인 무기 유지·Abort 수명주기와 관측 카운터를 추가했다.
- `Lvl_NPCSmartObjectGreybox`에 `BP_SO_Cover` 두 개를 배치했다. 작성 도구는 기존 Actor를 덮어쓰거나 중복 생성하지 않고 StateTree·두 Station을 갱신/검증한다.
- MG 사수가 사망하면 Cover 중인 다른 MG 가능 Hostile이 Root 감지 Event로 전환돼 Cover를 해제하고 비어진 MG를 재Claim한다.
- Editor Development Build와 StateTree/Map Upgrade 검증이 성공했다. 최신 `Drone.AI.NPCPerceptionSearchPIE` 1/1은 MG 1명·Cover 1명, Cover Occupied 개인 무기, 사망 뒤 Cover→MG 교대, DroneLost Search→Patrol을 통과했다.
- 전체 테스트·Blueprint 전체 Compile·LFS는 반복하지 않았다. 소스/에셋 27개와 문서/도구는 사용자 요청에 따라 로컬 미커밋으로 유지한다.

### HP-01 및 사망 뒤 MG 재점유 마감

- NPC와 Drone에 공통 `UDroneHealthComponent`를 부착했다. 기본·최대 체력은 모두 100이며 0 이하에서 사망 Event를 정확히 한 번 보내고 이후 Damage를 무시한다.
- Rifle 발당 10, Shotgun 적중 Pellet당 8, MG 발당 8의 Greybox Damage를 표준 `UGameplayStatics::ApplyDamage` 흐름으로 연결했다. 모두 최종 밸런스가 아닌 시험값이다.
- NPC 사망 시 이동·충돌·개인 무기·StateTree·MG 사용·Smart Object Claim을 정리한다. 사망한 MG 사수가 놓은 Slot은 감지 중인 다른 MG 가능 Hostile이 다시 Claim·Occupied하여 조준·사격을 이어간다.
- Drone 사망은 입력 Mapping·이동·충돌을 정지하고 기체는 현 위치에 남긴다. 래그돌·폭발·시체 제거·Respawn·Mission 실패 화면은 후속 표현/게임 규칙이다.
- `UDroneFlightHUDWidget` 우측 상단 동적 패널에 `기체 내구도 현재/최대`와 `파괴됨`을 Event 기반으로 표시하고 PlayerController가 Possess Pawn의 Health Source를 연결·정리한다.
- `DroneEditor Win64 Development`가 성공했다. 집중 `Drone.AI.NPCPerceptionSearchPIE`는 100/100 시작, 사망 1회, MG 해제·두 번째 적 재점유·생존자 Search/Patrol 복귀를 통과했고 `Drone.UI.FlightHUDTelemetryBinding`은 100→70→파괴 표시와 Delegate 해제를 통과했다.
- 전체 27개·Blueprint 전체 Compile·LFS는 사용량 절약 원칙에 따라 반복하지 않았다. Unreal 소스 21개와 문서는 Commit·Push하지 않고 로컬에 유지한다.

- Reservation Component에 Occupied 판정과 예약한 Smart Object 소유 Actor 조회를 추가했다.
- MG Station에 `MGTurretAimPivot`과 사용자·표적 수명주기를 추가했다. 6,000cm·0.15초 Greybox Visibility Trace를 수행하고 Blueprint가 외형·Muzzle Flash·Sound를 연결할 수 있도록 사용 상태와 발사 Event를 노출했다.
- Controller는 도착한 Claim을 Occupied로 바꾸고 활성 Station을 보관한다. 기존 저장 StateTree Struct 경로를 유지한 채 Hold Task가 실제 MG 시작·조준·Cooldown 사격을 실행한다.
- DroneLost·Task 실패·UnPossess·EndPlay에서는 Station 사용자와 Occupied Slot을 정리한다. MG 사용 중 개인 Rifle 발사는 중단된다.
- `DroneEditor Win64 Development`와 직접 관련 `Drone.AI.NPCPerceptionSearchPIE` 1/1이 통과했다. 테스트는 Occupied, 사용자·표적·Aim Point, Trace 발생, Shotgun Fallback, Friendly 비무장, DroneLost 해제를 확인한다.
- 이 핵심 구현 뒤 위 HP-01 단계에서 Damage·사망·다른 AI 재점유 완료 조건까지 마감했다.

## 2026-09-02 — AI-MG-01 MG 1-Slot Claim·Move

- `ADroneNPCAIController`에 `MoveToMGTurret`, `HoldMGTurret` 관측 상태와 Claim·도착 카운터를 추가했다. MG 사용 가능 Hostile만 기존 MGTurret Activity Tag와 Reservation Component로 가장 가까운 빈 Slot을 예약한다.
- 새 Native StateTree Task가 Claim 1회, 예약 위치까지 NavMesh 이동, 도착 뒤 Claim 유지를 각각 담당한다. 권한 없음·빈 Slot 없음·이동 실패는 기존 `DroneDetected` 개인 무기 상태로 대체한다.
- 반복되는 성공 Sight 자극은 최초 감지 Event를 다시 보내지 않아 이동 중 Claim을 풀지 않는다. DroneLost·이동 실패·StateTree 중단·UnPossess에서는 이동과 예약을 정리한다.
- 저장된 `ST_NPC_HostilePatrol`을 6-State에서 9-State로 업그레이드했다. 새 문서 도구 `Invoke-DroneHostileMGTurretStateTreeSetup.ps1`의 Upgrade와 새 프로세스 Validate가 모두 성공했다.
- NPC Greybox PIE는 MG 운영자 정확히 1명, 유효 예약 정확히 1개, Claim·도착 카운터 1회, 도착 뒤 개인 무기 정지, Shotgun Hostile의 개인 무기 Fallback과 Friendly 비무장을 검증한다.
- Game/Editor Development Build, AI 11/11과 전체 `Drone.` 27/27, Blueprint 0 errors·0 Blueprint warnings·0 failed loads, LFS fsck를 통과했다. Rifle 빈 World 경고 1건과 공급사 Pose GUID 28건·MCP 고지 1건은 기존과 같다.
- Unreal 한글 Commit `249d6cd` (`기능: 적 AI의 MG 터렛 예약과 이동 구현`)을 `origin/main`에 Push했다. 다음 카드는 `AI-MG-02`이며 Occupied·Aim·Fire·Release와 사망 뒤 재점유를 구현한다.

## 2026-09-02 — AI-WPN-02 Rifle 확정·AI-WPN-03 Shotgun Greybox 사격

- 최신 `98f67d0`에 들어온 Rifle Visibility 단일 Trace, 4,000cm 사거리, 0.25초 Cooldown과 `Drone.AI.RifleTrace`를 Editor에서 빌드했다. 전용 테스트는 개방 표적 명중, 장애물 차단, 사거리 밖 거부와 즉시 재발사 Cooldown을 통과했다.
- 첫 전체 회귀에서는 수동 Sight Broadcast가 실제 Sight 반경을 적용하지 않아 기존 공용 Weapon 경로 테스트가 Rifle 사거리에서 실패했다. Rifle/Shotgun 전용 테스트가 사거리를 검증하도록 두고, 공용 경로 테스트에서는 시험용 사거리를 넓혀 Target/Aim Point 계약만 분리 검증했다. 수정 뒤 Rifle 기준 전체 26/26이 통과했다.
- `AI-WPN-03`으로 Shotgun 1,600cm 사거리, 0.9초 Cooldown, 8 Pellet, 6도 원뿔 반각 Greybox를 같은 `UDroneNPCWeaponComponent`에 추가했다. 첫 Pellet은 중심, 나머지는 원뿔 가장자리에 균등 배치해 실행마다 같은 Spread를 재현한다.
- `Drone.AI.ShotgunTrace`는 한 Trigger가 설정된 Pellet 수만큼 Trace를 만드는지, 0도 Spread 전탄 명중, 장애물 전탄 차단, 사거리 밖 거부, 즉시 재발사 Cooldown, Spread Endpoint 분리와 Rifle 코드 분리를 검증했다.
- Game 빌드에서 Rifle/Shotgun 자동화가 Editor 전용 `AutomationEditorCommon` 헤더를 포함하던 기존 경계 오류를 발견했다. 두 테스트를 `WITH_DEV_AUTOMATION_TESTS && WITH_EDITOR`로 제한해 런타임 코드와 Editor 테스트를 분리했고 `Drone Win64 Development`와 `DroneEditor Win64 Development`가 모두 성공했다.
- 최종 AI 11/11과 전체 `Drone.` 27/27이 성공했다. Rifle 테스트의 빈 World에서 RecastNavMesh가 없다는 예상 경고 1건만 있으며 실패는 0이다. `CompileAllBlueprints`는 0 errors / 0 Blueprint warnings / 0 failed loads이고 전역 Summary의 기존 Battlefield Pose GUID 28건과 MCP EULA 1건은 별도 경고다. `git lfs fsck`와 `git diff --check`도 통과했다.
- Unreal 한글 Commit `0d92a5f` (`기능: 샷건 펠릿 사격과 무기 테스트 보강`)을 `origin/main`에 Push했다. 실제 Damage·탄약·Animation·FX·SFX는 미구현이며 다음 활성 카드는 `AI-MG-01`이다.

## 2026-09-02 — Rifle Trace 착수·MilitaryBase 강/도로 구조 확인

- Unreal `origin/main=c7f116f`까지 사용자가 저장·Push했고 두 저장소 모두 작업 트리가 깨끗한 상태에서 재개했다.
- `AI-WPN-02` 코드에 Rifle Visibility 단일 Trace, 4,000cm 시험 사거리, 0.25초 Cooldown, 장애물 차단·디버그 선·상태 정리를 추가하고 `Drone.AI.RifleTrace` 자동화 테스트를 작성했다. Editor 빌드는 성공했으나 전용 테스트 결과 로그는 다음 확인 대상이다.
- `Lvl_MilitaryBase`의 강은 WaterBody가 아니라 `Landscape` 내부 `SM_RiverBank` SplineMesh 166개와 물 재질 슬롯으로 구성된다. 강 반사광은 별도 `MI_DecalCaustic_Inst` 9개 및 Wetness Decal 계열이며, Sphere Reflection Capture 9개도 별도로 존재한다.
- 도로는 별도 Road Actor가 아니라 Landscape 높이/재질 레이어 방식으로 보이며 `rockyPath`, `forrestPath`, `brownMud` Target Layer를 Paint/Layer Debug로 확인하는 절차를 정리했다. 맵 삭제·저장은 수행하지 않았다.
- 다음 확인: Rifle 전용 자동화 결과 판정 후 장애물·사거리·Cooldown이 모두 통과하면 `AI-WPN-02`를 완료하고, 실패 시 코드만 수정한다.

## 2026-09-02 — Friendly/Hostile NPC 선택 PropertyEditor 크래시 수정

- `Lvl_NPCSmartObjectGreybox`에서 Friendly 또는 Hostile NPC Actor를 선택하면 `UnrealEditor_PropertyEditor` 호출이 반복된 뒤 `EXCEPTION_STACK_OVERFLOW`로 Editor가 종료되는 현상을 사용자와 자동 선택으로 동일 재현했다. 맵 로드와 무선택 상태는 정상이므로 플레이 로직이 아니라 Details 패널 생성 경로로 범위를 좁혔다.
- Friendly도 동일하게 재현돼 적 전용 Weapon이나 Hostile StateTree가 아니라 `ADroneNPCCharacter` 공통 Details 표시 경로 문제로 판정했다.
- 공통 컴포넌트와 Weapon 진단값의 다단계 `Category`를 단일 카테고리로 바꾸고, `FDroneNPCProfile`의 `ShowOnlyInnerProperties` 자동 인라인 표시를 제거했다. 값·저장 구조·런타임 공개 API와 AI 동작은 변경하지 않았다.
- `DroneEditor Win64 Development`가 MSVC 14.51.36256으로 성공했다. 사용자가 Friendly 선택 후 크래시가 없음을 확인했고, MCP로 `BP_NPC_Hostile_Rifle_C_0`을 정확히 선택한 뒤 12초 이상 Editor가 정상 생존했다.
- 엔진 내부의 어느 단일 메타데이터가 직접 원인인지는 추가 격리하지 않았다. 현재 확정 범위는 공통 NPC Details 메타데이터 조합에서 재현됐고 표시 단순화 후 해소됐다는 것이다.
- Unreal 변경은 `DroneNPCCharacter.h`, `DroneNPCProfileComponent.h`, `DroneNPCWeaponComponent.h` 3개이며 로컬 미커밋이다. 다음 기능 카드는 그대로 `AI-WPN-02` Rifle Greybox Trace다.

## 2026-09-02 — AI-PER-01 Hostile 감지·Search·순찰 복귀

- `ADroneNPCAIController`에 `Patrol`, `DroneDetected`, `Search` 관측 상태와 마지막 감지 위치, 감지·실종·Search 진입·완료 카운터를 추가했다. Hostile은 감지 즉시 이동을 멈추고 Smart Object Claim을 해제하며 Friendly는 같은 자극을 무시한다.
- `FDroneStateTreeDetectedTask`와 `FDroneStateTreeSearchTask`를 추가했다. 실종 뒤 마지막 위치로 이동을 요청하고 NavMesh 밖이면 제자리에서 3초 Search를 유지한 뒤 기본 순찰 Activity와 Claim 흐름으로 복귀한다.
- 저장된 `/Game/Drone/AI/StateTrees/ST_NPC_HostilePatrol`에 `DroneDetected`, `SearchLastKnownLocation` 상태와 `DroneDetected`/`DroneLost` Event 전환, Search 성공·실패의 Claim 복귀를 추가했다. Upgrade는 기존 정확한 4-State 자산만 수정하고 알 수 없는 확장 자산은 덮어쓰지 않는다.
- 문서 저장소에 `Setup-DroneHostilePerceptionStateTree.py`와 `Invoke-DroneHostilePerceptionStateTreeSetup.ps1`을 추가했다. Upgrade와 Validate 모두 성공했고 저장 자산의 Task·Event 연결을 검사한다.
- 새 `Drone.AI.NPCPerceptionSearchPIE`는 Hostile 2명 감지·예약 해제, Friendly 2명 무반응, Hostile 실종·Search 진입, Search 완료·순찰 작업 재개와 Friendly 루틴 지속을 검증한다. 실제 Sight의 재감지와 수동 Lost 자극이 경합하지 않도록 Lost 뒤 시험 Pawn만 LoseSight 범위 밖으로 격리한다.
- 최종 `DroneEditor Win64 Development`와 `Drone Win64 Development` Build가 성공했다. AI `8/8`은 모두 무경고·무오류, 전체 `Drone.`은 `24/24`로 23개 무경고와 기존 `PIEInputLifecycle` RecastNavMesh 경고 포함 성공 1개다.
- `CompileAllBlueprints`는 `0 errors / 0 warnings / 0 failed loads`다. 전역 Summary의 기존 Battlefield Pose GUID와 MCP EULA 고지 29건은 Blueprint 결과 집계와 분리한다. `git lfs fsck`도 통과했다.
- 사용자가 Editor 화면에서 Hostile 정지→Search→순찰 복귀와 Friendly 지속을 직접 확인해 수동 Pass 처리했다.
- 공유 기준은 계속 `origin/main=2fcfb04`다. Unreal·문서는 로컬 `main` 위 미커밋 변경이며 자동 Commit·Push하지 않았다.
- 다음 활성 카드는 `AI-WPN-01` 공용 Weapon 계약으로 이어서 완료했다.

## 2026-09-02 — AI-WPN-01 공용 Weapon 계약

- `UDroneNPCWeaponComponent`를 추가해 Rifle·Shotgun 공통 `ConfigureWeapon`, `CanFire`, `StartFire`, `StopFire`, `Reload` 호출과 Target Actor·Aim Point 상태를 한 곳에서 관리한다.
- `ADroneNPCCharacter`가 Weapon Component를 소유하고, Controller는 Possess 때 NPC Profile의 Weapon Type을 구성한다. Hostile Controller는 `DetectedDrone`에서 Target과 Aim Point를 한 번만 만들어 Rifle·Shotgun 분기 없이 같은 경로로 전달한다.
- 감지 실종과 UnPossess에서는 발사 상태를 정리한다. Unarmed와 잘못된 Target은 거부하며 Rifle/Shotgun별 Trace·Damage·탄약·Cooldown·Pellet·Spread는 후속 카드 범위로 남겼다.
- `Drone.AI.WeaponContract` 자동화 테스트를 추가하고 NPC Greybox PIE를 확장해 Rifle·Shotgun의 같은 Target/Aim Point 경로, Friendly 비발사, Lost 시 발사 정리를 검증했다.
- 최종 `DroneEditor Win64 Development`와 `Drone Win64 Development` Build가 성공했다. AI `9/9`은 모두 무경고·무오류, 전체 `Drone.`은 `25/25`로 24개 무경고와 기존 `PIEInputLifecycle` RecastNavMesh 경고 포함 성공 1개다.
- 이번 카드는 Blueprint 자산을 수정하지 않아 전체 Blueprint Compile을 반복하지 않았다. 직전 `0 errors / 0 warnings / 0 failed loads`와 이번 자동화의 NPC Blueprint 로드 성공을 기준으로 유지한다.
- 공유 기준선은 `origin/main=2fcfb04`이며 Unreal·문서 로컬 `main`의 변경은 Stage·Commit·Push하지 않았다. 다음 활성 카드는 `AI-WPN-02` Rifle Greybox Trace다.

## 2026-09-02 — Generate 이후 DroneEditor Unity 빌드 수정

- 사용자가 AI-PER-01·AI-WPN-01과 문서를 Push해 Unreal `main=origin/main=2054d6f`, 문서 `main=origin/main=356d942`가 됐다.
- 생성 폴더를 정리하고 프로젝트 파일을 다시 만든 뒤 Editor 자동 컴파일에서 `DroneNPCPatrolStateTreeTasks.cpp`와 `DroneNPCPerceptionStateTreeTasks.cpp`의 익명 Namespace 헬퍼 `GetDroneController`가 Unity Translation Unit 안에서 중복 정의되는 오류를 확인했다.
- Perception 파일의 헬퍼를 `GetPerceptionDroneController`로 고유화했다. 런타임 API나 동작은 바꾸지 않았다.
- Generate가 `.vsconfig`의 세부 MSVC Component를 UE 5.8 권장 14.50으로 갱신했다. 실제 Build는 설치된 MSVC 14.51.36256을 사용했고 비선호 버전 주의 메시지만 남긴 채 `DroneEditor Win64 Development`가 성공했다.
- 이 수정과 `.vsconfig` 자동 갱신, 본 기록은 새 로컬 미커밋 변경이다.

## 2026-08-28 — 팀원 환경 변경 검증·정리와 AI-FRIEND-01

- 중앙 `main`을 팀원 변경 `852e6e6`까지 Fast-forward하고 LFS Object 78개를 내려받아 `git lfs fsck`를 통과했다.
- 중앙 환경 맵 3종을 새 Editor 프로세스에서 실제 로드했다. Camp 추가 외부 의존성 0, Base는 기존 `T_Linear_Grad`, Battlefield는 기존 Manny/Quinn과 새 `M_Enemy`, `M_Start`, `M_Target`만 참조하며 누락은 0이다.
- 읽기 전용 `Audit-DroneEnvironmentDependencies.py`를 추가하고 엄격한 환경 검증 허용 목록에는 확인된 세 Material만 명시했다. 수정한 검증은 세 맵 모두 성공했다.
- 팀원 변경의 `.vsconfig`를 UE 권장 14.50 구성으로 복원하고 `Drone.cpp`의 `//test`를 제거했다. 바이너리 환경 맵·Fab 자산·시험 맵은 삭제하지 않았다. 기능 `f8c8568`, Merge `888414f`로 중앙에 Push했다.
- `/Game/Drone/AI/StateTrees/ST_NPC_FriendlyBaseRoutine`을 생성했다. 상태는 Friendly Claim → 공용 Move → 공용 Wait → Friendly Release 네 단계다.
- Friendly Controller는 Base Patrol과 Ambient를 번갈아 먼저 시도하고, 빈 선호 Slot이 없으면 다른 아군 활동으로 대체한다. 직전 지점 반경 250 cm를 우선 피하며 Smart Object의 배타 Claim을 사용한다.
- Greybox Friendly 2명 각각이 2회 이상 완료하고 서로 다른 2지점 이상과 두 Activity 종류를 모두 방문하도록 `Drone.AI.NPCBaseRoutinesPIE`에서 검증했다. Hostile 2명의 기존 순찰도 같은 PIE에서 회귀 확인했다.
- Game/Editor Build 성공, AI 7/7 경고·오류 0, 전체 `Drone.` 23/23 성공이다. 22개는 무경고, 기존 `PIEInputLifecycle` 한 개만 예상 RecastNavMesh 경고를 포함한다.
- Blueprint Compile은 `0 errors / 0 warnings / 0 failed loads`다. 전역 Summary의 기존 Battlefield Pose GUID와 MCP 고지 경고 29건은 Blueprint 결과와 분리한다.
- 새 StateTree는 Git LFS 대상이며 LFS fsck를 통과했다. 기능 `b5b733f`, Merge `2fcfb04`를 한국어 메시지로 `origin/main`에 Push했다.
- 다음 기능 카드는 `AI-PER-01`이다. 현재 드론 감지는 예약을 안전 해제하지만 Search·Return·Rifle/Shotgun·MG 전환은 아직 구현하지 않았다.

## 2026-08-28 — 팀원 Fork 원격 감사와 문서 최신화

- 문서 저장소를 먼저 `main=origin/main=602c863`까지 Fast-forward한 뒤 최신 Unreal 기준선 `095dda7`과 현재 작업 순서를 대조했다. 이 항목의 문서 변경은 사용자가 직접 Commit할 예정이며 자동 Commit·Push하지 않았다.
- 중앙 `gyeonliz/drone`의 `main=095dda7`, 팀원 Fork `Yook34/drone`의 `main=0ff4fb1`을 원격에서 확인했다. Merge Base는 `095dda7`, 좌우 차이는 중앙 0 / Fork 4 Commit이다.
- 팀원 Fork 순 변경에는 `Lvl_Battlefield.umap`, `M_Enemy`, `M_Start`, `M_Target`과 함께 `.vsconfig`, PC별 `Drone.uproject` Engine Association GUID, `Drone.cpp`의 `//test`가 섞여 있다.
- 팀원 PC에서 Fork를 Clone해 `origin=Yook34/drone`인 상태라면 GitHub Desktop과 `git push origin`이 팀원 저장소로 전송되는 것이 정상이다. Git 작성자 설정이나 로그인 계정이 Remote URL을 자동으로 중앙 저장소로 바꾸지는 않는다.
- 중앙 직접 협업은 `origin=gyeonliz/drone`, 보존할 Fork는 `fork=Yook34/drone`으로 구성한다. 중앙 쓰기 권한이 없다면 `origin=Yook34/drone`, `upstream=gyeonliz/drone`으로 두고 Pull Request를 사용한다.
- 현재 Fork `main`을 중앙 `main`에 바로 Push하거나 전체 Merge하지 않는다. 중앙 `095dda7`에서 새 Feature Branch를 만들고 채택이 확인된 Battlefield Map·재질만 선별 복원한 뒤 Build·Blueprint·Automation·LFS를 재검증한다.
- `git lfs push`는 대용량 Object 전송이며 Commit·Branch Push가 아니다. 일반 `git push`가 성공해야 GitHub Desktop의 Pull/Commit 이력에 새 Git Commit이 나타난다.
- 구체 명령과 두 Remote 운영 방식은 [`GIT_UNREAL_GUIDE.md`](../git/GIT_UNREAL_GUIDE.md)에 추가했다.
- 위 항목은 원격 감사 당시 판단 기록이다. 이후 팀원 변경은 중앙에 반영됐고, 현재 판정은 바로 위 `팀원 환경 변경 검증·정리와 AI-FRIEND-01` 절을 우선한다.

## 2026-08-28 — AI-PATROL-01 Hostile Smart Object 순찰

- `/Game/Drone/AI/StateTrees/ST_NPC_HostilePatrol`을 생성하고 AI Component Schema, 네 상태와 Native Task 형식을 저장 자산으로 검증했다.
- `ClaimEnemyPatrolSlot → MoveToPatrolSlot → WaitAtPatrolSlot → ReleasePatrolSlot`을 반복한다. 기본 재검색 간격은 0.5초, 이동 수용 반경은 80 cm, 대기는 1초다.
- `UDroneSmartObjectReservationComponent`에 직전 완료 지점 반경 250 cm를 우선 피하는 검색을 추가했다. 대안이 없으면 일반 검색으로 돌아가 한 지점 맵에서도 교착되지 않는다.
- Hostile Controller는 World BeginPlay 이후 Tree를 시작한다. 이 순서로 Smart Object Runtime 초기화 전 첫 조회 경고를 제거했다. Runtime Spawn은 Controller BeginPlay가 끝난 뒤 Possess되면 즉시 시작한다.
- Hostile 2명은 EnemyPatrol만 Claim하며 완료 횟수와 서로 다른 방문 위치를 기록한다. Friendly는 `AI-FRIEND-01` 전까지 Tree를 시작하지 않는다.
- 드론 감지, 이동 실패, UnPossess에서는 이동·예약을 해제한다. 현재 감지는 순찰을 안전 중단할 뿐 Search·Return·Rifle/Shotgun·MG로 전환하지 않는다.
- `Lvl_NPCSmartObjectGreybox`의 PlayerStart를 초기 Sight 반경 밖으로 옮겨 순찰 검증 시작 즉시 감지되지 않게 했다. 플레이어가 기지에 접근하면 기존 Sight 기반은 계속 동작한다.
- StateTree와 Greybox는 각각 새 Editor 프로세스 `Validate`를 통과했다. AI 자동화 6/6은 경고·오류 0이다.
- 전체 `Drone.` 자동화 22/22는 실패 0이며 기존 `PIEInputLifecycle`의 RecastNavMesh 경고 포함 성공 1개만 남는다.
- Game/Editor Build 성공, Blueprint Compile `0 errors / 0 warnings / 0 load failures`, 새 StateTree와 갱신 맵 LFS Pointer 및 `git lfs fsck`를 통과했다. 전역 Blueprint Commandlet Summary의 기존 Battlefield Pose GUID·MCP 고지 경고 29건은 Blueprint 결과 집계와 분리한다.
- 문서 저장소에 `Setup-DroneHostilePatrolStateTree.py`와 `Invoke-DroneHostilePatrolStateTreeSetup.ps1`을 추가했다. 기존 Asset을 덮어쓰지 않고 Create 또는 읽기 전용 Validate를 수행한다.
- Unreal 기능 Commit `a721fe4`를 기능 Branch에 Push하고 Merge Commit `095dda7`로 `origin/main`에 반영했다.

## 2026-08-27 — NPC·Smart Object 기반 준비

- `SmartObjects`와 `GameplayInteractions` Plugin 및 모듈 의존성을 추가했다.
- NPC 역할을 `Neutral/Friendly/Hostile`, 무기를 `Unarmed/Rifle/Shotgun`으로 구분하고 Hostile의 MG 사용 가능 여부를 Profile로 분리했다.
- EnemyPatrol, FriendlyBasePatrol, Ambient, Guard, Cover, MGTurret Activity와 DroneDetected/DroneLost Native Gameplay Tag를 추가했다.
- 프로젝트 소유 `ADroneNPCCharacter`, `ADroneNPCAIController`, `ADroneNPCSpawnPoint`, `ADroneSmartObjectStation`과 예약 Component를 추가했다.
- Hostile은 EnemyPatrol/Guard, Friendly는 FriendlyBasePatrol/Ambient만 기본 검색한다. Required Activity가 비어 있으면 검색을 거부해 잘못된 점유를 막는다.
- Drone Prototype을 Sight 감지 대상으로 등록했다. Hostile이 드론을 감지하면 순찰 Claim을 해제하고 StateTree Event를 보내며 Friendly는 전투 전환하지 않는다.
- `UsesRifle()`과 `UsesShotgun()` 분기는 준비했지만 실제 Trace·Damage·Animation·FX·SFX는 구현하지 않았다.
- Game/Editor Build와 `Drone.AI.SmartObjectFoundationDefaults` 1/1, 전체 `Drone.` 17/17을 통과했다. 전체 자동화에는 기존 PIE RecastNavMesh 경고 1개가 있으나 실패는 0이다.
- `CompileAllBlueprints`는 Blueprint errors 0, Blueprint warnings 0, failed load 0이다. 기존 Battlefield Pose GUID와 MCP EULA 고지 Summary 경고는 새 AI 코드와 무관하게 유지된다.
- `git diff --check`, `git lfs fsck`, Unreal 프로세스 종료를 확인했다.
- Definition·Blueprint·StateTree·NavMesh·Rifle/Shotgun·MG의 Editor 작성 순서를 [`DRONE_SMART_OBJECT_NPC_GUIDE.md`](../ai/DRONE_SMART_OBJECT_NPC_GUIDE.md)에 정리했다.
- 사용자 Battlefield Map Commit `4f14d2f`을 기반으로 Branch를 만들었으며 해당 Map 변경은 수정하거나 되돌리지 않았다.
- 기능 Commit `489ced5`를 `codex/smart-object-npc-foundation`에 Push하고 Merge Commit `c3e6d38`로 `origin/main`에 반영했다.

## 2026-08-27 — AI-SO-01 Definition·Station Asset 구성

- `/Game/Drone/AI/SmartObjects/Definitions`에 EnemyPatrol, FriendlyBasePatrol, Ambient, Guard, Cover, MGTurret Definition 6종을 생성했다.
- `/Game/Drone/AI/SmartObjects/Blueprints`에 대응하는 `ADroneSmartObjectStation` 자식 Blueprint 6종을 생성했다.
- 각 Definition은 Slot 1개, 정확한 Native Activity Tag와 Gameplay Interaction Behavior 1개를 가진다.
- 각 Blueprint의 Activity와 Definition을 대응시켰고 `BP_SO_MGTurret`에만 Ground Drone Kit의 `MG_Turret_SK` 후보 Mesh를 연결했다.
- Engine Smart Object Component의 Definition 설정을 자동화가 안전하게 수행하도록 `ADroneSmartObjectStation`에 프로젝트 소유 Definition·Mesh 접근 함수를 추가했다.
- `Drone.AI.SmartObjectStationAssets` 자동화를 추가해 Definition 유효성, Slot·Tag·Behavior, Blueprint 부모·Activity·Definition·MG Mesh를 재로딩 후 검사한다.
- Game/Editor Build, 전용 AI Asset 1/1, 전체 `Drone.` 18/18, Blueprint 0 errors·0 warnings·0 load failures, LFS fsck를 통과했다. 전체 자동화의 경고 포함 성공 1개는 기존 PIE RecastNavMesh 경고다.
- Interaction StateTree는 후속 `AI-PATROL-01`·`AI-FRIEND-01`에서 연결하므로 현재 의도적으로 비어 있다. 실제 순찰·아군 이동·사격을 완료로 표현하지 않는다.
- 문서 저장소의 `tools/unreal/Setup-DroneSmartObjectStations.py`와 `Invoke-DroneSmartObjectSetup.ps1`로 정확한 12개 Asset을 재구성하거나 읽기 전용 검증할 수 있게 했다.

## 2026-08-27 — AI-NPC-01 역할 Blueprint·Greybox 맵 구성

- `/Game/Drone/AI/Blueprints`에 `BP_NPC_Hostile_Rifle`, `BP_NPC_Hostile_Shotgun`, `BP_NPC_Friendly_Base`, `BP_NPCSpawnPoint`를 생성했다.
- 역할별 Profile은 Hostile/Rifle/MG 가능, Hostile/Shotgun/MG 불가, Friendly/Unarmed/MG 불가로 분리했다.
- `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`에 Rifle 1명, Shotgun 1명, Friendly 2명과 EnemyPatrol 3·Guard 1·MGTurret 1·FriendlyBasePatrol 3·Ambient 2 Station을 배치했다.
- 시각용 바닥과 별도로 `ADroneNPCNavigationFloor`를 추가해 NavMesh에 실제 충돌 지오메트리를 제공했다. Recast는 현재 MVP 검증을 위해 Dynamic·Force Rebuild On Load로 설정했으며, 넓은 맵에서는 성능 범위를 다시 결정한다.
- StateTree Asset이 비어 있을 때 자동 시작하지 않고, 실행 중인 StateTree에만 감지 Event를 보내도록 Controller의 현재 단계 오류를 막았다.
- `Drone.AI.NPCGreyboxAssets`와 `Drone.AI.NPCGreyboxPIE` 2/2에서 Profile, Controller Possess, 역할 Tag, NPC·Station 수, Navigation Floor, Dynamic Recast, NPC 시작점 NavMesh 투영을 검증했다.
- Game/Editor Build, 전체 `Drone.` 20/20을 통과했다. 19개 정상 성공, 기존 PIE RecastNavMesh 경고 포함 성공 1개, 실패 0개다.
- Blueprint 전체 Compile은 errors 0·warnings 0·failed load 0이며, 새 패키지 5개는 LFS Pointer와 `git lfs fsck`를 통과했다.
- Manny Simple·`ABP_Unarmed`은 임시 Greybox다. 최종 Soldier/Insurgent 외형, 실제 StateTree·순찰·아군 이동·Rifle/Shotgun 사격은 아직 미구현이다.
- 기능 Commit `362edaa`를 `codex/npc-greybox-setup`에 Push하고 Merge Commit `eeb4354`로 `origin/main`에 반영했다.
- 문서 저장소의 `tools/unreal/Setup-DroneNPCGreybox.py`와 `Invoke-DroneNPCGreyboxSetup.ps1`로 자산 생성·유지보수와 읽기 전용 검증을 반복할 수 있게 했다.

## 2026-08-27 — 남은 에셋 선별 이식·OilRig·TUT-04B

- `ArmyVFX`, `InfantrySFX`, `GC_DroneS`, `Modular Soldier`, `Modular Insurgents`, Non-Pilot Quad v4, PBR Sting과 OilRig을 별도 UE 5.8 스테이징에서 검사했다.
- 실제 프로젝트에는 ThirdParty 891개와 중앙 `Lvl_OilRig` 1개만 이식했다.
- Ground Drone의 구형 PhysX 차량 Blueprint는 제외했고, Soldier/Insurgent는 외형 후보로만 이식했다.
- OilRig에서 FirstPerson 샘플 의존성을 끌어오던 `BP_Simple_Door` Actor 8개를 중앙 사본에서 제거했다.
- 새 7개 Root 수량 일치, 대표 로드 성공, 외부·누락 `/Game` 참조 0, OilRig `default_game_mode=None`을 확인했다.
- OilRig 별도 Map Check는 약 8분간 맵 Construction이 끝나지 않아 저장 없이 프로세스만 중단했다. Editor 시각·성능·Map Check는 미확인이다.
- `FDroneTrainingLapComparison`, Segment 비교, 이전 평균·Best·Delta와 `OnLapComparisonReady`를 추가했다.
- HUD에 이전 완주 평균, Best, 시간·속도 Delta 네 행을 추가했다.
- Build 성공, Blueprint 오류 0, 전체 `Drone.` 16/16 성공했다.
- 기능 Commit `3fa4444`을 `codex/remaining-asset-migration`에 Push하고 Merge Commit `55b3ffe`로 `origin/main`에 반영했다.
- 신규 Unreal 패키지 892개는 모두 LFS Pointer로 커밋됐고 4.9GB 업로드 및 `git lfs fsck`를 통과했다.
- 상세 범위와 수동 확인은 [`DRONE_REMAINING_ASSET_MIGRATION_2026-08-27.md`](../assets/DRONE_REMAINING_ASSET_MIGRATION_2026-08-27.md)를 따른다.

## 2026-08-21 — Camera·Mouse·Gamepad 기준선 갱신

### 실제 변경

- SpringArm을 Controller 자유 회전에서 Drone Yaw를 따르는 고정 추적 Camera로 변경
- Mouse X를 Drone Actor Yaw, Mouse Y를 CameraBoom Pitch로 분리
- Gamepad Left Stick 이동, `RT/LT` 고도, Right Stick X Yaw, Right Stick Y Camera Pitch 추가
- Input Action을 5개, IMC Mapping을 15개로 확장
- PIE lifecycle 테스트를 Keyboard·Mouse·Gamepad와 복합·반대 입력까지 확장
- Tutorial·Story 공통 구조와 실행 순서를 `DRONE_TUTORIAL_STORY_PLAN.md`로 확정

### 검증 결과

- `DroneEditor Win64 Development` 빌드 성공
- Blueprint 전체 Compile: 0 errors, 0 warnings
- `PawnDefaults`, `PIEInputLifecycle`, `SpawnPossess`: 3 succeeded, 0 failed
- 새 PIE 3회에서 입력과 IMC 중복 없음 확인
- Prototype 자산 9개, Input Action 5개, Mapping 15개 확인
- `/Game/Drone`에서 동결한 Legacy 자산으로 향하는 의존성 0개
- 기존 ThirdPerson 기본 Map 로드 유지
- 두 저장소 `git diff --check` 통과

### 남은 작업

- 사용자 수동 확인으로 Camera·Keyboard·Mouse 조작 수정이 정상임을 확인함
- 실제 Gamepad가 연결되어 있으면 Stick·Trigger 체감 확인하고, 없으면 `미확인`으로 기록
- 창 닫기 뒤 `Win RequestExit`, `Game engine shut down`, `Exiting` 로그와 프로세스 종료를 확인함
- PFN-06을 Done으로 판정

### 다음 구현

PFN-06 통과 후 `HUD-01`을 시작한다. Drone Telemetry를 10Hz Snapshot으로 제공하고 속도·고도·수직 속도·Heading을 공용 HUD에 표시한다.

### 수동 판정 마감

- 사용자 보고: 조작 수정 정상
- 종료 방식: `Esc`가 아닌 창 닫기
- 로그 판정: 정상 종료, Fatal·Assertion 없음
- Gamepad 체감: 연결 여부 미보고로 미확인
- 최종 판정: PFN-06 Done, `HUD-01` Ready
- Unreal 로컬 Commit: `2c38ebf` (`feat: finalize prototype camera and input lifecycle`)
- 원격 Push: 수행하지 않음

## 2026-08-21 — HUD-01 시작

### 현재 설계

- 공용 Snapshot은 속도 km/h, 기준면 대비 고도 m, 수직 속도 m/s, Heading 0~359°를 가진다.
- `UDroneTelemetryComponent`가 0.1초 간격으로 값을 갱신하고 Blueprint가 구독할 수 있는 Event를 보낸다.
- Component는 Prototype Pawn에 기본 부착하되 `/Source/Drone/Telemetry`의 재사용 가능한 생산 코드로 만든다.
- 고도는 매번 지형을 Trace하지 않고 Course/Mission이 지정하는 기준 World Z 대비로 계산한다. Tutorial 코스가 만들어지면 시작 Pad 또는 Course 기준면을 전달한다.
- Widget은 값을 계산하거나 매 프레임 Pawn을 검색하지 않는다. `HUD-02`에서 Snapshot Event를 구독한다.

### 이번 완료 조건

- Telemetry 계산과 10Hz 기본값 자동화 통과
- Prototype Pawn이 Component를 한 개 소유
- `DroneEditor Win64 Development` 빌드 성공
- 기존 Prototype 자동화 회귀 통과
- 검증 뒤 `HUD-01` Done, `HUD-02` Ready로 문서 갱신

### 구현 결과

- `FDroneTelemetrySnapshot`에 Speed km/h, Altitude m, Vertical Speed m/s, Heading degree를 정의했다.
- `UDroneTelemetryComponent`가 BeginPlay 즉시 한 번, 이후 0.1초 Timer로 Snapshot을 갱신한다.
- `OnTelemetryUpdated` Blueprint Event와 최신 Snapshot Getter를 제공한다.
- Course/Mission 기준 World Z를 런타임에 설정하면 즉시 Snapshot을 다시 계산한다.
- Prototype Pawn이 Component 한 개를 native 기본 Subobject로 소유한다.

### 검증 결과

- 최종 `DroneEditor Win64 Development` 빌드 성공
- `Drone.Telemetry.Calculation`, `Drone.Telemetry.Defaults` 통과
- `PawnDefaults`, `PIEInputLifecycle`, `SpawnPossess` 회귀 포함 최종 Report 5 succeeded, 0 warnings, 0 failed
- Runtime Spawn Pawn의 Component 존재, Spawn 고도와 Reference Z 변경 즉시 갱신 확인
- Blueprint 전체 Compile 0 errors, 0 warnings, failed load 0
- 첫 빌드 시 따옴표 없는 CompilerVersion을 PowerShell이 분리한 명령 오류가 있었고, 문자열 인자로 고정한 뒤 성공했다. 코드 컴파일 실패로 분류하지 않는다.

### 판정

- `HUD-01` Done
- `HUD-02` Ready
- 상세 구현: [`DRONE_TELEMETRY_IMPLEMENTATION.md`](../tutorial/DRONE_TELEMETRY_IMPLEMENTATION.md)
- Unreal 로컬 Commit: `08e876a` (`feat: add drone telemetry snapshot component`)
- 원격 Push: 수행하지 않음

## 2026-08-23 — HUD-02 구현·검증 완료

### 실제 변경

- `Source/Drone/UI/DroneFlightHUDWidget.*`에 C++ native UMG Flight HUD를 추가했다.
- `Source/Drone/Prototype/DronePrototypePlayerController.*`가 로컬 Player 화면에 HUD 하나를 만들고 PlayerController 수명 동안 재사용한다.
- Prototype GameMode가 전용 PlayerController를 사용하도록 연결했다.
- Widget은 현재 Possess Pawn의 `UDroneTelemetryComponent`를 찾아 `OnTelemetryUpdated`를 `AddUniqueDynamic`으로 구독하고, 연결 직후 최신 Snapshot을 한 번 적용한다.
- Pawn 전환 시 이전 Component Event를 해제하고 새 Source로 교체한다. UnPossess, Widget 종료와 Controller 종료에서도 해제를 멱등적으로 수행한다.
- Tick, UMG Property Binding, 매 프레임 Pawn 검색과 Widget 내부 단위 재계산은 사용하지 않는다.
- 현재 Prototype 표시는 `SPD %.1f km/h`, `ALT %.1f m`, `V/S %+.1f m/s`, `HDG %03d°` 형식이다. 배치·폰트·색상·Animation은 최종 디자인 확정이 아니라 교체 가능한 초기값이다.
- 현재 PC의 실제 저장소 경로는 `C:\URproject\drone`이며, 뒤처진 `C:\project\Drone` 복제본은 수정하지 않았다.

### 자동화와 수명주기 검증

- `Drone.UI.FlightHUDTelemetryBinding`이 동일 Source 중복 연결 방지, 이전 Source 해제, 새 Source 연결, 네 Text 포맷과 Clear를 확인한다.
- 기존 `PIEInputLifecycle`을 확장해 새 PIE 3회마다 Prototype PlayerController와 HUD가 정확히 하나인지, Viewport와 현재 Telemetry Source가 연결됐는지 확인한다.
- 각 PIE에서 `UnPossess → HUD Collapsed·Event 해제 → 같은 Widget 재사용 Re-Possess·Event 재연결`을 실행하고, 종료 뒤 Viewport·Telemetry·Possession Delegate 잔존이 없는지 확인한다.
- Keyboard·Mouse·Gamepad, 복합·반대 입력과 입력 세기 회귀도 같은 테스트에서 계속 통과했다.

### 최종 검증 결과

- `DroneEditor Win64 Development` 빌드 성공
- 최종 `Drone.` Automation: 6 succeeded, 0 warnings, 0 failed
- `CompileAllBlueprints`: 0 errors, 0 warnings, 0 blueprints failed to load
- 새 `.uasset`/`.umap`을 만들지 않아 `/Game/Drone`의 Legacy Variant 신규 의존성 0
- Standalone 초기 화면: `SPD 0.0 km/h`, `ALT 1.5 m`, `V/S +0.0 m/s`
- Standalone 이동: `SPD 43.2 km/h`
- Standalone 상승: `ALT 2.7 m`, `V/S +10.0 m/s`
- Standalone 하강: `V/S -7.2 m/s`
- Standalone Yaw: Heading `002° → 025°/045°`
- 단일 자동 입력을 10Hz 화면에 확실히 포착하기 위해 실행 중에만 Movement 가속·감속을 임시 조정했으며 프로젝트 기본값과 소스는 변경하지 않았다.

### 발견·수정한 문제

- 첫 테스트 빌드에서 Dynamic Multicast 검사 API 선택과 C++ 멤버 이름 가림 오류를 발견해 `Contains` 검사와 명확한 변수명으로 수정했다.
- `AddToPlayerScreen` 실패가 조용히 넘어가지 않도록 반환값 검사와 오류 로그를 추가했다.
- 기본 UMG 글자 크기가 작은 문제를 초기 Prototype 읽기 크기로 조정했다. 이는 최종 HUD 디자인 확정이 아니다.

### 판정과 Git

- `HUD-02` Done
- `TUT-01` Ready
- Unreal Commit: `410c940` (`feat: add event-driven drone flight HUD`)
- `codex/hud-02-flight-hud`와 `origin/main`에 Push 완료, 로컬 `main=origin/main=410c940`

## 2026-08-23 — HUD-02 WBP/BP 연결과 학습 주석 보강

### 실제 변경

- native `UDroneFlightHUDWidget` 자식인 `WBP_DroneFlightHUD`를 생성해 Designer에서 패널 배치·색·폰트를 편집할 수 있게 했다.
- `BP_DronePrototypePlayerController`를 만들고 `FlightHUDWidgetClass`에 `WBP_DroneFlightHUD`를 지정했다.
- `BP_DronePrototypeGameMode`의 PlayerController Class를 새 BP Controller로 연결했다.
- WBP Designer에는 C++ `BindWidget` 계약과 정확히 같은 이름의 TextBlock 4개를 둔다.

```text
SpeedValueText
AltitudeValueText
VerticalSpeedValueText
HeadingValueText
```

- C++는 Telemetry 계산, Widget 생성, Possession 동기화, Delegate 해제와 표시 문자열 포맷을 계속 담당한다. WBP는 위치·크기·색·폰트 같은 표시 외형만 담당하며 Event Graph Tick과 Property Binding은 사용하지 않는다.
- Designer Tree가 없는 native HUD Class를 직접 실행할 때의 C++ 기본 레이아웃은 유지했다. 정상 컴파일된 WBP는 필수 TextBlock 4개를 사용하며 런타임 누락 경로는 방어 코드다.
- Pawn, GameMode, PlayerController와 HUD 기반 Class를 Blueprintable로 명시하고 Blueprint에서 확인할 Getter를 정리했다.
- 입력·이동·Telemetry 단위·Widget/Controller 수명주기·C++↔WBP 이름 계약·테스트 목적을 설명하는 한국어 주석을 보강했다. 이 주석 작업은 최종 비행 물리·감도·게임 규칙을 새로 확정한 것이 아니다.

### 발견·수정한 문제

- 첫 Standalone 화면에서 WBP TextBlock의 FontObject가 비어 있어 글자가 대체 글리프로 깨졌다.
- Engine `Roboto` Font를 WBP Asset에 직렬화해 저장했고, 필수 TextBlock과 Header Font 유효성을 자동화에서 검사하도록 했다.
- “BP Asset이 사라지면 native로 자동 복구”, “항상 10Hz”, “Heading 000°는 진북”처럼 구현보다 강하게 읽히는 주석을 실제 동작에 맞게 교정했다.

### 최종 검증

- `DroneEditor Win64 Development` 빌드 성공
- `Drone.` Automation: 7 succeeded, 0 warnings, 0 failed
- 새 `Drone.UI.FlightHUDBlueprintAsset`이 WBP 부모, 필수 TextBlock 4개·Font, BP Controller→WBP, BP GameMode→BP Controller를 확인
- `PIEInputLifecycle` 새 PIE 3회에서 실제 BP Controller와 WBP Class 사용, native fallback 미사용, Widget 재사용·Delegate 정리 확인
- `CompileAllBlueprints`: 0 errors, 0 warnings, 0 blueprints failed to load
- Standalone에서 실제 WBP의 `FLIGHT DATA`, `SPD`, `ALT`, `V/S`, `HDG` 글자가 깨짐 없이 표시됨
- WBP·BP Controller 신규 Asset과 갱신 BP GameMode 모두 Git LFS 적용 확인

### 판정과 Git

- `HUD-02` Blueprint presentation follow-up 완료
- 최종 아트·Animation, 배터리·신호·Jamming 표시는 아직 미정/미구현
- `TUT-01` Ready
- Unreal Commit: `9f91bb6` (`feat: add Blueprint-backed flight HUD`)
- `codex/hud-blueprint-ready-comments`와 `origin/main`에 Push 완료, 로컬 `main=origin/main=9f91bb6`

## 2026-08-23 — TUT-01 Training Map과 비충돌 Spline 착수

### 확정 범위

- 별도 Training Map을 만든다. 당시 경로는 `/Game/Drone/Tutorial/Maps/Lvl_DroneTraining`이며 현재는 `/Game/Drone/Maps/Lvl_DroneTraining`으로 중앙화했다.
- `ADroneTrainingCourse`가 편집 가능한 `USplineComponent`와 Standalone에서도 보이는 표시용 구성요소를 소유한다.
- 표시용 Actor·Spline·Mesh의 Collision, Overlap, Physics, Navigation 영향을 모두 끈다.
- 기존 `BP_DronePrototypeGameMode`를 재사용해 Prototype Pawn/Input/HUD 기준선을 유지한다.
- Gate Trigger, 순서·방향 판정, Lap/Segment 기록은 다음 `TUT-02` 이후 범위로 남긴다.

### 검증 예정

- native Course 기본값과 Pawn 크기 Sweep 비간섭 자동화
- 실제 BP Course와 Training Map 계약 자동화
- Training Map PIE에서 BP Pawn·Controller·WBP와 표시선 생성 확인
- Editor Build, 전체 Blueprint Compile, 전체 `Drone.` 회귀, Standalone 시각·비행 확인

### 현재 판정

- `TUT-01` Doing
- Unreal 작업 Branch: `codex/tutorial-training-course`
- Unreal Commit: 아직 미커밋

## 2026-08-23 — TUT-01 Training Course 구현·검증 완료

### 실제 변경

- `ADroneTrainingCourse`에 편집 가능한 `USplineComponent`와 런타임 표시용 `USplineMeshComponent` 구성을 구현했다.
- 실제 `BP_DroneTrainingCourse`와 별도 `Lvl_DroneTraining` Map을 만들고 기존 `BP_DronePrototypeGameMode`를 재사용했다.
- `M_DroneTrainingGuide`를 Opaque·Unlit·Emissive·Spline Mesh 용도로 만들고 Standalone에서 식별 가능한 밝은 Cyan 표시선을 구성했다.
- Course Actor와 Spline 표시 구성요소의 Collision, Overlap, Physics, Navigation 영향을 모두 껐다.
- native Course 기본 계약, 실제 BP/Map Asset 계약, Training Map PIE 수명주기와 비간섭을 검사하는 Tutorial 자동화 테스트 3개를 추가했다.
- 학습할 때 구현 의도와 C++·Blueprint 역할을 따라갈 수 있도록 Course와 테스트 코드에 한국어 주석을 추가했다.

### 최종 검증 결과

- `DroneEditor Win64 Development` 빌드 성공
- `Drone.Tutorial` Automation: 3 succeeded, 0 warnings, 0 failed
- 전체 `Drone.` Automation: 10 succeeded, 0 warnings, 0 failed
- `CompileAllBlueprints`: 0 errors, 0 warnings, 0 blueprints failed to load
- Standalone에서 실제 BP Pawn·Controller·WBP HUD와 밝은 Cyan Course Spline 표시 확인
- Spline Mesh Material Usage 경고 없음
- 실제 Pawn Sweep이 표시선을 통과하고 목표 위치에 도달해 Blocking 없음 확인
- Course 소유 표시 구성요소의 Collision·Overlap·Physics·Navigation 관련 Flag가 모두 꺼져 있음 확인
- Training Map에 저장된 Recast Actor 확인

### 범위 정지선

- TUT-01은 Training Map, 편집 가능한 Course Spline과 비간섭 표시선까지만 완료했다.
- Gate, Trigger, 순서, 방향, Lap, Timing은 구현하지 않았으며 `TUT-02` 이후 범위다.
- Android는 사용자 결정에 따라 작업 범위에서 제외한다.
- Map과 다음 카드 담당자는 현재 미정이다.

### 판정과 Git

- `TUT-01` Done
- `TUT-02` Todo
- Unreal Commit: `5a9a2faed4591a574988b649278cb0f166e31267` (`feat: add tutorial training course`)
- `codex/tutorial-training-course`와 `origin/main`에 Push 완료, 로컬 `main=origin/main=5a9a2faed4591a574988b649278cb0f166e31267`

## 2026-08-24 — TUT-02 Ordered Ring Gate 구현·검증 완료

### 실제 변경

- `ADroneTrainingGate`에 Engine Cube 16조각으로 만든 비충돌 Ring Visual과 별도 `UBoxComponent` Pawn Overlap Trigger를 구현했다.
- `UDroneTrainingGateSequenceComponent`가 Course의 명시적 `OrderedGates` 배열을 단일 순서 기준으로 사용하도록 구성했다.
- 현재 Gate의 정방향 통과만 한 번 승인하고 잘못된 Actor, 미래 Gate, 역방향, 중복 통과와 잘못된 구성을 거부하도록 구현했다.
- Gate 외형은 `Current`, `Completed`, `Inactive` 상태로 분리하고, 정상 승인 시 다음 Gate로 정확히 한 칸 진행한다.
- 실제 `BP_DroneTrainingGate`를 추가하고 `Lvl_DroneTraining`에 네 Gate를 배치해 Course 배열과 연결했다.
- `SegmentDistance`는 후속 기록용 메타데이터로만 저장한다. TUT-02 판정에서 Lap·Timing·거리·평균 속도 계산에는 사용하지 않는다.
- 정상 Gate 승인 Event를 제공하되 기록 계층은 TUT-03에서 별도로 구독하도록 경계를 유지했다.

### 최종 검증 결과

- `DroneEditor Win64 Development` 빌드 성공
- `Drone.Tutorial.TrainingGateSequence`: 1 succeeded, 0 warnings, 0 failed
- 실제 BP Gate Begin/End Overlap을 포함한 `Drone.Tutorial.TrainingPIESmoke`: 1 succeeded, 0 warnings, 0 failed
- 전체 `Drone.Tutorial`: 4 succeeded, 0 warnings, 0 failed
- 전체 `Drone.`: 11 succeeded, 0 warnings, 0 failed
- `CompileAllBlueprints`: 0 errors, 0 warnings, 0 blueprints failed to load
- Standalone에서 실제 WBP HUD, Cyan Course 안내선과 Current/Inactive Gate 표시 확인
- 신규 `BP_DroneTrainingGate`와 갱신한 `Lvl_DroneTraining` 두 Asset의 Git LFS 적용과 Push 확인

### 범위 정지선

- Gate Visual·Trigger, 명시적 순서, 정방향·중복 통과 판정과 시각 상태까지 TUT-02로 완료했다.
- Lap 시작·완료, Segment/Lap Timing, 실제 이동 거리·평균 속도, 이전 기록 비교와 결과 UI는 구현하지 않았다.
- 다음 활성 카드는 `TUT-03 Segment/Lap 기록`이다.
- Android와 구매 에셋은 현재 범위에서 제외한다.

### 판정과 Git

- `TUT-02` Done
- `TUT-03` Todo
- Unreal Commit: `800a7baaf8247bf0a3ee7bccc2272e12d0098f2b` (`feat: add ordered tutorial ring gates`)
- `codex/tutorial-ring-gates`와 `origin/main`에 Push 완료, 로컬 `main=origin/main=800a7baaf8247bf0a3ee7bccc2272e12d0098f2b`

## 2026-08-25 — 제공 에셋 14팩 인수 감사와 이식 계획

### 실제 확인

- 사용자 입력 경로 `D:\JGY\project\Unreal\_260821`은 존재하지 않고 실제 폴더는 `D:\JGY\project\Unreal_260821`임을 확인했다.
- 최상위 ZIP 14개와 같은 이름의 해제 폴더 14개를 파일별 상대 경로와 크기로 대조했다.
- 모든 팩이 `Missing 0 / Extra 0 / SizeMismatch 0`으로 일치했다.
- 해제 결과는 10,499개 파일과 35,677,612,290 bytes이며 `.uasset` 10,445개, `.umap` 25개다.
- 외부 ZIP은 모두 해제됐지만 `Non-Pilot Drones KITBASH SET\FBX.zip` 안의 개별 FBX 55개는 내부 압축 상태로 남아 있다.
- Drone 저장소는 `main=origin/main=800a7ba`, 작업 트리 Clean이며 외부 에셋을 아직 추가하지 않았다.
- Drone Content는 768개·141,255,461 bytes이고 D Drive 여유 공간은 약 944 GB라 스테이징 여유는 충분하지만, 제공 에셋 전체를 LFS에 넣지 않기로 했다.

### 호환성 판정

- 확인된 제작 버전 단서는 UE 4.23~5.6이며 현재 프로젝트 UE 5.8에서 상향 변환·재저장이 필요하다.
- `DronePack_Project`는 UE 5.1 완전 프로젝트이고 내부 루트는 `/Game/Drone_Pack`이다.
- `GC_DroneS`는 UE 4.24와 `PhysXVehicles` 의존성이 있어 기능 Blueprint를 재사용하지 않고 Mesh·Material·Turret Part만 후보로 둔다.
- `OilRigLiope_Tr` 해제 폴더의 실제 패키지 루트는 `/Game/Liope_Tr`이다.
- 일부 팩에서 제공 폴더 밖 `/Game` 참조 단서를 발견해 스테이징 Asset Audit 전 Demo 자산의 직접 이식을 금지했다.

### 이식 결정

- 원본 ZIP·해제본은 보존하고 UE 5.8 스테이징 복사본에서 팩 하나씩 검증한다.
- 필요한 의존성만 Content Browser에서 `/Game/Drone/ThirdParty/<Pack>`으로 이동·재저장한 뒤 실제 프로젝트로 Migrate한다.
- 프로젝트 연결은 `/Game/Drone/Integrations/<Pack>`에서 만들고 현재 C++ Collision Root·Movement·Camera·Telemetry를 유지한다.
- 외부 Pawn, GameMode, PlayerController, Input Mapping과 Demo Level Blueprint는 사용하지 않는다.
- 첫 최소 Spike는 `DronePack_Project`의 FPV Body·Rotor·Material과 `Drone-Sounds` 44.1 kHz Loop Cue 하나다.

### 판정과 다음 작업

- `AST-00` 제공 에셋 인수 감사 Done
- 실제 에셋 이식 0건
- 내부 `FBX.zip` 별도 해제 필요
- 기능 실행 순서는 유지하며 다음 활성 카드는 `TUT-03 Segment/Lap 기록`
- 상세 결과: [`DRONE_ASSET_INTAKE_2026-08-25.md`](../assets/DRONE_ASSET_INTAKE_2026-08-25.md)

## 2026-08-25 — AST-01 FPV 최소 외형·Loop 선별 이식

### 실제 변경

- `D:\JGY\project\Unreal_260821\_Staging\DroneAssetStage` UE 5.8 스테이징 프로젝트를 만들고 DronePack FPV와 Drone-Sounds만 복사했다.
- 공급사 Blueprint 전체 Compile 결과는 `0 errors / 27 warnings / 0 load failures`였다. 경고가 구형 Input Axis와 누락 Mannequin Rig 참조에 집중되어 외부 기능 Blueprint 재사용 금지 판정을 확정했다.
- FPV Body·Rotor A~D·Material·Texture 4개와 44.1 kHz Cue/Wave, 총 12개·21,753,071 bytes만 `/Game/Drone/ThirdParty`로 이동·UE 5.8 재저장해 실제 프로젝트에 이식했다.
- `/Game/Drone/Integrations/DronePackFPV/BP_DroneFPVIntegration`을 만들었다. 기존 `ADronePrototypePawn`의 Collision Root·Movement·Camera·Input·Telemetry를 유지하고 본체 1, Rotor 4, Audio 1만 추가했다.
- 모든 FPV Visual은 Collision·Overlap·Physics·Navigation 영향을 끄고 기존 Sphere Collision Root와 분리했다.
- `BP_DronePrototypeGameMode`가 FPV Integration Pawn과 기존 `BP_DronePrototypePlayerController`를 명시적으로 사용하도록 연결했다.
- 기존 Prototype/Training PIE 테스트가 실제 FPV Integration Pawn Class를 기대하도록 갱신하고 `Drone.Integration.FPVAsset` 계약 테스트를 추가했다.

### 검증 중 발견·수정

- 첫 자동화에서 GameMode의 PlayerController 기본값이 비어 PIE 시작이 실패하는 문제를 발견했다. 이식 스크립트가 Pawn과 BP PlayerController를 함께 고정하도록 수정했다.
- 첫 자산 테스트는 Blueprint SCS Component를 CDO에서 찾으려 해 본체만 보였다. transient World에 실제 Pawn을 Spawn해 런타임 Component를 검사하도록 수정했다.
- 이식 스크립트 재실행 시 Template Object 이름과 SCS 변수명이 달라 Rotor·Audio가 중복되는 문제를 발견했다. 이름이 아니라 Mesh/Sound Asset 참조 기준으로 중복 제거하고 재실행 안전성을 확보했다.
- Editor가 Camera 표시용으로 생성하는 `UCameraProxyMeshComponent`를 Drone 외형으로 잘못 센 테스트를 수정했다. 실제 SCS는 본체 1·Rotor 4·Audio 1이다.
- 제공 Cue는 이름에 `Loop`가 있지만 실제 `IsLooping()`은 false였다. 프로젝트 이식본 SoundNode Wave Player의 Looping을 켜고 계약 테스트에 `SoundBase::IsLooping()` 검사를 추가했다.

### 최종 검증

- `DroneEditor Win64 Development`: MSVC 14.51.36256 명시 Build 성공
- 전체 Blueprint Compile: `0 errors / 0 warnings / 0 load failures`
- Map Check: `0 errors / 0 warnings`
- 선택 자산 12개: 외부 `/Game` 의존성 0, Integration의 ThirdPerson·Variant·원본 Vendor Root 의존성 0
- Loop 설정 수정 뒤 최종 전체 `Drone.` Automation: `12 succeeded / 0 failed / 0 warnings`
- `PIEInputLifecycle`: 새 PIE 3회 모두 FPV Pawn·IMC·Keyboard/Mouse/Gamepad·복합/반대 입력 회귀 통과
- Standalone Training Map: FPV 외형·고정 추적 Camera·기존 HUD/Course/Gate 초기 화면 캡처와 정상 종료 확인
- 첫 실제 렌더에서 4K Texture DDC를 생성하느라 종료 후 약 76초를 더 기다렸지만 `Game engine shut down`과 `Exiting`까지 정상 완료

### 현재 판정과 다음 작업

- `AST-01`은 코드·자산·자동 회귀·초기 화면까지 통과했다.
- 실제 스피커에서 Drone Loop 단일 재생과 종료 시 정지를 듣는 수동 확인만 남아 Doing으로 유지한다.
- 사용자 청감 확인이 통과하면 `AST-01`을 Done으로 이동하고 `TUT-03 Segment/Lap 기록`으로 복귀한다.
- Unreal과 문서 저장소 변경은 로컬 미커밋이며 Push하지 않았다.

## 2026-08-25 — UE-MCP-01 공식 Unreal MCP·Codex 연결

### 확인과 방향 전환

- 사용자가 전달한 Unreal Engine KR YouTube Community 게시물을 확인했다.
- 게시물은 UEFN MCP 공개 소식이지만, 연결된 Epic 기사에서 UE 5.8 일반 Unreal Editor에도 `ModelContextProtocol`이 포함됐음을 확인했다.
- UE 5.8 공식 문서에서 Unreal MCP가 Editor 프로세스 내부 HTTP 서버, Toolset Registry, Codex 프로젝트 설정 생성을 공식 지원함을 확인했다.
- 처음 추가했던 파일 기반 `DroneEditorBridge` 초안은 공식 기능과 중복되어 빌드 전에 전부 제거했다.

### 실제 구성

- `Drone.uproject`에 `ModelContextProtocol`을 Editor Target으로 활성화했다.
- Drone 작업에 필요한 `EditorToolset`, `AutomationTestToolset`, `UMGToolSet`, `StateTreeToolset`, `AIModuleToolset`만 선택했다.
- PCG·Niagara·GAS·Dataflow 등 현재 불필요한 플러그인을 함께 활성화하는 `AllToolsets`는 제외했다.
- `DefaultEditorPerProjectUserSettings.ini`에 `bAutoStartServer=True`, Port 8000, Path `/mcp`, Tool Search 활성 기본값을 추가했다.
- `.codex/config.toml`에 `unreal-mcp` 프로젝트 연결과 `default_tools_approval_mode="writes"`를 기록했다.
- 서버는 인증 없는 Experimental 기능이므로 `127.0.0.1` loopback 외부로 공개하지 않는다.

### 빌드에서 발견한 기존 경계 오류

- `DroneEditor Win64 Development`는 즉시 성공했다.
- 최초 `Drone Win64 Development`는 `DroneTrainingCourseTest`와 `DroneTrainingGateSequenceTest`의 `RerunConstructionScripts()`가 게임 Development에도 컴파일되어 실패했다.
- 두 테스트의 가드를 `WITH_DEV_AUTOMATION_TESTS`에서 `WITH_EDITOR && WITH_DEV_AUTOMATION_TESTS`로 좁혔다.
- 생산 Runtime API 변경 없이 재빌드한 `Drone Win64 Development`가 성공했다.

### 최종 회귀와 MCP 왕복 검증

- 전체 `Drone.` 자동화는 12/12 Success, Exit Code 0이다.
- 실제 Unreal Editor를 Training Map으로 열고 PID가 `127.0.0.1:8000`을 Listen함을 확인했다.
- MCP `initialize` HTTP 200과 Session ID, `notifications/initialized` 202, `tools/list` 200을 확인했다.
- Tool Search 메타 툴 `list_toolsets`, `describe_toolset`, `call_tool`이 반환됐다.
- 선택 Plugin 구성에서 총 23개 Toolset이 검색됐다.
- 실제 MCP 호출로 당시 Current Level `/Game/Drone/Tutorial/Maps/Lvl_DroneTraining`, PIE false, Selected Actors 0, Content Browser `/Game/Drone/Prototype/Maps`를 조회했다. 현재 Map 경로는 `/Game/Drone/Maps/Lvl_DroneTraining`이다.
- `AutomationTestToolset.DiscoverTests`는 `ready`, `ListTests`의 `Drone.` 필터는 12개를 반환했다.
- Codex 앱 번들 CLI는 WindowsApps 권한 거부로 PowerShell의 `codex mcp list`를 실행하지 못했다. 이는 Unreal MCP 서버나 프로젝트 TOML 오류가 아니라 현재 앱 패키지 실행 경계다.

### 판정과 다음 작업

- `UE-MCP-01` Done
- `UE-MCP-02` Todo — Drone 루트에서 새 Codex 작업을 열었을 때 네이티브 Tool 노출과 Current Level 호출을 한 번 확인
- Unreal Editor와 MCP 서버는 실행 상태로 유지한다.
- 현재 대화는 Drone 루트에서 시작한 Codex 작업이 아니므로 새 `.codex/config.toml`이 Tool 목록에 즉시 재주입되지 않는다. 후속 작업은 Editor를 먼저 열고 `D:\JGY\project\drone` 루트에서 Codex 작업을 열어 공식 MCP를 직접 사용한다.
- `AST-01` 실제 Loop 청감 확인은 여전히 남아 있으며, 통과 후 `TUT-03 Segment/Lap 기록`으로 복귀한다.
- 상세 사용법: [`DRONE_UNREAL_MCP.md`](../git/DRONE_UNREAL_MCP.md)

## 2026-08-25 — AST-01 수동 미확인 기준선과 Git 담당 확정

### 현재 판정

- FPV·Sound 선택 자산 12개와 프로젝트 소유 Integration BP 1개는 실제 Drone 프로젝트에 들어 있다.
- 전체 제공 에셋 14팩 35.7 GB는 의도적으로 프로젝트에 복사하지 않고 `D:\JGY\project\Unreal_260821`에 원본으로 보존한다.
- Build, Blueprint Compile, Map Check, 전체 `Drone.` Automation 12/12와 Standalone 초기 렌더·정상 종료는 통과 상태를 유지한다.
- 실제 스피커에서 Drone Loop가 한 번만 재생되는지와 Standalone 종료 후 멈추는지는 아직 수동 확인하지 않았다.
- 청감 결과는 실패가 아니라 `미확인`이며, 확인 전에는 성공으로 추정하거나 `AST-01`을 Done 처리하지 않는다.

### 다음 작업과 Git

- `AST-01`은 Doing으로 유지하고 수동 청감 결과가 생길 때 판정만 갱신한다.
- 다음 기능 카드는 `TUT-03 Segment/Lap 기록`이다.
- 현재 Drone·문서 작업 트리의 Stage·Commit·Push는 사용자가 직접 수행한다. 이번 문서 최신화에서는 Git 변경을 전송하지 않는다.

## 2026-08-25 — TUT-03 Segment/Lap 원본 기록

### 실제 구현

- `FDroneTrainingSegmentRecord`와 `FDroneTrainingLapRecord`에 Gate 구간, World Game Time 기준 경과 시간, 실제 이동 거리와 평균 속도 원본 값을 정의했다.
- `UDroneTrainingLapRecorderComponent`를 `ADroneTrainingCourse`가 소유하도록 추가하고 실제 Play 수명주기에서 Gate Sequence에 연결했다.
- Gate 0의 정상 승인을 Lap 시작선으로 사용한다. Gate가 N개면 Gate 0 이후 정상 Gate마다 Segment를 하나 완성하므로 성공 Lap은 N-1개 Segment를 가진다.
- 기록기는 기존 `UDroneTelemetryComponent`의 기본 10 Hz Snapshot Event에서 같은 Drone의 3차원 World 위치를 표본화한다. 별도 Actor Tick이나 Timer는 추가하지 않았다.
- Segment와 Lap 평균 속도는 `실제 이동 거리 / World Game Time`으로 계산하고 Unreal cm를 m와 km/h로 변환한다.
- Gate Sequence의 정상 승인 Event에 실제 통과 Actor와 승인 위치를 추가하고, Restart·재구성 시 부분 기록을 폐기할 수 있도록 Reset Event를 추가했다.

### 확정한 기록 경계

- Gate 0 이전 이동은 기록하지 않고 Gate 0 승인 위치부터 거리를 누적한다.
- `SegmentDistance`는 계속 후속 도구용 메타데이터이며 기록 거리 계산에 사용하지 않는다. 실제 경로는 Telemetry 위치 표본 사이의 3차원 거리 합으로 계산한다.
- 현재 Lap은 Gate 0을 통과한 같은 Drone만 이어 쓴다. 진행 중인 Drone이 파괴되거나 다른 Actor가 다음 Gate를 통과하면 부분 시도를 성공 기록으로 남기지 않는다.
- `ResetSequence()`는 진행 중인 시간·거리·부분 Segment만 폐기하고 이미 완료한 성공 Lap History는 현재 실행 동안 유지한다. Course 재구성은 코스 호환성이 달라질 수 있으므로 부분 시도와 성공 History를 함께 비운다.
- 평균 계산 함수는 0초·음수 시간이나 비정상 거리 입력에서 NaN·Infinity 대신 0을 반환한다. Recorder가 같은 Frame의 0초 Gate 경계를 받으면 가짜 기록을 확정하지 않고 해당 부분 시도를 취소한다.
- 이전 평균·Best·점수·결과 화면과 `USaveGame` 영속화는 TUT-03에 포함하지 않고 다음 `TUT-04` 이후 책임으로 유지한다.

### 자동화와 최종 검증

- `Drone.Tutorial.TrainingRecordCalculation`에서 cm/s 변환, 정상 평균 속도와 0·음수·NaN·Infinity 입력 안전성을 검증했다.
- `Drone.Tutorial.TrainingLapRecorder`에서 실제 `FTestWorldWrapper`의 Course, Gate 3개, Drone, Sequence와 Telemetry를 사용해 정상 2-Segment Lap을 검증했다.
- Lap Recorder 테스트는 꺾인 위치 표본의 실제 거리 합, World Game Time, Segment/Lap 평균 속도, 미래·역방향·중복 Gate 불변, 중간 Reset과 성공 History 보존, Course 재구성 시 History 초기화, 활성 Pawn 파괴 취소를 확인했다.
- `Drone.Tutorial.TrainingPIESmoke`를 실제 저장된 BP Gate 0→3 Overlap과 Recorder 상태까지 확장했다.
- `DroneEditor Win64 Development` Build 성공
- 전체 Tutorial 자동화: `6 succeeded / 0 failed / 0 warnings`
- 전체 `Drone.` 자동화: `14 succeeded / 0 failed / 0 warnings`
- 전체 Blueprint Compile: `0 errors / 0 warnings / 0 load failures`

### Git과 현재 판정

- `TUT-03` Done
- `TUT-04` Todo — 이전 성공 기록 평균·Best 비교와 Course/Gate/Lap 결과 UI
- Unreal Commit: `551e287e8a5de7fa33f28d1911f8a7a957bd66fa` (`feat: record tutorial lap timing and distance`)
- `codex/tutorial-lap-recording`과 `origin/main`에 Push 완료, 로컬 `main=origin/main=551e287e8a5de7fa33f28d1911f8a7a957bd66fa`

### 남은 사용자 수동 확인

- `Lvl_DroneTraining`에서 실제 Drone으로 Gate 0→3을 순서대로 통과해 조작감, Gate 간격과 시각 전환에 불편이 없는지 확인한다.
- TUT-03은 계산과 원본 기록까지라 결과 UI는 아직 없다. 시간·거리·평균·Best 비교 화면은 `TUT-04`에서 연결한다.
- `AST-01`의 실제 스피커 Drone Loop 단일 반복 재생과 Standalone 종료 후 정지는 여전히 미확인이다. 이 항목은 TUT-03 완료와 섞지 않고 별도 Doing으로 유지한다.

## 2026-08-25 — `C:\에셋` 제공 에셋 루트와 프로젝트 이식 재검증

### 현재 제공 에셋 위치 감사

- 사용자가 지정한 현재 제공 에셋 루트 `C:\에셋`을 읽기 전용으로 다시 감사했다. 이 PC에는 이전 D 드라이브 두 후보 경로가 없다.
- 공급사 해제본 14개 기준선은 최초 감사와 같은 10,499개·35,677,612,290 bytes다.
- `_Staging`, 내부 FBX 해제본, Unreal 생성 캐시를 포함한 현재 전체는 10,928개·866개 폴더·36,360,181,427 bytes다.
- 최초 감사에 사용한 최상위 ZIP 14개는 현재 C 드라이브에 없다. 과거 ZIP 14/14 대조 결과를 현재 재실행 결과처럼 사용하지 않고 역사 기록으로 구분했다.
- 현재 유일한 Archive인 `Non-Pilot Drones KITBASH SET\FBX.zip`의 55개 FBX와 해제 폴더 55개를 SHA-256으로 대조해 불일치 0을 확인했다.
- 라이선스·EULA·README·Manual 파일은 확인되지 않았다. `PBR Sting` Metadata의 `isAiForbidden: true`는 라이선스 자체가 아니므로 구매 증빙과 권리 조건을 별도로 보존·확인한다.
- `C:\에셋\DronePack_Project\Config\DefaultEngine.ini`의 활성 Android File Server에는 비어 있지 않은 토큰이 있었다. 값은 출력하거나 복사하지 않았고, 이 소스 팩 Config 전체를 이식·Commit 금지로 기록했다. 실제 Drone 프로젝트는 Plugin·네트워크 꺼짐, 빈 토큰 상태다.

### 실제 이식 대조

- `C:\URproject\drone\Content\Drone\ThirdParty` 12개·21,753,071 bytes와 `Content\Drone\Integrations`의 프로젝트 소유 BP 1개·34,484 bytes를 확인했다.
- FPV 10개와 Sound Wave는 UE 5.8 스테이징본과 SHA-256이 일치했다. Cue는 프로젝트에서 실제 Loop 설정을 켠 뒤 재저장했기 때문에 의도적으로 다르며 전용 테스트가 Loop 계약을 확인한다.
- 스테이징 선택 자산 감사와 현재 Integration Asset Registry 재감사에서 원본 `/Game/Drone_Pack`, `/Game/Drone-Sounds`, ThirdPerson, Variant 금지 의존성은 0이었다.
- Integration BP는 native Prototype Pawn을 부모로 사용하고 Body 1·Rotor 4·Auto Activate Audio 1만 더한다. Visual Collision·Overlap·Physics·Navigation은 꺼지고 native Collision Root·Movement·Camera·Input·Telemetry를 유지한다.

### 검증과 판정

- `Drone.Integration.FPVAsset` 새 실행: 1/1 Success
- 전체 Blueprint Compile 새 실행: 0 errors, 0 warnings, 0 failed to load
- 이식된 13개 `.uasset` 모두 Git LFS 대상, `git lfs fsck` 통과
- Unreal 저장소 `main=origin/main=551e287`, 작업 트리 깨끗함
- 전체 `Drone.` 14/14는 같은 현재 Commit에서 TUT-03 완료 시 통과한 전체 기준선이며 이번 재감사에서 전체 묶음을 다시 실행한 것으로 과장하지 않는다.
- 기존 Standalone 초기 렌더는 통과 기록이 있지만 이번 재감사에서 새 시각 캡처와 실제 청감은 하지 않았다. Body·Rotor·Camera 배치와 Loop 단일 재생·여러 경계·종료 정지는 사람이 확인해야 한다.
- 이식 파일·참조·구조는 Pass다. 실제 청감은 미확인이므로 `AST-01`은 Doing을 유지한다.

## 2026-08-26 — AST-02A NavigationArrows 1차 이식

### 사용자 확인과 범위

- 사용자가 제공 에셋은 지원과정을 통해 구매·지급된 것이므로 프로젝트 사용에 문제가 없다고 확인했다.
- 로컬 라이선스·영수증 파일 미발견은 증빙 보관 상태로 따로 기록하고 이식 차단으로 취급하지 않았다.
- 원본 11개 전체를 넣지 않고, 화면 밖 목표 방향 표시 Widget의 최소 폐쇄 집합만 이식하기로 했다.

### 실제 변경

- 별도 `NavigationArrowsStage` UE 5.8 프로젝트에서 원본 경로 `/Game/NavigationArrows`를 유지해 11개를 먼저 로드했다.
- Unreal 내부 이동으로 6개를 `/Game/Drone/ThirdParty/NavigationArrows`에 옮겨 참조를 갱신하고 재저장했다.
- Widget Blueprint 1개, Texture2D 2개, UserDefinedStruct 3개만 실제 Drone 프로젝트에 복사했다.
- Demo Map·BuiltData·Example Actor·Example Mesh·미사용 Circle Texture는 제외했다.
- `DroneNavigationArrowsAssetTest.cpp`를 추가해 Generated Class, Target 변수 계약, Texture·Struct 로드와 제외 자산 부재를 검증했다.
- 재현용 `tools/unreal/Audit-NavigationArrows.py`, `tools/unreal/Stage-NavigationArrows.py`를 문서 저장소에 추가했다.

### 검증 결과

- 원본·대상 Asset Registry 감사: 로드 실패 0, 외부 `/Game` 의존성 0
- UE 5.8 스테이징 Target Blueprint Compile: 0/0/0
- `DroneEditor Win64 Development`: 성공
- 전용 자동화: 1/1 성공
- 전체 `Drone.`: 15/15 성공, warning·failure 0
- 실제 프로젝트 Blueprint Compile: 0 errors, 0 Blueprint warnings, 0 failed loads
- 프로젝트 6개가 검증된 스테이징 6개와 SHA-256 일치
- Git LFS 속성 6/6, `git lfs fsck` 정상

첫 C++ 빌드는 `UUserDefinedStruct` 헤더 경로를 잘못 적어 실패했다. UE 5.8 실제 경로인 `StructUtils/UserDefinedStruct.h`로 수정한 뒤 빌드가 성공했다. 첫 전용 테스트는 Blueprint 변수의 GUID 접미사를 고려하지 않아 `TargetWorldLocation` 탐색이 실패했고, 접두사 기반 반사 검사로 수정한 뒤 1/1과 전체 15/15를 통과했다. 두 실패는 수정 전 검사 결함이며 최종 자산 결함으로 남지 않는다.

### 현재 판정

- 기술 이식·검증: 완료
- Git: Commit `5a052c8`을 `origin/codex/navigation-arrows-migration`에 Push 완료. 이후 `fb1d7ad`로 main 병합·Push 완료
- 실제 화면 연결: 미구현. 자산이 준비됐을 뿐 Training HUD 기능 완료가 아님
- `AST-01`: 실제 스피커 Loop 확인 전까지 계속 Doing
- `TUT-04`: 다음 기능 카드 유지

## 2026-08-26 09:17 — 작업 PC·Git·Editor 상태 재동기화

### 실제 확인

- 현재 Unreal 작업 경로는 `D:\JGY\project\drone`, 문서 경로는 `D:\JGY\project\md`다.
- Drone 로컬 `main`과 `origin/main`은 `551e287`로 일치하고 작업 트리는 깨끗하다.
- NavigationArrows 최소 이식은 Commit `5a052c8bab2eb0dd8bc9ab16cfc7b3784e8e4cd7`로 `origin/codex/navigation-arrows-migration`에 Push됐다. 이 Commit의 부모는 `551e287`이며 main에는 아직 병합하지 않았다.
- 문서 저장소는 최신화 직전 로컬 `main=origin/main=466609d`이고 작업 트리가 깨끗했다. 이번 최신화는 로컬 문서 변경으로 남기며 Commit·Push는 사용자가 수행한다.
- 현재 PC의 제공 에셋 루트는 `D:\JGY\project\Unreal_260821`이다. ZIP 14개·공급사 폴더 14개와 `_Staging`을 확인했고 `C:\에셋`은 이 PC에 없다.
- UE 5.8.1 Editor PID 9884가 D 드라이브 프로젝트로 실행 중이다. 로그에 MCP 서버 시작과 23 Toolset 등록이 있고 `127.0.0.1:8000/mcp`가 응답한다.

### 판정과 다음 작업

- `AST-02A` 최소 이식·검증·main 공유는 Done이다. 실제 Navigation Host/Wrapper는 후속 카드다.
- `UE-MCP-02`는 Drone 루트의 새 Codex 작업에서 네이티브 Tool 노출을 확인하기 전까지 Todo다.
- `AST-01` 실제 스피커 Loop와 TUT-03 실제 Gate 0→3 한 Lap은 계속 수동 미확인이다.
- 다음 기능 카드는 `TUT-04 이전 기록 비교·Best·결과 UI`다.

## 2026-08-26 09:44 — Dataflow·Chaos 그물·맵 파괴 방향 추가

### 확인

- Epic UE 5.8 소개와 Release Notes에서 Dataflow와 Chaos Cloth의 Production-Ready 상태, Dataflow의 Chaos Destruction 비파괴 반복 제작 용도를 확인했다.
- 공식 Cloth Node 문서에서 Max Distance 0 정점은 Kinematic이 되고 별도 `InKinematic` Selection도 사용할 수 있음을 확인했다.
- Chaos Fields 문서에서 Anchor, External/Internal Strain, Force, Sleep/Disable Field가 Geometry Collection의 고정·파괴·정리에 사용됨을 확인했다.
- 현재 UE 5.8.1 설치본에는 필요한 Dataflow/Chaos Cloth/Geometry Collection 플러그인이 있지만 `Drone.uproject`에는 아직 명시적 Cloth/Destruction Plugin을 추가하지 않았다.

### 결정

- 부분 고정 그물은 `Chaos Cloth + Dataflow`, 선택형 맵 파괴는 `Chaos Destruction + Geometry Collection + Dataflow`로 분리한다.
- 그물 고정부는 Weight Map의 Max Distance 0 또는 Kinematic Selection으로 만들고 나머지 영역만 처지게 한다.
- 포획·Crash·Damage·Mission Event는 물리 결과에 직접 종속시키지 않고 프로젝트 C++ Trigger/상태로 결정한다.
- 맵 전체 파괴는 제외하고 얇은 벽·출입구·Jammer 설비부터 한 종류씩 검증한다.
- 현재 기능 순서는 바꾸지 않는다. `TUT-04` 이후 별도 `PHY-DF-00` Sandbox에서 Plugin·Build·회귀를 먼저 검증한다.
- 상세 계획: [`DRONE_CHAOS_DATAFLOW_PLAN.md`](../gameplay/DRONE_CHAOS_DATAFLOW_PLAN.md)

### 현재 변경 경계

- Unreal Plugin 활성화 0
- Cloth/Geometry Collection 생산 자산 0
- C++ 변경 0
- 문서 계획만 추가, Commit·Push는 사용자 수행

## 2026-08-26 09:48 — 별도 `droner` Editor와 대용량 Untracked 에셋 확인

- 계획 검증 종료 시점에 기존 기준 `drone` Editor PID 9884가 종료되고 PID 10960이 `D:\JGY\project\droner\Drone.uproject`를 실행 중인 것을 확인했다.
- Port 8000 MCP Listener도 PID 10960이 소유하므로 현재 MCP 대상은 기준 `drone`이 아니라 `droner`다.
- `droner`는 같은 Git 원격과 `main=origin/main=551e287`을 사용한다.
- `droner/Content/Asset`에는 공급사 14개 폴더와 `_Staging`, 총 10,928개·36,360,181,427 bytes가 Untracked로 존재한다.
- 이 폴더는 전체 제공 소스 복사본이며 프로젝트 선별 이식 규칙을 만족하지 않는다. 일괄 Stage·Commit·Push 금지로 기록한다.
- 기준 `drone`과 `droner`에는 Editor가 추가한 `Config/DefaultEditor.ini` 변경이 있다. 이 작업에서는 되돌리거나 Commit하지 않았다.
- Dataflow/Chaos 구현을 시작할 때는 `droner` Editor를 닫고 기준 `D:\JGY\project\drone`을 연 뒤 별도 Branch에서 진행한다.

## 2026-08-26 11:50 — AST-01C DronePack 드론 시각 자산·정리 맵 이식

### 실제 변경

- `D:\JGY\project\Unreal_260821\DronePack_Project`를 UE 5.8 전용 스테이징에서 감사했다.
- 공급사 전체 기능 Blueprint는 Mannequin 누락, 구형 입력과 `ABP_Quinn_PostProcess` 중복 AnimGraph 오류가 있어 그대로 들여오지 않았다.
- 원본 Demo Map의 Drone Blueprint 6개를 Static Mesh 표시 Actor로 바꾸고, 열화상 Mannequin 3개·도우미 Collision/Camera Proxy·삭제 Actor를 참조하던 Level Blueprint Event Graph를 제거했다.
- 드론 `D_Mesh` 시각 자산과 정리 Map의 폐쇄 의존성만 `/Game/Drone/ThirdParty/DronePack`에 복사했다.
- 최종 이식 수량은 `.uasset` 153개와 `.umap` 1개, 총 154개·82,465,487 bytes다. 기존 파일 덮어쓰기는 0개다.
- 공급사 Pawn·Controller·GameMode·Input·HUD와 중복 FPV 기능 자산은 제외했다. 전역 시작 Map/GameMode와 프로젝트 C++ 공개 API는 변경하지 않았다.

### 검증과 발견

- 스테이징 Map 전이 Game 의존성은 161개이며 외부·누락 의존성 0이다.
- 실제 프로젝트에서 154/154 Package를 UE 5.8로 Resave했다.
- 정리 `Map_Demo` Map Check는 0 errors / 0 warnings다.
- 전체 Blueprint Compile은 0 errors / 0 warnings / 0 failed loads다.
- 처음 전체 자동화를 실행했을 때 Source보다 Editor DLL이 오래되어 12개만 탐색되는 것을 발견했다.
- `-CompilerVersion=14.51.36256`을 하나의 문자열 인자로 전달해 `DroneEditor Win64 Development`를 다시 빌드했다. 첫 호출의 PowerShell 점 구분 오류는 명령 인자 오류였고 소스 컴파일 오류가 아니다.
- 재빌드 DLL 기준 전체 `Drone.` 자동화는 14 succeeded / 0 warnings / 0 failed다. `TrainingLapRecorder`와 `TrainingRecordCalculation`을 포함하며 PIE Lifecycle 새 실행 3/3도 통과했다.
- 이식 154개 모두 Git LFS filter 대상이고 `git lfs fsck`, `git diff --check`가 통과했다. 원본 `/Game/Drone_Pack`, ThirdPerson, Variant 문자열 잔존도 0이다.

### 현재 판정과 다음 작업

- `AST-01C` 기술 이식·자동 검증: 완료
- `AST-01C` 수동 화면 검토: 미확인 — 드론 6종, 환경, 재질, 스케일, 조명과 카메라 구도를 Editor에서 확인해야 함
- 현재 기준 `drone` Editor PID 22936 실행 중. 이미 열린 인스턴스를 프로세스 조회가 놓쳐 추가로 실행된 PID 2764는 `CloseMainWindow`로 정상 종료했고 기존 Editor는 보존함
- Unreal Git: `main=origin/main=551e287`, 기존 `Config/DefaultEditor.ini` 변경과 새 DronePack 154개가 미커밋. 사용자가 Commit하며 Push하지 않음
- 다음 자산 작업: 화면 검토 뒤 선택 Mesh를 프로젝트 소유 Integration BP에 연결
- 다음 기능 작업: 기존 순서대로 `TUT-04` 이전 평균·Best 비교와 결과 UI

## 2026-08-26 12:57 — 사용자 요청 중단 정리

- `UnrealEditor`와 `UnrealEditor-Cmd`를 모두 종료했고 원본·스테이징·Git 변경을 삭제, 되돌림, Commit, Push하지 않았다.
- Course/HUD는 한글 현재 비행값, 최근/평균 구간 통계, Gate 배열 자동 동기화, 200 cm 거리 샘플 곡선 표시까지 코드에 반영됐다. 마지막 폰트 보강 전 Build와 집중 자동화 8/8은 통과했지만 최종 전체 검증과 화면 확인은 남았다.
- 환경 팩은 실제 Drone 저장소에 아직 복사하지 않았다. 스테이징 Battlefield 1,191개/Map 4만 새 경로로 변환됐고, 비호환 Demo Character 102개가 원본 경로에 남았다. MilitaryCamp 668개와 MilitaryBase 1,474개 원본은 보존됐다.
- 재개 순서: 스테이징 재감사 → 세 팩 의존성 정리·변환 → 실제 프로젝트 이식 → Build·BP Compile·Map Check·전체 자동화 → Training Map 저장·한글 HUD/곡선 화면 확인.

## 2026-08-26 13:11 — 중단 작업 재개·NavigationArrows main 병합

- `C:\URproject\drone`에서 기존 main `5540c6b`와 NavigationArrows 기능 Commit `5a052c8`의 분기를 확인했다.
- 기존 main 작업을 유지한 채 `--no-ff` Merge Commit `fb1d7ad`를 만들고 `origin/main`에 Push했다.
- 병합 main Build 성공.
- `Drone.Integration.NavigationArrowsAsset` 1/1 Success.
- 전체 `Drone.` 15/15 Success.
- Blueprint Compile 0 errors, 0 Blueprint warnings, 0 failed loads.
- NavigationArrows LFS 속성과 `git lfs fsck` 통과.
- 최종 `main=origin/main=fb1d7ad`, Drone 작업 트리 Clean.
- 실제 Training HUD Host/Wrapper와 PIE/Standalone 시각 확인은 구현하지 않았으므로 완료로 기록하지 않는다.

## 2026-08-26 13:21 — TUT-04A PIE 초기 화면 확인

- 정확한 `C:\URproject\drone\Drone.uproject`를 UE 5.8.1로 열고 `Lvl_DroneTraining`을 PIE 실행했다.
- 화면 좌측 상단에서 한글 `드론 비행 정보`, 현재 속도·고도·수직 속도·진행 방향이 정상 표시됐다.
- 화면 좌측 하단에서 한글 `코스 구간 기록`과 최근·완료 구간 속도/거리/시간 자리표시자가 정상 표시됐다.
- 현재 Gate Ring, 뒤쪽 Gate들, 세분화된 발광 코스 선이 뷰포트에 표시됐다.
- 공급사 NavigationArrows Host/Wrapper는 아직 미구현이므로 별도 화살표 Widget은 표시되지 않았다.
- 자동 UI의 짧은 키 입력으로는 지속 전진이 되지 않아 Gate 0→3 한 Lap과 구간 숫자 갱신은 확인하지 못했다.
- PIE와 Editor를 정상 종료했다. 13:21 KST Unreal 프로세스 0, Drone 작업 트리 Clean이다.

## 2026-08-26 16:55 — 맵 이식 상태 재확인

- 실제 저장소의 ThirdParty `.umap`은 `Content/Drone/ThirdParty/DronePack/Map/Map_Demo.umap` 1개다.
- 이 맵은 Commit `5540c6b`로 main에 포함됐고 Git LFS 대상이다.
- 기존 AST-01C 결과인 외부 Game·누락 의존성 0, Map Check 0/0, Blueprint 0/0/0과 LFS 검증을 현재 기술 완료 근거로 유지한다.
- `Map_Demo`에서 드론 6종·재질·스케일·조명을 직접 보는 최종 시각 검토는 아직 하지 않았다.
- Battlefield·MilitaryCamp·MilitaryBase 이름의 `.umap`은 현재 Drone 저장소에 0개다. Battlefield 스테이징 변환과 세 팩 실제 이식·대표 맵 검증은 `AST-03A` Doing으로 남긴다.
- `Lvl_DroneTraining`은 외부 맵 이식 결과가 아니라 프로젝트 소유 Tutorial Map이다.

## 2026-08-26 — RabbitHole 참고·맵 중앙화·템플릿 콘텐츠 정리

### 참고 구조와 결정

- 실제 최신 RabbitHole 프로젝트 `C:\project\Fractured\GoDownTheRabbitHole.uproject`의 Content와 Config를 확인했다.
- RabbitHole은 프로젝트 소유 맵을 `Content/Maps`에 모으고 Blueprint를 AI·GameMode·PlayerManager·Widget 등 역할별 폴더로 나눈다. 공급사 맵은 공급사 폴더에 유지한다.
- Drone에는 프로젝트에서 실제 사용하는 맵만 `/Game/Drone/Maps`에 모으는 규칙을 적용했다. 공급사 Mesh·Material 등 의존 자산은 ThirdParty 경계를 유지한다.

### 실제 변경

- `/Game/Drone/Tutorial/Maps/Lvl_DroneTraining` → `/Game/Drone/Maps/Lvl_DroneTraining`
- `/Game/Drone/Prototype/Maps/Lvl_DronePrototype` → `/Game/Drone/Maps/Lvl_DronePrototype`
- `/Game/Drone/ThirdParty/DronePack/Map/Map_Demo` → `/Game/Drone/Maps/Lvl_DronePackShowcase`
- Showcase BuiltData도 같은 중앙 맵 폴더로 이동했다.
- `/Game/ThirdPerson`, `/Game/Variant_Combat`, `/Game/Variant_Platforming`, `/Game/Variant_SideScrolling`과 대응 ExternalActors/ExternalObjects를 제거했다.
- `DefaultEngine.ini`, `DefaultEditor.ini`, Editor Content Browser 기본 경로와 자동화 테스트의 맵 경로를 새 기준으로 갱신했다.
- 기본 실행·Editor 시작 맵은 `Lvl_DroneTraining`, 전역 GameMode는 프로젝트 소유 `BP_DronePrototypeGameMode`다.
- C++ `DroneCharacter`, 기존 GameMode/Controller와 Variant Source는 Source/Build.cs 별도 감사가 필요해 보존했다.
- Git 감지 기준 변경 규모는 599개 경로, 삭제 589개, 이름·위치 변경 2개, 새 경로 추가 2개다. 삭제 파일은 Git 이력에서 복구할 수 있다.

### 감사와 검증

- 삭제 전 프로젝트 맵 3개의 네 Template Root 의존성 0, `/Game/Drone` 자산의 외부 참조 0을 확인했다.
- 중앙 맵 3개와 Showcase BuiltData 로드 성공.
- 이전 맵 경로와 제거 대상 Template Root 자산 0.
- `DroneEditor Win64 Development` Build 성공.
- Blueprint Compile `0 errors / 0 warnings / 0 failed loads`.
- 전체 `Drone.` 자동화 `15/15` 성공.
- 중앙 맵 4개 LFS 속성, `git lfs fsck`, `git diff --check` 통과.

### Git과 남은 확인

- 기능 Commit: `1c8f391 chore: centralize drone maps and remove templates`
- main Merge Commit: `2cc5d79 merge: centralize drone maps and remove templates`
- 기능 Branch와 `origin/main` Push 완료. 최종 `main=origin/main=2cc5d79`, Drone 작업 트리 Clean.
- 프로젝트 맵 중앙화와 템플릿 콘텐츠 정리는 완료다.
- `Lvl_DronePackShowcase`의 드론 6종·재질·스케일·조명 시각 검토와 `Lvl_DroneTraining` 한 Lap 수동 비행은 아직이다.
- Battlefield·MilitaryCamp·MilitaryBase 환경 맵은 여전히 미이식이다.
- 현재 폴더 규칙: [`DRONE_CONTENT_FOLDER_GUIDE.md`](../assets/DRONE_CONTENT_FOLDER_GUIDE.md)

## 2026-08-26 19:35 — 삭제 범위 교정·환경 맵 3종 실제 이식

### 삭제 범위 교정

- 사용자가 삭제를 허용한 대상은 Unreal 프로젝트 생성 때 포함된 기본 Map이었다. Content Root 전체 삭제로 해석한 것은 범위가 넓었다.
- `fb1d7ad`에서 비맵 자산 62개를 복구해 `909f6a3 fix: restore template assets while keeping starter maps removed`로 분리했다.
- 복구 후 Asset Registry 수는 ThirdPerson 4, Variant_Combat 30, Variant_Platforming 10, Variant_SideScrolling 18이다.
- 삭제 상태를 유지한 것은 `Lvl_ThirdPerson`, `Lvl_Combat`, `Lvl_Platforming`, `Lvl_SideScrolling`과 각 Map 전용 ExternalActors/ExternalObjects뿐이다.

### 스테이징과 선택

- 원본 `C:\에셋`은 수정하지 않고 `C:\에셋\_Staging\EnvironmentStage`에서 3팩 3,334개·18.76 GiB와 Map 10개를 감사했다.
- 대표 Map은 Battlefield `PL_Battlefield`, MilitaryCamp `Map_MilitaryCamp`, MilitaryBase `MilitaryBase`로 선정했다.
- 프로젝트 중앙 사본은 `/Game/Drone/Maps/Lvl_Battlefield`, `Lvl_MilitaryCamp`, `Lvl_MilitaryBase`다. 세 Map의 공급사 GameMode Override는 제거해 프로젝트 기본 GameMode를 상속한다.
- 대형 팩 내부 경로 수천 개를 강제로 재작성하지 않고 검증된 정확한 의존성만 공급사 Root 그대로 보존했다.

### 호환 보강과 이식 규모

- Battlefield의 Manny/Quinn 구 경로 2개는 팩 내부 실제 Mesh로 정확 경로 호환 사본을 만들었다.
- MilitaryCamp의 누락 직접 Map 참조 `Map_MilitaryCampValley3`는 현재 공급 `Map_RockyGrassland`의 호환 사본으로 닫았다.
- MilitaryBase의 Grass Preview Mesh 경로와 Glow Material 기본 Texture Override를 정리하고, 외부 RacingTrack Blueprint를 끌던 TireTrack 데모 Actor 6개를 중앙 Map 사본에서 제거했다. `/Game/Textures/T_Linear_Grad` 호환 Texture도 로컬 자산에서 만들었다.
- 최종 이식은 2,723개·18,211,844,112 bytes(16.96 GiB): Battlefield 710, MilitaryCamp 593, MilitaryBase 1,414, 중앙 Map 3, 호환 3이다.
- Battlefield Map Check에서 완전히 빈 독립 StaticMeshActor 1개를 중앙 Map에서 제거했다. 건물 Blueprint 14개는 일부 선택적 컴포넌트만 비어 있고 다른 실제 Mesh가 정상 연결되어 있어 삭제하지 않았다.

### 최종 검증

- `DroneEditor Win64 Development` Build 성공. 처음 지정한 미설치 MSVC 14.51.36256 호출은 컴파일 전 실패했고, 실제 설치 14.51.36231로 다시 실행해 성공했다.
- 전체 Blueprint Compile: `0 errors / 0 warnings / 0 failed loads`. 별도 자산 로그에는 Battlefield Manny/Quinn Pose GUID 경고 28건과 MCP EULA 안내 1건이 있다.
- 전체 `Drone.` Automation: 15/15 성공. 14개 무경고, 기존 `PIEInputLifecycle`의 RecastNavMesh 미발견 경고 포함 성공 1개다.
- Map Check: Battlefield 오류 0·공급 Blueprint NULL StaticMesh 메시지 14건, MilitaryCamp 0/0, MilitaryBase 0/0.
- 환경별 Game 의존성 누락 0, 허용 외 경로 0, 중앙 Map World Load와 GameMode None 확인.
- 신규 2,723개 전부 3줄 Git LFS Pointer, `git diff --check`, `git lfs fsck` 통과.
- 환경 이식 Commit: `f8c8fb2 feat: migrate validated environment maps`.

### 남은 사람 확인

- UE 5.8.1 Editor에서 환경 Map 3개를 각각 열어 조명·재질·스케일·Landscape·Collision과 드론 Spawn 위치를 눈으로 확인한다.
- 세 맵 중 어느 것을 데모 주력 Map으로 쓸지는 현재 미정이며, 기술 이식 완료를 최종 채택으로 표현하지 않는다.
## 2026-09-11 17:13 — CourseSpline과 분리된 Ring별 Handle 직접 편집

- 첫 구현의 `Spline Point 1개=Ring 1개`는 Ring 이동이 코스 곡선까지 바꾸므로 사용자 요구와 다름을 확인하고 폐기했다.
- `ADroneTrainingCourse`에 CourseSpline과 분리된 `Ring별 Spline Handle` 배열을 추가했다. `MakeEditWidget` 3D 점을 움직이면 가장 가까운 Spline 위치로 투영되고 Ring만 해당 위치·접선 회전을 따른다.
- Handle 배열 항목 수가 Ring 수이며 추가·삭제가 Ring·Sequence 수에 반영된다. 현재 숫자/수동 배치에서 Handle을 초기화하는 Editor 버튼과 전체 Handle을 다시 Spline에 붙이는 버튼도 추가했다.
- 자동화에 Handle Spline 투영, 추가·삭제, Ring·Sequence 수 변경과 CourseSpline 제어점 수·위치 불변 검사를 추가했다.
- Unreal Editor가 없는 상태에서 MSVC 14.51.36257 `DroneEditor Win64 Development` 최종 Build 성공, 최종 `Drone.Tutorial.TrainingCourse` 1/1 성공(0 warning/0 error), `git diff --check`와 `git lfs fsck` 통과.
- 작업 중 `3df654a`에 이어 사용자 `0911임시버전` 커밋 `46efd2e`까지 동기화됐다. 기존 자동 Ring/Gate 색상 Source·테스트·도구와 기관총 자산 10개는 이 커밋에 추적됐고 독립 Handle 변경 3개는 로컬에 보존됐다.
- 최종 감사 중 팀원 Training Map 후속 `55d6c61`과 Merge `9de1ead`가 추가되어 Fast-forward했다. 코드 충돌은 없었고 최신 Map에서도 Gate 17/Sequence 4, 역할 표적/Carryable 0 상태가 동일함을 `TrainingAssets`로 다시 확인했다.
- 최신 `Lvl_DroneTraining`은 원격과 같은 Clean 상태로 보존했다. 읽기 전용 감사와 `TrainingAssets` 재실행에서 Gate Actor 17개·Course Sequence 4개·역할 표적/Carryable 0개를 확인했다. 화면에서 실제 코스 Gate 범위와 순서를 확인한 뒤 독립 Handle 모드를 맵에 적용한다.
- Commit·Push하지 않았다.

## 2026-09-15 — 진행 상태와 차후 목록 재정리

- `git status -sb`와 마지막 Commit을 다시 확인했다. 확인 시작 시 Unreal은 `10da7ce`, 문서는 `27d002d`이고 각각 로컬 `origin/main`과 같으며 작업 트리는 Clean이었다.
- 2026-09-15 실시간 `git fetch origin --prune`은 두 저장소 모두 DNS 오류(`Could not resolve host: github.com`)로 실패했다. 따라서 GitHub 서버에 추가 Commit이 없는지는 네트워크 복구 후 다시 확인한다.
- 독립 Ring Handle Source/Test 3개는 Unreal `10da7ce`에, 직전 문서 갱신은 `27d002d`에 반영돼 더 이상 미커밋 대상이 아니다.
- UE 5.8 Editor가 `D:\JGY\project\drone\Drone.uproject`로 실행 중임을 확인했다. C++ 변경이나 전체 Build 전에는 저장 후 종료한다.
- 최종 Handle 보고서 `IndependentRingHandles_Final_20260911`은 `Drone.Tutorial.TrainingCourse` 1/1 성공, 0 warning/0 error다. 최신 Map 감사 `TrainingAssets_9de1ead`는 1/1 실패·8 errors이며 Gate Actor 17개/Sequence 4개, 역할 표적 3종과 Carryable 0개가 원인이다.
- 현재 알려진 실패 테스트는 `TrainingAssets`, `TrainingPIESmoke`, `NPCPerceptionSearchPIE` 3개이며 전체 자동화 Pass로 표시하지 않는다.
- 다음 순서를 `Training Map 링 범위·순서 확정 → 독립 Handle 배치와 역할 표적/Carryable 복원 → 한 Lap·두 Lap HUD 수동 확인 → 실패 3개 수정과 전체 회귀 → Mission 목표 Rule 데이터화 → Jamming → 수동 회귀 묶음 → Dataflow/Chaos Spike`로 정리했다.
- 코드와 Map은 이번 정리에서 변경하지 않았다. `CONTEXT.md`, `STATUS.md`, `WORKBOARD.md`, 이 Worklog만 최신화했으며 Commit·Push는 사용자가 진행한다.

## 2026-09-15 — Training 보존과 TestMap 분리 결정

- 사용자 결정으로 `/Game/Drone/Maps/Lvl_DroneTraining`은 현재 상태를 유지하고 기능 시험 중 직접 저장하거나 덮어쓰지 않는다.
- 목표 폴더는 `/Game/Drone/Maps/TestMap`이다. `Lvl_DroneTraining_Test` 사본에서 Ring·역할 표적·HUD·Mission 기능을 검증한 뒤 사용자 승인된 변경만 원본 Training에 반영한다.
- 이동 확정 후보는 `Lvl_DronePrototype`, `Lvl_NPCSmartObjectGreybox`, `Lvl_DronePackShowcase`, `Lvl_MilitaryBase_Test`다. `test1`, `test2`는 팀원 수정 이력과 용도를 먼저 확인하고 의미 있는 이름으로 바꿔 이동한다.
- 파일 탐색기 이동은 금지한다. Unreal AssetTools로 Move/Rename하고 C++ 테스트·Migration Tool·Soft Reference를 갱신한 뒤 Redirector, Map Load, Map Check, Blueprint Compile, 전체 자동화와 LFS를 검증한다.
- 이번 기록에서는 Unreal 자산을 이동·복제하지 않았다. Editor가 실행 중이고 사용자 표현이 `그거 다 하고나면`이므로 `MAP-TEST-01` 후속 카드로 등록했으며 현재 Training Map은 건드리지 않았다.

## 2026-09-15 — 팀원 Training Map과 기능 시험 완전 분리

- 사용자가 `Lvl_DroneTraining`에서 팀원이 실제 Tutorial 환경을 제작 중이고 Map 분할도 어렵다고 확인했다.
- 기존 `Lvl_DroneTraining_Test` 전체 복제 계획은 폐기했다. 374.94MiB Training Map과 Environment·Landscape를 복사하지 않고 `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest`를 빈 경량 맵으로 새로 만든다.
- 경량 맵에는 기본 바닥, PlayerStart, Prototype GameMode, Course/Gate, 역할 표적, Carryable, HUD 검증에 필요한 Actor만 둔다. 실제 코스 배치나 환경 제작은 포함하지 않는다.
- TestMap에서 통과한 C++/Blueprint/Data Asset과 배치 가이드를 Training 담당자에게 전달한다. 실제 Training Map의 저장·자동 배치·분할·덮어쓰기는 담당자와 통합 시점을 정하기 전 금지한다.
- `TrainingAssets`와 `TrainingPIESmoke`는 실제 맵 중간 상태를 보여주는 Production 감사로 남긴다. 개발용 TestMap 검사를 별도로 추가해 원본 검사를 억지로 녹색으로 만들지 않는다.

## 2026-09-15 — 외부 엔지니어링 참고 5종 검토·팀 규칙 반영

- Ponytail, ECC, Archify, fmt, Matt Pocock Skills의 기본 브랜치 README와 License를 검토했다. CLI의 GitHub DNS 조회가 실패해 특정 Commit SHA는 고정하지 못했으며 실제 도입 전 Version/Commit을 다시 고정한다.
- Ponytail의 최소 의존성 판단 순서, ECC의 계획→테스트→구현→검토→검증→기록 Loop, Archify의 근거 기반 Workflow/Sequence 표현, Matt Pocock Skills의 공유 용어·ADR·TDD·원인 우선 진단을 Drone Playbook으로 재작성했다.
- `Source/Drone` 감사에서 fmt Include/Namespace 사용이 없음을 확인했다. Runtime UI는 `FText`, 내부 문자열과 로그는 Unreal 기본 체계를 사용하므로 fmt를 새 의존성으로 추가하지 않는다.
- ECC와 Ponytail은 Hook/Skill 범위가 겹치므로 동시에 설치하지 않는다. Archify와 Matt Pocock Skills도 현 단계에는 설치하지 않는다. 새 Plugin/Hook/Library/Node Package, Codex 전역 설정, `Drone.Build.cs` 변경은 0이다.
- 공유용 폴더 [`EXTERNAL_ENGINEERING_REFERENCES`](../reference/external-engineering/README.md)에 저장소별 Review, 팀 Playbook, 격리 도입 계획을 추가하고 `DOC-EXT-01`을 Done 처리했다. `AI-TOOL-REVIEW-01`은 TestMap Vertical Slice 이후로 등록했다.
- 기능 우선순위는 바꾸지 않는다. 바로 다음은 팀원 Training을 건드리지 않는 경량 `Lvl_DroneTutorialSystemsTest` 생성과 TestMap 전용 검증이다.

## 2026-09-15 — 경량 Tutorial Systems Test Map 생성·검증

- 작업 시작 시 Unreal은 `main=origin/main=10da7ce` Clean이고 UE Editor 프로세스가 없음을 확인했다. 팀원 `/Game/Drone/Maps/Lvl_DroneTraining`은 Git 변경 0으로 유지했다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest`를 284,865 bytes로 새로 만들었다. 대형 Environment/Landscape를 복사하지 않고 기본 Cube 바닥, PlayerStart, Directional/Sky Light, Prototype GameMode만 사용했다.
- `BP_DroneTrainingCourse`에 여섯 점의 곡선 Spline과 100cm 표시 Segment, CourseSpline과 분리된 독립 Ring Handle 5개를 구성했다. `BP_DroneTrainingGate` 생성 Ring 5개와 Sequence 5개가 일치한다.
- Recon/Impact/Payload 역할 표적 BP를 각 1개, `BP_DroneCarryablePayload`를 1개 배치했다. 최종 위치·크기·가시성은 Editor 수동 확인 전이므로 기술 배치 완료와 화면 완료를 구분한다.
- `BuildDroneTutorialSystemsTestMap.py`를 추가했다. 기존 맵에서는 기본 Validate-only이고 환경 변수와 PowerShell `Rebuild`를 명시한 경우에만 `DroneTutorialSystemsTest.Owned` Tag Actor를 다시 만든다.
- 첫 생성 실행은 UE Python에 노출되지 않은 `rerun_construction_scripts` 호출에서 중단됐다. 빈 TestMap만 저장된 상태를 확인하고, 이미 재구성을 수행하는 공개 Course API와 중복된 호출을 제거한 뒤 명시적 Rebuild로 정상 완성했다. 이 실패를 성공으로 숨기지 않았으며 후속 Wrapper에는 `-ScriptErrorsAreFatal`과 로그 검사 조건을 넣었다.
- `Invoke-DroneTutorialSystemsTestMap.ps1 -Mode Validate`는 별도 UserDir/Log로 성공했다. 명시적 Map Check 결과 0 errors/0 warnings, `DRONE_TUTORIAL_TESTMAP|VALIDATION_OK`는 rings=5/targets=3/carryable=1이다.
- 새 `Drone.Tutorial.TutorialSystemsTestMap` 자동화는 저장 Map을 새 프로세스에서 로드해 PlayerStart 1, 선배치 Drone 0, Course 1, Role Target 각 1, Carryable 1, Ring/Sequence 5, 독립 Handle 모드, Prototype GameMode, Legacy Actor 0을 검사했고 1/1 Success다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build는 성공했다. 첫 Build 호출의 CompilerVersion 분리는 PowerShell 인자 오류였고 하나의 문자열 인자로 다시 실행해 해결했으며 C++ 컴파일 오류가 아니었다.
- `.gitattributes`는 파일 크기와 무관하게 모든 `.uasset`·`.umap`을 LFS 대상으로 둔다. 새 TestMap은 `filter=lfs diff=lfs merge=lfs`, C++·Python·Markdown은 일반 Git이다.
- 현재 Unreal 변경은 새 TestMap 1개, 자동화 C++ 1개, 생성 Python 1개, 검증 PowerShell 1개다. Commit·Push하지 않았다. 다음은 Editor에서 곡선 안내선, Ring 3상태 색, 역할 표적, Carryable, HUD와 한/두 Lap을 직접 확인하는 것이다.

## 2026-09-15 — Git LFS 용량 원인 감사와 비파괴 절감 계획

- 현재 `.gitattributes`가 크기와 무관하게 모든 `.uasset`·`.umap`을 LFS로 처리하고, `lfs.fetchinclude`·`lfs.fetchexclude` 별도 설정은 없음을 확인했다.
- 사람이 읽는 LFS 크기 표시는 반올림되므로 `git lfs ls-files --json`의 정확한 Byte로 재집계했다. 현재 Commit은 LFS 5,550개·약 27.66GiB다. 1MiB 미만은 3,602개·0.45GiB(1.6%)이고, 10~100MiB 942개가 21.34GiB(77.2%)다.
- 70MiB Threshold를 가정하면 5,538개·25.67GiB가 일반 Git으로 이동하고 LFS에는 12개·1.99GiB만 남는다. 100MiB Push 차단까지 여유는 생기지만 일반 Git 저장소·Binary 이력·Clone 부담이 커지므로 용량 해결책으로 채택하지 않았다.
- 전체 로컬 Ref의 고유 LFS Object는 6,137개·약 29.62GiB다. 현재 Commit보다 약 1.96GiB만 크므로 현재는 오래된 이력보다 Checkout에 포함된 Asset 범위가 주원인이다.
- 프로젝트 소유 `Content/Drone` 중 ThirdParty 제외 범위 0.89GiB, `Content/Drone/ThirdParty` 4.61GiB, `Content/Drone` 밖 Vendor Root 22.16GiB로 집계됐다. 큰 감사 후보는 `MillitaryBase` 7.67GiB, `FC_MilitaryCamp` 6.20GiB, `STF` 3.04GiB, `Battlefield` 2.71GiB다.
- LFS는 변경된 Package의 새 전체 Object를 저장하므로 374.94MiB Training Map과 약 206MiB MilitaryBase Map의 반복 저장을 줄인다. 팀원 Training을 보존하고 284,865-byte 경량 TestMap을 만든 현재 분리는 그대로 유지한다.
- `.gitattributes`, Unreal Asset, Git 이력과 원격은 변경하지 않았다. 먼저 대표 Map별 Dependency Closure와 Demo/중복/Source 후보를 감사하고 Core/선택형 Asset Depot를 분리한다. 선택 Clone은 LFS Pointer를 Content에 남겨 Editor 오류를 만들지 않도록 별도 Clone에서 Sparse Checkout과 `GIT_LFS_SKIP_SMUDGE`, 경로별 LFS Fetch를 함께 검증한다.
- 원격 LFS Object는 현재 Branch에서 파일을 지워도 GitHub 저장 할당량에 남는다. 원격 저장량 초기화가 필요하면 Curated 새 저장소 또는 백업 후 재생성·Support 협의를 팀이 별도로 결정하며 자동 실행하지 않는다.
- 상세 수치와 실행 순서는 [`DRONE_GIT_LFS_CAPACITY_PLAN.md`](../git/DRONE_GIT_LFS_CAPACITY_PLAN.md)에 기록했다. 후속 카드는 `GIT-LFS-CAP-01`이다.
- GitHub 공식 2026-09-15 단가와 Free/Pro 각 10GiB 포함량으로 비용을 추정했다. 원격 Associated Storage를 로컬 고유 Object 29.62GiB로 가정하면 저장 약 `$1.37/월`, 현재 전체 Clone 1회가 있는 달 약 `$2.92`, 2회가 있는 달 약 `$5.34`다. `$5`는 두 달 선불 잔액이 아니라 월 Budget으로 운영하고 실제 Billing 값을 최종 기준으로 삼는다.

## 2026-09-15 — 유인 MG 교대 안정화·Smart Object 팀 가이드·최소 Skill 도입

- AI 시험 맵에는 기관총 계열 Actor가 3개 있지만 NPC가 Claim하는 대상은 Smart Object Definition이 있는 `BP_SO_MGTurret` 1개뿐임을 테스트 계약에 반영했다. `BP_AutoTurret_Vehicle`과 `BP_AutoTurret_Emplaced`는 차량형/설치형 무인 자동포탑이며 유인 MG 수량·피해량·교대 판정에서 제외한다.
- 유인 MG 사수 사망 시 생존 가능한 적이 즉시 한 번만 이벤트를 받고 끝나던 경로를 0.75초 간격·15초 창 재할당 재시도로 보강했다. 사망·UnPossess·Drone Lost/Destroyed·MG 점유 성공 시 재시도를 정리하며 공개 런타임 API는 바꾸지 않았다.
- `Move To Reserved MG Turret` StateTree Task에 진행 거리 감시, 2초 정체 판정, 1회 재경로, 250cm Greybox 조작 위치 Snap 반경을 추가했다. 이동 상태가 `Moving`이어도 반경 안이면 먼저 정확한 Operator Anchor/Rotation으로 정렬해 점유를 완료한다. 최종 Mesh·Collision 적용 시 Snap 반경은 StateTree Details에서 줄인다.
- 테스트는 Rifle 10, Shotgun Pellet 8, 유인 MG 8의 기본 피해 계약을 먼저 검증한 뒤 이 PIE 안에서만 피해를 0으로 내려 Drone 조기 사망이 상태 검증을 가리지 않게 했다. Cover는 Nav 실패 시 제자리 `DroneDetected` 사격 Fallback도 정상 계약으로 인정한다. 게임/BP 기본 피해값은 바꾸지 않았다.
- `DroneEditor Win64 Development` Build가 성공했다. `Drone.AI.NPCPerceptionSearchPIE`는 단독 새 PIE 3회 연속 성공했고, 후속 `Drone.AI.NPC` 묶음에서도 해당 항목이 성공했다. 같은 묶음의 종료 코드 255는 별개 `NPCBaseRoutinesPIE`에서 느린 Headless 실행 중 적 한 명이 35초 안에 두 번째 순찰을 끝내지 못한 간헐 실패이며 MG 실패로 기록하지 않는다.
- 팀 공유용 [`DRONE_SMART_OBJECT_ROUTE_EDITING_GUIDE.md`](../ai/DRONE_SMART_OBJECT_ROUTE_EDITING_GUIDE.md)를 추가했다. 현재 동선은 스플라인/번호 고정 순서가 아니라 태그가 맞는 최근접 빈 Slot 선택임을 명시하고, 맵 경계, BP 경로, 지점 이동·회전·복제, Cyan 방향, NavMesh, Offset/StateTree 조정, 검증과 문제 해결 절차를 정리했다.
- 외부 참고 저장소는 Project Plugin/Hook/Library로 추가하지 않았다. 개인 Codex 환경에는 반복되는 원인 진단과 테스트 우선 작업에 직접 필요한 Matt Pocock Skills의 `diagnosing-bugs`, `tdd`만 설치했으며 다음 Codex 작업부터 사용 가능하다. Ponytail/ECC/Archify/fmt는 현재 Unreal 기본 도구와 문서 체계에 비해 중복·도입 부담이 커 보류한다.
- 팀원 Production `/Game/Drone/Maps/Lvl_DroneTraining`은 Git 변경 0으로 유지했다. Editor와 명령줄 검사 프로세스는 종료 상태이며 Commit·Push하지 않았다.
- 최종 경량 맵 재검증 `Resume_TutorialSystemsTestMap_Final_20260915_113347.log`에서 `Drone.Tutorial.TutorialSystemsTestMap` 1/1 Success·Exit 0을 확인했다. Unreal/문서 `git diff --check`와 Unreal `git lfs fsck`도 통과했으며 출력된 LF→CRLF 문구는 작업 트리 줄바꿈 안내이지 오류가 아니다.

## 2026-09-15 — 추천자료 장기 계획과 깨지는 World Text 정리

- PBRT, OSTEP, Crafting Interpreters, Game Programming Patterns, Computer Networking 9판 강좌, Speech and Language Processing 3판 Draft, Deep Learning, Immersive Linear Algebra의 공식 공개 페이지와 목차를 확인했다.
- [`CS_GAMEDEV_READING_PLAN.md`](../learning/CS_GAMEDEV_READING_PLAN.md)를 추가했다. 현재 Drone 작업에 가까운 `Game Programming Patterns + Immersive Linear Algebra`부터 시작하고 OS·Interpreter·그래픽스·네트워크·AI/NLP로 확장하는 장기 순서, 주 2시간/바쁜 주 25분 운영, 30분 세션 기록, 첫 4주 실행표를 포함한다. 비공식 PDF 다운로드와 원문 파일의 Git Commit은 권장하지 않는다.
- TestMap 역할 표적 위의 긴 한글 `TextRender`가 깨진다는 사용자 화면 피드백을 재현하는 검사를 먼저 추가했다. 수정 전 저장 TestMap에서 Recon/Impact/Payload 3개와 활성 Carryable 1개의 World Text가 모두 Visible이라 전용 테스트가 `3`과 `1`로 실패했다.
- 역할 표적은 `bShowInstructionText`, Carryable은 `bShowPickupLabel`을 기본 `false`로 추가하고 실제 Refresh/활성화/재투하 뒤에도 이 값을 적용했다. BP에서 명시적으로 켤 수는 있지만 문구는 `SCAN`·`IMPACT`·`DROP`·`PICKUP`으로 짧게 바꿨다. Mission HUD의 한글 조작 안내와 표적 기능 판정은 변경하지 않았다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build가 성공했고 동일 `Drone.Tutorial.TutorialSystemsTestMap` 검사는 visible 0+0, 1/1 Success, Exit 0으로 전환됐다. Production `Lvl_DroneTraining`은 변경하지 않았고 Commit·Push하지 않았다.

## 2026-09-15 — Markdown 문서 구조 정리

- 루트 문서가 모두 장문이고 `STATUS`·`WORKBOARD`·`CONTEXT`·세부 계획에 같은 상태가 반복돼 현재와 과거를 구분하기 어려운 문제를 정리했다.
- 기존 루트 원문 4개는 삭제하지 않고 `docs/history/snapshots/2026-09-15`에 보존했다. 새 루트 `README.md`는 시작점, `STATUS.md`는 현재 사실, `WORKBOARD.md`는 지금/다음 작업, `CONTEXT.md`는 변경 금지 경계만 담당한다.
- 상세 문서를 `planning`, `tutorial`, `ai`, `gameplay`, `assets`, `git`, `learning`, `reference`, `history`로 분류하고 [`docs/README.md`](../README.md)를 단일 안내 페이지로 추가했다.
- 이동된 문서의 상대 링크를 새 위치에 맞게 일괄 보정했다. 전체 Markdown 51개를 검사한 결과 존재하지 않는 로컬 `.md` 링크는 0개다.
- Unreal 저장소와 Asset은 변경하지 않았다. 문서 이동·요약·링크 수정만 문서 저장소의 로컬 변경으로 남기며 Commit과 Push는 사용자가 처리한다.
- 이후 진행 보고는 새 Markdown 파일을 늘리지 않고 루트 `STATUS.md`, `WORKBOARD.md`와 이 Worklog에 갱신한다. 완료된 일회성 보고서만 `history`로 옮긴다.

## 2026-09-15 — 이 PC 최신 빌드·Mission 목표 Rule Vertical Slice 준비

- 원격 재조회 때 Unreal `8b9b2a8`, 문서 `3e89e43`의 `main=origin/main`을 확인했고 두 저장소에 Stash는 없었다. 이후 작업은 로컬 수정으로만 남기고 Commit·Push하지 않았다.
- 첫 비파괴 TestMap Validate는 `RoleTest_PayloadTarget`이 없다는 메시지로 실패했다. 로그에는 역할 표적 Blueprint가 `/Script/Drone` C++ 부모를 못 읽는 경고가 있었고, 로컬 `UnrealEditor-Drone.dll`은 9월 8일 빌드라 최신 Source보다 오래됐다. 맵을 재구성하지 않고 최신 `DroneEditor`로 재빌드한 뒤 같은 Validate가 `rings=5/targets=3/carryable=1`, Map Check 오류·경고 0으로 성공했다.
- `FDroneMissionObjectiveRule`에 목표 ID·설명·사건 종류·필요 수량·제한 시간·Actor Tag 대상 ID를 추가했다. 새 Rule 배열이 비어 있으면 기존 `InitialObjectives` 문구형 1회 목표를 사용하므로 레거시 Data Asset을 깨지 않는다. ID 중복·0 수량·음수/비정상 시간 값을 거부한다.
- Director는 현재 Rule과 일치하는 Scan 완료, 의도된 Payload 적중, 맵 시작 시점 Health 대상 사망, Training Lap, 명시적 Return Event만 진행한다. 같은 Actor는 목표당 한 번만 세고, 목표별 제한 시간은 Tick 대신 TimerManager로 만료 시 Failure를 보고하며 전환·종료에 정리한다. 목표 Event·TargetId·수량·제한값이 Snapshot으로 HUD에 전달된다.
- Blueprint 배치형 `DroneMissionReturnZone` Box Trigger를 추가했다. 플레이어가 실제 출격한 Drone의 Overlap만 Director에 Return Event로 보고한다. 최종 기지 위치·크기는 미정이므로 Production 맵과 TestMap 어디에도 자동 배치하지 않았다.
- `ConfigureDroneTutorialMissionObjectiveRule.py`는 저장 `DA_Mission_Tutorial_Training`의 Mission ID와 기존 목표가 정확히 하나인지 확인한 뒤 같은 문구를 `Objective.TrainingLap` Rule로 이행했다. `DRONE_MISSION_RULE|SAVED`를 확인했고 해당 `.uasset`은 Git LFS 대상이다. 팀원 `/Game/Drone/Maps/Lvl_DroneTraining` `.umap`은 변경하지 않았다.
- MSVC 14.51.36256 `DroneEditor Win64 Development` 두 번 모두 Build 성공. 새 `Drone.Mission.ObjectiveRules`는 잘못된 Event/Tag, Actor 중복, 두 Scan→Delivery→Return→Success, 종료 후 Event 거부와 귀환 Zone 기본 Box 계약을 검증한다. 최종 회귀에서 이 테스트와 `Drone.Flow.Contract`, `MissionEntryContract`, `TrainingGateSequence`, `TutorialSystemsTestMap`이 5/5 Success·Exit 0이었다.
- 실제 역할 기능의 연쇄 PIE, 귀환 Zone의 맵 배치·Overlap, 제한 시간 만료 화면과 TestMap/AI 수동 화면 검증은 미완료다. 새 Data Asset/맵의 최종 목표 규칙을 임의로 확정하지 않는다. 설정과 문제 확인법은 [`DRONE_MISSION_OBJECTIVE_RULE_GUIDE.md`](../gameplay/DRONE_MISSION_OBJECTIVE_RULE_GUIDE.md)에 기록했다.
- 최종 로컬 Unreal·문서 `git diff --check`는 모두 종료 코드 0이다. 표출된 LF→CRLF 메시지는 줄바꿈 안내다. Unreal·문서 저장소의 HEAD는 각 `origin/main`과 같지만 작업 트리는 새 Source/Data Asset/가이드가 미커밋으로 남았다.

## 2026-09-16 — 재밍 신호 Greybox·Mission 사건 연결

- 로컬 기획의 첫 Story Mission은 구급품 전달·정찰·재밍 회피·적 기지 침투 후보로 확인했다. Figma 링크는 현재 읽기 연결이 없어서 실제 화면/최종 목표는 확인하지 못했다. Figma 연결 옵션을 제안했지만 설치·연결하거나 내용을 수정하지 않았다. 후보를 확정 Mission Data Asset으로 만들지 않았다.
- `UDroneSignalComponent`와 `ADroneJammingVolume`을 추가했다. Overlap 기반 여러 방해 Source 중 최대 강도를 써 `None/Weak/Moderate/Strong` 신호 단계와 HUD 경고를 계산한다. Tick·무작위 입력 손실을 사용하지 않고 강한 단계에서 기본 비행 튜닝의 최대 속도/가속도에 0.70 Greybox 배율을 적용해 Zone 이탈·해제 뒤 복원한다.
- Flight HUD에 신호율·단계 경고와 Blueprint `VideoNoiseIntensity` Snapshot Event를 추가했다. 실제 영상 Noise Material이나 목표 정보 일부 숨김은 아직 구현하지 않았다. `Jamming Exited`·`Jammer Disabled` Mission Rule 사건은 현재 목표/Actor Tag가 맞을 때만 진행한다.
- 초기 재밍 회귀에서는 `Drone.Signal.StageContract`는 성공했으나 `Drone.Mission.ObjectiveRules`의 Jammer 해제 자동 진입이 실패했다. 사건을 Director에 직접 보고하면 통과하고 Blueprint Delegate 구독만 Editor World 자동화에서 호출되지 않는 것을 확인해, 게임 규칙 연결은 Zone의 C++ Native Event로 변경하고 BP Event는 연출용으로 유지했다. 진단용 수동 보고와 로그는 최종 코드에서 제거했다.
- 최신 `DroneEditor Win64 Development` Build 성공, `Drone.Signal.StageContract`, `Drone.Mission.ObjectiveRules`, `Drone.UI.FlightHUDTelemetryBinding` 신호 경고/복원, Flow 2개, Tutorial 2개 묶음 7/7 `Success`·Exit 0. 비활성 Zone의 BeginPlay 사전 Overlap에서도 신호 Source를 제거하도록 방어했다. 실제 맵에 귀환/재밍 Zone을 배치한 PIE, Drone 비행 체감과 HUD 영상 표현은 아직 수동 확인 전이다. 팀원 Training과 TestMap `.umap`은 수정하지 않았고 Commit·Push도 하지 않았다.
- 팀원 배치 절차·기본 수치·실제/미구현 경계는 [`DRONE_JAMMING_GREYBOX_GUIDE.md`](../gameplay/DRONE_JAMMING_GREYBOX_GUIDE.md)에 기록했다.

## 2026-09-16 — Figma 4개 Mission 대조·양쪽 Story 분기·광섬유 면역

- 새로 연결된 Figma `Project:Droner`의 node `1:3`, `46:3`, `49:2`, `53:10`, `273:73`, `282:105`, `283:136`을 읽기 전용으로 확인했다. 원본은 수정하지 않았다. `골든 타임`, `인터셉트`, `베일 브레이커`, `엔드게임`과 Drop/FPV/광섬유/UGV/장거리 타격 역할, Tutorial 요구를 현재 코드와 대조했다.
- 같은 Figma 파일에서 차량은 미끼이고 오마르는 Mission 3에서 처리된다는 전체 설명과, Mission 2 차량에 탑승했다고 전제하고 Mission 3 시작 전에 이미 처리됐다는 개별 화면 문구가 충돌했다. 사용자 요청대로 한쪽을 삭제하지 않고 둘 다 데이터로 설정 가능하게 했다.
- Mission Definition에 성공 시 추가/제거할 Story Fact, Objective Rule에 `Always/FactPresent/FactAbsent` 조건과 Fact ID를 추가했다. Game Flow Snapshot은 Fact를 GameInstance 동안 보존하며 성공 전환과 함께 한 번에 적용한다. Mission Director는 현재 Fact가 맞는 목표만 실행 목록에 포함한다.
- `Story.TargetStillAtLarge` 분기는 Mission 3의 표적 처리 목표를 포함하고, `Story.TargetEliminated` 분기는 그 목표를 제외하고 이미 처리된 후속 목표를 포함하는 경로를 자동화에서 각각 실행했다. 동일 Fact 추가/제거, 빈/중복 ID와 잘못된 조건은 Definition 검증 경계로 관리한다. 실제 Mission 2/3 Data Asset 기본안은 사용자 결정 전 만들지 않았다.
- Figma의 광섬유 Drone `재밍에 면역` 요구를 기존 `EDroneGameplayCapability::JammingImmunity`에 연결했다. Definition의 **Implemented** 목록에 들어간 기체만 활성 재밍 Source를 무시하고, 면역 해제 시 아직 겹친 Source의 가장 강한 단계가 즉시 돌아온다. 광섬유 Drone Definition/Pawn이 없으므로 기존 세 기체에는 면역을 부여하지 않았다.
- `DroneEditor Win64 Development` 전체 Build 성공. `Drone.Mission.ObjectiveRules`, `Drone.Prototype.FlightProfiles`, `Drone.Signal.StageContract`, UI/Flow/Tutorial을 포함한 회귀 8/8 `Success`·Exit 0. 팀원 Training/TestMap `.umap`, Figma 원본, Git Commit/Push는 변경하지 않았다.
- Figma 요구와 구현/미구현·충돌·순서를 [`DRONE_FIGMA_MISSION_IMPLEMENTATION_MATRIX.md`](../planning/DRONE_FIGMA_MISSION_IMPLEMENTATION_MATRIX.md)에 정리했다. 추가 Figma 상세 읽기는 연결에서 재인증을 요구해 중단했고, 이미 확인된 node 내용만 기록했다.

## 2026-09-16 — AI 시험 맵 이동·Mission/Signal 통합 시험 맵

- Unreal AssetTools로 `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`를 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`로 이동했다. 이동 직후 같은 Python 프로세스에서 World를 다시 열어 Python 참조가 GC를 막는 실패가 한 번 발생했지만 실제 AssetTools 이동은 저장됐다. 이동 도구를 에셋 레지스트리 검증까지만 담당하도록 고쳐 재실행했고 정상 종료를 확인했다.
- C++ 자동화와 자동포탑 배치 도구의 고정 맵 경로를 새 위치로 바꿨다. Production `Lvl_DroneTraining`, 용도 미확인 `test1`·`test2`, 나머지 이동 후보 맵은 변경하지 않았다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneMissionSystemsTest`를 새로 만들었다. 충돌 없는 위치 표식, 35%/80% 겹침 Jammer, `Test.Mission.ReturnZone` Tag의 Return Box, Recon/Impact/Payload 표적 각 1개, Carryable 1개와 Prototype GameMode를 배치했다.
- 생성 도구는 기존 맵에서 Validate-only이고 명시적 `Rebuild` 때 `DroneMissionSystemsTest.Owned` Actor 14개만 다시 만든다. 저장 Map Check는 `0 errors / 0 warnings`다.
- `DroneEditor Win64 Development` 빌드 성공. 이동된 AI 맵의 `NPCGreyboxAssets`, `NPCGreyboxPIE`, `NPCPerceptionSearchPIE`, 새 `MissionSystemsTestMap`, `ObjectiveRules`, `Signal.StageContract` 최종 회귀는 6/6 Success·경고 0이다. 자동포탑 배치 도구의 새 경로 Validate-only도 설치형/차량형 각 1기, 차량 Attach, 4점 Suspension, 노면 5개 계약으로 통과했다.
- 새 맵을 바로 Play하면 비행·Signal HUD·역할 기능은 볼 수 있지만 Prototype GameMode이므로 Return/Jammer Mission 목표 완료까지는 실행하지 않는다. 다음은 Test Mission DA와 개발용 진입 경로를 추가해 실제 Mission Director 연쇄를 확인하는 작업이다.
- 사용법과 다음 경계는 [`DRONE_TEST_MAP_GUIDE.md`](../gameplay/DRONE_TEST_MAP_GUIDE.md)에 정리했다. Commit·Push는 하지 않았다.

## 2026-09-16 — 추가 Shotgun NPC·독립 사격 시험 맵

- 기존 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`에 NPC를 더 넣으면 순찰·MG/Cover 점유 경쟁과 기존 4-NPC 자동화 시간이 바뀌므로, 기존 Rifle 1·Shotgun 1·Friendly 2는 그대로 유지했다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneShotgunSystemsTest`를 새로 만들고 `BP_NPC_Hostile_Shotgun` 1명을 추가 배치했다. 약 9m 정면 PlayerStart, 5/10/15m 표식, 독립 Navigation Floor/Bounds와 옆 LOS 차단벽을 두었다. Production `Lvl_DroneTraining`은 열거나 저장하지 않았다.
- 역할 BP가 실제 Gun Mesh를 별도 Component로 쓰면서 부모의 교체용 `WeaponVisualComponent`를 비워 두어 Map Check 경고가 났다. 역할 BP 원본 구조를 바꾸지 않고 이 시험 맵 인스턴스에서만 보이지 않는 Engine Mesh를 채워 실제 Gun 외형을 유지했고, 최종 Map Check는 `0 errors / 0 warnings`다.
- 기본 Projectile Shotgun에서도 8개 Pellet의 예상 비행선을 Cyan으로 표시한다. 실제 충돌·피해는 이동 Projectile이 담당한다. Blueprint에서 표시를 켜고 끄며 직전 Pellet 끝점 배열을 읽는 API도 추가했다.
- `Drone.AI.ShotgunSystemsTestMap`과 `Drone.AI.ShotgunSystemsTestMapPIE`는 전용 NPC/Profile/GameMode/Nav 배치, 실제 감지, 8 Projectile 생성, Shell 소모, 6° 원뿔과 독립 방향을 검증했고 최종 `2/2 Success`, 경고 0이다. `WeaponContract`, `ShotgunTrace`, `ProjectileBallistics`까지 묶은 전체 샷건 계약은 `5/5 Success`, 실패 0이었다. `ShotgunTrace`는 탄창 비움과 명시적 재장전도 확인한다.
- 기존 Smart Object 맵의 Rifle 1·Shotgun 1·Friendly 2와 Asset 계약은 별도 `Drone.AI.NPCGreyboxAssets` 재실행 `1/1 Success`, 경고 0으로 영향 없음을 확인했다.
- 빌드와 생성/검증 도구 사용법은 [`DRONE_TEST_MAP_GUIDE.md`](../gameplay/DRONE_TEST_MAP_GUIDE.md)에 갱신했다. 기본값은 기능 검증용 Greybox이며 최종 밸런스가 아니다. Commit·Push는 하지 않았다.

## 2026-09-16 — FPV Rate/Acro 조작과 바람·비 기획

- 기존 `Assisted Easy`와 제한 자세 `Manual Realistic Greybox`를 유지한 채 세 번째 `Acro Rate Realistic Greybox`를 추가했다. 오른쪽 Stick Pitch/Roll과 Yaw 입력을 Betaflight Actual Rates 의미의 Body 각속도로 변환하며, Stick 중앙에서 자동 수평 복귀하지 않고 Root Local Rotation을 누적해 Roll/Loop가 가능하다.
- FPV Definition만 갱신하는 안전한 Python 도구를 추가해 다른 Mission Data Asset을 다시 저장하지 않았다. FPV 기본값은 Rate/Acro+Agile이고 공개 민간 FPV 참고선으로 Runtime 수평 27m/s, World Z 9m/s, Pitch/Roll 650°/s, Yaw 400°/s를 적용했다. 특정 군용 기체의 성능이나 완전한 모터/PID 물리로 표현하지 않는다.
- `FDroneAcroRateSettings`를 Flight Profile에 노출해 중앙 감도, 축별 최대 Rate, Expo, 수직 속도를 Data Asset/Blueprint에서 조정할 수 있게 했다. 조작 버튼은 쉬운 조작→제한 자세→Rate/Acro 순환으로 갱신했다.
- MSVC 14.51.36256 `DroneEditor Win64 Development` Build 성공. `Drone.Prototype.FlightProfiles`, 3회 PIE 입력·Binding 수명주기의 `Drone.Prototype.PIEInputLifecycle`, `Drone.Flow.MissionEntryContract`, `Drone.Flow.MissionEntryPIE`, `Drone.Prototype.RoleAbilities` 모두 Success·Exit 0이다.
- 바람 지속풍/돌풍/난류/고도 반응과 비 강도/시야/젖음/Splash/실내 감쇠 변수, Weather Subsystem/Volume 책임, Camera-follow GPU Niagara·Effect Type Scalability·저빈도 실내 Trace·MPC Wetness·비입자 Collision 제한을 [`DRONE_WEATHER_WIND_RAIN_PLAN.md`](../gameplay/DRONE_WEATHER_WIND_RAIN_PLAN.md)에 정리했다. 기상 Runtime과 Niagara Asset은 아직 구현하지 않았다.
- Production `Lvl_DroneTraining`과 Figma 원본은 수정하지 않았고 Commit·Push하지 않았다.

## 2026-09-16 — 기상 데이터 계약·지속풍/돌풍 Vertical Slice

- `UDroneWeatherProfile`, `FDroneWeatherSnapshot`, `UDroneWeatherWorldSubsystem`을 추가했다. Profile 기본 10Hz Timer와 고정 Seed로 지속풍·돌풍·풍향 흔들림·수직 기류를 계산하고, 0~60초 Profile 전환을 하나의 World Snapshot으로 전달한다.
- 배치형 `ADroneWeatherController`가 BeginPlay에 Profile을 적용한다. World 기상과 Level 연결을 분리해 Mission이나 TestMap이 같은 C++ 계약을 재사용한다.
- 모든 `ADronePrototypePawn`에 `UDroneWeatherResponseComponent`를 기본 부착했다. 쉬운 조작 65%, 제한 자세 25%, Rate/Acro 0% 기본 보정 뒤 Sweep 위치 Drift를 적용하고 바람이 없으면 Component Tick을 끈다. 현재 `UFloatingPawnMovement` 위 Greybox이며 모터·PID·공기역학 최종 구현이 아니다.
- `/Game/Drone/Data/Weather`에 `DA_Weather_Clear`, `DA_Weather_LightWind`, `DA_Weather_RainStorm_Greybox`를 만들었다. 폭우 Profile의 최대 수평풍 약 10.7m/s는 공개 민간 FPV 참고선이고 최종 내풍 한계가 아니다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneWeatherSystemsTest`를 새로 만들었다. `LightWind` Controller 1개, 35° 풍향 화살표, 바닥·PlayerStart·조명과 Prototype GameMode만 둔 독립 맵이며 Map Check `0 errors / 0 warnings`다. Production Training 맵은 열거나 저장하지 않았다.
- `DroneEditor Win64 Development` Build가 성공했다. `Drone.Weather.ProfileAndWindContract`, `Drone.Weather.ProfileAssets`, `Drone.Weather.SystemsTestMap`은 3/3 Success·Exit 0이고 `Drone.Prototype.PawnDefaults` 회귀도 Success·Exit 0이다.
- 비 강도·생성량·시야·화면 물방울·젖음·Splash·실내 감쇠·Audio 값은 Snapshot에 포함됐지만 Niagara/MPC/Audio 표현은 아직 없다. 비가 체력·신호·Mission 규칙을 자동으로 바꾸지 않는다. 다음 구현은 Camera-follow GPU Rain과 성능 측정이다.
- Commit·Push는 하지 않았다.

## 2026-09-16 — D 드라이브 작업 PC 원격 재동기화

- `D:\JGY\project\drone`과 `D:\JGY\project\md`에서 `git fetch origin --prune`을 다시 실행해 원격 조회가 정상 동작함을 확인했다.
- Unreal은 `main = origin/main = 962ff02`이고 Commit 제목은 `기상 시스템과 기능별 테스트맵 구현`이다. Mission Rule·재밍·Story Fact·FPV Rate/Acro·기상 Runtime, Weather/Mission/Shotgun TestMap과 AI 맵 이동이 모두 이 Push 기준선에 포함됐다.
- 문서는 `main = origin/main = 3c28611`이고 위 구현에 대응하는 상태·가이드·Worklog가 Push 기준선에 포함됐다.
- 확인 시작 시 두 저장소 모두 Clean, Stash 없음, `HEAD...origin/main` 차이 `0/0`이었다. 이전 문서의 C 드라이브 경로와 `로컬 미커밋` Git 표기는 다른 PC의 Push 전 기록이므로 현재 D 드라이브 경로와 최신 Commit으로 정정했다.
- 이번 최신화는 `STATUS.md`, `WORKBOARD.md`, `CONTEXT.md`와 이 Worklog만 변경한다. Unreal 코드·자산·Map은 수정하지 않았으며 Commit과 Push는 사용자가 처리한다.

## 2026-09-16 — Shotgun Pellet 가시화·피해 조정과 Weather TestMap 판독성 개선

- Shotgun 사격장에서 한 탄두만 보인다는 보고를 기존 PIE 계측과 대조했다. 실제 발사 로직은 한 Volley마다 8개 이동 Projectile을 6° 원뿔 안의 독립 방향으로 생성하고 있었고, 전용 PIE도 8발 생성을 통과했다. 원인은 모든 발이 같은 총구에서 같은 프레임에 큰 공용 Sphere로 시작하고 별도 Tracer가 없어 겹쳐 보이는 표현 문제였다.
- 먼저 회귀 계약을 `Pellet당 3 피해`, `작은 비드`, `짧은 Tracer`, `전용 Projectile BP`로 추가했다. 변경 전 `8 피해`, Tracer 없음, 큰 기본 Scale과 Weather Visualizer 0개로 의도한 실패를 확인했다.
- `ADroneNPCProjectile`에 Blueprint 교체 가능한 `ProjectileVisual`과 `ProjectileTrailVisual` Getter를 추가하고 기본 Sphere Scale을 `0.025`, 뒤쪽 Cube Tracer를 `0.14 x 0.0075 x 0.0075`로 설정했다. `/Game/Drone/AI/Blueprints/Projectiles/BP_ShotgunPelletProjectile`을 만들고 `BP_NPC_Hostile_Shotgun`의 Projectile Class에 연결했다. Shotgun은 `8 Pellet`, `6°`, `3500cm/s`를 유지하고 Pellet당 피해를 `8→3`으로 낮춰 전탄 최대 24가 됐다.
- `ADroneWeatherDebugVisualizer`와 `/Game/Drone/Weather/Blueprints/BP_DroneWeatherDebugVisualizer`를 추가했다. Weather TestMap에서 24개 Sphere Bead가 현재 Snapshot 풍향/풍속으로 이동하며 Profile·풍속·풍향·모드를 화면에 표시한다. `1/2/3`과 NumPad `1/2/3`은 Easy 65%/Manual 25%/Rate-Acro 0% 보정을 즉시 비교한다. Bead 수·범위·Scale·재생 배율·Mesh·Readout/Hotkey 사용은 BP/배치 인스턴스에서 조정한다.
- Shotgun/Weather 맵을 도구 소유 Actor만 다시 생성했고 두 Map Check는 `0 errors / 0 warnings`다. MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공, Shotgun 전용 Asset/PIE 2/2, `NPCGreyboxAssets`, `WeaponContract`, `ProjectileBallistics`, `ShotgunTrace`, 강화한 `Drone.Weather.SystemsTestMap`이 모두 성공했다. `git diff --check`와 `git lfs fsck`도 통과했다.
- 화면에서 Pellet 8개 분리 정도와 Tracer 길이·밝기, 한 Volley 최대 24 피해 체감, Weather Bead 가독성과 1/2/3 Drift 차이는 수동 확인이 남았다. RainStorm Profile은 값만 전달하며 Niagara/MPC/Audio 비 표현은 아직 없다. Commit·Push는 하지 않았다.

## 2026-09-16 — 실제 Shotgun 탄 시인성 보강·개인화기 고개 흔들림 안정화

- 작은 회색 Pellet/Tracer가 화면에서 너무 안 보인다는 재확인에 따라 TestMap 선이 아니라 실제 `/Game/Drone/AI/Blueprints/Projectiles/BP_ShotgunPelletProjectile`을 수정했다. `/Game/Drone/AI/Materials/M_ShotgunPelletGlow` 주황 Unlit Emissive 재질을 만들고 비드 Scale을 `0.04`, Tracer를 `0.20 x 0.0125 x 0.0125`로 올려 실제 샷건 NPC가 배치된 모든 맵에 적용했다.
- 샷건 NPC가 표적 발견 뒤 정면에서도 몸/고개를 좌우 왕복한다는 보고를 실제 Controller Tick 경로의 PIE 회귀로 고정했다. NPC 9m 전방 표적을 좌우 30cm, 약 ±1.9°로 번갈아 이동하는 테스트는 수정 전 몸체 회전 한도를 넘어 실패했다.
- `ADroneNPCAIController`의 개인화기 몸 Yaw와 Bone Gaze에 공통 `PersonalWeaponFacingDeadZoneDegrees = 3°`를 추가했다. 데드존 안에서는 정면 오차로 허용하고, 밖에서는 기존 초당 180° 몸 회전과 상체/목/머리 보간을 유지한다. 데드존과 몸 회전속도는 `FDroneNPCProfile`로 옮겨 Hostile Rifle/Shotgun Blueprint `NPCProfileComponent > Profile > NPC|Gaze`에서 역할별 조정할 수 있다.
- 같은 PIE 회귀가 수정 뒤 성공했고, MSVC 14.51.36257 `DroneEditor Win64 Development` Build와 Shotgun Asset/PIE `2/2`가 성공했다. 실제 Pellet BP의 발광 Material·크기·Tracer와 1.9° 정면 안정화가 자동 계약에 포함됐다.
- 영향 확인용 기존 `Drone.AI.NPCPerceptionSearchPIE` 단독 실행은 이번 Shotgun/Gaze 검증이 아니라 사수 사망 뒤 MG 재점유 제한시간에서 실패했다. 로그상 사망 NPC 정리는 성공했지만 생존 Shotgun NPC가 개인화기 상태에 머물러 MG를 다시 Claim하지 않았다. 최신 전체 AI 통과로 기록하지 않고 별도 재현·진단 항목으로 남겼다.
- Rate/Acro 현재 키를 문서화했다. Gamepad Mode 2는 왼쪽 Y Throttle·왼쪽 X Yaw·오른쪽 Y Pitch·오른쪽 X Roll이다. 키보드는 W/S Throttle·A/D Yaw·Q/E Roll이고 Body Pitch 전용 키가 아직 없어 완전한 Loop 시험은 Gamepad/RC Controller가 필요하다. Commit·Push는 하지 않았다.

## 2026-09-16 — Shotgun 실제 분리·공용 탄 시인성·시선 Hysteresis·UI 임시 프로토타입

- 화면에는 Cyan 예상선 8개가 보이지만 실제 Pellet이 하나처럼 보인다는 보고를 생성 카운터만 확인하던 기존 테스트와 분리했다. 첫 Volley 후 80ms 시점의 살아 있는 Shotgun Projectile 수를 세는 회귀를 추가했고 수정 전 `6개 미만`으로 실패해 화면 문제가 실제 수명 문제임을 확인했다.
- 같은 총구·같은 프레임에서 생성된 동일 소유자의 Pellet들이 `WorldDynamic`으로 서로 Block한 것이 원인이었다. Spawn 초기화에서 같은 발사자 Projectile끼리 양방향 Sweep Ignore를 등록해 상호 제거를 막았다. 테스트는 80ms 뒤 8개 전부 개별 비행으로 Green이다.
- 실제 Hostile Shotgun BP와 전용 TestMap 인스턴스를 `8 Pellet / 원뿔 반각 12° / Pellet당 3 피해 / Cyan Debug 기본 Off`로 갱신했다. 전용 발광 비드/Tracer는 유지하고 안전한 적용·검증 도구 `ConfigureDroneShotgunCombatDefaults.py`를 추가했다.
- Rifle·유인 MG·무인 포탑이 공유하는 Native Projectile의 기본 탄두를 `0.06`, Tracer를 `0.60 × 0.018`로 확대하고 Shotgun Glow Material을 공용 임시 발광 재질로 연결했다. Shotgun 전용 BP는 자체 작은 Scale을 계속 덮어쓴다.
- 개인화기 몸 회전은 단일 3° 경계 대신 `3° 정지 + 3° Hysteresis = 6° 시작`으로 바꿨다. Bone Gaze는 작은 잔여 오차를 보간하고 경계에서 0도로 Snap하지 않는다. 머리 Socket Yaw/Pitch 변동까지 실제 PIE에서 검사한다.
- 첨부 와이어프레임을 참고해 C++ fallback Front-end를 `작전 목록 / 선택 작전 / 작전 개요`, Drone Select를 `보유 기체 / 상세 / 조작 설정` 3열 임시 레이아웃으로 다시 구성했다. Flow·Mission/Drone Data Asset·Map 전환 책임은 바꾸지 않았다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `Drone.AI.ShotgunSystemsTestMap` Asset/PIE 2/2, `Drone.AI.ProjectileBallistics`, `Drone.Flow.FrontEndPIE`, `Drone.Flow.MissionEntryPIE`가 모두 Success다. Production `Lvl_DroneTraining`은 열거나 저장하지 않았으며 화면 체감과 16:9 잘림 여부는 사용자 수동 확인이 남았다. Commit·Push는 하지 않았다.

## 2026-09-16 — Acro 키보드/패드 축 분리와 바람 보간 후속 방향

- 고기동 FPV에서 W가 전진 Pitch를 만들지 못하고 W/S와 Space/Ctrl이 모두 Throttle 역할을 하던 증상을 재현했다. 원인은 Acro에서 공용 `IA_Move`를 왼쪽 Stick Throttle/Yaw로 재해석해 같은 Action을 쓰는 키보드까지 함께 바뀌고, 키보드 Body Pitch가 사라진 구조였다.
- 전용 Axis1D Action `AcroPitch/Roll/Yaw/Throttle` 네 개를 만들었다. 키보드는 `W/S Pitch`, `A/D Roll`, `Q/E Yaw`, `Space/Left Ctrl Throttle`, Gamepad는 오른쪽 Y Pitch·오른쪽 X Roll·왼쪽 X Yaw·왼쪽 Y Throttle의 Mode 2다. 쉬운/제한 자세 공용 Action과 Acro Action은 Pawn이 현재 모드별로 한쪽만 소비한다.
- 자산이 없는 상태에서 `Drone.Prototype.AcroInputContract`가 네 Action 누락으로 의도한 Red를 냈다. 구현 후 IMC 33 Mapping, 음수 키 Negate, FPV Integration BP Action 연결과 Pawn Binding을 검사해 Green으로 전환했다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build와 `Drone.Prototype` 8/8이 성공했다. Production Training Map은 열거나 저장하지 않았고 Commit·Push하지 않았다. 키보드/패드 실제 체감은 수동 확인이 남았다.
- 기상 코드를 대조한 결과 Gameplay Gust와 Drone Drift에는 이미 보간이 있으나 Debug Bead는 현재 풍향에 누적 이동거리 전체를 다시 곱해 방향 변화 때 튈 수 있다. 다음 `WTH-02B`는 돌풍 Attack/Release·풍향 최단각 보간, 표시 전용 순간 속도 적분, Bead/Arrow 방향·길이 보간을 테스트 우선으로 진행한다.

## 2026-09-16 — Acro 추력·중력 비행 v1과 WTH-02B 구현

- 기존 Rate/Acro는 Body 각속도로 Root만 회전하고 이동은 별도 `AddMovementInput`에 의존해 W Pitch로 기체를 숙여도 전진력이 생기지 않았다. `Drone.Prototype.FlightProfiles`에 `Nose-down Acro attitude creates forward thrust` 계약을 먼저 추가했고 기존 코드에서 의도대로 실패했다.
- `FDroneAcroRateSettings`에 `HoverThrottleNormalized`, `GravityAccelerationCentimetersPerSecondSquared`, `LinearDragPerSecond`, `BodyRateResponseTimeSeconds`를 추가했다. 모두 `DA_Drone_* > Flight Profile > Acro Rate Settings`와 Blueprint에서 조정 가능하다.
- Acro 스로틀은 `-1=무추력`, `0=수평 호버`, `+1=최대 추력`으로 변환한다. World Down 중력과 Body Up 추력을 합쳐 기체를 Pitch/Roll하면 추진 방향이 실제로 바뀌며, 속도 비례 지수 항력과 Rate 응답 지연을 적용한다. 기존 FloatingPawnMovement 자동 감속은 Acro에서 꺼 항력과 중복되지 않게 했다.
- FPV 저장 기본값은 호버 `0.50`, 중력 `980cm/s²`, 선형 항력 `0.12/s`, Body Rate 응답 `0.08s`다. 기존 27m/s 전체 속도와 World Z 9m/s 제한, 650°/s Pitch/Roll, 400°/s Yaw는 유지한다. 모터별 RPM·PID·공력·질량/관성 모델은 아니며 물리 체감 v1이다.
- Acro Throttle의 `Completed/Canceled` 입력 리셋을 추가하고 PIE Binding 수명주기 계약도 Triggered/Completed/Canceled 각 1개로 갱신했다. Editor Build 성공, 최종 `Drone.Prototype` 8/8 Success·실패 0이다.
- `FDroneWindSettings`에 돌풍 Attack/Release와 풍향 Response 시간을 추가했다. 세기·수직 돌풍은 Attack/Release 지수 응답, Yaw 편차는 최단각 응답을 사용한다. LightWind는 `0.8/1.8/1.0s`, RainStorm은 `0.45/1.2/0.65s`를 저장했다.
- Debug Visualizer의 스칼라 누적 거리 재투영을 제거하고 표시용 풍속을 매 Frame 보간한 뒤 Local 속도 벡터를 적분한다. 풍향 X→Y 전환 시 이전 X 이동을 유지하며, Bead는 풍향으로 회전하고 풍속에 따라 길이가 변한다. 응답 시간·기준 풍속·길이·단면은 BP/배치 인스턴스에서 조정한다.
- `Drone.Weather` 3/3 Success·실패 0, 방향 전환 궤적 보존과 Frame Step 독립 적분 자동화가 통과했다. Production `Lvl_DroneTraining`은 열거나 저장하지 않았고 Commit·Push하지 않았다. Acro 체감과 Weather 화면 무점프 확인은 사용자 수동 항목으로 남겼다.

## 2026-09-16 — Smart Object Greybox 차량 바퀴 회전축 교정

- `Lvl_NPCSmartObjectGreybox`의 차량 바퀴가 진행 방향으로 구르지 않고 옆으로 회전한다는 화면 보고를 저장 Asset과 대조했다. 차량 BP와 맵 인스턴스는 기본 Cylinder가 아니라 `/Game/MillitaryBase/Meshes/SM_SpikeStorm_Tire2_FR`을 네 바퀴에 사용하며, Mesh Local Bounds의 얇은 축은 Y였다. 기존 코드는 Cylinder 전용 Local Z축 회전을 고정해 실제 Tire Mesh 장착 회전과 맞지 않았다.
- 실제 저장 `BP_GroundConformingVehicle_Greybox`를 Spawn해 전진 한 프레임 뒤 각 바퀴 Rotation Delta 축을 검사하는 회귀를 추가했다. 수정 전 네 바퀴 모두 차량 좌우 차축 조건에 실패하는 Red를 확인했다.
- 바퀴 회전은 Mesh 원본축이 아니라 `VehicleCollision` 부모 공간 `+Y`에 적용하도록 바꿨다. 좌우별 `Roll 0°/180°` 장착 회전은 Base Rotation으로 보존하며, 방향 부호는 기존 `+1`을 유지한다. `Wheel Visual Spin Axis In Vehicle Space`를 Blueprint에 노출해 다른 차량 좌표계도 조정할 수 있게 했다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공, `Drone.Vehicle.GroundConformingSuspension`은 동일 회귀를 포함해 Success로 전환했다. 자동포탑/차량 읽기 전용 검증도 차량 1·바퀴 4·차량 포탑 Attach·노면 5·Map Check 0/0으로 통과했다.
- 전체 `Drone.AI.NPCGreyboxAssets`는 차량이 아니라 팀원이 교체한 `BP_NPC_Friendly_Base` Character Mesh가 오래된 역할 Mesh 기대값과 달라 실패했다. 이번 바퀴 수정과 분리해 기록하며 Friendly 자산을 되돌리지 않았다. 최종 바퀴 구름 방향은 Editor 화면 재확인이 남았다.
- 회전축 교정 후 실제 Tire가 도로 두께만큼 잠긴다는 화면 보고를 독립 평면 회귀로 추가했다. `SM_SpikeStorm_Tire2_FR`의 세로 반지름은 약 50cm지만 저장 차량 BP의 `Wheel Radius`는 Native Cylinder용 30cm여서 네 바퀴 모두 약 20cm가 지면 아래에 있었다.
- `Wheel Radius`의 Blueprint 범위를 `1~500cm`로 명시하고 현재 Tire BP 기본값을 52cm로 저장했다. BP 한 개만 갱신하는 `DRONE_VEHICLE_WHEEL_DEFAULTS_ONLY` 도구 모드를 추가해 팀원 NPC와 맵을 재저장하지 않았다. 수정 뒤 Tire Bounds·평면 접촉·회전축을 함께 검사하는 `GroundConformingSuspension`과 읽기 전용 차량/포탑 맵 Validate가 성공했다.

## 2026-09-17 — 적 AI 재검증 및 Weather TestMap 디버그 강우 프리뷰

- 문서 저장소 Markdown 57개를 목록화하고 최신 README/CONTEXT/STATUS/WORKBOARD, AI·Smart Object·MG·Gaze, 날씨/시험 맵 계획, Project Audit, 최신 Worklog 항목을 대조했다. 서로 충돌하는 과거 기준은 현재 Source와 최신 STATUS/WORKBOARD를 우선했다.
- 사용자 체감 적 NPC 떨림/애니메이션 중첩은 Headless 자동화만으로 화면 재현되지 않았다. `Drone.AI.NPCGreyboxAssets`, `NPCPerceptionSearchPIE`, `PersonalWeaponEngagementPolicy` 3/3과 Shotgun Asset/PIE 2/2는 통과했으나, AnimBP 포즈 중첩·실제 화면 떨림이 해결됐다는 뜻은 아니다. AI 소스와 Production 맵은 수정하지 않았고 수동 PIE 재현이 남아 있다.
- 기존 `ADroneWeatherDebugVisualizer`에 `7 Clear / 8 LightWind / 9 RainStorm` 진입점을 추가했다. 지정된 `Lvl_DroneWeatherSystemsTest`에서만 프로파일 Snapshot을 즉시 교체하며 다른 맵과 잘못된 인덱스는 거부한다. 기존 1/2/3 조작 모드 키는 유지했다.
- Rain Snapshot 강도×SpawnScale로 최대 80개 선분을 0.2초 간격으로 생성하는 DebugDraw 프리뷰를 전용 TestMap에만 연결했다. 비가 0이면 추가 Draw 호출을 멈추고 잔여 선분은 짧은 수명 뒤 사라진다. 파티클별 Trace·새 Niagara/Material/맵 저장은 없다. 이 프리뷰는 정식 Niagara 효과나 GPU 성능 측정이 아니다.
- UE 5.8.2 `DroneEditor Win64 Development` Build 성공, `Drone.Weather.DebugPresetEntry` 1/1 Success. 기존 기상 회귀 3/3도 성공했다. Rain VFX Niagara, Wetness MPC consumer, Rain Audio, 품질별 GPU 측정은 미완성이다. MCP 서버는 설정돼 있지 않아 별도 연결/설치는 하지 않았다.
- Drone Source/Test/가이드와 문서 STATUS/WORKBOARD/기상·시험 맵 안내를 로컬 수정했다. Unreal 시작 기준 `3449766`, 문서 시작 기준 `8b3b7b1`; Commit·Push하지 않았고 실제 맵/기존 자산을 저장하지 않았다.

## 2026-09-17 — NPC 행동 로직 추가 감사 및 타이밍 수정

- 사용자 요청에 따라 OpenCode `openrouter/stealth/union-alpha`에 NPC 행동 로직 점검·문제 수정 업무를 위임했다. 제공된 키는 프로세스 입력으로만 사용했으며 문서/명령 출력에 다시 기록하지 않았다. 완료된 뒤 별도 모델 실행은 남아 있지 않다.
- `ADroneNPCAIController`에서 MG 재할당 유지 처리와 일반 Controller Tick이 같은 프레임에 `UpdatePersonalWeaponEngagement`를 중복 호출해 사거리 이탈·무진행·재경로 타이머가 두 배 진행될 수 있음을 확인했다. 유지 분기는 유효성 확인만 하고, 한 프레임의 시간/발사/이동 갱신은 Controller Tick 한 곳이 담당하도록 수정했다. `Drone.AI.PersonalWeaponMaintenanceTiming` 회귀를 추가했다.
- UE 5.8.2 `DroneEditor Win64 Development` Build 1회 성공. 한 번 실행한 집중 필터에서 `PersonalWeaponMaintenanceTiming` 성공(로그 경고 7건), `NPCPerceptionSearchPIE` 성공, `ShotgunSystemsTestMapPIE` 실패(정지 pursuit 목표에서 MoveTo 요청 수 기대 2/실제 3). 프로세스 종료 코드 0은 전체 자동화 성공을 뜻하지 않는다.
- 추가 요청이 이미 끝난 경로의 정상 복구인지 중복 제출인지는 PathFollowing 상태·이전 RequestID·완료/중단 사유 로그가 없어 판단하지 못했다. 추측성 가드/테스트 기대값 변경은 하지 않았다. 사용자 보고 몸/머리 떨림은 Headless에서 재현되지 않았으며 저장 AnimBP 전체 그래프/실제 포즈도 이번 확인 범위가 아니다.
- 추가 실행은 사용량을 아끼도록 실패한 Shotgun PIE 한 건만 대상으로 호출 전후 PathFollowing 상태, RequestID, 목표 편차, 완료/Abort 결과를 계측해 원인을 분리한다. 화면 떨림은 PIE에서 관찰할 때 AnimBP Debug Filter와 StateTree 실제 활성 노드를 함께 기록해야 한다.

## 2026-09-17 — Smart Object 맵 종료 후 최종 재검증

- Unreal Editor 종료를 확인한 뒤 최신 `DroneEditor Win64 Development` 빌드를 다시 성공시켰다.
- 실제 스마트 오브젝트 맵 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`만 대상으로 `NPCBaseRoutinesPIE`, `NPCGreyboxPIE`, `NPCPerceptionSearchPIE`를 실행해 3/3 Success, 실패 0, 미실행 0을 확인했다.
- 앞선 연속 실행에서 보였던 MG 재할당 실패는 최종 재실행에서 재현되지 않았다. 다만 해당 자동화의 수동 감지 주입·런타임 프로필 변경 한계 때문에 화면상의 도리도리/옆구리 사격/뒤로 걷기 해결을 자동화만으로 확정하지 않는다.
- 진단용 `SOAudit` 로그 코드는 제거하고 기능 수정만 남겼다. 커밋·푸시는 하지 않았다.

## 2026-09-17 — 순찰 중 NPC 충돌 정지 수정

- 순찰 중 Shotgun NPC가 고개를 돌리며 뒤로 걷고 이동을 반복 중단하는 현상을 `PatrolProjectileFixAudit` 로그로 대조했다. `BP_ShotgunPelletProjectile`이 `ECC_Pawn`을 Block해 NPC를 이동 장애물로 막는 것이 직접 원인이었다.
- `DroneNPCProjectile`이 의도한 표적이 아닌 `ADroneNPCCharacter`를 Sweep Ignore하도록 수정했다. 감지 진입/Search 종료의 잔여 속도 제거와 Patrol 중 Combat Gaze 차단도 함께 적용했다.
- 최신 Editor Build 성공. `NPCPerceptionSearchPIE`와 `NPCBaseRoutinesPIE`가 각각 Success로 통과했고 수정 후 `stuck` 로그가 없었다. 커밋·푸시는 하지 않았다.
- 감사 세부사항과 저장 금지 수동 PIE 절차는 [`../ai/DRONE_NPC_BEHAVIOR_AUDIT_2026-09-17.md`](../ai/DRONE_NPC_BEHAVIOR_AUDIT_2026-09-17.md)에 있다. 추가 빌드/테스트, 맵/에셋 저장, Production Training 접근, commit/push는 하지 않았다.

## 2026-09-16 — 병사 StateTree 상태 전환 안정화

- Cover/MG 태스크가 일시적인 예약·사격 실패를 바로 `Failed`로 반환하고, MG 사망 교대 Event가 0.75초마다 현재 Cover 상태를 끊을 수 있어 병사 상태와 시선이 왕복할 수 있는 경로를 확인했다.
- 먼저 `SmartObjectFoundationDefaults`에 Blueprint 조정 가능한 최소 상태 유지시간 계약을 추가했고, 구현 전 Property가 없어 의도대로 Red가 되는 것을 확인했다.
- `ADroneNPCAIController`가 모든 대응 상태 진입 시각을 한 곳에서 기록하고 기본 `Minimum Response State Duration Seconds=1.0`을 제공하도록 변경했다. 최소시간 동안 `DroneDetected`, MG/Cover 이동·점유·사격, Search의 현재 행동 조건을 재점검하고 시간이 지난 뒤에도 실패일 때만 기존 StateTree 실패 전환을 허용한다.
- MG 재할당 대기 시작 시 개인화기 사격을 즉시 끄지 않고 실제 Event를 보낼 때만 정리하도록 바꿨다. Cover 점유 성공과 같은 프레임에 첫 사격 시작이 실패해도 점유 상태 자체를 실패 처리하지 않으며 `UseCover` Tick에서 다시 시작한다.
- 사망, Drone 파괴, Sight Lost 유예 뒤 확정 정리는 즉시 처리해 위험한 상태를 억지로 유지하지 않는다. 값 `0`은 안정화 대기를 끄며 Controller Blueprint `Drone > AI > State Stability`에서 조정할 수 있다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. Red였던 `SmartObjectFoundationDefaults`와 `HostilePatrolStateTreeAsset`, 차량 `GroundConformingSuspension`은 Success다.
- 실제 `NPCPerceptionSearchPIE`는 2회 모두 감지·사격·Cover·최초 MG 점유와 사망 정리까지 진행했지만, 생존 병사가 빈 MG를 각각 2회/3회 Claim한 뒤 Operator Anchor로 Nav 도착하지 못해 기존 재점유 제한시간 항목에서 실패했다. 상태 안정화 결과와 분리해 맵 경로/Collision 결함으로 계속 추적하며 Success로 기록하지 않는다.
- 최종 Git 감사 중 원격 `72c964c`, Merge `4a3d4ba`가 추가됐고 변경 파일은 팀원 `Lvl_MilitaryBase.umap` 하나였다. 로컬 작업과 겹침이 없어 fast-forward했으며 Unreal 기준은 `main = origin/main = 4a3d4ba`다.
- `stash@{0}: On main: !!GitHub_Desktop<main>` 1개가 남아 있다. Shotgun/Weather/Acro 시기 파일 49개를 포함한 자동 Stash라 현재 로컬 변경과 중복 가능성이 크지만, 사용자 작업 유실을 피하기 위해 이번에는 적용·삭제하지 않았다.

## 2026-09-18 — D 드라이브 기준 재동기화와 NPC 순찰 재현

- `fetch --prune` 뒤 Unreal `D:\JGY\project\drone`은 `main = origin/main = 9f58b51`, 문서 `D:\JGY\project\md`는 `main = origin/main = 6960648`이며 두 저장소 모두 원격 차이 `0/0`임을 확인했다. 문서 최신화 시작 전 두 작업 트리는 clean이었다.
- 최신 Unreal Commit과 사용자 화면 보고를 대조해 Shotgun NPC 뒤로 걷기/문워크는 해결 완료가 아니라 진행 중 결함으로 다시 분류했다. 기존 Actor 전방 정렬 자동화는 Skeletal Mesh 포즈, AnimBP의 Speed/Direction, 실제 BlendSpace 선택을 검증하지 못한다.
- 격리된 `Drone.AI.ShotgunSystemsTestMapPIE`는 경계 흔들림·추적 진전·몸/시선 정렬·사거리 진입 정지·리시 포기 후 순찰 복귀를 모두 통과했다.
- 실제 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`의 `NPCBaseRoutinesPIE`는 최초 묶음 실패, 단독 재실행 성공 뒤 4회 반복에서 3회 실패해 높은 재현율의 순찰 플래키로 확정했다. `NPCPerceptionSearchPIE`는 같은 기준에서 성공했다.
- 순찰과 개인화기 추적 양쪽에서 `EPathFollowingStatus::Paused`를 정상 진행으로 취급해 재요청과 정체 제한을 우회하던 분기를 확인했다. `Moving`만 실제 진행으로 인정하고 `Paused`는 기존 재요청·2초 정체 처리로 회복하도록 1차 수정했다.
- 실패 시 Rifle/Shotgun 역할, ResponseState, MoveStatus, 완료/방문 횟수, 위치·속도를 보고하도록 실제 맵 자동화 진단을 보강했다. Editor가 열려 있어 Build와 수정 후 반복 검증은 대기 중이다.
- 외부 OpenCode 모델 검증은 실제 호출이 정상 보고서로 이어지지 않아 사용을 종료했다. 이번에 만든 프로젝트 Agent·모델 설정과 문서 가이드는 제거했으며 이후 외부 모델 호출을 작업 기준에 포함하지 않는다.
- Production Training 맵과 Asset은 수정하지 않았고 Commit·Push도 수행하지 않았다.
- 실제 보행 증상을 직접 잡도록 `NPCBaseRoutinesPIE`에 Actor 전방과 실제 수평 속도의 내적을 샘플링하고, 역방향 상태가 0.35초를 넘으면 실패하는 회귀를 추가했다. 수정 전 Shotgun은 3/3 실패했고 `worstDot=-1.000`, 최대 연속 역방향 1.56~3.95초가 기록됐다.
- 순찰·수색·추적 등 실제 이동 중에는 상태명이 아니라 속도 벡터를 몸 Yaw의 단일 기준으로 사용하도록 수정했다. 같은 회귀를 포함한 실제 맵 순찰은 수정 빌드에서 4/4 성공했다.
- 묶음 회귀의 `ShotgunSystemsTestMapPIE`에서 고정 표적에 MoveTo가 1회에서 2회로 늘어나는 Red를 추가로 추적했다. 첫 감지를 Perception과 StateTree가 중복 진입해 경로를 취소할 수 있는 흐름, 순찰 Task의 늦은 종료가 전투 MoveTo를 취소하는 소유권 충돌을 막았다.
- 마지막으로 첫 MoveTo가 `Success`로 끝났어도 부분 경로/허용 반경 때문에 실제 사거리 밖일 수 있고, 기존 코드는 같은 투영 목적지를 즉시 재요청함을 확인했다. 성공 완료한 동일 목적지는 정착 상태로 유지하고 표적이 재경로 거리 이상 이동할 때만 새 경로를 만들며, 계속 사거리 밖이면 기존 무진전 제한으로 포기·순찰 복귀하도록 수정했다.
- 임시 `[DEBUG-MOVE-COMPLETE]`, `[DEBUG-PURSUIT-REPATH]` 계측은 제거했다. Editor 종료 뒤 MSVC 14.51.36257 `DroneEditor Win64 Development` 최종 링크 Build가 성공했다.
- 전용 Shotgun PIE의 Pursuit 표적은 시험 맵 NavMesh 안의 실제 사거리 밖 지점으로 옮겨 부분 경로 Success와 정상 추적을 혼동하지 않게 했다. 단독 `ShotgunSystemsTestMapPIE`가 Success이고, `PersonalWeaponEngagementPolicy`, `PersonalWeaponMaintenanceTiming`, `ShotgunSystemsTestMapPIE`, `NPCGreyboxAssets`, `NPCPerceptionSearchPIE` 묶음 5개도 전부 Success·실패 0이다.
- 실제 Smart Object 맵 `NPCBaseRoutinesPIE`를 `-TestLoops=4`로 실행해 4/4 Success, 오류·경고 0을 확인했다. 수정 전 4회 중 3회 실패 및 몸/속도 역방향 3/3 Red였던 피드백 루프가 최종 Green으로 바뀌었다. 맵·Asset은 저장하지 않았고 Commit·Push도 수행하지 않았다.

## 2026-09-18 — Shotgun Pursue 전신 회전 후속 수정

- 사용자 화면 보고의 Shotgun 빙글빙글 회전을 `Drone.AI.ShotgunSystemsTestMapPIE`에 같은 대응 상태 안에서의 연속 몸 Yaw 회귀로 재현했다. 수정 전 `PursueDrone`에서 3초 안에 같은 방향 누적 `301~304°`를 반복해 넘겼고 최근 Yaw·속도 표본을 확보했다. 상태가 바뀌면 누적값을 초기화해 서로 다른 행동의 정상 회전은 합산하지 않는다.
- 진단 계측에서 Nav 가속과 RVO는 이미 꺼져 있었지만 `UCharacterMovementComponent::bRequestedMoveUseAcceleration`은 켜져 있었다. Drone 위치에 무기 사거리 크기의 큰 도착 반경을 둔 MoveTo가 가까운 부분 경로 Segment를 가속으로 지나치고, 몸과 Bone Gaze가 약 40~120cm 거리의 즉시 경로 코너를 계속 따라가며 공전하는 흐름을 확인했다.
- Drone에서 `PersonalWeaponPursuitRangeRatio`만큼 떨어진 실제 지상 사거리 정지점을 NavMesh에 투영하고 기본 75cm 도착 반경으로 이동하도록 바꿨다. Pursue에만 요청 가속을 기본 해제하고, Controller가 안정된 최종 정지점을 향해 몸 Yaw를 보간하며 Bone Gaze도 같은 목표를 공유한다. 순찰·수색의 실제 속도 방향 보정과 정지 사격 조준은 유지했다.
- 요청 가속을 전 상태에서 끈 첫 시도는 실제 맵 회귀가 순찰 역방향 `0.614초`를 검출했다. 이를 Pursue에만 한정하고 일반 순찰은 요청 가속을 유지하도록 수정한 뒤 다시 검증했다.
- 전용 Shotgun PIE에는 같은 상태에서 연속 300° 초과 몸 회전 실패 조건을, 실제 Smart Object 맵 회귀에는 정지 회전과 0.35초 초과 역방향 보행 실패 조건을 유지·추가했다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. 완전히 새 Editor 프로세스에서 Shotgun 교전 3/3, 실제 Smart Object 맵 순찰 3/3이 성공했다. `NPCGreyboxAssets`, `NPCPerceptionSearchPIE`, `PersonalWeaponEngagementPolicy`, `PersonalWeaponMaintenanceTiming`, `ShotgunSystemsTestMapPIE` 관련 묶음 5개도 모두 Success다. Maintenance의 Skeletal Mesh 없는 최소 시험 Actor 경고 7건은 예상 경고다. 맵·Asset·Production Training은 수정하지 않았고 Commit·Push도 수행하지 않았다.
- 종료 정리 중 `fetch --prune`에서 `origin/main=9a94f06 260918`을 새로 확인해 로컬 `main=9f58b51`이 1개 뒤가 됐다. 원격 커밋은 Content 1,412개만 변경하고 Source·Config·Plugins·현재 AI 소스·Shotgun/Smart Object 시험 맵과 겹치지 않는다. `Lvl_DroneTraining`과 `Lvl_DroneTutorialSystemsTest` 및 대용량 LFS 에셋을 포함하므로 더러운 작업 트리에 자동 Pull하지 않았으며, 위 검증은 로컬 기준이다.

## 2026-09-18 — Shotgun 순찰 충돌 2차 원인과 FPV Mode 1/2

- 사용자가 실제 `Lvl_NPCSmartObjectGreybox`를 다시 실행했을 때 Shotgun의 회전 주기만 줄어든 채 증상이 남았다. 이 실행의 `Drone.log`에서 Rifle이 Shotgun BP의 추가 `Gun` 컴포넌트에 침투·충돌해 `stuck and failed to move`가 되는 정확한 상대를 확인했다.
- 자동 PIE에서도 Shotgun `Gun`이 `QueryAndPhysics`, Overlap On, Navigation On으로 재현됐다. NPC Character는 이동 Capsule만 충돌을 소유하고, Construction/BeginPlay에서 나머지 Primitive를 `NoCollision`, Overlap Off, Nav Off로 강제하도록 변경했다. 역할 BP에 팀원이 별도 Gun/Mesh를 추가해도 같은 계약을 적용한다.
- 순찰 시작 구간에서 Shotgun이 100cm 진행하기 전에 누적 300도를 도는 Red도 추가했다. Nav의 50~100cm 즉시 경로점을 몸 방향으로 계속 쓰던 흐름을 분리하고, Patrol 몸은 예약된 최종 Smart Object 슬롯 방향을 유지하도록 했다.
- 수동 재현 후 바로 원인을 읽을 수 있도록 개발 빌드에 `[NPC-STATE]`, `[NPC-MOVE]`, `[NPC-COLLISION-FIX]`를 추가했다. 이동 로그는 적 NPC당 기본 0.5초 간격이며, 화면 해결 확인 뒤 기본 비활성화할 임시 진단 단계다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `NPCBaseRoutinesPIE`, `NPCGreyboxPIE`, `ShotgunSystemsTestMapPIE`가 모두 Success이고 수정 뒤 `stuck` 로그가 없다. 실제 렌더 화면에서 45~60초 순찰 교차·추적·복귀 확인은 사용자 수동 항목으로 남겼다.
- FPV 조작은 기존 Easy·제한 자세에 RC 송신기 Mode 1과 Mode 2를 별도 모드로 추가했다. Mode 1은 왼쪽 Y Pitch/오른쪽 Y Throttle, Mode 2는 왼쪽 Y Throttle/오른쪽 Y Pitch이며 두 모드 모두 왼쪽 X Yaw/오른쪽 X Roll이다. 키보드는 W/S Pitch, A/D Roll, Q/E Yaw, Space/Ctrl Throttle을 공통 유지한다.
- 새 패드 세로축 Input Action 2개와 IMC 전체 33 Mapping을 저장하고 FPV Pawn BP에 연결했다. 기존 `AcroRateRealisticGreybox` 이름은 Asset 직렬화 호환을 위해 Mode 2 의미로 유지했다.
- UI의 `안정/균형/고기동`은 `느림/보통/빠름`으로 바꿨다. 내부 Stable/Balanced/Agile 이름은 Asset 호환을 위해 유지하고 기본 프리셋은 MaxSpeed `0.80/1.00/1.25`만 변경하며 가속·Yaw·자세각 배율은 모두 1.0이다.
- 입력 변경 후 `AcroInputContract`, `FlightProfiles`, 3회 새 PIE의 `PIEInputLifecycle`, `MissionEntryPIE`가 Success다. Lifecycle은 처음에 새 Action을 예상 목록에서 빼 `31/33` Red, 다음에는 Completed/Canceled Binding 분류 누락으로 Red가 났고 테스트 계약을 보완해 최종 Green으로 전환했다.
- Production `Lvl_DroneTraining`은 열거나 저장하지 않았고 Commit·Push·원격 Pull도 수행하지 않았다.

## 2026-09-18 — 첫 사격 조준 지연·Figma 재확인·CourseSpline 편집 확인

- 사용자 화면에서 Shotgun/Rifle 이동·회전 수정이 정상임을 확인해 임시 이동 진단 로그 기본값을 Off로 전환했다.
- 적이 Drone을 최초 감지한 뒤 Rifle/Shotgun 첫 발까지 기본 1.0초를 기다리는 `PersonalWeaponInitialAimDelaySeconds`를 Controller Blueprint 조절값으로 추가했다. Sight 감지 시각을 별도로 보존하므로 DroneDetected/Pursue/Cover 상태 전환이 지연을 재시작하지 않는다.
- 다른 Drone으로 표적이 바뀔 때 기존 사격 Timer가 새 조준 지연을 우회하지 않도록 이전 개인화기 사격을 먼저 정리한다.
- MSVC 14.51.36257 Editor Build, `SmartObjectFoundationDefaults`, `ShotgunSystemsTestMap`, `ShotgunSystemsTestMapPIE`, `NPCGreyboxPIE`가 Success다. Shotgun PIE는 조준 완료 전 Fire Event 0과 감지 관측 시각부터 첫 Volley까지의 시간도 검사한다.
- Figma `Project:Droner` Page 1 최상위 148개를 읽기 전용으로 재확인했다. 최신 Mission 진입 흐름, Mission 선택 Greybox, 공중 Drone 공통 HUD, Racing UI/Restart/Quit/기록·감도·Ghost 요구를 문서 매트릭스에 반영했으며 Figma 원본은 수정하지 않았다.
- CourseSpline 점 추가는 UE 5.8 기본 편집 기능으로 이미 제공된다. `CourseSpline`의 기존 점 선택 후 `Alt+이동 기즈모 드래그` 또는 선분 우클릭 `Add Spline Point Here`를 사용한다. Ring별 Spline Handle은 Gate 전용이므로 구분한다. 코드·Blueprint·맵은 수정하지 않았다.

## 2026-09-22 — 야외 AI·차량 Spline Route·Random Weather Manager

- Native AI 기본값을 유지하면서 `/Game/Drone/AI/Blueprints/BP_DroneNPCAIController_Outdoor`를 추가했다. Hostile Rifle/Shotgun은 이 BP를 사용하며 Sight 60m, Lose Sight 70m, Smart Object 검색 반경 80m·Half Height 10m, 직전 완료 지점 회피 15m를 Blueprint에서 조정한다.
- `/Game/Drone/Vehicles/Blueprints/BP_DroneVehicleSplineRoute`와 `ADroneVehicleSplineRoute`를 추가했다. 차량은 Instance에서 Route를 지정하고 Follow, 속도, 끝 반전/Loop를 조정한다. XY/Yaw는 Spline 위치·접선, Z/Pitch/Roll은 기존 4점 지면 Trace가 담당하며 종점 Event를 노출한다.
- `/Game/Drone/Weather/Blueprints/BP_DroneRandomWeatherController`를 배치형 Weather Manager로 추가했다. E/NE/N/NW/W/SW/S/SE와 CALM, 방향 8~18초·세기 5~12초·풍속 1~9m/s 시작값, 방향/속도 보간과 재현 Seed를 Blueprint Class Defaults에서 조정한다.
- Manager는 에디터에서 위치 확인용 원뿔 Mesh를 보이지만 Editor 전용 Component라 Play/Package에는 존재하지 않는다. Actor·원뿔 Collision, Overlap, Navigation 영향은 모두 끈다.
- Runtime Wind Override를 World Subsystem에 추가해 Random Manager가 Profile의 비·가시거리 등은 유지하면서 수평 바람만 갱신한다. CALM은 Gust까지 억제해 실제 0m/s가 된다.
- 풍향 표기는 프로젝트 좌표 `+X=E`, `+Y=N` 기준 Cardinal로 통일했다. Flight HUD는 `풍향 NE | 풍속 5.2 m/s`, Debug Visualizer는 같은 방향과 m/s를 표시한다.
- 팀원이 수정 중인 `Lvl_DroneShotgunSystemsTest`, `Lvl_NPCSmartObjectGreybox`는 덮어쓰지 않았다. 차량 Route는 안전한 TestMap에서 맵 담당자가 직접 배치·연결하도록 남겼다. Production `Lvl_DroneTraining`도 수정하지 않았다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. Weather TestMap 재생성 Map Check 0/0, `SmartObjectFoundationDefaults`, HUD 2종, `GroundConformingSuspension`, Weather 2종 최종 6/6 Success·경고 0이다. Commit·Push는 수행하지 않았다.
