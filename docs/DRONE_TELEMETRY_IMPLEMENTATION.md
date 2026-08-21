# Drone Telemetry 구현 및 검증 기록

기준일: 2026-08-21 (Asia/Seoul)

## 1. 현재 결과

`HUD-01`의 공용 Telemetry Snapshot과 `UDroneTelemetryComponent`를 구현했다. Component는 Prototype Pawn에 기본 부착되며, 매 프레임 Tick 대신 0.1초 Timer를 사용해 10Hz로 Snapshot을 갱신하고 Blueprint Event를 보낸다.

현재 제공 값은 다음 네 가지다.

| 값 | 단위 | 계산 |
|---|---|---|
| Speed | km/h | `Velocity.Size() × 0.036` |
| Altitude | m | `(Actor Z - Reference Z) × 0.01` |
| Vertical Speed | m/s | `Velocity.Z × 0.01` |
| Heading | degree | Actor Yaw를 `0~359°`로 정규화 |

## 2. 실제 코드 위치

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

공용 Flight HUD는 다음 방식으로 연결한다.

1. 현재 Possess한 Drone에서 `UDroneTelemetryComponent`를 가져온다.
2. `OnTelemetryUpdated`를 한 번만 구독한다.
3. 새 Snapshot을 받으면 네 Text 값을 갱신한다.
4. Pawn 전환·Widget 종료 시 기존 Component Event를 해제한다.
5. Widget은 표시 자릿수와 색상만 담당하고 단위 변환은 하지 않는다.

초기 표시 후보:

```text
SPD  42.5 km/h
ALT  18.2 m
V/S  +1.4 m/s
HDG  315°
```

## 7. 자동화와 빌드 결과

### C++ 빌드

```text
Target: DroneEditor Win64 Development
CompilerVersion: 14.51.36256
Result: Succeeded
```

첫 실행은 PowerShell이 따옴표 없는 CompilerVersion을 분리해 UBT Rules 인자 오류가 났다. 코드는 컴파일되지 않은 실행 명령 문제였고, 전체 버전 인자를 문자열로 전달한 뒤 빌드가 성공했다.

### 자동화

최종 `Drone.` Report:

```text
Drone.Prototype.PawnDefaults       Success
Drone.Prototype.PIEInputLifecycle  Success
Drone.Prototype.SpawnPossess       Success
Drone.Telemetry.Calculation        Success
Drone.Telemetry.Defaults           Success
Total                              5 succeeded, 0 warnings, 0 failed
```

`SpawnPossess`는 실제 생성된 Prototype Pawn이 Telemetry Component 한 개를 소유하고 Spawn Z를 고도로 보고하며, Reference Z 변경 직후 Snapshot이 갱신되는 것까지 확인한다.

### Blueprint

```text
CompileAllBlueprints
0 errors
0 warnings
0 blueprints failed to load
```

## 8. 현재 경계와 다음 작업

`HUD-01`은 C++ 데이터 공급 계층까지 완료한다. 다음 `HUD-02`에서 UMG Widget과 화면 배치를 만들고 Standalone에서 실제 숫자가 이동에 따라 변하는지 확인한다.

아직 포함하지 않는 항목:

- 최종 HUD 디자인과 Animation
- 배터리·신호·Jamming 표시
- 지형 Line Trace 기반 AGL
- SaveGame 기록
- Tutorial Lap/Segment 통계
