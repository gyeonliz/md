# 드론 프로젝트 MVP 개발 가이드

> 현재 구현 지점: Camera/Input PFN-06, HUD-01 Telemetry, HUD-02 Flight HUD, TUT-01 Training Course, TUT-02 순서형 Ring Gate와 TUT-03 Segment/Lap 원본 기록까지 완료했다. Course가 소유한 Recorder가 정상 Gate Event와 기존 Telemetry 10Hz 위치 표본을 사용해 World Game Time, 실제 3차원 이동 거리와 평균 속도를 기록한다. Source 기준은 맵 중앙화·템플릿 콘텐츠 정리를 포함한 `main=origin/main=2cc5d79`이고, 전체 `Drone.` 자동화 15/15, Blueprint Compile Errors/Warnings/Load Failures 0/0/0을 통과했다. 다음 카드는 TUT-04 이전 기록 비교·Best·결과 UI다. 입력 결과는 [`DRONE_PROTOTYPE_IMPLEMENTATION.md`](DRONE_PROTOTYPE_IMPLEMENTATION.md), Telemetry/HUD 결과는 [`DRONE_TELEMETRY_IMPLEMENTATION.md`](DRONE_TELEMETRY_IMPLEMENTATION.md), TUT-01 결과는 [`DRONE_TRAINING_COURSE_IMPLEMENTATION.md`](DRONE_TRAINING_COURSE_IMPLEMENTATION.md), TUT-03 결과는 [`DRONE_TRAINING_RECORDING_IMPLEMENTATION.md`](DRONE_TRAINING_RECORDING_IMPLEMENTATION.md), 현재 C++·BP 책임과 사용자 확인 절차는 [`DRONE_CODE_STRUCTURE_AND_USER_TASKS.md`](DRONE_CODE_STRUCTURE_AND_USER_TASKS.md)를 따른다.

> 현재 실행 순서는 [`DRONE_TUTORIAL_STORY_PLAN.md`](DRONE_TUTORIAL_STORY_PLAN.md)가 우선한다. PFN 카드 번호와 Placeholder 교체 경계는 [`DRONE_PREASSET_FUNCTION_PLAN.md`](DRONE_PREASSET_FUNCTION_PLAN.md)를 함께 따른다.

## 1. 문서 목적

이 문서는 Unreal Engine 5.8.1 기반 드론 시뮬레이터 게임 프로젝트를 작은 기능 단위로 구현하고 검증하기 위한 작업 기준이다. 목표는 거대한 게임을 먼저 만드는 것이 아니라, 짧더라도 아래 플레이 사이클이 끝까지 이어지는 데모를 완성하는 것이다.

`출격 → 기지 접근 → 적 탐지 → 적이 드론을 발견 → 병사가 비어 있는 MG 터렛으로 이동·점유 → 다른 병사의 대응 → 드론 회피 → 목표 정보 획득 → 귀환 → 평가`

모든 작업은 가능하면 1~3시간 안에 끝낼 수 있는 크기로 나누고, 한 기능을 Editor에서 확인한 뒤 다음 기능으로 넘어간다.

## 2. 현재 기준과 미정 사항

### 확정된 기준

- 엔진: Unreal Engine 5.8.1
- 팀 규모: 대학생 5명
- 기존 논의 기준: 개발 1명, 모델링/콘텐츠 작업 인원 다수
- 첫 구현 대상: 정찰용 멀티콥터 1종
- 핵심 요소: 드론 운용, 정찰, 침투, 탐지, 적 AI 반응, 임무, 귀환, 평가
- 현재 v1 조작: 고정 추적 Camera, Actor-relative 이동, World Up 고도, Mouse X Drone Yaw, Mouse Y Camera Pitch, Gamepad Left Stick·Trigger·Right Stick
- 현재 기능 우선 순서: TUT-04 이전 기록 비교·결과 UI → Flight 상태 → Operator↔Drone → NPC·Mission UI·Jamming → AI/MG → 에셋 통합
- 후속 물리 환경: Dataflow/Chaos Sandbox → 부분 고정 그물 → 선택형 벽·Jammer 파괴. Flight Collision/Damage 기준 뒤 연결
- J3C: 프로젝트 콘셉트에서 사용하는 가상의 외주 발주처 설정일 뿐이며, 실제 계약·협력·지원·공식 관계가 아니다.

