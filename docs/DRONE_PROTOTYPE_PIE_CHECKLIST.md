# Drone Prototype PFN-06 PIE 검증 기록

기준일: 2026-08-19 (Asia/Seoul)

## 현재 판정

```text
PFN-01~05  Done
PFN-06     Doing, 0/3 Pass
PFN-P2     잠금
```

두 번의 PIE에서 Prototype 입력 계열이 실제로 반응하는 것은 확인했다. 그러나 어느 실행도 한 번의 새 PIE 안에서 전체 체크리스트를 끝내지 못했으므로 Pass로 계산하지 않는다.

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
- 감사 시점에는 두 번째 PIE가 열린 상태였으므로 Pass 또는 Fail로 판정하지 않음

## 로그 근거

`C:\project\Drone\Saved\Logs\Drone.log`에서 확인한 현재 세션 기준:

- `Lvl_DronePrototype` PIE 시작 2회
- `BP_DronePrototypeGameMode_C` 로드 2회
- BP Prototype Pawn Possess 2회
- 정상 PIE 종료 로그 1회
- Prototype 관련 금지 진단 문자열 0회

엔진 자체 오류 출력을 시험하는 `UE::UnifiedErrorTest`의 시작 로그와 렌더 설정 경고는 Prototype 기능 오류와 분리한다. 따라서 전체 로그가 warning/error 0이라고 표현하지 않는다.

## 다음 3회 공통 체크리스트

각 실행은 아래 항목을 전부 만족해야 한 번의 Pass다.

- [ ] `Lvl_DronePrototype`에서 새 PIE 시작
- [ ] BP Prototype Pawn 정확히 한 대 Spawn
- [ ] `PlayerController_0`가 해당 Pawn Possess
- [ ] `IMC_DronePrototype` 정확히 한 개, Priority 1
- [ ] `W` Forward, `S` Backward
- [ ] `A` Left, `D` Right
- [ ] `Space Bar` Up, `Left Ctrl` Down
- [ ] `E` Right Yaw, `Q` Left Yaw
- [ ] Mouse X/Y가 Camera Look에 반영
- [ ] Mouse Look 중 Actor Yaw는 변하지 않음
- [ ] `W+Space`, `D+E` 같은 복합 입력이 한 번씩 반응
- [ ] `W+S`, `A+D` 반대 입력에서 비정상 가속이나 이중 전달 없음
- [ ] Input Action/IMC 누락·등록 실패·다른 경로 소유 진단 없음
- [ ] PIE 정상 종료

세 번의 위치 절대값을 같게 만드는 것이 목적은 아니다. 각 새 PIE의 시작 위치와 같은 입력 시간 기준으로 반응이 갑자기 두 배가 되지 않는지 비교한다.

## 반복 결과표

| 실행 | Pawn/IMC | 모든 키·Look | 복합·반대 입력 | 중복 없음 | 종료 | 판정 |
|---|---|---|---|---|---|---|
| 사전 부분 확인 1 | 확인 | `S` 제외 부분 확인 | 미확인 | 미확인 | 확인 | 미산정 |
| 사전 부분 확인 2 | 확인 | Move 일부 | 미확인 | 미확인 | 판정 전 | 미산정 |
| 정식 1 | 대기 | 대기 | 대기 | 대기 | 대기 | 대기 |
| 정식 2 | 대기 | 대기 | 대기 | 대기 | 대기 | 대기 |
| 정식 3 | 대기 | 대기 | 대기 | 대기 | 대기 | 대기 |

## 안전한 재개 조건

사용자가 다른 앱을 직접 조작 중일 때는 GUI 자동 입력을 보내지 않는다. Unreal Editor를 직접 사용할 수 있는 상태에서 현재 PIE를 먼저 정상 종료하고, 새 PIE 3회를 처음부터 수행한다. 이 검증이 끝나기 전에는 PFN-06을 Done으로 옮기거나 PFN-07 이후 Flight MVP 카드를 활성화하지 않는다.
