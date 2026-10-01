# 시작 화면 · 로비 탭 · 원형 코스 가이드

기준일: 2026-10-01. 기존 시작 화면·원형 코스·로비 기반은 Unreal 원격 `main`의 `83b33c1`로 현재 D 드라이브 작업컴에 수신됐다. 같은 날 첨부 UI 기획안에 맞춘 훈련/Story 진입 분리·화면 재배치·사운드/화면/성능 설정은 현재 작업 트리의 추가 변경이며 아직 Commit/Push하지 않았다. Figma 원본과 기존 이미지 자산은 수정하지 않았다.

## 1. 이번 변경

- 사용자가 제공한 `Title_Asset`의 배경, 어두운 오버레이, 로고, 일반/호버/클릭 버튼 PNG 6개를 Unreal Texture로 가져왔다. 참고이미지는 완성 화면 비교용이며 그대로 한 장짜리 버튼 화면으로 쓰지 않는다.
- 시작 화면의 제공 배경·어두운 오버레이·로고·버튼 6개 이미지는 유지한다. `Start / Training / Setting / Exit` 중 Start는 Story 4개 목록, Training은 `튜토리얼 / 레이싱` 하위 선택으로 연결한다. 훈련 목록은 튜토리얼 9개(기존 종합 Training 포함)와 레이싱 1개다. Story 목록에는 훈련 탭을 표시하지 않는다.
- 로비를 첨부 기획안의 좌측 스크롤 목록 / 중앙 작전 이미지·이름·지역·난이도 / 우측 개요·목표의 3열로 정리하고 하단 중앙 시작 버튼을 배치했다. 선택 강조와 현재 분류 필터를 유지하며, 다른 분류에 남은 선택을 바로 실행하지 않는다.
- 브리핑은 좌측 이미지와 우측 스크롤 설명·목표 순서, 하단 작전 지역 이동 버튼이다. 로비/브리핑/설정에도 기존 배경을 사용하고, 선택 Mission에 별도 Thumbnail이 없으면 기존 배경으로 보완한다.
- 기체 선택은 상단 큰 역할 프리뷰와 상세·조작 설정, 프리뷰 아래 출격 버튼, 하단 가로 기체 카드로 재배치했다. 기체 5종 Catalog와 Mission 허용 목록은 유지한다. 프리뷰는 공중 기체/UGV를 구분하는 역할 도식이며 실제 Mesh 렌더 프리뷰는 아니다.
- 로비·브리핑·기체 선택은 1920×1080 설계를 비율 유지해 축소하고 긴 설명은 스크롤한다. 1280×720·1920×1080 실제 화면 가독성은 수동 확인 대기다.
- Setting의 임시 품질 3버튼을 전체 음량·창 모드·해상도·품질·수직 동기화·프레임 제한과 적용/기본값/뒤로가기 화면으로 교체했다. 저장과 미적용 취소 기준은 아래 9절을 따른다.
- 회전 수업을 **방향 맞추기가 아닌 원형 코스를 한 바퀴 도는 비행**으로 수정했다.
- 독립 레이싱 시험맵을 추가했다. Best Lap JSON 영구 저장은 2026-10-02 구현·자동 검증 완료·실기 재실행 확인 대기다. 정식 경기 규칙·순위는 미완료다.

## 2. 어디를 열고 테스트하나

1. 새 C++ 코드가 포함되므로 Editor를 닫고 `DroneEditor Win64 Development`를 빌드한다. Live Coding만으로 새 UPROPERTY/enum 변경을 확인하지 않는다.
2. `/Game/Drone/Maps/Lvl_DroneFrontEnd`를 열어 Play한다. 프로젝트 `GameDefaultMap`도 이 맵이다. Editor 첫 맵은 기존 Production Training 설정을 유지한다.
3. 시작 화면의 기존 배경·로고·버튼 호버/클릭을 확인한다. `시작`은 Story 4개, 시작 화면으로 돌아온 뒤 `훈련`은 튜토리얼 9개와 레이싱 1개 하위 탭을 보여야 한다.
4. 훈련의 튜토리얼/레이싱 탭, 3열 선택 화면과 스크롤을 확인한다. Story에서는 훈련 탭이 숨겨져야 하고 브리핑에서 돌아오면 분류와 선택이 복원되어야 한다.
5. 목록 선택 → 하단 미션 시작 → 브리핑 → 작전 지역 이동 → 하단 기체 카드 선택 → 조작 설정 → 출격을 진행한다. 기체 선택의 버튼/Esc/패드 B는 해당 미션의 브리핑으로 돌아간다.
6. 튜토리얼 `1-3 원형 코스 비행`은 `/Game/Drone/Maps/TestMap/Tutorial/Lvl_Tutorial_Heading_Test`, 레이싱은 `/Game/Drone/Maps/TestMap/Lvl_DroneRacingTest`로 이동한다.

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

