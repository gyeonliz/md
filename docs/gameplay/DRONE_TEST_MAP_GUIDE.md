# Drone 기능 시험 맵 가이드

2026-10-01 후속: 튜토리얼 8개를 `TestMap/Tutorial/Lvl_Tutorial_*_Test`로 분리하고 Story 4/Racing 1과 함께 직접 Play 기본 Mission Entry를 설치했다. OilRig 비 4모드 비교 맵과 Title 시안 보완도 추가했다. 최신 위치·테스트 절차는 [통합 점검 가이드](DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md)를 우선한다. 아래 9월 맵 설명은 당시의 기록이다.

기준일: 2026-09-29

## Shotgun 시선 안정화 확인 — 2026-10-04 C PC

1. TestMap/Lvl_DroneShotgunSystemsTest를 직접 Play하고 정면 표적 고정 시 Idle·사격 애니메이션 움직임과 좌우±1.9° 추적 시 추가 움직임을 구분한다.
2. AI-SHOTGUN-RENDER-01 해결(2026-10-04 C PC Claude). 표적 고정 시 머리4.2~4.4°(Idle·사격 애니메이션), 표적±1.9° 왕복 시 머리5.2~5.4°·SmoothedDroneLookRotation 1.45°. 9/18 몸 Hysteresis·Bone Gaze 보간(데드존 경계 0 Snap 없음)은 정상, 5~6° 대부분은 9월 하순 Rifle 계열 AnimBP 교체 뒤 애니메이션 흔들림이다. 절대 머리4° 판정(애니메이션 포함)과 미렌더 뼈 정지에 따른 NullRHI 거짓 통과가 원인. 표적 고정0.6초 기준 측정 후 시선 출력≤2.5°·애니메이션 대비 추가 머리 흔들림≤2.5°로 시험 정정(경계0↔±1.9° 튐3.8° 검출). NullRHI·렌더 Success(ClaudeInterview/shotgun3_*.log), known-test-failures에서 제외(Claude 지시서 근거).
3. 자동 시험 Drone.AI.ShotgunSystemsTestMapPIE 성공은 실제 장치 수동 Pass와 구분한다. NPCPerception 감지 실패는 별도이며 Production Training은 저장하지 않는다.

## 2026-10-04 Acro·첫 포커스 수동 확인 (C PC)

Unreal `41444c2` + 로컬 미커밋. Claude 조사/C++/Build/자동화·IMC 패치, Codex(ui) Scout/Drop BP 입력 연결→Claude 확인, Codex 문서 반영. 자동 검증12/12 Success(`ClaudeAcro/test_after_dz.log`), 화면 그려진 전체94개 중90 Success·기존4 Fail(`ClaudeAcroFull/test3.log`)이며 **수동 Pass 아님**. 아래 과거 맵 설명과 당시 검사는 보존한다.

1. `/Game/Drone/Maps/Lvl_DroneFrontEnd`에서 Acro 선택 가능한 비행 기체로 출격한다. Mode1/2를 각각 확인한다. 키보드 W/S Pitch·A/D Roll·Q/E Yaw·Space/Ctrl Throttle는 둘 다 같고, 패드 Mode2 LeftY=Throttle/RightY=Pitch·Mode1은 반대다. 회의 “좌우 스틱 반전”이 이 배치인지 다른 축 부호인지 기록한다(현재 미정).
2. 자세를 맞춘 뒤 W/S·A/D·Q/E를 놓고 **Space만** 누른다. 상승/추력 변화와 별개로 스로틀만으로 자세가 뒤집히지 않아야 한다. 자동화는 스로틀+1/0/-1·프레임 끊김에서 자세 불변 확인. W+Space 동시 입력과 Space 단독을 구분한다.
3. Mode1에서 스틱에 엄지를 걸친 채 Space→상승, 키 떼고 스틱→패드 조종, 모두 놓으면0인지 확인한다. Mode2도 같은 혼합입력을 비교한다. 키보드/패드 입력원 분리·절댓값 큰 쪽 사용은 자동 검증됐고 실제체감은 수동대기다.
4. FPV 키보드 W/S 또는 A/D를 짧게 톡(약0.1초) 누른다. 최대650°/s 기준 약65° 회전 후 Acro는 자동 수평 복귀가 없어 자세가 유지될 수 있다. 응답/체감과 W+Space 습관을 기록한다. 키보드 배율·Angle 모드·마우스 Yaw는 현재 미정이며 이 단계에서 임의 결정하지 않는다.
5. Scout·Drop 각각 Acro Mode1/2 비행 입력6개가 실제로 동작하는지 확인한다. 저장 BP 연결은 자동 계약으로 확인했지만 실제 비행은 수동 대기다. FPV/FiberOptic도 회귀 확인하며 지상 UGV는 Acro 대상에서 제외한다.
6. 결과·타이틀 화면을 반복 열어 첫 버튼 강조·방향/A/B·다른 버튼 이동 유지 여부를 본다. UI-FOCUS-RACE-01은 UIOnly 지연 루트 포커스 경쟁에5프레임 복원을 넣은 **수정 후 확인 중**. 화면 그려진 수정 전Fail/후Success 각1회뿐, 안정화 완료 아님. TutorialNextLessonPIE 실패 진단의 강조 위젯/Slate 위젯 이름을 비교한다.

