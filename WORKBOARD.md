# 현재 작업 보드

기준일: 2026-09-03 (Asia/Seoul)

이 보드는 실제로 확인한 결과만 반영한다. 개별 준비 카드가 Done이어도 `Git + Unreal 환경 구축` 전체는 첫 Push, 다른 PC Clone, LFS 확인, Clone한 프로젝트 실행까지 성공해야 완료다.

Unreal 공유 기준선은 `origin/main=2d6a459`다. 전투 Greybox·AI-VIS-01A와 Smart Object 방향 보강까지 Push됐다. 실제 Mesh·Animation·FX·SFX 연결은 후속 작업이다.

2026-09-03 게임 흐름은 `실행 → 시작 트레일러 → 로비 → 미션 선택/측면 설명 → 하단 시작 → 미션 트레일러 → 맵 → Drone 선택 → Mission 시작/측면 목표 UI`로 변경됐다. 사람 Operator 조작·NPC 대화 수령·Operator↔Drone 전환은 폐기하며 [`docs/DRONE_FRONTEND_MISSION_FLOW_PLAN.md`](docs/DRONE_FRONTEND_MISSION_FLOW_PLAN.md)를 최우선 실행 기준으로 사용한다.

## 현재 작업 스냅샷

마지막 갱신: 2026-09-03 — FLOW-03 미션 선택·설명·시작 완료

| 항목 | 상태 |
|---|---|
| 현재 단계 | FLOW-01~03 데이터·시작 화면·로비 미션 선택 완료, FLOW-04 브리핑→Map 준비 |
| 진행 정도 | GameInstance Flow/Catalog, 실제 Mission·Drone Data Asset, 전용 Front-end BP/WBP/Map, 정적 Opening→Lobby와 Training Mission 목록·측면 설명·하단 시작 완료. NPC Visual/Muzzle 기반도 후속 표현용으로 준비 |
| 지금 작업 중 | `FLOW-03` 데이터 기반 로비 UI·집중 PIE 완료. 다음 활성 카드는 `FLOW-04` |
| 완료 근거 | Game/Editor Build와 최종 `Drone.Flow` 3/3 통과. Mission 이름·설명은 저장 Definition과 일치, 잘못된 ID·중복 확정 0, Root Widget 생성 1회 확인 |
| 수동 미확인 | Training 두 Lap 비교 HUD, OilRig Map Check·재질·조명·스케일·충돌·성능, Ground Drone/MG·NPC·Raw Drone 외형 채택 |
| 현재 차단 | FLOW-04 코드 차단 없음. 실제 Mission Trailer Asset 형식은 미정이므로 정적 Briefing 대체 화면 뒤 `MissionMap` Soft Reference를 여는 경로로 먼저 검증 가능 |
| 다음 행동 | `FLOW-04`에서 MissionTrailer 대체 패널 종료 → `LoadingMissionMap` → 선택 Definition의 Training Map 로드와 GameInstance 선택 보존 연결 |
| 다음 기능 | `FLOW-04 → FLOW-06` 한 Mission·한 Drone Front-end Vertical Slice. `AI-VIS-01B`는 Mission 흐름 뒤 실제 전투 표현 단계로 유지 |
| 에셋 인수 | `C:\에셋` 원본은 보존. ArmyVFX·InfantrySFX·Ground Drone·NPC 외형·Raw Drone을 정확한 의존성 묶음으로 이식 |
| 맵 이식 | 기존 환경 3종에 `Lvl_OilRig`을 추가. Vendor FirstPerson Sample 의존성을 끌어오던 Door Actor 8개는 중앙 사본에서 제거 |
| Editor/MCP | Build·Headless 검증 뒤 모든 Unreal Editor 프로세스 종료. Codex 네이티브 Tool 노출은 `UE-MCP-02` 미확인 |
| 확정 후속 방향 | UE 5.8 Dataflow/Chaos로 부분 고정 그물과 선택형 맵 파괴를 구현 후보로 채택. Plugin·자산·코드는 아직 변경하지 않았으며 TUT-04/Flight Collision 기준 뒤 별도 Spike |
| Git 처리 | Unreal `main=origin/main=2d6a459` 위 FLOW-01~03·NPC Visual 기반 26개 경로, 문서 `main=origin/main=14c4ae6` 위 상태 문서와 Flow 작성/검증 도구 4개가 로컬 미커밋. Codex는 Commit·Push하지 않음 |
| UI/기획 참고 | Figma `Project:Droner`는 세계관·청록/녹색 HUD·경고 아이콘 참고용으로만 읽음. Figma는 수정하지 않았고 게임 제목 통일은 보류 |
| 협업 Git | 팀원 환경 맵·재질은 중앙 `main`에 들어온 상태다. Battlefield의 새 `M_Enemy`·`M_Start`·`M_Target` 의존성과 세 중앙 맵 로드를 검증했고, `.vsconfig` 14.50 복원과 `//test` 제거를 별도 정리했다. 팀원 PC의 실제 Remote 구성 확인은 남음 |
| 학습 일정 | 정보처리산업기사 2026년 공식 일정 확인 완료. 개인 접수·필기일·면제 상태는 미확인, 코딩테스트는 공통 시험일 없음 |
| 학습 다음 행동 | Q-Net 상태를 확인해 Track A/B/C를 고르고 첫 학습 블록 실행 |

