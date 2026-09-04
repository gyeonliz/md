# 이동 중 읽는 Drone 현황·내 작업·학습 일정

기준일: 2026-09-03 (Asia/Seoul)

이 문서는 휴대폰으로 현재 상태와 다음 행동을 빠르게 확인하기 위한 요약본이다. 코드의 상세 설명은 [`DRONE_CODE_STRUCTURE_AND_USER_TASKS.md`](DRONE_CODE_STRUCTURE_AND_USER_TASKS.md), 학습 기록 양식은 [`STUDY_PLANS.md`](STUDY_PLANS.md)를 따른다.

## 30초 요약

- Unreal 공유 기준선은 `main=origin/main=2d6a459`이며 전투 Greybox·AI-VIS-01A와 Smart Object 방향 보강까지 반영돼 있다.
- Drone 입력·Telemetry·실제 WBP HUD·Training Course·Ring Gate 4개, Segment/Lap 원본과 이전 평균·Best·Delta 결과까지 구현됐다.
- 현재 개발 완료 지점은 `FLOW-03` 미션 선택·측면 설명·하단 시작이며 다음 신규 기능은 `FLOW-04` 정적 브리핑→선택 Map 로드다.
- 확정 화면 흐름은 `시작 트레일러 → 로비 → 미션 선택/측면 설명 → 하단 시작 → 미션 트레일러 → Map → Drone 선택 → Mission 시작/측면 목표 UI`다. 사람 Operator·NPC 대화 수령·Operator↔Drone 전환은 폐기했다.
- 현재 실행 세션은 Unreal `D:\JGY\project\drone`, 문서 `D:\JGY\project\md`다. `C:\URproject\drone`은 다른 PC의 이전 검증 경로이며 제공 에셋 원본은 직접 수정하지 않는다.
- NavigationArrows 최소 자산 6개와 전용 테스트는 main에 병합됐다. 화면 Host는 아직 미구현이다.
- 프로젝트 사용 맵은 `/Game/Drone/Maps`로 중앙화했다. 환경 맵 3종에 `Lvl_OilRig`을 추가했고, 남은 제공 자산 891개를 후보 라이브러리로 선별 이식했다.
- 사용자는 Gate나 기록 C++를 다시 만들 필요가 없다. 직접 비행하며 Gate 크기·간격·색·조종 난이도와 Drone Loop를 확인하면 된다.
- MG Claim·Move뿐 아니라 Occupied·Aim·Damage·사망 뒤 다른 AI 재점유, Cover 대응과 Drone 파괴 시 전체 교전 종료까지 공유 main에 반영했다.
- 전투 비주얼 감사와 BP `OnWeaponFired`·`OnReloadCompleted`까지 준비됐다. Manny Rifle Animation 38개와 Weapon Mesh 70개를 확인했지만 이름으로 식별되는 Shotgun Weapon Mesh는 0개다.
- FLOW-01은 8개 상태의 GameInstance Subsystem과 실제 Training Mission/Scout Drone Data Asset을 만들었다. FLOW-02는 실제 `WBP_DroneFrontEndRoot`, 전용 BP Controller/GameMode와 `Lvl_DroneFrontEnd`를 만들고 Opening→Lobby를 같은 Widget 한 개로 전환한다. FLOW-03은 Training Mission 버튼·설명·지역/난이도·하단 시작을 같은 Data Asset에 연결했다.
- 확정된 학습 항목은 `정보처리산업기사`와 `C++ 코딩테스트` 두 가지뿐이다.
- 정보처리산업기사 2026년 3회 필기 접수는 끝났다. 오늘 가장 먼저 Q-Net에서 자신의 접수·면제·응시 상태를 확인해야 한다.
- 코딩테스트는 공통 시험일이 없으므로 자격시험 일정에 맞춰 주간 반복 학습으로 운영한다.

## 1. 현재 Git·검증 상태