기록: 날짜/PC·실제 패드·기체/BP·Mode·키/축·단독/동시 입력·기대/실제·첫 버튼 강조. 자동 키/축 주입 성공을 실제 장치 확인으로 확대하지 않는다. 기존1280/1920 UI·8수업 연속 진행·Best Lap 재실행·설정/입력 표시 수동 확인도 별도 유지한다.

### 추가 자동 회귀 판정 전 화면 확인

TEST-RENDER-UNPAINTED-01: 새벽 전체5회 중3회(당시 관찰) PIE 화면이 그려지지 않음(LobbyLayout `samples=0`, 렌더 전용 Shotgun Fail이 Success로 바뀜). 이 실행은 GamepadMissionFlow/GamepadNavigation/TitleFiveMenu/TitleFiveMenuWidget/TutorialComplete/TutorialNextLesson 포커스6개가 동반 Fail하므로 화면 포커스 판정에서 제외한다. `-stdout`·MCP 포트와 무관·원인 미특정. 새벽 화면그려진 test3.log의94/90/4는 당시근거이며 최신후속95개2회는 아래와 같이별도판정한다. `.claude/known-test-failures.md`의 판정 절차를 따른다. 같은 증상 수정→검증2회 후 중단했으므로 사람 확인/추가 관찰 카드로 유지한다.

최신 오후 전체97개중86 Success·11 Fail은 PIE 미렌더이며 오늘10회 중8회 발생했다. 패드 포커스6개 판정 제외·당시 나머지5개(후속 Shotgun 해결·전체 재실행 아님)는 NPCPerception·Shotgun 판정 오류(후속 해결)·LobbyLayout samples=0 진단·팀원 TrainingAssets/TrainingPIESmoke. Shotgun은 미렌더 표지에서 제외하고 렌더 전용으로 분류하지 않는다. 화면 그려진 포커스 확인 대기·Production 보존.

### 장거리 표시선 수동 확인 — 10/04 C PC

Claude 곡률 분할·MaximumCourseLineSegments 기본1024(시작값·미확정)·BP드래그재구성Off는 구현됨·자동검증됨. TestMap 짧은 코스68/113조각은 기존 균일분할 유지. 팀원은 Production코스 급커브·원경·끝연결과 Editor편집체감을 확인한다. Production은 읽기 전용 측정·MCP캡처만 했고 맵미저장. 기능검증은TestMap, Production편집/저장은 맵소유팀원만. 상세 수치·2048검토·46/258ms비용은 [저작가이드](../tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md)를 따른다.

### pull 뒤 레이싱 지형 확인

Claude 조사(10/04 C PC pull41444c2·LFS 실제 파일 수신): 팀원 코스는 MWLandscapeAutoMaterial 예제 Island/MountainRange 계열1개·PlayerStart 없음, 아이템/Gate 자산의 맵·DA 참조 없음. 제품 DA는 `TestMap/Lvl_DroneRacingTest`. 제품으로 사용할 지형·PlayerStart·완주/복귀 연결은 사용자/팀원 결정 대기이며 이번 맵 미수정·제품 지형 완주 수동 Pass 없음.

## 9/17 안전 감사 추가

최신 Source와 STATUS/WORKBOARD를 우선한다. 기존 본문의 샷건 `6°`/Cyan 기본 표시/공통 3° 데드존 설명은 과거 기록이며, 현재는 **12° 반각, Cyan 기본 Off, 몸 3° stop/6° start Hysteresis + Bone Gaze 잔여 보간**이다. 사거리 안 즉시 사격/밖 0.2초 확인 후 추적이 현재 계약이다.

