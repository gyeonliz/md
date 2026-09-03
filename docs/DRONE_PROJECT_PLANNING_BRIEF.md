# Project:Droner 통합 기획·개발 현황서

기준일: 2026-09-03 (Asia/Seoul)

문서 상태: FLOW-01~03 로컬 구현 완료·FLOW-04 대기

이 문서는 Drone 프로젝트의 게임 기획, 현재 구현 상태, 다음 개발 순서와 검증 기준을 한 번에 확인하기 위한 통합 문서다. 세부 기술 계약은 링크된 구현 문서를 따르며, 구현 완료 여부는 실제 Unreal 코드·Asset·빌드·자동화·화면 확인을 근거로 판정한다.

## 1. 한눈에 보는 프로젝트

| 항목 | 현재 기준 |
|---|---|
| 장르 | 싱글플레이 드론 운용·정찰·미션 게임 |
| 엔진 | Unreal Engine 5.8.1 |
| 현재 작업 루트 | Unreal `C:\URproject\drone`, 문서 `C:\Users\jkw11\Documents\Codex\2026-08-19\codex-gpt-chatgpt-codex-1-6` |
| 다른 PC의 이전 경로 | `D:\JGY\project\drone`, `D:\JGY\project\md` |
| Unreal 공유 기준 | `main=origin/main=2d6a459` |
| 플레이어 표현 | 사람 캐릭터 없이 Drone 조작 중심 |
| 핵심 모드 | Tutorial 비행 훈련, Story Mission |
| 현재 신규 개발 | `FLOW-04` 정적 브리핑→선택 Map 로드. FLOW-01~03은 로컬 완료 |
| 제외 범위 | Android, Network/협동, 실제 군사 장비 1:1 재현 |

핵심 경험은 다음과 같다.

```text
임무를 고른다
→ 브리핑을 확인한다
→ 임무에 맞는 Drone을 선택한다
→ 직접 비행하며 정찰·전달·회피·전투 목표를 수행한다
→ 결과를 확인하고 재도전하거나 로비로 돌아간다
```

## 2. 세계관과 플레이어 역할

Figma `Project:Droner`에 정리된 현재 참고 설정은 아래와 같다. Figma는 읽기 전용 기획 참고 자료이며 구현 완료의 근거로 사용하지 않는다.

- 시점: 2030년
- 지역: 중앙아시아 접경의 고산·사막 분쟁지대 `카슈 회랑`
- 플레이어 소속: `그레이라인 시큐리티`
- 플레이어 역할: 얼굴·국적이 드러나지 않는 프리랜서 Drone 조종사
- 지원 오퍼레이터: 정보를 모아 전달하는 콜사인 `허브(HUB)`
- 적대 세력: 자경단에서 군벌로 변질된 `다르감`
- 주요 위협: 밀수·마약 유통·무장 세력·통제되지 않는 국경 지대

사람 Player Character는 화면에 등장하거나 직접 조작하지 않는다. `허브`는 로비 NPC가 아니라 트레일러, 브리핑 음성·자막과 Mission 진행 안내를 담당하는 지원자다.

최종 게임 제목은 `Project:Droner`, `DRONE LINE` 또는 다른 이름 중 아직 확정하지 않았다.

## 3. 확정된 전체 화면 흐름

```text
게임 실행
→ 시작 트레일러
→ 로비
→ 미션 레벨 선택
→ 선택 미션의 측면 설명
→ 하단 시작 버튼
→ 미션 트레일러/브리핑
→ 미션 Map 진입
→ Drone 선택
→ Mission 시작
→ 측면 목표 UI와 Flight HUD 표시
→ 성공/실패 결과
→ 재도전 또는 로비 복귀
```

### 시작 트레일러

- 세계관, 카슈 회랑, 다르감의 위협과 플레이어 파견 이유를 설명한다.
- 영상·Sequencer가 준비되지 않은 Greybox에서는 정적 이미지·자막 화면으로 같은 상태 전환을 검증한다.
- 미션별 브리핑 트레일러와 분리한다.

### 로비와 미션 선택

