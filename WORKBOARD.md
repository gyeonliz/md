# Drone 작업 보드

마지막 갱신: 2026-10-14 D PC — Drone bb6233c8·MD b38fc84 + Gate/Rain/City/UI·문서 미커밋. 오늘 승인으로 Codex 직접 구현·검증, 상시 역할은 유지. Commit/Push는 사용자.

## Now

최신 Git·검증 요약은 [STATUS](STATUS.md)를 따른다. 현재 카드·수동 확인 안내·Next만 유지한다.

### 결정 필요 — 현재 DA 값은 채택 사양이 아님

| 항목 | 필요한 결정/자료 | 현재 처리 |
|---|---|---|
| M2 | 실제 타겟 탑승 vs 미끼 결말·시스템 성공/실패·다음 Story Fact | D-1 보류(2026-10-05 사용자): 기획자 내용 대기. 양쪽 분기 기반 유지, M3 반대 분기 첫 대사 비어 있음 |
| M3/M4 | 타겟·적·드론 수량, 성공/실패, 제한·재출격·결과 카메라 | D-2 보류(2026-10-05 사용자): 기획자 내용 대기. M4 시험값 표적3·재출격0(무제한)는 채택 사양 아님 |
| 조종 입력 표시 | 기본값, 장치 자동 전환, 혼합 입력·연결 해제/재연결 | D-3 결정(2026-10-05 사용자): 기본 끔(False), 설정에서 ON/OFF. 기존 구현과 일치·수동 확인 대기. 장치 자동 전환·혼합 입력·연결 해제/재연결 정책 현재 미정 |
| 레이싱 | 지형/4코스 진행도 대조, Ghost/리플레이·커브·Restart/Quit 범위 | D-5 기존 구현. 팀원 “미션3까지 완료” 커밋·맵 변경 수신, 실제 연결/완주 미검증; RACING-TERRAIN-LINK-01 |
| Tutorial | 수업8개 유지, 권장문구/건너뛰기 정책 | D-4 수업1~8 유지·회의 “4”는 고정 레이싱 코스4개. 진행도 JSON 저장은 수신 코드에 구현됨; 재실행 확인은 TUT-COMPLETION-SAVE-01 |
| Bangkok 의존 자산 | 방콕·다른 구매/팀원 자산 정리 범위 | D-13 종료(10/05 사용자 결정): 방콕만 삭제, 자연환경 팩·지형 머티리얼·병사 팩·HDRI·RawDrones·NavigationArrows 유지. 삭제 커밋·푸시 상태는 별도 확인 |
| 콘텐츠/전시 | 캐릭터 메시·관찰 시점 적용 맵·조종기 비치/책임, 기록 등급, 브리핑 실명/납품일, 행사일 | 임의 실명·수치·마감일 없음 |



### 면접·공유 결정 대기

10/06 비교표 원문은 [10월 아카이브](docs/history/archive/WORKBOARD_2026-10.md)에 보존했다. 기능별 수동 대기 카드는 아래에 유지한다.

| 항목 | 남은 확인/결정 |
|---|---|
| D-7 구매 자산 공유 | 비공개 전환은 사용자 방향. 실제 공개/팀원 접근 설정은 이번 미조회. 향후 공개물은 구매 에셋을 제외한 코드·빌드·영상/출처 목록 |
| D-8 본인 기여·AI 활용/README | md에만 작성하는 결정 유지. 본인 설계·결정·검증 범위 확인 뒤 정직하게 작성, 이번 신규 작성 없음 |
| BP/Legacy API | 삭제 후 남은 디자이너용 접근자/Legacy 정리 범위 결정 대기. 수신 코드 존재만으로 삭제 승인하지 않음 |

스냅숏 백로그 GIT-LFS-CAP-01·AI-TOOL-REVIEW-01은 현재 카드 없음(09-15 스냅숏), 복원/보류/폐기 결정 대기.

