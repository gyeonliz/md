# Drone Prototype 입력 계약

기준일: 2026-10-27 D PC. 기존45매핑/Mode1·2와 안전가드를 보존하며 키보드·패드·RC의 스로틀 계산을 분리했다. 현재 정책은 아래를 따르며 검증 이력/중간 실패는 [WORKLOG](../history/DRONE_WORKLOG.md)에 둔다. 실물 수정 후 조작·전체 Slate/미션·패키징은 미확인이다.

이 문서는 구매 에셋 없이 Flight 기능을 시험하기 위한 **기존 v1 Prototype 조작 계약**을 유지한다. 사용자 확인 대상은 일반 게임패드와 InterLink DX 모두다. 아래 기존 입력 역할을 보존하며 새 카메라 상하 축/버튼 배정·왼쪽 축 이외의 실장치 보정·최종 물리/감도 튜닝은 별도 미정이다. 두 장치 사용 요청을 미사용 조작의 재배치 승인으로 해석하지 않는다.

### 파일럿 테스트맵 전용 숫자키

`/Game/Drone/Maps/TestMap/Lvl_DroneRotorDynamicsPilot`의 `ADroneRotorPilotSetup`만 소유하는 임시 숫자열 단축키다. 일반 미션/기존 훈련맵의 IMC나 사용자 키 설정을 바꾸지 않는다. 현재 저장 배치에서는 전용 Setup·GameMode·`DroneRotorControlledTest` 표식이 이 맵에만 있다. 실행 World·PIE 접두사를 제거한 정확한 위 패키지 경로·표식을 함께 검사한다. 액터/표식을 다른 맵에 복사해도 초기 기체 생성과 숫자키는 동작하지 않는다.

| 키 | 동작 | 조건 |
|---|---|---|
| 숫자열 `1` | 고정 관찰 진입; 관찰 중 재입력마다 좌상단3인칭 소화면 ON/OFF | 메인 관찰 시점 유지·비행 입력 차단/일시정지 중 거부 |
| 숫자열 `2` | 드론 1인칭, ViewTarget을 드론으로 복귀 | 소화면 닫힘·Drop 하부 시점 해제·기체 Pitch/Roll 추적 유지 |
| 숫자열 `3` | 드론3인칭: 기수 Yaw만 추적, Pitch/Roll은 수평 유지 | 소화면 닫힘·Drop 하부 시점 해제 |
| 숫자열 `4` / `5` | 쉬운 / 게임 조작, Legacy 이동 | 모터 OFF에서만 변경 |
| 숫자열 `6` / `7` | Mode1 / Mode2, 로터 후보 이동 | 모터 OFF·Racer/controlled tag 등 후보 제약 |
| 숫자열 `0` / `9` | 바람 / 비 독립 토글 | 바람 기본5m/s·비는 일시적 Profile/시각 액터 사용 |
| 숫자열 `8` | 출발 위치에서 새 Racer로 재시작 | Mode2·기본 시점·모터OFF·날씨 유지, 누른 키 실제 해제 후 새 입력 필요 |

NumPad는 별도 연결하지 않는다. 재시작은 관찰 카메라·기존 기체를 정리하고 선형/각속도·모터·제어기 상태를 초기화한다. 입력 초기화가 만든 합성 release는 실제 키 해제로 인정하지 않고 반복8에도 미해제 키를 유지한다. InterLink 래치형 버튼은 순간 버튼 해제 대기에서 제외하며 RC는 새 최하단→상승 확인을 유지한다. 사망으로 DisableInput된 기체도 새 기체로 교체한다. `9`는 기존 바람의 방향/세기를 바꾸지 않는다.

