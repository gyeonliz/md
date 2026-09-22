# Truck·Smart Object 동선 설계 가이드

기준일: 2026-09-22 (Asia/Seoul)

이 문서는 팀원이 맵에서 차량과 NPC 동선을 설계할 때 사용하는 진입 문서다. 차량 동선과 Smart Object 동선은 서로 다른 시스템이며, 같은 Spline이나 번호 규칙을 공유하지 않는다.

## 1. 현재 구현 상태부터 구분하기

| 구분 | 현재 동작 | 아직 없는 것 |
|---|---|---|
| Truck Greybox | 4점 지면 Trace, Z·Pitch·Roll 추종, 전후 이동, Steering, 바퀴 회전, 차량형 포탑 부모 추종 | 장애물 회피, Chaos Vehicle |
| Vehicle Spline Route v1 | 별도 Route BP의 Spline 거리·접선을 따라 XY/Yaw 이동, 기존 4점 Trace가 Z·Pitch·Roll 유지, 끝 도착 Event·정지/반전/Loop | 곡률 감속, Look Ahead 조향, Mission Director 목적지 실패 연결 |
| Greybox Auto Drive | 배치 시작 위치와 Yaw를 기준으로 한 직선 구간 왕복 | 커브 주행, 교차로, 정류, Mission 목적지 판정 |
| Smart Object NPC | 역할 Tag에 맞는 최근접 빈 Slot을 Claim하고 NavMesh로 이동 | `1→2→3` 고정 순서, Spline Patrol, Route ID 기반 분기 |

현재 차량의 `Greybox Auto Drive`는 실제 임무용 동선 기능이 아니다. 시작점에서 `Greybox Auto Drive Distance`만큼 직진했다가 같은 방향을 유지한 채 후진하는 화면 시험 기능이다. 장애물 Sweep과 경로 탐색도 하지 않으므로 Mission 2 이동 표적에 그대로 사용하지 않는다.

## 2. 작업 위치와 소유권

- 차량·Smart Object 시험 맵: `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`
- 차량 Blueprint: `/Game/Drone/Vehicles/Blueprints/BP_GroundConformingVehicle_Greybox`
- Smart Object Blueprint: `/Game/Drone/AI/SmartObjects/Blueprints`
- 실제 Tutorial 제작 맵: `/Game/Drone/Maps/Lvl_DroneTraining`

`Lvl_DroneTraining`은 팀원이 제작 중인 Production Map이다. 담당자 합의 없이 차량·순찰 시험 Actor를 추가하거나 저장하지 않는다. Unreal Map은 Git에서 병합할 수 없는 Binary이므로 한 시점에 한 명만 같은 `.umap`을 수정한다.

## 3. 현재 Truck 직선 시험 동선 배치법

1. `Lvl_NPCSmartObjectGreybox`를 연다.
2. `BP_GroundConformingVehicle_Greybox`를 배치한다.
3. Actor의 `+X`가 진행 방향을 향하도록 Yaw를 맞춘다.
4. Instance Details에서 `Greybox Auto Drive Enabled`를 켠다.
5. `Greybox Auto Drive Speed`와 `Greybox Auto Drive Distance`를 조정한다.
6. 차량 아래 도로가 네 바퀴 Trace를 받을 수 있도록 `Visibility`를 Block하는지 확인한다.
7. PIE에서 차체 Z·Pitch·Roll, 네 바퀴 구름, 차량형 포탑 추종을 확인한다.

현재 시험 기본값은 속도 `220 cm/s`, 왕복 거리 `1050 cm`다. 차량 크기와 지면 추종 값은 [`DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md`](DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md)에서 조정한다.

### 직선 시험에서 지켜야 할 배치 기준

- 차량 중심선 양쪽에 최소 차량 반 폭보다 `100cm` 이상 여유를 둔다.
- 네 Trace 중 세 개 이상이 항상 지면을 맞아야 Pitch·Roll이 갱신된다.
- `Trace Length`보다 큰 낭떠러지나 계단을 시험 구간 중간에 두지 않는다.
- 차량의 최대 지면각 기본값은 `28°`지만, Mission용 도로는 시각 안정성을 위해 `15°` 안쪽 경사를 우선한다.
- 현재 이동은 장애물을 Sweep하지 않으므로 벽이나 NPC를 통과할 수 있다. 장애물 회피 검증에는 사용하지 않는다.

## 4. Vehicle Spline Route v1 배치법

현재 다음 두 Blueprint가 준비돼 있다.

- Route: `/Game/Drone/Vehicles/Blueprints/BP_DroneVehicleSplineRoute`
- Vehicle: `/Game/Drone/Vehicles/Blueprints/BP_GroundConformingVehicle_Greybox`

```text
BP_DroneVehicleSplineRoute
└─ RouteSpline
   ├─ 출발점
   ├─ 커브/경유점
   └─ 목적지

BP_GroundConformingVehicle_Greybox
→ RouteSpline의 현재 진행거리 추적
→ 현재 거리의 위치와 접선으로 XY·Yaw 계산
→ 기존 4점 Trace가 Z·Pitch·Roll 담당
→ 끝 도착 시 On Spline Route Reached End Event 발생
```

