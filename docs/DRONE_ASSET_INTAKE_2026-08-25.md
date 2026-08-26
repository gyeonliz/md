# Drone 제공 에셋 인수 감사와 이식 계획

기준일: 2026-08-25 (Asia/Seoul)

> 최초 D 드라이브 감사 기록은 역사 자료로 보존하고, 같은 날짜에 확인한 현재 `C:\에셋` 상태와 실제 프로젝트 이식 재검증을 앞부분과 7절에 덧붙였다. 이후 구현·Git 상태는 [`STATUS.md`](../STATUS.md)와 [`DRONE_WORKLOG.md`](DRONE_WORKLOG.md)를 따른다.

## 0. 현재 `C:\에셋` 재감사 요약

현재 이 PC에서 제공 에셋이 실제로 있는 위치는 `C:\에셋`이다. 이전 기록의 두 D 드라이브 경로는 이 PC에 없다. 현재 폴더에는 공급사 해제본 14개와 `_Staging`이 있으며, 최초 감사에 사용한 최상위 ZIP 14개는 없다. 따라서 1절의 ZIP 대조 결과는 당시의 역사적 증거이고 현재 C 드라이브에서 다시 실행한 결과가 아니다.

| 최상위 항목 | 현재 파일 수 | 현재 크기(bytes) |
|---|---:|---:|
| `_Staging` | 348 | 480,636,195 |
| `ArmyVFX` | 147 | 185,086,080 |
| `Battlefield` | 1,192 | 4,347,332,483 |
| `cplomedia_InfantrySFX` | 4,288 | 2,611,067,865 |
| `Drone-Sounds` | 48 | 139,485,217 |
| `DronePack_Project` | 274 | 338,626,778 |
| `FC_MilitaryCamp` | 668 | 7,231,564,285 |
| `GC_DroneS` | 436 | 729,800,325 |
| `MillitaryBase` | 1,474 | 8,564,009,222 |
| `Modular_Insurgents` | 207 | 1,193,429,704 |
| `Modular_Soldier` | 970 | 5,505,904,898 |
| `NavigationArrows` | 11 | 1,364,087 |
| `Non-Pilot Drones KITBASH SET` | 57 | 212,245,701 |
| `OilRigLiope_Tr` | 795 | 4,670,839,064 |
| `PBR_Sting_Counter-Drone_Interceptor_UAV___Anti-Drone___Loitering_Munition-62a9ca6e` | 13 | 148,789,523 |

- 현재 전체: 10,928개 파일, 866개 폴더, 36,360,181,427 bytes
- 현재 확장자: `.uasset` 10,734개, `.umap` 26개, `.fbx` 66개, `.png` 13개, `.zip` 1개
- `.uproject`는 `DronePack_Project\DronePack.uproject`와 `_Staging\DroneAssetStage\DroneAssetStage.uproject` 두 개이고 둘 다 현재 Engine Association 5.8. `.uplugin`은 0개
- 공급사 해제본 14개에서 스테이징과 현재 추가로 존재하는 내부 FBX 해제본·Unreal 생성 캐시를 제외한 기준선은 최초 감사와 같은 10,499개·35,677,612,290 bytes
- 현재 유일한 ZIP `Non-Pilot Drones KITBASH SET\FBX.zip`의 내부 FBX 55개와 현재 `FBX` 폴더의 55개는 파일별 SHA-256 불일치 0. 통합 `Drones-all.fbx`도 별도로 존재
- 라이선스·EULA·README·Documentation·Manual 문서는 확인되지 않음. 구매 계정의 영수증과 라이선스 증빙을 별도 보존해야 함
- `PBR Sting`의 Fab Metadata에는 대상 버전 `UE_5.7`, `isAiForbidden: true`, 실제 Ukraine 전쟁·Counter-Drone 설정 문구가 있으나 이것은 라이선스 문서나 프로젝트 설정 확정 근거가 아님. 권리 조건을 별도로 확인하기 전에는 해당 자산을 생성형 도구에 업로드하지 않고, 프로젝트의 국가·적군·세계관을 이 Metadata에서 가져오지 않음
- `C:\에셋\DronePack_Project\Config\DefaultEngine.ini`에는 활성 Android File Server와 비어 있지 않은 토큰이 있음. 값을 출력·복사·Commit하지 않으며, 실제 Drone 프로젝트의 Android File Server 꺼짐·네트워크 꺼짐·빈 토큰 설정을 유지

