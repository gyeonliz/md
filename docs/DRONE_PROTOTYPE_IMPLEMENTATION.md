# Drone Prototype Pawn 구현 및 검증 기록

기준일: 2026-08-24 (Asia/Seoul)

## 1. 현재 결과

현재 작업 경로 `D:\JGY\project\drone`에 기존 Third Person 경로와 분리된 최소 Drone Prototype이 있다. `C:\URproject\drone`은 2026-08-24 다른 PC에서 검증한 경로이며, 구현을 시작한 2026-08-19 당시 `C:\project\Drone`도 역사 기록일 뿐 현재 D 드라이브 작업 경로가 아니다.

- `ADronePrototypePawn` C++ 클래스가 컴파일된다.
- `ADronePrototypeGameMode`를 직접 선택하면 native 기본값으로 해당 Pawn을 Spawn한다.
- 자동화 테스트에서 컴포넌트 기본값, Spawn/Possess와 PIE 입력 lifecycle을 검증했다.
- Prototype Input Action 5개와 Keyboard·Mouse·Gamepad 15개 Mapping의 전용 IMC를 생성했다.
- BP Pawn에 입력 자산과 Engine Cube Placeholder를 연결했다.
- BP GameMode와 별도 `Lvl_DronePrototype` Greybox Map을 연결했다.
- BP PlayerController와 실제 WBP Flight HUD를 연결했다. C++는 생성·Possession·Delegate 수명주기, WBP는 Designer 외형을 담당한다.
- 새 자산 재로드 검증과 Map Check를 통과했다.
- 2026-08-21 Automation에서 새 PIE 3회 모두 IMC 한 개와 Keyboard·Mouse·Gamepad 입력을 확인했다.
- 기존 기본 맵과 전역 기본 GameMode는 변경하지 않았다.
- Android File Server는 사용하지 않는다는 사용자 결정을 반영해 비활성화했다.

현재 PFN-01~06은 완료했다. 새 PIE 자동화 세 회와 Standalone Keyboard·Mouse 수동 조작을 통과했고, 사용자가 창을 닫은 뒤 로그에서 `Win RequestExit`, `Game engine shut down`, `Exiting`을 확인했다. 실제 Gamepad 체감은 미확인이다. 항목과 결과는 [`DRONE_PROTOTYPE_PIE_CHECKLIST.md`](DRONE_PROTOTYPE_PIE_CHECKLIST.md)를 단일 기준으로 사용한다. 다음은 아직 완료되지 않았다.

- 최종 입력 키·감도·Mouse Y 반전 기본값 결정
- 최종 Drone Mesh 선택·연결
- 착륙·충돌 실패 처리

2026-08-19의 두 GUI PIE는 역사적 부분 확인이며 Pass 횟수에는 포함하지 않는다. PFN-06의 정식 판정은 2026-08-21 자동화와 별도 Standalone 수동 회차를 근거로 한다.

## 2. 변경된 실제 프로젝트 파일

```text
D:\JGY\project\drone\Config\DefaultEngine.ini
D:\JGY\project\drone\Source\Drone\Prototype\DronePrototypePawn.h
D:\JGY\project\drone\Source\Drone\Prototype\DronePrototypePawn.cpp
D:\JGY\project\drone\Source\Drone\Prototype\DronePrototypeGameMode.h
D:\JGY\project\drone\Source\Drone\Prototype\DronePrototypeGameMode.cpp
D:\JGY\project\drone\Source\Drone\Prototype\DronePrototypePlayerController.h
D:\JGY\project\drone\Source\Drone\Prototype\DronePrototypePlayerController.cpp
D:\JGY\project\drone\Source\Drone\UI\DroneFlightHUDWidget.h
D:\JGY\project\drone\Source\Drone\UI\DroneFlightHUDWidget.cpp
D:\JGY\project\drone\Source\Drone\Prototype\Tests\DronePrototypeDefaultsTest.cpp
D:\JGY\project\drone\Source\Drone\Prototype\Tests\DronePrototypeSpawnPossessTest.cpp
D:\JGY\project\drone\Content\Drone\Prototype\Input\Actions\IA_DronePrototype_Move.uasset
D:\JGY\project\drone\Content\Drone\Prototype\Input\Actions\IA_DronePrototype_Altitude.uasset
D:\JGY\project\drone\Content\Drone\Prototype\Input\Actions\IA_DronePrototype_Yaw.uasset
D:\JGY\project\drone\Content\Drone\Prototype\Input\Actions\IA_DronePrototype_Look.uasset
D:\JGY\project\drone\Content\Drone\Prototype\Input\Actions\IA_DronePrototype_CameraPitchRate.uasset
D:\JGY\project\drone\Content\Drone\Prototype\Input\IMC_DronePrototype.uasset
D:\JGY\project\drone\Content\Drone\Prototype\Blueprints\BP_DronePrototypePawn.uasset
D:\JGY\project\drone\Content\Drone\Prototype\Blueprints\BP_DronePrototypeGameMode.uasset
D:\JGY\project\drone\Content\Drone\Prototype\Blueprints\BP_DronePrototypePlayerController.uasset
D:\JGY\project\drone\Content\Drone\Prototype\UI\WBP_DroneFlightHUD.uasset
D:\JGY\project\drone\Content\Drone\Prototype\Maps\Lvl_DronePrototype.umap
```

