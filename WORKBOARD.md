# Drone 작업 보드

마지막 갱신: 2026-09-30 — Bangkok City·OilRig Preview 실맵 이식

## Now

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| ASSET-BANGKOK-01 | Bangkok City 환경 이식 | 실제 `Maps/BangkokCity`를 `/Game/Drone/Maps/Lvl_BangkokCity`, 의존 자산 987개를 `/Game/Drone/ThirdParty/BangkokCity`로 이식. 본 프로젝트 Map load·외부/누락 0/0·GameMode None·Map Check 0/0 통과 | Editor에서 재질·조명·충돌·스케일·첫 로드와 FPS 확인. 약 11.46GiB 신규 LFS를 기존 사용자 변경과 분리 확인한 뒤 사용자 Commit/Push |
| ASSET-OILRIG-PREVIEW-01 | OilRig 실제 Preview 환경 이식 | 기존 Overview `Lvl_OilRig` 보존. 실제 `Maps/Preview`를 `Lvl_OilRigPreview`, 의존 자산 614개를 `ThirdParty/OilRigPreview`로 이식. Door BP 32개는 외형 64개를 정적화하고 Sample FirstPerson 로직만 제거. 빈 Actor 14개·완전 중복 1개 정리. Map load·외부/누락 0/0·GameMode None·Map Check 0/0 통과 | Editor에서 문/문틀 위치, 재질·조명·충돌·오션·비·첫 로드와 FPS를 수동 확인. 약 3.80GiB 신규 LFS를 기존 사용자 변경과 분리 확인한 뒤 사용자 Commit/Push |
| PHY-CAMERA-01 | 벽·그물 접촉 화면 안정화 | 접촉 피격 Shake 호출·급감속과 벽 순간 이격/Root 회전을 제거. 연속 접촉은 재충격 대신 제약으로 처리하며 외형 기울기와 FPV 카메라를 분리. Camera 위치 보간·그물 Camera Ignore 추가. 총알 피격 화면 Shake는 기존 동작 유지. Editor Build·Physics 4/4·Prototype 8/8·Story 저장 계약 1/1 성공(오류/경고 0), 관련 BP 6개 Compile 0/0 | Physics Sandbox에서 1/3인칭 저속/고속/지속 벽 접촉·그물 감속/포획 때 화면 떨림 감소와 충돌 유지 확인. NPC 맵에서 총알 피격 화면 흔들림이 남는지 확인. 자동화만으로 체감 Pass 처리하지 않음 |
| TUT-GATE-PRESENTATION-01 | Gate 통과음·위치·크기·자산 재질 | 정상 통과 음성/Sound 슬롯과 BP 연출 Event, 하단 1/6 배치·기존 저장 Child 시작 위치 복구, 공통/개별 Gate 전용 Scale, 전체 Mesh와 상태별 Material 슬롯 구현. 최종 Editor Build·관련 회귀 8/8 성공(오류/경고 0), Gate/Course BP Compile 0/0 | 실제 음원·최종 Gate Mesh를 BP에 지정한 뒤 TestMap에서 가청성, 1/6 위치, 확대해도 선 크기 불변, 상태별 재질·미지정 슬롯 보존을 수동 확인. 팀원 Production 맵은 직접 저장하지 않음 |
| SYNC-WORKPC-01 | 작업컴 즉시 재개 인계 | 2026-09-29 Unreal `7ad9a23`, 문서 `578304f`가 각각 `origin/main`과 일치하고 Clean임을 확인. 인계 문서와 점검 스크립트의 Build·Map Check 0/0·`WORKSTATION_READY` 검증 완료 | 작업컴에서 두 저장소 Pull·LFS 후 같은 명령으로 `WORKSTATION_READY` 재확인 |
| MISSION-FRAMEWORK-01 | Mission 통합 Blueprint 기반 | Manager/GameMode/Controller, 목표·실패·귀환 Trigger, 체력 100 파괴 표적을 `/Game/Drone/Mission`에 추가. Build와 Mission 자동화 3/3 성공 | Mission 1 Test Map/Definition에서 Delivery→선택 목표→Return과 시간/파괴 실패를 실제 Flow로 확인 |
| STORY-TEST-01 | Story Mission별 격리 TestMap 4개 | GoldenTime Drop/Return, Intercept Spline 차량·목적지 실패, VeilBreaker 재밍 이탈/Return, Endgame UGV 표적 3개/Return과 DA 4개 생성. Map Check 5맵 0/0, 저장 계약과 FrontEnd 13개 Catalog 자동화 성공 | 각 맵을 FrontEnd에서 수동 실행해 목표·실패·귀환을 확인하고 M1 선택 목표, M3 기체 교대, M4 장거리 타격을 후속 카드로 분리 |
| PHYSICS-SANDBOX-01 | 벽 충돌·그물 얽힘·국소 파괴 벽 | 일반 비행체 속도 비례 벽 반발·Wing/Rotor Probe와 그물 감속·조종/추력 저하·자세 교란·포획/하강까지 구현. Drone 충돌은 그물을 기본 절단하지 않고 탄환/폭발 Point Damage 국소 절단은 유지. Build 성공, `Drone.Physics` 2/2·`Drone.Prototype` 8/8·Story 저장 계약 1/1 성공 | Sandbox에서 저속 접촉은 작게 밀리고 고속 충돌은 크게 반발하는지, 날개 끝 접촉 방향의 자세 Kick, 그물 포획·하강·자동 해제와 조종 복구를 화면 확인하고 실제 Chaos Cloth/Dataflow와 Geometry Collection을 별도 구역에서 비교 |
| DR-FLIGHT-PHYS-02 | 단일 고속 기준·질량/추력·Payload 하중 | 느림/보통/빠름 UI 제거, 기존 빠름 배율 1.25를 단일 무적재 기준으로 승격. Dry Mass·합산 추력·모터 지연·선형/제곱 항력 추가, Mode 1/2 공통 적용. Drop 내장/부착 화물 kg 질량이 속도·가속·Yaw·호버 여유를 낮추고 투하 즉시 복구. Build 및 Prototype 8/8·Physics 2/2·Flow 5/5 성공 | FPV/Drop 수동 비행으로 무적재 속도, 모터 추력 지연, 적재 전후 호버·가속·선회 차이와 Mode 1/2 축만 달라지는지 확인. 실제 기체 스펙이 정해지면 Definition별 질량·추력·항력 교정 |
| PHY-NET-03 | 그물 날개 걸림·포획 장애물 | C++ 결정적 접촉 상태와 Collision Root 바깥 네 Wing/Rotor Sphere Probe v1 완료. 실제 이동 속도와 반복 접촉으로 감속·추력/조종 저하·Pitch/Roll/Yaw 교란·하강을 누적하고 임계값 이상은 Captured가 된다. 일반 충돌 절단은 기본 Off이며 BP 수치 조정 가능 | 수동 체감 조정 뒤 Chaos Cloth 시각 변형 + 필요 시 전용 Net Interaction Volume + 역추진/접촉 해제 탈출·Crash/Mission 실패를 연결하고 Standalone 3회 확인 |
| PHY-COL-01 | 모든 벽·구조물 공통 반발 | 일반 `ADronePrototypePawn`의 Component 기본 On. `120cm/s` 무반응·고정 Kick/6cm 이격을 없애고 저속부터 반발 속도·분리 거리·회전 Kick을 충돌 속도에 비례시켰다. 직전 속도 보존과 Wing/Rotor Probe를 사용하며 바닥/천장·Ground UGV는 제외. 비례 반발 Red→Green 회귀 성공 | Sandbox와 다른 TestMap에서 연속 입력 비비기/침투·날개 Probe 크기/방향을 수동 확인하고 강한 Crash/Damage 우선순위·Landing 상태·얇은 벽 Sweep/CCD를 후속 구현 |
| TUT-ROUTE-SELECT-01 | Training Route 4개 선택 시험 | `Lvl_DroneTrainingRouteSelectionTest`에 직선·좌곡선·우곡선·상승 슬라럼과 Gate 각 5개 배치. `1~4` 고정·`5` 무작위, 단일 활성, 진행 초기화, HUD 기록 Source 전환. Build·Map Check·API/저장/실제 키 PIE 성공 | 사용자가 화면에서 경로 형태·Gate 간격·랜덤 전환과 Lap HUD를 확인하고 각 Spline 점을 최종 조정 |
| TUTORIAL-MISSION-01 | Figma Tutorial 8개 독립 Mission | 공용 Test Map에 8개 Station/DA 구성. 사용자가 7개를 대략 확인했고 Hover는 새 실제 PIE에서 3초 유지→Return 전환 Success. 보이지 않던 Hover 영역에 비충돌 모서리 표식 4개 추가 | FrontEnd에서 Hover 표식·3초 진행 표시와 나머지 수업의 위치·크기·탄속·낙차·결과 화면 최종 수동 확인 |
| TUT-BEST-01 | Course별 Best Lap 영구 저장 | Lap History·평균·Best 비교는 현재 실행 메모리에만 있고 재실행하면 사라진다. `USaveGame`은 아직 없음 | 유효한 완주만 `CourseId + DroneId + ControlMode` 기준으로 최고 기록을 저장하고 새 실행·재시도 뒤 복원. 폐기된 HandlingPreset은 새 저장 Key에서 제외. 저장 없음/구버전/손상 데이터 안전 처리, HUD 구분, 자동화와 수동 재실행 통과 |
| TUTORIAL-FIGMA-02 | Figma 8개 훈련 ↔ Test Map 대조 | 8개 기능 판정과 독립 재시도 구현. 단계별 클리어 타임·연속 진행·전체 완료 UI와 Warehouse 환경은 미구현 | 수동 확인 뒤 Tutorial 진행 UI와 Warehouse Greybox 추가 |
| TUTORIAL-GUIDE-03 | 8개 수업 구현·테스트 기준 | 클래스 책임, DA/Tag, 수업별 구현법, Build→Asset→Map→PIE→성능 검증과 문제 확인 순서를 문서화 | 팀원이 문서만 보고 호버/FPV/Payload를 재현하고 Forward 수업을 추가 가능 |
| AI-LOCOMOTION-01 | 적·아군 NPC 걷기 모션 | Hostile Rifle/Shotgun은 프로젝트 Rifle Idle/Walk/Run, Friendly는 프로젝트 Unarmed Idle/Walk/Run AnimBP/BlendSpace 연결. 생성·저장 검증 성공 | Smart Object 맵에서 정지/보행/달리기 전환과 발 미끄러짐을 화면 확인. 낡은 NPC 맵 개수 고정 자동화 갱신 |
| MAP-TEST-01 | 경량 Tutorial Systems TestMap 수동 확인 | 맵·생성 도구·전용 자동화·Map Check 완료 | Gate/Ring/역할/HUD 한·두 Lap 화면 확인 |
| AI-SO-TUNE-01 | Smart Object·유인 MG·개인화기 추적 확인 | 순찰 최종 슬롯 방향·Pursue 정지점·Capsule 외 VisualOnly 계약을 적용했고 사용자 화면에서 정상 이동을 확인했다. 진단 로그 기본값 Off | 새 `1.0초` 첫 사격 조준 대기를 실제 화면에서 확인. 재발 시 Blueprint에서 `[NPC-STATE]`·`[NPC-MOVE]` 진단을 켜 로그 회수 |
| AI-OUTDOOR-TUNE-01 | 야외 감지·Smart Object 검색 범위 | Outdoor Controller BP를 Rifle/Shotgun에 연결. Sight 60m/Lose 70m/Search 80m×±10m/직전 회피 15m, BP 조절 가능 | 넓은 야외 맵 화면에서 과도한 원거리 점유·감지 끊김 여부를 확인하고 역할별 수치 확정 |
| AI-SHOTGUN-PIE-01 | 추가 Shotgun NPC 사격 체감 확인 | 실제 8 Projectile·12° 반각, Pellet당 3 피해, 상호 충돌 방지, Cyan Debug 기본 Off, 발광 비드/Tracer·3°/6° 시선 Hysteresis·Asset/PIE 자동화 완료 | 발광 비드 8개 분리 가시성·Cyan 선 제거·회피·최대 24 피해·사거리·LOS·시선 안정화를 Editor 화면에서 확인 |
| UI-FLOW-PROTOTYPE-01 | Mission/Drone 선택 임시 UI 확인 | 첨부 와이어프레임 기반 3열 C++ fallback 구현, `FrontEndPIE`·`MissionEntryPIE` 통과 | 16:9 화면에서 작전 목록/설명/시작과 기체 목록/상세/설정/출격이 잘리지 않는지 수동 확인 후 최종 WBP·Thumbnail 범위 결정 |
| MISSION-RULE-PIE-01 | 새 목표 Rule의 실제 맵 Vertical Slice | 귀환·Jammer·역할 Actor 시험 배치 완료, 직접 실행은 Prototype Flow | Test Mission DA/진입 경로에서 Scan/Delivery/Destroy/Return/Jamming Event·Tag·시간 규칙 확인 |
| STY-03-PIE-01 | 재밍 신호·비행·HUD Vertical Slice | 35%/80% 겹침 Zone TestMap 배치·저장 계약 완료 | 실제 비행으로 Overlap·HUD·둔화/복원 확인. 영상 Noise WBP는 별도 표현 작업 |
| STORY-BRANCH-01 | Mission 2→3 양쪽 스토리 분기 | Story Fact 저장·성공 적용·조건 목표 필터, 미끼/실제 탑승 양쪽 자동화 완료 | 사용자가 기본 스토리안을 정하면 실제 Mission DA에 Fact 설정 |
| DRONE-FIBER-01 | 광섬유 Drone 기반 | DroneSpy Body·분리 Rotor 4개와 회전을 사용하고 공급 GSU 통을 `FiberSpoolMeshComponent`에 약 28cm 높이로 하부 장착. BaseColor·Normal·ORM·Emissive Material, 통 상단 출구→누적 지면→현재 기체 다점 포물선/Hermite 케이블, `JammingImmunity + ImpactDetonation`, 1인칭 기본값 적용. Editor Build·ExtendedRole 1/1 성공 | TestMap에서 Spy 본체·통 크기/위치, 본체/카메라 비간섭, Rotor 회전, 통 상단 케이블 출발과 곡률, 조작·자폭·재밍 면역을 화면 확인하고 BP Transform/굵기·간격을 최종 조정 |
| DRONE-GROUND-01 | 지상 UGV 기반 | 기존 주행·4점 접지·상부 독립 조준에 `UDroneGroundWeaponComponent` 연결. 좌클릭 직사 총탄 25 피해, 우클릭 중력 유탄 100 반경 피해, 수명/쿨다운 적용 | 시험맵에서 상부 방향과 실제 탄도·4발 처치·유탄 낙차/반경을 수동 확인하고 수치 조정 |
| DR-FPV-ACRO-PIE-01 | FPV Rate/Acro 실제 조작 체감 | Mode 1/2 축 분리와 각속도·무수평복귀에 공통 질량·추력·모터 응답·중력·Body Up 추진·선형/제곱 항력 v2 연결. 별도 속도 단계는 제거 | 키보드/패드로 Nose-down 전진력, 호버·상승·무추력 하강, Roll/Loop와 650°/s 체감, Mode 1/2가 축 배치 외 비행 성능이 같은지 확인 후 수치 조정 |
| DR-FPV-ACRO-INPUT-02 | Acro 키보드·패드 Mode 1/2 | 의미축 Action 4개+패드 세로 원시축 2개, IMC 33 Mapping, Pawn/UI 분기, Editor Build·계약·프로필·3회 PIE·MissionEntryPIE 성공 | 키보드 W/S Pitch·A/D Roll·Q/E Yaw·Space/Ctrl Throttle 유지, 패드 Mode 1 LeftY Pitch/RightY Throttle와 Mode 2 반대 배치를 화면에서 확인 |
| WTH-03 | 비 표현 Vertical Slice | OilRig `T_rain_Mask` 참조 전용 Material, 최대 112개 짧은 Plane 빗줄기, 파란 Debug 기본 Off, 표면별 천장/지면 차단·0.35초 실내 감쇠 구현. Weather 4/4·Map Check 0/0 | 실외→지붕 아래→실외, 긴 잔상 감소·천장 침투 차단, RainStorm→Clear/비 Off 화면 확인 후 Niagara·MPC·Audio·품질 단계 범위 결정 |

