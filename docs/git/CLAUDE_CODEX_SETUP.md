# 다른 PC에서 Claude ↔ Codex 협업 세팅

작성: 2026-10-01 (C PC, Claude). 협업 규칙은 [CLAUDE_CODEX_COLLABORATION.md](CLAUDE_CODEX_COLLABORATION.md).

## 무엇이 따라가고 무엇이 PC마다 따로인가

| 구분 | 파일 | 다른 PC로 가는 방법 |
|---|---|---|
| 공유(Git) | `CLAUDE.md`, `AGENTS.md`, `.mcp.json`, `.claude/settings.json`, `.claude/skills/`, Unreal 저장소 `.claude/codex-bridge/`(스크립트·역할·지시서 틀) | `drone` 저장소 Commit/Push → 다른 PC Pull |
| 공유(Git) | md 저장소의 `AGENTS.md`, `CLAUDE.md`, STATUS/WORKBOARD 및 `docs/git/CLAUDE_CODEX_SETUP.md`, `docs/git/CLAUDE_CODEX_COLLABORATION.md`, `docs/git/USER_RULES.md` | `gyeonliz/md` 저장소 Commit/Push → Pull |
| PC 전용(Git 제외) | `.claude/settings.local.json`, `.claude/codex-bridge/local.json`, Unreal 저장소 `.claude/codex-bridge/runs/`, `briefs/` | 각 PC에서 Unreal 저장소 `.claude/codex-bridge/Test-CollabSetup.ps1 -WriteLocalConfig`로 생성 |
| 계정(로그인) | Claude 계정, ChatGPT(Codex) 계정 | 각 PC 앱에서 직접 로그인. 인증 파일(`~/.codex/auth.json` 등)은 복사하지 않는다 |
| PC 전용(사용자 홈) | `~/.claude/settings.json`, Claude 메모리(`~/.claude/projects/...`), `~/.codex/config.toml` | 따라가지 않는다. 필요한 규칙은 이미 `CLAUDE.md`(공유)에 있다 |
| 사용자 공통 규칙 | md 저장소 `docs/git/USER_RULES.md`(공유 원본) → 각 PC `~/.claude/CLAUDE.md`(가져오기 줄) | Pull 후 Unreal 저장소 `.claude/codex-bridge/Test-CollabSetup.ps1 -InstallUserRules` 한 번 |

## 공유 파일 목록 — 최초 공유 2026-10-02 완료

기존 공유 파일은 5b03ad3(10/02)로 Commit/Push 완료됐다. 새 `roles/ui.md`·`roles/image.md`는 미추적이며 사용자가 별도 Commit할 때 포함할 대상이다. 아래는 공유 대상 목록으로, 이번 문서 작업에서는 Commit/Push하지 않는다. PC 전용 설정·runs·briefs는 Git 제외다.

- `CLAUDE.md`, `AGENTS.md`, `.mcp.json`, `.gitignore`
- `.claude/settings.json`, `.claude/skills/codex-handoff/SKILL.md`
- `.claude/codex-bridge/` 아래 `*.ps1`, `BRIEF_TEMPLATE.md`, Unreal 저장소 `.claude/codex-bridge/roles/`, `.gitignore`

md의 미커밋 문서는 사용자가 명시적으로 지시한 경우에만 Commit/Push한다.

## 새 PC에서

1. **설치·로그인**
   - Claude 데스크톱 앱 설치 → 같은 Claude 계정으로 로그인.
   - Codex 데스크톱 앱 설치 → 같은 ChatGPT 계정으로 로그인(Codex CLI가 앱과 함께 깔린다).
   - Unreal Engine 5.8, Visual Studio, Git LFS, GitHub Desktop.
