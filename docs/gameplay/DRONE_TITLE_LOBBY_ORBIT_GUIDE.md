# 시작 화면 · 로비 탭 · 원형 코스 가이드

현재 절차 기준: 2026-10-14 D PC. 기존5메뉴·결과·훈련/레이싱을 유지하면서 제공 `Select_UI`를 Story 선택에만 적용하는 코드/슬롯을 설명한다. 구현과 새 자산 저장·자동 검증·수동 화면 확인은 구분하며 현재 결과는 STATUS·WORKLOG를 따른다. 원본 이미지·Figma·기존 타이틀 아트는 보존한다.

## 0. 현재 계약 — 5메뉴·조종 입력 표시 현재 구현과 계약

기존5메뉴·조종 입력 표시 계약은 유지한다. 10/01~10/03 당시 구현/검증과 담당 구분은 WORKLOG에 보존하며, 새 Story Select_UI 변경까지 그 당시 Pass에 포함하지 않는다. 실제 패드/화면 확인은 별도다.

- 타이틀 순서: **스토리 / 레이싱 / 튜토리얼 / 설정 / 종료**. `UDroneFrontEndRootWidget::OpenLobbyForCategory(Category)`가 먼저 분류를 정한 뒤 첫 목록/포커스부터 표시한다. `OpenStoryLobby`=Mission, `OpenRacingLobby`=Racing, `OpenTutorialLobby`=Tutorial, 종료=`RequestExitGame`. 기존 `FinishOpeningTrailer`=스토리·`OpenTrainingLobby`=튜토리얼은 호환 유지. 시작 뒤 중간 화면 없음, 브리핑·기체 선택·출격·결과·복귀는 기존 흐름 재사용.
- `WBP_DroneFrontEndRoot` Class Defaults `TitleMenuClass = WBP_DroneFiveItemMenu`로 **저장 연결 완료**. 위젯 필수 버튼 `StoryButton / RacingButton / TutorialButton / SettingsButton / ExitButton`, 필수 Dispatcher `OnStoryRequested / OnRacingRequested / OnTutorialRequested / OnSettingsRequested / OnExitRequested`, 선택 `OnBackRequested`. 이름 계약을 확인해 연결하며 틀리면 `[TITLE-MENU]` 경고 후 C++ 기본 5버튼. 위젯 디자인은 유지하고 호버/클릭 효과음만 붙인다.
- `GetTitleButton`과 Title*Index는 순서대로 0~4. 설정 닫으면 설정(3), 로비 닫으면 들어갔던 메뉴, 맵 이동 후 새 타이틀은 마지막 분류 메뉴로 포커스. 위/아래 끝 순환, B/Esc 반복은 한 화면만 Back. 진입 뒤 분류를 바꾸던 기존 훈련→Racing 포커스 문제도 진입 전 분류 지정으로 수정. 로비 Tutorial/Racing 탭·LB/RB는 그대로 두며 유지 여부는 **현재 미정**.
- C++ 기본 메뉴 `TitleButtonHeight=80 / TitleButtonSpacing=26`은 5개 배치를 위한 임시값이며 UI 담당 조정 대상. 별도 `TitleMenuClass` 위젯 외형은 해당 Designer에서 조정한다. 기존 사람 디자인/배경/로고는 보존한다.
- 설정 “조종 > 조종 입력 표시”(`ControlInputDisplayCheck`)는 고도계와 독립한 수동 ON/OFF. 적용·취소·기본값 복원 구조 그대로, 기존 음량 SaveGame에 `bHasControlInputDisplayChoice / bControlInputDisplayEnabled` 저장. 사용자 선택이 우선하며 기본값 복원→적용은 선택을 지워 앞으로 정해질 기본값을 따른다. `DefaultGame.ini`의 `[/Script/Drone.DroneAudioSettingsSubsystem] bControlInputDisplayEnabledByDefault=False`는 결정 전 임시 끔, **최종 기본값 현재 미정**. 자동화는 `DroneAudioSettings_Automation` 슬롯으로 사용자 설정 보호.
- `WBP_DroneFlightHUD` Class Defaults `ControlInputDisplayClass = WBP_DroneControlInputDisplay`로 저장 연결 완료. 화면 아래 가운데 `ControlInputDisplayOffset=(0,-24)`, 월드 타이머 `ControlInputDisplayUpdateInterval=1/30초`, 설정 ON·기체 있음일 때만 `SetControlInputDisplayVisible`·`UpdateStickAxes` 이름 호출(축은 값이 바뀔 때만). OFF는 숨김·갱신 중지, 다른 HUD는 유지.
- `ADroneFlightPawn::GetControlInputSnapshot()` BlueprintPure의 X 오른쪽+, Y 위+, [-1,1]은 스틱 물리 위치. 쉬운/실제 조작형: 왼쪽 이동·오른쪽 X 회전/Y 카메라·트리거 고도. Acro Mode 2: 왼쪽 Yaw/스로틀·오른쪽 Roll/Pitch, Mode 1: 왼쪽 Yaw/Pitch·오른쪽 Roll/스로틀. 지상: 왼쪽 조향/전후. 키보드도 같은 액션 위치로 표시되며 입력 매핑 추가 없음. UI 커서는 중심±38px·화면 Y 반전. 장치 자동 구분/전환·혼합 입력·분리/재연결 정책은 현재 미정이다.
- 저장 BP 연결을 검사하며 테스트 메모리 Class Defaults 덮어쓰기는 인스턴스 연결 근거로 쓰지 않는다. 제품 연결은 구현됨·자동 검증됨·실제 패드/1280·1920 수동 대기다.
- 제품 Racing `TestMap/Lvl_DroneRacingTest`에는 RouteSelector 없어 숫자키 미노출 확인. Selector `bAllowPlayerRouteKeys=true / bBlockRouteKeysInRacingMissions=true`: 로비 Racing 미션 1~5 바인딩·키 안내 없음. 시험맵 직접 실행·Tutorial/Training/Story는 기존대로, 랜덤 기능 보존. 팀원 지형 LFS 수신됨(10/04), 제품 연결/PlayerStart·완주 규칙은 현재 미정.
- 최신 검증은 STATUS를 따른다. 팀원 지형 LFS는 10/04 수신됐으나 제품 Racing 연결·PlayerStart·완주/복귀는 현재 미정(RACING-TERRAIN-LINK-01), 결정 전 완주 확인 대상으로 두지 않는다.

