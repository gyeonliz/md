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

- 이 계층은 ADroneMGTurretStation 계열(BP_SO_MGTurret, BP_AutoTurret_Emplaced/Vehicle)에 있고 일반 ADroneSmartObjectStation에는 없다.
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

`/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`에서 다음 순서로 본다.

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

## 6. 패트리어트 미사일 포대: 접합부 회전축 조정

대상 Blueprint는 `/Game/Drone/AI/Blueprints/Turrets/BP_PatriotMissileLauncher`다. 기존 MG·Smart Object와 별개의 **Actor Blueprint**이며, 이 절은 현재 조정 방법을 설명한다. 생성·저장·재로드 회전 검사와 수동 외형 확인을 구분한 근거는 [STATUS](../../STATUS.md)와 [WORKLOG](../history/DRONE_WORKLOG.md)를 확인한다.

### 6.1. 원본 메시 대신 Scene Component를 회전축으로 사용

원본 세 메시의 원점이 전체 포대 하단에 있으므로 메시 자체를 회전시키면 접합부가 아니라 하단을 중심으로 크게 돌 수 있다. 원본 `/Game/Item/missile/Missile_Lower`, `Missile_Middle`, `Missile_Upper`는 수정하지 않고, 접합부에 배치한 별도 Scene Component를 회전시킨다.

```text
FixedSceneRoot             포대 전체 위치·방향·크기
├─ LowerMesh               고정 하단부
└─ YawPivot                하단/중단 접합부, 좌우 회전축
   ├─ MiddleMesh           좌우로 도는 중단부
   └─ PitchPivot           중단/상단 접합부, 상하 회전축
      └─ UpperMesh         상하로 도는 발사부
```

아래는 생성 도구의 상대 Location 초기값이다. 이후 BP가 편집·재저장됐으므로 **현재 BP Details를 우선**하며 이 표로 기존 조정을 덮어쓰지 않는다. 생성 당시 단위는 `cm`, 상대 Rotation은 모두 `0`, Scale은 모두 `1`이다. 현재 저장본 검증 범위는 STATUS/WORKLOG를 따른다.

| Component | 부모 | 상대 Location (X, Y, Z) | 연결할 Static Mesh |
|---|---|---|---|
| `LowerMesh` | `FixedSceneRoot` | `(0, 0, 0)` | `/Game/Item/missile/Missile_Lower` |
| `YawPivot` | `FixedSceneRoot` | `(0.315, -4.35, 13.33)` | 없음: Scene Component |
| `MiddleMesh` | `YawPivot` | `(-0.315, 4.35, -13.33)` | `/Game/Item/missile/Missile_Middle` |
| `PitchPivot` | `YawPivot` | `(-0.315, -7.15, 47.07)` | 없음: Scene Component |
| `UpperMesh` | `PitchPivot` | `(0, 11.50, -60.40)` | `/Game/Item/missile/Missile_Upper` |

회전축을 접합부로 옮긴 만큼 자식 메시를 반대 방향으로 보정해 원래 조립 위치를 유지하는 방식이다. 접합부 초기값은 메시 받침과 몸체 어깨 형상을 기준으로 잡은 값이므로, 최종 외형에서 이음새를 보며 소폭 조정한다. 메시 원점을 영구 변경하거나 원본 에셋을 다시 저장할 필요는 없다.

### 6.2. Blueprint에서 좌우·상하 움직이기

1. 좌우 회전: `YawPivot`을 그래프로 가져와 `Set Relative Rotation`에 연결한다. `Make Rotator`의 **Yaw / Z**만 변경한다.
2. 상하 회전: `PitchPivot`을 가져와 `Set Relative Rotation`에 연결한다. 이 에셋은 발사부 길이 방향이 Y이므로 **Roll / X**만 변경한다. 이름이 `PitchPivot`이어도 `Make Rotator`의 Pitch / Y로 회전시키지 않는다.
3. 메시 Component나 Actor 전체에 조준 회전을 넣지 않는다. Actor Rotation은 포대 설치 방향, 두 Pivot의 상대 Rotation은 포대 가동에만 사용한다.
4. 순차 조준이 필요하면 현재 상대 Rotation에서 목표 Rotation으로 보간한 결과를 위 노드에 연결한다. 회전 한계·속도·입력·추적 로직은 별도로 설계하며 이 조립 기준에 포함하지 않는다.

