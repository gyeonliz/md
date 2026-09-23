# Figma Mission 기획 ↔ 현재 구현 매트릭스

기준일: 2026-09-23. Figma `Project:Droner` Page 1의 최상위 148개 항목을 읽기 전용으로 확인한 2026-09-18 기준을 유지하고, 이후 코드 구현 상태만 갱신했다. Figma 원본은 수정하지 않았다.

## 읽은 기준과 충돌 처리

- 전체 세계관/맵 배정: Figma node `1:3`
- 초기 기능 메모: `46:3`, `49:2`
- Drone 기능 메모: `53:10`
- 최신형 Mission 선택 화면: Mission 1 `195:533`, Mission 2 `273:73`, Mission 3 `282:105`, Mission 4 `283:136`
- 최신 공통 흐름/화면: Title~Mission 진입 Flow `363:4`, Mission 선택 Greybox `366:523`, 공중 Drone 공통 UX `403:72`, Racing UI 참고 `406:2`, `406:45`
- 동일 파일 안에서도 초기 메모와 최신형 화면, Mission 2와 Mission 3 대사 사이에 내용 차이가 있다. 구현은 둘 중 하나를 하드코딩하지 않고 Story Fact 분기로 지원한다. 최종 문구·순서는 사용자 결정 뒤 Data Asset으로 저장한다.
- 실제 국가명은 확정하지 않는다는 Figma 문구와 기존 사용자 기준을 유지한다. J3C를 실제 발주처·협력사로 표현하지 않는다.

## 전체 흐름

Figma에서 확인한 큰 구조는 `튜토리얼 + Story Mission 4개 / 환경 맵 3개`다.

## 2026-09-18 최신 UX 재확인

- 화면 흐름은 `게임 실행 → 타이틀 → 시작 → 미션 선택 → 선택 미션 설명 → 시작 → 로비 → 드론 선택 → 인게임` 순서다. 사람 플레이어 전환 화면은 현재 기준에 넣지 않는다.
- Mission 선택 Greybox는 왼쪽 미션 1~4 버튼, 중앙/측면 이미지·설명 영역, 나가기와 로고를 사용한다. 선택한 미션 버튼이 활성화될 때 설명 UI가 열린다.
- 공중 Drone 공통 HUD 필수 항목은 배터리, ALT 고도계, 숫자 속도, Heading, 풍향/풍속, HP, 기체명, 목표 현황이다.
- Racing UI 참고안은 Lap/기록, 감도·Rate 커브, 코스/체크포인트 개요, 기체 튜닝, 실시간 FPV HUD와 조종 스틱 오버레이를 포함한다. 실패 사망보다 즉시 Restart와 Quit/Exit를 핵심 흐름으로 본다.
- 추가 후보는 카운트다운, 배터리 HUD, Replay, 이전 기록 Ghost다. `한 맵에 여러 코스가 나타나는 방식`과 현재 Tutorial Course 데이터 구조를 고려해 트랙 선택 UI는 그대로 복제하지 않고 재해석한다.
- 적 NPC 메모에는 감지 후 공격까지의 Delay를 조절 가능하게 하라는 요구가 있다. Controller의 `PersonalWeaponInitialAimDelaySeconds` 기본 1.0초가 이 계약을 담당한다.

| 구분 | Figma 내용 | 현재 코드 기반 | 남은 실제 콘텐츠 |
|---|---|---|---|
| Tutorial | 기본 비행, 자폭, 드랍, UGV/포탑 훈련 | Flight Profile, Easy/Manual, Stable/Balanced/Agile, Gate/Lap, Recon/FPV/Drop, HUD | 호버링 범위 Rule, 세분화된 브리핑/완료 WBP, UGV 훈련 |
| Mission 1 | `골든 타임`: 드랍 드론으로 부상 요원에게 구급품 전달, 정보 회수 | Payload 픽업/드랍, `Payload Delivered`, 시간 제한, Actor Tag, Drone 사망 실패 | 사막 마을 Mission Map/DA, 요원·구급품·정보 회수 대상, Line/그물 실패 Rule |
| Mission 2 | `인터셉트`: 이동 차량을 FPV로 기지 도착 전 격파 | FPV Arm/충돌 자폭, Target Destroyed, 시간 제한, 차량/자동포탑 기반 | 목표 차량 Mission Actor/Route, 도착 실패 Trigger, 잔해 Scan/스토리 분기 DA |
| Mission 3 | `베일 브레이커`: 광섬유 Drone으로 Jammer 무력화 후 UGV·다른 Drone으로 거점/예비 방공망 무력화 | Jamming Zone, 면역 Capability, Jammer Disabled, AI/MG/자동포탑, 목표 Rule, 광섬유·UGV Definition/Integration Pawn | 한 Mission 내 Drone 교대, 산악 기지 Map/DA, 방공망 Actor, 두 새 기체 화면·밸런스 확인 |
| Mission 4 | `엔드게임`: 본진 방어 체계와 방공망을 무력화 후 장거리 타격/엔딩 | 순차 목표 Rule, Target Destroyed, AI·포탑 기반, 결과 Flow | 모든 Drone/UGV 교대, 본진 Map/DA, 장거리 타격 Sequence, 엔딩 Cinematic |

