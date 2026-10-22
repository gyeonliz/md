# 현실 조종감 기준과 후속 개발 계획

기준: 2026-10-22 D PC. 현재 요청은 기존 InterLink/패드·키보드 매핑 복구만이다. 스로틀·모터 수정은 사용자 요청으로 보류했고 Computer Use/화면조작·입력주입은 전부 중지했다. 매핑 원본은 정상내용이며 사용자가 재실행 후 입력 복구를 확인했다. 매핑/입력 추가수정은 없고 근본원인은 미확정이다. 직전 Build003/Run003의 물리12+기존회귀11=23Success는 직접 Pawn API·자동화 범위다. actual console/Slate/조종기·키보드 전체입력 파이프라인을 통과했다는 뜻이 아니다. 후보구현/가상계수·실기체교정/본미션/B·C 미완은 보존한다.

## Racer 로터 1차 후보

`/Game/Drone/Maps/TestMap/Lvl_DroneRotorDynamicsPilot`을 열고 Play한다. 새 전용 맵의 DroneRotorControlledTest tag와 Setup이 기존 saved `DA_Drone_Racer_Greybox`의 PawnClass/Definition을 읽어 메모리에서만 Acro Mode2·FixedStepCandidate로 진입시킨다. 시작은 motor OFF다. 원래 DA/BP와 제품맵은 opt-in으로 저장하지 않는다.

| 항목 | 현재 지원·구분 |
|---|---|
| 백엔드/기체 | Legacy가 기본. Racer1종의 명시 opt-in FixedStepCandidate·Acro Mode1/2만 지원 |
| 월드/무게중심 | 명시 controlled tag·CG0·외부pose writer 없음. 활성 altitude manager가 있거나 net rig/observer lesson이 존재하는 World는 진입 거부 |
| 운동 | 로터별 힘/반작용토크·대각관성·rate 제어/배분/포화·THRUST 지연·중력/상대공기속도 항력을 공유 SI커널로 계산 |
| 단독 writer/시간 | 후보 이동소유자1개. Legacy Floating/Acro 적분·수직clamp·Weather 별도drift를 중복적용하지 않음. bounded fixed-step의 성공step/pose commit·pending/drop을 기록, hold/pause는 진행하지 않음 |
| 접촉/모터 | 구 swept 이동·normal 속도투영·support slop의 근사접촉. 저스로틀 motor arm·정상OFF·실제grounded·rearm/재이륙. 무장 ArmSwitch/방전·사망과 구분 |
| 가상 계수 | 실제saved Racer에서 질량2kg/최대합산추력40N/THRUST tau0.055초를 읽었다. geometry/inertia/drag/gains는 synthetic이며 첨부안의 미검증수치 .527kg/60N을 채택한 것이 아님 |

**콘솔 실행 권장 중지:** 사용자 실콘솔에서 arm거부가 재현됐고 미해결이다. 구 -1/arm/스로틀 절차를 현재 실행지침으로 제공하지 않는다. 현재는 기존매핑 범위만·스로틀/모터는 사용자지시보류·모든화면조작/CUA 중지다. 직전23성공은 direct API 자동범위이며 actual console/Slate 조작복구 Pass가 아니다.

사용자 실콘솔의 motor arm거부가 재현돼 이전 콘솔순서의 실행권장은 중지했다. 입력파일 정상내용/장치등록과 실제조작복구를 구분하며, 현재는 매핑범위만 기록한다. 모터/스로틀은 후속 사용자 요청까지 보류한다.

직전 Build00319.61초·Run003 신규12/기존회귀11=23Success(19clean/4warnings), 실제savedRacer의 직접API 생명주기·551개관측(헤더포함552행)은보존한다. 실제console/Slate/실물조종 전체경로 Pass를 뜻하지 않는다. 구 motor 콘솔 지침은 실제사용 경로에서 검증되지 않았다. 기록된 사용자 DroneRotorThrottle -1 뒤 약21.6초 후 DroneMotorArm true가 Pawn에 도달했지만 low-throttle조건으로 거부됐다. Root의 recorded-log replay는 exit1 RED이며 새 엔진실행/전체장치 입력시험이 아니다. 원인확정·스로틀/모터 수리·최종Pass는 하지 않았다. 이번 후속에는 production patch·Build·PIE검증 실행 결과가 없다. 사용자Editor의 진입/possess 관찰과 이전23자동검사를 이번 복구완료로 합산하지 않는다. [정정이력](../history/DRONE_WORKLOG.md).