## 1. 최초 D 드라이브 감사 범위와 판정 (역사 기록)

- 사용자가 알려준 `D:\JGY\project\Unreal\_260821`은 실제 파일시스템에는 없었다.
- 실제 인수 폴더는 `D:\JGY\project\Unreal_260821`이다.
- 최상위 ZIP 14개와 같은 이름의 해제 폴더 14개를 대조했다.
- ZIP 내부의 파일별 상대 경로와 크기를 해제 폴더와 비교한 결과 14개 모두 `Missing 0 / Extra 0 / SizeMismatch 0`이다.
- 해제 결과는 10,499개 파일, 35,677,612,290 bytes다. 주요 Unreal 파일은 `.uasset` 10,445개와 `.umap` 25개다.
- 최상위 ZIP 14개의 원본 크기는 33,730,171,781 bytes다. 원본과 해제본을 합쳐 약 64.6 GiB이므로 전체를 Drone 저장소에 복사하지 않는다.
- 최초 감사 당시 외부 ZIP 14개는 정상 해제됐고 `Non-Pilot Drones KITBASH SET\FBX.zip`에는 개별 FBX 55개가 한 번 더 압축되어 있었다. 현재 C 드라이브에는 그 55개도 `FBX` 폴더에 해제되어 있으며 내부 ZIP과 SHA-256이 모두 일치한다.
- 해제본에서 파일명 기준 `LICENSE`, `EULA`, `README`, `Documentation`, `Manual` 문서를 찾지 못했다. 배포·포트폴리오 사용 전 구매 계정의 라이선스와 영수증을 별도로 보존한다.
- 이 감사는 제공된 ZIP과 해제본의 완전성을 확인한 것이다. 판매 페이지의 상품 구성, 라이선스 증빙, 최신 판매자 업데이트 포함 여부까지 증명하지는 않는다.

## 2. 팩별 기술 감사

| 팩 | 파일 수 | 내부 기준 경로·버전 단서 | 판정과 용도 |
|---|---:|---|---|
| ArmyVFX | 147 | `/Game/ArmyVFX`, UE 5.0, Niagara | 폭발·연기 VFX 후보. Demo와 외부 참조는 제외하고 Niagara System 단위로 선별한다. |
| Battlefield | 1,192 | `/Game/Battlefield`, ControlRig·Niagara·구형 NV Clothing 참조 | 4.35 GB급 환경 팩. 전체 이식 금지, Overview/Demo를 스테이징에서 본 뒤 필요한 건물·장애물만 선택한다. |
| cplomedia_InfantrySFX | 4,288 | `/Game/cplomedia_InfantrySFX`, UE 5.0 | 보병·무기·환경음 후보. Cue 하나를 고르면 연결 WAV만 함께 이식한다. |
| Drone-Sounds | 48 | `/Game/Drone-Sounds`, UE 5.2 | 44.1 kHz와 96 kHz Drone Loop가 중복 제공된다. 첫 적용은 용량이 작은 44.1 kHz Cue 한 세트로 제한한다. |
| DronePack_Project | 248 | 선택 FPV 패키지 UE 5.1, 전체 패키지 4.24/5.0/5.1 혼합, 현재 `.uproject` Association 5.8, `/Game/Drone_Pack` | FPV·Delivery·Police·Spy·Baba Drone 메시와 Blueprint가 있다. 기능 Blueprint 대신 FPV Body·Rotor·Material만 우선 사용한다. |
| FC_MilitaryCamp | 668 | `/Game/FC_MilitaryCamp`, UE 5.1/5.3 혼합 | 군사 캠프·지형 후보. 7.23 GB라 Map 전체보다 선택한 건물·소품 의존성만 이식한다. |
| GC_DroneS | 436 | `/Game/GC_DroneS`, UE 4.24, `PhysXVehicles` | 궤도형 Drone·MG·Missile Turret 메시 후보. 구형 차량 Blueprint는 UE 5.8에 그대로 적용하지 않고 프로젝트 코드로 기능을 재구현한다. |
| MillitaryBase | 1,474 | `/Game/MillitaryBase`, UE 5.3 | 대형 기지 환경 후보. `/Game/RacingTrack` 참조 문자열이 있어 스테이징에서 누락 의존성을 확인한다. |
| Modular_Insurgents | 207 | `/Game/Modular_Insurgents`, UE 4.23 | 적 NPC 외형 후보. Demo AnimBP는 제외하고 Skeletal Mesh·Material 중심으로 평가한다. |
| Modular_Soldier | 970 | `/Game/Modular_Soldier`, UE 5.6 | Operator·아군 NPC 외형 후보. Demo Input·ControlRig·Widget을 프로젝트 게임플레이에 상속하지 않는다. |
| NavigationArrows | 11 | `/Game/NavigationArrows`, UE 5.2/5.3 | 목표 안내 후보. 현재 Tutorial Gate 표시와 비교한 뒤 필요한 경우에만 Wrapper로 사용한다. |
| Non-Pilot Drones KITBASH SET | 외부 2 + 내부 FBX 55 | Raw FBX | 개별 조립형 Drone 후보. 현재 해제된 `FBX` 폴더에서 필요한 부품만 선별 임포트한다. 내부 ZIP과 해제본 55개는 SHA-256이 일치한다. |
| OilRigLiope_Tr | 795 | 실제 경로 `/Game/Liope_Tr`, UE 5.3 | 해제 폴더명과 패키지 경로가 다르다. `Content/OilRigLiope_Tr`로 직접 복사하면 참조가 깨지므로 스테이징에는 `Content/Liope_Tr`로 배치한다. |
| PBR Sting Counter-Drone | 13 | Raw FBX·PNG | 직접 임포트 가능한 Anti-Drone 외형 후보. Import Scale·Forward·Pivot·재질 채널을 먼저 확인한다. |

