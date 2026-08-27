# 작업컴 Codex/GPT 기준 컨텍스트

기준일: 2026-08-24 (Asia/Seoul)

이 문서는 메인컴 ChatGPT/Codex에서 진행하던 작업을 작업컴에서 이어가기 위한 기준 컨텍스트다. 추측해서 내용을 추가하지 않고, 사용자가 실제 진행 상황을 알려준 경우에만 상태를 갱신한다.

## 1. 전체 작업 목록

현재 진행하거나 가이드를 만들어야 할 항목은 총 6개다.

1. Git + Unreal 작업 가이드
2. 메인컴 ↔ 작업컴 Codex/GPT 작업 데이터 공유
3. Unreal 드론 프로젝트 개발 가이드
4. 정보처리산업기사 공부 계획
5. 코딩테스트 공부 계획
6. 전체 작업 정리 및 관리 가이드

우선순위:

- 최우선: Git/Unreal 협업 환경
- 최우선: Codex 작업 데이터 PC 간 공유
- 최우선: 드론 프로젝트 실제 개발
- 병행: 정보처리산업기사
- 병행: 코딩테스트
- 기반: 전체 작업 정리 시스템

## 2. 메인컴 ↔ 작업컴 Codex/GPT 데이터 공유 목적

여기서 말하는 로컬 데이터 공유는 Unreal 프로젝트 데이터 공유를 의미하지 않는다.

목적은 메인컴의 Codex/GPT에서 진행하던 개발 대화, 세션, 작업 문맥을 작업컴으로 가져가 동일한 작업을 최대한 이어서 진행하는 것이다.

두 영역을 분리한다.

### 프로젝트 데이터

Git/GitHub를 이용한다.

메인컴 → Git Push → GitHub → 작업컴 Git Pull

### Codex/GPT 작업 문맥

Codex의 로컬 세션 및 필요한 컨텍스트를 별도로 작업컴으로 전달한다.

목표 작업 흐름:

- 메인컴 작업 종료: Git Push → Codex/GPT 작업 컨텍스트 저장 → 작업컴으로 전달
- 작업컴 작업 시작: Git Pull → Codex/GPT 컨텍스트 로드 → 이전 작업 계속

인증 정보나 비밀번호 같은 민감한 파일을 그대로 복사하지 않는다.

향후 후보:

- 작업 보내기 스크립트
- 작업 받기 스크립트
- 세션 백업
- 컨텍스트 텍스트 자동 생성
- Git과 함께 실행되는 동기화 스크립트

## 3. Git + Unreal 작업 가이드 목표

Unreal Engine 프로젝트를 Git/GitHub로 안전하게 관리하고 여러 PC 또는 팀원이 작업할 수 있도록 환경을 구성한다.

- 주요 엔진: Unreal Engine
- 현재 드론 프로젝트 기준: UE 5.8.1

가이드 범위:

1. Git 설치
2. GitHub 저장소 생성
3. Unreal용 `.gitignore`
4. Git LFS 설정
5. `.uasset` / `.umap` 관리
6. `Source` / `Config` / `Content` 관리
7. `Intermediate` / `Saved` / `DerivedDataCache` 제외
8. 첫 Commit / Push
9. 다른 PC에서 Clone
10. Pull / Push 기본 사용법
11. Branch 사용법
12. Merge / Conflict 처리
13. Unreal Asset 충돌 방지
14. Level 작업 충돌 방지
15. 팀원별 작업 분리
16. Git 복구 방법
17. 잘못된 Commit 되돌리는 방법

브랜치 예시:

- `main`
- `develop`
- `feature/drone-flight`
- `feature/enemy-ai`
- `feature/ui`
- `feature/map`

Unreal 바이너리 Asset은 일반 코드처럼 Merge하기 어렵기 때문에 가능한 한 작업 영역과 담당 Asset을 분리한다.

## 4. 드론 프로젝트 정의

벤처창업아이템 경진대회를 염두에 둔 Unreal Engine 기반 드론 시뮬레이터 게임 프로젝트다. 단순한 군사 훈련 프로그램보다는 게임성을 가진 드론 운용 시뮬레이터 방향이다.

- Unreal Engine: UE 5.8.1
- 팀: 대학생 5명 규모
- 기존 논의 기준: 개발 1명, 모델링/콘텐츠 작업 인원 다수
- 정확한 역할 분담: 현재 미정이며 변경 가능

J3C는 실제 계약된 발주처가 아니다. 프로젝트 콘셉트상의 가상 외주 발주처로만 사용하며 실제 협력, 계약, 지원, 공식 관계가 있다고 표현하지 않는다.

## 5. 드론 프로젝트 핵심 방향

- 드론 운용
- 정찰
- 침투
- 탐지
- 적 AI 반응
- 임무
- 귀환
- 평가

예상 게임 루프:

Briefing → Recon → Detect → Information acquisition → Enemy response → Mission → Egress → Evaluation

아직 모든 시스템이 확정된 것은 아니다.

## 6. 드론 기본 시스템 개발 순서

처음부터 모든 기능을 구현하지 않고 MVP부터 만든다.

### Phase 1

드론 1대를 정상적으로 조작 가능하게 한다.

- Spawn
- Take Off
- Forward / Backward
- Left / Right
- Yaw
- Altitude
- Camera
- Landing
- Crash 또는 실패 처리

