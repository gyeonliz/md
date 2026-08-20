# Drone Prototype 입력 계약

기준일: 2026-08-19 (Asia/Seoul)

이 문서는 구매 에셋 없이 Flight 기능을 시험하기 위한 **임시 Prototype 입력 계약**이다. 최종 조작 방식의 승인이 아니며, Greybox 플레이 결과에 따라 바꿀 수 있다.

## 1. 현재 계약

| Input Action | Value Type | 키 | Mapping Modifier | Callback 기대값과 역할 |
|---|---|---|---|---|
| `IA_DronePrototype_Move` | Axis2D | `W` | Swizzle `YXZ` | `(X=0, Y=+1)`, 기체 Forward |
|  |  | `S` | Negate X → Swizzle `YXZ` | `(X=0, Y=-1)`, 기체 Backward |
|  |  | `A` | Negate X | `(X=-1, Y=0)`, 기체 Left |
|  |  | `D` | 없음 | `(X=+1, Y=0)`, 기체 Right |
| `IA_DronePrototype_Altitude` | Axis1D | `Space Bar` | 없음 | `+1`, World Up |
|  |  | `Left Ctrl` | Negate X | `-1`, World Down |
| `IA_DronePrototype_Yaw` | Axis1D | `E` | 없음 | `+1`, 기체 오른쪽 Yaw 후보 |
|  |  | `Q` | Negate X | `-1`, 기체 왼쪽 Yaw 후보 |
| `IA_DronePrototype_Look` | Axis2D | `Mouse XY 2D-Axis` | 우선 없음 | X=카메라 Yaw, Y=카메라 Pitch |

전용 Mapping Context 이름은 `IMC_DronePrototype`이고 우선순위는 C++ 기본값 `1`을 사용한다. 첫 기준선에는 Trigger, Scalar, Dead Zone을 추가하지 않는다.

## 2. 현재 C++과의 연결

- Move의 Y는 `GetActorForwardVector()`, X는 `GetActorRightVector()`에 전달된다.
- Altitude는 기체 기울기와 무관하게 `FVector::UpVector`에 전달된다.
- Yaw는 `AddActorLocalRotation()`으로 Pawn 자체를 회전한다.
- Look은 Controller Yaw/Pitch를 바꾸며, Control Rotation을 따르는 SpringArm 카메라에 적용된다.
- Blueprint Event Graph에서는 Mapping Context 추가나 동일 Action 재바인딩을 하지 않는다. `ADronePrototypePawn::PawnClientRestart()`가 자기 Context만 한 번 등록하고 수명주기에 맞춰 제거한다.

## 3. PIE에서 결정할 항목

Mouse Y는 `AddControllerPitchInput()`과 PlayerController의 Pitch Scale을 거친다. 다음 두 결과 중 하나를 실제 PIE에서 기록한다.

- Mouse Up이 Camera Up이면 Look Mapping에 Modifier를 추가하지 않는다.
- 반대이면 IMC의 Look Mapping에서 **Y축만** 반전한다.

C++와 IMC 양쪽에서 동시에 반전하지 않는다.

## 4. PFN-06 통과 기준

Editor를 새로 실행한 상태를 포함하여 PIE를 3회 반복한다. 매 실행에서 다음을 모두 확인해야 한다.

- `BP_DronePrototypePawn` 정확히 한 대가 Spawn되고 PlayerController에 Possess된다.
- `IMC_DronePrototype`이 중복 없이 한 번 적용된다.
- `W/S/A/D`, `Space/Left Ctrl`, `Q/E`, Mouse가 위 표의 방향으로 동작한다.
- 반대 키와 복합 이동을 입력해도 속도가 중복 누적되거나 Callback이 이중 전달되지 않는다.
- PIE 종료 후 다시 시작해도 입력 세기가 두 배가 되지 않는다.
- Mouse는 현재 Prototype에서 기체 Yaw가 아니라 카메라 Control Rotation만 바꾼다.

## 5. 현재 미정

- 최종 키 배치와 사용자 재매핑
- Mouse Y 반전 기본값과 Look 감도
- Actor-relative 또는 Camera-relative 수평 이동
- Gamepad 및 조종기 입력
- 최종 비행 물리와 자동 수평 유지
- 멀티플레이 입력·이동 권한 구조

## 6. 현재 검증 상태

- 자산 재로드 검증에서 네 Action의 Value Type과 IMC의 9개 Mapping·Modifier 순서를 확인했다.
- GUI PIE에서 IMC 한 개와 Move·Altitude·Yaw·Look Callback 계열의 실제 동작을 부분 확인했다. 첫 실행의 `S`와 복합·중복 조건은 미확인이다.
- Mouse Look은 기체 Yaw를 바꾸지 않고 카메라 Control Rotation만 변경했다.
- 두 번째 PIE도 일부만 확인하고 사용자 직접 조작 보호를 위해 중단했다.
- PFN-06은 0/3 Pass이며 새 PIE 3회 전체 반복과 재시작 뒤 입력 중복 없음 확인이 남았다.
