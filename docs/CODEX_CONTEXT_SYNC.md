# 메인컴 ↔ 작업컴 Codex/GPT 작업 문맥 전달

## 목적과 경계

두 데이터 흐름은 반드시 분리해서 관리한다.

| 데이터 | 전달 방법 | 예시 |
| --- | --- | --- |
| Unreal/프로젝트 데이터 | `gyeonliz/drone` Git + GitHub | `Source`, `Config`, `Content`, Commit, Branch |
| Codex/GPT 작업 문맥 | `gyeonliz/md` Git + GitHub | `CONTEXT.md`, `STATUS.md`, `WORKBOARD.md`, 가이드, 안전한 도구 |
| 선택적 단일 인계본 | 검토 가능한 인계 패키지 | 특정 시점의 목표·진행·다음 작업을 합친 `handoff.md`와 검증용 `manifest.json` |

`drone`과 `md`는 서로 다른 저장소다. 문서 저장소가 Unreal 프로젝트 Push를 대신하지 않으며, Git이 Codex의 전체 대화나 원시 세션 상태를 자동 보존해 주는 것도 아니다. 보내는 PC에서는 두 저장소의 작업을 서로 독립적으로 확인해야 한다.

## 현재 확정된 저장소

```text
Unreal 프로젝트  https://github.com/gyeonliz/drone
작업 문서·문맥   https://github.com/gyeonliz/md
```

`md` 저장소에는 사람이 읽고 검토할 수 있는 문서와 안전한 보조 스크립트만 둔다. Unreal `Content`·`Source` 복제본, `auth.json`, `.env`, 원시 세션 DB, 브라우저 프로필, 로그와 생성된 handoff 패키지는 넣지 않는다.

## 현재 사용할 안전한 기본 방식

일상적인 PC 간 공유는 `md` 저장소의 검토 가능한 Markdown을 Clone/Pull하는 방식으로 운영한다. 특정 시점의 단일 전달본이나 Git과 분리된 전달이 필요할 때만 이식 가능한 `handoff.md` + `manifest.json` 자료를 보조 수단으로 사용한다. 어느 방식에서도 Codex 데이터 디렉터리, 세션 DB, 브라우저 프로필, 자격 증명 저장소, 인증 캐시는 복제하지 않는다.

