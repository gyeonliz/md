# Drone 작업 보드

마지막 갱신: 2026-09-15 — 문서 구조 정리 및 Push 이후 Git 상태 반영

## Now

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| MAP-TEST-01 | 경량 Tutorial Systems TestMap 수동 확인 | 맵·생성 도구·전용 자동화·Map Check 완료 | Gate/Ring/역할/HUD 한·두 Lap 화면 확인 |
| AI-SO-TUNE-01 | Smart Object·유인 MG 화면 확인 | 재점유와 도착 안정화 코드·자동화 완료 | AI 시험 맵에서 방향·정렬·Gaze·재점유 확인 |

### 사용자가 지금 확인할 맵

`/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest`

1. 4변 Gate Frame이 네모 Trigger 안쪽을 깔끔하게 따르는지 본다.
2. `통과 전 / 현재 목표 / 통과 후` 색이 순서대로 바뀌는지 본다.
3. Ring Handle 하나를 움직여 CourseSpline 자체는 변하지 않고 Ring만 가장 가까운 Spline 위치를 따르는지 본다.
4. Recon·Impact·Payload 표적과 Carryable이 보이고 깨진 긴 World Text가 없는지 본다.
5. 한 Lap에서 현재 속도·고도·구간 시간·평균값이 갱신되는지 본다.
6. 두 번째 Lap에서 이전 평균·Best·빠름/느림 증감 부호가 맞는지 본다.
7. 종료 후 Editor가 정상 복귀하는지 확인한다.

Production `/Game/Drone/Maps/Lvl_DroneTraining`에서는 위 시험을 위해 Actor를 추가하거나 저장하지 않는다.

## Next

1. 수동 확인에서 발견된 Gate/HUD/역할 결함 수정 후 TestMap 회귀
2. `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`에서 MG 재점유·Smart Object 방향·NPC Gaze·무인 포탑 확인
3. 소유권과 참조를 감사한 기존 시험 맵만 Unreal AssetTools로 `/Game/Drone/Maps/TestMap` 아래 이동
4. Mission Definition에 목표 종류·필요 수량·제한 시간·대상 ID Rule 추가
5. 정찰·투하·파괴·귀환 Event를 공통 Objective 진행도와 Mission HUD에 연결
6. Jamming 감지 범위·신호 단계·HUD 경고·조작/영상 방해·회복 조건 Vertical Slice

## 이동 후보 맵

| 맵 | 처리 |
|---|---|
| `Lvl_DronePrototype` | 참조 감사 후 TestMap으로 이동 |
| `Lvl_NPCSmartObjectGreybox` | AI 수동 확인 후 이동 |
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

세부 구현 순서는 [`docs/planning/DRONE_TUTORIAL_STORY_PLAN.md`](docs/planning/DRONE_TUTORIAL_STORY_PLAN.md), 날짜별 이력은 [`docs/history/DRONE_WORKLOG.md`](docs/history/DRONE_WORKLOG.md)를 참고한다.
