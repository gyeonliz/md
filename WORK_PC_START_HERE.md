# 작업컴 시작 가이드

기준일: 2026-10-01 (Asia/Seoul)

이 문서는 작업컴 `D:\JGY\project\md`와 `D:\JGY\project\drone`에서 현재 Drone 작업을 바로 이어가기 위한 단일 시작점이다. 최신 구현 사실은 `STATUS.md`, 다음 작업은 `WORKBOARD.md`, 변경 금지 경계는 `CONTEXT.md`를 우선한다.

## 1. 현재 인계 상태

2026-10-01 작업컴 수신 확인: 출격 전 뒤로가기(기체 선택→설명→로비→시작), 설정 닫기·Esc/패드 Back·선택 복원, Tutorial 8개 독립 시험맵·Story/Racing 직접 Play Entry, Title 이미지/탭·Setting, 비 CPU 예산 개선·OilRig 비교 맵은 이미 현재 체크아웃과 원격에 반영됐다. [기능·인계 검증 범위](docs/gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md)

- 최신 확인 Unreal: `D:\JGY\project\drone`, `main = origin/main = 83b33c1bccf5e9524579001a7688df57e972426b`
- 최신 확인 문서: `D:\JGY\project\md`, 점검 시작 시 `main = origin/main = aecb6ece1cb7b369a84499e3645098c0cbb8a801`
- Physics Sandbox, Story 4맵, Training Route, 광섬유 GSU, Bangkok City·OilRig Preview도 포함됐다.
- `git ls-remote origin refs/heads/main`으로 실제 원격과 대조했다. 점검 시작 두 Clean·앞섬/뒤처짐 0/0, Unreal LFS 업로드 대기·Stash 없음. 최신 커밋의 변경 바이너리 패키지 32개가 포인터 아닌 본문이며 전체 LFS 해시 무결성 검사를 대신하지는 않는다.
- 오늘 기본 준비는 `WORKSTATION_READY`(실패/경고 0). 후속 UI 요청으로 Editor Build와 집중 5개 자동화도 성공했다(`Saved/Automation/TrainingLobbySettings`). 전체 Tutorial/성능과 렌더 화면·음량은 재검증하지 않았다. 이전 PC의 Oct 1 원시 보고서는 현재 Saved에 없어 인계 결과로 구분한다.
- 후속 로컬 변경: 기존 이미지 유지, 시작→Story4/훈련→Tutorial9·Racing1, 로비/브리핑·기체 카드 레이아웃, 사운드/화면/성능 설정. C++/테스트·MD는 아직 미커밋이고 Content/맵은 변경하지 않았다. Commit/Push는 사용자 담당이다.
- 이미 작업컴에서 이 문서를 Pull해 읽고 있다면 4절 점검 결과를 우선한다. 두 저장소가 원격과 일치하고 필수 Asset 검사가 통과하면 전달이 완료된 상태다.
- Codex 원시 세션 폴더, `auth.json`, API Key, 토큰은 복사하지 않는다.

## 2. 새 변경을 메인컴에서 만든 경우의 사용자 작업

Unreal Editor와 실행 중인 명령줄 Editor를 모두 종료한다. 그다음 GitHub Desktop에서 아래 순서로 처리한다.

### 2-1. Unreal 저장소

1. 저장소 `gyeonliz/drone`을 선택한다.
2. 오늘 변경은 `Source/Drone/UI`·`Source/Drone/Flow`와 테스트·`AGENTS.md`다. 자산/맵 재이식은 필요 없다. `Saved` 보고서는 Git 제외이므로 필요한 증거는 별도 전달하거나 문서 결과를 참고한다.
3. Commit 제목 예시: `훈련 메뉴와 UI 시안 반영 및 사운드 화면 설정`
4. Commit 후 `Push origin`을 누른다.
5. Git LFS 업로드가 끝날 때까지 GitHub Desktop을 닫지 않는다.

### 2-2. 문서 저장소

1. 저장소 `gyeonliz/md`를 선택한다.
2. `WORK_PC_START_HERE.md`, `STATUS.md`, `WORKBOARD.md`, `CONTEXT.md`, `docs`, `tools/work-pc` 변경을 확인한다.
3. Commit 제목 예시: `작업컴 인계 문서와 튜토리얼 가이드 최신화`
4. Commit 후 `Push origin`을 누른다.

기존 독립 맵/대형 환경 이식은 이미 원격에 있으므로 다시 구현/Commit하지 않는다. 오늘 후속 UI·Settings와 MD 변경만 새 공유 대상이다. `git lfs push`만으로는 Commit 이력이 올라가지 않으므로 사용자가 검토 후 Commit과 `Push origin`을 수행한다.

## 3. 작업컴에서 받는 순서

