# Drone 프런트엔드·미션 진입 흐름 계획

기준일: 2026-09-03 (Asia/Seoul)

이 문서는 2026-09-03에 사용자가 확정한 새 게임 흐름의 최우선 기준이다. 기존의 `사람 Operator 조작 → NPC 대화 → Drone 전환` 구상은 폐기하며, 이미 구현된 적 NPC·Smart Object·전투 Greybox는 미션 맵 내부 요소로 계속 사용한다.

Figma `Project:Droner`는 화면 분위기와 세계관 참고 자료로만 읽는다. Figma 파일 자체는 수정하지 않았으며, 구현 상태의 근거는 Unreal 코드·Asset·빌드·실행 결과를 우선한다.

## 1. 확정 사용자 흐름

```text
게임 실행
→ 시작 트레일러
→ 로비
→ 미션 레벨 선택
→ 선택 항목 측면에 미션 설명 표시
→ 하단 시작 버튼
→ 선택 미션 트레일러/브리핑
→ 미션 맵 진입
→ 드론 선택
→ 미션 시작
→ 플레이 중 측면 UI에 현재 미션 목표 표시
→ 성공/실패 결과
→ 재도전 또는 로비 복귀
```

`시작 트레일러`와 `미션 트레일러`는 서로 다른 단계다. 시작 트레일러는 세계관과 파견 배경, 미션 트레일러는 선택한 임무의 장소·목표·위험 요소를 설명한다.

## 2. 폐기·유지 범위

### 폐기 또는 선행조건에서 제외

- 사람 Player Character 직접 조작
- Operator와 Drone 사이 실시간 Possess 전환
- 로비에서 걸어 다니며 NPC에게 미션을 받는 구조
- NPC 대화를 완료해야 미션이 열리는 구조
- Operator 전용 Input Mapping Context와 상호작용 키
- `SetViewTargetWithBlend`를 이용한 Character↔Drone 전환 상태

관련 코드는 아직 생산 구현하지 않았으므로 새로 만들지 않는다. 과거 계획 문서의 Operator/NPC 대화 항목은 역사 기록으로만 본다.

### 유지·재사용

- Drone Pawn, 고정 추적 Camera, Keyboard·Mouse·Gamepad 조작
- Telemetry와 Flight HUD
- Tutorial Course·Gate·Lap/Segment 기록
- Mission Director 후보와 성공·실패 Event 경계
- 적 NPC 순찰·감지·Cover·Rifle/Shotgun·MG Smart Object 전투
- Jamming, Crash, 귀환, 목표 획득 후보
- 아군 NPC/Smart Object Greybox는 환경 연출 후보로 보존하되 프런트엔드 흐름의 필수 기능으로 보지 않음

## 3. 런타임 책임 구조

### 영속 흐름 상태

프로젝트 소유 `GameInstanceSubsystem` 하나가 맵 전환 사이에 다음 최소 상태만 보존한다.

- 현재 Front-end 상태
- 선택한 Mission ID
- 선택 가능한 Drone 목록
- 최종 선택 Drone ID
- Mission 시작 요청 여부
- 직전 Mission 결과와 로비 복귀 요청

권장 상태는 아래와 같다.

```text
Boot
→ OpeningTrailer
→ LobbyMissionSelect
→ MissionTrailer
→ LoadingMissionMap
→ DroneSelect
→ InMission
→ MissionResult
→ LobbyMissionSelect 또는 LoadingMissionMap
```

Level Blueprint를 상태의 단일 기준으로 사용하지 않는다. Level Blueprint는 필요하면 해당 맵의 연출 호출만 담당하고, 선택 데이터와 전환 가능 여부는 C++ 흐름 계층이 관리한다.

### 데이터 자산

`Mission Definition`은 최소한 아래 정보를 가진 프로젝트 소유 Data Asset으로 계획한다.

