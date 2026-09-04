# Drone NPC 감지·추적 시선 및 고개 회전 계획

기준일: 2026-09-04 (Asia/Seoul)

상태: C++·Rifle AnimBP Component Space 축 교정·자동화 완료, 수동 화면 재확인 대기

이 문서는 적 NPC가 드론을 발견한 뒤 이동·엄폐·MG 사용 중에도 표적을 자연스럽게 바라보고, 시야가 잠깐 끊겨도 고개가 튀지 않게 만드는 기준이다. `ADroneNPCAIController`의 감지·1초 Sight 실종 유예·마지막 감지 위치·Search와 프로젝트 소유 Rifle AnimBP의 상체/목/고개 보정을 연결했다. 첫 화면 확인에서 좌우 회전 대신 위아래 까딱임이 발생해 Bone Space를 Component Space로 교정했으며, 교정 뒤 실제 축과 체감 속도를 다시 확인한다.

## 1. 결론

새 StateTree 상태를 계속 추가하지 않는다. 역할은 아래 세 층으로 분리한다.

```text
StateTree
  감지·MG·Cover·Search·Patrol 상태만 결정
        ↓
ADroneNPCAIController
  현재 Drone 또는 마지막 감지 위치를 시선 목표로 유지
  목표 방향을 NPC 로컬 Yaw/Pitch로 계산하고 제한·보간
        ↓
ABP_NPC_Rifle_Greybox
  전달받은 Yaw/Pitch/Alpha로 상체·목·고개만 회전
```

StateTree Task마다 머리 회전 코드를 넣으면 `DroneDetected → MoveToCover → UseCover` 전환 때마다 시선이 초기화된다. 시선 수명은 Controller가 감지 대상 수명과 함께 관리하고 AnimBP는 표현만 담당한다.

## 2. 상태별 시선 계약

| 상태 | 바라볼 대상 | 종료 조건 |
|---|---|---|
| `Patrol` | 없음, 정면으로 부드럽게 복귀 | Drone 감지 |
| `DroneDetected` | 현재 `DetectedDrone` | 실종 확정·Drone 파괴·NPC 사망 |
| `MoveToMGTurret`, `MoveToCover` | 현재 `DetectedDrone` | 같은 조건. 이동 방향은 CharacterMovement가 담당 |
| `HoldMGTurret`, `UseMGTurret`, `UseCover` | 현재 `DetectedDrone` | 같은 조건 |
| Sight 실패 유예 1초 | 기존 `DetectedDrone` 유지 | 재감지하면 계속 추적, 유예 만료 시 마지막 위치로 전환 |
| `Search` | `LastKnownDroneLocation` | 재감지 또는 Search 완료 |
| Drone 파괴·NPC 사망·UnPossess | 즉시 해제 | 해당 없음 |

Friendly NPC는 현재 드론 감지를 전투 조건으로 쓰지 않으므로 `AI-GAZE-01`에서는 추적 대상에서 제외한다.

## 3. C++ 구현 기준

수정 중심은 `Source/Drone/AI/DroneNPCAIController.h/.cpp`다.

1. 감지 성공 시 `DetectedDrone` 약한 참조를 시선 목표로 쓰고 움직이는 Actor 위치를 매 프레임 갱신한다.
2. Sight 실패 Callback에서는 목표를 즉시 지우지 않는다. 기존 `DroneSightLossGracePeriod=1.0s` 동안 같은 Actor 시선을 유지한다.
3. 실종 확정 뒤 `Search`에서는 `LastKnownDroneLocation`을 시선 목표로 쓴다.
4. Search 완료, Drone 파괴, NPC 사망, `OnUnPossess`에서는 시선 Alpha와 회전을 정면으로 부드럽게 복귀시킨다.
5. 원하는 시선 방향을 NPC Actor Rotation 기준 로컬 회전으로 바꾸고 `Yaw/Pitch`를 제한한 뒤 보간한다.
6. AnimBP는 Controller가 공급하는 `DroneLookRotation`, 3개 Bone 분배 회전, `DroneLookAlpha`, `bHasDroneLookTarget`만 읽는다. AnimBP가 Perception이나 StateTree를 직접 조회하지 않는다.
7. `AAIController::SetFocus/SetFocalPoint`는 사용하지 않는다. Gameplay Focus가 Controller Yaw를 바꿔 Smart Object Slot·Cover·MG 몸 방향과 경쟁한 회귀가 확인되어, 몸과 무관한 시각용 Gaze 상태로 분리했다.

