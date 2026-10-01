# Claude ↔ Codex 협업 규칙

정한 날: 2026-10-01. 사용자 결정: "코드는 Claude, 나머지 영역은 Codex".
작성: Claude가 초안을 쓰고, Codex가 넘긴 규칙(Unreal 저장소 `.claude/codex-bridge/runs/20261001-184649-research-codex-rules`, 근거 파일 명시)을 합쳤다. 다른 PC 세팅은 [CLAUDE_CODEX_SETUP.md](CLAUDE_CODEX_SETUP.md).

## 1. 역할

| 영역 | 담당 | 비고 |
|---|---|---|
| `Source/Drone` C++, Build, 자동화 테스트, Unreal 도구·맵 생성 스크립트 실행 | **Claude** | Codex는 샌드박스상 Unreal 저장소를 쓸 수 없다 |
| md 저장소(STATUS·WORKBOARD·WORKLOG·가이드) | **Codex** | Claude는 사실을 담은 지시서로 맡긴다 |
| Drone Space 페이지 5개 | **Codex** | Claude 도구로는 접근 불가 |
| Figma·Trello 대조, 보고서·제출 서류, 기획 선택지 정리 | **Codex** | Figma·Trello는 읽기만 |
| Claude 변경 교차 리뷰, 원인 조사 의견 | **Codex** | 읽기 전용. 반영 여부는 Claude가 검증 후 결정 |
| Commit/Push, Trello 카드 수정, 공유 권한 변경 | **사용자** | 둘 다 요청 없이는 하지 않는다 |

## 2. 흐름

```
사용자 ──요청──▶ Claude ──(코드·Build·테스트)──▶ 결과 검증
                   │
                   ├─ 지시서 → Unreal 저장소 .claude/codex-bridge/Invoke-CodexTask.ps1 → Codex(docs/review/research)
                   │                                    │
                   ◀──── result.md ◀──────────────────────┘
                   │  Claude가 git diff·로그로 검증
                   ▼
                사용자 보고 (Codex가 한 일 / Claude 검증 결과 구분)

사용자 ──요청──▶ Codex 앱(직접 대화)
                   └─ 코드 변경 요청이면 직접 고치지 않고 WORKBOARD 카드로 남김 → Claude가 다음 세션에서 처리
```

- Claude → Codex: Unreal 저장소 `.claude/codex-bridge/Invoke-CodexTask.ps1` (절차는 `codex-handoff` 스킬).
- Codex → Claude: 결과 보고의 "Claude에게 넘길 코드 작업", 또는 WORKBOARD 카드(아래 5절).
- 한쪽만 고친다. Claude가 코드 작업 중이면 Codex는 읽기 전용 역할만 맡는다.

## 3. 지시서 고정 칸 (Codex 요청 반영)

Codex는 이 대화를 모른다. 지시서는 Unreal 저장소 `.claude/codex-bridge/BRIEF_TEMPLATE.md`의 칸을 모두 채운다. 결과가 없는 칸은 "미실행/미확인", 파일이 없는 칸은 "현재 PC에 없음"으로 적는다. 빈칸으로 두면 Codex가 완료로 잘못 판정할 수 있다.

필수: 역할·범위·제외 / 기준(날짜·PC·Commit·미커밋 파일) / 변경 사실 / 검증 출처(테스트명·수치·조건·보고서 경로, 자동과 수동 경계) / 문서 대상(카드 ID·STATUS 항목·가이드, 새 파일 여부) / Space 범위 또는 "Space 제외" / 확정·미정 사항 / 근거 위치(로그·Figma 슬라이드·Trello 링크).

## 4. 문서 규칙 (Codex 규칙 1절)

| 문서 | 쓴다 | 쓰지 않는다 |
|---|---|---|
| `STATUS.md` | 현재 구현 상태, 검증 범위, 알려진 문제, 미구현·미정 | 계획만으로 완료 판정, 다른 PC 결과를 현재 PC 결과로 |
| `WORKBOARD.md` | Now/Next 순서, 카드, 상태, 완료 조건 | 자동 검증만으로 수동 완료, Trello 완료 표기 그대로 수용 |
| `docs/history/DRONE_WORKLOG.md` | 날짜별 수행·검증 결과와 출처, 실패·미반영 (끝에 추가) | 과거 기록의 작업 도구 소급 변경, 전체 재독 |
| 주제별 `docs/...` | 책임·설정·진입·검증 절차·정상 결과·문제 확인 | 범위 밖 전체 최신화, 미확정 기획을 확정값처럼 |

- 진행 기록용 새 파일을 만들지 않는다(지시서가 명시하면 예외).
- 날짜 `2026-10-01`(Asia/Seoul). 같은 날 여러 번이면 "후속"·"저녁"으로 구분.
- PC·경로·Commit·미커밋 변경을 같이 적는다. 소스 수신과 최신 바이너리·실제 플레이 성공을 구분한다.
- **구현됨 / 자동 검증됨 / 수동 확인 대기 / 미구현**을 나눈다. NullRHI/NoSound 성공을 렌더·소리·실제 패드 확인으로 넓히지 않는다.
- **실행 담당과 문서 반영 담당을 따로 적는다.** 예: "작업 도구 Claude, 문서 반영 Codex". 지시서에서 전달받은 결과와 Codex가 직접 읽은 증거도 구분한다.

