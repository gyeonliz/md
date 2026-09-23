# 드론 역할·조작 방식·핸들링 프리셋

기준일: 2026-09-23 (Asia/Seoul)

## 기획 자료 사용 원칙

- 읽기 기준: [Figma `Project:Droner`](https://www.figma.com/design/x9CAVMxSxFdME9XUIlrf78/Project-Droner?node-id=0-1&t=tXU1hQ5hhU1MmrDq-1)
- Figma 내부 내용은 읽기만 했으며 수정·댓글·공유 설정 변경을 하지 않는다.
- 아래 목록은 현재 Figma에서 확인한 기획 역할이다. 최종 이름·규칙 확정이나 구현 완료를 뜻하지 않는다.
- Unreal 코드·Data Asset·자동화 시험으로 확인한 항목만 `구현`으로 표시한다.

## 세 축을 분리한다

기체 역할, 조작 보조 수준, 반응성은 서로 다른 값이다.

| 축 | 현재 값 | 의미 |
|---|---|---|
| 임무 역할 `EDroneMissionRole` | 정찰, 드랍, FPV 자폭, 광섬유, 지상 UGV, 장거리 타격 | 기체가 임무에서 맡는 기능 |
| 조작 방식 `EDroneControlMode` | 쉬운 조작, 실제 조작형(제한 자세), FPV Rate/Acro Mode 1, FPV Rate/Acro Mode 2 | 입력 보조와 RC 송신기 스틱 배치 |
| 속도 단계 `EDroneHandlingPreset` | 느림, 보통, 빠름 | 같은 기체의 최대 이동 속도 |

따라서 `고기동 드론`을 별도 기체 종류로 만들지 않는다. 같은 기체에서 조작 방식과 속도를 따로 고른다. 기존 열거형 내부 이름 `Stable/Balanced/Agile`은 저장 Asset 호환을 위해 유지하지만 UI와 기획 의미는 `느림/보통/빠름`이며, 현재는 최대 속도 배율만 바꾼다. FPV 자폭 역할 Data Asset은 `Rate/Acro Mode 2 + 빠름`을 기본값으로 사용한다.

## 기체 역할별 현재 상태

| 역할 | 현재 Pawn/제공 모델 | 역할 고유 기능 | 다음 확인·구현 |
|---|---|---|---|
| 정찰 드론 | `BP_DroneScoutIntegration`; DroneSpy 본체·카메라·로터 4 | 거리·화각·LOS 유지형 Scan과 Training 표적 구현 | 모델 스케일/방향·Scan 체감, 최종 UI/FX |
| FPV 자폭 드론 | `BP_DroneFPVIntegration`; FPV 본체·로터 4, FPV 기본 시점 | 명시적 Arm·최소 속도 충돌·1회 폭발, 제공 Niagara/Cue 연결 | 폭발 크기/청감·Mission별 Damage 조정 |
| 드랍 드론 | `BP_DroneDropIntegration`; Delivery 본체·카메라·로터 6·크레이트 선적재 화물 | 탑뷰·투하·착지 후 잔류·가장 가까운 목표 자동 선택·맵 크레이트 근접 적재·실제 Actor 재투하 구현 | 부착 위치/크기 체감, FX와 Mission별 투하 규칙 |
| 광섬유 드론 | `BP_DroneFiberOpticIntegration`; Sting Interceptor Visual, 빈 통 Static Mesh 슬롯, 1인칭 기본 | `JammingImmunity + ImpactDetonation`, 통 출구→지나온 지면 Spline과 처진 마지막 구간 구현 | 제작 통 Mesh·출구 Offset·케이블 굵기 화면 조정, 충돌 자폭·재밍 Zone 면역 확인, Mission 3 교대 연결 |
| 지상 드론 UGV | `BP_DroneGroundUGVIntegration`; GC Drone 1 Skeletal Visual | W/S 전후·A/D 조향·Q/E 제자리 회전, 최초 장거리 지면 획득, 4점 지면 높이/Pitch/Roll 추종, 공중 바람 Drift 차단 | 높은 Spawn→접지·Mesh 위치·스케일·경사/단차 추종 화면 확인, 무장·연료와 Mission 3 교대는 후속 |
| 장거리 타격 드론 | 플레이 기체 미등록 | 출격/타격 연출 미구현 | 플레이 가능 여부 확정 뒤 Sequencer 또는 Pawn 결정 |

`UDroneDefinition`은 `PlannedCapabilities`와 `ImplementedCapabilities`를 따로 가진다. 현재 Catalog에는 Scout/FPV/Drop/Fiber/Ground 5종 Data Asset이 등록돼 있고 자동화가 순서와 역할 Capability를 검사한다. 장거리 타격 후보는 아직 구현 목록에 넣지 않는다.

## 네 조작 방식의 실제 차이

### 쉬운 조작

- 기존 `UFloatingPawnMovement`의 빠른 자동 감속과 선회 보조를 사용한다.
- 전후·좌우 입력은 즉시 이동 방향으로 사용한다.
- 고도 입력은 기체가 기울어도 항상 World Up을 사용한다.
- 충돌 Root와 3인칭 Camera는 수평을 유지하고 `VisualTiltPivot` 외형만 기울인다.

### 실제 조작형(그레이박스)

- 감속과 Turning Boost를 낮춰 입력을 놓은 뒤 관성이 더 남는다.
- 전후·좌우 입력으로 충돌 Root의 Pitch/Roll 자세가 변한다.
- 기울어진 Actor의 Forward/Right/Up 축이 이동 입력에 사용된다.
- 입력 해제 또는 쉬운 조작 복귀 시 Root가 서서히 수평으로 돌아온다.
- 아직 모터별 RPM, 중력-양력 평형, PID, 공기저항을 계산하는 실제 비행 물리 모델은 아니다.

### FPV Rate/Acro Mode 1·2(그레이박스)

- Betaflight Rate/Acro와 같이 Pitch/Roll/Yaw 스틱을 이동 방향이 아닌 **기체 Body 각속도 명령**으로 해석한다.
- 스틱을 중앙으로 돌려도 자동 수평 복귀하지 않고 현재 자세를 유지한다.
- Pitch/Roll에 고정 각도 제한이 없어 Roll과 Loop가 가능하다.
- Throttle 중립은 수평 자세에서 중력을 상쇄하는 호버, 위 입력은 추가 추력, 아래 입력은 추력 감소로 해석한다. 추력은 기울어진 기체의 Local Up 방향으로 적용되어 W로 기수를 숙이면 전진력이 생긴다.
- Mode 1은 왼쪽 스틱 `Yaw/Pitch`, 오른쪽 스틱 `Roll/Throttle`을 사용한다.
- Mode 2는 왼쪽 스틱 `Yaw/Throttle`, 오른쪽 스틱 `Roll/Pitch`를 사용한다.
- 키보드는 Mode 1·2 모두 같은 직관적 배치를 유지한다. 장치별 입력을 공용 Move Action에서 재해석하지 않고 Acro 의미축 4개와 패드 세로 원시축 2개로 분리한다.
- 현재 v1은 World 중력, 호버 스로틀, Body Up 추력, 속도 비례 선형 항력, Body Rate 응답 시간을 계산한다. 이동 기반은 여전히 `UFloatingPawnMovement`이며 모터별 RPM, PID, 프로펠러 공력, 질량·관성 텐서를 푼 완전한 비행 시뮬레이터는 아니다.

#### 현재 Rate/Acro 입력표

Rate/Acro는 Front-end Drone 선택 화면에서 FPV 기체를 고르면 기본 Mode 2로 적용된다. 일반 플레이 중 모드를 바꾸는 확정 단축키는 아직 없고, UI의 조작 설정 순환은 `쉬운 조작 → 제한 자세 → Mode 1 → Mode 2` 순서다.

| 기능 | 키보드·마우스 | Gamepad Mode 1 | Gamepad Mode 2 | 비고 |
|---|---|---|---|---|
| Throttle / Local Up 추진 | `Space/Left Ctrl` | 오른쪽 Stick Y | 왼쪽 Stick Y | 중립=호버, Space=추력 증가, Ctrl=추력 감소. 기울면 Body Up 방향으로 추진 |
| Yaw | `Q/E` | 왼쪽 Stick X | 왼쪽 Stick X | 왼쪽/오른쪽 선회 |
| Roll | `A/D` | 오른쪽 Stick X | 오른쪽 Stick X | 기체 좌/우 회전, 90° 제한 없음 |
| Pitch | `W/S` | 왼쪽 Stick Y | 오른쪽 Stick Y | W는 Nose-down/전진 방향 Pitch, S는 Nose-up/후진 방향 Pitch |
| Mouse Look | Mouse X: 기체 Yaw, Mouse Y: Camera Pitch | 해당 없음 | 해당 없음 | Rate 스틱이 아닌 개발용 직접 회전/카메라 입력 |
| 1인칭/3인칭 | `P` | Y/Triangle | Y/Triangle | 임시 시점 전환 |
| 역할 Primary/Secondary | 좌/우 클릭 | RB/LB | RB/LB | 정찰·자폭·투하 역할 기능 |

`IA_DronePrototype_AcroPitch/Roll/Yaw/Throttle` 네 Action과 `AcroGamepadLeftVertical/RightVertical` 두 Action은 Acro에서만 값을 사용한다. 쉬운/제한 자세용 Move·Altitude·Yaw와 같은 물리 키가 IMC에 함께 있어도 Pawn이 현재 모드에 맞는 Action만 소비하므로 W/S와 Space/Ctrl이 같은 축으로 겹치지 않는다. Mode 1·2 배치는 Spektrum의 공식 송신기 설명과 DX5e 매뉴얼의 채널 배치를 기준으로 했다: [Mode 1 vs Mode 2](https://my.spektrumrc.com/Articles/Article.aspx?ArticleID=2105), [DX5e Manual](https://spektrumrc.com/ProdInfo/Files/SPMR5510-Manual_EN.pdf).

## 공개 자료를 반영한 현재 FPV 기준값

특정 군용 자폭 드론의 비공개 성능을 추정하지 않는다. 조작 의미는 Betaflight 공식 문서, 이동 성능 범위는 공개된 민간 FPV 제품 사양을 기준으로 잡았다.

| 항목 | 현재 Greybox 값 | 근거와 해석 |
|---|---:|---|
| 수평 최대 속도 | 27 m/s | DJI Avata 2 Manual mode 공개 최대 수평 속도. `2160 cm/s × Agile 1.25 = 2700 cm/s` |
| 상승/하강 World Z 제한 | 9 m/s | DJI Avata 2 Sport 공개 최대 상승·하강 속도 |
| Pitch/Roll 최대 Rate | 650°/s | Betaflight 공식 Rate Calculator가 설명하는 Racing 예시 범위 550~650°/s의 상단 |
| Yaw 최대 Rate | 400°/s | 플레이 테스트용 보수적 프로젝트 값. DJI의 공개 사양값으로 오해하지 않는다 |
| Pitch/Roll 중앙 감도 | 180°/s | 조정 가능한 프로젝트 시작값 |
| Pitch/Roll Expo | 0.30 | 조정 가능한 프로젝트 시작값 |
| Hover Throttle | 0.50 | Stick 중립이 수평 자세에서 1g를 상쇄하는 추력 위치 |
| Gravity | 980 cm/s² | World Down 가속도 시작값 |
| Linear Drag | 0.12 /s | 고속 관성을 점진적으로 줄이는 Greybox 항력 |
| Body Rate 응답 | 0.08 s | 목표 각속도로 수렴하는 시작 응답 시간 |

DJI 공개값에는 무풍·해수면 등 측정 조건이 붙으며, 현재 프로젝트 값은 기체를 1:1 복제한다는 뜻이 아니다. 공식 참고: [DJI Avata 2 사양](https://www.dji.com/avata-2/specs), [Betaflight Modes](https://betaflight.com/docs/wiki/guides/current/Modes), [Betaflight Rate Calculator](https://betaflight.com/docs/wiki/guides/current/Rate-Calculator).

## Blueprint에서 바꾸는 방법

대상은 `BP_DroneScoutIntegration`, `BP_DroneFPVIntegration`, `BP_DroneDropIntegration`, `BP_DroneFiberOpticIntegration`, `BP_DroneGroundUGVIntegration` 또는 `ADronePrototypePawn` 파생 Blueprint다.

1. Pawn 참조에서 `Set Control Mode`를 호출한다.
2. `Assisted Easy`, `Manual Realistic Greybox`, `Acro Rate Mode 1 Greybox`, `Acro Rate Realistic Greybox` 중 하나를 전달한다. 마지막 기존 이름은 Asset 호환을 위해 유지한 Mode 2다.
3. 핸들링은 `Set Handling Preset`에 `Stable`, `Balanced`, `Agile` 중 하나를 전달한다.
4. `Toggle Control Mode`는 쉬운 조작 → 제한 자세 → Mode 1 → Mode 2 → 쉬운 조작 순서로 순환한다.
5. 느림→보통→빠름 순환 버튼은 `Cycle Handling Preset`을 사용한다.
6. UI 문구 갱신은 `On Flight Control Settings Changed` Event에 바인딩한다.
7. 시작값은 각 `DA_Drone_*_Greybox`의 `Flight Profile > Default Control Mode / Default Handling Preset`에서 설정한다.

키 바인딩은 아직 확정하지 않았다. FLOW-05 Drone 선택 화면의 `조작`·`반응성` 버튼이 값을 고르고, Controller가 Spawn Pawn에 같은 API로 적용한다.

## Blueprint에서 조정 가능한 수치

Pawn Class Defaults에서 다음 Struct를 연다.

- `Assisted Easy Tuning`: 가속·감속·Turning Boost·Yaw 배율
- `Manual Realistic Greybox Tuning`: 위 배율, Local Up 사용, Collision Root 자세 사용
- `Acro Rate Realistic Greybox Tuning`: Rate/Acro에서 사용할 가속·관성·Local Up·Root 자세 사용
- `Stable / Balanced / Agile Handling Tuning`: Asset 호환 내부 이름. 현재 `느림/보통/빠름` 최대 속도 배율만 사용하고 나머지 배율은 1.0 유지

각 기체의 절대 기준값은 Data Asset의 `Flight Profile`에 둔다. Rate/Acro의 중앙 감도·최대 Rate·Expo·수직 속도·호버/중력/항력/Rate 응답은 `Flight Profile > Acro Rate Settings`에서 조정한다. 모드 전환 시에는 기준값에서 다시 계산하므로 반복 전환해도 배율이 누적되지 않는다.

Ground UGV는 `BP_DroneGroundUGVIntegration` Class Defaults에서 `GroundSteeringRateDegreesPerSecond`, 앞뒤·좌우 4점 간격, Clearance, `GroundInitialAcquireDistanceCentimeters`, 일반 Trace 시작 높이/거리/채널, 높이·회전 보간 속도를 조정한다. 시작 시 최대 10,000cm 아래 지면을 한 번 획득하고 이후 4점 Suspension Trace를 사용한다. GroundDrive 기체는 Assisted 모드로 고정되고 고도 입력과 Weather Drift를 사용하지 않는다. W/S 이동 벡터의 Z도 제거해 비행하지 않으며 `Q/E`는 차체 제자리 회전 보조다. 최종 궤도/바퀴 물리 구현은 아니다.

광섬유 통은 `BP_DroneFiberOpticIntegration > Components > FiberSpoolMeshComponent`의 `Static Mesh` 칸에 넣는다. 현재 칸은 의도적으로 비어 있고 기본 Relative Location은 `X -32 / Y 0 / Z -18cm`다. 통에서 선이 나오는 위치는 Class Defaults의 `FiberSpoolExitOffset`, 지면 점 간격은 `FiberPointSpacingCentimeters`, 처짐은 `FiberSagDepthCentimeters`, 굵기는 `FiberCableThicknessScale`, 보존 길이는 `FiberMaximumLaidPoints`에서 조정한다. Spline은 이동 경로 아래의 지면 점을 누적하고 마지막 지면점에서 현재 통 출구까지 한 점을 내려 처지게 연결한다. Collision·Overlap·Navigation은 사용하지 않는다.

FPV 기본값은 `/Game/Drone/Data/Drones/DA_Drone_FPVStrike_Greybox`에서 조정한다.

- `Pitch Roll Center Sensitivity Degrees Per Second`: Stick 중앙 부근 민감도. 먼저 이 값을 낮춰 미세 조작을 맞춘다.
- `Maximum Pitch Rate Degrees Per Second`, `Maximum Roll Rate Degrees Per Second`: Stick 끝의 Loop/Roll 최대 회전속도.
- `Pitch Roll Expo`: 중앙을 둔하게 하고 끝 입력을 유지하는 곡선. 현재 `0.30`.
- `Yaw Center Sensitivity Degrees Per Second`, `Maximum Yaw Rate Degrees Per Second`, `Yaw Expo`: Yaw 전용 같은 항목.
- `Maximum World Vertical Speed Centimeters Per Second`: World Z 상승·하강 속도 안전 제한. 현재 `900cm/s`.
- `Hover Throttle Normalized`: 입력 0에서 중력을 상쇄하는 0~1 추력 위치. 현재 `0.50`; 낮추면 최대 추력 여유가 커진다.
- `Gravity Acceleration Centimeters Per Second Squared`: World Down 중력. 현재 `980cm/s²`.
- `Linear Drag Per Second`: 속도 비례 항력. 현재 `0.12/s`; 높이면 고속 관성이 더 빨리 줄어든다.
- `Body Rate Response Time Seconds`: 목표 Pitch/Roll/Yaw Rate까지 수렴하는 시간. 현재 `0.08s`; 낮추면 더 즉각적이다.
- Pawn Blueprint의 `Acro Rate Realistic Greybox Tuning`: 이동 Component의 MaxSpeed/Acceleration 배율과 Root 자세 계약. Acro 자동 감속은 끄고 위 선형 항력을 사용한다.
- Pawn Blueprint의 `Stable/Balanced/Agile Handling Tuning`: 각각 느림/보통/빠름에 대응한다. 현재 기본값은 MaxSpeed `0.80/1.00/1.25`, 가속·Yaw·자세각 배율은 모두 `1.0`이다.

조정 순서는 `호버 스로틀 → Body Rate 응답 → 중앙 감도 → Expo → 최대 Rate → 선형 항력/최대 속도`로 잡는다. 먼저 수평 호버와 Pitch 추진을 맞춘 뒤 회전 감도를 조정해야 상승감과 조향감을 혼동하지 않는다.

## Editor 확인 순서

1. `Lvl_DroneTraining` 또는 Prototype Map을 연다.
2. 정찰 Data Asset 기본값인 `쉬운 조작 + 보통`으로 전후·좌우·고도를 확인한다.
3. `Set Control Mode(ManualRealisticGreybox)`를 임시 Widget/Button에서 호출한다.
4. 전진 입력에서 Root와 FPV Camera가 Pitch되고, 고도 입력이 기체 Local Up을 따르는지 확인한다.
5. 입력을 놓았을 때 쉬운 조작보다 관성이 길게 남는지 확인한다.
6. 느림/보통/빠름을 차례로 바꾸며 최대 이동 속도만 달라지고 조향감이 몰래 바뀌지 않는지 확인한다.
7. 쉬운 조작으로 돌아왔을 때 Root Pitch/Roll이 수평 복귀하는지 확인한다.
8. FPV 기체를 골라 Mode 1과 Mode 2에서 각 Pitch/Throttle 세로축이 표대로 바뀌고 스틱을 놓아도 자세가 유지되는지 확인한다.
9. 수평에서 키를 놓으면 중립 호버가 유지되고, Space는 상승하며 Ctrl은 추력을 줄여 하강하는지 확인한다.
10. W로 Nose-down한 뒤 중립/상승 Throttle에서 기체 Up 축이 전진력으로 바뀌는지 확인한다.
11. Roll/Pitch 끝 입력으로 90도를 넘어 회전하고 Local Up Throttle로 바라보는 축에 추진되는지 확인한다.
12. 회전이 너무 민감하면 `Body Rate Response Time`, 중앙 감도와 Expo를 먼저 조정하고 최대 Rate는 마지막에 바꾼다.

자동 검증은 `Drone.Prototype.FlightProfiles`와 `Drone.Flow` 필터로 실행한다.

## 역할·선택 FLOW 구현 결과와 다음 순서

1. `DR-TYPE-01` 역할/조작/핸들링 데이터 계약 — 구현·Build·자동화 완료, 수동 체감 확인 대기
2. `DR-RECON-01` 정찰 스캔 Greybox — 구현·역할 기능 자동화 완료
3. `DR-FPV-01` FPV 충돌 자폭 Greybox — 구현·역할 기능 자동화 완료
4. `DR-DROP-01` 드랍 탑뷰·Payload Greybox — 구현·역할 기능 자동화 완료
5. FLOW-04 Mission Briefing→Map 로드 — 실제 PIE 완료
6. FLOW-05 Mission 허용 3종 카드·설정·선택 Definition 1대 Spawn/Possess — 실제 PIE 완료
7. FLOW-06~07 Mission Director·목표 패널·성공/실패·재도전·로비 복귀 — 실제 PIE 완료
8. FLOW-08 새 실행 기준 전체 흐름 3회 반복 — 3/3 자동화 완료
9. 공통 역할 입력 — 임시 좌클릭/RB 1차, 우클릭/LB 2차, `P`/패드 Y 시점 전환, Mode 1·2 세로축을 포함한 Acro 전용 12개 Mapping, 전체 IMC 33 Mapping과 Pawn Binding 자동화 완료
10. Training Map 정찰/자폭/투하 Target·역할 상태 UI·역할별 제공 모델 — 구현 및 자동화 완료, 수동 화면 확인 대기

현재 역할 입력은 다음처럼 동작한다.

| 역할 | 좌클릭 / 패드 RB: Primary | 우클릭 / 패드 LB: Secondary |
|---|---|---|
| 정찰 | 거리·화각·LOS를 만족하는 가장 가까운 미완료 Target Scan | 진행 중 Scan 취소 |
| FPV 자폭 | 충돌 자폭 Arm | Disarm |
| 드랍 | 적재 중이면 투하, 비어 있으면 300cm 안의 가장 가까운 운반 화물 적재 | 탑뷰 진입/복귀 |

이 키는 기능 검증용 임시값이다. 최종 키보드·마우스·Gamepad 배치는 현재 미정이다.

세 역할을 바꿔가며 시험할 때는 `/Game/Drone/Maps/Lvl_DroneFrontEnd`에서 시작해 `계속 → Training Mission 선택 → 미션 시작 → 작전 시작 → Drone 선택 → 출격` 순서로 진입한다. `/Game/Drone/Maps/Lvl_DroneTraining`은 실제 표적이 놓인 맵이지만 직접 PIE하면 기본 기체만 시작해 전체 역할 선택 흐름을 건너뛴다. 특히 FPV 폭발 뒤 Pawn이 파괴되므로 직접 실행에서는 더 조종할 대상이 없고, Front-end Mission 흐름에서는 결과 UI의 재도전 또는 로비 복귀를 사용한다. 폭발 기능 자체는 Unreal Editor를 종료하지 않는다.

Training 역할 시험 표적은 코스 진행 판정과 분리되어 있다.

- `RoleTest_ReconTarget`: 시작점 우측의 Cyan 안내 표적. 정찰 드론으로 바라본 뒤 좌클릭 또는 패드 RB를 유지한다.
- `RoleTest_ImpactTarget`: Red 안내 충돌 표적. FPV 드론에서 좌클릭 또는 패드 RB로 무장하고 600cm/s 이상으로 충돌한다.
- `RoleTest_PayloadTarget`: 시작점 반대편 Yellow 투하 패드. 드랍 드론에서 우클릭 또는 패드 LB로 탑뷰 전환 후 패드 위에서 좌클릭 또는 패드 RB로 투하한다. 별도 Target 지정 없이 가장 가까운 미완료 패드를 자동 선택한다.
- `RoleTest_CarryablePayload`: 시작점 부근의 MilitaryCamp 크레이트. 선적재 화물을 먼저 투하해 적재 수를 0으로 만든 뒤 300cm 안에서 좌클릭/RB로 적재하고, 기체 하단에 붙은 상태에서 다시 좌클릭/RB로 재투하한다.
- Mission 측면 UI는 정찰 진행률/완료 수, FPV 안전·무장, 드랍 적재/성공/탑뷰 상태를 한글로 표시한다.

### 맵 배치 화물 BP 사용·조정

1. Content Browser에서 `/Game/Drone/Abilities/Payload/BP_DroneCarryablePayload`를 원하는 Mission Map으로 끌어다 놓는다.
2. 다른 외형은 Blueprint의 `PayloadVisual > Static Mesh`, `Transform > Scale`에서 바꾼다. 부모는 `ADroneDroppedPayload`를 유지한다.
3. 맵에서 처음부터 주울 수 있는 물체는 Class Defaults의 `Starts As Carryable Pickup`을 켠다. 이 Actor는 투하·착지 후 사라지지 않고 다시 적재할 수 있다. `Dropped Payload Lifetime Seconds`는 Carryable이 아닌 일반 1회용 Payload에만 적용된다.
4. 드론에 붙는 위치·회전은 각 Drop Pawn Blueprint의 Components에서 `PayloadCarryAnchor` Transform을 바꾼다. 이 Anchor는 외형 기울기를 따라가되 Collision Root와 분리된다.
5. 적재 거리는 Drop Pawn의 `PayloadDropComponent > Carryable Pickup Range Centimeters`에서 바꾸며 기본값은 300cm다.
6. 별도 Event Graph 적재 로직이나 Level Blueprint 입력을 추가하지 않는다. Pawn의 공통 Primary 입력과 C++ Component가 검색·부착·투하 상태를 단일 소유한다.

`BP_DroneDropIntegration`의 `PayloadDropComponent > Payload Class`도 이 BP로 연결되어 있다. 따라서 기체가 처음 들고 시작하는 화물과 맵에 미리 배치한 화물이 모두 같은 크레이트·착지 잔류·재적재 규칙을 사용한다.

광섬유·UGV·장거리 타격은 위 3종 Vertical Slice 뒤 진행한다. 특히 UGV는 공중 Pawn의 핸들링 프리셋을 재사용하지 않고 별도 지상 이동 구조로 만든다.
