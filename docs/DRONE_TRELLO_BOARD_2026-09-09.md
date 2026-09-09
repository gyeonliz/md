# Drone 프로젝트 Trello 입력용 작업 정리

기준일: 2026-09-09 (Asia/Seoul)

현재 공유 기준은 Unreal `main=origin/main=ac88992`, 문서 `main=origin/main=9a4f715`이다. Unreal과 문서 작업 트리는 정리 시작 시점에 Clean이며, `test1.umap`과 `M_Start.uasset`은 팀원 Stash 버전으로 복구해 `ac88992`로 Push했다.

## Trello List와 Label 권장안

List는 `완료`, `수동 확인`, `다음 개발`, `장기 후보·보류` 네 개로 사용한다. 구현과 자동화가 끝나도 화면·조작 확인이 남은 기능은 `수동 확인`에 둔다.

Label 권장값:

- `P0`: 현재 바로 확인하거나 막힘을 제거해야 하는 작업
- `P1`: 다음 개발 순서
- `P2`: 통합 뒤 진행할 작업
- `Code`, `Blueprint`, `UI`, `AI`, `Map`, `Asset`, `Git`, `Test`

## 완료 List

### `[완료][Git·환경] UE 5.8 프로젝트와 Git LFS 공유 기준 구축`

설명: Unreal 프로젝트와 문서 저장소를 분리하고 GitHub·Git LFS·UE 5.8 Editor Build 기준을 구성했다. 생성물과 개인 인증 정보는 저장소에서 제외했다.

완료 체크리스트:

- [x] Unreal 저장소 `gyeonliz/drone`과 문서 저장소 `gyeonliz/md` 분리
- [x] `.uasset`, `.umap` Git LFS 추적
- [x] UE 5.8 Editor Build 환경과 MSVC 14.51.36256 실제 빌드 확인
- [x] 팀원 원격·LFS·Plugin 재현성 점검 가이드 작성
- [x] 손상된 `test1.umap`, `M_Start.uasset`을 팀원 버전으로 복구하고 `ac88992` Push
- [x] `.vsconfig`의 구형 14.44 Stash 변경 제외, 기존 14.50 공유 설정 유지

### `[완료][Flight·Input] Drone Prototype 조작과 카메라 기준선`

설명: Collision Root와 Visual Mesh를 분리한 Drone Pawn에 이동·고도·Yaw·카메라·시점 전환·외형 기울기를 구현했다.

완료 체크리스트:

- [x] W/S 전후, A/D 좌우, Space/Ctrl 고도, Q/E Yaw
- [x] Mouse Look과 Gamepad 입력
- [x] `P` 또는 패드 Y로 1인칭·3인칭 임시 전환
- [x] Pawn 한 곳에서 IMC 등록·제거, 재시작 중복 방지
- [x] 쉬운 조작/실제 조작형과 안정/균형/고기동 분리
- [x] 좌우 Roll·앞뒤 Pitch 외형 표현 및 Camera/Collision 분리
- [x] PFN-06 자동화와 Standalone 수동 조작 기준 통과

### `[완료][HUD·Tutorial] 비행 HUD와 Training 코스 기록 시스템`

설명: 편집 가능한 Spline 코스, 순서형 Ring Gate, 구간·랩 기록과 비교 HUD를 구현했다.

완료 체크리스트:

- [x] 현재 속도·고도 Telemetry Snapshot
- [x] 한글 Flight HUD
- [x] Spline 기반 Course와 부드러운 Runtime Spline Mesh
- [x] Gate 순서·정방향·중복 통과 판정
- [x] Segment 시간·속도·거리와 Lap 기록
- [x] 이전 평균·Best·증감 Delta 계산 및 UI 공급
- [x] Course/Gate/Record 자동화 통과

### `[완료][Flow·UI] Front-end에서 Mission 결과까지 전체 흐름`

설명: 사람 Operator 조작과 NPC 대화 수령을 폐기하고 Drone 중심의 Front-end Mission 흐름을 구현했다.

완료 체크리스트:

- [x] Opening/시작 트레일러 자리 → Lobby
- [x] Mission 선택·측면 설명·하단 시작
- [x] Mission Briefing/트레일러 자리 → Mission Map
- [x] Map 진입 뒤 Drone 선택
- [x] 선택 전 Drone 0대, 선택 뒤 정확히 1대 Spawn/Possess
- [x] 측면 Mission 목표 UI
- [x] 성공/실패, 재도전, 로비 복귀
- [x] 완전히 새 PIE 실행 기준 전체 수명주기 3/3 통과

