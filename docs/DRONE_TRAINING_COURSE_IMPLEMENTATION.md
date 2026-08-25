# TUT-01 Training Course 구현 가이드

기준일: 2026-08-24 (Asia/Seoul)

이 문서는 `C:\URproject\drone`의 실제 `ADroneTrainingCourse` 소스, 자동화 테스트, `BP_DroneTrainingCourse`, `Lvl_DroneTraining` 자산을 기준으로 한다.

TUT-01의 범위는 다음 두 가지뿐이다.

- 편집 가능한 비행 경로 `Spline`
- 플레이 중 보이지만 Drone 이동과 Navigation에는 간섭하지 않는 안내선

TUT-01 자체 완료 범위에는 Gate, 통과 Trigger, 통과 순서, 정·역방향 판정, Segment/Lap 기록과 Timing을 포함하지 않는다. 이후 TUT-02에서 Gate·Trigger·순서·정방향 판정을, TUT-03에서 Segment/Lap 시간·실제 이동 거리·평균 속도 원본 기록을 각각 별도 책임으로 구현했다.

TUT-01 자체 완료 기준선은 Unreal Commit `5a9a2fa`다. 현재 프로젝트 기준선 `551e287`에는 TUT-02 Gate와 TUT-03 Lap Recorder가 추가됐으며 Editor Build, Tutorial 6/6, 전체 `Drone.` 14/14, 전체 Blueprint Compile 0 errors·0 warnings·0 load failures를 통과했다. Standalone에서는 TUT-02 기준 실제 BP Pawn·Controller·WBP HUD, 밝은 청록 안내선과 Current/Inactive Gate를 확인했다.

## 1. 왜 필요한가

Tutorial을 처음부터 Gate와 기록 시스템까지 한 번에 만들면 경로 표시 문제, 충돌 문제, Gate 판정 문제가 서로 섞인다. TUT-01은 먼저 “Designer가 경로를 편집할 수 있고 Drone은 그 안내선을 막힘없이 통과한다”는 가장 작은 기반을 고정한다.

이 구조를 먼저 두는 이유는 다음과 같다.

- 구매한 코스나 Drone 에셋 없이 Engine Cube와 프로젝트 전용 단순 Material만으로 비행 동선을 시험할 수 있다.
- Level을 다시 모델링하지 않고 Spline 점만 움직여 접근 방향과 난이도를 바꿀 수 있다.
- 화면용 안내선과 이후의 판정용 Gate를 분리해, 표시 Mesh 때문에 Overlap이나 이동 판정이 잘못되는 일을 막는다.
- TUT-02 Gate를 추가할 때 같은 Spline과 별도 Training Map을 배치 기준으로 재사용했다.

현재 기본 S자 경로와 표시 크기는 Greybox 시험값이다. 최종 코스 형태나 아트 스타일을 확정한 값이 아니다.

## 2. Unreal에서 담당하는 클래스와 자산

### `ADroneTrainingCourse`

파일:

```text
Source/Drone/Tutorial/DroneTrainingCourse.h
Source/Drone/Tutorial/DroneTrainingCourse.cpp
```

이 Actor가 담당하는 일은 다음과 같다.

- `CourseSpline`에 비행 경로 점과 Tangent를 보관한다.
- 열린 Spline의 점 사이마다 `USplineMeshComponent` 안내선 한 개를 만든다.
- Construction이 반복될 때 이전 안내선을 지운 뒤 다시 만들어 중복을 막는다.
- Actor, Spline, 생성 안내선이 Collision, Overlap, Physics, Navigation에 관여하지 않게 한다.
- 기본 Engine Cube와 `M_DroneTrainingGuide`를 사용하되 BP에서 표시용 Mesh와 Material을 바꿀 수 있게 한다.

매 프레임 처리할 일이 없으므로 Tick은 사용하지 않는다. 이 Actor는 경로 데이터와 표시만 담당하며 게임 규칙을 소유하지 않는다.

### `BP_DroneTrainingCourse`

```text
/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingCourse
```

`ADroneTrainingCourse`의 실제 Blueprint 자식이다. Level에 배치할 자산과 Designer 조정 지점을 제공한다. 경로 생성과 비간섭 규칙은 부모 C++가 담당한다.

### `Lvl_DroneTraining`

```text
/Game/Drone/Tutorial/Maps/Lvl_DroneTraining
```