별도 ChaosContactComparison은 실제 sphere body 질량2kg·대각관성0.05kgm² 재조회·solver 진행0.100000005초/마지막dt0.008333334초·힘가속/바닥정착을 확인한 최소 비교다. full Chaos flight callback/backend를 설치한 것이 아니며 `ChaosCandidate`는 명시거부한다. 확장B/ChaosC의 최종채택·실기체교정·payload/비영CG·일반강체/로터충돌·고속추락·제품미션 altitude/net/observer 호환·전기체전환·손조종/숙련자 평가·패키징은 미완료다.

## 확정한 방향과 아직 정하지 않은 것

|구분|현재 결정|후속 결정에 미치는 영향|
|---|---|---|
|Racer|실제 레이싱 드론을 참조한다|레이싱에서의 입력 반응·선회·스로틀 보정·FPV 시야를 비교한다|
|Scout·Drop·FPVStrike·FiberOptic|전쟁에 사용되는 기체를 역할별로 참조한다|정찰·운반/투하·FPV·유선 역할의 질량·적재·제어·카메라 차이를 조사한다. 모든 기체를 같은 FPV Rate로 통일하지 않는다|
|GroundUGV|공중 기체와 구분한 지상 모델을 유지한다|주행·접지·조향을 별도로 검증한다|
|실기체 모델·정확한 사양|미정|질량·추력·관성·배터리·로터 수치를 이름만 보고 정하지 않는다|
|주 제어 모드·Rates/스로틀 설정|미정|Mode1/2 축 배치와 Rate/Angle/고도·위치 보조를 구분해 정한다|
|사용·검증 장치|일반 게임패드와 InterLink DX 모두|두 장치를 따로 검증한다. InterLink 카메라 상하의 축/버튼 배정·보정 정책은 미정이며 새 배정 승인이 아니다|
|비행 로그·영상·숙련자 평가|자료와 평가 가능 여부 미정|자료 확보 전에는 일반 모델/수치 검증과 실기체 일치 판정을 구분한다|
|최종 물리 구조|확장 B와 Chaos C 모두 미확정|참조 응답·회전 관성/포화·접촉 요구와 성능을 비교한 뒤 선택한다|

참조 종류만 확정된 상태다. 특정 제품 채택·실제 제어 모드·현실감 합격 기준까지 결정된 것은 아니다. 장거리 타격 후보의 플레이 기체 구현도 이번 계획에 포함해 완료 처리하지 않는다.

## 현재 구현에서 출발할 부분과 한계

Legacy 기본 구조는 [역할·조작 가이드](DRONE_TYPES_AND_CONTROL_MODES.md)를 따른다. 아래 기본/게임·Legacy Acro 한계는 기존 모델에 대한 정적 조사이며 위 opt-in 로터후보와 구분한다. 여섯 DA 수치의 이전 C PC 조회를 전기체 실사양으로 쓰지 않는다. 이번 실제Racer 런타임의2kg/40N/tau0.055만 별도 확인했다.