현재 저장된 Mission Definition은 Training 하나다. 표의 Story Mission 이름·목표는 Figma에서 확인했지만, 실제 Mission Asset/맵은 아직 만들지 않았으므로 플레이 가능한 것으로 기록하지 않는다.

## Mission 2 → 3 두 스토리안 지원

Figma 안에는 다음 두 문맥이 함께 있다.

1. 차량은 미끼이고 오마르는 타지 않음 → 잔해 Scan으로 오인 정보 확인 → Mission 3에서 실제 위치/처리를 확정.
2. 오마르가 차량에 탑승한 것으로 브리핑 → Mission 3 도입 대사에서 이미 처리됐다고 전제.

2026-09-16 코드는 둘 다 지원하도록 만들었다.

| 설정 | Mission 2 성공 Fact | Mission 3 조건 목표 |
|---|---|---|
| 미끼 차량 | `Story.TargetStillAtLarge` 추가, `Story.TargetEliminated` 제거 | `FactPresent: Story.TargetStillAtLarge`인 표적 처리 목표 포함 |
| 실제 탑승 차량 | `Story.TargetEliminated` 추가, `Story.TargetStillAtLarge` 제거 | 표적 처리 목표 제외, `FactPresent: Story.TargetEliminated` 후속 목표 포함 |

`UDroneGameFlowSubsystem`이 Story Fact를 GameInstance 동안 유지한다. Mission 재도전·로비 복귀로 Fact가 사라지지 않으며, 성공할 때만 Mission Definition의 `StoryFactsGrantedOnSuccess`와 `StoryFactsRemovedOnSuccess`를 원자적으로 적용한다. `FDroneMissionObjectiveRule`의 `StoryFactCondition`은 `Always / FactPresent / FactAbsent`를 지원한다. 조건이 맞지 않는 목표는 Director 초기화 때 실행 목록에서 빠진다.

두 분기는 자동화에서 실제로 각각 실행해 확인했다. 현재는 최종 선택을 기다리므로 Story Mission Data Asset에 어느 Fact를 넣을지는 보류했다.

## 광섬유 재밍 면역

Figma node `53:10`에는 광섬유 Drone의 `재밍에 면역` 요구가 있다. `EDroneGameplayCapability::JammingImmunity`는 이미 데이터 계약에 있었지만 동작 연결이 없었고, 2026-09-16 다음처럼 연결했다.

- 선택된 Drone Definition의 `ImplementedCapabilities`에 `JammingImmunity`가 있을 때만 `UDroneSignalComponent`가 활성 방해 Source를 무시한다.
- 면역 상태에서도 Source 목록은 유지하므로 능력을 끄면 현재 겹친 가장 강한 재밍 단계가 즉시 복원된다.
- 일반 Drone은 기존처럼 약함/중간/강함 경고와 강한 단계 비행 둔화를 받는다.
- `/Game/Drone/Data/Drones/DA_Drone_FiberOptic_Greybox`와 `/Game/Drone/Integrations/RoleDrones/BP_DroneFiberOpticIntegration`을 추가했다. Sting Visual, `JammingImmunity + ImpactDetonation`, 1인칭 기본값을 사용하며 기존 Scout/FPV/Drop에는 면역을 부여하지 않았다.
- `/Game/Drone/Data/Drones/DA_Drone_GroundUGV_Greybox`와 `/Game/Drone/Integrations/RoleDrones/BP_DroneGroundUGVIntegration`도 추가해 Mission 3 교대 대상으로 사용할 기반을 준비했다. Catalog/선택 Flow는 5종으로 확장됐지만 Mission 도중 실제 교대는 아직 없다.

## 구현 순서

1. 사용자 결정으로 Mission 2 스토리 Fact 기본값을 확정한다.
2. 완료: 광섬유 Drone과 UGV의 프로젝트 소유 Definition/Pawn 기반, 외부 Visual 참조, 5종 선택 Catalog와 자동화를 구현했다.
3. Mission 1 Vertical Slice를 먼저 만든다: Drop 출격 → 요원 Tag 대상 전달 → 선택적 정보 회수 → 시간/파괴 실패 → 결과.
4. 이동 차량과 도착 실패 Trigger를 만든 뒤 Mission 2 Vertical Slice를 구성한다.
5. 검증용 산악 기지 맵에서 구현된 광섬유 Drone → Jammer 해제 → 다른 Drone/UGV 교대 기능을 먼저 검증하고 Mission 3에 연결한다.
6. Mission 4는 1~3에서 검증한 교대·파괴·AI·포탑·Cinematic Event를 조합한다.

새 Story Map/Definition의 최종 이름·대상 수량·제한 시간·영상은 아직 저장값으로 확정하지 않는다. 팀원 Production Training Map은 이 작업에 사용하지 않는다.
