# Drone 제공 에셋 인수 감사와 이식 계획

기준일: 2026-08-25 (Asia/Seoul)

> 이 문서는 AST-01 에셋 이식 시점의 감사 기록이다. 이후 구현·Git 상태는 [`STATUS.md`](../STATUS.md)와 [`DRONE_WORKLOG.md`](DRONE_WORKLOG.md)를 따른다.

## 1. 감사 범위와 판정

- 사용자가 알려준 `D:\JGY\project\Unreal\_260821`은 실제 파일시스템에는 없었다.
- 실제 인수 폴더는 `D:\JGY\project\Unreal_260821`이다.
- 최상위 ZIP 14개와 같은 이름의 해제 폴더 14개를 대조했다.
- ZIP 내부의 파일별 상대 경로와 크기를 해제 폴더와 비교한 결과 14개 모두 `Missing 0 / Extra 0 / SizeMismatch 0`이다.
- 해제 결과는 10,499개 파일, 35,677,612,290 bytes다. 주요 Unreal 파일은 `.uasset` 10,445개와 `.umap` 25개다.
- 최상위 ZIP 14개의 원본 크기는 33,730,171,781 bytes다. 원본과 해제본을 합쳐 약 64.6 GiB이므로 전체를 Drone 저장소에 복사하지 않는다.
- 외부 ZIP 14개는 정상 해제됐지만 `Non-Pilot Drones KITBASH SET\FBX.zip`에는 개별 FBX 55개가 한 번 더 압축되어 있다. 현재 해제 폴더에는 통합 `Drones-all.fbx`와 내부 `FBX.zip`만 있다.
- 해제본에서 파일명 기준 `LICENSE`, `EULA`, `README`, `Documentation`, `Manual` 문서를 찾지 못했다. 배포·포트폴리오 사용 전 구매 계정의 라이선스와 영수증을 별도로 보존한다.
- 이 감사는 제공된 ZIP과 해제본의 완전성을 확인한 것이다. 판매 페이지의 상품 구성, 라이선스 증빙, 최신 판매자 업데이트 포함 여부까지 증명하지는 않는다.

## 2. 팩별 기술 감사

| 팩 | 파일 수 | 내부 기준 경로·버전 단서 | 판정과 용도 |
|---|---:|---|---|
| ArmyVFX | 147 | `/Game/ArmyVFX`, UE 5.0, Niagara | 폭발·연기 VFX 후보. Demo와 외부 참조는 제외하고 Niagara System 단위로 선별한다. |
| Battlefield | 1,192 | `/Game/Battlefield`, ControlRig·Niagara·구형 NV Clothing 참조 | 4.35 GB급 환경 팩. 전체 이식 금지, Overview/Demo를 스테이징에서 본 뒤 필요한 건물·장애물만 선택한다. |
| cplomedia_InfantrySFX | 4,288 | `/Game/cplomedia_InfantrySFX`, UE 5.0 | 보병·무기·환경음 후보. Cue 하나를 고르면 연결 WAV만 함께 이식한다. |
| Drone-Sounds | 48 | `/Game/Drone-Sounds`, UE 5.2 | 44.1 kHz와 96 kHz Drone Loop가 중복 제공된다. 첫 적용은 용량이 작은 44.1 kHz Cue 한 세트로 제한한다. |
| DronePack_Project | 248 | 완전한 UE 5.1 프로젝트, `/Game/Drone_Pack` | FPV·Delivery·Police·Spy·Baba Drone 메시와 Blueprint가 있다. 기능 Blueprint 대신 FPV Body·Rotor·Material만 우선 사용한다. |
| FC_MilitaryCamp | 668 | `/Game/FC_MilitaryCamp`, UE 5.1/5.3 혼합 | 군사 캠프·지형 후보. 7.23 GB라 Map 전체보다 선택한 건물·소품 의존성만 이식한다. |
| GC_DroneS | 436 | `/Game/GC_DroneS`, UE 4.24, `PhysXVehicles` | 궤도형 Drone·MG·Missile Turret 메시 후보. 구형 차량 Blueprint는 UE 5.8에 그대로 적용하지 않고 프로젝트 코드로 기능을 재구현한다. |
| MillitaryBase | 1,474 | `/Game/MillitaryBase`, UE 5.3 | 대형 기지 환경 후보. `/Game/RacingTrack` 참조 문자열이 있어 스테이징에서 누락 의존성을 확인한다. |
| Modular_Insurgents | 207 | `/Game/Modular_Insurgents`, UE 4.23 | 적 NPC 외형 후보. Demo AnimBP는 제외하고 Skeletal Mesh·Material 중심으로 평가한다. |
| Modular_Soldier | 970 | `/Game/Modular_Soldier`, UE 5.6 | Operator·아군 NPC 외형 후보. Demo Input·ControlRig·Widget을 프로젝트 게임플레이에 상속하지 않는다. |
| NavigationArrows | 11 | `/Game/NavigationArrows`, UE 5.2/5.3 | 목표 안내 후보. 현재 Tutorial Gate 표시와 비교한 뒤 필요한 경우에만 Wrapper로 사용한다. |
| Non-Pilot Drones KITBASH SET | 외부 2 + 내부 FBX 55 | Raw FBX | 개별 조립형 Drone 후보. 내부 `FBX.zip`을 별도 원본 폴더에 해제한 뒤 필요한 부품만 임포트한다. |
| OilRigLiope_Tr | 795 | 실제 경로 `/Game/Liope_Tr`, UE 5.3 | 해제 폴더명과 패키지 경로가 다르다. `Content/OilRigLiope_Tr`로 직접 복사하면 참조가 깨지므로 스테이징에는 `Content/Liope_Tr`로 배치한다. |
| PBR Sting Counter-Drone | 13 | Raw FBX·PNG | 직접 임포트 가능한 Anti-Drone 외형 후보. Import Scale·Forward·Pivot·재질 채널을 먼저 확인한다. |

