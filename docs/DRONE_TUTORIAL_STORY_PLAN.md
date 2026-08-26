# Drone Tutorial·Story 구현 계획

기준일: 2026-08-23 (Asia/Seoul)

## 1. 목표와 우선순위

현재 Drone Prototype을 다음 두 플레이 모드의 공통 기반으로 확장한다.

1. **Tutorial**: 표시용 비충돌 경로와 순서형 Ring Gate를 따라 비행하고, 속도·고도·Lap/구간 기록을 비교하는 훈련 모드
2. **Story**: Operator Character가 NPC와 상호작용하고 Mission 안내를 받은 뒤 Drone 조작으로 전환해 정찰·재밍·전투 방해 요소를 해결하는 모드

구현 순서는 아래와 같이 고정한다.

```text
카메라·Mouse·Gamepad 조작 기준선
→ Telemetry·공용 HUD 기반
→ Tutorial 코스·Gate·Timing Vertical Slice
→ Take Off·Landing·Crash Flight 상태
→ Operator ↔ Drone 전환
→ NPC 대화·Mission UI Story Shell
→ Enemy AI·MG·Jamming Mission
→ 통합 Greybox와 외부 Drone 에셋 적용
```

Tutorial을 먼저 완성해 조작감, 카메라, HUD, 비행 기록 계산을 검증한 뒤 Story에 재사용한다.

## 2. 확정 조작 계약

카메라는 Controller Rotation을 따라 자유 회전하지 않는다. Drone 뒤에서 함께 Yaw하는 SpringArm 추적 카메라를 사용하고 입력별 책임을 분리한다.

| 장치 | 입력 | 기능 |
|---|---|---|
| Keyboard | `W/S`, `A/D` | Actor-relative 전후·좌우 이동 |
| Keyboard | `Space/Left Ctrl` | World Up 기준 상승·하강 |
| Keyboard | `Q/E` | 세밀한 좌/우 Drone Yaw |
| Mouse | X | Drone Actor Yaw, 추적 카메라도 함께 회전 |
| Mouse | Y | SpringArm Camera Pitch만 조정 |
| Gamepad | Left Stick | 전후·좌우 이동 |
| Gamepad | `RT/LT` | 상승·하강 |
| Gamepad | Right Stick X | Drone Yaw |
| Gamepad | Right Stick Y | Camera Pitch |
| 공통 | `Tab` / Gamepad `Y` | Story의 Operator ↔ Drone 전환 후보 |
| 공통 | `F` / Gamepad `A` | NPC·오브젝트 상호작용 후보 |

현재 Camera Pitch 범위는 `-70°~20°`, Keyboard/Gamepad Yaw Rate는 `90°/s`, Mouse 감도는 `1.0°/input`의 시험값이다. Mouse Y 반전과 최종 감도는 수동 체감 검증 뒤 조정한다.

입력 소유권은 다음과 같이 고정한다.

- Drone 전용 IMC는 Drone Pawn이 Possess 수명주기에 맞춰 한 번만 등록·제거한다.
- Operator 전용 IMC는 Operator Pawn이 소유한다.
- 화면 전환, Pause, 공용 UI 입력만 프로젝트 소유 PlayerController의 Common IMC가 담당한다.
- 같은 IMC를 PlayerController, Pawn, Level Blueprint에서 중복 등록하지 않는다.

## 3. 공용 런타임 구조

### Control과 화면 전환

- Story 전용 프로젝트 소유 PlayerController가 Operator와 지정 Drone 참조를 관리한다.
- `Tab` 또는 Gamepad `Y` 입력 시 `SetViewTargetWithBlend(0.35s)`와 Possess 전환을 수행한다.
- Drone 모드 진입 시 Operator는 위치를 유지하고 이동 입력을 받지 않는다.
- Operator 복귀 시 Drone Movement 입력과 속도를 정리하고 현재 위치에서 Hover 상태를 유지한다.
- `Character`, `TransitionToDrone`, `Drone`, `TransitionToCharacter`, `Dialogue` 상태에서 중복 전환을 차단한다.
- HUD는 PlayerController 수명에 연결해 Pawn이 바뀌어도 다시 생성하지 않고 데이터 공급자만 교체한다.

### Telemetry

Drone에 공용 Telemetry Component를 두고 10Hz 이벤트로 UI에 Snapshot을 전달한다. HUD-01·02에서 현재 구현·표시하는 범위는 아래 네 비행 수치다.