완료·종료 카드·현재 카드의 이전 장문 근거·지난 Next·수동 맵 안내는 [10월 보드 아카이브](docs/history/archive/WORKBOARD_2026-10.md)에 원문 보존했다. 10/06 D PC: RACING-MEETING-01·FIGMA-RACING-02·MISSION-FRAMEWORK-01·MAP-TEST-01(대체)·TUTORIAL-GUIDE-03(완료)도 이동. 현재 수동 순서는 [테스트 가이드](docs/gameplay/DRONE_TEST_MAP_GUIDE.md)를 따른다.


### 카드 그룹

회의 후 카드는 각 그룹 맨 앞에 둔다.

#### 튜토리얼·코스·레이싱

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| TUT-OBSERVER-01 | 고정 조종자 첫 수업 | 구현·새 Observer 맵/DA 저장. Hover ID·8수업 유지; 검증 WORKLOG | 이륙→전진→방향 유지 후진→실제 착지, 고정 카메라·재출격/다음 수업 복원 수동 확인 |
| TUT-GATE-SAVE-01 | Gate BP 저장 사고 | CDO MID 참조 원인 수정·Gate BP 수리, 재로드3회·Gate5/5 성공(기존 경고100) | 팀원 Source+BP 수신/종료 후 Build·같은 저장 실기. 기하/색·16개 유지, Production 미수정 |
| TUT-COURSE-SMOOTH-01 | 장거리 코스 표시선 곡률 분할·BP 표시 예산 | 구현됨·자동 검증됨·수동 확인 대기(10/04 C PC Claude). 긴 코스 곡률 분할·기본1024(시작값·미확정), BP 드래그 재구성 Off. 수치·근거 STATUS/WORKLOG | 팀원 Production 코스 외형·급커브/끝 연결·Editor 편집 체감 수동 확인. BP2048(측정 최대20cm) 검토 가능. 짧은 TestMap68/113조각 기존 균일 분할 유지·Production 저장/재생성 금지 |
| RACING-TERRAIN-LINK-01 | 레이싱 흐름·지형 연결 | D-5 기존 구현. a57a4444에 팀원 미션3 완료 보고·Training/Island/MountainRange/Demonstration 변경 수신. Editor 로그는 Racing 진입/카운트다운까지만 확인 | 실제 진입 맵·시작점·완주/기록·4코스 진행도 대조. 팀원 보고를 수동 Pass로 확대하지 않음·Production 보존 |
| TUT-PROGRESS-01 | 튜토리얼 시간·연속 진행·전체 완료 | 이전 자동 검증 WORKLOG. 수신 코드의 완료 미션/Story Fact JSON 저장은 TUT-COMPLETION-SAVE-01 | 실제8수업·현재 결과창·로비 완료 표시/재진입 확인. Production Training 보존 |
| TUT-BRIEFING-TEXT-01 | 튜토리얼 조작키 브리핑 문구 결정·입력 | 미구현·문구 현재 미정. Codex research 2026-10-02: 8수업 키보드 키, 자폭/드랍/UGV NPC/포탑 패드 키·대사, 튜토리얼 화자 Figma 미기재. 호버/전진/회전/게이트 패드 브리핑 원문 있음. 이번 조작키 브리핑 미입력 | 사람이 미기재 문구·화자를 결정한 뒤 Claude가 DA/UI 연결·검증, Story 허브를 튜토리얼 화자로 추정하지 않음 |
| TUT-COMPLETION-SAVE-01 | 미션 진행도 영구 저장 | 10/13 수신 소스 확인: 완료 미션·Story Fact·권장문구 표시 여부 JSON 저장/복원 구현. Best Lap 저장과 별개 | Claude가 현재HEAD 회귀 확인 후 실제 성공→종료→재실행 복원·저장 실패 처리 확인. 수신만으로 자동/수동 Pass 아님 |
| TUT-ORBIT-02 | 회전 수업 = 원형 코스 한 바퀴 | Heading DA ID 호환 유지, Closed Spline·9 Gate, Tag별 Recorder·HUD, 다른 코스 비활성. 독립 Heading 수업 맵으로 연결 | 실제 비행 제자리 Yaw/다른 코스/7⁄8 바퀴 미완료, 결승→귀환→성공 확인 |
| TUT-GATE-PRESENTATION-01 | Gate 크기·진행 방향 | Island112개 정합·숨김Native 보존/원본 무저장. 비균등Scale·0접선 수리, m_green Naniteflag 수리; STATUS | 새Source Build 후 Island 크기/방향·3상태색 실기. 잔존 삭제·맵 재생성 금지, Main 참조 별도 |
| TUT-ROUTE-SELECT-01 | Training Route 4개 선택 시험 | `Lvl_DroneTrainingRouteSelectionTest`에 직선·좌곡선·우곡선·상승 슬라럼과 Gate 각 5개 배치. `1~4` 고정·`5` 무작위, 단일 활성, 진행 초기화, HUD 기록 Source 전환. Build·Map Check·API/저장/실제 키 PIE 성공 | 사용자가 화면에서 경로 형태·Gate 간격·랜덤 전환과 Lap HUD를 확인하고 각 Spline 점을 최종 조정 |
| TUTORIAL-MISSION-01 | Figma Tutorial 8개 독립 Mission | 수업별 `TestMap/Tutorial` 8맵·DA·직접 Play Entry 구현, 공용 종합 시험장 보존. 다른 PC의 Hover 로비/직접 PIE에서 3초 유지→귀환 Success. 비충돌 표식 4개 유지 | FrontEnd와 각 독립 맵에서 Hover 가독성 및 8수업 전체 위치·목표·결과를 수동 확인. 이전 사용자 7개 대략 확인과 최종 완주를 구분 |
| TUT-BEST-01 | Course별 Best Lap 영구 저장 | 구현됨·자동 검증됨·수동 확인 대기(10/02 C PC Claude). 코스/기체/조작별 Best Lap JSON·HUD, 자동화 별도 슬롯. 평균은 실행 History | 같은 조건 실제 완주2회·재실행 복원·첫 완주 전 HUD 확인. D-5 결과 시간은 RACING-TERRAIN-LINK-01 참조 |
| PROCEDURAL-RACING-01 | 시드 도시·외형 | 완성BP1체·닫힌모듈/슬롯재질·차선·소유 팔레트. 시드194849 화면/실제RHI21개 통과; STATUS | 지정/무작위·같은 시드·완주/기록 실기. 공급팩·Production 보존 |
| TUTORIAL-FIGMA-02 | Figma 8개 훈련 ↔ Test Map 대조 | 8개 기능/DA·독립 시험맵·시간·연속 진행·전체 완료 UI 구현과 기존 자동 검증 보고가 있음. 2026-10-03 DA 순서 재확인; Warehouse 최종 환경은 별도 | 기존 진행 UI의 실제 8수업 연속 완주·결과/로비 복귀를 수동 확인. D-4 수업1~8 유지·회의4는 레이싱 코스4개. Warehouse 범위 결정, 결과 UI 중복 구현 금지 |

