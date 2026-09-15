# 컴퓨터과학·게임개발 추천도서 장기 학습 계획

기준일: 2026-09-15 (Asia/Seoul)

이 문서는 추천 자료 8종을 드론 Unreal 프로젝트, C++ 코딩테스트, 정보처리산업기사와 병행해 **부담 없이 오래 읽기 위한 계획**이다. 전부를 순서대로 완독하는 것이 목표가 아니라, 지금 필요한 내용을 읽고 작은 코드·설명·프로젝트 연결점으로 남기는 것을 목표로 한다.

## 1. 운영 원칙

1. 한 주에 `주교재 1개 + 보조교재 1개`만 연다.
2. 평상시에는 `30분 × 2회 + 60분 × 1회`, 바쁜 주에는 `25분 × 1회`만 한다.
3. 한 장을 다 읽지 못해도 세션이 끝나면 멈춘다. 다음 세션에서 같은 절부터 재개한다.
4. 읽은 분량보다 `내 말로 설명 3줄`, `작은 예제 1개`, `현재 프로젝트 연결점 1개`를 우선한다.
5. 책에서 본 Pattern이나 기술을 Drone Production 코드에 바로 넣지 않는다. 문제와 이득이 확인된 경우에만 별도 TestMap·시험 코드에서 검증한다.
6. 시험이 임박하거나 Drone 통합 작업이 바쁜 주에는 이 계획을 중단해도 된다. 밀린 분량을 몰아서 보충하지 않는다.
7. 자료는 공식 웹 공개본이나 정식 구입본을 사용한다. 출처가 불분명한 PDF는 받지 않고, PDF·영상 파일 자체를 Git 저장소에 Commit하지 않는다.

## 2. 추천 순서

원래 추천 번호와 실제 학습 순서는 다르다. 현재 작업과 연결하기 쉬운 순서로 재배치한다.

