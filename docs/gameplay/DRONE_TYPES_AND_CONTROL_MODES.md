# 드론 역할·조작 방식·핸들링 프리셋

기준일: 2026-09-08 (Asia/Seoul)

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
| 조작 방식 `EDroneControlMode` | 쉬운 조작, 실제 조작형(그레이박스) | 입력 보조와 기체 자세가 이동에 반영되는 정도 |
| 핸들링 `EDroneHandlingPreset` | 안정, 균형, 고기동 | 같은 기체의 속도·가속·Yaw·최대 기울기 반응성 |

따라서 `고기동 드론`을 별도 기체 종류로 만들지 않는다. 예를 들어 같은 정찰 드론에서 `쉬운 조작 + 안정`, `쉬운 조작 + 고기동`, `실제 조작형 + 균형` 조합을 모두 시험할 수 있다.

## 기체 역할별 현재 상태

| 역할 | 현재 Pawn/제공 모델 | 역할 고유 기능 | 다음 확인·구현 |
|---|---|---|---|
| 정찰 드론 | `BP_DroneScoutIntegration`; DroneSpy 본체·카메라·로터 4 | 거리·화각·LOS 유지형 Scan과 Training 표적 구현 | 모델 스케일/방향·Scan 체감, 최종 UI/FX |
| FPV 자폭 드론 | `BP_DroneFPVIntegration`; FPV 본체·로터 4, FPV 기본 시점 | 명시적 Arm·최소 속도 충돌·1회 폭발, 제공 Niagara/Cue 연결 | 폭발 크기/청감·Mission별 Damage 조정 |
| 드랍 드론 | `BP_DroneDropIntegration`; Delivery 본체·카메라·로터 6·크레이트 선적재 화물 | 탑뷰·투하·착지 후 잔류·가장 가까운 목표 자동 선택·맵 크레이트 근접 적재·실제 Actor 재투하 구현 | 부착 위치/크기 체감, FX와 Mission별 투하 규칙 |
| 광섬유 드론 | 미구현 | 재밍 면역 미구현 | FPV 공통 기능 뒤 별도 Data Asset과 재밍 규칙 |
| 지상 드론 UGV | 공중 Pawn으로 처리하지 않음 | 주행·무장·연료 미구현 | 별도 Ground Pawn/Movement로 구현 |
| 장거리 타격 드론 | 플레이 기체 미등록 | 출격/타격 연출 미구현 | 플레이 가능 여부 확정 뒤 Sequencer 또는 Pawn 결정 |

`UDroneDefinition`은 `PlannedCapabilities`와 `ImplementedCapabilities`를 따로 가진다. 현재 3종 Data Asset은 각각 검증된 고유 기능 한 개를 두 목록에 모두 가진다. 광섬유·UGV·장거리 타격 후보는 아직 구현 목록에 넣지 않는다.

## 두 조작 방식의 실제 차이

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

## Blueprint에서 바꾸는 방법

대상은 `BP_DroneScoutIntegration`, `BP_DroneFPVIntegration`, `BP_DroneDropIntegration` 또는 `ADronePrototypePawn` 파생 Blueprint다.

1. Pawn 참조에서 `Set Control Mode`를 호출한다.
2. `Assisted Easy` 또는 `Manual Realistic Greybox`를 전달한다.
3. 핸들링은 `Set Handling Preset`에 `Stable`, `Balanced`, `Agile` 중 하나를 전달한다.
4. 두 조작 방식을 번갈아 시험할 때는 `Toggle Control Mode`를 사용한다.
5. 안정→균형→고기동 순환 버튼은 `Cycle Handling Preset`을 사용한다.
6. UI 문구 갱신은 `On Flight Control Settings Changed` Event에 바인딩한다.
7. 시작값은 각 `DA_Drone_*_Greybox`의 `Flight Profile > Default Control Mode / Default Handling Preset`에서 설정한다.

키 바인딩은 아직 확정하지 않았다. FLOW-05 Drone 선택 화면의 `조작`·`반응성` 버튼이 값을 고르고, Controller가 Spawn Pawn에 같은 API로 적용한다.

## Blueprint에서 조정 가능한 수치

Pawn Class Defaults에서 다음 Struct를 연다.

- `Assisted Easy Tuning`: 가속·감속·Turning Boost·Yaw 배율
- `Manual Realistic Greybox Tuning`: 위 배율, Local Up 사용, Collision Root 자세 사용
- `Stable / Balanced / Agile Handling Tuning`: 최대 속도·가속·Yaw·최대 자세각 배율

각 기체의 절대 기준값은 Data Asset의 `Flight Profile`에 둔다. 모드 전환 시에는 기준값에서 다시 계산하므로 반복 전환해도 배율이 누적되지 않는다.

## Editor 확인 순서

1. `Lvl_DroneTraining` 또는 Prototype Map을 연다.
2. 정찰 Data Asset 기본값인 `쉬운 조작 + 균형`으로 전후·좌우·고도를 확인한다.
3. `Set Control Mode(ManualRealisticGreybox)`를 임시 Widget/Button에서 호출한다.
4. 전진 입력에서 Root와 FPV Camera가 Pitch되고, 고도 입력이 기체 Local Up을 따르는지 확인한다.
5. 입력을 놓았을 때 쉬운 조작보다 관성이 길게 남는지 확인한다.
6. Stable/Balanced/Agile을 차례로 바꾸며 속도·Yaw·기울기 한도가 즉시 달라지는지 확인한다.
7. 쉬운 조작으로 돌아왔을 때 Root Pitch/Roll이 수평 복귀하는지 확인한다.

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
9. 공통 역할 입력 — 임시 좌클릭/RB 1차, 우클릭/LB 2차, `P`/패드 Y 시점 전환, IMC 21 Mapping과 Pawn Binding 자동화 완료
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
