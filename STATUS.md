# 현재 작업 상태

기준일: 2026-09-23 (Asia/Seoul)

## 한눈에 보기

- 현재 단계: Random Weather와 차량 Spline Route의 사용자 화면 확인·시험 맵 작업은 완료 보고를 받았다. Weather Manager 비 On/Off, 카메라 추종 강우 Greybox·실내 지붕 감쇠, 광섬유 자폭 드론의 빈 통 Mesh 슬롯·지면 추종 Spline 케이블, 최초 장거리 지면 획득을 포함한 UGV와 5종 선택 Flow를 구현했다
- 조작 단계: 기존 쉬운 조작·제한 자세에 FPV Rate/Acro 송신기 Mode 1·Mode 2를 분리했다. 키보드는 W/S Pitch·Space/Ctrl Throttle을 유지하고 패드 세로축만 실제 Mode에 따라 바뀐다. 핸들링 UI는 느림/보통/빠름으로 바꾸고 현재는 최대 속도만 변경한다
- 바로 다음 개발: 새 강우 실외→실내 화면 확인과 광섬유/UGV 조작·스케일 확인 → 첫 사격 전 약 1초 조준 체감과 Mode 1/2 패드 체감 확인 → Niagara/MPC/Audio·Mission 중 기체 교대 → Test Mission DA/진입 경로
- 검증 운영: 외부 OpenCode 모델 호출은 종료했다. 프로젝트 전용 Agent·모델 설정은 제거했으며 이후 구현과 검증은 Unreal 자동화와 사용자 수동 화면 확인으로 진행한다
- Unreal Editor: 2026-09-23 확장 역할·강우 빌드와 자동화 뒤 종료 상태
- Production Training: 팀원이 실제 Tutorial 환경을 제작 중이므로 열람 외 저장·덮어쓰기·자동 재구성 금지

## Git 기준

| 저장소 | 현재 기준 | 상태 |
|---|---|---|
| Unreal `D:\JGY\project\drone` | 작업 시작 기준 `main = origin/main = de81c19` | 비/실내 감쇠·광섬유/UGV·5종 선택 Source와 프로젝트 소유 Asset이 로컬 변경. 사용자 수정 Skeleton 3개는 보존 |
| 문서 `D:\JGY\project\md` | 작업 시작 기준 `main = origin/main = 6527d7b` | 이번 상태·역할·Weather 가이드 최신화가 로컬 변경 |

2026-09-23 작업 시작 시 두 저장소의 HEAD와 `origin/main`은 각각 일치했다. 이번 변경은 아직 커밋하지 않았고, 기존 `MG_Turret/GC_Drone_2/GC_Drone_3 Skeleton` 사용자 변경을 되돌리거나 저장하지 않았다. 외부 모델 검증은 종료했고 프로젝트 저장소에 OpenCode 설정을 남기지 않는다.

## 최신 완료 항목

