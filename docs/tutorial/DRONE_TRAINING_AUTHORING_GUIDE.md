# Drone Training 게이트·루트 배치 가이드

현재 조정 기준: 2026-10-14 (Asia/Seoul)

코스 제작은 `BP_DroneTrainingCourse`에서 관리한다. 권장 자동 편집 방식은 Course Spline과 분리된 `Ring별 Spline Handle`이며, Handle 배열 순서가 Gate 통과 순서다. 생성된 빛나는 선 Component, 자동 Gate Child Actor와 GateIndex를 직접 관리하지 않는다. 공용 BP의 RaceRing·상태 재질 연결은 반영됐다. Main 자동78개 승계·비사용20개 참조 문제는 이전 조사 결과이며 이후 맵 변경 수신으로 현재 개수/참조를 재확인해야 한다. 기능/외형 시험은 `/Game/Drone/Maps/TestMap/Lvl_DroneTrainingRouteSelectionTest`에서 하고 팀원 Production은 덮어쓰지 않는다. 과거 측정·실행 근거는 [WORKLOG](../history/DRONE_WORKLOG.md).

## 1. 현재 맵과 자산 위치

```text
/Game/Drone/Maps/Lvl_DroneTraining
/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingCourse
/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingGate
/Game/Drone/Tutorial/Materials/M_DroneTrainingGuide
```

과거 `9de1ead` 기준 Production 맵 감사 결과는 Gate Actor 17개, Course Sequence 4개였다. 현재 맵 배치 개수의 증거로 재사용하지 않는다. 수동 배치 Gate를 자동 Handle 방식으로 전환하는 작업은 맵 담당 팀원이 진행한다.

### 첫 수업: 고정 관찰 시점 기초 조종

첫 수업의 표시명은 `기초 조종 / BASIC FLIGHT`, 호환 ID는 기존 `Mission.Tutorial.Hover`다. 기존8수업 연결을 유지하면서 **사람 눈높이의 고정 카메라로 드론을 바라보고** 이륙→전진→후진→실제 착지를 연습한다. 사람 캐릭터를 새로 빙의하거나 드론 FPV로 바꾸는 수업이 아니다. 입력·빙의는 Drone에 남고 카메라만 Observer Actor를 사용한다.

| 무엇을 여나 | 위치 |
|---|---|
| 첫 수업 전용 시험 맵 | `/Game/Drone/Maps/TestMap/Tutorial/Lvl_Tutorial_Observer_Test` |
| 배치/조정 BP | `/Game/Drone/Mission/Blueprints/Tutorial/BP_TutorialObserverLesson` |
| 목표4개·목록·다음 수업 | `/Game/Drone/Data/Missions/DA_Mission_Tutorial_Hover` |

BP Components에서 `ObserverCamera`의 위치·회전·FOV를 조절한다. 기본 높이는165cm이며 자동 추적/회전하지 않는다. `LaunchPoint` 화살표는 **바닥 출발점과 기체 전방**을 정한다. Actor를 옮기거나 회전하면 수업 기준도 함께 옮겨진다. 카메라를 포함한 Actor 전체 Scale을 키우기보다 Component Transform과 아래 수치로 조정한다.

Class Defaults 또는 배치 Instance의 `Drone > Tutorial > Observer`:

| 항목 | 기본 시험값·의미 |
|---|---|
| Flight / Minimum·Maximum Flight Height | 출발 시 기체 중심 대비125~400cm 높이 |
| Forward Distance / Position Tolerance | 전방900cm·허용 오차180cm |
| Maximum Flight Speed / Maximum Tilt / Flight Hold | 100cm/s 이하·기울기25° 이하·1초 유지 |
| Backward Heading Tolerance / Minimum Backward Travel | 기수 오차30° 이내·후진 이동 증거500cm. 짧은 코스에서는 요구 거리를 자동 제한 |
| Landing / Maximum Landing Speed / Landing Hold | 25cm/s 이하·1.25초 접지 유지 |
| Ground Contact Tolerance / Minimum Support Normal Z / Ground Trace Channel | 바닥 Sweep 접지 판정5cm·법선Z≥0.75·Visibility. 바닥 Collision도 같은 채널에 Block 필요 |

