# Unreal Engine + Git/GitHub 실전 작업 가이드

이 문서는 기존 Unreal Engine 프로젝트를 Git/GitHub에 안전하게 연결하고, 메인컴·작업컴 또는 팀원 간에 같은 프로젝트를 이어서 작업하기 위한 기준 절차다.

## 0. 현재 기준과 미정 사항

- 사용자가 밝힌 프로젝트 기준 버전은 **Unreal Engine 5.8.1**이다.
- 작업컴의 설치 식별자는 **`UE_5.8`**이며, 당시 `Build.version`에서 `MajorVersion=5`, `MinorVersion=8`, `PatchVersion=1`을 확인했다. 따라서 작업컴 설치본은 **UE 5.8.1로 검증됨** 상태다.
- 이번 확인 PC도 `C:\Program Files\Epic Games\UE_5.8\Engine\Build\Build.version`에서 UE 5.8.1, Changelist 56057345를 확인했고 실제 프로젝트의 `EngineAssociation`은 `5.8`이다.
- 다만 `UE_5.8` 폴더명이나 `.uproject`의 `EngineAssociation` 값만으로 패치 버전을 판정해서는 안 된다. 이번 확인 PC를 메인컴 또는 작업컴 중 어느 역할로 부를지는 이 문서에서 임의로 정하지 않으므로, 메인컴 설치 버전과 두 PC 일치 판정은 PC 역할을 확인한 뒤 닫는다.
- 실제 Drone GitHub 저장소는 **`gyeonliz/drone`**으로 확정했다.
- GitHub 저장소 공개 범위(Public/Private)는 **현재 미정**이다.
- 기본 Drone 작업 경로는 `D:\JGY\project\drone`이고 문서 경로는 `D:\JGY\project\md`다. 다른 PC의 검증 Clone `C:\URproject\drone`도 별도 기록으로 보존한다. 현재 중앙 main은 `2fcfb04`이며 AI-FRIEND-01까지 병합·Push했다. Game/Editor Build, AI 7/7, 전체 `Drone.` 23/23, Blueprint 0/0/0, 환경 맵 검증과 LFS fsck를 통과했다. 프로젝트 사용 맵과 환경 중앙 사본은 `/Game/Drone/Maps`에 있고 Unreal 생성 기본 Map 4개만 제거했다. 실제 코드 구조와 사용자 확인 작업은 [`DRONE_CODE_STRUCTURE_AND_USER_TASKS.md`](DRONE_CODE_STRUCTURE_AND_USER_TASKS.md)를 따른다. 다른 PC Pull/LFS/UE 실행 검증은 아직 남았다.
- 사용자는 현재 Drone 프로젝트에서 Android를 사용하지 않는다고 확정했다. 기준 Drone 프로젝트에서는 Android File Server Plugin과 네트워크 연결을 끄고 `SecurityToken`을 빈 할당으로 정리했다.
- 아래 브랜치 구조는 현재 컨텍스트에 맞춘 권장 시작안이며, 최종 팀 규칙으로 확정된 것은 아니다.
- 이 가이드는 명령줄 Git을 기준으로 한다. Unreal Editor 안의 Git 플러그인 제공 여부와 동작은 실제 UE 5.8 환경에서 확인하기 전까지 전제하지 않는다.

> 중요: Git은 Unreal 프로젝트 파일을 공유한다. Codex/GPT 대화·세션·작업 문맥 동기화는 별도 절차로 관리한다.

## 1. 가장 먼저 지킬 원칙

1. 저장소 루트는 `.uproject` 파일이 있는 폴더로 잡는다.
2. `.gitignore`와 `.gitattributes`를 **첫 `git add`보다 먼저** 적용한다.
3. `.uasset`과 `.umap`은 Git LFS로 추적한다.
4. `Content/`, `Config/`, `Source/`, `.uproject`는 커밋한다.
5. `Intermediate/`, `Saved/`, `DerivedDataCache/`는 커밋하지 않는다.
6. `Binaries/`와 IDE 생성 파일도 기본적으로 커밋하지 않고 각 PC에서 다시 만든다.
7. `.uasset`과 `.umap`은 바이너리다. Git LFS는 저장 방식을 개선할 뿐, 두 사람의 변경을 자동 병합하지 않는다.
8. 같은 Asset이나 Level을 여러 사람이 동시에 수정하지 않는다.
9. Pull, 브랜치 전환, 충돌 해결 전에는 Unreal Editor를 닫는다.
10. 공유 브랜치에서는 `push --force`, `reset --hard`, `clean -fdx`를 기본 작업으로 사용하지 않는다.

## 2. Git에 넣을 것과 제외할 것

### 커밋할 항목

- `ProjectName.uproject`
- `Config/`
- `Content/`
- `Source/`
- 프로젝트에서 직접 관리하는 `Plugins/`
- 프로젝트에서 직접 관리하는 `Build/`의 아이콘·설정 등
- `.gitignore`
- `.gitattributes`
- 프로젝트 문서

`Plugins/` 안에서도 각 플러그인의 `Binaries/`와 `Intermediate/`는 기본적으로 제외한다. 소스 없이 바이너리로만 공급되는 외부 플러그인은 라이선스와 배포 방식이 다를 수 있으므로 예외 규칙을 팀이 별도로 결정한다.

### 제외할 항목

- `Binaries/`
- `Intermediate/`
- `Saved/`
- `DerivedDataCache/`
- `.vs/`
- 생성 가능한 Visual Studio 솔루션(`.sln`, `.slnx`)과 사용자 설정 파일
- 로그, 임시 파일, OS 메타데이터

이 저장소의 재사용 템플릿은 다음 두 파일이다.

- `templates/unreal/.gitignore`
- `templates/unreal/.gitattributes`

기존 프로젝트에 이미 같은 파일이 있다면 덮어쓰지 말고 규칙을 비교하여 병합한다.

## 3. Windows에서 Git과 Git LFS 설치 확인

PowerShell 또는 Git Bash의 새 터미널을 열고 확인한다.

```powershell
git --version
git lfs version
```

두 명령 모두 버전이 출력되면 설치 단계는 통과다. 정확한 버전 번호 자체를 이 문서에서 고정하지 않는다.

### Git이 없을 때

공식 Git for Windows 설치 프로그램을 사용하거나 Windows 패키지 관리자를 사용한다.

```powershell
winget install --id Git.Git -e --source winget
```

설치 후 기존 터미널을 닫고 새 터미널에서 다시 `git --version`을 실행한다.

