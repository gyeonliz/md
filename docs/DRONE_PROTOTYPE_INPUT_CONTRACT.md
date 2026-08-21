# Drone Prototype 입력 계약

기준일: 2026-08-21 (Asia/Seoul)

이 문서는 구매 에셋 없이 Flight 기능을 시험하기 위한 **확정된 v1 Prototype 조작 계약**이다. Camera 소유와 장치별 역할은 승인됐으며 감도·반전·최종 물리 수치만 Greybox 체감 결과에 따라 조정한다.

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
| `IA_DronePrototype_Look` | Axis2D | `Mouse XY 2D-Axis` | 없음 | X=기체 Yaw, Y=CameraBoom Pitch |
| `IA_DronePrototype_Move` | Axis2D | Gamepad Left X | Dead Zone | 기체 좌·우 |
|  |  | Gamepad Left Y | Dead Zone → Swizzle `YXZ` | 기체 전·후 |
| `IA_DronePrototype_Altitude` | Axis1D | Gamepad `RT` | 없음 | World Up |
|  |  | Gamepad `LT` | Negate X | World Down |
| `IA_DronePrototype_Yaw` | Axis1D | Gamepad Right X | Dead Zone | 기체 Yaw Rate |
| `IA_DronePrototype_CameraPitchRate` | Axis1D | Gamepad Right Y | Dead Zone | CameraBoom Pitch Rate |

전용 Mapping Context 이름은 `IMC_DronePrototype`이고 우선순위는 C++ 기본값 `1`을 사용한다. Keyboard/Mouse에는 별도 Trigger나 Dead Zone을 추가하지 않고 Gamepad Stick에는 기본 `0.2` Dead Zone을 적용한다.

## 2. 현재 C++과의 연결

- Move의 Y는 `GetActorForwardVector()`, X는 `GetActorRightVector()`에 전달된다.
- Altitude는 기체 기울기와 무관하게 `FVector::UpVector`에 전달된다.
- Keyboard/Gamepad Yaw는 Delta Seconds와 `90°/s` 시험 Rate로 Pawn 자체를 회전한다.
- Mouse X는 입력 Delta에 감도를 적용해 Pawn Yaw를 직접 회전한다.
- Mouse Y와 Gamepad Right Y는 SpringArm의 상대 Pitch만 `-70°~20°` 범위에서 조정한다.
- SpringArm은 Controller Rotation을 사용하지 않고 Drone Actor Yaw를 따라간다.
- Blueprint Event Graph에서는 Mapping Context 추가나 동일 Action 재바인딩을 하지 않는다. `ADronePrototypePawn::PawnClientRestart()`가 자기 Context만 한 번 등록하고 수명주기에 맞춰 제거한다.

## 3. PIE에서 결정할 항목

Mouse Y는 Controller Pitch를 사용하지 않고 CameraBoom Pitch를 직접 조정한다. PFN-06 수동 확인에서는 현재 부호와 감도를 바꾸지 않고 체감 결과만 기록한다. 이후 조정할 때는 다음 원칙을 사용한다.

- Mouse Up이 Camera Up이면 Look Mapping에 Modifier를 추가하지 않는다.
- 반대이면 C++과 IMC 중 한 곳에서만 **Y축**을 반전한다.

C++와 IMC 양쪽에서 동시에 반전하지 않는다.

## 4. PFN-06 통과 기준

Editor lifecycle을 포함한 새 PIE 3회 자동화와 별도 수동 화면 확인 1회를 모두 통과해야 한다. 중복을 막기 위해 상세 항목과 실행별 결과는 [`DRONE_PROTOTYPE_PIE_CHECKLIST.md`](DRONE_PROTOTYPE_PIE_CHECKLIST.md)만을 단일 기준으로 사용한다.

## 5. 현재 미정

- 최종 키 배치와 사용자 재매핑
- Mouse Y 반전 기본값과 Look 감도
- Gamepad Stick 감도와 Response Curve
- 범용 조종기 입력
- 최종 비행 물리와 자동 수평 유지
- 멀티플레이 입력·이동 권한 구조

## 6. 현재 검증 상태

- 자산 재로드 검증에서 5개 Action의 Value Type과 IMC의 15개 Mapping·Modifier 순서를 확인했다.
- Mouse X Drone Yaw, Mouse Y CameraBoom Pitch, Gamepad 6축을 포함한 lifecycle 자동화가 새 PIE 3회를 통과했다.
- 전체 Automation Report는 3 succeeded, 0 warnings, 0 errors다.
- 사전 부분 확인 두 번은 모두 전체 조건을 끝내지 않아 Pass로 산정하지 않았다.
- PFN-06 자동화 3/3과 Standalone Keyboard·Mouse 수동 조작, 창 닫기 정상 종료가 통과해 Done이다. 실제 Gamepad 체감은 장치 연결 여부 미보고로 미확인이다. 정식 판정은 [`DRONE_PROTOTYPE_PIE_CHECKLIST.md`](DRONE_PROTOTYPE_PIE_CHECKLIST.md)를 따른다.