그 다음 후보:

- 속도
- 고도
- 배터리
- 통신 거리
- 신호 상태
- 재밍

## 7. 드론 종류

초기에는 정찰용 멀티콥터 1종부터 구현한다.

향후 후보:

- Scout
- FPV
- Carrier / Support
- Fixed Wing
- Counter Drone / Interceptor

실제 군용 드론을 정확히 1:1 구현하는 방향은 아니다. 가상의 드론 이름과 디자인을 사용하는 방안도 고려한다.

## 8. 적 AI

적 AI는 프로젝트의 중요한 요소다. 단순히 플레이어를 보고 공격하는 수준이 아니라 상황에 따라 행동하도록 만든다.

핵심 예시:

Patrol → Drone Detection → Suspicious → Confirm → Response

대응 행동 예시:

- 엄폐
- MG 터렛으로 이동
- 무전
- 공격
- 드론 수색
- 경계 위치 복귀

특히 구현하고 싶은 행동은 드론을 발견한 병사가 비어 있는 MG 터렛으로 달려가 점유하고 드론을 공격하는 것이다. 다른 병사는 상황에 따라 엄폐하거나 별도의 대응 행동을 한다.

## 9. 적 AI 기술 후보

Unreal 기능 후보:

- AI Perception
- StateTree
- EQS
- NavMesh
- Smart Objects
- Gameplay Interactions
- Anim Blueprint
- Aim Offset
- Motion Warping
- Detour / RVO

우선순위:

AI Perception → StateTree → NavMesh → Smart Object → Turret Interaction → Search / Cover / Return

처음부터 모든 기술을 사용하지 않고 기능에 필요한 것만 단계적으로 추가한다.

## 10. 적 AI 상태 예시

- Idle
- Patrol
- Guard
- Suspicious
- DroneDetected
- MoveToTurret
- UseTurret
- Attack
- TakeCover
- Search
- Return
- Death

Smart Object를 사용하는 경우 터렛은 한 명만 점유할 수 있도록 Reservation / Occupancy 개념을 사용한다. 점유자가 사라지거나 사망하면 다른 AI가 이어서 사용할 수 있는 구조도 향후 고려한다.

## 11. 드론 프로젝트 맵

논의된 환경:

- 사막
- 산악 지역
- 군사 기지
- 캠프

영상/데모에서 생각한 흐름:

넓은 지형 Establishing Shot → 기지 → 드론 이륙 → 저고도 비행 → 능선을 따라 접근 → FPV/정찰 카메라 → 경계병 발견 → 병사가 MG 터렛으로 이동 → 다른 병사는 엄폐 → 드론 회피 → 임무 진행

## 12. 드론 프로젝트 데모 목표

거대한 게임을 먼저 만드는 것이 목표가 아니다. 짧아도 하나의 플레이 사이클이 완성되어야 한다.

최소 데모 예시:

드론 출격 → 기지 접근 → 적 탐지 → 적이 드론을 발견 → 병사가 MG에 탑승 → 드론 회피 → 목표 정보 획득 → 귀환 → 평가

이 흐름을 먼저 완성한다.

## 13. 추가 고려 요소

다음은 확정되지 않은 후보이며 구현된 기능처럼 표현하지 않는다.

- 배터리
- 통신거리
- 전파 방해
- 드론 손실
- 경로
- 탐지 시스템
- 제한시간
- 점수
- 임무 평가
- 역할 분담
- 협동 플레이
- 2인 Listen Server

## 14. Unreal 관련 사용자 작업 성향

사용자는 Unreal Engine 개발을 취업 방향 중 하나로 보고 있다. 코드 설명은 가능하면 다음 순서를 따른다.

1. 왜 필요한지
2. Unreal에서 어느 클래스가 담당하는지
3. 헤더에 무엇을 추가하는지
4. CPP에 무엇을 추가하는지
5. Blueprint에서 무엇을 설정하는지
6. Editor에서 테스트 방법
7. 정상 결과
8. 문제가 생겼을 때 확인할 항목

한 번에 너무 많은 시스템을 만들지 않는다. 기능 단위로 완성하고 테스트한 후 다음 단계로 넘어간다.

## 15. 기존 Unreal 경험

사용자는 이전 Unreal 프로젝트에서 다음 시스템을 직접 다뤄봤다.

- C++ Character
- Enhanced Input
- Camera / SpringArm
- Weapon
- Line Trace
- HP
- Damage
- Animation Montage
- Monster AI
- AI State
- UMG
- Item
- GameMode
- Timer
- DataTable
- Collision / Overlap
- Live Coding

Visual Studio 2022를 사용해 왔다. Unreal 기초 개념을 매번 처음부터 장황하게 설명할 필요는 없지만 새로운 시스템은 구현 구조를 명확하게 설명한다.

## 16. 코딩테스트 공부

취업 준비와 함께 C++ 중심으로 진행한다.

초기:

- 입출력
- 조건문
- 반복문
- 배열
- 문자열
- 함수

그 다음:

- vector
- sort
- stack
- queue
- deque
- map
- unordered_map
- set
- priority_queue

그 다음:

- DFS
- BFS
- 재귀
- 그래프
- 이분탐색
- Greedy
- DP

문제풀이 방식:

문제 확인 → 직접 풀이 → 실패 → 실패 이유 확인 → 정답 아이디어 공부 → 다시 직접 구현 → 며칠 뒤 재풀이