### Git LFS가 없을 때

Git LFS는 Git과 별도 프로그램이다. Git for Windows 설치에 포함되어 있을 수 있으므로 먼저 `git lfs version`으로 확인한다. 없을 때만 공식 Git LFS 설치 프로그램을 사용하거나 다음 패키지를 설치한다.

```powershell
winget install --id GitHub.GitLFS -e --source winget
```

그 후 새 터미널에서 사용자 계정 단위 초기화를 한 번 실행한다.

```powershell
git lfs install
git lfs version
```

### Git 사용자 정보 설정

아래 값은 예시가 아니라 본인의 GitHub 표시 이름과 커밋 이메일로 교체한다. 비밀번호나 Personal Access Token을 입력하면 안 된다.

```powershell
git config --global user.name "YOUR_NAME"
git config --global user.email "YOUR_EMAIL"
git config --global init.defaultBranch main
git config --global --list
```

GitHub 이메일 공개를 원하지 않으면 GitHub가 제공하는 `noreply` 이메일 사용 여부를 계정 설정에서 결정한다.

## 4. Unreal 버전 먼저 확인

프로젝트를 Git에 올리기 전에 메인컴과 작업컴이 같은 Unreal 버전을 쓸 수 있는지 확인한다.

1. Epic Games Launcher의 Library에서 설치된 엔진 버전을 확인한다.
2. 필요하면 `UnrealEditor.exe` 파일 속성의 세부 정보를 확인한다.
3. `.uproject`를 텍스트로 열어 `EngineAssociation` 값을 확인한다.
4. 두 PC의 결과를 기록한다.

현재 확인 상태는 다음과 같다.

| 항목 | 현재 상태 |
| --- | --- |
| 프로젝트 기준 | UE 5.8.1이라고 전달받음 |
| 작업컴 설치 식별자 | `UE_5.8` |
| 작업컴 `Build.version` | 5.8.1 확인 완료 |
| 이번 확인 PC `Build.version` | 5.8.1, Changelist 56057345 확인 완료 |
| 메인컴 설치 버전 | 아직 확인 필요 |
| 실제 프로젝트 `EngineAssociation` | `D:\JGY\project\drone\Drone.uproject`와 다른 PC `C:\URproject\drone\Drone.uproject`에서 `5.8` 확인 |

작업컴과 이번 확인 PC의 엔진 패치 버전, 이번 확인 PC의 실제 프로젝트 `EngineAssociation`은 확인했다. 이번 확인 PC의 메인컴/작업컴 역할과 나머지 PC 설치 버전을 확인해 두 PC 일치 여부를 닫기 전에는 프로젝트 연결 버전을 임의로 바꾸거나 버전 변경으로 생성된 `.uproject` 수정사항을 커밋하지 않는다.

## 5. GitHub 저장소 생성

현재 Drone 저장소 이름은 `gyeonliz/drone`으로 확정했고 생성·첫 Push까지 완료했다. 공개 범위는 아직 미정이므로 팀 프로젝트와 미공개 경진대회 자료를 고려해 별도로 확인한다. 아래 절차는 새 저장소를 다시 만들 때의 기준으로 유지한다.

GitHub 웹에서 새 저장소를 만들 때 기존 로컬 프로젝트를 처음 연결할 예정이라면 다음처럼 만든다.

1. Owner를 선택한다.
2. Repository name을 입력한다. 현재 Drone 프로젝트는 `drone`을 사용한다.
3. Public 또는 Private를 선택한다. 현재 공개 범위는 미정이다.
4. `Add a README file`을 선택하지 않는다.
5. `.gitignore` 템플릿을 GitHub에서 추가하지 않는다.
6. License도 첫 연결 단계에서는 추가하지 않는다.
7. 빈 저장소를 생성한다.

빈 저장소로 만드는 이유는 로컬 첫 커밋과 GitHub의 자동 생성 커밋이 갈라지는 상황을 피하기 위해서다. 이미 README 등이 있는 원격 저장소라면 강제로 덮어쓰지 말고, 먼저 그 저장소를 Clone한 뒤 프로젝트 파일을 옮기는 별도 절차를 사용한다.

GitHub 인증에는 계정 비밀번호를 Git 명령에 직접 쓰지 않는다. Git Credential Manager의 브라우저 로그인, SSH 키, 또는 별도 승인된 인증 방법을 사용한다. 토큰을 프로젝트 파일이나 명령 기록에 남기지 않는다.

## 6. 기존 Unreal 프로젝트를 로컬 Git 저장소로 만들기

### 6.1 사전 안전 확인

1. Unreal Editor와 Visual Studio를 닫는다.
2. 중요한 미커밋 프로젝트라면 현재 폴더를 별도 위치에 한 번 백업한다.
3. `.uproject`가 있는 프로젝트 루트로 이동한다.

```powershell
$ProjectRoot = "D:\UnrealProjects\YOUR_PROJECT"
Set-Location -LiteralPath $ProjectRoot
Get-ChildItem -LiteralPath . -Filter *.uproject
Get-ChildItem -LiteralPath . -Force -Directory -Filter .git
```

- `.uproject`가 정확히 보여야 한다.
- `.git`이 이미 보이면 새로 초기화하기 전에 `git status`와 `git remote -v`로 기존 저장소인지 확인한다.
- 상위 폴더의 다른 저장소 안에 프로젝트를 중첩해서 만들지 않는다.

### 6.2 템플릿 적용

이 저장소의 `templates/unreal/`에 있는 두 파일을 Unreal 프로젝트 루트로 복사한다.

```text
YOUR_PROJECT/
├─ .gitattributes
├─ .gitignore
├─ YOUR_PROJECT.uproject
├─ Config/
├─ Content/
└─ Source/
```

`Content/`, `Config/`, `Source/`를 무시하는 규칙이 기존 `.gitignore`에 들어 있지 않은지 반드시 확인한다.

### 6.3 저장소 초기화

```powershell
git init -b main
git lfs install
git status
```

`git init -b main`이 지원되지 않는 오래된 Git이라면 Git을 업데이트한다. 프로젝트 작업용 PC끼리는 가능한 한 같은 최신 안정 버전 계열을 사용하는 편이 안전하다.

### 6.4 LFS 규칙 확인

제공된 `.gitattributes`에는 다음 규칙이 들어 있다.

```gitattributes
*.uasset filter=lfs diff=lfs merge=lfs -text
*.umap   filter=lfs diff=lfs merge=lfs -text
```

