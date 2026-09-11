# Drone Training 게이트·루트 배치 가이드

기준일: 2026-09-11 (Asia/Seoul)

이 문서는 `D:\JGY\project\drone`의 현재 구현과 `/Game/Drone/Maps/Lvl_DroneTraining` 저장 상태를 기준으로 한다. 코스 제작은 `BP_DroneTrainingCourse` 한 개에서 관리한다. 권장 자동 편집 방식은 `Spline Point 1개당 Ring 1개`이며, 각 Point의 배열 순서가 곧 Gate 통과 순서다. 생성된 빛나는 선 Component, 자동 Gate Child Actor와 GateIndex를 직접 관리하지 않는다.

## 1. 현재 맵과 자산 위치

```text
/Game/Drone/Maps/Lvl_DroneTraining
/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingCourse
/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingGate
/Game/Drone/Tutorial/Materials/M_DroneTrainingGuide
```

현재 `3df654a` Pull 기준 맵 감사 결과는 Gate Actor 17개, Course Sequence 4개, 역할 표적 3종과 Carryable Payload 0개다. 이 맵은 원격 LFS 파일과 같은 Clean 상태라 이번 코드 작업에서 저장하거나 덮어쓰지 않았다. 17개 링의 의도와 배치 위치를 화면에서 확인한 뒤 Point 직접 편집 방식으로 변환해야 한다.

## 2. 루트 만들기와 Spline 점 추가

1. `Lvl_DroneTraining`을 열고 World Outliner에서 `BP_DroneTrainingCourse`를 선택한다.
2. Components에서 `CourseSpline`을 선택한다.
3. Viewport의 Spline 위 원하는 위치를 우클릭하고 `Add Spline Point Here`를 선택한다.
4. 새 점을 이동·회전하고, Point Type을 `Curve` 또는 급격한 꺾임을 줄이는 `Curve Clamped`로 둔다.
5. 점의 Tangent Handle을 드래그해 진입·이탈 곡률을 조정한다. 점 위치만 옮기고 Tangent가 너무 짧으면 S자 구간도 급하게 꺾여 보일 수 있다.
6. 닫힌 순환 코스가 필요하지 않으면 `Closed Loop`를 켜지 않는다. 현재 기록 규칙은 열린 코스의 Gate 0에서 시작해 마지막 Gate에서 끝난다.
7. 맵을 저장하기 전에 코스 Actor의 `Synchronize Gate Definitions` 버튼을 한 번 실행하고 BP·Map을 저장한다. Construction과 BeginPlay에서도 같은 동기화가 자동 실행된다.

`Spline Point 1개당 Ring 1개`를 켠 상태에서는 제어점 수와 Ring 수가 항상 같다. Point를 움직이면 같은 Index의 Ring이 움직이고, Point를 추가·삭제하면 Ring도 하나씩 추가·삭제된다. 숫자 배치 모드나 수동 `OrderedGates` 모드에서만 Spline 제어점 수와 Gate 수를 다르게 운용한다.

## 3. 빛나는 코스가 각져 보였던 이유와 현재 규칙

기존 구현은 Spline 제어점 한 쌍마다 긴 Cube Spline Mesh 한 개만 만들었다. Spline 자체가 Curve여도 제어점 사이가 길면 화면의 단면·Tangent 보간이 거칠게 보여 빛나는 선이 꺾인 것처럼 보일 수 있었다.

현재는 전체 Spline을 거리 기준으로 다시 샘플링한다.

```text
기본 목표 길이      CourseLineSegmentLengthCentimeters = 200 cm
생성 Segment 수    ceil(Spline 전체 길이 / 목표 길이)
안전 상한           256개
현재 64.9 m 코스    33개 생성 예상
```

각 구간은 시작·끝 위치뿐 아니라 해당 거리의 Spline 방향으로 Tangent를 계산하고 Smooth Interpolation을 사용한다. 따라서 제어점 6개 사이를 5개의 긴 조각으로 그리지 않고 약 2 m 단위의 33개 조각으로 이어 곡선을 더 매끄럽게 표시한다.