2. **저장소 받기**: GitHub Desktop에서 `gyeonliz/drone`, `gyeonliz/md`를 Clone 또는 Fetch → Pull. 이어서 `git lfs pull origin main`(drone).
3. **점검과 PC 전용 설정 생성** (PowerShell, drone 저장소 루트에서)

   ```powershell
   powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\.claude\codex-bridge\Test-CollabSetup.ps1 -WriteLocalConfig -InstallUserRules
   ```

   `-InstallUserRules`는 사용자 공통 규칙([USER_RULES.md](USER_RULES.md): 정확성·직접 진행·실제 검증·이미지·세계관 규칙)을 그 PC의 `~/.claude/CLAUDE.md`에 가져오기 줄로 넣는다. 기존 내용은 지우지 않는다. 그래서 드론 외 다른 프로젝트에서도 같은 규칙이 적용된다.

   md 저장소가 `drone` 옆 `md` 폴더, `D:\JGY\project\md`, `%USERPROFILE%\Documents\Codex\2026-08-19\codex-gpt-chatgpt-codex-1-6` 중 하나면 자동으로 찾는다. 다른 곳이면 `-MdRepo '<경로>'`를 붙인다. 마지막 줄이 `COLLAB_READY`면 준비 완료다. `WARN`은 안내, `FAIL`만 막힘이다.
4. **Claude Code에서 drone 폴더를 연다.** `CLAUDE.md`, `AGENTS.md`, `codex-handoff` 스킬, Unreal MCP 설정이 자동으로 읽힌다.
5. **(선택) 휴대폰 연동**: Claude 앱 설정의 "Connect new sessions to Remote Control"을 켠다. 이 설정은 PC마다 따로다.
6. **(선택) 사용자 기본값**: `~/.claude/settings.json`이 없으면 아래를 넣는다. 모델 기본값과 Commit/Push 승인 요청을 C PC와 맞춘다.

   ```json
   {
     "model": "opus",
     "permissions": {
       "defaultMode": "acceptEdits",
       "ask": ["Bash(git commit:*)", "Bash(git push:*)", "Bash(git reset:*)", "Bash(git clean:*)", "Bash(git stash:*)"],
       "deny": ["Read(**/auth.json)", "Read(**/.env)", "Read(**/.env.*)"]
     }
   }
   ```

## Unreal MCP 자동 시작 — Git 공유 Default 설정 (10/04 정정)

자동 시작은 Git 추적 Config/DefaultEditorPerProjectUserSettings.ini의 [/Script/ModelContextProtocolEngine.ModelContextProtocolSettings] bAutoStartServer=True·ServerPortNumber=8000·ServerUrlPath=/mcp로 8월부터 모든 PC에 켜져 있다. PC별 Saved ini는 끄거나 바꿀 때만 사용한다. C PC Saved 설정 완료라는 이전 설명은 오류였고 공유 Default로 충족한다.

Claude 클라이언트는 Unreal 루트 .mcp.json을 사용한다. 연결이 안 되면 자동화 등 다른 Unreal 프로세스가8000포트를 점유했는지 확인한다. 자동화 실행은 -ModelContextProtocolPort=8010으로 사용자Editor8000을 보존한다. 열린Editor 즉시시작은 ModelContextProtocol.StartServer이며 설정 존재와 실제 도구 연결 성공을 구분한다.

## 알려진 제한

- Claude 메모리는 PC별이다. 다른 PC의 Claude는 이 PC에서 쌓인 메모리를 모른다. 지켜야 할 규칙은 `CLAUDE.md`·`CLAUDE_CODEX_COLLABORATION.md`에 적어 공유한다.
- Codex 세션(대화 기록)도 PC별이다. 작업 문맥은 md 저장소의 STATUS/WORKBOARD로 넘긴다.
- Unreal Editor가 켜져 있으면 Claude의 C++ Build가 거절된다(Live Coding). Build 전에 Editor를 저장하고 닫는다.
- Codex CLI 버전과 비대화형 Space 저장 가능 여부는 PC·앱 버전마다 다를 수 있다. 새 PC에서는 첫 docs 위임 결과의 "Drone Space" 칸을 확인한다.
