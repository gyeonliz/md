# 구매 소스 확보 전 Drone 기능 우선 개발 계획

기준일: 2026-08-24 (Asia/Seoul)

## 1. 목적

외부 구매 소스가 아직 없는 동안 모델·환경·애니메이션·효과·사운드의 완성도를 기다리지 않고, Unreal Engine 기본 도형과 기존 Template 자산만으로 게임의 핵심 기능을 먼저 검증한다.

구매 전 목표는 완성된 그래픽 데모가 아니라 다음 Greybox 플레이 사이클이다.

```text
Spawn
→ Take Off
→ 기지 방향으로 비행
→ 적이 드론을 감지
→ 한 명이 빈 MG 터렛을 Claim하고 이동·점유
→ 다른 AI가 Prototype 대응 행동 수행
→ 목표 정보 획득
→ 귀환
→ 성공/실패 결과 확인
```

구매 소스가 예상보다 늦어져도 이 사이클까지는 Placeholder만으로 완성할 수 있게 한다.

사용자가 Tutorial과 Story 구성을 확정한 뒤의 최신 실행 순서는 [`DRONE_TUTORIAL_STORY_PLAN.md`](DRONE_TUTORIAL_STORY_PLAN.md)가 우선한다. 이 문서는 기존 PFN 카드, Placeholder 원칙과 에셋 교체 경계를 보존하는 참고 기준이다.

## 2. 현재 출발점

확인된 현재 상태는 다음과 같다.

- 작업컴 기본 작업 루트: `D:\JGY\project`
- UE 5.8.1 프로젝트: 작업컴 기록 경로 `D:\JGY\project\drone`; 이번 확인 PC `C:\URproject\drone`의 로컬 `main`과 `origin/main`은 TUT-03 완료 Commit `551e287`
- 문서 저장소: 작업컴 기록 경로 `D:\JGY\project\md`; 이번 확인 PC의 저장소 위치와 최신 동기화 상태는 [`STATUS.md`](../STATUS.md)를 따른다.
- 별도 `ADronePrototypePawn`과 `ADronePrototypeGameMode` C++ 구현 완료
- 컴포넌트 기본값과 standalone Spawn/Possess 자동화 테스트 완료
- 기존 Third Person 기본 맵과 전역 GameMode 유지
- PFN-01~05 완료: Prototype Input Action, IMC, Blueprint Pawn/GameMode, 전용 Greybox Map 생성·연결
- 고정 추적 Camera, Mouse X Drone Yaw, Mouse Y Camera Pitch와 Gamepad 6축을 구현했다. 새 계약의 `PIEInputLifecycle` 자동화 3/3, Standalone Keyboard·Mouse 수동 조작과 창 닫기 정상 종료를 확인해 PFN-06은 Done이다.
- Camera와 장치별 역할은 v1으로 확정했지만 감도·Mouse Y 반전·물리·Mesh·멀티플레이 방식은 미정
- Android는 현재 개발 범위에서 제외

`HUD-01` Telemetry Snapshot과 `HUD-02` C++ HUD 기능·실제 WBP 표시를 완료했다. 이어서 `TUT-01` Training Map과 비충돌 Spline도 완료했다. 별도 Map의 실제 `BP_DroneTrainingCourse`가 수정 가능한 Spline과 Runtime SplineMesh 안내선을 제공하며, 프로젝트 소유 불투명·Unlit·Emissive `M_DroneTrainingGuide`를 사용한다. Course Actor, Spline과 표시선은 Collision·Overlap·Physics·Navigation 영향을 모두 끈다. TUT-01 당시 전체 `Drone` 자동화 10/10, Tutorial 3/3, Blueprint Compile 오류·경고 0/0과 Standalone 안내선 표시를 확인했다.

`TUT-02`에서는 실제 `BP_DroneTrainingGate` 4개, Course의 명시적 Gate 순서와 정방향 통과 판정을 구현했다. 이어진 `TUT-03`에서는 정상 Gate Event만 구독하는 Course 소유 Recorder를 추가해 Segment/Lap 시간, 실제 3차원 이동 거리와 평균 속도 원본을 기록한다. 현재 `main=origin/main=551e287`이며 전체 `Drone.` 자동화 14/14, Tutorial 6/6, Blueprint Compile Errors/Warnings/Load Failures 0/0/0을 통과했다.