## 1. 이전 4메뉴 구현 기록 (2026-10-01)

당시 세션 원문은 [WORKLOG](../history/DRONE_WORKLOG.md)에 보존했다. 현재 구현·검증은 [STATUS](../../STATUS.md)를 따른다.

## 2. 어디를 열고 테스트하나

1. 새 C++ 코드가 포함되므로 Editor를 닫고 `DroneEditor Win64 Development`를 빌드한다. Live Coding만으로 새 UPROPERTY/enum 변경을 확인하지 않는다.
2. `/Game/Drone/Maps/Lvl_DroneFrontEnd`를 열어 Play한다. 프로젝트 `GameDefaultMap`도 이 맵이다. Editor 첫 맵은 기존 Production Training 설정을 유지한다.
3. 스토리·레이싱·튜토리얼·설정·종료5개 문구를 확인한다. 스토리는 M1 맨 위4개 Story 목록, 레이싱은 Circuit/Procedural2개, 튜토리얼은 `기초 조종` 맨 위 수업 목록으로 처음부터 진입해야 한다. B/Esc 메뉴 복귀·설정 닫은 뒤 설정(3) 포커스, 위/아래 끝 순환과 키 반복 한 화면 Back을 확인한다.
4. Story는 아래 Select_UI 절의 왼쪽 목록·가운데 이미지·오른쪽 설명·하단 START 배치를 확인한다. 훈련 탭은 숨기고 브리핑 복귀 시 분류/선택을 복원해야 한다. 튜토리얼/레이싱의 기존3열·스크롤·탭/LB/RB는 보존한다(최종 탭 유지 여부 미정).
5. Story 카드 클릭은 선택만 하며 하단 `START MISSION`에서 기존 MissionTrailer/브리핑 흐름을 시작한다. 이후 작전 지역 이동→기체 카드→조작 설정→출격을 진행한다. 튜토리얼/레이싱 카드의 기존 즉시 확인 동작은 바꾸지 않는다. 기체 선택의 뒤로/Esc/패드B는 해당 브리핑으로 돌아간다.
6. 튜토리얼 `1-3 원형 코스 비행`은 `/Game/Drone/Maps/TestMap/Tutorial/Lvl_Tutorial_Heading_Test`, 레이싱은 `/Game/Drone/Maps/TestMap/Lvl_DroneRacingTest`로 이동한다.


7. 설정 > 조종 > 조종 입력 표시 ON→적용→출격하여 아래 가운데 스틱 커서를 확인한다. 위쪽 입력은 화면 위로, 해제하면 중심, Mode 1/2 축 위치가 맞아야 한다. OFF→적용은 입력 표시만 숨기고 고도계·비행 HUD는 유지한다. 적용 전 취소·기본값 복원→취소/적용·저장 후 재실행도 확인한다. 임시 기본 OFF를 최종 사양으로 판정하지 않는다.
8. 1280×720·1920×1080에서 5메뉴 크기/간격·입력 표시 위치/가림을 실제 패드로 확인한다. Bluetooth 분리/재연결·키보드/패드 혼합 현상은 기록하되 미정 정책을 Pass 기준으로 만들지 않는다. 로비 Racing 출격에서 1~5 안내/전환 없음, 시험 Route 맵에서 기존 1~5/랜덤 유지 확인. 팀원 지형은 LFS 수신됐지만 제품 연결·PlayerStart·완주/복귀 결정 전에는 완주 확인 항목이 아니다(RACING-TERRAIN-LINK-01).

통합 로비/맵 이동은 FrontEnd에서 확인한다. 독립 Tutorial 8맵·Story 4맵·Racing 1맵은 Boot 상태에만 적용되는 기본 Mission Entry가 있어 직접 Play도 가능하다. 선택 Mission이 없는 보존된 공유 시험장은 별도 기능 종합 시험장이다.

## 3. Blueprint에서 이미지 교체

`/Game/Drone/FrontEnd/UI/WBP_DroneFrontEndRoot`를 열고 **Class Defaults → Drone → Front End → Artwork**에서 아래 슬롯에 Texture를 드래그한다. C++를 수정하거나 PNG 파일 절대 경로를 입력할 필요가 없다.