### 맵에서 연결하는 순서

1. 안전한 TestMap에 `BP_DroneVehicleSplineRoute`를 배치한다.
2. Route Actor를 선택하고 `RouteSpline`을 선택한다.
3. 기존 Point를 선택한 뒤 `Alt+이동 기즈모 드래그`로 새 Point를 만들거나, 선분 우클릭 `Add Spline Point Here`를 사용한다.
4. 도로 중심선에 맞추고 일반 커브는 Point Type을 `Curve` 또는 `Curve Clamped`로 둔다.
5. `BP_GroundConformingVehicle_Greybox`를 배치하고 Details의 `Drone > Vehicle > SplineRoute`에서 `Spline Route`에 방금 Route Actor를 지정한다.
6. `Follow Spline Route`를 켜고 `Spline Follow Speed`를 조정한다.
7. 끝에서 왕복하려면 `Reverse At Spline End`, 처음으로 순간 이동해 반복하려면 `Loop Open Spline`을 사용한다. 둘 다 끄면 끝에서 정지한다.
8. PIE에서 XY/Yaw가 Spline을 따르는 동안 차체 Z/Pitch/Roll과 바퀴 접지가 지면을 따르는지 확인한다.

현재 팀원이 수정 중인 `Lvl_NPCSmartObjectGreybox`에는 자동 배치하지 않았다. 같은 Binary Map을 덮어쓰지 말고 맵 담당자가 직접 Route를 배치·연결한다.

### 현재 Blueprint에 노출된 값

| 값 | 용도 |
|---|---|
| `RouteSpline` | 맵에서 직접 편집하는 차량 중심선 |
| `Spline Route` | Vehicle Instance가 따라갈 Route Actor 참조 |
| `Follow Spline Route` | Spline 추종 On/Off |
| `Spline Follow Speed` | 진행 속도, 기본 `300cm/s` |
| `Reverse At Spline End` | 끝과 시작에서 진행 방향을 뒤집어 왕복 |
| `Loop Open Spline` | 열린 Spline 끝에서 시작 거리로 Loop |
| `On Spline Route Reached End` | 종점 도달 시 Blueprint에서 받는 Event |

`RouteId`, 곡률별 속도, Look Ahead, 출발 지연, Mission Director 목적지 실패 보고는 아직 후속이다. 현재 v1은 배치와 지면 굴곡 추종을 먼저 확인하는 Greybox이며 장애물 회피용 경로 탐색이 아니다.

### Spline을 그리는 기준

1. Spline은 도로의 가장자리나 바퀴 자국이 아니라 차량 중심선을 따라 그린다.
2. 직선은 Point를 과도하게 늘리지 않고, 방향이나 경사가 바뀌는 곳에만 추가한다.
3. 완만한 구간은 Point 간격 `500~1000cm`, 급한 커브는 `200~500cm`를 시작값으로 사용한다.
4. Point Type은 꺾이는 연출이 아니라면 `Curve` 또는 `Curve Clamped`를 사용한다.
5. 기본 최대속도 `360cm/s`, 최대 Yaw `45°/s`에서는 이론상 최소 회전반경이 약 `460cm`다. 화면 안정성을 위해 Mission 도로는 가능하면 `700cm` 이상의 곡선 반경으로 설계한다.
6. Spline을 이동시킨 뒤 도로 Collision과 네 Trace가 모두 맞는지 확인한다. Spline이 지면을 통과하거나 허공에 있어도 차량 높이는 Spline Z가 아니라 지면 Trace가 결정한다.
7. 마지막 Point 직전에 충분한 감속 거리를 둔다. 마지막 Point를 벽·문·낭떠러지에 바로 붙이지 않는다.
8. 목적지 실패 Trigger는 차량 Actor 전체가 들어갈 크기로 두고 `RouteId` 또는 Actor Tag로 대상 차량을 제한한다.

### 검증 상태와 후속 자동화

- 완료: Spline Actor 기본점, 진행거리, Follow On/Off, Reverse/Loop 설정, 도착 Event 계약 자동화.
- 완료: `Drone.Vehicle.GroundConformingSuspension`에서 Route Follow 계약과 기존 4점 지면 추종 회귀 통과.
- 수동 대기: 곡선·경사 도로에서 차체·바퀴·차량형 자동포탑 화면 확인.
- 후속: Frame Rate별 진행거리, Mission 목적지 Event 1회성, 파괴 차량 중단, 곡률 감속·장애물 정책.

## 5. Smart Object 동선 설계법

Smart Object는 차량 Spline과 달리 `점들의 망`이다.

```text
역할에 맞는 Activity 검색
→ 반경 안의 최근접 빈 Slot Claim
→ NavMesh 이동
→ 도착 방향 정렬·대기/사용
→ Release
→ 직전 지점 주변을 피하고 다시 검색
```

### 배치 순서