기존 Template Map을 그대로 사용하는 것이 아니라 Tutorial용으로 분리된 맵이다. 현재 자산 계약은 다음과 같다.

- `BP_DroneTrainingCourse` 한 개
- `PlayerStart` 한 개
- 직접 배치된 `ADronePrototypePawn` 없음
- World Settings의 GameMode Override는 `BP_DronePrototypeGameMode`
- 저장된 RecastNavMesh Actor 존재
- 배치된 ThirdPerson/Variant 게임플레이 Actor 없음

따라서 플레이를 시작하면 맵에 Pawn을 미리 놓는 대신 기존 BP GameMode → BP PlayerController → BP Prototype Pawn → WBP Flight HUD 연결을 그대로 사용한다.

## 3. 헤더에 무엇을 추가했는가

### 편집 가능한 경로 컴포넌트

```cpp
UPROPERTY(VisibleAnywhere, BlueprintReadOnly, Category="Tutorial|Course")
TObjectPtr<USplineComponent> CourseSpline;
```

`CourseSpline`은 실제 경로 데이터다. `GetCourseSpline()`을 통해 자동화와 후속 기능이 같은 경로를 읽을 수 있다. `BlueprintReadOnly`인 이유는 BP가 컴포넌트 참조 자체를 다른 객체로 바꾸기보다, Viewport에서 Spline 점을 편집하도록 하기 위해서다.

### 표시 자산과 Greybox 조정값

헤더에는 아래 값을 `EditAnywhere`로 열어 두었다.

- `CourseLineMesh`: 현재 기본값은 `/Engine/BasicShapes/Cube`
- `CourseLineMaterial`: 현재 기본값은 `/Game/Drone/Tutorial/Materials/M_DroneTrainingGuide`
- `CourseLineWidthCentimeters`: 기본 `32 cm`
- `CourseLineThicknessCentimeters`: 기본 `10 cm`
- `CourseLineVerticalOffsetCentimeters`: 기본 `0 cm`
- `CourseLineColor`: 기본 청록 계열 시험색

최종 외형이 정해지면 BP에서 Mesh와 Material, 폭, 두께를 바꿀 수 있다. 이 값을 바꾸는 것과 Collision 판정 기능을 추가하는 것은 별개다.

### 재구성 함수와 확인용 API

```cpp
void RebuildCourseLineSegments();
void ApplyNonInterferenceRules();
UMaterialInterface* CreateCourseLineMaterial();
int32 GetCourseLineSegmentCount() const;
UMaterialInterface* GetCourseLineMaterial() const;
static FName GetGeneratedSegmentTag();
```

- `RebuildCourseLineSegments()`는 Spline 점을 읽어 안내선을 다시 만든다.
- `ApplyNonInterferenceRules()`는 BP나 Level 값이 역직렬화된 뒤에도 Course 소유 Primitive의 안전 설정을 복원한다.
- `CreateCourseLineMaterial()`은 표시 Segment가 공유할 Dynamic Material을 만든다.
- `GetCourseLineSegmentCount()`는 현재 생성된 표시 Segment 수를 센다.
- `GetCourseLineMaterial()`은 자동화와 BP가 실제 표시 Material을 확인할 수 있게 한다.
- `GetGeneratedSegmentTag()`는 생성된 Segment를 구분하는 동일한 Tag 계약을 테스트와 후속 코드에 제공한다.

`DynamicCourseLineMaterial`은 Construction 재실행 중 Garbage Collection 추적을 유지하기 위한 `Transient` 참조다. 저장해야 하는 게임 상태가 아니다.

## 4. CPP에서 어떻게 동작하는가

### 4.1 생성자: 안전한 기본 구조

생성자는 먼저 Actor의 Tick과 Collision을 끈다. `CourseRoot`와 `CourseSpline`은 Static Mobility를 사용하며 Navigation 영향을 끈다. Spline에는 다음 비간섭 설정을 적용한다.

```text
Collision Enabled       NoCollision
Generate Overlap Events false
Simulate Physics        false
Can Ever Affect Nav     false
```

기본 경로는 아래 다섯 로컬 좌표를 사용하는 열린 Spline이다.

```text
(0,    0,    250)
(1200, 0,    350)
(2400, 700,  500)
(3600, -700, 400)
(5000, 0,    300)
```

