# Unreal · Git · Codex 작업 공유 저장소

이 폴더는 실제 Unreal 프로젝트가 아니라 다음 작업을 준비하고 PC 간 문맥을 이어가기 위한 문서·템플릿·도구 저장소다. GitHub `gyeonliz/md`를 이 폴더의 공유 원격으로 사용하고, 실제 Unreal 프로젝트는 별도 `gyeonliz/drone` 저장소로 관리한다.

## 먼저 읽을 파일

1. [`CONTEXT.md`](CONTEXT.md): 사용자가 제공한 확정 기준과 미정 사항
2. [`STATUS.md`](STATUS.md): 현재 작업컴에서 실제 확인한 환경과 남은 선택
3. [`WORKBOARD.md`](WORKBOARD.md): 실제 확인 결과를 반영한 현재 보드
4. [`docs/MOBILE_CURRENT_BRIEF.md`](docs/MOBILE_CURRENT_BRIEF.md): 이동 중 읽는 코드 현황·내 작업·공식 시험 일정·날짜별 공부 계획
5. [`docs/DRONE_WORKLOG.md`](docs/DRONE_WORKLOG.md): 현재 작업 위치와 날짜별 변경·검증·다음 작업 기록
6. [`docs/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md`](docs/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md): 현재 코드·Asset 책임, 구현 경계와 사용자가 직접 확인할 작업
7. [`docs/GIT_UNREAL_GUIDE.md`](docs/GIT_UNREAL_GUIDE.md): Unreal 프로젝트 Git/GitHub 실전 절차
8. [`docs/CODEX_CONTEXT_SYNC.md`](docs/CODEX_CONTEXT_SYNC.md): 메인컴 ↔ 작업컴 문맥 전달 절차
9. [`docs/DRONE_PROJECT_AUDIT.md`](docs/DRONE_PROJECT_AUDIT.md): 현재 후보 프로젝트의 실제 C++·입력·맵 구조 감사
10. [`docs/DRONE_PROTOTYPE_IMPLEMENTATION.md`](docs/DRONE_PROTOTYPE_IMPLEMENTATION.md): 실제 C++ Prototype 구현·검증과 Editor 연결 절차
11. [`docs/DRONE_PROTOTYPE_INPUT_CONTRACT.md`](docs/DRONE_PROTOTYPE_INPUT_CONTRACT.md): 현재 Prototype 전용 임시 입력 계약
12. [`docs/DRONE_PROTOTYPE_PIE_CHECKLIST.md`](docs/DRONE_PROTOTYPE_PIE_CHECKLIST.md): PFN-06 자동화 결과와 수동 화면 체크리스트
13. [`docs/DRONE_TELEMETRY_IMPLEMENTATION.md`](docs/DRONE_TELEMETRY_IMPLEMENTATION.md): HUD-01 Snapshot 공급과 HUD-02 Flight HUD 구현·검증
14. [`docs/DRONE_TRAINING_RECORDING_IMPLEMENTATION.md`](docs/DRONE_TRAINING_RECORDING_IMPLEMENTATION.md): TUT-03 구간·랩 기록 구조, Blueprint 연결점과 검증 절차
15. [`docs/DRONE_PREASSET_FUNCTION_PLAN.md`](docs/DRONE_PREASSET_FUNCTION_PLAN.md): 구매 소스 없이 Greybox 기능을 먼저 완성하는 실행 계획
16. [`docs/DRONE_MVP_GUIDE.md`](docs/DRONE_MVP_GUIDE.md): Flight MVP부터 데모까지의 개발 단위
17. [`docs/DRONE_SMART_OBJECT_NPC_GUIDE.md`](docs/DRONE_SMART_OBJECT_NPC_GUIDE.md): 적 순찰·드론 감지·Rifle/Shotgun·MG와 기지 아군 Smart Object 이동 준비·사용 절차
18. [`docs/WORK_MANAGEMENT.md`](docs/WORK_MANAGEMENT.md): Inbox → Todo → Doing → Done 운영
19. [`docs/DRONE_FRONTEND_MISSION_FLOW_PLAN.md`](docs/DRONE_FRONTEND_MISSION_FLOW_PLAN.md): 시작 트레일러·로비·미션 선택·브리핑·Map·Drone 선택·목표 UI의 최신 최우선 흐름
20. [`docs/DRONE_TUTORIAL_STORY_PLAN.md`](docs/DRONE_TUTORIAL_STORY_PLAN.md): 확정 조작, Tutorial 코스·기록 UI, Mission·Jamming·에셋 적용 계획
21. [`docs/DRONE_ASSET_INTAKE_2026-08-25.md`](docs/DRONE_ASSET_INTAKE_2026-08-25.md): 최초 D 드라이브 14팩 압축 감사, 다른 PC의 C 드라이브 재감사와 FPV·Loop 선별 이식 검증
22. [`docs/DRONE_REMAINING_ASSET_MIGRATION_2026-08-27.md`](docs/DRONE_REMAINING_ASSET_MIGRATION_2026-08-27.md): 남은 제공 자산 891개·OilRig 중앙 맵·TUT-04B 이식 및 검증
23. [`docs/DRONE_UNREAL_MCP.md`](docs/DRONE_UNREAL_MCP.md): UE 5.8 공식 Unreal MCP·Codex 연결, 선택 Toolset과 검증 기준
24. [`docs/DRONE_CHAOS_DATAFLOW_PLAN.md`](docs/DRONE_CHAOS_DATAFLOW_PLAN.md): UE 5.8 Dataflow 기반 부분 고정 그물·선택형 맵 파괴 설계와 검증 순서
25. [`docs/UNREAL_PROJECT_EXPERIENCE_DESCRIPTION.md`](docs/UNREAL_PROJECT_EXPERIENCE_DESCRIPTION.md): 지원서·이력서용 Unreal 프로젝트 경험 기술 예시와 사실 확인 경계
26. [`docs/STUDY_PLANS.md`](docs/STUDY_PLANS.md): 정보처리산업기사·C++ 코딩테스트 병행 계획
27. [`docs/DRONE_PROJECT_PLANNING_BRIEF.md`](docs/DRONE_PROJECT_PLANNING_BRIEF.md): 게임 기획·화면 흐름·UI·현재 구현·로드맵·검증을 한 문서로 정리한 통합 기획서

