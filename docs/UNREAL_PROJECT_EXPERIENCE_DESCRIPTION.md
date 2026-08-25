# Unreal 프로젝트 경험 기술 예시

기준일: 2026-08-25

이 문서는 현재 실제 구현·검증한 범위만 사용해 지원서의 `관련 경력`, `프로젝트 경험`, `경험 기술` 항목을 작성하기 위한 초안이다. 근무·계약 경력이 아니라면 회사 경력으로 쓰지 말고 **팀 프로젝트 경험**으로 구분한다.

## 가장 무난한 한 줄

> UE 5.8.1 기반 드론 운용 시뮬레이터 팀 프로젝트에서 C++/Blueprint로 비행 프로토타입, 텔레메트리 HUD, 순서형 링 게이트와 구간·랩 기록 시스템을 구현하고 Git LFS 및 자동화 테스트 환경을 구축했습니다.

## 지원서용 짧은 버전

### 프로젝트명

UE 5.8.1 기반 드론 운용 시뮬레이터 게임 — 대학생 5인 팀 프로젝트

### 기간

`[실제 시작 YYYY.MM] ~ 진행 중`

기간은 실제 날짜를 확인해 입력한다. 현재 문서만으로 시작 월을 확정하지 않는다.

### 역할

Unreal C++ Gameplay 개발 및 Git/Git LFS 개발 환경 구성

### 경험 기술

> 구매 에셋에 의존하기 전에 Greybox Vertical Slice를 검증하는 방향으로 개발했습니다. C++ `APawn`과 Enhanced Input을 기반으로 드론 이동·카메라·입력 구조를 만들고, 10Hz Event 기반 Telemetry와 Blueprint HUD를 연결했습니다. Tutorial에서는 Spline Course, 순서·정방향을 검증하는 Ring Gate, World Game Time과 10Hz 위치 표본을 이용한 Segment/Lap 시간·3차원 누적 이동 거리·평균 속도 기록을 구현했습니다. 바이너리 Asset 충돌을 줄이기 위해 Git LFS와 기능 Branch를 사용했으며, Editor Build·Blueprint Compile과 Unreal Automation Test 14개로 회귀를 검증했습니다.

## 이력서 Bullet 버전

- UE 5.8.1 C++ `APawn` 기반 드론 비행 Prototype과 Enhanced Input Keyboard·Mouse·Gamepad 입력 구조 구현
- Camera, Movement, Telemetry, HUD, Tutorial Course, Gate Sequence, Lap Recorder의 책임을 Component와 Event 경계로 분리
- Telemetry 10Hz Event와 World Game Time을 사용해 위치 표본 기반 3차원 누적 이동 거리, Segment/Lap 시간, 평균 속도 계산
- C++ 기능과 Blueprint 외형을 분리하고 `BlueprintAssignable` Event와 `BlueprintPure` Getter로 후속 UI 연결 지점 제공
- 잘못된 Gate 순서·역방향·중복 통과, Reset, Pawn 파괴와 Delegate 수명주기를 자동화 테스트로 검증
- `.uasset`·`.umap`을 Git LFS로 관리하고 기능 Branch → 검증 → `main` 반영 흐름 운영
- 외부 FPV Mesh·Sound를 프로젝트 소유 Integration Blueprint 아래 선별 이식해 Gameplay C++와 외부 Asset 의존성 분리

## 문제 해결 중심 버전

### 문제

Unreal의 바이너리 Asset은 코드처럼 병합하기 어렵고, Gate 판정·기록과 향후 결과 UI까지 한 Blueprint에 넣으면 기능 확장과 테스트가 어려워지는 문제가 있었다.

### 해결

- `UDroneTrainingGateSequenceComponent`는 순서·방향 판정만 담당하도록 유지했다.
- 별도 `UDroneTrainingLapRecorderComponent`가 정상 Gate Event만 구독해 시간과 이동 거리를 기록하도록 분리했다.
- 기존 `UDroneTelemetryComponent`의 10Hz Event를 위치 표본 시계로 재사용해 추가 Tick과 Timer를 만들지 않았다.
- 결과 Struct와 Event를 Blueprint에 노출해 TUT-04 결과 UI가 계산 로직을 다시 작성하지 않도록 했다.
- Game World, 실제 저장 BP/Map PIE, 전체 회귀를 서로 다른 자동화 테스트로 나눴다.

### 결과

> Gate 0 시작, Gate별 Segment 확정, 마지막 Gate Lap 완료 흐름과 Reset·오류 입력·Pawn 파괴 예외를 구현했습니다. `DroneEditor Win64 Development` Build, Tutorial 6/6, 전체 `Drone.` Automation 14/14, Blueprint Compile 0 errors·0 warnings·0 load failures를 통과했으며 Unreal Commit `551e287`로 GitHub `main`에 반영했습니다.

## 면접에서 40초로 설명하는 순서

1. **목표:** 드론 조작만 있는 Prototype을 짧은 Tutorial 플레이 사이클로 확장했다.
2. **내 역할:** C++ Gameplay 구조, Blueprint 연결 경계, Git/LFS와 자동화 검증을 담당했다.
3. **핵심 선택:** Gate 판정과 기록을 별도 Component로 나누고 기존 Telemetry Event를 재사용했다.
4. **검증:** 정상·실패·Reset·수명주기와 실제 BP PIE까지 자동화했다.
5. **다음 단계:** 이전 평균·Best 비교와 결과 UI를 추가한 뒤 Flight 상태와 Mission으로 확장할 예정이다.

## 아직 쓰면 안 되는 표현

현재 확인되지 않았거나 구현 전인 내용은 실적으로 쓰지 않는다.

- `J3C 발주·협력 프로젝트` — J3C는 콘셉트상 가상 발주처일 뿐 실제 계약 관계가 아니다.
- `군사 훈련 시스템 납품` 또는 특정 군·국가 대상 개발
- `멀티플레이 구현`, `Listen Server 구현`
- `Enemy AI·MG Turret·Jamming 구현 완료`
- `배터리·통신 거리·Mission·평가 시스템 구현 완료`
- `출시`, `수상`, `대회 입상`, `상용 서비스` — 실제 결과가 생기기 전에는 사용하지 않는다.
- `드론 물리를 실기체와 동일하게 재현` — 현재 최종 물리 모델은 미정이다.

## 제출 전에 사용자가 채울 값

- 실제 프로젝트 시작 월
- 본인의 공식 팀 역할명
- 실제로 직접 담당한 기능 범위
- 지원서 글자 수
- 대회 출품 여부와 결과가 실제로 확정됐는지
- GitHub 공개 가능 여부와 포트폴리오 영상 링크

현재 가장 안전한 분류는 **관련 경력**보다 **프로젝트 경험**이다. 채용 양식에 `관련 경력(경험)`이 하나의 칸으로 합쳐져 있다면 위 짧은 버전을 사용하고, 고용형태·회사명 칸에는 사실과 다른 회사나 발주처를 적지 않는다.