샘플 문자열 감사에서 `ArmyVFX`의 `/Game/DemoRoom2`, `/Game/Global`, `DronePack_Project`의 `/Game/Characters`, `/Game/Developers`, `MillitaryBase`의 `/Game/RacingTrack`, `Modular_Soldier`의 `/Game/NewFolder1` 참조 단서가 발견됐다. 실제 Hard/Soft 참조 또는 단순 Import Metadata인지 UE 5.8 Asset Audit로 구분하기 전에는 해당 Demo 자산을 본 프로젝트로 옮기지 않는다.

## 3. 이식 원칙

1. 원본 ZIP과 현재 해제본은 읽기 전용 원본으로 보존한다.
2. `D:\JGY\project\drone\Content`에 외부 팩 전체를 Explorer로 직접 복사하지 않는다.
3. UE 5.8 전용 임시 스테이징 프로젝트의 복사본에서 팩을 하나씩 연다.
4. Loose `.uasset`은 내부에 기록된 원래 Content Root를 유지해 먼저 로드한다. `OilRigLiope_Tr`만 `Liope_Tr` 경로를 사용한다.
5. Blueprint Compile, Asset Audit, Reference Viewer와 Demo Map Check로 누락 클래스·플러그인·참조를 확인한다.
6. 필요한 Mesh·Material·Texture·Sound·VFX와 그 의존성만 고른다. 외부 GameMode, Pawn, PlayerController, Input Mapping, Level Blueprint는 가져오지 않는다.
7. 선택 자산은 스테이징 Content Browser에서 `/Game/Drone/ThirdParty/<Pack>`으로 이동하고 Redirector를 정리한다. 바이너리 파일을 Explorer에서 임의 이동하지 않는다.
8. 이동·재저장한 선택 자산만 Unreal `Migrate`로 실제 Drone 프로젝트에 넣는다.
9. 프로젝트 소유 연결 Blueprint는 `/Game/Drone/Integrations/<Pack>`에 만들고 현재 C++ Pawn·Collision Root·Movement·Camera·Telemetry를 유지한다.
10. 외부 Blueprint를 프로젝트 핵심 클래스의 부모로 사용하지 않는다. 구형 기능은 외형·소리·애니메이션만 재사용하고 상태와 기능은 `Source/Drone`에서 구현한다.

## 4. 권장 이식 순서

### AST-01A — 첫 Drone 외형 Spike

- `DronePack_Project/Content/Drone_Pack/D_Mesh/DroneFPV`의 Body, Rotor A~D, Material과 필요한 Texture만 선택한다.
- 현재 `BP_DronePrototypePawn`의 Cube Visual을 바로 지우지 않고 Integration Blueprint에서 숨김 전환 가능하게 둔다.
- Body와 Rotor는 Collision을 끄고 기존 C++ Collision Root를 유지한다.
- Forward, Pivot, Scale, Rotor 위치와 Camera 가림을 확인한다.
- 외부 `BP_DroneEnhancedFPV`의 입력·이동 코드는 사용하지 않는다.

### AST-01B — Drone Loop Sound

- `Drone-Sounds`의 44.1 kHz Loop Cue 하나와 연결 WAV만 이식한다.
- Drone 상태 Component 또는 Integration Blueprint가 재생을 소유하고 HUD·입력 코드와 결합하지 않는다.
- 정지·Possess 해제·PIE 종료 때 중복 Audio Component가 남지 않는지 확인한다.

### AST-02 — VFX와 목표 안내

- ArmyVFX는 필요한 Niagara System만, NavigationArrows는 현재 프로젝트 표시보다 이점이 있을 때만 이식한다.
- Demo Map, Demo Room, Sequence는 의존성 검증용 스테이징에만 둔다.

### AST-03 — Story 환경과 NPC

- Battlefield, FC_MilitaryCamp, MillitaryBase, OilRig은 Overview/Demo를 각각 열어 시각·성능 비교 후 한 팩부터 선택한다.
- Modular Soldier와 Insurgents는 외형·Skeleton·Material을 우선하고 프로젝트 소유 Operator/NPC 클래스에 연결한다.

