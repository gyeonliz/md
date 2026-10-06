# Drone Prototype 입력 계약

기준일: 2026-10-04 (Asia/Seoul)

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
| `IA_DronePrototype_ToggleView` | Boolean | `P` | 없음 | 3인칭 고정 추적 ↔ 1인칭 전환, 누를 때 한 번만 실행 |

전용 Mapping Context 이름은 `IMC_DronePrototype`이고 우선순위는 C++ 기본값 `1`을 사용한다. Keyboard/Mouse에는 별도 Trigger나 Dead Zone을 추가하지 않고 Gamepad Stick에는 기본 `0.2` Dead Zone을 적용한다.

### FPV Rate/Acro 전용 입력 계약 — 2026-10-04 C PC

공용 Move/Altitude/Yaw/CameraPitchRate를 Acro에서 재해석하지 않는다. 전용 Action6개(IA_DronePrototype_AcroPitch, IA_DronePrototype_AcroRoll, IA_DronePrototype_AcroYaw, IA_DronePrototype_AcroThrottle, IA_DronePrototype_AcroGamepadLeftVertical, IA_DronePrototype_AcroGamepadRightVertical)를 사용한다. 키보드 W/S=Pitch, A/D=Roll, Q/E=Yaw, Space/Ctrl=Throttle는 Mode1/2 동일하다.

| 패드 축 | Mode1 | Mode2 |
|---|---|---|
| LeftX | Yaw | Yaw |
| RightX | Roll | Roll |
| LeftY | Pitch | Throttle |
| RightY | Throttle | Pitch |

IMC Acro 패드4축 Dead Zone은 쉬운 조작 값을 복사한 Lower0.2/Upper1.0/Radial이다. 키보드에는 Dead Zone을 추가하지 않는다. RT/LT 공용 Altitude를 Acro 보조 스로틀로 안내하지 않는다.

## 2. 현재 C++과의 연결

ADroneFlightPawn은 키보드·패드 입력원을 따로 보관하고 의미축별 절댓값이 큰 쪽을 사용한다(한 Action의 여러 키를 합치는 Enhanced Input 규칙과 동일). 키를 누르면 키보드가 이기고 떼면 패드가 조종하며 모두 놓으면0이다. Mode1/2 차이는 패드 세로축 배치뿐이다. 수정 전 Space+오른쪽-0.5→스로틀-0.38, W+왼쪽-0.5→피치-0.38 덮어쓰기를 재현한 뒤 입력원 분리로 수정했다. 실제 패드 체감은 수동 대기다.

쉬운/제한 자세는 기존 Move·Altitude·Yaw·카메라 역할을 유지한다. Acro 피치/롤/요는 Body 각속도, 스로틀은 Body Up 추진이다. Mouse X 직접 Yaw·Mouse Y CameraBoom Pitch는 개발 입력이며 최종 정책 미정. SpringArm은 Controller Rotation을 쓰지 않는다. PawnClientRestart가 IMC를 한 번 등록·수명주기에 제거하며 BP EventGraph에 IMC 추가/Action 재바인딩을 넣지 않는다.

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
- Gamepad/RC Controller의 Rate/Acro 중앙 감도·Expo 최종값
- 범용 조종기 입력
- 최종 비행 물리와 자동 수평 유지
- 멀티플레이 입력·이동 권한 구조

## 6. 현재 검증 상태

- 현재 IMC는 역할 기능과 시점 전환을 포함해 33개 Mapping·Input Action14개을 사용한다. Action Asset 자체는 모드 전환 때 교체하지 않는다.
- Rate/Acro의 연속 축은 `Triggered + Completed + Canceled`를 묶어 Stick 해제 뒤 Pitch/Roll/Yaw 입력이 0으로 돌아가게 한다.
- 현재 Drone.Prototype 테스트11개. 10/04 후속 Prototype+Tutorial+ControlInputDisplayPIE는32개 중30 Success·Production 맵 의존2 Fail(ClaudeCourse/review_fix_test.log). AcroInputBehaviorPIE D구역8시나리오에서 키+패드-0.5·키 해제 인계·모두 해제0·패드만 피치/스로틀 자동 검증. overlap_before.log의4개 실패 항목은 overlap_after.log에서 해소, 실제 패드 체감은 수동 확인 대기.
- 사전 부분 확인 두 번은 모두 전체 조건을 끝내지 않아 Pass로 산정하지 않았다.
- PFN-06 자동화 3/3과 Standalone Keyboard·Mouse 수동 조작, 창 닫기 정상 종료가 통과해 Done이다. 실제 Gamepad 체감은 장치 연결 여부 미보고로 미확인이다. 정식 판정은 [`DRONE_PROTOTYPE_PIE_CHECKLIST.md`](DRONE_PROTOTYPE_PIE_CHECKLIST.md)를 따른다.