현재 PFN-06 작업 트리에는 `Source/Drone/Drone.Build.cs`의 Editor 전용 `UnrealEd` 의존성과 `Source/Drone/Prototype/Tests/DronePrototypePIEInputLifecycleTest.cpp`도 추가되어 있다. 두 변경은 `DroneEditor Win64 Development` 빌드와 Automation Report 3 succeeded, 0 warnings, 0 errors로 검증했다.

`DefaultEngine.ini`에서는 Android File Server 관련 Plugin과 네트워크 사용을 끄고 기존 토큰 할당을 비웠다. 토큰 값은 이 문서나 로그에 기록하지 않았다.

## 3. 왜 필요한가

기존 `ADroneCharacter`는 Third Person 템플릿의 `ACharacter` 기반 보행 구조다. 이를 바로 드론으로 개조하면 기존 예제와 새로운 비행 실험이 섞여 비교와 복구가 어려워진다.

이번 단계에서는 다음 원칙을 적용했다.

1. 기존 Third Person 클래스·맵·GameMode를 보존한다.
2. 별도 `APawn` 기반 Prototype으로 드론 조종 구조를 시험한다.
3. 입력 자산과 키, 최종 물리, 멀티플레이 방식은 확정하지 않는다.
4. 작은 구조 테스트와 Spawn/Possess 테스트를 먼저 통과시킨다.

이 선택은 최종 Drone 클래스가 반드시 `APawn`이어야 한다는 결정이 아니다. Flight MVP 결과와 향후 물리·멀티 요구를 보고 다시 평가할 임시 기준이다.

## 4. Unreal에서 담당하는 클래스

### `ADronePrototypePawn`

다음 Prototype 구성요소와 동작을 담당한다.

- `USphereComponent`: Root와 충돌 기준
- `UStaticMeshComponent`: 나중에 Drone 외형을 연결할 표시용 컴포넌트
- `USpringArmComponent`와 `UCameraComponent`: 추적 카메라 기준
- `UFloatingPawnMovement`: 최소 이동 반응을 위한 임시 Movement Component
- Enhanced Input Action 바인딩
- 이 Pawn이 직접 추가한 Input Mapping Context의 등록·정리

### `ADronePrototypeGameMode`

격리 테스트나 native GameMode 직접 실행에서 `ADronePrototypePawn`을 기본 Pawn으로 Spawn하는 native 기본값이다.

주의: native Pawn의 Input Asset과 Mesh 기본값은 계속 `null`이다. 현재 실제 Prototype Map에서는 BP 자식에 자산을 배정하고 BP GameMode의 Default Pawn도 그 BP Pawn으로 바꿨다. native GameMode만 직접 쓰면 BP에 지정한 값이 적용되지 않는다는 경계는 그대로 유지한다.

### `ADronePrototypePlayerController`

로컬 화면의 Flight HUD 하나를 생성해 PlayerController 수명 동안 재사용한다. Pawn이 바뀌면 Widget을 새로 만들지 않고 현재 Pawn의 `UDroneTelemetryComponent`만 교체한다. `BP_DronePrototypePlayerController`는 `FlightHUDWidgetClass`에 `WBP_DroneFlightHUD`를 지정하며, Event Graph에서 생성·구독 로직을 중복 구현하지 않는다.

### 자동화 테스트

- `Drone.Prototype.PawnDefaults`: Root, Collision, Camera, Movement, GameMode 기본값 검증
- `Drone.Prototype.SpawnPossess`: 임시 Game World에서 GameMode 생성, Pawn Spawn, PlayerController Possess 검증
- `Drone.Prototype.PIEInputLifecycle`: `Lvl_DronePrototype` 새 PIE 3회에서 BP Pawn/IMC/입력 매핑과 단일 입력·복합 입력·반대 입력·재시작 간 입력 세기를 검증

