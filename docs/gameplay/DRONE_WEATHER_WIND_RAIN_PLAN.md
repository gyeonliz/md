# 드론 기상 변수·바람·비 구현 계획

기준일: 2026-09-17 (Asia/Seoul)

### 9/17 무저장 시험 진입 경로

기존 Weather TestMap의 native DebugVisualizer에 숫자열 `7 Clear / 8 LightWind / 9 RainStorm` 및 Rain/Spawn/Wet Readout을 추가했다. `ApplyTestWeatherPreset(0/1/2)`는 전용 맵에서만 즉시 Snapshot을 바꾸며 자산/맵을 저장하지 않는다. RainStorm은 Snapshot 강도·spawn scale을 받아 최대 80개, 5Hz의 제한된 DrawDebug 선분 프리뷰를 만든다. 비가 0이면 새 선분 생성을 멈추고 남은 선분은 약 0.3초 내 사라진다. 이는 Niagara/젖음/Audio 구현 또는 GPU 성능 검증이 아니다. 기존 1/2/3 조작 모드 키는 유지한다. 성능 비교 절차·품질 후보는 Unreal repo `Tools/AssetMigration/README_NPC_WEATHER_TEST.md`를 참고한다. Low~Epic preset 적용 또는 GPU 측정 결과로 간주하지 않는다.

## 현재 상태와 확정 경계

- `WTH-01` Profile/Snapshot/World Subsystem, `WTH-02` 지속풍·돌풍 Drone 응답, `WTH-02B` Attack/Release와 표시 벡터 적분은 2026-09-16 기준 구현됐다.
- `/Game/Drone/Data/Weather`에 `Clear`, `LightWind`, `RainStorm_Greybox` Profile이 있고, `/Game/Drone/Maps/TestMap/Lvl_DroneWeatherSystemsTest`는 `LightWind`를 즉시 적용한다.
- 비 Snapshot은 전용 Weather TestMap의 제한형 DrawDebug 선분 프리뷰에서만 소비한다. Camera-follow Niagara, 젖음 Material/MPC consumer, Audio, 실내 판정은 아직 구현 완료 기능이 아니다.
- 최종 Mission별 날씨, 비가 신호·체력·배터리에 미치는 영향, 최종 성능 예산은 현재 미정이다.
- 1차 Vertical Slice에서는 바람이 비행에 미치는 영향과 비의 시야·연출만 분리해 검증한다.
- 비를 맞는다고 Drone 체력 감소, 통신 두절, Mission 실패를 자동으로 넣지 않는다. 필요하면 별도 Mission Rule로 명시한다.

## 구현된 데이터 구조

`UDroneWeatherProfile` Data Asset 하나가 아래 값을 보관한다. Runtime은 `UDroneWeatherWorldSubsystem`이 World당 활성 Profile 하나와 `FDroneWeatherSnapshot`을 소유한다. 국소 기상 `ADroneWeatherVolume`은 후속 후보이며 현재 코드에 있다고 표현하지 않는다.

### 공통

| 변수 | 형식 | 시작 범위 | 용도 |
|---|---|---:|---|
| `WeatherId` | Name | 필수 | 저장·Mission·디버그 식별자 |
| `RandomSeed` | int32 | Mission 설정 | Gust와 시각 변동 재현 |
| `TransitionSeconds` | float | 코드 허용 0~60초 | 날씨 전환 보간 |
| `GameplayUpdateHertz` | float | 코드 허용 1~30Hz, 기본 10Hz | Gust Snapshot 갱신. Particle Tick과 분리 |

### 바람

| 변수 | 형식 | Greybox 시작값 | 설명 |
|---|---|---:|---|
| `WindDirectionYawDegrees` | float | 0° | World 수평 풍향 |
| `BaseWindSpeedMetersPerSecond` | float | 0~5 | 지속풍 |
| `GustAdditionalSpeedMetersPerSecond` | float | 0~3 | 돌풍 추가량 |
| `GustIntervalSeconds` | FVector2D | 2~8초 | 다음 돌풍 간격 범위 |
| `GustAttackSeconds` | float | 0.45~0.80초 | 더 강한 돌풍 목표로 올라가는 응답 시간 |
| `GustReleaseSeconds` | float | 1.2~1.8초 | 약한 돌풍 목표로 빠지는 응답 시간 |
| `DirectionResponseSeconds` | float | 0.65~1.0초 | 풍향 목표를 최단각으로 따라가는 응답 시간 |
| `Turbulence01` | float | 0~0.35 | 작은 방향·세기 흔들림 |
| `VerticalGustMetersPerSecond` | float | 0~1 | 선택형 상승·하강 기류 |
| `DroneWindResponseMultiplier` | float | 0~2 | 기체별 바람 영향 배율 |

