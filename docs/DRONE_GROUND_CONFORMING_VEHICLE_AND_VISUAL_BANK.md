# 4점 지면 추종 차량·Drone 외형 기울기 가이드

기준일: 2026-09-04 (Asia/Seoul)

## 구현 범위

이번 구현은 완전한 Chaos Vehicle 물리가 아니라 Greybox 검증용 `4점 지면 추종`이다. 차량 앞좌·앞우·뒤좌·뒤우 네 지점에서 아래로 Visibility Trace를 쏘고, 접촉점이 세 개 이상이면 지면 높이와 경사에 맞춰 Actor의 Z·Pitch·Roll을 보간한다.

- Native Class: `/Script/Drone.DroneGroundConformingVehicle`
- Blueprint: `/Game/Drone/Vehicles/Blueprints/BP_GroundConformingVehicle_Greybox`
- 시험 Map: `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`
- 배치 Actor: `AutoTurret_VehicleCarrier_Greybox`
- 시험 노면: `VehicleRoughRoad_01`~`05`, 공통 Tag `DroneVehicleRoughRoad`
- 차량 포탑: `AutoTurret_Vehicle_A`, 차량의 `TurretMount`에 Attach

차량은 Query 전용 Box Collision, 임시 Cube Body, Cylinder Wheel 네 개와 `TurretMount`를 가진다. 완전한 질량·타이어 마찰·스프링 힘을 계산하지 않고 지형에 맞는 차체 자세와 탑재 포탑 추종을 먼저 검증한다.

## Blueprint 조정값

`BP_GroundConformingVehicle_Greybox > Class Defaults`에서 다음 값을 조정한다.

| Category | 기본값 | 역할 |
|---|---:|---|
| `Drone > Vehicle > Suspension > Half Wheelbase` | 110 cm | 차량 중심에서 앞/뒤 Trace까지 거리 |
| `... > Half Track Width` | 78 cm | 차량 중심에서 좌/우 Trace까지 거리 |
| `... > Trace Start Height` | 160 cm | Trace 시작 높이 |
| `... > Trace Length` | 420 cm | 아래 방향 탐색 길이 |
| `... > Ride Height` | 72 cm | 접촉면 위 차체 중심 높이 |
| `... > Wheel Radius` | 30 cm | 임시 바퀴 외형과 접지 보정 기준 |
| `... > Maximum Ground Angle Degrees` | 28° | Pitch·Roll 최대 제한 |
| `... > Height Interpolation Speed` | 10 | 높이 추종 속도 |
| `... > Rotation Interpolation Speed` | 8 | 경사 회전 추종 속도 |
| `Drone > Vehicle > Drive > Maximum Drive Speed` | 360 cm/s | 수동 Throttle 최대 속도 |
| `... > Maximum Turn Rate Degrees Per Second` | 45°/s | 수동 Steering 최대 회전 속도 |
| `... > Wheel Visual Spin Direction Multiplier` | +1 | 수동 화면 확인으로 확정한 현재 Greybox Cylinder의 전진 구름 방향. 최종 Wheel Mesh 축이 반대면 `-1`로 변경 |
| `Drone > Vehicle > Greybox > Greybox Auto Drive Enabled` | Map 배치만 켬 | Controller 없이 시험 왕복 주행 |
| `... > Greybox Auto Drive Speed` | 220 cm/s | 시험 주행 속도 |
| `... > Greybox Auto Drive Distance` | 1050 cm | 시작점 기준 왕복 거리 |

실제 차량 Mesh로 바꿀 때 먼저 바퀴 중심에 맞게 `Half Wheelbase`, `Half Track Width`, `Wheel Radius`, `Ride Height`를 조정한다. 그 뒤 Trace 길이와 보간 속도를 바꾸며, 차체 Mesh 자체의 원본 축이나 높이는 `VehicleBodyMesh` 상대 Transform으로 맞춘다.

`SetDriveInput(Throttle, Steering)`은 각 입력을 `-1~1`로 받는다. Map의 자동 왕복 주행이 켜져 있으면 수동 입력은 무시된다. 실제 차량 Controller·Waypoint 이동을 붙일 때는 자동 주행을 끄고 이 함수만 호출한다.

### 바퀴 회전

네 바퀴는 `Throttle × 최대속도` 표시값을 그대로 회전속도로 사용하지 않는다. 매 Tick의 실제 Actor 이동거리를 차량 전진축에 투영하고 `이동거리 / WheelRadius`로 회전각을 계산한다. 따라서 반속에서는 회전속도도 절반이 되고, 후진하면 누적각이 반대로 감소하며 지면 추종으로 Z가 바뀌어도 수평 이동거리 기준 회전은 유지된다.

