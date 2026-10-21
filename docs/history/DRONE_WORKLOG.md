# Drone 개발 진행 기록



### 최종 축 보정과 실제 새 프로세스 검증

원본 export의 RapidIterationParameterData를 해독하고 실제 particle JSON과 교차했다. Rain Box=(500,5,5), Lifetime=2초, Velocity Min=(0,200,-980)/Max=(1,400,-3000)였다. 실제 rawX 약-250..249는 생성 폭, rawY 약-2..1017은 나이별 이동이었다. Y-age 상관0.625/Y-Z 상관-0.542를 확인했으며 Y 범위를 생성 폭으로 보고 -1650cm만 옮긴 중간 가설은 틀렸다. 이 실패/진단은 위 기록으로 보존한다.

최종은 카메라 quaternion × simulation basis(Yaw=-90°), 위치는 카메라 quaternion × Offset(1150,0,600)으로 분리했다. 원본 X→화면 가로(-Y), 원본 Y 이동→카메라 전방(+X), 원본 Z→화면 세로다. BP에 CameraRainLayerRotationOffset을 노출했다. 비기본 camera/basis의 pitch/yaw/roll과 위치 offset을 섞어도 합성 순서가 유지되는 회귀를 추가했다. 원본 Niagara 그래프/velocity·프로젝트 mask/density는 이 보정에서 변경하지 않았다.

| 마지막 검사 | 실제 결과 | Saved 기준 근거 |
|---|---|---|
| DroneEditor Win64 Development Build | Succeeded·26.40초, MSVC14.51.36257·기존 경고 유지 | Logs/Build_20261014_GateRainCity_Final3.log |
| 실제 D3D12 RHI 집중 자동화 | **21 Success / 0 SuccessWithWarnings / 0 Fail / 0 NotRun**, 46.5602초 | Automation/GateRainCity/Final3Report/index.json·final3_render.log |
| 실제 생성기·시드194849 도시/비 | 9 PNG 모두1274×716, 정면/90°이동/75°상향 이동에서 가로3·세로3뿐 아니라 실제9칸 전부 입자 존재, Off/Disable/Clear0 | Automation/CityAppearance/S194849/gate_rain_city_final/Capture_6F09F85349AAB75E6F2A4395B5FE79A7/ |
| 별도3품질·카메라 캡처 | 낮음/중간/높음 × 정면/90°/75° + Off=10 PNG | Automation/RainCameraPresentation/gate_rain_city_final/Capture_46B32C8A4547D1300D9C628F740FBC1E/ |
| Palette 재실행 | 성공·추가 재질 생성0·Type51 유지. BP/TestMap만 저장, m_green 재저장0·복제 parent/class/HISM guard 통과 | Automation/GateRainCity/city_reapply_verified.log·CityAppearance/20261014T062349_880961Z/report.json |
| 원본/팀원 보존 | Island 재로드 SHA 불변/저장0, Production Training/FC/MOUT/ThirdParty pack 경로 Git diff0 | IslandGateSize/report.json·최종 경로별 Git 확인 |

최종21개는 Diagnostics 실제도시/별도Rain캡처2개, Procedural Appearance5개, Tutorial Course/Gate6개, Weather5개, UI Font/선택명2개, Settings1개다. 엔진 startup/PSO·VSM/드라이버 경고까지0이라는 뜻은 아니다. 전체 Drone.*·패키징·실제 패드·실내 복귀/FPS·모든 시드/완주/기록 검증도 아니다. 기존 CourseManyGates 경고100을 수정 완료로 바꾸거나 전체 회귀에 포함하지 않았다.

최종 실제 도시 Rain frustum 입자수는 정면377/90°이동383/75°상향388이다. 각9칸 최소8/14/12개로 한쪽 빈 화면 문제를 재현한 동일 검사가 통과했다. root가 최종3뷰 PNG를 직접 열어 화면 좌우 분포/얇은 빗줄기를 확인했고, 앞선 도로·닫힌 컨테이너·콘크리트 골조·중복 없는 완성 창고도 확인했다. 이는 사용자 플레이 체감 Pass가 아니다. 원본 Rain/Island/Production 맵을 덮는 생성 도구는 실행하지 않았다.

### 문서·Space와 인계

기존 STATUS/WORKBOARD/CONTEXT·비/저작/시험 가이드를 갱신했고 새 주제 MD는 만들지 않았다. STATUS 크기 확보는 이전 Acro 회의·코스 표시선 상세 원문만 기존 STATUS_2026-10.md로 이동했다. 원문 이동 당시 STATUS29,829B/126줄→26,167B/113줄, 아카이브56,297B/206줄→60,489B/228줄이었다. 이동 raw CRLF 텍스트 SHA256=6658E3B4010F6A25B784208A91798D6C2C1FA9A1308BD66B907FE8936704E033, 이전 아카이브 prefix를 보존했고 기존 색인 링크를 사용했다. 최종 현재 상태 갱신 뒤 크기는 아래 마감 확인을 따른다.

Drone Space 기존 진행상황 Sequence40(3블록)·BP가이드26(2블록)·시험가이드27(2블록) 총7연산을 적용했다. 각 블록을 같은 content stream에서 다시 읽어 기대 Markdown과 전부 정확히 일치함을 확인했다. 기획3·지침9·루트는 변경하지 않았으며 새 Page·공유 권한 변경·예약은 없다. 사람의 기존 기획/보드 링크·이전 검증 출처를 보존하고 현재 수정·자동 검사/수동 대기를 구분했다. GitHub MD 링크는 사용자 Commit/Push 뒤에야 새 본문이 반영된다.

다음 실기: 새 Editor에서 Island Gate 폭/방향·3상태색, Lvl_ProceduralCityRaceTest 또는 로비 랜덤 레이싱 시드194849의 콘크리트·도로/차선·컨테이너 지지·지붕 중복 없음과 Rain3품질/회전/이동/실내/실외/Off를 확인한다. 팀원 Gate 저장 재시험·InterLink/8수업/완주/기록·Observer/물리/재밍 체감·Patriot는 기존 후속이다. Commit/Push는 사용자가 한다.

마감 확인: 변경 Python9개 UTF-8 AST 구문 검사 통과·플레이어 UI 기본 폰트 감사 위반0, Unreal diff --check 오류0(일부 CRLF 알림). MD는 이동 원문의 CRLF 보존 때문에 git -c core.whitespace=cr-at-eol diff --check로 확인하며 오류0이다. STATUS27,028B·WORKBOARD29,610B로30,000B 이하, 기존 STATUS 아카이브60,489B 보존. Unreal63개·MD12개 상태 항목은 앞선 변경을 포함한 의도된 미커밋 목록이다. Editor/Commandlet/Build 프로세스0, HEAD/로컬 origin은 그대로다. 처음 AST stdin 검사는 Windows 기본 인코딩 때문에 중단됐고 UTF-8 명시 후9개 모두 통과했으며 소스 구문 결함은 아니었다. 사용자 수동 Pass·Commit/Push는 실행/추정하지 않았다.
기준일: 2026-10-04 (Asia/Seoul)

기존 날짜별 기록의 배열은 보존하고 새 기록은 끝에 날짜순으로 추가한다. 현재 상태는 [STATUS](../../STATUS.md)를 따른다.

## 2026-10-01 후속 — C 드라이브 PC 현황 최신화와 다음 작업 정리

- 현재 Unreal `C:\URproject\drone` HEAD `9f67706`, 문서 작업 폴더 HEAD `ff69c11`을 실제 원격 main과 `git ls-remote`로 대조했다. 점검 시작 두 Clean·추적 브랜치 0/0이며 후속 UI/Settings 코드는 수신됐다. 이전 D PC `83b33c1`/`aecb6ec` 기준과 로컬 미커밋 설명을 현재 현황에서 교정하고 당시 기록은 아래에 보존했다.
- C PC의 기존 GameReadiness 32 Success·Back 32 Success + 경고 동반 성공 1(실패 0)·TitleLobbyOrbit 14 Success 보고서를 읽었다. D PC의 후속 UI 5/5와 목록 Geometry Fail 원시 보고서는 현재 C PC에 없어 이전 MD 근거로 구분한다. 이번 Build/자동화/수동 Pass는 없다.
- 현재 소스는 선택 시 `ClearChildren`·AutoWrap Label 재생성을 유지한다. Root/기체 선택에는 Esc/패드 Back이 있으나 초기 활성 버튼 포커스·전체 탐색/확인·강조와 실제 패드 전체 흐름은 완료로 확인되지 않았다. 목록 안정화 → 패드 선택 보강 → UI/설정/독립 미션 수동 확인 → Best Lap 저장 → Tutorial 연속 진행 → Story 고도화 순으로 작업 보드를 정리했다.
- 이번 범위는 로컬 MD와 기존 Drone Space 페이지 최신화다. 코드/Content/Production Training/Figma·Trello 카드 변경, 엔진 Build/PIE/맵 재생성·Commit/Push·권한/예약 변경은 수행하지 않는다. Space 반영 결과는 연결 가이드에 기록한다.

## 2026-10-01 후속 — 로비 목록 튐 진단(실제 UI 미수정)

- 사용자 요청은 원인 확인으로 한정했다. Editor 종료 상태에서 실제 FrontEnd BP를 렌더 PIE로 실행하고 진입/선택 후 첫 6프레임의 Widget Geometry를 측정했다. NullRHI는 Geometry를 얻지 못해 불충분으로 제외했다.
- 훈련 진입→Hover 선택 두 단계로 최소 재현했다. 목록 내부 아래 항목이 선택 시 최대 67.508px 이동하며 목록 높이는 50.232px 증가했다(1920×1080 설계 좌표). 선택 간 세 바깥 열은 0px 이동. Story 진입 측정은 0.278px로 큰 튐을 재현하지 못했다.
- 선택 Snapshot마다 `RebuildNativeMissionButtons → ClearChildren`으로 모든 버튼/AutoWrap Label을 재생성한다. 엔진 `STextBlock`의 AutoWrap은 최소 한 프레임 늦게 계산되며, transient PIE Label에만 명시적 폭을 주는 비교에서 0px로 안정화됐다. 스크롤바 공간 확보를 추가해도 0px로 같았다.
- 진단 보고서 `Saved/Automation/LobbyLayoutDiagnosticWrapProbe/index.json`(2026-10-01 02:31:18 UTC): 원래 UI 단계가 실패하므로 전체 Result는 Fail이다. 비교 단계 0px를 실제 수정/전체 Pass로 표기하지 않는다. 진단 테스트는 `Source/Drone/Flow/Tests/Diagnostics/DroneLobbyLayoutStabilityTest.cpp`에 보존하며 로그/Wrap 실험은 해당 검사 안에서만 동작한다.
- 다음 수정안: 같은 목록은 버튼을 재사용해 선택 강조만 변경하고 초기 줄바꿈 폭을 안정화한다. 실제 UI·Content·Production Training·Figma 수정/저장과 Commit/Push는 하지 않았다. MD·Drone Space 현황/테스트에 확인 결과를 반영했다.

## 2026-10-01 후속 — UI 기획안·훈련 분리·설정 추가

- 사용자 첨부 UI 시안을 참고해 기존 이미지 6개·미션 DA·맵을 유지하면서 `시작 → Story 4`, `훈련 → Tutorial 9 / Racing 1`로 분리했다. 로비는 목록/카드/설명 3열, 브리핑은 이미지/목표와 하단 시작, 기체 선택은 상단 상세/역할 도식·하단 가로 카드다. 실제 Mesh 렌더 Preview는 미구현이다.
- Flow의 마지막 로비 Mission ID를 기억해 출격 전 Back·결과 로비 복귀에서 분류를 복원한다. 명시적으로 시작을 누르면 Story 목록으로 전환하며 기존 상태 전환과 Catalog는 유지한다.
- `UDroneSettingsWidget`과 `UDroneAudioSettingsSubsystem`을 추가했다. Master 음량 미리보기/SaveGame, 화면 모드/해상도, 그래픽 품질·VSync·FPS와 적용/기본값/뒤로 취소를 구현했다. PIE/Designer 창·해상도 변경은 차단한다. 설정을 열기만 해서는 저장/덮어쓰기하지 않는다. 음악/SFX/음성 분리는 실제 SoundClass 연결 후속이다.
- 현재 작업컴 MSVC 14.51.36257 Editor Build 성공, UI 집중 `FrontEndContract / BackNavigationContract / MissionEntryContract / SettingsContract / FrontEndPIE` 최종 5/5·자동화 이벤트 오류/경고 0. `Saved/Automation/TrainingLobbySettings/index.json`(02:03:48 UTC)에 저장했다. 엔진 Deprecated API/비선호 컴파일러 Build 경고는 남아 있다. 분류·숨은 선택 거절·Back/결과 복원·음량 범위/NaN·SaveGame 메모리 직렬화와 실제 FrontEnd PIE, Settings 자식 컨트롤 생성·슬라이더/Back Delegate·미리보기 취소를 확인했다.
- NullRHI/NoSound 검사여서 새 화면·실제 가청성·Standalone 창/해상도·디스크 저장 후 재실행·패드 체감은 수동 대기다. 이전 PC 화면 Pass를 새 UI에 적용하지 않는다. Content/맵 저장·Production Training 재생성·Figma 수정·Commit/Push 없음. 관련 MD와 기존 Drone Space Page를 함께 갱신한다.
- 다음은 새 UI/설정 수동 확인 → Best Lap 영구 저장 → Tutorial 진행/재시도/완료 UI → Story 고도화다. Lap SaveGame은 아직 없으며 신규 음량 SaveGame과 구분한다.

## 2026-10-01 Spaces 연동과 Trello 대조

- `Drone 프로젝트` Space를 생성하고 안내·진행/다음 작업·테스트 맵·기획 기준·Blueprint 팀원 가이드 5개 Page에 최신 MD/코드 요약을 저장했다. 중복 진행 파일을 만들지 않고 현재 Page를 갱신하도록 연결했다.
- 사용자 Trello 보드는 API 인증 제한 뒤 기존 Chrome 로그인 세션으로 주요 목록/카드를 읽었다. 담당자별 현재 표시 카드 74개, Gate 4항목 완료 표기와 랩 저장·미션 목표·Chaos·차량 도착·벽/그물·레이싱 3·2·1 후속을 코드 근거와 구분해 진행 Page에 반영했다. 보드/카드를 수정하지 않았다.
- md/drone 저장소 및 현재 대화 폴더에 AGENTS.md를 추가하고 [연동 규칙](../git/DRONE_SPACES_SYNC.md)에 Page ID/링크·갱신 시점·접근 실패 처리·검증 출처·권한 경계를 기록했다. 상시 감시·예약 자동화·Cloud Controller는 활성화하지 않았다.
- Space 루트의 본문/네이티브 Agent Instructions 삽입은 도구 schema 거부로 미적용. 같은 Space의 안내 Page와 로컬 지침으로 대체했고 루트/기존 문서를 삭제하거나 재생성하지 않았다. 실제 Page 본문/부모 배치 확인과 문서 diff 검증만 수행하며 화면 렌더·Build·PIE 재검증으로 주장하지 않는다.
- 코드/자산 변경과 Commit/Push 없음. 새 연결 설정 AGENTS.md와 MD는 로컬 미커밋이며 다른 PC 공유 시 사용자가 함께 Commit/Push한다.

## 2026-10-01 작업컴 최신화 — 원격 수신·검증 출처 정리

- 현재 작업 위치는 Unreal `D:\JGY\project\drone`, 문서 `D:\JGY\project\md`다. 아래 다른 PC의 구현 시점 기록은 수정하지 않고 보존한다.
- Unreal `83b33c1bccf5e9524579001a7688df57e972426b`(09:29:57 KST, `10월스타트 로비랑 ui 전체적정비`), 문서 `aecb6ece1cb7b369a84499e3645098c0cbb8a801`(09:29:39 KST, `10`)을 확인했다. `git ls-remote`로 실제 원격 main과 대조했고 점검 시작 두 Clean·0/0이었다. Unreal은 09:34:51 KST Fast-forward Pull 이력이 있다.
- 최신 커밋의 변경 바이너리 패키지 32개는 모두 존재하며 LFS 포인터가 아닌 본문이다. LFS 업로드 대기·Stash·실행 중인 Editor 없음. 전체 LFS 해시 무결성 검사나 엔진 재빌드의 대체 검사는 아니다.
- `Test-DroneWorkstation.ps1 -RequireClean` 기본 점검은 0 failure / 0 warning, `WORKSTATION_READY`. Build/Validate/PIE/화면/성능은 재실행하지 않았다. Oct 1 `GameReadiness`/`TitleLobbyOrbit` 원시 보고서는 현재 D 드라이브 Saved에 없다.
- 코드 확인: Title PNG 6개·9/1/4 탭·출격 전 Back·독립 Tutorial 8 + Story 4 + Racing 1 기본 Entry·원형 9 Gate 수업·비 Trace 예산/맑은 날 생략이 현재 커밋에 포함됐다. Best Lap은 실행 메모리만 사용하고 영구 저장은 미구현이다.
- STATUS/WORKBOARD/작업컴 시작 가이드·CONTEXT·UI/통합 점검 가이드의 오래된 PC 경로·커밋·미커밋 주장, 공유/독립 맵 진입 설명, Story/차량 미구현 주장과 고정 27m/s 기준을 교정했다. 이전 Build 32/32·Back 33개 실패 0·14맵 점검은 다른 PC의 인계 증거로 명시했다.
- 다음 순서를 FrontEnd/독립 미션 수동 완주·패드 → Best Lap SaveGame → Tutorial 진행 UI → Story 고도화로 통일했다. Gate/Physics/AI/기상 회귀와 Chaos 비교 Spike는 별도 미확인으로 유지한다. Production Training·코드·자산 수정 없이 문서만 갱신하며 Commit/Push는 사용자 담당이다.

## 2026-10-01 후속 — 출격 전 뒤로가기

- Acro의 자세 제한 없는 롤/루프·추력 방향 가속·하강 지원과 실제 기체 응답 검증의 차이를 설명했다. 비행 수치/물리는 이번에 변경하지 않았다.
- FrontEnd 로비/설명, 기체 선택의 Back 버튼과 Widget `NavigateBack`, Esc·패드 Back 입력을 추가했다. Flow에서 선택/Story Fact 수명과 상태를 검증하고 기체 선택의 실제 FrontEnd 맵 복귀는 Mission Controller가 담당한다. 설명→로비에서 미션/탭을 보존하고 로비→시작은 선택을 지운다. 반복 키·비행/로딩/결과의 잘못된 Back은 차단한다.
- Editor Build 성공, `BackNavigationContract`와 실제 버튼 Delegate PIE 포함 33개 실패 0. 1건의 경고는 엔진 외부 연결 확인 HTTP 요청 시간 초과다. computer-use로 1280 화면에서 설명 Back 클릭·레이싱 맵의 기체 선택 Back·FrontEnd 설명/Esc→레이싱 탭 복원/Esc→시작을 확인했다. 패드 실제 기기 입력은 미검증이다.
- [가이드](../gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md)에 BP 버튼 이름·API·동작·검증 범위를 기록했다. Commit/Push하지 않았다.

## 2026-10-01 후속 — 물리/비/UI/독립 미션 점검

- 최종 Editor Build 및 집중 회귀 32/32 Success·테스트 오류/경고 0. 직접 Hover Play PIE의 중복 Mission 등록 실패를 고쳐 출격→3초 유지→Return 전환도 통과했다. Tutorial/Story/Racing/비 비교 시험맵 14개 Map Check 0/0. 1280 상호작용·1920 제목/Exit 수동 관찰과 별도 엔진 `-game` Toolset Python 오류를 구분해 기록했다.

- 실제 코드상 Acro의 추력/중력/항력과 회전 보간, 바람 위치 Drift, 질량 반영 및 미구현 관성/PID/센서/모터별 토크를 구분했다. FPV DA는 현재 4500cm/s × 1.25, BP Override Off임을 확인하고 옛 27m/s 고정 테스트를 현재 데이터 계약으로 수정했다. 기체 수치는 변경하지 않았다.
- OilRig Preview 13,144 Actor/12,710 Mesh Component/25 CPU Niagara System(2 Emitter씩) 확인. Effect Type None·Fixed Bounds Off. 원본을 보존한 비교 맵과 자동 정순/역순 성능 측정을 만들었다. 최종 평균 원본 20.56ms/Off 9.67ms/근거리 8개 10.65ms/프로젝트 비 9.65ms. 한 시점·품질 차이가 있는 비용 비교다.
- Rain은 최초/실내 전환 추적 예산, 무강우 작업 생략, ISM 일괄 갱신으로 보완. 미검사 열은 숨겨 지붕 관통을 방지한다.
- Tutorial 8개 수업별 맵 및 DA MissionMap 연결, Story/Racing 포함 13개 직접 Play 기본 Entry. 기존 공유 맵/Production Training은 보존했다. Python Rotator는 명명 인자로 수정했다.
- 제공 시안의 Start/Training/Setting/Exit 배치와 그래픽 Setting·돌아가기, Hover/Pressed/음원 교체 슬롯, 실제 목록/썸네일/탭 반응을 확인했다. 음원·최종 애니메이션을 지급받아 연결한 상태는 아니다.
- Map Check와 최종 테스트 보고서/수동 화면 범위는 [통합 점검 가이드](../gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md)에 기록한다. Commit/Push하지 않았다.

이 문서는 Drone 개발의 **진행 이력**을 시간순으로 남긴다. 가장 최신의 현재 상태는 [`../WORKBOARD.md`](../../WORKBOARD.md), 확정 구현 순서는 [`DRONE_TUTORIAL_STORY_PLAN.md`](../planning/DRONE_TUTORIAL_STORY_PLAN.md)를 따른다.

## 갱신 규칙

Drone 코드·자산·계획 작업을 진행할 때마다 작업 종료 전에 Markdown을 함께 갱신한다.

1. `WORKBOARD.md`: 현재 단계, 지금 작업 중인 카드, 완료 근거, 남은 조건과 바로 다음 작업
2. `DRONE_WORKLOG.md`: 실제 변경, 검증 결과, 발견한 문제와 다음 행동을 날짜순으로 추가
3. `STATUS.md`: 빌드·테스트·자산 수처럼 검증된 기준선이 달라졌을 때 갱신
4. `CONTEXT.md`: 사용자가 확정한 방향, 장기 규칙과 범위가 달라졌을 때 갱신
5. 계획 문서: 구현 순서, 완료 조건이나 설계가 달라졌을 때 같은 작업에서 갱신

진행률은 근거 없는 전체 백분율로 표시하지 않는다. 대신 `현재 단계`, `통과한 게이트/전체 게이트`, `Doing`, `다음 활성 카드`로 기록한다. 자동화가 통과해도 필수 수동 확인이 남아 있으면 완료로 이동하지 않는다.

## 현재 상태 참조

최신 상태는 [STATUS](../../STATUS.md), 순서는 [WORKBOARD](../../WORKBOARD.md)를 따른다. 기존 스냅샷은 [10월 아카이브](archive/STATUS_2026-10.md)에 원문 보존했다.

## 2026-10-01 — Title 이미지·3탭 로비·원형 비행 정정

- 사용자 제공 Title_Asset의 PNG 6개를 `/Game/Drone/FrontEnd/Textures/Title`에 가져오고 WBP Class Defaults의 교체 슬롯에 연결했다. 배경·로고·버튼 원본 파일과 Figma는 수정하지 않았다.
- 로비를 Tutorial/Racing/Mission으로 구분해 실제 목록·선택 강조·썸네일·스크롤을 연결했다. 숨겨진 탭 선택은 시작할 수 없다. Tutorial 9 / Racing 1 / Story 4 = Catalog 14개다.
- 회전은 제자리 방향 정렬이 아닌 원형 코스 비행이라는 사용자 정정을 반영했다. Heading 자산/ID는 유지하고 Lap→귀환으로 규칙을 바꿨으며 기존 Owned Heading Zone/Pad만 제거하고 Orbit Course를 추가했다. 수동 Hover/기타 배치는 보존했다.
- 9개 Gate는 시작+체크포인트 7개+결승이다. 결승을 전체 Spline 길이에 두어 7/8 바퀴에 성공하지 않으며 시작과 겹치지 않게 결승만 2.5m 분리했다.
- 다른 Course가 먼저 발견되는 문제를 막기 위해 Director/HUD가 Tag에 맞는 같은 Recorder를 읽고 다른 코스를 끈다. Native `CircularCourse` 자동화는 역순·역방향·제자리 회전·다른 코스·미완주·Lap→귀환을 검증한다.
- 별도 `Lvl_DroneRacingTest`, `DA_Mission_Racing_Circuit_Test`를 만들었다. 정식 경기 규칙/영구 Best Lap은 이번 범위가 아니다. Story 맵 분리는 유지하고 튜토리얼 전체 맵 분리는 사용자 검토 단계로 남겼다.
- Editor Build 성공(MSVC 14.51.36256). 두 시험맵 Map Check 0 errors / 0 warnings. 첫 집중 회귀는 9/10 성공했고 새 Racing ID가 빠진 기존 목록 기대값 하나를 수정했다. 최종 집중 회귀는 Flow 5개, Mission 2개, Acro Input 1개, Tutorial/Hover/Gate 6개, 총 14/14 Success(오류/경고 0), Exit 0이다. 보고서 `drone/Saved/Automation/TitleLobbyOrbit/index.json`, 2026-10-01 01:47:42 KST. Build에는 엔진 Deprecated API와 비선호 최신 MSVC 경고가 남으며 프로젝트 신규 컴파일 오류는 없다.
- `GateAssetVisual`의 미지정 선택 슬롯이 Map Check에 Null Mesh 경고를 만들지 않도록 숨겨진 안전 Mesh만 할당했다. 미지정일 때 외형은 계속 숨기고 최종 Gate Mesh 지정 기능은 유지한다.
- Mode 1/2는 스틱 배치, Angle/Acro는 비행 제어 방식이라고 DJI/Betaflight 공식 자료와 현재 코드로 구분했다. 단순화 물리를 실제 FC/PID 1:1 모델로 표현하지 않으며 이번에 물리 수치는 임의 변경하지 않았다.
- [시작 화면·BP 이미지·탭·원형·맵 분리 가이드](../gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md)와 작업컴/현재 상태를 갱신했다. 실제 UI 배치·원형 비행 체감은 수동 확인 대기. Commit/Push 없음.

## 2026-10-01 — 원격 기준선과 작업컴 인계 최신화

- 두 저장소에서 `git fetch origin --prune`을 다시 실행했다. Unreal은 `3b77aef`, 문서는 `1ffe3b2`로 각각 `HEAD...origin/main = 0/0`이다.
- Unreal 작업 트리는 Clean이고 `git lfs status`의 Push·Commit·Staging 대기 목록도 비어 있다. Bangkok City·OilRig Preview 맵과 ThirdParty 의존 자산은 2026-09-30 원격 Commit에 포함됐다.
- `STATUS.md`, `WORKBOARD.md`, `WORK_PC_START_HERE.md`의 예전 Commit ID와 로컬 미커밋 표현을 실제 원격 상태로 교정했다. 이번 문서 최신화는 사용자 지시에 따라 Commit·Push하지 않는다.

## 2026-09-30 — 공급 광섬유 통 GSU 적용

- `C:\Users\Metacon_41\Downloads\새 폴더\광섬유`의 `GSU.fbx`와 BaseColor·Emissive·Normal·ORM Texture를 확인했다. 원본 FBX를 렌더링한 결과 전체 Drone이 아니라 세로형 광섬유 통/카트리지 Mesh임을 확인해 전용 통 슬롯에 장착했다. 후속 사용자 지정에 따라 기체 본체는 기존 FPV 외형 대신 프로젝트의 `DroneSpy` Body·분리 Rotor 4개를 사용한다.
- `/Game/Drone/ThirdParty/FiberOpticGSU`에 `SM_FiberOpticGSU`, `M_FiberOpticGSU`, Texture 4개를 프로젝트 소유 자산으로 가져왔다. Material은 BaseColor, Normal, ORM의 R=AO/G=Roughness/B=Metallic, Emissive를 연결했다.
- `BP_DroneFiberOpticIntegration`은 `SM_Drone01Body + SM_Drone01_r1~r4`와 Scout에서 검증한 배치값을 재사용해 Rotor 회전을 유지한다. `FiberSpoolMeshComponent`에 GSU를 약 28cm 높이로 축소해 중심 `(-24,0,-16)cm` 부근에 배치했고 Collision·Overlap·Navigation은 끈 상태다.
- 광섬유 Spline 출발점은 기존 임시 Offset 대신 GSU 통 상단 노즐 위치를 사용한다. 재밍 면역, 충돌 자폭, 1인칭 기본값, 지면 누적 케이블 로직은 변경하지 않았다.
- `DA_Drone_FiberOptic_Greybox`의 표시명·설명은 실제 광섬유 자폭 Drone 기준으로 정리했다. Preview는 복합 Component 전체를 담을 수 없는 단일 Mesh 슬롯이므로 DroneSpy Body를 사용한다.
- `ImportDroneFiberOpticGSU.py`와 실행 도구를 추가하고 `BuildDroneExtendedRoles.py`도 같은 통 Mesh·Transform·케이블 출구를 재생성하도록 갱신했다. 추후 Extended Role 재생성 시 새 통이 사라지지 않는다.
- DroneSpy 교체 후 MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `Drone.Integration.ExtendedRoleDrones` 1/1 Success, 자동화 오류·경고 0. 새 `.uasset` 6개는 모두 Git LFS 대상이다.
- 남은 수동 확인은 기체 하부에서 통이 본체/카메라와 겹치지 않는지, 회전 날개가 유지되는지, 통 상단부터 케이블이 자연스럽게 풀리는지다. 크기와 위치가 어색하면 Fiber BP의 `FiberSpoolMeshComponent` Transform만 조정한다.

## 2026-09-30 — 벽·그물 접촉 카메라 안정화(총알 피격 유지)

- 사용자 피드백은 벽/그물 접촉 화면이 피격처럼 덜컥거리는 문제이며, 후속 확인에서 **총알 피격 화면 흔들림은 제거하지 않는다**고 범위를 확정했다.
- 실제 Hit/Net 진입점을 사용하는 `Drone.Physics.ContactSmoothing`을 먼저 실행해 벽 순간 위치/Root 회전, 그물 피해 Shake Event 0→1과 즉시 속도 절단을 Red로 재현했다. 추가 Camera 검사에서는 그물 Camera Block, FPV 본체 기울기 상속과 Additive Shake 경로도 분리해 검사했다.
- 같은 벽 접촉이 계속되는 동안은 재충격·Point Damage·자세 Pulse를 재생하지 않고 새 안쪽 입력만 바깥으로 제약한다. 0.18초 해제 여유 뒤 새 충돌은 다시 반응한다. 반발 속도 비례는 유지하고 표면 분리는 기본 0.12초 Sweep 보간, 작은 본체 기울기는 0.35초 Pulse/0.10초 보간으로 적용한다.
- 그물 접촉의 `TriggerDamageShakeGreybox` 호출과 반복 속도 배율 절단·위상 재시작을 제거했다. Severity를 기본 0.25초로 보간해 감속·조종/추력 저하·하강을 적용하고 포획/자동 해제/비절단 규칙은 유지한다. Root 회전 대신 기본 3°/0.35Hz 완만한 외형 기울기를 사용한다.
- `CameraFlightPivot`은 조작 자세와 실제 피격 기울기를 따르되 벽/그물 외형 기울기는 제외한다. 카메라 이동 보간은 기본 추종속도 18, FPV 최대 지연 20cm/3인칭 100cm로 제한한다. 의도한 회전, 실제 이동, 마우스 조작과 총알 `DamageShake`의 Camera Additive Offset/FOV 복원 계약은 유지한다.
- Net Strand는 Camera 채널만 기본 Ignore/Pawn Block 유지다. 저장 BP/맵도 BeginPlay에서 적용하며 카메라 암이 줄마다 수축/복귀하지 않게 한다. 일반 벽의 Camera 충돌은 끄지 않았다. 조정값은 BP Class Defaults/CollisionResponseComponent/Net Actor에 노출했다.
- 최종 MSVC 14.51.36257 Editor Build 성공. `Drone.Physics` 4/4·`Drone.Prototype` 8/8·`Drone.Mission.StoryPhysicsTestMaps` 1/1, 총 13 Success(자동화 오류/경고 0). Prototype/FPV/Fiber/UGV/Physics Pawn/Net BP 6개 메모리 Compile 오류·경고 0. 보고서: `drone/Saved/Automation/ContactCameraIsolation/index.json`, 2026-09-30 03:26:32 UTC.
- 엔진 헤더 Deprecated API와 비선호 MSVC 경고는 기존 Build 환경 경고이며 자동화 이벤트 0과 구분한다. 실제 렌더 화면의 부드러움은 아직 수동 확인하지 않았다. Production Training/Content 자산 저장, Commit·Push, Unreal MCP 호출 없음. 기존 미커밋 변경 전부 보존.
- 다음: `Lvl_DronePhysicsSandbox`에서 P로 1/3인칭 전환 후 저속/고속/지속 벽 입력과 그물 접촉, `Lvl_DroneShotgunSystemsTest` 또는 NPC 맵에서 실제 피격 Shake 유지 확인.

## 2026-09-30 — Gate 통과음·하단 1/6 위치·독립 스케일·상태 재질

- 사용자 Trello 요청을 구체화해 통과 판정 성공에만 음성/Sound를 출력하는 BP 슬롯을 추가했다. SoundWave/SoundCue, 볼륨·피치·2D/공간 재생을 지원하고 기본 음원은 지정하지 않았다. `OnGatePassed`는 판정 로직과 별개인 자막/연출 확장 지점이다.
- 기존 코드는 `Color`만 갱신했으므로 세 상태 **머티리얼 지정 슬롯**은 없었다. `InactiveMaterial`, `CurrentMaterial`, `CompletedMaterial`을 추가하고 빈 상태는 공통 `RingMaterial`로 fallback한다. 색상 파라미터 이름도 BP로 조절하며, 파라미터가 없는 재질은 재질 자체 교체만 적용한다.
- 기존 공통/개별 위치 Offset과 Gate Scale이 이미 선과 분리돼 있음을 확인했다. 사용자 요구에 맞춰 `AutomaticGateSplineHeightFraction` 기본 1/6을 추가해 Spline은 그대로 두고 Gate 중심을 올린다. 공통 Gate Scale과 새 Index별 배율을 함께 적용하며 선 폭·두께·제어점·Course Transform은 건드리지 않는다.
- 기존 저장 Child의 Transform을 BeginPlay 때 새 높이로 갱신해 중심 위치로 저장된 이전 맵도 플레이 시작부터 새 규칙을 사용하게 했다. 수동 `OrderedGates`는 자동 이동하지 않는다.
- 전체 Gate 에셋용 `GateAssetVisual` Component와 `GateAssetMesh`, Pivot/회전/크기 보정, Material Slot 선택을 추가했다. 원래 16개 Component 이름은 보존하고 완성형 메시가 있으면 임시 네 변을 숨긴다. 선택하지 않은 슬롯은 원본 재질을 유지한다. Visual은 계속 비충돌이고 Box/aperture 판정은 그대로다.
- MSVC 14.51.36257 Editor Build 성공. 첫 회귀는 Course/Gate Presentation/Gate Sequence/Lap Recorder/Route Selector/Route 저장 계약/Route 실제 키 PIE 7/7 Success다. 새 시험 World 종료에서 Child 정리 경고 3건을 발견해 Context 제거 전에 Course를 정상 종료하도록 시험 수명을 보강했고 실제 Gate/Course BP Compile 검증을 추가했다. 최종 결과는 아래에 기록한다.
- 최종 수정 후 Editor Build 성공, 위 7개와 `TrainingGateBlueprint`까지 8/8 Success(자동화 이벤트 오류·경고 0). Gate/Course BP 메모리 Compile은 각각 0/0이며 패키지는 저장하지 않았다. `TrainingGatePresentation`은 실제 World에서 기본/확대 Gate의 1/6 높이, 개별 배율, 선 크기/제어점 불변, 저장 중심 배치의 BeginPlay 복구, 전체 메시 교체/복구, 세 상태 재질/색과 미지정 슬롯 보존, 정상 통과 피드백 단발·실패/Reset 무음을 검사한다. 실제 음원 데이터의 가청성은 자동화로 주장하지 않는다.
- 팀원 Production Training과 Content Asset은 저장하지 않았다. 실제 음원과 Gate Mesh 지정은 사용자/팀원 작업이며, 가청성·최종 외형은 수동 확인으로 남긴다. Guide/STATUS/WORKBOARD/CONTEXT를 함께 갱신하고 Commit·Push는 하지 않았다.

## 2026-09-30 — 일반 벽 반발·그물 얽힘/포획 v1

- 작업 시작 전에 Unreal `main=origin/main=494dde2`, 문서 `main=origin/main=44662f9`와 두 Clean 작업 트리를 확인했다. 사용자가 어제 이후 추가 작업이 없다고 확인했으며 오래된 GitHub Desktop Stash는 복원 대상으로 사용하지 않았다.
- `UDroneCollisionResponseComponent`를 전용 Physics Pawn 기능에서 일반 비행 `ADronePrototypePawn` 공통 규칙으로 전환했다. 초기안은 수평에 가까운 Blocking 벽·기둥·구조물에 Hit Normal 반사와 고정 최소 반발/이격을 적용했고 바닥·천장·Ground UGV는 제외했다. 아래 화면 피드백 교정에서 고정 반발/이격을 속도 비례식으로 대체했다.
- 사용자 화면 기준과 다른 원인을 자동화로 재현했다. 기존 구현은 `120cm/s` 미만 접촉을 버리고, 약한 접촉에도 최소 `90cm/s` 반발과 고정 `6cm` 위치 이동을 줘 속도와 무관한 이진 Bounce처럼 보였다. `20cm/s < 80cm/s` 반발이어야 한다는 회귀는 수정 전 Fail, 수정 후 Success다.
- 반발 계산을 접선 속도는 유지하고 법선 반발만 충돌 속도에 비례하도록 바꿨다. 기본 반발 계수는 강한 충돌도 분명히 느껴지도록 `0.55`, 표면 분리 거리는 `0.25~6cm`, 자세 Kick은 `0~12°` 범위에서 속도에 비례한다. 직전 비행속도를 보존해 Movement가 충돌 직후 속도를 0/Slide로 바꾼 경우에도 실제 입사 속도를 잃지 않는다.
- Collision Root보다 바깥의 네 기본 Local Offset `(±95, ±95, 0)cm`를 Sphere Sweep하는 Wing/Rotor Probe를 추가했다. 벽 모서리와 그물을 먼저 감지하고 접촉 위치·벽 법선으로 기체를 벽 바깥쪽으로 기울인다. Probe Offset·Radius·Channel·회전 Kick 수치는 Blueprint Component Defaults에서 기체별 조정 가능하다.
- `ADroneNetPlacementRig`의 일반 Drone 충돌은 기본 절단 Off로 바꿨다. FloatingPawnMovement의 실제 속도를 읽어 공통 Collision Response Component에 전달하며, 탄환·폭발 Point Damage 또는 명시적 `Break On Impact`에서만 기존 국소 절단/물리 조각 진단을 사용한다.
- Net Entanglement 상태는 접촉 속도와 반복 접촉으로 Severity를 누적한다. 즉시 속도 손실, 이동/Yaw/Acro Body Rate·추력 반응 저하, 수평 감쇠, 상승 제한, 하강 가속도와 Pitch/Roll/Yaw 교란을 적용하며 임계값 이상은 Captured로 판정한다. 기본 자동 해제 뒤 조종 비율을 1.0으로 복구한다.
- 최소 접촉 속도, 즉시 포획 기준 속도, 지속시간, 포획 임계값, 최소 조종 비율, 수평 감쇠, 하강 가속도, 최대 상승속도, 자세 교란, 자동 해제와 접촉 누적 Cooldown은 Blueprint Component Defaults에서 조절 가능하다.
- 첫 자동화 확장에서는 Net Hit Delegate 시험이 FloatingPawnMovement 속도가 아닌 Primitive 속도를 읽는 결함을 드러냈다. Pawn Movement Velocity를 우선하도록 고치고 실제 Hit Delegate와 자동화가 공유하는 `ApplyDroneImpact` 경로로 정리했다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `Drone.Physics.Breakables`와 속도 비례 Red→Green을 포함한 `Drone.Physics.CollisionResponse` 2/2가 최종 Success다. 실제 Test World에서 Root Sphere가 벽에 닿지 않은 상태로 날개 Probe만 저속 20cm/s·고속 600cm/s 벽 접촉을 만들고, 두 경우 모두 바깥 반발·자세 Kick이 생기며 고속 반발이 더 큰 것도 검사한다. 변경 영향 `Drone.Prototype` 8/8과 `Drone.Mission.StoryPhysicsTestMaps` 1/1도 Success다. 저장 맵·Asset은 수정하지 않았다.
- 저장 맵과 Production Training은 수정하지 않았다. 수동 확인은 `/Game/Drone/Maps/TestMap/Lvl_DronePhysicsSandbox`에서 정면/비스듬한 벽 접촉, 저속/고속 그물 접촉, 포획·하강·자동 해제 후 조종 복구 순서로 진행한다.

## 2026-09-29 — Physics Sandbox 국소 절단·조각 파괴 기준 확장

### 화면 피드백 후 교정

- 사용자 화면에서 그물 약 13×12m와 파괴 벽 약 12.8×9.2m가 Drone 대비 과도하게 크고, 충돌해도 파괴 변화가 보이지 않는 문제를 재현했다. 이를 완료 상태로 보지 않고 결함으로 분류했다.
- 자동화 Red에서 그물 폭·높이 상한 위반과 실제 `ADronePrototypePawn::OnActorHit`가 Breakable Wall을 깨지 못하는 것을 확인했다. 원인은 `UDroneCollisionResponseComponent`가 Drone 속도 반사만 하고 `OtherActor`에 Damage를 전달하지 않은 것이었다.
- 전용 Physics Drone의 유효 충돌이 같은 `FHitResult`와 입사 방향으로 Point Damage를 전달하도록 수정했다. 이 설정은 Component의 Blueprint 값으로 켜고 끌 수 있고 기존 Production Drone 기본 반응은 바꾸지 않는다.
- 그물 기본값을 6×3m·처짐 70cm·굵기 2.2cm, 파괴 벽을 6×4 조각·약 5.55×3.69m로 축소했다. 두 대상의 기본 국소 파괴 최소 속도는 250cm/s다.
- 끊어진 그물 Segment를 즉시 숨기기만 하던 동작도 보강했다. 충돌 주변 신규 파괴 Segment 중 최대 16개를 Rigid Body Component로 바꿔 충돌 방향·무작위 회전·중력을 적용하고 기본 5초 뒤 정리한다. Blueprint에서 생성 On/Off, Impulse, Random Impulse, Lifetime, 최대 조각 수를 조정하며 Reset은 파편까지 즉시 제거한다.
- 시험맵 배치 간격과 고정 벽도 축소해 Drone→벽→그물→파괴 벽을 한 화면 흐름으로 시험할 수 있게 다시 저장했다. Physics Map Check는 `0 errors / 0 warnings`다.
- 수정 후 `Drone.Physics.Breakables`, `Drone.Physics.CollisionResponse` 2/2와 저장된 맵의 Blueprint 크기 상한까지 검사하는 `Drone.Mission.StoryPhysicsTestMaps` 1/1이 경고·오류 없이 성공했다. Net 자동화는 물리 조각 생성과 Reset 정리도 검사한다. 실제 Cloth/Geometry Collection 자산은 여전히 0개이며 다음 수동 화면 확인 뒤 별도 Spike에서 비교한다.

### 사용자 의도 재확정

- 그물은 파괴 효과용 오브젝트가 아니라 Drone 날개·Rotor가 엉켜 비행을 방해하는 장애물이다. 최종 반응은 감속·추력 저하·Roll/Yaw 교란 뒤 탈출 또는 Snared/Entangled·Crash이며, 현재 국소 절단·떨어지는 Segment는 충돌 위치와 물리 반응을 확인하는 진단 기능으로만 판정한다.
- Cloth Solver 결과를 Mission 판정에 직접 쓰지 않고, Collision Root와 가벼운 Wing/Rotor Contact Probe 또는 Net Interaction Volume의 접촉 누적 상태가 포획·탈출·추락을 결정하도록 설계 기준을 고정했다.
- 벽 반발은 Sandbox의 지정 Cube 전용이 아니라 모든 일반 Blocking 벽·기둥·구조물에 적용할 비행 공통 규칙이다. 현재 Component는 전용 시험 Pawn에서만 활성화되어 있으므로 일반 Flight Pawn 적용, Landing 표면 분리, 강한 Crash 우선순위, 연속 접촉 비비기와 얇은 벽 Sweep 검증을 후속 카드로 남겼다.

- `ADroneNetPlacementRig`을 전체 숨김 전용 Greybox에서 충돌/Point Damage 위치 반경의 Strand Segment만 제거하는 구조로 확장했다. 전체 제거 API는 비교용으로 유지하고 Reset에서 전부 복구한다.
- `ADroneBreakableWallPanel`과 `BP_DroneBreakableWallPanel`을 추가했다. 온전한 벽은 ISM 격자로 유지하고 맞은 조각만 물리 Static Mesh Component로 전환한다.
- Physics Sandbox에 Breakable Wall을 추가했고 Map Check `0 errors / 0 warnings`를 확인했다.
- `Dataflow`, `GeometryCollectionPlugin`, `ChaosClothAsset`, `ChaosClothAssetEditorCore(Editor)`를 `Drone.uproject`에 명시 활성화했다. Deprecated Cloth Editor는 활성화하지 않았다.
- TDD Red→Green으로 `Drone.Physics.Breakables`를 추가했고 `Drone.Physics.CollisionResponse`, `Drone.Mission.StoryPhysicsTestMaps` 회귀와 `DroneEditor Win64 Development` 빌드가 성공했다.
- 실제 Cloth/Geometry Collection 생산 자산은 아직 0개다. 다음은 화면에서 절단 반경·파편 Impulse·복구를 확인한 뒤 같은 Sandbox의 별도 구역에 실제 자산을 배치해 비교한다.

## 2026-09-29 — Training Route 4개·숫자키/무작위 선택 TestMap

- Production `Lvl_DroneTraining`을 건드리지 않고 `/Game/Drone/Maps/TestMap/Lvl_DroneTrainingRouteSelectionTest`를 새로 만들었다.
- 직선, 좌측 곡선, 우측 곡선, 상승·하강 슬라럼의 편집 가능한 Course 4개를 배치하고 각 Route에 자동 Gate 5개와 고유 Course ID를 부여했다.
- `ADroneTrainingRouteSelector`가 `1~4` 고정 Route와 `5` 무작위 Route를 단독 처리한다. 선택하지 않은 Course 선·Gate Trigger를 끄며, 전환 시 Gate Sequence와 부분 Lap을 초기화한다. Route가 둘 이상이면 무작위 선택은 현재 Route를 즉시 반복하지 않는다.
- Prototype PlayerController는 Route 변경 Event를 구독해 Flight HUD의 Lap Recorder Source를 활성 Course로 교체한다.
- 공개 API 계약은 미구현 상태에서 Red를 확인한 뒤 Green으로 전환했다. 저장 맵 계약도 맵 부재 Red 뒤 생성해 Green으로 전환했다.
- Editor Build, Map Check 0/0, 선택기·저장 맵·실제 `1~5` 키 PIE와 기존 Course/Gate Sequence/Lap Recorder 회귀가 모두 성공했다. Commit·Push는 수행하지 않았다.

## 2026-09-29 — Physics Sandbox·Story Mission별 TestMap 4개·Hover 실제 PIE

- 팀원이 제작 중인 Production `/Game/Drone/Maps/Lvl_DroneTraining`은 열거나 저장하지 않고, 물리 1개와 Story 4개 시험맵을 전부 `/Game/Drone/Maps/TestMap`에 격리했다.
- `Lvl_DronePhysicsSandbox`에 시험 전용 벽 충돌 반발 Drone, 벽 2개, 네 Corner 좌표·줄 수·분할·처짐·굵기를 Blueprint에서 바꾸는 절차형 그물 Greybox를 배치했다. 피해 임계값 뒤 숨김/Collision 해제와 Reset을 지원한다.
- 충돌 반발은 기존 Drone 기본값에서 꺼진 Component로 추가해 Production 동작을 바꾸지 않았다. 시험 Pawn만 켜며 반발 계수·최소 분리 속도·최대 응답 속도를 Blueprint에서 조절한다.
- Story Test 4개는 Golden Time의 Drop 전달→귀환, Intercept의 Spline 차량 표적 파괴·목적지 실패, Veil Breaker의 재밍 이탈→귀환, Endgame의 UGV 표적 3개 파괴→귀환을 최소 Objective로 연결했다. FrontEnd Catalog는 총 13개가 됐다.
- `Drone.Tutorial.HoverMissionPIE`가 FrontEnd Mission 선택, Scout Spawn, Hover Zone 진입, 실제 3초 안정 Hover, Return 목표 전환을 통과했다. 보이지 않던 Hover 영역에는 Collision 없는 모서리 표식 4개를 추가했다.
- `DroneEditor Win64 Development` Build, 새 5개 맵 Map Check 0/0, `Drone.Physics.CollisionResponse`, `Drone.Mission.StoryPhysicsTestMaps`, `Drone.Tutorial.HoverMissionPIE`, `Drone.Tutorial.MissionLessonsTestMap`, Flow/FrontEnd 계약 자동화가 성공했다.
- 현재 그물은 실제 Dataflow/Chaos Cloth 절단이 아닌 빠른 비교용 Greybox다. 실제 부분 고정 Cloth와 Geometry Collection 벽 파괴는 수동 체감 확인 뒤 별도 Spike에서 진행한다.
- 실행법과 미구현 범위는 [`DRONE_STORY_PHYSICS_TEST_MAP_GUIDE.md`](../gameplay/DRONE_STORY_PHYSICS_TEST_MAP_GUIDE.md)에 기록했다. Unreal·문서 변경은 로컬 미커밋이며 Commit·Push하지 않았다.

## 2026-09-29 — Tutorial 로드 복구와 후속 개발 순서 확정

- 작업컴의 C++ Source는 9월 29일 `7ad9a23`이지만 `UnrealEditor-Drone.dll`은 9월 23일 빌드라 신규 Mission/Heading/Hover 부모 클래스가 없었다. 이 때문에 Blueprint 부모 로드 실패 뒤 맵 Actor의 `SceneRoot`, `TargetCollision`, `HeadingBox` 등이 연쇄 `CreateExport` 오류를 냈다.
- Editor를 저장하지 않고 종료한 뒤 MSVC 14.51.36257로 `DroneEditor Win64 Development` 전체 빌드를 성공했다. 새 DLL에 네 신규 클래스가 포함됐고 Tutorial Validate는 Mission 8개·Map Check 0/0·`VALIDATION_OK`, 새 로그의 `CreateExport` 실패 0건이다.
- `Lvl_DroneTutorialMissionTest`를 직접 Play했을 때 자유 카메라가 뜬 원인은 Flow 상태가 `Boot(0)`인 채 Mission GameMode의 의도된 Spectator로 시작했기 때문이다. 전체 판정은 FrontEnd에서 수업 선택→맵 진입→Drone 선택 경로로 시험하며, 직접 Drone 조작은 `Lvl_DroneTutorialSystemsTest`를 사용한다.
- Lap Recorder의 이전 평균·Best 비교는 현재 실행 메모리에만 있고 `USaveGame`은 없음을 다시 확인했다. 다음 구현은 조건이 다른 기록을 섞지 않는 `CourseId + DroneId + ControlMode + HandlingPreset` 키의 Best Lap 최소 저장으로 확정했다.
- 이후 순서는 Tutorial 8개 수동 확인 → Best Lap 영구 저장 → 단계별 결과·8개 진행/전체 완료 UI → Warehouse Greybox → Mission 1 → Mission 2 차량 Route/도착 판정 → Mission 3 광섬유/UGV 교대다. 차량은 Spline이 연속 주행을, Smart Object가 정차/도착 Slot을 맡고 Actor Tag Trigger가 Mission별 성공·실패를 결정한다.
- 이미지에 정리된 Drone 벽면/날개 충돌 반대 반응, 그물 4점 배치, Dataflow/Chaos 부분 고정 그물과 파괴 시험은 Story 기반 뒤 별도 Physics Sandbox 카드로 보존했다. Unreal 코드·맵·자산은 이번 계획 정리에서 추가 변경하지 않았다.

## 2026-09-29 — 원격 기준선과 작업컴 인계 상태 재확인

- `D:\JGY\project\drone`과 `D:\JGY\project\md`에서 `git fetch --all --prune`을 실행했다. Unreal은 `7ad9a23`, 문서는 `578304f`로 각각 `origin/main`과 `0/0` 일치했고 확인 시작 시 두 작업 트리 모두 Clean이었다.
- Unreal `7ad9a23`에는 Tutorial 8개 Mission·공유 시험맵·UGV 총/유탄·Mission Framework가, 문서 `578304f`에는 작업컴 인계와 Tutorial/Mission 가이드가 포함돼 있어 이전의 `로컬 미커밋` 차단은 해소됐다.
- 보조 원격 `yook34/main=c845430`은 중앙 `main`보다 57 Commit 뒤이고 고유 Commit은 0개다. 팀 공유 기준은 계속 `origin/main`이다.
- 다음 순서는 작업컴 Pull·LFS·`WORKSTATION_READY` 확인, FrontEnd Tutorial 8개 수동 플레이, 클리어 타임·연속 진행·전체 완료 UI, Warehouse Greybox, Mission 1 Story Vertical Slice다.
- Unreal 코드·자산·맵은 변경하지 않았다. 현재 상태 문서만 정정했으며 Commit·Push는 수행하지 않는다.

## 2026-09-29 — Tutorial 8개 Mission 시험장과 작업컴 인계 마감

- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialMissionTest`에 Hover, Forward, Heading, Gate Flight, FPV, Payload, UGV NPC, UGV Turret Station과 공용 Return Zone을 구성했다. 각 수업은 독립 Mission Definition과 허용 기체를 사용한다.
- `ADroneTutorialHeadingZone`은 목표 World Yaw의 최단 각도 차이와 유지 시간을 검사하고 Overlap 중 0.1초 Timer만 사용한다. 기본은 동쪽 90°±8°, 1초 유지다.
- Ground UGV에 별도 `GroundWeapons` Capability, `UDroneGroundWeaponComponent`, 직사/반경 모드 `ADronePlayerProjectile`을 연결했다. 좌클릭 총은 25 피해, 우클릭 유탄은 100 반경 피해의 Greybox 기본값이다.
- FrontEnd 기본 Catalog는 기존 Training과 독립 Tutorial 8개, 총 9개 Mission을 노출한다. Production `/Game/Drone/Maps/Lvl_DroneTraining`은 열거나 저장하지 않았다.
- `DroneEditor Win64 Development` Build, Tutorial TestMap Rebuild/Validate와 Map Check 0/0, 신규 집중 회귀 9/9를 통과했다. 전체 `Drone.*`는 51개 성공과 기존 맵 개수·Shotgun 표적 감지·보호 중 Training 기대값 관련 7개 실패다.
- `WORK_PC_START_HERE.md`와 `tools/work-pc/Test-DroneWorkstation.ps1`을 추가했다. 작업컴에서 두 저장소 동기화, LFS 본문, UE 5.8 경로, 필수 Mission Asset, 선택적 LFS fsck·Build·Map Validate를 한 명령으로 확인한다.
- Windows PowerShell 5.1이 UTF-8 BOM 없는 Tutorial 검증 래퍼의 한글 정규식을 잘못 읽는 문제를 실제 전체 실행에서 발견했다. Map Check 요약의 지역화 단어를 Unicode 코드 포인트로 구성하는 ASCII 안전 파서로 교체했고, 같은 `powershell.exe -ExecutionPolicy Bypass` 경로에서 Build 성공·LFS fsck·Map Check 0/0·8개 Mission 검증과 최종 `WORKSTATION_READY`를 확인했다.
- 새 `.uasset`·`.umap` 20개는 모두 `.gitattributes`의 `filter=lfs` 적용을 확인했다. 두 저장소 `git diff --check`도 공백 오류 없이 통과했고 Unreal Editor/명령줄 Editor 프로세스는 종료 상태다.
- 이 마감 시점에는 두 저장소 변경이 로컬 미커밋이었고 Codex는 Commit·Push하지 않았다. 이후 사용자가 Push를 완료했으며 현재 원격 기준은 바로 위 `원격 기준선과 작업컴 인계 상태 재확인` 절을 따른다.

## 2026-09-17 — 개인화기 추적·리시 포기·NPC 회전 안정화 마감

- 같은 Shotgun 병사만 제자리에서 Yaw가 왕복하던 화면 증상을 Rifle과 비교했다. Shotgun은 짧은 사거리 때문에 추적 상태에 들어갔고, 0.35초마다 거의 같은 목적지로 `MoveToLocation`을 다시 발행해 이동/회전을 계속 초기화하는 것이 핵심 원인이었다. 최소 상태 보장시간 자체가 원인은 아니었다.
- `FDroneNPCEngagementPolicy`를 분리해 `Fire / Pursue / Disengage` 결정을 테스트 가능하게 만들었다. 개인화기 사거리 밖에서는 공중 표적을 NavMesh로 투영해 추적하고, 진행 중 목적지가 기본 150cm 이상 바뀐 경우에만 MoveTo를 갱신한다.
- 후속 화면 확인에서 사거리 경계가 애매할 때 다시 왕복하는 증상을 재현했다. 1,590↔1,610cm 반복 입력에서 기존 단일 1,600cm 경계가 Fire/Pursue를 5회 뒤집는 Red를 만들었다. 공간 Hysteresis는 사거리 안에서도 계속 접근하거나 사거리 밖에서 멈추는 구간을 만들므로 최종 폐기했다. 무기 Component와 같은 3D 실제 사거리 안이면 즉시 정지·Fire, 밖 판정이 기본 0.2초 지속될 때만 Pursue한다. 짧은 경계 노이즈는 시간 확인으로 거르고 사거리 안 복귀는 지연하지 않는다.
- 개인화기 교전 상태는 순간 `CanFire` 값이 아니라 거리 정책으로 정한다. 탄창이 비어도 근거리에서 추적 상태로 잘못 빠지지 않고 정지 교전 경로에서 재장전/발사를 다시 시도한다.
- 전투 시작점 기준 기본 3,000cm 리시, 2.5초 무진행 한계, 3초 재감지 Cooldown과 85% 복귀 반경을 추가했다. 범위를 벗어나거나 접근 불가하면 사격·이동·예약을 정리하고 순찰로 복귀한다. 모든 값은 Controller Blueprint Class Defaults에서 조정 가능하다.
- NPC Character는 역할 BP가 저장한 과거 설정과 무관하게 BeginPlay에서 이동 회전 계약을 복구한다. 추적 중에는 Controller가 실제 수평 속도 방향으로 몸 Yaw를 보간하고 Bone Gaze도 같은 이동 벡터를 보며, 정지 사격/엄폐에서만 Drone 방향 몸 Yaw를 사용한다. 이동 경로와 표적 직선 방향이 달라도 몸과 고개가 서로 반대로 선택하지 않는다.
- 리시 포기 중 StateTree를 동기 `RestartLogic()`하던 경로에서 `Reentrant call to StartTree`를 재현했다. 순찰 재시작을 다음 Tick으로 예약해 현재 Task 종료와 분리했다.
- 넓은 PIE 테스트는 수동 Sight 자극을 실제 Perception과 분리하고, 두 Hostile의 리시 안에 시험 Drone을 배치하며, 같은 맵의 무인 자동포탑 피해를 0으로 격리했다. Production Map/Asset은 수정하지 않았다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `Drone.AI.PersonalWeaponEngagementPolicy`, `Drone.AI.SmartObjectFoundationDefaults`, 경계 흔들림·몸/시선 이동 정렬·사거리 진입 즉시 정지를 확장한 `Drone.AI.ShotgunSystemsTestMapPIE`, `Drone.AI.NPCPerceptionSearchPIE`, `Drone.AI.NPCGreyboxAssets`가 최종 `5/5 Success`다. 마지막 넓은 PIE는 감지·MG 경합·개인화기 대체·사수 사망 후 재점유·Lost/Search·순찰 복귀 전체를 통과했고 StateTree 재진입 오류도 0이다.
- 팀원이 `BP_NPC_Friendly_Base` 역할 Mesh를 Manny에서 `/Game/QuantumCharacter/Mesh/SKM_QuantumCharacter`로 변경한 뒤 자산 회귀의 기대값만 옛 경로로 남아 있던 실패를 확인했다. Blueprint/Asset은 수정하지 않고 테스트 기대 경로만 현재 역할 Mesh로 갱신해 `NPCGreyboxAssets`를 Red→Green 전환했다.
- 임시 `[DEBUG-AI-*]` 로그는 모두 제거했고 `git diff --check`는 공백 오류 없이 통과했다. Unreal Editor는 종료 상태이며 Commit·Push는 하지 않았다. 다음 확인은 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`의 Rifle/Shotgun 추적 무떨림·리시 포기·MG 재점유 화면이다.

## 2026-09-15 — Gate 임시 16각 Ring을 Trigger 정합 4변 Frame으로 교체

- 화면에서 16개 Cube 조각의 끝이 튀어나오고 틈이 보이며 붉은 Box Trigger와 경계가 맞지 않는 문제를 확인했다.
- TDD 경계를 `표시 Frame 안쪽 크기 = 실제 Trigger/승인 범위`, `표시되는 변 = 4개`, `기존 3상태 색 유지`로 잡았다. 변경 전 테스트는 표시 16개와 정사각형 모서리 통과 거부를 재현해 실패했다.
- `ADroneTrainingGate`는 기존 Blueprint 직렬화 호환을 위해 16개 Visual Component를 보존하지만 앞의 4개만 상·하·좌·우 Cube Bar로 표시한다. Corner는 겹치거나 벌어지지 않게 맞물리고 Visual Collision/Overlap/Nav는 계속 꺼져 있다.
- `통과 영역 반쪽 크기`가 Frame 안쪽과 Box Trigger를 함께 정하고 `프레임 굵기`가 테두리 굵기/깊이를 정한다. 예전 `GateRadiusCentimeters`는 `Tutorial|Gate|Legacy`의 미사용 호환값으로 남겼다.
- 승인 판정도 원형 반경 검사에서 Actor Local Y/Z 정사각형 검사로 바꿔, 화면 Frame 안쪽 모서리를 통과했는데 실패하는 불일치를 제거했다. 순서·정방향·중복 방지와 `통과 전/현재 목표/통과 후` 색 전환은 변경하지 않았다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `Drone.Tutorial.TrainingGateSequence`와 `Drone.Tutorial.TutorialSystemsTestMap`이 각각 1/1 성공했다. Production `/Game/Drone/Maps/Lvl_DroneTraining`은 열거나 저장하지 않았고 TestMap 화면 확인만 남았다.

## 2026-09-11 — 팀원 Pull·Discard 자동 Stash 복구와 푸시 준비

- GitHub Desktop Pull 중 Hostile Rifle/Shotgun `.uasset` 교체가 Windows의 일시적 파일 점유로 실패했다. 재시도 과정에서 `Discard Changes`를 눌렀지만 Desktop이 직전 변경을 15:56 자동 Stash에 보존한 것을 확인했다.
- 이후 `44303a1` Fast-forward는 성공했다. Training Map SHA-256은 원격 LFS OID `ea66a333...`와 일치하고 Shotgun 9개·STF 492개가 정상 추적된다.
- 자동 Stash 전체에는 Map 삭제와 이미 원격에 들어간 대형 에셋도 함께 있어 그대로 적용하지 않았다. TUT-05 Source/Test 9개와 새 `ConfigureAutomaticTrainingGates.py`만 선택 복구했고 Stash는 삭제하지 않았다.
- 팀원 Hostile Rifle/Shotgun BP는 각각 Modular Insurgents `SK_Preset1`/`SK_Preset2`를 사용한다. 자산 테스트의 Manny 고정을 역할별 실제 Mesh 계약으로 바꿨고 NPC 자산·기본 PIE·Greybox PIE 3개가 통과했다. `NPCPerceptionSearchPIE`의 MG 사망 사수 정리/재점유는 재현되어 별도 실패로 남는다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build는 성공했다. Pull 직후 전체 `Drone.` 40개 중 36개가 성공했고 4개가 실패했다. Mesh 기준 수정 뒤 알려진 실패 테스트는 `NPCPerceptionSearchPIE`, `TrainingAssets`, `TrainingPIESmoke` 3개다.
- 최신 Training Map에는 Gate Actor 18개가 있지만 Course Sequence는 4개다. Recon/Impact/Payload 역할 표적과 Carryable Payload도 모두 0개여서 `TrainingAssets`, `TrainingPIESmoke`가 실패했다. 393MB 원격 맵을 임의 고정 좌표로 다시 저장하지 않고 화면에서 의도와 위치를 확인한 뒤 수정한다.
- `git diff --check`와 새로 받은 LFS Object 전체 `git lfs fsck`는 통과했다. Commit·Push는 하지 않았고, 전체 자동화가 다시 통과하기 전까지 현재 상태를 완전 검증으로 표시하지 않는다.

## 2026-09-11 — TUT-05 Spline 기반 자동 Ring Gate 구현·자동 검증

- 공통 Mission Flow, Drone 선택, 목표 패널, Training Lap 성공과 Drone 사망 실패 연결은 이미 구현된 상태로 확인했다. 이번 작업에서 같은 Flow를 중복 작성하지 않는다.
- `ADroneTrainingCourse`에 자동/수동 Gate 모드를 분리했다. 자동 모드는 수치로 Ring 개수, 균등 분배/고정 간격, 시작·끝 여백, 전체 거리 이동, Index별 거리 이동, 로컬 위치·회전·Scale과 Gate Class를 조정한다.
- 자동 Ring은 `UChildActorComponent`로 Course가 소유하며 현재 Spline 거리의 위치와 접선 회전을 따른다. Spline 또는 수치를 바꿀 때 이전 생성 Component를 Tag로 제거한 뒤 다시 만들어 중복을 막는다.
- 자동 모드는 생성 Ring 배열, 수동 모드는 기존 `OrderedGates`를 Sequence의 단일 기준으로 사용한다. `CourseId`, `GateIndex`, `SegmentDistance`는 기존 Sequence 계약으로 동기화한다.
- `Drone.Tutorial.TrainingCourse`에 5개 자동 Ring 생성, Spline 위치·방향·Index·거리, Sequence 유효성, 반복 재생성 중복 0, 자동 모드 종료 정리를 검사하는 항목을 추가했다.
- 첫 빌드는 `TArray<float>`에 허용되지 않는 `Units` UHT 메타데이터 한 건을 발견해 제거했다. 사용자 Editor 종료 뒤 MSVC 14.51.36257로 `DroneEditor Win64 Development` Build를 통과했다.
- 15:31의 `/Game/Drone/Maps/Lvl_DroneTraining` 검증본은 사용자 조정값인 자동 Ring 14개, 수동 Gate 0개였다. 별도 명령줄 프로세스 재로드에서 Gate Class·개수·Sequence와 수동 Gate 부재를 확인했다.
- 자동 Map 전환 뒤 자산 테스트의 Construction 재실행 포인터와 PIE 복제 시 Child Actor Cache 복원 문제를 발견해, 생성 Component Tag 재검색·정렬로 보강했다. 최종 `Drone.Tutorial` 7/7이 경고·오류 없이 통과했다.
- 전체 Suite에서는 RecastNavMesh 초기화 경고가 선행 Map 상태에 따라 1회 또는 2회 발생하는데 기존 테스트가 정확히 2회로 고정돼 2건이 실패했다. 기능 검증은 유지하고 예상 경고 1회 이상을 허용하도록 바꾼 뒤 전체 `Drone.` 40/40을 통과했다.
- 전체 Blueprint Compile은 실패 0이다. 종료 요약의 29 warnings는 기존 Battlefield Quinn Pose GUID 경고이며 이번 Course/Map 변경의 Blueprint 경고가 아니다. Training Map Check는 0 errors/0 warnings다.
- `git diff --check`, `git lfs fsck`를 통과했고 Unreal Editor와 명령줄 검사 프로세스는 종료 상태다. 코드·Map·테스트·문서는 로컬 미커밋이며 사용자가 Commit/Push한다.
- 이후 사용자가 Training Map을 의도적으로 덮어쓰는 중이라고 알려 현재 Map 변경을 수정·복구하지 않았다. 교체 완료 뒤 최종 Ring 수·Sequence·Map Check와 전체 순서 비행을 다시 확인한다.
- 후속 요청에 따라 `AutomaticGateSplineDistancesCentimeters`와 `AutomaticGateLocalOffsets`를 추가했다. 배열 Index별로 Spline 절대 거리와 X 진행방향/Y 좌우/Z 높이를 직접 지정하며, 항목이 없는 Ring은 기존 균등/고정 배치와 0 위치 보정을 유지한다.
- `ConfigureAutomaticGateOverrides` Blueprint 함수와 5개 Ring의 서로 다른 절대 거리·로컬 위치 자동화 검증을 추가했다. 저장 맵의 Ring 수를 4로 고정하던 자산/PIE 테스트도 2개 이상이며 Course·Sequence 수와 일치하는지를 검사하도록 일반화했다.
- `BP_DroneTrainingGate`에서 `통과 전`, `현재 목표`, `통과 후` 색을 한글 Class Defaults로 편집하고 Blueprint Graph의 `Set Gate State Colors`로 런타임 변경할 수 있게 했다.
- 후속 변경 뒤 MSVC 14.51.36257 Editor Build, Tutorial 7/7, 전체 `Drone.` 40/40, 저장 맵 재로드 `count=14/manual=0`, Map Check 0/0을 통과했다. `BP_DroneTrainingCourse`와 `BP_DroneTrainingGate`를 포함한 전체 Blueprint Compile은 오류 0이며 29 warnings는 기존 Battlefield Quinn Pose GUID다.
- Mission 다음 구현은 목표 종류·필요 수량·제한 시간·대상 ID를 데이터화하고 정찰/투하/파괴/귀환 Event를 Director에 연결한 뒤 Jamming Rule로 확장한다.

## 2026-09-09 — Rotor 외형 회전·Blueprint 튜닝·역할 표적 BP 전환

- `ADronePrototypePawn`이 `DroneRotor` Component Tag 또는 기존 `Rotor` 이름을 가진 Static Mesh를 수집해 Tick에서 회전시키도록 구현했다. 이동·Collision에는 영향을 주지 않으며 사망 시 정지한다. FPV·Scout는 Rotor 4개, Drop은 6개에 Tag를 저장했다.
- 첫 화면 확인에서 Rotor가 자기 자리가 아니라 기체 주위를 크게 공전했다. 공급 Drone Pack의 일부 분리 Mesh는 Asset Pivot이 기체 원점에 있고 날개 Geometry만 떨어져 있기 때문이었다. 회전 전후 Static Mesh Bounds 중심의 Parent-space 위치 차이를 Relative Location으로 상쇄해 각 Rotor가 자기 Bounds 중심에서만 돌도록 수정했다.
- 후속 화면 확인에서 FPV 자폭 Drone의 Rotor 4개가 본체 중앙에 겹친 상태를 확인했다. FPV 전용 Rotor Mesh에는 이미 본체 기준 네 모서리 Geometry 좌표가 들어 있는데 BP Component Location이 반대 Offset을 한 번 더 적용해 중심을 `(0, 0)`으로 상쇄한 것이 원인이었다. FPV Rotor A~D Component Location을 원점으로 복구해 Mesh 내부 좌표대로 네 암 끝에 배치했다.
- Pawn BP Class Defaults에 `Rotor Visual Spin Enabled`, 초당 회전 각도, 로컬 회전축, 교차 방향, Component Tag를 노출했다. 역할별 BP에서 모델 축과 체감에 맞춰 수정할 수 있다.
- `Override Definition Flight Profile In Blueprint`를 켜면 Data Asset 대신 Pawn BP의 Flight Profile로 최대 속도·가속/감속·Yaw·Pitch/Roll·시작 시점·체력 등 비행 프로필을 한 번에 덮어쓸 수 있다. 기본값은 꺼짐이라 기존 DA_Drone 설정을 유지한다.
- NPC Controller BP에는 Sight/Lose Sight 거리, 주변 시야각, 자극 유지시간과 진영 감지 옵션을 노출했다. AnimBP에는 Spine/Neck/Head 시선 회전 분배 비중을 노출했다. 기존 런타임 캐시·안전 상수·상태값은 조정값이 아니므로 내부에 유지한다.
- Training의 Native Recon/Impact/Payload 표적을 `/Game/Drone/Abilities/RoleTargets/BP_RoleTest_*` 3개로 교체했다. 표적 Mesh/Scale과 안내 문구·색·크기·위치·회전을 BP Class Defaults 또는 맵 배치 Instance에서 조정할 수 있다.
- VS 업데이트 뒤 설치된 MSVC 14.51.36231 Toolchain(cl 19.51.36257)으로 `DroneEditor Win64 Development` 전체 Build가 성공했다. 이전 14.38 실패는 UE 5.8 SharedPCH와 구형 컴파일러의 호환 문제였고 프로젝트 코드 오류가 아니었다.
- `FlightProfiles`, `VisualBank`, `RoleDroneAssets`, `TrainingAssets`, `NPCGreyboxAssets`, `NPCPerceptionSearchPIE` 집중 자동화 6/6 성공. Pivot 보정 뒤 `VisualBank`, `RoleDroneAssets` 2/2를 다시 실행해 FPV·Scout·Drop 모두 회전값은 변하고 실제 Rotor Bounds 중심은 0.1cm 오차 안에서 고정됨을 확인했다. FPV 배치 보정 뒤 `FPVAsset`, `VisualBank`, `RoleDroneAssets` 3/3을 다시 통과해 Rotor 중심이 본체에서 20cm 이상 떨어지고 네 사분면에 하나씩 배치됨도 확인했다. 전체 Blueprint 420개는 컴파일 실패 0이며, 종료 요약의 29 warnings는 기존 Battlefield Quinn Pose GUID 불일치다. Training Map Check 0 errors/0 warnings, `git diff --check`, `git lfs fsck`도 통과했다.
- 남은 작업은 Editor에서 Rotor 회전축·교차 방향·속도, 역할 표적 표시, 역할별 기능과 드랍 화물 루프를 화면으로 확인하는 것이다. 수치 보정은 해당 Pawn/Controller/AnimBP/표적 BP의 Class Defaults에서 처리한다.

## 2026-09-09 — 팀원 LFS 자산 복구와 Trello 정리

- GitHub Desktop에서 Stashed Changes Restore를 반복하면 `test1.umap`, `M_Start.uasset: needs merge`, `could not write index`가 발생했다. 첫 Restore가 이미 두 LFS 바이너리 충돌을 만든 상태라 두 번째 적용이 거부된 것이며 Stash 자체는 보존됐다.
- 현재 main의 손상된 277/274-byte 충돌문자 LFS Object는 선택하지 않고 사용자 결정에 따라 팀원 Stash 버전을 보존했다. `test1.umap` 48,817 bytes와 `M_Start.uasset` 11,456 bytes 모두 Unreal Package Magic과 팀원 OID를 확인했다.
- 두 파일만 충돌 해결·Stage한 뒤 사용자가 `ac88992`로 Commit/Push했다. Fetch 뒤 `HEAD=origin/main=ac88992`, 원격 LFS OID 일치와 Clean 작업 트리를 확인했다.
- `.vsconfig`는 공유 가능한 구성요소 목록이지만 Stash의 14.44 Toolset 변경은 UE 5.8 기준에 맞지 않아 제외했다. 기존 14.50 파일을 유지했고 복구 Commit에 포함하지 않았다.
- 지금까지 구현한 기능과 앞으로 할 작업을 Trello List/카드/체크리스트 형식으로 [`DRONE_TRELLO_BOARD_2026-09-09.md`](DRONE_TRELLO_BOARD_2026-09-09.md)에 정리했다.

## 2026-09-08 — DR-DROP-02 맵 배치형 운반 화물

- `ADroneDroppedPayload`에 맵 Pickup, Carried, 투하 상태를 추가하고 Pickup 상태에서는 충돌 투하 판정을 막았다. `UDronePayloadDropComponent`의 Primary는 적재 중이면 투하하고 비어 있으면 300cm 안의 가장 가까운 사용 가능 화물을 한 번 검색한다.
- Pickup 성공 시 맵의 실제 Payload Actor를 `ADronePrototypePawn.PayloadCarryAnchor`에 붙인다. 재투하 때 새 Actor를 복제하지 않고 같은 Actor를 분리해 낙하시키며, 역할 재설정 때 운반 중 화물은 월드 Pickup 상태로 안전하게 돌려놓는다.
- `/Game/Drone/Abilities/Payload/BP_DroneCarryablePayload`를 `ADroneDroppedPayload` 자식으로 생성했다. 외형은 `/Game/FC_MilitaryCamp/Models/MilitaryModels/SM_MilitaryCrate_01`, 시작 상태는 Carryable이며 Training Map `(300, -300, 70)`에 `RoleTest_CarryablePayload` 한 개를 배치했다.
- Mission 역할 안내는 Drop 적재 수가 0이면 `화물 가까이서 좌클릭/RB 적재`, 적재 중이면 `좌클릭/RB 화물 투하`를 표시한다. 탑뷰 우클릭/LB는 유지한다.
- MSVC 14.51.36256 Editor Build가 성공했다. `Drone.Prototype` 7/7, `Drone.Integration` 3/3, `Drone.Tutorial` 7/7, `Drone.Flow` 5/5로 집중 자동화 22/22가 전부 통과했다.
- 생성 Commandlet은 `DRONE_CARRYABLE_PAYLOAD|OK`와 저장 파일을 확인했다. 종료 코드 1은 별도 LFS 충돌 Pointer `test1.umap`, `M_Start.uasset`의 Asset Registry 오류이며 두 파일·`.vsconfig`·`Drone.cpp //test`는 건드리지 않았다. Commit·Push하지 않았다.
- 첫 화면 확인에서 착지 직후 투하물이 사라졌다. 원인은 기존 일반 Payload가 모든 충돌 뒤 0.1초 후 제거되는 공용 처리였다. Carryable 이력이 있는 Actor는 낙하 중 자동 수명을 끄고 착지 후 그 자리에 정지·표시·재적재 가능 상태로 남기며, 일반 1회용 Payload만 기존 제거 규칙을 유지하도록 분리했다. `BP_DroneDropIntegration.PayloadDropComponent.PayloadClass`도 새 크레이트 BP로 바꿔 첫 투하부터 같은 규칙을 사용한다. 수정 Build와 `Drone.Prototype.RoleAbilities`, `Drone.Integration.RoleDroneAssets` 각 1/1이 통과했다.
- 다음은 Front-end→Training에서 Drop을 선택해 선적재 화물을 먼저 투하하고, 크레이트 적재·하단 부착·재투하의 크기와 위치를 화면으로 확인하는 것이다.

## 2026-09-08 — 패드 역할 기능·시점 입력 마무리

- `IA_DronePrototype_PrimaryAbility`에 패드 RB, `SecondaryAbility`에 패드 LB를 추가했다. 역할별 의미는 Mouse와 같으며 정찰 Scan/취소, FPV Arm/Disarm, 드랍 투하/탑뷰로 분기한다.
- 기존 `P` 전용 시점 전환에는 패드 Y를 추가했다. IMC는 18개에서 RB/LB/Y를 더한 총 21 Mapping이다.
- 입력 재생성 스크립트는 Action별 모든 예상 Key를 집합으로 검증하도록 바꿨다. PIE Input Lifecycle은 P/Y, 좌클릭/RB, 우클릭/LB가 각각 정확히 한 번 존재하고 Pawn 소유 Binding이 재시작 3회 동안 중복되지 않는지 검사한다.
- MSVC 14.51.36256 `DroneEditor Win64 Development`가 성공했고, 최종 `Drone.Prototype` 7/7이 통과했다. 직전 동일 변경 묶음의 Integration 3/3, Tutorial 7/7, Flow 5/5 결과도 유지되어 집중 자동화는 22/22다.
- 확인용 Editor는 `/Game/Drone/Maps/Lvl_DroneFrontEnd`로 다시 열었다. 실제 Controller 버튼 압력·모델 크기·폭발/투하 체감은 사용자 수동 확인으로 남긴다.

## 2026-09-08 — DR-ROLE-TARGET-01 역할별 모델·기능 시험장

- 세 Definition이 같은 FPV 외형을 공유하던 임시 상태를 분리했다. Scout는 `/Game/Drone/Integrations/RoleDrones/BP_DroneScoutIntegration`과 DroneSpy 6파트, FPV는 기존 `BP_DroneFPVIntegration` 5파트, Drop은 `BP_DroneDropIntegration`과 Delivery 8파트를 사용한다. 공통 입력·카메라·비행 C++ 기반은 그대로 재사용한다.
- Drop Pawn에 `DroneCarriedPayload` Tag의 임시 Cube 적재물을 달았다. 역할 활성화·재장전 때 보이고 실제 투하하면 즉시 숨는다. `UDronePayloadDropComponent`는 지정 Target이 없거나 이미 완료됐으면 가장 가까운 미완료 `UDronePayloadTargetComponent`를 클릭 시점에 자동 선택한다.
- `ADroneReconRoleTestTarget`, `ADroneImpactRoleTestTarget`, `ADronePayloadRoleTestTarget`을 추가하고 `Lvl_DroneTraining`에 각 1개를 배치했다. 표적에는 역할별 한글 조작 문구가 있고 코스 Gate/안내선 판정과 독립이다.
- FPV 자폭에는 제공 `/Game/Drone/ThirdParty/ArmyVFX` Niagara와 `/Game/Drone/ThirdParty/InfantrySFX` Explosion Cue를 연결했다. Arm/Disarm/Detonate 상태 Event도 UI가 구독한다.
- Mission 목표 Widget은 선택 Pawn을 직접 주입받고 정찰 진행률·완료 수, FPV 안전/무장, Drop 적재/성공/탑뷰 상태를 Event 기반 한글 텍스트로 표시한다. Tick Actor 검색은 추가하지 않았다.
- 재생성 도구 `BuildDroneRoleIntegrations.py`, `BuildDroneRoleTestArena.py`를 추가하고 기존 `BuildDroneFlightProfileAssets.py`를 역할별 Class 매핑으로 갱신했다.
- MSVC 14.51.36256 `DroneEditor Win64 Development` Build 성공. 자동화는 Prototype 7/7, Integration 3/3, Tutorial 7/7, Flow 5/5로 총 22/22 통과했다. Map Check는 Training PIE에서 0 errors/0 warnings다.
- Commandlet 종료 코드는 미해결 `test1.umap`, `M_Start.uasset` LFS 충돌 Pointer 때문에 Asset Registry 오류를 기록할 수 있으나, 기능 스크립트 실행과 관련 테스트는 모두 성공했다. 두 충돌 파일과 `.vsconfig`, `Drone.cpp //test`는 이번 기능 범위에서 건드리지 않았다.
- Commit·Push는 사용자가 수행한다. 다음은 Editor에서 세 모델 크기/방향, 정찰 좌클릭/RB 유지와 우클릭/LB 취소, FPV 좌클릭/RB 무장 후 고속 충돌 폭발, Drop 우클릭/LB 탑뷰와 좌클릭/RB 투하·적재물 소멸을 수동 확인하는 것이다.

## 2026-09-08 — 공유 main 최신화와 Pull/Stash 충돌 감사

- Fetch 결과 Unreal `main=origin/main=63f60c1`, 문서 `main=origin/main=d30e098`로 원격과 일치한다. `63f60c1`은 역할 기능 3종·공통 역할 입력·FLOW-04~08을 58개 변경 파일로 공유한 Commit이다.
- Unreal은 09:20 Fast-forward Pull 직후 자동 복원된 Stash와 Upstream 사이에 `test1.umap`, `M_Start.uasset` 양쪽 추가 충돌이 남았다. Worktree의 두 파일은 `.uasset/.umap` 본문이 아니라 충돌 마커가 삽입된 LFS Pointer라서 그대로 Unreal 저장·Stage·Commit하지 않는다.
- Upstream/HEAD 후보는 `test1.umap` 36,998,062 bytes·`M_Start.uasset` 11,569 bytes이고, Stash 후보는 각각 48,817 bytes·11,456 bytes다. 두 바이너리는 내용 병합이 불가능하므로 보존할 버전을 선택해야 한다.
- `.vsconfig`는 Index 14.44와 Worktree/HEAD 14.50이 서로 다르고 `Drone.cpp`의 `//test`가 Staged로 돌아왔다. 이전 규칙대로 `//test`는 기능 변경과 분리해 제거하고 Toolchain은 실제 설치·빌드 기준으로 하나만 남겨야 한다.
- UE 5.8.2 Editor가 D 드라이브 프로젝트를 정상 로드했다. 수동 로그에서 Front-end→Training Map, FPV Definition 적용과 Pawn Possess까지 확인했고 Fatal/Crash는 없었다.
- 실제 Spawn Class는 `BP_DronePrototypePawn_C_0`이며 `모든 Prototype Input Action이 아직 배정되지 않았다`는 프로젝트 진단이 발생했다. 후속 Asset 대조에서 세 Mission Definition의 Pawn Class가 모두 기본 Prototype을 가리키고 있음이 확정됐다.
- 공유 전 기록의 Flow 5/5·Prototype 7/7·새 PIE 3/3은 보존한다. 현재 PC의 Saved Automation Report는 없으므로 충돌 선택과 역할 입력 연결 수정 뒤 Editor Build, `Drone.Flow`, `Drone.Prototype`, 수동 좌/우 클릭 역할 기능을 다시 검증한다.

## 2026-09-08 — Mission Drone 모델·입력 누락 원인 확정과 수정 준비

- `DA_Drone_Scout_Greybox`, `DA_Drone_FPVStrike_Greybox`, `DA_Drone_Drop_Greybox` 내부 참조를 직접 대조했다. 세 Asset 모두 `BP_DronePrototypePawn`을 참조해 Mission 선택 뒤 기본 Cube/Prototype 표현과 미배정 Input 경고가 재현됐다.
- 실제 Drone Pack 본체·로터 4개·Loop Sound와 Prototype/역할 Input Action은 `/Game/Drone/Integrations/DronePackFPV/BP_DroneFPVIntegration`에 존재한다. 역할 기능 C++ 자체가 사라진 것이 아니라 `ADroneMissionPlayerController::StartSelectedDrone()`이 Definition의 잘못된 `PawnClass`를 그대로 Spawn한 연결 오류다.
- `BuildDroneFlightProfileAssets.py`가 세 Definition 모두 Integration Pawn Class를 명시적으로 저장하도록 수정했다. `Drone.Prototype.FlightProfiles`는 세 Definition의 Class가 정확히 Integration Pawn인지 검사하고, `Drone.Flow.MissionEntryPIE`는 최초 Scout와 재시도 Drop 출격에서 실제 Spawn Class를 검사하도록 강화했다.
- 기존 테스트는 Definition Class가 단지 `ADronePrototypePawn` 하위인지 확인했고 Integration Asset 테스트를 별도로 수행했기 때문에 두 연결이 달라도 통과할 수 있었다. 이번 정확한 Class 검증으로 같은 회귀를 막는다.
- Editor를 종료한 뒤 스크립트를 실행해 세 Data Asset에 Integration Pawn을 실제 저장했다. `DroneEditor Win64 Development`, `Drone.Prototype` 7/7, `Drone.Flow` 5/5, `Drone.Integration.FPVAsset` 1/1이 통과했다. Flight Profile은 세 역할 모두 Integration Class를 생성했고 Mission PIE 3회는 Scout와 재시도 Drop을 매회 Integration Class로 Spawn/Possess했다. 기존 `does not have all prototype Input Actions assigned yet` 경고는 새 Mission 실행 로그에서 0건이다.
- 자동 검증은 모델 Component와 Class 연결을 확인하지만 실제 렌더 화면·스피커·손 조작을 대신하지 않는다. Front-end에서 세 역할을 각각 출격해 외형과 조작을 확인해야 한다. `test1.umap`, `M_Start.uasset` LFS 충돌은 이 수정과 무관하게 남아 있고 Commit·Push는 사용자가 담당한다.

## 2026-09-08 — FLOW-08 새 실행 3회 반복 완료

- `DroneMissionEntryPIE`가 하나의 PIE를 재활용하지 않고 완전히 종료한 뒤 새 PIE를 시작하도록 Lazy Start와 종료 안정화 대기를 추가했다. Engine Start 명령이 생성 즉시 `EndPIE`를 구독해 다음 실행이 조기 실패하던 문제를 실제 실행 차례에 생성하는 방식으로 고쳤다.
- 각 실행은 `Opening→Lobby→Briefing→Training Map→Scout 성공→Retry→Drop Health 0 실패→Lobby`를 끝까지 수행한다. Root Widget 1, Map 요청 1, 선택 전 Drone 0, 출격 뒤 Drone 1·Director 1, Finish Event 1, 로비 복귀 뒤 Drone 0을 검증한다.
- UI 전용 GameMode는 빈 Pawn/HUD Class 대신 비-Drone `ASpectatorPawn`과 기본 HUD를 사용해 `SpawnActor failed because no class was specified` 경고를 0건으로 만들었다.
- 최종 `DroneEditor Win64 Development` Build, `Drone.Flow` 5/5와 `Drone.Prototype` 7/7이 통과했다. 빈 시험 World의 기존 RecastNavMesh 경고만 남았으며 기능 실패는 아니다.
- FLOW-01~08 자동화 게이트를 모두 닫았다. 다음은 Editor 수동 Vertical Slice와 TUT-04 두 Lap 확인이다. Commit·Push하지 않았다.

## 2026-09-08 — DR-ROLE-INPUT-01 공통 역할 입력

- `IA_DronePrototype_PrimaryAbility`, `IA_DronePrototype_SecondaryAbility` Boolean Action을 만들고 `IMC_DronePrototype`과 `BP_DroneFPVIntegration` CDO에 연결했다. Mapping은 기존 16개에서 Mouse 2개와 Gamepad Shoulder 2개, 시점 전환용 패드 Y 1개를 더한 21개가 됐다.
- 최종 키를 확정하지 않고 Greybox 임시값으로 좌클릭/RB=1차, 우클릭/LB=2차를 사용한다. 정찰은 가장 가까운 유효 Target Scan/취소, FPV는 Arm/Disarm, 드랍은 Payload 투하/상단 Camera 전환으로 분기한다.
- 정찰 자동 표적 검색은 클릭 시점에만 World를 한 번 순회하며 Tick에서 Actor를 계속 찾지 않는다. 거리·화각·LOS와 완료 여부는 기존 Scan Component 단일 검증 함수를 재사용한다.
- `Drone.Prototype.RoleAbilities`에서 세 역할 분기와 상태를, `PIEInputLifecycle`에서 두 Action의 Mapping·Pawn 소유 Started Binding·3회 PIE 수명주기를 확인했다. 전체 `Drone.Prototype` 7/7과 `Drone.Flow` 5/5가 재통과했다.
- Training Map에 실제 `UDroneReconScanTargetComponent`와 `UDronePayloadTargetComponent`가 붙은 시험 표식, 역할 상태 HUD는 아직 없다. 이는 `DR-ROLE-TARGET-01`로 분리한다. Commit·Push하지 않았다.

## 2026-09-08 — 역할 기능 3종·FLOW-04~07 완료

- 정찰은 `UDroneReconScanComponent`와 Target Component로 거리·화각·시야선 유지 중 진행하고 이탈 시 취소하며 한 번만 완료한다. FPV는 명시적 Arm과 최소 충돌 속도 뒤 1회 Radial Damage·자기 Health 0을 적용한다. 드랍은 기존 1/3인칭 상태를 복원하는 상단 Camera와 한 발 Payload·목표 접촉·재장전을 사용한다.
- `DA_Drone_Scout_Greybox`, `DA_Drone_FPVStrike_Greybox`, `DA_Drone_Drop_Greybox`의 구현 Capability를 각각 하나씩 활성화했다. `Drone.Prototype.RoleAbilities`와 Flight Profile 검증에서 다른 역할 기능 중첩이 없음을 확인했다.
- Front-end Root에 선택 Mission의 정적 Briefing·초기 목표와 종료 버튼을 추가했다. Controller는 정확히 한 번 선택 `MissionMap`을 열며 URL 전용 `DroneMissionGameMode`로 Map의 기존 Prototype GameMode를 이번 진입에만 덮어쓴다.
- Mission Map의 `UDroneSelectionWidget`은 세 역할 카드, 쉬운/실제 조작형, 안정/균형/고기동을 표시한다. 선택 전에는 비-Drone Spectator만 있고, 확정 뒤 Data Asset Pawn 한 대에 Profile과 이번 설정을 적용해 Possess한다.
- 새 `ADroneMissionDirector`는 출격 뒤 시작 요청을 한 번 소비하고 Data Asset 목표를 `UDroneMissionObjectiveWidget`에 Event로 보낸다. 현재 Training 연결은 Lap 완료=성공, Drone Health 0=실패인 Greybox이며 최종 Story 규칙은 아니다.
- `UDroneMissionResultWidget`의 성공/실패, 같은 Mission 재도전과 Front-end 로비 복귀를 구현했다. 로비 복귀 표지는 새 Front-end Controller가 한 번 소비한다.
- `DroneMissionEntryPIE`가 `Opening→Lobby→Briefing→Training Map→Scout 출격→Success→Retry→Drop 출격→Health 0 Failure→Lobby`를 실제 Map 전환으로 통과했다. `DroneEditor Win64 Development`, `Drone.Flow` 5/5, `Drone.Prototype` 7/7이 성공했다.
- 실제 Trailer Media, 최종 WBP Designer·Preview, 최종 성공/실패 규칙과 손 조작 체감은 미정/수동 대기다. Commit·Push하지 않았다. FLOW-08 결과는 바로 위 최신 절을 따른다.

## 2026-09-08 — Figma 기체 역할·조작 모드 분리

- 사용자 제공 Figma `Project:Droner`를 로그인된 Browser에서 읽기만 했다. 수정·댓글·공유 설정 변경은 하지 않았다.
- 현재 기획 역할로 정찰, 드랍, FPV 자폭, 광섬유, 지상 UGV, 장거리 타격을 확인했다. 최종 확정·완료 목록으로 해석하지 않는다.
- 잘못된 임시 기체 분류 `균형 정찰형/고기동형/안정 관측형`을 역할과 핸들링으로 분리했다.
- `EDroneMissionRole`, `EDroneGameplayCapability`, `EDroneControlMode`, `EDroneHandlingPreset`을 추가했다.
- `UDroneDefinition`에 플레이 가능 여부와 계획/구현 Capability 목록을 추가했다. 구현 기능은 계획 기능의 부분집합이어야 Validation을 통과한다.
- `ADronePrototypePawn`에 쉬운/실제 조작형과 안정/균형/고기동 변경 API·Blueprint Event를 추가했다. 실제 조작형은 낮은 자동 감속/선회 보조, Root Pitch/Roll, Local Up을 사용하는 Greybox이며 실제 모터 물리로 표현하지 않는다.
- Data Asset은 `DA_Drone_Scout_Greybox`, `DA_Drone_FPVStrike_Greybox`, `DA_Drone_Drop_Greybox` 3종으로 정리했다. 이 시점에는 역할 기능을 Planned로 시작했고 같은 날짜 후속 절에서 구현 Capability로 승격했다.
- `DroneEditor Win64 Development` Build 성공. `Drone.Prototype.FlightProfiles` 1/1과 `Drone.Flow` 3/3 성공.
- Unreal 기준 `main=origin/main=dbc0dd8`, 문서 기준 `main=origin/main=aaef93d` 위 로컬 변경이다. Commit·Push하지 않았다.
- 상세 가이드: [`DRONE_TYPES_AND_CONTROL_MODES.md`](../gameplay/DRONE_TYPES_AND_CONTROL_MODES.md)

## 2026-09-04 — DR-DMGFX-01 Drone 피격 본체·카메라 흔들림

- `UDroneHealthComponent`의 Blueprint `OnHealthChanged`는 유지하고 C++ 표현 수신용 Native Event를 추가했다. 모든 무기가 공용 Health Damage를 사용하면 별도 무기 분기 없이 같은 피격 반응을 실행한다.
- `ADronePrototypePawn`은 피해량을 25 Damage에서 최대 강도로 제한하고 작은 피해에는 최소 25% 강도를 준다. 기본 0.30초 동안 본체 최대 6°, Camera View 최대 5cm·1.5°를 18Hz로 흔들며 제곱 감쇠한다.
- 본체 흔들림은 기존 A/D Visual Bank와 합성하고 Camera는 기존 Additive Offset을 보존했다가 종료 시 복원한다. Actor 위치·Collision 회전·이동 속도에는 변화가 없다. 연속 피격은 시간을 다시 시작하고 더 강한 피해 강도를 유지한다.
- 첫 자동화는 Editor 임시 World에서 게임 실행 전용 Delegate 수명주기가 아직 시작되지 않는 차이를 발견했다. Construction·Runtime 모두 같은 Native Health Binding을 보장하도록 수정했고, 최종 `Drone.Prototype.DamageShake`가 Health Damage→흔들림→Camera 복원과 Collision 불변을 통과했다.
- 최종 MSVC 14.51.36256 Editor Build와 `DamageShake`, `VisualBank`, `GroundConformingSuspension`, `AutomaticTurretTargeting`, `NPCGreyboxAssets`, `FlightHUDTelemetryBinding` 6/6이 통과했다. 이어 `NPCPerceptionSearchPIE`에 실제 `UGameplayStatics::ApplyDamage`가 피격 흔들림을 정확히 한 번 늘리고 파괴 뒤 중복 피해는 다시 시작하지 않는 조건을 추가해 1/1 재통과했다. 빈 시험 World의 기존 RecastNavMesh 경고 외 실패는 없다.
- 실제 탄환 피격의 강도·멀미 체감과 연속 피격은 수동 확인 전이다. 방향성 반동, Gamepad 진동, HUD Flash, Sound·Niagara는 후속이며 Commit·Push하지 않았다.

## 2026-09-04 — VEH-GROUND-01 4점 지면 추종·DR-VBANK-01 Drone 외형 Roll

- 완전한 차량 물리 대신 앞좌·앞우·뒤좌·뒤우 네 지점의 Visibility Trace로 굴곡을 읽는 `ADroneGroundConformingVehicle`를 추가했다. 접촉점 세 개 이상에서 평균 높이와 접촉 평면으로 Z·Pitch·Roll을 계산하고 최대 28° 안에서 보간한다. Collision은 Query 전용이고 Chaos Simulation은 사용하지 않는다.
- 임시 Cube Body, Cylinder Wheel 네 개와 `TurretMount`를 분리했다. 수동 `SetDriveInput(-1~1)`과 Controller 없이 왕복하는 Greybox Auto Drive를 제공해 향후 실제 Vehicle AI와 시험 배치를 분리했다.
- `/Game/Drone/Vehicles/Blueprints/BP_GroundConformingVehicle_Greybox`를 만들고 `Lvl_NPCSmartObjectGreybox`의 정적 Carrier를 교체했다. `VehicleRoughRoad_01`~`05` 다섯 굴곡 노면을 추가하고 차량형 자동포탑을 `TurretMount`에 Attach했다.
- `ADronePrototypePawn`에 Collision 자식 `VisualTiltPivot`을 추가했다. 최초 구현은 A/D 좌우 입력만 최대 ±18° Roll했으나 수동 확인에서 전후 기울기 누락과 좌우 방향 반대가 발견됐다. W/S는 최대 ±14° Pitch(전진 기수 아래·후진 기수 위)를 추가하고 A/D Roll 부호를 반전했으며 복합 입력에서는 두 축을 동시에 합성한다. CameraBoom과 Collision은 기존 부모를 유지하며 실제 FPV Integration의 Body·Rotor 네 개를 Pivot 아래로 정리한다. `DroneNoVisualBank` Tag로 개별 Mesh를 제외할 수 있다.
- 보정 뒤 MSVC 14.51.36256 Editor Build가 성공했다. `Drone.Prototype` 5/5가 통과해 Pitch·Roll 방향과 복귀, Camera/Collision 불변, 피격 흔들림 합성, Pawn 기본값, Spawn/Possess 및 새 PIE 3회 입력 수명주기를 재검증했다. Move Action은 조작용 Triggered 1개와 외형 복귀용 Completed/Canceled 각 1개만 Pawn에 연결되는 계약으로 검사한다.
- MSVC 14.51.36256로 `DroneEditor Win64 Development` Build가 성공했다. 첫 실제 Compile에서 lambda capture와 Camera proxy 타입 접근 두 건을 바로잡은 뒤 최종 소스가 통과했다.
- `Drone.Vehicle.GroundConformingSuspension`, `Drone.Prototype.VisualBank`, `Drone.AI.AutomaticTurretTargeting`, `Drone.AI.NPCGreyboxAssets` 집중 4/4가 성공했다. 실제 맵 자산 테스트는 차량 1·Wheel 4·굴곡 노면 5·포탑 Attach와 자동 주행 설정을 확인했다.
- 저장 자산 Validation은 자동포탑 BP 2개와 차량 BP를 재컴파일하고 `MAP_VALIDATION_OK|emplaced=1|vehicle=1|vehicle_attached=true|suspension=4|road=5`, Map Check 0 errors/0 warnings로 종료했다.
- 전체 Blueprint Commandlet는 0 errors, 29 warnings로 성공했다. 경고는 전부 공급사 `/Game/Battlefield/Demo/Characters/Mannequins/Rigs/Poses`의 Manny/Quinn Pose GUID 불일치이며 이번 `/Game/Drone` 자산의 Compile 실패가 아니다.
- 수동 화면 확인은 남았다. 자세한 조정과 보고 형식은 [`DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md`](../gameplay/DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md)를 따른다. Commit·Push는 사용자 요청대로 하지 않았다.

### 진행 중 — VEH-WHEEL-01·DR-CAM-01

- 차량 네 바퀴는 Throttle 표시값이 아니라 프레임 사이 실제 전진축 이동거리와 `WheelRadius`로 회전각을 계산하도록 C++를 작성했다. 전진은 누적각 증가, 후진은 감소하며 반속 이동에서는 회전속도도 절반이 되는 자동화 조건을 추가했다.
- Drone은 기존 FollowCamera 하나를 재사용한다. 3인칭은 CameraBoom이 Collision Root와 500cm Arm을 사용하고, 1인칭은 CameraBoom이 `VisualTiltPivot`에 붙어 Arm 0과 전방 Offset을 사용하므로 이동 Pitch·Roll과 피격 흔들림을 화면도 따른다. 전환 입력은 `P`로 설계했고 Enhanced Input Action·IMC 연결 및 PIE 검증을 이어서 적용한다.
- 최초 Link는 사용자가 실행한 `Drone - 언리얼 에디터`가 모듈 DLL을 잡아 중단됐다. 저장하지 않은 작업 보호를 위해 강제 종료하지 않았고 사용자 저장·종료 뒤 같은 Build를 재개해 성공했다.
- `/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_ToggleView`를 생성하고 `IMC_DronePrototype`의 P에 한 번 매핑했다. 전체 16 Mapping과 `BP_DroneFPVIntegration.ToggleViewAction` 저장을 재실행 가능한 `BuildDroneViewToggleInput.py`로 검증했다.
- 최종 MSVC 14.51.36256 Editor Build, 차량 회전비례·후진 조건 `GroundConformingSuspension` 1/1, P Mapping/Binding 새 PIE 3회와 Camera 추종을 포함한 `Drone.Prototype` 5/5가 성공했다. 빈 시험 World의 기존 Recast 경고 외 실패는 없다.
- 실제 화면에서 바퀴 Mesh 축 방향과 속도 체감, P 전환, FPV 위치·Mesh 가림·멀미 여부를 확인해야 한다. Commit·Push는 하지 않았다.
- 첫 차량 화면 확인에서 실제 이동과 바퀴 구름 방향이 반대인 것이 확인됐다. Greybox Cylinder의 `WheelVisualSpinDirectionMultiplier`를 `-1`에서 `+1`로 바꾸고 BP·맵 배치 Actor에도 같은 값을 저장·검증하도록 생성 도구를 보강했다. 방향 재확인은 남아 있다.
- 축 교정 뒤 MSVC 14.51.36256 Editor Build가 성공했다. 생성 도구의 동일 Cube 재배정 멱등성 오류도 수정한 뒤 차량 BP·맵 Actor를 저장했고, 새 프로세스 `VALIDATION_OK`, Map Check 0/0과 `GroundConformingSuspension` 1/1을 통과했다. 자동화의 유일한 경고는 빈 시험 World의 기존 Recast 경고다.

## 2026-09-04 — AI-AUTO-TURRET-01 설치형·차량형 무인 자동포탑

- 사용자가 요청한 차량 위 무인 포탑과 지면 설치형 자동포탑을 기존 유인 MG 베이스로 구현했다. 유인 MG의 3분할 회전 계층, 정렬 후 발사, Projectile/Trace 선택, Damage·탄속·분산은 한 경로를 공유하고 자동 탐지만 새 계층에서 담당한다.
- `ADroneAutomaticTurret`는 0.2초 간격으로 살아 있는 Prototype Drone을 검색한다. 첫 획득 거리와 더 큰 이탈 거리를 분리하고 Visibility 시야선을 요구해 사거리 경계 깜박임과 벽 너머 획득을 막았다. 표적 사망·이탈·차단 시 내부 MG 사용을 종료한다.
- `ADroneEmplacedAutomaticTurret`와 `ADroneVehicleAutomaticTurret`를 분리했다. 설치형은 높은 받침대와 저속/고피해 기본값, 차량형은 낮은 장착판과 긴 탐지·발사거리/빠른 연사 기본값을 사용한다. 값은 BP Class Defaults에서 교체 가능한 Greybox다.
- 차량형 Actor는 차량 Mesh Socket 또는 부모 Actor에 Attach해서 쓰며, Projectile과 Trace가 Attach Parent/Owner를 무시하도록 공통 MG 발사 경로를 보강했다. 탄환 Source에는 `AutomaticTurret`를 추가해 유인 MG 결과와 분리했다.
- `/Game/Drone/AI/AutomaticTurrets/Blueprints/BP_AutoTurret_Emplaced`, `BP_AutoTurret_Vehicle`를 생성했다. `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox` 우측 `(2600,1600)`에 설치형, `(2600,-1600)`에 차량 Carrier와 차량형을 배치했다. 차량형은 `AutoTurret_VehicleCarrier_Greybox`에 실제 Attach돼 있다.
- 재현용 `Tools/AssetMigration/BuildAutomaticTurretGreybox.py`는 두 BP와 소유 Actor 3개만 생성/검증하며 기존 맵 내용을 덮어쓰지 않는다. 읽기 전용 모드는 `DRONE_AUTO_TURRET_VALIDATE_ONLY=1`이다.
- `DroneEditor Win64 Development` Build 성공. `AutomaticTurretTargeting`, `SmartObjectFoundationDefaults`, `NPCGreyboxAssets` 3/3, 실제 맵 시작·종료 `NPCGreyboxPIE` 1/1이 통과했다. 전용 테스트는 Blocking Box가 시야를 가리면 획득하지 않고 Collision을 끄면 즉시 재획득하는 경로까지 확인했다. 자동화 보고서는 실패 0이며 빈 시험 World의 기존 Crowd/NavMesh 경고 1건만 있다.
- 화면 수동 확인은 남았다. 현재 포탑은 Prototype Drone만 적으로 보고 진영/우선순위·포탑 체력/파괴·최종 차량/포탑 Mesh·FX/SFX는 후속이다. 상세 조정법은 [`DRONE_AUTOMATIC_TURRET_GUIDE.md`](../ai/DRONE_AUTOMATIC_TURRET_GUIDE.md)에 기록했다.

## 2026-09-04 — 팀원 Plugin·Git·LFS 재현성 점검

- 중앙 저장소는 로컬·원격 모두 `6fd0e77`이고 작업 트리가 깨끗하다. 별도 `yook34/main=c845430`은 중앙의 정확한 조상이며 `18 Commit 뒤 / 0 Commit 앞`이지만, 이후 사용자가 팀원 작업 PC는 중앙 `gyeonliz/drone` 권한을 받아 중앙에서 직접 Pull한다고 확인했다. 따라서 이 Fork 상태를 팀원 증상의 원인으로 단정하지 않는다.
- 두 Head 사이에는 총 586개 파일 차이가 있고 그중 Content 520개, Source 61개다. AI, MG, Mission Flow, NPC/무기 Asset이 포함되므로 팀원 PC에서 기능과 화면이 다르게 열리는 직접 원인이 될 수 있다.
- 두 Head의 `Drone.uproject`와 `Plugins` 경로 차이는 0이다. 프로젝트 자체 `Plugins` 폴더와 Git Submodule도 없으므로 현재 확인 범위에는 공유되지 않은 Project Plugin이 없다.
- `Drone.uproject`가 명시한 UE 내장 Plugin 13개를 작업컴 UE 5.8.1 CL 56057345에서 대조했고 모두 존재했다. StateTree·SmartObjects·GameplayInteractions는 Runtime 의존성이고 ModelContextProtocol·Toolset 계열은 Editor 전용이다.
- 최근 Unreal 로그 20개에서 Plugin 로드 실패, `/Script` 누락, Unknown Class, Package Load 실패는 0건이었다. `Binaries`, `Intermediate`, `Saved`, `DerivedDataCache`는 정상적으로 Git 제외되며 PC마다 달라도 정상이다. 단, C++ 변경 뒤 각 PC에서 Project Files 재생성과 Editor Build가 필요하다.
- LFS 추적 Package는 4,563개이고 `git lfs fsck --pointers HEAD`가 통과했으며 중앙으로 Push할 LFS 객체가 없다. 팀원은 중앙 Branch를 Fast-forward한 뒤 `git lfs pull`을 실행해야 실제 Asset 본문을 받는다.
- Water는 현재 UE 설치에 존재하고 최근 로그에서 정상 Mount됐지만 `.uproject`의 직접 선언 목록에는 없다. 동일 5.8.1 환경에서는 현재 오류가 없으며, 팀원 동기화 뒤 Military Map에서 Water 관련 오류가 재현될 때만 명시 의존성 추가를 별도 변경으로 검토한다.
- 팀원 실행 순서는 새 [`DRONE_TEAM_SYNC_PLUGIN_CHECKLIST.md`](../git/DRONE_TEAM_SYNC_PLUGIN_CHECKLIST.md)에 고정했다. 먼저 원격/Commit/LFS를 맞추고, 그 뒤에도 재현될 때만 Plugin·생성 파일 문제로 분리한다.
- 두 번째 정밀 점검에서 `Drone.uproject`, `Config`, `Content`, `Source`, `Tools`, 향후 `Plugins`·`Build`에 Git Untracked/Ignore 필수 파일이 0개이고 외부 Junction/Symlink도 0개임을 확인했다. 현재 제외 대상은 `Binaries`, `Intermediate`, `Saved`, `DerivedDataCache` 등 재생성 항목뿐이다.
- Commit `6fd0e77`을 LFS Smudge 없이 별도 Worktree에 Checkout하자 `Binaries=False`, `Intermediate=False`, 필수 Untracked 0 상태였다. 그 상태에서 MSVC 14.51.36256으로 `DroneEditor Win64 Development`를 처음부터 Build해 `UnrealEditor-Drone.dll` 생성과 Exit Code 0을 확인했다. 검증 Worktree는 즉시 삭제했다. 따라서 DLL을 Git에 올리지 않아도 기능 소스는 재현되지만, 팀원이 Pull 뒤 빌드하지 않으면 기존 DLL 때문에 옛 기능처럼 보일 수 있다.
- Runtime 설정과 Source에는 PC 절대 경로가 없다. `Tools/AssetMigration/ImportRawDroneCandidates.py`만 `C:\에셋` 공급 원본을 가리키므로 이미 이식된 Asset 실행에는 영향이 없지만 다른 PC에서 원본 재수입은 재현되지 않는다.
- `/Script/Fab` 메타데이터가 Project의 Megascans Asset 4개에 남아 있고 작업컴에서는 별도 설치된 Fab 0.0.15 Editor Plugin이 Mount됐다. Fab가 없는 팀원 PC에서는 해당 4개의 재수입 메타데이터 경고 가능성이 있으나, 현재 Drone C++·MG·AI Runtime 기능 누락 원인은 아니다.
- 팀원 화면에서 사격 모션과 기관총 기능이 없다는 보고 뒤 중앙 파일을 재확인했다. 중앙 `6fd0e77`에는 `ABP_NPC_Rifle_Greybox` 473,761 bytes, `BS_NPC_Rifle_Locomotion` 49,269 bytes, 최신 `BP_SO_MGTurret` 26,966 bytes와 `DroneMGTurretStation`, `DroneNPCAnimInstance`, MG StateTree Source가 모두 있다. 이 기능들은 새 C++ 부모와 그 부모를 쓰는 Asset이 한 Commit에 묶여 있다. 팀원이 중앙을 직접 Pull했다면 `Plugins`보다 LFS 파일이 포인터로 남았는지와 Git에서 제외되는 `UnrealEditor-Drone.dll`을 Pull 뒤 새 Source로 재빌드했는지가 우선 확인 대상이다. 팀원 PC 자체 출력 전에는 원인을 확정하지 않는다.

## 2026-09-04 — AI-GAZE-01 감지·추적 시선/고개 회전·AI-MG-03 3분할 조준 기반

- 작업 시작 기준은 Unreal `main=origin/main=46f7f37`, 문서 `main=origin/main=b8799c3`이었다. 이후 사용자가 문서 최신화를 `2cc51f1`로 Commit·Push해 현재 문서 기준은 `main=origin/main=2cc51f1`이다. 작업 시작에는 `Lvl_MilitaryBase.umap`이 수정으로 표시됐지만 직접 수정·체크아웃하지 않았고 최종 내용 비교에서는 Git 변경이 아닌 것으로 정리됐다.
- `ADroneNPCAIController`에 감지 Actor·1초 Sight 유예·Search 마지막 위치를 잇는 독립 Gaze와 Yaw/Pitch 제한·보간을 구현했다. Gameplay AI Focus는 Slot 몸 회전과 경쟁하는 회귀가 확인되어 사용하지 않는다.
- `UDroneNPCAnimInstance`와 Editor 작성 도구를 추가하고 프로젝트 소유 `ABP_NPC_Rifle_Greybox`의 기존 Rifle Pose 뒤에 `spine_03`, `neck_01`, `head` 보정을 20/45/35%로 삽입했다. 사용자 화면 확인에서 좌우 회전 대신 위아래 까딱임만 보인 원인을 Manny Bone 로컬축으로 좁혀 세 Modify Bone을 Bone Space에서 Component Space로 교정·재저장했다. 공급사 AnimBP와 Friendly `ABP_Unarmed`는 건드리지 않았다.
- 감지 중 움직이는 Drone Actor를 계속 바라보고, 1초 유예에는 Gaze를 유지하며, 실종 확정 뒤 Search 중 마지막 위치를 바라본다. Search 완료·Drone 파괴·NPC 사망·UnPossess에서는 정면으로 복귀한다.
- 첫 Greybox 제한은 Yaw `±65°`, Pitch `-25°~+40°`, 추적 보간 `6.0`, 정면 복귀 `3.5` 후보로 기록했다. 최종값은 Rifle/MG/Cover 화면 확인 뒤 역할 BP에서 조정한다.
- 처음 포탑 Pivot을 범용 `ADroneSmartObjectStation`에 넣었던 구조를 수정했다. 범용 Station에서는 포탑 Component와 일체형 `StationMesh`를 제거하고, 새 `ADroneMGTurretStation`에만 `BaseMount → YawPivot → PitchPivot → Muzzle` 및 Engine Cylinder 기반 `BaseMesh / BodyMesh / BarrelMesh` 3개를 만들었다. `BP_SO_MGTurret` 한 개만 전용 부모로 이관했으며 다른 Smart Object는 영향을 받지 않는다.
- 임시 Base 원기둥은 `(0.65, 0.65, 0.40)`, Body는 `(0.45, 0.45, 0.35)`, Barrel은 `(0.12, 0.12, 1.10)`으로 잡았다. Cylinder 포신을 Pitch 90°로 눕혀 +X를 향하게 했고, Base는 고정·Body는 Yaw·Barrel과 Muzzle은 Pitch만 상속한다.
- 첫 통합 PIE에서는 AI Focus가 Slot Yaw를 덮어 MG 안정화가 실패했고, Focus 제거 뒤 통과했다. 3분할 첫 실행에서는 저장 BP의 Pitch Pivot이 옛 부모를 유지해 조준 갱신 2,431회에도 Yaw 오차 24.35°가 고정됐다. MG 전용 `OnConstruction`에서 정확한 Attachment를 복구하고 이미 동작 중인 Controller Tick에서 점유 포탑 조준을 계속 갱신하도록 한 뒤 통과했다.
- 사용자 추가 요구에 따라 처음에는 고정 Base 아래 `MGTurretOperatorAnchor`를 만들었으나, 몸체 회전을 직접 따르라는 최종 요구에 맞춰 Anchor를 `MGTurretYawPivot`의 자식으로 옮겼다. 사수는 기본 120cm 후방의 Anchor에 붙고 몸체가 돌면 후방 위치·몸 방향도 함께 돈다. 별도 `Operator Facing Yaw Offset`은 제거했으며 거리·좌우·높이만 `BP_SO_MGTurret > Class Defaults > Drone|AI|MG|Operator`에서 조정한다. Controller는 포탑 조준을 먼저 갱신한 뒤 같은 프레임에 사수를 정렬해 한 프레임 지연도 피한다. Smart Object Slot은 검색·배타 점유 기준으로만 남긴다.
- MG가 아닌 개인화기 `DroneDetected`·`UseCover` 상태는 몸 Yaw를 기본 초당 180°로 Drone 방향에 돌린 뒤 로컬 Gaze를 계산하도록 바꿨다. MG 이동·점유와 Patrol에는 적용하지 않아 포탑 Operator 방향이나 이동을 덮어쓰지 않는다.
- 첫 Editor Build는 새 지역 변수 `Character`가 `AController::Character`를 가린다는 C4458 한 건으로 멈췄고 변수명을 `CharacterPawn`으로 바로잡았다. 이후 Editor/Game Build 모두 성공했으므로 기능 소스 오류는 남아 있지 않다.
- `DroneEditor Win64 Development`, `Drone Win64 Development`, 저장 AnimBP·MG BP 새 프로세스 검증, Smart Object 6쌍 Validation과 `NPCGreyboxAssets`, `NPCPerceptionSearchPIE`, `SmartObjectFoundationDefaults`, `SmartObjectStationAssets`, `ProjectileBallistics` 집중 5/5가 성공했다. 디버그 계측 제거 뒤 최종 소스 그대로 `NPCPerceptionSearchPIE`를 한 번 더 실행해 11.42초, Exit Code 0으로 재통과했고 PIE 정상 종료까지 확인했다. 수동 화면 확인 전이라 `AI-GAZE-01`과 `AI-MG-03`은 Doing으로 유지한다.
- Operator·개인화기 Facing 추가 뒤 같은 집중 5종을 다시 실행해 5/5가 통과했다. 최종 Yaw 종속 Anchor 구조로 바꾼 뒤에도 MSVC 14.51.36256의 Editor/Game Build, `NPCGreyboxAssets`·`NPCPerceptionSearchPIE`·`ProjectileBallistics`·`SmartObjectFoundationDefaults`·`SmartObjectStationAssets` 5/5, 저장 `BP_SO_MGTurret`과 Smart Object 6쌍 읽기 전용 Validation이 다시 성공했다. 확장 PIE는 MG 사수의 Anchor XY 2cm 이내·몸체 종속 방향 정렬과 개인화기 병사의 Drone 방향 5° 이내 몸 정렬, MG 발사·Cover 사격·Search 회귀를 함께 확인했다.
- 기관총 최종 연결 기준은 새 [`DRONE_MG_TURRET_3PART_GUIDE.md`](../ai/DRONE_MG_TURRET_3PART_GUIDE.md)에 기록했다. `Lvl_MilitaryBase.umap`은 이 작업에서 직접 열거나 덮어쓰지 않았고 최종 Git 변경 목록에도 없다.

## 2026-09-04 — AI-ACCURACY-01 사격 분산·AI-ANIM-TEMP-01 무장 자세 수정

- 기존 Rifle·MG는 목표 중심으로 정확히 발사했고 Shotgun은 중앙 1발과 원뿔 테두리의 결정적 배치였다. 사용자 의도에 맞춰 세 무기 모두 탄환마다 원뿔 내부의 무작위 방향을 고르도록 통일했다.
- 기본 반각은 Rifle `2.5도`, Shotgun `6도`, MG `3.5도`다. 역할 BP Component Details에서 직접 바꾸거나 `ConfigureAccuracyGreybox`, `ConfigureMGTurretAccuracyGreybox` BP Node로 바꿀 수 있으며 0도는 정확 사격이다.
- Projectile과 보존된 즉시 Trace 경로가 같은 분산 규칙을 사용한다. MG Pivot은 표적 중심을 계속 바라보고 탄환 방향만 흔들려 외형 조준과 명중률을 분리했다.
- Rifle 회귀 테스트는 장애물·Damage 계약을 안정적으로 확인하기 위해 0도를 명시한다. 별도 검증은 무작위 Rifle/Shotgun 방향이 설정 원뿔을 벗어나지 않는지 확인한다.
- 첫 임시 연결은 `MM_Rifle_Fire`, `MM_Rifle_Reload`를 `ABP_Unarmed`의 `DefaultSlot`에서 재생했지만, 화면에서 무장 자세가 없고 0.533초 발사 동작을 0.25초마다 재시작해 떨리는 문제가 확인됐다.
- `/Game/Drone/AI/Animation/ABP_NPC_Rifle_Greybox`와 `BS_NPC_Rifle_Locomotion`을 프로젝트 소유 Asset으로 만들었다. Hostile Rifle·Shotgun은 Rifle ADS Idle, 8방향 Walk/Jog와 Rifle Jump를 사용하고 Friendly만 기존 Unarmed를 유지한다.
- 발사 가산 Sequence 기본 Play Rate를 `2.4x`로 설정해 약 0.222초 안에 끝낸다. 역할 BP에서 Fire/Reload Asset·Play Rate를 바꾸거나 임시 재생을 끌 수 있다.
- `DroneEditor Win64 Development` Build 성공. `NPCGreyboxAssets`, `WeaponContract`, `NPCPerceptionSearchPIE` 3/3과 새 Editor 프로세스의 저장된 Rifle Idle·27개 Rifle BlendSpace Sample·Hostile/Friendly AnimBP 분리 검증이 성공했다. 손 위치·총기 정렬과 반복 동작은 화면 육안 재확인이 남았고 전체 자동화·Blueprint 전체 Compile은 반복하지 않았으며 Commit·Push하지 않았다.

## 2026-09-03 — AI-BALLISTIC-01 회피 가능한 Projectile

- 기존 개인 무기와 MG는 발사 즉시 맞는 Visibility Trace였다. 드론이 발사 뒤에도 이동으로 회피할 수 있도록 `ADroneNPCProjectile` 공용 탄환을 추가했다.
- 기본 탄속은 Rifle `4,500 cm/s`, Shotgun `3,500 cm/s`, MG `5,500 cm/s`다. 최종 난이도 값이 아니며 `ConfigureProjectileBallisticsGreybox`와 `ConfigureMGTurretProjectileGreybox` 또는 BP Class Defaults에서 조정한다.
- Projectile은 Actor Tick·Chaos 물리 Simulation 없이 `ProjectileMovementComponent`의 Sweep 충돌을 사용한다. 지정 사거리 비행 시간에 0.25초 여유를 더한 뒤 자동 제거되어 누적되지 않는다.
- Rifle은 탄환 1개, Shotgun은 기존 결정적 Spread 방향마다 탄환을 한 개씩 Spawn한다. 발사자와 MG 사용자는 이동 충돌에서 제외하고, 현재 지정한 Target에 맞았을 때만 기존 Damage를 적용한다.
- Engine 기본 Sphere는 구매 에셋 전 이동 확인용이다. 최종 Mesh/Tracer/Niagara/Sound는 BP 파생 Projectile과 기존 `OnWeaponFired`에서 표현만 연결한다.
- 즉시 Rifle/Shotgun Trace 코드는 삭제하지 않고 `bUseProjectileBallistics=false` 선택 경계로 보존했다. 회귀 테스트는 이 모드를 명시적으로 사용한다.
- 첫 빌드 실패 표시는 소스 오류가 아니라 UnrealBuildTool의 AppData Trace 로그 교체 권한 거부였다. 권한 해소 후 `DroneEditor Win64 Development` Build가 성공했다.
- 추가 충돌 결과 검사에서 Component Delegate의 생성자 연결이 시험 인스턴스에 적용되지 않는 문제를 발견했다. CDO 복제에 의존하지 않는 Actor `NotifyHit` 경계로 교체하고 Rifle/Shotgun Target impact가 무기 적중 카운터까지 돌아오는 것을 재검증했다.
- `Drone.AI.ProjectileBallistics`, `RifleTrace`, `ShotgunTrace`, `WeaponContract`, `NPCPerceptionSearchPIE` 5/5가 성공했다. 전체 `Drone.`·Blueprint 전체 Compile·LFS는 반복하지 않았고 Commit·Push도 하지 않았다.

## 2026-09-03 — FLOW-03 미션 선택·설명·시작 완료

- Flow Subsystem이 등록 Mission ID를 이름순으로 반환하도록 해 로비가 `TMap` 내부 순서나 별도 문자열 목록을 소유하지 않게 했다.
- 현재 한 개의 Training Mission을 `MissionSelectButton`으로 표시하고, 선택 뒤 이름·설명·지역·난이도는 `DA_Mission_Tutorial_Training`에서 읽는다.
- 하단 `StartMissionButton`은 유효한 선택이 있을 때만 활성화되고 `ConfirmSelectedMission()`으로 `MissionTrailer` 상태까지만 전환한다. 실제 영상·Map 이동은 FLOW-04로 남겼다.
- WBP가 최종 Designer를 만들 때 사용할 이름 계약은 `MissionSelectButton`, `MissionSelectButtonText`, `MissionNameText`, `MissionDescriptionText`, `MissionMetaText`, `StartMissionButton`이다. Blueprint는 선택/확정 판정을 중복 구현하지 않는다.
- 최종 Drone Game/Editor Build와 `Drone.Flow` 3/3이 성공했다. PIE에서 잘못된 Mission ID 거부, Definition과 표시 이름·설명 일치, 중복 확정 거부, 같은 Root Widget 1회 생성을 확인했다.
- 이 시점에는 새 Asset을 추가하지 않아 Unreal 변경 경로 수는 26개로 유지했다. Commit·Push하지 않았고 당시 다음 카드는 `FLOW-04`였다. 최신 상태는 문서 상단을 따른다.

## 2026-09-03 — FLOW-02 시작 화면→로비 완료

- `UDroneGameFlowSubsystem::EnsureDefaultCatalog()`을 추가해 첫 Vertical Slice Drone을 먼저, Mission을 다음에 GameInstance 수명 Catalog로 등록한다. 같은 Asset의 반복 호출은 중복 항목을 만들지 않는다.
- 새 `ADroneFrontEndGameMode`는 `DefaultPawnClass=None`, 새 `ADroneFrontEndPlayerController`는 Root Widget 한 개와 UI 입력 수명만 소유한다.
- 새 `UDroneFrontEndRootWidget`은 정적 Opening 대체 화면과 Lobby 패널을 같은 인스턴스에서 전환한다. 실제 영상이 생기면 `FinishOpeningTrailer()`를 Media/Sequencer 종료 Callback에서 호출하고, `ReceiveFrontEndStateDisplayed`에는 Blueprint 표현만 붙인다.
- 실제 `/Game/Drone/FrontEnd/UI/WBP_DroneFrontEndRoot`, BP Controller/GameMode와 `/Game/Drone/Maps/Lvl_DroneFrontEnd`를 만들었다. WBP Designer는 최종 외형 미정이므로 비어 있고 현재는 C++ fallback Layout을 사용한다.
- `GameDefaultMap`을 `Lvl_DroneFrontEnd`로 바꿨지만 `EditorStartupMap`은 기존 Training Map을 유지했다. Front-end Map에서는 Drone 선택 전 Drone Pawn을 Spawn하지 않는다.
- 최초 Front-end Asset Create는 자산 저장까지 성공했으나 Python 검증에서 Generated Class API 이름을 잘못 사용해 종료 코드 3이 났다. `MathLibrary.class_is_child_of`로 검증만 수정한 뒤 새 프로세스 Validate가 성공했으며 생성 Asset은 덮어쓰지 않았다.
- 첫 PIE에서는 UIOnly Focus 대상이 Focusable이 아니어서 실패했다. Root Widget을 Focusable로 만든 뒤 `Drone.Flow.FrontEndPIE` 1/1이 성공했다.
- 최종 확인은 `Drone Win64 Development`, `DroneEditor Win64 Development`, Front-end Asset Validate와 `Drone.Flow` 3/3이다. Root 생성 1회, Opening→Lobby 단일 전환, 두 번째 전환 거부, Mission/Drone Catalog 각 1개, 선택 전 Drone 0대를 확인했다.
- 모든 변경은 로컬 미커밋이며 Commit·Push하지 않았다. 다음 카드는 `FLOW-03`이다.

## 2026-09-03 — FLOW-01 상태·Mission/Drone 데이터 계약 완료

- `UDroneGameFlowSubsystem`에 실행부터 결과까지 8개 상태, Mission/Drone 선택 Snapshot, 잘못된 순서와 중복 요청 거부 규칙을 구현했다.
- `UDroneDefinition`, `UDroneMissionDefinition` Primary Data Asset과 실제 `DA_Drone_Scout_Greybox`, `DA_Mission_Tutorial_Training`을 만들었다. 이는 첫 Greybox 값이며 최종 Drone 종류나 게임 규칙 확정이 아니다.
- `DroneEditor Win64 Development`, 저장 Asset 새 프로세스 Validate와 `Drone.Flow.Contract` 1/1이 통과했다.
- 후속 전투 표현을 위해 NPC Character에 `WeaponVisualComponent`, `WeaponMuzzleComponent`, BP 발사/재장전 표현 Event를 준비했다. 실제 Rifle/Shotgun Mesh·Animation·FX·SFX는 연결하지 않았다.
- 모든 변경은 로컬 미커밋으로 유지했다.

## 2026-09-03 — 프로젝트 통합 기획·개발 현황서

- 새 [`DRONE_PROJECT_PLANNING_BRIEF.md`](../planning/DRONE_PROJECT_PLANNING_BRIEF.md)에 세계관·플레이어 역할, 확정 Front-end 흐름, Tutorial/Story Mission, 한글 UI 수치, 구현/미구현, 폐기/보존, 기술 구조, Map 활용, FLOW-01~08 로드맵, 검증, 역할 분리와 보류 결정을 한 문서로 정리했다.
- 진행상황은 실제 `main=origin/main=6a18210`, Unreal 로컬 Smart Object 변경 8개와 기존 빌드·자동화·수동 미확인 기록을 기준으로 작성했다.
- Figma는 세계관·UI 방향 참고로만 구분하고 사람 Operator 조작이 구현된 것으로 표현하지 않았다.
- 이번 작업은 Markdown만 변경했고 Unreal Build·PIE·Asset 변경은 수행하지 않았다.

## 2026-09-03 — 사람 Operator 폐기와 Front-end Mission Flow 확정

- 사용자가 사람 Player Character 구상을 취소하고 새 흐름을 `게임 실행 → 시작 트레일러 → 로비 → 미션 레벨 선택 → 측면 미션 설명 → 하단 시작 → 미션 트레일러 → Map 진입 → Drone 선택 → Mission 시작 → 측면 목표 UI`로 확정했다.
- 기존 Operator↔Drone Possess/Camera 전환과 로비 NPC 대화 Mission 수령 카드는 폐기했다. 아직 해당 생산 코드를 만들지 않았으므로 제거할 Unreal 구현은 없다.
- 기존 Drone 조작·Telemetry·Tutorial 기록과 적 NPC·Smart Object·Rifle/Shotgun·MG·Cover·체력 기능은 Mission Map 내부 기능으로 재사용한다. 아군 NPC 생활 루틴은 보존하지만 Front-end 선행조건에서는 제외했다.
- 새 최우선 계획 [`DRONE_FRONTEND_MISSION_FLOW_PLAN.md`](../planning/DRONE_FRONTEND_MISSION_FLOW_PLAN.md)에 영속 Flow 상태, Mission/Drone Data Asset, 화면별 책임, Content 경계, `FLOW-00~08` 카드와 3회 반복 검증을 기록했다.
- 첫 Vertical Slice는 기존 `Lvl_DroneTraining`을 한 개 Tutorial Mission으로 등록하고 한 개 Drone만 허용해 흐름을 검증한다. MilitaryCamp·MilitaryBase·Battlefield 연결은 이 골격 뒤에 진행한다.
- Figma `Project:Droner`는 세계관과 UI 분위기 참고용으로 읽었고 수정하지 않았다. 최종 제목 통일은 보류했다.
- 이번 작업은 MD 기준선만 변경했다. Unreal Source·Asset·Build·PIE 결과는 추가하지 않았으며 새 Flow가 구현됐다고 표시하지 않는다.

## 2026-09-03 — AI-SO-TUNE-01 Smart Object 배치·방향 조정 보강

- 실제 수정 위치를 맵 Actor, Station Blueprint, Smart Object Definition, StateTree, C++ Station/Reservation/Controller/Task로 나눠 `DRONE_SMART_OBJECT_NPC_GUIDE.md` 상단에 빠른 표와 Editor 배치 절차를 추가했다.
- `SlotFacingPreview`를 `SmartObjectComponent` 아래에 부착해 Blueprint에서 Slot Offset을 조정할 때 Cyan 화살표도 같은 Transform을 따르게 했다.
- `ADroneNPCAIController::AlignPawnToReservedSlot()`을 추가해 예약 Slot의 Yaw를 Pawn과 Control Rotation에 적용했다. 순찰·아군 활동 공용 이동, Cover, MG 도착 경로에서 호출한다. Pitch/Roll은 지면 Character 기울어짐 방지를 위해 적용하지 않는다.
- Smart Object Foundation 기본 계약에 Preview의 Attach Parent 검증을 추가했다.
- Smart Object Setup Wrapper는 하드코딩된 C 드라이브 경로 대신 문서 저장소와 같은 상위 폴더의 `drone/Drone.uproject`를 자동 계산한다.
- 첫 Build 시 Unreal Editor가 `D:\JGY\project\drone\Drone.uproject`로 실행 중임을 확인해 저장되지 않은 작업 보호를 위해 강제 종료하지 않았다. 사용자 종료 뒤 `DroneEditor Win64 Development` Build가 성공했다.
- `NPCPerceptionSearchPIE`에 Pawn Yaw와 예약 Slot Yaw의 1도 이내 비교를 추가했다. MG 점유와 Cover 점유 경로를 직접 판정하며 `SmartObjectFoundationDefaults`의 Preview Parent 계약과 함께 2/2 성공, 경고·오류 0이다.
- 자동 계산 Wrapper로 Definition/BP 6쌍을 `Validate`해 모두 역할·Tag·Definition·MG Mesh 계약과 일치했다. 이제 Editor 화면에서 Cyan 화살표와 실제 NPC 도착 방향만 확인하면 `AI-SO-TUNE-01`을 Done으로 옮길 수 있다.
- 최종 Git 확인에서 `SO_Def_FriendlyBasePatrol`이 5,493 bytes에서 5,750 bytes로 바뀐 LFS 객체를 확인했다. 사용자 Editor 종료 저장인지 Headless 재직렬화인지 확정할 수 없어 변경을 삭제하지 않고 보존했다. 변경된 Definition 상태로 후속 NPC PIE가 통과했으며 Commit 전 Slot 설정을 Editor에서 확인한다.

## 2026-09-03 — AI-MG-02 Occupy·Aim·Fire·Release 핵심

### 2026-09-03 공유 기준선 재확인

- 사용자가 전투 Greybox와 표현 이벤트 변경을 Commit·Push해 Unreal `main=origin/main=6a18210`, 문서 `main=origin/main=2c99f00`이며 두 작업 트리가 Clean임을 확인했다.
- `6a18210`에는 AI-MG-02, HP-01, AI-COVER-01, AI-COMBAT-END-01, AI-AMMO-01, AI-VIS-01A에 해당하는 코드·StateTree·Greybox Map 변경이 포함된다.
- 각 기능의 단계별 Editor Build와 집중 테스트 결과는 유지한다. 이 대형 Commit 이후 전체 `Drone.` 회귀·Blueprint 전체 Compile·LFS 검증은 새로 실행하지 않았으므로 완료 근거를 과장하지 않는다.
- 다음 구현 후보는 `AI-VIS-01B`: Manny Rifle 임시 표현과 MG FX/SFX 연결이다. Shotgun Mesh와 최종 Soldier/Insurgent 외형은 후보·Retarget 확인 전까지 미정이다.

### AI-VIS-01A 자산 호환성 감사·Blueprint 표현 이벤트

- 새 읽기 전용 `Audit-DroneNPCVisualAssets.py`와 실행 Wrapper로 후보 Asset의 Load, Skeleton, Animation 수량, Weapon Mesh 수량을 반복 감사할 수 있게 했다.
- Manny Rifle Animation은 38개이고 AR4·MG·Niagara Muzzle Flash·Sound Cue 후보는 정상 로드된다. FPS Weapon Mesh는 70개지만 이름으로 식별되는 Shotgun Weapon Mesh는 0개다.
- Modular Soldier/Insurgent는 Manny와 Skeleton이 직접 일치하지 않고 이식된 두 Root의 Animation Asset은 각각 0개다. 따라서 최종 진영 외형과 Retarget 결과를 확인하기 전에는 역할 Blueprint에 강제 적용하지 않았다.
- `UDroneNPCWeaponComponent`에 Blueprint용 `OnWeaponFired(WeaponType, TraceStart, AimPoint)`와 `OnReloadCompleted(WeaponType, CurrentAmmo, Capacity)`를 추가했다. Rifle은 Trace당 1회, Shotgun은 Volley당 1회이며 실패/거절 요청은 방송하지 않는다.
- `DroneEditor Win64 Development`와 WeaponContract·RifleTrace·ShotgunTrace 3/3이 통과했다. 전체 자동화·Blueprint Compile·LFS는 반복하지 않았다.
- `6a18210` Push 전 당시 Unreal 변경은 `git status --porcelain -uall` 기준 30개 파일, 문서 저장소는 12개 파일이며 모두 로컬 미커밋이었다.

### AI-AMMO-01 Rifle·Shotgun 탄창·재장전

- `UDroneNPCWeaponComponent`에 현재 탄약, 장비별 탄창 용량, Blueprint 조회 함수와 시험 설정 함수를 추가했다. 기본 Rifle 30발, Shotgun 8발은 최종 밸런스가 아니다.
- Rifle은 실제 Trace 한 번에 한 발, Shotgun은 Volley 한 번에 Shell 한 발을 소모한다. 장애물에 막혀도 발사한 탄은 소모하지만 사거리·Cooldown으로 거부된 요청은 소모하지 않는다.
- 마지막 탄 뒤 Timer·Target을 정리하고 빈 탄창 발사를 거부한다. `Reload()`는 소모된 탄창만 즉시 채우며, Hostile Controller는 교전 지속 중 빈 탄창이면 Reload 후 같은 공용 발사 경로를 재개한다.
- 예비 탄약, 재장전 시간·Animation·FX·SFX는 이번 카드에 넣지 않았다.
- Editor Build 성공. 한 Editor 실행에서 `NPCPerceptionSearchPIE`, `RifleTrace`, `ShotgunTrace`가 통과했고 Owner 없는 순수 계약 객체의 생존 검사 오류를 수정한 뒤 `WeaponContract` 1/1도 최종 통과했다.
- 전체 테스트·Blueprint Compile·LFS, Commit·Push는 실행하지 않았다.

### AI-COMBAT-END-01 Drone 파괴 교전 종료

- `ADronePrototypePawn`에 BlueprintAssignable `OnDroneDestroyed`와 1회 발생 진단값을 추가했다. Health 사망 Event가 입력·이동·충돌을 끄고 Perception Source를 해제한 뒤 이 신호를 보낸다.
- 현재 Drone을 감지하던 살아 있는 Hostile은 개인 무기, 이동, MG 사용자 상태, Cover/MG 예약, 마지막 감지 위치를 즉시 정리한다. 파괴 표적은 수색하지 않고 기존 StateTree Lost 전환을 이용해 Patrol로 복귀한다.
- 사망한 Hostile과 Friendly는 파괴 응답 대상에서 제외했다. 사망 뒤 추가 Damage도 Health/Drone 파괴 Event를 다시 발생시키지 않는다.
- 구현 중 성공 Sight가 곧바로 Lost로 처리될 수 있던 조건 분기 오류와 StateTree 강제 재시작 시 이전 감지 Event가 남던 문제를 집중 PIE에서 발견해 수정했다.
- 최종 `DroneEditor Win64 Development`와 확장 `Drone.AI.NPCPerceptionSearchPIE` 1/1이 통과했다. 테스트는 기존 MG·Cover·사망 교대·Search 복귀 뒤 재교전, Drone 파괴, 모든 전투 자원 해제, Patrol 복귀와 Event 1회를 연속 검증한다.
- 전체 테스트·Blueprint 전체 Compile·LFS는 반복하지 않았고, Commit·Push도 하지 않았다.

### AI-COVER-01 MG 실패 병사 엄폐 대응

- Hostile StateTree에 `ClaimCoverSlot`, `MoveToCover`, `UseCover`를 추가해 총 12개 상태로 확장했다. MG Claim 실패는 Cover로 가고 Cover도 실패하면 기존 DroneDetected 개인 무기 상태로 내려간다.
- Controller에 Cover 1-Slot Claim·NavMesh 이동 완료·Occupied·개인 무기 유지·Abort 수명주기와 관측 카운터를 추가했다.
- `Lvl_NPCSmartObjectGreybox`에 `BP_SO_Cover` 두 개를 배치했다. 작성 도구는 기존 Actor를 덮어쓰거나 중복 생성하지 않고 StateTree·두 Station을 갱신/검증한다.
- MG 사수가 사망하면 Cover 중인 다른 MG 가능 Hostile이 Root 감지 Event로 전환돼 Cover를 해제하고 비어진 MG를 재Claim한다.
- Editor Development Build와 StateTree/Map Upgrade 검증이 성공했다. 최신 `Drone.AI.NPCPerceptionSearchPIE` 1/1은 MG 1명·Cover 1명, Cover Occupied 개인 무기, 사망 뒤 Cover→MG 교대, DroneLost Search→Patrol을 통과했다.
- 전체 테스트·Blueprint 전체 Compile·LFS는 반복하지 않았다. 소스/에셋 27개와 문서/도구는 사용자 요청에 따라 로컬 미커밋으로 유지한다.

### HP-01 및 사망 뒤 MG 재점유 마감

- NPC와 Drone에 공통 `UDroneHealthComponent`를 부착했다. 기본·최대 체력은 모두 100이며 0 이하에서 사망 Event를 정확히 한 번 보내고 이후 Damage를 무시한다.
- Rifle 발당 10, Shotgun 적중 Pellet당 8, MG 발당 8의 Greybox Damage를 표준 `UGameplayStatics::ApplyDamage` 흐름으로 연결했다. 모두 최종 밸런스가 아닌 시험값이다.
- NPC 사망 시 이동·충돌·개인 무기·StateTree·MG 사용·Smart Object Claim을 정리한다. 사망한 MG 사수가 놓은 Slot은 감지 중인 다른 MG 가능 Hostile이 다시 Claim·Occupied하여 조준·사격을 이어간다.
- Drone 사망은 입력 Mapping·이동·충돌을 정지하고 기체는 현 위치에 남긴다. 래그돌·폭발·시체 제거·Respawn·Mission 실패 화면은 후속 표현/게임 규칙이다.
- `UDroneFlightHUDWidget` 우측 상단 동적 패널에 `기체 내구도 현재/최대`와 `파괴됨`을 Event 기반으로 표시하고 PlayerController가 Possess Pawn의 Health Source를 연결·정리한다.
- `DroneEditor Win64 Development`가 성공했다. 집중 `Drone.AI.NPCPerceptionSearchPIE`는 100/100 시작, 사망 1회, MG 해제·두 번째 적 재점유·생존자 Search/Patrol 복귀를 통과했고 `Drone.UI.FlightHUDTelemetryBinding`은 100→70→파괴 표시와 Delegate 해제를 통과했다.
- 전체 27개·Blueprint 전체 Compile·LFS는 사용량 절약 원칙에 따라 반복하지 않았다. Unreal 소스 21개와 문서는 Commit·Push하지 않고 로컬에 유지한다.

- Reservation Component에 Occupied 판정과 예약한 Smart Object 소유 Actor 조회를 추가했다.
- MG Station에 `MGTurretAimPivot`과 사용자·표적 수명주기를 추가했다. 6,000cm·0.15초 Greybox Visibility Trace를 수행하고 Blueprint가 외형·Muzzle Flash·Sound를 연결할 수 있도록 사용 상태와 발사 Event를 노출했다.
- Controller는 도착한 Claim을 Occupied로 바꾸고 활성 Station을 보관한다. 기존 저장 StateTree Struct 경로를 유지한 채 Hold Task가 실제 MG 시작·조준·Cooldown 사격을 실행한다.
- DroneLost·Task 실패·UnPossess·EndPlay에서는 Station 사용자와 Occupied Slot을 정리한다. MG 사용 중 개인 Rifle 발사는 중단된다.
- `DroneEditor Win64 Development`와 직접 관련 `Drone.AI.NPCPerceptionSearchPIE` 1/1이 통과했다. 테스트는 Occupied, 사용자·표적·Aim Point, Trace 발생, Shotgun Fallback, Friendly 비무장, DroneLost 해제를 확인한다.
- 이 핵심 구현 뒤 위 HP-01 단계에서 Damage·사망·다른 AI 재점유 완료 조건까지 마감했다.

## 2026-09-02 — AI-MG-01 MG 1-Slot Claim·Move

- `ADroneNPCAIController`에 `MoveToMGTurret`, `HoldMGTurret` 관측 상태와 Claim·도착 카운터를 추가했다. MG 사용 가능 Hostile만 기존 MGTurret Activity Tag와 Reservation Component로 가장 가까운 빈 Slot을 예약한다.
- 새 Native StateTree Task가 Claim 1회, 예약 위치까지 NavMesh 이동, 도착 뒤 Claim 유지를 각각 담당한다. 권한 없음·빈 Slot 없음·이동 실패는 기존 `DroneDetected` 개인 무기 상태로 대체한다.
- 반복되는 성공 Sight 자극은 최초 감지 Event를 다시 보내지 않아 이동 중 Claim을 풀지 않는다. DroneLost·이동 실패·StateTree 중단·UnPossess에서는 이동과 예약을 정리한다.
- 저장된 `ST_NPC_HostilePatrol`을 6-State에서 9-State로 업그레이드했다. 새 문서 도구 `Invoke-DroneHostileMGTurretStateTreeSetup.ps1`의 Upgrade와 새 프로세스 Validate가 모두 성공했다.
- NPC Greybox PIE는 MG 운영자 정확히 1명, 유효 예약 정확히 1개, Claim·도착 카운터 1회, 도착 뒤 개인 무기 정지, Shotgun Hostile의 개인 무기 Fallback과 Friendly 비무장을 검증한다.
- Game/Editor Development Build, AI 11/11과 전체 `Drone.` 27/27, Blueprint 0 errors·0 Blueprint warnings·0 failed loads, LFS fsck를 통과했다. Rifle 빈 World 경고 1건과 공급사 Pose GUID 28건·MCP 고지 1건은 기존과 같다.
- Unreal 한글 Commit `249d6cd` (`기능: 적 AI의 MG 터렛 예약과 이동 구현`)을 `origin/main`에 Push했다. 다음 카드는 `AI-MG-02`이며 Occupied·Aim·Fire·Release와 사망 뒤 재점유를 구현한다.

## 2026-09-02 — AI-WPN-02 Rifle 확정·AI-WPN-03 Shotgun Greybox 사격

- 최신 `98f67d0`에 들어온 Rifle Visibility 단일 Trace, 4,000cm 사거리, 0.25초 Cooldown과 `Drone.AI.RifleTrace`를 Editor에서 빌드했다. 전용 테스트는 개방 표적 명중, 장애물 차단, 사거리 밖 거부와 즉시 재발사 Cooldown을 통과했다.
- 첫 전체 회귀에서는 수동 Sight Broadcast가 실제 Sight 반경을 적용하지 않아 기존 공용 Weapon 경로 테스트가 Rifle 사거리에서 실패했다. Rifle/Shotgun 전용 테스트가 사거리를 검증하도록 두고, 공용 경로 테스트에서는 시험용 사거리를 넓혀 Target/Aim Point 계약만 분리 검증했다. 수정 뒤 Rifle 기준 전체 26/26이 통과했다.
- `AI-WPN-03`으로 Shotgun 1,600cm 사거리, 0.9초 Cooldown, 8 Pellet, 6도 원뿔 반각 Greybox를 같은 `UDroneNPCWeaponComponent`에 추가했다. 첫 Pellet은 중심, 나머지는 원뿔 가장자리에 균등 배치해 실행마다 같은 Spread를 재현한다.
- `Drone.AI.ShotgunTrace`는 한 Trigger가 설정된 Pellet 수만큼 Trace를 만드는지, 0도 Spread 전탄 명중, 장애물 전탄 차단, 사거리 밖 거부, 즉시 재발사 Cooldown, Spread Endpoint 분리와 Rifle 코드 분리를 검증했다.
- Game 빌드에서 Rifle/Shotgun 자동화가 Editor 전용 `AutomationEditorCommon` 헤더를 포함하던 기존 경계 오류를 발견했다. 두 테스트를 `WITH_DEV_AUTOMATION_TESTS && WITH_EDITOR`로 제한해 런타임 코드와 Editor 테스트를 분리했고 `Drone Win64 Development`와 `DroneEditor Win64 Development`가 모두 성공했다.
- 최종 AI 11/11과 전체 `Drone.` 27/27이 성공했다. Rifle 테스트의 빈 World에서 RecastNavMesh가 없다는 예상 경고 1건만 있으며 실패는 0이다. `CompileAllBlueprints`는 0 errors / 0 Blueprint warnings / 0 failed loads이고 전역 Summary의 기존 Battlefield Pose GUID 28건과 MCP EULA 1건은 별도 경고다. `git lfs fsck`와 `git diff --check`도 통과했다.
- Unreal 한글 Commit `0d92a5f` (`기능: 샷건 펠릿 사격과 무기 테스트 보강`)을 `origin/main`에 Push했다. 실제 Damage·탄약·Animation·FX·SFX는 미구현이며 다음 활성 카드는 `AI-MG-01`이다.

## 2026-09-02 — Rifle Trace 착수·MilitaryBase 강/도로 구조 확인

- Unreal `origin/main=c7f116f`까지 사용자가 저장·Push했고 두 저장소 모두 작업 트리가 깨끗한 상태에서 재개했다.
- `AI-WPN-02` 코드에 Rifle Visibility 단일 Trace, 4,000cm 시험 사거리, 0.25초 Cooldown, 장애물 차단·디버그 선·상태 정리를 추가하고 `Drone.AI.RifleTrace` 자동화 테스트를 작성했다. Editor 빌드는 성공했으나 전용 테스트 결과 로그는 다음 확인 대상이다.
- `Lvl_MilitaryBase`의 강은 WaterBody가 아니라 `Landscape` 내부 `SM_RiverBank` SplineMesh 166개와 물 재질 슬롯으로 구성된다. 강 반사광은 별도 `MI_DecalCaustic_Inst` 9개 및 Wetness Decal 계열이며, Sphere Reflection Capture 9개도 별도로 존재한다.
- 도로는 별도 Road Actor가 아니라 Landscape 높이/재질 레이어 방식으로 보이며 `rockyPath`, `forrestPath`, `brownMud` Target Layer를 Paint/Layer Debug로 확인하는 절차를 정리했다. 맵 삭제·저장은 수행하지 않았다.
- 다음 확인: Rifle 전용 자동화 결과 판정 후 장애물·사거리·Cooldown이 모두 통과하면 `AI-WPN-02`를 완료하고, 실패 시 코드만 수정한다.

## 2026-09-02 — Friendly/Hostile NPC 선택 PropertyEditor 크래시 수정

- `Lvl_NPCSmartObjectGreybox`에서 Friendly 또는 Hostile NPC Actor를 선택하면 `UnrealEditor_PropertyEditor` 호출이 반복된 뒤 `EXCEPTION_STACK_OVERFLOW`로 Editor가 종료되는 현상을 사용자와 자동 선택으로 동일 재현했다. 맵 로드와 무선택 상태는 정상이므로 플레이 로직이 아니라 Details 패널 생성 경로로 범위를 좁혔다.
- Friendly도 동일하게 재현돼 적 전용 Weapon이나 Hostile StateTree가 아니라 `ADroneNPCCharacter` 공통 Details 표시 경로 문제로 판정했다.
- 공통 컴포넌트와 Weapon 진단값의 다단계 `Category`를 단일 카테고리로 바꾸고, `FDroneNPCProfile`의 `ShowOnlyInnerProperties` 자동 인라인 표시를 제거했다. 값·저장 구조·런타임 공개 API와 AI 동작은 변경하지 않았다.
- `DroneEditor Win64 Development`가 MSVC 14.51.36256으로 성공했다. 사용자가 Friendly 선택 후 크래시가 없음을 확인했고, MCP로 `BP_NPC_Hostile_Rifle_C_0`을 정확히 선택한 뒤 12초 이상 Editor가 정상 생존했다.
- 엔진 내부의 어느 단일 메타데이터가 직접 원인인지는 추가 격리하지 않았다. 현재 확정 범위는 공통 NPC Details 메타데이터 조합에서 재현됐고 표시 단순화 후 해소됐다는 것이다.
- Unreal 변경은 `DroneNPCCharacter.h`, `DroneNPCProfileComponent.h`, `DroneNPCWeaponComponent.h` 3개이며 로컬 미커밋이다. 다음 기능 카드는 그대로 `AI-WPN-02` Rifle Greybox Trace다.

## 2026-09-02 — AI-PER-01 Hostile 감지·Search·순찰 복귀

- `ADroneNPCAIController`에 `Patrol`, `DroneDetected`, `Search` 관측 상태와 마지막 감지 위치, 감지·실종·Search 진입·완료 카운터를 추가했다. Hostile은 감지 즉시 이동을 멈추고 Smart Object Claim을 해제하며 Friendly는 같은 자극을 무시한다.
- `FDroneStateTreeDetectedTask`와 `FDroneStateTreeSearchTask`를 추가했다. 실종 뒤 마지막 위치로 이동을 요청하고 NavMesh 밖이면 제자리에서 3초 Search를 유지한 뒤 기본 순찰 Activity와 Claim 흐름으로 복귀한다.
- 저장된 `/Game/Drone/AI/StateTrees/ST_NPC_HostilePatrol`에 `DroneDetected`, `SearchLastKnownLocation` 상태와 `DroneDetected`/`DroneLost` Event 전환, Search 성공·실패의 Claim 복귀를 추가했다. Upgrade는 기존 정확한 4-State 자산만 수정하고 알 수 없는 확장 자산은 덮어쓰지 않는다.
- 문서 저장소에 `Setup-DroneHostilePerceptionStateTree.py`와 `Invoke-DroneHostilePerceptionStateTreeSetup.ps1`을 추가했다. Upgrade와 Validate 모두 성공했고 저장 자산의 Task·Event 연결을 검사한다.
- 새 `Drone.AI.NPCPerceptionSearchPIE`는 Hostile 2명 감지·예약 해제, Friendly 2명 무반응, Hostile 실종·Search 진입, Search 완료·순찰 작업 재개와 Friendly 루틴 지속을 검증한다. 실제 Sight의 재감지와 수동 Lost 자극이 경합하지 않도록 Lost 뒤 시험 Pawn만 LoseSight 범위 밖으로 격리한다.
- 최종 `DroneEditor Win64 Development`와 `Drone Win64 Development` Build가 성공했다. AI `8/8`은 모두 무경고·무오류, 전체 `Drone.`은 `24/24`로 23개 무경고와 기존 `PIEInputLifecycle` RecastNavMesh 경고 포함 성공 1개다.
- `CompileAllBlueprints`는 `0 errors / 0 warnings / 0 failed loads`다. 전역 Summary의 기존 Battlefield Pose GUID와 MCP EULA 고지 29건은 Blueprint 결과 집계와 분리한다. `git lfs fsck`도 통과했다.
- 사용자가 Editor 화면에서 Hostile 정지→Search→순찰 복귀와 Friendly 지속을 직접 확인해 수동 Pass 처리했다.
- 공유 기준은 계속 `origin/main=2fcfb04`다. Unreal·문서는 로컬 `main` 위 미커밋 변경이며 자동 Commit·Push하지 않았다.
- 다음 활성 카드는 `AI-WPN-01` 공용 Weapon 계약으로 이어서 완료했다.

## 2026-09-02 — AI-WPN-01 공용 Weapon 계약

- `UDroneNPCWeaponComponent`를 추가해 Rifle·Shotgun 공통 `ConfigureWeapon`, `CanFire`, `StartFire`, `StopFire`, `Reload` 호출과 Target Actor·Aim Point 상태를 한 곳에서 관리한다.
- `ADroneNPCCharacter`가 Weapon Component를 소유하고, Controller는 Possess 때 NPC Profile의 Weapon Type을 구성한다. Hostile Controller는 `DetectedDrone`에서 Target과 Aim Point를 한 번만 만들어 Rifle·Shotgun 분기 없이 같은 경로로 전달한다.
- 감지 실종과 UnPossess에서는 발사 상태를 정리한다. Unarmed와 잘못된 Target은 거부하며 Rifle/Shotgun별 Trace·Damage·탄약·Cooldown·Pellet·Spread는 후속 카드 범위로 남겼다.
- `Drone.AI.WeaponContract` 자동화 테스트를 추가하고 NPC Greybox PIE를 확장해 Rifle·Shotgun의 같은 Target/Aim Point 경로, Friendly 비발사, Lost 시 발사 정리를 검증했다.
- 최종 `DroneEditor Win64 Development`와 `Drone Win64 Development` Build가 성공했다. AI `9/9`은 모두 무경고·무오류, 전체 `Drone.`은 `25/25`로 24개 무경고와 기존 `PIEInputLifecycle` RecastNavMesh 경고 포함 성공 1개다.
- 이번 카드는 Blueprint 자산을 수정하지 않아 전체 Blueprint Compile을 반복하지 않았다. 직전 `0 errors / 0 warnings / 0 failed loads`와 이번 자동화의 NPC Blueprint 로드 성공을 기준으로 유지한다.
- 공유 기준선은 `origin/main=2fcfb04`이며 Unreal·문서 로컬 `main`의 변경은 Stage·Commit·Push하지 않았다. 다음 활성 카드는 `AI-WPN-02` Rifle Greybox Trace다.

## 2026-09-02 — Generate 이후 DroneEditor Unity 빌드 수정

- 사용자가 AI-PER-01·AI-WPN-01과 문서를 Push해 Unreal `main=origin/main=2054d6f`, 문서 `main=origin/main=356d942`가 됐다.
- 생성 폴더를 정리하고 프로젝트 파일을 다시 만든 뒤 Editor 자동 컴파일에서 `DroneNPCPatrolStateTreeTasks.cpp`와 `DroneNPCPerceptionStateTreeTasks.cpp`의 익명 Namespace 헬퍼 `GetDroneController`가 Unity Translation Unit 안에서 중복 정의되는 오류를 확인했다.
- Perception 파일의 헬퍼를 `GetPerceptionDroneController`로 고유화했다. 런타임 API나 동작은 바꾸지 않았다.
- Generate가 `.vsconfig`의 세부 MSVC Component를 UE 5.8 권장 14.50으로 갱신했다. 실제 Build는 설치된 MSVC 14.51.36256을 사용했고 비선호 버전 주의 메시지만 남긴 채 `DroneEditor Win64 Development`가 성공했다.
- 이 수정과 `.vsconfig` 자동 갱신, 본 기록은 새 로컬 미커밋 변경이다.

## 2026-08-28 — 팀원 환경 변경 검증·정리와 AI-FRIEND-01

- 중앙 `main`을 팀원 변경 `852e6e6`까지 Fast-forward하고 LFS Object 78개를 내려받아 `git lfs fsck`를 통과했다.
- 중앙 환경 맵 3종을 새 Editor 프로세스에서 실제 로드했다. Camp 추가 외부 의존성 0, Base는 기존 `T_Linear_Grad`, Battlefield는 기존 Manny/Quinn과 새 `M_Enemy`, `M_Start`, `M_Target`만 참조하며 누락은 0이다.
- 읽기 전용 `Audit-DroneEnvironmentDependencies.py`를 추가하고 엄격한 환경 검증 허용 목록에는 확인된 세 Material만 명시했다. 수정한 검증은 세 맵 모두 성공했다.
- 팀원 변경의 `.vsconfig`를 UE 권장 14.50 구성으로 복원하고 `Drone.cpp`의 `//test`를 제거했다. 바이너리 환경 맵·Fab 자산·시험 맵은 삭제하지 않았다. 기능 `f8c8568`, Merge `888414f`로 중앙에 Push했다.
- `/Game/Drone/AI/StateTrees/ST_NPC_FriendlyBaseRoutine`을 생성했다. 상태는 Friendly Claim → 공용 Move → 공용 Wait → Friendly Release 네 단계다.
- Friendly Controller는 Base Patrol과 Ambient를 번갈아 먼저 시도하고, 빈 선호 Slot이 없으면 다른 아군 활동으로 대체한다. 직전 지점 반경 250 cm를 우선 피하며 Smart Object의 배타 Claim을 사용한다.
- Greybox Friendly 2명 각각이 2회 이상 완료하고 서로 다른 2지점 이상과 두 Activity 종류를 모두 방문하도록 `Drone.AI.NPCBaseRoutinesPIE`에서 검증했다. Hostile 2명의 기존 순찰도 같은 PIE에서 회귀 확인했다.
- Game/Editor Build 성공, AI 7/7 경고·오류 0, 전체 `Drone.` 23/23 성공이다. 22개는 무경고, 기존 `PIEInputLifecycle` 한 개만 예상 RecastNavMesh 경고를 포함한다.
- Blueprint Compile은 `0 errors / 0 warnings / 0 failed loads`다. 전역 Summary의 기존 Battlefield Pose GUID와 MCP 고지 경고 29건은 Blueprint 결과와 분리한다.
- 새 StateTree는 Git LFS 대상이며 LFS fsck를 통과했다. 기능 `b5b733f`, Merge `2fcfb04`를 한국어 메시지로 `origin/main`에 Push했다.
- 다음 기능 카드는 `AI-PER-01`이다. 현재 드론 감지는 예약을 안전 해제하지만 Search·Return·Rifle/Shotgun·MG 전환은 아직 구현하지 않았다.

## 2026-08-28 — 팀원 Fork 원격 감사와 문서 최신화

- 문서 저장소를 먼저 `main=origin/main=602c863`까지 Fast-forward한 뒤 최신 Unreal 기준선 `095dda7`과 현재 작업 순서를 대조했다. 이 항목의 문서 변경은 사용자가 직접 Commit할 예정이며 자동 Commit·Push하지 않았다.
- 중앙 `gyeonliz/drone`의 `main=095dda7`, 팀원 Fork `Yook34/drone`의 `main=0ff4fb1`을 원격에서 확인했다. Merge Base는 `095dda7`, 좌우 차이는 중앙 0 / Fork 4 Commit이다.
- 팀원 Fork 순 변경에는 `Lvl_Battlefield.umap`, `M_Enemy`, `M_Start`, `M_Target`과 함께 `.vsconfig`, PC별 `Drone.uproject` Engine Association GUID, `Drone.cpp`의 `//test`가 섞여 있다.
- 팀원 PC에서 Fork를 Clone해 `origin=Yook34/drone`인 상태라면 GitHub Desktop과 `git push origin`이 팀원 저장소로 전송되는 것이 정상이다. Git 작성자 설정이나 로그인 계정이 Remote URL을 자동으로 중앙 저장소로 바꾸지는 않는다.
- 중앙 직접 협업은 `origin=gyeonliz/drone`, 보존할 Fork는 `fork=Yook34/drone`으로 구성한다. 중앙 쓰기 권한이 없다면 `origin=Yook34/drone`, `upstream=gyeonliz/drone`으로 두고 Pull Request를 사용한다.
- 현재 Fork `main`을 중앙 `main`에 바로 Push하거나 전체 Merge하지 않는다. 중앙 `095dda7`에서 새 Feature Branch를 만들고 채택이 확인된 Battlefield Map·재질만 선별 복원한 뒤 Build·Blueprint·Automation·LFS를 재검증한다.
- `git lfs push`는 대용량 Object 전송이며 Commit·Branch Push가 아니다. 일반 `git push`가 성공해야 GitHub Desktop의 Pull/Commit 이력에 새 Git Commit이 나타난다.
- 구체 명령과 두 Remote 운영 방식은 [`GIT_UNREAL_GUIDE.md`](../git/GIT_UNREAL_GUIDE.md)에 추가했다.
- 위 항목은 원격 감사 당시 판단 기록이다. 이후 팀원 변경은 중앙에 반영됐고, 현재 판정은 바로 위 `팀원 환경 변경 검증·정리와 AI-FRIEND-01` 절을 우선한다.

## 2026-08-28 — AI-PATROL-01 Hostile Smart Object 순찰

- `/Game/Drone/AI/StateTrees/ST_NPC_HostilePatrol`을 생성하고 AI Component Schema, 네 상태와 Native Task 형식을 저장 자산으로 검증했다.
- `ClaimEnemyPatrolSlot → MoveToPatrolSlot → WaitAtPatrolSlot → ReleasePatrolSlot`을 반복한다. 기본 재검색 간격은 0.5초, 이동 수용 반경은 80 cm, 대기는 1초다.
- `UDroneSmartObjectReservationComponent`에 직전 완료 지점 반경 250 cm를 우선 피하는 검색을 추가했다. 대안이 없으면 일반 검색으로 돌아가 한 지점 맵에서도 교착되지 않는다.
- Hostile Controller는 World BeginPlay 이후 Tree를 시작한다. 이 순서로 Smart Object Runtime 초기화 전 첫 조회 경고를 제거했다. Runtime Spawn은 Controller BeginPlay가 끝난 뒤 Possess되면 즉시 시작한다.
- Hostile 2명은 EnemyPatrol만 Claim하며 완료 횟수와 서로 다른 방문 위치를 기록한다. Friendly는 `AI-FRIEND-01` 전까지 Tree를 시작하지 않는다.
- 드론 감지, 이동 실패, UnPossess에서는 이동·예약을 해제한다. 현재 감지는 순찰을 안전 중단할 뿐 Search·Return·Rifle/Shotgun·MG로 전환하지 않는다.
- `Lvl_NPCSmartObjectGreybox`의 PlayerStart를 초기 Sight 반경 밖으로 옮겨 순찰 검증 시작 즉시 감지되지 않게 했다. 플레이어가 기지에 접근하면 기존 Sight 기반은 계속 동작한다.
- StateTree와 Greybox는 각각 새 Editor 프로세스 `Validate`를 통과했다. AI 자동화 6/6은 경고·오류 0이다.
- 전체 `Drone.` 자동화 22/22는 실패 0이며 기존 `PIEInputLifecycle`의 RecastNavMesh 경고 포함 성공 1개만 남는다.
- Game/Editor Build 성공, Blueprint Compile `0 errors / 0 warnings / 0 load failures`, 새 StateTree와 갱신 맵 LFS Pointer 및 `git lfs fsck`를 통과했다. 전역 Blueprint Commandlet Summary의 기존 Battlefield Pose GUID·MCP 고지 경고 29건은 Blueprint 결과 집계와 분리한다.
- 문서 저장소에 `Setup-DroneHostilePatrolStateTree.py`와 `Invoke-DroneHostilePatrolStateTreeSetup.ps1`을 추가했다. 기존 Asset을 덮어쓰지 않고 Create 또는 읽기 전용 Validate를 수행한다.
- Unreal 기능 Commit `a721fe4`를 기능 Branch에 Push하고 Merge Commit `095dda7`로 `origin/main`에 반영했다.

## 2026-08-27 — NPC·Smart Object 기반 준비

- `SmartObjects`와 `GameplayInteractions` Plugin 및 모듈 의존성을 추가했다.
- NPC 역할을 `Neutral/Friendly/Hostile`, 무기를 `Unarmed/Rifle/Shotgun`으로 구분하고 Hostile의 MG 사용 가능 여부를 Profile로 분리했다.
- EnemyPatrol, FriendlyBasePatrol, Ambient, Guard, Cover, MGTurret Activity와 DroneDetected/DroneLost Native Gameplay Tag를 추가했다.
- 프로젝트 소유 `ADroneNPCCharacter`, `ADroneNPCAIController`, `ADroneNPCSpawnPoint`, `ADroneSmartObjectStation`과 예약 Component를 추가했다.
- Hostile은 EnemyPatrol/Guard, Friendly는 FriendlyBasePatrol/Ambient만 기본 검색한다. Required Activity가 비어 있으면 검색을 거부해 잘못된 점유를 막는다.
- Drone Prototype을 Sight 감지 대상으로 등록했다. Hostile이 드론을 감지하면 순찰 Claim을 해제하고 StateTree Event를 보내며 Friendly는 전투 전환하지 않는다.
- `UsesRifle()`과 `UsesShotgun()` 분기는 준비했지만 실제 Trace·Damage·Animation·FX·SFX는 구현하지 않았다.
- Game/Editor Build와 `Drone.AI.SmartObjectFoundationDefaults` 1/1, 전체 `Drone.` 17/17을 통과했다. 전체 자동화에는 기존 PIE RecastNavMesh 경고 1개가 있으나 실패는 0이다.
- `CompileAllBlueprints`는 Blueprint errors 0, Blueprint warnings 0, failed load 0이다. 기존 Battlefield Pose GUID와 MCP EULA 고지 Summary 경고는 새 AI 코드와 무관하게 유지된다.
- `git diff --check`, `git lfs fsck`, Unreal 프로세스 종료를 확인했다.
- Definition·Blueprint·StateTree·NavMesh·Rifle/Shotgun·MG의 Editor 작성 순서를 [`DRONE_SMART_OBJECT_NPC_GUIDE.md`](../ai/DRONE_SMART_OBJECT_NPC_GUIDE.md)에 정리했다.
- 사용자 Battlefield Map Commit `4f14d2f`을 기반으로 Branch를 만들었으며 해당 Map 변경은 수정하거나 되돌리지 않았다.
- 기능 Commit `489ced5`를 `codex/smart-object-npc-foundation`에 Push하고 Merge Commit `c3e6d38`로 `origin/main`에 반영했다.

## 2026-08-27 — AI-SO-01 Definition·Station Asset 구성

- `/Game/Drone/AI/SmartObjects/Definitions`에 EnemyPatrol, FriendlyBasePatrol, Ambient, Guard, Cover, MGTurret Definition 6종을 생성했다.
- `/Game/Drone/AI/SmartObjects/Blueprints`에 대응하는 `ADroneSmartObjectStation` 자식 Blueprint 6종을 생성했다.
- 각 Definition은 Slot 1개, 정확한 Native Activity Tag와 Gameplay Interaction Behavior 1개를 가진다.
- 각 Blueprint의 Activity와 Definition을 대응시켰고 `BP_SO_MGTurret`에만 Ground Drone Kit의 `MG_Turret_SK` 후보 Mesh를 연결했다.
- Engine Smart Object Component의 Definition 설정을 자동화가 안전하게 수행하도록 `ADroneSmartObjectStation`에 프로젝트 소유 Definition·Mesh 접근 함수를 추가했다.
- `Drone.AI.SmartObjectStationAssets` 자동화를 추가해 Definition 유효성, Slot·Tag·Behavior, Blueprint 부모·Activity·Definition·MG Mesh를 재로딩 후 검사한다.
- Game/Editor Build, 전용 AI Asset 1/1, 전체 `Drone.` 18/18, Blueprint 0 errors·0 warnings·0 load failures, LFS fsck를 통과했다. 전체 자동화의 경고 포함 성공 1개는 기존 PIE RecastNavMesh 경고다.
- Interaction StateTree는 후속 `AI-PATROL-01`·`AI-FRIEND-01`에서 연결하므로 현재 의도적으로 비어 있다. 실제 순찰·아군 이동·사격을 완료로 표현하지 않는다.
- 문서 저장소의 `tools/unreal/Setup-DroneSmartObjectStations.py`와 `Invoke-DroneSmartObjectSetup.ps1`로 정확한 12개 Asset을 재구성하거나 읽기 전용 검증할 수 있게 했다.

## 2026-08-27 — AI-NPC-01 역할 Blueprint·Greybox 맵 구성

- `/Game/Drone/AI/Blueprints`에 `BP_NPC_Hostile_Rifle`, `BP_NPC_Hostile_Shotgun`, `BP_NPC_Friendly_Base`, `BP_NPCSpawnPoint`를 생성했다.
- 역할별 Profile은 Hostile/Rifle/MG 가능, Hostile/Shotgun/MG 불가, Friendly/Unarmed/MG 불가로 분리했다.
- `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`에 Rifle 1명, Shotgun 1명, Friendly 2명과 EnemyPatrol 3·Guard 1·MGTurret 1·FriendlyBasePatrol 3·Ambient 2 Station을 배치했다.
- 시각용 바닥과 별도로 `ADroneNPCNavigationFloor`를 추가해 NavMesh에 실제 충돌 지오메트리를 제공했다. Recast는 현재 MVP 검증을 위해 Dynamic·Force Rebuild On Load로 설정했으며, 넓은 맵에서는 성능 범위를 다시 결정한다.
- StateTree Asset이 비어 있을 때 자동 시작하지 않고, 실행 중인 StateTree에만 감지 Event를 보내도록 Controller의 현재 단계 오류를 막았다.
- `Drone.AI.NPCGreyboxAssets`와 `Drone.AI.NPCGreyboxPIE` 2/2에서 Profile, Controller Possess, 역할 Tag, NPC·Station 수, Navigation Floor, Dynamic Recast, NPC 시작점 NavMesh 투영을 검증했다.
- Game/Editor Build, 전체 `Drone.` 20/20을 통과했다. 19개 정상 성공, 기존 PIE RecastNavMesh 경고 포함 성공 1개, 실패 0개다.
- Blueprint 전체 Compile은 errors 0·warnings 0·failed load 0이며, 새 패키지 5개는 LFS Pointer와 `git lfs fsck`를 통과했다.
- Manny Simple·`ABP_Unarmed`은 임시 Greybox다. 최종 Soldier/Insurgent 외형, 실제 StateTree·순찰·아군 이동·Rifle/Shotgun 사격은 아직 미구현이다.
- 기능 Commit `362edaa`를 `codex/npc-greybox-setup`에 Push하고 Merge Commit `eeb4354`로 `origin/main`에 반영했다.
- 문서 저장소의 `tools/unreal/Setup-DroneNPCGreybox.py`와 `Invoke-DroneNPCGreyboxSetup.ps1`로 자산 생성·유지보수와 읽기 전용 검증을 반복할 수 있게 했다.

## 2026-08-27 — 남은 에셋 선별 이식·OilRig·TUT-04B

- `ArmyVFX`, `InfantrySFX`, `GC_DroneS`, `Modular Soldier`, `Modular Insurgents`, Non-Pilot Quad v4, PBR Sting과 OilRig을 별도 UE 5.8 스테이징에서 검사했다.
- 실제 프로젝트에는 ThirdParty 891개와 중앙 `Lvl_OilRig` 1개만 이식했다.
- Ground Drone의 구형 PhysX 차량 Blueprint는 제외했고, Soldier/Insurgent는 외형 후보로만 이식했다.
- OilRig에서 FirstPerson 샘플 의존성을 끌어오던 `BP_Simple_Door` Actor 8개를 중앙 사본에서 제거했다.
- 새 7개 Root 수량 일치, 대표 로드 성공, 외부·누락 `/Game` 참조 0, OilRig `default_game_mode=None`을 확인했다.
- OilRig 별도 Map Check는 약 8분간 맵 Construction이 끝나지 않아 저장 없이 프로세스만 중단했다. Editor 시각·성능·Map Check는 미확인이다.
- `FDroneTrainingLapComparison`, Segment 비교, 이전 평균·Best·Delta와 `OnLapComparisonReady`를 추가했다.
- HUD에 이전 완주 평균, Best, 시간·속도 Delta 네 행을 추가했다.
- Build 성공, Blueprint 오류 0, 전체 `Drone.` 16/16 성공했다.
- 기능 Commit `3fa4444`을 `codex/remaining-asset-migration`에 Push하고 Merge Commit `55b3ffe`로 `origin/main`에 반영했다.
- 신규 Unreal 패키지 892개는 모두 LFS Pointer로 커밋됐고 4.9GB 업로드 및 `git lfs fsck`를 통과했다.
- 상세 범위와 수동 확인은 [`DRONE_REMAINING_ASSET_MIGRATION_2026-08-27.md`](../assets/DRONE_REMAINING_ASSET_MIGRATION_2026-08-27.md)를 따른다.

## 2026-08-21 — Camera·Mouse·Gamepad 기준선 갱신

### 실제 변경

- SpringArm을 Controller 자유 회전에서 Drone Yaw를 따르는 고정 추적 Camera로 변경
- Mouse X를 Drone Actor Yaw, Mouse Y를 CameraBoom Pitch로 분리
- Gamepad Left Stick 이동, `RT/LT` 고도, Right Stick X Yaw, Right Stick Y Camera Pitch 추가
- Input Action을 5개, IMC Mapping을 15개로 확장
- PIE lifecycle 테스트를 Keyboard·Mouse·Gamepad와 복합·반대 입력까지 확장
- Tutorial·Story 공통 구조와 실행 순서를 `DRONE_TUTORIAL_STORY_PLAN.md`로 확정

### 검증 결과

- `DroneEditor Win64 Development` 빌드 성공
- Blueprint 전체 Compile: 0 errors, 0 warnings
- `PawnDefaults`, `PIEInputLifecycle`, `SpawnPossess`: 3 succeeded, 0 failed
- 새 PIE 3회에서 입력과 IMC 중복 없음 확인
- Prototype 자산 9개, Input Action 5개, Mapping 15개 확인
- `/Game/Drone`에서 동결한 Legacy 자산으로 향하는 의존성 0개
- 기존 ThirdPerson 기본 Map 로드 유지
- 두 저장소 `git diff --check` 통과

### 남은 작업

- 사용자 수동 확인으로 Camera·Keyboard·Mouse 조작 수정이 정상임을 확인함
- 실제 Gamepad가 연결되어 있으면 Stick·Trigger 체감 확인하고, 없으면 `미확인`으로 기록
- 창 닫기 뒤 `Win RequestExit`, `Game engine shut down`, `Exiting` 로그와 프로세스 종료를 확인함
- PFN-06을 Done으로 판정

### 다음 구현

PFN-06 통과 후 `HUD-01`을 시작한다. Drone Telemetry를 10Hz Snapshot으로 제공하고 속도·고도·수직 속도·Heading을 공용 HUD에 표시한다.

### 수동 판정 마감

- 사용자 보고: 조작 수정 정상
- 종료 방식: `Esc`가 아닌 창 닫기
- 로그 판정: 정상 종료, Fatal·Assertion 없음
- Gamepad 체감: 연결 여부 미보고로 미확인
- 최종 판정: PFN-06 Done, `HUD-01` Ready
- Unreal 로컬 Commit: `2c38ebf` (`feat: finalize prototype camera and input lifecycle`)
- 원격 Push: 수행하지 않음

## 2026-08-21 — HUD-01 시작

### 현재 설계

- 공용 Snapshot은 속도 km/h, 기준면 대비 고도 m, 수직 속도 m/s, Heading 0~359°를 가진다.
- `UDroneTelemetryComponent`가 0.1초 간격으로 값을 갱신하고 Blueprint가 구독할 수 있는 Event를 보낸다.
- Component는 Prototype Pawn에 기본 부착하되 `/Source/Drone/Telemetry`의 재사용 가능한 생산 코드로 만든다.
- 고도는 매번 지형을 Trace하지 않고 Course/Mission이 지정하는 기준 World Z 대비로 계산한다. Tutorial 코스가 만들어지면 시작 Pad 또는 Course 기준면을 전달한다.
- Widget은 값을 계산하거나 매 프레임 Pawn을 검색하지 않는다. `HUD-02`에서 Snapshot Event를 구독한다.

### 이번 완료 조건

- Telemetry 계산과 10Hz 기본값 자동화 통과
- Prototype Pawn이 Component를 한 개 소유
- `DroneEditor Win64 Development` 빌드 성공
- 기존 Prototype 자동화 회귀 통과
- 검증 뒤 `HUD-01` Done, `HUD-02` Ready로 문서 갱신

### 구현 결과

- `FDroneTelemetrySnapshot`에 Speed km/h, Altitude m, Vertical Speed m/s, Heading degree를 정의했다.
- `UDroneTelemetryComponent`가 BeginPlay 즉시 한 번, 이후 0.1초 Timer로 Snapshot을 갱신한다.
- `OnTelemetryUpdated` Blueprint Event와 최신 Snapshot Getter를 제공한다.
- Course/Mission 기준 World Z를 런타임에 설정하면 즉시 Snapshot을 다시 계산한다.
- Prototype Pawn이 Component 한 개를 native 기본 Subobject로 소유한다.

### 검증 결과

- 최종 `DroneEditor Win64 Development` 빌드 성공
- `Drone.Telemetry.Calculation`, `Drone.Telemetry.Defaults` 통과
- `PawnDefaults`, `PIEInputLifecycle`, `SpawnPossess` 회귀 포함 최종 Report 5 succeeded, 0 warnings, 0 failed
- Runtime Spawn Pawn의 Component 존재, Spawn 고도와 Reference Z 변경 즉시 갱신 확인
- Blueprint 전체 Compile 0 errors, 0 warnings, failed load 0
- 첫 빌드 시 따옴표 없는 CompilerVersion을 PowerShell이 분리한 명령 오류가 있었고, 문자열 인자로 고정한 뒤 성공했다. 코드 컴파일 실패로 분류하지 않는다.

### 판정

- `HUD-01` Done
- `HUD-02` Ready
- 상세 구현: [`DRONE_TELEMETRY_IMPLEMENTATION.md`](../tutorial/DRONE_TELEMETRY_IMPLEMENTATION.md)
- Unreal 로컬 Commit: `08e876a` (`feat: add drone telemetry snapshot component`)
- 원격 Push: 수행하지 않음

## 2026-08-23 — HUD-02 구현·검증 완료

### 실제 변경

- `Source/Drone/UI/DroneFlightHUDWidget.*`에 C++ native UMG Flight HUD를 추가했다.
- `Source/Drone/Prototype/DronePrototypePlayerController.*`가 로컬 Player 화면에 HUD 하나를 만들고 PlayerController 수명 동안 재사용한다.
- Prototype GameMode가 전용 PlayerController를 사용하도록 연결했다.
- Widget은 현재 Possess Pawn의 `UDroneTelemetryComponent`를 찾아 `OnTelemetryUpdated`를 `AddUniqueDynamic`으로 구독하고, 연결 직후 최신 Snapshot을 한 번 적용한다.
- Pawn 전환 시 이전 Component Event를 해제하고 새 Source로 교체한다. UnPossess, Widget 종료와 Controller 종료에서도 해제를 멱등적으로 수행한다.
- Tick, UMG Property Binding, 매 프레임 Pawn 검색과 Widget 내부 단위 재계산은 사용하지 않는다.
- 현재 Prototype 표시는 `SPD %.1f km/h`, `ALT %.1f m`, `V/S %+.1f m/s`, `HDG %03d°` 형식이다. 배치·폰트·색상·Animation은 최종 디자인 확정이 아니라 교체 가능한 초기값이다.
- 현재 PC의 실제 저장소 경로는 `C:\URproject\drone`이며, 뒤처진 `C:\project\Drone` 복제본은 수정하지 않았다.

### 자동화와 수명주기 검증

- `Drone.UI.FlightHUDTelemetryBinding`이 동일 Source 중복 연결 방지, 이전 Source 해제, 새 Source 연결, 네 Text 포맷과 Clear를 확인한다.
- 기존 `PIEInputLifecycle`을 확장해 새 PIE 3회마다 Prototype PlayerController와 HUD가 정확히 하나인지, Viewport와 현재 Telemetry Source가 연결됐는지 확인한다.
- 각 PIE에서 `UnPossess → HUD Collapsed·Event 해제 → 같은 Widget 재사용 Re-Possess·Event 재연결`을 실행하고, 종료 뒤 Viewport·Telemetry·Possession Delegate 잔존이 없는지 확인한다.
- Keyboard·Mouse·Gamepad, 복합·반대 입력과 입력 세기 회귀도 같은 테스트에서 계속 통과했다.

### 최종 검증 결과

- `DroneEditor Win64 Development` 빌드 성공
- 최종 `Drone.` Automation: 6 succeeded, 0 warnings, 0 failed
- `CompileAllBlueprints`: 0 errors, 0 warnings, 0 blueprints failed to load
- 새 `.uasset`/`.umap`을 만들지 않아 `/Game/Drone`의 Legacy Variant 신규 의존성 0
- Standalone 초기 화면: `SPD 0.0 km/h`, `ALT 1.5 m`, `V/S +0.0 m/s`
- Standalone 이동: `SPD 43.2 km/h`
- Standalone 상승: `ALT 2.7 m`, `V/S +10.0 m/s`
- Standalone 하강: `V/S -7.2 m/s`
- Standalone Yaw: Heading `002° → 025°/045°`
- 단일 자동 입력을 10Hz 화면에 확실히 포착하기 위해 실행 중에만 Movement 가속·감속을 임시 조정했으며 프로젝트 기본값과 소스는 변경하지 않았다.

### 발견·수정한 문제

- 첫 테스트 빌드에서 Dynamic Multicast 검사 API 선택과 C++ 멤버 이름 가림 오류를 발견해 `Contains` 검사와 명확한 변수명으로 수정했다.
- `AddToPlayerScreen` 실패가 조용히 넘어가지 않도록 반환값 검사와 오류 로그를 추가했다.
- 기본 UMG 글자 크기가 작은 문제를 초기 Prototype 읽기 크기로 조정했다. 이는 최종 HUD 디자인 확정이 아니다.

### 판정과 Git

- `HUD-02` Done
- `TUT-01` Ready
- Unreal Commit: `410c940` (`feat: add event-driven drone flight HUD`)
- `codex/hud-02-flight-hud`와 `origin/main`에 Push 완료, 로컬 `main=origin/main=410c940`

## 2026-08-23 — HUD-02 WBP/BP 연결과 학습 주석 보강

### 실제 변경

- native `UDroneFlightHUDWidget` 자식인 `WBP_DroneFlightHUD`를 생성해 Designer에서 패널 배치·색·폰트를 편집할 수 있게 했다.
- `BP_DronePrototypePlayerController`를 만들고 `FlightHUDWidgetClass`에 `WBP_DroneFlightHUD`를 지정했다.
- `BP_DronePrototypeGameMode`의 PlayerController Class를 새 BP Controller로 연결했다.
- WBP Designer에는 C++ `BindWidget` 계약과 정확히 같은 이름의 TextBlock 4개를 둔다.

```text
SpeedValueText
AltitudeValueText
VerticalSpeedValueText
HeadingValueText
```

- C++는 Telemetry 계산, Widget 생성, Possession 동기화, Delegate 해제와 표시 문자열 포맷을 계속 담당한다. WBP는 위치·크기·색·폰트 같은 표시 외형만 담당하며 Event Graph Tick과 Property Binding은 사용하지 않는다.
- Designer Tree가 없는 native HUD Class를 직접 실행할 때의 C++ 기본 레이아웃은 유지했다. 정상 컴파일된 WBP는 필수 TextBlock 4개를 사용하며 런타임 누락 경로는 방어 코드다.
- Pawn, GameMode, PlayerController와 HUD 기반 Class를 Blueprintable로 명시하고 Blueprint에서 확인할 Getter를 정리했다.
- 입력·이동·Telemetry 단위·Widget/Controller 수명주기·C++↔WBP 이름 계약·테스트 목적을 설명하는 한국어 주석을 보강했다. 이 주석 작업은 최종 비행 물리·감도·게임 규칙을 새로 확정한 것이 아니다.

### 발견·수정한 문제

- 첫 Standalone 화면에서 WBP TextBlock의 FontObject가 비어 있어 글자가 대체 글리프로 깨졌다.
- Engine `Roboto` Font를 WBP Asset에 직렬화해 저장했고, 필수 TextBlock과 Header Font 유효성을 자동화에서 검사하도록 했다.
- “BP Asset이 사라지면 native로 자동 복구”, “항상 10Hz”, “Heading 000°는 진북”처럼 구현보다 강하게 읽히는 주석을 실제 동작에 맞게 교정했다.

### 최종 검증

- `DroneEditor Win64 Development` 빌드 성공
- `Drone.` Automation: 7 succeeded, 0 warnings, 0 failed
- 새 `Drone.UI.FlightHUDBlueprintAsset`이 WBP 부모, 필수 TextBlock 4개·Font, BP Controller→WBP, BP GameMode→BP Controller를 확인
- `PIEInputLifecycle` 새 PIE 3회에서 실제 BP Controller와 WBP Class 사용, native fallback 미사용, Widget 재사용·Delegate 정리 확인
- `CompileAllBlueprints`: 0 errors, 0 warnings, 0 blueprints failed to load
- Standalone에서 실제 WBP의 `FLIGHT DATA`, `SPD`, `ALT`, `V/S`, `HDG` 글자가 깨짐 없이 표시됨
- WBP·BP Controller 신규 Asset과 갱신 BP GameMode 모두 Git LFS 적용 확인

### 판정과 Git

- `HUD-02` Blueprint presentation follow-up 완료
- 최종 아트·Animation, 배터리·신호·Jamming 표시는 아직 미정/미구현
- `TUT-01` Ready
- Unreal Commit: `9f91bb6` (`feat: add Blueprint-backed flight HUD`)
- `codex/hud-blueprint-ready-comments`와 `origin/main`에 Push 완료, 로컬 `main=origin/main=9f91bb6`

## 2026-08-23 — TUT-01 Training Map과 비충돌 Spline 착수

### 확정 범위

- 별도 Training Map을 만든다. 당시 경로는 `/Game/Drone/Tutorial/Maps/Lvl_DroneTraining`이며 현재는 `/Game/Drone/Maps/Lvl_DroneTraining`으로 중앙화했다.
- `ADroneTrainingCourse`가 편집 가능한 `USplineComponent`와 Standalone에서도 보이는 표시용 구성요소를 소유한다.
- 표시용 Actor·Spline·Mesh의 Collision, Overlap, Physics, Navigation 영향을 모두 끈다.
- 기존 `BP_DronePrototypeGameMode`를 재사용해 Prototype Pawn/Input/HUD 기준선을 유지한다.
- Gate Trigger, 순서·방향 판정, Lap/Segment 기록은 다음 `TUT-02` 이후 범위로 남긴다.

### 검증 예정

- native Course 기본값과 Pawn 크기 Sweep 비간섭 자동화
- 실제 BP Course와 Training Map 계약 자동화
- Training Map PIE에서 BP Pawn·Controller·WBP와 표시선 생성 확인
- Editor Build, 전체 Blueprint Compile, 전체 `Drone.` 회귀, Standalone 시각·비행 확인

### 현재 판정

- `TUT-01` Doing
- Unreal 작업 Branch: `codex/tutorial-training-course`
- Unreal Commit: 아직 미커밋

## 2026-08-23 — TUT-01 Training Course 구현·검증 완료

### 실제 변경

- `ADroneTrainingCourse`에 편집 가능한 `USplineComponent`와 런타임 표시용 `USplineMeshComponent` 구성을 구현했다.
- 실제 `BP_DroneTrainingCourse`와 별도 `Lvl_DroneTraining` Map을 만들고 기존 `BP_DronePrototypeGameMode`를 재사용했다.
- `M_DroneTrainingGuide`를 Opaque·Unlit·Emissive·Spline Mesh 용도로 만들고 Standalone에서 식별 가능한 밝은 Cyan 표시선을 구성했다.
- Course Actor와 Spline 표시 구성요소의 Collision, Overlap, Physics, Navigation 영향을 모두 껐다.
- native Course 기본 계약, 실제 BP/Map Asset 계약, Training Map PIE 수명주기와 비간섭을 검사하는 Tutorial 자동화 테스트 3개를 추가했다.
- 학습할 때 구현 의도와 C++·Blueprint 역할을 따라갈 수 있도록 Course와 테스트 코드에 한국어 주석을 추가했다.

### 최종 검증 결과

- `DroneEditor Win64 Development` 빌드 성공
- `Drone.Tutorial` Automation: 3 succeeded, 0 warnings, 0 failed
- 전체 `Drone.` Automation: 10 succeeded, 0 warnings, 0 failed
- `CompileAllBlueprints`: 0 errors, 0 warnings, 0 blueprints failed to load
- Standalone에서 실제 BP Pawn·Controller·WBP HUD와 밝은 Cyan Course Spline 표시 확인
- Spline Mesh Material Usage 경고 없음
- 실제 Pawn Sweep이 표시선을 통과하고 목표 위치에 도달해 Blocking 없음 확인
- Course 소유 표시 구성요소의 Collision·Overlap·Physics·Navigation 관련 Flag가 모두 꺼져 있음 확인
- Training Map에 저장된 Recast Actor 확인

### 범위 정지선

- TUT-01은 Training Map, 편집 가능한 Course Spline과 비간섭 표시선까지만 완료했다.
- Gate, Trigger, 순서, 방향, Lap, Timing은 구현하지 않았으며 `TUT-02` 이후 범위다.
- Android는 사용자 결정에 따라 작업 범위에서 제외한다.
- Map과 다음 카드 담당자는 현재 미정이다.

### 판정과 Git

- `TUT-01` Done
- `TUT-02` Todo
- Unreal Commit: `5a9a2faed4591a574988b649278cb0f166e31267` (`feat: add tutorial training course`)
- `codex/tutorial-training-course`와 `origin/main`에 Push 완료, 로컬 `main=origin/main=5a9a2faed4591a574988b649278cb0f166e31267`

## 2026-08-24 — TUT-02 Ordered Ring Gate 구현·검증 완료

### 실제 변경

- `ADroneTrainingGate`에 Engine Cube 16조각으로 만든 비충돌 Ring Visual과 별도 `UBoxComponent` Pawn Overlap Trigger를 구현했다.
- `UDroneTrainingGateSequenceComponent`가 Course의 명시적 `OrderedGates` 배열을 단일 순서 기준으로 사용하도록 구성했다.
- 현재 Gate의 정방향 통과만 한 번 승인하고 잘못된 Actor, 미래 Gate, 역방향, 중복 통과와 잘못된 구성을 거부하도록 구현했다.
- Gate 외형은 `Current`, `Completed`, `Inactive` 상태로 분리하고, 정상 승인 시 다음 Gate로 정확히 한 칸 진행한다.
- 실제 `BP_DroneTrainingGate`를 추가하고 `Lvl_DroneTraining`에 네 Gate를 배치해 Course 배열과 연결했다.
- `SegmentDistance`는 후속 기록용 메타데이터로만 저장한다. TUT-02 판정에서 Lap·Timing·거리·평균 속도 계산에는 사용하지 않는다.
- 정상 Gate 승인 Event를 제공하되 기록 계층은 TUT-03에서 별도로 구독하도록 경계를 유지했다.

### 최종 검증 결과

- `DroneEditor Win64 Development` 빌드 성공
- `Drone.Tutorial.TrainingGateSequence`: 1 succeeded, 0 warnings, 0 failed
- 실제 BP Gate Begin/End Overlap을 포함한 `Drone.Tutorial.TrainingPIESmoke`: 1 succeeded, 0 warnings, 0 failed
- 전체 `Drone.Tutorial`: 4 succeeded, 0 warnings, 0 failed
- 전체 `Drone.`: 11 succeeded, 0 warnings, 0 failed
- `CompileAllBlueprints`: 0 errors, 0 warnings, 0 blueprints failed to load
- Standalone에서 실제 WBP HUD, Cyan Course 안내선과 Current/Inactive Gate 표시 확인
- 신규 `BP_DroneTrainingGate`와 갱신한 `Lvl_DroneTraining` 두 Asset의 Git LFS 적용과 Push 확인

### 범위 정지선

- Gate Visual·Trigger, 명시적 순서, 정방향·중복 통과 판정과 시각 상태까지 TUT-02로 완료했다.
- Lap 시작·완료, Segment/Lap Timing, 실제 이동 거리·평균 속도, 이전 기록 비교와 결과 UI는 구현하지 않았다.
- 다음 활성 카드는 `TUT-03 Segment/Lap 기록`이다.
- Android와 구매 에셋은 현재 범위에서 제외한다.

### 판정과 Git

- `TUT-02` Done
- `TUT-03` Todo
- Unreal Commit: `800a7baaf8247bf0a3ee7bccc2272e12d0098f2b` (`feat: add ordered tutorial ring gates`)
- `codex/tutorial-ring-gates`와 `origin/main`에 Push 완료, 로컬 `main=origin/main=800a7baaf8247bf0a3ee7bccc2272e12d0098f2b`

## 2026-08-25 — 제공 에셋 14팩 인수 감사와 이식 계획

### 실제 확인

- 사용자 입력 경로 `D:\JGY\project\Unreal\_260821`은 존재하지 않고 실제 폴더는 `D:\JGY\project\Unreal_260821`임을 확인했다.
- 최상위 ZIP 14개와 같은 이름의 해제 폴더 14개를 파일별 상대 경로와 크기로 대조했다.
- 모든 팩이 `Missing 0 / Extra 0 / SizeMismatch 0`으로 일치했다.
- 해제 결과는 10,499개 파일과 35,677,612,290 bytes이며 `.uasset` 10,445개, `.umap` 25개다.
- 외부 ZIP은 모두 해제됐지만 `Non-Pilot Drones KITBASH SET\FBX.zip` 안의 개별 FBX 55개는 내부 압축 상태로 남아 있다.
- Drone 저장소는 `main=origin/main=800a7ba`, 작업 트리 Clean이며 외부 에셋을 아직 추가하지 않았다.
- Drone Content는 768개·141,255,461 bytes이고 D Drive 여유 공간은 약 944 GB라 스테이징 여유는 충분하지만, 제공 에셋 전체를 LFS에 넣지 않기로 했다.

### 호환성 판정

- 확인된 제작 버전 단서는 UE 4.23~5.6이며 현재 프로젝트 UE 5.8에서 상향 변환·재저장이 필요하다.
- `DronePack_Project`는 UE 5.1 완전 프로젝트이고 내부 루트는 `/Game/Drone_Pack`이다.
- `GC_DroneS`는 UE 4.24와 `PhysXVehicles` 의존성이 있어 기능 Blueprint를 재사용하지 않고 Mesh·Material·Turret Part만 후보로 둔다.
- `OilRigLiope_Tr` 해제 폴더의 실제 패키지 루트는 `/Game/Liope_Tr`이다.
- 일부 팩에서 제공 폴더 밖 `/Game` 참조 단서를 발견해 스테이징 Asset Audit 전 Demo 자산의 직접 이식을 금지했다.

### 이식 결정

- 원본 ZIP·해제본은 보존하고 UE 5.8 스테이징 복사본에서 팩 하나씩 검증한다.
- 필요한 의존성만 Content Browser에서 `/Game/Drone/ThirdParty/<Pack>`으로 이동·재저장한 뒤 실제 프로젝트로 Migrate한다.
- 프로젝트 연결은 `/Game/Drone/Integrations/<Pack>`에서 만들고 현재 C++ Collision Root·Movement·Camera·Telemetry를 유지한다.
- 외부 Pawn, GameMode, PlayerController, Input Mapping과 Demo Level Blueprint는 사용하지 않는다.
- 첫 최소 Spike는 `DronePack_Project`의 FPV Body·Rotor·Material과 `Drone-Sounds` 44.1 kHz Loop Cue 하나다.

### 판정과 다음 작업

- `AST-00` 제공 에셋 인수 감사 Done
- 실제 에셋 이식 0건
- 내부 `FBX.zip` 별도 해제 필요
- 기능 실행 순서는 유지하며 다음 활성 카드는 `TUT-03 Segment/Lap 기록`
- 상세 결과: [`DRONE_ASSET_INTAKE_2026-08-25.md`](../assets/DRONE_ASSET_INTAKE_2026-08-25.md)

## 2026-08-25 — AST-01 FPV 최소 외형·Loop 선별 이식

### 실제 변경

- `D:\JGY\project\Unreal_260821\_Staging\DroneAssetStage` UE 5.8 스테이징 프로젝트를 만들고 DronePack FPV와 Drone-Sounds만 복사했다.
- 공급사 Blueprint 전체 Compile 결과는 `0 errors / 27 warnings / 0 load failures`였다. 경고가 구형 Input Axis와 누락 Mannequin Rig 참조에 집중되어 외부 기능 Blueprint 재사용 금지 판정을 확정했다.
- FPV Body·Rotor A~D·Material·Texture 4개와 44.1 kHz Cue/Wave, 총 12개·21,753,071 bytes만 `/Game/Drone/ThirdParty`로 이동·UE 5.8 재저장해 실제 프로젝트에 이식했다.
- `/Game/Drone/Integrations/DronePackFPV/BP_DroneFPVIntegration`을 만들었다. 기존 `ADronePrototypePawn`의 Collision Root·Movement·Camera·Input·Telemetry를 유지하고 본체 1, Rotor 4, Audio 1만 추가했다.
- 모든 FPV Visual은 Collision·Overlap·Physics·Navigation 영향을 끄고 기존 Sphere Collision Root와 분리했다.
- `BP_DronePrototypeGameMode`가 FPV Integration Pawn과 기존 `BP_DronePrototypePlayerController`를 명시적으로 사용하도록 연결했다.
- 기존 Prototype/Training PIE 테스트가 실제 FPV Integration Pawn Class를 기대하도록 갱신하고 `Drone.Integration.FPVAsset` 계약 테스트를 추가했다.

### 검증 중 발견·수정

- 첫 자동화에서 GameMode의 PlayerController 기본값이 비어 PIE 시작이 실패하는 문제를 발견했다. 이식 스크립트가 Pawn과 BP PlayerController를 함께 고정하도록 수정했다.
- 첫 자산 테스트는 Blueprint SCS Component를 CDO에서 찾으려 해 본체만 보였다. transient World에 실제 Pawn을 Spawn해 런타임 Component를 검사하도록 수정했다.
- 이식 스크립트 재실행 시 Template Object 이름과 SCS 변수명이 달라 Rotor·Audio가 중복되는 문제를 발견했다. 이름이 아니라 Mesh/Sound Asset 참조 기준으로 중복 제거하고 재실행 안전성을 확보했다.
- Editor가 Camera 표시용으로 생성하는 `UCameraProxyMeshComponent`를 Drone 외형으로 잘못 센 테스트를 수정했다. 실제 SCS는 본체 1·Rotor 4·Audio 1이다.
- 제공 Cue는 이름에 `Loop`가 있지만 실제 `IsLooping()`은 false였다. 프로젝트 이식본 SoundNode Wave Player의 Looping을 켜고 계약 테스트에 `SoundBase::IsLooping()` 검사를 추가했다.

### 최종 검증

- `DroneEditor Win64 Development`: MSVC 14.51.36256 명시 Build 성공
- 전체 Blueprint Compile: `0 errors / 0 warnings / 0 load failures`
- Map Check: `0 errors / 0 warnings`
- 선택 자산 12개: 외부 `/Game` 의존성 0, Integration의 ThirdPerson·Variant·원본 Vendor Root 의존성 0
- Loop 설정 수정 뒤 최종 전체 `Drone.` Automation: `12 succeeded / 0 failed / 0 warnings`
- `PIEInputLifecycle`: 새 PIE 3회 모두 FPV Pawn·IMC·Keyboard/Mouse/Gamepad·복합/반대 입력 회귀 통과
- Standalone Training Map: FPV 외형·고정 추적 Camera·기존 HUD/Course/Gate 초기 화면 캡처와 정상 종료 확인
- 첫 실제 렌더에서 4K Texture DDC를 생성하느라 종료 후 약 76초를 더 기다렸지만 `Game engine shut down`과 `Exiting`까지 정상 완료

### 현재 판정과 다음 작업

- `AST-01`은 코드·자산·자동 회귀·초기 화면까지 통과했다.
- 실제 스피커에서 Drone Loop 단일 재생과 종료 시 정지를 듣는 수동 확인만 남아 Doing으로 유지한다.
- 사용자 청감 확인이 통과하면 `AST-01`을 Done으로 이동하고 `TUT-03 Segment/Lap 기록`으로 복귀한다.
- Unreal과 문서 저장소 변경은 로컬 미커밋이며 Push하지 않았다.

## 2026-08-25 — UE-MCP-01 공식 Unreal MCP·Codex 연결

### 확인과 방향 전환

- 사용자가 전달한 Unreal Engine KR YouTube Community 게시물을 확인했다.
- 게시물은 UEFN MCP 공개 소식이지만, 연결된 Epic 기사에서 UE 5.8 일반 Unreal Editor에도 `ModelContextProtocol`이 포함됐음을 확인했다.
- UE 5.8 공식 문서에서 Unreal MCP가 Editor 프로세스 내부 HTTP 서버, Toolset Registry, Codex 프로젝트 설정 생성을 공식 지원함을 확인했다.
- 처음 추가했던 파일 기반 `DroneEditorBridge` 초안은 공식 기능과 중복되어 빌드 전에 전부 제거했다.

### 실제 구성

- `Drone.uproject`에 `ModelContextProtocol`을 Editor Target으로 활성화했다.
- Drone 작업에 필요한 `EditorToolset`, `AutomationTestToolset`, `UMGToolSet`, `StateTreeToolset`, `AIModuleToolset`만 선택했다.
- PCG·Niagara·GAS·Dataflow 등 현재 불필요한 플러그인을 함께 활성화하는 `AllToolsets`는 제외했다.
- `DefaultEditorPerProjectUserSettings.ini`에 `bAutoStartServer=True`, Port 8000, Path `/mcp`, Tool Search 활성 기본값을 추가했다.
- `.codex/config.toml`에 `unreal-mcp` 프로젝트 연결과 `default_tools_approval_mode="writes"`를 기록했다.
- 서버는 인증 없는 Experimental 기능이므로 `127.0.0.1` loopback 외부로 공개하지 않는다.

### 빌드에서 발견한 기존 경계 오류

- `DroneEditor Win64 Development`는 즉시 성공했다.
- 최초 `Drone Win64 Development`는 `DroneTrainingCourseTest`와 `DroneTrainingGateSequenceTest`의 `RerunConstructionScripts()`가 게임 Development에도 컴파일되어 실패했다.
- 두 테스트의 가드를 `WITH_DEV_AUTOMATION_TESTS`에서 `WITH_EDITOR && WITH_DEV_AUTOMATION_TESTS`로 좁혔다.
- 생산 Runtime API 변경 없이 재빌드한 `Drone Win64 Development`가 성공했다.

### 최종 회귀와 MCP 왕복 검증

- 전체 `Drone.` 자동화는 12/12 Success, Exit Code 0이다.
- 실제 Unreal Editor를 Training Map으로 열고 PID가 `127.0.0.1:8000`을 Listen함을 확인했다.
- MCP `initialize` HTTP 200과 Session ID, `notifications/initialized` 202, `tools/list` 200을 확인했다.
- Tool Search 메타 툴 `list_toolsets`, `describe_toolset`, `call_tool`이 반환됐다.
- 선택 Plugin 구성에서 총 23개 Toolset이 검색됐다.
- 실제 MCP 호출로 당시 Current Level `/Game/Drone/Tutorial/Maps/Lvl_DroneTraining`, PIE false, Selected Actors 0, Content Browser `/Game/Drone/Prototype/Maps`를 조회했다. 현재 Map 경로는 `/Game/Drone/Maps/Lvl_DroneTraining`이다.
- `AutomationTestToolset.DiscoverTests`는 `ready`, `ListTests`의 `Drone.` 필터는 12개를 반환했다.
- Codex 앱 번들 CLI는 WindowsApps 권한 거부로 PowerShell의 `codex mcp list`를 실행하지 못했다. 이는 Unreal MCP 서버나 프로젝트 TOML 오류가 아니라 현재 앱 패키지 실행 경계다.

### 판정과 다음 작업

- `UE-MCP-01` Done
- `UE-MCP-02` Todo — Drone 루트에서 새 Codex 작업을 열었을 때 네이티브 Tool 노출과 Current Level 호출을 한 번 확인
- Unreal Editor와 MCP 서버는 실행 상태로 유지한다.
- 현재 대화는 Drone 루트에서 시작한 Codex 작업이 아니므로 새 `.codex/config.toml`이 Tool 목록에 즉시 재주입되지 않는다. 후속 작업은 Editor를 먼저 열고 `D:\JGY\project\drone` 루트에서 Codex 작업을 열어 공식 MCP를 직접 사용한다.
- `AST-01` 실제 Loop 청감 확인은 여전히 남아 있으며, 통과 후 `TUT-03 Segment/Lap 기록`으로 복귀한다.
- 상세 사용법: [`DRONE_UNREAL_MCP.md`](../git/DRONE_UNREAL_MCP.md)

## 2026-08-25 — AST-01 수동 미확인 기준선과 Git 담당 확정

### 현재 판정

- FPV·Sound 선택 자산 12개와 프로젝트 소유 Integration BP 1개는 실제 Drone 프로젝트에 들어 있다.
- 전체 제공 에셋 14팩 35.7 GB는 의도적으로 프로젝트에 복사하지 않고 `D:\JGY\project\Unreal_260821`에 원본으로 보존한다.
- Build, Blueprint Compile, Map Check, 전체 `Drone.` Automation 12/12와 Standalone 초기 렌더·정상 종료는 통과 상태를 유지한다.
- 실제 스피커에서 Drone Loop가 한 번만 재생되는지와 Standalone 종료 후 멈추는지는 아직 수동 확인하지 않았다.
- 청감 결과는 실패가 아니라 `미확인`이며, 확인 전에는 성공으로 추정하거나 `AST-01`을 Done 처리하지 않는다.

### 다음 작업과 Git

- `AST-01`은 Doing으로 유지하고 수동 청감 결과가 생길 때 판정만 갱신한다.
- 다음 기능 카드는 `TUT-03 Segment/Lap 기록`이다.
- 현재 Drone·문서 작업 트리의 Stage·Commit·Push는 사용자가 직접 수행한다. 이번 문서 최신화에서는 Git 변경을 전송하지 않는다.

## 2026-08-25 — TUT-03 Segment/Lap 원본 기록

### 실제 구현

- `FDroneTrainingSegmentRecord`와 `FDroneTrainingLapRecord`에 Gate 구간, World Game Time 기준 경과 시간, 실제 이동 거리와 평균 속도 원본 값을 정의했다.
- `UDroneTrainingLapRecorderComponent`를 `ADroneTrainingCourse`가 소유하도록 추가하고 실제 Play 수명주기에서 Gate Sequence에 연결했다.
- Gate 0의 정상 승인을 Lap 시작선으로 사용한다. Gate가 N개면 Gate 0 이후 정상 Gate마다 Segment를 하나 완성하므로 성공 Lap은 N-1개 Segment를 가진다.
- 기록기는 기존 `UDroneTelemetryComponent`의 기본 10 Hz Snapshot Event에서 같은 Drone의 3차원 World 위치를 표본화한다. 별도 Actor Tick이나 Timer는 추가하지 않았다.
- Segment와 Lap 평균 속도는 `실제 이동 거리 / World Game Time`으로 계산하고 Unreal cm를 m와 km/h로 변환한다.
- Gate Sequence의 정상 승인 Event에 실제 통과 Actor와 승인 위치를 추가하고, Restart·재구성 시 부분 기록을 폐기할 수 있도록 Reset Event를 추가했다.

### 확정한 기록 경계

- Gate 0 이전 이동은 기록하지 않고 Gate 0 승인 위치부터 거리를 누적한다.
- `SegmentDistance`는 계속 후속 도구용 메타데이터이며 기록 거리 계산에 사용하지 않는다. 실제 경로는 Telemetry 위치 표본 사이의 3차원 거리 합으로 계산한다.
- 현재 Lap은 Gate 0을 통과한 같은 Drone만 이어 쓴다. 진행 중인 Drone이 파괴되거나 다른 Actor가 다음 Gate를 통과하면 부분 시도를 성공 기록으로 남기지 않는다.
- `ResetSequence()`는 진행 중인 시간·거리·부분 Segment만 폐기하고 이미 완료한 성공 Lap History는 현재 실행 동안 유지한다. Course 재구성은 코스 호환성이 달라질 수 있으므로 부분 시도와 성공 History를 함께 비운다.
- 평균 계산 함수는 0초·음수 시간이나 비정상 거리 입력에서 NaN·Infinity 대신 0을 반환한다. Recorder가 같은 Frame의 0초 Gate 경계를 받으면 가짜 기록을 확정하지 않고 해당 부분 시도를 취소한다.
- 이전 평균·Best·점수·결과 화면과 `USaveGame` 영속화는 TUT-03에 포함하지 않고 다음 `TUT-04` 이후 책임으로 유지한다.

### 자동화와 최종 검증

- `Drone.Tutorial.TrainingRecordCalculation`에서 cm/s 변환, 정상 평균 속도와 0·음수·NaN·Infinity 입력 안전성을 검증했다.
- `Drone.Tutorial.TrainingLapRecorder`에서 실제 `FTestWorldWrapper`의 Course, Gate 3개, Drone, Sequence와 Telemetry를 사용해 정상 2-Segment Lap을 검증했다.
- Lap Recorder 테스트는 꺾인 위치 표본의 실제 거리 합, World Game Time, Segment/Lap 평균 속도, 미래·역방향·중복 Gate 불변, 중간 Reset과 성공 History 보존, Course 재구성 시 History 초기화, 활성 Pawn 파괴 취소를 확인했다.
- `Drone.Tutorial.TrainingPIESmoke`를 실제 저장된 BP Gate 0→3 Overlap과 Recorder 상태까지 확장했다.
- `DroneEditor Win64 Development` Build 성공
- 전체 Tutorial 자동화: `6 succeeded / 0 failed / 0 warnings`
- 전체 `Drone.` 자동화: `14 succeeded / 0 failed / 0 warnings`
- 전체 Blueprint Compile: `0 errors / 0 warnings / 0 load failures`

### Git과 현재 판정

- `TUT-03` Done
- `TUT-04` Todo — 이전 성공 기록 평균·Best 비교와 Course/Gate/Lap 결과 UI
- Unreal Commit: `551e287e8a5de7fa33f28d1911f8a7a957bd66fa` (`feat: record tutorial lap timing and distance`)
- `codex/tutorial-lap-recording`과 `origin/main`에 Push 완료, 로컬 `main=origin/main=551e287e8a5de7fa33f28d1911f8a7a957bd66fa`

### 남은 사용자 수동 확인

- `Lvl_DroneTraining`에서 실제 Drone으로 Gate 0→3을 순서대로 통과해 조작감, Gate 간격과 시각 전환에 불편이 없는지 확인한다.
- TUT-03은 계산과 원본 기록까지라 결과 UI는 아직 없다. 시간·거리·평균·Best 비교 화면은 `TUT-04`에서 연결한다.
- `AST-01`의 실제 스피커 Drone Loop 단일 반복 재생과 Standalone 종료 후 정지는 여전히 미확인이다. 이 항목은 TUT-03 완료와 섞지 않고 별도 Doing으로 유지한다.

## 2026-08-25 — `C:\에셋` 제공 에셋 루트와 프로젝트 이식 재검증

### 현재 제공 에셋 위치 감사

- 사용자가 지정한 현재 제공 에셋 루트 `C:\에셋`을 읽기 전용으로 다시 감사했다. 이 PC에는 이전 D 드라이브 두 후보 경로가 없다.
- 공급사 해제본 14개 기준선은 최초 감사와 같은 10,499개·35,677,612,290 bytes다.
- `_Staging`, 내부 FBX 해제본, Unreal 생성 캐시를 포함한 현재 전체는 10,928개·866개 폴더·36,360,181,427 bytes다.
- 최초 감사에 사용한 최상위 ZIP 14개는 현재 C 드라이브에 없다. 과거 ZIP 14/14 대조 결과를 현재 재실행 결과처럼 사용하지 않고 역사 기록으로 구분했다.
- 현재 유일한 Archive인 `Non-Pilot Drones KITBASH SET\FBX.zip`의 55개 FBX와 해제 폴더 55개를 SHA-256으로 대조해 불일치 0을 확인했다.
- 라이선스·EULA·README·Manual 파일은 확인되지 않았다. `PBR Sting` Metadata의 `isAiForbidden: true`는 라이선스 자체가 아니므로 구매 증빙과 권리 조건을 별도로 보존·확인한다.
- `C:\에셋\DronePack_Project\Config\DefaultEngine.ini`의 활성 Android File Server에는 비어 있지 않은 토큰이 있었다. 값은 출력하거나 복사하지 않았고, 이 소스 팩 Config 전체를 이식·Commit 금지로 기록했다. 실제 Drone 프로젝트는 Plugin·네트워크 꺼짐, 빈 토큰 상태다.

### 실제 이식 대조

- `C:\URproject\drone\Content\Drone\ThirdParty` 12개·21,753,071 bytes와 `Content\Drone\Integrations`의 프로젝트 소유 BP 1개·34,484 bytes를 확인했다.
- FPV 10개와 Sound Wave는 UE 5.8 스테이징본과 SHA-256이 일치했다. Cue는 프로젝트에서 실제 Loop 설정을 켠 뒤 재저장했기 때문에 의도적으로 다르며 전용 테스트가 Loop 계약을 확인한다.
- 스테이징 선택 자산 감사와 현재 Integration Asset Registry 재감사에서 원본 `/Game/Drone_Pack`, `/Game/Drone-Sounds`, ThirdPerson, Variant 금지 의존성은 0이었다.
- Integration BP는 native Prototype Pawn을 부모로 사용하고 Body 1·Rotor 4·Auto Activate Audio 1만 더한다. Visual Collision·Overlap·Physics·Navigation은 꺼지고 native Collision Root·Movement·Camera·Input·Telemetry를 유지한다.

### 검증과 판정

- `Drone.Integration.FPVAsset` 새 실행: 1/1 Success
- 전체 Blueprint Compile 새 실행: 0 errors, 0 warnings, 0 failed to load
- 이식된 13개 `.uasset` 모두 Git LFS 대상, `git lfs fsck` 통과
- Unreal 저장소 `main=origin/main=551e287`, 작업 트리 깨끗함
- 전체 `Drone.` 14/14는 같은 현재 Commit에서 TUT-03 완료 시 통과한 전체 기준선이며 이번 재감사에서 전체 묶음을 다시 실행한 것으로 과장하지 않는다.
- 기존 Standalone 초기 렌더는 통과 기록이 있지만 이번 재감사에서 새 시각 캡처와 실제 청감은 하지 않았다. Body·Rotor·Camera 배치와 Loop 단일 재생·여러 경계·종료 정지는 사람이 확인해야 한다.
- 이식 파일·참조·구조는 Pass다. 실제 청감은 미확인이므로 `AST-01`은 Doing을 유지한다.

## 2026-08-26 — AST-02A NavigationArrows 1차 이식

### 사용자 확인과 범위

- 사용자가 제공 에셋은 지원과정을 통해 구매·지급된 것이므로 프로젝트 사용에 문제가 없다고 확인했다.
- 로컬 라이선스·영수증 파일 미발견은 증빙 보관 상태로 따로 기록하고 이식 차단으로 취급하지 않았다.
- 원본 11개 전체를 넣지 않고, 화면 밖 목표 방향 표시 Widget의 최소 폐쇄 집합만 이식하기로 했다.

### 실제 변경

- 별도 `NavigationArrowsStage` UE 5.8 프로젝트에서 원본 경로 `/Game/NavigationArrows`를 유지해 11개를 먼저 로드했다.
- Unreal 내부 이동으로 6개를 `/Game/Drone/ThirdParty/NavigationArrows`에 옮겨 참조를 갱신하고 재저장했다.
- Widget Blueprint 1개, Texture2D 2개, UserDefinedStruct 3개만 실제 Drone 프로젝트에 복사했다.
- Demo Map·BuiltData·Example Actor·Example Mesh·미사용 Circle Texture는 제외했다.
- `DroneNavigationArrowsAssetTest.cpp`를 추가해 Generated Class, Target 변수 계약, Texture·Struct 로드와 제외 자산 부재를 검증했다.
- 재현용 `tools/unreal/Audit-NavigationArrows.py`, `tools/unreal/Stage-NavigationArrows.py`를 문서 저장소에 추가했다.

### 검증 결과

- 원본·대상 Asset Registry 감사: 로드 실패 0, 외부 `/Game` 의존성 0
- UE 5.8 스테이징 Target Blueprint Compile: 0/0/0
- `DroneEditor Win64 Development`: 성공
- 전용 자동화: 1/1 성공
- 전체 `Drone.`: 15/15 성공, warning·failure 0
- 실제 프로젝트 Blueprint Compile: 0 errors, 0 Blueprint warnings, 0 failed loads
- 프로젝트 6개가 검증된 스테이징 6개와 SHA-256 일치
- Git LFS 속성 6/6, `git lfs fsck` 정상

첫 C++ 빌드는 `UUserDefinedStruct` 헤더 경로를 잘못 적어 실패했다. UE 5.8 실제 경로인 `StructUtils/UserDefinedStruct.h`로 수정한 뒤 빌드가 성공했다. 첫 전용 테스트는 Blueprint 변수의 GUID 접미사를 고려하지 않아 `TargetWorldLocation` 탐색이 실패했고, 접두사 기반 반사 검사로 수정한 뒤 1/1과 전체 15/15를 통과했다. 두 실패는 수정 전 검사 결함이며 최종 자산 결함으로 남지 않는다.

### 현재 판정

- 기술 이식·검증: 완료
- Git: Commit `5a052c8`을 `origin/codex/navigation-arrows-migration`에 Push 완료. 이후 `fb1d7ad`로 main 병합·Push 완료
- 실제 화면 연결: 미구현. 자산이 준비됐을 뿐 Training HUD 기능 완료가 아님
- `AST-01`: 실제 스피커 Loop 확인 전까지 계속 Doing
- `TUT-04`: 다음 기능 카드 유지

## 2026-08-26 09:17 — 작업 PC·Git·Editor 상태 재동기화

### 실제 확인

- 현재 Unreal 작업 경로는 `D:\JGY\project\drone`, 문서 경로는 `D:\JGY\project\md`다.
- Drone 로컬 `main`과 `origin/main`은 `551e287`로 일치하고 작업 트리는 깨끗하다.
- NavigationArrows 최소 이식은 Commit `5a052c8bab2eb0dd8bc9ab16cfc7b3784e8e4cd7`로 `origin/codex/navigation-arrows-migration`에 Push됐다. 이 Commit의 부모는 `551e287`이며 main에는 아직 병합하지 않았다.
- 문서 저장소는 최신화 직전 로컬 `main=origin/main=466609d`이고 작업 트리가 깨끗했다. 이번 최신화는 로컬 문서 변경으로 남기며 Commit·Push는 사용자가 수행한다.
- 현재 PC의 제공 에셋 루트는 `D:\JGY\project\Unreal_260821`이다. ZIP 14개·공급사 폴더 14개와 `_Staging`을 확인했고 `C:\에셋`은 이 PC에 없다.
- UE 5.8.1 Editor PID 9884가 D 드라이브 프로젝트로 실행 중이다. 로그에 MCP 서버 시작과 23 Toolset 등록이 있고 `127.0.0.1:8000/mcp`가 응답한다.

### 판정과 다음 작업

- `AST-02A` 최소 이식·검증·main 공유는 Done이다. 실제 Navigation Host/Wrapper는 후속 카드다.
- `UE-MCP-02`는 Drone 루트의 새 Codex 작업에서 네이티브 Tool 노출을 확인하기 전까지 Todo다.
- `AST-01` 실제 스피커 Loop와 TUT-03 실제 Gate 0→3 한 Lap은 계속 수동 미확인이다.
- 다음 기능 카드는 `TUT-04 이전 기록 비교·Best·결과 UI`다.

## 2026-08-26 09:44 — Dataflow·Chaos 그물·맵 파괴 방향 추가

### 확인

- Epic UE 5.8 소개와 Release Notes에서 Dataflow와 Chaos Cloth의 Production-Ready 상태, Dataflow의 Chaos Destruction 비파괴 반복 제작 용도를 확인했다.
- 공식 Cloth Node 문서에서 Max Distance 0 정점은 Kinematic이 되고 별도 `InKinematic` Selection도 사용할 수 있음을 확인했다.
- Chaos Fields 문서에서 Anchor, External/Internal Strain, Force, Sleep/Disable Field가 Geometry Collection의 고정·파괴·정리에 사용됨을 확인했다.
- 현재 UE 5.8.1 설치본에는 필요한 Dataflow/Chaos Cloth/Geometry Collection 플러그인이 있지만 `Drone.uproject`에는 아직 명시적 Cloth/Destruction Plugin을 추가하지 않았다.

### 결정

- 부분 고정 그물은 `Chaos Cloth + Dataflow`, 선택형 맵 파괴는 `Chaos Destruction + Geometry Collection + Dataflow`로 분리한다.
- 그물 고정부는 Weight Map의 Max Distance 0 또는 Kinematic Selection으로 만들고 나머지 영역만 처지게 한다.
- 포획·Crash·Damage·Mission Event는 물리 결과에 직접 종속시키지 않고 프로젝트 C++ Trigger/상태로 결정한다.
- 맵 전체 파괴는 제외하고 얇은 벽·출입구·Jammer 설비부터 한 종류씩 검증한다.
- 현재 기능 순서는 바꾸지 않는다. `TUT-04` 이후 별도 `PHY-DF-00` Sandbox에서 Plugin·Build·회귀를 먼저 검증한다.
- 상세 계획: [`DRONE_CHAOS_DATAFLOW_PLAN.md`](../gameplay/DRONE_CHAOS_DATAFLOW_PLAN.md)

### 현재 변경 경계

- Unreal Plugin 활성화 0
- Cloth/Geometry Collection 생산 자산 0
- C++ 변경 0
- 문서 계획만 추가, Commit·Push는 사용자 수행

## 2026-08-26 09:48 — 별도 `droner` Editor와 대용량 Untracked 에셋 확인

- 계획 검증 종료 시점에 기존 기준 `drone` Editor PID 9884가 종료되고 PID 10960이 `D:\JGY\project\droner\Drone.uproject`를 실행 중인 것을 확인했다.
- Port 8000 MCP Listener도 PID 10960이 소유하므로 현재 MCP 대상은 기준 `drone`이 아니라 `droner`다.
- `droner`는 같은 Git 원격과 `main=origin/main=551e287`을 사용한다.
- `droner/Content/Asset`에는 공급사 14개 폴더와 `_Staging`, 총 10,928개·36,360,181,427 bytes가 Untracked로 존재한다.
- 이 폴더는 전체 제공 소스 복사본이며 프로젝트 선별 이식 규칙을 만족하지 않는다. 일괄 Stage·Commit·Push 금지로 기록한다.
- 기준 `drone`과 `droner`에는 Editor가 추가한 `Config/DefaultEditor.ini` 변경이 있다. 이 작업에서는 되돌리거나 Commit하지 않았다.
- Dataflow/Chaos 구현을 시작할 때는 `droner` Editor를 닫고 기준 `D:\JGY\project\drone`을 연 뒤 별도 Branch에서 진행한다.

## 2026-08-26 11:50 — AST-01C DronePack 드론 시각 자산·정리 맵 이식

### 실제 변경

- `D:\JGY\project\Unreal_260821\DronePack_Project`를 UE 5.8 전용 스테이징에서 감사했다.
- 공급사 전체 기능 Blueprint는 Mannequin 누락, 구형 입력과 `ABP_Quinn_PostProcess` 중복 AnimGraph 오류가 있어 그대로 들여오지 않았다.
- 원본 Demo Map의 Drone Blueprint 6개를 Static Mesh 표시 Actor로 바꾸고, 열화상 Mannequin 3개·도우미 Collision/Camera Proxy·삭제 Actor를 참조하던 Level Blueprint Event Graph를 제거했다.
- 드론 `D_Mesh` 시각 자산과 정리 Map의 폐쇄 의존성만 `/Game/Drone/ThirdParty/DronePack`에 복사했다.
- 최종 이식 수량은 `.uasset` 153개와 `.umap` 1개, 총 154개·82,465,487 bytes다. 기존 파일 덮어쓰기는 0개다.
- 공급사 Pawn·Controller·GameMode·Input·HUD와 중복 FPV 기능 자산은 제외했다. 전역 시작 Map/GameMode와 프로젝트 C++ 공개 API는 변경하지 않았다.

### 검증과 발견

- 스테이징 Map 전이 Game 의존성은 161개이며 외부·누락 의존성 0이다.
- 실제 프로젝트에서 154/154 Package를 UE 5.8로 Resave했다.
- 정리 `Map_Demo` Map Check는 0 errors / 0 warnings다.
- 전체 Blueprint Compile은 0 errors / 0 warnings / 0 failed loads다.
- 처음 전체 자동화를 실행했을 때 Source보다 Editor DLL이 오래되어 12개만 탐색되는 것을 발견했다.
- `-CompilerVersion=14.51.36256`을 하나의 문자열 인자로 전달해 `DroneEditor Win64 Development`를 다시 빌드했다. 첫 호출의 PowerShell 점 구분 오류는 명령 인자 오류였고 소스 컴파일 오류가 아니다.
- 재빌드 DLL 기준 전체 `Drone.` 자동화는 14 succeeded / 0 warnings / 0 failed다. `TrainingLapRecorder`와 `TrainingRecordCalculation`을 포함하며 PIE Lifecycle 새 실행 3/3도 통과했다.
- 이식 154개 모두 Git LFS filter 대상이고 `git lfs fsck`, `git diff --check`가 통과했다. 원본 `/Game/Drone_Pack`, ThirdPerson, Variant 문자열 잔존도 0이다.

### 현재 판정과 다음 작업

- `AST-01C` 기술 이식·자동 검증: 완료
- `AST-01C` 수동 화면 검토: 미확인 — 드론 6종, 환경, 재질, 스케일, 조명과 카메라 구도를 Editor에서 확인해야 함
- 현재 기준 `drone` Editor PID 22936 실행 중. 이미 열린 인스턴스를 프로세스 조회가 놓쳐 추가로 실행된 PID 2764는 `CloseMainWindow`로 정상 종료했고 기존 Editor는 보존함
- Unreal Git: `main=origin/main=551e287`, 기존 `Config/DefaultEditor.ini` 변경과 새 DronePack 154개가 미커밋. 사용자가 Commit하며 Push하지 않음
- 다음 자산 작업: 화면 검토 뒤 선택 Mesh를 프로젝트 소유 Integration BP에 연결
- 다음 기능 작업: 기존 순서대로 `TUT-04` 이전 평균·Best 비교와 결과 UI

## 2026-08-26 12:57 — 사용자 요청 중단 정리

- `UnrealEditor`와 `UnrealEditor-Cmd`를 모두 종료했고 원본·스테이징·Git 변경을 삭제, 되돌림, Commit, Push하지 않았다.
- Course/HUD는 한글 현재 비행값, 최근/평균 구간 통계, Gate 배열 자동 동기화, 200 cm 거리 샘플 곡선 표시까지 코드에 반영됐다. 마지막 폰트 보강 전 Build와 집중 자동화 8/8은 통과했지만 최종 전체 검증과 화면 확인은 남았다.
- 환경 팩은 실제 Drone 저장소에 아직 복사하지 않았다. 스테이징 Battlefield 1,191개/Map 4만 새 경로로 변환됐고, 비호환 Demo Character 102개가 원본 경로에 남았다. MilitaryCamp 668개와 MilitaryBase 1,474개 원본은 보존됐다.
- 재개 순서: 스테이징 재감사 → 세 팩 의존성 정리·변환 → 실제 프로젝트 이식 → Build·BP Compile·Map Check·전체 자동화 → Training Map 저장·한글 HUD/곡선 화면 확인.

## 2026-08-26 13:11 — 중단 작업 재개·NavigationArrows main 병합

- `C:\URproject\drone`에서 기존 main `5540c6b`와 NavigationArrows 기능 Commit `5a052c8`의 분기를 확인했다.
- 기존 main 작업을 유지한 채 `--no-ff` Merge Commit `fb1d7ad`를 만들고 `origin/main`에 Push했다.
- 병합 main Build 성공.
- `Drone.Integration.NavigationArrowsAsset` 1/1 Success.
- 전체 `Drone.` 15/15 Success.
- Blueprint Compile 0 errors, 0 Blueprint warnings, 0 failed loads.
- NavigationArrows LFS 속성과 `git lfs fsck` 통과.
- 최종 `main=origin/main=fb1d7ad`, Drone 작업 트리 Clean.
- 실제 Training HUD Host/Wrapper와 PIE/Standalone 시각 확인은 구현하지 않았으므로 완료로 기록하지 않는다.

## 2026-08-26 13:21 — TUT-04A PIE 초기 화면 확인

- 정확한 `C:\URproject\drone\Drone.uproject`를 UE 5.8.1로 열고 `Lvl_DroneTraining`을 PIE 실행했다.
- 화면 좌측 상단에서 한글 `드론 비행 정보`, 현재 속도·고도·수직 속도·진행 방향이 정상 표시됐다.
- 화면 좌측 하단에서 한글 `코스 구간 기록`과 최근·완료 구간 속도/거리/시간 자리표시자가 정상 표시됐다.
- 현재 Gate Ring, 뒤쪽 Gate들, 세분화된 발광 코스 선이 뷰포트에 표시됐다.
- 공급사 NavigationArrows Host/Wrapper는 아직 미구현이므로 별도 화살표 Widget은 표시되지 않았다.
- 자동 UI의 짧은 키 입력으로는 지속 전진이 되지 않아 Gate 0→3 한 Lap과 구간 숫자 갱신은 확인하지 못했다.
- PIE와 Editor를 정상 종료했다. 13:21 KST Unreal 프로세스 0, Drone 작업 트리 Clean이다.

## 2026-08-26 16:55 — 맵 이식 상태 재확인

- 실제 저장소의 ThirdParty `.umap`은 `Content/Drone/ThirdParty/DronePack/Map/Map_Demo.umap` 1개다.
- 이 맵은 Commit `5540c6b`로 main에 포함됐고 Git LFS 대상이다.
- 기존 AST-01C 결과인 외부 Game·누락 의존성 0, Map Check 0/0, Blueprint 0/0/0과 LFS 검증을 현재 기술 완료 근거로 유지한다.
- `Map_Demo`에서 드론 6종·재질·스케일·조명을 직접 보는 최종 시각 검토는 아직 하지 않았다.
- Battlefield·MilitaryCamp·MilitaryBase 이름의 `.umap`은 현재 Drone 저장소에 0개다. Battlefield 스테이징 변환과 세 팩 실제 이식·대표 맵 검증은 `AST-03A` Doing으로 남긴다.
- `Lvl_DroneTraining`은 외부 맵 이식 결과가 아니라 프로젝트 소유 Tutorial Map이다.

## 2026-08-26 — RabbitHole 참고·맵 중앙화·템플릿 콘텐츠 정리

### 참고 구조와 결정

- 실제 최신 RabbitHole 프로젝트 `C:\project\Fractured\GoDownTheRabbitHole.uproject`의 Content와 Config를 확인했다.
- RabbitHole은 프로젝트 소유 맵을 `Content/Maps`에 모으고 Blueprint를 AI·GameMode·PlayerManager·Widget 등 역할별 폴더로 나눈다. 공급사 맵은 공급사 폴더에 유지한다.
- Drone에는 프로젝트에서 실제 사용하는 맵만 `/Game/Drone/Maps`에 모으는 규칙을 적용했다. 공급사 Mesh·Material 등 의존 자산은 ThirdParty 경계를 유지한다.

### 실제 변경

- `/Game/Drone/Tutorial/Maps/Lvl_DroneTraining` → `/Game/Drone/Maps/Lvl_DroneTraining`
- `/Game/Drone/Prototype/Maps/Lvl_DronePrototype` → `/Game/Drone/Maps/Lvl_DronePrototype`
- `/Game/Drone/ThirdParty/DronePack/Map/Map_Demo` → `/Game/Drone/Maps/Lvl_DronePackShowcase`
- Showcase BuiltData도 같은 중앙 맵 폴더로 이동했다.
- `/Game/ThirdPerson`, `/Game/Variant_Combat`, `/Game/Variant_Platforming`, `/Game/Variant_SideScrolling`과 대응 ExternalActors/ExternalObjects를 제거했다.
- `DefaultEngine.ini`, `DefaultEditor.ini`, Editor Content Browser 기본 경로와 자동화 테스트의 맵 경로를 새 기준으로 갱신했다.
- 기본 실행·Editor 시작 맵은 `Lvl_DroneTraining`, 전역 GameMode는 프로젝트 소유 `BP_DronePrototypeGameMode`다.
- C++ `DroneCharacter`, 기존 GameMode/Controller와 Variant Source는 Source/Build.cs 별도 감사가 필요해 보존했다.
- Git 감지 기준 변경 규모는 599개 경로, 삭제 589개, 이름·위치 변경 2개, 새 경로 추가 2개다. 삭제 파일은 Git 이력에서 복구할 수 있다.

### 감사와 검증

- 삭제 전 프로젝트 맵 3개의 네 Template Root 의존성 0, `/Game/Drone` 자산의 외부 참조 0을 확인했다.
- 중앙 맵 3개와 Showcase BuiltData 로드 성공.
- 이전 맵 경로와 제거 대상 Template Root 자산 0.
- `DroneEditor Win64 Development` Build 성공.
- Blueprint Compile `0 errors / 0 warnings / 0 failed loads`.
- 전체 `Drone.` 자동화 `15/15` 성공.
- 중앙 맵 4개 LFS 속성, `git lfs fsck`, `git diff --check` 통과.

### Git과 남은 확인

- 기능 Commit: `1c8f391 chore: centralize drone maps and remove templates`
- main Merge Commit: `2cc5d79 merge: centralize drone maps and remove templates`
- 기능 Branch와 `origin/main` Push 완료. 최종 `main=origin/main=2cc5d79`, Drone 작업 트리 Clean.
- 프로젝트 맵 중앙화와 템플릿 콘텐츠 정리는 완료다.
- `Lvl_DronePackShowcase`의 드론 6종·재질·스케일·조명 시각 검토와 `Lvl_DroneTraining` 한 Lap 수동 비행은 아직이다.
- Battlefield·MilitaryCamp·MilitaryBase 환경 맵은 여전히 미이식이다.
- 현재 폴더 규칙: [`DRONE_CONTENT_FOLDER_GUIDE.md`](../assets/DRONE_CONTENT_FOLDER_GUIDE.md)

## 2026-08-26 19:35 — 삭제 범위 교정·환경 맵 3종 실제 이식

### 삭제 범위 교정

- 사용자가 삭제를 허용한 대상은 Unreal 프로젝트 생성 때 포함된 기본 Map이었다. Content Root 전체 삭제로 해석한 것은 범위가 넓었다.
- `fb1d7ad`에서 비맵 자산 62개를 복구해 `909f6a3 fix: restore template assets while keeping starter maps removed`로 분리했다.
- 복구 후 Asset Registry 수는 ThirdPerson 4, Variant_Combat 30, Variant_Platforming 10, Variant_SideScrolling 18이다.
- 삭제 상태를 유지한 것은 `Lvl_ThirdPerson`, `Lvl_Combat`, `Lvl_Platforming`, `Lvl_SideScrolling`과 각 Map 전용 ExternalActors/ExternalObjects뿐이다.

### 스테이징과 선택

- 원본 `C:\에셋`은 수정하지 않고 `C:\에셋\_Staging\EnvironmentStage`에서 3팩 3,334개·18.76 GiB와 Map 10개를 감사했다.
- 대표 Map은 Battlefield `PL_Battlefield`, MilitaryCamp `Map_MilitaryCamp`, MilitaryBase `MilitaryBase`로 선정했다.
- 프로젝트 중앙 사본은 `/Game/Drone/Maps/Lvl_Battlefield`, `Lvl_MilitaryCamp`, `Lvl_MilitaryBase`다. 세 Map의 공급사 GameMode Override는 제거해 프로젝트 기본 GameMode를 상속한다.
- 대형 팩 내부 경로 수천 개를 강제로 재작성하지 않고 검증된 정확한 의존성만 공급사 Root 그대로 보존했다.

### 호환 보강과 이식 규모

- Battlefield의 Manny/Quinn 구 경로 2개는 팩 내부 실제 Mesh로 정확 경로 호환 사본을 만들었다.
- MilitaryCamp의 누락 직접 Map 참조 `Map_MilitaryCampValley3`는 현재 공급 `Map_RockyGrassland`의 호환 사본으로 닫았다.
- MilitaryBase의 Grass Preview Mesh 경로와 Glow Material 기본 Texture Override를 정리하고, 외부 RacingTrack Blueprint를 끌던 TireTrack 데모 Actor 6개를 중앙 Map 사본에서 제거했다. `/Game/Textures/T_Linear_Grad` 호환 Texture도 로컬 자산에서 만들었다.
- 최종 이식은 2,723개·18,211,844,112 bytes(16.96 GiB): Battlefield 710, MilitaryCamp 593, MilitaryBase 1,414, 중앙 Map 3, 호환 3이다.
- Battlefield Map Check에서 완전히 빈 독립 StaticMeshActor 1개를 중앙 Map에서 제거했다. 건물 Blueprint 14개는 일부 선택적 컴포넌트만 비어 있고 다른 실제 Mesh가 정상 연결되어 있어 삭제하지 않았다.

### 최종 검증

- `DroneEditor Win64 Development` Build 성공. 처음 지정한 미설치 MSVC 14.51.36256 호출은 컴파일 전 실패했고, 실제 설치 14.51.36231로 다시 실행해 성공했다.
- 전체 Blueprint Compile: `0 errors / 0 warnings / 0 failed loads`. 별도 자산 로그에는 Battlefield Manny/Quinn Pose GUID 경고 28건과 MCP EULA 안내 1건이 있다.
- 전체 `Drone.` Automation: 15/15 성공. 14개 무경고, 기존 `PIEInputLifecycle`의 RecastNavMesh 미발견 경고 포함 성공 1개다.
- Map Check: Battlefield 오류 0·공급 Blueprint NULL StaticMesh 메시지 14건, MilitaryCamp 0/0, MilitaryBase 0/0.
- 환경별 Game 의존성 누락 0, 허용 외 경로 0, 중앙 Map World Load와 GameMode None 확인.
- 신규 2,723개 전부 3줄 Git LFS Pointer, `git diff --check`, `git lfs fsck` 통과.
- 환경 이식 Commit: `f8c8fb2 feat: migrate validated environment maps`.

### 남은 사람 확인

- UE 5.8.1 Editor에서 환경 Map 3개를 각각 열어 조명·재질·스케일·Landscape·Collision과 드론 Spawn 위치를 눈으로 확인한다.
- 세 맵 중 어느 것을 데모 주력 Map으로 쓸지는 현재 미정이며, 기술 이식 완료를 최종 채택으로 표현하지 않는다.
## 2026-09-11 17:13 — CourseSpline과 분리된 Ring별 Handle 직접 편집

- 첫 구현의 `Spline Point 1개=Ring 1개`는 Ring 이동이 코스 곡선까지 바꾸므로 사용자 요구와 다름을 확인하고 폐기했다.
- `ADroneTrainingCourse`에 CourseSpline과 분리된 `Ring별 Spline Handle` 배열을 추가했다. `MakeEditWidget` 3D 점을 움직이면 가장 가까운 Spline 위치로 투영되고 Ring만 해당 위치·접선 회전을 따른다.
- Handle 배열 항목 수가 Ring 수이며 추가·삭제가 Ring·Sequence 수에 반영된다. 현재 숫자/수동 배치에서 Handle을 초기화하는 Editor 버튼과 전체 Handle을 다시 Spline에 붙이는 버튼도 추가했다.
- 자동화에 Handle Spline 투영, 추가·삭제, Ring·Sequence 수 변경과 CourseSpline 제어점 수·위치 불변 검사를 추가했다.
- Unreal Editor가 없는 상태에서 MSVC 14.51.36257 `DroneEditor Win64 Development` 최종 Build 성공, 최종 `Drone.Tutorial.TrainingCourse` 1/1 성공(0 warning/0 error), `git diff --check`와 `git lfs fsck` 통과.
- 작업 중 `3df654a`에 이어 사용자 `0911임시버전` 커밋 `46efd2e`까지 동기화됐다. 기존 자동 Ring/Gate 색상 Source·테스트·도구와 기관총 자산 10개는 이 커밋에 추적됐고 독립 Handle 변경 3개는 로컬에 보존됐다.
- 최종 감사 중 팀원 Training Map 후속 `55d6c61`과 Merge `9de1ead`가 추가되어 Fast-forward했다. 코드 충돌은 없었고 최신 Map에서도 Gate 17/Sequence 4, 역할 표적/Carryable 0 상태가 동일함을 `TrainingAssets`로 다시 확인했다.
- 최신 `Lvl_DroneTraining`은 원격과 같은 Clean 상태로 보존했다. 읽기 전용 감사와 `TrainingAssets` 재실행에서 Gate Actor 17개·Course Sequence 4개·역할 표적/Carryable 0개를 확인했다. 화면에서 실제 코스 Gate 범위와 순서를 확인한 뒤 독립 Handle 모드를 맵에 적용한다.
- Commit·Push하지 않았다.

## 2026-09-15 — 진행 상태와 차후 목록 재정리

- `git status -sb`와 마지막 Commit을 다시 확인했다. 확인 시작 시 Unreal은 `10da7ce`, 문서는 `27d002d`이고 각각 로컬 `origin/main`과 같으며 작업 트리는 Clean이었다.
- 2026-09-15 실시간 `git fetch origin --prune`은 두 저장소 모두 DNS 오류(`Could not resolve host: github.com`)로 실패했다. 따라서 GitHub 서버에 추가 Commit이 없는지는 네트워크 복구 후 다시 확인한다.
- 독립 Ring Handle Source/Test 3개는 Unreal `10da7ce`에, 직전 문서 갱신은 `27d002d`에 반영돼 더 이상 미커밋 대상이 아니다.
- UE 5.8 Editor가 `D:\JGY\project\drone\Drone.uproject`로 실행 중임을 확인했다. C++ 변경이나 전체 Build 전에는 저장 후 종료한다.
- 최종 Handle 보고서 `IndependentRingHandles_Final_20260911`은 `Drone.Tutorial.TrainingCourse` 1/1 성공, 0 warning/0 error다. 최신 Map 감사 `TrainingAssets_9de1ead`는 1/1 실패·8 errors이며 Gate Actor 17개/Sequence 4개, 역할 표적 3종과 Carryable 0개가 원인이다.
- 현재 알려진 실패 테스트는 `TrainingAssets`, `TrainingPIESmoke`, `NPCPerceptionSearchPIE` 3개이며 전체 자동화 Pass로 표시하지 않는다.
- 다음 순서를 `Training Map 링 범위·순서 확정 → 독립 Handle 배치와 역할 표적/Carryable 복원 → 한 Lap·두 Lap HUD 수동 확인 → 실패 3개 수정과 전체 회귀 → Mission 목표 Rule 데이터화 → Jamming → 수동 회귀 묶음 → Dataflow/Chaos Spike`로 정리했다.
- 코드와 Map은 이번 정리에서 변경하지 않았다. `CONTEXT.md`, `STATUS.md`, `WORKBOARD.md`, 이 Worklog만 최신화했으며 Commit·Push는 사용자가 진행한다.

## 2026-09-15 — Training 보존과 TestMap 분리 결정

- 사용자 결정으로 `/Game/Drone/Maps/Lvl_DroneTraining`은 현재 상태를 유지하고 기능 시험 중 직접 저장하거나 덮어쓰지 않는다.
- 목표 폴더는 `/Game/Drone/Maps/TestMap`이다. `Lvl_DroneTraining_Test` 사본에서 Ring·역할 표적·HUD·Mission 기능을 검증한 뒤 사용자 승인된 변경만 원본 Training에 반영한다.
- 이동 확정 후보는 `Lvl_DronePrototype`, `Lvl_NPCSmartObjectGreybox`, `Lvl_DronePackShowcase`, `Lvl_MilitaryBase_Test`다. `test1`, `test2`는 팀원 수정 이력과 용도를 먼저 확인하고 의미 있는 이름으로 바꿔 이동한다.
- 파일 탐색기 이동은 금지한다. Unreal AssetTools로 Move/Rename하고 C++ 테스트·Migration Tool·Soft Reference를 갱신한 뒤 Redirector, Map Load, Map Check, Blueprint Compile, 전체 자동화와 LFS를 검증한다.
- 이번 기록에서는 Unreal 자산을 이동·복제하지 않았다. Editor가 실행 중이고 사용자 표현이 `그거 다 하고나면`이므로 `MAP-TEST-01` 후속 카드로 등록했으며 현재 Training Map은 건드리지 않았다.

## 2026-09-15 — 팀원 Training Map과 기능 시험 완전 분리

- 사용자가 `Lvl_DroneTraining`에서 팀원이 실제 Tutorial 환경을 제작 중이고 Map 분할도 어렵다고 확인했다.
- 기존 `Lvl_DroneTraining_Test` 전체 복제 계획은 폐기했다. 374.94MiB Training Map과 Environment·Landscape를 복사하지 않고 `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest`를 빈 경량 맵으로 새로 만든다.
- 경량 맵에는 기본 바닥, PlayerStart, Prototype GameMode, Course/Gate, 역할 표적, Carryable, HUD 검증에 필요한 Actor만 둔다. 실제 코스 배치나 환경 제작은 포함하지 않는다.
- TestMap에서 통과한 C++/Blueprint/Data Asset과 배치 가이드를 Training 담당자에게 전달한다. 실제 Training Map의 저장·자동 배치·분할·덮어쓰기는 담당자와 통합 시점을 정하기 전 금지한다.
- `TrainingAssets`와 `TrainingPIESmoke`는 실제 맵 중간 상태를 보여주는 Production 감사로 남긴다. 개발용 TestMap 검사를 별도로 추가해 원본 검사를 억지로 녹색으로 만들지 않는다.

## 2026-09-15 — 외부 엔지니어링 참고 5종 검토·팀 규칙 반영

- Ponytail, ECC, Archify, fmt, Matt Pocock Skills의 기본 브랜치 README와 License를 검토했다. CLI의 GitHub DNS 조회가 실패해 특정 Commit SHA는 고정하지 못했으며 실제 도입 전 Version/Commit을 다시 고정한다.
- Ponytail의 최소 의존성 판단 순서, ECC의 계획→테스트→구현→검토→검증→기록 Loop, Archify의 근거 기반 Workflow/Sequence 표현, Matt Pocock Skills의 공유 용어·ADR·TDD·원인 우선 진단을 Drone Playbook으로 재작성했다.
- `Source/Drone` 감사에서 fmt Include/Namespace 사용이 없음을 확인했다. Runtime UI는 `FText`, 내부 문자열과 로그는 Unreal 기본 체계를 사용하므로 fmt를 새 의존성으로 추가하지 않는다.
- ECC와 Ponytail은 Hook/Skill 범위가 겹치므로 동시에 설치하지 않는다. Archify와 Matt Pocock Skills도 현 단계에는 설치하지 않는다. 새 Plugin/Hook/Library/Node Package, Codex 전역 설정, `Drone.Build.cs` 변경은 0이다.
- 공유용 폴더 [`EXTERNAL_ENGINEERING_REFERENCES`](../reference/external-engineering/README.md)에 저장소별 Review, 팀 Playbook, 격리 도입 계획을 추가하고 `DOC-EXT-01`을 Done 처리했다. `AI-TOOL-REVIEW-01`은 TestMap Vertical Slice 이후로 등록했다.
- 기능 우선순위는 바꾸지 않는다. 바로 다음은 팀원 Training을 건드리지 않는 경량 `Lvl_DroneTutorialSystemsTest` 생성과 TestMap 전용 검증이다.

## 2026-09-15 — 경량 Tutorial Systems Test Map 생성·검증

- 작업 시작 시 Unreal은 `main=origin/main=10da7ce` Clean이고 UE Editor 프로세스가 없음을 확인했다. 팀원 `/Game/Drone/Maps/Lvl_DroneTraining`은 Git 변경 0으로 유지했다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest`를 284,865 bytes로 새로 만들었다. 대형 Environment/Landscape를 복사하지 않고 기본 Cube 바닥, PlayerStart, Directional/Sky Light, Prototype GameMode만 사용했다.
- `BP_DroneTrainingCourse`에 여섯 점의 곡선 Spline과 100cm 표시 Segment, CourseSpline과 분리된 독립 Ring Handle 5개를 구성했다. `BP_DroneTrainingGate` 생성 Ring 5개와 Sequence 5개가 일치한다.
- Recon/Impact/Payload 역할 표적 BP를 각 1개, `BP_DroneCarryablePayload`를 1개 배치했다. 최종 위치·크기·가시성은 Editor 수동 확인 전이므로 기술 배치 완료와 화면 완료를 구분한다.
- `BuildDroneTutorialSystemsTestMap.py`를 추가했다. 기존 맵에서는 기본 Validate-only이고 환경 변수와 PowerShell `Rebuild`를 명시한 경우에만 `DroneTutorialSystemsTest.Owned` Tag Actor를 다시 만든다.
- 첫 생성 실행은 UE Python에 노출되지 않은 `rerun_construction_scripts` 호출에서 중단됐다. 빈 TestMap만 저장된 상태를 확인하고, 이미 재구성을 수행하는 공개 Course API와 중복된 호출을 제거한 뒤 명시적 Rebuild로 정상 완성했다. 이 실패를 성공으로 숨기지 않았으며 후속 Wrapper에는 `-ScriptErrorsAreFatal`과 로그 검사 조건을 넣었다.
- `Invoke-DroneTutorialSystemsTestMap.ps1 -Mode Validate`는 별도 UserDir/Log로 성공했다. 명시적 Map Check 결과 0 errors/0 warnings, `DRONE_TUTORIAL_TESTMAP|VALIDATION_OK`는 rings=5/targets=3/carryable=1이다.
- 새 `Drone.Tutorial.TutorialSystemsTestMap` 자동화는 저장 Map을 새 프로세스에서 로드해 PlayerStart 1, 선배치 Drone 0, Course 1, Role Target 각 1, Carryable 1, Ring/Sequence 5, 독립 Handle 모드, Prototype GameMode, Legacy Actor 0을 검사했고 1/1 Success다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build는 성공했다. 첫 Build 호출의 CompilerVersion 분리는 PowerShell 인자 오류였고 하나의 문자열 인자로 다시 실행해 해결했으며 C++ 컴파일 오류가 아니었다.
- `.gitattributes`는 파일 크기와 무관하게 모든 `.uasset`·`.umap`을 LFS 대상으로 둔다. 새 TestMap은 `filter=lfs diff=lfs merge=lfs`, C++·Python·Markdown은 일반 Git이다.
- 현재 Unreal 변경은 새 TestMap 1개, 자동화 C++ 1개, 생성 Python 1개, 검증 PowerShell 1개다. Commit·Push하지 않았다. 다음은 Editor에서 곡선 안내선, Ring 3상태 색, 역할 표적, Carryable, HUD와 한/두 Lap을 직접 확인하는 것이다.

## 2026-09-15 — Git LFS 용량 원인 감사와 비파괴 절감 계획

- 현재 `.gitattributes`가 크기와 무관하게 모든 `.uasset`·`.umap`을 LFS로 처리하고, `lfs.fetchinclude`·`lfs.fetchexclude` 별도 설정은 없음을 확인했다.
- 사람이 읽는 LFS 크기 표시는 반올림되므로 `git lfs ls-files --json`의 정확한 Byte로 재집계했다. 현재 Commit은 LFS 5,550개·약 27.66GiB다. 1MiB 미만은 3,602개·0.45GiB(1.6%)이고, 10~100MiB 942개가 21.34GiB(77.2%)다.
- 70MiB Threshold를 가정하면 5,538개·25.67GiB가 일반 Git으로 이동하고 LFS에는 12개·1.99GiB만 남는다. 100MiB Push 차단까지 여유는 생기지만 일반 Git 저장소·Binary 이력·Clone 부담이 커지므로 용량 해결책으로 채택하지 않았다.
- 전체 로컬 Ref의 고유 LFS Object는 6,137개·약 29.62GiB다. 현재 Commit보다 약 1.96GiB만 크므로 현재는 오래된 이력보다 Checkout에 포함된 Asset 범위가 주원인이다.
- 프로젝트 소유 `Content/Drone` 중 ThirdParty 제외 범위 0.89GiB, `Content/Drone/ThirdParty` 4.61GiB, `Content/Drone` 밖 Vendor Root 22.16GiB로 집계됐다. 큰 감사 후보는 `MillitaryBase` 7.67GiB, `FC_MilitaryCamp` 6.20GiB, `STF` 3.04GiB, `Battlefield` 2.71GiB다.
- LFS는 변경된 Package의 새 전체 Object를 저장하므로 374.94MiB Training Map과 약 206MiB MilitaryBase Map의 반복 저장을 줄인다. 팀원 Training을 보존하고 284,865-byte 경량 TestMap을 만든 현재 분리는 그대로 유지한다.
- `.gitattributes`, Unreal Asset, Git 이력과 원격은 변경하지 않았다. 먼저 대표 Map별 Dependency Closure와 Demo/중복/Source 후보를 감사하고 Core/선택형 Asset Depot를 분리한다. 선택 Clone은 LFS Pointer를 Content에 남겨 Editor 오류를 만들지 않도록 별도 Clone에서 Sparse Checkout과 `GIT_LFS_SKIP_SMUDGE`, 경로별 LFS Fetch를 함께 검증한다.
- 원격 LFS Object는 현재 Branch에서 파일을 지워도 GitHub 저장 할당량에 남는다. 원격 저장량 초기화가 필요하면 Curated 새 저장소 또는 백업 후 재생성·Support 협의를 팀이 별도로 결정하며 자동 실행하지 않는다.
- 상세 수치와 실행 순서는 [`DRONE_GIT_LFS_CAPACITY_PLAN.md`](../git/DRONE_GIT_LFS_CAPACITY_PLAN.md)에 기록했다. 후속 카드는 `GIT-LFS-CAP-01`이다.
- GitHub 공식 2026-09-15 단가와 Free/Pro 각 10GiB 포함량으로 비용을 추정했다. 원격 Associated Storage를 로컬 고유 Object 29.62GiB로 가정하면 저장 약 `$1.37/월`, 현재 전체 Clone 1회가 있는 달 약 `$2.92`, 2회가 있는 달 약 `$5.34`다. `$5`는 두 달 선불 잔액이 아니라 월 Budget으로 운영하고 실제 Billing 값을 최종 기준으로 삼는다.

## 2026-09-15 — 유인 MG 교대 안정화·Smart Object 팀 가이드·최소 Skill 도입

- AI 시험 맵에는 기관총 계열 Actor가 3개 있지만 NPC가 Claim하는 대상은 Smart Object Definition이 있는 `BP_SO_MGTurret` 1개뿐임을 테스트 계약에 반영했다. `BP_AutoTurret_Vehicle`과 `BP_AutoTurret_Emplaced`는 차량형/설치형 무인 자동포탑이며 유인 MG 수량·피해량·교대 판정에서 제외한다.
- 유인 MG 사수 사망 시 생존 가능한 적이 즉시 한 번만 이벤트를 받고 끝나던 경로를 0.75초 간격·15초 창 재할당 재시도로 보강했다. 사망·UnPossess·Drone Lost/Destroyed·MG 점유 성공 시 재시도를 정리하며 공개 런타임 API는 바꾸지 않았다.
- `Move To Reserved MG Turret` StateTree Task에 진행 거리 감시, 2초 정체 판정, 1회 재경로, 250cm Greybox 조작 위치 Snap 반경을 추가했다. 이동 상태가 `Moving`이어도 반경 안이면 먼저 정확한 Operator Anchor/Rotation으로 정렬해 점유를 완료한다. 최종 Mesh·Collision 적용 시 Snap 반경은 StateTree Details에서 줄인다.
- 테스트는 Rifle 10, Shotgun Pellet 8, 유인 MG 8의 기본 피해 계약을 먼저 검증한 뒤 이 PIE 안에서만 피해를 0으로 내려 Drone 조기 사망이 상태 검증을 가리지 않게 했다. Cover는 Nav 실패 시 제자리 `DroneDetected` 사격 Fallback도 정상 계약으로 인정한다. 게임/BP 기본 피해값은 바꾸지 않았다.
- `DroneEditor Win64 Development` Build가 성공했다. `Drone.AI.NPCPerceptionSearchPIE`는 단독 새 PIE 3회 연속 성공했고, 후속 `Drone.AI.NPC` 묶음에서도 해당 항목이 성공했다. 같은 묶음의 종료 코드 255는 별개 `NPCBaseRoutinesPIE`에서 느린 Headless 실행 중 적 한 명이 35초 안에 두 번째 순찰을 끝내지 못한 간헐 실패이며 MG 실패로 기록하지 않는다.
- 팀 공유용 [`DRONE_SMART_OBJECT_ROUTE_EDITING_GUIDE.md`](../ai/DRONE_SMART_OBJECT_ROUTE_EDITING_GUIDE.md)를 추가했다. 현재 동선은 스플라인/번호 고정 순서가 아니라 태그가 맞는 최근접 빈 Slot 선택임을 명시하고, 맵 경계, BP 경로, 지점 이동·회전·복제, Cyan 방향, NavMesh, Offset/StateTree 조정, 검증과 문제 해결 절차를 정리했다.
- 외부 참고 저장소는 Project Plugin/Hook/Library로 추가하지 않았다. 개인 Codex 환경에는 반복되는 원인 진단과 테스트 우선 작업에 직접 필요한 Matt Pocock Skills의 `diagnosing-bugs`, `tdd`만 설치했으며 다음 Codex 작업부터 사용 가능하다. Ponytail/ECC/Archify/fmt는 현재 Unreal 기본 도구와 문서 체계에 비해 중복·도입 부담이 커 보류한다.
- 팀원 Production `/Game/Drone/Maps/Lvl_DroneTraining`은 Git 변경 0으로 유지했다. Editor와 명령줄 검사 프로세스는 종료 상태이며 Commit·Push하지 않았다.
- 최종 경량 맵 재검증 `Resume_TutorialSystemsTestMap_Final_20260915_113347.log`에서 `Drone.Tutorial.TutorialSystemsTestMap` 1/1 Success·Exit 0을 확인했다. Unreal/문서 `git diff --check`와 Unreal `git lfs fsck`도 통과했으며 출력된 LF→CRLF 문구는 작업 트리 줄바꿈 안내이지 오류가 아니다.

## 2026-09-15 — 추천자료 장기 계획과 깨지는 World Text 정리

- PBRT, OSTEP, Crafting Interpreters, Game Programming Patterns, Computer Networking 9판 강좌, Speech and Language Processing 3판 Draft, Deep Learning, Immersive Linear Algebra의 공식 공개 페이지와 목차를 확인했다.
- [`CS_GAMEDEV_READING_PLAN.md`](../learning/CS_GAMEDEV_READING_PLAN.md)를 추가했다. 현재 Drone 작업에 가까운 `Game Programming Patterns + Immersive Linear Algebra`부터 시작하고 OS·Interpreter·그래픽스·네트워크·AI/NLP로 확장하는 장기 순서, 주 2시간/바쁜 주 25분 운영, 30분 세션 기록, 첫 4주 실행표를 포함한다. 비공식 PDF 다운로드와 원문 파일의 Git Commit은 권장하지 않는다.
- TestMap 역할 표적 위의 긴 한글 `TextRender`가 깨진다는 사용자 화면 피드백을 재현하는 검사를 먼저 추가했다. 수정 전 저장 TestMap에서 Recon/Impact/Payload 3개와 활성 Carryable 1개의 World Text가 모두 Visible이라 전용 테스트가 `3`과 `1`로 실패했다.
- 역할 표적은 `bShowInstructionText`, Carryable은 `bShowPickupLabel`을 기본 `false`로 추가하고 실제 Refresh/활성화/재투하 뒤에도 이 값을 적용했다. BP에서 명시적으로 켤 수는 있지만 문구는 `SCAN`·`IMPACT`·`DROP`·`PICKUP`으로 짧게 바꿨다. Mission HUD의 한글 조작 안내와 표적 기능 판정은 변경하지 않았다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build가 성공했고 동일 `Drone.Tutorial.TutorialSystemsTestMap` 검사는 visible 0+0, 1/1 Success, Exit 0으로 전환됐다. Production `Lvl_DroneTraining`은 변경하지 않았고 Commit·Push하지 않았다.

## 2026-09-15 — Markdown 문서 구조 정리

- 루트 문서가 모두 장문이고 `STATUS`·`WORKBOARD`·`CONTEXT`·세부 계획에 같은 상태가 반복돼 현재와 과거를 구분하기 어려운 문제를 정리했다.
- 기존 루트 원문 4개는 삭제하지 않고 `docs/history/snapshots/2026-09-15`에 보존했다. 새 루트 `README.md`는 시작점, `STATUS.md`는 현재 사실, `WORKBOARD.md`는 지금/다음 작업, `CONTEXT.md`는 변경 금지 경계만 담당한다.
- 상세 문서를 `planning`, `tutorial`, `ai`, `gameplay`, `assets`, `git`, `learning`, `reference`, `history`로 분류하고 [`docs/README.md`](../README.md)를 단일 안내 페이지로 추가했다.
- 이동된 문서의 상대 링크를 새 위치에 맞게 일괄 보정했다. 전체 Markdown 51개를 검사한 결과 존재하지 않는 로컬 `.md` 링크는 0개다.
- Unreal 저장소와 Asset은 변경하지 않았다. 문서 이동·요약·링크 수정만 문서 저장소의 로컬 변경으로 남기며 Commit과 Push는 사용자가 처리한다.
- 이후 진행 보고는 새 Markdown 파일을 늘리지 않고 루트 `STATUS.md`, `WORKBOARD.md`와 이 Worklog에 갱신한다. 완료된 일회성 보고서만 `history`로 옮긴다.

## 2026-09-15 — 이 PC 최신 빌드·Mission 목표 Rule Vertical Slice 준비

- 원격 재조회 때 Unreal `8b9b2a8`, 문서 `3e89e43`의 `main=origin/main`을 확인했고 두 저장소에 Stash는 없었다. 이후 작업은 로컬 수정으로만 남기고 Commit·Push하지 않았다.
- 첫 비파괴 TestMap Validate는 `RoleTest_PayloadTarget`이 없다는 메시지로 실패했다. 로그에는 역할 표적 Blueprint가 `/Script/Drone` C++ 부모를 못 읽는 경고가 있었고, 로컬 `UnrealEditor-Drone.dll`은 9월 8일 빌드라 최신 Source보다 오래됐다. 맵을 재구성하지 않고 최신 `DroneEditor`로 재빌드한 뒤 같은 Validate가 `rings=5/targets=3/carryable=1`, Map Check 오류·경고 0으로 성공했다.
- `FDroneMissionObjectiveRule`에 목표 ID·설명·사건 종류·필요 수량·제한 시간·Actor Tag 대상 ID를 추가했다. 새 Rule 배열이 비어 있으면 기존 `InitialObjectives` 문구형 1회 목표를 사용하므로 레거시 Data Asset을 깨지 않는다. ID 중복·0 수량·음수/비정상 시간 값을 거부한다.
- Director는 현재 Rule과 일치하는 Scan 완료, 의도된 Payload 적중, 맵 시작 시점 Health 대상 사망, Training Lap, 명시적 Return Event만 진행한다. 같은 Actor는 목표당 한 번만 세고, 목표별 제한 시간은 Tick 대신 TimerManager로 만료 시 Failure를 보고하며 전환·종료에 정리한다. 목표 Event·TargetId·수량·제한값이 Snapshot으로 HUD에 전달된다.
- Blueprint 배치형 `DroneMissionReturnZone` Box Trigger를 추가했다. 플레이어가 실제 출격한 Drone의 Overlap만 Director에 Return Event로 보고한다. 최종 기지 위치·크기는 미정이므로 Production 맵과 TestMap 어디에도 자동 배치하지 않았다.
- `ConfigureDroneTutorialMissionObjectiveRule.py`는 저장 `DA_Mission_Tutorial_Training`의 Mission ID와 기존 목표가 정확히 하나인지 확인한 뒤 같은 문구를 `Objective.TrainingLap` Rule로 이행했다. `DRONE_MISSION_RULE|SAVED`를 확인했고 해당 `.uasset`은 Git LFS 대상이다. 팀원 `/Game/Drone/Maps/Lvl_DroneTraining` `.umap`은 변경하지 않았다.
- MSVC 14.51.36256 `DroneEditor Win64 Development` 두 번 모두 Build 성공. 새 `Drone.Mission.ObjectiveRules`는 잘못된 Event/Tag, Actor 중복, 두 Scan→Delivery→Return→Success, 종료 후 Event 거부와 귀환 Zone 기본 Box 계약을 검증한다. 최종 회귀에서 이 테스트와 `Drone.Flow.Contract`, `MissionEntryContract`, `TrainingGateSequence`, `TutorialSystemsTestMap`이 5/5 Success·Exit 0이었다.
- 실제 역할 기능의 연쇄 PIE, 귀환 Zone의 맵 배치·Overlap, 제한 시간 만료 화면과 TestMap/AI 수동 화면 검증은 미완료다. 새 Data Asset/맵의 최종 목표 규칙을 임의로 확정하지 않는다. 설정과 문제 확인법은 [`DRONE_MISSION_OBJECTIVE_RULE_GUIDE.md`](../gameplay/DRONE_MISSION_OBJECTIVE_RULE_GUIDE.md)에 기록했다.
- 최종 로컬 Unreal·문서 `git diff --check`는 모두 종료 코드 0이다. 표출된 LF→CRLF 메시지는 줄바꿈 안내다. Unreal·문서 저장소의 HEAD는 각 `origin/main`과 같지만 작업 트리는 새 Source/Data Asset/가이드가 미커밋으로 남았다.

## 2026-09-16 — 재밍 신호 Greybox·Mission 사건 연결

- 로컬 기획의 첫 Story Mission은 구급품 전달·정찰·재밍 회피·적 기지 침투 후보로 확인했다. Figma 링크는 현재 읽기 연결이 없어서 실제 화면/최종 목표는 확인하지 못했다. Figma 연결 옵션을 제안했지만 설치·연결하거나 내용을 수정하지 않았다. 후보를 확정 Mission Data Asset으로 만들지 않았다.
- `UDroneSignalComponent`와 `ADroneJammingVolume`을 추가했다. Overlap 기반 여러 방해 Source 중 최대 강도를 써 `None/Weak/Moderate/Strong` 신호 단계와 HUD 경고를 계산한다. Tick·무작위 입력 손실을 사용하지 않고 강한 단계에서 기본 비행 튜닝의 최대 속도/가속도에 0.70 Greybox 배율을 적용해 Zone 이탈·해제 뒤 복원한다.
- Flight HUD에 신호율·단계 경고와 Blueprint `VideoNoiseIntensity` Snapshot Event를 추가했다. 실제 영상 Noise Material이나 목표 정보 일부 숨김은 아직 구현하지 않았다. `Jamming Exited`·`Jammer Disabled` Mission Rule 사건은 현재 목표/Actor Tag가 맞을 때만 진행한다.
- 초기 재밍 회귀에서는 `Drone.Signal.StageContract`는 성공했으나 `Drone.Mission.ObjectiveRules`의 Jammer 해제 자동 진입이 실패했다. 사건을 Director에 직접 보고하면 통과하고 Blueprint Delegate 구독만 Editor World 자동화에서 호출되지 않는 것을 확인해, 게임 규칙 연결은 Zone의 C++ Native Event로 변경하고 BP Event는 연출용으로 유지했다. 진단용 수동 보고와 로그는 최종 코드에서 제거했다.
- 최신 `DroneEditor Win64 Development` Build 성공, `Drone.Signal.StageContract`, `Drone.Mission.ObjectiveRules`, `Drone.UI.FlightHUDTelemetryBinding` 신호 경고/복원, Flow 2개, Tutorial 2개 묶음 7/7 `Success`·Exit 0. 비활성 Zone의 BeginPlay 사전 Overlap에서도 신호 Source를 제거하도록 방어했다. 실제 맵에 귀환/재밍 Zone을 배치한 PIE, Drone 비행 체감과 HUD 영상 표현은 아직 수동 확인 전이다. 팀원 Training과 TestMap `.umap`은 수정하지 않았고 Commit·Push도 하지 않았다.
- 팀원 배치 절차·기본 수치·실제/미구현 경계는 [`DRONE_JAMMING_GREYBOX_GUIDE.md`](../gameplay/DRONE_JAMMING_GREYBOX_GUIDE.md)에 기록했다.

## 2026-09-16 — Figma 4개 Mission 대조·양쪽 Story 분기·광섬유 면역

- 새로 연결된 Figma `Project:Droner`의 node `1:3`, `46:3`, `49:2`, `53:10`, `273:73`, `282:105`, `283:136`을 읽기 전용으로 확인했다. 원본은 수정하지 않았다. `골든 타임`, `인터셉트`, `베일 브레이커`, `엔드게임`과 Drop/FPV/광섬유/UGV/장거리 타격 역할, Tutorial 요구를 현재 코드와 대조했다.
- 같은 Figma 파일에서 차량은 미끼이고 오마르는 Mission 3에서 처리된다는 전체 설명과, Mission 2 차량에 탑승했다고 전제하고 Mission 3 시작 전에 이미 처리됐다는 개별 화면 문구가 충돌했다. 사용자 요청대로 한쪽을 삭제하지 않고 둘 다 데이터로 설정 가능하게 했다.
- Mission Definition에 성공 시 추가/제거할 Story Fact, Objective Rule에 `Always/FactPresent/FactAbsent` 조건과 Fact ID를 추가했다. Game Flow Snapshot은 Fact를 GameInstance 동안 보존하며 성공 전환과 함께 한 번에 적용한다. Mission Director는 현재 Fact가 맞는 목표만 실행 목록에 포함한다.
- `Story.TargetStillAtLarge` 분기는 Mission 3의 표적 처리 목표를 포함하고, `Story.TargetEliminated` 분기는 그 목표를 제외하고 이미 처리된 후속 목표를 포함하는 경로를 자동화에서 각각 실행했다. 동일 Fact 추가/제거, 빈/중복 ID와 잘못된 조건은 Definition 검증 경계로 관리한다. 실제 Mission 2/3 Data Asset 기본안은 사용자 결정 전 만들지 않았다.
- Figma의 광섬유 Drone `재밍에 면역` 요구를 기존 `EDroneGameplayCapability::JammingImmunity`에 연결했다. Definition의 **Implemented** 목록에 들어간 기체만 활성 재밍 Source를 무시하고, 면역 해제 시 아직 겹친 Source의 가장 강한 단계가 즉시 돌아온다. 광섬유 Drone Definition/Pawn이 없으므로 기존 세 기체에는 면역을 부여하지 않았다.
- `DroneEditor Win64 Development` 전체 Build 성공. `Drone.Mission.ObjectiveRules`, `Drone.Prototype.FlightProfiles`, `Drone.Signal.StageContract`, UI/Flow/Tutorial을 포함한 회귀 8/8 `Success`·Exit 0. 팀원 Training/TestMap `.umap`, Figma 원본, Git Commit/Push는 변경하지 않았다.
- Figma 요구와 구현/미구현·충돌·순서를 [`DRONE_FIGMA_MISSION_IMPLEMENTATION_MATRIX.md`](../planning/DRONE_FIGMA_MISSION_IMPLEMENTATION_MATRIX.md)에 정리했다. 추가 Figma 상세 읽기는 연결에서 재인증을 요구해 중단했고, 이미 확인된 node 내용만 기록했다.

## 2026-09-16 — AI 시험 맵 이동·Mission/Signal 통합 시험 맵

- Unreal AssetTools로 `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`를 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`로 이동했다. 이동 직후 같은 Python 프로세스에서 World를 다시 열어 Python 참조가 GC를 막는 실패가 한 번 발생했지만 실제 AssetTools 이동은 저장됐다. 이동 도구를 에셋 레지스트리 검증까지만 담당하도록 고쳐 재실행했고 정상 종료를 확인했다.
- C++ 자동화와 자동포탑 배치 도구의 고정 맵 경로를 새 위치로 바꿨다. Production `Lvl_DroneTraining`, 용도 미확인 `test1`·`test2`, 나머지 이동 후보 맵은 변경하지 않았다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneMissionSystemsTest`를 새로 만들었다. 충돌 없는 위치 표식, 35%/80% 겹침 Jammer, `Test.Mission.ReturnZone` Tag의 Return Box, Recon/Impact/Payload 표적 각 1개, Carryable 1개와 Prototype GameMode를 배치했다.
- 생성 도구는 기존 맵에서 Validate-only이고 명시적 `Rebuild` 때 `DroneMissionSystemsTest.Owned` Actor 14개만 다시 만든다. 저장 Map Check는 `0 errors / 0 warnings`다.
- `DroneEditor Win64 Development` 빌드 성공. 이동된 AI 맵의 `NPCGreyboxAssets`, `NPCGreyboxPIE`, `NPCPerceptionSearchPIE`, 새 `MissionSystemsTestMap`, `ObjectiveRules`, `Signal.StageContract` 최종 회귀는 6/6 Success·경고 0이다. 자동포탑 배치 도구의 새 경로 Validate-only도 설치형/차량형 각 1기, 차량 Attach, 4점 Suspension, 노면 5개 계약으로 통과했다.
- 새 맵을 바로 Play하면 비행·Signal HUD·역할 기능은 볼 수 있지만 Prototype GameMode이므로 Return/Jammer Mission 목표 완료까지는 실행하지 않는다. 다음은 Test Mission DA와 개발용 진입 경로를 추가해 실제 Mission Director 연쇄를 확인하는 작업이다.
- 사용법과 다음 경계는 [`DRONE_TEST_MAP_GUIDE.md`](../gameplay/DRONE_TEST_MAP_GUIDE.md)에 정리했다. Commit·Push는 하지 않았다.

## 2026-09-16 — 추가 Shotgun NPC·독립 사격 시험 맵

- 기존 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`에 NPC를 더 넣으면 순찰·MG/Cover 점유 경쟁과 기존 4-NPC 자동화 시간이 바뀌므로, 기존 Rifle 1·Shotgun 1·Friendly 2는 그대로 유지했다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneShotgunSystemsTest`를 새로 만들고 `BP_NPC_Hostile_Shotgun` 1명을 추가 배치했다. 약 9m 정면 PlayerStart, 5/10/15m 표식, 독립 Navigation Floor/Bounds와 옆 LOS 차단벽을 두었다. Production `Lvl_DroneTraining`은 열거나 저장하지 않았다.
- 역할 BP가 실제 Gun Mesh를 별도 Component로 쓰면서 부모의 교체용 `WeaponVisualComponent`를 비워 두어 Map Check 경고가 났다. 역할 BP 원본 구조를 바꾸지 않고 이 시험 맵 인스턴스에서만 보이지 않는 Engine Mesh를 채워 실제 Gun 외형을 유지했고, 최종 Map Check는 `0 errors / 0 warnings`다.
- 기본 Projectile Shotgun에서도 8개 Pellet의 예상 비행선을 Cyan으로 표시한다. 실제 충돌·피해는 이동 Projectile이 담당한다. Blueprint에서 표시를 켜고 끄며 직전 Pellet 끝점 배열을 읽는 API도 추가했다.
- `Drone.AI.ShotgunSystemsTestMap`과 `Drone.AI.ShotgunSystemsTestMapPIE`는 전용 NPC/Profile/GameMode/Nav 배치, 실제 감지, 8 Projectile 생성, Shell 소모, 6° 원뿔과 독립 방향을 검증했고 최종 `2/2 Success`, 경고 0이다. `WeaponContract`, `ShotgunTrace`, `ProjectileBallistics`까지 묶은 전체 샷건 계약은 `5/5 Success`, 실패 0이었다. `ShotgunTrace`는 탄창 비움과 명시적 재장전도 확인한다.
- 기존 Smart Object 맵의 Rifle 1·Shotgun 1·Friendly 2와 Asset 계약은 별도 `Drone.AI.NPCGreyboxAssets` 재실행 `1/1 Success`, 경고 0으로 영향 없음을 확인했다.
- 빌드와 생성/검증 도구 사용법은 [`DRONE_TEST_MAP_GUIDE.md`](../gameplay/DRONE_TEST_MAP_GUIDE.md)에 갱신했다. 기본값은 기능 검증용 Greybox이며 최종 밸런스가 아니다. Commit·Push는 하지 않았다.

## 2026-09-16 — FPV Rate/Acro 조작과 바람·비 기획

- 기존 `Assisted Easy`와 제한 자세 `Manual Realistic Greybox`를 유지한 채 세 번째 `Acro Rate Realistic Greybox`를 추가했다. 오른쪽 Stick Pitch/Roll과 Yaw 입력을 Betaflight Actual Rates 의미의 Body 각속도로 변환하며, Stick 중앙에서 자동 수평 복귀하지 않고 Root Local Rotation을 누적해 Roll/Loop가 가능하다.
- FPV Definition만 갱신하는 안전한 Python 도구를 추가해 다른 Mission Data Asset을 다시 저장하지 않았다. FPV 기본값은 Rate/Acro+Agile이고 공개 민간 FPV 참고선으로 Runtime 수평 27m/s, World Z 9m/s, Pitch/Roll 650°/s, Yaw 400°/s를 적용했다. 특정 군용 기체의 성능이나 완전한 모터/PID 물리로 표현하지 않는다.
- `FDroneAcroRateSettings`를 Flight Profile에 노출해 중앙 감도, 축별 최대 Rate, Expo, 수직 속도를 Data Asset/Blueprint에서 조정할 수 있게 했다. 조작 버튼은 쉬운 조작→제한 자세→Rate/Acro 순환으로 갱신했다.
- MSVC 14.51.36256 `DroneEditor Win64 Development` Build 성공. `Drone.Prototype.FlightProfiles`, 3회 PIE 입력·Binding 수명주기의 `Drone.Prototype.PIEInputLifecycle`, `Drone.Flow.MissionEntryContract`, `Drone.Flow.MissionEntryPIE`, `Drone.Prototype.RoleAbilities` 모두 Success·Exit 0이다.
- 바람 지속풍/돌풍/난류/고도 반응과 비 강도/시야/젖음/Splash/실내 감쇠 변수, Weather Subsystem/Volume 책임, Camera-follow GPU Niagara·Effect Type Scalability·저빈도 실내 Trace·MPC Wetness·비입자 Collision 제한을 [`DRONE_WEATHER_WIND_RAIN_PLAN.md`](../gameplay/DRONE_WEATHER_WIND_RAIN_PLAN.md)에 정리했다. 기상 Runtime과 Niagara Asset은 아직 구현하지 않았다.
- Production `Lvl_DroneTraining`과 Figma 원본은 수정하지 않았고 Commit·Push하지 않았다.

## 2026-09-16 — 기상 데이터 계약·지속풍/돌풍 Vertical Slice

- `UDroneWeatherProfile`, `FDroneWeatherSnapshot`, `UDroneWeatherWorldSubsystem`을 추가했다. Profile 기본 10Hz Timer와 고정 Seed로 지속풍·돌풍·풍향 흔들림·수직 기류를 계산하고, 0~60초 Profile 전환을 하나의 World Snapshot으로 전달한다.
- 배치형 `ADroneWeatherController`가 BeginPlay에 Profile을 적용한다. World 기상과 Level 연결을 분리해 Mission이나 TestMap이 같은 C++ 계약을 재사용한다.
- 모든 `ADronePrototypePawn`에 `UDroneWeatherResponseComponent`를 기본 부착했다. 쉬운 조작 65%, 제한 자세 25%, Rate/Acro 0% 기본 보정 뒤 Sweep 위치 Drift를 적용하고 바람이 없으면 Component Tick을 끈다. 현재 `UFloatingPawnMovement` 위 Greybox이며 모터·PID·공기역학 최종 구현이 아니다.
- `/Game/Drone/Data/Weather`에 `DA_Weather_Clear`, `DA_Weather_LightWind`, `DA_Weather_RainStorm_Greybox`를 만들었다. 폭우 Profile의 최대 수평풍 약 10.7m/s는 공개 민간 FPV 참고선이고 최종 내풍 한계가 아니다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneWeatherSystemsTest`를 새로 만들었다. `LightWind` Controller 1개, 35° 풍향 화살표, 바닥·PlayerStart·조명과 Prototype GameMode만 둔 독립 맵이며 Map Check `0 errors / 0 warnings`다. Production Training 맵은 열거나 저장하지 않았다.
- `DroneEditor Win64 Development` Build가 성공했다. `Drone.Weather.ProfileAndWindContract`, `Drone.Weather.ProfileAssets`, `Drone.Weather.SystemsTestMap`은 3/3 Success·Exit 0이고 `Drone.Prototype.PawnDefaults` 회귀도 Success·Exit 0이다.
- 비 강도·생성량·시야·화면 물방울·젖음·Splash·실내 감쇠·Audio 값은 Snapshot에 포함됐지만 Niagara/MPC/Audio 표현은 아직 없다. 비가 체력·신호·Mission 규칙을 자동으로 바꾸지 않는다. 다음 구현은 Camera-follow GPU Rain과 성능 측정이다.
- Commit·Push는 하지 않았다.

## 2026-09-16 — D 드라이브 작업 PC 원격 재동기화

- `D:\JGY\project\drone`과 `D:\JGY\project\md`에서 `git fetch origin --prune`을 다시 실행해 원격 조회가 정상 동작함을 확인했다.
- Unreal은 `main = origin/main = 962ff02`이고 Commit 제목은 `기상 시스템과 기능별 테스트맵 구현`이다. Mission Rule·재밍·Story Fact·FPV Rate/Acro·기상 Runtime, Weather/Mission/Shotgun TestMap과 AI 맵 이동이 모두 이 Push 기준선에 포함됐다.
- 문서는 `main = origin/main = 3c28611`이고 위 구현에 대응하는 상태·가이드·Worklog가 Push 기준선에 포함됐다.
- 확인 시작 시 두 저장소 모두 Clean, Stash 없음, `HEAD...origin/main` 차이 `0/0`이었다. 이전 문서의 C 드라이브 경로와 `로컬 미커밋` Git 표기는 다른 PC의 Push 전 기록이므로 현재 D 드라이브 경로와 최신 Commit으로 정정했다.
- 이번 최신화는 `STATUS.md`, `WORKBOARD.md`, `CONTEXT.md`와 이 Worklog만 변경한다. Unreal 코드·자산·Map은 수정하지 않았으며 Commit과 Push는 사용자가 처리한다.

## 2026-09-16 — Shotgun Pellet 가시화·피해 조정과 Weather TestMap 판독성 개선

- Shotgun 사격장에서 한 탄두만 보인다는 보고를 기존 PIE 계측과 대조했다. 실제 발사 로직은 한 Volley마다 8개 이동 Projectile을 6° 원뿔 안의 독립 방향으로 생성하고 있었고, 전용 PIE도 8발 생성을 통과했다. 원인은 모든 발이 같은 총구에서 같은 프레임에 큰 공용 Sphere로 시작하고 별도 Tracer가 없어 겹쳐 보이는 표현 문제였다.
- 먼저 회귀 계약을 `Pellet당 3 피해`, `작은 비드`, `짧은 Tracer`, `전용 Projectile BP`로 추가했다. 변경 전 `8 피해`, Tracer 없음, 큰 기본 Scale과 Weather Visualizer 0개로 의도한 실패를 확인했다.
- `ADroneNPCProjectile`에 Blueprint 교체 가능한 `ProjectileVisual`과 `ProjectileTrailVisual` Getter를 추가하고 기본 Sphere Scale을 `0.025`, 뒤쪽 Cube Tracer를 `0.14 x 0.0075 x 0.0075`로 설정했다. `/Game/Drone/AI/Blueprints/Projectiles/BP_ShotgunPelletProjectile`을 만들고 `BP_NPC_Hostile_Shotgun`의 Projectile Class에 연결했다. Shotgun은 `8 Pellet`, `6°`, `3500cm/s`를 유지하고 Pellet당 피해를 `8→3`으로 낮춰 전탄 최대 24가 됐다.
- `ADroneWeatherDebugVisualizer`와 `/Game/Drone/Weather/Blueprints/BP_DroneWeatherDebugVisualizer`를 추가했다. Weather TestMap에서 24개 Sphere Bead가 현재 Snapshot 풍향/풍속으로 이동하며 Profile·풍속·풍향·모드를 화면에 표시한다. `1/2/3`과 NumPad `1/2/3`은 Easy 65%/Manual 25%/Rate-Acro 0% 보정을 즉시 비교한다. Bead 수·범위·Scale·재생 배율·Mesh·Readout/Hotkey 사용은 BP/배치 인스턴스에서 조정한다.
- Shotgun/Weather 맵을 도구 소유 Actor만 다시 생성했고 두 Map Check는 `0 errors / 0 warnings`다. MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공, Shotgun 전용 Asset/PIE 2/2, `NPCGreyboxAssets`, `WeaponContract`, `ProjectileBallistics`, `ShotgunTrace`, 강화한 `Drone.Weather.SystemsTestMap`이 모두 성공했다. `git diff --check`와 `git lfs fsck`도 통과했다.
- 화면에서 Pellet 8개 분리 정도와 Tracer 길이·밝기, 한 Volley 최대 24 피해 체감, Weather Bead 가독성과 1/2/3 Drift 차이는 수동 확인이 남았다. RainStorm Profile은 값만 전달하며 Niagara/MPC/Audio 비 표현은 아직 없다. Commit·Push는 하지 않았다.

## 2026-09-16 — 실제 Shotgun 탄 시인성 보강·개인화기 고개 흔들림 안정화

- 작은 회색 Pellet/Tracer가 화면에서 너무 안 보인다는 재확인에 따라 TestMap 선이 아니라 실제 `/Game/Drone/AI/Blueprints/Projectiles/BP_ShotgunPelletProjectile`을 수정했다. `/Game/Drone/AI/Materials/M_ShotgunPelletGlow` 주황 Unlit Emissive 재질을 만들고 비드 Scale을 `0.04`, Tracer를 `0.20 x 0.0125 x 0.0125`로 올려 실제 샷건 NPC가 배치된 모든 맵에 적용했다.
- 샷건 NPC가 표적 발견 뒤 정면에서도 몸/고개를 좌우 왕복한다는 보고를 실제 Controller Tick 경로의 PIE 회귀로 고정했다. NPC 9m 전방 표적을 좌우 30cm, 약 ±1.9°로 번갈아 이동하는 테스트는 수정 전 몸체 회전 한도를 넘어 실패했다.
- `ADroneNPCAIController`의 개인화기 몸 Yaw와 Bone Gaze에 공통 `PersonalWeaponFacingDeadZoneDegrees = 3°`를 추가했다. 데드존 안에서는 정면 오차로 허용하고, 밖에서는 기존 초당 180° 몸 회전과 상체/목/머리 보간을 유지한다. 데드존과 몸 회전속도는 `FDroneNPCProfile`로 옮겨 Hostile Rifle/Shotgun Blueprint `NPCProfileComponent > Profile > NPC|Gaze`에서 역할별 조정할 수 있다.
- 같은 PIE 회귀가 수정 뒤 성공했고, MSVC 14.51.36257 `DroneEditor Win64 Development` Build와 Shotgun Asset/PIE `2/2`가 성공했다. 실제 Pellet BP의 발광 Material·크기·Tracer와 1.9° 정면 안정화가 자동 계약에 포함됐다.
- 영향 확인용 기존 `Drone.AI.NPCPerceptionSearchPIE` 단독 실행은 이번 Shotgun/Gaze 검증이 아니라 사수 사망 뒤 MG 재점유 제한시간에서 실패했다. 로그상 사망 NPC 정리는 성공했지만 생존 Shotgun NPC가 개인화기 상태에 머물러 MG를 다시 Claim하지 않았다. 최신 전체 AI 통과로 기록하지 않고 별도 재현·진단 항목으로 남겼다.
- Rate/Acro 현재 키를 문서화했다. Gamepad Mode 2는 왼쪽 Y Throttle·왼쪽 X Yaw·오른쪽 Y Pitch·오른쪽 X Roll이다. 키보드는 W/S Throttle·A/D Yaw·Q/E Roll이고 Body Pitch 전용 키가 아직 없어 완전한 Loop 시험은 Gamepad/RC Controller가 필요하다. Commit·Push는 하지 않았다.

## 2026-09-16 — Shotgun 실제 분리·공용 탄 시인성·시선 Hysteresis·UI 임시 프로토타입

- 화면에는 Cyan 예상선 8개가 보이지만 실제 Pellet이 하나처럼 보인다는 보고를 생성 카운터만 확인하던 기존 테스트와 분리했다. 첫 Volley 후 80ms 시점의 살아 있는 Shotgun Projectile 수를 세는 회귀를 추가했고 수정 전 `6개 미만`으로 실패해 화면 문제가 실제 수명 문제임을 확인했다.
- 같은 총구·같은 프레임에서 생성된 동일 소유자의 Pellet들이 `WorldDynamic`으로 서로 Block한 것이 원인이었다. Spawn 초기화에서 같은 발사자 Projectile끼리 양방향 Sweep Ignore를 등록해 상호 제거를 막았다. 테스트는 80ms 뒤 8개 전부 개별 비행으로 Green이다.
- 실제 Hostile Shotgun BP와 전용 TestMap 인스턴스를 `8 Pellet / 원뿔 반각 12° / Pellet당 3 피해 / Cyan Debug 기본 Off`로 갱신했다. 전용 발광 비드/Tracer는 유지하고 안전한 적용·검증 도구 `ConfigureDroneShotgunCombatDefaults.py`를 추가했다.
- Rifle·유인 MG·무인 포탑이 공유하는 Native Projectile의 기본 탄두를 `0.06`, Tracer를 `0.60 × 0.018`로 확대하고 Shotgun Glow Material을 공용 임시 발광 재질로 연결했다. Shotgun 전용 BP는 자체 작은 Scale을 계속 덮어쓴다.
- 개인화기 몸 회전은 단일 3° 경계 대신 `3° 정지 + 3° Hysteresis = 6° 시작`으로 바꿨다. Bone Gaze는 작은 잔여 오차를 보간하고 경계에서 0도로 Snap하지 않는다. 머리 Socket Yaw/Pitch 변동까지 실제 PIE에서 검사한다.
- 첨부 와이어프레임을 참고해 C++ fallback Front-end를 `작전 목록 / 선택 작전 / 작전 개요`, Drone Select를 `보유 기체 / 상세 / 조작 설정` 3열 임시 레이아웃으로 다시 구성했다. Flow·Mission/Drone Data Asset·Map 전환 책임은 바꾸지 않았다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `Drone.AI.ShotgunSystemsTestMap` Asset/PIE 2/2, `Drone.AI.ProjectileBallistics`, `Drone.Flow.FrontEndPIE`, `Drone.Flow.MissionEntryPIE`가 모두 Success다. Production `Lvl_DroneTraining`은 열거나 저장하지 않았으며 화면 체감과 16:9 잘림 여부는 사용자 수동 확인이 남았다. Commit·Push는 하지 않았다.

## 2026-09-16 — Acro 키보드/패드 축 분리와 바람 보간 후속 방향

- 고기동 FPV에서 W가 전진 Pitch를 만들지 못하고 W/S와 Space/Ctrl이 모두 Throttle 역할을 하던 증상을 재현했다. 원인은 Acro에서 공용 `IA_Move`를 왼쪽 Stick Throttle/Yaw로 재해석해 같은 Action을 쓰는 키보드까지 함께 바뀌고, 키보드 Body Pitch가 사라진 구조였다.
- 전용 Axis1D Action `AcroPitch/Roll/Yaw/Throttle` 네 개를 만들었다. 키보드는 `W/S Pitch`, `A/D Roll`, `Q/E Yaw`, `Space/Left Ctrl Throttle`, Gamepad는 오른쪽 Y Pitch·오른쪽 X Roll·왼쪽 X Yaw·왼쪽 Y Throttle의 Mode 2다. 쉬운/제한 자세 공용 Action과 Acro Action은 Pawn이 현재 모드별로 한쪽만 소비한다.
- 자산이 없는 상태에서 `Drone.Prototype.AcroInputContract`가 네 Action 누락으로 의도한 Red를 냈다. 구현 후 IMC 33 Mapping, 음수 키 Negate, FPV Integration BP Action 연결과 Pawn Binding을 검사해 Green으로 전환했다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build와 `Drone.Prototype` 8/8이 성공했다. Production Training Map은 열거나 저장하지 않았고 Commit·Push하지 않았다. 키보드/패드 실제 체감은 수동 확인이 남았다.
- 기상 코드를 대조한 결과 Gameplay Gust와 Drone Drift에는 이미 보간이 있으나 Debug Bead는 현재 풍향에 누적 이동거리 전체를 다시 곱해 방향 변화 때 튈 수 있다. 다음 `WTH-02B`는 돌풍 Attack/Release·풍향 최단각 보간, 표시 전용 순간 속도 적분, Bead/Arrow 방향·길이 보간을 테스트 우선으로 진행한다.

## 2026-09-16 — Acro 추력·중력 비행 v1과 WTH-02B 구현

- 기존 Rate/Acro는 Body 각속도로 Root만 회전하고 이동은 별도 `AddMovementInput`에 의존해 W Pitch로 기체를 숙여도 전진력이 생기지 않았다. `Drone.Prototype.FlightProfiles`에 `Nose-down Acro attitude creates forward thrust` 계약을 먼저 추가했고 기존 코드에서 의도대로 실패했다.
- `FDroneAcroRateSettings`에 `HoverThrottleNormalized`, `GravityAccelerationCentimetersPerSecondSquared`, `LinearDragPerSecond`, `BodyRateResponseTimeSeconds`를 추가했다. 모두 `DA_Drone_* > Flight Profile > Acro Rate Settings`와 Blueprint에서 조정 가능하다.
- Acro 스로틀은 `-1=무추력`, `0=수평 호버`, `+1=최대 추력`으로 변환한다. World Down 중력과 Body Up 추력을 합쳐 기체를 Pitch/Roll하면 추진 방향이 실제로 바뀌며, 속도 비례 지수 항력과 Rate 응답 지연을 적용한다. 기존 FloatingPawnMovement 자동 감속은 Acro에서 꺼 항력과 중복되지 않게 했다.
- FPV 저장 기본값은 호버 `0.50`, 중력 `980cm/s²`, 선형 항력 `0.12/s`, Body Rate 응답 `0.08s`다. 기존 27m/s 전체 속도와 World Z 9m/s 제한, 650°/s Pitch/Roll, 400°/s Yaw는 유지한다. 모터별 RPM·PID·공력·질량/관성 모델은 아니며 물리 체감 v1이다.
- Acro Throttle의 `Completed/Canceled` 입력 리셋을 추가하고 PIE Binding 수명주기 계약도 Triggered/Completed/Canceled 각 1개로 갱신했다. Editor Build 성공, 최종 `Drone.Prototype` 8/8 Success·실패 0이다.
- `FDroneWindSettings`에 돌풍 Attack/Release와 풍향 Response 시간을 추가했다. 세기·수직 돌풍은 Attack/Release 지수 응답, Yaw 편차는 최단각 응답을 사용한다. LightWind는 `0.8/1.8/1.0s`, RainStorm은 `0.45/1.2/0.65s`를 저장했다.
- Debug Visualizer의 스칼라 누적 거리 재투영을 제거하고 표시용 풍속을 매 Frame 보간한 뒤 Local 속도 벡터를 적분한다. 풍향 X→Y 전환 시 이전 X 이동을 유지하며, Bead는 풍향으로 회전하고 풍속에 따라 길이가 변한다. 응답 시간·기준 풍속·길이·단면은 BP/배치 인스턴스에서 조정한다.
- `Drone.Weather` 3/3 Success·실패 0, 방향 전환 궤적 보존과 Frame Step 독립 적분 자동화가 통과했다. Production `Lvl_DroneTraining`은 열거나 저장하지 않았고 Commit·Push하지 않았다. Acro 체감과 Weather 화면 무점프 확인은 사용자 수동 항목으로 남겼다.

## 2026-09-16 — Smart Object Greybox 차량 바퀴 회전축 교정

- `Lvl_NPCSmartObjectGreybox`의 차량 바퀴가 진행 방향으로 구르지 않고 옆으로 회전한다는 화면 보고를 저장 Asset과 대조했다. 차량 BP와 맵 인스턴스는 기본 Cylinder가 아니라 `/Game/MillitaryBase/Meshes/SM_SpikeStorm_Tire2_FR`을 네 바퀴에 사용하며, Mesh Local Bounds의 얇은 축은 Y였다. 기존 코드는 Cylinder 전용 Local Z축 회전을 고정해 실제 Tire Mesh 장착 회전과 맞지 않았다.
- 실제 저장 `BP_GroundConformingVehicle_Greybox`를 Spawn해 전진 한 프레임 뒤 각 바퀴 Rotation Delta 축을 검사하는 회귀를 추가했다. 수정 전 네 바퀴 모두 차량 좌우 차축 조건에 실패하는 Red를 확인했다.
- 바퀴 회전은 Mesh 원본축이 아니라 `VehicleCollision` 부모 공간 `+Y`에 적용하도록 바꿨다. 좌우별 `Roll 0°/180°` 장착 회전은 Base Rotation으로 보존하며, 방향 부호는 기존 `+1`을 유지한다. `Wheel Visual Spin Axis In Vehicle Space`를 Blueprint에 노출해 다른 차량 좌표계도 조정할 수 있게 했다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공, `Drone.Vehicle.GroundConformingSuspension`은 동일 회귀를 포함해 Success로 전환했다. 자동포탑/차량 읽기 전용 검증도 차량 1·바퀴 4·차량 포탑 Attach·노면 5·Map Check 0/0으로 통과했다.
- 전체 `Drone.AI.NPCGreyboxAssets`는 차량이 아니라 팀원이 교체한 `BP_NPC_Friendly_Base` Character Mesh가 오래된 역할 Mesh 기대값과 달라 실패했다. 이번 바퀴 수정과 분리해 기록하며 Friendly 자산을 되돌리지 않았다. 최종 바퀴 구름 방향은 Editor 화면 재확인이 남았다.
- 회전축 교정 후 실제 Tire가 도로 두께만큼 잠긴다는 화면 보고를 독립 평면 회귀로 추가했다. `SM_SpikeStorm_Tire2_FR`의 세로 반지름은 약 50cm지만 저장 차량 BP의 `Wheel Radius`는 Native Cylinder용 30cm여서 네 바퀴 모두 약 20cm가 지면 아래에 있었다.
- `Wheel Radius`의 Blueprint 범위를 `1~500cm`로 명시하고 현재 Tire BP 기본값을 52cm로 저장했다. BP 한 개만 갱신하는 `DRONE_VEHICLE_WHEEL_DEFAULTS_ONLY` 도구 모드를 추가해 팀원 NPC와 맵을 재저장하지 않았다. 수정 뒤 Tire Bounds·평면 접촉·회전축을 함께 검사하는 `GroundConformingSuspension`과 읽기 전용 차량/포탑 맵 Validate가 성공했다.

## 2026-09-17 — 적 AI 재검증 및 Weather TestMap 디버그 강우 프리뷰

- 문서 저장소 Markdown 57개를 목록화하고 최신 README/CONTEXT/STATUS/WORKBOARD, AI·Smart Object·MG·Gaze, 날씨/시험 맵 계획, Project Audit, 최신 Worklog 항목을 대조했다. 서로 충돌하는 과거 기준은 현재 Source와 최신 STATUS/WORKBOARD를 우선했다.
- 사용자 체감 적 NPC 떨림/애니메이션 중첩은 Headless 자동화만으로 화면 재현되지 않았다. `Drone.AI.NPCGreyboxAssets`, `NPCPerceptionSearchPIE`, `PersonalWeaponEngagementPolicy` 3/3과 Shotgun Asset/PIE 2/2는 통과했으나, AnimBP 포즈 중첩·실제 화면 떨림이 해결됐다는 뜻은 아니다. AI 소스와 Production 맵은 수정하지 않았고 수동 PIE 재현이 남아 있다.
- 기존 `ADroneWeatherDebugVisualizer`에 `7 Clear / 8 LightWind / 9 RainStorm` 진입점을 추가했다. 지정된 `Lvl_DroneWeatherSystemsTest`에서만 프로파일 Snapshot을 즉시 교체하며 다른 맵과 잘못된 인덱스는 거부한다. 기존 1/2/3 조작 모드 키는 유지했다.
- Rain Snapshot 강도×SpawnScale로 최대 80개 선분을 0.2초 간격으로 생성하는 DebugDraw 프리뷰를 전용 TestMap에만 연결했다. 비가 0이면 추가 Draw 호출을 멈추고 잔여 선분은 짧은 수명 뒤 사라진다. 파티클별 Trace·새 Niagara/Material/맵 저장은 없다. 이 프리뷰는 정식 Niagara 효과나 GPU 성능 측정이 아니다.
- UE 5.8.2 `DroneEditor Win64 Development` Build 성공, `Drone.Weather.DebugPresetEntry` 1/1 Success. 기존 기상 회귀 3/3도 성공했다. Rain VFX Niagara, Wetness MPC consumer, Rain Audio, 품질별 GPU 측정은 미완성이다. MCP 서버는 설정돼 있지 않아 별도 연결/설치는 하지 않았다.
- Drone Source/Test/가이드와 문서 STATUS/WORKBOARD/기상·시험 맵 안내를 로컬 수정했다. Unreal 시작 기준 `3449766`, 문서 시작 기준 `8b3b7b1`; Commit·Push하지 않았고 실제 맵/기존 자산을 저장하지 않았다.

## 2026-09-17 — NPC 행동 로직 추가 감사 및 타이밍 수정

- 사용자 요청에 따라 OpenCode `openrouter/stealth/union-alpha`에 NPC 행동 로직 점검·문제 수정 업무를 위임했다. 제공된 키는 프로세스 입력으로만 사용했으며 문서/명령 출력에 다시 기록하지 않았다. 완료된 뒤 별도 모델 실행은 남아 있지 않다.
- `ADroneNPCAIController`에서 MG 재할당 유지 처리와 일반 Controller Tick이 같은 프레임에 `UpdatePersonalWeaponEngagement`를 중복 호출해 사거리 이탈·무진행·재경로 타이머가 두 배 진행될 수 있음을 확인했다. 유지 분기는 유효성 확인만 하고, 한 프레임의 시간/발사/이동 갱신은 Controller Tick 한 곳이 담당하도록 수정했다. `Drone.AI.PersonalWeaponMaintenanceTiming` 회귀를 추가했다.
- UE 5.8.2 `DroneEditor Win64 Development` Build 1회 성공. 한 번 실행한 집중 필터에서 `PersonalWeaponMaintenanceTiming` 성공(로그 경고 7건), `NPCPerceptionSearchPIE` 성공, `ShotgunSystemsTestMapPIE` 실패(정지 pursuit 목표에서 MoveTo 요청 수 기대 2/실제 3). 프로세스 종료 코드 0은 전체 자동화 성공을 뜻하지 않는다.
- 추가 요청이 이미 끝난 경로의 정상 복구인지 중복 제출인지는 PathFollowing 상태·이전 RequestID·완료/중단 사유 로그가 없어 판단하지 못했다. 추측성 가드/테스트 기대값 변경은 하지 않았다. 사용자 보고 몸/머리 떨림은 Headless에서 재현되지 않았으며 저장 AnimBP 전체 그래프/실제 포즈도 이번 확인 범위가 아니다.
- 추가 실행은 사용량을 아끼도록 실패한 Shotgun PIE 한 건만 대상으로 호출 전후 PathFollowing 상태, RequestID, 목표 편차, 완료/Abort 결과를 계측해 원인을 분리한다. 화면 떨림은 PIE에서 관찰할 때 AnimBP Debug Filter와 StateTree 실제 활성 노드를 함께 기록해야 한다.

## 2026-09-17 — Smart Object 맵 종료 후 최종 재검증

- Unreal Editor 종료를 확인한 뒤 최신 `DroneEditor Win64 Development` 빌드를 다시 성공시켰다.
- 실제 스마트 오브젝트 맵 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`만 대상으로 `NPCBaseRoutinesPIE`, `NPCGreyboxPIE`, `NPCPerceptionSearchPIE`를 실행해 3/3 Success, 실패 0, 미실행 0을 확인했다.
- 앞선 연속 실행에서 보였던 MG 재할당 실패는 최종 재실행에서 재현되지 않았다. 다만 해당 자동화의 수동 감지 주입·런타임 프로필 변경 한계 때문에 화면상의 도리도리/옆구리 사격/뒤로 걷기 해결을 자동화만으로 확정하지 않는다.
- 진단용 `SOAudit` 로그 코드는 제거하고 기능 수정만 남겼다. 커밋·푸시는 하지 않았다.

## 2026-09-17 — 순찰 중 NPC 충돌 정지 수정

- 순찰 중 Shotgun NPC가 고개를 돌리며 뒤로 걷고 이동을 반복 중단하는 현상을 `PatrolProjectileFixAudit` 로그로 대조했다. `BP_ShotgunPelletProjectile`이 `ECC_Pawn`을 Block해 NPC를 이동 장애물로 막는 것이 직접 원인이었다.
- `DroneNPCProjectile`이 의도한 표적이 아닌 `ADroneNPCCharacter`를 Sweep Ignore하도록 수정했다. 감지 진입/Search 종료의 잔여 속도 제거와 Patrol 중 Combat Gaze 차단도 함께 적용했다.
- 최신 Editor Build 성공. `NPCPerceptionSearchPIE`와 `NPCBaseRoutinesPIE`가 각각 Success로 통과했고 수정 후 `stuck` 로그가 없었다. 커밋·푸시는 하지 않았다.
- 감사 세부사항과 저장 금지 수동 PIE 절차는 [`../ai/DRONE_NPC_BEHAVIOR_AUDIT_2026-09-17.md`](../ai/DRONE_NPC_BEHAVIOR_AUDIT_2026-09-17.md)에 있다. 추가 빌드/테스트, 맵/에셋 저장, Production Training 접근, commit/push는 하지 않았다.

## 2026-09-16 — 병사 StateTree 상태 전환 안정화

- Cover/MG 태스크가 일시적인 예약·사격 실패를 바로 `Failed`로 반환하고, MG 사망 교대 Event가 0.75초마다 현재 Cover 상태를 끊을 수 있어 병사 상태와 시선이 왕복할 수 있는 경로를 확인했다.
- 먼저 `SmartObjectFoundationDefaults`에 Blueprint 조정 가능한 최소 상태 유지시간 계약을 추가했고, 구현 전 Property가 없어 의도대로 Red가 되는 것을 확인했다.
- `ADroneNPCAIController`가 모든 대응 상태 진입 시각을 한 곳에서 기록하고 기본 `Minimum Response State Duration Seconds=1.0`을 제공하도록 변경했다. 최소시간 동안 `DroneDetected`, MG/Cover 이동·점유·사격, Search의 현재 행동 조건을 재점검하고 시간이 지난 뒤에도 실패일 때만 기존 StateTree 실패 전환을 허용한다.
- MG 재할당 대기 시작 시 개인화기 사격을 즉시 끄지 않고 실제 Event를 보낼 때만 정리하도록 바꿨다. Cover 점유 성공과 같은 프레임에 첫 사격 시작이 실패해도 점유 상태 자체를 실패 처리하지 않으며 `UseCover` Tick에서 다시 시작한다.
- 사망, Drone 파괴, Sight Lost 유예 뒤 확정 정리는 즉시 처리해 위험한 상태를 억지로 유지하지 않는다. 값 `0`은 안정화 대기를 끄며 Controller Blueprint `Drone > AI > State Stability`에서 조정할 수 있다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. Red였던 `SmartObjectFoundationDefaults`와 `HostilePatrolStateTreeAsset`, 차량 `GroundConformingSuspension`은 Success다.
- 실제 `NPCPerceptionSearchPIE`는 2회 모두 감지·사격·Cover·최초 MG 점유와 사망 정리까지 진행했지만, 생존 병사가 빈 MG를 각각 2회/3회 Claim한 뒤 Operator Anchor로 Nav 도착하지 못해 기존 재점유 제한시간 항목에서 실패했다. 상태 안정화 결과와 분리해 맵 경로/Collision 결함으로 계속 추적하며 Success로 기록하지 않는다.
- 최종 Git 감사 중 원격 `72c964c`, Merge `4a3d4ba`가 추가됐고 변경 파일은 팀원 `Lvl_MilitaryBase.umap` 하나였다. 로컬 작업과 겹침이 없어 fast-forward했으며 Unreal 기준은 `main = origin/main = 4a3d4ba`다.
- `stash@{0}: On main: !!GitHub_Desktop<main>` 1개가 남아 있다. Shotgun/Weather/Acro 시기 파일 49개를 포함한 자동 Stash라 현재 로컬 변경과 중복 가능성이 크지만, 사용자 작업 유실을 피하기 위해 이번에는 적용·삭제하지 않았다.

## 2026-09-18 — D 드라이브 기준 재동기화와 NPC 순찰 재현

- `fetch --prune` 뒤 Unreal `D:\JGY\project\drone`은 `main = origin/main = 9f58b51`, 문서 `D:\JGY\project\md`는 `main = origin/main = 6960648`이며 두 저장소 모두 원격 차이 `0/0`임을 확인했다. 문서 최신화 시작 전 두 작업 트리는 clean이었다.
- 최신 Unreal Commit과 사용자 화면 보고를 대조해 Shotgun NPC 뒤로 걷기/문워크는 해결 완료가 아니라 진행 중 결함으로 다시 분류했다. 기존 Actor 전방 정렬 자동화는 Skeletal Mesh 포즈, AnimBP의 Speed/Direction, 실제 BlendSpace 선택을 검증하지 못한다.
- 격리된 `Drone.AI.ShotgunSystemsTestMapPIE`는 경계 흔들림·추적 진전·몸/시선 정렬·사거리 진입 정지·리시 포기 후 순찰 복귀를 모두 통과했다.
- 실제 `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`의 `NPCBaseRoutinesPIE`는 최초 묶음 실패, 단독 재실행 성공 뒤 4회 반복에서 3회 실패해 높은 재현율의 순찰 플래키로 확정했다. `NPCPerceptionSearchPIE`는 같은 기준에서 성공했다.
- 순찰과 개인화기 추적 양쪽에서 `EPathFollowingStatus::Paused`를 정상 진행으로 취급해 재요청과 정체 제한을 우회하던 분기를 확인했다. `Moving`만 실제 진행으로 인정하고 `Paused`는 기존 재요청·2초 정체 처리로 회복하도록 1차 수정했다.
- 실패 시 Rifle/Shotgun 역할, ResponseState, MoveStatus, 완료/방문 횟수, 위치·속도를 보고하도록 실제 맵 자동화 진단을 보강했다. Editor가 열려 있어 Build와 수정 후 반복 검증은 대기 중이다.
- 외부 OpenCode 모델 검증은 실제 호출이 정상 보고서로 이어지지 않아 사용을 종료했다. 이번에 만든 프로젝트 Agent·모델 설정과 문서 가이드는 제거했으며 이후 외부 모델 호출을 작업 기준에 포함하지 않는다.
- Production Training 맵과 Asset은 수정하지 않았고 Commit·Push도 수행하지 않았다.
- 실제 보행 증상을 직접 잡도록 `NPCBaseRoutinesPIE`에 Actor 전방과 실제 수평 속도의 내적을 샘플링하고, 역방향 상태가 0.35초를 넘으면 실패하는 회귀를 추가했다. 수정 전 Shotgun은 3/3 실패했고 `worstDot=-1.000`, 최대 연속 역방향 1.56~3.95초가 기록됐다.
- 순찰·수색·추적 등 실제 이동 중에는 상태명이 아니라 속도 벡터를 몸 Yaw의 단일 기준으로 사용하도록 수정했다. 같은 회귀를 포함한 실제 맵 순찰은 수정 빌드에서 4/4 성공했다.
- 묶음 회귀의 `ShotgunSystemsTestMapPIE`에서 고정 표적에 MoveTo가 1회에서 2회로 늘어나는 Red를 추가로 추적했다. 첫 감지를 Perception과 StateTree가 중복 진입해 경로를 취소할 수 있는 흐름, 순찰 Task의 늦은 종료가 전투 MoveTo를 취소하는 소유권 충돌을 막았다.
- 마지막으로 첫 MoveTo가 `Success`로 끝났어도 부분 경로/허용 반경 때문에 실제 사거리 밖일 수 있고, 기존 코드는 같은 투영 목적지를 즉시 재요청함을 확인했다. 성공 완료한 동일 목적지는 정착 상태로 유지하고 표적이 재경로 거리 이상 이동할 때만 새 경로를 만들며, 계속 사거리 밖이면 기존 무진전 제한으로 포기·순찰 복귀하도록 수정했다.
- 임시 `[DEBUG-MOVE-COMPLETE]`, `[DEBUG-PURSUIT-REPATH]` 계측은 제거했다. Editor 종료 뒤 MSVC 14.51.36257 `DroneEditor Win64 Development` 최종 링크 Build가 성공했다.
- 전용 Shotgun PIE의 Pursuit 표적은 시험 맵 NavMesh 안의 실제 사거리 밖 지점으로 옮겨 부분 경로 Success와 정상 추적을 혼동하지 않게 했다. 단독 `ShotgunSystemsTestMapPIE`가 Success이고, `PersonalWeaponEngagementPolicy`, `PersonalWeaponMaintenanceTiming`, `ShotgunSystemsTestMapPIE`, `NPCGreyboxAssets`, `NPCPerceptionSearchPIE` 묶음 5개도 전부 Success·실패 0이다.
- 실제 Smart Object 맵 `NPCBaseRoutinesPIE`를 `-TestLoops=4`로 실행해 4/4 Success, 오류·경고 0을 확인했다. 수정 전 4회 중 3회 실패 및 몸/속도 역방향 3/3 Red였던 피드백 루프가 최종 Green으로 바뀌었다. 맵·Asset은 저장하지 않았고 Commit·Push도 수행하지 않았다.

## 2026-09-18 — Shotgun Pursue 전신 회전 후속 수정

- 사용자 화면 보고의 Shotgun 빙글빙글 회전을 `Drone.AI.ShotgunSystemsTestMapPIE`에 같은 대응 상태 안에서의 연속 몸 Yaw 회귀로 재현했다. 수정 전 `PursueDrone`에서 3초 안에 같은 방향 누적 `301~304°`를 반복해 넘겼고 최근 Yaw·속도 표본을 확보했다. 상태가 바뀌면 누적값을 초기화해 서로 다른 행동의 정상 회전은 합산하지 않는다.
- 진단 계측에서 Nav 가속과 RVO는 이미 꺼져 있었지만 `UCharacterMovementComponent::bRequestedMoveUseAcceleration`은 켜져 있었다. Drone 위치에 무기 사거리 크기의 큰 도착 반경을 둔 MoveTo가 가까운 부분 경로 Segment를 가속으로 지나치고, 몸과 Bone Gaze가 약 40~120cm 거리의 즉시 경로 코너를 계속 따라가며 공전하는 흐름을 확인했다.
- Drone에서 `PersonalWeaponPursuitRangeRatio`만큼 떨어진 실제 지상 사거리 정지점을 NavMesh에 투영하고 기본 75cm 도착 반경으로 이동하도록 바꿨다. Pursue에만 요청 가속을 기본 해제하고, Controller가 안정된 최종 정지점을 향해 몸 Yaw를 보간하며 Bone Gaze도 같은 목표를 공유한다. 순찰·수색의 실제 속도 방향 보정과 정지 사격 조준은 유지했다.
- 요청 가속을 전 상태에서 끈 첫 시도는 실제 맵 회귀가 순찰 역방향 `0.614초`를 검출했다. 이를 Pursue에만 한정하고 일반 순찰은 요청 가속을 유지하도록 수정한 뒤 다시 검증했다.
- 전용 Shotgun PIE에는 같은 상태에서 연속 300° 초과 몸 회전 실패 조건을, 실제 Smart Object 맵 회귀에는 정지 회전과 0.35초 초과 역방향 보행 실패 조건을 유지·추가했다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. 완전히 새 Editor 프로세스에서 Shotgun 교전 3/3, 실제 Smart Object 맵 순찰 3/3이 성공했다. `NPCGreyboxAssets`, `NPCPerceptionSearchPIE`, `PersonalWeaponEngagementPolicy`, `PersonalWeaponMaintenanceTiming`, `ShotgunSystemsTestMapPIE` 관련 묶음 5개도 모두 Success다. Maintenance의 Skeletal Mesh 없는 최소 시험 Actor 경고 7건은 예상 경고다. 맵·Asset·Production Training은 수정하지 않았고 Commit·Push도 수행하지 않았다.
- 종료 정리 중 `fetch --prune`에서 `origin/main=9a94f06 260918`을 새로 확인해 로컬 `main=9f58b51`이 1개 뒤가 됐다. 원격 커밋은 Content 1,412개만 변경하고 Source·Config·Plugins·현재 AI 소스·Shotgun/Smart Object 시험 맵과 겹치지 않는다. `Lvl_DroneTraining`과 `Lvl_DroneTutorialSystemsTest` 및 대용량 LFS 에셋을 포함하므로 더러운 작업 트리에 자동 Pull하지 않았으며, 위 검증은 로컬 기준이다.

## 2026-09-18 — Shotgun 순찰 충돌 2차 원인과 FPV Mode 1/2

- 사용자가 실제 `Lvl_NPCSmartObjectGreybox`를 다시 실행했을 때 Shotgun의 회전 주기만 줄어든 채 증상이 남았다. 이 실행의 `Drone.log`에서 Rifle이 Shotgun BP의 추가 `Gun` 컴포넌트에 침투·충돌해 `stuck and failed to move`가 되는 정확한 상대를 확인했다.
- 자동 PIE에서도 Shotgun `Gun`이 `QueryAndPhysics`, Overlap On, Navigation On으로 재현됐다. NPC Character는 이동 Capsule만 충돌을 소유하고, Construction/BeginPlay에서 나머지 Primitive를 `NoCollision`, Overlap Off, Nav Off로 강제하도록 변경했다. 역할 BP에 팀원이 별도 Gun/Mesh를 추가해도 같은 계약을 적용한다.
- 순찰 시작 구간에서 Shotgun이 100cm 진행하기 전에 누적 300도를 도는 Red도 추가했다. Nav의 50~100cm 즉시 경로점을 몸 방향으로 계속 쓰던 흐름을 분리하고, Patrol 몸은 예약된 최종 Smart Object 슬롯 방향을 유지하도록 했다.
- 수동 재현 후 바로 원인을 읽을 수 있도록 개발 빌드에 `[NPC-STATE]`, `[NPC-MOVE]`, `[NPC-COLLISION-FIX]`를 추가했다. 이동 로그는 적 NPC당 기본 0.5초 간격이며, 화면 해결 확인 뒤 기본 비활성화할 임시 진단 단계다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `NPCBaseRoutinesPIE`, `NPCGreyboxPIE`, `ShotgunSystemsTestMapPIE`가 모두 Success이고 수정 뒤 `stuck` 로그가 없다. 실제 렌더 화면에서 45~60초 순찰 교차·추적·복귀 확인은 사용자 수동 항목으로 남겼다.
- FPV 조작은 기존 Easy·제한 자세에 RC 송신기 Mode 1과 Mode 2를 별도 모드로 추가했다. Mode 1은 왼쪽 Y Pitch/오른쪽 Y Throttle, Mode 2는 왼쪽 Y Throttle/오른쪽 Y Pitch이며 두 모드 모두 왼쪽 X Yaw/오른쪽 X Roll이다. 키보드는 W/S Pitch, A/D Roll, Q/E Yaw, Space/Ctrl Throttle을 공통 유지한다.
- 새 패드 세로축 Input Action 2개와 IMC 전체 33 Mapping을 저장하고 FPV Pawn BP에 연결했다. 기존 `AcroRateRealisticGreybox` 이름은 Asset 직렬화 호환을 위해 Mode 2 의미로 유지했다.
- UI의 `안정/균형/고기동`은 `느림/보통/빠름`으로 바꿨다. 내부 Stable/Balanced/Agile 이름은 Asset 호환을 위해 유지하고 기본 프리셋은 MaxSpeed `0.80/1.00/1.25`만 변경하며 가속·Yaw·자세각 배율은 모두 1.0이다.
- 입력 변경 후 `AcroInputContract`, `FlightProfiles`, 3회 새 PIE의 `PIEInputLifecycle`, `MissionEntryPIE`가 Success다. Lifecycle은 처음에 새 Action을 예상 목록에서 빼 `31/33` Red, 다음에는 Completed/Canceled Binding 분류 누락으로 Red가 났고 테스트 계약을 보완해 최종 Green으로 전환했다.
- Production `Lvl_DroneTraining`은 열거나 저장하지 않았고 Commit·Push·원격 Pull도 수행하지 않았다.

## 2026-09-18 — 첫 사격 조준 지연·Figma 재확인·CourseSpline 편집 확인

- 사용자 화면에서 Shotgun/Rifle 이동·회전 수정이 정상임을 확인해 임시 이동 진단 로그 기본값을 Off로 전환했다.
- 적이 Drone을 최초 감지한 뒤 Rifle/Shotgun 첫 발까지 기본 1.0초를 기다리는 `PersonalWeaponInitialAimDelaySeconds`를 Controller Blueprint 조절값으로 추가했다. Sight 감지 시각을 별도로 보존하므로 DroneDetected/Pursue/Cover 상태 전환이 지연을 재시작하지 않는다.
- 다른 Drone으로 표적이 바뀔 때 기존 사격 Timer가 새 조준 지연을 우회하지 않도록 이전 개인화기 사격을 먼저 정리한다.
- MSVC 14.51.36257 Editor Build, `SmartObjectFoundationDefaults`, `ShotgunSystemsTestMap`, `ShotgunSystemsTestMapPIE`, `NPCGreyboxPIE`가 Success다. Shotgun PIE는 조준 완료 전 Fire Event 0과 감지 관측 시각부터 첫 Volley까지의 시간도 검사한다.
- Figma `Project:Droner` Page 1 최상위 148개를 읽기 전용으로 재확인했다. 최신 Mission 진입 흐름, Mission 선택 Greybox, 공중 Drone 공통 HUD, Racing UI/Restart/Quit/기록·감도·Ghost 요구를 문서 매트릭스에 반영했으며 Figma 원본은 수정하지 않았다.
- CourseSpline 점 추가는 UE 5.8 기본 편집 기능으로 이미 제공된다. `CourseSpline`의 기존 점 선택 후 `Alt+이동 기즈모 드래그` 또는 선분 우클릭 `Add Spline Point Here`를 사용한다. Ring별 Spline Handle은 Gate 전용이므로 구분한다. 코드·Blueprint·맵은 수정하지 않았다.

## 2026-09-22 — 야외 AI·차량 Spline Route·Random Weather Manager

- Native AI 기본값을 유지하면서 `/Game/Drone/AI/Blueprints/BP_DroneNPCAIController_Outdoor`를 추가했다. Hostile Rifle/Shotgun은 이 BP를 사용하며 Sight 60m, Lose Sight 70m, Smart Object 검색 반경 80m·Half Height 10m, 직전 완료 지점 회피 15m를 Blueprint에서 조정한다.
- `/Game/Drone/Vehicles/Blueprints/BP_DroneVehicleSplineRoute`와 `ADroneVehicleSplineRoute`를 추가했다. 차량은 Instance에서 Route를 지정하고 Follow, 속도, 끝 반전/Loop를 조정한다. XY/Yaw는 Spline 위치·접선, Z/Pitch/Roll은 기존 4점 지면 Trace가 담당하며 종점 Event를 노출한다.
- `/Game/Drone/Weather/Blueprints/BP_DroneRandomWeatherController`를 배치형 Weather Manager로 추가했다. E/NE/N/NW/W/SW/S/SE와 CALM, 방향 8~18초·세기 5~12초·풍속 1~9m/s 시작값, 방향/속도 보간과 재현 Seed를 Blueprint Class Defaults에서 조정한다.
- Manager는 에디터에서 위치 확인용 원뿔 Mesh를 보이지만 Editor 전용 Component라 Play/Package에는 존재하지 않는다. Actor·원뿔 Collision, Overlap, Navigation 영향은 모두 끈다.
- Runtime Wind Override를 World Subsystem에 추가해 Random Manager가 Profile의 비·가시거리 등은 유지하면서 수평 바람만 갱신한다. CALM은 Gust까지 억제해 실제 0m/s가 된다.
- 풍향 표기는 프로젝트 좌표 `+X=E`, `+Y=N` 기준 Cardinal로 통일했다. Flight HUD는 `풍향 NE | 풍속 5.2 m/s`, Debug Visualizer는 같은 방향과 m/s를 표시한다.
- 팀원이 수정 중인 `Lvl_DroneShotgunSystemsTest`, `Lvl_NPCSmartObjectGreybox`는 덮어쓰지 않았다. 차량 Route는 안전한 TestMap에서 맵 담당자가 직접 배치·연결하도록 남겼다. Production `Lvl_DroneTraining`도 수정하지 않았다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. Weather TestMap 재생성 Map Check 0/0, `SmartObjectFoundationDefaults`, HUD 2종, `GroundConformingSuspension`, Weather 2종 최종 6/6 Success·경고 0이다. Commit·Push는 수행하지 않았다.

## 2026-09-23 — 강우·실내 감쇠와 광섬유/지상 Drone 기반

- 사용자가 Random Weather의 수동 화면 확인과 차량 Spline Route 시험 맵 제작·화면 확인을 완료했다고 보고했다. 두 항목은 재작업 목록에서 제외하고 최근 완료로 이동했다.
- Weather World Subsystem에 비 Runtime Override를 추가했다. Manager의 `Enable Rain`을 끄면 Rain 표현값만 0이 되고 현재 Profile ID와 바람은 유지되며, Manager 종료 시 Override를 정리한다.
- `/Game/Drone/Weather/Blueprints/BP_DroneRainVisual`을 추가했다. 로컬 카메라 주변 최대 160개 Instanced Mesh 빗줄기를 재사용하고 Collision·Navigation·Shadow를 끈다. 카메라 위쪽 Visibility Trace를 기본 0.2초마다 한 번 수행하고 기본 0.35초로 실내 감쇠를 보간하므로 Particle별 Trace나 World Snapshot 변경은 없다.
- `/Game/Drone/Integrations/RoleDrones/BP_DroneFiberOpticIntegration`과 `DA_Drone_FiberOptic_Greybox`를 추가했다. 외부 Sting Interceptor Visual만 참조하며 프로젝트 코드의 `JammingImmunity + ImpactDetonation`, 1인칭 기본값을 사용한다.
- `/Game/Drone/Integrations/RoleDrones/BP_DroneGroundUGVIntegration`과 `DA_Drone_GroundUGV_Greybox`를 추가했다. 외부 GC Drone 1 Skeletal Visual만 참조하며 W/S 전후·A/D 조향·Q/E 제자리 회전, 고도 입력 차단, 네 지점 Trace의 높이/Pitch/Roll 추종과 Weather Drift 비활성화를 적용했다. 지면 간격·Clearance·Trace·보간·조향값은 Blueprint에서 조정한다.
- Tutorial Mission과 선택 Catalog/UI를 Scout/FPV/Drop/Fiber/Ground 5종으로 확장했다. 공급 Asset의 Skeleton은 수정하지 않고 Integration BP에서 Visual로만 참조한다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `Drone.Weather` 4/4, `Drone.Integration.ExtendedRoleDrones` 1/1, 5종 `Drone.Flow.Contract`, `Drone.Flow.FrontEndContract`, `Drone.Flow.FrontEndPIE`가 각각 1/1 Success이며 Weather Validate/Map Check는 0 errors / 0 warnings다.
- 작업 시작 기준 Unreal `main = origin/main = de81c19`, 문서 `main = origin/main = 6527d7b`였다. 기존 사용자 변경 `MG_Turret`, `GC_Drone_2`, `GC_Drone_3` Skeleton 3개는 되돌리거나 저장하지 않았고 Production `Lvl_DroneTraining`은 열거나 저장하지 않았다. Commit·Push는 수행하지 않았다.

## 2026-09-23 — 광섬유 통 슬롯·처짐 케이블과 UGV 고공 Spawn 접지

- 사용자 요구에 따라 광섬유 통은 임의 에셋을 넣지 않았다. `BP_DroneFiberOpticIntegration`에 상속되는 빈 `FiberSpoolMeshComponent`를 만들고 기본 위치 `(-32,0,-18)cm`, 통 출구 Offset `(-14,0,-3)cm`만 설정했다. 제작 통은 이 Static Mesh 칸에 넣고 Transform을 BP에서 조정한다.
- 광섬유 역할이 활성화되면 통 출구 아래 지면을 찾고, 이동 경로 아래에 기본 160cm 간격으로 지면 점을 누적한다. `FiberOpticSplineComponent`가 누적 지면점과 현재 통 출구를 연결하고 마지막 구간에는 기본 45cm 처짐점을 추가한다. Engine Cylinder 단면의 Spline Mesh와 OilRig Cable Material을 사용하되 Collision·Overlap·Navigation·Shadow는 끈다.
- 지상 UGV가 높은 PlayerStart에서 360cm 일반 Trace 범위 밖 지면을 못 찾아 공중에 남는 회귀를 자동화로 재현했다. 최초 최대 10,000cm 장거리 Trace로 지면을 획득해 접지한 뒤 기존 4점 높이/Pitch/Roll 추종으로 전환한다. Visibility를 막지 않는 지형은 WorldStatic/WorldDynamic Object Trace가 보조하며 W/S 이동 벡터에서 World Z를 제거했다.
- 수정 전 `Drone.Integration.ExtendedRoleDrones`는 통 슬롯·Spline·표시 Segment·고공 Spawn 접지 4개 조건으로 실패했다. 수정 후 같은 테스트 `1/1`, 전체 `Drone.Prototype` `8/8`이 Success이고 `DroneEditor Win64 Development` Build도 성공했다. 첫 Prototype 전체 회귀에서 빈 통 슬롯까지 외형 개수로 세던 `VisualBank` 계약 1건을 실제 Mesh 보유 Component만 세도록 보정한 뒤 8/8 Green을 확인했다.
- 공급사 Skeleton과 Production `Lvl_DroneTraining`은 열거나 저장하지 않았고 Commit·Push도 수행하지 않았다.

## 2026-09-23 — OilRig Mask 강우와 천장 침투 차단

- Weather TestMap의 파란 선은 실제 비가 아니라 `ADroneWeatherDebugVisualizer`의 구형 DrawDebug 프리뷰였고, 흰 긴 선은 Cube Instanced Mesh를 늘인 Greybox였다. 구형 프리뷰를 기본 `Off/0개`로 바꾸고 화면 Readout에서도 Debug streak 수를 제거했다.
- OilRig 원본은 수정하지 않고 `/Game/Drone/ThirdParty/OilRig/Rain/Texture/T_rain_Mask`만 참조하는 프로젝트 소유 Translucent Unlit Material `M_DroneRainStreak_OilRigMask`를 생성했다. 빗줄기는 카메라를 향하는 Plane으로 바꾸고 최대 112개, 기본 길이 65cm·폭 2.4cm·Opacity 0.22·개별 크기 편차·낙하 2,600cm/s로 긴 균일 잔상을 줄였다.
- 카메라 위쪽 실내 판정 외에 각 활성 빗줄기 열을 프레임당 기본 8개씩 분산 Trace한다. Visibility가 안 막히는 Marketplace 지붕도 WorldStatic/WorldDynamic Object Trace로 보조 검출하고, Streak 하단이 표면에 닿기 전에 숨겨 천장과 지면 아래 선을 막는다.
- `DroneEditor Win64 Development` Build, Weather 생성 도구 Validate, Map Check `0 errors / 0 warnings`, `Drone.Weather` `4/4`가 모두 성공했다. Material/Blueprint 생성은 TestMap Validate로 수행했으며 Production Training은 열거나 저장하지 않았다. 최종 비 길이·농도·천장 전환은 렌더 화면 수동 확인이 남았다.

## 2026-09-30 — 단일 고속 기준·Payload 질량·Rate/Acro 물리 v2

- 사용자 요구에 따라 기체 선택 화면의 느림/보통/빠름 버튼을 제거했다. `EDroneHandlingPreset`, `Set/CycleHandlingPreset`, 기존 WBP Widget 이름은 저장 Asset과 Blueprint 호출 호환을 위해 남기되 런타임은 항상 `Balanced` 단일 기준으로 정규화한다.
- 각 Definition의 기존 Base Max Speed에 `UnloadedMaximumSpeedMultiplier=1.25`를 적용해 별도 선택 없이 기존 빠름 수준을 무적재 기본 성능으로 사용한다. 선택 화면에는 무적재 최고속도와 기체 질량을 표시한다.
- `FDronePhysicalFlightSettings`에 Dry Mass 2.0kg, 합산 최대 추력 40N, 모터 응답 0.055초, 제곱 항력, 적재 속도 하한을 추가했다. 모든 값은 Data Asset 또는 Pawn Flight Profile Override에서 조정할 수 있다.
- RC Mode 1과 Mode 2는 Pitch/Throttle 세로축 배치만 다르고 같은 질량·추력·모터 응답·중력·Body Up 추진·선형/제곱 항력·Body Rate 응답을 공유한다. 총질량과 Newton 추력으로 현재 호버점을 계산하며 스로틀 명령에는 즉시값이 아닌 모터 1차 응답을 적용한다.
- `ADroneDroppedPayload`에 인스턴스/BP 조절 가능한 `PayloadMassKilograms` 기본 0.75kg을 추가했다. Drop Drone의 내장 화물도 Component 기본 질량을 가지며 적재/투하/운반 중 질량 변경 즉시 최고속도·가속·감속·Yaw와 Acro 추력 대비 중량이 다시 계산된다.
- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공. `Drone.Prototype` 8/8, `Drone.Physics` 2/2, `Drone.Flow` 5/5가 Success다. Production `Lvl_DroneTraining`과 Content Asset은 수정하지 않았고 Commit·Push도 수행하지 않았다.
- 이 구현은 실제 조작 축과 하중 반응을 반영한 게임용 물리 Greybox v2다. 모터별 RPM/PID/프로펠러 유동/관성 텐서/배터리 전압을 푸는 공학 시뮬레이터로 판정하지 않으며, 실제 기체별 질량·추력 자료가 정해지면 Definition마다 교정한다.

## 2026-09-30 — Bangkok City 실맵 이식·OilRig Overview 재확인

- `D:\JGY\project\BangkokCity`는 독립 `.uproject`가 아닌 `/Game/BangkokCity` Content 루트임을 확인했다. `Maps/Overview`는 전시 맵이고 실제 환경 `Maps/BangkokCity`를 이식 대상으로 선택했다.
- 원본을 수정하지 않고 일회용 UE 5.8 스테이징에서 `/Game/Drone/Maps/Lvl_BangkokCity`를 만들고 GameMode Override를 비웠다. 의존 자산 987개를 `/Game/Drone/ThirdParty/BangkokCity`로 이동했다.
- 첫 저장은 `/Game/Drone` 전체를 저장해 기존 스테이징 팩 재빌드와 로컬 DDC 507을 유발했다. 저장 범위를 대상 ThirdParty 폴더와 Seed Map으로 좁혔고, 남은 360개 참조가 전부 ObjectRedirector임을 확인한 뒤 `ResavePackages -FixupRedirects`로 중앙 맵을 재저장했다.
- 최종 스테이징과 본 프로젝트 감사 모두 Map load 성공, 자산 987개, 의존성 988개, 외부 `/Game` 0, 누락 0, `default_game_mode=None`, Map Check 0 errors / 0 warnings다.
- 신규 파일은 맵 포함 988개, 12,309,059,738 bytes(약 11.46GiB)이며 모두 Git LFS 대상이다. Commit·Push는 수행하지 않았다.
- `D:\JGY\project\Unreal_260821\OilRigLiope_Tr`의 기존 중앙 맵은 이미 `/Game/Liope_Tr/Maps/Overview` 복제본이다. `PrepareOilRigMap.py`와 과거 감사에서 Preview 체인 제외, Vendor GameMode 제거, Sample Door 8개 제거가 확인돼 재이식하지 않았다.
- 자동 Gate 하단 1/6 배치는 기존 구현을 재확인했다. `AutomaticGateSplineHeightFraction=1/6`이고 Gate 중심을 `ApertureHalfSize × ScaleZ × (1 - 2 × Fraction)`만큼 올려 Spline/안내선은 그대로 둔다. 공통·개별 Gate Scale 뒤에도 같은 비율을 유지하며 수동 `OrderedGates`는 이동시키지 않는다.

## 2026-09-30 — OilRig 실제 Preview 별도 이식

- 사용자 정정에 따라 기존 Overview 기반 `/Game/Drone/Maps/Lvl_OilRig`을 덮지 않고 실제 장면 `/Game/Liope_Tr/Maps/Preview`를 `/Game/Drone/Maps/Lvl_OilRigPreview`로 별도 이식했다.
- 원본은 수정하지 않고 전용 `OilRigPreviewStage`에서 처리했다. 맵의 Vendor GameMode를 제거하고 재귀 의존 자산 614개를 `/Game/Drone/ThirdParty/OilRigPreview`로 이동했다.
- 문 Blueprint 32개가 구형 FirstPerson Character·Input·Arms를 끌어오는 경로를 확인했다. 문/문틀 Static Mesh Component 64개는 World Transform과 Material을 보존한 일반 StaticMeshActor로 바꾸고 상호작용 Wrapper만 제거했다.
- 빈 StaticMeshActor 14개와 메시·Transform이 완전히 동일한 중복 1개를 제거했다. 같은 위치에 서로 다른 구조 메시를 조립한 공급사 배치는 유지했다.
- 본 프로젝트 최종 감사에서 Map load 성공, 자산 614개, dependency closure 615, 외부 `/Game` 0, 누락 0, `default_game_mode=None`, Map Check `0 errors / 0 warnings`를 확인했다.
- 신규 맵과 자산은 4,082,822,021 bytes(약 3.80GiB)이며 Git LFS 대상이다. Commit·Push는 수행하지 않았다.

## 2026-10-01 저녁 — UI-LAYOUT-01 자동 검증 완료·수동 확인 대기

아래 Build·테스트·LFS·Figma 결과는 Claude 작성 작업 지시서의 C PC 결과를 Codex가 문서에 반영한 것이다. Codex는 Build·PIE·맵 생성 도구를 실행하지 않았다. Codex의 읽기 전용 Git 조회에서 HEAD `ec2e88f`와 지정 미커밋/미추적 파일 목록은 확인했다. 이전 같은 날 점검과 D PC 결과는 당시 기록으로 보존한다.

- 환경: C PC, Unreal `ec2e88f`(팀원 Yook34 Content 191파일 수신, LFS 9,039 본문 확인) + 로컬 미커밋 Source 3파일. 작업 도구 Claude.
- Build: `DroneEditor Win64 Development` 성공(우리 코드 경고 0, 엔진 헤더 C4996만).
- 전체 `Drone.*` NullRHI 75개: 성공 62 · 경고 동반 성공 4 · 실패 9.
  - 해결: `UI-LAYOUT-01` 렌더 진단 `LobbyLayoutStabilityPIE` Fail → **Success**(RenderOffScreen 1920×1080). EnterStory 0.3px, EnterTraining 13→0px, 첫 선택 36.1→0px, 이후 선택·열 이동 모두 0px. 원인 3개: 선택마다 목록 전체 재생성+AutoWrap 첫 프레임 폭 미확정 / 넘칠 때만 생기는 스크롤바 13px(9+2×2) / 선택 전 빈 메타 줄.
  - 해결: `HoverMissionPIE`는 10월 로비 개편(타이틀 [훈련]→Tutorial) 미반영 테스트였다. `OpenTrainingLobby()`로 진입하도록 고쳐 Success.
  - 기존(변경 없음): `TrainingAssets`·`TrainingPIESmoke` = 팀원 Production Training 맵 중간 상태(기존 기록과 동일, 맵 미수정).
  - 기존(변경 없음): `NPCGreyboxAssets`·`NPCGreyboxPIE`·`NPCBaseRoutinesPIE`·`NPCPerceptionSearchPIE` = 9/22 NPC 맵 증설(Rifle·Shotgun 각 3, SO 34) 뒤 고정 개수 테스트 미갱신.
  - 회귀(조사 필요): `ShotgunSystemsTestMapPIE` 9/18 통과 → 지금 Shotgun NPC가 Drone을 전혀 감지하지 못함(detected=0, 발사 0). 9/22·9/29 AI 자산 변경(Outdoor Controller 연결 등) 이후로 의심. 2회 재현.
- 회귀 확인: `Flow.FrontEndPIE`·`FrontEndContract`·`MissionEntryPIE`·`BackNavigationContract`·`HoverMissionPIE` Success.
- 수동 확인 대기: 1280/1920 실제 화면 가독성, 스크롤바 상시 표시가 Story 4개 목록에서 어색하지 않은지.
- WORKBOARD: `UI-LAYOUT-01` → 자동 검증 완료·수동 확인 대기. 신규 카드 `AI-SHOTGUN-REGRESS-01`, `TEST-NPC-COUNT-01`, `FIGMA-RACING-02`(아래).

### Figma 재대조(2026-10-01, 읽기 전용) — 09-24 매트릭스 이후 새 항목
- Slide 63 "드론레이싱 계획 변경": 맵 1개+랜덤+코스 선택 → **맵 여러 개 + 맵별 코스 + 랜덤 없음 + 사용자가 직접 선택**. 현재 구현(Racing 1맵, Route 선택 `5`=무작위)과 다름.
- Slide 57/58 레이싱 UI: 골드/실버/브론즈 목표 기록, 쉐도우(이전 기록), 리플레이, 스틱 입력 오버레이, 조종 감도(Rate/스로틀 커브), 3·2·1 카운트다운, Restart/Quit. 코드에는 Countdown·Ghost·스틱 오버레이 없음.
- Slide 55 HUD: 배터리 게이지·나침반/헤딩·풍향 기호·HP·기체명·목표 현황·신호 주파수. 현재 HUD에 배터리·기체명·주파수 없음(속도/고도/수직속도/Heading/HP/Signal/Weather는 있음). Figma 드론별 "배터리 시스템(드론별 시간)"도 미구현.
- Slide 34/42/43/44: 미션별 허브(HUB) 브리핑 대사와 HUD 서브텍스트가 정리됨. `UDroneMissionDefinition`에는 DisplayName·LobbyDescription·BriefingAsset만 있어 대사/서브텍스트 필드 없음.
- 스토리 충돌(현재 미정, 임의 확정 금지): 세계관 슬라이드는 "M2 차량은 미끼, 오마르는 M3에서 사살"인데 M3 브리핑은 "오마르는 처리됐다"로 시작. M3·M4 표적도 구 슬라이드 MANPADS ↔ 신 슬라이드 방공망 '베일(VEIL)'로 표기가 갈린다. STORY-BRANCH-01 양쪽 분기 기반은 이미 있음.

### 협업 설정 반영

- 작업 도구: Claude 작성·구현·검증, Codex 로컬 문서·Space 반영. 설정 원문 교체와 Codex→Claude 이관 절/역할 분담을 기록했다. 연결 시험 종료 코드 0은 Claude 지시서 근거다. Commit/Push·Trello/Figma 수정·Production 맵 변경은 하지 않았다.

### Drone Space 미반영

- 2026-10-01 저녁 Space 반영 실패: 두 기존 페이지의 본문·편집 권한은 읽었으나 저장 도구가 "MCP tool call requires approval, but approval policy is never"로 차단했다. 이번 편집은 적용되지 않았다. 진행상황과 다음 작업의 UI 자동 검증/75개 판정/Shotgun 회귀/Figma 새 항목, 테스트 맵과 확인 가이드의 1280/1920·Story 상시 스크롤바 칸 수동 확인 항목이 미반영이다. 기획과 개발 기준은 변경하지 않았다. 새 Page·공유 권한 변경·예약 자동화는 없다.

## 2026-10-01 저녁 후속 — 협업 체계·다른 PC 세팅·낡은 규칙 정리·Space 재시도

- 실행 담당/작업 도구: Claude. 문서·Space 반영 담당: Codex. 근거는 Claude 작성 `runs/20261001-185310-docs-docs-collab/prompt.md`, Unreal `.claude/codex-bridge/COLLABORATION.md`·`SETUP.md`. Codex 읽기 전용 Git 확인: C PC HEAD `ec2e88f`, 미커밋 Source 3파일(DroneFrontEndRootWidget.h/.cpp, DroneTutorialHoverPIETest.cpp)·AGENTS.md·.gitignore, 미추적 CLAUDE.md·.mcp.json·.claude/. md는 앞선 docs-sync 포함 로컬 미커밋이며 Commit/Push하지 않았다.
- 구현됨(Claude 지시서): 협업 규칙·SETUP·BRIEF_TEMPLATE·PC 점검·경로 탐색 스크립트, docs 브리지의 `--approve-for-me`, 공유/PC 전용 설정 분리 및 Unreal 지침 경로/링크 수정. Codex는 STATUS·WORKBOARD·가이드에 반영하고 `SYNC-COLLAB-01`을 추가했다.
- 자동 검증됨(Claude 지시서, C PC): `Test-CollabSetup.ps1 -WriteLocalConfig` COLLAB_READY(FAIL 0), WARN 공유 파일 Git 미추적·Editor 실행 중. Codex는 이 점검을 재실행하지 않았다.
- 로비 후속 3건 코드 구현됨: 재사용 경로 줄바꿈 설정 재적용, WBP 상시 스크롤바, 기본 줄바꿈 폭 160→270(목록 열 309px − 버튼 여백 28 ≈ 281px 안쪽). 후속 Build·재검증은 미실행/미확인. 18:29 사용자 Editor 실행·Live Coding 활성으로 Build 거절(OtherCompilationError), Claude 지시서 출처 `C:\URproject\drone\Saved\Automation\ClaudeRecheck4\build.log`. 직전 160 버전 LobbyLayoutStabilityPIE Success를 후속3건의 검증으로 확대하지 않았다.
- 수동 확인 대기: 1280/1920 로비 가독성·Story 4개 목록 상시 스크롤바 칸·다른 PC SETUP 절차. 다른 PC 실제 세팅은 미구현(공유 파일 Commit/Push 전). 완료 조건은 사용자 drone·md Commit/Push → 다른 PC Pull → 점검 COLLAB_READY → 첫 docs 위임 Space 저장 확인이다.
- 낡은 규칙 정리: md CLAUDE 서두/실행·문서 담당/Space 실패 구분, WORK_PC_START_HERE 최신 STATUS·WORKBOARD 우선/당시 기록 보존/D PC 예시/Build·PIE·자동화 Claude 담당, CODEX_CONTEXT_SYNC 종료·Wrapper Commit/Push 사용자 요청 시만. md 공유 `.claude/settings.json`의 additionalDirectories를 `.claude/settings.local.json`으로 옮기고 `.gitignore`에 제외 추가, 나머지 공유 설정은 유지했다.
- Drone Space: 기존 진행·테스트·안내 페이지 3개, 편집 연산 8건 적용 후 재조회 본문 일치 확인. 진행에는 앞선 미반영 UI/75개 판정/회귀·카드/Figma 현재 미정과 후속 Build 대기, 테스트에는 로비 수동 확인, 안내에는 역할 분담/코드 요청 카드 인계를 반영했다. 기획·Blueprint 페이지는 변경하지 않았다. 앞선 저장 차단 이력은 보존, 이번 대상 미반영 없음.
- 범위 유지: Unreal 파일 수정·Editor/Build/PIE·맵 생성·Commit/Push·Trello/Figma 수정·공유 권한 변경·예약 자동화·새 Page 생성 없음. 스토리 충돌과 레이싱 맵/코스 방식은 현재 미정이다. 기존 날짜별 기록·Codex 표기는 바꾸지 않았다.
- 로컬 확인: JSON 파싱·공유 설정 additionalDirectories 제거·로컬 경로 보존·git check-ignore 확인, git diff --check 통과. 최종 git status --short로 기존 변경과 이번 대상 파일을 구분해 보고한다.

## 2026-10-01 19시 이후 후속 — 로비 후속 검증 완료·사용자 규칙 설치

- 실행 담당/작업 도구 Claude, 문서·Space 반영 Codex. C PC Unreal HEAD ec2e88f + 이전과 동일한 미커밋 Source 3파일, md 로컬 미커밋. 근거 Claude 지시서 runs/20261001-190132-docs-docs-followup/prompt.md.
- 후속 3건(재사용 경로 줄바꿈 재적용·WBP 상시 스크롤바·기본 줄바꿈 폭 160→270) 구현됨·자동 검증 완료. 2026-10-01 19시 이후 후속 보고, C PC, 작업 도구 Claude: Editor 종료 후 DroneEditor Win64 Development Build Succeeded, RenderOffScreen 1920×1080 LobbyLayoutStabilityPIE·FrontEndPIE·FrontEndContract·MissionEntryPIE·BackNavigationContract·HoverMissionPIE 6/6 Success. 로비 단계별 최대 이동 0.255px(기준 2px). 근거 Saved/Automation/ClaudeRecheck5/build.log·render.log. Codex는 위 로그의 성공과 0.255px를 읽기 전용 대조했으며 Build/PIE를 실행하지 않았다.
- 줄바꿈 270 실측(Claude 지시서): Story 4개 중 2개·Training 표본 8개 중 5개가 한 줄(높이 약 25), 긴 이름만 두 줄. 160에서 Story 첫 버튼은 폭 146으로 두 줄.
- 사용자 규칙 구현/설치됨: 공유 원본 .claude/codex-bridge/USER_RULES.md, C PC ~/.claude/CLAUDE.md 가져오기 설치, Claude 점검 콘솔 COLLAB_READY·사용자 공통 규칙 설치됨. 다른 PC Pull 후 Test-CollabSetup.ps1 -WriteLocalConfig -InstallUserRules. 드론 전용 추가 규칙은 Unreal CLAUDE.md. 다른 PC 실제 설치는 확인 대기.
- 수동 확인 대기: 1280/1920 실제 화면 가독성·Story 목록 상시 스크롤바 칸(변경 없음). 이 범위 미구현 없음. 스토리 충돌·레이싱 방식 현재 미정. 과거 이력 보존, 다른 카드 상태 변경·새 파일·Unreal 수정·Commit/Push 없음.
- Drone Space: 진행상황과 다음 작업의 UI-LAYOUT-01 후속 검증 완료 관련 3개 연산 적용, 저장 후 재조회 본문 일치 확인. 다른 페이지 변경·새 Page 없음. 이번 대상 미반영 없음.

- 2026-10-01 저녁 후속(C PC): 결정·지시 Claude, 문서 반영 Codex. Unreal HEAD `ec2e88f`·`.claude/` 전체 Git 미추적(지시서 기준), md 로컬 미커밋. 협업·세팅·사용자 규칙 원본 3개를 md `docs/git/CLAUDE_CODEX_SETUP.md`·`CLAUDE_CODEX_COLLABORATION.md`·`USER_RULES.md`로 경로만 조정해 이동하고 목록·협업 링크·문맥 안내·SYNC-COLLAB-01에 반영. 엔진 검증 미실행/해당 없음, Space 제외. Unreal 원본 안내 전환·설치 스크립트의 md USER_RULES 참조는 Claude 후속 작업. Commit/Push 없음.


## 2026-10-01 밤 — Shotgun 시험 정정·미션 Catalog 자동 등록

- 기준: C PC Unreal HEAD `ec2e88f`(Codex 읽기 전용 Git 확인) + 미커밋 `DroneFrontEndRootWidget.{h,cpp}`, `DroneGameFlowSubsystem.cpp`, `Drone.Build.cs`, `DroneTutorialHoverPIETest.cpp`, `DroneShotgunSystemsTestMapTest.cpp`, `DroneGameFlowContractTest.cpp`, `DroneFrontEndContractTest.cpp`, `DroneFrontEndPIETest.cpp`, 새 `Flow/Tests/DroneCatalogAutoRegistrationTest.cpp`(파일 목록은 Claude 지시서). md 로컬 미커밋. 작업 도구 Claude, 문서·Space 반영 Codex.
- `AI-SHOTGUN-REGRESS-01` → **Shotgun PIE 시험 장면 수정 / 자동 검증 완료**. 사용자가 2026-10-01 실기에서 Shotgun 감지 정상을 확인했다. Claude가 자동화 실패를 실제 감지 회귀로 넓혀 쓴 잘못된 서술을 정정한다. 실패는 시험 장면의 Drone이 NPC에서 8.8m·정면 약 93° 옆(기본 시야 반각 70° 밖)에 정지하고 NPC도 대기해 5초 동안 감지되지 않은 것이었다. RenderOffScreen에서도 동일하므로 NullRHI 문제가 아니다. 사격 단계의 Drone을 NPC 정면 min(900cm, 사거리−100)·높이 150cm에 고정하는 시험만 수정했고 AI 코드는 바꾸지 않았다. 수정 후 NullRHI Shotgun 관련 5개 5/5 Success. 9/18 이후 어떤 9/22·9/29 변경이 NPC 회전에 영향을 줬는지는 미확인.
- 구현됨·자동 검증됨: `EnsureDefaultCatalog`는 C++ 기본 목록 Drone 5·Mission 14를 먼저 등록한 뒤 `/Game/Drone/Data/Drones`·`/Game/Drone/Data/Missions`의 하위 폴더까지 Asset Registry로 탐색해 미등록 Definition을 추가한다. 새 미션 DA는 지정 폴더에 만들면 C++ 수정 없이 로비에 등록된다. 잘못된 DA·ID 중복은 기존 Catalog를 유지하고 `LogDrone` 경고만 남긴다. 로비는 MissionId 알파벳순, Runtime `AssetRegistry` 의존성 추가.
- 자동 검증(2026-10-01 밤, C PC, Claude): Editor 종료 후 Build Succeeded. Flow 전체 + Mission 전체 + HoverMissionPIE + IndependentMapEntryPIE **15/15 Success**(CatalogAutoRegistration 포함). 렌더 전용 `LobbyLayoutStabilityPIE`는 이번 NullRHI 로그에서 Fail·samples=0이나 화면 표본이 없어 판정 불가이며 15/15 대상에서 제외한다. 앞선 렌더 Success와 구분한다. 미션 14·버튼 4/9/1 고정 비교는 하한 비교로 바꿨다. 새 검사는 두 폴더의 모든 Definition이 같은 Asset으로 등록됨·폴더 밖 Mission 없음·재호출 개수 유지를 확인한다.
- 근거: `Saved/Automation/ClaudeShotgunFix/test.log`, 수정 전 `ClaudeShotgunRender/render.log`(RenderOffScreen 1280×720 Fail), `ClaudeCatalog/build.log`·`test.log`. Codex가 관련 코드·성공 로그를 읽기 전용으로 대조했으며 Build·PIE를 재실행하지 않았다.
- 수동 확인 대기: 새 DA를 하나 만들어 실제 로비에 뜨는지, 1280/1920 로비 가독성. 미구현: 패키징 쿠킹 설정(`BUILD-PACKAGE-01`), 체크포인트/리스폰(`MISSION-CHECKPOINT-01`), HUB 보이스·자막/1회 시네마틱(`MISSION-BRIEFING-02`), HUD·기체별 배터리(`HUD-FIGMA-01`). Story M1~4 콘텐츠 후보는 `STORY-TEST-01`에 합쳤다. 스토리 충돌·MANPADS/베일 표기·레이싱 맵/코스 방식은 현재 미정.
- 근거 지시서: `.claude/codex-bridge/runs/20261001-215610-docs-docs-mission-catalog/prompt.md`. WORKBOARD 신규 4개 카드·STORY-TEST-01 통합·TEST-NPC-COUNT-01 하한 비교 참고 반영. 기존 날짜별 기록과 Codex 표기 보존. Unreal 쓰기·Editor/Build/PIE·Commit/Push·Trello/Figma 수정 없음.
- Drone Space(2026-10-01 밤): 기존 「진행상황과 다음 작업」 6개 연산(Shotgun 정정·Catalog 자동 등록·남은 카드 요약), 「Blueprint 조정과 팀원 가이드」 1개 연산(미션 연결·설정 위치 표)을 저장 후 재조회했다. 총 7개 연산 적용, 거부 없음. 두 페이지에서 기대 본문·표 일치를 확인했으며 이번 대상 미반영 없음. 나머지 페이지·기획·새 Page·공유 권한은 변경하지 않았다.
- 로컬 검증: git diff --check 통과, 카드 ID 중복 없음·설정 위치 표 11개 항목 대조. 최종 git status --short로 기존 미커밋 변경을 보존한 이번 대상 4개 파일을 확인했다.

## 2026-10-01 밤 후속 — UI-PAD-01·MISSION-CHECKPOINT-01 문서 반영

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


## 2026-10-02 새벽 후속 — TUT-PROGRESS-01·스토리 순서 연결

- 기준: C PC Unreal HEAD `ec2e88f` + 로컬 미커밋, 작업 도구 Claude·문서/Space 반영 Codex. 구현·검사 조건은 Claude 지시서 근거이며 Codex는 HEAD와 지정 전체 회귀 로그의 결과를 읽기 전용 대조했다. Build·Editor Python·PIE·맵 생성·수동 검증은 이번 문서 작업에서 실행하지 않았다.
- `TUT-PROGRESS-01`: **구현됨·자동 검증됨·수동 확인 대기**. Mission DA `NextMissionId`로 호버→전진→회전→게이트→자폭(FPV)→드랍(Payload)→UGV NPC→포탑(끝)을 연결했다. Story는 Figma 번호 M1 골든타임→M2 인터셉트→M3 베일브레이커→M4 엔드게임(끝), 공용 Training·Racing은 연결 없음. Editor Python으로 DA 12/12 저장·재조회(exit 0), 맵 미수정(ClaudeTutProgress/py.log·py2.log). Story 연결은 순서만 정하며 M2→M3 결과 분기는 현재 미정이다.
- `UDroneGameFlowSubsystem`이 성공 결과에서만 `RequestNextMission`으로 FrontEnd의 다음 수업 브리핑(MissionTrailer)을 열고 [출격]하면 해당 맵으로 이동한다. GetNextMissionId/GetMissionSequence(고리 방어)/GetMissionSequencePosition/IsMissionCompleted/GetMissionIdsInLobbyOrder, RequestReturnToLobbyFocusing·RequestReturnToTitle 연결. Snapshot `CompletedMissionIds`는 이번 실행 동안만 유지(영구 저장 현재 미정), `LastMissionElapsedSeconds`는 Director가 World 시간으로 계산한 출격~결과 시간(재출격 포함), 공개 GetMissionElapsedSeconds(). Widget이 시간을 재지 않는다.
- 결과 `UDroneMissionResultWidget`이 S48/S49를 담당한다. 수업 완료는 “훈련 완료”·수업 이름·“시간 mm:ss.cc”·“수업 n/8 | 완료 c/8”, [다음](패드 첫 포커스)·[다시하기]·[작전 로비로 복귀](Figma에는 없지만 유지). 8개 모두 완료는 “훈련 완료”·“이제 운용 할 준비가 되었습니다.”·“수업 8/8 모두 완료”, [미션 진행](로비 미션 탭 M1)·[시작 메뉴](../gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md), [다시하기] 숨김. Story 등은 “미션 성공”·“클리어 시간”·“미션 n/4 | 완료”·[다음 미션: 이름], 실패는 “진행 시간”과 첫 포커스 [다시하기].
- 로비 튜토리얼은 수업 순서(호버 맨 위·공용 Training은 그 뒤), 미션은 M1→M4. 이번 실행 성공 미션 이름 뒤 “· 완료”, 설명에 “수업 n/8 (완료 c)”/“순서 n/4”. Tutorial Text 6개와 선택 WBP 이름은 튜토리얼 가이드 5절에 정리했다.
- 자동 검증(Claude, C PC, RenderOffScreen 1920×1080, `C:\URproject\drone\Saved\Automation\ClaudeTutProgressFull\test2.log`): 신규 `Drone.Flow.TutorialProgression`·`TutorialNextLessonPIE`·`TutorialCompletePIE` **3건 Success**. 순서/위치/고리 방어·실패 시 다음 불가·8개 연속 다음·시간/완료 8/8·타이틀·로비 정렬·M1 포커스, 실제 호버 클리어→S48→전진 브리핑을 검증했다. 전체 완료 PIE는 나머지 7개를 테스트용 완료 처리한 뒤 호버 클리어→S49를 검사했으며 실제 8수업 수동 완주 근거는 아니다.
- 최신 전체 `Drone.*` 렌더링 회귀: **87개 중 81 Success·6 Fail**(같은 로그). NPCPerceptionSearchPIE=기존 AI-PERCEPTION-TEST-01, TrainingAssets·TrainingPIESmoke=기존 팀원 Production 맵, ShotgunSystemsTestMapPIE=렌더링 실행에서만 실패/NullRHI 통과(`AI-SHOTGUN-RENDER-01`), LobbyLayoutStabilityPIE=실행마다 첫 프레임 높이·판정 변동(10/01부터 관찰, `UI-LAYOUT-DIAG-01`), TrainingRouteSelectionPIE=전체 렌더링 회귀에서만 숫자키 미반영(`TEST-ORDER-ROUTE-01`). Route는 최대 30프레임 대기에도 Route 1 유지, 단독·패드 테스트 뒤·Training Smoke 뒤 Success이며 원인 선행 테스트 미특정. 전체 Pass로 확대하지 않는다.
- 테스트 정리(기능 변경 아님): GamepadMissionFlowPIE는 호버 최상단에 맞춰 ↓ 탐색을 보정하고 결과 검사 동안만 호버 DA를 메모리에서 결과 화면 모드로 변경(저장 안 함). TrainingRouteSelectionPIE는 숫자키 대기를 1→최대 30프레임으로 변경했다.
- 수동 확인 대기: 결과 화면 배치·글자, 실제 8개 연속 진행 체감, 로비 “· 완료” 가독성, 전체 완료 뒤 [미션 진행]·[시작 메뉴]. 현재 미정: 완료 영구 저장, Figma 미기재 조작키 브리핑 문구/화자, 4-1·4-2 통합, M2→M3 결과 분기. Figma에 패드 브리핑 원문이 있는 호버·전진·회전·게이트 4개와 달리 자폭·드랍·UGV·포탑은 키/대사가 없으며 튜토리얼 조작키 브리핑은 넣지 않았다.

- Drone Space(2026-10-02 새벽 후속): 기존 진행상황과 다음 작업 3개·테스트 맵과 확인 가이드 1개·Blueprint 조정과 팀원 가이드 2개 연산 저장(총 6개, 거부 없음). 세 페이지 저장 후 재조회에서 구현/Story 순서·87개 판정·수동 절차·NextMissionId/Tutorial Text 6개/선택 WBP 이름의 기대 본문 7개가 모두 일치했다. 이번 대상 미반영 없음. 새 Page·Commit/Push·Unreal 쓰기·Build/PIE/맵 생성·Trello/Figma 수정은 하지 않았다. GitHub 로컬 MD 본문은 사용자 Commit/Push 후 반영된다.

- 문서 반영(Codex): STATUS 최신 절/10-01 밤 미구현 줄 후속 표시, WORKBOARD TUT-PROGRESS-01·문구/영구 저장·진단 3건 카드와 Next 순서, 튜토리얼 가이드 5절 S48/S49·설정·Figma 미기재 목록, Mission 프레임워크 NextMissionId·Story 순서 갱신. 기존 Codex/Claude 과거 이력은 보존하고 이 수행 이력을 끝에 추가했다. Figma 조사 근거는 2026-10-02 Codex research runs/20261002-003829-research-research-tutorial-controls/result.md이며 원본 수정·수치/기획 확정은 하지 않았다.

## 2026-10-03 — 회의 후 UI/DA 점검과 문서 정합성 (Codex)

C PC Unreal main5b03ad3/원격41444c2(2커밋 뒤)·md250e975, 시작 두 Clean. Library 체크리스트/ASR 대조회의록을 읽고 최신 역할(Codex BP/UI, Claude C++)을 적용. 레이싱 DA 설명의 Best Lap 미구현 문구 한 곳을 정정하고 12개 비UI 속성 동일·DA 유효성을 확인했다. 로컬14개 DA·8수업/Story4 순서/실패 실제값 확인, 기존 결과/브리핑/JSON저장 기반은 재구현하지 않음. UI 설명 독립 Editor 재로드 통과. Codex 직접 집중 회귀 FrontEndContract·TutorialProgression·BestLapPersistence 3/3 Success(기존 바이너리, NullRHI/NoSound, 종료0·오류0·Best Lap 손상/구버전 복구 경고2; focused_regression/index.json). 맵/C++/WBP/Production은 미수정; 실제5메뉴·패드 표시/장치/맵3 수동은 대기.

5메뉴/C++ 인터페이스와 미정 결정표를 WORKBOARD에 남겼다. 메인컴 드론 Claude 세션 idle은 공식CLI로 확인했지만 CLI 미로그인으로 실제 전달/응답 없음. 비공개 세션 JSON 읽기는 자동 승인 검토가 민감한 세션 자료 노출 위험으로 거부했으며 실행/우회하지 않았다. 별도 인증·세션 재개/중복제출·Push/배포/Figma/Trello 수정 없음. Drone Space 진행/테스트/BP 3개 페이지는 미반영: 진행 페이지 쓰기를 자동 승인 검토가 외부 저장 대상/자료의 명시적 승인 부족으로 거부해 후속 쓰기를 중단했다. 기존 진행 본문 미변경을 읽기 재확인했으며 검토 가능한 초안은 작업폴더 drone_space_pending_patch.json에 보관. 이전 기록 보존, 백업·SHA/새 검증 로그는 작업폴더에 보관.

## 2026-10-03 C PC 추가 UI 준비·진단 — 핵심 연결 대기

전체 요청은 **부분 완료**다. 레이싱 DA의 Best Lap 설명과 문서 정합성 수정을 마쳤고, 아래 신규 UMG 두 개를 준비·저장했다. 기존 `WBP_DroneFrontEndRoot`/`WBP_DroneFlightHUD`, C++, 맵, 설정은 바꾸지 않았다. 신규 위젯은 아직 제품 호스트에 참조·연결되지 않았다.

| 준비한 로컬 에셋 | 실제 내용 | 남은 연결 |
|---|---|---|
| `/Game/Drone/FrontEnd/UI/WBP_DroneFiveItemMenu` | 스토리/레이싱/튜토리얼/설정/종료 순서의 텍스트 버튼 5개, 상하 Explicit 포커스 이름 참조, 클릭 요청 Dispatcher 5개+Back, `FocusFirstItem`/`RequestBack` | C++의 현재 4버튼 호스트·카테고리 진입·뒤로가기와 연결 필요 |
| `/Game/Drone/Prototype/UI/WBP_DroneControlInputDisplay` | 좌우 스틱 UI, `UpdateStickAxes(LeftX,LeftY,RightX,RightY)`의 [-1,1] 클램프/화면 Y 반전, `SetControlInputDisplayVisible(Show)` | Settings 상태·실제 입력 축·HUD 장착 필요. 고도계는 독립이며 전역 기본값/자동 전환 정책은 미정 |

공개 Unreal `ToolsetRegistry`를 통해 실제 WBP Designer/그래프를 확인하고 편집했다. 기존 타이틀 WBP Designer는 0개 위젯이며 native fallback 4메뉴를 사용한다. 기존 비행 HUD Designer는 8개 위젯이고 입력 표시/토글 BP 변수는 없다. 이전 일반 Python API 실패를 BP 편집 도구 부재로 확대 해석하지 않는다. 신규 메뉴의 runtime-only 포커스 참조가 저장되지 않는 문제는 Designer `WidgetToFocus` 이름 참조로 교정했다.

검증: UE 5.8 새 에디터 재로드·경고를 오류로 처리한 BP 컴파일, 정확한 5메뉴/버튼/포커스/클릭 실행 연결/Dispatcher/함수/고도계 독립/저장 SHA **19/19 Pass**. `WidgetLibrary.create`가 Python에 노출되지 않아 위젯 함수 실제 실행은 미실행. 화면 렌더·PIE·실제 패드/혼합 입력/분리·재연결·제품 맵3 완주/복귀는 미검증. 앞서 기존 바이너리 focused 회귀는 3/3 Success이며 신규 UI 제품 연결의 검증으로 간주하지 않는다.

Claude 인계 진단: `C:\URproject\drone`의 idle Code 세션 `fd8b6237-e858-42e3-b584-d1ffaafa940f`(표시명 “대화 내용 수집”, PID33636)는 Claude Desktop PID8872가 관리하는 stream-json/stdio 자식이다. 별도 CLI `loggedIn=false`는 Desktop 로그아웃 증거가 아니다. 현재 Codex 실행 도구에는 기존 Claude UI 입력용 `node_repl/@oai/sky`나 세션 전송 connector가 없다. 공식 `agents --json`은 읽기 목록 경로이고 help에 기존 대화 메시지 전송 명령은 없다. **C++ 인계 미전달/미시작**. 사용자가 기존 Claude Desktop→Code의 위 드론 세션에 작업 폴더의 `claude_drone_cpp_handoff.txt`를 붙여넣으면 정상 기존 UI 경로로 전달할 수 있다. 토큰/키/사적 세션 원문은 읽거나 복사하지 않았고 resume/attach/중복 세션은 실행하지 않았다.

원격 읽기 비교: drone 로컬 `5b03ad3` 대비 원격 main `41444c2`의 2커밋은 훈련맵/게이트4개/산악맵 6파일이며 DA·신규 UI·C++과 직접 경로 충돌 없음. MD 원격은 `250e9758`로 로컬과 같다. 6개 LFS 원격 본문 모두 로컬 캐시 없음, 게이트4개 로컬 파일 없음. 최신 원격 맵의 런타임 검증은 미실행이며 다운로드·pull·merge·checkout·reset은 하지 않았다.

Space 동기화는 최신 요청에서 제외했다. 기존 Space 쓰기 자동 승인 거절 후 재시도/권한 우회하지 않았다. 로컬 신규 위젯은 `remove_drone_ui_components.ps1` 기본 Preview로 확인 후 필요할 때만 `-Apply`로 제거할 수 있으며 후속 수정 SHA가 다르면 중단한다. 원래 DA+MD8 복구는 `restore_drone_meeting_changes.ps1` 기본 Preview/선택적 `-Apply`; 최초 원본 백업을 유지한다.


## 2026-10-03 밤 — 5메뉴·조종 입력 표시·레이싱 숫자키 연결 완료

- 기준: Asia/Seoul 2026-10-03 밤, C PC Unreal HEAD `5b03ad3` + 로컬 미커밋. 원격 2커밋(Training.umap·MountainRange.umap·Gate 4개)은 LFS 대용량으로 미수신. C++·Build·자동화 테스트는 Claude, BP 연결 스크립트는 Codex(ui run `20261003-225410-ui-ui-menu5-inputdisplay`) 작성 후 Claude 실행·검증, 문서·Space는 Codex 담당이다. Codex는 HEAD·지정 회귀 로그를 읽기 전용 대조했으며 이번 문서 작업에서 Unreal 쓰기·Build·PIE·맵 생성·수동 검증을 실행하지 않았다.
- **5메뉴 구현됨·자동 검증됨·수동 확인 대기**: 스토리·레이싱·튜토리얼·설정·종료 순서. `OpenLobbyForCategory`/`OpenStoryLobby`/`OpenRacingLobby`/`OpenTutorialLobby`가 진입 전 분류를 지정해 중간 시작 화면 없이 첫 목록·포커스를 만든다. `RequestExitGame`, 기존 `FinishOpeningTrailer`(스토리)·`OpenTrainingLobby`(튜토리얼)는 호환 유지. `TitleMenuClass`의 5버튼/요청 Dispatcher 계약 오류는 `[TITLE-MENU]` 경고와 기본 5버튼으로 대체. `GetTitleButton`·Title*Index는 0~4, 설정 복귀는 3, 로비 복귀는 진입 메뉴, 맵 이동 후 새 화면은 마지막 분류 메뉴. 상하 순환·B/Esc 반복 한 화면 Back. 로비 Tutorial/Racing 탭·LB/RB는 유지하며 최종 유지 여부는 현재 미정이다.
- **조종 입력 표시 구현됨·자동 검증됨·기본값 미정**: 설정 “조종 > 조종 입력 표시”(`ControlInputDisplayCheck`), 적용/취소/기본값 복원 구조 유지. 기존 음량 SaveGame에 `bHasControlInputDisplayChoice`·`bControlInputDisplayEnabled` 저장, 사용자 선택 우선. `DefaultGame.ini`의 `[/Script/Drone.DroneAudioSettingsSubsystem] bControlInputDisplayEnabledByDefault=False`는 결정 전 임시 끔이다. 기본값 복원→적용은 선택을 지워 이후 기본값을 따른다. 자동화는 `DroneAudioSettings_Automation` 슬롯으로 실제 설정 보호.
- `GetControlInputSnapshot()`(BlueprintPure)은 스틱 물리 위치 X 오른쪽+, Y 위+, [-1,1]. 쉬운/실제 조작형 왼쪽 이동·오른쪽 X 회전/Y 카메라·트리거 고도, Acro Mode 2 왼쪽 Yaw/스로틀·오른쪽 Roll/Pitch, Mode 1 왼쪽 Yaw/Pitch·오른쪽 Roll/스로틀, 지상 왼쪽 조향/전후. 키보드도 같은 액션 위치로 보인다. 장치 구분·자동 전환·혼합 입력·분리/재연결 정책은 현재 미정, 입력 바인딩/매핑 추가 없음. HUD는 아래 가운데 입력 위젯을 붙여 설정 ON·기체 존재 시만 Visibility/축 함수를 호출하고 고도계·다른 HUD는 독립 유지한다.
- **BP 연결 저장·자동 검증됨**: `WBP_DroneFrontEndRoot.TitleMenuClass = WBP_DroneFiveItemMenu`, `WBP_DroneFlightHUD.ControlInputDisplayClass = WBP_DroneControlInputDisplay`. 두 자산만 BS_UP_TO_DATE 컴파일·저장(ClaudeMenu5/wire.log). BP 최초 로드 시 부모와 다른 값만 인스턴스로 복사하므로 테스트의 메모리 Class Defaults 덮어쓰기를 연결 증거로 삼지 않고 실제 저장된 연결을 검사했다. 이전 `C:\Users\jkw11\Documents\Codex\2026-10-03\task-2\claude_drone_cpp_handoff.txt`의 5메뉴·설정/축/HUD **남은 C++ 연결은 이번 결과로 닫음**. 원본 인계문은 과거 기록으로 보존, 맵3·실기 검증은 남는다.
- **레이싱 숫자키 보호 구현됨·자동 검증됨**: 현재 제품 Racing `TestMap/Lvl_DroneRacingTest`에는 RouteSelector가 없어 숫자키 노출 없음. `bAllowPlayerRouteKeys=true`·`bBlockRouteKeysInRacingMissions=true` 보호로 로비 Racing 미션은 1~5 바인딩·안내 숨김. 시험맵 직접 실행·튜토리얼·훈련·스토리는 기존대로, 랜덤 포함 경로 전환 기능 보존. 원격 맵3 완주/복귀는 LFS 미수신으로 **미실행**.
- **MCP C PC 설정 완료(Claude 지시서)**: 엔진 내장 ModelContextProtocol 플러그인은 켜져 있으나 서버 자동 시작 기본 꺼짐. Git 제외 `Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini`의 `[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings] bAutoStartServer=True`로 다음 Editor 실행부터 `localhost:8000/mcp` 자동 시작, 현재 Editor는 `ModelContextProtocol.StartServer`. 엔진 HTTP 기본 바인드 localhost. 다른 PC 적용/실제 연결은 별도 확인 대기, 팀 공유 설정에 넣지 않는다.

### 검증 출처 — Claude 실행, C PC

| 검사 | 결과·조건 | 근거 |
|---|---|---|
| Build | Editor 종료 후 Succeeded(지시서 근거) | Claude 결과 지시서 |
| Flow+UI+Prototype+Tutorial.TrainingRoute | RenderOffScreen 1920×1080, 실제 저장 BP 연결, **33/33 Success** | `C:\URproject\drone\Saved\Automation\ClaudeMenu5\test2.log` |
| TitleFiveMenuPIE / TitleFiveMenuWidgetPIE | native 5문구·각 분류/첫 목록·메뉴 복귀 포커스·설정3·재입력 무시, 저장된 BP 버튼→Dispatcher로 같은 흐름 Success. 종료 Dispatcher 연결만 확인, 누르지 않음 | 같은 로그 |
| GamepadNavigationPIE / GamepadMissionFlowPIE | 패드 키 주입·5메뉴 WBP, 위↑ 순환·Racing 직접 진입/복귀·Tutorial 호버 비행/결과/복귀 Success | 같은 로그 |
| ControlInputDisplayPIE | Lvl_DronePrototype 패드 축 주입, ON 표시·왼쪽 위 -38px·해제 중심·오른쪽 X +38px·오른쪽 위+·Acro Mode 1/2·OFF 숨김/갱신 중지·비행 HUD 유지 Success | 같은 로그 |
| SettingsContract / FrontEndContract / FrontEndPIE / FlightHUDTelemetryBinding / TrainingRouteKeyPolicy | Success | 같은 로그 |
| 전체 Drone.* | RenderOffScreen **91개 중 86 Success·5 Fail**, 전체 Pass 아님 | `C:\URproject\drone\Saved\Automation\ClaudeMenu5Full\test.log` |

- 기존 Fail 5개: NPCPerceptionSearchPIE(`AI-PERCEPTION-TEST-01`), ShotgunSystemsTestMapPIE(렌더링에서만), LobbyLayoutStabilityPIE(진단·변동), TrainingAssets·TrainingPIESmoke(팀원 Production 맵). `TEST-ORDER-ROUTE-01`의 TrainingRouteSelectionPIE는 이번 전체 회귀 Success이나 순서 의존 원인 미특정·해결 확정 아님.
- **수동 확인 대기**: 실제 패드 5메뉴/입력 표시 체감, 1280/1920 메뉴 크기·입력 표시 위치, Bluetooth 분리/재연결·혼합 입력, 제품 맵3 완주/복귀. **현재 미정**: 입력 표시 기본값·장치 자동 전환·혼합/재연결 정책, 로비 탭/LB·RB 유지, M2 결말, M3·4 수량/규칙, 캐릭터 메시, 고도계 토글(확정 요구 아님), 회의4개 vs 문서8수업. 기존 사람 기획/디자인·날짜별 기록·Production 맵 보존.

## 2026-10-03 밤 후속 — 5메뉴·조종 입력 표시 Space 반영 마무리 (Codex)

- run `20261003-231705-docs-docs-menu5-space` 지시서와 직전 `briefs/20261003-docs-menu5-inputdisplay.md`를 UTF-8로 읽고 로컬 미커밋 MD 10개 diff를 대조했다. STATUS·WORKBOARD·타이틀/Blueprint 가이드·SETUP·WORKLOG에 5메뉴/설정·축/HUD 연결, 레이싱 키 보호, 33/33·전체91개 중86 Success/기존5 Fail, 기본값/정책 미정·수동 대기가 반영돼 있었다. 흐름 계획의 현재 절에 남은 “연결 구현 대기” 한 문장만 구현됨·자동 검증됨·수동 대기로 보완했다. 과거 Codex/Claude 이력은 보존했다.
- 추가 사실(Claude 실행·지시서 근거, 2026-10-03 밤 C PC): 사용자 Editor `Lvl_DroneFrontEnd` MCP 서버 응답·Claude `unreal-mcp` 연결 완료. Claude가 MCP PIE로 캡처한 타이틀에서 저장된 `WBP_DroneFiveItemMenu`(스토리·레이싱·튜토리얼·설정·종료)가 로고 아래 왼쪽에 표시되고 첫 [스토리]에 패드 포커스 강조, Editor 로그 `[TITLE-MENU]`·`[INPUT-DISPLAY]` 경고·오류 없음. 약560px 폭 Editor 뷰포트 캡처여서 실제1280/1920 배치·실제 패드 체감은 수동 대기. 입력 표시는 임시 기본 꺼짐(최종 기본값 현재 미정)이므로 사용자가 설정 ON→적용 후 비행에서 확인할 항목이다. STATUS에 짧게 추가하고 WORKBOARD MCP-LOCAL-01의 현재 연결 상태를 갱신했다. Codex가 Build/PIE/수동 검증을 실행한 것이 아니다.
- Drone Space: 진행상황과 다음 작업·테스트 맵과 확인 가이드·Blueprint 조정과 팀원 가이드 모두 직전 내용이 이미 저장된 것을 현재 본문으로 확인했다. 중복 추가 없이 기존 관련 블록 1개씩 추가 사실을 보완(총3개 연산, 모두 적용·거부 없음). 저장 후 content 스트림 전체 재조회로 기대 본문 정확 일치와 나머지 기존 블록 원문 보존을 3/3 확인했다(진행 sequence15, 테스트9, BP9). 이번 대상 미반영 없음. 입력 표시·실제 해상도 수동 Pass로 확대하지 않았다.
- 새 파일/Page·Commit/Push·Unreal 저장소 쓰기·Build/PIE/맵 생성·Trello/Figma 수정·공유 권한/예약 자동화 변경 없음. 로컬 미커밋 MD의 GitHub 반영은 사용자 Commit/Push 후이며 기존 수동 대기·미정·전체 회귀5 Fail은 유지한다.

## 2026-10-04 STATUS 정리 — 10월 세션·기존 요약 원문 보존 (Codex)

아래는 정리 전 STATUS의 10/01 이후 세션과 기존 한눈에 보기·Git 요약 원문이다. 당시 미수신·연결 대기는 당시 상태이며 최신 10/04 판정은 다음 세션 기록과 STATUS를 따른다. 기존 Codex/Claude 표기를 보존했다. 9월 집계 네 절은 [원문 아카이브](archive/STATUS_2026-09.md)에 이동했다.

STATUS 원문과 중복 세션은 [10월 STATUS 아카이브](archive/STATUS_2026-10.md)에 그대로 보존했다.

## 2026-10-04 새벽 — Acro 회의 조사·입력/자세 수정·포커스 관찰 반영

- 지시서: `C:\URproject\drone\.claude\codex-bridge\runs\20261004-010254-docs-docs-acro-meeting-fix\prompt.md`를 UTF-8로 읽었다. 작업 도구: 조사·C++·Build·테스트·IMC headless 패치 Claude, Scout/Drop 입력6개 연결·BP 컴파일/저장 Codex(ui run 20261004-001325-ui-ui-acro-input-assets, Editor MCP)→Claude 확인, 이번 문서/Space Codex. C PC Unreal HEAD=추적 origin/main41444c2+로컬 미커밋을 Codex 읽기 Git 확인. 원격 pull·LFS 실제 파일 확인은 Claude 지시서 근거. 문서 HEAD250e975, 기존 미커밋10개 보존.
- 회의 조사 결론: Space 단독 자세 변화 경로 없음(Mode1/2×스로틀+1/0/-1·프레임 끊김 자동 확인). 키보드0.1초 탭=FPV 최대650°/s×시간 약65°·무수평복귀, W+Space 습관은 체감 원인 후보이며 수동 대기. 키보드 Mode1/2 동일, 패드세로축만 RC 표준 배치(Mode2 왼쪽스로틀/오른쪽피치·Mode1 반대). 회의 “좌우 스틱 반전” 뜻은 미정.
- 결함2건: Enhanced Input은 DefaultInput.ini 데드존을 쓰지 않으며 IMC Acro4축에 데드존 없어0.05쏠림이 키보드스로틀을 덮고 회전이 누적됨→동일 IMC 쉬운 조작값 Lower0.2/Upper1.0/Radial을 맨 앞 복사,33매핑/키/Action/순서 보존. Codex MCP Instanced Modifier 생성(None) 실패 후 저장 없이 복구→Claude Editor종료/headless Python IMC만 저장·재조회(patch_dz.log). Scout/Drop은6개 AcroAction None→Codex MCP로 FPV와 동일 연결·컴파일·저장. 최종 result.md는 모델 용량 오류로 없지만 Claude Python 재조회(assign_bp.log)·자동화로 확인. FPV/FiberOptic 기존 연결·UGV 제외.
- 정확도(C++): ADronePrototypePawn::UpdateControlAttitude 1차 응답 정확 적분 `Target·dt+(Start−Target)·τ·(1−e^(−dt/τ))`, 피치/요/롤 단일 축-각 합성으로30/60/240fps 자세 일치. 기존 FlightProfile.AcroRateSettings 응답시간/최대각속도 유지. BuildDroneAcroInput.py는4축 데드존 복사·FPV/Scout/Drop/FiberOptic6개 입력 연결을 생성하도록 Claude 변경, 이번 도구 미실행.
- 새 자동화3개: AcroAttitude(Space 불변·0.1초 탭·FPS/Mode 동일), AcroInputBehaviorPIE(실제 키/축 주입·Mode배치·쏠림 보호), AcroInputAssetContract(비행BP4종/DeadZone4개). Build Succeeded는 Claude 지시서(별도 Build 경로 미제공). Codex가 읽은 로그: Saved/Automation/ClaudeAcro/test_after_dz.log 집중12/12 Success, ClaudeAcroFull/test3.log 화면 그려진 전체94개 중90 Success·Fail4(NPCPerceptionSearchPIE·렌더전용 ShotgunSystemsTestMapPIE·Production TrainingAssets/TrainingPIESmoke). 전체 Pass/수동 Pass 아님.
- UI-FOCUS-RACE-01: UIOnly WidgetToFocus 루트의 엔진지연 처리가 버튼포커스를 가져가는 경쟁. FDroneGamepadFocus 5프레임 감시/루트·없음 이탈 복원, 다른 강조버튼 이동 보존. 화면 그려진 수정 전 final.log Fail·후 test3.log Success 각1회뿐이므로 수정 후 확인 중. 단독 혼재·실제 결과/타이틀 첫강조 수동대기. NextLessonPIE 실패에 강조/Slate위젯 이름 진단 추가.
- TEST-RENDER-UNPAINTED-01: 전체5회 중3회(test.log/test2.log/final2.log) samples=0·Shotgun렌더실패가Success·패드포커스6개 동반Fail, 판정 제외. -stdout/MCP포트와 무관·원인 미특정, Claude known-test-failures.md에 판정전 화면확인 기록. 같은증상 수정→검증2회 후 중단 유지, 사람/추가관찰 필요. TEST-ORDER-ROUTE-01은5회 모두 TrainingRouteSelectionPIE Success를 Codex 로그대조, 원인 미특정·해결확정 아님·3회 미렌더와 구분.
- 레이싱 pull뒤 조사(Claude): MWLandscapeAutoMaterial Island/MountainRange 계열 코스1개·PlayerStart없음. 아이템/Gate 자산 맵·DA 참조없음. 제품DA는 TestMap/Lvl_DroneRacingTest 유지, 연결지형·PlayerStart·완주/복귀는 사용자/팀원 결정필요, 맵미수정. RACING-TERRAIN-LINK-01 카드 추가·기존 RACING-MEETING-01 최신화.
- 수동대기: 실제 패드/키보드 Mode1/2 전환→Space단독→패드놓고Space→키보드0.1초탭/약65° 후 유지, Scout/Drop Acro비행, 결과/타이틀 첫강조. 현재미정: 키보드배율/Angle모드/마우스Yaw·회의반전뜻·입력표시기본값·로비탭·레이싱연결·Production Training2건. 기획/사람디자인·날짜별기록·팀원맵 보존.
- 로컬 문서: STATUS 최신요약/Git/검증·수동경계, WORKBOARD 관련카드/Next, Blueprint 조정 가이드6개입력/4축데드존/AcroRateSettings/재생성경계, 테스트가이드 수동순서/미렌더 판정 추가. 이번docs는 Unreal쓰기·Build/PIE/맵재생성·Commit/Push·Trello/Figma·권한/예약 변경 없음.
- STATUS 다이어트: 정리 전100,283바이트·386줄(LF분할, 마지막빈줄 포함)→정리 후12,653바이트·71줄(같은 기준). 2026-10-01이전 9월 집계 원문을 docs/history/archive/STATUS_2026-09.md로 이동한 절: 「최신 완료 항목」「검증된 근거」「아직 확인하지 않은 항목」「알려진 실패와 경계」. 기준일 이전 날짜가 본문에 있는 집계절이며 날짜제목절은 없었다. 10/01~10/03 세션/한눈/Git원문은 위 WORKLOG 정리절에 그대로 추가 보존하여 STATUS는현재요약만 유지. 네절원문 archive포함·나머지 STATUS원문 WORKLOG포함을 쓰기후검사했다. WORKBOARD 다이어트는 하지 않았다.

- Space 저장/재조회 완료: 기존 진행상황과 다음 작업 4개 연산(sequence16), 테스트 맵과 확인 가이드2개(sequence10), Blueprint 조정과 팀원 가이드2개(sequence10), 총8개 적용·거부없음. 진행/BP 기대 본문 정확일치, 테스트는 목록 블록 분할을 제외한 모든 원문줄/공백정규화 일치 확인. 비대상 기존 블록44/32/47개 각각 원문보존 확인. 새Page/권한/자동화 변경없음. 이번대상 미반영없음.
- 최종 git status --short 대조: 이번 작업6파일(STATUS·WORKBOARD·WORKLOG·DRONE_CODE_STRUCTURE_AND_USER_TASKS·DRONE_TEST_MAP_GUIDE·archive/STATUS_2026-09), 나머지 기존미커밋6개(타이틀가이드·SETUP·기획4개)는 이번에수정하지않음. git diff --check 통과(줄끝 자동변환 안내만 있음), 엔진검사 재실행없음. Claude후속은포커스/미렌더 관찰과사용자결정후레이싱연결이며 새코드수정미실행.

## 2026-10-04 후속 — Production Course 표시선 상한 읽기 조사

- 사용자 요청: BP_DroneTrainingCourse 92개 CurveAuto·약19.2km·256개 표시선 각짐을 UI보다 먼저 확인하고 기존 변경을 보존하며 최소 수정/실제 화면 검증. 실행 역할은 Claude, 이번 읽기 조사·문서/Space 담당은 Codex다. C PC Unreal HEAD41444c2 + 기존 미커밋/미추적을 확인했고 변경하지 않았다.
- 직접 확인: Course.cpp 고정 MaximumGeneratedSegmentCount=256, GetExpectedCourseLineSegmentCount의 min(ceil(length/target),256), Rebuild의 length/count 재분배. C++ 목표 기본200cm·기본 Engine Cube, 이전 TestMap 생성 스크립트100cm. 제보 길이가 계산 SplineLength와 같다면 조각약75m이며 목표100cm만 바꿔도 상한은 동일하다. 최종 각짐 원인은 실제 BP CDO/인스턴스·메시/스케일·화면 비교 전이라 유력으로 구분한다.
- Editor PID44680·127.0.0.1:8000 Listen 확인, 프로젝트 설정은 unreal-mcp HTTP 주소를 사용한다. 현재 Codex 노출 도구에는 Unreal MCP가 없고 플러그인 검색에서도 관련 연결을 찾지 못했다. 서버 Listen을 MCP 도구 연결·현재 인스턴스 조회·화면 Pass로 표시하지 않는다. 서버 호출/설정 변경·Unreal Python·Editor 종료/Build/PIE·Production 저장/재생성은 실행하지 않았다.
- TUT-COURSE-SMOOTH-01 카드와 Course 가이드에 Claude 인계를 작성했다. 실제 기본값/인스턴스/생성수 확인→별도 동일 경로 비교→상한 정책 최소 수정→긴 경로/비간섭/Gate 자동 회귀→동일 카메라 실제 렌더·비용 확인 순서다. 코드 최소 수정·새 자동화·수동 화면 검증은 모두 대기이며 Commit/Push·Trello/Figma·권한/예약 변경 없음. Space 반영 결과는 아래에 추가한다.
- Space 진행 Page의 코스 행/최우선 작업2건·BP 가이드 코스 설명1건 저장 후 재조회 정확 일치를 확인했다(sequence17/11). BP 문단 추가 patch는 topology_change로 미반영되어 재조회 후 한 문단 전체 교체로 수정했고 비대상 본문/링크는 보존했다. 새 Page·권한 변경 없음. 이번 반영 대상은 미반영 없음이며 실제 Unreal 인스턴스/수정/화면 검증은 여전히 대기다.


## 2026-10-03 UI 준비·진단 원문 보존 — 10/04 이관

10/03 당시 기록이며 같은 날 밤 제품 연결 완료로 대체됐다. **10/03 밤 제품 연결 이후 remove_drone_ui_components.ps1 사용 금지(실행 시 5메뉴·입력 표시 위젯 삭제, Git 미추적이라 복구 불가).** 아래 제거 안내는 역사 기록으로만 보존한다.

### WORKBOARD에서 이동한 원문

## 2026-10-03 C PC 추가 UI 준비·진단 — 핵심 연결 대기

전체 요청은 **부분 완료**다. 레이싱 DA의 Best Lap 설명과 문서 정합성 수정을 마쳤고, 아래 신규 UMG 두 개를 준비·저장했다. 기존 `WBP_DroneFrontEndRoot`/`WBP_DroneFlightHUD`, C++, 맵, 설정은 바꾸지 않았다. 신규 위젯은 아직 제품 호스트에 참조·연결되지 않았다.

| 준비한 로컬 에셋 | 실제 내용 | 남은 연결 |
|---|---|---|
| `/Game/Drone/FrontEnd/UI/WBP_DroneFiveItemMenu` | 스토리/레이싱/튜토리얼/설정/종료 순서의 텍스트 버튼 5개, 상하 Explicit 포커스 이름 참조, 클릭 요청 Dispatcher 5개+Back, `FocusFirstItem`/`RequestBack` | C++의 현재 4버튼 호스트·카테고리 진입·뒤로가기와 연결 필요 |
| `/Game/Drone/Prototype/UI/WBP_DroneControlInputDisplay` | 좌우 스틱 UI, `UpdateStickAxes(LeftX,LeftY,RightX,RightY)`의 [-1,1] 클램프/화면 Y 반전, `SetControlInputDisplayVisible(Show)` | Settings 상태·실제 입력 축·HUD 장착 필요. 고도계는 독립이며 전역 기본값/자동 전환 정책은 미정 |

공개 Unreal `ToolsetRegistry`를 통해 실제 WBP Designer/그래프를 확인하고 편집했다. 기존 타이틀 WBP Designer는 0개 위젯이며 native fallback 4메뉴를 사용한다. 기존 비행 HUD Designer는 8개 위젯이고 입력 표시/토글 BP 변수는 없다. 이전 일반 Python API 실패를 BP 편집 도구 부재로 확대 해석하지 않는다. 신규 메뉴의 runtime-only 포커스 참조가 저장되지 않는 문제는 Designer `WidgetToFocus` 이름 참조로 교정했다.

검증: UE 5.8 새 에디터 재로드·경고를 오류로 처리한 BP 컴파일, 정확한 5메뉴/버튼/포커스/클릭 실행 연결/Dispatcher/함수/고도계 독립/저장 SHA **19/19 Pass**. `WidgetLibrary.create`가 Python에 노출되지 않아 위젯 함수 실제 실행은 미실행. 화면 렌더·PIE·실제 패드/혼합 입력/분리·재연결·제품 맵3 완주/복귀는 미검증. 앞서 기존 바이너리 focused 회귀는 3/3 Success이며 신규 UI 제품 연결의 검증으로 간주하지 않는다.

Claude 인계 진단: `C:\URproject\drone`의 idle Code 세션 `fd8b6237-e858-42e3-b584-d1ffaafa940f`(표시명 “대화 내용 수집”, PID33636)는 Claude Desktop PID8872가 관리하는 stream-json/stdio 자식이다. 별도 CLI `loggedIn=false`는 Desktop 로그아웃 증거가 아니다. 현재 Codex 실행 도구에는 기존 Claude UI 입력용 `node_repl/@oai/sky`나 세션 전송 connector가 없다. 공식 `agents --json`은 읽기 목록 경로이고 help에 기존 대화 메시지 전송 명령은 없다. **C++ 인계 미전달/미시작**. 사용자가 기존 Claude Desktop→Code의 위 드론 세션에 작업 폴더의 `claude_drone_cpp_handoff.txt`를 붙여넣으면 정상 기존 UI 경로로 전달할 수 있다. 토큰/키/사적 세션 원문은 읽거나 복사하지 않았고 resume/attach/중복 세션은 실행하지 않았다.

원격 읽기 비교: drone 로컬 `5b03ad3` 대비 원격 main `41444c2`의 2커밋은 훈련맵/게이트4개/산악맵 6파일이며 DA·신규 UI·C++과 직접 경로 충돌 없음. MD 원격은 `250e9758`로 로컬과 같다. 6개 LFS 원격 본문 모두 로컬 캐시 없음, 게이트4개 로컬 파일 없음. 최신 원격 맵의 런타임 검증은 미실행이며 다운로드·pull·merge·checkout·reset은 하지 않았다.

Space 동기화는 최신 요청에서 제외했다. 기존 Space 쓰기 자동 승인 거절 후 재시도/권한 우회하지 않았다. 로컬 신규 위젯은 `remove_drone_ui_components.ps1` 기본 Preview로 확인 후 필요할 때만 `-Apply`로 제거할 수 있으며 후속 수정 SHA가 다르면 중단한다. 원래 DA+MD8 복구는 `restore_drone_meeting_changes.ps1` 기본 Preview/선택적 `-Apply`; 최초 원본 백업을 유지한다.


### 타이틀 가이드에서 이동한 원문

## 2026-10-03 C PC 추가 UI 준비·진단 — 핵심 연결 대기

전체 요청은 **부분 완료**다. 레이싱 DA의 Best Lap 설명과 문서 정합성 수정을 마쳤고, 아래 신규 UMG 두 개를 준비·저장했다. 기존 `WBP_DroneFrontEndRoot`/`WBP_DroneFlightHUD`, C++, 맵, 설정은 바꾸지 않았다. 신규 위젯은 아직 제품 호스트에 참조·연결되지 않았다.

| 준비한 로컬 에셋 | 실제 내용 | 남은 연결 |
|---|---|---|
| `/Game/Drone/FrontEnd/UI/WBP_DroneFiveItemMenu` | 스토리/레이싱/튜토리얼/설정/종료 순서의 텍스트 버튼 5개, 상하 Explicit 포커스 이름 참조, 클릭 요청 Dispatcher 5개+Back, `FocusFirstItem`/`RequestBack` | C++의 현재 4버튼 호스트·카테고리 진입·뒤로가기와 연결 필요 |
| `/Game/Drone/Prototype/UI/WBP_DroneControlInputDisplay` | 좌우 스틱 UI, `UpdateStickAxes(LeftX,LeftY,RightX,RightY)`의 [-1,1] 클램프/화면 Y 반전, `SetControlInputDisplayVisible(Show)` | Settings 상태·실제 입력 축·HUD 장착 필요. 고도계는 독립이며 전역 기본값/자동 전환 정책은 미정 |

공개 Unreal `ToolsetRegistry`를 통해 실제 WBP Designer/그래프를 확인하고 편집했다. 기존 타이틀 WBP Designer는 0개 위젯이며 native fallback 4메뉴를 사용한다. 기존 비행 HUD Designer는 8개 위젯이고 입력 표시/토글 BP 변수는 없다. 이전 일반 Python API 실패를 BP 편집 도구 부재로 확대 해석하지 않는다. 신규 메뉴의 runtime-only 포커스 참조가 저장되지 않는 문제는 Designer `WidgetToFocus` 이름 참조로 교정했다.

검증: UE 5.8 새 에디터 재로드·경고를 오류로 처리한 BP 컴파일, 정확한 5메뉴/버튼/포커스/클릭 실행 연결/Dispatcher/함수/고도계 독립/저장 SHA **19/19 Pass**. `WidgetLibrary.create`가 Python에 노출되지 않아 위젯 함수 실제 실행은 미실행. 화면 렌더·PIE·실제 패드/혼합 입력/분리·재연결·제품 맵3 완주/복귀는 미검증. 앞서 기존 바이너리 focused 회귀는 3/3 Success이며 신규 UI 제품 연결의 검증으로 간주하지 않는다.

Claude 인계 진단: `C:\URproject\drone`의 idle Code 세션 `fd8b6237-e858-42e3-b584-d1ffaafa940f`(표시명 “대화 내용 수집”, PID33636)는 Claude Desktop PID8872가 관리하는 stream-json/stdio 자식이다. 별도 CLI `loggedIn=false`는 Desktop 로그아웃 증거가 아니다. 현재 Codex 실행 도구에는 기존 Claude UI 입력용 `node_repl/@oai/sky`나 세션 전송 connector가 없다. 공식 `agents --json`은 읽기 목록 경로이고 help에 기존 대화 메시지 전송 명령은 없다. **C++ 인계 미전달/미시작**. 사용자가 기존 Claude Desktop→Code의 위 드론 세션에 작업 폴더의 `claude_drone_cpp_handoff.txt`를 붙여넣으면 정상 기존 UI 경로로 전달할 수 있다. 토큰/키/사적 세션 원문은 읽거나 복사하지 않았고 resume/attach/중복 세션은 실행하지 않았다.

원격 읽기 비교: drone 로컬 `5b03ad3` 대비 원격 main `41444c2`의 2커밋은 훈련맵/게이트4개/산악맵 6파일이며 DA·신규 UI·C++과 직접 경로 충돌 없음. MD 원격은 `250e9758`로 로컬과 같다. 6개 LFS 원격 본문 모두 로컬 캐시 없음, 게이트4개 로컬 파일 없음. 최신 원격 맵의 런타임 검증은 미실행이며 다운로드·pull·merge·checkout·reset은 하지 않았다.

Space 동기화는 최신 요청에서 제외했다. 기존 Space 쓰기 자동 승인 거절 후 재시도/권한 우회하지 않았다. 로컬 신규 위젯은 `remove_drone_ui_components.ps1` 기본 Preview로 확인 후 필요할 때만 `-Apply`로 제거할 수 있으며 후속 수정 SHA가 다르면 중단한다. 원래 DA+MD8 복구는 `restore_drone_meeting_changes.ps1` 기본 Preview/선택적 `-Apply`; 최초 원본 백업을 유지한다.


## 2026-10-04 감사1차 수정·코스/Acro 후속 반영 — C PC

작업 지시: Claude bridge run20261004-063805-docs-docs-audit-fix-batch1/prompt.md(UTF-8). 코드/도구/자동화·리뷰 Claude, 로컬MD·DroneSpace Codex. Unreal HEAD=추적origin/main41444c2·0/0는 읽기전용Git조회, 미커밋/미추적 유지. Build/PIE/패키징/쿠킹/맵생성·Unreal셸쓰기·Commit/Push·Trello/Figma수정·키읽기 미실행. md tools2개는 작업 시작 전 Claude 변경이며 Codex는 수정하지 않았다.

### 후속 결과와 검증 출처

- ACRO-MEETING-01: Mode1 Space 하강/반전은 키보드Action·패드세로축Action이 한 변수를 나중 값으로 덮는 문제. Space+오른쪽-0.5→스로틀-0.38, W+왼쪽-0.5→피치-0.38, Mode2도동일. 입력원분리·절댓값큰쪽사용, 키보드해제시패드인계·모두해제0. AcroInputBehaviorPIE D구역8시나리오 자동검증. overlap_before.log의실패4항목(테스트1개Fail)→overlap_after.log17Success/0Fail·review_fix_test.log집중30Success/2Fail를Codex조회. 실제패드체감수동대기.
- TUT-COURSE-SMOOTH-01: Production읽기전용측정 Scale2·로컬9.6km/월드19.2km·92CurveAuto, 기존256균일조각약75m·표시선오차최대7.9m/95%2.3m. MountainRange33.8km·Island10.6km도같은원인. 짧은TestMap68/113조각불변, 긴코스만sqrt(곡률)밀도+15%균일몫. MaximumCourseLineSegments 기본1024(16~4096·Tutorial|Course|Visual)는최대약50cm/95%7cm로선택한시작값·확정값아님,2048측정최대20cm. 재생성25646ms·1024258ms(로드/BeginPlay1회). BP Run Construction Script on Drag Off·놓을때1회·BP만저장, Production미저장·MCP급커브캡처확인. CourseLineAdaptiveSegments15.2km 최대오차균일256244cm→곡률25640cm→곡률10243cm·상한증감·BP설정자동검증. 근거ClaudeCourse/inspect.log·deviation.log·bp_drag.log·review_fix_test.log(측정/캡처는Claude지시서근거). 팀원코스외형·Editor편집체감수동대기.
- 도구재실행안전(Claude수정): ConfigureDroneTitleLobby.py 현재레이싱DA문구유지·Heading/GateFlight일치(lobby_cmp.log). md NPCGreybox TestMap·적InsurgentPreset1/2/ABP_NPC_Rifle_Greybox·아군QuantumCharacter/ABP_NPC_Unarmed_Greybox·기존맵Create거부(BP수정전)·Validate통과(지시서). HostileCoverResponse TestMap. Codex도구미수정·미실행.
- 회귀: Drone.Prototype+Drone.Tutorial+ControlInputDisplayPIE32개중30Success·2Fail은팀원Production맵의존(변경전메시지동일). 전체Drone.*95개2회각85Success·10Fail(test.log/test2.log)이며둘다PIE미렌더(samples=0); 포커스6개판정제외·나머지알려진4개NPCPerceptionSearchPIE/LobbyLayoutStabilityPIE진단/TrainingAssets/TrainingPIESmoke. 오늘9회중7회미렌더는Claude지시서, 화면그려진포커스확인대기. known-test-failures갱신. 새벽12/12·90/94는별도 실행으로보존하고합산하지않음.
- Claude반박검증리뷰: 낮음4건(테스트초기화누수·입력해제검사누락·코스드래그비용·엄폐맵경로)모두수정, 제품동작버그없음판정. Codex가새Build나테스트를실행한결과가아님.
- Bangkok: ec2e88f(10/01)맵삭제·10/04사용자의도된삭제확인, ASSET-BANGKOK-01종료. 의존987개·LFS약11.46GiB정리사용자결정. md공개범위/제출가이드개인정보처리·9/17OpenRouter키폐기확인도현재미정·키값미열람.

### 감사 처리목록 — 원본 감사파일의 파일:줄

99건중41건처리·58건이번미처리(2차대상; 고의로범위확장안함). 별도상대링크11건은99건에포함하지않는다.

| 파일 | 감사 원본 줄 |
|---|---|
| WORKBOARD.md | 76·243·35·80·109·226 |
| docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md | 30 |
| CONTEXT.md | 23·15 |
| WORK_PC_START_HERE.md | 126·94·150 |
| docs/ai/DRONE_SMART_OBJECT_NPC_GUIDE.md | 199·202·471·487·632·248 |
| docs/assets/DRONE_BANGKOK_OILRIG_MIGRATION_2026-09-30.md | 8 |
| docs/assets/DRONE_CONTENT_FOLDER_GUIDE.md | 119 |
| docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md | 267 |
| docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md | 88·156 |
| docs/git/CLAUDE_CODEX_COLLABORATION.md | 10·99 |
| docs/git/CLAUDE_CODEX_SETUP.md | 59 |
| docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md | 432·619 |
| docs/tutorial/DRONE_PROTOTYPE_IMPLEMENTATION.md | 202 |
| docs/tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md | 20 |
| docs/tutorial/DRONE_TRAINING_COURSE_IMPLEMENTATION.md | 212·145 |
| CLAUDE.md | 19 |
| README.md | 20 |
| docs/README.md | 94 |
| docs/ai/DRONE_MG_TURRET_3PART_GUIDE.md | 23 |
| docs/gameplay/DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md | 131 |
| docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md | 62 |
| docs/gameplay/DRONE_TEST_MAP_GUIDE.md | 134 |
| docs/gameplay/DRONE_WEATHER_WIND_RAIN_PLAN.md | 44 |
| docs/planning/WORK_MANAGEMENT.md | 107 |

### WORKBOARD 다이어트

전58,728바이트·244줄 → 후39005바이트·142줄(UTF-8·LF개수+1). 옮긴절: 10/04새벽최신기준, 10/02새벽후속/새벽,10/01밤후속/밤/저녁최신기준과앞선점검, 이동후보맵, 병행수동회귀, 최근완료, 종료된요청범위. 원문은archive/WORKBOARD_2026-10.md, 완료·대체카드ASSET-BANGKOK-01/UI-TITLE-LOBBY-02/UI-DATA-COPY-01은현재상태1줄정정후이동. 10/03UI준비·진단은위WORKLOG절에원문보존, 연결후위젯삭제사용금지명시. 이관본문은링크기준경로만정정. 현재카드·결정필요·사용자맵확인·Next보존.

### 상대링크·Space 확인

상대링크11개수정: STATUS_2026-09.md3개·WORKLOG7개·TUTORIAL_IMPLEMENTATION_TEST_GUIDE1개(버튼타이틀대상은실제타이틀가이드로경로정정). 지정3문서및이번변경32문서파일대상상대링크재점검0개. 기존이력본문은링크경로만수정, 기존기획/날짜/작업도구표기보존.

DroneSpace 기존진행상황과다음작업·테스트맵과확인가이드·Blueprint조정과팀원가이드3페이지의총13개연산저장, 13개모두재조회본문일치. 기존기획·날짜별기록·Trello링크보존, 새페이지·공유권한변경·예약자동화없음. GitHub본문은로컬미커밋상태로아직미반영.

### 최종 문서 확인·Git 상태

32개 변경 문서의 상대파일링크0개·코드펜스불균형0개·주요계약검사누락0개. git diff --check 통과. 아래 status는 전체작업트리이며 기존변경(planning4개·tools2개)도포함한다. 이번Codex수정은문서32개(새아카이브1개포함), 기존파일내용은보존했다.

```text
 M CLAUDE.md
 M CONTEXT.md
 M README.md
 M STATUS.md
 M WORKBOARD.md
 M WORK_PC_START_HERE.md
 M docs/README.md
 M docs/ai/DRONE_MG_TURRET_3PART_GUIDE.md
 M docs/ai/DRONE_NPC_GAZE_TRACKING_PLAN.md
 M docs/ai/DRONE_SMART_OBJECT_NPC_GUIDE.md
 M docs/ai/DRONE_SMART_OBJECT_ROUTE_EDITING_GUIDE.md
 M docs/assets/DRONE_BANGKOK_OILRIG_MIGRATION_2026-09-30.md
 M docs/assets/DRONE_CONTENT_FOLDER_GUIDE.md
 M docs/gameplay/DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md
 M docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md
 M docs/gameplay/DRONE_TEST_MAP_GUIDE.md
 M docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md
 M docs/gameplay/DRONE_TUTORIAL_IMPLEMENTATION_TEST_GUIDE.md
 M docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md
 M docs/gameplay/DRONE_WEATHER_WIND_RAIN_PLAN.md
 M docs/git/CLAUDE_CODEX_COLLABORATION.md
 M docs/git/CLAUDE_CODEX_SETUP.md
 M docs/git/DRONE_UNREAL_MCP.md
 M docs/history/DRONE_WORKLOG.md
 M docs/planning/DRONE_FIGMA_MISSION_IMPLEMENTATION_MATRIX.md
 M docs/planning/DRONE_FRONTEND_MISSION_FLOW_PLAN.md
 M docs/planning/DRONE_PROJECT_PLANNING_BRIEF.md
 M docs/planning/DRONE_TUTORIAL_STORY_PLAN.md
 M docs/planning/WORK_MANAGEMENT.md
 M docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md
 M docs/tutorial/DRONE_PROTOTYPE_IMPLEMENTATION.md
 M docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md
 M docs/tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md
 M docs/tutorial/DRONE_TRAINING_COURSE_IMPLEMENTATION.md
 M tools/unreal/Setup-DroneHostileCoverResponse.py
 M tools/unreal/Setup-DroneNPCGreybox.py
?? docs/history/archive/
```


### 이관 원문: docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md — 2026-10-04 최신 Acro 입력·데드존·응답 조정 (C PC)

## 2026-10-04 최신 Acro 입력·데드존·응답 조정 (C PC)

Unreal HEAD `41444c2` + 로컬 미커밋. 조사·C++·Build·자동화 Claude, Scout/Drop 입력 연결 Codex ui run `20261004-001325-ui-ui-acro-input-assets`(Editor MCP)→Claude 검증, 문서 Codex. 아래 10/03·9월 검증은 당시 범위다. 새벽 집중12/12·화면 그려진90/94는 당시 근거다. 최신10/04 후속 집중30/32(팀원Production맵의존2Fail)·전체95개2회미렌더, 패드포커스6개판정제외·화면그려진포커스확인대기. 실제패드·키보드체감은수동대기다.

| 조정 위치 | 계약·현재값 | 확인할 것 |
|---|---|---|
| Acro 선택 가능한 모든 비행 기체 BP Class Defaults | FPV·Scout·Drop·FiberOptic에 AcroPitchAction/AcroRollAction/AcroYawAction/AcroThrottleAction/AcroGamepadLeftVerticalAction/AcroGamepadRightVerticalAction 6개를 FPV와 같은 Input Action으로 연결 | 하나라도 None이면 Acro 입력 누락 가능. Scout/Drop 누락 수정·컴파일·저장 후 Claude 재조회와 AssetContract로 확인. 지상 UGV 제외 |
| IMC_DronePrototype Acro 패드 축4개, Modifiers 맨 앞 | Gamepad_RightX→AcroRoll, LeftX→AcroYaw, LeftY→AcroGamepadLeftVertical, RightY→AcroGamepadRightVertical에 Dead Zone | 같은 IMC 쉬운 조작 Gamepad_RightX→IA_DronePrototype_Yaw 값을 복사: Lower0.2·Upper1.0·Radial. 새 수치 결정 아님. 33매핑·키·Action·순서 보존 |
| Drone Definition Data Asset `FlightProfile.AcroRateSettings` | `BodyRateResponseTimeSeconds`·최대 Pitch/Yaw/Roll 각속도 | 조정은 여기서 한다. Pawn 정확 적분과 단일 축-각 합성으로 30/60/240fps 자세 일치, 이번 기존 조정값 유지. 키보드 별도 배율/Angle 모드·마우스 Yaw는 현재 미정 |
| `Tools/AssetMigration/BuildDroneAcroInput.py` | Acro 패드 Dead Zone 복사 및 FPV/Scout/Drop/FiberOptic 6개 연결 생성 | 재생성 때 수정 유지하도록 Claude 변경. 이번 미실행, docs 작업에서 실행하지 않음 |

10/04 추가수정(Claude): Acro 키보드/패드Action이 한 변수에 나중 값을 덮는 원인 재현(Space+오른쪽-0.5→스로틀-0.38·W+왼쪽-0.5→피치-0.38). 입력원을 분리하고 절댓값 큰 쪽을 사용해 키를 누르면키보드가이기고떼면패드로인계한다. AcroInputBehaviorPIE D구역8시나리오(해제/인계/0포함)자동검증·실제패드수동대기. Mode차이는패드세로축배치뿐, 키보드 W/S·A/D·Q/E·Space/Ctrl동일.

Enhanced Input은 DefaultInput.ini 축 데드존을 쓰지 않으므로 해당 INI만 보고 Acro 패드 보호를 판정하지 않는다. 기존 0.05 쏠림이 키보드 스로틀을 덮고 회전이 누적되던 결함은 매핑 Dead Zone으로 수정·자동 검증됐다. Codex MCP의 Instanced Modifier 생성은 None으로 실패해 저장 없이 복구했고, IMC 실제 저장은 Claude headless Python 패치(`Saved/Automation/ClaudeAcro/patch_dz.log`)다. Scout/Drop BP 저장은 Codex(ui), run의 최종 보고는 모델 용량 오류로 없지만 Claude `assign_bp.log`·자동화로 확인했다.

Mode2 LeftY=Throttle/RightY=Pitch, Mode1 LeftY=Pitch/RightY=Throttle; 키보드는 양쪽 W/S Pitch·A/D Roll·Q/E Yaw·Space/Ctrl Throttle로 같은 결과다. Space 단독 자세 불변은 자동 검증, FPV 키보드0.1초 탭 약65° 회전/무수평복귀는 체감 원인 후보다. 실제 장치에서 [테스트 순서](../gameplay/DRONE_TEST_MAP_GUIDE.md)를 확인하고 회의 “반전” 뜻을 사람에게 확인해야 한다.

UI-FOCUS-RACE-01은 UIOnly 지연 루트 포커스에 대한 5프레임 감시/복원 수정 후 확인 중이다. 다른 강조 버튼으로 패드 이동한 경우 복원하지 않는다. 화면 그려진 회귀 수정 후 Success는 1회, 수동 첫 강조 확인 대기다. 추가 회귀는 LobbyLayout samples=0 등 미렌더 실행 여부부터 확인한다. 10/04 pull 뒤 지형 코스와 제품 Racing 연결/PlayerStart·완주 판정은 현재 미정이며 이전 LFS 미수신 문구는 당시 이력이다.




### 이관 원문: docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md — 2026-10-03 밤 최신 Blueprint 조정 — 5메뉴·조종 입력 표시·레이싱 키

## 2026-10-03 밤 최신 Blueprint 조정 — 5메뉴·조종 입력 표시·레이싱 키

C PC Unreal `5b03ad3` + 로컬 미커밋. C++·Build·테스트 Claude, BP 연결 스크립트 Codex(ui)→Claude 실행·검증. 저장 BP2개 BS_UP_TO_DATE, 집중 렌더 33/33 Success, 전체 91개 중 86 Success·기존5 Fail. 아래 9월 기록은 당시 기준이며 현재 메뉴/API는 [타이틀·로비 가이드](../gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md) 0·2절을 우선한다. 자동 검증 출처 `Saved/Automation/ClaudeMenu5/test2.log`·`ClaudeMenu5Full/test.log`, 수동 패드·1280/1920·연결 해제/혼합 입력·맵3는 대기다.

| 위치 | 조정 항목·현재값 | 의미 |
|---|---|---|
| WBP_DroneFrontEndRoot Class Defaults | TitleMenuClass = WBP_DroneFiveItemMenu | 저장 연결됨. 버튼 StoryButton/RacingButton/TutorialButton/SettingsButton/ExitButton, 필수 OnStoryRequested/OnRacingRequested/OnTutorialRequested/OnSettingsRequested/OnExitRequested·선택 OnBackRequested. 계약 오류는 [TITLE-MENU] 경고+native 5개 |
| 같은 Root Class Defaults | TitleButtonHeight=80, TitleButtonSpacing=26 | C++ 기본 5버튼의 임시 크기/간격. 지정한 메뉴 WBP 디자인은 Designer에서 조정 |
| WBP_DroneFlightHUD Class Defaults | ControlInputDisplayClass = WBP_DroneControlInputDisplay | 저장 연결됨. SetControlInputDisplayVisible(bool), UpdateStickAxes(float LeftX,LeftY,RightX,RightY) 이름 계약 |
| 같은 HUD Class Defaults | ControlInputDisplayOffset=(0,-24) | 아래 가운데 기준 위치. 실제 1280/1920 가독성·다른 HUD 가림 확인 |
| 같은 HUD Class Defaults | ControlInputDisplayUpdateInterval=1/30초 | 월드 타이머 갱신, ON·기체 있을 때만 표시/축 전달, 축 값 바뀔 때만 호출·OFF 갱신 중지 |
| Config/DefaultGame.ini | [/Script/Drone.DroneAudioSettingsSubsystem] bControlInputDisplayEnabledByDefault=False | 사용자 결정 전 임시 끔·최종 기본값 미정. 저장 사용자 선택 우선, 기본값 복원→적용은 선택 삭제 |
| 설정 UDroneSettingsWidget | ControlInputDisplayCheck | 조종 > 조종 입력 표시, 기존 적용/취소/기본값 유지. 음량 SaveGame bHasControlInputDisplayChoice/bControlInputDisplayEnabled, 자동화 DroneAudioSettings_Automation |
| ADroneTrainingRouteSelector BP/배치 액터 Details | bAllowPlayerRouteKeys=true | 플레이어 경로 키 허용 스위치 |
| 같은 Selector | bBlockRouteKeysInRacingMissions=true | 로비 Racing 미션은 1~5 바인딩/안내 차단. 시험맵 직접 실행·Tutorial/Training/Story는 기존대로, 랜덤 API 삭제 안 함 |

축은 Pawn `GetControlInputSnapshot()` BlueprintPure가 소유하며 UI에서 별도 입력 바인딩을 만들지 않는다. 물리 위치 X 오른쪽+, Y 위+, [-1,1], 커서 중심±38px/화면Y 반전. 쉬운/실제 왼쪽 이동·오른쪽 회전/카메라·트리거 고도, Acro Mode2 왼쪽 Yaw/스로틀·오른쪽 Roll/Pitch, Mode1 왼쪽 Yaw/Pitch·오른쪽 Roll/스로틀, 지상 왼쪽 조향/전후. 키보드도 같은 액션 위치, 장치 자동 전환/혼합 입력/분리·재연결 정책 현재 미정. 고도계는 독립 유지한다.

테스트 Class Defaults를 메모리로 채우는 덮어쓰기는 BP 최초 로드의 부모 대비 차이 복사 때문에 인스턴스 연결 증거가 아니다. 실제 저장된 위 두 Class Defaults를 검사한다. 제품 Lvl_DroneRacingTest에는 RouteSelector가 없어 숫자키 미노출 확인, 원격 맵3는 LFS 미수신·완주/복귀 미실행. 사람 디자인·Production Training 맵 보존, 최종 기본값/레이아웃/정책은 임의 확정하지 않는다.




### 이관 원문: docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md — 현재 검증 기준선

## 현재 검증 기준선

| 검증 항목 | 현재 확인 결과 |
|---|---|
| `DroneEditor Win64 Development` | Build 성공 |
| `Drone.Tutorial` Automation | 7/7 통과 |
| `Drone.AI` Automation | 11/11 통과. Rifle 빈 시험 World의 예상 RecastNavMesh 경고 1건 |
| 전체 `Drone.` Automation | 27/27 통과, 실패 0 |
| 전투 집중 검증 | AI-MG-02·HP-01·AI-COVER-01·AI-COMBAT-END-01·AI-AMMO-01 관련 집중 테스트 통과. AI-VIS-01A Editor Build와 WeaponContract·RifleTrace·ShotgunTrace 3/3 통과. 이 변경을 포함한 `6a18210` 뒤 전체 묶음은 아직 반복하지 않음 |
| Front-end Flow | FLOW-01~08 완료. `Drone.Flow` 5/5 통과, 전체 수명주기를 완전히 새 PIE 실행 3회 반복해 Root·Map 요청·Drone·Director·Finish 중복 0 확인 |
| 역할·비행 회귀 | 공통 Primary/Secondary Action 포함 `Drone.Prototype` 7/7 통과. IMC 21 Mapping과 Pawn 소유 Binding 확인 |
| `CompileAllBlueprints` | Blueprint Errors 0, Blueprint warnings 0, failed load 0. 별도 Summary에 기존 Battlefield Pose GUID와 MCP 고지 경고 유지 |
| 현재 에셋 이식 재검증 | FPV 전용 1/1, Blueprint 0/0/0, 스테이징 선택 자산·현재 Integration 금지 의존성 0, 이식 13개 LFS와 fsck 통과 |
| 기존 Standalone 시각 기록 | FPV 외형, 고정 추적 Camera, 실제 WBP HUD, Cyan 안내선, Current/Inactive Gate 표시 확인 |
| 사용자 수동 확인 | Training 두 Lap 비교 HUD, OilRig Map Check·화면·성능, Ground Drone/MG·NPC·Raw Drone 외형을 확인할 차례 |

현재 main의 `UDroneTrainingLapRecorderComponent`는 Segment/Lap 원본 뒤 TUT-04B 비교 결과도 만든다. 첫 성공은 기준 기록, 이후 성공은 현재 시도를 제외한 이전 평균과 Best를 사용한다. HUD에 이전 완주 평균·Best·시간 Delta·속도 Delta가 표시되며 계산은 Blueprint에 중복하지 않는다. 실제 두 Lap 표시 확인 전까지 TUT-04의 수동 판정은 남아 있다.




### 이관 원문: docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md — 2026-09-08 현재 역할·Front-end·Mission 구조

## 2026-09-08 현재 역할·Front-end·Mission 구조

현재 코드 흐름은 아래처럼 연결된다.

```text
UDroneGameFlowSubsystem (GameInstance 수명)
  → UDroneFrontEndRootWidget
  → ADroneFrontEndPlayerController가 선택 MissionMap OpenLevel
  → ADroneMissionGameMode + ADroneMissionPlayerController
  → UDroneSelectionWidget
  → 선택 Definition Pawn 1대 Spawn/Possess
  → ADroneMissionDirector
  → UDroneMissionObjectiveWidget
  → UDroneMissionResultWidget
  → 같은 Mission Retry 또는 Front-end Lobby
```

핵심 책임은 다음과 같다.

| 코드 | 현재 책임 |
|---|---|
| `Flow/DroneGameFlowSubsystem.*` | 맵을 넘어 유지되는 상태, Mission/Drone 선택, 성공 Story Fact와 중복 요청 거부 |
| `Flow/DroneFrontEndPlayerController.*` | Front-end Root 1개 생성, 선택한 Map을 정확히 한 번 열기 |
| `UI/DroneFrontEndRootWidget.*` | Opening·Lobby·정적 Briefing 표시와 버튼 입력 |
| `Flow/DroneMissionGameMode.*` | 선택 전 비-Drone Spectator 사용, 자동 Drone Spawn 방지 |
| `Flow/DroneMissionPlayerController.*` | 선택 UI, 선택 Definition 한 대 Spawn/Possess, Director·목표·결과 UI 수명주기 |
| `UI/DroneSelectionWidget.*` | 정찰/FPV/드랍과 쉬운/실제 조작형·안정/균형/고기동 선택 |
| `Mission/DroneMissionObjectiveTypes.h`, `DroneMissionDefinition.*` | Objective ID·사건·수량·시간·대상 Tag·Story Fact 조건과 성공 Fact 데이터/검증, 기존 문구형 목표 fallback |
| `Mission/DroneMissionDirector.*` | 출격 뒤 현재 Rule의 Scan/Delivery/Destroy/Lap/Return/Jamming Event·시간 제한·중복 Actor 관리, Snapshot과 성공/실패 1회 확정 |
| `Mission/DroneMissionReturnZone.*` | BP/맵 배치형 귀환 Box Trigger. 실제 기지 위치·크기와 대상 Tag는 아직 미정 |
| `Signal/DroneSignalTypes.h`, `DroneSignalComponent.*` | 재밍 Source 중 최대값·단계·신호율·비행 반응/영상 Noise와 Definition 기반 면역. Tick 없음 |
| `Signal/DroneJammingVolume.*` | BP/맵 배치형 방해 Box와 이탈·명시적 Jammer 해제 Event. 실제 Zone 위치·무력화 방식은 미정 |
| `Abilities/DroneReconScanComponent.*` | 거리·화각·LOS 유지형 정찰 Scan |
| `Abilities/DroneImpactDetonationComponent.*` | Arm 뒤 유효 속도 충돌 시 1회 폭발·기체 파괴 |
| `Abilities/DronePayloadDropComponent.*` | 상단 시점, 투하, 빈 상태의 근접 운반 화물 검색·실제 Actor 부착·재투하, 목표 접촉 결과와 재장전 |
| `Abilities/DroneDroppedPayload.*` | 투하 중 충돌 판정과 맵 배치 Pickup/Carried 상태; `BP_DroneCarryablePayload`의 Native 부모 |
| `UI/DroneMissionObjectiveWidget.*` | Director Event만 구독하는 측면 목표 패널; Tick/Actor 전체 검색 없음 |
| `UI/DroneMissionResultWidget.*` | 성공/실패, 재도전, 로비 복귀 |

Training Mission의 현재 Greybox 규칙은 저장 Data Asset의 `Objective.TrainingLap` 1회 Lap 완료=성공, `Drone Health 0`=실패다. 이는 Vertical Slice 시험 규칙이며 새 Mission별 목표 수량·대상·귀환 기지와 최종 Story Mission 규칙은 현재 미정이다.

2026-09-16 신호 Greybox는 Mission 후보에 재사용할 기능 기반으로만 추가됐다. Zone 강도에 따른 HUD 경고·강한 단계 기본 비행 속도/가속도 배율·이탈/해제 Rule Event가 코드/자동화 완료다. `VideoNoiseIntensity`와 Blueprint Event는 전달하지만 실제 영상 Noise Material·목표 정보 손실 화면과 새 Story Mission Data Asset/맵 배치는 아직 없다. [재밍 가이드](../gameplay/DRONE_JAMMING_GREYBOX_GUIDE.md)에서 담당 클래스와 Editor 시험을 본다.

### 현재 UI의 정확한 상태

- Front-end에는 기존 `WBP_DroneFrontEndRoot`가 있지만 FLOW-04 이후 필수 이름이 모두 없으면 C++ 기본 Layout으로 안전하게 대체된다.
- Drone 선택·목표·결과는 현재 C++ native fallback UI로 실제 실행 가능하다.
- 최종 WBP Designer와 Drone 3D Preview는 아직 만들지 않았다. 기능 완료와 최종 외형 완료를 같은 것으로 기록하지 않는다.
- 최종 WBP를 만들 때 아래 이름을 그대로 배치하면 C++ 상태·버튼·Delegate 로직을 재사용할 수 있다. Blueprint Event Graph에 Flow나 Spawn 로직을 다시 만들지 않는다.

| Widget 부모 | 필수 Designer 이름 |
|---|---|
| `UDroneFrontEndRootWidget` | `OpeningPanel`, `LobbyPanel`, `MissionBriefingPanel`, `ContinueButton`, `OpeningTitleText`, `LobbyTitleText`, `LobbyStatusText`, `MissionSelectButton`, `MissionSelectButtonText`, `MissionNameText`, `MissionDescriptionText`, `MissionMetaText`, `StartMissionButton`, `MissionBriefingTitleText`, `MissionBriefingBodyText`, `FinishMissionBriefingButton` |
| `UDroneSelectionWidget` | `DroneSelectionPanel`, `MissionNameText`, `DroneNameText`, `DroneDescriptionText`, `DroneProfileText`, `DroneButton0~2`, `DroneButton0Text~2Text`, `ControlModeButton`, `ControlModeButtonText`, `HandlingPresetButton`, `HandlingPresetButtonText`, `LaunchDroneButton` |
| `UDroneMissionObjectiveWidget` | `MissionObjectivePanel`, `MissionObjectiveTitleText`, `MissionObjectiveText`, `MissionObjectiveProgressText` |
| `UDroneMissionResultWidget` | `MissionResultPanel`, `MissionResultTitleText`, `RetryMissionButton`, `ReturnToLobbyButton` |

### 사용자가 지금 Editor에서 확인할 순서

1. `/Game/Drone/Maps/Lvl_DroneFrontEnd`를 연 뒤 PIE를 시작한다.
2. `계속 → Training Mission 선택 → 미션 시작 → 작전 시작` 순서로 누른다.
3. Training Map에서 선택 전 Drone이 없고 정찰·FPV 자폭·드랍 카드 세 개가 보이는지 확인한다.
4. `쉬운 조작/실제 조작형`과 `안정/균형/고기동`을 각각 바꿔 본 뒤 한 기체를 출격시킨다.
5. 선택한 Drone 한 대만 생성되고 Flight HUD와 측면 목표가 표시되는지 확인한다.
6. Drop Drone은 선적재 화물을 좌클릭/RB로 한 번 투하한 뒤 `RoleTest_CarryablePayload` 크레이트 300cm 안에서 같은 키로 적재한다. 크레이트가 기체 하단을 따라가고 다시 누르면 실제 크레이트가 투하되는지 확인한다.
7. Gate 0→1→2→3을 통과해 성공 화면과 `재도전`을 확인한다.
8. 재도전 뒤 다른 기체를 선택하고 파괴/체력 0 경로에서 실패 화면과 `로비 복귀`를 확인한다.
9. 로비에 돌아왔을 때 이전 Drone·목표·결과 UI가 남아 있지 않은지 확인한다.

정찰 `StartScan`, FPV `ArmImpactDetonation`, 드랍 `ActivatePrimaryPayloadAction/SetDropViewEnabled` API와 Event에 공통 `Primary Ability / Secondary Ability` Input Action을 연결했다. 임시 Greybox 키는 좌클릭/RB와 우클릭/LB이며 최종 키로 확정한 것이 아니다. 정찰은 Primary로 가장 가까운 유효 Target Scan·Secondary로 취소, FPV는 Arm/Disarm, 드랍은 적재 중 투하·빈 상태 근접 화물 적재/탑뷰 전환이다. Training Map에는 정찰·자폭·투하 시험 표적, 배치형 크레이트와 Event 기반 한글 역할 상태 UI가 배치되어 있다.

자동 검증은 `DroneEditor Win64 Development`, `Drone.Flow` 5/5, `Drone.Prototype` 7/7, `Drone.Integration` 3/3, `Drone.Tutorial` 7/7을 통과했다. `MissionEntryPIE`는 Scout 전용 Pawn과 재시도 Drop 전용 Pawn을 포함한 전체 수명주기를 완전히 새 PIE 실행에서 3회 반복해 3/3 통과했다. Commit·Push는 하지 않았다.



### 이관 원문: docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md — 1. 이전 4메뉴 구현 기록 (2026-10-01)

## 1. 이전 4메뉴 구현 기록 (2026-10-01)

- 사용자가 제공한 `Title_Asset`의 배경, 어두운 오버레이, 로고, 일반/호버/클릭 버튼 PNG 6개를 Unreal Texture로 가져왔다. 참고이미지는 완성 화면 비교용이며 그대로 한 장짜리 버튼 화면으로 쓰지 않는다.
- 시작 화면의 제공 배경·어두운 오버레이·로고·버튼 6개 이미지는 유지한다. `Start / Training / Setting / Exit` 중 Start는 Story 4개 목록, Training은 `튜토리얼 / 레이싱` 하위 선택으로 연결한다. 훈련 목록은 튜토리얼 9개(기존 종합 Training 포함)와 레이싱 1개다. Story 목록에는 훈련 탭을 표시하지 않는다.
- 로비를 첨부 기획안의 좌측 스크롤 목록 / 중앙 작전 이미지·이름·지역·난이도 / 우측 개요·목표의 3열로 정리하고 하단 중앙 시작 버튼을 배치했다. 선택 강조와 현재 분류 필터를 유지하며, 다른 분류에 남은 선택을 바로 실행하지 않는다.
- 브리핑은 좌측 이미지와 우측 스크롤 설명·목표 순서, 하단 작전 지역 이동 버튼이다. 로비/브리핑/설정에도 기존 배경을 사용하고, 선택 Mission에 별도 Thumbnail이 없으면 기존 배경으로 보완한다.
- 기체 선택은 상단 큰 역할 프리뷰와 상세·조작 설정, 프리뷰 아래 출격 버튼, 하단 가로 기체 카드로 재배치했다. 기체 5종 Catalog와 Mission 허용 목록은 유지한다. 프리뷰는 공중 기체/UGV를 구분하는 역할 도식이며 실제 Mesh 렌더 프리뷰는 아니다.
- 로비·브리핑·기체 선택은 1920×1080 설계를 비율 유지해 축소하고 긴 설명은 스크롤한다. 1280×720·1920×1080 실제 화면 가독성은 수동 확인 대기다.
- Setting의 임시 품질 3버튼을 전체 음량·창 모드·해상도·품질·수직 동기화·프레임 제한과 적용/기본값/뒤로가기 화면으로 교체했다. 저장과 미적용 취소 기준은 아래 9절을 따른다.
- 회전 수업을 **방향 맞추기가 아닌 원형 코스를 한 바퀴 도는 비행**으로 수정했다.
- 독립 레이싱 시험맵을 추가했다. Best Lap JSON 영구 저장은 2026-10-02 구현·자동 검증 완료·실기 재실행 확인 대기다. 정식 경기 규칙·순위는 미완료다.




### 이관 원문: docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md — 8. 도구와 확인할 것

## 8. 도구와 확인할 것

`Tools/AssetMigration/Invoke-DroneTitleLobby.ps1`은 Editor 종료 후 실행한다. 이미 이식된 Texture가 있으면 원본 Downloads 폴더가 없는 작업컴에서도 실행할 수 있다. 원본 재수입이 필요하면 `-TitleAssetDir '실제 Title_Asset 경로'`를 지정한다.

도구는 WBP 이미지 기본값, 전용 Tutorial 원형 Station, 관련 DA 두 개, 독립 Racing 맵/DA만 갱신한다. 기존 레이싱 맵 전체 재생성이나 Production 저장은 하지 않는다. 최종 UI 수동 변경 뒤 이 도구를 무작정 재실행하면 이미지 기본값이 제공 이미지로 돌아가므로 주의한다.

자동화 보고서는 프로젝트 `Saved/Automation/TitleLobbyOrbit` 아래에 저장한다. 실제 수동 확인은 다음을 남긴다.

2026-10-01 다른 PC `C:\URproject\drone`의 기록: 앞선 Editor Build·14/14 → GameReadiness **32/32·테스트 오류/경고 0**, 시험맵 14개 Map Check 0/0 → Back 후속 33개 실패 0(HTTP 경고 동반 성공 1건). 1280 Setting/Training/탭·목록 일부와 Back/선택 복원, 1920 제목/Exit를 당시 확인했다. 이번 UI 변경 이전의 D 드라이브 최신화에서는 재실행하지 않았고 해당 다른 PC의 Oct 1 원시 `Saved` 보고서도 수신하지 않았다. 이 기록을 이번 UI의 수동 Pass로 해석하지 않는다. [검증 출처와 범위](../gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md)

이번 추가 UI/설정 코드는 현재 D 드라이브에서 MSVC `14.51.36257` Editor Build 및 `FrontEndContract / BackNavigationContract / MissionEntryContract / SettingsContract / FrontEndPIE` **5/5 Success**, 자동화 이벤트 오류/경고 0이다. 최종 보고서는 `Saved/Automation/TrainingLobbySettings/index.json`(2026-10-01 02:03:48 UTC). 분류/숨은 선택/복귀, 음량 Clamp·NaN·SaveGame 메모리 직렬화와 실제 Settings 자식 컨트롤·슬라이더/Back Delegate·미적용 취소를 검사했다. NullRHI/NoSound이므로 새 화면·실제 가청성·Standalone 창 변경·디스크 저장 후 재실행·전체 미션 손 조작 완주·패드 실기·최종 음원/연출은 수동 확인 대기다.

1. 1920×1080와 1280×720에서 로고·버튼·3열 로비·브리핑·가로 기체 카드·출격이 잘리는지. 긴 설명/목표/기체 정보는 스크롤해 끝까지 읽을 수 있는지.
2. 제공 버튼 PNG의 투명 여백, 텍스트 위치, 클릭 범위가 자연스러운지.
3. 원형 7/8 바퀴에서 미완료, 마지막 결승 통과 후 귀환으로 전환되는지.
4. 레이싱의 9개 Gate 정방향 완주 → 성공 결과가 나오는지.
5. 타이머 만료/충돌 실패 → 재시도 때 Gate 진행이 초기화되는지.
6. Start→Story 4와 Training→Tutorial 9/Racing 1 분리, 탭 선택·목록 선택 강조, 브리핑/기체 선택의 Back/Esc/패드 B, 선택/분류 복원과 반복 키 차단이 맞는지.
7. Setting의 음량 미리보기→취소 복원, 적용→재실행 복원, 품질/VSync/FPS 적용, 기본값의 미적용 취소를 확인한다. 창 모드/해상도는 PIE에서 비활성이고 Standalone에서 변경/재실행 확인한다.

자동화 성공만으로 최종 시각/조작 체감 검증까지 끝났다고 처리하지 않는다.




### 이관 원문: docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md — 10. 목록 튐 진단 (수정 전)

## 10. 목록 튐 진단 (수정 전)

2026-10-01 사용자 화면 제보를 렌더 PIE로 확인했다. 현재 실제 UI는 아직 수정하지 않았다. 기존 기능 자동화 5/5는 화면의 프레임별 배치 안정성을 검사하지 않았다.

| 측정 대상 | 첫 프레임 이후 최대 이동 | 판정 |
|---|---|---|
| 훈련 진입 목록 내부 | 80.507 설계 px | 튐 재현 |
| Hover 항목 선택 목록 내부 | 67.508 설계 px | 튐 재현 |
| Tutorial 선택 간 바깥 세 열 | 0.000 px | 열 자체는 고정 |
| 진단용 명시적 줄바꿈 폭 | 0.000 px | 지연 AutoWrap 원인 확인 |
| 위 비교 + 스크롤바 공간 확보 | 0.000 px | 이 최소 재현에서 추가 개선 없음 |

좌표는 1280×720 렌더 PIE의 Geometry를 1920×1080 설계 기준으로 정규화했다. 목록 높이도 658.047→708.279px로 다시 계산됐다. 전체 Tutorial 9개 선택에서 반복됐으며, Story 진입의 큰 튐은 이번 측정에서 재현되지 않았다(0.278px).

원인 경로: `SelectLobbyMission → Flow.SelectMission/BroadcastSnapshot → HandleFlowSnapshotChanged → RefreshLobbyContent → RebuildNativeMissionButtons`. 항목만 선택해도 `MissionButtonsColumn->ClearChildren()` 뒤 모든 Label을 새로 만든다. Label은 `AutoWrapText=true`, 명시 폭 없음이다. UE 5.8의 `STextBlock.h`는 AutoWrap 크기를 최소 한 프레임 늦게 얻는다고 명시하며, Slate는 Paint에서 얻은 실제 폭을 다음 측정에 사용한다.

권장 수정은 같은 목록의 버튼을 재사용하고 선택 강조/상세만 갱신하는 것, 첫 Paint 전에 Label의 줄바꿈 폭을 실제 가용 폭과 여백에서 결정하는 것이다. 스크롤 위치·포커스도 보존한다. 진단 비교의 `160px`는 원인 분리용 시험값이지 최종 UI 폭이 아니다.

진단 테스트: `Source/Drone/Flow/Tests/Diagnostics/DroneLobbyLayoutStabilityTest.cpp`, 이름 `Drone.Flow.Diagnostic.LobbyLayoutStabilityPIE`. `RenderOffscreen`으로 실행하고 `LobbyLayoutHoverOnly`로 최소 재현, `LobbyLayoutWrapProbe`로 transient Widget 비교를 추가한다. NullRHI는 이 Geometry 검사에 사용할 수 없다. 보고서는 `Saved/Automation/LobbyLayoutDiagnosticWrapProbe/index.json`(2026-10-01 02:31:18 UTC)이며 원래 UI가 실패하므로 전체 Result는 **Fail**이다. 실제 수정 이후 동일 검사와 1280/1920 화면 확인을 다시 통과해야 완료다.




### 이관 원문: docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md — 11. 패드 UI 확인 범위

## 11. 패드 UI 확인 범위

2026-10-01 C 드라이브 PC의 소스 `9f67706`을 확인했다. Root/기체 선택의 `NativeOnPreviewKeyDown`은 Esc·패드 Face Button Right·Virtual Back을 처리한다. Root의 화면 전환은 `SetUserFocus`로 Root 자신에 포커스를 주며 첫 활성 버튼을 선택하는 코드가 아니다. 네이티브 UI의 화면별 명시 탐색 설정·포커스 강조와 패드만으로 전 화면을 완주하는 검사도 확인되지 않았다. 기본 UMG 포커스 이동이 가능한 경우와 완전한 패드 지원을 구분한다.

다음 구현 범위는 시작/로비/브리핑/기체 선택/설정/결과의 초기 활성 버튼 포커스, 방향 탐색·확인/취소, 포커스 강조, 숨김/비활성 항목 제외, 목록 변경·Back 뒤 선택/스크롤 복원이다. 설정 Slider/ComboBox도 포함한다. 목록 전체 재생성 문제를 먼저 수정해 포커스가 붙은 버튼이 선택할 때마다 사라지지 않게 한다.

완료 조건은 키 입력 자동화와 실제 패드 수동 확인을 분리한다. 마우스를 쓰지 않고 메뉴 진입→탭/미션 선택→브리핑→기체 선택→출격, 설정 조절/적용/취소, 결과→재시도/로비를 확인하고 `PC / 패드 / 화면 / 입력 / 기대 / 결과`를 기록한다. 기존 Back 계약 성공이나 NullRHI 5/5를 이 전체 Pass로 사용하지 않는다. 이번 최신화에서는 코드·BP 변경과 새 검증을 실행하지 않았다.

### 패드 조작 — 2026-10-01 밤 후속

C PC Unreal `ec2e88f` + 로컬 미커밋, 작업 도구 Claude·문서 반영 Codex. UI-PAD-01은 구현됨·자동 검증 완료·실제 PS4 패드 수동 확인 대기다. 위 `9f67706`의 보강 전 기록은 당시 범위다.

| 입력 | 동작 |
|---|---|
| 방향 입력 / A / B | UE 기본 방향 탐색·확인 / 각 화면의 기존 Back |
| 훈련 로비 LB / RB | 튜토리얼 / 레이싱 탭 전환 |
| 로비 미션 목록 → / 출격 ← | 출격 버튼 / 고른 미션 |
| 기체 카드 ↑ / 출격·조작 모드 ↓ | 출격 / 고른 카드 |
| 결과 다시 하기 ↓ | 로비로 |
| 설정 음량 슬라이더 A → 좌우 | A로 잠근 뒤 UE 기본 좌우 조정 |

| 화면 | 첫 포커스/복귀 |
|---|---|
| 타이틀 | 마지막으로 쓴 버튼 → 없으면 시작 |
| 로비 | 고르던 미션 → 미션 종료 복귀 시 방금 한 미션(`LastLobbyMissionId`) → 첫 미션 |
| 브리핑 | 출격 버튼 |
| 설정 | 음량 슬라이더, 닫으면 타이틀 설정 버튼 |
| 기체 선택 | 고른 기체 → 첫 기체 |
| 결과 | 실패면 다시 하기, 성공이면 로비로 |

공통 `FDroneGamepadFocus`는 첫 조작 가능한 위젯에 포커스를 주고 새로 보인 위젯이 배치될 때까지 최대 30프레임 재시도한다. 강조는 RenderScale(기본 1.06)·버튼 글자색이며 그리기 변환만 바꿔 레이아웃을 유지한다. 각 UI 위젯(FrontEndRoot·Settings·Selection·MissionResult)의 Class Defaults `GamepadFocusScale`·`GamepadFocusTint`에서 조정한다. 목록의 `ScrollWhenFocusChanges`로 포커스를 따라 스크롤한다. 기체 선택의 출격은 기체 선택 전 비활성이므로 카드에서 A로 먼저 고른 뒤 ↑를 누른다.

자동 검증(C PC, Claude, RenderOffScreen 1920×1080): `GamepadNavigationPIE` 11단계·`GamepadMissionFlowPIE` 16단계 Success, `LobbyLayoutStabilityPIE` Success(최대 0.255px). 근거 `C:\URproject\drone\Saved\Automation\ClaudePad\render6.log`. 전체 NullRHI의 패드 2개는 렌더링 필요 경고로 건너뛰어 별도 렌더 검사와 구분한다. 실제 PS4 패드 검증은 아니다.

수동 확인 순서: 마우스 없이 타이틀 포커스→훈련→Hover 선택→→출격→브리핑→카드 A 선택→↑출격→↓카드 복귀→↑출격을 확인한다. 훈련 LB/RB 탭·선택 복원·B 타이틀 복귀, 설정 A 슬라이더 잠금/좌우·적용/취소/B 설정 버튼 복귀, 결과 다시 하기↓로비로·미션 선택 복원과 강조 가독성을 확인한다. 실패 재출격 DA를 쓰는 튜토리얼에서 추락 시 현재는 결과 화면 대신 첫 출격 위치에서 재출격하는 체감도 확인한다. 자동 결과 화면 탐색 검사는 재출격 수동 확인과 구분한다. `PC / PS4 패드 / 화면 / 입력 / 기대 / 결과`를 남기고 수동 Pass를 추정하지 않는다.




### 이관 원문: docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md — 배터리·신호 대역·HUD 조정 (2026-10-02 새벽, C PC)

## 배터리·신호 대역·HUD 조정 (2026-10-02 새벽, C PC)

작업 도구 Claude, 문서 반영 Codex. 기존 풍향 N/E/…·풍속은 구현되어 있으며 바람 아래 오른쪽 위 패널에 기체명과 신호 대역, 배터리 줄을 추가했다.

| 위치 | 조정값 | 의미 |
|---|---|---|
| `/Game/Drone/Data/Drones/DA_Drone_*`의 비행 프로필 | BatteryLifeSeconds | 플레이어 조종 중 소모할 용량(초). 0=배터리 끔·HUD 배터리 줄 숨김 |
| 같은 기체 Definition의 FlightProfile | SignalBandLabel | 신호 대역 표시 문자열. 5.8GHz는 시험 예시 |
| 기체 Pawn BP Class Defaults의 DroneBatteryComponent | LowBatteryFraction | 기본 0.2 이하 부족 경고 |
| 같은 Battery Component | DepletedResponse | 기본 WarnOnly(경고만), 선택 FailMission(미션 실패 처리, 미션이 재출격 설정이면 재출격) |
| FrontEnd Root Class Defaults | BriefingSecondsPerCharacter / BriefingMinLineSeconds / BriefingMaxLineSeconds | 브리핑 자동 시간 기본 0.075초/글자·2.5~9초. 줄별 DurationSeconds는 Mission DA에서 조정 |

모든 기체에 DroneBatteryComponent가 기본 부착된다. HUD는 “기체명 | 신호 대역” / “BATTERY nn% (mm:ss)”, 부족 시 빨간색·“부족”, 소진 시 “방전”을 표시한다. **현재 기체별 BatteryLifeSeconds는 모두 0, SignalBandLabel은 빈 값이다.** 배터리 시간·소진 처리·신호 대역 최종값은 현재 미정이다.

시험용 기체 Definition에 양수 BatteryLifeSeconds와 시험 신호 문자열을 넣어 출격한 뒤 시작 100%·조종 중 소모·부족·방전을 확인한다. 기체 선택 대기/AI 조종 중에는 소모되지 않아야 한다. FailMission은 미션 FailureResponse에 따라 실패 결과 또는 새 기체 재출격이 되어야 한다. 시험 값은 최종 기획값으로 남기지 않는다. Production Training을 시험용으로 덮어쓰지 않는다.

2026-10-02 C PC Claude NullRHI BatteryHUDPIE + HUD 2개 + CheckpointRestart **4/4 Success**, 근거 `C:\URproject\drone\Saved\Automation\ClaudeHUD\test.log`. 패널 위치·가독성 수동 확인 대기다. 브리핑 대사 DA 입력법은 [Mission 가이드](../gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md)를 따른다.

10/03 UI 준비·진단은 [WORKLOG](DRONE_WORKLOG.md)에 당시 원문 보존했다. 같은 날 밤 0절의 제품 연결 완료로 대체됐다. 연결 위젯 삭제 도구는 사용 금지다.



## 2026-10-04 오후 감사2차·면접 대비 정리 — C PC, Codex docs

지시서: Claude bridge run 20261004-074911-docs-docs-batch2-interview-cleanup/prompt.md(UTF-8). MdAudit와 InterviewAudit를 읽고 1차 원본 파일:줄 41건과 대조했다. Unreal HEAD=추적 origin/main41444c2는 읽기전용 Git조회(명령 한정 safe.directory, 설정 파일 변경 없음). 로컬 미커밋/미추적·기존 문서 변경 보존, Commit/Push·Unreal 쓰기/Build/PIE/패키징/쿠킹/맵생성·Trello/Figma 수정·키읽기 미실행. md tools2개는 Claude 기존 변경이며 이번 Codex 미수정.

### 감사 처리 수와 항목별 근거

이번 남은58건 전부 대조/처리방향 기록: 문서 정정57건, applications 개인정보1건은 지시서의 수정 금지·사용자 결정 대기로 유지. 누적99건 대조 완료(문서 정정98건·결정 대기1건), 자동으로 개인정보를 가리지 않았으며 해결 완료로 계산하지 않는다. 별도 상대링크11개는 1차 수정, 이번 변경41개 문서와 아카이브 재점검 파일대상 깨진 상대링크0·코드펜스 불균형0. UI 버튼 뒤 괄호 설명처럼 링크가 아닌 표기는 파일 경로 검사에서 제외했다.

| 감사 원본 파일:줄 | 이번 처리 |
|---|---|
| docs/ai/DRONE_SMART_OBJECT_NPC_GUIDE.md:583 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md:73 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_TUTORIAL_IMPLEMENTATION_TEST_GUIDE.md:48 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md:195 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/git/GIT_UNREAL_GUIDE.md:13 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/history/DRONE_WORKLOG.md:2091 | STATUS 원문·당시 스냅샷을 10월 아카이브로 이관, 최신 STATUS 참조·이력 배열 보존 |
| docs/planning/DRONE_PROJECT_PLANNING_BRIEF.md:15 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/planning/DRONE_PROJECT_PLANNING_BRIEF.md:49 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/planning/DRONE_PROJECT_PLANNING_BRIEF.md:218 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/planning/DRONE_TUTORIAL_STORY_PLAN.md:92 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md:7 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md:684 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/tutorial/DRONE_PROTOTYPE_IMPLEMENTATION.md:186 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/ai/DRONE_NPC_GAZE_TRACKING_PLAN.md:73 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/ai/DRONE_NPC_WALK_BACKWARD_HANDOFF_2026-09-18.md:256 | 역사 본문 보존·C PC 로그 경로 정정·현행 진단 기본 False 안내를 새 날짜로 추가 |
| docs/ai/DRONE_SMART_OBJECT_NPC_GUIDE.md:60 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/ai/DRONE_SMART_OBJECT_NPC_GUIDE.md:387 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/applications/PROJECT_EXPERIENCE_PLAN_HWP_GUIDE.md:31 | 수정 금지 준수·STATUS/WORKBOARD 기존 공개 범위/개인정보 결정 대기 유지 |
| docs/assets/DRONE_CONTENT_FOLDER_GUIDE.md:20 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_CHAOS_DATAFLOW_PLAN.md:145 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md:3 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md:224 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_STORY_PHYSICS_TEST_MAP_GUIDE.md:54 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_TEST_MAP_GUIDE.md:36 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md:3 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md:43 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md:71 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md:135 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md:261 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_TUTORIAL_IMPLEMENTATION_TEST_GUIDE.md:414 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md:109 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md:115 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/git/CLAUDE_CODEX_SETUP.md:16 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/git/CODEX_CONTEXT_SYNC.md:187 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/git/DRONE_GIT_LFS_CAPACITY_PLAN.md:102 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/git/DRONE_TEAM_SYNC_PLUGIN_CHECKLIST.md:73 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/git/DRONE_UNREAL_MCP.md:9 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/git/GIT_UNREAL_GUIDE.md:9 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/git/GIT_UNREAL_GUIDE.md:401 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/learning/STUDY_PLANS.md:16 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/planning/DRONE_MVP_GUIDE.md:3 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/planning/DRONE_PREASSET_FUNCTION_PLAN.md:33 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/planning/DRONE_TUTORIAL_STORY_PLAN.md:155 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/planning/DRONE_TUTORIAL_STORY_PLAN.md:191 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/planning/DRONE_TUTORIAL_STORY_PLAN.md:291 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md:11 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md:48 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md:225 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md:1042 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/reference/external-engineering/ADOPTION_PLAN.md:11 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/tutorial/DRONE_PROTOTYPE_IMPLEMENTATION.md:7 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/tutorial/DRONE_PROTOTYPE_IMPLEMENTATION.md:235 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/tutorial/DRONE_PROTOTYPE_PIE_CHECKLIST.md:67 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/tutorial/DRONE_TELEMETRY_IMPLEMENTATION.md:204 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md:5 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md:241 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/tutorial/DRONE_TRAINING_RECORDING_IMPLEMENTATION.md:364 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |
| docs/tutorial/DRONE_TRAINING_ROUTE_SELECTION_TEST_GUIDE.md:56 | 정정 또는 당시 기록 표시·현행 문서/코드 계약 참조 |

### Claude 오후 코드/설정/도구 결과

면접 점검5관점+반박 검증58건(높음7·중간32·낮음19) 중14건 처리(부분처리 포함, 잔여44건은 미처리·결정 필요; 전부 수정으로 표시하지 않음). StateTree HostileStateTree/FriendlyStateTree EditDefaultsOnly Soft참조·기존2개기본값·Controller BP변경·실패 에러 로그·StateTrees AlwaysCook 및 StateTreeCookContract, Moderate 신호 불안정/영상 Noise 미연결·Scout/FPV/Drop 광고문구 정정·VeilBreaker 광섬유 드론으로/끊김규칙미정·PlayerFacingTextContract. Rifle/MG 디버그 선 기본 Off, 상수 TestTrue4건 실제조건, 기체6개이상 경고(동적 목록 후속).

Shotgun NullRHI통과는 미렌더 뼈 미갱신 거짓통과였다. 표본동안 항상뼈갱신 후 NullRHI5.81°·렌더5.04°·기준4°·몸통0°. 표적±1.9°추종+애니메이션 흔들림으로 보임은 Claude 의견, 체감·기준은 사람 판단 대기. 미렌더 표지에서 Shotgun삭제, LobbyLayout samples=0만 유지.

참조0반박 검증 삭제: FDroneHandlingPresetTuning·Pawn Stable/Balanced/AgileHandlingTuning, Selection HandleHandlingPresetClicked, FrontEnd HandleLow/Medium/HighQualityClicked·ApplyGraphicsQuality(현행 Settings 한곳), CollisionResponse NetAttitudeDisturbanceDegreesPerSecond, TrainingGate GateRadiusCentimeters·GetTriggerApertureRadiusCentimeters, AudioSettings SaveMasterVolume(현행 SaveSettings), Pawn SetVisualBankInputGreybox, Definition RoleTags, RecordSubsystem ClearAllRecordsForTesting, 불필요 include·Build.cs 템플릿 주석. HoverThrottleNormalized는 도구3개 호환 유지·런타임 미사용 주석.

Unreal Tools/AssetMigration 삭제12개(삭제됨·Git이력참조): BuildDroneRoleTestArena.py·BuildDroneCarryablePayload.py·ConfigureDroneTutorialMissionObjectiveRule.py·UpgradeMGTurretThreePartAsset.py·PrepareOilRigMap.py·PrepareOilRigPreviewMap.py·CleanOilRigPreviewMap.py·ImportDroneFiberOpticGSU.py·Invoke-DroneFiberOpticGSU.ps1·InspectDronePackShowcase.py·InspectDroneTrainingMap.py·InspectDroneVisualHierarchy.py. ConfigureAutomaticTrainingGates 기본검증·저장 DRONE_TRAINING_GATE_APPLY=1·기존 VALIDATE_ONLY=1도검증만. 타이틀 최초 임포트 DRONE_TITLE_ASSET_DIR/-TitleAssetDir필수. md HostileCoverResponse TestMap은 Claude 기존수정. DefaultEngine중복키2줄삭제·DefaultGame ProjectName=Drone, CLAUDE MCP공유Default/문서위임하루상한삭제. 삭제도구를 현재절차로 실행하지 않음.

Build Succeeded는 지시서 근거. StateTreeCookContract·PlayerFacingTextContract·FrontEndContract·FlightProfiles통과, AI/UI NullRHI22개중20Success·NPCPerception/Shotgun알려진2Fail. 지정 전체로그 ClaudeInterviewFull/test.log를 읽기 대조: Drone.*97개중86Success·11Fail. 포커스6개는PIE미렌더 판정제외, 나머지알려진5개는NPCPerception·Shotgun실제동작·LobbyLayout진단·TrainingAssets/TrainingPIESmoke팀원Production맵. 오늘10회중8미렌더는Claude지시서, 실제패키징미실행·수동Pass추정없음.

WORKBOARD/STATUS에 영향순서 결정11개(약51GB라이선스/공개·본인기여/AI활용·루트README·상시실패4개·Pawn분리/명명·Legacy76/100·Bangkok987/약12GB·풍향·MCP공유자동시작·미사용함수19/접근자71/Legacy·Shotgun)를 기록했다. 기존 스토리·기본값·applications/OpenRouter 결정대기 보존. 코드작업은 결정전실행하지 않으며 INTERVIEW-CLEANUP-01로인계 추적.

### 원문 이관·전후 크기

파일크기는 실행직전 실제바이트·LF개수+1 기준(감사의75KB/42KB는1차이전관찰이며 이번실측과 구분).

| 파일 | 이전 바이트/줄 | 이후 바이트/줄 |
|---|---:|---:|
| docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md | 75196 / 1056 | 63174 / 962 |
| docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md | 37844 / 251 | 23626 / 163 |

옮긴 절(원문9/9 보존 확인·상대링크 경로만 이관기준정정):

- docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md — 2026-10-04 최신 Acro 입력·데드존·응답 조정 (C PC)
- docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md — 2026-10-03 밤 최신 Blueprint 조정 — 5메뉴·조종 입력 표시·레이싱 키
- docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md — 현재 검증 기준선
- docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md — 2026-09-08 현재 역할·Front-end·Mission 구조
- docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md — 1. 이전 4메뉴 구현 기록 (2026-10-01)
- docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md — 8. 도구와 확인할 것
- docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md — 10. 목록 튐 진단 (수정 전)
- docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md — 11. 패드 UI 확인 범위
- docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md — 배터리·신호 대역·HUD 조정 (2026-10-02 새벽, C PC)

WORKLOG의 STATUS10월원문·중복세션·이전현재스냅샷은 archive/STATUS_2026-10.md에 원문 이관. WORKLOG H1중복 제거·머리최신날짜/새기록끝추가원칙·루트STATUS참조, 기존순서/도구명/검증과이력내용보존.

### Drone Space 저장·재조회

기존 진행상황과다음작업6·테스트맵과확인가이드2·Blueprint조정과팀원가이드4개 연산(총12) 저장, 12/12 기대본문 재조회 정확일치. 비대상 기존블록49/41/50개 원문보존 확인. 새Page/공유권한/예약자동화없음. 이번대상미반영없음, 로컬미커밋본문GitHub는사용자Commit/Push뒤반영.

### 변경 파일(이번 실행 기준)

- docs/ai/DRONE_NPC_GAZE_TRACKING_PLAN.md
- docs/ai/DRONE_NPC_WALK_BACKWARD_HANDOFF_2026-09-18.md
- docs/ai/DRONE_SMART_OBJECT_NPC_GUIDE.md
- docs/ai/DRONE_SMART_OBJECT_ROUTE_EDITING_GUIDE.md
- docs/assets/DRONE_BANGKOK_OILRIG_MIGRATION_2026-09-30.md
- docs/assets/DRONE_CONTENT_FOLDER_GUIDE.md
- docs/gameplay/DRONE_CHAOS_DATAFLOW_PLAN.md
- docs/gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md
- docs/gameplay/DRONE_JAMMING_GREYBOX_GUIDE.md
- docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md
- docs/gameplay/DRONE_STORY_PHYSICS_TEST_MAP_GUIDE.md
- docs/gameplay/DRONE_TEST_MAP_GUIDE.md
- docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md
- docs/gameplay/DRONE_TUTORIAL_IMPLEMENTATION_TEST_GUIDE.md
- docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md
- docs/git/CLAUDE_CODEX_COLLABORATION.md
- docs/git/CLAUDE_CODEX_SETUP.md
- docs/git/CODEX_CONTEXT_SYNC.md
- docs/git/DRONE_GIT_LFS_CAPACITY_PLAN.md
- docs/git/DRONE_TEAM_SYNC_PLUGIN_CHECKLIST.md
- docs/git/DRONE_UNREAL_MCP.md
- docs/git/GIT_UNREAL_GUIDE.md
- docs/history/DRONE_WORKLOG.md
- docs/learning/STUDY_PLANS.md
- docs/planning/DRONE_FIGMA_MISSION_IMPLEMENTATION_MATRIX.md
- docs/planning/DRONE_MVP_GUIDE.md
- docs/planning/DRONE_PREASSET_FUNCTION_PLAN.md
- docs/planning/DRONE_PROJECT_PLANNING_BRIEF.md
- docs/planning/DRONE_TUTORIAL_STORY_PLAN.md
- docs/README.md
- docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md
- docs/reference/external-engineering/ADOPTION_PLAN.md
- docs/tutorial/DRONE_PROTOTYPE_IMPLEMENTATION.md
- docs/tutorial/DRONE_PROTOTYPE_PIE_CHECKLIST.md
- docs/tutorial/DRONE_TELEMETRY_IMPLEMENTATION.md
- docs/tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md
- docs/tutorial/DRONE_TRAINING_RECORDING_IMPLEMENTATION.md
- docs/tutorial/DRONE_TRAINING_ROUTE_SELECTION_TEST_GUIDE.md
- STATUS.md
- WORKBOARD.md
- docs/history/archive/STATUS_2026-10.md


### 최종 Git 확인

정상 저장소 설정의 git diff --check exit0 확인. CRLF 변환 경고는 기존 저장소 줄바꿈 설정이며 내용 검증 실패가 아니다. 아래는 전체 작업트리의 git -C <md> status --short 결과(이번41개와 1차/Claude 기존 변경을 포함한다). Commit/Push 미실행.

```text
 M CLAUDE.md
 M CONTEXT.md
 M README.md
 M STATUS.md
 M WORKBOARD.md
 M WORK_PC_START_HERE.md
 M docs/README.md
 M docs/ai/DRONE_MG_TURRET_3PART_GUIDE.md
 M docs/ai/DRONE_NPC_GAZE_TRACKING_PLAN.md
 M docs/ai/DRONE_NPC_WALK_BACKWARD_HANDOFF_2026-09-18.md
 M docs/ai/DRONE_SMART_OBJECT_NPC_GUIDE.md
 M docs/ai/DRONE_SMART_OBJECT_ROUTE_EDITING_GUIDE.md
 M docs/assets/DRONE_BANGKOK_OILRIG_MIGRATION_2026-09-30.md
 M docs/assets/DRONE_CONTENT_FOLDER_GUIDE.md
 M docs/gameplay/DRONE_CHAOS_DATAFLOW_PLAN.md
 M docs/gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md
 M docs/gameplay/DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md
 M docs/gameplay/DRONE_JAMMING_GREYBOX_GUIDE.md
 M docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md
 M docs/gameplay/DRONE_STORY_PHYSICS_TEST_MAP_GUIDE.md
 M docs/gameplay/DRONE_TEST_MAP_GUIDE.md
 M docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md
 M docs/gameplay/DRONE_TUTORIAL_IMPLEMENTATION_TEST_GUIDE.md
 M docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md
 M docs/gameplay/DRONE_WEATHER_WIND_RAIN_PLAN.md
 M docs/git/CLAUDE_CODEX_COLLABORATION.md
 M docs/git/CLAUDE_CODEX_SETUP.md
 M docs/git/CODEX_CONTEXT_SYNC.md
 M docs/git/DRONE_GIT_LFS_CAPACITY_PLAN.md
 M docs/git/DRONE_TEAM_SYNC_PLUGIN_CHECKLIST.md
 M docs/git/DRONE_UNREAL_MCP.md
 M docs/git/GIT_UNREAL_GUIDE.md
 M docs/history/DRONE_WORKLOG.md
 M docs/learning/STUDY_PLANS.md
 M docs/planning/DRONE_FIGMA_MISSION_IMPLEMENTATION_MATRIX.md
 M docs/planning/DRONE_FRONTEND_MISSION_FLOW_PLAN.md
 M docs/planning/DRONE_MVP_GUIDE.md
 M docs/planning/DRONE_PREASSET_FUNCTION_PLAN.md
 M docs/planning/DRONE_PROJECT_PLANNING_BRIEF.md
 M docs/planning/DRONE_TUTORIAL_STORY_PLAN.md
 M docs/planning/WORK_MANAGEMENT.md
 M docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md
 M docs/reference/external-engineering/ADOPTION_PLAN.md
 M docs/tutorial/DRONE_PROTOTYPE_IMPLEMENTATION.md
 M docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md
 M docs/tutorial/DRONE_PROTOTYPE_PIE_CHECKLIST.md
 M docs/tutorial/DRONE_TELEMETRY_IMPLEMENTATION.md
 M docs/tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md
 M docs/tutorial/DRONE_TRAINING_COURSE_IMPLEMENTATION.md
 M docs/tutorial/DRONE_TRAINING_RECORDING_IMPLEMENTATION.md
 M docs/tutorial/DRONE_TRAINING_ROUTE_SELECTION_TEST_GUIDE.md
 M tools/unreal/Setup-DroneHostileCoverResponse.py
 M tools/unreal/Setup-DroneNPCGreybox.py
?? docs/history/archive/
```

## 2026-10-04 Shotgun 판정 정정 — C PC, Claude 실행·Codex docs 반영

오늘 2차의 실제 머리 흔들림·사람 판단 대기는 잘못된 판정이었다. 과거 기록은 보존하고 후속으로 정정한다. AI-SHOTGUN-RENDER-01 해결(2026-10-04 C PC Claude). 표적 고정 시 머리4.2~4.4°(Idle·사격 애니메이션), 표적±1.9° 왕복 시 머리5.2~5.4°·SmoothedDroneLookRotation 1.45°. 9/18 몸 Hysteresis·Bone Gaze 보간(데드존 경계 0 Snap 없음)은 정상, 5~6° 대부분은 9월 하순 Rifle 계열 AnimBP 교체 뒤 애니메이션 흔들림이다. 절대 머리4° 판정(애니메이션 포함)과 미렌더 뼈 정지에 따른 NullRHI 거짓 통과가 원인. 표적 고정0.6초 기준 측정 후 시선 출력≤2.5°·애니메이션 대비 추가 머리 흔들림≤2.5°로 시험 정정(경계0↔±1.9° 튐3.8° 검출). NullRHI·렌더 Success(ClaudeInterview/shotgun3_*.log), known-test-failures에서 제외(Claude 지시서 근거). 근거: Claude 지시서·Saved/Automation/ClaudeInterview/shotgun2_*.log·shotgun3_*.log. Codex는 성공 로그를 읽기 전용 대조했고 엔진 실행·Unreal 수정·Commit/Push는 하지 않았다. 전체97/86·11Fail과 AI/UI22/20은 당시 수치로 보존하며 후속 집중 성공을 합산하지 않는다.

STATUS·WORKBOARD·테스트 가이드의 Shotgun 판단 대기를 해제로 정정했다. reference 미구현·현재 미정에 엄폐, MG 승하차/최종 난이도, NPC 래그돌/시체·Drone 폭발/Respawn, Drone Class 정책, Network/Multiplayer 권한을 Git HEAD 근거로 복원했다.

Drone Space: 기존 진행상황과 다음 작업 3개·테스트 맵과 확인 가이드 2개 연산 모두 적용, 저장 후 대상 블록 재조회로 기대 본문 일치 확인. Shotgun 항목만 정정했고 새 페이지·다른 주제·과거 기록은 변경하지 않았다. 이번 범위 미반영 없음. git diff --check 통과(기존 CRLF 변환 경고), 변경 파일은 STATUS.md·WORKBOARD.md·docs/history/DRONE_WORKLOG.md·docs/gameplay/DRONE_TEST_MAP_GUIDE.md·docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md 5개, 기존 작업트리 변경과 구분한다.

## 2026-10-04 NPC 걷기 미재생 수정 — C PC, Claude 실행·Codex docs 반영

사용자 보고: NPC가 선 채로 움직임. 9/29 검증은 자산 연결뿐이어서 실제 재생은 확인되지 않았다. ABP_NPC_Rifle_Greybox·ABP_NPC_Unarmed_Greybox는 UE 템플릿 ABP_Unarmed 복제본의 ShouldMove(지면 속도 > 3 AND CurrentAcceleration ≠ 0)를 사용했다. AI 경로 이동은 기본 bUseAccelerationForPaths=false, 개인화기 추적은 9월에 의도한 직접 속도 추종으로 가속도0→Idle이었다. Claude는 이동 코드를 유지하고 UDroneNPCAnimationAuthoringLibrary::UseVelocityOnlyLocomotionGate/ValidateVelocityOnlyLocomotionGate로 두 AnimBP 이벤트 그래프를 속도 조건만으로 수정·두 자산 저장, Rifle Gaze 체인 유지 확인. Tools/AssetMigration/BuildNPCGreyboxAnimationAssets.py·VerifyNPCGreyboxAnimationAssets.py에도 반영해 재생성 유지·검증 통과. 시험은 Drone.AI.NPCLocomotionAnimPIE(TestMap/Lvl_NPCSmartObjectGreybox 순찰 이동), 로그는 C:\URproject\drone\Saved\Automation\ClaudeNPCWalk\before.log·after.log. Codex는 엔진을 실행하지 않았다.

AI-LOCOMOTION-01 구현됨·자동 검증됨(2026-10-04 C PC Claude 재생 확인)·수동 확인 대기. 두 AnimBP의 ShouldMove를 속도 > 3만으로 수정: 수정 전 이동 표본41개 중0→수정 후40개(NPC8명) 모두 ShouldMove·걷기/뛰기 BlendSpace 진입. Drone.AI 19개 중18 Success·기존 NPCPerceptionSearchPIE 1 Fail, Shotgun 시선 Success. Claude 지시서 근거(ClaudeNPCWalk/before.log·after.log). 자연스러운 순찰/추적 전환·발 미끄러짐(속도 대비 보폭)·뒷걸음 방향 수동 확인 대기. Epic 마네킹 임시 동작·최종 아님. 기존 전체 회귀 수치와 합산하지 않는다. STATUS·WORKBOARD·NPC 가이드·테스트 가이드 반영. Unreal 수정·Build/PIE·Commit/Push 없음.

Drone Space: 기존 진행상황과 다음 작업·테스트 맵과 확인 가이드의 NPC 걷기 항목 각1개 연산 적용, 저장 후 재조회로 기대 본문 일치 확인. 이번 범위 미반영 없음. 기존 작업트리 변경 보존, 이번 변경 파일은 STATUS.md·WORKBOARD.md·docs/history/DRONE_WORKLOG.md·docs/ai/DRONE_SMART_OBJECT_NPC_GUIDE.md·docs/gameplay/DRONE_TEST_MAP_GUIDE.md 5개.

## 2026-10-04 NPC 소총 IK Retarget·총 오른손 부착 후속 — C PC, Claude 실행·Codex docs 반영

기준: Unreal HEAD `41444c2` + 이번 도구·Editor 작성 함수·검증 시험·변환/연결 자산 미커밋(그 밖의 미커밋은 이전 작업분, Claude 지시서 기준). md HEAD `94f6375`, 작업 전 git status --short 출력 없음. 두 HEAD를 읽기 전용으로 확인했다. 작업·검증 Claude, 문서·Space 반영 Codex. 지시서: `C:\URproject\drone\.claude\codex-bridge\runs\20261004-205005-docs-docs-npc-rifle-retarget\prompt.md`.

사용자 보고의 양팔 벌림은 Mannequin AnimBP/Sequence와 적 Insurgent·아군 Quantum 스켈레톤의 불일치 때문이었다. 사용자가 선택한 IK Retarget으로 IK Rig3개·Retargeter2개, Insurgent 소총24개·Quantum 비무장22개 변환. 적 Rifle/Shotgun은 ABP_NPC_Rifle_Greybox_Insurgent·변환 Fire/Reload, 아군은 ABP_NPC_Unarmed_Greybox_Quantum으로 연결했다. 원본 ABP_NPC_*_Greybox는 변환 원본으로만 남기고 속도 > 3 판정·Gaze 그래프·발사 가산 설정을 유지했다. Gun 캡슐 고정을 hand_r 부착으로 교체하고 조준 Idle 첫 프레임 환산 오프셋(소총 약 10cm, 산탄총 약16cm)으로 Idle 모습과 동작 중 손 추종을 유지했다. Editor 전용 AttachBlueprintComponentToMeshSocket·GetBlueprintComponentAttachment 추가, Build 원본 생성만/Retarget 연결/Attach 손 부착/Verify 검증 순서로 정리했다. 변경 도구: Tools/AssetMigration/RetargetNPCAnimationAssets.py·AttachNPCWeaponsToHands.py(신규), BuildNPCGreyboxAnimationAssets.py·VerifyNPCGreyboxAnimationAssets.py(후속 정리). 시험 NPCGreyboxAssets에 스켈레톤 일치, NPCLocomotionAnimPIE에 위팔20° 이상·양손 간격60cm 이하·보이는 총 hand_r 추종·왼손 총 위 검사를 추가했다(구현 사실은 Claude 지시서 근거).

AI-LOCOMOTION-01 후속 구현됨·자동 검증됨(2026-10-04 C PC, 작업·검증 Claude)·수동 확인 대기. Mannequin 원본과 Insurgent/Quantum 메시의 스켈레톤 불일치로 양팔을 벌리던 문제를 사용자 선택 IK Retarget으로 수정하고 적 Gun을 hand_r에 부착. 속도 > 3 이동 판정·Gaze 유지. NPCLocomotionAnimPIE 오프스크린 Success: 이동40개(NPC5명) ShouldMove40, 위팔 기본 자세 대비 평균51.7°·40/40, 총 든 NPC 양손 간격 평균34.4cm·24/24, 총 hand_r 추종·왼손 총 위 각각24/24. Drone.AI 19개 중18 Success·기존 NPCPerceptionSearchPIE 1 Fail(state=1 detected=0), 새 실패 없음. 자산 Verify success(ClaudeNPCWalk/rt_tests3.log·ai_suite.log·verify_rt3.log). 걷기/뛰기 전환·발 미끄러짐·뒷걸음 방향·손/총 정렬(특히 산탄총)·사격/재장전은 사용자 수동 확인 대기. CR_Mannequin_FootIK는 Insurgent 계층 차이로 Editor 컴파일 경고 잔존. Epic 마네킹 변환 임시 동작·최종 아님; 최종 애니메이션 미구현·자산 미정, 산탄총 전용 동작 미구현·도입 여부 미정(소총 동작 공유).

검증 조건: TestMap/Lvl_NPCSmartObjectGreybox, 렌더 오프스크린. 로그 전체 경로는 `C:\URproject\drone\Saved\Automation\ClaudeNPCWalk\rt_tests3.log`·`ai_suite.log`·`verify_rt3.log`. Codex가 시험 성공·위팔/양손/부착 수치·AI 19개 결과·Verify success를 읽기 전용 대조했다. Claude Editor Simulate의 적 총 들고 걷기·조준/아군 비무장 걷기는 지시서의 after1_crop.png·after_friendly_crop.png 근거이며 Codex 직접 화면 확인이나 사용자 수동 Pass로 쓰지 않는다. 이전 40개(NPC8명) 속도 조건 수정 기록은 당시 이력으로 보존하며 이번 40개(NPC5명) 자세 검증과 합산하지 않는다.

STATUS AI·차량·날씨 행, WORKBOARD AI-LOCOMOTION-01 카드/Next7, NPC 가이드의 변환 AnimBP 경로·도구 순서·검증 기준, 테스트 맵 Smart Object 확인 순서에 손/총 정렬·사격/재장전을 반영했다. 기존 날짜별 기록은 변경하지 않고 끝에 추가했다. 새 파일·문서 다이어트·Unreal 수정·엔진 Build/PIE/도구 실행·Commit/Push·Trello/Figma 수정 없음.

Drone Space: 기존 진행상황과 다음 작업·테스트 맵과 확인 가이드의 NPC 걷기 항목 각1개 연산 적용(진행 sequence22, 테스트 sequence15). 저장 후 두 대상 블록을 다시 읽어 기대 본문과 일치 확인. 이번 범위 미반영 없음. 최종 NPC 애니메이션 자산·산탄총 전용 동작 여부는 현재 미정으로 유지했다.

## 2026-10-05 사용자 결정 D-7·D-9·D-10·D-15 — C PC, Codex 문서 반영

결정 사용자(총괄 세션 경유 전달), 문서 반영 Codex. 지시서 `C:\URproject\drone\.claude\codex-bridge\runs\20261005-180714-docs-docs-decisions-1005\prompt.md` 근거로 WORKBOARD 두 결정 표의 D-7·D-9·D-10 상태 행만 갱신했다. 결정 내용 정본은 [WORKBOARD 결정 표](../../WORKBOARD.md#결정-필요--현재-da-값은-채택-사양이-아님). D-7 비공개 전환은 사용자 직접 확인·처리 대기이며 공개 상태 관찰은 Claude 비로그인 curl HTTP 200(10/05 C PC, 로그 미저장) 전달 근거이고 Codex 재검증은 아니다.

D-15 확정(2026-10-05 사용자 결정): 로컬 미커밋 변경은 커밋만 하고 푸시는 나중에 사용자 지시 시 진행. 커밋 전 묶음별로 나누어 커밋 메시지를 정리하고 사용자 확인 후 Claude가 커밋 실행. 지정된 두 결정 표에는 해당 행이 없어 다른 행·절은 수정하지 않았다. 나머지 D-1~6·8·11~14는 현재 미정 유지. 구현/자동 검증/수동 확인/미구현 분류는 해당 없음(결정 기록).

지시서 기준 Unreal `41444c2` + 미커밋(이번 작업 없음), md `94f6375` + 10/04 NPC Retarget 미커밋 5파일. 실제 작업 전 git status에는 AGENTS.md·CLAUDE.md를 포함한 기존 수정 7파일이 있었으며 보존했다. STATUS·applications·Unreal·Space 수정, Build/PIE, Commit/Push 없음. Space는 지시서에 따라 제외. WORKBOARD는 갱신 전 42,138바이트로 30KB 초과; 다이어트 대상 없음 지시에 따라 아카이브하지 않았다.

## 2026-10-05 사용자 결정 2차 — C PC, Codex 문서 반영

결정 사용자(총괄 세션 경유 전달), 문서 반영 Codex. 지시서 `C:\URproject\drone\.claude\codex-bridge\runs\20261005-184640-docs-docs-decisions-1005b\prompt.md` 근거. WORKBOARD 두 결정 표·관련 카드·Next 반영, 결정 정본은 [WORKBOARD](../../WORKBOARD.md)에 둔다. D-1·D-2 보류, D-3 기존 구현과 일치, 후속 구현/실행 대기를 구분했다. 이번 구현·자동 검증 없음. 지시서 기준 Unreal `41444c2` + 미커밋, md `94f6375` + 미커밋이며 현재 HEAD 재검증 결과로 쓰지 않는다. 미사용 자산 판정 출처는 지시서의 unused_packs.json이며 Codex 재검증이 아니다.

STATUS·applications·README·Unreal 수정, 새 파일·아카이브, Build/PIE·Commit/Push 없음. Space는 지시서에 따라 제외. WORKBOARD 30KB 초과는 이번 다이어트 대상 없음에 따라 유지·다음 위임 정리 대기. 배터리 시간·코스 실제 지형·장치 자동 전환·D-1/D-2·D-13 나머지 목록은 현재 미정. 과거 WORKLOG 내용은 보존했다.

## 2026-10-05 D-5·D-6·D-11·D-12(1차)·D-14 반영 — C PC, Claude 작업·검증·Codex 문서

지시서: `C:\URproject\drone\.claude\codex-bridge\runs\20261005-194407-docs-docs-impl-1005\prompt.md`(UTF-8 읽기). 날짜/PC 2026-10-05 C PC, 구현·자동 검증 Claude, 문서 Codex. Unreal HEAD와 origin/main `3f02577`을 Codex가 읽기 전용 확인했다. 사용자 푸시 + 아래 변경 스테이징은 Claude 지시서 근거이며 커밋은 사용자 담당. md 실제 HEAD는 `76f7a3f`로 지시서 기준 `94f6375`와 다르다. 기존 WORKBOARD·WORKLOG 미커밋 2파일을 보존했다. Codex는 엔진 Build·PIE·패키징·쿠킹·맵 생성/재생성·Unreal 파일 수정·Commit/Push를 하지 않았다.

### 구현 사실·남은 범위(Claude 지시서 근거)

- D-14: 공유 `Config/DefaultEditorPerProjectUserSettings.ini`의 MCP `bAutoStartServer=False`. MCP가 필요한 PC만 Git 제외 `Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini`의 `[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]`에 `bAutoStartServer=True`. C PC 로컬 설정으로 Editor 실행15초 뒤8000 응답 확인(Claude 지시서, Codex가 Editor를 실행하거나 접속한 결과 아님). 다른 PC의 실제 연결은 별도 확인. 현재 절차 정본은 [협업 세팅 MCP 절](../git/CLAUDE_CODEX_SETUP.md#unreal-mcp-자동-시작--pc별-로컬-설정).
- D-11: 상시 실패4개 경로를 `KnownIssues.AI.NPCPerceptionSearchPIE`·`KnownIssues.Flow.LobbyLayoutStabilityPIE`·`KnownIssues.Tutorial.TrainingAssets`·`KnownIssues.Tutorial.TrainingPIESmoke`로 변경, 기본 `Automation RunTests Drone.`에서 제외. `.claude/known-test-failures.md` 갱신. 그룹 분리는 실패 원인 해결이 아니다. LobbyLayout 진단이 기본 회귀에 없어 미렌더는 패드 포커스6개 모두 화면 루트 포커스로 실패하는지로 판단한다.
- D-6 풍향: HUD 방위와 통일(+X=북000°·+Y=동090°), 불어오는 쪽 표기(+X로 부는 바람=풍향 S). 바람 물리는 유지. HUD 표기는 수동 확인 대기.
- D-6 배터리: 방전 처리 추락 추가(동력 상실→조종 정지→중력 낙하→땅/구조물 접촉 또는8초 뒤 파괴→기존 파괴 실패/재출격). 미션 DA `BatteryLimitSeconds`(0=기체 값)·`BatteryDepletedResponse`(기본 추락). 현재 기체 DA 배터리 시간 모두0으로 시간 값 확정 전 실제 게임 동작 변화 없음. 시간 값 현재 미정·미설정, 확정 뒤 추락 체감 수동 확인 대기. 높이 제한 보류·미구현.
- D-5: 출격 후 스타트 지점 중앙3·2·1→출발!, 카운트다운 조종 잠금·기체 정지. 출발부터 미션 시간(결과 창 클리어 시간)과 목표 제한 시간 시작. 미션 DA `StartCountdownSeconds`(레이싱=3). 맵 선택은 기존 레이싱 분류 코스 목록, 완주는 기존 게이트 통과, 기록은 결과 창 클리어 시간. 카운트다운 화면/체감 수동 확인 대기. 현재 레이싱1개, 코스4개는 지형 현재 미정·미구현.
- D-12 1차: Legacy C++ Variant_*39클래스+3인칭 템플릿3클래스, 자산100개(Variant_Combat30·Variant_Platforming10·Variant_SideScrolling18·ThirdPerson4·LevelPrototyping29·Input9) 삭제. 삭제 전 외부 참조0. Characters(마네킹)는 NPC 동작 변환 원본으로 유지. 미사용 UFUNCTION18개 삭제. Prototype Pawn 분리·이름 변경은 미구현·새 이름 결정 대기.
- D-13 앞선 작업: 방콕 잔여987개 삭제됨(Claude 지시서). 사용자 커밋·푸시 완료분인지 사용자 확인 필요, 완료로 추정하지 않음. D-1·D-2는 기획자 내용 대기·현재 미정.

### 자동 검증 출처·읽기 전용 대조

| 검사 | 결과·판정 | 출처(C:\URproject\drone 아래) |
|---|---|---|
| D-12 뒤 Drone.+KnownIssues. 전체 | 99개, 실패는 KnownIssues4개와 미렌더 실행의 알려진 패드 포커스6개뿐(Claude 지시서). Codex 로그 대조89 Success·10 Fail, 다른 실패 경로 없음 | Saved/Automation/ClaudeD12/full2.log |
| D-6 | Drone.Weather5·Drone.Mission7·Drone.Health.BatteryHUDPIE Success | Saved/Automation/ClaudeD6/t1.log·t4.log |
| D-5 신규 | Drone.Mission.RacingStartCountdownPIE Success | Saved/Automation/ClaudeD5/t1.log |

구현·자동 검증은 위 Claude 결과이며 사용자 수동 Pass나 이번 Codex 엔진 실행 결과가 아니다. Codex는 지정 로그의 완료 결과를 읽기 전용 대조했다. 이전 전체97/86·11Fail 등은 당시 기록으로 보존하고 이번 전체99개 또는 집중 검사와 합산하지 않는다.

### WORKBOARD 원문 보존·문서 반영

WORKBOARD만 기준2026-10-05로 다이어트했다. 현재 카드의 긴 근거·완료/종료 행·지난 Next를 포함한 이동 전 원문 절을 기존 [WORKBOARD_2026-10 아카이브](archive/WORKBOARD_2026-10.md) 끝에 그대로 보존하고, 루트 보드는 현재 진행/대기 카드·결정 표와 Next로 요약했다. 기존 아카이브 본문은 변경하지 않았다. 완료/종료 AI-SHOTGUN-RENDER-01·AI-SHOTGUN-REGRESS-01·TEST-NPC-COUNT-01·INTERVIEW-CLEANUP-01·MCP-LOCAL-01·D-9·D-10 행은 현재 표에서 제외; 남은 수동 사격/감지/패키징/다른 PC 확인 카드는 유지했다. 이력 보존 후 구현 상태를 갱신했으며 과거 카드 문장을 덮어쓰지 않았다.

- WORKBOARD: 44,648바이트·160줄 → 29,978바이트·111줄(UTF-8, 30,000바이트 이하).
- WORKBOARD_2026-10 아카이브: 16,196바이트·107줄 → 60,899바이트·265줄.
- 옮긴 원문 절 제목: `회의 후 역할별 카드`, `결정 필요 — 현재 DA 값은 채택 사양이 아님`, `면접 대비 결정 필요 — 영향 순서(10/05, 결정·구현 대기 구분)`, `사용자가 지금 확인할 맵`, `Next`. 현재 카드·미정 결정은 루트 보드에 요약/링크로 유지했다.
- STATUS: 현재 Git·레이싱·배터리·풍향·KnownIssues·Legacy/MCP 및 수동/미구현 상태 반영. WORKBOARD: D-5·D-6·D-11·D-12·D-14 관련 행/카드와 D-13 삭제 상태, Next 갱신. CLAUDE_CODEX_SETUP: MCP 자동 시작 절만 PC별 로컬 설정 절차로 교체. docs/README: 기존 아카이브 색인 설명 최신화. WORKLOG: 이번 결과는 이 끝 절에만 추가.

Drone Space는 지시서의 “Space 제외(다음 묶음에서)”에 따라 갱신하지 않았다. 이번 구현/보드 정리의 Space 반영은 다음 묶음 미반영 범위다. applications·Trello·Figma·공유 권한·예약 자동화 수정 없음. 새 파일 없음(기존 아카이브에 추가). 문서 저장소 최종 git status --short로 이번 변경6파일을 확인하고, git diff --check와 30KB 기준·원문 보존을 점검했다.

## 2026-10-05 NPC 다리·높이 제한 매니저·매니저 폴더 정리 — C PC, Claude 작업·검증·Codex 문서

지시서: `C:\URproject\drone\.claude\codex-bridge\runs\20261005-204432-docs-docs-legs-alt-mgr\prompt.md`(UTF-8 읽기). 구현·자동 검증 Claude, 문서 반영 Codex. Unreal 기준은 지시서의 원격 `3f02577` + 스테이징(커밋은 사용자), md 실제 HEAD `76f7a3f`. 기존 미커밋 STATUS·WORKBOARD·README·CLAUDE_CODEX_SETUP·WORKLOG·WORKBOARD_2026-10 아카이브 변경을 보존했다. 이번 수치·판정은 Claude 지시서 근거이며 Codex가 엔진이나 테스트를 실행한 결과가 아니다.

### NPC 다리 정지 수정·검증

사용자 보고 “상체는 나아졌는데 다리가 안 움직인다”의 원인은 IK Retarget 체인에 없는 ik_foot_l/r가 기본 자세에 남고 AnimBP의 CR_Mannequin_FootIK가 발을 그 뼈로 끌어당긴 것이다. 걷기 데이터 자체의 다리 움직임은 있었다. Retargeter Pin Bone 단계(ik_foot ← foot, ik_hand ← hand, ik_hand_gun ← hand_r) 추가로 아군 Quantum 해결. 적 Insurgent는 Pin 뒤에도 IK 뼈가 기본 자세에 남아 원인 미특정이며, 적 AnimBP에서 발 IK Control Rig 노드를 우회·삭제했다. 적 NPC는 경사면 발 맞춤이 없다. 양손 총 파지·총 hand_r 부착은 유지했다.

Drone.AI.NPCLocomotionAnimPIE에 걷는 동안 두 발 앞뒤 간격 변화(2초 이상 표본) 보폭 판정을 추가했다. 수정 전 NPC8명 모두0cm → 수정 후155~200cm, 2회 연속 Success(10/05 C PC Claude 지시서 근거). 이전 상체/부착 검증과 이번 보폭 검증은 별도 기록이며 사용자 수동 Pass로 간주하지 않는다.

### D-6 높이 제한

사용자 요청 “매니저를 깔고 BP에 값을 넣으면 적용되게 구현만”에 따라 ADroneAltitudeLimitManager와 `/Game/Drone/Managers/BP_DroneAltitudeLimitManager` 구현됨·자동 검증됨. 레벨 배치 위치 Z + MaxAltitudeMeters가 천장이다. MaxAltitudeMeters 시험값120m·WarningMarginMeters5m, 천장에서 위치 되돌림·상승 속도 제거, OnAltitudeLimitReached 이벤트 제공(경고 연출은 BP). 높이 제한 수치·경고 연출은 현재 미정이며 시험값을 확정 사양으로 쓰지 않는다. Drone.Flight.AltitudeLimitPIE Success(10/05 C PC Claude).

### D-13 종료·매니저 폴더 정리

D-13 사용자 결정 정본은 [WORKBOARD](../../WORKBOARD.md)의 Bangkok 행이다. 방콕만 삭제하고 나머지 폴더 유지로 종료했으며, 커밋·푸시 완료를 추정하지 않는다.

사용자 요청 매니저 폴더 정리 구현됨·자동 검증됨. `/Game/Drone/Managers`로 BP_DroneMissionManager(이전 `/Game/Drone/Mission/Blueprints/Managers`), BP_DroneRandomWeatherController·BP_DroneWeatherDebugVisualizer(이전 `/Game/Drone/Weather/Blueprints`)를 이동했다. 참조 자산 BP_DroneMissionPlayerController 및 TestMap/Lvl_DroneWeatherSystemsTest를 다시 저장한 뒤 옛 경로 Redirector를 삭제했다. 팀원 Production 맵 참조 없음. GameMode·PlayerController BP와 BP_DroneRainVisual은 이동하지 않았다. 목록 원본: `C:\URproject\drone\Saved\Managers_Move_List_20261005.md`(Claude 지시서 근거).

매니저 이동 뒤 전체 회귀100개, 알려진 실패만(KnownIssues4·미렌더 포커스6). 로그: `C:\URproject\drone\Saved\Automation\ClaudeAltitude\full.log`. 수치·판정은 10/05 C PC Claude 결과이며 KnownIssues 해결·수동 검증 완료를 뜻하지 않는다.

### 문서 반영·수동 확인 대기

STATUS 현재 AI·미션·날씨/환경·전체 회귀 상태, WORKBOARD AI-LOCOMOTION-01·D-6 높이 제한·D-13 종료·MANAGERS-FOLDER-01 및 Next를 갱신했다. CONTEXT·Mission 프레임워크 가이드(폴더 트리 포함)·테스트 맵 가이드·날씨 계획의 지정 BP 경로를 새 경로로 정정했다. 상세 결과는 이 WORKLOG 끝에만 추가하고 이전 기록은 변경하지 않았다.

수동 확인 대기: Lvl_NPCSmartObjectGreybox NPC 걷기 다리·발 미끄러짐(속도 대비 보폭), 높이 제한 체감, 날씨 시험 맵 정상 동작. 현재 미정: 높이 제한 수치·경고 연출·Pawn 새 이름·배터리 시간·코스4개 지형. Space는 지시서에 따라 제외·이번 변경 미반영. applications·history/archive 수정, 아카이브/새 파일 생성, Unreal 수정·Build·PIE·Commit/Push·Trello/Figma 수정 없음. 기존 아카이브 미커밋 변경은 이전 작업분이다.

DOC_SIZES: STATUS.md 20,982바이트·101줄, WORKBOARD.md 30,579바이트·113줄. WORKBOARD는 운영 기준30,000바이트 초과 경고이며 이번 지시의 ‘다이어트 없음’에 따라 아카이브하지 않았다. git diff --check 오류 없음, 최종 git status --short 변경10파일 중 이번 변경7파일·이전 작업만의 변경3파일(README·CLAUDE_CODEX_SETUP·WORKBOARD_2026-10 아카이브)을 구분했다.

## 2026-10-06 D-5 랩 타이머·D-12 Flight 이름 변경/분리·CLAUDE.md MCP 반영 — C PC, Claude 작업·검증·Codex 문서

지시서: `C:\URproject\drone\.claude\codex-bridge\runs\20261006-013613-docs-docs-d12-split\prompt.md`(UTF-8 읽기). 구현·자동 검증 Claude, 문서 반영 Codex. Unreal 기준은 지시서의 원격 `3f02577` + 스테이징이며, **커밋 직전까지 스테이징, 커밋·푸시는 사용자**. md HEAD `76f7a3f`는 Codex가 읽기 전용 Git 확인했다. 기존 미커밋 10파일을 보존했다. 아래 수치·판정은 Claude 지시서 근거이며 Codex가 엔진이나 자동화를 실행하거나 지정 로그를 재검증한 결과가 아니다.

### D-5 랩 타이머

사용자 보완 지시 반영 구현됨·자동 검증됨(2026-10-06 C PC Claude). 3·2·1 동안 타이머를 숨기고 기록하지 않는다. 출발 순간부터 0초로 측정하여 화면 위 가운데 `00:00.00` 형식으로 표시한다. 첫 게이트를 통과할 때 다시 시작하지 않고 첫 구간으로 이어간다. `Drone.Mission.RacingStartCountdownPIE`에 해당 판정 추가 후 Success. 이번 집중 검사 로그 경로는 지시서 미제공이며 기존 10/05 로그로 대체하지 않았다. 실제 카운트다운·랩 타이머 화면 수동 확인 대기. 코스4개 지형은 현재 미정·코스4개 미구현.

### D-12 2차 이름 변경·피격 흔들림 분리

구현됨·자동 검증됨(2026-10-06 C PC Claude). `ADronePrototypePawn`→`ADroneFlightPawn`, `ADronePrototypePlayerController`→`ADroneFlightPlayerController`, `ADronePrototypeGameMode`→`ADroneFlightGameMode`; C++ 파일 경로 `Source/Drone/Prototype/`→`Source/Drone/Flight/`. `DefaultEngine.ini`의 `[CoreRedirects]` ClassRedirects 3줄로 옛 이름의 BP·맵이 열린다. 팀원 Production 맵이 GameMode BP를 사용하므로 BP_DronePrototype* 자산 이름과 /Game/Drone/Prototype/... 경로는 재저장 없이 유지한다. 피격 흔들림은 `UDroneDamageShakeComponent`로 분리. 2차 뒤 전체 회귀100개는 알려진 실패만(Claude 지시서; 별도 로그 경로 미제공).

### D-12 3차 Acro·지상 주행 분리 및 검증

구현됨·자동 검증됨(2026-10-06 C PC Claude). 곡예 비행을 `UDroneAcroFlightComponent`, 지상 주행을 `UDroneGroundDriveComponent`로 분리했다. 계산과 실행 중 상태만 이동했으며 BP 조정값·입력 Action·지면 Trace·Pivot은 Pawn 유지, 기존 Pawn 함수 이름도 유지했다. Pawn cpp 2,454→2,090줄.

- 분리 전후 비교 `Drone.Flight.FlightGolden`: 6개 시나리오, 기준값 `Source/Drone/Flight/Tests/FlightGoldenBaseline.txt`, 60줄 0건 불일치.
- 3차 뒤 전체 회귀101개: 실패는 KnownIssues4개·미렌더 패드 포커스6개뿐. 로그 `C:\URproject\drone\Saved\Automation\ClaudeSplit\full_after.log`.
- Claude 지시서의 에이전트 교차 검토(동작 동일성·수명·호환성)에서 확인된 결함0. 이번 Codex docs 작업에서는 에이전트 검토를 새로 실행하지 않았다.
- 한계: 골든은 위치 이동을 기록하지 않는다. 위치 이동은 Claude PIE 회귀로 확인한 범위이며 골든 자체의 검증 범위로 확대하지 않는다.

2차100개·3차101개·과거 전체 회귀는 각각 당시 결과이며 합산하지 않는다. 알려진 실패 해결·새 수동 Pass로 쓰지 않는다. FPV 곡예 비행·UGV 주행이 분리 전과 같은지는 사용자 수동 확인 대기.

### CLAUDE.md MCP 설명·사용자 커밋 준비

사용자 직접 지시에 따라 Unreal `CLAUDE.md`의 MCP 자동 시작 설명을 D-14와 일치하도록 수정됨(Claude 지시서 근거). 공유 설정은 끄고 사용자 PC 로컬만 켠다. 팀원은 불필요하다. Codex는 Unreal CLAUDE.md나 설정을 직접 수정하지 않았다.

Claude가 준비한 커밋 메시지 안은 `C:\URproject\drone\Saved\CommitDraft_D12b_RenameAndShake.txt`, `C:\URproject\drone\Saved\CommitDraft_D12c_AcroGroundSplit.txt`, `C:\URproject\drone\Saved\CommitDraft_D5_RacingCountdown.txt`(랩 타이머 포함). 커밋 직전까지 스테이징, 커밋·푸시는 사용자. Codex Commit/Push·스테이징 미실행.

### 문서 반영·보존·미반영

STATUS 관련 현재 상태·레이싱·D-12·최신 전체 회귀, WORKBOARD D-5 결정 행·RACING 카드·D-12 결정 행·MCP 설명·Next를 갱신했다. CONTEXT와 현재 AI/주행/물리/로비/기체/코드 구조/입력/Telemetry/Training 가이드의 C++ 이름·경로를 정정했다. 상세 구현·검증 이력은 이 WORKLOG 끝 항목을 정본으로 삼고 현재 문서는 요약·링크를 유지한다.

WORKBOARD는 관련 현재 행을 요약하여 30KB 이하로 맞췄다. 변경 전 30,579바이트·113줄 → 변경 후 29,950바이트·114줄(UTF-8; 끝 개행을 줄로 세지 않음). 이번 지시의 history/archive 수정 금지에 따라 절 이동·아카이브 수정/생성은 하지 않았다. 과거 WORKLOG·감사/인수 보고·당시 계획/모바일 요약·snapshot·handoff·가이드의 명시된 당시 파일 목록/검증 절은 옛 이름까지 원문 보존했다. 현재 이름 정정과 과거 기록 보존 지시가 겹치는 곳은 역사 기록을 보존하고 현재 안내에서 새 이름을 명시했다. BP_DronePrototype*와 /Game/Drone/Prototype/... 자산 이름·경로는 변경하지 않았다.

수동 확인 대기: 레이싱 카운트다운·랩 타이머 화면, FPV 곡예·UGV 주행 분리 전 동일 체감. 현재 미정: 코스4개 지형·배터리 시간 값·높이 제한 수치(경고 연출 등 기존 미정도 유지). Drone Space는 지시서의 “Space 제외”에 따라 갱신하지 않았으며 이번 문서 변경은 Space 미반영. applications·history/archive·Unreal 수정, Build·PIE·패키징·쿠킹·맵 생성/재생성, Commit/Push, Trello/Figma·공유 권한·예약 자동화 수정 없음. 새 파일 없음.

## 2026-10-06 D PC 동기화·WORKBOARD 7그룹 정리·10/02 Editor 시작 지연 진단 재반영 — D PC, 문서 반영 Claude

사용자 요청(md 확인·업데이트·그룹 나누기)으로 D PC(`D:\JGY\project\md`, `D:\JGY\project\drone`)에서 수행했다. 작업 도구·문서 반영 모두 Claude이며 이 PC에 Codex 세션은 없었다. Build·PIE·맵 생성/재생성·Commit/Push·Trello/Figma 수정·Drone Space 갱신은 하지 않았다.

### Git 동기화

- 문서: 로컬 HEAD `250e975` → origin/main `c5a0524` fast-forward(10/04 `94f6375`·10/05 `76f7a3f`·10/06 `c5a0524` 수신, 57파일 변경·STATUS/WORKBOARD 정리·archive 3파일 생성 포함).
- Unreal: 로컬 HEAD `5b03ad3`(Clean) → origin/main `1619b4f` fast-forward + `git lfs pull origin main`(10/02 `e662cb4`·`41444c2`, 10/05 `3f02577`, 10/06 `1619b4f` 수신, 1,453파일 변경: 방콕 ThirdParty 삭제·Flight 이름 변경·Legacy 템플릿 삭제·NPC Retarget 애니메이션·도구 정리 포함). Unreal Editor·Zen 미실행 상태에서 수행, Editor Build·PIE 미실행이므로 소스 수신이며 플레이 완료가 아니다.
- 로컬 미커밋 보존: ff 전 D PC의 10/02 미커밋(CLAUDE.md 경로표, STATUS/WORKBOARD/WORKLOG의 10/02 오전 진단)은 `git stash`(stash@{0} "D PC 2026-10-02 PERF-ZEN 진단·CLAUDE.md 경로표 (10/06 ff 전 보존)")와 패치 파일로 보존한 뒤 새 구조에 다시 반영했다. stash pop·Discard·Reset은 하지 않았다.
- CLAUDE.md: 원격 10/06 본문(WORKLOG 대용량 문구·아카이브 예외) 위에 10/02 D PC 수정분(PC별 경로 표, `D:\JGY\project\droner`는 별도 Clone·비작업 공간)을 다시 적용했다.

### 10/02 오전 진단 원문 (Codex 읽기 전용, 당시 D PC 미커밋 WORKLOG 절)

#### 2026-10-02 오전 — D PC Editor 시작 지연 읽기 전용 진단

- 사용자 실행 로그를 Codex가 읽었다. D PC Unreal HEAD `5b03ad3` 작업 트리 Clean, 문서 HEAD `250e975`는 기존 `CLAUDE.md` 수정 상태를 보존한다. 앞선 C PC ec2e88f 검증을 이번 PC 재검증으로 바꾸지 않는다. Editor/Zen은 사용자 실행 중이며 Codex는 실행·종료·Build·PIE를 하지 않았다.
- `drone/Saved/Logs/Drone.log`: Zen AutoLaunch 473.350초, 전체 Engine Initialization 532.66초. `Drone-backup-2026.10.01-03.18.07.log`: 3.559초/24.51초. 현재 로그는 대규모 셰이더 재컴파일로 473초를 소모했다는 근거가 아니며, 셰이더 초기화는 Zen 대기 이후 시작했다.
- 사용자 Zen 로그 `Common/Zen/Data/logs/zenserver.log`는 09:23:08.958 KST에 running, Editor HTTP OK는 09:30:37.590이다. 인덱스 읽기 0~19ms·GC 대기·사용량 약6.89G. 초기 세션 파일 읽기 구간도 있었지만 전체 473초를 설명하지 않는다. 엔진 ZenServerInterface.cpp의 Startup Event 대기/20초 이후 YesNo 확인창/health ready 요청(긴 timeout) 경로를 대조했다. 특정 확인창에 사용자가 응답했는지는 미확인이다. Zen HTTP는 proxy bypass를 사용하며 현재 시스템 proxy 없음이라 일반 proxy를 원인으로 확정하지 않는다.
- 읽기 전용 현재 `http://[::1]:8558/health/ready` 검사: HTTP200·142ms. C/D는 NVMe, C 약40GiB/D 약801GiB 여유. 정상 응답은 시작 지연 해결 근거가 아니다. 캐시 삭제·경로 변경·보안 설정 변경·엔진 소스/프로젝트 수정은 하지 않았다.
- Claude 후속 `PERF-ZEN-START-01`: 사용자 저장·종료 후 같은 캐시/맵에서 cold/warm 시작 비교, 확인창 응답 시점/서버 running/Editor status 시간 분리. DDC 유지, 가벼운 시작 맵은 PC 설정 또는 명시 맵 진입으로 비교하고 Production Training을 저장하지 않는다. 새 자산/맵 첫 사용의 캐시 생성 비용은 별개다. [Epic UE5.8 DDC 안내](https://dev.epicgames.com/documentation/unreal-engine/using-derived-data-cache-in-unreal-engine?lang=en-US).
- STATUS·WORKBOARD와 기존 Drone Space 진행 페이지에 진단 사실/미확정/다음 비교를 반영한다. Commit/Push·Trello/Figma 수정·예약 자동화는 하지 않는다.

당시 STATUS 절·WORKBOARD 카드 원문은 stash@{0}에 있으며 현재 STATUS 알려진 실패 줄과 WORKBOARD PERF-ZEN-START-01 카드로 요약했다.

### WORKBOARD 7그룹 정리

- 회의 후 역할별 카드 표(8)와 본 카드 표(48)를 하나로 합쳐 7그룹으로 재배치했다: 튜토리얼·코스·레이싱 / UI·설정·패드 / 미션·스토리·HUD / 비행 물리·조작·기체 / AI·NPC / 환경·날씨·자산 / 테스트·빌드·성능·동기화. 회의 후 카드는 각 그룹 맨 앞. 결정 필요·면접 대비 표와 Next는 그대로 두었고 카드 행 본문은 바꾸지 않았다.
- 추가: PERF-ZEN-START-01 카드(테스트·빌드·성능·동기화). SYNC-WORKPC-01 현재 상태 끝에 D PC 수신 한 줄. 결정 필요 레이싱 행에 FIGMA-RACING-02의 Ghost/리플레이·커브·Restart/Quit 범위 결정을 이관.
- 30KB 규칙(AGENTS 문서 정리 규칙)에 따라 내용 추가 전 아카이브: RACING-MEETING-01·FIGMA-RACING-02(RACING-TERRAIN-LINK-01·결정 행으로 대체), MISSION-FRAMEWORK-01(STORY-TEST-01·MISSION-RULE-PIE-01로 대체), MAP-TEST-01(TUT-GATE-PRESENTATION-01·TUT-ROUTE-SELECT-01 수동 확인으로 대체), TUTORIAL-GUIDE-03(문서화 완료)을 `docs/history/archive/WORKBOARD_2026-10.md` 끝 절로 원문 이동. 루트에는 한 줄 요약·링크.
- 크기: WORKBOARD.md 29,950바이트·114줄 → 29,999바이트·142줄. 아카이브 61,006바이트·265줄 → 62,958바이트·277줄(UTF-8, wc 기준).

### STATUS 갱신

- 기준일과 Git 기준 표를 D PC 현재로 덮어썼다. 이전 10/06 C PC 표 원문: `| Unreal C:\URproject\drone | 원격 3f02577 + 스테이징 | 10/06 Claude 지시서 기준. 커밋 직전까지 스테이징, 커밋·푸시는 사용자 |`, `| 문서 C:\Users\jkw11\Documents\Codex\2026-08-19\codex-gpt-chatgpt-codex-1-6 | HEAD 76f7a3f | Codex 읽기 전용 Git 확인(10/06). 기존 미커밋 보존·이번 문서 변경 추가, Commit/Push 미실행 |`. 그 스테이징분은 원격 `1619b4f`로 Push된 것으로 보이며 C PC 작업 트리는 이 PC에서 확인 불가.
- 알려진 실패·미정에 PERF-ZEN-START-01 줄, 다음 확인에 D PC 항목 4 추가. 나머지 C PC 10/06 내용은 유지.

미반영: Drone Space(Claude 접근 불가, Codex 반영 대기). Commit/Push는 사용자가 GitHub Desktop에서 검토 후 처리한다.

- LFS 결과: `git lfs fetch origin main --include=Content/Drone/Maps/Lvl_DroneTraining.umap`(index 미잠금)으로 391,433,900바이트 수신 후 `git lfs checkout`. 추적 8,010개 모두 본문 있음(pointer 0). 사용자 GitHub Desktop Pull이 "A lock file already exists"로 막힌 원인은 Claude의 백그라운드 `git lfs pull`이 잡은 index.lock이었고, 해당 작업을 중단·stale lock 제거 후 해소했다. 중단된 `lfs pull`이 남긴 통계만 어긋난 80개 파일(내용·OID 동일)은 `git add`로 index 통계만 맞췄으며 스테이징된 변경 0. 최종: drone HEAD `1619b4f` = origin/main, Clean, 0/0.

## 2026-10-06 D PC Codex 최신화·동시 Pull 잠금 재확인

사용자 최신화 요청으로 원격 Git 메타데이터 Fetch·코드/설정/MD/로그 읽기 대조와 기존 Drone Space 갱신을 수행했다. Codex는 Pull·스테이징·Commit/Push·프로세스 종료·lock 삭제·Discard·Build·PIE·에셋 변경을 하지 않았다. 기존 CLAUDE.md와 Claude의 MD 정리·아카이브 변경을 보존했다.

원격 Unreal1619b4f·MD c5a0524를 확인했다. 원격 코드에는 레이싱 카운트다운/출발 타이머·배터리 추락/재출격·고도 제한 매니저·Prototype→Flight/3 ClassRedirects·Acro/GroundDrive/DamageShake 분리·입력 HUD 저장·튜토리얼8개 진행·Best Lap JSON 저장이 있다. Managers BP4개와 Bangkok 잔여987개 삭제 경로도 확인했다. C PC 최신 전체101개 검증/Build 기록은 인계 근거이며 이번 D PC 실행 결과가 아니다. 수동 패드/화면/체감·실제 패키징, 코스4개·배터리 시간/고도 수치·최종 경고/아트/음원은 미확인 또는 미정 상태로 유지한다.

현재 D PC Editor 로그는10/02가 최신(Zen473.350초·전체532.66초), 자동화 보고서는10/01 LobbyLayoutDiagnosticWrapProbe 총1건 Fail이다. 새 로그나 Zen cold/warm 해결 근거는 없다. 초기화 중 UnifiedErrorTest 메시지를 새 프로젝트 테스트 실패로 집계하지 않았다.

잠금 경과: 09:10:07 만들어진 .git/index.lock과 git merge41256/git-lfs16216을 확인했다. 부모 프로세스 체인은 Claude 터미널이었다. GitHub Desktop의09:13:57/09:14:03 Pull은 같은 lock 오류로 차단됐다. 09:21 재확인에서는 Git/LFS 프로세스가 검출되지 않았지만 lock이 남고 HEAD는5b03ad3였다. 원격1619b4f보다4커밋 뒤며 수신 완료/Clean을 판정할 수 없다. 처음 Clean에서 대량 수정/삭제/미추적으로 바뀌는 과정을 관찰했다. 앞선 Claude 문서의 수신 완료/Clean 표기는 이 실제 재확인과 달라 STATUS/WORKBOARD의 현재 표기만 정정했다. 과거 인계 기록은 지우지 않았다. 잠금 제거·재수신은 별도 확인 후 처리하며 변경 파일을 Discard하지 않는다.

MD 현재 경로/시작 가이드와 상태·동기화 카드를 정정하고 Space 진행/테스트/BP/안내 페이지를 갱신·저장 후 재조회했다. C PC의 임시 False 기재는 D-3 사용자 결정(기본 False 확정)과 구분하고, 배터리 컴포넌트 WarnOnly와 미션 기본 Crash도 구분했다. 레이싱3·2·1은 후속 미구현이 아닌 원격 구현/수동 대기로 정정했다. Trello/Figma·기획 원본·Production Training·공유 권한·예약 자동화는 변경하지 않았다.

Codex 후속 읽기 확인(09:24~09:25): 다른 작업의 복구 뒤 HEAD=origin/main1619b4f·0/0, index.lock 없음·Git/LFS 프로세스 미검출. `git ls-remote origin refs/heads/main` 성공으로 현재 Git 원격 접근은 확인했다. LFS 포인터는 Training 맵1개, 실제 파일134바이트이며 자산 수정80개가 남아 Clean/본문 수신 완료는 확인하지 못했다. 이후 상태는 별도 재확인이 필요하다. 현재 STATUS/시작 가이드/동기화 카드와 Space에 이 후속 상태를 반영했다. Codex는 잠금 제거·reset·Pull을 실행하지 않았다.

### Unreal 수신 정정 (같은 세션 후속)

- 첫 `git merge --ff-only origin/main`은 1,470파일 체크아웃을 마친 뒤 LFS 본문 수신(81개 중 80개 완료, 마지막 1개 대용량) 단계에서 도구 시간 제한(10분)으로 중단됐다. HEAD·index는 `5b03ad3`에 남고 0바이트 `index.lock`(09:10:07)만 남았다. GitHub Desktop이 켜져 있어 git 프로세스가 간헐적으로 보였으나 merge/checkout/lfs 쓰기 프로세스가 없음을 확인한 뒤 stale lock을 제거했다.
- 재시도 merge는 작업 트리에 남은 대상 버전 파일 때문에 거부됐다. `git status -uall` 변경 1,470개가 `git diff --name-only --no-renames 5b03ad3 1619b4f` 1,470개와 정확히 일치(차집합 0)함을 확인한 뒤, 즉 사용자 작업이 아니라 중단된 merge 잔여물뿐임을 근거로 `GIT_LFS_SKIP_SMUDGE=1 git reset --hard origin/main`으로 fast-forward와 같은 결과(`1619b4f`, Clean, 0/0)를 만들었다. 중단 전 작업 트리는 Clean·0/0이었다.
- LFS: 추적 8,010개 중 pointer 1개(`Content/Drone/Maps/Lvl_DroneTraining.umap`, 391MB, 팀원 Production 맵)만 남아 `git lfs pull origin main`으로 수신 중. 결과는 아래 줄에 기록한다. Production 맵은 수신만 하며 저장·재구성하지 않는다.
- PERF-ZEN-START-01 원인 특정(같은 세션 후속, Editor 실행 중 로그 읽기): 오늘 09:38 시작 Zen AutoLaunch 24.288초·Engine Initialization 91.36초. zenserver.log에서 HTTP 포트는 0초에 열리나 설정 요약(09:38:46.982)→세션 서비스 로드 완료(09:39:07.325) 사이 20.3초 공백, 10/02도 09:22:46.619→09:23:08.969 22.4초 공백. 로드 대상 `Common\Zen\Data\sessions` 733폴더·1,466파일·20MB(8/20부터 실행마다 누적). 엔진 ZenServerInterface.cpp: 10초 뒤 Waiting 표시, 20초 초과 시 Yes/No 모달. 10/02 473초는 Zen ready 09:23:08 뒤 모달 응답 09:30:37까지의 대기. 사용자 요청으로 오늘 세션 폴더 `0ad5dd14e0b65079da2203e6`만 남기고 732개를 `%LOCALAPPDATA%\UnrealEngine\Common\Zen_sessions_backup_2026-10-06`로 이동(삭제 아님). 캐시(cas/cache)·엔진·프로젝트 미수정. Defender 실시간 검사(켜짐)는 보안 설정이라 Claude가 변경하지 않고 설정 창만 열어 사용자에게 맡김. 효과는 다음 Editor 시작에서 재측정.

## 2026-10-06 D PC — 조작 버튼·Drop 집게 수정 인계 (Codex 읽기 전용 진단)

사용자 사진: 조작 3 이름이 여러 줄로 찢어짐, 초기 화물과 Drop→재픽업 화물의 위치/회전이 다름. 요청은 버튼 전체 가로폭 확대·짧은 이름과 두 부착 경로의 집게 중앙 정렬이다. WORKBOARD `UI-CONTROL-LAYOUT-01`·`PAYLOAD-GRIP-01` 등록. Claude 수정/검증 대기이며 Codex는 C++/BP/도구 수정·Build·PIE·Commit/Push를 실행하지 않았다. 프로젝트 역할 규칙상 C++는 Claude, BP는 ui 지시서가 있어야 Codex 편집 가능하다. 기존 미커밋 변경을 보존했다.

### UI-CONTROL-LAYOUT-01 — Claude 구현 조건

- 대상 `Source/Drone/UI/DroneSelectionWidget.cpp`의 라벨 helper·RefreshControlLabels·BuildDefaultLayout/TryBindBlueprintLayout와 실제 사용 WBP. 현재 미커밋 코드는 Arcade/Angle/Acro Mode 1/2와 C++ 최소폭360이 있으나 저장 WBP가 연결되면 native layout을 건너뛴다. UButtonSlot 내부 HAlign도 명시되지 않아 부모 Fill만으로 텍스트 영역 전체 폭을 보장할 수 없다. 실제 사용 레이아웃/빌드·BP 값은 미확인이다.
- 짧은 표시명 제안: `쉬운 조작 / 게임 조작 / RC 모드 1 / RC 모드 2`. RC는 스틱 배치 뜻이며 Mode1/2의 물리 정확도 보증이 아니다. enum 값/순서·입력·저장 ID는 변경하지 않는다. 사용자 요청대로 인접 선택 박스 가로폭도 함께 점검하되 기존 로비 이미지·흐름은 유지한다.
- 버튼과 내부 텍스트 슬롯 폭·padding/Fill을 함께 수정. 1280×720·1920×1080에서 4개 이름을 모두 한 줄로, 잘림 없이 표시하고 normal/hover/pressed/패드 강조·모드 순환·저장/복원을 회귀 확인한다. 기존 MissionEntryPIE·GamepadMissionFlowPIE는 이 레이아웃 결함을 검사하지 않는다.

### PAYLOAD-GRIP-01 — Claude 구현 조건

- 초기 화물은 Actor가 아닌 CarriedPayloadVisual이며 `DronePayloadDropComponent.cpp` UpdateCarriedPayloadVisual이 PayloadClass CDO의 mesh/material/scale/location을 복사하지만 rotation은 복사하지 않는다. 재픽업은 `DroneDroppedPayload.cpp`에서 실제 Actor root를 PayloadCarryAnchor world pose에 맞춘다. 기존 생성 도구는 표시 Mesh와 anchor를 각각 VisualTiltPivot 아래에 둔다. 부모/좌표계가 다른 두 경로이므로 같은 grip pose가 보장되지 않지만 사진의 정확한 원인·최종 수치는 BP 실측 전 단정하지 않는다.
- `/Game/Drone/Integrations/RoleDrones/BP_DroneDropIntegration`의 PayloadCarryAnchor와 `/Game/Drone/Abilities/Payload/BP_DroneCarryablePayload`의 PayloadVisual local Transform을 공통 부착 기준으로 사용. 초기·재픽업 모두 집게 가운데에서 자연스럽게 잡힌 방향/크기를 맞추고 위치·회전·크기는 BP에서 조정 가능하게 유지한다. 기존 부모/Transform·PayloadClass·동기화 flag를 먼저 기록하고 전체 BuildDroneRoleIntegrations 재생성은 금지한다.
- ApplyDronePayloadBagMesh.py는 최장40cm 크기와 pivot offset만 설정하며 회전은 없다. 회전 변경 시 bounds/pivot 보정도 회전된 좌표를 반영해야 한다. 사진만 보고 Z/90도를 임의 확정하지 않는다. 초기 visual 위치 자동복사가 grip anchor 조정을 무효화하지 않도록 통일한다.
- TestMap에서 초기→Drop→착지→재픽업→재Drop 반복: 중앙·방향·크기 동일, 기체 tilt 추종, 표시 중복 없음, release pose 점프 없음, 하중·Drop 물리·미션 유지. Production Lvl_DroneTraining은 저장하지 않는다. RoleAbilities/PayloadLanding 기존 검사에 pose 비교를 추가 검토하고 RoleDroneAssets의 Crate 이름 assertion도 Bag 메시 변경에 맞게 검토한다.
- 기존 Saved/Automation/ClaudePayload/test.log(10/06 11:29 KST)에는 RoleAbilities/PayloadLanding Success가 있지만 nullrhi/nosound 실행이므로 집게 외형 수동 Pass가 아니다. 이번 Codex 실행 결과도 아니다.

읽기 시점 11:45 KST: Unreal HEAD=origin/main `0c0ed99`(드론빙의 수정), tracked17·untracked3 변경. Training 맵은391,433,900바이트 본문 수신, Payload BP와 미션 DA5개 총6개는 포인터였다. 현재 HEAD 변경/동시 작업과 자산 본문 상태는 수정 전 Claude가 재확인해야 한다. 추가 Pull/Discard/reset은 이번 요청에서 실행하지 않는다.

## 2026-10-06 D PC — 조작 UI·Drop 파지 예외 수정/검증 (12:17 KST)

사용자 `ㅇㅇ 예외처리하고 수정해줘` 승인으로 이번 UI-CONTROL-LAYOUT-01/PAYLOAD-GRIP-01만 Codex가 C++·회귀·Drop BP를 직접 수정했다. 이후 사용자 이름 제안에 맞춰 RC 대신 FPV 모드 1/2로 확정했다. 상시 역할 분담/AGENTS는 변경하지 않았으며 기존 미커밋 변경을 보존했다. Unreal MCP 호출·Commit/Push·Pull/reset/Discard·Trello/Figma/권한/예약 변경은 없다.

### 변경 내용

- SelectionWidget: `쉬운 조작 / 게임 조작 / FPV 모드 1 / FPV 모드 2`, FPV 하단 설명 `스틱 배치가 다른 수동 비행 모드입니다`. enum/입력 순서/저장 ID 불변. 공통 초기화 1회에 내부 ButtonSlot Fill/padding0·no-wrap/WrapAt0·텍스트 최소폭300·선택 박스 최소420×72 적용. native 화면 좌우 패널/카드 여백 축소, 기존 로비 이미지·흐름 보존. 이름 있는 WBP 연결 경로도 같은 보정 적용.
- PayloadDropComponent: 초기 표시 Mesh를 실제 화물과 같은 PayloadCarryAnchor 아래 붙이고 PayloadClass CDO의 전체 local Transform을 복사. 새 stock 화물 Spawn도 같은 anchor와 CDO pose 사용, 재픽업 SnapToTargetIncludingScale, 재투하는 KeepWorld로 위치 점프 방지. 기존 일반 Owner SpawnOffset은 유지; 일반 Actor의 tagged-mesh fallback 파지 외형은 이번 검증 범위 밖.
- RoleDroneAssets의 오래된 Crate 이름 조건을 실제 `/Game/Item/Bag/Bag` 계약과 부모/pose 비교로 변경. 새 `Drone.Drop.PayloadGripPose`와 `Drone.Flow.SelectionControlLayout` 회귀 추가.
- Delivery 본체 mesh 실측: 하단 집게 약Z=-28.5cm, 카메라 바닥=-21.22cm, 가로 Bag 반두께8.78cm. Drop BP PayloadCarryAnchor `(0,0,-65)/회전0`→`(0,0,-30.5)/Roll90`, Scale1/VisualTiltPivot 부모 유지. 카메라 아래 약0.5cm 여유를 둔 시험 기본값이며 자연스러운 파지 외형은 수동 대기. 화물 BP의 기존 Bag 최장40cm·pivot 보정은 그대로여서 적용 도구는 SKIP했고 Drop BP만 저장했다. fresh process 재조회로 저장된 anchor 확인(apply_grip2.log/after_grip.log).
- `ApplyDronePayloadBagMesh.py`는 기존 mesh 변경을 보존하면서 회전 포함 pivot 보정·지정 Drop BP anchor 적용을 추가. 전체 역할 BP 재생성/맵 저장은 하지 않았다. BP 수정 전 본문 백업은 Saved/Automation/CodexGripPose에 보관.

### 실제 검사와 범위

기존 코드에서 PayloadGripPose 실제 Fail과 UI 이름/내부 Fill/폭 실제 Fail을 확인 후 수정했다(red.log/probe.log). UI 검사 초기 World/LocalPlayer fixture 문제는 먼저 수정해 silent pass를 없앴다. 최초 green의 텍스트 요구 높이39px/할당36px를 실측해 박스64→72와 세로 clipping assertion을 추가했다. stock Actor ctor가 CDO local pose를 기본값으로 덮는 실제 실패도 Spawn 직후 source pose 적용으로 수정했다.

- 최종 `DroneEditor Win64 Development` Build Succeeded, 설치 엔진 UE5.8.2·MSVC14.51.36257 명시. 이전 문서의36256은 현재 설치되지 않았다. preferred compiler 및 기존 엔진 deprecation 경고는 남아 있으며 경고0이라고 보고하지 않는다. 최종 로그 `Saved/Automation/CodexGripPose/final_build.log`.
- 12:16~12:17 KST 최종 자동화 **6 Success / 0 Fail / 0 NotRun**: PayloadGripPose, PayloadLanding, PlayerFacingTextContract, SelectionControlLayout, RoleDroneAssets, RoleAbilities. 보고서 `Saved/Automation/CodexGripPose/final2_report/index.json`, 실행 `final2.log`. 엔진 초기 UnifiedErrorTest 자기검사 메시지는 이 6개 실패로 집계하지 않았다.
- PayloadGripPose는 기체/tilt 회전·offset/비균일 local scale·anchor scale, 초기→첫 투하→착지/픽업→재투하 2회·표시 중복 없음 검사. RoleAbilities의 하중·역할과 PayloadLanding의 옆면 후 낙하/안착도 통과.
- SelectionControlLayout는 native + Blueprint-compatible named-tree fixture(폭90·명시 wrap70)를 실제 Slate로 배치해 4모드×1280/1920·이름/순환·가로/세로 clipping·힌트를 검사했다. native button local914.8×72/text874.8×39, fixture도text39px 확보. 실제 authored WBP override 렌더·실물 패드 확인이 아니다. nullrhi/nosound 검사이므로 사용자 화면·파지 체감은 미확인.
- 두 저장소 `git diff --check` 통과. Unreal HEAD=origin/main0c0ed99·tracked19/untracked5, 시작 시 기존17/3를 보존하고 이번 변경 추가. 앞서 포인터였던 Payload BP25925B·미션 DA5개3976~6464B 본문을 확인했으며 전체 LFS 자산 수신을 새로 검사한 것은 아니다. Production Training 맵391433900B·09:31:24 수정시각 그대로, 맵 변경/저장 없음.

현재 사용/수동 절차는 [역할·화물 가이드](../gameplay/DRONE_TYPES_AND_CONTROL_MODES.md)와 [UI 가이드](../gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md)를 따른다. 다음은 선택 화면4개 모드 한 줄/강조와 Payload TestMap에서 시작→바닥 투하→재픽업→재투하 파지 외형 확인이다. 이후 기존 레이싱/패드/8수업/Best Lap 검증 순서를 유지한다. STATUS/WORKBOARD는 수동 대기, Drone Space에는 이번 예외 구현·자동화 출처와 BP 조정/수동 절차를 반영한다.

Space 반영 결과: 기존 진행/안내/BP/테스트 Page의 8개 guarded 연산 적용, 저장 후 동일 stream·block 재조회로 기대 본문8/8 일치 확인. Trello 링크·기존 기획/역할 규칙·날짜 이력 보존, 새 Page 없음. 로컬 STATUS23014B·WORKBOARD29868B로 각각30KB 이하 유지. 미커밋 MD는 원격 GitHub 본문에도 이미 반영된 것으로 표현하지 않는다.

### 같은 날 후속 — 미션 결과창 사진 진단/UI-RESULT-LAYOUT-01 (읽기 전용)

사용자 미션 성공 사진의 기본 회색 3버튼·Next 좌우 돌출·행 간격 없음·큰 하단 빈 공간을 실제 소스와 대조했다. 이번 요청은 원인 질문이므로 Unreal 코드/BP/Build/PIE/MCP를 실행하거나 수정하지 않았다. 앞선 예외 구현 범위를 이 결과창까지 확장하지 않는다.

- `DroneMissionResultWidget.cpp:283~330`의 native fallback은 Canvas에 .25/.25→.75/.75 비율 패널을 두고 VerticalBox에 텍스트/버튼을 자연 높이로 쌓는다. 버튼 SetStyle·패널/행 Padding·내용 수직 중앙/SizeBox가 없어 기본 회색·밀착 버튼·남는 빈 공간이 발생할 수 있는 구성이다.
- 성공 시 Next에 포커스가 간다(cpp389). `GamepadFocusScale=1.06`(Result h38), 공통 `DroneGamepadFocus.cpp:146~150`은 중앙 pivot/RenderScale·tint만 변경한다. 주변 배치/여유 공간은 확장하지 않으므로 전폭 버튼 양옆이 돌출한다.
- 제공 이미지 본문을 System.Drawing으로 읽기만 해 회색 영역을 비교: Next1527px/재도전1438px=1.0619, 코드1.06배 예측1524.3px. 렌더 containment는 사진에서 Fail이며 확대 원인과 정합한다. 픽셀 경계 오차가 있어 정확한 runtime geometry 측정으로 표현하지 않는다. 세 번째 행 표본은 바닥 회색이 섞여 비교에서 제외했다. 실제 현재 WBP/controller override는 실행 없이 확정하지 않았다.
- 현재 Result diff는 DetailText AutoWrapText true 2줄뿐이며 Selection 수정은 다른 클래스의 지역 StyleButton/ApplySelectionLayout에 한정된다. 상세문구 줄바꿈이 회색 스타일/Next 확대를 만든 근거는 없다. 기존 Entry/TutorialNextLesson/GamepadMissionFlow 검사는 결과 상태·문구·버튼 동작·포커스를 보지만 결과창 스타일/간격/돌출을 검사하지 않는다. 앞선 집중6/6 성공은 이 외형 해결 근거가 아니다.
- 수정 인계 조건: Result 전용 결과 카드/명시적 패널 padding·버튼 높이/간격·공통 UI 스타일을 적용하고, Result만 확대 대신 색/테두리 강조 또는 확대 여유 공간을 확보한다. 공통 패드 확대를 전역 제거해 다른 UI를 바꾸지 않는다. 짧은 표시명 `다음 미션 / 재도전 / 로비로`와 다음 미션명 별도 표시를 검토하되 progression/실패/튜토리얼 전체 완료 계약은 유지한다. 1280/1920 성공·실패·다음 없음·전체 완료·키보드/패드에서 버튼이 카드 안에 남는 렌더 회귀 필요.

STATUS/WORKBOARD에 진단·미수정 상태로 등록하고 기존 Drone Space 진행 Page의 같은 상태 표/다음 작업을 갱신한다. Commit/Push·Trello/Figma·Production Training 변경 없음.

문서 유지관리 스킬로 기존 진행 Page 두 블록의 guarded 교체를 적용하고 재조회2/2 일치 확인. MD diff --check 통과, STATUS23335B·WORKBOARD29947B로30KB 이하 유지했다.

### 같은 날 후속 — 결과창 예외 수정/UI-RESULT-LAYOUT-01 (12:43 KST)

사용자 `그래 수정해주고` 승인에 따라 결과창에 한정해 Codex가 생산 코드·검사를 직접 수정했다. 앞선 읽기 전용 진단 이후의 별도 예외이며 상시 AGENTS/Claude 역할 분담은 바꾸지 않았다. 기존 미커밋 코드·자산을 보존했고 Editor 종료 확인 후 CLI Build/자동화를 실행했다. Unreal MCP·맵 저장/재생성·Commit/Push·Trello/Figma/공유 권한/예약 변경은 없다.

- native Result: 고정 비율 패널 대신 중앙 폭680·내용 자연 높이 카드, ScaleToFit/DownOnly·화면10% 여유, 패널 여백32/28·둥근 청록 테두리. 버튼616×67·간격12(검사 실측), 글자22·중앙 정렬/긴 이름 줄바꿈. 기본 문구는 다시하기/로비로 복귀로 단축. Story 다음 미션 이름·결과 시간/순서·튜토리얼 다음/전체 완료·실패/복귀 로직은 유지.
- Result만 NativeTick에서 실제 focus배율1을 고정하고 GamepadFocusTint 색/2px 테두리 강조. 기존 GamepadFocusScale BP 속성은 직렬화 호환으로 남고 옛1.06도 런타임 확대하지 않는다. 공통 focus helper나 다른 UI 배율은 변경 없음. 포커스/색이 바뀔 때만 스타일 갱신하고 파괴 시 강조/대기 요청 해제. 이름 계약 WBP는 버튼/직접 VerticalBox 행만 보정, 작성한 부모 트리는 보존한다.
- 새 `Drone.Flow.MissionResultLayout`: native/named-tree fixture×성공 다음/다음 없음/실패/전체 완료/긴 이름×1280/1920, 실제 Slate 배치·그리기 경계·라벨·높이56 이상·간격8 이상·회색 아닌 스타일·하단 불필요한 공백 검사. 별도 real Root→NativeTick 성공/실패로 옛BP1.06 보존·실제배율1·처음 포커스·동적 테두리 검사. 콘텐츠 매트릭스는 공개 UMG로 구성하고 실제 Flow 분기는 기존 PIE로 확인한다.
- red.log에서 기존 돌출/붙은 행/스타일/공백 Fail을 실제 재현. 첫 수정 Build는 Stretch enum/Slot 이름 가림을 설치 엔진 API에 맞춰 정리했다. green.log의 배치/기존5개 검사는 통과했지만 반복 SetKeyboardFocus의 반환값 검사만2Fail이어서 실제 HasKeyboardFocus 사후 조건으로 고쳤다(이미 같은 버튼이면 반환false 가능). final 검사에서 실제 포커스와 NativeTick을 함께 확인했다.
- 최종 `DroneEditor Win64 Development` Succeeded(UE5.8.2·MSVC14.51.36257 명시), `Saved/Automation/CodexResultLayout/final_build.log`. preferred compiler·기존 엔진 deprecation 경고는 유지하며 경고0으로 표현하지 않는다.
- 최종12:43 KST **6 Success / 0 Fail / 0 NotRun**(4일반+2경고): MissionResultLayout, SelectionControlLayout, MissionEntryPIE, TutorialNextLessonPIE, TutorialCompletePIE, GamepadMissionFlowPIE. `Saved/Automation/CodexResultLayout/final_report/index.json`·`final.log`. NullRHI 경고2개는 렌더가 필요한 패드 판정 제한이며 실물 패드/실제 WBP 화면 Pass가 아니다. 결과창 기본 배치 측정에서 카드680×458, 버튼616×67·12간격·하단28여백 확인.
- 기존 변경을 제외한 이번 Unreal 범위는 Result cpp/h와 신규 test 하나. tracked20·untracked6, HEAD=origin/main0c0ed99. Production Training391433900B·09:31:24 수정시각 그대로. Payload/Selection/기타 자산은 이번 작업에서 추가 변경하지 않았다.

현재 UI 가이드에 결과 WBP 필수/선택 이름·Controller 연결·배율 호환·수동 확인을 기록했다. 다음은 720p/1080p에서 성공/실패/다음 없음/전체 완료의 카드/문구/버튼과 실제 패드·다음/재도전/로비/시작 메뉴 전환 확인이다. 이후 기존 조작/화물·레이싱/8수업/Best Lap 확인 순서는 유지한다. STATUS/WORKBOARD는 구현·자동 검증됨/수동 대기로 갱신하고 Drone Space 같은 항목에 반영한다.

마무리: MD·Unreal diff --check 통과(줄바꿈 변환 안내만 있음). STATUS23761B·WORKBOARD29918B로30KB 이하 유지. Space 기존 진행/테스트/BP/안내4개 Page의 guarded6연산 적용·본문7블록을 재조회해 기대 변경6/6 일치 확인. Trello 링크·날짜 이력/역할 규칙 보존, 새 Page/권한 변경 없음. Git 두 작업 트리는 미커밋 상태이며 사용자 Commit/Push 대기다.

## 2026-10-07 InterLink DX 조종기 입력과 메뉴 연결 — D PC Claude

- 작업 도구/실행: Claude(D PC). 문서·Space 반영: Codex. 통합 지시서 `20261007-123213-docs-interlink-all`의 1차 입력 연결→2차 실측/메뉴 순서 반영, 충돌은 2차 우선. 1차 run은 미실행이어서 이번에 함께 반영했다.
- Git 기준: Unreal `cb77c0d`, MD `6558cca`(작업 전 Clean), 이번 문서는 미커밋. Codex가 읽기 전용 HEAD/설정/성공 로그를 대조했다. Unreal 쓰기·Build/PIE·패키징·맵 생성·Commit/Push·Trello/Figma 수정 없음.
- 장치: Spektrum InterLink DX, USB HID VID 0x1781/PID 0x0E5A, 축8·버튼27. PnP·joy.cpl OEM·HID value caps로 Claude가 식별(장치 식별 로그 파일 없음). XInput이 아니므로 기존 Gamepad 33매핑은 이 장치에서 무반응이었다.
- 1차 구현: 프로젝트 `Plugins/RawInput/`에 UE5.8 엔진 Experimental/Deprecated RawInput 복사본을 두고 축24키 등록에 Axis1D를 추가(IsAnalog=false로 PlayerInput이 버리던 문제), uplugin DeprecatedEngineVersion 제거. `Drone.uproject` RawInput Win64 활성화, 프로젝트 플러그인 우선 로드 로그 확인. `DefaultInput.ini` 축8·버튼27 장치 설정, IMC 기존33+InterLink8=41. 쉬운/제한 자세4축+Acro4축·기존 쉬운 조작 Dead Zone Lower0.2/Upper1.0/Radial 복사. 상세 배치는 [입력 계약](../tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md) 정본.
- 도구/계약: 신규 `BuildDroneInterLinkInput.py`는 InterLink 매핑 교체 방식. `BuildDroneAcroInput.py`는 매핑 수 검사에서 GenericUSBController 제외(변경 후 미실행). AcroInputAssetContract의 조종기4축 Dead Zone 계약, PIEInputLifecycle ExpectedMappingCount 33→41.
- 2차 실측: 사용자가 조작한 12:21·12:23 HID 기록 2회(100초). 앞/위/오른쪽으로 밀면 0..4096 값 증가. 초기 Axis6/8 bInverted=True 가정을 정정해 축8개 전부 False, bGamepadStick=True 정규화. 실물 Mode2(왼쪽 세로 비복귀 스로틀·오른쪽 세로 중앙 복귀)와 게임 기본 배치 일치. scratchpad interlink_sample.log/interlink_sample2.log는 저장소 밖 Claude 근거이며 개인 로그 업로드 없음.
- 사용자 확정(10/07): 실제 콘솔 InterLink DX 사용, 구현 방식 Claude 위임. Select 노브 회전=위/아래·딸깍=확인·Cancel=뒤로. 실측 Button17/18 회전 펄스·16 딸깍·15 Cancel. 회전 어느 방향이17인지는 미확인.
- 2차 구현: 신규 `DroneInterLinkNavigationSubsystem.h/.cpp`(GameInstanceSubsystem·Config=Game), 시작 시 기본 키보드/패드 Slate FNavigationConfig 보존+조종기4키 추가, 종료 복원·Slate 없는 Commandlet 생성 제외. `DefaultGame.ini` 설정: 17 Up/18 Down/16 Accept/15 Back, 방향 반대면 KnobUpKey/KnobDownKey 맞바꿈. FrontEndRootWidget/SelectionWidget Back에 IsBackKey 추가. 신규 Drone.UI.InterLinkNavigationContract는 조종기4키와 기본 규칙 보존 검사.

| 검증 | 조건/판정 | Claude 근거(루트 D:/JGY/project/drone/Saved/Automation/ClaudeInterLink/) |
|---|---|---|
| 장치 식별 | PnP·joy.cpl·HID, 축8·버튼27 | Claude 세션·별도 식별 로그 없음 |
| Build 1차 | Editor 종료 후 Succeeded 2회 | build.log, build2.log |
| IMC 패치 | replaced=0·added=8·mappings=41, 프로젝트 플러그인 우선 로드 | imc.log |
| Prototype 전체+ControlInputDisplayPIE 1차 | NullRHI 11/12 Success·PIEInputLifecycle Fail(기대33 고정) | test.log |
| 수정 후 집중 | PIEInputLifecycle/AcroInputAssetContract/AcroInputBehaviorPIE 3/3 Success | test2.log, report2/ |
| 1차 최종 판정 | Prototype+ControlInputDisplay 12/12 판정은 11/12+수정 후3/3의 조합; 수정 후 전체12개 일괄 재실행과 구분 | Claude 통합 지시서, test.log/test2.log |
| RawInput 장치 등록 | VID1781/PID0E5A 연결 등록 로그 | test.log, test2.log |
| Build 2차 | build3 테스트 플래그 오타 실패→build4 Succeeded | build3.log, build4.log |
| 메뉴 후속 집중 | NullRHI 5/5 Success: InterLinkNavigationContract, GamepadNavigationPIE, GamepadMissionFlowPIE, PIEInputLifecycle, PlayerFacingTextContract | test3.log, report3/ |

- 구현됨/자동 검증됨: 축 연결·전부 반전 해제·Mode2 실측 반영·메뉴 Subsystem/키 설정/Cancel 연결·계약 테스트. 1차 Prototype12/12 판정 유지, 후속은PIEInputLifecycle 재확인이며 새 전체 회귀 합산 아님. Codex가 build/build2/build4 성공·imc41·test2 3/3·test3 5/5 로그를 직접 대조했다. HID 실측 자체는 Claude 지시서 근거다.
- 수동 확인 대기: 비행 축 배치/부호·Dead Zone·쉬운 조작 비복귀 스로틀 고도 유지·게임 Mode2 호버/피치, 노브 방향·딸깍/Cancel이 타이틀/로비/기체 선택/설정/결과 전부 동작·첫 강조·기존 패드 포커스 영향. HID 방향 확인은 실기 게임 체감 Pass가 아니다.
- 미구현/미완료: 조종기 좌우 이동·LB/RB 탭·브리핑 넘김·시점 전환·역할 기능 버튼·CameraPitchRate, 미인식 안내 UI, 다른 송신기 설정·전시 PC 배포 플러그인 포함 확인. 필요 조작은 키보드·마우스 사용.
- 현재 미정: 노브 물리 회전 방향 대응, 미연결 버튼 배치, 미인식 안내 문구, 쉬운 조작 비복귀 스로틀 처리(중앙=고도 유지 Claude 가안), 전시 조종기 정책·멀티 송신기 지원. 원래 1차 세로축 최종값 미정은 2차 실측 설정으로 대체하되 실기 체감은 대기.
- 로컬 반영: STATUS 최신 요약/입력 자산/Acro/다음 확인, WORKBOARD 신규 DR-INTERLINK-INPUT-01·DR-FPV-ACRO-INPUT-02·UI-PAD-01/Next, 입력 계약/기획 답변 2·3절. 상세 계약은 입력 가이드, 검증 이력은 본 절에 모았다. 새 파일/아카이브 없음.
- Unreal 미커밋 대상(Claude 통합 지시서): `Drone.uproject`, `Config/DefaultInput.ini`, `Config/DefaultGame.ini`, 신규 `Plugins/RawInput/`, 신규 `Tools/AssetMigration/BuildDroneInterLinkInput.py`, `Tools/AssetMigration/BuildDroneAcroInput.py`, `Source/Drone/Flight/Tests/DroneAcroInputAssetContractTest.cpp`, `Source/Drone/Flight/Tests/DroneFlightPIEInputLifecycleTest.cpp`, `Content/Drone/Prototype/Input/IMC_DronePrototype.uasset`, 신규 `Source/Drone/UI/DroneInterLinkNavigationSubsystem.h/.cpp`, 신규 `Source/Drone/UI/Tests/DroneInterLinkNavigationContractTest.cpp`, `Source/Drone/UI/DroneFrontEndRootWidget.cpp`, `Source/Drone/UI/DroneSelectionWidget.cpp`. 본 목록은 위임 사실이며 이번 Codex 변경 파일 목록과 구분한다.
- Space 반영: pages:write-page 스킬로 기존 [진행상황과 다음 작업](https://chatgpt.com/space/page_a81d11314f60819188530a4ea2ed4663)(sequence30)·[테스트 맵과 확인 가이드](https://chatgpt.com/space/page_ba2823e59d7c8191b0ea8bab809367dc)(sequence19, 자동 근거 요약 후속20)에 축/메뉴 구현·자동 검증·수동 순서/미정 반영. 저장 연산6건의 적용/거부없음·본문 재조회 확인, 새 Page/공유/예약 없음. 전체 사용자 화면 폭에서 렌더 배치는 미검증.

## 2026-10-07 InterLink DX 버튼·ArmSwitch·노브 전용 메뉴 이동 — D PC Claude

- 작업 도구/실행: Claude(D PC), 문서·Space 반영: Codex. 지시서 `20261007-125357-docs-interlink-buttons`, 이전 interlink-all 미커밋 반영 위 후속. 기준 Unreal `cb77c0d`·MD `6558cca`; 기존 미커밋 변경 보존. 이번 Codex는 Unreal 수정·Build/PIE·패키징·맵 생성·Commit/Push를 실행하지 않았다.
- 사용자 확정(10/07): 버튼3개는 좌클릭/우클릭/P 역할, 자폭1=온·0=오프, 메뉴는 좌우 없이 노브 위/아래만으로 전부 이동. Claude 사용자 HID 실측12:40에서 Button1/12/13 확인; scratchpad `interlink_sample4.log`는 저장소 밖 근거이며 Codex가 읽거나 업로드하지 않았다.
- 구현됨: IMC41→45(기본33+축8+버튼4), Button1 PrimaryAbility와 신규 Boolean ArmSwitch·Button12 SecondaryAbility·Button13 ToggleView. Pawn ArmSwitchAction Started=ArmImpactDetonation/Completed=Disarm, 비행BP4종 연결. 자폭 없는 Scout/Drop/FiberOptic/UGV는 무시·마우스 무장/해제 유지. RawInput ButtonProperties27→32(28~32 상태 포함). 축 재생성 도구는 버튼 보존. 상세 계약은 [입력 가이드](../tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md) 정본.
- 구현됨: StepFocus 강조 목록 이전/다음·끝 순환, FrontEndRoot/Selection/Settings Preview 노브 처리, 결과창 기존 위/아래. 설정 열린 콤보 Slate 위/아래·확인으로 슬라이더 잠금 후 노브 조절·KnobSliderStep0.05(BP 조정 가능), GetKnobStep 추가. 패드·키보드 규칙 유지.
- 테스트 계약: 신규 InterLinkButtonAssetContract 추가4/기존6매핑 보존·BP4종 ArmSwitchAction, InterLinkNavigationContract GetKnobStep, PIEInputLifecycle 매핑45·ArmSwitch2바인딩.

| 검증 | 판정과 범위 | 근거(루트 D:/JGY/project/drone/Saved/Automation/ClaudeInterLink/) |
|---|---|---|
| Build | 지시서 build5 Live Coding 실패(Editor 켜짐)→build6·build7 Succeeded; Codex가 두 성공 로그 대조 | build5~7.log |
| IMC·BP 패치 | OK·replaced=0·added=4·mappings=45·pawns=4 직접 대조 | buttons.log |
| 전체+UI/Flow | 지시서17/18이나 실제 report4는 succeeded14+warnings2·failed1·notRun0, 즉16/17; PIEInputLifecycle Fail | test4.log, report4/index.json |
| 수정 후 집중 | PIEInputLifecycle/InterLinkButtonAssetContract/RoleAbilities 3/3 Success 직접 대조 | test5.log, report5/index.json |
| 최종 판정 차이 | 지시서18/18(실패1건 수정 재실행 포함)과 실제 보고서 집계 차이 Claude 재확인 대기. 전체 일괄 재실행 아님·18/18을 직접 확인한 것으로 쓰지 않음 | 지시서와 report4/5 대조 |

- 자동 검증됨: Build·버튼 매핑/BP 연결·IMC45·노브 계약·수정 후 집중3/3. report4 Success 중 경고2개는 별도 분류하며 실기 Pass로 산정하지 않는다.
- 수동 확인 대기: 기존 축 부호/Dead Zone·Mode2 호버/피치·비복귀 스로틀, Button1 무장/해제 체감·12/13 동작, 노브만으로 타이틀→로비→탭→미션→브리핑→기체 선택→출격→결과 이동·첫 강조·확인/Cancel, 설정 슬라이더 잠금/조절·콤보 목록·노브 방향. 훈련 로비 탭은 코드상 목록 포함·실기 확인 대기이며 미구현 확정으로 쓰지 않는다.
- 미구현/미연결: 브리핑 대사 넘김 조종기 버튼·미인식 안내 UI·CameraPitchRate. 현재 미정: 노브 회전 방향 대응·Button1 물리 종류(누름 버튼이면 누르고 있는 동안 무장될 수 있음)·브리핑 넘김/탭 전용 버튼·안내 문구·전시 정책; 기존 비복귀 스로틀/다기종 미정 유지.
- Unreal 추가 미커밋 대상(Claude 지시서): 신규 `Content/Drone/Prototype/Input/Actions/IA_DronePrototype_ArmSwitch.uasset`, IMC_DronePrototype.uasset, 비행BP4종(FPV/Scout/Drop/FiberOptic), 신규 `Tools/AssetMigration/BuildDroneInterLinkButtons.py`, BuildDroneInterLinkInput.py, `Source/Drone/Flight/DroneFlightPawn.h/.cpp`, Flight/Tests/DroneFlightPIEInputLifecycleTest.cpp·신규 DroneInterLinkButtonAssetContractTest.cpp, `Source/Drone/UI/DroneGamepadFocus.h/.cpp`·DroneInterLinkNavigationSubsystem.h/.cpp·DroneFrontEndRootWidget.cpp·DroneSelectionWidget.cpp·DroneSettingsWidget.h/.cpp·Tests/DroneInterLinkNavigationContractTest.cpp, Config/DefaultInput.ini. 이전 목록에 추가된 인계 사실이며 Codex 변경 파일과 구분한다.
- 로컬 반영: STATUS 현재 요약/입력/미정/다음 확인, WORKBOARD 기존 DR-INTERLINK-INPUT-01·UI-PAD-01 압축 갱신과 DR-FPV-ACRO-INPUT-02 매핑 수 정정, 입력 가이드 버튼 표/메뉴 규칙/6절45매핑·Action15. 본 WORKLOG 끝에만 이력 추가. 기존 기획 답변 파일 변경은 이전 run 결과로 보존·이번 미수정. 새 파일/아카이브 없음.
- Space 반영: pages:write-page 스킬 적용, 기존 [진행상황과 다음 작업](https://chatgpt.com/space/page_a81d11314f60819188530a4ea2ed4663)(sequence31)·[테스트 맵과 확인 가이드](https://chatgpt.com/space/page_ba2823e59d7c8191b0ea8bab809367dc)(sequence21)의6연산 적용/거부없음, 저장 본문 재조회6/6 일치. 버튼/무장/노브 이동·실기 순서·미정·집계 차이 반영. 새 Page·권한/예약 변경 없음, 사용자 화면 렌더 배치는 미검증.
- 크기: STATUS24610→24901B, WORKBOARD29980→29819B(30KB 이하). Claude 확인 필요: 지시서17/18·18/18과 report4 실제16/17 집계 대조. 코드 작업 새 요청은 없음.

- 10/07 집계 정정(Claude 직접 기록): interlink-buttons 지시서의 "17/18·18/18"은 Claude 집계 실수다. `ClaudeInterLink/test4.log`는 17개 중 16 Success·1 Fail(PIEInputLifecycle, ArmSwitch 미등록), 테스트 수정 뒤 `test5.log` 3/3 Success. 실패했던 테스트는 재실행으로 통과했고 나머지 16개는 test4 결과를 그대로 쓴다.

## 2026-10-07 — 비 연출 도입·비 품질 옵션 (C PC Claude)

작업·검증: Claude, C PC `C:\URproject\drone`. 문서 반영: Codex, 지시서 `20261007-110533-docs-rain-quality-docs/prompt.md` 기준. 아래 실행·캡처·실측은 Claude가 전달한 결과이며 Codex 재실행 결과가 아니다. Unreal HEAD `cb77c0d`, 이번 변경은 스테이징 상태. 커밋 메시지 안 `Saved/CommitDraft_RainQuality.txt`. **스테이징까지, 커밋·푸시는 사용자**. Codex는 Unreal 수정·Build/PIE/맵 생성·Commit/Push·문서 스테이징을 실행하지 않았다.

### 승인·구현

- 10/07 사용자 승인: 비 연출 도입과 최적화. 날씨 매니저 유지, 원본 팩 젖음·물결 머티리얼과 소리 도입, 원본 Niagara는 맵 전체 배치 대신 높음에서 카메라 주변1개만 사용.
- 설정 성능 항목 `비 품질` 자동/끔/낮음/중간/높음 추가·기존 설정 SaveGame 저장/복원. 자동은 엔진 효과 품질0→낮음, 1→중간, 2 이상→높음. Claude가 1280×720 캡처로 화면 안에 들어감을 확인했다. 실제 패드 조작 Pass는 아니다.
- `BP_DroneRainVisual.QualityLevels`: 끔은 비 연출 전부 Off, 낮음은 빗줄기 절반·단순 젖음·빗소리, 중간은 빗줄기 전부·물결 절반, 높음은 카메라 주변 원본 Niagara1개 추가. 원본 Niagara는 지붕 차폐가 없어 실내 Off, 빗소리는 실내35%로 감쇠.
- 새 자산 `/Game/Drone/Weather`: `Niagara/NS_DroneRain_NearCamera`는 `NS_Rain_Fast` 복제. `Niagara/NET_DroneRain` Effect Type은 효과 품질 낮음 입자0.35배·중간0.6배·최대2개. `Audio/SCON_DroneRain`은 동시 재생1개. `Materials/MPC_DroneWeather`는 RainWetness/RainDetail. `Materials/M_DroneWetSurface`는 원본 MF_Wetness/MF_WaterRipples 사용, Detail/Simple 인스턴스가 있고 끔·낮음에서는 맵 표면을 Simple로 교체.
- 생성 도구 `Tools/AssetMigration/BuildDroneRainQualityAssets.py`. `Lvl_DroneWeatherSystemsTest` 바닥에 젖음 머티리얼 적용. 원본 ThirdParty·원본 맵은 수정하지 않았다.
- 빗소리는 원본 `SC_Ambience`(`SW_Ambience`, 230초 반복). 실제로 빗소리인지는 미확인.

### 자동 검증·렌더 확인

- 새 `Drone.Weather.RainQualityLevels` Success.
- 전체 회귀128개 중 실패는 알려진 미렌더 패드 포커스6개뿐. 알려진 실패 해결이나 실제 패드 Pass로 해석하지 않는다.
- Niagara 실제 활성화는 Claude 렌더 실측에서1개 확인. Effect Type 최대2개 예산과 구분한다.

### 품질 실측

C PC, RTX3080·i5-13600KF·32GB, `-game` Development, 1280×720 창 모드, VSync·FPS 제한 Off, 엔진 효과 품질 최고(3), `Lvl_OilRigRainComparisonTest` 고정 카메라. 단계마다10초 안정화 후10초 측정, 정순·역순2회. 품질 측정 중 원본 맵 배치 비는 Off.

| 모드 | 평균 프레임(ms) 2회 | FPS |
|---|---|---|
| 끔 | 10.061 / 10.549 | 약97 |
| 낮음 | 10.195 / 10.722 | 약96 |
| 중간 | 10.291 / 10.593 | 약96 |
| 높음 | 10.316 / 11.025 | 약94 |
| 원본 맵 배치25개 | 30.358 / 31.972 | 약32 |

앞선 실측은 **판 빗줄기 버전(폐기)**: 끔9.919/10.022·낮음9.867/10.401·중간9.884/9.995·높음10.109/10.106·원본25개27.702/27.430ms; 당시 구성은 아래 정정 항목으로 대체한다.

재실측 조건은 위와 같다. 첫 단계30.2ms는 준비 구간으로 제외했고 단계 간 차이는0.4ms 안쪽이다. 젖음 머티리얼 비용은 별도 미측정이며 입자 모양의 수동 Pass를 뜻하지 않는다.

### 수동 확인 대기·현재 미정·미구현

- 높음 카메라 주변 원본 비 위치·양의 자연스러움(오프셋600cm는 시험값).
- `Lvl_DroneWeatherSystemsTest` 비 프리셋의 젖음·물결 외형.
- 빗소리 내용·실내 감쇠, 설정 비 품질의 실제 패드 조작.
- 단계별 수치의 최종값·원본 Ambience를 빗소리로 확정할지는 현재 미정. 화면 물방울·바닥 Splash는 미구현.

현재 설정·자산·확인 절차는 [비 가이드](../gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md#비-품질-설정과-조정)가 정본이다. STATUS 날씨 행·WORKBOARD WTH-03/Next 갱신. Space는 이번 지시에서 제외하여 미반영. docs/applications·docs/history/archive와 과거 WORKLOG 본문은 수정하지 않았다.

## 2026-10-07 — 비 품질 정정·원본 Niagara 기반 (C PC Claude)

작업·검증: Claude, C PC. 문서 반영: Codex, `20261007-112159-docs-rain-quality-fix/prompt.md` 기준. 사용자 피드백: 낮음·중간 판 빗줄기(카메라 주변 ISM)가 네모·픽셀처럼 보임. 앞선 구성·단일 사본 설명은 폐기하며 현재 절차는 [비 가이드](../gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md#비-품질-설정과-조정)가 정본이다.

- 낮음·중간·높음 모두 원본 NS_Rain_Fast 사본을 카메라 주변1개 사용한다. 단계별 자산·입자/생성 범위/물결 값은 가이드 참조. 판 빗줄기 전 단계 기본0, 끔·낮음 Simple 머티리얼. 젖음·빗소리(실내35%)·실내 Niagara Off 유지. 예전 NS_DroneRain_NearCamera·NET_DroneRain 삭제.
- 자동 검증: Weather 전체·SettingsContract Success. RainPerformanceBudget은 빗줄기를 명시적으로 켜서 검사하도록 조정. Claude 전달 결과이며 Codex 재실행이 아니다. 이번 개수·새 전체 회귀 결과는 미제공.
- 위 실측 표를 새 값으로 교체했다. RTX3080·1280×720·-game·VSync Off·효과 품질 최고·고정 카메라·10초+10초·정순/역순. 첫 단계30.2ms 제외·단계 차이0.4ms 안쪽. 새 CSV 경로는 미제공.
- 단계별 캡처: `E:\기획안\06_드론_메인\비품질_캡처\`. 고정 원거리 정지 화면이라 비가 잘 보이지 않는다. 입자 크기·모양(픽셀 여부), 위치·양, 젖음·물결, 빗소리·실내 감쇠, 실제 패드 조작은 수동 확인 대기. 최종 수치·음원 채택 현재 미정, 화면 물방울·바닥 Splash 미구현.

STATUS 날씨 행·WORKBOARD WTH-03/Next·비 가이드 정정. Space 지시상 제외. Unreal 수정·엔진 실행·Commit/Push·archive·applications 수정 없음.

## 2026-10-13 D PC — MD 최신화·Pull 완료 후 수신 코드 대조 (Codex)

처음 사용자 `md만 일단 최신화 드론 깃은 아직 풀중이야`로 MD만 읽었다. MD HEAD=로컬origin/main`1c4e76d`(10/08 커밋)·작업트리Clean, 개발 기록은10/07까지였다. 이어 `깃도 받아졌다 최신화` 보고 후 Unreal을 읽기 전용 대조했다. 작업/문서 반영 Codex, 이번 코드·자산·Git 쓰기/Build/PIE/MCP·Commit/Push·Trello/Figma/권한/예약 변경 없음. 초기 MD만 요청 범위를 유지해 Space는 보류·미반영이다.

### 현재 수신 근거

- Unreal `D:\JGY\project\drone` HEAD=로컬origin/main`2a10c3de30bc99700c02683c09f27efd0413f24f`(10/11), 변경 경로0·Clean. MD HEAD=로컬origin/main`1c4e76dcb3c221dd15548e14e88a8a69edcbd225`. 추가 Fetch/Pull/원격 실시간 조회/lock 제거를 하지 않았다.
- git lfs ls-files:9,394개 모두본문표시(*)·포인터표시(-)0. 각 객체 checksum/의존성·자산 호환/실제 게임 실행 검증과는 다르다. 엔진/팀원 Production Training 맵은 저장하지 않았다.
- 문서의 마지막개발기준`cb77c0d`부터현재HEAD의 변경경로:Source103·Config2·Tools27·Content1425·Plugins11·uproject1·.claude1. 전 코드/자산 의미를 전수검증한 것이 아니라 현재요약과 충돌하는 핵심기능을 확인했다.
- STATUS 표에 남은10/06 `0c0ed99/c5a0524`와 수신 후1619b4f Build 안내는 현재기준이 아닌 옛 내용이므로 현재수신/미실행으로 갱신했다. 이전 검사결과는 그날PC/실행담당근거로 보존했다.

### 핵심 코드 확인과 문서 정정

- `Source/Drone/Flow/DroneGameFlowSubsystem.cpp` LoadProgress/SaveProgress·Initialize·NotifyMissionResult:완료 미션·Story Fact·권장문구 표시 여부를 `Saved/SaveGames/DroneMissionProgress.json`로 저장/복원, 성공·권장 표시때 저장. 실패는 이번실행동안만 유지 경고. 따라서 실행메모리만/영구저장미구현 표기를 정정하되 재실행Pass로 표시하지 않았다.
- `Procedural/DroneProceduralCityGenerator.cpp` BeginPlay·RunStage·GenerateCourse와 ProceduralSession:지정/무작위 시드로 도시·날씨·코스단계생성·같은시드 재현·시드/난도 기록키 코드가 있다. FrontEndContractTest와두 DA파일은Circuit.Test+Procedural.Test 2항목을 기대한다. 제품고정4코스 제작/지형확정과 별개이며 실제로비목록/생성/완주는 이번미실행이다.
- `Flow/DroneMissionPlayerController.cpp` BeginProceduralLoadingIfNeeded·BeginStoryLoadingIfNeeded·TogglePauseMenu·RestartFromPauseMenu:로딩/취소·미션중Pause/재개/재시작/타이틀복귀 연결. 일시정지재시작은 같은도시시드예약. 결과창의일반Retry/같은시드Retry는별도계약이다.
- `Tutorial/DroneTrainingRecordSubsystem.cpp` SubmitLap/SaveRecords/LoadRecords:최고랩의구간시간을 bestLapSegments JSON으로 저장/복원하는후속이있다. HUD구간대비는저장최고랩을우선사용. Best와구간재실행복원은수동대기다.
- `UI/DroneMissionResultWidget.cpp/.h`:native는1920×1080 기준TitleKit 팀원상자버튼·좌측버튼열/우측정보카드(InfoPanelWidth 기본900)이며유효Kit이면옛카드보정을건너뛴다. TitlePosition/Font·FirstButtonPosition/Pitch/Font·InfoPanelPosition/Width는BP노출. 배율1유지, Kit선택상태강조. 중앙680은옛native/현재named-WBP fixture기준이므로 현재native 설명을바꿨다.
- InterLink 전체검사집계는10/07정정으로해소됐으므로 카드의집계재확인대기를제거했다(test4 16/17·수정후test5 3/3, 과거실행). 비는끔=Off·낮음/중간/높음=카메라주변원본Niagara1개로명확히했다. 브리핑문구/실기/고정4코스·스토리기획대기는임의완료하지않았다.

### 실행 검증 경계와 다음 작업

이번 수신 뒤새Build/자동화/수동확인은미실행. 로컬Saved/Automation의최신근거는10/07ClaudeInterLink test5.log/report5 3/3이고현재HEAD실행근거가아니다. 최신브리지인계도10/07 interlink-buttons다. 수신 known-test-failures에10/08PauseMenuRacingPIE 첫Resume포커스(전체1회Fail·단독/패드뒤2회Pass) 관찰이추가됐지만실행PC/새로그경로미명시라현재D PC판정으로합산하지않았다.

다음:Claude에서현재HEAD Editor Build/집중회귀확인→지정/무작위시드·같은시드재시작·로딩취소·Esc/Start재개/복귀·현재결과창·진행도/최고구간재실행복원→InterLink/8수업/기존레이싱/NPC·날씨·접촉수동회귀. 소스/LFS수신과바이너리/자동/수동통과를분리하며사용자저장기록·팀원Production을보존한다.

### 문서 정리 범위

WORKBOARD가 30KB를 넘어서 10/06 면접 비교표·옛 PC 인계 행을 원문 그대로 10월 아카이브 끝에 옮기고, 남은 결정 3개는 현재 보드에 요약했다. 원문 삭제·과거 WORKLOG 수정은 없다. 보드 30,133B/146줄→28,197B/143줄, 아카이브 62,958B/277줄→66,553B/302줄. STATUS는25,928B로 두 루트 문서 모두30KB 이하이다. STATUS/WORKBOARD·UI 가이드·README 색인·WORKLOG·기존 아카이브 6개 문서만 변경했고 새 진행 파일/Space Page는 없다. 두 저장소 diff --check 통과, Unreal 작업 트리는 최종 Clean이다. 이번 MD 변경은 로컬 미커밋이며 원격 GitHub/Space에 반영됐다고 표현하지 않는다.

### 같은 날 후속 — 준비된 Gate 자산 적용 요청/메인 맵 포함

사용자 `/Game/Item/Gate`와 머티리얼 M Blue/M Green로 Gate 교체 요청, 이어 팀원 맵이 게이트 메인이므로 그 맵도 적용 대상으로 확장했다. 기존 Production 보존 원칙을 시험용 재생성 금지로 유지하면서, 이번 사용자 지정 외형/재질 교체만 계획에 기록했다. 실제 BP·맵 변경/저장은 아직 없다.

- 파일 확인: `/Game/Item/Gate/{RaceRing,Center,Inner,Outter}`, `/Game/Material/M_BLUE`, `/Game/Material/m_green`. 바이너리의 StaticMesh 이름 표시는 있으나 Export 유형·조립 구조·bounds·재질 슬롯은 Editor 실측 전 확정하지 않았다.
- 공용 후보 `/Game/Drone/Tutorial/Blueprints/BP_DroneTrainingGate`: GateAssetMesh/LocalTransform·Inactive/Current/CompletedMaterial·GateAssetStateMaterialSlots·StateColorParameterName 슬롯이 이미 있다. 단일 메시 지정 시 기존 프레임은 숨기고 판정 Box는 유지한다. 연결 전 원형 개구부/로컬 YZ 방향·Pivot·Trigger 크기를 맞춰야 한다. 원형 외형만으로 판정이 원형이 되지는 않는다.
- 공용 기본값만 바꾸면 Native Gate나 개별 override에는 전파되지 않을 수 있으므로 메인 맵 각 Course의 AutomaticGateClass·기존 Gate override와 Procedural CourseClass를 확인한다. 코스 순서/개수/위치/Scale·Spline·통과 판정/소리·기존 팀원 변경은 보존한다.
- 상태 재질은 실제 색 변경 슬롯만 지정하고 금속/기둥 슬롯은 보존한다. Color 파라미터가 있으면 기존 상태 색이 재질 자체 색을 덮을 수 있어 원본을 확인한다. M_BLUE/m_green의 상태 배분과 통과 후 기존 상태 유지 여부는 적용 전에 정한다.
- `ConfigureAutomaticTrainingGates.py`는 Production에서 수동 Gate 삭제·재배치·맵 저장까지 하므로 이번 외형 교체에 그대로 실행하지 않는다. 현재 UnrealEditor 프로세스는 실행 중이며 열린 레벨/미저장 변경은 확인하지 못했다.
- Unreal MCP 도구 없음·현재 역할 규칙상 Codex의 임의 CLI/Unreal 스크립트 실행 금지. 실행 방식 예외 승인을 받거나 Claude에서 적용해야 한다. 이번에는 읽기와 MD 카드만 변경했고 Unreal 자산/Source/맵·Build/PIE·Commit/Push를 실행하지 않았다. Space는 앞선 MD만 범위에 따라 계속 보류한다.

### 같은 날 후속 — 지정 BP 실행·패트리어트 접합부 회전과 Gate 연결

2026-10-13 KST D PC. 앞선 저장/종료 요청에 사용자가 `저장하고 종료해놨어`로 답한 뒤 지정 자산 작업에 한해 Codex CLI 실행 예외로 진행했다. 이어 받은 패트리어트 포대 요청을 별도 Actor BP로 구현했다. 상시 Claude/Codex 역할 규칙·AGENTS는 바꾸지 않았다. Unreal MCP·C++ 수정·Commit/Push·Trello/Figma/권한/예약 변경은 없다.

#### 수신·빌드와 변경 경계

- 사용자 추가 Pull로 Unreal HEAD=로컬origin/main `965b993a`, MD `1c4e76d` 확인. 앞선 `2a10c3de` 이후 수신은 패트리어트 메시/재질/텍스처와 Landscape Island 맵이며 Source 변경 없음. Codex가 Fetch/Pull하지 않았다.
- 시작 Editor 종료 확인. UE5.8.2의 `DroneEditor Win64 Development`, CompilerVersion `14.51.36257` 지정 Build: **Succeeded / Target is up to date / 컴파일 작업0**. preferred compiler14.50 경고가 있어 빌드 전체 경고0이라고 하지 않는다. `Saved/Automation/CodexGateItem/build.log`.
- 변경 자산: 기존 `BP_DroneTrainingGate`, `BP_DroneTrainingCourse` 2개와 신규 `BP_PatriotMissileLauncher` 1개. 신규 Tools/AssetMigration 도구2개. Source/Config/Plugins/uproject·원본 Item/Material·맵 파일은 변경하지 않았다. 원본 Gate/Course BP와 Main 맵은 Saved/Automation/CodexGateItem/Backups_965b993a에 복사 보존했다.

#### 패트리어트 접합부 BP

- `/Game/Item/missile/Missile_Lower/Middle/Upper`가 실제 StaticMesh3개임을 UE GeometryScript 정점/삼각형과 bounds로 확인. 모두 전체 조립 하단 원점을 공유해 상단 단독 회전 시 접합부가 이동하는 형태다. 메시 원점·원본 재질은 수정하지 않았다.
- `/Game/Drone/AI/Blueprints/Turrets/BP_PatriotMissileLauncher`: Actor 직접 부모, `FixedSceneRoot → LowerMesh + YawPivot → MiddleMesh + PitchPivot → UpperMesh`의 SceneComponent6개. Yaw joint `(0.315,-4.35,13.33)`cm, Pitch joint `(0,-11.50,60.40)`cm. 받침/어깨 형상으로 잡은 초기 접합부 값이며 실제 이음새 미세 조정은 수동 확인 대기. 자식 메시 역오프셋으로 무회전 원본 조립좌표 유지.
- 좌우는 YawPivot의 Yaw/Z, 상하는 발사부 길이Y에 맞춰 PitchPivot의 **Roll/X**. 원본 메시 슬롯은 WorldGridMaterial이어서 BP Component 슬롯0에 제공 `Missile_M`을 오버라이드했다. Movable, NoCollision/NoPhysics의 조립 rig이며 AI/조준/발사/입력/네트워크/차량 부착/맵 배치는 미포함.
- 진단 loop: 실제 UE Transform API로 원점 기준 Roll30°에서 접합부 이동 **31.826998cm** 재현, pivot+역오프셋에서는 **0cm**. 잘못된 오프셋1cm red fixture도 검출. 실제 BP 임시 Actor7개에서0/±90Yaw·±30Roll·복합 회전, 하단 고정·부모 관계·원본 조립좌표·재질 검사 통과. 저장 후 새 프로세스로 같은7회 재검증 성공, 최대 위치 오차 약4.28e-14cm(허용0.1cm). 자동 검사와 접합부 최종 외형 검증은 구분한다.
- 첫 생성 도구 실패는 UE SubobjectDataSubsystem의 SCS 재귀 child handle 중복 수집이었다. 설치 소스 FactoryCreateInheritedBpSubobject의 이중 append와 실제 같은 UObject를 확인하고, opaque Python handle `==` 대신 동일 component/parent/associated UObject·경로·flags에 한해서만 합쳤다. 실제 SceneComponent6개/부모 관계는 임시 Actor에서 다시 검사했다. 실패 과정은 저장하지 않았다.
- 근거: `Saved/Automation/CodexPatriot/apply3.log`, `verify.log`, 대응 apply/verify JSON. 둘 다 종료0·Python 성공, 최종 commandlet summary 오류/경고0. 스크립트 `Tools/AssetMigration/BuildPatriotLauncherBlueprint.py`; 조정 절차는 [MG·패트리어트 가이드](../ai/DRONE_MG_TURRET_3PART_GUIDE.md#6-패트리어트-미사일-포대-접합부-회전축-조정).

#### RaceRing 공용 연결과 Main 읽기 확인

- 실제 타입 정정: Gate 폴더의 `RaceRing`만 전체 StaticMesh, `Center/Inner/Outter`는 MaterialInstanceConstant다. 바이너리 문자열의 StaticMesh 표시는 타입 근거가 아니었다. RaceRing 슬롯0 Outter=M_black, 1 Center=M_BLUE, 2 Inner=m_white, 원본평면XZ·외곽225.6cm·개구부반쪽100cm를 확인했다.
- 공용 Gate BP: RaceRing·Yaw90°·Scale1.75·X중심보정-2.21339cm. 기존 TriggerHalfSize175cm 개구부에 맞춘 외형 보정이며 Box 판정은 그대로다. 실제 bounds8점을 UE Transform으로 검사해 **X두께4.426828cm·Y/Z394.800011cm·중심오차0.000000654cm**, Gate YZ 평면 정렬 확인. Python Rotator 위치 인자가 C++ 순서와 달랐던 최초 저장은 키워드 인자로 정정·재저장·재로드했다. 잘못된 Pitch90은 이 평면 검사가 실패하도록 보강했다.
- 상태 슬롯 `[1]`, Inactive/Current/Completed 부모 `M_BLUE/m_green/M_BLUE`, Vector Parameter `Param`으로 연결. 원래 세 상태 색을 유지해 어두운파랑/초록/밝은청록 구분, 검정0/흰색2는 원본 유지. 음원은 임의 연결하지 않았다. Course BP의 AutomaticGateClass도 Gate BP로 연결했다. 원본 메시/Material과 Actor/Trigger 크기는 바꾸지 않았다.
- `bp_apply2.log` 지정 BP2개만 저장 성공. `bp_verify.log` 새 프로세스에서 저장3상태부모/Param·CDO 보존·임시 BP Gate 실제 Inactive MID/Param·원본슬롯·정렬·Trigger `(60,175,175)` 확인. Current/Completed 실제 전환은 Python 비반사 API를 우회하지 않고 기존 Native 자동화로 검증했다.
- Main 읽기: Course1개, 실제 Sequence78개(0~77·valid), Gate 객체98개. BP 기본값 승계 후 활성78개는 새 Gate BP/RaceRing이고 첫 목표1개 Current. `active_training_verify.log`와 `active_training_verification.json`에서 **78개 실제 메시/정렬·상태 MID 부모/Param·미선택 슬롯** 확인. 화면/완주 검증은 아니다.
- 전후 감사에서 위치·스케일·순서·거리·Spline점/접선·Trigger·안내선 예상 밖 차이0. 동일 생성태그·Child/Component 경로를 확인한 78개에 대해 Native→GateBP 클래스/자동 기본 라벨390개만 의도된 메타데이터 차이로 별도 보고했다. ID/이름 정규화로 차이를 숨기지 않았다.
- 사용 Sequence 밖 기존 Native20개는 `GetGateTrigger()==None`, 그중10개는 `GetGateAssetVisual()==None`이다. 이름이 같은 컴포넌트는 남아 있으므로 삭제됐다고 단정하지 않고 **native 참조 연결 문제**로 기록한다. `map_apply_blocked2.log`는 변환 감사 통과 후 이20개를 SCOPE_BLOCKED로 보고하고 변경/저장 전 중단했다. 기존 객체 복구/삭제·맵 정리는 별도 범위 결정 필요.
- Main 맵 파일394,031,686B, SHA256 `22F016ECF2F7CC0AC8EE6D3D421DEB0EB676DD87A2C40B9167F8A49845ECAC5D` 전후 동일. SaveAll/맵 저장/명시적 Course Rebuild/기존 Gate 삭제는 없음. 기존 위험한 ConfigureAutomaticTrainingGates.py도 실행하지 않았다. Engine의 로드/Construction에 의한 공용 기본값 승계와 명시적인 맵 재배치를 구분한다.

#### 자동 회귀·남은 확인

- Entry/nullrhi의 기존5개 자동화 **모두 Success**: `Drone.Tutorial.TrainingGateBlueprint`, `TrainingGatePresentation`, `TrainingGateSequence`, `TrainingCourse`, `CourseManyGates`. 보고서집계 Success4·SuccessWithWarnings1·Fail0. `CourseManyGates`의 시험 World 정리 `UWorld::DestroyActor: World has no context` 경고100건이 있어 전체 경고0 완료는 아니다. Gate/Course BP compile 오류·경고0 assertion은 통과했다. Source 테스트 정리 수정은 이번 BP 예외 범위 밖이며 Claude 후속이다.
- `Saved/Automation/CodexGateItem/regression.log`, `RegressionReport/index.json`; Queue Empty5·종료0. 초기 엔진 self-test 로그의 Condition failed와 이5개 결과를 혼동하지 않았다. 전체 Drone.*·실제 Standalone/PIE·수동 화면 검증은 실행하지 않았다.
- 다음: Patriot BP Viewport/TestMap에서 이음새·크기·±Yaw/±Roll/복합 회전, Main78 링 외형/정순서 상태색 확인. 비사용20개 정리 범위는 별도 합의. 기존 새 도시/로딩/일시정지/저장·전체UI/패드 회귀는 Claude 후속이며 이번 집중 성공으로 완료하지 않는다.

#### 가이드에서 WORKLOG로 옮긴 과거 검증 원문

주제 가이드는 현재 조정 절차만 유지하므로 아래 원문을 이력으로 보존한다. 현재10/13 검증으로 재사용하지 않는다.

> 2026-09-30 Editor Build와 관련 회귀 8/8(오류·경고 0), 실제 Gate/Course BP Compile 각각 0/0을 통과했다. Test World 종료 경고도 최종 재실행에서 0건이다. Production 맵/Asset 저장 없이 검증했다.

이번 MD는 기존 STATUS/WORKBOARD·주제가이드/색인·WORKLOG에 반영했다. 신규 진행 문서·삭제·원격 GitHub 반영은 없으며 변경 파일은 사용자 Commit/Push 대상이다. Space 관련 페이지의 저장 결과는 최종 동기화 확인 기록을 따른다.

최종 동기화 확인: 기존 Space의 진행상황·Blueprint 가이드·테스트 가이드 3개에 6연산을 적용했고, 저장 후 대상 블록 재조회로 기대 본문과 일치를 확인했다(Sequence32/20/22). 과거 날짜별 기록과 링크·기획/안내·Root/권한은 보존했고 새 Page는 만들지 않았다. 페이지 렌더의 모든 화면 폭은 미검증이다. 로컬 MD8개 변경, STATUS27,439B·WORKBOARD28,820B로30KB 이하; 두 저장소 diff --check 통과(CRLF 예고만), Unreal은 BP2개 변경+BP1개/도구2개 신규 상태다. 맵 SHA/원본 자산·Source 미변경, Editor 프로세스 종료 유지. Commit/Push는 하지 않았다.

## 2026-10-14 — 수신 기준·Gate/Patriot 검증 경계 최신화 (D PC Codex)

사용자 “업데이트”에 따라 Git·소스/도구·기존 로그를 읽고 STATUS/WORKBOARD·관련 가이드·Space를 정리했다. Unreal 실행·MCP·Build·새 자동화·맵/자산 저장·Fetch/Pull·Commit/Push는 하지 않았다. 점검 시 UnrealEditor 프로세스는 관찰되지 않았다. 문서 최신화는 기능 구현/수동 Pass를 뜻하지 않는다.

### 수신 기준과 변경 범위

- Unreal HEAD `a57a4444`=로컬 `origin/main`, MD HEAD `b38fc84`=로컬 `origin/main`; 두 저장소 점검 시작 Clean. 실제 원격 서버와 타 PC 작업 트리는 미조회다.
- Unreal `965b993a..a57a4444`는 2커밋·19파일 변경. `454a982f`에 이전 Gate/Course BP·Patriot BP·적용/생성 도구가 커밋 수신됐고 `a57a4444`에 Training·MWLandscapeAutoMaterial Island/MountainRange·Demonstration 맵과 Anim 추가/이동이 있다. Source·Config·Plugins·uproject 차이는 없다. Anim 이동 후 참조 무결성은 Engine에서 새로 검사하지 않았다.
- 팀원 커밋 본문 “레이싱콘텐츠 미션3까지 완료”를 보고 수신으로 기록했다. 실제 진입 맵/DA 연결·시작점·완주/기록·4코스 전체 진행도는 미확인이다. 이전 “4코스 미구현”·아이템/Gate 무참조·단일 지형 조사 결과를 현재 판정처럼 쓰던 문장을 정정했다. 이번 diff에 미션 DA 변경은 없다.
- 현재 Training 파일은 394,745,474B로 이전 검사본394,031,686B와 다르다. 체크아웃 파일 시각을 오늘 맵 편집의 증거로 사용하지 않는다. 10/13 당시 Main 자동78개/비사용 Native20개 참조 조사는 역사적 근거이며 현재 개수/연결 재검증이 아니다.

### 기존 Editor 로그에서 새로 확인한 경계

근거는 `D:\JGY\project\drone\Saved\Logs\Drone.log`의 10/13 UE5.8.2 세션이다. 로그 내부 UTC를 KST로 환산했으며 해당 세션의 Git HEAD는 로그에 없어 단정하지 않는다.

- 12:41:48(`LogMaterial`·`MapCheck`, 약2049행): `/Game/Material/m_green`에 Nanite 사용 플래그 누락, Editor 밖 렌더링을 위해 재저장 필요 경고. Map Check 오류0/경고1. 이 세션에서 해당 재질 저장/해결 근거를 찾지 못했으므로 **해결 여부 미확인**으로 기록했다. 지금 재질이 반드시 깨진다고 단정하지 않으며 이번 수정하지 않았다.
- 12:49~12:50(약2446행 이후): Patriot BP Editor 열기·트랜스폼 Undo·12:50:14 BP 저장과 이후 Compile 로그가 있다. 현재 BP35,958B는 초기 생성본31,030B와 다르다. 초기 생성/새 프로세스 재로드의 각7회 검사 후 저장된 버전이므로 **현재 저장본의 Pivot 위치/회전·이음새/크기는 재검증 대기**다. Compile 로그만으로 오류/경고0을 선언하지 않는다. 현재 BP Details 우선·기존 조정 보존·생성 도구 덮어쓰기 금지를 가이드에 명시했다.
- 이후 FrontEnd PIE→RacingTest 진입·DroneMissionGameMode·Pawn 생성/빙의·MISSION-COUNTDOWN 로그2회, 12:51 정상 Editor 종료가 있다. 진입/카운트다운 근거이며 랩 완주·최고 기록 저장/복원·Gate/Patriot 수동 Pass 증거는 아니다.
- `UE::UnifiedErrorTest` 인접 `LogAutomationTest: Error: Condition failed`15행은 이름 있는 Drone 테스트 결과와 구분했다. 이를 신규 Drone15개 실패로 집계하지 않는다.
- `Saved/Automation`의 최신 근거는 10/13까지이며 10/14 새 Build/테스트 결과는 없다. 이전 Build/Gate5/5·Patriot7+7과 Claude 결과를 현재 HEAD 전체 통과로 재사용하거나 합산하지 않는다. CourseManyGates 정리 경고100건도 해결된 것으로 바꾸지 않았다.

### 정리 결과·다음 순서

STATUS/WORKBOARD와 Training 배치·MG/Patriot 가이드·이력 총5파일만 수정했다. 현재 정보는 교체하고 과거 이력은 보존했으며 신규 진행 문서를 만들지 않았다. 다음은 현재 Patriot BP 축/이음새·복합 회전 → 변경 Main의 Gate 개수/참조·세 상태색/m_green 경고 해결 및 Editor 밖 렌더 → 팀원 레이싱 보고와 실제 맵/완주/기록 대조 순서다. Production 덮어쓰기·삭제와 새 구현은 이번 범위가 아니다.

Space 기존 진행상황·Blueprint 가이드·테스트 가이드3개에 총9연산을 적용하고 대상9블록 재조회로 기대 본문 일치를 확인했다(Sequence33/21/23). 안내/기획·Root·권한/예약·Trello·Figma는 변경하지 않았다. 유지관리 스킬에 따라 현재 근거와 과거 검증을 분리해 기존 블록만 갱신했다. 페이지 전체 화면 폭/렌더는 미검증이다.

최종 점검: STATUS28,027B·WORKBOARD28,839B로30KB 이하. 두 저장소 diff --check 통과, Unreal Clean·HEAD a57a4444 유지, MD5파일만 로컬 변경이다. Commit/Push는 사용자 담당으로 남겼다.

## 2026-10-14 — 후속: 고정 조종자 첫 수업·미션 박스 치환·실제 그물/공통 접촉 요구

사용자 요청을 현재 코드와 읽기 전용 대조하고 Claude 인계 카드4개를 정리했다. 역할 규칙에 따라 Codex는 C++/BP/맵을 수정하거나 Unreal·MCP·Build·자동화를 실행하지 않았다. 앞선 문서 미커밋 변경을 보존했고 신규 기능은 구현 완료가 아니다.

### TUT-OBSERVER-01 — 첫 수업 교체 기준

- 해석/기준: 기존 첫 `Mission.Tutorial.Hover`를 기초 수업으로 확장한다. 9번째 수업 추가나 취소된 사람 캐릭터 조작 부활은 아니다. 기존8수업 ID·저장 키·다음 수업 연결은 보존한다. 새 독립 수업 추가가 필요하면 번호/기존 완료 기록 정책을 따로 정한다.
- 카메라는 지상 사람 눈높이의 고정 관찰 시점(LOS)이며 드론 FPV와 다르다. 카메라 월드 위치·회전은 고정하고 드론 소유/Possess와 입력은 유지한다. 수업 한정 ViewTarget 정책으로 구성하고 출격/재출격에 재적용·종료/다음 수업에서 해제한다. P 시점 전환 등으로 해당 수업 카메라가 덮어써지지 않아야 한다.
- 순서: 바닥 출발 → 이륙/목표 높이 유지 → 전진 구역 → 후진해 출발 패드 복귀 → 실제 접지·정지. 전/후진은 초기 방향·기체 방향과 이동을 함께 확인해 옆길/180°회전 후 전진으로 후진 수업이 완료되지 않게 한다. 패드 공중 통과만으로 착지 성공 처리하지 않는다.
- 착지: 패드 안·바닥 접촉 또는 짧은 하향 지면 확인·허용 수평/수직 속도·안정 유지 시간을 함께 판정한다. 목표 높이/거리·허용 오차/속도·유지시간·카메라 높이/FOV는 BP/DA 조절값이며 최종 숫자는 이번 임의 확정하지 않았다. 안내 UI는 현재 단계와 완료 이유를 표시한다.
- 실제 대상: `Source/Drone/Flow/DroneMissionPlayerController.cpp:390,777` 출격/재출격 Possess, `Source/Drone/Flight/DroneFlightPawn.cpp:1154` 드론 시점 분기, `Source/Drone/Tutorial/DroneTutorialHoverZone.*`, `Tools/AssetMigration/BuildDroneTutorialMissionTest.py:87`, `BuildDroneIsolatedMissionMaps.py:21`, `DA_Mission_Tutorial_Hover`와 `TestMap/Tutorial/Lvl_Tutorial_Hover_Test`.
- 현재 생성 도구의 첫 수업은 3초 호버→귀환뿐이다. `DroneMissionReturnZone.cpp:59`는 단순 Overlap으로 ReturnToBase를 보고하므로 착지 판정으로 그대로 쓰면 안 된다. 전용 목표 Event를 추가한다면 기존 enum 직렬화 숫자는 보존한다. 화면/자동화 기준은 고정 카메라+입력 정상·기체1대·단계 순서/건너뛰기 방지·공중 귀환 미완료·착지 완료·재출격/다음 수업 시점 복원이다.

### MISSION-MARKER-01 — 배치 박스를 실제 콘텐츠로 치환

팀원 보고상 미션맵에 net/적 등 박스가 있으나 실제 맵별 위치/수량/라벨·대상 미션 DA는 아직 Engine에서 읽지 않았다. 이름만 보고 적 무기/역할을 임의 선택하지 않는다. Claude가 DA→MissionMap과 각 Actor 경로·라벨·종류·Transform/Bounds·Tags/TargetId·폴더·외부 참조를 목록화해 교체 BP 매핑을 확정한다. 미매핑/중복/목적 불명 항목은 보류하고 원본을 보존한다.

Net 박스의 크기는 그물 폭/높이·고정점으로 변환하며 무조건 Actor Scale로 복사하지 않는다. 적은 종류·바닥/Nav 배치·순찰/목표 참조를 유지한다. 검증된 BP만 시험 복사본에서 먼저 치환하고 원본/교체/보류 수 일치·미션 목표·재시작·그물 크기를 확인한 뒤 승인된 맵을 개별 반영한다. 기존 생성 도구로 팀원 맵을 재생성하거나 Production Training을 시험 저장하지 않는다. 외형만 바꾸고 목표 Tags를 잃는 변경은 불합격이다.

### PHY-NET-03 / PHY-COL-01 — 실제 차이와 구현 대상

- 그물: `Source/Drone/Physics/DroneNetPlacementRig.cpp:24,30,321`은 Tick 없는 Cube ISM·계산 처짐이며 `:264`의 파단 조각만 SimulatePhysics다. 현재 전체 그물이 중력·접촉으로 늘어지는 물리는 아니다. 고정점 유지·중력 처짐·접촉 국소 변형·복원/감쇠를 실제 Cloth/Dataflow로 Sandbox에서 검증한다. 크기/간격·고정점·강성/감쇠 등 BP 조정과 Reset을 포함한다. 기존 포획 게임 규칙은 보존하고 일반 접촉 즉시 절단은 금지한다.
- 상호작용: `DroneCollisionResponseComponent.cpp:332,499`가 NetPlacementRig를 직접 Cast하므로 새 Cloth 표현과 기존 포획의 호환 계약을 유지/분리해야 한다. Cloth 표시만 바꿔 포획이 사라지거나 고정 ISM/새 대리 충돌이 중복 반응하는 상태를 피한다. 줄/구멍과 실제 판정 대리 형상 차이·성능 제한은 검증으로 밝혀야 한다. 기술 근거는 Epic [Panel Cloth Editor Overview](https://dev.epicgames.com/documentation/en-us/unreal-engine/panel-cloth-editor-overview)의 Cloth Asset/Dataflow·Runtime Component·Weight Map/Collision 제작 흐름을 읽기 확인했으며 프로젝트 자산 제작 성공을 뜻하지 않는다.
- 벽: `Flight/DroneFlightPawn.cpp:200`의 공통 CollisionResponseComponent와 `Physics/DroneCollisionResponseComponent.cpp:29,341`의 OnActorHit/일반 OtherActor 처리에 이미 특정 시험벽 제한이 없다. 새 특수벽 코드를 만들기보다 옆면 범위를 보강하는 작업이다.
- 빈틈: `DroneFlightPawn.cpp:85,104`의45cm Root구/외형 NoCollision, `DroneCollisionResponseComponent.cpp:17,475`의 대각4점(±95,±95,0)·12cm Probe와 `.h:172`의 Visibility 채널 때문에 모델 옆면/날개·충돌 채널별 누락 가능성이 있다. 현재 위치의 중심→끝 검사만으로 고속 이전 위치부터의 외곽 이동 Sweep을 보장하지 않는다. 실제 맵 증상을 확인한 뒤 BP별 외곽 범위·공통 환경 채널·이동 Sweep을 보강한다. 현재 증상을 재현·원인 확정한 것은 아니다.
- 수락 기준: 일반 StaticMesh 벽/기둥의 전후좌우·로터 끝, 서로 다른 드론 크기, Pawn Block/Visibility Ignore 조합, 저속<고속 반발량, 모서리·연속 압박·고속 얇은 벽을 확인한다. 카메라는 부드럽고 안정적으로 유지하며 총알 피해 Shake는 남긴다. 바닥 착륙·천장·UGV 제외 정책은 기존 유지, 강한 Crash/Damage·Landing 통합은 기존 후속과 대조한다. 충돌 형상이 없는 장식 메시까지 감지한다고 약속하지 않는다.

진행 순서: 1번 수업 → 미션 박스 목록/매핑 → Sandbox에서 실제 그물·옆면 공통 접촉 검증 → 검증된 Actor로 맵별 치환. 상세 물리 절차는 기존 `DRONE_CHAOS_DATAFLOW_PLAN.md`에 갱신했다. Build·자동 회귀·수동 화면 검증은 모두 구현 담당의 후속이며 이번 Pass는 없다. MD와 Space 반영/최종 상태는 아래 확인 기록을 따른다.

반영 확인: Space 기존 진행상황·BP 가이드2개/3블록을 수정하고 재조회로 기대 본문 일치를 확인했다(Sequence34/22). 새 Page·예약·권한·Trello 변경 없음. 기존 미커밋 포함 MD6파일, STATUS28,673B·WORKBOARD29,430B로30KB 이하. 두 저장소 diff --check 통과·Unreal Clean 유지. 코드/맵 구현과 실제 박스 인벤토리는 미실행이며 Commit/Push는 하지 않았다.

## 2026-10-14 — 후속: Story 표시명 확정·박스 후보 맵 조사 범위

사용자 확정명은 M1 골든 타임/GOLDEN TIME, M2 길목 차단/INTERCEPT, M3 보급 차단/SUPPLY BREAK, M4 최종 타격/ENDGAME이다. CONTEXT에 정본 표를 두고 STATUS/미션 가이드에서 연결했다. MISSION-NAME-01은 Claude 담당 DA DisplayName/EnglishTitle·화면 검증 대기로 남겼다. 내부 MissionId·StoryFact·저장 키·맵/DA 경로·미션 목표는 변경하지 않는다. M3 내부 VeilBreaker는 호환용으로 보존한다.

읽기 확인: `SetStoryMissionTexts.py`의 M1/M2/M4 문구는 요청과 같고 M3는 장막 돌파/VEIL BREAKER다. 도구상 기본값 확인이며 현재 DA 본문 재조회가 아니다. 이 도구는 설명/무전/목표 요약/팁도 쓰므로 이름만 바꾸려고 전체 실행하면 안 된다. 구형 RenameDroneMissionDisplayNames·Story 빌더의 표시 기본값도 역덮어쓰기 방지를 위해 동기화 대상이다. 결과 Widget은 EnglishTitle을 M3 SupplyBreak처럼 자동 축약하는 기존 계약이 있어 로비/부제/브리핑/로딩/기체 선택/HUD/결과 표시를 대조해야 한다. 이번 이름 변경만으로 UI 포맷·게임플레이를 임의 변경하지 않는다.

Space 기획·진행 Page2개/2블록 저장 및 재조회 일치를 확인했다(Sequence2/35). 실제 Unreal DA/UI 수정·Build·화면 검증은 하지 않았다.

이후 사용자 지정 후보는 `/Game/Drone/Maps/Lvl_Battlefield`, `Lvl_MilitaryBase`, `Lvl_MilitaryCamp`다. 각각 파일73,233,451B/215,783,918B/50,378,631B 존재를 확인했다. 기존 도구·Saved 로그/자동화·브리지·문서에서 현재 박스 Actor 인벤토리는 찾지 못했다. 과거 이식/MapCheck·강/지형 기록은 플레이스홀더 목록으로 재사용하지 않았다.

보조적으로 파일 내부 ASCII/UTF-16 문자열을 읽었으나 boxContainer/Cube/GuardTower 등은 ActorLabel·실제 배치/역할/박스 크기의 검증이 아니다. net/enemy 후보 문자열이 검출되지 않았다고 배치가 없다고 판정하지 않는다. 광범위 문자열 나열의 첫 읽기 보조 세션은 중단했고 이후 제한 검색2개는 완료했다. 파일은 수정하지 않았다.

확정된 후속 절차: 세 맵 실제 Actor 목록(맵/경로/표시명/클래스·메시/Transform/Bounds/Tags/참조)을 읽기 전용으로 확보 → 교체 후보/불명 항목 표를 사용자에게 제시·질문 → 답변 후에만 승인된 치환. 사용자 확인 전에 그물/적 종류를 임의 결정하거나 삭제·저장하지 않는다. 현재 역할 규칙상 Unreal 도구 실행은 Claude 담당이므로 실제 맵 인벤토리 단계는 미실행/담당 인계 대기다.

후속 확인: 진행 Page의 후보3맵·사용자 확인 후 치환 경계를 저장/재조회 확인했다(Sequence36). STATUS28,894B·WORKBOARD29,717B로30KB 이하, MD diff --check 통과·Unreal Clean 유지. 이름/후보 맵 문서만 갱신했고 실제 박스 발견/개수 확정·맵 로드/수정·커밋/푸시는 하지 않았다.

## 2026-10-14 — 사용자 승인 직접 구현·미션 치환·Pretendard UI·Gate 저장 수리 (D PC Codex)

사용자 “너가 작업다해 오늘은”으로 오늘 C++/자산/엔진 실행을 직접 승인받았다. 기존 Codex/Claude 상시 분담·AGENTS는 변경하지 않았다. Unreal `a57a4444`·MD `b38fc84`에서 시작한 로컬 미커밋 작업이며 Fetch/Pull·Commit/Push·MCP·Trello/Figma·공유 권한·예약은 실행하지 않았다. 현재 PC 엔진은 UE5.8.2, 빌드는 DroneEditor Win64 Development·MSVC14.51.36257이다. 실행 결과와 수동 체감은 구분한다.

### 구현과 승인된 자산 반영

- 첫 `Mission.Tutorial.Hover`를 지상 고정 사람 눈높이 카메라에서 이륙/안정→전진→방향 유지 후진→실제 접지 착지4단계로 확장했다. 드론 소유/입력·8개 ID/Next/저장 호환 유지, P 시점 전환이 관찰 카메라를 덮어쓰지 않으며 재출격은 단계 초기화·다음 수업은 시점 복원한다. 거리/높이·방향/속도 오차·유지시간·카메라 BP 조절. `BP_TutorialObserverLesson`과 `TestMap/Tutorial/Lvl_Tutorial_Observer_Test`를 만들고 Hover DA만 새 수업으로 연결했다. 기존 Hover/공용/Production Training 맵은 미저장. 과거 생성 도구가 이 DA를 역덮어쓰지 않도록 보호했다.
- NetPlacementRig를 공유 매듭 PBD 중력·구조/전단 제약·감쇠·국소 충격·드론/지면 접촉으로 변경했다. Top Corner/Top Edge 고정, 하단 자유·Slack/강성/충돌 예산 BP 조절, 기존 포획/해제/파단/Reset 유지. 일반 접촉 자동 절단은 금지다. **실제 Chaos Cloth/Dataflow 제작을 완료한 것이 아니다.** 벽 반발은 몸체·로터 외곽 자동 범위와 시간/방사 Sweep·Pawn 충돌 채널을 보강했다. 카메라 안정화·총알 피해 Shake·착륙/천장/UGV 예외는 유지한다.
- 새 `BP_DroneJammingRadar`는 빈 RadarMesh 슬롯과 기지 중심 Offset/범위/중심 강도 반경을 조절한다. 화면 Noise→NO SIGNAL/조종 입력 차단·이탈 복구, 약한 신호는 영상만 방해한다. 입력 손실/복구 때 이전 입력 캐시를 지우되 실제 속도/비행 물리를 배율로 늦추지 않는다. 광섬유 드론은 노이즈·연결 차단에 면역이다.
- Story DA4개의 확정 표시명을 확인했고 M3만 보급 차단/SUPPLY BREAK로 새 저장했다. 내부 VeilBreaker·ID/Next/Story Fact/맵/목표는 유지했다. 이름 전용 도구와 과거 생성 기본값을 동기화했으며 설명을 다시 쓰는 전체 도구는 실행하지 않았다.

실제 세 맵 로드 목록은 Battlefield1828·MilitaryBase3061·MilitaryCamp4593 Actor였다(로드된 Actor 기준, 미로드 Partition 전체 증명 아님). 사용자 승인 후 Battlefield M_net~M_net8 전부→물리 그물8, M_Target→M1 전달1; MilitaryBase M_Turret1→설치 무인1, 숫자 없는 M_Radar→재밍1을 저장했다. 원본11박스는 삭제하지 않고 Drone/ArchivedMarkers·비표시/무충돌로 보존했고 두 원본 umap bytes를 Saved에 백업했다. 그물 원래 폭/높이·상단 고정/하단 자유, 기존 NPC/포탑과 주변 Actor를 보존했다. 레이더는 빈 Mesh·기지 범위 반경159.67m/반높이50m·최대 강도30m로 시험 배치했다(채택 최종 수치 아님). 숫자 레이더/타워5개·MilitaryBase M_Target·MilitaryCamp·Production Training은 미변경이다.

환경 배정은 사용자 확정 Battlefield=M1·MilitaryBase=M2/3·MilitaryCamp=M4다. **Story DA의 실제 진입은 아직 기존4개 TestMap**이며 제품 맵 시작/목표/실패 연결 완료라고 쓰지 않는다. MilitaryBase M_Target의 역할은 사용자도 미확정이므로 보류한다. 기존 M1 PayloadTarget Actor는 이동/삭제하지 않았다.

### Select_UI와 실제 Pretendard 텍스트

Select_UI 원본21PNG를 처음 연결한 뒤, 사용자 후속 “텍스트 이미지 대신 Pretendard 실제 텍스트”에 맞춰 최종 사용은 배경1+사진4개뿐이다. 제목/한영 목록/설명/목표·방식·제약/무전/START는 실제 UTextBlock·기존 DA 값이며 PNG 문장으로 미션 기획을 덮어쓰지 않았다. 카드 강조·선·화살표는 코드 도형이다. 원본/이미 임포트한 텍스트PNG16개는 삭제하지 않고 참조만 해제했다. Story 목록 선택→하단 START→기존 브리핑/Back, 훈련/레이싱 기존 동작·타이틀 아트는 유지한다. 목록 첫 버튼의 중복 포커스 후보 때문에 노브가 M4→M1로 반복되던 경로를 제거했다. 실제 렌더에서 발견한 START 축소는 Fill 슬롯·텍스트/화살표 실제 크기로 보정하고 기하 검사에 포함했다.

공식 Pretendard v1.3.9 Regular/Bold 원본 해시를 고정해 프로젝트 UFontFace/UFont로 Inline 포함했다. Root InterfaceFont/InterfaceBoldFont 연결·글꼴이 실제로 달라질 때만 갱신, 타이틀/권장 팝업 포커스 스타일이 기본 글꼴로 역덮던 경로도 보정했다. OS 글꼴 설치 불필요, OFL 고지와 NonUFS 동봉 설정 추가. 폰트 최초 commandlet 임포트는 Slate 미초기화 Assert로 실패했고 Gate 사고와 무관하다. 일반 Editor `-ExecutePythonScript`로 변경해 정상 임포트/종료했다. 가이드/도구에 해당 실행 전제를 명시했다.

### 검증 근거와 경계

| 범위 | 결과 | Saved 근거 |
|---|---|---|
| 최종 UI/기능 Build | Succeeded, 기존 deprecation/비권장 컴파일러 경고 있음 | Logs/Build_20261014_Pretendard_Final.log |
| 첫 수업 자산 설치 | 성공·0 errors/0 warnings | Automation/ObserverTutorial/setup_verified.log·setup.json |
| 표시명 전용 적용 | 성공·M3만 변경·ID/Next/Map 보존 | Automation/CodexMissionNames/20261014T012335Z/report.json |
| 승인 맵11치환 | 적용0errors/62warnings, 별도 재로드0errors/39warnings | Automation/CodexStoryActors/apply4.log·verify.log·20261014T015703Z/report.json |
| 원본 맵 복원 백업 | 두 umap bytes 보존 | Automation/CodexStoryActors/20261014T015458Z/ |
| UI/폰트 연결 | 5text-free Texture·WBP·UFont2개 검증 | Automation/SelectUI/textfree_import.log·ImportDroneSelectUI.json·font_import_editor.log·PretendardImport.json |
| 새 집중 렌더 자동화 | **18 Success / 0 warnings / 0 Fail(테스트 집계)** | Automation/CodexOct14Features/final_render.log·FinalReport/index.json |
| 실제 UI 캡처 | 1920×1080 M1~4 모두 열어 글꼴/배치/START 확인 | Automation/SelectUI/story_m1~4.png |

집중18개는 물리7·Signal3·Observer3·MissionLessonsTestMap1·StoryDisplayNames1·FlightHUD1·SelectUI2다. 초기 NullRHI16개 중 ControlLink/ObserverPIE2개는 fixture 오류로 Fail했다. ControlLink는 World BeginPlay만 호출해 동적 Delegate가 actor 초기화 가드에 막혔고 정식 BeginPlayInTestWorld로 수정했다. Observer는 재출격 후 파괴된 이전 Pawn 가드 때문에 새 Pawn 회수를 못 했고 순서를 수정했다. 실제 런타임 차단/재출격 코드를 억지로 바꾸거나 assertion을 낮추지 않았다. 최종18개는 새 RHI 프로세스에서 재실행했다. 보고서 경고0은 테스트 집계이며 엔진의 기존 startup/self-test·렌더/환경 경고까지 0이라는 뜻이 아니다. 승인 맵 경고는 Landscape collision 및 외부 MilitaryBase WireFence Construction 등 기존 환경 경고를 포함한다.

### Gate BP 저장 오류 — 재현→수정→동일 저장 경로 재검증

사용자가 팀원 PC의 자동 Gate 생성/기존 위치 수정→저장 크래시와 정확 BP_DroneTrainingGate 경로를 보고했고, 진단 뒤 수정까지 명시 승인했다. 팀원 정확한 콜스택·커밋/엔진 버전은 아직 미수신이다. 로컬에서 새 격리 맵의 BP 자동4개+독립1개 저장이 거부됐고, **Course/Spline을 모두 뺀 BP Gate1개도 동일하게 실패**했다. Native Gate1개의 첫 저장/재로드는 성공했다. 로컬은 SavePackage의 저장 거부이며 프로세스 크래시가 아니므로 팀원 동일 사고 완치로 단정하지 않는다.

명시 오류는 BP CDO의 `MID_M_BLUE_1.MID_M_BLUE_1EditorOnlyData` private 객체를 맵 Gate의 MID가 참조하는 것이었다. 기존 ApplyDroneGateItemAsset의 CDO 상태 재질/색 setter→RefreshStateMaterial→MID 생성→OverrideMaterials 직렬화 경로와 일치했다. 세그먼트 개수/자동 모드는 실패 필요조건이 아니었다. 수정은 템플릿에 정적 재질만 연결, 인스턴스 MID의 안전한 원본/Outer/native Archetype 확인·고유 이름 사용, 동적 부모만 풀고 작성된 MaterialInstanceConstant는 보존하는 것이다. 숨긴 링과 완성형 메시 모두 처리했다. 기존16개 컴포넌트를 삭제하지 않았다.

Gate.cpp·적용 도구/회귀 검사와 **Gate BP 한 개만** 수리 저장했다. Repair 도구는 원본 uasset bytes 백업 후 메시/보정 Transform/Scale/Trigger/3상태 재질/색·사운드/기존 컴포넌트 전후 동일을 검사한다. Course BP·Production 맵 저장/Compile·전체 이식/재생성은 하지 않았다.

| Gate 수리 검증 | 결과 | 근거 |
|---|---|---|
| 새 코드 Build | Succeeded18.89초(기존 경고 포함) | Saved/Logs/Build_20261014_GateSave.log |
| Gate BP targeted repair | 0errors/0warnings·기하/설정 exact 동일·MID참조17곳→0·Legacy16→16 | Saved/Automation/GateTemplateRepair/20261014T024251_430296Z/report.json·원본 BP 백업 |
| 새 프로세스 verify | 0errors/0warnings·템플릿 MID0 | Saved/Automation/GateTemplateRepair/20261014T024322_025356Z/report.json |
| 원래 실제 저장 루프 | 자동BP4+독립1 생성·Spline/Handle/위치 수정 포함 저장→unload/reload3회 성공 | Saved/Automation/GateSaveDiagnostic/20261014_114345_75775e4a/journal.json(stage COMPLETE) |
| Gate 회귀5개 | 5/5 Success, 집계4Success+1SuccessWithWarnings·Fail0 | Saved/Automation/GateTemplateRepair/regression.log·RegressionReport/index.json |

Gate5개는 TrainingGateBlueprint/Presentation/Sequence·TrainingCourse·CourseManyGates다. 마지막 정리 경고100건은 기존 이슈이며 해결된 것으로 바꾸지 않는다. 실제 저장 루프의 Spline 편집 뒤 선분 수32→33→34는 예상 수와 매회 같고 Child/live Gate4대 유지, 잔존 세그먼트 무한 증가 근거는 없었다. commandlet에서 EditorActorSubsystem 이동이 false인 경우 Actor API 대체를 journal에 기록하고 실제 위치를 검사했다. 이 검사와 실제 Editor 드래그/팀원 크래시 재시험은 구분한다.

진단 중 새로 만든 미참조 임시 umap5개와 성공 fixture1개는 소유 journal·Git 미추적·절대경로 확인과 bytes/SHA256 백업 대조 후 Saved/Automation/GateSaveDiagnostic/FixtureBackups로만 보관했다. 로그/journal/cleanup manifest·도구는 유지하며 Content Diagnostics에는 진단 맵을 남기지 않았다. 제품/팀원 자산 삭제가 아니고 복원 가능하다. 중간 Python API/진단 assertion 오류는 실제 저장 실패 재현으로 집계하지 않았다.

팀원은 **Gate C++ 수정과 수리 BP를 함께** 받고 Editor 종료 후 Build→같은 자동 생성/위치 수정/저장을 재시험한다. 자체 수정 BP는 먼저 보존·대조하며 새 코드에서 targeted Repair 도구를 사용한다. 세그먼트/Production 맵·DDC·Intermediate를 지울 이유는 없다. 실제 패드·1280 UI·Observer 조작·벽/그물/재밍 체감·제품 Story 시작/목표 연결·패키징은 후속이다. MD·Space 최종 동기화/작업 트리 점검은 아래 확인 기록을 따른다. Commit/Push는 사용자다.

최종 확인: Space 기존 진행상황 Sequence38·BP 가이드24·시험 가이드25·기획3에 오늘 증거와 미확인 경계를 반영했다. 마지막 Gate 수정5블록도 재조회하여 기대 본문 일치를 확인했다. 두 저장소 diff --check 오류 없음(일부 LF→CRLF 알림만 있음), STATUS29,777B·WORKBOARD29,770B로30KB 이하. Production Training·MilitaryCamp·Course BP에 diff 없음, Unreal Editor/빌드 프로세스0개다. Unreal67개·MD10개 상태 항목이 남은 의도된 미커밋 변경이며 Commit/Push·사용자 수동 Pass는 실행/추정하지 않았다.

## 2026-10-14 — 랜덤 레이싱 비 정면/픽셀 수정·플레이어 UI 공통 Pretendard

### 기준과 범위

사용자는 랜덤 레이싱에서 평면 옆면/픽셀처럼 보이던 대상이 비라고 명확히 했다. 도시·도로·코스 생성은 수정하지 않았다. 이전 Observer/물리·재밍·Gate 수리 등은 사용자가 커밋한 Unreal `bb6233c8`(로컬 origin/main 동일)에 포함되어 있으며, 이번에는 그 위에서 Rain/UI만 변경했다. MD 기준 `b38fc84`와 앞선 문서 변경을 보존했다. Fetch/Pull·Commit/Push·Trello/Figma/공유 권한/예약 변경은 하지 않았다. 오늘 전작업 승인 범위 내 Codex 직접 구현이며 상시 협업 역할 변경이 아니다.

### 비 원인과 수정

1. 실제 저장된 프로젝트 NS 사본3개·Sprite Renderer6개의 `VelocityAligned`가 `FacingMode=Automatic` 설정과 함께 사용됐다. 엔진 정의상 속도 정렬은 FacingMode를 무시한다. `Unaligned + FaceCameraPlane`으로 바꾸고 CPU/World Space 낙하는 유지하여 카메라를 기울여도 중력 방향까지 회전시키지 않았다.
2. 사용자 Drone.log에는 두 프로젝트 비 재질의 `Sampler type is Masks, should be Linear Color` 및 PCD3D_SM6 컴파일 실패→Default Material 대체가 있었다. 원본 OilRig T_rain_Mask의 실제 인코딩에 맞춰 **프로젝트 재질2개만 Linear Color 샘플러**로 수리했다. 원본 텍스처는 수정하지 않았다.
3. 위 두 수정 후에도 실제 캡처에는 짧은 흰 사각형이 남았다. 원본 마스크를 읽기 전용 PNG로 내보내 확인한 결과 4×512 RGBA에서 R은 짧은 밝은 머리, A가 긴 투명 꼬리였다. 현재 사용 재질 M_DroneRainSprite의 투명도를 **A 채널**로 연결하고 좌우 폭·상하 끝을 부드럽게 감쇠했다. `RainStreakHalfWidth=0.10`; 기존 ParticleColor/밝기·Opacity 파라미터·근거리 깊이 감쇠는 보존했다. 최종 캡처를 직접 열어 가는 빗줄기로 바뀐 것을 확인했다.

낮음/중간/높음의 기존 입자 수·밀도·Bounds·낙하 속도·커버 범위·천장 검사·젖음/빗소리·기상 프로필은 바꾸지 않았다. 비 켜짐=카메라 주변 Niagara1개·legacy ISM0, 끔=0개 유지. 전체 성능/FPS 개선율은 이번 측정하지 않았다.

`ConfigureDroneRainPresentation.py`는 기본 읽기 전용 inventory이며 자체 보고서에도 화면 검증이 아니라고 명시한다. 명시 Apply 때만 정확히 프로젝트 NS3개/재질2개를 허용하고 변경 전 bytes/SHA256을 백업한다. C++ DroneRainAssetLibrary도 같은 패키지 허용 목록을 사용한다. `DroneRainMaterialProfile.py`는 기존 Opacity 하위 그래프를 보존하는 멱등 처리·기존 마커 업그레이드와 A 연결을 공유한다. 이후 재생성 도구도 같은 규칙을 따르도록 수정했지만 광범위 맵/에셋 생성 도구는 실행하지 않았다.

### Pretendard·선택 이름

Native 기본 글꼴44곳을 DroneUIFont로 통일하고 프로젝트 DroneUserWidget 공통 기반에서 Native/Designer UI 10종의 일반 텍스트·입력칸·Combo/생성 행·Rich 기본 스타일을 처리했다. 기존 크기/굵기/자간/외곽선/색·레이아웃·아트는 유지한다. Initialize/PreConstruct/Construct/Sync 때 적용하며 Tick마다 전체 트리를 순회하지 않는다. `bUnifyDesignerFonts`, `FontOptOutWidgetNames`, 동적 추가 후 `RefreshProjectFonts` 예외를 제공한다. 기존 Regular/Bold UFont 임베드·OFL 동봉을 유지하고 폰트 폴더 AlwaysCook을 추가했다. 글꼴 자산/WBP 대량 재저장은 하지 않았다.

아이콘·명시 opt-out·Vendor/Legacy·엔진 Editor/디버그 글꼴과 기본 숨김인 월드 TextRender 라벨은 범위 밖이다. Rich 태그별 스타일 테이블을 강제로 바꾸는 작업도 아니다. 기존 Story 배경/사진·로고 아트는 보존한다.

선택 목록 두 경로는 표시 전용 formatter로 `랜덤 도시 레이싱(시험)` 같은 **끝 괄호 부연만 숨긴다**. 중간 괄호/불완전 괄호·DA 원문·ID·상세/툴팁·맵/저장키·진행 순서는 바꾸지 않는다. 중첩/전각/복수 끝 괄호 등13개 사례를 회귀 검사했다.

### 검증과 재현 이력

검증 환경: UE5.8.2, MSVC14.51.36257, DroneEditor Win64 Development, 실제 D3D12_SM6 RHI. 로그/보고서는 아래 `D:\JGY\project\drone\Saved` 기준이다.

| 검사 | 실제 결과 | 근거 |
|---|---|---|
| 최종 Build | Succeeded, 12.20초·기존 컴파일러/엔진 경고 유지 | Logs/Build_20261014_RainFont_Final6.log |
| 실제 RHI 집중 자동화 | **14 Success / 0 SuccessWithWarnings / 0 Fail / 0 NotRun**, 39.555초 | Automation/RainCameraFacing/SoftAlphaReport/index.json·soft_alpha_render.log |
| 비 화면·실제 컴포넌트 | 3품질×정면/90°/75°상향 + Off=10장, 실제1280×720. 켜짐 Niagara1개·ISM0, Off0 | Automation/RainCameraPresentation/soft_alpha/Capture_BEB211AC46588D5AC65D0380FA51364E/ |
| UI 렌더·글꼴 | Story4장·설정 화면 직접 확인, 10 native+기존WBP2개·Designer 크기37/자간143/외곽선2/색 유지 회귀 | Automation/SelectUI/story_m1~4.png·Automation/Settings/settings_main.png·settings_open.png |
| UI 소스 기본 글꼴 감사 | 위반0 | Tools/Validation/AuditDroneUIFontSources.py |
| 마지막 대상 적용 | Sprite 알파/soft profile 변경, 기타 허용 대상 기존 수리 유지·원본/Rain BP SHA 보존 | Automation/RainCameraFacing/20261014T035631_137046Z/report.json |

14개는 RainCameraPresentation/Follow/QualityLevels/PerformanceBudget, UI FontContract/PlayerWidgetFontsPIE/SelectionDisplayLabelContract/SelectUILayoutContract/SelectUIPresentationPIE/FlightHUDTelemetryBinding/FlightHUDBlueprintAsset, Flow.SettingsContract, Diagnostics Weather.RainCameraCapture/UI.SettingsCapture다. 앞선18개/Gate5개와 별도 실행이며 전체 Drone.* 또는 실제 플레이 Pass로 합산하지 않는다. 테스트 경고0은 엔진 startup/self-test·환경 경고까지 0이라는 뜻이 아니다.

RED 단계에서 실제 정렬12·샘플러6 문제를 재현했다(BeforeFinalReport). 초기 NullRHI GetUsedTextures와 BeginPlay/플레이어 등록 fixture는 실제 렌더/정식 GameWorld로 바로잡았다. 첫 수리 배치의12성공/2실패 중 Rich 기본 스타일의 초기화 전 조회는 새 UI helper 결함으로 수정했다. 이어13성공/1실패는 화면 캡처 fixture가 OS 창 테두리 차이(클라이언트1280×722/PNG1280×720)를 동일값으로 가정한 문제였다. 첫 실제 PNG가 최소960×540이고 이후9장이 정확히 같은 크기여야 한다는 조건으로 바꿨으며 사용자 비/입력 검사를 약화하지 않았다. 마지막 새 프로세스에서14개 전부 재실행했다. 정적 검사 통과만으로 픽셀 해결을 판정하지 않고 첫 수리 캡처의 사각형을 발견해 A/soft profile까지 후속 수정했다. 진단 조명 변경은 캡처 fixture만이며 제품 맵 조명을 수정하지 않았다. 따라서 전후 이미지를 동일 조명 성능/측광 비교로 해석하지 않는다.

처음 수리의 NS3개/재질2개 원본 bytes 백업은 Automation/RainCameraFacing/20261014T033748_069008Z/, 이후 soft/alpha 변경 백업은 035349_590873Z·035631_137046Z 폴더에 있다. 원본 마스크 검사 PNG는 MaskInspection/T_rain_Mask.png에만 보존했다. Content diff는 기존 프로젝트 Weather 자산5개만이며 맵·Gate/Rain BP·ThirdParty 원본은 미변경이다.

### 남은 수동 확인·인계

랜덤 도시 레이싱의 비 날씨에서 낮음/중간/높음→좌우90°/상향/이동, 실내 차단/실외 복귀, 비 품질 Off를 확인한다. 선택 목록 끝 괄호 숨김·HUD/설정/결과/로딩 Pretendard와 실제 패드·1280/1920 가독성을 확인한다. 실제 랜덤 레이싱 플레이·사용자 화면 체감·전체 회귀/패키징·FPS 측정은 미완료다. Gate 팀원 동일 저장 재시험·기존 Observer/물리/재밍 실기 대기는 유지한다.

MD STATUS/WORKBOARD/CONTEXT·UI/비 가이드를 갱신했다. Space 기존 진행39·BP25·시험26에8블록을 반영하고 모두 재조회하여 기대 본문 일치를 확인했다. 기획3·지침9·루트는 미변경. 두 저장소 diff --check 오류 없음(일부 CRLF 알림), STATUS29,829B·WORKBOARD29,798B로30KB 이하이며 Unreal Editor/Build 프로세스0개다. Unreal46개·MD11개 상태 항목은 의도된 미커밋 변경이며 Commit/Push는 사용자다.

## 2026-10-14 — Island Gate 크기·랜덤 Gate 방향·도시 외형과 Rain 볼륨 후속

### 기준·승인과 조사

같은 D PC, Unreal HEAD/로컬 origin/main bb6233c8·MD b38fc84와 앞선 Rain/UI·문서 변경을 보존했다. 사용자가 Island의 좁은 Gate, 랜덤 레이싱의 돌아간 Gate·화면 한쪽 비, 콘크리트/컨테이너/도로/지붕 위 건물 중복을 지적해 해당 수정까지 승인했다. Editor PID1468이 남아 있던 첫 확인 뒤 사용자의 본창 종료 답변과 실제 프로세스0을 확인하고 Build했다. 오늘 전작업 승인에 따른 Codex 직접 구현이며 상시 역할 분담 변경은 아니다. Fetch/Pull·Commit/Push·Trello/Figma/권한·예약 변경은 하지 않았다.

고립된 비 fixture의 앞선14/14 통과는 실제 랜덤 레이싱 전체 화면 분포 검증이 아니었다. 이번에는 실제 저장 맵/생성기·사용자 시드194849를 별도 프로세스/PIE에서 읽고 재현했다. 원본 팩·Island·Production Training은 저장하지 않고 실제 테스트 복제본으로만 생성/캡처했다.

### Gate 원인과 수정

- Island 읽기 전용 조사: 전체464개 중 live BP112개가 모두 좁았고 나머지352개는 숨김/Trigger 비활성인 옛 Native였다. 이 잔존물을 삭제하지 않았다. Course AutomaticGateScale=(1,2,2), RaceRing 작성 Yaw90°·Scale1.75의 조합에서 visible Y/Z=197.4/394.8cm, Trigger span350/350cm였다. 메모리에서만 Actor X scale1→2→1 A/B로 폭394.8→197.4 재현, 디스크 bytes는 불변이었다.
- 작성 GateAssetLocalTransform은 그대로 보존하고 Native visual의 파생 relative scale만 회전축/부모 비균등 scale에 맞춰 보상했다. Root transform 갱신·등록/Construction/BeginPlay·ChildActor 후배치에서 적용하며 Tick은 추가하지 않았다. Trigger/Actor transform·3색/재질·16개 기존 컴포넌트·MID 저장 수리는 보존한다. 90°/180° 축 정렬·signed scale 회귀를 추가했다. 임의 각도의 shear는 FTransform으로 완전 표현할 수 없으므로 이 범위는 축 길이 정합으로 제한한다.
- 실제 seed194849의 두 CurveClamped knot에서 derivative가 정확히0이어서 spline quat이 Identity로 돌아갔다. RaceRing의 필수 작성 Yaw90°가 원인은 아니었다. GetSegmentDistance의 실제 거리로 재측정하고 직선/모서리/폐곡선 seam 3개 RED를 만들었다. 유효 접선/roll/회전 offset은 그대로, 0/비정상 접선에서만 유한 차분·loop wrap/open clamp·outgoing fallback을 사용한다.
- 최종 코드로 Island를 다시 읽은 report.json은 NO_SMALL_FRAME_REPRO, live112개 좁음0, before/after SHA 동일·saved_packages0이다. 맵 재생성/저장 없이 적용된다. 도구/보고서: Saved/Automation/IslandGateSize/InspectIslandGateSize.py·report.json·engine_probe.log·engine_after_fix.log·procedural_report.json·procedural_tangent.log.
- 사용자 재질 /Game/Material/m_green의 Nanite 누락은 별도 byte 백업 후 used_with_nanite 플래그만 보강했다. 색/파라미터/그래프 변경 호출은 없다. Final2 RHI에서 이 재질의 missing usage 경고는 없으며 세 상태색/사용자 게임 체감은 별도 수동 대기다.

### 도시 생성·재질

완성 SourceBlueprint/지붕 포함 건물은 MaxStackLevels 값과 관계없이 한 구조물만 배치한다. 명시 bStackableModule인 독립 SingleMesh만 반복하고 같은 XY/Yaw·실제 Z bounds/바닥 pivot으로 지지한다. 층마다180° 뒤집던 처리와 완성 지붕 위에 다시 얹는 구조를 없앴다. 원본 BP 내부의 진짜 층은 보존하며 전역 MaxStack=1 우회가 아니다. GetBuildingSpecs 재생성 때 캐시도 갱신한다.

깨끗한 닫힌 /Game/FC_MilitaryCamp/Models/MilitaryModels/SM_Container_01만 적층 모듈로 추가했다(bounds1356.978×389.051×384cm·bottom0). 변형/문 돌출 bounds의02/03과 완성 컨테이너 건물 BP는 이를 대체하지 않는다. SingleMesh의 MaterialOverrides는 슬롯 인덱스별 적용하고 비거나 null이면 원본 슬롯으로 fallback한다. 원본 mesh slot은 수정하지 않는다.

차선은 도로와 분리한 비충돌 HISM이며 중앙 점선·가장자리 실선을 생성하고 교차로를 피한다. BP에서 폭/점선 길이·간격/가장자리 inset·On/Off를 조정한다. 원본 M_Concrete1은 없는 Substance parent, 기존 도로는 RVT/타이어 자국, 바닥은 금속 격자였다. 프로젝트 소유 standalone 콘크리트/아스팔트/포장/지면/차선 재질을 만들고 콘크리트는 world-normal triplanar로 늘어짐을 줄였다. MI_DroneCity_Asphalt의 TextureWorldSizeCm=12cm로 미세 입자 크기를 조정한다.

실제 RHI 첫 캡처에서 FC 원본 Container MI가 InstancedStaticMeshes usage 부족으로 DefaultMaterial로 바뀌는 문제가 추가로 드러났다. 원본을 수정하는 대신 MIC3개와 M_Master_Props parent를 /Game/Drone/Procedural/Materials/CityContainer_*로 복제하고 소유 parent에만 HISM 지원을 넣었다. 새 프로세스에서3개 MIC의 scalar/vector/texture arrays 및 노출 static switch 값이 원본과 같고 복제 parent HISM=true임을 확인했다(rain_palette_inventory.json). static_parameters 직접 조회는 API에 없어 처음에는 미확인으로 기록했고, 설치 엔진 MaterialEditingLibrary의 static-switch 조회로 보완했다.

ConfigureDroneCityAppearance.py는 기본 read-only audit, 명시 DRONE_CITY_APPEARANCE_APPLY=1에서만 소유 재질·기존 Generator BP·기존 TestMap 생성기1개를 수정한다. m_green은 위 플래그 예외만 허용한다. 원본 팩/Island/Production은 저장하지 않으며 기존 BP·맵·재질은 bytes/SHA 백업한다. 재실행은 기존 소유 재질의 아티스트 그래프를 덮지 않고 class/parent/HISM 상태 불일치 시 중단한다. 승인 Container01을 재실행 때 일반 건물로 되돌리지 않으며 Type51개를 유지한다. 별도 도시를 생성해 맵에 저장하는 도구가 아니다.

적용: Saved/Automation/CityAppearance/20261014T054933_738398Z/report.json(기본5재질/BP/TestMap), 20261014T060813_156373Z/report.json(Asphalt MIC·컨테이너 parent/MIC3·m_green flag·BP/TestMap). 기존 타깃 백업은 같은 폴더다. 초기 도구의 없는 Material.desc와 UV 입력명 Coordinates 실패는 metadata 태그/설치 엔진 UVs 조회로 수정했고 실패본은 새 재질 저장0이었다(city_apply.log·city_apply2.log). 수정 후 city_apply3/4는 exit0·Python script success와 실제 saved 목록을 확인했다.

### Rain 후속·중간 검증(최종 결과는 아래 후속 기록)

Sprite 정면 정렬만으로는 근거리 생성 볼륨이 카메라 시야를 따라가지 않았다. 프로젝트 사본 NS3개만 camera-local로 바꾸고 전체 카메라 pose를 PostUpdateWork에 따른다. SceneRoot/천장 Trace는 월드 위쪽을 유지한다. 원본 OilRig World Space와 mask/낙하/밀도·품질/젖음·오디오는 보존한다. LocalSpace bool만 변경하지 않고 versioned emitter PostEditChange와 Niagara VM compile/Ready 완료 후 저장하도록 보강했다. 명시 품질Off·맑음·SetRainEnabled(false)는 DeactivateImmediate, 실내 노출 감소는 기존 자연 소멸 경로로 구분한다.

Niagara Ready는 NullRHI 및 -AllowCommandletRendering 없는 commandlet에서 성립하지 않는다. 두 초기 시도는 NS 저장0으로 차단됐다. -AllowCommandletRendering -RenderOffscreen으로 실행한 rain_apply_render_allowed.log와 RainCameraFacing/20261014T054838_105151Z/report.json은 compiled_ready·NS3개 저장 성공, 원본/Rain BP SHA 보존이다.

최초 actual-city 캡처는 첫 viewport가961×335였고 이후1274×716이었다. 기준을 낮추지 않고 실제 client viewport >=960×540·6프레임/0.5초 안정 후 첫 shot을 시작하게 고쳤다. Final2 9장 모두1274×716이며 root가 도로/컨테이너/콘크리트 골조/완성 창고 PNG를 직접 열었다. 기본 재질 체크무늬와 지붕 위 완성 건물 중복이 사라진 범위만 확인했고 모든 시드/도시 동선 최종 완성을 판정하지 않았다.

Build/테스트는 UE5.8.2·MSVC14.51.36257·D3D12_SM6이다. Final Build22.03초 및 Final2 Build35.60초 성공. 첫 FinalReport는18 Success/1 Fail, Final2Report는 신규MaterialOverrides 포함19 Success/1 Fail(20개)이다. 단위/정적 회귀가 통과해도 actual-city 비는 여전히 화면 좌측에 쏠려 우측 화면1/3 두 시점 검사가 실패했다. 이 결과를 숨기거나 assertion을 완화하지 않았다. Rain 위치보정만으로 부족해 by-emitter 실제 position/velocity/age/lifetime·카메라 projection을 JSON으로 추가 기록했다(ParticleProbe Build14.15초 성공). source NS는 ObjectExporterT3D로 읽기만 내보냈으며 저장하지 않았다.

현재 캡처: Saved/Automation/CityAppearance/S194849/gate_rain_city_fix2/Capture_98CD6C3742A6BE9D21D7F6B9113ACFA6/. 실제 좌표 JSON/PNG: particle_probe/Capture_5BC80B324206CAAD53F1659FD9324868/. 중간 실패를 전체 완료/사용자 체감 Pass로 바꾸지 않는다. 최종 추가 수정/새 프로세스 검증 결과는 아래에 이어 기록한다.

## 2026-10-14 — 팀원 커밋3cb9c184 수신·로컬 작업 보존

사용자 Pull 요청·Editor 종료 확인 후 Drone origin만 Fetch, bb6233c8→3cb9c184를 FF 수신했다(1커밋·31경로, 0/0). 수정/삭제51개·미추적50개를 먼저 Saved/Backups/GitPull_20261014_164500에 백업했다(101레코드·실파일98개·710,189,004B, SHA 확인·manifest.json). 실제 겹침6개/새파일23개는 원격과 SHA 또는 삭제 상태가 같아 선택 충돌이 없었다. Gate/Course BP2개는 clean이던 이전 파일에서 원격 새 버전으로 정상 수신했다. MilitaryBase/Island·차량BP, Tutorial8맵·Driving/Car/LOS·RC Controller/Traffic Cone을 받았다. 옛 Training1/2/training1_1 삭제는 이미 로컬에서도 삭제 상태였고 커밋으로 확정됐으며 이전 Git 커밋에서 회복 가능하다.

임시 Stash51bd8d3a로 전체 로컬 변경을 보관한 뒤 수신하고, incoming 밖 tracked45개/미추적27개 총72개를 백업의 원래 바이트로 복원·SHA 검증했다. 이전 Gate/Rain/City/UI 코드/자산63개 상태 항목은 그대로 보존했다. 수신31경로의 LFS 실제 데이터 SHA/삭제 상태도 전부 확인했다. 새 Stash만 정확한SHA를 대조해 제거했고 현재Stash0·unmerged0·staged0·main/origin0/0이다. 사용자 데이터는 백업+manifest에 남아 있으며 Source/맵 임의 폐기나 reset--hard는 사용하지 않았다. 초기 백업/manifest의 Git CRLF 경고가 stdout JSON과 섞이는 도구 처리 문제는 경고와 JSON을 분리해 보완했으며 작업 파일 손실은 없다.

MD는 사용자 HEAD5ab41d6(로컬origin b38fc84보다1앞)·기존 편집을 보존하고 Fetch/Pull하지 않았다. STATUS/WORKBOARD의 현재커밋과 검증 경계만 갱신한다. 이번 수신 후 Build/PIE/Unreal 맵 저장은 하지 않았다. 직전 실제 Saved/Automation/GateRainCity/Final3Report/index.json의21/21·Build26.40초·도시9장/Rain10장은 bb6233c8 위 로컬 수정 검증이며 새 Gate/Course BP·Island 저장본 Pass가 아니다. 전체마지막 결과 전문이 현재 WORKLOG에 없더라도 실제 보고서는 Saved에 유지된다. Commit/Push·Trello/Figma·공유/예약·모델 설정 변경은 없다.

Space 기존 진행상황41·시험가이드28의2블록에 새 수신/로컬 보존과 이전21검증 경계를 반영하고 동일본문 재조회로 확인했다. BP/기획/지침/루트·새Page/권한은 미변경. 최종 main/origin0/0·stash/unmerged/staged0·Unreal63개 미커밋 유지, MD diff --check는 원문CRLF 허용 설정으로0이며 STATUS27,076B·WORKBOARD29,644B다. byte 백업/manifest/result는 위 Saved 폴더에 보존했다. 스태시 제거는 복원·수신 SHA 검증 뒤 수행했으며 사용자 작업을 폐기한 것이 아니다.

## 2026-10-16 — 커밋 51bf2629·95beefa 확인, 팀원 6c07afa5 수신

사실 확인은 Claude(D PC, Git log/status·파일 크기·세션 기록), 문서·Space 반영은 Codex이며, Codex도 두 저장소의 HEAD·origin/main 일치와 작업 시작 Clean을 읽기 전용 Git으로 대조했다: Unreal `6c07afa5`, MD `95beefa`(이번 문서 반영분 제외).
10/14 16:56 사용자 커밋 `51bf2629`(1014 픽스, 72파일·3,482+/151-)로 Gate/Rain/City/UI·DefaultGame.ini 로컬 작업이 커밋·푸시됐고 MD도 `95beefa`(1014, STATUS/WORKBOARD/WORKLOG)로 커밋·푸시됐으며, Final3 Build·RHI21 Success는 같은 작업의 당시 근거이고 커밋 후 재검증은 없었다.
10/15 14:16 Yook34의 `6c07afa5`(261015, Content142파일·420+/12-) 수신은 Battlefield·MilitaryBase·TUT_Delivary·TUT_FreeGate·TUT_UGV_Turret 맵5개 및 M_net 수정과 Fab `Content/Fab/Military_Supplies__30+_/` 보급품136파일 추가이며, Claude가 LFS 본문 크기 Battlefield73,711,089B·TUT_Delivary35,273,709B·VV_MedicalCrates_M73,107B를 확인했다(포인터 아님).
Content만 바뀐 수신 뒤 Build·PIE·자동화는 미실행(최신 Editor 로그10/14 16:40·자동화 폴더10/14 15:28 RainCameraPresentation)이고 이번 세션의 신규 구현됨·자동 검증됨은 없음, 미구현은 해당 없음이며, 맵5개·M_net의 Editor 열기·PIE는 수동 확인 대기이고 실제 변경 내용·의도·검증 책임, Fab 의료 상자의 드랍 화물 사용 여부, 전체 회귀 시점은 현재 미정이다.
STATUS 지정 Git 구간·WORKBOARD 갱신일/SYNC-WORKPC-01만 갱신하고 기존 기능 판정·과거 기록은 보존했으며, Drone Space 기존 진행상황 페이지 Git/수신 관련2블록의 편집2건(sequence42) 적용 및 재조회 일치를 확인했고 새 파일·Build·PIE·맵 저장·Commit/Push는 없다.

## 2026-10-16 — D PC 저장공간 점검·중복 백업 정리

사용자의 "용량 확인·쓸모없는 과거 백업 정리" 및 "백업의 백업이면 정리" 요청으로 C/D 파일 크기와 백업 사본을 대조했다. 삭제한 파일 길이 합계는 49,241,318,304B(45.860GiB)이며, 보존 사본의 존재·삭제 대상 부재를 다시 확인했다. 폴더 크기는 논리 크기 기준이고 링크는 따라가지 않았으며 C 접근 오류286건·D3건으로 보호 영역 전체 크기를 확정한 측정은 아니다.

| 정리 대상 | 확인·보존 근거 | 삭제량 |
|---|---|---|
| `D:\JGY\00\FRACTURED.zip` 중복1개 | `D:\JGY\programing\FRACTURED.zip`와 SHA-256 동일(`B79EFC88376CB0213FED5F4CEF3C152EE920E02CBC5B9A0B48DABA27B65BBFF9`), programing 사본 유지 | 11,219,540,912B / 10.449GiB |
| `D:\JGY\programing\0414\backup\0608`, `0609` 안의 Windows 실행 묶음7개 / 457파일 | 각 상대경로·개수·크기·모든 파일 SHA-256 동일 확인. `0414\Windows`와 `0414\Build\001/002/003\Windows` 원본4개 유지. 검증된 중복 파일만 개별 삭제 후 빈 폴더 제거 | 22,686,439,575B / 21.128GiB |
| 0418일·0501 과거 백업의 PCH2개와 0418일 `.vs` DB/WAL3개 | 재생성 가능한 컴파일·검색 캐시만 개별 삭제. Source/Config/Content/uproject와 나머지 백업 보존 | 6,444,540,648B / 6.002GiB |
| C 사용자 Temp의 `_CL_*` 1,155파일 | 2026-09-16 이전 수정, 실제 최신8/26. 루트 직속·일반 파일·크기/수정일 재검증 후 개별 삭제 | 8,890,797,169B / 8.280GiB |

측정 여유 공간은 시작 C10.85GiB·D786.07GiB → 종료 C20.59GiB·D824.23GiB이며 실행 중 다른 프로세스의 사용량 변동도 포함한다. C의 큰 사용처는 Epic Games 설치73.23GiB, Twinmotion 로컬 라이브러리49.36GiB, Unreal 공통 캐시26.73GiB, 시스템 최대절전 파일25.49GiB다. Temp45.72GiB는 정리 전 스캔 값(이후 `_CL_*` 8.28GiB 삭제)이며 Adobe Temp19.44GiB에는 당일 갱신 파일이 있다. D의 `programing`546.05GiB·과거 backup129.53GiB도 정리 전 값이다. 설치 프로그램·라이브러리·현재 Zen 캐시·최대절전 설정·휴지통·고유 버전의 소스/에셋은 유지했다.

폴더 전체 재귀 삭제는 자동 승인 정책에서 차단됐고 적용0이었다. 범위를 검증된 중복 파일과 명시한 재생성 캐시 파일로 줄여 개별 삭제했고 위 수치를 검증했다. 프로젝트 Unreal 소스·Content·Git/LFS·현재 Saved/Backups·실행 검증 보고서는 정리하지 않았으며 새 Build/PIE·기능/수동 검증·Commit/Push·Trello 수정·공유/예약 변경은 없다. 기존 미커밋 작업과 과거 기록을 보존했다.

증거는 현재 PC `C:\Users\Metacon_41\Documents\ChatGPT\드론\output\storage-audit-20261016\`의 cleanup-summary.json, duplicate-hashes.json, build-copy-comparisons.json, duplicate-build-cleanup-result.json, compiler-temp-cleanup-result.json, old-backup-cache-files.json이다. 원시 전체 스캔은 로컬 Temp/codex-storage-audit-20261016에 있으며 개인 파일이나 대용량 데이터를 Space에 업로드하지 않는다. Drone Space 기존 진행 페이지에 같은 정리 요약을 반영하며 상세 MD는 로컬 미커밋이다.

Space 반영 확인: 기존 진행상황 페이지에 정리 요약1블록을 추가(sequence43)했고 같은 블록 재조회에서 본문 전체 일치를 확인했다. 다른 기능 판정·과거 기록은 수정하지 않았다.

## 2026-10-16 — 오후 UI 전면 개편·WBP 전환·UGV 무장

작업·실행 담당 Claude(일부 구현 Claude 하위 에이전트), 교차 리뷰 Codex 2회, 문서·Space Codex. Asia/Seoul 2026-10-16 D PC, Unreal D:\JGY\project\drone·md D:\JGY\project\md. 오전 미커밋 STATUS/WORKBOARD/WORKLOG와 기존 저장공간 점검 기록을 보존해 끝에 추가했다. 이 절은 오후 세션 변경·검증 상세 정본이며 STATUS는 현재 요약, WORKBOARD는 현재 카드/Next다.

Codex 읽기 전용 Git 조회: Unreal HEAD 6c07afa5·로컬 origin/main 52594d0f(팀원 커밋 미수신), 미커밋 102개(인계 약100개와 부합). Source/Tools/Config diff --stat는 추적49파일·3,838추가/655삭제이며 미추적 자산까지 포함한 수치가 아니다. md HEAD95beefa, 시작 미커밋3개. Git 소유권 경고는 명령 한정 safe.directory로 읽기 조회했고 전역 설정을 쓰지 않았다. Codex는 Unreal 파일 수정·Build·PIE·자동화·맵/에디터 도구 실행·Commit/Push·Trello/Figma/권한/예약 변경을 하지 않았다.

아래 변경 사실·사용자 확정 범위는 Claude 지시서 인계다. Codex가 이번 문서 작업에서 코드를 재구현하거나 모든 자산/캡처를 독립 검증했다는 뜻이 아니다. 검증 표는 인계 원문을 보존하며, 직접 읽은 원시 보고서와의 차이는 바로 다음 정정 절을 우선한다.
## 변경 사실
1. WBP 전환·정리: 코드로만 그리던 위젯을 WBP로 내보내는 Editor 도구(`Source/Drone/UI/Tools/DroneWidgetBlueprintExport`, 자동화 `Drone.Tools.ExportWidgetBlueprints`)와 확인 테스트(`Drone.UI.NativeWidgetBlueprintAssets`). 모든 WBP를 `/Game/Drone/UI/WBP/{FrontEnd,Mission,HUD}`로 이동(AssetTools, `Tools/AssetMigration/OrganizeDroneWidgetBlueprints.py`). 이동 때 참조 고침 누락 3건(FrontEnd→설정·시드, FlightHUD→입력 표시, FrontEndRoot TitleMenuClass)을 `FixMovedWidgetReferences.py`·`WireDroneWidgetBlueprints.py`로 복구.
   - WBP 목록: FrontEnd(WBP_DroneFrontEndRoot, WBP_DroneFrontEnd, WBP_DroneFiveItemMenu, WBP_DroneSettings, WBP_DroneSeedInput, WBP_DroneControlsGuide), Mission(WBP_DroneSelection, WBP_DroneMissionObjective, WBP_DroneMissionResult, WBP_DroneMissionPause, WBP_DroneProceduralLoading, WBP_DroneStartCountdown, WBP_DroneMissionStartPrompt), HUD(WBP_DroneFlightHUD(구 프로토타입), WBP_DroneControlInputDisplay).
   - **아직 코드만**: 미션 맵 비행 HUD 본체(HUD Kit: 나침반·고도·속도·상태·UGV 조준선/무장), 로비 미션 카드 버튼, 로비 배치 좌표(실행 시 코드가 다시 잡음). 다음 작업 후보: HUD Kit WBP화.
2. 프론트엔드: 레이싱·훈련 로비를 캠페인과 같은 MISSION BRIEFING 형식(번호 목록·가운데 사진·오른쪽 정보 3칸, Select_UI 배경)으로 통일. 카드 클릭은 선택만, START로 확정(세 분류 공통). 카드 제목 한 줄 고정(완료 표시는 부제로). 정보 칸 높이 글에 맞게.
   - 브리핑 화면(작전 지역으로 이동) → 시안 8.webp 형식: TRAINING/RACING/MISSION BRIEFING 제목, 사진·정보 3칸, 오른쪽 CONTROLS 3탭(게임패드/키보드·마우스/드론 조종기, 장치 그림·번호·3열 범례, LB/RB 전환), START.
   - 모든 시작 버튼 글자 "START", 화살표는 받은 이미지(T_UI_StartChevrons).
3. 기체 선택 화면: 시안 6.webp 형식(큰 미리보기, DRONE 상세·능력치, 작은 ‹ 조작 모드 › 버튼, SELECTED 카드, START). 기체 이미지 4종(Figma 렌더) 연결. 특징·안내 줄 제거, 설명/능력치 칸 높이 고정.
4. 훈련 시작 안내창: 훈련 출격 직후 게임 멈춤 + 미션 이름·현재 목표·진행·역할 조작 안내·전체 목표 + [시작](A/Enter). 기본 훈련만 켬(레이싱·스토리 BP 옵션). 테스트 `Drone.Flow.MissionStartPromptPIE`.
5. 비행 HUD(시안 5.webp, 코드): 왼쪽 위 미션 패널(MISSION NN · 이름, 목표, 역할 안내, 진행 막대), 맨 위 나침반(가로 눈금 + "355°" 상자, 매 프레임 부드럽게), 타이머(남은 시간·TIME LIMIT), 오른쪽 위 기체 상태(내구도·배터리·신호·바람·조작 모드), 왼쪽 속도 상자(세로 눈금 제거), 오른쪽 고도 사다리 + 뾰족한 지시 상자 + VS(수직 속도). UGV만 조준선·무장 패널(MG 탄창·GL 잔탄·재장전). 해상도와 무관하게 맞게 그리기 좌표 수정.
6. UGV 무장: 기관총 누르고 있으면 연사, 탄창 200·재장전 2초(빈 탄창 자동, R/□ 수동), 유탄 6발 제한(연사·재장전 없음). UGV일 때만 L2 기관총·R2 유탄 IMC(`IMC_DroneGroundWeapons`, `IA_DroneGround_Reload`). Space/Ctrl은 UGV에서 포탑 위아래 조준. 테스트 `Drone.Weapons.GroundUGV.Ammo`.
7. 설정 체크박스 버그 수정: 수직 동기화·조종 입력 표시 체크박스가 켜짐/꺼짐 모두 검은 네모로 보이던 문제(체크 스타일 전경색 검정) → 흰색 고정. 타이틀·일시정지 양쪽 마우스·키보드 재현 테스트(`Drone.UI.SettingsCheckboxClickPIE`, `Drone.UI.PauseSettingsCheckboxClickPIE`, 캡처 `Saved/Automation/SettingsCheckbox/`). 설정 콤보 항목이 WBP 경로에서 비던 문제도 수정.
8. 드랍 목표: `BP_RoleTest_PayloadTarget` 외형 SM_Pallet(Battlefield 자산, 수정 안 함), 메시 크기에 맞춘 충돌 상자 자동(LandingCollision), Target Visual Mesh를 바꾸면 바로 적용.
9. 문구: 기체·미션의 "(그레이박스)·시험" 표기 제거, 역할별 기체 설명, 레이싱 기체 이름 "스카이드론"(외형 자산은 팀원 미푸시로 미연결), 기획서 기준 미션·훈련 문구(오전).
10. Codex 교차 리뷰 2회 지적 8건 모두 Claude가 코드 대조 후 수정(콤보 항목, 시드 칸, 로딩 단계 줄, 첫 수업 완료 색, 기체 카드 바인딩, 정리 스크립트 API, 시작 안내창 버튼 누락 시 멈춤, 입력 자산 쿠킹 → DefaultGame.ini DirectoriesToAlwaysCook 추가).

## 검증 출처
| 검사 | 조건 | 결과 | 보고서·로그 경로 |
|---|---|---|---|
| Build | DroneEditor Development | Succeeded(마지막 16:5x) | `Saved/Automation/ClaudeCheckbox/` |
| UI·Flow 등 회귀 | RenderOffScreen 1920×1080 | 80건 중 73 → 재실행 후 실패 1(테스트 하네스 문제) | `Saved/Automation/ClaudeUIOverhaul3`, `ClaudeUIOverhaul4` |
| 체크박스 재현 | RenderOffScreen | 2/2 Success + 캡처 | `Saved/Automation/ClaudeCheckbox/report2` |
| HUD 캡처 | 1920·1600·1280 | 정상 배치 | `Saved/Automation/HUD`, `ClaudeHUDRes` |
| 드랍·능력 | NullRHI | 3/3 | `Saved/Automation/ClaudeHUD5/report3` |

- 구현됨: 위 1~10
- 자동 검증됨: 위 표
- 수동 확인 대기: 새 로비·브리핑·기체 선택·조작 안내 실제 조작(패드·마우스), UGV 연사·재장전·유탄·Space/Ctrl 조준, 훈련 시작 안내창, 체크박스 실사용, 팔레트 투하 착지, HUD 실제 해상도별 배치
- 미구현/알려진 문제: HUD Kit WBP화 미착수, `Drone.UI.FlightHUDKitLayout` 테스트는 테스트 World에서 위젯 초기화가 돌지 않아 실패(제품 HUD는 PIE 캡처로 정상, 2회 수정 후 중단), 스카이드론 외형 미연결, 패드 포커스 PIE 4건은 미렌더 실행 시 알려진 실패(UI-FOCUS-RACE-01, 재실행 통과)

### Codex 원시 보고서 대조·인계 수치 정정/확인 대기

- ClaudeUIOverhaul3/verify_report/index.json: 성공73·경고 동반 성공2·실패5, 합계80. 실패는 Drone.Flow.GamepadMissionFlowPIE, Drone.Flow.GamepadNavigationPIE, Drone.Flow.KeyboardStoryFlowPIE, Drone.Flow.PauseMenuRacingPIE, Drone.UI.FlightHUDKitLayout.
- ClaudeUIOverhaul4/report/index.json: 성공4·경고 동반 성공1·실패2, 합계7. 실패는 Drone.UI.FlightHUDKitLayout 및 KnownIssues.Flow.LobbyLayoutStabilityPIE. 이 파일만으로 인계 “재실행 후 실패1”을 확인할 수 없다. 포커스4건 재실행 통과·하네스 원인은 Claude 인계이며 전체80건 최종 재통과로 확대하지 않는다. 최종 로그/집계와 KnownIssues 포함 여부는 Claude 재확인 필요(TEST-HUD-LAYOUT-01).
- ClaudeCheckbox/report2/index.json: 성공2·경고0·실패0(타이틀/일시정지 체크박스). ClaudeHUD5/report3/index.json: 성공3·경고0·실패0. 앞선 HUD5/report는 3성공/1실패, report2는 2/2이며 최종 report3와 합산하지 않는다.
- Build Succeeded(마지막16:5x)·HUD 1920/1600/1280 정상 배치·캡처 내용은 Claude 인계 근거다. Codex 이번 Build 재실행·이미지 전수 열람·실제 장치 수동 Pass 없음. FlightHUDKitLayout 실패는 알려진 테스트 World 위젯 초기화 문제로 인계됐고 2회 수정 후 중단 원칙을 유지한다.
- 구현됨은 위 변경1~10, 자동 검증됨은 위 출처/조건 한정. 수동 확인 대기는 새 로비/브리핑/기체 선택/CONTROLS의 패드·마우스, 훈련 시작 안내, 체크박스 실사용, UGV 연사/재장전/유탄/Space·Ctrl, 팔레트 투하 착지, HUD 실제 해상도 배치다. 미구현은 HUD Kit WBP화·스카이드론 외형 연결이다.
- WORKBOARD 기존 관련 카드를 갱신하고 UI-WBP-EXPORT-01(구현·수동 대기), UI-HUD-WBP-01(미착수), UI-CONTROLS-DECISION-01(미정), ASSET-SKYDRONE-01(팀원 푸시 대기), TEST-HUD-LAYOUT-01(하네스/집계 확인)을 추가했다. 완료 구현을 수동 완료 카드로 닫지 않았다.
- 아카이브 대상/기준 날짜가 지정되지 않아 절 이동·아카이브 파일 생성은 하지 않았다. 현재 관련 요약/카드만 갱신해 크기를 STATUS 27,227→28,515B, WORKBOARD 29,848→28,466B로 유지했다(모두 보수적30,000B 미만). 과거 WORKLOG 본문은 수정하지 않았다.
## 확정·미정
- 사용자가 확정한 것: 위 변경 사실 전부(시안 이미지·Figma Slide 102 기준), 유탄은 발수 제한만·기관총만 연사, 훈련·레이싱 테마를 캠페인과 통일, START 통일, 그레이박스·시험 문구 제거, 레이싱 기체 = 스카이드론.
- 현재 미정(결정 쓰지 말 것): 게임패드 드랍 집기 버튼(시안 L2, 실제 R1), 게임패드 비행 범례가 FPV 모드 2 기준인 점, 키보드 UGV 범례 번호, 스카이드론 외형 자산(팀원 푸시 대기), 훈련 목록과 구현 수업 매핑(기획서 8개 vs UGV NPC 수업), 결과 화면 [다음] 동작.

### Space 반영·최종 문서 확인

기존 페이지 3개에 편집6건을 적용했다: 진행상황과 다음 작업 sequence44(4건, 현재 Git/UI·작업판/Next), 테스트 맵과 확인 가이드 sequence29(1건, UI·무장 수동 확인/검증 경계), Blueprint 조정과 팀원 가이드 sequence27(1건, WBP·HUD·UGV/조작·팔레트). 각 결과의 affected_blocks 총27개를 같은 페이지에서 다시 읽어 저장 hash 전부 일치·선택 완전성을 확인했다. 새 페이지 생성·기획/날짜별 기존 기록 삭제·공유/예약 변경 없음. 이번 대상 Space 미반영 없음. 기존 기획/지침/루트 페이지는 변경하지 않았다.

최종 로컬 변경 대상은 STATUS.md·WORKBOARD.md·docs/history/DRONE_WORKLOG.md 3개이며 Commit/Push는 하지 않는다. 문서 검사는 Git diff --check(CRLF 허용)·크기/변경 범위 대조로 마무리하며 엔진 Build·PIE·수동 Pass를 추가하지 않는다.

## 2026-10-16 — 저녁 HUD WBP화·가이드 상자·좌표·체크박스

작업·실행 Claude(HUD 바인딩 Claude 하위 에이전트), 문서·Space Codex. 2026-10-16 저녁 KST D PC, Unreal `D:\JGY\project\drone`·md `D:\JGY\project\md`. Codex 읽기 전용 Git 조회 HEAD6c07afa5·미커밋102개, 원격 기준 로컬 origin/main52594d0f(팀원 커밋 미수신·이번 Fetch 없음). MD 오전·오후 미커밋3개와 과거 기록을 보존했다. 아래 구현 사실은 Claude 지시서 인계이며 Codex는 지정 로그/보고서를 읽어 대조했다. 엔진 Build·PIE·자동화 재실행·Unreal 수정·Commit/Push 없음.

### 추가 구현·사용자 확정

1. `/Game/Drone/UI/WBP/HUD/WBP_DroneFlightHUDKit` 내보내기 생성(242위젯), `BP_DroneMissionPlayerController.FlightHUDWidgetClass` 연결 완료. `HudKit*` 고정 이름·`TryBindHudKitLayout`으로 중복 생성 없이 바인딩한다. Designer 위치·글꼴·색은 유지하고 코드는 값·상태색만 갱신한다. 코드가 그리는 나침반·고도 눈금은 `HudKitCompass`·`HudKitAltitudeLadder` 틀 위치·크기를 따른다. 화면 UI·HUD WBP 편집 가능, 예외는 로비 미션 카드 개별 버튼과 실행 중 코드가 다시 잡는 로비 배치 좌표. 프로토타입 맵의 구 `WBP_DroneFlightHUD`는 유지한다. 오후의 HUD WBP화 미착수 기록은 당시 상태이며 현재 구현 완료로 정정한다.
2. Tick 공간 좌표로 창의 바탕화면 위치만큼 눈금이 오른쪽 아래로 밀리던 문제를 `GetPaintSpaceGeometry`로 수정했다. 나침반·고도는 텔레메트리0.1초 간격 대신 매 프레임 기체 값으로 갱신한다. 나침반 시안3(가로 눈금·방위 상자·화면 최상단), 고도 시안2(사다리·뾰족한 지시 상자·VS), UGV 조준선 시안 반영. UGV ONLY와 왼쪽 속도 세로 눈금 제거.
3. 첫 LOS 수업 막대·화살표를 판정 구역과 같은 3D 테두리 상자2개(출발·전방, 각각12모서리)로 변경. 높이1.25~4m, 착지 단계 출발 상자 바닥~1.25m로 하강. 노랑/초록/흐림 색·두께8cm(BP 조정).
4. 설정 체크 값은 바뀌지만 체크 스타일 검정 전경 때문에 켜짐/꺼짐 그림 모두 검은 네모로 보이던 원인 확정·흰색 고정, `WBP_DroneSettings` 재생성. 타이틀·일시정지 양쪽 마우스·키보드·0.5초 유지 재현과 켜짐 ✓ 캡처 확인은 Claude 인계(`Saved/Automation/SettingsCheckbox/`); Codex 캡처 직접 열람·실사용 확인은 없음.
5. UGV Space/Ctrl 포탑 상하60°/초(BP 조정). 기체 설명/능력치 높이 고정, 로비 정보 칸은 글에 맞춰 증가·카드 제목 한 줄/완료 부제, 훈련·레이싱 로비 배경/사진 틀 캠페인과 통일, 드랍 목표 팔레트+LandingCollision 유지.

### 검증 출처 — D PC Claude 실행·Codex 원시 로그 대조

아래 경로는 Unreal `Saved/Automation/` 기준이며 온라인 업로드하지 않았다.

| 검사 | 조건 | 대조 결과 | 경로 |
|---|---|---|---|
| Build | DroneEditor Development | Result: Succeeded | `ClaudeHUDWBP/build.log` |
| HUD WBP 내보내기·연결 | Export·Wire | widgets=242 saved=1, changed=1 failed=0 | `ClaudeHUDWBP/export.log`, `wire.log` |
| UI·HUD 회귀 | RenderOffScreen | 성공18·경고0·실패1/총19, FlightHUDKitLayout Fail | `ClaudeHUDWBP/report/index.json` |
| 가이드·수업 | RenderOffScreen | 성공5·경고0·실패0: Mission·ObserverGuide·ObserverLessonPIE·HoverMissionPIE·MissionLessonsTestMap | `ClaudeGuideBox/report/index.json` |
| 체크박스 | RenderOffScreen | 성공2·경고0·실패0: 타이틀/일시정지 | `ClaudeCheckbox/report2/index.json` |

가이드 지시서는 수업4개를 나열했으며 원시 보고서는 Mission을 포함해5개다. 오후80개/후속7개 집계 차이를 이19개 결과로 해결 처리하거나 실행들을 합산하지 않는다. FlightHUDKitLayout 원인은 기존 테스트 하네스로 인계됐고2회 수정 후 중단 상태 유지.

구현됨: 추가분1~5. 자동 검증됨: 위 조건·보고서 범위. 수동 확인 대기: HUD WBP Designer 위치/글꼴/색 실행 반영, 창 위치를 옮긴 후 나침반/고도 눈금 정합, 첫 LOS 상자 가시성·색/착지 하강, 체크박스 실사용. 기존 로비/브리핑/기체 선택/조작 안내 패드·마우스, 훈련 안내·UGV 무장/조준·팔레트/해상도·이전 수동 항목도 유지한다. 알려진 미해결: FlightHUDKitLayout 하네스·스카이드론 외형(팀원 푸시 대기).

사용자 확정: HUD WBP화·첫 미션 테두리 상자·나침반/고도 시안·UGV Space/Ctrl 조준, Commit은 사용자 직접. 현재 미정 유지: 드랍 집기 패드 L2/R1, 비행 범례 FPV 모드2 기준 처리, 키보드 UGV 번호, 스카이드론 외형, 훈련8개↔UGV NPC 매핑, 결과 [다음].

### 문서·Space 반영

STATUS 현재 요약과 WORKBOARD 관련 카드/Next를 고쳤고 HUD WBP화는 구현 완료·수동 대기로 유지한다. 별도 아카이브 대상/기준 날짜가 없어 절 이동·새 파일 생성은 하지 않았다. 과거 WORKLOG는 수정하지 않고 이 절만 추가했다.

Drone Space 기존 진행상황 sequence45(5블록), 테스트 가이드 sequence30(3블록), Blueprint 가이드 sequence28(4블록)을 갱신했다. 수정12블록을 같은 페이지에서 재조회하여 저장 hash 일치를 확인했다. HUD 틀 위치/크기로 눈금 조정·상태색 코드 갱신·수동 경계를 반영했고 이번 대상 미반영 없음. 새 페이지·공유/예약·Trello/Figma 수정 없음. GitHub 본문 반영은 사용자 Commit/Push 후다.
## 2026-10-16 — 사용자 우선순위로 Drone 수신·Commit/Push

사용자 요청은 "맵은 팀원 자산 우선, 다른 겹침은 로컬 우선으로 Pull 후 Commit/Push"다. 실행은 Codex(D PC), Unreal 시작 HEAD6c07afa5·문서 HEAD95beefa이며 Git 작업 전 MD의 기존 미커밋3개와 기능 판정을 보존했다. 원격은 origin(gyeonliz/drone)만 Fetch했다.

로컬125상태(실파일121·삭제4·미추적46, 9,163,759B)를 Saved/Backups/GitSync_20261016_184841에 원시 바이트·SHA-256·index·diff와 함께 백업했다. Fetch 결과 팀원52594d0f·62f77024의2커밋/16경로가 incoming이었다. 실제 겹침은 Content/Drone/Abilities/RoleTargets/BP_RoleTest_PayloadTarget.uasset 한 개라 로컬 원시 바이트를 우선했다. 로컬 맵 수정은0개였다. Lvl_Battlefield·Lvl_MilitaryBase·Lvl_MilitaryCamp·TestMap/Lvl_NPCSmartObjectGreybox 맵4개와 그 밖의 팀원 자산은 원격본으로 수신했고, LFS14파일의 SHA-256 및 원격삭제1경로(M_Rador_Tower)를 확인했다. Fab 팔레트5자산·M_militaty_pallaet·포탑/그물/재밍/차량 BP도 포함된다.

첫 Stash는 별도 Claude의 UnrealEditor-Cmd(PID19324, ClaudeViewGuide 검증)가 자산을 잡아 미추적 정리 단계에서 실패했다. Stash와 바이트 백업은 생성됐고, 빠진28파일만 원본 백업에서 복원해125상태/121SHA 일치를 확인했다. 사용자가 해당 검증 프로세스 종료를 명시 승인해 PID/명령을 대조한 후 그 프로세스만 종료했다. 기존 로그는 백업에 보존했다. 해당 실행은 FlightGolden6개 비교 불일치·DefaultViewModeSetting 진행 중 정체 기록이 있어 완료/전체 Pass로 취급하지 않는다.

다시 임시 보관 후6c07afa5→62f77024를 FF 수신하고 로컬121파일을 바이트 그대로, 삭제4개를 복원했다. 맵을 Editor로 저장하거나 자동 병합하지 않았다. 동시 Claude 작업의 DefaultViewModeSettingTest 최신 수정 및 FlightGoldenBaseline.txt 변경도 커밋 직전에 별도 스냅샷해 d0c24f90(126파일·8,284+/758-)에 포함했다. staged Unreal 자산46개의 LFS pointer·실파일 SHA·로컬 LFS 객체 존재와 diff --check를 확인하고 origin/main Push 및 LFS46/46·7.8MB 업로드 성공을 확인했다.

첫 Push 후 Claude가 같은 테스트의 임시 PlayerController/LocalPlayer와 위젯 초기화를 추가 수정해 다시 로컬1파일이 남았다. 이 최신 수정도 별도 백업·diff 확인 후833c1c5f(1파일·17+/1-)로 Commit/Push했다. 최종 HEAD=origin/main=실제 ls-remote main 833c1c5f23c5d5b1ef56ec5da3ccc3ac719fc7f7, ahead/behind0/0·미커밋0·미추적0·unmerged0이다. 이번에 만든 Stash2개는 Push/복원 검증 후 SHA를 대조해 정확히 제거했으며 사용자 기존 Stash는 없었다. 바이트 백업과 manifest·integration/commit/push 증거는 위 Saved 폴더에 유지했다.

이번 작업은 사용자 로컬 변경의 수신/통합/공유이며 Codex가 새 생산 코드를 작성하거나 Build·PIE·전체 회귀를 실행한 것은 아니다. 별도 Claude 검증이 계속된 결과를 이번 통합 커밋의 Pass로 확대하지 않는다. 통합 뒤 기능/맵·전체 회귀·실제 패드·패키징은 후속이다. MD는 STATUS Git 구간·WORKBOARD 갱신일/SYNC-WORKPC-01·이 기록만 갱신하며 문서 저장소 Commit/Push는 이번 Drone Git 요청에 포함하지 않았다. Trello·공유 권한·예약·다른 원격은 변경하지 않았다. Drone Space 기존 현재 기준 블록의 Git/수신 요약도 갱신한다.

Space 최종 확인: 기존 진행상황과 다음 작업의 현재 Git 기준·문서 기준2블록을 sequence46으로 저장하고 같은 블록 재조회에서 전체 본문 일치를 확인했다. 19:01 KST 최종 실제 원격/HEAD833c1c5f·0/0·Clean·unmerged0·Stash0을 재확인했다. STATUS29,440B·WORKBOARD28,706B이며 MD diff --check는 원문CRLF 허용 기준으로 통과했다.

## 2026-10-19 — 드론 최신화와 면접 자료 반영

C PC `C:\URproject\drone`의 HEAD·origin/main·실제 원격 main이 `0d5f039d`로 일치함을 확인했다. 현재 작업 트리는 `DA_Mission_Racing_Circuit_Test` 수정 1개와 `DA_Mission_Racing_Map1/2/3` 미추적 3개가 있어 Clean이 아니다. 사용자 작업으로 판단해 내용을 덮어쓰거나 Stash·Commit·Push하지 않았다.

10/16 기준 문서 이후 변경을 코드에서 대조했다. Mission DA에 로비 숨김/준비 중 상태와 Runtime Placement(시작 Transform, 클래스별 태그, 실행 중 Actor 생성, M_Start·M_Target 표시 큐브 숨김), 코스별 `RecordCourseId`가 추가됐다. Flow는 준비 중 미션의 출격을 거절하고 다음 수업에서 숨김/준비 중 항목을 건너뛴다. PlayerController는 팀원 맵을 저장하지 않고 DA의 실행 배치를 적용한다. 튜토리얼 TUT 맵·HUD 해상도 캡처 자동화와 구성 도구도 추가됐다.

이번에는 Git·코드·자산 존재만 확인했다. 최신 HEAD Build·PIE·전체 회귀·수동 플레이는 실행하지 않았으며, Map1~3 DA는 아직 GitHub에 없다. STATUS·WORKBOARD와 Drone Space의 진행/Blueprint 가이드, 넥토리얼 면접 준비 Word 문서를 이 경계에 맞춰 최신화한다. Commit/Push·Trello/Figma·공유 권한·예약은 변경하지 않는다.

## 2026-10-19 후속 — Codex 직접 실행 제한 해제·레이싱 검증 대기

- 사용자 결정: Codex 직접 작업의 이전 Claude 전담/문서 전용·읽기 전용/Unreal 실행 금지 해제. 정본은 USER_RULES의 「Codex 직접 작업 기준」이다. md AGENTS·협업 규칙과 Unreal AGENTS/CLAUDE에 반영했으며 과거 세션 기록·브리지 위임 범위는 보존했다. 기존 변경/팀원 맵·인증정보 보호와 커밋/푸시 금지는 유지한다.
- 레이싱 요청은 DA 4개→3맵 진입/완주→코스별 기록 재실행 복원이다. 기존 DA 4개를 변경하지 않고 Git 상태와 ConfigureRacingTeamMaps.py/기존 카운트다운 시험을 읽었다. 실제 DA 로드·빌드·PIE·새 검증은 아직 미실행이다.
- Editor PID38056, 프로젝트 unreal-mcp 설정과 127.0.0.1:8000 Listen을 확인했다. 현재 노출된 Codex 도구에는 Unreal MCP가 없으며 프로토콜 초기화/실제 도구 호출은 아직 하지 않았다. 서버 Listen을 MCP 도구 연결 완료로 쓰지 않는다.
- 사용자가 직접 Editor를 켜서 확인하겠다고 하여 엔진 조작·빌드·PIE를 중지했다. 확인 종료 신호 뒤 Codex가 직접 레이싱 검증을 재개한다. 이번 로컬 규칙 결정의 Space 반영은 검증 결과와 묶어 후속 처리할 예정이며 아직 미반영이다. Commit/Push·맵/자산 저장·계정/권한/예약 변경 없음.

## 2026-10-19 — 훈련 사진·시작 카메라·레이싱 전체 뷰·실제 입력 가이드·오프닝

실행: C PC Codex, UE5.8.3 CL58210709. Unreal HEAD `0d5f039d`, MD HEAD `792e6079` 위 로컬 작업이다. 최초 사용자 변경인 Circuit DA 수정과 미추적 Map1/2/3 DA를 보존했다. 변경 대상 DA/WBP/그림은 `C:/URproject/drone/Saved/Automation/CodexTrainingUI`에 적용 전 사본을 남겼다. Commit/Push·Stash·맵 저장·전체 쿠킹/패키징은 하지 않았다.

### 훈련 사진과 실제 맵 시작 연결

- `UDroneMissionDefinition.BriefingImage`를 추가하고 비면 Thumbnail로 fallback한다. 제공한 선택8장·브리핑8장을 별도 Texture로 가져와8개 Tutorial DA에 연결했다. 원본 PNG·기존 Title 아트·MissionId/Rule은 유지했다. 재사용/적용 도구는 `SourceArt`, `Tools/AssetMigration/ApplyTrainingPresentationImages.py`에 있다.
- `ADroneTutorialObserverLesson`은 첫 LOS의 배치된 BP_LOS Actor Eyes Viewpoint(카메라 컴포넌트 없음)에 전방18cm를 더한다. 실측 카메라 `(62069.65,-19980.08,153.78)`, 패드 상단 `(62070,-20360,55.47)`이다. `SM_helicopter_base` 상단+기체 충돌 반경을 시작으로 쓰며 LOS 가이드/출발, Hovering/Return 판정을 실행 중 맞춘다. 없으면 기존 DA 시작값을 쓴다. 다른 비행 훈련은 드론1인칭으로 시작하되 저장된 시점 선호를 바꾸지 않는다.
- 실제 TUT_LOS/Hover/Forward_Gate/Circle_Gate/FPV_Target5개에서 진입·카메라/시작 자동 검사 통과. LOS 캡처의 초기 재질/노출·검정 안내선 외형은 최종 품질 Pass로 보지 않는다. 나머지 준비 중3수업을 강제 활성화하거나8수업 연속 완주로 확대하지 않았다.

### 레이싱 사진과 미해결 기록 경계

- `Drone.UI.RacingEditorOverview`는 Map1 Island·Map2 Production Lvl_DroneTraining·Map3 MountainRange를 **Editor에서 직접 열어 전체 뷰**를 촬영했다. Map3는 Landscape뿐 아니라 CourseSpline 경계도 포함한다. HUD/기즈모 없는1920×1080 원본은 `Saved/Automation/CodexTrainingUI/RacingMap{1,2,3}_editor_overview.png`, 재사용본은 `SourceArt/Racing`이다. `ApplyRacingMapThumbnails.py`로3개 DA의 Thumbnail/BriefingImage만 백업 후 연결했고 MissionMap/RecordCourseId는 유지했다. UI는 ScaleToFit으로 사진 전체를 보인다.
- 실제 Gate overlap을 자동 위치 이동으로 통과한 Map1 112개/Map3 187개는 각각7.003781초/7.896341초 기록·미션 완료가 됐다. 테스트 전용 `CodexRacingValidation_20261019` 슬롯으로 사용자 기록을 보호했다. **실제 연속 조종 완주 기록이 아니다.**
- Map2는102 GateSequence의 통과와 달리 최고 기록0/미션 미완료다. 분리 NullRHI 로그: `[RACING-RECORD-LOST] RacingMap2 accepted=100 next=100 state=0 segments=0 time=12.290061 drone=(-156040.80,24972.36,-1258.22) health=100`. Gate99/100 인접 중첩·자동 위치 이동의 같은 시각 통과가 후보이나 미확정이다. 0 이하 구간시간 보호를 풀지 않았고, world time 가드0.04초도 해결하지 못해 반복 수정을 중단했다. 다음은 두 Gate 기하/이벤트 순서 조사다. 새 프로세스 기록 복원 검사는 미실행이다.
- 초기 렌더 보고서는10 Success/1 Fail(Map2), 이후 별도 `FinalPresentationReport`는 레이싱 UI3개+ControlsGuide4/4다. 서로 다른 실행을 합쳐 전체 Pass로 쓰지 않는다. 이 렌더 결과는 **이후 교체한 최종 키할당 그림 외형 검증이 아니다**.

### 실제 입력에 맞는 가이드와 MCP 사용

- 사용자가 장치 몸체가 아닌 **실제 키할당 가이드**를 원한다고 정정해 번호/키/안내선이 포함된 전체 그림으로 교체했다. 패드는 실제 비행/UGV 매핑으로, RC는 원래 제공한 시뮬레이터 컨트롤러의 형태·스틱/버튼 위치를 기준으로 생성했다. 일반 라디오 조종기의 새 화면/스위치를 덧붙이지 않았다.
- 실제 Unreal MCP JSON-RPC 초기화→도구 조회/호출을 확인했다. 127.0.0.1:8000 Listen만으로 연결 완료라고 하던 이전 한계를 해소했다. MCP로 `IMC_DronePrototype.defaultKeyMappings.mappings`45개(구 deprecated mappings는 비어 있음), 지상 무장4개와 Scout/UGV CDO 참조를 읽었다. UGV CDO의 일부 None은 런타임 기본 자산 로드 경로와 대조했다.
- 범례는 쉬운 비행으로 한정·FPV 별도·고정 LOS 시점 예외를 명시한다. R1/L1은 비행 역할만, UGV는 L2 기관총/R2 유탄, □는 UGV 재장전, ○는 메뉴 뒤로다. 없는 기능은 안내하지 않는다. 기존 R1/L1 UGV 대체 바인딩 등 **입력 자체는 변경하지 않았다**.
- 최종 WBP `/Game/Drone/UI/WBP/FrontEnd/WBP_DroneControlsGuide`: `GamepadDiagramImage=T_Controls_Gamepad_Guide_Verified_20261019`, `RCDiagramImage=T_Controls_RC_Guide_20261019`, `bArtworkIncludesGuideLabels=true`를 MCP로 저장·Compile·재조회했다. 동일 이름 import는 덮어쓰기 미지원이라 기존 그림을 지우지 않고 Verified 별도 자산을 사용했다. 비율 보존·하단 범례 공간 보정, 한글 범례/탭은 UMG다. Native fallback과 제품 WBP override를 구분한다. 최종 생성 그림은 원본 해상도에서 확인했으나 새 게임 화면은 미확인이다.
- 사용자 마우스 제어 중단 요청 이후 화면/키보드 조작을 멈추고, 숨김 `UnrealEditor-Cmd -nullrhi`를 MCP 서버로만 사용했다. 보이는 Editor/PIE를 다시 열지 않았다. 실제 입력 장치 시험/영상 재생은 수동 대기다.

### 오프닝 영상

- `E:/새 폴더 (4)/Main_cinematic.mp4`를 `Content/Movies/Main_cinematic.mp4`로 복사했다. ffprobe: H.264/AAC·1920×1080·30fps·79.433333초·148,658,835B. 양쪽 SHA-256 `C8391DFBA106DBBA7D95D48AAE8E0890D04308570F40314D0DC57A88E1AE8755` 동일하다. MP4 LFS와 NonUFS 동봉 설정을 추가했고 StartupMovies 중복 재생은 하지 않는다.
- 새 `UDroneOpeningMovieWidget`이 MediaPlayer/MediaTexture/MediaSound로 재생한다. FrontEnd PC가 새 Boot에서만 표시하며 정상 종료/Esc/패드 ○·파일/열기 실패/시간 초과가 같은 정리→타이틀 경로를 쓴다. 종료 때 소리·미디어·타이머·델리게이트 정리, 타이틀 포커스 복원. 로비/미션 복귀 시 재재생하지 않는다. BP 조절값은 PC `bPlayOpeningMovie/OpeningMovieWidgetClass`, 위젯 `MovieFilename/OpenTimeoutSeconds`다.
- DroneEditor Win64 Development Build 성공(최종30.73초). MCP로 `Drone.UI.ControlsGuide`, `Drone.UI.GamepadGuideInputContract`, `Drone.UI.OpeningMovieContract` **3/3 Success·경고/오류0**. 마지막 로그 `Saved/Automation/CodexTrainingUI/headless_final_verify.log`의2026.10.19-04.44.21 UTC(13:44 KST) 확인. 테스트는 안내/실자산 매핑·완료/스킵 키·새 실행 조건·파일/포장 설정 계약이며, NullRHI/자동화는 영상을 의도적으로 건너뛴다. **실제 영상 화상/소리·패키지 배포판 Pass가 아니다.**

### 보호·인계

Production Training·Island·MountainRange와 Tutorial8맵의 원시 SHA-256은 작업 전후 동일하다. 최종 Git에서 `.umap` 수정 없음, UE diff --check 통과(CRLF 변환 안내만 있음). 미디어·소스·DA·WBP 변경은 로컬에만 있다. 계정/비밀 키·Trello/Figma·외부 권한·예약은 변경하지 않았다. 현재 상태/Next는 STATUS·WORKBOARD, 설정/실행 절차는 `docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md`가 정본이다. Space는 같은 기존 진행/시험/BP/안내 페이지를 갱신하며 아래 최종 영수증으로 확인한다.

최종 Space 반영: 진행 sequence49·시험32·BP31·안내11, 수정5연산/최종6블록 모두 적용 영수증과 재조회 hash 일치 확인. 새 Page·권한 변경·영상/대용량 자산 업로드는 없다. STATUS30,460B·WORKBOARD29,141B로30KiB 이하이며 MD diff --check도 CRLF 허용 기준 통과했다. 우리 숨김 검증 엔진 PID39532는 명령줄/프로젝트/로그를 대조한 뒤 종료했다. 현재 MCP 서버를 계속 켜 둔 상태가 아니며, 보이는 Editor/PIE는 시작하지 않았다.

## 2026-10-19 — 차량 후방 직격·자동 자폭·NPC 래그돌·호버 표시·UI/레이싱 사진 수정

요청: 차량 뒤쪽 타격 누락, 자폭 기본 무장/On·Off 잠금, 적 NPC 사망과 쓰러짐, 기본 피해/체력, 키보드와 같은 패드/RC 안내, 호버 구역 식별, 더 가까운 레이싱 사진/랜덤도시 임시 카드. 실행은 C PC Codex, UE5.8.3이며 기존 로컬 변경 위에서 작업했다. 원본 자산은 `C:/URproject/drone/Saved/Automation/CodexCombatFix/AssetBackups_20261019`에 보존했다. Commit/Push·맵 저장·Trello/Figma 수정은 하지 않았다.

### 원인과 구현

- 실제 TUT_FPV_Target의 BP_GroundConformingVehicle_Greybox를 MCP로 읽었다. HealthComponent가 없었고 이동 Root Box 반경은(200,100,100), 차체는 SM_CAR·상대Z=-86.24였다. 이동용 Box와 실제 차체 경계가 별개라 후방 누락 가능성이 있으며, 자폭도 직접 표적 없이 범위 피해의 Visibility 차폐에 의존하고 있었다.
- Vehicle Native에 공통 Health300과 차체 전체 DamageCollision을 추가했다. 원본 메시/Root/지면 추종은 유지한다. 사망→주행/Route 중지·NS_Expl_Tank_1/Cue_Explosion01 폭발·부착 포탑 Tick 정지·무충돌 잔해/30초 정리다. MissionDirector는 같은 Health 사망을 목표 Tag와 함께 받는다.
- 자폭은 기능이 있는 FPV/Fiber만 시작부터 무장하고 입력/스위치 해제를 잠갔다. 최소 속도100cm/s·피해600. 이동 전 속도와 Rotor Sweep까지 같은 접촉 경로로 묶고 반발 이전에 처리한다. 접촉 Actor에는 확정 피해, 범위 피해에서는 제외해 중복/차체 자체 차폐 누락을 막았다. Owner Health 사망/폭발 이벤트는 한 번이다. 원래 입력/API는 호환용 보존, HUD/브리핑/가이드의 무장/해제 지시는 제거했다.
- UGV는 기관총25·유탄150(차량에12발/2발), 200발·2초 재장전·유탄6발은 유지한다. 유탄도 접촉 확정 피해/범위 중복 제외다. 수치는 BP에서 조정 가능하며 임시 기준이다.
- NPC는 기존 Health100을 사용한다. AI/SmartObject 예약·사격/이동 정리 후 Capsule만 무충돌, PhysicsAsset 전체 시뮬레이션/블렌드·작은 수평 충격으로 쓰러진다. 원본 본/Skeleton은 삭제하지 않았다. PhysicsAsset가 없으면 숨김 fallback, 시체25초 정리다. 초기 물리 활성 상태만 확인하던 검사에 실제 골반20cm 이상 낙하를 추가해 '서 있는 사체'를 구분했다.
- 호버 구역이 Pad 메시 Forward와 출격 Yaw의 차이로 뒤/옆에 놓이던 것을 출격 정면6m·패드 위 중심3m로 맞췄다. 12변 테두리·진행 라벨·완료 색과 구체적 목표 문구를 추가했다. BeginPlay 내부 HasActorBegunPlay=false 때문에 재질 초기화를 건너뛰는 조건을 GameWorld로 고쳤다. 첫 Shader 준비 전 검정 프레임을 확인해 준비 시간을 둔 캡처로 구분했다. 신규 전용 M_HoverGuide_Visible의 Brightness1000은 과발광이라 MCP로3으로 낮추고 재컴파일/저장·실제 TUT_Hover 청록 테두리 화면을 확인했다. 원래 M_DroneTrainingGuide는 보존했다.
- 패드/RC 안내는 생성 PNG를 반복 편집하지 않고 `bUseUnifiedNativeDiagrams=true`의 UMG 키캡/테두리/번호로 통일했다. 원래 RC 형태·키 배치는 유지한다. 저장된 이전 도형도 한 번 갱신하고 미지원 ✕ 문자를 ASCII X로 교체해 최종 UI 글리프 경고를 없앴다. 옛 PNG/Texture 참조는 보존하되 현재 표시하지 않는다.
- 레이싱 사진은 활성 코스 경계/FOV8꼭짓점에12% 여백으로 맞춰 기존4.2반경 원거리를 줄였다. SetGameView 뒤 촬영 때만 Fog/Atmosphere/Cloud를 숨겼다가 원복한다. Map1/2/3의1920×1080 Editor 사진과 '?'·RANDOM CITY 임시 카드(실제 랜덤 지형 사진 아님)를 새 Close/Random Texture로 가져와 Thumbnail/BriefingImage에 연결했다. 원래 사진/DA 맵/RecordCourseId는 보존했다.

### 검증과 경계

- 최종 DroneEditor Build 성공8.14초, `Saved/Automation/CodexCombatFix/build_final.log`. 초기 로컬 변수 Mesh의 상속 멤버 가림 오류를 고친 뒤 성공했으며 엔진 API 사용 중단 예고/권장 컴파일러 경고는 별도다.
- `acceptance.log`/`acceptance_before_settle.json`: 집중14/14 Success. 전투/역할/통신·실제 FPV/Hover·Editor 사진3·요청 해상도1280/1920 UI·가이드/입력·랜덤카드 검사다. NavMesh 초기화 경고2건은 SmartObjectDeathPIE/RoleAbilities이며 기존 MOUT 배열 경고는 맵 검사 필터 밖 원본 문제다. 전체 프로젝트 무오류 Pass가 아니다.
- 후속 `settled_verify.log`/`settled_acceptance.json`: 최신 C++의 DamageAndDeath·SmartObjectDeathPIE·FPV·Hovering·RacingMap2 레이아웃 **5/5 Success**. 실제 FPV 수업에서 뒤쪽 이동 Sweep→무장 키 없이 차량0HP→MissionResult와 LastMissionOutcome=Success 확인. 전후좌우4면 Trace·직격 중복/유탄150×2·NPC25×4 사망도 검사했다. 실제 SmartObject 적의 전체 물리/골반 낙하·바닥에 누운 화면을 확인했다(Shotgun 전용 맵으로 대체하지 않음).
- 발광 조정 뒤 Hovering 별도1/1, `hover_brightness_final.json`. `Saved/Automation/TUT/Hovering.png`는 준비 후 청록 구역이 보이는 최종 사진이며 `SmartObject_NPC_Death.png`는 실제 시험 맵 사체다. 자동 위치/피해 주입 검사로, 실제 패드·연속 조종 호버3초/귀환·폭발 음량·잔해30초/시체25초 실시간 정리·전체 회귀/패키징 Pass는 아니다.
- UI의1280/1920은 요청 설정/범례 경계 검사이며 창/디스플레이 배율을 포함한 모든 실제 해상도 Pass가 아니다. RacingMap2 캡처에서는 초기 카드 포커스 영향으로1번 프리뷰가 남는 도구 한계를 관찰했다. 선택별 실제 UI 확인은 대기다. 사진4종의 **저장 DA 연결**은 재실행 MCP `saved_asset_facts.json`으로 직접 대조했고 MissionMap/RecordCourseId 유지 확인. GroundUGV 기본 테스트는 같은 이름 아래 Ammo 자식 보고서와 충돌해 Not Run이므로14개 집계에 넣지 않았다. 별도 Ammo 실행 로그는 Success이나 전체 무장 회귀라고 확대하지 않는다.
- 레이싱 사진/범례 수정은 기존 Map2 Gate100 부근 랩 기록 소실이나 새 프로세스 복원 대기를 해결한 것이 아니다. 사용자 기본 저장 슬롯은 바꾸지 않았다.

### 파일·인계

코드는 `Source/Drone/{Abilities,AI,Physics,Tutorial,Vehicles,Weapons,UI,Flow}`, 적용 도구는 `ApplyCombatHoverPresentation.py`·`ApplyRacingMapThumbnails.py`다. 새 재사용 그림은 `SourceArt/Racing/*Close*`·`RacingRandomCity_20261019.png`, 생산 Texture는 `/Game/Drone/UI/Textures/Racing`이며 호버 BP/재질과 DA만 저장했다. 사진/VFX/캐릭터 원본·Production Training/Island/MountainRange와 TUT 맵을 덮어쓰지 않았다. 최종 Git .umap 변경0, 보호 맵 SHA 동일·diff --check 통과(CRLF 안내 별도). 검증 엔진은 명령줄을 대조한 자기 프로세스만 종료했다. 자동 마우스/키보드·보이는 Editor/PIE 조작·비밀 키 복사·외부 자산 업로드는 없다.

정본 절차는 차량/피해 가이드·타이틀/로비 가이드, 현재 작업은 STATUS/WORKBOARD다. 기존 Drone Space 진행50·시험33·Blueprint32·안내12를 갱신했고 아래 최종 재조회로 보존/저장을 확인한다. 미커밋이라 다른 PC/GitHub 반영은 사용자의 Commit/Push/Pull 뒤다.

최종 확인: Space8개 연산의8블록 모두 적용·재조회 hash 일치. 보호 맵12개(Production/Island/MountainRange/SmartObject/TUT8)는 HEAD의 LFS SHA-256과 현재 원시 바이트가 전부 일치했다. STATUS30,630B·WORKBOARD29,413B로30KiB 이하, 문서 diff --check 통과. 두 HEAD는 그대로이며 우리 마지막 검증 PID39032 종료 뒤 UnrealEditor 프로세스가 남지 않았다. 이번 대상 Space 미반영은 없다.

## 2026-10-19 — 전체 문제 검증·코스/AI/UI/로딩 수정 (C PC Codex)

요청: 전체 문제를 검사하고 재현되는 오류 수정. Unreal `0d5f039d`·MD `792e6079` 위 기존 변경을 보존했다. 실제 UE5.8.3, 숨김 RenderOffScreen·로컬 MCP·정상 Editor Build를 사용했다. 커밋/푸시·패키징/전체 쿠킹·자동 마우스/키보드·보이는 Editor 조작은 하지 않았다. 아래 결과는 실행별이며 합산해 단일 전체 Pass로 쓰지 않는다.

### 확인한 원인과 수정

1. 레이싱2: 실제 Production 코스에서 92~99번 링이 위치·방향까지 같아 한 번의 overlap에서 `accepted=92→100`이 됐다. 같은 시각에 승인된 구간 때문에 Recorder가 유효하지 않은 0초 기록을 폐기했다. 검사 이동 속도만의 문제가 아니었다. `DroneTrainingCourse`는 자동 링의 연속 동일 위치(0.1cm 이내)·회전/크기 중복을 실행 중만 숨김·무충돌로 제외한다. 원본 Component 순서를 유지하며 실행 GateIndex를 다시 매긴다. 맵과 원본 링은 삭제/저장하지 않고 Recorder의 0초 거부도 유지했다. 실제 Map2는93개 실행 Gate로 완주·Mission Success·별도 키 저장 통과. 정상 간격·반복 Route 활성/비활성·나중에 출발점으로 돌아오는 링 보존 회귀도 통과했다.
2. UI: `SelectLobbyMission`이 Flow만 바꾸고 Preview/예약 포커스는 첫 카드에 남겨 다른 사진/START 대상이 될 수 있었다. 성공한 선택의 세 상태를 함께 맞추고 실제 DA 사진의 리소스 동일성까지 검사했다. 오프닝 뒤에는 루트만이 아니라 현재 타이틀 버튼 포커스를 재예약한다. 실제 파일 디코딩/재생 시간 진행·1920×1080 트랙·영상 화면·Unreal 내부 Esc→타이틀 버튼 복귀를 검사했다. 실제 장치 입력/음성 청감은 아니다.
3. MG: 저장된 Station BP의 Yaw/Aim Pivot이 Static이라 짧은 검사 중 이동 경고가1천 건 넘게 발생했다. `DroneMGTurretStation`에서 생성/Construction/BeginPlay의 회전 계층만 Movable로 보장했다. 고정 하단·맵은 보존했고 같은 실제 SmartObject 검사에서 이동 경고0을 확인했다.
4. 기존 AI 실패: `lost=0, disengaged=1`을 추가 추적했다. 자동 Sight가 초기 드론 `(-3000,2400,180)`을 먼저 보고 Rifle의 원점 `(900,-650,90)`에서30m 리시를 넘어 포기했으며, 이어진 수동 검사 자극은 무시 대상/쿨다운에 걸렸다. 범위 설정만 앞당긴 시도는 원인 해결이 아니었다. PIE에서만 자동 Sight를 끄고 재소유해 선행 교전을 정리한 뒤 MG 경합·점유자 사망/재점유·수색/순찰 복귀·재교전/드론 파괴까지 통과했다. 제품 리시/감지 규칙은 바꾸지 않았다. `Drone.AI.NPCPerceptionSearchPIE`를 기본 회귀로 복귀하고 known-test-failures에서 해결 행을 뺐다. 자동 실제 시야와 사용자 조종 비교는 별도다. 추격 포기 이유는 LogDrone Verbose의 `[NPC-DISENGAGE]`로 확인할 수 있다.
5. 기타: 호버 진행 라벨을 판정 뒤 즉시 갱신하고 이탈 초기화도 표시한다. 부모 테스트와 충돌해 누락되던 UGV 기본 검사를 `GroundUGV.Contract`로 바꿔 Ammo와 둘 다 실행했다. 옛 Circuit 선택/레이싱2개 전제 검사도 현재 팀원3맵+별도 도시 목록으로 고쳤다. DA3개의 ‘원형·7개’ 안내와 Map2 옛 거리 문구를 수정했으며 맵/기록 키는 재조회로 보존 확인. 원본 DA는 `Saved/Backups/CodexFullAudit_RacingText`에 보존하고 `ConfigureRacingTeamMaps.py`도 같은 문구로 맞췄다.
6. 마지막 전역 회귀에서 도시 로딩이0.94초에 닫히는 새 실패를 잡았다. 벽시계로 대기 시간을 계산하고 게임 시간 Timer로만 종료하던 혼용 문제다. 종료 콜백이 Wall clock 마감 시각을 다시 확인하도록 해 최소 표시/ReadyHold를 보장했다. 허용치를 낮추지 않았고 취소 시 마감도 정리한다. 수정 뒤 도시1.24초·Story1.02초, 로딩/취소/일시정지/재출격 등11개 통과.

### 실행 근거와 범위

모든 원시 결과는 Unreal `Saved/Automation/CodexFullAudit/` 아래이며 Git 제외다.

| 실행 | 결과 | 근거 |
|---|---|---|
| 최초 핵심 기능 | 136개 중134 Success·2 Fail(Map2 기록, 옛 레이싱2개 검사) | `core_before.json`, `full.log` |
| 최초 Flow/기존 문제 | 일반29개 중28 Success·옛 Circuit 선택1 Fail, KnownIssues4 Fail | `flow_before.json` |
| 등록 맵 진입 | 26개 중14 Success·12 미완료 | `full.log`; 중간15개 보고는 집계 오류로 정정 |
| 수정 집중 | 9개 중7 Success·Map2/AI 원인 추적2 Fail | `fixes1.json`, `fixes.log` |
| 코스 수정 | 24개 중23 Success·AI 격리 전1 Fail | `course_final.json`, `final.log`; Map2 93 Gate·전용 슬롯9.771385초(사용자 실제 기록 아님) |
| 새 엔진 복원 | 레이싱1·2·3 및 중복 링 검사4 Success·격리 전 AI1 Fail | `restore.json`, `restore.log`; 전용 슬롯 Map1 7.003781/Map2 9.771385/Map3 7.896341초 복원 |
| AI 격리 | 1/1 Success·경고0 | `ai_isolated.json`; 이후 전역/최종 관련 검사에서도 통과 |
| 전역 기능/UI | **172개 중171 Success·CityRacePIE 최소 표시1 Fail** | `regression_before_clock.json`, `regression.log` |
| 로딩 수정 후 관련 흐름 | **11/11 Success** | `clock_final.json`, `clock_final.log`; 전체172를 이 수정 뒤 다시 돌린 것은 아님 |
| 최종 Build | Success34.51초 | `build_clock.log`; 엔진 API/비권장 컴파일러 안내는 별도 |

`summary.json`이 실행 색인이다. 전역 대상204개에서 고비용 맵 진입26·별도 실제 레이싱3·사진 촬영3을 제외한172개를 실행했다. 별도 레이싱 완주/복원과 맵 진입 결과를 섞어204/204라고 보고하지 않는다. 최종 후속11개에는 CityRace·LoadingCancel·LobbySeed·StoryLoading·PauseRacing/Tutorial·MissionEntry·CheckpointRestart·OpeningMovie·NPCPerceptionSearch·Map2 UI가 포함된다.

### 남음·보호·다음 시작

- MilitaryCamp 로딩 중 PC 여유 RAM이 약340MB로 내려가 자기 검사 엔진을 종료했다. 나머지12개 맵 진입은 통과 아님. 최종 제한 회귀는 여유 약6GB를 유지했다. 고비용 맵은 메모리 확보 뒤 격리 실행한다.
- KnownIssues의 구 Production 구조 검사2개는 기본 역할 타겟/저장 NavMesh/구 링 개수를 전제로 한다. 구 Native Lobby 진단1개는 현재 Designer WBP를 받지 않는다. 현재 대상과 다른 전제를 해결하려고 팀원 맵/디자인을 덮지 않았다.
- 최종11개는 Success지만 MissionEntry의 Recast 초기화 경고1·PauseTutorial에서 외부 `MOUT_Fabrication/Demo/FirstPersonBP` 미등록 입력 경고24가 남는다. 원본 팩을 고치거나 숨기지 않았다. 무경고 전체 Pass 아님.
- 실제 패드/RC·연속 조종 완주/호버·청감·영상 자연 종료·시체25초/잔해30초 정리 체감·패키징은 별도다. 사진 전체 뷰/여백 가독성도 사용자 확인 대상이다. 검사는 실제 TUT/SmartObject/Production 대상에서 수행했지만 자동 위치/피해 주입을 실제 조종 Pass로 바꾸지 않는다.
- 보호 맵12개(Production·Island·MountainRange·SmartObject·TUT8)는 HEAD LFS SHA-256과 모두 같았고 `.umap` diff0이다. 최종 검사 PID55748을 명령줄 대조 후 종료해 남은 UnrealEditor가 없는 것을 확인했다. 비밀 파일/키는 읽거나 복사하지 않았다.
- 현재 조정/시험 절차는 코스 배치·타이틀/로비·자동포탑 가이드에 반영했다. 현재 상태는 STATUS/WORKBOARD를 따른다. 다른 PC의 새 코드/DA는 사용자의 Commit/Push/Pull 뒤이며 Space 갱신과 Git 배포는 별개다.

최종 문서/동기화 확인: 기존 Space 진행51·테스트34·Blueprint33·안내13의6개 연산을 적용하고 대상6블록의 본문/receipt를 재조회해 모두 일치했다. 새 Page/권한 변경/예약은 없다. STATUS30,548B·WORKBOARD29,430B로30KiB 이하, 두 저장소 diff --check 통과(CRLF 안내 별도), HEAD 유지·남은 UnrealEditor0·맵 diff0이다. 이번 대상 Space 미반영은 없다. 다음 담당자는 `Saved/Automation/CodexFullAudit/summary.json`과 `clock_final.json`부터 읽고 사용자 수동 체크/메모리 확보 후 남은 맵만 이어간다. 이미 끝난 전체 회귀를 이유 없이 반복하지 않는다.

## 2026-10-19 C PC — 남은 맵 격리 검사·외부팩 경계 수리

사용자 요청: 남은12개를 메모리 안전하게 하나씩 검증하고 고칠 수 있는 외부팩 경고 수리, 기존 변경 보존·Commit 금지. Unreal `0d5f039d`·MD `792e6079` 유지, UE5.8.3/Win64. 이전172개 전체 회귀는 반복하지 않았다. 이번 최종 Editor Build16.34초 성공(`Saved/Automation/CodexExternalPackAudit/build_standalone.log`), 일반 하네스 변경 빌드18.07초는 `build.log`다.

### 맵별 결과 — 통과/삭제/메모리 제한을 분리

`Tools/Validation/Test-RemainingMapsIsolated.ps1`이 맵마다 별도 UnrealEditor-Cmd PID를 실행·종료한다. 960×540 숨김 D3D12 렌더/NoSound, 최소 물리 RAM3GB·커밋4GB 보호, 기본300초 제한, PID·실행 파일·자신의 로그 경로 일치 확인 후 자기 프로세스만 종료한다. 다른 Editor가 Drone을 열면 거부한다. 실제 마우스/키보드 자동 조작·맵 저장은 하지 않았다. CLI 이름 양끝(^/$)을 고정해 OilRig가 Preview/Comparison까지 함께 실행되는 것을 수정했다(초기 OilRig 보고서만3개 포함, Final은 정확히1개).

| 남은 목록의 맵 | 결과 | 최소 여유 RAM(MB) | 근거 폴더/summary.json |
|---|---|---:|---|
| Lvl_NPCSmartObjectGreybox | PIE 시작·FPV 빙의 통과 | 8893 | CodexIsolatedMaps_20261019_Greybox |
| Lvl_OilRigPreview | 수리 뒤 정확한 단독 PIE 통과 | 7710 | CodexIsolatedMaps_20261019_Final |
| Lvl_OilRigRainComparisonTest | PIE 통과 | 8002 | CodexIsolatedMaps_20261019_Remaining |
| Lvl_ProceduralCityRaceTest | 수리 뒤 선택 흐름/PIE 통과 | 8479 | CodexIsolatedMaps_20261019_Final |
| Lvl_Tutorial_Hover_Test | PIE/선택 흐름 통과·초기 포커스 경고 잔존 | 8601 | CodexIsolatedMaps_20261019_Final |
| test1 | PIE·FPV 빙의 통과 | 8679 | CodexIsolatedMaps_20261019_Remaining |
| test2 | PIE·FPV 빙의 통과 | 8790 | CodexIsolatedMaps_20261019_Remaining |
| Lvl_OilRig | 수리 뒤 정확한 단독 PIE 통과 | 8318 | CodexIsolatedMaps_20261019_Final |
| Training1 / training1_1 / Training2 | 이미 삭제된3개, 검증 대상 없음 | — | git 3cb9c184(10/14) 삭제·현재 파일/참조 대조 |
| Lvl_MilitaryCamp | 독립 게임1회 통과·재현 안정성 미완료 | 아래 참조 | CampStandalone / CampFinal |

위 폴더 루트는 Unreal `Saved/Automation`이다. 기존14개와 이번8개를 합산해 최종 동일 빌드23개 일괄 Pass로 쓰지 않는다. `DroneMapStartPossessionPIETest.cpp`의 삭제된 옛3개를 제거해 현행 목록23개로 정정했다. 패키지 존재·LoadMap 반환값·실제 PIE 월드/GameMode/Controller 준비도 검사한다. 없는 맵의 이전 월드나 null을 ‘선택 화면’으로 오인하는 거짓 통과를 막는다. 맵은 복구/대체하지 않았고 TUT 수업별 전용 검사는 별도다.

MilitaryCamp: Editor+PIE 렌더는96.7초/최소3058MB·Private13071MB에서 보호 중단(Remaining). NullRHI도59.0초/2940MB·Private12601MB에서 PIE 복제 단계 보호 중단(CampNull)했다. 월드 이중 복제를 피한 `-game` 독립 렌더는54.2초/최소4655MB·Private18119MB에서 요청 맵 일치·BeginPlay·FPV 빙의 검사2.03초 Success(CampStandalone)였다. 그러나 최종 재실행은40.9초/2940MB·Private20244MB에서 자동 중단(CampFinal)됐다. ‘독립 게임이면 안정적으로 해결’로 판정하지 않는다. 반복을 멈추고 Camp 시작 전 여유 RAM20GB를 요구하도록 하네스를 강화했다. 실제 PreflightMemory 검사에서 엔진0회 실행으로 대기 처리(Preflight). 사용자 앱을 닫거나 페이지파일/품질·원본 맵을 임의 변경하지 않았다. 여유를 확보한 뒤 한 번만 재검증할 후속 대상이다.

독립 검사 `Drone.Flow.StandaloneMapStartPossession`은 ClientContext이며 Editor PIE와 다른 테스트다. `-DroneExpectedMap`을 요구해 잘못된 시작 월드는 거부한다. Editor 바이너리 -game에서 MCP용 Python Editor API가 없어 생기는 시작 스크립트 오류는 검사 프로세스 한정 `-DisablePython`으로 분리했다. 이 옵션이 메모리 개선을 보장하지는 않는다(최종 보호 중단). 렌더 실행도 화면 육안·실제 패드/비행/임무 완주를 검증한 것은 아니다.

### 외부팩 — 수리4자산·원본 백업·실제 흐름 재검증

`InspectExternalPackWarnings.py`로 그래프/하드·소프트 역참조를 조사했다(`CodexExternalPackAudit/graphs_before.json`). `FixExternalPackWarnings.py`가 다음4개만 저장했다. 원본은 `Saved/Backups/CodexExternalPackWarnings_20261019`, 최초SHA 영수증은 `CodexExternalPackAudit/fixes.json`이다. 중간 도구 API/로캘 보정 실패 로그도 보존했으며 최종 적용은 `fix5.log` exit0이다.

- MOUT `BP_MountedLadder_Slider`: Add가 반환한 첫 인덱스0에서 ‘이전 인덱스’ -1을 읽던 사다리/덮개2곳의 Attach 앞에 IsValidIndex/Branch. 유효 구간은 원래 연결, 첫 조각의 원래 실패 Attach만 생략한다. 새 조각을 자기 자신에게 붙이는 Clamp로 덮지 않았다.
- MOUT `BP_ElectricityPole`: 마지막 기둥 인덱스+1이 배열 길이와 같아지는데 Get 뒤의 IsValid만 있어 범위 오류가 났다. Get을 소비하는 IsValid 실행 전 범위를 검사한다. 끝의 없는 다음 기둥만 건너뛴다.
- `/Game/Drone/ThirdParty/{OilRig,OilRigPreview}/Assets/Cluster_Wall/Static_Mesh/SM_CL_wall_1`: 반투명 MI_Glass_windows가 Nanite와 비호환이므로 벽2종만 Nanite Off. 재질·다른 메시·전역 품질·맵은 유지한다. 자동 주석의 GUID 경고는 로드 시 생성된 GUID를 재저장해 정리했고, 최종 LOS 로그에서0이다. 재발 원인인 AddCommentToNodes 호출은 수리 도구에서 제거했다.

수리 뒤 실제 `Drone.Flow.PauseMenuTutorialPIE`(LOS 진입 포함)는 Success/오류0/경고8, 최소 RAM7019MB였다(`CodexIsolatedMaps_20261019_Tutorial/TUT_LOS/report/index.json`). 이전24건은 전부 입력 경고가 아니라 입력8개+배열 Script Msg/문맥16건이었다는 정정이다. 배열 범위/NodeGuid 경고는0으로 줄었고, 정확한 OilRig/Preview 단독 렌더 검사에서도 Invalid material/Nanite 경고0이었다. 숨긴 타이틀의 포커스 요청은 다른 상태에서 취소하도록 보강했지만 호버 시험맵의 대상None 초기 포커스 경고까지 해결한 것은 아니다.

남음: MOUT 외부 Demo FirstPersonCharacter의 옛 입력 참조8개는 보존했다. 전역에 사용하지 않는 입력을 만들어 숨기거나 데모 노드를 삭제하지 않았다. Modular_Insurgents의 SKM_BaseBody_Skeleton이 더는 없는 `/Engine/EngineMeshes/Humanoid`를 참조하는 로드 메시지가 있으며, 리그/애니메이션을 임의 대입·삭제하지 않았다. Camp의 VSM Non-Nanite Marking Queue overflow 및 시작 프레임 CharacterMovement 최대 반복 경고는 별도 성능 측정 대상이다. 기존 NavMesh 초기화/호버 포커스 경고도 잔존한다. 엔진 셀프테스트/인터넷 연결 확인/에디터 도구의 시작 로그는 제품 assertion 실패와 구분했다. 무경고·전체 게임 완료 보고가 아니다.

### 보존·다음 작업

수리4개 외 새 외부 자산 저장 없음, 모든 검사 대상 맵 SHA 동일·`.umap` diff0. 기존 코드/DA/아트와 Production Training 보존, Commit/Push·팀 권한/기획 수정 없음. 현재 절차는 `DRONE_TEST_MAP_GUIDE`에 통합했다. 더 무거운 반복/전체172 재실행 대신 Camp 메모리 확보 후 격리 재현, 남은 데모 입력/옛 리그 처리 판단·VSM/포커스 측정, 사용자 실제 패드/조종 확인을 이어간다. 현재 상태는 STATUS/WORKBOARD 정본이다.

마무리 확인: 보호 보고서6묶음의 맵 SHA 변경0, 수리4파일의 백업SHA가 모두 HEAD LFS 원본과 일치했다. 하네스 PowerShell 구문 오류0·남은 UnrealEditor0, 두 저장소 diff --check 통과(CRLF 안내 별도). STATUS30,465B·WORKBOARD29,568B로30KiB 이하, 아카이브 추가 없이 현재 상태를 교체했다. 기존 Space 진행52·테스트35·Blueprint34·안내14의4개 블록을 guarded 수정하고 본문/영수증 재조회까지 일치 확인했다. 미반영 Page 없음·새 Page/권한/예약 없음. 다음 담당자는 Unreal `Saved/Automation/CodexIsolatedMaps_20261019/index.json`부터 읽는다. 최신 Camp는 안정성 미완료이며 이전1회 Pass만으로 완료 처리하지 않는다.

## 2026-10-20 — MilitaryCamp 준비 메모리·스트리밍 및 외부팩 경고 정리 (C PC Codex)

요청: MilitaryCamp 메모리 원인 우선 확인·줄일 수 있는 부분 수정, 무거운 재실행 반복 금지, 외부팩 잔여 경고 수리. Unreal `0d5f039d`·MD `792e6079` 위 이전 변경을 보존했다. 실제 UE5.8.3 CL58210709·32GB C PC이며 로그 UTC10/19 15시대는 KST10/20이다. 맵 저장·Commit/Push·전체172 재검사·패키징/전체 쿠킹·DDC 삭제/대량 재생성·자동 마우스/키보드는 하지 않았다. 이번 결과를 Camp 전체 로드 안정성 Pass로 확대하지 않는다.

### 원인 조사 — 확인한 것과 아직 모르는 것

- AssetRegistry만으로 Camp 하드 의존성748패키지·디스크6.69GiB, Texture2D385개 중4096×4096이242개를 확인했다. StaticMesh136종이며 저장 Actor 메타데이터에는 StaticMeshActor4175개가 있다. 이 수는 디스크/저장 메타데이터이지 실제 동시 상주 메모리/실행 Actor 계측이 아니다. Base는1662패키지9.27GiB, Battlefield는821패키지3.59GiB이므로 파일 용량만으로 Camp의 RAM 문제를 설명할 수 없다.
- Camp 월드를 열거나 AI·PIE를 시작하지 않는 NullRHI 패키지 로드 진단을 **1회만** 했다. 40.7초에 가용 RAM3033MB·프로세스 Private10421MB에서 보호 중단했다. 최종 패키지 통계 파일은 생성되지 않았다. 준비/로드 단계에도 큰 메모리 증가가 있으며 AI 틱·화면 렌더링만의 문제라고 볼 수 없다. 다만 전체20GB 사용의 실제 배분·지배적인 할당·수정 후 전체 맵 피크 감소는 아직 미확정이다.
- 위 로그의 SkinnedAsset `[SkinnedAsset]|hpp` 예약4608MiB는 엔진 소스의 기본 SkeletalMesh 컴파일 예약량4096MiB 등에 따른 **스케줄러 추정치**다. 특정 `hpp` 메시가 실제4.5GB를 먹는다는 측정이 아니며, 파일/의존성에서도 해당 이름의 자산을 특정하지 못했다. 예약 추정치를 실측 메모리로 쓰지 않는다.
- Landscape/Foliage의 저장 bounds가 IsValid=false라 이 자료만으로 NavMesh/지형 크기·폴리지 인스턴스 수·실제 버퍼 용량을 단정하지 않았다. VSM Non-Nanite Queue overflow·시작 CharacterMovement 반복 경고는 이번 전체 Camp 렌더로 재현/수정하지 않았다.

### 수정 — 준비 동시성과 실제 스트리밍 장애

`Config/DefaultEngine.ini`의 `[SystemSettingsEditor]`에 자산/텍스처/스킨드 준비 동시성2/2/1, 추정 예산6GB를 설정했다. 처음2GB로 제한했으나 단일 작업 예약4608MiB도 넘지 못하게 하는 RAM 상한은 아니었고, 엔진이 단일 작업을 강제 진행하는 경고를 확인해6GB로 보정했다. 이 값은 전체 프로세스 RAM6GB 제한이 아니다. 초기 준비가 느려질 수 있으며 최종 게임 해상도/품질 설정을 낮춘 것은 아니다. 최종 실제 Editor CVar 검사에서2/2/1/6과 Camp 월드 미로드를 확인했다. Commandlet의 미초기화 Console 기본값(-1/0)과 실제 Editor 설정은 구분한다. 독립 -game 검사에도 동시성2/2/1을 명령줄로 전달한다.

원본 백업 후 산 텍스처2개만 수정했다. Source 픽셀 크기/GUID를 보존하고 새 엔진 RHI에서 다시 읽었다.

| 자산 | 수정 전 실제 준비 리소스 | 수정 후 | 해석 |
|---|---|---|---|
| FC_MilitaryCamp `T_Mountain_BC` | 4097²·Mip1·B8G8R8A8·NeverStream, 전체 Mip69,533,696B(66.3125MiB) | 원본4097² 유지, 빌드4096²·Mip13·DXT1·스트리밍, 11,206,656B(10.6875MiB) | 전체 Mip 리소스55.625MiB 감소. PC/맵 전체 피크 절감량은 아님. 1픽셀 빌드 리샘플/압축의 최종 질감은 수동 확인 |
| FC_MilitaryCamp `T_Mountain_N` | 원본/최고8K·Mip1·BC5·NeverStream, 67,108,864B(64MiB) | 원본/최고8K 유지·Mip14·BC5·스트리밍, 전체 Mip89,522,176B(85.375MiB) | 전체 Mip 용량은 증가하지만 거리별 Mip 상주 선택이 가능해짐. 실제 맵 상주 절감량은 아직 미측정 |

노멀은 NeverStream만 끈 첫 적용에서 Mip1이 남아 충분하지 않았다. FromTextureGroup으로 Mip 생성도 복구했으며 최종 두 텍스처 모두 `streamingMipChainReady=true`다. 해상도를 일괄 절반으로 줄이거나 외부팩 전체를 재저장하지 않았다.

### 외부팩 — 명확한 연결만 수리

1. MOUT Demo `FirstPersonCharacter`: 기존8개 입력이 실제 그래프에 연결돼 있음을 확인했다. 의미가 명확한 카메라4축만 MouseX/MouseY/Gamepad_RightX/Gamepad_RightY 원시 축 이벤트로 교체했다. 실행/AxisValue 연결·스케일 처리·입력 소비/일시정지/부모Override·노드 위치는 보존하고 주석을 남겼다. Blueprint 컴파일 오류0, 새 엔진 rawAxes4·remainingNamedAxes2다. 이동2축과 Jump/PrimaryAction은 원래 키 정책을 알 수 없어 유지했다. 사용하지 않는 전역 매핑을 만들거나 살아 있는 노드를 지워 경고를 숨기지 않았다.
2. Modular_Insurgents `SKM_BaseBody_Skeleton`: 현재 엔진에 더는 없는 옛 Rig 직렬화 참조를 같은 엔진 재저장만으로 정리했다. 다른 리그/애니메이션을 대입하지 않았다. 본68개·Skeleton GUID·본 이름/부모/참조변환·translation retargeting·virtual bone·compatible skeleton·retarget source/pose fingerprint `ac9c79dbc8efda24be1d4fbf4926d14b`가 원본과 새 엔진에서 같다. 새 검증 로그의 `/Engine/EngineMeshes/Humanoid` 로드 메시지0이다.
3. 실제 `Drone.Flow.PauseMenuTutorialPIE`(LOS 흐름 포함) 성공/오류0/경고4로 이전8→4를 확인했다. 남은4건은 Demo 이동2축/Jump/PrimaryAction이다. 전날 수리한 배열/NodeGuid·OilRig 유리/Nanite 경고0도 유지했다. 호버의 초기 포커스None/일시적 Recast 경고와 Camp의 VSM/시작 이동 경고까지 무경고가 된 것은 아니다.

이번 저장4자산과 원본 Config는 `Saved/Backups/CodexCampMemory_20261020/`에 있다. 자산 백업4개의 SHA-256은 HEAD LFS 원본과 전부 일치했다. 전날의 사다리/전신주·OilRig2벽 수정과 사용자 코드/DA/아트·팀원 맵은 그대로 보존했다.

### 실행 근거와 재실행 경계

`Saved/Automation/CodexCampMemory_20261020/index.json`이 이번 인계 색인이다. 원시 보고서/로그는 Saved에만 두며 Space에 대량 업로드하지 않았다. 아래 프로세스 피크는 **서로 다른 격리 검사**이며 전후 Camp 메모리 비교가 아니다.

| 실행 디렉터리 접미사 | 결과/시간 | 가용 RAM 최소 / Private 피크(MB) | 범위 |
|---|---|---|---|
| `_Readonly` | Pass27.8초 | 8681 / 2852 | NullRHI 자산 기준값, 텍스처 RHI 용량0은 실제 비교에 쓰지 않음 |
| `_Apply` | Pass45.3초 | 5593 / 7174 | RHI 자산4개 첫 수리, 원래 컬러 값은 assets_initial_applied.json |
| `_Mips` | Pass35.8초 | 6441 / 6644 | 노멀 Mip 생성까지 복구, assets_applied.json |
| `_Package` | **MemoryGuard40.7초** | 3033 / 10421 | 유일한 무거운 Camp 패키지 진단, AI/PIE 전 중단·최종 package_memory.json 없음 |
| `_Verify` | Pass35.8초 | 8443 / 5943 | 별도 새 엔진 RHI로 두 텍스처·Skeleton/카메라 축 보존 확인 |
| `_LOS` | Pass54.0초 | 8026 / 9435 | 실제 LOS 흐름 Success·오류0·경고4 |
| `_ProfilePreflight` | PreflightMemory | 시작 가용14608 / 요구20480 | 엔진 미실행, 무거운 진단 재시도가 아님 |
| `_Budget` | Pass33.7초 | 9850 / 5838 | 최종 실제 Editor 설정2/2/1/6·Camp 월드 미로드 |

최종 Build18.31초 성공(`build_budget.log`). 중간 Build/도구 보정 로그도 보존했다. 일반 Engine 셀프테스트의 시작 로그와 제품 테스트 assertion 결과는 구분한다. 전체172·Camp 전체 플레이·인간 조작/패드·최종 질감 육안 검증은 이번에 수행하지 않았다.

추가한 `DroneCampAssetAuditTest.cpp`의 진단3종은 Editor/dev-test 전용이다. `Diagnostics.Camp.MemoryAssetsAndWarnings`는 기본 자산 읽기 전용이며 명시적 `-DroneRepairCampAssets` 때만 백업/4자산 저장한다. 패키지 진단에는 별도 `-DroneProfileCampPackage`가 필요하다. `Diagnostics.Camp.EditorBudget`는 설정만 검사한다. `AuditMilitaryCampDependencies.py`는 AssetRegistry만 읽으며 `get_asset`/월드 로드/저장을 하지 않는다. 재조회한 registry.json은 태그 허용목록으로 불필요한 대형 Actor 메타데이터를 덜었고 최초 원시 registry_initial.json은 로컬 보존했다. 설명 주석 추가만을 위해 다시 엔진을 돌리지는 않았다.

`Test-RemainingMapsIsolated.ps1`은 Camp 전체 검사와 패키지 진단 모두 가용 RAM20GB 사전 검사를 적용한다. 실행 중 가용 RAM3GB/커밋4GB 보호·타임아웃·정확한 exe/로그를 확인한 자기 PID만 종료하며 다른 앱/엔진·페이지파일은 건드리지 않는다. 여유 확보 후 전체 Camp를 **한 번 계측할 후속 일**은 남기되 이번 세션에서는 더 무겁게 반복하지 않았다. 현재 실행 절차는 `DRONE_TEST_MAP_GUIDE`, 현재 상태/다음 작업은 STATUS/WORKBOARD 정본이다.

마무리: 자산 백업4개=HEAD LFS 원본, 모든 이번 검사 mapUnchanged=true·Git .umap 변경0, 하네스 PowerShell 구문 오류0·두 저장소 diff --check 통과(CRLF 안내 별도). STATUS30,516B·WORKBOARD29,596B로30KiB 이하이고 아카이브는 필요하지 않았다. 기존 Space 진행53·테스트36·Blueprint35·안내15의4개 블록을 guarded 수정해 모두 적용, 본문/hash 재조회 일치·미반영 없음을 확인했다. 새 Page/권한/예약/비밀값 복사/외부 자산 업로드 없음. 두 HEAD 그대로·검증 엔진 종료 상태를 최종 재확인한다. 수리 후 Camp 전체 안정성은 여전히 미검증이며 이전1회 Pass나 가벼운 자산 검사 Pass를 대신 쓰지 않는다.

최종 재확인 완료: Unreal HEAD0d5f039d·MD HEAD792e6079 유지, .umap Git 상태 변경0·UnrealEditor/UnrealEditor-Cmd 프로세스0, 두 저장소 diff --check 오류0. 이번 index.json 구문과 연결된 Budget/자산 검증/LOS/보호중단/Preflight 근거5경로의 존재를 확인했다. 추가 엔진 실행은 하지 않았다.

## 2026-10-20 — 사용자 훈련·미션·전투/UI 피드백 반영 (C PC Codex 직접)

### 범위와 보존

사용자가 PIE 피드백 중에는 이미지/코드 준비만, “엔진 껐으니까 싹 작업시작” 이후 Build·자산 적용·격리 검증을 승인했다. 이어진 방 배정/휴식/상점 메시지는 다른 기획안 대화용이라 무시하라는 최신 지시를 따랐다. 기존 미커밋을 보존하고 Commit/Push·원격 동기화·마우스/키보드 자동 조작·전체172 회귀·패키징·대량 DDC 재생성을 하지 않았다. Unreal HEAD0d5f039d·MD HEAD792e6079 위 로컬 변경이다.

### 이번 구현

- `DroneMissionFeedbackAssetTest.cpp`는 기본 읽기 전용이고 명시적 `-DroneApplyMissionFeedback`에서만 DA 원본을 백업한 뒤 저장한다. 원본14개는 `Saved/Backups/CodexMissionFeedback_20261020/Drone/Data/Missions/`에 있다. 기존 ID/Story Fact·분기/제한시간·기체·사람 BriefingLines는 보존했다. Tutorial/Story의 추가 ReturnToBase 규칙·Tutorial.Return.Zone 배치를 제거하되 첫 LOS(Hover 호환ID)의 이륙/전진/후진/착지는 유지했다. 귀환이 포함된 로비 요약만 남은 실제 목표로 수정했다.
- `TUT_Delivary`·`TUT_UGV_Turret`의 준비 중을 해제하고 DA Runtime Placement를 연결했다. 물자는 빈 집게로 시작→가까이 접근/실제 화물 집기→투하 적중, 포탑은 실제 자동포탑200HP 파괴로 완료한다. 새 Spawn 구조의 상대 시작점/지면 맞춤/이미 같은Tag 대상이 충분하면 생략 옵션은 BP/DA에서 조정 가능하다. 디버그 Arrow/SmartObject 전체 Bounds가 아닌 실제 보이는 StaticMesh Bounds로 지면을 맞췄다.
- Story DA는 확정 배정 M1 Battlefield·M2/3 MilitaryBase·M4 MilitaryCamp로 연결했다. 기존 목표 Tag/수량을 쓰는 Runtime 표적을 보충하고 M3 기존 레이더를 재사용한다. 시작은 배치된 M_Start 표식을 읽어 지면으로 보정한다. M2 경로 미지정 차량의 직선60m는 **데모용 임시 경로**이며 실제 도로/장애물/실패 동선은 검증 전이다. 맵4개의 모든 콘텐츠/스토리를 완성하거나 제품 전체 플레이를 통과한 것이 아니다. 기존 그물·ArchivedMarkers·M_Target·NPC·팀원 Production Training은 저장하지 않았다.
- `ADroneMGTurretStation` 공용 Health/DamageCollision·200HP를 추가했다. 사망은1회만 처리하고 조작자 사용/SmartObject 등록·추적/사격 Tick을 정리한다. 실제 연결 Base/Body/Barrel만 원본 메시/재질의 단순 Box 물리 잔해로 분리·15초 정리한다. 현재 `BP_AutoTurret_Emplaced`는 Base=model_part2_L·Body=model_part1_L·Barrel=None이므로 잔해2개다. 3단 신규 모델·Chaos 파쇄라고 표현하지 않는다. 원본 메시 Collision/재질은 보존했다.
- `ADronePlayerProjectile` 유탄 충돌에 ArmyVFX `NS_Expl_Tank_1`·InfantrySFX `Cue_Explosion01_Cue`를 연결했다. Projectile BP의 `GrenadeExplosionEffect/Sound/Scale`(0.25)로 조정하며 공유 자산 준비·Niagara AutoRelease 풀/자동 정리를 사용한다. 직격150→해당Actor 범위 중복 제외, MG25/200발·유탄6발은 유지했다. 현재 프레임 캡처에는 폭발이 선명하지 않아 **효과 생성 계약 통과와 최종 가시성/청감은 구분**한다.
- LOS는 BP_LOS 눈높이에서 뒤400·옆120·위80cm로 카메라를 빼고 수업 구간을 바라보게 했다. 다른 비행 수업은 드론1인칭이며 출격 SpringArm 초기 지연을 정리하고 자기 메시만 OwnerNoSee 처리했다. 외부 LOS/충돌/저장 카메라 선호는 보존한다. 시작 안내는 미션 BriefingImage(없으면 Thumbnail) 불투명 배경으로 초기3D 준비 프레임을 가리고 기존 WBP/버튼·정지/재개를 유지한다. Overlay Fill 보정 뒤 중앙 사진/목표1/1 화면을 확인했다. Lumen cached-lighting pre-exposure 경고 원인을 없앤 것은 아니며 전역 품질/노출 CVar로 숨기지 않았다.

### 장치 이미지 — 생성/연결/보류 구분

내장 imagegen 스킬/도구로 기기 외형만 있는 투명 RGBA PNG3개를 버전명으로 만들고 원본을 보존했다. `SourceArt/Controls/*_Device_20261020.png`·manifest에 원본 SHA/프롬프트/라벨 앵커를 기록하고 신규 Texture3개만 UI/NoMips로 Import했다. WBP/맵은 저장하지 않았다. 패드/키보드는 PNG 위에 편집 가능한 UMG 키/번호를 배치하고 기존 한글3열/탭·입력 바인딩을 유지한다.

사용자가 새 RC 외형에 대한 집착을 지적했다. 기존 조종기 가이드의 키 배치 참고를 외형 고정 승인으로 잘못 해석한 점을 정정하고 **추가 RC 생성·새 그림 적용을 중단**했다. 새 RC PNG/Texture는 삭제하지 않고 보존하되 `BuildDeviceArtwork(RCController)`에서 사용하지 않는다. 기존 Native RC7번호 안내만 유지하며 외형 개편 완료나 실물 일치로 쓰지 않는다. manifest 프롬프트의 USER-APPROVED는 당시 생성 요청에 있던 잘못된 가정이며 실제 사용자 승인 아님을 별도 명시했다.

처음8개 검사는 그림 비율 assertion이 없어 통과했지만 육안으로 새 패드/키보드가 좁아 보였다. 추가 렌더 기하 검사에서 두 그림 모두123.7×123.7로 Fail을 재현했다. UE5.8 Texture2D GetSizeX/Y는 비동기 준비 중 임시 기본 Texture 크기를 반환하며 이후 원본1536×1024·1774×887로 바뀐다. `GetImportedSize()`로 초기 배치 기준을 바꾼 뒤 새 엔진에서 패드185.6×123.7·키보드247.4×123.7(1280), 패드252.1×168.1·키보드336.1×168.1(1920)의1.5/2.0 비율을 확인했다. 장치별3열 범례가 패널 안에 있고 실제 캡처를 확인했다. 작은 글자/번호의 최종 디자인·실물 패드/RC 입력은 수동 확인이다. 과거 캡처는 `Saved/Backups/CodexFeedback_20261020/UI_Captures`에 보존했다.

현재 레이싱1·2·3 DA의 Thumbnail/BriefingImage는 모두 `T_RacingMap{1,2,3}_Close_20261019`다. 각각 Island·Production Training·MountainRange이며 실제 원본 사진3장을 사용자에게 표시했다. 개인 랜덤도시는 '?' 카드다. 옛 CodexTrainingUI의 이전 사진 바인딩 기록은 현재 근거로 재사용하지 않고 새 `assets_verified.json`로 확인했다. 이번에는 레이싱 월드/DA를 저장하지 않았다.

### 실제 검증과 중간 실패 정정

아래는 모두 C PC·UE5.8.3/RTX3080/32GB·숨김 실제 RHI 렌더이며 자동 위치 이동/피해 이벤트는 손 조종으로 세지 않는다. 일반 시작 self-test 로그의 Condition failed와 제품 assertion 결과를 구분한다. 원시 엔진 로그의 사용자/장치 메타데이터는 Space에 업로드하지 않는다.

| 실행 디렉터리 접미사 (`Saved/Automation/CodexMissionFeedback_20261020_`) | 결과 | 시간 / 가용 RAM 최소 / Private 피크(MB) | 확인 |
|---|---|---|---|
| ContractsVerified | 3/3 Success | 32.7초 /8040 /5993 | DA 적용/클래스 연결·전투·가이드 계약 |
| TUT_LOS | Pass | 39.7초 /7611 /9629 | 실제LOS·후퇴 시점/외부 드론 |
| TUT_Hovering | Pass | 52.9초 /6874 /10138 | 실제영역3초→귀환 없이 성공 |
| TUT_Forward | Pass | 40.7초 /5601 /9609 | 실제전방Trigger→성공 |
| TUT_Final_Payload | Pass | 49.0초 /6743 /10113 | 실제화물 집기/투하 이벤트→성공 |
| Visual_CircleGate | Pass | 45.9초 /6191 /10428 | 원형 순서완주→성공·안내 중앙 사진/목표1/1 |
| Visual_UGVTurret | Pass | 35.6초 /5779 /10260 | 실제설치형200HP·유탄2발 파괴/효과 생성→성공 |
| FinalVerification | 8/8 Success | 45.9초 /5118 /8955 | 읽기전용DA·전투·시작 안내 정지/재개·Story/수업 경량계약·가이드·1280/1920 |
| DeviceAspect | **Fail** | 40.9초 /5515 /6675 | 실제기하 비율 검사 추가로 새 그림1:1 오류 검출 |
| DeviceAspectFixed | 3/3 Success | 49.1초 /5754 /6717 | 원본비율 수정 후 가이드·1280/1920 재확인 |

최신 `DroneEditor Win64 Development` Build7.08초 성공(`Saved/Automation/CodexFeedback_build10.log`). 첫 Build의 ToSharedRef 오용1건은 수정했고 중간 Build 로그도 보존한다. 최종8개는 MissionAssets·Combat.DamageAndDeath·MissionStartPromptPIE·StoryPhysicsTestMaps·MissionLessonsTestMap·ControlsGuide·PresentationCapture2해상도다. 경량 Story fixture 계약은 제품 Battlefield/MilitaryBase/Camp 전체 플레이가 아니다. 뒤의 UI3개 재검증이 그림 비율 수정 후 최종 근거다. 전체172를 다시 돌리지 않았다.

중간 실패를 지우거나 통과로 합산하지 않는다. `Contracts`의 `|` 필터는0개 선택이었으며 이후 UE의 `+` 정확 일치로 교체했다. `ContractsFinal`은 원시 report2Success/1Fail인데 기존 wrapper가 먼저 Success를 봐 summary Pass로 잘못 표시했다. `Test-RemainingMapsIsolated.ps1`을 수정해 MemoryGuard/Timeout 우선·failed>0이면 Fail·실행0개/미실행은 Pass 금지로 바꾸고 완료 개수를 기록한다. **당시 summary는 역사 그대로 두되 여기서 정정**한다. 실패는 설치형에 없는3번째 메시까지 기대한 검사였고 실제 할당 개수2로 교정·별도 ContractsVerified3/3 및 Final8/8 통과했다.

첫 Payload 검사는300cm 집기 반경 밖350cm에 화물이 있는데 접근 전 검색해 Fail, Circle은 첫 Gate 전 Recorder Idle을 실패로 취급해 Fail이었다. 실제 배치 화물을 Tag로 찾은 뒤 접근/집기·첫 Gate를 받은 이후에만 Recorder 진행 검사로 보정하고 실제 이벤트 성공을 재확인했다. 제품 입력/규칙을 느슨하게 만들어 통과한 것이 아니다. UGV FX fixture는 자동포탑 선행 사격을 테스트 안에서만 억제하고 실제 시선 Hit 위치를 사용했으며 제품 AI 기본 감지는 바꾸지 않았다.

### Camp·남은 경고·인계

사용자 엔진 종료 후 RAM을 확인하고 Camp 사전 검사1회만 수행했다. `Saved/Automation/CodexFeedback_20261020_CampPreflight/summary.json`: 시작12620MB < 요구20480MB, **PreflightMemory·엔진/월드 미실행**이다. 지난 무거운 패키지 진단에 이어 추가 Camp 실행을 하지 않았다. 기존 컬러/Mip·노멀/스트리밍·Editor 준비2/2/1/6 수리는 보존하고 수리 후 전체 안정성/피크 감소는 미검증으로 둔다. 다른 프로세스/페이지파일을 강제 정리하거나 임계값을 내리지 않았다.

TUT 실행의 MOUT 데모 이동2·Jump/PrimaryAction 경고4는 원래 입력 정책 미정이라 유지했다. 이전 배열/NodeGuid·OilRig 유리/Nanite·Humanoid 참조 수리는 유지하고 새 근거 없는 전역 키 매핑/노드 삭제를 하지 않았다. Lumen 초기 노출·VSM/시작 CharacterMovement·호버 포커스/NavMesh와 실제 FX 가시성/청감은 남는다.

인계 색인은 Unreal `Saved/Automation/CodexMissionFeedback_20261020/index.json`, 최신 DA읽기 결과는 `assets_verified.json`이다. 현재 절차는 `DRONE_TEST_MAP_GUIDE`·UI/차량·Training 가이드, 지금 상태/Next는 STATUS/WORKBOARD 정본에 반영했다. Space 기존 진행54·테스트37·Blueprint36·안내16의 총8개 블록을 guarded 수정하고 같은본문 재조회8/8 일치를 확인했다. 오래된 날짜별 기록·부모/기획 페이지·Agent Instructions·권한은 건드리지 않았고 새 Page/예약 없음. 사용자 커밋/푸시 전에는 미커밋 코드/자산/MD가 다른 PC·GitHub에 있다고 말하지 않는다. 마지막 보존/구문 검사는 아래에 이어 적는다.

최종 보존 검사: 두 저장소 diff --check0, PowerShell2파일 구문 오류0·Python4파일 AST/기기 원본 RGBA/SHA 읽기 검증 통과. 색인에 연결한 근거 경로 누락0·DA 백업14개·Git .umap 변경0, 검증 엔진0·두 HEAD 그대로다. 사용자 진행 파일481B/수정시각01:16:33 유지로 자동화 전용 저장 분리를 확인했다(개인 저장 내용 복사 없음). STATUS/WORKBOARD는30KiB 이하로 유지해 아카이브 없이 현재 관련 절만 교체했고, 과거 날짜 기록은 고치지 않았다. 이 이후 추가 엔진 실행 없이 마무리했다.

### 후속 — RC 새 외형 후보·사망 연출/미션 연결 질의 확인

사용자가 기존 RC 그림의 외형을 명시적으로 거절하고 새로 예쁘게 만들어 달라고 요청해, 앞선 생성 보류 이후 **이번 후보1장만** 내장 imagegen으로 생성했다. 무광 차콜/금속 짐벌/얇은 청록 포인트의 새 케이스이며 `C:/URproject/drone/SourceArt/Controls/T_Controls_RC_Device_Premium_20261020.png`로 비파괴 저장했다.1536×1024·32bppARGB·모서리/왼쪽 가장자리alpha0·SHA3675cdb8307d79958261f03bc74d31b0c260e48fd112ca100f052c1f69913f73를 확인했다. 최종 영문 프롬프트/도구/경로는 기존 `controls_devices_20261020.json`의 별도 redesign_candidate에 기록했다. 기존 assets3개/Import 검사 형식은 유지하며 신규 Import·UMG 키 앵커/화면 적용·매핑/코드 변경·Build/엔진 실행은 하지 않았다. 기존 RC 안내는 유지되며 새 후보의 디자인 채택/최종 입력 안내 적용은 미완료다.

현재 코드로 재확인한 사망 연출: 차량300HP→0은 폭발 Niagara/소리·주행/포탑 중단·30초 정리, 포탑200HP→0은 사격/점유 중단·실제 연결 메시별 붕괴·15초 정리다. **포탑 자체 사망 시 폭발 Niagara/소리는 아직 미구현**이며 별도로 연결된 유탄 명중 폭발과 혼동하면 안 된다. 본/Skeleton을 삭제하는 방식이 아니다. 이번 질의는 확인 요청이므로 전투 코드를 추가 수정하지 않았다.

현재 `assets_verified.json` 재조회로 물자=TUT_Delivary·포탑=TUT_UGV_Turret·M1=Battlefield·M2/3=MilitaryBase·M4=MilitaryCamp, 준비 중False를 확인했다. 기존 물자/포탑 자동 클리어 근거와 제품Story 전체 플레이 미검증·M4 메모리 대기는 유지한다. 과거 메모리 검색은 오래된 대화 보존본이어서 최신 완료 근거로 사용하지 않았다. 별도 Commit/Push·미션DA/맵 재저장 없음.

직후 사용자가 “우리 컨트롤러는 네모모양”이라고 정정해 첫 차콜 후보를 같은 재질/조작부의 **직사각형 케이스**로1회 수정했다. 결과 `SourceArt/Controls/T_Controls_RC_Device_Rectangular_20261020.png`(1536×1024·32bppARGB·모서리/왼쪽alpha0·SHA473f115dbc8e6aed1b967bd702e9ea7adca03faac09e219dc81e024855bbdd18)를 별도 저장하고 앞선 손잡이형 후보/원본은 보존했다. manifest의 rectangular_candidate에 실제 최종 프롬프트·참조·경로를 기록했다. 네모형 요청 반영과 실제 실물 버튼 위치 재검증은 별개이며, 현재 최신 후보는 미Import/미연결이다. 엔진/Build·코드/매핑·맵·DA 변경은 없다. 현재 UI/전투 경계는 기존 Blueprint Space 페이지와 관련 진행/안내 문구에도 정정했다.

### 후속 — 확인 배치 RC 실제 적용·레이싱3맵 사진 교체·포탑 자체 사망 연출

사용자가 기존 도식의 버튼 배치는 맞다고 확인하고 네모형 검정/은색 외형·오른쪽 아래 세로 롤러(회전 위/아래·누름 확인)·왼쪽 아래 하단Cancel로 새 그림 적용과 전체 마무리를 요청했다. 최종 생성본 `exec-b3b1111f-8f7d-4566-b88a-6a4a62350301.png`를 `SourceArt/Controls/T_Controls_RC_LayoutMatched_20261020.png`로 보존했다(1536×1024·SHA7897ef70da58ca4700d3cef20e41a389774c6cf7ea8079d06af70b3400f14cd8). 이번 턴에 다시 생성하지 않았다. 최종 프롬프트·원본/앵커는 기존 controls manifest의 approved_rc에 두고 이전 후보/PNG/Native 폴백을 보존했다.

Native RC 표시 보류를 해제하고 새 Texture1개를 Import, 기존 WBP_DroneControlsGuide의 RCDeviceImage·범례6번만 연결했다. Designer 트리 재생성·실제 매핑 변경은 없다. UMG7번호/키와 그림에 같은 비율 변환을 사용한다. GenericUSB17/18→위/아래·16→확인·15→Cancel을 실제 Slate 합성 Raw키로 검사해 포커스 이동/복원·브리핑 뒤로·훈련 시작 정지/재개를 확인했고, 시작 안내에 휠 누름 설명도 추가했다. 실물 입력 시험과는 다르다. 실제 저장 WBP가 새 Texture를 쓰는지와1280/1920 비율을 렌더 검사했다.

기존 Close_20261019 레이싱 사진은 전체 지형/검정 배경과 디버그 큐브가 보여 이름만으로 근접 결과라고 할 수 없었다. 실제 Editor 맵1 Island·맵2 Production Lvl_DroneTraining·맵3 MountainRange를 각각 열어 FOV70 사선 전경으로 재촬영했다. 첫 촬영은3개 자동 통과했지만 눈으로 보니 GameView의 큐브가 남았다. 두 번째에서 촬영 중 Game/Editor 숨김 플래그를 함께 바꾸고 원복했다. 첫 사진은 attempt1에 보존하며 추가 반복은 안 했다. 최종 촬영은43.9/46.9/42.9초, 최소 가용6065/4769/6758MB·맵2 최대Private9515MB다. 시작/실행4GB 보호와 커밋 보호를 유지했고 실제 World 경로·맵 파일MD5 불변을 Native 검사했다. 래퍼의 FrontEnd는 검사 컨테이너이며 실제 촬영 대상이 아니다. 사진에 지형/코스 주변 사선 전경이 보이며 전체 게이트가 식별된다는 주장은 아니다.

`SourceArt/Racing/RacingMapN_CoursePreview_20261020.png`와 새 Texture3개를 저장하고 DA_Mission_Racing_Map1/2/3을 원본 백업 뒤 Thumbnail/BriefingImage만 교체했다. MissionMap/RecordCourseId 불변을 확인하고 랜덤도시 '?'·옛 사진/Texture·원본 맵/컴포넌트를 보존했다. 새 로비/브리핑 화면에서도 실제 DA 사진과 선택 항목 일치를 검사했다.

기존 포탑 자체 HP0 폭발 미구현을 이번에 보완했다. DroneMGTurretStation에 DestructionExplosionEffect/Sound/Scale(0.35)을 노출하고 ArmyVFX NS_Expl_Tank_1·InfantrySFX Cue_Explosion01_Cue를 한 번 준비·강한 참조로 유지한다. 사망 가드 안에서 피해Box 중심에 AutoRelease Niagara/소리1회, 중복 피해나 새 범위 피해 없이 기존 점유 해제/실제 메시2개 잔해15초를 유지한다. 차량300·포탑200·MG25/유탄150/자폭600·NPC100은 그대로다. 실제 BP 전투 검사와 TUT_UGV_Turret 유탄2발→HP0·자체 효과 생성1회→클리어를 통과했다. 사진은1초 뒤 잔해만 보여 캡처 대기만0.15초로 줄여 한 번 보강했으나 불꽃이 여전히 뚜렷하지 않다. 따라서 **효과 생성/사망 연결 자동 통과, 최종 가시성/청감은 수동 대기**로 남기며 화면 검증 완료로 쓰지 않는다. 게임의 효과 수명/임무 종료를 지연시키지 않았다.

Build5회 모두 성공(65.70/18.27/5.71/16.16/13.24초, 후반은 검사 코드 보완). 최종 FrontEnd 묶음은 실제8/8·70.4초·최소7101MB다. 래퍼가 끝 앵커를 붙여 마지막 Map3가 필터에서 빠진 것을 집계8로 발견했고 Map3UI만 별도1/1·40.8초·최소7134MB로 검증했다. 실제 포탑 수업 최종1/1·41.8초·최소5893MB, 첫 수업 검사는46.9초였다. 전역172·Camp를 재실행하지 않았다. 기존 MOUT 데모 이동/액션4경고와 검사 시작 전 Condition failed 엔진 로그는 남아 있으며 제품 시험 실패0을 경고0으로 바꾸어 쓰지 않는다.

근거 정본: `C:/URproject/drone/Saved/Automation/CodexRCFinalize_20261020/index.json`, 새 RC manifest·racing_thumbnail_bindings.json·실행별 summary/report. 변경 전 코드/기존 WBP/DA 백업은 `Saved/Backups/CodexRCFinalize_20261020`이며 기존 작업을 재설정하지 않았다. 사용자 진행도 JSON481B/UTC2026-10-19T16:16:33 유지, .umap 변경0, HEAD Unreal0d5f039d/MD792e6079 유지·Commit/Push 없음. STATUS/WORKBOARD는 현재 문구를 교체해30KiB 아래로 유지한다. 실제 조종기/패드·청감/폭발 가시성·Story 제품4맵/M2도로·Camp 안정성/패키징은 남는다. 다른 PC에서는 사용자가 GitHub Desktop으로 이번 로컬 변경을 전달하기 전 자동으로 볼 수 없다.

maintain-space 절차로 기존 진행/테스트/Blueprint/안내4페이지의 현재6블록만 갱신했다(각sequence56/38/39/18). 전 연산 적용·같은6블록 저장 후 본문 일치를 확인했다. 새 Page·미디어/자산/개인 로그 업로드·기획/과거 기록 정리·Trello/Figma 수정·예약·권한 변경은 없다. 최종 STATUS30220B·WORKBOARD29230B로30KiB 아래이며 별도 아카이브 이동은 필요하지 않았다.

### 후속 — 사용자의 원거리 사진 거절·RC LT/RT 표시 개선

사용자가 직전 레이싱 사진도 더 가까이 찍으라고 지적했다. 이어 RC의 LT/RT 모양/표시 개선을 요청했다. 기존 CoursePreview 사진을 근접 요구 충족으로 더 주장하지 않고 원거리 전체 코스 Fit을 제거했다. 새 아트를 생성하거나 원본 조종기 PNG/키 할당을 바꾸지 않았다.

실제 Editor 맵1/2/3에서 활성 코스40% 주변 지형에 근접 카메라를 뒀다. Landscape 수직 Trace로 지면 높이를 맞추고 외곽 코스의 중심은 촬영 중에만 지형 안으로 제한한다. FOV60·대상 거리680.1/680.1/712.8m이며 맵 전체/모든 게이트를 한 장에 넣으려 하지 않는다. 1번 설산 능선·2번 수목/게이트 구간·3번 설산 계곡을 눈으로 확인했다. 실제 월드 경로/맵 MD5 불변 검사3/3,46.0/53.1/44.9초·최소 가용7243/5339/7021MB. 맵2 최대Private10219MB·RAM4GB/커밋 보호를 유지했다. 재촬영은 각1회이며 Camp나 전투/전체172 검사는 재실행하지 않았다.

새 `SourceArt/Racing/RacingMapN_NearView_20261020.png`와 Texture3개를 저장하고 사진 확인 뒤 `-RacingPreviews -RacingNear`로 실제 DA Thumbnail/BriefingImage만 연결했다. DA 백업과 MissionMap/RecordCourseId 불변을 확인했으며 옛 Close/CoursePreview/랜덤도시 '?'와 팀원 맵을 유지했다. 결과/메타데이터는 `Saved/Automation/CodexRacingNear_20261020/racing_thumbnail_bindings.json`에 있다.

RC LT/RT는 금속 레버 위 글자를 없애고 바깥 `④ LT`·`⑦ RT`의 짧은 UMG 칩+얇은 지시선으로 분리했다. Native ControlsGuide와 기존 WBP 실제 화면에서 확인했다. 첫 칩76×34는 폭이 빠듯해96×34로 한 번 보강하고 최종1280/1920의 TextBlock이 칩 내부에 들어오는지 자동 검사했다. 번호7개·기존 다른 버튼/범례/휠·실제 매핑과 원본PNG는 유지했다. controls manifest에는 원래 레버 앵커와 별도로 외부 라벨 배치를 기록했다.

Build8.33초·폭 보강 후6.53초 모두 성공. 새 사진 연결/Guide/1280/1920/레이싱3종 UI6/6·75.4초·최소6975MB 통과 후, 칩 폭만 수정해 Guide/1280/1920 3/3·50.0초·최소7380MB를 추가 통과했다(중복 시험이므로9종 전체 Pass라고 합산하지 않는다). 최종 조종기 실제 화면과 새 레이싱 선택 화면을 확인했다. 기존 엔진 사전 Condition failed 로그/MCP 고지는 남으며 경고0을 주장하지 않는다.

근거 정본은 `C:/URproject/drone/Saved/Automation/CodexRacingNear_20261020/index.json`. 변경 전 파일/DA는 `Saved/Backups/CodexRacingNear_20261020`에 보존했다. 원본 .umap 변경0·사용자 진행도481B/UTC2026-10-19T16:16:33.452796Z·Unreal0d5f039d/MD792e6079 유지·Commit/Push 없음. 물리 조종기 감도/방향과 기존 폭발 가시성/청감·Story/Camp/패키징의 수동 대기 경계는 그대로다.

maintain-space로 기존4페이지 현재5블록을 수정하고 전부 저장 후 본문 일치를 확인했다(sequence57/39/40/19). 최종 RC 화면2장은 위 근거 폴더의 RC_LT_RT_1280/1920.png로 별도 보존했다. 사진3장의 SHA가 실제 DA 연결 영수증과 일치·두 Git diff--check0·엔진 프로세스0이며 STATUS30205B/WORKBOARD29229B로30KiB 아래다. 새 Page/미디어 업로드·과거 기록 정리·Trello/Figma·권한/예약·Commit/Push 변경은 없다.

## 2026-10-20 — LOS 복귀 예외 보존·귀환 안내 정리·실제 미션 검증 (C PC Codex)

사용자는 전체 미션 검증과 귀환 요구 제거를 요청한 뒤 **LOS만 복귀/착지까지 한 수업이므로 유지**한다고 명시했다. 이 정정을 DA 저장/Build 전에 반영했다. LOS는 Hover ID·이륙→전진→후진 복귀→실제 착지4단계와 원본 DA SHA256 `BB05376C1FBAB22C7D491189C1FA84AD2EBCF377EA81FDEEE85618F7A2EB6E14`를 보존했다. 메뉴 Back/로비 복귀·NPC 순찰 복귀·범용 ReturnZone API·기존 맵 안 액터는 삭제하지 않았다.

`UDroneMissionDefinition`에 명시적 저작/이관용 `RemoveReturnRequirements / HasReturnRequirements`를 추가했다. LOS는 예외이며 다른 DA의 ReturnToBase Rule·ReturnZone 실행 배치와 로비 설명/요약/보조정보·시작 목표/LoadingTips·Briefing/Radio의 낡은 귀환 문구를 정리한다. 수정된 자막에 옛 음성이 남지 않게 해당 Voice 참조도 비운다. 자동 로드/플레이 때 DA를 수정하지 않는다. 이전 저작 스크립트8개에도 저장 전 호출을 연결해 재도입을 막았다. Native `-DroneRemoveAllMissionReturns`는 다른 연결/배치 재설정을 건너뛰는 귀환 전용 적용이며 원본을 `Saved/Backups/CodexMissionNoReturn_20261020`에 보존한다. 실제 새 저장은 Forward/Hovering의 잔존 안내2개 DA뿐이고 다른 Story/수업의 기존 정리 결과는 검증만 했다. 비레이싱14개 정의·레이싱5개 참조 행을 검사했고 MissionMap/기체/진행ID/Story Fact는 보존했다.

새 Story 자동화는 FrontEnd 실제 선택→브리핑→제품 맵 이동→기체 선택/출격을 거쳐 본목표 성공을 확인한다. M1 첫 RHI 실행은 가용 RAM3949MB로4GB 보호 중단(43.5초)했다. 무거운 화면 재시도는 하지 않고 같은 Battlefield의 NullRHI로 전환했다. 첫 논리 검사 실패 후 목표 메시 경계 위에 정확히 투하하도록 fixture를 보강해도 의도 표적이 아닌 곳에 먼저 충돌했다. 로그에서 표적 원점Z111.26/상단226.26·Payload 안착Z456.41·delivered0/hitTarget0을 확인했다. 원인은 같은 Tag 기존 액터를 재사용할 때 생성과 함께 지면 보정까지 생략하는 경로였다. 호환 클래스/첫 Tag로 중복을 세고, bSnapToGround가 켜진 재사용 표적의 실제 표시 메시가 지형에 묻힌 경우만 위로 보정한다. 기존 XY/회전·맵은 보존한다. 실제 M1은 Shack 위로328.99cm 보정 뒤 물리 투하 first impact→delivered1/hitTarget1→즉시 MissionResult Success를 통과했다. 이 수령 위치의 최종 외형/요원 배치는 별도 확인이 필요하다.

M3의 최초 실패는 회전/스케일된 레이더 Box의 바깥점을 월드X와 로컬 Extent로 섞어 완전히 이탈시키지 못한 검사 오류였다. 실제 월드 AABB/드론 경계 바깥으로 fixture를 수정해 진입/완전 이탈→성공을 통과했다. 생산 재밍 코드는 바꾸지 않았다. M2는 실제 차량의 이동을 확인한 뒤 실제 FPV 후방 Sweep 자폭으로 HP0→성공을 확인했다. 임시 직선60m 경로의 도로/장애물 적합성까지 검증한 것은 아니다.

Build1은 새 테스트의 UArrowComponent 완전 타입 include 누락으로 실패했고 수정 뒤 Build2 7.58초·진단 보강 Build3 15.87초·최종 Build4 8.08초 성공했다. 최종 읽기 전용 DA/귀환 정책·ObjectiveRules·LOS 계약/접지·PayloadLanding **6/6**(17.2초·최소9425MB) 통과다. 실제 TUT7종은 각 새 프로세스 RHI에서 LOS34.4/호버42.6/전진30.4/원형30.4/FPV30.5/물자30.5/포탑29.4초 모두 통과했다. 최소 가용6116~6514MB·최대Private10372MB이며 LOS4단계/다른 수업 즉시 성공·집기/투하·포탑 파괴를 확인했다. LOS와 원형 시작 화면을 직접 읽어 원형 안내에 귀환이 없는 것을 확인했다. 기존 LOS Lumen 노출 경고와 외부팩 경고는 남으며 무경고/시각 완성을 주장하지 않는다.

최종 실제 Story M1/2/3은 각각29.5/25.5/26.4초, 최소7366/8281/7624MB로 NullRHI 통과다. 화면/손 조종 Pass가 아니다. M4 Camp는 가용12067MB<요구20480MB로 `PreflightMemory`·엔진 미실행이다. 검사 별칭 StoryM4여도 실제 Camp 패키지에20GB 보호가 적용되게 도구를 보강했다. 자유 게이트는 comingSoon=true 그대로이고 숨김 수업/Story 최종 단말·Scan/역할교대·엔딩·실물 장치/패키징은 완료 처리하지 않았다. 이전 레이싱3맵/사진·RC·전투 결과는 보존하며 이번 전체172 회귀로 확대하지 않는다.

근거 정본: `C:/URproject/drone/Saved/Automation/CodexMissionNoReturn_20261020/index.json`과 거기서 연결한 assets_applied/verified·FinalAudit·Verify_<case>/summary/report/engine.log. 이전 실패/메모리 중단도 삭제하지 않았다. 대상 맵 SHA 불변·.umap 변경0·사용자 진행도481B/UTC2026-10-19T16:16:33.452796Z·HEAD Unreal0d5f039d/MD792e6079 유지, 두 Git diff--check0·엔진0이다. 기존117개 dirty 항목을 리셋하지 않았고 Commit/Push는 없다.

STATUS/WORKBOARD·시험/로비/미션 현재 가이드를 갱신했다. STATUS30454B·WORKBOARD29333B로30KiB 아래여서 이번 아카이브 이동은 없다. maintain-space로 기존 진행/테스트/Blueprint/안내4페이지의 관련5블록만 수정했고 sequence58/40/41/20 및 저장 후 기대 본문 일치를 확인했다. 새 Page·원시 로그/자산/비밀값 업로드·기획/과거 기록 정리·Trello/Figma·권한/예약 변경은 없다. 미커밋 자료는 사용자가 전달하기 전 다른 PC/GitHub에 자동 반영되지 않는다.

## 2026-10-20 — 스포이드 목표 연결·배치형 나침반 매니저 (C PC Codex)

사용자가 BP에서 대상 변경/스포이드 설정 가능 여부와 배치형 목표 나침반 매니저를 요청했다. 기존 Event/수량/시간은 DA 편집이 가능하지만 대상은 주로 TargetId 문자열이었다. 이를 전부 스포이드였다고 답하지 않고 `ADroneMissionTargetManager`·`/Game/Drone/Managers/BP_DroneMissionTargetManager`를 추가했다. 규칙 DA의 월드 참조 대신 레벨 인스턴스 TargetBindings(ObjectiveId 또는 TargetId/Targets Actor 배열)가 실제 대상 참조를 소유한다. MissionId는 같은 맵의 적용 미션 필터다. 기존 Director는 Controller가 생성하고 새 매니저만 사용자가 배치한다.

명시적 목록은 판정과 나침반을 함께 바꾸며 선택되지 않은 옛 태그 대상은 거절한다. 빈 명시적 연결은 기존 Tag 대상으로 대체하지 않는다. 매니저/연결이 없으면 기존 Tag 판정은 그대로다. 코스 선택 시 실제 Lap Recorder도 같은 코스로 바꾼다. 마커는 기존 기체 Yaw 나침반에 맞춰 정면 중앙·좌우 방위·뒤/범위 밖 가장자리 방향과 거리/이름을 표시하고 HP0·제거·목표 전환/종료 때 숨긴다. 코스는 현재 Gate를 가리킨다. 기본8개/매니저·전체16개 상한, Actor Tick 없이0.5초 캐시·HUD1초 매니저 발견이며 프레임에는 제한된 좌표만 읽는다. 가까운 글자 겹침은 글자만 생략한다. 대상 BP의 체력/Recon/Payload 기능·DA 수량/시간까지 자동 생성하지는 않는다. Production 맵에 자동 배치하지 않았다.

새 전용 `TestMap/Lvl_MissionCompassTest`·로비 숨김 `DA_Mission_CompassTargetDemo`를 생성했다. 태그 없는 A/B 두 개는 실제 저장된 BP 매니저의 Actor 참조로 연결하고, 뒤 DECOY에는 옛 태그만 붙였다. BP/DA/이 새 시험장 외 기존 자산/맵을 재생성하지 않았다. 생성 도구 첫 오류는 MissionMap에 World 대신 SoftObjectPath를 넣은 것, 다음 오류는 Python native type과 Class 객체 비교였다. 자기 작업으로 생성된 빈 맵을 백업하고 빈 맵 클래스/정확한 부모 경로를 확인한 복구 경로로 완료했다. 새 시험장 TextRender는 최종 명명 인자 yaw180/roll0으로 바로잡고1280 재검증했다. 기존 맵 복구/변경이 아니다.

첫 기능 Build46.29초·테스트 추가14.57초·코스 연결5.19초·검사 보강5.80초 성공. Build5는 검사 정수형 오버로드 오류로 실패했고 int32 명시 후 최종 Build6 **5.81초 성공**이다. 실패 뒤 구 바이너리로 시작된 불완전 검사는 자기 PID/로그를 확인해 중단·제외했다. 최초 경량 검사3/4의 사망 실패는 임시 월드가 ActorsInitialized 이전이라 Actor::ProcessEvent가 동적 콜백을 무시한 것이었다(엔진 Actor.cpp 확인). 검사 한정 Editor 실행 가드를 넣었고 생산 사망 로직은 바꾸지 않았다. 실제 PIE의 대상 사망/진행은 그 전에도 통과했다.

최종 경량 **4/4**(17.3초·최소9095MB): CompassBearing·TargetPickerBinding·기존 ObjectiveRules·FlightHUDKitLayout. Actor 선택 프로퍼티의 인스턴스 편집/Actor 타입, 정면/좌우/뒤/359→0, 옛 태그 거절·빈 연결 보호·중복 사망 방지·코스 Recorder 일치를 확인했다. 실제 BP/스포이드 참조는 프로그램으로 저장한 뒤 새 프로세스에서 읽어 검사한 것으로 사람이 스포이드를 클릭한 실기 Pass는 아니다.

전용 맵 실제 렌더 PIE는 두 폭 모두 성공: **client1280×722 / PNG1286×760**, **client1920×1082 / PNG1926×1120**, 각31.4초·최소7400/7158MB·Private7908/8067MB. 처음960px 캡처는2해상도 근거로 쓰지 않았고, 창 Resize 뒤 테두리6px를 게임 해상도와 잘못 비교한 검사도 수정해 viewport 폭과 바깥 PNG를 분리했다. 실제 저장 BP/대상2개 재로드→정면/회전→옛 태그 DECOY 사망 진행0→A 사망1/2/마커1→B 사망 성공/마커0을 확인했다. 명명 Yaw로 글자를 최종 수정한 현재 맵도1280에서31.4초·최소7360MB 통과했다(반복을 신규 시험으로 합산하지 않음). 자동 직접 피해/회전 검사이며 손 조종·실제 무기 조준/장치 Pass가 아니다. 기존 실제 TUT_Circle_Gate도35.5초·최소6069MB 통과해 매니저 없는 Tag/원형 완주 경로를 확인했다. 이미지로 중앙/옆 마커·1/2/마커 감소 및 최종 TargetA/B 글자 방향을 확인했다.

근거 정본은 `C:/URproject/drone/Saved/Automation/CodexMissionCompass_20261020/index.json`. 이전 실패/제외 실행·최초960 그림·수정 전 C++4개/새 시험장 사본을 `Saved/Backups/CodexMissionCompass_20261020` 및 실행별 폴더에 보존했다. 기존 제품 맵 변경0·새 시험장1개, 사용자 진행도481B/UTC2026-10-19T16:16:33.452796Z·HEAD Unreal0d5f039d/MD792e6079 유지·Commit/Push 없음. Camp/자유 게이트/Story 전체 콘텐츠·손 조종/패키징 한계는 기존과 같다.

현재 절차를 DRONE_MISSION_FRAMEWORK_GUIDE의 스포이드 목표 연결과 나침반 절에 정리하고 STATUS/WORKBOARD·시험 가이드를 연결했다. STATUS30586B·WORKBOARD29675B로30KiB 아래라 아카이브 이동은 없다. maintain-space로 기존4페이지 현재5블록만 갱신했고 sequence59/41/42/21·저장 후 기대 본문 일치를 확인했다. 새 Space Page·원시 로그/이미지/자산/비밀값 업로드·Trello/Figma·예약/권한 변경은 없다. 미커밋 코드/문서는 아직 다른 PC/GitHub에 전달되지 않았다.

## 2026-10-20 — 실제 Story 배치·M2/3 분리·Nav 저장·Camp 저메모리/재밍 조정 (C PC Codex)

사용자 Push를 실제 원격과 대조해 Unreal2a7b0418·MDe160207c 수신/초기 Clean을 확인했다. 객체명/폴더의 위치 표시, M1 주목표, M2/3 분리, 헬기포트 출격·나침반·NPC NavMesh와 시작/목표 사진 요청을 이어 수행했다. 기존 파일은 Saved/Backups/CodexMissionLayout_20261020에 보존했다. 팀원 Production Lvl_DroneTraining은 저장/재생성하지 않았다. 원본 MilitaryBase SHA256은 26D27CCB2F565090D6390151251BC1D29A78EBB70BA2A2EEB587F987BFBF53E4로 동일하다. 사용자 진행 저장481B·UTC2026-10-19T16:16:33.452796Z도 유지했다.

M1은 기존 M_Target XY를 유지한 M01_MainTarget_Delivery를 Shack의 표시 지붕 위로 올리고 DROP 글자를 켰다. M_Enemy/M_Turret 재료를 쓰던 오해하기 쉬운 M_Start 표식은 Editor에 보존하고 플레이 표시/충돌만 끄며 기존 병사6명·표식 위치 고정 포탑2개를 연결했다. M2/3은 원본 Base를 저장하지 않고 Editor Save As로 Missions/Lvl_Story02_Intercept·Lvl_Story03_VeilBreaker 독립 사본으로 분리했다. 첫 AssetTools World 복제는 전환 시 GC 오류가 나서 완료로 세지 않았고 원본 해시를 확인한 뒤 Save As 방식으로 대체했다. M2는 실제 배치 차량과 기존 BP_DroneVehicleSplineRoute를 직접 연결해 임시 직선60m를 제거했다. M3는 기존 레이더를 유지하고 해당 사본의 패드만 M_Start_Mission3 XY 지면으로 옮겼으며 재밍 진입/완전 이탈 규칙은 유지했다.

Controller는 Tutorial/Story의 실제 SM_helicopter_base 메시 경계 윗면+52cm를 출격점으로 사용한다. 첫 LOS 고정 관찰/후진/접지 예외와 다른 미션 귀환 제거를 유지한다. 각 맵의 BP_DroneMissionTargetManager가 실제 목표와 판정/나침반을 함께 연결하며 DA의 중복 상대좌표 목표 Spawn을 제거했다. 새로운 최종 시나리오·수량·기체교대·엔딩을 확정한 것은 아니다.

NavMesh는 실제 NPC 범위+지면으로 제한하고 Dynamic/ForceRebuildOnLoad/타일 작업2를 사용한다. 플래그만 바꾸고 저장한 중간 검사는 새 로드에서 타일0·전원 투영 실패였다. 이를 통과로 재사용하지 않고 Diagnostics.StoryLayout.BakeNavigation을 추가해 Build→EnsureBuildCompletion→유효 타일/전원 투영 확인→해당 맵 저장으로 수정했다. 중복 Recast는 만들지 않는다. 최신 Build는 잘못된 void LoadMap 사용을 수정한 뒤5.11초 성공이다. 최종 M1/2/3 새 프로세스 RHI 검사는51.5/44.7/45.6초 Pass, 최소 물리 RAM12613/12252/11844MiB·Private피크11714/11459/11790MiB, 타일486/523/523·NPC6/8/8 전원 투영이었다. 이전 실패/중간 보고서는 삭제하지 않았다.

Camp 실행 전 승인받은 Chrome·Discord·Steam·Epic·Claude·NexonPlug·카카오톡·NVIDIA Overlay를 종료했다(Overlay는 UE 실행 시 재시작). GitHub Desktop·Codex·ChatGPT는 유지했다. 그래도 일반 시작 기준20,480MiB가 부족해 사용자가 별도 저메모리 검사 모드를 승인했다. 이 모드만 시작16,384MiB·RAM/커밋4,096MiB 중단 보호, Asset/Texture 준비1·예상 작업 예산3GiB·Texture/Shadow1·Pool768MiB·Grass0.25/Foliage0.5를 이번 실행에 적용했다. 일반 기준/원본 맵 기본 화질은 낮추지 않았다. Editor PID20260 한 프로세스를 MCP로 조작했고 마우스 제어·전체 쿠킹/패키징·DDC 삭제는 없다. 최초 로드 private 관측 피크24,335MiB·후속 Process PeakPaged24,476MiB는 프로세스 커밋량이며 물리 RAM 자산별 귀속/정상 화질 개선율이 아니다. 기존 텍스처·준비 동시성 수리와 구분한다.

실제 Camp에는 헬기포트나 객체명 목표 폴더가 없고 NPC27·자동포탑18개·재머8개가 있었다. 동일 SM_helicopter_base_01을 추가하고 기존 고정포탑 Emplaced_C_24/18/14를 M04_MainTarget_Turret_01/02/03으로 이름/Tag/매니저 연결했다. 기존 배치/나머지 방어 시설은 보존하고 현재3개 파괴 규칙·240초·기체 선택은 바꾸지 않았다. 새 Nav1605타일·NPC27/27을 확인했다. Camp BakeNavigation은 기능 assert가 맞고 저장됐지만 MCP HTTP socket_send_failure가 함께 기록돼 전체 Fail로 보존한다. 이후 실제 로비→Camp 출격·매니저1/표식3·전원 투영·실제 목표 피해/파괴→클리어 검사는 오류/경고0으로 통과했다.

첫 M4 화면은 재머 중첩으로 NO SIGNAL이었다. 사용자 정정에 따라 시작점을 재밍 회피 위치로 옮기지 않고 **Camp의 Radar8개 인스턴스만** 반경150m/최대25m→반경20m/최대4m로 조정했다. 출력1/활성/높이30m·M3/BP 기본값은 유지한다. 사용자에게 원본에는 패드가 없음을 설명했고 ‘현재 포트 위치 유지—재밍 조정 전 위치’를 확인받았다. 최종 위치(9700,6500,6105.43cm)·회전0·Scale0.3이며 기존 미션과 같은 패드 크기다. DA 기준 출격(9700,6500,6212.90cm)은 실제 기체 충돌/착지 보정을 받을 수 있다. 크기 수정 중 MCP 부분 Transform이 누락 Location을0으로 해석한 일시 상태는 full Transform으로 즉시 복원했으며 그0좌표는 저장하지 않았다.

재밍 조정 후 시작 신호100%/NO SIGNAL 해제와 목표 파괴→성공을 확인했고 최종 크기 저장본도 StoryM4 **70.41초 Success·오류/경고0**, NPC27/27·1605타일 통과했다. 마지막 검사 시 Dynamic Nav12타일은 갱신 중이었으므로 ‘Nav가 전혀 다시 빌드되지 않는다’고 해석하지 않는다. 경량 MissionAssets/CompassBearing/TargetPickerBinding은 마지막0.36초 **3/3** 통과다. 다만 실제 화면에는 Lumen Surface Cache 초과 경고와 출발 적 피격/카메라 흔들림(HP70)이 보인다. 자동 성공과 주행 동선/손 조종·정상 화질/장시간 안정성·연출 완성을 구분하고 이 문제들은 남겼다. 무작정 Lumen 캐시 예산을 늘리지 않았다.

근거 정본은 `C:/URproject/drone/Saved/Automation/CodexMissionLayout_20261020/index.json`, 실제 시작/목표8장은 같은 폴더 Screenshots/StoryM1~4_Start/Target.png다. 마지막 M4 시작 캡처에는 실제 피격 흔들림이 있으므로 예쁜 무피격 사진/플레이 완성 근거로 쓰지 않는다. 실패/중간 실행은 형제 CodexMissionLayout 폴더에 보존하고 중복을 고유 통과 수로 합산하지 않는다. 한 맵 감사가 DA soft World를 읽으며 여러 맵을 로드하던 메모리 문제도 수정해 명시 단일 맵 감사는 DA World 읽기를 건너뛴다. 초기 보호 중단과 수정 뒤 단일 감사 결과를 구분한다.

사용자의 수동 시작점 질문에 현재 코드의 패드 우선·DA Yaw 우선·여러 패드일 때 DA 근처 선택을 설명하고 Mission 배치 가이드에 절차를 추가했다. Camp 에디터는 켜 둔 채 M04_SM_helicopter_base_01을 선택했고 추가 무거운 검사는 하지 않는다. 초기900초 러너 보호를 같은 소유 PID의 ContinueGuard.ps1로 먼저 넘겼으며 RAM/커밋4GiB 보호는 유지한다. 원본 Base/Training·진행 저장 보존, Commit/Push 없음. STATUS30,559B·WORKBOARD29,578B로30KiB 아래라 이번 아카이브 이동은 없다. maintain-space는 기존 진행/시험/BP 페이지의 현재4블록만 갱신·읽기 재확인(sequence61/42/43)하고 수동 시작점 절차만 BP44로 보강·재확인했다. 별도 페이지·원시 로그/자산/이미지 업로드·공유 권한·Trello/Figma 변경은 없다. 미커밋 코드/맵/MD는 아직 다른 PC/GitHub에 전달되지 않았다.

## 2026-10-20 D PC — 조작 그림·기체 사진·튜토리얼 권장창 개선

- 사용자 요청: 최신화 후 겹치는 키 글자를 없애고 번호/아래 범례로 정리, RC LT/RT를 세로 스틱 형태로 변경, 바닥 있는 기존 사진 교체·없는 정찰 사진 촬영/연결, 튜토리얼 권장 안내 한글화. Codex가 직접 수행했다.
- 기준: 실제 D:\JGY\project\drone HEAD=origin/main `6553f72f`, MD `dd16749`. Fetch 후 양쪽 ahead/behind0/0으로 추가 수신 없음. 현재 변경은 로컬 미커밋이며 새 Commit/Push·Trello·공유 권한 변경 없음. 수신 전 C PC 검증을 이번 실행으로 세지 않는다.
- 조작 안내: `BuildDeviceArtwork`의 L/R·OPTIONS·LT/RT 등 글자/외부 칩/지시선을 제거, 26px 번호 배지로 정리했다. `FitDiagramArea`가 저장된 WBP의 옛 그림 자식도 갱신한다. 하단 키/동작 범례·입력 매핑·다른 Designer 설정은 유지한다. 새 실제 위젯 트리 번호 전용 검사는 수정 전 Fail을 재현(red.log), 수정 후 ControlsGuide Success다.
- RC: 기존 LayoutMatched 원본을 built-in image_gen으로 편집, 본체/버튼 배치 유지·양 어깨에 세로 금속 토글/검정 손잡이를 적용했다. 실제 RGBA alpha 모서리0을 확인하고 `SourceArt/Controls/T_Controls_RC_StickSwitch_20261020.png`와 최종 prompt 파일/manifest SHA·앵커를 보존했다. 새 Texture와 WBP_DroneControlsGuide.rc_device_image를 연결, 옛 PNG/Texture는 보존했다.
- 기체 사진: 기존 T_SelectDrone_FPV를 PNG로 읽기 전용 Export해 사용자 첨부의 바닥 사진과 일치함을 확인했다. 정찰은 BP_DroneScoutIntegration(보이는 메시6), FPV는 BP_DroneFPVIntegration(메시5)을 각 실제 DA의 PawnClass로 불러왔다. 바닥 없는 격리 PreviewScene·푸른 unlit 배경·3/4 카메라에서1536×864로 촬영했다. 첫 검정/체커 배경 결과는 채택하지 않았고, 물리 노출 해제/배경 보강 뒤 파란 배경 픽셀 검사·육안 확인을 통과했다. 제품 맵 촬영/저장은 없다. 새 `T_SelectDrone_{Scout,FPV}_Studio_20261020`을 두 DA.SelectImage에 연결했다. 재사용 원본/SHA/클래스 근거는 SourceArt/Selection과 studio.log, 가져오기 결과는 apply-presentation.json이다. 다른 기체의 기존 사진은 유지한다.
- 권장창: Native/저장된 Designer 바인딩 두 경로에서 제목 "튜토리얼을 먼저 해 보세요", 본문, "튜토리얼로 이동"/"계속 진행" 버튼에 NSLOCTEXT를 적용했다. 패드 이동·확인·1회만 표시 정책은 유지한다. 최초 실행은 phase2 시간 초과 Fail이며 렌더 준비 영향은 추정이다. 소스 수정 없는 warm 재실행과 최종 UI 실행에서 성공했다.
- 검증: DroneEditor Win64 Development 최종 Build 성공10.32초(build-final.log, 엔진 기존 경고 별도). 실제 D3D11 RHI 최종 UI4/4 Success·테스트 경고/오류0(final-ui-report/index.json): ControlsGuide, TutorialHintPIE, TrainingPresentationCapture.1280/1920. 사진 진단1/1 Success(studio-report, 엔진 r.MotionVectorSimulation 경고1). 일반 시작 로그의 UE 자체 오류 테스트 메시지는 제품 테스트 Fail로 세지 않는다. 첫 UI 실행3/4와 warm1/1을 최종4/4에 합산하지 않는다.
- 해상도: PIE 창이 모니터에 맞춰 줄어드는 것을 확인해 캡처/측정을 FWidgetRenderer의 실제1280×720/1920×1080 타깃으로 변경했다. PNG 크기/번호 겹침0·그림 비율·범례 경계 확인. 캡처 읽기 감마 옵션만 보강 후 두 크기2/2 재검사(capture-report), 중복을6종으로 합산하지 않는다. 원시 근거는 Saved/Automation/ControlsRefresh_20261020, 그림은 Saved/Automation/CodexTrainingUI와 Title/tutorial_hint.png다. 실제 패드/비행·청감·제품 맵 전체·패키징 Pass는 아니다.
- 보존: 시작 전 PayloadTarget BP·TUT_Delivary 맵 등 관련 자산을 Saved/Automation/ControlsRefresh_20261020/before에 백업했다. 기존 사용자 수정2개는 작업 후 SHA256 일치, Production Training 미저장. 초기 열린 Editor는 D3D12 GPU 크래시 로그로 종료됐으며 이번 작업이 GPU 문제 전체를 해결한 것은 아니다. 후속 검증은 D3D11로 수행했다.
- 문서: STATUS의 이전 면접/참조0 절 원문을 기존 docs/history/archive/STATUS_2026-10.md에 보존했다. 정리 전30559B/140줄→정리 후29050B/134줄, 최종 현재 상태 반영29160B. WORKBOARD 최종29541B, 두 문서30KB 이하. 기존 docs/README 색인 링크 유지. 주제 가이드는 현행 번호/사진/한글 경로로 갱신했다.
- Drone Space: 기존 진행상황과 다음 작업(sequence62)·Blueprint 조정과 팀원 가이드(sequence45)를 해당 ID/hash로 갱신했다. 모든 연산 적용 후 content 스트림 재조회 hash 일치 확인. 새 페이지 생성/권한 변경 없음. 링크: https://chatgpt.com/space/page_a81d11314f60819188530a4ea2ed4663 , https://chatgpt.com/space/page_90d36613770c819182701fa5869ba17a . 로컬 미커밋 파일/로그를 GitHub나 다른 PC에 배포한 것은 아니다.

- 마무리: 진행 Page sequence63에서 최초 시간 초과 원인 문구를 추정으로 명시하고 재조회 일치를 확인했다. 최종 근거 묶음은 Saved/Automation/ControlsRefresh_20261020/final-evidence.json. D3D11 Editor를 FrontEnd로 다시 열었다(PID6276).

## 2026-10-20 — HUD Designer 한 WBP 통합 (D PC Codex)

사용자 요청: HUD 간격/배치와 이미지 파츠를 WBP에서 쉽게 조정하도록 분산 구조 정리. 작업 시작 Unreal HEAD/origin/main a645c793 Clean, MD dd16749와 앞선 UI 작업 문서 변경 보존. 작업 중 외부 Git 변경으로 HEAD/origin/main 547efd1f·0/0이 됐음을 재조회했다. a645c793..547efd1f는 Content 변경이며 Source/Config 차이 없음. Codex는 이번 작업에서 Fetch/Pull·Commit/Push를 실행하지 않았다.

구현: WBP_DroneFlightHUDKit 한 트리에316위젯·01~13 표시명 구역과99 접힌 호환 그룹. MissionObjective/Countdown/조종 입력을 실제 주 트리 파츠에 연결하고 별도 뷰포트 중첩을 없앴다. 기존 이벤트/시간/기록/입력 API와 독립 WBP 폴백 유지. UGV 조준선13개·화면 모서리·고도 값 테두리4개·나침반 기준선/포인터를 UImage로 분리. 이동 눈금은 WBP Template Brush/크기/색/Font를 읽고, 간격 배율은 기존 Class Defaults를 사용한다. 좌우/하단 안전 여백32px·나침반680px. Designer 글자 최소 크기 강제는 native fallback에만 남겨 사용자 크기/색/배치를 보존한다. 일반 native Controller도 SharedHUDWidgetClass로 주 WBP 사용. Countdown 해제 시 두 타이머와 표시를 정리한다. 고도 테두리 Canvas의 Overlay 수직 Fill도 수정했다.

자산 저장: 주 HUD WBP 하나만 저장. 기존 FlightHUD/ControlInputDisplay/Objective/Countdown4개는 before-manifest SHA256 일치, Production Training 등 맵 저장 없음. 이전242위젯 상태의 STATUS 문구는 당시 기록으로 보존: “**구현됨(10/16 D PC Claude)**: WBP 15개를 /Game/Drone/UI/WBP/{FrontEnd,Mission,HUD}로 정리하고 이동 참조 3건 복구. FrontEnd 6·Mission 7·HUD 2(구 FlightHUD 프로토타입/입력 표시). 저녁에 `WBP_DroneFlightHUDKit`(242위젯) 생성·Mission PC 연결 완료. 화면 UI·HUD는 WBP 편집 가능(로비 카드 버튼 개별 위젯·런타임 로비 좌표 예외). `HudKit*` 이름 바인딩으로 Designer 위치/글꼴/색 유지·값/상태색만 코드 갱신.” 현재 편집 절차는 DRONE_MISSION_FRAMEWORK_GUIDE의 HUD 편집 정본으로 옮겼다.

검증(각 보고서는 별도 실행이며 합산 통과 수로 쓰지 않음):
- DroneEditor Win64 Development 마지막 build-verified.log Succeeded12.24초. Editor가 없는 상태에서 전체 Build.
- 최초 read-only 계약 검사는 파츠 누락으로 의도대로 Fail. 첫 적용2회는 UE5.8 위젯 GUID/복사 Panel Outer 문제로 handled ensure가 나서 Fail. 명시적 루트+하위 위젯 이관·폐기 위젯 transient 이동·GUID 매핑 갱신 후 organized-report5/5 Success, 경고/오류0(자산·KitLayout·Telemetry·Designer·정리도구).
- 최초 D3D11 render-report에서 시작 안내·레이싱 Countdown·기존 입력3종 Success. Designer 캡처는 테스트의 abstract UUserWidget 생성 문제로 Fail, MissionEntry는 재출격/복귀30초 시간 초과 Fail. 캡처를 RootWidget 직접 렌더·Slate 강참조·LDR 타깃으로 수정했다. 제품 Flow 규칙/판정은 바꾸지 않았다.
- final-render-report5/5 Success, 경고/오류0: 시작 안내·레이싱 Countdown·기존 입력·Designer 계약·정리도구. 최종 Brush/프레임 보정 뒤 parts-final-report2/2 Success, 경고/오류0.
- Designer 계약은 저장 트리에 중첩 UserWidget이 없고, 변경한 위치/9px Font/색이 Initialize·데이터 갱신 후 유지됨을 검사했다. 실제 주 HUD 임무/Countdown 텍스트 갱신·입력 커서와1280×720/1920×1080 UGV 렌더, Designer 전체 미리보기를 확인했다.
- MissionEntry 단독 NullRHI는 Success35.83초(HTTP 연결 경고3), 이어 단독 D3D11은 Success39.10초(같은 HTTP 경고1). 재출격·실패 후 로비 복귀3회 시나리오가 통과했다. 최초 RHI 실패 원인은 확정하지 않았으며 준비/시간 영향이라는 추정을 제품 결함 없음의 증명으로 쓰지 않는다. 초기 실패 보고서도 보존한다.

증거는 Unreal Saved/Automation/HudDesigner_20261020의 before-manifest.json·hierarchy-after.tsv·각 report/index.json·build-verified.log·runtime-ugv-1280.png·runtime-ugv-1920.png·designer-master-1920.png다. 실제 사용자의 패드 조종·창 이동·전체 플레이·패키징 Pass는 아니다. 원본 맵·기체 입력 매핑·미션 규칙·Trello·공유 권한·예약 자동화는 변경하지 않았다. MD/기존 Drone Space 갱신 후 읽기 확인은 아래 마무리 기록을 따른다.

마무리: Drone Space 진행상황/Blueprint 가이드 기존2개 Page의 관련4블록을 ID/hash 보호로 수정(각 sequence64/46), 같은 content stream 읽기 재조회로 기대 본문 일치 확인. 새 Page 없음. STATUS29,146바이트·WORKBOARD29,650바이트로30KB 이하 유지. 상세 편집 절차는 가이드에만 두고 완료 이력은 이 절에 기록했다.

Editor 마무리: /Engine/Maps/Entry로 GUI Editor를 열고 WBP_DroneFlightHUDKit의 Designer·01~13/99 계층 표시를 실제 창에서 확인했다. 자산 탭은 저장 완료 상태이며 편집할 수 있도록 열어 두었다. 이 확인은 실물 조종 Pass가 아니다.

## 2026-10-20 — 전체 WBP 편집 정본·목표 매니저 배치·게이트 재질·M1 영상 (D PC Codex)

사용자 요청: HUD처럼 로비부터 모든 화면을 Designer에서 찾고 문구/간격/이미지 파츠를 조정, 한글·미선택 투명도/선택 강조, 목표 스포이드/조건 +와 Tutorial/Story 실제 배치, 게이트3상태 MI 정리, 배달 TUT_Delivary_2 연결, 헬기포트 외곽/9시 정리 후 자료 누락 확인. 후속으로 시작 버튼4곳 우하단·제공 UGV JPG·M1 MP4/Esc·사진 상자/레이싱 Fill을 추가 승인했다. 사용자가 미저장 배달2 맵을 직접 저장/종료한 뒤 Build/자산 작업을 진행했다. Unreal HEAD/origin/main547efd1f·로컬0/0, MD dd16749. 이번 후속 Fetch/Pull·Commit/Push·Trello·공유/예약 변경 없음.

**구현과 자산**

- `/Game/Drone/UI/WBP`22개를 정리했다. FrontEnd Root/Entry는15개 호스트이며 별도 TitleScreen/Lobby/Briefing/TutorialRecommendation/MissionListItem/Cinematic을 실제 연결했다. 제공 Select_UI/TitleKit 아트와 기존 그래프/내부 이름·진입 API를 보존한다. 목록 번호가 모두01이던 문제·권장창이 계속 뜨던 문제·저장 화면 배경/폰트/위치가 런타임에 재작성되던 예외를 수정했다. 정적 TextBlock·Canvas/SizeBox/Slot Padding·Image Brush·버튼 Style로 편집하며 동적 문구는 DA 또는 TextOverrides로 조정한다. 일반 포커스/호버·선택1, 미선택0.55, 반복 줄 ListItemPadding. HUD 외 간격은4px/글자 최소12로 명시적1회 정리, 이후 강제하지 않는다.
- 조작 안내는 세 장치의 Diagram/Legend를 모두 저장했다. 번호만 그림 위에, 키/한글 설명은 아래 범례이며 RC 세로 스틱 그림을 유지한다. 탭 전환 시 파츠를 다시 만들지 않는다. 기존 HUD Kit13구역/이미지 파츠·사용자 위치는 보존했다. 이번 시작/종료 HUD inventory는312위젯이며 이전316 기록은 당시 이력으로 남긴다.
- 시작4곳(로비/브리핑/기체 선택/출격 안내)은 앵커/정렬(1,1), 위치(-80,-40),300×80. 사진3곳 외곽600×360·안쪽14px·모서리24×2 이미지8개, 레이싱/훈련 사진은 Fill. UGV 큰 사진은 전체 기체를 보이게 Fit 옵션을 둔다. 캡처 검토에서 기체 선택 루트가 저장된 Collapsed 상태 때문에 검게 나오던 문제를 찾아 상태 갱신이 authored Root도 보이게 수정했다. 이미지 Brush 크기는 비동기 기본32가 아닌 실제 ImportedSize를 사용한다. 영문 ‹ Back 잔존도 한글로 고쳤다.
- Tutorial 폴더9맵(TUT_LOS/Hover/Forward_Gate/Circle_Gate/FreeGate/FPV_Target/Delivary/Delivary_2/UGV_Turret)·Story4맵에 매니저1개씩, Outliner 이름 BP_DroneMissionTargetManager_목표연결/폴더 Drone/Managers. 목표 문구·Event·횟수·시간·Story 조건/ID 배열과 대상 스포이드·+를 노출했다. 조건 적용 버튼은 연결된 DA를 갱신, 대상 참조는 맵에 저장한다. 전역 실패/재출격은 DA에서 조정한다. 준비 버튼은 기존 비어 있지 않은 대상/Transform을 보존하고 RuntimeSpawnActors를 미리 배치·중복 생성 생략을 연결한다. 기존 클래스별 runtime tag도 Course/FPV 실제 액터에 반영했다. Drone.EditorPlaced는 runtime 지면 스냅/호버 재배치를 건너뛴다.
- 배달 DA MissionMap은 사용자 결정 `/Game/Drone/Maps/Tutorial/TUT_Delivary_2`. 직전 사용자 저장본을 백업한 뒤 목표만 보완했다. 옛 Delivary·자유 게이트 준비 중·숨김 시험 항목·기존 ID를 유지한다. Production Lvl_DroneTraining은 작업 대상/시험 저장에서 제외했다.
- `/Game/Drone/Tutorial/Materials`의 기존 재질 옆 `M_DroneTrainingGate_States` 노드 그래프(Color/EmissiveStrength/Fresnel)와 MI_DroneTrainingGate_01_Waiting/02_Current/03_Passed. 청회색#68889F/0.35, 노랑#FFD54F/3, 초록#56B896/0.75. BP/배치 Gate는 MI 색 모드이며 수동 MI 변경은 반복 도구가 덮어쓰지 않는다. 기존 private MID 저장 수리 유지.
- UGV 제공 원본 `Downloads/1792467754744.jpg`는 SourceArt/Selection/UGV_User_20261020.jpg로 보존·Texture `FrontEnd/UI/SelectUI/Drones/T_SelectDrone_UGV_User_20261020`를 DA_Drone_GroundUGV_Greybox.SelectImage에 연결했다. MP4는 byte 동일 `Content/Movies/Mission_briefing1.mp4`(28,004,924B), FileMediaSource `FrontEnd/Media/MS_Mission01_Briefing`의 상대경로 ./Movies/Mission_briefing1.mp4를 DA_Mission_Story_GoldenTime_Test.BriefingAsset에 연결했다. M1 로비 확정→영상→기존 브리핑이며 Esc/B·실제 종료/오류 시 복귀한다. 재생 중 기존 대사/포커스를 멈추고 브리핑을 재개한다. WBP_DroneCinematic·Controller 하드 참조·Movies 패키징 목록 저장, 실제 패키징은 미실행.

**헬기포트와 누락 조사**

SM_helicopter_base_01·MI_helicopter_01·MI_exterior_chunk_01·M_Master는 수리 전 HEAD LFS 원본 SHA와 일치했다. Nanite/원본441,028 triangles에 외곽이 있지만 Auto fallback9,423 triangles가 얇은 프레임을 없앴다. RelativeError0만 설정한 첫 가설은 Auto에서 효과가 없어 원본 복원, transient source/noNanite와 명시적 전체 fallback 렌더를 비교했다. 최종 기존 메시 경로에 Nanite 유지·GenerateFallback Enabled/Target PercentTriangles/Percent1.0/Error0 저장. 새 프로세스 fallback441,028==source441,028 및 helipad-repaired.png 외곽 전체를 확인했다. 원본 geometry/material/배치 Transform 수정 없음.

file-presence-audit.json(14:04 KST): 추적 Unreal 자산9753개 누락0·LFS 포인터0·추적 삭제0. 이번 작업에서 삭제하지 않았다. 10/16 storage-audit-20261016 manifest의45.860GiB 정리는 다른 프로젝트 중복 백업/컴파일 캐시였고 현재 Drone Source/Content/Saved/Git 삭제가 아니었다. 10/16 stash 복구/푸시 근거도 이전 WORKLOG에 있다. 이 조사는 파일 존재·기존 원본 일치 범위이며 ‘9시 메모리 정리’의 모든 상태 변화를 단정하지 않는다. 이번에 발견한 런타임 레이아웃 덮어쓰기/미반영/비표시를 수리했다. 백업은 Saved/Automation/AllWbp_20261020/before와 manifest들이다.

**빌드/자동 검사 — 실행별 별도 근거, 통과 수 합산하지 않음**

증거 루트 `D:\JGY\project\drone\Saved\Automation\AllWbp_20261020`. GUI Editor 저장/종료 상태에서 DroneEditor Win64 Development Build18 Succeeded16.33초(직전 Build17 12.71초·Build16 12.20초). MSVC14.51 preferred-version 경고는 유지한다. Build12의 delegate 이름/헤더 컴파일 오류는 Build13에서 수리한 이력이다.

| 보고서 | 결과/검사 범위 |
|---|---|
| organized-report | 2/2 Success·0 errors/0 warnings, 저장/Designer 계약. 초기 UE5.8 GUID·transient delegate/navigation 복사 실패는 보존 후 수리 |
| final-ui-report | 11/11 Success·0/0, Gate5·조작 안내·정리/자산·목표 편집·현재 UI 계약 |
| corner-render-report | 5/5 Success·0/0, 시작4곳/조작 위치·SelectionControlLayout/SelectUI·포트 비교. Selection 검정 캡처를 이후 검토에서 발견했으므로 이 보고서를 기체 선택 외형 Pass로 쓰지 않음 |
| presentation-final-report | 11/11 Success·0/0, 포트 영구 수리 재로드/렌더·UGV DA/사진/프레임·Gate·OpeningMovie 연결. 당시 검정 Selection 캡처 한계 동일 |
| movie-final | 미리보기 도구가 CreateNewMap GC 뒤 raw Flow를 참조해 access violation. 실제 영화 검사 시작 전 실패·자산 저장 전이며 로그 보존. StrongObjectPtr로 Instance/Flow 수명 보장 후 재검사 |
| movie-final-2-report | 3/3 Success·0/0: OrganizeAllDesigners/AllDesignerContract/Mission01MoviePIE. 실제 WBP 루트 Visible·ImportedSize·UGV/지도 프레임·1280/1920 캡처, 실제 디코더1920×1080/14.356초·Slate Esc down/up·끝0.3초 seek 뒤 실제 end event→기존 브리핑/조기 맵 로드0 확인. mission01-cinematic-playing.png·UGV 캡처 시각 확인 |
| mapped-final-report | 4 Success/2 Fail(6개): 원형7Gate 실제 통과·FPV 실제 충돌 파괴·WBP 정리/계약 Success. Hover/Payload는 목표 완료 검사는 통과하고 옛 ‘runtime 새 생성 수=1/2’만0으로 Fail. 미리 배치한 목표를 세지 않는 검사였음 |
| mapped-final-2-report | Hovering/Payload 2/2 Success·0/0. 기존 검사에 계획 클래스/Tag 일치·Drone.EditorPlaced 액터와 runtime 추가를 함께 세어 누락/중복을 검사하도록 수정했다. 배달 실제 로비→TUT_Delivary_2→기체 선택→빈 집게/실제 집기/투하/성공, 호버3초 완료를 확인. 기존 두 Fail 보고서는 보존 |

맵 PIE 하네스는 팀원 외부팩 로그 경고/오류를 검사 사건에서 제외하고 명시적 assertion으로 판정한다. 위0/0은 해당 보고서 사건 수이며 엔진 전체 raw 로그에 경고가 없다는 뜻이 아니다. 실제 조종 대신 위치/피해/키 이벤트 주입을 사용했다. 사용자 패드·손 조종/전체8수업/Story 최종 분기·청감·패키징 Pass는 아니다. 마지막 Source/Config/Tools·MD `git diff --check` 오류 없음(일부 LF→CRLF 안내).

**편집창/문서 마무리**

기본 RHI GUI Editor를 TUT_Delivary_2로 재실행해 매니저 선택·Selection/Briefing/Lobby 자산 열기를 editor-review.json으로 확인했다. 열기 직후 dirty map/content0, 실제 Lobby Designer/계층·제공 아트 확인. 이후 사용자가 LobbyBackLine 위치를 직접 편집해 WBP_DroneLobby*가 된 것을 관찰했으므로 추가 UI/저장/재내보내기를 중단했다. 사용자 새 편집은 보존한다.

편집 절차는 UI/미션/게이트 가이드 정본, STATUS29,074B·WORKBOARD29,455B(각30KB 이하). Drone Space 기존 진행/Blueprint/테스트3개 Page에8연산 적용(sequence65/47/43)·동일 content stream 재조회에서 대상8블록 기대 본문 전부 일치. 새 Page·공유 변경 없음. 미커밋 코드/자산/MD와 Git 제외 Saved 보고서는 다른 PC/GitHub에 자동 배포되지 않는다.

## 2026-10-20 — 후속 UI·Pull·배달2·사진, 사용자 중간 확인 인계

- D PC `D:/JGY/project/drone`: 사용자 저장/종료 뒤119파일 약1.135GB를 before/post-save로 보존하고547efd1f→fc27eb7b fast-forward. stash5488ea0be62383d8f572967ee5ec866c873950a9 보존. 맵 충돌5개는 사용자 정책대로 수신본, 나머지 로컬 변경 복원. 미해결 충돌 없음·Commit/Push 없음. Production Training 저장 없음.
- 실제 저장 WBP의 직접 OnClicked 검사는 처음부터 통과했으나 실제 마우스 재현에서 타이틀 Back hit-test 차단/일시정지 두 번째 열기 Back 구독 소실을 별도로 재현했다. SettingsPanel Z 순서/NativeConstruct 재연결로 ui-applied-report4/4 통과(실제 마우스 Title·Pause2회 포함). 한글 CDO/정적 문구·작은 번호10·고도 흰 프레임·입력 십자선·허브 박스 기본 숨김을22WBP에 제한 적용, 사용자 배치/기존 주 HUD 보존.
- 회색 사진 띠는 테두리 포함 옛 Story Override를 저장된 새 프레임에 덧씌우던 원인. 새 화면은 DA의 테두리 없는 Thumbnail/BriefingImage 사용. 스카이드론은 지정 실제 SM_Drone01Body 촬영; 최초 사진은 컴파일 중 체커 재질이라 재촬영했다. 재질 재컴파일/AssetCompiling 완료 대기 뒤 실제 사진을 DA Racer.SelectImage로 저장. 원본 메시/비행 Pawn 변경 없음.
- Tutorial9·Story4에 기존 매니저/태그/재질 설정을 수신 맵 위 재적용. mission-apply2/2·cylinder-apply1/1 저장 성공. 배달2의 VV_grenades1/VV_highcaliber1/VV_WeaponBox2를 원래 메시·위치의 Carryable BP로 바꾸고 Cylinder의 허용 액터3개/고유3회·DA 목표3회를 연결. 옛 가방/팔레트와 대체된 정적 액터만 이 레벨에서 제거, 공용 자산 파일은 삭제하지 않음. FreeGate 준비 중/숨김 해제·실제 TUT_FreeGate13게이트 완주 Success.
- 배달 실제 낙하1차 실패: M_Target 재질 목적지까지 marker 정리가 숨김/충돌 OFF. PayloadTargetComponent가 붙은 목적지는 정리에서 제외하고 Cylinder BlockAll 복구. 재검사 첫 화물 전달은 성공했으나 두 번째는 첫 화물 위에 놓여 미집계. 이 **실패는 미해결**이며 사용자 확인 뒤 적재 위 전달 판정을 고치고3개 완료 PIE를 다시 돌린다. 계약 UniqueCargoDelivery 통과만으로 실제 완료라 쓰지 않는다.
- final-ui-tutorial-report는 D3D12 SM6 8성공/1실패: UniqueCargoDelivery·허브 숨김·FPV·Hovering·LOS·AllDesignerContract(실제1280/1920 사진/로비/브리핑/조작/스카이/UGV/일시정지/결과)·FlightHUDTelemetryBinding·HudDesignerContract 성공, Payload 실패. 렌더에서 회색 띠 제거/한글/번호10/HUD 십자선·고도 흰 박스 제거 확인. 직접 조종/실물 패드/청감/패키징은 별도.
- 전체 NPC Nav14맵 순차 도구/범위 보완·정식 Build/타일·전원 NPC 투영/저장 후 재로드 검사 소스 준비. **이번 배치는 아직 실행하지 않음**. 원본 Base/Production Training 보호, 다른 엔진 실행 차단·RAM/커밋/5분 보호·자기 PID 종료. 초기 RHI 맵 저장 보조는 잔디 생성 대기로 자기 PID25488만 중단, 뒤 NullRHI 저장 성공. 도구/검사 컴파일 실패와 사진 진단 API 오류는 원시 로그에 보존하고 수정 Build와 구분.
- 사용자 중간 확인 요청: 제공 Downloads/1792480499269.png를 픽셀 변경 없이 SourceArt/Selection/DropDrone_User_20261020.png로 복사, SHA2566488D3DF49DFCE54D6D3F0047DCD5CCD7FF7C6981F16BB77C7AE754EC15DEBB3 일치. T_SelectDrone_Drop_User_20261020·DA_Drone_Drop_Greybox.SelectImage 저장/메모리 참조 확인. bFitDropDronePhoto로 날개 전체 비율 표시. 이 새 사진은 사용자 실화면 확인 단계다. 마지막 Build 결과는 build-user-drop-photo.log를 따르며 성공을 추정하지 않는다.
- 이어갈 순서: 사용자 확인/에디터 종료 확인→배달 적재 판정 수리와 실제3상자 완료→NPC Nav14맵 실행/재로드→최종 회귀·자산/Git 보존 검사·MD/Space 마무리. 자동 예약/다른 작업자 엔진 조작 없음. 원시 자료 Saved/Automation/UiMissionFixes_20261020.

- 중간 확인 직전 최종 확인: build-user-drop-photo.log의 Result Succeeded/50.00초를 확인했다. Drone Space 진행/Blueprint/테스트3페이지에 같은 완료/미완료 경계를 반영하고 저장 뒤 본문 일치를 확인한다.


## 2026-10-20 — 중간 확인 후속: 실제 M1 선택창·배달 적재·NPC Nav 마무리

- D PC, Unreal HEAD/origin `fc27eb7b`, MD `dd16749` + 로컬 변경. 사용자 요청의 FrontEnd→1번 미션→드랍드론 선택 경로로 실제 PIE를 열어 촬영했다. `Saved/Automation/UiMissionFixes_20261020/m1-selection-city.png`를 사용자에게 전달했다. 초기 선택창 촬영은 도시 배경이 검게 나와 사용자 지적 뒤 원래 T_Select_Background의 저장 Image Brush/전체 앵커/Z0~3를 복구했다. 사진 안쪽 DronePreviewBackdrop만 alpha0이며 도시 배경/모서리 프레임은 유지한다. 예전 검은 스샷은 최종본이 아니다.
- 실제 Mission travel이 native Controller 기본 클래스를 사용해 저장 Designer를 우회하던 것을 DropSelection 빨간 검사로 재현했다. BeginPlay에서 native 기본값에만 Mission WBP7종을 연결하고 명시 BP override는 보존했다. Mission WBP 폴더 AlwaysCook 추가(실제 패키징은 미실행). 실제 선택 클래스는 WBP_DroneSelection_C·한글/저장 배치/사용자 원본 Drop 사진이다. 한정 수리 플래그 -DroneRepairSelectionBackdrop은 선택 WBP만 저장한다. Title/Pause 실제 마우스/Back2회 왕복도 이 경로에서 통과했다.
- 배달2 적재 실패를 실제 물리 투하로 재현했다. 이미 같은 목표에 전달된 화물의 안정된 윗면도 원래 목적지로 판정한다. Director의 목적지 Actor 중복 방지가 같은 Cylinder의 두 번째/세 번째를 막던 원인은 목적지 검증과 진행 신원을 분리해 수리했다. 고유 화물을 진행 신원으로 사용하고 일반 이벤트의 중복 방지는 보존했다. Cylinder가 M_Target marker 정리로 숨김/충돌 비활성이 되던 것도 PayloadTargetComponent 제외로 수리했다. 실제 세 상자 집기/적재 투하 뒤1/2개에서는 미완료·3개에서 성공, 중복/비허용/다른 목표 거부 검사 통과. 마지막3번째 뒤 결과를 기다리는 테스트 상태 오류도 수정했다.
- `m1-final-report` 4/4 Success: UniqueCargoDelivery·선택 배경 수리·실제 M1Selection·Payload. `delivery-gate-report` 실제 FreeGate13게이트 완료 통과. 앞선 실패 보고서는 덮어쓰지 않았다. LOS는 실제 후진 복귀→접지까지 검사한 `final-ui-tutorial-report` LOS Success이며 사용자 재확인대로 그 조건을 유지했다.
- Nav14맵을 격리 프로세스로 점검했다. Tutorial9맵 NPC0은 저장 없이 skip Success. UGV NPC 시험장1/1·20타일, Story Battlefield9/9·977타일, Story02 8/8·581타일, Story03 8/8·581타일, Camp27/27·1,874타일로 5맵53명·4,033타일 빌드/저장/재로드 후 시작점 투영을 통과했다. 최종 근거는 `NavigationVerified/Lvl_Tutorial_UGV_NPC_Test-report`와 `NavigationReadyVerified/summary.json`이다. Story4개 실행63.1/59.5/46.3/102.3초, 보호 중단0·오류0, 기존 경고57/5/5/1(UGV1)이다. NPCless9맵은 `Navigation/summary.json` 해당9행이다.
- Nav 재로드 초기 타일0은 Dynamic/ForceRebuildOnLoad 진행 중 상태여서 ready까지 기다리도록 했다. Battlefield의 서쪽 NPC4 투영 실패는 단순 Bounds 크기/위치만으로 해결되지 않았다. AsyncLoadLock 상태에서 Build가 실제 실행되지 않고 낡은 Nav가 남는 것을 로그/엔진 코드로 확인했다. 전용 도구가 명시 로드한 자체 월드에서 FlushAsyncLoading/전체 AssetCompilation 완료0 뒤 AsyncLoadLock만 해제하고 Bounds 갱신/실제 Build→저장→새 월드 재로드/대기한다. NPC/돌 충돌/지형은 옮기거나 제거하지 않았다. BSP pivot 대신 실제 Bounds 중심으로 보정하며 모든 NPC 범위 포함도 assert한다. 임시 NPC_NAV_PROBE/SELECTION_BACKGROUND 계측은 제거했다. 실패·probe 보고서는 보존했다.
- 최종 Build-clean16.41초 성공 뒤 집중 회귀 `final-regression-report`는13 Success/원형1 Fail이었다. 오류2개는 오래된 시험이 원형 완주 후 ReturnToBase/InMission을 요구한 것으로, 현행 원형 완주 즉시 성공 규칙과 불일치했다. 제품/LOS DA는 바꾸지 않고 시험에 원형 단일 목표/귀환 없음·완주 결과 성공을 검증하도록 수정했다. 최종 Build `build-circular-contract.log`32.35초 Success, `circular-current-contract-report` 원형 계약+실제 CircleGate2/2 Success. 기존13통과는 그대로이며 광범위 전체/실물 Pass로 확대하지 않는다. 사용자에게14통과로 성급히 보고한 뒤13/1로 즉시 정정하고 위 재검사를 수행했다. 중간 컴파일 실패 incomplete type은 DroppedPayload include 추가로 수리해 후속 Build 성공이다.
- `final-asset-audit.json`: 추적 Content 바이너리9,755개(Drone2,228) 누락0/LFS 포인터0·삭제/충돌/스테이징0, Production Training SHA256=HEAD LFS oid `6f297e405bc6d924ab345b60d55816c2fb3d1e6c718fc1fc2597734292fb6ed2` 일치. Pull 보존119파일/복구 stash는 유지한다. 신규 Commit/Push·Trello·공유·예약 변경 없음. NPC 전체 순찰/실물 패드/손 조종·청감·정상 화질 Camp 장시간·패키징은 수동/후속 경계다. 원래 맵의 Substance/MOUT 의존·Convex/zero-scale 경고를 새로 해결했다고 주장하지 않는다.
- Drone Space 기존 진행/Blueprint/테스트3개 Page의5개 수정 연산 적용 확인, 저장 뒤 동일 content stream 재조회5개 본문 모두 기대값과 일치(최종 sequence67/49/45). 새 Page/권한/예약 변경 없음. 수신/수정 receipt는 Saved/Automation/UiMissionFixes_20261020/space-final-sync.json. STATUS28,907B·WORKBOARD29,503B로30KB 이하 유지, source/docs diff --check 통과(줄바꿈 안내만 있음).


## 2026-10-20 — 사용자 제보 설정창 압축 수리와 검증 정정

- 사용자 실제 스샷에서 로비 설정이 수평 얇은 줄로 압축된 것을 확인했다. 앞선 Title/Pause 클릭/Back 자동 Success는 버튼 이벤트와 hit-test만 검사해 1픽셀 미만 버튼도 통과시켰다. 기존 저장 스샷 settings-title.png에도 같은 실패 외형이 있었는데 완료 보고 전 확인하지 못했다. 앞선 완료 표현의 설정 외형 Pass는 이 기록으로 정정하며 당시 보고서/기록은 보존한다.
- 같은 실제 FrontEnd 마우스 경로에 가독성 검사를 먼저 추가해 Title Fail3/Pause Success를 재현했다(settings-geometry-before-report). Title SettingsWidth의 WidthOverride=106244.164였고 화면상 패널1032×16.246px·뒤로2.819×0.670px이었다. 바깥 Fit/앵커보다 저장 WBP의 폭 값이 원인이다. 크기 원본·실패 스샷은 before-settings-sizing에 보존했다.
- 명시 -DroneRepairSettingsSizing 도구로 WBP_DroneSettings의 SettingsWidth를1240으로 고치고 Min/MaxDesiredWidth 제약을 비웠다(원래0). 전체 UI 재생성·텍스트/이미지 교체는 하지 않았다. 일시정지의 native 설정 자식도 같은 WBP_DroneSettings 클래스로 바꿔 공통 Designer를 편집하면 양쪽이 따라가게 했다. 해당 Pause WBP/클래스 기본값만 추가 저장하며 다른 화면/맵/LOS는 수정하지 않았다.
- 첫 수리 보고서3/3, 공통 WBP 및 wide 설정 인자 보고서5/5 통과. 후자의 캡처가 실제로는 기본 창 크기여서 wide 화면 증거로 사용하지 않았다. 테스트가 SWindow를 실제1280×720/2553×936으로 Resize하고 ClientSize를 assert하도록 보강했다. 최종 settings-window-proof-final-report Title/Pause/TitleWide/PauseWide4/4 Success, 패널 높이>350px·선택칸>=16px·뒤로>=100×24px·실제 클릭/Back·일시정지2회 재진입을 검증했다. 처음 실제 창 크기 검사에서 Pause Standard의 OS 테두리6px 차이만 실패해 허용 오차를8px로 보정했다. 해당 실패 보고서를 보존하고4종을 다시 실행했다. 최종 source Build build-settings-final.log Succeeded12.20초. 실제 수정 후 settings-title.png와 settings-title-wide.png를 시각 확인하고 사용자에게 전달했다. 실물 패드·화면 모드/해상도 적용은 Standalone 별도이며 이 검사는 사용자 설정 파일을 변경하지 않았다.
- 설정 수리의 MD 현재 상태/가이드 갱신과 Space 기존 진행·Blueprint·테스트3개 Page 수정3건 적용·재조회 일치를 확인했다(sequence68/50/46, settings-space-sync.json). STATUS29,082B·WORKBOARD29,541B, diff --check 통과. 모든 Unreal 검증 프로세스 종료·Production Training 해시 보존·Commit/Push 없음.

## 2026-10-21 D PC — 최신 Git 대조와 드론 선택 사진 교체 안내

- 사용자 요청은 최신화와 이미지 교체 방법 안내다. 실제 Drone005e24a2(1021)·MD1aef63a(1020)에서 origin Fetch 후 HEAD/origin 모두0/0을 확인했다. 추가 Pull 수신은 없었다. 사용자 Briefing/Lobby/TitleScreen/Selection WBP4개 수정과 미추적 Content/Drone/UI/HUD/Icons/less.uasset을 보존했다. 사용자 Editor가 실행 중이며 조작/종료·Build/PIE·자산 저장을 하지 않았다. Commit/Push·Trello·권한·예약 변경 없음.
- 현재 DroneDefinition.h의 SelectImage/CardSelectImage/bFitSelectionImages, DroneSelectionWidget.cpp의 큰 사진/카드 분기와 비어 있는 카드 fallback, ApplyUserDroneSelectionImages.py 매핑을 대조했다. DA6개의 실제 바이너리에서 T_SelectDrone_{Scout,Drop,FPV,Fiber,UGV,Sky}_{Preview,Card}12개 참조와 LFS 포인터가 아닌 저장 파일임을 확인했다. 카드가 이미 있으면 SelectImage만 교체해도 카드는 바뀌지 않는다. WBP의 DronePreviewImage Brush를 고쳐도 실행 시 DA 값이 들어가는 점과 스카이의 DA가 Racer인 점을 안내에 명시했다.
- STATUS 현재 Git/새 이미지 연결·WORKBOARD 소개와 UI 가이드의 6기체 DA 표/Import→큰 사진→카드→Fit→저장/실제 FrontEnd 확인 절차를 갱신했다. 이전 원본/텍스처를 현재 기본 연결로 쓰던 가이드 문구를 User_20261021 연결로 바로잡고 옛 자산은 보존했다. 사용자 Designer 치수는 초기 기준보다 우선한다. STATUS29,477B·WORKBOARD29,587B로30KB 이하 유지, diff --check 통과.
- Space의 C PC 기록은 Build69.98초·RAM 보호로 실제 새 사진 검증 미실행이며, 이전29/29는10/20 C PC 실행 근거다. 현재 D PC에 SelectionImages_20261021 원시 보고서는 없으므로 그 결과를 D PC에서 재검증했다고 쓰지 않았다. 오늘 소스/파일 참조 확인을 Build나 새 사진 렌더 Pass로 확대하지 않는다. Space 원문과 사람/다른 PC의 날짜별 기록을 보존하며 기존 진행·Blueprint 가이드 관련 본문만 보완했다.
- Space 기존 진행/Blueprint 페이지 수정2건 적용·재조회 일치 확인(sequence71/53). 새 Page 생성·공유 변경 없이 완료했다.


## 2026-10-21 D PC — Story 실패 정책과 미션 4 시작지점 3곳

- 사용자 확정: M1 폭파/실패·M2 실패는 결과 화면에서 재도전, M3/M4는 목표 완료까지 무제한 재출격. M4는 매 출격마다 3곳 중 다시 선택한다. M2 분기 결말·적 수량·제한 시간 등 미정 기획을 임의 확정하지 않았다.
- `FailureResponse`/`MaxCheckpointRestarts`를 Story DA4개에 반영했다. 기존 완료/부분 목표·파괴 표적 보존 경로를 재사용하며 같은 기체 종류/조작 방식으로 교체한다. LOS 수업의 별도 재시작/이륙→전진→후진→착지는 유지했다. M3/M4 6종 허용은 조율한 기존 UI 작업 창의 변경을 보존했다.
- `StartLocations`는 정확히3개·중복 없는 ID/표시명/유한 Transform을 검증한다. `WBP_DroneStartLocation`에 번호3개·이름/설명·선택 강조·출격/뒤로를 편집 가능한 트리로 저장했다. 첫 선택의 뒤로/Esc는 기체 선택으로, 재출격 때는 지점 확정 후 출격한다. 선택 중 세계를 멈추고 확정 후 복귀한다. 출격글은 한 줄과 안쪽 패딩으로 보완했다.
- `/Game/Drone/Managers/BP_DroneMissionStartPoint`는 기존 TargetManager 옆에 두었다. 기존 임시 `/Game/Drone/Mission` 경로에서 이동했다. 실제 M4 `Lvl_MilitaryCamp`에 BP3개와 기존 TargetManager.StartPoints 스포이드 연결을 저장했다. Outliner의 `Drone/StartPoints` 폴더 또는 `시작지점` 검색으로 찾는다. 위치/화살표를 직접 조정하며 DA에서 표시명/설명을 편집한다. 실행 위치 우선순위는 매니저 참조→일치 ID BP→DA 기본 Transform이다.
- 초기 배치는 기존 출발점 주변 약15m 간격이며, 좌표(cm)는 Start1=(9934.058,5019.004,6169.950), Start2=(9699.407,6500.536,6188.737), Start3=(9464.755,7982.069,6169.356). 지면 검사에서 시작 표식 큐브를 제외했다. 최종 전략 위치/적 시야/모든 기체 안전거리는 사용자 조정과 실제 맵 플레이가 남아 있다.
- D PC 직접 Build14.33초 성공(`Saved/Automation/StorySorties_20261021_build-1.log`), NullRHI SetupStorySorties/FailureResponseData 2개 성공(`StorySorties_20261021/setup.log`). Camp 메모리20GiB·정확한 맵 패키지명 확인·저장 전 백업을 적용했다. Production Training 맵은 열거나 저장하지 않았다.
- D PC RenderOffscreen `StorySortiesPIE.M1~M4` 4/4 성공(`StorySorties_20261021/pie.log`). 실제 Story DA 정책을 경량 Compass TestMap에 메모리에서만 적용하고 복원했다. 파괴/실제 FPV 접촉 자폭/실패 보고 후 M3/M4 3회 재출격·동일 Director·완료 및 부분 목표/파괴 표적 보존·목표 완료 시 Success, M4 실제 마우스 지점 선택/확정·배치 Transform·일시정지/복귀를 확인했다. 3D 사진 기능은 이 테스트에서 일시적으로 끄고 복원했으며 별도 UI 테스트의 결과로 확대하지 않는다.
- 마지막 출격글 보완은 같은 D PC의 조율한 통합 실행 `Preview3D_20261021/setup-final.log` SetupStorySorties 성공→`verify-4.log` M4 PIE Success(10:52:00 KST)로 재확인했다. `StorySorties_20261021/start-location.png`를 직접 열어 글이 한 줄이며 선택 강조/3카드가 보이는 것을 확인했다. 이 PNG는 경량 시험장의 UI 검증 화면이다. 실제 Camp 전체 전투 완주·실물 패드·패키징 Pass는 아니다.
- 사용자가 다른 작업 창에 전달/조율을 승인해 3D·6카드 UI 담당과 엔진 사용 시간을 나눴다. 사용자 기존 자산 변경을 보존했고 Commit/Push·Trello·공유 권한/예약 변경은 하지 않았다. 이전 자산/맵은 `Saved/Automation/StorySorties_20261021/Before`와 기존 Preview3D 백업에 보존했다.
- MD의 프레임워크 가이드/STATUS/WORKBOARD와 기존 Space 진행·Blueprint 가이드에 정책·조정 경로·검증 범위를 반영하고 읽어 대조했다. UI 작업 창의 이후 3D 결과는 별도로 기록한다.

## 2026-10-21 D PC — 기체 선택창 3D·M3/M4 기체6종·Back 이름 정정

- 사용자 요청: 모델 크기에 맞춘 자동 카메라/마우스 회전·확대 구현, M3/M4 모든 기체 허용, 복사된 기체 선택 뒤로 버튼 이름 수정. 실제 Drone005e24a2/MD1aef63a 위 로컬 변경이며 Commit/Push 없음. 사용자 편집 WBP·Drop DA·less 아이콘과 다른 작업의 Mission/StartLocation 변경을 보존했다.
- 새 UDroneSelectionPreviewWidget은 Engine FPreviewScene의 별도 GamePreview 월드에 실제 BP/StaticMesh를 조립한다. 월드를 Tick/BeginPlay하지 않고 충돌/물리/컴포넌트 Tick을 끈다. 6종 모두 실제 보이는 Mesh가 있다(정찰6/드랍9/FPV5/광섬유11/UGV1/스카이1). PreviewActorClass를 PreviewMesh보다 우선하며, 비어 있던 Scout/Drop/FPV는 기존 PawnClass, Racer는 사용자가 지정한 DroneRacing/SM_Drone01Body/StaticMeshes 메시를 연결했다. Fiber/UGV 기존 명시값과 사용자 사진은 유지한다.
- 기체 부품별 로컬 Bounds 8모서리를 월드로 변환해 화면 비율/수평·수직 FOV와 근접면을 고려한 자동 거리를 계산한다. 전체 AABB의 빈 모서리 때문에 초기 기체가 작게 보이던 구도를 부품 OBB로 개선하고 방향광8/보조광6으로 밝혔다. 왼쪽 드래그 궤도 회전, 휠 .35~4배 줌, 더블클릭 초기화. RT는 표시 크기에 맞춰 최대1024, 정지 시 상시 캡처하지 않는다. Clear/화면 이탈 시 임시 월드/RT를 해제한다.
- 큰 칸만3D, 아래 사진은 기존 CardSelectImage/빈 칸 SelectImage fallback. bUse3DSelectionPreview를 끄거나 모델 없음/로드 실패 시 큰 사진으로 돌아간다. 실제 WBP의 기존 사진/도시 배경/프레임/좌표를 유지하며 DronePreview3D 파츠·6번째 카드·DroneListViewport/Scroll만 추가했다. M3/M4 AllowedDroneIds를 기존 playable6종으로 맞췄다. 사용자 Drop의 빈 카드/Fill 선택도 보존한다. PreviewInteractionHint는 자식 TextOverrides로 수정 가능하다. UI material/기본 RT는 /Game/Drone/FrontEnd/UI/SelectUI/Preview3D, Cook 디렉터리도 추가했다.
- 기체 선택 WBP 안의 복사 이름은 실제 LobbyBackButton이었다. FWidgetBlueprintOperationUtils::RenameWidget으로 SelectionBackButton으로 바꿔 그래프/포커스 참조도 정정했다. 표시 이름 ‘기체 선택 · 뒤로 버튼’, 문구 ‘‹ 뒤로’. 최종 PIE는 실제 마우스 Back 클릭으로 MissionTrailer 복귀 상태까지 검사했다.
- 실패 근거 보존: Python widget_tree 비노출 검사, Setup 초기 Back 이름/6번째 native 문맥 실패, 새 위젯 GUID 미등록 Ensure를 보존했다. Save 전에 BP.OnVariableAdded를 호출하도록 고쳐 setup-final.log 2/2 성공. Build 초기 UE5.8 API 오타/변수 shadow, Build7의 다른 작업 LoadMap 반환 오류, Build9의 테스트 동적 델리게이트 매크로 오용, Build11 GetMaterialResource 인자/API 및 Build12 RHI global 링크 오류는 해당 코드/API로 수정했다. Build6 실행 도중 시작했던 setup-3는 테스트 시작 전 자신의 프로세스만 즉시 종료했다. 다른 작업 엔진을 종료하지 않았다.
- verify-1은 FStartPIEForAutomationCommand의 PlaySettings 수명으로 assertion 종료했다. Settings AddToRoot/엔진 helper RemoveFromRoot 균형으로 고쳤다. verify-2는 RT 숫자/실제 입력이 통과했지만 직접 연 PNG에서 모델 누락을 발견했다. RT template의 sRGB와 LinearColor sampler가 불일치해 기본 머터리얼을 썼다. template/live RT를 linear HDR로 맞추고 머터리얼 재컴파일·실제 UI shader map/compile error 검사를 추가했다. ‘입력/RT Pass’를 표시 Pass로 보지 않았다. 사진 검사의 임시 Demo 기본 Drone=None 오류와 사용자 Drop Fill을 무조건 Fit으로 기대하던 옛 검사를 실제 DA/Designer 선택에 맞춰 수정했다. 실패/중단 로그는 삭제하지 않았다.
- 최종 Build: Preview3D_20261021_build-14.log, DroneEditor Development Succeeded25.15초. 최종 실행: Saved/Automation/Preview3D_20261021/verify-final.log 및 verify-final-report, 10:55:51 종료0, 5/5 Success(Story34AllDrones, Selection3D.Framing/PIE, SelectionImageAssetsPIE.Racing/Roles). 경량 Lvl_MissionCompassTest의 실제 저장 WBP로6종 렌더/별도 월드·BeginPlay 없음·기체 해제·카드 사진·실제 드래그/휠/더블클릭/6번째 카드 클릭·실제 Back를 검사했다. 사진 모드6종은1280/1920 캡처·DA Fit/Fill·도시 배경을 검사했다. 3D PNG6개를 생성했고 Drop/UGV/Racer는 직접 열어 확인했다. 이 캡처는 경량 시험 미션 선택창이며 실제 M1 맵 전체 진입/손 조종/실물 패드·패키징 Pass로 확대하지 않는다.
- 다른 채팅 ‘드론 저장 공간 확인 및 정리 (2)’의 사용자 ‘작업 내용 보내고 조율’ 승인을 직접 읽어 확인한 뒤 파일/엔진 시간을 조율했다. 그 작업의 M1/M2 실패, M3/M4 목표 보존, M4 시작지점 소스는 담당자를 보존했다. 단일 엔진으로 setup-final에서 두 자산 도구2/2, verify-4에서 상대 M4 PIE를 선행 저장 후 재검사해 Success/출격 문구 한 줄 PNG를 전달했다. 그 다음 새 사용자 요구의 재출격마다 기체 선택/M1임시6종은 상대 작업 후속이며 이번 UI5/5 이후 소스 변경에 대한 Pass가 아니다. 사용자 GUI UnrealEditor PID26924는 새로 열렸으며 제 프로세스가 아니어서 조작/종료하지 않았다.
- 남은 외형: Sky 긴 설명3줄이 능력치와 겹치는 기존 Designer 간격은 별도 후속으로 명시했다. 조종/전투 전체·실물 장치/재출격 후속·패키징은 미확인이다. Production Training은 저장하지 않았고 SHA256은 6f297e405bc6d924ab345b60d55816c2fb3d1e6c718fc1fc2597734292fb6ed2와 일치했다.
- MD의 선택UI 가이드·STATUS/WORKBOARD 관련 줄만 갱신했다. 두 파일29,823B/29,831B로30KB 이하, diff --check 통과. Space는 기존 진행/UI가이드 본문만 갱신(sequence73/57), 다른 작업 미션 기록/사람/PC별 과거 기록은 보존했다. 새 Page·Trello·공유·예약 변경 없음. Saved 보고서는 GitHub에 게시한 자료가 아니다.


## 2026-10-21 D PC — 재출격 기체 재선택과 M1 임시6종 허용 후속

- 사용자 지시: M3/M4는 재출격 때 기체도 다시 선택. M4는 기체→시작지점→출격 순서. M1은 현재 조종 가능한6종을 임시 허용한다. M1/M2 실패 결과 방식·M1 기본드랍·목표 조건·M4 배치3곳은 유지했다.
- 미션 DA의 `bChooseDroneOnEverySortie`(재출격마다 기체 다시 선택)를 M3/M4에서 켰다. `SetupStorySorties`가 M1/M3/M4 AllowedDroneIds6종을 적용하며 기존 DefaultDroneId를 보존한다. M2는 재선택을 켜지 않는다.
- Flow는 InMission 상태를 유지한 채 재출격 선택 flag/API를 노출한다. 기존 `WBP_DroneSelection`을 다시 생성하고 세계를 멈춘다. 카드/3D/출격 활성 조건은 IsDroneSelectionActive를 사용하며 미션을 다시 초기화하지 않는다. 재출격 기체 창의 로비 뒤로는 숨긴다.
- 이번에 고른 PawnClass/ControlMode로 실제 새 기체를 만들고 같은 Director에 건강·배터리·정찰/투하 이벤트를 다시 연결한다. 목표 완료/부분 수치와 파괴 표적을 유지하고 새 기체를 직전 출격으로 기억한다. M4 시작지점 뒤로/Esc는 기체 선택으로 돌아가며 멈춤과 기존 미션을 보존한다.
- 사용자가 저장/직접 종료 회신 뒤 GUI/Cmd 종료를 직접 확인해 Build했다. 재선택 Build60.38초·실제 카드 클릭 테스트 추가 증분10.72초 성공. 설정/FailureResponseData 2개 성공(`Saved/Automation/StorySorties_20261021/reselect-setup.log`). 맵/기체 자산/사진/WBP 레이아웃을 이번 후속에서 다시 만들지 않았다.
- 첫 RHI 실행 `reselect-pie.log`: M1/M2/M3 Success, M4는 UGV의 지면 취득을 공중 출격 높이로 검사한1건 Fail. 생산 이동 코드는 그대로 두고 UGV를 XY선택점+실제 지면 높이로 검사하도록 보완했다. 실패 로그는 보존했다.
- M4 보완은 조율한 같은 D PC GateColors Build2에 포함됐고 추가 reselect-3 Build는0action1.44초 성공. `Saved/Automation/GateColors_20261021/verify-final.log` M4 Success(11:08:03 KST). 기체/출격/위치 실제 마우스 클릭, 정찰→FPV→UGV→드랍 교체, M4 지점 뒤로→기체 선택, 미션/Director/완료·부분 목표·파괴 표적 보존, 재출격3회, 3D 프리뷰 활성, 최종목표 Success를 확인했다. UGV는 기준 XY(0,2000)를 유지하고 Z1400 공중 표식에서 실제 지면 Z58로 취득했으며 다른 비행기체는 표식의3D 위치를 유지했다.
- M1 임시6종은 실제 카탈로그6개 각각 선택되는 것을 검사했다. M1/M2 실패 결과와 자동재출격0회도 유지됐다. 최신 `StorySorties_20261021/start-location.png`를 열어 지점창 뒤로/출격 단일줄·선택 강조를 확인했다. 실제 Camp 전체 전투·모든 기체 주행·실물 패드·패키징은 별도다. Gate 집중검사의 결과는 이 미션 작업의 Pass로 확대하지 않는다.
- 기존 사용자 변경/Story 목표/Production Training 맵 보존, Commit/Push·Trello·공유/예약 변경 없음. MD·기존 Space 미션 조정/현재 정책 절을 갱신하고 조율 창에 완료를 전달했다.

## 2026-10-21 D PC — Gate BP의 세 상태 색상 직접 편집

- 사용자 요청은 게이트 BP에서 통과 전/현재 목표/통과 완료3색 변경이다. 기존 코드는 색상 필드가 있었으나 저장된 bUseMaterialInstanceColors가 켜져 있으면 BP 색/발광을 무시했다. 새 AppearanceSource(enum)는 기본 Blueprint이고 MI 선택을 명시할 수 있다. 구형 bool은 숨김/deprecated 읽기 호환으로 남기며 기존 맵을 재저장하지 않아도 BP 기본3색을 사용한다.
- DroneTrainingGateTypes의 상태 표시명을 한글화하고, Gate의 기존 InactiveColor/CurrentColor/CompletedColor 멤버 이름과 값을 보존하면서 Category를 Tutorial|Gate|상태 색상으로 모았다. 표시명은 ‘01 통과 전 색상 (대기)’/‘02 현재 목표 색상’/‘03 통과 완료 색상’이며 발광3값과 색상·발광 조정 위치도 같은 항목이다. Class Defaults와 레벨 인스턴스에서 편집 가능하다. PostEditChangeProperty의 컬러/발광 편집·SetGateStateColors 호출은 BP 모드로 전환해 현재 재질에 즉시 반영한다. MI 모드를 선택하면 동적 override를 비워 원래 MI 값을 쓴다.
- 실제 BP 검사의 첫 실행에서 두 가지를 구분했다. 검사 코드가 금속 슬롯0만 기대한 것은 잘못이어서 실제 Gate 소유 MID 슬롯을 검사하도록 고쳤다. 실제 저장 BP는 색상 슬롯1/파라미터 Param이며 새 공통 부모는 Color여서 적용이 빠질 수 있었다. 생산 코드 ApplyAppearance는 저장된 파라미터가 실제 부모에 없으면 Color로 호환하고, 명시 None은 보존한다. 원래 메시의 비대상 금속 슬롯과 MI 자산 값은 변경하지 않는다. 사각 fallback4변과 완성형 자산 모두 같은 경로로 갱신한다.
- Build1 Succeeded35.31초. verify-1은 기존 TrainingGateBlueprint/Presentation/Sequence3개 Success, 신규 GateBlueprintColorEditing Fail을 보존했다. 위 슬롯/파라미터를 수정한 Build2 Succeeded10.07초. 최종 Saved/Automation/GateColors_20261021/verify-final.log 및 report-final은11:08:04 종료0,5/5 Success다. 이 중 Gate4개는 GateBlueprintColorEditing, TrainingGateBlueprint, TrainingGatePresentation, TrainingGateSequence이며 실제 저장 BP를 불러 Compile·Editor World에 Spawn해 세 색/MI 선택/Details property change/현재 표시/사각 fallback/CDO 비영속 MID 차단을 검사했다. 시각적 현장 가독성·사람의 컬러피커 조작 확인을 자동 Pass로 확대하지 않는다.
- 단일 엔진 시간은 다른 미션 작업과 조율했다. 상대 reselect 신규 M4 위치 검사를 함께 컴파일·RHI 재실행해11:08:03 Success를 전달했다. 해당 테스트 수정은 상대 소유이며 Gate 기능 결과와 분리한다. 서로 메시지가 교차해 상대 증분 Build가 함께 요청됐으나 WaitMutex로 직렬 실행됐고 상대 reselect-3는0action/1.44초 Success였다. 두 Build 종료와 UE 없음 확인 뒤 최종 RHI1회만 실행했다. 외부 Editor 조작·종료는 없다.
- 이번 변경은 Tutorial 소스3개/신규 Gate 편집 검사와 문서다. 실제 BP·MI·맵을 재저장하지 않았고 기존 상태 재질 폴더는 /Game/Drone/Tutorial/Materials 그대로다. Production Training SHA256 6f297e405bc6d924ab345b60d55816c2fb3d1e6c718fc1fc2597734292fb6ed2 일치, Git unmerged0, 해당 소스 diff --check 통과. Commit/Push·Trello·공유·예약 변경 없음.
- MD Gate 저작 가이드의 현재 편집 절차·STATUS Gate 줄·WORKBOARD Gate 행을 갱신했다. STATUS29,871B/WORKBOARD29,845B로30KB 이하를 확인했다. Space 기존 Blueprint 가이드 Gate 본문2300f09f...를 갱신하며 UI·미션·코스 기존 기록은 보존했다. 진행 페이지는 다른 작업의 Story 부분 저장 뒤 fresh hash로 Gate 현재 결과만 반영한다.
- Space Gate 가이드 seq59·진행 seq75 적용/재조회 일치 확인. 상대 Story seq74를 fresh read해 보존했다. 최종 STATUS29,886B/WORKBOARD29,881B로30KB 이하이며 Gate 관련 소스/문서 diff --check 통과. 이번 Gate 범위 완료.

## 2026-10-21 D PC — main 분기 병합·Push와 게이트 머터리얼 자동 우선

- 사용자 GitHub Desktop Push 거부 화면을 실제 저장소와 대조했다. 로컬 `9f1610e1`(1021)과 원격 `05a47d3c`(261021)가 공통 `005e24a2`에서 각각1개씩 갈라져 있었고 시작 작업 트리는 Clean이었다. Fetch와 merge-tree에서 로컬47파일/원격3파일 겹침0·충돌0, 예상 병합 트리의 각 파일 blob이 해당 출처와 모두 같음을 확인했다.
- 사용자의 명시적 ‘병합하고 푸쉬’ 지시 후 부모9f1610e1/05a47d3c를 보존하는 `63f653ab37f760e321bdc1a8459774004e6d774d`를 만들고 origin/main에 Push했다. 실제 ls-remote SHA 동일·ahead/behind0/0·병합 직후 Clean을 확인했다. force push/rebase/reset은 사용하지 않았다. 수신은 Training/FreeGate 맵과 Gate States 머터리얼3개이며, 팀원 원격 파일을 그대로 적용했다. 엔진으로 Production 맵을 저장한 작업이 아니다.
- LFS 전송 중 Windows 파일 크기 표시 지연을 정체로 잘못 판단해 자신의 filter-process만1회 종료했다. 뒤에 실제 열린 파일 길이로 수신 진행을 확인했다. 중단된 적용3개만 HEAD로 복원하고 index를 갱신한 뒤 LFS smudge를 분리해 병합/Push와 다운로드를 마쳤다. 최종 로컬 LFS 파일 SHA256은 원격 포인터와3개 모두 일치했다: Training=`27c2c0c25183d7914a3686306e44e250642b70c16eb9988560d093e580808128`, FreeGate=`87a468abecc5e05db07054ad03e4697c700786720f6914c28bbd9fb1f37b1b04`, States=`020d8deac2188679986294278d9219c373cffb5cd54734e5634508f119698d7f`. 완성 LFS 객체 해시 확인 뒤 이번 전송이 남긴 부분 파일382,918,558B만 삭제했다. 기존 다른 부분 파일·stash는 건드리지 않았다.
- 후속 사용자 요청에 따라 게이트는 모드 선택 없이 상태별 머터리얼을 자동 우선한다. InactiveMaterial/CurrentMaterial/CompletedMaterial을 BP의 Tutorial/Gate/상태 색상으로 모았으며, 연결된 상태는 원본 재질의 색/발광/표현을 그대로 사용하고 빈 상태만 BP 기본 색·발광을 쓴다. 현재 목표만 MI/나머지 BP 혼합도 가능하다. 기본 색 편집·SetGateStateColors는 연결한 MI를 덮어쓰지 않는다. 재질을 지우면 즉시 해당 상태 기본값으로 복귀한다.
- 기존 AppearanceSource 수동 UI는 숨겼다. 저장 필드와 구형 setter 노드는 로딩/호출 호환용으로 유지하지만 현재 판정을 바꾸지 않으며 getter는 현재 상태의 실제 출처를 반환한다. Param/Color 호환, 비대상 금속 슬롯, 사각 fallback, CDO 런타임 MID 직렬화 방지는 유지한다. 기존 BP/MI/맵은 재저장하지 않았다.
- 사용자 Editor/Cmd 실행 없음 확인 뒤 DroneEditor Development Build53.04초 성공(`Saved/Automation/GateMaterialAuto_20261021/build.log`). RenderOffscreen 기존 BP Compile/Editor World 실제 인스턴스·완성형/사각 표시의 Color/EmissiveStrength·혼합 슬롯·Details 해제·같은 부모의 MID 재사용·벡터/스칼라 override0·기존 통과 판정4/4 Success, warning0/failed0/notRun0, 11:36:45 KST 종료0(`verify.log`, `report/index.json`). 시작 전 Condition failed15줄은 이전 GateColors 실행과 동일하며 개별 Gate4 리포트는 errors/warnings0이다. 현장 가독성/사람의 컬러피커 조작·전체 맵 플레이/패키징 검증은 아니다.
- Git 병합·Push는 완료됐지만 그 뒤 추가한 게이트 자동 전환 소스5개와 MD는 로컬 수정이다. 추가 Commit/Push는 수행하지 않았다. STATUS/WORKBOARD의 현재 Git·Gate 줄과 저작 가이드만 갱신하고 기존 UI/Story 변경과 과거 이력을 보존했다. Space 기존 진행/Gate 가이드는 같은 자동 우선/빈칸 기본 규칙과 현재 Git 기준으로 갱신한다. 새 Page·Trello·공유/예약 변경은 없다.
- Space 기존 Gate 가이드 seq60·진행 seq76 적용 후 본문 전체 재조회가 기대값과 일치했다. 이전 UI/Story 및 PC별 실행 기록을 보존했다. 최종 STATUS29,928B/WORKBOARD29,895B로30KB 이하, 두 저장소 diff --check 통과·Unreal 프로세스 없음. Git HEAD/origin0/0 유지, 수신3자산 해시도 재확인 일치다.

## 2026-10-21 D PC — 출발 카운트다운 흰색

- 사용자 요청은 3·2·1 글자를 흰색으로 바꾸는 것이다. 시작 HEAD/origin/main은 사용자 커밋 `ddbd963d`로 같고 작업 트리는 Clean이었다. 실제 원격 SHA도 동일했다. 이번 Commit/Push는 없다.
- 정본 `/Game/Drone/UI/WBP/HUD/WBP_DroneFlightHUDKit`과 독립 `/Game/Drone/UI/WBP/Mission/WBP_DroneStartCountdown`의 CountdownText를 기존 RGBA(1,.86,.25,1)에서 (1,1,1,1)로 변경·Compile·저장했다. 실제 글꼴/크기72·120/간격은 저장 전후 같음을 확인했다. 위치·크기·그림자 등은 편집하지 않았다. 같은 TextBlock의 출발 문구도 흰색이다.
- Native fallback과 기존 HUD 생성 도구의 기본 색도 FLinearColor::White로 맞췄다. Designer 색을 런타임에 강제 덮어쓰지 않으므로 이후에는 HUD12구역 CountdownText의 Color and Opacity에서 계속 조정한다. 전체 HUD 재생성은 하지 않았다.
- Editor 종료 확인 뒤 Build30.32초 성공(`Saved/Automation/CountdownWhite_20261021/build.log`). 기존 자산2개만 Python의 UObject 탐색으로 수정했으며 백업은 같은 폴더 Before에 있다. 첫 asset 스크립트는 SlateColor 래퍼 동등 비교에서 저장 전 중단했고, 채널 값/스타일 규칙으로 비교를 바꾼 두 번째 실행에서 두 자산 모두 실제 RGBA(1,1,1,1)·Compile/Save 성공·종료0을 확인했다(`assets-2.log`, `asset-receipts.json`). 첫 실패 로그는 보존했다. 추가 자동 테스트나 전체 PIE/화면 캡처는 실행하지 않았다.
- 사용자 기존 자산/맵/배치 보존, 프로젝트 플러그인 설정 변경 없음. MD 현재 상태·HUD 조정 표와 기존 Space HUD 안내를 흰색 기본값으로 갱신한다.
- Space 기존 HUD 안내491b98ac 블록만 seq61에서 수정·재조회 일치 확인했다. STATUS29,809B/WORKBOARD29,877B, 양쪽 저장소 diff --check 통과·Editor 종료 확인이다. 로컬 수정은 WBP2개/소스2개이며 Commit/Push는 하지 않았다.

## 2026-10-21 D PC — 지급 이미지5장 교체·레이싱 실제 기체 외형 수정

- 사용자 지급 PNG5장에 대해 2번은 정찰·광섬유 공용, 4번은 레이싱이라는 회신을 받아 적용했다. 연결은1 FPV/2 Scout·FiberOptic/3 UGV/4 Racer/5 Drop이다. 파일은 모두1920×1080 RGBA·알파0~255이며 SourceArt/Selection/User_20261021_Updated로 바이트 그대로 복사했다. manifest.json의5개 SHA256이 원본과 일치한다. 이미지 픽셀/알파를 가공하지 않았다.
- /Game/Drone/FrontEnd/UI/SelectUI/Drones/User_20261021_Updated에 UI 텍스처5개를 새로 저장하고 DA6개의 SelectImage/CardSelectImage에 연결했다. 같은 원본을 양쪽에 쓰며 Fit=True로 전체 기체를 보존한다. Drop의 기존 Fill은 새 원본 잘림을 피하도록 Fit으로 바뀌었다. 기존 사진/원본/텍스처는 삭제·덮어쓰기하지 않았다. PreviewMesh/PreviewActorClass/3D 사용과 FlightProfile은 적용 전후 동일했다. 기존 카운트다운4개 로컬 수정도 보존했다.
- 랜덤 도시에서 FPV 외형이 나오던 원인은 미션 선택 ID가 아니다. Racing_Circuit_Test/Procedural_Test/Map1/Map2/Map3의5개 DA는 이미 허용/기본 ID가 Drone.Racer.Greybox였다. 공통 BP_DroneRacerIntegration의 VisualMeshComponent는 SM_DroneFPVBody, FPVRotorA~D는 FPV 메시로 남아 있었고 초기 BuildDroneRacerDrone.py도 FPV BP 복제만 했다. audit.log/race-before.json에 저장했다.
- 공통 Racer BP 본체를 사용자 지정 DroneRacing/SM_Drone01Body/StaticMeshes의 완성형 메시로 교체하고 FPV 별도 로터4개는 메시/태그를 비우고 숨겼다. 기본 Scale5·Yaw-90·위치0, 기존 충돌45cm/카메라·입력·기체 비행 수치는 유지한다. 완성형 단일 메시이므로 별도 로터 회전용 새 분할 자산은 만들지 않았다. 기존 FPV BP/공급 원본 메시/미션 DA·맵은 수정하지 않았다. 새 ConfigureDroneRacerVisual.py를 기존 Racer 생성 도구에도 연결하고 대상 미션 목록을5개로 맞춰 재생성 시 외형이 되돌아가지 않게 했다.
- 적용은 Editor 없음 확인 뒤 선택적 Python 명령으로 새 텍스처5/DA6/Racer BP1만 저장했다(apply.log/applied.json). 기존 DA6/BP 백업은 Saved/Automation/ImageRefreshRace_20261021/Before에 보관했다. 원래 게임/사용자 Editor를 종료하지 않았다. 프로젝트 플러그인 설정은 변경하지 않았다.
- 기존 원형/랜덤 도시 PIE 검사에 실제 Spawn된 Racer의 본체 메시와 FPV 잔여 메시0을 추가했다. 원형 검사 시작에는5개 미션의 Racer 허용/기본 ID도 읽기 검증한다. 첫 Build는 검사 switch 지역변수 범위 오류(C2360)로 실패했고 범위만 고친 Build2는12.70초 성공했다. 첫 RHI verify.log/report에서 원형 출격·사진 Roles/Racing3개는 Success, 랜덤 도시1개는 가이드선의 낡은 최근접 높이 검사만 Fail이었다. 새 Racer 메시/FPV 잔여 검사는 실제 도시 출격에서도 통과했다.
- 도시 검사에서 높인 Gate 중심의 최근접 Spline 점을 찾으면 언덕/교차부의 다른 구간을 잡을 수 있었다. 생산 Course가 Gate에 기록하는 SegmentDistance를 사용하고 기존 TrainingGatePresentation과 같은 Actor 로컬 좌표로 검사하도록 바꿨다. 기대값을 넓히지 않고 실제1/6±.01로 더 엄격히 검사한다. Build3는14.62초 성공, verify-city-final.log/report-city-final의 CityRacePIE는13:11:54 KST Success·종료0이었다. [GATE-LINE] 실제 배정 구간0.167~0.167, 과거 최근접 질의0.167~0.290으로 차이를 확인했다. 첫 실패 로그/보고서는 보존한다. 생산 Gate/도시/미션 코드는 변경하지 않았다.
- 최종 대상4종은 사진 Roles/Racing2개·원형 출격1개(첫 verify 성공)와 랜덤 도시1개(보완 재실행 성공)다. 실제 선택 WBP의 DA 이미지/카드/도시 배경·Fit·1280/1920 렌더와 실제 Racer Spawn·카운트다운/생성/재시작 흐름을 확인했다. Saved/Automation/SelectionImages_20261021/Captures의 새 Sky/Scout/UGV/FPV PNG를 직접 열어 확인했다. 이 사진 검사는 경량 Compass TestMap의 실제 UI이며3D는 검사 중만 메모리에서 끄고 복원했다. 실제3D 설정은 저장 전 값 그대로다. 팀원3맵은 DA와 공통 Pawn을 확인한 범위이며 이번에 각 대형 맵 전체를 열어 손 조종 완주한 것은 아니다.
- 기존 MI_DroneTrainingGate_03_Passed의 Nanite 사용 플래그 경고는 별도로 남아 있고 재질/맵을 이 이미지 작업으로 재저장하지 않았다. 사용자 원본/팀원 Production/카운트다운 변경을 보존했다. Commit/Push·Trello·공유/예약 변경은 없다. MD 현재 상태/선택 사진·Racer 조정 안내와 기존 Space 관련 블록을 갱신한다.
- Space UI 가이드5298e67b seq62·진행66a7c9a4 seq77 적용 후 전체 대상 블록 재조회가 기대값과 일치했다. 다른 HUD/미션/게이트·PC별 기록을 보존했다. 최종 STATUS29,689B/WORKBOARD29,784B, 두 저장소 diff --check 통과·Editor/Cmd 없음. HEAD ddbd963d 위 로컬 수정이며 추가 Commit/Push는 없다.

## 2026-10-21 D PC — 레이싱 프로펠러 누락 정정

- 사용자 제보로 앞선 ‘SM_Drone01Body 완성형’ 판단을 정정한다. 이 메시에는 프로펠러가 없는데 ConfigureDroneRacerVisual.py에서 기존 로터4개를 비웠고, 선택3D는 본체 단일 PreviewMesh만 사용했다. 직전 본체 경로/FPV 잔여0 검사는 이 결함을 잡지 못했다. 위 과거 기록은 당시 판단/실행 이력으로 보존하며 현재 올바른 조립은 아래와 같다.
- Saved/Automation/RacerRotors_20261021/audit_rotors.py를 Unreal Python 명령으로 실제 BP를 생성해 실행했다. audit-red.log는 runtime_visible=0·preview_actor=None으로 실패했다. 이어 실제 원형 출격/선택3D PIE에 로터 개수·표시/재질/태그·허브 위치 판정을 추가하고 수정 전 verify-red.log/report-red에서2종 모두 예상한 누락으로 Fail인 것을 확인했다(게임0개, 선택 본체1개). 결정적인 재현/삭제 기록이 있어 별도 가설 나열 단계는 생략했다.
- DroneSky/SM_Drone01_r1~r4는 Racing 본체와 원본 치수/좌표가 맞는 별도 날개다. 공통 BP_DroneRacerIntegration의 기존 이름 FPVRotorA~D에 이 메시를 연결하고 본체와 위치0·Scale5·Yaw-90을 공유한다. DroneRoleVisual/DroneRotor 태그·기존 회전 로직으로 각 허브를 고정해 회전한다. 새 부품/원본 재질 복제는 필요하지 않았다. Racer DA.PreviewActorClass는 같은 BP여서 실제 선택3D에서도 본체+로터5부품을 표시한다. PreviewMesh 본체 fallback·3D 사용/사진 Select/Card 참조·Fit·FlightProfile/능력은 적용 전후 동일함을 apply-receipt.json으로 검사했다.
- 현재 작업본 BP/DA2개를 Before에 백업하고 이2개만 저장했다(apply.log 성공). 원형/랜덤 도시/Map1/2/3이 공유하므로 모든 레이싱 선택/출격 외형에 적용된다. 생성 도구에도 부품 복구와 PreviewActorClass 연결을 넣어 재생성 시 누락을 막았다. 다른 기체/사진 원본·팀원 맵·생산 코스/미션/카메라 설정값은 저장하지 않았다. 기존 카운트다운/이미지 수정도 보존했다.
- 첫 C++ Build는 새 검사 helper의 GetStaticMesh 반환 TObjectPtr 자동 포인터 추론 오류로 실패했고 명시적 UStaticMesh 포인터로 고친 Build2는13.68초 성공했다. 같은 audit_rotors.py 재실행은 로터4개/전체 PreviewActorClass로 성공했다. RHI verify-green.log/report-green의 RacingStartCountdownPIE·CityRacePIE·Selection3D.PIE3종 모두13:32:16 KST 최종 Success다. 원형 출격 전후와 도시 실제 Spawn의 허브 좌표(±6.13,±5.11,3.95)가 유지되고 선택3D는 실제5개 메시/렌더 픽셀·마우스/Back을 확인했다.
- 실제 게임 사진이 처음에는 멀고 낮은 각도여서 테스트 인스턴스의3인칭 SpringArm만180cm·Pitch-35/Yaw35로 바꿔 근접 촬영했다. BP 기본 카메라는 수정하지 않았다. Build-camera13.02초 성공·verify-camera.log/report-camera의 원형 검사13:34:20 KST Success이며 게임의 회전 프로펠러 부착 상태를 직접 이미지로 확인했다. Saved/Automation/Racing/circuit_racing.png와 Preview3D_20261021/preview-DA_Drone_Racer_Greybox.png가 실제 결과다. 선택 캡처는 경량 Compass TestMap의 실제3D 화면이며 M1 FrontEnd 캡처로 표현하지 않는다. 수정 전 사진도 preview-before/gameplay-before.png로 보존했다.
- 실제3D 렌더/자동 출격 검증이며 팀원3맵 전체 손 조종·실물 패드·패키징 Pass는 아니다. 원래 Nanite/기존 맵 경고와 Sky 설명 간격 후속은 별도로 남긴다. Git HEAD ddbd963d, 원격 추적 origin/main ed85c0e8로0/2이며 이번 Fetch/Pull/Commit/Push는 없다.
- MD 현재 조립/조정 안내와 기존 Space UI5298e67b seq63·진행66a7c9a4 seq78을 정정했다. 두 블록을 다시 읽어 전체 기대값 일치/타 주제 보존을 확인했다. STATUS29,718B·WORKBOARD29,751B로30KB 이하를 유지한다.