| 구분 | 현재 상태 |
|---|---|
| Unreal 저장소 | `D:\JGY\project\drone` |
| Unreal 기준 Commit | `2d6a459` |
| Git 상태 | `main=origin/main=2d6a459`; FLOW-01~03·NPC Visual 기반 Source/Test, Data Asset, Front-end BP/Map을 합쳐 26개 경로 로컬 미커밋 |
| Git LFS | `fsck` 정상 |
| 최종 Game/Editor Build | 성공 |
| Tutorial 자동화 | 7/7 통과 |
| AI 자동화 | 11/11 통과. Rifle 빈 시험 World의 예상 RecastNavMesh 경고 1건 |
| 전체 `Drone.` 자동화 | 27/27 통과, 실패 0 |
| Blueprint Compile | 0 errors, 0 Blueprint warnings, 0 failed loads. 별도 공급사/MCP 경고 29건 |
| Standalone | 실제 WBP HUD·Cyan Course·Current/Inactive Gate 표시 확인 |
| 에셋 이식 | 환경 3종+OilRig와 후보 라이브러리 891개. 새 Root 수량 일치·대표 로드·외부/누락 0, LFS fsck 통과 |
| NPC/Smart Object | 공유 main에 MG Claim/Move·Occupied·Aim·Damage·사망 교대·Cover·Drone 파괴 교전 종료·탄창과 BP 표현 Event까지 구성. 단계별 Editor Build·무기 테스트 3/3 통과 |
| Front-end Flow | FLOW-03 뒤 Game/Editor Build와 최종 `Drone.Flow` 3/3 통과. WBP Root 1개·중복 전환 0·선택 전 Drone 0대·Mission Definition과 표시 일치 확인 |

공유 이전 기준선에서 Game/Editor Build, AI 11개와 전체 Drone 27개를 실행했다. 실패는 0이고 Rifle의 빈 시험 World에서 RecastNavMesh가 없다는 예상 경고 1건만 있다. Blueprint 전체 Compile은 오류·Blueprint 경고·로드 실패 0이며 별도 공급사 Pose GUID와 MCP 고지 경고 29건은 기능 결과와 분리한다. 최신 FLOW-01에서는 Editor Build와 직접 관련 테스트·Data Validate만 확인했고 전체 회귀·Blueprint 전체 Compile은 반복하지 않았다.

## 2. 코드가 어떻게 연결되는가

```text
Lvl_DroneTraining
│
├─ BP_DronePrototypeGameMode
│  ├─ ADronePrototypePawn
│  │  ├─ Enhanced Input
│  │  ├─ 수평 이동·고도·Yaw·Camera
│  │  └─ UDroneTelemetryComponent
│  │     └─ 속력·고도·수직 속도·Heading Event
│  │
│  └─ ADronePrototypePlayerController
│     └─ UDroneFlightHUDWidget / WBP_DroneFlightHUD
│
├─ ADroneTrainingCourse
│  ├─ 편집 가능한 Spline
│  ├─ 비충돌 Cyan 안내선
│  ├─ OrderedGates[4]
│  ├─ UDroneTrainingGateSequenceComponent
│  │  └─ 순서·정방향·중복 통과·색 상태 판정
│  └─ UDroneTrainingLapRecorderComponent
│     ├─ Gate 0 시작 → Gate별 Segment → 마지막 Gate Lap 완료
│     ├─ World Time·Telemetry 위치로 실제 거리·평균속도 기록
│     └─ 이전 성공 평균·Best·시간/속도 Delta 비교
│
└─ ADroneTrainingGate × 4
   ├─ Pawn Overlap Box Trigger
   └─ 비충돌 Ring Visual 16조각

ADroneNPCSpawnPoint 또는 직접 배치
└─ ADroneNPCCharacter + NPC Profile
   └─ ADroneNPCAIController
      ├─ StateTree Component
      │  ├─ Hostile: ST_NPC_HostilePatrol 실행
      │  └─ Friendly: ST_NPC_FriendlyBaseRoutine 실행
      ├─ Sight: Drone Prototype 감지
      └─ Smart Object Reservation
         ├─ Hostile: EnemyPatrol / Guard / 선택적 MG
         └─ Friendly: FriendlyBasePatrol / Ambient

Lvl_NPCSmartObjectGreybox
├─ Hostile Rifle 1 + Hostile Shotgun 1 + Friendly 2
├─ Smart Object Station 12개 (기존 10 + Cover 2)
├─ ADroneNPCNavigationFloor + NavMeshBoundsVolume
├─ Hostile: EnemyPatrol Claim → Move → Wait → Release 반복
└─ Friendly: BasePatrol/Ambient Claim → Move → Wait → Release 반복
```

### 클래스별 한 줄 책임

