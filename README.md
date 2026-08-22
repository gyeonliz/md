# Unreal · Git · Codex 작업 공유 저장소

이 폴더는 실제 Unreal 프로젝트가 아니라 다음 작업을 준비하고 PC 간 문맥을 이어가기 위한 문서·템플릿·도구 저장소다. GitHub `gyeonliz/md`를 이 폴더의 공유 원격으로 사용하고, 실제 Unreal 프로젝트는 별도 `gyeonliz/drone` 저장소로 관리한다.

## 먼저 읽을 파일

1. [`CONTEXT.md`](CONTEXT.md): 사용자가 제공한 확정 기준과 미정 사항
2. [`STATUS.md`](STATUS.md): 현재 작업컴에서 실제 확인한 환경과 남은 선택
3. [`WORKBOARD.md`](WORKBOARD.md): 실제 확인 결과를 반영한 현재 보드
4. [`docs/DRONE_WORKLOG.md`](docs/DRONE_WORKLOG.md): 현재 작업 위치와 날짜별 변경·검증·다음 작업 기록
5. [`docs/GIT_UNREAL_GUIDE.md`](docs/GIT_UNREAL_GUIDE.md): Unreal 프로젝트 Git/GitHub 실전 절차
6. [`docs/CODEX_CONTEXT_SYNC.md`](docs/CODEX_CONTEXT_SYNC.md): 메인컴 ↔ 작업컴 문맥 전달 절차
7. [`docs/DRONE_PROJECT_AUDIT.md`](docs/DRONE_PROJECT_AUDIT.md): 현재 후보 프로젝트의 실제 C++·입력·맵 구조 감사
8. [`docs/DRONE_PROTOTYPE_IMPLEMENTATION.md`](docs/DRONE_PROTOTYPE_IMPLEMENTATION.md): 실제 C++ Prototype 구현·검증과 Editor 연결 절차
9. [`docs/DRONE_PROTOTYPE_INPUT_CONTRACT.md`](docs/DRONE_PROTOTYPE_INPUT_CONTRACT.md): 현재 Prototype 전용 임시 입력 계약
10. [`docs/DRONE_PROTOTYPE_PIE_CHECKLIST.md`](docs/DRONE_PROTOTYPE_PIE_CHECKLIST.md): PFN-06 자동화 결과와 수동 화면 체크리스트
11. [`docs/DRONE_TELEMETRY_IMPLEMENTATION.md`](docs/DRONE_TELEMETRY_IMPLEMENTATION.md): HUD-01 Snapshot 공급과 HUD-02 Flight HUD 구현·검증
12. [`docs/DRONE_PREASSET_FUNCTION_PLAN.md`](docs/DRONE_PREASSET_FUNCTION_PLAN.md): 구매 소스 없이 Greybox 기능을 먼저 완성하는 실행 계획
13. [`docs/DRONE_MVP_GUIDE.md`](docs/DRONE_MVP_GUIDE.md): Flight MVP부터 데모까지의 개발 단위
14. [`docs/WORK_MANAGEMENT.md`](docs/WORK_MANAGEMENT.md): Inbox → Todo → Doing → Done 운영
15. [`docs/DRONE_TUTORIAL_STORY_PLAN.md`](docs/DRONE_TUTORIAL_STORY_PLAN.md): 확정 조작, Tutorial 코스·기록 UI, Story·NPC·Jamming·에셋 적용 계획
16. [`docs/STUDY_PLANS.md`](docs/STUDY_PLANS.md): 정보처리산업기사·C++ 코딩테스트 병행 계획

## 구성

```text
CONTEXT.md                 기준 컨텍스트
STATUS.md                  작업컴 점검 결과와 다음 결정
WORKBOARD.md               현재 Inbox/Todo/Doing/Done
docs/                      실행 가이드와 계획
templates/unreal/          Unreal 프로젝트 루트용 Git 템플릿
tools/context-sync/        검토 가능한 작업 문맥 Export/Import 도구
tools/unreal/              Prototype 자산 생성·재검증용 안전 실행 도구
```

