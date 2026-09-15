# Mission 목표 Rule 구현·사용 가이드

기준: 2026-09-16 로컬 작업. 커밋·푸시 전에는 두 PC에 자동으로 전달되지 않는다.

## 왜 필요한가

기존 `InitialObjectives`는 화면에 보여줄 문구만 있었고 `CompleteCurrentObjective()`로 1회 완료했다. 정찰 표적 2개, 제한 시간 30초, 특정 기지 Actor처럼 사건별 조건을 구분하려면 미션 데이터와 실행 상태를 분리해야 한다. 기존 Training은 깨지지 않도록 한 Lap 목표를 같은 새 형식으로 이행했다.

## 담당 클래스와 코드 구조

| 위치 | 책임 |
|---|---|
| `Source/Drone/Mission/DroneMissionObjectiveTypes.h` | 사건 종류 `EDroneMissionObjectiveEvent`, ID·설명·수량·시간·대상 ID 데이터 `FDroneMissionObjectiveRule` |
| `DroneMissionDefinition.h/.cpp` | Data Asset의 `ObjectiveRules`와 ID 중복·수량·시간 유효성 검사. 배열이 비어 있으면 기존 문구 목표 사용 |
| `DroneMissionDirector.h/.cpp` | 현재 목표와 타이머 소유, 사건을 현재 Rule과 대조, Actor 중복 계산 방지, 성공·실패 한 번만 Flow에 보고 |
| `DroneMissionRuntimeTypes.h` | UI가 읽는 목표 Event·대상 ID·제한 시간·진행값 사본 |
| `DroneMissionObjectiveWidget.cpp` | 현재 목표와 `진행 n/m`, 제한 시간이 있으면 설정된 `제한 n초` 표시 |
| `DroneMissionPlayerController.cpp` | 기존 문구 또는 새 Rule 중 하나라도 있으면 Drone 출격 가능 |
| `DroneMissionReturnZone.h/.cpp` | 플레이어 Drone의 Box Overlap을 `Return To Base` 사건으로 보고하는 배치형 Trigger |

헤더에는 데이터 필드·공개 `ReportObjectiveEvent()`·남은 시간 getter·Event Handler를 선언하고, CPP에는 초기 목표 생성·Event 구독·타이머 시작/정리·진행/종료를 구현했다. UI는 Actor를 매 프레임 검색하지 않고 Director의 Snapshot 변경 Delegate를 받는다. 남은 시간의 초 단위 실시간 표시는 아직 기본 HUD에 없다. 필요하면 BP에서 `GetCurrentObjectiveTimeRemainingSeconds()`를 표시할 수 있다.

## Blueprint/Data Asset 설정

`DA_Mission_Tutorial_Training`에는 기존 설명을 유지한 `Objective.TrainingLap / Training Lap / 1회 / 시간 제한 없음` Rule이 들어 있다. 실제 팀원 Training 맵은 이행 과정에서 수정하지 않았다. 다른 Mission Data Asset을 만들 때는 `ObjectiveRules`를 순서대로 추가한다. Rule이 하나라도 있으면 `InitialObjectives`는 런타임 목표로 사용하지 않는다.

예시(최종 Mission 규칙이 아니라 편집 방법):

| 필드 | 예시 | 의미 |
|---|---|---|
| `ObjectiveId` | `Recon.Base` | Mission 안에서 중복되지 않는 ID |
| `Description` | `정찰 표적 2개 스캔` | HUD 문구 |
| `Event` | `Recon Scan` | 목표가 받아들일 사건 |
| `RequiredProgress` | `2` | 다른 Actor 두 개가 필요 |
| `TimeLimitSeconds` | `30` | 활성화 순간부터 30초; `0`이면 무제한 |
| `TargetId` | `MissionTarget.Base` | 해당 Actor의 Details → Actor → Tags에 같은 Name을 넣는다. 비우면 해당 사건의 모든 Actor 허용 |
| `StoryFactCondition` | `Fact Present` | 이전 성공 결과의 Fact가 있을 때만 이 목표를 실행 목록에 넣는다 |
| `StoryFactId` | `Story.TargetStillAtLarge` | 조건이 `Always`가 아닐 때 검사할 GameInstance 수명 ID |

드론이 정상 Scan을 완료하면 Director가 자동으로 `Recon Scan` 사건을 받는다. Payload는 **의도된 투하 표적에 적중한** `OnPayloadResolved`만 `Payload Delivered`로 센다. `UDroneHealthComponent`가 붙은 맵 시작 시점 Actor의 사망은 `Target Destroyed`로 받는다. Mission 시작 뒤 새로 Spawn되는 파괴 대상은 현재 자동 사망 구독 대상이 아니므로 그 Actor BP의 `OnDeath`에서 Director의 `ReportObjectiveEvent(Target Destroyed, DeadActor)`를 연결한다.

귀환의 최종 기지 위치는 미정이다. 현재는 `DroneMissionReturnZone`의 `ReturnTrigger` Box를 필요한 Mission Map에 배치하고 크기를 BP/Instance에서 조정하면 된다. 플레이어가 출격한 Drone만 Overlap Event를 보고하고, 현재 Rule이 `Return To Base`여야 진행한다. Rule의 `TargetId`를 쓴다면 Zone Actor Tags도 같아야 한다. 현재 어떤 Production 맵에도 Zone을 자동 배치하지 않았다. 별도 연출/조건이 필요한 귀환 Actor BP는 `Get Player Controller → Cast to DroneMissionPlayerController → Get Mission Director → ReportObjectiveEvent(Return To Base, 귀환 Actor)` 경계를 사용할 수 있다.