하루 1~2문제를 기본으로 하되 Unreal 프로젝트 시간을 지나치게 뺏지 않도록 한다.

## 17. 정보처리산업기사 공부

개념 → 문제 → 오답 순서로 학습한다.

오답 원인 분류:

- 개념 부족
- 암기 부족
- 개념 혼동
- 계산 실수

시험 날짜가 정해지면 D-Day 기준으로 세부 공부 계획을 다시 작성한다.

## 18. 전체 작업 관리 방식

Inbox → Todo → Doing → Done

프로젝트 구분 예시:

- Drone
- Unreal
- Git
- Codex Sync
- 정보처리산업기사
- Coding Test
- Portfolio

작업 하나의 크기는 가능하면 1~3시간 안에 완료할 수 있도록 쪼갠다.

잘못된 작업: `적 AI 만들기`

좋은 작업 예시:

- AI Perception Component 추가
- Sight 설정
- Drone Actor 감지 테스트
- Debug Sight 확인
- StateTree Alert State 생성
- MG Smart Object 배치
- AI MG 이동 테스트
- MG 점유 테스트
- 공격 테스트

## 19. 프로젝트 작업 우선순위

1. 작업 정리 환경 구축
2. Git + Unreal 환경 구축
3. Codex/GPT PC 간 작업 공유 환경 구축
4. Drone 프로젝트 기본 구조
5. PFN-06 Spawn/Input 기준선 검증
6. Drone Flight MVP
7. 최소 Mission Shell
8. Enemy AI·MG
9. 통합 Greybox와 평가
10. 에셋 교체 준비와 포트폴리오 정리

공부는 별도로 병행한다.

## 20. 답변 시 주의사항

사용자가 확정하지 않은 내용을 확정된 것으로 만들지 않는다.

다음 사항을 임의로 정하지 않는다.

- 군/국가 설정
- 적군 국적
- 실제 J3C 협력 관계
- 실제 발주 관계
- 최종 드론 종류
- 최종 게임 규칙
- 최종 멀티플레이 방식
- 세부 입력 방식
- 최종 물리 시스템

모르는 것은 현재 미정이라고 구분한다. 기술적으로 불확실한 내용은 확인 없이 있는 기능처럼 말하지 않는다. 정확성을 우선한다.

## 21. 다음 작업

### 완료: PFN-06 Camera/Input, HUD-01 Telemetry, HUD-02 Flight HUD, TUT-01 Course, TUT-02 Ring Gate와 TUT-03 Segment/Lap 기록

사용자 승인안의 Camera/Input과 Telemetry/HUD 기준선, TUT-01 Training Map·비충돌 Spline을 완료했다. TUT-02에서는 실제 `BP_DroneTrainingGate` 네 개, 비충돌 Ring Visual과 별도 Pawn Overlap Trigger, Course의 명시적 Gate 배열과 순서·정방향·중복 통과 판정을 구현했다. TUT-03에서는 Course 소유 `UDroneTrainingLapRecorderComponent`가 정상 Gate Event와 Telemetry 10Hz 위치 표본을 이용해 Segment/Lap 시간, 3차원 누적 이동 거리와 평균 속도 원본을 기록하도록 구현했다. Unreal 기준은 `main=origin/main=551e287`이며 전체 `Drone.` 자동화 14/14, Tutorial 6/6, Blueprint 0 errors·0 warnings·0 load failures를 통과했다.

### 1순위: Tutorial Vertical Slice와 기능 우선 Greybox

`TUT-04 비교·결과 UI → Flight 상태 → Operator↔Drone → NPC·Mission UI Story Shell → AI/MG/Jamming → 에셋 적용` 순서로 진행한다. TUT-03에서 Lap 시작·완료, Segment/Lap Timing, 10Hz 위치 표본 기반 이동 거리와 평균 속도 원본까지 구현했다. 이전 성공 평균·Best 비교와 화면 표시는 아직 구현하지 않았으며 TUT-04 범위다. 상세 기준은 `docs/DRONE_TUTORIAL_STORY_PLAN.md`를 따른다.

### 병행: PC 간 공유 검증

`drone`과 `md`의 첫 Push는 완료했다. 다른 PC Clone/LFS/UE 5.8.1 실행과 문서 Clone/Pull을 확인하면 PC 간 전체 공유 흐름을 닫는다.

## 22. 이후 사용자가 확정한 사항

- 현재 Drone 프로젝트에서는 Android를 사용하지 않는다.
- 이에 따라 Android 전용 기능은 현재 개발 범위에 포함하지 않는다.
- 제공 에셋 위치는 현재 `C:\에셋`이다.

## 23. 2026-08-19 실제 진행 상태 (역사적 스냅샷)

