# Drone 개발 진행 기록

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
