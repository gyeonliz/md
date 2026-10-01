# 현재 작업 상태

기준일: 2026-10-02 (Asia/Seoul)

## 2026-10-02 새벽 후속 — TUT-PROGRESS-01·스토리 순서 연결

- 기준: C PC Unreal HEAD `ec2e88f` + 로컬 미커밋, 작업 도구 Claude·문서/Space 반영 Codex. 구현·검사 조건은 Claude 지시서 근거이며 Codex는 HEAD와 지정 전체 회귀 로그의 결과를 읽기 전용 대조했다. Build·Editor Python·PIE·맵 생성·수동 검증은 이번 문서 작업에서 실행하지 않았다.
- `TUT-PROGRESS-01`: **구현됨·자동 검증됨·수동 확인 대기**. Mission DA `NextMissionId`로 호버→전진→회전→게이트→자폭(FPV)→드랍(Payload)→UGV NPC→포탑(끝)을 연결했다. Story는 Figma 번호 M1 골든타임→M2 인터셉트→M3 베일브레이커→M4 엔드게임(끝), 공용 Training·Racing은 연결 없음. Editor Python으로 DA 12/12 저장·재조회(exit 0), 맵 미수정(ClaudeTutProgress/py.log·py2.log). Story 연결은 순서만 정하며 M2→M3 결과 분기는 현재 미정이다.
- `UDroneGameFlowSubsystem`이 성공 결과에서만 `RequestNextMission`으로 FrontEnd의 다음 수업 브리핑(MissionTrailer)을 열고 [출격]하면 해당 맵으로 이동한다. GetNextMissionId/GetMissionSequence(고리 방어)/GetMissionSequencePosition/IsMissionCompleted/GetMissionIdsInLobbyOrder, RequestReturnToLobbyFocusing·RequestReturnToTitle 연결. Snapshot `CompletedMissionIds`는 이번 실행 동안만 유지(영구 저장 현재 미정), `LastMissionElapsedSeconds`는 Director가 World 시간으로 계산한 출격~결과 시간(재출격 포함), 공개 GetMissionElapsedSeconds(). Widget이 시간을 재지 않는다.
- 결과 `UDroneMissionResultWidget`이 S48/S49를 담당한다. 수업 완료는 “훈련 완료”·수업 이름·“시간 mm:ss.cc”·“수업 n/8 | 완료 c/8”, [다음](패드 첫 포커스)·[다시하기]·[작전 로비로 복귀](Figma에는 없지만 유지). 8개 모두 완료는 “훈련 완료”·“이제 운용 할 준비가 되었습니다.”·“수업 8/8 모두 완료”, [미션 진행](로비 미션 탭 M1)·[시작 메뉴](타이틀), [다시하기] 숨김. Story 등은 “미션 성공”·“클리어 시간”·“미션 n/4 | 완료”·[다음 미션: 이름], 실패는 “진행 시간”과 첫 포커스 [다시하기].
- 로비 튜토리얼은 수업 순서(호버 맨 위·공용 Training은 그 뒤), 미션은 M1→M4. 이번 실행 성공 미션 이름 뒤 “· 완료”, 설명에 “수업 n/8 (완료 c)”/“순서 n/4”. Tutorial Text 6개와 선택 WBP 이름은 튜토리얼 가이드 5절에 정리했다.
- 자동 검증(Claude, C PC, RenderOffScreen 1920×1080, `C:\URproject\drone\Saved\Automation\ClaudeTutProgressFull\test2.log`): 신규 `Drone.Flow.TutorialProgression`·`TutorialNextLessonPIE`·`TutorialCompletePIE` **3건 Success**. 순서/위치/고리 방어·실패 시 다음 불가·8개 연속 다음·시간/완료 8/8·타이틀·로비 정렬·M1 포커스, 실제 호버 클리어→S48→전진 브리핑을 검증했다. 전체 완료 PIE는 나머지 7개를 테스트용 완료 처리한 뒤 호버 클리어→S49를 검사했으며 실제 8수업 수동 완주 근거는 아니다.
- 최신 전체 `Drone.*` 렌더링 회귀: **87개 중 81 Success·6 Fail**(같은 로그). NPCPerceptionSearchPIE=기존 AI-PERCEPTION-TEST-01, TrainingAssets·TrainingPIESmoke=기존 팀원 Production 맵, ShotgunSystemsTestMapPIE=렌더링 실행에서만 실패/NullRHI 통과(`AI-SHOTGUN-RENDER-01`), LobbyLayoutStabilityPIE=실행마다 첫 프레임 높이·판정 변동(10/01부터 관찰, `UI-LAYOUT-DIAG-01`), TrainingRouteSelectionPIE=전체 렌더링 회귀에서만 숫자키 미반영(`TEST-ORDER-ROUTE-01`). Route는 최대 30프레임 대기에도 Route 1 유지, 단독·패드 테스트 뒤·Training Smoke 뒤 Success이며 원인 선행 테스트 미특정. 전체 Pass로 확대하지 않는다.
- 테스트 정리(기능 변경 아님): GamepadMissionFlowPIE는 호버 최상단에 맞춰 ↓ 탐색을 보정하고 결과 검사 동안만 호버 DA를 메모리에서 결과 화면 모드로 변경(저장 안 함). TrainingRouteSelectionPIE는 숫자키 대기를 1→최대 30프레임으로 변경했다.
- 수동 확인 대기: 결과 화면 배치·글자, 실제 8개 연속 진행 체감, 로비 “· 완료” 가독성, 전체 완료 뒤 [미션 진행]·[시작 메뉴]. 현재 미정: 완료 영구 저장, Figma 미기재 조작키 브리핑 문구/화자, 4-1·4-2 통합, M2→M3 결과 분기. Figma에 패드 브리핑 원문이 있는 호버·전진·회전·게이트 4개와 달리 자폭·드랍·UGV·포탑은 키/대사가 없으며 튜토리얼 조작키 브리핑은 넣지 않았다.

- Drone Space(2026-10-02 새벽 후속): 기존 진행상황과 다음 작업 3개·테스트 맵과 확인 가이드 1개·Blueprint 조정과 팀원 가이드 2개 연산 저장(총 6개, 거부 없음). 세 페이지 저장 후 재조회에서 구현/Story 순서·87개 판정·수동 절차·NextMissionId/Tutorial Text 6개/선택 WBP 이름의 기대 본문 7개가 모두 일치했다. 이번 대상 미반영 없음. 새 Page·Commit/Push·Unreal 쓰기·Build/PIE/맵 생성·Trello/Figma 수정은 하지 않았다. GitHub 로컬 MD 본문은 사용자 Commit/Push 후 반영된다.

## 2026-10-02 새벽 — NPC 테스트·허브 브리핑·HUD 배터리·Best Lap·패키징 설정

- 기준: Asia/Seoul 2026-10-02 새벽, C PC Unreal HEAD `ec2e88f` + 로컬 미커밋. 구현·자동화 작업 도구 Claude, 문서·Space 반영 Codex. 허브 원문 수집은 Codex research(2026-10-01). 구현 상세·검사 조건/수치는 Claude 지시서 근거이며 Codex는 HEAD·관련 선언·지정 로그 결과를 읽기 전용으로 대조했다. Build·PIE·맵 생성·패키징·수동 검증은 이번 문서 작업에서 실행하지 않았다.
- `TEST-NPC-COUNT-01`: 테스트 갱신됨·자동 검증 **3/4 Success**, 맵 미수정. 9/22 사용자가 Rifle 2·Shotgun 2(기본 BP_NPC_Hostile_* 이름), 두 번째 차량·포탑·Spline을 추가한 장면을 보존한다. 구성 검사는 생성 기준 이상(NPC 클래스별 하한, Smart Object 12 이상, 차량/포탑 1 이상, 포탑 수 ≥ 차량 수), 차량은 Greybox 자동 주행 또는 Spline 경로를 허용. PIE 장면 3개는 `NPC_` 기준 4명(적 2·아군 2)만 판정하고 감지·수색은 PIE 월드 안에서만 추가 NPC를 제거한다. NPCGreyboxAssets·NPCGreyboxPIE·NPCBaseRoutinesPIE Success. NPCPerceptionSearchPIE는 여전히 Fail: 기준 적 1명이 합성 자극 뒤 실제 시야 감지를 유지하지 못함(`state=1 detected=0`). 추가 NPC 제거 뒤에도 같아 간섭은 아니며 방향·시야각 계열은 추정이다. AI 코드 미변경, `AI-PERCEPTION-TEST-01` 실기 비교 필요.
- `MISSION-BRIEFING-02`: **자막·음성 슬롯 구현됨·자동 검증됨·수동 확인 대기**. Mission DA `BriefingLines`(화자·자막·Voice·표시 시간·스토리 조건)을 브리핑 아래 고정 높이 영역에 순서대로 표시한다. 월드 타이머 자동 진행(음성 길이 또는 글자당 0.075초, 2.5~9초), 패드 Y/Tab 건너뛰기, 마지막 줄 유지, 화면 이탈 시 정지. FrontEnd Root Class Defaults의 `BriefingSecondsPerCharacter / BriefingMinLineSeconds / BriefingMaxLineSeconds`로 조정. Figma Slide 34/42/43/44 원문을 Story DA M1 4·M2 4·M3 5·M4 6줄, 화자 허브로 입력. M3 “오마르는 처리됐다…”는 `Story.TargetEliminated`가 있을 때만 표시(없으면 4줄). 반대 분기 첫 대사는 원문이 없어 비워 둔다. **음원 없음, 튜토리얼 대사 미입력**, 진입 1회 시네마틱 완료 근거 없음. 재출격 브리핑 재생 여부는 현재 미정.
- `HUD-FIGMA-01`: **배터리·기체명·신호 대역 HUD 구현됨·자동 검증됨·수동 확인 대기**. 기존 풍향 기호(N/E/…)·풍속 구현 확인. 모든 기체 기본 `DroneBatteryComponent`, 비행 프로필 `BatteryLifeSeconds`(0=끔), 플레이어 조종 중만 소모, `LowBatteryFraction=0.2`. `DepletedResponse` 기본 WarnOnly(경고만), 선택 FailMission(미션 실패, 미션 재출격 설정이면 재출격). 오른쪽 위 바람 아래 기체명 | `SignalBandLabel` / `BATTERY nn% (mm:ss)`, 부족은 빨간색·“부족”, 소진은 “방전”; 비활성 기체는 배터리 줄 숨김. **현재 모든 기체 시간 0·신호 대역 빈 값**, 5.8GHz는 시험 예시이며 실제 값·소진 처리는 현재 미정.
- `TUT-BEST-01`: **유효 완주 최고 기록 JSON 저장 구현됨·자동 검증됨·수동 재실행 확인 대기**. `DroneTrainingRecordSubsystem`이 `CourseId|DroneId|ControlMode`별 저장(HandlingPreset 제외). `Saved/SaveGames/DroneTrainingBestLaps.json`; 없음=NoSave, 구버전·손상은 백업 후 새로 시작(손상 `<슬롯>_Corrupt_<시각>.json`). 자동화는 `DroneTrainingBestLaps_Automation.json`으로 실제 기록 보호. BestElapsedSeconds는 실행 History와 저장 기록 중 빠른 값, `bHasSavedBest / SavedBestElapsedSeconds / bIsNewSavedBest` 반영. 첫 완주 전 HUD에도 “최고 완주 기록 nn.nn초 (저장)” 표시. 손상 USaveGame 바이너리 로드가 FName 길이 Assert로 엔진 정지를 일으켜 JSON 텍스트로 변경했다. 평균은 실행 History 기준, 정식 레이싱 방식 확정 아님.
- `BUILD-PACKAGE-01`: **쿠킹 설정 구현됨·정적 자동 검증됨·실제 패키징 미실행**. `Config/DefaultGame.ini` Asset Manager에서 `DroneMission`(/Game/Drone/Data/Missions)·`DroneDefinition`(/Game/Drone/Data/Drones) AlwaysCook, MissionMap Soft 참조 맵도 함께 쿠킹하도록 설정. 패키징 실행 성공으로 확대하지 않는다.

### 자동 검증 출처(Claude 실행, C PC, NullRHI)