- Prototype 시험 전용 입력 계약을 기록했다. 현재 키는 `W/S/A/D`, `Space/Left Ctrl`, `Q/E`, `Mouse XY`다. 이는 PFN 실행을 위한 임시값이며 최종 조작 방식의 승인이 아니다.
- PFN-01~05를 완료했다. Input Action 4개, `IMC_DronePrototype`, `BP_DronePrototypePawn`, `BP_DronePrototypeGameMode`, `Lvl_DronePrototype`을 생성·연결했다.
- BP Pawn에는 네 Input Action과 IMC, Engine Cube Placeholder를 연결했다. BP GameMode의 Default Pawn과 Prototype Map의 GameMode Override도 연결했다.
- 자산 생성 직후 검증과 수정된 별도 프로세스 재로드 검증에서 IA 타입, 9개 Mapping, BP 부모·참조, Map 설정과 Greybox Actor 구성을 확인했다. Map Check는 0 errors, 0 warnings였다.
- GUI PIE에서 `IMC_DronePrototype` 한 개와 Move·Altitude·Yaw·Look Callback 계열의 실제 동작을 부분 확인했다. 첫 실행은 `S`와 복합·중복 조건을 끝내지 못했고 두 번째 실행도 일부 확인 뒤 중단했다.
- PFN-06 자동화는 3/3 Pass다. 수동 화면 확인 1회가 남았으므로 PFN-06과 Flight MVP는 아직 완료가 아니다.
- 최종 키·Look 감도·Mouse Y 반전 기본값·최종 Mesh·최종 물리·멀티플레이 방식은 계속 미정이다.

## 24. 2026-08-21 GitHub 저장소 역할과 실제 상태 (역사적 스냅샷)

- 실제 Unreal 프로젝트는 `https://github.com/gyeonliz/drone` 저장소로 관리한다.
- 현재 기본 작업 루트는 `D:\JGY\project`, Unreal 프로젝트는 `D:\JGY\project\drone`, 문서 저장소는 `D:\JGY\project\md`다.
- Unreal 저장소의 로컬 `main`은 HUD-01 Commit `08e876a`이고 `origin/main`은 별도 Push 전 `fb891fb`다. `2c38ebf`는 PFN-06 마감, `91498b7`은 초기 Commit으로 보존하는 역사 기록이다.
- 기준선 확인 당시 Unreal 프로젝트 작업 트리는 깨끗했고 `.uasset`·`.umap`은 Git LFS 추적 대상이다.
- Markdown 작업 문맥·계획·가이드·안전한 보조 도구는 `https://github.com/gyeonliz/md.git` 저장소로 공유한다.
- 문서 저장소의 첫 Stage·Commit·Push를 완료했으며 로컬 `main`과 `origin/main`은 `9e81de0`에서 일치한다. `MD-02`, `MD-03`은 Done이다.
- `drone`과 `md`는 서로 다른 저장소다. Unreal Content/Source를 `md`에 복제하거나 Codex 인증·원시 세션 파일을 어느 저장소에도 넣지 않는다.
- 다른 PC에서 `drone` Clone/LFS/UE 5.8.1 실행과 `md` Clone/Pull을 모두 확인하기 전까지 PC 간 전체 공유 흐름은 완료로 처리하지 않는다.

## 25. 현재 작업 기준

- 실제 Git·코드·설정·실행 로그를 최우선 근거로 삼고, 상태는 `WORKBOARD.md`, 현재 실행 순서는 `docs/DRONE_TUTORIAL_STORY_PLAN.md`를 따른다. 기존 Preasset 계획은 카드 번호와 에셋 교체 경계 참고용으로 유지한다.
- 새 생산 코드는 `Source/Drone`, 새 자산은 `/Game/Drone` 아래에 둔다.
- ThirdPerson·Combat·Platforming·SideScrolling은 참고용 Legacy로 동결한다. 신규 상속·참조를 만들지 않고 Vertical Slice 전에는 삭제하지 않는다.
- Prototype IMC의 등록·제거 책임은 Pawn 한 곳에만 둔다. PlayerController나 Level Blueprint에 중복 등록하지 않는다.
- C++는 상태·계산·수명주기, Blueprint는 자산 연결·Greybox 조정과 UI 표시 외형을 담당한다. Collision Root와 Visual Mesh를 분리한다.
- Tutorial Course의 안내선은 경로 표시만 담당한다. Collision·Overlap·Physics·Navigation에 영향을 주지 않으며 Gate 판정 책임을 섞지 않는다.
- PFN-06 v1 조작은 Actor-relative 수평 이동, World Up 고도, Q/E와 Mouse X Actor Yaw, Mouse Y CameraBoom Pitch, Gamepad Left Stick 이동·Trigger 고도·Right Stick Yaw/Pitch로 확정했다. Keyboard·Mouse 시험 감도는 수동 Pass했으며 실제 Gamepad 체감과 최종 물리 조정은 이후 별도 카드로 남긴다.
- Standalone 싱글플레이만 현재 검증 범위로 두며 네트워크·Android는 제외한다. 제공 에셋은 검증된 FPV 외형·Loop 최소 이식만 허용하고 전면 교체는 제외한다.
- C++ 변경과 전체 빌드 전에는 열려 있는 Unreal Editor를 저장하고 종료한다.
- Drone 작업을 진행할 때 `WORKBOARD.md`에 현재 단계·진행 정도·지금 작업·완료 근거·다음 작업을 갱신하고, 실제 변경과 검증 이력은 `docs/DRONE_WORKLOG.md`에 같은 작업에서 추가한다.
- Codex가 새로 만드는 Git 기능 Commit과 Merge Commit 메시지는 사용자가 GitHub Desktop에서 읽기 쉽도록 한글로 작성한다. 기존 영문 Commit 이력은 바꾸지 않는다.

## 26. 2026-08-21 Tutorial·Story 방향 확정

