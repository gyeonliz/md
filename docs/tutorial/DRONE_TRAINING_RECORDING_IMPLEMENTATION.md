# TUT-03 Training Lap·Segment 기록 구현 가이드

기준일: 2026-08-27 (Asia/Seoul)

Unreal 구현 기준: `551e287e8a5de7fa33f28d1911f8a7a957bd66fa` (`feat: record tutorial lap timing and distance`)

이 문서는 TUT-03에서 실제 구현한 Lap·Segment 원본 기록 계층을 설명한다. 2026-08-26에는 이 원본을 기존 Flight HUD에 연결했고, 2026-08-27에는 TUT-04B로 현재 시도를 제외한 이전 성공 평균·Best·Delta와 Segment 비교를 추가했다. `USaveGame` 영속화와 점수는 아직 만들지 않았다.

## 1. 왜 필요한가

TUT-02까지는 Drone이 현재 순서의 Gate를 정방향으로 통과했는지만 판정했다. 마지막 Gate까지 통과해도 다음 정보는 남지 않았다.

- Gate 사이를 이동한 시간
- Gate 사이에서 Drone이 실제로 움직인 거리
- 구간 평균 속도
- Gate 0부터 마지막 Gate까지의 전체 Lap 기록
- 성공한 Lap의 현재 실행 중 원본 History

이 계산을 Gate Actor나 HUD에 직접 넣으면 순서 판정, 기록 계산, 화면 표시 책임이 섞인다. TUT-03은 이를 피하기 위해 Course가 별도 `UDroneTrainingLapRecorderComponent`를 소유하게 하고, 기존 Gate Sequence의 정상 승인 Event만 기록 입력으로 사용한다.

```text
Gate Begin/End Overlap
→ Gate Sequence가 순서·정방향 판정
→ 정상 승인만 OnGateAccepted Broadcast
→ Lap Recorder가 시간·위치 표본을 기록
→ Segment/Lap 원본 Record 생성
→ Blueprint Event와 Getter로 후속 UI에 전달
```

잘못된 순서, 역방향, 중복 통과처럼 Sequence가 거부한 시도는 `OnGateAccepted`가 발생하지 않으므로 새 Segment 경계나 성공 기록을 만들지 않는다. 다만 이미 Lap을 기록 중이라면 World Game Time과 Telemetry 위치 표본은 계속 누적되므로, 잘못된 Gate까지 비행한 시간과 이동 경로도 현재 시도에 포함된다.

## 2. 이번 구현 파일

```text
Source/Drone/Tutorial/
├─ DroneTrainingRecordTypes.h
├─ DroneTrainingLapRecorderComponent.h
├─ DroneTrainingLapRecorderComponent.cpp
├─ DroneTrainingCourse.h                         수정
├─ DroneTrainingCourse.cpp                       수정
├─ DroneTrainingGateTypes.h                      수정
├─ DroneTrainingGateSequenceComponent.h          수정
├─ DroneTrainingGateSequenceComponent.cpp        수정
└─ Tests/
   ├─ DroneTrainingRecordCalculationTest.cpp
   ├─ DroneTrainingLapRecorderTest.cpp
   ├─ DroneTrainingAssetTest.cpp                 보강
   └─ DroneTrainingPIESmokeTest.cpp              보강
```

Commit `551e287`은 C++ Source와 테스트만 변경했다. TUT-03 때문에 새 Blueprint Asset이나 Map Asset을 만들지는 않았다.

## 3. 클래스별 책임