### 사용자가 지금 확인할 맵

`/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest`

1. 4변 Gate Frame이 네모 Trigger 안쪽을 깔끔하게 따르는지 본다.
2. `통과 전 / 현재 목표 / 통과 후` 색이 순서대로 바뀌는지 본다.
3. Ring Handle 하나를 움직여 CourseSpline 자체는 변하지 않고 Ring만 가장 가까운 Spline 위치를 따르는지 본다.
4. Recon·Impact·Payload 표적과 Carryable이 보이고 깨진 긴 World Text가 없는지 본다.
5. 한 Lap에서 현재 속도·고도·구간 시간·평균값이 갱신되는지 본다.
6. 두 번째 Lap에서 이전 평균·Best·빠름/느림 증감 부호가 맞는지 본다.
7. 종료 후 Editor가 정상 복귀하는지 확인한다.

Production `/Game/Drone/Maps/Lvl_DroneTraining`에서는 위 시험을 위해 Actor를 추가하거나 저장하지 않는다.

추가 확인 맵:

- `/Game/Drone/Maps/TestMap/Lvl_DroneTrainingRouteSelectionTest`: `1~4` 고정 Route, `5` 무작위 Route, Gate/Lap/HUD 전환
- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialMissionTest`: Figma Tutorial 8개 독립 Mission Station과 귀환
- `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`: 순찰·감지·수색·MG·자동포탑·차량
- `/Game/Drone/Maps/TestMap/Lvl_DroneMissionSystemsTest`: 재밍 약/강/겹침·Return Zone·역할 표적
- `/Game/Drone/Maps/TestMap/Lvl_DroneShotgunSystemsTest`: 추가 Shotgun NPC·작은 Pellet 8개/Tracer·탄약·LOS 사격장
- `/Game/Drone/Maps/TestMap/Lvl_DroneWeatherSystemsTest`: 기존 `1/2/3/4` 조작·`7/8/9` 날씨·바람 확인에 더해 `BP_DroneRainVisual`의 카메라 추종 Instanced Mesh 비와 지붕 감쇠를 확인한다. 정식 Niagara는 아니다
- `/Game/Drone/Maps/TestMap/Lvl_DronePhysicsSandbox`: 일반 Flight 공통 벽 반발, 4 Corner 처짐 그물 얽힘/포획·선택적 국소 절단/복구, 격자 벽 조각별 물리 파괴/복구
- `/Game/Drone/Maps/TestMap/Lvl_DroneStory01_GoldenTimeTest`: Drop 물자 전달→귀환
- `/Game/Drone/Maps/TestMap/Lvl_DroneStory02_InterceptTest`: Spline 차량 요격→목적지 도착 실패
- `/Game/Drone/Maps/TestMap/Lvl_DroneStory03_VeilBreakerTest`: 광섬유 Drone 재밍 구역 이탈→귀환
- `/Game/Drone/Maps/TestMap/Lvl_DroneStory04_EndgameTest`: Ground UGV 지휘 표적 3개 파괴→귀환

## Next

이번 요청의 바로 다음 확인은 [`Gate 배치 가이드`](docs/tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md)에 따라 BP에 실제 음원·최종 Gate Mesh·세 상태 재질을 지정하고 Route TestMap에서 1/6 높이·Gate 전용 Scale·정상 통과음/재질을 수동 확인하는 것이다. 아래 기존 순서는 유지한다.

1. [`DRONE_STORY_PHYSICS_TEST_MAP_GUIDE.md`](docs/gameplay/DRONE_STORY_PHYSICS_TEST_MAP_GUIDE.md)대로 Physics Sandbox에서 저속 벽 접촉의 작은 밀림, 고속 충돌의 큰 반발, 날개 끝 접촉 자세 Kick과 그물 감속/포획·자동 해제·선택적 절단을 수동 확인한다
2. FrontEnd에서 FPV와 Drop을 각각 출격해 단일 무적재 고속 기준, Mode 1/2 축 배치, Drop 내장 화물 투하 전후와 0.75kg/1.25kg Carryable 적재 전후 성능 차이를 수동 확인한다
3. Physics Sandbox의 절차형 그물/조각 벽과 실제 Chaos Cloth/Dataflow 부분 고정 그물·Geometry Collection 벽을 같은 크기/충돌 조건으로 비교한다. 맵 전체 파괴는 하지 않는다
4. [`DRONE_TRAINING_ROUTE_SELECTION_TEST_GUIDE.md`](docs/tutorial/DRONE_TRAINING_ROUTE_SELECTION_TEST_GUIDE.md)대로 `1~5` Route 선택·Gate/Lap/HUD를 화면 확인하고 Spline 점을 조정한다
5. Tutorial Hover를 모서리 표식 안에서 3초 유지해 목표가 귀환으로 바뀌는지 화면 확인한다. 자동 PIE는 이미 통과했다
6. `TUT-BEST-01`을 구현한다. 이전 평균은 실행 중 History로 유지하고 저장 파일에는 공정한 조건별 Best Lap만 먼저 기록한다
7. 단계별 조작키·목표 브리핑, 클리어 타임, 재시도/다음 수업, `n/8` 진행도와 전체 완료 UI를 순서대로 붙인다
8. Warehouse Greybox를 TestMap에 먼저 적용하고 팀원 Production Training 맵에는 검증된 Station만 수동 이식한다
9. M1에 선택 정보 회수와 화물 파괴 실패, M2에 잔해/Story Fact, M3에 Jammer 해제·UGV 교대, M4에 장거리 타격·엔딩을 순서대로 추가한다
10. Shotgun, AI 첫 사격 1초 조준, Mission 재밍, FPV Rate/Acro, 비·실내 감쇠, 광섬유 통/케이블과 Ground UGV 수동 회귀는 위 단계 사이의 회귀 묶음으로 유지한다
11. 중간/강한 재밍의 실제 영상 Noise WBP·목표 정보 손실, 정식 Niagara Rain·MPC Wetness·Audio·품질 단계는 Story Vertical Slice 이후 표현 작업으로 진행한다
12. 나머지 시험 맵은 소유권·참조 감사 후 AssetTools로 이동한다. `test1`·`test2`는 용도 확인 전 유지한다

## 이동 후보 맵

| 맵 | 처리 |
|---|---|
| `Lvl_DronePrototype` | 참조 감사 후 TestMap으로 이동 |
| `Lvl_NPCSmartObjectGreybox` | `/Game/Drone/Maps/TestMap` 이동 완료, 회귀 6/6에 포함 |
| `Lvl_DronePackShowcase` | 자산 시각 확인 후 이동 |
| `Lvl_MilitaryBase_Test` | 참조 감사 후 이동 |
| `test1`, `test2` | 팀원 용도 확인 전 이동·개명 금지 |
| `Lvl_DroneTraining` | 팀원 Production 맵, 이동·분할·덮어쓰기 금지 |

## 병행 수동 회귀

- Drone 외형: 모델별 Mesh, Rotor 제자리 축·방향·속도, W/S Pitch와 A/D Roll
- 역할 기능: 정찰 Scan, FPV Arm/자폭, Carryable 픽업·드랍 후 잔존
- AI: Rifle/MG/Cover 시선, 유인 MG 사수 후방 정렬, 사망 뒤 생존 사수 교대
- 무인 포탑: 설치형·차량형 탐지, Yaw/Pitch, 발사와 장애물 차단
- 차량: 4점 지면 추종, Z/Pitch/Roll, 바퀴 회전 방향, 차량형 포탑 부모 추종
- 피격 효과: 본체·카메라 흔들림, 연속 피격, 종료 후 복원과 멀미 여부

## 최근 완료

| 항목 | 결과 |
|---|---|
| 경량 TestMap 분리 | 팀원 Training 변경 없이 별도 맵·검증 도구 생성 |
| Gate 시각 정합 | 16각 임시 Ring을 Trigger와 맞는 4변 Frame으로 교체 |
| 역할 World Text 정리 | 기본 숨김, 선택 시 짧은 `SCAN/IMPACT/DROP/PICKUP` 사용 |
| 유인 MG 안정화 | 사망 후 재할당, 정체 감시·재경로·도착 Snap 검증 |
| 문서 정리 | 현재 문서 4개 요약, 상세 문서 주제별 분류, 과거 원문 보존 |
| Git 정리 | Unreal·문서 Push 완료, 자동 Stash 2개 삭제 |
| Mission Rule 기반 | Data Asset 목표 종류·수량·시간·대상 ID, Director Event/Timer/중복 방지, HUD Snapshot 연결 |
| Training Mission 이행 | 기존 한 Lap 목표를 Training Lap Rule로 저장, Map 미수정 |
| 귀환 Zone 코드 | 배치형 Box Overlap Actor 추가, 실제 맵 배치·화면 검증 대기 |
| 재밍 Greybox | Zone/Signal 단계·HUD 경고·강한 단계 비행 둔화/복원·이탈/해제 Rule C++ Event, UI 포함 회귀 7/7 Success |
| Figma Mission 대조 | Tutorial+4개 Story Mission, 역할 Drone, 화면과 현재 코드/미구현 항목 매트릭스 작성 |
| Story 분기 | Mission 성공 Fact·조건부 목표로 Mission 2→3 두 안 모두 지원 |
| 광섬유 면역 | Implemented Capability에 따라 활성 재밍 Source 무시/해제 시 즉시 재평가 |
| AI 시험 맵 이동 | AssetTools 이동·코드/도구 경로 갱신, Asset·PIE·감지/수색 통과 |
| Mission Systems TestMap | Jammer 2·겹침 1·Return 1·역할 표적 3·Carryable 1, Map Check 0/0·회귀 통과 |
| Shotgun Systems TestMap | 기존 AI 맵 유지, 추가 Shotgun NPC 1·거리 표식 3·LOS 벽 1, Map Check 0/0·전용 회귀 2/2 |
| Shotgun 가시성/API | Projectile 모드 Cyan Pellet 비행선, BP 표시 On/Off·직전 끝점 조회, 전체 계약 5/5 성공 |
| FPV Rate/Acro | 송신기 Mode 1·Mode 2, Actual Rates형 각속도, 자동 수평 복귀 없음, 공통 질량·합산 추력·모터 응답·Body Up 추진·선형/제곱 항력 v2, FPV 무적재 27m/s·650°/s 기준 |
| Acro 입력 분리 | 키보드 W/S Pitch·A/D Roll·Q/E Yaw·Space/Ctrl Throttle 유지, Gamepad Mode별 세로축 Action 2개 추가, IMC 33 Mapping·3회 PIE 성공 |
| AI 순찰 회전·부착물 충돌 차단 | 예약 최종 슬롯 기준 Patrol 몸 방향, 300°/100cm 회전 회귀, Capsule 외 Primitive VisualOnly 강제. 실제 Shotgun `Gun`→Rifle stuck 로그 재현 후 AI 핵심 PIE 3종 성공 |
| 개인화기 첫 사격 조준 지연 | 최초 Sight 뒤 기본 1.0초, Blueprint 조절 가능, StateTree 전환과 독립, 표적 교체 시 이전 사격 정리. Build·기본 계약·Shotgun Map/PIE·NPC Greybox PIE 성공 |
| Figma 2026-09-18 재확인 | Page 1 최상위 148개 읽기 전용 감사. 타이틀→미션 선택/설명→로비/드론 선택→인게임, 공중 HUD, Racing UI 최신 요구 확인. 원본 미수정 |
| 단일 비행 성능 기준 | 느림/보통/빠름 UI 제거. Legacy Stable/Balanced/Agile 이름만 유지하고 모든 런타임 요청은 Balanced로 정규화. 기존 빠름 1.25 배율을 무적재 기본 성능으로 사용 |
| 기상 데이터·바람 Runtime | Profile/Snapshot/Subsystem·Controller·Drone Response, 저장 Profile 3종, TestMap·Map Check·기상 자동화 3/3 성공 |
| 차량 바퀴 회전축·접지 교정 | 실제 Tire Mesh의 옆 회전을 부모 공간 +Y 차축으로 교체하고, 30cm 반지름 때문에 약 20cm 잠기던 BP를 52cm로 교정. 축·Bounds·평면 접지 Red→Green과 맵 Validate 통과, 화면 재확인 대기 |
| Shotgun Pellet 가시화 | 실제 8발·12° 확산, Pellet당 3 피해, 전용 BP의 주황 발광 `0.04` 비드와 `0.20 × 0.0125` Tracer, 집중 회귀 성공 |
| 개인화기 정면 시선 안정화 | 몸 Yaw와 Bone Gaze 공통 3° 데드존, 1.9° 좌우 표적 왕복 회귀 Red→Green, Blueprint 역할별 조정 가능 |
| 병사 상태 전환 안정화 | 공통 최소 유지 1.0초, 유지 중 사격·점유·이동 조건 재점검, MG 재시도 Event 지연, 사망·파괴·Lost 확정 즉시 정리. 후속 추적 안정화 뒤 MG 재점유 포함 전체 PIE Green |
| 개인화기 추적·포기 안정화 | Fire/Pursue/Disengage 정책, 실제 3D 사거리 안 즉시 정지·사격, 밖 판정 0.2초 확인 뒤 Pursue, Nav 투영, 같은 목적지 MoveTo 중복 방지, 3,000cm 리시·2.5초 무진행·복귀 Cooldown, 추적 몸·Gaze 이동 벡터 정렬, StateTree 다음 Tick 재시작. 집중 회귀 성공 |
| Weather TestMap 가시화 | BP 조절형 Visualizer, 이동 Bead 24개, Profile/풍속/풍향/모드 Readout, 1/2/3/4 비교 키와 Map Check 0/0 |
| 자연스러운 바람 전환 | Gust Attack/Release·풍향 최단각 응답, 표시 속도 벡터 적분, 풍속별 Bead 방향/길이, Weather 3/3 성공 |
| 야외 AI Blueprint 튜닝 | Outdoor Controller BP에 60/70m Sight, 80m Search, 15m 직전 지점 회피를 분리하고 Rifle/Shotgun 연결 |
| 차량 Spline Route v1 | Route BP·차량 참조/속도/Reverse/Loop/도착 Event, Spline XY/Yaw와 4점 지면 Z/Pitch/Roll 결합 |
| Random Weather Manager | 8방향+무풍, 독립 변경 주기·풍속 범위·보간, Cardinal/m/s HUD, Editor 전용 무충돌 원뿔, Map Check 0/0·핵심 회귀 6/6 |
| Random Weather 수동 확인 | 사용자가 Weather 화면 확인 완료를 보고함. 원뿔 Play 숨김·무충돌과 Random Wind 판독을 재작업 대상으로 두지 않음 |
| 차량 Spline Route 시험 | 사용자가 별도 시험 맵 제작과 화면 확인 완료를 보고함. 후속은 실제 Mission Route/곡률 감속 요구가 생길 때 진행 |
| 광섬유·지상 Drone 기반 | 프로젝트 소유 Definition/Integration BP, FPV Body+Rotor 4·GC Drone 1 Poseable Visual, 빈 통 Mesh 슬롯·다점 곡선 Spline 케이블, 면역/자폭, 최초 장거리 지면 획득·GroundDrive/4점 접지, 차체 독립 Turret/Camera 조준과 총·유탄 Anchor, 5종 선택 Flow. ExtendedRole 1/1·FPVAsset 1/1·Prototype+Flow 13/13 성공 |
| 강우·실내 감쇠 Greybox | OilRig Mask 기반 Plane 최대 112개, 기본 65×2.4cm·Opacity 0.22·개별 크기 편차, 위쪽/표면 Trace·0.35초 실내 감쇠, Weather 4/4·Map Check 0/0. 화면 확인 대기 |
| 강우 Snapshot 디버그 프리뷰 | 전용 Weather TestMap 7/8/9 프로파일 전환은 유지하되 구형 파란 DrawDebug 선분은 기본 `Off/0개`다. Rain Visual과 겹치지 않으며 진단할 때만 수동 활성화 |
| 비 기획 | Camera-follow GPU Rain·Effect Type·젖음/실내/Splash 최적화 계획과 Snapshot 표현값. Niagara/MPC/Audio는 다음 작업 |

시험 맵 사용법은 [`docs/gameplay/DRONE_TEST_MAP_GUIDE.md`](docs/gameplay/DRONE_TEST_MAP_GUIDE.md), Mission BP 배치는 [`docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md`](docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md), FPV 조작은 [`docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md`](docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md), 기상은 [`docs/gameplay/DRONE_WEATHER_WIND_RAIN_PLAN.md`](docs/gameplay/DRONE_WEATHER_WIND_RAIN_PLAN.md), Mission Rule 설정은 [`docs/gameplay/DRONE_MISSION_OBJECTIVE_RULE_GUIDE.md`](docs/gameplay/DRONE_MISSION_OBJECTIVE_RULE_GUIDE.md), 전체 순서는 [`docs/planning/DRONE_TUTORIAL_STORY_PLAN.md`](docs/planning/DRONE_TUTORIAL_STORY_PLAN.md)를 참고한다.