- Mission ID와 한글 표시명
- 로비 측면 설명, 썸네일, 난이도·지역 표시 후보
- 미션 트레일러/브리핑 Media Source 또는 Sequencer 참조
- 로드할 Mission Map
- 허용 Drone ID 목록과 기본 Drone
- 시작 목표 목록
- 성공·실패 및 귀환 규칙 참조

`Drone Definition`은 아래 정보를 가진다.

- Drone ID와 한글 표시명
- 선택 화면 Preview Mesh 또는 Actor Class
- 실제 Spawn할 프로젝트 Integration Pawn Class
- 설명과 역할 태그
- 잠금 여부 후보

미션 설명과 목표 문자열을 Widget Blueprint에 직접 하드코딩하지 않는다. 첫 Greybox는 한 개 Mission·한 개 Drone으로 시작하되 배열과 ID 계약을 유지한다.

### UI 책임

| 화면 | 최소 표시 | 입력 결과 |
|---|---|---|
| 시작 트레일러 | 영상·자막, 건너뛰기 후보 | 종료 시 로비 이동 |
| 로비/미션 선택 | 미션 목록, 선택 강조 | 선택 Mission ID 갱신 |
| 측면 미션 설명 | 제목, 설명, 지역·난이도 후보 | 읽기 전용 |
| 하단 시작 영역 | 시작 버튼, 선택 유효성 | 미션 트레일러로 진행 |
| 미션 트레일러 | 선택 미션 브리핑 영상·자막 | 종료 시 Mission Map 로드 |
| 드론 선택 | 허용 드론 목록, Preview, 설명 | Drone ID 확정 후 출격 |
| 인게임 목표 패널 | 현재 목표, 진행값, 선택 보조 거리 | Mission Event를 표시만 함 |
| 결과 화면 | 성공/실패, 주요 기록, 재도전·로비 | 흐름 상태 전환 |

Widget은 상태를 직접 추론하지 않고 C++의 상태 변경 Event와 Mission Runtime Snapshot을 받아 표시한다. Animation·Layout·Font·색상은 UMG가 맡는다.

## 4. 맵과 Content 경계

새 생산 자산은 계속 `/Game/Drone` 아래에 둔다. 아래 경로명은 첫 구현 전 확정할 권장안이다.

```text
/Game/Drone/FrontEnd/Maps/
/Game/Drone/FrontEnd/UI/
/Game/Drone/FrontEnd/Media/
/Game/Drone/Data/Missions/
/Game/Drone/Data/Drones/
/Game/Drone/Mission/UI/
/Game/Drone/Mission/Directors/
/Game/Drone/Integrations/<Pack>/
```

- 로비는 전용 가벼운 Front-end Map 하나에서 시작한다.
- 환경 맵은 `/Game/Drone/Maps`의 중앙 사본을 사용한다.
- 공급사 Map의 GameMode·Pawn·Input을 그대로 상속하지 않는다.
- 미션 맵 진입 직후에는 Drone을 자동 Spawn/Possess하지 않고 드론 선택 UI를 먼저 연다.
- 드론 확정 후에만 해당 Integration Pawn을 Spawn/Possess하고 Mission Director를 시작한다.

## 5. 첫 Vertical Slice 개발 순서