| 클래스·구조체 | 담당 책임 | 담당하지 않는 책임 |
|---|---|---|
| `ADroneTrainingGate` | Pawn Overlap 수집, 진입·이탈 위치를 Sequence에 전달 | 시간·거리·평균 속도 계산 |
| `UDroneTrainingGateSequenceComponent` | Gate 구성 검증, 현재 Gate, 순서·정방향·중복 판정, Reset | Lap 계산, History, 결과 UI |
| `UDroneTrainingLapRecorderComponent` | 정상 Gate Event 구독, Segment/Lap 원본, 이전 평균·Best·Delta 비교 생성 | 점수, SaveGame |
| `ADroneTrainingCourse` | Sequence와 Recorder를 함께 소유하고 런타임 연결 | 직접 기록 계산 |
| `UDroneTelemetryComponent` | 기존 10Hz `OnTelemetryUpdated` Event 제공 | Segment 경계와 Lap 상태 결정 |
| `FDroneTrainingSegmentRecord` | 완료된 한 구간의 원본 값 보관 | 비교·표시 문자열 생성 |
| `FDroneTrainingLapRecord` | 완료된 한 Lap과 그 Segment 배열 보관 | 영구 저장 |
| `FDroneTrainingLapComparison` | 현재 Lap, 이전 평균, Best, Delta와 Segment 비교 보관 | 영구 저장·점수 규칙 |

핵심 원칙은 다음과 같다.

- Gate Sequence는 계속 통과 판정만 담당한다.
- Lap Recorder는 별도 Tick이나 Timer를 만들지 않는다.
- 이동 위치는 기존 Telemetry의 기본 10Hz Event가 갱신할 때 표본화한다.
- HUD는 계산하지 않고 후속 카드에서 Event와 Getter가 제공한 값을 표시한다.

## 4. 기록 데이터 계약

### `EDroneTrainingLapRecordState`

| 상태 | 의미 |
|---|---|
| `Idle` | 진행 중 Lap이 없음. 유효한 Gate가 2개 이상이고 Sequence가 Gate 0을 기다리면 시작 준비 상태 |
| `Recording` | Gate 0을 정상 통과한 Drone의 현재 Lap을 기록 중 |
| `Completed` | 마지막 Gate까지 정상 통과한 Lap을 성공 History에 저장한 상태 |

완료 뒤 같은 Course에서 새 Lap을 시작하려면 `ResetSequence()`로 Gate 진행을 Gate 0으로 되돌려야 한다.

### `FDroneTrainingSegmentRecord`

| 값 | 단위·의미 |
|---|---|
| `SegmentIndex` | 0부터 시작하는 Segment 배열 위치 |
| `FromGateIndex` | 구간 시작 Gate Index |
| `ToGateIndex` | 구간 종료 Gate Index |
| `ElapsedSeconds` | World Game Time 기준 구간 시간, 초 |
| `TravelDistanceMeters` | 3차원 World 위치 표본 사이 거리를 합한 값, m |
| `AverageSpeedKilometersPerHour` | 구간 이동 거리 ÷ 구간 시간, km/h |

Gate 0은 출발선이다. Gate가 `N`개라면 기록되는 Segment는 `N-1`개다.

```text
Gate 0 승인: Lap 시작, 완료 Segment 0개
Gate 1 승인: Segment 0 = Gate 0 → Gate 1
Gate 2 승인: Segment 1 = Gate 1 → Gate 2
...
마지막 Gate 승인: 마지막 Segment 확정 뒤 Lap 완료
```

현재 Training Map의 Gate는 4개이므로 정상 Lap 한 번에는 Segment가 3개 생긴다. Gate 0 이전 이동은 Lap 시간과 거리에 포함하지 않는다.

### `FDroneTrainingLapRecord`

| 값 | 단위·의미 |
|---|---|
| `bCompleted` | 마지막 Gate까지 유효하게 완료했는지 표시 |
| `ElapsedSeconds` | Gate 0 승인부터 마지막 Gate 승인까지의 World Game Time, 초 |
| `TravelDistanceMeters` | 같은 기간에 누적한 전체 3차원 이동 거리, m |
| `AverageSpeedKilometersPerHour` | 전체 이동 거리 ÷ 전체 Lap 시간, km/h |
| `Segments` | 순서대로 완료된 `N-1`개 Segment 원본 배열 |

시간은 `UWorld::GetTimeSeconds()`를 사용하므로 Pause와 Time Dilation의 영향을 받는다. 거리는 Gate의 `SegmentDistance` 메타데이터가 아니라 실제 Drone 위치 표본을 이어 붙인 3차원 경로 길이다. 현재 10Hz 표본 사이에서 일어난 세부 곡선 이동은 표본 간 직선으로 근사한다.