- `GetCurrentForwardSpeedCentimetersPerSecond`: 실제 전진축 속도, 후진은 음수
- `GetCurrentWheelRotationDegrees`: 이동거리로 누적한 회전각, 전진 증가·후진 감소
- 최종 Wheel Mesh 교체 시 `WheelRadius`를 실제 반지름으로 맞추고 회전축이 반대일 때만 `Wheel Visual Spin Direction Multiplier`를 `-1 ↔ 1`로 바꾼다.
- 2026-09-04 첫 수동 화면 확인에서 기본 `-1` 방향이 반대로 굴러 `+1`로 수정했다. 동일 Greybox Mesh에서는 `+1`을 기준으로 사용한다.
- 현재 Greybox는 네 바퀴에 같은 구름 회전각을 사용하며 조향각·좌우 차동속도는 아직 포함하지 않는다.

## 차량형 자동포탑 연결

현재 `AutoTurret_Vehicle_A`는 차량의 `TurretMount` Component에 붙어 있다. 따라서 차체가 경사에 맞춰 Pitch·Roll하고 이동하면 포탑 전체가 같은 Transform을 따라가며, 포탑 내부의 Body Yaw와 Barrel Pitch는 그 로컬 기준 안에서 Drone을 계속 조준한다.

최종 차량 Blueprint에서는 다음 중 하나를 사용한다.

1. 차량 Mesh에 포탑 Socket을 만들고 `BP_AutoTurret_Vehicle` Child Actor를 Socket에 연결한다.
2. 현재 Native `TurretMount` 위치를 최종 지붕 위치로 조정한 뒤 포탑 Actor를 Attach한다.

포탑의 `MGTurretYawPivot`, `MGTurretAimPivot`, `MGTurretMuzzle` 계층은 바꾸지 않는다.

## Drone 전후·좌우 이동 외형 기울기

`ADronePrototypePawn`의 `VisualTiltPivot`은 전후 입력을 외형 Pitch, 좌우 입력을 외형 Roll에 사용한다. 실제 Collision과 CameraBoom은 기울이지 않는다.

- 전진 입력: 외형 Pitch `-14°` 방향(기수 아래)
- 후진 입력: 외형 Pitch `+14°` 방향(기수 위)
- 오른쪽 입력: 외형 Roll `+18°` 방향
- 왼쪽 입력: 외형 Roll `-18°` 방향
- 입력 중 보간 속도: `7`
- 입력 해제 복귀 속도: `5`
- 적용 대상: 기본 Drone Visual Mesh와 FPV Integration의 Body·Rotor 네 개
- 제외 대상: Camera, Collision, 또는 Component Tag `DroneNoVisualBank`가 붙은 Mesh

값은 `BP_DronePrototypePawn` 또는 파생 BP의 `Prototype > VisualBank`에서 조정한다. `Maximum Visual Tilt Pitch Degrees`는 전후 최대각, `Maximum Visual Bank Roll Degrees`는 좌우 최대각이다. 외형만 기울기 때문에 조작 방향, 충돌 체적, 카메라 수평선은 기존 계약을 유지한다. 최종 비행 감각에서는 가속량 기반 기울기와 속도별 제한을 별도 카드로 확장한다.

## Drone 1인칭·3인칭 전환

`P`를 누르면 같은 FollowCamera를 3인칭 추적 모드와 1인칭 FPV 모드로 전환한다. 별도 Camera를 중복 생성하지 않는다.

- 입력 액션: `/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_ToggleView`
- Mapping: `IMC_DronePrototype`의 `P` 1개, 전체 Mapping 16개
- 3인칭: CameraBoom이 Collision Root에 연결되고 기본 Arm Length `500 cm`를 사용한다. 이동 외형 Pitch·Roll은 화면을 기울이지 않는다.
- 1인칭: CameraBoom이 `VisualTiltPivot`에 연결되고 Arm Length `0`, 기본 Offset `(X=70,Y=0,Z=12) cm`를 사용한다. 따라서 W/S Pitch, A/D Roll, 복합 입력과 본체 피격 회전을 Camera가 함께 따른다.
- Mouse Y와 Gamepad 우측 Stick Y의 Camera Pitch는 기존 CameraBoom 회전을 그대로 사용하므로 두 모드에서 유지된다.
- 조정 위치: 파생 Pawn BP의 `Prototype > Camera`에서 `Third Person Camera Arm Length`, `Third Person Camera Boom Offset`, `First Person Camera Boom Offset`을 변경한다.

## Drone 피격 흔들림

Drone의 공용 `HealthComponent`에서 실제 피해가 적용될 때 본체와 Camera View에 짧은 감쇠 흔들림을 준다. Actor 위치·Collision·이동 속도에는 힘이나 회전을 적용하지 않으므로 피격 표현 때문에 조작 판정이 바뀌지 않는다.

`BP_DronePrototypePawn` 또는 파생 BP의 `Prototype > DamageShake`에서 조정한다.

| 값 | 기본값 | 역할 |
|---|---:|---|
| `Damage Shake Enabled` | true | 피격 흔들림 전체 사용 |
| `Damage Shake Duration Seconds` | 0.30초 | 한 번 피격된 뒤 감쇠 시간 |
| `Damage For Maximum Shake` | 25 Damage | 최대 강도에 도달하는 피해량 |
| `Minimum Damage Shake Scale` | 0.25 | 작은 피해도 보이게 하는 최소 강도 |
| `Damage Shake Visual Rotation Degrees` | 6° | 본체 최대 회전 흔들림 |
| `Damage Shake Camera Location Centimeters` | 5 cm | Camera View 위치 흔들림 |
| `Damage Shake Camera Rotation Degrees` | 1.5° | Camera View 회전 흔들림 |
| `Damage Shake Oscillations Per Second` | 18 | 흔들림 주파수 |

