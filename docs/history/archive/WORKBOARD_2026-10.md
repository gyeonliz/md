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