GitHub Desktop에서 문서 저장소와 Unreal 저장소를 각각 `Fetch origin` → `Pull origin` 한다. 저장소가 없다면 다음 위치에 Clone한다.

```text
D:\JGY\project\md
D:\JGY\project\drone
```

PowerShell에서 LFS 본문을 받는다.

```powershell
cd D:\JGY\project\drone
git lfs install
git lfs pull origin main
```

`Discard Changes`, `Reset`, 자동 Stash 적용은 하지 않는다. 작업컴에 기존 변경이 보이면 먼저 파일 소유자와 내용을 확인한다.

## 4. 한 번에 준비 상태 확인

Unreal Editor를 닫은 상태에서 실행한다. 기본 점검은 Git·LFS·Branch·원격 동기화·필수 Tutorial Asset·Engine 경로를 확인한다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
  -File D:\JGY\project\md\tools\work-pc\Test-DroneWorkstation.ps1 `
  -DocsPath D:\JGY\project\md `
  -DroneProjectPath D:\JGY\project\drone\Drone.uproject `
  -EngineRoot 'C:\Program Files\Epic Games\UE_5.8' `
  -RequireClean `
  -RunLfsFsck `
  -RunBuild `
  -RunTutorialValidation
```

마지막 줄이 `WORKSTATION_READY`면 지정한 검사 범위를 통과한 것이다. 빠른 기본 점검만 할 때는 `-RunLfsFsck`, `-RunBuild`, `-RunTutorialValidation`을 빼고 실행한다. 기본 통과를 빌드/런타임 성공으로 해석하지 않는다. 기본 도구는 Fetch/Pull하지 않으므로 원격 최신성은 별도 대조한다. 실행 정책은 이 명령 한 번에만 우회하며 시스템 전체 정책을 변경하지 않는다.

### 실패 메시지별 처리

| 메시지 | 처리 |
|---|---|
| 원격보다 뒤처짐 | GitHub Desktop에서 Fetch/Pull |
| 원격보다 앞섬 | 다른 PC와 공유할 작업인지 확인 후 사용자가 Push |
| 작업 트리 변경 | 자동 삭제하지 말고 변경 소유권 확인. 의도한 작업이면 `-RequireClean` 없이 상태만 점검 |
| LFS 본문 미수신 | `git lfs pull origin main` 재실행 |
| Engine 파일 없음 | 실제 UE 5.8 설치 경로를 `-EngineRoot`에 전달 |
| Unreal Process | Editor 저장·종료 후 재실행 |
| Tutorial Validation 실패 | 출력된 `Saved/Automation/TutorialMissionTestSetup/.../Setup.log` 확인 |

## 5. Codex에서 시작하는 방법

작업컴 Codex에서 프로젝트 루트를 `D:\JGY\project\drone`으로 연다. 첫 메시지는 다음처럼 사용한다.

```text
D:\JGY\project\md\WORK_PC_START_HERE.md,
D:\JGY\project\md\CONTEXT.md,
D:\JGY\project\md\STATUS.md,
D:\JGY\project\md\WORKBOARD.md를 먼저 읽고 현재 Git 상태와 대조해.
Production /Game/Drone/Maps/Lvl_DroneTraining은 저장하거나 재구성하지 말고,
테스트는 /Game/Drone/Maps/TestMap에서 진행해.
커밋과 푸시는 내가 요청하기 전에는 하지 마.
우선 FrontEnd 뒤로가기/패드 입력, 독립 Tutorial/Orbit/Racing·Story 4개 수동 완주 상태를 확인하고 WORKBOARD Next 순서대로 이어가.
```

과거 대화 전체를 다시 설명할 필요는 없다. 위 네 문서와 실제 저장소 상태가 현재 기준이다.

## 6. 가장 먼저 열 맵과 수동 확인

통합 흐름은 `/Game/Drone/Maps/Lvl_DroneFrontEnd`에서 Play한다. 시작→Story4, 훈련→Tutorial9/Racing1, 설정의 적용/취소·재실행 복원·실제 음량을 확인한다. 창 모드/해상도는 PIE에서 비활성화되므로 Standalone을 사용한다. 설명→기체 선택→출격과 버튼/Esc/패드 Back 및 아래 8수업은 별도 완주한다. 독립 Tutorial 8·Story4·Racing1은 직접 Play도 가능하다.

1. Hover: Zone 안에서 3초 안정 유지 후 귀환
2. Forward: 전방 Trigger 통과 후 귀환
3. Orbit(기존 Heading ID): 원형 코스 Gate 0 → 1~7 → 결승 8 한 바퀴 후 귀환
4. Gate Flight: Ring 4개를 순서와 정방향으로 통과
5. FPV: Arm 후 체력 100 표적에 충돌
6. Payload: 화물 투하로 표적 적중 후 귀환
7. UGV NPC: 좌클릭 총으로 체력 100 적 NPC 처치
8. UGV Turret: 좌클릭 총 또는 우클릭 유탄으로 고정 표적 파괴

