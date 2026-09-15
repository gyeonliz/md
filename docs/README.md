# Drone 상세 문서 안내

일상 작업에서는 루트의 [`STATUS.md`](../STATUS.md)와 [`WORKBOARD.md`](../WORKBOARD.md)만 보면 된다. 아래 문서는 특정 기능을 구현하거나 팀원에게 작업법을 전달할 때 연다.

## Planning

- [`DRONE_PROJECT_PLANNING_BRIEF.md`](planning/DRONE_PROJECT_PLANNING_BRIEF.md): 전체 기획·개발 현황서
- [`DRONE_FRONTEND_MISSION_FLOW_PLAN.md`](planning/DRONE_FRONTEND_MISSION_FLOW_PLAN.md): 트레일러·로비·미션 선택·진입 흐름
- [`DRONE_TUTORIAL_STORY_PLAN.md`](planning/DRONE_TUTORIAL_STORY_PLAN.md): Tutorial·Mission·Jamming 실행 순서
- [`DRONE_FIGMA_MISSION_IMPLEMENTATION_MATRIX.md`](planning/DRONE_FIGMA_MISSION_IMPLEMENTATION_MATRIX.md): Figma 4개 Mission 요구와 현재 코드/남은 작업 대조
- [`DRONE_PREASSET_FUNCTION_PLAN.md`](planning/DRONE_PREASSET_FUNCTION_PLAN.md): 구매 에셋 전 기능 계획
- [`DRONE_MVP_GUIDE.md`](planning/DRONE_MVP_GUIDE.md): 전체 MVP 카드 참고
- [`WORK_MANAGEMENT.md`](planning/WORK_MANAGEMENT.md): 보드 운영 원칙

## Tutorial·HUD

- [`DRONE_TRAINING_AUTHORING_GUIDE.md`](tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md): Spline·Ring·Gate 배치
- [`DRONE_TRAINING_COURSE_IMPLEMENTATION.md`](tutorial/DRONE_TRAINING_COURSE_IMPLEMENTATION.md): Course 구현
- [`DRONE_TRAINING_RECORDING_IMPLEMENTATION.md`](tutorial/DRONE_TRAINING_RECORDING_IMPLEMENTATION.md): Segment·Lap·평균·Best 기록
- [`DRONE_TELEMETRY_IMPLEMENTATION.md`](tutorial/DRONE_TELEMETRY_IMPLEMENTATION.md): 속도·고도·HUD 데이터
- [`DRONE_PROTOTYPE_IMPLEMENTATION.md`](tutorial/DRONE_PROTOTYPE_IMPLEMENTATION.md): Prototype Pawn 구현
- [`DRONE_PROTOTYPE_INPUT_CONTRACT.md`](tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md): 입력 계약
- [`DRONE_PROTOTYPE_PIE_CHECKLIST.md`](tutorial/DRONE_PROTOTYPE_PIE_CHECKLIST.md): 입력 수동·자동 검증

## AI·Smart Object·Turret

- [`DRONE_SMART_OBJECT_ROUTE_EDITING_GUIDE.md`](ai/DRONE_SMART_OBJECT_ROUTE_EDITING_GUIDE.md): 팀원용 동선·방향·NavMesh 조정 절차
- [`DRONE_SMART_OBJECT_NPC_GUIDE.md`](ai/DRONE_SMART_OBJECT_NPC_GUIDE.md): NPC·StateTree·Smart Object 전체 계약
- [`DRONE_NPC_GAZE_TRACKING_PLAN.md`](ai/DRONE_NPC_GAZE_TRACKING_PLAN.md): 감지 뒤 시선·고개 회전
- [`DRONE_MG_TURRET_3PART_GUIDE.md`](ai/DRONE_MG_TURRET_3PART_GUIDE.md): 유인 MG 3분할 Mesh와 사수 Anchor
- [`DRONE_AUTOMATIC_TURRET_GUIDE.md`](ai/DRONE_AUTOMATIC_TURRET_GUIDE.md): 설치형·차량형 무인 자동포탑

## Gameplay·Physics