현재 실행 카드는 `TUT-04 이전 기록 비교·Best·결과 UI`다. 비교 규칙과 표시 형식은 구현 전에 확정하며, 현재 C++·BP·Editor 책임과 사용자 수동 확인법은 [`DRONE_CODE_STRUCTURE_AND_USER_TASKS.md`](DRONE_CODE_STRUCTURE_AND_USER_TASKS.md)를 따른다.

새 생산 코드는 `Source/Drone`, 새 자산은 `/Game/Drone` 아래에 둔다. ThirdPerson·Combat·Platforming·SideScrolling은 참고용 Legacy로 동결하고 신규 상속·참조를 만들지 않는다. Prototype IMC는 Pawn만 등록·제거하며 PlayerController와 Level Blueprint에는 같은 책임을 추가하지 않는다. 현재 검증 범위는 Standalone 싱글플레이이고 네트워크·Android·구매 에셋은 제외한다.

## 3. 구매 전 범위

### 반드시 구현할 것

- 정찰용 드론 한 대의 Flight MVP
- Enemy 한 종류의 Patrol과 Drone Detection
- Placeholder MG 터렛 하나의 단일 점유 흐름
- 비점유 AI의 Prototype 대응 행동 한 가지
- 목표 Actor 하나의 정보 획득 흐름
- 귀환 구역과 성공/실패 판정
- 상태 텍스트 중심의 최소 HUD와 Evaluation
- 새 PIE에서 반복 가능한 Greybox 한 사이클

### 구매 전에는 하지 않을 것

- 최종 드론·병사·터렛·환경 외형 제작과 세부 튜닝
- 최종 Skeleton Retargeting과 Animation Montage 구성
- 최종 Material, VFX, SFX, Cinematic 연출
- Placeholder 크기에 맞춘 최종 Collision·Camera·물리 수치 확정
- 여러 드론 종류와 여러 적 병과
- 실제 무기 성능이나 군사 장비의 1:1 재현
- 배터리, 통신 거리, 재밍, 협동 플레이, 2인 Listen Server
- EQS, Motion Warping, Aim Offset, Detour/RVO의 선제 도입
- 최종 점수 공식과 최종 게임 규칙 확정

이후 후보 기능은 Greybox Vertical Slice가 통과한 뒤 데모 가치와 일정으로 다시 평가한다.

## 4. Placeholder 기준

| 대상 | 구매 전 표현 | 기능 검증 기준 | 구매 후 교체 경계 |
|---|---|---|---|
| Drone | Sphere Collision + Cube/Cylinder 또는 Mesh 없음 | 이동·충돌·Camera·상태 | Visual Mesh만 BP 자식에서 교체 |
| Enemy | Capsule 또는 기존 Template Character | NavMesh·Perception·StateTree | Skeletal Mesh와 Anim BP만 교체 |
| MG Turret | Cube 2~3개와 Scene Component | Claim·Move·Use·Aim·Attack 이벤트 | Base/Yaw/Pitch 시각 Mesh 교체 |
| 목표물 | 색이 다른 Cube와 Trigger | 유효 목표 판정·1회 획득 | 목표 Visual만 교체 |
| 기지/지형 | Engine 기본 도형과 단색 Material | 이동 경로·시야 차폐·NavMesh | 환경 Modular Asset으로 교체 |
| HUD | Text·Progress 표시만 사용 | 상태와 이벤트 전달 | Widget Style과 Icon 교체 |
| 효과/사운드 | 로그·화면 텍스트·Debug Line | 이벤트 발생 여부 | Niagara·Sound 연결 |

Placeholder는 보기 좋게 만드는 대상이 아니다. 기능을 구분할 수 있는 색과 이름만 사용한다.

## 5. 나중에 에셋을 바꾸기 위한 구조 규칙

### 기능과 외형 분리