Weather TestMap은 최신 Editor 빌드 후 Play에서 숫자열 **7 Clear / 8 LightWind / 9 RainStorm**으로 맵 저장 없이 Snapshot을 즉시 전환한다. 배치된 Random Weather Manager는 8방향+무풍을 사용하며 Flight HUD와 Visualizer에 Cardinal/m/s로 표시한다. RainStorm에서는 강우 값에 반응하는 최대 80개의 저빈도 디버그 선분 프리뷰를 확인할 수 있다. 이는 실제 Niagara 효과나 GPU 최적화 완료를 의미하지 않는다. Wetness consumer·Audio는 여전히 후속 작업이다. 조작 비교 키는 `1/2/3/4`다.

정확한 명령, 무저장 경계, NPC 재현 항목, 미구현 품질 preset 후보 및 `stat unit/gpu/niagara` 비교 절차는 Unreal repo `Tools/AssetMigration/README_NPC_WEATHER_TEST.md`를 따른다. 현재 C PC 설치 엔진은 Build.version상 **5.8.3**·CL58210709(2026-10-04 확인), 이전 PC의5.8.1/5.8.2 기록과 구분한다. 기존 Weather Validate 도구는 자산 생성 fallback이 있어 이번 읽기 전용 감사에는 사용하지 않았다.

## 맵 구성

| 맵 | 담당 기능 | 현재 상태 |
|---|---|---|
| `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest` | 비행 Ring, 역할 표적, Carryable, HUD | 저장 계약·Map Check·자동화 완료, 화면 확인 대기 |
| `/Game/Drone/Maps/TestMap/Lvl_DroneTrainingRouteSelectionTest` | 편집 가능한 Training Route 4개와 고정/무작위 선택 | `1~4` 고정·`5` 무작위, 각 Gate 5개, Map Check 0/0·실제 키 PIE 통과 |
| `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox` | 적·아군 NPC, Smart Object, 유인 MG, 자동포탑, 지면 추종 차량 | 기존 맵을 AssetTools로 이동, Asset·PIE·감지/수색 회귀 통과 |
| `/Game/Drone/Maps/TestMap/Lvl_DroneMissionSystemsTest` | 재밍 강도/겹침, 귀환 Zone, 정찰·파괴·투하 대상 | 신규 경량 맵 생성, Map Check 0/0·저장 계약 자동화 통과 |
| `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialMissionTest` | 실제 Mission GameMode에서 Figma Tutorial 8개 수업을 각각 선택해 시험 | Mission Definition 8개, Map Check 0/0·집중 회귀 9/9 통과 |
| `/Game/Drone/Maps/TestMap/Lvl_DroneShotgunSystemsTest` | 샷건 NPC 감지·산탄 분포·투사체·탄약·정면 시선 안정화 검증 | 발광 Pellet 8개+짧은 Tracer 실제 BP, 몸/고개 3° 데드존, Map Check 0/0·Asset/PIE 자동화 2/2 통과 |
| `/Game/Drone/Maps/TestMap/Lvl_DroneWeatherSystemsTest` | 8방향+무풍 Random Weather, 조작 모드별 Drone 보정, 강우 데이터/디버그 프리뷰 체감 | Manager 원뿔 Editor 전용·무충돌, 이동 Bead 24개·Cardinal/m/s Readout·1/2/3/4 키·7/8/9 날씨 키. 비 선분은 TestMap 전용 DrawDebug 프리뷰이며 Niagara가 아님 |

Production `/Game/Drone/Maps/Lvl_DroneTraining`은 팀원이 제작 중인 실제 Tutorial 맵이다. 시험 Actor 추가, 자동 재구성, 저장 대상으로 사용하지 않는다.

## Mission Systems 시험 맵 배치

시작점에서 `+X` 방향으로 진행하면 다음 순서다.

1. `MissionSystemsTest_JammerWeak`: 강도 `0.35`, 약한 재밍 구역
2. 약한/강한 구역 겹침: 여러 Source 중 최댓값 `0.80` 적용 확인 구간
3. `MissionSystemsTest_JammerStrong`: 강도 `0.80`, 강한 재밍과 비행 배율 확인 구역
4. `MissionSystemsTest_ReturnZone`: Tag `Test.Mission.ReturnZone`, 귀환 Box

