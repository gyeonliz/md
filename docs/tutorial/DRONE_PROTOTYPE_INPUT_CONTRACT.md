# Drone Prototype 입력 계약

기준일: 2026-10-23 C PC(Asia/Seoul). 기존45매핑·Mode1/2를 보존하고 최신 자동 스로틀 모터 정책을 반영했다. 장치 실측 이력과 이번 엔진 내부 자동검증은 구분한다.

이 문서는 구매 에셋 없이 Flight 기능을 시험하기 위한 **기존 v1 Prototype 조작 계약**을 유지한다. 사용자 확인 대상은 일반 게임패드와 InterLink DX 모두다. 아래 기존 입력 역할을 보존하며 새 카메라 상하 축/버튼 배정·실장치 보정·최종 물리/감도 튜닝은 별도 미정이다. 두 장치 사용 요청을 미사용 조작의 재배치 승인으로 해석하지 않는다.

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

### 자동 스로틀 모터 정책

최신 사용자 요청으로 모터·스로틀 보류를 해제했다. 아래는 프로젝트에서 선택해 구현한 조작 정책이며 모든 실기체의 공통 방식이라는 뜻은 아니다. IMC의 기존45매핑과 Mode1/2 축 배치를 유지하고 별도 RC 스위치/채널은 추가하지 않았다.

| 입력원 | OFF와 시동 | 시동 후 출력/중립 |
|---|---|---|
| RC 절대축 | 기존 저장 IMC에 연결된 스로틀 축의 최하단 OFF→새 최하단 확인 뒤 올리면 ON | 엔진 signed -1=0%·+1=100% 선형 출력. 중앙 dead zone을 절대 출력에 다시 적용하지 않으며 중립 호버 명령과 구분 |
| XInput Acro | Mode1 오른쪽 세로/Mode2 왼쪽 세로의 아래 끝 OFF→의도적 위 입력으로 ON | 중앙 호버·부분 음수 제어 하강 |
| XInput 쉬운/게임 조작 | 기존 L2 끝 OFF→R2로 ON/상승 | 트리거 해제는 호버 |
| 키보드 | Ctrl OFF→Space로 ON/상승. Ctrl을 누르는 동안 OFF 우선 | Space 해제는 호버. Mode1/2 같은 키 유지 |

사람의 Possess/재Possess·일시정지/재개·링크 상실/복귀·출발 hold/해제·입력원 변경 뒤에는 최하단을 새로 확인해야 한다. 초기 높은 출력이나 중앙 복귀로 자동 시동하지 않는다. 실제 KeyState 보고가 없는 RC 축의 기본0을 50% 출력으로 사용하지 않는다. M/Ctrl+M 필수 바인딩·안내·검사는 제거했고 `DroneMotorArm`은 명시적 디버그 API로 남았다. 명시 OFF 뒤에도 이전 최하단 확인을 재사용하지 않는다.

Pawn Blueprint Class Defaults에 `MotorOffThrottle01=0.02`, `MotorStartThrottle01=0.06`(RC), `CenteredMotorStartCommand=0.10`을 노출했다. OFF는 즉시 적용하며 접지나 길게 누르기를 강제하지 않는다. 시동/정지 문턱 차이로 최하단 잡음을 처리한다. 일반 OFF의 무추력 중력·착지/재이륙은 무기 ArmSwitch·배터리 방전/파손과 구분하고 Legacy·AI·UGV 기존 모델을 보존한다. 새 FixedStepCandidate는 controlled Racer TestMap의 명시 opt-in 범위다.

