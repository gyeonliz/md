# 현재 작업 보드

기준일: 2026-08-26 (Asia/Seoul)

이 보드는 실제로 확인한 결과만 반영한다. 개별 준비 카드가 Done이어도 `Git + Unreal 환경 구축` 전체는 첫 Push, 다른 PC Clone, LFS 확인, Clone한 프로젝트 실행까지 성공해야 완료다.

Unreal 현재 기준선은 로컬 `main`과 `origin/main`이 일치하는 Merge Commit `2cc5d79`이다. `fb1d7ad` 이후 맵 중앙화와 미사용 템플릿 콘텐츠 제거 Commit `1c8f391`을 병합했으며 작업 트리는 Clean이다. 기능 실행 순서는 `TUT-04 비교·결과 UI → Flight 상태 → Operator↔Drone → Story/NPC/Mission → AI/MG/Jamming`이며, 검증된 소형 에셋 이식은 기능 작업과 병행한다.

## 현재 작업 스냅샷

마지막 갱신: 2026-08-26 17:31 KST — 맵 중앙화·미사용 템플릿 콘텐츠 정리 완료

| 항목 | 상태 |
|---|---|
| 현재 단계 | 3단계 Tutorial Vertical Slice — `TUT-04A` 자동 검증과 PIE 초기 화면 통과, 한 Lap 구간 값 갱신 확인 대기 |
| 진행 정도 | 한글 현재 속도·고도·수직속도·방향과 구간 기록 패널, 현재 Gate와 세분화 코스 선을 실제 PIE에서 확인했다. 최근·평균 구간 값은 코드·자동화 검증을 통과했지만 실제 Gate 0→3 비행 후 숫자 갱신은 아직 확인하지 않았다 |
| 지금 작업 중 | 맵 중앙화·템플릿 콘텐츠 정리와 원격 반영까지 완료했다. Unreal 실행은 0이며 실제 한 Lap 수동 비행 확인이 남았다. 환경 맵 이식은 별도 일시 중단 상태다 |
| 완료 근거 | `main=origin/main=2cc5d79`. 중앙 맵 3개와 BuiltData 로드, 이전 경로·템플릿 루트 부재, `DroneEditor` Build, 전체 `Drone.` 15/15, Blueprint 0/0/0, LFS fsck 통과 |
| 수동 미확인 | Gate 0→3 한 Lap 후 최근·완료 구간 숫자 갱신, 저장 Map의 GateIndex 0~3 상세 확인, DronePack 화면·Loop 청감, 환경 맵 3종 로드·Map Check는 미확인 |
| 현재 차단 | 기능 코드의 기술 차단은 없다. 자동 UI 제어는 지속 키 입력이 짧아 한 Lap을 재현하지 못했다. TUT-04A 완료 판정에는 사람이 실제 한 바퀴를 비행한 화면 결과가 남아 있다 |
| 다음 행동 | `Lvl_DroneTraining`에서 Gate 0→3을 실제로 한 바퀴 비행해 방금 구간·완료 구간 속도/거리/시간 갱신을 확인한다. 통과 후 `TUT-04B` 이전 성공 Lap 평균·Best 비교로 진행한다 |
| 다음 기능 | TUT-04A 한 Lap 수동 확인 후 이전 성공 Lap 평균·Best 대비 `+/-` 비교를 `TUT-04B`로 구현 |
| 에셋 인수 | 이번 확인 PC의 제공 에셋 루트는 `C:\에셋`. NavigationArrows 6개는 main 반영 완료. D 드라이브 환경 팩 스테이징은 별도 PC의 중단 기록으로 보존 |
| 맵 이식 | 프로젝트 맵 3개를 `/Game/Drone/Maps`로 중앙화했다. 기존 `Map_Demo`는 `Lvl_DronePackShowcase`로 변경했고 Editor 시각 검토는 대기 중이다. Battlefield·MilitaryCamp·MilitaryBase 대표 맵은 실제 저장소 미이식, AST-03A Doing |
| Editor/MCP | 2026-08-26 17:31 KST 현재 `UnrealEditor`와 `UnrealEditor-Cmd` 실행 0. Codex 네이티브 Tool 노출은 `UE-MCP-02` 미확인 |
| 확정 후속 방향 | UE 5.8 Dataflow/Chaos로 부분 고정 그물과 선택형 맵 파괴를 구현 후보로 채택. Plugin·자산·코드는 아직 변경하지 않았으며 TUT-04/Flight Collision 기준 뒤 별도 Spike |
| Git 처리 | 이번 확인 PC의 `C:\URproject\drone`은 `main=origin/main=2cc5d79`, 작업 트리 Clean. 맵 중앙화·템플릿 정리 기능 Commit은 `1c8f391`, main 병합 Commit은 `2cc5d79` |
| 학습 일정 | 정보처리산업기사 2026년 공식 일정 확인 완료. 개인 접수·필기일·면제 상태는 미확인, 코딩테스트는 공통 시험일 없음 |
| 학습 다음 행동 | Q-Net 상태를 확인해 Track A/B/C를 고르고 첫 학습 블록 실행 |