## 중요한 경계

- Unreal 프로젝트 파일은 `gyeonliz/drone` Git/GitHub 저장소로 전달한다.
- 검토 가능한 Markdown 작업 문맥·계획·가이드는 `gyeonliz/md` 저장소로 전달한다.
- 특정 시점의 단일 인계본이 필요하면 사람이 읽을 수 있는 별도 handoff 패키지를 보조 수단으로 사용한다.
- `.codex` 전체, `auth.json`, 토큰, 비밀번호, 브라우저 프로필, 원시 세션 DB는 이 방식으로 복사하지 않는다.
- `templates/unreal`의 파일은 실제 프로젝트의 기존 규칙을 확인한 뒤 병합한다. 기존 파일을 무조건 덮어쓰지 않는다.

## 현재 진행 지점

작업컴 기본 작업 루트는 `D:\JGY\project`이고, 이번 HUD-02를 구현·검증한 현재 PC의 Unreal 저장소는 `C:\URproject\drone`이다. 별도 `ADronePrototypePawn`과 GameMode, 5개 Input Action, Keyboard·Mouse·Gamepad 15개 Mapping, BP Pawn/GameMode와 Greybox Map을 연결했다. Camera는 Drone 뒤 고정 추적, Mouse X는 Drone Yaw, Mouse Y는 Camera Pitch로 동작한다.

확정 조작을 반영한 PFN-06은 자동화와 Standalone 수동 조작을 통과해 Done이다. HUD-01 공용 Telemetry Component는 기본 10Hz Snapshot Event를 제공한다. HUD-02는 C++가 계산·생성·Possession·Delegate 수명주기를 맡고 실제 `WBP_DroneFlightHUD`가 배치·색·폰트 같은 화면 외형을 맡도록 연결했다. BP PlayerController와 BP GameMode 연결, native 직접 실행용 fallback, 자동화 7/7, Blueprint 0/0과 Standalone WBP 표시를 검증했다. 다음 구현은 `Tutorial Course/기록 → Flight 상태 → Operator↔Drone → Story/NPC/Mission/Jamming` 순서이며 [`DRONE_TUTORIAL_STORY_PLAN.md`](docs/DRONE_TUTORIAL_STORY_PLAN.md)를 우선 기준으로 한다.

2026-08-23 기준 Unreal 저장소 로컬 `main`과 `origin/main`은 WBP/BP 연결 보강 Commit `9f91bb6`으로 일치한다. 문서 저장소는 이번 갱신 직전 `origin/main=7e3a9ec`이었으며 이번 문서 갱신도 Commit·Push해 공유한다. `410c940`은 native HUD 기준선, `91498b7`은 Unreal 저장소의 초기 Commit이다. 자세한 현재 상태는 [`STATUS.md`](STATUS.md)를 따른다.

외부 구매 소스는 아직 확보되지 않았으므로 현재 개발은 Engine 기본 도형과 기존 Template만 사용하는 기능 우선 Greybox 방식으로 진행한다. 현재 실행 순서는 [`DRONE_TUTORIAL_STORY_PLAN.md`](docs/DRONE_TUTORIAL_STORY_PLAN.md)가 우선하고 PFN 카드 번호와 교체 경계는 [`DRONE_PREASSET_FUNCTION_PLAN.md`](docs/DRONE_PREASSET_FUNCTION_PLAN.md)를 함께 따른다.

```text
PFN-06 Camera/Input 기준선 Done
→ HUD-01 Telemetry Done
→ HUD-02 Flight HUD Done
→ Tutorial Course/Gate/Lap 기록
→ Flight 상태
→ Operator↔Drone
→ Story/NPC/Mission/Jamming
→ AI/MG와 에셋 통합
```