#### UI·설정·패드

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| UI-SELECT-ART-01 | 전체 Pretendard·선택명 | Native/Designer 10종 공통 적용·기존 크기/굵기 보존, 목록 끝 괄호만 숨김. 추가 렌더14/14·Story/설정 캡처 확인 | 실제 패드·1280/1920 가독성. DA/ID·아트 보존, 아이콘/명시 Opt-out 제외 |
| UI-CONTROL-LAYOUT-01 | 조작 이름·가로폭 | Codex 예외 수정·자동 Pass; WORKLOG | 1280/1920·패드 수동 확인 |
| UI-RESULT-LAYOUT-01 | 결과창 | 현재 native TitleKit 좌측 버튼/우측 정보 카드, 소스 확인; 옛680 검증은 WORKLOG | 현재 화면·패드·다음/재도전/복귀 확인 |
| UI-LOADING-PAUSE-01 | 로딩·일시정지 | Story/Procedural 로딩·취소, 미션 일시정지/재시작/타이틀 복귀 연결을 소스로 확인 | 현재HEAD Build/회귀→Esc/Start·재개·같은 시드/취소 실기 확인. Pause 포커스 관찰은 UI-FOCUS-RACE-01 |
| UI-FOCUS-RACE-01 | UIOnly 첫 포커스 경쟁 | 이전5프레임 복원·관찰은 WORKLOG. 수신 목록에 PauseMenuRacingPIE Resume 포커스 전체Fail/단독Pass 혼재 추가; STATUS | 현재 결과/일시정지/타이틀 첫 강조·패드 이동 수동 확인. 실제PC/로그 대조 전 안정화 완료 아님 |
| UI-MEETING-LOBBY-01 | Claude 5메뉴/포커스 계약·Codex BP 연결 | 구현됨·자동 검증됨·수동 확인 대기(2026-10-03 밤 C PC). Story/Racing/Tutorial 진입 전 분류·중간 화면 없음, TitleMenuClass 저장 연결. TitleFiveMenuPIE/WidgetPIE·패드 흐름 Success, 이전 남은 C++ 연결 닫음 | 실제 패드 상하 순환·5개 진입/설정3·진입 메뉴 복귀·B/Esc 반복, 1280/1920 위젯 크기 확인. 종료 자동화는 Dispatcher 연결만 검사. 로비 탭/LB·RB 유지 여부 현재 미정 |
| UI-CONTROL-DISPLAY-01 | Claude 설정/축/HUD·Codex 입력 표시 BP 연결 | 구현됨·자동 검증됨·수동 확인 대기(2026-10-03 밤 C PC). 조종 입력 표시 수동 ON/OFF·적용/취소/기본값·SaveGame, ControlInputDisplayClass 저장 연결·ControlInputDisplayPIE Success. D-3 기본값 결정은 아래 결정 표 참조(기존 False와 일치) | 실제 패드·1280/1920 위치·저장/재실행·기본값 복원 확인, 고도계 독립. 장치 자동 전환·혼합 입력·분리/재연결 정책 결정 필요. 자동화 슬롯은 DroneAudioSettings_Automation |
| UI-LAYOUT-DIAG-01 | 로비 레이아웃 진단 판정 변동 조사 | 진단 판정 변동·기존 Fail 유지. D-11로 KnownIssues.Flow.LobbyLayoutStabilityPIE 분리됨(10/05 C PC Claude), 안정화 완료 아님 | Claude가 표본/대기·레이아웃 원인을 구분하고 반복 렌더 검사 판정 안정화, 1280/1920 수동 확인 별도 |
| UI-LAYOUT-01 | 목록 진입·선택 시 한 프레임 재배치 | 구현됨·자동 검증됨·수동 확인 대기. 줄바꿈·상시 스크롤바·폭270 후속 포함. 최신 진단 분리는 UI-LAYOUT-DIAG-01 참조, 이전 근거 아카이브/WORKLOG | 1280/1920 실제 화면 가독성, Story 4개 목록의 상시 스크롤바 칸 확인 후 수동 완료 |
| UI-PAD-01 | 패드만으로 전체 UI 선택 | 구현/자동 검증됨·실기 대기(10/07 D PC Claude). InterLink 노브만으로 전체 이동(좌우 불필요)·패드 규칙 유지. [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md) | 전체 흐름·탭/첫 강조·가독성·복귀, 설정 노브 잠금/조절·콤보 실기 확인. NullRHI는 실기 Pass 아님 |
| UI-SETTINGS-01 | 사운드·화면·성능 설정 | Master 음량 미리보기/SaveGame, 창·전체화면/해상도, 품질·VSync·FPS, 적용/기본값/뒤로 취소 구현. PIE 창·해상도 차단. 설정 계약과 FrontEnd PIE 성공 | Standalone에서 실제 소리/창·해상도, Apply와 Back 취소·재실행 복원 확인. 음악/SFX/음성 분리 라우팅은 후속 |
| UI-FLOW-PROTOTYPE-01 | Mission/Drone 선택 임시 UI 확인 | 후속 첨부 시안으로 로비 3열·브리핑 이미지/설명·기체 상단 도식/상세·하단 가로 카드 갱신, `FrontEndPIE`와 계약 성공 | 16:9 1280/1920 가독성/스크롤·선택/출격 확인 뒤 최종 WBP·Thumbnail/3D Preview 범위 결정 |

