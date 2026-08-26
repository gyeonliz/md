# Drone 남은 제공 에셋 선별 이식과 TUT-04B 작업 기록

기준일: 2026-08-27 (Asia/Seoul)

이 문서는 `C:\에셋`에 남아 있던 제공 소스를 UE 5.8.1 스테이징에서 검사한 뒤 실제 `C:\URproject\drone` 프로젝트에 선별 이식한 범위와, 같은 작업에서 추가한 `TUT-04B` 이전 평균·Best 결과 기능을 기록한다.

원본 제공 폴더는 수정하지 않았다. `C:\에셋\_Staging` 아래 복사본만 UE에서 상향 로드·경로 이동했고, 실제 프로젝트에는 선택 자산과 그 재귀 의존성만 복사했다.

## 1. 이번 실제 이식 범위

| 프로젝트 경로 | 실제 자산 수 | 대략 크기 | 선택 기준 |
|---|---:|---:|---|
| `/Game/Drone/ThirdParty/ArmyVFX` | 44 | 48.77 MiB | 폭발, 지면 피격, MG Muzzle Flash, Rocket Smoke, Smoke Screen Niagara 5종과 정확한 의존성 |
| `/Game/Drone/ThirdParty/InfantrySFX` | 8 | 5.93 MiB | Battlefield Atmos, Explosion, Autocannon, Bullet Flyby/Impact Cue 4개와 Wave 4개 |
| `/Game/Drone/ThirdParty/GroundDroneKit` | 78 | 324.37 MiB | 지상 드론 3종, MG Turret, Search Light 부품, 7.62 Ammo의 Mesh·Skeleton·Physics·Material·Texture 의존성 |
| `/Game/Drone/ThirdParty/ModularSoldier` | 80 | 510.02 MiB | 몸체와 대표 Helmet·Vest·Trousers·Gloves·Boot 외형, Skeleton·Physics·Material·Texture |
| `/Game/Drone/ThirdParty/ModularInsurgents` | 46 | 195.21 MiB | `SK_Preset1`, Base Body, Skeleton·Physics·Material·Texture |
| `/Game/Drone/ThirdParty/RawDrones` | 16 | 47.37 MiB | Non-Pilot Quad v4 본체·카메라 2·프로펠러와 PBR Sting 후보를 Static Mesh로 임포트 |
| `/Game/Drone/ThirdParty/OilRig` | 619 | 약 3.41 GiB에 중앙 Map 포함 | 정리한 OilRig Map이 실제로 참조하는 환경 의존성만 이동 |
| `/Game/Drone/Maps/Lvl_OilRig` | 1 | 위 수치에 포함 | 프로젝트 소유 중앙 맵 사본 |

합계는 ThirdParty 891개와 중앙 Map 1개다. 원본 팩 전체 10,000여 개를 넣지 않았으며, 선택하지 않은 변형과 Demo Map은 실제 저장소에 복사하지 않았다.

## 2. 제외한 기능과 이유

- `GC_DroneS`의 이동·Track·Vehicle Blueprint는 구형 `/Script/PhysXVehicles`와 UE 5.8 컴파일 오류가 있어 제외했다. 이번 Ground Drone과 MG는 외형 라이브러리이며 이동·점유·조준·발사·Damage 구현이 아니다.
- Soldier와 Insurgent는 NPC 외형 후보만 있다. Operator, Enemy AI, Animation State, 무기와 팀 규칙은 아직 연결하지 않았다.
- ArmyVFX Demo Room, Sequence와 전체 Niagara 변형은 제외했다. 선택한 지면 피격 효과 일부는 Mesh Distance Field를 사용하므로 실제 적용 전 프로젝트 성능 정책과 `Generate Mesh Distance Fields` 사용 여부를 결정해야 한다.
- InfantrySFX 4,288개 전체를 넣지 않고 첫 임무 프로토타입에서 바로 비교할 Cue 4개만 넣었다.
- Raw FBX는 자동 Static Mesh Import와 자동 Collision까지 통과한 후보 라이브러리다. 최종 Drone 종류, 실제 스케일·Forward·Pivot·Collision·LOD 채택은 아직 미정이다.
- PBR Sting은 로컬 Unreal Import에만 사용했다. Metadata의 `isAiForbidden: true`를 따라 생성형 서비스에 업로드하지 않았으며, 자산 설명의 국가·전쟁 설정을 프로젝트 세계관으로 채택하지 않았다.

## 3. OilRig 정리 내용

원본 해제 폴더명은 `OilRigLiope_Tr`지만 실제 패키지 루트는 `/Game/Liope_Tr`다. 스테이징에서 원래 루트를 유지해 연 뒤 다음 순서로 처리했다.

1. `/Game/Liope_Tr/Maps/Overview`를 `/Game/Drone/Maps/Lvl_OilRig`로 복제했다.
2. Map의 Vendor GameMode Override를 비웠다.
3. `BP_Simple_Door` 8개가 Vendor FirstPerson Pawn·Input·Arms 전체를 의존성으로 끌어오는 것을 확인했다.
4. 환경 후보 맵에서 이 Sample Door Actor 8개를 제거했다. 문 Static Mesh 자체를 일괄 삭제한 것이 아니라, 구형 FirstPerson Cast를 가진 상호작용 Actor를 제거한 것이다.
5. 정리한 Map의 재귀 의존성 620개만 실제 프로젝트로 복사했다.