상세 변경 이력은 [`docs/DRONE_WORKLOG.md`](docs/DRONE_WORKLOG.md)에 계속 추가한다. 매 구현 작업 종료 시 이 스냅샷의 현재 작업·완료 근거·다음 작업을 함께 갱신한다.

## Inbox

| ID | 태그 | 작업 | 활성화 조건 |
|---|---|---|---|
| PF-01 | Portfolio | 데모 기능별 기록 시작 | 첫 재현 가능한 Drone 기능 완료 |
| DR-FUTURE-01 | Drone | 배터리·통신·재밍·멀티 후보 평가 | Flight MVP 이후 |
| PFN-P2 | Drone | Flight MVP 카드 PFN-07~14 활성화 | Tutorial Vertical Slice 통과 |
| PFN-P3 | Drone | Mission Runtime 카드 PFN-15~21 활성화 | FLOW-06과 PFN-14 통과 |
| PFN-P4 | Drone / Unreal | Enemy AI·Turret 카드 PFN-22~32 활성화 | PFN-21 통과 |
| PFN-P5 | Drone / Unreal | 통합 Greybox 카드 PFN-33~38 활성화 | PFN-32 통과 |
| FLOW-05 | Drone / Mission / UI | Map 진입 뒤 Drone 선택·Spawn/Possess | FLOW-04 통과 |
| FLOW-06 | Drone / Mission / UI | Mission 시작과 측면 목표 UI | FLOW-05 통과 |
| FLOW-07 | Drone / Mission / UI | 성공·실패 결과, 재도전·로비 복귀 | FLOW-06 통과 |
| FLOW-08 | Drone / Front-end / Test | 전체 흐름 새 실행 3회 반복 | FLOW-07 통과 |
| PFN-P6 | Drone / Unreal | 에셋 교체 준비 카드 PFN-39~43 활성화 | PFN-38 완료 + 최신 PFN-37 결과 3회 Pass |
| ASSET-GATE-01 | Drone / Unreal | 구매 소스 후보 비교와 구매 결정 | Greybox Vertical Slice 3회 Pass와 차단 결함 0건 |
| PHY-DF-00 | Drone / Physics / Unreal | Dataflow·Chaos Physics Sandbox | TUT-04 완료 또는 사용자 우선순위 변경 후 별도 Branch에서 Plugin·Build·회귀 검증 |
| PHY-NET-01 | Drone / Physics | 일부 고정 그물 Cloth Spike | PHY-DF-00 + Flight Collision 기준 완료 |
| PHY-DST-01 | Drone / Physics / Mission | 선택형 Geometry Collection 파괴 Spike | PHY-DF-00 + Damage/Crash Event 기준 완료 |

## 폐기된 계획

| ID | 기존 계획 | 처리 |
|---|---|---|
| CTRL-02 | 사람 Operator↔Drone Possess·Camera 전환 | 2026-09-03 기획 변경으로 폐기. Drone 선택 확정 뒤 단일 Drone Pawn을 Spawn/Possess |
| STY-01 | 로비에서 Operator가 NPC와 대화해 Mission 수령 | 2026-09-03 기획 변경으로 폐기. 로비 미션 목록·측면 설명·하단 시작 버튼으로 대체 |

## Todo