두 번째 테스트에는 실제 `ULocalPlayer`가 없으므로 IMC 등록과 실제 입력 전달까지 검증하는 테스트는 아니다.

## 5. 헤더에 추가된 것

`DronePrototypePawn.h`에는 다음 선언이 있다.

- 다섯 개의 컴포넌트 `TObjectPtr`
- Prototype IMC와 다섯 Input Action용 `TObjectPtr`
- Mapping Priority, Mouse Yaw/Pitch 감도, Gamepad Camera Pitch Rate와 Camera Pitch 범위
- `PawnClientRestart`, `SetupPlayerInputComponent`, `UnPossessed`, `EndPlay`
- 이동·고도·Yaw·Mouse Look·Gamepad Camera Pitch 처리 함수
- 이 Pawn이 실제로 추가한 IMC만 제거하기 위한 약한 참조와 소유 플래그

`ClearAllMappings()`는 사용하지 않는다. 다른 시스템이 등록한 Mapping Context까지 지우지 않기 위해서다.

`DronePrototypeGameMode.h`에는 격리 테스트용 `AGameModeBase` 자식만 선언한다.

## 6. CPP에 추가된 것

### 컴포넌트 구성

- 반경 `45.0`인 Sphere를 Root로 사용한다.
- Root Collision Profile은 `Pawn`이다.
- Root와 표시용 Mesh의 물리 시뮬레이션을 끈다.
- 표시용 Mesh 충돌은 끈다.
- Root가 NavMesh에 영향을 주지 않게 설정한다.
- SpringArm 길이는 Prototype 값 `500.0`이다.
- Camera는 SpringArm 끝에 붙는다.

### 임시 이동 값

```text
MaxSpeed     1200
Acceleration 2400
Deceleration 3000
TurningBoost 8
Yaw Rate     90 degrees/second
```

이 값들은 비교와 입력 반응 확인을 위한 Prototype 값이며 최종 비행 모델이 아니다. `UFloatingPawnMovement`에는 중력이 없고, 최종 드론 물리나 네트워크 이동 해법으로 확정하지 않았다.

### 입력 수명주기

1. `PawnClientRestart()`가 먼저 부모 구현을 호출한다.
2. 로컬 PlayerController와 LocalPlayer Subsystem이 있을 때만 Prototype IMC를 추가한다.
3. 이미 다른 경로가 같은 IMC를 등록했다면 소유한 것으로 표시하지 않는다.
4. 추가 뒤 `HasMappingContext()`로 실제 등록 여부를 다시 확인한다.
5. `UnPossessed()`와 `EndPlay()`에서 이 Pawn이 추가한 IMC만 제거한다.

현재 standalone 범위에는 맞지만, 향후 클라이언트 Pawn 교체나 멀티플레이를 구현할 때는 `NotifyControllerChanged()` 또는 PlayerController 소유 IMC 구조를 다시 검토해야 한다.

### 입력 함수

- Move: Actor Forward/Right 방향 이동 입력
- Altitude: World Up 방향 이동 입력
- Yaw: Delta Seconds를 적용한 Local Yaw 회전
- Mouse Look X: Actor Local Yaw 회전
- Mouse Look Y: SpringArm 상대 Pitch 조정
- Gamepad Camera Pitch: Delta Seconds를 적용한 SpringArm 상대 Pitch Rate

Input Action이 배정되지 않았으면 크래시 대신 진단 로그를 남긴다.

## 7. 현재 Blueprint와 Input 설정

다음 자산은 생성과 저장 뒤 별도 Editor 프로세스에서 다시 로드해 검증했다.

```text
/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_Move       Axis2D
/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_Altitude   Axis1D
/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_Yaw        Axis1D
/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_Look       Axis2D
/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_CameraPitchRate Axis1D
/Game/Drone/Prototype/Input/IMC_DronePrototype
/Game/Drone/Prototype/Blueprints/BP_DronePrototypePawn
/Game/Drone/Prototype/Blueprints/BP_DronePrototypeGameMode
/Game/Drone/Prototype/Blueprints/BP_DronePrototypePlayerController
/Game/Drone/Prototype/UI/WBP_DroneFlightHUD
/Game/Drone/Prototype/Maps/Lvl_DronePrototype
```