- 미션 목록 또는 레벨 카드를 표시한다.
- 선택한 항목을 강조한다.
- 화면 측면에 미션 이름, 설명, 지역과 난이도 후보를 표시한다.
- 하단 시작 버튼은 유효한 Mission이 선택됐을 때만 활성화한다.
- 로비에서 사람 캐릭터를 움직이거나 NPC에게 걸어가 Mission을 받지 않는다.

### 미션 트레일러와 Map 진입

- 선택 Mission의 장소·목표·위험 요소를 영상 또는 자막 브리핑으로 전달한다.
- 종료되면 Mission Definition에 지정된 Map을 연다.
- Map 진입 직후 Mission을 바로 시작하지 않고 Drone 선택 UI를 먼저 표시한다.

### Drone 선택과 Mission 시작

- 해당 Mission에서 허용된 Drone만 보여 준다.
- Drone 이름, 역할, 설명과 Preview를 표시한다.
- 선택 확정 전 플레이어 Drone Pawn은 0대여야 한다.
- 확정 뒤 Integration Pawn 한 대만 Spawn/Possess하고 입력·HUD·Mission Director를 시작한다.

### 결과

- 성공/실패, 주요 수행 기록과 재도전·로비 버튼을 표시한다.
- 재도전 시 같은 Mission Definition을 다시 사용한다.
- 로비 복귀 시 이전 Mission Widget·Delegate·Pawn·입력 상태를 남기지 않는다.

## 4. 모드별 기획

### Tutorial 비행 훈련

목표는 비충돌 Spline 안내선을 따라 순서형 원형 Gate를 정확히 통과하고 자신의 기록을 비교하는 것이다.

- Spline Point는 Editor에서 자유롭게 추가·이동한다.
- 빛나는 코스는 Spline Mesh를 충분히 세분화해 각진 꺾임을 줄인다.
- 안내선은 Collision·Overlap·Physics·Navigation에 영향을 주지 않는다.
- Gate는 명시적 배열 순서, Actor 로컬 `+X` 정방향과 중복 통과 방지를 사용한다.
- 첫 Gate에서 Lap을 시작하고 마지막 Gate에서 완료한다.
- 잘못된 순서·역방향·이미 완료한 Gate는 기록을 변경하지 않는다.

Tutorial UI 표시 항목:

- 현재 속도 `km/h`
- 현재 고도 `m`
- 수직 속도 `m/s`
- 현재 방위 `°`
- 기체 내구도
- 현재 Gate와 다음 Gate
- 현재 Lap 시간
- 최근 구간 시간
- 최근 구간 실제 이동 거리
- 최근 구간 평균 속도
- 전체 구간 평균 시간·거리·속도
- 이전 성공 평균과의 시간 차이
- 이전 성공 평균과의 속도 차이
- Best Lap·Best Segment

시간은 음수 Delta면 더 빠른 기록, 양수면 더 느린 기록이다. 속도는 양수 Delta면 더 빠르고 음수면 더 느리다. 첫 완주는 비교 대상이 없으므로 `기준 기록 생성`으로 표시한다.

### Story Mission

Story Mission은 로비에서 직접 선택한다. 사람 조작과 NPC 대화 수령은 포함하지 않는다.

첫 Mission 후보:

- 구급품 전달: 고립 지역 또는 마을의 지정 지점으로 보급품 운반
- 정찰: 표적 지역에 접근해 정보 획득 후 귀환
- 재밍 회피: 신호 방해 구역을 우회하거나 Jammer를 해제
- 적 기지 침투: Patrol·Cover·Rifle/Shotgun·MG 대응을 피해 목표 달성

Mission 공통 상태 후보:

```text
WaitingForDroneSelection
→ Deploy
→ Recon
→ Objective
→ Egress
→ Evaluation 또는 Failed
```

미션 측면 UI에는 현재 목표, 진행 수치와 필요한 경우 목표 거리만 표시한다. Telemetry와 목표 UI는 서로 다른 데이터 공급자를 사용하되 같은 PlayerController 수명주기에서 한 개씩 관리한다.