- 속도: `Velocity.Size() × 0.036`, km/h
- 고도: 코스/미션 기준 지면 높이 대비 m
- 수직 속도: m/s
- Heading: 0~359°

Flight·Control·Mission 상태와 신호 세기·Jamming 단계는 후속 카드의 확장 후보이며 HUD-02가 구현한 기능으로 간주하지 않는다.

Widget에서 매 프레임 Pawn을 검색하거나 Property Binding으로 계산하지 않는다. C++ Telemetry가 Multicast Event를 보내고 native 또는 후속 Blueprint Widget은 표시만 담당한다.

## 4. Tutorial Vertical Slice

현재 구현 경계는 다음과 같다.

- `TUT-01` 완료: Training Map, 수정 가능한 Spline, Runtime 안내선과 비충돌·비탐색 안전 설정
- `TUT-02` 완료: Gate 목록, Gate Actor와 Trigger, 순서·정방향·중복 통과 판정과 시각 상태
- `TUT-03` 완료: Segment/Lap World Game Time, 실제 3차원 이동 거리와 평균 속도 원본 기록
- `TUT-04` 다음 활성 카드: 이전 성공 평균·Best 비교 규칙과 결과 UI

구매 에셋은 이 Vertical Slice의 선행 조건이 아니다. 현재는 Engine 기본 도형과 프로젝트 소유 Material로 기능을 검증하며, Android는 범위에서 제외한다.

### TUT-01 — 코스와 표시선 (완료)

- 별도 `/Game/Drone/Tutorial/Maps/Lvl_DroneTraining` Map을 만든다.
- `ADroneTrainingCourse`가 Editor에서 수정 가능한 `USplineComponent`를 소유한다.
- Runtime 표시선은 `USplineMeshComponent`로 만들고 프로젝트 소유 불투명·Unlit·Emissive `M_DroneTrainingGuide`를 사용한다.
- Course Actor, Spline과 생성된 표시선은 Collision·Overlap·Physics·Navigation 영향을 모두 끈다.
- 실제 `BP_DroneTrainingCourse`를 Map에 배치하고 기존 Prototype BP GameMode·Pawn·PlayerController·WBP를 재사용한다.

TUT-01에는 Gate 목록이나 통과 판정이 없다. 현재 Spline 점과 경로는 기능 검증용 Greybox 값이며 최종 코스 확정이 아니다.

### TUT-02 — 순서형 Ring Gate (완료)

- `ADroneTrainingCourse`에 명시적 순서의 Gate 목록과 비-Primitive Gate Sequence Component를 연결했다.
- `ADroneTrainingGate`는 비충돌 원형 Visual과 별도 Pawn Overlap Trigger를 분리한다.
- Gate는 `CourseId`, `GateIndex`, `SegmentDistance`를 가지며 Actor 로컬 `+X`를 유일한 정방향으로 사용한다. `SegmentDistance`는 배치/표시용 메타데이터이며 TUT-03 실제 이동 거리 계산에는 사용하지 않는다.
- 실제 `BP_DroneTrainingGate` 네 개를 Training Map에 배치하고 Course 배열 순서와 GateIndex를 일치시켰다.
- 현재 목표 Gate는 Current, 정상 통과한 Gate는 Completed, 이후 Gate는 Inactive로 표시한다.
- 현재 순서가 아닌 Gate, 역방향, 중복 통과와 잘못된 Actor는 진행 상태를 바꾸지 않는다.

### TUT-03 — Lap과 구간 원본 기록 (완료)

- Course가 별도 `UDroneTrainingLapRecorderComponent`를 소유하고 Gate Sequence의 정상 승인 Event만 구독한다.
- Gate 0 통과 시 Lap을 시작하고 이후 Gate마다 Segment를 확정하며 마지막 Gate 통과 시 완료한다. Gate 네 개면 Segment는 `0→1`, `1→2`, `2→3` 세 개다.
- Segment Time은 이전 정상 Gate 승인부터 현재 Gate 승인까지의 World Game Time으로 계산한다.
- 실제 이동 거리는 같은 Drone의 Telemetry 10Hz World 위치 표본 사이 3차원 거리를 합산하고 Gate 승인 위치를 끝점으로 추가한다.
- Segment/Lap 평균 속도는 해당 누적 거리 ÷ 시간이며 cm/s에서 km/h로 변환한다.
- 잘못된 순서·역방향·중복 Gate는 승인 Event가 없어 기록 경계를 만들지 않는다.
- Restart는 부분 시도만 폐기하고 성공 원본 History는 유지한다. Course 재구성은 비교 기준이 달라지므로 History도 비운다.
- Pawn 파괴, 구성 무효화와 같은 Frame 0초 순간이동은 성공 기록으로 남기지 않는다.
- 결과 Struct, Getter, `OnLapStarted`, `OnSegmentRecorded`, `OnLapCompleted`는 Blueprint에 노출한다.