### 현재 미정이며 구현 중에도 확정된 것처럼 다루지 않을 항목

- 입력 감도, Mouse Y 반전, 조종 보조와 최종 물리 반응
- 최종 물리 모델과 비행 보조 수준
- 최종 드론 종류·이름·디자인
- 군·국가·적군 국적 및 세계관 설정
- 최종 게임 규칙, 점수 공식, 실패 조건의 세부 수치
- 최종 멀티플레이 방식과 2인 Listen Server 적용 여부
- 배터리, 통신 거리, 신호 상태, 재밍, 제한 시간, 협동 플레이의 채택 여부

미정 항목이 필요한 작업에서는 임시 테스트 값을 사용할 수 있다. 이 경우 이름이나 주석에 `Prototype` 또는 `Test`임을 표시하고 최종 결정으로 기록하지 않는다.

## 3. 구현 원칙

1. C++은 핵심 상태와 재사용 가능한 동작을 담당한다.
2. Blueprint는 에셋 연결, 조정 가능한 값, 빠른 시각 검증에 사용한다.
3. 한 작업마다 Editor 재현 절차와 통과 조건을 둔다.
4. 실패한 테스트는 다음 기능으로 넘어가기 전에 원인을 기록한다.
5. `.uasset`과 `.umap`은 병합이 어렵기 때문에 담당 파일을 분리하고 같은 에셋의 동시 수정을 피한다.
6. 기능 구현과 콘텐츠 제작을 분리해, 코드가 임시 메시·맵에서도 검증 가능하게 만든다.
7. Cloth·Destruction은 연출과 시뮬레이션을 담당하고 포획·Damage·Mission 판정은 프로젝트 C++ 상태가 담당한다.

### 기능 설명·구현 기록 형식

새 기능을 만들거나 설명할 때 다음 순서를 사용한다.

1. 왜 필요한가
2. Unreal에서 어느 클래스 또는 컴포넌트가 담당하는가
3. 헤더에 무엇을 추가하는가
4. CPP에 무엇을 추가하는가
5. Blueprint에서 무엇을 설정하는가
6. Editor에서 어떻게 테스트하는가
7. 정상 결과는 무엇인가
8. 문제가 생기면 무엇을 확인하는가

## 4. 프로젝트 구조 초안

아래 이름은 초기 가이드의 역사적 후보이며 최종 클래스명은 아니다. 현재 새 생산 코드는 `Source/Drone`, 새 자산은 `/Game/Drone` 아래에 두므로 이 초안을 따라 중복 루트를 만들지 않는다.

```text
Source/<ProjectName>/
  Drone/
    DroneControllable.*         # 스파이크에서 선택한 조종 클래스의 이름 후보
    DroneFlightComponent.*      # 이동 계산을 분리할 때의 후보
  AI/
    EnemyAIController.*         # 감지와 상태 전환 연결 후보
    EnemyCharacter.*            # 병사 표현 후보
  Interaction/
    TurretActor.*               # MG 터렛과 점유 상태 후보
  Mission/
    MissionManager.*            # 임무 진행과 완료/실패 상태 후보
  UI/
    DroneHUD.*                  # 비행·임무 정보 표시 후보

Content/
  Blueprints/Drone/
  Blueprints/AI/
  Blueprints/Interaction/
  Blueprints/Mission/
  UI/
  Maps/Prototype/
  StateTrees/
  SmartObjects/
  Art/
```