1. Collision과 Movement를 Visual Mesh에 의존시키지 않는다.
2. Drone Mesh를 Root로 사용하지 않는다.
3. Collision Root와 Actor Scale은 가능한 한 `(1,1,1)`을 유지하고 외형 축·Pivot·크기 보정은 별도 `VisualRoot` 후보에서 처리한다.
4. Visual Mesh는 기본적으로 Collision, Simulate Physics, Overlap, Navigation 영향을 끈다.
5. Camera, Sensor, Turret Use Point, Yaw Pivot, Pitch Pivot, Muzzle은 이름이 명확한 프로젝트 소유 `USceneComponent` 기준점을 사용한다.
6. 외부 Mesh의 Socket·Bone 이름은 Integration Blueprint 안에서만 연결한다.
7. C++은 구매 Asset 경로와 특정 Socket 이름을 직접 참조하지 않는다.
8. 구매 Mesh와 Material은 C++ 부모가 아니라 Blueprint 자식에서 배정한다.
9. 수치 조정은 `EditDefaultsOnly`, Data Asset 또는 Data Table 후보로 노출한다.
10. 게임 상태 전환은 Animation 완료 여부에 직접 묶지 않는다. Animation 연동이 필요해지는 시점에 별도 Event 경계를 추가한다.
11. Placeholder 단계에서 Root Motion, IK Retargeting, 최종 Rotor/Payload Socket을 만들지 않는다.
12. Placeholder 클래스 이름과 값에는 `Prototype` 또는 `Test`를 표시한다.

### 권장 Content 분리안

아래는 작업을 시작하기 위한 권장안이며 기존 Content 구조와 충돌하면 조정한다.

```text
Content/Drone/Core/
  Blueprints/
  Data/
  UI/

Content/Drone/Prototype/
  Blueprints/
  Input/
  Maps/
  Materials/
  UI/

Content/Drone/Integrations/
  <PackShortName>/

Content/<VendorOriginalFolder>/
```

`Core`는 Prototype이나 Vendor Asset을 참조하지 않는다. `Prototype`과 `Integrations/<Pack>`이 같은 Core 부모를 사용하고, Integration Blueprint만 Vendor 원본을 참조하는 의존 방향을 유지한다.

구매 에셋은 가능하면 원본 폴더를 유지하고, 프로젝트용 수정은 `Content/Drone/Integrations/<Pack>`의 Blueprint 자식·Wrapper·Material Instance에서 수행한다. 외부 Pack의 부모 Blueprint를 핵심 게임 로직의 부모로 바로 사용하지 않는다.

## 6. 전체 실행 순서

```text
P0. 현재 C++ 기준선
  ↓
P1. 입력·BP·Greybox 시험장
  ↓
P2. Telemetry HUD + Tutorial Vertical Slice (TUT-01~03 완료, TUT-04 비교·결과 UI 진행 예정)
  ↓
P3. Flight 상태 + Operator ↔ Drone
  ↓
P4. NPC·Mission UI Story Shell
  ↓
P5. Enemy AI + MG + Jamming
  ↓
P6. 통합 Greybox + 에셋 교체 준비
```

기존 PFN 번호는 유지하지만 실제 활성화 순서는 Tutorial에서 조작·Telemetry·기록 UI를 먼저 검증한 뒤 Story의 Operator·NPC·Mission·Jamming으로 확장한다.

경진대회 마감일과 팀원별 주간 투입 시간이 현재 문서에 확정되어 있지 않으므로 주차별 완료일은 임의로 만들지 않는다. 우선 모든 작업을 1~3시간 카드로 운영하고, 일정이 정해지면 이 의존 순서를 유지한 채 주차 계획으로 배치한다.

## 7. P1 — 입력·Blueprint·Greybox 시험장