템플릿을 사용하지 않고 직접 설정해야 할 때는 다음 명령으로 같은 규칙을 만든다.

```powershell
git lfs track "*.uasset"
git lfs track "*.umap"
```

`git lfs track`은 `.gitattributes`를 수정한다. 따라서 `.gitattributes` 자체도 반드시 커밋해야 한다.

등록 상태를 확인한다.

```powershell
git lfs track
git check-attr filter diff merge text -- "Content/Path/Example.uasset"
git check-attr filter diff merge text -- "Content/Path/Example.umap"
```

실제 존재하는 Asset 경로로 바꿔 실행한다. 기대 결과는 `filter`, `diff`, `merge`가 `lfs`이고 `text`가 `unset`인 것이다.

### 6.5 첫 Stage 전 무시 규칙 확인

```powershell
git status --short --ignored
git check-ignore -v "Intermediate" "Saved" "DerivedDataCache" "Binaries"
git add --dry-run .
```

확인할 내용:

- `.uproject`, `Config/`, `Content/`, `Source/`가 추가 대상이다.
- `.gitignore`와 `.gitattributes`가 추가 대상이다.
- `Intermediate/`, `Saved/`, `DerivedDataCache/`, `Binaries/`, `.vs/`는 추가 대상이 아니다.
- 인증 파일, 개인 메모, 비밀번호, API 키가 포함되지 않는다.

### 6.6 Unreal 설정의 보안 값 확인

`Config/DefaultEngine.ini`처럼 반드시 커밋해야 하는 설정 파일에도 Plugin이 만든 보안 값이 들어갈 수 있다. 특히 Android File Server의 `SecurityToken`은 접속에 사용하는 값이며 Epic 문서도 조직 밖에 전달하지 말라고 안내한다. 공개 저장소에는 활성 토큰을 커밋하지 않는다.

값 자체를 출력하지 않고 설정 여부만 확인하는 예:

```powershell
$EngineConfig = Get-Content -LiteralPath '.\Config\DefaultEngine.ini' -Raw
if ($EngineConfig -match '(?m)^SecurityToken=.+$') {
    'Android File Server SecurityToken이 설정되어 있습니다. Commit 전에 처리 방침을 정하세요.'
}
```

Android File Server를 사용하지 않는지, 토큰을 비울지, 비공개 팀 저장소에서 공유할지, 별도 설정으로 관리할지는 프로젝트 요구와 저장소 공개 범위를 확인한 뒤 결정한다. 이미 외부에 노출했다면 기존 값을 다시 사용하지 않고 회전한다. 토큰 값을 Issue, 채팅, Commit 메시지, 로그에 붙여 넣지 않는다.

현재 `D:\JGY\project\drone`에서는 사용하지 않는 것으로 결정되어 `bEnablePlugin=False`, `bAllowNetworkConnection=False`, 빈 `SecurityToken`을 확인했다. 향후 AFS를 다시 켜면 빈 토큰을 유지하지 말고 인증과 노출 범위를 새로 검토한다.

## 7. 첫 Commit

검토가 끝났을 때만 전체 프로젝트를 Stage한다.

```powershell
git add .
git status --short
git diff --cached --stat
git diff --cached --name-only
git lfs status
git lfs ls-files
```

생성 폴더가 Stage되었는지 별도로 확인한다.

```powershell
git diff --cached --name-only | Select-String -Pattern '(^|/)(Binaries|DerivedDataCache|Intermediate|Saved)/'
```

정상이라면 마지막 명령은 아무것도 출력하지 않는다. 출력이 있다면 커밋하지 말고 `.gitignore`와 기존 추적 상태를 먼저 고친다.

`.uasset`과 `.umap`이 실제로 존재한다면 `git lfs ls-files`에 표시되어야 한다. 표시되지 않으면 커밋 전에 LFS 설정을 다시 확인한다.

이후 첫 커밋을 만든다.

```powershell
git commit -m "chore: initialize Unreal project repository"
git status
git log --oneline -n 3
```

정상 결과:

- 현재 브랜치는 `main`이다.
- 작업 트리는 clean이다.
- 첫 커밋이 보인다.
- `Content`의 `.uasset`과 `.umap`은 LFS 추적 목록에 보인다.

## 8. 첫 Push

이 절차는 저장소 최초 생성자가 GitHub에 만든 **빈 중앙 저장소**를 처음 연결할 때만 사용한다. 팀원이 `YOUR_ACCOUNT`에 자기 계정을 넣으면 자기 저장소 또는 Fork가 `origin`이 되며 이후 Push도 그곳으로 간다. 이미 팀 저장소가 있으면 새 저장소를 만들지 말고 아래의 팀 Remote 절차를 사용한다.

```powershell
$RemoteUrl = "https://github.com/YOUR_ACCOUNT/YOUR_REPOSITORY.git"
git remote add origin $RemoteUrl
git remote -v
git push -u origin main
```

첫 Push 중 LFS 업로드 진행률이 별도로 보일 수 있다. Push 후 확인한다.

```powershell
git status
git branch -vv
git lfs ls-files
```

GitHub 웹에서도 다음을 확인한다.

- `.gitignore`와 `.gitattributes`가 보인다.
- `Source/`, `Config/`, `Content/`가 보인다.
- `Intermediate/`, `Saved/`, `DerivedDataCache/`가 보이지 않는다.
- LFS 대상 파일이 일반 바이너리 본문이 아니라 LFS 객체로 연결된다.

GitHub의 Git LFS 저장공간·대역폭·파일 크기 제한은 요금제와 정책에 따라 달라질 수 있다. 대형 원본 영상, 렌더 결과물, 마켓플레이스 원본까지 무조건 넣기 전에 현재 계정의 LFS 사용량과 라이선스를 확인한다.

### 8.1 팀 저장소와 Fork의 Remote 규칙

GitHub Desktop의 **Push origin**과 명령줄의 `git push origin`은 로그인한 계정 이름이 아니라 현재 로컬 저장소에 설정된 `origin`의 Push URL로 보낸다. `user.name`·`user.email`은 Commit 작성자 정보이고 Remote 목적지가 아니다. 먼저 팀원 PC의 실제 Unreal 프로젝트 폴더에서 다음을 확인한다.

```powershell
git status --short
git remote -v
git remote get-url origin
git remote get-url --push origin
git branch -vv
git config --get remote.pushDefault
git config --get branch.main.pushRemote
```