파일럿4~7은 본체 밑면 높이에 맞춘 같은 평평한 상자 판정을 사용하며 모드 전환에 따라 높이가 바뀌지 않는다.4/5는 기존 쉬운/게임 비행·키보드 Ctrl 접지OFF 정책을 유지하고 실제 새 판정의 지지를 확인한다.6/7의 자연 착륙 보조는 실제 접지·낮은 추력에서 모터 ON/OFF 모두 정립과 감속을 돕고, 새 이륙/강한 회전 명령에 해제한다. 모터 스위치·재시동 입력 규칙은 그대로다. 형상·접지 전환 조건과 별도 시험용 Data Asset 조정 위치는 [물리 정본](../gameplay/DRONE_REALISTIC_HANDLING_PLAN.md#파일럿-맵의-접촉회전착륙-보정)을 따른다.

이 키들은 `WasInputKeyJustPressed`를 직접 읽어 사용자 조작키 재지정 대상이 아니다. 일반 플레이의 `P`/Triangle/InterLink Button13 시점 전환은 기존 IMC→ToggleViewAction→ToggleFirstPersonView 경로와 3장치 설정을 유지한다. 숫자 `1/0`의 기존 자폭 ArmSwitch와 물리키를 공유하지만 파일럿 Racer의 기폭 기능은 비활성이며 일반 미션에 파일럿 토글이 추가되는 것은 아니다. 실행 반영 여부는 [시험 가이드](../gameplay/DRONE_TEST_MAP_GUIDE.md#파일럿-숫자키-실행-확인)를 따른다.

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

InterLink DX는 10/27 사용자 지정 Mode1 배치를 별도로 쓴다: 왼쪽 가로 Axis7=Roll(A/D), 오른쪽 가로 Axis5=Yaw(Q/E), 왼쪽 세로 Axis8=Pitch, 오른쪽 세로 Axis6=Throttle. 원본45매핑 자산은 보존하고 런타임 transient 사본의 RC 가로 Action2개만 교환한다. 일반 패드의 위 표와 키보드 배치는 그대로다. Mode2로 돌아오면 원래 RC 가로 배치를 쓴다.

IMC Acro 패드4축의 기존 Lower0.2/Upper1.0/Radial 자산은 보존한다. 스로틀은 보고된 raw 축에서 전용 dead zone0.08/exponent1.5를 한 번 적용하므로 옛 IMC0.2를 다시 적용한 값을 기대하지 않는다. Pitch/Roll/Yaw와 키보드의 기존 계약은 유지한다. RT/LT 공용 Altitude를 Acro 보조 스로틀로 안내하지 않는다.

<a id="자동-스로틀-모터-정책"></a>

### Space키 자동 시동·OFF 정책

10/23 사용자 요청으로 전날 모터/스로틀 보류를 해제했다. 최신 전체 Build를 완료하고 Editor를 재시작해 새 DLL을 로드해야 한다. 구10/22 DLL을 로드한 상태에서는10/23 소스정책이 적용되지 않았다.

| 입력원 | 시동/OFF | 입력 해제·안전조건 |
|---|---|---|
| 키보드 쉬운/게임 | 새 Space press 시동·상승, Ctrl은 모터ON 하강→실제 지면 접촉 시OFF | 공중 Ctrl 해제hover. 착지 후 release/기존 heldSpace로 재시동하지 않으며 새 Space 필요 |
| 키보드 Acro1/2 | Space 시동·hover 위 여유출력0.70 상승, Ctrl 즉시OFF | 기존 물리·속도상한·해제hover·fresh edge 시동 유지 |
| RC 절대축 | 최하단OFF·OFF 상태 새 입력원은 새 최하단 확인 후 올리면ON | 이미Armed인 유효 입력원 전환은 ON 유지. 절대출력/45매핑·Mode1/2 보존 |
| XInput | raw 축에 전용 dead zone0.08/exponent1.5·중앙hover·끝까지100%. Acro 아래끝OFF/의도적위입력ON, 쉬운·게임 L2/R2 역할 유지 | fresh-low/공통안전 유지·키 유지 중 탈취 금지. 장치별 게임 튜닝값이며 실측사양 아님 |

이미 Armed인 유효 입력원 전환은 ON을 유지하고 OFF 상태 새 입력원은 fresh-low 확인이 필요하다. 키보드 Space/Ctrl 유지 중 게임패드보다 우선하고 해제 후 살아 있는 패드 입력으로 복귀한다. RC 절대축의 유효 인계는 보존한다. 비활성 키보드 release·패드 중립의 탈취와 Possess/hold/pause/dead/link 공통가드를 유지한다. Keyboard0.70·Pad deadzone0.08/exponent1.5는 장치별 게임 기본값이며 실기체/사용자 장치 실측값이 아니다. RC는 선형 절대출력이며 키보드·패드 튜닝의 영향을 받지 않는다.

2026-10-27 키마 고도 반응 수정: 키보드의 모터 출력 한정값과 쉬운/게임의 방향성 고도 명령을 분리했다. 보조모드 Space 유지=고도입력1, 해제=0이며, Acro는 기존 질량·추력·모터응답·속도상한을 사용하면서 키보드 ClimbFractionAboveHover 기본/비정상값 fallback만0.70으로 올렸다. 패드/RC 곡선·UGV·마우스 감도·Acro CtrlOFF·중력은 보존한다. 실제 검증 상태는 [STATUS](../../STATUS.md), 날짜별 측정/Build 이력은 [WORKLOG](../history/DRONE_WORKLOG.md)를 따른다.

키보드 쉬운/게임 착지 정책: Ctrl 유지 중에는 모터ON·고도입력-1을 전달한다. 실제 몸체의 지면 blocking contact(위쪽 법선≥0.7, 다른 Pawn 제외)에서OFF하며, 근접 지면·옆벽·천장만으로OFF하지 않는다. 실제 이동 충돌 이벤트를 사용하므로 UE가 충돌 뒤 남기는 프레임별 pullback 간격을 착지 거리로 임의 확장하지 않는다. 기존 엄격한 접지 query는 이미 지지된 상태의 보조 판정이다. OFF 상태 Ctrl로 시동할 수 없고, 착지 후 Ctrl 해제나 이미 누르던 Space로 자동 재시동하지 않는다. 공중 Ctrl 해제는 모터ON/hover이며 기존 관성·제동은 유지한다. FPV/Acro·패드·RC·UGV 및 사망/신호손실/일시정지 가드는 기존 정책이다.

PlayerInput의 flush된 키 상태(!State 또는 bWasJustFlushed)는 새 RC 보고로 읽지 않는다. 실제 새 InputKey/InputAxis 보고 후 사용한다. 이번에는 flush Raw0이 Axis8 보정 후 RC출력0.504304로 오인되는 재현을 수리했으며 10/22 전체 입력 장애의 원인으로 소급하지 않는다. M/Ctrl+M/console motor API는 필수 시동 절차가 아니다. 실제 EnhancedPlayerInput/ProcessInputStack 4모드·saved6종(PawnClass, 공중5/UGV별도) 자동 범위이며 실물 손조작 Pass는 아니다.

Pawn BP Class Defaults의 시동/정지 문턱은 `MotorOffThrottle01=0.02`, `MotorStartThrottle01=0.06`(RC), `CenteredMotorStartCommand=0.10`이다. RC/패드·키보드 Acro의 OFF는 즉시 적용하고 시동/정지 문턱 차이로 최하단 잡음을 처리한다. 키보드 쉬운/게임 Ctrl은 위 접지OFF 정책을 따른다. 별도 RC 스위치/채널을 추가하지 않았으며 `DroneMotorArm`은 명시적 디버그 API다. 이는 프로젝트의 게임 조작 정책으로 실기체 공통 표준이나 장치 실측값이 아니다. 현재 Armed 유효 인계·OFF 새 입력원 fresh-low·키 유지 우선은 위 정책을 따른다.

InterLink DX 왼쪽 세로 Axis8(HID VID1781/PID0E5A, usage0x31)의 사용자 확인 최하단 raw642·최상단6표본3429~3431(중앙3430)을 읽었다. 장치 논리0~4096을 그대로 쓰면 출력은 약0.156738~0.837402에 그친다. `ReadRCLeftThrottle`의 Axis8 경계에서642~3430을0~1로 선형 보정하고 끝2raw를 snap/clamp한다. Pawn defaults의 EditDefaultsOnly On/Min/Max/Jitter 4항목으로 조정한다. 이 왼쪽 실측 보정은 일반 패드·Mode1 오른쪽 세로·다른 RC 축에 적용하지 않으며 범용 RawInput RangeMin0 계산도 유지한다. 이 실측은 현재 장치 왼쪽 축의 표본이며 실기체 물리 교정/전 장치 보정이 아니다.

Mode1 오른쪽 Axis6에는 별도의 최저점 인식 여유를 추가했다. 사용자 요청으로 논리 범위 하단20%까지 OFF/최하단으로 인식하고, 그 상태에서는23%를 초과해야 복귀한다. 이후 절대출력은 원래 선형 값이다. Pawn Class Defaults의 `InterLink Right Throttle`에서 사용 여부·하단 비율·복귀 여유를 조절한다. 오른쪽 실측 endpoints를 얻었다는 뜻이 아니며 왼쪽642~3430 보정·패드·키보드에는 적용하지 않는다. 최신 빌드/검증 경계는 [STATUS](../../STATUS.md)를 따른다.

### 지상 마찰·착지 자세와 실제 스틱 표시

일반 모터OFF Legacy 기체는 최근 실제 바닥 hit·정지한 지지면·짧은 접촉 sweep이 함께 확인될 때만 지상 마찰과 바람 drift 억제를 적용한다. Pawn Class Defaults `Ground Contact`의 마찰계수0.40, 최소 지지법선Z0.70, 접촉 여유0.50cm를 사용한다. 지면이 가깝다는 이유만으로 공중 관성을 없애지 않는다.

같은 접지 상태에서 날개가 위를 향하면 `bEnableMotorOffUprightLandingAssist`로 기울기를 서서히 지면 법선에 맞춘다. `UprightLandingMinimumUpDot=0.25`, `UprightLandingAlignmentRatePerSecond=6`이며 착지 때의 heading을 유지한다. 공중·뒤집힌 상태·동력상실/파괴·UGV에는 적용하지 않는다. 이는 게임용 착지 보정이며 강체 접촉/전복 전체 모델은 아니다.

HUD 십자 표시는 장치 축 보고가 있으면 실제 좌/우 스틱 위치를 먼저 읽는다. 일반 패드는 Gamepad LeftX/LeftY·RightX/RightY, InterLink는 Axis7/8·Axis5/6이다. 비행 Action의 모드별 재배치·모터 출력·응답 곡선·조작 차단과 분리하고, 알려진 왼쪽 실측 보정만 반영한다. 장치 보고가 없는 키보드는 기존 Action 대응 표시를 쓴다. 두 장치가 함께 보고하면 RC 조종권일 때 RC, 그 외에는 일반 패드를 우선한다. 기본 표시 끔/사용자 ON·OFF는 유지한다.

### 비행 키 재지정

설정의 `조작키 설정`은 `키보드 · 마우스 / 게임패드 / InterLink DX` 세 탭으로 나뉜다. 기능명과 현재 입력을 분리하고 선택 행·입력 대기·축 선택을 표시한다. 위/아래 항목 이동, Enter 변경/확정, Esc 또는 패드 Circle/RC Cancel로 취소·뒤로를 쓴다. 입력 대기나 축 선택 중 첫 취소는 편집만 취소하며 키 반복으로 창까지 연달아 닫지 않는다. 같은 기본 키를 공유하는 일반/Acro Action은 함께 바뀐다. 2D 이동 행과 Acro의 1D 축 행은 실제 IMC 슬롯에 따라 구분된다.

키보드는 디지털 키·마우스 버튼을 받으며 Enter/Esc/방향키를 메뉴용으로 보존한다. 패드/InterLink는 자기 장치의 버튼·같은 차원/범위의 축만 선택한다. signed 스틱과 0~1 트리거를 서로 바꾸지 않으며, 사용 중인 같은 종류의 축은 두 행을 원자적으로 교환한다. 스틱/RC 축에는 정방향·반전을 제공한다. 패드 Circle/Start/Dpad, InterLink의 설정된 knob/cancel은 메뉴 예약 입력으로 유지한다. 스틱 행은 물리 좌/우 위치 기준으로 표시하며 Mode1/2의 역할 차이와 InterLink 전용 Mode1 좌Roll·우Yaw 안내를 함께 제공한다.

`현재 장치 기본값`은 선택 탭만 복원한다. 키창의 `적용`은 부모 설정의 pending만 바꾸며, 실제 메모리·디스크 반영은 부모 `적용`에서 다른 설정과 함께 한 번 수행한다. 부모 취소는 변경을 버리고, 부모 기본값은 세 장치 모두 복원 대상으로 삼는다. 저장 실패 시 적용 전 입력 배정을 복구한다. 기존 `UDroneAudioSettingsSaveGame`과 `KeyboardBindings`를 유지하고 별도 `DeviceBindings(Device, BindingId, Key, bInvert)` 배열을 추가했다. 새 배열이 없는 옛 저장은 원래 배치다.

런타임은 원본45매핑·Mode1 RC action 교환·키보드·장치 사본을 순서대로 조합한다. native 시동/하강 키와 RC/패드 스로틀도 같은 배정/반전을 사용하며, 변경 시 이전 소유 바인딩·누른 입력·스로틀 interlock을 정리해 재배정만으로 시동되지 않게 한다. InterLink 실측 보정과 최저점 여유는 선택된 물리 채널에 맞춰 유지하고 HUD의 좌/우 스틱 표시는 비행 배정과 분리한다. 원본 IMC·제작 맵을 저장하지 않는다. 검사 수치와 실물 손조종 범위는 [STATUS](../../STATUS.md)·[WORKLOG](../history/DRONE_WORKLOG.md)를 따른다.

표준 패드는 UE5.8 `FSceneViewport::OnAnalogValueChanged`가 오른쪽 Y만 추가 반전한다. 프로젝트 `UDroneGameViewportClient::InputAxis`에서 이를 한 번 보정하여 양쪽 세로축을 물리 위+로 통일한다. Mode2 피치, Mode1 오른쪽 스로틀, 물리 HUD와 사용자 반전이 같은 기준을 사용한다. Config/DefaultEngine.ini의 GameViewportClientClassName으로 적용하고 엔진 원본·RawInput HID 부호·키보드·InterLink는 변경하지 않는다. 입력 검사는 PlayerInput 직접 주입과 실제 SceneViewport 경유를 구분하며, 새5기종×2모드×2장치20경로는 후자를 검사한다.

### 일반 패드·InterLink 카메라 설정 경계

역할별 1인칭 HFOV·장착각·Drop 하부 전환과 카메라 override는 [역할/카메라 정본](../gameplay/DRONE_TYPES_AND_CONTROL_MODES.md#1인칭-카메라-역할-프리셋)을 따른다. 아래 카메라 감도/추가 축 배정과 장치별 스로틀 설정은 별개다.

쉬운/게임 조작의 감도X/Y·반전 설정은 기존 기체 Yaw/CameraBoom Pitch 입력에만 적용된다. 이동·고도축, Acro 전용 Rate/스로틀, UGV 조향/포탑은 새 설정에서 제외한다. 이 look 감도/시야 반전은 공통 설정이며, 위 장치별 키 배정·비행 축 반전과 별개다. 기본값·pending/적용/취소/저장·Designer와 확정 자동 검증 범위는 [설정 가이드](../gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#카메라-감도반전과-designer)가 정본이다.

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

기본 33개에 축 8개·아래 버튼 4개 매핑을 추가해 총 45개다. 키보드·마우스·XInput 매핑은 유지하고 현재 모터·스로틀 동작은 [위 정책](#space키-자동-시동off-정책)을 따른다. 새 축 매핑의 Dead Zone은 쉬운 조작 Gamepad_RightX의 Lower 0.2·Upper 1.0·Radial을 복사한 값이며 새 수치 결정이 아니다. `bGamepadStick=True`로 -1..+1 정규화, 축 8개 모두 `bInverted=False`다. D PC 사용자 HID 실측에서 앞/위/오른쪽으로 밀면 원시값이 증가(0..4096)했으므로 초기 세로축 반전 가정은 폐기했다. 실제 장치는 Mode 2(왼쪽 세로 비복귀 스로틀·오른쪽 세로 중앙 복귀)로 확인됐다. 게임 Mode 2는 왼쪽 세로=Throttle·오른쪽 세로=Pitch다. 일반 패드 Mode1은 두 세로축 역할만 교환하고, InterLink 사용자 Mode1은 위 전용 계약처럼 가로도 좌Roll·우Yaw로 분리한다. 실기 비행 부호·Dead Zone·Mode 2 호버/피치 체감은 수동 확인 대기다. 비복귀 RC 절대출력과 중앙복귀 XInput 호버·시동/OFF는 위 현재 정책을 따른다. 10/07 실측/자산 Dead Zone은 당시 이력이며 현재 raw 스로틀 곡선과 구분한다.

사용자가 확정한 비행 버튼 역할은 좌클릭·우클릭·P(시점 전환), 자폭 온/오프는 1=온·0=오프다. 모든 키는 `GenericUSBController_` 접두사를 사용한다.

| 버튼 | Input Action | 역할 |
|---|---|---|
| Button1 | PrimaryAbility | 좌클릭 역할 |
| Button12 | SecondaryAbility | 우클릭 역할 |
| Button13 | ToggleView | P·시점 전환 |
| Button1 | IA_DronePrototype_ArmSwitch(Boolean) | Started=ArmImpactDetonation 무장, Completed=Disarm 해제 |

Button1의 PrimaryAbility/ArmSwitch 동시 매핑과4종 BP 연결은 보존한다. 현재 FPVStrike/FiberOptic은 자동 무장·해제 잠금이므로 ArmSwitch release/보조 입력으로 자폭을 해제하지 않는다. 자폭 기능 없는 Scout/Drop/UGV는 ArmSwitch를 무시한다. 무장과 모터 시동/OFF는 별개다. 위 버튼/IA 매핑은 유지하며 자폭의 실제 접촉 조건은 [전방 센서 정본](../gameplay/DRONE_TYPES_AND_CONTROL_MODES.md#fpv광섬유-자폭-센서와-물리-충돌)을 따른다. 실물 버튼 체감·비행은 수동 확인 대기다.

사용자가 확정한 메뉴 조작은 좌우 없이 Select 노브 위/아래만으로 전부 이동·딸깍=확인·Cancel=뒤로다.

| 버튼 | 실물 조작 | 현재 메뉴 규칙 |
|---|---|---|
| Button15 | Cancel | Esc와 같은 Back·영상Skip·미션Pause/복귀·시드편집취소 |
| Button16 | Select 노브 딸깍 | Accept |
| Button17 | 노브 회전 한 방향 펄스 | Up·실물 방향 대응 미확인 |
| Button18 | 노브 회전 반대 방향 펄스 | Down·실물 방향 대응 미확인 |

`UDroneInterLinkNavigationSubsystem`(GameInstanceSubsystem, Config=Game)은 게임 시작 시 기본 키보드·패드 Slate FNavigationConfig 규칙을 보존하며 위 4개를 추가하고 종료 시 복원한다. Slate 없는 Commandlet에서는 생성하지 않는다. `DefaultGame.ini [/Script/Drone.DroneInterLinkNavigationSubsystem]`의 `KnobUpKey / KnobDownKey / KnobPressKey / CancelKey`로 설정하며 노브 방향이 반대면 Up/Down 키를 맞바꾼다. FrontEndRoot·Selection 등 기존 Back에 더해 영상 Skip·시드 편집 취소·시작 지점 Back도 공통 IsBackKey를 쓴다. 미션 Pause는 유효한 설정 Cancel을 중복 없이 바인딩하고 paused 상태에서도 실행한다. WidgetParity·실제 PlayerInput pause PIE·오프닝/M1 영상 Cancel PIE와 기존 Esc 회귀가 최종15에 포함된다. 실물 Cancel 버튼 수동 확인은 별도다.

`FDroneGamepadFocus::StepFocus`는 화면 강조 목록 순서로 이전/다음 포커스를 이동하고 끝에서 감긴다. FrontEndRoot(타이틀/로비/브리핑)·Selection·Settings의 Preview 키 처리에서 노브 키를 가로채며 결과창은 기존 위/아래 명시 규칙을 사용한다. 훈련 로비 탭 버튼은 코드상 목록에 포함되며 실기 확인 대기다. 설정 콤보가 열려 있으면 Slate 기본 위/아래를 사용한다. 음량 슬라이더는 확인(노브 딸깍·A·Enter)으로 잠근 뒤 노브로 조절하며 `KnobSliderStep` 기본 0.05는 BP에서 조정 가능하다. `UDroneInterLinkNavigationSubsystem::GetKnobStep`으로 노브 단계를 판별한다. 패드·키보드 이동 규칙은 유지한다.

실기에서 Button1 무장/해제 체감·Button12/13, 노브만으로 타이틀→로비→탭→미션→브리핑→기체 선택→출격→결과 전체 이동·첫 강조·확인/뒤로, 설정 슬라이더 잠금/조절·콤보 목록과 노브 회전 방향을 확인한다. 브리핑 대사 넘김 버튼·CameraPitchRate는 조종기에 미연결, 미인식 안내 UI 미구현, 다른 송신기 설정·전시 PC 배포 플러그인 포함 확인도 미완료다. 탭 전용 버튼·안내 문구·전시 정책은 현재 미정이다.

`BuildDroneInterLinkInput.py`는 재실행 시 InterLink 축 매핑을 교체하고 버튼 매핑을 보존한다. `BuildDroneInterLinkButtons.py`는 버튼 4매핑·ArmSwitch/BP 연결을 반영한다. `BuildDroneAcroInput.py`의 매핑 수 검사에서는 GenericUSBController를 제외한다(이 변경 도구는 미실행). AcroInputAssetContract는 InterLink 4축 Dead Zone 계약을, PIEInputLifecycle은 총 45개·ArmSwitch 2개 바인딩을 검사한다. InterLinkButtonAssetContract는 추가4/기존6매핑 보존·BP4종 연결, InterLinkNavigationContract는 GetKnobStep 계약을 검사한다. 검증 날짜/PC·수치 이력은 [WORKLOG](../history/DRONE_WORKLOG.md#2026-10-07-interlink-dx-버튼armswitch노브-전용-메뉴-이동--d-pc-claude) 참조.

## 2. 현재 C++과의 연결

아래는 기존 Acro 의미축 중첩 수정의 이력이다. ADroneFlightPawn은 키보드·패드 입력원을 따로 보관하고 의미축별 절댓값이 큰 쪽을 사용한다(한 Action의 여러 키를 합치는 Enhanced Input 규칙과 동일). 키를 누르면 키보드가 이기고 떼면 패드가 조종하며 모두 놓으면0이다. Mode1/2 차이는 패드 세로축 배치뿐이다. 수정 전 Space+오른쪽-0.5→스로틀-0.38, W+왼쪽-0.5→피치-0.38 덮어쓰기를 재현한 뒤 입력원 분리로 수정했다. 실제 패드 체감은 수동 대기다. 현재 스로틀의 RC 절대출력·키 유지 우선/해제 후 패드 복귀·Armed 유효 인계·OFF 새 입력원 fresh-low는 [위 현재 정책](#space키-자동-시동off-정책)이 우선한다.

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