| ID | 작업 | 완료 조건 |
|---|---|---|
| FLOW-00 | 새 흐름 문서 기준선 | Operator 조작 폐기와 확정 화면 순서가 WORKBOARD·STATUS·CONTEXT에 동일하게 기록됨 |
| FLOW-01 Done | Flow 상태·Mission/Drone 데이터 계약 | 실제 Training Mission/Scout Drone 등록, 정상·오류·중복·재도전·로비 복귀 계약 자동 검증 통과 |
| FLOW-02 Done | 시작 트레일러 → 로비 | 새 실행에서 정적 Opening 종료 후 같은 Root가 로비를 표시하며 Widget 생성 1회·중복 전환 0 PIE 통과 |
| FLOW-03 Done | 로비 미션 선택 UI | Training Mission 선택 시 Definition 기반 측면 설명이 바뀌고 하단 시작으로 MissionTrailer 상태 확정, 오류·중복 거부 PIE 통과 |
| FLOW-04 | 미션 트레일러 → 맵 로드 | 선택한 Mission Definition의 영상/대체 화면이 끝난 뒤 지정 Map으로 이동 |
| FLOW-05 | 맵 내 드론 선택 | 허용 목록 밖 선택을 거부하고 확정 전 Drone Pawn 0대, 확정 뒤 1대만 Spawn/Possess |
| FLOW-06 | Mission 시작·목표 UI | Drone 확정 뒤에만 Mission이 시작되고 측면 목표 패널이 Event 기반으로 갱신됨 |
| FLOW-07 | 결과·재도전·로비 | 성공/실패에서 재도전과 로비 복귀가 중복 전환 없이 동작 |
| FLOW-08 | 전체 반복 검증 | 새 실행부터 결과까지 3회 반복해 Widget·Pawn·IMC·Delegate·Mission 상태 중복 0 |

첫 기능 Vertical Slice는 `Lvl_DroneTraining`을 Tutorial Mission 한 개로 등록해 기존 Course/Gate/HUD를 재사용한다. Front-end 골격이 안정된 뒤 MilitaryCamp·MilitaryBase·Battlefield 후보를 실제 Story Mission에 연결한다.

## 6. 다음 구현의 기술 기준

- C++: Flow 상태, ID 검증, Data Asset 계약, 맵 전환 요청, Mission 시작·종료, Event 수명주기
- Blueprint/UMG: 트레일러 자산 연결, 목록·측면 설명·버튼 Layout, 드론 Preview, 목표 패널 외형
- Drone 입력 IMC: Drone Possess 뒤 한 번만 등록하고 UnPossess/EndPlay에서 제거
- Front-end 입력: UI 전용 PlayerController 또는 공용 UI 계층 한 곳에서만 처리
- Mission Director: Drone 선택 완료 Event 전에는 목표 타이머·AI 교전·Lap 기록을 시작하지 않음
- Trailer: 실제 영상이 준비되지 않으면 Sequencer 또는 정적 대체 화면으로 흐름부터 검증
- UI 텍스트: 한글을 기준으로 작성하고 목표·설명은 데이터에서 공급

### FLOW-01 첫 코드 묶음 권장안

```text
Source/Drone/Flow/
├─ DroneGameFlowTypes.h
├─ DroneGameFlowSubsystem.h/.cpp
└─ Tests/DroneGameFlowContractTest.cpp

Source/Drone/Mission/
├─ DroneMissionDefinition.h/.cpp
└─ DroneDefinition.h/.cpp
```

- `DroneGameFlowTypes`: 상태 Enum과 Mission/Drone 선택 Snapshot
- `DroneGameFlowSubsystem`: 허용된 상태 전환, 선택 ID 보존, 중복 요청 거부
- `DroneMissionDefinition`: 로비 설명·브리핑·Map·허용 Drone·목표 시작 데이터
- `DroneDefinition`: 표시 정보·Preview·실제 Spawn Pawn Class
- `DroneGameFlowContractTest`: 정상 순서, 잘못된 ID, 중복 Start, 결과 뒤 재도전/로비 초기화 계약

FLOW-01에서는 Widget Blueprint, 동영상, 실제 Map 이동과 Pawn Spawn을 만들지 않는다. 먼저 데이터와 상태 계약을 자동화로 고정한 다음 FLOW-02부터 화면을 연결한다.

### 2026-09-03 FLOW-01~03 구현 결과

