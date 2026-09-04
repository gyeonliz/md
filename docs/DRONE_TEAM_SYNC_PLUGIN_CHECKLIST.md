# Drone 팀원 Git·LFS·Unreal Plugin 동기화 체크리스트

기준일: 2026-09-04 (Asia/Seoul)

## 확인된 기준

- 중앙 저장소: `https://github.com/gyeonliz/drone.git`, `main=6fd0e77`
- 별도 원격 참고: `https://github.com/Yook34/drone.git`, `main=c845430`, 중앙보다 `18 Commit 뒤 / 0 Commit 앞`
- 사용자가 확인한 실제 팀 협업 경로는 권한을 받은 중앙 `gyeonliz/drone` 직접 Pull이다. 위 별도 원격 상태를 팀원 PC 상태로 간주하지 않는다.
- 차이는 총 586개 파일이며 Content 520개, Source 61개가 포함된다.
- 두 Head의 `Drone.uproject`와 `Plugins` 차이는 0이다.
- Project `Plugins` 폴더와 Git Submodule은 없다.
- 기준 Unreal은 **UE 5.8.1, Changelist 56057345**다.
- LFS Package는 4,563개이며 중앙 작업컴의 Pointer 검사가 통과했다.
- 필수 입력 영역의 Git Untracked/Ignore 파일과 외부 Junction/Symlink는 0개다.
- 별도 Clean Worktree에서 `Binaries`·`Intermediate` 없이 Editor Source Build가 성공했다.

따라서 팀원 PC에서 기능·맵·Blueprint가 다르면 Plugin 복사보다 먼저 **실제 HEAD, LFS 본문, C++ 재빌드**를 확인한다.

### 사격 모션·기관총 중앙 기준

중앙 `6fd0e77`에는 다음 파일이 모두 들어 있다.

- `Content/Drone/AI/Animation/ABP_NPC_Rifle_Greybox.uasset`
- `Content/Drone/AI/Animation/BS_NPC_Rifle_Locomotion.uasset`
- `Source/Drone/AI/Animation/DroneNPCAnimInstance.cpp`
- `Source/Drone/AI/DroneMGTurretStation.cpp/.h`
- `Source/Drone/AI/DroneNPCMGTurretStateTreeTasks.cpp`

중앙의 실제 파일 크기는 `ABP_NPC_Rifle_Greybox` 473,761 bytes, `BS_NPC_Rifle_Locomotion` 49,269 bytes, `BP_SO_MGTurret` 26,966 bytes다. 팀원 PC 파일이 약 130 bytes의 LFS Pointer이거나 파일이 없으면 LFS 수신 문제다. Source와 Asset이 모두 있는데 기능이 없으면 Git 제외 대상인 `Binaries/Win64/UnrealEditor-Drone.dll`이 Pull 전 버전일 가능성을 먼저 본다.

팀원 PC의 중앙 Clone 루트에서 다음을 실행하면 세 경우를 구분할 수 있다.

```powershell
git remote -v
git branch --show-current
git rev-parse --short HEAD
git status --short
git lfs status
Get-Item Content\Drone\AI\Animation\ABP_NPC_Rifle_Greybox.uasset,
  Content\Drone\AI\Animation\BS_NPC_Rifle_Locomotion.uasset,
  Content\Drone\AI\SmartObjects\Blueprints\BP_SO_MGTurret.uasset |
  Select-Object FullName, Length, LastWriteTime
Test-Path Source\Drone\AI\DroneMGTurretStation.cpp
Test-Path Source\Drone\AI\Animation\DroneNPCAnimInstance.cpp
Get-Item Binaries\Win64\UnrealEditor-Drone.dll -ErrorAction SilentlyContinue |
  Select-Object FullName, Length, LastWriteTime
```

## 팀원 PC 동기화 순서

Unreal Editor와 Visual Studio를 먼저 종료하고 팀원 Clone 폴더에서 실행한다.

```powershell
git status --short
git remote -v
git branch --show-current
git fetch --all --prune
git log -1 --oneline origin/main
```

작업 파일이 있으면 Pull 전에 Commit하거나 별도 Branch로 보존한다. 깨끗한 상태이고 `origin`이 중앙 저장소라면 다음을 실행한다.

```powershell
git switch main
git pull --ff-only origin main
git lfs install
git lfs pull origin main
git rev-parse --short HEAD
git status --short
```

마지막 Commit은 `6fd0e77`, 상태 출력은 비어 있어야 한다.

팀원 Clone의 `origin`이 `Yook34/drone`이라면 중앙을 `upstream`으로 추가하고 중앙 기준으로 Fast-forward한다.

```powershell
git remote add upstream https://github.com/gyeonliz/drone.git
git fetch upstream
git switch main
git merge --ff-only upstream/main
git lfs pull upstream main
```

그 다음 팀원 Fork도 최신화하려면 팀원이 직접 `git push origin main`을 실행한다.

## Unreal 재생성·빌드

