# Drone 작업 보드

마지막 갱신: 2026-10-27 D PC — 3장치 키 설정·패드 RightY/Cancel 보완, 공식28검사·UI4장 확인. 검사창 정리 후 UI3연속도 통과했으며 실물 비행체감은 대기다. [STATUS](STATUS.md)·[WORKLOG](docs/history/DRONE_WORKLOG.md).

## Now

최신 절차는 [카메라/자폭](docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md)·[설정/UI](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md)·[Story 단계](docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md)다. 입력33/OFF34와 중간 실패·수선 실행은 최신 검증과 중복 합산하지 않는다.

### 결정 필요 — 현재 DA 값은 채택 사양이 아님

| 항목 | 필요한 결정/자료 | 현재 처리 |
|---|---|---|
| M2 | 실제 타겟 탑승 vs 미끼 결말·시스템 성공/실패·다음 Story Fact | D-1 보류(2026-10-05 사용자): 기획자 내용 대기. 양쪽 분기 기반 유지, M3 반대 분기 첫 대사 비어 있음 |
| M3/M4 | 최종 전투 배치·시간/결과 카메라·시작지점 안전성 | 현재 초기 FiberOptic→재머 전부 해제→전투4종 재선택, M3 실제 거점 방어/M4 실제 Patriot 전부. 진행 보존 무한 출격·M4 3지점 유지. 손 조종/최종 전략 배치는 후속. [정본](docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md#실패-처리와-체크포인트) |
| 조종 입력 표시 | 실물 좌/우 스틱 표시·혼합 입력 | 기본 끔/설정ON·OFF 유지. 패드/RC 물리축과 비행액션 분리, 모드4종·실제HUD PIE 통과. 실물 손조종 확인 대기 |
| 레이싱 | 지형/4코스 진행도 대조, Ghost/리플레이·커브·Restart/Quit 범위 | 팀원3맵 연결·완주/복원 자동 통과, 실제 조종·후속 규칙 대기; RACING-TERRAIN-LINK-01 |
| Tutorial | 수업8개 유지, 권장문구/건너뛰기 정책 | D-4 수업1~8 유지·회의 “4”는 고정 레이싱 코스4개. 진행도 JSON 저장은 수신 코드에 구현됨; 재실행 확인은 TUT-COMPLETION-SAVE-01 |
| Bangkok 의존 자산 | 방콕·다른 구매/팀원 자산 정리 범위 | D-13 종료(10/05 사용자 결정): 방콕만 삭제, 자연환경 팩·지형 머티리얼·병사 팩·HDRI·RawDrones·NavigationArrows 유지. 삭제 커밋·푸시 상태는 별도 확인 |
| 콘텐츠/전시 | 캐릭터 메시·관찰 시점 적용 맵·조종기 비치/책임, 기록 등급, 브리핑 실명/납품일, 행사일 | 임의 실명·수치·마감일 없음 |



D-7 구매 자산 공개/공유·D-8 기여/AI 설명·BP/Legacy API 정리와 스냅숏 백로그는 결정 대기다. 완료/종료 카드·이전 근거·지난 Next·해당 결정표 원문은 [10월 보드 아카이브](docs/history/archive/WORKBOARD_2026-10.md)에 보존했다. 현재 수동 순서는 [테스트 가이드](docs/gameplay/DRONE_TEST_MAP_GUIDE.md)를 따른다.

### 카드 그룹

회의 후 카드는 각 그룹 맨 앞에 둔다.

#### 튜토리얼·코스·레이싱

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| INPUT-KM-VERTICAL-01 | 키마 상승·착지 | 쉬운/게임 Ctrl 하강→접지OFF, 집중10건 통과 | 손 조작 확인·FPV/패드/RC 정책 유지. [입력](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md) |
| RACING-RANDOM-UI-01 | 공통 결과·게이트 화살표 | 전용4건·viewport4건·제목1280 확인 | [범위](docs/planning/DRONE_RANDOM_CITY_RACING_PROPOSAL_2026-10-27.md) |
| INPUT-PHYSICS-RECHECK-01 | 3장치 키 설정·패드 RightY/Cancel | 고유28최종통과·실제화면20경로·UI4장/정리3건 재검증 | 실물 RC/PS 비행·체감 확인 |
| TUT-OBSERVER-01 | 첫 LOS 관찰·후퇴 | 수평 후퇴/메시 Yaw·고정 카메라 추적, 이륙→전진→후진→접지 자동 계약 통과 | World 연결 캡처·HitResult 디코더 수리 후 실제 사람/드론 가시성. 높이 원인 미확정 |
| TUT-GATE-SAVE-01 | Gate BP 저장 사고 | CDO MID 참조 원인 수정·Gate BP 수리, 재로드3회·Gate5/5 성공(기존 경고100) | 팀원 Source+BP 수신/종료 후 Build·같은 저장 실기. 기하/색·16개 유지, Production 미수정 |
| TUT-COURSE-SMOOTH-01 | 장거리 코스 표시선 곡률 분할·BP 표시 예산 | 구현됨·자동 검증됨·수동 확인 대기(10/04 C PC Claude). 긴 코스 곡률 분할·기본1024(시작값·미확정), BP 드래그 재구성 Off. 수치·근거 STATUS/WORKLOG | 팀원 Production 코스 외형·급커브/끝 연결·Editor 편집 체감 수동 확인. BP2048(측정 최대20cm) 검토 가능. 짧은 TestMap68/113조각 기존 균일 분할 유지·Production 저장/재생성 금지 |
| RACING-TERRAIN-LINK-01 | 레이싱 흐름·지형 연결 | 본체 단독 연결 오류 정정·프로펠러4개/BP 선택3D 복구. 원형/도시 출격·회전 중심·3D 검사 통과; WORKLOG | 손 조종 완주·HUD/기록 체감·원본 맵 보존 |
| TUT-PROGRESS-01 | 튜토리얼 시간·연속 진행·전체 완료 | 이전 자동 검증 WORKLOG. 수신 코드의 완료 미션/Story Fact JSON 저장은 TUT-COMPLETION-SAVE-01 | 실제8수업·현재 결과창·로비 완료 표시/재진입 확인. Production Training 보존 |
| TUT-BRIEFING-TEXT-01 | 훈련 문구·시작 안내 | 기획 문구·역할 조작·기본 훈련 시작 안내 구현(Claude), 수동 대기 | 패드/Enter 시작·목표/안내 확인. 기획8개↔UGV NPC 매핑·미기재 화자/키 결정 |
| TUT-COMPLETION-SAVE-01 | 미션 진행도 영구 저장 | 10/13 수신 소스 확인: 완료 미션·Story Fact·권장문구 표시 여부 JSON 저장/복원 구현. Best Lap 저장과 별개 | 실행 담당이 현재 HEAD 회귀 확인 후 실제 성공→종료→재실행 복원·저장 실패 처리를 확인. 수신만으로 자동/수동 Pass 아님 |
| TUT-ORBIT-02 | 회전 수업 = 원형 코스 한 바퀴 | Heading ID 유지·실제 TUT_Circle_Gate 완주→즉시 성공 자동 통과, 귀환 제거 | 손 조종으로 순서/역방향/7⁄8 바퀴 미완료 확인 |
| TUT-GATE-PRESENTATION-01 | Gate 크기·방향·3색 | 상태별 MI 자동 우선·빈칸 BP 기본색/발광·Param/Color 호환. Build53.04초·Gate4/4. Island정합/Scale수리 유지. [조정](docs/tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md#세-상태-색과-머터리얼-조정) | 실제 코스 색/방향 확인·원본 맵 보존 |
| TUT-ROUTE-SELECT-01 | Training Route 4개 선택 시험 | `Lvl_DroneTrainingRouteSelectionTest`에 직선·좌곡선·우곡선·상승 슬라럼과 Gate 각 5개 배치. `1~4` 고정·`5` 무작위, 단일 활성, 진행 초기화, HUD 기록 Source 전환. Build·Map Check·API/저장/실제 키 PIE 성공 | 사용자가 화면에서 경로 형태·Gate 간격·랜덤 전환과 Lap HUD를 확인하고 각 Spline 점을 최종 조정 |
| TUTORIAL-MISSION-01 | Figma 수업별 Mission | 기존 ID/종합 시험장 보존, 현재 제품 TUT와 UGV NPC 별도 맵 사용. LOS 외 귀환 제거·호버3초 즉시 성공·물자/포탑 연결; 시험 가이드 | FrontEnd에서 각 수업 위치·목표·결과·실제 조종 확인. 자동 위치 이동 완료와 손 조종 완주 구분 |
| TUT-BEST-01 | Course별 Best Lap 영구 저장 | 구현됨·자동 검증됨·수동 확인 대기(10/02 C PC Claude). 코스/기체/조작별 Best Lap JSON·HUD, 자동화 별도 슬롯. 평균은 실행 History | 같은 조건 실제 완주2회·재실행 복원·첫 완주 전 HUD 확인. D-5 결과 시간은 RACING-TERRAIN-LINK-01 참조 |
| PROCEDURAL-RACING-01 | 시드 도시·외형 | 완성BP1체·닫힌모듈/슬롯재질·차선·소유 팔레트. 시드194849 화면/실제RHI21개 통과; STATUS | 지정/무작위·같은 시드·완주/기록 실기. 공급팩·Production 보존 |
| TUTORIAL-FIGMA-02 | Figma 8개 훈련 ↔ Test Map 대조 | 8개 기능/DA·독립 시험맵·시간·연속 진행·전체 완료 UI 구현과 기존 자동 검증 보고가 있음. 2026-10-03 DA 순서 재확인; Warehouse 최종 환경은 별도 | 기존 진행 UI의 실제 8수업 연속 완주·결과/로비 복귀를 수동 확인. D-4 수업1~8 유지·회의4는 레이싱 코스4개. Warehouse 범위 결정, 결과 UI 중복 구현 금지 |

#### UI·설정·패드

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| UI-WBP-EXPORT-01 | WBP 정리 | 화면22종·3D/6카드/Back 유지. 새 투명 PNG5장→6종, 사진 모드/카드1280·1920 자동 통과·캡처 확인. [정본](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#화면별-wbp-편집-정본) | Sky 긴 설명 간격·실물 패드 확인 |
| UI-HUD-WBP-01 | HUD·첫 경고 | 실제Race3/2/1/출발4PNG·M4 첫경고epoch4부터 배경/아이콘/문구 동시 확인 | 자동public flow/health/fire 주입 범위. 실물/청감·전체수동플레이 별도, AUDIO-USER-01 |
| AUDIO-USER-01 | 사용자 음원·실제 미션 | 실제Race/M4 조립2Success(경고포함)·local사망음 pause 수리·Build5, 직접영향 기존 DroneDestroyed/ImpactDestroyed/MasterMute3개 재검사 Success | 유인MG미배치·직전26전체재실행 아님. 손조종/실청·패키징 대기. [정본](docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md#사용자-오디오와-체력-경고) |
| UI-CONTROLS-DECISION-01 | 조작·흐름 결정 | 자폭 기본 무장/해제 잠금 반영, 나머지 미정 유지 | 기획 결정 후 연결. 드랍 L2/R1·FPV2 범례·수업 매핑·결과 다음 임의 확정 금지 |
| ASSET-SKYDRONE-01 | 스카이드론 외형 | Racing 본체+Sky 로터4개·선택 BP 연결/검증됨 | 조종 체감 확인 |
| TEST-HUD-LAYOUT-01 | HUD 실제 표시 확인 | D PC 자산5종·RHI5종·최종 파츠2종 통과,1280/1920 캡처. 상세 WORKLOG | 창 이동·실물 패드/연속 조종 수동 확인. 숨김 렌더와 구분 |
| UI-SELECT-ART-01 | 전체 Pretendard·선택명 | Native/Designer 10종 공통 적용·기존 크기/굵기 보존, 목록 끝 괄호만 숨김. 추가 렌더14/14·Story/설정 캡처 확인 | 실제 패드·1280/1920 가독성. DA/ID·아트 보존, 아이콘/명시 Opt-out 제외 |
| UI-CONTROL-LAYOUT-01 | 조작 이름·가로폭 | Codex 예외 수정·자동 Pass; WORKLOG | 1280/1920·패드 수동 확인 |
| UI-RESULT-LAYOUT-01 | 결과창 | Mission/WBP_DroneMissionResult에 배치 저장·실행 시 Designer 값 보존 | 현재 패드·다음/재도전/복귀 확인 |
| UI-LOADING-PAUSE-01 | 로딩·일시정지 | Story/Procedural 로딩·취소, 미션 일시정지/재시작/타이틀 복귀 연결을 소스로 확인 | 현재HEAD Build/회귀→Esc/Start·재개·같은 시드/취소 실기 확인. Pause 포커스 관찰은 UI-FOCUS-RACE-01 |
| UI-FOCUS-RACE-01 | UIOnly 첫 포커스 | 미렌더4건 재실행 통과는 Claude 인계. 원시 집계 차이 WORKLOG | 실제 패드 첫 강조·렌더 여부 대조, 안정화 확정 금지 |
| UI-MEETING-LOBBY-01 | 5메뉴·WBP 연결 | 이동 참조/TitleMenuClass 복구·구현, 상세 WORKLOG | 패드 순환·진입/복귀·B/Esc·해상도 확인 |
| UI-CONTROL-DISPLAY-01 | 조종 입력 표시 | WBP 참조 복구·설정/저장 구현, 기본 False 유지 | 위치·저장/재실행·기본값 복원. 장치 전환/분리 정책 미정 |
| UI-LAYOUT-DIAG-01 | 로비 레이아웃 진단 판정 변동 조사 | 진단 판정 변동·기존 Fail 유지. D-11로 KnownIssues.Flow.LobbyLayoutStabilityPIE 분리됨(10/05 C PC Claude), 안정화 완료 아님 | Claude가 표본/대기·레이아웃 원인을 구분하고 반복 렌더 검사 판정 안정화, 1280/1920 수동 확인 별도 |
| UI-LAYOUT-01 | 목록 진입·선택 시 한 프레임 재배치 | 구현됨·자동 검증됨·수동 확인 대기. 줄바꿈·상시 스크롤바·폭270 후속 포함. 최신 진단 분리는 UI-LAYOUT-DIAG-01 참조, 이전 근거 아카이브/WORKLOG | 1280/1920 실제 화면 가독성, Story 4개 목록의 상시 스크롤바 칸 확인 후 수동 완료 |
| UI-PAD-01 | 패드만으로 전체 UI 선택 | 구현/자동 검증됨·실기 대기(10/07 D PC Claude). InterLink 노브만으로 전체 이동(좌우 불필요)·패드 규칙 유지. [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md) | 전체 흐름·탭/첫 강조·가독성·복귀, 설정 노브 잠금/조절·콤보 실기 확인. NullRHI는 실기 Pass 아님 |
| UI-SETTINGS-01 | 설정/선택·시야/기본 조작 | 사용자 FPV HFOV·기본 시점/조작·드롭다운·명시적 선택/START·M4 Back 수리. 최신 검증 WORKLOG | 실제 두 장치·구버전.sav/종료 후 복원·전체 화면 실기. [조정](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md) |
| UI-FLOW-PROTOTYPE-01 | 로비·브리핑·조작 안내 | 번호만 표시·RC 세로 스틱·Scout/FPV 푸른 배경 사진·권장창 한글 적용. Build·UI4/4, 실제1280/1920 렌더 확인; WORKLOG | 실물 휠 방향/감도·번호 가독성·패드·영상/청감 수동 확인 |
| COMBAT-IMPACT-DEATH-01 | 차량·포탑·유탄·사망 | 차량300/포탑200·MG25/유탄150/자폭600. 포탑 자체 HP0 폭발/소리1회·점유 해제·잔해15초·실제 TUT2발 파괴/클리어 검사 | 실물 발사·가시성/청감·잔해 정착/밸런스 수동 확인 |

#### 미션·스토리·HUD

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| MISSION-MARKER-01 | 승인 박스11개 치환 | Battlefield net8/전달1·MilitaryBase 설치무인1/재밍1 저장·재로드 확인. 원본 보존 | 크기/지면·재밍 범위 수동 확인. MBase M_Target 보존, 제품 DA/실행 배치는 연결됐으나 전체 플레이 후속 |
| MISSION-NAME-01 | Story4개 표시명 | DA 한/영 반영·ID/진행 보존, 검증 WORKLOG | 로비/브리핑/HUD/결과 수동 확인. M3 내부 VeilBreaker는 호환용 |
| MISSION-CHECKPOINT-01 | 실패 시 시작/중간 지점 재출격 | 구현됨·자동 검증됨·수동 확인 대기(C PC Claude). 파괴/시간/Trigger 통합 재출격, 맵·목표·표적 유지. 실제 체크포인트 미배치·첫 출격 위치 재출격 | 맵 체크포인트 배치, M1 픽업 지점은 정보단말 회수 구현 뒤. 재출격 브리핑 재생은 MISSION-BRIEFING-02 뒤(여부 현재 미정). 튜토리얼 추락→동일 기체/조작·현재 목표 시간 재설정·목표/표적 유지·재출격 체감 수동 확인. Production Training 보존 |
| MISSION-BRIEFING-02 | HUB 대사·M1 시네마틱 | 허브 대사 박스 기본 숨김·데이터 보존. M1 MP4/Esc/종료→브리핑 연결 유지. [영상 교체](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#ugv-사진과-미션-1-영상-교체) | 청감/가독성·패드 확인. HUB 음원/튜토 대사·분기/재출격 정책 별도 |
| HUD-FIGMA-01 | 시안5 HUD Kit | WBP화·Paint 좌표/매 프레임 눈금 수정, 저녁 검증 WORKLOG | 실제 해상도·미션/나침반/타이머/상태/속도/고도/VS·UGV 표시 수동 확인. 배터리 시간 미정 |
| MISSION-COMPASS-01 | 스포이드 목표/조건 | Tutorial9·Story4에 BP_DroneMissionTargetManager 저장·검색/스포이드/조건 `+`·DA 적용. [편집](docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md#이미-배치된-맵에서-바로-찾기) | FreeGate13게이트·배달2 고유3상자 적재/완료 통과. Nav14맵 점검·NPC5맵53명 빌드/재로드 통과. LOS 복귀/착지 유지·실물 조종 별도 |
| D-6 높이 제한 | 배치 매니저·BP 값으로 적용 | 구현됨·자동 검증됨(10/05 C PC Claude). BP_DroneAltitudeLimitManager 배치·값 설정, 상세 [WORKLOG](docs/history/DRONE_WORKLOG.md) | 천장 체감 수동 확인 대기. 높이 제한 수치·경고 연출 현재 미정 |
| STORY-TEST-01 | Story 실맵·단계 교대 | M1 Drop, M3/4 Fiber→전투4종·실제 표적/진행 보존·Back 재확정. 실제 M1/M3/M4 3Success(자동 선택/출격·목표 사건) | 손 조종/사격 완주·M2 분기·M4 공중 높이/최종 위치 안전성. [범위](docs/gameplay/DRONE_TEST_MAP_GUIDE.md) |
| MISSION-RULE-PIE-01 | 실제 수업 완료 흐름 | 실제 TUT7종 자동 통과. LOS4단계만 복귀/접지 유지·DA 원본 SHA 보존, 다른 DA 귀환 안내 정리·저작 도구 재도입 방지 | 실제 손 조작·실패/재시도·Story 화면 확인. 자유 게이트 준비 중 유지 |
| STY-03-PIE-01 | 재밍 Radar·연결/HUD | 빈 Mesh·기지 범위 BP, Noise→NO SIGNAL·조종 차단·복구, 광섬유 면역 구현. 속도 저하 없음 | 일반/광섬유 진입·중심/경계·이탈·입력 복구 수동 확인. 자동 결과 WORKLOG |
| STORY-BRANCH-01 | Mission 2→3 양쪽 스토리 분기 | Story Fact 저장·성공 적용·조건 목표 필터, 미끼/실제 탑승 양쪽 자동화 완료 | 사용자가 기본 스토리안을 정하면 실제 Mission DA에 Fact 설정 |

#### 비행 물리·조작·기체

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| PAYLOAD-GRIP-01 | 집게 부착 통일 | Codex 예외 수정·자동 Pass; WORKLOG | 시작→투하→재픽업 외형 확인 |
| ACRO-MEETING-01 | Mode1 Space 하강·반전 및 키보드/패드 겹침 수정 | 구현됨·자동 검증됨·수동 확인 대기(10/04 C PC Claude). 입력원 분리·절댓값 큰 쪽·키 해제 시 패드 인계, 기존 Dead Zone·정확 적분 유지. 근거 STATUS | Mode1 스틱에 엄지를 걸친 채 Space→상승, 키 떼고 스틱→패드 조종, 모두 놓으면0을 실제 장치로 확인. Mode2도 혼합 입력 확인. W/S·A/D·Q/E·Space/Ctrl은 두 Mode 동일; 키보드 배율·Angle·마우스Yaw·회의 반전 뜻 현재 미정 |
| DR-FPV-ACRO-INPUT-02 | Acro 키보드·패드 Mode 1/2 | InterLink Acro 4축 추가·총45매핑·Dead Zone 계약 자동 검증됨(10/07 D PC Claude). [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md), 혼합 입력은 ACRO-MEETING-01 | Mode 1/2 실기 혼합 입력·비행 체감 확인. 조작 정책/회의 반전 뜻 미정 |
| DR-INTERLINK-INPUT-01 | 장치별 스로틀·인계 | Keyboard/Pad/RC 분리·실측642~3430 유지·keyheld 우선/해제pad복귀·flush guard, 최종34에 회귀 포함 | 실물 전축/Cancel·재연결·손조작·다른 장치 교정은 별도. [입력](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md) |
| DR-FPV-ACRO-PIE-01 | FPV Rate/Acro 실제 조작 체감 | Mode 1/2 축 분리와 각속도·무수평복귀에 공통 질량·추력·모터 응답·중력·Body Up 추진·선형/제곱 항력 v2 연결. 별도 속도 단계는 제거 | 키보드/패드로 Nose-down 전진력, 호버·상승·무추력 하강, Roll/Loop와 650°/s 체감, Mode 1/2가 축 배치 외 비행 성능이 같은지 확인 후 수치 조정 |
| DR-FLIGHT-PHYS-02 | 모터OFF 항력·기존 정합 | OFF 공유항력/Worldg·추력0·입력 정합 보존. 이전 검증은WORKLOG | ON assisted·controlledRacer/실기체교정·live질량/payload·본미션/B·C 한계, 실물/실청·패키징 별도. [정본](docs/gameplay/DRONE_REALISTIC_HANDLING_PLAN.md) |
| PHY-CAMERA-01 | 벽·그물 접촉 화면 안정화 | 구현됨·자동 검증됨·수동 확인 대기. 연속 접촉 제약·외형/FPV 카메라 분리·그물 Camera Ignore, 피해 Shake 유지. 검증 WORKLOG | Physics Sandbox에서 1/3인칭 저속/고속/지속 벽 접촉·그물 감속/포획 때 화면 떨림 감소와 충돌 유지 확인. NPC 맵에서 총알 피격 화면 흔들림이 남는지 확인. 자동화만으로 체감 Pass 처리하지 않음 |
| PHYSICS-SANDBOX-01 | 벽 충돌·그물 얽힘·국소 파괴 벽 | 벽 반발·날개 접촉·그물 감속/포획/하강·탄환/폭발 국소 절단 구현/자동 검증. 실제 Chaos 비교 별도·이전 근거 WORKLOG | Sandbox에서 저속 접촉은 작게 밀리고 고속 충돌은 크게 반발하는지, 날개 끝 접촉 방향의 자세 Kick, 그물 포획·하강·자동 해제와 조종 복구를 화면 확인하고 실제 Chaos Cloth/Dataflow와 Geometry Collection을 별도 구역에서 비교 |
| PHY-NET-03 | 늘어지는 그물 장애물 | 공유 매듭 PBD·상단 고정/중력·제약/접촉·BP 예산 구현. Chaos Cloth는 별도 후속 | 포획·국소 변형/감쇠·Reset·크기/FPS 수동 확인. 일반 접촉 자동 절단 금지 |
| PHY-COL-01 | 외곽 충돌·전방 자폭 센서 | 전체 본체/로터 물리 충돌 유지·하부 Z 범위 보정·FPV/Fiber 돌출 센서 직접 접촉 자폭. 최신 검증 WORKLOG | 고저속/얇은 벽/연속 압박·실제 조준/폭발·손 조종. [정본](docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md) |
| DRONE-FIBER-01 | 광섬유 Drone 기반 | DroneSpy·GSU 통·Rotor·재질·다점 케이블·재밍 면역/ImpactDetonation·1인칭 기반 구현/자동 검증. 상세 아카이브/WORKLOG | TestMap에서 Spy 본체·통 크기/위치, 본체/카메라 비간섭, Rotor 회전, 통 상단 케이블 출발과 곡률, 조작·자폭·재밍 면역을 화면 확인하고 BP Transform/굵기·간격을 최종 조정 |
| DRONE-GROUND-01 | UGV 무장 | 연사/탄수/재장전·전용 IMC·포탑 조준 구현, 규칙 STATUS | 패드/마우스 연사·빈 탄창/수동 재장전·유탄6발·Space/Ctrl·탄도 실기 |

#### AI·NPC

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| AI-PATRIOT-PIVOT-01 | 패트리어트 접합부 회전 BP | 초기 생성/재로드 각7회 통과 뒤 10/13 12:50 BP 재저장 확인. 현재 저장본 재검증 대기; [가이드](docs/ai/DRONE_MG_TURRET_3PART_GUIDE.md#6-패트리어트-미사일-포대-접합부-회전축-조정) | 현재 축/이음새·크기·복합 회전 확인. 기존 편집 보존·생성 도구 덮어쓰기 금지. AI/발사·차량 부착 미포함 |
| AI-PERCEPTION-TEST-01 | 실제 시야와 수동 조종 비교 | 선행 자동 교전/리시 포기를 PIE 검사에서 격리해 점유·사망/재점유·수색/복귀 통과, Drone.AI 기본 회귀 복귀. MG 회전부 Static 경고도 해소; WORKLOG | 실제 SmartObject 맵에서 사용자 드론 조종·시야/엄폐/장기 순찰 확인. 맵·제품 리시 규칙 보존 |
| AI-LOCOMOTION-01 | 적·아군 NPC 걷기 모션 | 다리 고정 후속 구현됨·자동 검증됨·수동 확인 대기(10/05 C PC Claude). 아군 Pin Bone·적 발 IK 제거, 양손 총 파지/hand_r 부착 유지. 상세 [WORKLOG](docs/history/DRONE_WORKLOG.md) | Lvl_NPCSmartObjectGreybox 걷기 다리·속도 대비 보폭/발 미끄러짐·손/총 정렬·사격/재장전 확인. 적 경사면 발 맞춤 없음, 최종 애니메이션/산탄총 전용 동작 미정 |
| AI-SO-TUNE-01 | Smart Object·유인 MG·개인화기 추적 확인 | 순찰 최종 슬롯 방향·Pursue 정지점·Capsule 외 VisualOnly 계약을 적용했고 사용자 화면에서 정상 이동을 확인했다. 진단 로그 기본값 Off | 새 `1.0초` 첫 사격 조준 대기를 실제 화면에서 확인. 재발 시 Blueprint에서 `[NPC-STATE]`·`[NPC-MOVE]` 진단을 켜 로그 회수 |
| AI-OUTDOOR-TUNE-01 | 야외 감지·Smart Object 검색 범위 | Outdoor Controller BP를 Rifle/Shotgun에 연결. Sight 60m/Lose 70m/Search 80m×±10m/직전 회피 15m, BP 조절 가능 | 넓은 야외 맵 화면에서 과도한 원거리 점유·감지 끊김 여부를 확인하고 역할별 수치 확정 |
| AI-SHOTGUN-PIE-01 | 추가 Shotgun NPC 사격 체감 확인 | 실제 8 Projectile·12° 반각, Pellet당 3 피해, 상호 충돌 방지, Cyan Debug 기본 Off, 발광 비드/Tracer·3°/6° 시선 Hysteresis·Asset/PIE 자동화 완료 | 발광 비드 8개 분리 가시성·Cyan 선 제거·회피·최대 24 피해·사거리·LOS·시선 안정화를 Editor 화면에서 확인 |

#### 환경·날씨·자산

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| ASSET-OILRIG-PREVIEW-01 | OilRig 실제 Preview 환경 이식 | Preview 이식·외부/누락0/0·Map Check0/0·원격 반영의 이전 근거 아카이브/WORKLOG. 기존 Overview·사람 환경 보존 | Editor에서 문/문틀 위치, 재질·조명·충돌·오션·비·첫 로드와 FPS를 수동 확인 |
| MANAGERS-FOLDER-01 | 사용자 요청: 매니저 폴더 정리 | 구현됨·자동 검증됨(10/05 C PC Claude). MissionManager·RandomWeatherController·WeatherDebugVisualizer를 `/Game/Drone/Managers`로 이동·Redirector 정리. 상세 WORKLOG | 날씨 시험 맵 정상 동작 수동 확인 대기. GameMode·PlayerController·RainVisual 기존 위치 유지 |
| WTH-03 | 실제 도시 비 화면 추종 | 사본LocalSpace·원본생성축 보정/위치 분리. 실제도시3뷰 화면분포·Off0/3품질 캡처 포함RHI21개 통과 | 회전/이동·실내/실외·Off 실기, FPS 별도. 원본/품질예산 보존, [비 가이드](docs/gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md) |

#### 테스트·빌드·성능·동기화

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| TEST-RENDER-UNPAINTED-01 | PIE 미렌더 판정 구분 | D-11 구현됨·자동 검증됨(10/05 C PC Claude). 상시 실패4개 KnownIssues 분리. 최신 전체101개 결과 STATUS 참조. 미렌더는 포커스6개 모두 화면 루트 포커스로 실패하는지로 판단 | 화면 그려진 포커스/실제 패드 수동 확인·KnownIssues 별도 실행. 같은 증상2회 상한·Production 보존 |
| TEST-ORDER-ROUTE-01 | 전체 렌더 회귀 Route 키 순서 의존 관찰 | 2026-10-04 C PC ClaudeAcroFull 전체5회(test.log/test2.log/final.log/final2.log/test3.log) TrainingRouteSelectionPIE 모두 Success(Codex 로그 대조). 그중3회 화면 미렌더이므로 화면 검증과 구분. 지난 Fail은 날짜별 기록 보존, 원인 미특정·해결 확정 아님 | 재발 시 선행 테스트/입력 처리 순서 재현·Claude 조사. Production 맵 보존 |
| BUILD-PACKAGE-01 | 패키징 쿠킹 설정 | 정적 자동 검증됨(10/02 C PC Claude). Mission/Drone DA AlwaysCook·MissionMap Soft 참조. 실제 패키징 미실행; 검증 WORKLOG | 실제 패키징 미실행. 패키지에서 DA 자동 등록·모든 MissionMap 진입 확인, Production Training 보존 |
| PERF-ZEN-START-01 | D PC Editor 시작 지연(Zen 대기) 조사 | 원인 특정(10/06 D PC Claude): Zen 세션 기록 733개 로드 약 20초 + 엔진 20초 초과 모달. 10/02 473초는 모달 미응답 대기. 세션 폴더 732개 백업 이동 완료, 재측정 대기. 상세 STATUS/WORKLOG | Claude가 같은 맵·캐시로 cold/warm 시작 로그 비교, 확인창 응답·Zen running→Editor 확인 시간 분리. 캐시 삭제·엔진 소스 수정·보안 해제 금지, Production Training 보존 |
| SYNC-WORKPC-01 | D PC 10/27 | FINAL4 Source/Config67·보호9·최신Saved10 hash 일치/Editor0 | 다른 PC 수신·실기·패키징 별도. [등록부](docs/git/DRONE_WORK_PC_SESSIONS.md) |
| RACING-MAPS-01 | 팀원 레이싱 맵 1·2·3 | Map2 중복 링 때문에 생기던 기록 취소 수정·93개 실행 Gate 완주/저장. 3맵 새 프로세스 복원 통과. 선택/사진/API 포커스 정합·옛 7개 안내 수정; STATUS | 사용자 실제 비행/카드별 사진 확인. 자동 기록은 전용 슬롯, 원본 맵/사진과 기존 DA 변경 보존 |
| SYNC-COLLAB-01 | 협업·다른 PC 세팅 | 최신 소유권·단일 엔진·10/23 승인 이력은 [등록부](docs/git/DRONE_WORK_PC_SESSIONS.md) | 다른 PC 수신/Build 별도. 사용자 Lobby·Claude 문서 보존, 이번 Commit/Push 없음 |
| SYNC-SPACES-01 | MD·Space 최신화 | 기존3Page/5블록 교체·재읽기 일치, seq121/76/84 | 새Page0·역사/비대상 보존. 이번 Commit/Push 없음 |

## Next

현재 상태는 [STATUS](STATUS.md), 수치·원시 로그 이력은 [WORKLOG](docs/history/DRONE_WORKLOG.md), 이전 Next는 [원문 아카이브](docs/history/archive/WORKBOARD_2026-10.md)를 따른다.

0. 실제Race/M4 오디오 조립 자동 검증·사망음 pause 수리 결과를 유지하고 실물 손조종/전체완주·스피커 청감/밸런스·Cook/패키징을 확인한다. M4 유인MG는 미배치라 기존 개별검사와 구분한다.
1. PS 앞밀기 HID750표본·SceneViewport20경로·3장치 키 설정의 공식28검사 근거를 유지하고 실제 장치 양방향/중립/해제·비행체감·종료/재실행 복원을 확인한다. InterLink 추가 카메라 조작 배정은 기존 비행4축과 구분한다. 키·축·반전 pending/부모적용/취소/기본값과 원본45매핑 보존 절차는 입력 정본을 따른다.
2. LOS 캡처를 검사 World/LocalPlayer에 연결하고 HitResult 디코더를 수리한 뒤 사람·드론 가시성과 지면 관계를 확인한다. 후퇴 시작값400cm·기존 동선/실제 착지 보존, 눈높이 원인 단정/임의 높이 변경 없음.
3. M3 Fence null guard/기하 보존을 유지하고 실제 배치·접촉을 확인한다. M4 Lumen 경고·긴 로딩은 별도 성능 과제다. 기존 무입력 CPU 표본으로 원인/최적화 효과를 확정하지 않고 같은 조건의 비행/사격과 GPU 지원 여부를 계측한다.
4. 최신 전체Build 후 새DLL Editor를 사용한다. 전방 센서 직접 접촉/본체·로터 접촉 구분과3초 파괴 화면·생존 단계 즉시 교대를 실제 조종으로 확인한다. 실기체 교정/payload/B·C·패키징은 후속이다.
5. M1 배달·M3/4 재머→교대→후속 목표를 손 조종/사격으로 확인하고 M2 분기·M4 공중 높이/출격 위치 안전성을 점검한다. Camp 일반20GiB·승인 저메모리16GiB 시작/runtime4GiB 보호와 Production Training 보존을 유지한다.
