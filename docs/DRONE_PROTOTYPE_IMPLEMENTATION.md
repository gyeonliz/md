# Drone Prototype Pawn 구현 및 검증 기록

기준일: 2026-08-19 (Asia/Seoul)

## 1. 현재 결과

`C:\project\Drone`에 기존 Third Person 경로와 분리된 최소 Drone Prototype을 추가했다.

- `ADronePrototypePawn` C++ 클래스가 컴파일된다.
- `ADronePrototypeGameMode`가 native fallback으로 해당 Pawn을 Spawn한다.
- 자동화 테스트에서 컴포넌트 기본값과 Spawn/Possess를 검증했다.
- Prototype Input Action 4개와 전용 IMC를 생성했다.
- BP Pawn에 입력 자산과 Engine Cube Placeholder를 연결했다.
- BP GameMode와 별도 `Lvl_DronePrototype` Greybox Map을 연결했다.
- 새 자산 재로드 검증과 Map Check를 통과했다.
- GUI PIE 1회차에서 IMC 한 개와 Move·Altitude·Yaw·Look의 실제 동작을 확인했다.
- 기존 기본 맵과 전역 기본 GameMode는 변경하지 않았다.
- Android File Server는 사용하지 않는다는 사용자 결정을 반영해 비활성화했다.

현재 PFN-01~05는 완료했고 PFN-06은 **0/3 Pass**다. GUI에서 핵심 동작은 부분 확인했지만 한 실행 안에서 전체 체크리스트를 끝내지 못했다. 다음은 아직 완료되지 않았다.

- 새 PIE 3회에서 Pawn 한 대 Spawn/Possess, IMC 한 개와 모든 매핑을 확인
- PIE 재시작 뒤 입력 세기와 Callback이 중복되지 않는지 확인
- 최종 입력 키·감도·Mouse Y 반전 기본값 결정
- 최종 Drone Mesh 선택·연결
- 착륙·충돌 실패 처리

첫 번째 PIE는 `S`와 복합·중복 조건을 끝내지 못했고, 두 번째 PIE는 Pawn Spawn/Possess, IMC 한 개와 Move까지 확인한 뒤 사용자가 다른 앱을 직접 조작하는 것을 감지해 입력 충돌 방지를 위해 중단했다. 두 실행 모두 Pass 횟수에 포함하지 않는다. 따라서 현재 상태를 PFN-06 완료나 Flight MVP 완료라고 표현하지 않는다.

## 2. 변경된 실제 프로젝트 파일

```text
C:\project\Drone\Config\DefaultEngine.ini
C:\project\Drone\Source\Drone\Prototype\DronePrototypePawn.h
C:\project\Drone\Source\Drone\Prototype\DronePrototypePawn.cpp
C:\project\Drone\Source\Drone\Prototype\DronePrototypeGameMode.h
C:\project\Drone\Source\Drone\Prototype\DronePrototypeGameMode.cpp
C:\project\Drone\Source\Drone\Prototype\Tests\DronePrototypeDefaultsTest.cpp
C:\project\Drone\Source\Drone\Prototype\Tests\DronePrototypeSpawnPossessTest.cpp
C:\project\Drone\Content\Drone\Prototype\Input\Actions\IA_DronePrototype_Move.uasset
C:\project\Drone\Content\Drone\Prototype\Input\Actions\IA_DronePrototype_Altitude.uasset
C:\project\Drone\Content\Drone\Prototype\Input\Actions\IA_DronePrototype_Yaw.uasset
C:\project\Drone\Content\Drone\Prototype\Input\Actions\IA_DronePrototype_Look.uasset
C:\project\Drone\Content\Drone\Prototype\Input\IMC_DronePrototype.uasset
C:\project\Drone\Content\Drone\Prototype\Blueprints\BP_DronePrototypePawn.uasset
C:\project\Drone\Content\Drone\Prototype\Blueprints\BP_DronePrototypeGameMode.uasset
C:\project\Drone\Content\Drone\Prototype\Maps\Lvl_DronePrototype.umap
```

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

격리 테스트에서 `ADronePrototypePawn`을 기본 Pawn으로 Spawn하는 native fallback이다.

주의: native Pawn의 Input Asset과 Mesh 기본값은 계속 `null`이다. 현재 실제 Prototype Map에서는 BP 자식에 자산을 배정하고 BP GameMode의 Default Pawn도 그 BP Pawn으로 바꿨다. native GameMode만 직접 쓰면 BP에 지정한 값이 적용되지 않는다는 경계는 그대로 유지한다.

### 자동화 테스트

