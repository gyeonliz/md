# Drone 개발 진행 기록



### 최종 축 보정과 실제 새 프로세스 검증

원본 export의 RapidIterationParameterData를 해독하고 실제 particle JSON과 교차했다. Rain Box=(500,5,5), Lifetime=2초, Velocity Min=(0,200,-980)/Max=(1,400,-3000)였다. 실제 rawX 약-250..249는 생성 폭, rawY 약-2..1017은 나이별 이동이었다. Y-age 상관0.625/Y-Z 상관-0.542를 확인했으며 Y 범위를 생성 폭으로 보고 -1650cm만 옮긴 중간 가설은 틀렸다. 이 실패/진단은 위 기록으로 보존한다.

최종은 카메라 quaternion × simulation basis(Yaw=-90°), 위치는 카메라 quaternion × Offset(1150,0,600)으로 분리했다. 원본 X→화면 가로(-Y), 원본 Y 이동→카메라 전방(+X), 원본 Z→화면 세로다. BP에 CameraRainLayerRotationOffset을 노출했다. 비기본 camera/basis의 pitch/yaw/roll과 위치 offset을 섞어도 합성 순서가 유지되는 회귀를 추가했다. 원본 Niagara 그래프/velocity·프로젝트 mask/density는 이 보정에서 변경하지 않았다.

| 마지막 검사 | 실제 결과 | Saved 기준 근거 |
|---|---|---|
| DroneEditor Win64 Development Build | Succeeded·26.40초, MSVC14.51.36257·기존 경고 유지 | Logs/Build_20261014_GateRainCity_Final3.log |
| 실제 D3D12 RHI 집중 자동화 | **21 Success / 0 SuccessWithWarnings / 0 Fail / 0 NotRun**, 46.5602초 | Automation/GateRainCity/Final3Report/index.json·final3_render.log |
| 실제 생성기·시드194849 도시/비 | 9 PNG 모두1274×716, 정면/90°이동/75°상향 이동에서 가로3·세로3뿐 아니라 실제9칸 전부 입자 존재, Off/Disable/Clear0 | Automation/CityAppearance/S194849/gate_rain_city_final/Capture_6F09F85349AAB75E6F2A4395B5FE79A7/ |
| 별도3품질·카메라 캡처 | 낮음/중간/높음 × 정면/90°/75° + Off=10 PNG | Automation/RainCameraPresentation/gate_rain_city_final/Capture_46B32C8A4547D1300D9C628F740FBC1E/ |
| Palette 재실행 | 성공·추가 재질 생성0·Type51 유지. BP/TestMap만 저장, m_green 재저장0·복제 parent/class/HISM guard 통과 | Automation/GateRainCity/city_reapply_verified.log·CityAppearance/20261014T062349_880961Z/report.json |
| 원본/팀원 보존 | Island 재로드 SHA 불변/저장0, Production Training/FC/MOUT/ThirdParty pack 경로 Git diff0 | IslandGateSize/report.json·최종 경로별 Git 확인 |

최종21개는 Diagnostics 실제도시/별도Rain캡처2개, Procedural Appearance5개, Tutorial Course/Gate6개, Weather5개, UI Font/선택명2개, Settings1개다. 엔진 startup/PSO·VSM/드라이버 경고까지0이라는 뜻은 아니다. 전체 Drone.*·패키징·실제 패드·실내 복귀/FPS·모든 시드/완주/기록 검증도 아니다. 기존 CourseManyGates 경고100을 수정 완료로 바꾸거나 전체 회귀에 포함하지 않았다.

최종 실제 도시 Rain frustum 입자수는 정면377/90°이동383/75°상향388이다. 각9칸 최소8/14/12개로 한쪽 빈 화면 문제를 재현한 동일 검사가 통과했다. root가 최종3뷰 PNG를 직접 열어 화면 좌우 분포/얇은 빗줄기를 확인했고, 앞선 도로·닫힌 컨테이너·콘크리트 골조·중복 없는 완성 창고도 확인했다. 이는 사용자 플레이 체감 Pass가 아니다. 원본 Rain/Island/Production 맵을 덮는 생성 도구는 실행하지 않았다.

### 문서·Space와 인계

기존 STATUS/WORKBOARD/CONTEXT·비/저작/시험 가이드를 갱신했고 새 주제 MD는 만들지 않았다. STATUS 크기 확보는 이전 Acro 회의·코스 표시선 상세 원문만 기존 STATUS_2026-10.md로 이동했다. 원문 이동 당시 STATUS29,829B/126줄→26,167B/113줄, 아카이브56,297B/206줄→60,489B/228줄이었다. 이동 raw CRLF 텍스트 SHA256=6658E3B4010F6A25B784208A91798D6C2C1FA9A1308BD66B907FE8936704E033, 이전 아카이브 prefix를 보존했고 기존 색인 링크를 사용했다. 최종 현재 상태 갱신 뒤 크기는 아래 마감 확인을 따른다.

Drone Space 기존 진행상황 Sequence40(3블록)·BP가이드26(2블록)·시험가이드27(2블록) 총7연산을 적용했다. 각 블록을 같은 content stream에서 다시 읽어 기대 Markdown과 전부 정확히 일치함을 확인했다. 기획3·지침9·루트는 변경하지 않았으며 새 Page·공유 권한 변경·예약은 없다. 사람의 기존 기획/보드 링크·이전 검증 출처를 보존하고 현재 수정·자동 검사/수동 대기를 구분했다. GitHub MD 링크는 사용자 Commit/Push 뒤에야 새 본문이 반영된다.

다음 실기: 새 Editor에서 Island Gate 폭/방향·3상태색, Lvl_ProceduralCityRaceTest 또는 로비 랜덤 레이싱 시드194849의 콘크리트·도로/차선·컨테이너 지지·지붕 중복 없음과 Rain3품질/회전/이동/실내/실외/Off를 확인한다. 팀원 Gate 저장 재시험·InterLink/8수업/완주/기록·Observer/물리/재밍 체감·Patriot는 기존 후속이다. Commit/Push는 사용자가 한다.

마감 확인: 변경 Python9개 UTF-8 AST 구문 검사 통과·플레이어 UI 기본 폰트 감사 위반0, Unreal diff --check 오류0(일부 CRLF 알림). MD는 이동 원문의 CRLF 보존 때문에 git -c core.whitespace=cr-at-eol diff --check로 확인하며 오류0이다. STATUS27,028B·WORKBOARD29,610B로30,000B 이하, 기존 STATUS 아카이브60,489B 보존. Unreal63개·MD12개 상태 항목은 앞선 변경을 포함한 의도된 미커밋 목록이다. Editor/Commandlet/Build 프로세스0, HEAD/로컬 origin은 그대로다. 처음 AST stdin 검사는 Windows 기본 인코딩 때문에 중단됐고 UTF-8 명시 후9개 모두 통과했으며 소스 구문 결함은 아니었다. 사용자 수동 Pass·Commit/Push는 실행/추정하지 않았다.
기준일: 2026-10-04 (Asia/Seoul)

기존 날짜별 기록의 배열은 보존하고 새 기록은 끝에 날짜순으로 추가한다. 현재 상태는 [STATUS](../../STATUS.md)를 따른다.

## 2026-10-01 후속 — C 드라이브 PC 현황 최신화와 다음 작업 정리

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-01 후속 — 로비 목록 튐 진단(실제 UI 미수정)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-01 후속 — UI 기획안·훈련 분리·설정 추가

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-01 Spaces 연동과 Trello 대조

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-01 작업컴 최신화 — 원격 수신·검증 출처 정리

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-01 후속 — 출격 전 뒤로가기

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-01 후속 — 물리/비/UI/독립 미션 점검

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

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

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-01 — 원격 기준선과 작업컴 인계 최신화

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

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

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-01 저녁 후속 — 협업 체계·다른 PC 세팅·낡은 규칙 정리·Space 재시도

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-01 19시 이후 후속 — 로비 후속 검증 완료·사용자 규칙 설치

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-01 밤 — Shotgun 시험 정정·미션 Catalog 자동 등록

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-01 밤 후속 — UI-PAD-01·MISSION-CHECKPOINT-01 문서 반영

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-02 새벽 — NPC 테스트·허브 브리핑·HUD 배터리·Best Lap·패키징 설정

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-02 새벽 후속 — TUT-PROGRESS-01·스토리 순서 연결

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-03 — 회의 후 UI/DA 점검과 문서 정합성 (Codex)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-03 C PC 추가 UI 준비·진단 — 핵심 연결 대기

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-03 밤 — 5메뉴·조종 입력 표시·레이싱 숫자키 연결 완료

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-03 밤 후속 — 5메뉴·조종 입력 표시 Space 반영 마무리 (Codex)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-04 STATUS 정리 — 10월 세션·기존 요약 원문 보존 (Codex)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-04 새벽 — Acro 회의 조사·입력/자세 수정·포커스 관찰 반영

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-04 후속 — Production Course 표시선 상한 읽기 조사

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-03 UI 준비·진단 원문 보존 — 10/04 이관

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-03 C PC 추가 UI 준비·진단 — 핵심 연결 대기

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-03 C PC 추가 UI 준비·진단 — 핵심 연결 대기

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-04 감사1차 수정·코스/Acro 후속 반영 — C PC

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-04 최신 Acro 입력·데드존·응답 조정 (C PC)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-03 밤 최신 Blueprint 조정 — 5메뉴·조종 입력 표시·레이싱 키

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

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

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

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

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-04 오후 감사2차·면접 대비 정리 — C PC, Codex docs

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-04 Shotgun 판정 정정 — C PC, Claude 실행·Codex docs 반영

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-04 NPC 걷기 미재생 수정 — C PC, Claude 실행·Codex docs 반영

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-04 NPC 소총 IK Retarget·총 오른손 부착 후속 — C PC, Claude 실행·Codex docs 반영

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-05 사용자 결정 D-7·D-9·D-10·D-15 — C PC, Codex 문서 반영

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-05 사용자 결정 2차 — C PC, Codex 문서 반영

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-05 D-5·D-6·D-11·D-12(1차)·D-14 반영 — C PC, Claude 작업·검증·Codex 문서

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-05 NPC 다리·높이 제한 매니저·매니저 폴더 정리 — C PC, Claude 작업·검증·Codex 문서

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-06 D-5 랩 타이머·D-12 Flight 이름 변경/분리·CLAUDE.md MCP 반영 — C PC, Claude 작업·검증·Codex 문서

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-06 D PC 동기화·WORKBOARD 7그룹 정리·10/02 Editor 시작 지연 진단 재반영 — D PC, 문서 반영 Claude

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-06 D PC Codex 최신화·동시 Pull 잠금 재확인

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-06 D PC — 조작 버튼·Drop 집게 수정 인계 (Codex 읽기 전용 진단)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-06 D PC — 조작 UI·Drop 파지 예외 수정/검증 (12:17 KST)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-07 InterLink DX 조종기 입력과 메뉴 연결 — D PC Claude

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-07 InterLink DX 버튼·ArmSwitch·노브 전용 메뉴 이동 — D PC Claude

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-07 — 비 연출 도입·비 품질 옵션 (C PC Claude)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-07 — 비 품질 정정·원본 Niagara 기반 (C PC Claude)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-13 D PC — MD 최신화·Pull 완료 후 수신 코드 대조 (Codex)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-14 — 수신 기준·Gate/Patriot 검증 경계 최신화 (D PC Codex)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-14 — 후속: 고정 조종자 첫 수업·미션 박스 치환·실제 그물/공통 접촉 요구

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-14 — 후속: Story 표시명 확정·박스 후보 맵 조사 범위

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-14 — 사용자 승인 직접 구현·미션 치환·Pretendard UI·Gate 저장 수리 (D PC Codex)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-14 — 랜덤 레이싱 비 정면/픽셀 수정·플레이어 UI 공통 Pretendard

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-14 — Island Gate 크기·랜덤 Gate 방향·도시 외형과 Rain 볼륨 후속

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-14 — 팀원 커밋3cb9c184 수신·로컬 작업 보존

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-16 — 커밋 51bf2629·95beefa 확인, 팀원 6c07afa5 수신

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-16 — D PC 저장공간 점검·중복 백업 정리

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-16 — 오후 UI 전면 개편·WBP 전환·UGV 무장

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 변경 사실
1. WBP 전환·정리: 코드로만 그리던 위젯을 WBP로 내보내는 Editor 도구(`Source/Drone/UI/Tools/DroneWidgetBlueprintExport`, 자동화 `Drone.Tools.ExportWidgetBlueprints`)와 확인 테스트(`Drone.UI.NativeWidgetBlueprintAssets`). 모든 WBP를 `/Game/Drone/UI/WBP/{FrontEnd,Mission,HUD}`로 이동(AssetTools, `Tools/AssetMigration/OrganizeDroneWidgetBlueprints.py`). 이동 때 참조 고침 누락 3건(FrontEnd→설정·시드, FlightHUD→입력 표시, FrontEndRoot TitleMenuClass)을 `FixMovedWidgetReferences.py`·`WireDroneWidgetBlueprints.py`로 복구.
   - WBP 목록: FrontEnd(WBP_DroneFrontEndRoot, WBP_DroneFrontEnd, WBP_DroneFiveItemMenu, WBP_DroneSettings, WBP_DroneSeedInput, WBP_DroneControlsGuide), Mission(WBP_DroneSelection, WBP_DroneMissionObjective, WBP_DroneMissionResult, WBP_DroneMissionPause, WBP_DroneProceduralLoading, WBP_DroneStartCountdown, WBP_DroneMissionStartPrompt), HUD(WBP_DroneFlightHUD(구 프로토타입), WBP_DroneControlInputDisplay).
   - **아직 코드만**: 미션 맵 비행 HUD 본체(HUD Kit: 나침반·고도·속도·상태·UGV 조준선/무장), 로비 미션 카드 버튼, 로비 배치 좌표(실행 시 코드가 다시 잡음). 다음 작업 후보: HUD Kit WBP화.
2. 프론트엔드: 레이싱·훈련 로비를 캠페인과 같은 MISSION BRIEFING 형식(번호 목록·가운데 사진·오른쪽 정보 3칸, Select_UI 배경)으로 통일. 카드 클릭은 선택만, START로 확정(세 분류 공통). 카드 제목 한 줄 고정(완료 표시는 부제로). 정보 칸 높이 글에 맞게.
   - 브리핑 화면(작전 지역으로 이동) → 시안 8.webp 형식: TRAINING/RACING/MISSION BRIEFING 제목, 사진·정보 3칸, 오른쪽 CONTROLS 3탭(게임패드/키보드·마우스/드론 조종기, 장치 그림·번호·3열 범례, LB/RB 전환), START.
   - 모든 시작 버튼 글자 "START", 화살표는 받은 이미지(T_UI_StartChevrons).
3. 기체 선택 화면: 시안 6.webp 형식(큰 미리보기, DRONE 상세·능력치, 작은 ‹ 조작 모드 › 버튼, SELECTED 카드, START). 기체 이미지 4종(Figma 렌더) 연결. 특징·안내 줄 제거, 설명/능력치 칸 높이 고정.
4. 훈련 시작 안내창: 훈련 출격 직후 게임 멈춤 + 미션 이름·현재 목표·진행·역할 조작 안내·전체 목표 + [시작](A/Enter). 기본 훈련만 켬(레이싱·스토리 BP 옵션). 테스트 `Drone.Flow.MissionStartPromptPIE`.
5. 비행 HUD(시안 5.webp, 코드): 왼쪽 위 미션 패널(MISSION NN · 이름, 목표, 역할 안내, 진행 막대), 맨 위 나침반(가로 눈금 + "355°" 상자, 매 프레임 부드럽게), 타이머(남은 시간·TIME LIMIT), 오른쪽 위 기체 상태(내구도·배터리·신호·바람·조작 모드), 왼쪽 속도 상자(세로 눈금 제거), 오른쪽 고도 사다리 + 뾰족한 지시 상자 + VS(수직 속도). UGV만 조준선·무장 패널(MG 탄창·GL 잔탄·재장전). 해상도와 무관하게 맞게 그리기 좌표 수정.
6. UGV 무장: 기관총 누르고 있으면 연사, 탄창 200·재장전 2초(빈 탄창 자동, R/□ 수동), 유탄 6발 제한(연사·재장전 없음). UGV일 때만 L2 기관총·R2 유탄 IMC(`IMC_DroneGroundWeapons`, `IA_DroneGround_Reload`). Space/Ctrl은 UGV에서 포탑 위아래 조준. 테스트 `Drone.Weapons.GroundUGV.Ammo`.
7. 설정 체크박스 버그 수정: 수직 동기화·조종 입력 표시 체크박스가 켜짐/꺼짐 모두 검은 네모로 보이던 문제(체크 스타일 전경색 검정) → 흰색 고정. 타이틀·일시정지 양쪽 마우스·키보드 재현 테스트(`Drone.UI.SettingsCheckboxClickPIE`, `Drone.UI.PauseSettingsCheckboxClickPIE`, 캡처 `Saved/Automation/SettingsCheckbox/`). 설정 콤보 항목이 WBP 경로에서 비던 문제도 수정.
8. 드랍 목표: `BP_RoleTest_PayloadTarget` 외형 SM_Pallet(Battlefield 자산, 수정 안 함), 메시 크기에 맞춘 충돌 상자 자동(LandingCollision), Target Visual Mesh를 바꾸면 바로 적용.
9. 문구: 기체·미션의 "(그레이박스)·시험" 표기 제거, 역할별 기체 설명, 레이싱 기체 이름 "스카이드론"(외형 자산은 팀원 미푸시로 미연결), 기획서 기준 미션·훈련 문구(오전).
10. Codex 교차 리뷰 2회 지적 8건 모두 Claude가 코드 대조 후 수정(콤보 항목, 시드 칸, 로딩 단계 줄, 첫 수업 완료 색, 기체 카드 바인딩, 정리 스크립트 API, 시작 안내창 버튼 누락 시 멈춤, 입력 자산 쿠킹 → DefaultGame.ini DirectoriesToAlwaysCook 추가).

## 검증 출처
| 검사 | 조건 | 결과 | 보고서·로그 경로 |
|---|---|---|---|
| Build | DroneEditor Development | Succeeded(마지막 16:5x) | `Saved/Automation/ClaudeCheckbox/` |
| UI·Flow 등 회귀 | RenderOffScreen 1920×1080 | 80건 중 73 → 재실행 후 실패 1(테스트 하네스 문제) | `Saved/Automation/ClaudeUIOverhaul3`, `ClaudeUIOverhaul4` |
| 체크박스 재현 | RenderOffScreen | 2/2 Success + 캡처 | `Saved/Automation/ClaudeCheckbox/report2` |
| HUD 캡처 | 1920·1600·1280 | 정상 배치 | `Saved/Automation/HUD`, `ClaudeHUDRes` |
| 드랍·능력 | NullRHI | 3/3 | `Saved/Automation/ClaudeHUD5/report3` |

- 구현됨: 위 1~10
- 자동 검증됨: 위 표
- 수동 확인 대기: 새 로비·브리핑·기체 선택·조작 안내 실제 조작(패드·마우스), UGV 연사·재장전·유탄·Space/Ctrl 조준, 훈련 시작 안내창, 체크박스 실사용, 팔레트 투하 착지, HUD 실제 해상도별 배치
- 미구현/알려진 문제: HUD Kit WBP화 미착수, `Drone.UI.FlightHUDKitLayout` 테스트는 테스트 World에서 위젯 초기화가 돌지 않아 실패(제품 HUD는 PIE 캡처로 정상, 2회 수정 후 중단), 스카이드론 외형 미연결, 패드 포커스 PIE 4건은 미렌더 실행 시 알려진 실패(UI-FOCUS-RACE-01, 재실행 통과)

### Codex 원시 보고서 대조·인계 수치 정정/확인 대기

- ClaudeUIOverhaul3/verify_report/index.json: 성공73·경고 동반 성공2·실패5, 합계80. 실패는 Drone.Flow.GamepadMissionFlowPIE, Drone.Flow.GamepadNavigationPIE, Drone.Flow.KeyboardStoryFlowPIE, Drone.Flow.PauseMenuRacingPIE, Drone.UI.FlightHUDKitLayout.
- ClaudeUIOverhaul4/report/index.json: 성공4·경고 동반 성공1·실패2, 합계7. 실패는 Drone.UI.FlightHUDKitLayout 및 KnownIssues.Flow.LobbyLayoutStabilityPIE. 이 파일만으로 인계 “재실행 후 실패1”을 확인할 수 없다. 포커스4건 재실행 통과·하네스 원인은 Claude 인계이며 전체80건 최종 재통과로 확대하지 않는다. 최종 로그/집계와 KnownIssues 포함 여부는 Claude 재확인 필요(TEST-HUD-LAYOUT-01).
- ClaudeCheckbox/report2/index.json: 성공2·경고0·실패0(타이틀/일시정지 체크박스). ClaudeHUD5/report3/index.json: 성공3·경고0·실패0. 앞선 HUD5/report는 3성공/1실패, report2는 2/2이며 최종 report3와 합산하지 않는다.
- Build Succeeded(마지막16:5x)·HUD 1920/1600/1280 정상 배치·캡처 내용은 Claude 인계 근거다. Codex 이번 Build 재실행·이미지 전수 열람·실제 장치 수동 Pass 없음. FlightHUDKitLayout 실패는 알려진 테스트 World 위젯 초기화 문제로 인계됐고 2회 수정 후 중단 원칙을 유지한다.
- 구현됨은 위 변경1~10, 자동 검증됨은 위 출처/조건 한정. 수동 확인 대기는 새 로비/브리핑/기체 선택/CONTROLS의 패드·마우스, 훈련 시작 안내, 체크박스 실사용, UGV 연사/재장전/유탄/Space·Ctrl, 팔레트 투하 착지, HUD 실제 해상도 배치다. 미구현은 HUD Kit WBP화·스카이드론 외형 연결이다.
- WORKBOARD 기존 관련 카드를 갱신하고 UI-WBP-EXPORT-01(구현·수동 대기), UI-HUD-WBP-01(미착수), UI-CONTROLS-DECISION-01(미정), ASSET-SKYDRONE-01(팀원 푸시 대기), TEST-HUD-LAYOUT-01(하네스/집계 확인)을 추가했다. 완료 구현을 수동 완료 카드로 닫지 않았다.
- 아카이브 대상/기준 날짜가 지정되지 않아 절 이동·아카이브 파일 생성은 하지 않았다. 현재 관련 요약/카드만 갱신해 크기를 STATUS 27,227→28,515B, WORKBOARD 29,848→28,466B로 유지했다(모두 보수적30,000B 미만). 과거 WORKLOG 본문은 수정하지 않았다.
## 확정·미정
- 사용자가 확정한 것: 위 변경 사실 전부(시안 이미지·Figma Slide 102 기준), 유탄은 발수 제한만·기관총만 연사, 훈련·레이싱 테마를 캠페인과 통일, START 통일, 그레이박스·시험 문구 제거, 레이싱 기체 = 스카이드론.
- 현재 미정(결정 쓰지 말 것): 게임패드 드랍 집기 버튼(시안 L2, 실제 R1), 게임패드 비행 범례가 FPV 모드 2 기준인 점, 키보드 UGV 범례 번호, 스카이드론 외형 자산(팀원 푸시 대기), 훈련 목록과 구현 수업 매핑(기획서 8개 vs UGV NPC 수업), 결과 화면 [다음] 동작.

### Space 반영·최종 문서 확인

기존 페이지 3개에 편집6건을 적용했다: 진행상황과 다음 작업 sequence44(4건, 현재 Git/UI·작업판/Next), 테스트 맵과 확인 가이드 sequence29(1건, UI·무장 수동 확인/검증 경계), Blueprint 조정과 팀원 가이드 sequence27(1건, WBP·HUD·UGV/조작·팔레트). 각 결과의 affected_blocks 총27개를 같은 페이지에서 다시 읽어 저장 hash 전부 일치·선택 완전성을 확인했다. 새 페이지 생성·기획/날짜별 기존 기록 삭제·공유/예약 변경 없음. 이번 대상 Space 미반영 없음. 기존 기획/지침/루트 페이지는 변경하지 않았다.

최종 로컬 변경 대상은 STATUS.md·WORKBOARD.md·docs/history/DRONE_WORKLOG.md 3개이며 Commit/Push는 하지 않는다. 문서 검사는 Git diff --check(CRLF 허용)·크기/변경 범위 대조로 마무리하며 엔진 Build·PIE·수동 Pass를 추가하지 않는다.

## 2026-10-16 — 저녁 HUD WBP화·가이드 상자·좌표·체크박스

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-16 — 사용자 우선순위로 Drone 수신·Commit/Push

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-19 — 드론 최신화와 면접 자료 반영

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-19 후속 — Codex 직접 실행 제한 해제·레이싱 검증 대기

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-19 — 훈련 사진·시작 카메라·레이싱 전체 뷰·실제 입력 가이드·오프닝

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-19 — 차량 후방 직격·자동 자폭·NPC 래그돌·호버 표시·UI/레이싱 사진 수정

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-19 — 전체 문제 검증·코스/AI/UI/로딩 수정 (C PC Codex)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-19 C PC — 남은 맵 격리 검사·외부팩 경계 수리

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-20 — MilitaryCamp 준비 메모리·스트리밍 및 외부팩 경고 정리 (C PC Codex)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-20 — 사용자 훈련·미션·전투/UI 피드백 반영 (C PC Codex 직접)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-20 — LOS 복귀 예외 보존·귀환 안내 정리·실제 미션 검증 (C PC Codex)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-20 — 스포이드 목표 연결·배치형 나침반 매니저 (C PC Codex)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-20 — 실제 Story 배치·M2/3 분리·Nav 저장·Camp 저메모리/재밍 조정 (C PC Codex)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-20 D PC — 조작 그림·기체 사진·튜토리얼 권장창 개선

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-20 — HUD Designer 한 WBP 통합 (D PC Codex)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-20 — 전체 WBP 편집 정본·목표 매니저 배치·게이트 재질·M1 영상 (D PC Codex)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-20 — 후속 UI·Pull·배달2·사진, 사용자 중간 확인 인계

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-20 — 중간 확인 후속: 실제 M1 선택창·배달 적재·NPC Nav 마무리

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-20 — 사용자 제보 설정창 압축 수리와 검증 정정

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-21 D PC — 최신 Git 대조와 드론 선택 사진 교체 안내

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-21 D PC — Story 실패 정책과 미션 4 시작지점 3곳

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-21 D PC — 기체 선택창 3D·M3/M4 기체6종·Back 이름 정정

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-21 D PC — 재출격 기체 재선택과 M1 임시6종 허용 후속

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-21 D PC — Gate BP의 세 상태 색상 직접 편집

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-21 D PC — main 분기 병합·Push와 게이트 머터리얼 자동 우선

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-21 D PC — 출발 카운트다운 흰색

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-21 D PC — 지급 이미지5장 교체·레이싱 실제 기체 외형 수정

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-21 D PC — 레이싱 프로펠러 누락 정정

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-21 C PC — Story4 검증 계약·현재 안내 불일치 정리

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-22 C PC — Story4 후속 근거 대조·START/BACK·총괄 보고

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-22 C PC — 승인 사진3개 연결 후 검증 경계 최신화

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-22 C PC — 현실 조종감 참조 방향·공유 MD·커밋 준비

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-22 D PC — MD 최신화·작업컴 역할별 세션 분리

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-22 D PC — 검증/MD 작성권 인계·실행 전 체크리스트

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-22 — D PC 물리 조사·카메라/LOS·본미션 실행 최종 대조

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-22 D PC — 사용자 오디오·첫 경고 수리와 최종 자동 검증

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-22 D PC — 실제 미션 오디오 조립 확인과 사망 재선택 pause 결함 수리

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-22 D PC — Racer opt-in 로터 1차 구현·실행 가능한 후보와 지정 회귀

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-22 D PC — 입력 보고·매핑 범위 보류 결정과 사용자 재실행 복구 확인

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-23 D PC — Space키 시동 수정·현지 최신화

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-23 D PC — MiniMax H3 로컬 설치·T2V 테스트 (작업 도구 Claude)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-23 D PC — MiniMax H3 I2V 테스트·엔딩 영상 시안 (작업 도구 Claude)

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-23 D PC — 입력원 전환 OFF·InterLink 왼쪽 끝값·Cancel/Esc 후속

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-23 D PC — 장치별 스로틀·역할 FPV·중력/평균추력 정합

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-23 — C PC 자동 스로틀 모터 결과 교차검토·MD 최신화

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-23 D PC — 넓은 FPV·Story 단계 교대·선택 UI·파괴 전환·전방 센서

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-27 — 랜덤 도시 레이싱 개선 시안

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-27 — 키마 Space 상승 반응 수정·Ctrl 물리 하강 검증

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-27 — 키보드 쉬운/게임 Ctrl 하강·접지OFF 분리

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-27 — 공통 결과·상세 모달·랜덤 도시 화살표 및 M1 Lit 사진

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-27 D PC — 세 장치 키 설정·패드 Viewport 반전·Circle 공통 취소 마감

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-28 — 전투 투하 폭탄·기체 교대·PSD 상세창·볼륨 편집

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-28 — Drop 공중 항력·수직 하방·정문/차량·재머 피격 수선과 승인 전달

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-29 — 카메라 지형/광각 near면·전투 표적 캡슐·M1 전선·창 모드 수선과 전달

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-30 — 최신 수신·파일럿 숫자키 전용 범위/실행 미반영·현재 관성/물리식 보고

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-30 — 파일럿 전용 접촉·회전·착륙/8재시작 완료·41검사·사용자 인계

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-30 — 파일럿 비행장400×400m 확장·공간감 환경39개 배치

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-30 — 파일럿 하늘 공간감·원경 박스 건물 추가

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-30 — 파일럿 자연 착륙·접지 방향·입력 관측 보강

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-30 — 사용자 요청 저장용 로컬 커밋

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-30 D PC — 저장용 커밋 후 파일럿 물리DA·호버/하강·소화면·yaw전용 추적

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-30 D PC — 파일럿 공통 평면 판정 검증

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.

