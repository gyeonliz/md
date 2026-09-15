# Drone 기능 시험 맵 가이드

기준일: 2026-09-16

## 맵 구성

| 맵 | 담당 기능 | 현재 상태 |
|---|---|---|
| `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest` | 비행 Ring, 역할 표적, Carryable, HUD | 저장 계약·Map Check·자동화 완료, 화면 확인 대기 |
| `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox` | 적·아군 NPC, Smart Object, 유인 MG, 자동포탑, 지면 추종 차량 | 기존 맵을 AssetTools로 이동, Asset·PIE·감지/수색 회귀 통과 |
| `/Game/Drone/Maps/TestMap/Lvl_DroneMissionSystemsTest` | 재밍 강도/겹침, 귀환 Zone, 정찰·파괴·투하 대상 | 신규 경량 맵 생성, Map Check 0/0·저장 계약 자동화 통과 |
| `/Game/Drone/Maps/TestMap/Lvl_DroneShotgunSystemsTest` | 샷건 NPC 감지·산탄 분포·투사체·탄약 검증 | 추가 샷건 NPC 1명 배치, Map Check 0/0·Asset/PIE 자동화 2/2 통과 |
| `/Game/Drone/Maps/TestMap/Lvl_DroneWeatherSystemsTest` | 지속풍·돌풍과 조작 모드별 Drone 보정 체감 | LightWind Controller·풍향 화살표, Map Check 0/0·저장 계약 자동화 통과 |

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
- 기본 회색상자 값은 `8 Pellet`, `6° 반각`, `3500 cm/s`, `8 Shell`, Pellet당 `8 Damage`, 발사 간격 `0.9초`다. 밸런스 확정값이 아니다.
- Cyan 선은 Projectile이 향하는 산탄 원뿔의 예상 비행선이다. 실제 충돌과 피해는 이동 Projectile이 담당한다.

기존 `Lvl_NPCSmartObjectGreybox`의 샷건 NPC 1명은 그대로다. 따라서 시험 맵 전체에는 샷건 NPC가 2명 있지만, 한 맵 안의 순찰·점유 경쟁 수는 변하지 않았다.

## Weather Systems 시험 맵 배치

- `WeatherSystemsTest_Controller` 한 개가 `DA_Weather_LightWind`를 BeginPlay에 즉시 적용한다.
- 시작값은 지속풍 `4m/s`, 돌풍 `+0~2m/s`, 풍향 `35°`, 난류 `0.2`다. 최종 밸런스가 아니다.
- 바닥의 큰 Cube 화살표는 35° 풍향을 가리키며 충돌하지 않는다.
- 쉬운 조작은 기본 65%, 제한 자세는 25%, Rate/Acro는 0% 보정을 사용한다. `WeatherResponseComponent` 기본값에서 바꿀 수 있다.
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
3. 한 번의 발사에서 Cyan 선 8개가 6° 원뿔 안에서 서로 다르게 퍼지는지 본다.
4. 이동하면 Pellet Projectile을 피할 여지가 있는지, 가까이 가면 여러 Pellet 피격이 체력 100에 과도하지 않은지 체감한다.
5. NPC를 16m보다 멀리 옮겼을 때 개인 샷건 사격이 멈추는지 확인한다.
6. NPC 또는 PlayerStart를 옆 LOS Blocker 뒤로 옮겨 벽을 뚫고 피해가 들어가지 않는지 확인한다.
7. `BP_NPC_Hostile_Shotgun`의 `NPCWeaponComponent`에서 Spread, Pellet Count, Projectile Speed, Damage, Magazine을 바꿔 비교한다. 최종값은 사용자 확인 전 저장 기본값으로 확정하지 않는다.

### Weather Systems

1. `Lvl_DroneWeatherSystemsTest`를 열고 Play한다.
2. 입력을 놓았을 때 바닥 화살표 방향으로 기체가 천천히 밀리는지 본다.
3. 쉬운 조작과 Rate/Acro를 바꿔 같은 바람에서 Drift 차이가 구분되는지 본다.
4. 화살표를 기준으로 순풍·역풍·횡풍을 비행해 조작을 빼앗는 느낌이 과한지 확인한다.
5. `WeatherSystemsTest_Controller`의 Profile을 `Clear`로 바꿨을 때 Drift가 사라지는지 확인한다.
6. `RainStorm_Greybox`의 최대 수평풍 약 10.7m/s는 강풍 시험 참고선이다. 모든 기체의 최종 내풍 한계로 확정하지 않는다.

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

# Weather 맵 생성 또는 저장 상태 검증
# Unreal Editor Python 실행 대상으로 Tools/AssetMigration/BuildDroneWeatherSystemsTestMap.py 사용
```

각 `Rebuild`는 각각 `DroneMissionSystemsTest.Owned` 또는 `DroneShotgunSystemsTest.Owned` Tag가 있는 Actor만 제거·재생성한다. 팀원이 수동 추가한 Actor는 이 Tag를 임의로 붙이지 않는다.

## 자동화 근거

- `Drone.Mission.MissionSystemsTestMap`: 두 Jammer 강도·겹침, Return Tag/Trigger, Actor 14개, Prototype GameMode 확인
- `Drone.AI.NPCGreyboxAssets`: 이동된 Smart Object 맵의 저장 Asset 계약 확인
- `Drone.AI.NPCGreyboxPIE`: 이동된 맵의 NPC·Station·Nav/PIE 기본 동작 확인
- `Drone.AI.NPCPerceptionSearchPIE`: Drone 감지·수색·복귀 경로 확인
- `Drone.AI.ShotgunSystemsTestMap`: 전용 맵·NPC·Profile·GameMode·Nav 배치와 샷건 기본 계약 확인
- `Drone.AI.ShotgunSystemsTestMapPIE`: 실제 감지 뒤 8개 Projectile 생성, Shell 소모, 6° 원뿔과 독립 방향 확인
- `Drone.AI.ShotgunTrace`: 즉시 Trace 비교 모드의 피해·차단·탄창 비움·명시적 재장전 확인
- `Drone.Weather.ProfileAndWindContract`: Profile Validation, World Snapshot 단위 변환, 쉬운 조작/Rate-Acro 보정 차이 확인
- `Drone.Weather.ProfileAssets`: Clear/LightWind/RainStorm 저장 Asset과 핵심 값 확인
- `Drone.Weather.SystemsTestMap`: Weather Controller 1개, LightWind 연결, Prototype GameMode와 도구 소유 Actor 8개 확인
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
