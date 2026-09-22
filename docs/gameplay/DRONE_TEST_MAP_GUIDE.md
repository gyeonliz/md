# Drone 기능 시험 맵 가이드

기준일: 2026-09-17

## 9/17 안전 감사 추가

최신 Source와 STATUS/WORKBOARD를 우선한다. 기존 본문의 샷건 `6°`/Cyan 기본 표시/공통 3° 데드존 설명은 과거 기록이며, 현재는 **12° 반각, Cyan 기본 Off, 몸 3° stop/6° start Hysteresis + Bone Gaze 잔여 보간**이다. 사거리 안 즉시 사격/밖 0.2초 확인 후 추적이 현재 계약이다.

Weather TestMap은 최신 Editor 빌드 후 Play에서 숫자열 **7 Clear / 8 LightWind / 9 RainStorm**으로 맵 저장 없이 Snapshot을 즉시 전환한다. 배치된 Random Weather Manager는 8방향+무풍을 사용하며 Flight HUD와 Visualizer에 Cardinal/m/s로 표시한다. RainStorm에서는 강우 값에 반응하는 최대 80개의 저빈도 디버그 선분 프리뷰를 확인할 수 있다. 이는 실제 Niagara 효과나 GPU 최적화 완료를 의미하지 않는다. Wetness consumer·Audio는 여전히 후속 작업이다. 조작 비교 키는 `1/2/3/4`다.

정확한 명령, 무저장 경계, NPC 재현 항목, 미구현 품질 preset 후보 및 `stat unit/gpu/niagara` 비교 절차는 Unreal repo `Tools/AssetMigration/README_NPC_WEATHER_TEST.md`를 따른다. 이 PC 설치 엔진은 Build.version상 **5.8.2**이며 5.8.1 검증으로 표기하지 않는다. 기존 Weather Validate 도구는 자산 생성 fallback이 있어 이번 읽기 전용 감사에는 사용하지 않았다.

## 맵 구성

| 맵 | 담당 기능 | 현재 상태 |
|---|---|---|
| `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest` | 비행 Ring, 역할 표적, Carryable, HUD | 저장 계약·Map Check·자동화 완료, 화면 확인 대기 |
| `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox` | 적·아군 NPC, Smart Object, 유인 MG, 자동포탑, 지면 추종 차량 | 기존 맵을 AssetTools로 이동, Asset·PIE·감지/수색 회귀 통과 |
| `/Game/Drone/Maps/TestMap/Lvl_DroneMissionSystemsTest` | 재밍 강도/겹침, 귀환 Zone, 정찰·파괴·투하 대상 | 신규 경량 맵 생성, Map Check 0/0·저장 계약 자동화 통과 |
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
- Play 중 숫자 `1/2/3` 또는 NumPad `1/2/3`으로 Easy/Manual/Rate-Acro를 즉시 바꿔 같은 바람에서 Drift를 비교한다.
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
2. Hostile Rifle/Shotgun의 순찰, Drone 발견, 수색, 복귀를 본다.
3. Cyan Slot 방향과 NPC 도착 방향이 일치하는지 본다.
4. 유인 MG 점유와 사수 사망 뒤 생존 NPC 재점유를 확인한다.
5. 설치형·차량형 자동포탑의 Yaw/Pitch, 장애물 차단, 차량 부모 추종을 확인한다.
6. Friendly NPC가 적 대응과 섞이지 않고 기지 동선을 유지하는지 본다.

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

각 `Rebuild`는 각각 `DroneMissionSystemsTest.Owned`, `DroneShotgunSystemsTest.Owned`, `DroneWeatherSystemsTest.Owned` Tag가 있는 Actor만 제거·재생성한다. 팀원이 수동 추가한 Actor는 이 Tag를 임의로 붙이지 않는다.

## 자동화 근거

- `Drone.Mission.MissionSystemsTestMap`: 두 Jammer 강도·겹침, Return Tag/Trigger, Actor 14개, Prototype GameMode 확인
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
2. Test Mission Data Asset과 개발용 진입 경로를 만들어 Return/Jammer Mission Event를 실제 PIE에서 진행한다.
3. Camera-follow Niagara Rain·젖음 MPC·Audio를 Weather Snapshot에 연결하고 TestMap에서 성능을 측정한다.
4. 중간/강한 재밍의 영상 Noise Material과 목표 정보 손실 표현을 붙인다.
5. Mission 1 전용 Map/DA Vertical Slice를 만든다.
6. 광섬유 Drone·UGV와 한 Mission 안의 기체 교대를 구현한다.
7. 소유권 감사 뒤 `Lvl_DronePrototype`, `Lvl_DronePackShowcase`, `Lvl_MilitaryBase_Test`도 TestMap 아래로 옮긴다.

Story Mission의 최종 지형·수치·규칙은 아직 확정하지 않는다. 이 문서의 위치와 값은 기능 검증용 Greybox 기준이다.
