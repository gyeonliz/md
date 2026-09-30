# Drone Chaos Dataflow 물리 환경 계획

기준일: 2026-09-30 (Asia/Seoul)

## 1. 결정

UE 5.8의 Dataflow·Chaos Cloth·Chaos Destruction을 Drone 프로젝트의 후속 물리 환경 후보로 채택한다. 한 기능으로 섞지 않고 다음 두 축으로 분리한다.

1. `Chaos Cloth + Dataflow`: 일부가 고정된 채 처지고 Drone 날개·Rotor 접촉을 방해하는 그물, 천막, 위장망과 유연 장애물
2. `Chaos Destruction + Geometry Collection + Dataflow`: 선택된 벽·문·안테나·Jammer 설비의 파괴

Dataflow는 자산 제작과 반복 수정 수단이다. Mission 상태, Drone 충돌·포획, Damage, 실패 판정의 단일 기준은 프로젝트 C++가 소유한다. 외형·Weight Map·파쇄 형태·배치 조정은 Blueprint와 Dataflow Asset이 담당한다.

2026-09-29 사용자 우선순위 변경으로 독립 Physics Sandbox와 절차형 비교 기준을 먼저 만들었다. 실제 Dataflow/Chaos Cloth·Geometry Collection Spike는 `Greybox 화면 확인 → Cloth/Destruction 자산 비교` 순서로 진행한다.

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

- 설치된 UE 5.8.2에는 `Dataflow`, `ChaosCloth`, `ChaosClothAsset`, `ChaosClothAssetEditorCore`, `ChaosClothAssetDataflowNodes`, `ChaosEditor`, `GeometryCollectionPlugin`이 존재한다.
- `Drone.uproject`에 `Dataflow`, `GeometryCollectionPlugin`, `ChaosClothAsset`, Editor 전용 `ChaosClothAssetEditorCore`를 명시적으로 활성화했다. Deprecated `ChaosClothAssetEditor`·`ChaosClothEditor`는 사용하지 않는다.
- Cloth 제작 시 `ChaosClothAssetEditorCore`를 진입점으로 사용하고, 필요한 Runtime 종속성은 플러그인 의존 관계를 확인해 최소 범위로 활성화한다.
- Dataflow가 정식 기능이어도 설치본의 일부 Destruction Editor 플러그인은 Beta 표기를 가진다. 따라서 프로젝트에서는 Branch Spike·빌드·Standalone 검증을 거쳐 채택한다.
- `/Game/Drone/Maps/TestMap/Lvl_DronePhysicsSandbox`에 전용 Pawn만 켜는 Hit Normal 반발, 고정 벽 2개, `BP_DroneNetPlacementRig`, `BP_DroneBreakableWallPanel`을 배치했다.
- 첫 화면 확인에서 절차형 그물·벽의 기본 크기가 Drone에 비해 과대했고, 전용 Drone의 Hit 처리도 반발만 수행해 대상 파괴로 이어지지 않는 결함이 있었다. 그물은 6×3m, 벽은 약 5.55×3.69m로 축소하고, 유효 충돌 시 같은 Hit 위치에 Point Damage를 전달하는 공용 Bridge를 추가했다. 기본 국소 파괴 최소 속도는 2.5m/s다.
- `ADroneNetPlacementRig`는 네 Corner·가로/세로 줄 수·분할·중심 처짐·굵기·충돌·피해/충돌 임계값을 Blueprint에서 조절한다. 일반 Drone 충돌은 기본적으로 절단하지 않고 실제 Pawn 이동 속도를 얽힘 상태에 전달한다. Point Damage 또는 명시적으로 `Break On Impact`를 켠 경우에만 충돌 반경 Segment를 제거하고 최대 16개 Rigid Body 조각을 기본 5초간 표시한다. Reset은 원본과 물리 조각을 함께 복원/정리한다. 잔존 줄 전체의 중력·탄성 시뮬레이션은 아직 Chaos Cloth가 아닌 절차형 비교 기준이다.
- `ADroneBreakableWallPanel`은 온전한 격자를 ISM으로 유지하고 충돌/피해 반경의 조각만 물리 Static Mesh로 전환한다. Columns·Rows·조각 크기·간격·파괴 반경·Impulse·최소 충돌 속도·파편 유지 시간을 Blueprint에서 조정한다. 기본 8초 뒤 파편을 정리하며, 이는 Geometry Collection의 게임 규칙과 체감 비교를 위한 Runtime Greybox이고 실제 Dataflow 파쇄 자산은 아니다.
- 2026-09-30 `UDroneCollisionResponseComponent`에 결정적 Net Entanglement 상태를 추가했다. 접촉 속도와 반복 접촉으로 Severity를 누적해 감속·조종/추력 저하·하강을 적용하고 임계값 이상을 Captured로 판정한다. 후속 화면 교정에서는 반응을 보간하고 Root 회전 교란을 완만한 외형 기울기로 바꿨다. 그물 접촉의 피격 Shake 호출과 반복 즉시 속도 절단은 제거했지만 총알 피격 Camera Shake는 유지한다. 자동 해제와 모든 수치는 Blueprint에서 조절한다.
- 카메라 접촉 피드백은 별도 Pivot/위치 보간으로 분리하고 Net Strand는 Camera 채널만 기본 Ignore한다. 연속 벽 접촉은 매번 순간 회전/이격/새 충격을 재생하지 않는다. 실제 이동·의도한 FPV 자세·총알 피격은 카메라에서 제거하지 않는다. 현재 수동 화면 확인이 남아 있다.
- 같은 Component의 벽 반발은 일반 Flight Pawn에서 기본 On이다. 수평에 가까운 Blocking 벽·기둥·구조물에 저속부터 속도 비례 반발·표면 분리·자세 Kick을 적용하고 바닥·천장·Ground UGV는 제외한다. Collision Root 바깥 네 Wing/Rotor Sphere Probe가 기체 모서리 접촉을 보강한다.
- `DroneEditor Win64 Development`, Physics Map Check `0/0`, 최종 `Drone.Physics` 2/2, 변경 영향 `Drone.Prototype` 8/8과 기존 `Drone.Mission.StoryPhysicsTestMaps` 1/1이 성공했다.

