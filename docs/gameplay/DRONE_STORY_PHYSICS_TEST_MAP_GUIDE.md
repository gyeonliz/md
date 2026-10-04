# Story·Physics TestMap 실행 가이드

기준일: 2026-09-30

Production `/Game/Drone/Maps/Lvl_DroneTraining`은 팀원이 실제 Tutorial을 제작하는 맵이다. 이 시험을 위해 열어 저장하거나 덮어쓰지 않는다. 아래 시험 자산은 모두 `/Game/Drone/Maps/TestMap`과 `/Game/Drone/Physics`에 격리했다.

## 1. Physics Sandbox

맵: `/Game/Drone/Maps/TestMap/Lvl_DronePhysicsSandbox`

이 맵만 Content Browser에서 직접 열어 Play한다. 전용 GameMode가 시험 Drone 한 대를 Spawn하지만 벽 반발 Component 자체는 이제 모든 일반 비행 `ADronePrototypePawn`에서 기본 활성화된다.

2026-09-29 화면 피드백 수정본의 기본 크기는 그물 `6m × 3m`, 파괴 벽 약 `5.55m × 3.69m`다. 이전 생성본의 약 `13m × 12m` 그물과 약 `12.8m × 9.2m` 벽은 잘못된 시험 크기였으므로 기준으로 사용하지 않는다. 맵이 열린 채 수정됐다면 Editor를 닫았다 다시 열거나 맵을 Reload해야 저장된 축소본을 볼 수 있다.

1. 앞의 두 벽에 먼저 아주 천천히 닿고, 이어 중간 속도와 고속으로 정면·비스듬하게 충돌한다.
2. 저속 접촉도 무시되지 않고 조금씩 밀려나며, 속도가 클수록 반발 속도·분리 거리·부드러운 본체 기울기가 커지는지 확인한다. 표면 분리는 기본 `0.12초` 보간이며 같은 벽을 계속 누르는 동안 새 충격을 반복하지 않는다. 위치/시점이 순간적으로 튀거나 피격처럼 화면이 덜컥거리면 실패다.
3. 기체 중심 Collision보다 바깥의 날개/로터 끝을 벽 모서리에 스치게 한다. 중심이 아직 닿지 않아도 Probe가 접촉을 잡고, 접촉 방향 반대로 밀리면서 충돌 속도에 비례해 기체가 살짝 기울어야 한다.
4. `PhysicsSandbox_NetRig`을 선택하고 Details의 `Drone|Physics|Net|Placement`와 `Drone|Physics|Net|Layout`에서 네 Corner, 가로·세로 줄 수, Segments, Sag Depth, Strand Thickness를 바꾼다.
5. Drone으로 그물 중심과 가장자리에 저속·중간 속도·고속으로 각각 충돌한다. 평범한 접촉에서는 Strand가 사라지지 않고, 기본 `0.25초` 반응 보간으로 감속·입력/추력 저하가 적용되며 본체는 천천히 기울고 아래로 끌려야 한다. 그물 접촉이 피격 Camera Shake를 재생하거나 줄마다 3인칭 Camera Arm이 수축/복귀하면 실패다.
6. 고속으로 한 번 충돌하거나 짧은 간격으로 반복 접촉해 포획 단계의 강한 감속·하강이 나오는지 본다. 기본 자동 해제 뒤에는 조종 비율이 100%로 복구돼야 한다. 현재 지속시간은 기본 4초에서 충돌 강도에 따라 늘어나는 시험값이다.
7. Drone Pawn의 `CollisionResponseComponent`에서 반발/분리값과 `Drone|Physics|Collision Response|Rotor Probes`의 네 Local Offset, Probe Radius, Trace Channel, 최대 Angular Kick·기준 속도·Lever Arm을 기체 크기에 맞춰 조정한다. `Drone|Physics|Net Entanglement`에서는 포획 관련 값을 조정한다. Net Actor에서는 `Entangle Drones On Impact`와 최소 얽힘 속도를 조정한다.
8. 절단 진단이 필요할 때만 Net Details의 `Break On Impact`를 켠다. 그러면 `Local Break Radius Centimeters`, `Minimum Impact Speed`, Detached Segment Impulse/Lifetime/최대 조각 수가 적용된다. 기본은 Drone 충돌 절단 Off이며, 탄환·폭발 Point Damage 국소 절단은 계속 사용할 수 있다.
9. `Reset Net Greybox`를 호출해 모든 Strand가 원래 상태로 돌아오고 떨어지던 물리 조각도 즉시 제거되는지 확인한다.
10. 더 앞쪽의 `PhysicsSandbox_BreakableWall`에 정면과 비스듬한 각도로 `2.5m/s`보다 빠르게 충돌한다. 맞은 반경의 조각만 분리되어 충격 방향으로 날아가고 나머지 벽이 유지되는지 확인한다.
11. 벽 Details의 Columns·Rows·Piece Size·Gap·Local Break Radius·Break/Random Impulse·Minimum Impact Speed·Debris Lifetime을 조정하고 `Reset Wall`로 복구한다. 기본 파편은 8초 뒤 정리된다.