- Weather Manager에 `Enable Rain`, 자동 강우 Visual 생성 Class를 추가했다. 비 Off는 바람/Profile ID를 유지하고 Rain Snapshot 표현값만 0으로 만들며 Blueprint에서 런타임 전환 가능하다
- `/Game/Drone/Weather/Blueprints/BP_DroneRainVisual`과 `/Game/Drone/Weather/Materials/M_DroneRainStreak_OilRigMask` 추가. OilRig 원본 `T_rain_Mask`를 참조하는 최대 112개 짧은 Plane 빗줄기(기본 65×2.4cm, 불투명도 0.22)를 재사용한다. 구형 파란 DrawDebug 선은 기본 Off/0개다. 카메라 위쪽 Trace·0.35초 실내 보간과 빗줄기별 WorldStatic/WorldDynamic 표면 Trace로 지붕·지면 아래 표시를 막으며 맵 전체 Weather Snapshot은 바꾸지 않는다
- `/Game/Drone/Integrations/RoleDrones/BP_DroneFiberOpticIntegration`과 `DA_Drone_FiberOptic_Greybox` 추가. Sting Interceptor Visual, `JammingImmunity + ImpactDetonation`, 1인칭 기본 시점을 사용한다. `FiberSpoolMeshComponent`는 제작 예정 통을 넣는 빈 Static Mesh 슬롯이며 기본 위치 `(-32,0,-18)cm`만 잡았다. 통 출구부터 지나온 지면까지 Spline과 Cylinder Spline Mesh가 이어지고 마지막 구간은 아래로 처진다
- `/Game/Drone/Integrations/RoleDrones/BP_DroneGroundUGVIntegration`과 `DA_Drone_GroundUGV_Greybox` 추가. GC Drone 1 Skeletal Mesh를 참조하고 `W/S` 전후·`A/D` 조향·`Q/E` 제자리 회전, 고도 입력 차단, 네 지점 지면 높이/Pitch/Roll 추종과 바람 Drift 비활성화를 적용한다. 높은 PlayerStart에서도 최대 10,000cm 아래 지면을 최초 획득해 즉시 접지한 뒤 4점 추종으로 전환하며, Visibility를 막지 않는 지형은 WorldStatic/WorldDynamic 보조 Trace로 찾는다. 거리·조향·Clearance·Trace·보간 수치는 BP에서 조정한다
- Tutorial Mission과 GameFlow/선택 UI를 기존 3종에서 Scout/FPV/Drop/Fiber/Ground 5종으로 확장했다. 외부 공급 Skeleton은 수정하지 않고 Integration BP가 Visual만 참조한다

- `/Game/Drone/AI/Blueprints/BP_DroneNPCAIController_Outdoor` 추가. Hostile Rifle/Shotgun에 Sight 60m, Lose Sight 70m, Smart Object 검색 반경 80m·높이 10m, 직전 지점 회피 15m를 적용하고 Blueprint Class Defaults에서 조정 가능하게 했다
- `/Game/Drone/Vehicles/Blueprints/BP_DroneVehicleSplineRoute`와 차량 Spline Follow v1 추가. Vehicle Instance에서 Route 참조·On/Off·속도·끝 반전/Loop를 조정하며 XY/Yaw는 Spline, Z/Pitch/Roll은 기존 4점 지면 Trace가 담당한다
- `/Game/Drone/Weather/Blueprints/BP_DroneRandomWeatherController` 추가. 8방향+무풍, 방향 8~18초·세기 5~12초·1~9m/s 시작값과 보간값을 BP에서 조정한다. 에디터에서는 원뿔 표식이 보이고 Play/Package에서는 제거되며 Actor/표식 Collision·Overlap·Navigation 영향은 없다
- 바람 UI를 `E/NE/N/NW/W/SW/S/SE/CALM`과 m/s로 통일하고 Flight HUD에 `풍향 … | 풍속 … m/s`를 추가했다

- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest` 경량 시험 맵 생성
- 곡선 Course, CourseSpline과 분리된 Ring Handle 5개, Gate/Sequence 5개 구성
- Recon·Impact·Payload 역할 표적 각 1개와 Carryable 1개 배치
- Gate의 임시 16각 Cube Ring을 Box Trigger 안쪽과 맞는 4변 발광 Frame으로 교체
- Gate `통과 전 / 현재 목표 / 통과 후` 3상태 색상 계약 유지
- 깨지는 역할 표적·Carryable World Text를 기본 숨김 처리하고 선택 표시 문구를 짧게 정리
- 유인 MG 사수 사망 뒤 재할당 재시도, 이동 정체 감시, 재경로와 Greybox 도착 Snap 보강
- 병사 전투 상태에 공통 `Minimum Response State Duration=1.0초`를 추가했다. MG·Cover 이동/사용 태스크가 한 프레임 실패해도 유지시간 동안 현재 예약·감지·사격 행동을 다시 점검하고, 시간이 지난 뒤에도 실패일 때만 다음 상태로 넘어간다. 사망·드론 파괴·Sight Lost 확정 정리는 지연하지 않는다
- 개인화기는 실제 3D 무기 사거리 안이면 즉시 정지·사격하고, 사거리 밖 판정이 기본 0.2초 지속될 때 추적을 시작한다. 사거리 밖에서는 NavMesh에 투영한 표적을 추적하며 전투 시작점 기준 기본 3,000cm 리시 또는 기본 2.5초 무진행 한계를 넘으면 표적을 포기하고 순찰로 복귀한다. 같은 투영 목적지는 기본 150cm 이상 바뀔 때만 갱신한다
- 개인화기 Pursue는 Drone 자체를 큰 허용 반경으로 쫓지 않고 `PersonalWeaponPursuitRangeRatio`로 계산한 지상 사거리 정지점을 작은 `PersonalWeaponPursuitDestinationAcceptanceRadius`로 추적한다. Pursue 동안에는 Controller 한 곳이 그 안정된 최종 목표를 향해 몸 Yaw를 보간하고 Bone Gaze도 같은 목표를 사용한다. `bUseAccelerationForPersonalWeaponPursuitMoves=false`가 기본이라 짧은 경로점을 가속으로 지나쳐 공전하지 않으며, 이 설정은 Pursue에만 적용되어 일반 순찰의 가속 이동은 유지된다. 리시 포기 후 StateTree 재시작은 다음 Tick으로 예약해 `StartTree` 재진입을 막는다. 사거리 비율·도착 반경·Pursue 가속 사용 여부·회전속도·리시·재경로 거리/주기·무진행·Cooldown 값은 Controller Blueprint에서 조정 가능하다
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
- FPV Rate/Acro를 송신기 Mode 1과 Mode 2로 분리했다. 키보드는 두 모드 모두 같은 의미축을 유지하고, Gamepad는 Mode 1 `Left Y=Pitch/Right Y=Throttle`, Mode 2 `Left Y=Throttle/Right Y=Pitch`를 사용한다. 기존 `AcroRateRealisticGreybox` 열거형 이름은 저장 Asset 호환을 위해 Mode 2 의미로 유지했다
- 기존 `안정/균형/고기동` UI를 `느림/보통/빠름`으로 바꿨다. 저장 호환을 위해 내부 Stable/Balanced/Agile 이름은 유지하며, 현재 기본 프리셋은 MaxSpeed `0.80/1.00/1.25`만 변경하고 가속·Yaw·자세각 배율은 1.0이다
- `Lvl_NPCSmartObjectGreybox` 실제 실행 로그에서 Rifle이 Shotgun의 `Gun` 컴포넌트에 걸려 `stuck`되는 정확한 충돌 상대를 확인했다. NPC Character는 Capsule 외 모든 Primitive를 Collision/Overlap/Nav 비활성 VisualOnly로 복구하며, 자동화가 각 런타임 컴포넌트를 검사한다
- 순찰 중 몸이 50~100cm 단위의 Nav 즉시 경로점을 따라 원을 그리지 않도록 Patrol 몸 방향은 예약된 최종 Smart Object 슬롯을 기준으로 유지한다. 3초/100cm 전에 300° 이상 누적 회전하면 실패하는 실제 맵 회귀를 추가했다
- FPV Data Asset 기본값을 Rate/Acro+고기동으로 변경. 공개 민간 FPV 참고선으로 수평 27m/s, 수직 9m/s, Pitch/Roll 650°/s, Yaw 400°/s를 조정 가능하게 저장
- Rate/Acro에 중력, 중립 호버, 기체 Up 방향 추력, 속도 비례 항력, Body Rate 응답 시간을 연결했다. `Space/Ctrl`은 호버 기준 추력 증감이고 W/S Pitch로 기울인 Up 축이 실제 전후 추진력을 만든다. 호버 스로틀·중력·항력·Rate 응답은 FPV Data Asset/Blueprint에서 조정 가능하다
- `UDroneWeatherProfile`, `FDroneWeatherSnapshot`, `UDroneWeatherWorldSubsystem`, 배치형 `ADroneWeatherController` 구현. Profile 기본 10Hz로 결정적 지속풍·돌풍·전환값을 공급
- 모든 Prototype Drone에 `UDroneWeatherResponseComponent`를 부착. 쉬운 조작 65%·제한 자세 25%·Rate/Acro 0% 기본 보정과 Sweep Drift 적용. 최종 물리가 아닌 `UFloatingPawnMovement` Greybox
- `/Game/Drone/Data/Weather`에 `Clear`, `LightWind`, `RainStorm_Greybox` Profile 3종 생성
- `/Game/Drone/Maps/TestMap/Lvl_DroneWeatherSystemsTest` 생성. LightWind Controller 1개·35° 풍향 화살표·Prototype GameMode, Map Check 0/0
- Weather TestMap에 `/Game/Drone/Weather/Blueprints/BP_DroneWeatherDebugVisualizer`를 배치했다. 24개 흐름 Bead, 현재 Profile/풍속/풍향/조작 모드 화면 표시와 `1 Easy / 2 Manual / 3 Acro Mode 1 / 4 Acro Mode 2` 비교 키를 제공한다
- 돌풍에 Attack/Release/풍향 응답 시간을 분리하고 최단각 풍향 보간을 적용했다. Debug Bead는 표시 속도를 부드럽게 따라간 뒤 벡터 적분하므로 풍향 변경 때 과거 누적 거리를 새 방향으로 재투영하지 않으며, 풍속에 따라 방향과 길이가 바뀐다
- OilRig Mask 기반 Camera-follow Plane 강우 Greybox, 실내 지붕 감쇠와 표면 아래 Streak 차단은 구현됐다. 정식 Niagara GPU Rain, MPC Wetness, Splash·Audio, 품질 단계와 GPU 측정은 아직 미구현

## 검증된 근거

- 2026-09-23 MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공
- `Drone.Weather` `4/4`, 통 슬롯·표시 Spline·고공 Spawn 접지를 검사하는 `Drone.Integration.ExtendedRoleDrones` `1/1`, Pawn 전체 회귀 `Drone.Prototype` `8/8`, 5종 Catalog를 검사하는 `Drone.Flow.Contract` `1/1`, 5종 선택 UI의 `Drone.Flow.FrontEndContract`·`FrontEndPIE` 각 `1/1` Success·실패 0
- Weather 생성 도구 Validate와 Map Check `0 errors / 0 warnings`. Production `Lvl_DroneTraining`은 열거나 저장하지 않았다
- 사용자가 Random Weather 화면 확인과 차량 Spline Route 시험 맵 제작·화면 확인을 완료했다고 보고했다
- 2026-09-22 MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공
- Random Weather TestMap 재생성 및 Map Check `0 errors / 0 warnings`, Production Training 수정 0
- `SmartObjectFoundationDefaults`, `FlightHUDBlueprintAsset`, `FlightHUDTelemetryBinding`, `GroundConformingSuspension`, `ProfileAndWindContract`, `SystemsTestMap` 최종 `6/6 Success`, 경고·실패 0

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
- 2026-09-17 후속 화면 피드백으로 `사거리 안인데도 계속 접근`과 추적 중 몸·고개가 이동과 반대로 도는 Red를 재현했다. 최종 규칙은 실제 무기와 같은 3D 사거리 안이면 즉시 정지·사격, 밖 판정이 0.2초 지속될 때만 Pursue다. Bone Gaze는 수평 이동을 따르고, Pursue 몸 Yaw는 Character Movement가 단독 소유한다. 역할 BP가 덮은 이동 회전 플래그도 BeginPlay에서 공통 계약으로 복구한다. Editor Build와 `PersonalWeaponEngagementPolicy`, `SmartObjectFoundationDefaults`, 경계 흔들림·이동/시선 정렬·사거리 진입 정지를 포함한 `ShotgunSystemsTestMapPIE`, `NPCPerceptionSearchPIE`, `NPCGreyboxAssets` 최종 `5/5 Success`
- 2026-09-18 MSVC 14.51.36257 `DroneEditor Win64 Development` 최종 링크 Build 성공. `PersonalWeaponEngagementPolicy`, `PersonalWeaponMaintenanceTiming`, `ShotgunSystemsTestMapPIE`, `NPCGreyboxAssets`, `NPCPerceptionSearchPIE` 5개가 모두 `Success`, 실패 0이다. Maintenance 단위 테스트의 Skeletal Mesh 미지정 경고 7건은 예상 경고다
- 실제 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`의 `NPCBaseRoutinesPIE`를 `-TestLoops=4`로 반복해 4/4 Success, 오류·경고 0을 확인했다. 각 실행은 Rifle/Shotgun 순찰 2회·서로 다른 슬롯 방문과 0.35초 초과 역방향 몸/속도 불일치를 함께 검증한다
- 사용자 실제 화면에서 Rifle/Shotgun 이동과 회전 수정이 정상임을 확인했다. 저빈도 `[NPC-STATE]`·`[NPC-MOVE]` 진단은 Blueprint에서 다시 켤 수 있게 유지하되 기본값은 Off로 전환했다
- 개인화기 Controller에 Blueprint 조절형 `PersonalWeaponInitialAimDelaySeconds=1.0`을 추가했다. 최초 Sight 성공 시각부터 계산하므로 DroneDetected/Pursue/Cover 상태 왕복이 시간을 초기화하지 않으며, 지연 중 행동을 정상 유지해 StateTree 실패로 처리하지 않는다. 다른 Drone으로 표적이 바뀌면 이전 사격을 먼저 정리한다
- Figma `Project:Droner` Page 1의 최상위 148개 항목을 읽기 전용으로 재확인했다. 최신 기준은 Slide 52~53의 타이틀→미션 선택/설명→로비→드론 선택→인게임 흐름, Slide 55의 공중 Drone 공통 HUD, Slide 57~58의 Racing UI/Restart/Quit/기록·감도·리플레이 요구다. Figma 원본은 수정하지 않았다
- `BP_DroneTrainingCourse`의 CourseSpline 점 추가는 UE 5.8 기본 Visualizer가 이미 지원함을 엔진 소스와 프로젝트 구현으로 확인했다. 기존 점 선택 뒤 `Alt+이동 기즈모 드래그` 또는 선분 우클릭 `Add Spline Point Here`를 사용하며 Ring별 Spline Handle과 구분한다. 별도 코드·맵 변경은 하지 않았다
- 2026-09-18 후속 화면 보고의 Shotgun 전신 회전을 전용 교전 PIE에서 `PursueDrone` 상태의 같은 방향 누적 몸 Yaw `301~304°`로 반복 재현했다. 진단 결과 Nav 가속과 RVO는 이미 꺼져 있었지만 `bRequestedMoveUseAcceleration`은 켜져 있었고, Drone 위치에 큰 도착 반경을 둔 MoveTo가 가까운 경로 Segment를 가속으로 지나치며 몸과 시선이 짧은 코너를 계속 쫓았다. 실제 사거리 정지점·75cm 도착 반경·Pursue 전용 직접 요청 속도·몸/시선 공통 최종 목표로 수정했다. 전용 테스트에는 같은 상태에서 연속 300° 초과 회전 실패 조건, 실제 맵에는 정지 회전과 역방향 보행 실패 조건을 추가했다. 중간에 요청 가속을 전 상태에서 끄자 순찰 역방향 `0.614초`가 회귀로 잡혀 Pursue에만 한정했다. 최종 Editor Build, 완전 새 Editor 프로세스 Shotgun 3/3, 실제 Smart Object 맵 3/3과 관련 5개 테스트가 모두 성공했다. `PersonalWeaponMaintenanceTiming`의 Skeletal Mesh 없는 최소 시험 Actor 경고 7건은 예상 경고다
- 2026-09-18 실제 사용자 PIE 로그에서 `BP_NPC_Hostile_Rifle_C_0 is stuck`의 충돌 상대가 `BP_NPC_Hostile_Shotgun_C_0 Component:Gun`임을 확인했다. 런타임에 해당 `Gun`이 `collision=3 overlap=1 nav=1`인 것도 자동 계측으로 재현했고, Capsule 외 Primitive를 VisualOnly로 강제한 뒤 `NPCBaseRoutinesPIE`, `NPCGreyboxPIE`, `ShotgunSystemsTestMapPIE`가 모두 Success이며 `stuck` 로그가 없다
- 2026-09-18 첫 사격 조준 지연 추가 뒤 MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `SmartObjectFoundationDefaults`, `ShotgunSystemsTestMap`, `ShotgunSystemsTestMapPIE`, `NPCGreyboxPIE`가 Success다. Shotgun PIE는 조준 지연 완료 전 Fire Event 0과 감지 관측 시점부터 첫 Volley까지 1초 이상을 함께 검사한다
- FPV Mode 1/2 변경 후 입력 Asset 생성 로그 `mappings=33`, MSVC 14.51.36257 Editor Build 성공, `AcroInputContract`, `FlightProfiles`, 수정된 3회 `PIEInputLifecycle`, `MissionEntryPIE`가 Success다. 첫 lifecycle 실행은 새 두 Action을 기존 예상 목록에서 누락해 `31/33` Red, 두 번째는 release-binding 분류 누락으로 Red였고 테스트 계약을 고친 뒤 3/3 Green으로 전환했다
- 최종 검증 뒤 `fetch --prune`에서 팀원 `9a94f06 260918` Content 커밋을 확인했다. 변경 1,412개는 Source·Config·Plugins를 건드리지 않고 현재 AI 소스와 Shotgun/Smart Object 시험 맵에도 겹치지 않지만, `Lvl_DroneTraining`과 `Lvl_DroneTutorialSystemsTest`를 포함해 자동 Pull은 보류했다
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