기존 Setup 도구는 Input·Pawn·GameMode·Map 9개 자산을 계속 검증한다. 추가한 BP Controller와 WBP 2개는 `Drone.UI.FlightHUDBlueprintAsset` 자동화가 부모 Class, 필수 TextBlock·Font와 Class 연결을 별도로 검증한다. 현재 Prototype 전체 자산은 이 둘을 포함해 11개다.

현재 IMC에는 15개 Mapping이 있다.

- Move: `W/S/A/D`
- Altitude: `Space Bar/Left Ctrl`
- Yaw: `E/Q`
- Look: `Mouse XY 2D-Axis`
- Move: Gamepad Left Stick X/Y
- Altitude: Gamepad `RT/LT`
- Yaw: Gamepad Right Stick X
- Camera Pitch Rate: Gamepad Right Stick Y

Modifier와 기대 부호는 [`DRONE_PROTOTYPE_INPUT_CONTRACT.md`](DRONE_PROTOTYPE_INPUT_CONTRACT.md)에 기록했다. 역할 배치는 사용자 승인 v1 기준이며 감도·반전·최종 물리는 수동 체감 뒤 조정한다.

`BP_DronePrototypePawn`은 `ADronePrototypePawn` 자식이다. Class Defaults에 IMC와 다섯 Action을 연결했고, Visual Mesh에는 외부 구매 소스가 아닌 Engine 기본 Cube를 Placeholder로 연결했다. Event Graph에서 IMC를 추가하거나 Action을 다시 바인딩하지 않는다.

`BP_DronePrototypeGameMode`는 `ADronePrototypeGameMode` 자식이며 Default Pawn은 BP Prototype Pawn, PlayerController Class는 `BP_DronePrototypePlayerController`다. 해당 BP Controller의 `FlightHUDWidgetClass`는 `WBP_DroneFlightHUD`다. 입력 IMC는 계속 Pawn 한 곳에서만 관리하고 BP Controller/Event Graph에는 중복 등록하지 않는다. native `ADronePrototypePlayerController`와 `UDroneFlightHUDWidget`은 직접 선택했을 때 사용할 기본 Class/레이아웃을 유지한다.

`Lvl_DronePrototype`은 기존 World Partition Template Map을 복제하지 않고 새로 만든 작은 비-World-Partition 시험장이다. Map-level GameMode Override, PlayerStart 한 개, 배치 Pawn 0개, 지면·이륙 Pad·벽·높이 표식·목표·귀환·Patrol·Turret 위치 표시를 포함한다. 위치와 크기는 모두 Greybox 임시값이다.

## 8. Editor에서 재검증하는 방법

1. UE 5.8.1로 `Drone.uproject`를 연다.
2. `Lvl_DronePrototype`을 연다.
3. World Settings의 GameMode Override가 `BP_DronePrototypeGameMode`인지 확인한다.
4. Map에 `PlayerStart`가 한 개이고 Pawn이 직접 배치되지 않았는지 확인한다.
5. BP GameMode의 PlayerController Class가 `BP_DronePrototypePlayerController`인지 확인한다.
6. BP Controller의 Flight HUD Widget Class가 `WBP_DroneFlightHUD`인지 확인한다.
7. PIE를 시작하고 BP Prototype Pawn 한 대가 BP Controller에 Possess되는지, 좌측 상단 WBP가 표시되는지 확인한다.
8. Enhanced Input Debug에서 `IMC_DronePrototype`이 Priority 1로 한 번만 등록되는지 확인한다.
9. `W/S/A/D`, `Space/Left Ctrl`, `Q/E`를 시험해 Move, Altitude와 보조 Yaw 방향을 확인한다.
10. Mouse X가 Drone Actor Yaw를 바꾸며 추적 Camera가 기체 뒤를 따라가는지, Mouse Y가 기체 Yaw 없이 CameraBoom Pitch만 바꾸는지 확인한다.
11. Gamepad가 연결되어 있으면 Left Stick 이동, `RT/LT` 고도, Right Stick X Drone Yaw와 Y Camera Pitch를 확인한다.
12. Output Log에서 Input Asset 누락, IMC 등록 실패, 다른 경로 소유 진단이 없는지 확인한다.
13. PIE를 종료하고 새로 두 번 더 실행해 Pawn·IMC·HUD·Callback·입력 세기가 중복되지 않는지 확인한다.

새 계약의 자동화 PIE 3회와 Standalone Keyboard·Mouse 수동 회차는 모두 통과했다. 실제 Gamepad 연결 여부가 보고되지 않아 Stick·Trigger 체감만 미확인이다.

## 9. 정상 결과