### 벽·그물 카메라 조정(총알 피격과 분리)

`P`로 1/3인칭을 바꿔 벽에 천천히 접근→강하게 충돌→벽 방향으로 계속 입력→그물 접촉을 비교한다. 카메라는 실제 이동·의도한 조작 회전은 따라가고, 접촉 외형 기울기만 받지 않는다. 벽의 Camera 충돌은 유지해 시점이 벽 안에 들어가지 않게 한다. 마지막으로 Shotgun/NPC TestMap에서 총알에 맞아 **기존 화면 피격 흔들림이 남아 있는지** 확인한다.

| 조정 위치 | BP 항목 | 기본값/의미 |
|---|---|---|
| Drone Pawn Class Defaults → `Prototype/Camera/Stability` | `카메라 벽·그물 흔들림 차단` | On. FPV는 `CameraFlightPivot`을 사용해 접촉 기울기만 제외. 총알 피격은 유지 |
| 같은 위치 | `카메라 이동 보간 사용` / `카메라 이동 추종 속도` | On / 18. 낮추면 부드러워지지만 이동 추종이 느려짐. 시선 회전 지연은 추가하지 않음 |
| 같은 위치 | `1인칭/3인칭 최대 이동 보간 거리` | 20cm / 100cm. 큰 지연으로 카메라가 기체에서 떨어지는 것을 제한 |
| `CollisionResponseComponent` → `Contact Feedback` | `벽 접촉 해제 여유 시간` | 0.18초. 연속 접촉의 재충격 방지 |
| 같은 위치 | `표면 분리 보간 시간` / `접촉 외형 기울기 보간 시간` | 0.12초 / 0.10초 |
| 같은 위치 | `벽 접촉 기울기 지속 시간` | 0.35초. 본체만 작은 기울기 Pulse 후 복귀 |
| 같은 Component → `Net Entanglement` | `그물 감속 반응 시간` / `그물 완만한 기울기 각도` / `주파수` | 0.25초 / 3° / 0.35Hz. 조종 저하와 외형을 완만하게 적용 |
| Net Actor → `Drone/Physics/Net/Camera` | `그물이 카메라 암을 막음` | Off. Camera 채널만 Ignore하고 Pawn 충돌은 그대로 유지 |

구 `NetAttitudeDisturbanceDegreesPerSecond`는 저장 자산 호환용 미사용 값이다. 그물에 닿을 때 Root에 주기적인 회전을 더하지 않으며 새 기울기 각도/주파수를 사용한다. 일반 총알 피해는 기존 `DamageShake` 경로를 그대로 탄다.

비행 Drone의 충돌 응답 Component는 벽 반발 뒤 같은 `FHitResult` 위치·입사 방향을 맞은 Actor에 Point Damage로 전달한다. 따라서 실제 Drone 충돌로 Breakable Wall의 국소 파괴 경로가 실행된다. Net은 별도로 감지해 반발/Point Damage보다 얽힘을 우선하므로 기본 충돌만으로 찢어지지 않는다.

현재 그물과 파괴 벽은 Dataflow/Chaos의 게임 규칙·체감 비교용 Runtime Greybox다. 그물의 끊어진 Segment는 실제 Rigid Body로 떨어지지만 남은 그물 전체가 Cloth처럼 휘거나 늘어나지는 않는다. 벽도 Geometry Collection Cluster/Field가 아니라 맞은 조각을 물리 Component로 바꾼다. 네 Corner는 Details 좌표값으로 조절하며 Viewport Handle은 아직 없다. 즉 현재 결과를 “Chaos Cloth/Geometry Collection 완료”로 판정하지 않는다. 실제 Cloth 고정 정점과 Geometry Collection 파쇄는 다음 자산 Spike에서 같은 맵의 별도 구역으로 비교한다.

`그물에 닿으면 즉시 잘려 통과`하지 않는 C++ 게임 규칙 v1은 구현됐다. 실제 이동 속도와 반복 접촉이 감속·조종/추력 저하·자세 교란·하강·포획을 결정하고 Cloth Solver 결과에는 의존하지 않는다. Collision Root 바깥 Wing/Rotor Probe도 벽·그물 접촉을 검사한다. 현재 국소 절단은 Hit 위치와 파편 반응을 확인하는 진단 기능이다. 남은 작업은 Chaos Cloth 화면 변형, 역추진/접촉 해제 탈출과 Crash/Mission 실패 연결이다.

벽 반발은 이 맵의 두 Cube가 아니라 일반 비행 Drone의 유효 Blocking 벽·기둥·구조물 접촉에 공통 적용된다. 수평에 가까운 표면 법선만 반발시키고 바닥·천장·Ground UGV는 제외한다. 같은 벽을 계속 눌렀을 때 비비기·침투가 남는지, 강한 Crash와 얇은 벽 고속 Sweep/CCD를 어떻게 분리할지는 수동 확인과 후속 구현 항목이다.

## 2. Story Mission 진입 공통

Story 4맵을 직접 Play하면 `MissionTest_DefaultEntry`가 해당 DA로 기체 선택을 준비한다(10/01 이후). 통합 흐름은 FrontEnd의 스토리 메뉴에서 확인한다.