| 슬롯 | 제공 자산 | 역할 |
|---|---|---|
| Title Background Texture | `T_Title_Background` | 배경 `Background_1.png` |
| Title Overlay Texture | `T_Title_Overlay` | 좌측 어두운 패널 `Background_2.png` |
| Title Logo Texture | `T_Title_Logo` | `Main_LOGO.png` |
| Button Normal Texture | `T_Title_ButtonNormal` | `Unselect.png` |
| Button Hovered Texture | `T_Title_ButtonHovered` | `Select.png` |
| Button Pressed Texture | `T_Title_ButtonPressed` | `Click.png` |

Texture 위치는 `/Game/Drone/FrontEnd/Textures/Title`이다. 원본 PNG는 수정하지 않았고 투명도를 유지했다. 제공 버튼은 734×429 투명 캔버스에 실제 그림이 작게 들어 있으므로 `Use Provided Button Atlas Regions`를 켜 UV로 여백만 제외한다. 나중에 버튼 크기에 딱 맞는 PNG로 교체하면 이 옵션을 끈다.

- 현재 WBP Designer는 C++ 기본 화면을 사용하는 구조다. WBP Class Defaults에서 외형을 바꾸면 기본 화면에도 적용된다. 모든 Designer 노드를 수작업 배치한 최종 UI 제작 완료라고 표현하지 않는다.
- 런타임에 Texture 변수를 바꿀 때 `Refresh Artwork`를 호출한다.
- 미션별 썸네일은 해당 `DA_Mission_*`의 `Thumbnail`에 넣는다. 레이싱은 임시로 제공 배경을 지정했고, 선택한 수업/Story에 Thumbnail이 없으면 `TitleBackgroundTexture`를 사용한다. 기체 Definition의 `PreviewMesh / PreviewActorClass`는 유지하지만 이번 역할 도식에는 실제 모델을 렌더하지 않는다.
- 직접 Designer를 만들면 `TitleBackgroundImage / TitleOverlayImage / TitleLogoImage / MissionThumbnailImage`라는 `Image` 이름을 쓰면 C++ 연결을 재사용한다. 추가 배경 이름은 `LobbyBackgroundImage / BriefingBackgroundImage / SettingsBackgroundImage`, 브리핑 이미지 이름은 `BriefingThumbnailImage`다. 기존 필수 패널·버튼·텍스트 이름도 유지한다.
- 훈련 하위 탭 컨테이너 이름은 `TrainingCategoryTabs`, 버튼 이름은 `TutorialTabButton / RacingTabButton`이다. `MissionTabButton` 이름/API는 기존 WBP 호환용으로 남고 런타임에는 숨긴다. 동적 목록은 `MissionButtonsColumn`이라는 VerticalBox에 자동 구성할 수 있다. 자체 카드 UI라면 `Get Visible Mission Ids`로 목록을 만들고 `Select Lobby Mission`을 호출한다. 우측 목표 텍스트는 `MissionObjectiveSummaryText`다.
- `Receive Lobby Category Changed`, `Receive Lobby Mission Selection Changed` 이벤트에서 자체 탭/카드 애니메이션을 붙일 수 있다. 이 이벤트 안에서 Flow를 중복 전환하지 않는다.

### Story 선택 화면: 제공 Select_UI 연결·배치

원본은 `C:\Users\Metacon_41\Downloads\새 폴더\Select_UI`, 생산 Texture는 `/Game/Drone/FrontEnd/UI/SelectUI`다. **배경1개와 미션 프리뷰4개만 이미지로 쓰고 글자는 모두 Pretendard의 실제 `UTextBlock`으로 표시한다.** Back·제목·미션 이름·상세/무전·START를 글자 PNG로 대체하지 않는다. 첨부 시안의 빨강/노랑/초록 영역은 배치 설명용 표시이지 실제 컬러 패널이 아니다. 기존 타이틀 아트와 훈련·레이싱 동작/그림은 보존한다.

`WBP_DroneFrontEndRoot > Class Defaults > Drone > Front End > Select UI`:

| 속성 | 사용법 |
|---|---|
| `bUseStorySelectUI` | Story 전용 배치·배경/프리뷰 사용. 끄면 기존 배치로 복귀하며 글자는 계속 동적 텍스트 |
| `StorySelectAssets.Background / Thumbnails` | 배경1개·M1~M4 순서의 프리뷰4개. 글자가 들어간 다른 Texture 슬롯은 사용하지 않음 |
| `InterfaceFont` | 일반 글자용 `/Game/Drone/UI/Fonts/Pretendard/Pretendard_Regular_Font` |
| `InterfaceBoldFont` | 제목·강조용 `/Game/Drone/UI/Fonts/Pretendard/Pretendard_Bold_Font` |
| `StorySelectLayout` | 1920×1080 기준 좌표/크기. `ListPosition / ListWidth`, `ThumbnailPosition / ThumbnailSize`, `DetailsPosition`, `StartPosition / StartSize`, `BackArtworkPosition / HeadingPosition` 조정 |