#### 미션·스토리·HUD

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| MISSION-MARKER-01 | 승인 박스11개 치환 | Battlefield net8/전달1·MilitaryBase 설치무인1/재밍1 저장·재로드 확인. 원본 보존·수동 대기 | 크기/지면·재밍 범위 확인. MBase M_Target 보류. 제품 Story DA 맵/목표 연결은 별도 |
| MISSION-NAME-01 | Story4개 표시명 | DA 한/영 반영·ID/진행 보존, 검증 WORKLOG | 로비/브리핑/HUD/결과 수동 확인. M3 내부 VeilBreaker는 호환용 |
| MISSION-CHECKPOINT-01 | 실패 시 시작/중간 지점 재출격 | 구현됨·자동 검증됨·수동 확인 대기(C PC Claude). 파괴/시간/Trigger 통합 재출격, 맵·목표·표적 유지. 실제 체크포인트 미배치·첫 출격 위치 재출격 | 맵 체크포인트 배치, M1 픽업 지점은 정보단말 회수 구현 뒤. 재출격 브리핑 재생은 MISSION-BRIEFING-02 뒤(여부 현재 미정). 튜토리얼 추락→동일 기체/조작·현재 목표 시간 재설정·목표/표적 유지·재출격 체감 수동 확인. Production Training 보존 |
| MISSION-BRIEFING-02 | HUB 보이스·자막 브리핑·진입 1회 시네마틱 | 자막·Voice 슬롯·자동 진행/Y·Tab/정지 구현·BriefingLinesPIE Success(2026-10-02 C PC Claude, ClaudeBriefing/test2.log). Story M1 4·M2 4·M3 5(조건 없으면 4)·M4 6줄 원문 입력, 화자 허브. M3 첫 줄 Story.TargetEliminated 조건 | 자막 가독성·속도 수동 확인. 음원 없음·튜토리얼 대사 미입력·1회 시네마틱 완료 근거 없음. 반대 분기 M3 첫 대사와 M2→M3 분기·재출격 재생 여부 현재 미정 |
| HUD-FIGMA-01 | HUD 배터리·기체명·신호 대역·풍향 | D-6 구현됨·자동 검증됨(10/05 C PC Claude). HUD 방위 통일·불어오는 쪽 풍향, 미션별 배터리 제한/방전 추락 추가. 상세 STATUS/WORKLOG | 풍향 HUD·배터리/HUD 가독성 수동 확인. 배터리 시간 모두0·현재 미정·값 확정 뒤 추락 체감 확인. 높이 제한은 아래 D-6 행 참조·신호 대역 미정 |
| D-6 높이 제한 | 배치 매니저·BP 값으로 적용 | 구현됨·자동 검증됨(10/05 C PC Claude). BP_DroneAltitudeLimitManager 배치·값 설정, 상세 [WORKLOG](docs/history/DRONE_WORKLOG.md) | 천장 체감 수동 확인 대기. 높이 제한 수치·경고 연출 현재 미정 |
| STORY-TEST-01 | Story Mission별 격리 TestMap 4개 | GoldenTime Drop/Return, Intercept Spline 차량·목적지 실패, VeilBreaker 재밍 이탈/Return, Endgame UGV 표적 3개/Return과 DA 4개 존재. 4맵 직접 Play Entry 및 FrontEnd Catalog 총 14개 연결. Oct 1 다른 PC의 14맵 점검에 포함 | 각 맵 FrontEnd/직접 Play에서 목표·실패·귀환 수동 확인. 미구현 후보를 이 카드에 합침(Claude 지시서·Figma 매트릭스 Mission 1~4): M1 정보단말 회수·요원 NPC, M2 잔해 Scan·반전, M3 한 미션 내 기체 교대·MANPADS/베일 카운트, M4 장거리 타격·엔딩 시네마틱. 스토리 충돌·MANPADS/베일 표기는 현재 미정, Production Training 보존 |
| MISSION-RULE-PIE-01 | 새 목표 Rule의 실제 맵 Vertical Slice | 귀환·Jammer·역할 Actor 시험 배치 완료, 직접 실행은 Prototype Flow | Test Mission DA/진입 경로에서 Scan/Delivery/Destroy/Return/Jamming Event·Tag·시간 규칙 확인 |
| STY-03-PIE-01 | 재밍 Radar·연결/HUD | 빈 Mesh·기지 범위 BP, Noise→NO SIGNAL·조종 차단·복구, 광섬유 면역 구현. 속도 저하 없음 | 일반/광섬유 진입·중심/경계·이탈·입력 복구 수동 확인. 자동 결과 WORKLOG |
| STORY-BRANCH-01 | Mission 2→3 양쪽 스토리 분기 | Story Fact 저장·성공 적용·조건 목표 필터, 미끼/실제 탑승 양쪽 자동화 완료 | 사용자가 기본 스토리안을 정하면 실제 Mission DA에 Fact 설정 |