옆 공간에는 Recon, Impact, Payload 역할 표적 각 1개와 Carryable 1개를 배치했다. 바닥의 얇은 Cube 세 개는 구역 위치를 찾기 위한 Greybox 표식이며 충돌하지 않는다.

이 맵의 기본 GameMode는 `BP_DronePrototypeGameMode`다. 맵을 바로 Play하면 Drone 조종·Signal HUD·역할 기능을 빠르게 확인할 수 있다. 다만 이 직접 실행은 Mission Flow를 통과하지 않으므로 Return Zone에 들어가도 Mission 완료 화면은 뜨지 않는다. Return 목표까지 확인하려면 후속 Test Mission Data Asset과 Mission 진입 경로가 필요하다.

## Tutorial Mission 시험 맵 배치

`Lvl_DroneTutorialMissionTest`는 `BP_DroneMissionGameMode`를 사용하며 로비에서 선택한 다음 8개 Definition이 같은 맵을 공유한다.

- `DA_Mission_Tutorial_Hover`: Scout, Hover Zone 3초 → Return Zone
- `DA_Mission_Tutorial_Forward`: Scout, 전방 Trigger 통과 → Return Zone
- `DA_Mission_Tutorial_Heading`: Scout, 원형 코스의 시작·체크포인트 7개·결승을 정방향 완주 → Return Zone (2026-10-01 정정)
- `DA_Mission_Tutorial_GateFlight`: Scout, Gate 4개를 순서·정방향으로 통과
- `DA_Mission_Tutorial_FPV`: FPV Strike, Arm 뒤 체력 100 표적 파괴
- `DA_Mission_Tutorial_Payload`: Drop, Payload Target 적중 → Return Zone
- `DA_Mission_Tutorial_UGV_NPC`: Ground UGV, 체력 100의 정지 적 NPC 처치
- `DA_Mission_Tutorial_UGV_Turret`: Ground UGV, 체력 100 고정 포탑 Greybox 파괴

맵 직접 Play보다 `/Game/Drone/Maps/Lvl_DroneFrontEnd` 로비에서 Mission을 선택해 들어가야 Director·목표 HUD·성공/실패 화면까지 확인할 수 있다. 배치 재생성은 다음 명령만 사용한다.

```powershell
cd C:\URproject\drone
.\Tools\AssetMigration\Invoke-DroneTutorialMissionTest.ps1 -Mode Validate
.\Tools\AssetMigration\Invoke-DroneTutorialMissionTest.ps1 -Mode Rebuild
```

`Rebuild`는 `DroneTutorialMissionTest.Owned` Tag를 가진 전용 Actor만 다시 만든다. Production Training 맵은 대상이 아니다.

### Figma Tutorial과의 대응 범위

2026-09-24 Figma `Project:Droner`의 Tutorial 상세를 읽기 전용으로 다시 확인했다. 기획상 전체 수업은 `호버링 → 전진 → 회전 → 게이트 자유비행 → 자폭 드론 → 드랍 드론 → UGV 적 NPC 처치 → 고정형 포탑 처치`의 8개다. 각 수업은 조작키·목표 브리핑, 시작, 플레이, 클리어 타임 UI를 반복하고 마지막에 전체 완료 UI가 나온다.

현재 `Lvl_DroneTutorialMissionTest`에는 8개 수업의 독립 Mission Flow와 Station이 모두 있다. 회전과 게이트는 서로 다른 Tag의 `BP_DroneTrainingCourse`로 구분하고, UGV는 상부 조준 Pivot을 따르는 총·유탄 Projectile을 사용한다. UGV 총은 좌클릭/패드 Right Shoulder, 유탄은 우클릭/패드 Left Shoulder다. 독립 `Lvl_DroneRacingTest`는 로비 레이싱 탭에서 들어간다. [시작 화면·탭·원형 코스 가이드](DRONE_TITLE_LOBBY_ORBIT_GUIDE.md)를 함께 본다.

기능 판정과 독립 재시도는 구현됐지만 단계별 클리어 타임·8개 연속 진행·전체 완료 UI는 아직 없다. Figma의 Warehouse 사용 메모도 반영하지 않은 평면 Greybox다. 이 시험장에서 수동 체감을 확인한 뒤 검증된 Station만 팀원 Tutorial 환경에 수동 이식한다.

### 8개 수업 수동 확인

항상 `/Game/Drone/Maps/Lvl_DroneFrontEnd`에서 Play하고 로비의 해당 수업을 선택한다. 맵을 직접 Play하면 선택 Mission이 없어 Director 전체 흐름을 확인할 수 없다.

