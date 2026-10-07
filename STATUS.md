# 현재 작업 상태

기준일: 2026-10-07 KST D PC. InterLink DX 축·버튼·ArmSwitch·노브 전용 메뉴 이동은 Claude 구현·자동 검증됨, Codex 문서 반영. 실측 Mode 2·반전 해제 확인, 실기 비행/메뉴 체감 수동 대기. Unreal cb77c0d·MD 6558cca 기준+미커밋. 기존 C PC 검증은 별도 인계 근거이며 Commit/Push 미실행.

## Git 기준

| 저장소 | 현재 기준 | 상태 |
|---|---|---|
| Unreal 원격 `gyeonliz/drone` | 로컬 origin/main `0c0ed99` | 최신 읽기 기준. C PC 작업 트리 상태는 이 PC에서 확인 불가 |
| Unreal D PC `D:\JGY\project\drone` | HEAD `0c0ed99` = origin/main, tracked20·untracked6 | 기존 변경 보존·이번 UI/화물/결과창 수정 추가. Training 맵391MB 미저장, 앞서 포인터였던 Payload BP·미션 DA5개는 본문 확인. 전체 자산/패키징 준비 완료와는 구분. 수신·검증 경위 WORKLOG, Commit/Push는 사용자 |
| 문서 원격 `gyeonliz/md` | origin/main `c5a0524` (10/06 09:05 C PC Push) | 10/04~10/06 Codex 정리·아카이브 포함 |
| 문서 D PC `D:\JGY\project\md` | HEAD `c5a0524` + 로컬 미커밋 | 10/06 D PC Claude: 250e975→c5a0524 fast-forward. 미커밋은 이번 변경(STATUS·WORKBOARD·WORKLOG·CLAUDE.md·아카이브). 10/02 D PC 진단 원문은 stash@{0} 보존·WORKLOG 재반영. Commit/Push는 사용자 |

현재 D PC는 10/06 CodexGripPose 집중 자동화 6/6 Success와 Editor Build 성공을 확인했다. nullrhi 검사이므로 수동 화면 Pass가 아니며 이전 LobbyLayoutDiagnosticWrapProbe Fail·C PC 전체 검증과 분리한다. 원격 Bangkok 잔여987개 삭제는 과거 LFS 저장량/요금 감소와 다르다. 로그·수신/잠금·Zen 경위는 [WORKLOG](docs/history/DRONE_WORKLOG.md) 참조.

## 한눈에 보기

현재 우선 확인: `쉬운 조작 / 게임 조작 / FPV 모드 1 / FPV 모드 2` 한 줄 표시·폭 보정과 초기/재픽업 공통 집게 자세 구현·자동 검증됨. 수동 화면/실제 패드·화물 파지 외형은 대기. BP 조정은 Drop Pawn의 `PayloadCarryAnchor`, 화물의 `PayloadVisual`; 절차는 [역할 가이드](docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md), 이력은 [WORKLOG](docs/history/DRONE_WORKLOG.md).

`UI-RESULT-LAYOUT-01` 구현·자동 검증됨/수동 대기: 기본 결과창을 중앙 폭680·내용 높이 카드, 여백32/28·청록 버튼·행간12로 수정. 다시하기/로비로 복귀를 짧게 표시하며 다음 미션명·진행/전체 완료 계약은 유지. 결과창만 배율1 고정·색/테두리 강조(옛 BP1.06도 돌출 안 함), 다른 UI 배율은 유지. 12:43 KST ResultLayout·SelectionLayout·Entry·TutorialNext/Complete·GamepadFlow 6/6 Success; native/named fixture의720p/1080p 배치와 실제 NativeTick 검사이며 화면/실물 패드 Pass는 아님. [UI 가이드](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md)·WORKLOG 참조.