Greybox 시작값:

| 값 | 시작값 | 의미 |
|---|---:|---|
| 최대 좌우 고개 각도 | `65°` | 이 범위를 넘는 표적은 고개만 비틀지 않고 향후 몸 회전으로 넘김 |
| 위쪽 Pitch | `40°` | 공중 Drone 추적 |
| 아래쪽 Pitch | `25°` | 지면 가까운 Drone 추적 |
| 추적 보간 속도 | `6.0` | 감지 뒤 목표를 따라가는 속도 |
| 정면 복귀 속도 | `3.5` | 목표 해제 뒤 급히 튕기지 않는 복귀 |
| 시선 Alpha 보간 | `6.0` | AnimGraph 적용 강도 |

이 수치는 최종 밸런스가 아니다. Class Defaults 또는 역할별 Child BP에서 조정 가능한 값으로 둔다.

## 4. 몸 회전과 고개 회전 분리

- AI Gameplay Focus는 사용하지 않는다. 이동 중 몸 방향은 CharacterMovement 또는 Smart Object Slot Yaw가 담당하고, Drone 추적은 AnimBP Bone 보정만 담당한다.
- 표적이 고개 제한각을 벗어나도 첫 단계에서는 Actor Rotation을 즉시 바꾸지 않는다. `AI-GAZE-02`에서 일정 시간·각도 기준의 느린 몸 회전을 별도로 검토한다.
- MG 조준은 `고정 BaseMount → Yaw 몸체 → Pitch 포신 → Muzzle` 계약으로 분리했다. NPC 몸·고개와 MG Pivot이 서로 Transform을 덮어쓰지 않는다. 자세한 연결은 [`DRONE_MG_TURRET_3PART_GUIDE.md`](DRONE_MG_TURRET_3PART_GUIDE.md)를 따른다.

## 5. AnimBP 연결

첫 적용 대상은 프로젝트 소유 `/Game/Drone/AI/Animation/ABP_NPC_Rifle_Greybox`다. 공급사 AnimBP와 Legacy `ABP_Unarmed`는 직접 수정하지 않는다.

권장 AnimGraph 순서:

```text
Rifle Locomotion
→ DefaultSlot 발사·재장전
→ Component Space 변환
→ spine_03 소량 회전
→ neck_01 중간 회전
→ head 나머지 회전
→ Local Space 복귀
→ Output Pose
```

- `spine_03 / neck_01 / head`에 대략 `20% / 45% / 35%`로 분배해 목 한 곳만 꺾이는 모습을 피한다.
- `Transform (Modify) Bone`은 Rotation `Add to Existing`, Space `Component Space`를 사용한다. Manny Bone Space에서는 Controller의 Yaw가 Bone 로컬축 기준으로 적용돼 고개가 좌우로 돌지 않고 위아래로 까딱이는 현상이 실제 화면에서 확인됐다.
- `LookAlpha`로 전체 적용 강도를 보간한다.
- 발사·Reload Slot 뒤에 시선 보정을 적용해 Montage가 고개 방향을 매번 정면으로 덮지 않게 한다.
- 실제 Manny Skeleton의 Bone 이름과 Component Space 회전축을 Skeleton Tree에서 확인한 뒤 저장한다. 좌우·상하 방향이 반대일 때만 역할별 부호 보정을 검토한다.

향후 최종 Soldier/Insurgent Mesh가 확정되면 같은 C++ 시선 계약을 유지하고 AnimBP의 Bone 분배와 축만 교체한다.

