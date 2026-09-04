# Drone MG 기관총 3분할 연결 가이드

기준일: 2026-09-04 (Asia/Seoul)

상태: MG 전용 C++ Class·임시 원기둥 3분할·자동화 완료, 화면 확인과 최종 Asset 교체 대기

## 1. 확정 구조

기관총과 NPC 몸 회전을 분리한다.

```text
StationRoot
└─ MGTurretBaseMount       고정 하단부
   ├─ MGTurretBaseMesh     고정 원기둥
   └─ MGTurretYawPivot     좌우 회전 몸체
      ├─ MGTurretBodyMesh  Yaw 원기둥
      ├─ MGTurretOperatorAnchor  몸체와 함께 도는 사수 후방 위치·방향
      └─ MGTurretAimPivot  상하 회전 포신(Pitch, 기존 이름 호환)
         ├─ MGTurretBarrelMesh  Pitch 원기둥
         └─ MGTurretMuzzle 발사 위치
```

- 이 계층은 `ADroneMGTurretStation`과 이를 직접 부모로 쓰는 `BP_SO_MGTurret`에만 존재한다.
- Patrol·Ambient·Cover 등 일반 `ADroneSmartObjectStation`에는 포탑 Pivot이나 Mesh가 없다.
- Smart Object Slot은 검색·한 명 점유 계약에 사용하고, 실제 MG 사수 위치·몸 방향은 `MGTurretOperatorAnchor`가 담당한다.
- `MGTurretOperatorAnchor`는 `MGTurretYawPivot`의 자식이다. 몸체가 Yaw 회전하면 사수의 후방 위치와 몸 방향도 같은 회전을 직접 상속한다.
- 별도의 사수 Yaw 보정값은 두지 않는다. NPC 고개는 AnimBP Gaze로 Drone 방향을 보조한다.
- 기관총 몸체는 `MGTurretYawPivot`, 포신은 `MGTurretAimPivot`만 따라간다.
- 사격은 현재 포신 방향과 목표 방향의 오차가 기본 `4°` 이하일 때 시작한다.
- `BP_SO_MGTurret`은 전용 부모로 이관됐고, 예전 저장 Attachment는 `OnConstruction`에서 위 계층으로 복구한다.

현재 임시 모양은 Engine `/Engine/BasicShapes/Cylinder` 3개다.

| Component | 상대 위치 | 상대 회전 | 상대 Scale | 결과 역할 |
|---|---|---|---|---|
| `MGTurretBaseMesh` | `(0, 0, 20)` | `(0, 0, 0)` | `(0.65, 0.65, 0.40)` | 바닥 고정 받침 |
| `MGTurretBodyMesh` | `(0, 0, 0)` | `(0, 0, 0)` | `(0.45, 0.45, 0.35)` | 좌우 회전 몸체 |
| `MGTurretBarrelMesh` | `(55, 0, 0)` | Pitch `90°` | `(0.12, 0.12, 1.10)` | +X를 향하는 상하 포신 |

## 2. 3분할 에셋 제작 규칙

세 Mesh를 다음 단위로 준비한다.

| Mesh | 포함 범위 | Pivot 기준 |
|---|---|---|
| Base | 삼각대·고정판·지면 고정부 | 바닥 중심, 회전하지 않음 |
| Body | 좌우로 도는 포탑 몸체·손잡이 지지부 | Yaw 회전 중심 |
| Barrel | 총열·총구·상하 가동부 | Pitch 회전축 중심 |

공통 규칙은 Unreal `cm`, 정면 `+X`, 위 `+Z`다. Body와 Barrel의 원점이 실제 회전축과 다르면 Blueprint에서 Mesh 상대 위치로 맞추되 Pivot Component 자체에 임의의 회전을 섞지 않는다. 총구는 `MGTurretMuzzle`을 포신 끝에 배치한다.

## 3. Blueprint 확인·최종 Asset 교체

대상은 `/Game/Drone/AI/SmartObjects/Blueprints/BP_SO_MGTurret`다.