| ID | 작업 | 예상 크기 | 의존성 | 완료 조건 |
|---|---|---:|---|---|
| PFN-01 | 임시 입력 계약 결정 | 1시간 | 없음 | Move·Altitude·Yaw·Look의 테스트 키와 Action Value Type 기록 |
| PFN-02 | Input Action 5개와 전용 IMC 생성 | 1~2시간 | PFN-01 | 5개 Action과 Keyboard·Mouse·Gamepad 15개 Mapping이 기록됨 |
| PFN-03 | `BP_DronePrototypePawn` 생성·자산 연결 | 1~2시간 | PFN-02 | IMC와 5개 Action이 BP Class Defaults에 연결됨 |
| PFN-04 | `BP_DronePrototypeGameMode` 연결 | 1시간 | PFN-03 | Default Pawn이 BP Prototype Pawn을 사용함 |
| PFN-05 | `Lvl_DronePrototype` Greybox 생성 | 2~3시간 | PFN-04 | PlayerStart·지면·장애물·높이 표식이 있는 별도 Map 실행 |
| PFN-06 | Spawn/Input 기준선 반복 PIE | 1시간 | PFN-05 | 새 PIE 3회 모두 Pawn 한 대 Spawn·Possess, 네 Callback 값 전달, IMC·입력 중복 없음 |

### P1 Map에 필요한 최소 도형

- 이륙 Pad 한 개
- 전후·좌우 이동을 확인할 바닥 Grid
- 고도 확인용 높이 표식 두 개 이상
- Collision 확인용 벽과 좁은 통로
- 시야 차폐 확인용 큰 벽
- 목표 Cube 한 개
- 귀환 영역 표시 한 개
- Patrol Point 두 개
- MG 터렛 배치용 평면 한 곳

상세 사막·산악·기지 미술 배치는 하지 않는다.

### P1 결정 게이트

다음은 최종 조작 방식으로 임의 확정하지 않는다.

- 현재 임시 입력 키는 PFN-06 동안 유지한다.
- Look 반전과 감도는 현재값을 유지하고 수동 화면 확인에서 체감만 기록한다.
- PFN-06 수평 이동은 현재 구현인 Actor-relative 기준으로 검증한다. 최종 Actor-relative/Camera-relative 선택은 별도 결정이다.

입력 계약은 Prototype 전용이며 최종 조작 방식 승인이 아니다.

## 8. P2 — Flight MVP

| ID | 작업 | 예상 크기 | 의존성 | 완료 조건 |
|---|---|---:|---|---|
| PFN-07 | 전후·좌우 이동 PIE 검증 | 1~2시간 | PFN-06 | 회전 전후에도 선택한 기준으로 왕복 이동 가능 |
| PFN-08 | 고도·Yaw PIE 검증 | 1~2시간 | PFN-06 | 서로 다른 높이 도달과 방향 전환 재현 |
| PFN-09 | Camera Prototype 조정 | 1~2시간 | PFN-07 | 이동·회전 중 기체와 경로 확인 가능 |
| PFN-10 | Take Off 상태 | 2~3시간 | PFN-07~09 | 지상 대기에서 이륙 완료로 한 번 전환 |
| PFN-11 | Landing 상태 | 2~3시간 | PFN-10 | 평평한 지면에 착륙하고 재이륙 가능 |
| PFN-12 | Crash/실패 공통 이벤트 | 2~3시간 | PFN-10 | 유효 충돌을 한 번만 실패 처리 |
| PFN-13 | Flight 상태 Debug 표시 | 1~2시간 | PFN-10~12 | Grounded·TakingOff·Flying·Landing·Failed 구분 가능 |
| PFN-14 | Flight 회귀 테스트 | 1~2시간 | PFN-07~13 | Spawn→Take Off→이동→Camera→Landing→Crash 반복 재현 |

현재 `UFloatingPawnMovement`와 수치는 기능 시험용이다. 이 단계의 통과가 최종 물리 확정을 뜻하지 않는다.

## 9. P3 — 최소 Mission Shell

| ID | 작업 | 예상 크기 | 의존성 | 완료 조건 |
|---|---|---:|---|---|
| PFN-15 | Mission 상태와 변경 Event 골격 | 1~2시간 | PFN-14 | Briefing·Recon·Acquired·Egress·Evaluation 전환 가능 |
| PFN-16 | Placeholder 목표 Actor | 1~2시간 | PFN-15 | 유효 목표 하나를 다른 Actor와 구분 가능 |
| PFN-17 | 정보 획득 Prototype | 2~3시간 | PFN-16 | 선택한 임시 판정으로 목표를 한 번만 획득 |
| PFN-18 | 귀환 Trigger | 1~2시간 | PFN-17 | 정보 획득 뒤 진입할 때만 완료 처리 |
| PFN-19 | Flight 실패와 Mission 연결 | 1~2시간 | PFN-12, PFN-15 | Crash가 중복 없이 Evaluation 실패로 연결 |
| PFN-20 | Mission 상태 Debug Text | 1~2시간 | PFN-15~19 | 콘솔 없이 현재 Mission 상태 확인 |
| PFN-21 | 비행 Mission Shell 반복 테스트 | 1~2시간 | PFN-20 | 출격→획득→귀환과 Crash 실패를 각각 재현 |