첫 비행체는 `Pawn` 기반을 우선 후보로 검토한다. 이는 드론이 일반적인 보행 `Character`의 캡슐·보행 이동을 반드시 필요로 하지는 않기 때문이다. 다만 최종 Pawn/Character 선택과 물리 모델은 현재 미정이다. 첫 스파이크에서 요구사항과 테스트 결과로 조종 클래스를 선택하며, 이후 작업의 클래스명과 책임은 그 결과를 따른다.

## 5. 현재 추천 작업 순서와 단계별 통과 기준

현재 실행 순서는 PFN 카드와 [`DRONE_PREASSET_FUNCTION_PLAN.md`](DRONE_PREASSET_FUNCTION_PLAN.md)를 따른다. 아래 상세 작업 목록의 장별 배치보다 이 순서가 우선한다.

```text
PFN-06 Spawn/Input 기준선
→ PFN-07~14 Flight MVP
→ PFN-15~21 최소 Mission Shell
→ PFN-22~32 Enemy AI/MG
→ PFN-33~38 HUD·Evaluation·통합 Greybox
→ PFN-39~43 에셋 교체 준비
```

- Flight MVP 통과: 한 대가 생성되어 이륙·이동·Yaw·고도 변경·카메라 확인·착륙을 수행하고 충돌/실패를 확인할 수 있다.
- 최소 Mission Shell 통과: 출격부터 정보 획득, 귀환, 완료/실패 판정까지 최소 상태가 이어진다.
- Enemy AI/MG 통과: 순찰 중인 AI가 드론을 감지하고, 한 명이 빈 터렛을 점유해 공격 상태로 전환한다. 점유되지 못한 AI는 현재 테스트에서 선택한 Prototype 대응 한 가지를 수행한다. 점유자 사망·소멸 후 다른 AI가 이어서 사용하는 승계 기능은 이 통과 기준에 포함하지 않는다.
- UI/Evaluation 통과: 플레이어가 필요한 상태를 확인하고 종료 시 결과를 볼 수 있다. 세부 점수 공식은 별도 확정 전까지 임시 판정만 사용한다.
- 통합 데모 통과: 위 흐름을 새 실행에서 반복 재현할 수 있다.

## 6. Flight MVP 작업 목록

각 항목은 독립적으로 커밋하고 Editor에서 확인한다.

### F-01. C++ 프로젝트와 프로토타입 맵 확인 — 1~2시간

- 목적: 이후 기능을 검증할 최소 실행 환경 확보
- C++/클래스: 게임 모듈이 UE 5.8.1에서 컴파일되는지 확인
- Blueprint: 없음 또는 빈 테스트 GameMode만 연결
- Editor 테스트: 프로토타입 맵을 열고 PIE 실행
- 통과 조건: 컴파일 오류 없이 빈 맵이 실행됨
- 문제 확인: 엔진 버전, UE가 인식하는 설치된 Visual Studio C++ 워크로드/툴체인, 프로젝트 파일 생성, 모듈 의존성

### F-02. 스파이크에서 선택한 조종 클래스 골격 생성 — 1~2시간

- 목적: 플레이어가 소유할 드론 Actor의 책임 범위 확인
- C++/클래스: 앞선 스파이크에서 선택한 Pawn/Character 기반을 사용하며, 결과가 바뀌면 이 카드의 클래스명과 설정도 함께 변경
- 헤더: 루트, 기체 메시 기준 컴포넌트, 카메라 기준 컴포넌트 선언
- CPP: 기본 서브오브젝트 생성과 부착 관계 구성
- Blueprint: C++ 클래스를 부모로 하는 프로토타입 BP 생성, 임시 메시 연결
- Editor 테스트: 맵에 배치하고 Possess 여부 확인
- 통과 조건: PIE에서 한 대가 생성되고 플레이어가 제어 대상을 소유함
- 문제 확인: 선택한 조종 클래스의 Possess 설정, Pawn을 선택했다면 Auto Possess와 GameMode Default Pawn, 컴포넌트 루트/부착 관계