수동 확인 순서:

1. FrontEnd→튜토리얼 첫 `기초 조종` 또는 전용 맵 직접 Play로 진입한다. 드론1대가 지면에 놓이고 사람 시점 카메라가 고정되는지 확인한다.
2. 쉬운 조작으로 이륙해 출발점 위 지정 높이에서1초 멈춘다. 전방 패드까지 이동해 멈춘다.
3. **기체 방향을 돌리지 않고 후진**해 출발점 위로 돌아온다. 180° 돌고 전진해서 돌아오는 방식은 후진 성공이 아니어야 한다.
4. 출발점에 낮은 속도로 실제 바닥에 착지해 멈춘다. 높이만 낮거나 공중에 멈춘 상태로 완료되면 안 된다.
5. 수업 중 P/마우스로 Observer 화면이 따라가지 않는지, 추락 재출격 시4단계가 처음부터 시작되는지, 다음 수업/로비에서는 원래 카메라가 복원되는지 확인한다.

이전 `Lvl_Tutorial_Hover_Test`·공유 종합 시험장·팀원 Production Training은 덮어쓰지 않는다. 자산 설치 도구 `Tools/AssetMigration/BuildDroneObserverTutorial.py`는 새 전용 맵을 만들되 이미 존재하는 맵은 검증만 하며 재생성하지 않는다. 자동화 항목 `Drone.Tutorial.ObserverLessonContract / ObserverGroundSupport / ObserverLessonPIE`와 실제 키보드·패드/화면 확인은 구분한다. 현재 실행 결과는 STATUS·WORKLOG, 새 수업의 수동 체감은 확인 대기다.

## 2. 루트 만들기와 Spline 점 추가

Production Lvl_DroneTraining 편집·저장은 맵 소유 팀원만 한다. AI 기능 검증은 TestMap/Lvl_DroneTrainingRouteSelectionTest에서 수행한다. 아래 저장 단계는 해당 TestMap 또는 맵 소유 팀원에게만 적용한다.

1. `Lvl_DroneTraining`을 열고 World Outliner에서 `BP_DroneTrainingCourse`를 선택한다.
2. Components에서 `CourseSpline`을 선택한다.
3. Viewport의 Spline 위 원하는 위치를 우클릭하고 `Add Spline Point Here`를 선택한다.
   - 또는 기존 Spline 점 하나를 선택하고 `W` 이동 모드에서 `Alt`를 누른 채 이동 기즈모 화살표를 좌클릭 드래그하면 그 점이 복제되어 새 Spline 점이 된다.
   - `Alt+좌클릭`만 누르는 동작이 아니라 반드시 선택한 점의 **이동 기즈모를 드래그**해야 한다.
4. 새 점을 이동·회전하고, Point Type을 `Curve` 또는 급격한 꺾임을 줄이는 `Curve Clamped`로 둔다.
5. 점의 Tangent Handle을 드래그해 진입·이탈 곡률을 조정한다. 점 위치만 옮기고 Tangent가 너무 짧으면 S자 구간도 급하게 꺾여 보일 수 있다.
6. 닫힌 순환 코스가 필요하지 않으면 `Closed Loop`를 켜지 않는다. 현재 기록 규칙은 열린 코스의 Gate 0에서 시작해 마지막 Gate에서 끝난다.
7. 맵을 저장하기 전에 코스 Actor의 `Synchronize Gate Definitions` 버튼을 한 번 실행하고 BP·Map을 저장한다. Construction과 BeginPlay에서도 같은 동기화가 자동 실행된다.

Spline 제어점은 코스 곡선만 만든다. Ring 수와 위치는 별도의 `Ring별 Spline Handle` 배열이 담당하므로 제어점을 움직이지 않고 Ring만 옮길 수 있다. Handle을 움직이면 가장 가까운 Spline 위치로 투영되고, Handle 항목을 추가·삭제하면 Ring도 하나씩 추가·삭제된다.

