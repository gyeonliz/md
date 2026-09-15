# 현재 작업 상태

기준일: 2026-09-16 (Asia/Seoul)

## 한눈에 보기

- 현재 단계: AI/Mission/Signal/Shotgun TestMap, FPV Rate/Acro, 기상 Profile·지속풍/돌풍 Vertical Slice 구현 완료. 화면 체감 확인과 비 표현·실제 Mission Flow PIE·Story 맵 통합 대기
- 바로 다음 개발: Weather TestMap 바람 체감 확인 → Camera-follow Niagara Rain/MPC/Audio → Test Mission DA/진입 경로로 Return·Jammer Event 실제 PIE
- Unreal Editor: 마지막 확인 시 종료 상태
- Production Training: 팀원이 실제 Tutorial 환경을 제작 중이므로 열람 외 저장·덮어쓰기·자동 재구성 금지

## Git 기준

| 저장소 | 현재 기준 | 상태 |
|---|---|---|
| Unreal `C:\URproject\drone` | `main = origin/main = 8b9b2a8` | Mission Source·Training Mission Data Asset·시험 도구 로컬 수정, Stash 없음 |
| 문서 `C:\Users\jkw11\Documents\Codex\2026-08-19\codex-gpt-chatgpt-codex-1-6` | `main = origin/main = 3e89e43` | 상태·보드·가이드 등 로컬 수정, Stash 없음 |

2026-09-15 `origin` 재조회 기준으로 두 저장소의 HEAD는 원격과 일치했다. 그 후 아래 Mission·재밍·시험 맵 작업을 로컬에서 진행했으며 Commit·Push하지 않았다. 현재 원격 서버의 추가 변경은 다시 조회하지 않았다. 팀원 Training 맵은 변경하지 않았고 TestMap에는 AI 맵 이동본, Mission Systems 맵, Shotgun Systems 맵이 추가됐다. 이전 GitHub Desktop 자동 Stash 두 개는 이미 정리된 상태다.

## 최신 완료 항목

- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest` 경량 시험 맵 생성
- 곡선 Course, CourseSpline과 분리된 Ring Handle 5개, Gate/Sequence 5개 구성
- Recon·Impact·Payload 역할 표적 각 1개와 Carryable 1개 배치
- Gate의 임시 16각 Cube Ring을 Box Trigger 안쪽과 맞는 4변 발광 Frame으로 교체
- Gate `통과 전 / 현재 목표 / 통과 후` 3상태 색상 계약 유지
- 깨지는 역할 표적·Carryable World Text를 기본 숨김 처리하고 선택 표시 문구를 짧게 정리
- 유인 MG 사수 사망 뒤 재할당 재시도, 이동 정체 감시, 재경로와 Greybox 도착 Snap 보강
- Smart Object 동선·배치 팀 가이드, LFS 용량 계획, 외부 도구 검토와 추천도서 학습 계획 작성
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
- 세 번째 `FPV Rate/Acro` 조작 모드 추가. Pitch/Roll/Yaw를 Body 각속도로 해석하고 Stick 중앙에서 자동 수평 복귀하지 않아 Roll/Loop 가능
- FPV Data Asset 기본값을 Rate/Acro+고기동으로 변경. 공개 민간 FPV 참고선으로 수평 27m/s, 수직 9m/s, Pitch/Roll 650°/s, Yaw 400°/s를 조정 가능하게 저장
- `UDroneWeatherProfile`, `FDroneWeatherSnapshot`, `UDroneWeatherWorldSubsystem`, 배치형 `ADroneWeatherController` 구현. Profile 기본 10Hz로 결정적 지속풍·돌풍·전환값을 공급
- 모든 Prototype Drone에 `UDroneWeatherResponseComponent`를 부착. 쉬운 조작 65%·제한 자세 25%·Rate/Acro 0% 기본 보정과 Sweep Drift 적용. 최종 물리가 아닌 `UFloatingPawnMovement` Greybox
- `/Game/Drone/Data/Weather`에 `Clear`, `LightWind`, `RainStorm_Greybox` Profile 3종 생성
- `/Game/Drone/Maps/TestMap/Lvl_DroneWeatherSystemsTest` 생성. LightWind Controller 1개·35° 풍향 화살표·Prototype GameMode, Map Check 0/0
- 비 Snapshot·최적화/품질 계획은 준비됐지만 Camera-follow Niagara, MPC Wetness, Audio, 실내 감쇠 표현은 아직 미구현

## 검증된 근거

- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공
- TestMap Map Check `0 errors / 0 warnings`
- `Drone.Tutorial.TrainingGateSequence` 1/1 성공
- `Drone.Tutorial.TutorialSystemsTestMap` 1/1 성공
- `Drone.AI.NPCPerceptionSearchPIE` 단독 새 PIE 3회 성공
- 이전 9월 15일 작업 종료 시 Unreal·문서 `git diff --check`, Unreal `git lfs fsck` 통과. 이번 로컬 작업의 최종 검사 결과는 아래에 따로 기록
- 이 PC에서 최신 Source로 `DroneEditor Win64 Development` 재빌드 성공
- TestMap Validate/Map Check `0 errors / 0 warnings`, rings=5/targets=3/carryable=1
- 최종 단독 Commandline 회귀: `Drone.Mission.ObjectiveRules`, `Drone.Flow.Contract`, `Drone.Flow.MissionEntryContract`, `Drone.Tutorial.TrainingGateSequence`, `Drone.Tutorial.TutorialSystemsTestMap` 5/5 성공
- 2026-09-16 `DroneEditor Win64 Development` 전체 재빌드 성공. 양쪽 Story 분기와 재밍 면역을 포함한 Flow/Mission/Prototype/Signal/Tutorial/UI 회귀 8/8 Success·Exit 0
- 시험 맵 이동/추가 후 `DroneEditor Win64 Development` 재빌드 성공, Mission Systems Map Check `0 errors / 0 warnings`
- 이동된 AI 맵 Asset·PIE·감지/수색, 새 Mission Systems 맵, Mission Rule, Signal Stage 최종 회귀 6/6 Success·경고 0
- 자동포탑/지면 추종 차량 배치 도구를 새 AI 맵 경로에서 Validate-only 실행해 설치형 1·차량형 1·Attach·4점 Suspension·노면 5개 확인
- Shotgun Systems 맵 Map Check `0 errors / 0 warnings`; 전용 Asset/PIE 자동화 `2/2 Success`, 경고 0
- 전체 샷건 묶음 `WeaponContract`, `ShotgunTrace`, `ProjectileBallistics`, 전용 Map/PIE `5/5 Success`, 실패 0. 기존 두 단위 테스트의 Recast 경고만 존재하며 샷건 기능 실패는 아님
- 기존 Smart Object 맵의 NPC 수·역할이 유지되는지 `Drone.AI.NPCGreyboxAssets`를 별도 재실행해 `1/1 Success`, 경고 0 확인
- FPV Rate/Acro 추가 후 `DroneEditor Win64 Development` Build 성공. `Drone.Prototype.FlightProfiles`, `Drone.Prototype.PIEInputLifecycle`, `Drone.Flow.MissionEntryContract`, `Drone.Flow.MissionEntryPIE`, `Drone.Prototype.RoleAbilities` 5/5 Success·Exit 0
- 기상 Runtime 추가 후 `DroneEditor Win64 Development` Build 성공. `Drone.Weather.ProfileAndWindContract`, `Drone.Weather.ProfileAssets`, `Drone.Weather.SystemsTestMap` 3/3 Success·Exit 0
- Weather TestMap Python 저장 검증과 Map Check `0 errors / 0 warnings`, `Drone.Prototype.PawnDefaults` 회귀 Success·Exit 0
- 이번 로컬 작업의 Unreal·문서 `git diff --check` 모두 종료 코드 0. LF→CRLF 메시지는 줄바꿈 안내이며 공백 오류가 아니다

## 아직 확인하지 않은 항목

- TestMap Gate Frame 외형과 Trigger 정합, 3상태 색
- Ring Handle 개별 이동과 Spline 투영 체감
- 한 Lap HUD 갱신과 두 Lap 이전 평균·Best·증감값
- 역할 표적 3종, Carryable 픽업·드랍과 숨긴 World Text
- 이동된 AI 시험 맵의 MG 재점유·도착 방향·Gaze·자동포탑·차량 화면 확인
- Drone Rotor 축·방향·속도, 비행 기울기, 실제 탄환 피격 흔들림 등 기존 수동 회귀
- 새 TestMap의 귀환 Zone 위치/크기와 재밍 Zone Overlap·신호 경고·강한 단계 이동 체감 수동 확인
- Shotgun Systems 맵의 Cyan Pellet 선, 이동 회피 체감, 여러 Pellet 피격 피해, 16m 사거리 경계와 LOS 차단 화면 확인
- FPV Rate/Acro에서 Gamepad/RC Controller Mode 2 축, Stick 중앙 자세 유지, 90° 이상 Roll/Loop, Local Up Throttle, 27m/s 체감 수동 확인
- 현재 Rate/Acro는 `UFloatingPawnMovement` Greybox이므로 모터별 RPM·PID·중력/양력·공기저항 기반 완전 물리와 같은지 확인한 상태가 아님
- Weather TestMap에서 쉬운 조작/Rate-Acro Drift 차이, 순풍·역풍·횡풍, 돌풍 세기 수동 확인
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