공식 OpenAI 명령 문서는 Codex에 저장되어 있는 세션을 `codex resume`으로 재개하는 방법을 설명한다. 그러나 원시 세션 저장소를 임의로 PC 사이에 복사하는 방식을 안정적인 이식/백업 규격으로 문서화하지는 않는다. 사용 중인 정확한 제품과 버전에 대해 OpenAI가 지원 경로를 별도로 문서화하기 전까지 원시 로컬 상태는 구현 세부사항으로 취급한다. 참고: [Codex developer commands](https://learn.chatgpt.com/docs/developer-commands?surface=cli).

OpenAI의 현재 [다른 에이전트에서 가져오기](https://learn.chatgpt.com/docs/import) 흐름은 Claude Code, Claude Cowork 또는 Cursor에서 ChatGPT/Codex로 가져오는 지원 경로다. Codex가 설치된 두 PC 사이에서 Codex 데이터 디렉터리를 그대로 복제하는 절차로 문서화된 것은 아니므로, 이 문서의 PC 간 기본선은 계속 검토 가능한 인계 자료다.

OpenAI의 [인증 문서](https://learn.chatgpt.com/docs/auth)는 파일 기반 `~/.codex/auth.json`에 액세스 토큰이 있으므로 비밀번호처럼 다루라고 안내한다. 이 작업 흐름에서는 해당 파일을 의도적으로 제외하고, 각 PC에서 정상적인 로그인 절차를 별도로 진행한다.

## 이 방식으로 절대 전달하지 않는 것

- `auth.json`, API Key, Access/Refresh Token, 비밀번호, Cookie, Private Key
- OS 자격 증명 저장소 또는 Keychain 내보내기
- `.env` 파일이나 환경변수 전체 덤프
- 원시 Codex 세션 DB, Cache, Log, Codex 홈/Profile 디렉터리 복사본
- Git Credential Helper/설정이나 `git remote -v` 출력
- Git diff 또는 자동으로 수집한 임의의 workspace 파일

스크립트는 허용 목록, 파일 크기 제한, 일반적인 비밀정보 패턴 검사, 명시적인 선택 매개변수를 사용한다. 하지만 이런 검사는 일반 문장에 비공개 정보가 전혀 없음을 증명하지 못한다. 보내기 전에 사람이 `handoff.md` 전체를 읽어야 한다.

## 보내는 PC의 작업 종료 절차

1. Git 작업 절차에 맞게 Unreal Editor 내용을 저장하고 필요하면 Editor를 종료한다.
2. `drone` 프로젝트 변경 사항을 검토하고, 의도한 Branch에 Commit한 뒤 Push한다.
3. `md` workspace의 `CONTEXT.md`, `STATUS.md`, `WORKBOARD.md`를 다음 내용으로 갱신한다.
   - 현재 목표
   - 완료하고 테스트한 작업
   - 진행 중인 작업
   - 정확한 다음 행동
   - 결정 사항과 제약 조건
   - 미해결 질문과 알려진 문제
4. 변경된 Markdown과 도구 범위를 검토하고 `md` 저장소에 Commit·Push한다.
5. 단일 인계본이 필요한 경우에만 별도의 인계 패키지를 Export한다.
6. 생성된 `handoff.md`를 열어 모든 줄을 검토한 뒤 신뢰할 수 있는 전달 수단으로 두 파일짜리 패키지만 옮긴다.

예시:

```powershell
.\tools\context-sync\Export-WorkContext.ps1 `
    -OutputPath 'D:\Transfer\drone-context-2026-08-19' `
    -WorkspacePath $PWD `
    -ContextFile '.\CONTEXT.md' `
    -IncludeGitMetadata `
    -RecentCommitCount 10 `
    -CurrentObjective 'Drone PFN-06 반복 입력 검증' `
    -NextAction '새 PIE 3회 전체 체크리스트 실행'
```

`-IncludeGitMetadata`는 선택 사항이다. 지정하면 로컬 Branch, 짧은 Status, 최근 Commit의 Hash/날짜/작성자 이름/제목만 읽는다. Remote URL, Credential 설정, 환경변수, diff는 읽지 않는다. 흔한 민감 파일명에 해당하는 Status 항목도 제외한다.

새 목적지에는 먼저 `-WhatIf`를 사용하는 것이 좋다. 기존 디렉터리는 `-Force`가 없으면 거부하며, `-Force`가 있어도 알려진 두 패키지 파일 외의 항목이 있으면 거부한다.

현재 작업컴에서 실행 정책 오류가 발생하면 시스템 설정을 영구 변경하지 말고 다음처럼 해당 프로세스에만 `Bypass`를 적용한다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass `
    -File .\tools\context-sync\Export-WorkContext.ps1 `
    -OutputPath 'D:\Transfer\drone-context-2026-08-19' `
    -WorkspacePath $PWD `
    -ContextFile '.\CONTEXT.md'
```

실행 전에 로컬 스크립트의 경로와 내용을 확인한다. 이 방식은 컴퓨터나 사용자 계정의 영구 실행 정책을 변경하지 않는다.

## 받는 PC의 작업 시작 절차

1. 이 PC에서 GitHub와 Codex에 정상적으로 로그인한다. 다른 PC의 인증 파일을 가져오지 않는다.
2. `gyeonliz/drone`을 Clone하거나 의도한 Branch를 Pull한다.
3. Branch, Commit, Git LFS Object, Unreal 실행 상태를 확인한다.
4. `gyeonliz/md`를 별도 폴더에 Clone하거나 Pull한다.
5. `CONTEXT.md`, `STATUS.md`, `WORKBOARD.md`를 읽고 실제 Drone 저장소 상태와 비교한다.
6. 선택적 handoff 패키지를 받았다면 프로젝트와 `md` 저장소와 구분되는 디렉터리로 Import한다.
7. Codex에 문서를 이전 작업 문맥으로 사용하되, 저장소의 증거와 사용자가 새로 알려준 내용을 우선하라고 지시한다.
8. 확인된 다음 행동부터 계속한다.

예시:

```powershell
.\tools\context-sync\Import-WorkContext.ps1 `
    -PackagePath 'D:\Transfer\drone-context-2026-08-19' `
    -DestinationPath '.\.work-context\incoming-2026-08-19'
```

Import 후 첫 요청 예시:

```text
.work-context/incoming-2026-08-19/handoff.md를 이전 작업 문맥으로 읽어라.
작업 전에 현재 Git Branch/Status와 비교해라.
확인되지 않았거나 미정이라고 표시된 항목을 구현 완료 상태로 취급하지 마라.
문서의 다음 행동부터 시작하되, 불일치가 있으면 먼저 보고해라.
```

## 패키지 구조와 검증

내보낸 패키지는 정확히 다음 두 파일로 구성된다.

```text
handoff-package/
  handoff.md
  manifest.json
```

`handoff.md`가 유일한 작업 문맥 본문이다. 선택한 `.md`/`.txt` 입력은 숨은 첨부 파일이 생기지 않도록 이 파일 안에 포함된다. `manifest.json`에는 스키마, 안전 선언, 입력 문서의 상대 경로/해시, 선택적 Git 메타데이터, `handoff.md`의 예상 바이트 수와 SHA-256이 기록된다.

Import 스크립트는 복사 전에 패키지 구조와 해시를 확인한다. SHA-256은 우발적인 손상이나 변경을 찾지만 진위성을 증명하는 서명은 아니다. 신뢰할 수 있는 경로로 받은 패키지만 사용하고 Markdown도 직접 검토한다.

## 수동 방식부터 시작하고 이후 자동화하기

처음에는 명시적인 두 명령과 사람의 검토 절차로 운영한다. 작업 흐름이 안정된 다음 Wrapper Script로 아래 단계를 연결할 수 있다.

1. `drone` Git Status/Commit/Push 결과 확인
2. `md`의 `CONTEXT.md`, `STATUS.md`, `WORKBOARD.md` 갱신
3. `md` Status/Commit/Push 결과 확인
4. 선택적으로 `Export-WorkContext.ps1` 실행
5. 다른 PC에서 `drone` Pull/LFS와 `md` Pull 확인
6. 패키지를 사용한 경우에만 `Import-WorkContext.ps1` 실행

자동화 이후에도 데이터 분리와 안전 경계는 그대로 유지한다. Codex Profile을 몰래 검색하거나 원시 Session/Credential을 복사하거나 환경변수를 덤프하면 안 된다. Git Push의 종료 코드를 확인하지 않고 성공했다고 추측해서도 안 된다.

스크립트별 사용법과 매개변수는 [`../tools/context-sync/README.md`](../tools/context-sync/README.md)를 참고한다.