점 추가가 Actor 복제로 동작하면 `BP_DroneTrainingCourse` Actor만 선택한 상태다. Components의 `CourseSpline`과 Viewport의 실제 Spline 점을 다시 선택한다. `Ring별 Spline Handle`의 3D Widget은 Gate 전용 점이며 CourseSpline 점 추가 대상이 아니다.

## 3. 빛나는 코스가 각져 보였던 이유와 현재 규칙

기존 구현은 Spline 제어점 한 쌍마다 긴 Cube Spline Mesh 한 개만 만들었다. Spline 자체가 Curve여도 제어점 사이가 길면 화면의 단면·Tangent 보간이 거칠게 보여 빛나는 선이 꺾인 것처럼 보일 수 있었다.

현재 전체 Spline을 분할하되 상한에 걸리지 않은 짧은 코스(TestMap68·113조각)는 기존 균일 분할을 유지한다. 긴 코스만 같은 조각 수를 sqrt(곡률) 밀도+15% 균일 몫으로 배치한다. 목표 길이 CourseLineSegmentLengthCentimeters 기본200cm와 표시 예산 MaximumCourseLineSegments를 구분한다. 생성 CourseLineSegment_*를 직접 이동·복제하지 않는다.

### 3-1. 장거리 코스 수정·팀원 조정 — 10/04 C PC Claude

구현됨·자동 검증됨·수동 확인 대기. Production을 저장하지 않고 측정한 값은 액터Scale2·로컬9.6km(월드19.2km)·92 CurveAuto점이다. 이전 고정256 균일분할은 약75m 조각·실제경로 대비최대7.9m/95%2.3m 오차였다. MountainRange33.8km·Island10.6km도 같은 원인이다.

| 조정 위치 | 값·의미 |
|---|---|
| BP_DroneTrainingCourse > Tutorial > Course > Visual | MaximumCourseLineSegments 기본1024·16~4096. 측정으로 고른 시작값·확정값 아님. 긴 코스는 목표길이만 낮춰도 상한에 걸림 |
| Production 동일경로1024 측정 | 최대약50cm·95%7cm. 더 매끈하게는2048(최대약20cm) 검토 |
| BP Class Settings | Run Construction Script on Drag Off. 끄는 동안 매프레임 재구성 대신 놓을 때1회, BP만 저장됨 |
| 재생성 비용 | 256조각46ms·1024조각258ms(로드/BeginPlay1회), Component/렌더 예산 비교 필요 |

CourseLineAdaptiveSegments 자동 검증: 짧은코스 불변·15.2km 시험코스 최대오차 균일256244cm→곡률25640cm→곡률10243cm·상한 변경/감소·BP드래그설정. 근거 Saved/Automation/ClaudeCourse/inspect.log·deviation.log·bp_drag.log·review_fix_test.log(Claude 실행). MCP 급커브 캡처 확인·Production맵 미저장, 팀원 코스 외형과 Editor 편집 체감은 수동 대기다. 원래92점·CurveAuto·Gate/Handle위치·순서·개수·폭·색을 보존하고 기능검증은 TestMap, Production저장은 맵 소유 팀원만 한다.

## 4. 자동 Spline Ring Gate 배치

`BP_DroneTrainingCourse`를 선택하고 Details의 `Tutorial > Course > Automatic Gates`에서 다음 값을 조정한다.

| 항목 | 역할 |
|---|---|
| `Use Automatic Spline Gates` | 자동 Ring 생성 사용 여부 |
| `개별 Ring 위치 Handle 사용` | 권장 직접 편집 모드. Course Spline은 유지하고 Ring 전용 Handle을 사용 |
| `Ring별 Spline Handle` | Viewport에 표시되는 Ring별 독립 3D 위치점. 배열 Index가 통과 순서 |
| `Automatic Gate Count` | 독립 Handle 모드를 끈 경우의 Ring 수, 최소2·최대512. UI 슬라이더 범위2~128, 그 이상은 수치 직접 입력 |
| `Automatic Gate Class` | 공용 Course BP 기본은 `BP_DroneTrainingGate`. Native/다른 개별 override는 별도로 확인 |
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