`remote.pushDefault`나 `branch.main.pushRemote`가 출력되면 `origin`과 다른 Push 대상이 지정될 수 있으므로 함께 기록한다. Unreal Editor를 저장·종료하고 작업 트리가 깨끗한 상태에서만 Remote 이름이나 Branch 구조를 바꾼다.

2026-08-28 팀원 변경 인수 전 원격 감사 결과는 다음과 같다.

| 역할 | 저장소 | main |
|---|---|---|
| 중앙 | `https://github.com/gyeonliz/drone.git` | `095dda7` |
| 팀원 Fork | `https://github.com/Yook34/drone.git` | `0ff4fb1` |

`Yook34/drone`은 `gyeonliz/drone`의 Fork이며 Merge Base는 `095dda7`이다. 중앙 전용 Commit은 0개, Fork 전용 Commit은 4개다. 따라서 팀원 PC가 Fork를 Clone해 `origin=Yook34/drone`인 경우 팀원 GitHub에 Push된 것은 정상 동작이다.

이후 팀원 환경 변경은 중앙에 반영됐고 현재 중앙 `main`은 `2fcfb04`다. 위 표는 Push가 사라진 것처럼 보였던 원인을 설명하는 당시 감사 기록이며 최신 기준선으로 사용하지 않는다.

#### 방식 A — Fork + Pull Request

팀원이 중앙 저장소에 직접 쓰기 권한이 없거나 리뷰 후 반영하려면 이 방식을 사용한다. 팀원 Fork는 `origin`, 중앙 저장소는 `upstream`으로 둔다.

```powershell
git remote -v
git remote add upstream https://github.com/gyeonliz/drone.git
git fetch --all --prune
git remote -v
```

이미 `upstream`이 있으면 새로 추가하지 말고 `git remote set-url upstream https://github.com/gyeonliz/drone.git`로 교정한다. 작업 Branch는 중앙 최신 main에서 만들고 팀원 Fork에 Push한 뒤, GitHub에서 `Yook34/drone:feature/...`를 `gyeonliz/drone:main`으로 보내는 Pull Request를 연다.

```powershell
git switch -c feature/yook34-battlefield-assets upstream/main
# 의도한 파일만 작업·검증·Commit
git push -u origin feature/yook34-battlefield-assets
```

#### 방식 B — 중앙을 origin으로 직접 협업

팀원 GitHub 계정이 `gyeonliz/drone` Collaborator로 초대되고 초대를 수락한 경우에만 사용한다. 기존 Fork를 잃지 않도록 먼저 이름을 `fork`로 보존한다.

```powershell
git remote rename origin fork
git remote add origin https://github.com/gyeonliz/drone.git
git fetch --all --prune
git remote -v
```

감사 당시 팀원 로컬 `main`에는 Fork 전용 4 Commit이 있었다. 현재는 먼저 `git fetch --all --prune`과 `git branch -vv`로 실제 상태를 다시 확인하고, 기존 작업 Branch를 보존한 뒤 중앙 최신 `main`에서 새 Feature Branch를 만든다. 아래 이름 변경 예시는 감사 당시 Fork `main`을 보존할 때만 사용한다.

```powershell
git status --short
git branch --show-current
git branch -m main yook34-import-20260828
git switch -c main --track origin/main
git switch -c feature/yook34-battlefield-assets
```

이름을 바꾼 `yook34-import-20260828` Branch에 기존 4 Commit이 남으므로 이력은 삭제되지 않는다. 기능 Branch 검증 후 중앙에 Branch만 Push하고 Pull Request로 병합한다.

```powershell
git push -u origin feature/yook34-battlefield-assets
```

중앙 직접 Push가 403 또는 권한 오류로 거절되면 Remote 문제가 아니라 Collaborator 권한 문제다. 저장소 소유자가 팀원 계정을 초대하거나 방식 A를 사용한다.

### 8.2 현재 팀원 Fork 변경 선별 인수

팀원 Fork의 순 변경에는 다음 항목이 함께 섞여 있다.

- 후보 기능 자산: `Content/Drone/Maps/Lvl_Battlefield.umap`, `Content/Material/M_Enemy.uasset`, `M_Start.uasset`, `M_Target.uasset`
- 인수 제외 기본값: PC별 `.vsconfig`, GUID 형태로 바뀐 `Drone.uproject`의 `EngineAssociation`, `Source/Drone/Drone.cpp`의 `//test`

후보 자산도 의도 확인 전에는 중앙에 반영하지 않는다. 방식 A라면 `upstream/main`, 방식 B라면 `origin/main`에서 만든 깨끗한 Feature Branch에서만 다음 네 파일을 임시 복원해 확인한다. 아래 예시는 방식 A 기준이다.

```powershell
git switch feature/yook34-battlefield-assets
git restore --source=origin/main -- `
  Content/Drone/Maps/Lvl_Battlefield.umap `
  Content/Material/M_Enemy.uasset `
  Content/Material/M_Start.uasset `
  Content/Material/M_Target.uasset
git status --short
git lfs status
```

방식 B에서는 Source Remote만 `fork/main`으로 바꾼다. 프로젝트 규칙상 새 생산 자산은 `/Game/Drone` 아래에 있어야 하므로 `/Game/Material`의 세 Material을 그대로 Commit하지 않는다. Unreal Editor의 Content Browser에서 `/Game/Drone/Materials/Battlefield`로 옮겨 Map 참조를 갱신하고 Redirector를 정리한 뒤, 이전 `/Game/Material` 경로가 남지 않았는지 확인한다.

검증 범위는 Battlefield Map Load·Map Check, Blueprint Compile, 관련 Automation, `git lfs fsck`, `git diff --check`다. 그 뒤에도 `.vsconfig`, `Drone.uproject`, `Drone.cpp`가 Stage되지 않았는지 확인하고 필요한 파일만 Commit한다.

```powershell
git status --short
git diff --check
git lfs fsck
git diff --cached --name-status
```

`git lfs push`만 실행해서는 Git Commit과 Branch Reference가 이동하지 않는다. 정상 `git push`가 실행될 때 LFS pre-push Hook이 해당 Commit이 참조하는 LFS Object를 함께 업로드한다.

### Push가 `non-fast-forward`로 거절될 때

원격 저장소에 이미 커밋이 있다는 뜻이다. 절대로 바로 Force Push하지 않는다.

```powershell
git fetch origin
git log --oneline --graph --decorate --all -n 20
```

