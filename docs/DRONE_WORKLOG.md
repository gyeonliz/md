# Drone 개발 진행 기록

기준일: 2026-08-23 (Asia/Seoul)

이 문서는 Drone 개발의 **진행 이력**을 시간순으로 남긴다. 가장 최신의 현재 상태는 [`../WORKBOARD.md`](../WORKBOARD.md), 확정 구현 순서는 [`DRONE_TUTORIAL_STORY_PLAN.md`](DRONE_TUTORIAL_STORY_PLAN.md)를 따른다.

## 갱신 규칙

Drone 코드·자산·계획 작업을 진행할 때마다 작업 종료 전에 Markdown을 함께 갱신한다.

1. `WORKBOARD.md`: 현재 단계, 지금 작업 중인 카드, 완료 근거, 남은 조건과 바로 다음 작업
2. `DRONE_WORKLOG.md`: 실제 변경, 검증 결과, 발견한 문제와 다음 행동을 날짜순으로 추가
3. `STATUS.md`: 빌드·테스트·자산 수처럼 검증된 기준선이 달라졌을 때 갱신
4. `CONTEXT.md`: 사용자가 확정한 방향, 장기 규칙과 범위가 달라졌을 때 갱신
5. 계획 문서: 구현 순서, 완료 조건이나 설계가 달라졌을 때 같은 작업에서 갱신

진행률은 근거 없는 전체 백분율로 표시하지 않는다. 대신 `현재 단계`, `통과한 게이트/전체 게이트`, `Doing`, `다음 활성 카드`로 기록한다. 자동화가 통과해도 필수 수동 확인이 남아 있으면 완료로 이동하지 않는다.

## 현재 스냅샷

마지막 갱신: 2026-08-23 15:42 KST

| 구분 | 현재 상태 |
|---|---|
| 전체 단계 | 3단계 Tutorial Vertical Slice — `TUT-01` 완료, `TUT-02` Todo |
| PFN-06 진행도 | 필수 게이트 5/5 Pass, Done |
| 지금 작업 중 | 없음. 다음 카드 `TUT-02`의 담당자는 현재 미정 |
| 차단 조건 | 없음. Android는 사용자 결정에 따라 작업 범위에서 제외 |
| 다음 행동 | `TUT-02` 순서형 Ring Gate의 Trigger·순서·방향 판정 설계와 구현 |
| 다음 기능 | `TUT-02` 순서형 Ring Gate. Gate·Trigger·순서·방향·Lap·Timing은 현재 미구현 |
| 이후 | `TUT-03~04` Lap/Segment 기록·결과 UI → Flight 상태 → Operator↔Drone → Story/NPC/Mission/Jamming |

## 2026-08-21 — Camera·Mouse·Gamepad 기준선 갱신

### 실제 변경

- SpringArm을 Controller 자유 회전에서 Drone Yaw를 따르는 고정 추적 Camera로 변경
- Mouse X를 Drone Actor Yaw, Mouse Y를 CameraBoom Pitch로 분리
- Gamepad Left Stick 이동, `RT/LT` 고도, Right Stick X Yaw, Right Stick Y Camera Pitch 추가
- Input Action을 5개, IMC Mapping을 15개로 확장
- PIE lifecycle 테스트를 Keyboard·Mouse·Gamepad와 복합·반대 입력까지 확장
- Tutorial·Story 공통 구조와 실행 순서를 `DRONE_TUTORIAL_STORY_PLAN.md`로 확정

### 검증 결과

- `DroneEditor Win64 Development` 빌드 성공
- Blueprint 전체 Compile: 0 errors, 0 warnings
- `PawnDefaults`, `PIEInputLifecycle`, `SpawnPossess`: 3 succeeded, 0 failed
- 새 PIE 3회에서 입력과 IMC 중복 없음 확인
- Prototype 자산 9개, Input Action 5개, Mapping 15개 확인
- `/Game/Drone`에서 동결한 Legacy 자산으로 향하는 의존성 0개
- 기존 ThirdPerson 기본 Map 로드 유지
- 두 저장소 `git diff --check` 통과

