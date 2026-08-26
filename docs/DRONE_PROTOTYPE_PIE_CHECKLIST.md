# Drone Prototype PFN-06 PIE 검증 기록

기준일: 2026-08-24 (Asia/Seoul)

이 문서는 PFN-06의 체크 항목과 실행별 결과를 기록하는 **단일 기준 문서**다. `STATUS.md`, `WORKBOARD.md`, 구현 문서는 판정 요약과 이 문서 링크만 유지하며 체크리스트를 복제하지 않는다.

## 현재 판정

```text
PFN-01~05  Done
PFN-06     Done, 자동화 3/3 Pass · Standalone 수동 Pass
HUD-01     Done
HUD-02     Done, WBP/BP 실제 연결 · 전체 자동화 7/7
TUT-01     Done, Training Map · 비충돌 Cyan Spline
TUT-02     Done, Gate · 명시적 순서 · 정방향 판정
TUT-03     Done, Segment/Lap 시간 · 실제 이동 거리 · 평균 속도 원본 기록
TUT-04B    Implemented, 자동 검증 Pass · 실제 두 Lap 확인 대기
```

현재 main 기준은 `55b3ffe`이며 전체 `Drone.` 자동화 16/16과 Blueprint 오류 0을 통과했다. TUT-04B 결과 HUD가 추가됐으므로 두 번 완주해 첫 기준과 이전 평균·Best·Delta 표시를 확인한다. 현재 구조와 사용자 수동 확인 절차는 [`DRONE_CODE_STRUCTURE_AND_USER_TASKS.md`](DRONE_CODE_STRUCTURE_AND_USER_TASKS.md)를 따른다.

2026-08-19 사전 PIE 두 번에서 Prototype 입력 계열이 실제로 반응하는 것은 확인했다. 그러나 어느 실행도 한 번의 새 PIE 안에서 전체 체크리스트를 끝내지 못했으므로 Pass로 계산하지 않는다. 두 실행은 이미 종료된 역사적 부분 확인이며 현재 열린 PIE가 있다는 뜻이 아니다.

## 실제로 확인한 내용

### 첫 번째 PIE

- `BP_DronePrototypePawn_C_0` 한 대가 `PlayerController_0`에 Possess됨
- `IMC_DronePrototype` 한 개가 Priority 1로 표시됨
- `W`: Move가 Triggered되고 Actor 위치가 전진 방향으로 변함
- `A/D`: Move가 서로 반대 좌우 방향으로 변함
- `Space Bar/Left Ctrl`: Altitude가 각각 `+1/-1`로 Triggered되고 Z가 반대 방향으로 변함
- `E/Q`: 기체 Yaw가 서로 반대 방향으로 변함
- Mouse Look: Camera 시점이 바뀌지만 Actor Yaw 값은 그대로 유지됨
- Prototype Input Action/IMC 누락·중복 소유·등록 실패 진단 없음

미확인:

- `S`의 실제 반대 방향
- 반대 키 동시 입력
- 수평과 고도 복합 입력
- 같은 실행에서 Callback 이중 전달 여부
- PIE 재시작 사이 입력 세기 비교

### 두 번째 PIE

- BP Prototype Pawn Spawn/Possess 확인
- `IMC_DronePrototype` 한 개 확인
- `W` Move 반응 확인
- 사용자가 다른 앱을 직접 조작하는 것을 감지해 GUI 입력을 즉시 중단
- 당시 감사 도중 입력을 중단했고 이후 종료함. 전체 조건을 끝내지 않았으므로 Pass 또는 Fail로 산정하지 않음

## 로그 근거

2026-08-19 당시 경로 `C:\project\Drone\Saved\Logs\Drone.log`에서 확인한 역사적 세션 기준:

- `Lvl_DronePrototype` PIE 시작 2회
- `BP_DronePrototypeGameMode_C` 로드 2회
- BP Prototype Pawn Possess 2회
- 정상 PIE 종료 로그 1회
- Prototype 관련 금지 진단 문자열 0회

엔진 자체 오류 출력을 시험하는 `UE::UnifiedErrorTest`의 시작 로그와 렌더 설정 경고는 Prototype 기능 오류와 분리한다. 따라서 전체 로그가 warning/error 0이라고 표현하지 않는다.

## 정식 3회 공통 체크리스트

2026-08-21 PFN-06 검증 당시와 현재 D 드라이브 작업 PC의 프로젝트는 `D:\JGY\project\drone\Drone.uproject`다. `C:\URproject\drone`은 2026-08-24 다른 PC에서 확인한 경로다. 확정된 고정 추적 Camera와 Gamepad 계약을 반영한 `Drone.Prototype.PIEInputLifecycle`가 당시 Automation Report에서 새 PIE 3회를 모두 통과했다. 각 실행은 아래 항목을 전부 만족해야 한 번의 Pass다.

- [x] `Lvl_DronePrototype`에서 새 PIE 시작
- [x] BP Prototype Pawn 정확히 한 대 Spawn
- [x] `PlayerController_0`가 해당 Pawn Possess
- [x] `IMC_DronePrototype` 정확히 한 개, Priority 1, 15개 Mapping
- [x] `W` Forward, `S` Backward
- [x] `A` Left, `D` Right
- [x] `Space Bar` Up, `Left Ctrl` Down
- [x] `E` Right Yaw, `Q` Left Yaw
- [x] Mouse X가 Drone Actor Yaw를 바꾸고 추적 Camera가 함께 회전
- [x] Mouse Y가 CameraBoom Pitch만 바꾸고 Actor/Controller 회전은 변경하지 않음
- [x] Gamepad Left Stick 전후좌우, `RT/LT` 상승·하강
- [x] Gamepad Right Stick X Drone Yaw, Y Camera Pitch
- [x] `W+Space`, `D+E` 같은 복합 입력이 한 번씩 반응
- [x] `W+S`, `A+D` 반대 입력에서 비정상 가속이나 이중 전달 없음
- [x] 같은 입력 시간 기준으로 이전 PIE보다 입력 세기가 갑자기 두 배가 되지 않음
- [x] Input Action/IMC 누락·등록 실패·다른 경로 소유 진단 없음
- [x] PIE 정상 종료

