# Drone 작업 보드

마지막 갱신: 2026-09-17 — 개인화기 추적·리시 포기·이동 회전 안정화와 AI 핵심 회귀 완료

## Now

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| MAP-TEST-01 | 경량 Tutorial Systems TestMap 수동 확인 | 맵·생성 도구·전용 자동화·Map Check 완료 | Gate/Ring/역할/HUD 한·두 Lap 화면 확인 |
| AI-SO-TUNE-01 | Smart Object·유인 MG·개인화기 추적 화면 확인 | 최소 상태 1.0초, 실제 3D 사거리 안 즉시 정지·사격/밖 0.2초 지속 시 Pursue, 3,000cm 리시·무진행 포기, 안정된 MoveTo, 추적 몸·Gaze의 이동 벡터 정렬과 다음 Tick StateTree 복귀 구현. 정책·Shotgun PIE·`NPCPerceptionSearchPIE` Green | 화면에서 Rifle/Shotgun 사거리 밖 연속 접근, 사거리 안 진입 즉시 정지, 몸·고개·이동 같은 방향, 리시 포기, MG 사망 후 재점유 확인 |
| AI-SHOTGUN-PIE-01 | 추가 Shotgun NPC 사격 체감 확인 | 실제 8 Projectile·12° 반각, Pellet당 3 피해, 상호 충돌 방지, Cyan Debug 기본 Off, 발광 비드/Tracer·3°/6° 시선 Hysteresis·Asset/PIE 자동화 완료 | 발광 비드 8개 분리 가시성·Cyan 선 제거·회피·최대 24 피해·사거리·LOS·시선 안정화를 Editor 화면에서 확인 |
| UI-FLOW-PROTOTYPE-01 | Mission/Drone 선택 임시 UI 확인 | 첨부 와이어프레임 기반 3열 C++ fallback 구현, `FrontEndPIE`·`MissionEntryPIE` 통과 | 16:9 화면에서 작전 목록/설명/시작과 기체 목록/상세/설정/출격이 잘리지 않는지 수동 확인 후 최종 WBP·Thumbnail 범위 결정 |
| MISSION-RULE-PIE-01 | 새 목표 Rule의 실제 맵 Vertical Slice | 귀환·Jammer·역할 Actor 시험 배치 완료, 직접 실행은 Prototype Flow | Test Mission DA/진입 경로에서 Scan/Delivery/Destroy/Return/Jamming Event·Tag·시간 규칙 확인 |
| STY-03-PIE-01 | 재밍 신호·비행·HUD Vertical Slice | 35%/80% 겹침 Zone TestMap 배치·저장 계약 완료 | 실제 비행으로 Overlap·HUD·둔화/복원 확인. 영상 Noise WBP는 별도 표현 작업 |
| STORY-BRANCH-01 | Mission 2→3 양쪽 스토리 분기 | Story Fact 저장·성공 적용·조건 목표 필터, 미끼/실제 탑승 양쪽 자동화 완료 | 사용자가 기본 스토리안을 정하면 실제 Mission DA에 Fact 설정 |
| DRONE-FIBER-01 | 광섬유 Drone 기반 | `JammingImmunity` Capability→Signal 동작 연결·자동화 완료, 실제 Definition/Pawn 없음 | 프로젝트 소유 Definition/Integration Pawn과 Visual 연결 후 Zone PIE |
| DR-FPV-ACRO-PIE-01 | 고기동 FPV 실제 조작 체감 | Rate/Acro 각속도·무수평복귀에 중력·호버·Body Up 추력·선형 항력·Rate 응답 v1 연결, FPV Data Asset·Prototype 8/8 완료 | 키보드/패드로 Nose-down 전진력, 호버·상승·무추력 하강, Roll/Loop와 650°/s 체감 확인 후 수치 조정 |
| DR-FPV-ACRO-INPUT-02 | Acro 키보드·패드 축 분리 | 전용 Action 4개, IMC 33 Mapping, Pawn 분기, Editor Build와 Prototype 8/8 완료 | 키보드 W/S Pitch·A/D Roll·Q/E Yaw·Space/Ctrl Throttle와 패드 Mode 2를 화면에서 확인 |
| WTH-02-PIE-01 | 바람 Vertical Slice 체감 | 24개 이동 Bead·풍속/풍향/모드 Readout·1/2/3 모드 키·전용 TestMap 자동화 완료 | 표시 방향과 실제 Drift, 세 모드 보정 차이, 순풍·역풍·횡풍과 돌풍 세기 화면 확인 |
| WTH-02B | 자연스러운 바람 전환·표시 | 돌풍 Attack/Release·풍향 최단각 응답, 표시 속도 보간·벡터 적분, Bead 방향/길이 변화 구현. Weather 3/3 완료 | Weather TestMap에서 방향 전환 무점프·속도/길이 변화와 LightWind/RainStorm 체감 확인 |
| WTH-03 | 비 표현 Vertical Slice | Snapshot 비 값과 최적화·품질 계획 완료, 표현 자산 없음 | Camera-follow Niagara Rain·MPC Wetness·Audio를 붙이고 Low~Epic GPU 측정 |

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