## 5. Codex → Claude 코드 작업 카드 (Codex 규칙 4절)

WORKBOARD 표의 기존 칸 `ID | 작업 | 현재 상태 | 완료 조건`을 그대로 쓴다.

| 칸 | 내용 |
|---|---|
| ID | 기존 카드 ID 또는 새 주제 ID(`주제-기능-번호`, 예: `AI-SHOTGUN-REGRESS-01`) |
| 작업 | 해결할 문제, 변경 대상 파일·클래스·자산 |
| 현재 상태 | 재현 상황, 확인된 사실과 가설 구분, 날짜·PC·출처 |
| 완료 조건 | 기대 동작, 필요한 자동 회귀, 별도 수동 확인, 지킬 계약(`Source/Drone`·`/Game/Drone`, Legacy 금지, Production `Lvl_DroneTraining` 보존, TestMap 검증) |

Codex가 읽기 전용(`review`/`research`)으로 돌 때는 카드를 직접 쓰지 않고 결과 보고에 적는다. 기록이 필요하면 Claude가 `docs`로 다시 맡긴다.

## 6. Drone Space 규칙 (Codex 규칙 2절)

Space `Drone 프로젝트`(ID `page_space_0d47818e41608191bc3c83a1c0aaea15`). 대상과 링크는 md 저장소 `docs/git/DRONE_SPACES_SYNC.md`가 기준이다.

| 페이지 | 용도 |
|---|---|
| 프로젝트 안내와 갱신 규칙 | 동기화 안내·지속 지침 |
| 진행상황과 다음 작업 | STATUS·WORKBOARD 기준 구현·미완료·다음 작업·Trello 차이 |
| 테스트 맵과 확인 가이드 | 맵별 진입·시험 기능·수동 통과 기준 |
| 기획과 개발 기준 | CONTEXT·확정 기획(사용자 결정 없이 바꾸지 않음) |
| Blueprint 조정과 팀원 가이드 | Gate·NPC·차량·Weather 조정 위치 |

절차: 근거 대조 → MD 반영 → 대상 Page 읽기 → 관련 부분만 수정(기존 ID·hash·sequence 보호) → 재조회로 확인 → 링크·미반영 보고.
금지: 같은 목적의 새 Page·대체 Space 생성, 사람의 기획·이력 삭제, 대용량 에셋·인증정보 업로드, 미커밋 MD가 GitHub에 있다고 주장.
실패 시: 로컬 기록 보존, 실패 페이지·미반영 내용·이유를 남긴다.

비대화형 Codex의 Space 저장은 도구 승인이 필요하다. 2026-10-01 첫 위임에서 `approval policy is never`로 막혔고, 이후 브리지의 `docs` 역할은 `--approve-for-me`(자동 검토)로 실행한다.

## 7. 결과 검증과 보고

- Claude는 Codex 결과를 그대로 전달하지 않는다. docs는 md `git diff`로 지시서 밖 사실·수치가 들어갔는지, review/research는 지적마다 코드·로그로 확인한다.
- 사용자 보고에는 Codex가 한 일, Claude가 검증한 것, Space 반영 여부, 미커밋 상태를 나눠 쓴다.
- 호출마다 사용자의 Codex 사용량이 든다. 기본 추론 강도 `medium`, 리뷰·원인 조사 `high`, `xhigh`는 요청 시만. 같은 위임을 반복하지 않는다.

## 8. 알려진 충돌·낡은 규칙 (Codex 규칙 6절) — 정리 계획

| 위치 | 문제 | 처리 |
|---|---|---|
| md `CLAUDE.md` 서두·새 기록 지침·Space 처리 | "문서 저장소가 Claude로 이관", "새 기록 도구는 Claude", "Claude 접근 불가라 로컬만" — 지금은 md·Space가 Codex 담당 | Codex `docs`로 수정 |
| md `WORK_PC_START_HERE.md` | D 경로 예시가 기본처럼 적힘, 이전 `9f67706`·목록 튐 미수정 상태 잔존, Build/PIE를 Codex 흐름에 연결 | Codex `docs`로 수정 |
| md `docs/git/CODEX_CONTEXT_SYNC.md` | 종료 절차에 Commit/Push가 무조건 단계처럼 적힘 | "사용자 지시 시에만" 연결 — Codex `docs` |
| Unreal `AGENTS.md` | Space 동기화 문서를 `../md/...` 상대 경로로 가리킴(C PC는 인접 폴더 아님) | Claude 수정 완료 |
| md `tools/work-pc` | README 없음 | 보류(필요 시 Codex) |
| Space 루트 네이티브 지침 | `invalid_page_schema`로 미등록 | 등록 완료로 쓰지 않는다 |