평균 속도 계산식은 다음과 같다.

```text
거리 cm × 0.01 = 거리 m
거리 m ÷ 시간 s = m/s
m/s × 3.6 = km/h
```

거리나 시간이 0 이하이거나 NaN·무한대라면 평균 속도는 안전하게 `0.0`을 반환한다.

## 5. 헤더에 추가된 핵심

### Record Type

`DroneTrainingRecordTypes.h`에는 다음 Blueprint Type을 추가했다.

- `EDroneTrainingLapRecordState`
- `FDroneTrainingSegmentRecord`
- `FDroneTrainingLapRecord`
- `FDroneTrainingLapStartedSignature`
- `FDroneTrainingSegmentRecordedSignature`
- `FDroneTrainingLapCompletedSignature`

Record의 필드는 `BlueprintReadOnly`다. Blueprint는 완료된 원본 값을 읽을 수 있지만 C++ 계산 결과를 임의로 덮어쓰는 구조는 아니다.

### Lap Recorder Component

`UDroneTrainingLapRecorderComponent`는 `BlueprintType`, `BlueprintSpawnableComponent`지만 실제 Training Course에서는 native 기본 Subobject로 한 개를 소유한다.

주요 내부 상태는 다음과 같다.

- 연결된 `GateSequence`
- Gate 0을 통과한 `ActiveDrone`
- 위치 표본 Event를 제공하는 `ActiveTelemetry`
- `Idle`, `Recording`, `Completed` 상태
- 현재 Lap의 완료 Segment 배열
- 현재 실행 동안의 성공 Lap 배열
- Lap/Segment 시작 시간
- Lap/Segment 누적 거리
- 마지막 정상 Gate Index와 마지막 위치 표본

### Gate Sequence Event 확장

`OnGateAccepted`는 TUT-03 기록에 필요한 정보를 전달하도록 다음 네 값을 제공한다.

```text
Gate
PassingActor
AcceptedGateCount
AcceptedWorldLocation
```

`AcceptedWorldLocation`은 정상 관통이 승인된 Gate 이탈 위치다. 또한 Sequence에 다음 두 Event를 추가했다.

- `OnSequenceReset`: Restart 또는 구성 무효화로 부분 시도를 폐기할 때 사용
- `OnSequenceReconfigured`: Gate 배열·Course 구성이 다시 적용되어 기존 기록 기준이 달라졌을 때 사용

`ResetSequence()`는 Gate 진행과 진행 중 Overlap을 초기화한 뒤 `OnSequenceReset`을 보낸다. 재구성은 `OnSequenceReconfigured`를 보낸다.

### Course 연결

`ADroneTrainingCourse`는 생성자에서 `LapRecorderComponent`를 만들고 `PostInitializeComponents()`의 Game World 경로에서 Recorder와 Gate Sequence를 연결한다. 따라서 Blueprint `BeginPlay`나 초기 Overlap보다 먼저 기록 구독을 준비한다.

## 6. CPP의 실제 처리 순서

### 시작

```text
Gate 0 정상 승인
→ PassingActor를 ADronePrototypePawn으로 확인
→ Pawn의 UDroneTelemetryComponent 확인
→ Gate 0 승인 시간·이탈 위치를 시작 기준으로 저장
→ Telemetry OnTelemetryUpdated와 Pawn OnDestroyed 구독
→ RecordState = Recording
→ OnLapStarted Broadcast
```

Recorder는 Gate가 두 개 이상인 유효한 Sequence에서만 준비된다. Gate 0을 통과한 Pawn과 같은 Pawn만 이후 Gate 기록을 이어 갈 수 있다.

### 거리 표본

Telemetry Event가 올 때마다 현재 Drone의 Actor Location을 읽는다. Snapshot 안의 속도 값을 적분하지 않는다.