1. World Outliner에서 `Station_` 또는 `BP_SO_`를 검색한다.
2. 용도에 맞는 Blueprint를 배치한다.
   - 적 순찰: `BP_SO_EnemyPatrol`
   - 아군 순찰: `BP_SO_FriendlyBasePatrol`
   - 생활·대기: `BP_SO_Ambient`
   - 경계: `BP_SO_Guard`
   - 엄폐: `BP_SO_Cover`
   - 병사가 잡는 유인 기관총: `BP_SO_MGTurret`
3. `W`로 위치를 옮기고 `E`로 Yaw를 맞춘다.
4. Cyan 화살표 `+X`를 NPC가 도착 후 바라볼 방향으로 둔다.
5. Editor에서 `P`를 눌러 시작점부터 Station까지 녹색 NavMesh가 이어지는지 본다.
6. 같은 역할 Station을 최소 2개, 권장 3개 이상 충분히 떨어뜨려 배치한다.
7. Actor Label을 `Station_역할_번호`로 정리한다. 번호는 관리용이며 방문 순서가 아니다.
8. PIE에서 중복 점유, 정지, 도착 방향, 반복 지점 편중을 확인한다.

세부 Offset, MG Operator Anchor, StateTree 시간과 검증 명령은 [`DRONE_SMART_OBJECT_ROUTE_EDITING_GUIDE.md`](../ai/DRONE_SMART_OBJECT_ROUTE_EDITING_GUIDE.md)를 따른다.

### 고정 순찰 순서가 필요할 때

현재 Actor Label을 `01`, `02`, `03`으로 바꿔도 순서대로 걷지 않는다. 고정 순서는 별도 기능으로 구현해야 한다.

권장 계약은 각 Station에 `RouteId`, `OrderIndex`, 선택적 `NextStation`을 두고, StateTree가 같은 Route의 다음 Index를 Claim하는 방식이다. Slot이 사용 중일 때는 `대기`, `건너뛰기`, `대체 Route` 중 정책을 Data로 선택해야 한다. 이 기능이 구현되기 전에는 번호를 실행 규칙처럼 사용하지 않는다.

## 6. Truck Route와 Smart Object를 함께 배치할 때

- Truck Spline은 도로 중앙, NPC Station은 보행 가능 가장자리나 엄폐 지점에 둔다.
- NPC Station과 차량 중심선 사이에 차량 반 폭, NPC Capsule 반경, 안전 여유를 합친 간격을 둔다.
- 횡단이 필요하면 교차 지점을 적게 만들고, 향후 차량 접근 감지·대기 규칙을 별도 구현한다.
- 차량형 무인포탑 `BP_AutoTurret_Vehicle`은 Smart Object가 아니다.
- NPC가 잡는 유인 포탑은 `BP_SO_MGTurret` 한 개뿐이다.
- 차량 Route 도착과 NPC Slot 도착은 서로 다른 Event다. Mission Director에서 필요한 목표만 각각 구독한다.

## 7. 팀 인계 체크리스트

### Truck

- [ ] 현재 직선 Greybox 시험인지, Mission Spline Route 작업인지 표시했다.
- [ ] Actor 시작 위치와 `+X` 진행 방향을 기록했다.
- [ ] 속도, 거리 또는 RouteId를 기록했다.
- [ ] 도로 Visibility Collision과 4점 접촉을 확인했다.
- [ ] 급경사·급커브·목적지 감속 구간을 화면에서 확인했다.
- [ ] 차량 포탑 부모 추종과 바퀴 방향을 확인했다.

### Smart Object

- [ ] Station 역할과 Activity가 맞다.
- [ ] Cyan 방향과 `P` NavMesh를 확인했다.
- [ ] 같은 Slot을 두 NPC가 동시에 쓰지 않는다.
- [ ] 번호가 고정 순서를 보장하지 않는다고 인계했다.
- [ ] 유인 MG와 무인 자동포탑을 구분했다.

### Git/Map

- [ ] 맵 담당자가 한 명인지 확인했다.
- [ ] 수정한 `.umap`과 Blueprint 목록을 팀원에게 알렸다.
- [ ] Production `Lvl_DroneTraining`을 실수로 저장하지 않았다.
- [ ] 미확인 화면 항목은 `Done`이 아니라 `수동 확인 대기`로 기록했다.

## 8. 다음 구현 순서

1. 맵 담당자가 안전한 TestMap에 Route와 Vehicle을 배치하고 곡선·경사 화면 확인
2. 곡률 감속·Look Ahead 조향과 장애물 정책 결정
3. 목적지 도착 Event를 Mission 2 시간/실패 규칙에 연결
4. 차량 파괴 시 Route 중단과 Story Fact 적용
5. 필요한 경우에만 Smart Object 고정 순서 Route를 별도 카드로 구현

차량 물리 세부 조정은 [`DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md`](DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md), Smart Object 전체 구조는 [`DRONE_SMART_OBJECT_NPC_GUIDE.md`](../ai/DRONE_SMART_OBJECT_NPC_GUIDE.md)를 참고한다.