샘플 문자열 감사에서 `ArmyVFX`의 `/Game/DemoRoom2`, `/Game/Global`, `DronePack_Project`의 `/Game/Characters`, `/Game/Developers`, `MillitaryBase`의 `/Game/RacingTrack`, `Modular_Soldier`의 `/Game/NewFolder1` 참조 단서가 발견됐다. 실제 Hard/Soft 참조 또는 단순 Import Metadata인지 UE 5.8 Asset Audit로 구분하기 전에는 해당 Demo 자산을 본 프로젝트로 옮기지 않는다.

## 3. 이식 원칙

1. 현재 확보한 공급사 해제본과 남아 있는 Archive는 읽기 전용 제공 소스로 보존한다.
2. `C:\URproject\drone\Content`에 외부 팩 전체를 Explorer로 직접 복사하지 않는다.
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

## 6. AST-01 최초 이식 시점의 정지선

- 최초 이식 작업은 당시 `D:\JGY\project\Unreal_260821\_Staging\DroneAssetStage`의 UE 5.8 스테이징에서 수행했다. 다른 PC에서는 `C:\에셋\_Staging\DroneAssetStage`를 대응 스테이징으로 재감사했으며 선택 자산 대조 결과는 7절에 기록한다. 현재 D 드라이브 PC 경로는 다시 원래 D 스테이징이다.
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

## 7. 현재 프로젝트 이식 재검증

### 실제 이식 수량과 출처

- 프로젝트 `/Game/Drone/ThirdParty`: 12개, 21,753,071 bytes
- 프로젝트 `/Game/Drone/Integrations`: `BP_DroneFPVIntegration` 1개, 34,484 bytes
- 합계: 13개, 21,787,555 bytes
- FPV 10개 출처: `C:\에셋\DronePack_Project\Content\Drone_Pack\D_Mesh\DroneFPV`
- Sound 2개 출처: `C:\에셋\Drone-Sounds\Cue\44_1kHz-24bit`과 `C:\에셋\Drone-Sounds\Wav\44_1kHz-24bit`의 첫 Standard Drone Loop Cue/Wave

선택한 12개는 FPV Body 1, Rotor A~D 4, Material 1, Texture 4, Sound Cue 1, Sound Wave 1이다. Raw 원본은 패키지 경로가 `/Game/Drone_Pack`과 `/Game/Drone-Sounds`이고 UE 5.1/5.2 헤더이므로, `/Game/Drone/ThirdParty` 이동과 UE 5.8 재저장 뒤 SHA-256이 같아야 하는 파일이 아니다.

### 스테이징·프로젝트 대조

