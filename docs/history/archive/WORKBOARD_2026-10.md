# WORKBOARD 원문 아카이브 — 2026-10

2026-10-04 Codex 문서 정리. 아래는 당시 기록이다. 원문 이동, 상대 링크 경로만 조정했다. 현재 상태는 루트 WORKBOARD·STATUS를 따른다.

## 날짜별 최신 기준·앞선 점검

2026-10-04 새벽 최신 기준: C PC Unreal HEAD=추적 origin/main `41444c2` + 로컬 미커밋, pull·LFS 실제 본문 확인은 Claude 지시서 근거. 조사/C++/Build/테스트 Claude, Scout·Drop BP 입력 연결 Codex(ui)→Claude 검증, IMC Dead Zone은 Codex MCP 저장 없이 복구→Claude headless Python 패치. Build Succeeded(지시서), RenderOffScreen 1920×1080 집중12/12 Success·화면 그려진 기준 회귀94개 중90 Success/기존4 Fail(ClaudeAcro/test_after_dz.log·ClaudeAcroFull/test3.log, Codex 로그 대조). Acro 체감/Scout·Drop 비행·첫 버튼 강조 수동 대기, 레이싱 지형 연결/조작 방식 미정. 포커스 수정 후 확인 중·미렌더 원인 미특정. 앞선 검사/날짜별 이력 보존, 최신 요약은 STATUS.

2026-10-02 새벽 후속 최신 기준: C PC Unreal ec2e88f + 로컬 미커밋, 작업 도구 Claude·문서/Space 반영 Codex. TUT-PROGRESS-01 다음 수업·시간·n/8·전체 완료 구현·신규 렌더 검사 3건 Success·수동 확인 대기. NextMissionId로 튜토리얼 8·Story M1→M4 연결(DA 12/12 저장·재조회, 맵 미수정), 완료 기록은 이번 실행만 유지. 전체 RenderOffScreen 1920×1080 회귀 87개 중 81 Success·6 Fail(ClaudeTutProgressFull/test2.log). 기존 NPC 감지/Production 2건과 아래 렌더·레이아웃·Route 순서 의존 카드 3건을 구분한다. M2→M3 결과 분기·4-1/4-2 통합·미기재 브리핑 문구·완료 영구 저장은 현재 미정. 아래 앞선 검사는 당시 범위로 보존한다.

2026-10-02 새벽 최신 기준: C PC Unreal ec2e88f + 로컬 미커밋, 작업 도구 Claude·문서/Space 반영 Codex. NPC 테스트 갱신 3/4 Success·감지 유지 Fail 1건은 AI-PERCEPTION-TEST-01로 실기 비교. 브리핑 자막/음성 슬롯·배터리/HUD·Best Lap JSON 저장 구현·자동 검증 완료, 음원/튜토리얼 대사·실기 확인 대기. Asset Manager AlwaysCook 자동 검증 완료·실제 패키징 미실행. 기체별 배터리 시간/소진 처리/신호 대역·스토리 분기·레이싱 방식 현재 미정. 아래 10/01 회귀는 당시 검사로 보존한다.

2026-10-01 밤 후속 최신 기준: C PC Unreal ec2e88f + 로컬 미커밋, 작업 도구 Claude·문서/Space 반영 Codex. UI-PAD-01·MISSION-CHECKPOINT-01 구현·자동 검증 완료, 실제 PS4 패드·강조·재출격 체감 수동 확인 대기. RenderOffScreen 1920×1080 패드 11/16단계·레이아웃(최대 0.255px) Success. NullRHI 체크포인트·FailureResponseData Success, 전체 Drone.* 80개 중 Success 73·기존 실패 7(NPC 개수 4·렌더 진단 1·Production Training 2), 패드 2개는 렌더링 필요 경고로 건너뜀. 맵 체크포인트 미배치라 현재 첫 출격 위치에서 재출격. M1 픽업 지점은 정보단말 회수 구현 뒤, 재출격 브리핑은 MISSION-BRIEFING-02 뒤이며 재생 여부 현재 미정. 아래 앞선 밤/저녁 검사는 당시 범위로 보존한다.

2026-10-01 밤 최신 기준: C PC ec2e88f + 지시서 지정 미커밋 Source/테스트(목록은 STATUS 밤 절), 작업 도구 Claude·문서 반영 Codex. Shotgun 실기 감지 정상(사용자 확인), 시험 장면 수정 후 NullRHI 5/5 Success. 미션 Catalog 자동 등록 구현·Build Succeeded·Flow/Mission/진입 15/15 Success. 렌더 진단은 NullRHI samples=0으로 판정 불가(로그 Fail, 15/15에서 제외). 새 DA 실제 로비 등록·1280/1920 수동 확인 대기. 패키징 쿠킹 미구현. 아래 저녁 전체 75개 판정은 이전 검사이며 밤 결과로 전체 Pass를 추정하지 않는다.