점이 다섯 개이므로 기본 표시 Segment는 네 개다. 이 좌표는 최종 레벨 디자인이 아니라 맵을 열자마자 비행 경로를 확인하기 위한 S자형 Greybox다.

### 4.2 `OnConstruction`과 `BeginPlay`

`OnConstruction()`은 Editor에서 Actor를 배치하거나 Spline 점·표시 속성을 바꿀 때 비간섭 설정을 복원하고 안내선을 다시 만든다. `BeginPlay()`도 같은 순서를 실행해 BP/Level 직렬화나 Cook 방식이 달라도 런타임 계약을 다시 맞춘다.

두 경로가 같은 `RebuildCourseLineSegments()`를 사용하므로 Editor 표시와 실제 플레이 표시가 서로 다른 구현으로 갈라지지 않는다.

### 4.3 Segment 중복 방지

재구성을 시작하면 Actor가 소유한 `USplineMeshComponent` 중 `DroneTrainingCourse.GeneratedLineSegment` Tag가 붙은 것만 제거한다. 그 뒤 현재 Spline 점으로 새 Segment를 만든다.

따라서 Construction Script가 여러 번 실행되어도 안내선 수는 계속 누적되지 않는다. 열린 Spline에서는 아래 관계가 유지된다.

```text
표시 Segment 수 = Spline 점 수 - 1
```

실수로 Spline 점을 지나치게 늘려 Editor가 멈추는 일을 줄이기 위해 한 Actor가 만드는 Segment 수는 최대 256개로 제한한다.

### 4.4 Spline을 Mesh로 표시

각 Segment는 현재 점과 다음 점의 위치·Tangent를 받아 `SetStartAndEnd()`로 곡선을 따른다. Engine Cube의 실제 Bounds를 읽어 폭과 두께를 cm 값에 맞게 Scale하므로, Mesh 크기를 100 cm라고 코드에 고정하지 않는다.

`M_DroneTrainingGuide`는 `Opaque + Unlit`이며 `Color × Intensity`를 Emissive Color에 연결한다. 특히 `Used with Spline Meshes` 사용 플래그를 저장해 런타임 Material 대체를 막는다. C++는 이 Material로 Dynamic Material Instance를 만들고 `Color` Parameter에 `CourseLineColor`를 적용한다.

일반 Material에 SplineMesh 사용 플래그가 없으면 Editor에서 보이더라도 Standalone에서 World 기본 회색 Material로 대체될 수 있다. 표시 재질을 교체할 때는 색뿐 아니라 이 사용 플래그도 확인한다.

### 4.5 안내선의 비간섭 규칙

새로 생성되는 모든 `USplineMeshComponent`에는 다음 값을 명시적으로 다시 적용한다.

```text
Collision Profile       NoCollision
Collision Enabled       NoCollision
Generate Overlap Events false
Simulate Physics        false
Can Ever Affect Nav     false
Cooked Collision Data   만들 필요 없음
Cast Shadow             false
Receive Decals          false
Visible                 true
Hidden In Game          false
```

안내선은 “보이는 길”이지 비행 판정용 Trigger가 아니다. TUT-02에서도 Ring Visual과 판정 Trigger를 별도 Component로 분리했으며, 이 SplineMesh에는 Overlap을 켜거나 Gate 역할을 맡기지 않는다.

## 5. Blueprint와 Map에서 무엇을 설정하는가

### `BP_DroneTrainingCourse`

1. Content Browser에서 `/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingCourse`를 연다.
2. Parent Class가 `ADroneTrainingCourse`인지 확인한다.
3. Components에서 `CourseSpline`을 선택한다.
4. Viewport에서 Spline 점을 이동·추가·삭제하고 Tangent를 조정한다.
5. Class Defaults의 `Tutorial | Course | Visual`에서 Mesh, Material, 폭, 두께, Z Offset과 색을 조정한다.
6. Compile 후 안내선이 현재 Spline을 따라 다시 만들어지는지 확인한다.

외형을 바꾸더라도 새 Mesh에 Collision을 켜지 않는다. C++은 Construction과 BeginPlay마다 Course가 소유한 모든 Primitive에 비간섭 값을 다시 적용한다. Gate Trigger는 이 BP의 SplineMesh에 섞지 않고 TUT-02의 별도 `BP_DroneTrainingGate` Actor에 둔다.

### `Lvl_DroneTraining`

