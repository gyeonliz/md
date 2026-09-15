# Drone 프로젝트 문서

이 저장소는 `D:\JGY\project\drone` Unreal 프로젝트의 기획, 현재 상태, 작업 순서와 팀 가이드를 관리한다.

## 먼저 볼 문서

| 문서 | 용도 |
|---|---|
| [`STATUS.md`](STATUS.md) | 지금 실제로 확인된 구현·Git·검증 상태 |
| [`WORKBOARD.md`](WORKBOARD.md) | 현재 작업, 사용자 확인 항목, 바로 다음 개발 |
| [`CONTEXT.md`](CONTEXT.md) | 경로·맵 소유권·코드/Blueprint 책임 등 변경 금지 기준 |
| [`docs/README.md`](docs/README.md) | 주제별 상세 문서 찾기 |
| [`docs/history/DRONE_WORKLOG.md`](docs/history/DRONE_WORKLOG.md) | 날짜별 작업과 검증 이력 |

현재 판단은 위 순서대로 우선한다. 오래된 문서 안의 `현재`, Commit ID, Todo는 당시 기록이며 최신 상태를 뜻하지 않는다.

## 저장소

- Unreal: `D:\JGY\project\drone`
- 문서: `D:\JGY\project\md`
- Production 코드: `Source/Drone`
- 프로젝트 소유 자산: `/Game/Drone`
- 팀원 Tutorial 맵: `/Game/Drone/Maps/Lvl_DroneTraining`
- 기능 시험 맵: `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest`

## 문서 관리 규칙

- 진행 상황은 새 파일을 만들지 않고 `STATUS.md`, `WORKBOARD.md`, `DRONE_WORKLOG.md`에 반영한다.
- 기능 설명이 장기적으로 반복 사용될 때만 주제별 상세 문서를 추가한다.
- 완료된 일회성 보고서는 `docs/history`로 옮긴다.
- 상세 문서와 현재 상태가 충돌하면 실제 Git·코드·실행 로그와 `STATUS.md`를 우선한다.
- 문서 변경의 Commit과 Push는 별도 사용자 지시가 없으면 사용자가 처리한다.