```text
현재 위치와 직전 위치의 FVector::Distance
→ LapDistanceCentimeters에 더함
→ SegmentDistanceCentimeters에 더함
→ 현재 위치를 다음 표본 기준으로 저장
```

정상 Gate 승인 시에도 Gate의 승인 위치를 마지막 표본으로 한 번 추가해 Segment 끝을 Gate 이탈 위치에 맞춘다.

### Segment 확정

Gate 1 이후 정상 Gate가 승인되면 다음을 수행한다.

1. 현재 Gate 승인 시간에서 Segment 시작 시간을 뺀다.
2. 시간이 0보다 큰 유효 값인지 확인한다.
3. `FromGateIndex`, `ToGateIndex`, 시간, 거리, 평균 속도를 Record에 저장한다.
4. 현재 Segment 배열에 추가한다.
5. 다음 Segment의 시간·거리 기준을 초기화한다.
6. `OnSegmentRecorded`로 완료된 Record를 전달한다.

같은 Frame에서 Gate를 연속 직접 승인해 시간이 사실상 0이면 유효한 비행 기록으로 저장하지 않고 현재 시도를 취소한다.

### Lap 완료

마지막 Gate 승인 뒤 완료 Segment 수가 `Gate 수 - 1`과 일치하고 Lap 시간이 유효하면 다음을 수행한다.

1. 전체 시간·거리·평균 속도와 Segment 배열을 `FDroneTrainingLapRecord`에 저장한다.
2. `bCompleted`를 `true`로 설정한다.
3. 현재 실행의 `SuccessfulLaps`에 추가한다.
4. Telemetry와 Pawn 파괴 Event 구독을 해제한다.
5. 상태를 `Completed`로 바꾼다.
6. 진행 중 임시 값을 정리한다.
7. `OnLapCompleted`로 완성된 불변 Record를 전달한다.

마지막 Gate에서는 `OnSegmentRecorded`가 먼저 발생하고 그 다음 `OnLapCompleted`가 발생한다.

### 취소와 Reset

- 잘못된 Gate 시도는 Sequence에서 거부되므로 Recorder에 도착하지 않는다.
- Sequence Reset은 현재 부분 시도를 폐기하지만 이미 완료된 성공 History는 유지한다.
- Course Gate 구성이 다시 적용되면 현재 시도와 이전 성공 History를 모두 비운다.
- 기록 중인 Drone이 파괴되면 Telemetry 구독과 부분 시도를 정리하고 성공 Lap을 만들지 않는다.
- Component `EndPlay`에서는 활성 구독을 모두 해제한다.

## 7. Blueprint에 공개된 Event와 Getter

### Course에서 Recorder 얻기

`ADroneTrainingCourse::GetLapRecorderComponent()`는 `BlueprintPure`다. Course Blueprint나 후속 HUD 연결 계층에서 이 Getter로 Recorder를 얻는다.

### Blueprint Event

| Event | 전달 값 | 발생 시점 |
|---|---|---|
| `OnLapStarted` | 없음 | Gate 0 정상 승인 뒤 Recording 상태가 확정된 직후 |
| `OnSegmentRecorded` | `FDroneTrainingSegmentRecord` | Gate 1 이후 각 정상 Gate에서 Segment 저장 직후 |
| `OnLapCompleted` | `FDroneTrainingLapRecord` | 마지막 Gate에서 성공 History 저장과 Completed 상태 확정 뒤 |

Event는 상태를 먼저 반영한 뒤 Broadcast한다. Blueprint가 Event 안에서 Getter를 호출해도 이미 갱신된 값을 읽는다.

### BlueprintPure Getter