| 검사 | 결과 | 로컬 로그 |
|---|---|---|
| NPC 4개 | 3 Success, PerceptionSearch Fail | `C:\URproject\drone\Saved\Automation\ClaudeNPCMap\test.log`·`test2.log` |
| Drone.Flow.BriefingLinesPIE | Success: 첫 줄·화자/자동 진행/Y·Tab/마지막 줄/정지/M3 조건 없을 때 4줄 | `C:\URproject\drone\Saved\Automation\ClaudeBriefing\test2.log` |
| BatteryHUDPIE + HUD 2개 + CheckpointRestart | 4/4 Success: 기체명·5.8GHz·100%, 비행 소모·부족, FailMission→Hover 재출격·새 배터리 | `C:\URproject\drone\Saved\Automation\ClaudeHUD\test.log` |
| Drone.Tutorial.* + BestLapPersistence | BestLapPersistence 및 나머지 튜토리얼 Success, 기존 Production Training 맵 TrainingAssets·TrainingPIESmoke 2건 Fail | `C:\URproject\drone\Saved\Automation\ClaudeBestLap\test2.log` |
| Drone.Flow.PackagingPrimaryAssets | Success: 미션 14·기체 5 AlwaysCook, 모든 미션 맵 존재 | `C:\URproject\drone\Saved\Automation\ClaudePackaging\test.log` |

- 수동 확인 대기: Story 미션 선택→브리핑 자막 가독성·속도·Y/Tab·M3 조건, HUD 위치·배터리 표시, 실제 랩 저장 후 같은 코스/기체/조작으로 재실행 복원, NPC 감지·수색 실기 비교, 실제 패키징과 미션 진입.
- 현재 미정: 기체별 배터리 시간, 소진 처리, 신호 대역 표기, M2→M3 스토리 분기와 반대 분기 M3 첫 대사, 레이싱 방식. Production Training과 과거 날짜별 검증은 보존하며 전체 Drone.* 재검사/새 총 성공 수를 추정하지 않는다.

- Drone Space(2026-10-02 새벽): 기존 진행상황과 다음 작업·테스트 맵과 확인 가이드·Blueprint 조정과 팀원 가이드를 갱신하고 저장 후 재조회했다. 5개 상태·NPC 감지 유지 실패 1건, 자막/배터리/Best Lap 수동 절차와 DA/BP 조정값 반영 확인. 새 Page 없음, 이번 대상 미반영 없음. Commit/Push·Unreal 쓰기·Build/PIE/패키징·Trello/Figma 수정은 하지 않았다. GitHub 링크의 이번 로컬 MD 본문은 사용자 Commit/Push 후 반영된다.

## 2026-10-01 밤 후속 — 패드 UI·실패 재출격 구현 반영

- 기준: C PC Unreal HEAD `ec2e88f` + 로컬 미커밋. 작업 도구 Claude, 문서·Space 반영 Codex. 구현 사실·검사 조건/수치는 Claude 지시서 근거이며 Codex는 HEAD와 지정 로그의 Success/기존 Fail을 읽기 전용으로 대조했다. 이번 Build·PIE·맵 생성·수동 검증은 실행하지 않았다.
- 변경 범위(Claude): 신규 `Source/Drone/UI/DroneGamepadFocus.{h,cpp}`, `Source/Drone/Mission/DroneMissionCheckpoint.{h,cpp}`, `Flow/Tests/DroneGamepadNavigationPIETest.cpp`·`DroneGamepadMissionFlowPIETest.cpp`, `Mission/Tests/DroneCheckpointRestartPIETest.cpp`·`DroneFailureResponseDataTest.cpp`. 수정은 UI 4종(FrontEndRoot·Settings·Selection·MissionResult), MissionDirector·MissionPlayerController·MissionDefinition/ObjectiveTypes/RuntimeTypes와 미션 DA 14개(`Content/Drone/Data/Missions`).
- `UI-PAD-01`: **구현됨·자동 검증 완료·수동 확인 대기**. 공통 FDroneGamepadFocus가 첫 조작 가능 위젯을 선택(새 위젯 배치까지 최대 30프레임 재시도), RenderScale 1.06·버튼 글자색으로 강조한다. 방향/A는 UE 기본, B는 기존 Back. 로비·기체 선택/복귀 선택 복원, 훈련 LB/RB 탭, 명시 방향 이동과 포커스 따라 목록 스크롤을 연결했다.
- 패드 자동 검증(C PC, Claude): RenderOffScreen 1920×1080 `Drone.Flow.GamepadNavigationPIE` **11단계 Success**, `Drone.Flow.GamepadMissionFlowPIE` **16단계 Success**, `Drone.Flow.Diagnostic.LobbyLayoutStabilityPIE` **Success·최대 0.255px**. 근거 `C:\URproject\drone\Saved\Automation\ClaudePad\render6.log`. 실제 PS4 패드·강조 가독성 Pass는 아니다.
- `MISSION-CHECKPOINT-01`: **실패 재출격 구현됨·자동 검증 완료·수동 확인 대기**. DA FailureResponse(결과 화면/체크포인트 재출격), MaxCheckpointRestarts(0=무제한). 기체 파괴·시간 초과·실패 Trigger는 같은 경로이며 맵·완료 목표·부서진 표적을 유지하고 같은 기체/조작 방식으로 마지막 체크포인트(없으면 첫 출격 위치)에서 다시 띄운다. 현재 목표 제한 시간만 다시 센다. 횟수 소진 시 기존 결과 화면.
- 체크포인트 자동 검증(NullRHI): `Drone.Mission.CheckpointRestartPIE` Success. 다른 목표용 체크포인트 무시·1회 갱신, 파괴→재출격 2회(새 기체·빙의·Director 재연결·옛 기체 제거·체크포인트 300cm 이내·방향 90°), 세 번째 파괴→실패 결과. 근거 `C:\URproject\drone\Saved\Automation\ClaudeCheckpoint\test1.log`.
- 최신 전체 회귀(NullRHI): `Drone.Mission.FailureResponseData` Success, 전체 `Drone.*` **80개 중 Success 73·실패 7**. 실패 7은 기존 NPC 개수 4·렌더 전용 진단 1·Production Training 맵 2. 패드 검사 2개는 NullRHI에서 “렌더링 필요” 경고로 건너뛰었으므로 73 Success를 패드 검증으로 확대하지 않는다. 근거 `C:\URproject\drone\Saved\Automation\ClaudeCheckpoint\full.log`; 이전 75개·15/15 기록은 당시 범위로 보존한다.
- 실패 방식 확정(Figma 기준, Claude 지시서): 재출격 = Tutorial Hover·Forward·Heading·GateFlight·Payload·FPV·UGV_NPC·UGV_Turret 8개와 Story GoldenTime(M1)·VeilBreaker(M3)·Endgame(M4). 결과 화면 = Story Intercept(M2)·Tutorial_Training·Racing_Circuit. 모두 재출격 횟수 제한 없음.
- 미구현/남은 작업: 체크포인트 Actor의 실제 맵 배치(현재 첫 출격 위치에서 재출격). M1 정보단말 픽업 지점 배치는 정보단말 회수 구현 뒤. 재출격 브리핑 재생은 MISSION-BRIEFING-02 뒤이며 재생 여부는 현재 미정(Figma M1은 “브리핑 재생 포함”, 브리핑 시스템 미구현). 스토리 충돌·레이싱 방식도 현재 미정.
- 수동 확인 대기: 실제 PS4 패드로 타이틀→훈련/탭/미션→브리핑→카드 A 선택→↑출격→결과/로비 복귀, 설정 슬라이더 A 잠금·좌우·B 복귀, 강조 가독성. 재출격 DA를 쓰는 튜토리얼에서 추락해 같은 기체/조작·현재 목표 시간 재설정·목표/표적 유지와 재출격 체감을 확인한다.
- Drone Space(2026-10-01 밤 후속): 기존 「진행상황과 다음 작업」 4개·「테스트 맵과 확인 가이드」 2개·「Blueprint 조정과 팀원 가이드」 3개 연산 저장(총 9개, 거부 없음). 저장 후 세 페이지를 재조회해 수정한 본문·표 9개 모두 기대 내용과 일치함을 확인했다. 이번 대상 미반영 없음. 새 Page·Commit/Push·Trello/Figma 수정·권한 변경·예약 자동화는 하지 않았다.

## 2026-10-01 밤 — Shotgun 시험 정정·미션 Catalog 자동 등록

- 기준: C PC Unreal HEAD `ec2e88f`(Codex 읽기 전용 Git 확인) + 미커밋 `DroneFrontEndRootWidget.{h,cpp}`, `DroneGameFlowSubsystem.cpp`, `Drone.Build.cs`, `DroneTutorialHoverPIETest.cpp`, `DroneShotgunSystemsTestMapTest.cpp`, `DroneGameFlowContractTest.cpp`, `DroneFrontEndContractTest.cpp`, `DroneFrontEndPIETest.cpp`, 새 `Flow/Tests/DroneCatalogAutoRegistrationTest.cpp`(파일 목록은 Claude 지시서). md 로컬 미커밋. 작업 도구 Claude, 문서·Space 반영 Codex.
- `AI-SHOTGUN-REGRESS-01` → **Shotgun PIE 시험 장면 수정 / 자동 검증 완료**. 사용자가 2026-10-01 실기에서 Shotgun 감지 정상을 확인했다. Claude가 자동화 실패를 실제 감지 회귀로 넓혀 쓴 잘못된 서술을 정정한다. 실패는 시험 장면의 Drone이 NPC에서 8.8m·정면 약 93° 옆(기본 시야 반각 70° 밖)에 정지하고 NPC도 대기해 5초 동안 감지되지 않은 것이었다. RenderOffScreen에서도 동일하므로 NullRHI 문제가 아니다. 사격 단계의 Drone을 NPC 정면 min(900cm, 사거리−100)·높이 150cm에 고정하는 시험만 수정했고 AI 코드는 바꾸지 않았다. 수정 후 NullRHI Shotgun 관련 5개 5/5 Success. 9/18 이후 어떤 9/22·9/29 변경이 NPC 회전에 영향을 줬는지는 미확인.
- 구현됨·자동 검증됨: `EnsureDefaultCatalog`는 C++ 기본 목록 Drone 5·Mission 14를 먼저 등록한 뒤 `/Game/Drone/Data/Drones`·`/Game/Drone/Data/Missions`의 하위 폴더까지 Asset Registry로 탐색해 미등록 Definition을 추가한다. 새 미션 DA는 지정 폴더에 만들면 C++ 수정 없이 로비에 등록된다. 잘못된 DA·ID 중복은 기존 Catalog를 유지하고 `LogDrone` 경고만 남긴다. 로비는 MissionId 알파벳순, Runtime `AssetRegistry` 의존성 추가.
- 자동 검증(2026-10-01 밤, C PC, Claude): Editor 종료 후 Build Succeeded. Flow 전체 + Mission 전체 + HoverMissionPIE + IndependentMapEntryPIE **15/15 Success**(CatalogAutoRegistration 포함). 렌더 전용 `LobbyLayoutStabilityPIE`는 이번 NullRHI 로그에서 Fail·samples=0이나 화면 표본이 없어 판정 불가이며 15/15 대상에서 제외한다. 앞선 렌더 Success와 구분한다. 미션 14·버튼 4/9/1 고정 비교는 하한 비교로 바꿨다. 새 검사는 두 폴더의 모든 Definition이 같은 Asset으로 등록됨·폴더 밖 Mission 없음·재호출 개수 유지를 확인한다.
- 근거: `Saved/Automation/ClaudeShotgunFix/test.log`, 수정 전 `ClaudeShotgunRender/render.log`(RenderOffScreen 1280×720 Fail), `ClaudeCatalog/build.log`·`test.log`. Codex가 관련 코드·성공 로그를 읽기 전용으로 대조했으며 Build·PIE를 재실행하지 않았다.
- 수동 확인 대기: 새 DA를 하나 만들어 실제 로비에 뜨는지, 1280/1920 로비 가독성. 미구현: 패키징 쿠킹 설정(`BUILD-PACKAGE-01`), 체크포인트/리스폰(`MISSION-CHECKPOINT-01`), HUB 보이스·자막/1회 시네마틱(`MISSION-BRIEFING-02`), HUD·기체별 배터리(`HUD-FIGMA-01`). → 2026-10-02 구현됨(위 최신 항목 참고). 음원·1회 시네마틱·기체별 최종 배터리 값과 실제 패키징/수동 확인은 별도 대기. Story M1~4 콘텐츠 후보는 `STORY-TEST-01`에 합쳤다. 스토리 충돌·MANPADS/베일 표기·레이싱 맵/코스 방식은 현재 미정.

- Drone Space(2026-10-01 밤): 기존 「진행상황과 다음 작업」 6개 연산(Shotgun 정정·Catalog 자동 등록·남은 카드 요약), 「Blueprint 조정과 팀원 가이드」 1개 연산(미션 연결·설정 위치 표)을 저장 후 재조회했다. 총 7개 연산 적용, 거부 없음. 두 페이지에서 기대 본문·표 일치를 확인했으며 이번 대상 미반영 없음. 나머지 페이지·기획·새 Page·공유 권한은 변경하지 않았다.

## 2026-10-01 저녁 — UI-LAYOUT-01 후속 3건 자동 검증 완료·수동 확인 대기

