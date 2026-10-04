# CLAUDE.md — Drone 문서 저장소 (gyeonliz/md)

설정·대화는 Claude로 이관했고, 이 문서 저장소와 Drone Space는 Codex 담당이다(2026-10-01). 기존 지침은 그대로 유효하며 아래에서 불러온다.

@AGENTS.md

## 이 PC의 경로

| 대상 | 경로 |
|---|---|
| 문서 저장소(이 폴더) | `C:\Users\jkw11\Documents\Codex\2026-08-19\codex-gpt-chatgpt-codex-1-6` |
| Unreal 저장소 | `C:\URproject\drone` (`gyeonliz/drone`, UE 5.8) |
| 이전 D PC | `D:\JGY\project\md`, `D:\JGY\project\drone` — 이 PC에는 없음 |

## 세션 시작 순서

1. `WORK_PC_START_HERE.md` → `CONTEXT.md` → `STATUS.md` → `WORKBOARD.md` 순으로 읽는다.
2. 두 저장소의 `git status`, `git log -1`, `git rev-list --left-right --count origin/main...main`으로 실제 상태를 대조한다.
3. 상세 주제는 `docs/README.md`에서 필요한 문서만 찾아 읽는다. `docs/history/DRONE_WORKLOG.md`(계속 증가하는 대용량 문서)는 통째로 읽지 말고 검색한다.

## 응답·작업 방식 (Codex 대화에서 이관, 2026-10-01)

- 한국어로 답하고 Commit 메시지도 한국어로 쓴다.
- 정확성 우선. 확인하지 않은 기능을 있는 것처럼 말하지 않고, 미확정은 "현재 미정"으로 구분한다.
- 사용량(토큰)을 아낀다. 필요한 범위만 읽고 `docs/history/DRONE_WORKLOG.md`는 검색으로만 본다.
- 기능 단위로 완성·테스트한 뒤 다음으로 넘어간다. 작업은 1~3시간 크기로 쪼갠다.
- 새 시스템 설명 순서: 왜 → 담당 클래스 → 헤더 → CPP → Blueprint 설정 → Editor 테스트 → 정상 결과 → 문제 시 확인 항목.
- Figma `Project Droner`와 Trello는 읽기 전용이다. 자세한 이관 내역은 `docs/git/CODEX_CONTEXT_SYNC.md`의 2026-10-01 절에 있다.
- 이 문서 저장소와 Drone Space는 Codex 담당, Unreal 코드는 Claude Code 담당. 코드 변경 요청을 받으면 WORKBOARD 카드로 남긴다. 협업 절차는 [Claude↔Codex 협업 규칙](docs/git/CLAUDE_CODEX_COLLABORATION.md)을 따른다.

## Claude 환경에서 달라지는 점

- **Drone Space(ChatGPT Pages)는 Codex가 갱신한다.** Claude 직접 접근 불가와 Codex 저장 실패를 구분해 보고한다. 저장 후 재조회로 확인하기 전 동기화 완료라고 쓰지 않는다.
- Trello는 연결된 커넥터가 있을 때만 읽기 참고로 쓴다.
- 문서 안의 "Codex"는 당시 작업 도구를 가리키는 이력이다. 기존 문서의 기록을 바꾸지 말고, 새 기록은 실행 담당과 문서 반영 담당을 따로 적는다(예: 작업 도구 Claude, 문서 반영 Codex).
- 진행 상황을 기록할 새 파일을 만들지 않는다. `STATUS.md`, `WORKBOARD.md`, `docs/history/DRONE_WORKLOG.md`에 반영한다.
- Commit/Push는 사용자가 요청할 때만 한다(GitHub Desktop으로 사용자가 처리하는 것이 기본).