### F-03. 드론 Spawn 경로 하나 확정 — 1시간

- 목적: 맵 직접 배치와 GameMode 생성이 중복되지 않게 함
- C++/Blueprint: 현재 프로토타입에서 사용할 한 경로만 선택
- Editor 테스트: PIE를 여러 번 실행해 드론 수 확인
- 통과 조건: 시작할 때 항상 정확히 한 대가 생성됨
- 문제 확인: 선택한 생성 경로, Pawn을 선택했다면 월드 배치 Pawn과 Default Pawn의 중복

### F-04. 임시 입력 자산과 입력 연결 — 1~2시간

- 목적: 비행 기능을 시험할 입력 이벤트 확보
- C++/클래스: 스파이크에서 선택한 조종 클래스의 입력 바인딩 또는 별도 입력 전달 구조
- 헤더: 테스트에 필요한 액션 콜백 선언
- CPP: 이동·Yaw·고도 명령으로 전달
- Blueprint/Editor: 임시 Input Action과 Mapping Context 연결
- 통과 조건: 입력 이벤트와 축 값이 디버그로 확인됨
- 주의: 키 배치와 최종 입력 방식은 미정이다. 이 작업의 매핑은 테스트용이다.
- 문제 확인: Mapping Context 등록 시점, Player Controller, 입력 소비 여부

### F-05. 전진/후진 이동 — 1~2시간

- 목적: 드론의 첫 수평 이동 축 검증
- C++: 프레임 입력을 이동 처리에 전달하고 속도를 조정 가능한 값으로 둠
- Blueprint: 테스트용 속도 값 설정
- Editor 테스트: 고정된 기준점 사이를 왕복
- 통과 조건: 입력 방향과 이동 방향이 일치하고 입력 해제 시 의도한 프로토타입 동작을 보임
- 주의: 가속·감속·관성 및 최종 물리 방식은 미정이다.

### F-06. 좌/우 이동 — 1~2시간

- 목적: 두 번째 수평 이동 축 검증
- C++: 전후 이동과 독립된 좌우 명령 처리
- Blueprint/Editor: 기준 격자 또는 표식을 두고 방향 확인
- 통과 조건: 회전 상태에서도 선택한 로컬/월드 기준이 일관됨
- 주의: 로컬 좌표와 월드 좌표 중 최종 조작 기준은 확정 전 테스트 기록으로 남긴다.

### F-07. Yaw — 1~2시간

- 목적: 기체 방향 전환 검증
- C++: Yaw 입력과 회전 속도 처리
- Blueprint: 회전 속도 노출
- Editor 테스트: 90도 단위 표식을 향해 회전
- 통과 조건: 방향 전환 후 전진 기준이 예상과 일치함
- 문제 확인: Controller Rotation과 Actor Rotation의 중복 적용

### F-08. 고도 변경 — 1~2시간

- 목적: 상승·하강 명령 검증
- C++: 수직 이동 명령과 테스트 범위 처리
- Blueprint: 수직 속도 테스트 값 설정
- Editor 테스트: 서로 다른 높이의 표식 도달
- 통과 조건: 상승/하강이 안정적으로 재현됨
- 주의: 고도 제한과 자동 고도 유지의 최종 규칙은 미정이다.

### F-09. Take Off 상태 — 1~2시간

- 목적: 지상 대기와 비행 가능 상태를 구분
- 헤더: 최소 비행 상태 또는 상태 플래그 선언
- CPP: 이륙 시작·완료 조건과 중복 입력 방지
- Blueprint: 필요 시 이륙 높이/시간을 테스트 값으로 설정
- Editor 테스트: 지상에서 이륙 후 이동 가능 여부 확인
- 통과 조건: 지상 상태에서는 의도하지 않은 비행이 없고 한 번의 이륙 흐름이 완료됨
- 주의: 자동/수동 이륙의 최종 조작 규칙은 미정이다.