- Tutorial은 비충돌 Spline 안내선과 순서형 원형 Gate를 따라 비행하는 훈련 모드다.
- 상시 HUD에는 속도·고도·수직 속도·Heading을 표시한다.
- Gate마다 Segment Time과 실제 이동 거리 기준 평균 속도를 계산하고 이전 성공 기록 평균·Best 대비 ± 차이를 표시한다.
- Story는 Operator Character, NPC 대화, Mission 안내 UI, Operator↔Drone 화면/Possess 전환을 포함한다.
- Jamming은 신호 경고 → HUD Noise → 조작/통신 저하의 재현 가능한 단계형 규칙으로 만든다.
- 제공 Drone 에셋은 기능 부모로 상속하지 않고 `/Game/Drone` 아래 Integration Blueprint에서 Visual만 교체한다.

## 27. 2026-08-24 HUD-02·TUT-01·TUT-02 완료와 현재 기준

- 이번 확인 PC의 실제 Unreal 저장소는 `C:\URproject\drone`이다. 뒤처진 `C:\project\Drone` 복제본은 현재 작업에 사용하지 않는다.
- Unreal 저장소의 로컬 `main`과 `origin/main`은 TUT-02 Commit `800a7baaf8247bf0a3ee7bccc2272e12d0098f2b`으로 일치한다. `5a9a2fa`는 TUT-01, `9f91bb6`은 WBP/BP 연결 보강, `410c940`은 native HUD 기준선으로 보존한다.
- C++ `UDroneFlightHUDWidget`과 PlayerController가 현재 Possess Drone의 Telemetry Event·Widget 생성·Delegate 정리를 담당하고, 실제 `WBP_DroneFlightHUD`가 `SPD`, `ALT`, `V/S`, `HDG`의 배치·폰트·색을 담당한다. BP Controller가 WBP를 선택하고 BP GameMode가 BP Controller를 선택한다. Tick·Property Binding·매 프레임 Pawn 검색은 사용하지 않는다.
- TUT-01은 `ADroneTrainingCourse`, `BP_DroneTrainingCourse`, `Lvl_DroneTraining`, `M_DroneTrainingGuide`와 Tutorial 자동화 테스트 3개로 구성한다. Course가 편집 가능한 Spline과 런타임 표시용 Spline Mesh를 소유하고, Material은 Opaque·Unlit·Emissive와 Spline Mesh 사용 설정으로 Cyan 안내선을 표시한다.
- TUT-02는 `ADroneTrainingGate`, `UDroneTrainingGateSequenceComponent`, 실제 `BP_DroneTrainingGate` 네 개와 갱신한 Training Map으로 구성한다. Ring Visual은 충돌하지 않고 별도 Trigger만 Pawn Overlap을 받으며, Sequence Component가 현재 순서·정방향·중복 통과와 Current/Completed/Inactive 상태를 판정한다.
- TUT-02 `DroneEditor Win64 Development` 빌드는 성공했다. Gate Sequence 1/1과 실제 BP PIE Smoke 1/1, 전체 `Drone.Tutorial` 4/4, 전체 `Drone.` 11/11이 warning·failure 없이 통과했다. `CompileAllBlueprints`도 0 errors, 0 warnings, 0 blueprints failed to load다.
- Standalone에서 실제 BP Controller/Pawn/WBP HUD, Cyan Course 안내선과 Current/Inactive Gate 표시를 확인했다. 신규 BP Gate와 갱신 Map 두 Asset은 Git LFS로 Push했다.
- 다음 활성 카드는 `TUT-03` Segment/Lap 기록이다. Gate·순서·방향은 구현됐지만 Lap·Timing·거리·평균 속도·기록 UI는 아직 구현되지 않았다. 배터리·신호·Jamming 표시와 최종 HUD 디자인도 구현 완료로 간주하지 않는다.
- Android는 개발 범위에서 제외하고 구매 소스는 TUT-03의 선행 조건으로 두지 않는다.
- 문서 저장소는 이번 갱신 직전 로컬 `main`과 `origin/main`이 `e6395f1`에서 일치했으며, 이 상태·계획 갱신도 Commit·Push해 PC 간 공유 기준에 반영한다.

## 28. 2026-08-25 TUT-03·현재 에셋 재검증

