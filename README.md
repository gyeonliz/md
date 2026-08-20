# Unreal · Git · Codex 작업 공유 저장소

이 폴더는 실제 Unreal 프로젝트가 아니라 다음 작업을 준비하고 PC 간 문맥을 이어가기 위한 문서·템플릿·도구 저장소다. GitHub `gyeonliz/md`를 이 폴더의 공유 원격으로 사용하고, 실제 Unreal 프로젝트는 별도 `gyeonliz/drone` 저장소로 관리한다.

## 먼저 읽을 파일

1. [`CONTEXT.md`](CONTEXT.md): 사용자가 제공한 확정 기준과 미정 사항
2. [`STATUS.md`](STATUS.md): 현재 작업컴에서 실제 확인한 환경과 남은 선택
3. [`WORKBOARD.md`](WORKBOARD.md): 실제 확인 결과를 반영한 현재 보드
4. [`docs/GIT_UNREAL_GUIDE.md`](docs/GIT_UNREAL_GUIDE.md): Unreal 프로젝트 Git/GitHub 실전 절차
5. [`docs/CODEX_CONTEXT_SYNC.md`](docs/CODEX_CONTEXT_SYNC.md): 메인컴 ↔ 작업컴 문맥 전달 절차
6. [`docs/DRONE_PROJECT_AUDIT.md`](docs/DRONE_PROJECT_AUDIT.md): 현재 후보 프로젝트의 실제 C++·입력·맵 구조 감사
7. [`docs/DRONE_PROTOTYPE_IMPLEMENTATION.md`](docs/DRONE_PROTOTYPE_IMPLEMENTATION.md): 실제 C++ Prototype 구현·검증과 Editor 연결 절차
8. [`docs/DRONE_PROTOTYPE_INPUT_CONTRACT.md`](docs/DRONE_PROTOTYPE_INPUT_CONTRACT.md): 현재 Prototype 전용 임시 입력 계약
9. [`docs/DRONE_PROTOTYPE_PIE_CHECKLIST.md`](docs/DRONE_PROTOTYPE_PIE_CHECKLIST.md): PFN-06 부분 결과와 다음 3회 전체 체크리스트
10. [`docs/DRONE_PREASSET_FUNCTION_PLAN.md`](docs/DRONE_PREASSET_FUNCTION_PLAN.md): 구매 소스 없이 Greybox 기능을 먼저 완성하는 실행 계획
11. [`docs/DRONE_MVP_GUIDE.md`](docs/DRONE_MVP_GUIDE.md): Flight MVP부터 데모까지의 개발 단위
12. [`docs/WORK_MANAGEMENT.md`](docs/WORK_MANAGEMENT.md): Inbox → Todo → Doing → Done 운영
13. [`docs/STUDY_PLANS.md`](docs/STUDY_PLANS.md): 정보처리산업기사·C++ 코딩테스트 병행 계획

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

`C:\project\Drone`에 Git/LFS와 Unreal 무시 규칙을 적용했고, Android를 사용하지 않는다는 결정을 반영해 Android File Server를 껐다. 별도 `ADronePrototypePawn`과 GameMode를 구현해 UE 5.8.1 빌드, 기본값 테스트, Spawn/Possess 테스트와 헤드리스 실행을 통과했다. 이어서 Prototype 전용 Input Action 4개, IMC, BP Pawn/GameMode와 별도 Greybox Map을 생성·연결했다.

GUI PIE에서 IMC 한 개와 Move·Altitude·Yaw·Look Callback 계열의 실제 동작을 부분 확인했다. 하지만 첫 실행은 `S`와 복합·중복 조건을 끝내지 못했고 두 번째도 도중 중단했으므로 PFN-06은 0/3 Pass다. 새 PIE 3회 전체 반복이 남았고 최종 입력 키·감도·Mesh·비행 물리는 계속 미정이다.

Unreal 프로젝트는 `91498b7` (`chore: initialize Drone project`)을 `gyeonliz/drone`의 `origin/main`에 Push했으며 현재 로컬과 원격이 일치한다. 이 문서 저장소는 `gyeonliz/md`를 `origin`으로 연결했지만 아직 첫 Stage·Commit·Push 전이다. 자세한 현재 상태는 [`STATUS.md`](STATUS.md)를 따른다.

외부 구매 소스는 아직 확보되지 않았으므로 현재 개발은 Engine 기본 도형과 기존 Template만 사용하는 기능 우선 Greybox 방식으로 진행한다. 구매 전 실행 순서는 [`DRONE_PREASSET_FUNCTION_PLAN.md`](docs/DRONE_PREASSET_FUNCTION_PLAN.md)를 따른다.