### P3 결정 게이트

정보 획득 방식은 다음 후보 중 Prototype 하나만 선택한다.

- 목표 Trigger 진입
- 카메라 방향과 거리 조건
- 일정 시간 목표 유지
- 임시 상호작용 입력

선택한 방식은 기능 연결을 위한 임시 기준이며 최종 정찰 규칙이 아니다.

## 10. P4 — Enemy AI와 MG Turret

| ID | 작업 | 예상 크기 | 의존성 | 완료 조건 |
|---|---|---:|---|---|
| PFN-22 | Placeholder Enemy와 AI Controller | 1~2시간 | PFN-05 | Capsule/Template 외형으로 Controller Possess 확인 |
| PFN-23 | NavMesh 단일 이동과 Patrol | 2~3시간 | PFN-22 | Patrol Point 두 곳을 반복 이동 |
| PFN-24 | AI Perception Sight | 1~2시간 | PFN-23 | 시야 안·밖·차폐 뒤 감지/상실 구분 |
| PFN-25 | Drone 대상 필터 | 1시간 | PFN-24 | 비대상 Actor는 반응 상태를 시작하지 않음 |
| PFN-26 | 최소 StateTree 전환 | 2~3시간 | PFN-25 | Patrol→DroneDetected→대응 상태 재현 |
| PFN-27 | Placeholder MG Turret 구조 | 2~3시간 | PFN-05 | Use Point·Yaw/Pitch Pivot·Muzzle 기준점 확인 |
| PFN-28 | 단일 Slot Claim·Use·Release | 2~3시간 | PFN-22, PFN-27 | AI 두 명 중 한 명만 점유하고 정상 종료 시 반환 |
| PFN-29 | MoveToTurret와 UseTurret | 2~3시간 | PFN-26, PFN-28 | 감지한 AI가 예약한 위치에 도착해 사용 상태 유지 |
| PFN-30 | 조준·공격 Debug Event | 2~3시간 | PFN-29 | 점유 AI만 목표를 추적하고 상실 시 정지 |
| PFN-31 | 비점유 AI 대응 한 가지 | 2~3시간 | PFN-26, PFN-28~29 | Claim 실패 AI가 선택한 Prototype 행동으로 전환 |
| PFN-32 | Enemy AI 회귀 테스트 | 1~2시간 | PFN-23~31 | Patrol→Detect→Claim→Move→Use→Attack과 다른 AI 분기 반복 |

### P4 Placeholder 표현

- Enemy 상태: 머리 위 Text 또는 Debug 색
- 감지: Perception Debug와 로그
- MG 회전: Yaw/Pitch Scene Component 회전
- 발사: Debug Line 또는 단순 공격 Event
- 점유: 터렛의 Debug Text로 `Free`, `Claimed`, `InUse` 표시

공격 방식, 피해량, 탄도, Animation, 실제 MG 외형은 확정하지 않는다.

### P4 결정 게이트

- Suspicious와 Confirm을 별도 상태로 둘지
- Claim 실패 AI가 TakeCover 또는 Search 중 무엇을 시험할지
- 공격을 Debug Line, Line Trace, 단순 Event 중 무엇으로 시험할지

한 번에 하나만 선택해 Prototype으로 기록한다.

## 11. P5 — HUD·Evaluation·통합 Greybox