|부분|현재 확인|현실 조종감 검증에서 필요한 구분|
|---|---|---|
|기본/게임 조작|UFloatingPawnMovement에 이동 입력을 주며 기울기 표현·감속 계수가 다르다|기체 자세가 로터 추력의 방향을 바꿔 가속하는 구조와 동일하지 않다|
|Acro|추력·질량·중력·모터 응답·항력을 계산하고 각속도 응답을 적분한다|각속도 1차 응답과 직접 자세 회전은 관성 텐서·유한 토크·모터 배분/포화를 계산하는 모델과 다르다|
|기체 프로파일|이전C PC의6개DA 공통2kg/40N 일부값·BP override 꺼짐, 이번D PC actualRacer2kg/40N 확인|synthetic 가상값과 실사양을 구분하고 나머지기체 런타임/UGV 공중추력 적용을 추정하지 않음|
|바람·항력|Acro 속도/항력과 WeatherResponse의 별도 AddActorWorldOffset Drift가 나뉜다|Movement 속도·위치 차분·바람을 함께 계측하고 새 상대 공기속도 공력과 기존 위치 이동을 중복 적용하지 않는다|
|배터리·적재|시간 기반 배터리와 적재 질량 반영은 있다|전압 강하·가용 출력·적재 위치/무게중심·회전 관성은 별도 범위다|
|접촉|몸체/로터 충돌 검사·반사·시각 회전 반응이 있다|충돌이 없는 것이 아니라, 접촉 충격량이 실제 각속도에 미치는 강체 회전과 구분해야 한다|
|모터/접지 상태|Legacy 중립은호버/정상OFF아님. 로터후보는별도motor arm/OFF·접지/재이륙 구현·자동검증|공격ArmSwitch·출력0·배터리fault/Health사망·정상착지를분리, 실물채널매핑은미추가|

