# 작업컴 시작 가이드

기준일: 2026-10-04 (Asia/Seoul)

최신 상태는 STATUS·WORKBOARD가 기준이며 아래 일부 문단은 당시 기록이다. 아래 D 경로 명령은 **D PC 예시**다. Build·PIE·자동화 테스트는 Claude 담당이다.

이 문서는 PC를 옮겨 Drone 작업을 이어가기 위한 단일 시작점이다. 현재 C 드라이브 PC는 Unreal `C:\URproject\drone`, 문서는 이 작업 폴더이며 이전 D 드라이브 작업컴 경로는 `D:\JGY\project\md`/`drone`다. 아래 D 경로 명령은 해당 작업컴용 예시이므로 다른 PC에서는 실제 경로로 바꾼다. 최신 사실은 `STATUS.md`, 다음 작업은 `WORKBOARD.md`, 경계는 `CONTEXT.md`를 우선한다.

## 1. 현재 인계 상태

최신 해시·미커밋 범위는 [STATUS Git 기준 표](STATUS.md)를 따른다. 현재 C PC Unreal C:\URproject\drone에는 10/02~10/04 코드·입력·UI·도구의 로컬 미커밋/미추적이 있으므로 원격 수신만으로 전달 완료를 판단하지 않는다. PC 이동 전 사용자가 변경을 검토하고 공유할 때만 Commit/Push한다. 소스 수신과 최신 바이너리·수동 플레이 Pass는 구분한다. Lvl_BangkokCity는 10/01 의도적으로 삭제됐으며 남은 의존 자산 정리 여부는 미정이다.

이전 D PC Build/UI5/5(NullRHI/NoSound)·목록 렌더 Fail의 원시 TrainingLobbySettings 보고서는 현재 C PC에 없다. 최신 검증은 STATUS를 따른다. 인증 파일·API 키·원시 세션을 복사하지 않는다.

## 2. 새 변경을 공유할 때의 사용자 작업

해시·미커밋 범위는 STATUS Git 기준 표를 따른다. 사용자가 공유를 결정한 경우 GitHub Desktop에서 drone·md 변경을 각각 검토한 뒤 Commit/Push하고 LFS 업로드 완료를 확인한다. Saved 보고서는 Git 제외이므로 필요한 검사명·날짜·PC·수치만 전달한다. Codex는 별도 요청 없이 Commit/Push하지 않는다.

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

## 5. Claude Code에서 시작하는 방법

코드·Build·테스트는 Claude Code가 Unreal 저장소의 CLAUDE.md와 WORKBOARD Next를 따라 수행한다. 문서는 Codex가 맡는다. Claude 허브가 Codex를 docs/ui/image 역할 지시서로 한 번에 하나씩 호출하고 결과를 검증한다. 문서 경로는 각 PC .claude/codex-bridge/local.json의 mdRepo를 사용한다. Production Lvl_DroneTraining 편집·저장은 맵 소유 팀원만, 기능 검증은 TestMap이다.

새 PC 협업 세팅(실제 Unreal 경로로 바꿔 실행):

```powershell
C:\URproject\drone\.claude\codex-bridge\Test-CollabSetup.ps1 -WriteLocalConfig -InstallUserRules
```

전체 절차는 [CLAUDE_CODEX_SETUP](docs/git/CLAUDE_CODEX_SETUP.md)을 따른다. 이 문서 최신화에서는 세팅·Build·테스트를 실행하지 않았다.

## 6. 가장 먼저 열 맵과 수동 확인

통합 흐름은 `/Game/Drone/Maps/Lvl_DroneFrontEnd`에서 Play한다. 타이틀 스토리/레이싱/튜토리얼/설정/종료 5메뉴→분류 직접 진입(로비 Tutorial/Racing 탭·LB/RB는 현재 유지, 최종 유지 여부 미정), 설정의 적용/취소·재실행 복원·실제 음량을 확인한다. 창 모드/해상도는 PIE에서 비활성화되므로 Standalone을 사용한다. 설명→기체 선택→출격과 버튼/Esc/패드 Back 및 아래 8수업은 별도 완주한다. 독립 Tutorial 8·Story4·Racing1은 직접 Play도 가능하다.

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

최신 검사명·조건·수치·로그는 STATUS 검증 표를 따른다(10/04 C PC Claude 실행). 새벽12/12·90/94와 후속 집중30/32·전체95개2회는 각각 다른 실행이다. 최신 전체2회는 PIE 미렌더여서 패드 포커스6개 판정 제외, 나머지 알려진4개 Fail. 화면 그려진 실행의 포커스 확인은 대기다.

이전 D PC UI5/5(NullRHI/NoSound)·Build 성공은 당시 문서 근거이고 Saved/Automation/TrainingLobbySettings/index.json은 C PC에 없다. C PC Saved의 10/01 기존 GameReadiness32 Success·Back32 Success+경고 동반 성공1·TitleLobbyOrbit14 Success는 최신 UI 이전 검사다. 다른 PC 결과를 현재 PC의 수동 Pass로 확대하지 않는다. Production 맵 의존 Fail을 맵 저장/재구성으로 통과시키지 않는다.

## 8. 바로 이어갈 실제 작업

[WORKBOARD Next](WORKBOARD.md)를 따른다. Acro Mode1에서 스틱에 엄지를 걸친 채 Space→상승, 키 해제→패드 인계와 코스 급커브 표시·Editor 편집 체감을 먼저 수동 확인한다. 5메뉴·포커스·입력 표시·8수업·Best Lap 실제 재실행 복원도 수동 대기다. 미정 수치·기본값·레이싱/스토리 결정은 사람이 정한다.

## 9. 종료할 때

1. Unreal 저장 후 Editor 종료
2. Build 또는 관련 집중 자동화 실행
3. `git diff --check`
4. `STATUS.md`, `WORKBOARD.md`, 필요하면 `DRONE_WORKLOG.md` 갱신
5. GitHub Desktop에서 두 저장소 변경을 사용자가 검토
6. 사용자가 요청한 경우에만 Commit·Push

PC 간 전달에는 Git/GitHub와 검토 가능한 Markdown만 사용한다. 인증 파일과 원시 Codex 세션 데이터는 복사하지 않는다.