2026-10-23 C PC BuildAutomatic09와 RegressionAutomatic03 13종(12성공·지원하지 않는 모드 거부의 예상 경고1)이 통과했다. 저장 맵/BP와 IMC45개를 엔진 simulated key-state·등록 delegate·API PIE로 검사했다. 실제 InterLink DX/XInput 입력 경로·캘리브레이션·조작감 및 HUD 화면 확인은 미실시이며 CUA 중지를 유지한다. [검증 범위](../gameplay/DRONE_REALISTIC_HANDLING_PLAN.md#자동-스로틀-모터-정책과-검증-범위)·[실행/실패 이력](../history/DRONE_WORKLOG.md).

### 일반 패드·InterLink 카메라 설정 경계

쉬운/게임 조작의 감도X/Y·반전 설정은 기존 기체 Yaw/CameraBoom Pitch 입력에만 적용된다. 이동·고도축, Acro 전용 Rate/스로틀, UGV 조향/포탑은 새 설정에서 제외한다. 두 장치는 현재 같은 적용 설정을 사용하며 장치별 프로파일을 새로 채택하지 않았다. 기본값·pending/적용/취소/저장·Designer와 확정 자동 검증 범위는 [설정 가이드](../gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#카메라-감도반전과-designer)가 정본이다.

| 장치/경로 | 현재 연결·설정 | 남은 확인 |
|---|---|---|
| 일반 게임패드 | RightX→YawAction→ChangeYaw에 감도X/반전X, RightY→CameraPitchRate→ChangeCameraPitch→CameraBoom에 감도Y/반전Y | 실제 장치의 중립/방향/해제→엔진 값→IMC/IA 실효값→모드→Boom→최종 ViewTarget을 함께 계측한다. 기존 경로 존재를 실물 상하 동작 Pass로 쓰지 않는다 |
| InterLink DX | 기존 Axis5/6=Move, Axis7=Yaw, Axis8=Altitude와 Acro/메뉴 계약을 유지한다. CameraPitchRate용 InterLink 매핑은 기존 연결 도구/계약에 없다 | 상하 시야 명령 공백은 감도Y 증가만으로 해결되지 않는다. 실제 저장 IMC·장치의 미사용 축/버튼을 읽고 배정·중립·유지/해제 정책을 확정한 뒤 연결한다 |

InterLink Axis1~4·미사용 버튼의 번호만 보고 물리 복귀형/순간 버튼으로 단정하거나 기존 비행4축을 재사용하지 않는다. 후보 두 버튼 유지 입력이나 남는 축은 아직 선택하지 않았다. 일반 패드의 실제 단절이 확인되면 해당 연결만 별도로 수정한다.

계측은 장치 모델·드라이버·분리/동시 연결, raw/min/center/max·Dead Zone 전후 값·현재 모드·신호/사망 차단·BP 회전율/clamp·최종 ViewTarget을 구분한다. 엔진 키 값은 USB 원시 HID 패킷과 다르다. Boom만 움직였어도 LOS 관찰자나 다른 Camera가 ViewTarget이면 화면 상하 성공으로 판정하지 않는다. 완료 기준은 두 장치 각각 쉬운/게임×1/3인칭·양방향/해제·적용/취소/기본값·실제 재실행과 기존 비행/메뉴 보존이다.

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

기본 33개에 축 8개·아래 버튼 4개 매핑을 추가해 총 45개다. 키보드·마우스·XInput 매핑은 유지하며 모터 동작은 위 자동 스로틀 정책을 따른다. 새 축 매핑의 Dead Zone은 쉬운 조작 Gamepad_RightX의 Lower 0.2·Upper 1.0·Radial을 복사한 값이며 새 수치 결정이 아니다. `bGamepadStick=True`로 -1..+1 정규화, 축 8개 모두 `bInverted=False`다. D PC 사용자 HID 실측에서 앞/위/오른쪽으로 밀면 원시값이 증가(0..4096)했으므로 초기 세로축 반전 가정은 폐기했다. 실제 장치는 Mode 2(왼쪽 세로 비복귀 스로틀·오른쪽 세로 중앙 복귀)로 확인됐다. 게임 Mode 2는 왼쪽 세로=Throttle·오른쪽 세로=Pitch, Mode 1은 두 세로축 역할만 교환한다. 실기 비행 부호·Dead Zone·Mode 2 호버/피치 체감은 수동 확인 대기다. 현재 비복귀 RC 절대출력과 XInput 중앙 호버·자동 시동/OFF 정책은 위 [자동 스로틀 모터 정책](#자동-스로틀-모터-정책)을 따른다. 10/07 실측은 당시 이력이다.

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

기존 Acro 축 겹침 수정에서 ADroneFlightPawn은 키보드·패드 입력원을 따로 보관하고 의미축별 절댓값이 큰 쪽을 사용한다(한 Action의 여러 키를 합치는 Enhanced Input 규칙과 동일). 키를 누르면 키보드가 이기고 떼면 패드가 조종하며 모두 놓으면0이다. Mode1/2 차이는 패드 세로축 배치뿐이다. 수정 전 Space+오른쪽-0.5→스로틀-0.38, W+왼쪽-0.5→피치-0.38 덮어쓰기를 재현한 뒤 입력원 분리로 수정했다. 현재 RC 절대출력·중앙 복귀형 시동/정지와 입력원 변경 후 재확인은 위 자동 스로틀 모터 정책을 우선한다. 실제 패드 체감은 수동 대기다.

쉬운/제한 자세는 기존 Move·Altitude·Yaw·카메라 역할을 유지한다. Acro 피치/롤/요는 Body 각속도, 스로틀은 Body Up 추진이다. Mouse X 직접 Yaw·Mouse Y CameraBoom Pitch는 개발 입력이며 최종 정책 미정. SpringArm은 Controller Rotation을 쓰지 않는다. PawnClientRestart가 IMC를 한 번 등록·수명주기에 제거하며 BP EventGraph에 IMC 추가/Action 재바인딩을 넣지 않는다.

## 3. PIE에서 결정할 항목

현재 사용자 감도/반전은 기존 IMC 부호 위에서 C++ 설정 변환을 한 번 거친다. 실물 장치 재현 전에는 IMC Modifier를 추가하거나 기본 회전율을 임의로 높이지 않는다. 일반 패드 RightY/InterLink 후보 조작의 실제 값→IA→모드→Boom→최종 화면을 구분해 기록하고 반전을 두 경로에 중복 적용하지 않는다.

아래 PFN-06 문단은 이전 확인 절차를 보존한 내용이며 위 현재 카메라 설정 경계를 대체하지 않는다.

Mouse Y는 Controller Pitch를 사용하지 않고 CameraBoom Pitch를 직접 조정한다. PFN-06 수동 확인에서는 현재 부호와 감도를 바꾸지 않고 체감 결과만 기록한다. 이후 조정할 때는 다음 원칙을 사용한다.

- Mouse Up이 Camera Up이면 Look Mapping에 Modifier를 추가하지 않는다.
- 반대이면 C++과 IMC 중 한 곳에서만 **Y축**을 반전한다.

C++와 IMC 양쪽에서 동시에 반전하지 않는다.

## 4. PFN-06 통과 기준

Editor lifecycle을 포함한 새 PIE 3회 자동화와 별도 수동 화면 확인 1회를 모두 통과해야 한다. 중복을 막기 위해 상세 항목과 실행별 결과는 [`DRONE_PROTOTYPE_PIE_CHECKLIST.md`](DRONE_PROTOTYPE_PIE_CHECKLIST.md)만을 단일 기준으로 사용한다.

## 5. 현재 미정

- 최종 키 배치와 사용자 재매핑
- 새 감도/반전 설정의 기본 동작은 기존 기준1배·반전 Off다. 실장치별 최종 감도·튜닝값과 InterLink 상하 조작 배정은 미정
- Gamepad/RC Controller의 Rate/Acro 중앙 감도·Expo 최종값
- InterLink DX 연결됨: 노브 회전 방향 대응·Button1 물리 종류·브리핑 넘김/탭 전용 버튼, 미인식 안내 문구·전시 조종기 정책·멀티 송신기 지원 현재 미정
- 최종 비행 물리와 자동 수평 유지
- 멀티플레이 입력·이동 권한 구조

## 6. 현재 검증 상태

- 10/22 D PC 카메라 설정의 지정 자동 검사·새 PNG 검토 범위는 [설정 가이드](../gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#카메라-감도반전과-designer)를 따른다. 자동 입력/메모리 직렬화와 일반 패드·InterLink의 실물 조작·실제 재실행은 구분한다. 아래 기존 검증 기록을 이번 장치 Pass로 재사용하지 않는다.

- 현재 IMC는 역할 기능과 시점 전환을 포함해 45개 Mapping(기본 33+축 8+버튼 4)·Input Action15개를 사용한다. Action Asset 자체는 모드 전환 때 교체하지 않는다.
- Rate/Acro의 연속 축은 `Triggered + Completed + Canceled`를 묶어 Stick 해제 뒤 Pitch/Roll/Yaw 입력이 0으로 돌아가게 한다.
- InterLink 축·버튼·ArmSwitch·노브 전용 메뉴 이동 구현됨·자동 검증됨(D PC Claude), 실기 체감·전체 화면 메뉴 수동 확인 대기. 최신 결과와 이전 C PC 회귀 수치는 [WORKLOG](../history/DRONE_WORKLOG.md#2026-10-07-interlink-dx-버튼armswitch노브-전용-메뉴-이동--d-pc-claude) 참조.
- 사전 부분 확인 두 번은 모두 전체 조건을 끝내지 않아 Pass로 산정하지 않았다.
- PFN-06 자동화 3/3과 Standalone Keyboard·Mouse 수동 조작, 창 닫기 정상 종료가 통과해 Done이다. 실제 Gamepad 체감은 장치 연결 여부 미보고로 미확인이다. 정식 판정은 [`DRONE_PROTOTYPE_PIE_CHECKLIST.md`](DRONE_PROTOTYPE_PIE_CHECKLIST.md)를 따른다.