- 현재 Unreal 기준 Commit은 로컬·원격이 일치하는 `551e287e8a5de7fa33f28d1911f8a7a957bd66fa`다. TUT-03 Segment/Lap 원본 기록을 완료했고 다음 기능 카드는 TUT-04 비교·결과 UI다.
- 현재 제공 에셋 루트는 `C:\에셋`이다. 14개 공급사 해제본 기준선은 10,499개·35,677,612,290 bytes이고, `_Staging`·내부 FBX 해제본·생성 캐시를 포함한 현재 전체는 10,928개·36,360,181,427 bytes다.
- 현재 C 드라이브에는 최초 감사의 최상위 ZIP 14개가 없으므로 과거 `Missing 0 / Extra 0 / SizeMismatch 0` 결과는 역사 기록으로만 취급한다. 남아 있는 내부 `FBX.zip`의 55개 FBX는 현재 해제본과 SHA-256 불일치 0이다.
- 해당 루트에서 구매 영수증·사용 라이선스 증빙 파일은 확인되지 않았다. 제공 소스가 있어도 전체 팩을 프로젝트에 흡수하지 않고 기능·Greybox를 우선하며 검증된 선택 자산만 Integration 경계로 이식한다.
- 실제 Drone 프로젝트에는 `/Game/Drone/ThirdParty` 선택 자산 12개·21,753,071 bytes와 `/Game/Drone/Integrations/DronePackFPV/BP_DroneFPVIntegration` 1개만 있다. 스테이징 선택 자산·현재 Integration 감사에서 외부 Game Root·ThirdPerson·Variant 금지 의존성은 0이고 13개 모두 Git LFS 대상이다.
- `C:\에셋\DronePack_Project\Config\DefaultEngine.ini`의 Android File Server에는 비어 있지 않은 토큰이 있으므로 Config를 이식하거나 Commit하지 않는다. 값은 기록하지 않으며 실제 Drone 프로젝트는 Plugin·네트워크 꺼짐, 빈 토큰을 유지한다.
- 이번 재검증에서 `Drone.Integration.FPVAsset` 1/1, Blueprint Compile 0/0/0, LFS fsck를 통과했다. 전체 `Drone.` 14/14는 현재 Commit에서 TUT-03 완료 때 통과한 기준선이며 이번에는 미재실행이다.
- 기존 Standalone 초기 렌더는 통과했지만 실제 스피커 Loop 단일 재생과 종료 정지는 여전히 사람이 확인하지 않았다. `AST-01`은 Doing으로 유지한다.

## 29. 2026-08-26 자산 권리 확인과 NavigationArrows 1차 이식

- 사용자는 제공 에셋이 지원과정을 통해 구매·지급된 것이며 현재 프로젝트에서 사용하는 데 문제가 없다고 확인했다. 이 사용자 확인으로 프로젝트 사용 권리는 이식 차단 조건이 아니다.
- `C:\에셋`에서 별도 `LICENSE`, `EULA`, 영수증 파일을 찾지 못한 사실은 로컬 증빙 보관 상태다. 법률 검토 완료나 판매 페이지 조건 확인 완료를 뜻하지 않는다.
- `PBR Sting`의 `isAiForbidden: true`는 해당 팩을 생성형 도구에 넣지 않는 별도 제한으로 유지한다. 다른 팩이나 일반 Unreal 사용에 임의로 확대 적용하지 않는다.
- `AST-02A NavigationArrows`는 원본 11개·1,364,087 bytes를 UE 5.8 전용 스테이징에서 감사한 뒤 기능 최소 폐쇄 집합 6개만 `/Game/Drone/ThirdParty/NavigationArrows`로 이동·재저장했다. UE 5.8 재저장 후 실제 프로젝트 크기는 1,098,730 bytes다.
- 이식한 6개는 `NavigationArrow` Widget Blueprint 1개, Texture2D 2개, UserDefinedStruct 3개다. Demo Map·BuiltData·Example Actor·Example Mesh·미사용 `TransparentCircle`은 제외했다.
- 실제 Drone 프로젝트에서 6개 로드, Generated Class, 의존성 폐쇄와 제외 목록을 검사했다. 외부 `/Game` 의존성 0, 로드 실패 0, 전용 자동화 1/1, 전체 `Drone.` 15/15, Blueprint Compile 0 errors·0 Blueprint warnings·0 load failures, LFS 속성과 `git lfs fsck`를 통과했다.
- 자산과 검증 코드는 Commit `5a052c8bab2eb0dd8bc9ab16cfc7b3784e8e4cd7`로 기능 Branch에 Push한 뒤 Merge Commit `fb1d7ad2c23d6bf3b1c854ca7c1c0cddba2062ef`로 `origin/main`에도 반영했다. 훈련 Map/HUD의 실제 Host/Wrapper 화면 연결은 아직 하지 않았다.
- 다음 자산 단계는 프로젝트 소유 Host/Wrapper가 현재 Gate 하나를 이 Widget의 `TargetComponent` 또는 `TargetWorldLocation`에 전달하는 것이다. 기존 Course 안내선과 Gate Ring을 교체하지 않으며, `TUT-04`는 별도의 다음 기능 카드로 유지한다.

## 30. 2026-08-26 09:17 현재 작업 PC 동기화

- 현재 실제 작업 경로는 Unreal `D:\JGY\project\drone`, 문서 `D:\JGY\project\md`다.
- Drone은 로컬 `main=origin/main=551e287`, 작업 트리 Clean이다. NavigationArrows Commit `5a052c8`은 원격 기능 Branch에만 있고 main 미병합이다.
- 문서는 최신화 직전 `main=origin/main=466609d`, 작업 트리 Clean이었다. 이 최신화 변경의 Commit·Push는 사용자가 직접 수행한다.
- 현재 PC의 제공 에셋 루트는 `D:\JGY\project\Unreal_260821`이다. ZIP 14개·공급사 폴더 14개와 `_Staging`이 있으며 `C:\에셋`은 이 PC에 없다. C 드라이브 감사 결과는 다른 PC의 역사 기록으로 유지한다.
- UE 5.8.1 Editor PID 9884가 D 드라이브 프로젝트로 실행 중이다. MCP 서버 시작·23 Toolset 등록 로그와 `127.0.0.1:8000/mcp` 응답을 확인했지만 현재 문서 루트 Codex 작업의 네이티브 Tool 노출은 확인하지 않았으므로 `UE-MCP-02`는 Todo다.
- 다음 기능 카드는 `TUT-04 이전 기록 비교·Best·결과 UI`다. `AST-01` 청감과 TUT-03 실제 한 Lap 수동 확인은 계속 미확인이다.