- `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`: 순찰·감지·수색·MG·자동포탑·차량
- `/Game/Drone/Maps/TestMap/Lvl_DroneMissionSystemsTest`: 재밍 약/강/겹침·Return Zone·역할 표적
- `/Game/Drone/Maps/TestMap/Lvl_DroneShotgunSystemsTest`: 추가 Shotgun NPC·작은 Pellet 8개/Tracer·탄약·LOS 사격장
- `/Game/Drone/Maps/TestMap/Lvl_DroneWeatherSystemsTest`: LightWind 지속풍·돌풍, 이동 Bead·풍속/풍향 표시, `1/2/3` 조작 모드별 보정

## Next

1. 수동 확인에서 발견된 Gate/HUD/역할 결함 수정 후 TestMap 회귀
2. Shotgun Systems 맵에서 작은 Pellet/Tracer 8개가 분리되어 보이는지와 Cyan 선 제거·12° 확산·회피 가능 탄속·피해·사거리·LOS를 수동 확인
3. Front-end와 Drone 선택 3열 UI의 해상도별 잘림·버튼 상태를 확인하고 최종 WBP Designer/Thumbnail 작업 범위를 확정
4. 이동된 AI 시험 맵에서 Rifle/Shotgun의 사거리 밖 추적·이동 방향 Yaw·리시 포기/순찰 복귀와 병사 상태 최소 1초 유지, MG 사망 후 재점유를 화면 확인
5. 새 Mission Systems 맵에서 재밍 HUD·둔화/복원·역할 기능·Return 크기 수동 확인
6. FPV Rate/Acro 키보드 전용 축과 Gamepad/RC Mode 2로 호버·기울기 추진·무추력 하강·Roll/Loop를 수동 확인하고 호버 스로틀·항력·Rate 응답·감도·Expo를 체감 조정
7. Weather Systems 맵에서 개선된 Bead의 방향 전환 무점프·풍속별 길이와 `1/2/3` 세 조작 모드 Drift·LightWind/RainStorm 돌풍을 수동 확인
8. `WTH-03` Camera-follow Niagara Rain·MPC Wetness·Audio·품질 단계를 연결하고 GPU 측정
9. Test Mission DA와 개발용 진입 경로를 추가해 Return/Jammer Mission Event를 실제 PIE로 확인
10. Mission 1 검증용 DA/Map에서 Drop→요원 전달→선택적 정보 회수→시간/파괴 실패 Vertical Slice
11. 이동 차량 목적지 실패 Trigger와 Mission 2 FPV 격파/Story Fact 적용 Vertical Slice
12. 광섬유 Drone·UGV 프로젝트 소유 Definition/Pawn 기반과 Mission 중 기체 교대 계약 구현. 외부 에셋은 Visual만 연결
13. 중간/강한 재밍의 실제 영상 Noise WBP와 목표 정보 손실 규칙 구현. 현재 `VideoNoiseIntensity` Snapshot·BP Event까지만 있음
14. 나머지 시험 맵은 소유권·참조 감사 후 AssetTools로 이동. `test1`·`test2`는 용도 확인 전 유지
15. Mission 2의 미끼/실제 탑승 중 기본 스토리안 확정 후 Story Mission DA에 반영. 코드는 양쪽 지원

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
| FPV Rate/Acro | Mode 2+Actual Rates형 각속도, 자동 수평 복귀 없음, 중력·호버·Body Up 추력·항력·Rate 응답 v1, FPV DA 27m/s·650°/s 기준, Prototype 8/8 성공 |
| Acro 입력 분리 | 키보드 W/S Pitch·A/D Roll·Q/E Yaw·Space/Ctrl Throttle, Gamepad Mode 2 전용 Action 4개와 IMC 33 Mapping, Prototype 8/8 성공 |
| 기상 데이터·바람 Runtime | Profile/Snapshot/Subsystem·Controller·Drone Response, 저장 Profile 3종, TestMap·Map Check·기상 자동화 3/3 성공 |
| 차량 바퀴 회전축·접지 교정 | 실제 Tire Mesh의 옆 회전을 부모 공간 +Y 차축으로 교체하고, 30cm 반지름 때문에 약 20cm 잠기던 BP를 52cm로 교정. 축·Bounds·평면 접지 Red→Green과 맵 Validate 통과, 화면 재확인 대기 |
| Shotgun Pellet 가시화 | 실제 8발·12° 확산, Pellet당 3 피해, 전용 BP의 주황 발광 `0.04` 비드와 `0.20 × 0.0125` Tracer, 집중 회귀 성공 |
| 개인화기 정면 시선 안정화 | 몸 Yaw와 Bone Gaze 공통 3° 데드존, 1.9° 좌우 표적 왕복 회귀 Red→Green, Blueprint 역할별 조정 가능 |
| 병사 상태 전환 안정화 | 공통 최소 유지 1.0초, 유지 중 사격·점유·이동 조건 재점검, MG 재시도 Event 지연, 사망·파괴·Lost 확정 즉시 정리. 후속 추적 안정화 뒤 MG 재점유 포함 전체 PIE Green |
| 개인화기 추적·포기 안정화 | Fire/Pursue/Disengage 정책, 실제 3D 사거리 안 즉시 정지·사격, 밖 판정 0.2초 확인 뒤 Pursue, Nav 투영, 같은 목적지 MoveTo 중복 방지, 3,000cm 리시·2.5초 무진행·복귀 Cooldown, 추적 몸·Gaze 이동 벡터 정렬, StateTree 다음 Tick 재시작. 집중 회귀 성공 |
| Weather TestMap 가시화 | BP 조절형 Visualizer, 이동 Bead 24개, Profile/풍속/풍향/모드 Readout, 1/2/3 비교 키와 Map Check 0/0 |
| 자연스러운 바람 전환 | Gust Attack/Release·풍향 최단각 응답, 표시 속도 벡터 적분, 풍속별 Bead 방향/길이, Weather 3/3 성공 |
| 비 기획 | Camera-follow GPU Rain·Effect Type·젖음/실내/Splash 최적화 계획과 Snapshot 표현값. Niagara/MPC/Audio는 다음 작업 |

시험 맵 사용법은 [`docs/gameplay/DRONE_TEST_MAP_GUIDE.md`](docs/gameplay/DRONE_TEST_MAP_GUIDE.md), FPV 조작은 [`docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md`](docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md), 기상은 [`docs/gameplay/DRONE_WEATHER_WIND_RAIN_PLAN.md`](docs/gameplay/DRONE_WEATHER_WIND_RAIN_PLAN.md), Mission Rule 설정은 [`docs/gameplay/DRONE_MISSION_OBJECTIVE_RULE_GUIDE.md`](docs/gameplay/DRONE_MISSION_OBJECTIVE_RULE_GUIDE.md), 전체 순서는 [`docs/planning/DRONE_TUTORIAL_STORY_PLAN.md`](docs/planning/DRONE_TUTORIAL_STORY_PLAN.md)를 참고한다.