완료 원본은 첫 Vertical Slice에서 현재 실행 동안만 유지한다. `USaveGame` 영속화, 비교, Best와 표시 문자열은 이 카드에 포함하지 않는다.

### TUT-04 — 이전 기록 비교와 결과 UI (미구현·다음 카드)

- 첫 성공 시도에는 `기준 기록 생성 중`을 표시한다.
- 두 번째 시도부터 현재 결과를 **현재 시도를 제외한 이전 성공 기록 평균**과 비교한다.
- Time Delta는 음수면 빠름, 양수면 느림으로 표시한다.
- Speed Delta는 양수면 빠름, 음수면 느림으로 표시한다.
- Best Lap과 Best Segment는 평균 기록과 별도로 보존한다.

표시 예시는 다음과 같다.

```text
구간 03
현재        4.82초
이전 평균   5.10초
차이       -0.28초 빠름

평균 속도   42.5 km/h
평균 대비   +2.3 km/h
```

### Tutorial UI

- 상시 Flight HUD: 속도, 고도, 수직 속도, Heading
- Course HUD: 다음 Gate, 현재 Lap Time, 현재 Segment Time
- Gate 결과 Toast: 구간 시간, 구간 평균 속도, 이전 평균 대비 차이
- Lap 결과: 총시간, 평균 속도, Best/평균 대비, 구간별 표
- 잘못된 Gate: `다음 Gate를 통과하세요` 안내만 표시하고 기록은 변경하지 않음
- Restart: 현재 시도를 폐기하고 Gate 0 상태로 초기화

기록은 현재 실행 동안만 유지한다. TUT-04 비교·표시 계산을 검증한 뒤에만 `USaveGame`으로 Course별 Attempt Count, 평균, Best 기록을 영속화한다.

## 5. Story Mode

### Operator와 NPC

- Legacy ThirdPerson/Variant를 상속하지 않는 `ACharacter` 기반 Operator를 `/Game/Drone` 전용으로 만든다.
- `IDroneInteractable` Interface로 NPC·콘솔·목표물을 동일한 상호작용 입력에 연결한다.
- NPC 대화는 Speaker, Text, Portrait 후보, 다음 Line, Mission Event를 가진 Data Asset으로 구성한다.
- 첫 버전은 선택지 없는 순차 대화이며 실제 분기 요구가 생길 때 Choice를 추가한다.
- Dialogue 중 Character/Drone 이동 입력과 전환 입력을 잠근다.

### Mission

- Mission Definition은 Data Asset, 실행 상태는 Map의 Mission Director가 소유한다.
- 공통 상태는 `Briefing`, `Deploy`, `Recon`, `Objective`, `Egress`, `Evaluation`, `Failed`로 시작한다.
- Mission UI는 현재 목표, 거리, 상호작용 Prompt, Drone/Operator 전환 가능 여부를 표시한다.
- Crash, 목표 획득, 귀환, NPC 대화 완료를 중복 없이 Mission Event로 연결한다.

### Jamming

Jamming은 무작위 입력 손실이 아닌 재현 가능한 단계형 게임 규칙으로 시작한다.

1. 약함: 신호 경고와 Signal Meter 변화
2. 중간: HUD Noise와 목표 정보 일부 손실
3. 강함: 조작 반응 저하 또는 통신 두절

`ADroneJammingVolume`의 범위와 정규화된 세기로 상태를 계산한다. Jammer 회피, 범위 이탈, 전원 차단 또는 파괴를 Mission 목표로 연결한다. 실제 전자전 장비를 1:1 재현하지 않는다.

## 6. 외부 Drone 에셋 적용