1. `/Game/Drone/Tutorial/Maps/Lvl_DroneTraining`을 연다.
2. World Settings의 GameMode Override가 `BP_DronePrototypeGameMode`인지 확인한다.
3. World Outliner에서 `BP_DroneTrainingCourse`가 한 개만 있는지 확인한다.
4. `PlayerStart`가 한 개이고 Prototype Pawn이 직접 배치되지 않았는지 확인한다.
5. 배치된 Course Actor를 선택해 Level 전용 경로를 조정할 수 있다.
6. 맵과 BP를 모두 저장한다.

현재 경로는 코스 흐름을 시험하는 Greybox다. TUT-02의 실제 BP Gate 네 개는 별도 Actor로 배치됐으며, Course Spline을 수정할 때 Gate 배열 순서와 GateIndex가 자동으로 바뀐다고 가정하지 않는다. Lap UI는 아직 추가하지 않았다.

## 6. Editor에서 테스트하는 방법

### 눈으로 확인

1. UE 5.8.1에서 `Lvl_DroneTraining`을 연다.
2. `BP_DroneTrainingCourse`를 선택하고 Spline 점 하나를 움직인다.
3. 점 사이의 안내선이 새 곡선을 따라 재구성되는지 확인한다.
4. PIE 또는 Standalone을 시작한다.
5. 기존 `BP_DronePrototypePawn`과 `WBP_DroneFlightHUD`가 나타나는지 확인한다.
6. Drone을 안내선의 한쪽에서 반대쪽으로 통과시킨다.
7. 안내선에 부딪히거나 멈추거나 밀려나지 않는지 확인한다.
8. Editor에서 `P`를 눌러 Navigation 표시를 켜고 안내선 때문에 NavMesh가 잘리거나 새 장애물 영역이 생기지 않는지 확인한다.

### 자동화 확인

Session Frontend의 Automation에서 아래 세 테스트를 실행한다.

```text
Drone.Tutorial.TrainingCourse
Drone.Tutorial.TrainingAssets
Drone.Tutorial.TrainingPIESmoke
```

각 테스트의 역할은 다음과 같다.

- `TrainingCourse`: native 기본값, 실제 World Spawn, N-1 Segment 생성, Construction 반복 시 중복 없음, 모든 Primitive의 Collision·Overlap·Physics·Nav 비간섭, Drone 크기 Sweep 통과를 검사한다.
- `TrainingAssets`: 실제 BP 부모, 정확한 Map 경로, BP GameMode Override, PlayerStart/Pawn/Course 개수, `M_DroneTrainingGuide`의 Unlit/Opaque/SplineMesh 사용 플래그, 배치 Course의 생성 Segment와 비간섭 설정을 검사한다.
- `TrainingPIESmoke`: 새 1인 PIE에서 실제 BP Controller·Pawn·WBP HUD·BP Course와 저장된 RecastNavMesh Actor 존재를 확인하고, 실제 PIE Drone을 안내선 가로 방향으로 Sweep한다.

자동화가 통과해도 안내선의 색·두께와 실제 조작 체감은 화면에서 별도로 확인한다.

## 7. 정상 결과

TUT-01의 정상 기준은 다음과 같다.

- `Lvl_DroneTraining`이 정확한 Tutorial 경로에서 열린다.
- 맵에는 `BP_DroneTrainingCourse` 한 개, `PlayerStart` 한 개, 직접 배치 Pawn 0개가 있다.
- 기존 `BP_DronePrototypeGameMode`가 BP Pawn, BP Controller와 WBP Flight HUD를 생성한다.
- Course Actor에는 편집 가능한 열린 `CourseSpline`이 있다.
- 기본 다섯 점에서 안내선 Segment 네 개가 플레이 중 보인다.
- Spline 점을 바꾸면 안내선이 새 경로를 따라 다시 만들어진다.
- Construction을 반복해도 이전 Segment가 겹쳐 남지 않는다.
- Drone이 안내선을 가로질러도 Blocking Hit와 Overlap이 생기지 않는다.
- 안내선은 Physics를 사용하지 않고 NavMesh에 영향을 주지 않는다.
- Course Actor는 Tick을 사용하지 않는다.