| ID | 태그 | 작업 | 완료 조건 |
|---|---|---|---|
| GIT-10 | Git / Unreal | 다른 PC Clone과 실행 | LFS 포함 Clone 후 UE 5.8.1에서 열림 |
| FLOW-04 | Drone / Front-end / Mission | 미션 트레일러 → 선택 Map 로드 | 정적 Briefing 종료 뒤 선택 Definition의 Training Map으로 이동하고 GameInstance의 Mission 선택이 유지됨 |
| GIT-TEAM-01 | Git / Unreal / 협업 | 팀원 PC 원격 규칙 확인 | 환경 맵·재질 중앙 반영과 개인 설정 정리는 완료. 팀원 PC에서 `origin`/`upstream` 또는 `origin`/`fork`, `pushurl`을 실제 확인 |
| SYNC-04 | Codex Sync | 두 PC 간 실제 수동 인계 시험 | Git 흐름과 문맥 패키지 흐름을 각각 완료 |
| TUT-04 | Drone / Tutorial / UI | 비교 결과 수동 판정 | 두 번 완주해 첫 기준 생성과 두 번째 이전 평균·Best·부호를 실제 HUD에서 확인 |
| UE-MCP-02 | Drone / Unreal / Codex Sync | Codex 네이티브 MCP Tool 노출 확인 | Unreal Editor 실행 후 `D:\JGY\project\drone` 루트의 새 Codex 작업에서 `unreal-mcp` Tool을 찾고 Current Level을 한 번 조회 |
| STUDY-EXAM-01 | 정보처리산업기사 | Q-Net 개인 상태 확인 | 3회 접수·수험일·응시 여부·필기 합격/면제 상태를 확인하고 Track A/B/C 기록 |
| STUDY-EXAM-02 | 정보처리산업기사 | 선택 Track 첫 학습 | 필기 60문항 진단 또는 실기 기초 1블록과 오답 기록 완료 |
| STUDY-CT-01 | Coding Test | C++ 기본 진단 시작 | 첫 문제 직접 풀이·실패 이유·재풀이 날짜 기록 |
| AI-VIS-01B | Drone / AI / Assets | NPC·Rifle·Shotgun·MG 실제 외형과 전투 표현 연결 | 프로젝트 Integration BP에서 T Pose·손 위치·발사 표현 검증. Shotgun은 실제 후보 Mesh 확보 필요 |

## Doing

| ID | 태그 | 작업 | 현재 확인 | 남은 완료 조건 |
|---|---|---|---|---|
| AST-01 | Drone / Unreal | 제공 에셋 최소 외형 Spike | FPV 본체·로터 4·재질/Texture와 44.1 kHz Loop Cue/Wave를 `/Game/Drone/ThirdParty`로 선별 이식. Integration BP와 GameMode 연결. 이번 재검증에서 전용 자동화 1/1·의존성 감사·Blueprint 0/0/0·LFS fsck 통과. 전체 14/14는 TUT-03 당시 같은 Commit의 기준선이며 이번에 미재실행 | 실제 스피커 출력의 Loop 단일 재생·종료 정지는 미확인. 결과 확보 전까지 Doing 유지 |
| AST-01C | Drone / Unreal / Asset | DronePack 드론 시각 라이브러리·데모 맵 | 드론 Mesh·Material·Texture와 정리 Map 154개를 `/Game/Drone/ThirdParty/DronePack`에 선별 이식. Build·전체 14/14·BP 0/0/0·Map Check 0/0·의존성·LFS 검증 통과 | Editor에서 드론 6종·맵 화면을 확인하고 재질·스케일·조명 이상 유무를 기록 |
| TUT-04A | Drone / Tutorial / UI | 한글 비행·구간 통계 HUD와 Course Authoring 보강 | 병합 main Build·전체 15/15·BP 0/0/0 통과. PIE에서 한글 HUD 두 패널·현재 Gate·세분화 코스 선 초기 렌더 확인 | Gate 0→3 실제 한 Lap 뒤 최근·완료 구간 숫자 갱신 확인 |
| TUT-04B | Drone / Tutorial / UI | 이전 평균·Best·Delta 결과 | 현재 시도 제외 평균, 첫 기준, Best와 Segment 비교, Blueprint Event, HUD 네 행 구현. Build·16/16 통과 | 실제 두 Lap에서 표시 값과 부호 확인 |
| AST-05 | Drone / Unreal / Asset | 남은 제공 에셋 선별 라이브러리 | ThirdParty 891개와 `Lvl_OilRig` 1개. 수량·대표 로드·외부/누락 0 | Editor 시각·성능·Map Check와 실제 채택 후보 결정 |
| AI-SO-TUNE-01 | Drone / AI / Smart Object | 배치·Offset·Definition·검색·StateTree 조정 가이드와 Slot 도착 방향 적용 | 공유 `2d6a459`에 방향 보강과 Definition이 Push됨. DroneEditor Build, Slot Yaw 판정 포함 자동화 2/2, Definition/BP 6쌍 Validate 통과 | `Lvl_NPCSmartObjectGreybox`에서 Cyan 화살표와 순찰·Cover·MG 도착 방향의 화면 일치만 확인 |

## Done