- UE 5.8 스테이징 12개와 프로젝트 12개 중 FPV 10개와 Wave 1개는 SHA-256이 정확히 일치
- Cue 1개만 프로젝트에서 Wave Player의 `Looping=true`를 저장해 스테이징본과 의도적으로 다름
- 전용 자동화의 `SoundBase::IsLooping()` 검사가 이 변경을 확인
- Integration BP는 외부 팩에서 가져온 기능 BP가 아니라 프로젝트에서 만든 `ADronePrototypePawn` 자식
- 구성은 Body 1, Rotor 4, Auto Activate Audio 1이며 Visual의 Collision·Overlap·Physics·Navigation은 꺼짐. native Collision Root·Movement·Camera·Input·Telemetry는 유지
- Prototype BP GameMode의 Default Pawn은 이 Integration BP를 가리킴

### 의존성·Git·Unreal 검증

- 현재 Integration Asset Registry 재감사에서 Engine Audio 아이콘 2개, 프로젝트 Input Action 5개와 IMC 1개, FPV Mesh 5개, 프로젝트 Cue 1개, `/Script/Drone`만 확인
- 원본 `/Game/Drone_Pack`, `/Game/Drone-Sounds`, ThirdPerson, Variant 금지 의존성 0
- 이식 자산 13개 모두 Git LFS 추적, `git lfs fsck` 통과
- 이번 재검증 `Drone.Integration.FPVAsset`: 1/1 Success
- 이번 재검증 전체 Blueprint Compile: 0 errors, 0 warnings, 0 failed to load
- 현재 Commit의 전체 자동화 기준선: `Drone.` 14/14. 이 전체 묶음은 TUT-03 완료 때 실행한 기준선이며 이번 재감사에서는 FPV 전용 테스트만 다시 실행
- 이 재감사 시점의 프로젝트 전역 기본 Map/GameMode는 ThirdPerson이었다. 현재 `2cc5d79`에서는 기본 Map이 `/Game/Drone/Maps/Lvl_DroneTraining`, 전역 GameMode가 `BP_DronePrototypeGameMode`다.

### 남은 사람 확인

전용 자동화·Asset Registry 감사·Git 검증은 파일 존재·참조·구성요소 수·Loop 설정·의존성·LFS를 나누어 확인하지만 실제 화면과 스피커 결과를 대신하지 않는다. `Lvl_DroneTraining` 또는 `Lvl_DronePrototype`에서 다음을 확인한다.

1. FPV Body와 Rotor 4개가 보이고 Camera를 가리거나 비정상 크기·방향·위치로 나오지 않는지 확인한다.
2. 재생 중 Drone 소리가 한 겹만 들리는지 확인한다.
3. 여러 Loop 경계를 지나도 끊김이나 겹침이 없는지 듣는다.
4. PIE/Standalone을 종료했을 때 소리가 즉시 멈추는지 확인한다.

청감 결과가 없으므로 `AST-01`은 계속 Doing이다. 이번 재검증은 이식 파일과 구조가 정상이라는 판정이며 실제 청감 Pass를 뜻하지 않는다.

## 2026-08-26 — AST-02A NavigationArrows 최소 이식

### 권리와 증빙 상태

- 사용자는 이 제공 에셋이 지원과정을 통해 구매·지급되었으며 프로젝트 사용에 문제가 없다고 확인했다. 프로젝트 사용 권리는 이번 이식의 차단 조건이 아니다.
- `C:\에셋`에서 별도 `LICENSE`, `EULA`, 영수증 파일을 찾지 못한 기존 결과는 로컬 증빙 보관 상태다. 판매 페이지 조건 확인이나 법률 검토 완료를 의미하지 않는다.
- `PBR Sting` Metadata의 `isAiForbidden: true`는 해당 팩을 생성형 도구에 올리지 않는 제한으로만 적용한다. NavigationArrows나 일반 Unreal 사용에 확대하지 않는다.

### 원본 감사와 선택

- 원본 `C:\에셋\NavigationArrows`: 11개·1,364,087 bytes
- UE 5.8 전용 스테이징: `C:\에셋\_Staging\NavigationArrowsStage`
- 선택한 최소 폐쇄 집합: 6개·원본 기준 1,072,269 bytes
- UE 5.8 이동·재저장 후 실제 프로젝트 크기: 1,098,730 bytes