### F-10. Landing 상태 — 1~2시간

- 목적: 비행 종료와 지상 상태 복귀 검증
- C++: 착륙 시작·접지·완료 상태 처리
- Blueprint/Editor: 평평한 테스트 지면에서 실행
- 통과 조건: 착륙 후 지상 상태가 되고 다시 이륙 테스트가 가능함
- 문제 확인: 충돌 채널, 접지 판정, 상태 전환 중 입력

### F-11. 카메라 — 1~2시간

- 목적: 비행과 정찰에 필요한 시야 확보
- C++/컴포넌트: Camera 및 필요 시 SpringArm 구성
- Blueprint: 위치·회전·시야각을 조정 가능한 값으로 둠
- Editor 테스트: 전후/좌우/고도/Yaw 중 시야 확인
- 통과 조건: 기체와 환경을 확인하며 조종할 수 있음
- 주의: 최종 FPV/정찰 카메라 모드와 전환 방식은 미정이다.

### F-12. 충돌과 Crash/실패 이벤트 — 2~3시간

- 목적: 데모에서 실패 흐름을 시작할 공통 이벤트 확보
- 헤더: 충돌 수신 함수와 실패 이벤트 선언
- CPP: 유효한 충돌을 한 번만 실패 처리하도록 보호
- Blueprint: 임시 효과 또는 디버그 메시지 연결
- Editor 테스트: 장애물에 의도적으로 충돌
- 통과 조건: 실패가 중복 발생하지 않고 조작/재시작 흐름으로 이어질 수 있음
- 주의: 충돌 속도 임계값, 내구도, 드론 손실 규칙은 미정이다.

### F-13. Flight MVP 회귀 테스트 — 1~2시간

- 순서: Spawn → Take Off → 전후 → 좌우 → Yaw → 고도 → Camera → Landing → Crash
- 통과 조건: 새 PIE 세션에서 전체 순서를 반복 재현하고 오류를 작업 목록으로 분리함
- 결과물: 짧은 테스트 기록과 알려진 문제 목록

## 7. Enemy AI MVP 작업 목록

기능 도입의 현재 우선순위는 `AI Perception → StateTree → NavMesh → Smart Object → Turret Interaction`이다. 다만 아래 카드에서는 Patrol과 MoveToTurret이 이동 가능한지 먼저 확인하기 위해 A-02에서 NavMesh 단일 이동 검증을 선행한다. 이는 기술 우선순위를 바꾸거나 NavMesh 기반 행동을 먼저 완성한다는 뜻이 아니라, 이후 이동 카드의 전제 조건을 짧게 검증하는 작업이다. EQS, Motion Warping, Detour/RVO 등은 필요한 시점에만 추가한다.

### A-01. Enemy Character/Controller 골격 — 1~2시간

- 목적: 감지와 행동을 시험할 최소 AI 준비
- C++: Enemy Character와 AI Controller 후보 생성
- Blueprint: 임시 캐릭터와 Controller 연결
- Editor 테스트: NavMesh가 있는 맵에서 생성 확인
- 통과 조건: AI가 Controller에 의해 소유되고 디버그 가능함

### A-02. NavMesh 이동 한 점 테스트 — 1~2시간

- 목적: 상태 로직 전에 기본 이동 경로 검증
- Blueprint/Editor: 단일 목적지로 Move To 실행
- 통과 조건: 성공/실패 결과가 확인되고 목적지에 도달함
- 문제 확인: NavMesh Bounds, Agent 크기, 충돌, 도달 반경

### A-03. Patrol 최소 루프 — 2~3시간

- 목적: 감지 전 기본 행동 확보
- StateTree 또는 현재 선택한 최소 상태 구조: Patrol 상태와 지점 이동
- Editor 테스트: 2개 이상의 테스트 지점 순환
- 통과 조건: 드론이 없을 때 순찰을 반복함

### A-04. AI Perception Sight 설정 — 1~2시간

