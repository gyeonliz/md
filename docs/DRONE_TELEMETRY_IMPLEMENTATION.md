# Drone Telemetry 구현 및 검증 기록

기준일: 2026-08-23 (Asia/Seoul)

## 1. 현재 결과

`HUD-01`의 공용 Telemetry Snapshot 공급 계층과 `HUD-02`의 실제 Flight HUD 화면 계층을 구현했다. Component는 Prototype Pawn에 기본 부착되며, 매 프레임 Tick 대신 기본 0.1초 Timer와 명시적 즉시 갱신으로 Snapshot Event를 보낸다. C++ PlayerController/HUD 기능이 현재 Possess Drone의 Event와 수명주기를 관리하고 실제 `WBP_DroneFlightHUD`가 네 수치의 Designer 외형을 표시한다.

현재 제공 값은 다음 네 가지다.

| 값 | 단위 | 계산 |
|---|---|---|
| Speed | km/h | `Velocity.Size() × 0.036` |
| Altitude | m | `(Actor Z - Reference Z) × 0.01` |
| Vertical Speed | m/s | `Velocity.Z × 0.01` |
| Heading | degree | Actor의 World Yaw를 `0~359°`로 정규화; 진북 Compass 값은 아님 |

## 2. 실제 코드 위치

아래 절대 경로는 작업컴 기준이다. 이번 검증 PC의 루트는 `C:\URproject\drone`이며 저장소 안의 상대 경로는 동일하다.

```text
D:\JGY\project\drone\Source\Drone\Telemetry\DroneTelemetryTypes.h
D:\JGY\project\drone\Source\Drone\Telemetry\DroneTelemetryComponent.h
D:\JGY\project\drone\Source\Drone\Telemetry\DroneTelemetryComponent.cpp
D:\JGY\project\drone\Source\Drone\Telemetry\Tests\DroneTelemetryTest.cpp
```

Prototype Pawn과 런타임 회귀 테스트 연결 위치:

```text
D:\JGY\project\drone\Source\Drone\Prototype\DronePrototypePawn.h
D:\JGY\project\drone\Source\Drone\Prototype\DronePrototypePawn.cpp
D:\JGY\project\drone\Source\Drone\Prototype\Tests\DronePrototypeDefaultsTest.cpp
D:\JGY\project\drone\Source\Drone\Prototype\Tests\DronePrototypeSpawnPossessTest.cpp
```

HUD-02 화면·Controller·수명주기 테스트 위치는 저장소 기준 다음과 같다. 이번 검증 PC의 저장소 루트는 `C:\URproject\drone`이다.

```text
Source\Drone\UI\DroneFlightHUDWidget.h
Source\Drone\UI\DroneFlightHUDWidget.cpp
Source\Drone\Prototype\DronePrototypePlayerController.h
Source\Drone\Prototype\DronePrototypePlayerController.cpp
Source\Drone\UI\Tests\DroneFlightHUDTest.cpp
Source\Drone\UI\Tests\DroneFlightHUDBlueprintAssetTest.cpp
Source\Drone\Prototype\Tests\DronePrototypePIEInputLifecycleTest.cpp
Content\Drone\Prototype\UI\WBP_DroneFlightHUD.uasset
Content\Drone\Prototype\Blueprints\BP_DronePrototypePlayerController.uasset
Content\Drone\Prototype\Blueprints\BP_DronePrototypeGameMode.uasset
```

## 3. Snapshot 책임

`FDroneTelemetrySnapshot`은 UI와 Tutorial 기록 시스템이 읽는 값 묶음이다. Widget이 속도나 고도를 다시 계산하지 않도록 C++ 계산 결과만 전달한다.

- `SpeedKilometersPerHour`
- `AltitudeMeters`
- `VerticalSpeedMetersPerSecond`
- `HeadingDegrees`

현재 Speed는 수평 속도만이 아니라 수직 이동을 포함한 전체 속력이다. Tutorial 구간 평균 속도도 같은 기준을 사용할지, 수평 속도를 별도로 표시할지는 실제 Course 검증 뒤 결정한다.

## 4. Component 수명주기

1. `BeginPlay`에서 첫 Snapshot을 즉시 갱신한다.
2. 0.1초 간격의 반복 Timer를 등록한다.
3. Owner의 Velocity, Location과 Yaw로 Snapshot을 계산한다.
4. `OnTelemetryUpdated` Blueprint Event를 Broadcast한다.
5. `EndPlay`에서 자신이 등록한 Timer를 제거한다.

`PrimaryComponentTick.bCanEverTick`은 `false`다. HUD가 Pawn을 매 프레임 검색하거나 Property Binding으로 계산하는 구조도 사용하지 않는다.

## 5. 고도 기준