## 2026-10-30 D PC — 제출14음원·파일럿 최종 통합 확인

원문은 [10월 WORKLOG 아카이브](archive/DRONE_WORKLOG_2026-10.md)에 보존했다.


<a id="2026-11-03--10301101-코드-27커밋-문서space-대조"></a>

## 2026-11-03 — 10/30~11/01 코드 27커밋 문서·Space 대조

작업 도구: 문서/Space Codex. 코드 커밋 작성자 gyeonliz이며 실행 담당/실행 PC는 작성자만으로 추정하지 않았다. D PC의 Unreal HEAD·로컬 origin/main `5905a3cb6c5c2947bfe36f3d3ded283a7bbe9823`, md 시작 HEAD·로컬 origin/main `0646cc51a77f289dd862128824ce7613e088c93a`, 양쪽 시작 미커밋0을 읽기 대조했다. 실제 원격 조회/Fetch·Commit/Push 없음. Git 소유권 경고는 호출별 `-c safe.directory=D:/JGY/project/drone`으로 읽기만 수행했고 전역 설정은 변경하지 않았다.

### 10/31~11/01 구현 반영 범위와 앞선 10/30 두 커밋

범위 `59b3c0f7..5905a3cb`: 27커밋·77파일·+5805/−152. 지시서 제목과 달리10/30 저녁2커밋도 포함되므로 생략하지 않았다. 아래는 커밋 메시지와 diff로 확인한 구현/시험 추가이며 실행 성공 목록이 아니다.

| 커밋 | KST 날짜 | 코드·시험 변경 |
|---|---|---|
| `e053e38d` | 2026-10-30 | 카메라 체감 흔들림·짐벌 지연·화물 분리 반동 추가 |
| `2472bc89` | 2026-10-30 | 시뮬레이터 비교 계측: 레이트 곡선·각속도·모터 스텝 응답 |
| `31819f06` | 2026-10-31 | 교육용 GPS(P)/ATTI(A) 비행 모드 추가(정찰·투하 보조 조작) |
| `c8ac5b46` | 2026-10-31 | 투하 물리 정합: 질량·관성 갱신과 속도 보존, 연출 반동 분리 |
| `14ac2cb7` | 2026-10-31 | 부하별 배터리 전압 강하를 최대 추력 한 곳에 연결 |
| `a5c364b6` | 2026-10-31 | 물리 프롭워시·지면효과(추력 경로), 카메라 체감은 물리 상태 표시 |
| `28e46ee2` | 2026-10-31 | FPV Angle/Horizon 자세 보조 모드 |
| `12a1328c` | 2026-10-31 | 역할×조작 방식 라우팅과 비행 모드·카메라 키 추가 |
| `59610871` | 2026-10-31 | 일반 화물도 투하 순간 운반 드론 속도 상속 |
| `bb48369b` | 2026-10-31 | 교육용 GPS/ATTI를 DJI Mini 4 Pro N 모드 공개 사양에 맞춤 |
| `3f5b53ae` | 2026-10-31 | 건물 차폐 공간 바람: 위치별 바람과 차폐 난류 |
| `b494b4f0` | 2026-10-31 | Mode 1/2 짐벌 축과 RC 모드 스위치·짐벌 다이얼 기본 배정 |
| `e41dbf63` | 2026-10-31 | HUD 비행 모드 표시와 선택 기억 |
| `51fd81d0` | 2026-10-31 | FPV 어안 렌즈 왜곡(설정으로 끄기) |
| `9d368341` | 2026-10-31 | 프롭 손상과 젤로 근사 |
| `ed38a04c` | 2026-10-31 | 착륙·충돌 판정과 입력→자세 지연 계측 시험 |
| `197922fd` | 2026-10-31 | 실제 PIE 자동 비행 스모크와 보고용 스크린샷 |
| `004d4c1b` | 2026-10-31 | PIE 스모크: NullRHI에서는 건너뛰고 어안 켬/끔 같은 자세 비교 추가 |
| `e2be32bb` | 2026-10-31 | PIE 스모크: FPV 1인칭 자기 기체 숨김 검증, 화면에 섞이던 투하 드론 제거 |
| `112eb0ba` | 2026-10-31 | FPV 실제 수치·모터 실기 동작·조종 민감도(Mode 1/2) |
| `b0238d34` | 2026-10-31 | 국내 무인멀티콥터 실기 기동 ATTI 조작감 측정 시험 |
| `3b0b7a25` | 2026-10-31 | 실기시험 평가기준 원문 허용오차 반영·광섬유 FPV 정찰+200g |
| `91dcb31b` | 2026-10-31 | 착륙 완료 상태 분리·DJI 착지 후 모터 정지·실기 착륙 시험 |
| `ed69916f` | 2026-11-01 | SITL 비교 반영·FPV airmode arm 토글·DJI 착륙 보호·GPS 제동 되밀림 수정 |
| `ca040362` | 2026-11-01 | 입력 PIE 시험 2건 갱신: 비행 명령 스냅샷 분리·IMC 53매핑 확인·probe 전 시동 |
| `7108b911` | 2026-11-01 | 시험 정정: StoryPhysicsTestMaps의 M2·M3 진입 맵 기대값을 분리 맵으로 |
| `5905a3cb` | 2026-11-01 | 광섬유 FPV 아이들 5.5%·DJI 경로 패드/RC 같은 수직 속도 |
### 근거와 판정

- 구현됨(코드 커밋 기준): `DroneTrainingFlightModel.*`, `DroneFlightPawn.*`, `DroneAcroFlightComponent.*`, `DroneFlightControlTypes.h`의 역할별 제어/모터/착륙, `DroneCameraFeel.*`·`DroneCameraProfile.*`·UI 설정/HUD, `DroneRotorAeroEffects.*`·배터리·Weather, `DroneDroppedPayload.cpp`·FlightDynamics 질량/관성 갱신을 대조했다. 관련 DA/IMC/렌즈 커밋과 `BuildDroneInterLinkInput.py`·`ConfigureFiberOpticMotorIdle.py` 및 테스트 기대값을 확인했다. 자산 바이너리를 Editor에서 재조회하거나 도구를 실행한 것은 아니다.
- 자동 검증됨: 이번27커밋에 대해 확인된 신규 실행 판정 없음. 첫 조회에서 Saved/Automation의 index.json263개 경로를 열거했고 최신 항목은 `UserAudioPack_20261030/Execution/SILENT3_E2/index.json`(파일시각10/30 17:37 KST)이었다. 파일시각 기준10/31 이후 JSON/log/txt/csv는 발견하지 못했다. 이후 일괄 본문 대조 중 일부 경로가 사라졌고 재조회 시 Saved/Automation 자체가 보이지 않았다. 원인·이동/삭제 주체는 미확인이다. 따라서 모든 보고서 내용/실행 날짜를 감사 완료했다고 주장하지 않으며10/31 이후 실행 근거 미확인으로 남긴다. 기존10/30 91검사를 이번 HEAD의 Pass로 재사용하지 않았다.
- 시험 소스 구현됨: `Drone.SimParity.*`의 Rate/모터 응답·교육비행·Angle/Horizon·공력/전압/차폐·payload·손상/젤로·착륙/입력지연·실기 기동·PIE 스모크·SITL replay·제동·arm/수직속도 계약과 입력 PIE fixture2개·StoryPhysicsTestMaps 기대값 정정이다. 테스트 수/통과 수를 소스 개수로 대신하지 않았다. SmokeFlightPIE는 NullRHI skip, SitlReplay는 원본CSV 없으면 skip이다. 소스의 `작업/SimParity_20261030`·`작업/SITL_20261031` 출력/입력 경로 존재나 실행 성공도 추정하지 않았다.
- 수동 확인 대기: 일반 패드/InterLink의 모드·짐벌·arm/CSC·착륙/재시동·실제 설정 저장/재실행, 손조종/실기체 교정·어안/흔들림/젤로·공력/바람/배터리/투하·스피커 청감·전체 수업/미션·패키징. 실기시험 소스의 사람모델/허용오차 인용은 실제 자격시험 합격이나 현행 규정 검증이 아니다.
- 미구현/범위 한계: full Chaos 비행 backend·전기체 물리 통일/비영CG 확대·실기체 검교정/최종 B/C 채택은 완료 처리하지 않았다. 기존 WORKBOARD Now의 기획 미정·실물 튜닝값을 유지했다. M2/M3 테스트 기대값 수정은 기존 분리 맵 계약에 맞춘 것으로 새 맵 생성/실제 진입 성공이 아니다.

### 로컬 정본과 원문 보존

현재 역할/비행모드·참고 수치/카메라는 [역할 정본](../gameplay/DRONE_TYPES_AND_CONTROL_MODES.md), 키·모터·53매핑은 [입력 정본](../tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md), 공력·전압·질량/관성·투하/착륙 계산은 [물리 정본](../gameplay/DRONE_REALISTIC_HANDLING_PLAN.md), 수동/자동 시험 계약은 [시험 가이드](../gameplay/DRONE_TEST_MAP_GUIDE.md)가 정본이다. STATUS는 현재요약, WORKBOARD는 기존 미정/대기와 실행 근거 확보→실물 확인 순서로 갱신했다.

아카이브는 한 파일씩 처리했고 이관 텍스트가 저장된 원문에 그대로 포함됨을 검사했다. 수치는 이관 직전→직후이며 이후 최신 요약/본 기록 추가 뒤 최종 크기는 별도다.

| 대상 | 원래 파일 bytes/줄 | 이관 후 bytes/줄 | 아카이브 bytes/줄 | 옮긴 제목·구간 |
|---|---:|---:|---:|---|
| STATUS.md | 29,345/126 | 26,463/116 | 70,704/287→75,570/313 | 10/30 현재 요약5문단, `Git 기준(10/30 작업컴·최종 전달)`, `작업컴 세션 운영` |
| WORKBOARD.md | 29,856/151 | 29,729/150 | 69,668/331→72,046/348 | 10/30 마지막 갱신 요약, `SYNC-SPACES-01` 완료 행, `Next` 원문 |
| DRONE_WORKLOG.md 1차 | 978,169/5,122 | 331,709/2,604 | 새668,215/3,002 | 제목이2026-10-로 시작하는120개 절 |
| DRONE_WORKLOG.md 2차 | 331,709/2,604 | 327,034/2,573 | 668,215/3,002→673,196/3,041 | `1. 이전 4메뉴 구현 기록 (2026-10-01)`, `배터리·신호 대역·HUD 조정 (2026-10-02 새벽, C PC)` |

122개 전체 이관 제목 목록/원문은 [10월 WORKLOG 아카이브의 H2 제목](archive/DRONE_WORKLOG_2026-10.md)에 있다. 첫 제목은 `2026-10-01 후속 — C 드라이브 PC 현황 최신화와 다음 작업 정리`, 120번째는 `2026-10-30 D PC — 제출14음원·파일럿 최종 통합 확인`, 추가2개는 위 표와 같다. 원래 제목/앵커에는 아카이브 링크를 남겼으며 미확정 날짜의 서문·다른 달 기록은 보존했다. docs/README에 월별 색인을 추가했다. 아카이브 본문 안의 상대 링크는 이관 전 위치 기준임을 안내하고 과거 원문 링크 자체는 고치지 않았다.

### Drone Space

pages:write-page 스킬을 적용해 기존 진행상황과 다음 작업(Sequence140, 현재 요약/Next2연산), 테스트 맵과 확인 가이드(88, 현행 시험절차 삽입1연산), Blueprint 조정과 팀원 가이드(98, 비행/카메라 조정절 삽입1연산)를 갱신했다. 4연산의 저장 영수증에 거부/ignored 없음, 같은 content stream 재읽기에서 작성한 Markdown과 일치함을 확인했다. 기존 날짜별 기록·기획·Trello 링크와 다른 절은 보존했고 새 Page/공유/예약은 없다. 기획과 개발 기준은 변경하지 않았다. 사용자 화면의 레이아웃·모든 폭 렌더는 확인하지 않았다. GitHub MD 링크에는 사용자 Commit/Push 뒤 새 본문이 반영된다.

이번 작업은 Unreal 파일 수정·Build·PIE·자동화·맵 생성·Trello/Figma 수정·Commit/Push를 수행하지 않았다. Claude에게 넘길 코드 수정은 없음. 실행 근거 확보/필요 시 별도 실행과 실물 검증은 남아 있다.

최종 정적 확인: git diff --check(core.whitespace=cr-at-eol) 오류0. STATUS26,721B/118줄·WORKBOARD29,731B/151줄로 각각30,000B 이하. 10월 WORKLOG122개 절을 시작 Git 원문과 줄끝 정규화 후 대조해 누락/본문변경0을 확인했다. 추가된 로컬 링크172개 후보 중 기존 9월 원문의 시작 버튼(A/Enter) 표기1건은 파일 링크가 아니므로 보존했으며 실제 새 로컬 파일 링크 누락은 없다. Unreal HEAD5905a3cb·git status --short 빈 결과로 기존 코드 상태를 확인했고 md 실제 변경은11파일(기존10+월별 아카이브1)이다. 엔진 실행·Commit/Push는 없으며 Space3Page 저장/본문 일치는 위 영수증을 따른다.

## 2026-11-03 — 실기 정합·배달 튜토리얼·미션 사진 후속

### 기준·근거 대조

Claude 브리지 `20261103-113242-docs-docs-realpilot-delivery-1103/prompt.md`를 UTF-8로 읽고 오전 10/31~11/01 문서 최신화에 이어 반영했다. 날짜/환경은2026-11-03 D PC(`D:\JGY\project\drone`, 문서 `D:\JGY\project\md`), Unreal HEAD `5905a3cb` + 사용자 미커밋 변경이다. 코드·자산/실행 담당 Claude, 문서·Space 반영 Codex이며 사용자가 커밋할 예정이다. 오전의 “실행 근거 미확인” 기록은 당시 기록으로 보존하고 이번 지정 로그로 후속 정정한다. 문서 시작 미커밋11파일을 보존했다.

Codex는 `Source/Drone` 미커밋 diff47파일(+1080/−139)와 관련 구현 구간·도구2개를 읽었다. DroneFlightControlTypes의 Hidden/ACTUAL, DroneCameraProfile의 화각/짐벌, DroneTrainingFlightModel의 적분/제동, DroneDroppedPayload의 Yaw 보존, DroneSelectionPreviewWidget의 재생성/촬영을 대조했다. `git -c safe.directory=...`를 조회 명령에만 적용해 소유권 경고를 우회했으며 전역 Git 설정은 변경하지 않았다. Content 포함 diff는 Git LFS clean filter가 읽기 전용 .git/lfs/tmp에 쓰려다 거부되어 중단됐다. 이후 Source/Tools/Config로 조회 범위를 제한했다. 자산/맵 저장 내용·캡처·Steam 설치와 독립 재현 수치는 지시서의 Claude 보고이며 Codex가 Editor나 시뮬레이터에서 재실행/수동 확인한 결과가 아니다.

### 변경 사실·사용자 결정

1. 게임 조작 폐지(11/03 사용자 결정): 설정 목록 제거·enum Hidden·옛 저장값 쉬운 조작 이전. 쉬운 조작 유지, FPV타격·광섬유·레이서는 실기 송신기 Mode1/2 경로다.
2. FPV는 Betaflight 기본 참고 ACTUAL70/670/0(광섬유 포함)·Angle60°·small_angle25° 시동 차단·아이들5.5%·thr_mid0.5/expo0·기본 자세 Angle이다. FPV/광섬유 업틸트25°·레이서30°, 설정3행 업틸트/화각/어안 끔·약·강, Betaflight식 OSD 셀 전압·타이머·LQ·스로틀·인공수평선·조준선을 구현했다. FPV HFOV120°는 공식 출처 없는 커뮤니티 권장값이며 사용자 실물 기준 결정으로 유지한다.
3. DJI Mini4Pro 공개 사양 참고: 대각82.1°→수평약69.7°(기존110° 대체), 짐벌−90~+60°·100°/s, P(N)12m/s·25°·S16m/s·35°, F/L3로 P→S→A·HUD S-SPORT, GPS 능동 제동35°·위치 유지·바람 보정이다. ed69916f 이후 횡풍 제동에서 적분이 얼어 약100m 흐르던 결함을 수리했다. 독립 재현(엔진 실측 아님)은12m/s 정지2.15s·9.96m, 횡풍5m/s 최대0.34m 이탈 뒤 복귀, ATTI30s135.8m 표류다. 실기 공식 제동거리는 없으며 제동/위치 유지 게인은 미정이다.
4. 학습 비행 모델 외형은 실제 제어기 각도 atan(a/g)를 그대로 표시(14°/18° 축소 대체)한다. DJI1인칭은 짐벌 수평, FPV는 기체 고정이다.
5. 사용자 zip의13미션 사진을 Thumbnail=BriefingImage로 통일했다. M1 골든타임=사막 건물 옥상·M2 길목차단=기지 정문 트럭, 튜토01~08 파일명 대응, racing1~3→Map1~3 번호 순 유지(사용자 확정)다. `Tools/AssetMigration/ApplyMissionPhotos20261103.py`, `/Game/Drone/UI/Textures/MissionPhotos_20261103`; M1/M2 선택·설명 캡처 확인은 Claude 보고다. 도구 주석의 레이싱 “사용자 확인 대기”는 이후 사용자 유지 결정으로 대체되며 소스는 docs 범위에서 고치지 않았다.
6. 팀원 Yook34 `TUT_Delivary_2`는 요청 범위만 수정·백업 `Saved/TUT_Delivary_2_Backup_20261103.umap`이다. 팔레트 TargetVisualScale XY2.5배(약3.05×3.22m)·화물3개 PayloadVisual1/3, 10/29 맵 수정에서 빠진 Tutorial.Payload.Target·서로 다른3상자 수령 설정 복구로 목적지 미인식 문제를 보완했다. 도구는 `Tools/AssetMigration/AdjustDeliveryTutorial20261103.py`다. “원통 착륙장” 문구는 그대로이며 팔레트 변경 여부는 미정이다.
7. `ADroneDroppedPayload::bKeepGroundYawOnPickup` 기본 켜짐으로 집는 순간 바닥 Yaw를 유지한다.
8. `UDroneSelectionPreviewWidget::ReloadAfterOpenSeconds`0.75초 재생성1회·`RecaptureAfterBuildSeconds`1.5초 매프레임 재촬영·텍스처 프리스트림을 구현했다.
9. 3번 TUT_Forward_Gate의 게이트 강조/HUD 제보는 D PC에서 정상 표시·TUTMapLaunchPIE.Forward 성공, Claude 캡처 `Saved/Automation/TUT/Forward.png`다. 제보 PC는 바이너리 재생성/Build 필요 안내이며 타 PC 해결 완료는 아니다.
10. Steam 무료 ORQA FPV.SkyDive·FPV Drone Simulator D PC 설치 보고. SkyDive 실행 파일 메타데이터에서 Betaflight 레이트·Angle/Horizon·카메라 각도·좁게/넓게 FOV·프롭워시·지면효과·전압강하·TPA 항목을 확인했으나 기본값은 미확인이다. 우리 TPA·FOV 빠른 선택·터틀 모드는 미구현이다.

### 자동 검증 — 원시 로그와 지시서 구분

모든 경로는 D PC Unreal `Saved/Automation/` 아래다. Codex는 Test Completed의 Success/Fail을 직접 집계했다. 실행별 코드/자산 변경이 끼어 있어 아래 수를 고유 검사 합계/동일 최종 리비전 전체 Pass로 합산하지 않는다. RenderOffScreen 회귀도 수동 Pass가 아니다.

| 검사 | 지시서 보고 | 원시 완료 집계 | 로그 |
|---|---|---|---|
| SimParity+Flight+Flow+Physics+UI+Training·RenderOffScreen | 283성공/30실패 | 283성공/30실패 일치 | ClaudeRealPilot/verify.log |
| 실패 분류·수정 재실행174개 | 149성공/19실패 | 155성공/19실패, 총174. 성공 수6차이 정정 확인 필요 | ClaudeTriage/verify.log |
| 위 후속 재검사 | 별도 수치 없음 | FlightGolden·AxisSignsAndContact 2성공/0실패 | ClaudeTriage/verify2.log |
| Drop·Selection3D·SelectionImageAssetsPIE·Prototype 등21개 | 20성공/1실패(Payload·이후 수정) | 20성공/1실패 일치 | ClaudeDelivery/verify.log |
| 배달 종단 Payload·DropSelection·PayloadGripPose | 3성공·상자3개 배달 뒤 성공 | 3성공/0실패 일치 | ClaudeDelivery2/verify.log |

사양 변경으로 고친 기대값: AssistedStrikeAim, FiberOpticAirmodeIdle, LookSettings.WidgetTransaction, Settings.KeyboardNavigation2개, RotorPilot ShortcutsPIE/FlatHull/AxisSignsAndContact(허용오차), InputToPoseLatency, TUTMapLaunchPIE.Payload(목적지 태그). FlightGolden 재기록은 ScoutEasy·DropEasy 각6/10, ScoutManual10/10 변경으로 되밀림 제거·게임 조작→쉬운 조작을 반영했다(Claude 보고). 테스트 기대값 변경과 제품 결함 수리는 구분한다.

- 기존 실패(오늘 변경 무관 근거가 있다는 Claude 분류): StoryPresentation3(문구 보정5ed30281이 테스트보다 나중), TutorialProgression, SelectionControlLayout, MissionEntryPIE, Gamepad/KeyboardStoryFlowPIE, AllDesignerContract·SelectUIPresentationPIE, TrainingPresentationCapture5(ScaleToFill vs ScaleToFit 등 일부 원인 미확정).
- 원인 미확인·2회 상한 중단: SimParity.LandingMap1PIE(EasyKeyboard 접지 전 모터 정지), SettingsCheckboxClickPIE·PauseSettingsCheckboxClickPIE(checkbox geometry0).
- 환경 의존: Mission01MovieInterLinkCancelPIE는 -DroneTestMissionMovies·실 RHI가 필요하다.
- 구현됨: 위1~8 코드·자산. 자동 검증됨: 표의 성공 항목에 한정한다. 배달/선택1실패는 후속 배달3성공으로 보완했으나 전체21개/넓은 회귀 전체를 최종 수정 뒤 재실행한 것은 아니다.
- 수동 확인 대기: 제동 세기·위치 유지·수평 복귀 체감, 외형 기울기 화면, 배달 판/화물 크기, 화물 집기 방향, 선택창3D 재로딩, FPV 설정3행 화면 배치·OSD. 실물 장치/실기체 교정·기존 전체 미션·청감·패키징 대기도 유지한다.
- 현재 미정: 배달 목표 문구·실물 튜닝 게인·기존 WORKBOARD 미정. 미구현: TPA·FOV 빠른 선택·터틀.

### 문서·Space 반영과 인계

STATUS 최신 요약/링크, WORKBOARD 실기·배달·사진·선택3D 카드/Next, 역할/모드·입력·물리·시험 절차 정본4개를 갱신했다. 과거 WORKLOG/아카이브 원문·오전 변경을 보존하고 새 진행 파일/아카이브는 만들지 않았다.

기존 Drone Space 진행상황과 다음 작업 Sequence141(현재 요약/Next2연산), 테스트 맵과 확인 가이드89(현행 확인 절차 교체1연산), Blueprint 조정과 팀원 가이드99(조작/카메라·조정3연산)를 갱신했다. 총6연산 모두 저장 영수증 거부/ignored 없음, 같은 content stream 재읽기에서 작성 본문 전체 일치를 확인했다. 기존 날짜별 기록·사람 기획/디자인·다른 절은 보존했다. 새 Page·공유/예약 변경은 없으며 GitHub MD 본문은 사용자 Commit/Push 이후다. UI의 모든 화면 폭 렌더는 검증하지 않았다. 이번 대상 Space 미반영 없음.

Claude에게 넘길 문서/후속 작업: Unreal `.claude/known-test-failures.md`에 기존 실패·원인 미확인3종·영상/RHI 환경 의존·Payload 수정 후3성공·기대값/FlightGolden 갱신을 분리 반영하고 Triage 성공 수149↔155 차이를 정정 확인할 것. 사진 도구 레이싱 주석의 확인 대기도 사용자 번호 유지 결정과 맞출 필요가 있다. 이 docs 세션에서 Unreal 파일은 수정하지 않았고 Build/PIE/자동화/맵 생성·Commit/Push·Trello/Figma 수정은 실행하지 않았다.

최종 정적 확인: git diff --check(core.whitespace=cr-at-eol) 오류0, 대상 현재문서6개의 로컬 파일 링크 누락0. STATUS 26940B/118줄, WORKBOARD 29951B/154줄로 각각30,000B 이하. 이번 수정7파일이며 git status --short의 전체11파일 중 docs/README와 아카이브3개는 오전 변경 보존이다. 추가 아카이브/새 파일/Commit/Push 없음.

## 2026-11-03 — SkyDive 실측 정합(FPV 물리)

### 기준·읽기 대조

브리지 `20261103-160217-docs-docs-skydive-parity-1103/prompt.md`를 UTF-8로 읽고 같은 날 realpilot-delivery 반영 뒤에 추가했다. 기준은 D PC(`D:\JGY\project\drone`, md `D:\JGY\project\md`), Unreal HEAD·로컬 origin/main `6de91783`, 브랜치 `feat/skydive-fpv-physics-parity` + Claude 미커밋이다. 코드·자산·실측·실행 담당 Claude, 문서·Space 반영 Codex. md 시작 HEAD·로컬 origin/main `7d9afc8`, 작업트리 Clean을 확인했으며 Commit/Push·Fetch는 하지 않았다.

Codex는 지정 C++/골든 diff8파일·신규 시험/적용/덤프 도구3개, 지정 DA2개 수정 상태, 실측 원문0·3~11절과 지정 로그/보고서를 읽기 대조했다. 자산 바이너리를 Editor에서 재조회하거나 실측 캡처37장을 독립 판독한 것은 아니다. DA 적용값은 도구 내용·Claude 실행 보고와 자동 로그를 근거로 한다. Unreal 수정·Build/PIE/자동화·도구 실행은 하지 않았다.

### 실측·구현·결정