실제 프로젝트 감사 결과 Map 로드 성공, `default_game_mode=None`, 외부 `/Game` 참조 0, 누락 참조 0이다. 별도 `MAP CHECK` 명령은 첫 대형 Map Construction에서 약 8분 동안 종료되지 않아 저장 없이 검사 프로세스만 중단했다. 따라서 **OilRig의 최종 Map Check, 뷰포트 재질·조명·스케일·충돌·성능은 수동 미확인**이다.

## 4. TUT-04B 이전 평균·Best 결과

`UDroneTrainingLapRecorderComponent`가 현재 완료 Lap을 `SuccessfulLaps`에 넣기 전에 비교 결과를 만든다. 이 순서 덕분에 현재 기록이 자기 비교 평균에 섞이지 않는다.

추가 데이터 경계:

- `FDroneTrainingSegmentComparison`
- `FDroneTrainingLapComparison`
- `GetLastCompletedComparison()`
- `OnLapComparisonReady`
- `BuildLapComparison(PreviousLaps, CurrentLap)`

규칙:

- 첫 성공 Lap은 `기준 기록 생성`, 이전 평균 없음, 자기 자신이 첫 Best다.
- 두 번째 성공부터 현재 Lap을 제외한 유효한 이전 성공 Lap만 평균에 사용한다.
- 시간 Delta는 `현재 - 이전 평균`이므로 음수면 빠름, 양수면 느림이다.
- 속도 Delta도 `현재 - 이전 평균`이며 양수면 평균 속도가 높다.
- Best Time은 최솟값, Best Average Speed는 최댓값이다.
- 같은 Segment 배열 위치끼리 별도 평균·Best·Delta를 만든다.
- Course Gate 구성이 바뀌면 호환되지 않는 History와 마지막 비교 결과를 함께 비운다.

기존 Flight HUD 하단 패널에는 다음 결과 행을 추가했다.

```text
이전 완주 평균  11.00초
최고 완주 기록  9.00초 · 신기록
평균 대비  -2.00초 빠름
속도 평균 대비  +5.0 km/h
```

계산은 Blueprint나 Widget에서 다시 하지 않는다. C++ Recorder가 Struct를 만들고 HUD·후속 WBP는 Event 결과를 표시한다. `USaveGame` 영속화와 점수 규칙은 아직 미구현이다.

## 5. 자동 검증 결과

| 검증 | 결과 |
|---|---|
| `DroneEditor Win64 Development` | 성공 |
| 새 자산 수량 | 7개 Root 모두 스테이징 예상 수량과 일치 |
| 대표 자산 로드 | Niagara, Cue, Ground Drone, MG, Soldier, Insurgent, Quad, Sting 모두 성공 |
| 새 자산 외부 `/Game` 의존성 | 0 |
| 새 자산 누락 의존성 | 0 |
| OilRig 중앙 Map 로드·GameMode | 성공, `None` |
| `CompileAllBlueprints` | 오류 0, 기존 Battlefield Pose GUID 경고와 MCP 고지 경고만 유지 |
| 전체 `Drone.` Automation | 16/16 성공, 실패 0 |
| 새 `Drone.Tutorial.TrainingComparison` | 성공 |
| `Drone.UI.FlightHUDTelemetryBinding` 비교 문자열 | 성공 |

전체 자동화 중 `PIEInputLifecycle` 하나는 Prototype Map에서 RecastNavMesh를 찾지 못했다는 기존 CrowdManager 경고 1개와 함께 성공했다. 기능 실패는 아니다.

## 6. 사용자가 Unreal Editor에서 확인할 일

1. `Lvl_OilRig`을 열고 첫 로드 시간을 기록한다.
2. Missing Material, 검은 Texture, 과도한 밝기, 크기와 충돌 이상을 확인한다.
3. `Build > Map Check`를 직접 실행해 Error/Warning 수를 기록한다.
4. Ground Drone 3종과 MG Turret Skeletal Mesh를 열어 재질·Skeleton·Physics Asset을 확인한다.
5. Modular Soldier와 `SK_Preset1`을 열어 외형을 확인하되 아직 AI가 붙었다고 판단하지 않는다.
6. Quad v4와 Sting Mesh의 크기·Forward·Pivot·Collision을 비교하고 실제 비행 Drone 후보를 고른다.
7. `Lvl_DroneTraining`을 두 번 완주해 첫 시도 `기준 기록 생성`, 두 번째 시도 이전 평균·Best·부호가 실제 HUD에 갱신되는지 확인한다.

## 7. Git 전달 상태

- 기능 Commit: `3fa4444 feat: migrate remaining drone assets and add lap comparisons`
- main Merge Commit: `55b3ffe merge: migrate remaining assets and add lap comparisons`
- 신규 Unreal 패키지: 892개 모두 Git LFS Pointer
- 원격 업로드: LFS 892개·4.9GB 완료
- 로컬 `main`과 `origin/main`: 일치

## 8. 다음 구현 순서

1. 다른 PC에서 `55b3ffe` Pull과 Git LFS 다운로드 확인
2. Training 두 Lap 수동 표시 확인
3. `NavigationArrows` 프로젝트 소유 Host/Wrapper 또는 Course의 다음 Gate 표시 중 하나를 선택
4. Flight 상태: Spawn/Take Off/Landing/Crash 기준 확정
5. Ground Drone·MG는 Enemy AI MVP에서 프로젝트 소유 이동·Smart Object 점유·공격 코드에 연결
6. Soldier/Insurgent 외형은 AI 상태와 Animation 구조가 준비된 뒤 Integration Blueprint로 연결
