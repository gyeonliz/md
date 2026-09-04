# 무인 자동포탑 배치·조정 가이드

기준일: 2026-09-04 (Asia/Seoul)

## 현재 구현

자동포탑은 기존 유인 기관총의 3분할 구조와 발사 기능을 재사용한다.

```text
StationRoot
└─ MGTurretBaseMount
   ├─ MGTurretBaseMesh          고정 하단/장착판
   └─ MGTurretYawPivot          좌우 회전 몸체
      ├─ MGTurretBodyMesh
      └─ MGTurretAimPivot       상하 회전 포신
         ├─ MGTurretBarrelMesh
         └─ MGTurretMuzzle
```

- 설치형 BP: `/Game/Drone/AI/AutomaticTurrets/Blueprints/BP_AutoTurret_Emplaced`
- 차량형 BP: `/Game/Drone/AI/AutomaticTurrets/Blueprints/BP_AutoTurret_Vehicle`
- 시험 맵: `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`
- 설치형 배치: `AutoTurret_Emplaced_A`, 대략 `(2600, 1600, 0)`
- 차량형 배치: `AutoTurret_Vehicle_A`, 대략 `(2700, -2200, 120)`
- 차량 시험 부모: `AutoTurret_VehicleCarrier_Greybox` (`BP_GroundConformingVehicle_Greybox`)
- 차량 시험 노면: `VehicleRoughRoad_01`~`05`, Tag `DroneVehicleRoughRoad`

자동포탑은 Smart Object Slot을 쓰지 않는다. NPC가 접근해 잡는 유인 MG와 달리 살아 있는 Prototype Drone을 직접 검색하고, 탐지 거리와 Visibility 시야선을 통과한 가장 가까운 대상을 추적한다.

## Blueprint에서 조정할 값

BP를 열고 `Class Defaults`에서 다음 Category를 사용한다.

| Category | 값 | 역할 |
|---|---|---|
| `Drone > AI > Automatic Turret` | `Automatic Turret Enabled` | 자동 탐지·조준 전체 켜기/끄기 |
| `... > Detection` | `Detection Range` | 새 Drone을 처음 잡는 거리 |
| `... > Detection` | `Lose Target Range` | 이미 잡은 Drone을 놓는 거리. Detection보다 같거나 크게 유지 |
| `... > Detection` | `Target Scan Interval Seconds` | 표적 재검사 간격. 기본 0.2초 |
| `... > Detection` | `Require Target Line Of Sight` | 벽 뒤 표적 획득 금지. 기본 true |
| `Drone > AI > MG` | `MG Turret Range` | 실제 발사 가능 거리 |
| `Drone > AI > MG` | `MG Turret Cooldown Seconds` | 발사 간격 |
| `Drone > AI > MG` | `MG Turret Damage` | 한 발 피해량 |
| `... > Aim` | Yaw/Pitch 한계·보간·정렬 허용각 | 회전 범위와 추적 감각 |
| `... > Accuracy` | `MG Turret Spread Half Angle Degrees` | 탄 퍼짐 반각. 0이면 정확 사격 |
| `... > Projectile` | 탄환 사용·Class·Speed | 이동 탄환과 최종 Tracer BP 연결 |

탐지 거리는 실제 `MG Turret Range`보다 크게 만들지 않는 것을 기본으로 한다. 이탈 거리는 탐지 거리보다 크게 둬 경계에서 잡았다 놓는 현상을 줄인다.

## 차량 위에 연결하는 방법

권장 방식은 차량 Blueprint 안에 `Child Actor Component`를 만드는 것이다.

1. 차량 Skeletal/Static Mesh에 포탑 중심 Socket을 만들고 +X를 차량/포탑 전방, +Z를 위로 맞춘다.
2. 차량 Blueprint에 `Child Actor Component`를 추가한다.
3. Parent를 차량 Mesh의 해당 Socket으로 지정한다.
4. `Child Actor Class`를 `BP_AutoTurret_Vehicle`로 지정한다.
5. 상대 위치·회전은 Socket에서 맞추고 Actor Scale은 가능하면 `(1,1,1)`을 유지한다.
6. 포신 끝에 `MGTurretMuzzle`이 오도록 Barrel Mesh 상대 위치를 조정한다.

레벨에 차량과 포탑을 각각 배치한다면 World Outliner에서 포탑을 차량 아래로 Attach해도 된다. 현재 시험 맵의 `AutoTurret_Vehicle_A`는 `AutoTurret_VehicleCarrier_Greybox`의 `TurretMount` Component에 붙어 있다. 차량이 4점 Trace로 굴곡 노면을 따라 이동·Pitch·Roll하면 포탑 전체가 같이 움직이고, Yaw/Pitch는 그 부모 Transform 안에서 계속 로컬 회전한다. 차량 세부 조정은 [`DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md`](DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md)를 따른다.

## 최종 포탑 메시 교체

각 BP에서 상속 Component를 선택해 Static Mesh와 상대 Transform만 바꾼다.

- 고정 하단 또는 차량 장착판 → `MGTurretBaseMesh`
- 좌우로 회전할 포탑 몸체 → `MGTurretBodyMesh`
- 상하로 회전할 포신 → `MGTurretBarrelMesh`

원본 Mesh 축이 +X 전방이 아니면 Mesh Component의 상대 회전으로만 보정한다. `MGTurretYawPivot`, `MGTurretAimPivot`, `MGTurretMuzzle`의 계층을 바꾸지 않는다. 충돌은 별도 간단 Collision Component로 만들고 임시 시각 Mesh에 복잡한 물리 충돌을 바로 켜지 않는다.

## 수동 확인 순서

1. `Lvl_NPCSmartObjectGreybox`를 열고 Play한다.
2. 시작 위치에서는 우측 끝 포탑이 사거리 밖이라 불필요하게 발사하지 않는지 본다.
3. 맵 우측의 설치형 `(2600,1600)` 또는 차량형 `(2600,-1600)`으로 접근한다.
4. 고정 Base는 돌지 않고 Body만 좌우 Yaw, Barrel만 상하 Pitch로 Drone을 따라오는지 본다.
5. 포신이 목표에 정렬된 뒤 이동 Projectile을 발사하는지 본다.
6. 구조물 뒤로 숨었을 때 다음 Scan에서 추적·발사가 멈추는지 본다.
7. 다시 시야에 들어오면 재획득하는지, 사거리 밖으로 나가면 놓는지 본다.
8. 차량 Carrier가 다섯 개 굴곡 노면을 왕복할 때 차체 Pitch·Roll과 차량형 포탑의 위치·기준 방향이 함께 바뀌는지 본다.
9. PIE를 종료했을 때 Editor가 정상 상태로 돌아오는지 확인한다.

보고 형식:

`설치형 탐지/회전/발사 ○○, 차량형 탐지/회전/발사 ○○, 장애물 차단 ○○, 차량 부모 추종 ○○, 종료 정상/이상`

## 아직 구현하지 않은 범위

- Hostile/Friendly 진영 판정과 여러 표적 우선순위
- 포탑 체력, 피격, 파괴, 수리
- 실제 Chaos 차량 물리·타이어 접지·브레이크·네트워크 동기화. 현재는 4점 Trace 기반 Greybox 지면 추종만 구현
- 탄약·재장전·과열
- 최종 Mesh, Animation, Muzzle Flash, Sound, Niagara, 피격 표현
- 재밍에 따른 탐지거리 축소·표적 상실·오조준

다음 전투 확장은 `진영 필터 → 표적 우선순위 → 포탑 체력/파괴 → 재밍 인터페이스 → 최종 에셋/FX` 순서가 안전하다.