세 번의 위치 절대값을 같게 만드는 것이 목적은 아니다. 각 새 PIE의 시작 위치와 같은 입력 시간 기준으로 반응이 갑자기 두 배가 되지 않는지 비교한다.

자동화 3회가 모두 통과한 뒤 `Lvl_DronePrototype`을 한 번 화면으로 확인한다. BP Prototype Pawn 한 대, Drone 뒤에 고정된 추적 Camera, Mouse X Drone Yaw, Mouse Y Camera Pitch, 기체 이동 방향과 정상 종료를 직접 확인한다. 실제 Gamepad가 연결돼 있으면 동일 회차에서 Stick과 Trigger 체감도 기록한다. 자동화 3/3과 이 수동 확인을 모두 완료한 경우에만 PFN-06을 Done으로 옮긴다.

## 반복 결과표

| 실행 | Pawn/IMC | Keyboard·Mouse·Gamepad | 복합·반대 입력 | 중복 없음 | 종료 | 판정 |
|---|---|---|---|---|---|---|
| 사전 부분 확인 1 | 확인 | `S` 제외 부분 확인 | 미확인 | 미확인 | 확인 | 미산정 |
| 사전 부분 확인 2 | 확인 | Move 일부 | 미확인 | 미확인 | 종료 | 미산정 |
| 정식 1 | Pawn 1 / IMC 1 | Pass | Pass | Pass | 정상 종료 | 자동화 Pass |
| 정식 2 | Pawn 1 / IMC 1 | Pass | Pass | Pass | 정상 종료 | 자동화 Pass |
| 정식 3 | Pawn 1 / IMC 1 | Pass | Pass | Pass | 정상 종료 | 자동화 Pass |

| 수동 화면 확인 | Pawn/고정 Camera | 이동·Mouse 방향 | Gamepad 체감 | 종료 | 판정 |
|---|---|---|---|---|---|
| 새 조작 자동화 3회 통과 후 1회 | Pawn 1·고정 Camera 정상 | Keyboard·Mouse Pass | 연결 여부 미보고 | 창 닫기 정상 종료 | 수동 Pass |

## 2026-08-23 HUD WBP/BP 최신 검증

PFN-06의 2026-08-21 입력 결과는 그대로 유지한다. `9f91bb6` WBP/BP 보강 뒤 같은 `Drone.Prototype.PIEInputLifecycle`의 새 PIE 3회에 다음 HUD 조건을 추가해 모두 통과했다.

- [x] 실제 Controller Class가 `BP_DronePrototypePlayerController_C`
- [x] 실제 HUD Class가 `WBP_DroneFlightHUD_C`
- [x] `IsUsingNativeFallbackLayout()`이 `false`
- [x] HUD 인스턴스가 로컬 Player 화면에 정확히 한 개
- [x] 현재 Possess Pawn의 Telemetry Component 연결
- [x] UnPossess 시 Telemetry Event 해제와 HUD 숨김
- [x] Re-Possess 시 같은 Widget 인스턴스 재사용과 Event 재연결
- [x] 각 PIE 종료 후 Possession Delegate·Telemetry Delegate·Viewport Widget 잔존 없음

전체 `Drone.` 자동화는 `Drone.UI.FlightHUDBlueprintAsset`을 포함해 7 succeeded, 0 warnings, 0 failed다. 전체 Blueprint Compile도 0 errors, 0 warnings, 0 failed to load다. 별도 Development Standalone에서는 실제 WBP의 `FLIGHT DATA`, `SPD`, `ALT`, `V/S`, `HDG`가 깨짐 없이 표시되는 것을 화면으로 확인하고 정상 종료했다.

## 2026-08-24 TUT-02 최신 회귀 기준선

PFN-06의 입력 3/3과 HUD WBP/BP 7/7은 위의 역사적 단계 결과로 그대로 유지한다. `800a7ba` TUT-02 통합 뒤에는 실제 `BP_DroneTrainingGate` 4개, Course의 명시적 Gate 순서, 정방향 판정과 기존 Prototype 입력·HUD 회귀를 함께 검증했다.

- `DroneEditor Win64 Development` Build 성공
- `Drone.Tutorial` Automation 4/4
- 전체 `Drone.` Automation 11/11
- Blueprint Compile Errors/Warnings/Load Failures 0/0/0
- Standalone에서 Gate Ring과 상태 시각 표시 확인
- 당시 Done 범위: Gate·순서·정방향
- 당시 다음 카드: TUT-03 Segment/Lap 기록

## 완료 판정

사용자는 수정된 조작이 정상이라고 확인했다. `Esc`로 종료되지는 않았지만 창 닫기 뒤 로그가 `Win RequestExit → Game engine shut down → Exiting`으로 끝났고 Fatal·Assertion은 없었다. 실제 Gamepad 체감은 장치 연결 여부가 보고되지 않아 미확인으로 남기되 필수 자동화 입력 Probe가 통과했으므로 PFN-06 완료를 차단하지 않는다.