### Jamming

Jamming은 무작위 키 입력 손실이 아니라 재현 가능한 단계형 규칙으로 만든다.

1. 약함: 신호 경고와 Meter 변화
2. 중간: HUD Noise와 목표 정보 일부 손실
3. 강함: 조작 반응 저하 또는 통신 두절

Jammer 회피, 범위 이탈, 전원 차단 또는 파괴를 Mission 목표로 연결한다. 실제 전자전 장비를 그대로 복제하지 않는다.

## 5. UI·시각 방향

Figma의 UI 참고 이미지는 청록·녹색 계열 전술 HUD, 얇은 선, 표적 Crosshair, Telemetry Panel과 경고 아이콘을 중심으로 한다.

적용 원칙:

- 정보 우선순위가 높은 수치는 크고 짧게 표시한다.
- 모든 핵심 UI 문구는 한글을 기준으로 작성한다.
- 정상 정보는 청록/녹색, 주의는 노랑, 위험·실패는 빨강을 후보로 사용한다.
- Mission 목표 패널은 화면 측면, 시작 버튼은 로비 하단에 둔다.
- Drone 시야를 가리지 않도록 중앙 영역은 Crosshair와 최소 정보만 사용한다.
- C++이 상태와 수치를 계산하고 UMG는 배치·색·폰트·Animation만 담당한다.
- Widget Tick, 매 프레임 Pawn 전체 검색과 동일 계산의 Blueprint 중복을 피한다.

## 6. 현재 구현 현황

### 구현·자동 검증 완료

| 영역 | 현재 상태 |
|---|---|
| Drone 조작 | Actor-relative 이동, World Up 고도, Q/E·Mouse X Yaw, Mouse Y Camera Pitch, Gamepad Mapping |
| Camera/Input | 고정 추적 Camera, PFN-06 자동화 3/3과 Keyboard·Mouse Standalone 수동 Pass |
| Telemetry/HUD | 속도·고도·수직 속도·방위 10Hz Event, 실제 WBP HUD, 기체 내구도 |
| Tutorial Course | 편집 가능한 Spline, 비충돌 Cyan Spline Mesh 안내선 |
| Gate | Ring Visual·Trigger 분리, 순서·정방향·중복 판정, 상태 색상 |
| 기록 | Segment/Lap 시간·실제 3차원 이동 거리·평균 속도 |
| 기록 비교 | 이전 성공 평균·Best·시간/속도 Delta 계산과 HUD 결과 행 |
| 적 AI | 순찰, Drone 감지·실종 Search, NavMesh 이동 |
| Smart Object | 1-Slot Claim·Occupied·Release, Patrol·Ambient·Cover·MG 역할 |
| 전투 | Rifle/Shotgun Trace·Damage·탄창·즉시 Reload, MG 조준·사격 |
| 체력·사망 | NPC/Drone 공통 체력, 사망 1회, 전투·입력·예약 정리 |
| 협업 자산 | FPV Drone, 환경 Map, Ground Drone/MG, NPC·VFX·SFX 후보 선별 이식 |
| Front-end 기반 | GameInstance Flow/Catalog, 실제 Mission·Drone Data Asset, 전용 Map/BP GameMode·Controller/WBP, 정적 Opening→Lobby, Training Mission 선택·설명·시작 |

공유 Unreal 기준은 `2d6a459`이다. 이 기준에 전투 Greybox, Blueprint 발사·재장전 표현 Event와 Smart Object 방향 보강까지 들어 있다. FLOW-01~03은 아직 로컬 미커밋이다.

### 로컬 구현·수동 확인 대기

- `Lvl_NPCSmartObjectGreybox`에서 Patrol·Cover·MG 도착 방향 실제 화면 확인
- FLOW-01~03 Source/Test, Data Asset 2개, Front-end BP/WBP/Map과 기본 Game Map 설정
- NPC Weapon Visual/Muzzle Component와 Character 표현 Event 기반. 실제 Mesh는 미연결
- Training 두 Lap에서 첫 기준·이전 평균·Best·Delta 표시 확인
- Drone Loop 단일 재생과 종료 정지 청감
- MilitaryCamp·MilitaryBase·Battlefield·OilRig의 조명·재질·충돌·성능·채택 여부