기존 Blueprint용 `OnHealthChanged`는 그대로 유지하고 C++ 표현 수신을 별도 Native Event로 연결했다. 따라서 Rifle·Shotgun·MG·자동포탑·환경 피해가 같은 Health 진입점을 쓰면 무기별 중복 구현 없이 흔들린다. 연속 피격은 시간을 다시 0.30초로 시작하고 현재보다 강한 피해가 들어오면 강도를 올린다.

현재 Any Damage 계약에는 정확한 충돌 방향이 없으므로 흔들림은 방향성이 없는 Greybox 반응이다. 탄착 방향별 반동, Gamepad 진동, HUD 적색 점멸, Sound·Niagara는 후속 표현 범위다.

## 수동 화면 확인

### 차량

1. `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`를 연다.
2. PIE 또는 Standalone으로 실행한다.
3. 맵의 `Y=-2200` 부근에서 차량이 다섯 개 굴곡 노면을 왕복하는지 본다.
4. 차체가 노면 높이에 따라 위아래로 움직이고 Pitch·Roll이 갑자기 튀지 않는지 본다.
5. 바퀴 네 개가 각 접촉 높이를 시각적으로 따라오는지 본다.
6. 차량 포탑 전체가 차체 이동·경사를 따라가면서 Body Yaw와 Barrel Pitch로 Drone을 추적하는지 본다.
7. 전진 중 네 바퀴가 같은 방향으로 구르고, 후진 전환 시 즉시 반대로 회전하는지 본다.
8. 빠른 구간의 바퀴 회전이 느린 구간보다 눈에 띄게 빠른지 본다.

### Drone

1. `/Game/Drone/Prototype/Maps/Lvl_DronePrototype` 또는 Training Map에서 Drone을 조종한다.
2. `W`를 누르면 기수가 아래로, `S`를 누르면 기수가 위로 기우는지 본다.
3. `D`를 누르면 본체와 Rotor 네 개가 오른쪽 이동 방향으로 기울고, `A`는 반대로 기우는지 본다.
4. `W+D` 같은 복합 입력에서는 Pitch와 Roll이 동시에 적용되는지 본다.
5. 키를 놓으면 부드럽게 수평으로 복귀하는지 본다.
6. 외형이 기울어도 카메라 수평선과 Collision 때문에 이동이 튀지 않는지 본다.
7. `P`를 누르면 1인칭으로 전환되고 다시 누르면 3인칭으로 돌아오는지 본다.
8. 1인칭에서 `W/S`, `A/D`, `W+D`를 입력하면 기체 기울기와 함께 화면도 Pitch·Roll하는지 본다.
9. 3인칭으로 돌아오면 화면 수평선은 다시 기체 외형 기울기를 따르지 않는지 본다.
10. 적 사격 또는 자동포탑 탄환에 맞았을 때 본체와 화면이 짧게 흔들리는지 본다.
11. 흔들리는 동안에도 조작과 Collision이 튀지 않고 약 0.3초 뒤 원래 카메라 상태로 돌아오는지 본다.

보고 형식:

`차량 4점 추종 ○○, 바퀴 속도비례/후진회전 ○○, 노면 Pitch/Roll ○○, 차량 포탑 추종 ○○, Drone W/S Pitch ○○, A/D Roll ○○, P 1/3인칭 전환 ○○, 1인칭 기울기 추종 ○○, 피격 본체/카메라 흔들림 ○○, 카메라/충돌 안정 ○○, 종료 정상/이상`

## 현재 한계

- 실제 스프링 힘, 댐퍼, 질량 이동, 타이어 접지·슬립, 구동륜·브레이크는 없다.
- 급격한 단차와 공중 상태는 완전한 차량 물리처럼 처리하지 않는다.
- 시험 노면은 Engine Cube 다섯 개의 Greybox이며 최종 도로 Mesh가 아니다.
- 실제 차량 AI/Waypoint, 장애물 회피, 네트워크 동기화는 아직 연결하지 않았다.
- Drone 기울기는 현재 조작 입력 기반 Pitch·Roll이며 실제 가속도·속도·관성 기반 기울기는 후속이다.
- 1인칭은 Greybox Offset이며 최종 Drone Cockpit/Camera Socket과 Mesh 가림 처리 전이다.
- 피격 흔들림은 현재 피해 방향을 구분하지 않고 Gamepad 진동·HUD Flash·Sound·Niagara를 포함하지 않는다.

완전한 차량 물리가 필요해지는 시점에는 이 계약을 폐기하지 않고, `TurretMount`와 외부 Drive API를 유지한 채 Chaos Vehicle 기반 구현으로 교체한다.