상세 변경 이력은 [`docs/DRONE_WORKLOG.md`](docs/DRONE_WORKLOG.md)에 계속 추가한다. 매 구현 작업 종료 시 이 스냅샷의 현재 작업·완료 근거·다음 작업을 함께 갱신한다.

## Inbox

| ID | 태그 | 작업 | 활성화 조건 |
|---|---|---|---|
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
| PHY-DF-00 | Drone / Physics / Unreal | Dataflow·Chaos Physics Sandbox | TUT-04 완료 또는 사용자 우선순위 변경 후 별도 Branch에서 Plugin·Build·회귀 검증 |
| PHY-NET-01 | Drone / Physics | 일부 고정 그물 Cloth Spike | PHY-DF-00 + Flight Collision 기준 완료 |
| PHY-DST-01 | Drone / Physics / Mission | 선택형 Geometry Collection 파괴 Spike | PHY-DF-00 + Damage/Crash Event 기준 완료 |

## Todo

| ID | 태그 | 작업 | 완료 조건 |
|---|---|---|---|
| GIT-10 | Git / Unreal | 다른 PC Clone과 실행 | LFS 포함 Clone 후 UE 5.8.1에서 열림 |
| SYNC-04 | Codex Sync | 두 PC 간 실제 수동 인계 시험 | Git 흐름과 문맥 패키지 흐름을 각각 완료 |
| TUT-04 | Drone / Tutorial / UI | 이전 기록 비교와 결과 UI | 성공 Lap 원본을 기준으로 이전 평균·Best 규칙을 확정하고 Blueprint 결과 UI와 회귀 검증 완료 |
| UE-MCP-02 | Drone / Unreal / Codex Sync | Codex 네이티브 MCP Tool 노출 확인 | Unreal Editor 실행 후 `D:\JGY\project\drone` 루트의 새 Codex 작업에서 `unreal-mcp` Tool을 찾고 Current Level을 한 번 조회 |
| STUDY-EXAM-01 | 정보처리산업기사 | Q-Net 개인 상태 확인 | 3회 접수·수험일·응시 여부·필기 합격/면제 상태를 확인하고 Track A/B/C 기록 |
| STUDY-EXAM-02 | 정보처리산업기사 | 선택 Track 첫 학습 | 필기 60문항 진단 또는 실기 기초 1블록과 오답 기록 완료 |
| STUDY-CT-01 | Coding Test | C++ 기본 진단 시작 | 첫 문제 직접 풀이·실패 이유·재풀이 날짜 기록 |

## Doing