1. 호버링: Zone 안에서 속도와 자세를 안정시키고 3초 유지한 뒤 Return Zone으로 돌아간다.
2. 전진: 시작점 앞 `TutorialMissionTest_ForwardGoal` Box를 통과한 뒤 Return Zone으로 돌아간다.
3. 회전: 원형 안내선을 따라 Gate 0 → 1~7 → 결승 8을 순서대로 한 바퀴 통과한 뒤 Return Zone으로 돌아간다. 제자리 Yaw나 다른 코스 완주로 완료되면 안 된다.
4. 게이트: 네 Ring을 번호 순서와 Ring 로컬 `+X` 방향으로 통과한다.
5. FPV: 좌클릭으로 Arm하고 충분한 속도로 `TutorialMissionTest_FPVTarget`에 충돌한다.
6. 드랍: 좌클릭으로 화물을 투하해 Payload Target에 맞힌 뒤 Return Zone으로 돌아간다.
7. UGV NPC: 차체는 이동 입력으로, 상부는 시점 입력으로 조준하고 좌클릭 총 4발 이상을 적중시킨다.
8. UGV 포탑: 좌클릭 총 또는 우클릭 유탄으로 고정 표적을 파괴한다. 유탄은 중력 낙차가 있으므로 포신을 위로 보정한다.

## Shotgun Systems 시험 맵 배치

`Lvl_DroneShotgunSystemsTest`는 기존 Smart Object 맵의 NPC 수와 MG·순찰 경합 시간을 바꾸지 않기 위한 독립 사격장이다.

- 시작점과 `ShotgunSystemsTest_HostileShotgun` 사이 거리는 약 9m다.
- 샷건 NPC는 드론을 정면에서 감지하고 기본 투사체 방식으로 사격한다.
- 바닥 옆의 5m·10m·15m 표식은 수동 거리 비교용이며 최종 사거리 규칙이 아니다.
- 중앙 사선은 자동 발사용으로 비워 두었다. 옆 `ShotgunSystemsTest_LOSBlocker`는 NPC 또는 Drone을 옮겨 시야 차단을 시험할 때 쓴다.
- 기본 회색상자 값은 `8 Pellet`, `6° 반각`, `3500 cm/s`, `8 Shell`, Pellet당 `3 Damage`(전탄 최대 24), 발사 간격 `0.9초`다. 밸런스 확정값이 아니다.
- Cyan 선은 Projectile이 향하는 산탄 원뿔의 예상 비행선이다. 실제 충돌과 피해는 이동 Projectile이 담당한다.
- 탄두 외형은 실제 샷건이 모든 맵에서 쓰는 `/Game/Drone/AI/Blueprints/Projectiles/BP_ShotgunPelletProjectile`이다. `ProjectileVisual`은 `0.04` 크기 주황 발광 비드, `ProjectileTrailVisual`은 길이 `0.20`·두께 `0.0125`의 같은 발광 재질을 사용한다. 두 Component의 Static Mesh/Material/Transform을 Blueprint에서 바꿀 수 있다.
- 발광 재질은 `/Game/Drone/AI/Materials/M_ShotgunPelletGlow`다. 밝기·색을 바꾸려면 이 Material의 Emissive Color 상수를 조정한다.
- 어떤 탄환 BP를 쓸지는 `BP_NPC_Hostile_Shotgun > NPCWeaponComponent > Projectile Class`, Pellet 수·확산·피해·탄속·탄창은 같은 Component의 Shotgun/Projectile/Damage/Ammo 항목에서 조정한다.
- 샷건 NPC의 몸/고개가 정면 부근에서 좌우로 왕복하면 `BP_NPC_Hostile_Shotgun > NPCProfileComponent > Profile > NPC|Gaze > Personal Weapon Facing Dead Zone Degrees`를 조정한다. 기본 `3°`는 표적이 조준선 근처에서 조금 움직일 때 몸체와 Bone Gaze가 번갈아 쫓지 않게 한다. 같은 곳의 `Personal Weapon Facing Turn Speed Degrees Per Second` 기본 `180`으로 몸 회전속도를 바꾼다.

기존 `Lvl_NPCSmartObjectGreybox`의 샷건 NPC 1명은 그대로다. 따라서 시험 맵 전체에는 샷건 NPC가 2명 있지만, 한 맵 안의 순찰·점유 경쟁 수는 변하지 않았다.

