# 현재 작업 상태

기준일: 2026-10-04 오후 면접 대비·정리 반영 (Asia/Seoul), C PC. 조사·C++·Build·자동화 Claude, Scout/Drop BP 입력 연결 Codex(ui, Editor MCP)→Claude 검증, 문서·Space Codex. 아래 구현·검사 수치는 Claude 지시서 근거이며 Codex는 Git·감사 근거와 지정 로그를 읽기 전용 대조했다. 이번 docs 작업에서 엔진 Build·PIE·맵 재생성을 실행하지 않았다.

## Git 기준

| 저장소 | 현재 기준 | 상태 |
|---|---|---|
| Unreal `C:\URproject\drone` | HEAD = 추적 origin/main = `41444c2` | Codex 읽기 전용 Git 확인. pull·LFS 실제 본문 수신은 Claude 지시서 근거. 입력 자산·C++·UI·테스트·재생성 도구 등 로컬 미커밋/미추적 있음 |
| 문서 `C:\Users\jkw11\Documents\Codex\2026-08-19\codex-gpt-chatgpt-codex-1-6` | HEAD `250e975` | 기존 미커밋 MD 보존, 이번 문서 변경 추가. Commit/Push 미실행; GitHub는 로컬 변경 반영 전 |

## 한눈에 보기

10/04 오후: Claude의 면접 대비 5관점+반박 검증 58건(높음7·중간32·낮음19), 처리14건과 참조0 코드/도구 정리를 반영했다. StateTree Soft 참조/AlwaysCook·플레이어 문구 계약·디버그 선 Off 자동 검증, 실제 패키징·패드 체감 미확인. 코스/Acro 기존 수정·자동 검증과 Production 맵 보호는 유지한다.