- `BP_DroneRainVisual`이 RainStorm에서 파란 선 없이 짧고 부드러운 Mask 빗방울로 보이는지, Clear/비 Off에서 사라지는지, 지붕 아래에서 침투하지 않고 기본 0.35초 보간으로 줄며 밖에서 복원되는지 화면 확인
- 광섬유 Drone의 Sting 외형·1인칭·ImpactDetonation·재밍 면역, 빈 `FiberSpoolMeshComponent`에 제작 통을 넣은 뒤 통 끝 케이블의 지면 누적·처짐을 화면 확인. Ground UGV는 높은 시작점에서 지면으로 내려와 W/S/A/D/Q/E와 4점 경사 추종을 유지하는지 확인

- TestMap Gate Frame 외형과 Trigger 정합, 3상태 색
- Ring Handle 개별 이동과 Spline 투영 체감
- 한 Lap HUD 갱신과 두 Lap 이전 평균·Best·증감값
- 역할 표적 3종, Carryable 픽업·드랍과 숨긴 World Text
- 이동된 AI 시험 맵의 MG 재점유·도착 방향·Gaze·자동포탑·차량 화면 확인
- Rifle/Shotgun 병사가 사거리 밖에서 Drone을 자연스럽게 추적하고, Shotgun이 가까운 경로 코너에서 전신 회전·도리도리하지 않으며, 사거리 안에서 정지·사격하고 리시 밖에서는 포기·순찰 복귀하는지 화면 확인
- 병사 감지 후 최소 1초 안에 Cover/MG/개인화기 상태가 프레임 단위로 왕복하지 않고 현재 행동을 유지하는지 화면 확인
- Drone Rotor 축·방향·속도, 비행 기울기, 실제 탄환 피격 흔들림 등 기존 수동 회귀
- 새 TestMap의 귀환 Zone 위치/크기와 재밍 Zone Overlap·신호 경고·강한 단계 이동 체감 수동 확인
- Shotgun Systems 맵의 발광 Pellet 8개와 짧은 Tracer 분리 가시성, Cyan 선이 보이지 않는지, 이동 회피 체감, 최대 24 피해, 16m 사거리·LOS와 Hysteresis 고개 안정화 화면 확인
- `Lvl_DroneFrontEnd`의 새 3열 Mission UI와 Training 진입 뒤 3열 Drone 선택 UI가 해상도에서 잘리지 않는지 수동 확인
- FPV Rate/Acro에서 키보드 `W/S Pitch`, `A/D Roll`, `Q/E Yaw`, `Space/Ctrl Throttle` 중복 없음과 Gamepad/RC Mode 1·2, Stick 중앙 자세 유지, Roll/Loop·27m/s 체감 수동 확인
- 현재 Rate/Acro는 중력·호버 추력·기체 Up 추진·선형 항력·Rate 응답을 계산하지만 `UFloatingPawnMovement` 기반 v1이다. 모터별 RPM·PID·질량/관성 텐서·프로펠러 공력 기반 완전 물리와 같은지 확인한 상태는 아님
- Camera-follow Instanced Mesh 강우와 카메라 위쪽 Trace 기반 실내 감쇠는 구현했으나 화면 확인 전이다. 정식 Niagara GPU Rain, 젖음 MPC, Splash·Audio, 품질 단계와 Low~Epic GPU 측정은 미구현
- Test Mission DA/진입 경로에서 Return/Jammer Mission Event, 역할 Event 연쇄, 제한 시간 만료 화면 확인
- 영상 노이즈 WBP 연출과 목표 정보 손실 표현 확인
- Figma에서 `골든 타임/인터셉트/베일 브레이커/엔드게임`과 큰 목표는 확인했지만 실제 Story Mission DA/Map은 아직 없음
- 같은 Figma 파일에서 Mission 2 차량이 미끼라는 전체 설명과 탑승 차량으로 전제한 개별 화면, Mission 3에서 오마르를 처리하는 설명과 이미 처리됐다는 대사가 충돌함. 코드는 양쪽을 지원하며 저장 기본안은 사용자 결정 대기
- 광섬유 Drone·UGV의 프로젝트 소유 Definition/Integration Pawn은 구현했다. 두 외형의 스케일·조작 화면 확인, Mission 중 기체 교대, 장거리 타격 Drone, 차량 목적지 실패 Trigger와 최종 Cinematic 연결은 미구현