### Mission 1 — Golden Time

- 맵: `/Game/Drone/Maps/TestMap/Lvl_DroneStory01_GoldenTimeTest`
- Mission ID: `Mission.Story.GoldenTime.Test`
- 추천 Drone: Drop Drone
- 간이 흐름: Payload 전달 → 귀환
- 아직 없음: 선택 정보 수집, 화물 분실 실패, 실제 연출

### Mission 2 — Intercept

- 맵: `/Game/Drone/Maps/TestMap/Lvl_DroneStory02_InterceptTest`
- Mission ID: `Mission.Story.Intercept.Test`
- 추천 Drone: FPV
- 간이 흐름: Spline 차량 추적·파괴 → 목적지 도달 전 성공
- 아직 없음: 잔해 정보 수집, 마지막 분기, 실제 차량·폭발 연출

### Mission 3 — Veil Breaker

- 맵: `/Game/Drone/Maps/TestMap/Lvl_DroneStory03_VeilBreakerTest`
- Mission ID: `Mission.Story.VeilBreaker.Test`
- 추천 Drone: Fiber Optic Drone
- 간이 흐름: 재밍 구역 진입·이탈 → 귀환
- 아직 없음: 재머 파괴, Mission 중 Fiber Drone에서 UGV로 전환, 광섬유 실패 조건

### Mission 4 — Endgame

- 맵: `/Game/Drone/Maps/TestMap/Lvl_DroneStory04_EndgameTest`
- Mission ID: `Mission.Story.Endgame.Test`
- 추천 Drone: Ground UGV
- 간이 흐름: 지휘 목표 3개 파괴 → 귀환
- 아직 없음: 장거리 타격, 최종 환경·엔딩 연출

## 3. Tutorial Hover 재확인

1. FrontEnd에서 `튜토리얼 1-1 - 호버링`를 선택한다.
2. Scout Drone으로 시작한다.
3. 시험맵의 네 모서리 기둥으로 표시된 Hover Zone 안으로 들어간다.
4. 이동 입력을 놓고 속도와 회전을 안정시킨 채 3초 유지한다.
5. 목표가 `Return To Base`로 바뀌는지 확인한다.

자동화 `Drone.Tutorial.HoverMissionPIE`는 FrontEnd 선택부터 Zone 진입, 실제 3초 안정 Hover, 귀환 목표 전환까지 통과했다. 수동 확인에서는 Zone 가독성과 조작 체감만 추가로 본다.

## 4. 자동 검증

- `Drone.Physics.CollisionResponse`
- `Drone.Physics.Breakables`
- `Drone.Mission.StoryPhysicsTestMaps`
- `Drone.Tutorial.HoverMissionPIE`
- `Drone.Flow.Contract`
- `Drone.Flow.FrontEndContract`
- `Drone.Flow.FrontEndPIE`

Story·Physics 자산을 다시 만들거나 검증할 때는 `Tools/AssetMigration/Invoke-DroneStoryPhysicsTestMaps.ps1`을 사용한다. Tutorial 공유 시험맵은 `Tools/AssetMigration/Invoke-DroneTutorialMissionTest.ps1`로 별도 관리한다.

2026-09-30 접촉 카메라 교정 최종 결과는 MSVC 14.51.36257 Editor Build 성공, `Drone.Physics` 4/4, `Drone.Prototype` 8/8, `Drone.Mission.StoryPhysicsTestMaps` 1/1 Success(자동화 이벤트 오류·경고 0)다. `ContactSmoothing`은 순간 이격/Root 회전 없음, 지속 벽 접촉 12회 중복 충격 없음·해제 후 새 충격 허용, 시간 적분 그물 감속, FPV 접촉 회전 차단·실제 피해 Camera Shake 유지와 그물 Camera Ignore/Pawn Block을 검사한다. `ContactSmoothingBlueprint`는 관련 BP 6개를 메모리 Compile(오류/경고 0)하고 Camera Pivot/실제 피격 유지 계약을 확인한다. 기존 Physics Map Check `0/0` 저장 계약은 유지하며 이번 작업은 패키지/맵을 저장하지 않았다. 보고서: `drone/Saved/Automation/ContactCameraIsolation/index.json`. 실제 시점 부드러움은 아직 수동 확인 대상이다.

## 5. 다음 구현 순서

1. Physics Sandbox 수동 벽 반발·그물 감속/포획·자동 해제/조종 복구·선택적 절단 확인
2. Story 4개 Mission의 간이 Objective 수동 통과 확인
3. Mission 1부터 실패 조건과 UI 문구 보강
4. 현재 Runtime 그물/벽 기준과 Dataflow/Chaos Cloth·Geometry Collection 자산을 같은 조건으로 비교
5. 현재 Wing/Rotor Contact Probe와 Net Interaction 상태에 역추진/접촉 해제 탈출·포획/추락·Mission 실패 연결
6. 공통 벽 반발에 Landing/Crash 우선순위와 얇은 벽 Sweep/CCD 검증 추가
7. 파편 Sleep/Disable/Removal과 Mission Damage Event 1회 전달 추가