| 영역 | 구현·자동 검증 | 수동 확인 대기·미구현·현재 미정 |
|---|---|---|
| 시작·로비 | 스토리/레이싱/튜토리얼/설정/종료 5메뉴, 분류 직접 진입, 상하 순환·Back/포커스 복원, 저장 `WBP_DroneFiveItemMenu` 연결 | 실제 패드·1280/1920 배치 확인 대기. 로비 Tutorial/Racing 탭·LB/RB는 현재 유지, 최종 유지 여부 미정 |
| 조종 입력 표시 | 설정 수동 ON/OFF·선택 저장, 저장 `WBP_DroneControlInputDisplay` 연결. 아래 중앙 스틱 표시·OFF 갱신 중지, 고도계 독립 | 기본 False는 임시 끔, 최종 기본값·장치 자동 전환/분리·재연결 정책 미정. 실제 화면/패드 확인 대기 |
| 코스 표시선 | 긴 코스만 sqrt(곡률) 밀도+15% 균일 몫, 짧은 TestMap68/113조각 기존 균일 분할 유지. MaximumCourseLineSegments 노출·기본1024(시작값·미확정), BP 드래그 재구성 Off | 팀원 Production 코스 외형·Editor 편집 체감 수동 대기. Production 맵 미저장 |
| Acro | 비행 기체 FPV/Scout/Drop/FiberOptic 6개 입력 연결, 패드 축 4개 Dead Zone, 정확 자세 적분. 키보드·패드 입력원 분리·절댓값 큰 쪽 사용·키 해제 시 패드 인계, Space 단독 자세 불변·Mode 1/2 키보드 동일·FPS 무관 자동 검증 | 실제 패드/키보드 체감·Scout/Drop 비행 대기. 키보드 각속도 배율·Angle 모드·마우스 Yaw·회의 “좌우 스틱 반전” 뜻 미정 |
| 패드 첫 포커스 | `FDroneGamepadFocus`가 포커스 부여 후 5프레임 감시·루트/없음으로 이탈 시 복원, 다른 강조 버튼 이동은 보존 | UI-FOCUS-RACE-01 **수정 후 확인 중**. 화면 그려진 수정 전 Fail/후 Success 각 1회, 간헐적 첫 버튼 강조 수동 확인 대기 |
| 튜토리얼·Story 순서 | 독립 Tutorial 8수업·Story 4·Racing 1, 로비 Tutorial 9/Racing 1/Story 4. 호버→전진→회전→게이트→자폭→드랍→UGV NPC→포탑. 시간·다음·n/8·전체 완료·로비 완료 표시 | 실제 8수업 연속 완주/S48·S49·로비 확인 대기. 완료 영구 저장·회의 4개와 문서 8수업 집계 단위 미정; 조작키 브리핑 미입력 |
| Best Lap | `CourseId|DroneId|ControlMode`별 JSON 저장/복원·없음/구버전/손상 처리·HUD, HandlingPreset 제외. 평균은 실행 History | 같은 조건 실제 랩 후 재실행 복원 확인 대기. 정식 레이싱 방식 미정 |
| 허브·HUD | Story 허브 브리핑 4/4/5/6줄·Voice 슬롯·자동 진행/Y·Tab·정지; M3 첫 줄 TargetEliminated 조건. 기체명·신호 대역·배터리 %/시간·부족/방전 | 음원 없음·튜토리얼 대사 미입력. 기체 배터리 시간 모두 0·신호 대역 빈 값, 수치·소진 처리·분기/재출격 브리핑 미정 |
| 미션·실패 | DA 지정 폴더 자동 등록, Definition/Rule/Trigger·체크포인트 재출격. Tutorial 8/M1·M3·M4 재출격, M2/공용 Training/Racing 결과 화면 | 실제 체크포인트 Actor 미배치·현재 첫 출격 위치 재출격. 추락 체감·새 DA 로비 등록 수동 확인 대기. Story M1~4 콘텐츠·분기 고도화 필요 |
| 레이싱 | 제품 DA는 `TestMap/Lvl_DroneRacingTest`, RouteSelector 없음·제품 1~5 안내/입력 차단. 직접 Route 시험/Tutorial/Training/Story 보존 | 팀원 지형 코스와 제품 연결·PlayerStart·완주 판정 미정. 3·2·1/최종 경기 규칙 미구현 |
| 물리·역할 | 질량·추력·모터 응답·선형/제곱 항력·Drop kg 하중, Mode 1/2 공통. 속도 단계 제거. 벽/날개 접촉·그물 포획 Greybox·접촉 카메라 분리, 피해 Shake 유지 | Acro는 게임용 근사 모델, 실기체 교정 미완료. 수동 속도/하중/접촉·실제 Chaos 비교 필요 |
| AI·차량·날씨 | NPC 순찰/추적/사격·AI-LOCOMOTION-01 구현됨·자동 검증됨(2026-10-04 C PC Claude 재생 확인)·수동 확인 대기. 두 AnimBP의 ShouldMove를 속도 > 3만으로 수정: 수정 전 이동 표본41개 중0→수정 후40개(NPC8명) 모두 ShouldMove·걷기/뛰기 BlendSpace 진입. Drone.AI 19개 중18 Success·기존 NPCPerceptionSearchPIE 1 Fail, Shotgun 시선 Success. Claude 지시서 근거(ClaudeNPCWalk/before.log·after.log). 자연스러운 순찰/추적 전환·발 미끄러짐(속도 대비 보폭)·뒷걸음 방향 수동 확인 대기. Epic 마네킹 임시 동작·최종 아님. StateTree Soft 참조 및 폴더 AlwaysCook/로드 실패 로그·Rifle/MG 디버그 선 기본 Off. 차량·바람/비·천장 차단 | NPC 감지 PIE Fail 유지. Shotgun 시선 안정화 정상·시험 정정 후 NullRHI/렌더 Success(해결). 최종 Rain/Audio/품질 미구현 |
| 환경·기체 | OilRigPreview 이식·외부/누락0/0·Map Check0/0의 9월 근거. Bangkok 맵은 ec2e88f(10/01)에서 삭제, 10/04 사용자 의도된 삭제 확인; 의존987개·LFS약11.46GiB 남음, 광섬유 DroneSpy·GSU/케이블·UGV 총/유탄 기반 | 현재 PC의 전체 맵 성능·외형 수동 확인 별도. 사람 최종 아트·애니메이션·음원 보존 |
| 패키징 | Asset Manager DroneMission/DroneDefinition AlwaysCook·MissionMap 참조, StateTrees 폴더 DirectoriesToAlwaysCook·StateTreeCookContract 자동 검증 | 실제 패키징/패키지 맵 진입 미실행 |

## Acro 회의 조사·수정 — ACRO-MEETING-01

