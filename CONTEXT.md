# Drone 작업 기준

이 문서는 다음 작업자가 반드시 지켜야 할 현재 경계만 보존한다. 구현 현황은 [`STATUS.md`](STATUS.md), 실행 순서는 [`WORKBOARD.md`](WORKBOARD.md)를 먼저 확인한다.

## 작업 위치

- 2026-10-01 현재 C 드라이브 PC Unreal: `C:\URproject\drone`
- 현재 PC 문서: `C:\Users\jkw11\Documents\Codex\2026-08-19\codex-gpt-chatgpt-codex-1-6`
- 이전 D 드라이브 PC의 경로는 Unreal `D:\JGY\project\drone`, 문서 `D:\JGY\project\md`다. 현재 PC에는 해당 D 경로가 없다. PC마다 실제 경로를 확인하고 다른 PC의 절대 경로를 실행 명령에 그대로 복사하지 않는다.
- 새 생산 코드: `Source/Drone`
- 새 프로젝트 소유 자산: `/Game/Drone`

## 맵 소유권

- 최신 검증 기준은 [STATUS](STATUS.md)의 날짜·PC·검증 근거 표다. 상세 수동 절차는 [비행 물리·OilRig 비·UI·독립 미션 가이드](docs/gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md)를 참고한다. Acro는 현실 요소를 반영한 근사 모델이며 실기체 검증 완료라고 표현하지 않는다.
- `/Game/Drone/Maps/TestMap/Tutorial/Lvl_Tutorial_*_Test`: 수업 8개 독립 시험맵. 해당 DA MissionMap과 Default Mission Entry가 연결됐다. 기존 공유 시험맵은 보존한다.
- `/Game/Drone/Maps/TestMap/Lvl_OilRigRainComparisonTest`: 원본/비 끔/근거리 원본/프로젝트 비 A/B 비교용이다. `Lvl_OilRigPreview`와 ThirdParty Niagara 원본에 실험 세팅을 저장하지 않는다.

