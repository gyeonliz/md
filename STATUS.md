# 현재 작업 상태

기준일: 2026-09-17 (Asia/Seoul)

## 한눈에 보기

- 현재 단계: 기존 AI 3/3·Shotgun 2/2 기준선은 통과했으나, 9/17 후속 집중 회귀는 새 타이밍 테스트와 `NPCPerceptionSearchPIE` 성공, Shotgun PIE의 안정된 MoveTo 요청 수 검사 실패로 부분 통과다. 개인화기 교전 타이머의 한 Tick 중복 누적 경로를 수정했다. 사용자 체감 애니메이션 떨림은 화면에서 아직 재현/해결 확인되지 않았다. Weather TestMap의 디버그 빗줄기 프리뷰는 정식 Niagara 비가 아니다
- 바로 다음 개발: Weather TestMap에서 7/8/9 비 프리뷰와 적 NPC 애니메이션 떨림을 직접 화면 확인 → 정식 camera-follow Niagara/MPC/Audio·품질 단계 → Test Mission DA/진입 경로
- Unreal Editor: 마지막 확인 시 종료 상태
- Production Training: 팀원이 실제 Tutorial 환경을 제작 중이므로 열람 외 저장·덮어쓰기·자동 재구성 금지

## Git 기준

| 저장소 | 현재 기준 | 상태 |
|---|---|---|
| Unreal `C:\URproject\drone` | 기준 `main = origin/main = 3449766` | 9/17 로컬 변경: Weather TestMap 비 디버그 프리뷰와 AI 교전 타이머 중복 누적 수정, 테스트/가이드. Commit·Push 안 함 |
| 문서 `C:\Users\jkw11\Documents\Codex\2026-08-19\codex-gpt-chatgpt-codex-1-6` | 기준 `main = origin/main = 8b3b7b1` | 확인 뒤 WTH-03/AI 감사 결과 반영으로 `STATUS.md`, `WORKBOARD.md`, Worklog 및 NPC 감사 문서 로컬 수정; Commit·Push 안 함 |

2026-09-17 작업컴 재확인: 확인 시 Unreal `3449766`, 문서 `8b3b7b1`이 각각 `origin/main`과 일치하고 두 작업 트리가 clean이었다. 이번 확인 이후 문서 저장소에는 `STATUS.md`와 `WORKBOARD.md`만 로컬 수정되어 있다. 수동 PIE 화면 확인은 아직 완료로 간주하지 않는다. OpenCode CLI `v2.0.5`를 사용자 제공 키로 `openrouter/stealth/union-alpha`에 연결해 WTH-03 범위를 점검했다. OilRig Rain 텍스처/Material Function은 있으나 Niagara Rain 시스템, 재질에서 실제 소비하는 Wetness MPC, Rain Audio 연결은 없어 추측성 C++ 연결을 추가하지 않았다. `DroneEditor Win64 Development` 빌드와 `Drone.Weather.ProfileAssets` 1/1이 통과했고, Unreal 작업 트리는 clean이며 Commit·Push는 하지 않았다. 제공 키는 채팅/파일에 재출력·저장하지 않고 해당 실행 프로세스에서만 사용했다.

같은 날 후속 작업: Union Alpha 위임 검토는 사용량 증가를 줄이기 위해 중단하고 남은 확인은 로컬로 진행했다. 사용자 체감 NPC 떨림은 Headless 회귀에서 원인이 재현되지 않아 AI 코드는 수정하지 않았다. Baseline AI 3/3, Shotgun Asset/PIE 2/2, Weather 기존 3/3이 통과했다. 별도 Weather TestMap에서만 `7 Clear / 8 LightWind / 9 RainStorm`을 바꾸고 Snapshot 강도·spawn·wind에 반응하는 최대 80개/5Hz의 DrawDebug 선분 프리뷰를 표시한다. Rain preview 회귀 1/1 통과, `DroneEditor Win64 Development` 빌드 성공(이 PC UE 5.8.2). 이는 Niagara·젖음 Material·Audio 구현 또는 GPU 최적화 성능 측정이 아니다. 수동 PIE 화면 확인과 정식 VFX는 남아 있으며 Unreal 변경은 로컬, commit/push 안 했다.