### 권장: Spline 위에서 링만 하나씩 직접 이동

1. Course에서 `Use Automatic Spline Gates`를 켠다.
2. `현재 배치에서 Ring Handle 만들기`를 한 번 누른다. 현재 숫자 배치 또는 수동 `OrderedGates` 위치를 복사해 `Ring별 Spline Handle` 배열을 만들고 독립 Handle 모드를 켠다.
3. Details에서 `Ring별 Spline Handle`의 원하는 Index를 선택하고 Viewport의 3D Widget을 드래그한다.
4. Handle은 드래그한 위치에서 Course Spline의 가장 가까운 지점으로 붙고, Ring만 그 위치와 접선 회전을 따라간다. CourseSpline 제어점과 코스 곡선은 바뀌지 않는다.
5. Ring을 추가하려면 Handle 배열에 항목을 추가한 뒤 새 Widget을 원하는 Spline 구간 가까이 옮긴다. 삭제하면 같은 Index Ring도 제거된다. 시작·종료 판정을 위해 최소 2개를 유지한다.
6. 즉시 붙지 않거나 전체를 재정렬하려면 `모든 Ring Handle을 Spline에 붙이기`, 이어서 `Rebuild Automatic Gates`를 누른다.

생성된 `AutomaticSplineGate_*`를 직접 드래그하면 다음 Construction 때 위치가 다시 계산된다. 반드시 `Ring별 Spline Handle`의 3D Widget을 잡아 움직인다. `Automatic Gate Distance Offset(s)`와 `Automatic Gate Local Offset(s)`은 Handle 원본을 바꾸지 않고 앞뒤·좌우·높이를 미세 보정할 때만 사용한다.

자동 Gate의 순서는 Spline 거리 증가 방향이며 Actor 로컬 `+X`가 해당 지점의 Spline 진행 방향을 따른다. `GateIndex`, `CourseId`, `SegmentDistance`와 Sequence 배열은 자동 동기화된다. 생성된 `AutomaticSplineGate_*` Component나 그 Child Actor를 Outliner에서 직접 옮기지 않는다.

권장 시작값:

```text
Use Automatic Spline Gates = true
개별 Ring 위치 Handle 사용 = true
Ring별 Spline Handle = Ring 수만큼
Automatic Gate Class = BP_DroneTrainingGate
```

기존 숫자 배치가 필요할 때만 개별 위치 Handle을 끄고 Automatic Gate Count/거리 배열을 쓴다. `Tools/AssetMigration/ConfigureAutomaticTrainingGates.py`는 기본 검증만, 저장은 `DRONE_TRAINING_GATE_APPLY=1`일 때만 허용한다. 기존 `DRONE_TRAINING_GATE_VALIDATE_ONLY=1`도 검증만 한다. Production 편집·저장은 맵 담당 팀원만, AI 검증은 TestMap이다.

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

### Spline을 게이트 중앙 하단 1/6 지점에 두기

Course Actor의 `Tutorial > Course > Automatic Gates`에서 다음 값을 조정한다.

| Details 표시 이름 | 내부 속성 이름 | 설정 |
|---|---|---|
| 게이트 안쪽 Spline 높이 비율 | `AutomaticGateSplineHeightFraction` | 기본 `0.166667` = 안쪽 하단에서 전체 통과 높이의 1/6. `0.5`는 중앙, `0`은 하단 |
| 게이트 공통 위치 보정 (cm) | `AutomaticGateLocalOffset` | 전체 Gate의 추가 X/Y/Z 보정. 기본 `(0,0,0)` |
| 게이트별 위치 보정 (cm) | `AutomaticGateLocalOffsets` | 특정 Gate만 추가 보정. 배열 Index가 Gate 순서 |