UFloatingPawnMovement는 속도·가속 제한을 제공하지만 자체 중력은 구현하지 않는다. 프로젝트 Acro가 더한 중력과 엔진 기본 이동 기능을 혼동하지 않는다. [Epic 공식 API](https://dev.epicgames.com/documentation/en-us/unreal-engine/API/Runtime/Engine/UFloatingPawnMovement)

Legacy 제동값의 정지 시간/거리는 조건부 예측이다. 실제 입력·풍속·적재·모드 계측 전 사용자 관성을 재현한 값으로 쓰지 않는다. 위1차후보 자동검증도 실기체 현실감/숙련자 합격 완료가 아니다.

## 권장 접근과 B/C 선택 기준

추천 순서는 **참조 조건과 입력/화면 기준 확보 → 한 기체의 응답 계측 → 모델 한계 확인 → 구조 선택**이다. 먼저 제동 수치만 올리거나 엔진 물리 옵션만 켜는 방식으로 현실감 달성을 선언하지 않는다.

|후보|유효한 범위|결정 전에 확인할 비용·한계|
|---|---|---|
|현재 B의 단순 보정|범위를 좁힌 정상 비행의 평균 응답을 비교하는 기준|각속도 1차 응답만으로 회전 관성·포화·적재 위치·접촉을 일관되게 설명할 수 있는지 제한이 있다|
|확장 B: 직접 강체 계산 + 제어/구동 모델|질량·관성·힘/토크·모터 한계·바람을 계산하는 자유 비행 후보|접지·마찰·복잡한 접촉을 직접 구현할 비용과 기존 코드 재사용 이점을 비교한다|
|C: Chaos 강체 + 같은 제어/구동 모델|회전·접촉·마찰·충격과 동적 물체 상호작용 활용 후보|기체 계수·모터·제어기·공력은 여전히 필요하다. 이동/테더/충돌 이관과 실제 맵 CPU·프레임 비용을 측정한다|

B/C는 보정 입력→같은 제어기→모터 배분/포화→모터 응답→힘/토크를 공통 조건으로 두고 비교한다. 로터별 구동 모델과 Chaos 사용은 별개의 선택이다. 로터 4개를 그렸거나 Chaos를 사용한다는 사실만으로 현실감을 판정하지 않는다. 서브스텝도 안정성과 CPU 비용을 함께 보며, 임의 Actor Tick이 엔진 물리와 자동으로 같은 간격에 실행된다고 가정하지 않는다. [Epic Physics Sub-Stepping](https://dev.epicgames.com/documentation/en-us/unreal-engine/physics-sub-stepping-in-unreal-engine)

공통 기체 물리 위에 실제 제어 방식의 목표를 구분한다. Rate/Acro는 각속도와 수동 출력을 명령하고 스틱 중립이 자동 수평·위치 정지를 뜻하지 않는다. Angle의 자세 복원, 고도 보조, 위치/속도 보조도 서로 다른 기능이다. 기본/게임이라는 현재 UI 이름에 자동 정지·관성 정도를 임의로 배정하지 않는다. Mode1/2는 축 배치 차이로 유지한다. [PX4 v1.16 Acro](https://docs.px4.io/v1.16/en/flight_modes_mc/acro), [제어 구조](https://docs.px4.io/v1.16/en/flight_stack/controller_diagrams)

## 59번 구현안 검토와 선행 계약

사용자 제공 `59_드론물리_기반데이터_구현안_20261022.md`는 설계참고이며 원문의 구현/담당지시 자체를 승인으로 보지 않는다. 이후 사용자의 직접 구현 요청 범위로 Racer1 opt-in 후보를 작성·검증했다. 기존Definition/FlightProfile·입력API/ID/저장 구조를 재사용하되 실사양/계수·최종확장B/ChaosC 채택은 여전히 미정이다.

- **시간/callback:** 자체 고정 accumulator·Chaos 가변 substep·fixed async를 구분한다. 실제 callback의 dt/SimTime·입력 timestamp·wall/game/physics 시계·catch-up/drop 정책과 배터리/랩/카운트다운의 시간을 먼저 정한다. 120/240Hz·8step은 비교 후보이며 확정 주기/한도가 아니다.
- **단위·CG·관성:** World/Body/주관성축·원점·deg/rad·좌표 부호와 SI→엔진 변환을 계약한다. COM offset을 절대 CG setter로, 관성 getter를 tensor 적용 API로 취급하지 않는다. 적용/재조회와 단위 힘·토크 검사를 준비하고 힘/중력·위치/자세 작성의 중복을 막는다.
- **기존 자산 이행:** 모델/스키마 버전 또는 명시적 opt-in과 조건부 검증을 둔다. 새 로터/관성 필드를 즉시 필수화해 기존 DA/BP의 출격·Preview·재출격을 막지 않는다. enum 숫자·Mission/Drone ID·저장 키·BP override/API를 보존한다.
- **계수 채택:** 60N과 제안 질량 조합·관성/CG·공력·모터/전압 계수·현수 길이·합격 오차는 채택 보류다. 표본의 제조사 값·합성 시험값·현재 가상값을 분리한다. 현재 합산 추력 상태의 지연을 같은 수치의 RPM 지연으로 옮겨 같은 응답이라고 보지 않으며 전압/전류/RPM/추력 모델을 닫고 sag를 중복 적용하지 않는다.
- **고정/현수 화물:** 고정 anchor·작은 진폭의 진자 기준과 움직이는 기체-화물 결합 검사를 분리한다. 별도 화물 질량을 기체에 중복 합산하지 않고 slack/인장 전용·기체 반력·해제 시 위치/선속도/각속도 이행을 정한다.

Legacy 회귀 기대값과 이관/조건부검증을 보존하고 신규커널5·pilot6·프로필1 및 기존회귀11을 Run003에서 확인했다. 과거59 정적조사와 이번실행의 실패/수선·계측·소스보존은 [WORKLOG](../history/DRONE_WORKLOG.md)와 `Saved/Automation/PhysicsImplementation_20261022`가 정본이다. 최소Chaos접촉 통과로 fullflight backend/실기체일치/B·C채택을 선언하지 않는다.

## 잔여 작업과 완료 기준

아래는 착수 순서와 검증 범위의 제안이다. 조사 완료를 각 기능의 구현 완료로 바꾸지 않는다.

|작업|현재 상태|다음 작업|완료를 판단할 근거|
|---|---|---|---|
|참조 기체·입력 계약|기체 종류 방향과 일반 패드·InterLink DX 두 검증 대상 확정, InterLink 카메라 상하 추가 축/버튼 배정·보정 미정. 기존45매핑/비행4축·Mode1/2 보존|역할별 후보 중 첫 참조 기체/제어 모드·조종기·Rates/expo·스로틀·FPV 조건을 정리|참조와 미정 항목, 재현 가능한 장치/프로파일 기록|
|현실적인 비행 물리|Racer1 opt-in FixedStepCandidate 구현·신규12/회귀11 Success, controlledMap/Acro1·2/CG0|payload/외부writer·실기체참조/장치/숙련자 검증·동일조건B/C비교|힘/토크/시간/실접지 실제계측과 회귀·한계·실기체반복과제 구분|
|화면 상하 시야·감도|쉬운/게임 조작의 감도X/Y·반전·UI/저장 구현, D PC 지정 자동 검사와 PNG 검토 확인 범위는 [설정 가이드](DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#카메라-감도반전과-designer) 참조|두 장치의 원시 축→Input Action→모드→SpringArm→최종 ViewTarget 계측. InterLink 상하 배정은 미정|실물 장치별 양방향/해제·적용/취소/기본값·실제 재실행/구버전 저장 복원. 자동 입력·메모리 직렬화와 구분|
|모터 OFF·착지·재이륙|Racer후보의 저속OFF→실접지→rearm/재이륙 PIE자동검증 완료|경사·고속충돌/공중OFF 보정·본미션writer/다른기체·실물장치 후속|안전저속과 경사/고속/실제장치 조건의 반복기록을 구분|
|LOS 사람 후퇴·드론 보기|후퇴/추적 구현·4단계 자동 계약 통과, 사람/드론 가시성 미확정|검사 World/LocalPlayer 연결 캡처·HitResult 디코더 수리 후 지면/가시성 확인|실제 TUT_LOS에서 사람 메시/카메라가 드론을 보고 과도한 Pitch/Roll 없이 가시성 확보|
|M3·M4 오브젝트/목표|M3 현행 목표·M4 실제3지점/UGV접지·3목표 자동 통과. 자동 피해 이벤트이며 손 조종/발사 아님|실물 플레이·M4 공중 기체 높이·최종 출발 위치/안전성·시나리오 보완|실제 맵의 진행/실패/성공·장치 입력, World 일치 화면과 구분 기록|
|본미션 렉|1280×720·품질3·출발점 무입력10초 CPU 계측 확보, 전체 플레이/GPU 미검증|M3 Fence BP 오류·CSV ensure와 M4 Lumen 경고를 분리 조사. 같은 입력/비행/사격 구간 계측|변경 전후 같은 과제 p50/p95·최대 지연·GPU 지원 확인. 진단 우회는 최적화 근거 아님|
|본미션 로딩|M3/M4 요청→선택→조작과 엔진 LoadMap 구간 확보, 수치는 WORKLOG|같은 PC/옵션·cold/warm/순서·입력 과제로 반복 비교|구간별 시간과 반복 편차. 프로세스 전체/캡처 대기를 로딩/FPS로 쓰지 않음|
|사진·실물 입력 회귀|M1 조망/DROP·M2 차량 상세 연결, UI 검사 통과|M2 도로와 차량 대표·M3 재밍 외형/진입이탈·M4 전체/출발3곳 보완|사진 메타데이터/맵·대상 일치와 실제 키보드/패드 플레이. M3 흰 원반은 graybox이며 최종 레이더 외형 아님|

공중 모터 OFF·일반 착지는 배터리 소진의 파괴 경로를 그대로 재사용하지 않는다. Racer후보는 무장 ArmSwitch와 별도인 motor armed/OFF·저속접지/재이륙을 구현·자동검증했으며 전기체·경사/고속충돌·본미션/실물장치 확대는 후속이다. 화면 상하 카메라 피치는 기체 상승/하강이나 기체 Pitch와 구분한다.

## 변경 책임과 구현 전 계약

|담당 클래스/자산|다룰 책임|변경 전 맞출 계약|
|---|---|---|
|DroneFlightPawn·입력 IMC|입력 해석·모드·기체/카메라 명령 분리|장치 범위·중립 의미·축 배치·시점 전환·기존 Blueprint API|
|DroneAcroFlightComponent·이동/충돌 담당|힘·각속도/토크·적분·접촉을 적용하는 경로|위치/자세/속도의 단일 소유 경로, 바람과 호출 순서, 제한된 계산 간격|
|DroneDefinition·FlightProfile·Pawn BP|기체별 값과 자산 override|질량·추력·관성/무게중심·응답·항력의 단위/출처·적재 조건, 원본 백업|
|WeatherResponse|날씨 바람 전달|상대 공기속도와 위치 이동의 일관성|
|SettingsWidget·설정 Subsystem|카메라 감도/반전과 저장|UI/백엔드 소유 파일 조율, 적용/취소/기본값/기존 저장 호환|
|GroundDrive·LOS|UGV 주행과 관찰자 시야|공중 모델과 구분, 실제 TUT_LOS/UGV 맵 회귀|

기존 enum 숫자·Mission/Drone ID·저장 키·팀원 원본은 유지한다. 조정값은 Blueprint/Data Asset에서 바꿀 수 있게 하되, 실제 사양을 확보하기 전에 임의 수치를 확정하지 않는다. 생산 코드·자산 변경은 [세션 소유권](../git/DRONE_WORK_PC_SESSIONS.md)의 실행/카메라 담당이 범위를 맞춘 뒤 수행한다.

## 검증 단계

1. **참조와 입력/화면 기준:** 장치 min/center/max·갱신 간격·deadband·Rates/expo·스로틀·FPV 장착각/FOV를 기록한다. USB 입력부터 카메라/렌더까지 지연을 나눠 본다.
2. **한 기체의 정상 비행:** 같은 무적재/실제 적재·전압·무풍/바람 조건에서 호버·상승/하강·완만한 선회와 작은 각속도 입력을 비교한다.
3. **모델 한계와 구조 선택:** 저/중/고 출력의 반전·포화/복구·적재 위치·모터 OFF/접지에서 남는 오차를 확인해 확장 B/C를 선택한다. CPU·프레임·메모리 비용도 같은 맵에서 비교한다.
4. **숙련자 평가:** 같은 조종기/카메라와 과제로 입력 보정량·오버슈트·시간·주관적 차이를 함께 기록한다. 보정에 쓴 기동과 검증용 기동을 구분한다.
5. **실맵 회귀:** Physics Sandbox의 분리 시험 뒤 실제 본미션·TUT_LOS·팀원 레이싱 맵1·2·3·UGV에서 확인한다. 다른 맵의 통과로 대신하지 않는다.

합격 오차는 참조 반복 편차와 로그 해상도를 확인한 뒤 정한다. 프레임별 수치 차이·가상 호버 기준만으로 ‘실제 조종자 이질감 거의 없음’을 확정하지 않는다. 새 실제 비행을 요구하기보다 이미 보유한 로그/영상·제조사/제어기 자료부터 활용한다.

엔진은 본미션/LOS/성능 실행 세션 하나만 사용한다. 읽기6GiB/UI RHI10GiB/실출격12GiB/Camp 일반20GiB·승인된 저메모리 모드16GiB 시작 여유와 실행 중 RAM·commit 각각4GiB 보호를 유지한다. 미달이면 같은 조건 반복이나 사용자 앱 강제 종료를 하지 않는다. Production Training 원본을 시험 저장하지 않으며, 10분 초과 패키징/전체 쿠킹/DDC 작업은 실행 시점을 먼저 확인한다.

현재 UI·M1 출격 상태와 PC별 실행 수치의 정본은 [STATUS](../../STATUS.md)·[WORKLOG](../history/DRONE_WORKLOG.md)다. 새 RHI 검사 통과는 물리 입력·미션 완료·패키징·숙련자 평가의 완료가 아니다. 실행 순서는 [WORKBOARD](../../WORKBOARD.md), 현재 화면/출발·목표 확인은 [시험 가이드](DRONE_TEST_MAP_GUIDE.md)를 따른다.