### `[완료][Drone Role] 정찰·FPV 자폭·드랍 역할 3종`

설명: 세 역할을 Data Asset과 전용 Pawn 외형으로 분리하고 공통 Primary/Secondary 입력으로 기능을 연결했다.

완료 체크리스트:

- [x] 정찰 DroneSpy, FPV DronePackFPV, 드랍 Delivery 모델 분리
- [x] 정찰: 거리·화각·LOS 유지 Scan과 진행·취소·완료 Event
- [x] FPV: Arm/Disarm, 최소 충돌 속도, Radial Damage, 폭발 VFX/SFX
- [x] 드랍: 탑뷰, 자동 투하 대상, 목표 접촉 성공
- [x] 좌클릭/RB Primary, 우클릭/LB Secondary 임시 입력
- [x] 역할별 Training 표적과 한글 상태 UI
- [x] 다른 역할 기능이 한 Pawn에서 중첩되지 않도록 검증

### `[완료][Drop·Asset] 맵 배치형 운반 화물과 재적재`

설명: `BP_DroneCarryablePayload`를 Mission Map에 놓을 수 있는 크레이트 Actor로 만들고 Drop Drone의 최초 화물에도 같은 Class를 사용한다.

완료 체크리스트:

- [x] MilitaryCamp 크레이트 Mesh 적용
- [x] Training Map에 `RoleTest_CarryablePayload` 배치
- [x] 빈 기체가 300cm 안에서 가장 가까운 화물 적재
- [x] 실제 Actor를 `PayloadCarryAnchor`에 부착
- [x] 같은 Actor 재투하
- [x] 착지 후 사라지지 않고 월드에 잔류
- [x] 착지한 화물 재적재 가능
- [x] 최초 선적재 화물도 같은 크레이트·잔류 규칙 사용
- [x] Build, 역할 기능, 역할 자산 자동화 통과

### `[완료][AI·Combat] 적 NPC 전투 핵심 코드`

설명: Mission Map에서 재사용할 적·아군 NPC, Smart Object와 기본 전투 수명주기를 구현했다. 최종 외형과 화면 검수는 별도 카드로 남긴다.

완료 체크리스트:

- [x] Hostile/Friendly Patrol과 Smart Object 1-Slot Claim
- [x] Drone Sight 감지, 추적, Search, Patrol 복귀
- [x] Rifle Trace, Shotgun Greybox, 탄속·분산·탄창·재장전
- [x] Cover 점유와 사망 뒤 역할 교대
- [x] 공용 Health와 Drone 파괴 시 교전 종료
- [x] StateTree·PIE 자동화 통과

### `[완료][Asset·Map] 제공 에셋 선별 이식과 프로젝트 경계 정리`

설명: 구매 에셋 전체를 무조건 흡수하지 않고 필요한 의존성 묶음만 프로젝트에 이식했다.

완료 체크리스트:

- [x] DronePack 드론 Mesh·Material·Texture 선별 이식
- [x] ArmyVFX·InfantrySFX 대표 자산 연결
- [x] MilitaryCamp·MilitaryBase·Battlefield·OilRig 중앙 맵 준비
- [x] NavigationArrows 최소 의존성 이식
- [x] 신규 생산 코드 `/Source/Drone`, 신규 프로젝트 자산 `/Game/Drone` 경계 유지
- [x] ThirdPerson·Variant 영역 Legacy 동결

## 수동 확인 List

### `[P0][수동 확인] 역할 3종 Vertical Slice`

확인 맵: `/Game/Drone/Maps/Lvl_DroneFrontEnd`에서 Training Mission으로 진입한다.

- [ ] 정찰 DroneSpy 크기·방향 확인
- [ ] 정찰 Scan 진행·취소·완료와 한글 상태 UI 확인
- [ ] FPV Arm 후 고속 충돌·폭발 크기·소리 확인
- [ ] FPV 폭발 후 결과 UI에서 재도전·로비 복귀 확인
- [ ] Drop 탑뷰 진입·복귀 확인
- [ ] 최초 크레이트 투하 후 착지·잔류 확인
- [ ] 300cm 안에서 크레이트 재적재·기체 하단 부착 확인
- [ ] 재투하와 재적재 반복 확인
- [ ] 세 모델 Transform과 표적 위치 조정값 기록

완료 조건: 기능 오류 없이 한 번의 Front-end→Mission→결과 흐름을 완료하고 크기·방향·입력 체감을 기록한다.