| ID | 작업 | 예상 크기 | 의존성 | 완료 조건 |
|---|---|---:|---|---|
| PFN-33 | 최소 HUD Event 연결 | 2~3시간 | PFN-20, PFN-32 | Flight·Mission·Enemy 반응 상태를 Text로 확인 |
| PFN-34 | Evaluation 성공/실패 화면 | 1~2시간 | PFN-19 | 두 결과와 재시작 경로 표시 |
| PFN-35 | AI 반응을 Mission 흐름에 통합 | 1~2시간 | PFN-21, PFN-32 | Recon 중 감지와 터렛 대응이 자연스럽게 발생 |
| PFN-36 | Greybox 한 사이클 연결 | 2~3시간 | PFN-33~35 | Debug 명령 없이 출격부터 Evaluation까지 진행 |
| PFN-37 | 새 PIE 3회 연속 테스트 | 1~2시간 | PFN-36 | 세 실행의 Pass/Fail과 실패 위치를 각각 기록 |
| PFN-38 | 결함을 1~3시간 카드로 분리 | 1시간 | PFN-37 | 재현 절차·예상·실제 결과가 있는 결함 목록 작성 |

### 구매 전 Vertical Slice 완료 기준

PFN-37의 최신 결과가 **3회 연속 Pass**여야 이 게이트를 통과한다. 한 번이라도 실패하면 PFN-38에서 수정 카드를 만들고, 수정 뒤 PFN-37을 다시 실행한다. 실패 위치를 기록한 것만으로 Vertical Slice를 통과한 것으로 보지 않는다.

- 외부 구매 에셋 없이 실행된다.
- Drone 한 대, Enemy 두 명 이상, Turret 한 개, 목표 한 개만으로 핵심 흐름이 보인다.
- 한 AI만 Turret을 점유한다.
- 다른 AI가 선택한 Prototype 대응 행동을 수행한다.
- 정보 획득 전 귀환은 성공 처리되지 않는다.
- Crash는 한 번만 실패 처리된다.
- 성공과 실패가 각각 Evaluation으로 이어진다.
- 새 PIE 세 번에서 결과가 재현된다.
- 기존 Third Person 기본 실행 경로가 깨지지 않는다.

## 12. P6 — 구매 요구사항과 교체 준비

| ID | 작업 | 예상 크기 | 의존성 | 완료 조건 |
|---|---|---:|---|---|
| PFN-39 | 구매 에셋 요구사항 표 작성 | 1~2시간 | PFN-38, PFN-37 Pass | Drone·Enemy·Turret·환경별 필수 조건과 제외 조건 기록 |
| PFN-40 | 기능↔Visual 교체 계약 점검 | 1~2시간 | PFN-39 | Mesh를 바꿔도 핵심 C++ 변경이 필요 없는지 확인 |
| PFN-41 | License·엔진 호환·용량 점검표 | 1~2시간 | PFN-39 | 후보 Pack마다 구매 전 확인란 존재 |
| PFN-42 | 외부 에셋 격리 통합 절차 | 1시간 | PFN-41 | 별도 Branch/Test Map/담당자/복구 절차 기록 |
| PFN-43 | Placeholder 교체 Smoke Test | 1~2시간 | PFN-40 | 다른 기본 Mesh로 교체해도 기능 회귀 없음 |

### 구매 후보 확인 항목

- 사용 License와 팀/경진대회 영상·빌드 배포 가능 범위
- UE 5.8 프로젝트에서 Import 또는 Migration 가능 여부
- 추가 Plugin 의존성
- Skeletal Mesh라면 Rig, Skeleton, Animation 포함 범위
- Static Mesh의 Pivot, Forward 방향, Scale, Collision, LOD
- Turret의 Base/Yaw/Pitch 분리 여부
- Drone의 Camera/Sensor 장착 위치를 만들 수 있는지
- Environment의 Modular 단위와 NavMesh/Collision 적합성
- Texture 해상도와 전체 저장소/LFS 용량 영향
- 유지보수·업데이트 필요성과 원본 폴더 변경 위험

특정 Pack이 좋다는 이유만으로 기능 구조를 그 Pack의 Blueprint에 종속시키지 않는다.

## 13. 구매 후 통합 순서

구매 소스가 생기면 한꺼번에 모두 교체하지 않는다.

