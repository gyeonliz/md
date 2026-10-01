# Drone Spaces 연동과 갱신 규칙

설정일: 2026-10-01 (Asia/Seoul)

로컬 MD는 개발 기준과 상세 이력, Spaces는 팀원이 쉽게 읽을 진행상황·테스트·조정 가이드로 사용한다. 관련 작업 마무리와 최신화 요청 때 양쪽을 갱신한다. Unreal 에셋 저장소나 Git LFS를 Spaces로 옮기는 작업은 아니다.

## 연결 대상

- Space: `Drone 프로젝트`
- Space ID: `page_space_0d47818e41608191bc3c83a1c0aaea15`
- Space 루트 Page ID: `page_6abdb1fbe86481919a1be745d3a85fa2`
- [프로젝트 안내와 갱신 규칙](https://chatgpt.com/space/page_75732d3acd6481919ba26bf5b0b972cd)

| 정본 Page | 로컬 근거 | 용도 |
|---|---|---|
| [진행상황과 다음 작업](https://chatgpt.com/space/page_a81d11314f60819188530a4ea2ed4663) | STATUS.md, WORKBOARD.md, 현재 Git·코드 | 현재 구현, 미완료, Trello 대조, 다음 개발 |
| [테스트 맵과 확인 가이드](https://chatgpt.com/space/page_ba2823e59d7c8191b0ea8bab809367dc) | 최신 진입/시험 가이드, 맵·기본 Entry | 맵별 테스트 기능과 수동 통과 기준 |
| [기획과 개발 기준](https://chatgpt.com/space/page_5508036c3eec8191a54b42343643e552) | CONTEXT.md, 확정 사용자 기획 | 게임 흐름, 경계, 맵 소유권 |
| [Blueprint 조정과 팀원 가이드](https://chatgpt.com/space/page_90d36613770c819182701fa5869ba17a) | 기능별 최신 코드·팀원 가이드 | Gate·NPC·차량·Weather 조정 위치 |

같은 목적으로 새 Page를 만들지 않는다. 위 페이지의 관련 부분을 수정하고 사람의 기획/디자인과 날짜별 이력을 보존한다. 연결 대상이 접근 불가·삭제된 경우 임의로 다른 Space를 만들지 않고 미반영 범위를 보고한다.

## 갱신 시점과 순서

1. 관련 개발 작업 마무리, 최신화, 진행 보고, 기획/계획의 실질적 변경 때 수행한다. 단순 질의마다 전체 문서를 재독하거나 동기화를 반복하지 않는다.
2. Git·코드·설정·실행 로그와 최신 STATUS/WORKBOARD를 대조한다. 필요 범위만 읽는다.
3. 현재 상태는 STATUS, 실행 순서는 WORKBOARD, 날짜별 수행 이력은 DRONE_WORKLOG에 정리한다.
4. Spaces의 기존 대상 Page와 지침을 읽고 현재 상태/미확인/다음 작업을 해당 주제에 반영한다. 기존 ID·hash·sequence로 변경을 보호하고 적용 결과를 확인한다.
5. 사람이 조작해야 하는 항목은 자동화 성공만으로 수동 Pass/Done 처리하지 않는다. 검증 날짜·환경·다른 PC 결과·현재 PC 확인을 구분한다.
6. 완료 요약과 링크, 미반영 사항을 알려준다. 접근 불가 시 로컬 작업은 보존하고 Spaces 최신화 실패를 명시한다.

원본 GitHub 링크는 Push된 버전만 보여 준다. 미커밋 MD와 Git에서 제외된 Saved 실행 보고서가 온라인에도 있다고 주장하지 않는다. 로컬 코드/파일을 읽을 수 없는 Cloud 실행은 로컬 변경이나 Build 상태를 확인할 수 없으며 마지막 근거와 접근 한계를 기록한다.

## Trello 참고 기준

[드로너 보드](https://trello.com/b/1WHjJMf9/드로너)는 사용자 제공 계획 참고다. 2026-10-01 API는 인증 필요로 읽지 못했으나 기존 로그인 Chrome에서 읽었다. 현재 보이는 카드 74개이며 담당자별 박정환 12·전유경 21·정규연 25·이수림 6·맹보민 5, 나중에 할 일 2·후순위 2·이거 가능해요? 1의 구조다. 전체 카드 본문·첨부·보관된 카드를 모두 검토했다는 뜻은 아니다.

| 참고 카드 | Trello 표기 | 코드/작업 판단 |
|---|---|---|
| [랩 기록 저장](https://trello.com/c/KpHNEtFa) | 미완료 | 실행 메모리 기록만 있으며 SaveGame 필요 |
| [Mission 목표 데이터화](https://trello.com/c/dMXHThh0), [목표 연결](https://trello.com/c/Eg90YRHy) | 미완료 | Definition·Rule·Trigger 기반/간이 맵은 있고 실제 콘텐츠·실패·UI 연결은 후속 |
| [Chaos 그물·파괴](https://trello.com/c/5rCvvFA9) | 미완료 | Runtime Greybox와 실제 Chaos Cloth/Geometry Collection 완성을 구분 |
| [차량 루트·도착 종료](https://trello.com/c/ES7ZAqQG) | 미완료 | Spline 주행·간이 목적지 실패 기반과 실제 Mission 종료 연결을 구분 |
| [벽면 날개 충돌](https://trello.com/c/KRrzBnr5), [그물 배치](https://trello.com/c/j0r6n8nI) | 미완료 | Probe·반발·얽힘 기반과 최종 수동 검증/자산 작업을 구분 |
| [레이싱 시작 3·2·1](https://trello.com/c/FGfMmLV3) | 미완료 요구 | 별도 카운트다운 후속 작업으로 유지. 구현 완료로 표시하지 않음 |
| [Gate 사운드](https://trello.com/c/u9Dfasi4), [하단 위치](https://trello.com/c/kp0m2DIq), [크기 분리](https://trello.com/c/rFNi6Ae8), [머터리얼](https://trello.com/c/sMz9hU1Z) | 완료 | 코드 슬롯/배치/크기/재질 기반은 있음. 최종 음원·Mesh 연결/수동 확인은 별도 |
| [튜토리얼 기획](https://trello.com/c/Ok68Sj3X) | 체크 1/4 | 기본조작만 체크. UGV·Drop·FPV 시험 구현과 기획/체크 완료를 혼동하지 않음 |

카드 상태를 자동 변경하지 않는다. 계획과 구현이 다르면 차이를 현재 진행 페이지에 기록한다. 수동 카드 변경은 사용자 요청 후 처리한다. 계정/공유 권한을 자동 추가하지 않는다.

## 지속 지침과 한계

- 문서/Unreal 저장소의 AGENTS.md와 현재 대화 작업 폴더의 AGENTS.md에 연결 규칙을 저장했다. 프로젝트 지침은 [공식 AGENTS.md 동작](https://learn.chatgpt.com/docs/agent-configuration/agents-md)에 따른다. 다른 PC에는 저장소 지침을 Commit/Push/Pull한 뒤 해당 프로젝트 작업에서 사용한다.
- 상시 폴더 감시, 예약 자동화, Cloud auto-update Controller는 만들거나 켜지 않았다. 지금은 작업 세션 안에서 근거를 확인한 뒤 갱신하는 방식이다.
- Space 루트 본문과 네이티브 Agent Instructions 삽입은 현재 도구의 invalid_page_schema 거부로 적용하지 못했다. 루트/다른 문서를 삭제하거나 재생성하지 않았고, 위 안내 Page와 로컬 지침을 정본으로 사용한다.
- 대용량 .uasset/.umap, API 키·인증정보·개인 로그는 업로드하지 않는다. 기존 Git/LFS 전달과 공유 권한을 그대로 유지한다.
- Git Commit/Push, Trello 수정, 외부 공유 권한 변경은 별도 사용자 지시가 필요하다. 이번 연결은 코드·자산을 변경하거나 엔진 Build를 실행하는 작업이 아니다.
- Page 저장 결과와 본문/계층 확인은 가능하지만 사용자 화면의 모든 폭에서 레이아웃을 검증한 것은 아니다.

## 2026-10-01 연결 결과

Unreal 수신 `83b33c1`, 문서 수신 `aecb6ec` 기준을 반영했다. Title/로비/독립 Tutorial 8·Story 4·Racing 1, Gate/물리/AI/날씨·환경 이식을 요약하고 미완료와 검증 출처를 분리했다. Trello 주요 카드 링크와 대조를 같은 진행 Page에 반영했다. 두 저장소의 기존 Clean은 연결 설정 이전 확인이며 이후 MD 변경과 새 AGENTS.md는 로컬 미커밋 상태다. Commit/Push·Trello 수정·권한 변경은 하지 않았다.