로컬 프로젝트를 유지할지, 원격 초기 커밋을 유지할지 확인한 뒤 병합 또는 저장소 재생성 방식을 결정한다. 알 수 없는 원격 기록을 덮어쓰지 않는다.

## 9. 기본 브랜치 구성

아래 `develop` 구조는 일반 권장 시작안이며 현재 Drone 원격의 실제 Branch 구조가 아니다. 2026-08-28 기준 실제 협업 흐름은 `main`에서 기능 Branch를 만들고 검증 후 `main`으로 Pull Request/Merge하는 방식이다. 팀 합의 전에는 `develop`을 새 공유 기준선으로 만들지 않는다.

일반 권장 시작안은 다음과 같다.

```text
main
└─ develop
   ├─ feature/drone-flight
   ├─ feature/enemy-ai
   ├─ feature/ui
   └─ feature/map
```

- `main`: 실행 확인된 안정 데모 기준
- `develop`: 기능 통합 기준
- `feature/*`: 한 기능 또는 한 작업 영역

첫 `develop` 브랜치를 만든다.

```powershell
git switch main
git pull --ff-only
git switch -c develop
git push -u origin develop
```

GitHub에서 기본 브랜치를 `main`으로 유지할지, Pull Request의 기본 대상을 `develop`으로 둘지는 팀 규칙으로 확정한다. 저장소가 안정되면 `main`과 `develop`에 직접 Push를 막는 Branch Protection 또는 Ruleset을 검토한다.

## 10. 기능 브랜치 작업 흐름

예를 들어 Drone Flight MVP를 시작한다.

```powershell
git switch develop
git pull --ff-only
git switch -c feature/drone-flight
```

작업 후 Unreal에서 저장하고 Editor를 닫은 다음 변경을 확인한다.

```powershell
git status
git diff --stat
git lfs status
```

가능하면 기능과 관계있는 파일만 명시적으로 Stage한다.

```powershell
git add Source Config "Content/Path/UsedByDroneFlight"
git status --short
git diff --cached --stat
git commit -m "feat: add initial drone flight controls"
git push -u origin feature/drone-flight
```

커밋 메시지는 무엇을 바꿨는지 알 수 있게 작게 나눈다. `적 AI 만들기`처럼 너무 큰 작업보다 Perception 추가, 감지 테스트, State 추가처럼 기능 단위로 커밋한다.

GitHub에서 `feature/drone-flight` → `develop` Pull Request를 만든다. 바이너리 Asset은 웹 Diff만으로 내용 검토가 어렵기 때문에 리뷰어가 브랜치를 로컬에서 열어 영향받은 Asset과 Level을 확인하는 절차가 필요하다.

### 작업 시작 전 매일 확인

```powershell
git status
git switch develop
git pull --ff-only
```

작업 트리에 변경이 있으면 먼저 커밋, 폐기 또는 임시 보관 방식을 결정한다. 무엇인지 모르는 변경을 둔 채 Pull하지 않는다.

### 원격 Feature 브랜치에 새 커밋이 있을 때

```powershell
git fetch origin
git log --oneline --left-right HEAD...origin/feature/drone-flight
git merge origin/feature/drone-flight
```

공유 중인 Feature 브랜치에서는 이력 재작성보다 일반 Merge를 우선한다. Force Push는 사용하지 않는다.

### Develop 변경을 Feature에 반영

```powershell
git fetch origin
git switch feature/drone-flight
git merge origin/develop
```

충돌은 Feature 브랜치에서 해결하고 테스트한 뒤 Push한다. Unreal 바이너리 브랜치는 `ours`와 `theirs` 의미가 헷갈릴 수 있는 Rebase를 기본 흐름으로 사용하지 않는다.

## 11. 다른 PC에서 Clone하고 Unreal 실행 테스트

### 11.1 새 PC 준비

1. Git과 Git LFS를 설치한다.
2. `git lfs install`을 실행한다.
3. Visual Studio 2022와 프로젝트에 필요한 Unreal C++ 워크로드를 준비한다.
4. 팀과 같은 Unreal Engine 정확한 버전을 설치한다.

작업컴은 `Build.version`으로 UE 5.8.1을 확인했다. 메인컴이나 다른 팀원 PC도 폴더명만 보지 말고 같은 방식으로 정확한 패치 버전을 확인한다.

### 11.2 Clone

```powershell
$RemoteUrl = "https://github.com/YOUR_ACCOUNT/YOUR_REPOSITORY.git"
$CloneRoot = "D:\UnrealProjects\YOUR_PROJECT"
git clone $RemoteUrl $CloneRoot
Set-Location -LiteralPath $CloneRoot
git lfs pull
git lfs fsck
git lfs ls-files
git status
```

정상 결과:

- Clone과 LFS 다운로드가 성공한다.
- `git lfs fsck`가 오류 없이 끝난다.
- 작업 트리가 clean이다.
- `.uasset`과 `.umap`이 LFS 목록에 보인다.

### 11.3 프로젝트 파일 생성과 빌드

1. 정확한 엔진 버전이 맞는지 확인한다.
2. C++ 프로젝트라면 `.uproject`를 우클릭하고 Visual Studio 프로젝트 파일을 생성한다.
3. Visual Studio 2022에서 `Development Editor` / `Win64` 구성을 빌드한다.
4. `.uproject`를 연다.
5. 시작 맵과 주요 Asset을 로드한다.
6. PIE로 최소 기능을 실행한다.

엔진 연결 변경 안내가 나오면 즉시 확정하지 말고 두 PC의 정확한 버전을 먼저 확인한다. 엔진 연결을 바꾸면 `.uproject`가 수정될 수 있다.

### 11.4 실행 후 검증

```powershell
git status --short --ignored
```

- 실행 때문에 생긴 `Intermediate/`, `Saved/`, `DerivedDataCache/`, `Binaries/`는 ignored 상태여야 한다.
- 추적 파일에 의도하지 않은 변경이 없어야 한다.
- Asset이 열리지 않고 작은 텍스트 포인터처럼 보이면 LFS 다운로드 문제를 확인한다.

## 12. Unreal Asset과 Level 충돌 방지

### 12.1 Git LFS가 해결하지 않는 것

`.uasset`과 `.umap`은 일반 텍스트처럼 줄 단위 Merge가 불가능하다. Git LFS에 넣어도 같은 파일을 두 사람이 수정하면 충돌은 그대로 발생한다. 충돌 시 두 결과를 합치는 것이 아니라 한쪽 버전을 선택하고 다른 쪽 작업을 다시 적용해야 하는 경우가 많다.