스플라인의 곡선·제어점·안내선은 움직이지 않고 **게이트 중심만 위로 옮겨** 선이 중앙 하단을 지나게 한다. 기본 통과 높이 350cm에서는 Gate 중심이 선보다 약 116.67cm 위다. Gate를 확대해도 1/6 비율이 유지된다. 공통/개별 위치 보정을 추가하면 그만큼 선과의 상대 위치도 바뀐다. 정확한 1/6 정렬이 목적이면 보정 Z는 0으로 둔다.

자동 Gate는 Construction과 Play 시작 때 새 배치 규칙을 적용한다. 과거에 중심에 저장된 Child도 Play 때 재배치하므로 맵을 다시 생성할 필요가 없다. **수동 `OrderedGates`는 자동으로 이동시키지 않는다.** 수동 Gate는 팀원이 위치를 조절하거나 합의 후 자동 배치로 전환한다.

### 코스 선과 별개로 Gate 크기 조절

- `게이트 전용 스케일` (`AutomaticGateScale`): Gate Visual과 통과 Trigger만 함께 확대한다. 예: `(1,1.5,1.5)`는 앞뒤 깊이를 유지하고 폭/높이를 1.5배로 만든다.
- `게이트별 추가 스케일` (`AutomaticGateScales`): 공통 스케일에 Index별 배율을 곱한다. 없는 항목은 `(1,1,1)`이다.
- Course Actor의 Transform Scale이나 `CourseSpline` Scale을 키우면 **코스 전체가 커진다.** Gate만 키울 때는 위 전용 항목을 사용한다.
- 선 폭/두께는 기존 `CourseLineWidthCentimeters` / `CourseLineThicknessCentimeters`로만 조절한다.
- 수동 Gate는 Gate Actor 자체의 Scale을 조절한다. Course Actor의 Scale은 건드리지 않는다.

런타임 BP에서도 Course의 `Configure Automatic Gate Presentation`으로 공통 위치·Gate 스케일·높이 비율·개별 스케일을 지정할 수 있다. 이 호출은 Gate를 재구성하고 진행을 초기화하므로 Lap 도중 매 프레임 호출하지 않는다.

### 통과 음성 / 사운드 슬롯

1. `/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingGate`를 연다.
2. `Class Defaults > Tutorial > Gate > Audio`의 **통과 음성 / 사운드** (`GatePassSound`)에 `SoundWave` 또는 `SoundCue`를 넣는다. 녹음 음성도 같은 슬롯을 사용한다.
3. 기본은 **통과음 2D 재생** On, 볼륨 1.0, 피치 1.0이다. 2D는 빠르게 지나가도 안내 음성이 거리 때문에 작아지지 않는다. 공간음이 필요하면 2D를 끈다.
4. Compile·Save 후 Course의 `AutomaticGateClass`가 이 BP인지 확인하고 `Rebuild Automatic Gates`로 Editor 미리보기를 갱신한다.

**현재 목표를 정방향으로 정상 통과했을 때만 1회 출력**한다. 오순서·역방향·중복 통과·Reset·Construction·색 변경에서는 출력하지 않는다. 새 Lap에서 다시 정상 통과하면 다시 출력한다. 슬롯이 None이면 무음이며 임의 음원을 자동으로 연결하지 않는다.

Gate BP의 `On Gate Passed` 이벤트에 자막/연출을 붙일 수 있다. 사운드는 C++에서 이미 출력하므로 이 이벤트에 같은 Play Sound를 또 연결하면 두 번 들린다. 통과 판정/다음 Gate 진행 로직은 Sequence에서만 처리한다. 음성 겹침 제어가 필요하면 Sound 자산의 Concurrency로 제한한다.

### 상태별 머티리얼 지정과 완성형 Gate 자산 교체

기존 세 상태 **색상**과 별개로, `BP_DroneTrainingGate > Class Defaults > Tutorial > Gate > Visual`에 다음 **머티리얼 지정 슬롯**이 있다.

