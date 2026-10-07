# Drone 작업 보드

마지막 갱신: 2026-10-06 D PC — 카드 7그룹 정리·PERF-ZEN-START-01 추가·5카드 아카이브(문서 반영 Claude)

## Now

최신 Git·검증 요약은 [STATUS](STATUS.md)를 따른다. 현재 카드·수동 확인 안내·Next만 유지한다.

### 결정 필요 — 현재 DA 값은 채택 사양이 아님

| 항목 | 필요한 결정/자료 | 현재 처리 |
|---|---|---|
| M2 | 실제 타겟 탑승 vs 미끼 결말·시스템 성공/실패·다음 Story Fact | D-1 보류(2026-10-05 사용자): 기획자 내용 대기. 양쪽 분기 기반 유지, M3 반대 분기 첫 대사 비어 있음 |
| M3/M4 | 타겟·적·드론 수량, 성공/실패, 제한·재출격·결과 카메라 | D-2 보류(2026-10-05 사용자): 기획자 내용 대기. M4 시험값 표적3·재출격0(무제한)는 채택 사양 아님 |
| 조종 입력 표시 | 기본값, 장치 자동 전환, 혼합 입력·연결 해제/재연결 | D-3 결정(2026-10-05 사용자): 기본 끔(False), 설정에서 ON/OFF. 기존 구현과 일치·수동 확인 대기. 장치 자동 전환·혼합 입력·연결 해제/재연결 정책 현재 미정 |
| 레이싱 | 코스4개 지형 결정, Ghost/리플레이·커브·Restart/Quit 범위 | D-5 카운트다운·랩 타이머 구현/자동 검증됨(10/06 C PC Claude), 화면 수동 대기. 코스4개 미구현·지형 현재 미정; 상세 RACING-TERRAIN-LINK-01 |
| Tutorial | 회의 4개와 수업 ID 8개의 집계 단위, 권장문구/건너뛰기·완료 영구 저장 | D-4 결정(2026-10-05 사용자): 수업 1~8 그대로 유지. 회의안의 “4”는 레이싱 코스 4개로 해석. 권장문구/건너뛰기·완료 영구 저장 현재 미정 |
| Bangkok 의존 자산 | 방콕·다른 구매/팀원 자산 정리 범위 | D-13 종료(10/05 사용자 결정): 방콕만 삭제, 자연환경 팩·지형 머티리얼·병사 팩·HDRI·RawDrones·NavigationArrows 유지. 삭제 커밋·푸시 상태는 별도 확인 |
| 콘텐츠/전시 | 캐릭터 메시·관찰 시점 적용 맵·조종기 비치/책임, 기록 등급, 브리핑 실명/납품일, 행사일 | 임의 실명·수치·마감일 없음 |



### 면접 대비 결정 필요 — 영향 순서(10/06, 결정·구현 대기 구분)