```text
/Game/Drone/ThirdParty/NavigationArrows
├─ Blueprints/NavigationArrow          # Widget Blueprint
├─ Icons/NewTransparentArrow           # Texture2D
├─ Icons/TransparentArrow              # Texture2D
└─ InfoStructs
   ├─ ImageInfo                        # UserDefinedStruct
   ├─ MovementInfo                     # UserDefinedStruct
   └─ TextInfo                         # UserDefinedStruct
```

첫 이식에서 제외한 자산은 `Demo.umap`, `Demo_BuiltData`, `NavigationArrowExampleActor`, `ExampleMesh`, `TransparentCircle`이다. Demo와 Example은 기능 Widget의 런타임 폐쇄 집합이 아니며, `TransparentCircle`은 팩 내부 참조가 없다.

### UE 5.8 검증

- 원본 11개 Asset Registry 발견 11/11, 로드 실패 0
- 원본 `NavigationArrow`와 `NavigationArrowExampleActor` Compile 성공
- 이동 후 정확히 6개, 원본 `/Game/NavigationArrows` 의존성 0, 외부 `/Game` 의존성 0
- 실제 Drone 프로젝트에서 Generated Class와 2개 Texture·3개 Struct 로드 성공
- `DroneEditor Win64 Development` Build 성공
- `Drone.Integration.NavigationArrowsAsset`: 1/1 Success
- 전체 `Drone.` 자동화: 15/15 Success, warning·failure 0
- Blueprint Compile: 0 errors, 0 Blueprint warnings, 0 failed loads
- 6개 모두 Git LFS filter·diff·merge 적용, `git lfs fsck` 통과

Blueprint Compile 프로세스의 전역 로그에는 활성 Unreal MCP 플러그인의 EULA 안내 경고가 한 번 있었지만 Blueprint 결과 집계는 0 errors·0 warnings·0 failed loads였다. 자산 오류로 계산하지 않는다.

### 현재 경계와 다음 단계

이번 단계는 외부 Widget과 그 의존성을 안전한 ThirdParty 경계에 넣은 것이다. `NavigationArrow`는 현재 Training Map/HUD에 생성되지 않으므로 아직 화면에 보이는 기능이 아니다. 기존 Course Spline과 Gate Ring을 교체하지 않는다.

다음 자산 카드는 프로젝트 소유 Host/Wrapper가 로컬 플레이어에게 Widget 한 개만 만들고 `UDroneTrainingGateSequenceComponent::GetCurrentGate()`의 결과를 `TargetComponent` 또는 `TargetWorldLocation`으로 전달하는 작업이다. Course 완료·Reset·UnPossess·EndPlay에서 숨김과 정리를 검증한다. `NavigationArrowExampleActor`는 사용하지 않는다.

Commit `5a052c8bab2eb0dd8bc9ab16cfc7b3784e8e4cd7`을 `origin/codex/navigation-arrows-migration`에 Push한 뒤 Merge Commit `fb1d7ad2c23d6bf3b1c854ca7c1c0cddba2062ef`로 `origin/main`에도 반영했다. 병합된 main에서 Build와 동일 검증 묶음을 다시 통과했다. 실제 Training HUD Host/Wrapper는 아직 미구현이다.

## 2026-08-26 09:17 — D 드라이브 작업 PC 재확인

- 현재 제공 에셋 루트: `D:\JGY\project\Unreal_260821`
- 현재 PC에 `C:\에셋`은 없으며, 앞 절의 C 드라이브 수치와 검증은 다른 PC에서 수행한 역사 기록이다.
- D 루트에는 최상위 ZIP 14개, 대응 공급사 폴더 14개와 `_Staging`이 존재한다. 잘못 알려졌던 `D:\JGY\project\Unreal\_260821`은 존재하지 않는다.
- 이 시점의 D 드라이브 기록은 역사 상태다. 2026-08-26 13:11 KST 이번 확인 PC의 `C:\URproject\drone`은 `main=origin/main=fb1d7ad`, 작업 트리 Clean이다.
- FPV·Sound와 기존 main 작업을 보존한 채 NavigationArrows 6개와 전용 테스트도 main에 포함했다.
- 다음 기능 우선순위는 `TUT-04`다. NavigationArrows Host/Wrapper 화면 연결은 별도 후속 카드이며, 실제 Drone Loop 청감은 계속 미확인이다.