- `Drone.Prototype.PawnDefaults`: Root, Collision, Camera, Movement, GameMode 기본값 검증
- `Drone.Prototype.SpawnPossess`: 임시 Game World에서 GameMode 생성, Pawn Spawn, PlayerController Possess 검증

두 번째 테스트에는 실제 `ULocalPlayer`가 없으므로 IMC 등록과 실제 입력 전달까지 검증하는 테스트는 아니다.

## 5. 헤더에 추가된 것

`DronePrototypePawn.h`에는 다음 선언이 있다.

- 다섯 개의 컴포넌트 `TObjectPtr`
- Prototype IMC와 네 Input Action용 `TObjectPtr`
- Mapping Priority와 임시 Yaw Rate
- `PawnClientRestart`, `SetupPlayerInputComponent`, `UnPossessed`, `EndPlay`
- 이동·고도·Yaw·Look 처리 함수
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
- Look: Controller Yaw/Pitch 입력

Input Action이 배정되지 않았으면 크래시 대신 진단 로그를 남긴다.

## 7. 현재 Blueprint와 Input 설정

다음 자산은 생성과 저장 뒤 별도 Editor 프로세스에서 다시 로드해 검증했다.

```text
/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_Move       Axis2D
/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_Altitude   Axis1D
/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_Yaw        Axis1D
/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_Look       Axis2D
/Game/Drone/Prototype/Input/IMC_DronePrototype
/Game/Drone/Prototype/Blueprints/BP_DronePrototypePawn
/Game/Drone/Prototype/Blueprints/BP_DronePrototypeGameMode
/Game/Drone/Prototype/Maps/Lvl_DronePrototype
```

현재 IMC에는 9개 Mapping이 있다.

- Move: `W/S/A/D`
- Altitude: `Space Bar/Left Ctrl`
- Yaw: `E/Q`
- Look: `Mouse XY 2D-Axis`

Modifier와 기대 부호는 [`DRONE_PROTOTYPE_INPUT_CONTRACT.md`](DRONE_PROTOTYPE_INPUT_CONTRACT.md)에 기록했다. 이 키는 PFN 시험 전용이며 최종 조작 승인안이 아니다.

`BP_DronePrototypePawn`은 `ADronePrototypePawn` 자식이다. Class Defaults에 IMC와 네 Action을 연결했고, Visual Mesh에는 외부 구매 소스가 아닌 Engine 기본 Cube를 Placeholder로 연결했다. Event Graph에서 IMC를 추가하거나 Action을 다시 바인딩하지 않는다.

`BP_DronePrototypeGameMode`는 `ADronePrototypeGameMode` 자식이며 Default Pawn은 BP Prototype Pawn이다. PlayerController Class는 기존 Third Person BP Controller가 아니라 기본 `APlayerController`를 유지한다. Third Person Controller가 추가하는 기존 IMC와 키가 겹쳐 중복되는 것을 막기 위해서다.

`Lvl_DronePrototype`은 기존 World Partition Template Map을 복제하지 않고 새로 만든 작은 비-World-Partition 시험장이다. Map-level GameMode Override, PlayerStart 한 개, 배치 Pawn 0개, 지면·이륙 Pad·벽·높이 표식·목표·귀환·Patrol·Turret 위치 표시를 포함한다. 위치와 크기는 모두 Greybox 임시값이다.

## 8. Editor에서 재검증하는 방법

1. UE 5.8.1로 `Drone.uproject`를 연다.
2. `Lvl_DronePrototype`을 연다.
3. World Settings의 GameMode Override가 `BP_DronePrototypeGameMode`인지 확인한다.
4. Map에 `PlayerStart`가 한 개이고 Pawn이 직접 배치되지 않았는지 확인한다.
5. PIE를 시작하고 BP Prototype Pawn 한 대가 Spawn되어 PlayerController에 Possess되는지 확인한다.
6. Enhanced Input Debug에서 `IMC_DronePrototype`이 Priority 1로 한 번만 등록되는지 확인한다.
7. `W/S/A/D`, `Space/Left Ctrl`, `Q/E`, Mouse를 각각 시험해 Move, Altitude, Yaw, Look의 방향을 확인한다.
8. Mouse Look 뒤 Actor Yaw는 그대로이고 Camera Control Rotation만 바뀌는지 확인한다.
9. Output Log에서 Input Asset 누락, IMC 등록 실패, 다른 경로 소유 진단이 없는지 확인한다.
10. PIE를 종료하고 새로 두 번 더 실행해 Pawn·IMC·Callback·입력 세기가 중복되지 않는지 확인한다.

