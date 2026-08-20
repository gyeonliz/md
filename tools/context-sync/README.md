# Context Sync 툴킷

이 툴킷은 Unreal 프로젝트 데이터나 Codex의 비공개 로컬 상태가 아니라 **작업 문맥의 선택적 단일 인계본**만 옮긴다.

- 프로젝트 데이터: `gyeonliz/drone`에 `push`한 뒤 다른 PC에서 `pull` 또는 `clone`한다.
- 일상적인 작업 문맥: `gyeonliz/md`의 `CONTEXT.md`, `STATUS.md`, `WORKBOARD.md`와 가이드를 검토해 Commit·Push하고 다른 PC에서 Pull한다.
- 선택적 단일 인계본: 이 툴킷이 만드는, 사람이 검토할 수 있는 `handoff.md` + `manifest.json` 패키지로 옮긴다.
- 인증 및 로컬 내부 데이터: PC마다 별도로 로그인한다. `auth.json`, 토큰, 비밀번호, 자격 증명 저장소 내보내기, 원시 세션 DB, Codex 홈 디렉터리 복사본은 패키지에 넣지 않는다.

공식 OpenAI 문서는 Codex 명령으로 저장된 세션을 재개하는 방법을 설명하지만, 원시 온디스크 세션 저장소를 PC 사이에서 복사하는 방식을 이식 가능한 백업/복원 규격으로 보장하지는 않는다. 또한 [인증 문서](https://learn.chatgpt.com/docs/auth)는 파일 기반 `auth.json`에 액세스 토큰이 들어 있으므로 비밀번호처럼 다루라고 안내한다. 따라서 이 툴킷은 사람이 읽을 수 있는 인계 자료 방식을 안전한 기본선으로 사용한다.

현재 공식 [다른 에이전트에서 가져오기](https://learn.chatgpt.com/docs/import)는 Claude Code, Claude Cowork 또는 Cursor를 출발점으로 설명한다. 이는 두 Codex 설치 사이의 원시 데이터 디렉터리 복제를 보장하는 절차가 아니다.

## 보내는 PC에서 내보내기

프로젝트 workspace에서 실행한다.

```powershell
.\tools\context-sync\Export-WorkContext.ps1 `
    -OutputPath 'D:\Transfer\drone-context-2026-08-19' `
    -WorkspacePath $PWD `
    -ContextFile '.\CONTEXT.md' `
    -IncludeGitMetadata `
    -CurrentObjective 'Unreal + Git 작업 환경 구축' `
    -NextAction '첫 Push 전에 Git LFS 추적 상태 확인'
```

파일을 쓰지 않고 미리 확인하려면 다음과 같이 실행한다.

```powershell
.\tools\context-sync\Export-WorkContext.ps1 `
    -OutputPath 'D:\Transfer\drone-context-preview' `
    -ContextFile '.\CONTEXT.md' `
    -IncludeGitMetadata `
    -WhatIf
```

전송하기 전에 `handoff.md`를 열고 작성 필요 표시가 있는 항목을 채운다. 오래된 내용을 지우고 비공개 정보가 없는지 직접 검토한다. `handoff.md`를 수동 수정했다면 다시 내보내서 `manifest.json`의 해시도 갱신해야 한다. Import 스크립트는 해시가 맞지 않는 패키지를 거부한다.

`-ContextFile`은 `-WorkspacePath` 내부의 `.md`, `.txt` 파일만 받는다. 각 파일은 크기 제한과 일반적인 자격 증명 패턴 검사를 거친 뒤 상대 경로/해시가 기록되고 `handoff.md` 본문에 포함된다. Git 메타데이터는 명시적으로 요청한 경우에만 현재 브랜치, 짧은 상태, 최근 Commit 정보만 수집한다. `git remote`를 실행하거나 diff, 환경변수, Git 파일 내용을 수집하지 않는다.

기존 출력 디렉터리는 기본적으로 거부한다. `-Force`를 사용하더라도 해당 디렉터리에 `handoff.md`, `manifest.json` 외의 파일이 하나라도 있으면 덮어쓰지 않는다.

### 작업컴에서 실행 정책 오류가 날 때

현재 작업컴은 `.ps1` 직접 실행을 기본 정책으로 차단한다. 시스템 전체 정책을 바꾸지 않고, 검토한 로컬 스크립트의 해당 실행에만 우회 옵션을 적용하려면 다음 형식을 사용한다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
    -File .\tools\context-sync\Export-WorkContext.ps1 `
    -OutputPath 'D:\Transfer\drone-context-2026-08-19' `
    -WorkspacePath $PWD `
    -ContextFile '.\CONTEXT.md' `
    -IncludeGitMetadata
```

이 명령은 컴퓨터나 사용자 계정의 영구 실행 정책을 변경하지 않는다. 실행 전에 이 저장소의 스크립트가 맞는지 경로와 내용을 확인한다. Import도 같은 방식으로 `-File .\tools\context-sync\Import-WorkContext.ps1`을 지정할 수 있다.

## 받는 PC에서 가져오기

먼저 Git으로 프로젝트를 `clone` 또는 `pull`한다. 그다음 작업 문맥 패키지를 별도 위치에 가져온다.

```powershell
.\tools\context-sync\Import-WorkContext.ps1 `
    -PackagePath 'D:\Transfer\drone-context-2026-08-19' `
    -DestinationPath '.\.work-context\incoming-2026-08-19'
```

파일을 쓰지 않고 검증과 쓰기 작업을 미리 확인하려면 다음과 같이 실행한다.

```powershell
.\tools\context-sync\Import-WorkContext.ps1 `
    -PackagePath 'D:\Transfer\drone-context-2026-08-19' `
    -DestinationPath '.\.work-context\incoming-2026-08-19' `
    -WhatIf
```

Import 스크립트는 `handoff.md`, `manifest.json` 두 파일만 받는다. 스키마, 안전 선언, 바이트 수, SHA-256을 검증한 뒤 두 파일을 복사한다. 해시는 우발적인 변경을 찾는 용도이며 디지털 서명이 아니므로 패키지 작성자의 신원을 증명하지 않는다.

가져온 뒤 Codex에 `handoff.md`를 읽고 현재 체크아웃한 저장소와 비교하라고 요청한다. 문서의 모든 내용이 아직 유효하다고 가정하지 않는다.

## 매개변수

### `Export-WorkContext.ps1`

- `-OutputPath` (필수): 새 패키지 디렉터리. 상대 경로는 현재 셸 디렉터리를 기준으로 한다.
- `-WorkspacePath`: 프로젝트 workspace. 기본값은 현재 디렉터리다.
- `-ContextFile`: workspace 내부의 `.md`/`.txt` 파일 하나 이상.
- `-IncludeGitMetadata`: 로컬 브랜치/상태/최근 Commit 수집을 명시적으로 켠다.
- `-RecentCommitCount`: 1~50, 기본값 10.
- `-ProjectName`, `-CurrentObjective`, `-NextAction`: 인계 문서에 기록할 정보.
- `-MaxContextFileBytes`: 파일별 제한. 기본값 1 MiB, 최대 10 MiB.
- `-Force`: 안전한 기존 디렉터리에서 알려진 두 파일만 교체한다.
- `-WhatIf`: 쓰기 작업을 미리 확인한다.

### `Import-WorkContext.ps1`

- `-PackagePath` (필수): 내보낸 패키지 디렉터리.
- `-DestinationPath` (필수): 별도로 둘 로컬 가져오기 디렉터리.
- `-Force`: 안전한 기존 목적지에서 알려진 두 파일만 교체한다.
- `-WhatIf`: 전체 검증 후 쓰기 작업을 미리 확인한다.

PC 간 전체 운영 절차는 [`../../docs/CODEX_CONTEXT_SYNC.md`](../../docs/CODEX_CONTEXT_SYNC.md)를 참고한다.