- **10/04 사용자 보고 Mode1 Space 하강/뒤집힘**: 키보드와 패드 세로축 Action이 한 변수를 나중 값으로 덮는 원인을 재현했다. Space+오른쪽 -0.5→스로틀 -0.38, W+왼쪽 -0.5→피치 -0.38(Mode2도 같은 구조). 키보드·패드 입력원을 분리하고 절댓값이 큰 쪽을 사용하도록 수정. 키를 누르면 키보드가 이기고 떼면 패드가 조종한다. Space 단독 자세 불변 검사는 패드 혼합 입력 결함이 없다는 근거가 아니었다. 실제 패드 체감은 수동 대기.
- **Mode 1/2**: 키보드 키/결과 동일, 패드 세로축만 RC 표준에 따라 다름. Mode 2 LeftY=Throttle·RightY=Pitch, Mode 1 LeftY=Pitch·RightY=Throttle. 회의 “좌우 스틱 반전”이 이 배치인지 축 부호 등 다른 문제인지 **현재 미정**.
- **결함 1, 패드+키보드 동시 입력**: Enhanced Input은 DefaultInput.ini 축 데드존을 사용하지 않음. Acro 패드 매핑에 Dead Zone이 없어 0.05 쏠림이 키보드 스로틀을 덮고 손을 떼도 각속도가 누적됐다. IMC 4개 축 매핑 맨 앞에 쉬운 조작 패드 매핑 값을 그대로 복사(Lower 0.2·Upper 1.0·Radial). 새 수치 결정 아님, 매핑 33개·키/Action/순서 유지.
- IMC 수정 담당 구분: Codex MCP는 Instanced Modifier 하위 객체 생성 실패(None)로 **저장 없이 원상복구**. Claude가 Editor 종료 후 headless Unreal Python으로 IMC만 패치·저장·재조회(`ClaudeAcro/patch_dz.log`).
- **결함 2, Scout/Drop Acro 입력 누락**: 두 BP의 Acro 입력 6개가 None이었다. Codex ui run `20261004-001325-ui-ui-acro-input-assets`에서 FPV와 같은 6개 Action을 Class Defaults에 연결·컴파일·저장. 모델 용량 오류로 result.md 없이 종료했으나 Claude 재조회/테스트로 저장 자산 확인(`assign_bp.log`). FPV/FiberOptic은 기존 연결, 지상 UGV 제외.
- **정확도 수정(C++)**: `ADronePrototypePawn::UpdateControlAttitude`의 각속도 1차 응답을 `Target·dt + (Start−Target)·τ·(1−e^(−dt/τ))`로 정확 적분하고 Pitch/Yaw/Roll을 단일 축-각 회전으로 합성. 같은 입력의 30/60/240fps 최종 자세 일치. 기존 Data Asset `FlightProfile.AcroRateSettings`의 응답 시간·최대 각속도 유지.
- `Tools/AssetMigration/BuildDroneAcroInput.py`도 Dead Zone 복사·FPV/Scout/Drop/FiberOptic 입력 6개 연결을 유지하도록 변경됨. **이번 재생성 도구는 미실행**, IMC는 일회성 패치로 처리.

## 코스 표시선·재실행 도구 — 10/04 C PC Claude

Production 읽기 전용 측정: Scale2·로컬9.6km(월드19.2km)·92 CurveAuto, 기존256조각 약75m·표시/경로 오차최대7.9m(95%2.3m). MountainRange33.8km·Island10.6km도 같은 원인. 긴 코스만 상한 내 곡률 분할, MaximumCourseLineSegments 기본1024(16~4096·Tutorial|Course|Visual)는 측정 최대50cm/95%7cm로 고른 시작값이며 확정값 아님. 2048은 최대20cm. 재생성256 46ms/1024 258ms(로드/BeginPlay 1회). BP_DroneTrainingCourse Run Construction Script on Drag Off(놓을 때1회, BP만 저장). 15.2km 시험코스 최대오차 균일256 244cm→곡률256 40cm→곡률1024 3cm. 근거 ClaudeCourse/inspect.log·deviation.log·bp_drag.log·review_fix_test.log. 팀원 코스 외형/편집 체감 수동 대기.

