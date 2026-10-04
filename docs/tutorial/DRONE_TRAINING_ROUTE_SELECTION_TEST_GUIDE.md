# Training 4-Route 선택 시험 가이드

기준일: 2026-09-29

## 맵과 목적

- 맵: `/Game/Drone/Maps/TestMap/Lvl_DroneTrainingRouteSelectionTest`
- 직접 Play하는 독립 시험장이다.
- Production `/Game/Drone/Maps/Lvl_DroneTraining`과 기존 Tutorial Mission 맵은 수정하지 않는다.
- Editor에서는 네 Route를 모두 보고 편집할 수 있지만 Play 중에는 활성 Route 하나만 표시되고 Gate 판정도 그 Route만 켜진다.

## Play 입력

| 키 | 동작 |
|---|---|
| `1` | Route 1 직선·완만한 고도 변화 |
| `2` | Route 2 좌측 곡선 |
| `3` | Route 3 우측 곡선 |
| `4` | Route 4 상승·하강 슬라럼 |
| `5` | Route 1~4 중 하나를 무작위 활성화 |

초기 활성 Route는 1이다. Route가 둘 이상이면 `5`는 현재 Route를 즉시 다시 선택하지 않아 화면에서 전환 여부를 확인할 수 있다. 화면 상단에 현재 활성 Route와 입력 안내가 표시된다.

Route를 바꾸면 이전 Route의 Gate Sequence와 진행 중 Lap을 초기화한다. Flight HUD의 구간 기록 Source도 새 활성 Route로 교체된다.

## Route 편집

World Outliner에서 다음 Actor 중 하나를 선택한다.

- `TrainingRouteSelectionTest_Route01_Straight`
- `TrainingRouteSelectionTest_Route02_LeftCurve`
- `TrainingRouteSelectionTest_Route03_RightCurve`
- `TrainingRouteSelectionTest_Route04_ClimbSlalom`

`CourseSpline` Component를 선택한 뒤 Viewport에서 점과 Tangent를 이동한다. Spline 점 추가는 기존 점을 `Alt+Drag`하거나 Spline Segment를 우클릭해 `Add Spline Point Here`를 사용한다. 각 Route의 Gate는 현재 Spline을 따라 5개가 자동 배치된다.

숫자키 순서는 `TrainingRouteSelectionTest_Selector` Actor의 `Routes` 배열 순서가 기준이다. `Initial Route Number`, `Random Seed`, `Avoid Immediate Random Repeat`도 같은 Actor의 Details에서 조정할 수 있다.

## 수동 확인

1. 맵을 열고 Play한다.
2. 처음에는 Route 1만 보이는지 확인한다.
3. `2`, `3`, `4`, `1`을 차례로 눌러 해당 Route 하나만 표시되는지 확인한다.
4. 각 Route에서 첫 Gate만 현재 색이고 나머지는 대기 색인지 확인한다.
5. Gate를 한두 개 통과한 뒤 다른 숫자를 눌러 이전 진행이 초기화되는지 확인한다.
6. `5`를 여러 번 눌러 항상 하나의 Route만 활성화되고 현재 Route와 다른 번호로 전환되는지 확인한다.
7. 활성 Route를 비행할 때 HUD 구간 기록이 해당 Route Gate 기준으로 갱신되는지 확인한다.

## 자동 검증·재생성

- `Drone.Tutorial.TrainingRouteSelector`: 고정·무작위 선택과 단일 활성 계약
- `Drone.Tutorial.TrainingRouteSelectionTestMap`: 맵, Route 4개, 고유 Course ID, Gate 5개 계약
- `Drone.Tutorial.TrainingRouteSelectionPIE`: 실제 `1~5` 키 입력과 HUD Source 전환

```powershell
cd C:\URproject\drone # 현재 C PC 예시; 다른 PC는 실제 Unreal 저장소 경로로 바꿀 것
.\Tools\AssetMigration\Invoke-DroneTrainingRouteSelectionTestMap.ps1 -Mode Validate
```

Route 좌표를 수동 조정한 뒤에는 `Validate`만 사용한다. `Rebuild`는 도구 소유 Actor를 기본 좌표로 다시 만들므로 의도적으로 초기화할 때만 실행한다.

