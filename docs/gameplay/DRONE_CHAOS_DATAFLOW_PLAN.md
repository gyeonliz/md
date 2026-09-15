# Drone Chaos Dataflow 물리 환경 계획

기준일: 2026-08-26 (Asia/Seoul)

## 1. 결정

UE 5.8의 Dataflow·Chaos Cloth·Chaos Destruction을 Drone 프로젝트의 후속 물리 환경 후보로 채택한다. 한 기능으로 섞지 않고 다음 두 축으로 분리한다.

1. `Chaos Cloth + Dataflow`: 일부가 고정된 채 처지는 그물, 천막, 위장망과 유연 장애물
2. `Chaos Destruction + Geometry Collection + Dataflow`: 선택된 벽·문·안테나·Jammer 설비의 파괴

Dataflow는 자산 제작과 반복 수정 수단이다. Mission 상태, Drone 충돌·포획, Damage, 실패 판정의 단일 기준은 프로젝트 C++가 소유한다. 외형·Weight Map·파쇄 형태·배치 조정은 Blueprint와 Dataflow Asset이 담당한다.

현재 우선순위 `TUT-04 → Flight 상태/Collision/Crash`를 바꾸지 않는다. 실제 물리 Spike는 현재 Editor를 종료하고 별도 기능 Branch에서 시작한다.

## 2. UE 5.8 확인 근거

- Epic의 UE 5.8 소개는 Dataflow와 Chaos Cloth를 Production-Ready로 분류하고, Dataflow를 Chaos Destruction의 비파괴 반복 제작에 사용할 수 있다고 설명한다.
- UE 5.8 Release Notes에는 Dataflow Runtime Graph Evaluation, 개선된 UI·Gizmo·Rendering, Geometry Collection용 Template과 파쇄 Node 개선이 포함된다.
- `SimulationMaxDistanceConfig`에서 최대 이동 거리가 0인 Cloth Particle은 Kinematic이 된다. `InKinematic` 선택으로 Weight Map과 별개로 고정 정점을 지정할 수도 있다.
- Chaos Destruction은 Geometry Collection, Cluster Damage Threshold, Anchor/Strain/Force/Sleep/Disable Field를 사용한다.

공식 참고:

- <https://www.unrealengine.com/news/unreal-engine-5-8-is-now-available>
- <https://dev.epicgames.com/documentation/unreal-engine/unreal-engine-5-8-release-notes>
- <https://dev.epicgames.com/documentation/en-us/unreal-engine/panel-cloth-editor-overview>
- <https://dev.epicgames.com/documentation/unreal-engine/node-reference/Dataflow/SimulationMaxDistanceConfig>
- <https://dev.epicgames.com/documentation/unreal-engine/dataflow-for-destruction-quickstart>
- <https://dev.epicgames.com/documentation/unreal-engine/chaos-fields-user-guide-in-unreal-engine>

## 3. 현재 프로젝트 상태

- 설치된 UE 5.8.1에는 `Dataflow`, `ChaosCloth`, `ChaosClothAsset`, `ChaosClothAssetEditorCore`, `ChaosClothAssetDataflowNodes`, `ChaosEditor`, `GeometryCollectionPlugin`이 존재한다.
- 현재 `Drone.uproject`에는 위 Cloth/Destruction 플러그인을 명시적으로 활성화하지 않았다.
- Deprecated인 `ChaosClothAssetEditor`, `ChaosClothEditor`는 사용하지 않는다.
- Cloth 제작 시 `ChaosClothAssetEditorCore`를 진입점으로 사용하고, 필요한 Runtime 종속성은 플러그인 의존 관계를 확인해 최소 범위로 활성화한다.
- Dataflow가 정식 기능이어도 설치본의 일부 Destruction Editor 플러그인은 Beta 표기를 가진다. 따라서 프로젝트에서는 Branch Spike·빌드·Standalone 검증을 거쳐 채택한다.

## 4. 일부 고정 그물 설계

### 자산 구조

```text
/Game/Drone/Physics/Net/
├─ Meshes/SM_NetRender_Prototype
├─ Cloth/CA_NetPrototype
├─ Dataflow/DF_NetPrototype
├─ Materials/M_NetPrototype
└─ Blueprints/BP_DroneNetObstacle
```

- Simulation Mesh는 규칙적인 저해상도 Grid로 만든다. Render Mesh와 Material은 그물 구멍을 표현하되 물리 정점 수를 불필요하게 늘리지 않는다.
- 상단 모서리 두 점, 상단 한 줄 또는 기둥에 묶인 영역을 Selection/Weight Map으로 지정한다.
- 고정 영역은 `SimulationMaxDistanceConfig`의 `MaxDistance=0` 또는 `InKinematic`으로 고정한다.
- 아래쪽으로 갈수록 Max Distance를 늘려 중력·바람·충돌에 따라 처지고 늘어지게 한다.
- Edge/Bending Stiffness, Damping, Gravity, Wind는 Dataflow 변수로 노출하고 시험값임을 이름에 표시한다.
- Drone Collision은 복잡한 FPV Visual Mesh가 아니라 단순 Sphere/Physics Asset 기준으로 시험한다.

### 게임플레이 경계

첫 Spike는 시각·물리 반응만 확인한다. “그물에 걸려 조작 불능” 같은 게임 규칙은 Cloth Vertex 접촉을 직접 판정 기준으로 쓰지 않는다.

후속 포획 기능은 프로젝트 소유 `NetCaptureVolume`이 다음 값을 판정한다.

- 진입 속도와 방향
- 머문 시간
- Drone 상태와 Mission 허용 여부
- 포획, 감속, 탈출 또는 Crash 결과