Blueprint와 Input 연결까지 완료했을 때의 정상 기준은 다음과 같다.

- Prototype 맵에서 Pawn이 한 대만 Spawn된다.
- `BP_DronePrototypePlayerController`가 해당 Pawn을 Possess한다.
- `WBP_DroneFlightHUD`가 한 개만 표시되고 현재 Pawn Telemetry를 사용한다.
- Camera가 SpringArm 기준으로 표시된다.
- 수평 이동, 고도, Yaw, Look 입력이 서로 독립적으로 반응한다.
- PIE를 반복해도 입력이 중복되지 않는다.
- 기존 `Lvl_ThirdPerson` 실행 경로는 그대로 동작한다.

착륙, Crash/실패, 배터리, 통신 거리, 재밍은 이 정상 기준에 포함하지 않는다.

## 10. 문제가 생겼을 때 확인할 항목

### Pawn이 Spawn되지 않음

- 테스트 맵의 World Settings GameMode Override
- Blueprint GameMode의 Default Pawn Class
- PlayerStart 존재와 충돌 여부
- 맵에 Pawn을 직접 배치하면서 GameMode Spawn도 함께 사용해 두 대가 생기지 않았는지

### Pawn은 생기지만 입력이 없음

- native GameMode가 native Pawn을 Spawn하고 있지 않은지
- `BP_DronePrototypePawn`의 IMC와 다섯 Action이 모두 연결됐는지
- Project Settings의 Default Input Component Class가 Enhanced Input인지
- Output Log의 누락 자산 또는 Mapping 등록 메시지
- IMC에 실제 키 Mapping이 추가됐는지

### 이동이 안 되거나 충돌이 이상함

- `UFloatingPawnMovement.UpdatedComponent`가 Sphere Root인지
- Sphere Collision Profile이 `Pawn`인지
- Visual Mesh Collision과 Simulate Physics가 꺼져 있는지
- Root를 다른 컴포넌트로 바꾼 Blueprint Override가 없는지

### Camera가 기체와 분리되거나 두 번 회전함

- SpringArm의 `Use Pawn Control Rotation`은 꺼져 있는지
- SpringArm이 Pawn Yaw를 상속하는지
- Camera의 `Use Pawn Control Rotation`은 꺼져 있는지

### 멀티플레이 또는 Pawn 교체에서 IMC가 남음

현재 범위를 넘어서는 문제다. 최종 멀티 방식이 결정되면 Controller 변경 수명주기와 IMC 소유 위치를 다시 설계한다.

## 11. 수행한 검증

### C++ 빌드

```text
Target: DroneEditor Win64 Development
Engine: UE 5.8.1
Result: Succeeded
```

기본 선택되는 MSVC 14.38은 UE 5.8 Engine PCH 컴파일 오류를 내므로, 설치된 MSVC `14.51.36256`을 `-CompilerVersion=14.51.36256`으로 명시했다. 이 버전은 UE가 표시한 선호 버전 `14.50.35717`보다 새 버전이라는 경고가 있었지만 이번 빌드는 성공했다.

### 자동화 테스트

```text
Drone.Prototype.PawnDefaults  Success, 0 warnings, 0 errors
Drone.Prototype.PIEInputLifecycle  Success, 0 warnings, 0 errors
Drone.Prototype.SpawnPossess  Success, 0 warnings, 0 errors
Total                        3 succeeded, 0 failed
Process exit code            0
```

결과 파일은 로컬 임시 검증 폴더의 `AutomationReport/index.json`에 생성했으며 Git 추적 대상이 아니다.

### Prototype 자산 생성과 재로드 검증

Editor Python은 프로젝트 Plugin 설정을 바꾸지 않고 실행 시점에만 `PythonScriptPlugin`을 활성화했다. 최초 생성기는 8개 대상 경로를 먼저 검사하고 기존 자산이 하나라도 있으면 덮어쓰지 않고 중단한다. 이후 전용 `UpdateControls` 도구로 Camera Pitch Rate Action과 새 Mapping만 안전하게 추가했다.

확인 결과:

- Input Action 5개와 IMC 한 개 생성
- 정확히 15개 Mapping과 Modifier 순서·부호 검증
- BP Pawn/GameMode 부모와 CDO 참조 검증
- Map GameMode Override, PlayerStart 한 개, 배치 Pawn 0개와 Greybox Actor 검증
- `CompileAllBlueprints` 종료 코드 0, 0 errors, 0 warnings
- 수정된 별도 프로세스 재로드 검증 `VALIDATION_OK`
- Map Check 0 errors, 0 warnings

