# Drone 재밍 Greybox 구현·배치 가이드

재머 본체 피격 캡슐의 여유·메시 교체·조정은 [현재 피격 정본](DRONE_MISSION_FRAMEWORK_GUIDE.md#재머-본체-피격-캡슐)을 따른다. 재밍 효과 범위와 별도인 피격 표면이다. 현재 재밍 정책과 Radar 조정은 [Mission 가이드](DRONE_MISSION_FRAMEWORK_GUIDE.md#재밍-radar-bp-설정시험)를 따른다. Noise→NO SIGNAL·입력 차단/복구를 사용하며 속도 저하로 처리하지 않는다. M3/M4는 [현재 단계별 Story 정책](DRONE_MISSION_FRAMEWORK_GUIDE.md#실패-처리와-체크포인트)을 따른다. 아래2026-09-23 Greybox 기록은 공통 구조/과거값 참고이며 최신 게임 규칙·검증을 대신하지 않는다.

## 왜 필요한가

드론이 방해 구역에 들어가면 신호 상태와 조작 반응을 일정한 규칙으로 바꾸고, 벗어나거나 Jammer를 무력화했을 때 회복시키기 위함이다. 입력을 무작위로 버리는 방식은 테스트가 어렵고 조작감을 예측하기 어려워 사용하지 않았다. 실제 재밍 장비의 물리·군사 성능을 재현하지 않는다.

## 어느 클래스가 담당하는가

| 클래스·파일 | 책임 |
|---|---|
| `Source/Drone/Signal/DroneSignalTypes.h` | 단계 `None/Weak/Moderate/Strong`와 HUD·Pawn이 받는 Snapshot |
| `DroneSignalComponent.h/.cpp` | 드론마다 활성 방해 Source를 보관, 가장 강한 Source로 단계·신호율·반응 배율 계산. Tick 없음 |
| `DroneJammingVolume.h/.cpp` | Pawn Overlap Box, 강도와 활성 상태, 이탈/무력화 Event. Tick 없음 |
| `DronePrototypePawn.h/.cpp` | 기본 비행 튜닝값에 강한 단계의 `ControlResponseMultiplier`를 적용하고 복원. 반복 중첩 곱셈 없음 |
| `DronePrototypePlayerController.cpp`, `DroneFlightHUDWidget.h/.cpp` | 선택한 Pawn의 Signal 구독/해제, 신호율·단계 경고 표시, Blueprint 영상 노이즈 연출용 Snapshot Event |
| `DroneMissionObjectiveTypes.h`, `DroneMissionDirector.h/.cpp` | `Jamming Exited`, `Jammer Disabled` 목표 Rule과 Map Zone의 C++ Event 연결 |

헤더에는 조정할 Threshold·강도·Event·getter를 선언하고 CPP에는 Overlap→Source 갱신→Snapshot 방송→Pawn/HUD 적용 흐름을 넣었다. Mission Director는 게임 진행용 C++ Event를 구독한다. Zone의 Blueprint Assignable Event는 별도로 남겨 사운드·이펙트 연출에 사용할 수 있다.

## 공통 Greybox 조정 위치

첫 Greybox 기본값일 뿐 최종 밸런스가 아니다.

| 값 | 기본 | Editor 위치 |
|---|---:|---|
| 약함/중간/강함 시작 | `0.20 / 0.50 / 0.80` | Drone Integration BP → `SignalComponent` → Class Defaults |
| 중간/강함 영상 노이즈 강도 데이터 | `0.35 / 0.70` | 같은 Component의 `Presentation` |
| 강함 반응 | 현재 속도 배율 변경 없음·링크 손실 때 입력 차단 | [현재 Signal/Radar 정책](DRONE_MISSION_FRAMEWORK_GUIDE.md#재밍-radar-bp-설정시험) |
| Zone 방해 세기 | `0.60` | `DroneJammingVolume` BP 또는 Map Instance |
| Zone Box 크기 | 반폭 `1000/1000/500 cm` | Zone `JammingBounds` Box Extent |

가장 강한 Zone을 사용하며 여러 세기를 더하지 않는다. 현재 Signal/링크 손실·회복·면역과 실제 화면/입력 확인은 [Mission 가이드](DRONE_MISSION_FRAMEWORK_GUIDE.md#재밍-radar-bp-설정시험)를 따른다. 아래 날짜별 자동 검사 이력은 당시 정책의 결과다.

Figma에서 확인한 광섬유 Drone은 예외다. 해당 Drone Definition의 `ImplementedCapabilities`에 `JammingImmunity`가 들어간 경우에만 Signal Component가 활성 Source의 영향을 무시한다. 면역을 껐을 때도 아직 Box 안이면 즉시 원래 방해 단계로 돌아간다. 현재 `/Game/Drone/Data/Drones/DA_Drone_FiberOptic_Greybox`와 `/Game/Drone/Integrations/RoleDrones/BP_DroneFiberOpticIntegration`이 이 Capability와 `ImpactDetonation`을 구현한다. 기존 Scout·FPV·Drop에는 면역을 임의로 넣지 않았다.

## Blueprint와 Mission Data Asset 설정

1. 팀원 Production Training Map이 아닌 검증용 맵에 `DroneJammingVolume` 또는 그 자식 BP를 배치한다. `JammingBounds`로 드론이 지나갈 영역을 잡고 `NormalizedJammingStrength`를 설정한다. 기본 0.60이면 중간 단계다. 강함 시험에는 0.80 이상을 설정한다.
2. 배치한 Zone의 `Details → Actor → Tags`에 Mission Rule `TargetId`와 동일한 Name을 넣는다. Tag가 비면 해당 종류의 모든 Zone 사건을 목표로 받을 수 있다.
3. Mission Definition의 `ObjectiveRules`에 `Jamming Exited` 또는 `Jammer Disabled`를 목표 순서에 맞게 추가한다. 이는 배치 예시이며 실제 Story Mission의 최종 순서·기지 위치·성공 규칙은 현재 미정이다. 설정법은 [Mission 목표 Rule 가이드](DRONE_MISSION_OBJECTIVE_RULE_GUIDE.md)를 따른다.
4. 이탈 목표는 활성 Zone 안에 들어왔던 출격 드론이 Box 밖으로 나갈 때만 보고한다. Jammer 해제 목표는 Zone BP가 명시적으로 `DisableJammer()`를 호출했을 때 한 번 보고한다. 무력화 방식(접근·파괴·상호작용)은 미정이며 자동 파괴 규칙은 없다.
5. HUD Noise/NO SIGNAL·입력 차단/복구와 FiberOptic 면역은 [현재 Radar 시험 절차](DRONE_MISSION_FRAMEWORK_GUIDE.md#재밍-radar-bp-설정시험)를 따른다. 별도 파괴 후3초 화면과 Signal Snapshot을 같은 이벤트로 취급하지 않는다.

## Editor에서 테스트

1. 검증용 맵에서 PIE 출격 후 Zone 밖의 HUD 신호 `100% | 정상`을 확인한다.
2. Zone 가장자리→중심에서 신호율/Noise가 변하고 링크 손실 임계점에 NO SIGNAL·입력 차단이 되는지 확인한다. 잔여 속도/중력은 유지하고 속도 배율을 줄이지 않는다. 정확한 임계값과 복원은 Mission 가이드를 따른다.
3. Zone 밖으로 나가면 신호 100%, 원래 최대 속도/가속도로 복원되는지 본다. 두 Zone이 겹치면 강한 쪽이 우선이고 강한 Zone만 나가면 남은 Zone 단계로 돌아간다.
4. `Jamming Exited` 또는 `Jammer Disabled` Rule이 활성일 때 같은 Tag Zone에서 해당 사건을 발생시켜 HUD 목표 진행값을 확인한다. `DisableJammer()` 두 번째 호출은 `false`이며 Mission 진행도 중복되지 않아야 한다.
5. Commandline 자동화 `Drone.Signal.StageContract`는 단계·겹침·복원·면역 on/off·무효 강도·한 번만 해제 계약을, `Drone.Mission.ObjectiveRules`는 재밍/Story 분기를, `Drone.UI.FlightHUDTelemetryBinding`는 강한 경고·노이즈 강도 전달·이탈 뒤 표시 복원을 확인한다. 2026-09-16 관련 회귀 8/8 Success. 실제 화면·맵 배치 PIE는 아직 미확인이다.
6. 광섬유 Drone을 선택해 0.85 Zone 안에서도 신호가 `100% | 정상`을 유지하는지, 같은 위치에서 Scout/FPV/Drop은 강한 방해를 받는지 비교한다. 2026-09-23 `Drone.Integration.ExtendedRoleDrones` 자동화는 Definition·Capability·Visual 계약을 통과했으며 실제 Zone 화면 비교는 남았다.

## 문제가 생기면

- 경고가 안 뜨면 해당 Pawn에 `SignalComponent`가 있는지, Zone Box가 Pawn과 Overlap하는지, HUD가 선택한 Pawn의 Signal Source를 받고 있는지 확인한다.
- 강한 방해가 안 되면 Zone 강도가 `StrongThreshold` 이상인지, 실제 현재 겹치는 Zone 중 가장 강한 값이 무엇인지 확인한다.
- 임무가 진행되지 않으면 현재 Objective의 Event·TargetId와 Zone Actor Tags, 실제 선택된 출격 Drone의 Zone 이탈인지 확인한다. Mission 시작 전에 Zone이 Map에 있어야 Director가 자동 구독한다. 나중에 Spawn한 Zone은 BP에서 `ReportObjectiveEvent()`를 명시 연결해야 한다.
- 복원이 안 되면 모든 Zone에서 나왔는지, 다른 Zone Source가 남아 있는지, Pawn의 기본 비행 튜닝값을 확인한다.

남은 작업은 최종 Mission 내용 확인 후 검증용 Mission Map/Data Asset 연결, 영상 잡음 WBP 표현, 목표 정보 손실의 화면 규칙 결정, PIE 수동 테스트다. Figma는 현재 이 PC에서 읽기 연결이 없어 화면 내용을 근거로 확정하지 않았다.


10/04 현재 C PC Claude: Moderate HUD 문구를 신호 불안정으로 정정·PlayerFacingTextContract 자동 검증됨. VideoNoiseIntensity/Blueprint 데이터는 있지만 영상 Noise 효과는 아직 미연결이다.