ConfigureDroneTitleLobby.py 설명은 현재 DA와 일치(ClaudeCourse/lobby_cmp.log). md NPCGreybox 도구는 TestMap·현재 역할별 메시/AnimBP·기존 맵이면BP를 건드리기 전Create거부, Validate통과. HostileCoverResponse도TestMap으로 정정(Claude수정/실행, Codex도구미수정). 코드 리뷰 낮음4건 모두 수정(테스트 초기화 누수·입력 해제 검사·드래그 비용·엄폐 경로), 제품 동작 버그 없음은 Claude 리뷰 판정이다.

## 최신 검증 근거 — 2026-10-04 C PC, Claude 실행

| 검사 | 조건·결과 | 출처 |
|---|---|---|
| 입력 자산 | Dead Zone 4개·매핑 33·재조회 일치; Scout/Drop 같은 입력 6개 확인 | `Saved/Automation/ClaudeAcro/patch_dz.log`·`assign_bp.log` |
| Build | Editor 종료 후 Succeeded | Claude 지시서; 별도 Build 로그 경로 미제공 |
| Drone.Prototype 전체 + Drone.UI.ControlInputDisplayPIE | RenderOffScreen 1920×1080, **12/12 Success** | `Saved/Automation/ClaudeAcro/test_after_dz.log` |
| 최신 집중 회귀 | Drone.Prototype + Drone.Tutorial + Drone.UI.ControlInputDisplayPIE **32개 중30 Success·2 Fail(팀원 Production 맵 의존, 변경 전 메시지 동일)** | Saved/Automation/ClaudeCourse/review_fix_test.log |
| 최신 전체 회귀 | Drone.* **97개 중86 Success·11 Fail**, PIE 미렌더: 포커스6개 판정 제외, 당시 나머지5개(후속 Shotgun 해결·전체 재실행 아님)(NPCPerception·Shotgun 판정 오류(후속 해결)·LobbyLayout 진단·Production Training2) | Saved/Automation/ClaudeInterviewFull/test.log (Codex 읽기 전용97/86 대조) |
| 입력 겹침·코스 | overlap_before 4 Fail→overlap_after, AcroInputBehaviorPIE D구역8시나리오·CourseLineAdaptiveSegments 자동 검증 | Saved/Automation/ClaudeAcro/overlap_before.log·overlap_after.log·ClaudeCourse/review_fix_test.log |
| Route 순서 의존 관찰 | 전체 5회 TrainingRouteSelectionPIE Success; 원인 미특정·해결 확정 아님 | 같은 폴더 `test.log`·`test2.log`·`final.log`·`final2.log`·`test3.log` |

경로 루트는 C:\URproject\drone. 새벽12/12·90/94, 코스 후속30/32·전체95개2회는 당시 기록이며 최신 오후97개와 합산하지 않는다. AcroInputBehaviorPIE D구역8시나리오는 키+패드-0.5·키 해제 후 인계·전체 해제0·패드만 스로틀/피치를 확인했다. 자동 입력 주입은 실제 장치 수동 Pass가 아니다.

## 알려진 실패·실행 환경·미정