| 실제 순서 | 자료 | 우선도 | 읽는 목적 | 현재 Drone 연결점 |
|---:|---|---|---|---|
| 1 | [Game Programming Patterns](https://gameprogrammingpatterns.com/) | 최우선 | 게임 코드의 결합도·상태·이벤트·성능 구조 이해 | GameFlow, Mission, StateTree, Component, Delegate, Projectile |
| 2 | [Immersive Linear Algebra](https://immersivemath.com/ila/index.html) | 최우선 보조 | Vector·내적·외적·행렬·좌표 변환을 시각적으로 이해 | Drone 기울기, Camera, Gate 방향 판정, Turret 조준, 지면 추종 |
| 3 | [Operating Systems: Three Easy Pieces](https://pages.cs.wisc.edu/~remzi/OSTEP/) | 높음 | Process·가상화·동시성·메모리·저장장치 이해 | Editor/Commandlet 분리, Thread, Race, Asset I/O, Build 성능 |
| 4 | [Crafting Interpreters](https://craftinginterpreters.com/) | 높음 | Scanner→Parser→AST→실행기→VM이 이어지는 구조를 직접 구현 | Mission 조건식, 데이터 검증, 상태/명령 해석 구조 이해 |
| 5 | [Physically Based Rendering 4판](https://pbr-book.org/4ed/contents) | 선택 심화 | 광선·Camera·Material·Light·Sampling·BVH 이해 | Unreal Camera/Material/Trace/Lighting과 성능 판단 |
| 6 | [Computer Networking: A Top-Down Approach 9판 강좌](https://gaia.cs.umass.edu/kurose_ross/lectures.php) | 선택 기초 | Application→Transport→Network→Link 순서로 통신 이해 | 향후 원격 조종, Telemetry, 지연·손실·Jamming 설계 기반 |
| 7 | [Deep Learning](https://www.deeplearningbook.org/) | 장기 심화 | 선형대수·확률·최적화·신경망의 고전적 기초 정리 | 향후 AI 판단 도구 평가, 모델 성능·오류 해석 |
| 8 | [Speech and Language Processing 3판 Draft](https://web.stanford.edu/~jurafsky/slp3/) | 장기 심화 | Token·분류·Embedding·Transformer·RAG·음성 이해 | 향후 NPC 대화·Mission 문장·음성 기능의 기술 판단 |

### 우선순위 해석

- `Game Programming Patterns + Immersive Linear Algebra`는 지금 바로 시작한다.
- OSTEP과 Crafting Interpreters는 C++와 시스템 사고를 단단하게 만드는 두 번째 축이다.
- PBRT는 Unreal 렌더링을 직접 수정하기보다, Material·Light·Trace가 왜 그렇게 동작하는지 이해하기 위해 선택해 읽는다.
- Network는 현재 프로젝트가 Standalone이므로 급한 구현 항목이 아니다. Jamming을 실제 통신 모델로 확장하거나 온라인 기능을 검토할 때 우선도를 올린다.
- Deep Learning과 SLP는 기초 수학·시스템 학습 뒤 진행한다. 현재 NPC에 대화 기능이 필요하다는 이유만으로 곧바로 모델을 붙이지 않는다.

## 3. 한 번 공부할 때의 30분 루프

| 시간 | 행동 |
|---:|---|
| 5분 | 지난 기록을 보지 않고 핵심 개념을 말하거나 적는다. |
| 15분 | 한 절을 읽거나 강의 영상 한 구간을 본다. 모르는 문장을 전부 번역하려 하지 않는다. |
| 5분 | 코드·그림·수식 예제를 손으로 다시 써 본다. |
| 5분 | 아래 기록 양식으로 3줄 요약과 다음 시작점을 남긴다. |

60분 세션에서는 읽기 25분, 예제·연습 20분, Drone 연결 검토 10분, 기록 5분으로 늘린다.

### 세션 기록 양식

```text
날짜:
자료 / 장·절:
공부 시간:

내 말로 설명 3줄:
1.
2.
3.

핵심 용어 1개:
작은 예제 또는 손풀이:
Drone/C++와 연결되는 부분:
아직 모르는 점:
다음 시작 위치:
```

### 한 장 완료 기준

- 핵심 문제를 한 문장으로 설명할 수 있다.
- 주요 개념 2~3개를 코드나 그림으로 설명할 수 있다.
- 사용할 때와 사용하지 말아야 할 때를 하나씩 말할 수 있다.
- Drone 프로젝트의 실제 코드 또는 기능과 연결점 하나를 찾았다.
- 연결점이 없으면 `현재 적용하지 않음`이라고 적고 넘어갔다.

## 4. 1단계 — 게임 구조와 수학 감각, 8주

주교재는 Game Programming Patterns, 보조교재는 Immersive Linear Algebra다.

| 주차 | Game Programming Patterns | Immersive Linear Algebra | 작은 결과물 |
|---:|---|---|---|
| 1 | Architecture, Performance, and Games | 1장 Introduction, 삼각함수 복습 | 현재 Drone 모듈 책임을 5줄로 설명 |
| 2 | Command | 2장 Vector | 입력 Action→명령 흐름을 간단히 그림 |
| 3 | Observer | 3장 Dot Product | Delegate/Event와 Gate 방향 내적 연결 |
| 4 | State | 4장 Vector/Cross Product | GameFlow 또는 NPC 상태 전이표 1개 |
| 5 | Component | 5장 Gaussian Elimination은 가볍게 훑기 | Health/Telemetry/Reservation 책임 비교 |
| 6 | Event Queue | 6장 Matrix | Mission Event 전달 경로 1개 추적 |
| 7 | Type Object, Dirty Flag | 9장 Linear Mappings 우선 | Data Asset/Definition과 Transform 연결 |
| 8 | Object Pool, Spatial Partition, Data Locality | 필요한 절 복습 | Pattern 후보 1개를 도입/보류 판정 |

### 이 단계에서 Drone 코드에 대입할 질문

- `State`: Front-end/Mission 상태와 NPC StateTree의 책임은 어디서 갈리는가?
- `Observer`: Health·Gate·Mission Event가 직접 참조 없이 전달되는가?
- `Component`: Pawn이 너무 많은 기능을 직접 소유하고 있지 않은가?
- `Event Queue`: 한 프레임의 여러 이벤트 순서가 결과를 바꾸는가?
- `Object Pool`: 실제 Projectile 생성 비용이 측정됐는가? 측정 전에는 Pool을 넣지 않는다.
- `Dot Product`: Ring 정방향, AI 시야각, Turret 정렬 오차를 어떻게 판정하는가?
- `Matrix/Transform`: Local·World·Component Space를 혼동해 Rotor나 Gaze가 잘못 도는 지점은 없는가?

## 5. 2단계 — 운영체제 기초, 10주

OSTEP은 공식 사이트가 설명하는 세 축인 Virtualization, Concurrency, Persistence 순서로 읽는다. 전 장 완독보다 아래 핵심 절을 우선한다.

| 주차 | 우선 주제 | 실습·확인 |
|---:|---|---|
| 1 | Processes, Process API | Editor와 `UnrealEditor-Cmd`가 별도 Process인 이유 정리 |
| 2 | Direct Execution, CPU Scheduling | Build/Automation 동시 실행 시 CPU 점유 관찰 |
| 3 | Address Spaces, Memory API | Stack/Heap/UObject 생명주기 차이 메모 |
| 4 | Paging, TLB | 큰 Map·Asset 로드에서 메모리 지표 확인 방법 조사 |
| 5 | Concurrency and Threads | Game Thread, Render Thread, Task의 책임을 구분 |
| 6 | Locks, Condition Variables | Race/Deadlock 예제 하나 손으로 추적 |
| 7 | Semaphores, Concurrency Bugs | 재현 어려운 테스트 실패를 순서·공유상태 관점에서 분석 |
| 8 | Files and Directories | Unreal Package와 생성 폴더의 차이 정리 |
| 9 | File System Implementation, Journaling | 저장 중 Crash와 복구 경계를 개념적으로 정리 |
| 10 | Data Integrity, Distributed Systems는 선택 | Git/Git LFS가 해결하는 문제와 하지 못하는 문제 정리 |

주의: OSTEP의 `LFS`는 Log-structured File System 문맥일 수 있으며, 현재 프로젝트의 `Git LFS`와 같은 뜻이 아니다.

## 6. 3단계 — Interpreter 직접 만들기, 12주

Crafting Interpreters는 읽기만 하면 효과가 크게 줄어든다. 첫 번째 Tree-Walk Interpreter를 따라 만들되 Production Drone 코드가 아닌 별도 학습 폴더에서 진행한다.

| 기간 | 범위 | 목표 |
|---|---|---|
| 1~2주 | 1~3장 | 언어 구현 지형과 Lox 문법 이해 |
| 3주 | 4장 Scanning | 문자열을 Token으로 분리 |
| 4~5주 | 5~6장 AST·Parsing | 연산 우선순위와 Syntax Tree 구성 |
| 6주 | 7장 Evaluating | 식 계산기 완성 |
| 7~8주 | 8~9장 State·Control Flow | 변수·분기·반복 구현 |
| 9~10주 | 10~11장 Functions·Binding | Scope와 이름 해석 구현 |
| 11~12주 | 12~13장 Classes·Inheritance | 첫 Interpreter 완료와 회고 |

14~30장의 Bytecode VM은 별도 2회차다. 첫 회차와 동시에 진행하지 않는다. C++ 연습이 목적이면 개념을 이해한 뒤 작은 Expression Parser만 C++로 다시 작성해도 된다.

### Drone 연결 아이디어

- `목표 3개 파괴 AND 제한시간 120초` 같은 Mission 조건이 어떻게 Token/AST로 표현될지 종이에만 설계한다.
- 기존 Data Asset과 Enum으로 충분하다면 별도 DSL은 구현하지 않는다.
- Parser의 오류 위치·메시지 설계를 Mission Definition 검증 로그에 참고한다.

## 7. 4단계 — 그래픽스와 렌더링, 10주 이상

PBRT 4판은 앞 내용을 전제로 쓰였으므로 첫 회차에는 구현 세부를 전부 따라가지 않는다. Immersive Linear Algebra의 Vector, Dot/Cross Product, Matrix, Linear Mapping을 먼저 끝낸다.

### 첫 회차 선택 경로

1. PBRT 1장 Introduction
2. 3장 Geometry and Transformations
3. 5장 Cameras and Film
4. 6장 Shapes
5. 7장 Primitives and Intersection Acceleration
6. 9장 Reflection Models
7. 10장 Textures and Materials
8. 12장 Light Sources
9. 13장 Surface Light Transport와 간단한 Path Tracer

### 두 번째 회차 후보

- 2장 Monte Carlo Integration
- 4장 Radiometry, Spectra, Color
- 8장 Sampling and Reconstruction
- 11·14장 Volume Scattering
- 15장 GPU Wavefront Rendering

### Unreal 연결 질문

- Camera FOV와 Projection이 Drone 조작 체감에 어떤 영향을 주는가?
- Line/Sphere Trace와 Ray/Shape Intersection은 개념적으로 어디가 같은가?
- Material의 Base Color, Roughness, Metallic이 반사 모델과 어떻게 연결되는가?
- BVH·공간 분할을 이해하면 대규모 Trace/AI 탐색 비용을 어떻게 판단할 수 있는가?

PBRT 코드를 Unreal Renderer에 직접 이식하는 것이 목표는 아니다. 원리 이해와 성능 판단이 목표다.

## 8. 5단계 — 네트워크, 8주

공식 9판 온라인 강좌는 영상, Notes, Knowledge Check, Interactive Problems를 함께 제공한다. 책은 정식 구입본을 사용하고 공개 강좌만으로도 첫 회차를 진행할 수 있다.

| 주차 | 범위 | 확인할 핵심 |
|---:|---|---|
| 1 | Chapter 1 | Protocol, Delay, Loss, Throughput |
| 2~3 | Chapter 2 | HTTP, DNS, Socket, Client/Server |
| 4~5 | Chapter 3 | UDP/TCP, Reliability, Congestion |
| 6 | Chapter 4~5 | Forwarding, Routing, Control Plane |
| 7 | Chapter 6 | Ethernet, ARP, Link Layer |
| 8 | Chapter 7~8 선택 | Wireless/Mobile, Security |

각 장에서 영상 1~2개 → Notes → Knowledge Check 순으로 진행한다. Wireshark Lab은 사용 가능한 공식 자료 범위에서 한 장당 하나만 선택한다.

### Drone 연결 질문

- 지연, Jitter, Packet Loss를 게임의 `재밍`과 같은 것으로 취급하면 왜 안 되는가?
- 원격 Drone 영상·입력·Telemetry는 신뢰성/지연 요구가 어떻게 다른가?
- 현재 Standalone 범위에 실제 Networking 구현이 필요한가? 필요하지 않으면 문서 설계까지만 한다.

## 9. 6단계 — Deep Learning과 SLP, 12주 이상

두 자료를 동시에 처음부터 완독하지 않는다. Deep Learning의 수학·ML 기초를 먼저 읽고 SLP의 현대 언어 모델 경로로 넘어간다.

### Deep Learning 첫 회차

1. 1장 Introduction
2. 2장 Linear Algebra — Immersive Linear Algebra 복습용
3. 3장 Probability and Information Theory
4. 4장 Numerical Computation
5. 5장 Machine Learning Basics
6. 6장 Deep Feedforward Networks
7. 7장 Regularization
8. 8장 Optimization
9. 9장 Convolutional Networks는 선택

2016년 교재이므로 최신 LLM 사용법 안내서로 읽지 않는다. 수학·최적화·일반화의 기반을 배우는 자료로 사용한다.

### Speech and Language Processing 첫 회차

현재 공식 사이트의 3판 Draft는 계속 갱신되므로 기록에 읽은 Release 날짜를 함께 남긴다.

1. 1장 Introduction
2. 2장 Words and Tokens
3. 3장 N-gram Language Models
4. 4장 Logistic Regression and Text Classification
5. 5장 Embeddings
6. 6장 Neural Networks
7. 7장 Transformers, Pretraining, Decoding
8. 11장 Information Retrieval and RAG
9. NPC 음성이 실제 범위에 들어올 때만 15~17장 Speech/TTS

### 적용 경계

- NPC 대화가 필요해도 처음에는 정적 데이터·분기 UI로 구현한다.
- 모델이 필요하다는 가설이 생기면 품질, 지연, 비용, 개인정보, Offline 동작을 먼저 정의한다.
- 학습용 Python 실험과 Unreal Runtime 기능을 같은 단계에서 결합하지 않는다.

## 10. 첫 4주 바로 실행표

### 1주차

- 30분: Game Programming Patterns `Architecture, Performance, and Games`
- 30분: Immersive Linear Algebra 1장과 삼각함수 복습
- 60분: `Source/Drone`의 큰 기능 5개를 Component/State/Event 관점으로 분류

### 2주차

- 30분: Game Programming Patterns `Command`
- 30분: Immersive Linear Algebra `Vectors`
- 60분: Enhanced Input Action 하나가 Pawn 기능 호출까지 가는 경로를 손으로 작성

### 3주차

- 30분: Game Programming Patterns `Observer`
- 30분: Immersive Linear Algebra `Dot Product`
- 60분: Gate 통과 Event 또는 Health Damage Event의 발행자·구독자·수명주기 기록

### 4주차

- 30분: Game Programming Patterns `State`
- 30분: Immersive Linear Algebra `Vector Product`
- 60분: GameFlow와 NPC Response State 중 하나를 상태·Event·금지 전이 표로 정리

## 11. 4주마다 할 회고

아래 질문에 한 줄씩 답한다.

```text
지난 4주에 실제로 읽은 자료:
가장 잘 설명할 수 있는 개념:
아직 설명하지 못하는 개념:
직접 작성한 예제:
Drone 프로젝트를 이해하는 데 도움 된 부분:
괜히 적용하려 했던 Pattern/기술:
다음 4주 주교재:
보조교재:
주당 현실적인 시간:
```

진도가 계속 밀리면 학습량을 늘리지 않는다. 주교재의 범위를 절반으로 줄이고 보조교재를 한 달 쉬는 방식으로 조정한다.

## 12. 진행표

| 자료 | 현재 상태 | 다음 시작점 | 완료 기준 |
|---|---|---|---|
| Game Programming Patterns | 시작 대기 | Architecture, Performance, and Games | 우선 Pattern 10개를 문제·장단점·Drone 연결로 설명 |
| Immersive Linear Algebra | 시작 대기 | Introduction → Vectors | Vector·Dot/Cross·Matrix·Transform을 그림과 예제로 설명 |
| OSTEP | 대기 | Processes | Virtualization·Concurrency·Persistence 핵심 노트 완성 |
| Crafting Interpreters | 대기 | Introduction | Tree-Walk Interpreter 1개와 회고 완성 |
| PBRT | 대기 | Introduction | 선택 경로 9개 장의 핵심 원리 노트 |
| Computer Networking | 대기 | 9판 Chapter 1 강좌 | 1~6장 Knowledge Check와 네트워크 흐름 설명 |
| Deep Learning | 장기 대기 | 1장 | 2~8장 핵심 개념과 작은 Python 실험 |
| Speech and Language Processing | 장기 대기 | Release 날짜 확인 → 1장 | 1~7·11장 개념과 NPC 적용/미적용 판단 |

첫 실행은 `Game Programming Patterns 1장 30분`이다. 읽은 뒤 완독률을 계산하지 말고 세션 기록 하나만 남긴다.