- 현재 D 드라이브 작업 PC의 제공 에셋 해제본·스테이징 보관 루트는 `D:\JGY\project\Unreal_260821`이며 Drone Git 저장소에 전체 복사하지 않는다. 다른 PC의 `C:\에셋` 재감사와 D 드라이브 ZIP 14개 감사는 PC별 기록으로 구분한다.
- Loose `.uasset`은 UE 5.8 스테이징 프로젝트에서 먼저 원래 `/Game/<PackRoot>` 경로로 로드한다. Explorer에서 바로 `/Game/Drone` 아래로 옮기지 않는다.
- 필요한 의존성만 고른 뒤 스테이징 Content Browser에서 `/Game/Drone/ThirdParty/<PackName>`으로 이동·재저장하고 Redirector를 정리한다.
- 실제 사용 Blueprint는 `/Game/Drone/Integrations/<PackName>` 아래에 만들고 프로젝트 기능 Pawn에 연결한다.
- C++ Collision Root, Movement, Camera/Sensor 기준점은 유지한다.
- 외부 Mesh, Rotor, Material, Animation, VFX만 Integration Blueprint가 연결한다.
- 외부 Pawn/GameMode/Input Mapping을 신규 게임플레이 부모로 사용하지 않는다.
- 적용 전에 Plugin, 부모 클래스, Collision, Pivot/Forward, Scale, Socket/Bone, Animation, License, LFS 용량을 감사한다.

2026-08-25 제공 ZIP 14개 감사 결과와 팩별 UE 버전·경로·위험, 첫 `DronePack FPV + Drone-Sounds` Spike 절차는 [`DRONE_ASSET_INTAKE_2026-08-25.md`](DRONE_ASSET_INTAKE_2026-08-25.md)를 따른다. `GC_DroneS` 기능 Blueprint는 UE 4.24 `PhysXVehicles` 의존성이 있어 메시·재질·Turret Part만 후보로 보고 기능은 프로젝트 코드로 재구현한다.

## 7. 작업 카드

| ID | 작업 | 완료 조건 |
|---|---|---|
| CTRL-01 | 고정 추적 Camera와 Mouse/Gamepad 입력 | 5 Action, 15 Mapping, 자동화 3/3과 수동 체감 확인 |
| HUD-01 | Telemetry Snapshot Component | 속도·고도·수직 속도·Heading을 10Hz Event로 제공 |
| HUD-02 | C++ 기능 + WBP Flight HUD | Drone Possess 중 실제 WBP로 네 수치를 화면에서 확인 |
| TUT-01 | Training Map과 비충돌 Spline | 별도 Map에서 수정 가능한 Spline과 Runtime 표시선이 비행·Collision·Overlap·Physics·Nav에 영향 없음 |
| TUT-02 | 순서형 Ring Gate | 정방향 현재 Gate만 한 번 통과 처리 |
| TUT-03 | Segment/Lap 기록 | 시간·실제 이동 거리·평균 속도 계산 |
| TUT-04 | 비교와 결과 UI | 이전 평균·Best 대비 ± 결과 표시 |
| TUT-05 | Tutorial 회귀 테스트 | 정상 Lap, 역순, 재통과, Restart를 자동/수동 검증 |
| FLT-01 | Take Off·Landing·Crash | 비행 상태와 Mission 실패 Event 연결 가능 |
| CTRL-02 | Operator·Drone 전환 | Blend, Possess, IMC 정리, Drone Hover 복귀 확인 |
| STY-01 | NPC 상호작용·대화 | 이동 잠금과 순차 대화 완료 Event 확인 |
| STY-02 | Mission Director·UI | Briefing부터 Evaluation까지 상태 전환 |
| STY-03 | Jamming Mission | 세 단계 효과와 회피/해제 목표 재현 |
| STY-04 | AI·MG 통합 | Drone 탐지와 대응을 Mission 흐름에서 재현 |
| AST-00 | 제공 에셋 인수 감사 | ZIP 14개와 해제본의 상대 경로·크기 일치 및 팩별 호환성·이식 위험 기록 |
| AST-01 | 제공 Drone 에셋 선별 적용 | UE 5.8 스테이징 검증 후 기능 코드 변경 없이 Integration BP에서 외형 교체 |

현재 `CTRL-01`, `HUD-01`, `HUD-02`, `TUT-01`, `TUT-02`, `TUT-03`을 완료했다. TUT-03은 Gate 0 시작, 이후 Gate별 Segment, 마지막 Gate Lap 완료와 World Game Time·Telemetry 위치 표본 기반 실제 거리·평균 속도 원본 기록을 포함한다. 2026-08-26 병합 main에서 Editor Build, 전체 `Drone.` 15/15, Blueprint Compile 0 errors·0 warnings·0 load failures를 통과했다. Unreal 저장소 로컬 `main`과 `origin/main`의 현재 기준선은 `fb1d7ad2c23d6bf3b1c854ca7c1c0cddba2062ef`이다.