## Weather Systems 시험 맵 배치

- `WeatherSystemsTest_Controller`는 `/Game/Drone/Weather/Blueprints/BP_DroneRandomWeatherController`다. `DA_Weather_LightWind`를 BeginPlay에 적용하고 기본 8방향+무풍, 방향 8~18초, 세기 5~12초, 1~9m/s를 사용한다.
- Manager는 에디터에서 원뿔로 보이지만 Play/Package에는 표시되지 않고 Collision·Overlap·Navigation 영향이 없다.
- 시작값은 지속풍 `4m/s`, 돌풍 `+0~2m/s`, 풍향 `35°`, 난류 `0.2`다. 최종 밸런스가 아니다.
- 바닥의 큰 Cube 화살표는 35° 풍향을 가리키며 충돌하지 않는다.
- `WeatherSystemsTest_Visualizer`는 현재 Snapshot 풍향으로 24개 Bead를 움직이고 화면에 Profile·Cardinal 풍향·m/s·현재 조작 모드를 표시한다.
- 쉬운 조작은 기본 65%, 제한 자세는 25%, Rate/Acro는 0% 보정을 사용한다. `WeatherResponseComponent` 기본값에서 바꿀 수 있다.
- Play 중 숫자1/2/3/4 또는 NumPad1/2/3/4로 Easy/Manual/Acro Mode1/Acro Mode2를 즉시 바꿔 같은 바람에서 Drift를 비교한다.
- Bead 수·범위·크기·재생 속도와 표시/키 사용 여부는 `/Game/Drone/Weather/Blueprints/BP_DroneWeatherDebugVisualizer` 또는 배치 인스턴스에서 조정한다.
- `Weather Profile`을 `DA_Weather_Clear` 또는 `DA_Weather_RainStorm_Greybox`로 교체할 수 있다. 폭우 Profile은 비 수치를 전달하지만 Niagara가 아직 없으므로 빗줄기가 안 보이는 것이 정상이다.

## 수동 확인 순서

### Mission Systems

1. `Lvl_DroneMissionSystemsTest`를 열고 Play한다.
2. 약한 구역에서 신호 단계와 신호율이 변하는지 본다.
3. 두 구역이 겹치는 곳에서 강한 값이 우선되는지 본다.
4. 강한 구역에서 속도·가속도 저하가 발생하고 빠져나오면 원래 값으로 돌아오는지 본다.
5. Recon/Impact/Payload 역할 기능과 Carryable 픽업·드랍을 각각 확인한다.
6. Return Zone 위치와 크기가 수동 비행에 적당한지 확인한다. Mission 완료 판정은 후속 Mission Flow 시험에서 확인한다.

### Smart Object

1. `Lvl_NPCSmartObjectGreybox`를 열고 Play한다.
2. Hostile Rifle/Shotgun의 순찰, Drone 발견, 수색, 복귀를 본다. 순찰·추적 중 정지/걷기/뛰기 전환·속도 대비 보폭/발 미끄러짐·뒷걸음 방향을 확인한다. 적의 양손 총 들기·걷기/조준, 총의 오른손 hand_r 추종·왼손 총 위, 손/총 정렬(특히 산탄총)·사격/재장전을 확인한다. AI-LOCOMOTION-01 후속 구현됨·자동 검증됨(2026-10-04 C PC, 작업·검증 Claude)·수동 확인 대기. Mannequin 원본과 Insurgent/Quantum 메시의 스켈레톤 불일치로 양팔을 벌리던 문제를 사용자 선택 IK Retarget으로 수정하고 적 Gun을 hand_r에 부착. 속도 > 3 이동 판정·Gaze 유지. NPCLocomotionAnimPIE 오프스크린 Success: 이동40개(NPC5명) ShouldMove40, 위팔 기본 자세 대비 평균51.7°·40/40, 총 든 NPC 양손 간격 평균34.4cm·24/24, 총 hand_r 추종·왼손 총 위 각각24/24. Drone.AI 19개 중18 Success·기존 NPCPerceptionSearchPIE 1 Fail(state=1 detected=0), 새 실패 없음. 자산 Verify success(ClaudeNPCWalk/rt_tests3.log·ai_suite.log·verify_rt3.log). 걷기/뛰기 전환·발 미끄러짐·뒷걸음 방향·손/총 정렬(특히 산탄총)·사격/재장전은 사용자 수동 확인 대기. CR_Mannequin_FootIK는 Insurgent 계층 차이로 Editor 컴파일 경고 잔존. Epic 마네킹 변환 임시 동작·최종 아님; 최종 애니메이션 미구현·자산 미정, 산탄총 전용 동작 미구현·도입 여부 미정(소총 동작 공유).
3. Cyan Slot 방향과 NPC 도착 방향이 일치하는지 본다.
4. 유인 MG 점유와 사수 사망 뒤 생존 NPC 재점유를 확인한다.
5. 설치형·차량형 자동포탑의 Yaw/Pitch, 장애물 차단, 차량 부모 추종을 확인한다.
6. Friendly NPC가 적 대응과 섞이지 않고 기지 동선을 유지하며 팔을 내린 비무장 걷기를 하는지 본다.