선이 여전히 거칠면 Course의 `Course Line Segment Length Centimeters`를 `100~150 cm`로 낮춘다. 값이 작을수록 부드럽지만 Component와 렌더 비용이 늘어난다. 생성된 `CourseLineSegment_*`는 Construction 때 지워지고 다시 만들어지므로 직접 이동·복제·저장하지 않는다.

## 4. 자동 Spline Ring Gate 배치

`BP_DroneTrainingCourse`를 선택하고 Details의 `Tutorial > Course > Automatic Gates`에서 다음 값을 조정한다.

| 항목 | 역할 |
|---|---|
| `Use Automatic Spline Gates` | 자동 Ring 생성 사용 여부 |
| `Spline Point 1개당 Ring 1개` | 권장 직접 편집 모드. Point 이동·추가·삭제가 같은 Index Ring에 반영 |
| `Automatic Gate Count` | Point 직접 편집 모드를 끈 경우의 Ring 수, 최소 2개·최대 64개 |
| `Automatic Gate Class` | 기본 Native Gate 또는 외형을 가진 `BP_DroneTrainingGate` |
| `Evenly Distribute Automatic Gates` | 켜면 시작 거리~끝 여백 사이 균등 분배 |
| `Automatic Gate Start Distance Centimeters` | 첫 Ring을 Spline 시작점에서 띄우는 거리 |
| `Automatic Gate End Padding Centimeters` | 균등 배치 시 마지막 Ring과 Spline 끝의 여백 |
| `Automatic Gate Spacing Centimeters` | 균등 배치를 끈 경우 Ring 사이 고정 거리 |
| `Automatic Gate Distance Offset Centimeters` | 모든 Ring을 Spline 앞/뒤로 함께 이동 |
| `Automatic Gate Distance Offsets Centimeters` | 배열 Index별 추가 앞/뒤 이동 |
| `Automatic Gate Spline Distances Centimeters` | 배열 Index별 Spline 시작점 기준 절대 거리. 각 Ring 간격을 직접 지정할 때 사용 |
| `Automatic Gate Local Offset` | Spline 접선 기준 좌우·상하 위치 보정 |
| `Automatic Gate Local Offsets` | 배열 Index별 개별 위치 보정. X는 진행방향, Y는 좌우, Z는 높이 |
| `Automatic Gate Rotation Offset` | Spline 접선 회전에 더할 회전 보정 |
| `Automatic Gate Scale` | 생성 Ring 전체 크기 보정 |

값이나 Spline 점을 바꾸면 Construction에서 Ring을 다시 만들고 스플라인 위치·접선 회전을 따라 자동 정렬한다. 즉시 갱신이 필요하면 Details의 `Rebuild Automatic Gates`를 누른다.

### 권장: 링 하나씩 화면에서 직접 배치

1. Course에서 `Use Automatic Spline Gates`와 `Spline Point 1개당 Ring 1개`를 켠다.
2. Components에서 `CourseSpline`을 선택한다.
3. Viewport에서 Point 0, 1, 2…를 각각 링을 놓을 위치로 이동한다. 링은 해당 Point 위치와 Spline 접선 회전을 따른다.
4. 링이 더 필요하면 Spline 위를 우클릭해 `Add Spline Point Here`를 사용한다. 새 Point와 새 Ring이 같은 Index에 생긴다.
5. 링을 없애려면 해당 Spline Point를 선택해 삭제한다. 시작·종료 판정을 위해 Point는 최소 2개를 유지한다.
6. 위치를 조정한 뒤 `Rebuild Automatic Gates`를 누르고 Ring 수와 순서를 확인한다.

생성된 `AutomaticSplineGate_*`를 직접 드래그하면 다음 Construction 때 위치가 다시 계산된다. 반드시 `CourseSpline` Point를 잡아 움직인다. `Automatic Gate Distance Offset(s)`와 `Automatic Gate Local Offset(s)`은 Point 위치를 바꾸지 않고 앞뒤·좌우·높이를 미세 보정할 때만 사용한다.