## 31. 2026-08-26 UE 5.8 Dataflow·Chaos 물리 환경 방향

- 사용자는 일부 지점을 고정해 늘어뜨리는 그물 물리와 선택형 맵 파괴를 프로젝트에 포함하려고 한다.
- 그물은 `Chaos Cloth + Dataflow`, 파괴물은 `Chaos Destruction + Geometry Collection + Dataflow`로 분리한다.
- Cloth 변형과 파괴 연출은 물리 표현이며, 포획·Damage·Mission 성공/실패의 단일 기준은 프로젝트 C++ 상태가 소유한다.
- 그물 고정부는 Max Distance 0 또는 Kinematic Selection, 동적 영역은 Weight Map으로 처짐 범위를 조정한다.
- 맵 전체를 파괴 가능하게 하지 않고 벽·출입구·Jammer 설비 같은 명시적 대상만 Geometry Collection으로 만든다.
- 현재 설치본에는 필요한 플러그인이 있지만 `Drone.uproject`에는 아직 명시적으로 활성화하지 않았다. Deprecated Cloth Editor는 사용하지 않는다.
- 다음 기능 우선순위는 TUT-04로 유지하며, Dataflow/Chaos는 별도 Sandbox Branch와 Flight Collision/Damage 기준 뒤 구현한다.
- 상세 설계와 검증 게이트는 `docs/DRONE_CHAOS_DATAFLOW_PLAN.md`를 따른다.

## 32. 2026-08-26 09:48 별도 `droner` 복제본 발견

- 기준 작업 루트는 계속 `D:\JGY\project\drone`이다.
- 현재 열린 UE Editor PID 10960은 `D:\JGY\project\droner\Drone.uproject`를 사용하며 MCP Port 8000도 이 프로세스가 소유한다.
- `droner`는 같은 원격과 `main=origin/main=551e287`을 사용하지만 `Content/Asset` 아래에 공급사 원본·스테이징 10,928개·36,360,181,427 bytes가 Untracked로 들어 있다.
- `droner/Content/Asset` 전체를 Stage·Commit·Push하지 않는다. 기준 프로젝트로 필요한 에셋만 UE 5.8 스테이징·감사 후 `/Game/Drone/ThirdParty`로 선별 이식한다.
- 기준 `drone`과 `droner` 모두 Editor가 만든 `Config/DefaultEditor.ini` 변경이 있다. 사용자 변경으로 보존하고 임의로 되돌리지 않는다.
- C++·Plugin·Dataflow Asset 작업 전에는 `droner` Editor를 정상 종료하고 기준 `drone`을 명시적으로 연다.

## 33. 2026-08-26 13:11 중단 작업 재개와 NavigationArrows main 반영

- 이번 확인 PC의 실제 경로는 Unreal `C:\URproject\drone`, 문서 `C:\Users\jkw11\Documents\Codex\2026-08-19\codex-gpt-chatgpt-codex-1-6`다.
- 기존 원격 `main`의 `5540c6b` 작업을 보존하고 NavigationArrows 기능 Commit `5a052c8`을 Merge Commit `fb1d7ad`로 병합해 `origin/main`에 Push했다.
- 병합된 main에서 `DroneEditor Win64 Development` Build, NavigationArrows 1/1, 전체 `Drone.` 15/15, Blueprint Compile 0/0/0과 `git lfs fsck`를 다시 통과했다.
- 로컬 `main=origin/main=fb1d7ad`이고 Drone 작업 트리는 Clean이다.
- 이 완료는 자산 인수·공유 완료를 뜻한다. NavigationArrows를 실제 Training HUD에 표시하는 프로젝트 소유 Host/Wrapper와 PIE/Standalone 시각 검증은 아직 남아 있다.
- 같은 기준선의 `Lvl_DroneTraining` PIE에서 한글 Flight HUD·구간 기록 패널·현재 Gate·세분화 코스 선의 초기 렌더는 확인했다. Gate 0→3 한 Lap 뒤 구간 숫자 갱신과 NavigationArrows Host/Wrapper는 아직 확인·구현하지 않았다.
- 맵 이식은 DronePack의 정리 `Map_Demo` 1개만 기술 검증·main 반영까지 완료했다. Battlefield·MilitaryCamp·MilitaryBase 환경 맵은 실제 Drone 저장소에 아직 없으며 `AST-03A`로 계속 분리한다.

## 34. 2026-08-26 맵 중앙화와 당시 템플릿 콘텐츠 정리