| Getter | 의미 |
|---|---|
| `GetRecordState()` | `Idle`, `Recording`, `Completed` 상태 |
| `IsRecordingReady()` | 유효한 Gate가 2개 이상이고 Gate 0 시작 전인지 확인 |
| `IsLapRecording()` | 현재 Lap 기록 중인지 확인 |
| `HasCompletedLap()` | 현재 실행에 성공 Lap이 하나 이상 있는지 확인 |
| `GetSuccessfulLapCount()` | 현재 실행의 성공 Lap 수 |
| `GetSuccessfulLaps()` | 현재 실행 동안 완료된 모든 원본 Lap 배열 |
| `GetLastCompletedLap()` | 마지막 성공 Lap. 없으면 기본값 Record |
| `GetCurrentLapElapsedSeconds()` | Recording 중 현재 Lap 시간. 다른 상태에서는 0 |
| `GetCurrentSegmentElapsedSeconds()` | Recording 중 현재 Segment 시간. 다른 상태에서는 0 |
| `GetCurrentLapTravelDistanceMeters()` | Recording 중 현재 Lap 누적 거리. 다른 상태에서는 0 |
| `GetCurrentSegmentTravelDistanceMeters()` | Recording 중 현재 Segment 누적 거리. 다른 상태에서는 0 |
| `GetRecordedSegmentCount()` | 현재 진행 중 Lap에서 이미 완료된 Segment 수 |

완료 화면은 `Completed` 상태에서 Current Getter가 0인 것을 오류로 보지 말아야 한다. 완료 값은 `OnLapCompleted`의 Event 인자 또는 `GetLastCompletedLap()`에서 읽는다.

`CalculateAverageSpeedKilometersPerHour()`는 C++의 정적 계산 함수이며 현재 Blueprint 함수로 노출하지 않았다. Blueprint는 Record에 이미 계산된 km/h 값을 사용한다.

### Reset 연결

`UDroneTrainingGateSequenceComponent::ResetSequence()`는 `BlueprintCallable`이다. 후속 Restart 버튼이나 입력은 Course의 Gate Sequence를 얻어 이 함수를 호출해야 한다. Recorder를 별도로 수동 초기화하지 않아도 `OnSequenceReset`을 받아 부분 시도를 함께 취소한다.

현재는 Restart 버튼이나 입력 UI를 연결하지 않았다.

## 8. Editor 수동 테스트

### 준비

1. UE 5.8.1에서 프로젝트를 연다.
2. `/Game/Drone/Maps/Lvl_DroneTraining`을 연다.
3. World Outliner에서 `BP_DroneTrainingCourse`를 선택한다.
4. Course의 `OrderedGates`가 Gate 0, 1, 2, 3 순서인지 확인한다.
5. PIE를 시작하고 Gate 0이 Current 상태인지 확인한다.

현재 Flight HUD는 Training Course의 Recorder를 자동으로 찾아 최근 정상 구간 통계와 완료 구간 평균을 한글로 표시한다. TUT-04B 이후에는 이전 완주 평균, Best, 시간·속도 Delta도 표시한다. 원본 검증은 기존 세 Event와 `OnLapComparisonReady`, `FDroneTrainingLapComparison`을 확인한다.

### 정상 Lap

1. Gate 0을 Actor 로컬 `+X` 방향으로 완전히 통과한다.
2. `OnLapStarted`가 한 번 발생하고 Segment 결과는 아직 없는지 확인한다.
3. Gate 1로 가는 동안 좌우 또는 상하로 경로를 조금 꺾어 실제 이동 거리가 누적되게 한다.
4. Gate 1을 정상 통과한다.
5. `OnSegmentRecorded`가 한 번 발생하고 `FromGateIndex=0`, `ToGateIndex=1`인지 확인한다.
6. Gate 2와 Gate 3도 차례로 정상 통과한다.
7. Gate 3에서 세 번째 `OnSegmentRecorded` 뒤 `OnLapCompleted`가 발생하는지 확인한다.
8. 완료 Record의 `Segments`가 3개이고 시간·거리·평균 속도가 유한한 양수인지 확인한다.

### 거부 흐름

1. 새 PIE에서 Gate 1을 먼저 통과한다.
2. Recorder가 `Idle`이고 Event가 발생하지 않는지 확인한다.
3. Gate 0을 역방향으로 통과한다.
4. Recorder 상태와 History가 바뀌지 않는지 확인한다.
5. Gate 0을 정상 통과한 뒤 Gate 0을 다시 통과한다.
6. 중복 통과로 Segment가 생기지 않는지 확인한다.