## 4. 일부 고정 그물 설계

### 배치 기술 Spike

- `BP_DroneNetObstacle`은 네 모서리 Scene Handle을 노출하고 Level Viewport에서 각 점을 직접 이동할 수 있게 한다.
- 첫 버전은 사각형 그물만 지원한다. Handle 4개의 중심·폭·높이·회전을 계산해 Editor Preview를 맞추고, 실제 Cloth Asset은 검증된 크기 단계 또는 Scale 범위 안에서만 사용한다.
- 고정할 위쪽 두 점/한 줄은 Blueprint 옵션으로 고르고 Dataflow의 Kinematic Selection과 일치시킨다.
- Construction Script는 Editor Preview만 갱신하며 Play 중 매 Frame Dataflow Graph나 Mesh를 재생성하지 않는다.
- Handle 이동, 회전, 비균일 배치, 바닥/기둥 접촉과 복제 배치를 Sandbox에서 확인한 뒤에만 다점·곡면 그물로 확장한다.

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

그물의 최종 Gameplay 역할은 `날개/Rotor가 걸려 감속·자세 교란·포획 또는 추락을 일으키는 장애물`이다. 첫 Spike는 그 역할에 필요한 시각·물리 반응을 확인하되, “그물에 걸려 조작 불능” 같은 게임 규칙은 Cloth Vertex 접촉을 직접 판정 기준으로 쓰지 않는다.

현재 C++ v1은 Collision Root Hit, Collision Root 바깥 네 Wing/Rotor Sphere Probe와 프로젝트 소유 `UDroneCollisionResponseComponent`가 다음 값을 판정한다. Cloth 표현을 붙인 뒤 필요할 때만 별도 `NetCaptureVolume`로 접촉 위치 정확도를 더 보강한다.

- 진입 속도와 방향
- Collision Root와 Wing/Rotor Contact Probe의 접촉 수·위치
- 머문 시간
- Drone 상태와 Mission 허용 여부
- 접촉 누적값에 따른 추력/속도 저하와 Roll/Yaw 교란
- 역추진·접촉 해제로 탈출할지, `Snared → Entangled`로 고정되거나 Crash할지

Cloth는 화면 변형을 담당하고 C++ 상태가 게임 결과를 담당한다. 이렇게 해야 Cloth Substep·LOD·Frame Rate 차이로 Mission 판정이 흔들리지 않는다.

Runtime Net Rig의 국소 절단과 떨어지는 Rigid Body Segment는 충돌 위치·Impulse·Reset을 빠르게 확인하기 위한 진단 기능이다. “부딪히면 즉시 구멍이 나서 통과”하지 않고 먼저 걸림·감속·추력/조종 저하·자세 교란·하강이 발생하도록 v1을 구현했다. 절단은 폭발물·절단 도구·Mission Rule이 요구할 때만 별도 옵션으로 활성화한다.

### 일반 벽·구조물 반발