자동 Gate의 순서는 Spline 거리 증가 방향이며 Actor 로컬 `+X`가 해당 지점의 Spline 진행 방향을 따른다. `GateIndex`, `CourseId`, `SegmentDistance`와 Sequence 배열은 자동 동기화된다. 생성된 `AutomaticSplineGate_*` Component나 그 Child Actor를 Outliner에서 직접 옮기지 않는다.

권장 시작값:

```text
Use Automatic Spline Gates = true
Spline Point 1개당 Ring 1개 = true
Automatic Gate Class = BP_DroneTrainingGate
```

기존 숫자 배치가 필요한 경우에만 `Spline Point 1개당 Ring 1개`를 끄고 `Automatic Gate Count`, 균등 분배 또는 절대 거리 배열을 사용한다. 프로젝트 재설정 도구 `Tools/AssetMigration/ConfigureAutomaticTrainingGates.py`의 설정 실행은 사용자 배치를 기본 4개 숫자 배치로 되돌릴 수 있으므로 현재 맵에는 실행하지 않고 검증 모드만 사용한다.

Ring 사이 간격을 완전히 직접 지정하려면 `Automatic Gate Spline Distances Centimeters` 배열을 Ring 수만큼 만든다. 예를 들어 `500, 1300, 2600, 4100`은 Spline 시작점에서 각각 5m, 13m, 26m, 41m 지점에 Ring 0~3을 둔다. 배열 값은 통과 순서대로 증가시키는 것이 권장되며, 항목이 없거나 음수인 Index는 균등/고정 간격 계산값을 사용한다.

기본 거리에서 조금씩만 움직이려면 기존 `Automatic Gate Distance Offsets Centimeters`를 사용한다. 절대 거리 배열과 같이 쓰면 `절대 거리 + 공통 거리 Offset + Index별 거리 Offset` 순서로 계산된다.

각 Ring의 좌우·높이를 따로 바꾸려면 `Automatic Gate Local Offsets`를 Ring 수만큼 만든다. `X`는 Spline 진행 방향, `Y`는 좌우, `Z`는 위아래이며 공통 `Automatic Gate Local Offset`에 더해진다. 예를 들어 Ring 1만 오른쪽 100cm·위 50cm 옮기려면 Index 1을 `(X=0, Y=100, Z=50)`으로 둔다. 배열이 짧으면 없는 Index는 `(0,0,0)`을 사용한다.

### Gate 3상태 색상 바꾸기

1. `/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingGate`를 연다.
2. `Class Defaults`에서 `Tutorial > Gate > Visual`을 연다.
3. `통과 전 색상`, `현재 목표 색상`, `통과 후 색상`을 각각 지정한다.
4. Compile·Save 후 Training Map으로 돌아오면 자동 생성 Ring 전체에 같은 상태 색 규칙이 적용된다.

상태 의미는 다음과 같다.

- `통과 전 색상`: 아직 차례가 오지 않은 Ring
- `현재 목표 색상`: 지금 통과해야 하는 Ring 한 개
- `통과 후 색상`: 정상 통과를 마친 Ring

미션이나 Blueprint 연출 중 색을 바꾸려면 Gate 참조에서 `Set Gate State Colors`를 호출한다. 입력 순서는 `Before Pass`, `Current Target`, `After Pass`이며 호출 즉시 현재 상태 Material에도 반영된다.

## 5. 수동 Gate 설치와 순서 지정

1. Content Browser에서 `BP_DroneTrainingGate`를 맵으로 끌어오거나 기존 Gate를 복제한다.
2. Gate 중심을 Spline 위 통과시키고 싶은 위치에 배치한다.
3. Gate Actor의 로컬 `+X` 방향이 드론이 통과할 정방향을 바라보게 회전한다. 링의 모양만 보고 앞뒤를 판단하지 말고 Local 축 표시로 확인한다.
4. Course Actor를 선택하고 Details의 `OrderedGates` 배열에 Gate를 실제 통과 순서대로 넣는다.
5. 배열의 0번이 출발 Gate, 마지막 원소가 종료 Gate다. 배열 중간에 `None`, 중복 Gate 또는 다른 Course의 Gate를 넣지 않는다.
6. `Synchronize Gate Definitions`를 실행한다. `CourseId`와 `GateIndex`는 배열 순서에서 자동 설정되므로 Gate마다 숫자를 손으로 맞추지 않는다.
7. 플레이 전에 Current 색이 Gate 0 하나에만 표시되고 나머지는 Inactive인지 확인한다.