| 클래스 | 책임 |
|---|---|
| `ADronePrototypePawn` | 입력을 받아 Drone과 Camera를 움직임 |
| `UDroneTelemetryComponent` | 0.1초 기본 주기로 네 비행 수치를 계산해 Event로 전달 |
| `ADronePrototypePlayerController` | HUD 한 개를 만들고 현재 Possess Drone의 Telemetry에 연결 |
| `UDroneFlightHUDWidget` | WBP의 `SPD`, `ALT`, `V/S`, `HDG` Text를 갱신 |
| `ADroneTrainingCourse` | Spline·안내선·Gate 순서 배열·Lap Recorder를 소유 |
| `ADroneTrainingGate` | Ring과 Overlap Trigger를 소유하고 진입·이탈 위치를 전달 |
| `UDroneTrainingGateSequenceComponent` | 현재 Gate와 정상 통과 여부를 판정하고 `OnGateAccepted`를 발생 |
| `UDroneTrainingLapRecorderComponent` | 정상 승인·Telemetry Event를 구독해 Segment/Lap 원본 기록 생성 |
| `ADroneNPCNavigationFloor` | Greybox NavMesh에 사용할 BlockAll·Navigation Relevant 바닥 제공 |
| `UDroneGameFlowSubsystem` | GameInstance 수명으로 Flow 상태·Mission/Drone Catalog와 선택을 보존 |
| `ADroneFrontEndPlayerController` | Front-end WBP Root 한 개를 만들고 Flow와 UI 입력을 연결 |
| `UDroneFrontEndRootWidget` | 정적 Opening과 Lobby 표시를 전환하고 실제 Trailer/WBP 표현 Event를 제공 |

### C++와 Blueprint의 경계

- C++: 이동 규칙, Telemetry 계산, HUD 수명주기, Gate 순서·방향·중복 판정, Segment/Lap 원본 계산, Collision·Delegate 안전 규칙
- Blueprint·Editor: 실제 Pawn/GameMode/Controller/WBP Class 연결, HUD 외형, Course Spline, Gate 위치·회전·크기·색
- Gate Actor의 로컬 `+X`가 유일한 정방향이다.
- `OrderedGates` 배열 위치가 통과 순서의 단일 기준이며 `GateIndex`는 `0, 1, 2, 3`이다.
- BP Event Graph에 Gate 판정 로직을 다시 만들 필요가 없다.
- TUT-04B UI는 Recorder의 `OnLapComparisonReady`와 Getter를 사용하며 계산을 BP에 중복 작성하지 않는다.

### 현재 UI 상태

구현됨:

- 실제 Blueprint Widget `WBP_DroneFlightHUD`
- 실제 Blueprint Widget `WBP_DroneFrontEndRoot`와 전용 Front-end BP Controller/GameMode/Map
- 실제 영상 전의 정적 Opening 화면, `계속` 버튼, 같은 Root의 Lobby 전환
- Training Mission 목록 버튼, 선택 시 Data Asset 기반 이름·설명·지역/난이도, 하단 `미션 시작`
- Speed, Altitude, Vertical Speed, Heading 표시
- 우측 상단 Drone 내구도 100/100·피해·파괴 상태 표시
- Gate Ring의 `Inactive`, `Current`, `Completed` 색 전환
- 최근/완료 Segment 통계와 이전 완주 평균·Best·시간/속도 Delta 표시

아직 없음:

- 실제 시작 트레일러 영상·최종 로비 외형
- 미션 트레일러·Map 로드 Flow·Map 내 Drone 선택 화면
- Mission 측면 목표 패널과 성공/실패 결과 화면
- 다음 Gate 번호·화살표
- Wrong Order·Wrong Direction 메시지
- 현재 Lap/Segment 실시간 타이머와 구간별 결과 표
- 완주 팝업·결과·평가 화면

## 3. 구현된 것과 아직 남은 것

### 구현 완료