1. Blueprint의 Parent Class가 `DroneMGTurretStation`인지 확인한다.
2. Components에서 상속된 `MGTurretBaseMount`, `MGTurretOperatorAnchor`, `MGTurretYawPivot`, `MGTurretAimPivot`, `MGTurretMuzzle`을 확인한다.
3. 상속된 `MGTurretBaseMesh`, `MGTurretBodyMesh`, `MGTurretBarrelMesh` 세 개를 확인한다. 새 Mesh Component를 추가하지 않는다.
4. 최종 Base/Body/Barrel Asset이 준비되면 대응 Component의 `Static Mesh`를 원기둥에서 최종 Mesh로 바꾼다.
5. 원점이 실제 회전축과 다르면 각 Mesh의 상대 Location·Rotation·Scale만 조정한다. Pivot Component 계층은 바꾸지 않는다.
6. `MGTurretMuzzle`을 실제 Barrel 총구 끝으로 이동한다. 이 Component의 +X가 발사 방향이다.
7. Smart Object Slot과 Cyan 화살표는 검색·예약 기준으로 유지한다. 실제 사수 위치는 초록 `MGTurretOperatorAnchor`이며 아래 Operator 값을 조정한다. 포탑 조준 Pivot과 섞지 않는다.

## 4. 사수 위치·조준값 조정 위치

`BP_SO_MGTurret`의 Class Defaults에서 `Drone > AI > MG > Operator`를 조정한다.

| 값 | 기본값 | 용도 |
|---|---:|---|
| Operator Distance | `120 cm` | 포탑 중심에서 뒤쪽으로 떨어지는 거리 |
| Operator Lateral Offset | `0 cm` | 포탑 기준 좌우 위치, `+`는 오른쪽 |
| Operator Vertical Offset | `0 cm` | 사수 발 위치 높이 보정 |

초록 `MGTurretOperatorAnchor` 화살표가 사수의 몸 정면이다. 이 화살표와 위치는 `MGTurretYawPivot`을 그대로 따라가므로 회전값을 따로 맞추지 않는다. 손·발 위치가 어색하면 Distance, Lateral, Vertical 세 위치값만 조정한다.

`BP_SO_MGTurret`의 Class Defaults에서 `Drone > AI > MG > Aim`을 조정한다.

| 값 | 기본값 | 용도 |
|---|---:|---|
| Max Yaw | `180°` | Base 정면 기준 좌우 한계 |
| Max Pitch Up | `60°` | 공중 Drone을 올려보는 한계 |
| Max Pitch Down | `25°` | 아래 방향 한계 |
| Aim Interpolation Speed | `8.0` | 포탑 추적 속도 |
| Fire Alignment Tolerance | `4°` | 이 각도 안에서만 발사 |

사거리·Cooldown·Damage·Muzzle Offset·Spread·Projectile Speed는 기존 `Drone > AI > MG` 항목을 사용한다. 난이도 조정과 Mesh 축 보정을 한 번에 바꾸지 말고, 먼저 Mesh가 정확히 +X를 보는지 확인한 뒤 수치를 조정한다.

## 5. 수동 확인

`/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`에서 다음 순서로 본다.

1. Rifle Hostile이 MG에 도착한 뒤 초록 Operator Anchor 위치에 붙는지 확인한다.
2. 원기둥이 정확히 세 개이고 다른 Patrol·Ambient·Cover Station에는 원기둥 포탑이 생기지 않았는지 본다.
3. Drone을 좌우로 움직여 Base 원기둥은 고정되고 Body 원기둥이 Yaw 회전할 때 사수도 몸체 뒤를 유지하며 같은 방향으로 함께 도는지 본다.
4. Drone을 위아래로 움직여 Barrel 원기둥과 Muzzle만 Pitch 회전하는지 본다.
5. 포탑이 목표 방향에 도착하기 전에 탄이 옆으로 발사되지 않는지 본다.
6. 사수 고개는 Drone을 따라가되 몸과 기관총 Transform을 덮어쓰지 않는지 본다.
7. 사수 사망 뒤 다음 MG 가능 NPC가 같은 Slot을 점유하고 포탑 조준을 이어가는지 본다.
8. 거리·좌우·높이가 어색하면 `BP_SO_MGTurret > Class Defaults > Drone|AI|MG|Operator`의 세 위치값만 조정하고 Smart Object Slot, 회전 Pivot, 별도 Yaw 값은 만들지 않는다.

통과 기록 형식:

```text
원기둥 3개만 표시, 일반 Station 영향 없음, 사수가 Body 회전을 따라 후방 위치·방향 유지,
Base 고정, Body Yaw 정상, Barrel Pitch 정상, Muzzle 방향 정상, 정렬 후 발사 정상,
NPC 몸/고개/포탑 간섭 없음, 사망 교대 정상
```