Cloth는 화면 변형을 담당하고 C++ 상태가 게임 결과를 담당한다. 이렇게 해야 Cloth Substep·LOD·Frame Rate 차이로 Mission 판정이 흔들리지 않는다.

## 5. 선택형 맵 파괴 설계

### 자산 구조

```text
/Game/Drone/Physics/Destruction/
├─ GeometryCollections/GC_WallPrototype
├─ Dataflow/DF_WallFracturePrototype
├─ Blueprints/BP_DroneDestructibleTarget
└─ Maps/Lvl_DronePhysicsSandbox
```

1. 원본 Static Mesh를 보존한다.
2. Geometry Collection을 만들고 Dataflow Graph에서 파쇄·Cluster·Collision을 생성한다.
3. 바닥·기둥 연결부는 World Support 또는 Anchor Field로 고정한다.
4. Drone 충돌, 폭발 또는 Mission Event가 프로젝트 Damage Event를 발생시킨다.
5. Damage Event가 Damage Threshold를 넘는 위치에 External Strain/Force Field를 적용한다.
6. 파편은 Sleep/Disable과 Removal 정책으로 정리한다.

맵 전체를 파괴 가능하게 만들지 않는다. 첫 적용은 다음 중 한 종류로 제한한다.

- 부서지는 얇은 벽
- 파괴 가능한 Jammer 안테나 지지대
- 폭파 가능한 출입구 또는 장애물

파괴 가능 대상은 명시적 Tag/Interface와 프로젝트 소유 Wrapper를 사용한다. Geometry Collection Hit 자체가 Mission 성공 조건을 직접 변경하지 않는다.

## 6. 성능·안전 기준

- PC Standalone 싱글플레이만 첫 검증 대상으로 둔다.
- 활성 Cloth와 Geometry Collection 수, 파편 수, Solver 시간과 Frame Time을 실행 로그에 기록한다.
- 배경 파괴는 Cache/재생 또는 비파괴 Static Mesh Proxy를 우선하고 상호작용 대상만 Live Simulation한다.
- 작은 파편은 Sleep/Disable/Removal로 정리하고 무기한 시뮬레이션하지 않는다.
- Dataflow Runtime Evaluation이 가능해도 첫 버전은 Editor에서 자산을 생성·재저장한다. 매 Frame Graph 재평가는 사용하지 않는다.
- Legacy ThirdPerson/Variant 신규 의존성 0, 새 생산 자산은 `/Game/Drone/Physics`, 새 코드는 `Source/Drone/Physics`에 둔다.
- C++·Plugin 변경 전에 열린 Editor를 저장 후 종료한다.
- 현재 열려 있는 Editor는 별도 복제본 `D:\JGY\project\droner`다. `PHY-DF-00`을 시작할 때 이를 닫고 기준 `D:\JGY\project\drone`을 명시적으로 연다.
- `droner/Content/Asset`의 36.36 GB 공급사 전체 복사본을 Physics 자산 원본 경로로 사용하거나 Commit하지 않는다. 외부 원본은 `D:\JGY\project\Unreal_260821`, 생산 이식은 `/Game/Drone/Physics`만 사용한다.

## 7. 작업 카드와 순서

| ID | 작업 | 활성화 조건 | 완료 조건 |
|---|---|---|---|
| PHY-DF-00 | Dataflow/Chaos Sandbox 준비 | TUT-04 완료 또는 별도 사용자 우선순위 변경 | 별도 Branch에서 최소 Plugin 활성화, `Lvl_DronePhysicsSandbox`, Editor/Game Build, Blueprint 0/0/0, 기존 전체 회귀 통과 |
| PHY-NET-01 | 부분 고정 그물 시각·물리 Spike | PHY-DF-00 + Flight Collision 기준 존재 | 상단 고정·하단 처짐, 중력/바람, 단순 Drone Collision, Reset/종료 정상, Standalone 3회 |
| PHY-NET-02 | 그물 포획 게임 규칙 | PHY-NET-01 + Crash/실패 상태 | 별도 Capture Volume이 포획·감속·탈출/실패를 결정하고 Cloth 결과와 분리됨 |
| PHY-DST-01 | 선택형 파괴 벽 Spike | PHY-DF-00 + Damage/Crash Event | Dataflow 파쇄, Anchor, Threshold, Strain Field, Debris 정리와 Standalone 3회 |
| PHY-DST-02 | Mission/Jamming 파괴 통합 | Mission Shell + PHY-DST-01 | Jammer/장애물 파괴 Event가 Mission을 정확히 한 번 갱신하고 Restart 시 복구 |

## 8. 검증 게이트

- `DroneEditor Win64 Development`와 `Drone Win64 Development` 성공
- Blueprint Compile errors/warnings/load failures `0/0/0`
- Physics Sandbox Map Check errors/warnings 0
- 기존 `Drone.` 전체 자동화 회귀 유지
- Plugin은 필요한 Target에만 활성화하고 Deprecated Cloth 플러그인 0
- Cloth 고정 정점이 흔들리지 않고 동적 영역만 처짐
- Drone Spawn/Input/Camera/Telemetry/HUD 결과 변화 없음
- Geometry Collection 고정부가 먼저 떨어지지 않고 지정 Threshold/Field에서만 파괴
- 종료·Restart 뒤 Cloth/파편/Delegate/Audio 잔존 0
- Standalone 새 실행 3회와 한 번의 수동 화면·성능 확인

## 9. 현재 판정

- 방향 채택과 문서 설계: 완료
- Unreal Plugin 활성화: 미실행
- Cloth/Geometry Collection 생산 자산: 0개
- 코드 변경: 0개
- 다음 기능 우선순위: 계속 `TUT-04`