- Greybox Drone Spawn·Possess와 Enhanced Input
- 전후·좌우·상승·하강·Yaw·Camera Pitch
- Telemetry Snapshot과 실제 WBP Flight HUD
- 별도 Training Map과 비충돌 Spline Course
- 실제 `BP_DroneTrainingGate` 4개
- 현재 Gate만 정방향으로 통과시키는 순서 판정
- 미래 Gate·역방향·완료 Gate 중복 통과 거부
- Current·Completed·Inactive 색 상태
- Reset과 Gate·Course·Pawn 수명 종료 안전 처리
- Gate 0 시작, Gate별 Segment와 마지막 Gate Lap 완료 원본 기록
- World Game Time·Telemetry 10Hz 3차원 위치 기반 실제 이동 거리·평균 속도
- Reset 시 부분 기록 폐기, 성공 History 유지, Course 재구성 시 History 초기화
- 현재 기록을 제외한 이전 성공 평균·Best·시간/속도 Delta와 Segment 비교
- 결과 UI가 구독할 `OnLapComparisonReady`와 Getter
- Friendly/Hostile, Unarmed/Rifle/Shotgun, MG 사용 가능 NPC Profile
- Smart Object Activity Tag와 Slot Claim·Release 기반
- NPC Character·Controller·Spawn Point·Station C++ 기반
- Drone Sight 감지 대상 등록과 Hostile Detected/Lost StateTree Event
- Smart Object Definition·Station Blueprint 6쌍
- Hostile Rifle·Hostile Shotgun·Friendly Base Blueprint와 Spawn Point BP
- `Lvl_NPCSmartObjectGreybox`의 NPC 4명·Station 12개·Navigation Floor
- 역할 Profile·Possess·Activity Tag·시작 위치 NavMesh 투영 자동 검증
- `ST_NPC_HostilePatrol`과 Native Claim·Move·Wait·Release Task
- Hostile 2명의 반복 순찰, 각 2회 이상 완료·서로 다른 2지점 이상 방문 자동 검증
- `ST_NPC_FriendlyBaseRoutine`과 Base Patrol/Ambient 교대·Fallback·방문 기록
- Friendly 2명의 반복 이동, 각 두 Activity·서로 다른 2지점 이상 방문 자동 검증
- 직전 지점 우선 회피와 감지·실패·UnPossess 시 예약 해제
- MG Claim→Move→Occupied→조준→발당 8 Damage와 중단/사망 해제
- 사망한 MG 사수 뒤 다른 MG 가능 Hostile의 재점유
- NPC·Drone 공통 기본 체력 100, 사망 1회와 사망 후 Damage 무시
- Rifle 발당 10, Shotgun 적중 Pellet당 8 Greybox Damage
- NPC 사망 시 이동·충돌·무기·StateTree 정지, Drone 사망 시 입력·이동·충돌 정지
- MG 실패 병사의 Cover 1-Slot Claim·이동·Occupied 개인 무기 대응
- Greybox Map Cover Station 2개와 사망 뒤 Cover 병사의 MG 재점유
- Drone 파괴 Event 1회와 살아 있는 적의 감지·사격·MG/Cover 정리, Search 없는 순찰 복귀
- Rifle 30발·Shotgun 8발 탄창, 발사당 1발 소모, 빈 탄창 정지·거부와 즉시 Reload
- GameInstance Flow 상태·Mission/Drone Data Asset, 정적 Opening→Lobby
- Training Mission 선택·Definition 기반 설명·하단 시작→MissionTrailer 상태

### 미구현

- 실제 시작 영상·최종 로비 외형, 미션 트레일러·Map 내 Drone 선택
- Drone 선택 뒤 Mission 시작과 측면 목표 UI·결과/재도전/로비 복귀
- 다음 Gate·잘못된 순서/방향 안내와 완주 팝업·구간별 결과 표
- 명시적인 Take Off·Landing·Crash 상태와 최종 비행 물리
- Mission·귀환·평가
- Rifle·Shotgun 예비 탄약·재장전 시간·Animation·FX·SFX
- MG 승하차 Animation·FX·SFX와 최종 밸런스
- NPC 래그돌·시체 제거, Drone 폭발·Respawn·최종 Mission 실패 화면
- 배터리·통신거리·재밍
- SaveGame·Multiplayer·최종 에셋 전면 적용

남아 있는 C++ `Variant_Combat`와 복구된 Template Content는 참고용이다. 현재 전역 Game 시작 Map은 `/Game/Drone/Maps/Lvl_DroneFrontEnd`, Editor 시작 Map은 `/Game/Drone/Maps/Lvl_DroneTraining`이다.

## 4. 사용자가 지금 해야 하는 일

### 이동 중 바로 할 일