## 2026-08-26 11:50 — AST-01C DronePack 드론·맵 선별 이식

### 원본과 이식 범위

- 원본 프로젝트: `D:\JGY\project\Unreal_260821\DronePack_Project`
- UE 5.8 스테이징: `D:\JGY\project\Unreal_260821\_Staging\DroneAssetStage`
- 대상 경로: `/Game/Drone/ThirdParty/DronePack`
- 실제 이식: `.uasset` 153개와 `.umap` 1개, 총 154개·82,465,487 bytes
- 포함: DronePack의 Drone `D_Mesh` 시각 자산 전부와 정리된 `Map_Demo`
- 제외: 공급사 Pawn·Controller·GameMode·Input·HUD Blueprint, 열화상 Mannequin, 기존 프로젝트와 중복되는 FPV 기능 자산

원본 Demo Map의 Drone Blueprint Actor 6개는 시각 Mesh Actor로 변환했다. 누락된 Mannequin을 요구하던 열화상 Actor 3개와 도우미 Collision·Camera Proxy를 제거했고, 삭제 Actor를 가리키던 Level Blueprint Event Graph도 제거했다. 장애물 배치에 필요한 `BP_Boxtemplate`은 컴파일 가능한 맵 구성요소로 유지했다. 따라서 이 맵은 공급사 조작 기능을 들여온 플레이 맵이 아니라 드론 6종과 환경을 비교하는 시각 검토 맵이다.

### 검증 결과

- 스테이징 Map 전이 의존성: 외부 Game 의존성 0, 누락 의존성 0
- 실제 프로젝트 UE 5.8 Resave: 154/154 성공
- `Map_Demo` Map Check: 0 errors / 0 warnings
- 전체 Blueprint Compile: 0 errors / 0 warnings / 0 failed loads
- `DroneEditor Win64 Development`: MSVC 14.51.36256 지정 빌드 성공
- 재빌드 DLL 기준 전체 `Drone.` 자동화: 14 succeeded / 0 warnings / 0 failed
- PIE Input Lifecycle: 새 PIE 3/3에서 Keyboard·Mouse·Gamepad·복합·반대 입력과 HUD/Possession 수명주기 통과
- 원본 `/Game/Drone_Pack`, ThirdPerson, Variant 문자열 잔존 0
- Git LFS 속성 154/154, `git lfs fsck`와 `git diff --check` 통과

### 현재 경계와 다음 단계

당시 `Map_Demo`를 전역 시작 Map이나 Training Map으로 지정하지 않았고 기존 ThirdPerson 기본 실행 경로도 유지했다. 이후 Commit `2cc5d79`에서 이 맵을 `/Game/Drone/Maps/Lvl_DronePackShowcase`로 중앙화하고, 기본 실행 경로는 `/Game/Drone/Maps/Lvl_DroneTraining`으로 교체했다. 다음 확인은 Editor에서 Showcase 맵을 열어 드론 6종, 환경 배치, 재질, 스케일, 조명과 카메라 구도를 눈으로 확인하는 것이다. 이후 선택한 외형만 프로젝트 소유 Integration BP에 연결한다. 공급사 기능 Blueprint를 다시 상속하거나 입력·GameMode를 가져오지 않는다.

위 문장은 11:50 당시의 중간 상태였으며 이후 완료됐다. 154개 원본 이식은 Commit `5540c6b`로 main에 포함됐고, 이후 맵 중앙화·템플릿 콘텐츠 정리 Merge `2cc5d79`까지 반영되어 `main=origin/main`, 작업 트리 Clean이다. 현재 맵 이름은 `Lvl_DronePackShowcase`이며 Editor에서 드론 6종·재질·스케일·조명을 보는 시각 검토는 아직이다.

Battlefield·MilitaryCamp·MilitaryBase는 AST-01C와 분리된 `AST-03A`에서 이후 이식했다. 현재 중앙 Map 3종과 정확한 의존성 2,723개·16.96 GiB가 Commit `f8c8fb2`에 있으며, 기술 검증 결과와 수동 확인 경계는 [`DRONE_CONTENT_FOLDER_GUIDE.md`](DRONE_CONTENT_FOLDER_GUIDE.md)를 따른다.
