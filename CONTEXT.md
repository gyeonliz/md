# Drone 작업 기준

이 문서는 다음 작업자가 반드시 지켜야 할 현재 경계만 보존한다. 구현 현황은 [`STATUS.md`](STATUS.md), 실행 순서는 [`WORKBOARD.md`](WORKBOARD.md)를 먼저 확인한다.

## 작업 위치

- Unreal 프로젝트: `D:\JGY\project\drone`
- 문서 저장소: `D:\JGY\project\md`
- 새 생산 코드: `Source/Drone`
- 새 프로젝트 소유 자산: `/Game/Drone`

## 맵 소유권

- `/Game/Drone/Maps/Lvl_DroneTraining`: 팀원이 실제 Tutorial 환경을 제작하는 Production 맵이다. 합의 전 저장·덮어쓰기·자동 재구성·분할·이동을 금지한다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest`: Course, Gate, 역할 기능과 HUD를 자유롭게 검증하는 경량 시험 맵이다.
- `test1`, `test2`: 용도를 확인하기 전 이동하거나 이름을 바꾸지 않는다.
- 자산 이동은 파일 탐색기가 아니라 Unreal AssetTools로 수행하고 Redirector·Soft Reference·하드코딩 경로를 검증한다.

## 게임 흐름

확정 흐름은 `게임 실행 → 시작 트레일러 → 로비 → 미션 선택/설명 → 시작 → 미션 트레일러 → 맵 진입 → 드론 선택 → 미션 시작/목표 UI`다.

사람 Operator 직접 조작, NPC 대화로 임무 수령, 플레이어와 Drone 간 실시간 화면 전환 기획은 폐기했다. NPC·Smart Object·전투 기능은 Mission 내부 요소로 유지한다.

## 구현 책임

- C++: 상태, 규칙, 기능, 테스트와 안정적인 공개 계약
- Blueprint/Data Asset: Mesh·Material·색·속도·거리·시간·임계값·자산 연결과 Greybox 조정
- Collision Root와 Visual Mesh는 분리한다.
- 나중에 조정할 수치는 가능하면 `EditDefaultsOnly` 또는 `EditAnywhere`와 명확한 Category로 Blueprint에 노출한다.
- ThirdPerson·Combat·Platforming·SideScrolling은 Legacy 참고용이며 신규 생산 코드와 자산에서 상속·참조하지 않는다.

## 현재 조작·역할 기준

- 수평 이동은 Actor-relative, 고도는 World Up, Q/E는 Actor Yaw, Mouse는 카메라 회전이다.
- 카메라·Collision은 비행 외형 기울기와 분리한다.
- 역할은 정찰 Scan, FPV Arm/자폭, Payload 픽업·드랍의 프로젝트 소유 기능을 사용한다.
- 현재 속도·감도·Collision·Greybox Mesh는 최종값이 아니다.

## AI·포탑 기준

- NPC가 점유하는 유인 포탑은 `BP_SO_MGTurret` 한 개다.
- `BP_AutoTurret_Vehicle`, `BP_AutoTurret_Emplaced`는 NPC가 잡지 않는 무인 자동포탑이다.
- 유인 MG는 `고정 Base → Yaw Body → Pitch Barrel → Muzzle` 구조이며 사수 Anchor는 Yaw Body의 자식으로 후방 위치와 회전을 따른다.
- Smart Object 동선은 번호나 Spline 고정 순서가 아니라 태그가 맞는 최근접 빈 Slot 선택이다.

## Git·LFS 기준

- 실제 Git 상태, 코드, 자산과 실행 로그를 문서보다 우선한다.
- 사용자의 변경과 팀원 맵을 임의로 되돌리거나 덮어쓰지 않는다.
- 모든 `.uasset`, `.umap`은 크기와 무관하게 Git LFS로 관리한다.
- LFS 비용 문제를 Threshold 변경으로 일반 Git에 옮기지 않는다. Core와 선택형 Asset Depot 분리를 별도로 검토한다.
- Commit과 Push는 별도 지시가 없으면 사용자가 수행한다.

## 문서 갱신 규칙

- 현재 사실: `STATUS.md`
- 현재와 다음 작업: `WORKBOARD.md`
- 변경 금지 경계: `CONTEXT.md`
- 날짜별 기록: `docs/history/DRONE_WORKLOG.md`
- 상세 주제 문서: `docs/README.md`에서 찾아간다.
- 과거 상세 원문은 `docs/history/snapshots`에 보존하며 현재 기준으로 사용하지 않는다.