| ID | 태그 | 작업 | 현재 확인 | 남은 완료 조건 |
|---|---|---|---|---|
| AST-01 | Drone / Unreal | 제공 에셋 최소 외형 Spike | FPV 본체·로터 4·재질/Texture와 44.1 kHz Loop Cue/Wave를 `/Game/Drone/ThirdParty`로 선별 이식. Integration BP와 GameMode 연결. 이번 재검증에서 전용 자동화 1/1·의존성 감사·Blueprint 0/0/0·LFS fsck 통과. 전체 14/14는 TUT-03 당시 같은 Commit의 기준선이며 이번에 미재실행 | 실제 스피커 출력의 Loop 단일 재생·종료 정지는 미확인. 결과 확보 전까지 Doing 유지 |
| AST-01C | Drone / Unreal / Asset | DronePack 드론 시각 라이브러리·데모 맵 | 드론 Mesh·Material·Texture와 정리 Map 154개를 `/Game/Drone/ThirdParty/DronePack`에 선별 이식. Build·전체 14/14·BP 0/0/0·Map Check 0/0·의존성·LFS 검증 통과 | Editor에서 드론 6종·맵 화면을 확인하고 재질·스케일·조명 이상 유무를 기록 |
| TUT-04A | Drone / Tutorial / UI | 한글 비행·구간 통계 HUD와 Course Authoring 보강 | 병합 main Build·전체 15/15·BP 0/0/0 통과. PIE에서 한글 HUD 두 패널·현재 Gate·세분화 코스 선 초기 렌더 확인 | Gate 0→3 실제 한 Lap 뒤 최근·완료 구간 숫자 갱신 확인 |
| AST-03A | Drone / Unreal / Asset | Battlefield·MilitaryCamp·MilitaryBase 환경 맵 이식 | 원본 3팩 3,334개·약 20.14 GB, Map 10개 감사. Battlefield 1,191개는 스테이징 새 경로 변환, 원본 쪽에 비호환 Demo Character 102개 잔류 | 팩별 변환·의존성 검사 완료 후 실제 `/Game/Drone/ThirdParty/Environments` 복사와 세 대표 Map 검증 |

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
| TUT-02 | Drone / Tutorial | `ADroneTrainingGate`, Gate Sequence Component, 실제 `BP_DroneTrainingGate` 네 개 구현. Ring Visual·Pawn Trigger 분리, 현재 순서·정방향·중복 통과와 Current/Completed/Inactive 상태를 검증. Build, Gate Sequence 1/1, 실제 BP PIE Smoke 1/1, Tutorial 4/4, 전체 Drone 11/11, Blueprint 0/0/0, Standalone Current/Inactive 표시 통과. 신규 BP와 갱신 Map 두 Asset LFS Push 완료 |
| TUT-03 | Drone / Tutorial | Course 소유 `UDroneTrainingLapRecorderComponent`와 BlueprintType 기록 Struct 구현. Gate 0 시작, 이후 Gate별 Segment, 마지막 Gate Lap 완료. World Game Time과 Telemetry 10Hz 3차원 위치 표본으로 실제 거리·평균속도를 계산하고 Reset·재구성·Pawn 파괴 시 부분 시도를 폐기. Build, Tutorial 6/6, 전체 Drone 14/14, Blueprint 0/0/0 통과. `551e287`을 feature Branch와 main에 Push |
| AST-00 | Drone / Unreal | 최초 D 드라이브 감사 당시 제공 ZIP 14개와 해제 폴더 14개의 상대 경로·크기를 대조해 Missing/Extra/SizeMismatch 0 확인. 10,499개·35,677,612,290 bytes 기준선과 UE 4.23~5.6 이식 계획 기록. 이 행의 이식 0건은 당시 시점의 역사 기록 |
| AST-VERIFY-01 | Drone / Unreal | 다른 PC의 `C:\에셋` 14개 공급사 해제본·스테이징·내부 FBX를 재감사. 내부 FBX 55개 SHA-256 불일치 0, 프로젝트 선택 자산 12개+Integration BP 1개 존재, 스테이징 선택 자산·현재 Integration 금지 의존성 0, LFS fsck·FPV 자동화 1/1·Blueprint 0/0/0 통과. 소스 팩 Config의 활성 Android 토큰은 값 노출 없이 복사 금지로 기록 |
| AST-02A | Drone / Unreal / UI | NavigationArrows 최소 이식과 main 공유 완료. 기능 폐쇄 집합 6개, 외부 Game 의존성 0. Commit `5a052c8`을 기능 Branch에 Push하고 `fb1d7ad`로 main 병합·Push. 병합 main에서 Build, 전용 1/1, 전체 15/15, BP 0/0/0, LFS 검증 통과. 실제 화면 Host/Wrapper 미구현은 후속 경계 |
| AST-CLEAN-01 | Drone / Unreal / Asset | RabbitHole의 프로젝트 소유 맵 중앙화 방식을 참고해 `/Game/Drone/Maps`로 맵 3개를 모았다. 미사용 `ThirdPerson`과 Variant 콘텐츠 3종 및 대응 ExternalActors/ExternalObjects를 제거했다. 중앙 맵 로드·이전 경로 부재·Build·전체 15/15·BP 0/0/0·LFS 검증 뒤 `2cc5d79`로 main Push 완료. C++ Legacy/Variant 코드는 별도 감사 전까지 보존 |
| UE-MCP-01 | Drone / Unreal / Codex Sync | UE 5.8 공식 `ModelContextProtocol`과 Editor·Automation·UMG·StateTree·AI Toolset을 Editor Target으로 연결. Codex 프로젝트 설정·자동 시작 기본값 추가, Editor/Game Build, 전체 Drone 12/12, HTTP MCP 초기화·23 Toolset·Training Map 상태 조회·12개 테스트 탐색 통과. 새 Codex 작업의 네이티브 노출 확인은 UE-MCP-02로 분리 |
| STUDY-PLAN-01 | 정보처리산업기사 / Coding Test | Q-Net 공식 2026 일정·시험 구성을 확인하고 접수 상태별 Track A/B/C, C++ 주간 병행안과 이동용 통합 문서를 작성 |
| SYNC-01 | Codex Sync | 목표·완료·진행·결정·미정·다음 작업 형식 정의 |
| SYNC-02 | Codex Sync | `handoff.md` + `manifest.json` Export/Import 구현 |
| SYNC-03 | Codex Sync | 인증·토큰·원시 세션 제외 기준과 검사 구현 |
| SYNC-QA-01 | Codex Sync | Windows PowerShell 5.1 왕복, SHA-256, 변조·추가 파일·비밀 패턴 거부 확인 |
| SYNC-PACKAGE-01 | Codex Sync | 현재 기준 문서를 담은 로컬 인계 패키지 생성, Git 제외 확인. 실제 PC 간 전송은 아직 미수행 |