- 목적: 드론 발견 이벤트 확보
- C++/Controller: AI Perception과 Sight 후보 구성
- Blueprint: 시야 거리·각도는 테스트 값으로 조정
- Editor 테스트: 드론을 시야 안/밖과 장애물 뒤에 배치
- 통과 조건: 감지 시작과 상실 이벤트가 구분됨
- 문제 확인: 드론의 Stimuli Source 수동 등록 또는 자동 등록 설정, Sight를 차폐해야 하는 오브젝트의 충돌 설정, Affiliation/Team 필터, 시야 디버그

### A-05. Drone Actor 감지 검증 — 1시간

- 목적: 다른 Actor가 아니라 드론만 현재 실험 대상으로 분류
- C++: 감지된 Actor 유효성 확인과 대상 저장/해제
- Editor 테스트: 드론과 비대상 Actor를 함께 배치
- 통과 조건: 드론 감지만 상태 전환 입력으로 사용됨

### A-06. StateTree 기본 상태 — 2~3시간

- 목적: 행동 전환을 눈에 보이는 상태로 관리
- 상태: Idle, Patrol, DroneDetected의 최소 연결. Suspicious와 Confirm을 별도 상태로 둘지는 이 Prototype 카드에서 결정하고 기록
- Blueprint/Editor: 상태별 디버그 표시
- 통과 조건: 감지/상실 조건에 따라 선택한 최소 전환이 재현되고, Suspicious/Confirm 사용 여부가 Prototype 결정으로 기록됨
- 주의: Confirm 상태의 채택 여부, 확인 시간, Suspicious 세부 규칙은 최종 규칙이 아니다.

### A-07. MG Turret Actor 상호작용 지점 — 1~2시간

- 목적: AI가 향할 수 있는 빈 터렛 표현
- C++/Blueprint: 터렛 Actor와 사용 위치/방향 표시
- Editor 테스트: AI가 사용 지점까지 이동 가능한지 확인
- 통과 조건: 배치한 터렛의 상호작용 위치가 NavMesh 위에서 유효함

### A-08. 터렛 Reservation/Occupancy — 2~3시간

- 목적: 한 터렛을 한 명만 점유하도록 보장
- C++ 또는 Smart Object로 점유 모델을 구성. Smart Object를 선택하면 터렛 하나에 단일 사용 slot을 두고 `Claim → Use → Release` 수명주기를 구현. Claim은 사용권 확보, Use는 실제 점유, Release는 정상 종료·취소 때 사용권 반환을 뜻함
- Editor 테스트: AI 두 명이 같은 터렛을 동시에 요청
- 통과 조건: 한 AI만 slot Claim과 Use에 성공하고, 다른 AI는 Claim 실패 결과를 받으며, 정상 종료 후 Release됨
- 문제 확인: Claim과 Use 사이의 취소, 정상 종료 시 Release 누락, 중복 Claim/Use 요청

### A-09. MoveToTurret 상태 — 2~3시간

- 목적: 드론을 발견한 AI가 예약한 터렛으로 이동
- StateTree: DroneDetected → 단일 slot Claim 성공 → MoveToTurret
- Editor 테스트: 접근 가능한 터렛과 막힌 터렛 각각 시험
- 통과 조건: Claim 성공 시 사용 지점에 도착하고, 이동 실패 시 slot을 Release한 뒤 대체 상태로 전환

### A-10. UseTurret 상태 — 2~3시간

- 목적: 도착한 AI와 터렛의 점유 관계를 명확히 함
- C++/Blueprint: 위치 정렬과 사용 시작/종료 이벤트
- Editor 테스트: 한 명의 탑승·해제 반복
- 통과 조건: 도착 후 Use 상태가 유지되고 정상 종료 시 slot이 Release됨
- 주의: 애니메이션 세부 방식과 Motion Warping 사용 여부는 필요 시 결정한다.