2026-10-01 저녁 당시 기준: C PC Unreal `ec2e88f` + 로컬 Source 3파일. 작업 도구 Claude, 문서 반영 Codex. Editor Build 성공(우리 코드 경고 0·엔진 헤더 C4996만). 전체 `Drone.*` NullRHI 75개는 성공 62·경고 동반 성공 4·실패 9이며 전체 Pass가 아니다. `LobbyLayoutStabilityPIE`와 `HoverMissionPIE` 수정 후 Success, FrontEnd/진입/복귀 회귀 Success. 기존 Production Training 맵 중간 상태·NPC 고정 개수 테스트와 Shotgun 시험 장면 실패(밤에 정정·수정 완료)를 구분한다. 후속 3건(재사용 줄바꿈 재적용·WBP 상시 스크롤바·폭 160→270)은 처음엔 Editor/Live Coding 때문에 Build가 거절됐으나, 사용자가 Editor를 닫은 뒤 Build 성공, RenderOffScreen 1920×1080 `LobbyLayoutStabilityPIE`·`FrontEndPIE`·`FrontEndContract`·`MissionEntryPIE`·`BackNavigationContract`·`HoverMissionPIE` 6/6 Success, 로비 최대 이동 0.255px로 자동 검증됐다(근거: `C:\URproject\drone\Saved\Automation\ClaudeRecheck5\`). 1280/1920 가독성과 Story 목록 상시 스크롤바 칸은 수동 확인 대기다. 전체 판정·Figma 새 항목은 [STATUS](../../../STATUS.md)의 저녁 절을 따른다.

아래 같은 날 앞선 점검 문단은 당시 근거이며 최신 기준은 밤 문단과 카드 상태를 따른다.

앞선 점검 당시 C 드라이브 PC의 Unreal `9f67706`, 문서 `ff69c11`이 실제 원격 main과 일치한다. 점검 시작 두 저장소 Clean/0/0이며 후속 UI·설정 코드도 수신됐다. 이번에는 MD·Space만 갱신하며 코드/자산·Build·Commit/Push는 수행하지 않는다. [현재 상태와 작업 위치](../../../STATUS.md)

이전 D 드라이브 PC의 UI 집중 **5/5 Success**와 렌더 목록 튐 진단 **Fail**은 서로 다른 검사이며 해당 원시 보고서는 현재 C PC에 없다. C PC의 기존 GameReadiness 32 Success·Back 32 Success + 경고 동반 성공 1·TitleLobbyOrbit 14 Success 보고서는 직접 읽었으나 최신 UI 이전 검사다. 이번 Build/자동화 재실행·수동 Pass는 없다.

이번 후속 구현: 목록/카드/설명 3열 로비, 기체 상단 상세·하단 가로 카드, 결과 복귀 분류 유지, Master 음량·화면 모드/해상도·품질·VSync·FPS 설정의 적용/기본값/취소. 수업·Story 목표 로직과 Production Training은 변경하지 않았다. [UI·설정 가이드](../../gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md)

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
| FPV Rate/Acro | 송신기 Mode 1·Mode 2, Actual Rates형 각속도, 자동 수평 복귀 없음, 공통 질량·합산 추력·모터 응답·Body Up 추진·선형/제곱 항력 v2. 속도는 현재 DA/BP·적재 상태 기준이며 초기 27m/s를 고정값으로 사용하지 않음 |
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
| 광섬유·지상 Drone 기반 | 프로젝트 소유 Definition/Integration BP, 광섬유 Drone은 DroneSpy Body+Rotor 4·GSU 통 장착·통 상단 다점 곡선 케이블·면역/자폭. Ground UGV는 지면 획득·4점 접지·차체 독립 Turret/Camera·총/유탄 Anchor, 5종 선택 Flow. 과거 초기 기반 회귀 뒤 GSU 변경 ExtendedRole 1/1 성공 기록 |
| 강우·실내 감쇠 Greybox | OilRig Mask 기반 Plane 최대 112개, 기본 65×2.4cm·Opacity 0.22·개별 크기 편차, 위쪽/표면 Trace·0.35초 실내 감쇠, Weather 4/4·Map Check 0/0. 화면 확인 대기 |
| 강우 Snapshot 디버그 프리뷰 | 전용 Weather TestMap 7/8/9 프로파일 전환은 유지하되 구형 파란 DrawDebug 선분은 기본 `Off/0개`다. Rain Visual과 겹치지 않으며 진단할 때만 수동 활성화 |
| 비 기획 | Camera-follow GPU Rain·Effect Type·젖음/실내/Splash 최적화 계획과 Snapshot 표현값. Niagara/MPC/Audio는 다음 작업 |

시험 맵 사용법은 [`docs/gameplay/DRONE_TEST_MAP_GUIDE.md`](../../gameplay/DRONE_TEST_MAP_GUIDE.md), Mission BP 배치는 [`docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md`](../../gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md), FPV 조작은 [`docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md`](../../gameplay/DRONE_TYPES_AND_CONTROL_MODES.md), 기상은 [`docs/gameplay/DRONE_WEATHER_WIND_RAIN_PLAN.md`](../../gameplay/DRONE_WEATHER_WIND_RAIN_PLAN.md), Mission Rule 설정은 [`docs/gameplay/DRONE_MISSION_OBJECTIVE_RULE_GUIDE.md`](../../gameplay/DRONE_MISSION_OBJECTIVE_RULE_GUIDE.md), 전체 순서는 [`docs/planning/DRONE_TUTORIAL_STORY_PLAN.md`](../../planning/DRONE_TUTORIAL_STORY_PLAN.md)를 참고한다.


## 종료된 요청의 당시 범위

구현 작업은 각 단계 안에서도 1~3시간 규모의 기능/검사로 나눈다. 이번 요청에서는 계획과 문서만 최신화했고 위 코드 수정이나 시험은 실행하지 않았다.

## 완료·대체 카드 현재 상태

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| ASSET-BANGKOK-01 | Bangkok City 맵 삭제로 종료 | 종료(맵 삭제). ec2e88f(10/01 팀원)에서 Lvl_BangkokCity.umap 삭제, 10/04 사용자 의도된 삭제 확인. 9월 D PC 이식/Map Check0/0은 당시 근거 | Editor 확인 지시 종료. ThirdParty/BangkokCity 의존987개·LFS약11.46GiB 정리 여부는 사용자 결정 |
| UI-TITLE-LOBBY-02 | 이전 타이틀 UI 기획 대체됨 | 10/03 회의 타이틀5메뉴(스토리/레이싱/튜토리얼/설정/종료)·분류 직접 진입으로 대체됨 | 현재 UI-MEETING-LOBBY-01을 따른다. 로비 탭·LB/RB 최종 유지 여부 미정 |
| UI-DATA-COPY-01 | 레이싱 DA 설명·재실행 안전 | 처리됨(10/04 C PC Claude). ConfigureDroneTitleLobby.py 현재 DA 문구로 정정, Best Lap 미구현으로 되돌리지 않음. Heading/GateFlight 값 일치(ClaudeCourse/lobby_cmp.log) | Best Lap 재실행 수동 확인은 TUT-BEST-01, 정식 경기 규칙 미정 |


## 2026-10-05 WORKBOARD 다이어트 — 기준 2026-10-05

현재 카드의 긴 근거·완료/종료 행·수동 맵 안내·지난 Next를 포함한 이동 전 원문 절이다. 현재 카드·결정·Next는 루트 WORKBOARD를 따른다. 아래 원문은 수정하지 않았다.

### 회의 후 역할별 카드

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| TUT-COURSE-SMOOTH-01 | 장거리 코스 표시선 곡률 분할·BP 표시 예산 | 구현됨·자동 검증됨·수동 확인 대기(10/04 C PC Claude). Production 읽기 전용 측정: Scale2·로컬9.6km/월드19.2km·92 CurveAuto, 기존256조각 약75m·최대오차7.9m/95%2.3m. 긴 코스만 sqrt(곡률)+15% 균일 배분. MaximumCourseLineSegments 기본1024(16~4096), 시작값·미확정. Production 측정 최대50cm/95%7cm, 재생성256 46ms/1024 258ms(로드/BeginPlay 1회). BP 드래그 재구성 Off·BP만 저장, 맵 미저장. CourseLineAdaptiveSegments Success | 팀원 Production 코스 외형·급커브/끝 연결·Editor 편집 체감 수동 확인. BP2048(측정 최대20cm) 검토 가능. 짧은 TestMap68/113조각 기존 균일 분할 유지·Production 저장/재생성 금지 |
| ACRO-MEETING-01 | Mode1 Space 하강·반전 및 키보드/패드 겹침 수정 | 구현됨·자동 검증됨·수동 확인 대기(10/04 C PC Claude). 키보드/패드 Action이 한 변수에 나중 값을 덮던 원인 재현: Space+오른쪽-0.5→스로틀-0.38, W+왼쪽-0.5→피치-0.38. Pawn 입력원 분리·절댓값 큰 쪽 사용, 키 해제 시 패드 인계. AcroInputBehaviorPIE D구역8시나리오 Success(overlap_before 4Fail→overlap_after/review_fix_test). 기존 DZ0.2/1.0/Radial·Scout/Drop6Action·정확 적분 보존 | Mode1 스틱에 엄지를 걸친 채 Space→상승, 키 떼고 스틱→패드 조종, 모두 놓으면0을 실제 장치로 확인. Mode2도 혼합 입력 확인. W/S·A/D·Q/E·Space/Ctrl은 두 Mode 동일; 키보드 배율·Angle·마우스Yaw·회의 반전 뜻 현재 미정 |
| UI-FOCUS-RACE-01 | UIOnly 루트/버튼 지연 포커스 경쟁 | 수정 후 확인 중(10/04 C PC Claude). FDroneGamepadFocus가 포커스 후5프레임 감시·루트/없음 이탈만 복원, 다른 강조 버튼 이동 보존. 화면 그려진 수정 전 final.log Fail/후 test3.log Success 각1회; 단독 혼재. NextLesson 실패에 강조/Slate 위젯 이름 진단 추가. 수정→확인2회에서 중단 | 실제 결과·타이틀 첫 버튼 강조 반복 확인 및 화면 그려진 회귀 추가 관찰. 패드 다른 버튼 이동을 빼앗지 않는지 확인, 안정화 완료로 추정하지 않음 |
| TEST-RENDER-UNPAINTED-01 | PIE 미렌더 판정 구분 | 오늘10회 중8회 미렌더(10/04 C PC Claude). 최신 Drone.*97개중86 Success·11 Fail(ClaudeInterviewFull/test.log). 포커스6개 판정제외·당시 나머지5개(후속 Shotgun 해결·전체 재실행 아님). 표지는 LobbyLayout samples=0만, Shotgun 제외·known-test-failures 갱신 | 화면 그려진 포커스 확인 대기·같은 증상2회 상한·Production 보존 |
| RACING-TERRAIN-LINK-01 | 팀원 지형 코스와 제품 레이싱 연결 결정 | D-5 결정(2026-10-05 사용자): 코스4개 전제, 맵 선택 → 기체 선택 → 시작 → 스타트 지점 → 화면 중앙 3·2·1 카운트다운 → 체크포인트(레일) 모두 통과 시 완주 → 기록 결과 창. 구현 대기·실제 지형 현재 미정. 기존 조사(10/04 C PC pull41444c2 뒤 Claude): MWLandscapeAutoMaterial Island/MountainRange 계열 코스1개·PlayerStart 없음. 아이템/Gate는 맵·DA 참조 없음. 제품 DA는 TestMap/Lvl_DroneRacingTest 유지, 맵 미수정 | 사용자/팀원 실제 지형 결정 후 Claude가 확정 흐름 연결·검증. 사람 코스/Production Training 보존, 문서 최신화로 맵 재생성 안 함 |
| UI-MEETING-LOBBY-01 | Claude 5메뉴/포커스 계약·Codex BP 연결 | 구현됨·자동 검증됨·수동 확인 대기(2026-10-03 밤 C PC). Story/Racing/Tutorial 진입 전 분류·중간 화면 없음, TitleMenuClass 저장 연결. TitleFiveMenuPIE/WidgetPIE·패드 흐름 Success, 이전 남은 C++ 연결 닫음 | 실제 패드 상하 순환·5개 진입/설정3·진입 메뉴 복귀·B/Esc 반복, 1280/1920 위젯 크기 확인. 종료 자동화는 Dispatcher 연결만 검사. 로비 탭/LB·RB 유지 여부 현재 미정 |
| UI-CONTROL-DISPLAY-01 | Claude 설정/축/HUD·Codex 입력 표시 BP 연결 | 구현됨·자동 검증됨·수동 확인 대기(2026-10-03 밤 C PC). 조종 입력 표시 수동 ON/OFF·적용/취소/기본값·SaveGame, ControlInputDisplayClass 저장 연결·ControlInputDisplayPIE Success. D-3 기본값 결정은 아래 결정 표 참조(기존 False와 일치) | 실제 패드·1280/1920 위치·저장/재실행·기본값 복원 확인, 고도계 독립. 장치 자동 전환·혼합 입력·분리/재연결 정책 결정 필요. 자동화 슬롯은 DroneAudioSettings_Automation |
| RACING-MEETING-01 | 제품 Racing 숫자키 노출 분리·지형 연결 확인 | Lvl_DroneRacingTest RouteSelector 없음·숫자키 미노출, 보호 스위치/TrainingRouteKeyPolicy 자동 Success. 10/04 C PC pull41444c2·LFS 실제 본문 수신(Claude). 팀원 Island/MountainRange 코스1개·PlayerStart 없음, 아이템/Gate 맵·DA 참조 없음 | 제품1~5 차단·직접 시험/Tutorial/Training/Story·랜덤 보존. D-5 흐름은 RACING-TERRAIN-LINK-01 참조. 실제 지형 결정 후 연결·검증(구현 대기) |
| INTERVIEW-CLEANUP-01 | 면접 대비·참조0 정리 반영 | Claude58건 점검·14건 처리, StateTreeCookContract/PlayerFacingTextContract/FrontEndContract/FlightProfiles 통과·Build Succeeded. 코드/도구 정리 완료·전체97개중86 Success(미렌더 제한) | 패키징·실제 패드 수동 대기, 결정 표 확정 후 후속 코드 작업을 Claude에 인계 |
| MCP-LOCAL-01 | MCP 공유 Default 자동 시작과 연결 | 공유 Config/DefaultEditorPerProjectUserSettings.ini bAutoStartServer=True·8000/mcp가 모든 PC에 적용. 10/03 C PC 연결·약560px 타이틀 캡처는 당시 확인 | D-14 결정은 면접 대비 9번 참조·구현 대기. Claude 루트 .mcp.json·자동화8010, 현재 실제 패드/해상도 수동 대기 |

### 결정 필요 — 현재 DA 값은 채택 사양이 아님

| 항목 | 필요한 결정/자료 | 현재 처리 |
|---|---|---|
| M2 | 실제 타겟 탑승 vs 미끼 결말·시스템 성공/실패·다음 Story Fact | D-1 보류(2026-10-05 사용자): 기획자 내용 대기. 양쪽 분기 기반 유지, M3 반대 분기 첫 대사 비어 있음 |
| M3/M4 | 타겟·적·드론 수량, 성공/실패, 제한·재출격·결과 카메라 | D-2 보류(2026-10-05 사용자): 기획자 내용 대기. M4 시험값 표적3·재출격0(무제한)는 채택 사양 아님 |
| 조종 입력 표시 | 기본값, 장치 자동 전환, 혼합 입력·연결 해제/재연결 | D-3 결정(2026-10-05 사용자): 기본 끔(False), 설정에서 ON/OFF. 기존 구현과 일치·수동 확인 대기. 장치 자동 전환·혼합 입력·연결 해제/재연결 정책 현재 미정 |
| Tutorial | 회의 4개와 수업 ID 8개의 집계 단위, 권장문구/건너뛰기·완료 영구 저장 | D-4 결정(2026-10-05 사용자): 수업 1~8 그대로 유지. 회의안의 “4”는 레이싱 코스 4개로 해석. 권장문구/건너뛰기·완료 영구 저장 현재 미정 |
| md 공개 범위·개인정보 | PROJECT_EXPERIENCE_PLAN_HWP_GUIDE의 기업 주소·대표자·팀원 실명·예산·로컬 경로(이미 원격 Push됨) 처리 여부 | D-9 종료(2026-10-05 사용자 결정): 비공개 유지, Git 기록 재작성 없음. applications 내용 미수정 |
| OpenRouter | 9/17 대화의 API 키 폐기 여부 확인 | D-10 종료(2026-10-05 사용자 결정): 결제수단 없음·미사용으로 무시·삭제. 키 정리는 사용자 직접, 저장소 작업 없음·키 값 읽지 않음 |
| Bangkok 의존 자산 | ThirdParty/BangkokCity 987개·LFS약11.46GiB 정리 여부 | D-13 결정(2026-10-05 사용자): 방콕 잔여 약11.4GB·987파일 삭제, 실행 대기. 나머지 목록은 면접 대비 7번 참조 |
| 콘텐츠/전시 | 캐릭터 메시·관찰 시점 적용 맵·조종기 비치/책임, 기록 등급, 브리핑 실명/납품일, 행사일 | 임의 실명·수치·마감일 없음 |



### 면접 대비 결정 필요 — 영향 순서(10/05, 결정·구현 대기 구분)

| 항목 | 필요한 결정/자료 | 현재 처리 |
|---|---|---|
| 1. 제3자 구매 자산 약51GB | GitHub 공개 여부 확인 후 비공개 전환 또는 자산 분리·출처 목록 | D-7 결정(2026-10-05 사용자): 비공개 전환 방향, 사용자가 GitHub에서 직접 전환. 팀원 접근 가능 여부는 GitHub 설정에서 확인 필요(이 PC gh 없음). 향후 공개 시 빌드·코드·영상만(구매 에셋 제외). 10/05 C PC Claude 비로그인 curl HTTP 200 공개 상태 관찰은 이전 전달 근거 |
| 2. 본인 기여와 AI 활용 설명 | 본인 설계·결정·검증 범위를 먼저 확인하고 README에 정직하게 정리 | D-8 결정(2026-10-05 사용자): 본인 기여·AI 활용 README는 md 저장소에만 둠, drone 저장소에는 넣지 않음. 작성 대기·이번 결정만 기록, 본인 담당 범위 미확인 |
| 3. 포트폴리오 루트 README | 플레이 방법·설계/기여·검증 근거·용량/출처를 담을 범위 결정 | D-8 위치 결정은 위 2번 참조. Unreal 루트 README 부재, 이번 신규 작성 안 함 |
| 4. main 상시 실패 테스트4개 | 별도 그룹 분리 또는 조건부 건너뛰기 여부 | D-11 결정(2026-10-05 사용자): 상시 실패 테스트4개 별도 그룹 분리, 구현 대기. NPCPerception·LobbyLayout 진단·TrainingAssets/TrainingPIESmoke; Shotgun 해결 |
| 5. Prototype Pawn 분리·명명 | h875/cpp2410줄 분리 범위/순서 및 Prototype/Greybox 변경 시점 | D-12 결정(2026-10-05 사용자): 분리·명명 지금 진행, 구현 대기. 리디렉터·참조 검사 후 커밋만(푸시 금지). Legacy는 아래 6번 |
| 6. Legacy 템플릿 | C++76파일·자산100개 정리 범위 | D-12 결정(2026-10-05 사용자): Legacy 정리 지금 진행, 구현 대기. 리디렉터·참조 검사 후 커밋만(푸시 금지) |
| 7. 방콕·미사용 자산 | Bangkok 잔여987개 약12GB와 다른 구매/팀원 자산 정리 | 방콕 삭제 결정·실행 대기는 위 D-13 참조. 나머지 참조0 폴더7개 약5.1GB 사용자 결정 대기: `E:\기획안\06_드론_메인\미사용자산_목록_D13_20261005.md`. 판정 출처: `C:\URproject\drone\Saved\Automation\unused_packs.json`(지시서 근거) |
| 8. 풍향 기준 | HUD 방위와 거울상 불일치, 불어오는 쪽 기상 관례 채택 여부 | D-6 결정(2026-10-05 사용자): 풍향은 기상 관례(불어오는 쪽), 적용·검증 대기. 배터리는 미션별 제한 + 방전 시 추락 추가(구현 대기·시간 값 미정). 높이 제한은 C++·문서에서 구현을 찾지 못해 미구현으로 기록(BP 전용 여부 미확인; Claude 지시서 근거) |
| 9. 공유 Config MCP | 모든 팀원 PC의 8000포트 자동 시작 유지 여부 | D-14 결정(2026-10-05 사용자): 공유 Config의 MCP 자동 시작 끄고 사용자 PC 로컬 설정에서만 켬, 구현 대기 |
| 10. BP/Legacy API | 호출 없는 함수19개·1회 접근자71개가 디자이너용인지, 핸들링 Legacy 정리 | 참조0 확정 삭제분과 구분, 추가 삭제 결정 대기 |

스냅숏 백로그 GIT-LFS-CAP-01·AI-TOOL-REVIEW-01은 현재 카드 없음(09-15 스냅숏), 복원/보류/폐기 결정 대기.

날짜별 최신 기준·앞선 점검은 [10월 보드 아카이브](docs/history/archive/WORKBOARD_2026-10.md)에 원문 보존했다.

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| TUT-PROGRESS-01 | 튜토리얼 클리어 시간·다음 수업·n/8·전체 완료 UI | 구현됨·자동 검증됨·수동 확인 대기(2026-10-02 새벽 C PC Claude). NextMissionId 튜토리얼 8·Story 4 연결, S48/S49 결과·로비 순서/완료 표시, Director 시간(재출격 포함), 완료 기록 실행 메모리. TutorialProgression/NextLessonPIE/CompletePIE 3건 Success, DA 12/12 저장·재조회(ClaudeTutProgressFull/test2.log·ClaudeTutProgress/py.log·py2.log) | 결과 글자/배치·실제 8수업 연속 진행·로비 완료 가독성·S49 미션 진행→M1/시작 메뉴→타이틀 수동 확인. 별도 WBP 4개 없음, Production Training 보존 |
| TUT-BRIEFING-TEXT-01 | 튜토리얼 조작키 브리핑 문구 결정·입력 | 미구현·문구 현재 미정. Codex research 2026-10-02: 8수업 키보드 키, 자폭/드랍/UGV NPC/포탑 패드 키·대사, 튜토리얼 화자 Figma 미기재. 호버/전진/회전/게이트 패드 브리핑 원문 있음. 이번 조작키 브리핑 미입력 | 사람이 미기재 문구·화자를 결정한 뒤 Claude가 DA/UI 연결·검증, Story 허브를 튜토리얼 화자로 추정하지 않음 |
| TUT-COMPLETION-SAVE-01 | 완료 수업 기록 영구 저장 여부 | 현재 미정·영구 저장 미구현. CompletedMissionIds는 이번 실행만 유지하며 Best Lap JSON 저장과 별개 | 저장 여부/범위를 사람이 결정한 뒤 Claude가 필요한 구현·재실행 회귀, 결정 전 완료로 표시하지 않음 |
| UI-LAYOUT-DIAG-01 | 로비 레이아웃 진단 판정 변동 조사 | 10/01부터 첫 프레임 높이가 실행마다 달라 통과/실패 변동. 10/02 C PC Claude 전체 렌더 회귀 LobbyLayoutStabilityPIE Fail(ClaudeTutProgressFull/test2.log). 앞선 최대 0.255px Success는 당시 근거 | Claude가 표본/대기·레이아웃 원인을 구분하고 반복 렌더 검사 판정 안정화, 1280/1920 수동 확인 별도 |
| AI-SHOTGUN-RENDER-01 | Shotgun 시선 안정화 시험 판정 정정 | 해결·자동 검증됨(10/04 C PC Claude). 고정 머리4.2~4.4°·왕복 머리5.2~5.4°·시선1.45°, 9/18 수정 정상. 절대4° 판정은 애니메이션 포함 오류·NullRHI 뼈 정지는 거짓 통과 원인 | 고정0.6초 기준 측정·시선≤2.5°·애니메이션 대비 추가 머리≤2.5° 판정, NullRHI/렌더 Success(ClaudeInterview/shotgun3_*.log). known-test-failures 제외·사람 판단 항목 삭제 |
| TEST-ORDER-ROUTE-01 | 전체 렌더 회귀 Route 키 순서 의존 관찰 | 2026-10-04 C PC ClaudeAcroFull 전체5회(test.log/test2.log/final.log/final2.log/test3.log) TrainingRouteSelectionPIE 모두 Success(Codex 로그 대조). 그중3회 화면 미렌더이므로 화면 검증과 구분. 지난 Fail은 날짜별 기록 보존, 원인 미특정·해결 확정 아님 | 재발 시 선행 테스트/입력 처리 순서 재현·Claude 조사. Production 맵 보존 |
| UI-LAYOUT-01 | 목록 진입·선택 시 한 프레임 재배치 | 자동 검증 완료(후속 3건 포함)·수동 확인 대기. 후속 3건(재사용 경로 줄바꿈 재적용·WBP 상시 스크롤바·기본 줄바꿈 폭 160→270) 구현됨·자동 검증 완료. 2026-10-01 19시 이후 후속 보고, C PC, 작업 도구 Claude: Editor 종료 후 DroneEditor Win64 Development Build Succeeded, RenderOffScreen 1920×1080 LobbyLayoutStabilityPIE·FrontEndPIE·FrontEndContract·MissionEntryPIE·BackNavigationContract·HoverMissionPIE 6/6 Success. 로비 단계별 최대 이동 0.255px(기준 2px). 근거 Saved/Automation/ClaudeRecheck5/build.log·render.log | 1280/1920 실제 화면 가독성, Story 4개 목록의 상시 스크롤바 칸 확인 후 수동 완료 |
| SYNC-COLLAB-01 | 협업·다른 PC 세팅 | 공유 파일 최초 5b03ad3(10/02) Commit/Push 완료. ui/image 역할 파일과 이번 변경은 미추적/미커밋. 다른 PC 실제 세팅 미구현 | 사용자 명시 지시 후 남은 파일 Commit/Push→다른 PC Pull·COLLAB_READY→첫 Space 저장 확인 |
| AI-SHOTGUN-REGRESS-01 | Shotgun PIE 시험 장면 수정 | 자동 검증 완료. 2026-10-01 밤 C PC, Claude 시험 수정·Codex 문서 반영. 실기 감지 정상(사용자 확인), 초기 8.8m·약 93° 옆 배치가 기본 시야 반각 70° 밖. Drone을 정면 min(900cm, 사거리−100)·높이 150cm에 고정, AI 코드 변경 없음. NullRHI 관련 5개 5/5 Success(ClaudeShotgunFix/test.log) | 시험 수정·자동 회귀 완료. 사격 체감은 기존 AI-SHOTGUN-PIE-01에서 별도 수동 확인. 9/18 이후 NPC 회전에 영향을 준 변경은 미확인 |
| TEST-NPC-COUNT-01 | NPC 증설 뒤 테스트 기대값 갱신 | 테스트만 수정·맵 보존, 2026-10-02 새벽 C PC Claude NullRHI 3/4 Success(ClaudeNPCMap/test.log·test2.log). 구성 하한(SO 12 이상, 차량/포탑 1 이상·포탑≥차량), 자동 주행 또는 Spline. PIE는 NPC_ 기준 4명만 판정 | 남은 NPCPerceptionSearchPIE Fail은 AI-PERCEPTION-TEST-01에서 실기 비교. 추가 NPC는 감지 시험 PIE 월드 안에서만 제거, AI/원본 맵 미변경 |
| AI-PERCEPTION-TEST-01 | 감지·수색 PIE와 실기 비교 | 2026-10-02 C PC Claude NPCPerceptionSearchPIE Fail: 기준 적 1명이 합성 자극 뒤 실제 시야 감지 유지 실패(state=1 detected=0). 추가 NPC 제거 뒤에도 동일(ClaudeNPCMap/test2.log), 간섭 아님. 방향·시야각 계열은 추정, AI 코드 미변경 | Claude가 실기 방향·시야각·감지/수색 비교 후 시험 장면 또는 AI 원인을 판별해 필요한 변경·회귀. Shotgun 실기 정상과 혼동하지 않음. 원본/Production Training 맵 보존 |
| BUILD-PACKAGE-01 | 패키징 쿠킹 설정 | 구현됨·정적 자동 검증됨(2026-10-02 C PC Claude). DefaultGame.ini Asset Manager DroneMission·DroneDefinition 지정 폴더 AlwaysCook, MissionMap Soft 참조 포함. PackagingPrimaryAssets Success: 미션 14·기체 5, 모두 맵 있음(ClaudePackaging/test.log) | 실제 패키징 미실행. 패키지에서 DA 자동 등록·모든 MissionMap 진입 확인, Production Training 보존 |
| MISSION-CHECKPOINT-01 | 실패 시 시작/중간 지점 재출격 | 구현됨·자동 검증 완료·수동 확인 대기(2026-10-01 밤 후속, C PC, Claude). FailureResponse/MaxCheckpointRestarts·DroneMissionCheckpoint, 파괴/시간 초과/실패 Trigger 통합, 맵·완료 목표·부서진 표적 유지. NullRHI CheckpointRestartPIE·FailureResponseData Success(ClaudeCheckpoint/test1.log·full.log). 실제 맵 체크포인트는 미배치, 현재 첫 출격 위치에서 재출격 | 맵 체크포인트 배치, M1 픽업 지점은 정보단말 회수 구현 뒤. 재출격 브리핑 재생은 MISSION-BRIEFING-02 뒤(여부 현재 미정). 튜토리얼 추락→동일 기체/조작·현재 목표 시간 재설정·목표/표적 유지·재출격 체감 수동 확인. Production Training 보존 |
| MISSION-BRIEFING-02 | HUB 보이스·자막 브리핑·진입 1회 시네마틱 | 자막·Voice 슬롯·자동 진행/Y·Tab/정지 구현·BriefingLinesPIE Success(2026-10-02 C PC Claude, ClaudeBriefing/test2.log). Story M1 4·M2 4·M3 5(조건 없으면 4)·M4 6줄 원문 입력, 화자 허브. M3 첫 줄 Story.TargetEliminated 조건 | 자막 가독성·속도 수동 확인. 음원 없음·튜토리얼 대사 미입력·1회 시네마틱 완료 근거 없음. 반대 분기 M3 첫 대사와 M2→M3 분기·재출격 재생 여부 현재 미정 |
| HUD-FIGMA-01 | HUD 배터리·기체명·신호 대역·풍향 | 구현됨·자동 검증됨·수동 확인 대기(2026-10-02 C PC Claude). DroneBatteryComponent, BatteryLifeSeconds(0=끔), 플레이어 조종 중만 소모, 부족 0.2, 기본 경고만/선택 FailMission. 바람 아래 기체명·SignalBandLabel·BATTERY %/시간·부족/방전. 기존 풍향 확인. HUD·재출격 4/4 Success(ClaudeHUD/test.log) | 실제 HUD 위치·가독성 확인. 모든 기체 배터리 0·신호 대역 빈 값이며 시간·표기 현재 미정(5.8GHz는 시험 예시). D-6 미션별 제한/방전 추락·풍향 결정은 면접 대비 8번 참조·추가 구현 대기 |
| FIGMA-RACING-02 | Figma 레이싱 변경·UI 요구 대조 | Slide 63은 맵 여러 개·맵별 코스·랜덤 없음·직접 선택. 현재 Racing 1맵·Route 5 무작위와 차이. Slide 57/58의 Countdown·Ghost·스틱 오버레이 미구현 | D-5 흐름·코스4개는 RACING-TERRAIN-LINK-01 참조·구현 대기, 실제 지형 현재 미정. 목표 기록·쉐도우·리플레이·스틱·Rate/스로틀 커브·3·2·1·Restart/Quit 요구 확인 후 기능별 범위 정리 |
| UI-PAD-01 | 패드만으로 전체 UI 선택 | 구현됨·자동 검증 완료·수동 확인 대기(2026-10-01 밤 후속, C PC, Claude). 첫 활성 위젯 포커스·강조·방향/A/B·훈련 LB/RB·명시 이동·선택/스크롤 복원. RenderOffScreen 1920×1080 GamepadNavigationPIE 11단계·GamepadMissionFlowPIE 16단계·LobbyLayoutStabilityPIE 최대 0.255px Success(ClaudePad/render6.log) | 실제 PS4 패드만으로 타이틀/로비/브리핑/기체 선택/설정/결과·복귀 확인, 강조 가독성. 카드 A 선택 뒤 ↑출격, 설정 슬라이더 A 잠금 뒤 좌우. NullRHI 패드 2개 건너뜀을 실기 Pass로 간주하지 않음 |
| SYNC-SPACES-01 | MD·Spaces·Trello 정리 연결 | 초기 연결에서 5개 Page 저장·본문/부모 확인. 앞선 2026-10-01 저녁 진행/테스트 Page 저장은 approval_policy=never로 차단됐으나 저녁 후속 재시도에서 진행·테스트·안내 3개 기존 Page 저장/재조회 확인 완료(8개 연산). Trello 주요 카드 읽기 대조, 저장소 AGENTS.md 갱신 규칙 추가. [연결 대상](docs/git/DRONE_SPACES_SYNC.md) | 관련 작업 마무리/최신화 때 기존 Page 갱신. 다른 PC 공유는 사용자가 지침 Commit/Push/Pull. 실시간/예약 자동화 아님. 루트 네이티브 지침 등록은 도구 제한으로 미적용 |
| UI-SETTINGS-01 | 사운드·화면·성능 설정 | Master 음량 미리보기/SaveGame, 창·전체화면/해상도, 품질·VSync·FPS, 적용/기본값/뒤로 취소 구현. PIE 창·해상도 차단. 설정 계약과 FrontEnd PIE 성공 | Standalone에서 실제 소리/창·해상도, Apply와 Back 취소·재실행 복원 확인. 음악/SFX/음성 분리 라우팅은 후속 |
| TUT-ORBIT-02 | 회전 수업 = 원형 코스 한 바퀴 | Heading DA ID 호환 유지, Closed Spline·9 Gate, Tag별 Recorder·HUD, 다른 코스 비활성. 독립 Heading 수업 맵으로 연결 | 실제 비행 제자리 Yaw/다른 코스/7⁄8 바퀴 미완료, 결승→귀환→성공 확인 |
| ASSET-OILRIG-PREVIEW-01 | OilRig 실제 Preview 환경 이식 | 기존 Overview `Lvl_OilRig` 보존. 실제 `Maps/Preview`를 `Lvl_OilRigPreview`, 의존 자산 614개를 `ThirdParty/OilRigPreview`로 이식. Door BP 32개는 외형 64개를 정적화하고 Sample FirstPerson 로직만 제거. 빈 Actor 14개·완전 중복 1개 정리. Map load·외부/누락 0/0·GameMode None·Map Check 0/0 통과. 약 3.80GiB LFS까지 원격 반영 완료 | Editor에서 문/문틀 위치, 재질·조명·충돌·오션·비·첫 로드와 FPS를 수동 확인 |
| PHY-CAMERA-01 | 벽·그물 접촉 화면 안정화 | 접촉 피격 Shake 호출·급감속과 벽 순간 이격/Root 회전을 제거. 연속 접촉은 재충격 대신 제약으로 처리하며 외형 기울기와 FPV 카메라를 분리. Camera 위치 보간·그물 Camera Ignore 추가. 총알 피격 화면 Shake는 기존 동작 유지. Editor Build·Physics 4/4·Prototype 8/8·Story 저장 계약 1/1 성공(오류/경고 0), 관련 BP 6개 Compile 0/0 | Physics Sandbox에서 1/3인칭 저속/고속/지속 벽 접촉·그물 감속/포획 때 화면 떨림 감소와 충돌 유지 확인. NPC 맵에서 총알 피격 화면 흔들림이 남는지 확인. 자동화만으로 체감 Pass 처리하지 않음 |
| TUT-GATE-PRESENTATION-01 | Gate 통과음·위치·크기·자산 재질 | 정상 통과 음성/Sound 슬롯과 BP 연출 Event, 하단 1/6 배치·기존 저장 Child 시작 위치 복구, 공통/개별 Gate 전용 Scale, 전체 Mesh와 상태별 Material 슬롯 구현. 최종 Editor Build·관련 회귀 8/8 성공(오류/경고 0), Gate/Course BP Compile 0/0 | 실제 음원·최종 Gate Mesh를 BP에 지정한 뒤 TestMap에서 가청성, 1/6 위치, 확대해도 선 크기 불변, 상태별 재질·미지정 슬롯 보존을 수동 확인. 팀원 Production 맵은 직접 저장하지 않음 |
| SYNC-WORKPC-01 | PC별 즉시 재개 인계 | 현재 Git·미커밋 범위는 STATUS Git 기준 표를 따른다. Unreal HEAD41444c2+로컬 미커밋/미추적, 다른 PC 전달 전 사용자 검토·Commit/Push 필요. D PC 준비/LFS·32패키지는 이전 기록 | 실제 경로 확인 후 시작 가이드·CLAUDE_CODEX_SETUP의 -WriteLocalConfig -InstallUserRules 사용. 소스 수신·바이너리·최신 플레이 Pass 구분 |
| MISSION-FRAMEWORK-01 | Mission 통합 Blueprint 기반 | Manager/GameMode/Controller, 목표·실패·귀환 Trigger, 체력 100 파괴 표적을 `/Game/Drone/Mission`에 추가. Build와 Mission 자동화 3/3 성공 | Mission 1 Test Map/Definition에서 Delivery→선택 목표→Return과 시간/파괴 실패를 실제 Flow로 확인 |
| STORY-TEST-01 | Story Mission별 격리 TestMap 4개 | GoldenTime Drop/Return, Intercept Spline 차량·목적지 실패, VeilBreaker 재밍 이탈/Return, Endgame UGV 표적 3개/Return과 DA 4개 존재. 4맵 직접 Play Entry 및 FrontEnd Catalog 총 14개 연결. Oct 1 다른 PC의 14맵 점검에 포함 | 각 맵 FrontEnd/직접 Play에서 목표·실패·귀환 수동 확인. 미구현 후보를 이 카드에 합침(Claude 지시서·Figma 매트릭스 Mission 1~4): M1 정보단말 회수·요원 NPC, M2 잔해 Scan·반전, M3 한 미션 내 기체 교대·MANPADS/베일 카운트, M4 장거리 타격·엔딩 시네마틱. 스토리 충돌·MANPADS/베일 표기는 현재 미정, Production Training 보존 |
| PHYSICS-SANDBOX-01 | 벽 충돌·그물 얽힘·국소 파괴 벽 | 일반 비행체 속도 비례 벽 반발·Wing/Rotor Probe와 그물 감속·조종/추력 저하·자세 교란·포획/하강까지 구현. Drone 충돌은 그물을 기본 절단하지 않고 탄환/폭발 Point Damage 국소 절단은 유지. Build 성공, `Drone.Physics` 2/2·`Drone.Prototype` 8/8·Story 저장 계약 1/1 성공 | Sandbox에서 저속 접촉은 작게 밀리고 고속 충돌은 크게 반발하는지, 날개 끝 접촉 방향의 자세 Kick, 그물 포획·하강·자동 해제와 조종 복구를 화면 확인하고 실제 Chaos Cloth/Dataflow와 Geometry Collection을 별도 구역에서 비교 |
| DR-FLIGHT-PHYS-02 | 단일 고속 기준·질량/추력·Payload 하중 | 느림/보통/빠름 UI 제거, 기존 빠름 배율 1.25를 단일 무적재 기준으로 승격. Dry Mass·합산 추력·모터 지연·선형/제곱 항력 추가, Mode 1/2 공통 적용. Drop 내장/부착 화물 kg 질량이 속도·가속·Yaw·호버 여유를 낮추고 투하 즉시 복구. Build 및 Prototype 8/8·Physics 2/2·Flow 5/5 성공 | FPV/Drop 수동 비행으로 무적재 속도, 모터 추력 지연, 적재 전후 호버·가속·선회 차이와 Mode 1/2 축만 달라지는지 확인. 실제 기체 스펙이 정해지면 Definition별 질량·추력·항력 교정 |
| PHY-NET-03 | 그물 날개 걸림·포획 장애물 | C++ 결정적 접촉 상태와 Collision Root 바깥 네 Wing/Rotor Sphere Probe v1 완료. 실제 이동 속도와 반복 접촉으로 감속·추력/조종 저하·Pitch/Roll/Yaw 교란·하강을 누적하고 임계값 이상은 Captured가 된다. 일반 충돌 절단은 기본 Off이며 BP 수치 조정 가능 | 수동 체감 조정 뒤 Chaos Cloth 시각 변형 + 필요 시 전용 Net Interaction Volume + 역추진/접촉 해제 탈출·Crash/Mission 실패를 연결하고 Standalone 3회 확인 |
| PHY-COL-01 | 모든 벽·구조물 공통 반발 | 일반 `ADronePrototypePawn`의 Component 기본 On. `120cm/s` 무반응·고정 Kick/6cm 이격을 없애고 저속부터 반발 속도·분리 거리·회전 Kick을 충돌 속도에 비례시켰다. 직전 속도 보존과 Wing/Rotor Probe를 사용하며 바닥/천장·Ground UGV는 제외. 비례 반발 Red→Green 회귀 성공 | Sandbox와 다른 TestMap에서 연속 입력 비비기/침투·날개 Probe 크기/방향을 수동 확인하고 강한 Crash/Damage 우선순위·Landing 상태·얇은 벽 Sweep/CCD를 후속 구현 |
| TUT-ROUTE-SELECT-01 | Training Route 4개 선택 시험 | `Lvl_DroneTrainingRouteSelectionTest`에 직선·좌곡선·우곡선·상승 슬라럼과 Gate 각 5개 배치. `1~4` 고정·`5` 무작위, 단일 활성, 진행 초기화, HUD 기록 Source 전환. Build·Map Check·API/저장/실제 키 PIE 성공 | 사용자가 화면에서 경로 형태·Gate 간격·랜덤 전환과 Lap HUD를 확인하고 각 Spline 점을 최종 조정 |
| TUTORIAL-MISSION-01 | Figma Tutorial 8개 독립 Mission | 수업별 `TestMap/Tutorial` 8맵·DA·직접 Play Entry 구현, 공용 종합 시험장 보존. 다른 PC의 Hover 로비/직접 PIE에서 3초 유지→귀환 Success. 비충돌 표식 4개 유지 | FrontEnd와 각 독립 맵에서 Hover 가독성 및 8수업 전체 위치·목표·결과를 수동 확인. 이전 사용자 7개 대략 확인과 최종 완주를 구분 |
| TUT-BEST-01 | Course별 Best Lap 영구 저장 | 구현됨·BestLapPersistence Success(2026-10-02 C PC Claude, ClaudeBestLap/test2.log). 유효 완주 CourseId&#124;DroneId&#124;ControlMode, HandlingPreset 제외. Saved/SaveGames/DroneTrainingBestLaps.json, 없음/구버전/손상 처리·HUD 저장 기록. 자동화 별도 슬롯. 기존 Production Training 2 Fail 보존 | 같은 코스/기체/조작으로 실제 랩 두 번 실행·재실행 복원과 첫 완주 전 저장 HUD 수동 확인. 평균은 실행 History, 정식 레이싱 방식 현재 미정 |
| TUTORIAL-FIGMA-02 | Figma 8개 훈련 ↔ Test Map 대조 | 8개 기능/DA·독립 시험맵·시간·연속 진행·전체 완료 UI 구현과 기존 자동 검증 보고가 있음. 2026-10-03 DA 순서 재확인; Warehouse 최종 환경은 별도 | 기존 진행 UI의 실제 8수업 연속 완주·결과/로비 복귀를 수동 확인. 4/8 집계 단위와 Warehouse 제작 범위 결정, 결과 UI 중복 구현 금지 |
| TUTORIAL-GUIDE-03 | 8개 수업 구현·테스트 기준 | 클래스 책임, DA/Tag, 수업별 구현법, Build→Asset→Map→PIE→성능 검증과 문제 확인 순서를 문서화 | 팀원이 문서만 보고 호버/FPV/Payload를 재현하고 Forward 수업을 추가 가능 |
| AI-LOCOMOTION-01 | 적·아군 NPC 걷기 모션 | AI-LOCOMOTION-01 후속 구현됨·자동 검증됨(2026-10-04 C PC, 작업·검증 Claude)·수동 확인 대기. Mannequin 원본과 Insurgent/Quantum 메시의 스켈레톤 불일치로 양팔을 벌리던 문제를 사용자 선택 IK Retarget으로 수정하고 적 Gun을 hand_r에 부착. 속도 > 3 이동 판정·Gaze 유지. NPCLocomotionAnimPIE 오프스크린 Success: 이동40개(NPC5명) ShouldMove40, 위팔 기본 자세 대비 평균51.7°·40/40, 총 든 NPC 양손 간격 평균34.4cm·24/24, 총 hand_r 추종·왼손 총 위 각각24/24. Drone.AI 19개 중18 Success·기존 NPCPerceptionSearchPIE 1 Fail(state=1 detected=0), 새 실패 없음. 자산 Verify success(ClaudeNPCWalk/rt_tests3.log·ai_suite.log·verify_rt3.log). 걷기/뛰기 전환·발 미끄러짐·뒷걸음 방향·손/총 정렬(특히 산탄총)·사격/재장전은 사용자 수동 확인 대기. CR_Mannequin_FootIK는 Insurgent 계층 차이로 Editor 컴파일 경고 잔존. Epic 마네킹 변환 임시 동작·최종 아님; 최종 애니메이션 미구현·자산 미정, 산탄총 전용 동작 미구현·도입 여부 미정(소총 동작 공유). | Smart Object 맵 정지/걷기/뛰기 전환·발 미끄러짐·뒷걸음 방향·손/총 정렬(특히 산탄총)·사격/재장전 화면 확인 |
| MAP-TEST-01 | 경량 Tutorial Systems TestMap 수동 확인 | 맵·생성 도구·전용 자동화·Map Check 완료 | Gate/Ring/역할/HUD 한·두 Lap 화면 확인 |
| AI-SO-TUNE-01 | Smart Object·유인 MG·개인화기 추적 확인 | 순찰 최종 슬롯 방향·Pursue 정지점·Capsule 외 VisualOnly 계약을 적용했고 사용자 화면에서 정상 이동을 확인했다. 진단 로그 기본값 Off | 새 `1.0초` 첫 사격 조준 대기를 실제 화면에서 확인. 재발 시 Blueprint에서 `[NPC-STATE]`·`[NPC-MOVE]` 진단을 켜 로그 회수 |
| AI-OUTDOOR-TUNE-01 | 야외 감지·Smart Object 검색 범위 | Outdoor Controller BP를 Rifle/Shotgun에 연결. Sight 60m/Lose 70m/Search 80m×±10m/직전 회피 15m, BP 조절 가능 | 넓은 야외 맵 화면에서 과도한 원거리 점유·감지 끊김 여부를 확인하고 역할별 수치 확정 |
| AI-SHOTGUN-PIE-01 | 추가 Shotgun NPC 사격 체감 확인 | 실제 8 Projectile·12° 반각, Pellet당 3 피해, 상호 충돌 방지, Cyan Debug 기본 Off, 발광 비드/Tracer·3°/6° 시선 Hysteresis·Asset/PIE 자동화 완료 | 발광 비드 8개 분리 가시성·Cyan 선 제거·회피·최대 24 피해·사거리·LOS·시선 안정화를 Editor 화면에서 확인 |
| UI-FLOW-PROTOTYPE-01 | Mission/Drone 선택 임시 UI 확인 | 후속 첨부 시안으로 로비 3열·브리핑 이미지/설명·기체 상단 도식/상세·하단 가로 카드 갱신, `FrontEndPIE`와 계약 성공 | 16:9 1280/1920 가독성/스크롤·선택/출격 확인 뒤 최종 WBP·Thumbnail/3D Preview 범위 결정 |
| MISSION-RULE-PIE-01 | 새 목표 Rule의 실제 맵 Vertical Slice | 귀환·Jammer·역할 Actor 시험 배치 완료, 직접 실행은 Prototype Flow | Test Mission DA/진입 경로에서 Scan/Delivery/Destroy/Return/Jamming Event·Tag·시간 규칙 확인 |
| STY-03-PIE-01 | 재밍 신호·비행·HUD Vertical Slice | 35%/80% 겹침 Zone TestMap 배치·저장 계약 완료 | 실제 비행으로 Overlap·HUD·둔화/복원 확인. 영상 Noise WBP는 별도 표현 작업 |
| STORY-BRANCH-01 | Mission 2→3 양쪽 스토리 분기 | Story Fact 저장·성공 적용·조건 목표 필터, 미끼/실제 탑승 양쪽 자동화 완료 | 사용자가 기본 스토리안을 정하면 실제 Mission DA에 Fact 설정 |
| DRONE-FIBER-01 | 광섬유 Drone 기반 | DroneSpy Body·분리 Rotor 4개와 회전을 사용하고 공급 GSU 통을 `FiberSpoolMeshComponent`에 약 28cm 높이로 하부 장착. BaseColor·Normal·ORM·Emissive Material, 통 상단 출구→누적 지면→현재 기체 다점 포물선/Hermite 케이블, `JammingImmunity + ImpactDetonation`, 1인칭 기본값 적용. Editor Build·ExtendedRole 1/1 성공 | TestMap에서 Spy 본체·통 크기/위치, 본체/카메라 비간섭, Rotor 회전, 통 상단 케이블 출발과 곡률, 조작·자폭·재밍 면역을 화면 확인하고 BP Transform/굵기·간격을 최종 조정 |
| DRONE-GROUND-01 | 지상 UGV 기반 | 기존 주행·4점 접지·상부 독립 조준에 `UDroneGroundWeaponComponent` 연결. 좌클릭 직사 총탄 25 피해, 우클릭 중력 유탄 100 반경 피해, 수명/쿨다운 적용 | 시험맵에서 상부 방향과 실제 탄도·4발 처치·유탄 낙차/반경을 수동 확인하고 수치 조정 |
| DR-FPV-ACRO-PIE-01 | FPV Rate/Acro 실제 조작 체감 | Mode 1/2 축 분리와 각속도·무수평복귀에 공통 질량·추력·모터 응답·중력·Body Up 추진·선형/제곱 항력 v2 연결. 별도 속도 단계는 제거 | 키보드/패드로 Nose-down 전진력, 호버·상승·무추력 하강, Roll/Loop와 650°/s 체감, Mode 1/2가 축 배치 외 비행 성능이 같은지 확인 후 수치 조정 |
| DR-FPV-ACRO-INPUT-02 | Acro 키보드·패드 Mode 1/2 | 의미축4개+패드세로2개, IMC33매핑·4축 Dead Zone·비행BP4종 연결. 10/04 C PC Space 불변/Mode 키보드 동일/쏠림 보호/자산 계약 자동 Success(ClaudeAcro/test_after_dz.log), 상세 ACRO-MEETING-01 | 기존 W/S Pitch·A/D Roll·Q/E Yaw·Space/Ctrl Throttle, Mode1 LeftY Pitch/RightY Throttle·Mode2 반대 배치와 실제 혼합 입력 수동 확인. 반전 뜻/조작 정책 미정 |
| WTH-03 | 비 표현 Vertical Slice | OilRig `T_rain_Mask` 참조 전용 Material, 최대 112개 짧은 Plane 빗줄기, 파란 Debug 기본 Off, 표면별 천장/지면 차단·0.35초 실내 감쇠 구현. Weather 4/4·Map Check 0/0 | 실외→지붕 아래→실외, 긴 잔상 감소·천장 침투 차단, RainStorm→Clear/비 Off 화면 확인 후 Niagara·MPC·Audio·품질 단계 범위 결정 |

### 사용자가 지금 확인할 맵

최신 통합 진입은 `/Game/Drone/Maps/Lvl_DroneFrontEnd`다. 타이틀 스토리/레이싱/튜토리얼/설정/종료 5메뉴→분류 직접 진입(로비 탭·LB/RB 현재 유지, 최종 유지 여부 미정), 설정의 적용/취소/재실행, 설명→기체 선택→출격과 버튼/Esc/패드 Back을 확인한다. Tutorial 8개 독립 맵·Story 4·Racing 1은 직접 Play도 가능하다. 아래 경량 맵은 Gate/역할/HUD 자체 시험장이다.

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
- `/Game/Drone/Maps/TestMap/Tutorial/Lvl_Tutorial_*_Test`: 8개 수업별 독립 Mission·직접 Play·귀환
- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialMissionTest`: 기존 8 Station이 남아 있는 공유 종합 시험장. 현재 수업별 DA의 진입 맵과 구분
- `/Game/Drone/Maps/TestMap/Lvl_DroneRacingTest`: 단일 코스 순서/정방향 완주·시간 기록 시험
- `/Game/Drone/Maps/TestMap/Lvl_OilRigRainComparisonTest`: `R`로 원본/비 끔/근거리 원본/프로젝트 비 비교
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

현재 순서는 이 Next가 기준이며 최신 검증은 STATUS를 따른다. 수동 미확인 사항을 자동화 완료와 섞지 않는다.

10/05: 결정 표의 확정 항목은 Claude 구현 대기로 인계한다. D-1·D-2는 기획자 내용 대기, D-13 나머지 목록은 사용자 결정 대기. 기존 코스·Acro 체감 수동 확인을 이어간다. 최신 전체97개중86 Success·11 Fail, PIE 미렌더 포커스6개 판정 제외·당시5개 실패(후속 Shotgun 해결·전체 재실행 아님). 오늘10회 중8회 미렌더, 표지는 LobbyLayout samples=0만 사용한다. 이전 집중30/32·전체95개2회는 당시 기록. 다음은 실제 UI/8수업/Best Lap과 제품 지형 결정이다.

Trello 참고를 추가했다. [레이싱 3·2·1 시작](https://trello.com/c/FGfMmLV3)은 후속 요구이며 아직 구현하지 않았다. [목표 데이터화](https://trello.com/c/dMXHThh0)·[목표 연결](https://trello.com/c/Eg90YRHy)·[차량 도착 규칙](https://trello.com/c/ES7ZAqQG)은 기존 기반이 있으므로 완전 미구현으로 되돌리지 않고 아래 Story 고도화에서 실제 콘텐츠 연결을 대조한다. 카드 상태는 수정하지 않았다.

1. `UI-LAYOUT-01`: 후속 3건 포함 자동 검증 완료(C PC, Build 성공·6/6 Success·최대 이동 0.255px). 1280/1920 실제 화면 가독성과 Story 4개 목록의 상시 스크롤바 칸을 수동 확인한다. 패드 강조 추가 후 렌더 최대 이동 0.255px Success도 확인됐으며 아래 2번 실기 확인과 함께 진행한다. Shotgun 시험 수정은 자동 검증 완료이며 새 DA 실제 로비 등록 수동 확인과 `AI-PERCEPTION-TEST-01` 실기 비교을 진행하며 Production Training 맵은 수정하지 않는다.
2. `UI-PAD-01`: 초기 활성 위젯 포커스·방향/A/B·강조·탭/선택/스크롤 복원 구현과 렌더 자동 검증 완료(11/16단계 Success). 다음은 실제 PS4 패드만으로 전체 흐름·설정·결과/복귀와 강조 가독성을 확인한다. `MISSION-CHECKPOINT-01`은 튜토리얼 추락 재출격 체감을 함께 확인하고 맵 배치/M1 정보단말 회수 이후 픽업 지점/브리핑 후속을 구분한다.
3. Standalone 설정의 적용/취소·실제 소리·창/해상도·재실행 복원을 확인한다. 미션은 Hover와 FPV부터 성공/실패·재시도·결과/복귀를 확인한 뒤 독립 Tutorial 8개(Orbit 결승→귀환)·Racing·Story 4개로 확대한다. 최신 바이너리 확인은 이 단계에서 별도 수행한다.
4. `TUT-BEST-01`: JSON 저장·복원·없음/구버전/손상 자동 검증 완료. 같은 코스/기체/조작으로 실제 완주 후 재실행하여 첫 완주 전 저장 기록 HUD를 확인한다. 브리핑 자막 속도·HUD 위치와 BUILD-PACKAGE-01 실제 패키징도 확인 대기다. 평균은 실행 History, 레이싱 후속은 RACING-TERRAIN-LINK-01의 D-5 확정 흐름에 따라 구현 대기다.
5. `TUT-PROGRESS-01` 시간·다음 수업·`n/8`·전체 완료 UI는 구현·자동 검증됐다. 실제 8수업 연속 진행/S48·S49·로비 완료 표시를 수동 확인하고, `TUT-BRIEFING-TEXT-01` 미기재 문구와 `TUT-COMPLETION-SAVE-01` 영구 저장 여부는 사람이 결정한다. `UI-LAYOUT-DIAG-01`·`TEST-ORDER-ROUTE-01` 원인 조사는 Claude 담당. AI-SHOTGUN-RENDER-01은 시험 정정 후 해결. Warehouse는 TestMap에서 먼저 검증하고 Production은 합의 뒤 수동 이식한다.
6. Story M1 선택 정보/화물 파괴 실패 → M2 잔해/Story Fact → M3 재밍 해제/UGV 교대 → M4 장거리 타격/엔딩을 한 미션씩 고도화한다. D-1·D-2는 기획자 내용 대기로 보류하며 충돌하는 기본 스토리안은 임의 확정하지 않는다.
7. 단계별 수동 회귀로 Gate 최종 자산·1/6 높이/Scale, Route `1~5`, Physics 벽/그물·카메라/피격 Shake, FPV/Drop 하중·Mode 1/2, NPC Smart Object 맵의 순찰/Shotgun·AI-LOCOMOTION-01 걷기/뛰기 전환·발 미끄러짐·뒷걸음 방향·손/총 정렬(특히 산탄총)·사격/재장전, 비 실내 차폐·광섬유/UGV를 확인한다. Shotgun 전용 맵 결과만으로 Smart Object 맵을 완료 처리하지 않는다.
8. 실제 Chaos 비교 Spike·정식 Rain/젖음/Audio/품질·재밍 Noise·최종 영상/음원·패키징은 Story Vertical Slice 이후다. 맵 이동은 소유권·참조 감사 후 수행하고 `test1`·`test2`는 용도 확인 전 유지한다.

이동 후보·병행 회귀·최근 완료와 종료된 요청은 [10월 보드 아카이브](docs/history/archive/WORKBOARD_2026-10.md), 10/03 UI 준비·진단은 [WORKLOG](docs/history/DRONE_WORKLOG.md)에 보존했다.