UGV는 `W/S` 전후, `A/D` 조향, `Q/E` 제자리 회전이며 마우스/패드 시점은 차체가 아니라 상부 포탑만 회전시킨다.

## 7. 자동 검증 기준

현재 작업컴 후속 UI 검증: Editor Build 성공, `FrontEndContract / BackNavigationContract / MissionEntryContract / SettingsContract / FrontEndPIE` 5/5·자동화 오류/경고 0. 보고서 `Saved/Automation/TrainingLobbySettings/index.json`. NullRHI/NoSound여서 렌더·가청성·실제 창 설정·디스크 재실행 복원은 미확인이다. 아래는 다른 PC `C:\URproject\drone`의 기존 Oct 1 인계 결과이며 오늘 전체 재실행 결과는 아니다.

- Editor Development Build 성공, Title/Orbit 앞선 회귀 14/14 성공
- GameReadiness 집중 회귀 32/32·오류/경고 0, Tutorial 8 + Story 4 + Racing 1 + 비 비교 1의 Map Check 14맵 0/0
- Hover 로비 PIE와 독립 맵 직접 Play PIE에서 실제 출격→3초 유지→귀환 목표 전환 성공
- Back 후속 회귀 33개 실패 0, 외부 LogHttp 시간 초과 경고 동반 성공 1건
- 1280 UI 일부 상호작용·뒤로가기/선택 복원, 1920 제목/Exit 확인. 전체 미션 완주·실제 패드·최종 음원/연출은 미확인
- 오늘 작업컴 기본 준비 점검 0/0은 위 런타임 결과와 별도다. `-game` Toolset Python 환경 오류도 프로젝트 집중 테스트 실패와 구분한다

이전 전체 `Drone.*` 결과는 **51개 성공/7개 실패**였다. 최신 집중 회귀로 전체 회귀가 전부 Green이라고 판정하지 않는다. 당시 7개 실패는 다음과 같으며 Production을 재구성해 억지로 통과시키지 않는다.

- NPC Greybox 시험이 예전의 정확한 Actor 수를 기대하는 항목
- Shotgun PIE에서 활성 Drone 표적을 잡지 못하는 항목
- 팀원 소유 Production Training 맵에 예전 Course/Gate가 있다고 가정하는 항목

Production 맵을 자동 재구성해서 테스트를 억지로 통과시키지 않는다. 상세 내용은 `docs/gameplay/DRONE_CODE_STRUCTURE_AUDIT_2026-09-29.md`를 본다.

## 8. 바로 이어갈 실제 작업

최신 구현은 이미 수신됐다. 다른 PC의 자동화와 일부 화면 확인을 인계받았지만 현재 PC의 전체 미션 체감은 미확인이다. 이미지 교체법과 Mode 1/2는 [가이드](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md), 실제 우선순위는 `WORKBOARD.md`를 따른다.

우선순위는 다음과 같다.

1. FrontEnd 뒤로가기/탭 복원·패드 입력, 독립 Tutorial 8개·Orbit/Racing·Story 4개 수동 완주와 실패/결과를 확인한다.
2. Best Lap SaveGame을 조건별로 저장·복원하고 저장 없음/구버전/손상 처리를 검증한다.
3. Tutorial 브리핑·클리어 타임·재시도/다음 수업·`n/8`·전체 완료 UI를 추가한다.
4. Story M1 선택 목표/실패 → M2 Story Fact → M3 기체 교대 → M4 장거리 타격/엔딩을 고도화한다.
5. 관련 단계의 회귀로 Gate 음원/Mesh/재질·1/6 배치, Physics 벽/그물 카메라 안정성과 총알 Shake 유지, FPV/Drop 하중·Mode 1/2·AI/Shotgun·비/광섬유/UGV를 확인한다. 발견된 수치는 BP에서 조정한다.
6. 별도 Spike로 실제 Dataflow/Chaos Cloth·Geometry Collection을 Greybox와 비교한다. 최종 Niagara/젖음/Audio·영상/UI·패키징은 후속이다.

아직 최종값으로 확정하지 않은 항목은 `STATUS.md`와 `WORKBOARD.md`에서 계속 미정으로 유지한다.

## 9. 종료할 때

1. Unreal 저장 후 Editor 종료
2. Build 또는 관련 집중 자동화 실행
3. `git diff --check`
4. `STATUS.md`, `WORKBOARD.md`, 필요하면 `DRONE_WORKLOG.md` 갱신
5. GitHub Desktop에서 두 저장소 변경을 사용자가 검토
6. 사용자가 요청한 경우에만 Commit·Push

PC 간 전달에는 Git/GitHub와 검토 가능한 Markdown만 사용한다. 인증 파일과 원시 Codex 세션 데이터는 복사하지 않는다.