시작 배치는 목록 `(117,321)`·폭389, 프리뷰 `(556,350)`·`584×543`, 설명 `(1248,321)`, START `(695,980)`·`530×58`이다. 제목/설명도 실제 글자의 폭·줄바꿈을 사용하므로1280/1920에서 겹침·끝 잘림을 보고 Layout/텍스트 박스를 조정한다. 텍스트가 길다는 이유로 부모 전체 Scale을 늘리거나 글자를 이미지로 굳히지 않는다.

기존 MissionId로4개 프리뷰를 찾으며 M3도 `Mission.Story.VeilBreaker.Test` ID를 유지한다. 이름·영문명·설명·목표·무전은 Mission DA의 동적 값을 사용하므로 기획 문구 수정 때 텍스트PNG를 다시 만들 필요가 없다. Back/Heading/MissionLabel/Start·Selected/Unselected·Details의 구형 필드와 원본/이미 임포트한 텍스트PNG16개는 호환·원본 보존을 위해 삭제하지 않지만 화면에는 쓰지 않는다. 프리뷰 미지정 시 기존 DA/배경 fallback과 Tooltip 계약을 유지한다.

`Tools/AssetMigration/ImportDroneSelectUI.py`는 배경/프리뷰5개와 위 Story WBP 기본값만 가져온다. 다른 PC 원본 위치는 `DRONE_SELECT_UI_SOURCE`로 지정하고, `DRONE_SELECT_UI_VERIFY_ONLY=1`은 기존 임포트/기본값을 읽기 검사한다. 타이틀8개 기본값·Designer 트리·맵·Mission DA는 변경하지 않는다. 보고서 위치는 `Saved/Automation/SelectUI/ImportDroneSelectUI.json`이다.