2026-09-16 D 드라이브 작업 PC에서 두 저장소를 `fetch --prune`으로 다시 확인했을 때 Mission Rule·재밍·Story Fact·FPV Rate/Acro·기상 Runtime과 기능별 TestMap은 Unreal `962ff02`, 대응 문서는 `3c28611`로 Push 완료됐고 원격 차이는 `0/0`이었다. 그 기준 위에 이번 Shotgun Pellet/Tracer와 Weather TestMap 시각화 작업을 로컬로 진행했다. Commit과 Push는 사용자가 처리한다.

후속 점검에서 Unreal 원격의 `72c964c`, `4a3d4ba`가 추가된 것을 확인했다. 들어오는 변경은 `Content/Drone/Maps/Lvl_MilitaryBase.umap` 하나였고 로컬 수정과 겹치지 않아 `git pull --ff-only`로 `4a3d4ba`까지 반영했다.

같은 날 NPC 전용 후속 감사: 사용자 위임으로 OpenCode `openrouter/stealth/union-alpha`에 NPC 행동 로직 점검/수정을 한 번 요청했다. 관련 코드에서 개인화기 교전 타이머가 MG 재할당 유지 분기와 일반 Controller Tick에서 같은 프레임에 두 번 누적될 수 있는 경로를 찾아, 유지 분기에서 중복 갱신을 제거하고 단위 회귀를 추가했다. 이후 `1초` 유지시간이 매초 행동을 새로 선택하는 구조인지 다시 확인했고, StateTree를 매 Tick/매초 재시작하는 경로는 확인되지 않았다. UE 5.8.2 Editor Build 성공. 집중 자동화 3건 중 타이밍 회귀와 `NPCPerceptionSearchPIE`는 성공했으나 `ShotgunSystemsTestMapPIE`는 정지 pursuit 목표의 MoveTo 요청 수가 예상 2회/실제 3회로 실패했다. 후속으로 실제 활성 `Moving/Paused` 경로일 때만 중복 요청 검사를 적용하도록 진단 getter와 테스트 보강을 추가했으며, 이 보강 뒤 빌드는 성공했지만 Shotgun PIE 재실행은 아직 하지 않았다. 요청 종료 사유를 기록하지 않아 정상 경로 복구인지 중복인지 미확정이며, 임의로 가드를 추가하거나 테스트 기대값을 낮추지 않았다. 사용자 보고 떨림은 화면 재현되지 않아 해결 판정하지 않았고, 저장 AnimBP 전체 그래프/실제 포즈도 확인되지 않았다. 자세한 관측 및 수동 PIE 절차는 [`DRONE_NPC_BEHAVIOR_AUDIT_2026-09-17.md`](docs/ai/DRONE_NPC_BEHAVIOR_AUDIT_2026-09-17.md)에 기록했다. 추가 실행과 커밋/푸시는 하지 않았다.

## 최신 완료 항목

- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest` 경량 시험 맵 생성
- 곡선 Course, CourseSpline과 분리된 Ring Handle 5개, Gate/Sequence 5개 구성
- Recon·Impact·Payload 역할 표적 각 1개와 Carryable 1개 배치
- Gate의 임시 16각 Cube Ring을 Box Trigger 안쪽과 맞는 4변 발광 Frame으로 교체
- Gate `통과 전 / 현재 목표 / 통과 후` 3상태 색상 계약 유지
- 깨지는 역할 표적·Carryable World Text를 기본 숨김 처리하고 선택 표시 문구를 짧게 정리
- 유인 MG 사수 사망 뒤 재할당 재시도, 이동 정체 감시, 재경로와 Greybox 도착 Snap 보강
- 병사 전투 상태에 공통 `Minimum Response State Duration=1.0초`를 추가했다. MG·Cover 이동/사용 태스크가 한 프레임 실패해도 유지시간 동안 현재 예약·감지·사격 행동을 다시 점검하고, 시간이 지난 뒤에도 실패일 때만 다음 상태로 넘어간다. 사망·드론 파괴·Sight Lost 확정 정리는 지연하지 않는다
- 개인화기는 실제 무기 사거리를 벗어나는 즉시 추적을 시작하고, 추적 상태에서는 사거리보다 100cm 안쪽으로 들어와야 사격으로 복귀한다. 따라서 사거리 밖에서 멈추지 않고 NavMesh에 투영한 표적을 계속 추적한다. 전투 시작점 기준 기본 3,000cm 리시 또는 기본 2.5초 무진행 한계를 넘으면 표적을 포기하고 순찰로 복귀하며, 같은 투영 목적지는 기본 150cm 이상 바뀔 때만 갱신한다
- NPC 이동 중에는 Character Movement 한 곳만 몸 Yaw를 쓰고 정지 사격·Cover에서만 개인화기 Yaw 보간을 사용한다. 리시 포기 후 StateTree 재시작은 다음 Tick으로 예약해 `StartTree` 재진입을 막는다. 리시·재경로 거리/주기·무진행·Cooldown 값은 Controller Blueprint에서 조정 가능하다
- Smart Object 동선·배치 팀 가이드, LFS 용량 계획, 외부 도구 검토와 추천도서 학습 계획 작성
- Truck 직선 Greybox와 향후 Mission Spline Route, Smart Object 최근접 Slot 동선을 구분한 팀 설계·인계 가이드 작성. 현재 차량 Spline 추종과 목적지 Event는 문서화된 후속 구현이며 완료 기능으로 판정하지 않음
- Smart Object Greybox 차량의 실제 `SM_SpikeStorm_Tire2_FR`이 Cylinder 가정의 Mesh 로컬 Z축으로 회전해 옆으로 빙글도는 결함을 재현하고, Mesh 장착 회전과 무관한 차량 부모 공간 `+Y` 차축 회전으로 교정. 축은 Blueprint `Wheel Visual Spin Axis In Vehicle Space`에서 조정 가능
- 같은 실제 Tire의 약 50cm 시각 반지름에 `Wheel Radius=30cm`를 사용해 바닥 아래로 약 20cm 잠기던 결함을 독립 평면에서 재현. 차량 BP 기본값을 52cm로 올리고 Blueprint 허용 범위를 1~500cm로 확장, Tire Bounds·지면 접촉 Red→Green과 맵 Validate 통과
- Mission Definition에 순서형 목표 Rule(사건 종류·필요 수량·선택적 제한 시간·Actor Tag 대상 ID) 추가. 기존 문구형 목표는 fallback 유지
- Director에 Scan·의도된 Payload 적중·Health 대상 사망 Event, 목표별 시간 만료 실패, Actor 중복 방지와 Snapshot/HUD 진행값 연결
- Blueprint 배치형 `DroneMissionReturnZone`을 추가해 플레이어 Drone Overlap을 귀환 Event로 보고하도록 준비
- 저장 `DA_Mission_Tutorial_Training`의 기존 한 Lap 목표를 `Training Lap` Rule로 이행. 팀원 Training Map은 미수정
- 배치형 `DroneJammingVolume`과 Pawn의 `DroneSignalComponent` 추가. 겹치는 방해 Source 중 최대 강도로 단계·신호율 계산, 강한 단계에서 기본 비행 튜닝값의 속도·가속도 배율 적용/복원
- Flight HUD 신호율·단계 경고, Blueprint 영상 노이즈 강도 Event 추가. 실제 화면 Noise Material·목표 정보 숨김은 미구현
- Director에 `Jamming Exited`, `Jammer Disabled` Rule Event 연결. 자동화 Editor World에서 BP Delegate 구독이 진행되지 않아 게임 규칙 연결은 C++ Event로 분리하고 BP Delegate는 연출용으로 유지
- Figma `Project:Droner`를 읽기 전용으로 확인해 Tutorial + 4개 Story Mission, 역할 Drone과 UI 흐름을 현재 코드에 대조. 원본은 미수정
- Mission 성공이 남기는 `StoryFactsGrantedOnSuccess/RemovedOnSuccess`와 목표의 `Always/FactPresent/FactAbsent` 조건 추가. 미끼 차량→Mission 3 표적 처리와 실제 탑승 차량→Mission 3 처리 생략을 모두 데이터로 선택 가능
- `JammingImmunity`가 실제 구현 Capability인 Drone만 활성 Zone의 재밍 영향을 무시하도록 Signal/Pawn 연결. 기존 세 Drone에는 면역을 임의 부여하지 않음
- `Lvl_NPCSmartObjectGreybox`를 Unreal AssetTools로 `/Game/Drone/Maps/TestMap` 아래 이동하고 코드·생성 도구의 고정 경로 갱신
- `/Game/Drone/Maps/TestMap/Lvl_DroneMissionSystemsTest` 생성. 35%/80% 겹침 Jammer, Return Zone, 역할 표적 3종, Carryable과 위치 표식 배치
- `/Game/Drone/Maps/TestMap/Lvl_DroneShotgunSystemsTest` 생성. 기존 AI 맵을 바꾸지 않고 추가 Hostile Shotgun NPC 1명, 약 9m 시작 거리, 5/10/15m 표식과 LOS 차단벽 배치
- 기본 Projectile Shotgun에서도 Cyan 예상 비행선 8개를 표시하고 Blueprint에서 표시 On/Off와 직전 Pellet 끝점 배열을 조회할 수 있게 보강
- Shotgun은 실제 8 Projectile·12° 독립 확산, Pellet당 3 피해를 사용한다. 같은 발사자의 Projectile끼리 Sweep 충돌을 무시해 같은 총구에서 생성된 Pellet이 서로 제거되지 않으며, Cyan 예상선은 기본 Off다. 전용 BP에는 주황 Emissive `0.04` 비드와 `0.20 × 0.0125` Tracer가 적용돼 있다
- Rifle·유인 MG·무인 포탑의 공용 Projectile 기본 외형을 주황 Emissive 탄두 `0.06`과 Tracer `0.60 × 0.018`로 확대했다. Shotgun 전용 BP Scale은 유지한다
- Shotgun/Rifle 개인화기 몸 Yaw를 `3° 정지 / 6° 시작` Hysteresis로 바꾸고 Bone Gaze는 작은 잔여 오차를 계속 보간한다. 경계 Snap 없이 몸과 고개의 왕복을 억제하며 정지각·Hysteresis·기본 `180°/s` 몸 회전속도는 BP Profile에서 역할별 조정 가능하다
- 첨부 와이어프레임을 기준으로 C++ 임시 Front-end를 `작전 목록 / 선택 작전 / 작전 개요`, 기체 선택을 `보유 기체 / 상세 / 조작 설정` 3열 레이아웃으로 갱신했다. Flow와 Data Asset은 기존 계약을 재사용하며 최종 WBP Designer·Thumbnail/영상은 아직 별도 작업이다
- 세 번째 `FPV Rate/Acro` 조작 모드 추가. Pitch/Roll/Yaw를 Body 각속도로 해석하고 Stick 중앙에서 자동 수평 복귀하지 않아 Roll/Loop 가능
- Rate/Acro의 공용 Action 재해석을 제거하고 전용 Axis1D Action 4개를 추가했다. 키보드는 `W/S Pitch`, `A/D Roll`, `Q/E Yaw`, `Space/Ctrl Throttle`, Gamepad는 기존 Mode 2를 유지해 W/S와 고도 입력 중복 및 키보드 Pitch 누락을 해소했다
- FPV Data Asset 기본값을 Rate/Acro+고기동으로 변경. 공개 민간 FPV 참고선으로 수평 27m/s, 수직 9m/s, Pitch/Roll 650°/s, Yaw 400°/s를 조정 가능하게 저장
- Rate/Acro에 중력, 중립 호버, 기체 Up 방향 추력, 속도 비례 항력, Body Rate 응답 시간을 연결했다. `Space/Ctrl`은 호버 기준 추력 증감이고 W/S Pitch로 기울인 Up 축이 실제 전후 추진력을 만든다. 호버 스로틀·중력·항력·Rate 응답은 FPV Data Asset/Blueprint에서 조정 가능하다
- `UDroneWeatherProfile`, `FDroneWeatherSnapshot`, `UDroneWeatherWorldSubsystem`, 배치형 `ADroneWeatherController` 구현. Profile 기본 10Hz로 결정적 지속풍·돌풍·전환값을 공급
- 모든 Prototype Drone에 `UDroneWeatherResponseComponent`를 부착. 쉬운 조작 65%·제한 자세 25%·Rate/Acro 0% 기본 보정과 Sweep Drift 적용. 최종 물리가 아닌 `UFloatingPawnMovement` Greybox
- `/Game/Drone/Data/Weather`에 `Clear`, `LightWind`, `RainStorm_Greybox` Profile 3종 생성
- `/Game/Drone/Maps/TestMap/Lvl_DroneWeatherSystemsTest` 생성. LightWind Controller 1개·35° 풍향 화살표·Prototype GameMode, Map Check 0/0
- Weather TestMap에 `/Game/Drone/Weather/Blueprints/BP_DroneWeatherDebugVisualizer`를 배치했다. 24개 흐름 Bead, 현재 Profile/풍속/풍향/조작 모드 화면 표시와 `1 Easy / 2 Manual / 3 Rate-Acro` 비교 키를 제공한다
- 돌풍에 Attack/Release/풍향 응답 시간을 분리하고 최단각 풍향 보간을 적용했다. Debug Bead는 표시 속도를 부드럽게 따라간 뒤 벡터 적분하므로 풍향 변경 때 과거 누적 거리를 새 방향으로 재투영하지 않으며, 풍속에 따라 방향과 길이가 바뀐다
- 비 Snapshot·최적화/품질 계획은 준비됐지만 Camera-follow Niagara, MPC Wetness, Audio, 실내 감쇠 표현은 아직 미구현

## 검증된 근거

- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공
- TestMap Map Check `0 errors / 0 warnings`
- `Drone.Tutorial.TrainingGateSequence` 1/1 성공
- `Drone.Tutorial.TutorialSystemsTestMap` 1/1 성공
- `Drone.AI.NPCPerceptionSearchPIE` 단독 새 PIE 3회 성공
- 상태 안정화 계약 추가 전 Reflection 자동화가 새 설정 누락으로 Red가 된 뒤, 구현 후 `SmartObjectFoundationDefaults`, `HostilePatrolStateTreeAsset`, `GroundConformingSuspension`이 Success로 전환했고 최종 Editor Build도 성공했다
- 이전 9월 15일 작업 종료 시 Unreal·문서 `git diff --check`, Unreal `git lfs fsck` 통과. 9월 16일 기능 변경의 최종 검사 결과는 아래에 따로 기록
- 이 PC에서 최신 Source로 `DroneEditor Win64 Development` 재빌드 성공
- TestMap Validate/Map Check `0 errors / 0 warnings`, rings=5/targets=3/carryable=1
- 최종 단독 Commandline 회귀: `Drone.Mission.ObjectiveRules`, `Drone.Flow.Contract`, `Drone.Flow.MissionEntryContract`, `Drone.Tutorial.TrainingGateSequence`, `Drone.Tutorial.TutorialSystemsTestMap` 5/5 성공
- 2026-09-16 `DroneEditor Win64 Development` 전체 재빌드 성공. 양쪽 Story 분기와 재밍 면역을 포함한 Flow/Mission/Prototype/Signal/Tutorial/UI 회귀 8/8 Success·Exit 0
- 시험 맵 이동/추가 후 `DroneEditor Win64 Development` 재빌드 성공, Mission Systems Map Check `0 errors / 0 warnings`
- 이동된 AI 맵 Asset·PIE·감지/수색, 새 Mission Systems 맵, Mission Rule, Signal Stage 최종 회귀 6/6 Success·경고 0
- 자동포탑/지면 추종 차량 배치 도구를 새 AI 맵 경로에서 Validate-only 실행해 설치형 1·차량형 1·Attach·4점 Suspension·노면 5개 확인
- Shotgun Systems 맵 Map Check `0 errors / 0 warnings`; 발광 Material/실제 Pellet BP·정면 시선 안정화 포함 전용 Asset/PIE 자동화 `2/2 Success`
- Shotgun 가시성 변경 전 자동화가 피해 8·Tracer 없음·큰 탄두를 의도대로 실패한 뒤, 변경 후 전용 Asset/PIE `2/2`와 `NPCGreyboxAssets`, `WeaponContract`, `ProjectileBallistics`, `ShotgunTrace` 집중 회귀가 모두 성공
- 전체 샷건 묶음 `WeaponContract`, `ShotgunTrace`, `ProjectileBallistics`, 전용 Map/PIE `5/5 Success`, 실패 0. 기존 두 단위 테스트의 Recast 경고만 존재하며 샷건 기능 실패는 아님
- 3° 시선/최소 상태 유지 구현 직후 `NPCPerceptionSearchPIE`에서 재점유 제한시간 실패가 재현됐던 이력은 보존한다. 2026-09-17 추적·테스트 격리와 StateTree 재진입 수정 뒤 같은 테스트가 감지→MG 경합→개인화기 대체→사수 사망 후 재점유→Lost/Search→순찰 복귀까지 `1/1 Success`로 전환됐다
- 2026-09-17 후속 화면 피드백으로 `사거리 안인데도 계속 접근`과 추적 중 몸·고개가 이동과 반대로 도는 Red를 재현했다. 최종 규칙은 실제 무기와 같은 3D 사거리 안이면 즉시 정지·사격, 밖 판정이 0.2초 지속될 때만 Pursue다. 추적 몸 Yaw와 Bone Gaze는 실제 수평 이동 벡터를 함께 따르며, 역할 BP가 덮은 이동 회전 플래그도 BeginPlay에서 공통 계약으로 복구한다. Editor Build와 `PersonalWeaponEngagementPolicy`, `SmartObjectFoundationDefaults`, 경계 흔들림·이동/시선 정렬·사거리 진입 정지를 포함한 `ShotgunSystemsTestMapPIE`, `NPCPerceptionSearchPIE`, `NPCGreyboxAssets` 최종 `5/5 Success`
- 기존 Smart Object 맵의 NPC 수·역할이 유지되는지 `Drone.AI.NPCGreyboxAssets`를 별도 재실행해 `1/1 Success`, 경고 0 확인
- FPV Rate/Acro 추가 후 `DroneEditor Win64 Development` Build 성공. `Drone.Prototype.FlightProfiles`, `Drone.Prototype.PIEInputLifecycle`, `Drone.Flow.MissionEntryContract`, `Drone.Flow.MissionEntryPIE`, `Drone.Prototype.RoleAbilities` 5/5 Success·Exit 0
- 기상 Runtime 추가 후 `DroneEditor Win64 Development` Build 성공. `Drone.Weather.ProfileAndWindContract`, `Drone.Weather.ProfileAssets`, `Drone.Weather.SystemsTestMap` 3/3 Success·Exit 0
- Weather TestMap Python 저장 검증과 Map Check `0 errors / 0 warnings`, `Drone.Prototype.PawnDefaults` 회귀 Success·Exit 0
- Weather 시각화 추가 전 저장 계약이 Visualizer `0개`로 의도대로 실패한 뒤, BP Visualizer 1개·Bead 24개·화면 Readout·모드 키 계약의 `Drone.Weather.SystemsTestMap` 성공
- Acro 입력 계약은 전용 Action 4개가 없는 기존 상태에서 의도한 Red를 확인한 뒤, IMC 33 Mapping·BP 연결과 Pawn 전용 분기로 Green 전환했다. MSVC 14.51.36257 Editor Build 및 `Drone.Prototype` 8/8 Success
- Acro 추력 연결 전 `Nose-down Acro attitude creates forward thrust`가 의도대로 실패한 뒤 중력·호버·추력·항력·Rate 응답 구현으로 Green 전환했다. 최종 Editor Build, `Drone.Prototype` 8/8 Success·실패 0
- WTH-02B 벡터 적분·돌풍 응답 구현 뒤 `Drone.Weather` 3/3 Success·실패 0. 방향 변경 시 이전 X 이동을 보존한 채 Y 이동이 누적되고, 고정 속도 적분은 Frame Step과 무관함을 자동화했다
- `962ff02`와 대응 문서 Push 전 Unreal·문서 `git diff --check` 모두 종료 코드 0. LF→CRLF 메시지는 줄바꿈 안내이며 공백 오류가 아니다

## 아직 확인하지 않은 항목

- TestMap Gate Frame 외형과 Trigger 정합, 3상태 색
- Ring Handle 개별 이동과 Spline 투영 체감
- 한 Lap HUD 갱신과 두 Lap 이전 평균·Best·증감값
- 역할 표적 3종, Carryable 픽업·드랍과 숨긴 World Text
- 이동된 AI 시험 맵의 MG 재점유·도착 방향·Gaze·자동포탑·차량 화면 확인
- Rifle/Shotgun 병사가 사거리 밖에서 Drone을 자연스럽게 추적하고, 이동 중 좌우 떨림 없이 이동 방향을 보며, 리시 밖에서는 포기·순찰 복귀하는지 화면 확인
- 병사 감지 후 최소 1초 안에 Cover/MG/개인화기 상태가 프레임 단위로 왕복하지 않고 현재 행동을 유지하는지 화면 확인
- Drone Rotor 축·방향·속도, 비행 기울기, 실제 탄환 피격 흔들림 등 기존 수동 회귀
- 새 TestMap의 귀환 Zone 위치/크기와 재밍 Zone Overlap·신호 경고·강한 단계 이동 체감 수동 확인
- Shotgun Systems 맵의 발광 Pellet 8개와 짧은 Tracer 분리 가시성, Cyan 선이 보이지 않는지, 이동 회피 체감, 최대 24 피해, 16m 사거리·LOS와 Hysteresis 고개 안정화 화면 확인
- `Lvl_DroneFrontEnd`의 새 3열 Mission UI와 Training 진입 뒤 3열 Drone 선택 UI가 해상도에서 잘리지 않는지 수동 확인
- FPV Rate/Acro에서 키보드 `W/S Pitch`, `A/D Roll`, `Q/E Yaw`, `Space/Ctrl Throttle` 중복 없음과 Gamepad/RC Mode 2, Stick 중앙 자세 유지, Roll/Loop·27m/s 체감 수동 확인
- 현재 Rate/Acro는 중력·호버 추력·기체 Up 추진·선형 항력·Rate 응답을 계산하지만 `UFloatingPawnMovement` 기반 v1이다. 모터별 RPM·PID·질량/관성 텐서·프로펠러 공력 기반 완전 물리와 같은지 확인한 상태는 아님
- Weather TestMap에서 움직이는 Bead·화면 풍속/풍향이 실제 Drift와 맞는지, `1/2/3`으로 쉬운 조작/제한 자세/Rate-Acro 보정 차이가 구분되는지 수동 확인
- 개선된 Debug Bead의 풍향 전환 궤적·길이 변화와 LightWind/RainStorm Attack·Release 체감은 자동화만 완료했고 실제 화면 확인이 남았다
- Camera-follow Niagara Rain, 젖음 MPC, Audio, 실내 감쇠와 Low~Epic 성능 측정은 미구현
- Test Mission DA/진입 경로에서 Return/Jammer Mission Event, 역할 Event 연쇄, 제한 시간 만료 화면 확인
- 영상 노이즈 WBP 연출과 목표 정보 손실 표현 확인
- Figma에서 `골든 타임/인터셉트/베일 브레이커/엔드게임`과 큰 목표는 확인했지만 실제 Story Mission DA/Map은 아직 없음
- 같은 Figma 파일에서 Mission 2 차량이 미끼라는 전체 설명과 탑승 차량으로 전제한 개별 화면, Mission 3에서 오마르를 처리하는 설명과 이미 처리됐다는 대사가 충돌함. 코드는 양쪽을 지원하며 저장 기본안은 사용자 결정 대기
- 광섬유 Drone·UGV·장거리 타격 Drone의 플레이 Definition/Pawn, Mission 중 기체 교대, 차량 목적지 실패 Trigger, 최종 Cinematic 연결은 미구현

## 알려진 실패와 경계

- `TrainingAssets`, `TrainingPIESmoke` 실패는 팀원이 제작 중인 실제 Training 맵의 Gate/Sequence와 역할 Actor 중간 상태를 보여준다. Codex가 원본 맵을 수정해 억지로 통과시키지 않는다.
- `NPCBaseRoutinesPIE`는 느린 Headless 묶음에서 두 번째 순찰을 제한 시간 안에 끝내지 못하는 간헐성이 있다. MG 재점유 결함과 분리해 추적한다.
- 유인 NPC 점유 포탑은 `BP_SO_MGTurret` 한 개다. `BP_AutoTurret_Vehicle`, `BP_AutoTurret_Emplaced`는 무인 자동포탑이다.
- 모든 `.uasset`, `.umap`은 크기와 무관하게 Git LFS 대상이다. Threshold 방식으로 일반 Git에 옮기지 않는다.
- 이 PC의 첫 TestMap Validate 실패는 9월 8일 생성 DLL이 9월 15일 Source보다 오래되어 역할 표적 BP의 C++ 부모를 못 읽은 문제였다. 최신 Editor Build 후 같은 비파괴 Validate가 성공했고 맵 Actor 삭제/재구성은 하지 않았다.

다음 행동과 완료 조건은 [`WORKBOARD.md`](WORKBOARD.md), 상세 문서 위치는 [`docs/README.md`](docs/README.md), 과거 근거는 [`docs/history/DRONE_WORKLOG.md`](docs/history/DRONE_WORKLOG.md)를 따른다.