아래 Build·테스트·LFS·Figma 결과는 Claude 작성 작업 지시서의 C PC 결과를 Codex가 문서에 반영한 것이다. Codex는 Build·PIE·맵 생성 도구를 실행하지 않았다. Codex의 읽기 전용 Git 조회에서 HEAD `ec2e88f`와 지정 미커밋/미추적 파일 목록은 확인했다. 이전 같은 날 점검과 D PC 결과는 당시 기록으로 보존한다.

- 환경: C PC, Unreal `ec2e88f`(팀원 Yook34 Content 191파일 수신, LFS 9,039 본문 확인) + 로컬 미커밋 Source 3파일. 작업 도구 Claude.
- Build: `DroneEditor Win64 Development` 성공(우리 코드 경고 0, 엔진 헤더 C4996만).
- 전체 `Drone.*` NullRHI 75개: 성공 62 · 경고 동반 성공 4 · 실패 9.
  - 해결: `UI-LAYOUT-01` 렌더 진단 `LobbyLayoutStabilityPIE` Fail → **Success**(RenderOffScreen 1920×1080). EnterStory 0.3px, EnterTraining 13→0px, 첫 선택 36.1→0px, 이후 선택·열 이동 모두 0px. 원인 3개: 선택마다 목록 전체 재생성+AutoWrap 첫 프레임 폭 미확정 / 넘칠 때만 생기는 스크롤바 13px(9+2×2) / 선택 전 빈 메타 줄.
  - 해결: `HoverMissionPIE`는 10월 로비 개편(타이틀 [훈련]→Tutorial) 미반영 테스트였다. `OpenTrainingLobby()`로 진입하도록 고쳐 Success.
  - 기존(변경 없음): `TrainingAssets`·`TrainingPIESmoke` = 팀원 Production Training 맵 중간 상태(기존 기록과 동일, 맵 미수정).
  - 기존(변경 없음): `NPCGreyboxAssets`·`NPCGreyboxPIE`·`NPCBaseRoutinesPIE`·`NPCPerceptionSearchPIE` = 9/22 NPC 맵 증설(Rifle·Shotgun 각 3, SO 34) 뒤 고정 개수 테스트 미갱신.
  - 정정(2026-10-01 밤): `ShotgunSystemsTestMapPIE` 실패는 실기 감지 회귀가 아니라 시야 밖 시험 배치 문제였다. 사용자 실기 감지 정상 확인·시험 수정 후 5/5 Success. 상세는 위 밤 절을 따른다.
- 회귀 확인: `Flow.FrontEndPIE`·`FrontEndContract`·`MissionEntryPIE`·`BackNavigationContract`·`HoverMissionPIE` Success.
- 후속 3건(재사용 경로 줄바꿈 재적용·WBP 상시 스크롤바·기본 줄바꿈 폭 160→270) 구현됨·자동 검증 완료. 2026-10-01 19시 이후 후속 보고, C PC, 작업 도구 Claude: Editor 종료 후 DroneEditor Win64 Development Build Succeeded, RenderOffScreen 1920×1080 LobbyLayoutStabilityPIE·FrontEndPIE·FrontEndContract·MissionEntryPIE·BackNavigationContract·HoverMissionPIE 6/6 Success. 로비 단계별 최대 이동 0.255px(기준 2px). 근거 Saved/Automation/ClaudeRecheck5/build.log·render.log. 줄바꿈 270 실측: Story 4개 중 2개·Training 표본 8개 중 5개가 한 줄(높이 약 25), 나머지 긴 이름만 두 줄. 160에서는 Story 첫 버튼이 폭 146으로 두 줄이었다. 이 범위 미구현 없음.
- 협업 체계: 코드·Build·자동화 Claude / 문서·Drone Space Codex. C PC 점검 `COLLAB_READY`(FAIL 0, Claude 지시서), 공유 파일 미커밋·Git 미추적 WARN 및 Editor 실행 WARN. 다른 PC 실제 세팅은 미구현이며 SETUP 절차와 첫 docs 위임 Space 저장 확인이 남아 있다(`SYNC-COLLAB-01`). 사용자 공통 규칙 공유 원본은 Unreal .claude/codex-bridge/USER_RULES.md이며 C PC ~/.claude/CLAUDE.md에 가져오도록 설치됨(Claude 지시서: COLLAB_READY·사용자 공통 규칙 설치됨). 드론 추가 규칙은 Unreal CLAUDE.md에 반영.
- `SYNC-COLLAB-01`: 2026-10-01 저녁 후속(C PC), 협업·세팅 문서 md `docs/git/`로 이동(결정·지시 Claude, 문서 반영 Codex).
- 수동 확인 대기: 1280/1920 실제 화면 가독성, 스크롤바 상시 표시가 Story 4개 목록에서 어색하지 않은지, 다른 PC SETUP 절차.
- WORKBOARD: `UI-LAYOUT-01` → 자동 검증 완료(후속 3건 포함)·수동 확인 대기. 신규 카드 `AI-SHOTGUN-REGRESS-01`, `TEST-NPC-COUNT-01`, `FIGMA-RACING-02`(아래).

### Figma 재대조(2026-10-01, 읽기 전용) — 09-24 매트릭스 이후 새 항목
- Slide 63 "드론레이싱 계획 변경": 맵 1개+랜덤+코스 선택 → **맵 여러 개 + 맵별 코스 + 랜덤 없음 + 사용자가 직접 선택**. 현재 구현(Racing 1맵, Route 선택 `5`=무작위)과 다름.
- Slide 57/58 레이싱 UI: 골드/실버/브론즈 목표 기록, 쉐도우(이전 기록), 리플레이, 스틱 입력 오버레이, 조종 감도(Rate/스로틀 커브), 3·2·1 카운트다운, Restart/Quit. 코드에는 Countdown·Ghost·스틱 오버레이 없음.
- Slide 55 HUD: 배터리 게이지·나침반/헤딩·풍향 기호·HP·기체명·목표 현황·신호 주파수. 현재 HUD에 배터리·기체명·주파수 없음(속도/고도/수직속도/Heading/HP/Signal/Weather는 있음). Figma 드론별 "배터리 시스템(드론별 시간)"도 미구현.
- Slide 34/42/43/44: 미션별 허브(HUB) 브리핑 대사와 HUD 서브텍스트가 정리됨. `UDroneMissionDefinition`에는 DisplayName·LobbyDescription·BriefingAsset만 있어 대사/서브텍스트 필드 없음.
- 스토리 충돌(현재 미정, 임의 확정 금지): 세계관 슬라이드는 "M2 차량은 미끼, 오마르는 M3에서 사살"인데 M3 브리핑은 "오마르는 처리됐다"로 시작. M3·M4 표적도 구 슬라이드 MANPADS ↔ 신 슬라이드 방공망 '베일(VEIL)'로 표기가 갈린다. STORY-BRANCH-01 양쪽 분기 기반은 이미 있음.

## 한눈에 보기