폰트 설치/연결 도구는 `Tools/AssetMigration/ImportDronePretendard.py`다. **일반 Editor의 `-ExecutePythonScript`로 실행한다.** FontFactory는 Slate 서비스가 필요하므로 `-run=pythonscript` commandlet로 가져오지 않는다. 공식 [orioncactus/pretendard@v1.3.9](https://github.com/orioncactus/pretendard/tree/v1.3.9)의 변형하지 않은 Regular/Bold를 사용하고 원본 해시를 대조한다. 다운로드 원본은 임포트용 `Saved/Automation/SelectUI/FontSource`에 두며 다른 위치는 `DRONE_PRETENDARD_SOURCE`로 지정한다. `DRONE_PRETENDARD_VERIFY_ONLY=1`은 저장된 연결을 읽기 검사하고 보고서는 `Saved/Automation/SelectUI/PretendardImport.json`이다. FontFace는 **Inline으로 프로젝트 자산에 포함**하므로 팀원/실행 PC의 OS에 폰트를 따로 설치할 필요가 없다. OFL 고지는 `Content/Drone/UI/Fonts/Pretendard/License/Pretendard-LICENSE.txt`를 보존하고 `DefaultGame.ini`의 NonUFS 스테이징으로 배포에 포함한다. 새 USTRUCT/UPROPERTY가 있어 Editor 종료 후 Build가 먼저이며 Live Coding만으로 가져오지 않는다. 현재 빌드/임포트/검증 완료 여부는 STATUS·WORKLOG를 따른다.

확인 순서: FrontEnd→스토리→M1~M4 선택→프리뷰·DA의 글자/무전 교체·선택 강조→START→뒤로 복귀 순으로 본다. 일반/굵은 한글에 Pretendard가 적용되고 긴 문구가 잘리지 않는지, 텍스트PNG Image가 숨겨졌는지도 확인한다. 마우스뿐 아니라 키보드/패드 첫 강조·목록 이동·START·Back을 확인한 뒤 튜토리얼/레이싱·타이틀 아트가 그대로인지 본다. 자동화 대상은 `Drone.UI.SelectUILayoutContract / SelectUIPresentationPIE`, 캡처는 `Saved/Automation/SelectUI/story_m1~4.png`이며 생성/통과 여부는 STATUS·WORKLOG를 따른다. 캡처나 계약 테스트가 실제 패드/화면 수동 Pass를 대신하지 않는다.

### 프로젝트 공통 Pretendard

메뉴뿐 아니라 비행 HUD·미션 목표/결과/일시정지·기체 선택·설정·시드 입력·로딩·카운트다운의 일반 글자는 같은 임베드 Regular/Bold를 쓴다. `Source/Drone/UI/DroneUIFont`가 글꼴만 교체하고 크기·굵기·간격·외곽선·색·배치는 유지한다. `UDroneUserWidget`은 생성/Preview/속성 동기화 때 Designer 글꼴과 입력칸·Combo의 실제 표시 글자를 반영하며 매 Tick 전체 트리를 순회하지 않는다. 동적으로 자식 UI를 추가한 뒤에는 BP `RefreshProjectFonts`로 반영한다. 폰트 폴더는 AlwaysCook, OFL 고지는 NonUFS로 포함한다. OS 설치나 엔진 CoreStyle 변경은 하지 않는다.

`Drone|Typography`의 `bUnifyDesignerFonts`는 기본 True다. 합의된 특수 서체만 False 또는 `FontOptOutWidgetNames`의 정확한 위젯 이름으로 제외한다. 아이콘 글꼴·Vendor/Legacy 위젯·Editor/디버그 글씨는 변경하지 않는다. 숨김 기본인 시험 오브젝트의 `TextRender` 월드 라벨은 Offline/거리필드 폰트가 필요하므로 Runtime UFont를 억지로 연결하지 않는다. RichText는 기본 스타일을 통일하며 별도 태그별 스타일표를 새로 도입한다면 해당 표도 조정해야 한다.

선택 목록 이름 끝의 `(시험)` 등 괄호 부연은 표시할 때만 제거한다. DA 원문·설명/툴팁·영문 부제·MissionId·맵 경로·기록 키는 유지한다. `Drone.UI.FontContract / PlayerWidgetFontsPIE / SelectionDisplayLabelContract`와 `Tools/Validation/AuditDroneUIFontSources.py`가 이 경계를 확인하며 실행 결과는 WORKLOG를 따른다.

### 직접 WBP를 만들 때 유지할 API와 이름

- 5메뉴 API는 OpenLobbyForCategory/OpenStoryLobby/OpenRacingLobby/OpenTutorialLobby/RequestExitGame이며 TitleMenuClass는 WBP_DroneFiveItemMenu의 StoryButton/RacingButton/TutorialButton/SettingsButton/ExitButton과 OnStoryRequested/OnRacingRequested/OnTutorialRequested/OnSettingsRequested/OnExitRequested 계약을 지킨다. FinishOpeningTrailer·OpenTrainingLobby는 호환용. 선택/확정 SelectLobbyMission/ConfirmSelectedMission, 브리핑 FinishMissionBriefing, Back NavigateBack을 유지한다.
- FrontEnd 필수 이름은 `OpeningPanel / LobbyPanel / MissionBriefingPanel`, `ContinueButton`, `OpeningTitleText / LobbyTitleText / LobbyStatusText`, `MissionSelectButton / MissionSelectButtonText`, `MissionNameText / MissionDescriptionText / MissionMetaText`, `StartMissionButton`, `MissionBriefingTitleText / MissionBriefingBodyText`, `FinishMissionBriefingButton`이다. Back 버튼은 `LobbyBackButton / BriefingBackButton`으로 연결한다.
- 기체 선택의 필수 이름은 `DroneSelectionPanel`, `MissionNameText`, `DroneNameText / DroneDescriptionText / DroneProfileText`, `DroneButton0`~`DroneButton4`, 각 `DroneButton0Text`~`DroneButton4Text`, `ControlModeButton / ControlModeButtonText`, `LaunchDroneButton`이다. `SelectionBackButton`을 쓰면 기본 Back 처리를 재사용한다. 폐기된 속도 단계의 `HandlingPresetButton / HandlingPresetButtonText`는 호환용으로 숨긴다.
- 조작 이름은 `쉬운 조작 / 게임 조작 / FPV 모드 1 / FPV 모드 2`다. FPV 1·2는 시점이 아닌 스틱 배치 차이이며 기존 입력·enum·저장 ID는 유지한다. 선택적 `ControlModeHintText` 이름의 TextBlock을 두면 설명을 표시한다. 공통 초기 레이아웃 보정은 Button 내부 슬롯 Fill·padding0, Label no-wrap/WrapAt0·최소폭300, selector 최소420×72를 적용한다. 폭을 고정한 좁은 SizeBox/Canvas를 보정하지만 모든 임의 WBP 부모 제약을 해결하는 것은 아니다. native 화면과 named-tree fixture의 1280/1920 Slate 배치 검증은 렌더된 실제 WBP/패드 수동 확인과 구분한다. 상세 검증은 [WORKLOG](../history/DRONE_WORKLOG.md).
- 기체 카드 입력은 `Select Drone`, 조작 전환은 `Toggle Control Mode`, 출격은 `Confirm And Launch Selected Drone`이다. `Receive Drone Selection Refreshed`에서 최종 카드/모델 연출을 붙일 수 있으며 실제 승인과 Pawn Spawn은 기존 Flow/Controller가 담당한다.
- 설정 Host에는 `SettingsPanel`과 `UDroneSettingsWidget` 타입의 `SettingsWidget`을 넣고 `Set Settings Visible`로 열고 닫는다. 설정 위젯 자체의 Designer 노드는 이름만으로 자동 Bind되지 않는다. 기본 native 위젯을 재사용하거나 아래 9절의 공개 API에 직접 연결한다.

## 4. 탭과 미션 데이터

### 현재 결과창 배치와 확인

`UDroneMissionResultWidget`의 native 기본 화면은1920×1080 기준 화면·왼쪽 그라데이션/제목/상자 버튼열·오른쪽 정보 카드다. `TitleKit`의 팀원 버튼 자산을 사용한다. 이전 중앙680/청록 카드 설명은 현재 native 화면이 아니라 과거 기록이다. 이름 계약의 자체 WBP 경로는 유지한다.

- 결과창 실제 포커스 배율은1이다. native+유효TitleKit은 버튼 자산의 선택 상태를 사용하며, 자체 WBP/카드 fallback은 색·테두리 강조다. `GamepadFocusScale`은 직렬화 호환으로 남고 옛1.06도 런타임 확대하지 않는다.
- Class Defaults → `Drone | Mission Result | Layout`: `TitleKit`, `TitlePosition / TitleFontSize`, `FirstButtonPosition / ButtonPitch / ButtonFontSize`, `InfoPanelPosition / InfoPanelWidth`로 조절한다. 현재 정보 폭900은 소스 기본값이며 저장된 개별 WBP override는 따로 확인한다.
- 자체 WBP 필수 이름: `MissionResultPanel / MissionResultTitleText / RetryMissionButton / ReturnToLobbyButton`. 선택 이름: `MissionResultDetailText / NextMissionButton / NextMissionButtonText / RetryMissionButtonText / ReturnToLobbyButtonText`. 결과 위젯 클래스는 Mission PlayerController의 `MissionResultWidgetClass`에 지정한다.
- 이름 계약 WBP는 작성한 부모 Canvas/SizeBox/이미지 트리를 교체하지 않는다. 과도한 고정 크기는 Designer에서 조절한다. native+Kit은 자체 WBP/카드용 예전 스타일 보정을 건너뛴다.
- 시드 도시 결과의 일반 다시하기는 새 시드, `Same Seed`는 같은 조건 재도전이라는 코드 계약이다. 실제 결과/기록 재현은 아직 확인해야 한다.
- 실제 화면 확인: 1280×720/1920×1080에서 성공·실패·다음 없음·훈련 전체 완료·시드 레이싱 결과를 본다. 버튼열/정보/긴 글자 잘림·선택 상태와 다음·재도전·로비/시작 메뉴 전환을 확인한다. 옛680 fixture 검사 통과를 현재 팀원 자산 화면 Pass로 대신하지 않는다.

담당 클래스는 `UDroneMissionDefinition`과 `UDroneFrontEndRootWidget`이다.

- DA의 `Lobby Category`: Tutorial / Racing / Mission. `Auto`는 기존 저장 DA 호환용이며 ID 접두어로 분류한다.
- Auto 규칙: `Mission.Tutorial.*` → 튜토리얼, `Mission.Racing.*` → 레이싱, 그 외 → 미션.
- 미션 목록은 Flow Catalog 등록 항목에서 읽는다. `DefaultMissionPaths`와 함께 `/Game/Drone/Data/Missions`의 유효 Definition을 Asset Registry로 자동 등록하는 코드가 있다. DA 생성/유효성만으로 실제 제품 맵의 Gate·GameMode·완주가 보장되지는 않는다.
- 분류와 맵은 독립적이다. `Lobby Category`를 바꾸면 표시 탭만 바뀌고 실제 이동 맵은 `Mission Map`이 결정한다.
- 기존 8개 수업과 Story 4개는 보존했고, 새 `DA_Mission_Racing_Circuit_Test`만 Catalog에 추가했다.
- 현재 소스/DA 계약은 스토리→Mission(4), 레이싱→Racing(2: Circuit.Test/Procedural.Test), 튜토리얼→Tutorial(9) 직접 진입이다. Back은 분류·선택과 진입 메뉴 포커스를 복원한다. 현재HEAD의 실제 목록 검사는 미실행이다.
- 완료 미션·Story Fact·튜토리얼 권장문구 표시 여부는 Flow의 `Saved/SaveGames/DroneMissionProgress.json`로 저장/복원한다. 성공 결과와 권장 표시 변경 때 저장하며 실패하면 이번 실행 동안만 유지 경고를 낸다. 실제 성공→종료→재실행 후 로비 완료 표시/Story Fact 복원을 확인하고 사용자 기록을 임의 삭제하지 않는다.

### 시드 레이싱·로딩·일시정지 확인

`ADroneProceduralCityGenerator`는 도시·날씨·코스를 단계 생성하고 같은 시드를 다시 사용할 수 있다. 지정/무작위 시드·난도별 기록을 확인하되 팀원 고정4코스 완성으로 표시하지 않는다. 미션 Controller는 생성/Story 준비 중 로딩과 취소, 미션 중 Esc/Start 일시정지·재개·재시작·타이틀 복귀를 연결한다. 일시정지 재시작은 같은 도시 시드를 예약한다. 로딩/기체 선택/결과 화면은 미션 중 Pause와 별도 뒤로 처리를 사용한다. 실제 프레임 정지/취소 복귀/재생성·첫 포커스는 현재HEAD Build/회귀 뒤 확인한다.

## 5. 회전 = 원형 코스 비행

이전 `동쪽 90° 바라보기 → 1초 유지`는 이번 수업의 의미가 아니므로 연결을 해제했다. `ADroneTutorialHeadingZone` 클래스와 Event는 별도의 방향 정렬 시험 및 기존 자산 호환을 위해 삭제하지 않았다.

호환을 위해 자산 이름/ID는 `DA_Mission_Tutorial_Heading / Mission.Tutorial.Heading`을 유지하지만 표시명과 규칙은 원형 코스로 바뀌었다.

- Actor: 보존된 공유 시험장의 `TutorialMissionTest_OrbitCourse` (`BP_DroneTrainingCourse`)를 바탕으로 독립 Heading 맵의 Orbit Station을 구성했다. 현재 DA는 독립 맵을 사용하며 기존 공유 Hover/다른 배치는 보존했다.
- Spline: 반지름 약 10m, 닫힌 곡선. 위치/반경/고도는 시험용 값이며 최종 난이도가 아니다.
- 순서: 시작 Gate 0 → 체크포인트 1~7 → 결승 Gate 8 → Return Zone.
- 결승은 Spline 전체 길이 L에 두어 **7/8 바퀴를 돌고 완료하는 오류를 막는다**. 시작 Gate와 겹치지 않도록 결승만 진행 방향으로 2.5m 떨어뜨렸다.
- Rule Event: `TrainingLap`, TargetId: `Tutorial.Orbit.Course`. 기존 게이트 수업은 `Tutorial.GateFlight.Course`다.
- Director가 Tag에 맞는 코스 Recorder만 구독하고 다른 코스 선/Trigger를 끈다. HUD도 동일한 Recorder를 사용한다.
- 원순서 건너뛰기, 역방향 통과, 제자리 Yaw, 다른 코스 완주는 이 목표를 완료시키지 않는다.
- Course Spline, Automatic Gate Count/배치, Gate Scale/크기와 Rule Time Limit은 BP/맵 Details에서 조절한다. 변경 후 순서·결승 위치를 다시 테스트한다.

구현 책임: Course가 경로와 Gate 생성, Gate Sequence가 순서/정방향, Lap Recorder가 시간·거리·평균 속도, Mission Director가 Lap→귀환→결과 전환을 맡는다.

## 6. 실제 드론 Mode 1 / Mode 2는 물리 모드인가

아니다. **송신기 스틱 축 배치**다. DJI 공식 제어 규격도 Mode 1/2를 이렇게 구분한다. [DJI 공식 스틱 배치](https://developer.dji.com/iframe/mobile-sdk-doc/android/reference/dji/common/remotecontroller/DJIRCControlStyle.html)

| 조작 | 왼쪽 세로 | 왼쪽 가로 | 오른쪽 세로 | 오른쪽 가로 |
|---|---|---|---|---|
| Mode 1 | Pitch(앞뒤 기울기) | Yaw(방향 회전) | Throttle(추력) | Roll(좌우 기울기) |
| Mode 2 | Throttle(추력) | Yaw(방향 회전) | Pitch(앞뒤 기울기) | Roll(좌우 기울기) |

반면 Angle/Acro(Rate)는 비행 제어 방식이다. Angle은 스틱으로 목표 기울기를 주고 수평 복귀를 지원하며, Acro는 회전 속도를 명령한다. Betaflight의 Acro/Angle 설명과 대응한다. [Betaflight 공식 제어 모드 설명](https://betaflight.com/docs/wiki/getting-started/setup-guide#mode-settings)

현재 코드는 Mode 1/2 세로 스틱 매핑만 다르고 같은 질량·합산 최대 추력·모터 응답 지연·중력·기체 Up 방향 추력·선형/제곱 항력 모델을 공유한다. 키보드는 두 모드 모두 W/S Pitch, A/D Roll, Q/E Yaw, Space/Ctrl Throttle로 동일하다.

실제에 가까운 방향은 있지만 실제 기체 1:1 물리 구현은 아니다. 개별 모터 힘/토크, 관성 텐서, 실제 센서·PID 제어기·Mixer·공력까지 교정한 시뮬레이터가 아니며 `UFloatingPawnMovement` 기반의 단순화 모델이다. Easy 조작의 자동 보조도 실제 Acro와 같다고 말하면 안 된다. 이번 작업에서는 비행 물리를 임의 변경하지 않았다.

## 7. 미션마다 맵을 나누는 게 좋은가

사용자의 후속 요청으로 **튜토리얼 8개 수업별 시험맵을 실제 분리**했다. Story 4개·Racing 1개 독립 맵을 유지하며 13개 맵 모두 직접 Play용 기본 Mission Entry를 갖는다. [전체 맵과 비/물리 점검 가이드](DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md)

- Story 미션은 장소·목표·성능·팀 작업을 분리하기 좋다. 이미 Story TestMap 4개가 분리되어 있다.
- 레이싱은 이번에 `Lvl_DroneRacingTest`를 별도 생성했다. NPC나 다른 수업의 Trigger 없이 완주를 시험한다.
- 튜토리얼 공유 맵은 종합 확인용으로 보존했다. 각 DA MissionMap은 `TestMap/Tutorial/Lvl_Tutorial_*_Test`의 해당 수업 맵을 가리킨다.
- 분리할 때 **C++/BP 기능은 공유하고 배치와 DA의 Mission Map만 다르게** 한다. 미션마다 매니저 코드를 복제하지 않는다. 맵 개수 증가 자체가 런타임 부하를 의미하지 않지만, 중복 환경 자산은 저장소 용량과 수정 부담을 늘린다.
- 각 새 맵에는 Mission GameMode, PlayerStart, 해당 Rule의 대상 Actor/Tag만 두고 FrontEnd OpenLevel 경로와 패키징 포함을 확인한다.
- 팀원 Production `Lvl_DroneTraining`은 합의 전 저장·분할·덮어쓰기하지 않는다. 이번에도 손대지 않았다.

## 8. 도구 재실행 경계

당시 세션 원문은 [WORKLOG](../history/DRONE_WORKLOG.md)에 보존했다. 현재 구현·검증은 [STATUS](../../STATUS.md)를 따른다.

현행 ConfigureDroneTitleLobby.py/Invoke-DroneTitleLobby.ps1은 WBP 이미지·Racing DA 설명/허용 기체/목표 Rule·Heading/GateFlight DA 문구를 도구 값으로 덮어쓸 수 있다. 10/04 Best Lap JSON 설명은 현재 DA와 일치하도록 수정됐으며 구버전 설명 복귀 문제는 해소됨. 최초 이미지 가져오기는 DRONE_TITLE_ASSET_DIR 또는 -TitleAssetDir 지정 필수(개인 폴더 기본값 제거). 수동 변경 뒤 의도 없이 재실행하지 않는다. 10/01 이전 D PC UI 5/5 원시 TrainingLobbySettings 보고서는 현재 C PC에 없으며 당시 원문은 WORKLOG에 보존했다.

## 9. 사운드 · 화면 · 성능 설정

설정은 타이틀의 설정 메뉴로 연다. `UDroneSettingsWidget`이 현재값을 읽어 편집을 시작하며 Root의 Back/Esc/패드 B도 같은 취소 경계를 사용한다.

| 항목 | 제공 선택 | 적용/저장 경계 |
|---|---|---|
| 전체 음량 | 0~100%, 1% 간격 | 즉시 미리보기, 적용 때 `DroneAudioSettings` SaveGame(UserIndex 0)에 저장 |
| 화면 모드 | 창 / 테두리 없는 창 / 전체 화면 | Standalone·Game World에서 적용, `GameUserSettings` 저장 |
| 해상도 | 1280×720 / 1920×1080 / 2560×1440, 현재값 보존 | Standalone·Game World에서 적용, `GameUserSettings` 저장 |
| 그래픽 품질 | 낮음 / 보통 / 높음, 기존 최고·시네마틱·사용자 지정값 보존 | 변경한 항목만 적용, `GameUserSettings` 저장 |
| 프레임 제한 | 무제한 / 30 / 60 / 120 FPS, 현재값 보존 | 변경한 항목만 적용, `GameUserSettings` 저장 |
| 수직 동기화 | On / Off | 변경한 항목만 적용, `GameUserSettings` 저장 |

- Apply는 변경한 값만 확정하며 성공 후 편집 기준을 새 적용값으로 갱신한다. 화면을 자동 닫지는 않는다. 전체 음량 저장 실패는 상태 메시지로 표시하고 다시 적용할 수 있게 한다.
- 기본값은 음량 100%, 테두리 없는 창·1920×1080, 품질 보통, 60 FPS, VSync On이다. 먼저 편집값으로 준비하며 Apply 전에는 화면/성능을 저장하지 않는다. 음량은 미리보기한다. PIE에서는 기본값 복원도 창/해상도를 변경하지 않는다.
- Back/Esc/패드 B는 미적용 음량을 편집 시작값으로 되돌리고 화면/성능 편집값을 버린다. 이미 Apply한 값은 유지한다.
- PIE/Designer에서는 창 모드와 해상도 컨트롤을 비활성화하고 Standalone 안내를 표시한다. 품질/VSync/FPS 적용은 비해상도 경로를 사용해 Editor 창 크기를 바꾸지 않는다. 실제 디스플레이 변경은 Standalone에서 확인한다.
- `UDroneAudioSettingsSubsystem`은 같은 GameInstance의 맵 이동 뒤에도 전체 음량을 적용하고 재실행 시 SaveGame을 복원한다. 다른 GameInstance/Editor 오디오에는 적용하지 않는다. 저장 없음·다른 타입·비정상 수치에는 기본 음량을 유지한다. UI 사운드 원본은 `ButtonHoverSound / ButtonClickSound` 슬롯에 별도로 지정하며 미지정이면 무음이다.
- 공개 API는 `Refresh From Current Settings / Set Master Volume / Get Master Volume / Apply Pending Settings / Restore Defaults / Cancel Pending Settings / Request Close / Are Display Settings Available`, 닫기 이벤트는 `On Close Requested`다. pending 품질·해상도·VSync·FPS getter도 제공한다.
- native 설정 컨트롤 이름은 `MasterVolumeSlider`, `DisplayModeCombo`, `ResolutionCombo`, `GraphicsCombo`, `FrameRateCombo`, `VSyncCheck`, `RestoreDefaultsButton / ApplySettingsButton / SettingsBackButton`이다. 이 이름은 기본 WidgetTree를 점검할 때 사용하며 자체 Designer의 자동 바인딩을 보장하지 않는다.

구현 소스: `Source/Drone/UI/DroneFrontEndRootWidget.*`, `DroneSelectionWidget.*`, `DroneSettingsWidget.*`, `DroneAudioSettingsSubsystem.*`. 실제 화면·가청 변화·재실행 저장 복원은 현재 PC의 수동 확인이 남아 있다.

## 10. 목록 튐 진단 (수정 전)

당시 세션 원문은 [WORKLOG](../history/DRONE_WORKLOG.md)에 보존했다. 현재 구현·검증은 [STATUS](../../STATUS.md)를 따른다.

## 11. 패드 UI 확인 범위

당시 세션 원문은 [WORKLOG](../history/DRONE_WORKLOG.md)에 보존했다. 현재 구현·검증은 [STATUS](../../STATUS.md)를 따른다.

## 배터리·신호 대역·HUD 조정 (2026-10-02 새벽, C PC)

당시 세션 원문은 [WORKLOG](../history/DRONE_WORKLOG.md)에 보존했다. 현재 구현·검증은 [STATUS](../../STATUS.md)를 따른다.
