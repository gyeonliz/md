# 비행 물리 · OilRig 비 · UI · 독립 미션 점검

기준일: 2026-10-01 이전 D PC 작성 당시 기록(이후 UI·Settings는 9f67706/5b03ad3로 커밋). 현재 C PC의 상태와 수동 순서는 [테스트 맵 가이드](DRONE_TEST_MAP_GUIDE.md)를 우선한다. 지급 PNG·Content·Figma 원본은 보존한다.

## 1. 현실과 비슷한 물리인가?

기동 자체는 가능하다. FPV Rate/Acro에서는 자세 제한·자동 수평 복귀 없이 Local Body Rate를 누적하므로 롤/루프/급선회가 가능하고, 기체 Up 방향 추력·중력으로 기울임 가속과 무추력 하강을 표현한다. 이는 코드가 해당 조작과 움직임을 지원한다는 뜻이며 실기체의 선회 반경·응답·실속/프로펠러 공력까지 같다는 검증은 아니다. Easy/제한 자세 모드는 같은 곡예비행 모드가 아니다. 이번 뒤로가기 작업에서는 비행 수치를 변경하지 않았다.

결론: **Acro는 일부 현실 요소를 반영한 게임용 근사 모델이다. 실기체 성능을 검증한 물리 시뮬레이터는 아니다.** Easy/Manual을 같은 수준의 현실 물리라고 부르면 안 된다. 이번에는 비행 모델을 통째로 바꾸지 않고 평가했다.

| 요소 | 현재 구현 | 정확성의 한계 |
|---|---|---|
| 병진 이동 | Acro에서 기체 Up 방향 추력, 중력, kg 질량, 뉴턴 추력 → cm/s² 가속도 | `UFloatingPawnMovement` 속도에 직접 적용. 전체 속도·수직 속도 상한은 게임 규칙 |
| 모터 반응 | 합산 추력의 1차 응답 지연 | 모터 4개별 RPM/출력·Mixer·토크가 없음 |
| 회전 | 스틱 → Body Rate, 응답 보간 → Local Rotation | 관성 텐서·각운동량·자이로 효과·PID/센서 모델이 없음 |
| 항력 | 속도 비례 및 속도 제곱 항력 | 기체별 Cd·전면적·공기밀도로 교정한 모델이 아님 |
| 적재 | 화물 질량을 총질량에 더하고 추력 여유/성능에 반영 | 무게중심 이동/관성 변화는 미반영 |
| 바람 | 보상 비율과 응답 시간 후 별도 `AddActorWorldOffset` | 상대풍을 힘으로 계산하지 않아 속도계·관성·에너지와 완전히 일치하지 않음 |
| Easy/Manual | 이동 입력·기울기·자동 보조 | 실기체 제어기/힘 기반 운동으로 동일시하면 안 됨 |
| 프레임률 | 응답 보간은 dt 사용, 물리 적분은 프레임당 수행 | 고정 시간 간격/전체 운동 substep 및 30/60/120 FPS 궤적 검증이 필요 |

근거 코드: `DronePrototypePawn::UpdateControlAttitude / UpdateAcroFlightPhysics / LimitAcroVerticalSpeed`, `DroneWeatherResponseComponent::TickComponent`.

실제 FPV DA 점검값: 기본 MaxSpeed **4,500cm/s**, 무적재 배율 **1.25** → 이동 상한 **5,625cm/s(56.25m/s)**, 기본 Acro. 해당 FPV BP의 Definition Override는 꺼져 있다. 이는 설정값/게임 속도 상한이며 실제 기체가 그 속도로 비행한다는 검증이 아니다. 과거 27m/s 고정 기대 테스트는 현재 DA 기준값을 검증하도록 수정했으며 기체 튜닝값은 바꾸지 않았다. 옛 `ConfigureDroneFPVAcroProfile.py / BuildDroneFlightProfileAssets.py`는 27m/s 초기 참조값을 재설정하므로 현재 수동 튜닝을 보존하려면 무작정 재실행하지 않는다.