## 구성

```text
CONTEXT.md                 기준 컨텍스트
STATUS.md                  작업컴 점검 결과와 다음 결정
WORKBOARD.md               현재 Inbox/Todo/Doing/Done
docs/                      실행 가이드와 계획
templates/unreal/          Unreal 프로젝트 루트용 Git 템플릿
tools/context-sync/        검토 가능한 작업 문맥 Export/Import 도구
tools/unreal/              Prototype·Tutorial 자산 생성·재검증용 안전 실행 도구
```

## 중요한 경계

- Unreal 프로젝트 파일은 `gyeonliz/drone` Git/GitHub 저장소로 전달한다.
- 검토 가능한 Markdown 작업 문맥·계획·가이드는 `gyeonliz/md` 저장소로 전달한다.
- 특정 시점의 단일 인계본이 필요하면 사람이 읽을 수 있는 별도 handoff 패키지를 보조 수단으로 사용한다.
- `.codex` 전체, `auth.json`, 토큰, 비밀번호, 브라우저 프로필, 원시 세션 DB는 이 방식으로 복사하지 않는다.
- `templates/unreal`의 파일은 실제 프로젝트의 기존 규칙을 확인한 뒤 병합한다. 기존 파일을 무조건 덮어쓰지 않는다.

## 현재 진행 지점

현재 실행 세션의 Unreal 저장소는 `C:\URproject\drone`, 문서 저장소는 이 폴더다. `D:\JGY\project`는 다른 PC에서 사용한 이전 경로다. 별도 `ADronePrototypePawn`과 GameMode, 5개 Input Action, Keyboard·Mouse·Gamepad 15개 Mapping, BP Pawn/GameMode와 Greybox Map을 연결했다. Camera는 Drone 뒤 고정 추적, Mouse X는 Drone Yaw, Mouse Y는 Camera Pitch로 동작한다.