두 번의 실행에서 핵심 동작을 부분 확인했지만 전체 체크리스트를 끝낸 실행은 없다. 사용자 직접 조작 보호를 위해 GUI 조작을 중단했으며 새 PIE 3회 전체 반복이 필요하다.

## 9. 정상 결과

Blueprint와 Input 연결까지 완료했을 때의 정상 기준은 다음과 같다.

- Prototype 맵에서 Pawn이 한 대만 Spawn된다.
- PlayerController가 해당 Pawn을 Possess한다.
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
- `BP_DronePrototypePawn`의 IMC와 네 Action이 모두 연결됐는지
- Project Settings의 Default Input Component Class가 Enhanced Input인지
- Output Log의 누락 자산 또는 Mapping 등록 메시지
- IMC에 실제 키 Mapping이 추가됐는지

### 이동이 안 되거나 충돌이 이상함

- `UFloatingPawnMovement.UpdatedComponent`가 Sphere Root인지
- Sphere Collision Profile이 `Pawn`인지
- Visual Mesh Collision과 Simulate Physics가 꺼져 있는지
- Root를 다른 컴포넌트로 바꾼 Blueprint Override가 없는지

### Camera가 두 번 회전함

- SpringArm의 `Use Pawn Control Rotation`은 켜져 있는지
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

설치된 MSVC `14.51.36252`가 UE가 표시한 선호 버전 `14.50.35717`보다 새 버전이라는 경고가 있었지만 이번 빌드는 성공했다.

### 자동화 테스트

```text
Drone.Prototype.PawnDefaults  Success, 0 warnings, 0 errors
Drone.Prototype.SpawnPossess  Success, 0 warnings, 0 errors
Total                        2 succeeded, 0 failed
Process exit code            0
```

결과 파일은 로컬 임시 검증 폴더의 `AutomationReport/index.json`에 생성했으며 Git 추적 대상이 아니다.

### Prototype 자산 생성과 재로드 검증

Editor Python은 프로젝트 Plugin 설정을 바꾸지 않고 실행 시점에만 `PythonScriptPlugin`을 활성화했다. 생성기는 8개 대상 경로를 먼저 검사하고 기존 자산이 하나라도 있으면 덮어쓰지 않고 중단한다.

확인 결과:

- Input Action 4개와 IMC 한 개 생성
- 정확히 9개 Mapping과 Modifier 순서·부호 검증
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

첫 번째 새 PIE에서 다음을 부분 확인했다.

- BP Prototype Pawn 한 대 Spawn/Possess
- `IMC_DronePrototype` 한 개, Priority 1
- W와 A/D가 기대 수평 방향으로 동작. `S`는 미확인
- Space/Left Ctrl이 고도 `+1/-1` 방향으로 동작
- E/Q가 기체 Yaw의 반대 방향으로 동작
- Mouse가 Actor Yaw를 바꾸지 않고 Camera Look만 변경
- Prototype 관련 금지 진단 문자열 0회

두 번째 PIE도 Pawn Spawn/Possess와 IMC 한 개, Move까지 확인했다. 이후 사용자가 다른 앱을 직접 조작하는 것을 감지해 입력을 빼앗지 않도록 GUI 조작을 중단했다. 어느 실행도 완전한 Pass가 아니며 PFN-06은 0/3 Pass다.

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
- Prototype 8개 자산 모두 Git LFS 속성 적용
- 기존 전역 Map/GameMode는 Third Person 설정 그대로 유지
- Python Plugin을 `.uproject`에 영구 추가하지 않음
- 자산 8개의 디스크 수정 시각은 생성 시점 그대로이며 이후 검증·PIE에서 저장 변경 흔적 없음
- 현재 두 번째 PIE를 시작한 Unreal Editor는 열려 있으므로 유휴 상태라고 기록하지 않음

## 12. 다음 완료 게이트

구매 소스 확보 전 전체 실행 순서와 Greybox 기준은 [`DRONE_PREASSET_FUNCTION_PLAN.md`](DRONE_PREASSET_FUNCTION_PLAN.md)를 따른다.

다음 완료 게이트는 PFN-06의 새 PIE 3회 전체 반복이다.

```text
현재 두 번째 PIE를 안전하게 종료
→ 새 PIE 3회에서 각각 Pawn 1대·IMC 1개·모든 매핑 확인
→ 3회 Pass와 중복 없음 기록
→ PFN-06 Done
→ PFN-07~14 Flight MVP 활성화
```

이 게이트를 통과하기 전에는 Flight MVP 카드를 완료로 이동하지 않는다. 통과한 뒤 Take Off, Landing, Crash/실패 처리를 각각 별도 기능 단위로 진행한다.