첫 별도 프로세스 검증에서는 Map을 generic asset으로 강참조한 채 다시 여는 검증 도구 결함이 발견됐다. Map을 `LevelEditorSubsystem`으로만 열도록 수정한 뒤 새 프로세스에서 통과했으며, 이 과거 실패는 현재 자산 결함으로 분류하지 않는다.

### BP Prototype Map 헤드리스 실행

`Lvl_DronePrototype`을 명령줄에서 실행했다.

확인 결과:

- `BP_DronePrototypeGameMode_C` 사용
- `BP_DronePrototypePawn_C_0` Spawn/Possess
- Enhanced Input Subsystem 초기화
- Input Component 불일치, Action/IMC 누락, IMC 중복 소유·등록 실패 진단 0회
- 정상 종료 코드 0

### GUI PIE PFN-06

2026-08-19의 사전 PIE 두 번은 Spawn/Possess, IMC 한 개와 입력 반응을 부분 확인한 역사적 기록이다. 이후 2026-08-21 lifecycle 자동화 새 PIE 3회와 별도 Standalone Keyboard·Mouse 수동 회차, 정상 종료가 통과해 PFN-06은 Done이다.

정식 검증의 체크 항목, 실행별 결과와 수동 화면 확인은 [`DRONE_PROTOTYPE_PIE_CHECKLIST.md`](DRONE_PROTOTYPE_PIE_CHECKLIST.md)에만 기록한다.

### 과거 native fallback 실행

기존 `Lvl_ThirdPerson`을 저장 변경하지 않고 명령줄 URL로 Prototype GameMode만 Override해 실행했다.

확인 결과:

- `DronePrototypeGameMode` 로드 1회
- `DronePrototypePawn` Spawn/Possess 1회
- 미배정 IMC 진단 로그 1회 — BP 자산 생성 전 native fallback을 검증한 역사적 결과
- 프로젝트 코드 Fatal/Error 0회
- 정상 종료 코드 0

### 정적 확인

- Prototype Source 6개 모두 strict UTF-8
- 충돌 마커 0
- 후행 공백 0
- Setup 도구 대상 Prototype 9개와 추가 UI 2개를 합친 11개 자산 모두 Git LFS 속성 적용
- 기존 전역 Map/GameMode는 Third Person 설정 그대로 유지
- Python Plugin을 `.uproject`에 영구 추가하지 않음
- 새 Input Action과 갱신한 BP/IMC를 포함한 기존 9개 자산은 Setup 별도 프로세스에서 재로드 검증
- 추가 BP Controller와 WBP 2개는 Blueprint Asset 자동화와 PIE 실제 Class 검증

## 12. 현재 다음 완료 게이트

현재 Tutorial/Story 우선 실행 순서와 Greybox 기준은 [`DRONE_TUTORIAL_STORY_PLAN.md`](DRONE_TUTORIAL_STORY_PLAN.md)를 우선하며, PFN 카드 세부 정의는 [`DRONE_PREASSET_FUNCTION_PLAN.md`](DRONE_PREASSET_FUNCTION_PLAN.md)를 함께 따른다.

`HUD-01` Telemetry Snapshot, `HUD-02` 공용 Flight HUD, `TUT-01` Training Map·비충돌 Spline, `TUT-02` 순서형 Ring Gate와 `TUT-03` Segment/Lap 원본 기록을 완료했다. Source 기준은 `main=origin/main=551e287`이고 전체 `Drone.` 자동화 14/14, Tutorial 6/6, Blueprint Compile Errors/Warnings/Load Failures 0/0/0을 통과했다. 현재 코드 책임과 Editor 확인법은 [`DRONE_CODE_STRUCTURE_AND_USER_TASKS.md`](DRONE_CODE_STRUCTURE_AND_USER_TASKS.md)를 따른다. 다음 완료 게이트는 `TUT-04` 이전 기록 비교·Best·결과 UI다.

```text
PFN-06 Done
→ HUD-01 Telemetry Snapshot Done
→ HUD-02 Flight HUD Done
→ TUT-01 Training Map·비충돌 Spline Done
→ TUT-02 Gate·순서·정방향 Done
→ TUT-03 Segment/Lap 원본 기록 Done
→ TUT-04 이전 기록 비교·Best·결과 UI
```

이후 순서는 `TUT-04 결과 UI → Flight 상태 → Operator↔Drone → Story NPC·Mission·Jamming → Enemy AI/MG → 에셋 통합`이다.