1. Epic Games Launcher에서 Unreal Engine 버전이 `5.8.1`인지 확인한다.
2. `Drone.uproject` 우클릭 → `Generate Visual Studio project files`를 실행한다.
3. `DroneEditor Win64 Development`를 Build한다.
4. `Drone.uproject`를 열고 Output Log에서 `Plugin failed`, `Failed to load /Script`, `Unknown Class`, `Failed to load package`를 검색한다.
5. `Lvl_NPCSmartObjectGreybox`, `Lvl_DroneTraining`, `Lvl_MilitaryBase`를 각각 열어 Blueprint·Map 오류를 확인한다.

`Binaries`, `Intermediate`, `Saved`, `DerivedDataCache`는 Git에 공유하지 않는 생성 폴더다. PC별로 내용이 다른 것이 정상이며, 소스 동기화 뒤 컴파일 문제가 있을 때만 Editor를 닫고 해당 생성물을 재생성한다. `Content`, `Config`, `Source`, `Drone.uproject`는 공유 대상이다.

특히 `Binaries/Win64/UnrealEditor-Drone.dll`은 Git에 올라가지 않는다. 따라서 C++ 변경을 Pull한 뒤 Build하지 않으면 팀원 PC의 기존 DLL이 남아 옛 기능이 실행되거나 `Drone could not be compiled`가 나타날 수 있다. Pull 성공과 기능 적용 완료를 같은 것으로 취급하지 말고 Editor Build 성공까지 확인한다.

## Plugin 기준

`Drone.uproject`가 직접 활성화한 것은 UE 5.8.1에 포함된 Engine Plugin이다.

- Runtime: `StateTree`, `PropertyBindingUtils`, `GameplayStateTree`, `SmartObjects`, `GameplayInteractions`, `HDRIBackdrop`
- Editor 전용: `ModelingToolsEditorMode`, `ModelContextProtocol`, `EditorToolset`, `AutomationTestToolset`, `UMGToolSet`, `StateTreeToolset`, `AIModuleToolset`

팀원에게 별도로 복사할 Project Plugin 폴더는 현재 없다. 정확히 같은 5.8.1 설치에서 위 Plugin을 찾지 못하면 Epic Games Launcher의 해당 Engine 설치에서 `Verify`를 먼저 실행한다.

추가 확인된 `Fab`은 Epic Launcher가 Engine에 별도로 설치하는 Editor Plugin이다. Project의 Megascans Asset 4개가 `/Script/Fab` 가져오기 메타데이터를 갖고 있다. Fab가 없으면 이 4개에서 재수입 메타데이터 경고가 생길 수 있으므로 팀원 UE 5.8에도 Fab를 설치하는 편이 안전하다. 다만 이미 Commit된 Mesh·Material·Texture 본문과 Drone Runtime 기능 자체는 Git LFS로 받는다.

`ModelContextProtocol`은 Editor 전용이며 기본 설정이 포트 8000 자동 시작이다. 다른 프로그램이 8000번 포트를 사용하면 MCP만 실패할 수 있지만 게임 Runtime 기능에는 영향을 주지 않는다.

Military Map의 Water는 현재 작업컴에서 정상 Mount되고 최근 로그에도 관련 실패가 없다. 중앙 동기화·LFS Pull·5.8.1 일치 뒤에도 Water Class 누락이 재현될 때는 해당 PC 로그를 확보하고 `Water`를 `.uproject`에 직접 명시하는 변경을 검토한다.

## 문제 분류

| 증상 | 우선 확인 |
|---|---|
| 새 AI·기관총·Mission 기능이 없음 | `git rev-parse --short HEAD`가 `6fd0e77`인지 확인 |
| Mesh·Material·Map이 비거나 LFS Pointer처럼 보임 | `git lfs pull origin main` 또는 `git lfs pull upstream main` |
| Pull은 됐는데 C++ 기능이 이전 상태 | Editor 종료 → Project Files 재생성 → `DroneEditor Win64 Development` Build. `Binaries`는 공유되지 않음 |
| `Drone could not be compiled` | UE 5.8.1과 MSVC Toolchain 확인 → Project Files 재생성 → `DroneEditor` Build |
| Plugin을 찾을 수 없음 | Engine 5.8.1 설치 Verify, Plugin 이름과 Error Log 확보 |
| Fab 관련 Import Data 경고 | UE 5.8용 Fab Plugin 설치. Runtime 기능 문제와 분리 |
| MCP 연결만 실패 | 포트 8000 충돌 확인. 게임 기능 문제와 분리 |
| Editor 배치·최근 Map·캐시만 다름 | `Saved`·`DerivedDataCache`는 PC별 로컬 상태이므로 정상 |

팀원 화면이 계속 다르면 추측으로 폴더를 복사하지 말고 아래 네 결과와 Unreal 오류 한 줄을 함께 전달한다.

```powershell
git remote -v
git branch --show-current
git rev-parse --short HEAD
git status --short
```