수동 배치를 사용할 때는 `Use Automatic Spline Gates`를 끈다. Gate를 추가했는데 반응하지 않으면 `OrderedGates`에 들어갔는지, 앞 Gate를 먼저 통과했는지, 로컬 `+X` 정방향으로 들어갔는지 확인한다. Gate Visual은 비충돌이고 별도 Trigger만 Pawn Overlap을 판정한다. 빛나는 Spline은 경로 안내 전용이라 Gate 통과 판정을 하지 않는다.

## 6. 루트 수정 권장 순서

1. Point 직접 편집 모드에서는 Ring 위치가 필요한 곳에 Spline Point를 놓고 Tangent로 접근 방향과 곡률을 함께 만든다.
2. 편집 카메라로 빛나는 선이 Spline을 부드럽게 따르는지 확인한다.
3. 권장 자동 모드에서는 Point 수로 Ring 수를 정한다. 숫자 자동 모드는 균등 배치가 필요한 코스에만 쓰고, 수동 모드에서만 Gate Actor와 `OrderedGates`를 직접 구성한다.
4. 자동 Ring이 Spline 접선과 진행 방향을 따르는지 확인한다.
5. `Standalone Game`에서 Gate 0부터 끝까지 한 번 통과한다.
6. 역순, 같은 Gate 재통과, Gate 우회가 기록을 변경하지 않는지 확인한다.
7. HUD의 현재 비행 값과 구간 통계를 확인하고 정상 종료한다.

## 7. 현재 한글 HUD 표기

항상 표시되는 비행 정보:

- `현재 속도`: 드론의 현재 3차원 속도, `km/h`
- `현재 고도`: 현재 고도, `m`
- `수직 속도`: 상승은 `+`, 하강은 `-`, `m/s`
- `진행 방향`: Heading, `도`

Training Course가 있는 맵에서만 표시되는 구간 정보:

- `방금 구간 평균 속도`: 가장 최근 정상 구간의 이동 거리 ÷ 통과 시간, `km/h`
- `방금 구간 이동 거리`: 실제 3차원 이동 거리, `m`
- `방금 구간 통과 시간`: 직전 Gate에서 현재 Gate까지 걸린 시간, `초`
- `완료 구간 평균 속도`: 현재 표시 중인 완료 구간들의 산술 평균, `km/h`
- `완료 구간 평균 거리`: 완료 구간 거리들의 산술 평균, `m`
- `완료 구간 평균 시간`: 완료 구간 시간들의 산술 평균, `초`

첫 Gate를 통과하기 전에는 `기록 준비`, Lap 측정 중에는 `코스 측정 중`, 완료 이력이 있으면 `최근 완료 기록` 상태를 표시한다. 이전 Lap 평균·Best 대비 `+/-` 비교와 영구 저장은 별도 TUT-04 후속 범위이며 이번 표기의 완료 항목으로 과장하지 않는다.

## 8. 저장·검증 체크리스트

- Course 1개, 직접 배치 Prototype Pawn 0개
- 자동 모드의 생성 Ring 수 또는 수동 모드의 `OrderedGates` 수가 의도와 일치
- GateIndex가 저장 후 `0, 1, 2, ...`로 일치
- Current Gate가 0번 하나로 시작
- 생성 코스 선이 긴 직선 조각으로 꺾이지 않고 Spline 곡선을 따름
- 코스 선 Collision·Overlap·Physics·Navigation 영향 없음
- 정방향 순서 통과만 Segment와 Lap에 기록
- 한글 HUD에 현재 속도·고도와 최근/평균 구간 값 표시
- `Drone.Tutorial`과 `Drone.UI` 자동화 통과
- Blueprint Compile과 Training Map Check 오류·경고 0
- 화면 확인 후에만 수동 Pass 기록