### 12.2 작업 소유권 규칙

팀 작업 전에 다음을 작업 보드나 문서에 기록한다.

| 항목 | 기록할 내용 |
| --- | --- |
| 담당자 | 현재 Asset 또는 Level을 수정하는 사람 |
| 경로 | 예: `Content/Drone/Blueprints/BP_Drone` |
| 작업 시작 | 시작 시각 또는 Doing 전환 |
| 예상 종료 | 다른 사람이 기다릴 수 있는 기준 |
| 상태 | Free / Editing / Review |

기본 규칙:

1. Asset을 열어 수정하기 전에 Pull한다.
2. 작업 보드에서 담당을 선언한다.
3. 한 Asset은 한 시점에 한 사람만 수정한다.
4. 한 사람이 작업 중인 Persistent Level을 다른 사람이 동시에 저장하지 않는다.
5. 모델, Material, Blueprint, Animation, Map을 폴더와 담당 기준으로 분리한다.
6. 작업 완료 후 작은 커밋으로 Push하고 담당 상태를 해제한다.

### 12.3 Level 작업 분리

- World Partition을 쓰는 Level은 One File Per Actor(OFPA)가 기본 활성화된다.
- 비 World Partition Level은 World Settings의 `Use External Actors`로 OFPA를 켤 수 있다.
- OFPA는 Actor 인스턴스를 외부 파일로 나누어 메인 `.umap` 경쟁을 줄이지만, 외부 Actor 파일도 바이너리이므로 같은 Actor의 동시 편집 충돌은 해결하지 못한다.
- 이미 작업 중인 Level을 OFPA로 일괄 전환하면 많은 파일이 한꺼번에 바뀔 수 있으므로 팀 합의와 별도 브랜치에서 진행한다.
- 맵을 구역, Sublevel, 작업용 Level 등으로 나누는 방식은 실제 맵 구조를 보고 결정한다. 현재 프로젝트의 최종 맵 구조는 미정이다.

### 12.4 Asset 이동과 이름 변경

Asset은 Windows 탐색기가 아니라 Unreal Content Browser에서 이동하거나 이름을 바꾼다. Redirector 정리로 참조 Asset이 함께 바뀔 수 있으므로 다음을 지킨다.

1. 관련 작업자가 없는 시간에 이동한다.
2. 이동 전 Pull한다.
3. Redirector와 참조 변경 목록을 확인한다.
4. 이동·참조 수정 파일을 같은 커밋에 넣는다.
5. 영향받은 Level을 열고 참조 오류를 테스트한다.

### 12.5 선택 사항: Git LFS Locking

원격 호스트와 현재 인증 방식이 Git LFS Locking을 지원하고, 팀 전원이 같은 규칙을 지키기로 한 경우에만 도입한다.

제공된 `.gitattributes` 템플릿에는 의도적으로 `lockable`을 넣지 않았다. 현재 저장소·인증 방식의 Locking 지원 여부와 팀의 잠금/해제 운영 규칙이 아직 확정되지 않았기 때문이다. 따라서 기본 템플릿을 쓰는 동안에는 LFS 잠금 사용 여부와 무관하게 **담당 Asset 분리 규칙이 필수**다.

팀이 Locking을 도입하기로 확정하면 프로젝트 루트에서 다음처럼 속성을 갱신하고, 변경된 `.gitattributes`를 팀 전체가 Pull하도록 한다.

```powershell
git lfs track --lockable "*.uasset"
git lfs track --lockable "*.umap"
git add .gitattributes
git commit -m "chore: mark Unreal assets as LFS lockable"
```

도입 후 `.gitattributes`의 두 규칙에는 다음처럼 `lockable`이 포함되어야 한다.

```gitattributes
*.uasset filter=lfs diff=lfs merge=lfs -text lockable
*.umap   filter=lfs diff=lfs merge=lfs -text lockable
```

`lockable` 파일은 잠기지 않았을 때 작업 사본에서 읽기 전용이 될 수 있다. 따라서 팀 전원이 수정 전 Lock, Commit/Push 후 Unlock 순서를 알아야 하며 장기간 부재하거나 오프라인인 팀원의 오래된 Lock을 처리할 관리자 절차도 필요하다. 실제 Asset에서 잠금 왕복을 시험한다.

```powershell
git lfs locks
git lfs lock "Content/Path/Asset.uasset"
git lfs unlock "Content/Path/Asset.uasset"
```

Locking 지원 여부를 확인하지 않은 상태에서는 이 기능이 있다고 가정하지 않는다. Lock을 도입해도 Unreal Editor의 저장 동작과 팀 해제 절차를 실제 저장소에서 시험해야 한다.

## 13. Merge와 Conflict 처리

### 13.1 충돌 확인

```powershell
git status
git diff --name-only --diff-filter=U
```

충돌한 파일이 텍스트인지 Unreal 바이너리인지 먼저 구분한다.

### 13.2 텍스트 파일 충돌

`Source/`의 C++ 코드나 `Config/`의 `.ini`는 충돌 표시를 읽고 필요한 내용을 직접 합칠 수 있다.

1. `<<<<<<<`, `=======`, `>>>>>>>` 구간을 검토한다.
2. 최종 내용만 남기고 충돌 표시를 제거한다.
3. 빌드 또는 설정 테스트를 한다.
4. 해결된 파일을 Stage한다.

```powershell
git add "Source/Path/File.cpp" "Config/DefaultGame.ini"
git status
git merge --continue
```

Git 버전과 Merge 상태에 따라 `git merge --continue` 대신 일반 `git commit`이 필요할 수 있다.

Merge 자체를 취소하려면 아직 해결 커밋을 만들기 전에 실행한다.

```powershell
git merge --abort
```

### 13.3 `.uasset` 또는 `.umap` 충돌

바이너리 충돌 파일을 텍스트 편집기로 합치지 않는다.

가장 안전한 절차:

1. Unreal Editor를 닫는다.
2. `git status`로 충돌 파일을 기록한다.
3. 담당자끼리 어느 쪽 변경을 기준으로 할지 결정한다.
4. 가능하면 Merge를 중단하고 작업을 분리한 뒤, 한쪽을 먼저 통합한다.
5. 다른 쪽 작업자는 통합된 Asset 위에서 자신의 변경을 다시 적용한다.

일반 Merge에서 한쪽을 완전히 선택하기로 합의했을 때만 다음을 사용한다.

