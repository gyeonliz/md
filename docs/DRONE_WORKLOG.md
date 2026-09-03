# Drone 개발 진행 기록

기준일: 2026-09-03 (Asia/Seoul)

이 문서는 Drone 개발의 **진행 이력**을 시간순으로 남긴다. 가장 최신의 현재 상태는 [`../WORKBOARD.md`](../WORKBOARD.md), 확정 구현 순서는 [`DRONE_TUTORIAL_STORY_PLAN.md`](DRONE_TUTORIAL_STORY_PLAN.md)를 따른다.

## 갱신 규칙

Drone 코드·자산·계획 작업을 진행할 때마다 작업 종료 전에 Markdown을 함께 갱신한다.

1. `WORKBOARD.md`: 현재 단계, 지금 작업 중인 카드, 완료 근거, 남은 조건과 바로 다음 작업
2. `DRONE_WORKLOG.md`: 실제 변경, 검증 결과, 발견한 문제와 다음 행동을 날짜순으로 추가
3. `STATUS.md`: 빌드·테스트·자산 수처럼 검증된 기준선이 달라졌을 때 갱신
4. `CONTEXT.md`: 사용자가 확정한 방향, 장기 규칙과 범위가 달라졌을 때 갱신
5. 계획 문서: 구현 순서, 완료 조건이나 설계가 달라졌을 때 같은 작업에서 갱신

진행률은 근거 없는 전체 백분율로 표시하지 않는다. 대신 `현재 단계`, `통과한 게이트/전체 게이트`, `Doing`, `다음 활성 카드`로 기록한다. 자동화가 통과해도 필수 수동 확인이 남아 있으면 완료로 이동하지 않는다.

## 현재 스냅샷

마지막 갱신: 2026-09-03 — 전투 비주얼 자산 호환성 감사와 Blueprint 이벤트 경계 완료

| 구분 | 현재 상태 |
|---|---|
| 전체 단계 | Tutorial 두 Lap 수동 확인 대기 + 전투 Greybox 확장 |
| Unreal 기준선 | 공유 `main=origin/main=249d6cd`; AI-MG-02·HP-01·AI-COVER-01·AI-COMBAT-END-01·AI-AMMO-01·AI-VIS-01A 로컬 미커밋 |
| 자동 검증 | 공유 기준선은 전체 27/27·Blueprint 0/0/0·LFS 성공. 최신 로컬은 Editor Build, 무기 집중 테스트 3/3과 비주얼 자산 감사 통과 |
| PFN-06 진행도 | 필수 게이트 5/5 Pass, Done |
| 지금 작업 중 | 다음 후보 `AI-VIS-01B` 실제 Mesh·Animation·FX·SFX 연결 |
| 차단 조건 | Shotgun Weapon Mesh 후보가 확인되지 않았다. Soldier/Insurgent는 Manny와 Skeleton이 달라 최종 외형에 Retarget 검증 필요 |
| 다음 행동 | Manny Rifle Animation/AR4로 임시 Rifle 표현을 연결하고 MG Muzzle 기준을 Editor에서 확인. Shotgun Mesh는 후보 확보 뒤 진행 |
| 다음 기능 | `AI-VIS-01B` |
| 이후 | 전투 Animation·FX·SFX와 최종 Mission 실패 화면 |
| Git 처리 | 마지막 Push는 `249d6cd`. 이후 Unreal 코드와 문서는 사용자 요청대로 로컬 미커밋 유지 |
| 협업 Git | 환경 맵·재질 중앙 반영 및 검증 완료. 개인 `.vsconfig`·시험 주석 정리 완료. 팀원 PC Remote 실측만 남음 |

## 2026-09-03 — AI-MG-02 Occupy·Aim·Fire·Release 핵심

### AI-VIS-01A 자산 호환성 감사·Blueprint 표현 이벤트

- 새 읽기 전용 `Audit-DroneNPCVisualAssets.py`와 실행 Wrapper로 후보 Asset의 Load, Skeleton, Animation 수량, Weapon Mesh 수량을 반복 감사할 수 있게 했다.
- Manny Rifle Animation은 38개이고 AR4·MG·Niagara Muzzle Flash·Sound Cue 후보는 정상 로드된다. FPS Weapon Mesh는 70개지만 이름으로 식별되는 Shotgun Weapon Mesh는 0개다.
- Modular Soldier/Insurgent는 Manny와 Skeleton이 직접 일치하지 않고 이식된 두 Root의 Animation Asset은 각각 0개다. 따라서 최종 진영 외형과 Retarget 결과를 확인하기 전에는 역할 Blueprint에 강제 적용하지 않았다.
- `UDroneNPCWeaponComponent`에 Blueprint용 `OnWeaponFired(WeaponType, TraceStart, AimPoint)`와 `OnReloadCompleted(WeaponType, CurrentAmmo, Capacity)`를 추가했다. Rifle은 Trace당 1회, Shotgun은 Volley당 1회이며 실패/거절 요청은 방송하지 않는다.
- `DroneEditor Win64 Development`와 WeaponContract·RifleTrace·ShotgunTrace 3/3이 통과했다. 전체 자동화·Blueprint Compile·LFS는 반복하지 않았다.
- 현재 Unreal 변경은 `git status --porcelain -uall` 기준 30개 파일, 문서 저장소는 12개 파일이며 모두 로컬 미커밋이다.

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
- 구체 명령과 두 Remote 운영 방식은 [`GIT_UNREAL_GUIDE.md`](GIT_UNREAL_GUIDE.md)에 추가했다.
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
- Definition·Blueprint·StateTree·NavMesh·Rifle/Shotgun·MG의 Editor 작성 순서를 [`DRONE_SMART_OBJECT_NPC_GUIDE.md`](DRONE_SMART_OBJECT_NPC_GUIDE.md)에 정리했다.
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
- 상세 범위와 수동 확인은 [`DRONE_REMAINING_ASSET_MIGRATION_2026-08-27.md`](DRONE_REMAINING_ASSET_MIGRATION_2026-08-27.md)를 따른다.

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
- 상세 구현: [`DRONE_TELEMETRY_IMPLEMENTATION.md`](DRONE_TELEMETRY_IMPLEMENTATION.md)
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
- 상세 결과: [`DRONE_ASSET_INTAKE_2026-08-25.md`](DRONE_ASSET_INTAKE_2026-08-25.md)

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
- 상세 사용법: [`DRONE_UNREAL_MCP.md`](DRONE_UNREAL_MCP.md)

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
- 상세 계획: [`DRONE_CHAOS_DATAFLOW_PLAN.md`](DRONE_CHAOS_DATAFLOW_PLAN.md)

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
- 현재 폴더 규칙: [`DRONE_CONTENT_FOLDER_GUIDE.md`](DRONE_CONTENT_FOLDER_GUIDE.md)

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