### Shotgun Systems

1. `Lvl_DroneShotgunSystemsTest`를 열고 Play한다.
2. 시작 직후 샷건 NPC가 드론을 감지하고 사격하는지 본다.
3. 한 번의 발사에서 주황 발광 비드/Tracer 8개와 Cyan 선 8개가 6° 원뿔 안에서 서로 다르게 퍼지는지 본다.
4. 이동하면 Pellet Projectile을 피할 여지가 있는지, 가까이 가도 한 Volley 최대 24 피해가 체력 100에 적당한지 체감한다.
5. NPC를 16m보다 멀리 옮겼을 때 개인 샷건 사격이 멈추는지 확인한다.
6. NPC 또는 PlayerStart를 옆 LOS Blocker 뒤로 옮겨 벽을 뚫고 피해가 들어가지 않는지 확인한다.
7. `BP_NPC_Hostile_Shotgun`의 `NPCWeaponComponent`에서 Spread, Pellet Count, Projectile Speed, Damage, Magazine을 바꿔 비교한다. 최종값은 사용자 확인 전 저장 기본값으로 확정하지 않는다.
8. 드론을 NPC 정면에서 조금씩 좌우로 움직였을 때 몸과 고개가 계속 좌우 왕복하지 않고, 3°를 넘는 큰 이동에는 자연스럽게 따라오는지 확인한다.

### Weather Systems

1. `Lvl_DroneWeatherSystemsTest`를 열고 Play한다.
2. 에디터에 있던 Manager 원뿔이 Play에서 사라지고 Drone과 접촉하지 않는지 본다.
3. 20~40초 동안 `E/NE/N/NW/W/SW/S/SE/CALM`과 m/s가 바뀌며 움직이는 Bead·실제 Drift와 일치하는지 본다.
4. 입력을 놓고 `1 Easy / 2 Manual / 3 Acro Mode 1 / 4 Acro Mode 2`를 눌러 같은 바람에서 보정률과 Drift 차이가 구분되는지 본다.
5. 방향·세기 변경 때 Bead와 Drift가 순간이동하지 않고 설정한 Blend 시간에 맞게 부드럽게 변하는지 본다.
6. 숫자열 `7/8/9`로 Clear/LightWind/RainStorm 디버그 Preset과 강우 선분을 비교한다. Random Wind를 완전히 끈 Profile 고정 시험은 Manager의 `Enable Random Wind`를 꺼서 수행한다.
7. `RainStorm_Greybox`의 최대 수평풍 약 10.7m/s는 강풍 시험 참고선이다. 모든 기체의 최종 내풍 한계로 확정하지 않는다.

## 생성·검증 도구

Unreal Editor를 닫은 상태에서 프로젝트 루트에서 실행한다.

```powershell
# 현재 저장 상태만 검증
.\Tools\AssetMigration\Invoke-DroneMissionTestMaps.ps1 -Mode Validate

# Mission Systems 맵의 도구 소유 Actor 14개만 다시 생성
.\Tools\AssetMigration\Invoke-DroneMissionTestMaps.ps1 -Mode Rebuild

# Smart Object 시험 맵 이동까지 함께 수행한다. 이미 이동된 경우 읽기 검증만 한다.
.\Tools\AssetMigration\Invoke-DroneMissionTestMaps.ps1 -Mode Validate -MoveSmartObjectMap

# Shotgun 사격장 저장 상태만 검증
.\Tools\AssetMigration\Invoke-DroneShotgunTestMap.ps1 -Mode Validate

# Shotgun 사격장의 도구 소유 Actor만 다시 생성
.\Tools\AssetMigration\Invoke-DroneShotgunTestMap.ps1 -Mode Rebuild

# Weather Profile 3종을 생성·동일 값으로 갱신
# Unreal Editor Python 실행 대상으로 Tools/AssetMigration/BuildDroneWeatherProfiles.py 사용

# Weather 맵과 Visualizer 저장 상태 검증
.\Tools\AssetMigration\Invoke-DroneWeatherTestMap.ps1 -Mode Validate

# Weather 맵의 도구 소유 Actor만 다시 생성
.\Tools\AssetMigration\Invoke-DroneWeatherTestMap.ps1 -Mode Rebuild
```