- UI 목록 튐: 후속 3건(재사용 경로 줄바꿈 재적용·WBP 상시 스크롤바·기본 줄바꿈 폭 160→270) 구현됨·자동 검증 완료. 2026-10-01 19시 이후 후속 보고, C PC, 작업 도구 Claude: Editor 종료 후 DroneEditor Win64 Development Build Succeeded, RenderOffScreen 1920×1080 LobbyLayoutStabilityPIE·FrontEndPIE·FrontEndContract·MissionEntryPIE·BackNavigationContract·HoverMissionPIE 6/6 Success. 로비 단계별 최대 이동 0.255px(기준 2px). 근거 Saved/Automation/ClaudeRecheck5/build.log·render.log. 1280/1920 가독성·Story 상시 스크롤바 칸 수동 확인 대기. 이전 진단과 전체 75개 판정은 당시 기록으로 보존한다.
- Spaces 연동: 2026-10-01 저녁 후속 재시도로 진행상황과 다음 작업·테스트 맵과 확인 가이드·프로젝트 안내와 갱신 규칙 3개 기존 Page 저장 및 재조회 확인 완료(편집 연산 8건). UI 직전 자동 검증/후속 Build 대기·75개 판정·당시 Shotgun 회귀 서술(밤에 정정)·NPC 기대값·Figma 차이/현재 미정·로비 수동 확인·역할 분담을 반영했다. 앞선 approval_policy=never 저장 실패는 당시 기록이며 이번 대상 미반영은 없다. 19시 이후 이번 후속에서는 진행상황과 다음 작업의 UI-LAYOUT-01 후속 검증 완료(Build 성공·6/6·0.255px) 관련 3개 연산을 저장 후 재조회 확인했다. 다른 페이지는 변경하지 않았다. 기획·Blueprint 페이지는 변경하지 않았고 새 Page·권한 변경·예약 자동화는 없다. [연동 규칙과 범위](docs/git/DRONE_SPACES_SYNC.md)
- 2026-10-01 C PC 저녁 당시 기준: Unreal HEAD `ec2e88f`(origin/main 일치는 Claude 지시서 근거), Source 3파일·AGENTS.md·.gitignore 미커밋 및 CLAUDE.md·.mcp.json·.claude/ 미추적. 앞선 `9f67706`/문서 `ff69c11` Clean·0/0은 점검 시작 당시 기록이다. 기존 MD 미커밋 변경을 보존했다.
- 최신 UI: 기존 Title 이미지 6개를 유지하고 `시작 → Story 미션 4개`, `훈련 → 튜토리얼 9개 / 레이싱 1개`로 분리했다. 로비는 목록/선택 카드/설명 3열, 브리핑은 이미지/목표와 하단 시작, 기체 선택은 상단 상세·역할 도식과 하단 가로 카드다. 결과에서 복귀해도 마지막 분류를 복원한다. 실제 모델 3D Preview·최종 영상/연출은 미구현이다. [UI·원형 코스 가이드](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md)
- 설정 추가: 전체 음량 미리보기·저장, 창/테두리 없는 창/전체화면, 해상도, 그래픽 품질, VSync, FPS 제한과 적용/기본값/뒤로가기를 구현했다. 미적용 변경은 뒤로갈 때 취소하며 PIE는 창 모드·해상도를 변경하지 않는다. Master 음량은 `DroneAudioSettings` SaveGame, 그래픽은 `GameUserSettings`에 저장한다. 음악/효과음/음성 개별 SoundClass 라우팅과 실제 재실행·가청성 확인은 후속이다. Best Lap 저장과는 별개다.
- 독립 시험 구성: Tutorial 8개 수업별 맵 + Story 4개 + Racing 1개에 직접 Play용 기본 Mission Entry가 있다. Heading ID는 원형 9 Gate 완주→귀환 수업으로 사용한다. 공유 Tutorial 시험장은 보존하며 Production Training은 변경하지 않는다. Racing은 단일 코스 기록 시험이다. Best Lap JSON 영구 저장은 2026-10-02 구현·자동 검증 완료·실기 재실행 대기이며 정식 경기 규칙은 미완료다.
- 이전 D 드라이브 PC UI 검증(2026-10-01): MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공, `FrontEndContract / BackNavigationContract / MissionEntryContract / SettingsContract / FrontEndPIE` **5/5 Success**·자동화 이벤트 오류/경고 0의 문서 기록을 보존한다. 보고서 `Saved/Automation/TrainingLobbySettings/index.json`(02:03:48 UTC)과 후속 목록 튐 진단 보고서는 현재 C 드라이브 PC에 없다. NullRHI·NoSound 검사는 화면·실제 음량/해상도·재실행·패드 수동 Pass가 아니며 이번에는 재실행하지 않았다. 엔진 헤더/비선호 컴파일러 Build 경고는 별도다.
- 현재 C 드라이브 PC의 기존 보고서 확인(2026-10-01): `Saved/Automation/GameReadiness/Tests/index.json` 32 Success·실패 0, `BackNavigation/Tests/index.json` 32 Success + 경고 동반 성공 1·실패 0, `TitleLobbyOrbit/index.json` 14 Success·실패 0을 읽었다. 새 UI·설정보다 앞선 검사이므로 최신 코드의 전체 Pass로 확대하지 않는다. 기존 14맵 Map Check 0/0·Hover 3초·일부 UI 기록과 D PC의 기본 준비 0/0·32개 패키지 본문 확인은 당시 증거로 유지한다. [인계 검증 범위](docs/gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md)
- 패드 UI: UI-PAD-01 구현됨·자동 검증 완료(C PC, 2026-10-01 밤 후속, Claude). 첫 활성 위젯 포커스·방향/A/B·강조·LB/RB 탭·선택/스크롤 복원, 렌더 패드 11/16단계와 레이아웃 0.255px Success. 실제 PS4 패드 전체 흐름·강조 가독성 수동 확인 대기. [확인 범위](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#11-패드-ui-확인-범위)
- 물리·비 현황: Acro는 질량·추력·모터 응답을 반영한 게임용 근사 모델이며 실기체 교정 완료가 아니다. 비의 초기 천장 Trace 예산·맑은 날 갱신 생략·배치 갱신과 OilRig 4모드 비교 맵은 구현됐다. 다른 PC의 고정 시점 측정은 평균 원본 약 20.56ms / 비 끔 9.67ms / 근거리 원본 10.65ms / 프로젝트 비 9.65ms이며, 화질 동등·전체 맵·현재 PC 성능 결과로 해석하지 않는다.

- Bangkok City 이식: 공급 `D:\JGY\project\BangkokCity`의 실제 도시 맵 `Maps/BangkokCity`를 프로젝트 소유 `/Game/Drone/Maps/Lvl_BangkokCity`와 `/Game/Drone/ThirdParty/BangkokCity` 987개 의존 자산으로 이식했다. 본 프로젝트에서 맵 로드, 외부/누락 참조 0/0, GameMode Override 없음, Map Check 0 errors / 0 warnings를 확인했다. 약 11.46GiB의 LFS 자산과 맵은 2026-09-30 원격 `main`에 반영됐고 화면·성능 확인만 남아 있다.
- OilRig Preview 이식: 기존 Overview 기반 `/Game/Drone/Maps/Lvl_OilRig`은 보존하고 실제 장면 `Maps/Preview`를 `/Game/Drone/Maps/Lvl_OilRigPreview`로 별도 이식했다. 문 BP 32개의 외형 64개는 정적 메시로 보존하고 FirstPerson Sample 로직만 제거했다. 의존 자산 614개, 외부/누락 0/0, GameMode Override 없음, Map Check 0/0이다. 약 3.80GiB의 LFS 자산과 맵도 2026-09-30 원격 `main`에 반영됐고 화면·성능 확인만 남아 있다.
- 광섬유 GSU 적용: 공급 `GSU.fbx`가 전체 Drone이 아닌 광섬유 통임을 확인했다. 기체는 사용자 지정에 따라 DroneSpy Body·분리 Rotor 4개를 사용하고, 통은 전용 `FiberSpoolMeshComponent`에 약 28cm 높이로 하부 장착해 BaseColor·Normal·ORM·Emissive Material과 통 상단 케이블 출구를 연결했다. Editor Build 및 `ExtendedRoleDrones` 1/1 성공이며 화면 위치·크기 확인이 남아 있다.
- 접촉 카메라 교정: 사용자 확인 범위는 벽·그물만이며 총알 피격 화면 흔들림은 유지한다. 그물의 피격 Shake 호출·반복 급감속, 벽 순간 이격/Root 회전과 연속 재충격을 제거하고 외형 접촉 기울기를 FPV 카메라와 분리했다. 그물은 Pawn을 계속 막지만 Camera 채널은 기본 Ignore다. 빌드 성공, Physics 4/4·Prototype 8/8·Story 저장 계약 1/1 성공(총 13, 자동화 오류/경고 0), 관련 BP 6개 Compile 0/0. 렌더 체감은 수동 확인 대기다.
- Gate 편집: 정상 통과 음성/사운드 BP 슬롯, 하단 1/6 Spline 배치, 코스 선과 독립적인 공통/개별 Gate 스케일, 완성형 Gate Mesh 슬롯, 세 상태별 머티리얼 지정과 적용 슬롯 선택을 구현했다. 음원·최종 Mesh는 미지정이고 가청성/최종 외형 수동 확인은 남아 있다. Production Training과 Content 자산은 저장하지 않았다.
- 현재 단계: Tutorial 8개 독립 Station, Story Mission별 TestMap 4개, 별도 Racing 시험맵과 Training 4-Route 시험맵, Physics Sandbox를 유지한다. 로비 Catalog는 Tutorial 9 / Racing 1 / Story Test 4, 총 14개다. Route/Physics 시험맵은 로비가 아닌 직접 Play한다
- 조작 단계: 느림/보통/빠름 선택을 제거하고 각 기체의 기존 빠름 기준을 단일 무적재 성능으로 사용한다. FPV Rate/Acro Mode 1·Mode 2는 송신기 세로축 배치만 다르고 같은 질량·최대 추력·모터 응답·선형/제곱 항력 모델을 공유한다. Drop Drone은 내장/실제 부착 화물의 kg 질량이 총질량에 더해져 최고속도·가속·감속·Yaw·호버 추력 여유가 감소한다
- 다음 순서: UI-LAYOUT-01의 1280/1920·Story 스크롤바 칸 수동 확인과 새 DA 로비 등록 수동 확인/NPC 개수 테스트 갱신 → 패드 초기 포커스·탐색/선택 보강 → 새 UI/설정·미션 흐름 수동 확인 → Best Lap SaveGame → Tutorial 진행 UI → Story 고도화. Figma 레이싱 변경의 적용 방식과 스토리 충돌은 현재 미정이다.
- 검증 운영: 외부 OpenCode 모델 호출은 종료했다. 프로젝트 전용 Agent·모델 설정은 제거했으며 이후 구현과 검증은 Unreal 자동화와 사용자 수동 화면 확인으로 진행한다
- Unreal Editor/바이너리: 이번 최신화에서는 Build·PIE·맵 재생성을 실행하지 않았다. 다른 PC에서 받은 소스만으로 로컬 바이너리 최신화를 보장하지 않으므로 실제 구현/플레이 점검을 시작할 때 별도 확인한다.
- Production Training: 팀원이 실제 Tutorial 환경을 제작 중이므로 열람 외 저장·덮어쓰기·자동 재구성 금지
- 작업컴 인계: [시작 가이드](WORK_PC_START_HERE.md)와 기본 점검 도구 준비 완료. 오늘은 Build/Validate 옵션 없이 실행해 Git·LFS·필수 Tutorial 자산·Engine/Plugin 설정을 확인했다. 기본 준비 통과와 런타임 재검증 완료를 구분한다

## Git 기준

| 저장소 | 현재 기준 | 상태 |
|---|---|---|
| Unreal 현재 PC `C:\URproject\drone` | HEAD `ec2e88f` (origin/main 일치는 Claude 지시서 근거) | 밤 HEAD는 Codex 읽기 전용 Git 확인. 최신 미커밋 UI·Flow·Build.cs·테스트 목록은 위 밤 절의 Claude 지시서 기준. 저녁 Source 3파일과 기존 Clean은 앞선 점검 시점 |
| 문서 현재 PC `C:\Users\jkw11\Documents\Codex\2026-08-19\codex-gpt-chatgpt-codex-1-6` | 점검 시작 `main = origin/main = ff69c11` | 실제 원격 main 대조·점검 시작 Clean/0/0. 이번 최신화 MD는 로컬 미커밋 |

2026-10-01 앞선 C 드라이브 PC 점검에서 두 저장소의 `git ls-remote origin refs/heads/main`과 `HEAD...origin/main = 0/0`을 확인했다. 이전 D 드라이브 PC의 `83b33c1`/`aecb6ec` 수신·09:34:51 KST Pull과 후속 미커밋 기록은 당시 상태이며 지금의 기준이 아니다. 현재 PC에 `D:\JGY\project\drone`/`md` 경로는 없다. 상세 Worklog의 과거 기록은 보존하며 이번 MD 공유의 Commit·Push는 사용자가 수행한다. 외부 모델 검증은 종료했고 프로젝트 저장소에 OpenCode 인증/설정을 남기지 않는다.

## 최신 완료 항목

- 2026-09-30 `D:\JGY\project\BangkokCity` 원본을 수정하지 않고 일회용 UE 5.8 스테이징에서 `Maps/BangkokCity`를 `/Game/Drone/Maps/Lvl_BangkokCity`로 복제했다. 실제 의존성 987개를 `/Game/Drone/ThirdParty/BangkokCity`로 이동하고 Redirector 참조를 재저장했다. 본 프로젝트 감사 결과 Map load 성공, dependency closure 988, 외부 `/Game` 0, 누락 0, `default_game_mode=None`, Map Check 0/0이다. `Overview`는 자산 전시 맵이라 이식하지 않았다.
- `/Game/Drone/Maps/Lvl_OilRig`은 공급 `Overview` 기반 기존 맵으로 보존했다. 실제 환경 `Preview`는 별도 `/Game/Drone/Maps/Lvl_OilRigPreview`와 `/Game/Drone/ThirdParty/OilRigPreview` 614개 자산으로 이식했다. 본 프로젝트 감사 결과 dependency closure 615, 외부/누락 0/0, `default_game_mode=None`, Map Check 0/0이다. 빈 Mesh Actor 14개와 완전 중복 1개만 정리했으며 문/문틀 64개 외형은 보존했다.
- 2026-09-30 `/Game/Drone/ThirdParty/FiberOpticGSU`에 공급 GSU Mesh·Material·Texture 4개를 이식했다. `BP_DroneFiberOpticIntegration`은 DroneSpy Body·분리 Rotor 4개와 회전을 사용하고 재밍 면역·충돌 자폭·케이블 로직은 유지하며 GSU를 전용 통 Component에 장착했다. 통 상단이 Spline 시작점이며 재생성 도구도 동일 설정으로 갱신했다. MSVC 14.51.36257 Editor Build와 `Drone.Integration.ExtendedRoleDrones` 1/1이 오류·경고 없이 성공했다.
- 2026-09-30 벽/그물 접촉 화면 교정 최종: MSVC 14.51.36257 `DroneEditor Win64 Development` 성공. `Drone.Physics` 4/4(`ContactSmoothing`, `ContactSmoothingBlueprint` 추가), `Drone.Prototype` 8/8(기존 `DamageShake` 그대로 통과), `Drone.Mission.StoryPhysicsTestMaps` 1/1 Success. 관련 BP 6개 메모리 Compile 오류·경고 0. 보고서 `drone/Saved/Automation/ContactCameraIsolation/index.json`(2026-09-30 03:26:32 UTC). 기존 엔진 헤더의 Deprecated API/비선호 MSVC 경고는 Build에 남아 있으며 신규 프로젝트 컴파일 오류는 없다. 패키지/맵 저장·Commit·Push 없음.
- 접촉 회귀는 순간 이격/Root 회전·그물의 피해 Shake 호출을 Red로 재현한 뒤 Green을 확인했다. 지속 접촉 12회에서 새 충격 중복 없음, 접촉 해제 뒤 재충격 허용, Camera 채널만 Ignore/Pawn Block 유지, FPV 접촉 회전 차단과 실제 피해 Camera Shake 유지, 저장 Pawn BP의 새 Camera Pivot 상속을 검사한다.
- Gate 최종 검증: MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `TrainingCourse`, `TrainingGateBlueprint`, `TrainingGatePresentation`, `TrainingGateSequence`, `TrainingLapRecorder`, `TrainingRouteSelector`, `TrainingRouteSelectionTestMap`, `TrainingRouteSelectionPIE` 8/8 Success(자동화 이벤트 오류·경고 0). 실제 Gate/Course BP 메모리 Compile도 각각 0 errors / 0 warnings다. 보고서: `drone/Saved/Automation/GatePresentation/index.json` (2026-09-30 02:42:54 UTC). 패키지 저장·Production Training 변경 없음.
- 2026-09-30 Gate 통과음은 Sequence가 정방향·순서를 승인한 뒤에만 재생한다. `GatePassSound`는 음성 SoundWave/SoundCue를 받고 볼륨·피치·2D/공간 재생을 BP에서 조절한다. `OnGatePassed` 이벤트는 자막/연출 확장용이며 같은 소리를 BP에서 중복 재생하지 않는다.
- 자동 Gate는 `AutomaticGateSplineHeightFraction=1/6`을 기본으로 하고, `AutomaticGateScale × AutomaticGateScales[Index]`로 Visual/Trigger만 조절한다. 이전 중심 배치 Child도 BeginPlay 때 파괴/재생성 없이 최신 위치로 갱신한다. 수동 Gate와 Course Spline 제어점·선 폭/두께는 변경하지 않는다.
- Gate Visual에 전체 메시용 `GateAssetMesh`/로컬 Transform과 상태 적용 슬롯 배열을 추가했다. 기존 16개 Component 이름은 보존하며 전체 메시가 있을 때 네 임시 Frame만 숨긴다. 상태별 `InactiveMaterial/CurrentMaterial/CompletedMaterial` 지정 슬롯을 추가했고 비어 있는 상태는 `RingMaterial`로 fallback한다. 선택하지 않은 슬롯은 Mesh 원본 Material을 보존한다.
- 2026-09-30 기체 선택 화면의 느림/보통/빠름 버튼을 폐기했다. 기존 `EDroneHandlingPreset`·함수·WBP 이름은 직렬화 호환용으로만 남고 모든 요청을 `Balanced` 단일 기준으로 정규화한다. 무적재 최고속도는 각 Definition의 기존 Base Speed × `UnloadedMaximumSpeedMultiplier=1.25`를 사용하므로 기존 빠름 수준을 유지한다
- `FDronePhysicalFlightSettings`를 Flight Profile에 추가해 Dry Mass, 합산 최대 추력, 모터 응답 시간, 제곱 항력, 적재 시 속도 하한을 Data Asset/Blueprint에서 조정할 수 있다. Mode 1/2는 이 Struct와 Acro Rate 설정을 그대로 공유하며 입력 축 배치만 다르다
- Carryable Payload에 `PayloadMassKilograms`를 노출했다. 기본 내장 화물은 `DronePayloadDropComponent > DefaultInventoryPayloadMassKilograms`, 맵 배치 화물은 Payload BP/인스턴스의 질량을 사용한다. 적재/투하와 운반 중 질량 변경 직후 비행 수치가 즉시 재계산된다
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `Drone.Prototype` 8/8, `Drone.Physics` 2/2, `Drone.Flow` 5/5가 Success다. Mode 1/2의 실제 패드 축, 무적재 고속 체감, Drop 적재 전후 가속·호버 차이는 렌더 화면 수동 확인이 남았다

- 2026-09-30 `UDroneCollisionResponseComponent`를 시험 Pawn 전용에서 일반 비행 `ADronePrototypePawn` 공통 규칙으로 전환했다. 후속 교정에서 `120cm/s` 미만 무반응, 고정 `90cm/s` Kick, 고정 `6cm` 순간 이격을 제거했다. 저속 접촉부터 반발 속도·분리 거리·자세 Kick이 연속 비례하고, 직전 비행속도를 보존해 이동 Component가 충돌 직후 속도를 줄여도 반발이 사라지지 않는다. 바닥·천장과 Ground UGV는 제외한다
- Collision Root 밖 네 모서리 기본 `±95cm` Wing/Rotor Probe가 벽과 그물을 Sphere Sweep한다. Probe Offset·Radius·Trace Channel, 최대 회전 Kick·기준 속도·Lever Arm과 모든 반발 수치는 Pawn Blueprint의 `CollisionResponseComponent`에서 조정할 수 있다
- 그물은 일반 Drone 충돌에서 기본적으로 절단되지 않는다. `ADroneNetPlacementRig`가 `UFloatingPawnMovement` 실제 속도를 읽어 `UDroneCollisionResponseComponent`에 전달하고, 속도·반복 접촉에 따라 감속·조종/추력 저하·자세 교란·하강을 누적하며 임계값 이상은 포획 상태로 올린다. 현재 기본 자동 해제는 4초 계열 시험값이고 모든 수치는 Pawn/Net Blueprint Component Defaults에서 조절 가능하다
- 폭발·탄환 Point Damage에 의한 국소 절단과 떨어지는 Segment 진단 기능은 유지한다. Drone 충돌 절단은 `Break On Impact`를 명시적으로 켤 때만 동작한다
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. 속도 비례 Red→Green을 포함한 `Drone.Physics` 2/2, 변경 영향 `Drone.Prototype` 8/8, `Drone.Mission.StoryPhysicsTestMaps` 1/1이 Success다. 실제 렌더 화면에서 저속 밀림·고속 반발·날개 끝 회전 방향, 그물 포획 체감·자동 해제 후 조작 복구는 수동 확인이 남았다

- 2026-09-29 `/Game/Drone/Maps/TestMap/Lvl_DroneTrainingRouteSelectionTest`에 직선·좌곡선·우곡선·상승 슬라럼 Course 4개와 Route Selector를 추가했다. `1~4`는 고정 선택, `5`는 현재 Route를 제외한 무작위 선택이며 전환 시 이전 Gate/Lap을 초기화하고 HUD 기록 Source도 활성 Course로 바꾼다
- Route 맵 Map Check 0/0, `Drone.Tutorial.TrainingRouteSelector`, `TrainingRouteSelectionTestMap`, 실제 입력 `TrainingRouteSelectionPIE`, 기존 `TrainingCourse`, `TrainingGateSequence`, `TrainingLapRecorder`가 모두 Success다
- 2026-09-29 `/Game/Drone/Maps/TestMap/Lvl_DronePhysicsSandbox`와 Story Mission별 `Lvl_DroneStory01_GoldenTimeTest`, `02_InterceptTest`, `03_VeilBreakerTest`, `04_EndgameTest`를 생성했다. 5개 맵 모두 Map Check `0 errors / 0 warnings`다
- Physics Sandbox에 기존 Drone에는 영향을 주지 않는 시험용 벽 충돌 반발 Component와 전용 Pawn/GameMode를 추가했다. Hit Normal 기준 반사·최소 분리 속도·반발 계수·최대 속도는 Blueprint 조절값이며 정면/비스듬한 반사 계산 자동화가 통과했다
- 첫 화면 확인에서 그물 약 13×12m와 벽 약 12.8×9.2m가 시험 Drone 대비 지나치게 컸고, Drone의 `OnActorHit`가 반발만 처리하고 맞은 Actor에 Point Damage를 전달하지 않아 그물·벽이 실제 충돌로 깨지지 않는 결함을 확인했다. 그물 기본값을 6×3m, 파괴 벽을 약 5.55×3.69m로 축소하고 최소 충돌 속도를 2.5m/s로 낮췄으며, 충돌 위치·방향을 그대로 Point Damage로 전달하도록 수정했다
- `BP_DroneNetPlacementRig`는 네 Corner, 가로/세로 줄 수, 분할 수, 중심 처짐, 줄 굵기, 충돌, 파괴 반경·최소 속도를 Blueprint에서 조정한다. 충돌/Point Damage 위치 주변 Segment를 원본 격자에서 제거하고 최대 16개를 중력·충격량이 적용된 물리 조각으로 5초간 떨어뜨리며 Reset에서 격자와 파편을 함께 복구한다
- `BP_DroneBreakableWallPanel`은 온전한 벽을 ISM 격자로 유지하고 맞은 반경의 조각만 물리 Component로 바꾼다. Columns·Rows·조각 크기·간격·반경·Impulse·최소 속도를 Blueprint에서 조정한다
- `Dataflow`, `GeometryCollectionPlugin`, `ChaosClothAsset`, Editor 전용 `ChaosClothAssetEditorCore`를 프로젝트에 명시 활성화했다. 실제 Chaos Cloth/Geometry Collection 생산 자산은 아직 0개다
- 최종 Physics 의도에 맞춰 C++ 게임 규칙을 구현했다. 그물 감속·추력 저하·자세 교란·포획/하강, 일반 Flight Pawn의 벽·기둥·구조물 속도 비례 반발, Wing/Rotor Probe v1은 구현됐고, 실제 Chaos Cloth 변형·탈출 입력 판정·강한 Crash/Damage 우선순위·얇은 벽 CCD는 후속이다
- Story Test Mission 4개를 로비 Catalog에 추가했다. M1은 Drop 전달→귀환, M2는 Spline 차량 핵심 표적 파괴와 목적지 도착 실패, M3는 광섬유 Drone 재밍 구역 이탈→귀환, M4는 UGV 지휘 표적 3개 파괴→귀환을 시험한다
- `Drone.Tutorial.HoverMissionPIE`를 추가해 FrontEnd 선택부터 Scout Spawn, Hover Zone 진입, 안정 자세 3초 유지와 `ReturnToBase` 목표 전환까지 실제 PIE로 검증했다. 결과는 Success이며 Tutorial TestMap의 보이지 않던 Hover Box에는 충돌 없는 모서리 표식 4개를 추가했다
- 2026-09-29 최종 회귀에서 `Drone.Physics.Breakables`, `Drone.Physics.CollisionResponse` 2/2와 `Drone.Mission.StoryPhysicsTestMaps` 1/1이 오류·경고 없이 Success다. `Drone.Tutorial.MissionLessonsTestMap`, `Drone.Flow.Contract`, `Drone.Flow.FrontEndContract`, `Drone.Flow.FrontEndPIE`의 기존 성공 기준도 유지한다. FrontEnd는 등록 Mission 13개와 버튼 13개를 확인했다

- 2026-09-29 `Lvl_DroneTutorialMissionTest`를 8개 수업 Station으로 확장했다. `DA_Mission_Tutorial_Forward/Heading/GateFlight/UGV_NPC/UGV_Turret`을 추가하고 로비 Catalog는 기존 Training 포함 9개 Mission을 노출한다
- `ADroneTutorialHeadingZone`의 방향 정렬 기능은 별도 시험/참조 호환용으로 보존했다. 현재 회전 수업에는 사용하지 않고 원형 Course의 `TrainingLap`을 사용한다
- `UDroneGroundWeaponComponent`와 `ADronePlayerProjectile`을 추가했다. GroundWeapons Capability에서만 활성화하고 상부 Muzzle 기준 좌클릭 총 25 피해·우클릭 유탄 100 반경 피해를 사용한다
- Tutorial 시험맵 Rebuild/Validate Map Check `0 errors / 0 warnings`, Build 성공, 새 Mission 집중 회귀 9/9 성공. 전체 `Drone.*`는 51개 성공과 기존 기준선 실패 7개이며 실패는 NPC 맵 고정 Actor 수, Shotgun PIE 감지, 보호 중 Production Training 코스 기대값이다
- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialMissionTest`에 Hover/Forward/Orbit/Gate/FPV/Payload/UGV NPC/UGV Turret Station과 Return Zone을 배치했다. 2026-10-01 기존 Owned Heading 두 Actor만 원형 Course로 교체하고 수동 Hover/기타 배치를 보존했다. Map Check 오류·경고 0
- Tutorial 독립 Mission Definition 8개는 각 수업에 맞는 목표 순서와 허용 기체 한 종류를 가진다
- `Hover Maintained` Mission Event와 `BP_TutorialHoverZone`을 추가했다. 기본 3초·75cm/s·수직 40cm/s·15°이며 Overlap 중 0.1초 Timer만 사용하고 Blueprint 조정 가능하다
- Game Flow 기본 Catalog를 기존 Training과 Tutorial 독립 Mission 8개, 총 9개로 확장하고 C++ fallback 로비가 등록된 Mission 버튼을 모두 생성하도록 바꿨다
- `/Game/Drone/Mission/Blueprints`에 Mission Manager·PlayerController·GameMode, 목표/실패/귀환 Trigger, 체력 100 Damage Target, Hover/Heading Zone 등 재사용 Blueprint를 생성했다. Manager는 출격 시 Controller가 자동 생성하므로 맵에 수동 배치하지 않는다
- 공용 `DroneMissionTrigger`는 Active Player Drone/Actor Tag/Any Actor 정책, 목표 Event/실패 Action, 일회 실행과 명시 호출을 지원한다. `DroneMissionDamageTarget`은 표준 Damage·Health·파괴 연출 Event를 제공하고 Mission 중 동적 Spawn 대상도 Director에 등록한다
- `/Game/Drone/AI/Animation`에 적 Rifle과 Friendly Unarmed용 프로젝트 전용 Idle/Walk/Run AnimBP·BlendSpace를 저장하고 Hostile Rifle/Shotgun·Friendly BP에 연결했다

- Weather Manager에 `Enable Rain`, 자동 강우 Visual 생성 Class를 추가했다. 비 Off는 바람/Profile ID를 유지하고 Rain Snapshot 표현값만 0으로 만들며 Blueprint에서 런타임 전환 가능하다
- `/Game/Drone/Weather/Blueprints/BP_DroneRainVisual`과 `/Game/Drone/Weather/Materials/M_DroneRainStreak_OilRigMask` 추가. OilRig 원본 `T_rain_Mask`를 참조하는 최대 112개 짧은 Plane 빗줄기(기본 65×2.4cm, 불투명도 0.22)를 재사용한다. 구형 파란 DrawDebug 선은 기본 Off/0개다. 카메라 위쪽 Trace·0.35초 실내 보간과 빗줄기별 WorldStatic/WorldDynamic 표면 Trace로 지붕·지면 아래 표시를 막으며 맵 전체 Weather Snapshot은 바꾸지 않는다
- `/Game/Drone/Integrations/RoleDrones/BP_DroneFiberOpticIntegration`과 `DA_Drone_FiberOptic_Greybox`는 DroneSpy Body·분리 Rotor 4개 Visual, `JammingImmunity + ImpactDetonation`, 1인칭 기본 시점을 사용한다. `FiberSpoolMeshComponent`에는 공급 GSU 통을 약 28cm 높이로 하부 장착했고 통 상단 출구부터 지나온 지면까지 Spline과 Cylinder Spline Mesh가 이어진다. 마지막 지면점→통 구간은 기본 내부점 4개·포물선 처짐·이웃점 Hermite Tangent로 자연스럽게 휜다
- `/Game/Drone/Integrations/RoleDrones/BP_DroneGroundUGVIntegration`과 `DA_Drone_GroundUGV_Greybox`는 GC Drone 1 Poseable Mesh를 참조한다. `W/S` 전후·`A/D` 조향·`Q/E` 제자리 회전은 하부 차체를 움직이지만 마우스/패드 시점은 `Turret` Yaw와 `Turret_Swivel` Pitch만 움직여 차체를 돌리지 않는다. Camera와 총·유탄 Muzzle Anchor도 같은 상부 Yaw/Pitch Pivot을 따른다. 고도 입력 차단, 네 지점 지면 높이/Pitch/Roll 추종, 바람 Drift 비활성화와 최초 10,000cm 지면 획득은 유지한다. 좌클릭 직사 총탄과 우클릭 중력 유탄 발사·피해 기능이 연결됐으며 정식 무기 Mesh는 아직 미정이다
- Tutorial Mission과 GameFlow/선택 UI를 기존 3종에서 Scout/FPV/Drop/Fiber/Ground 5종으로 확장했다. 외부 공급 Skeleton은 수정하지 않고 Integration BP가 Visual만 참조한다

- `/Game/Drone/AI/Blueprints/BP_DroneNPCAIController_Outdoor` 추가. Hostile Rifle/Shotgun에 Sight 60m, Lose Sight 70m, Smart Object 검색 반경 80m·높이 10m, 직전 지점 회피 15m를 적용하고 Blueprint Class Defaults에서 조정 가능하게 했다
- `/Game/Drone/Vehicles/Blueprints/BP_DroneVehicleSplineRoute`와 차량 Spline Follow v1 추가. Vehicle Instance에서 Route 참조·On/Off·속도·끝 반전/Loop를 조정하며 XY/Yaw는 Spline, Z/Pitch/Roll은 기존 4점 지면 Trace가 담당한다
- `/Game/Drone/Weather/Blueprints/BP_DroneRandomWeatherController` 추가. 8방향+무풍, 방향 8~18초·세기 5~12초·1~9m/s 시작값과 보간값을 BP에서 조정한다. 에디터에서는 원뿔 표식이 보이고 Play/Package에서는 제거되며 Actor/표식 Collision·Overlap·Navigation 영향은 없다
- 바람 UI를 `E/NE/N/NW/W/SW/S/SE/CALM`과 m/s로 통일하고 Flight HUD에 `풍향 … | 풍속 … m/s`를 추가했다

- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest` 경량 시험 맵 생성
- 곡선 Course, CourseSpline과 분리된 Ring Handle 5개, Gate/Sequence 5개 구성
- Recon·Impact·Payload 역할 표적 각 1개와 Carryable 1개 배치
- Gate의 임시 16각 Cube Ring을 Box Trigger 안쪽과 맞는 4변 발광 Frame으로 교체
- Gate `통과 전 / 현재 목표 / 통과 후` 3상태 색상 계약 유지
- 깨지는 역할 표적·Carryable World Text를 기본 숨김 처리하고 선택 표시 문구를 짧게 정리
- 유인 MG 사수 사망 뒤 재할당 재시도, 이동 정체 감시, 재경로와 Greybox 도착 Snap 보강
- 병사 전투 상태에 공통 `Minimum Response State Duration=1.0초`를 추가했다. MG·Cover 이동/사용 태스크가 한 프레임 실패해도 유지시간 동안 현재 예약·감지·사격 행동을 다시 점검하고, 시간이 지난 뒤에도 실패일 때만 다음 상태로 넘어간다. 사망·드론 파괴·Sight Lost 확정 정리는 지연하지 않는다
- 개인화기는 실제 3D 무기 사거리 안이면 즉시 정지·사격하고, 사거리 밖 판정이 기본 0.2초 지속될 때 추적을 시작한다. 사거리 밖에서는 NavMesh에 투영한 표적을 추적하며 전투 시작점 기준 기본 3,000cm 리시 또는 기본 2.5초 무진행 한계를 넘으면 표적을 포기하고 순찰로 복귀한다. 같은 투영 목적지는 기본 150cm 이상 바뀔 때만 갱신한다
- 개인화기 Pursue는 Drone 자체를 큰 허용 반경으로 쫓지 않고 `PersonalWeaponPursuitRangeRatio`로 계산한 지상 사거리 정지점을 작은 `PersonalWeaponPursuitDestinationAcceptanceRadius`로 추적한다. Pursue 동안에는 Controller 한 곳이 그 안정된 최종 목표를 향해 몸 Yaw를 보간하고 Bone Gaze도 같은 목표를 사용한다. `bUseAccelerationForPersonalWeaponPursuitMoves=false`가 기본이라 짧은 경로점을 가속으로 지나쳐 공전하지 않으며, 이 설정은 Pursue에만 적용되어 일반 순찰의 가속 이동은 유지된다. 리시 포기 후 StateTree 재시작은 다음 Tick으로 예약해 `StartTree` 재진입을 막는다. 사거리 비율·도착 반경·Pursue 가속 사용 여부·회전속도·리시·재경로 거리/주기·무진행·Cooldown 값은 Controller Blueprint에서 조정 가능하다
- Smart Object 동선·배치 팀 가이드, LFS 용량 계획, 외부 도구 검토와 추천도서 학습 계획 작성
- Truck Spline Route v1은 차량 참조·속도·Reverse/Loop·목적지 Event와 4점 지면 추종을 구현했다. Story Intercept 시험맵은 차량의 목적지 도착을 실패 조건으로 사용한다. Smart Object 최근접 Slot 동선과 구분하며 제작 맵의 최종 동선·난이도는 수동 조정 대상이다
- Smart Object Greybox 차량의 실제 `SM_SpikeStorm_Tire2_FR`이 Cylinder 가정의 Mesh 로컬 Z축으로 회전해 옆으로 빙글도는 결함을 재현하고, Mesh 장착 회전과 무관한 차량 부모 공간 `+Y` 차축 회전으로 교정. 축은 Blueprint `Wheel Visual Spin Axis In Vehicle Space`에서 조정 가능
- 같은 실제 Tire의 약 50cm 시각 반지름에 `Wheel Radius=30cm`를 사용해 바닥 아래로 약 20cm 잠기던 결함을 독립 평면에서 재현. 차량 BP 기본값을 52cm로 올리고 Blueprint 허용 범위를 1~500cm로 확장, Tire Bounds·지면 접촉 Red→Green과 맵 Validate 통과
- Mission Definition에 순서형 목표 Rule(사건 종류·필요 수량·선택적 제한 시간·Actor Tag 대상 ID) 추가. 기존 문구형 목표는 fallback 유지
- Director에 Scan·의도된 Payload 적중·Health 대상 사망 Event, 목표별 시간 만료 실패, Actor 중복 방지와 Snapshot/HUD 진행값 연결
- Blueprint 배치형 `DroneMissionReturnZone`을 추가해 플레이어 Drone Overlap을 귀환 Event로 보고하도록 준비
- 저장 `DA_Mission_Tutorial_Training`의 기존 한 Lap 목표를 `Training Lap` Rule로 이행. 팀원 Training Map은 미수정
- 배치형 `DroneJammingVolume`과 Pawn의 `DroneSignalComponent` 추가. 겹치는 방해 Source 중 최대 강도로 단계·신호율 계산, 강한 단계에서 기본 비행 튜닝값의 속도·가속도 배율 적용/복원
- Flight HUD 신호율·단계 경고, Blueprint 영상 노이즈 강도 Event 추가. 실제 화면 Noise Material·목표 정보 숨김은 미구현
- Director에 `Jamming Exited`, `Jammer Disabled` Rule Event 연결. 자동화 Editor World에서 BP Delegate 구독이 진행되지 않아 게임 규칙 연결은 C++ Event로 분리하고 BP Delegate는 연출용으로 유지
- Figma `Project:Droner`를 읽기 전용으로 확인해 Tutorial + 4개 Story Mission, 역할 Drone과 UI 흐름을 현재 코드에 대조. 원본은 미수정
- 2026-09-24 Figma Tutorial 상세를 읽기 전용으로 재확인했다. `310:3`/`318:20`/`353:2` 기준 8개 수업, 단계별 브리핑·클리어 타임, 전체 완료 UI, Warehouse 환경 메모를 확인했다. 당시 공용 Mission 시험 맵은 3개 수업만 있었고, 2026-09-29에 8개 독립 Station으로 확장했다
- 2026-09-28 `DRONE_TUTORIAL_IMPLEMENTATION_TEST_GUIDE.md`로 구현·검증 계약을 먼저 고정했고, 2026-09-29 전진·회전·Gate·UGV 총/유탄·NPC/포탑 처치까지 구현 상태로 갱신했다
- Mission 성공이 남기는 `StoryFactsGrantedOnSuccess/RemovedOnSuccess`와 목표의 `Always/FactPresent/FactAbsent` 조건 추가. 미끼 차량→Mission 3 표적 처리와 실제 탑승 차량→Mission 3 처리 생략을 모두 데이터로 선택 가능
- `JammingImmunity`가 실제 구현 Capability인 Drone만 활성 Zone의 재밍 영향을 무시하도록 Signal/Pawn 연결. 기존 세 Drone에는 면역을 임의 부여하지 않음
- `Lvl_NPCSmartObjectGreybox`를 Unreal AssetTools로 `/Game/Drone/Maps/TestMap` 아래 이동하고 코드·생성 도구의 고정 경로 갱신
- `/Game/Drone/Maps/TestMap/Lvl_DroneMissionSystemsTest` 생성. 35%/80% 겹침 Jammer, Return Zone, 역할 표적 3종, Carryable과 위치 표식 배치
- `/Game/Drone/Maps/TestMap/Lvl_DroneShotgunSystemsTest` 생성. 기존 AI 맵을 바꾸지 않고 추가 Hostile Shotgun NPC 1명, 약 9m 시작 거리, 5/10/15m 표식과 LOS 차단벽 배치
- 기본 Projectile Shotgun에서도 Cyan 예상 비행선 8개를 표시하고 Blueprint에서 표시 On/Off와 직전 Pellet 끝점 배열을 조회할 수 있게 보강
- Shotgun은 실제 8 Projectile·12° 독립 확산, Pellet당 3 피해를 사용한다. 같은 발사자의 Projectile끼리 Sweep 충돌을 무시해 같은 총구에서 생성된 Pellet이 서로 제거되지 않으며, Cyan 예상선은 기본 Off다. 전용 BP에는 주황 Emissive `0.04` 비드와 `0.20 × 0.0125` Tracer가 적용돼 있다
- Rifle·유인 MG·무인 포탑의 공용 Projectile 기본 외형을 주황 Emissive 탄두 `0.06`과 Tracer `0.60 × 0.018`로 확대했다. Shotgun 전용 BP Scale은 유지한다
- Shotgun/Rifle 개인화기 몸 Yaw를 `3° 정지 / 6° 시작` Hysteresis로 바꾸고 Bone Gaze는 작은 잔여 오차를 계속 보간한다. 경계 Snap 없이 몸과 고개의 왕복을 억제하며 정지각·Hysteresis·기본 `180°/s` 몸 회전속도는 BP Profile에서 역할별 조정 가능하다
- 첨부 와이어프레임을 기준으로 C++ 임시 Front-end를 `작전 목록 / 선택 작전 / 작전 개요`, 기체 선택을 `보유 기체 / 상세 / 조작 설정` 3열 레이아웃으로 갱신했다. Flow와 Data Asset은 기존 계약을 재사용하며 최종 WBP Designer·Thumbnail/영상은 아직 별도 작업이다
- 세 번째 `FPV Rate/Acro` 조작 모드 추가. Pitch/Roll/Yaw를 Body 각속도로 해석하고 Stick 중앙에서 자동 수평 복귀하지 않아 Roll/Loop 가능
- Rate/Acro의 공용 Action 재해석을 제거하고 전용 Axis1D Action 4개를 추가했다. 키보드는 `W/S Pitch`, `A/D Roll`, `Q/E Yaw`, `Space/Ctrl Throttle`, Gamepad는 기존 Mode 2를 유지해 W/S와 고도 입력 중복 및 키보드 Pitch 누락을 해소했다
- FPV Rate/Acro를 송신기 Mode 1과 Mode 2로 분리했다. 키보드는 두 모드 모두 같은 의미축을 유지하고, Gamepad는 Mode 1 `Left Y=Pitch/Right Y=Throttle`, Mode 2 `Left Y=Throttle/Right Y=Pitch`를 사용한다. 기존 `AcroRateRealisticGreybox` 열거형 이름은 저장 Asset 호환을 위해 Mode 2 의미로 유지했다
- 과거 `안정/균형/고기동`→`느림/보통/빠름` UI 단계는 2026-09-30 폐기했다. 저장 호환을 위해 내부 Stable/Balanced/Agile 이름만 유지하며 런타임에서는 모두 단일 `Balanced` 기준과 기체별 Physical Flight Settings를 사용한다
- `Lvl_NPCSmartObjectGreybox` 실제 실행 로그에서 Rifle이 Shotgun의 `Gun` 컴포넌트에 걸려 `stuck`되는 정확한 충돌 상대를 확인했다. NPC Character는 Capsule 외 모든 Primitive를 Collision/Overlap/Nav 비활성 VisualOnly로 복구하며, 자동화가 각 런타임 컴포넌트를 검사한다
- 순찰 중 몸이 50~100cm 단위의 Nav 즉시 경로점을 따라 원을 그리지 않도록 Patrol 몸 방향은 예약된 최종 Smart Object 슬롯을 기준으로 유지한다. 3초/100cm 전에 300° 이상 누적 회전하면 실패하는 실제 맵 회귀를 추가했다
- 초기 FPV 참고값은 수평 27m/s·수직 9m/s·Pitch/Roll 650°/s·Yaw 400°/s였다. 이후 단일 고속·질량/추력 변경이 적용됐으므로 27m/s는 현재 고정 기준이 아니다. 현재 FPV DA 수평 Base 4,500cm/s × 무적재 배율 1.25 = 56.25m/s이며 실제 적용값은 Definition/Profile/Pawn BP Override와 적재 상태를 함께 확인한다
- Rate/Acro에 중력, 중립 호버, 기체 Up 방향 추력, 속도 비례 항력, Body Rate 응답 시간을 연결했다. `Space/Ctrl`은 호버 기준 추력 증감이고 W/S Pitch로 기울인 Up 축이 실제 전후 추진력을 만든다. 호버 스로틀·중력·항력·Rate 응답은 FPV Data Asset/Blueprint에서 조정 가능하다
- `UDroneWeatherProfile`, `FDroneWeatherSnapshot`, `UDroneWeatherWorldSubsystem`, 배치형 `ADroneWeatherController` 구현. Profile 기본 10Hz로 결정적 지속풍·돌풍·전환값을 공급
- 모든 Prototype Drone에 `UDroneWeatherResponseComponent`를 부착. 쉬운 조작 65%·제한 자세 25%·Rate/Acro 0% 기본 보정과 Sweep Drift 적용. 최종 물리가 아닌 `UFloatingPawnMovement` Greybox
- `/Game/Drone/Data/Weather`에 `Clear`, `LightWind`, `RainStorm_Greybox` Profile 3종 생성
- `/Game/Drone/Maps/TestMap/Lvl_DroneWeatherSystemsTest` 생성. LightWind Controller 1개·35° 풍향 화살표·Prototype GameMode, Map Check 0/0
- Weather TestMap에 `/Game/Drone/Weather/Blueprints/BP_DroneWeatherDebugVisualizer`를 배치했다. 24개 흐름 Bead, 현재 Profile/풍속/풍향/조작 모드 화면 표시와 `1 Easy / 2 Manual / 3 Acro Mode 1 / 4 Acro Mode 2` 비교 키를 제공한다
- 돌풍에 Attack/Release/풍향 응답 시간을 분리하고 최단각 풍향 보간을 적용했다. Debug Bead는 표시 속도를 부드럽게 따라간 뒤 벡터 적분하므로 풍향 변경 때 과거 누적 거리를 새 방향으로 재투영하지 않으며, 풍속에 따라 방향과 길이가 바뀐다
- OilRig Mask 기반 Camera-follow Plane 강우 Greybox, 실내 지붕 감쇠와 표면 아래 Streak 차단은 구현됐다. 정식 Niagara GPU Rain, MPC Wetness, Splash·Audio, 품질 단계와 GPU 측정은 아직 미구현

## 검증된 근거

- 2026-09-24 Tutorial Mission 추가 뒤 `DroneEditor Win64 Development` Build 성공. Test Map Rebuild/Validate와 Map Check `0 errors / 0 warnings`
- `Drone.Tutorial.MissionLessonsTestMap`, `Drone.Mission.FrameworkAssets`, `Drone.Mission.ObjectiveRules`, `Drone.Flow.Contract`, `Drone.Flow.FrontEndContract`, `Drone.Flow.FrontEndPIE` 최종 `6/6 Success`, 오류·경고 0
- 2026-09-24 MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. Mission Blueprint 7개 생성/컴파일/저장 검증과 적 Rifle·아군 Unarmed Idle/Walk/Run 자산 생성/검증 성공
- `Drone.Mission.FrameworkAssets`, `Drone.Mission.ObjectiveRules`, `Drone.Mission.MissionSystemsTestMap` 최종 `3/3 Success`. 기존 `Drone.AI.NPCGreyboxAssets`는 AnimBP 연결 검사를 지난 뒤 Smart Object 맵의 낡은 정확한 Actor 수 기대값과 Ground Vehicle Auto Drive 설정에서 실패했으며 새 애니메이션 자산 생성 실패는 아니다
- 2026-09-23 MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. 광섬유/UGV 변경 뒤 증분 Build도 성공
- FPV 동일 본체·Rotor 4개, 광섬유 다점 곡선/Tangent, UGV Poseable Mesh의 `Turret`·`Turret_Swivel`, 차체 불변 상부 조준, 총·유탄 Anchor를 검사하는 `Drone.Integration.ExtendedRoleDrones` `1/1`과 `Drone.Integration.FPVAsset` `1/1` 성공
- 변경 뒤 `Drone.Prototype + Drone.Flow` 전체 회귀 `13/13 Success`, 실패 0. `MissionEntryPIE`의 인터넷 연결 확인 요청 시간초과만 경고 1건이며 게임 로직 오류는 아니다
- 기존 기준선 `Drone.Weather` `4/4`, 5종 Catalog를 검사하는 `Drone.Flow.Contract` `1/1`, 5종 선택 UI의 `Drone.Flow.FrontEndContract`·`FrontEndPIE` 각 `1/1` Success·실패 0
- Weather 생성 도구 Validate와 Map Check `0 errors / 0 warnings`. Production `Lvl_DroneTraining`은 열거나 저장하지 않았다
- 사용자가 Random Weather 화면 확인과 차량 Spline Route 시험 맵 제작·화면 확인을 완료했다고 보고했다
- 2026-09-22 MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공
- Random Weather TestMap 재생성 및 Map Check `0 errors / 0 warnings`, Production Training 수정 0
- `SmartObjectFoundationDefaults`, `FlightHUDBlueprintAsset`, `FlightHUDTelemetryBinding`, `GroundConformingSuspension`, `ProfileAndWindContract`, `SystemsTestMap` 최종 `6/6 Success`, 경고·실패 0

- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공
- TestMap Map Check `0 errors / 0 warnings`
- `Drone.Tutorial.TrainingGateSequence` 1/1 성공
- `Drone.Tutorial.TutorialSystemsTestMap` 1/1 성공
- `Drone.AI.NPCPerceptionSearchPIE` 단독 새 PIE 3회 성공
- 상태 안정화 계약 추가 전 Reflection 자동화가 새 설정 누락으로 Red가 된 뒤, 구현 후 `SmartObjectFoundationDefaults`, `HostilePatrolStateTreeAsset`, `GroundConformingSuspension`이 Success로 전환했고 최종 Editor Build도 성공했다
- 이전 9월 15일 작업 종료 시 Unreal·문서 `git diff --check`, Unreal `git lfs fsck` 통과. 9월 16일 기능 변경의 최종 검사 결과는 아래에 따로 기록
- 이 PC에서 최신 Source로 `DroneEditor Win64 Development` 재빌드 성공
- TestMap Validate/Map Check `0 errors / 0 warnings`, rings=5/targets=3/carryable=1
- 최종 단독 Commandline 회귀: `Drone.Mission.ObjectiveRules`, `Drone.Flow.Contract`, `Drone.Flow.MissionEntryContract`, `Drone.Tutorial.TrainingGateSequence`, `Drone.Tutorial.TutorialSystemsTestMap` 5/5 성공
- 2026-09-16 `DroneEditor Win64 Development` 전체 재빌드 성공. 양쪽 Story 분기와 재밍 면역을 포함한 Flow/Mission/Prototype/Signal/Tutorial/UI 회귀 8/8 Success·Exit 0
- 시험 맵 이동/추가 후 `DroneEditor Win64 Development` 재빌드 성공, Mission Systems Map Check `0 errors / 0 warnings`
- 이동된 AI 맵 Asset·PIE·감지/수색, 새 Mission Systems 맵, Mission Rule, Signal Stage 최종 회귀 6/6 Success·경고 0
- 자동포탑/지면 추종 차량 배치 도구를 새 AI 맵 경로에서 Validate-only 실행해 설치형 1·차량형 1·Attach·4점 Suspension·노면 5개 확인
- Shotgun Systems 맵 Map Check `0 errors / 0 warnings`; 발광 Material/실제 Pellet BP·정면 시선 안정화 포함 전용 Asset/PIE 자동화 `2/2 Success`
- Shotgun 가시성 변경 전 자동화가 피해 8·Tracer 없음·큰 탄두를 의도대로 실패한 뒤, 변경 후 전용 Asset/PIE `2/2`와 `NPCGreyboxAssets`, `WeaponContract`, `ProjectileBallistics`, `ShotgunTrace` 집중 회귀가 모두 성공
- 전체 샷건 묶음 `WeaponContract`, `ShotgunTrace`, `ProjectileBallistics`, 전용 Map/PIE `5/5 Success`, 실패 0. 기존 두 단위 테스트의 Recast 경고만 존재하며 샷건 기능 실패는 아님
- 3° 시선/최소 상태 유지 구현 직후 `NPCPerceptionSearchPIE`에서 재점유 제한시간 실패가 재현됐던 이력은 보존한다. 2026-09-17 추적·테스트 격리와 StateTree 재진입 수정 뒤 같은 테스트가 감지→MG 경합→개인화기 대체→사수 사망 후 재점유→Lost/Search→순찰 복귀까지 `1/1 Success`로 전환됐다
- 2026-09-17 후속 화면 피드백으로 `사거리 안인데도 계속 접근`과 추적 중 몸·고개가 이동과 반대로 도는 Red를 재현했다. 최종 규칙은 실제 무기와 같은 3D 사거리 안이면 즉시 정지·사격, 밖 판정이 0.2초 지속될 때만 Pursue다. Bone Gaze는 수평 이동을 따르고, Pursue 몸 Yaw는 Character Movement가 단독 소유한다. 역할 BP가 덮은 이동 회전 플래그도 BeginPlay에서 공통 계약으로 복구한다. Editor Build와 `PersonalWeaponEngagementPolicy`, `SmartObjectFoundationDefaults`, 경계 흔들림·이동/시선 정렬·사거리 진입 정지를 포함한 `ShotgunSystemsTestMapPIE`, `NPCPerceptionSearchPIE`, `NPCGreyboxAssets` 최종 `5/5 Success`
- 2026-09-18 MSVC 14.51.36257 `DroneEditor Win64 Development` 최종 링크 Build 성공. `PersonalWeaponEngagementPolicy`, `PersonalWeaponMaintenanceTiming`, `ShotgunSystemsTestMapPIE`, `NPCGreyboxAssets`, `NPCPerceptionSearchPIE` 5개가 모두 `Success`, 실패 0이다. Maintenance 단위 테스트의 Skeletal Mesh 미지정 경고 7건은 예상 경고다
- 실제 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`의 `NPCBaseRoutinesPIE`를 `-TestLoops=4`로 반복해 4/4 Success, 오류·경고 0을 확인했다. 각 실행은 Rifle/Shotgun 순찰 2회·서로 다른 슬롯 방문과 0.35초 초과 역방향 몸/속도 불일치를 함께 검증한다
- 사용자 실제 화면에서 Rifle/Shotgun 이동과 회전 수정이 정상임을 확인했다. 저빈도 `[NPC-STATE]`·`[NPC-MOVE]` 진단은 Blueprint에서 다시 켤 수 있게 유지하되 기본값은 Off로 전환했다
- 개인화기 Controller에 Blueprint 조절형 `PersonalWeaponInitialAimDelaySeconds=1.0`을 추가했다. 최초 Sight 성공 시각부터 계산하므로 DroneDetected/Pursue/Cover 상태 왕복이 시간을 초기화하지 않으며, 지연 중 행동을 정상 유지해 StateTree 실패로 처리하지 않는다. 다른 Drone으로 표적이 바뀌면 이전 사격을 먼저 정리한다
- Figma `Project:Droner` Page 1의 최상위 148개 항목을 읽기 전용으로 재확인했다. 최신 기준은 Slide 52~53의 타이틀→미션 선택/설명→로비→드론 선택→인게임 흐름, Slide 55의 공중 Drone 공통 HUD, Slide 57~58의 Racing UI/Restart/Quit/기록·감도·리플레이 요구다. Figma 원본은 수정하지 않았다
- `BP_DroneTrainingCourse`의 CourseSpline 점 추가는 UE 5.8 기본 Visualizer가 이미 지원함을 엔진 소스와 프로젝트 구현으로 확인했다. 기존 점 선택 뒤 `Alt+이동 기즈모 드래그` 또는 선분 우클릭 `Add Spline Point Here`를 사용하며 Ring별 Spline Handle과 구분한다. 별도 코드·맵 변경은 하지 않았다
- 2026-09-18 후속 화면 보고의 Shotgun 전신 회전을 전용 교전 PIE에서 `PursueDrone` 상태의 같은 방향 누적 몸 Yaw `301~304°`로 반복 재현했다. 진단 결과 Nav 가속과 RVO는 이미 꺼져 있었지만 `bRequestedMoveUseAcceleration`은 켜져 있었고, Drone 위치에 큰 도착 반경을 둔 MoveTo가 가까운 경로 Segment를 가속으로 지나치며 몸과 시선이 짧은 코너를 계속 쫓았다. 실제 사거리 정지점·75cm 도착 반경·Pursue 전용 직접 요청 속도·몸/시선 공통 최종 목표로 수정했다. 전용 테스트에는 같은 상태에서 연속 300° 초과 회전 실패 조건, 실제 맵에는 정지 회전과 역방향 보행 실패 조건을 추가했다. 중간에 요청 가속을 전 상태에서 끄자 순찰 역방향 `0.614초`가 회귀로 잡혀 Pursue에만 한정했다. 최종 Editor Build, 완전 새 Editor 프로세스 Shotgun 3/3, 실제 Smart Object 맵 3/3과 관련 5개 테스트가 모두 성공했다. `PersonalWeaponMaintenanceTiming`의 Skeletal Mesh 없는 최소 시험 Actor 경고 7건은 예상 경고다
- 2026-09-18 실제 사용자 PIE 로그에서 `BP_NPC_Hostile_Rifle_C_0 is stuck`의 충돌 상대가 `BP_NPC_Hostile_Shotgun_C_0 Component:Gun`임을 확인했다. 런타임에 해당 `Gun`이 `collision=3 overlap=1 nav=1`인 것도 자동 계측으로 재현했고, Capsule 외 Primitive를 VisualOnly로 강제한 뒤 `NPCBaseRoutinesPIE`, `NPCGreyboxPIE`, `ShotgunSystemsTestMapPIE`가 모두 Success이며 `stuck` 로그가 없다
- 2026-09-18 첫 사격 조준 지연 추가 뒤 MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `SmartObjectFoundationDefaults`, `ShotgunSystemsTestMap`, `ShotgunSystemsTestMapPIE`, `NPCGreyboxPIE`가 Success다. Shotgun PIE는 조준 지연 완료 전 Fire Event 0과 감지 관측 시점부터 첫 Volley까지 1초 이상을 함께 검사한다
- FPV Mode 1/2 변경 후 입력 Asset 생성 로그 `mappings=33`, MSVC 14.51.36257 Editor Build 성공, `AcroInputContract`, `FlightProfiles`, 수정된 3회 `PIEInputLifecycle`, `MissionEntryPIE`가 Success다. 첫 lifecycle 실행은 새 두 Action을 기존 예상 목록에서 누락해 `31/33` Red, 두 번째는 release-binding 분류 누락으로 Red였고 테스트 계약을 고친 뒤 3/3 Green으로 전환했다
- 최종 검증 뒤 `fetch --prune`에서 팀원 `9a94f06 260918` Content 커밋을 확인했다. 변경 1,412개는 Source·Config·Plugins를 건드리지 않고 현재 AI 소스와 Shotgun/Smart Object 시험 맵에도 겹치지 않지만, `Lvl_DroneTraining`과 `Lvl_DroneTutorialSystemsTest`를 포함해 자동 Pull은 보류했다
- 기존 Smart Object 맵의 NPC 수·역할이 유지되는지 `Drone.AI.NPCGreyboxAssets`를 별도 재실행해 `1/1 Success`, 경고 0 확인
- FPV Rate/Acro 추가 후 `DroneEditor Win64 Development` Build 성공. `Drone.Prototype.FlightProfiles`, `Drone.Prototype.PIEInputLifecycle`, `Drone.Flow.MissionEntryContract`, `Drone.Flow.MissionEntryPIE`, `Drone.Prototype.RoleAbilities` 5/5 Success·Exit 0
- 기상 Runtime 추가 후 `DroneEditor Win64 Development` Build 성공. `Drone.Weather.ProfileAndWindContract`, `Drone.Weather.ProfileAssets`, `Drone.Weather.SystemsTestMap` 3/3 Success·Exit 0
- Weather TestMap Python 저장 검증과 Map Check `0 errors / 0 warnings`, `Drone.Prototype.PawnDefaults` 회귀 Success·Exit 0
- Weather 시각화 추가 전 저장 계약이 Visualizer `0개`로 의도대로 실패한 뒤, BP Visualizer 1개·Bead 24개·화면 Readout·모드 키 계약의 `Drone.Weather.SystemsTestMap` 성공
- Acro 입력 계약은 전용 Action 4개가 없는 기존 상태에서 의도한 Red를 확인한 뒤, IMC 33 Mapping·BP 연결과 Pawn 전용 분기로 Green 전환했다. MSVC 14.51.36257 Editor Build 및 `Drone.Prototype` 8/8 Success
- Acro 추력 연결 전 `Nose-down Acro attitude creates forward thrust`가 의도대로 실패한 뒤 중력·호버·추력·항력·Rate 응답 구현으로 Green 전환했다. 최종 Editor Build, `Drone.Prototype` 8/8 Success·실패 0
- WTH-02B 벡터 적분·돌풍 응답 구현 뒤 `Drone.Weather` 3/3 Success·실패 0. 방향 변경 시 이전 X 이동을 보존한 채 Y 이동이 누적되고, 고정 속도 적분은 Frame Step과 무관함을 자동화했다
- `962ff02`와 대응 문서 Push 전 Unreal·문서 `git diff --check` 모두 종료 코드 0. LF→CRLF 메시지는 줄바꿈 안내이며 공백 오류가 아니다

## 아직 확인하지 않은 항목

- `BP_DroneRainVisual`이 RainStorm에서 파란 선 없이 짧고 부드러운 Mask 빗방울로 보이는지, Clear/비 Off에서 사라지는지, 지붕 아래에서 침투하지 않고 기본 0.35초 보간으로 줄며 밖에서 복원되는지 화면 확인
- 광섬유 Drone의 DroneSpy Body·분리 Rotor 4개 배치와 회전, 1인칭·ImpactDetonation·재밍 면역, 장착된 GSU 통의 위치·크기와 통 상단에서 시작하는 케이블 지면 누적·곡률이 자연스러운지 화면 확인. Ground UGV는 높은 시작점에서 지면으로 내려와 W/S/A/D/Q/E와 4점 경사 추종을 유지하고, 마우스/패드 시점에서 차체는 고정된 채 상부 `Turret`/`Turret_Swivel`만 올바른 축으로 도는지 확인

- TestMap Gate Frame 외형과 Trigger 정합, 3상태 색
- Ring Handle 개별 이동과 Spline 투영 체감
- 한 Lap HUD 갱신과 두 Lap 이전 평균·Best·증감값
- 역할 표적 3종, Carryable 픽업·드랍과 숨긴 World Text
- 이동된 AI 시험 맵의 MG 재점유·도착 방향·Gaze·자동포탑·차량 화면 확인
- Rifle/Shotgun 병사가 사거리 밖에서 Drone을 자연스럽게 추적하고, Shotgun이 가까운 경로 코너에서 전신 회전·도리도리하지 않으며, 사거리 안에서 정지·사격하고 리시 밖에서는 포기·순찰 복귀하는지 화면 확인
- 병사 감지 후 최소 1초 안에 Cover/MG/개인화기 상태가 프레임 단위로 왕복하지 않고 현재 행동을 유지하는지 화면 확인
- Drone Rotor 축·방향·속도, 비행 기울기, 실제 탄환 피격 흔들림 등 기존 수동 회귀
- 새 TestMap의 귀환 Zone 위치/크기와 재밍 Zone Overlap·신호 경고·강한 단계 이동 체감 수동 확인
- Shotgun Systems 맵의 발광 Pellet 8개와 짧은 Tracer 분리 가시성, Cyan 선이 보이지 않는지, 이동 회피 체감, 최대 24 피해, 16m 사거리·LOS와 Hysteresis 고개 안정화 화면 확인
- `Lvl_DroneFrontEnd`의 새 3열 Mission UI와 Training 진입 뒤 3열 Drone 선택 UI가 해상도에서 잘리지 않는지 수동 확인
- FPV Rate/Acro에서 키보드 `W/S Pitch`, `A/D Roll`, `Q/E Yaw`, `Space/Ctrl Throttle` 중복 없음과 Gamepad/RC Mode 1·2, Stick 중앙 자세 유지, Roll/Loop와 현재 DA/BP의 단일 고속·적재 전후 체감 수동 확인
- 현재 Rate/Acro v2는 Dry Mass+Payload Mass, 합산 최대 추력, 총질량 호버점, 모터 응답, 기체 Up 추진, 선형/제곱 항력과 Body Rate 응답을 계산한다. 다만 `UFloatingPawnMovement` 기반 게임용 모델이며 모터별 RPM·PID·관성 텐서·프로펠러 공력 기반 완전 물리와 같다고 판정하지 않는다
- Camera-follow Instanced Mesh 강우와 카메라 위쪽 Trace 기반 실내 감쇠는 구현했으나 화면 확인 전이다. 정식 Niagara GPU Rain, 젖음 MPC, Splash·Audio, 품질 단계와 Low~Epic GPU 측정은 미구현
- Test Mission DA/진입 경로에서 Return/Jammer Mission Event, 역할 Event 연쇄, 제한 시간 만료 화면 확인
- 영상 노이즈 WBP 연출과 목표 정보 손실 표현 확인
- `골든 타임/인터셉트/베일 브레이커/엔드게임` Story DA와 독립 TestMap 4개는 구현됐다. 제작용 맵·선택 목표·기체 교대·장거리 타격·연출의 완성은 별도이며 각 시험맵 전체 수동 완주는 남아 있다
- 같은 Figma 파일에서 Mission 2 차량이 미끼라는 전체 설명과 탑승 차량으로 전제한 개별 화면, Mission 3에서 오마르를 처리하는 설명과 이미 처리됐다는 대사가 충돌함. 코드는 양쪽을 지원하며 저장 기본안은 사용자 결정 대기
- 광섬유 Drone·UGV의 프로젝트 소유 Definition/Integration Pawn과 차량 목적지 도착 실패는 구현했다. 두 외형의 스케일·조작 화면 확인은 남아 있고 Mission 중 기체 교대·장거리 타격 Drone·최종 Cinematic 연결은 미구현이다

## 알려진 실패와 경계

- `TrainingAssets`, `TrainingPIESmoke` 실패는 팀원이 제작 중인 실제 Training 맵의 Gate/Sequence와 역할 Actor 중간 상태를 보여준다. Codex가 원본 맵을 수정해 억지로 통과시키지 않는다.
- `NPCBaseRoutinesPIE`는 수정 전 4회 중 3회 실패했지만 최종 Source에서 4/4 성공했다. 묶음 회귀에서 잡힌 성공 완료 동일 부분 경로 재요청도 차단했고, Shotgun 전용 PIE와 전체 관련 묶음 모두 Green이다. 화면상의 애니메이션 체감은 사용자 수동 확인 전까지 별도 미확인으로 유지한다.
- 유인 NPC 점유 포탑은 `BP_SO_MGTurret` 한 개다. `BP_AutoTurret_Vehicle`, `BP_AutoTurret_Emplaced`는 무인 자동포탑이다.
- 모든 `.uasset`, `.umap`은 크기와 무관하게 Git LFS 대상이다. Threshold 방식으로 일반 Git에 옮기지 않는다.
- 이 PC의 첫 TestMap Validate 실패는 9월 8일 생성 DLL이 9월 15일 Source보다 오래되어 역할 표적 BP의 C++ 부모를 못 읽은 문제였다. 최신 Editor Build 후 같은 비파괴 Validate가 성공했고 맵 Actor 삭제/재구성은 하지 않았다.

다음 행동과 완료 조건은 [`WORKBOARD.md`](WORKBOARD.md), 상세 문서 위치는 [`docs/README.md`](docs/README.md), 과거 근거는 [`docs/history/DRONE_WORKLOG.md`](docs/history/DRONE_WORKLOG.md)를 따른다.