```text
GameInstance
└─ UDroneGameFlowSubsystem
   ├─ DA_Drone_Scout_Greybox를 먼저 Catalog 등록
   ├─ DA_Mission_Tutorial_Training을 다음에 등록
   └─ Boot → OpeningTrailer → LobbyMissionSelect

Lvl_DroneFrontEnd (새 GameDefaultMap)
└─ BP_DroneFrontEndGameMode (Default Pawn 없음)
   └─ BP_DroneFrontEndPlayerController
      └─ WBP_DroneFrontEndRoot 정확히 한 개
         ├─ OpeningPanel + ContinueButton
         └─ LobbyPanel
            ├─ MissionSelectButton
            ├─ Mission 이름·설명·지역/난이도
            └─ StartMissionButton → MissionTrailer
```

- Source: `Source/Drone/Flow/DroneGameFlowSubsystem.*`, `DroneFrontEndGameMode.*`, `DroneFrontEndPlayerController.*`, `Source/Drone/UI/DroneFrontEndRootWidget.*`
- Data: `/Game/Drone/Data/Drones/DA_Drone_Scout_Greybox`, `/Game/Drone/Data/Missions/DA_Mission_Tutorial_Training`
- Front-end: `/Game/Drone/FrontEnd/UI/WBP_DroneFrontEndRoot`, 두 전용 BP Class, `/Game/Drone/Maps/Lvl_DroneFrontEnd`
- WBP Designer가 비어 있으면 C++ 정적 대체 Layout이 동작한다. 최종 외형은 `OpeningPanel`, `LobbyPanel`, `ContinueButton` 이름 계약과 `ReceiveFrontEndStateDisplayed` Event를 유지하며 Blueprint에서 교체한다.
- 현재 한 개 Training Mission의 목록/설명/시작 버튼은 연결됐다. 실제 영상·OpenLevel·Drone Spawn은 없으며, 영상이 준비되면 `FinishOpeningTrailer()`를 종료 Callback에 연결한다. 다음 생산 범위는 FLOW-04 정적 Mission Briefing→선택 Map 로드다.
- 검증: Drone Game/Editor Build, Data/Front-end 새 프로세스 Validate, 최종 `Drone.Flow` 3/3.

## 7. 검증 게이트

- 새 실행 3회에서 `OpeningTrailer → Lobby → MissionTrailer → Map → DroneSelect → InMission` 순서가 동일함
- Back/Skip/Start 연타에도 상태 전환과 맵 로드 요청이 한 번만 발생함
- 로비에서 선택한 Mission ID가 로드된 Map·브리핑·목표와 일치함
- 드론 확정 전 Pawn 0대, 확정 후 플레이어 Drone Pawn 1대
- Drone IMC 1개, HUD 1개, 목표 패널 1개, Mission Director 1개
- Mission 목표 패널은 현재 목표 변경 Event에만 반응하고 Tick에서 Actor 전체 검색을 하지 않음
- 결과 화면 뒤 재도전과 로비 복귀가 정상이며 이전 Mission Delegate·Widget이 남지 않음
- `DroneEditor Win64 Development`, 관련 자동화, Blueprint Compile 0/0/0, 대상 Map Check 통과
- `/Game/Drone`에서 Legacy ThirdPerson·Variant 또는 공급사 Pawn/GameMode/Input으로 향하는 신규 의존성 0

## 8. 보류 결정

- 시작 트레일러를 매 실행 재생할지 최초 1회만 재생할지
- Trailer 건너뛰기 키와 최소 노출 시간
- 로비가 2D 전용인지 3D 배경을 포함할지
- 드론 선택 화면을 Mission Map 위 UI로 할지 별도 Preview Map으로 할지
- Mission 결과에서 Tutorial Lap 통계를 함께 보여 줄 범위
- 최종 게임 제목을 `Project:Droner`, `DRONE LINE`, 다른 이름 중 무엇으로 통일할지

보류 항목은 다음 FLOW-04~06 Greybox를 막지 않는다. 현재는 `매 실행 트레일러`, `정적 대체 가능`, `Mission Map 위 드론 선택`, `한 Mission·한 Drone` 기준을 유지한다.