| 항목 | 필요한 결정/자료 | 현재 처리 |
|---|---|---|
| 1. 제3자 구매 자산 약51GB | GitHub 공개 여부 확인 후 비공개 전환 또는 자산 분리·출처 목록 | D-7 결정(2026-10-05 사용자): 비공개 전환 방향, 사용자가 GitHub에서 직접 전환. 팀원 접근 가능 여부는 GitHub 설정에서 확인 필요(이 PC gh 없음). 향후 공개 시 빌드·코드·영상만(구매 에셋 제외). 10/05 C PC Claude 비로그인 curl HTTP 200 공개 상태 관찰은 이전 전달 근거 |
| 2. 본인 기여와 AI 활용 설명 | 본인 설계·결정·검증 범위를 먼저 확인하고 README에 정직하게 정리 | D-8 결정(2026-10-05 사용자): 본인 기여·AI 활용 README는 md 저장소에만 둠, drone 저장소에는 넣지 않음. 작성 대기·이번 결정만 기록, 본인 담당 범위 미확인 |
| 3. 포트폴리오 루트 README | 플레이 방법·설계/기여·검증 근거·용량/출처를 담을 범위 결정 | D-8 위치 결정은 위 2번 참조. Unreal 루트 README 부재, 이번 신규 작성 안 함 |
| 4. main 상시 실패 테스트4개 | 별도 그룹 분리 또는 조건부 건너뛰기 여부 | D-11 구현됨·자동 검증됨(10/05 C PC Claude): KnownIssues.* 분리·기본 Automation RunTests Drone.에서 제외. 실패 해결 아님; 상세 WORKLOG |
| 5. Flight Pawn 분리·명명 | 분리 전 동일 체감 확인 | D-12 2·3차 구현됨·자동 검증됨(10/06 C PC Claude): Flight 명명·Shake/Acro/Ground 컴포넌트 분리, BP 유지. FPV/UGV 수동 확인 대기; 상세 WORKLOG |
| 6. Legacy 템플릿 | 정리 후 수동 회귀 | D-12 1차 구현됨·자동 검증됨(10/05 C PC Claude). Characters 변환 원본 유지; 삭제 목록·근거 WORKLOG |
| 7. 방콕·미사용 자산 | 정리 범위 | D-13 종료·사용자 결정 정본은 위 Bangkok 행. 상세 [WORKLOG](docs/history/DRONE_WORKLOG.md) |
| 8. 풍향 기준 | HUD 방위와 거울상 불일치, 불어오는 쪽 기상 관례 채택 여부 | D-6 구현됨·자동 검증됨(10/05 C PC Claude): HUD 방위 통일·불어오는 쪽 풍향·미션별 배터리 제한/추락. 바람 물리 유지·수동 확인 대기. 시간 값 미정·높이 제한은 아래 D-6 행 참조. 상세 STATUS |
| 9. 공유 Config MCP | PC별 연결 확인 | D-14 공유 끔·사용자 PC 로컬만 켬, 팀원 불필요. CLAUDE.md 설명 수정됨(10/06 Claude). 절차 [협업 세팅](docs/git/CLAUDE_CODEX_SETUP.md#unreal-mcp-자동-시작--pc별-로컬-설정) |
| 10. BP/Legacy API | 호출 없는 함수19개·1회 접근자71개가 디자이너용인지, 핸들링 Legacy 정리 | 미사용 UFUNCTION18개 삭제됨(D-12 1차)·나머지 접근자/Legacy 범위는 별도 결정 대기 |

스냅숏 백로그 GIT-LFS-CAP-01·AI-TOOL-REVIEW-01은 현재 카드 없음(09-15 스냅숏), 복원/보류/폐기 결정 대기.

완료·종료 카드·현재 카드의 이전 장문 근거·지난 Next·수동 맵 안내는 [10월 보드 아카이브](docs/history/archive/WORKBOARD_2026-10.md)에 원문 보존했다. 10/06 D PC: RACING-MEETING-01·FIGMA-RACING-02·MISSION-FRAMEWORK-01·MAP-TEST-01(대체)·TUTORIAL-GUIDE-03(완료)도 이동. 현재 수동 순서는 [테스트 가이드](docs/gameplay/DRONE_TEST_MAP_GUIDE.md)를 따른다.


### 카드 그룹

회의 후 카드는 각 그룹 맨 앞에 둔다.

#### 튜토리얼·코스·레이싱

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| TUT-COURSE-SMOOTH-01 | 장거리 코스 표시선 곡률 분할·BP 표시 예산 | 구현됨·자동 검증됨·수동 확인 대기(10/04 C PC Claude). 긴 코스 곡률 분할·기본1024(시작값·미확정), BP 드래그 재구성 Off. 수치·근거 STATUS/WORKLOG | 팀원 Production 코스 외형·급커브/끝 연결·Editor 편집 체감 수동 확인. BP2048(측정 최대20cm) 검토 가능. 짧은 TestMap68/113조각 기존 균일 분할 유지·Production 저장/재생성 금지 |
| RACING-TERRAIN-LINK-01 | 레이싱 흐름·지형 연결 | D-5 구현됨·자동 검증됨(10/06 C PC Claude). 3·2·1 중 잠금/정지·타이머 숨김/미측정, 출발0초→상단 중앙 `00:00.00`, 첫 게이트 재시작 없음. 상세 STATUS/WORKLOG | 카운트다운·랩 타이머 화면 수동 확인. 코스4개 미구현·지형 미정, 확정 뒤 Claude 연결·Production 보존 |
| TUT-PROGRESS-01 | 튜토리얼 클리어 시간·다음 수업·n/8·전체 완료 UI | 구현됨·자동 검증됨·수동 확인 대기(10/02 C PC Claude). Tutorial8·Story4 다음 연결, 시간·n/8·전체 완료/로비 표시. 완료 기록은 실행 메모리; 검증 WORKLOG | 결과 글자/배치·실제 8수업 연속 진행·로비 완료 가독성·S49 미션 진행→M1/시작 메뉴→타이틀 수동 확인. 별도 WBP 4개 없음, Production Training 보존 |
| TUT-BRIEFING-TEXT-01 | 튜토리얼 조작키 브리핑 문구 결정·입력 | 미구현·문구 현재 미정. Codex research 2026-10-02: 8수업 키보드 키, 자폭/드랍/UGV NPC/포탑 패드 키·대사, 튜토리얼 화자 Figma 미기재. 호버/전진/회전/게이트 패드 브리핑 원문 있음. 이번 조작키 브리핑 미입력 | 사람이 미기재 문구·화자를 결정한 뒤 Claude가 DA/UI 연결·검증, Story 허브를 튜토리얼 화자로 추정하지 않음 |
| TUT-COMPLETION-SAVE-01 | 완료 수업 기록 영구 저장 여부 | 현재 미정·영구 저장 미구현. CompletedMissionIds는 이번 실행만 유지하며 Best Lap JSON 저장과 별개 | 저장 여부/범위를 사람이 결정한 뒤 Claude가 필요한 구현·재실행 회귀, 결정 전 완료로 표시하지 않음 |
| TUT-ORBIT-02 | 회전 수업 = 원형 코스 한 바퀴 | Heading DA ID 호환 유지, Closed Spline·9 Gate, Tag별 Recorder·HUD, 다른 코스 비활성. 독립 Heading 수업 맵으로 연결 | 실제 비행 제자리 Yaw/다른 코스/7⁄8 바퀴 미완료, 결승→귀환→성공 확인 |
| TUT-GATE-PRESENTATION-01 | Gate 통과음·위치·크기·자산 재질 | Gate 음성/Sound 슬롯·BP 연출·하단1/6 위치·공통/개별 Scale·상태 재질 구현/자동 검증. 실제 음원/최종 Mesh 후속 | 실제 음원·최종 Gate Mesh를 BP에 지정한 뒤 TestMap에서 가청성, 1/6 위치, 확대해도 선 크기 불변, 상태별 재질·미지정 슬롯 보존을 수동 확인. 팀원 Production 맵은 직접 저장하지 않음 |
| TUT-ROUTE-SELECT-01 | Training Route 4개 선택 시험 | `Lvl_DroneTrainingRouteSelectionTest`에 직선·좌곡선·우곡선·상승 슬라럼과 Gate 각 5개 배치. `1~4` 고정·`5` 무작위, 단일 활성, 진행 초기화, HUD 기록 Source 전환. Build·Map Check·API/저장/실제 키 PIE 성공 | 사용자가 화면에서 경로 형태·Gate 간격·랜덤 전환과 Lap HUD를 확인하고 각 Spline 점을 최종 조정 |
| TUTORIAL-MISSION-01 | Figma Tutorial 8개 독립 Mission | 수업별 `TestMap/Tutorial` 8맵·DA·직접 Play Entry 구현, 공용 종합 시험장 보존. 다른 PC의 Hover 로비/직접 PIE에서 3초 유지→귀환 Success. 비충돌 표식 4개 유지 | FrontEnd와 각 독립 맵에서 Hover 가독성 및 8수업 전체 위치·목표·결과를 수동 확인. 이전 사용자 7개 대략 확인과 최종 완주를 구분 |
| TUT-BEST-01 | Course별 Best Lap 영구 저장 | 구현됨·자동 검증됨·수동 확인 대기(10/02 C PC Claude). 코스/기체/조작별 Best Lap JSON·HUD, 자동화 별도 슬롯. 평균은 실행 History | 같은 조건 실제 완주2회·재실행 복원·첫 완주 전 HUD 확인. D-5 결과 시간은 RACING-TERRAIN-LINK-01 참조 |
| TUTORIAL-FIGMA-02 | Figma 8개 훈련 ↔ Test Map 대조 | 8개 기능/DA·독립 시험맵·시간·연속 진행·전체 완료 UI 구현과 기존 자동 검증 보고가 있음. 2026-10-03 DA 순서 재확인; Warehouse 최종 환경은 별도 | 기존 진행 UI의 실제 8수업 연속 완주·결과/로비 복귀를 수동 확인. D-4 수업1~8 유지·회의4는 레이싱 코스4개. Warehouse 범위 결정, 결과 UI 중복 구현 금지 |

#### UI·설정·패드

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| UI-CONTROL-LAYOUT-01 | 조작 이름·가로폭 | Codex 예외 수정·자동 Pass; WORKLOG | 1280/1920·패드 수동 확인 |
| UI-RESULT-LAYOUT-01 | 결과창 | 수정·자동검증; WORKLOG | 화면·패드 수동 확인 |
| UI-FOCUS-RACE-01 | UIOnly 루트/버튼 지연 포커스 경쟁 | 수정 후 확인 중(10/04 C PC Claude). 5프레임 루트/없음 이탈 복원·다른 버튼 이동 보존. 렌더 전 Fail/후 Success 각1회·단독 혼재, 수정→확인2회에서 중단 | 실제 결과·타이틀 첫 버튼 강조 반복 확인 및 화면 그려진 회귀 추가 관찰. 패드 다른 버튼 이동을 빼앗지 않는지 확인, 안정화 완료로 추정하지 않음 |
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
| MISSION-CHECKPOINT-01 | 실패 시 시작/중간 지점 재출격 | 구현됨·자동 검증됨·수동 확인 대기(C PC Claude). 파괴/시간/Trigger 통합 재출격, 맵·목표·표적 유지. 실제 체크포인트 미배치·첫 출격 위치 재출격 | 맵 체크포인트 배치, M1 픽업 지점은 정보단말 회수 구현 뒤. 재출격 브리핑 재생은 MISSION-BRIEFING-02 뒤(여부 현재 미정). 튜토리얼 추락→동일 기체/조작·현재 목표 시간 재설정·목표/표적 유지·재출격 체감 수동 확인. Production Training 보존 |
| MISSION-BRIEFING-02 | HUB 보이스·자막 브리핑·진입 1회 시네마틱 | 자막·Voice 슬롯·자동 진행/Y·Tab/정지 구현·BriefingLinesPIE Success(2026-10-02 C PC Claude, ClaudeBriefing/test2.log). Story M1 4·M2 4·M3 5(조건 없으면 4)·M4 6줄 원문 입력, 화자 허브. M3 첫 줄 Story.TargetEliminated 조건 | 자막 가독성·속도 수동 확인. 음원 없음·튜토리얼 대사 미입력·1회 시네마틱 완료 근거 없음. 반대 분기 M3 첫 대사와 M2→M3 분기·재출격 재생 여부 현재 미정 |
| HUD-FIGMA-01 | HUD 배터리·기체명·신호 대역·풍향 | D-6 구현됨·자동 검증됨(10/05 C PC Claude). HUD 방위 통일·불어오는 쪽 풍향, 미션별 배터리 제한/방전 추락 추가. 상세 STATUS/WORKLOG | 풍향 HUD·배터리/HUD 가독성 수동 확인. 배터리 시간 모두0·현재 미정·값 확정 뒤 추락 체감 확인. 높이 제한은 아래 D-6 행 참조·신호 대역 미정 |
| D-6 높이 제한 | 배치 매니저·BP 값으로 적용 | 구현됨·자동 검증됨(10/05 C PC Claude). BP_DroneAltitudeLimitManager 배치·값 설정, 상세 [WORKLOG](docs/history/DRONE_WORKLOG.md) | 천장 체감 수동 확인 대기. 높이 제한 수치·경고 연출 현재 미정 |
| STORY-TEST-01 | Story Mission별 격리 TestMap 4개 | GoldenTime Drop/Return, Intercept Spline 차량·목적지 실패, VeilBreaker 재밍 이탈/Return, Endgame UGV 표적 3개/Return과 DA 4개 존재. 4맵 직접 Play Entry 및 FrontEnd Catalog 총 14개 연결. Oct 1 다른 PC의 14맵 점검에 포함 | 각 맵 FrontEnd/직접 Play에서 목표·실패·귀환 수동 확인. 미구현 후보를 이 카드에 합침(Claude 지시서·Figma 매트릭스 Mission 1~4): M1 정보단말 회수·요원 NPC, M2 잔해 Scan·반전, M3 한 미션 내 기체 교대·MANPADS/베일 카운트, M4 장거리 타격·엔딩 시네마틱. 스토리 충돌·MANPADS/베일 표기는 현재 미정, Production Training 보존 |
| MISSION-RULE-PIE-01 | 새 목표 Rule의 실제 맵 Vertical Slice | 귀환·Jammer·역할 Actor 시험 배치 완료, 직접 실행은 Prototype Flow | Test Mission DA/진입 경로에서 Scan/Delivery/Destroy/Return/Jamming Event·Tag·시간 규칙 확인 |
| STY-03-PIE-01 | 재밍 신호·비행·HUD Vertical Slice | 35%/80% 겹침 Zone TestMap 배치·저장 계약 완료 | 실제 비행으로 Overlap·HUD·둔화/복원 확인. 영상 Noise WBP는 별도 표현 작업 |
| STORY-BRANCH-01 | Mission 2→3 양쪽 스토리 분기 | Story Fact 저장·성공 적용·조건 목표 필터, 미끼/실제 탑승 양쪽 자동화 완료 | 사용자가 기본 스토리안을 정하면 실제 Mission DA에 Fact 설정 |

#### 비행 물리·조작·기체

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| PAYLOAD-GRIP-01 | 집게 부착 통일 | Codex 예외 수정·자동 Pass; WORKLOG | 시작→투하→재픽업 외형 확인 |
| ACRO-MEETING-01 | Mode1 Space 하강·반전 및 키보드/패드 겹침 수정 | 구현됨·자동 검증됨·수동 확인 대기(10/04 C PC Claude). 입력원 분리·절댓값 큰 쪽·키 해제 시 패드 인계, 기존 Dead Zone·정확 적분 유지. 근거 STATUS | Mode1 스틱에 엄지를 걸친 채 Space→상승, 키 떼고 스틱→패드 조종, 모두 놓으면0을 실제 장치로 확인. Mode2도 혼합 입력 확인. W/S·A/D·Q/E·Space/Ctrl은 두 Mode 동일; 키보드 배율·Angle·마우스Yaw·회의 반전 뜻 현재 미정 |
| DR-FPV-ACRO-INPUT-02 | Acro 키보드·패드 Mode 1/2 | InterLink Acro 4축 추가·총45매핑·Dead Zone 계약 자동 검증됨(10/07 D PC Claude). [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md), 혼합 입력은 ACRO-MEETING-01 | Mode 1/2 실기 혼합 입력·비행 체감 확인. 조작 정책/회의 반전 뜻 미정 |
| DR-INTERLINK-INPUT-01 | InterLink DX 입력·메뉴 | 구현/자동 검증됨·실기 대기(10/07 D PC Claude): 45매핑·ArmSwitch·노브 전체 이동. [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md) | 축/DZ·Mode2·Button1 무장/해제 체감·12/13, 노브 전체 이동/탭·방향·설정 확인. 전체 테스트 집계 재확인 |
| DR-FPV-ACRO-PIE-01 | FPV Rate/Acro 실제 조작 체감 | Mode 1/2 축 분리와 각속도·무수평복귀에 공통 질량·추력·모터 응답·중력·Body Up 추진·선형/제곱 항력 v2 연결. 별도 속도 단계는 제거 | 키보드/패드로 Nose-down 전진력, 호버·상승·무추력 하강, Roll/Loop와 650°/s 체감, Mode 1/2가 축 배치 외 비행 성능이 같은지 확인 후 수치 조정 |
| DR-FLIGHT-PHYS-02 | 단일 고속 기준·질량/추력·Payload 하중 | 단일 무적재 고속 기준·질량/추력/모터/항력·Drop kg 하중 구현/자동 검증. Mode1/2 공통·투하 즉시 복구·이전 근거 WORKLOG | FPV/Drop 수동 비행으로 무적재 속도, 모터 추력 지연, 적재 전후 호버·가속·선회 차이와 Mode 1/2 축만 달라지는지 확인. 실제 기체 스펙이 정해지면 Definition별 질량·추력·항력 교정 |
| PHY-CAMERA-01 | 벽·그물 접촉 화면 안정화 | 구현됨·자동 검증됨·수동 확인 대기. 연속 접촉 제약·외형/FPV 카메라 분리·그물 Camera Ignore, 피해 Shake 유지. 검증 WORKLOG | Physics Sandbox에서 1/3인칭 저속/고속/지속 벽 접촉·그물 감속/포획 때 화면 떨림 감소와 충돌 유지 확인. NPC 맵에서 총알 피격 화면 흔들림이 남는지 확인. 자동화만으로 체감 Pass 처리하지 않음 |
| PHYSICS-SANDBOX-01 | 벽 충돌·그물 얽힘·국소 파괴 벽 | 벽 반발·날개 접촉·그물 감속/포획/하강·탄환/폭발 국소 절단 구현/자동 검증. 실제 Chaos 비교 별도·이전 근거 WORKLOG | Sandbox에서 저속 접촉은 작게 밀리고 고속 충돌은 크게 반발하는지, 날개 끝 접촉 방향의 자세 Kick, 그물 포획·하강·자동 해제와 조종 복구를 화면 확인하고 실제 Chaos Cloth/Dataflow와 Geometry Collection을 별도 구역에서 비교 |
| PHY-NET-03 | 그물 날개 걸림·포획 장애물 | 날개 Probe·감속/추력·조종 저하·자세 교란·포획/하강 Greybox 구현, 일반 충돌 절단 기본 Off. Chaos 시각 변형은 후속 | 수동 체감 조정 뒤 Chaos Cloth 시각 변형 + 필요 시 전용 Net Interaction Volume + 역추진/접촉 해제 탈출·Crash/Mission 실패를 연결하고 Standalone 3회 확인 |
| PHY-COL-01 | 모든 벽·구조물 공통 반발 | 일반 비행체 공통 반발·Wing/Rotor Probe 구현/자동 검증. 충돌 속도 비례 반발·분리·회전·바닥/천장·Ground UGV 제외 | Sandbox와 다른 TestMap에서 연속 입력 비비기/침투·날개 Probe 크기/방향을 수동 확인하고 강한 Crash/Damage 우선순위·Landing 상태·얇은 벽 Sweep/CCD를 후속 구현 |
| DRONE-FIBER-01 | 광섬유 Drone 기반 | DroneSpy·GSU 통·Rotor·재질·다점 케이블·재밍 면역/ImpactDetonation·1인칭 기반 구현/자동 검증. 상세 아카이브/WORKLOG | TestMap에서 Spy 본체·통 크기/위치, 본체/카메라 비간섭, Rotor 회전, 통 상단 케이블 출발과 곡률, 조작·자폭·재밍 면역을 화면 확인하고 BP Transform/굵기·간격을 최종 조정 |
| DRONE-GROUND-01 | 지상 UGV 기반 | 기존 주행·4점 접지·상부 독립 조준에 `UDroneGroundWeaponComponent` 연결. 좌클릭 직사 총탄 25 피해, 우클릭 중력 유탄 100 반경 피해, 수명/쿨다운 적용 | 시험맵에서 상부 방향과 실제 탄도·4발 처치·유탄 낙차/반경을 수동 확인하고 수치 조정 |

#### AI·NPC

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
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
| WTH-03 | 비 품질·연출 | 구현됨·자동 검증됨(10/07 C PC Claude). 전 단계 원본 Niagara1개·판 빗줄기 기본0·Weather 전체/SettingsContract Success; [가이드](docs/gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md#비-품질-설정과-조정)·검증 WORKLOG | 입자 크기/모양·위치/양·젖음/물결·음원/실내 감쇠·패드 수동 확인. 수치/음원 확정 미정; 화면 물방울/Splash 미구현 |

#### 테스트·빌드·성능·동기화

| ID | 작업 | 현재 상태 | 완료 조건 |
|---|---|---|---|
| TEST-RENDER-UNPAINTED-01 | PIE 미렌더 판정 구분 | D-11 구현됨·자동 검증됨(10/05 C PC Claude). 상시 실패4개 KnownIssues 분리. 최신 전체101개 결과 STATUS 참조. 미렌더는 포커스6개 모두 화면 루트 포커스로 실패하는지로 판단 | 화면 그려진 포커스/실제 패드 수동 확인·KnownIssues 별도 실행. 같은 증상2회 상한·Production 보존 |
| TEST-ORDER-ROUTE-01 | 전체 렌더 회귀 Route 키 순서 의존 관찰 | 2026-10-04 C PC ClaudeAcroFull 전체5회(test.log/test2.log/final.log/final2.log/test3.log) TrainingRouteSelectionPIE 모두 Success(Codex 로그 대조). 그중3회 화면 미렌더이므로 화면 검증과 구분. 지난 Fail은 날짜별 기록 보존, 원인 미특정·해결 확정 아님 | 재발 시 선행 테스트/입력 처리 순서 재현·Claude 조사. Production 맵 보존 |
| BUILD-PACKAGE-01 | 패키징 쿠킹 설정 | 정적 자동 검증됨(10/02 C PC Claude). Mission/Drone DA AlwaysCook·MissionMap Soft 참조. 실제 패키징 미실행; 검증 WORKLOG | 실제 패키징 미실행. 패키지에서 DA 자동 등록·모든 MissionMap 진입 확인, Production Training 보존 |
| PERF-ZEN-START-01 | D PC Editor 시작 지연(Zen 대기) 조사 | 원인 특정(10/06 D PC Claude): Zen 세션 기록 733개 로드 약 20초 + 엔진 20초 초과 모달. 10/02 473초는 모달 미응답 대기. 세션 폴더 732개 백업 이동 완료, 재측정 대기. 상세 STATUS/WORKLOG | Claude가 같은 맵·캐시로 cold/warm 시작 로그 비교, 확인창 응답·Zen running→Editor 확인 시간 분리. 캐시 삭제·엔진 소스 수정·보안 해제 금지, Production Training 보존 |
| SYNC-WORKPC-01 | PC별 즉시 재개 인계 | 10/06 09:32 D PC: MD c5a0524·Unreal 1619b4f 일치, LFS 8,010개 본문 수신·Clean·lock 없음, 정본 STATUS/WORKLOG | Training 맵 본문/자산 변경 표시를 확인. 소스/LFS 본문·바이너리·자동/수동 Pass 구분, Discard 금지 |
| SYNC-COLLAB-01 | 협업·다른 PC 세팅 | 공유 파일 최초 5b03ad3(10/02) Commit/Push 완료. ui/image 역할 파일과 이번 변경은 미추적/미커밋. 다른 PC 실제 세팅 미구현 | 사용자 명시 지시 후 남은 파일 Commit/Push→다른 PC Pull·COLLAB_READY→첫 Space 저장 확인 |
| SYNC-SPACES-01 | MD·Spaces·Trello 정리 연결 | 10/06 Codex: 기존 진행/테스트/BP/안내 Page 갱신·재조회. 상세 WORKLOG | 다른 PC 지침 전달은 사용자 Commit/Push/Pull. 실시간/예약 자동화·Trello 수정 없음 |

## Next

최신 구현·검증은 [STATUS](STATUS.md), 세션별 수치·로그는 [WORKLOG](docs/history/DRONE_WORKLOG.md)를 따른다. 이전 완료/종료 카드와 Next는 [10월 아카이브](docs/history/archive/WORKBOARD_2026-10.md)에 보존했다.

1. 레이싱 카운트다운·출발0초 타이머·상단 중앙 표시·첫 게이트 재시작 없음과 풍향 HUD를 수동 확인한다. 배터리 시간 결정 뒤 추락/재출격 확인.
2. 실제 패드 첫 강조·전체 UI·1280/1920 가독성·8수업 연속 진행·Best Lap 재실행·설정 저장을 확인한다. KnownIssues4개 분리는 실패 해결이 아니다. 미렌더는 포커스6개 모두 화면 루트 포커스로 실패하는지로 판단한다.
3. 코스4개 지형·배터리/고도 수치·경고 연출 미정. D-1·D-2 기획자 대기, D-13 종료. D-12 FPV/UGV 체감 수동 대기; 검증/Git은 STATUS 참조.
4. DR-INTERLINK-INPUT-01 실기 확인 후 Acro 혼합 입력·코스 표시선·NPC 다리/속도 대비 보폭·총 정렬·이동 뒤 날씨 시험 맵·비 차폐·벽/그물·광섬유/UGV 수동 회귀를 이어간다. WTH-03 비 입자 크기/모양·위치/양·젖음/물결·빗소리/실내 감쇠·패드를 가이드대로 확인한다. 팀원 Production Training 보존; 실제 패키징·Chaos 비교·최종 Rain/음원은 별도 후속이다.
5. Git·Space는 STATUS. Commit/Push는 사용자.