### 남은 작업

- 사용자 수동 확인으로 Camera·Keyboard·Mouse 조작 수정이 정상임을 확인함
- 실제 Gamepad가 연결되어 있으면 Stick·Trigger 체감 확인하고, 없으면 `미확인`으로 기록
- 창 닫기 뒤 `Win RequestExit`, `Game engine shut down`, `Exiting` 로그와 프로세스 종료를 확인함
- PFN-06을 Done으로 판정

### 다음 구현

PFN-06 통과 후 `HUD-01`을 시작한다. Drone Telemetry를 10Hz Snapshot으로 제공하고 속도·고도·수직 속도·Heading을 공용 HUD에 표시한다.

### 수동 판정 마감

- 사용자 보고: 조작 수정 정상
- 종료 방식: `Esc`가 아닌 창 닫기
- 로그 판정: 정상 종료, Fatal·Assertion 없음
- Gamepad 체감: 연결 여부 미보고로 미확인
- 최종 판정: PFN-06 Done, `HUD-01` Ready
- Unreal 로컬 Commit: `2c38ebf` (`feat: finalize prototype camera and input lifecycle`)
- 원격 Push: 수행하지 않음

## 2026-08-21 — HUD-01 시작

### 현재 설계

- 공용 Snapshot은 속도 km/h, 기준면 대비 고도 m, 수직 속도 m/s, Heading 0~359°를 가진다.
- `UDroneTelemetryComponent`가 0.1초 간격으로 값을 갱신하고 Blueprint가 구독할 수 있는 Event를 보낸다.
- Component는 Prototype Pawn에 기본 부착하되 `/Source/Drone/Telemetry`의 재사용 가능한 생산 코드로 만든다.
- 고도는 매번 지형을 Trace하지 않고 Course/Mission이 지정하는 기준 World Z 대비로 계산한다. Tutorial 코스가 만들어지면 시작 Pad 또는 Course 기준면을 전달한다.
- Widget은 값을 계산하거나 매 프레임 Pawn을 검색하지 않는다. `HUD-02`에서 Snapshot Event를 구독한다.

### 이번 완료 조건

- Telemetry 계산과 10Hz 기본값 자동화 통과
- Prototype Pawn이 Component를 한 개 소유
- `DroneEditor Win64 Development` 빌드 성공
- 기존 Prototype 자동화 회귀 통과
- 검증 뒤 `HUD-01` Done, `HUD-02` Ready로 문서 갱신

### 구현 결과

- `FDroneTelemetrySnapshot`에 Speed km/h, Altitude m, Vertical Speed m/s, Heading degree를 정의했다.
- `UDroneTelemetryComponent`가 BeginPlay 즉시 한 번, 이후 0.1초 Timer로 Snapshot을 갱신한다.
- `OnTelemetryUpdated` Blueprint Event와 최신 Snapshot Getter를 제공한다.
- Course/Mission 기준 World Z를 런타임에 설정하면 즉시 Snapshot을 다시 계산한다.
- Prototype Pawn이 Component 한 개를 native 기본 Subobject로 소유한다.

### 검증 결과

- 최종 `DroneEditor Win64 Development` 빌드 성공
- `Drone.Telemetry.Calculation`, `Drone.Telemetry.Defaults` 통과
- `PawnDefaults`, `PIEInputLifecycle`, `SpawnPossess` 회귀 포함 최종 Report 5 succeeded, 0 warnings, 0 failed
- Runtime Spawn Pawn의 Component 존재, Spawn 고도와 Reference Z 변경 즉시 갱신 확인
- Blueprint 전체 Compile 0 errors, 0 warnings, failed load 0
- 첫 빌드 시 따옴표 없는 CompilerVersion을 PowerShell이 분리한 명령 오류가 있었고, 문자열 인자로 고정한 뒤 성공했다. 코드 컴파일 실패로 분류하지 않는다.

### 판정

- `HUD-01` Done
- `HUD-02` Ready
- 상세 구현: [`DRONE_TELEMETRY_IMPLEMENTATION.md`](DRONE_TELEMETRY_IMPLEMENTATION.md)
- Unreal 로컬 Commit: `08e876a` (`feat: add drone telemetry snapshot component`)
- 원격 Push: 수행하지 않음

