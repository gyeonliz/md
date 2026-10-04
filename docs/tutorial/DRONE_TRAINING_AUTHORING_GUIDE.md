# Drone Training 게이트·루트 배치 가이드

기준일: 2026-09-30 (Asia/Seoul)

이 문서는 저장소 상대 경로(최신 10/04 현재 C PC 41444c2 + 로컬 미커밋) 기준으로 작성한다. 코스 제작은 `BP_DroneTrainingCourse`에서 관리한다. 권장 자동 편집 방식은 Course Spline과 분리된 `Ring별 Spline Handle`이며, Handle 배열 순서가 곧 Gate 통과 순서다. 생성된 빛나는 선 Component, 자동 Gate Child Actor와 GateIndex를 직접 관리하지 않는다. Production `Lvl_DroneTraining`은 팀원 소유이므로 이번 기능 작업에서 저장·덮어쓰지 않았다. 검증은 `/Game/Drone/Maps/TestMap/Lvl_DroneTrainingRouteSelectionTest`에서 한다.

## 1. 현재 맵과 자산 위치

```text
/Game/Drone/Maps/Lvl_DroneTraining
/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingCourse
/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingGate
/Game/Drone/Tutorial/Materials/M_DroneTrainingGuide
```

과거 `9de1ead` 기준 Production 맵 감사 결과는 Gate Actor 17개, Course Sequence 4개였다. 현재 맵 배치 개수의 증거로 재사용하지 않는다. 수동 배치 Gate를 자동 Handle 방식으로 전환하는 작업은 맵 담당 팀원이 진행한다.

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
| `Automatic Gate Count` | 독립 Handle 모드를 끈 경우의 Ring 수, 최소 2개·최대 64개 |
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

### 이 변경의 수동 확인

2026-09-30 Editor Build와 관련 회귀 8/8(오류·경고 0), 실제 Gate/Course BP Compile 각각 0/0을 통과했다. Test World 종료 경고도 최종 재실행에서 0건이다. Production 맵/Asset 저장 없이 검증했다.

`Lvl_DroneTrainingRouteSelectionTest`에서 Gate 음원과 교체 메시를 지정한 BP로 확인한다. (1) 선이 중앙 하단 1/6 위치를 지나는지, (2) Gate Scale을 키워도 선 두께/코스 크기는 유지되는지, (3) 순서대로 정방향 통과하면 음성이 한 번씩 나오는지, (4) 세 상태 머티리얼이 바뀌고 미지정 슬롯은 그대로인지 확인한다. 음원·최종 Gate Mesh는 사용자가 지정하므로 실제 가청성·최종 외형은 자동화 성공과 별도로 확인한다.

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