편집기에서만 자세를 잡을 때도 Components에서 해당 Pivot을 선택하고 Details의 상대 Rotation을 조정한다. 원본 발사부가 향하는 `+Y` 기준으로 Roll을 음수로 바꾸면 올리고, 양수로 바꾸면 내리는 방향이다. 설치 방향에 따라 화면에서 보이는 방향은 달라지므로 작은 각도로 먼저 확인한다.

### 6.3. 접합부 위치·크기·머터리얼 바꾸기

축 위치를 조정할 때는 먼저 두 Pivot Rotation을 `0`으로 돌려놓는다. 아래 보정은 이 기본 조립 자세에서 적용한다.

| 변경 | 함께 보정할 위치 | 이유 |
|---|---|---|
| `YawPivot` Location에 `Δ` 더하기 | `MiddleMesh`와 `PitchPivot` Location에서 각각 같은 `Δ` 빼기 | 조립된 중단·상단의 위치는 유지하고 좌우 축만 옮김 |
| `PitchPivot` Location에 `Δ` 더하기 | `UpperMesh` Location에서 같은 `Δ` 빼기 | 상단 위치는 유지하고 상하 축만 옮김 |

예를 들어 상하 축을 기본 자세 기준 Z로 `2 cm` 높이면 `PitchPivot.Z`에 `2`를 더하고 `UpperMesh.Z`에서 `2`를 뺀다. Pivot만 옮기면 메시 전체가 따라 이동하므로 반드시 짝으로 보정한다.

- 전체 크기: 원본 조립 크기는 대략 `1 m`다. 맵에 놓은 **Actor 전체 Scale**로 크기를 조정한다. 메시마다 서로 다른 Scale을 주면 이음새와 축 위치가 틀어질 수 있다.
- 머터리얼: 각 Mesh Component의 `Materials > Element 0`에 `/Game/Item/missile/Missile_M`을 지정한다. Blueprint Component의 오버라이드로 연결하고 원본 Static Mesh 머터리얼은 수정하지 않는다.
- 원본 메시 교체: 대응하는 세 Mesh Component의 `Static Mesh`에서 바꾼다. 새 메시가 같은 공통 조립 좌표를 사용하는지 먼저 확인하고, 다르면 위 상대 위치 보정을 다시 맞춘다.

### 6.4. 수동 외형 확인

TestMap에 별도로 배치한 후 다음을 확인한다. 기존 MG나 팀원 Production Training 맵을 이 시험 때문에 변경하지 않는다.

1. 두 축이 `0°`일 때 세 메시가 원래 조립 위치로 맞물리는지 본다.
2. `YawPivot`을 `-90° / +90°`로 돌려 Lower는 고정되고 Middle·Upper만 하단 접합부를 중심으로 도는지 본다.
3. `PitchPivot`의 **Roll**을 작은 각도부터 `-30° / +30°`로 바꿔 Upper만 상단 접합부를 중심으로 움직이는지 본다.
4. 좌우·상하를 동시에 바꿔도 접합부가 벌어지거나 전체 하단을 중심으로 공전하지 않는지 본다.
5. 전체 Actor Scale을 바꿔도 조립 간격과 축 위치가 함께 유지되는지 본다.

이 Blueprint 범위는 **메시 조립·회전축·머터리얼 연결**이다. AI 인식·조준, 미사일 발사, 조작 입력, 충돌·물리, 네트워크, 차량 부착이나 맵 배치 기능을 구현 완료로 간주하지 않는다.