#### 비행 물리·조작·기체

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| PAYLOAD-GRIP-01 | 집게 부착 통일 | Codex 예외 수정·자동 Pass; WORKLOG | 시작→투하→재픽업 외형 확인 |
| ACRO-MEETING-01 | Mode1 Space 하강·반전 및 키보드/패드 겹침 수정 | 구현됨·자동 검증됨·수동 확인 대기(10/04 C PC Claude). 입력원 분리·절댓값 큰 쪽·키 해제 시 패드 인계, 기존 Dead Zone·정확 적분 유지. 근거 STATUS | Mode1 스틱에 엄지를 걸친 채 Space→상승, 키 떼고 스틱→패드 조종, 모두 놓으면0을 실제 장치로 확인. Mode2도 혼합 입력 확인. W/S·A/D·Q/E·Space/Ctrl은 두 Mode 동일; 키보드 배율·Angle·마우스Yaw·회의 반전 뜻 현재 미정 |
| DR-FPV-ACRO-INPUT-02 | Acro 키보드·패드 Mode 1/2 | InterLink Acro 4축 추가·총45매핑·Dead Zone 계약 자동 검증됨(10/07 D PC Claude). [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md), 혼합 입력은 ACRO-MEETING-01 | Mode 1/2 실기 혼합 입력·비행 체감 확인. 조작 정책/회의 반전 뜻 미정 |
| DR-INTERLINK-INPUT-01 | InterLink DX 입력·메뉴 | 10/07 이전 자동 검증·집계 정정은 STATUS. 45매핑·ArmSwitch·노브; [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md) | 현재 수신 코드 빌드 후 축/DZ·Mode2·Button1·12/13·노브 이동/탭·방향·설정 실기 확인 |
| DR-FPV-ACRO-PIE-01 | FPV Rate/Acro 실제 조작 체감 | Mode 1/2 축 분리와 각속도·무수평복귀에 공통 질량·추력·모터 응답·중력·Body Up 추진·선형/제곱 항력 v2 연결. 별도 속도 단계는 제거 | 키보드/패드로 Nose-down 전진력, 호버·상승·무추력 하강, Roll/Loop와 650°/s 체감, Mode 1/2가 축 배치 외 비행 성능이 같은지 확인 후 수치 조정 |
| DR-FLIGHT-PHYS-02 | 단일 고속 기준·질량/추력·Payload 하중 | 단일 무적재 고속 기준·질량/추력/모터/항력·Drop kg 하중 구현/자동 검증. Mode1/2 공통·투하 즉시 복구·이전 근거 WORKLOG | FPV/Drop 수동 비행으로 무적재 속도, 모터 추력 지연, 적재 전후 호버·가속·선회 차이와 Mode 1/2 축만 달라지는지 확인. 실제 기체 스펙이 정해지면 Definition별 질량·추력·항력 교정 |
| PHY-CAMERA-01 | 벽·그물 접촉 화면 안정화 | 구현됨·자동 검증됨·수동 확인 대기. 연속 접촉 제약·외형/FPV 카메라 분리·그물 Camera Ignore, 피해 Shake 유지. 검증 WORKLOG | Physics Sandbox에서 1/3인칭 저속/고속/지속 벽 접촉·그물 감속/포획 때 화면 떨림 감소와 충돌 유지 확인. NPC 맵에서 총알 피격 화면 흔들림이 남는지 확인. 자동화만으로 체감 Pass 처리하지 않음 |
| PHYSICS-SANDBOX-01 | 벽 충돌·그물 얽힘·국소 파괴 벽 | 벽 반발·날개 접촉·그물 감속/포획/하강·탄환/폭발 국소 절단 구현/자동 검증. 실제 Chaos 비교 별도·이전 근거 WORKLOG | Sandbox에서 저속 접촉은 작게 밀리고 고속 충돌은 크게 반발하는지, 날개 끝 접촉 방향의 자세 Kick, 그물 포획·하강·자동 해제와 조종 복구를 화면 확인하고 실제 Chaos Cloth/Dataflow와 Geometry Collection을 별도 구역에서 비교 |
| PHY-NET-03 | 늘어지는 그물 장애물 | 공유 매듭 PBD·상단 고정/중력·제약/접촉·BP 예산 구현. Chaos Cloth는 별도 후속 | 포획·국소 변형/감쇠·Reset·크기/FPS 수동 확인. 일반 접촉 자동 절단 금지 |
| PHY-COL-01 | 드론 외곽 환경 반발 | 몸체/로터 크기 자동 범위·시간/방사 Sweep·Pawn 충돌 채널 보강, 검증 WORKLOG | 벽/기둥 전후좌우·고저속/얇은 벽·연속 압박 수동 확인. 안정 카메라·피격Shake·착륙/UGV 보존 |
| DRONE-FIBER-01 | 광섬유 Drone 기반 | DroneSpy·GSU 통·Rotor·재질·다점 케이블·재밍 면역/ImpactDetonation·1인칭 기반 구현/자동 검증. 상세 아카이브/WORKLOG | TestMap에서 Spy 본체·통 크기/위치, 본체/카메라 비간섭, Rotor 회전, 통 상단 케이블 출발과 곡률, 조작·자폭·재밍 면역을 화면 확인하고 BP Transform/굵기·간격을 최종 조정 |
| DRONE-GROUND-01 | 지상 UGV 기반 | 기존 주행·4점 접지·상부 독립 조준에 `UDroneGroundWeaponComponent` 연결. 좌클릭 직사 총탄 25 피해, 우클릭 중력 유탄 100 반경 피해, 수명/쿨다운 적용 | 시험맵에서 상부 방향과 실제 탄도·4발 처치·유탄 낙차/반경을 수동 확인하고 수치 조정 |