### `[P0][수동 확인] Training HUD 두 Lap 비교`

- [ ] Gate 0→1→2→3 첫 Lap 완주
- [ ] 첫 기준 평균·Best 생성 확인
- [ ] 두 번째 Lap 완주
- [ ] 구간 시간·속도·거리 평균 표시 확인
- [ ] 이전 평균 대비 빠름/느림 부호 확인
- [ ] Reset과 재시작 시 기록 중복 없음 확인

완료 조건: 실제 두 Lap에서 숫자 갱신과 증감 방향을 확인하고 TUT-04를 Done 처리한다.

### `[P0][수동 확인][AI] NPC Gaze·MG 3분할`

확인 맵: `/Game/Drone/Maps/Lvl_NPCSmartObjectGreybox`

- [ ] 일반 사격 병사가 Drone을 향해 자연스럽게 Yaw/Pitch 추적
- [ ] 감지 해제 뒤 Search 유예와 Patrol 복귀
- [ ] MG 사수가 기관총 뒤 지정 위치에 부착
- [ ] 사수가 몸체 Yaw를 따라 회전
- [ ] MG Base 고정, Body Yaw, Barrel Pitch 확인
- [ ] 손 위치와 발사 방향 확인

완료 조건: 위아래 까딱임이나 회전 누락 없이 Drone 추적과 MG 조준이 자연스럽게 보인다.

### `[P0][수동 확인][Turret] 설치형·차량형 자동포탑`

- [ ] 거리 내 Drone 탐지와 이탈
- [ ] 장애물 Visibility 차단
- [ ] Body Yaw·Barrel Pitch·Muzzle 방향
- [ ] Projectile 발사와 Damage
- [ ] 차량 Carrier 이동·회전 추종

완료 조건: 설치형과 차량형 각각 탐지→조준→발사→해제 한 사이클을 확인한다.

### `[P0][수동 확인][Vehicle] 4점 지면 추종 차량`

- [ ] 굴곡 노면에 따른 Z·Pitch·Roll 보간
- [ ] 네 바퀴 접지 외형
- [ ] 바퀴가 이동 방향으로 속도 비례 회전
- [ ] 급격한 튐이나 뒤집힘 없음
- [ ] 차량 포탑 부모 추종
- [ ] 1인칭·3인칭 전환과 Camera 회전 체감

완료 조건: 완전 차량 물리가 아닌 4점 Suspension Greybox로 자연스럽게 보인다.

### `[P1][수동 확인][Feedback] Drone 기울기·피격 흔들림`

- [ ] A/D Roll 방향이 실제 이동 방향과 일치
- [ ] W/S Pitch와 입력 해제 수평 복귀
- [ ] 3인칭 Camera와 Collision 안정
- [ ] 1인칭 Camera가 기체 움직임을 자연스럽게 반영
- [ ] Rifle/MG/자동포탑 피격 시 본체·Camera 감쇠 흔들림
- [ ] 연속 피격과 흔들림 종료 뒤 Camera 복원

### `[P1][수동 확인][Asset] 이식 맵·외형·오디오`

- [ ] DronePack 6종과 역할별 실제 모델 시각 확인
- [ ] MilitaryCamp/MilitaryBase/Battlefield/OilRig 조명·재질 확인
- [ ] FPV Loop Sound 단일 재생·종료 확인
- [ ] OilRig 성능과 Map Check 확인
- [ ] 실제 채택할 환경·NPC·무기 Mesh 후보 기록

### `[P1][수동 확인][Git] 다른 팀원 PC 재현`

- [ ] 최신 `origin/main=ac88992` Pull
- [ ] Git LFS 실제 바이너리 수신 확인
- [ ] `DroneEditor` Source 재빌드
- [ ] 역할 모델·사격 모션·MG·자동포탑 표시 확인
- [ ] Front-end→Training 한 번 실행

완료 조건: 별도 PC에서 Plugin/Generated Binary 없이 Source와 추적 Asset만으로 같은 기능을 재현한다.

## 다음 개발 List

### `[P1][AI·Asset] AI-VIS-01B 실제 NPC·무기·MG 비주얼 마감`

- [ ] Rifle/Shotgun/MG 최종 후보 Mesh 확정
- [ ] AnimBP·BlendSpace·손 IK/Grip 조정
- [ ] Muzzle FX·Impact FX·Sound 연결
- [ ] T Pose·손 미끄러짐·총구 오차 제거
- [ ] 역할별 Integration BP와 자동화 갱신

