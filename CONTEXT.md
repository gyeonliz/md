# 작업컴 Codex/GPT 기준 컨텍스트

기준일: 2026-08-23 (Asia/Seoul)

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

### 완료: PFN-06 Camera/Input, HUD-01 Telemetry, HUD-02 Flight HUD와 TUT-01 Training Course

사용자 승인안의 Camera/Input 기준선을 완료했다. 공용 Telemetry Component의 기본 10Hz Snapshot Event와 이를 표시하는 C++ HUD 기능·실제 WBP 외형을 구현했다. 이어서 TUT-01의 별도 Training Map, 편집 가능한 비충돌 Spline Course, 실제 BP Course와 Cyan 안내 Material을 구현했다. 현재 전체 `Drone.` 자동화 10/10, Blueprint 0 errors·0 warnings·0 load failures, Standalone 실제 BP Controller/Pawn/WBP와 안내선 표시까지 통과했다.

### 1순위: Tutorial Vertical Slice와 기능 우선 Greybox

`TUT-02 순서형 Ring Gate·정방향 판정 → Lap/Segment 기록 → Flight 상태 → Operator↔Drone → NPC·Mission UI Story Shell → AI/MG/Jamming → 에셋 적용` 순서로 진행한다. Gate·순서·정방향 판정·Lap·Timing은 아직 구현되지 않았으며 TUT-02 이후 범위다. 상세 기준은 `docs/DRONE_TUTORIAL_STORY_PLAN.md`를 따른다.

### 병행: PC 간 공유 검증

`drone`과 `md`의 첫 Push는 완료했다. 다른 PC Clone/LFS/UE 5.8.1 실행과 문서 Clone/Pull을 확인하면 PC 간 전체 공유 흐름을 닫는다.

## 22. 이후 사용자가 확정한 사항

- 현재 Drone 프로젝트에서는 Android를 사용하지 않는다.
- 이에 따라 Android 전용 기능은 현재 개발 범위에 포함하지 않는다.
- 외부 구매 소스는 아직 확보되지 않았다.
- 구매 소스를 확보하기 전에는 완성형 외형보다 기능 구현과 Greybox 플레이 사이클 검증을 우선한다.

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
- Standalone 싱글플레이만 현재 검증 범위로 두며 네트워크·Android·구매 에셋은 제외한다.
- C++ 변경과 전체 빌드 전에는 열려 있는 Unreal Editor를 저장하고 종료한다.
- Drone 작업을 진행할 때 `WORKBOARD.md`에 현재 단계·진행 정도·지금 작업·완료 근거·다음 작업을 갱신하고, 실제 변경과 검증 이력은 `docs/DRONE_WORKLOG.md`에 같은 작업에서 추가한다.

## 26. 2026-08-21 Tutorial·Story 방향 확정

- Tutorial은 비충돌 Spline 안내선과 순서형 원형 Gate를 따라 비행하는 훈련 모드다.
- 상시 HUD에는 속도·고도·수직 속도·Heading을 표시한다.
- Gate마다 Segment Time과 실제 이동 거리 기준 평균 속도를 계산하고 이전 성공 기록 평균·Best 대비 ± 차이를 표시한다.
- Story는 Operator Character, NPC 대화, Mission 안내 UI, Operator↔Drone 화면/Possess 전환을 포함한다.
- Jamming은 신호 경고 → HUD Noise → 조작/통신 저하의 재현 가능한 단계형 규칙으로 만든다.
- 제공 Drone 에셋은 기능 부모로 상속하지 않고 `/Game/Drone` 아래 Integration Blueprint에서 Visual만 교체한다.

## 27. 2026-08-23 HUD-02·TUT-01 완료와 현재 기준

- 이번 확인 PC의 실제 Unreal 저장소는 `C:\URproject\drone`이다. 뒤처진 `C:\project\Drone` 복제본은 현재 작업에 사용하지 않는다.
- Unreal 저장소의 로컬 `main`과 `origin/main`은 TUT-01 Commit `5a9a2faed4591a574988b649278cb0f166e31267`으로 일치한다. `9f91bb6`은 WBP/BP 연결 보강, `410c940`은 native HUD 기준선으로 보존한다.
- C++ `UDroneFlightHUDWidget`과 PlayerController가 현재 Possess Drone의 Telemetry Event·Widget 생성·Delegate 정리를 담당하고, 실제 `WBP_DroneFlightHUD`가 `SPD`, `ALT`, `V/S`, `HDG`의 배치·폰트·색을 담당한다. BP Controller가 WBP를 선택하고 BP GameMode가 BP Controller를 선택한다. Tick·Property Binding·매 프레임 Pawn 검색은 사용하지 않는다.
- TUT-01은 `ADroneTrainingCourse`, `BP_DroneTrainingCourse`, `Lvl_DroneTraining`, `M_DroneTrainingGuide`와 Tutorial 자동화 테스트 3개로 구성한다. Course가 편집 가능한 Spline과 런타임 표시용 Spline Mesh를 소유하고, Material은 Opaque·Unlit·Emissive와 Spline Mesh 사용 설정으로 Cyan 안내선을 표시한다.
- TUT-01 `DroneEditor Win64 Development` 빌드는 성공했다. `Drone.Tutorial`은 3/3, 전체 `Drone.` 자동화는 10/10이며 warning과 failure가 없다. `CompileAllBlueprints`도 0 errors, 0 warnings, 0 blueprints failed to load다.
- Standalone에서 실제 BP Controller/Pawn/WBP HUD와 Cyan 안내선을 확인했고 Material fallback 경고는 없었다. 자동화 Sweep에서 안내선이 이동을 막지 않으며 Course Primitive의 Collision·Overlap·Physics·Navigation 영향이 꺼진 것을 확인했다. Training Map에는 저장된 Recast NavMesh Actor가 있다.
- 다음 활성 카드는 `TUT-02` Gate·순서·정방향 판정이다. Gate·Lap·Segment Timing은 아직 구현되지 않았다. 배터리·신호·Jamming 표시와 최종 HUD 디자인도 구현 완료로 간주하지 않는다.
- Android는 개발 범위에서 제외하고 구매 소스는 TUT-02의 선행 조건으로 두지 않는다.
- 문서 저장소는 이번 갱신 직전 로컬 `main`과 `origin/main`이 `b63eee1`에서 일치했으며, 이 상태·계획 갱신도 Commit·Push해 PC 간 공유 기준에 반영한다.