## 이번 인계의 정지선

Unreal 프로젝트의 초기 Commit은 `91498b7`이고 현재 로컬 `main`과 `origin/main`은 Merge Commit `2cc5d79`로 일치한다. `1c8f391`은 맵 중앙화·템플릿 콘텐츠 정리 기능 Commit, `fb1d7ad`는 그 직전 NavigationArrows 병합 기준선, `551e287`은 TUT-03 기준선이다. 다른 PC Clone·LFS·UE 5.8.1 실행과 문서 Clone/Pull을 확인하기 전까지 PC 간 전체 공유 흐름은 완료로 닫지 않는다.

Android 제외와 PFN-01~06, HUD-01, HUD-02, TUT-01~03, 최초 에셋 인수 감사 `AST-00`, 다른 PC의 `C:\에셋` 재검증 `AST-VERIFY-01`, NavigationArrows 최소 이식·원격 공유 `AST-02A`를 완료했다. `AST-01`은 선택 자산 12개와 Integration BP 이식 뒤 기존 전체 회귀와 Standalone 초기 렌더를 통과했고, 이번에는 FPV 1/1·Blueprint 0/0/0·의존성·LFS만 다시 검증했다. 실제 Loop 단일 재생·종료 정지는 수동 미확인이므로 Pass나 Fail로 간주하지 않고 Doing을 유지한다. 다음 기능 카드는 `TUT-04`이며 이전 평균·Best 비교와 기록 결과 UI는 아직 구현된 기능으로 보지 않는다. 이후 상세 순서와 Tutorial/Story 범위는 `docs/DRONE_TUTORIAL_STORY_PLAN.md`가 우선한다.

UE-MCP-01도 완료했다. 이후 Editor 내부 Actor·Asset·Blueprint·UMG·Automation 작업은 가능한 범위에서 공식 Unreal MCP를 우선 사용하되, Experimental 기능이므로 실제 Git diff·빌드·자동화 로그를 최종 판정 기준으로 유지한다.

## 2026-08-26 현재 오버레이

- 제공 에셋의 프로젝트 사용 권리는 사용자가 지원과정 구매·지급 근거로 확인했다. 로컬 증빙 파일 미발견은 별도 보관 상태로 기록한다.
- `AST-02A`의 기술 이식·검증·기능 Branch와 `main` Push는 완료했다. 실제 Training HUD 연결은 아직 하지 않았다.
- HUD 연결 전에도 자산은 안전하게 로드 가능한 상태지만, 화면에 보이는 구현으로 과장하지 않는다.
- 프로젝트 소유 맵은 `/Game/Drone/Maps` 한 곳에서 관리한다. 공급사 원본 맵을 추가할 때도 검토용 사본만 이 폴더에 두고 의존 자산은 각 ThirdParty 폴더에 유지한다.
- 바로 다음 기능은 기존 우선순위의 `TUT-04`다. 프로젝트 소유 Navigation Host/Wrapper 화면 연결은 별도 후속 카드로 시작한다.