각 `Rebuild`는 각각 `DroneMissionSystemsTest.Owned`, `DroneTutorialMissionTest.Owned`, `DroneShotgunSystemsTest.Owned`, `DroneWeatherSystemsTest.Owned` Tag가 있는 Actor만 제거·재생성한다. 팀원이 수동 추가한 Actor는 이 Tag를 임의로 붙이지 않는다.

## 자동화 근거

- `Drone.Mission.MissionSystemsTestMap`: 두 Jammer 강도·겹침, Return Tag/Trigger, Actor 14개, Prototype GameMode 확인
- `Drone.Tutorial.MissionLessonsTestMap`: 8개 Station, Mission GameMode, 8개 Definition의 기체 제한·목표 Event/Tag 순서 확인
- `Drone.Tutorial.HeadingZone`: 최단 Yaw 각도와 기본 판정 수치 확인
- `Drone.Weapons.GroundUGV`: 총·유탄 Component, 투사체 모드·피해 기본값과 Muzzle 연결 확인
- `Drone.AI.NPCGreyboxAssets`: 이동된 Smart Object 맵의 저장 Asset 계약 확인
- `Drone.AI.NPCGreyboxPIE`: 이동된 맵의 NPC·Station·Nav/PIE 기본 동작 확인
- `Drone.AI.NPCPerceptionSearchPIE`: Drone 감지·수색·복귀 경로 확인
- `Drone.AI.ShotgunSystemsTestMap`: 전용 맵·NPC·전용 Pellet BP·3 피해·작은 비드/Tracer·GameMode·Nav 배치와 샷건 기본 계약 확인
- `Drone.AI.ShotgunSystemsTestMapPIE`: 실제 감지 뒤 8개 Projectile 생성, Shell 소모, 6° 원뿔·독립 방향과 정면 ±약 1.9° 미세 움직임의 몸체 안정화 확인
- `Drone.AI.ShotgunTrace`: 즉시 Trace 비교 모드의 피해·차단·탄창 비움·명시적 재장전 확인
- `Drone.Weather.ProfileAndWindContract`: Profile Validation, World Snapshot 단위 변환, 쉬운 조작/Rate-Acro 보정 차이 확인
- `Drone.Weather.ProfileAssets`: Clear/LightWind/RainStorm 저장 Asset과 핵심 값 확인
- `Drone.Weather.SystemsTestMap`: Random Weather Controller 1개, LightWind·8방향+무풍 설정, Prototype GameMode, Visualizer 1개·Bead 24개·Readout/모드 키와 도구 소유 Actor 확인
- 위 항목과 Mission Rule·Signal Stage를 묶은 최종 회귀 `6/6 Success`
- 샷건 전용 최종 회귀 `2/2 Success`, 경고 0. 전체 샷건 계약 묶음 `5/5 Success`, 실패 0

## 다음 구현 경계

1. 샷건 사격장의 산탄 가시성·피하기 체감·피격 피해를 Editor 화면에서 확인한다.
2. Tutorial 8개를 FrontEnd에서 손 조작해 위치·크기·각도·탄속·낙차를 확정한다.
3. Camera-follow Niagara Rain·젖음 MPC·Audio를 Weather Snapshot에 연결하고 TestMap에서 성능을 측정한다.
4. 중간/강한 재밍의 영상 Noise Material과 목표 정보 손실 표현을 붙인다.
5. Mission 1 전용 Map/DA Vertical Slice를 만든다.
6. 광섬유 Drone·UGV와 한 Mission 안의 기체 교대를 구현한다.
7. 소유권 감사 뒤 `Lvl_DronePrototype`, `Lvl_DronePackShowcase`, `Lvl_MilitaryBase_Test`도 TestMap 아래로 옮긴다.

Story Mission의 최종 지형·수치·규칙은 아직 확정하지 않는다. 이 문서의 위치와 값은 기능 검증용 Greybox 기준이다.
