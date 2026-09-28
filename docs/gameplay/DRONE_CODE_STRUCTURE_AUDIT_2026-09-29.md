# Drone 코드·구조 검증 보고서

기준일: 2026-09-29. 대상은 `C:\URproject\drone`의 현재 로컬 변경본이다. Production `/Game/Drone/Maps/Lvl_DroneTraining`은 열거나 저장하지 않았다.

## 결론

Tutorial Mission을 기능별로 독립 시험할 수 있는 구조는 정상이다. Mission 규칙, 기체 역할 기능, 맵 배치와 UI 책임이 분리되어 있으며 이번 검증에서 부족했던 전진·회전·게이트·UGV 두 수업을 같은 계약으로 연결했다.

현재 남은 큰 기능은 단계별 클리어 타임, 8개 연속 진행, 전체 완료 UI와 Warehouse 환경이다. 각 수업의 독립 실행·재시도 기반은 준비됐다.

## 현재 책임 구조

```text
FrontEnd
  → UDroneGameFlowSubsystem: Mission/Drone 선택과 화면 상태
  → UDroneMissionDefinition: 허용 기체, Map, 목표 Event/Tag/시간
  → ADroneMissionPlayerController: 선택 기체 Spawn/Possess, Director 생성
  → ADroneMissionDirector: 목표 진행, 중복 방지, 제한 시간, 성공/실패
  → Trigger/Heading/Hover/Course/Health Actor: 실제 사건 보고
  → Objective/Result Widget: Snapshot과 결과 표시
```

기체 기능은 `UDroneDefinition::ImplementedCapabilities`를 기준으로 `ADronePrototypePawn`이 Component를 활성화한다. UGV 무장은 새 `GroundWeapons` Capability가 있을 때만 켜지므로 다른 기체의 Primary/Secondary 입력과 섞이지 않는다.

## 이번에 확인하고 보완한 항목

| 항목 | 결과 |
|---|---|
| Mission Event 직렬화 | 기존 값을 보존하고 `HeadingAligned`를 열거형 마지막에 추가 |
| 회전 수업 | `ADroneTutorialHeadingZone`, 최단 Yaw 각도, ±8°, 1초 유지, Overlap 중 Timer 구현 |
| 전진 수업 | 공용 `ADroneMissionTrigger`의 `Manual` Event와 안정적인 Actor Tag 사용 |
| 게이트 수업 | Course 하나, Ring 4개, `TrainingLap` Event 연결 |
| UGV 무장 | AI 무기와 분리한 `UDroneGroundWeaponComponent`와 플레이어 Projectile 구현 |
| 총 | 상부 Gun Muzzle 기준 직사, 25 피해, 0.18초 간격, 체력 100 기준 4발 |
| 유탄 | 상부 Grenade Muzzle 기준 중력 투사체, 100 반경 피해, 350cm 반경 |
| 파괴 목표 | NPC와 고정 표적 모두 `UDroneHealthComponent` 사망 Event를 Director가 구독 |
| 시험맵 | 8개 Station과 Mission Definition 8개를 공유 맵에 구성 |
| 로비 | 기존 Training 포함 Mission 9개를 기본 Catalog에 등록 |
| 검증 도구 | 로그의 첫 Map Check가 아니라 마지막 결과만 판정하도록 수정 |

## 시험맵과 Mission

공유 맵:

`/Game/Drone/Maps/TestMap/Lvl_DroneTutorialMissionTest`

독립 Mission:

1. `DA_Mission_Tutorial_Hover`
2. `DA_Mission_Tutorial_Forward`
3. `DA_Mission_Tutorial_Heading`
4. `DA_Mission_Tutorial_GateFlight`
5. `DA_Mission_Tutorial_FPV`
6. `DA_Mission_Tutorial_Payload`
7. `DA_Mission_Tutorial_UGV_NPC`
8. `DA_Mission_Tutorial_UGV_Turret`

맵을 직접 Play하지 말고 `/Game/Drone/Maps/Lvl_DroneFrontEnd`에서 원하는 Mission을 선택한다. 그래야 선택 기체 제한, Director, HUD, 제한 시간, 결과와 재시도를 모두 확인할 수 있다.

## 자동 검증 결과

- `DroneEditor Win64 Development`: 성공
- Tutorial Map Rebuild: 성공
- Tutorial Map Validate: 성공
- 최종 Map Check: `0 errors / 0 warnings`
- 집중 회귀 9개: 모두 성공
  - `Drone.Tutorial.MissionLessonsTestMap`
  - `Drone.Tutorial.HeadingZone`
  - `Drone.Mission.FrameworkAssets`
  - `Drone.Mission.ObjectiveRules`
  - `Drone.Weapons.GroundUGV`
  - `Drone.Integration.ExtendedRoleDrones`
  - `Drone.Flow.Contract`
  - `Drone.Flow.FrontEndContract`
  - `Drone.Flow.FrontEndPIE`

전체 `Drone.*` 회귀는 51개 성공, 기존 기준선 7개 실패다. 실패는 이번 Mission 변경에서 생긴 항목이 아니다.

- NPC Smart Object 맵이 확장됐지만 테스트가 과거 Actor 수를 정확히 기대한다.
- Shotgun Systems PIE에서 Drone 감지와 Volley가 시작되지 않는 기존 문제가 남아 있다.
- 보호 중인 Production Training 맵에 예전 Course/Gate가 있다고 가정하는 테스트가 실패한다.

이 세 영역은 팀원 맵을 자동으로 덮어쓰지 않고 별도 정비 작업으로 처리해야 한다.

## 사용자가 화면에서 확인할 항목

1. 8개 Mission이 로비에 모두 보이는지 확인한다.
2. 각 Mission에서 허용된 기체 하나만 선택되는지 확인한다.
3. 전진 Trigger와 회전 Zone의 거리·크기가 적당한지 본다.
4. Gate 4개가 번호 순서와 정방향 통과를 명확히 안내하는지 본다.
5. UGV 좌클릭 총이 상부 조준 방향으로 나가고 NPC가 4발에 죽는지 본다.
6. UGV 우클릭 유탄의 낙차와 350cm 반경이 체감상 적당한지 본다.
7. Retry 뒤 Trigger, Heading 진행, 표적 체력이 초기화되는지 본다.

수동 확인 결과에 따라 수치만 Blueprint/C++ 기본값에서 조정하고, Mission Event·Tag 구조는 유지한다.