| 슬롯 | 적용 시점 |
|---|---|
| 통과 전 머티리얼 (`InactiveMaterial`) | 아직 순서가 오지 않은 Gate |
| 현재 목표 머티리얼 (`CurrentMaterial`) | 지금 통과할 Gate |
| 통과 후 머티리얼 (`CompletedMaterial`) | 정상 통과한 Gate |

빈 상태 슬롯은 공통 `RingMaterial`을 사용한다. 런타임 BP는 `Set Gate State Materials`로 세 재질을 지정할 수 있다. 임의 Material도 **재질 교체 자체**는 동작한다. 색상까지 조정하려면 `상태 색상 파라미터 이름`(기본 `Color`)과 실제 Material의 Vector Parameter 이름을 맞추고 Base Color 또는 Emissive에 연결한다. 파라미터가 없는 Material에 색상 값만 넣어도 색이 바뀌지는 않는다.

완성형 링/사각 Gate 에셋을 받을 때:

1. `Tutorial > Gate > Asset > 완성형 게이트 메시` (`GateAssetMesh`)에 **전체 Gate Static Mesh 하나**를 지정한다. `RingSegmentMesh`는 임시 네 변에 반복 사용하는 구형 슬롯이므로 전체 Gate를 넣지 않는다.
2. `게이트 메시 로컬 보정`으로 Pivot 위치·회전·크기를 조절한다. Gate 판정의 정방향은 Actor 로컬 `+X`, 통과 평면은 `YZ`다. 메시는 이 평면과 통과 Box에 맞춘다.
3. `상태 재질 적용 슬롯` (`GateAssetStateMaterialSlots`)에 상태를 바꿀 Material Index를 넣는다. 기본 `[0]`, 빈 배열은 전체 슬롯이다. 금속 기둥 재질을 보존하려면 발광/링 부분 슬롯만 지정한다.
4. 세 상태 머티리얼과 색을 설정한다. 선택한 슬롯에는 상태 재질을 적용하고, 선택하지 않은 슬롯에는 메시의 원래 재질을 유지한다. 상태 재질과 공통 `RingMaterial`을 모두 비우면 메시 원본 재질을 사용하며 대응 Color Parameter만 갱신한다.
5. 전체 Gate 메시를 지정하면 Greybox 네 변은 숨겨진다. 슬롯을 None으로 비우면 Greybox로 복구된다. **교체 Mesh는 비충돌**이고 기존 Box Trigger가 판정을 담당한다.

메시 보정 Scale은 외형만 바꾸므로 통과 영역 크기는 자동으로 추측하지 않는다. BP의 `통과 영역 반쪽 크기`를 실제 Mesh 안쪽 크기에 맞춘 뒤 Course의 Gate 전용 스케일로 외형과 판정을 함께 키운다. 원형 메시도 현재 판정은 정사각형 Box/aperture이므로 원형 모서리 판정이 꼭 필요하면 별도 요구사항으로 처리한다.

#### 현재 제공 RaceRing 설정

| 항목 | 현재 연결·조정 |
|---|---|
| 전체 메시 | `/Game/Item/Gate/RaceRing` 하나. 같은 폴더 `Center/Inner/Outter`는 Material Instance이며 조립용 메시가 아님 |
| GateAssetLocalTransform | Rotation **Yaw/Z=90°**, Scale `(1.75,1.75,1.75)`, Location `(-2.21339,0,0)`cm. 원본 XZ 평면을 Gate YZ에 맞추고 중심 보정 |
| 크기 기준 | 원본 개구부 반쪽100cm → 현재 TriggerHalfSize175cm에 맞춤. Gate 반쪽 크기를 바꾸면 Visual Scale=반쪽크기/100, X 중심 보정도 같은 배율로 조절 |
| 상태 적용 슬롯 | `[1]`(Center). 슬롯0 검정·2 흰색은 메시 원본 재질 유지 |
| 통과 전 / 목표 / 통과 후 | `M_BLUE / m_green / M_BLUE`, Vector Parameter 이름 `Param`. 기존 세 상태 색을 유지하므로 어두운 파랑 / 초록 / 밝은 청록·파랑으로 구분 |