- 위 33절은 `fb1d7ad` 시점의 역사 상태다. 이 절은 `2cc5d79` 시점의 역사 상태이며 35절에서 삭제 범위를 교정했다.
- 실제 RabbitHole 프로젝트 `C:\project\Fractured\GoDownTheRabbitHole.uproject`를 확인했다. 프로젝트 소유 맵을 `Content/Maps`에 모으고 역할별 Blueprint 폴더와 공급사 폴더를 분리하는 방식을 참고했다.
- Drone 프로젝트 소유 맵은 `/Game/Drone/Maps`로 중앙화했다: `Lvl_DroneTraining`, `Lvl_DronePrototype`, `Lvl_DronePackShowcase`.
- 기존 공급사 정리 맵 `Map_Demo`는 `Lvl_DronePackShowcase`로 이름과 위치를 바꿨다. 공급사 Mesh·Material 등 의존 자산은 `/Game/Drone/ThirdParty/DronePack`에 유지한다.
- 당시 미사용으로 판단한 `/Game/ThirdPerson`, `/Game/Variant_Combat`, `/Game/Variant_Platforming`, `/Game/Variant_SideScrolling` 전체를 제거했다. 사용자가 뜻한 대상은 기본 Map이었으므로 이 범위는 35절에서 바로잡았다.
- 시작 맵·Editor 시작 맵은 `/Game/Drone/Maps/Lvl_DroneTraining`, 전역 GameMode는 프로젝트 소유 `BP_DronePrototypeGameMode`다.
- C++ `DroneCharacter`, 기존 GameMode/Controller, Variant Source는 별도 Source/Build.cs 감사 없이 지우지 않았다.
- 중앙 맵과 BuiltData 로드, 이전 경로·템플릿 루트 부재, Build, Blueprint 0/0/0, 전체 `Drone.` 15/15, LFS, diff 검증을 통과했다.
- 기능 Commit `1c8f391`을 Merge Commit `2cc5d79`로 main에 병합·Push했다. 삭제 내용은 Git 이력에서 복구할 수 있다.
- Battlefield·MilitaryCamp·MilitaryBase 환경 맵은 아직 미이식이다. 현재 남은 수동 확인은 `Lvl_DronePackShowcase`의 시각 검토와 `Lvl_DroneTraining` 한 Lap 비행이다.
- 상세 폴더 규칙과 현재 트리는 `docs/DRONE_CONTENT_FOLDER_GUIDE.md`를 따른다.

## 35. 2026-08-26 삭제 범위 교정과 환경 맵 이식

- Unreal 생성 기본 Map 4개만 삭제 대상으로 확정했다. ThirdPerson·Variant 비맵 자산 62개는 Commit `909f6a3`에서 복구했다.
- 삭제 상태인 Map은 `Lvl_ThirdPerson`, `Lvl_Combat`, `Lvl_Platforming`, `Lvl_SideScrolling`과 각 Map 전용 ExternalActors/ExternalObjects다.
- `C:\에셋` 원본 3팩은 수정하지 않고 별도 UE 5.8 스테이징에서 Map 10개와 3,334개·18.76 GiB를 감사했다.
- 중앙 Map `/Game/Drone/Maps/Lvl_Battlefield`, `Lvl_MilitaryCamp`, `Lvl_MilitaryBase`와 정확한 의존성 2,723개·16.96 GiB를 Commit `f8c8fb2`로 이식했다.
- 대형 공급사 패키지의 내부 경로는 일괄 재작성하지 않고 `/Game/Battlefield`, `/Game/FC_MilitaryCamp`, `/Game/MillitaryBase`를 유지했다. 프로젝트에서 선택한 Map 사본만 중앙 경로에 둔다.
- 세 Map의 공급사 GameMode Override는 제거했다. 환경별 누락 Game 의존성 0, 허용 외 경로 0, World Load 성공을 확인했다.
- Build, Blueprint 0/0/0, 전체 Drone 15/15, Map Check, LFS Pointer 2,723개와 fsck를 통과했다. Battlefield에는 공급 Blueprint의 선택적 NULL StaticMesh Map Check 메시지 14건이 남고 Camp/Base는 0/0이다.
- 환경 맵의 기술 이식은 완료지만 실제 Editor 화면 시각 검토와 데모 주력 Map 선택은 아직 미정이다.

## 36. 2026-08-27 NPC·Smart Object 방향 추가

- 적 NPC는 순찰하다가 Drone을 발견하면 대응한다.
- 개인 화기 사격은 Rifle과 Shotgun 두 종류까지 구분해 준비한다. 최종 수치·입력·피해·Animation은 현재 미정이다.
- MG Turret은 Smart Object Slot 예약으로 한 명만 점유하도록 한다.
- 기지의 아군 NPC도 Smart Object를 이용해 Friendly Base Patrol 또는 Ambient 지점을 돌아다니는 방향으로 준비한다.
- Friendly/Hostile은 기술적인 역할 구분이며 국가·군·세계관 설정을 확정하지 않는다.
- Smart Object는 NPC Spawn이 아니라 이동 대상·생활 지점·MG 점유를 관리한다. NPC 직접 배치와 반복 Spawn은 별도 Character/Spawn Point가 담당한다.
- `c3e6d38` main의 C++ 기반은 Profile·Tag·Character·Controller·Spawn·Reservation·Drone Sight까지다. 그 위 `AI-SO-01` 작업에서 Smart Object Definition 6종과 대응 Station Blueprint 6종을 실제 구성하고 Slot·Activity·Definition·MG Mesh 연결을 검증했다.
- 각 Definition의 Gameplay Interaction Behavior에 연결할 StateTree는 현재 비어 있다. 실제 NPC Blueprint·순찰·아군 이동·Rifle/Shotgun 사격·MG Animation은 아직 구현 완료로 표현하지 않는다.
- 상세 구현·Editor 사용 순서는 `docs/DRONE_SMART_OBJECT_NPC_GUIDE.md`를 기준으로 한다.