### 아직 구현하지 않음

- 실제 시작 트레일러 영상과 최종 로비 외형
- 미션 트레일러와 선택 Map 전환
- Map 안 Drone 선택·Preview·허용 목록 검증
- Mission Director와 측면 목표 UI
- 성공/실패 결과·재도전·로비 복귀
- 명시적 Take Off·Landing·Crash 상태
- Jamming Runtime
- 실제 NPC·무기·MG Animation·Niagara·Sound 표현
- Drone 폭발·Respawn과 최종 Mission 실패 연출

## 7. 폐기·보존 결정

### 폐기

- 사람 Player Character 생산 구현
- 사람 Operator용 이동·상호작용 Input Mapping
- Operator↔Drone 실시간 Possess·Camera 전환
- 로비에서 NPC에게 걸어가 대화해 Mission을 받는 방식
- NPC 대화를 완료해야 Mission이 열리는 구조

### 보존

- 기존 적 NPC·Smart Object·전투 코드는 Mission 내부 기능으로 사용한다.
- Friendly NPC Routine은 환경 연출 후보로 보존하지만 Front-end 필수 기능으로 보지 않는다.
- Legacy ThirdPerson·Combat·Platforming·SideScrolling은 참고용으로 동결하며 새 상속·참조를 만들지 않는다.
- 외부 공급사 Pawn·GameMode·Input을 프로젝트 핵심 부모로 사용하지 않는다.

## 8. 기술 구조

```text
UDroneGameFlowSubsystem
├─ 현재 Front-end 상태
├─ 선택 Mission ID
├─ 선택 Drone ID
├─ 중복 전환 차단
└─ Map 전환 사이 결과 보존

UDroneMissionDefinition
├─ 한글 이름·설명·썸네일
├─ 브리핑 Media/Sequencer
├─ Mission Map
├─ 허용 Drone 목록
└─ 시작 목표·성공/실패 규칙

UDroneDefinition
├─ 한글 이름·역할 설명
├─ Preview 자산
└─ Spawn할 Integration Pawn Class

ADroneMissionDirector
├─ Mission 상태
├─ 현재 목표 Snapshot/Event
├─ 성공·실패 판정
└─ Drone 파괴·귀환·정보 획득 Event 연결
```

책임 경계:

- C++: 상태, 계산, 데이터 검증, 맵 전환 요청, Mission 수명주기와 Event
- Blueprint/UMG: Asset 연결, UI Layout·Animation, Preview와 Greybox 조정
- GameInstanceSubsystem: 맵 사이 선택 상태
- Mission Director: 현재 Map의 Mission 실행 상태
- PlayerController: 로컬 HUD·목표 Widget 한 개의 생성과 Delegate 정리
- Drone Pawn: Drone 전용 IMC 등록·제거와 실제 비행 입력

생산 코드는 `Source/Drone`, 생산 Asset은 `/Game/Drone` 아래에만 만든다.

## 9. 맵·Asset 활용 계획

| Map | 역할 후보 | 현재 상태 |
|---|---|---|
| `Lvl_DroneFrontEnd` | 게임 시작·정적 Opening·로비 | FLOW-02 로컬 구현·자동 PIE 통과 |
| `Lvl_DronePrototype` | 입력·Collision 단위 시험 | 구현됨 |
| `Lvl_DroneTraining` | 첫 Tutorial Mission Vertical Slice | 구현됨·두 Lap 수동 확인 대기 |
| `Lvl_NPCSmartObjectGreybox` | AI·Smart Object·전투 시험 | 구현됨·방향 수동 확인 대기 |
| `Lvl_MilitaryCamp` | 소규모 기지 침투/정찰 | 이식됨·채택 검토 대기 |
| `Lvl_MilitaryBase` | 강·도로를 포함한 대형 기지 Mission | 이식됨·채택 검토 대기 |
| `Lvl_Battlefield` | 전투·재밍 Mission 후보 | 이식됨·채택 검토 대기 |
| `Lvl_OilRig` | 해상·산업 시설 Mission 후보 | 이식됨·화면·성능 검토 대기 |