### AST-04 — Enemy Drone·MG

- `GC_DroneS`의 Mesh, Skeleton, Turret Part, Material, Audio를 후보로 사용한다.
- `PhysXVehicles` 기반 이동 Blueprint와 Demo Vehicle은 이식하지 않는다.
- Enemy AI, 점유, 조준, 발사, Damage는 프로젝트 소유 C++/Integration Blueprint 경계로 다시 연결한다.

### AST-05 — Raw FBX 후보

- Non-Pilot 개별 FBX와 PBR Sting을 `/Game/Drone/ThirdParty/RawDrones`에 임포트한다.
- 단위, 축, Normal/Tangent, UV, Collision, Material 채널과 LOD를 확인한 뒤 실제 후보만 남긴다.

## 5. 각 이식 단위의 완료 조건

- UE 5.8에서 선택 자산 Load Failure 0
- 선택 Blueprint Compile errors/warnings 0
- 선택 Demo 또는 검사 Map의 Map Check errors/warnings 0
- `/Game/Drone` 생산 자산에서 ThirdPerson·Variant 신규 의존성 0
- 외부 Pawn·GameMode·Input Mapping 신규 의존성 0
- 기존 Collision Root, 이동, 고도, Yaw, Camera, Telemetry HUD 동작 동일
- Tutorial 전체 `Drone.` 자동화 기준선 유지
- Standalone에서 외형, 재질, Rotor, Camera, Sound의 수동 확인
- 새 `.uasset`·`.umap` Git LFS 적용 확인
- Git에 추가할 실제 선택 자산의 파일 수와 LFS 용량을 Commit 전에 별도 검토

## 6. 현재 정지선

- `D:\JGY\project\Unreal_260821\_Staging\DroneAssetStage` UE 5.8 스테이징에서 DronePack과 Drone-Sounds를 복사·상향 재저장했다.
- 공급사 Blueprint 전체 Compile은 `0 errors / 27 warnings / 0 load failures`였다. 경고는 구형 `MoveForward` 등 Input Axis와 누락 Mannequin Rig 참조이므로 외부 기능 Blueprint는 사용하지 않는다.
- 실제 Drone 저장소에는 FPV Body·Rotor A~D·Material·Texture 4개와 44.1 kHz Cue/Wave, 합계 12개·21,753,071 bytes만 `/Game/Drone/ThirdParty`로 이식했다.
- `/Game/Drone/Integrations/DronePackFPV/BP_DroneFPVIntegration`은 `ADronePrototypePawn` 자식이다. 기존 Sphere Collision Root·Movement·고정 추적 Camera·Input·Telemetry를 유지하고 본체 1, Rotor 4, Engine Loop Audio 1을 소유한다.
- Prototype BP GameMode는 FPV Integration Pawn과 기존 BP PlayerController를 명시적으로 사용한다. 외부 Pawn·GameMode·PlayerController·IMC는 가져오지 않았다.
- 선택 자산의 외부 Game 의존성은 0이며 Integration에서 ThirdPerson·Variant·원본 `/Game/Drone_Pack`·`/Game/Drone-Sounds`로 향하는 의존성도 0이다.
- `DroneEditor Win64 Development` Build, Blueprint `0/0/0`, Map Check `0/0`, 전체 `Drone.` Automation `12/12`를 통과했다. 전용 `Drone.Integration.FPVAsset`은 런타임 본체/로터/Audio 개수와 Collision 분리를 검사한다.
- 이식 스크립트는 같은 Blueprint에 다시 실행해도 구성요소가 늘어나지 않도록 Asset 참조 기준 중복 제거를 적용했고 재실행 후에도 Mesh 5·Audio 1을 유지했다.
- 제공 Cue는 이름에 `Loop`가 있지만 실제 Wave Player 반복 설정은 꺼져 있었다. 프로젝트 이식본의 Looping을 켜고 `SoundBase::IsLooping()` 자동 계약을 추가했다.
- 실제 렌더러 Standalone 캡처에서 FPV 외형과 고정 추적 Camera, 기존 HUD·Course·Gate 표시 및 정상 종료를 확인했다.
- 실제 스피커에서 Loop가 한 번만 재생되고 종료 시 멈추는지는 아직 수동 확인하지 않았다. 자동 Loop 계약 통과와 실제 청감 통과는 별개이며, 현재 청감 상태는 Pass·Fail이 아닌 `미확인`이다.
- 따라서 `AST-01`은 Doing으로 유지한다. 수동 결과를 확보하면 판정을 갱신한다. 이 시점의 다음 기능 카드는 `TUT-03 Segment/Lap 기록`이었다.
- 이 시점에는 Drone/문서 변경이 로컬 작업 트리에 남아 있었고 아직 Commit·Push하지 않은 상태였다. 이후 동기화 결과는 현재 상태 문서에서 확인한다.