- AI-SHOTGUN-RENDER-01 해결(2026-10-04 C PC Claude). 표적 고정 시 머리4.2~4.4°(Idle·사격 애니메이션), 표적±1.9° 왕복 시 머리5.2~5.4°·SmoothedDroneLookRotation 1.45°. 9/18 몸 Hysteresis·Bone Gaze 보간(데드존 경계 0 Snap 없음)은 정상, 5~6° 대부분은 9월 하순 Rifle 계열 AnimBP 교체 뒤 애니메이션 흔들림이다. 절대 머리4° 판정(애니메이션 포함)과 미렌더 뼈 정지에 따른 NullRHI 거짓 통과가 원인. 표적 고정0.6초 기준 측정 후 시선 출력≤2.5°·애니메이션 대비 추가 머리 흔들림≤2.5°로 시험 정정(경계0↔±1.9° 튐3.8° 검출). NullRHI·렌더 Success(ClaudeInterview/shotgun3_*.log), known-test-failures에서 제외(Claude 지시서 근거). 현재 알려진 실패: NPCPerceptionSearchPIE·LobbyLayout 진단·TrainingAssets·TrainingPIESmoke(팀원 맵), 미렌더 실행 시 패드 포커스6개.
- **UI-FOCUS-RACE-01 수정 후 확인 중**: UIOnly WidgetToFocus(화면 루트)의 엔진 지연 처리가 버튼 포커스를 다시 가져갈 수 있음. 5프레임 복원 적용 후 화면 그려진 회귀는 Success 1회(`test3.log`), 수정 전 Fail 1회(`final.log`). 단독 결과 혼재·사람 체감 대기, 안정화 완료 아님. TutorialNextLessonPIE에 강조/Slate 위젯 이름 실패 진단 추가.
- **TEST-RENDER-UNPAINTED-01 원인 미특정**: 오늘 전체10회 중8회 PIE 미렌더(Claude 지시서). 최신97개도 포커스6개(GamepadMissionFlow/GamepadNavigation/TitleFiveMenu/TitleFiveMenuWidget/TutorialComplete/TutorialNextLesson) 판정 제외. 미렌더 표지는 LobbyLayout samples=0만 쓰고 Shotgun은 제외한다. known-test-failures 갱신, 화면 그려진 포커스 확인 대기.
- **레이싱 지형 연결 현재 미정**: pull 뒤 팀원 코스는 `MWLandscapeAutoMaterial` 예제 Island/MountainRange 계열에 1개, PlayerStart 없음. 아이템/게이트 자산은 어떤 맵·DA에서도 참조되지 않음. 제품 DA는 기존 `Lvl_DroneRacingTest`; 어느 지형을 제품 맵으로 쓸지·PlayerStart·완주/복귀는 사용자/팀원 결정 필요. Claude 맵 미수정.
- 기획 미정 보존: Acro 키보드 각속도 배율/Angle 모드/마우스 Yaw·회의 반전 뜻, 입력 표시 기본값, 로비 탭 유지, 레이싱 연결, Production Training 테스트2건. M2 결말·M3/M4 표적 수량/규칙, 브리핑/배터리 수치·최종 아트/메시·완료 저장도 기존 미정이다.

## 면접 대비·참조 0 정리 — Claude, 현재 C PC

- NPC Controller HostileStateTree/FriendlyStateTree(EditDefaultsOnly Soft 참조, 기본 기존 ST2개)·BP 변경 가능·로드 실패 에러 로그. StateTreeCookContract 통과, 패키징 미실행.
- Moderate HUD는 신호 불안정(영상 Noise 미연결), Scout 프리셋 전환/FPV27m/s/Drop 안정 기본 광고 문구 삭제. VeilBreaker 목표는 광섬유 드론으로(끊김 규칙 미정). PlayerFacingTextContract 통과.
- Rifle/MG 디버그 선 기본 Off, 상수 TestTrue4건을 실제 조건으로 교체, 기체6개 이상 [DRONE-SELECT] 경고(동적 목록 후속). FrontEndContract·FlightProfiles·StateTreeCookContract·PlayerFacingTextContract Success, AI/UI NullRHI22개 중20 Success·당시 NPCPerception/Shotgun2Fail(후속 Shotgun 해결).
- 참조0 검증된 프리셋 튜닝·미사용 API/include/Build.cs 주석 정리, HoverThrottleNormalized는 도구3개 호환 유지·런타임 미사용. Tools/AssetMigration 낡은 도구12개 삭제됨(Git 이력), 게이트 도구 기본검증·APPLY=1일 때만 저장, 타이틀 임포트 경로 명시 필수. md tools 변경은 Claude 기존 수정이며 Codex 미수정.
- DefaultEngine.ini 중복 키2줄 제거·DefaultGame.ini ProjectName=Drone. Unreal CLAUDE.md MCP 공유 Default 설명·문서 위임 하루 상한 삭제 반영. 문서 위임은 결과 확정 뒤 묶으며 횟수 제한 없음(10/04 사용자 결정).

## 사용자 결정·확인 대기

- md 공개 범위와 이미 원격 Push된 PROJECT_EXPERIENCE_PLAN_HWP_GUIDE의 기업 주소·대표자·팀원 실명·예산·로컬 경로 처리 여부: 사용자 결정, applications 미수정.
- 9/17 OpenRouter API 키 폐기 여부: 사용자 확인, 키 값은 저장소에 없음·읽지 않음.
- ThirdParty/BangkokCity 의존987개·LFS약11.46GiB 정리 여부: 사용자 결정. 맵은 의도된 삭제.