현재 고도는 지형 Line Trace가 아니라 Course/Mission 기준면의 World Z 대비 값이다.

- 기본 Reference Z: `0 cm`
- 런타임 설정: `SetAltitudeReferenceZCentimeters`
- 설정 즉시 Snapshot 재계산과 Event Broadcast
- 기준면 아래는 음수 고도로 보존

Tutorial에서는 시작 Pad 또는 `ADroneTrainingCourse`가 Reference Z를 지정한다. Story Mission에서는 출격 지점이나 Mission 기준면을 지정한다. 지형 바로 위 고도가 별도로 필요해질 때 `AGL` 값을 추가하되 현재 Altitude 의미를 조용히 바꾸지 않는다.

## 6. HUD-02 연결 기준

실제 Prototype Map의 연결 체인은 다음과 같다.

```text
Lvl_DronePrototype
→ BP_DronePrototypeGameMode
→ BP_DronePrototypePlayerController
→ WBP_DroneFlightHUD
→ UDroneFlightHUDWidget C++ 기능
→ UDroneTelemetryComponent Event
```

공용 Flight HUD는 다음 방식으로 동작한다.

1. `ADronePrototypePlayerController`가 로컬 Player 화면에 `UDroneFlightHUDWidget` 하나를 생성하고 수명 동안 재사용한다.
2. 현재 Possess Pawn에서 `UDroneTelemetryComponent`를 가져온다.
3. 기존 Source를 해제한 뒤 `OnTelemetryUpdated`를 `AddUniqueDynamic`으로 한 번만 구독한다.
4. 연결 직후 `GetLatestSnapshot()`을 한 번 적용해 초기 Event를 놓쳐도 빈 화면이 되지 않게 한다.
5. 새 Snapshot을 받으면 네 Text 값을 갱신한다.
6. Pawn 전환·UnPossess·Widget 종료·Controller 종료 시 기존 Component Event를 해제한다.
7. C++ Widget은 표시 문자열 포맷만 담당하고 단위 변환이나 Telemetry 재계산은 하지 않는다.
8. WBP는 배치·크기·색·폰트 같은 표시 계층만 담당하고 Event Graph Tick이나 Property Binding은 사용하지 않는다.

C++ `BindWidget`과 WBP Designer 사이의 필수 이름 계약은 다음 네 개다. 이름이나 타입을 바꾸면 WBP Compile에서 오류가 나므로 C++와 WBP를 함께 수정해야 한다.

```text
SpeedValueText
AltitudeValueText
VerticalSpeedValueText
HeadingValueText
```

Designer Tree가 없는 native `UDroneFlightHUDWidget` Class를 직접 실행할 때는 C++ 기본 레이아웃을 만든다. 정상 컴파일된 WBP는 필수 TextBlock 4개를 사용하며, 런타임에 계약이 비정상적으로 누락된 경우의 fallback은 방어 경로다. BP Asset 자체가 삭제됐을 때 Map 참조가 자동으로 native Class로 바뀐다는 뜻은 아니다.

현재 Prototype에서 채택한 표시 형식:

```text
SPD  42.5 km/h
ALT  18.2 m
V/S  +1.4 m/s
HDG  315°
```

소수점 자릿수와 3자리 Heading은 현재 읽기 쉬운 초기값이며 최종 배치·폰트·색상·Animation 계약은 아직 미정이다.

### Blueprint에서 직접 확인·수정할 위치

1. Content Browser에서 `/Game/Drone/Prototype/UI/WBP_DroneFlightHUD`를 연다.
2. Class Settings의 Parent Class가 `UDroneFlightHUDWidget`인지 확인한다.
3. Designer에서 Panel 위치·Padding·색·Font Size를 바꾼다. 네 Value TextBlock의 이름과 타입은 유지한다.
4. Event Graph에는 Tick, Pawn 검색, Text Property Binding을 추가하지 않는다. 값 갱신은 부모 C++가 처리한다.
5. `/Game/Drone/Prototype/Blueprints/BP_DronePrototypePlayerController`의 Class Defaults에서 `Flight HUD Widget Class`가 `WBP_DroneFlightHUD`인지 확인한다.
6. `/Game/Drone/Prototype/Blueprints/BP_DronePrototypeGameMode`의 Class Defaults에서 Player Controller Class가 `BP_DronePrototypePlayerController`인지 확인한다.
7. Compile 후 `Lvl_DronePrototype` PIE에서 WBP가 한 개만 나타나는지 확인한다.

화면 위치·크기·색·폰트는 WBP에서 자유롭게 조정할 수 있다. 표시 값의 의미, 단위 변환, Event 구독·해제와 Widget 생성 위치를 바꾸려면 C++ 계약과 자동화 테스트를 함께 검토한다.

