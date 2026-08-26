# Drone Training 게이트·루트 배치 가이드

기준일: 2026-08-26 (Asia/Seoul)

이 문서는 `C:\URproject\drone`의 현재 구현과 `/Game/Drone/Maps/Lvl_DroneTraining` 저장 상태를 기준으로 한다. 코스 제작 시 순서의 원본은 `BP_DroneTrainingCourse` 한 개가 가진 `OrderedGates` 배열이다. 생성된 빛나는 선 Component나 GateIndex를 직접 관리하지 않는다.

## 1. 현재 맵과 자산 위치

```text
/Game/Drone/Maps/Lvl_DroneTraining
/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingCourse
/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingGate
/Game/Drone/Tutorial/Materials/M_DroneTrainingGuide
```

현재 저장 맵 감사 결과는 Course 1개, Gate 4개, 열린 Spline 점 6개다. Spline 길이는 약 `64.9 m`이며 모든 점은 `Curve` 형식이다. 기존에 네 Gate의 저장 `GateIndex`가 모두 0이었던 문제는 Course의 `OrderedGates` 순서로 `CourseId`와 `GateIndex`를 자동 동기화하도록 수정했다.

## 2. 루트 만들기와 Spline 점 추가

1. `Lvl_DroneTraining`을 열고 World Outliner에서 `BP_DroneTrainingCourse`를 선택한다.
2. Components에서 `CourseSpline`을 선택한다.
3. Viewport의 Spline 위 원하는 위치를 우클릭하고 `Add Spline Point Here`를 선택한다.
4. 새 점을 이동·회전하고, Point Type을 `Curve` 또는 급격한 꺾임을 줄이는 `Curve Clamped`로 둔다.
5. 점의 Tangent Handle을 드래그해 진입·이탈 곡률을 조정한다. 점 위치만 옮기고 Tangent가 너무 짧으면 S자 구간도 급하게 꺾여 보일 수 있다.
6. 닫힌 순환 코스가 필요하지 않으면 `Closed Loop`를 켜지 않는다. 현재 기록 규칙은 열린 코스의 Gate 0에서 시작해 마지막 Gate에서 끝난다.
7. 맵을 저장하기 전에 코스 Actor의 `Synchronize Gate Definitions` 버튼을 한 번 실행하고 BP·Map을 저장한다. Construction과 BeginPlay에서도 같은 동기화가 자동 실행된다.

Spline 제어점과 Gate 수는 같을 필요가 없다. 제어점은 곡선의 형태를 만들고 Gate는 판정 위치를 만든다. 부드러운 곡선을 위해 필요한 만큼 Spline 점을 추가하되, Gate는 플레이 흐름상 의미 있는 통과 지점에만 둔다.

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

## 4. Gate 설치와 순서 지정

1. Content Browser에서 `BP_DroneTrainingGate`를 맵으로 끌어오거나 기존 Gate를 복제한다.
2. Gate 중심을 Spline 위 통과시키고 싶은 위치에 배치한다.
3. Gate Actor의 로컬 `+X` 방향이 드론이 통과할 정방향을 바라보게 회전한다. 링의 모양만 보고 앞뒤를 판단하지 말고 Local 축 표시로 확인한다.
4. Course Actor를 선택하고 Details의 `OrderedGates` 배열에 Gate를 실제 통과 순서대로 넣는다.
5. 배열의 0번이 출발 Gate, 마지막 원소가 종료 Gate다. 배열 중간에 `None`, 중복 Gate 또는 다른 Course의 Gate를 넣지 않는다.
6. `Synchronize Gate Definitions`를 실행한다. `CourseId`와 `GateIndex`는 배열 순서에서 자동 설정되므로 Gate마다 숫자를 손으로 맞추지 않는다.
7. 플레이 전에 Current 색이 Gate 0 하나에만 표시되고 나머지는 Inactive인지 확인한다.

Gate를 추가했는데 반응하지 않으면 `OrderedGates`에 들어갔는지, 앞 Gate를 먼저 통과했는지, 로컬 `+X` 정방향으로 들어갔는지 확인한다. Gate Visual은 비충돌이고 별도 Trigger만 Pawn Overlap을 판정한다. 빛나는 Spline은 경로 안내 전용이라 Gate 통과 판정을 하지 않는다.

## 5. 루트 수정 권장 순서

1. Spline만 편집해 접근 방향과 곡률을 먼저 만든다.
2. 편집 카메라로 빛나는 선이 Spline을 부드럽게 따르는지 확인한다.
3. 의미 있는 지점에 Gate를 배치하고 회전을 정한다.
4. `OrderedGates`를 통과 순서대로 구성하고 자동 동기화한다.
5. `Standalone Game`에서 Gate 0부터 끝까지 한 번 통과한다.
6. 역순, 같은 Gate 재통과, Gate 우회가 기록을 변경하지 않는지 확인한다.
7. HUD의 현재 비행 값과 구간 통계를 확인하고 정상 종료한다.

## 6. 현재 한글 HUD 표기

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

## 7. 저장·검증 체크리스트

- Course 1개, 직접 배치 Prototype Pawn 0개
- `OrderedGates` 배열 순서와 실제 비행 순서 일치
- GateIndex가 저장 후 `0, 1, 2, ...`로 일치
- Current Gate가 0번 하나로 시작
- 생성 코스 선이 긴 직선 조각으로 꺾이지 않고 Spline 곡선을 따름
- 코스 선 Collision·Overlap·Physics·Navigation 영향 없음
- 정방향 순서 통과만 Segment와 Lap에 기록
- 한글 HUD에 현재 속도·고도와 최근/평균 구간 값 표시
- `Drone.Tutorial`과 `Drone.UI` 자동화 통과
- Blueprint Compile과 Training Map Check 오류·경고 0
- 화면 확인 후에만 수동 Pass 기록