| ID | 태그 | 검증 결과 |
|---|---|---|
| WM-01 | 전체 관리 | 이 파일에 Inbox/Todo/Doing/Done과 일곱 분류 태그 사용 가능 |
| FLOW-00 | Drone / Front-end / Planning | 새 실행 흐름, 사람 Operator 폐기, Mission/Drone 데이터·UI 책임과 FLOW-01~08 검증 순서를 문서 기준선으로 확정 |
| FLOW-01 | Drone / Front-end / Data | `UDroneGameFlowSubsystem`, 8개 상태, Mission/Drone Primary Data Asset, ID/Catalog/중복 요청 검증을 구현했다. 실제 `DA_Mission_Tutorial_Training`과 `DA_Drone_Scout_Greybox`를 생성해 새 프로세스 Validate 및 `Drone.Flow.Contract` 1/1 통과. 로컬 미커밋 |
| FLOW-02 | Drone / Front-end / UI | `Lvl_DroneFrontEnd`, 전용 BP GameMode/Controller, `WBP_DroneFrontEndRoot`와 C++ 정적 대체 Layout을 구현했다. 새 실행 Opening→계속→Lobby, Root 1개, 중복 전환 0, 선택 전 Drone 0대를 PIE에서 확인. 로컬 미커밋 |
| FLOW-03 | Drone / Front-end / UI | 등록 Mission ID 목록을 이름순으로 공급하고 첫 Training Mission 버튼·이름·설명·지역/난이도·하단 시작을 같은 Definition에 연결했다. 시작은 `MissionTrailer`까지만 전환하며 잘못된 ID·중복 확정을 거부한다. 최종 Flow 3/3 통과, 로컬 미커밋 |
| PLAN-01 | Drone / Planning | 세계관·화면 흐름·Tutorial/Story·UI·구현 현황·기술 구조·로드맵·검증·보류 결정을 통합 기획서로 정리 |
| ENV-01 | Unreal | 작업컴 UE 5.8.1 설치 확인 |
| GIT-01 | Git | Git 2.53.0.windows.3 실행 확인 |
| GIT-02-CHECK | Git | 초기 점검 당시 전역 Git 이름과 이메일이 없었던 상태를 확인 |
| GIT-02A | Git | 전역 Commit 이름 `gyeonliz`, 이메일 `jkw6483@gmail.com` 설정 확인 |
| GIT-03 | Git | Unreal 원격 `gyeonliz/drone`과 문서 원격 `gyeonliz/md` 역할 확정 |
| GIT-05-CANDIDATE | Git / Unreal | 후보 프로젝트에서 Source/Config/Content 추적과 생성 폴더 제외 확인 |
| GIT-06-CANDIDATE | Git / Unreal | Git LFS 3.7.1과 후보 저장소 로컬 초기화 확인 |
| GIT-07-CANDIDATE | Git / Unreal | `.uasset`/`.umap`의 LFS 속성 확인 |
| GIT-08B | Git / Unreal | `.vsconfig`에는 공유 가능한 VS component ID만 있어 첫 Commit 포함을 권장안으로 기록 |
| GIT-08 | Git / Unreal | 863개 파일의 첫 Stage 범위를 검토하고 생성물·민감 정보 제외 확인 |
| GIT-09 | Git / Unreal | `91498b7` 첫 Commit을 `gyeonliz/drone`의 `origin/main`에 Push하고 LFS 추적 확인 |
| MD-01 | Codex Sync / Git | 현재 문서 작업 폴더의 `origin`을 `https://github.com/gyeonliz/md.git`로 연결 |
| MD-02 | Codex Sync / Git | `md` 저장소 첫 Stage 범위를 검토하고 민감 정보·생성 패키지를 제외 |
| MD-03 | Codex Sync / Git | `9e81de0` 첫 Commit을 `gyeonliz/md`의 `origin/main`에 Push하고 로컬·원격 일치 확인 |
| GIT-ANDROID-01 | Git / Unreal | 사용자 결정에 따라 Android File Server Plugin·네트워크를 끄고 토큰 할당을 비움 |
| BUILD-01 | Drone / Unreal | `DroneEditor Win64 Development` 빌드 성공 |
| BP-COMPILE-01 | Drone / Unreal | 전체 Blueprint Commandlet 컴파일 0 errors, 0 warnings 및 정상 종료 |
| DR-AUDIT-01 | Drone / Unreal | 기존 C++·Enhanced Input·맵·Variant 구조를 읽기 전용으로 기록 |
| DR-PROTOTYPE-01 | Drone / Unreal | 별도 `ADronePrototypePawn`과 native GameMode C++ 골격 구현 |
| DR-PROTOTYPE-02 | Drone / Unreal | Root·Collision·Camera·Movement 기본값 자동화 테스트 성공 |
| DR-PROTOTYPE-03 | Drone / Unreal | 임시 Game World에서 GameMode 경유 Pawn Spawn/Possess 자동화 테스트 성공 |
| DR-PROTOTYPE-04 | Drone / Unreal | 기존 맵 저장 변경 없이 명령줄 GameMode Override 실행과 정상 종료 확인 |
| DR-PLAN-PREASSET | Drone / Unreal | Placeholder만으로 Greybox Vertical Slice를 완성하고 구매 후 교체하는 계획 작성 |
| PFN-01 | Drone / Unreal | Prototype 전용 임시 키·Value Type·Modifier·기대 부호를 입력 계약에 기록 |
| PFN-02 | Drone / Unreal | Input Action 5개와 전용 IMC 생성, Action 타입과 Keyboard·Mouse·Gamepad 15개 Mapping 검증 |
| PFN-03 | Drone / Unreal | BP Pawn에 IMC·Input Action 5개와 Engine Cube Placeholder 연결 |
| PFN-04 | Drone / Unreal | BP GameMode의 Default Pawn을 BP Prototype Pawn으로 연결 |
| PFN-05 | Drone / Unreal | 별도 Map에 GameMode Override, PlayerStart 한 개, 배치 Pawn 0개와 Greybox 시험 요소 구성 |
| PFN-06 | Drone / Unreal | Camera·Spawn/Input 반복 PIE: 확정 조작 Automation 3/3, Standalone Keyboard·Mouse 조작과 창 닫기 정상 종료 Pass. 실제 Gamepad 체감은 미확인 |
| HUD-01 | Drone / UI | 공용 Telemetry Snapshot과 10Hz Timer Event 구현. 계산·기본값·Runtime Spawn 검증, Drone 자동화 5/5, Blueprint 0/0 |
| HUD-02 | Drone / UI | C++ Flight HUD 기능·native 직접 실행 fallback과 실제 `WBP_DroneFlightHUD` 외형 구현. BP Controller→WBP, BP GameMode→BP Controller 연결, 필수 TextBlock·폰트·PIE 3회 수명주기 검증, Drone 자동화 7/7, Blueprint 0/0, Standalone WBP 표시 확인 |
| TUT-01 | Drone / Tutorial | `ADroneTrainingCourse`, 실제 `BP_DroneTrainingCourse`, `Lvl_DroneTraining`, 밝은 Cyan `M_DroneTrainingGuide` 구현. Editor Build, Tutorial 3/3, 전체 Drone 10/10, Blueprint Compile, Standalone 시각 확인 통과. Pawn Sweep을 막지 않고 Course 표시 구성요소의 Collision·Overlap·Physics·Navigation 영향이 꺼졌으며 저장된 Recast Actor를 확인함. Map 담당자는 미정 유지 |
| TUT-02 | Drone / Tutorial | `ADroneTrainingGate`, Gate Sequence Component, 실제 `BP_DroneTrainingGate` 네 개 구현. Ring Visual·Pawn Trigger 분리, 현재 순서·정방향·중복 통과와 Current/Completed/Inactive 상태를 검증. Build, Gate Sequence 1/1, 실제 BP PIE Smoke 1/1, Tutorial 4/4, 전체 Drone 11/11, Blueprint 0/0/0, Standalone Current/Inactive 표시 통과. 신규 BP와 갱신 Map 두 Asset LFS Push 완료 |
| TUT-03 | Drone / Tutorial | Course 소유 `UDroneTrainingLapRecorderComponent`와 BlueprintType 기록 Struct 구현. Gate 0 시작, 이후 Gate별 Segment, 마지막 Gate Lap 완료. World Game Time과 Telemetry 10Hz 3차원 위치 표본으로 실제 거리·평균속도를 계산하고 Reset·재구성·Pawn 파괴 시 부분 시도를 폐기. Build, Tutorial 6/6, 전체 Drone 14/14, Blueprint 0/0/0 통과. `551e287`을 feature Branch와 main에 Push |
| AST-00 | Drone / Unreal | 최초 D 드라이브 감사 당시 제공 ZIP 14개와 해제 폴더 14개의 상대 경로·크기를 대조해 Missing/Extra/SizeMismatch 0 확인. 10,499개·35,677,612,290 bytes 기준선과 UE 4.23~5.6 이식 계획 기록. 이 행의 이식 0건은 당시 시점의 역사 기록 |
| AST-VERIFY-01 | Drone / Unreal | 다른 PC의 `C:\에셋` 14개 공급사 해제본·스테이징·내부 FBX를 재감사. 내부 FBX 55개 SHA-256 불일치 0, 프로젝트 선택 자산 12개+Integration BP 1개 존재, 스테이징 선택 자산·현재 Integration 금지 의존성 0, LFS fsck·FPV 자동화 1/1·Blueprint 0/0/0 통과. 소스 팩 Config의 활성 Android 토큰은 값 노출 없이 복사 금지로 기록 |
| AST-02A | Drone / Unreal / UI | NavigationArrows 최소 이식과 main 공유 완료. 기능 폐쇄 집합 6개, 외부 Game 의존성 0. Commit `5a052c8`을 기능 Branch에 Push하고 `fb1d7ad`로 main 병합·Push. 병합 main에서 Build, 전용 1/1, 전체 15/15, BP 0/0/0, LFS 검증 통과. 실제 화면 Host/Wrapper 미구현은 후속 경계 |
| AST-CLEAN-01 | Drone / Unreal / Asset | RabbitHole의 프로젝트 소유 맵 중앙화 방식을 참고해 기존 프로젝트 맵을 `/Game/Drone/Maps`로 모았다. `1c8f391`의 Content Root 전체 삭제는 범위가 넓었고 `909f6a3`에서 비맵 62개를 복구했다. 현재 삭제 대상은 Unreal 생성 기본 Map 4개와 그 전용 ExternalActors/ExternalObjects뿐이다 |
| AST-03A | Drone / Unreal / Asset | `C:\에셋` 세 환경 팩 3,334개·18.76 GiB와 Map 10개를 스테이징 감사했다. 대표 중앙 Map 3개와 정확한 폐쇄 2,723개·16.96 GiB 이식, GameMode Override 제거, 누락 직접 참조·호환 경로 보강, Build·BP 0/0/0·전체 15/15·실제 Map Load·LFS 검증 통과. Battlefield 공급 BP Map Check 메시지 14건과 세 맵 Editor 시각 검토는 별도 수동 항목 |
| UE-MCP-01 | Drone / Unreal / Codex Sync | UE 5.8 공식 `ModelContextProtocol`과 Editor·Automation·UMG·StateTree·AI Toolset을 Editor Target으로 연결. Codex 프로젝트 설정·자동 시작 기본값 추가, Editor/Game Build, 전체 Drone 12/12, HTTP MCP 초기화·23 Toolset·Training Map 상태 조회·12개 테스트 탐색 통과. 새 Codex 작업의 네이티브 노출 확인은 UE-MCP-02로 분리 |
| STUDY-PLAN-01 | 정보처리산업기사 / Coding Test | Q-Net 공식 2026 일정·시험 구성을 확인하고 접수 상태별 Track A/B/C, C++ 주간 병행안과 이동용 통합 문서를 작성 |
| AI-SO-00 | Drone / AI / Smart Object | Plugin·Module·Profile·Native Tag·Character·Controller·Spawn Point·Station·Reservation·Drone Sight 기반. Game/Editor Build, 전용 1/1, 전체 17/17, Blueprint 0/0/0, LFS 검증 후 `489ced5`를 `c3e6d38`로 main 병합·Push |
| AI-SO-01 | Drone / AI / Smart Object | Definition 6종과 Station Blueprint 6종을 실제 생성. 각 Definition Slot 1개·Activity Tag·Gameplay Interaction Behavior, 각 BP의 Activity·Definition과 MG 전용 Mesh를 전용 자동화 및 전체 18/18, Blueprint 0/0/0, LFS fsck로 검증. Interaction StateTree는 후속 카드까지 의도적으로 비움 |
| AI-NPC-01 | Drone / AI | `BP_NPC_Hostile_Rifle`, `BP_NPC_Hostile_Shotgun`, `BP_NPC_Friendly_Base`, `BP_NPCSpawnPoint`와 `Lvl_NPCSmartObjectGreybox` 생성. Rifle 1·Shotgun 1·Friendly 2명, Station 10개, 전용 Navigation Floor·Dynamic Recast를 구성하고 4명 Possess·역할 Tag·NavMesh 투영을 NPC 전용 2/2·전체 20/20·Blueprint 0/0/0으로 검증. Manny/Unarmed은 AI-VIS-01 전 임시 Greybox이며 StateTree·이동·사격은 미구현 |
| AI-PATROL-01 | Drone / AI / Smart Object | `/Game/Drone/AI/StateTrees/ST_NPC_HostilePatrol`과 Native Claim·Move·Wait·Release Task를 구현했다. Hostile 2명이 EnemyPatrol Slot을 예약하고 NavMesh 이동·1초 대기·해제·다른 지점 재선택을 반복한다. Friendly 2명은 정지 상태를 유지한다. AI 6/6 경고·오류 0, 전체 22/22, Blueprint 0/0/0, Game/Editor Build와 LFS 검증 뒤 기능 `a721fe4`를 `095dda7`로 main 병합·Push. 드론 감지는 순찰을 안전 중단하지만 Search·사격 전환은 미구현 |
| AI-FRIEND-01 | Drone / AI / Smart Object | `/Game/Drone/AI/StateTrees/ST_NPC_FriendlyBaseRoutine`과 Friendly Claim·공용 Move/Wait·Friendly Release Task를 구현했다. Friendly 2명이 `FriendlyBasePatrol`과 `Ambient`를 번갈아 Claim하고 서로 다른 지점 2개 이상을 방문한다. Smart Object 1-Slot Claim으로 동시 점유를 막는다. AI 7/7, 전체 23/23, Blueprint 0/0/0, Game/Editor Build와 LFS 검증 뒤 기능 `b5b733f`를 `2fcfb04`로 main 병합·Push. 생활 Animation과 드론 전투 반응은 미구현 |
| AI-PER-01 | Drone / AI / StateTree | Hostile만 Sight Event에 반응해 이동·Claim을 중단하고 마지막 위치를 3초 Search한 뒤 순찰로 복귀한다. Friendly는 루틴을 지속한다. AI 8/8·전체 24/24 자동화와 2026-09-02 사용자 수동 화면 확인에서 정상 동작 Pass. `2054d6f`에 포함돼 Push 완료 |
| AI-WPN-01 | Drone / AI / Combat | `UDroneNPCWeaponComponent`의 공용 `CanFire/StartFire/StopFire/Reload`, 단일 Target Actor·Aim Point 계약을 구현했다. Controller는 Rifle/Shotgun 분기 없이 `DetectedDrone`을 같은 경로로 전달하고 실종·UnPossess 때 발사를 정리한다. 실제 Trace·Damage·탄약은 후속 카드다. Game/Editor Build, AI 9/9, 전체 25/25 통과. `2054d6f`에 포함돼 Push 완료 |
| AI-WPN-02 | Drone / AI / Combat | Rifle Visibility 단일 Trace, 4,000cm Greybox 사거리, 0.25초 Cooldown과 반복 Timer를 구현했다. 장애물·사거리·Cooldown 전용 테스트와 기존 공용 Target/Aim Point 계약 회귀를 통과하고 Game용 테스트의 Editor 의존성도 차단했다. `0d92a5f` 기준 공유 완료 |
| AI-WPN-03 | Drone / AI / Combat | Shotgun 1,600cm·0.9초·8 Pellet·6도 반각 Greybox를 구현했다. 한 Trigger의 다중 Trace, 결정적 Spread, 장애물·사거리·Cooldown과 Rifle 코드 분리를 자동 검증했다. Game/Editor Build, AI 11/11·전체 27/27, Blueprint 0/0/0, LFS fsck 뒤 `0d92a5f`로 Push 완료 |
| AI-MG-01 | Drone / AI / Smart Object | Hostile 감지 StateTree에 MG 1-Slot Claim·NavMesh 이동·도착 뒤 예약 유지 상태를 추가했다. MG 사용 가능 Rifle Hostile 정확히 1명과 예약 1개, Shotgun 개인 무기 Fallback, Friendly 비무장을 PIE로 검증했다. Game/Editor Build, AI 11/11·전체 27/27, Blueprint 0/0/0, LFS fsck 뒤 `249d6cd`로 Push 완료 |
| AI-MG-02 | Drone / AI / Smart Object | MG Claim을 Occupied로 바꾸고 Aim Pivot·6,000cm/0.15초 Trace·발당 8 Damage를 연결했다. 사수 사망·DroneLost·중단 시 Slot을 Free로 만들고 감지 중인 다른 MG 가능 Hostile이 재점유한다. Editor Build와 관련 PIE 1/1 통과, `6a18210` Push 포함 |
| HP-01 | Drone / Combat / UI | NPC·Drone 공통 `UDroneHealthComponent` 기본 100/100, 0 이하 사망 1회, 추가 Damage 무시를 구현했다. Rifle 10·Shotgun 적중 Pellet당 8·MG 8 피해와 NPC/Drone 정지 규칙, 우측 상단 Drone 체력 HUD를 연결했다. 관련 AI PIE·HUD 테스트 각 1/1 통과, `6a18210` Push 포함 |
| AI-COVER-01 | Drone / AI / Smart Object | MG Claim 실패 뒤 Cover 1-Slot을 Claim해 이동·Occupied 전환 후 개인 무기 사격한다. Greybox Map에 Cover Station 2개를 추가했고, MG 사망 뒤 Cover 병사가 Slot을 해제하고 MG를 재점유한다. Editor Build·StateTree/Map 갱신 검증·관련 PIE 1/1 통과, `6a18210` Push 포함 |
| AI-COMBAT-END-01 | Drone / AI / Mission | Drone 체력 0에서 Blueprint `OnDroneDestroyed`를 한 번 보내고 Perception Source를 해제한다. 감지 중인 살아 있는 Hostile의 개인 무기·MG·Cover·이동·마지막 위치를 정리해 Search 없이 Patrol로 복귀시킨다. 사망 Hostile·Friendly 무반응과 중복 Damage Event 방지를 확장 PIE 1/1로 검증, `6a18210` Push 포함 |
| AI-AMMO-01 | Drone / AI / Combat | Rifle 30발·Shotgun 8발 Greybox 탄창, Trace/Volley당 한 발 소모, 빈 탄창 발사 정지·거부, 명시적 즉시 Reload와 AI 자동 요청 경계를 구현했다. 예비 탄약·시간·Animation은 미정. Editor Build와 WeaponContract·Rifle·Shotgun·NPC 교전 집중 테스트 통과, `6a18210` Push 포함 |
| AI-VIS-01A | Drone / AI / Assets | 읽기 전용 감사에서 Manny Rifle Animation 38개·FPS Weapon Mesh 70개·이름으로 식별되는 Shotgun Mesh 0개를 확인했다. Soldier/Insurgent는 Manny와 Skeleton이 다르고 각 이식 Root Animation은 0개다. Weapon Component에 BP `OnWeaponFired`·`OnReloadCompleted`를 추가하고 Build·무기 집중 테스트 3/3 통과, `6a18210` Push 포함 |
| AI-EDITOR-01 | Drone / AI / Unreal Editor | Friendly와 Hostile NPC Actor를 선택하면 `UnrealEditor_PropertyEditor`에서 `EXCEPTION_STACK_OVERFLOW`가 발생하던 문제를 공통 NPC Details 메타데이터 단순화로 해소. 런타임 API·기능은 유지하고 Profile 자동 인라인 표시와 다단계 Category만 제거했다. Editor Build, 사용자 Friendly 선택, MCP Hostile Rifle 선택 생존 검증 통과 후 원격 공유 완료 |
| SYNC-01 | Codex Sync | 목표·완료·진행·결정·미정·다음 작업 형식 정의 |
| SYNC-02 | Codex Sync | `handoff.md` + `manifest.json` Export/Import 구현 |
| SYNC-03 | Codex Sync | 인증·토큰·원시 세션 제외 기준과 검사 구현 |
| SYNC-QA-01 | Codex Sync | Windows PowerShell 5.1 왕복, SHA-256, 변조·추가 파일·비밀 패턴 거부 확인 |
| SYNC-PACKAGE-01 | Codex Sync | 현재 기준 문서를 담은 로컬 인계 패키지 생성, Git 제외 확인. 실제 PC 간 전송은 아직 미수행 |