## 알려진 실패와 경계

- `TrainingAssets`, `TrainingPIESmoke` 실패는 팀원이 제작 중인 실제 Training 맵의 Gate/Sequence와 역할 Actor 중간 상태를 보여준다. Codex가 원본 맵을 수정해 억지로 통과시키지 않는다.
- `NPCBaseRoutinesPIE`는 수정 전 4회 중 3회 실패했지만 최종 Source에서 4/4 성공했다. 묶음 회귀에서 잡힌 성공 완료 동일 부분 경로 재요청도 차단했고, Shotgun 전용 PIE와 전체 관련 묶음 모두 Green이다. 화면상의 애니메이션 체감은 사용자 수동 확인 전까지 별도 미확인으로 유지한다.
- 유인 NPC 점유 포탑은 `BP_SO_MGTurret` 한 개다. `BP_AutoTurret_Vehicle`, `BP_AutoTurret_Emplaced`는 무인 자동포탑이다.
- 모든 `.uasset`, `.umap`은 크기와 무관하게 Git LFS 대상이다. Threshold 방식으로 일반 Git에 옮기지 않는다.
- 이 PC의 첫 TestMap Validate 실패는 9월 8일 생성 DLL이 9월 15일 Source보다 오래되어 역할 표적 BP의 C++ 부모를 못 읽은 문제였다. 최신 Editor Build 후 같은 비파괴 Validate가 성공했고 맵 Actor 삭제/재구성은 하지 않았다.

다음 행동과 완료 조건은 [`WORKBOARD.md`](WORKBOARD.md), 상세 문서 위치는 [`docs/README.md`](docs/README.md), 과거 근거는 [`docs/history/DRONE_WORKLOG.md`](docs/history/DRONE_WORKLOG.md)를 따른다.