## 2026-08-23 — HUD-02 구현·검증 완료

### 실제 변경

- `Source/Drone/UI/DroneFlightHUDWidget.*`에 C++ native UMG Flight HUD를 추가했다.
- `Source/Drone/Prototype/DronePrototypePlayerController.*`가 로컬 Player 화면에 HUD 하나를 만들고 PlayerController 수명 동안 재사용한다.
- Prototype GameMode가 전용 PlayerController를 사용하도록 연결했다.
- Widget은 현재 Possess Pawn의 `UDroneTelemetryComponent`를 찾아 `OnTelemetryUpdated`를 `AddUniqueDynamic`으로 구독하고, 연결 직후 최신 Snapshot을 한 번 적용한다.
- Pawn 전환 시 이전 Component Event를 해제하고 새 Source로 교체한다. UnPossess, Widget 종료와 Controller 종료에서도 해제를 멱등적으로 수행한다.
- Tick, UMG Property Binding, 매 프레임 Pawn 검색과 Widget 내부 단위 재계산은 사용하지 않는다.
- 현재 Prototype 표시는 `SPD %.1f km/h`, `ALT %.1f m`, `V/S %+.1f m/s`, `HDG %03d°` 형식이다. 배치·폰트·색상·Animation은 최종 디자인 확정이 아니라 교체 가능한 초기값이다.
- 현재 PC의 실제 저장소 경로는 `C:\URproject\drone`이며, 뒤처진 `C:\project\Drone` 복제본은 수정하지 않았다.

### 자동화와 수명주기 검증

- `Drone.UI.FlightHUDTelemetryBinding`이 동일 Source 중복 연결 방지, 이전 Source 해제, 새 Source 연결, 네 Text 포맷과 Clear를 확인한다.
- 기존 `PIEInputLifecycle`을 확장해 새 PIE 3회마다 Prototype PlayerController와 HUD가 정확히 하나인지, Viewport와 현재 Telemetry Source가 연결됐는지 확인한다.
- 각 PIE에서 `UnPossess → HUD Collapsed·Event 해제 → 같은 Widget 재사용 Re-Possess·Event 재연결`을 실행하고, 종료 뒤 Viewport·Telemetry·Possession Delegate 잔존이 없는지 확인한다.
- Keyboard·Mouse·Gamepad, 복합·반대 입력과 입력 세기 회귀도 같은 테스트에서 계속 통과했다.

### 최종 검증 결과

- `DroneEditor Win64 Development` 빌드 성공
- 최종 `Drone.` Automation: 6 succeeded, 0 warnings, 0 failed
- `CompileAllBlueprints`: 0 errors, 0 warnings, 0 blueprints failed to load
- 새 `.uasset`/`.umap`을 만들지 않아 `/Game/Drone`의 Legacy Variant 신규 의존성 0
- Standalone 초기 화면: `SPD 0.0 km/h`, `ALT 1.5 m`, `V/S +0.0 m/s`
- Standalone 이동: `SPD 43.2 km/h`
- Standalone 상승: `ALT 2.7 m`, `V/S +10.0 m/s`
- Standalone 하강: `V/S -7.2 m/s`
- Standalone Yaw: Heading `002° → 025°/045°`
- 단일 자동 입력을 10Hz 화면에 확실히 포착하기 위해 실행 중에만 Movement 가속·감속을 임시 조정했으며 프로젝트 기본값과 소스는 변경하지 않았다.

### 발견·수정한 문제

- 첫 테스트 빌드에서 Dynamic Multicast 검사 API 선택과 C++ 멤버 이름 가림 오류를 발견해 `Contains` 검사와 명확한 변수명으로 수정했다.
- `AddToPlayerScreen` 실패가 조용히 넘어가지 않도록 반환값 검사와 오류 로그를 추가했다.
- 기본 UMG 글자 크기가 작은 문제를 초기 Prototype 읽기 크기로 조정했다. 이는 최종 HUD 디자인 확정이 아니다.

