# 작업컴 시작 가이드

기준일: 2026-10-23 KST, D PC. 실제 상태는 [STATUS](STATUS.md), 작업 순서는 [WORKBOARD](WORKBOARD.md), 경계는 [CONTEXT](CONTEXT.md)가 정본이다. [세션 등록부](docs/git/DRONE_WORK_PC_SESSIONS.md)에 역할별 실제 대화 ID와 파일/엔진 소유권을 기록한다.

## 1. 시작할 때 읽고 확인하기

1. 두 저장소의 AGENTS.md·CLAUDE.md와 위 현재 문서·세션 가이드를 읽는다. WORKLOG는 필요한 날짜/검사명으로 검색한다.
2. 이 작업컴의 문서는 `D:\JGY\project\md`, Unreal은 `D:\JGY\project\drone`이다. 다른 PC에서는 실제 경로부터 확인한다.
3. 각 저장소에서 아래를 확인한다. 추적 ref가 서버 최신이라는 뜻은 아니다. Fetch/Pull은 네트워크 갱신이 필요한 작업에서 별도로 수행한다.

```powershell
git status --short --branch
git log -1 --oneline
git rev-list --left-right --count HEAD...origin/main
```

미커밋 변경·Git/LFS 작업·lock이 있으면 소유권과 진행 상태를 먼저 확인한다. Discard/Reset·자동 Stash 복원·작업 중 lock 삭제를 하지 않는다. 프로젝트 수신과 바이너리·자동 검사·실물 조종 성공은 별개다.

## 2. 역할과 착수 순서

10/23 입력·모터/OFF 항력, 역할별 광각·설정/선택 UI, M1/M3/M4 단계, 전면 센서·하향 조준·파괴 전환을 반영했다. Source는 `5ed30281`로 푸시했고, 고유 자동검사 101건은 변경 단계별 검증으로 통과했다(마지막 DLL 전체 재실행 아님). 최종 DLL로 정상 FrontEnd Editor를 재오픈했으며 Space 시동/상승·Ctrl OFF·해제 hover와 RC/패드 안전 조건을 유지한다. [현재 상태](STATUS.md)·[입력 정책](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md#space키-자동-시동off-정책)을 따른다. 실물 손조작·실청·패키징은 별도이며, 사용자 승인에 따라 마무리 Commit/Push는 총괄만 수행한다.

엔진/PIE/빌드/Content 저장은 본미션/LOS/성능 담당 한 곳으로 모은다. 공유 FlightPawn/Definition/IMC는 파일·함수 소유권을 먼저 정한다. 총괄의 작성권 인계 후 MD/Space는 검증/MD 역할이 단독 작성하며 최종 실행 근거를 받은 뒤 묶어서 반영한다. Codex 직접 작업에는 옛 Claude 전담 제한을 적용하지 않는다. 명시적 브리지 위임만 해당 역할 계약을 따른다.

## 3. 수신과 검증 도구

다른 PC의 변경이 필요하면 사용자가 두 저장소의 Commit/Push·LFS 업로드를 마친 뒤 GitHub Desktop에서 Fetch/Pull한다. 작업컴 기존 변경을 보존한다. 인증 파일·토큰·원시 세션 DB는 옮기지 않는다.

아래 도구의 소스/인자와 실제 Engine 경로를 확인한 뒤 필요한 범위만 선택한다. 문서 최신화·세션 준비만으로 Build/PIE를 실행하지 않는다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File D:\JGY\project\md\tools\work-pc\Test-DroneWorkstation.ps1 `
  -DocsPath D:\JGY\project\md `
  -DroneProjectPath D:\JGY\project\drone\Drone.uproject `
  -EngineRoot 'C:\Program Files\Epic Games\UE_5.8'
```

`-RunLfsFsck`, `-RunBuild`, `-RunTutorialValidation`은 목적에 맞게 추가한다. 기본 점검 성공은 Build/실행 성공이 아니다. 전체 C++ Build 전에 사용자 Editor 저장/종료와 다른 역할의 소스 변경 중지를 확인한다. 장시간 패키징/전체 쿠킹은 먼저 영향과 실행 시점을 확인한다.

## 4. 실제 화면·맵·입력 확인

통합 진입은 `/Game/Drone/Maps/Lvl_DroneFrontEnd`이다. 현재 제품 Tutorial·Story·팀원 레이싱 맵의 정확한 DA 연결과 완료 조건은 [테스트 맵 가이드](docs/gameplay/DRONE_TEST_MAP_GUIDE.md)를 따른다. 옛 독립 TestMap 통과로 실제 제품 맵을 대신하지 않는다.

- LOS만 이륙→전진→후진 복귀→실제 접지를 유지한다. 원형 수업은 한 바퀴 뒤 즉시 성공이며 LOS 외 옛 귀환 조건을 되살리지 않는다.
- M1/M2 실패 재도전, M3/M4 진행 보존·기체 재선택 무한 출격, M4 기체→시작3지점→출격의 현재 구현/미확인은 [미션 가이드](docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md)를 따른다.
- 카메라 상하 시야·감도, 모터 OFF/착지/재이륙, LOS 후퇴/드론 보기, M3/4 실제 목표, 렉/로딩은 [현실 조종감 계획](docs/gameplay/DRONE_REALISTIC_HANDLING_PLAN.md)의 잔여 범위다.
- 자동 입력·NullRHI·숨김 렌더와 실제 화면·실물 패드·청감·숙련자 평가는 구분한다. START/BACK 영문·팀원 UI/폰트·맵 원본과 기존 변경을 보존한다.
- Production `/Game/Drone/Maps/Lvl_DroneTraining`을 시험 저장·재생성하지 않는다. 실제 PC 자원과 엔진 소유권을 확인하고 같은 조건 실패 반복·다른 앱 강제 종료를 하지 않는다.

## 5. 마무리와 인계

1. 실제 변경과 근거를 확인하고 관련 `git diff --check`를 수행한다. 개발 범위에 필요한 검사만 실행한다.
2. 현재 상태는 STATUS, 순서는 WORKBOARD, 검증 전문은 WORKLOG 끝에 남긴다. MD/Space 작성자는 한 명으로 조율한다.
3. [Space 갱신 규칙](docs/git/DRONE_SPACES_SYNC.md)에 따라 기존 관련 Page를 수정하고 저장 후 재조회한다. 실패하면 미반영 범위를 로컬에 남긴다.
4. 구현/자동 검사/실화면/실물 조종, 이전 PC/현재 PC, 로컬 추적 ref/실제 서버를 구분해 보고한다.
5. Commit/Push·Trello 수정·공유 권한 변경·예약 자동화는 별도 사용자 요청이 있을 때만 한다.

이전 시작 가이드의 날짜별 검증과 옛 절차는 [10월 원문 아카이브](docs/history/archive/WORK_PC_START_HERE_2026-10.md)에 보존했다.
