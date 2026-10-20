# 시작 화면 · 로비 탭 · 원형 코스 가이드

현재 절차 기준: 2026-10-20 D PC. 기존5메뉴·결과·훈련/레이싱을 유지한다. 훈련/레이싱 사진은 DA 슬롯, 장치 그림은 조작 안내 WBP에서 조정한다. 사용자 확인 배치의 네모형 RC 그림을 실제 WBP에 연결했다. 실제 검증 범위는 [STATUS](../../STATUS.md), 실행별 근거는 [WORKLOG](../history/DRONE_WORKLOG.md)를 따른다. 원본 이미지·Figma·기존 타이틀 아트는 보존한다.

## 화면별 WBP 편집 정본

Content Browser에서 아래 이름으로 검색하고 Designer를 연다. 경로는 `/Game/Drone/UI/WBP`다. 실행 진입 `FrontEnd/WBP_DroneFrontEnd`와 Root는 화면을 묶는 호스트이며, 개별 화면 배치는 아래 자산에서 조정한다.

| 화면 | 편집 자산 |
|---|---|
| 타이틀 배경·로고 / 메뉴 버튼 | `FrontEnd/WBP_DroneTitleScreen` / `WBP_DroneFiveItemMenu` |
| 임무·훈련·레이싱 선택창 | `FrontEnd/WBP_DroneLobby` |
| 반복 목록 한 줄·선택 강조 | `FrontEnd/WBP_DroneMissionListItem` |
| 출격 전 사진·조작 안내 | `FrontEnd/WBP_DroneBriefing` / `WBP_DroneControlsGuide` |
| 튜토리얼 권장 안내 | `FrontEnd/WBP_DroneTutorialRecommendation` |
| 미션 영상·건너뛰기 안내 | `FrontEnd/WBP_DroneCinematic` |
| 설정 / 시드 입력 | `FrontEnd/WBP_DroneSettings` / `WBP_DroneSeedInput` |
| 기체 선택 / 시작 안내 | `Mission/WBP_DroneSelection` / `WBP_DroneMissionStartPrompt` |
| 결과 / 일시정지 / 로딩 | `Mission/WBP_DroneMissionResult` / `WBP_DroneMissionPause` / `WBP_DroneProceduralLoading` |
| 비행 중 전체 HUD | `HUD/WBP_DroneFlightHUDKit` ([세부](DRONE_MISSION_FRAMEWORK_GUIDE.md#hud-편집-정본)) |

Native 미션 출격도 BeginPlay에서 위 Mission WBP 기본 화면7종을 로드한다. 별도 BP에서 지정한 위젯 클래스는 유지한다. 이전에는 Native GameMode가 C++ 기본 화면을 열어 저장된 WBP 편집/한글이 빠지는 경로가 있었고 이를 연결했다. Mission WBP 폴더는 Cook 목록에도 포함한다(실제 패키징 검사는 별도).

- 바깥 배치는 Canvas Slot의 앵커·위치·정렬, 크기는 SizeBox/Slot, 안쪽 간격은 가로/세로 Box Slot Padding에서 맞춘다. 계층 표시명은 한글 문구·이미지 파츠·가로/세로 배치로 구분했다. 연결에 쓰이는 내부 이름은 유지한다.
- 로비·브리핑·기체 선택·출격 안내의 시작 버튼은 오른쪽 아래 앵커/정렬 `(1,1)`, 위치 `(-80,-40)`, 크기 `(300,80)`로 통일했다(1920 기준·해상도별 DPI 적용). Designer에서 바꾼 위치를 실행 코드가 다시 중앙으로 덮어쓰지 않는다.
- 로비·브리핑·기체 선택 사진의 외곽 상자는 `600×360`, 안쪽 여백은14px다. 모서리 테두리는 길이24·두께2의 Image 파츠8개로 나눴다. 각각 `MissionCardPanel / BriefingThumbnailFrame / DronePreviewFrame`을 찾아 위치·크기·Padding을 조정한다. 지도 사진은 Scale To Fill로 상자를 채운다. UGV는 제공 사진의 기체가 잘리지 않도록 `bFitGroundDronePhoto=True`의 Scale To Fit을 쓴다.
- 정적 문구는 해당 TextBlock의 Text를 편집한다. 미션명/설명/목표/시간은 Mission DA에서 바꾼다. 데이터가 갱신하는 문구를 화면별로 고정하려면 Class Defaults의 `Drone|문구` → `TextOverrides`에 정확한 위젯 이름과 문구를 넣는다. 배열 값/키 이름은 내부 API이므로 한글 표시 문구와 구분한다.
- 일반 버튼의 Class Defaults `UnselectedButtonOpacity` 기본0.55, `SelectedButtonOpacity` 기본1이다. 목록의 선택 항목과 포커스/호버 항목을 강조한다. 반복 줄 바깥 간격은 `WBP_DroneMissionListItem`의 `ListItemPadding`이다.
- 기체 사진의 회색 바탕은 `DronePreviewBackdrop` Brush Color 알파0으로 제거했다. 바깥 도시 배경은 `SelectionBackground`의 원본 `T_Select_Background`와 `SelectionBackgroundDim`으로 유지한다. 전체 배경은 Stretch Canvas/Z 순서0~3, 사진 프레임은 기존 모서리 파츠다. 일회성 `-DroneRepairSelectionBackdrop`은 이 WBP 한 개만 저장한다. 확인 기준은 FrontEnd→미션1→드랍드론 선택의 실제 PIE 화면이다.
- 타이틀 설정창은 화면 형제보다 높은 Z Order로 열리고, 일시정지 설정은 재개 후 다시 열어도 `뒤로`가 연결된다. 위치/크기는 해당 WBP에서 조정한다. 허브 대사 박스는 기본 숨김이며 필요할 때만 Root의 `bShowHubDialogue`를 켠다. 미션 영상 안의 자막은 별개다.
- 지도 사진은 DA의 `Thumbnail / BriefingImage`에 **테두리 없는 사진**을 연결한다. 저장된 화면에서 옛 `T_Select_M*_Image`의 테두리 포함 Story Override를 다시 덧씌우지 않는다. `MissionImageBackground / BriefingThumbnailBackground`는 투명·Padding0이며 바깥 모서리 Image로 테두리를 조정한다.
- 배경/로고/화살표·조작 장치 그림은 각각 Image의 Brush, 버튼 그림은 Style의 Normal/Hovered/Pressed에서 바꾼다. 제공 Select_UI/Title Kit를 저장 연결했다. 새 화면의 정적 그림·글자 크기·Slot Padding을 런타임이 재작성하지 않는다.
- 조작 안내는 Diagram Switcher와 Legend Switcher에 장치3종을 모두 저장했다. 각 장치의 그림·번호·범례 TextBlock을 따로 편집하며 탭 전환은 저장된 파츠를 보여 주기만 한다. `GamepadGuide/KeyboardGuide/RCControllerGuide`는 Native 폴백 생성 데이터이며, 저장된 WBP 범례 문구는 Designer에서 직접 고친다.
- 한글 표시·공통 폰트를 적용했고 HUD를 제외한 화면의 간격은4px 단위, 일반 글자는 최소12로 한 번 정리했다. 그림 위 번호는 작은 원 안에 맞추며 두 자리 `10`은 원 지름의0.34배 크기로 예외 처리한다. 이후 편집값을 매 실행마다 강제하지 않는다. HUD의 기존 사용자 배치는 보존했다.
- `Drone.Tools.OrganizeAllDesigners`는 기본 읽기 전용이다. 새 화면 생성·간격 정리·타이틀/조작 안내 원본 재내보내기·시작 버튼 정렬은 각각 명시적 플래그가 필요한 일회성 도구다. 사람 편집 후 반복 실행해 재내보내지 않는다. 실제 검증/미확인은 WORKLOG를 따른다.

### UGV 사진과 미션 1 영상 교체

UGV의 `DA_Drone_GroundUGV_Greybox.SelectImage`는 `/Game/Drone/FrontEnd/UI/SelectUI/Drones/T_SelectDrone_UGV_User_20261020`에 연결했다. 사용자 제공 JPG를 그대로 사용하며, 큰 사진과 기체 카드에 함께 표시한다. 다른 사진으로 바꾸려면 같은 DA의 SelectImage를 교체한다.

스카이드론은 사용자가 지정한 `ThirdParty/DronePack/D_Mesh/DroneRacing/SM_Drone01Body/StaticMeshes/SM_Drone01Body`를 바닥 없는 스튜디오에서 실제 렌더했다. 선택 사진은 `DA_Drone_Racer_Greybox.SelectImage`의 `T_SelectDrone_SkyDrone_20261020`이며 비행 Pawn/조작 설정은 바꾸지 않는다. 원본 촬영 파일은 `SourceArt/Selection/SkyDrone_20261020.png`다. 새 촬영은 재질·텍스처 컴파일 완료 후 저장해야 체커 임시 재질이 사진에 남지 않는다.

드랍드론은 사용자 `1792480499269.png` 원본을 `DA_Drone_Drop_Greybox.SelectImage`의 `T_SelectDrone_Drop_User_20261020`에 연결했다. 원본은 `SourceArt/Selection/DropDrone_User_20261020.png`이며 픽셀을 바꾸지 않았다. 선택 WBP의 `bFitDropDronePhoto`로 전체 사진 비율을 보존해 날개가 잘리지 않게 한다.

미션 1은 로비에서 시작을 확정하면 영상 → 기존 브리핑 → 작전 지역/기체 선택으로 진행한다. 영상이 끝나거나 Esc/패드 B를 누르면 브리핑으로 넘어간다. 영상 재생 중에는 브리핑 대사와 버튼 입력을 잠시 멈춘다. 파일 재생 실패 시에도 기존 브리핑으로 복귀한다.

- 영상 파일: 프로젝트 `Content/Movies/Mission_briefing1.mp4`.
- Media Source: `/Game/Drone/FrontEnd/Media/MS_Mission01_Briefing`, File Path=`./Movies/Mission_briefing1.mp4`.
- 연결: `DA_Mission_Story_GoldenTime_Test`의 `BriefingAsset`. 다른 Story 미션에도 FileMediaSource를 연결하면 같은 재생/건너뛰기 흐름을 쓴다.
- 화면: `WBP_DroneCinematic`의 `CinematicFrameSize / OpeningMovieImage / CinematicSkipHint`에서 영상 크기·스킵 문구·위치를 편집한다. FrontEnd Controller의 위젯 클래스 참조와 Movies 패키징 목록도 저장했다. 실제 패키징 검증은 별도다.

## 0. 현재 계약 — 5메뉴·조종 입력 표시 현재 구현과 계약

기존5메뉴·조종 입력 표시 계약은 유지한다. 10/01~10/03 당시 구현/검증과 담당 구분은 WORKLOG에 보존하며, 새 Story Select_UI 변경까지 그 당시 Pass에 포함하지 않는다. 실제 패드/화면 확인은 별도다.

- 타이틀 순서: **임무 / 훈련 / 레이싱 / 설정 / 종료**. `UDroneFrontEndRootWidget::OpenLobbyForCategory(Category)`가 먼저 분류를 정한 뒤 첫 목록/포커스부터 표시한다. `OpenStoryLobby`=Mission, `OpenRacingLobby`=Racing, `OpenTutorialLobby`=Tutorial, 종료=`RequestExitGame`. 기존 `FinishOpeningTrailer`=스토리·`OpenTrainingLobby`=튜토리얼은 호환 유지. 시작 뒤 중간 화면 없음, 브리핑·기체 선택·출격·결과·복귀는 기존 흐름 재사용.
- `WBP_DroneFrontEndRoot` Class Defaults `TitleMenuClass = WBP_DroneFiveItemMenu`로 **저장 연결 완료**. 위젯 필수 버튼 `StoryButton / RacingButton / TutorialButton / SettingsButton / ExitButton`, 필수 Dispatcher `OnStoryRequested / OnRacingRequested / OnTutorialRequested / OnSettingsRequested / OnExitRequested`, 선택 `OnBackRequested`. 이름 계약을 확인해 연결하며 틀리면 `[TITLE-MENU]` 경고 후 C++ 기본 5버튼. 위젯 디자인은 유지하고 호버/클릭 효과음만 붙인다.
- `GetTitleButton`과 Title*Index는 순서대로 0~4. 설정 닫으면 설정(3), 로비 닫으면 들어갔던 메뉴, 맵 이동 후 새 타이틀은 마지막 분류 메뉴로 포커스. 위/아래 끝 순환, B/Esc 반복은 한 화면만 Back. 진입 뒤 분류를 바꾸던 기존 훈련→Racing 포커스 문제도 진입 전 분류 지정으로 수정. 로비 Tutorial/Racing 탭·LB/RB는 그대로 두며 유지 여부는 **현재 미정**.
- C++ 기본 메뉴 `TitleButtonHeight=80 / TitleButtonSpacing=26`은 5개 배치를 위한 임시값이며 UI 담당 조정 대상. 별도 `TitleMenuClass` 위젯 외형은 해당 Designer에서 조정한다. 기존 사람 디자인/배경/로고는 보존한다.
- 설정 “조종 > 조종 입력 표시”(`ControlInputDisplayCheck`)는 고도계와 독립한 수동 ON/OFF. 적용·취소·기본값 복원 구조 그대로, 기존 음량 SaveGame에 `bHasControlInputDisplayChoice / bControlInputDisplayEnabled` 저장. 사용자 선택이 우선하며 기본값 복원→적용은 선택을 지워 앞으로 정해질 기본값을 따른다. `DefaultGame.ini`의 `[/Script/Drone.DroneAudioSettingsSubsystem] bControlInputDisplayEnabledByDefault=False`는 결정 전 임시 끔, **최종 기본값 현재 미정**. 자동화는 `DroneAudioSettings_Automation` 슬롯으로 사용자 설정 보호.
- `WBP_DroneFlightHUD` Class Defaults `ControlInputDisplayClass = WBP_DroneControlInputDisplay`로 저장 연결 완료. 화면 아래 가운데 `ControlInputDisplayOffset=(0,-24)`, 월드 타이머 `ControlInputDisplayUpdateInterval=1/30초`, 설정 ON·기체 있음일 때만 `SetControlInputDisplayVisible`·`UpdateStickAxes` 이름 호출(축은 값이 바뀔 때만). OFF는 숨김·갱신 중지, 다른 HUD는 유지.
- `ADroneFlightPawn::GetControlInputSnapshot()` BlueprintPure의 X 오른쪽+, Y 위+, [-1,1]은 스틱 물리 위치. 쉬운/실제 조작형: 왼쪽 이동·오른쪽 X 회전/Y 카메라·트리거 고도. Acro Mode 2: 왼쪽 Yaw/스로틀·오른쪽 Roll/Pitch, Mode 1: 왼쪽 Yaw/Pitch·오른쪽 Roll/스로틀. 지상: 왼쪽 조향/전후. 키보드도 같은 액션 위치로 표시되며 입력 매핑 추가 없음. UI 커서는 중심±38px·화면 Y 반전. 장치 자동 구분/전환·혼합 입력·분리/재연결 정책은 현재 미정이다.
- 저장 BP 연결을 검사하며 테스트 메모리 Class Defaults 덮어쓰기는 인스턴스 연결 근거로 쓰지 않는다. 제품 연결은 구현됨·자동 검증됨·실제 패드/1280·1920 수동 대기다.
- Racing에서는 RouteSelector의 `bBlockRouteKeysInRacingMissions=true`로1~5 임의 코스 전환/키 안내를 막는다. 시험맵 직접 실행·Tutorial/Training/Story의 허용 옵션과 랜덤 기능은 보존한다. 기본 레이싱은 팀원1·2·3이며 옛 Circuit Test와 개인 랜덤도시는 별도다.
- 팀원 레이싱3맵 진입/완주·전용 슬롯 기록 복원은 자동 검증됐고 실제 조종/패드는 대기다. Map2 동일 위치 연속 링은 실행 중만 제외하며 원본 맵은 보존한다. 현재 검사 근거는 STATUS·WORKLOG를 따른다.

## 1. 이전 4메뉴 구현 기록 (2026-10-01)

당시 세션 원문은 [WORKLOG](../history/DRONE_WORKLOG.md)에 보존했다. 현재 구현·검증은 [STATUS](../../STATUS.md)를 따른다.

## 2. 어디를 열고 테스트하나

1. 새 C++ 코드가 포함되므로 Editor를 닫고 `DroneEditor Win64 Development`를 빌드한다. Live Coding만으로 새 UPROPERTY/enum 변경을 확인하지 않는다.
2. `/Game/Drone/Maps/Lvl_DroneFrontEnd`를 열어 Play한다. 프로젝트 `GameDefaultMap`도 이 맵이다. Editor 첫 맵은 기존 Production Training 설정을 유지한다.
3. 스토리·레이싱·튜토리얼·설정·종료5개를 확인한다. 스토리는 M1 맨 위4개, 기본 레이싱은 팀원1·2·3, 튜토리얼은 LOS 첫 수업부터 표시돼야 한다. B/Esc 복귀·설정 닫은 뒤 설정(3) 포커스·위/아래 끝 순환과 키 반복 한 화면 Back을 확인한다.
4. Story는 아래 Select_UI 절의 왼쪽 목록·가운데 이미지·오른쪽 설명·하단 START 배치를 확인한다. 훈련 탭은 숨기고 브리핑 복귀 시 분류/선택을 복원해야 한다. 튜토리얼/레이싱의 기존3열·스크롤·탭/LB/RB는 보존한다(최종 탭 유지 여부 미정).
5. 카드는 선택만 하고 하단 START로 확정한다. 기존 브리핑→작전 지역 이동→기체 카드→조작 설정→출격을 진행한다. 기체 선택의 뒤로/Esc/패드B는 해당 브리핑으로 돌아간다.
6. 원형 코스는 `/Game/Drone/Maps/Tutorial/TUT_Circle_Gate`, 레이싱1=Island Example·2=Lvl_DroneTraining·3=MountainRange Example로 진입한다. 보존된 옛 Heading/Circuit Test와 혼동하지 않는다.


7. 설정 > 조종 > 조종 입력 표시 ON→적용→출격하여 아래 가운데 스틱 커서를 확인한다. 위쪽 입력은 화면 위로, 해제하면 중심, Mode 1/2 축 위치가 맞아야 한다. OFF→적용은 입력 표시만 숨기고 고도계·비행 HUD는 유지한다. 적용 전 취소·기본값 복원→취소/적용·저장 후 재실행도 확인한다. 임시 기본 OFF를 최종 사양으로 판정하지 않는다.
8. 1280×720·1920×1080에서 메뉴/입력 표시 위치·가림을 실제 패드로 확인한다. 분리/재연결·혼합 입력은 미정 정책을 Pass 기준으로 만들지 않는다. 로비 Racing의1~5 안내/전환 없음·시험 Route 맵의 기존 전환/랜덤 유지와 팀원3맵 실제 완주/기록을 확인한다. 자동 이동 완주를 손 조종 Pass로 쓰지 않는다.

통합 로비/맵 이동은 FrontEnd에서 확인한다. 독립 Tutorial 8맵·Story 4맵·Racing 1맵은 Boot 상태에만 적용되는 기본 Mission Entry가 있어 직접 Play도 가능하다. 선택 Mission이 없는 보존된 공유 시험장은 별도 기능 종합 시험장이다.

## 3. Blueprint에서 이미지 교체

저장된 화면은 위 편집 정본의 Image Brush/버튼 Style에서 교체한다. 아래 `WBP_DroneFrontEndRoot`의 **Class Defaults → Drone → Front End → Artwork** 슬롯은 Native 폴백/최초 내보내기용이다. C++를 수정하거나 PNG 파일 절대 경로를 입력할 필요가 없다.

| 슬롯 | 제공 자산 | 역할 |
|---|---|---|
| Title Background Texture | `T_Title_Background` | 배경 `Background_1.png` |
| Title Overlay Texture | `T_Title_Overlay` | 좌측 어두운 패널 `Background_2.png` |
| Title Logo Texture | `T_Title_Logo` | `Main_LOGO.png` |
| Button Normal Texture | `T_Title_ButtonNormal` | `Unselect.png` |
| Button Hovered Texture | `T_Title_ButtonHovered` | `Select.png` |
| Button Pressed Texture | `T_Title_ButtonPressed` | `Click.png` |

Texture 위치는 `/Game/Drone/FrontEnd/Textures/Title`이다. 원본 PNG는 수정하지 않았고 투명도를 유지했다. 제공 버튼은 734×429 투명 캔버스에 실제 그림이 작게 들어 있으므로 `Use Provided Button Atlas Regions`를 켜 UV로 여백만 제외한다. 나중에 버튼 크기에 딱 맞는 PNG로 교체하면 이 옵션을 끈다.

- 현재 제품 화면은 저장된 WBP 트리를 사용한다. 기본 생성 코드와 런타임 좌표 예외에 의존하던 로비를 별도 Designer로 옮겼다.
- 저장 화면의 정적 그림은 해당 Image Brush를 바꾼다. `Refresh Artwork`의 정적 그림 재할당은 Native 폴백에만 적용한다.
- 미션별 선택 사진은 해당 `DA_Mission_*`의 `Thumbnail`, 출격 전 조작 안내 왼쪽 사진은 `BriefingImage`에 넣는다. 후자가 비면 Thumbnail을 재사용한다. 두 사진이 모두 없으면 타이틀 배경을 사용한다. 레이싱·훈련 사진 모두 Scale To Fill로 표시한다. 기체 Definition의 `PreviewMesh / PreviewActorClass`는 유지한다.
- 직접 Designer를 만들면 `TitleBackgroundImage / TitleOverlayImage / TitleLogoImage / MissionThumbnailImage`라는 `Image` 이름을 쓰면 C++ 연결을 재사용한다. 추가 배경 이름은 `LobbyBackgroundImage / BriefingBackgroundImage / SettingsBackgroundImage`, 브리핑 이미지 이름은 `BriefingThumbnailImage`다. 기존 필수 패널·버튼·텍스트 이름도 유지한다.
- 훈련 하위 탭 컨테이너 이름은 `TrainingCategoryTabs`, 버튼 이름은 `TutorialTabButton / RacingTabButton`이다. `MissionTabButton` 이름/API는 기존 WBP 호환용으로 남고 런타임에는 숨긴다. 동적 목록은 `MissionButtonsColumn`이라는 VerticalBox에 자동 구성할 수 있다. 자체 카드 UI라면 `Get Visible Mission Ids`로 목록을 만들고 `Select Lobby Mission`을 호출한다. 우측 목표 텍스트는 `MissionObjectiveSummaryText`다.
- `Receive Lobby Category Changed`, `Receive Lobby Mission Selection Changed` 이벤트에서 자체 탭/카드 애니메이션을 붙일 수 있다. 이 이벤트 안에서 Flow를 중복 전환하지 않는다.

### 훈련 사진·조작 장치 그림·시작 위치

- 훈련 DA 8개: `/Game/Drone/Data/Missions/DA_Mission_Tutorial_*`. 원본의 `훈련선택창규격이미지` 8장을 Thumbnail, `훈련진입전조작가이규격이미지` 8장을 BriefingImage로 연결했다. Texture는 `/Game/Drone/UI/Textures/Training/T_Training{Select,Briefing}_<수업>_20261019`이며 원본 PNG는 수정하지 않는다. `Hover`=LOS, `Heading`=원형 코스, `Payload`=배달(원본 Delivary 철자 유지)이다.
- `/Game/Drone/UI/WBP/FrontEnd/WBP_DroneControlsGuide`의 `bUseDeviceArtwork=true`는 세 장치 PNG 위에 **번호만** 표시한다. 키 이름과 동작은 아래 한글 범례에 둔다. `GamepadDeviceImage / KeyboardDeviceImage`는 기존 `T_Controls_{Gamepad,KeyboardMouse}_Device_20261020`, 범례는 `GamepadGuide / KeyboardGuide / RCControllerGuide`, 그림 높이는 `DiagramHeight`(기본300, 적용220~300)에서 조정한다. 저장된 WBP에서는 `FitDiagramArea`가 파츠를 다시 만들지 않으며, 세 장치의 그림/번호/범례를 Designer에서 직접 조정한다. `GetImportedSize()`로 그림 비율을 보존한다.
- `RCDeviceImage`는 `/Game/Drone/UI/Textures/Controls/T_Controls_RC_StickSwitch_20261020`에 연결한다. 검정/은색 네모형 본체와 버튼 배치를 유지하고 양쪽 어깨를 실제 세로 토글 스틱 형태로 바꿨다. 번호7개만 UMG로 표시하며 LT/RT 외부 칩·지시선은 제거했다. 오른쪽 아래 `SELECT 휠`은 **회전: 위/아래 · 누름: 확인**, 왼쪽 아래 하단 `CANCEL`은 뒤로다. GenericUSB17/18→위/아래·16→확인·15→취소 등 실제 매핑은 유지한다. 옛 PNG/폴백도 보존하며 원본/프롬프트/SHA는 Unreal `SourceArt/Controls/controls_devices_20261020.json`의 `current_rc_revision`을 따른다.
- 패드 안내는 MCP로 실제 `IMC_DronePrototype.defaultKeyMappings.mappings`·`IMC_DroneGroundWeapons` 및 Scout/UGV BP 연결을 읽어 확인했다. 비행은 **쉬운 조작 기준**으로 표기하며 FPV는 별도, 첫 LOS의 시점 전환은 고정 예외다. R1/L1 설명은 비행 역할에 한정하고 UGV 무장은 L2/R2로 안내한다(기존 R1/L1 대체 바인딩은 삭제하지 않음). ○는 메뉴 뒤로, □는 UGV 재장전만 표시한다. 기능 없는 버튼은 설명에서 제외했다. RC 그림은 사용자가 준 기존 시뮬레이터 조종기 형태·버튼 위치를 유지했다. 실제 입력 바인딩 자체는 변경하지 않았다.
- 첫 LOS 수업만 `ADroneTutorialObserverLesson`이 `BP_LOS` 눈높이를 읽어 **뒤400cm·옆120cm·위80cm** 보정하고 훈련 구간을 바라본다. Observer BP의 `bUsePlacedSceneAnchors`, `ObserverEyeForwardOffsetCentimeters`(기존18), `ObserverCameraBackOffsetCentimeters / ObserverCameraSideOffsetCentimeters / ObserverCameraHeightOffsetCentimeters`에서 조정한다. BP_LOS/맵은 저장하지 않는다. LOS 드론은 외부에서 보이게 하고 다른 비행 수업은 1인칭으로 시작한다. 출격 시 SpringArm 초기 지연을 한 번 정리하며 1인칭에서는 자기 본체/로터를 소유자에게만 숨긴다. 저장 카메라 선호값·충돌은 유지한다.
- 비행 출발은 가장 가까운 `SM_helicopter_base` 상단이다. 호버 구역은 **출격 Yaw 정면6m·패드 위 중심3m**, 청록12변 테두리에서3초 유지하면 바로 클리어한다. `BP_TutorialHoverZone`의 ShowHoverGuide/GuideThicknessCentimeters/GuideMaterial과 `M_HoverGuide_Visible` Brightness(3)로 조정한다. **LOS를 제외한 Tutorial·Story의 추가 ReturnToBase 목표/귀환 표적·낡은 로비/브리핑 문구를 제거**했다. LOS 자체의 후진→실제 착지는 수업 목표이므로 유지하며 LOS DA 원본도 보존했다. 전진/원형/물자도 본목표 성공 즉시 결과로 간다. 저장 도구의 재도입 방지·검사 방법은 [귀환 정책](DRONE_TEST_MAP_GUIDE.md#귀환-정책을-유지하는-방법)을 따른다.
- 시작 안내의 배경은 `UDroneMissionStartPromptWidget::bUseStableMissionBackdrop=true`로 `BriefingImage`(없으면 Thumbnail)를 쓴다. 기존 WBP 안내/버튼을 보존한 채 초기 카메라/조명 준비 프레임을 불투명 배경으로 가린다. [시작] 전 시간/입력 정지·확인 후 재개를 검사한다. Lumen 노출 경고 자체를 없애거나 전체 렌더 품질을 낮춘 수정은 아니다.
- 물자/포탑 수업은 준비 중 표시를 해제했다. 배달 출격은 `TUT_Delivary_2`로 연결하며 빈 집게로 시작→실제 화물 접근/집기→표적 위 투하다. `TUT_UGV_Turret`는 체력200 포탑 파괴로 완료한다. 기존 `TUT_Delivary`는 보존한다. 배치된 시작/표적은 레벨에서 조정하며 [목표 매니저 편집](DRONE_MISSION_FRAMEWORK_GUIDE.md#이미-배치된-맵에서-바로-찾기)을 따른다. 제품 Story 연결/제한은 [시험 가이드](DRONE_TEST_MAP_GUIDE.md#현재-미션-연결과-확인-순서)에 있다.
- 확인 순서: Editor 종료 후 Build → FrontEnd Play → Tutorial에서 각 사진 선택 → START → 세 장치 탭/하단 범례 확인 → LOS 사람 시점·다음 수업 드론 시점/패드 상단 확인. `Drone.UI.TrainingPresentationCapture`는 1280/1920 실제 화면과 범례 경계, `Drone.Tutorial.TUTMapLaunchPIE`는 실제 TUT 맵 시작을 검사한다. 실제 패드 비행·연속 완주는 별도다.
- 정찰·FPV 기체 선택 사진은 실제 `DA_Drone_Scout_Greybox` / `DA_Drone_FPVStrike_Greybox`의 PawnClass를 바닥 없는 별도 PreviewScene에 불러와 푸른 배경으로 촬영했다. `SelectImage`는 `/Game/Drone/FrontEnd/UI/SelectUI/Drones/T_SelectDrone_{Scout,FPV}_Studio_20261020`에 연결한다. 재사용 PNG/메시 출처는 `SourceArt/Selection`, 촬영은 `Drone.Diagnostics.SelectionPhotos`, 가져오기는 `Tools/AssetMigration/ApplyPresentationRefresh.py`다. 기존 사진과 제품 맵은 보존한다. 튜토리얼 권장창은 제목·본문·두 버튼을 한글로 표시하며 저장된 Designer WBP/Native 경로에 함께 적용한다. 검증 근거는 [WORKLOG](../history/DRONE_WORKLOG.md)를 따른다.
- 레이싱 사진 재촬영: `Drone.UI.RacingEditorOverview.Map1/2/3`은 각 실제 Editor 맵의 활성 코스40% 주변을 **약680m·FOV60 근접 전경**으로 촬영한다. 전체 코스 bounds Fit은 더 사용하지 않는다. 수직 Landscape Trace로 지면 높이를 맞추고 원본 World 경로·맵 해시를 확인한다. 촬영 중 Fog와 시작/목표 디버그 표시를 Editor/Game 양쪽에서만 숨기고 모두 원복하며 Atmosphere/Cloud는 표시한다. 맵은 저장하지 않는다. 결과는 `Saved/Automation/CodexRacingNear_20261020/RacingMapN_near.png`, 재사용 PNG는 `SourceArt/Racing/RacingMapN_NearView_20261020.png`다. 사진 확인 뒤 `Tools/Validation/Invoke-ControlDeviceArtworkImport.ps1 -RacingPreviews -RacingNear`가 기존 DA를 백업하고 새 `T_RacingMapN_NearView_20261020`을 Thumbnail/BriefingImage에만 연결한다. MissionMap/RecordCourseId·랜덤도시 '?'는 유지한다. 옛 Close/CoursePreview 사진과 Texture도 삭제하지 않는다.

### 시작 오프닝 영상

- 프로젝트 `Content/Movies/Main_cinematic.mp4`는 사용자 제공 원본과 SHA-256이 동일한 복사본이다. H.264/AAC·1920×1080·30fps·약79초·148,658,835B. 외부 E드라이브 경로를 런타임에서 참조하지 않는다.
- `ADroneFrontEndPlayerController`가 새 GameInstance의 Boot에서 `UDroneOpeningMovieWidget`을 타이틀 위에 한 번 표시한다. 정상 종료·Esc·패드 ○는 영상/소리를 정리하고 타이틀 포커스를 복원한다. 로비/미션에서 타이틀로 돌아올 때는 다시 재생하지 않는다. 파일 없음·디코더 실패·열기 시간 초과도 타이틀로 넘어간다.
- FrontEnd PlayerController Class Defaults의 `bPlayOpeningMovie`로 켜고 끈다. `OpeningMovieWidgetClass`에 해당 C++ 클래스의 BP 자식을 지정하면 `MovieFilename`(Content/Movies 안 파일명), `OpenTimeoutSeconds`(기본10초)를 조정할 수 있다. 영상은 16:9 비율 유지, 남는 화면은 검정 여백이다.
- `Drone.Build.cs`에 MediaAssets/AudioMixer, `.gitattributes`에 MP4 LFS, `DefaultGame.ini`에 `bSkipMovies=False`·`NonUFSMovies=Main_cinematic`을 설정했다. StartupMovies에는 등록하지 않아 중복 재생을 피한다. 다른 PC는 사용자 Commit/Push 후 LFS 영상까지 받아야 한다. 실제 패키징/배포판은 미검증이다.
- `Drone.UI.OpeningMoviePIE`는 실제 파일 디코딩·재생 시간 진행·1920×1080 트랙·Unreal 내부 Esc 입력→타이틀 버튼 포커스 복귀를 검사한다. 숨김 렌더 캡처로 실제 영상도 확인했다. 무음 실행이므로 청감·자연 종료까지의 전체 재생·실제 패드는 별도다. 사용자 시험은 새 Play → 영상/소리·비율 → Esc/○ → 타이틀 입력, 다음 새 Play의 자연 종료·로비 복귀 시 재재생 없음이다. 자동 마우스/키보드나 보이는 Editor 조작은 사용하지 않는다.

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

외부 WBP의 미션 선택은 `SelectLobbyMission(MissionId)`를 사용한다. 이 API가 Flow 선택·사진 미리보기·예약된 패드 포커스를 함께 맞추므로, 브리핑 전에 이전 카드로 되돌아가지 않는다. 미리보기와 선택을 따로 손대지 않는다. 레이싱 DA의 `SecondaryInfoText`도 해당 코스에 맞게 적고 숨김 Circuit_Test의 옛 ‘7개 체크포인트’ 문구를 복사하지 않는다.

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
- 순서: 시작 Gate 0 → 체크포인트 1~7 → 결승 Gate 8 → 즉시 클리어(별도 귀환 없음).
- 결승은 Spline 전체 길이 L에 두어 **7/8 바퀴를 돌고 완료하는 오류를 막는다**. 시작 Gate와 겹치지 않도록 결승만 진행 방향으로 2.5m 떨어뜨렸다.
- Rule Event: `TrainingLap`, TargetId: `Tutorial.Orbit.Course`. 기존 게이트 수업은 `Tutorial.GateFlight.Course`다.
- Director가 Tag에 맞는 코스 Recorder만 구독하고 다른 코스 선/Trigger를 끈다. HUD도 동일한 Recorder를 사용한다.
- 원순서 건너뛰기, 역방향 통과, 제자리 Yaw, 다른 코스 완주는 이 목표를 완료시키지 않는다.
- Course Spline, Automatic Gate Count/배치, Gate Scale/크기와 Rule Time Limit은 BP/맵 Details에서 조절한다. 변경 후 순서·결승 위치를 다시 테스트한다.

구현 책임: Course가 경로/Gate 생성, Gate Sequence가 순서/정방향, Lap Recorder가 시간·거리·평균 속도, Mission Director가 Lap→결과 전환을 맡는다. 옛 Return Zone은 이 수업 완료 조건이 아니다.

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