### `[P1][Flight] Take Off·Landing·Collision·Crash 상태`

- [ ] 비행 시작/대기/이륙/비행/착륙 상태 정의
- [ ] 착륙 가능 지면과 속도·각도 기준
- [ ] 충돌 세기와 Damage/Crash 판정
- [ ] Crash 후 Mission 실패 연결
- [ ] 자동화와 Standalone 반복 검증

### `[P1][Mission] 최소 Story Mission과 Jamming`

- [ ] Mission 단계·목표·성공/실패 Data 계약
- [ ] 측면 목표 UI 갱신
- [ ] 제한 구역·탐지·호위·투하 등 기본 목표 유형
- [ ] 통신 약화·재밍 범위와 UI 피드백
- [ ] 광섬유 역할의 재밍 면역 규칙
- [ ] Retry 시 Mission/Drone 상태 초기화

### `[P1][Tutorial] 역할별 튜토리얼 확장`

- [ ] 기본 비행 코스
- [ ] 정찰 Scan 구간
- [ ] FPV 무장·충돌 구간
- [ ] Drop 적재·투하 구간
- [ ] 역할별 안내 UI와 완료 판정

### `[P2][Integration] 통합 Greybox 플레이 사이클`

- [ ] Front-end에서 Mission 선택
- [ ] 역할에 맞는 Drone 선택
- [ ] Training 또는 Story 목표 수행
- [ ] Enemy AI·MG·자동포탑·차량과 교전
- [ ] 성공/실패·재도전·로비 복귀
- [ ] 완전히 새 실행 기준 3회 반복

### `[P2][UI·Media] 최종 WBP와 Trailer 연결`

- [ ] Figma 기준 Lobby/Mission/Drone 선택 화면 재검토
- [ ] Native fallback 계약을 유지하는 WBP Designer 제작
- [ ] Drone 3D Preview
- [ ] Opening/Mission Trailer Media 연결
- [ ] 최종 한글 문구·패드 포커스·해상도 대응

### `[P2][Asset·Performance] 에셋 교체와 최적화`

- [ ] Greybox Mesh 교체 지점 확정
- [ ] Collision·LOD·Nanite·Material 비용 점검
- [ ] Map별 Streaming/World Partition 필요성 판단
- [ ] Blueprint Compile 0 error/0 warning
- [ ] Map Check 0 error/0 warning
- [ ] Legacy 신규 의존성 0 확인

### `[P2][Git·Release] 팀 공유와 데모 기준선 마감`

- [ ] 남은 Stash 두 개 내용 감사 후 삭제 여부 결정
- [ ] 팀원 Clone/Pull/LFS/Build 체크리스트 통과
- [ ] 데모 Tag 또는 Release Commit 선정
- [ ] 테스트 결과와 실행 방법 문서화
- [ ] 포트폴리오용 기능별 영상·스크린샷 기록

## 장기 후보·보류 List

### `[P2][Physics] UE 5.8 Dataflow·Chaos 실험`

- [ ] 별도 Sandbox Branch에서 Dataflow Plugin 검증
- [ ] 일부 점 고정형 그물·늘어짐 Cloth Spike
- [ ] 선택형 Geometry Collection 맵 파괴 Spike
- [ ] 원본 비파괴 반복 편집과 성능 비교

### `[보류][Drone Role] 추가 역할`

- [ ] 광섬유 FPV
- [ ] 지상 UGV 전용 Pawn/Movement
- [ ] 장거리 타격 Drone/Sequencer 방식 결정

### `[보류][System] 배터리·통신·네트워크`

- [ ] 배터리·연료와 복귀 규칙
- [ ] 통신 거리·신호 강도
- [ ] 멀티플레이 필요성 재평가

현재 Standalone 싱글플레이가 검증 범위이며 네트워크·Android·신규 구매 에셋은 통합 Greybox 전까지 제외한다.

## Trello에 먼저 올릴 순서

1. `역할 3종 Vertical Slice`
2. `Training HUD 두 Lap 비교`
3. `NPC Gaze·MG 3분할`
4. `설치형·차량형 자동포탑`
5. `4점 지면 추종 차량`
6. `Drone 기울기·피격 흔들림`
7. `AI-VIS-01B 실제 비주얼 마감`
8. `Take Off·Landing·Collision·Crash`
9. `최소 Story Mission과 Jamming`
10. `통합 Greybox 플레이 사이클`
