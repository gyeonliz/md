# 시작 화면 · 로비 탭 · 원형 코스 가이드

기준일: 2026-10-01. 이번 구현은 로컬 변경이며 Commit/Push하지 않는다. Figma는 수정하지 않았다.

## 1. 이번 변경

- 사용자가 제공한 `Title_Asset`의 배경, 어두운 오버레이, 로고, 일반/호버/클릭 버튼 PNG 6개를 Unreal Texture로 가져왔다. 참고이미지는 완성 화면 비교용이며 그대로 한 장짜리 버튼 화면으로 쓰지 않는다.
- 시작 화면은 제공 시안의 좌측 로고·메뉴와 배경을 조합한다. `Start / Training / Setting / Exit`를 연결했고 Setting은 그래픽 품질·돌아가기다. 레이싱은 로비 탭에서 선택한다. 후속 화면 점검에서 오버레이/로고 크기와 버튼 위치·폰트도 시안에 맞췄다.
- 로비는 `튜토리얼 / 레이싱 / 미션` 탭으로 나누고 실제 목록을 필터링한다. 현재 각각 9 / 1 / 4개다. 튜토리얼의 기존 종합 Training 항목도 보존했다.
- 선택 상세, 썸네일, 스크롤 목록, 선택 강조를 제공한다. 다른 탭으로 옮긴 뒤 이전 탭의 미션이 몰래 시작되지 않는다.
- 회전 수업을 **방향 맞추기가 아닌 원형 코스를 한 바퀴 도는 비행**으로 수정했다.
- 독립 레이싱 시험맵을 추가했다. 정식 경기 규칙, 순위, Best Lap 영구 저장까지 완료한 것은 아니다.

## 2. 어디를 열고 테스트하나

1. 새 C++ 코드가 포함되므로 Editor를 닫고 `DroneEditor Win64 Development`를 빌드한다. Live Coding만으로 새 UPROPERTY/enum 변경을 확인하지 않는다.
2. `/Game/Drone/Maps/Lvl_DroneFrontEnd`를 열어 Play한다. 프로젝트 `GameDefaultMap`도 이 맵이다. Editor 첫 맵은 기존 Production Training 설정을 유지한다.
3. 시작 화면의 배경·로고·버튼 호버/클릭을 확인하고 `시작`을 누른다.
4. 탭을 전환해 튜토리얼 9, 레이싱 1, 미션 4개가 나오는지 본다. 작은 화면에서는 목록을 스크롤한다.
5. 미션을 선택하고 시작 → 브리핑 → 작전 지역 이동 → 기체 선택 → 출격을 진행한다.
6. 튜토리얼 `1-3 원형 코스 비행`은 기존 공유 시험맵, 레이싱은 새 독립 맵으로 이동한다.

시험맵을 직접 Play하면 선택된 Mission이 없는 상태라 전체 목표/결과 흐름 시험이 되지 않는다. 반드시 FrontEnd에서 시작한다.

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
- 미션별 썸네일은 해당 `DA_Mission_*`의 `Thumbnail`에 넣는다. 레이싱은 임시로 제공 배경을 지정했고, 다른 수업/Story 썸네일은 미지정이면 숨긴다.
- 직접 Designer를 만들면 `TitleBackgroundImage / TitleOverlayImage / TitleLogoImage / MissionThumbnailImage`라는 `Image` 이름을 쓰면 C++ 연결을 재사용한다. 기존 필수 패널·버튼·텍스트 이름도 유지한다.
- 탭 버튼 이름은 `TutorialTabButton / RacingTabButton / MissionTabButton`. 동적 목록은 `MissionButtonsColumn`이라는 VerticalBox에 자동 구성할 수 있다. 자체 카드 UI라면 `Get Visible Mission Ids`로 목록을 만들고 `Select Lobby Mission`을 호출한다.
- `Receive Lobby Category Changed`, `Receive Lobby Mission Selection Changed` 이벤트에서 자체 탭/카드 애니메이션을 붙일 수 있다. 이 이벤트 안에서 Flow를 중복 전환하지 않는다.

## 4. 탭과 미션 데이터

담당 클래스는 `UDroneMissionDefinition`과 `UDroneFrontEndRootWidget`이다.

- DA의 `Lobby Category`: Tutorial / Racing / Mission. `Auto`는 기존 저장 DA 호환용이며 ID 접두어로 분류한다.
- Auto 규칙: `Mission.Tutorial.*` → 튜토리얼, `Mission.Racing.*` → 레이싱, 그 외 → 미션.
- 미션 목록은 Flow Catalog 등록 항목에서만 읽는다. 새 DA를 만들기만 해서는 자동 등록되지 않는다. 현재 명시적 등록 경계는 `DroneGameFlowSubsystem.cpp`의 `DefaultMissionPaths`다.
- 분류와 맵은 독립적이다. `Lobby Category`를 바꾸면 표시 탭만 바뀌고 실제 이동 맵은 `Mission Map`이 결정한다.
- 기존 8개 수업과 Story 4개는 보존했고, 새 `DA_Mission_Racing_Circuit_Test`만 Catalog에 추가했다.

## 5. 회전 = 원형 코스 비행

이전 `동쪽 90° 바라보기 → 1초 유지`는 이번 수업의 의미가 아니므로 연결을 해제했다. `ADroneTutorialHeadingZone` 클래스와 Event는 별도의 방향 정렬 시험 및 기존 자산 호환을 위해 삭제하지 않았다.

호환을 위해 자산 이름/ID는 `DA_Mission_Tutorial_Heading / Mission.Tutorial.Heading`을 유지하지만 표시명과 규칙은 원형 코스로 바뀌었다.

- Actor: 공유 시험맵의 `TutorialMissionTest_OrbitCourse` (`BP_DroneTrainingCourse`). 기존 손으로 편집한 Hover/다른 배치는 보존했다.
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

2026-10-01 앞선 결과: Editor Build·집중 회귀 14/14 성공. 후속 최종 점검은 **32/32 성공·테스트 오류/경고 0**, 시험맵 14개 Map Check 0/0이다. 1280×720에서 Setting/Training/탭·목록 반응, 1920×1080에서 제목 배치/Exit를 실제 화면에서 확인했다. 전체 미션 손 조작 완주·최종 음원/연출은 별도 확인한다. [최신 검증 범위](DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md)

1. 1920×1080와 1280×720에서 로고·버튼·탭·목록이 잘리는지.
2. 제공 버튼 PNG의 투명 여백, 텍스트 위치, 클릭 범위가 자연스러운지.
3. 원형 7/8 바퀴에서 미완료, 마지막 결승 통과 후 귀환으로 전환되는지.
4. 레이싱의 9개 Gate 정방향 완주 → 성공 결과가 나오는지.
5. 타이머 만료/충돌 실패 → 재시도 때 Gate 진행이 초기화되는지.

자동화 성공만으로 최종 시각/조작 체감 검증까지 끝났다고 처리하지 않는다.