- `/Game/Drone/Maps/Lvl_DroneTraining`: 팀원이 실제 Tutorial 환경을 제작하는 Production 맵이다. 합의 전 저장·덮어쓰기·자동 재구성·분할·이동을 금지한다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest`: Course, Gate, 역할 기능과 HUD를 자유롭게 검증하는 경량 시험 맵이다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneTrainingRouteSelectionTest`: Route 4개를 편집하고 Play 중 `1~4` 고정 선택·`5` 무작위 선택을 검증하는 독립 시험 맵이다. Production Training과 분리한다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialMissionTest`: 초기 8개 Station을 보존한 평면 종합 Greybox 시험장이다. 현재 수업별 DA 진입은 위 `TestMap/Tutorial` 독립 맵이며 이 공유 맵과 구분한다. Orbit은 원형 코스 한 바퀴이고 Heading DA ID만 호환용으로 유지한다. 공유 맵 생성 도구는 `DroneTutorialMissionTest.Owned` Tag Actor만 관리한다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneRacingTest`: 로비 Racing 탭의 독립 원형 완주/시간 기록 시험맵. Best Lap은 조건별 JSON 영구 저장 구현·자동 검증됨(실제 랩 재실행 복원은 수동 확인 대기). 정식 경기 규칙은 현재 미정. 튜토리얼 수업별 시험맵은 사용자 후속 요청으로 분리 완료했으며 Production 맵 분할과는 구분한다.
- `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`: NPC·Smart Object·유인/무인 포탑·차량 전용 시험 맵이다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneMissionSystemsTest`: 재밍·귀환·역할 Event 배치 전용 시험 맵이다. 직접 실행은 Prototype Flow이므로 Mission 완료 판정은 후속 Test Mission 진입에서 확인한다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneShotgunSystemsTest`: 기존 AI 맵의 순찰·MG 경합을 건드리지 않고 추가 Shotgun NPC의 감지·실제 8개 산탄 Projectile·탄약을 보는 독립 시험 맵이다. 작은 탄두/Tracer 교체 지점은 `/Game/Drone/AI/Blueprints/Projectiles/BP_ShotgunPelletProjectile`이다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneWeatherSystemsTest`: LightWind 지속풍·돌풍, 조작 모드별 보정, RainStorm과 실내 감쇠 전용 맵이다. 이동 Bead·화면 수치·조작 키와 DrawDebug 비 선분은 TestMap 판독용이고, `BP_DroneRainVisual`은 카메라 추종 Instanced Mesh Greybox다. 정식 Niagara GPU Rain으로 표현하지 않는다.
- `test1`, `test2`: 용도를 확인하기 전 이동하거나 이름을 바꾸지 않는다.
- 자산 이동은 파일 탐색기가 아니라 Unreal AssetTools로 수행하고 Redirector·Soft Reference·하드코딩 경로를 검증한다.

## 게임 흐름

확정 흐름은 `게임 실행 → 시작 트레일러 → 로비 → 미션 선택/설명 → 시작 → 미션 트레일러 → 맵 진입 → 드론 선택 → 미션 시작/목표 UI`다.

2026-10-01 후속 UI 기획안: 시작 화면의 `시작`은 Story Mission 목록, `훈련`은 Tutorial/Racing 내부 탭으로 분리한다. 기존 `Title_Asset` 이미지와 DA/맵을 보존하며 목록/선택 카드/설명·하단 시작, 기체 상단 상세/하단 가로 카드 임시 화면을 사용한다. WBP Artwork와 DA Thumbnail에서 이미지를 교체한다. Settings는 Master 음량·화면·품질·VSync·FPS를 적용/저장하고 미적용 변경은 취소한다. PIE에서 창/해상도 변경은 금지한다. 최종 영상·3D 기체 Preview·개별 음원 라우팅은 별도다. 사용자의 회전 수업 정의는 특정 방향 바라보기가 아니라 원형 코스 비행이며 스틱 Mode 1/2와 비행 제어/물리 모델을 혼동하지 않는다.

10/03 회의로 타이틀 스토리/레이싱/튜토리얼/설정/종료 5메뉴·분류 직접 진입 확정(위 10/01 시작/훈련 기획안은 대체됨). 로비 탭·LB/RB 최종 유지 여부는 현재 미정.

사람 Operator 직접 조작, NPC 대화로 임무 수령, 플레이어와 Drone 간 실시간 화면 전환 기획은 폐기했다. NPC·Smart Object·전투 기능은 Mission 내부 요소로 유지한다.

2026-09-16 Figma 읽기 전용 확인 기준 Story 화면은 `골든 타임/인터셉트/베일 브레이커/엔드게임` 4개다. 이후 Story DA·독립 TestMap 4개와 전달/차량 요격·목적지 실패/재밍 이탈/UGV 표적·귀환 시험을 구현했다. 최종 제작 맵·선택 목표·미션 중 기체 교대·장거리 타격·영상은 후속이며 시험 구현을 스토리 완성으로 판정하지 않는다. Mission 2 차량이 미끼인지 실제 표적 탑승인지 Figma 내부 문구가 충돌하므로 코드는 양쪽 Story Fact를 지원하고 기본안은 사용자 결정 전 확정하지 않는다. Figma 원본은 수정하지 않는다. Android 개발은 현재 범위가 아니다.

## 구현 책임

- C++: 상태, 규칙, 기능, 테스트와 안정적인 공개 계약
- Blueprint/Data Asset: Mesh·Material·색·속도·거리·시간·임계값·자산 연결과 Greybox 조정
- Collision Root와 Visual Mesh는 분리한다.
- 나중에 조정할 수치는 가능하면 `EditDefaultsOnly` 또는 `EditAnywhere`와 명확한 Category로 Blueprint에 노출한다.
- ThirdPerson·Combat·Platforming·SideScrolling은 Legacy 참고용이며 신규 생산 코드와 자산에서 상속·참조하지 않는다.

## 현재 조작·역할 기준

- `Assisted Easy`는 Actor-relative 수평 이동·World Up 고도, `Manual Realistic Greybox`는 제한 자세·Local Up, Rate/Acro Mode 1·2는 Pitch/Roll/Yaw Body 각속도·자동 수평 복귀 없음으로 분리한다.
- 느림/보통/빠름 속도 선택은 제거한다. 각 기체의 기존 빠름 수준을 단일 무적재 기준으로 사용하고 Legacy `Stable/Balanced/Agile` 이름은 Asset 직렬화 호환용으로만 유지한다.
- Mode 1/2는 RC 송신기 축 배치만 다르며 같은 Dry Mass·합산 최대 추력·모터 응답·중력·Body Up 추력·선형/제곱 항력·Body Rate 응답을 사용한다. 기반은 `UFloatingPawnMovement`이고 비행 컨트롤러 PID·모터 믹싱·프로펠러 유동·관성 텐서를 1:1 해석한다고 표현하지 않는다.
- Drop Drone은 내장 화물 또는 실제 부착 Payload Actor의 kg 질량을 총질량에 더한다. 적재 시 최고속도·가속·감속·Yaw·추력 대비 중량 여유가 줄고, 투하하면 즉시 무적재 성능으로 복구한다. 질량과 기체 물리값은 Blueprint/Data Asset에서 조정한다.
- Rate/Acro Mode 2 축은 오른쪽 Stick Pitch/Roll, 왼쪽 세로 Throttle, 왼쪽 가로 Yaw다. 키보드는 `W/S Pitch`, `A/D Roll`, `Q/E Yaw`, `Space/Left Ctrl Throttle`로 각 축을 한 역할에만 연결한다. 공용 Move/Altitude/Yaw Action을 Acro에서 재해석하지 않으며 Mouse X/Y는 Rate 축이 아닌 직접 Yaw/Camera Pitch 개발 입력이다.
- 쉬운/제한 자세에서 카메라·Collision과 외형 기울기를 구분하고, Rate/Acro에서는 Root 자세가 Camera와 Local Up 추진을 함께 결정한다.
- 역할은 정찰 Scan, FPV Arm/자폭, Payload 픽업·드랍, Fiber의 재밍 면역+충돌 자폭, Ground UGV의 지상 주행과 상부 총·유탄을 프로젝트 소유 기능으로 사용한다. 현재 Catalog는 Scout/FPV/Drop/Fiber/Ground 5종이다.
- Ground UGV 무장은 `GroundWeapons` Capability가 있을 때만 활성화한다. 좌클릭은 상부 총구 기준 직사 총탄, 우클릭은 중력·반경 피해 유탄이며 다른 Drone의 Primary/Secondary 역할 입력과 섞지 않는다.
- 현재 무적재 속도·질량·추력·감도·Collision·Greybox Mesh는 실제 기체별 계측 전 시작값이며 최종값이 아니다.

## 비행 충돌·그물 장애물 기준

- 벽·그물 접촉과 총알 피격 화면 효과를 구분한다. 벽/그물의 외형 기울기는 카메라에서 분리하고 이동은 보간하지만, 총알 피격의 기존 Camera Additive Shake·체력·본체 피드백은 유지한다. 기체의 실제 이동과 의도한 FPV 자세/마우스 회전까지 고정시키는 것은 아니다.
- 벽 반발은 `PhysicsSandbox_Wall` 같은 특정 시험 Actor의 전용 기능이 아니다. 비행 Drone의 Collision Root가 일반적인 Blocking 벽·기둥·구조물에 닿으면 표면 안으로 파고들거나 계속 비비지 않고, 충돌 법선 바깥쪽으로 분리·반발하는 공통 비행 규칙이어야 한다.
- 바닥 착륙, 천장, 얇은 장애물과 고속 충돌은 같은 결과로 뭉개지 않는다. 표면 법선·접근 속도·Flight 상태로 `착륙 가능 접촉 / 일반 반발 / 강한 충돌·Crash`를 구분하고, 현재 시험 수치는 최종값으로 확정하지 않는다.
- 그물의 주 역할은 파괴물이 아니라 Rotor·날개가 걸려 조종을 방해하는 물리 장애물이다. 접촉 시 Cloth가 휘고 감기며, 기체는 감속·추력 저하·Roll/Yaw 교란을 받고 일정 조건을 넘으면 `Snared/Entangled` 또는 Crash·Mission 실패로 이어져야 한다.
- 복잡한 Visual Rotor마다 독립 강체를 두지는 않는다. 단일 Collision Root 원칙은 유지하되 가벼운 Wing/Rotor Contact Probe 또는 별도 Net Interaction Volume으로 “날개가 걸렸다”는 판정을 보강한다.
- Chaos Cloth 변형은 화면 표현을 담당한다. 포획·탈출·추락 판정의 단일 기준은 Frame Rate와 Cloth Solver 결과에 직접 의존하지 않는 프로젝트 C++ 상태와 접촉 누적값이 소유한다.
- 현재 Cube Strand 국소 절단·물리 낙하 기능은 Hit 위치와 물리 반응을 확인하기 위한 Runtime 진단용이다. 일반 Drone 충돌에서는 절단이 기본 Off이고 C++ 얽힘 상태가 감속·조종/추력 저하·완만한 외형 기울기·하강·포획을 결정한다. 접촉 때 피격 Shake를 호출하거나 Root를 반복 회전시키지 않는다. Collision Root 바깥의 네 Wing/Rotor Probe가 벽과 그물 접촉 위치를 보강하며, 실제 Chaos Cloth 변형과 탈출·Crash/Mission 실패 연결은 후속이다.
- 일반 비행 `ADronePrototypePawn`은 수평에 가까운 Blocking 벽·기둥·구조물 접촉에 공통 반발과 표면 분리를 적용한다. 저속 접촉도 버리지 않고 작은 속도·작은 거리로 밀려나며 충돌 속도가 커질수록 반발·분리·자세 Kick이 연속적으로 커져야 한다. 바닥·천장·Ground UGV는 제외하며, 강한 Crash/Damage 우선순위와 얇은 벽 CCD는 아직 별도 검증 항목이다.

## Training Gate 편집 기준

- 자동 Gate의 기준 선은 안쪽 하단에서 전체 통과 높이의 `1/6` 지점을 지난다. Spline 제어점·빛나는 선을 바꾸지 않고 Gate 중심을 올리며, 확대 후에도 같은 비율을 유지한다. 수동 `OrderedGates` 위치는 임의로 바꾸지 않는다.
- Gate 크기는 Course의 `게이트 전용 스케일`/`게이트별 추가 스케일`로 조절한다. Course Actor/Spline Scale을 Gate 크기 조절에 사용하지 않는다.
- 정상 순서·정방향 통과 승인에만 BP `통과 음성 / 사운드` 슬롯을 1회 출력한다. 슬롯 기본값은 None이며 임의 음원을 연결하지 않는다. Reset/중복/역방향/오순서에는 무음이다.
- 세 상태 색상과 별개로 `통과 전 머티리얼`/`현재 목표 머티리얼`/`통과 후 머티리얼`을 지정한다. 완성형 Static Mesh는 `GateAssetMesh`에 연결하고 적용할 Material Slot Index를 선택한다. 메시와 Trigger를 계속 분리한다.
- 구체적인 BP 항목과 팀원 설정법은 [`docs/tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md`](docs/tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md)를 따른다.

## 기상 기준

- World 기상 원본은 `UDroneWeatherProfile`과 `UDroneWeatherWorldSubsystem`, Level 연결은 `ADroneWeatherController`가 담당한다.
- Prototype Drone은 `UDroneWeatherResponseComponent`로 Snapshot 바람을 받는다. 현재 방식은 Sweep 위치 Drift Greybox이며 모터·PID·공기역학 1:1 구현이 아니다.
- 저장 Profile은 `Clear`, `LightWind`, `RainStorm_Greybox` 3종이다. 강풍 약 10.7m/s는 공개 민간 FPV 참고선이지 최종 내풍 한계가 아니다.
- 비 On/Off와 Snapshot Override, 카메라 추종 Instanced Mesh 빗줄기, 카메라 위쪽 Visibility Trace 기반 로컬 실내 감쇠는 구현됐다. 정식 Niagara GPU Rain, 젖음 Material/MPC, Splash·Audio와 품질 단계는 아직 구현되지 않았다. 비가 체력·신호·Mission 판정을 자동 변경하지 않는다.
- Weather 시험 표현은 `/Game/Drone/Weather/Blueprints/BP_DroneWeatherDebugVisualizer`에서 Bead 수·범위·크기·속도 배율·Mesh와 Readout/Hotkey 사용 여부를 조정한다. Gameplay 바람 계산과 분리한다.
- 자연스러운 바람 개선은 Gameplay Snapshot의 저빈도 결정성을 유지한 채 `지속풍 전환`, `돌풍 Attack/Release`, `표시용 보간`을 분리했다. Debug Bead는 풍향 변경 때 누적 이동거리 전체를 새 방향으로 재투영하지 않고, 보간된 순간 속도를 매 Frame 벡터 적분한다.

## AI·포탑 기준

- NPC가 점유하는 유인 포탑은 `BP_SO_MGTurret` 한 개다.
- `BP_AutoTurret_Vehicle`, `BP_AutoTurret_Emplaced`는 NPC가 잡지 않는 무인 자동포탑이다.
- 유인 MG는 `고정 Base → Yaw Body → Pitch Barrel → Muzzle` 구조이며 사수 Anchor는 Yaw Body의 자식으로 후방 위치와 회전을 따른다.
- Smart Object 동선은 번호나 Spline 고정 순서가 아니라 태그가 맞는 최근접 빈 Slot 선택이다.
- 개인화기 NPC의 몸 회전은 기본 3° 정지각과 추가 3° 시작 여유각을 쓰는 Hysteresis 방식이다. 몸은 큰 Yaw만 담당하고 Bone Gaze가 작은 잔여 오차를 보간해 보므로 3° 경계에서 몸/고개가 On/Off 왕복하지 않는다. Hostile Blueprint의 `NPCProfileComponent > Profile > NPC|Gaze`에서 정지각·Hysteresis·몸 회전속도를 역할별 조정한다.
- 실제 Shotgun은 모든 맵에서 `BP_ShotgunPelletProjectile`을 쓰며 `/Game/Drone/AI/Materials/M_ShotgunPelletGlow` 발광 비드/Tracer가 연결돼 있다. 기본은 8 Pellet·원뿔 반각 12°·Pellet당 3 피해이며 Cyan 예상선은 기본 Off인 Debug 옵션이다.
- Rifle·유인 MG·무인 포탑의 공용 기본 Projectile은 같은 발광 임시 Material과 확대된 탄두/Tracer를 사용한다. 역할별 최종 Mesh·Material·Scale은 파생 Blueprint에서 교체한다.

## Git·LFS 기준

- 실제 Git 상태, 코드, 자산과 실행 로그를 문서보다 우선한다.
- 사용자의 변경과 팀원 맵을 임의로 되돌리거나 덮어쓰지 않는다.
- 모든 `.uasset`, `.umap`은 크기와 무관하게 Git LFS로 관리한다.
- LFS 비용 문제를 Threshold 변경으로 일반 Git에 옮기지 않는다. Core와 선택형 Asset Depot 분리를 별도로 검토한다.
- Commit과 Push는 별도 지시가 없으면 사용자가 수행한다.
- 작업컴 인계 전에는 두 저장소의 로컬 변경이 Commit·Push됐는지 사용자가 GitHub Desktop에서 확인한다. 원격과 HEAD가 같아도 작업 트리가 Dirty면 다른 PC에는 전달되지 않은 상태다.

## 문서 갱신 규칙

- 현재 사실: `STATUS.md`
- 현재와 다음 작업: `WORKBOARD.md`
- 변경 금지 경계: `CONTEXT.md`
- 날짜별 기록: `docs/history/DRONE_WORKLOG.md`
- 상세 주제 문서: `docs/README.md`에서 찾아간다.
- 과거 상세 원문은 `docs/history/snapshots`에 보존하며 현재 기준으로 사용하지 않는다.