1. Q-Net 마이페이지에서 아래 다섯 가지를 확인한다.
   - 2026년 3회 필기를 접수했는가
   - 접수했다면 수험표의 정확한 필기일은 언제인가
   - 이미 필기를 응시했는가
   - 이전 필기 합격·면제 기간이 남아 있는가
   - 산업기사 응시자격 자가진단과 응시자격서류 제출 상태가 완료됐는가
2. 확인 결과를 다음 중 하나로 적어 둔다.
   - `A: 3회 필기 접수·미응시`
   - `B: 3회 필기 결과 대기, 2회 실기 결과 대기 또는 유효한 필기 합격·면제 있음`
   - `C: 3회 미접수·필기 합격/면제 없음`
3. 아래에서 자신의 Track만 읽고 오늘 첫 학습을 시작한다.

### PC 앞에서 할 일

1. 다른 PC라면 `drone`과 `md` 저장소를 Pull한다.
2. Unreal 기준 Commit이 `origin/main=2d6a459`인지 확인한다. FLOW-01~03은 현재 PC의 로컬 미커밋이므로 다른 PC에는 아직 보이지 않는 것이 정상이다.
3. 현재 PC에서는 `/Game/Drone/Maps/Lvl_DroneFrontEnd`를 열어 `계속`→로비→Training Mission 선택→설명/지역/난이도→하단 시작까지 확인한다. 시작 뒤 실제 영상·Map 이동이 없는 것은 FLOW-04 전 정상이다.
4. Gate 0→1→2→3을 정방향으로 완주한다.
5. 미래 Gate를 먼저 통과하거나 현재 Gate를 역방향으로 통과해 진행되지 않는지 확인한다.
6. 마지막 Gate 뒤 네 Gate가 모두 Completed 색인지 확인한다.
7. 두 번 완주해 첫 시도 `기준 기록 생성`, 두 번째 시도 이전 평균·Best·Delta 부호를 확인한다.
8. `Lvl_OilRig`을 열어 Map Check와 재질·조명·스케일·충돌·성능을 기록한다.
9. Ground Drone/MG·Soldier/Insurgent·Quad v4/Sting 후보의 외형과 스케일을 확인한다.
10. Gate 크기·높이·간격·색 대비와 Keyboard/Gamepad 조종 체감을 메모한다.
11. 실제 스피커에서 Drone Loop가 한 겹으로 여러 반복 경계를 이어가고 종료 후 즉시 멈추는지 기록한다.
12. AI 기반 Merge 뒤 Editor를 재시작해 Smart Objects와 Gameplay Interactions Plugin을 확인한다.
13. `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`을 열어 Rifle 1명·Shotgun 1명·Friendly 2명과 Station 12개(기존 10 + Cover 2)의 위치·방향을 확인한다.
14. `P` 키로 네 NPC 시작점과 Station 사이의 녹색 NavMesh 연결을 확인한다.
15. PIE에서 Hostile 2명이 EnemyPatrol 3개 사이를 반복 이동하고 같은 자리에만 머물지 않는지 확인한다.
16. Friendly 2명이 FriendlyBasePatrol/Ambient 사이를 이동하고 같은 1-Slot에 동시에 머물지 않는지 눈으로 확인한다.

다시 만들 필요가 없는 것:

- Gate C++ Class와 Sequence Component
- Lap Recorder와 Segment/Lap 기록 Struct
- `BP_DroneTrainingGate`
- Map의 Gate 4개 배치와 Course 배열 연결
- WBP Flight HUD
- Course 안내 Material
- Android 설정

### Codex가 다음에 구현할 카드