## 7. 자동화와 빌드 결과

### C++ 빌드

```text
Target: DroneEditor Win64 Development
CompilerVersion argument: 14.51.36231
Reported toolchain: 14.51.36252
Result: Succeeded
```

HUD-01 검증의 첫 실행에서는 PowerShell이 따옴표 없는 CompilerVersion을 분리해 UBT Rules 인자 오류가 났다. 코드는 컴파일되지 않은 실행 명령 문제였고, 전체 버전 인자를 문자열로 전달한 뒤 빌드가 성공했다. HUD-02 최종 빌드는 위 인자로 정상 성공했다.

### 자동화

최종 `Drone.` Report:

```text
Drone.Prototype.PawnDefaults       Success
Drone.Prototype.PIEInputLifecycle  Success
Drone.Prototype.SpawnPossess       Success
Drone.Telemetry.Calculation        Success
Drone.Telemetry.Defaults           Success
Drone.UI.FlightHUDBlueprintAsset   Success
Drone.UI.FlightHUDTelemetryBinding Success
Total                              7 succeeded, 0 warnings, 0 failed
```

`SpawnPossess`는 실제 생성된 Prototype Pawn이 Telemetry Component 한 개를 소유하고 Spawn Z를 고도로 보고하며, Reference Z 변경 직후 Snapshot이 갱신되는 것까지 확인한다. `FlightHUDTelemetryBinding`은 동일 Source 중복 연결 방지, 이전 Source 해제, 새 Source 연결과 네 표시 형식을 확인한다. `FlightHUDBlueprintAsset`은 WBP의 native 부모, Designer TextBlock 4개와 Font 유효성, BP Controller가 WBP를 선택하는지, BP GameMode가 BP Controller를 선택하는지 확인한다.

`PIEInputLifecycle`은 새 PIE 3회에서 실제 `BP_DronePrototypePlayerController_C`, `WBP_DroneFlightHUD_C`, HUD 한 개, native fallback 미사용, Viewport와 현재 Telemetry 연결을 확인한다. 각 회차에서 UnPossess 시 숨김/구독 해제, 같은 Widget 재사용 Re-Possess와 구독 복구, PIE 종료 뒤 잔존 Delegate 없음까지 검증하면서 기존 Keyboard·Mouse·Gamepad 입력 회귀도 유지한다.

### Blueprint

```text
CompileAllBlueprints
0 errors
0 warnings
0 blueprints failed to load
```

### Standalone 화면

`410c940` native HUD 기준선의 Development Standalone에서 다음 변화가 보였다.

```text
초기    SPD 0.0 km/h   ALT 1.5 m   V/S +0.0 m/s
이동    SPD 43.2 km/h
상승    ALT 2.7 m      V/S +10.0 m/s
하강                    V/S -7.2 m/s
Yaw     HDG 002° → 025°/045°
```

기본 10Hz HUD에 단일 자동 입력을 확실히 포착하기 위해 실행 인자에서만 Movement 가속·감속을 임시 조정했다. 프로젝트 기본 이동값과 소스 파일은 변경하지 않았다. 기준면 아래 Altitude의 음수 보존은 `Drone.Telemetry.Calculation` 자동화에서 검증했다.

`9f91bb6` WBP/BP 보강 뒤 다시 실행한 Standalone에서는 실제 WBP Class가 사용됐고 `FLIGHT DATA`, `SPD 0.0 km/h`, `ALT 1.5 m`, `V/S +0.0 m/s`, `HDG 000°`가 깨짐 없이 표시됐다. WBP 외형은 편집 가능한 첫 패널이며 최종 아트 디자인으로 확정한 것은 아니다.

## 8. 현재 경계와 다음 작업

`HUD-01` 데이터 공급 계층과 `HUD-02` C++ 기능·WBP 표시 계층, `TUT-01` Training Course, `TUT-02` Ordered Ring Gate와 `TUT-03` Segment/Lap 원본 기록을 완료했다. 현재 Unreal 기준 Commit은 `551e287`이며 로컬 `main`과 `origin/main`에 반영됐다. Lap Recorder는 이 문서의 10Hz Telemetry Event를 위치 표본 시계로 재사용한다. 다음 활성 카드는 `TUT-04` 이전 기록 비교·Best·결과 UI다. TUT-03의 구현·검증 기준은 [`DRONE_TRAINING_RECORDING_IMPLEMENTATION.md`](DRONE_TRAINING_RECORDING_IMPLEMENTATION.md)를 따른다.

아직 포함하지 않는 항목:

- 최종 HUD 디자인과 Animation
- 배터리·신호·Jamming 표시
- 지형 Line Trace 기반 AGL
- SaveGame 기록
- 이전 기록 평균·Best 비교와 Tutorial 결과 UI