1. 구매 원본과 License 정보를 기록한다.
2. 별도 Feature Branch와 Asset Test Map에서 한 Pack만 추가한다.
3. Import 후 생성 파일과 Plugin 의존성을 확인한다.
4. 원본 Asset은 가능한 한 이동·이름 변경하지 않는다.
5. 프로젝트 BP 자식에서 Visual만 연결한다.
6. Scale, Pivot, Collision, Socket, Animation 호환을 확인한다.
7. Flight 또는 AI 회귀 테스트를 실행한다.
8. 변경 파일과 LFS 용량을 검토한다.
9. 담당자 Review 뒤 통합한다.
10. 다음 Pack으로 넘어간다.

## 14. 5인 팀 병행 작업 묶음

정확한 역할은 변경 가능하므로 아래는 고정 배정이 아니라 파일 충돌을 줄이는 작업 묶음이다.

| 작업 묶음 | 구매 전 할 수 있는 일 | 주 수정 영역 |
|---|---|---|
| 기능 코드 | Flight·Mission·AI·Turret C++과 부모 BP | `Source`, 핵심 부모 BP |
| Greybox Map | 이동 경로·장애물·시야 차폐·Patrol/Turret 위치 | Prototype Map 또는 담당 Sublevel |
| UI·상태 표현 | Text HUD·Evaluation·Debug 색상 | Prototype UI |
| QA·데모 흐름 | 테스트 절차·결함 재현·3회 반복 기록 | 문서와 별도 테스트 자료 |
| 에셋 준비 | 요구사항 표·후보 조사·License·호환성 확인 | 문서, 구매 후 ThirdParty 폴더 |

한 사람이 Map을 편집하는 동안 다른 사람은 같은 `.umap`을 수정하지 않는다. 각 Blueprint와 Map의 담당자를 Doing 카드에 기록한다.

## 15. 단계별 검증 원칙

모든 카드는 다음 공통 조건을 만족해야 Done이다.

- 외부 구매 에셋 없이 재현할 수 있다.
- 카드에 적힌 결과물과 완료 조건이 확인됐다.
- Placeholder 값과 임시 선택은 `Prototype/Test`로 표시했다.
- 같은 기능에 관련 없는 `.uasset`이나 `.umap`을 함께 수정하지 않았다.
- 기능과 Visual 교체 경계가 유지된다.

구현·런타임 카드에는 다음 조건을 추가한다.

- C++ 변경이 있다면 `DroneEditor Win64 Development`가 빌드된다.
- Blueprint 변경이 있다면 참조·Compile 오류가 없다.
- 카드가 요구하는 새 PIE 테스트를 수행했다.
- 정상 결과와 실패 시 확인 항목을 기록했다.

결정·조사·문서 카드에는 PIE를 강제하지 않는다. 대신 선택 근거, 미정 항목, 검토자, 후속 카드가 기록되어야 한다.

자동화 가능한 C++ 상태, Spawn/Possess, Reservation, Mission 전환은 자동화 테스트 후보로 추가한다. LocalPlayer 입력, Blueprint 연결, Map 배치, Camera는 Editor PIE로 별도 확인한다.

## 16. 바로 시작할 순서

현재 기준 P1 진행 상태는 다음과 같다.

```text
PFN-01~05 Done
→ PFN-06 Done (자동화 3/3 + Standalone 수동 Pass)
→ HUD-01·02 Done
→ TUT-01 Training Course/Spline Done
→ TUT-02 Gate·순서·정방향 Done
→ TUT-03 Segment/Lap 원본 기록 Done
→ TUT-04 결과 UI
→ Take Off·Landing·Crash
→ Operator↔Drone와 NPC·Mission UI
→ Enemy AI·MG·Jamming
→ 통합 Greybox·에셋 교체 준비
```

현재는 TUT-03 Segment/Lap 원본 기록까지 통과했으므로 TUT-04 이전 기록 비교·Best·결과 UI부터 Tutorial Vertical Slice를 이어간다. 비교 규칙과 화면 표시를 검증한 뒤 Take Off와 Landing 상태 구현으로 넘어간다. 외부 구매 에셋은 이 순서의 선행 조건이 아니며 Android는 현재 범위에서 제외한다.
