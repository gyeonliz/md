# Drone Prototype 입력 계약

기준일: 2026-10-07 (Asia/Seoul)

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

### InterLink DX(RawInput) 입력 계약

사용자가 실제 조종 콘솔로 확정한 Spektrum InterLink DX는 USB 전용 시뮬레이터 조종기(USB HID, VID `0x1781` / PID `0x0E5A`, 축 8개·RawInput 버튼 설정 32개(스위치 상태 28~32 포함))다. XInput 장치가 아니므로 기존 `Gamepad_*` 33개 매핑만으로는 동작하지 않는다. 프로젝트 `Plugins/RawInput/`은 UE 5.8 엔진 복사본의 축 키에 `Axis1D`를 추가해 아날로그 값을 받으며, uplugin DeprecatedEngineVersion을 제거했다. `Drone.uproject`에서 Win64 활성화하고 프로젝트 플러그인이 우선 로드된다.

`Config/DefaultInput.ini`의 HID value caps 순서와 입력 배치는 다음과 같다. 모든 키는 `GenericUSBController_` 접두사를 사용한다.

| 축 | 실물 축 | 쉬운/제한 자세 | Acro |
|---|---|---|---|
| Axis1 | Slider | 미연결 | 미연결 |
| Axis2 | Rz·오른쪽 슬라이더 | 미연결 | 미연결 |
| Axis3 | Z·왼쪽 슬라이더 | 미연결 | 미연결 |
| Axis4 | Dial | 미연결 | 미연결 |
| Axis5 | Rx·오른쪽 스틱 가로 | Move.X | AcroRoll |
| Axis6 | Ry·오른쪽 스틱 세로 | Move.Y·Swizzle YXZ | AcroGamepadRightVertical |
| Axis7 | X·왼쪽 스틱 가로 | Yaw | AcroYaw |
| Axis8 | Y·왼쪽 스틱 세로 | Altitude | AcroGamepadLeftVertical |

기본 33개에 축 8개·아래 버튼 4개 매핑을 추가해 총 45개다. 키보드·마우스·XInput 매핑과 동작은 유지한다. 새 축 매핑의 Dead Zone은 쉬운 조작 Gamepad_RightX의 Lower 0.2·Upper 1.0·Radial을 복사한 값이며 새 수치 결정이 아니다. `bGamepadStick=True`로 -1..+1 정규화, 축 8개 모두 `bInverted=False`다. D PC 사용자 HID 실측에서 앞/위/오른쪽으로 밀면 원시값이 증가(0..4096)했으므로 초기 세로축 반전 가정은 폐기했다. 실제 장치는 Mode 2(왼쪽 세로 비복귀 스로틀·오른쪽 세로 중앙 복귀)로 확인됐다. 게임 Mode 2는 왼쪽 세로=Throttle·오른쪽 세로=Pitch, Mode 1은 두 세로축 역할만 교환한다. 실기 비행 부호·Dead Zone·Mode 2 호버/피치 체감은 수동 확인 대기다. 쉬운 조작의 중앙=고도 유지 처리는 Claude 채택 가안이며 비복귀 스로틀 정책은 현재 미정이다.

사용자가 확정한 비행 버튼 역할은 좌클릭·우클릭·P(시점 전환), 자폭 온/오프는 1=온·0=오프다. 모든 키는 `GenericUSBController_` 접두사를 사용한다.

| 버튼 | Input Action | 역할 |
|---|---|---|
| Button1 | PrimaryAbility | 좌클릭 역할 |
| Button12 | SecondaryAbility | 우클릭 역할 |
| Button13 | ToggleView | P·시점 전환 |
| Button1 | IA_DronePrototype_ArmSwitch(Boolean) | Started=ArmImpactDetonation 무장, Completed=Disarm 해제 |

Button1은 PrimaryAbility와 ArmSwitch에 함께 매핑된다. `ADroneFlightPawn.ArmSwitchAction`을 비행 BP FPV/Scout/Drop/FiberOptic 4종 Class Defaults에 연결하며, 자폭 기능 없는 Scout/Drop/FiberOptic/UGV는 ArmSwitch를 무시한다. 마우스 좌클릭 누르면 무장·우클릭 해제는 유지한다. Button1 물리 종류는 현재 미정이며 누름 버튼이면 누르고 있는 동안 무장될 수 있으므로 실기 체감을 확인한다.

사용자가 확정한 메뉴 조작은 좌우 없이 Select 노브 위/아래만으로 전부 이동·딸깍=확인·Cancel=뒤로다.

| 버튼 | 실물 조작 | 현재 메뉴 규칙 |
|---|---|---|
| Button15 | Cancel | Back |
| Button16 | Select 노브 딸깍 | Accept |
| Button17 | 노브 회전 한 방향 펄스 | Up·실물 방향 대응 미확인 |
| Button18 | 노브 회전 반대 방향 펄스 | Down·실물 방향 대응 미확인 |