새 Front-end 권장 Content 경계:

```text
/Game/Drone/Maps/Lvl_DroneFrontEnd
/Game/Drone/FrontEnd/UI/
/Game/Drone/FrontEnd/Media/
/Game/Drone/Data/Missions/
/Game/Drone/Data/Drones/
/Game/Drone/Mission/UI/
/Game/Drone/Mission/Directors/
```

## 10. 개발 로드맵

### 1단계 — 기존 변경 정리

1. Smart Object Yaw를 Editor에서 실제 확인한다.
2. Friendly Definition의 의도한 Slot 설정을 확인한다.
3. 사용자가 Unreal과 MD 변경의 Commit 범위를 검토·Commit한다.

### 2단계 — Front-end 데이터 기반

| ID | 작업 | 완료 조건 |
|---|---|---|
| FLOW-01 Done | Flow 상태·Mission/Drone 데이터 계약 | 정상 전환, 잘못된 ID와 중복 요청 거부 자동화 통과 |
| FLOW-02 Done | 시작 트레일러 → 로비 | 정적 Opening→Lobby, 실행마다 Root Widget·전환 요청 한 개 PIE 통과 |
| FLOW-03 Done | 미션 선택·측면 설명·하단 시작 | 같은 Mission Definition으로 목록·설명·시작 연결, 오류·중복 거부 PIE 통과 |
| FLOW-04 | 미션 트레일러 → Map | 선택 Mission의 브리핑 뒤 지정 Map 로드 |
| FLOW-05 | Map 내 Drone 선택 | 확정 전 Pawn 0, 확정 뒤 허용 Drone 1대 |
| FLOW-06 | Mission 시작·측면 목표 UI | Drone 확정 뒤에만 Director·목표 Event 시작 |
| FLOW-07 | 결과·재도전·로비 | 성공/실패 뒤 안전한 재시작·복귀 |
| FLOW-08 | 전체 회귀 | 새 실행부터 결과까지 3회 중복 0 |

첫 Vertical Slice는 `Lvl_DroneTraining` 한 Mission과 FPV Integration Drone 한 대를 사용한다.

### 3단계 — Flight·Mission 완성

1. Take Off·Landing·Crash 상태
2. Drone 파괴와 Mission 실패·재시작 연결
3. 목표 획득·귀환·평가
4. Tutorial 결과 화면과 SaveGame 후보

### 4단계 — Story Mission

1. 구급품 전달 Mission
2. 정찰·정보 획득 Mission
3. 재밍 회피·해제 Mission
4. 적 Patrol·Cover·Rifle/Shotgun·MG 통합
5. `허브` 음성·자막과 Mission 진행 안내

### 5단계 — 시각·물리·Asset 마감

1. NPC·무기·MG Animation·VFX·SFX
2. Drone 종류와 Preview 확장
3. 선택 환경 Map 최적화·Collision·Lighting
4. 부분 고정 그물 Chaos Cloth Spike
5. 지정 대상만 파괴하는 Geometry Collection Spike

## 11. 검증 기준

- `DroneEditor Win64 Development` Build 성공
- 관련 C++ 자동화 성공
- Blueprint Compile errors 0, warnings 0, failed loads 0
- 대상 Map Check 오류·경고 0 또는 공급사 기존 메시지 분리 기록
- Front-end 전체 흐름 새 실행 3회 동일 결과
- Start·Back·Skip 연타 시 상태와 Map Load 중복 0
- Drone 선택 전 Pawn 0대, 선택 뒤 1대
- IMC·HUD·목표 Widget·Mission Director 각각 1개
- Mission 종료 뒤 이전 Delegate·Widget·Pawn 참조 잔존 0
- `/Game/Drone` 신규 Asset의 Legacy·공급사 Pawn/GameMode/Input 의존성 0
- Gamepad Navigation과 Keyboard·Mouse를 각각 수동 확인
- Standalone 싱글플레이에서 정상 종료와 재진입 확인