다음 활성 카드는 `TUT-04`다. 이전 성공 평균·Best의 정확한 집계 규칙과 결과 UI는 현재 미구현이며, TUT-03의 성공 원본 History를 입력으로 사용한다.

## 8. 검증 게이트

- 각 카드 시작·중간 검증·종료 시 `WORKBOARD.md`의 현재 스냅샷과 `DRONE_WORKLOG.md`의 변경 이력을 함께 갱신
- C++ 변경마다 `DroneEditor Win64 Development` 빌드
- Blueprint 변경마다 Compile errors/warnings 0
- 새 `/Game/Drone` 자산에서 Legacy Variant 신규 의존성 0
- 각 입력 Mapping은 한 경로에서만 등록
- TUT-03 시간·거리·평균 속도와 TUT-04 Delta·첫 시도 예외는 각 카드에서 순수 C++ 자동화로 검증
- Gate는 정상 순서, 역순, 중복 Overlap, 잘못된 Pawn을 자동화 검증
- Operator↔Drone 전환을 새 PIE 3회 반복해 Pawn, Camera, IMC, HUD 중복 없음 확인
- Story Mission은 성공·Crash 실패·Jamming 해제 경로를 각각 반복
- 제공 에셋 적용 전후 Collision Root와 조작 테스트 결과가 동일해야 함

네트워크, Android, 협동 플레이, 구매 에셋 세부 튜닝은 현재 범위에서 제외한다.

## 9. AST-02A NavigationArrows 적용 경계 (2026-08-26)

`NavigationArrows`는 AI Navigation이나 Gate 판정을 담당하지 않는다. 화면 안·밖의 World Target을 투영해 방향 화살표와 Text를 보여 주는 공급사 `UUserWidget`이다.

- UE 5.8에서 검증한 최소 자산 6개만 `/Game/Drone/ThirdParty/NavigationArrows`에 둔다.
- 공급사 `NavigationArrowExampleActor`, Demo Map, Example Mesh는 사용하지 않는다.
- Gate 순서·현재 목표의 단일 기준은 계속 `UDroneTrainingGateSequenceComponent`다.
- 프로젝트 소유 Host/Wrapper가 로컬 Player에게 Widget 한 개만 생성하고 현재 Gate의 Target만 전달한다.
- Gate마다 Widget을 만들거나 공급사 Widget에서 Gate 목록을 검색하지 않는다.
- 정상 통과·Reset·Reconfigure에서 Target만 교체하고, Course 완료·UnPossess·EndPlay에서는 숨기거나 제거한다.
- 기존 Cyan Course 안내선과 Current/Inactive/Completed Gate Ring은 유지한다. NavigationArrow는 화면 밖 현재 목표를 보조하는 UI다.
- 실제 화면 연결, PIE/Standalone 시각 확인과 수명주기 회귀 검증 전에는 “목표 안내 UI 완료”로 판정하지 않는다.

자산 인수와 로드 검증을 완료하고 Commit `5a052c8`을 기능 Branch에 Push한 뒤 Merge Commit `fb1d7ad`로 `origin/main`에도 반영했다. `AST-02A`의 최소 이식·main 공유는 완료했지만 실제 Host/Wrapper 화면 연결은 후속 작업이다. 이 작업은 `TUT-04`의 이전 평균·Best 결과 UI와 별개다.

## 10. Dataflow·Chaos 물리 환경 확장 (2026-08-26)

- 일부가 고정된 그물·위장망은 Chaos Cloth Asset과 Dataflow Weight Map/Kinematic Selection으로 제작한다.
- 그물 변형은 물리 표현이고 Drone 포획·감속·Crash 판정은 별도 프로젝트 Trigger/상태가 소유한다.
- 선택형 벽·출입구·Jammer 설비는 Dataflow로 만든 Geometry Collection, Anchor/World Support, Damage Threshold와 Strain Field를 사용한다.
- 맵 전체 파괴는 범위에서 제외하고 명시적으로 지정한 대상만 파괴 가능하게 한다.
- 첫 Sandbox는 `TUT-04` 이후 또는 사용자가 우선순위를 명시적으로 변경했을 때 시작한다. 실제 그물 충돌은 Flight Collision, 파괴 Mission은 Damage/Crash와 Mission Shell 뒤에 연결한다.
- Plugin 활성화·자산 생성은 아직 하지 않았다. 상세 카드는 [`DRONE_CHAOS_DATAFLOW_PLAN.md`](DRONE_CHAOS_DATAFLOW_PLAN.md)를 따른다.