```powershell
# 현재 체크아웃된 브랜치의 파일을 선택
git restore --ours -- "Content/Path/Asset.uasset"

# 병합해 들어오는 브랜치의 파일을 선택
git restore --theirs -- "Content/Path/Asset.uasset"

git add "Content/Path/Asset.uasset"
git status
git merge --continue
```

`ours`와 `theirs`를 둘 다 실행하는 것이 아니다. 선택한 한 명의 작업은 사라질 수 있으므로 담당자 확인 없이 실행하지 않는다. Rebase에서는 의미를 혼동하기 쉬우므로 위 설명은 **일반 Merge 기준**이다.

해결 후 반드시 다음을 확인한다.

- `git lfs pull`이 성공하는가
- 영향받은 Asset이 Unreal에서 열리는가
- Level 참조가 유지되는가
- Blueprint Compile이 성공하는가
- PIE가 실행되는가
- `git status`가 예상 상태인가

### 13.4 Push 충돌

```powershell
git fetch origin
git log --oneline --left-right HEAD...origin/YOUR_BRANCH
```

원격 변경을 확인하고 현재 브랜치에 Merge한 뒤 테스트하고 다시 Push한다.

```powershell
git merge origin/YOUR_BRANCH
git push
```

단순히 Push를 통과시키기 위해 Force Push하지 않는다.

## 14. 잘못된 파일이 이미 추적될 때

`.gitignore`는 아직 추적되지 않은 파일에만 자동 적용된다. 이미 커밋된 생성 폴더는 인덱스에서 제거하는 커밋이 필요하다.

먼저 목록을 확인한다.

```powershell
git ls-files | Select-String -Pattern '(^|/)(Binaries|DerivedDataCache|Intermediate|Saved)/'
```

프로젝트 루트의 생성 폴더가 추적된 것이 확인되었을 때만 실행한다.

```powershell
git rm -r --cached --ignore-unmatch Binaries DerivedDataCache Intermediate Saved
git status
git commit -m "chore: stop tracking Unreal generated files"
```

`--cached`는 로컬 파일을 지우지 않고 Git 추적 대상에서만 뺀다. Plugin 내부 등 다른 경로가 출력되면 정확한 경로를 확인하여 개별적으로 제거한다.

## 15. LFS를 늦게 적용했을 때

### 아직 커밋하지 않았을 때

`.gitattributes`를 적용한 후 Asset을 인덱스에서 빼고 다시 추가한다.

```powershell
git rm --cached --ignore-unmatch -- '*.uasset' '*.umap'
git add .gitattributes
git add -- '*.uasset' '*.umap'
git lfs status
git lfs ls-files
```

### 이미 커밋했지만 Push하지 않았을 때

과거 커밋 안의 일반 Git 바이너리는 단순히 새 커밋을 추가해도 역사에 남는다. 먼저 복구용 백업 브랜치나 저장소 사본을 만든 뒤 `git lfs migrate` 사용 여부를 검토한다.

```powershell
git lfs migrate info --everything
git lfs migrate import --include="*.uasset,*.umap" --everything
git lfs fsck
```

이 작업은 커밋 ID를 바꾼다. 결과를 충분히 확인한 후 첫 Push를 한다.

### 이미 공유 저장소에 Push했을 때

`git lfs migrate import --everything`은 공유 이력을 다시 쓰므로 일상 명령으로 실행하지 않는다. 모든 팀원이 작업을 멈추고 백업한 상태에서 이력 재작성, 보호 브랜치, Force Push, 전원 재Clone 계획을 세워야 한다. 사용자 승인과 팀 합의 없이 실행하지 않는다.

## 16. Git LFS 문제 해결

### Clone 후 Asset 대신 작은 포인터 파일만 있을 때

```powershell
git lfs install
git lfs pull
git lfs checkout
git lfs fsck
git lfs status
```

그 후 Unreal Editor를 다시 연다. 계속 실패하면 원격에 실제 LFS 객체가 업로드되었는지 원본 PC에서 확인한다.

### LFS 객체 누락으로 Push가 거절될 때

원본 LFS 객체를 가진 PC에서 다음을 먼저 확인한다.

```powershell
git lfs fsck
git lfs status
```

GitHub가 참조된 LFS 객체 누락을 보고하고, 해당 PC가 모든 원본 객체를 보유한 것이 확실할 때만 다음을 검토한다.

```powershell
git remote get-url --push origin
git branch -vv
git lfs push --all origin
```

`--all`은 많은 과거 객체를 업로드할 수 있으므로 저장공간·대역폭과 대상 원격을 먼저 확인한다. 이 명령은 LFS Object만 전송하며 Git Commit·Branch는 Push하지 않는다.

## 17. 안전한 복구와 Commit 되돌리기

### 17.1 복구 전 공통 확인

```powershell
git status
git log --oneline --graph --decorate -n 20
git reflog -n 20
```

중요한 변경이 남아 있으면 먼저 복구용 브랜치에 WIP 커밋을 만든다.

```powershell
git switch -c recovery/before-fix-YYYYMMDD
git add -A
git commit -m "wip: checkpoint before recovery"
```

`YYYYMMDD`는 실제 날짜로 바꾼다. 생성 폴더가 올바르게 ignore되는지 확인한 뒤 커밋한다.

### 17.2 Stage만 취소하고 파일 수정은 유지

```powershell
git restore --staged -- "Source/Path/File.cpp"
```

### 17.3 커밋하지 않은 파일 변경 폐기

```powershell
git restore -- "Source/Path/File.cpp"
```

이 명령은 해당 파일의 미커밋 변경을 없앤다. 복구용 사본이나 커밋 없이 실행하면 되돌리기 어려우므로 경로를 반드시 확인한다.

### 17.4 이전 Commit의 파일을 현재 브랜치로 복원

```powershell
$CommitSha = "PASTE_COMMIT_SHA_HERE"
git restore --source=$CommitSha -- "Content/Path/Asset.uasset"
git status
git add "Content/Path/Asset.uasset"
git commit -m "fix: restore asset from known good revision"
```

Unreal Asset은 참조 관계가 있으므로 한 파일만 복원해도 되는지 확인한다. 필요하면 해당 커밋의 연관 Asset을 함께 복원하고 Editor에서 테스트한다.

### 17.5 아직 Push하지 않은 마지막 Commit을 다시 작성

변경 파일은 유지하면서 마지막 Commit만 취소한다.

```powershell
git reset --soft HEAD~1
git status
```