## 6. 자동 검증

기존 `Drone.AI.NPCPerceptionSearchPIE`를 확장한다.

1. Hostile 감지 성공 뒤 Gaze Target과 Alpha가 활성화되고 AI Focus Actor는 비어 있다.
2. Sight 실패 직후와 1초 유예 중에는 Gaze Target이 유지된다.
3. 재감지하면 Lost Count가 늘지 않고 Gaze가 끊기지 않는다.
4. 실종 확정 뒤 `Search`가 마지막 감지 위치를 바라본다.
5. Search 완료, Drone 파괴, NPC 사망, UnPossess 뒤 Gaze가 해제된다.
6. Friendly는 Drone을 보더라도 Gaze와 Look Alpha가 활성화되지 않는다.
7. Look Yaw/Pitch가 설정 제한을 넘지 않고 목표 해제 뒤 0으로 수렴한다.
8. Slot 몸 방향과 분리된 상태로 MG 점유·발사·교대, Cover 사격과 Search→Patrol 회귀가 유지된다.

2026-09-04 검증 결과:

- `DroneEditor Win64 Development`, `Drone Win64 Development` 빌드 성공
- 저장된 `ABP_NPC_Rifle_Greybox` 재부모화와 `spine_03 → neck_01 → head` Component Space 그래프 새 프로세스 검증 성공
- `Drone.AI.NPCGreyboxAssets`, `Drone.AI.NPCPerceptionSearchPIE`, `Drone.AI.SmartObjectFoundationDefaults`, `Drone.AI.SmartObjectStationAssets`, `Drone.AI.ProjectileBallistics` 집중 5/5 통과

## 7. 화면 확인

`/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`에서 다음을 확인한다.

1. Drone을 NPC 정면에서 왼쪽·오른쪽·위·아래 순서로 천천히 이동한다.
2. 왼쪽/오른쪽 이동에는 고개·상체가 좌우로 돌고, 위/아래 이동에만 고개가 상하로 움직이는지 본다. 이전처럼 좌우 이동에도 까딱이기만 하면 실패다.
3. 발견 뒤 눈·고개·상체가 먼저 따라오고 몸 전체가 한 프레임에 꺾이지 않는지 본다.
4. NPC가 MG 또는 Cover로 이동하는 중에도 시선이 끊기지 않는지 본다.
5. 장애물에 0.5초 가렸다 다시 보여 고개가 정면으로 튀지 않는지 본다.
6. 1초 이상 숨긴 뒤 마지막 위치를 바라보며 Search하고, Search 완료 후 정면으로 부드럽게 복귀하는지 본다.
7. Rifle 연사·Reload 중 손과 총기 정렬, 목 관절, 어깨가 무너지지 않는지 확인한다.

통과 기록 형식:

```text
좌우 Yaw 정상, 상하 Pitch 정상, 까딱임 없음, 감지 추적 정상, 이동 중 시선 유지,
1초 유예 끊김 없음, Search 마지막 위치 정상, 정면 복귀 자연스러움,
몸 순간 회전 없음, Rifle/MG/Cover 자세 이상 없음
```

## 8. 구현 순서

1. [x] `AI-GAZE-01A`: Controller의 독립 Gaze Target 수명과 부드러운 로컬 Look 값
2. [x] `AI-GAZE-01B`: PIE 감지·유예·Search·해제·몸 방향 비간섭 자동화
3. [x] `AI-GAZE-01C`: `ABP_NPC_Rifle_Greybox` 상체·목·고개 연결
4. `AI-GAZE-01D`: Greybox Map 화면 튜닝과 수동 Pass
5. `AI-GAZE-02`: 필요할 때만 제한각 밖 느린 몸 회전·Aim Offset 검토

현재 Editor는 자동 검증 뒤 종료된 상태다. `Lvl_MilitaryBase.umap`은 이번 작업에서 직접 수정·체크아웃하지 않았고 최종 Git 상태에서도 변경 파일로 잡히지 않는다.
