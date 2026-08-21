# Drone 개발 진행 기록

기준일: 2026-08-21 (Asia/Seoul)

이 문서는 Drone 개발의 **진행 이력**을 시간순으로 남긴다. 가장 최신의 현재 상태는 [`../WORKBOARD.md`](../WORKBOARD.md), 확정 구현 순서는 [`DRONE_TUTORIAL_STORY_PLAN.md`](DRONE_TUTORIAL_STORY_PLAN.md)를 따른다.

## 갱신 규칙

Drone 코드·자산·계획 작업을 진행할 때마다 작업 종료 전에 Markdown을 함께 갱신한다.

1. `WORKBOARD.md`: 현재 단계, 지금 작업 중인 카드, 완료 근거, 남은 조건과 바로 다음 작업
2. `DRONE_WORKLOG.md`: 실제 변경, 검증 결과, 발견한 문제와 다음 행동을 날짜순으로 추가
3. `STATUS.md`: 빌드·테스트·자산 수처럼 검증된 기준선이 달라졌을 때 갱신
4. `CONTEXT.md`: 사용자가 확정한 방향, 장기 규칙과 범위가 달라졌을 때 갱신
5. 계획 문서: 구현 순서, 완료 조건이나 설계가 달라졌을 때 같은 작업에서 갱신

진행률은 근거 없는 전체 백분율로 표시하지 않는다. 대신 `현재 단계`, `통과한 게이트/전체 게이트`, `Doing`, `다음 활성 카드`로 기록한다. 자동화가 통과해도 필수 수동 확인이 남아 있으면 완료로 이동하지 않는다.

## 현재 스냅샷

마지막 갱신: 2026-08-21 11:55 KST

| 구분 | 현재 상태 |
|---|---|
| 전체 단계 | 1단계 Camera·Input 기준선 완료, 2단계 Telemetry/HUD 준비 |
| PFN-06 진행도 | 필수 게이트 5/5 Pass, Done |
| 지금 작업 중 | PFN-06 마감 완료, `HUD-01` 구현 시작 대기 |
| 차단 조건 | 없음. 실제 Gamepad 체감은 미확인으로 별도 보존 |
| 다음 행동 | `HUD-01` Telemetry C++ 설계·테스트 시작 |
| 다음 기능 | `HUD-01` Telemetry Snapshot → `HUD-02` 공용 Flight HUD |
| 이후 | Tutorial Spline·Ring Gate·Lap/Segment 기록 → Flight 상태 → Operator↔Drone → Story/NPC/Mission/Jamming |

## 2026-08-21 — Camera·Mouse·Gamepad 기준선 갱신

### 실제 변경

- SpringArm을 Controller 자유 회전에서 Drone Yaw를 따르는 고정 추적 Camera로 변경
- Mouse X를 Drone Actor Yaw, Mouse Y를 CameraBoom Pitch로 분리
- Gamepad Left Stick 이동, `RT/LT` 고도, Right Stick X Yaw, Right Stick Y Camera Pitch 추가
- Input Action을 5개, IMC Mapping을 15개로 확장
- PIE lifecycle 테스트를 Keyboard·Mouse·Gamepad와 복합·반대 입력까지 확장
- Tutorial·Story 공통 구조와 실행 순서를 `DRONE_TUTORIAL_STORY_PLAN.md`로 확정

### 검증 결과

- `DroneEditor Win64 Development` 빌드 성공
- Blueprint 전체 Compile: 0 errors, 0 warnings
- `PawnDefaults`, `PIEInputLifecycle`, `SpawnPossess`: 3 succeeded, 0 failed
- 새 PIE 3회에서 입력과 IMC 중복 없음 확인
- Prototype 자산 9개, Input Action 5개, Mapping 15개 확인
- `/Game/Drone`에서 동결한 Legacy 자산으로 향하는 의존성 0개
- 기존 ThirdPerson 기본 Map 로드 유지
- 두 저장소 `git diff --check` 통과

### 남은 작업

- 사용자 수동 확인으로 Camera·Keyboard·Mouse 조작 수정이 정상임을 확인함
- 실제 Gamepad가 연결되어 있으면 Stick·Trigger 체감 확인하고, 없으면 `미확인`으로 기록
- 창 닫기 뒤 `Win RequestExit`, `Game engine shut down`, `Exiting` 로그와 프로세스 종료를 확인함
- PFN-06을 Done으로 판정

### 다음 구현

PFN-06 통과 후 `HUD-01`을 시작한다. Drone Telemetry를 10Hz Snapshot으로 제공하고 속도·고도·수직 속도·Heading을 공용 HUD에 표시한다.

### 수동 판정 마감

- 사용자 보고: 조작 수정 정상
- 종료 방식: `Esc`가 아닌 창 닫기
- 로그 판정: 정상 종료, Fatal·Assertion 없음
- Gamepad 체감: 연결 여부 미보고로 미확인
- 최종 판정: PFN-06 Done, `HUD-01` Ready
- Unreal 로컬 Commit: `2c38ebf` (`feat: finalize prototype camera and input lifecycle`)
- 원격 Push: 수행하지 않음