`UDroneInterLinkNavigationSubsystem`(GameInstanceSubsystem, Config=Game)은 게임 시작 시 기본 키보드·패드 Slate FNavigationConfig 규칙을 보존하며 위 4개를 추가하고 종료 시 복원한다. Slate 없는 Commandlet에서는 생성하지 않는다. `DefaultGame.ini [/Script/Drone.DroneInterLinkNavigationSubsystem]`의 `KnobUpKey / KnobDownKey / KnobPressKey / CancelKey`로 설정하며 노브 방향이 반대면 Up/Down 키를 맞바꾼다. FrontEndRoot·Selection의 뒤로 가기에도 Cancel을 연결했다.

`FDroneGamepadFocus::StepFocus`는 화면 강조 목록 순서로 이전/다음 포커스를 이동하고 끝에서 감긴다. FrontEndRoot(타이틀/로비/브리핑)·Selection·Settings의 Preview 키 처리에서 노브 키를 가로채며 결과창은 기존 위/아래 명시 규칙을 사용한다. 훈련 로비 탭 버튼은 코드상 목록에 포함되며 실기 확인 대기다. 설정 콤보가 열려 있으면 Slate 기본 위/아래를 사용한다. 음량 슬라이더는 확인(노브 딸깍·A·Enter)으로 잠근 뒤 노브로 조절하며 `KnobSliderStep` 기본 0.05는 BP에서 조정 가능하다. `UDroneInterLinkNavigationSubsystem::GetKnobStep`으로 노브 단계를 판별한다. 패드·키보드 이동 규칙은 유지한다.

실기에서 Button1 무장/해제 체감·Button12/13, 노브만으로 타이틀→로비→탭→미션→브리핑→기체 선택→출격→결과 전체 이동·첫 강조·확인/뒤로, 설정 슬라이더 잠금/조절·콤보 목록과 노브 회전 방향을 확인한다. 브리핑 대사 넘김 버튼·CameraPitchRate는 조종기에 미연결, 미인식 안내 UI 미구현, 다른 송신기 설정·전시 PC 배포 플러그인 포함 확인도 미완료다. 탭 전용 버튼·안내 문구·전시 정책은 현재 미정이다.

`BuildDroneInterLinkInput.py`는 재실행 시 InterLink 축 매핑을 교체하고 버튼 매핑을 보존한다. `BuildDroneInterLinkButtons.py`는 버튼 4매핑·ArmSwitch/BP 연결을 반영한다. `BuildDroneAcroInput.py`의 매핑 수 검사에서는 GenericUSBController를 제외한다(이 변경 도구는 미실행). AcroInputAssetContract는 InterLink 4축 Dead Zone 계약을, PIEInputLifecycle은 총 45개·ArmSwitch 2개 바인딩을 검사한다. InterLinkButtonAssetContract는 추가4/기존6매핑 보존·BP4종 연결, InterLinkNavigationContract는 GetKnobStep 계약을 검사한다. 검증 날짜/PC·수치 이력은 [WORKLOG](../history/DRONE_WORKLOG.md#2026-10-07-interlink-dx-버튼armswitch노브-전용-메뉴-이동--d-pc-claude) 참조.

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
- InterLink DX 연결됨: 노브 회전 방향 대응·Button1 물리 종류·브리핑 넘김/탭 전용 버튼, 미인식 안내 문구·전시 조종기 정책·멀티 송신기 지원 현재 미정
- 최종 비행 물리와 자동 수평 유지
- 멀티플레이 입력·이동 권한 구조

## 6. 현재 검증 상태

- 현재 IMC는 역할 기능과 시점 전환을 포함해 45개 Mapping(기본 33+축 8+버튼 4)·Input Action15개를 사용한다. Action Asset 자체는 모드 전환 때 교체하지 않는다.
- Rate/Acro의 연속 축은 `Triggered + Completed + Canceled`를 묶어 Stick 해제 뒤 Pitch/Roll/Yaw 입력이 0으로 돌아가게 한다.
- InterLink 축·버튼·ArmSwitch·노브 전용 메뉴 이동 구현됨·자동 검증됨(D PC Claude), 실기 체감·전체 화면 메뉴 수동 확인 대기. 최신 결과와 이전 C PC 회귀 수치는 [WORKLOG](../history/DRONE_WORKLOG.md#2026-10-07-interlink-dx-버튼armswitch노브-전용-메뉴-이동--d-pc-claude) 참조.
- 사전 부분 확인 두 번은 모두 전체 조건을 끝내지 않아 Pass로 산정하지 않았다.
- PFN-06 자동화 3/3과 Standalone Keyboard·Mouse 수동 조작, 창 닫기 정상 종료가 통과해 Done이다. 실제 Gamepad 체감은 장치 연결 여부 미보고로 미확인이다. 정식 판정은 [`DRONE_PROTOTYPE_PIE_CHECKLIST.md`](DRONE_PROTOTYPE_PIE_CHECKLIST.md)를 따른다.