RaceRing의 작성값 **Yaw90°·Scale1.75는 유지**한다. Gate 전용 Scale을 `(1,2,2)`처럼 비균등하게 키우면 Native 코드가 메시 회전축에 맞춰 **실제 Visual의 파생 Scale만 보상**한다. 저장된 `GateAssetLocalTransform`·Pivot·회전·Actor Scale·통과 Box는 바꾸지 않는다. Components에 보이는 보상값을 작성값으로 직접 되돌리거나, 좁아진 외형을 피하려고 Yaw90°를 지우지 않는다. 축정렬 회전은 정합 대상이며, 임의 각도와 비균등 Scale이 만드는 shear까지 일반 StaticMesh Transform으로 정확히 표현하는 기능은 아니다.

자동 Gate는 정상 Spline 접선의 Quaternion·Roll·회전 Offset을 그대로 사용한다. `CurveClamped` 점 등에서 **정확한 접선이 0인 경우만** 전후 실제 경로 위치의 유한 차분으로 진행 방향을 복원한다. 닫힌 코스 경계는 거리를 순환시키고 열린 코스는 끝에서 제한하며, 모든 점이 겹쳐 방향을 찾을 수 없는 완전 퇴화 코스는 명시적인 기본 방향을 사용한다. Spline 점·접선·Gate 거리·개수·1/6 높이 설정과 수동 Gate는 임의 수정하지 않는다.

이 Native 보상을 받기 위해 `LandscapeAutoMaterial_Island_Example` 원본 맵을 재생성하거나 다시 저장할 필요는 없다. 새 Source를 받은 PC에서 Editor 종료 후 빌드·재열기하고 기존 Gate 크기와 진행 방향을 확인한다. 이전 Native 잔존 Gate나 세그먼트는 별도 소유권 확인 없이 삭제하지 않는다. 최종 빌드·화면 검증 판정은 [STATUS](../../STATUS.md)를 따른다.

변경 위치는 공용 `BP_DroneTrainingGate`의 Class Defaults다. Material 슬롯을 준비한 것과 실제 상태 부모/Vector Parameter를 연결한 것을 구분한다. 원본 `/Game/Item/Gate` 메시와 재질의 색/그래프는 보존하며, `/Game/Material/m_green`만 아래 Nanite 플래그를 보강했다. 공용 BP의 상태 슬롯·색상·통과 음원을 바꾸면 해당 BP를 쓰는 자동 Gate에 승계되지만, Native 또는 개별 override를 가진 기존 수동 Gate까지 일괄 변경되지는 않는다.

이전 조사에서 Main 비사용20개는 사용 Sequence 밖이었다. 변경된 현재 맵은 먼저 개수·참조를 재확인하고 임의 삭제하거나 `ConfigureAutomaticTrainingGates.py` apply로 재배치하지 않는다. 지정 Gate 적용 도구도 누락된 native Trigger/Visual을 만나면 맵 변경·저장 전 중단한다. 복구/정리는 맵 담당자와 범위를 정한 별도 작업이다.

`m_green`의 Nanite 사용 플래그 누락은 byte 백업 후 해당 플래그만 켜서 저장했다(색·그래프 보존). 새 프로세스 RHI에서 해당 경고가 사라진 것은 확인했지만 세 상태색·실제 제품 맵 외형은 별도 수동 확인한다. Editor의 일시적 자동 보완만 보고 저장 완료로 판단하지 않는다. 적용/백업 근거는 [WORKLOG](../history/DRONE_WORKLOG.md)에 있다.

### 수동 확인

현재 자동 검사와 과거 결과의 날짜·PC·경고는 [WORKLOG](../history/DRONE_WORKLOG.md)를 따른다. 자동 성공을 실제 화면·가청성·코스 완주 Pass로 표시하지 않는다.