### A-11. 드론 조준/공격 프로토타입 — 2~3시간

- 목적: `UseTurret → Attack`의 기능 흐름 검증
- C++/Blueprint: 현재 대상 방향 갱신과 테스트 공격 이벤트
- Editor 테스트: 이동 중인 드론을 대상으로 상태와 방향 확인
- 통과 조건: 점유한 AI만 공격 상태가 되고 대상 상실 시 공격을 멈춤
- 주의: 무기 성능, 피해량, 탄도, 명중 규칙은 현재 미정이다.

### A-12. 비점유 AI의 Prototype 대응 한 가지 — 2~3시간

- 목적: 모든 AI가 같은 터렛을 향하지 않도록 최소 분기 하나를 검증
- StateTree: 예약 실패 또는 역할 조건에서 TakeCover, Search 등 선택한 한 가지 프로토타입 행동 연결
- Editor 테스트: AI 두 명 이상과 터렛 한 개 배치
- 통과 조건: 한 명은 터렛을 사용하고 다른 AI는 이 카드에서 선택한 Prototype 대응 하나로 전환
- 주의: 선택한 대응은 최종 행동이 아니다. 어떤 병사가 엄폐·수색·무전하는지에 대한 최종 규칙은 미정이다.

### A-13. Enemy AI MVP 회귀 테스트 — 1~2시간

- 순서: Patrol → Drone Detection → 선택했다면 Suspicious/Confirm → Claim → MoveToTurret → UseTurret → Attack, 다른 AI의 Prototype 대응, 정상 종료 시 Release
- 통과 조건: 새 PIE 세션에서 전체 상태 흐름을 반복 재현함

## 8. Mission, UI, Evaluation 작업 목록

### M-01. Mission 상태 골격 — 1~2시간

- 목적: Briefing, Recon, Information Acquisition, Egress, Evaluation을 연결할 기준 마련
- C++/클래스: Mission Manager 후보와 현재 상태, 상태 변경 이벤트
- Blueprint: 상태별 디버그 텍스트
- 통과 조건: 테스트 명령으로 각 상태를 한 번씩 전환 가능

### M-02. 출격 시작 조건 — 1~2시간

- 목적: 드론 이륙과 임무 시작을 연결
- 통과 조건: 한 번만 시작되며 현재 Mission 상태가 갱신됨
- 주의: 브리핑 UI와 시작 입력은 미정이다.

### M-03. 목표 정보 획득 프로토타입 — 2~3시간

- 목적: 정찰 행동의 완료 이벤트 확보
- C++/Blueprint: 테스트 목표 Actor와 획득 이벤트
- Editor 테스트: 목표 영역 또는 현재 선택한 임시 판정 방식으로 획득
- 통과 조건: 유효 목표에서 한 번만 정보 획득 처리
- 주의: 카메라 인식, 체류 시간, 거리 등 최종 획득 규칙은 미정이다.

### M-04. 귀환 구역 — 1~2시간

- 목적: Egress와 임무 종료 연결
- C++/Blueprint: 귀환 Trigger 후보
- Editor 테스트: 정보 획득 전/후 진입 비교
- 통과 조건: 필요한 선행 상태가 있을 때만 완료로 이어짐

### M-05. 실패 이벤트 연결 — 1~2시간

- 목적: Flight Crash와 Mission 실패를 하나의 경로로 연결
- 통과 조건: 실패가 중복 기록되지 않고 Evaluation으로 이동
- 주의: 배터리·제한시간·통신 단절 실패는 채택 여부가 미정이다.

### U-01. 최소 HUD — 2~3시간

- 목적: 현재 비행/임무/AI 테스트 상태 확인
- C++/UMG: 필요한 이벤트를 Widget에 전달
- Blueprint: 상태 텍스트 중심의 프로토타입 UI
- Editor 테스트: 상태 전환 때 표시 갱신
- 통과 조건: 디버그 콘솔 없이 핵심 진행 상태를 확인 가능
- 주의: 속도, 고도, 배터리, 신호 표시 중 무엇을 최종 채택할지는 미정이다.