## 12. 추천 역할 분리

실제 팀 역할은 아직 확정되지 않았으므로 아래는 충돌을 줄이기 위한 권장안이다.

| 담당 묶음 | 주 작업 |
|---|---|
| 기능 개발 | Flow·Mission·Drone 데이터, C++, 자동화 |
| UI | 로비·미션 설명·Drone 선택·목표·결과 UMG |
| 레벨 | Mission Map 배치, Spline·Gate·Smart Object·Collision |
| 모델링/Asset | Drone Preview·Integration, 환경·NPC·무기 외형 |
| 시네마틱/콘텐츠 | 시작/미션 Trailer, 자막·`허브` 안내, Mission 설명 |
| QA/문서 | 반복 PIE·Standalone, Map Check, Workboard·Worklog 갱신 |

같은 `.umap`이나 `.uasset`을 두 명이 동시에 수정하지 않는다. 레벨·UI·Data Asset 담당 파일을 먼저 나누고, 공급사 원본은 직접 수정하지 않는다.

## 13. 현재 사용자가 확인할 것

우선순위가 높은 수동 확인은 두 가지다.

1. `Lvl_NPCSmartObjectGreybox`에서 Cyan 화살표와 Patrol·Cover·MG 도착 방향이 일치하는지 확인
2. `Lvl_DroneTraining`을 두 번 완주해 첫 기준·이전 평균·Best·시간/속도 Delta가 실제 HUD에 맞게 표시되는지 확인

그다음 확인:

- Drone Loop가 한 겹으로 반복되고 종료 시 즉시 멈추는지
- MilitaryCamp·MilitaryBase·Battlefield·OilRig 중 실제 Mission 제작에 적합한 Map
- Gamepad UI Navigation과 Drone 조작 체감

## 14. 보류 결정과 위험

| 항목 | 현재 처리 |
|---|---|
| 최종 게임 제목 | 보류 |
| 시작 Trailer 매 실행/최초 1회 | 첫 Greybox는 매 실행 |
| Trailer Skip 키·최소 시간 | FLOW-02에서 결정 |
| 2D/3D 로비 | 첫 Greybox는 가벼운 전용 Front-end Map |
| Drone 선택 Preview 방식 | 첫 Greybox는 Mission Map 위 UI, 필요 시 Preview Map 분리 |
| 최종 비행 물리 | 현재 FloatingPawnMovement는 시험값 |
| Shotgun 실제 Mesh | 후보 미확보 |
| Soldier/Insurgent 외형 | Manny와 Skeleton이 달라 Retarget 검증 필요 |
| 환경 Map 선택 | 시각·Collision·성능 검토 뒤 결정 |
| SaveGame | Front-end·결과 흐름 안정화 뒤 |

## 15. 문서와 Git 운영

- 현재 상태: [`../WORKBOARD.md`](../WORKBOARD.md)
- 검증된 환경·기준선: [`../STATUS.md`](../STATUS.md)
- 날짜별 작업 기록: [`DRONE_WORKLOG.md`](DRONE_WORKLOG.md)
- Front-end 상세 설계: [`DRONE_FRONTEND_MISSION_FLOW_PLAN.md`](DRONE_FRONTEND_MISSION_FLOW_PLAN.md)
- Tutorial·Mission 세부 계획: [`DRONE_TUTORIAL_STORY_PLAN.md`](DRONE_TUTORIAL_STORY_PLAN.md)
- 현재 코드·Asset 구조: [`DRONE_CODE_STRUCTURE_AND_USER_TASKS.md`](DRONE_CODE_STRUCTURE_AND_USER_TASKS.md)

매 작업 종료 시 `WORKBOARD → WORKLOG → STATUS/CONTEXT → 관련 계획 문서` 순서로 실제 변경·검증·다음 작업을 갱신한다. Commit·Push는 사용자 지시와 저장소별 변경 범위를 확인한 뒤 수행한다.