1. 제3자 구매 자산 약51GB: GitHub 공개 여부 확인 후 비공개 전환 또는 자산 분리·출처 목록. 라이선스 처리·공개 범위 현재 미정.
2. 본인 기여와 AI 활용 설명: 본인 설계·결정·검증 범위를 먼저 확인하고 README에 정직하게 정리. C++ Claude 담당 표기의 면접 설명 필요, 본인 담당 미확인.
3. 포트폴리오 루트 README: 플레이 방법·설계/기여·검증 근거·용량/출처를 담을 범위 결정. Unreal 루트 README 부재, 이번 신규 작성 안 함.
4. main 상시 실패 테스트4개: 별도 그룹 분리 또는 조건부 건너뛰기 여부. NPCPerception·LobbyLayout 진단·TrainingAssets/TrainingPIESmoke; Shotgun 해결.
5. Prototype Pawn 분리·명명: h875/cpp2410줄 분리 범위/순서 및 Prototype/Greybox 변경 시점. CoreRedirects·팀원 BP/자산 영향 확인 필요, 현재 미정.
6. Legacy 템플릿: C++76파일·자산100개 정리 범위. 사용자/팀원 결정 대기.
7. 방콕·미사용 자산: Bangkok 잔여987개 약12GB와 다른 구매/팀원 자산 정리. 목록은 Claude 점검 근거, 팀원 자산 삭제·정리 미실행.
8. 풍향 기준: HUD 방위와 거울상 불일치, 불어오는 쪽 기상 관례 채택 여부. 규약 현재 미정, 수치/명명 변경 안 함.
9. 공유 Config MCP: 모든 팀원 PC의 8000포트 자동 시작 유지 여부. Default ini 공유 자동 시작이 실제 설정, 정책 현재 미정.
10. BP/Legacy API: 호출 없는 함수19개·1회 접근자71개가 디자이너용인지, 핸들링 Legacy 정리. 참조0 확정 삭제분과 구분, 추가 삭제 결정 대기.

## 다음 확인

1. Acro Mode1에서 스틱에 엄지를 걸친 채 Space→상승, 키 떼고 스틱→패드 조종·모두 놓으면0을 확인하고 Mode2도 비교한다. 코스 급커브 표시선·끝 연결과 Editor 편집 체감도 확인한다. 키보드 짧게 톡(0.1초, FPV 약65°) 후 자세 유지. W+Space와 Space 단독 구분, Scout/Drop Acro 비행도 실제 장치로 확인. 결과·타이틀 첫 버튼 강조를 반복 관찰.
2. 추가 자동 회귀 판정 전 화면이 그려졌는지 확인하고 포커스 경쟁·미렌더 실행을 따로 기록. UI-LAYOUT-DIAG-01·AI-PERCEPTION-TEST-01 기존 관찰 유지, AI-SHOTGUN-RENDER-01 해결. Route는 재발 시 순서 조사.
3. 사용자/팀원은 레이싱 지형/PlayerStart·완주 연결과 Acro 미정 조작 방식을 결정. 1280/1920·실제 패드·8수업 연속 진행·Best Lap 재실행·설정/배터리/브리핑·추락 재출격 수동 확인 후 Story 콘텐츠를 고도화.

세부 카드와 완료 조건은 [WORKBOARD](WORKBOARD.md), 입력 조정은 [Blueprint 가이드](docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md), 수동 순서는 [테스트 가이드](docs/gameplay/DRONE_TEST_MAP_GUIDE.md)를 따른다. Commit/Push·Trello/Figma 수정·공유 권한·예약 자동화는 수행하지 않는다.

## 이전 기록 보존

10/01 이전 구현·검증·당시 미확인/경계 집계 네 절은 [2026-09 원문 아카이브](docs/history/archive/STATUS_2026-09.md)로 이동했다. 10/01~10/03 세션 전문과 기존 한눈에 보기·Git 요약은 [WORKLOG의 2026-10-04 STATUS 정리 절](docs/history/DRONE_WORKLOG.md)에 원문 그대로 보존했다. 과거 PC/날짜·Codex/Claude 표기를 바꾸지 않았으며 최신 상태를 과거 기록에 소급하지 않는다.