### U-02. Evaluation 화면 골격 — 1~2시간

- 목적: 성공/실패와 확인 가능한 임무 결과 표시
- Blueprint/UMG: 결과 패널과 재시작 경로 후보
- 통과 조건: 성공과 실패 각각에서 결과 화면 진입
- 주의: 점수 공식과 등급은 현재 미정이며 임시 텍스트로만 표시한다.

### I-01. 전체 플레이 사이클 통합 — 2~3시간

- 순서: 출격 → 접근 → 탐지 → 터렛 대응 → 회피 → 정보 획득 → 귀환 → 평가
- 통과 조건: 기능 사이 수동 디버그 명령 없이 한 사이클이 이어짐

### I-02. 반복 테스트와 결함 분리 — 1~2시간

- 목적: 우연히 한 번 성공한 흐름과 재현 가능한 데모를 구분
- 테스트: 새 실행에서 같은 사이클 반복, 실패 위치 기록
- 통과 조건: 발견된 결함을 각각 1~3시간 작업으로 다시 나눔

## 9. 이후 후보 백로그

아래 항목은 구현 확정 목록이 아니다. MVP 완료 후 필요성·데모 가치·일정을 검토한다.

- 속도·고도 표시 고도화
- 배터리
- 통신 거리와 신호 상태
- 전파 방해
- 드론 손실
- 경로 시스템
- 탐지 시스템 고도화
- 제한 시간과 점수
- 역할 분담과 협동 플레이
- 2인 Listen Server
- 점유자가 사망하거나 소멸했을 때 slot을 정리하고 다른 AI가 이어서 사용하는 터렛 승계
- FPV, Carrier/Support, Fixed Wing, Counter Drone/Interceptor 추가 기체
- EQS 기반 수색/엄폐
- Aim Offset, Motion Warping, Detour/RVO 적용

## 10. 5인 팀 작업 분리 기준

정확한 역할 분담은 현재 변경 가능하다. 기존 논의의 개발 1명·모델링/콘텐츠 인원 다수 구성을 존중하면서, 다음처럼 파일 충돌이 적은 작업 묶음으로 배정한다.

- 코드 담당 영역: Source와 핵심 Blueprint 부모 클래스
- 드론 콘텐츠 영역: 드론 메시·머티리얼·관련 자식 Blueprint
- 적 콘텐츠 영역: 병사 메시·애니메이션·관련 자식 Blueprint
- 환경 영역: 사막/산악/기지/캠프 콘텐츠와 배치
- UI·데모 콘텐츠 영역: Widget, 데모 연출, 테스트 기록

이는 직책 확정안이 아니라 Asset 소유권을 나누기 위한 예시다. 실제 담당자는 팀 상황에 맞춰 바꾸되, 한 스프린트 동안 같은 `.uasset` 또는 `.umap`을 동시에 수정하지 않는다.

레벨은 가능하면 환경, AI 배치, 조명 등 작업 영역을 분리한다. 구체적인 World Partition/Data Layer 사용 여부는 프로젝트 구조를 확인한 뒤 결정한다.

## 11. 공통 Definition of Done

기능 하나를 Done으로 옮기려면 다음을 모두 만족한다.

- 목적과 담당 클래스/에셋이 기록되어 있다.
- C++ 변경이 있다면 전체 프로젝트가 컴파일된다.
- Blueprint 참조가 끊기지 않는다.
- Editor 테스트 절차를 다른 팀원이 따라 할 수 있다.
- 정상 결과와 실패 시 확인 항목이 적혀 있다.
- 새 PIE 실행에서 다시 재현된다.
- 관련 파일만 커밋하며 변경한 Asset의 담당자가 명확하다.
- 미정인 설계를 임시 구현했다면 `Prototype/Test`로 표시되어 있다.