```text
TUT-03 Segment/Lap 기록 Done
→ TUT-04B 비교·결과 UI 기술 구현 Done · 수동 확인 대기
→ AI-SO-00 C++ 기반 Done
→ AI-SO-01 Definition/Station BP Done
→ AI-NPC-01 적 Rifle·Shotgun·아군 BP와 Greybox Done
→ AI-PATROL-01 적 순찰 Done
→ AI-FRIEND-01 기지 아군 이동 Done
→ AI-PER-01 드론 감지·Search 자동/수동 Done
→ AI-WPN-01 공용 Weapon 계약 Done
→ AI-WPN-02 Rifle Greybox Trace Done
→ AI-WPN-03 Shotgun Pellet/Spread Done
→ AI-MG-01 MG 1-Slot Claim·Move Done
→ AI-MG-02 Occupy·Aim·Fire·Release·사망 교대 Done
→ HP-01 NPC·Drone 100 체력·사망·Drone HUD Done
→ AI-COVER-01 Cover 이동·점유·사망 뒤 MG 교대 Done
→ AI-COMBAT-END-01 Drone 파괴 교전 종료·실패 Event Done
→ AI-AMMO-01 Rifle·Shotgun 탄창·재장전 Greybox Done
→ AI-VIS-01A 자산 호환성 감사·BP 발사/재장전 Event Done
→ FLOW-00 사람 Operator 폐기·Front-end Mission Flow 문서 기준선 Done
→ FLOW-01 상태·Mission/Drone 데이터 계약 Done
→ FLOW-02 정적 시작 화면→로비 Done
→ FLOW-03 미션 선택·측면 설명·하단 시작 Done
→ FLOW-04 브리핑·Map 로드 Next
→ FLOW-05~06 Drone 선택·목표 UI
→ AI-VIS-01B 실제 전투 표현은 Mission 흐름 뒤 · Shotgun Mesh/최종 진영 외형 미정
```

TUT-03은 기존 Gate 판정과 분리된 Recorder가 정상 `OnGateAccepted`와 Telemetry Event를 구독하도록 완료했다. TUT-04B도 이 원본을 사용해 비교 결과를 C++에서 만들고 Widget은 표시만 한다.

## 5. 정보처리산업기사 공식 일정

공식 출처:

- [Q-Net 정보처리산업기사 종목별 상세정보·2026 일정](https://www.q-net.or.kr/crf005.do?gId=&gSite=Q&id=crf00503s02&jmCd=2290&jmInfoDivCcd=B0)
- [Q-Net 2026년도 국가기술자격검정 시행계획 공고](https://www.q-net.or.kr/man004.do?ARTL_SEQ=5249930&BOARD_ID=Q001&gSite=Q&id=man00402&notiType=10)
- [Q-Net 2026년 정기 기사 제3회 필기시험 안내](https://www.q-net.or.kr/man004.do?ARTL_SEQ=5268727&BOARD_ID=Q001&gSite=Q&id=man00402)
- [정보처리산업기사 출제기준 2025.1.1~2027.12.31](https://www.q-net.or.kr/cst006.do?artlSeq=5213449&brdId=Q006&gSite=Q&id=cst00602)

### 2026년 남은 일정

| 구분 | 날짜 | 2026-08-25 현재 상태 |
|---|---|---|
| 3회 필기 일반접수 | 2026-07-20~07-23 | 종료 |
| 3회 필기 빈자리접수 | 2026-08-01~08-02 | 종료 |
| 3회 필기시험 | 2026-08-07~09-01 | 진행 중, 접수자만 해당 |
| 3회 필기 합격예정자 발표 | 2026-09-09 09:00 | 예정 |
| 2회 최종합격 발표 | 2026-09-11 09:00 | 2회 실기 응시자만 해당 |
| 3회 실기 일반접수 | 2026-09-21~09-28, 휴일 제외 | 예정 |
| 3회 실기 빈자리접수 | 2026-10-18~10-19 | 남은 좌석이 있을 때만 가능 |
| 3회 실기시험 | 2026-10-24~11-13 | 예정 |
| 3회 최종합격 발표 | 2026-12-18 09:00 | 예정 |

원서접수는 공식 안내상 첫날 10:00부터 마지막 날 18:00까지다. 시험 기간 안의 실제 응시일은 종목·지역·수험표에 따라 다르므로 개인 수험표가 최종 기준이다.

3회 필기를 접수하지 않았고 유효한 필기 합격·면제도 없다면 2026년에 필기부터 새로 응시할 접수 기회는 남아 있지 않다. 2027년 검정형 연간 일정은 이번 공식 확인에서 찾지 못했으므로 현재 미정으로 둔다.

### 시험 구성

| 구분 | 공식 기준 |
|---|---|
| 필기 과목 | 정보시스템 기반 기술, 프로그래밍언어 활용, 데이터베이스 활용 |
| 필기 방식 | 객관식 4지 택일형, 과목당 20문항·30분 |
| 필기 합격 | 과목당 40점 이상이며 전 과목 평균 60점 이상 |
| 실기 | 정보처리 실무, 필답형 2시간 30분 |
| 실기 합격 | 60점 이상 |

## 6. 접수 상태에 따른 공부 계획

현재 진도와 하루 가능 시간이 기록되어 있지 않으므로 `1블록=60분`을 기본 단위로 사용한다. 시험 직전 모의고사만 실제 시험 시간에 맞춘다.

### Track A — 3회 필기를 접수했고 아직 응시하지 않음

수험표의 시험일이 최우선이다. 아래 날짜보다 시험이 빠르면 인접한 학습을 합치고, 시험 전날에는 새 범위를 늘리지 않는다.

| 날짜 | 할 일 |
|---|---|
| 08-25 | 수험표·응시자격 자가진단·서류 제출 상태 확인, 60문항·90분 진단 1회, 오답 4분류 |
| 08-26 | 정보시스템 기반 기술: 취약 개념 확인 → 관련 문제 → 오답 |
| 08-27 | 프로그래밍언어 활용: 직접 코드 추적·문제 풀이 → 오답 |
| 08-28 | 데이터베이스 활용: 개념·문제 → 오답 |
| 08-29 | 60문항·90분 전범위 모의 1회, 과목별 점수 기록 |
| 08-30 | 40점 미만 또는 최저 과목 집중 보완, 암기·혼동 카드 정리 |
| 08-31 | 최종 모의 1회와 누적 오답만 확인, 새 교재 범위 금지 |
| 수험일 | 20~30분 핵심 오답 확인 후 응시 |

판정 기준:

- 한 과목이라도 40점 미만이면 그 과목을 먼저 보완한다.
- 평균 60점에 못 미치면 맞힐 수 있는 기본 문제의 실수를 줄인다.
- 오답은 `개념 부족 / 암기 부족 / 개념 혼동 / 계산 실수`로 반드시 분류한다.

필기 응시 후에는 Track B로 이동한다.

응시자격서류 제출 대상이라면 Q-Net 제3회 수험자 안내에 따라 필기 합격예정자 발표 전에 제출을 끝낸다.

### Track B — 필기·실기 결과 대기 또는 유효한 필기 합격·면제 있음

- 3회 필기 응시자는 09-09 09:00에 필기 결과를 확인한다.
- 2회 실기 응시자는 09-11 09:00에 최종 결과를 확인한다.
- 기존 필기 합격·면제자는 위 발표를 기다리지 말고 면제 유효기간과 3회 실기 접수 가능 여부를 확인한다.

| 기간 | 목표 |
|---|---|
| 08-25~09-08 | C·Java·Python 코드 읽기, DB 활용, 시스템·UI·테스트를 순환하며 실기 기초 진단 |
| 09-09 | 3회 필기 응시자만 결과 확인. 합격이면 실기 Track 확정 |
| 09-10~09-20 | 짧은 답을 직접 손으로 쓰고 누적 오답을 실기형으로 다시 풀이 |
| 09-11 | 2회 실기 응시자만 최종 결과 확인. 불합격 시 필기 합격·면제 유효기간과 3회 실기 접수 가능 여부 확인 |
| 09-21~09-28 | 실기 일반접수. 가능한 한 첫날 확인하고 수험표의 실제 시험일 기록 |
| 09-29~10-11 | 프로그래밍·DB 중심 2주, 주 1회 혼합 문제 |
| 10-12~10-23 | 시스템·UI·테스트 보완, 150분 실전 모의와 오답 압축 |
| 10-18~10-19 | 일반접수 실패 시 빈자리 여부 확인. 좌석은 보장되지 않음 |
| 실제 실기 D-7 | 코딩테스트는 유지 수준으로 줄이고 매일 실기 오답·필답 연습 |
| 10-24~11-13 | 수험표의 지정일에 실기 응시 |
| 12-18 09:00 | 최종 결과 확인 |

실기 기본 주간 반복:

- 1회: C 코드 읽기·결과 예측
- 1회: Java 또는 Python 코드 읽기·결과 예측
- 1회: 데이터베이스 활용 문제
- 1회: 정보시스템 기반·UI·애플리케이션 테스트
- 1회: 혼합 문제와 누적 오답 재풀이

공식 세부 출제기준과 사용하는 교재의 목차가 다르면 공식 출제기준을 우선한다.

### Track C — 3회 미접수이고 필기 합격·면제 없음

2026년 시험일을 억지 목표로 만들지 않고, 2027년 공식 일정이 발표될 때 바로 D-Day 계획으로 바꿀 수 있는 12주 기초 계획을 실행한다.

| 기간 | 목표 |
|---|---|
| 08-25~08-30 | 60문항·90분 진단, 과목별 점수와 오답 원인 기록 |
| 08-31~09-20 | 필기 3과목을 1주씩 순환, 매주 마지막에 혼합 문제 |
| 09-21~10-18 | C·Java·Python, DB, 시스템·UI·테스트 실기 기초 순환 |
| 10-19~11-15 | 필기 60문항·90분과 실기 150분 모의를 번갈아 실행 |
| 11-16 이후 | 주 3회 유지 학습, Q-Net 2027 공식 공고 확인 후 D-Day 재계산 |

목표는 날짜만 채우는 것이 아니라 다음 세 조건이다.

- 필기 모의에서 모든 과목 40점 이상, 평균 60점 이상을 연속 3회 달성
- 틀린 이유를 네 오답 분류 중 하나로 설명 가능
- 실기 문제의 답을 해설을 보지 않고 다시 작성 가능

## 7. C++ 코딩테스트 병행 계획

코딩테스트는 특정 회사와 응시일이 정해지지 않아 공통 시험 일정이 없다. 자격시험의 D-7만 감량하고 나머지는 계속 유지한다.

### 임시 주간 최소안

- 코딩테스트를 하는 날: 1문제, 시간이 남아도 2문제를 넘기지 않음
- 새 문제: 주 2~3일을 임시 최소안으로 시작
- 재풀이: 주 1개
- 한 문제 제한: 첫 시도 40~60분
- 실패 시: 실패 이유 한 문장 → 아이디어 학습 → 코드 보지 않고 다시 구현
- 3~7일 뒤 같은 문제 재풀이

### 주제 순서

```text
C++ 기본
→ vector·sort
→ stack·queue·deque
→ map·unordered_map·set·priority_queue
→ DFS·BFS·재귀
→ 그래프·이분탐색
→ Greedy
→ DP
```

현재 단계가 기록되지 않았으므로 첫 문제 세트는 C++ 기본 진단 3문제로 시작한다. 세 문제를 설명 없이 구현할 수 있으면 `vector·sort`로 넘어가고, 막히면 기본 단계에서 같은 유형을 한 주 더 반복한다.

자격시험 필기 또는 실기 D-7에는 새 문제를 주 1개로 줄이고 재풀이 1개만 유지한다. 시험 다음 날부터 원래 주간량으로 돌아간다.

## 8. Drone과 공부를 같이 굴리는 기본 주간안

사용 가능한 요일·시간이 아직 미정이므로 아래 표는 확정 시간표가 아니라 바로 시작하기 위한 임시 최소안이다. 실제 가능 시간을 확인하면 Drone 블록을 먼저 확보한 뒤 나머지를 조정한다.

| 영역 | 평상시 임시 최소안 | 자격시험 D-7 임시안 |
|---|---:|---:|
| Drone 프로젝트 | 90분 × 4블록 | 90분 × 2블록, 진행 중 카드 마무리와 수동 확인 중심 |
| 정보처리산업기사 | 60분 × 4블록 | 90분 × 7블록 |
| C++ 코딩테스트 | 45~60분 × 3블록 | 새 문제 1개 + 재풀이 1개 |

권장 순서:

1. 이번 주 자격시험 Track의 마감 행동부터 배치한다.
2. Drone은 한 번에 1~3시간짜리 카드 하나만 처리한다.
3. 코딩테스트는 긴 프로젝트 작업 뒤가 아니라 별도 짧은 시간에 푼다.
4. 놓친 공부를 다음 날 두 배로 몰아서 보충하지 않는다.

## 9. 오늘 체크리스트

- [ ] Q-Net 3회 접수 여부 확인
- [ ] 수험표의 정확한 필기일 또는 필기면제 유효기간 확인
- [ ] 응시자격 자가진단·서류 제출 상태 확인
- [ ] 자신의 Track A/B/C 기록
- [ ] 정보처리산업기사 첫 진단 또는 실기 기초 1블록 실행
- [ ] C++ 기본 진단 문제 1개 직접 풀이
- [ ] PC에 도착하면 `Lvl_DroneTraining` Gate 수동 비행 확인
- [ ] 결과를 `잘됨 / 불편함 / 수정 필요` 세 줄로 기록