### 직접 WBP를 만들 때 유지할 API와 이름

- 시작 화면의 Start는 `Finish Opening Trailer`, Training은 `Open Training Lobby`를 호출한다. `Set Lobby Category / Get Lobby Category / Is Training Lobby`는 현재 목록 분류를 다룬다. 선택/확정은 `Select Lobby Mission / Confirm Selected Mission`, 브리핑 이동은 `Finish Mission Briefing`, 뒤로가기는 `Navigate Back`을 사용한다.
- FrontEnd 필수 이름은 `OpeningPanel / LobbyPanel / MissionBriefingPanel`, `ContinueButton`, `OpeningTitleText / LobbyTitleText / LobbyStatusText`, `MissionSelectButton / MissionSelectButtonText`, `MissionNameText / MissionDescriptionText / MissionMetaText`, `StartMissionButton`, `MissionBriefingTitleText / MissionBriefingBodyText`, `FinishMissionBriefingButton`이다. Back 버튼은 `LobbyBackButton / BriefingBackButton`으로 연결한다.
- 기체 선택의 필수 이름은 `DroneSelectionPanel`, `MissionNameText`, `DroneNameText / DroneDescriptionText / DroneProfileText`, `DroneButton0`~`DroneButton4`, 각 `DroneButton0Text`~`DroneButton4Text`, `ControlModeButton / ControlModeButtonText`, `LaunchDroneButton`이다. `SelectionBackButton`을 쓰면 기본 Back 처리를 재사용한다. 폐기된 속도 단계의 `HandlingPresetButton / HandlingPresetButtonText`는 호환용으로 숨긴다.
- 기체 카드 입력은 `Select Drone`, 조작 전환은 `Toggle Control Mode`, 출격은 `Confirm And Launch Selected Drone`이다. `Receive Drone Selection Refreshed`에서 최종 카드/모델 연출을 붙일 수 있으며 실제 승인과 Pawn Spawn은 기존 Flow/Controller가 담당한다.
- 설정 Host에는 `SettingsPanel`과 `UDroneSettingsWidget` 타입의 `SettingsWidget`을 넣고 `Set Settings Visible`로 열고 닫는다. 설정 위젯 자체의 Designer 노드는 이름만으로 자동 Bind되지 않는다. 기본 native 위젯을 재사용하거나 아래 9절의 공개 API에 직접 연결한다.

## 4. 탭과 미션 데이터

담당 클래스는 `UDroneMissionDefinition`과 `UDroneFrontEndRootWidget`이다.

- DA의 `Lobby Category`: Tutorial / Racing / Mission. `Auto`는 기존 저장 DA 호환용이며 ID 접두어로 분류한다.
- Auto 규칙: `Mission.Tutorial.*` → 튜토리얼, `Mission.Racing.*` → 레이싱, 그 외 → 미션.
- 미션 목록은 Flow Catalog 등록 항목에서만 읽는다. 새 DA를 만들기만 해서는 자동 등록되지 않는다. 현재 명시적 등록 경계는 `DroneGameFlowSubsystem.cpp`의 `DefaultMissionPaths`다.
- 분류와 맵은 독립적이다. `Lobby Category`를 바꾸면 표시 탭만 바뀌고 실제 이동 맵은 `Mission Map`이 결정한다.
- 기존 8개 수업과 Story 4개는 보존했고, 새 `DA_Mission_Racing_Circuit_Test`만 Catalog에 추가했다.
- 이번 UI 변경은 분류 데이터를 재작성하지 않고 진입 경로만 나눈다. Start→Mission(Story 4), Training→Tutorial(9)→Racing(1)이며 훈련/Story 사이 이동은 시작 화면의 메뉴로 선택한다. 브리핑·기체 선택에서 복귀하면 선택된 Mission의 분류를 복원하고, 시작 화면에서 새로 진입할 때는 선택을 초기화한다.

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

## 8. 도구와 확인할 것