### Reset 흐름

현재 사용자용 Restart 입력은 없으므로 Blueprint 임시 Debug 경로 또는 자동화 테스트에서 `GetGateSequenceComponent() → ResetSequence()`를 호출한다.

1. Gate 0을 통과하고 일부 이동한다.
2. `ResetSequence()`를 호출한다.
3. Recorder가 `Idle`, 완료 Segment 수가 0, 현재 거리와 시간이 0으로 돌아가는지 확인한다.
4. 이전에 완료한 성공 Lap이 있었다면 성공 History는 유지되는지 확인한다.
5. Gate 0부터 새 시도를 시작할 수 있는지 확인한다.

PIE를 끝내면 현재 실행 전용 History는 사라진다. 이는 SaveGame이 없는 현재 범위의 정상 동작이다.

## 9. 정상 결과

- Gate 0 승인 전 Recorder는 `Idle`이며 유효한 Course에서는 시작 준비 상태다.
- Gate 0 승인 직후 `Recording`이 되고 완료 Segment는 0개다.
- Gate 1부터 정상 Gate마다 Segment가 정확히 한 개씩 추가된다.
- Gate 4개인 Training Map은 성공 Lap마다 Segment 3개를 만든다.
- 마지막 Gate 승인 뒤 상태는 `Completed`이고 성공 Lap 수가 증가한다.
- Segment 시간 합은 Lap 시간과 일치하고 Segment 거리 합은 Lap 거리와 일치한다.
- 거리는 수평 이동뿐 아니라 상승·하강을 포함한 3차원 표본 경로다.
- 평균 속도는 m/s가 아니라 km/h로 저장된다.
- 잘못된 순서·역방향·중복 통과는 Segment/Lap 완료 Event나 새 Gate 경계를 만들지 않는다. 기록 중 실제로 이동했다면 그 시간과 3차원 경로는 현재 시도에 계속 포함된다.
- Reset은 부분 시도만 폐기하고 성공 History를 보존한다.
- Course 재구성은 비교 기준이 달라졌으므로 성공 History도 비운다.
- 화면에 결과 HUD·Toast·Best 비교가 나오지 않는 것이 현재 정상이다.

## 10. 문제가 생겼을 때 확인할 항목

### Gate 0을 통과해도 기록이 시작되지 않음

1. Course의 Gate Sequence 구성이 유효한지 확인한다.
2. `OrderedGates`가 최소 2개인지 확인한다.
3. 현재 기대 Gate가 Gate 0인지 확인한다.
4. Gate를 로컬 `+X` 정방향으로 완전히 빠져나왔는지 확인한다.
5. 통과 Actor가 `ADronePrototypePawn`의 자식인지 확인한다.
6. Pawn이 `UDroneTelemetryComponent`를 소유하는지 확인한다.
7. Course가 `GetLapRecorderComponent()`에서 유효한 Component를 반환하는지 확인한다.

### Gate를 통과했는데 Segment가 저장되지 않음

1. Gate 0은 출발선이라 Segment를 만들지 않는 것이 정상인지 확인한다.
2. 현재 Gate를 순서대로 통과했는지 확인한다.
3. Gate 0을 통과한 것과 같은 Drone이 다음 Gate를 통과했는지 확인한다.
4. 두 Gate 승인이 같은 Frame에 직접 실행되어 구간 시간이 0이 되지 않았는지 확인한다.
5. 중간에 Sequence Reset·Course 재구성·Drone 파괴가 발생하지 않았는지 확인한다.

### 이동 거리가 0이거나 기대보다 작음

1. Gate 0 이전 이동은 기록하지 않는다는 점을 확인한다.
2. Telemetry의 `OnTelemetryUpdated`가 기본 10Hz로 발생하는지 확인한다.
3. 기록 중인 Pawn의 Actor Location이 실제로 변하는지 확인한다.
4. 10Hz 표본 사이의 곡선은 직선으로 근사하므로 매우 빠른 세부 움직임은 짧게 계산될 수 있음을 확인한다.
5. Gate의 `SegmentDistance`는 현재 실제 이동 거리 계산에 사용하지 않는다는 점을 확인한다.