첫 시험 Preset은 `Calm 0~2m/s`, `Light 3~5m/s`, `Strong Test 8~10.7m/s`로 둔다. 10.7m/s는 DJI Avata 2의 공개 최대 풍속 저항 참고선일 뿐 최종 게임 규칙이나 모든 기체의 한계가 아니다. [DJI Avata 2 공식 사양](https://www.dji.com/avata-2/specs)

### 비

| 변수 | 형식 | Greybox 시작 범위 | 설명 |
|---|---|---:|---|
| `RainIntensity01` | float | 0~1 | 모든 비 연출의 대표 강도 |
| `RainSpawnScale01` | float | 0~1 | Niagara 생성량 배율 |
| `VisibilityDistanceMeters` | float | 50~1000m | 안개·색감용 목표 시야 거리 |
| `ScreenDropletIntensity01` | float | 0~1 | FPV Camera 표면 연출 |
| `SurfaceWetness01` | float | 0~1 | Material Parameter Collection 젖음 값 |
| `GroundSplashScale01` | float | 0~1 | 근거리 바닥 Splash 밀도 |
| `IndoorRainAttenuation01` | float | 0~1 | 지붕 아래 비와 소리 감소 |
| `RainAudioVolume01` | float | 0~1 | 비 Audio Layer |

## Runtime 책임

1. `UDroneWeatherWorldSubsystem`은 현재/목표 Profile, 전환 Alpha, 결정적 Seed, 한 개의 `FDroneWeatherSnapshot`을 소유한다.
2. 바람 Gameplay Snapshot은 Profile 기본 `10Hz` Timer로 계산하고 매 Frame·매 Particle마다 난수를 만들지 않는다. 돌풍 세기는 Attack/Release, Yaw 편차는 최단각 Direction Response로 프레임 시간에 안정적인 지수 보간을 사용한다.
3. `UDroneWeatherResponseComponent`는 Snapshot을 Event로 받아 필요할 때만 Tick하고, Sweep 이동으로 현재 Greybox Drone에 Drift를 적용한다.
4. 기본 보정은 쉬운 조작 `65%`, 제한 자세 `25%`, Rate/Acro `0%`다. 모두 Blueprint 기본값에서 조정할 수 있으며 최종 밸런스가 아니다.
5. 현재 외력은 `UFloatingPawnMovement` 위에 더하는 위치 Drift Greybox다. 모터·PID·공기역학 또는 최종 네트워크 물리 구현이 아니다.
6. `ADroneWeatherController`를 Level에 하나 배치하고 Profile을 지정하면 BeginPlay에 적용한다.
7. `ADroneWeatherVolume`은 협곡·건물 입구용 후속 후보다. 현재는 구현되지 않았다.
8. Niagara는 Snapshot을 읽어 표현만 담당한다. Particle 위치로 Gameplay 비행력을 계산하지 않는다.
9. 멀티플레이를 추가하면 서버는 Profile ID·Seed·전환 시작 시각만 복제하고, 빗방울 Simulation은 각 Client가 수행한다.

## 현재 Profile과 시험 맵

| Asset | 시작값 | 용도 |
|---|---|---|
| `DA_Weather_Clear` | 바람 0, 비 0 | 기상 해제·기준선 |
| `DA_Weather_LightWind` | 지속풍 4m/s, 돌풍 +0~2m/s, Attack 0.8s / Release 1.8s / 방향 1.0s | 기본 수동 비행 체감 |
| `DA_Weather_RainStorm_Greybox` | 지속풍 8m/s, 돌풍 +0~2.7m/s, Attack 0.45s / Release 1.2s / 방향 0.65s, 비 0.8 | 비 표현과 강풍 후속 시험용 데이터 |

`Lvl_DroneWeatherSystemsTest`에는 `ADroneWeatherController` 한 개와 35° 풍향 바닥 화살표가 있다. 기본 Profile은 `LightWind`이며, `WeatherSystemsTest_Controller`의 `Weather Profile`을 바꾼 뒤 Play하면 같은 맵에서 다른 값을 비교할 수 있다. 폭우 Profile을 선택해도 아직 빗줄기가 보이지 않는 것이 현재 정상이다.

## 자연스러운 바람 전환·표시 구현 결과

기존 Debug Visualizer는 `BaseBeadLocation + 현재 풍향 × 누적 이동거리`를 매 Frame 다시 계산해 풍향 변경 시 과거 이동거리 전체를 새 방향으로 재투영했다. `WTH-02B`에서 이를 제거했다.

구현된 계약은 다음과 같다.

1. `GustAttackSeconds`, `GustReleaseSeconds`, `DirectionResponseSeconds`는 Weather Data Asset에서 각각 조정한다.
2. 풍향 Yaw 편차는 `FindDeltaAngleDegrees`를 사용해 최단각으로 수렴한다.
3. Visualizer는 표시 전용 `DisplayedWindVelocity`를 매 Frame 지수 보간하고 `Offset += LocalVelocity × DeltaSeconds × PlaybackScale`로 이동을 누적한다.
4. 풍향이 X에서 Y로 바뀌어도 이전 X 이동을 보존한 채 Y 이동이 이어진다. 고정 풍속 적분은 Frame Step에 관계없이 같은 결과가 나도록 자동화했다.
5. Sphere Bead는 보간된 Local Wind 방향으로 회전하고 풍속에 따라 길어지는 유선형 표시가 된다. 응답 시간·기준 풍속·최소/최대 길이·단면 배율은 BP/배치 인스턴스에서 조정한다.
6. `Drone.Weather` 자동화 3/3이 통과했다. 35° 바닥 화살표와 실제 Drift 일치, Clear/RainStorm 전환의 화면 무점프 체감은 수동 확인이 남았다.

이 작업은 TestMap 표현과 Snapshot 품질 개선이며 Niagara 비 구현과 분리한다. Bead 방식이 안정된 뒤 같은 `DisplayedWindVelocity`를 Camera-follow Niagara의 User Parameter로 전달한다.

## 비 최적화 방안

### 1. 카메라 주변 한 시스템만 사용

- Local Player Camera를 따라가는 작은 Cylinder/Frustum 범위에 비를 생성한다.
- 맵 전체를 덮는 거대한 비 System이나 구역마다 중복된 비 System을 배치하지 않는다.
- Local Player 1명당 활성 비 System 1개를 기본 계약으로 한다.

### 2. GPU Sprite와 고정 Bounds

- 빗줄기는 GPU Simulation Sprite를 우선한다.
- 카메라 주변의 보수적인 Fixed Bounds를 설정한다. Bounds 계산 비용과 잘못된 Frustum Culling을 함께 점검한다.
- 투명 Particle Sorting은 화면상 필요할 때만 켠다.

### 3. 빗방울별 충돌 금지

- 모든 빗방울에 Scene Query/CPU Collision을 붙이지 않는다.
- High 품질의 카메라 근처 일부만 Depth Buffer Collision 후보로 둔다.
- 바닥 Splash는 빗방울 Event를 그대로 폭증시키지 않고, 하나의 재사용 Emitter 또는 낮은 빈도의 소수 Trace 결과로 생성한다.
- Niagara Event 대신 Particle Attribute Reader나 공유 Parameter로 해결 가능한지 먼저 검토한다.

### 4. 젖음과 실내 판정 분리

- 지면 젖음은 `Material Parameter Collection`의 전역 `Wetness` 값으로 처리하고 빗방울마다 Decal을 만들지 않는다.
- 꼭 필요한 웅덩이/타이어 자국만 제한된 Decal/Render Target 후보로 둔다.
- 실내 여부는 Camera 기준 위쪽 Trace 또는 Weather Volume을 4~10Hz로 갱신하고 `IndoorRainAttenuation01`을 부드럽게 보간한다.
- 지붕 아래로 들어갈 때 System을 매번 생성/파괴하지 않고 Spawn Rate·Audio·Splash만 낮춘다.

### 5. Niagara Effect Type과 품질 단계

`Niagara Effect Type`에 Distance/Visibility/Instance Count Culling과 Global Budget Scaling을 설정한다. Epic 공식 문서는 System Instance 수를 줄이고, Effect Type의 품질·거리·Instance 수·예산 기반 Scalability로 Spawn과 Emitter를 줄이는 방식을 권장한다. [UE 5.8 Niagara Scalability와 모범 사례](https://dev.epicgames.com/documentation/en-us/unreal-engine/scalability-and-best-practices-for-niagara), [Effect Type Performance Budgeting](https://dev.epicgames.com/documentation/en-us/unreal-engine/performance-budgeting-using-effect-types-in-niagara-for-unreal-engine)

| 품질 | 빗줄기 | Splash | Screen Droplet | 원거리 Mist |
|---|---:|---:|---:|---:|
| Low | 낮음 | 끔 | 끔/저해상도 | Post Process만 |
| Medium | 중간 | 희박 | 낮음 | 단순 Fog |
| High | 높음 | 근거리 | 중간 | Fog + 색감 |
| Epic | 높음 | 근거리 추가 | 높음 | 선택형 고품질 |

정확한 Spawn 수는 화면 해상도와 Target PC 측정 뒤 정한다. 표는 기능 단계이며 숫자를 최종값처럼 고정하지 않는다.

### 6. 측정과 합격 기준

- 도구: `stat Niagara`, Niagara Debugger, `stat GPU`, GPU Visualizer, `stat Unit`.
- 비교 장면: 맑음 / 약한 비 / 폭우, FPV 정지 / 27m/s 직선 / 빠른 Roll, 실외→실내 전환.
- 확인 항목: Game Thread, GPU Niagara, Translucency, Overdraw, 활성 System/Emitter/Particle 수, Frame Time Spike.
- 1차 PC 목표로 비 전체 GPU 비용 `1.0ms 이하`를 제안하되 아직 확정 예산은 아니다. 팀 Target PC와 해상도를 정한 뒤 확정한다.
- Low에서 Gameplay 바람은 유지하고 비 시각 효과만 줄어야 한다.

## 단계별 구현 카드

1. `WTH-01` — 완료: `UDroneWeatherProfile`, Snapshot, World Subsystem, Validation 자동화
2. `WTH-02` — 완료: 결정적 지속풍·돌풍 Timer, Drone별 응답 Component, Profile 3종
3. `WTH-02B` — 완료: 돌풍 Attack/Release·풍향 최단각 보간, Debug Bead 표시 속도 벡터 적분과 방향/길이 보간, 자동화 3/3
4. `WTH-03` — 후속: Camera-follow Niagara Rain, MPC Wetness, Audio Layer
5. `WTH-04` — 대기: 실내 감쇠 Trace/Volume, 근거리 Splash Service
6. `WTH-05` — 일부 완료: 전용 TestMap·저장 계약 자동화 완료, Low~Epic Scalability와 GPU Profile은 비 표현 뒤 진행
7. `WTH-06` — 대기: Mission Definition이 Weather Profile을 선택하고 필요할 때만 Weather Event를 목표 규칙에 연결

## 사용자가 확인할 첫 체감 항목

1. `Lvl_DroneWeatherSystemsTest`에서 Rate/Acro FPV로 바닥 화살표 기준 순풍·역풍·횡풍을 각각 비행한다.
2. 쉬운 조작의 보정과 Rate/Acro의 보정 없음이 구분되는지 확인한다.
3. 돌풍이 입력을 빼앗는 느낌이 아니라 예측 가능한 외력으로 느껴지는지 확인한다.
4. 폭우에서 표적을 찾을 수는 있으나 시야 난도가 올라가는지 확인한다.
5. 실내 진입 때 비·Splash·Audio가 튀지 않고 0.2~1초 사이에 자연스럽게 줄어드는지 확인한다.
6. Low~Epic 전환 시 Mission 판정과 바람 Gameplay가 달라지지 않는지 확인한다.