Gate 통과 표시, 다음 Gate 선택과 역방향 거부는 TUT-02에서 별도 Actor·Component로 구현됐다. Lap 시작·완료, 구간 시간·실제 이동 거리·평균 속도 원본은 TUT-03의 별도 Recorder Component로 구현됐다. 둘 다 TUT-01 자체 정상 결과에는 포함하지 않으며, 다음 작업은 **TUT-04 이전 기록 비교·Best·결과 UI**다.

## 8. 문제가 생겼을 때 확인할 항목

### 안내선이 보이지 않음

- Spline 점이 두 개 이상인지 확인한다.
- `CourseLineMesh`가 비어 있지 않은지 확인한다.
- 폭과 두께가 1 cm 이상인지 확인한다.
- Material이 완전 투명하거나 프로젝트 환경에서 사용할 수 없는 Editor 전용 자산인지 확인한다.
- BP Compile 후 Actor를 움직이거나 Construction을 다시 실행해 Segment가 재생성되는지 확인한다.
- `GetCourseLineSegmentCount()` 결과가 `Spline 점 수 - 1`인지 확인한다.

### 안내선 색이 바뀌지 않음

- `CourseLineMaterial`이 `M_DroneTrainingGuide`인지 확인한다.
- 연결한 Material에 `Color` Vector Parameter가 실제로 있는지 확인한다.
- Material의 `Used with Spline Meshes`가 켜져 있는지 확인한다. 빠지면 Standalone 로그에 `missing usage flag SplineMeshes`가 나타나며 기본 회색 Material로 대체된다.
- Lit Material은 조명에 따라 어둡게 보일 수 있으므로, 다른 Material로 교체해도 안내용 Unlit/Emissive 의도를 유지할지 함께 결정한다.

### 안내선이 여러 겹으로 생김

- Level에 `BP_DroneTrainingCourse` Actor를 두 개 이상 배치하지 않았는지 확인한다.
- 수동으로 추가한 SplineMesh와 C++이 생성한 Tag Segment를 구분한다.
- `RerunConstructionScripts()` 반복 뒤 `GetCourseLineSegmentCount()`가 증가한다면 생성 Segment의 Tag와 제거 코드가 유지되는지 확인한다.

### Drone이 안내선에 막힘

- Course가 소유한 모든 Primitive의 Collision Enabled가 `NoCollision`인지 확인한다.
- Generate Overlap Events와 Simulate Physics가 꺼져 있는지 확인한다.
- BP에 별도 Static Mesh, Blocking Volume 또는 Trigger를 추가하지 않았는지 확인한다.
- 실제 Hit Actor를 확인해 Course가 아니라 지면이나 다른 Greybox Actor에 부딪힌 것은 아닌지 구분한다.

### NavMesh 모양이 달라짐

- `CourseSpline`과 모든 생성 Segment의 `Can Ever Affect Navigation`이 꺼져 있는지 확인한다.
- 표시 Mesh Collision이 `NoCollision`인지 확인한다.
- BP에 추가한 별도 컴포넌트가 Navigation Relevant로 남아 있지 않은지 확인한다.
- `NavMeshBoundsVolume` 자체나 지면 설정을 안내선 문제로 오인해 끄지 않는다.

### Pawn이나 HUD가 나오지 않음

- `Lvl_DroneTraining` World Settings의 GameMode Override를 확인한다.
- `BP_DronePrototypeGameMode`의 Default Pawn과 PlayerController Class 연결을 확인한다.
- 맵에 Pawn을 직접 배치해 GameMode Spawn과 중복시키지 않았는지 확인한다.

### Spline 점을 너무 많이 추가함

한 Course Actor는 안전 상한 때문에 최대 256 Segment만 만든다. 257개보다 많은 점이 필요한 실제 요구가 생기면 무조건 상한만 높이지 말고 Course 분할, Editor 성능과 자동화 범위를 함께 검토한다.

## 현재 범위 요약

```text
TUT-01
ADroneTrainingCourse
→ 편집 가능한 CourseSpline
→ 비충돌·비Overlap·비Physics·비Navigation SplineMesh 안내선
→ BP_DroneTrainingCourse
→ Lvl_DroneTraining에서 기존 Prototype GameMode/Pawn/HUD 재사용

TUT-02 Done
→ Ring Gate
→ 통과 Trigger와 순서
→ 정·역방향 판정

TUT-03 Done
→ Segment/Lap 시간·실제 이동 거리·평균 속도 원본 기록

TUT-04 Todo
→ 이전 기록 비교·Best·결과 UI
```