### 완료 뒤 Current Getter가 0을 반환함

`GetCurrent...` Getter는 Recording 중 값만 제공한다. 완료 값은 `OnLapCompleted` 인자, `GetLastCompletedLap()` 또는 `GetSuccessfulLaps()`에서 읽는다.

### Reset 뒤 성공 기록이 사라짐

일반 `ResetSequence()`는 성공 History를 보존한다. Course의 Gate 배열을 다시 구성했다면 `OnSequenceReconfigured`가 발생해 기존 Course 기준의 성공 History까지 비우는 것이 정상이다. PIE 종료도 현재 실행 전용 History를 제거한다.

### Event가 중복 발생함

Recorder의 `InitializeRecorder()`는 `AddUniqueDynamic`으로 구독하고 EndPlay 때 해제한다. Blueprint에서 같은 Event를 여러 경로로 다시 Bind하지 않았는지 확인한다. Recorder 자체 Tick이나 별도 Timer를 추가하지 않는다.

## 11. 검증 결과

Commit `551e287` 기준 최종 검증 결과는 다음과 같다.

- `DroneEditor Win64 Development` Editor Build 성공
- `Drone.Tutorial` 자동화 테스트 `6/6` 성공
- 전체 `Drone.` 자동화 테스트 `14/14` 성공
- Blueprint Compile `0 errors / 0 warnings / 0 load failures`

TUT-03에서 추가·보강한 주요 자동화 범위는 다음과 같다.

- cm·초를 km/h로 바꾸는 계산과 0·음수·NaN·무한대 입력 안전 처리
- Gate 0 시작, Gate `N`개에서 Segment `N-1`개 생성
- World Game Time 기반 Segment/Lap 시간
- Telemetry 위치 표본의 꺾인 3차원 경로 합산
- Segment 합과 Lap 합의 일치
- 미래 Gate·역방향·중복 통과가 기록을 바꾸지 않음
- 성공 History 저장, Reset의 History 보존, 재구성의 History 제거
- 진행 중 Drone 파괴 시 부분 시도와 Delegate 정리
- 실제 Training Map Course가 Recorder를 소유하고 Tick을 사용하지 않음
- 실제 BP Gate Overlap으로 Gate 0 승인 시 Lap 기록 시작

## 12. 이번 범위에 포함하지 않은 것

다음 항목은 TUT-03에서 구현하지 않았다.

- Course HUD의 현재 Lap Time·현재 Segment Time 표시
- Gate 결과 Toast와 Lap 결과 표
- 첫 성공 시도의 `기준 기록 생성 중` 표시
- 이전 성공 기록 평균 계산과 현재 시도 Delta
- Best Lap과 Gate별 Best Segment
- 점수·등급·평가 공식
- `USaveGame` 기반 Course별 영구 기록
- Restart 버튼·키 입력과 사용자 메시지
- Network Replication과 Multiplayer 권한 처리
- 최종 HUD 디자인, Animation, VFX, SFX

`SuccessfulLaps`, 완료 Event와 Getter는 TUT-04가 이전 평균·Best·결과 UI를 만들 때 사용할 원본 경계다. 원본 계산을 Widget에서 다시 구현하거나 Property Binding으로 Pawn을 매 Frame 검색하지 않는다.

## 13. 다음 작업 경계

다음 카드는 `TUT-04 비교와 결과 UI`다.

```text
TUT-03 원본 Record와 Event
→ 이전 성공 기록 평균 계산
→ Best Lap·Gate별 Best Segment 계산
→ 현재 결과와 이전 평균·Best Delta 생성
→ Course HUD·Segment Toast·Lap 결과 UI 표시
```

SaveGame은 런타임 계산과 UI 비교가 검증된 뒤 별도 단계로 연결한다.