- 반발 로직은 맵의 특정 벽 Blueprint나 Tag가 아니라 비행 Drone Collision Root의 모든 유효한 Blocking Hit에 적용한다.
- 접촉 상태가 유지되는 동안은 새 충격/자세 Pulse를 반복하지 않고 새 안쪽 입력만 바깥 제약으로 바꾼다. 표면 분리는 Sweep 보간으로 적용하며 Root에 즉시 회전을 더하지 않는다. 작은 외형 기울기는 카메라에서 분리하고 총알 피격 Camera Shake는 유지한다.
- 충돌 법선과 입사 속도로 바깥쪽 반발 속도·분리 거리·자세 Kick을 연속 비례 계산한다. `120cm/s` 미만을 무시하거나 저속에도 고정 `90cm/s` Kick·고정 `6cm` 순간 이격을 주지 않는다. 같은 벽에 계속 입력해도 벽 안으로 누적 침투하거나 표면을 비비며 정지하지 않아야 한다.
- 바닥 착륙 후보는 Flight/Landing 상태와 표면 법선으로 제외하고, 강한 충돌은 단순 반발보다 Crash/Damage 규칙을 우선한다. 얇은 벽 고속 통과는 Sweep/CCD 시험으로 따로 검증한다.
- `UDroneCollisionResponseComponent`는 일반 Flight Pawn에서 기본 활성화되고 벽형 표면 법선만 분류한다. 남은 작업은 강한 Crash/Damage 우선순위, Landing 상태와의 명시적 통합, 얇은 벽 Sweep/CCD 및 여러 시험맵 수동 회귀다.

### 그물 파괴 시험

Dataflow가 자산 제작을 담당한다고 해서 Chaos Cloth Runtime Tearing이 곧바로 안정적인 Mission 규칙이 되는 것은 아니다. 첫 Sandbox에서 아래 두 방식을 같은 크기·충돌 조건으로 비교한다.

1. Cloth/Constraint 수준에서 지정 영역 절단 또는 연결 해제가 가능한지 확인한다.
2. 그물을 여러 패널로 나누고 가장자리 연결부를 프로젝트 Damage Event로 끊는 방식으로 대체한다.

완료 기준은 Drone 충돌/공격 위치 주변만 열리고, 고정점이 유지되며, Restart에서 원상 복구되고, 파괴 Event가 Mission에 한 번만 전달되는 것이다. 엔진 기능이 불안정하면 2번을 채택하며 실제 천 찢김을 과장해 표현하지 않는다.

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
| PHY-DF-00 | Dataflow/Chaos Sandbox 준비 | 사용자 우선순위 변경으로 시작 | 플러그인 명시 활성화, `Lvl_DronePhysicsSandbox`·Editor Build·Map Check·집중 회귀 완료. 실제 Dataflow 자산/Standalone 3회는 남음 |
| PHY-NET-00 | 그물 4점 배치 기술 | PHY-DF-00 | Blueprint Corner 4개·줄 수·처짐·굵기·충돌·국소 파괴/복구 Greybox와 저장 계약 완료. Viewport Transform Handle UX는 후속 |
| PHY-NET-01 | 부분 고정 그물 시각·물리 Spike | PHY-NET-00 + Flight Collision 기준 존재 | 상단 고정·하단 처짐, 중력/바람, 단순 Drone Collision, Reset/종료 정상, Standalone 3회 |
| PHY-NET-02 | 그물 파괴 방식 비교 | PHY-NET-01 + Damage Event | Cloth 절단과 분할 패널 연결부 파괴를 비교하고 안정적인 한 방식을 선택. 부분 개방·고정점·Restart·성능 확인 |
| PHY-NET-03 | 날개 걸림·그물 포획 게임 규칙 | C++ 접촉 누적 v1 완료 | 수동 체감 조정, Contact Probe/Interaction Volume, 탈출 입력·Crash/Mission 실패, Cloth와 결합 후 Standalone 3회 |
| PHY-COL-01 | 일반 벽·구조물 공통 반발 | 일반 Flight 공통 v1 완료 | 여러 맵 수동 회귀, 바닥 Landing·강한 Crash 분리, 연속 접촉 비비기/침투 0, 얇은 벽 Sweep/CCD 확인 |
| PHY-DST-00 | 선택형 파괴 벽 Runtime 기준 | PHY-DF-00 | 격자 조각 국소 파괴·Impulse·기본 8초 파편 정리·복구와 BP 수치 조정, 저장 계약·자동화 완료. 최종 수치는 수동 체감 뒤 확정 |
| PHY-DST-01 | 선택형 파괴 벽 Chaos Spike | PHY-DF-00 + Damage/Crash Event | Geometry Collection/Dataflow 파쇄, Anchor, Threshold, Strain Field, Debris 정리와 Standalone 3회 |
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
- Unreal 실행 로그와 프로젝트 명시 설정에서 Dataflow·Geometry Collection·Chaos Cloth Asset 경로 활성화 확인
- Cloth/Geometry Collection 생산 자산: 0개
- 코드 변경: 일반 Flight 공통 벽 반발, 결정적 그물 얽힘/포획 v1, 대상 Point Damage 전달, 선택적 국소 절단/복구 4점 Net Rig, 조각별 물리 전환 Breakable Wall 추가
- 다음 기능 우선순위: Physics Sandbox 수동 화면에서 반발·그물 감속/포획·복구 체감 확인 → 실제 Cloth/Geometry Collection 비교, 병행해서 Tutorial Best Lap SaveGame