`Tools/AssetMigration/Invoke-DroneTitleLobby.ps1`은 Editor 종료 후 실행한다. 이미 이식된 Texture가 있으면 원본 Downloads 폴더가 없는 작업컴에서도 실행할 수 있다. 원본 재수입이 필요하면 `-TitleAssetDir '실제 Title_Asset 경로'`를 지정한다.

도구는 WBP 이미지 기본값, 전용 Tutorial 원형 Station, 관련 DA 두 개, 독립 Racing 맵/DA만 갱신한다. 기존 레이싱 맵 전체 재생성이나 Production 저장은 하지 않는다. 최종 UI 수동 변경 뒤 이 도구를 무작정 재실행하면 이미지 기본값이 제공 이미지로 돌아가므로 주의한다.

자동화 보고서는 프로젝트 `Saved/Automation/TitleLobbyOrbit` 아래에 저장한다. 실제 수동 확인은 다음을 남긴다.

2026-10-01 다른 PC `C:\URproject\drone`의 기록: 앞선 Editor Build·14/14 → GameReadiness **32/32·테스트 오류/경고 0**, 시험맵 14개 Map Check 0/0 → Back 후속 33개 실패 0(HTTP 경고 동반 성공 1건). 1280 Setting/Training/탭·목록 일부와 Back/선택 복원, 1920 제목/Exit를 당시 확인했다. 이번 UI 변경 이전의 D 드라이브 최신화에서는 재실행하지 않았고 해당 다른 PC의 Oct 1 원시 `Saved` 보고서도 수신하지 않았다. 이 기록을 이번 UI의 수동 Pass로 해석하지 않는다. [검증 출처와 범위](DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md)

이번 추가 UI/설정 코드는 현재 D 드라이브에서 MSVC `14.51.36257` Editor Build 및 `FrontEndContract / BackNavigationContract / MissionEntryContract / SettingsContract / FrontEndPIE` **5/5 Success**, 자동화 이벤트 오류/경고 0이다. 최종 보고서는 `Saved/Automation/TrainingLobbySettings/index.json`(2026-10-01 02:03:48 UTC). 분류/숨은 선택/복귀, 음량 Clamp·NaN·SaveGame 메모리 직렬화와 실제 Settings 자식 컨트롤·슬라이더/Back Delegate·미적용 취소를 검사했다. NullRHI/NoSound이므로 새 화면·실제 가청성·Standalone 창 변경·디스크 저장 후 재실행·전체 미션 손 조작 완주·패드 실기·최종 음원/연출은 수동 확인 대기다.

1. 1920×1080와 1280×720에서 로고·버튼·3열 로비·브리핑·가로 기체 카드·출격이 잘리는지. 긴 설명/목표/기체 정보는 스크롤해 끝까지 읽을 수 있는지.
2. 제공 버튼 PNG의 투명 여백, 텍스트 위치, 클릭 범위가 자연스러운지.
3. 원형 7/8 바퀴에서 미완료, 마지막 결승 통과 후 귀환으로 전환되는지.
4. 레이싱의 9개 Gate 정방향 완주 → 성공 결과가 나오는지.
5. 타이머 만료/충돌 실패 → 재시도 때 Gate 진행이 초기화되는지.
6. Start→Story 4와 Training→Tutorial 9/Racing 1 분리, 탭 선택·목록 선택 강조, 브리핑/기체 선택의 Back/Esc/패드 B, 선택/분류 복원과 반복 키 차단이 맞는지.
7. Setting의 음량 미리보기→취소 복원, 적용→재실행 복원, 품질/VSync/FPS 적용, 기본값의 미적용 취소를 확인한다. 창 모드/해상도는 PIE에서 비활성이고 Standalone에서 변경/재실행 확인한다.

자동화 성공만으로 최종 시각/조작 체감 검증까지 끝났다고 처리하지 않는다.

## 9. 사운드 · 화면 · 성능 설정

설정은 시작 화면의 Setting으로 연다. `UDroneSettingsWidget`이 현재값을 읽어 편집을 시작하며 Root의 Back/Esc/패드 B도 같은 취소 경계를 사용한다.

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

2026-10-02 C PC Claude NullRHI BatteryHUDPIE + HUD 2개 + CheckpointRestart **4/4 Success**, 근거 `C:\URproject\drone\Saved\Automation\ClaudeHUD\test.log`. 패널 위치·가독성 수동 확인 대기다. 브리핑 대사 DA 입력법은 [Mission 가이드](DRONE_MISSION_FRAMEWORK_GUIDE.md)를 따른다.
