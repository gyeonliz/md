# 작업컴 시작 가이드

기준일: 2026-09-29 (Asia/Seoul)

이 문서는 작업컴 `D:\JGY\project\md`와 `D:\JGY\project\drone`에서 현재 Drone 작업을 바로 이어가기 위한 단일 시작점이다. 최신 구현 사실은 `STATUS.md`, 다음 작업은 `WORKBOARD.md`, 변경 금지 경계는 `CONTEXT.md`를 우선한다.

## 1. 현재 인계 상태

- 인계 준비 시점 Unreal 원격 기준: `main = origin/main = 19c86692f904914a3e913ed4483d1e83ec2eb87d`
- 인계 준비 시점 문서 원격 기준: `main = origin/main = e34ef4f30f46b785477573e6d3193303272bd94c`
- 위 Commit 이후 Tutorial 8개 Mission, 공유 시험맵, Heading 판정, UGV 총·유탄, NPC 걷기 자산, FrontEnd Mission 목록과 문서 변경을 메인컴 로컬에서 준비했다.
- 이 인계 문서를 작성할 때 Codex는 Commit·Push하지 않았다. 사용자가 이후 두 저장소를 Push해야 작업컴이 같은 상태를 받을 수 있다.
- 이미 작업컴에서 이 문서를 Pull해 읽고 있다면 4절 점검 결과를 우선한다. 두 저장소가 원격과 일치하고 필수 Asset 검사가 통과하면 전달이 완료된 상태다.
- Codex 원시 세션 폴더, `auth.json`, API Key, 토큰은 복사하지 않는다.

## 2. 메인컴을 떠나기 전 사용자 작업

Unreal Editor와 실행 중인 명령줄 Editor를 모두 종료한다. 그다음 GitHub Desktop에서 아래 순서로 처리한다.

### 2-1. Unreal 저장소

1. 저장소 `gyeonliz/drone`을 선택한다.
2. 변경 목록에 `Source/Drone`, `Tools/AssetMigration`, `/Game/Drone/Mission`, Tutorial Mission Data Asset 8개, `Lvl_DroneTutorialMissionTest`가 포함됐는지 확인한다.
3. Commit 제목 예시: `튜토리얼 8개 미션 테스트맵과 UGV 무장 구현`
4. Commit 후 `Push origin`을 누른다.
5. Git LFS 업로드가 끝날 때까지 GitHub Desktop을 닫지 않는다.

### 2-2. 문서 저장소

1. 저장소 `gyeonliz/md`를 선택한다.
2. `WORK_PC_START_HERE.md`, `STATUS.md`, `WORKBOARD.md`, `CONTEXT.md`, `docs`, `tools/work-pc` 변경을 확인한다.
3. Commit 제목 예시: `작업컴 인계 문서와 튜토리얼 가이드 최신화`
4. Commit 후 `Push origin`을 누른다.

사용자가 Commit·Push하기 전까지 Codex는 현재 변경을 작업컴으로 전달할 수 없다. `git lfs push`만으로는 Commit이 GitHub 이력에 올라가지 않으므로 GitHub Desktop의 `Push origin`까지 성공해야 한다.

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

마지막 줄이 `WORKSTATION_READY`면 다음 단계로 간다. 실행 정책은 이 명령 한 번에만 우회하며 시스템 전체 정책을 변경하지 않는다.

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
우선 FrontEnd에서 Tutorial 8개 수동 검증 준비부터 이어가.
```

과거 대화 전체를 다시 설명할 필요는 없다. 위 네 문서와 실제 저장소 상태가 현재 기준이다.

## 6. 가장 먼저 열 맵과 수동 확인

먼저 `/Game/Drone/Maps/Lvl_DroneFrontEnd`를 Play하고 다음 8개 Mission을 하나씩 선택한다. 공유 시험맵을 직접 Play하면 선택 Mission이 없으므로 전체 Director 흐름 검증에는 적합하지 않다.

1. Hover: Zone 안에서 3초 안정 유지 후 귀환
2. Forward: 전방 Trigger 통과 후 귀환
3. Heading: 동쪽 90° ±8°를 1초 유지 후 귀환
4. Gate Flight: Ring 4개를 순서와 정방향으로 통과
5. FPV: Arm 후 체력 100 표적에 충돌
6. Payload: 화물 투하로 표적 적중 후 귀환
7. UGV NPC: 좌클릭 총으로 체력 100 적 NPC 처치
8. UGV Turret: 좌클릭 총 또는 우클릭 유탄으로 고정 표적 파괴

UGV는 `W/S` 전후, `A/D` 조향, `Q/E` 제자리 회전이며 마우스/패드 시점은 차체가 아니라 상부 포탑만 회전시킨다.

## 7. 자동 검증 기준

현재 메인컴에서 확인한 기준은 다음과 같다.

- `DroneEditor Win64 Development` Build 성공
- Tutorial Mission TestMap Rebuild/Validate Map Check `0 errors / 0 warnings`
- 새 Mission 집중 회귀 9/9 성공
- 전체 `Drone.*`는 51개 성공, 별도 기준선 7개 실패

7개 실패는 새 Tutorial 기능 실패로 묶지 않는다.

- NPC Greybox 시험이 예전의 정확한 Actor 수를 기대하는 항목
- Shotgun PIE에서 활성 Drone 표적을 잡지 못하는 항목
- 팀원 소유 Production Training 맵에 예전 Course/Gate가 있다고 가정하는 항목

Production 맵을 자동 재구성해서 테스트를 억지로 통과시키지 않는다. 상세 내용은 `docs/gameplay/DRONE_CODE_STRUCTURE_AUDIT_2026-09-29.md`를 본다.

## 8. 바로 이어갈 실제 작업

우선순위는 다음과 같다.

1. FrontEnd에서 Tutorial 8개를 손으로 플레이하고 Trigger 위치·Heading 허용각·Gate 방향·총탄 속도·유탄 낙차를 기록한다.
2. 발견된 수치 문제만 Blueprint 또는 노출된 기본값에서 조정하고 8개 독립 Mission 계약은 유지한다.
3. 단계별 브리핑·클리어 타임 UI를 추가한다.
4. 8개 연속 진행과 전체 완료 UI를 연결한다.
5. 팀원 맵 소유권을 확인한 뒤 Warehouse Greybox 환경을 별도로 구성한다.
6. Tutorial 확인 뒤 Mission 1 Story Vertical Slice를 만든다.

아직 최종값으로 확정하지 않은 항목은 `STATUS.md`와 `WORKBOARD.md`에서 계속 미정으로 유지한다.

## 9. 종료할 때

1. Unreal 저장 후 Editor 종료
2. Build 또는 관련 집중 자동화 실행
3. `git diff --check`
4. `STATUS.md`, `WORKBOARD.md`, 필요하면 `DRONE_WORKLOG.md` 갱신
5. GitHub Desktop에서 두 저장소 변경을 사용자가 검토
6. 사용자가 요청한 경우에만 Commit·Push

PC 간 전달에는 Git/GitHub와 검토 가능한 Markdown만 사용한다. 인증 파일과 원시 Codex 세션 데이터는 복사하지 않는다.
