# Drone 문서 작업 지침

- 실제 Git·코드·설정·실행 로그를 우선한다. 상태/계획 작업은 STATUS.md와 WORKBOARD.md를 확인하고 관련 상세 문서만 읽는다.
- 관련 개발 작업 마무리, 최신화, 진행 보고 때 로컬 MD와 연결된 Drone Space의 해당 페이지를 함께 갱신한다. 연결 대상과 절차는 docs/git/DRONE_SPACES_SYNC.md에 있다.
- 진행 페이지를 새로 누적하지 않고 기존 페이지를 수정한다. 구현됨·자동 검증됨·수동 확인 대기·미구현과 검증 날짜/PC를 구분한다.
- Trello는 계획 참고로 읽기만 한다. 카드 완료 표시는 코드/수동 검증의 근거와 따로 대조한다. 카드 수정은 별도 사용자 요청이 필요하다.
- Spaces에 접근할 수 없으면 로컬 갱신을 유지하고 미반영 범위를 보고한다. 동기화 완료·Build·수동 Pass를 추정하지 않는다.
- 사람의 기획/디자인, 날짜별 기록, 팀원 Production Training 맵을 보존한다. 대용량 에셋·비밀 키·개인 로그를 업로드하지 않는다.
- Commit/Push, 공유 권한 변경, 예약 자동화는 별도 사용자 지시 없이 하지 않는다. 문서 최신화만으로 엔진 Build나 맵 재생성을 실행하지 않는다.
- 이 문서 저장소와 Drone Space는 Codex 담당, Unreal 코드는 Claude Code 담당. 코드 변경 요청을 받으면 WORKBOARD 카드로 남긴다. 협업 절차는 [Claude↔Codex 협업 규칙](docs/git/CLAUDE_CODEX_COLLABORATION.md)을 따른다.