### 판정과 Git

- `HUD-02` Done
- `TUT-01` Ready
- Unreal Commit: `410c940` (`feat: add event-driven drone flight HUD`)
- `codex/hud-02-flight-hud`와 `origin/main`에 Push 완료, 로컬 `main=origin/main=410c940`

## 2026-08-23 — HUD-02 WBP/BP 연결과 학습 주석 보강

### 실제 변경

- native `UDroneFlightHUDWidget` 자식인 `WBP_DroneFlightHUD`를 생성해 Designer에서 패널 배치·색·폰트를 편집할 수 있게 했다.
- `BP_DronePrototypePlayerController`를 만들고 `FlightHUDWidgetClass`에 `WBP_DroneFlightHUD`를 지정했다.
- `BP_DronePrototypeGameMode`의 PlayerController Class를 새 BP Controller로 연결했다.
- WBP Designer에는 C++ `BindWidget` 계약과 정확히 같은 이름의 TextBlock 4개를 둔다.

```text
SpeedValueText
AltitudeValueText
VerticalSpeedValueText
HeadingValueText
```

- C++는 Telemetry 계산, Widget 생성, Possession 동기화, Delegate 해제와 표시 문자열 포맷을 계속 담당한다. WBP는 위치·크기·색·폰트 같은 표시 외형만 담당하며 Event Graph Tick과 Property Binding은 사용하지 않는다.
- Designer Tree가 없는 native HUD Class를 직접 실행할 때의 C++ 기본 레이아웃은 유지했다. 정상 컴파일된 WBP는 필수 TextBlock 4개를 사용하며 런타임 누락 경로는 방어 코드다.
- Pawn, GameMode, PlayerController와 HUD 기반 Class를 Blueprintable로 명시하고 Blueprint에서 확인할 Getter를 정리했다.
- 입력·이동·Telemetry 단위·Widget/Controller 수명주기·C++↔WBP 이름 계약·테스트 목적을 설명하는 한국어 주석을 보강했다. 이 주석 작업은 최종 비행 물리·감도·게임 규칙을 새로 확정한 것이 아니다.

### 발견·수정한 문제

- 첫 Standalone 화면에서 WBP TextBlock의 FontObject가 비어 있어 글자가 대체 글리프로 깨졌다.
- Engine `Roboto` Font를 WBP Asset에 직렬화해 저장했고, 필수 TextBlock과 Header Font 유효성을 자동화에서 검사하도록 했다.
- “BP Asset이 사라지면 native로 자동 복구”, “항상 10Hz”, “Heading 000°는 진북”처럼 구현보다 강하게 읽히는 주석을 실제 동작에 맞게 교정했다.

### 최종 검증

- `DroneEditor Win64 Development` 빌드 성공
- `Drone.` Automation: 7 succeeded, 0 warnings, 0 failed
- 새 `Drone.UI.FlightHUDBlueprintAsset`이 WBP 부모, 필수 TextBlock 4개·Font, BP Controller→WBP, BP GameMode→BP Controller를 확인
- `PIEInputLifecycle` 새 PIE 3회에서 실제 BP Controller와 WBP Class 사용, native fallback 미사용, Widget 재사용·Delegate 정리 확인
- `CompileAllBlueprints`: 0 errors, 0 warnings, 0 blueprints failed to load
- Standalone에서 실제 WBP의 `FLIGHT DATA`, `SPD`, `ALT`, `V/S`, `HDG` 글자가 깨짐 없이 표시됨
- WBP·BP Controller 신규 Asset과 갱신 BP GameMode 모두 Git LFS 적용 확인

### 판정과 Git

- `HUD-02` Blueprint presentation follow-up 완료
- 최종 아트·Animation, 배터리·신호·Jamming 표시는 아직 미정/미구현
- `TUT-01` Ready
- Unreal Commit: `9f91bb6` (`feat: add Blueprint-backed flight HUD`)
- `codex/hud-blueprint-ready-comments`와 `origin/main`에 Push 완료, 로컬 `main=origin/main=9f91bb6`