`CompleteCurrentObjective()`는 기존 Training/시험용 명시 호출로 남아 있으므로 새 Mission BP에서는 일반 진행에 사용하지 않는다. 새 목표는 사건 Delegate 또는 `ReportObjectiveEvent()`로 진행한다.

`Jamming Exited`와 `Jammer Disabled` Rule은 맵 시작 시점의 `DroneJammingVolume` C++ Event를 Director가 구독한다. 첫 사건은 실제 출격한 Drone이 활성 Box를 나갔을 때, 둘째는 BP/코드가 Zone의 `DisableJammer()`를 명시 호출했을 때만 진행한다. Zone `Actor Tags`와 Rule `TargetId`가 있으면 일치해야 한다. 재밍 강도·HUD·비행 설정과 아직 없는 영상 Noise 표현은 [재밍 Greybox 가이드](DRONE_JAMMING_GREYBOX_GUIDE.md)를 본다.

## Story Fact로 두 스토리안 설정

Mission 성공 뒤 다음 Mission의 목표 구성이 달라져야 하면 `UDroneMissionDefinition`의 `StoryFactsGrantedOnSuccess`와 `StoryFactsRemovedOnSuccess`를 사용한다. Fact는 성공할 때만 한 번 적용되고, 로비 복귀·다음 맵 전환 동안 유지된다. 재도전 실패로 성공 Fact가 덮어써지지 않는다.

Figma Mission 2→3의 두 안은 다음처럼 둘 다 설정할 수 있다.

| Mission 2 선택 | Granted | Removed | Mission 3 조건 |
|---|---|---|---|
| 차량은 미끼 | `Story.TargetStillAtLarge` | `Story.TargetEliminated` | 표적 처리 목표를 `FactPresent / Story.TargetStillAtLarge`로 설정 |
| 차량에 실제 탑승 | `Story.TargetEliminated` | `Story.TargetStillAtLarge` | 이미 처리된 후속 목표를 `FactPresent / Story.TargetEliminated`로 설정 |

두 Fact를 같은 Mission에서 동시에 추가/제거할 수 없고, 중복·빈 ID도 Definition 검증에서 거부한다. `Always` 조건에는 `StoryFactId`를 비우고, `FactPresent/FactAbsent`에는 ID를 반드시 넣는다. 조건이 맞는 Rule이 하나도 없다면 Director 초기화는 실패하므로 다음 Mission에는 가능한 분기마다 최소 하나의 목표가 있어야 한다.

## Editor 시험과 정상 결과

1. Mission Data Asset에서 서로 다른 Objective ID, 사건 종류, 수량, 선택적 제한 시간/Target ID를 설정한다.
2. Target ID가 있으면 해당 맵 Actor Tags에 정확히 같은 Name을 넣는다.
3. PIE로 출격한 뒤 정찰·투하·대상 사망 또는 귀환 Overlap을 발생시킨다.
4. HUD의 목표 ID 순서와 `진행 n/m`이 바뀌고 마지막 목표 뒤 결과 화면으로 한 번만 이동하는지 확인한다.
5. 시간 제한이 있으면 제한 만료 때 Failure가 한 번만 보고되고, 완료 뒤 타이머가 다음 목표로 다시 시작되는지 본다.

현재 자동화 `Drone.Mission.ObjectiveRules`는 잘못된 사건/Tag 거부, 서로 다른 Scan Actor 2개, 같은 Actor 중복 거부, Delivery→Jamming Exited→Jammer Disabled→Return→Success, 종료 후 사건 거부와 Mission 2→3의 양쪽 Story Fact 목표 필터를 검증한다. 2026-09-16 Prototype 면역까지 포함한 묶음 회귀 8/8 Success다. 저장 Training Asset의 Lap Rule, 실제 역할 기능, 귀환/재밍 Zone의 화면 배치는 별도 수동 확인이 남아 있다.

## 이상할 때 확인

- 진행 0: `Event`가 현재 목표와 같은지, 표적 `Actor Tags`와 `TargetId` 철자가 같은지, Scan이 실제 완료됐는지, Payload가 intended target에 맞았는지 본다.
- 파괴 목표 미진행: 대상에 `UDroneHealthComponent`가 있는지, Mission 시작 전에 맵에 있었는지 확인한다. 동적 Spawn 대상은 BP `OnDeath` 연결이 필요하다.
- 귀환 미진행: Overlap Actor가 드론인지, 해당 PlayerController가 Mission Director를 소유하는지, 귀환 Actor를 EventActor로 전달했는지 확인한다.
- 재밍 목표 미진행: Zone이 Mission 시작 전에 맵에 있었는지, 현재 Event와 Zone Tags가 맞는지, 실제 출격 Drone이 이탈했는지, 해제는 `DisableJammer()`를 호출했는지 확인한다.
- 출격 거부: `ObjectiveRules`가 모두 비어 있고 사용 가능한 `InitialObjectives`도 없는지, 중복 Objective ID·0 수량·음수 시간 제한이 있는지 확인한다.
- 제한 시간 중 이상한 완료/실패: Director는 목표 교체·Mission 종료·EndPlay에 타이머와 Delegate를 정리한다. 다른 BP가 `CompleteCurrentObjective()` 또는 `ReportMissionFailure()`를 중복 호출하는지 본다.