`Lvl_DroneTrainingRouteSelectionTest`에서 `AutomaticGateClass=BP_DroneTrainingGate`인지 확인하고 시험한다. (1) 선이 중앙 하단 1/6 위치를 지나는지, (2) Gate Scale을 키워도 선 두께/코스 크기는 유지되는지, (3) 정방향·정순서 통과 음성이 한 번씩 나오는지, (4) RaceRing의 세 상태 색이 바뀌고 검정·흰색 슬롯은 그대로인지 본다. 실제 음원은 아직 별도 지정이며, 실제 가청성·최종 외형은 자동 검사와 구분한다. Main은 현재 저장본의 배치/참조를 먼저 읽기 확인하며 이 시험 때문에 맵을 덮어쓰지 않는다.

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

1. CourseSpline 제어점과 Tangent로 코스 곡선과 접근 방향을 먼저 만든다.
2. 편집 카메라로 빛나는 선이 Spline을 부드럽게 따르는지 확인한다.
3. 권장 자동 모드에서는 독립 Handle 배열 수로 Ring 수를 정하고 각 Widget을 Spline 위에서 옮긴다. 숫자 자동 모드는 균등 배치가 필요한 코스에만 쓰고, 수동 모드에서만 Gate Actor와 `OrderedGates`를 직접 구성한다.
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

이전 완주 평균·Best·시간/속도 Delta와 저장 최고기록 표시·Best Lap JSON은 구현됨·자동 검증됨·수동 확인 대기다. 평균 History는 실행 중만 유지하며 같은 조건 재실행 복원을 직접 확인한다.

## 8. 저장·검증 체크리스트

### Gate BP 임시 재질 저장 오류와 팀원 반영

`Illegal reference to private object ... BP_DroneTrainingGate ... MID_M_BLUE ... EditorOnlyData`라면 링 개수와 별개로 **BP 기본값 객체(CDO)의 임시 재질 참조**를 확인한다. 코스/스플라인 없이 Gate BP 하나만으로도 재현된 저장 거부다. 팀원 프로세스 크래시까지 같은 원인인지는 해당 PC 콜스택을 대조한다.

`Source/Drone/Tutorial/DroneTrainingGate.cpp`의 상태 재질 갱신은 CDO/Archetype에 원본 정적 재질만 연결하고, 실제 Gate 인스턴스에서만 안전한 원본을 부모로 한 고유 MID를 만든다. 완성형 메시뿐 아니라 숨긴 Legacy 링의 재질 참조도 검사한다. 기존 16개 컴포넌트는 저장 호환용으로 남으며 이를 삭제하는 방식으로 해결하지 않는다. 색/상태 재질·메시·Pivot·크기·Trigger 판정은 유지한다.

팀원은 **C++ 수정과 수리한 Gate BP를 함께** 받아 Editor 종료 후 DroneEditor를 빌드한다. BP만 받거나 예전 C++로 다시 기본값을 갱신하면 재발할 수 있다. 팀원이 Gate BP 자체를 별도로 편집했다면 덮어쓰지 말고 먼저 보존/대조한다. 그 팀원 값에 맞춰 한 개 BP만 수리하는 도구는 `Tools/AssetMigration/RepairDroneTrainingGateTemplateMaterials.py`다. 기본 `audit`는 읽기 검사이고, 새 코드 Build 후 `DRONE_GATE_TEMPLATE_REPAIR=apply`로 원본 bytes 백업·기하/3재질/색 동일 검사를 거쳐 Gate BP 한 개만 저장한다. 별도 프로세스의 `verify`로 템플릿 MID 참조0을 확인한다. 전체 Gate 이식/Production 재생성 도구를 수리 목적으로 실행하지 않는다.

실제 수락은 새 Gate 단독·Course 자동 Gate 생성→위치 수정→저장→다른 맵으로 전환→재로드 후 Gate/Trigger·위치 유지까지다. 임시 진단은 별도 Diagnostics에서만 수행하고 Production Training은 저장하지 않는다. 코드/저장·재로드 검사 결과와 원본 백업 경로는 STATUS·WORKLOG를 따른다. 폴더 삭제나 DDC/Intermediate 삭제를 이 오류의 해결책으로 사용하지 않는다.

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