- 사용자 지시: “콘솔 우리값 기준으로 넣고 조작 비교해서 우리 겜에 적용”. SkyDive 비교값의 FPV 타격·레이서 적용은 확정이며10/31 결정B의 실기 추력비8.3보다 비교 시뮬 정합을 우선한다. 되돌리기는 가능하지만 복귀 여부는 미정이다.
- 실측 원문은 Unreal `Saved/SkyDive_측정_지시서_20261103.md`, 캡처37장은 `Saved/SkyDive_측정_캡처/`다(Git 제외 Saved·온라인 공개 아님). SkyDive v2.9.2(b) 기본 RACER453g·2450KV·1400mAh·40180RPM, 키보드 가상 스틱 입력이다. 이륙24±1%·호버22~23%, 100/46/28% 상승 정속 약36/20/8 OSD ALT단위/s(m 추정), Acro 롤/요1초 약1.6/1.3회전(667°/s와 부합), 기체 고정 카메라·업틸트30°·FOV90·어안0이다. 스틱 램프·캡처지연 약0.9초·맵 길이/속도OSD 부재 제약이 있다. 감속은 저속도 정지로 단정할 수 없으며 최고속·고속 감속은 측정 실패다.
- 구현됨: FPV 타격·레이서 DA의 선형 추력·호버23%·질량/RPM·축별 항력·수직 상한을 적용했다. 수치 정본은 [현재 FPV 기준값](../gameplay/DRONE_TYPES_AND_CONTROL_MODES.md#공개-자료를-반영한-현재-fpv-기준값), 계산식 정본은 [Legacy 추력·항력·회전](../gameplay/DRONE_REALISTIC_HANDLING_PLAN.md#legacy-추력항력회전)이다. 이전 값은 적용 스크립트 로그 `before=`를 참조한다. MaxSpeed3200·레이트200/667/0.58·Angle60°·사용자 HFOV120°·광섬유 DA는 이번 적용에서 변경하지 않았다.
- 구현됨: `FDronePhysicalFlightSettings::VerticalQuadraticDragPerCentimeter`(기본0=기존 등방)와 `DroneAcroFlightComponent.cpp`의 기체 Up/직교 성분별 제곱 항력을 추가했다. 다른 기체·로터 후보 커널은 영향 대상이 아니다. `DroneAcroFlightComponent.h`·`DroneFlightPawn.h`에 시험 friend를 추가했다.
- 구현됨: 신규 `DroneSimParitySkyDiveMeasuredTest.cpp`의 `Drone.SimParity.SkyDiveMeasured`는 호버23%·상승36/20/8·35% 풀피치3초 수평22~40m/s를 판정한다. `DroneSimParityMotorTest.cpp`의 FpvRealSpecAndMotor는 추력비3.67·호버23%·100km/h 이상/프로파일 상한 이내를 검사한다(이전8.3·25~45%·130km/h 근접 대체).
- 구현됨: `Tools/AssetMigration/ApplySkyDiveMeasured20261103.py`로 DA2종 적용, `DumpDroneFpvPhysics.py`는 저장 없는 조회 도구다. `FlightGoldenBaseline.txt` FPVAcroMode1/2만20행 재기록했고 Scout·Drop·UGV 행은 diff상 동일하다. `DroneThrustGravityConsistencyTest.cpp`의 무항력 헬퍼 수직계수0, `DroneMotorControlTest.cpp`의 RC 착륙 출력25→15%·Acro 키보드/패드2초 속도비 하한0.80→0.75로 기대값을 조정했다. 기대값 변경은 제품 결함 수정과 구분한다.

### 자동 검증 — D PC Claude 실행·Codex 로그 대조

경로는 Unreal `Saved/Automation/ClaudeSkyDive/` 아래다. JSON의 `succeeded`는 경고 성공을 제외하므로 로그의 Success 수와 구분한다. 실행별 수를 합산하거나 최종 수정 뒤 전체 회귀 Pass로 표시하지 않는다.

| 검사/시점 | 지시서 | 실제 로그·보고서 | 근거 |
|---|---|---|---|
| SimParity·DA1차·RenderOffscreen | 37성공/2실패 | 완료37성공/2실패 일치 | simparity2.log |
| SimParity+Flight·DA최종 | 84성공/5실패 | JSON 일반84·경고 성공2·실패5, 로그 Success86/Fail5(총91) | flight3.log·report_flight3/index.json |
| FPV 골든 재기록 | 재기록 | FlightGolden1성공/0실패 | golden_record.log |
| 기대값/골든 수정 뒤 재검증6종 | 9성공/0실패 | JSON 일반9·경고 성공1·실패0, 로그 Success10/Fail0(총10) | verify4.log·report_verify4/index.json |

flight3의 경고 성공2건은 AssistedStrikeAim.EligibilityAndLifecycle·MotorControl.MixedDeviceHandoffKeyAxis, verify4의 경고 성공1건은 ThrustGravityConsistency.CandidateResponseFrameParity다. 지시서 수치는 JSON 일반 성공 수와 일치하며 누락된 경고 성공을 위처럼 별도 표시했다.

- 1차 실패: LandingMap1PIE(기존)·SkyDiveMeasured 수평1차 기준 미달. 수직 항력0.000169→최종0.000185 및 수평 판정 조정 뒤 후자는 성공했다.
- flight3 실패5건: LandingMap1PIE·RCAbsoluteBoundLifecycle·SpaceKeyDispatch·LegacyResponseFrameParity·FlightGolden. 후자4건은 기대값3건/골든 재기록 후 verify4에서 성공했다. LandingMap1PIE는 기존 잔여 실패이며 verify4에서 재실행하지 않았다.
- 최종 SkyDiveMeasured: 두 기체 모두 호버0.230·상승100/46/28%=36.0/18.9/7.3m/s·호버 드리프트0.00m/s, 35% 풀피치(Angle60°) 수평3초25.2·6초34.7m/s. SkyDive의 가속 중25~30m/s는 약30~45° 추정으로 시험 조건과 완전히 동일하지 않다. FpvRealSpec은 추력비3.67·호버0.230·고도 유지 최고속144km/h(40m/s 상한)다. 이 최고속을 SkyDive 실측값으로 쓰지 않는다.
- 자동 검증됨: 위 성공 항목 범위만. 수동 확인 대기: FPV 타격·레이서 손 조종 호버 위치·상승 세기·수평 가속·Angle 복귀. 광섬유 적용 여부 결정 대기.
- 미구현/미측정: SkyDive 최고속·고속 감속·광섬유 정합·키보드 램프 모델 비교. SkyDive 비스티키는 키 해제 즉시0%이며 우리 키보드 모델 채택은 미정이다. MaxSpeed 상한·추력비8.3 복귀 여부도 미정이다.

### 문서·Space 반영

STATUS 최신 요약/Git 기준, WORKBOARD의 FLIGHT-PHYSICS-01·SIMPARITY-EXEC-01/Next, 역할 기준값 표·물리 식/Steam 문단을 갱신했다. 이전 realpilot-delivery/과거 기록은 보존하고 새 파일·아카이브는 만들지 않았다. Drone Space 저장 결과와 최종 정적 확인은 아래 후속 문단에 기록한다.

Drone Space는 기존 진행상황과 다음 작업 Sequence142(현재 요약·Next2연산), Blueprint 조정과 팀원 가이드 Sequence100(물리값·실측/카메라2연산)을 갱신했다. 저장 영수증4연산 모두 거부/ignored 없음, 같은 content stream의 대상4블록 재읽기에서 작성 본문과 전체 일치를 확인했다. 기존 날짜별 기록·기획/디자인·Trello 링크·다른 절을 보존했고 새 Page·공유/예약 변경은 없다. 이번 대상 미반영 없음. GitHub MD 본문은 사용자 Commit/Push 뒤 반영되며 사용자 화면의 모든 폭 렌더는 확인하지 않았다.

범위 밖 발견·Claude 인계: `DroneFlightControlTypes.h`의 새 필드 주석과 `ApplySkyDiveMeasured20261103.py`의 머리말은 SkyDive “31% 풀피치45m/s 이상”을 아직 인용하지만 실측 원문6절은 해당 독해를 정정하고 최고속 미측정으로 둔다. 헤더의 “광섬유에도 값을 넣는다” 문구도 실제 적용2종/광섬유 미정과 다르므로 주석 정정이 필요하다. 실측 원문11절의 시험 하한25와 현재 소스22 차이도 기록 정합 확인 대상이다. docs 범위에서 Unreal/Saved 원문은 수정하지 않았다.

최종 정적 확인: git diff --check(core.whitespace=cr-at-eol) 오류0. STATUS27411B·WORKBOARD29926B로 각각30,000B 이하. 이번 변경은 지정5파일이며 과거 WORKLOG 본문 보존·추가 로컬 링크 검사는 아래 확인 결과를 따른다. Build/PIE/자동화·Commit/Push·Figma/Trello 수정·아카이브/새 파일 생성 없음.

확인 완료: 시작 HEAD의 WORKLOG 전체가 줄끝 정규화 후 그대로 접두부에 보존됨을 검사했다. 지정5파일의 실제 로컬 파일 링크 누락0이며 기존 과거 본문의 버튼 표기 [A/Enter]는 파일 링크가 아니므로 보존했다. git status --short는 지정5파일 수정만 표시했다.

### 같은 날 후속 — 광섬유 SkyDive 정합 확장

2026-11-03 D PC, Unreal HEAD `6de91783`·브랜치 `feat/skydive-fpv-physics-parity` + Claude 미커밋, md는 앞선 Codex 반영분 포함 미커밋이다. 실행 담당 Claude·문서/Space 반영 Codex. 사용자 “네, 적용”으로 광섬유 적용이 확정됐다. 앞선 절의 광섬유 미정/미구현·미변경 및 적용2종 표기는 당시 상태이며 이 후속으로 대체한다. 현재 값 정본은 [FPV 기준값](../gameplay/DRONE_TYPES_AND_CONTROL_MODES.md#공개-자료를-반영한-현재-fpv-기준값)이다. 10/31 정찰 기체+0.2kg 중 질량은 유지하고 정찰 추력 상속은 대체했다.

- 구현됨: 광섬유 DA 추력40→79.16N·호버23%·추력비2.04→3.67 및 SkyDive 항력/수직 제한 적용. `ApplySkyDiveMeasured20261103.py`에 광섬유 추가, `Drone.SimParity.SkyDiveMeasured` 광섬유 행은 역할 상한15m/s로 판정, `DroneSimParityMotorTest.cpp`의 `FiberOpticSpec` 기대값은 정찰 추력 상속에서 SkyDive 호버23% 규칙으로 변경했다.
- 자동 검증됨(Claude 지시서·Saved 측정 지시서11절 근거, Codex 재실행 없음): 적용 후 SimParity+Flight **87성공/2실패**(`Saved/Automation/ClaudeSkyDive/flight5.log`·`report_flight5`). 실패는 기존 LandingMap1PIE와 광섬유 상한 기준 미반영 SkyDiveMeasured다. 기준 수정 후 SkyDiveMeasured·FiberOpticSpec·RealPilotPawnScope **3성공/0실패**(`verify6.log`·`report_verify6`, 같은 디렉터리). 최종 전체 회귀 Pass로 처리하지 않는다.
- 광섬유 측정: 호버0.230, 상승100%/46%=15.0m/s(상한)·28%=7.3m/s, 35% 풀피치3초 수평14.3m/s(상한15). FiberSpec은 추력비3.67·1초 상승15m/s·최고속54km/h(역할 상한)다. SkyDive 최고속 실측값이 아니다.
- 수동 확인 대기: 광섬유15m/s 상한 안의 호버·상승 변화 손 조종 체감. 미정: 광섬유15m/s 상한 조정·최고속도·10/31 추력비8.3 복귀 여부. 과거 기록/실패는 보존한다.

문서 반영: STATUS 요약·WORKBOARD FLIGHT-PHYSICS-01/Next·역할 가이드 기준값 수정. 기존 물리 가이드 미커밋 변경은 보존했다. 새 파일/아카이브·Unreal 수정·Build/PIE/자동화·Commit/Push는 수행하지 않았다. Space 및 정적 검증 결과는 아래에 추가한다.

최종 확인: 진행상황 Space Sequence143의 요약·Next 2연산 모두 적용(거부/ignored 없음), 같은 content stream 재읽기로 두 블록 본문 전체 일치를 확인했다. 다른 페이지는 변경하지 않았으며 이번 대상 미반영 없음. STATUS27,458B·WORKBOARD29,996B로 각각30,000B 이하, git diff --check(core.whitespace=cr-at-eol) 오류0. git status의 수정5파일 중 이번 작업은 지정4파일이며 DRONE_REALISTIC_HANDLING_PLAN.md는 앞선 변경 그대로다.

## 2026-11-03 — 작업 브랜치 커밋 main 병합·Push

사용자의 “커밋 병합해서 푸쉬해줘” 지시에 따라 Codex가 실제 Git/원격을 확인하고 작업 브랜치를 main에 반영했다. 시작 Unreal은 feat/skydive-fpv-physics-parity=682852c5b96949bf3e16164a730fdeae5cee0926·Clean, main/origin/main=6de91783이었다. Fetch 후 작업 브랜치만1커밋 앞서고 main이 조상임을 확인했다. 변경14개는 기존 SkyDive Source/검사/Golden/도구와 FPV·레이서·광섬유 DA3개이며 diff --check를 통과했다.

기존682852c5 커밋을 재작성/스쿼시하지 않고 main으로 Fast-forward 병합했다. Push 뒤 실제 origin/main ls-remote=로컬HEAD 전체SHA, tracking0/0·worktree/index Clean이다. 원래 기능 브랜치도 그대로 보존했다. Force Push·새 기능/자산 편집·맵저장·엔진 제어·Build/PIE/자동검증은 없으며 이전 혼합 성공/실패 및 후속 집중3통과를 이번 병합의 새 검사로 재사용하지 않는다.

MD 시작main7aad12e는 Fetch 후 원격 일치·Clean이었다. 현재 STATUS/WORKBOARD의 오래된 미커밋/Git 표기를 교정하고 이 기록을 append-only로 추가해 동반 Commit/Push한다. Drone Space의 기존 진행 Page도 같은 Git 인계와 새 검사 없음으로 갱신하며 최종 문서SHA/원격 확인은 해당 인계와 Saved/Automation/MergePush_20261103/GIT_FINAL_RECEIPT.json을 따른다. STATUS/WORKBOARD는30KB 제한 안에 유지한다.


## 2026-11-04 — Antigravity 변경 감사와 병합 버전 검증

- 사용자 범위: 병합본 Build/FPV·레이서·광섬유 물리, Mode1/2 표기, Easy→Mode2 제보, Drop 선택 프리뷰 화물, M2~4 제공 영상 및 Antigravity 변경 전부 감사. main682852c5/MD d955b5e 유지·이번 Commit/Push 없음. 옛 실행 채팅은 사용량 제한으로 실행하지 못했고, Codex Root가 단일 실행 소유권을 인수했다. 하위 검토자는 Source/Content/엔진 쓰기 없이 Saved 초안만 제공했다.
- 입력18파일(추적11/미추적7)을 REQUEST_BASELINE.json/InputBackup에 byte 백업했다. Antigravity의 DA3·FileMediaSource3·Movies3·Config·연결 도구·UI/물리 변경을 Git diff와 실제 저장 자산/로그로 대조했다. 순수 main 단독 실행이 아니라 main+외부18개를 초기 기준으로 사용했다.
- 초기 Build19.98초 성공. 기존43개는 일반37/경고3성공·3실패: SelectionControlLayout(옛 이름/Designer wrap), TrainingGpsStopAndHold(바람3조건), LandingMap1PIE. 신규 독립 기하검사는 실제 저장3기체의 Easy 전진 시 앞부분 상승을 재현했고 Mode1/2는 정상 하향이었다. 외부 기존 VisualBank 기대값도 같은 역방향으로 바뀌어 결함을 가리므로 원래 기대를 복원했다.
- 수정: Pawn 전진 pitch2곳의 원래 음수 복원(최종 HEAD와 동일), Training 이동 중 Integral 매 프레임 초기화 제거, native fallback에서만 Selection no-wrap 적용, enum DisplayName/ControlsGuide까지 ‘모드 1/2’, OpeningMovie의 실제 decoder 크기 기반 비율 유지. HoldPoint/AltitudeHold 추적은 유지하고 질량/추력/항력·수직/프로필 상한은 바꾸지 않았다.
- Easy→Mode2: 실제 saved WBP·DA·PawnClass로 Selection callback9 + Settings Combo Apply3 → spawn/possession/HUD12개 통과. FPVStrike DA 기본3이어도 Easy 선택0/표시0/실제0을 확인했다. 생산 resolver 변경 없이 fresh Build에서 재현되지 않았다. 초기 신규 fixture는 DefaultDroneId/목표 준비 누락으로 실패해 시험 준비만 수정했다. RED1 반복 준비 실패 후 Root 자신의 시험 엔진만 중단한 원시 로그도 보존한다.
- LandingMap1: 실제 충돌 callback의 touchdown 모터OFF가 sweep pullback1.0239cm에서 발생해 다음 tick의 기존 gap<1cm 관측보다 빨랐다. 테스트는 고유 착지 사유·직전ON→OFF·실제 floor hit/법선/비관통을 추가 관측한다. 단순OFF를 접지로 간주하지 않고 원래1cm/속도/시간/접촉 assertion과 이전 airborne failure 누적을 유지했다. 생산 착지 허용범위 변경0. 최종 실제6시나리오 통과.
- 최종 Build GREEN_C11.75초 성공, module SHA256=aa234c35d29824395b0aee8e143b9947bee4abb677e15099bad72b4923b34778. GREEN_FINAL64개: 일반42+경고21성공/1실패·notRun0,303.24초. 실패 Selection3D.PIE는 index0/phase0 대기시간초과이며 같은 DLL의 ISOLATED_SELECTION에서24.03초 단독 경고성공1/실패0. 이를 묶음 전체 Pass나 해결 완료로 바꾸지 않는다. SitlReplay는 sitl_run.csv 부재로 내부skip1(보고서Success)이며 실제 SITL 검증으로 세지 않는다.
- 실제 기본 Mode1/2 경로3기체와 두 시점의 방향/카메라, active 물리값·모터τ0.055초·호버≈0.23·GPS 바람·착륙 통과. FPV0.66kg/23.75N·레이서0.453kg/16.30N·광섬유2.2kg/79.16N, idle5.5%·수평/기체Up 제곱항력.000027/.000185 per cm·선형.06/s·World-Z36m/s, 프로필40/40/15m/s. Easy ON은 별도 FloatingPawnMovement 보조이며 Acro 힘식과 동일하지 않다. 기존 SkyDiveMeasured/Spec 일부는 real-model flag opt-out seam이고 신규 semantic/실제 출격 검사는 기본 role routing을 유지했다.
- DropPreviewPayloadIsolation: actual Drop clone의 화물 숨김·reload·양수 RHI 모델 pixels, 원본 source의 화물 가시성/재고/질량/pose 보존 통과. 생산 프리뷰 추가 수정0. 단일 FScreenshotRequest가 Editor 화면을 잡은 PNG는 외형 확인 근거로 쓰지 않는다. 실제 기존 선택창 단독 검사의6기체 캡처를 따른다.
- 영상M2/M3/M4 원본/복사 SHA·bytes 동등(각107506287/120223606/116335064B), avc1+mp4a·14.443/17.216/13.909초·3704×1722/3622×1672/3768×1696. 실제 catalog→각 movie decoder, Esc/패드B/RC Cancel·브리핑 복귀·조기 맵이동0·끝까지 seek 없이 자연 종료3개 통과. M1 기존2개도 통과. RED2의16:9 늘어짐은 최종 sourceAspect=frameAspect로 수정했다. 묶음 실행의900×72 캡처는 크기 QA로 인정하지 않고 fresh VISUAL_FIXED 결과와 별도 대조한다. Python 임시 viewport override 시도는 property명 오류로 적용되지 않았으며 해당 원시 오류를 보존한다.
- 잔여: Antigravity OSD는 글자뿐 아니라 bFpvOsdActive=false로 인공수평선도 끈다. EnsureFpvOsdWidgets의 Designer 숨김은 호출되지 않는다. 제거 의도 질문은 미응답으로 현재 생산코드를 그대로 보존하며 이 항목을 완성 Pass로 표시하지 않는다. 실물 장치 손 조종·전체 미션 완주·청감·Cook/패키징은 미실시다.
- 보존: 저작 맵48/48 SHA 동일, 입력 Content/Config/도구 동일, 사용자 Saved8개는 시험 후 백업과 대조/복원, HEAD동일. 상세 원본은 D:/JGY/project/drone/Saved/Automation/AntigravityAudit_20261104의 baseline·RED·GREEN·별도실행·보존 보고서이며 Git 제외 로컬 자료다. 기존 팀원 맵/자산·사용자 입력 설정을 덮어쓰지 않았다. 문서/Space의 새 요약은 아래 동기화 결과로 구분한다.

### 11/04 감사 마무리·Space 반영

- fresh VISUAL_FIXED의 실제 M2/M3/M4 재생/취소/자연 종료3개 모두 성공했다. 캡처는1280×720/1280×686/1274×680이며 세 장을 직접 읽어 원본 비율·자막·검은 스킵 배경을 확인했다. 큰 Drop 선택창 단독 캡처도 읽어 들고 있는 화물이 빠진 것을 확인했다. 임시 viewport Python 설정은 실패했으므로 창 크기가 그 스크립트 덕분이라고 주장하지 않는다.
- 저장 없는 메타데이터 commandlet: FileMediaSource3 모두 ./Movies 상대 경로이고 실제 WBP_DroneCinematic의 PreserveMovieAspectRatio=True다. BriefingAsset의 Python str은 SoftObjectPath 구조체 설명만 반환하므로 연결 근거는 실제 catalog→해당 movie 통합검사를 사용한다. HUDKit WidgetTree는 protected로 읽지 못해 Designer OSD 존재/숨김을 확인했다고 표시하지 않는다.
- 경고는 오디오 장치 RAW 모드 미지원·PenetrationPullback cvar 반복 조회·광섬유 MI_cable SplineMeshes usage flag 누락/기본 재질 fallback이다. 케이블 재질은 이번 외부18파일 변경 대상이 아니며 별도 자산 저장 없이 잔여로 남긴다.
- Drone Space 기존 진행/테스트/BP3페이지에서6개 연산 적용·거부0, readback6개 본문 정확히 일치. sequence146/90/101, 신규 Page/권한/예약 변경0. 로컬 STATUS26993B·WORKBOARD29807B로30KB 이하, WORKLOG append-only. 이번 코드/문서 Commit/Push 없음. 최종 엔진/컴파일러0.


### 11/04 후속 — OSD 글자만 숨김·인공수평선 유지 확정

- 사용자 답변으로 전압·LQ·스로틀·시간 글자만 숨기고 인공수평선을 유지하도록 확정했다. 앞선 제거 범위 미응답 기록은 당시 상태이며 이번 결정으로 해소한다.
- DroneFlightHUDKit에서 글자 숨김을 매 Refresh에 연결하고 ForEachWidgetAndDescendants로 저장/자식 WBP의 이름 계약4종만 Collapsed 처리한다. 부모 패널과 비문자 장식은 건드리지 않는다. Native 텍스트 재생성 없이 기존 bShowFpvOsd·실기 송신기·1인칭·비투하 카메라 조건으로 선 활성화를 복원했다. 전압/배터리·타이머 계산·비행/입력/카메라/미션 자산은 변경하지 않았다.
- 신규 Drone.UI.FpvOsdTextOnly가 수정 전 실제 saved HUD/FPVStrike·Racer·FiberOptic에서 수평선 비활성·픽셀 차이0과 Designer 글자4종 노출로 실패했다(RED_RUNTIME). 최초 Build는 신규 cpp가 캐시에 반영되지 않아0action이었고, -NoUBTMakefiles로 소스 재탐색 후32.16초 실제 컴파일했다.
- 생산 수정 후 Build60.40초 성공, 같은 DLL의 FpvOsdTextOnly·HudDesignerContract·RealPilotSpecNumbers·FpvRealTransmitterModel 집중4개 성공/실패0. 원시 일반4·경고0 성공, 2.34초다. 직전64개 전체를 이 후속에서 다시 실행한 결과는 아니다.
- 실제 저장 HUD 수평/기울기/명시OFF 렌더를 비교해 선 가시성과 pitch/roll 추종을 확인하고 세 역할×모드1/2 활성·Easy/3인칭 숨김을 검사했다. 저장 트리 기반 Designer fixture의 기존 글자4종 숨김·부모/장식 유지와 native fallback의 글자 미생성도 검사했다. 증거는 Saved/Automation/FpvOsdTextOnly_20261104의 RED/GREEN 로그·Captures/FINAL_VERIFIED.json이다. 실물 조종 확인은 별도다.
- 저작 맵48개 SHA동일·사용자 Saved8개 백업 대조/복원, 소스2개와 신규 테스트1개만 이번 추가 변경이다. 엔진·Build는 Root 한 곳 순차 실행, Commit/Push 없음.

- OSD 후속 Space 반영: 진행147·테스트91·BP102의 기존3블록에 글자만 숨김/수평선 유지·BP 조정값·집중4검사 결과를 적용하고3개 본문 readback 일치를 확인했다. 새 Page/권한/예약/Commit/Push 없음. 실제 saved HUD의 수평/기울기1280×720 PNG2장을 직접 읽어 글자4종 부재와 흰 수평선·중앙 조준선 유지/기울기 이동을 확인했다.


## 2026-11-04 — 전체 자동 점검

- 사용자 ‘전반적으로 점검 한번 싹’ 요청. main682852c5/같은 DLL eb613656732a5195f108fc191196214ff623dbf9b41b51028d79890d32cc45a8 유지·제작 도구8개 제외·Editor 고유574개 실행. Build 재확인 성공(추가 컴파일0), 소스/자산 수정·Commit/Push 없음. Root 단일 엔진·순차 실행.
- 1차 실제530통과/43실패/1스킵, 후속 조건 분리 후 실제533통과/40실패/1스킵. 최초 실패/CLI는 보존하고 재검사로 지우지 않는다. 실물/독립 게임 창/패키징과 구분한다.
- Core/최초Flow에 영상 옵션이 포함됐음을 확인해 일반 Mission/UI와 후속Flow에서는 제거했다. 미디어5개는 전용 옵션 실행이다. 사용자 PIE942×386은 일부 캡처의 최소400px 조건보다 작아 UI/후속에는 저장 없는1280×720 기본값을 썼고 원본 설정을 복원했다.
- Source/Config/Tools733 SHA동일·보호122(저작 맵48) SHA동일·Content9859 metadata변경0·Saved8개 대조/복원·HEAD동일. 원시 전체는 로컬 Saved/Automation/GeneralCheck_20261104의 BASELINE/각 index.json·RUN·RESULTS_CURRENT/FINAL_AUDIT/REPORT.md다. Git 제외 파일을 GitHub에 올렸다고 표시하지 않는다.

| 범위 | 고유 검사 | 실제 통과 | 건너뜀 | 실패 |
|---|---:|---:|---:|---:|
| 비행·물리·입력/AI | 285 | 279 | 1 | 5 |
| 진입·메뉴 흐름 | 55 | 51 | 0 | 4 |
| 미션·튜토리얼·오디오 | 131 | 115 | 0 | 16 |
| UI·설정·영상 | 100 | 88 | 0 | 12 |
| 기존 KnownIssues | 3 | 0 | 0 | 3 |

마지막 실패(원시 메시지는 로컬 REPORT/JSON):

- Drone.AI.ShotgunSystemsTestMapPIE: Shotgun NPC did not make pursuit progress (state=0 detected=0 pursuits=1 disengages=0 move=0 maxTravel=560.6 minDistance=2091.2 maxSpeed=600.0 pawn=V(X=783.05, Y=-459.55, Z=90.15) target=V(X=500.53, Y=-2061.66, Z=-19871.91)). Samples: t=6.55 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.57 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.58 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.60 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.62 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.64 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.65 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.67 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.68 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.70 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.72 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.74 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.76 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.77 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.79 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 target=-100.0/1627 moves=1 | t=6.81 p=2 s=0 body=71.4 vel=0.0 speed=0.0 next=149.6/908 ta
- Drone.Integration.ExtendedRoleDrones: Expected 'Fiber Pawn uses the DroneSpy body and four separated rotor meshes' to be true.
- Drone.Integration.RoleDroneAssets: Expected 'Role Pawn references exactly its selected Drone Pack meshes' to be true.
- Drone.Prototype.FlightProfiles: Expected 'FPV Strike caps world vertical speed at 30 m/s' to be true.
- Drone.Signal.ControlLink: Expected 'Real Move/Altitude handlers queue pilot input while connected' to be false.; Expected 'Fresh Move input works again after reconnect' to be false.
- Drone.Flow.GamepadMissionFlowPIE: [UI-PAD] FAIL: A again on the chosen Hover card → Briefing with focus on the launch button (state=3, player=BP_DroneFrontEndPlayerController_C_0, Slate focus=SButton [Button.cpp(67)], highlighted=FinishMissionBriefingButton, droneCard=-1)
- Drone.Flow.KeyboardStoryFlowPIE: [UI-KEY] FAIL: Enter again → Briefing with focus on the start button (state=3, Slate focus=SButton [Button.cpp(67)], highlighted=FinishMissionBriefingButton, card=-1, drone=-1)
- Drone.Flow.MissionEntryPIE: Expected 'Native Selection fallback is usable without a finished WBP' to be true.; Expected 'Mission Success creates the Result Widget' to be not null.
- Drone.Flow.TutorialProgression: Expected 'Next lesson is the following playable one' to be Mission.Tutorial.FPV, but it was Mission.Tutorial.GateFlight.; Expected 'Next lesson becomes the selection' to be Mission.Tutorial.FPV, but it was Mission.Tutorial.GateFlight.
- Drone.Audio.UserCombat.SpatialFar: Synchronous WAV export from the same PIE mixer failed
- Drone.Audio.UserUI.CountdownLifecycle: Same-device synchronous UI mixer WAV export failed
- Drone.Audio.UserUI.HealthLifecycleAndMasterMute: Same-device synchronous UI mixer WAV export failed
- Drone.Tutorial.TUTMapLaunchPIE.FPV: Expected 'No arm key is needed before the real rear impact' to be true.; Expected 'Actual FPV lesson vehicle is destroyed in one impact' to be true.
- Drone.Tutorial.TUTMapLaunchPIE.Hovering: Expected 'Actual lesson goal completes without a return step' to be true.
- Drone.Tutorial.TUTMapLaunchPIE.LOS: LOS takeoff advances to forward: The two values are not equal.; LOS still requires its backward return: The two values are not equal.
- Drone.Tutorial.TUTMapLaunchPIE.StoryM1: Expected 'Actual Story goal completes immediately without return' to be true.
- Drone.Tutorial.TUTMapLaunchPIE.StoryM2: Expected 'StoryM2: drone starts over SM_helicopter_base' to be true.; Expected 'Actual FPV sweep intercepts the Story vehicle' to be true.
- Drone.Tutorial.TUTMapLaunchPIE.StoryM3: Expected 'StoryM3: objectives come from the lesson DA' to be 1, but it was 2.; Expected 'Actual Story goal completes immediately without return' to be true.
- Drone.Tutorial.TUTMapLaunchPIE.StoryM4: Expected 'StoryM4: lesson drone is selected' to be true.; Expected 'StoryM4: lesson launches' to be true.
- Drone.Tutorial.TUTMapLaunchPIE.StoryM4_Start1: Expected 'StoryM4_Start1: lesson drone is selected' to be true.; Expected 'StoryM4_Start1: lesson launches' to be true.
- Drone.Tutorial.TUTMapLaunchPIE.StoryM4_Start2: Expected 'StoryM4_Start2: lesson drone is selected' to be true.; Expected 'StoryM4_Start2: lesson launches' to be true.
- Drone.Tutorial.TUTMapLaunchPIE.StoryM4_Start3: Expected 'StoryM4_Start3: lesson drone is selected' to be true.; Expected 'StoryM4_Start3: lesson launches' to be true.
- Drone.Tutorial.HoverMissionPIE: Expected 'Lesson releases camera at result' to be false.; Expected 'Normal drone view restored' to be true.
- Drone.Tutorial.IndependentMapEntryPIE: Expected 'Lesson releases camera at result' to be false.; Expected 'Normal drone view restored' to be true.
- Drone.Tutorial.ObserverLessonPIE: Expected 'Lesson releases camera at result' to be false.; Expected 'Normal drone view restored' to be true.
- Drone.UI.StoryPresentation.Data: Expected 'Short goal follows the current execution rule' to be "광섬유 드론으로 재밍 구역을 완전히 통과하세요.", but it was "재밍 레이더 파괴 → 거점 방어 포탑 파괴".; Expected 'Short goal follows the current execution rule' to be "지휘 표적 세 개를 모두 파괴하세요.", but it was "재밍 레이더 파괴 → 패트리어트 미사일 발사대 파괴".
- Drone.UI.StoryPresentation.Layout1280: Expected 'Short goal follows the current execution rule' to be "광섬유 드론으로 재밍 구역을 완전히 통과하세요.", but it was "재밍 레이더 파괴 → 거점 방어 포탑 파괴".; Expected 'Short goal follows the current execution rule' to be "지휘 표적 세 개를 모두 파괴하세요.", but it was "재밍 레이더 파괴 → 패트리어트 미사일 발사대 파괴".
- Drone.UI.StoryPresentation.Layout1920: Expected 'Short goal follows the current execution rule' to be "광섬유 드론으로 재밍 구역을 완전히 통과하세요.", but it was "재밍 레이더 파괴 → 거점 방어 포탑 파괴".; Expected 'Short goal follows the current execution rule' to be "지휘 표적 세 개를 모두 파괴하세요.", but it was "재밍 레이더 파괴 → 패트리어트 미사일 발사대 파괴".
- Drone.UI.TrainingPresentationCapture.1280: Expected 'The preview actually belongs to the selected mission' to be true.; Presentation capture timed out
- Drone.UI.TrainingPresentationCapture.1920: Expected 'The preview actually belongs to the selected mission' to be true.; Presentation capture timed out
- Drone.UI.TrainingPresentationCapture.RacingMap1: Expected 'The preview actually belongs to the selected mission' to be true.; Expected 'The authored close-map photo is fitted without extra UI cropping' to be true.
- Drone.UI.TrainingPresentationCapture.RacingMap2: Expected 'The preview actually belongs to the selected mission' to be true.; Expected 'The authored close-map photo is fitted without extra UI cropping' to be true.
- Drone.UI.TrainingPresentationCapture.RacingMap3: Expected 'The preview actually belongs to the selected mission' to be true.; Expected 'The authored close-map photo is fitted without extra UI cropping' to be true.
- Drone.UI.AllDesignerContract: Start action bottom-right anchor: The two values are not equal.; Start action common outer margin: The two values are not equal.
- Drone.UI.PauseSettingsCheckboxClickPIE: Pause VSyncCheck mouse click toggles immediately: The two values are equal.; Pause VSyncCheck mouse click is still applied 0.5s later: The two values are equal.
- Drone.UI.SelectUIPresentationPIE: Expected 'Start keeps the authored corner action size' to be true.; Expected 'Start chevrons retain full geometry' to be true.
- Drone.UI.SettingsCheckboxClickPIE: Title VSyncCheck mouse click toggles immediately: The two values are equal.; Title VSyncCheck mouse click is still applied 0.5s later: The two values are equal.
- KnownIssues.Flow.LobbyLayoutStabilityPIE: [DEBUG-lobby-layout] Probe requires the actual native-fallback FrontEnd BP Root and Slate
- KnownIssues.Tutorial.TrainingAssets: Expected 'Training Map has one Recon role test target' to be 1, but it was 0.; Expected 'Training Map has one Impact role test target' to be 1, but it was 0.
- KnownIssues.Tutorial.TrainingPIESmoke: Expected 'Training PIE contains a saved RecastNavMesh Actor' to be true.; Expected 'Training PIE Gate Sequence contains every spawned Gate' to be 102, but it was 92.

후속 재검사:

- Drone.Flow.GamepadMissionFlowPIE: Fail→Fail (FLOW_RECHECK)
- Drone.Flow.GamepadNavigationPIE: Fail→Success (FLOW_RECHECK)
- Drone.Flow.KeyboardStoryFlowPIE: Fail→Fail (FLOW_RECHECK)
- Drone.Flow.MissionEntryPIE: Fail→Fail (FLOW_RECHECK)
- Drone.Flow.PauseMenuRacingPIE: Fail→Success (FLOW_RECHECK)
- Drone.Audio.UserCombat.SpatialFar: Fail→Fail (EVIDENCE_RECHECK)
- Drone.Audio.UserUI.CountdownLifecycle: Fail→Fail (EVIDENCE_RECHECK)
- Drone.Audio.UserUI.HealthLifecycleAndMasterMute: Fail→Fail (EVIDENCE_RECHECK)
- Drone.Mission.ActualStoryStages.M1: Fail→Success (EVIDENCE_RECHECK)

## 실패 해석과 우선순위

- **재검사 결과**: 영상 옵션 없이 표준 시험 창 조건으로 분리한 9개 중 GamepadNavigationPIE·PauseMenuRacingPIE·ActualStoryStages.M1은 통과했다. 일반 패드/키보드 흐름2개는 최초 타이틀 포커스를 지나 브리핑의 시작 버튼 기대에서 실패했으며, 실제 강조 위젯은 FinishMissionBriefingButton이었다. MissionEntryPIE도 기존 실패가 남았다. WAV 수집3개는 새 프로세스에서도 동일한 수집/파일 내보내기 오류였다. 1차 실패43개를 보존하고 최신40개와 구분한다.
- **M4 데이터 불일치 확인**: 읽기 전용 조회에서 Endgame DA의 DefaultDroneId는 `Drone.GroundUGV.Greybox`였다. 현재 출격 정책은 초기 `Drone.FiberOptic.Greybox` 1종이며, 옛 TUT M4 검사는 DA 기본 기체를 직접 선택한다(DroneTutorialTUTMapsPIETest.cpp:258/277). 따라서 이 4개 실패는 허용되지 않는 UGV 선택부터 시작한다. 새로운 ActualStoryStages.M4는 현행 Fiber로 통과했다. DA 기본값과 현행 정책의 정합·세 시작점 실제 경로는 후속 대상이며, 시작점 UI 자체가 깨졌다고 확정하지 않는다. M3 DA 기본값은 Fiber다.
- **외형 자산 실패2개는 경로 문자열 문제 확인**: Scout/Fiber의 실제 본체·로터는 DroneSky 경로다. 검사가 기대하는 DroneSpy 6개 경로를 엔진으로 읽으면 모두 같은 DroneSky 자산으로 리다이렉트됐다. 실제 Scout6/Fiber5/Drop8 메시 집합은 해석된 기대 자산과 맞는다. 리다이렉트를 해석하지 않는 옛 문자열 비교가 실패한 것이며 메시 파일 누락으로 표시하지 않는다(ROLE_ASSET_READONLY.json). 자동 검사 판정 자체는 Fail로 보존했다.
- **실제 동작을 더 확인할 경로**: 옛 수업의 이륙/복귀/완료·결과 카메라 해제, Story M1/2 완료, M4 시작지점 선택 경로와 메뉴 최초 포커스·결과창 흐름. 최신 단계 검사 성공만으로 이 실패를 정상 처리하지 않는다. M4 옛 검사는 기체 선택/출격부터 실패한 뒤 시작점 위젯을 180초 기다렸으므로, 시작점 UI 자체의 고장으로 단정할 수 없다.
- **Training 맵 구성 차이**: `KnownIssues.Tutorial.TrainingPIESmoke`에서 저장 RecastNavMesh 부재와 Gate Sequence 92/102가 관측됐다. `TrainingAssets`는 역할 표적/화물, 전체 게이트 수와 프레임 메시 수에 옛 생성맵 계약을 요구해 실패했다. 팀원 제작 맵을 시험용으로 재생성하거나 저장해 맞추지 않았다.
- **확정된 오래된 기대**: `FlightProfiles`는 30m/s를 기대하나 현재 설정은 36m/s다. `StoryPresentation` 3개는 M3 ‘재밍 구역 이탈’/M4 ‘지휘 표적3개’를 기대하며 현재 ‘재머 파괴 후 추가 타격’ 정책과 다르다. 옛 StoryM3 검사의 목표1개 기대와 TutorialProgression의 수업 순서/준비 중 기대도 현행 정책과 다르다. 이 검사들의 다른 실패까지 모두 같은 원인이라고 확정하지 않는다.
- **모터/센서 전제**: `ControlLink` fixture는 모터를 켜지 않은 채 Move 입력 큐 생성을 기대하지만 현재 Move는 미시동이면 반환한다(DroneFlightPawn.cpp:2522). 옛 FPV 수업 검사는 시동 없이 뒤쪽 실제 충돌 기폭을 기대한다. 사용자 결정인 초기 지상 폭발 방지·좁은 전면 중앙 센서와 대조해야 하며, 검사를 맞추려고 생산 안전 조건을 제거하지 않았다.
- **UI 검사 전제**: TrainingPresentationCapture 5개는 루트 WidgetTree에서 사진/안내를 직접 찾는다. 현행 루트는 자식 Designer 화면 내부까지 찾는 FindDesignerPart를 사용한다(DroneFrontEndRootWidget.cpp:1555/1606/1659). 따라서 안내 위젯 대기는 실제 화면 미표시의 증거가 아니다. 레이싱 사진 Fit 기대와 현재 Fill 설정 차이는 별도다. 체크박스2개 검사는 스크롤 밖 항목의 크기0 위치를 클릭했고 Enter는 통과했다. 실제 캡처도 설정 상단만 보인다. 마우스 고장으로 단정하지 않는다.
- **START 검사**: AllDesignerContract의 앵커/여백 수치와 SelectUIPresentationPIE의 저장 크기·화살표 높이 기대가 실패했다. 반면 WideCameraMissionPresentation은 1280/1920에서 실제 START 우하단 기준선 일치를 확인했다. 저장 슬롯 수치와 표시 결과를 구분하며, 현행 크기가 디자인상 적절한지는 별도다. M1 캡처의 사진에는 명암·그림자가 보였다.
- **AI 검사**: ShotgunSystemsTestMapPIE의 추격 표적이 약199m 아래로 낙하했다. fixture에서 비행 시동이 없는 점은 확인했지만 추격 구현 결함 여부는 미확정이다.
- **표시 경고**: 게이트 `MI_DroneTrainingGate_02_Current`의 Nanite 사용 플래그, 케이블 `MI_cable`의 SplineMeshes 사용 플래그가 없어 게임에서 기본 머티리얼을 쓴다는 경고가 있었다. 이번에는 머티리얼을 저장·수정하지 않았다. 화면 영향 확인과 자산 담당 조정이 필요하다.
- **맵 충돌 경고**: Battlefield의 일부 콘크리트 방벽 spline 컴포넌트와 철조망에는 X축 Scale=0으로 유효하지 않은 물리 Body가 생긴다는 경고가 있었다. 이번에는 제작 맵을 저장하지 않았다. 경고만으로 사용자가 겪은 허공 충돌과 동일하다고 단정하지 않지만 실제 배치/충돌 검토 대상이다.
- **오디오 검사**: 실제 RacingMap1/StoryM4 이벤트 검사는 통과했다. 일부 WAV 증거 수집 실패는 소리가 실제로 안 난다는 판정과 구분한다. 후속 재검사 상태를 아래 표와 원시 JSON에서 따른다. 청감 확인은 수행하지 않았다.

모든 실패 원문과 1차 결과는 보존했다. 현재 코드/자산을 바꿔 검사를 통과시키는 작업은 이번 점검에서 하지 않았다. 물리 입력 주입/순간이동/자동 피해에 의한 성공은 손 조종 완주와 다르다. 실제 플스·InterLink 축/버튼 입력과 청감·독립 게임창·Cook/패키징은 별도 확인 대상이다.

Content 패키지9845개 기본 헤더 이상/LFS 포인터0개, 전체 Content 맵75개 중 프로젝트 저작 맵48개는 별도 SHA보호다. 헤더 검사를 모든 자산 로드/Cook으로 표시하지 않는다.

- Space 동반 갱신: 진행상황 sequence148·테스트 가이드 sequence92의 현재 블록2개 모두 applied 후 정확한 본문 readback 일치. 기존 Page만 수정, 기획/BP 가이드·공유 권한·Trello·예약은 변경하지 않았다. 로컬 원시 로그는 업로드하지 않았다. 이번 소스/자산·HEAD·Saved 최종 대조도 일치하며 Commit/Push 없음.

## 2026-11-04 — 전체 점검 실패 수선과 재검사

D PC Unreal `main 682852c5`·MD `main d955b5e`와 기존 로컬 변경을 보존했다. 사용자의 실제 문제 수선/낡은 검사 최신화/전체 재실행 지시를 수행했다. Commit/Push·Trello·공유 권한·예약 변경은 없다. 엔진/Build/PIE/자산 작업은 `/root/pilot_shortcuts_restart` 한 곳만 담당하고 Root가 결과를 통합했다. 물리/Tutorial·UI 담당은 지정 Source만 수선하고 준비 장벽 뒤 동결했다.

실제 수선: M4 저장 DA 기본UGV를 초기 FiberOptic 정책과 맞췄다. asset 변경 전 B01 T01에서 기대Fiber/실제UGV 오류 하나를 재현하고, 적용 후 새 프로세스 verify에서 재저장0으로 확인했다. Allowed/목표/미션맵·세 시작점을 보존했다. Gate Current MIC Nanite와 OilRig cable MIC SplineMeshes 사용 플래그만 개별 override로 수선했고 부모/스칼라/벡터/텍스처를 보존했다. 적용 자산은 이3개, 제작 맵 저장0이다. 실제 M4 기본/Start1~3에서 재머 전부 해제→새 전투 기체→Patriot 진행, 실제 M1 물리 배송과 FPV/M2 활성 전면 센서도 통과했다.

M1 Game World의 지정 Battlefield barrier/barbed-wire 계열 중 축 배율0인 section만 충돌/overlap/nav 기여를 끈다. 실제 M1에서5개 비차단·정상300개 보존, 전선18개 비차단·기둥23개 차단과 외형/배치를 확인했다. 원본 자산 로딩 Body 경고를 없앴다고 표시하지 않는다. 원본 맵/BP는 저장하지 않았다.

로비는 정확 게임 SWindow의 자연 present와 같은 epoch paint 기하로 확인했다. D02 global screenshot은 첫 장이 다른 Editor 표면/후속 phase여서 가시 첫 프레임 근거에서 제외했다. D03 실제 첫 UI의 부제목/구분선·본문·정보행 약21px 이동을 재현했다. D04 초기 preview 선채움으로 첫 진입은 해결했으나 실제 Down→M2의 긴 부제목에서 같은 겹침이 남았다. 최종 수선은 최초 배치 전 실제 preview를 채우고, NativeTick에서 preview가 실제로 바뀌는 분기에서만 layout prepass1회를 수행한다. Flow 선택/폰트/좌표/폭/Wrap·작성 WBP 변경0이다. START4곳의 실제1280/1920렌더는 기존2design-px 기준을 통과해 제품수선 후보를 폐기했다.

낡은 검사는 리다이렉터/현행36m/s·실제 모터 시동/재연결 interlock·현재8수업/목표/활성 damage capsule·비동기 결과 UI 완료·저장 child Designer/실제 스크롤과 마우스 hit path로 갱신했다. TrainingAssets는 별도 경량 TestMap, 실제 Production readonly smoke는 active92/sequence92와 동일기하 비활성10 및 실제 ground Nav consumer 조건을 검사한다. 경고 Occurrences0이 UE5.8에서 필수 출현이라는 잘못된 전제만 optional -1로 바꿨다. 로비의 정상 scroll/content-fit/화면 밖 미배치 항목은 실제 visible fixed geometry와 구분하고2px 허용값을 유지한다. 생산 물리/모터 안전을 단언에 맞춰 바꾸거나 목표를 강제 완료하지 않았다. 오디오3개는 같은-device silent submix 휴면 때문에 empty export가 났으며 process 대조→fixture 범위 cvar/원복으로 실제 PCM·파형·peak/loop/pause/mute/export를 유지했다. 청감 Pass가 아니다.

중간 실패도 보존했다. B01 집중F02는25완료 후 낡은 legend 열의 null 접근으로 중단돼 나머지12는 미완료였다. B02 TObjectPtr compile 오류와 B05 멤버명 shadow compile 오류는 test 단위 최소 교정 뒤 별도 새 Build로 진행했다. B03 집중22개 최종19성공/3실패와 D01~D04 원시 실패/첫 프레임 PNG는 최종 성공으로 덮어쓰지 않았다.

첫 전체 시도는471개까지 실행하고466실제성공/4실패/1스킵, 남은103미실행으로 원형을 보존했다. G03에서 승인된 M4 기본 기체 수선과 달리 `StoryPhysicsTestMaps`가 아직UGV를 기대하는1개 실패를 발견해 기대값 한 줄만FiberOptic으로 맞췄다. 나머지 맵·목표·그물/벽 단언과 제품 Source는 B08 이후 그대로다.

첫 전체 시도에서 CORE 실제284/CSV스킵1은 정상이나 FLOW의 패드·키보드 카드→START Down 경로2개가 실패했다. 반복 PIE 중 systemresolution metadata가 줄었고 패드 실행 구간에는1196×160이 기록됐다. 초기 조사에서 키보드 실패 시1190×86이라고 해석했으나, 실행별 timeline 재대조 결과 그 값은 다음 MissionEntry 검사 구간이므로 정정했다. 시스템 해상도와 실제 game viewport도 구분한다. UE5.8 PlayLevel.cpp의 OnPIEWindowClosed가 client 크기를 기록하고, EndPIE가 CenterNewWindow=false이면 그 값을 CDO NewWindowWidth/Height에 다시 넣는 경로를 1차 소스로 확인했다. 시작 때 크기를 한 번만 지정하던 낡은 Saved harness 전제를 보완해, 백업된 설정을 최종 원복하는 실행 범위 안에서 CenterNewWindow=true와 초기1280×720으로 크기 재사용 오염을 차단했다. 같은 DLL의 FLOW55 대조를 통과했고 V2 전체 재실행에서 실제 game viewport/CDO를 관측했다. LastSize는 Python 보호 필드여서 미측정으로 명시했다. 이후 원래 두 Down 경로를 추가 키/직접 focus 없이 검사했다. 이전 시도의 성공을 최종 전체에 합산하지 않았다. harness 원형/변형·해시·실제 창 크기와 실패는 실행 보고서에 보존한다.

전체 B09_FINAL_EXPECTED_M4 Build 39.58초 성공, DLL SHA256 `54194CD409C790F79086C7E19957474DE0CEA4A70DF13BEDE854BE76500FB9DB`. 이 B09·V2의 여섯 분야 새 프로세스에서 Editor 고유574개(작성 도구8개 제외)를 모두 실행한 원형은 실제568 Success·Fail5·외부CSV 부재1 Skip이다. CORE285/FLOW55/MISSION131/UI95/KNOWN3/MEDIA5 전부 포함, MEDIA5에만 영상 flag를 사용했다. 나침반1280의 정확client 크기 단언에서1274가 나왔고, 나침반 목표/표시 단언 오류는 없었다. ApprovedVisual4개는 이전 v1 PNG와 파일명 충돌로 실패했고 게임/기록/UI 판정 오류는 없었다. 제품·헤더·자산·V2 환경을 보존하고 테스트3파일만 수선했다. 나침반/Approved의 창 크기 setup을 실제 game viewport residual 보정으로 맞췄다. 최대3회/5초 안에 요청width/height를 정확히 만족해야 하며 원래 width 단언/모든 목표 검사를 유지하고 height 엄격 단언을 추가했다.

ApprovedVisual은 case·UTC·GUID invocation 폴더를 한 번 생성해 widget/owned viewport 캡처와 progress/record sandbox를 함께 격리했다. 기존 비덮어쓰기 단언을 유지하고 viewport 저장에도 추가했으며, 지연된 전역 screenshot 대신 실제 World 소유 창을 동기 캡처하고 전후 client 크기를 엄격히 확인한다. 같은 CLI stage의 Racing1920 반복1회도 별도로 검사했다. 구 v1 관측본30파일은 불변 대조했다. H04 이전 위젯 PNG14개는 원래 guard로 보존됐지만, 전역 screenshot16개는 H04 때 갱신됐고 이전 byte 백업을 찾지 못했으므로 그 원본 보존을 주장하지 않는다. 현재 관측본/해시와 원시 로그를 보존했으며 프로젝트 작성 자산·맵과는 별개인 자동 생성 캡처다.

B10 첫 fixture 빌드는 Approved의 double RoundToInt 반환 int64와 expected int32의 TestEqual 형식 불일치4곳으로 실패했다. 엔진/컴파일러0 확인 뒤 실제값4표현만 명시 int32 cast로 맞췄고 수치·허용값·판정은 바꾸지 않았다. 원시 실패 빌드와 다음 B12을 구분한다.

B11 Build14.76초와 영향8개 검사에서는 직접 영향6+AllDesigner가 통과했고 대표 KnownLobby만 첫 프레임 제목 할당 높이3.768design-px 차이로 실패했다. 같은 CLI의 Racing1920 반복도 별도 고유 폴더/JSON과 구v1 30SHA불변으로 통과했다. 원시 자연PNG18장을 보존해 제목glyph는 같고 아래문구가2~3px 움직임을 확인했다. 직접 실제client는1280×722로 요청720과 달랐다. UE shortest-side DPI curve와 SScaleBox 첫 normalizing prepass 근거를 대조하고, 제품 폰트/레이아웃을 바꾸기 전에 검사의 Opening host를 정확1280×720으로 보정했다. 양수인 같은 client/root paint scale의 서로 다른 두 자연 Title 프레임이 확인된 뒤 최초 Lobby 동작을 요청하며, Lobby 선행paint·첫샘플폐기·extraDraw/prepass·2px완화는 없다. 원래 모든 단언을 유지한 B12로 같은 순서를 다시 검사했다. 보호 prepass-scale getter는 Source적용전검토에서 제거해 미측정으로 명시하고 공개paint geometry scale/높이만 읽었다.

후속 B12_KNOWN_HOST_PRECONDITION Build 11.59초 성공, DLL `5CE2476F2C26F65C231EB3BAFBDA015463FF94D45EAF98E350843CB6FF971A3B`에서 영향 8개를 재검사했다. 제품 Source 동일성 SHA를 확인했으며 fixture 외 변화0이다. 최신 고유574개 판정은 **실제573 Success·Fail0·외부CSV 부재1 Skip**이다. `full_plus_targeted_fixture_recheck`로 전체 원형·후속 검사와 각test의최신stage/module을 보존했고, B12 한 DLL로 전체574가 통과했다고 표시하지 않는다. 이전시도471/C01/F06의 성공을 최종 전체로 합산하지 않았다. exact inventory 누락/중복/추가0이다.

최종 보존: 모든 맵75 SHA일치·Production Training 저장0·Content 예정 자산3개 외 변경0·기존 Antigravity/OSD 변경 보존·사용자 Saved8개 byte원복·알려진 임시 검사 슬롯 정리·엔진/컴파일러0. 원시/최종 보고서와 각 실행 START/END·해시 정본은 `D:/JGY/project/drone/Saved/Automation/GeneralFix_20261104/REPORT.md`, `RESULTS_FULL_B09.json`, `RESULTS_VERIFIED_CURRENT.json`, `FINAL_RECEIPT.json`다. private Saved/대용량 자산은 Space에 업로드하지 않는다. 실물 키보드/PS/InterLink 손 조종·청감·전체 미션 손 조종 완주·독립 게임창/Cook/패키징은 별도다. MD/Space 동기화 결과는 후속 영수증을 따른다.

MD/Drone Space 최종 동기화 완료: STATUS·WORKBOARD·세션 등록부·현재 가이드·known-fail 등록과 이번 WORKLOG를 갱신했다. STATUS27,184B·WORKBOARD29,797B(각30KB 이하), WORKLOG 기존 prefix SHA보존을 확인했다. 기존 진행 Page seq150/hash35b15997…와 테스트 가이드 seq94/hash65f31709…의 guarded 편집2건 및 exact readback2건을 확인했다. 가이드 edit의 중간 seq93 unknown outcome은 같은 stream readback으로 이미 적용을 확인해 재시도하지 않았다. 새 Page·로그/자산 업로드·공유/Trello/예약·Commit/Push는0이다. 영수증은 로컬 GeneralFix_20261104/ROOT_DOCS_RECEIPT.json·SPACE_SYNC.json이다.


## 2026-11-05 — Git 점검과 정리

사용자 요청은 Git 확인·정리다. 두 저장소 origin을 새로 fetch하고 실제 refs/index/worktree·변경 파일·LFS 본문을 대조했다. 이번에는 Commit/Push·Merge/Rebase·브랜치 삭제·reset/stash·엔진/Build/PIE를 하지 않았다.

- Unreal main `871e87054b84fa6c03e09870e45c54b12e46a985`의 로컬 커밋 `1104`는 62파일(+2367/−353)이다. 직전 미션4 기본 기체/미션1 충돌/재질/로비 및 검사 수선·기존 Antigravity/OSD/영상 변경을 포함한다. 현재 origin/main은 `fbd691e3ffa4226c5a3c967695145bfa575e1b6a`의 `261104`이며 공통 조상은 `682852c5`다. HEAD...origin은 로컬1/원격1이다. 11/04의 에이전트 무커밋 기록은 당시 사실이며 새 커밋을 에이전트가 수행했다고 표시하지 않는다.
- 원격 변경5개는 `Content/Drone/Maps/Missions/Lvl_Story03_VeilBreaker.umap`, `Content/Drone/Maps/Tutorial/TUT_Delivary_2.umap`, `Content/Drone/Maps/Tutorial/TUT_UGV_Turret.umap`와 기획 DOCX2개다. 로컬62개와 파일 교집합0이며 `merge-tree --write-tree --name-only --messages HEAD origin/main`은 exit0/충돌0, 예상 tree `4dffc830fa2a99a950f3737f04541cd2e11ddc79`다. 이는 미리보기이며 브랜치/index/작업맵에는 적용하지 않았다. 원격3맵 수신/적용 후 엔진 재검증은 별도다.
- 변경된 로컬 LFS11개(미션 DA3·MediaSource3·재질2·영상3)의 실제 파일 크기/SHA256이 각 HEAD pointer와 모두 일치한다. 처음 없던 원격3맵 LFS 본문만 범위를 한정해 fetch했고 모두 pointer 크기/SHA256 일치를 확인했다. 원격 LFS 다운로드와 로컬 커밋의 Push/LFS 업로드는 구분한다.
- B12 마지막 SOURCE_FREEZE의 Source/Config/Tools/RawInput732파일은 정리 전 모두 SHA 일치했다. 코드 동작 변경 없이 `Tools/AssetMigration/ConnectMissionBriefingMovies.py` EOF의 빈 줄1개만 제거했다. 기존 커밋에 대한 `show --check`의 단일 공백 오류를 발견해 작업본에서 수선했고, 최종 working diff check로 확인한다. 새 Build/자동검사 성공으로 표시하지 않는다.
- MD main과 origin/main은 `d955b5e99c37b08652c6fb2f0fcecd90622a1911`로0/0이다. 기존 미커밋9문서·staged0/untracked0/unmerged0을 보존했다. STATUS Git 기준·WORKBOARD Next·세션 현재 소유권과 이번 WORKLOG만 최신화했다. 이전 날짜 기록은 수정하지 않고 이 절에 새 사실을 추가한다.
- 현재 남은 Git 작업은 원격 맵/기획 변경을 로컬 수정과 병합한 뒤 검증하고, 요청된 경우 문서/공백 정리를 Commit/Push하는 것이다. 검증된 자동573/실패0/외부CSV 스킵1은 11/04 전체+집중 재검사이며, 아직 적용하지 않은 원격3맵의 통과로 확대하지 않는다. 실물 조종·청감·패키징 대기도 유지한다.

근거는 작업공간 `artifacts/git-20261105/GIT_AUDIT_INITIAL.json`, `TESTED_SOURCE_COMPARISON.json`, `GIT_AUDIT_FINAL.json`이다. 마지막 문서는 작업 후 상태를 기록하며 원시 초깃값은 덮어쓰지 않는다. 기존 진행 Space의 현재 단락만 guarded 갱신하고 결과를 별도 receipt로 확인한다. private Git 메타데이터/로그·대용량 본문은 Space에 업로드하지 않는다.

이번 진행 Space 저장 seq151·hash8acf3b1c…b1f003a와 같은 stream exact readback을 확인했다. Git 초기/최종 상태와 LFS14개 일치·두 저장소 diff check exit0을 영수증에 보존했다. 새 Page·Commit/Push·실제 병합은 없다.


## 2026-11-05 — 쉬운 조작 입력 중복 수선

사용자 제보: 놓으면 이전 위치로 돌아가고, 이동 중 조작이 끊기며 기울어지는 방향이 뒤집힌다. 최신 Drone.log는 M2 FPV/Drop 뒤 Tutorial.Hover Scout control0을 보였지만 실물 장치/원시축 기록은 없어 입력 장치를 단정하지 않았다. 사용자 병합/Push 이후 실제 HEAD는 Unreal main/origin0e405e6a·MD main/origin e24c5c0이고 시작 worktree/index는 깨끗했다. 이번 Commit/Push는 없다.

원인은 일반 FloatingPawnMovement의 입력 가속/소비와 교육 GPS 제어가 겹치던 순서다. 로컬 UE5.8 MovementComponent의 bTickBeforeOwner=true에 따라 이동이 먼저 입력으로 가속한 뒤 ConsumeInputVector를 호출했다. 뒤의 Pawn.UpdateTrainingFlight는 같은 입력을 못 보고 이전 유지점/제동을 적용했다. 기존 검사는 Pawn.Tick+직접 AddActorOffset만 사용해 이 실제 컴포넌트 순서를 놓쳤다. 세 후보(이중 처리→좌표 부호→유지점 갱신)를 세우고 첫 후보의 단일 변수 수선으로 같은 재현이 통과했다.

- B01 재현 검사 Build는 잘못된 WorldSettings include1건으로 실패했다. GameFramework/WorldSettings.h로 교정했고 원형은 보존했다. 제품 버그의 RED와 혼동하지 않는다.
- B02 Build11.12초 후 제품변경0의 R01에서 TrainingPawnRoleScope Fail. Scout/Drop 각각 전진 기수Z +0.412/+0.409, 해제6초 잔류속도202.633/204.051cm/s를 재현했다. armed1/link1, held 역주행0이다. 이 짧은 조건에서 원점 도착 자체를 재현했다고 표시하지 않는다.
- 제품 수선은 DronePilotFloatingPawnMovement.cpp/h 두 파일이다. 활성 교육 모델일 때만 일반 ApplyControlInputToVelocity를 건너뛰어 입력 소비/속도를 교육 제어기 한 곳이 소유한다. 이동 sweep/충돌·모터 안전·교육 Off/FPV Acro/UGV 경로·모든 게인/추력/항력/기울기 부호는 유지했다.
- B03 Build46.91초의 같은 원형 검사 R02는 Success. 기수Z −0.414148·해제6초 속도0.687cm/s로 바뀌었으며 기존4개 실패 단언을 완화하지 않았다. 원형 검사 SHA1808E32B…14C9를 RED/GREEN 모두 유지했다.
- B04 Build10.68초는 제품2파일이 B03와 같고 검사만 확대했다. R03_EXPANDED_EASY_12의 같은 DLL/한 프로세스에서 요청 고유12개 모두Success/실패0이다. Scout/Drop×(60fps0도·30fps0도·120fps0도·60fps90도)=8조건에서 held 역주행/중단0·앞/오른쪽 기울기·새 HoldPoint·3초 추가 중립·두 번째 이동·Space상승/Ctrl하강을 검사했다. 정지속도0.680~0.700cm/s이며 기존30cm 후퇴/정지속도 단언은 유지했다. 기존 GPS/ATTI·모드/축/짐벌/키 충돌·FPV실기모델·시동/착지·기울기·신호 연결 회귀를 포함한다.
- 실제 자동 명령과 원형/후속 Report는 Saved/Automation/EasyControlRegression_20261105/Runs의 각 RUNTIME.log·Report/index.json·END.json에 남겼다. 최종12개 test-state는 모두Success이며 report 경고 합계는 0건이다. 실행 전후 보존/원복은 실행 담당의 최종 영수증을 따른다.
- 실행 담당은 /root/pilot_shortcuts_restart 한 곳이고 Root는 엔진을 직접 실행하지 않았다. source허용범위는 제품2+기존 검사1이며 Config/자산/맵은 수정하지 않았다. 새 Saved 원본8개/맵75 기준을 사용해 11/04의 옛 백업으로 되돌리지 않는다. 실물 손 조종/기기 원시축·전체 미션 손 조종·청감/패키징은 이번12자동 검사에 포함하지 않는다.

최신 문서에서 사용자 완료한 Git 병합/Push와 이번 미커밋 수선을 구분했다. 11/04 전체574→573성공/0실패/외부CSV스킵1은 당시 리비전이며 이번 DLL 전체574재검사로 합산하지 않는다. MD/Drone Space는 관련 현재 절차와 결과만 함께 갱신한다. private Saved/로그·자산 업로드·공유/Trello/예약 변경·Commit/Push는 하지 않는다.

최종 보존 감사/문서 반영 확인: 11/05 원본 Saved8개 byte원복·맵75/보호29 SHA불변·Content9859 메타데이터불변이다. 실제 디스크 B02 동결732개에서 허용3파일 외729개 rawSHA일치를 확인했다. HEAD archive의237개 차이는 CRLF/LF만 다른 것으로 별도 증명했으며 원시 감사 실패/원문을 보존하고 코드를 재저장하지 않았다. 최종 엔진/컴파일러0·Source변경은 제품2/검사1·Commit/Push0이다. MD6문서와 Space 진행seq152·테스트가이드seq95 guarded수정/같은stream exact readback2건을 확인했다. 새 Page/공유/Trello/예약은 없다. 최종 실행영수증은 EasyControlRegression_20261105/FINAL_RECEIPT.json, 문서/Space영수증은 작업공간 artifacts/easy-control-20261105다.


## 2026-11-05 — GPS 좌표 복귀 제거와 사람 기준 이동

사용자는 쉬운 조작에 GPS 수평 위치 유지를 요청한 적이 없음을 지적하고 좌표 유지/옛 좌표 복귀 제거를 명시했다. 기존 제동·공기저항·관성·수평 복귀·착륙 보정은 유지한다. Mode1/2의 GPS 기반 이동은 기체 회전과 무관한 사람 시점 기준 전후좌우이며 제동과 별개라는 답을 확인했다. 이 절이 현재 계약의 정본이며 앞선 GPS 정지점 유지/복귀 성공 기록은 당시 시험 결과로 보존한다.

구현 경계: 수평 유지점 API/분기를 없애고 기존 속도 PI 제동·항력·추력/관성·고도/착륙 보조를 보존했다. 저장된 GPS enum 숫자는 호환으로 남지만 P-ASSIST로 표시한다. 사람 방향 보조는 기본OFF·Mode1/2·실제 ObserverLesson ViewTarget에만 적용하며 F/L3/RC Button3의 기존 ActionStarted로 ON/OFF한다. 키 설정3장치의 같은 행에서 재지정하고 raw 스틱 표시·Yaw/스로틀과 제동/비행/자세 모드를 바꾸지 않는다. 실제 Pawn 1인칭/추적 뷰는 거부·해제한다. 실제 사람 관찰 뷰를 보는 동안 숨은 Pawn FPV/DropCamera 플래그만 바뀐 것은 실제 뷰 전환으로 처리하지 않는다.

세션 분담: Root 통합/수정, no_gps_code_review 독립 검토·뷰 조건 수선, no_gps_docs_sync 문서/Space, pilot_shortcuts_restart 한 곳만 Build/엔진/자동 검증/원복. 이번 문서 세션은 코드·Config·자산·엔진·Build·Commit/Push를 수행하지 않았다. 기존 MD6WIP와 대상8문서 원본을 DocsPrep/BeforeDocs에 raw byte/SHA로 보존한 뒤 현재 절차를 갱신했다.

검증 근거: 최종 B02 Build15.59초 성공·R02_FINAL20 한 프로세스/동일 DLL. Build의 nonpreferred MSVC와 Engine SoundWaveProcedural C4996 경고는 남고 아래0은 자동 검사 경고 수다; 최종 관련 자동 검사 **20통과·실패0**(B02 최종 DLL의 관련20개 한 프로세스, 오류/경고/스킵0·명세 누락/추가0); 검사경고 0건. 실제 Scout/Drop World.Tick8조건에서 입력 지속·해제·외부변위(+700,-400cm) 뒤 미복귀·이동 중 방향반전·Space/Ctrl을 확인했다. 관찰Yaw37°의5역할×2모드×기체Yaw4×입력8=320조건에서 방향·입력길이·Angle축별 한도, 실제Scout/Drop 이동4조건과 공유키 ON/OFF/실제뷰 해제를 확인했다. 내부 조건수는20개 검사에 합산하지 않는다. 최종 module SHA 2743DA03028712714BD44144AFA1A9E8ED0CCDADE14B33078EC7D44995886237. 실행 범위는 B02 최종 DLL의 관련20개 한 프로세스, 오류/경고/스킵0·명세 누락/추가0이며 이전 first5/직전12개·11/04 전체574개와 중복 합산하거나 현재 전체 Drone.* 통과로 확대하지 않는다. 원시 실패/중간판/최종판은 각 실행 폴더에 보존한다.

보존: 현재 디스크 원본 기준 Saved8개 byte복원·맵75/보호29 SHA동일·Content9859 크기/시각동일. Source735→736은 허용 기존9변경+새검사1뿐이며 이전 Pilot2파일 byte보존. ROOT_KEEP_PHYSICS_PROOF의 UpdateFlightPhysics/착륙보정 함수 EOL정규화 본문과 교육 수치30개 동일. 엔진/컴파일러0. 최종 영수증 D:/JGY/project/drone/Saved/Automation/EasyNoGps_20261105/FINAL_RECEIPT.json; 보고서 D:/JGY/project/drone/Saved/Automation/EasyNoGps_20261105/REPORT.md. 실물 키보드/플스/InterLink 손 조작·전체 미션 수동 완주·청감·독립 패키징은 이 자동 결과와 별도다.

문서 배치: STATUS 현재 요약·WORKBOARD 해당 카드/Next·입력 계약·역할/물리·시험 가이드·세션 소유권을 갱신하고 결과 수치 전문은 이 절에만 둔다. 이전 WORKLOG prefix를 보존하고 기존 Drone Space 진행/시험 페이지의 현재 단락만 guarded 반영한다. 새 Page·로그/대용량 자산 업로드·공유/Trello/예약·Commit/Push는 없다. Space exact readback과 최종 파일 크기는 DOCS_FINAL_RECEIPT.json을 따른다.

Space 동기화 완료: 진행상황 페이지 seq153·시험 가이드 seq96의 기존 현재 단락만 guarded 교체하고 동일 content stream exact readback을 확인했다. 두 블록의 이전 Markdown 전문은 당시 리비전 원문으로 그대로 남겼으며 새 Page/비공개 로그 업로드는 없다. 최종 문서8개·원문 prefix 보존·30KB/링크·diff 검증 영수증은 로컬 EasyNoGps_20261105/DOCS_FINAL_RECEIPT.json이다.


## 2026-11-05 — 드랍 드론 3시점 선택

사용자 확정 요청은 드랍 드론 카메라를1인칭·3인칭·투하 중 선택하는 것이다. Root가 Drop 전용 선택flag/3값을 저장하고 미선택 때 기존 전역 시점→기체 기본값을 따르는 최소안을 승인했다. 전역 DefaultView enum을 늘리거나 비Drop·비행/착륙 물리를 바꾸지 않는다.

선택/입력 계약 정본은 [역할/카메라](../gameplay/DRONE_TYPES_AND_CONTROL_MODES.md#드랍-드론의-3시점-선택), UI 조정은 [설정/선택 가이드](../gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#드랍-드론-출격-시점-선택)다. 시점 선택은 즉시 Drop 전용 저장·재출격 유지, P/Triangle/RC13은1→3→투하→1이며 Secondary RMB/LB/RC12는 투하 진입/직전1·3인칭 복귀를 유지한다. 실제 Observer ViewTarget은 유지하고 수직 하방/FOV/충돌 보호도 보존한다. 설정 기본값 복원은 Apply 성공 뒤만 Drop 선호를 해제하고 Cancel/저장 실패는 이전 Drop 선택을 보존/복구한다.

소스: 최종 SOURCE_READY_B04의 제품8파일+새검사1을 raw SHA 대조했다. 초기 카메라 mount 적용/저장 시점 순서를 수선해 기존 Fiber 각도/재출격 assertion을 그대로 통과했고 이동/제동/물리값·입력 매핑은 바꾸지 않았다. 최종 구현/진단/검토는 no_gps_code_review, Root는 사용자 추가 지시대로 배정/관리/결과 취합, MD/Space는 no_gps_docs_sync, Build/엔진/자동 검사/PNG 직접 검토/원복은 pilot_shortcuts_restart 하나만 실행했다. 문서 세션의 코드/Config/자산/엔진/Build/CommitPush 변경0이다.

검증: B04 Build13.55초 성공·R04_FINAL17_RHI 한 프로세스/동일 DLL. 앞선 B01은 검사 TObjectPtr 컴파일 오류, B02/R01은14통과/3실패(Slate fixture2·실제 Fiber mount 초기화 회귀1), B03/R02는 입력 초기화가 빠진 fixture World.Tick crash였고 원형을 보존했다. B04의 InitInputSystem 수선 후 R03 신규2통과는 최종17에 더하지 않는다. 실행 담당이 실제 D3D12/1920×1080 PNG를 열어 새 행 글자/화살표·기존 버튼 정렬/스타일·카드/START 비겹침을 확인했다. 캡처는3D 미리보기 영역이 비어 있고 focus 전환 프레임이 없으므로 그 확인으로 확대하지 않는다. 아래0은 자동 검사 경고 수다; 관련 자동 검사17통과·실패0(B04 동일 DLL·R04 한 D3D12 RHI 프로세스·검사오류/경고/스킵0); 검사경고 0건. 최종 DLL SHA A5C923C3DFAF8E94E69764DFE00522D8C9556D9F9B41D949D65BBF9ACEA2995C. 원시 실행·선택 목록·보존 감사는 Saved/Automation/DropCameraChoice_20261105/FINAL_RECEIPT.json·REPORT.md를 따른다. 이전 GPS제거20개/first5·과거 전체574개 결과를 현재 리비전의 통과로 합산하지 않는다. 실물 손 조종·전체 미션 완주·청감·Cook/패키징은 별도다.

보존: 현재 디스크 HEAD5a08d015 원본 Saved8 byte복원·맵75/보호29 SHA·Content9859 크기/시각동일. Source736→737은 허용 제품8+새검사1뿐이며 이전 Pilot movement2파일 byte보존. 엔진/컴파일러0. MD는 HEAD e24c5c0의 기존8WIP/관련9문서 원본을 DocsPrep/BeforeDocs에 raw byte/SHA로 보존한 뒤 현재8문서만 갱신했다. 물리 정본은 이번에 수정하지 않고 WORKLOG 기존 prefix를 보존했다. STATUS/WORKBOARD는30KB 아래이며 Space는 기존 진행/시험/Blueprint카메라 단락만 guarded 갱신/재조회한다. 최종 문서·Space 영수증은 로컬 DOCS_FINAL_RECEIPT.json이다. 새 Page·비공개 로그 업로드·공유/Trello/예약·Commit/Push는 없다.

Space 동기화 완료: 기존 진행/시험/Blueprint 카메라 단락3개(progress seq154·guide seq97·blueprint seq103)의 guarded 반영과 동일 content stream exact readback을 확인했다. 이전 단락 전문·과거 실행 표현은 그대로 보존했다. 문서8개/기존8WIP·WORKLOG prefix412321B·30KB·링크/diff 검증 영수증은 로컬 DropCameraChoice_20261105/DOCS_FINAL_RECEIPT.json이다.


## 2026-11-05 — 정찰 카메라 고정과 맵 로딩 최초 표시

사용자 요청은 정찰 카메라의 원하지 않은 자동 들림/자세 추종을 고치고 맵 로딩 때문에 로딩창이 뒤늦게 뜨지 않게 먼저 빠르게 보이는 것이다. Root는 사용자 추가 지시대로 배정/관리/취합만 맡았고 카메라는 no_gps_code_review, 로딩 진단/구현·MD/Space는 no_gps_docs_sync, Build/엔진/실제 RHI·PNG/원복은 pilot_shortcuts_restart 한 곳만 실행했다.

진단 루프: diagnosing-bugs 절차로 test-only 원형을 먼저 실행했다. R01 로딩은 DA의 raw Auto분류를 Story로 해석하지 못한 fixture 준비 실패였으며 사용자 증상 RED가 아니다. GetLobbyCategory 정본/명시적 transient 분류를 고친 R02는 START→PreLoad11.9066ms 동안 자연paint/firstPresent/nonblankPresent0·제출프레임0으로 실제 증상 RED를 보였다. 가설은 도착 뒤에만 UI 생성→같은 프레임 이동→첫 UI 이미지 동기 로드→준비 후 강제 유지 순이며 예측을 먼저 공유했다. 원인은 첫 두 경계였고 수선 후 중간 R03은 자연paint63.0598ms/1프레임·present177.3789ms<PreLoad217.5ms·제출2프레임/비영730769픽셀로 GREEN이었다. 이는 해당 중간 리비전이고 최종 검사는 아래와 구분한다.

최종 소스: 이번 실제 디스크 baseline의 허용11경로(제품7·기존검사2·새검사2)만 바뀌었다. 로딩6제품/2검사와 정찰 Pawn/기존Mode2검사/새Scout검사는 독립 범위이며 읽기 전용 로딩 독립검토의 확정 차단결함0·최종739파일 raw SHA 일치를 확인했다. 카메라 계약은 [역할 정본](../gameplay/DRONE_TYPES_AND_CONTROL_MODES.md#정찰-카메라의-수동각과-자세-분리), 로딩/취소·편집 위치는 [UI 정본](../gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#시드-레이싱로딩일시정지-확인)을 따른다. 기존 Mode2 검사에 카메라 효과 전체가 OFF였다는 앞선 설명은 정확하지 않다. TrainingFlightMode Off라 문제의 짐벌 누설 경로가 비활성이었던 것이며 새 검사는 기본 짐벌/진동 효과를 유지한다. 새 정찰 고정 요구와 충돌한 Scout 기대만 갱신하고 Racer·Yaw 음성 대조·기존 오차는 보존했다.

검증: 최종 B04 Build10.31초 성공·R05_FINAL28_RHI 한 프로세스/동일 DLL의22clean+6warning Success=28. 경고13은 WASAPI RAW_MODE_UNSUPPORTED8·제3자 MOUT demo의옛 입력 참조4·외부 연결 확인 HTTP timeout1이며 무경고 결과가 아니다. Build에도 비선호 MSVC 안내가 남는다. 카메라 R02/R03 수동/시동 준비 실패는 input setup/reset 순서의 fixture 오류로 분리했고 B04에서 정상 초기화/실제 시동/수평 이동 조건을 보강했다. 로딩은 R01 준비오류와 R02 actualRED, R03/R04 중간 GREEN을 분리했다; 관련 자동 검사28통과·실패0(B04 동일 DLL·R05 한 D3D12 RHI 프로세스·오류/스킵0·경고13); 검사경고 13건. 정찰1/3인칭×쉬운/모드1/모드2의6조건에서 실제 시동 유지·수평 비행·수동 상하/해제·전진/놓음/반전·시점 왕복이 통과했다. 입력 예시는1인칭−22°/3인칭−12°이며 cache오차0,1인칭 최대 POV오차0.010°/자동상승0.008°·3인칭0°로 기본 미세진동은 남는다. 최종 요청→첫 자연 paint26.1675ms/1프레임, 실제 비영 backbuffer 제출72.2442ms가 PreLoad 진입97.9485ms보다 앞섰다(2제출프레임·730769비영 픽셀). paint26ms를 실제 화면 제출시간으로 단정하지 않는다. SWindow backbuffer1280×720은 제목줄을 포함하며 실제 GameViewport client 크기와 구분한다. 이미 관찰한 픽셀 PNG를 실행 담당이 직접 열어 로딩 제목/그림/TIP/문구/진행바를 확인했다. 별도 LoadingCancelPIE는 실제 Slate B→생성정지/닫힘→Flow/FrontEnd 복귀 경로를 통과했다. 최종 DLL SHA 5BC816F5ED54FB262EB6AD16E98715B53B8C2BB221AFC5FB2686EDB40BD0B1EE. 중간 원형/실패·카메라 준비 오류와 이전 Drop17/NoGPS20·전체574를 현재 통과 개수에 합산하지 않는다. 원시 보고서는 Saved/Automation/ReconCameraLoading_20261105의 FINAL_RECEIPT.json·REPORT.md·실행별 폴더다.

검사 기준 변경은 사용자 최신 요구에 따른 것이다. 기존 LoadingCapture는0.95초 최소 표시와0.4초 대기를 강제해 빠른 준비 완료를 실패로 보던 전제였고, 실제 ready/선택/닫힘은 유지하면서 그 시간 전제만 제거했다. 최초 표시 판정은 새 실제 public travel·자연paint/RHI·엄격한 pre-load시각/원시픽셀 검사로 보강했다. 첫 PNG는 SWindow backbuffer이며 실제 GameViewport client와 구분하고 transient Story clone→경량 맵 재현 범위다. 생산 미션 완주·실물 키보드/플스/InterLink 손 조종·전용 패키징을 확인했다는 뜻이 아니다.

보존: Saved8개 exact원복·맵75/보호29 SHA동일·Content9859 크기/시각동일. Source737→739은 허용 기존9수정+새검사2뿐이며 기존728/Pilot movement2는 보존했다. 기존 shared loading_story.png도 원본SHA로 복원했다. 엔진/컴파일러0·Commit/Push0. 이번 MD는 실제 기존9WIP/관련10문서 원본을 LoadingDocsPrep/BeforeDocs에 raw byte/SHA로 보존하고 현재8문서만 갱신했다. 물리/입력 정본은 이번 원본에서 변경하지 않고 WORKLOG prefix416432B를 보존한다. 기존 Space 진행/시험/Blueprint 단락만 guarded 반영/재조회하며 새 Page·비공개 로그/대용량 자산 업로드·공유/Trello/예약·Commit/Push는 없다. 최종 MD/Space 영수증은 로컬 DOCS_FINAL_RECEIPT.json이다.

Space 동기화 완료: 기존 진행/시험/Blueprint 관련 단락3개(progress seq155·guide seq98·blueprint seq104)만 guarded 반영하고 동일 content stream exact readback을 확인했다. 이전 단락 원문과 당시 수치 표현은 보존했다. MD8문서·원문 prefix416432B·30KB/링크·diff 검사 영수증은 로컬 ReconCameraLoading_20261105/DOCS_FINAL_RECEIPT.json이다.


## 2026-11-05 — Tutorial2 실제 하늘 시야와 자동 검사 범위 정정

현재 판정은 **미해결·실제 사용자 증상 RED 있음·제품 수정0·원인/수정 GREEN 없음**이다. 과거 정찰 카메라/로딩28통과를 Tutorial2 실제 흐름 확인/해결로 넓혀 보고한 범위를 정정한다. 그28개는 당시 격리 조건과 B04/R05 DLL의 유효한 기록으로 원문 보존하며 이번 결과와 합산하지 않는다.

### 실제 사용자 증거와 자동 재현의 차이

사용자는 첫 LOS 완료→Next→Tutorial2 START 뒤 지속 하늘 시야를 키보드/마우스·플스·InterLink 모두에서 보고했다. 최신 사용자 원본 화면을 독립 열람했다. embedded PIE Outliner는 TUT_Hover이며 정찰 드론·Mode2/P_ASSIST·모터 ON72%·고도17.4m·방위219°·속도12.2km/h·HUD시간00:28.27에서 땅 없이 하늘/구름만 보인다. 이는 실제 오류 화면이고 아래 별도 창 자동 검사와 조건이 다르다. 한 화면에서 private 카메라 캐시·실제 HID 보고·원인을 추정하지 않았다. 이전 “증상 RED 미확보”는 그 당시 자동 재현 상태였으며 최신 실제 사용자 화면 뒤의 현재 판정으로 재사용하지 않는다.

실제 saved FrontEnd/DA/맵, 기체 START/시작 안내/결과 Next의 Slate hit path, 새 Hovering World/Controller/Pawn/안내창, 저장 profile 복원을 검사 원고에 보강했다. 자동화 초기화 뒤 실제 DroneAudioSettings 슬롯을 메모리에 적용했으며 로그는 hasControl1/control3, hasView0/view-1, training선택0→첫 Pawn control3/training1/first1이다. 로드 실패 시 silent fallback이 남아 있어 향후 검사는 fail-closed 보강 대상이지만 이번 실행의 profile 로그는 일치한다. LOS 완료는 공개 목표 완료 함수 경계이며 실제 LOS 손 조종 완주가 아니다.

검사 SHA `EE588432E4ACC916ED23E86297AC3B04E565A7F77AA9CBC3C2C5122ECFC32E3E`, B06_SIDEBAR_EE5884 Build exit0, 동일 DLL `DD3E52CD8BE949AFC3F969F41085AD07ED2999A58B6C0017BEE0813F5ED4D65F`로 아래 고유2경로를3회 실행했다. 고유3검사나 전체 회귀 통과로 세지 않는다.

| 실행 | 조건/결과 | 초기 무입력 frames | 비행 max Pitch 오차 / onboard 거리 | 상승 / 수평 이동 |
|---|---|---:|---|---|
| R04_LOS_NEXT_EE5884 | LOS.Next, unattended RenderOffscreen RHI, Success | 402 | 0.010° / 85.310cm | 247.026 / 222.028cm |
| R05_LOBBY_EE5884 | 로비 직접, unattended RenderOffscreen RHI, Success | 442 | 0.010° / 85.242cm | 248.402 / 223.120cm |
| R06_LOS_NEXT_DISPLAYED_EE5884 | LOS.Next 일반 표시 창, unattended/offscreen 없음, Success | 271 | 0.010° / 85.493cm | 246.297 / 226.615cm |

각 실행은 오류0·경고5(오디오 RAW 모드 미지원1·MOUT 데모 옛 입력4), 모터49%·정상 합성 저장 키보드 시동/전진·해제/후진·해제/시점 왕복 범위다. 27개 PNG를 직접 열어 각7개 게임 화면, 총21개만 유효하게 채택했다. `hovering-paused-start-prompt`/`hovering-first-gameplay`는 세 실행 모두 검은 편집기 viewport여서 총6개 제외했다. 존재/바이트 단언이 잘못된 캡처 surface를 걸러내지 못했다. 초기 멈춤/재개 수치가 정상이어도 실제 최초 표시·일시정지 직전 화면은 미확인이다. 실제 PNG 완료/표시 frame도 직접 기록하지 않아 요청 frame과 구분한다. 유효21장에는 지면/장애물/지평선과 시점 복원이 보이고 지속 하늘 시야는 재현되지 않았다. 실제 사용자 embedded PIE의72% 화면을 이 결과로 부정하지 않는다.

R02의357 frames는 실제 Hovering 무입력·motor0/HID0 진입 통과이며 시동/장치 검증이 아니다. R01의 native window 클릭 실패·R03의 LOS 기대 시점/옛 Controller+새 선택ID 혼동은 fixture 실패다. B05 E91A3D의 보호 입력API2개 접근과 TObjectPtr auto포인터 선언 실패(exit6)도 카메라 RED가 아니다. 앞선 정적 검토에서 이 컴파일 오류를 놓쳤고 원본 검토본을 보존했다. 검사만 공개 GetEnhancedActionMappingsView·명시 PCM Get() 포인터로 수선해 B06을 만들었으며 활성 IMC 목록/우선순위는 미지원으로 기록한다. 실제 Pawn의 CameraTilt/CameraPitchRate/AcroGimbal 이름과 공개 매핑·카메라/기체 quaternion·현재/직전 PCM 캐시·throttle/viewport 상태는 기록했지만 private manual pitch 캐시 직접 값은 미관측이다.

PlayerInput mouse/pad/RC 값은0이었고 InterLink 연결 로그만 관찰됐다. 물리 HID 보고 도착이나 PS 등록/실물3장치 동작을 확인한 결과가 아니다. 다음은 현재 사용자 증상 세션을 배정된 실행 담당만 MCP로 읽어 World/ViewTarget/카메라/입력/포커스·장치 수신을 대조하는 것이다. 사용자의 열린 세션을 종료·StopPIE·Build·설정 변경하지 않으며 원인/최소 수정과 같은 실제 경로의 GREEN을 확인하기 전 해결로 바꾸지 않는다.

### MCP 연결과 자동 시작 설명 정정

공유 DefaultEditorPerProjectUserSettings.ini는 bAutoStartServer=False·8000·/mcp다. 옛 공유 True 문구를 현재 설명에서 정정했고 이번 Config 수정은0이다. 사용자가 ModelContextProtocol.StartServer를 직접 실행한 뒤 로컬 HTTP initialize/tools/list200, protocol2025-11-25·래퍼3/toolset23을 확인했다. Codex 네이티브 도구 노출 완료와 구분한다. 처음 질의는 FrontEnd였으므로 이전 오류 상태를 읽은 것으로 쓰지 않는다. ObjectTools 노출 속성의 한계, 임의 UFunction/Python/live Slate 입력/정상 종료 도구 부재, PIE is_dirty 오류와 중단된 전체 dirty 검색을 clean으로 판정할 수 없음은 [MCP 현재 절차](../git/DRONE_UNREAL_MCP.md)에 반영했다. 세션 토큰/개인 로그는 업로드하지 않았다.

### 보존과 담당

자동 실행 최종 인계 `ExecutionOwner/ACTUAL_ENTRY_EXECUTION_HANDOFF.json`과 `R06_FINAL_PRESERVATION_VERIFY.json`은 Source/Config/도구 포함740개 동결·최신 Saved9 byte복원·맵75/보호29 SHA동일·Content9859 파일 집합/크기/mtime 동일을 기록한다. Content 전체 bytes SHA 검사는 아니다. 기존 Drop/Scout/로딩·입력/물리 WIP와 Production Training을 보존했다. 실행자의 Source/Config/자산/맵 저장·Git mutation·외부 GUI 자동화는0이다. 자동 인계 때 engine/compiler0이고 이후 별도 사용자 Editor가 떠 있는 현재 상태와 구분한다. 문서 담당은 Source/Config/자산·엔진/Build/PIE/MCP 엔진/CUA 호출0이며 읽기 파일/PNG 검토와 MD/기존 Space만 수행한다. Commit/Push·Trello·권한·예약 자동화는 없다.

Root는 기존4개 사이드바의 배정·취합, 카메라는 검사/원고, 실행 한 곳은 엔진/복원, 물리는 독립 몸체/HID 읽기, 검증/MD는 독립 검토·기록을 담당한다. 근거는 로컬 `Saved/Automation/Tutorial2Camera_20261105`의 실행/보고서/이미지와 `Coordination/REVIEW_RUNTIME_R04_R05_R06.json`이다. 사용자 원본 오류 화면은 검증 산출물에 byte보존하고 Space에는 사실 요약만 반영한다.

MD7파일과 기존 Drone Space3페이지를 현재 실제 RED/미해결로 반영하고 저장 본문을 재읽어 확인했다. 진행 seq156·시험 seq99·Blueprint seq105이며 새 Page·이미지/개인 로그 업로드·권한/예약 변경은0이다. STATUS27863B·WORKBOARD29925B로 각각30KB 이하, 기존 WORKLOG422591바이트 원문 prefix는 그대로다. UI 모든 폭의 레이아웃 재검증은 아니며 Source/Config/자산·엔진 변경과 Commit/Push는 없다.


### 실제 증상 세션 MCP1차 읽기 추가

실행 담당이 보존한 ConnectedRead01 응답5개를 독립 파일로 읽었다. 13:59:40 KST의 TUT_Hover Pawn Actor transform은 Pitch/Roll0°, CameraManager **액터 transform**은 Pitch59.9993°였다. 이는 현재 세션의 실제 MCP 연결/노출 transform 관측이며 내부 최종 PCM POV·private 수동 pitch 캐시·입력값·HID 보고를 읽은 것으로 확대하지 않는다. 14:00:40 KST의 별도 Component 속성 읽기는 CameraBoom 상대 Pitch60°/arm0·FollowCamera 상대 회전약0/FOV69.7265°·CameraFlightPivot 상대 회전0이었다. Actor 읽기·Component 읽기·앞선 모터72% 화면은 서로 다른 시점이며 동일 프레임의 인과관계/수동 캐시 값/원인으로 단정하지 않는다.

원시 근거는 LiveUserRED_20261105_1357/ConnectedRead01의 PAWN_TRANSFORM.json·PCM_TRANSFORM.json·CameraBoom_VALUES.json·FollowCamera_VALUES.json·CameraFlightPivot_VALUES.json(각 HTTP200), 독립 영수증은 Coordination/REVIEW_LIVE_MCP_FIRST_READ.json이다. 최종 실행 담당 MCP 인계는 대기이며 제품 수정·GREEN은 없다. 현재 STATUS/MCP 설명과 기존 Space 진행 페이지에 이1차 범위를 반영한다. 문서 담당의 엔진/MCP 호출·사용자 엔진 종료/StopPIE/설정 변경은0이다.


### 실제 MCP 반복 관측과 runtime 입력 조회 거부 확정

ConnectedRead02의 원시 응답5개와 LIVE_READ02_SUMMARY를 독립 대조했다. 두 차례 모두 Pawn Pitch/Roll0°, Boom 상대 Pitch+60°, FollowCamera 상대 회전약0°, CameraManager 액터 Pitch약+60°였다. CameraFlightPivot 상대 회전0·Boom arm0/상속 Pitch·Roll false도 일치했다. 이는 노출 transform/상대 속성의 반복 관측이며 직접 Component world getter·ViewTarget·내부 최종 PCM 캐시·private 수동 pitch 캐시를 읽은 결과가 아니다. 요청별 timestamp가 달라 동일 프레임/화면 촬영 시점으로 합치지 않는다.

14:06:12 KST ObjectTools.get_properties의 실제 PC.playerInput 읽기는 transport HTTP200이지만 tool isError이며 “the following properties could not be read: playerInput”으로 거부됐다. InputReflectionProbe/INPUT_READ_CAPABILITY_RESULT는 현재 도구가 Edit/Blueprint 노출 플래그를 요구하며 Transient PlayerInput은 해당하지 않음을 소스와 대조했다. ActionInstanceData까지 RPC 실패를 관찰한 것이 아니라 PlayerInput 참조를 얻지 못했고 해당 runtime 값도 미관측이다. 따라서 현재 Mouse/Pad/RC·CameraTilt/AcroGimbal 값과 과거 camera delta 발생원인은UNKNOWN이다. 축0/장치중립/기본 RC 입력을 실제 원인으로 확정하지 않는다. 독립 근거는 Coordination/REVIEW_LIVE_MCP_FINAL_SCOPE.json이다.

카메라 담당은 RC 기본 짐벌 연결 최소 수정 후보·발생원인 bounded 로그·회귀 검사 원고를 준비 중이다. 빌드/일반 PIE의 실제 delta source 및 수정 GREEN은 아직 없다. 이전3회 자동 PASS를 반복해 원인/해결로 처리하지 않는다. 물리 담당은 비행축/스로틀/Mode1·2/사용자 명시 override 보존을 읽기 검토하며 엔진은 실행 담당 한 곳만 사용한다. 현재 사용자가 연 PIE를 종료·StopPIE·Build·저장/설정 변경하거나 예전 Saved9로 원복하지 않는다.

작성 이력 질의도 읽기 추적했다. GetIntendedAirframeTransform/UpdateAssistedStrikeCameraAim은 5ed30281a(10/23 17:55 KST, Git 작성자 gyeonliz)이며 FPV/광섬유·쉬운/게임 조작 조건 때문에 현재 Scout Mode2에는 적용되지 않는다. CameraFeel 짐벌 지연은 e053e38df(10/30 20:04 KST, gyeonliz·Claude Opus5.5 공동작성 기록), 현재 Scout 누설 차단은 그 뒤 기존 미커밋 WIP로 이번 RC 후보 수정과 구분한다. Mode1/2 AcroGimbal/RC Axis3 기본 연결은 b494b4f04(10/31 15:22 KST, 같은 공동작성 기록)이며 정상 카메라 입력 누적 경로는 실행 가능하지만 실제 원인은 미확정이다. Git 작성자/공동작성 trailer와 실제 타이핑 주체를 동일시하지 않으며 미커밋 개인 작성자를 추정하지 않는다. 상세는 Coordination/CAMERA_TILT_AUTHORSHIP_REVIEW.json이다. Git mutation은0이다.

이번 반복 MCP/입력 거부 범위의 MD·기존 Space 반영을 재읽기로 확인했다. 최종 진행 seq158·시험 seq100·Blueprint seq106이며 새 Page/권한/예약/개인 로그 업로드는0이다. STATUS28002B·WORKBOARD29884B, WORKLOG 최초422591바이트 원문 prefix 보존을 확인했다. 수정 원고/빌드/실제 GREEN 완료를 뜻하지 않는다.

## 2026-11-05 — RC 카메라 B07 실사용 확인과 충돌·수평 후속

- D PC Unreal `5a08d015`·MD `e24c5c0` + 기존 WIP. Root가 전달한 사용자 확인은 B07의 Tutorial2 InterLink에서 카메라가 자동으로 위로 돌아가지 않음이다. 이 특정 실사용 확인을 모든 장치/미션의 해결로 확대하지 않는다. 최초 하늘 RED의 실제 원시 입력과 과거 각도 누적 원인은 여전히UNKNOWN이다.
- 실제 B07 실행 영수증 `Tutorial2Camera_20261105/Runs/B07_RC_CAMERA_FIX/END.json`의 exit0·DLL `C002C75E4C3013637C7D697AEC729EAAADA5B36EE47E07B94B9A72FAE92D0E1C`와 R08 Report/index.json의 DeviceBindings5 Success/오류0/경고0을 읽었다. R07은 첫 WorldTick의 합성 Controller fixture에서 RC축 주입 전 접근 위반으로 중단돼 카메라 각도 회귀 판정이 없다. 제품 입력 실패나 전체 통과로 기록하지 않는다.
- 최종 test-only READY `FA0612F7D04765C6BDC12769DC626F70C67C754940EDCE4AC8905CBA449801C9`의9파일 SHA를 독립 대조했고 제품5파일은 B07과 동일했다. Lifecycle의 실제 RuntimeContext 적용 확인·effective mapping 비교와 종료 감시 Capture가 같은 포인터를 사용하며, 앞서 지적한1109행 수정/비const 선언을 확인했다. Lifecycle SHA `39605779BA6CDEBB661266FE370AD7E082253FB8F76482CFEA280509DF330FFA`. 이 정적 지적은 해소됐지만 수정된 RC/UI/Lifecycle/진입 검사의 새 Build/실행 결과는 아직 없다. 검토 정본은 `Coordination/RC_CAMERA_TEST_REPAIR_FINAL_INDEPENDENT_REVIEW.json`이다.
- 새 사용자 요청은 튜토리얼 숨은 벽/전봇대 전선 걸림과 M1 전선 허공 막힘, 간헐적인 중립 후 수평 복귀 실패다. 후자는 모드 표시가 그대로인데 기체가 기울어진 채 유지된다는 사용자 관측이며 모드 자동 전환은 확정하지 않는다. 현재 충돌 HitActor/컴포넌트와 수평 실패 원인/최소 수정/검증은 미완료다.
- 실제 Source의 기존 M1 전선 정책은 `Mission.Story.GoldenTime.Test`·GameWorld·선택 DA와 실제 World 전체 패키지 일치·출격 runtime placement 경로에서 정확한 `/Game/Battlefield/StaticMeshes/Props/SM_Wire_01.SM_Wire_01` 컴포넌트만 NoCollision으로 한다. `.Test`는 실제 M1 ID이며 실제 맵 `/Game/Drone/Maps/Lvl_Battlefield`를 TestMap 전용으로 해석하지 않는다. 튜토리얼 ID/다른 메시/볼륨과 일회 스캔 이후 생성 부품은 기존 적용 범위 밖일 수 있으나 이번 실제 원인으로 단정하지 않는다. 원본 BP/Mesh/맵 저장을 하는 코드가 아니다.
- 10/29 WORKLOG 원문의 실제 M1 wire18/pole23·중앙 simple/complex line/18cm sweep 기록은 당시 범위로 보존했다. 문서에 적힌 CameraCollision_20261029 원시 영수증은 현재 Saved 경로에서 발견하지 못했으므로 이번 새 원시보고서 검증으로 쓰지 않는다. 11/04의 degenerate5/정상300 보존도 해당 기록 범위다. 기존 검사는 모든 길목·몸체/로터/카메라 형상의 무차단을 입증하지 않는다.
- 소스 TUT 실제 경로 기대값과 디스크8맵 존재를 대조했다: LOS/Hover/Forward/CircleGate/FreeGate/FPV/Delivary_2/UGV_Turret. 저장 DA 전부를 엔진으로 새 조회한 것은 아니다. 실제 ID/전체 패키지/차단 부품과 프로필·채널·형상을 실행 담당이 수집하고 정상 목표/게이트/배달 overlap·전봇대/정상 이웃·지면을 보존해야 한다. Production Training 시험 저장/덮어쓰기/재생성은 금지한다. 정본 `Coordination/COLLISION_SCOPE_INDEPENDENT_REVIEW.json`.
- 기존4대화만 유지한다. Camera는 최종 test-only 인계 뒤 충돌 조사, Physics는 B07 기준을 보존해 FlightPawn.cpp/h의 수평 복귀 조사/최소 수정, 실행 한 곳만 엔진/Build/PIE/MCP/실맵 적용, Root는 취합, 검증/MD는 독립 읽기·기록을 맡는다. Root가 사용자 엔진 종료와 검사 엔진 준비를 전달했으며 문서 담당은 엔진을 조작/조회하지 않았다. 조사 인계 최신 사용자 Saved98을 보존하며 과거 Saved9로 복원하지 않는다. 이번 기록은 진행 상태이며 완료 처리가 아니다. Source/Config/자산/맵 변경·엔진 실행·Commit/Push·Trello/공유/예약 변경은 없다.

## 2026-11-05 — 카메라·공중 UI 입력·충돌 최종 검증과 전달

- D PC 검증 시작 Unreal main `5a08d01548dbc749bcd31bdf54b1b641fd806381`·MD main `e24c5c0dcd88bf7edc5ca66e7ceb302cd53452f3`와 기존 관련 WIP를 보존했다. 사용자 "다끝나고 나면 커밋 푸쉬" 승인에 따라 최종 검증/MD·기존 Space 동기화 뒤 관련 완성 변경을 선별 Commit/정상 Push한다. Source/엔진은 각각 배정된 담당만 사용했고 검증·MD 담당은 Source/Config/자산/맵을 수정하지 않았다.
- 카메라: 기본 InterLink 카메라축을 미지정으로 두고 명시적 할당/반전·비행축 재지정·IMC53행/저장 ID·키보드/패드 조합을 보존했다. 사용자가 B07 Tutorial2 InterLink에서 카메라 자동 상향 없음 확인을 전달했다. 최초 embedded PIE 하늘 RED의 실제 입력/과거 누적 원인은 여전히 미확정이며 PCM 액터 회전 관측을 내부 최종 POV/동일프레임 측정으로 확대하지 않는다. 초기 R07 fixture 접근 위반과 R08 입력5 통과, R09 수정된 RC/중립8 통과는 당시 모듈 기록이다.
- 공중 UI 원인 경로: B10/R13의 실제 Prototype PIE FPV3(DeviceRebind/KeyboardRebind/PauseResume)는 시동·공중 조건 성립 뒤 모두 모터 유지 단언만 Fail했다. control3/HORIZON2·스로틀 명령 before/after0.6512는 그대로였지만 motors0·초기 fixtureRoll20°가 남았다. 기존 자유비행 중립4조건은 정상이며 실제 원 사용자 직전 UI 조작이 확인된 것은 아니다. 따라서 원 사용자 원인 확정과 실제 재현된 생산 소프트웨어 경로를 분리한다.
- 수선은 UI 입력 해제와 명시적 모터 정지의 분리다. 이미 Armed/공중/링크 정상/출발대기 없음인 비행만 보존하고 RC 절대 스로틀은 마지막 유효값, 키보드/중앙복귀패드는 기존 hover 명령으로 정리한다. OFF/죽음/링크 손실/hold/점유·기체 교대·새 입력원의 low-before-arm 보호를 유지하며 stale armed 강제복구를 하지 않는다. 모드·실제 각속도와 LOS 방향 선택을 유지한다. DroneAcroFlightComponent SHA `816BA618ACA49500C8A6657686291A5D1E234FE2180DBD771817B24DBE84AC88` 불변이며 자세 수학·새 모델·GPS/게인/데드존을 바꾸지 않았다.
- 독립 검토에서 UI 정리가 영구 LOS-DIR 토글까지 끄는 회귀1건을 찾아 그 한 줄만 제거했다. 실제 Observer ViewTarget/공개 방향 ON의 전후 보존3조건을 추가했다. 임시 TraceCameraPitchInput/4호출·24/4 예산 필드는 제거하고 command getter/유효 회귀는 보존했다. B12/R15는 LOS3+안전/방향2만 실행됐고 기존 FPV3은 계층명 때문에 숨겨져 미실행이었다. 표시명 한 줄을 LOS.*로 옮기고 내부 명령/단언/제품 코드를 유지한 B13에서6건 모두 실제 실행했다. 이 중간5를 최종6에 더하지 않는다.
- 최종 B13_UI_TEST_NAMES_FINAL Build exit0, DLL `207C4A7FA1FAB2D9B0E24E7C3980BB1795887E3D33D3BCBD218160F73B1625B9`; D1286873A78263470C662C82A7439ED263559951268D50BEA234B43B0B6A2847 READY17파일 동결을 대조했다. R16_FINAL_UI_AND_REGRESSION은 같은 DLL의 정확28건 Success(일반18/경고포함10), 오류0/미실행0·경고17이다. 원 FPV3+LOS3 모두 motors1·스로틀0.6512 유지, LOS 선택/시점 유지·명시OFF 뒤 held-high 재시동 거부를 단언했다. UI후 짧은 관측의 Roll은 약7~9°로 복귀 중이며 이6건만으로3초 완전 수평을 단언하지 않는다. 별도 명시 RC 중립4조건/실제 Angle-Horizon, 카메라 RC·Mode2, 모터/장치 인계·착지, lifecycle/실제 LOS.Next 진입과 Native/Saved 설정 회귀도 이28에 포함된다.
- 별도 재사용: B12/R15의 CenteredSafetyLifecycle·ObserverRelativeMovement2건은 제품 코드 불변/표시명 한 줄 차이로 유지했다(DLL E51AFFF60F830E115E0A9AA1CB8C350489526CD15A4B3C98E994F86FE8C33484). B10/R14의 충돌7건은 helper/Controller/형상·채널·시험 관련6파일 불변을 확인해 유지했다(DLL 5A47ABE9E3223E9339A3AE5340F27EB0EDB50816C2229E87785259D803268333). 최종28과 이전9를 단일 DLL/단일 실행37통과로 표시하지 않는다. 이전 Drop3시점/Scout·로딩/NoGPS 완료 WIP와 원시 검증은 각 기존 절/영수증을 보존하며 새 실행에 중복 합산하지 않는다.
- 충돌 정책은 정확한 전선/케이블과 FPV 순수 물리벽만 런타임 해제한다. R14 실제 FPV PIE는 native cable20/벽16 retained NoCollision·기둥 유지와 정상 표적 파괴→Mission Success를 확인했다. M1은 실제 선택 Drop Legacy SphereComponent/Pawn 채널2로18전선의 simple/complex36경로에서 Visibility18/동일채널18/활성형상 모두 무적중,3폴대 몸통·상단을 포함48비교와 native 폴대 양성대조3을 확인했다. 전선18 NoCollision/기둥23 Blocking·0배율5 비차단/정상300 유지. 주변 액터를 숨기지 않은 조회이며 다른 적중을 곧바로 결함으로 단정하지 않았다. 추가 의도치 않은 M1 차단체는 특정되지 않았고 모든 길목/방향/기체·원 사용자 허공 막힘 완치를 주장하지 않는다.
- UE5.8 response 배열64칸과 ECC_MAX65의 차이를 놓쳐 M1 진단/제품 벽 필터가 인덱스64를 읽던 결함은 실제 배열 순회·유효채널/출력 개수 단언으로 수선했다. R14 7/7은 실제 채널2, 출력64개·0~63/유효응답만, 채널64/채널경고0을 확인했다. 이전 R12의64:16과 그 정적 검토 누락은 이전 원문/감사에 보존하며 최종 깨끗한 검증으로 소급하지 않는다.
- 경고/제한: 최종 R16 경고17=HTTP2/RHI 가상예산1/Audio RAW 미지원10/기존 MOUT legacy input Blueprint4. 사전 startup Condition failed15는 선택 검사 시작 전 진단이며 report오류0과 구분한다. 정확한 기원은 별도 추적되지 않아 무해로 단정하지 않았다. 재사용 R14 M1 경고61=convex39(MudTracks/지형Spline12 컴포넌트 범위·실제 노면 영향 미검증),0축스케일15(고유5 반복·런타임 NoCollision5/정상300 유지),Nanite/RT3,빈Nav2,Recast부재1,AudioRAW1이다. 후속48kHz2채널 초기화 성공과 실제 청감은 별도다. 로딩 형상 경고를 새 전선/폴대 적중 원인으로 연결하지 않으며 실물 HID·사용자 손 조종·청감·모든 미션/Cook/패키징은 별도다.
- 최종 실행·보존 정본: `Tutorial2Camera_20261105/ExecutionOwner/FINAL_ACCEPTANCE_HANDOFF.json`·`FINAL_PRESERVATION_RECEIPT.json`. 검증 담당도 현재 동결입력743·최신 사용자 저장99·맵75·보호자산29를 다시 SHA 대조해 차이0과 실제 DLL 일치를 확인했다. Content9859는 파일집합/크기/mtime 보존이며 전체 Content SHA 주장 아님. Production Training 저장0·소스/자산의 실행 담당 변경0·엔진/컴파일러0 영수증을 확인했다. 개인 저장·원시 로그·대용량 자산은 Space에 업로드하지 않는다.

- 전달 기록: 기존 Drone Space 진행/시험/Blueprint의 해당 본문3개를 저장하고 각각 seq160/102/108에서 기대 본문과 정확한 재읽기 일치를 확인했다. 게임 main `7771f5491d6734a599856d5aebbc28b5d1fd5c04`를 origin에 정상 Push했고 원격 refs/heads/main 일치·남은 tracked/untracked WIP0을 확인했다. 커밋34파일은 최종 동결 raw SHA 그대로이며 저장 blob은 CRLF→LF 정규화만 다른 것을 대조했다. Drop/Scout·로딩·NoGPS 기존 완성 변경도 포함했고 개인 Saved·로컬 RawInput Input.ini는 추가하지 않았다. MD12파일도 기존 관련 변경을 보존해 선별 전달하며 이 문서 자신의 commit hash를 기록하기 위한 순환 commit은 만들지 않는다. 최종 두 저장소 식별자와 원격 일치는 기존 Space 진행 페이지에 남긴다. 로컬 전달 영수증은 `Tutorial2Camera_20261105/Coordination/FINAL_DOCS_SPACE_HANDOFF.json` 및 `GitPrep/READ_ONLY_COMMIT_SCOPE.json`이다.

## 2026-11-06 — 전시회 독립 사본 Core 진행 검증

- 별도 사본 `D:/JGY/project/drone_ops_exhibition_20261106/Drone.uproject`, UE5.8. 원본 main `7771f5491d6734a599856d5aebbc28b5d1fd5c04`·MD main `7efbbf3922f1659e147d7ca7c0ea35fad9fc9fb5`에서 시작했다. 원본 Git clean을 재확인했으며 사본 작업의 Commit/Push·공유 변경은 없다. 이번 갱신은 Core 진행 기록이며 전체 완료 인계가 아니다.
- COPY_COMPLETE는10863파일/52871008436바이트 전수 SHA·독립 일반파일/하드링크 없음·원본 Saved77 보존을 기록했다. 독립 검토는 목록 SHA `B08C82CE1DF7196BBF9A8CB7DD1863A2185FCB4F4AA7521E1D025B48C0CCFE3C`·10863기록/ID 분리·실물10파일 SHA/ID/nlink1·신규 미디어2파일 SHA를 대조했다. 52.9GB 전체 해시를 검토자가 다시 실행한 것으로 쓰지 않는다. 이번 진행 검토에서 원본 Saved77 전체와 사본 사용자 설정/진행4파일 SHA·nlink1을 재확인했다. 옛99/98/9 epoch를 복원하지 않았다.
- 브랜드 READY SHA `A5F3D952B5BD3E6E4CCEF41471E979662E9CE62A97E367DF9575149A70BAF516`: 동결 Source/Config591 중5변경·586동일 및 원본591 SHA를 대조했다. 사본 전체5파일 변경이라는 뜻이 아니며 미디어·README·Controls·영상 비율은 별도다. 표시문자·창 제목 설정·native 로고16:9 중앙 맞춤을 확인했고 주석2/옛 번역조회키1은 보존했다. 내부 이름·저장ID·비행 물리·기체 DA는 유지한다.
- 신규 PNG SHA `BB458224C540ECF9E82F6D6890E71E9B258F3BB3AC5B4C7EEE693B42881C5E58`(`SourceArt/Brand/New_logo.png`,1920×1080), 메인 영상 SHA `FEE778AF4E1619C8EAAA6E9EFF2E7711FA182D2ABDFF57E3C35294EC0189F092`(`Content/Movies/Main_cinematic.mp4`,150555024B)를 실제 대조했다. 로고2자산 임포트 경로는 사본 내부다. E02D BRAND_READBACK은 Title/Lobby/Briefing의 oldBrand0 뒤 NoneType에서 중단된 FAILED로 전체 WBP 성공이 아니다. E04 크기 조회32×32와 PNG1920×1080은 구분해 소스픽셀/품질·화면 확인 대상으로 남겼다. 창 제목은 설정값 확인이며 OS 제목줄 전체 검증은 아니다.
- Controls revision3 READY SHA `D7F31D93E7EFAD808112B77FCFB11BCE8B2F68A69BF3565A10276F8206185D46`의7파일·영상 READY SHA `E1BBB74817B7BA9E171AA3B8F164E0E387B2C7021B83D14EB950AC2ADB813916`의 생산1/검사3파일을 대조했다. PSD3종은 디자인 참고이며 매핑/보정/RC 카메라 기본값을 가져오지 않았다.
- B02 Build exit0·E05 전후 DLL `119EB093969DE33386113204286E6E4F8D3C91A5FF6FF77D348A6B39528691AB` 일치. E05 Report/index.json을 파싱해23 Success(일반22·경고포함1), failed/notRun/inProcess0을 확인했다. WindowsEditor/D3D12_SM6·RenderOffscreen 실제 RHI 실행이다. 선택 보고서 경고1은 SavedWBP의 google generate_204 HTTP3초 timeout이다. Report SHA `87A02732F5B76ED0F60E8B8D191102260810631E6A3735C9B1FC9491D6D1DC0D`, Runtime SHA `69E6CF7A65C023F9B53AFC888CB9075E06C5E7D9D467DDB9E75EEA372EC8BF19`.
- 실제 부모 버튼→`/Game/Drone/UI/WBP/FrontEnd/WBP_DroneControlsSettings.WBP_DroneControlsSettings_C`·NativeFallback false/Designer 보존을 단언했다. Slate K 캡처·축 선택 Escape 취소·모달 확인/취소·3기기 pending 전달·부모 Apply 저장 요청 정확1/키·장치 payload·포커스 복귀를 확인했다. 마지막 파일쓰기 경계만 시험 대역으로 가로챘으며 실제 디스크 저장/재실행·실물 HID 전체 통과가 아니다. 키보드/패드/축팝업/InterLink 캡처4개는 이름1280과 달리 실제888×500이었다.
- 영상5개 메타데이터 SAR1:1을 확인했다. Main/M1 1920×1080, M2 3704×1722, M3 3622×1672, M4 3768×1696. 아래 실제 로그는 모두 contained1/centerError0.000이며 각 현재 뷰포트 기준이다. 1920×1080·1280×720 두 규격 완료로 확대하지 않는다.

| 검사 | 실제 VIDEO-ASPECT 로그 |
|---|---|
| Drone.UI.StoryBriefingMoviePIE.Mission2 | [VIDEO-ASPECT] file=Mission_briefing2.mp4 dimensions=X=3704 Y=1722 track=2.150987 rendered=2.150987 image=882.00x410.04 screen=882.00x428.00 contained=1 centerError=0.000 |
| Drone.UI.StoryBriefingMoviePIE.Mission3 | [VIDEO-ASPECT] file=Mission_briefing3.mp4 dimensions=X=3622 Y=1672 track=2.166268 rendered=2.166268 image=876.00x404.38 screen=876.00x422.00 contained=1 centerError=0.000 |
| Drone.UI.StoryBriefingMoviePIE.Mission4 | [VIDEO-ASPECT] file=Mission_briefing4.mp4 dimensions=X=3768 Y=1696 track=2.221698 rendered=2.221698 image=862.02x388.00 screen=876.00x388.00 contained=1 centerError=0.000 |
| Drone.UI.Mission01MovieInterLinkCancelPIE | [VIDEO-ASPECT] file=Mission_briefing1.mp4 dimensions=X=1920 Y=1080 track=1.777778 rendered=1.777778 image=679.11x382.00 screen=870.00x382.00 contained=1 centerError=0.000 |
| Drone.UI.Mission01MoviePIE | [VIDEO-ASPECT] file=Mission_briefing1.mp4 dimensions=X=1920 Y=1080 track=1.777778 rendered=1.777778 image=618.67x348.00 screen=870.00x348.00 contained=1 centerError=0.000 |
| Drone.UI.OpeningMovieInterLinkCancelPIE | [VIDEO-ASPECT] file=Main_cinematic.mp4 dimensions=X=1920 Y=1080 track=1.777778 rendered=1.777778 image=608.00x342.00 screen=864.00x342.00 contained=1 centerError=0.000 |
| Drone.UI.OpeningMoviePIE | [VIDEO-ASPECT] file=Main_cinematic.mp4 dimensions=X=1920 Y=1080 track=1.777778 rendered=1.777778 image=547.56x308.00 screen=864.00x308.00 contained=1 centerError=0.000 |

- Source/성공 검사를 대조했다. 메인은 실제1초 재생 후 Esc/InterLink 스킵·타이틀 버튼 포커스를 검증했다. 미션은 스킵 후 재진입해 M1은 실제 끝0.3초 전 seek, M2`4는 처음부터 실제 End 이벤트까지 재생해 timeout 아닌 종료·브리핑/포커스 복귀를 단언했다. 메인79.466초 전편 자연 종료·끝장면 새 로고의 실제 플레이 화면은 이 결과로 주장하지 않는다.
- 시각 검토는 Root/UI 담당 진행 중이다. PSD 대조·전체 화면/로고 품질·실물 조종·청감·Cook/패키징은 별도다.
- M3 실제 `/Game/Drone/Maps/Missions/Lvl_Story03_VeilBreaker`의 덮개형 팔레트 후보4개는 xiwcfassc_tier_2..5/StaticMeshActor_57·63·69·119다. 기존 target tag/health/damage 연결이 없고 사용자 유형 확인이 대기다. 실제 목표/맵 미수정, StoryCombatTargets200HP 최소 지원은 준비 중이며 Source동결·Build·검사는 별도다.
- 기체값은 FlightProfile과 Pawn/BP·사용자·역할 override에 분산되며 관성 텐서는 Racer FixedStep 시험 경로 한정이다. Source 연결·기존 정상 덤프·파일 보존 근거로 안내하며 저장 BP 최종 적용값을 이번에 새로 엔진 조회했다고 쓰지 않는다. 비행 물리 변경 없음. 편집·실행 정본은 UI/기체 가이드 전시회 절이며 진행 영수증은 `drone_ops_exhibition_20261106_handoff/MD_SPACE_CORE_PROGRESS_RECEIPT.json`이다.

- 후속 사용자 확정: xiwcfassc_tier_2..5의 기존 StaticMeshActor_57/63/69/119 네 개가 요청한 M3 팔레트임을 사용자가 확인했다. 유형 선정 질문은 해소됐고 실제 맵/DA의 2차 규칙·목표4개·체력/파괴·완료 조건 연결·검증은 실행 담당 진행 중이다. generic StoryCombatTargets200HP 지원 Source는 READY 인계대로 별도 Build/검사한다. 생산 Drop 폭탄 직접 명중1발 파괴는 실제 생산 경로 결과 대기이며 체력/명목 피해량만으로 확정하지 않는다. 앞선 후보/질문 대기 기록은 당시 상태로 보존하며 Core23 통과·시각 검토·원본 보존·전체 미완료·Commit/Push 없음의 경계를 유지한다.

- 추가 범위 — 드랍 폭탄 시각: 사용자 `C:/Users/Metacon_41/Downloads/드랍폭탄.zip` 모델로 드랍드론의 held bomb 시각을 교체하고 필요 시 dropped 시각도 일관되게 연결한다. 실제 입력 ZIP21754977B·SHA `11A1F0BE84CA4D28BAB36F02223559455491CCDCD14D9999B4C3DA2A8EAD7FB0`를 읽기 확인했고 원본 ZIP/프로젝트는 보존한다. UI 담당은 모델/재질·archive 조사, 물리 담당은 held/dropped Source 연결 읽기, 실행 담당만 정상 UE 임포트/참조 교체를 맡는다. 기존 피해·질량·항력·충돌·투하/소모·선택 프리뷰 숨김 보존이 조건이다. 새 모델 임포트·실제 적용·생산 폭탄1발 직접 명중은 아직 검증 전이며 Core23에 포함하지 않는다. 전체 작업 미완료·Commit/Push 없음.

- M3 실제 연결·단계/완료 후속 검증: B03 Build exit0, 별도 DLL `06C12A15179B03D5C86853AF28DE49596128696B44C8867FE5956CBF368C27B2`의 E07 지원6개 Success(오류0·경고0/미실행0)와 E11 실제 공개 경로를 확인했다. Core23의 DLL119EB093…과 다른 실행이므로 합산하지 않는다. E08A는 사본 DA_Mission_Story_VeilBreaker_Test·Lvl_Story03_VeilBreaker에 Objective.Story.M3.DestroySupplyPallets/TARGET_DESTROYED/Required4/Story.M3.SupplyPallet와 사용자 확정4개 binding을 저장했고 기존 첫 규칙/binding·액터 census3103을 보존했다. 새 E11 프로세스가 FrontEnd 공개 미션 선택/확정·실제 M3 이동→FiberOptic 선택/출격·재머 표준 피해 처리→Drop 전투 기체 선택/출격·시작 안내를 거쳐 실제4개 목표를 읽었다. 각HP200, 표준 GameplayStatics.ApplyDamage200으로3/4 ACTIVE·outcome NONE·completed false, 네 번째 뒤 FINISHED/SUCCESS·4/4 true·deathCounts[1,1,1,1]을 검증했다. 재머는표준 피해100000으로 처리한 fixture이며 손 조종/생산 폭탄 낙하/실제 명중이 아니다. E11 exit0·전후 DLL동일·originalOperations0·assetWrites0. M3_ACTUAL_TEST_EXPECTATION_FOLLOWUP에는 기존 actual M3 PIE의 포탑 전제 기대값 수선 필요가 남아 있으므로 해당 검사 전체 통과를 E11로 대신 주장하지 않는다. 새 폭탄 모델 임포트/재질/생성자 참조와 한 발 직접 명중은 진행 중·검증 전, 전체 작업 미완료·Commit/Push 없음.
- M3 원시 근거 SHA Execution\E11_M3_PUBLIC_FOUR_PALLETS\ACTUAL_M3_RESULT.json: 17F0438EF2DFAAAB9D3FF3836416C24863C556A728CD8991AEFE262D6E3FBA01
- M3 원시 근거 SHA Execution\E11_M3_PUBLIC_FOUR_PALLETS\RUNTIME.log: 73A888EDB410ACC0379BBA1DC488084BEE5D6785A9C694F2DAE019C7E85F5EE0
- M3 원시 근거 SHA Execution\E11_M3_PUBLIC_FOUR_PALLETS\END.json: 95B10D86CDB81E94F879C22CF8AADA04DAC798BA83BF63F670C5A0E34CBA5706
- M3 원시 근거 SHA Execution\E07_M3_SIX_SUPPORT_TESTS\Report\index.json: 732158518716684A59BF06C4025823E4F939D5552540EBD97C9E4701E22F9269
- M3 원시 근거 SHA Execution\E08A_M3_PALLET_ASSETS\ASSET_RESULT.json: 993C658689037A8892E83582B5E9047DB6EB8C5BAF59F9367218B944DF3DFCB5

- 생산 폭탄 직접 명중/시각 후속: B04 exit0·DLL `B14C719FD476F2BB052720004BD92C7D672DB7B2818A36716FBB56270D1771C2`. E09 모델 후10개 Success(일반8·경고포함2/오류·미실행0), 공기저항4개(FPS30/120·AerodynamicUnitsAndWeather·HighSpeedFrameParity) 포함. 경고66=Material61/Crowd2/StaticMesh1/Renderer1/ConsoleManager1. E09A는 같은 CombatDropActualStoryPIE.M3의 추가 재실행1개 Success/오류0·경고59(Material55+StaticMesh/Renderer/ConsoleManager/Crowd 각1)이며 별도11개 고유 통과로 더하지 않는다. Core23의DLL119…·M3단계/지원의DLL06…와도 분리한다. 관찰은 새 모델 Native DroneDroppedBomb_1→StaticMeshActor_57/xiwcfassc_tier_2 실제 직접 명중, rawDamage600·HP200→0·사망1·목표0→1/4·다른3팔레트 피해0·observerErrors[]를 기록했다. healthChanged의appliedDamageReported200은 HP에 적용된 감소량이며 raw600과 구분한다. 전체 검사에는 먼저 PIE-only 원거리 miss witness에 닿는 DroneDroppedBomb_0과 수동 교대 후 실제 목표에 닿는_1이 있으므로 전체 발사1회/손 조종/조준정확도 통과로 확대하지 않는다. hitIntendedTarget=false는 원시대로 보존하며 DroneDroppedPayload.cpp의 combat 분기가 OnPayloadImpact(this,HitActor,false)를 보내는 배달용 판정 경계임을 확인했다. 실제 유효팔레트 피격과 모순되는 오류로 해석하지 않는다.
- 모델 Source READY SHA `BE26E6A64ABFA7C13D4BA159C5FAAD674D88B79328C8BA9458C19E3086FCFB45`의2파일 currentSHA·역치환 beforeSHA·원본2SHA를 대조했다. 5자산 currentSHA와 E12A 새에디터 재읽기의782삼각형/1재질/추가 simple·convex0·PBR핀·2048텍스처를 확인했다. 실제 held mesh/material·scale0.08098·stock1 visible→stock0 hidden·Native visual NoCollision/0.75kg 기록이 있으며 원시 bounds에 기존35cm 보정을 적용한 크기는10.8572×10.8572×35cm다. 기존 held2캡처는 그리드만 보여 무효다. E13 최초 시각 probe도 unavailable begin_deferred_actor_spawn_from_class에서 FAILED이므로 게임뷰 성공으로 쓰지 않으며 올바른 재캡처/최종 보존 인계를 기다린다. 모듈·Source·자산·보존과 실제 시각 통과를 각각 구분한다.
- 신규 사용자 승인: ‘다 하고나면 원본에도 싹 적용해줘’에 따라 사본 최종 검증 후 원본 `D:/JGY/project/drone`에도 이번 변경을 반영하는 단계가 추가됐다. 원본 적용은 아직 미시작이다. 지금까지 원본 보존 기록은 해당 시점 사실로 유지한다. 변경대상을 먼저 백업하고 필요한 Source/Config/Content·미디어·SourceArt만 선별 반영한다. 원본의 최신 사용자 설정/키 보정·SaveGames·.git·캐시·Training 맵은 사본 것으로 덮지 않으며 사본의옛4설정 baseline을 원본 복원에 쓰지 않는다. 원본 반영·Build·검증은 사본 결과와 별도 기록하며 이번 승인에 Commit/Push는 포함되지 않는다. held시각·마지막 원본/다운로드/지속설정4·최종 Source/모듈 영수증과 원본 반영이 남아 있어 전체 작업 미완료다.

- 사용자 머티리얼 정정: 원본 `MI_xiwcfassc` 변경은 의도한 수정이 아니라 재질이 빠져 보여 만지다 잘못 저장한 것임을 사용자가 확인했다. 해당 자산의 기존 사용자 수정 보존/동기화 제외 방침만 철회한다. 실행 담당이 원본 적용 때 현재본을 먼저 백업하고 수정 전본·parent/texture 의존성을 확인해 해당 자산을 복구할 예정이며 실제 복구 전 완료로 기록하지 않는다. 과거 발견/보존 예정 기록은 당시 사실로 유지하며 원본 전체 reset·다른 설정 덮어쓰기는 하지 않는다.

### 원본 선별 반영과 정상 Fab 후속 검증

- 사용자 승인에 따라 A01에서 Source20·승인 Content/미디어/SourceArt26·실수 MI복구1=47항목을 현재본 백업 후 적용하고 byte 검증했다. 적용03:10:01`03:10:09Z. 최신 원본 Saved59는 적용 전후 일치하며 과거77개를 복원하지 않았다. 초기77→최신59 차이는 추가 원본 Editor 세션의 EditorPerProjectUserSettings 변경·CrashReportClient 추가/삭제를 포함한 새 epoch다. 원본 최신 설정/키 보정·SaveGames·.git·캐시·Training을 사본으로 덮지 않았다.
- Source20 독립 일치 인계와 Content27 독립 영수증 SHA `AC5DD672323E483B388138BE27E7A7F3EAB685C94CC911BC510032517BC2D82F`를 확인했다. Content는26+MI1/27성공·실패0, 원본 활성 재임포트 경로6개/MD5 일치·copy/handoff 의존0, B/N/ORM3개 초기해시 유지다. 옛 copy-root Factory_UID는 활성 SourceFiles 밖 임포터 이력으로 바이너리 치환/자산 재작성을 하지 않았다. 실수 저장본79D126…을 별도 백업하고 HEAD 실제 LFS payload=초기사본=현재사본402FAA…로 해당 MI만 복구했다. LFS pointer text를 자산에 쓰지 않았다.
- 원본 B01_NORMAL_WITH_FAB(실제 디렉터리 B01_ORIGINAL_WITH_FAB) exit0, BUILD.log Result Succeeded/100.14초·DLL `8C3262AC1E2FA7183A310C4D07C99E881ACD0CF8085B74737D4AE6866EFE12AC`. 컴파일 경고 발생행81=C4996 API폐기예정50/C4305 double→float31이며 고유 결함81개나 새 제품 실패로 세지 않는다.
- 원본 E02_CORE_SMOKE의 실제20 leaf 모두 Success(일반18·경고포함2), failed/notRun/inProcess0·오류0·경고51. DLL8C… 전후 동일·exit0·engineCompilerProcesses[]. 경고51=Material VT요구45/콘솔 스레드·시험Cvar2/Crowd RecastNav2/Nanite WPO-RT1/VSM1이다. 앞선 사본의 같은 자산/환경/시험 진단 범주로 구분하며 무해로 단정하거나 광범위 재조사하지 않았다. 원본20은 사본23·M3지원6·M3공개단계·모델후10·중복M3관찰1과 별도 실행으로 유지한다.
- 원본 정상 Fab E01의03:15:27Z 조회에서 /Fab/Materials/Standard/M_MS_Base 직접 로드·MI parent·B/N/ORM Texture2D3개·실제4 Actor 할당을 확인했다. Restored_Pallet_Material.png를 독립 열어 녹색 덮개·파란 끈·목재·기본 그리드 없음도 확인했다. E14 parentnull/실패를 최종 미해결로 남기지 않는다.
- 사본 B05_COPY_WITH_FAB 정상 빌드 Result Succeeded/4.81초(타깃 메타데이터 정리), Source586은B04동결과 동일·DLLB14… 유지. 양쪽 DroneEditor.target PluginOverrides=None을 읽었다. 사본 E15 정상 세션03:21:55Z도 parent·텍스처3·4 Actor 할당 로드 성공,03:22:10Z exit0/moduleUnchanged다. 이전 Fab 비활성 타깃/세션 기록과 분리한다.
- 사본 B04 Source/Config586개와 실제 DLLB14…를 독립 재해시해 일치, 맵75중승인M3만차이는 실행 보존 gate 범위다. copy 지속설정4개는 오늘 sealed baseline으로만 복구했다(시험으로 바뀐 MissionProgress1개 포함). 이후 양쪽 지속설정4개 SHA도 실제 재확인해 초기 사용자 값과 일치했다. 최종 전체파일/보존 영수증은 실행 담당 취합 중으로 별도 반영한다.
- E13D의888×500 held/낙하2장을 실제 열어 새 red/metal 모델이 기체 아래와 투하 후 게임뷰에 보임을 확인했다. 같은mesh/material·실제primary release·임시camera/고정배치시험이며 과거 그리드2장/E13 API실패는 무효/이전기록으로 보존한다. 캡처 SHA held4C251D…/falling48D71F… . E06C 종료/타이틀 시각은 카메라 담당 독립 인계 범위다. 메타데이터32×32 중간 조회/중단된WBP검사를 최종 시각 실패로 확대하지 않는다.
- 적용·Build·각 실행·시각·설정 보존 범위를 구분했다. 실물HID/손 조종·전 미션 완주·청감·Cook/패키징과1920/1280 두 규격 전체 검증은 별도다. 이번 Commit/Push·공유 변경은 없으며 검증/MD 담당의 게임 Source/Config/Content·엔진 조작0이다.

- 최종 완료 인계: OriginalSyncExecution/FINAL/FINAL_EXECUTION_HANDOFF.json의 ORIGINAL_AND_EXHIBITION_COPY_REQUESTED_CHANGES_APPLIED_BUILT_VALIDATED_AND_PRESERVED를 읽어 최종47항목 해시·양쪽 Source/Config586 동결 해시·양쪽 Fab비활성 타깃 override 제거·원본 최신 Saved59 정확 복구/보존·최종 엔진/컴파일러0·Commit/Push/branch변경0을 확인했다. 추가 CrashReportClient.ini2개는 세션 시작0.8초 후 생긴 정상 startup설정이며 해당2세션 END exit0/치명적로그0으로 원본 검증크래시 증거가 없다. 생성분2개만 외부 보관해 최신59를 보존했고 과거77은 복원하지 않았다. 사본/원본의 적용·Build·실행별 검사·재질/held 시각과 보존을 구분해 요청 작업 완료로 기록한다. 실물HID/손비행·전미션 수동완주·청감·Cook/패키징과 두 해상도 전체는 기존 한계로 유지한다. 최종 실행 인계 SHA256 3140AE9A6DFA50CC942CECF905CFA5EA94143A53CBE595D46AC6FDFABCFE2B52.


## 2026-11-06 — M3 런타임 경고 수선과 원본·사본 검증

D PC, Unreal 원본 `D:/JGY/project/drone`·전시회 사본 `D:/JGY/project/drone_ops_exhibition_20261106`의 경고 후속이다. 기존 전시회 반영/비행 설정 결과와 별도 실행으로 기록한다. 원본·사본의 로비 브랜드는 최신 사용자 지시대로 각각 유지했다. 이번 Commit/Push·Trello/공유 변경은 없다.

### 원래 51건과 실제 수선 범위

E02 원본 핵심20의 원시 Warning51을 report pointer/시각/원문/runtime 행으로 정확히 추출했다. AutomationController 재출력을 중복 계산하지 않았다.

| 원래 E02 경고 | 횟수 | 후속 처리 |
|---|---:|---|
| VT 타입 불일치 | 45 | 13 material-texture 조합. 정확13 texture의 `virtual_texture_streaming`만 false→true |
| 반복 `DisableAllScreenMessages` lookup | 1 | M3 Level BP Tick→명령 실행선1개 제거. BeginPlay·노드3개 유지 |
| Nanite instanced WPO ray tracing 미지원 | 1 | M3 embedded Nanite39그룹의 RT WPO만 false. Birch139+추가38그룹675855=총675994인스턴스 |
| VSM one-pass light overflow | 1 | 양쪽 DefaultEngine.ini `r.Shadow.Virtual.OnePassProjection.MaxLightsPerPixel=32` 채택/실값 확인 |
| Crowd/RecastNavMesh | 2 | 모두 BeginTearingDown 직후. 종료 시점 경고로 분리하고 플레이 중 AI 이동 결함/정상으로 단정하지 않음 |
| `r.MotionVectorSimulation` render-thread 안전성 | 1 | 엔진 TSR/CVar 계약 문제로 분리. 엔진 패치·경고 필터 없음 |
| 합계 | **51** | 실제 원인4종(원래48 event에 해당)을 수선하고 Nav2+엔진CVar1의 원래3 event 분류를 유지 |

VT 부모 sampler와 non-VT 텍스처13의 실제 읽기를 대조했다. sRGB/압축26개 값은 직접 전후 일치 확인했으며 다른 보호속성은 이전값 전체가 없어서 writer assertion 확인과 독립 재계산을 구분했다(`compression_none` API 미제공). 콘솔 수선 전후 Actor3103 snapshot은 byte 동일했다. foliage component의 전체 instance-transform hash/위치/재질/raster WPO/RT가시성은 유지했고 비 Nanite2그룹은 기존 RT WPO=true를 유지했다. 공유 mesh·전역 Nanite·ray tracing을 끄지 않았다.

W09에서 Birch 설정이 유지됐어도 warn-once 대상이 SM_Tree1로 바뀌었으므로 당시 전체 Nanite0으로 판정하지 않았다. 같은 미지원 조합을 M3 embedded 범위에서1회 census한 뒤 추가38그룹만 수선했다. VSM32는 fresh16 overflow1/fresh32 overflow0과 제품 M3 계약 통과로 채택했다. mask64→128bpp 차이의 이론 증분은882×462 약3.1MiB/1080p 약15.8MiB/4K 약63.3MiB이며 총VRAM 실측이 아니다.

### 실행을 분리한 최종 결과

| 실행 | 판정 | 전체 Report Warning event | VT/Nanite/VSM 원시 대상 |
|---|---|---:|---|
| E02 원본 핵심20 | 20 Success·오류0 | 51 | 45/1/1 |
| W01 사본 M3+v1읽기 | 프로브의 PIE 중 editor-world 조회 오류1로 전체Fail | 65 | 61/1/1 |
| W03 사본 M3 기준선 | Success·오류0 | 70 | 66/1/1 |
| W06 사본 VT·콘솔 수선 | Success·오류0 | 3 | 0/1/1 |
| W07 사본 fresh32 후보 | Success·오류0·실값32 | 2 | 0/1/0 |
| W12 사본 최종 | 6/6 Success(일반5·경고포함검사1)·오류/미실행0 | **1**, M3 종료Crowd | **0/0/0** |
| W13 원본 최종 | 6/6 Success(일반5·경고포함검사1)·오류/미실행0 | **2**, M3 TSR CVar+종료Crowd | **0/0/0** |

경고 포함 **검사1개**와 그 검사 안의 **경고 이벤트2개**를 구분했다. E02 전체20/Warning51과 최종 M3/UI6개를 숫자로 단순 비교하거나 다른 실행·모듈/반복 사례를 합산하지 않는다. 같은 사본 M3 W03→W06은 동일DLL/원시스캔에서 VT66→0, 반복lookup경고1→0, 명령로그120→1이었다. 최종 양쪽도 명령1회·반복lookup0이다.

최종6개 실제 이름은 `Drone.Mission.CombatDropActualStoryPIE.M3`, `Drone.UI.OpeningMovieContract`, `Drone.UI.OpeningMovieInterLinkCancelPIE`, `Drone.UI.OpeningMoviePIE`, `Drone.UI.OpeningMovieRuntimeSlots`, `Drone.UI.WideCameraMissionPresentation`이다. RuntimeSlots의 실제Initialize6조건은 이 검사1개 내부 사례이며 별도6개로 더하지 않는다. Main 영상 실제 재생/비율·Esc/우클릭 스킵을 확인했다. M3는 직접 재머 피해 setup·carrier hold/teleport·miss witness→수동 교대→실제 물리투하/표적 피해를 사용했으므로 손비행·전체미션 완주 인증이 아니다.

최종 live 읽기는 양쪽 실제VSM32, foliage41=Nanite39(RTWPO false, 총675994instances)+비Nanite2(기존true)를 확인했다. 사본 module `6C82CFDF9E3CE4FBEB61D1190C86842A8659D6785A6B21AB589F86E7D95418B5`, 원본 module `F73C771858A4140F786153E9E0DF9A602AF5A3ECACD49AC6AB99EAC69CE0D83B`로 구분한다. 최종 M3맵은 양쪽 `E6468B9BF3ABD3C2CFF88190316AA784B5E876BD48C571CAD3BD668C3BC96C70` 일치를 직접 확인했고 VT13/양쪽 INI32/선별7소스도 저장후해시와 일치했다. 원본 반영 전14개 백업은 변경전해시와 일치했다. 후속맵/7소스는 guard 뒤 선별 반영했고 기존 브랜드 차이는 유지했다.

별도 runtime 패널/Editor-only guard5개/새 slotstest의 총7소스는 사본 Editor B12 **14.27초**, 사본 Game B13 **28.36초**, 원본 Editor B14 **39.44초** Build Succeeded를 확인했다. Game compile 성공을 Cook/패키지 성공으로 표시하지 않는다.

### 남은 한계와 보존

최종 테스트 Report 오류0과 전체 엔진 세션을 구분한다. W13 Verbose에서 엔진 시작 smoke `FUnifiedErrorTest_CreateErrorMessage` 실패/Condition failed7, `FUnifiedErrorTest_CreateErrorMessageWithContext` 실패4, `FStructuredLogFormatTest` 실패4를 확인했다. 합계 엔진 smoke3실패/조건15오류이며 ExpectedError 정상 소비로 취급하지 않는다. 정적 소스는 `Engine/Source/Runtime/Core/Tests/Experimental/UnifiedError/UnifiedErrorTests.cpp:479,512`와 `Core/Tests/Logging/StructuredLogFormatTest.cpp:21`이다. UnifiedError11건은 한글 FText와 영문 TEXTVIEW 기대값 비교의 영향 근거가 강하지만 Culture A/B는 실행하지 않아 원인 확정으로 쓰지 않는다. StructuredLog4의 추가 원인 검증도 별도다.

최종 자동요청 Shot은659×183 Editor grid라 게임 시각 근거에서 제외했다. 매칭 그림자/GI/바람 이미지 A/B, GPU/pass·총VRAM, 실물 HID/손비행·전미션·청감은 미확인이다. 광선추적 변형을 끈 설정만으로 최종 외형 동일을 주장하지 않는다.

Cook 중 읽기 전용 지속설정 영수증은 이번 task baseline 대비 양쪽 각4개(`GameUserSettings.ini`, `DroneAudioSettings.sav`, `DroneMissionProgress.json`, `DroneTrainingBestLaps.json`) **8행 모두 해시 일치**, 프로젝트쓰기0이다. 이번 feature의 전체 Saved 기준은 원본59/사본34이며 과거77/초기사본4로 복원하지 않았다. 전체 Saved·패키지 최종감사는 P01 격리 UAT 이후 별도다. 현재 `P01_COPY_WIN64_DEV` 패키징은 진행 중이며 이 문서 갱신 완료를 패키징 완료로 확대하지 않는다.

근거: [최신 해결·실행 취합](D:/JGY/project/drone_ops_exhibition_20261106_handoff/FlightSettings_20261106/FINAL_NARROW_VERIFICATION.json), [원래51건 원문 분류](D:/JGY/project/drone_ops_exhibition_20261106_handoff/OriginalSyncReadOnly/WARNINGS51_CLASSIFICATION.json), `FlightSettings_20261106/W12_COPY_RENDER_UI_FINAL`, `W13_ORIGINAL_RENDER_UI_FINAL`, `WarningVT/WarningConsole/WarningInstancedNanite/WarningVSM32`, `PackageCode/Original`, `PERSISTENT4_READONLY_DURING_COOK.json`. 로컬 실행 자료이며 원격에 게시됐다고 주장하지 않는다.


### 새 사용자 범위 — 경고 완료와 전체 작업 분리

이후 사용자가 Downloads/ui_텍스트_수정사항.pdf 전항목 반영→DroneOps 최종 패키징→Google Drive 업로드→전체 완료 후 Commit/Push를 명시 지시했다. 경고 분야의 위 반영/검증/기록은 완료하되 전체 작업은 진행 중이다. 원본 Droner/기존 브랜드와 Ops 사본 차이를 보호하고 PDF 페이지별 체크리스트/완료 증거를 후속 취합한다. Commit/Push는 조건부로 승인됐으며 PDF·패키지·업로드 전에 실행하지 않는다. 최종 문서·Space 쓰기는 이 채팅이 계속 소유하고 실행 담당은 동시 수정하지 않는다. 패키징·전체 Saved 감사와 업로드 완료는 후속 영수증으로 따로 판정한다.


PDF 사용자 예외 확정: p10의 PDF4 표기는 사용자 지시로 기존13개 코스를 유지하고 안내 문구도13개로 수정한다. 게임플레이 게이트를4개로 줄이지 않는다. p5 궈장→권장 OCR정정과 p14 A04 실측9796.01m→약9.8km도 확정이다. 이는 구현/검증 완료가 아니라 UI 최종 체크리스트에 반영할 승인 결정이다. 기존 UI 소유 v2 체크리스트는 보존하고 문서 추적 보충 영수증 OriginalSyncReadOnly/PDF18_USER_DECISIONS_TRACKING.json에 old/new 문구·사용자 예외를 기록했다. 중간P01은 최종배포 대상이 아니며 PDF 후 P02와 업로드 확인을 최종 근거로 사용한다. 지정 개인Drive 계정/새DroneOps 배포폴더 준비는 진행 상태로 두고 업로드 완료로 표시하지 않는다.


## 2026-11-06 — PDF18 UI 검증과 최종 패키지 전 진행 상태

D PC 실제 보고서와 인계 영수증을 읽어 진행 상태만 갱신했다. 전체 완료·패키징·Drive 업로드·Git 완료가 아니다.

- 사본 T13은 M4+8TUT의 관련9개 Success와 로딩 fixture1개 Fail이다. B20 뒤 별도 T14 로딩1개 Success/경고5로 실제 LOS Entry/Back의 첫 자연 paint·비영 backbuffer present가 PreLoad보다 앞섰다. 서로 다른 모듈/실행을 단일10/10으로 합치지 않는다. T12 LOS 캡처 실패는 T13 LOS Success로 닫혔다.
- UI 담당의 frozen T13 27장+T14 2장=29PNG 검토 영수증 SHA256 7F249FA09599E3A54DBA5C92706A474A8062D5F088B2FA6B9329EE3FE232F242를 확인했다. 8훈련 Result/Next/최종Lobby와 M4 goal6/fullVEIL을 확인했다. M4 한 PNG에서 읽히는 표지는2개이며 실제6개는 검사 단언 근거다. 창 장식 포함1286×758과 실제 client1280×720을 구분한다. 실물 손비행·동일 세션8훈련 완료 증거는 아니다.
- 초기 HUD6장에는 Exposure -8.5의 Lumen/실시간 sky cached-lighting 범위 경고가 보였다. A10 native CVar4.0/VSM32를 읽었고 S07은 양쪽 DefaultEngine.ini에 CachedLightingPreExposure=3.0 한 줄을 적용했다(기대범위[-9,11], SHA256 DEF3F8DCF75E766F314980A2258FEA1B3B2479ECAC77B82F41D38097F8CB8905). 자동노출 끄기·화면/로그 숨김·렌더 기능 비활성은0이다. 후속 초기화면 확인은 아직 진행 중이다. M4 VSM 비Nanite marking queue overflow와 별개이며 shader 즉시처리 fallback 근거만으로 작업손실·GPU비용을 단정하지 않는다.
- 원형은 사용자 직접7승인이 아니라 총괄의 기존 실제코스7 유지 판단이다. A10은 Heading 보조정보/RuleDescription의9→7 두 텍스트만 바꿨고 이벤트/count/timeout/softMap/맵배치 변경0이다. 추가 사용자 선택을 P02 필수게이트로 두지 않는다. A10 FINAL_PDF_ASSETS19.json(B12BE9DB0B440A926DBD1C29D906042495F744A7422B0F27064032276648CF0D)→A11 원본 최종19개 반영 후 두 프로젝트 현 파일19개씩 SHA 일치를 독립 확인했다. 사용자 직접 확정은 복합 FreeGate13 유지다.
- 원본 B21 Editor Build Succeeded78.24초, T15 관련6개 Success/오류0(로딩 경고7·M4 경고3)와 native18자산 reload/보호Rule 일치를 읽고 현 파일18해시도 일치했다. 이 실행은 Circle DA 제외·Lumen 수선 이전이므로 최종19 재로딩/노출후 검증으로 쓰지 않는다. 원본 Droner 실제Story 캡처와 Ops 별도브랜드를 유지한다.
- 실행 담당의 B23 후 관련 초기UI 확인은6개 영향화면+Circle7·기존 대표M4/Racing1/메인 범위다. 전체goal/Result/Next 재검사로 확대하지 않고 완주/결과/Next는 T13 근거로 남긴다. 기존 카메라·입력 계약 및 실물 조종 미검증 경계도 유지한다.

남은 순서는 기존 관련 화면 확인→최종 보존/freeze→P02 패키징→선택한 개인Drive에 최종P02 업로드 확인→조건부 승인된 Commit/Push다. P01 업로드·Trello 수정·공유변경·예약자동화는 없다. 정본 추적은 handoff/OriginalSyncReadOnly/PDF18_COVERAGE_REVIEW.json이며 최종 문서 쓰기 소유권은 이 채팅이 유지한다.


## 2026-11-06 — P03 UI Cook 수선과 분할 Drive 배포 검증

D PC, 2026-11-06 17:45:24 KST Drive 완료 영수증을 기준으로 PDF/패키지/배포의 최종 내용을 갱신했다. 원본·MD Commit/Push는 아직 실행 전이며 전체 작업의 Git 단계는 대기다. 앞선 중간 기록의 P02 예정·Circle 사용자 미확정·Lumen 화면 대기는 당시 상태이고, 아래 현재 결과가 이를 대체한다. 과거 기록/동결 영수증은 수정하지 않았다.

- PDF18 관련 변경: p5 권장 OCR, p14 실제 호수Map2 9.8km, 훈련/드론 설명·결과/Next·훈련 Entry/Back·M4 VEIL6/full표시를 반영했다. 최신 사용자 답변은 원형 실제7개 유지·문구7개와 복합 실제13개·문구13개를 모두 확정했다. P03과 일치해 추가 재빌드/재패키징은 없었다. A10/v3가 당시 원형7을 총괄의 기존코스 보존 판단으로 기록한 사실은 역사로 보존한다.
- 실행 범위: T08 관련13개 Success 뒤 T09/T11/T12의 실제 실패를 보존하고 후속 결과로 닫았다. T13은 M4+8TUT9개 Success와 로딩fixture1개 Fail이며 B20 뒤 별도 T14 로딩1개 Success가 Entry/Back 첫 자연paint·비영present<PreLoad를 확인했다. 서로 다른 실행을 한 번의10/10으로 합치지 않는다. 원본 T15 관련6개 Success/native18은 Circle/Lumen후속 이전, T16 사본9개와 T17 원본2개는 InitialUiOnly로 완주/Result/Next 재검사가 아니다. 완주·결과/Next의 근거는 T13이다. 최종 원본/사본19DA native 재로딩·Rule일치와 양쪽 현파일 동일을 별도 확인했다.
- UI/렌더: T13/T14 frozen29PNG 결과 검토와 T16 신규10PNG 검토를 구분한다. Lumen 초기6HUD의 Exposure -8.5 범위 경고는 native기존4.0→Config3.0(지원범위[-9,11]) 뒤 관련화면에서 소멸했다. AutoExposure1/Quality2·VSM32를 유지했고 경고숨김/자동노출·Lumen끄기는 없다. M4 한 PNG에서 읽히는 fullVEIL표지는2개이며 실제6개는 자동단언이다. ContactShadows 무시설정, M4 비Nanite VSM marking queue/SurfaceCacheAtlas 및 GPU예산 미측정은 별도 잔여다. 엔진 startup smoke3실패/조건15오류, TUT 로그캡처 억제에 따른 raw경고 판단 한계도 보존한다.
- P02 실제 결함과 P03 수선: P02 N01 패키지에서 SettingsKit/T_Arrow_Left_Focus, T_Arrow_Right_Focus, TitleKit/T_BtnBox_Select_v3의 실제Cook누락을 발견했다. 두 프로젝트 기존UI텍스처 디렉터리2개에 좁은 AlwaysCook설정을 추가했고 C++/그림은 바꾸지 않았다. P03 N03은 세 fullobjectpath를 TEXTUREGROUP_UI로 실제로드했으며 SkipPackage/Failedfindobject/TITLE-KITfallback0이다. 새 Native실행은 hidden/offscreen 객체/로그검증으로 신규SettingsPNG가 없으므로 기존Editor육안검토를 대체하지 않는다. P01/P02는 Drive파일0·배포대상 제외, 내부 증거만 보존한다.
- 최종 P03: P03_COPY_FINAL_UI_ART_WIN64_DEV BuildCookRun Exit0, Native N03Front/N04M3는 격리사용자경로·timeoutfalse·exit0·Error/Fatal0이다. Report상 전체경고0은 아니며 N03 경고3(TSR/WASAPI/MotionVector), N04 경고4(같은3+종료Crowd)다. 영상5개 Stage byte/SHA일치와 ProjectContentDir/Movies 경로를 확인했다. 전체47파일 ZIP CRC·각Stage SHA, 최종Saved59/34·SourceConfig1180·브랜드14pair/프로젝트간브랜드차이5·19DA·Training27C2C0C2…/M3E6468B9B… 보존을 확인했다. 원본 Git HEAD는 이 단계까지 daa8dbaecd8e243642796ec2958318b356036687이다. 실물 카메라/RC 손조종·전체미션·청감·타PC코덱·GPU/FPS 인증이 아니다.

최종 ZIP은 DroneOps_Exhibition_20261106_P03_COPY_FINAL_UI_ART_WIN64_DEV.zip, 12,582,806,196bytes다.

- SHA256: 4e18721fb74beef652850768613a8a973a17c5bb475162ef0f3c8bb3a4948544
- MD5: 20eda5ce8e0bddb9b630048b73ff6f34
- 선택 개인계정 jkw6483@gmail.com의 [DroneOps 전시 배포](https://drive.google.com/drive/folders/1gKR8RwQjLfBhWMbDIeDMsBf7jHYQxzGf)에 96MiB이하 순번part125개와 복원지원5개, 총130파일을 배포했다. 모든원격ID/이름/크기/계정/parent폴더 대조·최종목록130개 일치/불일치0, 공유권한변경0이다. 단일 ZIP 업로드 완료로 쓰지 않는다.
- 로컬에서 동등ZIP을 실제복원해 SHA256/MD5·47CRC·추출47파일SHA를 확인했다. 이후 최종96MiB125조각을 순서대로 stream한 SHA256/MD5도 원ZIP과 같아 기존 동일바이트 복원/CRC/Stage근거를 재사용했다. 새125조각을 다시 추출/CRC 실행한 것으로 쓰지 않는다. 원격MD5는130개 모두 커넥터 미제공이므로 원격 체크섬 일치는 검증하지 못했다.
- 사용자는130파일을 이름변경 없이 같은폴더에 받아 Restore-DroneOps.cmd를 실행한다. 순서/크기/SHA/MD5·ZIP/해제47파일을 확인하고 새폴더로 해제한 뒤 Windows\Drone.exe를 실행한다. Windows 기본PowerShell/.NET/tar를 쓰며 Python/7zip은 필요 없다. 조각+ZIP+해제본으로 약38GB가 필요하고 기존출력 덮어쓰기/자동삭제는 하지 않는다. 복원지원은 DroneOpsDelivery.Common.ps1, DroneOps_P03_manifest.json, README_ko.txt, Restore-DroneOps.cmd, Restore-DroneOps.ps1이다.

정본 근거는 handoff의 FlightSettings_20261106/PDF_FINAL_VERIFICATION_v3.json(SHA1BC1FA25…), P03_COPY_FINAL_UI_ART_WIN64_DEV/{ZIP_READY,DISTRIBUTION_FILES,MEDIA_PORTABILITY,NATIVE_SMOKE_RESULT}.json, FinalPreservation_P03/RESULT.json 및 DeliveryPreparation_20261106/P03_DRIVE_DELIVERY_FINAL.json(SHAD02A8F0E84CC4DCA96F11B30248E724F436B865019F9D5AB3848A9B875BCC5EA)이다. v3의 ZIP대기 표현은 더 늦은 ZIP_READY/Drive완료 영수증으로 해소됐다.

이후 총괄의 별도 실행 지시에 따라 원본 Commit/Push→실제 Source SHA를 MD에 기록→MD Commit/Push→Space에 Source/MD 두 SHA만 작은 최종 갱신한다. MD에 자신의 Commit SHA를 다시 써 dirty loop를 만들지 않는다. 이 채팅은 Git Commit/Push·엔진실행·제품코드/Config/자산쓰기·Trello/권한변경·예약자동화0이며, 기존featureguide 변경과 과거 WORKLOG를 보존했다.


## 2026-11-06 — P03 원본 Source Commit Push 확인

원본 Source Commit/Push가 실제 완료됐다. 커밋은 8805ca55849f56837352529ff68abc744ef80445이며 기존 daa8dbaecd8e243642796ec2958318b356036687 부모를 보존했다. 총괄 인계는 LFS52/52 성공·실제 remote main/localHEAD 동일·ahead/behind0/0·오류/인증대기0이다. 이 채팅도 읽기전용 Git 조회로 HEAD와 origin/main이 해당 SHA이고 ahead/behind0/0임을 확인했다. 앞선 daa8 시점 스냅숏과 당시 Push대기 기록은 수정하지 않았다.

현재 MD의 Source SHA/원본Push 상태만 선별 갱신했다. MD 자체 Commit/Push 최종 결과는 Drone Space 진행 정본과 저장소 밖 Git 영수증에서 확인한다. MD 자신의 Commit SHA를 다시 본문에 써서 새변경을 만드는 동작은 하지 않는다. 이후 MD Commit 뒤에는 tracked MD를 재수정하지 않고 두 실제 SHA를 Space에 한 번만 반영한다. 이 채팅의 Git Stage/Commit/Push 및 이번 Space 변경은0이다.


## 2026-11-10 — 영상과 WBP, 미션 4 지도, 직선 게이트 검증

D PC에서 원본 `D:/JGY/project/drone`은 사용자가 Pull한 `6ea35be1cd410c8e8d72f05939ce71781bc99352`(HEAD·origin/main)를 기준으로 검증했다. 전시 사본은 `D:/JGY/project/drone_ops_exhibition_20261106`이다. 공통 변경은 저장 WBP 3개, M4 지도 텍스처, 이를 연결하는 코드다. 전시 사본에는 새 영상 두 편과 엔딩 경로를 추가했다. 원본 오프닝과 각 프로젝트의 로비 브랜드를 유지했다. 이번 변경과 문서 갱신은 로컬 상태다.

- **영상:** 전시 사본의 `Content/Movies/Main_cinematic.mp4`와 `Ending_cinematic.mp4`는 1920×1080·16:9, 각각 79.43초·17.93초다. 오프닝 끝 DRONER는 사용자 제공 원본에 있다. T08 3건에서 실제 WMF 오프닝/16:9·Esc와 격리 M4의 실제 Director 성공 → 엔딩 자연 종료 또는 Esc → 성공 결과를 확인했다. T09 파일 없음 1건도 같은 결과창을 한 번 열었다. T01의 엔딩 두 실패는 당시 fixture 이력이며 최종 결과는 T08/T09다.
- **Designer 키/START:** T04 사본과 T06 원본의 관련 4건씩에서 저장 `WBP_DroneControlsSettings` 순서 W/S → A/D → Q/E → Space/Ctrl → F와 재배치된 행의 Slate 포커스 추종을 확인했다. 실제 Space → K 재할당, 격리 프로필 저장·재로드, 탭·축 선택/취소와 반전을 검증했다. `StartPromptStartHintFit`과 `StartPromptStartHint`의 가로 중심은 `StartPromptStartButton`과 1280×720·1920×1080 모두 0.000px 차이였다. 실제 START 입력으로 정지가 해제됐다. 화면별 편집 위치는 [WBP 가이드](../gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#화면별-wbp-편집-정본)에 둔다.
- **M4 지도:** 내장 이미지 생성 요청은 출력 자동검토에서 `violence` 사유로 거절됐다. 실제 `Lvl_MilitaryCamp`의 v5 2048×1152 정사영을 채택했다. 초록 표시는 실제 착륙 패드 3개였으며 캡처에서만 제외했다. `T_M4_StartLocationMap` Brush와 세 StartId 월드 좌표를 `WBP_DroneStartLocation`에서 연결했다. 정사영 오른쪽은 +X, 아래는 +Y다. `StartLocationViewportFit`은 작은 화면에서 축소한다. T04 사본 초기 지도 시간 초과와 T06/T07 원본 Back·출격 실패는 그 실행 결과로 보존한다. 최종 T10 사본 1280×688 및 T11 원본 실제 PIE에서 핀↔목록, Back·재열기, 3번 출격이 통과했다. T14는 876×346 창의 실제 876×314 뷰포트에서 하단 Back/출격을 Slate 포인터로 눌렀다. Start3의 실제 XY는 13864.755, 20462.069cm이며 Z에는 기존 충돌 보정 21.302cm가 적용됐다. `Proof/Original/M4StartMap.png`와 `Proof/Ops/M4StartMap.png` 및 `M4_MapReference/Projection_Verified.json`을 함께 보관한다.
- **게이트와 사진:** 원본 실측 유효 코스는 직선 7, 원형 7, 복합 13개다. 원형/복합의 예전 숫자 기록은 당시 맵 이력이다. 직선 `TUT_Forward_Gate`, `DA_Mission_Tutorial_Forward`, `T_MissionPhoto_Tutorial03_Forward_2`는 수신 바이트를 사본에 선별 동기화했다. 직선 목표는 `TrainingLap` 1회다. T10 사본·T11 원본 모두 HUD `0/7`에서 7번째 게이트 후 완주·성공했다. 수신 DA의 `Thumbnail`과 `BriefingImage`는 처음부터 `Forward_2`를 가리켰다. 초기 바이너리 검색의 숫자 접미사 누락과 32×32 중간 읽기는 최종 UE 로드 증거로 대체했다. P09에서 1920×1080을 확인했고 새 참조를 만들기 위한 별도 DA 저장은 없었다. `FORWARD_PHOTO_RUNTIME.json`과 `FORWARD_GATE_GIT_ASSETS_SHARED.json`이 근거다.
- **최종 확인:** 원본 B10 및 사본 B11 DroneEditor Development 빌드가 성공했다. 기존 Saved 20개와 콘텐츠 21건을 해시 대조했고 시험 중 변경된 설정·슬롯을 복구했다. Production Training/M4 맵과 기존 P03 ZIP 해시가 일치했으며 임시 author를 제거했다. 시험은 실제 UE Editor·PIE의 Slate 합성 입력/격리 데이터 범위다. 실물 조종·청감·사람의 본편 완주와 이번 변경의 패키지 배포는 검증 범위 밖이다.

실행 정본은 `D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_OpeningEndingUi/IMPLEMENTATION_RECEIPT.md`와 해당 실행 Report, `PROTECTED_AND_SHARED_VERIFIED.json`이다. 11월 6일 P03 배포 및 Drive 130파일은 [당시 이력](#2026-11-06--p03-ui-cook-수선과-분할-drive-배포-검증)에서 확인한다. 아래 완료 카드는 현재 보드에서 이력으로 옮겼다.

| ID | 작업 | 당시 상태 | 완료 조건 |
|---|---|---|---|
| EXHIBITION-1106 | Ops 최종화 | P03·Drive·원본Push 확인 | MD 최종Git 결과는 Space/외부영수증 정본. [상태](STATUS.md) |


## 2026-11-10 — 지도 중심 시작지점 UI와 NPC 재장전 잠금

- **시작지점 UI:** 원본과 전시 사본의 `WBP_DroneStartLocation`에 지도 설계 1280×720을 적용했다. M4는 카드 줄을 접고 실좌표의 번호 1~3을 포인터·키보드·패드 입력으로 선택한다. 선택은 청록 채움과 짙은 숫자, 포커스는 크기로 표시한다. 편집 위치는 [WBP 가이드](../gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#미션-4-시작지점-지도)다. 원본 B02·사본 B03 Editor 빌드가 성공했다. T01 사본 2/2는 WBP 적용과 실제 지도 1280×688 검증, T02 원본 1/1은 876×346 창의 실제 876×314 뷰포트 검증이다. 번호 선택·Back·3번 출격과 XY 13864.755, 20462.069cm를 확인했다. T03 사본 1/1은 비지도 카드 선택 및 재출격을 확인했다. 양쪽 1920×1080 렌더는 해시가 같았고 작은 창은 원본 라이브 캡처로 확인했다. 실행은 Editor PIE의 Slate 합성 입력이다. 앞 절의 지도·목록형 결과는 당시 이력이다.
- **NPC 재장전:** 원본 B03·사본 B02 최종 Editor 빌드가 성공했다. 양쪽 `Drone.AI.RifleTrace`·`Drone.AI.ShotgunTrace`·`Drone.AI.WeaponContract` 3/3에서 게임 시간 2.19초에는 사격 차단과 탄수 유지, 2.21초에는 탄창 충전과 사격 복귀를 확인했다. 시작 신호와 완료 신호는 각각 한 번이었다. 재요청과 `StopFire` 뒤에도 완료 시각이 유지됐다. 부분 탄창 Shotgun 잠금과 초기화 시 타이머 취소도 검사했다. 시작 이벤트가 기존 모션을 호출하고 공통 `CanFire`와 사망·`EndPlay` 정리를 사용하는 경로는 코드로 대조했다. 실제 NPC 모션과 교전 중 AI 복귀는 수동 확인 범위다. [NPC 무기 가이드](../ai/DRONE_SMART_OBJECT_NPC_GUIDE.md#역할과-무기).
- **기존 실패와 보존:** `Drone.AI.PersonalWeaponMaintenanceTiming`은 RecastNavMesh 기대 경고가 발생하지 않아 실패했다. 원본 변경 전 T02, 적용 후 원본 T03·사본 T01에서 동일했다. 핵심 3건과 이 실패를 구분한다. 두 변경의 보호 영수증은 각각 기존 Saved 42개와 대상 파일 19건을 대조했고, 시험 설정·슬롯은 복구 또는 격리했다. 지도 임시 author 제거와 기존 애니메이션 해시는 최종 영수증에서 확인했다. 이번 검증은 로컬 Editor 빌드, 합성 입력 PIE와 컴포넌트 자동화 범위다. 실물 패드와 사람의 본편 교전은 수동 확인 범위다.

지도 정본은 `D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_M4MapFirst/FINAL_RECEIPT.json`, 화면은 같은 폴더 `Proof/Copy-1920x1080.png`와 `Proof/Original-Live-876x346.png`다. 재장전 정본은 `D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_NPCReloadLock/FINAL_RECEIPT.json`이다.


## 2026-11-10 — 맵 그물 배치 읽기 조사

원본과 전시 사본의 저장본에서 PBD 물리 그물 인스턴스는 각각 10개로 대조됐다. M1 Battlefield 8개, M4 MilitaryCamp 1개, Physics Sandbox 1개다. M1의 옛 표식 8개는 숨김·무충돌 상태로 별도 집계했다. M4의 `NetStrands`는 97개 인스턴스, Pawn Block·Camera Ignore이며 얽힘 켬과 접촉 절단 끔을 읽었다.

원본 A01 Editor는 요청 48개 중 47개 맵에서 Actor를 열거했다. `Lvl_DroneFrontEnd`는 Actor가 열거되지 않았다. 이번 범위는 저장된 배치와 설정의 읽기 조사이며 맵 저장 0회·PIE 0회다. 상세 위치·철망·사본 비교의 집계 경로와 원본 스캔을 함께 남긴다. [조사 집계](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_MapNetAudit/MapNetAudit.json) · [원본 A01](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_MapNetAudit/Original_A01/map_net_audit.json).


**후속 최종 확인.** 앞의 47/48은 A01 첫 패스 수치다. 외부 레이싱 맵 2개를 추가로 열었고 FrontEnd는 Actor Subsystem 열거 0개와 참조 레벨 0개를 재확인했다. 원본 PBD 10개 모두 반경 45cm Pawn Sweep에서 NetStrands를 적중했다. 원본과 저장본이 달랐던 전시 사본 훈련 맵 4개는 각 317개 철망 배치·충돌 서명이 일치했다. M4의 장식 메시 배치 562개는 철조망 241개, 천 덮개 184개, 노출 철망 76개, 기타 61개다. 정적 철망은 저장 콜리전 설정과 제한된 지오메트리 질의 범위이며, 실제 비행과 도시 생성은 별도다. [최종 조사 집계](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_MapNetAudit/MapNetAudit.json).


**디자인 관찰** 저장 상태의 Lit 캡처에서 M4-01 사선은 칸이 크게 벌어지고 세로줄이 휘어 보이며, 아래 지붕·철조망과 화면상 겹친다. M1-01 정면·사선은 상단 모서리 지지가 화면에서 분명하지 않고 차양과 겹친다. 검토 범위는 맵 편집과 실플레이 시뮬레이션 없이 촬영한 대표 장면이다. [M4 사선](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_NetDesignReview/V01_OriginalLit/OriginalPNG/M4-01_oblique.png) · [M1 정면](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_NetDesignReview/V01_OriginalLit/OriginalPNG/M1-01_front.png) · [M1 사선](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_NetDesignReview/V01_OriginalLit/OriginalPNG/M1-01_oblique.png)


**M4 저장 형상 수치** 앵커 폭은 12.18m, 저장된 NetStrands 표시 폭은 14.75m이며 중심은 가로로 약 3.79m, 아래로 약 0.79m 치우쳤다. 맵 인스턴스의 NetStrands 상대 위치와 가로 1.211배 배율이 이 저장 형상 차이를 설명하며, 런타임 초기화 후 화면은 별도 확인 범위다. [디자인 검토](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_NetDesignReview/Design_Review.md)


## 2026-11-10 — M1·M4 그물 디자인 수정과 PIE 확인

수정 전 디자인 관찰에 이어 원본과 전시 사본의 `Lvl_MilitaryCamp`·`Lvl_Battlefield` 두 맵 인스턴스만 변경하고 최종 저장 해시 일치를 확인했다. M4 양끝은 라디오탑·조명탑 지지면에 맞췄고 격자는 매듭 11행×25열, 줄 514개다. M1-01 좌상단을 컨테이너 벽 지지면에 맞추고, M1-05 하단 지면 여유를 조정했으며, M1-08 중앙 칸은 가로·세로 약 43cm다. [적용 영수증](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_NetDesignFix/Author_Receipt.json) · [최종 사본 동기화](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_NetDesignFix/EXHIBITION_FINAL_SYNC.json).

실제 미션 PIE에서 M4는 양쪽 모두 네 코너 변위 0cm와 가로·세로 순서 역전 0을 기록했다. 최종 표본에서 상·하변은 직선 기준 약 50cm 이내였고 최소 세로 칸은 원본 42.4cm, 사본 약 35.0cm였다. 1m 이탈과 역전 2곳은 중간 보정 이력이다. M1-05의 하단 63개 지면 샘플 중 최솟값은 양쪽 약 51cm였다. 근거는 PIE의 입자·줄 데이터와 지면 질의이며, 구도로 측정한 값은 아니다. [최종 원본 M4 PIE](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_NetDesignFix/Original_M4_Tuned/PIE_Receipt.json) · [최종 사본 M4 PIE](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_NetDesignFix/Copy_M4_Final/PIE_Receipt.json) · [원본 M1 포함 PIE](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_NetDesignFix/Original_PIE02/PIE_Receipt.json) · [사본 M1 포함 PIE](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_NetDesignFix/Copy_PIE01/PIE_Receipt.json).

비교 시트는 수정 전 저장 맵의 Editor Lit과 수정 후 실제 미션 PIE 드론 뷰포트다. 촬영에는 소유한 드론을 임시 PIE 월드에서 스크립트로 배치했다. 손조종 비행, 그물 접촉·포획 및 장시간 성능은 별도 검증 범위다. [수정 전후 비교 시트](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_NetDesignFix/Net_Design_Before_After.png).

## 2026-11-10 — 랜덤 도시 레이싱 무풍 적용

원본과 전시 사본에서 실제 로비의 랜덤 도시 `Lvl_ProceduralCityRaceTest` 게임 월드에만 전역 바람 벡터 0을 적용했다. 프로필 전환 후 최종 스냅샷에서 제한하므로 외부 바람 재정의와 프로필 돌풍도 이 월드에 전달되지 않는다. 시드가 뽑은 맑음·흐림·비, 조명, 비 Niagara와 도시·코스 생성을 사용한다. 로딩 단계는 ‘날씨 정하기’, 결과 조건은 시드와 날씨를 표시한다. 양쪽 맵·미션 DA는 원본 Git LFS 해시와 일치했고 대상 소스 5개도 양쪽 해시가 일치했다.

D PC Editor Build B11 원본·B12 사본 모두 성공. 원본 T17은 선택 4/4, 사본 T18은 6/6, 원본 대조 T19는 3/3 성공이며 선택 보고서 오류·경고 0이다. T17/T18은 실제 로비에서 시드 424242로 출격, 맑음·흐림·비 월드 풍속 0, 비 강도 0.80, 빈 옵션에서 외부 7 m/s 주입 후 위치별 풍속 0, 같은 시드 도시·게이트·날씨를 확인했다. T19는 별도 맵과 건물 차폐·자동 보정 회귀를 확인했다. 시작 단계의 별도 엔진 진단과 선택 검사 결과를 구분한다. 기존 SaveGames와 Editor 설정을 검증 전 파일과 대조했다. 실물 조종과 패키징은 이번 검증 범위 밖이다. [실행 영수증](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_RandomCityCalm/FINAL_RECEIPT.json).


## 2026-11-10 — 원본·전시판 Win64 최종 패키지와 개발 사본

- D PC UE 5.8. 원본과 전시판의 로비 브랜드를 각각 확인하고 기체 속도 칸에는 모드에 따른 차이를 표시했다. FPV·스카이드론 설명을 다듬고 배터리·바람 HUD 행과 M2의 바람 무전 문구를 정리했다. 랜덤 도시에서만 무풍을 적용했다. 훈련·일반 미션의 기존 바람 프리셋과 배터리 소모·재출격 계약은 유지했다.
- 두 Win64 Development BuildCookRun이 종료 코드 0이었다. 각 Cook 5,213개, 오류 0건, 경고 59건이며 누락 패키지 경고는 발견되지 않았다. 배포용 IoStore에서 필수 자산 52개씩과 원본 영상 5개·전시판 6개의 소스 바이트 일치를 확인했다.
- 두 최종 바이너리에서 실제 로비와 Designer 설정·축 선택, 레이서 문구, 훈련·M2의 배터리/바람 행 접힘과 타이머/내구도, M2 무전, M4 지도 3번 출격, 시드 424242 코스 및 332 무풍·활성 비 Niagara를 확인했다. 전시판 엔딩은 성공 이벤트를 주입해 영상 열기·비율 맞춤·건너뛰기 뒤 성공 결과를 확인했다.
- ZIP은 모든 항목을 실행 폴더와 CRC·SHA-256으로 대조했다. 전체 백업과 정리 사본은 독립 데이터 복제이며 삭제 후보는 Cook 목록·Asset Registry·코드 참조를 대조했다.
- 드로너 원본 ZIP 12,592,938,592바이트, 47개 항목. SHA-256 `909e5079d06f0cd01ed506dc0392f657bca106331a974bc7026538bd622ee650`, MD5 `d7e86499b63bc3b8d876ac9b07c3f7ff`. 전체 백업 10,745개 파일. 정리 사본에서 확인된 데모 에셋 8개(7,933,738바이트)를 격리했고 두 사본에서 각각 실제 맵 8개를 열었다.
- 드론 옵스 전시판 ZIP 12,626,301,506바이트, 48개 항목. SHA-256 `9cff1356295fe935eeb121968732941f843bc2980e63739d424fbf85bf34fb00`, MD5 `d358cd07a6341617dc9cc69a1ea9c212`. 전체 백업 10,747개 파일. 정리 사본에서 확인된 데모 에셋 8개(7,933,738바이트)를 격리했고 두 사본에서 각각 실제 맵 8개를 열었다.
- 원본 `origin/main` `cb07840a6e338411c43c7fb95342c7b13d30c321`의 변경 26개를 푸시했고 LFS 5개를 원격에서 새로 받아 크기와 SHA-256을 확인했다. 승인된 M1·M4 그물 맵은 사전 검증 영수증과 두 원본 파일 해시가 일치했다.
- 사용자 Saved 설정·저장 데이터는 원본 41개와 전시판 28개의 기준 해시를 복원했다. 콘솔과 격리 진행 파일을 사용한 자동 실행이며 전체 미션 손 조종, 실제 장치, 엔딩 자연 재생 종료는 이 확인 범위와 구분한다.
- 최종 검수에서 현재 두 실행 폴더와 ZIP의 전체 항목 경로·크기·CRC 메타데이터, 두 런처와 네이티브 실행 파일, 영상 5개·6개, 기본 및 확장 실행 로그의 SHA-256을 각 영수증과 대조했다. 개발 사본 네 곳의 실제 파일 수·용량과 Editor DLL 해시, 정리 사본에서 격리된 8개 각각의 전체 백업·격리본 해시를 확인했다. 애니메이션 블루프린트와 BlendSpace 사이의 하드 참조 1개는 격리 목록 내부였고, 보존 패키지에서 격리 목록을 참조하는 항목은 없었다. 개발 사본 검사는 각 사본의 8개 맵 Editor 로드 범위다.
- 원본 초기 FrontendOnlyAttempt는 종료 코드 -1·루트 실행 파일 없음이었다. 최종 바이너리 검증에서 원본 비·훈련 HUD·스토리 HUD, 전시판 비의 최초 시도는 게임 초기화 전에 중단돼 PASS가 없었다. 명령 파일 방식의 재실행에서 해당 검사를 통과했다. 원본 M4 지도 최초 시도는 종료 로그는 있으나 PASS가 없어 제외했고 StartMapRetry를 근거로 삼았다. 11월 6일 P03 및 이번 초기 V1 검사와 최종 바이너리 실행을 합산하지 않는다.
- 배포본 검사는 패키지 실행 파일을 콘솔과 격리 슬롯으로 구동한 결과다. 전시판 엔딩은 최종 게시 경로에서 M4 3번 출격 후 성공 이벤트를 주입해 영상 열기와 스킵 뒤 결과를 확인했다. 전체 본편 손 조종이나 엔딩 자연 재생 종료는 확인 범위와 구분한다. [패키지 영수증](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_TwoWin64Packages/FINAL_RECEIPT.json) · [개발 사본 영수증](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_TwoWin64Packages/DEVELOPER_FINAL_RECEIPT.json) · [전시판 엔딩 실행](D:/JGY/project/drone_ops_exhibition_20261106_handoff/20261110_TwoWin64Packages/Exhibition/FinalEnding/M4Map/PASS.json).
