# 현재 작업 보드

기준일: 2026-08-23 (Asia/Seoul)

이 보드는 실제로 확인한 결과만 반영한다. 개별 준비 카드가 Done이어도 `Git + Unreal 환경 구축` 전체는 첫 Push, 다른 PC Clone, LFS 확인, Clone한 프로젝트 실행까지 성공해야 완료다.

Unreal 작업 기준은 로컬 `main`과 `origin/main`이 일치하는 TUT-01 완료 Commit `5a9a2fa`이다. 소스 Branch `codex/tutorial-training-course`도 Push했다. 현재 기능 실행 순서는 `TUT-02 Gate → TUT-03~04 기록·결과 UI → Flight 상태 → Operator↔Drone → Story/NPC/Mission → AI/MG/Jamming → 에셋 적용`이다.

## 현재 작업 스냅샷

마지막 갱신: 2026-08-23 15:42 KST

| 항목 | 상태 |
|---|---|
| 현재 단계 | 3단계 Tutorial Vertical Slice — `TUT-01` 완료, `TUT-02` Todo |
| 진행 정도 | Training Map·편집용 Spline·Standalone 표시선과 비간섭 검증 완료 |
| 지금 작업 중 | 없음. 다음 카드 `TUT-02`의 담당자는 현재 미정 |
| 완료 근거 | Editor Build 성공, `Drone.Tutorial` 3/3 및 전체 `Drone.` 10/10 경고·실패 0, Blueprint Compile 오류·경고·Load 실패 0, Standalone 실제 BP Pawn·Controller·WBP HUD와 밝은 Cyan Spline 확인 |
| 현재 차단 | 없음. Android는 사용자 결정에 따라 작업 범위에서 제외 |
| 다음 행동 | `TUT-02` 순서형 Ring Gate의 Trigger·순서·방향 판정 설계와 구현 |
| 다음 기능 | `TUT-02` 순서형 Ring Gate. Lap·Timing은 아직 미구현 |

상세 변경 이력은 [`docs/DRONE_WORKLOG.md`](docs/DRONE_WORKLOG.md)에 계속 추가한다. 매 구현 작업 종료 시 이 스냅샷의 현재 작업·완료 근거·다음 작업을 함께 갱신한다.

## Inbox

| ID | 태그 | 작업 | 활성화 조건 |
|---|---|---|---|
| STUDY-EXAM-01 | 정보처리산업기사 | D-Day 세부 계획 작성 | 시험 날짜 확정 |
| STUDY-CT-01 | Coding Test | 첫 C++ 문제 세트 선택 | 주간 프로젝트 시간 배분 결정 |
| PF-01 | Portfolio | 데모 기능별 기록 시작 | 첫 재현 가능한 Drone 기능 완료 |
| DR-FUTURE-01 | Drone | 배터리·통신·재밍·멀티 후보 평가 | Flight MVP 이후 |
| PFN-P2 | Drone | Flight MVP 카드 PFN-07~14 활성화 | Tutorial Vertical Slice 통과 |
| PFN-P3 | Drone | Mission Shell 카드 PFN-15~21 활성화 | PFN-14 통과 |
| PFN-P4 | Drone / Unreal | Enemy AI·Turret 카드 PFN-22~32 활성화 | PFN-21 통과 |
| PFN-P5 | Drone / Unreal | 통합 Greybox 카드 PFN-33~38 활성화 | PFN-32 통과 |
| CTRL-02 | Drone / Story | Operator↔Drone Possess·Camera 전환 | Tutorial Vertical Slice 통과 |
| STY-01 | Drone / Story | NPC 대화·Mission UI Story Shell | CTRL-02 통과 |
| PFN-P6 | Drone / Unreal | 에셋 교체 준비 카드 PFN-39~43 활성화 | PFN-38 완료 + 최신 PFN-37 결과 3회 Pass |
| ASSET-GATE-01 | Drone / Unreal | 구매 소스 후보 비교와 구매 결정 | Greybox Vertical Slice 3회 Pass와 차단 결함 0건 |

## Todo

| ID | 태그 | 작업 | 완료 조건 |
|---|---|---|---|
| GIT-10 | Git / Unreal | 다른 PC Clone과 실행 | LFS 포함 Clone 후 UE 5.8.1에서 열림 |
| SYNC-04 | Codex Sync | 두 PC 간 실제 수동 인계 시험 | Git 흐름과 문맥 패키지 흐름을 각각 완료 |
| TUT-02 | Drone / Tutorial | 순서형 Ring Gate | Gate Trigger와 순서·방향 판정을 구현하고 성공·실패 흐름 검증. 담당자는 현재 미정 |

## Doing

| ID | 태그 | 작업 | 현재 확인 | 남은 완료 조건 |
|---|---|---|---|---|
| — | — | 현재 Doing 카드 없음 | `TUT-02`는 Todo, 담당자는 현재 미정 | — |

## Done

| ID | 태그 | 검증 결과 |
|---|---|---|
| WM-01 | 전체 관리 | 이 파일에 Inbox/Todo/Doing/Done과 일곱 분류 태그 사용 가능 |
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
| SYNC-01 | Codex Sync | 목표·완료·진행·결정·미정·다음 작업 형식 정의 |
| SYNC-02 | Codex Sync | `handoff.md` + `manifest.json` Export/Import 구현 |
| SYNC-03 | Codex Sync | 인증·토큰·원시 세션 제외 기준과 검사 구현 |
| SYNC-QA-01 | Codex Sync | Windows PowerShell 5.1 왕복, SHA-256, 변조·추가 파일·비밀 패턴 거부 확인 |
| SYNC-PACKAGE-01 | Codex Sync | 현재 기준 문서를 담은 로컬 인계 패키지 생성, Git 제외 확인. 실제 PC 간 전송은 아직 미수행 |

## 이번 인계의 정지선

Unreal 프로젝트의 초기 Commit은 `91498b7`이고 현재 로컬 `main`과 `origin/main`은 TUT-01 완료 Commit `5a9a2faed4591a574988b649278cb0f166e31267` (`feat: add tutorial training course`)로 일치한다. 소스 Branch `codex/tutorial-training-course`도 Push했다. `410c940`은 native HUD 기준선이고 `9f91bb6`은 WBP/BP 연결 기준선이다. 다른 PC Clone·LFS·UE 5.8.1 실행과 문서 Clone/Pull을 확인하기 전까지 PC 간 전체 공유 흐름은 완료로 닫지 않는다.

Android 제외와 PFN-01~06, HUD-01, HUD-02, TUT-01을 완료했다. 공용 Telemetry Component는 기본 10Hz Snapshot Event를 제공하고 C++ PlayerController/HUD 기능과 실제 WBP가 현재 Possess Drone의 네 수치를 표시한다. 별도 Training Map에서는 실제 BP Course의 밝은 Cyan Spline이 비행·Collision·Navigation을 방해하지 않는다. 다음 카드는 TUT-02이며 Gate·Trigger·순서·방향·Lap·Timing은 아직 구현된 기능으로 보지 않는다. 이후 상세 순서와 Tutorial/Story 범위는 `docs/DRONE_TUTORIAL_STORY_PLAN.md`가 우선한다. 구매 소스는 현재 구현의 선행 조건으로 두지 않는다.