## 2026-08-23 — TUT-01 Training Map과 비충돌 Spline 착수

### 확정 범위

- 별도 `/Game/Drone/Tutorial/Maps/Lvl_DroneTraining` Map을 만든다.
- `ADroneTrainingCourse`가 편집 가능한 `USplineComponent`와 Standalone에서도 보이는 표시용 구성요소를 소유한다.
- 표시용 Actor·Spline·Mesh의 Collision, Overlap, Physics, Navigation 영향을 모두 끈다.
- 기존 `BP_DronePrototypeGameMode`를 재사용해 Prototype Pawn/Input/HUD 기준선을 유지한다.
- Gate Trigger, 순서·방향 판정, Lap/Segment 기록은 다음 `TUT-02` 이후 범위로 남긴다.

### 검증 예정

- native Course 기본값과 Pawn 크기 Sweep 비간섭 자동화
- 실제 BP Course와 Training Map 계약 자동화
- Training Map PIE에서 BP Pawn·Controller·WBP와 표시선 생성 확인
- Editor Build, 전체 Blueprint Compile, 전체 `Drone.` 회귀, Standalone 시각·비행 확인

### 현재 판정

- `TUT-01` Doing
- Unreal 작업 Branch: `codex/tutorial-training-course`
- Unreal Commit: 아직 미커밋

## 2026-08-23 — TUT-01 Training Course 구현·검증 완료

### 실제 변경

- `ADroneTrainingCourse`에 편집 가능한 `USplineComponent`와 런타임 표시용 `USplineMeshComponent` 구성을 구현했다.
- 실제 `BP_DroneTrainingCourse`와 별도 `Lvl_DroneTraining` Map을 만들고 기존 `BP_DronePrototypeGameMode`를 재사용했다.
- `M_DroneTrainingGuide`를 Opaque·Unlit·Emissive·Spline Mesh 용도로 만들고 Standalone에서 식별 가능한 밝은 Cyan 표시선을 구성했다.
- Course Actor와 Spline 표시 구성요소의 Collision, Overlap, Physics, Navigation 영향을 모두 껐다.
- native Course 기본 계약, 실제 BP/Map Asset 계약, Training Map PIE 수명주기와 비간섭을 검사하는 Tutorial 자동화 테스트 3개를 추가했다.
- 학습할 때 구현 의도와 C++·Blueprint 역할을 따라갈 수 있도록 Course와 테스트 코드에 한국어 주석을 추가했다.

### 최종 검증 결과

- `DroneEditor Win64 Development` 빌드 성공
- `Drone.Tutorial` Automation: 3 succeeded, 0 warnings, 0 failed
- 전체 `Drone.` Automation: 10 succeeded, 0 warnings, 0 failed
- `CompileAllBlueprints`: 0 errors, 0 warnings, 0 blueprints failed to load
- Standalone에서 실제 BP Pawn·Controller·WBP HUD와 밝은 Cyan Course Spline 표시 확인
- Spline Mesh Material Usage 경고 없음
- 실제 Pawn Sweep이 표시선을 통과하고 목표 위치에 도달해 Blocking 없음 확인
- Course 소유 표시 구성요소의 Collision·Overlap·Physics·Navigation 관련 Flag가 모두 꺼져 있음 확인
- Training Map에 저장된 Recast Actor 확인

### 범위 정지선

- TUT-01은 Training Map, 편집 가능한 Course Spline과 비간섭 표시선까지만 완료했다.
- Gate, Trigger, 순서, 방향, Lap, Timing은 구현하지 않았으며 `TUT-02` 이후 범위다.
- Android는 사용자 결정에 따라 작업 범위에서 제외한다.
- Map과 다음 카드 담당자는 현재 미정이다.

### 판정과 Git

- `TUT-01` Done
- `TUT-02` Todo
- Unreal Commit: `5a9a2faed4591a574988b649278cb0f166e31267` (`feat: add tutorial training course`)
- `codex/tutorial-training-course`와 `origin/main`에 Push 완료, 로컬 `main=origin/main=5a9a2faed4591a574988b649278cb0f166e31267`