## 이번 인계의 정지선

Unreal 프로젝트의 초기 Commit은 `91498b7`이고 현재 공유 기준은 `origin/main=2d6a459`다. AI-PER-01부터 AI-VIS-01A와 Smart Object 방향 보강이 원격에 포함됐다. 다른 PC Clone·LFS·UE 5.8.1 실행과 문서 Clone/Pull을 확인하기 전까지 PC 간 전체 공유 흐름은 완료로 닫지 않는다.

Android 제외와 PFN-01~06, HUD-01, HUD-02, TUT-01~03, 최초 에셋 인수 감사 `AST-00`, 다른 PC의 `C:\에셋` 재검증 `AST-VERIFY-01`, NavigationArrows 최소 이식·원격 공유 `AST-02A`를 완료했다. `AST-01`의 실제 Loop 청감은 여전히 수동 미확인이다. 현재 main에는 TUT-04B 이전 평균·Best 비교와 기록 결과 HUD까지 구현됐으며 실제 두 Lap 표시 판정이 남았다. 이후 상세 순서는 `docs/DRONE_FRONTEND_MISSION_FLOW_PLAN.md`, Tutorial·조작 기준은 `docs/DRONE_TUTORIAL_STORY_PLAN.md`를 따른다.

UE-MCP-01도 완료했다. 이후 Editor 내부 Actor·Asset·Blueprint·UMG·Automation 작업은 가능한 범위에서 공식 Unreal MCP를 우선 사용하되, Experimental 기능이므로 실제 Git diff·빌드·자동화 로그를 최종 판정 기준으로 유지한다.

## 2026-08-26 현재 오버레이

- 제공 에셋의 프로젝트 사용 권리는 사용자가 지원과정 구매·지급 근거로 확인했다. 로컬 증빙 파일 미발견은 별도 보관 상태로 기록한다.
- `AST-02A`의 기술 이식·검증·기능 Branch와 `main` Push는 완료했다. 실제 Training HUD 연결은 아직 하지 않았다.
- HUD 연결 전에도 자산은 안전하게 로드 가능한 상태지만, 화면에 보이는 구현으로 과장하지 않는다.
- 프로젝트 소유 맵은 `/Game/Drone/Maps` 한 곳에서 관리한다. 공급사 원본 맵을 추가할 때도 검토용 사본만 이 폴더에 두고 의존 자산은 각 ThirdParty 폴더에 유지한다.
- TUT-04 실제 두 Lap 확인은 그대로 남긴다. `FLOW-01~03`은 로컬 완료됐고 현재 신규 기능은 `FLOW-04`다. `AI-VIS-01B`는 Mission 흐름 뒤로 이동했다.