현실성을 올리는 순서는 (1) Acro의 이동·바람을 하나의 상대풍 힘 모델에 통합, (2) 고정 적분 단계/프레임률 비교, (3) 기체별 추력·질량·항력 교정, (4) 필요할 때만 관성·모터별 토크·Rate 제어기를 추가하는 것이다. 시험 기준은 호버 추력 ≈ mg, 입력 해제 후 관성 이동, 기울임에 따른 수평 가속/고도 감소, 적재에 따른 가속 감소, 같은 바람에서 풍상/풍하의 차이다. 실제 기체 1:1 재현 여부는 별도의 계측 데이터가 있어야 판정한다. 6DoF·공력·구동기·센서·바람을 구분하는 연구용 기준은 [RotorPy 논문](https://arxiv.org/abs/2306.04485)을 참고했다.

## 2. OilRig 비 분석

`Lvl_OilRig`은 Overview이고 실제 환경은 `Lvl_OilRigPreview`다. 둘을 혼동하지 않는다.

| 맵 | Actor | Static Mesh Component | Niagara Component |
|---|---:|---:|---:|
| OilRig Overview | 389 | 395 | 0 |
| OilRig Preview | 13,144 | 12,710 | 25 |

Preview 원본 비는 `NS_sky_Rain` 6개, `NS_Rain_Fast` 14개, `NS_Rain_Slow` 5개다. 컴포넌트는 Auto Activate 켜짐, 그림자 꺼짐, Max Draw Distance 0이며 세 시스템 모두 Effect Type이 미지정이다. **Editor에서 Active=false인 것은 게임에서 비가 꺼져 있다는 뜻이 아니다.** 런타임 활성화와 별도로 확인한다. 수치만으로 전체 25개가 매 순간 동일 비용을 쓰거나 비가 모든 렉의 원인이라고 단정하지 않는다.

실제 런타임 구조도 확인했다. 세 시스템 모두 `Rain / Drops` Emitter 2개이며 각각 **CPU Sim, World Space**, Renderer 1개다. System Fixed Bounds는 꺼져 있고 Effect Type은 None이다. 원본 전체 모드는 25개 활성화·총 50개 Emitter 구성이다. Dynamic Bounds와 CPU 시뮬레이션을 무조건 나쁘다고 보지는 않지만 현재 전체 동시 배치에는 비용이 크다.

원본 비, 바닥 젖음, 물 재질과 오션은 서로 다른 비용이다. 비를 꺼도 오션·젖은 표면의 셰이딩과 1만 개 이상 메시 장면은 남는다. GPU 시뮬레이션으로 바꿔도 System/Emitter CPU 비용은 남으므로 무조건 GPU 전환이 정답은 아니다. Effect Type, 거리/가시성 culling, 시스템/Emitter 개수, 투명 overdraw와 동적 Bounds를 함께 보아야 한다. [Epic Niagara 최적화 기준](https://dev.epicgames.com/documentation/en-us/unreal-engine/scalability-and-best-practices-for-niagara)

원본 맵·ThirdParty 효과는 유지했다. 비교 맵은 `/Game/Drone/Maps/TestMap/Lvl_OilRigRainComparisonTest`다. 비교 맵 복제 과정에서 생긴 원본 재저장분은 작업 시작 전과 동일한 LFS 원본 바이트로 복구했고 원본 diff가 없는지 검사한다.

### 프로젝트 비 개선

- 비 끄기/맑은 날: 빗줄기 Transform과 천장 열 추적을 건너뛴다.
- 최초 활성화/실내 전환: 112~512개를 한 프레임에 전부 추적하지 않는다. `Ceiling Trace Budget Per Frame`을 계속 지킨다.
- 아직 검사하지 않은 열은 일단 숨겨 차폐를 확인하기 전 지붕 아래로 비가 보이지 않게 한다. 기본 112개/8개 예산은 최대 약 14프레임에 걸쳐 회복한다.
- 개별 `UpdateInstanceTransform` 반복을 `BatchUpdateInstancesTransforms` 한 번으로 묶었다.
- 복잡한 지붕 감지를 유지했다. 예산은 **열 수**이며 Visibility 실패 시 WorldStatic/Dynamic fallback 때문에 열당 최대 두 Line Trace다. 카메라 실내 검사도 별도로 약 0.2초마다 한다.
- 카메라 주변 Plane ISM 비는 Niagara 원본을 대체할 수 있는 저비용 후보다. 원본 물방울/splash와 같은 화질이라고 보장하지 않는다. 빗소리·화면 물방울 등 Profile 필드가 있다고 실제 표현이 모두 구현된 것은 아니다.

### 실제 성능 비교 방법

1. `Lvl_OilRigRainComparisonTest`를 열고 Play한다. 고정 카메라와 `ADroneRainPerformanceProbe`가 들어 있다.
2. `R`로 **원본 전체(1) → 비 끔(0) → 근거리 원본 제한(2) → 프로젝트 카메라 비(3)**를 순환한다. 원본 비와 프로젝트 비는 중복 재생하지 않는다.
3. 콘솔에서 `stat unit`, `stat gpu`, `stat niagara`를 켠다. 같은 위치·해상도·화질로 비교한다. 창 포커스, VSync/FPS 제한, 최초 셰이더 컴파일과 다른 실행 중 게임도 확인한다.
4. `Maximum Nearby Original Systems=8`, 거리 기본 70m는 **비교 실험값**이다. 카메라가 이동하는 완성형 환경 매니저/원본 동등 외형 검증이 아니다. 실제 드론 비행용으로 채택하려면 카메라 추종/주기적 culling과 경계 가시성을 추가로 검증한다.
5. `-DroneRainBenchmark`로 실행하면 10초 안정화+10초 수집 × 8단계(정순/역순 반복) 후 종료한다. 결과는 `Saved/Automation/GameReadiness/oilrig_rain_frame_times.csv`다. `mean/median/p95`는 실제 Tick 간격이며 CPU/GPU 개별 시간은 아니다.
6. 더 정확한 원인 분리는 패키징한 Development 빌드의 Unreal Insights CPU/GPU Trace와 Niagara 타이머를 쓴다. `-StatNamedEvents`는 상세 원인 찾기에만 쓰고 대표 측정은 오버헤드 없이 다시 수행한다. [Epic 측정 가이드](https://dev.epicgames.com/documentation/unreal-engine/measuring-performance-in-niagara?lang=en-US)

### 개선 우선순위

1. 동시 비 시스템/Emitter와 화면 밖 업데이트 제한, Effect Type 품질 예산 지정.
2. 카메라 주변 비와 국소 splash 분리, 필요 없는 원거리 비/splash 제거. 실제 비행 속도에서 culling 경계 확인.
3. 투명 재질의 면적·겹침·정렬·씬 깊이/충돌 노드 비용 확인. 적절한 Fixed Bounds는 실제 범위를 측정하고 설정하며 작은 기본 상자를 강제로 켜지 않는다.
4. 비를 끈 상태도 느리면 메시/머티리얼 슬롯·Tick·조명/그림자·오션·PostProcess를 먼저 조사한다. 반복 메시는 ISM/HISM 후보이나 충돌/재질/LOD 요구를 검증한 뒤 프로젝트 소유 사본에 적용한다.
5. 실내 판정은 간단한 Rain Occlusion Volume으로 대체할 수 있다. 단, 원본 천장의 차폐 테스트를 유지한 채 검증한다.

### 비 품질 설정과 조정

날씨 매니저를 유지하고 원본 팩의 젖음·물결 머티리얼과 소리를 프로젝트 자산으로 연결한다. 원본 Niagara는 맵 전체 배치 대신 **낮음·중간·높음 모두 카메라 주변 1개**를 사용한다. 원본 ThirdParty와 원본 맵은 수정하지 않는다. 검증·실측은 [10/07 C PC Claude 작업 이력](../history/DRONE_WORKLOG.md#2026-10-07--비-연출-도입비-품질-옵션-c-pc-claude)을 따른다.

설정 화면 성능 항목의 `비 품질`은 자동·끔·낮음·중간·높음이며 기존 설정 SaveGame에 저장·복원한다. 자동은 엔진 효과 품질을 따른다(0→낮음, 1→중간, 2 이상→높음). 단계별 값은 `BP_DroneRainVisual`의 `QualityLevels`에서 조정한다. 아래는 현재 값이며 최종 튜닝값은 현재 미정이다.

| 단계 | 현재 동작 |
|---|---|
| 끔 | 비 연출 전부 끔 |
| 낮음 | Niagara1개·입자0.3배·생성 범위0.7배·물결0·Simple 젖음·빗소리 |
| 중간 | Niagara1개·입자0.6배·생성 범위0.85배·물결0.5 |
| 높음 | Niagara1개·입자1.0배·생성 범위1.0배·물결1.0 |

판 빗줄기는 전 단계 기본0(사용 안 함)이다. 예전 단일 사본 `NS_DroneRain_NearCamera`·`NET_DroneRain`은 삭제됐다. 원본 Niagara에는 지붕 차폐가 없어 실내에서는 끈다. 빗소리는 실내에서 35%로 줄인다. 카메라 비 오프셋 600cm는 시험값이며 전 단계 입자 크기·모양(픽셀 여부)·위치·양은 수동 확인 대기다.

프로젝트 소유 자산은 `/Game/Drone/Weather` 아래에 있다.

| 자산 | 역할·현재 조정 |
|---|---|
| `Niagara/NS_DroneRain_Low/Medium/High` | 단계별 `NS_Rain_Fast` 사본 |
| `Niagara/NET_DroneRain_Low/Medium/High` | Effect Type: 입자0.3/0.6/1.0배·효과 품질 낮으면 추가 감소·최대2개(실제 사용1개와 구분) |
| `Audio/SCON_DroneRain` | 빗소리 동시 재생1개 |
| `Materials/MPC_DroneWeather` | `RainWetness`, `RainDetail` |
| `Materials/M_DroneWetSurface` | 원본 `MF_Wetness`·`MF_WaterRipples` 사용. Detail/Simple 인스턴스, 끔·낮음은 맵 표면을 Simple로 교체 |

생성 도구는 `Tools/AssetMigration/BuildDroneRainQualityAssets.py`다. 문서 확인을 위해 재실행하지 않는다. `Lvl_DroneWeatherSystemsTest` 바닥에 젖음 머티리얼이 적용돼 있다. 비 프리셋으로 젖음·물결 외형을 확인한다. 빗소리는 원본 `SC_Ambience`(`SW_Ambience`, 230초 반복)를 사용하지만 실제 내용이 빗소리인지와 해당 음원 채택은 미확인·현재 미정이다.

수동 확인 순서: 전 단계 입자 크기·모양(픽셀 여부)·카메라 비 위치·양 → 날씨 시험 맵의 젖음·물결 → 실외/실내 음원 내용·감쇠 → 설정 비 품질의 실제 패드 조작. 화면 물방울·바닥 Splash는 미구현이다. 젖음 머티리얼은 품질 실측 장면에 없어 그 비용은 아직 측정하지 못했다.

## 3. 시작 화면과 버튼 점검

소스 6장(배경·오버레이·로고·Normal/Hover/Pressed)을 조합한다. 완성 참고이미지 자체를 클릭 배경으로 쓰지 않는다. 원본 1920×1080 오버레이 크기, 로고 734×429, 메뉴 위치/글자 크기를 시안 기준으로 보완했다. 현재는 `스토리 / 레이싱 / 튜토리얼 / 설정 / 종료` 5메뉴에서 분류로 직접 진입한다(10/04 C PC).

- 스토리: Story 4개. 레이싱: Racing 1개. 튜토리얼: Tutorial 9개(8수업+공용 Training). 설정: 음량·화면/성능·입력 표시와 적용/기본값/취소. 종료: 게임 종료 요청. 로비 Tutorial/Racing 탭·LB/RB는 유지 여부 미정.
- 후속 시안은 목록/선택 카드/설명 3열 로비, 이미지/목표 브리핑·하단 시작, 상단 상세/역할 도식·하단 가로 기체 카드다. 기존 DA·목표·맵은 보존했고 숨은 분류 미션 시작은 차단한다. 실제 Mesh Preview는 아직 아니다.
- 설정 Master 음량은 `DroneAudioSettings` SaveGame으로 저장하고 그래픽은 `GameUserSettings`를 사용한다. 미적용 음량 미리보기는 Back/Esc에서 취소하고 PIE 창/해상도는 차단한다. 개별 음악/SFX/음성 라우팅·실제 음량/재실행/창 적용은 수동 대기다. [상세 UI·설정 가이드](DRONE_TITLE_LOBBY_ORBIT_GUIDE.md)
- Hover/Pressed PNG는 연결되어 있다. 텍스트와 이미지에는 HitTest 방해가 없도록 배치한다. 제공 `Select`와 `Click` 그림이 같으면 클릭 시 별도 그림 차이는 없고 Pressed Padding으로 눌림을 표현한다.
- WBP `Button Hover Sound / Button Click Sound` 슬롯은 구현했다. 지급 음원이 없어 **기본 무음**이다. 클릭 특수 애니메이션·영상·최종 썸네일/음악까지 배정 완료라고 말하지 않는다.

이전 PC의 이전 레이아웃 화면 점검은 1280×720 Setting→돌아가기·Training/Racing 일부 클릭과 1920×1080 제목/Exit다. 이전 D PC의 10/01 후속 UI는 MSVC 14.51.36257 Build·집중 5/5(자동화 오류/경고 0)로 확인했으며 보고서는 `Saved/Automation/TrainingLobbySettings/index.json`이다. NullRHI/NoSound이므로 새 렌더 화면·음량·창 모드·저장 재실행·패드 체감은 수동 대기다. 이전 화면 확인을 새 레이아웃 Pass로 옮기지 않는다.
- `Title Background/Overlay/Logo Texture`, `Button Normal/Hovered/Pressed Texture`, DA `Thumbnail`에서 이미지를 교체한다. 런타임 교체는 `RefreshArtwork`를 호출한다.
- 기본은 C++ 생성 레이아웃이다. WBP Designer의 최종 모든 노드를 수작업 완성한 구조는 아니며 기존 BindWidget 이름/설정 API를 사용해 확장한다.
- 브리핑에 `ObjectiveRules`의 목표 순서와 제한 시간을 표시하도록 보완했다.

## 4. 미션별 독립 시험맵

### 출격 전 뒤로가기 — 2026-10-01 추가

| 현재 화면 | 버튼 / Esc / 패드 Back 처리 |
|---|---|
| 설정 | 설정만 닫고 시작 화면 유지 |
| 로비 | 시작 화면으로 복귀, Mission/Drone 선택 초기화 |
| 미션 설명 | 로비로 복귀, 미션 선택과 해당 탭 유지 |
| 드론 선택 | FrontEnd 맵의 미션 설명으로 복귀, 미션 유지·기체 선택 초기화 |

마우스 버튼과 Esc, 패드 오른쪽 Face Button(B/동그라미 계열), UE Virtual Gamepad Back이 같은 경계를 사용한다. 키 반복은 여러 단계를 연속으로 건너뛰지 않는다. 맵 로딩·비행 중·결과 화면에서는 출격 전 Back API를 거절하며 비행을 자동 중단/실패 처리하지 않는다. 결과 화면의 기존 재시도/로비 버튼은 유지한다. PIE Editor가 Esc를 게임 정지 단축키로 먼저 소비하는 설정에서는 화면 버튼 또는 Standalone 실행으로 검증한다.

BP 확장: FrontEnd WBP는 `LobbyBackButton / BriefingBackButton`, 기체 선택 WBP는 `SelectionBackButton` 이름의 Button을 두면 Native 초기화가 바인딩한다. 직접 작성한 버튼의 OnClicked에서 각 Widget의 `NavigateBack`을 호출해도 된다. 현재 프로젝트의 Native 생성 화면은 버튼이 기본 설치된다. 임의로 상태만 바꾸거나 Widget에서 OpenLevel하지 않는다. 상태 검증은 `DroneGameFlowSubsystem::RequestBackNavigation`, 실제 맵 복귀는 `DroneMissionPlayerController::BackToMissionBriefing`이 담당한다. Story Fact와 Catalog는 뒤로가기로 삭제하지 않는다.

검증: Editor Build 성공, 뒤로가기 계약 포함 **33개 실패 0**(32 Success + 1 경고 동반 성공). 경고는 `MissionEntryPIE` 중 엔진 `LogHttp`의 외부 인터넷 연결 확인 요청 3초 시간 초과이며 프로젝트 assertion 실패가 아니다. `Saved/Automation/BackNavigation/Tests/index.json`에 보존했다. computer-use로 실제 1280×720 게임의 설명 Back 클릭, 레이싱 맵→기체 선택 Back 클릭→FrontEnd 설명, Esc→레이싱 탭/선택 복원, 다시 Esc→시작 화면을 확인했다. 물리 패키징/실기체 교정 검증을 추가한 결과는 아니다.

튜토리얼 폴더: `/Game/Drone/Maps/TestMap/Tutorial`. 기존 공유 `Lvl_DroneTutorialMissionTest`는 종합 확인용으로 보존했다. 새 맵은 PlayerStart·바닥·조명과 **해당 수업의 목표만** 갖는다.

| 시험맵 | 드론 | 목표/설치 |
|---|---|---|
| `Lvl_Tutorial_Hover_Test` | Scout | Hover Zone·네 모서리 표식·3초 유지 → Return |
| `Lvl_Tutorial_Forward_Test` | Scout | 전방 Trigger/Pad 통과 → Return |
| `Lvl_Tutorial_Heading_Test` | Scout | 원형 Spline·시작+7개 체크포인트+결승 → Return |
| `Lvl_Tutorial_GateFlight_Test` | Scout | 별도 4 Gate 코스 정방향 통과 |
| `Lvl_Tutorial_FPV_Test` | FPV | 체력/피해를 받는 파괴 Target |
| `Lvl_Tutorial_Payload_Test` | Drop | 투하 Target·운반물 → Return |
| `Lvl_Tutorial_UGV_NPC_Test` | UGV | 체력 있는 NPC 표적 사격. 이 표적은 AI Auto Possess 비활성 |
| `Lvl_Tutorial_UGV_Turret_Test` | UGV | 체력 있는 고정 표적 사격. 공격하는 완성형 적 포탑은 아님 |

기존 Story 4맵은 `TestMap/Lvl_DroneStory01_GoldenTimeTest`, `02_InterceptTest`, `03_VeilBreakerTest`, `04_EndgameTest`이며 기존 목표 설치를 유지한다. 각각 물자 전달/귀환, 이동 차량 파괴, 재밍 구역 통과/귀환, UGV 표적 3개 파괴/귀환이다. 레이싱은 `Lvl_DroneRacingTest`다.

### 바로 Play하는 방법

각 독립 Tutorial 8 / Story 4 / Racing 1 맵에 `MissionTest_DefaultEntry`를 넣었다. `Default Test Mission`이 해당 DA다. 맵을 직접 Play하면 드론 선택 UI를 준비한다. 로비에서 이미 선택하고 넘어온 경우 그 선택을 덮어쓰지 않는다. 팀원 Production 맵은 변경하지 않았다.

1. 해당 맵을 연다 → Play → 드론/조작 모드 선택 → 출격.
2. 목표를 올바른 대상에 수행 → 진행/다음 목표/HUD 확인 → 성공 또는 시간 초과/파괴 실패 → 재도전 → 초기화 확인.
3. 오답 동작도 확인: 다른 Target/다른 Drone/다른 Gate 순서/역주행/목표 시작 전 발생 이벤트는 완료로 세지 않아야 한다.
4. 통합 흐름은 `Lvl_DroneFrontEnd`에서 탭·미션·브리핑·드론 선택·플레이·결과·재시도/로비 귀환으로 확인한다.

### 미션을 만드는 구조

미션마다 C++ 매니저를 복제하지 않는다. DA는 목표 순서/Event/TargetId/횟수/제한시간/드론/MissionMap, 맵은 실제 Target·Trigger·Return·Course·환경, 공통 Director는 판정/실패/평가를 담당한다. Blueprint는 `/Game/Drone/Mission/Blueprints`의 Managers/Triggers/Targets/Tutorial 기능을 재사용한다.

새 시험 미션: DA 복제 → 고유 MissionId/표시명/탭/허용 Drone → ObjectiveRules → Target Actor에 동일 Tag → Mission GameMode/PlayerStart/Test Entry → MissionMap 연결 → 로비 Catalog 등록 → 정답/오답/실패/재시도. Event 종류가 맞아도 TargetId가 다르면 완료되어서는 안 된다.

## 5. 게임적 완료와 남은 일

기능 시험맵이 있는 것은 최종 스토리 게임을 완성했다는 뜻이 아니다. 제작 맵에 같은 기능을 옮기고 목적·안내·실패 원인·동선·난이도를 튜닝해야 한다. Story 1 추가 선택 목표, Story 2 미끼/실제 목표에 따른 결과, Story 3 역할 전환, Story 4 장거리 타격 구체화는 별도 작업이다. 최종 규칙을 임의 확정하지 않는다.

출시/데모 전 확인: 튜토리얼 안내와 완료 저장, 임무 중 Pause/재시도, 결과 설명, 드론별 입력 안내/초기 카메라, 충돌·적 인지/사격 안정성, 음원·최종 UI/썸네일, Best Lap 저장/레이싱 규칙, 제작 맵 적용, 패키징 맵/Soft Reference 포함. Smart Object 순찰/소총·샷건 문제는 해당 전용 맵에서 재현해야 하며 UGV NPC 표적 시험의 성공으로 대신하지 않는다.

검증 결과와 성능 실측은 이 문서 마지막의 결과 절에 기록한다. 자동화 성공과 사람이 조작하는 전체 미션 성공은 구분한다.

## 6. 실제 검증 결과

아래는 C PC `C:\URproject\drone`의 10/01 이전 실행 기록이다. 작성 당시 이전 D PC에서는 Git/자산/도구 점검만 했고 해당 원시 보고서가 없었다. 현재 C PC에는 GameReadiness·TitleLobbyOrbit 보고서가 있으며 최신 회귀는 STATUS를 따른다.

당시 Editor Development Build 성공. 집중 회귀 **32/32 Success, 테스트 오류/경고 0**이다. 범위는 Flow/FrontEnd/Map Travel, Mission 목표·원형 코스, Prototype·Physics, Tutorial 저장 맵·Gate·기록, Weather/Rain 예산이다. 로비 진입 Hover PIE와 독립 Hover 맵 직접 Play PIE 모두 실제 출격→3초 유지→다음 목표 전환을 통과했다. 직접 진입 시 기본 카탈로그에 이미 등록된 DA를 중복 등록하던 문제도 수정했다. 이것은 모든 미션을 손으로 완주했다는 뜻이 아니다. 이후 Back 후속 회귀 33개 실패 0(HTTP 경고 동반 성공 1건)과 일부 버튼/Esc 복귀·선택 복원 기록도 있으며 전체 패드 입력·모든 미션 완주는 미확인이다.

Tutorial 8 + Story 4 + Racing 1 + 비 비교 1, **14개 시험맵 Map Check 오류/경고 0**. Title WBP Compile 성공. 보고서는 `Saved/Automation/GameReadiness/Tests/index.json`, 로그는 `Saved/Automation/GameReadinessTests.log`다. MSVC 14.51은 엔진 권장 14.50보다 새 버전이라는 빌드 도구 경고가 있지만 빌드는 성공했다.

환경 로그의 별도 주의: Editor 실행파일의 `-game`에서는 Experimental Toolset의 Python 시작 스크립트가 `ToolsetDefinition / PythonTestRunner`를 찾지 못하는 오류가 나온다. Editor 전용 API가 게임 실행 컨텍스트에 없는 문제로 보이며, 로비 실행/위 테스트 성공과 구분한다. 전체 로그까지 오류 0이라고 표현하지 않는다. 엔진 파일이나 기존 MCP 플러그인을 임의 수정하지 않았으며 정식 패키징 실행에서도 발생하는지 후속 확인한다.

성능 실측 환경: 당시 측정 PC의 **UE 5.8.2**, RTX 3080, Editor 실행파일의 `-game` Development, 1280×720·고정 카메라·VSync/FPS 제한 해제. 이전 D PC의 사양/성능 측정으로 해석하지 않는다. 당시 다른 실행 중 앱은 강제로 종료하지 않았다. 각 모드는 10초 안정화+10초 표본, 정순/역순 2회이며 올바른 카메라 방향으로 재측정한 기록이다.

| 모드 | 평균 프레임(ms), 2회 | p95(ms), 2회 | 평균 간격에서 환산한 FPS |
|---|---|---|---:|
| 원본 25개 | 20.552 / 20.558 | 24.195 / 24.805 | 약 49 |
| 원본/프로젝트 비 끔 | 9.630 / 9.707 | 10.586 / 10.711 | 약 103 |
| 가까운 원본 최대 8개 | 10.670 / 10.637 | 13.069 / 12.568 | 약 94 |
| 프로젝트 카메라 주변 비 | 9.665 / 9.636 | 10.669 / 10.547 | 약 104 |

이 **통제된 한 시점**에서는 원본 비가 주요 추가 비용이었다. 원본 대비 근거리 제한은 평균 프레임 비용 약 48%, 프로젝트 비는 약 53% 낮았다. 이는 원본 동등 화질/모든 비행 위치/패키징 결과를 보장하는 수치가 아니다. 비를 껐을 때도 장면의 렌더링 비용이 남는다. 수집 CSV는 Tick 간격이므로 GPU/CPU 분해 결과로 표현하지 않는다. 현장 `stat unit` 관찰과 후속 Insights로 원인을 추가 분해한다.

기상 기능의 범위: Wind/Rain Snapshot·강우 강도·카메라 비·지붕 차폐·On/Off는 존재한다. 비 품질·젖음/물결 머티리얼·Audio consumer가 연결됐으며 설정·조정은 [비 품질 설정과 조정](#비-품질-설정과-조정)을 따른다. 젖음/물결 외형·음원 내용/실내 감쇠·패드는 수동 확인 대기, 화면 물방울·바닥 Splash는 미구현이다. OilRig 원본 젖은 표면/오션은 Profile과 별개이며 위 과거 On/Off 비교에서도 남겨 두었다. 날짜별 실측·자동 검증은 [WORKLOG](../history/DRONE_WORKLOG.md#2026-10-07--비-연출-도입비-품질-옵션-c-pc-claude)에 기록한다.

검증 파일: `Saved/Automation/GameReadiness/oilrig_audit.json`, `isolated_mission_maps.json`, `oilrig_rain_frame_times.csv`, `GameReadinessRainBenchmark.log`, `GameReadinessFinalize.log`. 반복 도구는 `AuditDroneGameReadiness.py / BuildDroneIsolatedMissionMaps.py / BuildDroneRainComparisonMap.py / FinalizeDroneGameReadiness.py`다. 이미 생성된 독립 맵은 재생성하지 않고 연결/필수 Actor만 검증한다. 원본 공유 맵·Production Training은 저장하지 않는다.