#### AI·NPC

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| AI-PATRIOT-PIVOT-01 | 패트리어트 접합부 회전 BP | 초기 생성/재로드 각7회 통과 뒤 10/13 12:50 BP 재저장 확인. 현재 저장본 재검증 대기; [가이드](docs/ai/DRONE_MG_TURRET_3PART_GUIDE.md#6-패트리어트-미사일-포대-접합부-회전축-조정) | 현재 축/이음새·크기·복합 회전 확인. 기존 편집 보존·생성 도구 덮어쓰기 금지. AI/발사·차량 부착 미포함 |
| AI-PERCEPTION-TEST-01 | 감지·수색 PIE와 실기 비교 | 감지·수색 PIE 기존 Fail 유지. D-11로 KnownIssues.AI.NPCPerceptionSearchPIE 분리됨(10/05 C PC Claude), 원인 해결 아님 | Claude가 실기 방향·시야각·감지/수색 비교 후 시험 장면 또는 AI 원인을 판별해 필요한 변경·회귀. Shotgun 실기 정상과 혼동하지 않음. 원본/Production Training 맵 보존 |
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
| SYNC-WORKPC-01 | PC 재개 | 10/14 Drone bb6233c8=로컬 origin/main·MD b38fc84 + Rain/UI·문서 미커밋; STATUS | 사용자 Commit/Push 후 팀원 Pull·Build/실기 확인. 과거 Pass 재사용 금지 |
| SYNC-COLLAB-01 | 협업·다른 PC 세팅 | 공유 파일 최초 5b03ad3(10/02) Commit/Push 완료. ui/image 역할 파일과 이번 변경은 미추적/미커밋. 다른 PC 실제 세팅 미구현 | 사용자 명시 지시 후 남은 파일 Commit/Push→다른 PC Pull·COLLAB_READY→첫 Space 저장 확인 |
| SYNC-SPACES-01 | MD·Space 연결 | 10/14 구현/검증·Gate 저장 수리를 기존4 Page에 반영, 결과 WORKLOG | 사용자 Commit/Push/Pull 후 타 PC 수신. 새 Page·예약·권한·Trello 변경 없음 |

## Next

최신 구현·검증은 [STATUS](STATUS.md), 세션별 수치·로그는 [WORKLOG](docs/history/DRONE_WORKLOG.md)를 따른다. 이전 완료/종료 카드와 Next는 [10월 아카이브](docs/history/archive/WORKBOARD_2026-10.md)에 보존했다.

1. 실제 도시 비 방향 정렬 수리→새RHI 검증 후3품질·회전/이동·차폐/Off 실기. Island Gate 크기/방향·도시 모듈/재질·Pretendard/목록명도 확인. 팀원 Gate 저장은 Source+BP/Build 후 동일 저장 재시험. Production 보존.
2. 실제 패드 첫 강조·전체 UI·1280/1920 가독성·8수업 연속 진행·Best Lap 재실행·설정 저장을 확인한다. KnownIssues4개 분리는 실패 해결이 아니다. 미렌더는 포커스6개 모두 화면 루트 포커스로 실패하는지로 판단한다.
3. 레이싱4코스 전체 진행도/지형은 팀원 보고와 대조 대기. 배터리/고도 수치·경고 연출, D-1·D-2 기획자 대기. D-13 종료·D-12 FPV/UGV 체감 수동 대기; STATUS 참조.
4. DR-INTERLINK-INPUT-01 실기 확인 후 Acro 혼합 입력·코스 표시선·NPC 다리/속도 대비 보폭·총 정렬·이동 뒤 날씨 시험 맵·비 차폐·벽/그물·광섬유/UGV 수동 회귀를 이어간다. WTH-03 비 입자 크기/모양·위치/양·젖음/물결·빗소리/실내 감쇠·패드를 가이드대로 확인한다. 팀원 Production Training 보존; 실제 패키징·Chaos 비교·최종 Rain/음원은 별도 후속이다.
5. 제품 맵 배정은 Battlefield=M1·MilitaryBase=M2/3·MilitaryCamp=M4. 실제 DA 맵/시작/목표 연결은 미완료·MBase M_Target 보류. Git·Space는 STATUS, Commit/Push는 사용자.