공유된 Commit에는 사용하지 않는다. 필요한 파일을 다시 Stage하고 새 Commit을 만든다.

### 17.6 이미 Push한 잘못된 Commit 되돌리기

공유 이력을 지우지 않고 반대 변경을 새 Commit으로 만든다.

```powershell
$CommitSha = "PASTE_COMMIT_SHA_HERE"
git revert $CommitSha
git push
```

Merge Commit을 되돌릴 때는 부모 방향을 확인해야 한다.

```powershell
$MergeCommitSha = "PASTE_MERGE_COMMIT_SHA_HERE"
git show --summary $MergeCommitSha
git revert -m 1 $MergeCommitSha
```

`-m 1`이 항상 정답은 아니다. 어느 부모를 기준으로 유지할지 확인하지 못했다면 실행하지 않는다.

### 17.7 진행 중인 Merge 취소

```powershell
git merge --abort
```

### 17.8 잃어버린 Commit 찾기

```powershell
git reflog
$CommitSha = "PASTE_COMMIT_SHA_HERE"
git switch -c recovery/found-commit $CommitSha
```

복구 브랜치에서 내용을 확인한 후 필요한 Commit만 정상 브랜치로 반영한다.

### 위험 명령

다음 명령은 로컬 작업 또는 공유 이력을 대량으로 잃게 만들 수 있으므로 이 가이드의 기본 복구 절차에서 사용하지 않는다.

- `git reset --hard`
- `git clean -fd` 또는 `git clean -fdx`
- `git push --force`
- 확인하지 않은 대규모 `git lfs migrate`

## 18. 첫 PC 간 왕복 검증 시나리오

단순히 Clone 성공만 확인하지 말고 다음 왕복 테스트를 한 번 수행한다.

### 메인컴

1. 프로젝트가 clean인지 확인한다.
2. 작은 테스트용 텍스트 문서 또는 안전한 C++ 주석을 변경한다.
3. Feature 브랜치에 Commit/Push한다.

### 작업컴

1. 같은 Feature 브랜치를 Fetch/Switch한다.
2. `git lfs pull`을 실행한다.
3. Unreal 프로젝트를 열고 빌드·PIE한다.
4. 별도의 작은 변경을 Commit/Push한다.

### 메인컴

1. Editor를 닫는다.
2. Pull한다.
3. Unreal을 열어 변경을 확인한다.
4. `git status`가 clean인지 확인한다.

이 검증이 끝나야 여러 PC 작업 환경이 실제로 연결되었다고 본다.

## 19. 실전 완료 체크리스트

### 설치

- [x] `git --version` 성공
- [x] `git lfs version` 성공
- [x] `git lfs install` 성공
- [x] Git 사용자 이름과 이메일 확인

### 버전

- [ ] 메인컴의 정확한 UE 패치 버전 확인
- [x] 작업컴의 정확한 UE 패치 버전 확인: `Build.version` 기준 UE 5.8.1
- [ ] 두 PC 버전 일치 확인
- [x] `UE_5.8` 폴더명만이 아니라 `Build.version`으로 작업컴 패치 확인

### 저장소

- [x] GitHub 저장소 이름 결정: `gyeonliz/drone`
- [ ] Public/Private 결정
- [x] GitHub 저장소 생성
- [x] Unreal 프로젝트 루트에서 Git 초기화
- [x] `.gitignore` 적용
- [x] `.gitattributes` 적용
- [x] `.uasset` / `.umap` LFS 추적 확인
- [x] 첫 Commit: `91498b7`
- [x] 첫 Push: 로컬 `main`과 `origin/main` 일치

### 제외·포함 확인

- [x] `Source/`, `Config/`, `Content/`, `.uproject` 포함
- [x] `Intermediate/`, `Saved/`, `DerivedDataCache/` 제외
- [x] `Binaries/`, `.vs/` 제외
- [x] 비밀번호, 토큰, 인증 파일 제외
- [x] 현재 Drone 프로젝트의 Android File Server 비활성화와 빈 `SecurityToken` 확인

### 다른 PC

- [ ] Clone 성공
- [ ] `git lfs pull` 성공
- [ ] `git lfs fsck` 성공
- [ ] Visual Studio 프로젝트 파일 생성
- [ ] C++ 빌드 성공
- [ ] Unreal 실행 성공
- [ ] 주요 Level·Asset 로드 성공
- [ ] PIE 성공
- [ ] 실행 후 의도하지 않은 추적 변경 없음

### 협업

- [ ] 중앙/Fork Remote 역할과 실제 Push URL 확인
- [ ] `main` / `develop` / `feature/*` 규칙 합의
- [ ] Asset 담당 선언 방식 합의
- [ ] Level 동시 작업 방지 방식 합의
- [ ] 바이너리 충돌 시 한쪽 선택·재적용 원칙 합의
- [ ] Pull Request 테스트 기준 합의

## 20. 공식 참고 자료

- [Git for Windows](https://git-scm.com/download/win)
- [Git LFS 공식 사이트](https://git-lfs.com/)
- [GitHub Docs: Git LFS 설치](https://docs.github.com/en/repositories/working-with-files/managing-large-files/installing-git-large-file-storage)
- [GitHub Docs: Git LFS 설정](https://docs.github.com/en/repositories/working-with-files/managing-large-files/configuring-git-large-file-storage)
- [GitHub Docs: Git LFS 개요](https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-git-large-file-storage)
- [GitHub Docs: GitHub Desktop에서 Push](https://docs.github.com/en/desktop/making-changes-in-a-branch/pushing-changes-to-github-from-github-desktop)
- [GitHub Docs: Remote 저장소 관리](https://docs.github.com/en/get-started/git-basics/managing-remote-repositories)
- [GitHub 공식 Unreal `.gitignore` 템플릿](https://github.com/github/gitignore/blob/main/UnrealEngine.gitignore)
- [Epic UE 5.8: Source Control](https://dev.epicgames.com/documentation/en-us/unreal-engine/source-control-in-unreal-engine)
- [Epic UE 5.8: One File Per Actor](https://dev.epicgames.com/documentation/en-us/unreal-engine/one-file-per-actor-in-unreal-engine)
- [Epic UE 5.8: Android File Server](https://dev.epicgames.com/documentation/unreal-engine/android-file-server-for-unreal-engine?lang=ko)
- [Git: restore](https://git-scm.com/docs/git-restore)
- [Git: revert](https://git-scm.com/docs/git-revert)
- [Git: reset](https://git-scm.com/docs/git-reset)