확정 조작을 반영한 PFN-06은 자동화와 Standalone 수동 조작을 통과해 Done이다. HUD-01 공용 Telemetry Component는 기본 10Hz Snapshot Event를 제공한다. HUD-02는 C++가 계산·생성·Possession·Delegate 수명주기를 맡고 실제 `WBP_DroneFlightHUD`가 화면 외형을 맡도록 연결했다.

TUT-01~03을 완료했다. 별도 `Lvl_DroneTraining` Map의 실제 `BP_DroneTrainingCourse`가 편집 가능한 Spline과 Runtime 표시용 SplineMesh를 소유한다. `ADroneTrainingGate`는 비충돌 Ring Visual과 별도 Pawn Overlap Trigger를 분리하고, `UDroneTrainingGateSequenceComponent`가 Course의 명시적 Gate 배열을 기준으로 현재 순서·정방향·중복 통과를 판정한다. 실제 `BP_DroneTrainingGate` 네 개를 Map에 연결했으며 기존 Prototype BP GameMode·FPV Integration Pawn·PlayerController·WBP를 그대로 재사용한다.

TUT-03에서는 Course 소유 `UDroneTrainingLapRecorderComponent`를 Gate 판정과 분리했다. Gate 0 승인으로 Lap을 시작하고 이후 Gate마다 Segment를 확정하며, 마지막 Gate에서 Lap을 완료한다. TUT-04B는 현재 기록을 제외한 이전 성공 평균, Best, 시간·속도 Delta와 Segment 비교를 계산하고 Flight HUD에 표시한다. 최신 전체 검증은 Game/Editor Build와 전체 `Drone.` 25/25를 통과했다. 직전 Blueprint Compile은 0/0/0이며 실제 두 Lap 화면 확인은 남아 있다.

2026-09-03부터 게임 진입 흐름은 `시작 트레일러 → 로비 → 미션 선택/측면 설명 → 하단 시작 → 미션 트레일러 → Map → Drone 선택 → Mission 시작/측면 목표 UI`다. 사람 Player Character, 로비 NPC 대화 수령과 Operator↔Drone 전환은 폐기했다. `FLOW-01~03` 상태·데이터, 정적 시작 화면→로비, Training Mission 선택·설명·시작은 로컬 구현·검증했고 기존 적 NPC·Smart Object·전투 기능은 Mission Map 내부에 재사용한다.

현재 D 드라이브 작업 PC의 제공 에셋 루트는 `D:\JGY\project\Unreal_260821`이다. 초기 FPV 외형·Loop와 Integration BP에 이어 ArmyVFX·InfantrySFX·Ground Drone/MG·NPC 외형·Raw Drone 후보와 OilRig을 선별 이식했다. 원본 제공 폴더는 수정하지 않았고 실제 프로젝트의 새 자산 외부·누락 참조는 0이다. 실제 스피커의 Loop 단일 재생과 종료 정지는 수동 미확인이므로 `AST-01`은 Doing이다. 상세 결과는 [`docs/DRONE_ASSET_INTAKE_2026-08-25.md`](docs/DRONE_ASSET_INTAKE_2026-08-25.md)와 [`docs/DRONE_REMAINING_ASSET_MIGRATION_2026-08-27.md`](docs/DRONE_REMAINING_ASSET_MIGRATION_2026-08-27.md)를 따른다.

NPC·AI를 위해 Smart Objects와 Gameplay Interactions 모듈, Faction·Rifle·Shotgun Profile, Activity Tag, NPC Character/Controller/Spawn Point, Slot 예약 Component와 드론 Sight를 구성했다. 현재 공유 `2d6a459`에는 Rifle/Shotgun Trace·Damage·탄창, MG 점유·조준·사격·사망 교대, Cover, Drone 체력·파괴 교전 종료, Blueprint 표현 Event와 Smart Object 방향 보강까지 포함한다. 실제 Mesh·Animation·FX·SFX와 Mission 결과 화면은 미구현이며, AI 비주얼 작업은 새 Front-end Mission Vertical Slice 뒤에 잇는다.