10/06 C PC Claude: D-5 출발부터 랩 타이머 측정·D-12 Flight 명명과 피격/Acro/지상 주행 컴포넌트 분리 구현됨·자동 검증됨. 화면·FPV/UGV 체감 수동 확인 대기. 기존 NPC/높이 제한/매니저·Legacy 정리 유지, D-13 종료. 코스4개 지형·배터리 시간·높이 제한 수치/경고 연출 현재 미정. 세션 전문은 [WORKLOG](docs/history/DRONE_WORKLOG.md).

| 영역 | 구현·자동 검증 | 수동 확인 대기·미구현·현재 미정 |
|---|---|---|
| 시작·로비 | 스토리/레이싱/튜토리얼/설정/종료 5메뉴, 분류 직접 진입, 상하 순환·Back/포커스 복원, 저장 `WBP_DroneFiveItemMenu` 연결 | 실제 패드·1280/1920 배치 확인 대기. 로비 Tutorial/Racing 탭·LB/RB는 현재 유지, 최종 유지 여부 미정 |
| 조종 입력 표시 | 설정 수동 ON/OFF·선택 저장, 저장 `WBP_DroneControlInputDisplay` 연결. 아래 중앙 스틱 표시·OFF 갱신 중지, 고도계 독립 | D-3 기본 False 확정, 장치 자동 전환/분리·재연결 정책 미정. 실제 화면/패드 확인 대기 |
| 코스 표시선 | 긴 코스만 sqrt(곡률) 밀도+15% 균일 몫, 짧은 TestMap68/113조각 기존 균일 분할 유지. MaximumCourseLineSegments 노출·기본1024(시작값·미확정), BP 드래그 재구성 Off | 팀원 Production 코스 외형·Editor 편집 체감 수동 대기. Production 맵 미저장 |
| Acro | InterLink DX Acro 4축 추가·Mode 2 실측·세로축 반전 해제(10/07 D PC Claude), [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md). 비행 기체 FPV/Scout/Drop/FiberOptic 6개 입력 연결, 패드 축 4개 Dead Zone, 정확 자세 적분. 키보드·패드 입력원 분리·절댓값 큰 쪽 사용·키 해제 시 패드 인계, Space 단독 자세 불변·Mode 1/2 키보드 동일·FPS 무관 자동 검증 | 실제 패드/키보드 체감·Scout/Drop 비행 대기. 키보드 각속도 배율·Angle 모드·마우스 Yaw·회의 “좌우 스틱 반전” 뜻 미정 |
| 패드 첫 포커스 | `FDroneGamepadFocus`가 포커스 부여 후 5프레임 감시·루트/없음으로 이탈 시 복원, 다른 강조 버튼 이동은 보존 | UI-FOCUS-RACE-01 **수정 후 확인 중**. 화면 그려진 수정 전 Fail/후 Success 각 1회, 간헐적 첫 버튼 강조 수동 확인 대기 |
| 튜토리얼·Story 순서 | 독립 Tutorial 8수업·Story 4·Racing 1, 로비 Tutorial 9/Racing 1/Story 4. 호버→전진→회전→게이트→자폭→드랍→UGV NPC→포탑. 시간·다음·n/8·전체 완료·로비 완료 표시 | 실제 8수업 연속 완주/S48·S49·로비 확인 대기. 완료 영구 저장 미정(D-4 수업1~8 유지·회의4는 레이싱 코스4개); 조작키 브리핑 미입력 |
| Best Lap | `CourseId|DroneId|ControlMode`별 JSON 저장/복원·없음/구버전/손상 처리·HUD, HandlingPreset 제외. 평균은 실행 History | 같은 조건 실제 랩 후 재실행 복원 확인 대기. D-5 레이싱 시작/완주/결과 시간 구현, 코스4개 지형 미정 |
| 허브·HUD | Story 허브 브리핑·Voice 슬롯·기체명/신호 대역/배터리 HUD. D-6 미션 DA BatteryLimitSeconds(0=기체 값)·BatteryDepletedResponse(기본 추락), 동력 상실→조종 정지→중력 낙하→접촉 또는8초 뒤 파괴→기존 실패/재출격 구현됨·자동 검증됨(10/05 C PC Claude) | 풍향 HUD/배터리 가독성 수동 확인 대기. 기체 DA 시간 모두0·시간 값 현재 미정, 확정 전 실제 게임 동작 변화 없음·확정 뒤 추락 체감 확인. 음원/튜토리얼 대사·신호 대역·분기/재출격 브리핑 미정 |
| 미션·실패 | DA 자동 등록·Definition/Rule/Trigger·체크포인트 재출격 유지. D-6 높이 제한 매니저 구현됨·자동 검증됨(10/05 C PC Claude): `/Game/Drone/Managers/BP_DroneAltitudeLimitManager` 배치·BP 값 설정으로 적용. Mission/Weather 매니저 BP도 같은 폴더로 정리됨. 상세 [WORKLOG](docs/history/DRONE_WORKLOG.md) | 높이 제한 체감·날씨 시험 맵 수동 확인 대기, 높이 제한 수치·경고 연출 현재 미정. 체크포인트 미배치·첫 출격 위치 재출격. 추락 체감·새 DA 등록 및 Story M1~4 콘텐츠/분기 고도화 확인 |
| 레이싱 | D-5 구현됨·자동 검증됨(10/06 C PC Claude). 3·2·1 동안 조종 잠금·기체 정지·타이머 숨김/미측정, 출발부터 0초 측정·화면 위 가운데 `00:00.00`. 첫 게이트에서 재시작하지 않고 첫 구간으로 이어짐. 기존 목록·제품1~5 차단·게이트 완주 유지 | 카운트다운·랩 타이머 화면 수동 확인 대기. 현재 레이싱1개; 코스4개 미구현·지형 현재 미정 |
| 물리·역할 | 질량·추력·모터 응답·선형/제곱 항력·Drop kg 하중, Mode 1/2 공통. 속도 단계 제거. 벽/날개 접촉·그물 포획 Greybox·접촉 카메라 분리, 피해 Shake 유지 | Acro는 게임용 근사 모델, 실기체 교정 미완료. 수동 속도/하중/접촉·실제 Chaos 비교 필요 |
| AI·차량·날씨 | AI-LOCOMOTION-01 다리 고정 후속 구현됨·자동 검증됨(10/05 C PC Claude): 아군 Retargeter Pin Bone·적 발 IK Control Rig 제거. 양손 총 파지·hand_r 부착 유지. 원인·보폭 검증은 [WORKLOG](docs/history/DRONE_WORKLOG.md). StateTree Soft 참조/AlwaysCook·Rifle/MG 디버그 기본 Off 유지. 차량·바람/비·천장 차단, D-6 HUD 방위 통일·불어오는 쪽 풍향 구현됨·자동 검증됨. 비 품질 구현됨·자동 검증됨(10/07 C PC Claude, HEAD `cb77c0d`·스테이징): 전 단계 원본 Niagara1개·판 빗줄기 기본0. Weather 전체·SettingsContract Success. [비 가이드](docs/gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md#비-품질-설정과-조정)·[실측/정정](docs/history/DRONE_WORKLOG.md#2026-10-07--비-연출-도입비-품질-옵션-c-pc-claude) | NPC 걷기 다리·속도 대비 보폭/발 미끄러짐·손/총 정렬·사격/재장전 수동 확인 대기. 적 경사면 발 맞춤 없음·Pin 뒤 IK 뼈 잔존 원인 미특정. 최종 애니메이션/산탄총 전용 동작 미정·미구현. 감지 PIE KnownIssues Fail 유지, 풍향 HUD·날씨 시험 맵 수동 확인 대기. 비 입자 크기/모양·위치/양·젖음/물결·음원/실내 감쇠·설정 패드 수동 대기. 단계 최종값/음원 확정 현재 미정; 화면 물방울/바닥 Splash 미구현 |
| 환경·기체 | D-12 2·3차 구현됨·자동 검증됨(10/06 C PC Claude): Flight 클래스/소스 경로로 변경·ClassRedirects 3개, 피격/Acro/지상 주행 컴포넌트 분리. BP 이름·자산 경로 유지. Legacy 1차·Characters 변환 원본 유지, D-13 종료. 상세 [WORKLOG](docs/history/DRONE_WORKLOG.md) | FPV 곡예·UGV 주행 분리 전 동일 체감 수동 확인 대기. 방콕 삭제 커밋/푸시 상태 별도 확인. 사람 최종 아트·애니메이션·음원 보존 |
| 패키징 | Asset Manager DroneMission/DroneDefinition AlwaysCook·MissionMap 참조, StateTrees 폴더 DirectoriesToAlwaysCook·StateTreeCookContract 자동 검증 | 실제 패키징/패키지 맵 진입 미실행 |

## Acro 회의 조사·수정 — ACRO-MEETING-01

- **10/04 사용자 보고 Mode1 Space 하강/뒤집힘**: 키보드와 패드 세로축 Action이 한 변수를 나중 값으로 덮는 원인을 재현했다. Space+오른쪽 -0.5→스로틀 -0.38, W+왼쪽 -0.5→피치 -0.38(Mode2도 같은 구조). 키보드·패드 입력원을 분리하고 절댓값이 큰 쪽을 사용하도록 수정. 키를 누르면 키보드가 이기고 떼면 패드가 조종한다. Space 단독 자세 불변 검사는 패드 혼합 입력 결함이 없다는 근거가 아니었다. 실제 패드 체감은 수동 대기.
- **Mode 1/2**: 키보드 키/결과 동일, 패드 세로축만 RC 표준에 따라 다름. Mode 2 LeftY=Throttle·RightY=Pitch, Mode 1 LeftY=Pitch·RightY=Throttle. 회의 “좌우 스틱 반전”이 이 배치인지 축 부호 등 다른 문제인지 **현재 미정**.
- **결함 1, 패드+키보드 동시 입력**: Enhanced Input은 DefaultInput.ini 축 데드존을 사용하지 않음. Acro 패드 매핑에 Dead Zone이 없어 0.05 쏠림이 키보드 스로틀을 덮고 손을 떼도 각속도가 누적됐다. IMC 4개 축 매핑 맨 앞에 쉬운 조작 패드 매핑 값을 그대로 복사(Lower 0.2·Upper 1.0·Radial). 새 수치 결정 아님, 기본 매핑 33개·키/Action/순서 유지(현재 InterLink 축8+버튼4 추가·총45).
- IMC 수정 담당 구분: Codex MCP는 Instanced Modifier 하위 객체 생성 실패(None)로 **저장 없이 원상복구**. Claude가 Editor 종료 후 headless Unreal Python으로 IMC만 패치·저장·재조회(`ClaudeAcro/patch_dz.log`).
- **결함 2, Scout/Drop Acro 입력 누락**: 두 BP의 Acro 입력 6개가 None이었다. Codex ui run `20261004-001325-ui-ui-acro-input-assets`에서 FPV와 같은 6개 Action을 Class Defaults에 연결·컴파일·저장. 모델 용량 오류로 result.md 없이 종료했으나 Claude 재조회/테스트로 저장 자산 확인(`assign_bp.log`). FPV/FiberOptic은 기존 연결, 지상 UGV 제외.
- **정확도 수정(C++)**: `ADroneFlightPawn::UpdateControlAttitude`의 각속도 1차 응답을 `Target·dt + (Start−Target)·τ·(1−e^(−dt/τ))`로 정확 적분하고 Pitch/Yaw/Roll을 단일 축-각 회전으로 합성. 같은 입력의 30/60/240fps 최종 자세 일치. 기존 Data Asset `FlightProfile.AcroRateSettings`의 응답 시간·최대 각속도 유지.
- `Tools/AssetMigration/BuildDroneAcroInput.py`도 Dead Zone 복사·FPV/Scout/Drop/FiberOptic 입력 6개 연결을 유지하도록 변경됨. **이번 재생성 도구는 미실행**, IMC는 일회성 패치로 처리.

## 코스 표시선·재실행 도구 — 10/04 C PC Claude

Production 읽기 전용 측정: Scale2·로컬9.6km(월드19.2km)·92 CurveAuto, 기존256조각 약75m·표시/경로 오차최대7.9m(95%2.3m). MountainRange33.8km·Island10.6km도 같은 원인. 긴 코스만 상한 내 곡률 분할, MaximumCourseLineSegments 기본1024(16~4096·Tutorial|Course|Visual)는 측정 최대50cm/95%7cm로 고른 시작값이며 확정값 아님. 2048은 최대20cm. 재생성256 46ms/1024 258ms(로드/BeginPlay 1회). BP_DroneTrainingCourse Run Construction Script on Drag Off(놓을 때1회, BP만 저장). 15.2km 시험코스 최대오차 균일256 244cm→곡률256 40cm→곡률1024 3cm. 근거 ClaudeCourse/inspect.log·deviation.log·bp_drag.log·review_fix_test.log. 팀원 코스 외형/편집 체감 수동 대기.

ConfigureDroneTitleLobby.py 설명은 현재 DA와 일치(ClaudeCourse/lobby_cmp.log). md NPCGreybox 도구는 TestMap·현재 역할별 메시/AnimBP·기존 맵이면BP를 건드리기 전Create거부, Validate통과. HostileCoverResponse도TestMap으로 정정(Claude수정/실행, Codex도구미수정). 코드 리뷰 낮음4건 모두 수정(테스트 초기화 누수·입력 해제 검사·드래그 비용·엄폐 경로), 제품 동작 버그 없음은 Claude 리뷰 판정이다.

## 최신 검증 근거 — 입력은 2026-10-07 D PC, 나머지는 10-06 C PC Claude 실행

| 검사 | 조건·결과 | 출처 |
|---|---|---|
| 입력 자산 | 기본33+축8+버튼4=45·ArmSwitch·노브 전용 메뉴 이동 구현/자동 검증됨(10/07 D PC Claude), 실기 대기. 집계 정정(10/07 Claude): test4는 17개 중 16 Success·1 Fail, 테스트 수정 후 test5 3/3 | [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md)·[WORKLOG](docs/history/DRONE_WORKLOG.md#2026-10-07-interlink-dx-버튼armswitch노브-전용-메뉴-이동--d-pc-claude) |
| Build | Editor 종료 후 Succeeded | Claude 지시서; 별도 Build 로그 경로 미제공 |
| Drone.Prototype 전체 + Drone.UI.ControlInputDisplayPIE | RenderOffScreen 1920×1080, **12/12 Success** | `Saved/Automation/ClaudeAcro/test_after_dz.log` |
| 최신 집중 회귀 | Drone.Prototype + Drone.Tutorial + Drone.UI.ControlInputDisplayPIE **32개 중30 Success·2 Fail(팀원 Production 맵 의존, 변경 전 메시지 동일)** | Saved/Automation/ClaudeCourse/review_fix_test.log |
| 최신 전체 회귀 | D-12 3차 뒤 전체101개, 실패는 KnownIssues4개·미렌더 패드 포커스6개뿐(10/06 C PC Claude 지시서) | Saved/Automation/ClaudeSplit/full_after.log |
| 입력 겹침·코스 | overlap_before 4 Fail→overlap_after, AcroInputBehaviorPIE D구역8시나리오·CourseLineAdaptiveSegments 자동 검증 | Saved/Automation/ClaudeAcro/overlap_before.log·overlap_after.log·ClaudeCourse/review_fix_test.log |
| Route 순서 의존 관찰 | 전체 5회 TrainingRouteSelectionPIE Success; 원인 미특정·해결 확정 아님 | 같은 폴더 `test.log`·`test2.log`·`final.log`·`final2.log`·`test3.log` |
| D-6 풍향·미션 배터리 | Drone.Weather 5·Drone.Mission 7·Drone.Health.BatteryHUDPIE Success(10/05 C PC Claude) | Saved/Automation/ClaudeD6/t1.log·t4.log |
| D-5 레이싱 시작·랩 타이머 | RacingStartCountdownPIE 랩 타이머 판정 추가 Success(10/06 C PC Claude) | Claude 지시서; 이번 집중 로그 경로 미제공 |

입력 자산 행의 최신 근거는 D:\JGY\project\drone\Saved\Automation\ClaudeInterLink이며 나머지 경로 루트는 C:\URproject\drone. 새벽12/12·90/94, 코스 후속30/32·전체95개2회는 당시 기록이며 최신10/06 전체101개와 합산하지 않는다. AcroInputBehaviorPIE D구역8시나리오는 키+패드-0.5·키 해제 후 인계·전체 해제0·패드만 스로틀/피치를 확인했다. 자동 입력 주입은 실제 장치 수동 Pass가 아니다.


## 알려진 실패·실행 환경·미정

- AI-SHOTGUN-RENDER-01 해결(2026-10-04 C PC Claude). 표적 고정 시 머리4.2~4.4°(Idle·사격 애니메이션), 표적±1.9° 왕복 시 머리5.2~5.4°·SmoothedDroneLookRotation 1.45°. 9/18 몸 Hysteresis·Bone Gaze 보간(데드존 경계 0 Snap 없음)은 정상, 5~6° 대부분은 9월 하순 Rifle 계열 AnimBP 교체 뒤 애니메이션 흔들림이다. 절대 머리4° 판정(애니메이션 포함)과 미렌더 뼈 정지에 따른 NullRHI 거짓 통과가 원인. 표적 고정0.6초 기준 측정 후 시선 출력≤2.5°·애니메이션 대비 추가 머리 흔들림≤2.5°로 시험 정정(경계0↔±1.9° 튐3.8° 검출). NullRHI·렌더 Success(ClaudeInterview/shotgun3_*.log), known-test-failures에서 제외(Claude 지시서 근거). D-11 구현됨·자동 검증됨(10/05 C PC Claude): 상시 실패4개를 KnownIssues.*로 분리, 기본 Automation RunTests Drone.에서 제외. 실패 해결 아님; 경로 정본은 WORKLOG. 미렌더 패드 포커스6개는 별도 제한이다.
- **PERF-ZEN-START-01 원인 특정·재측정 대기**(10/06 D PC Claude): Zen 서버가 `CommonZenDatasessions`의 지난 실행 기록 733개 폴더(1,466파일·20MB)를 로드하는 데 약 20초가 걸리고(10/06 20.3초·10/02 22.4초), 엔진은 20초를 넘기면 "Wait for ZenServer?" 모달을 띄운다(ZenServerInterface.cpp). 10/02 473초는 그 모달을 09:30:37까지 누르지 않은 대기 시간이며 캐시·셰이더 원인 아님. 사용자 요청으로 오늘 세션 폴더 1개만 남기고 732개를 `CommonZen_sessions_backup_2026-10-06`로 이동(삭제 아님, Editor 실행 중). 다음 Editor 시작에서 Zen 대기 시간 재측정 대기. Defender 실시간 검사는 사용자 판단.
- **UI-FOCUS-RACE-01 수정 후 확인 중**: UIOnly WidgetToFocus(화면 루트)의 엔진 지연 처리가 버튼 포커스를 다시 가져갈 수 있음. 5프레임 복원 적용 후 화면 그려진 회귀는 Success 1회(`test3.log`), 수정 전 Fail 1회(`final.log`). 단독 결과 혼재·사람 체감 대기, 안정화 완료 아님. TutorialNextLessonPIE에 강조/Slate 위젯 이름 실패 진단 추가.
- **TEST-RENDER-UNPAINTED-01 원인 미특정**: 최신 전체101개에서 미렌더 실행의 알려진 패드 포커스6개 실패. LobbyLayout 진단이 기본 회귀에 없으므로 GamepadMissionFlow/GamepadNavigation/TitleFiveMenu/TitleFiveMenuWidget/TutorialComplete/TutorialNextLesson 6개 모두 화면 루트 포커스로 실패하는지로 미렌더를 판단한다(10/05 C PC Claude known-test-failures 갱신). 화면 그려진 포커스·실제 패드 확인 대기.
- **레이싱 지형 연결 현재 미정**: pull 뒤 팀원 코스는 `MWLandscapeAutoMaterial` 예제 Island/MountainRange 계열에 1개, PlayerStart 없음. 아이템/게이트 자산은 어떤 맵·DA에서도 참조되지 않음. 제품 DA는 기존 `Lvl_DroneRacingTest`; 어느 지형을 제품 맵으로 쓸지·PlayerStart 배치는 사용자/팀원 결정 필요·기존 제품 완주/결과 시간은 D-5 구현 유지. Claude 맵 미수정.
- 기획 미정 보존: Acro 키보드 각속도 배율/Angle 모드/마우스 Yaw·회의 반전 뜻, 입력 표시 장치 정책, 로비 탭 유지, 레이싱 연결, Production Training 테스트2건. M2 결말·M3/M4 표적 수량/규칙, 브리핑/배터리 수치·최종 아트/메시·완료 저장도 기존 미정이다.

## 면접 대비·참조 0 정리 — Claude, 현재 C PC

- NPC Controller HostileStateTree/FriendlyStateTree(EditDefaultsOnly Soft 참조, 기본 기존 ST2개)·BP 변경 가능·로드 실패 에러 로그. StateTreeCookContract 통과, 패키징 미실행.
- Moderate HUD는 신호 불안정(영상 Noise 미연결), Scout 프리셋 전환/FPV27m/s/Drop 안정 기본 광고 문구 삭제. VeilBreaker 목표는 광섬유 드론으로(끊김 규칙 미정). PlayerFacingTextContract 통과.
- Rifle/MG 디버그 선 기본 Off, 상수 TestTrue4건을 실제 조건으로 교체, 기체6개 이상 [DRONE-SELECT] 경고(동적 목록 후속). FrontEndContract·FlightProfiles·StateTreeCookContract·PlayerFacingTextContract Success, AI/UI NullRHI22개 중20 Success·당시 NPCPerception/Shotgun2Fail(후속 Shotgun 해결).
- 참조0 검증된 프리셋 튜닝·미사용 API/include/Build.cs 주석 정리, HoverThrottleNormalized는 도구3개 호환 유지·런타임 미사용. Tools/AssetMigration 낡은 도구12개 삭제됨(Git 이력), 게이트 도구 기본검증·APPLY=1일 때만 저장, 타이틀 임포트 경로 명시 필수. md tools 변경은 Claude 기존 수정이며 Codex 미수정.
- D-12 1차 Legacy 정리와 D-14 MCP 로컬 설정 전환은 구현됨·자동 검증됨(10/05 C PC Claude). MCP 공유 Default bAutoStartServer=False·필요 PC Saved 로컬 True·C PC 실행15초 뒤8000 응답 확인. CLAUDE.md MCP 설명도 D-14와 일치하도록 수정됨(10/06 Claude): 공유 끔·사용자 PC 로컬만 켬·팀원 불필요. 설정 절차는 [협업 세팅](docs/git/CLAUDE_CODEX_SETUP.md#unreal-mcp-자동-시작--pc별-로컬-설정)·삭제 상세는 WORKLOG.

## 사용자 결정·확인 대기

결정/카드 정본은 [WORKBOARD](WORKBOARD.md). D-5·D-6·D-11·D-14와 D-12 Legacy 정리·Flight 이름 변경/분리는 위 구현·검증 상태를 따른다.

- InterLink DX 실제 콘솔·노브/Cancel 메뉴 사용 확정. 버튼3개=좌클릭/우클릭/P·자폭1=온/0=오프·노브 위/아래만으로 메뉴 이동 확정. 구현/자동 검증됨·실기 대기. 노브 회전 방향·Button1 물리 종류·브리핑 넘김/탭 전용 버튼·미인식 안내·비복귀 스로틀 처리·전시 정책/다기종 지원 현재 미정. [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md).
- 현재 미정: 높이 제한 수치·경고 연출·배터리 시간 값·레이싱 코스4개 지형·D-1(M2)·D-2(M3/M4)는 기획자 내용 대기.
- 미구현: 코스4개·배터리 시간 설정.
- 방콕 잔여987개 삭제는 원격 `1619b4f` diff에서 확인했다. 로컬 수신과 과거 LFS 객체/요금은 별도이며 D-13 나머지 유지 결정은 종료(정본 WORKBOARD).
- 기타 기존 기획 미정·수동 대기는 위 기능별 행과 WORKBOARD 참조·applications는 수정하지 않는다.

## 다음 확인

1. InterLink DX의 비행 축·Dead Zone·Mode 2 호버/피치·쉬운 조작 비복귀 스로틀 체감, Button1 무장/해제 체감·Button12/13, 노브만으로 타이틀→로비→탭→미션→브리핑→기체 선택→출격→결과 이동·첫 강조, 설정 슬라이더 잠금/조절·콤보·노브 방향/확인/Cancel을 확인한다. Acro Mode1에서 스틱에 엄지를 걸친 채 Space→상승, 키 떼고 스틱→패드 조종·모두 놓으면0을 확인하고 Mode2도 비교한다. 코스 급커브 표시선·끝 연결과 Editor 편집 체감도 확인한다. 키보드 짧게 톡(0.1초, FPV 약65°) 후 자세 유지. W+Space와 Space 단독 구분, Scout/Drop Acro 비행도 실제 장치로 확인. 결과·타이틀 첫 버튼 강조를 반복 관찰.
2. 추가 자동 회귀 판정 전 화면이 그려졌는지 확인하고 포커스 경쟁·미렌더 실행을 따로 기록. UI-LAYOUT-DIAG-01·AI-PERCEPTION-TEST-01 기존 관찰 유지, AI-SHOTGUN-RENDER-01 해결. Route는 재발 시 순서 조사.
3. 사용자/팀원은 코스4개 지형/PlayerStart·배터리 시간과 Acro 미정 조작 방식을 결정. 레이싱 카운트다운·랩 타이머·FPV 곡예/UGV 분리 전 동일 체감·풍향 HUD 수동 확인·시간 결정 뒤 배터리 추락 확인. 1280/1920·실제 패드·8수업 연속 진행·Best Lap 재실행·설정/배터리/브리핑·추락 재출격 수동 확인 후 Story 콘텐츠를 고도화.
4. D PC: `1619b4f` 수신 뒤 Editor Build와 Zen 시작 시간 cold/warm 비교(PERF-ZEN-START-01). 소스 수신은 바이너리/플레이 완료가 아니다. WORKBOARD는 10/06 D PC에서 7그룹으로 재배치했고 카드 본문은 유지했다.

세부 카드와 완료 조건은 [WORKBOARD](WORKBOARD.md), 입력 조정은 [Blueprint 가이드](docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md), 수동 순서는 [테스트 가이드](docs/gameplay/DRONE_TEST_MAP_GUIDE.md)를 따른다. Commit/Push·Trello/Figma 수정·공유 권한·예약 자동화는 수행하지 않는다.

## 이전 기록 보존

10/01 이전 구현·검증·당시 미확인/경계 집계 네 절은 [2026-09 원문 아카이브](docs/history/archive/STATUS_2026-09.md)로 이동했다. 10/01~10/03 세션 전문과 기존 한눈에 보기·Git 요약은 [WORKLOG의 2026-10-04 STATUS 정리 절](docs/history/DRONE_WORKLOG.md)에 원문 그대로 보존했다. 과거 PC/날짜·Codex/Claude 표기를 바꾸지 않았으며 최신 상태를 과거 기록에 소급하지 않는다.