- [`DRONE_TYPES_AND_CONTROL_MODES.md`](gameplay/DRONE_TYPES_AND_CONTROL_MODES.md): Drone 역할과 조작 모드
- [`DRONE_WEATHER_WIND_RAIN_PLAN.md`](gameplay/DRONE_WEATHER_WIND_RAIN_PLAN.md): 구현된 Profile·지속풍/돌풍 Runtime·시험 맵과 남은 Niagara 최적화 계획
- [`DRONE_MISSION_OBJECTIVE_RULE_GUIDE.md`](gameplay/DRONE_MISSION_OBJECTIVE_RULE_GUIDE.md): 목표 Rule·Event·Blueprint 설정과 검증
- [`DRONE_JAMMING_GREYBOX_GUIDE.md`](gameplay/DRONE_JAMMING_GREYBOX_GUIDE.md): 재밍 신호·비행·HUD·Mission Zone 배치와 PIE 시험
- [`DRONE_TEST_MAP_GUIDE.md`](gameplay/DRONE_TEST_MAP_GUIDE.md): Tutorial·AI/Smart Object·Mission/Signal 시험 맵 위치와 수동/자동 검증
- [`DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md`](gameplay/DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md): 4점 차량·Drone 기울기·피격 흔들림
- [`DRONE_CHAOS_DATAFLOW_PLAN.md`](gameplay/DRONE_CHAOS_DATAFLOW_PLAN.md): 그물·파괴 Physics Spike

## Assets

- [`DRONE_CONTENT_FOLDER_GUIDE.md`](assets/DRONE_CONTENT_FOLDER_GUIDE.md): Content 폴더와 이식 경계
- [`DRONE_ASSET_INTAKE_2026-08-25.md`](assets/DRONE_ASSET_INTAKE_2026-08-25.md): 최초 제공 에셋 감사
- [`DRONE_REMAINING_ASSET_MIGRATION_2026-08-27.md`](assets/DRONE_REMAINING_ASSET_MIGRATION_2026-08-27.md): 후속 선별 이식

## Git·협업·도구

- [`GIT_UNREAL_GUIDE.md`](git/GIT_UNREAL_GUIDE.md): Unreal Git/GitHub 실전 절차
- [`DRONE_TEAM_SYNC_PLUGIN_CHECKLIST.md`](git/DRONE_TEAM_SYNC_PLUGIN_CHECKLIST.md): 팀원 Pull·LFS·Plugin 점검
- [`DRONE_GIT_LFS_CAPACITY_PLAN.md`](git/DRONE_GIT_LFS_CAPACITY_PLAN.md): LFS 용량·비용 절감 계획
- [`CODEX_CONTEXT_SYNC.md`](git/CODEX_CONTEXT_SYNC.md): PC 간 작업 문맥 전달
- [`DRONE_UNREAL_MCP.md`](git/DRONE_UNREAL_MCP.md): Unreal MCP 연결 경계

## Reference·Learning

- [`DRONE_CODE_STRUCTURE_AND_USER_TASKS.md`](reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md): 코드·Asset 책임 상세 사전
- [`external-engineering/README.md`](reference/external-engineering/README.md): 외부 저장소 검토와 팀 Playbook
- [`CS_GAMEDEV_READING_PLAN.md`](learning/CS_GAMEDEV_READING_PLAN.md): CS·게임개발 추천자료 읽기
- [`STUDY_PLANS.md`](learning/STUDY_PLANS.md): 자격증·코딩테스트 계획
- [`UNREAL_PROJECT_EXPERIENCE_DESCRIPTION.md`](learning/UNREAL_PROJECT_EXPERIENCE_DESCRIPTION.md): 지원서 경험 기술 예시
- [`MOBILE_CURRENT_BRIEF.md`](learning/MOBILE_CURRENT_BRIEF.md): 과거 이동용 통합 요약. 현재 상태는 루트 문서를 우선한다.

## History

- [`DRONE_WORKLOG.md`](history/DRONE_WORKLOG.md): 날짜별 개발 기록
- [`DRONE_TRELLO_BOARD_2026-09-09.md`](history/DRONE_TRELLO_BOARD_2026-09-09.md): 2026-09-09 Trello 입력본
- [`DRONE_PROJECT_AUDIT.md`](history/DRONE_PROJECT_AUDIT.md): Prototype 구현 전 감사
- [`snapshots/2026-09-15`](history/snapshots/2026-09-15): 정리 전 장문 루트 문서 원본

History와 오래된 상세 문서의 Commit ID·현재 상태 문구는 당시 기록이다. 최신 판단에는 사용하지 않는다.