2026-09-03 현재 Unreal 공유 기준은 `main=origin/main=2d6a459`이다. 그 위에 FLOW-01~03, Front-end Blueprint/Map, NPC Weapon Visual 기반을 합친 26개 경로가 로컬 미커밋이며 문서 변경도 사용자가 직접 Commit하기 전 상태다. Codex는 Commit·Push하지 않았다.

외부 제공 소스는 전체 팩을 흡수하지 않고 검증된 대표 자산과 정확한 의존성만 ThirdParty 경계로 선별 이식했다. 기능 구현은 계속 프로젝트 C++와 Greybox 기준을 유지하며 외부 Pawn·GameMode·Input은 사용하지 않는다. 현재 신규 기능 실행 순서는 [`DRONE_FRONTEND_MISSION_FLOW_PLAN.md`](docs/DRONE_FRONTEND_MISSION_FLOW_PLAN.md)가 우선하고 Tutorial·PFN 카드 번호와 교체 경계는 기존 계획 문서를 함께 따른다.

2026-08-25에는 UE 5.8.1에 포함된 Epic 공식 `Unreal MCP`를 프로젝트에 Editor 전용으로 연결했다. 전체 `AllToolsets` 대신 Editor·Automation·UMG·StateTree·AI Toolset만 선택했고, Codex 프로젝트 설정과 자동 시작 기본값을 추가했다. 연결 당시 실제 HTTP MCP 초기화, 23개 Toolset, Training Map 조회와 당시 12개 Drone 테스트 탐색까지 통과했다. 상세 기준은 [`docs/DRONE_UNREAL_MCP.md`](docs/DRONE_UNREAL_MCP.md)를 따른다.

```text
PFN-06 Camera/Input 기준선 Done
→ HUD-01 Telemetry Done
→ HUD-02 Flight HUD Done
→ TUT-01 Training Course/Spline Done
→ TUT-02 Gate·순서·정방향 Done
→ TUT-03 Segment/Lap 기록 Done
→ TUT-04B 비교·결과 UI 기술 구현 Done · 실제 두 Lap 확인 대기
→ FLOW-01 상태·Mission/Drone 데이터 계약 Done
→ FLOW-02 정적 시작 화면·로비 Host Done
→ FLOW-03 미션 선택·측면 설명·하단 시작 Done
→ FLOW-04 미션 트레일러·Map 로드 Next
→ FLOW-05~06 Drone 선택·Mission 목표 UI
→ Flight 상태·Jamming·결과
→ AI/MG와 에셋 통합
```

## 2026-08-26 자산 작업 메모

`NavigationArrows` 원본 11개를 UE 5.8에서 감사해 기능에 필요한 6개만 `/Game/Drone/ThirdParty/NavigationArrows`로 이식했다. Commit `5a052c8`을 기능 Branch에 Push한 뒤 Merge Commit `fb1d7ad`로 `origin/main`에도 반영했다. 병합된 `main`에서 Build, 전용 자동화 1/1, 전체 `Drone.` 15/15, Blueprint Compile 0/0/0과 LFS 검증을 다시 통과했다. 자산 인수와 main 공유는 완료했지만 Training Map/HUD의 실제 Host/Wrapper 화면 연결은 아직 하지 않았다. 상세 내용은 [`docs/DRONE_ASSET_INTAKE_2026-08-25.md`](docs/DRONE_ASSET_INTAKE_2026-08-25.md)를 따른다.

프로젝트 사용 맵은 `/Game/Drone/Maps`로 중앙화했다. Unreal 생성 기본 Map 4개만 제거했고 ThirdPerson·Variant 비맵 콘텐츠 62개는 복구했다. 환경 맵 3종은 중앙 사본으로 두되 대형 공급사 의존성 Root는 참조 안정성을 위해 보존했다. RabbitHole 참고 근거, 현재 폴더 트리, 삭제 경계와 검증 결과는 [`docs/DRONE_CONTENT_FOLDER_GUIDE.md`](docs/DRONE_CONTENT_FOLDER_GUIDE.md)에 정리했다.
