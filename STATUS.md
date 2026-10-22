# 현재 작업 상태

기준일: 2026-10-22 KST C PC. 최우선 목표는 현실 조종감. Racer=레이싱용·기타공중=역할별 전쟁 사용 참조 방향 확정, 모델/사양·장치·확장B/ChaosC 미정·새물리구현0. UI RHI4종/24캡처·M1 출격상태 확인, 미션완료/실기와 구분. [근거](docs/history/DRONE_WORKLOG.md).

## Git 기준(10/22 로컬 추적 ref·Fetch 없음)

| 저장소 | 현재 기준 | 상태 |
|---|---|---|
| Unreal 추적 origin/main | `17938bb7` | 현재 HEAD가1개 앞섬, 이번 Fetch/Pull 없음 |
| Unreal C PC `C:\URproject\drone` | HEAD `c589bbf9` | 빌드14.14초·UI RHI4종·M1출격상태, 새물리구현0 |
| 문서 추적 origin/main | `9995d8e1` | 로컬과0/0, 이번 Fetch/Pull 없음 |
| 문서 C PC | HEAD `9995d8e1` | 역할5 관련 문서 미커밋, Commit/Push 없음 |

## 10/18~20 최신 구현과 확인 경계

- **Story4 UI/사진**: 새사진뒤 Data/Layout1280/Layout1920/ActionLabel4Success·24PNG. M1 Battlefield/Drop/Player0·DirectorActive·목표0/1 확인; 완료/물리입력 미검증. M2미시작·M3/4최신오브젝트/실출격·패드 후속. [정본](docs/gameplay/DRONE_TEST_MAP_GUIDE.md#story4-선택브리핑-검증-경계).

- **기반 구현**: DA 숨김/준비 중·다음 수업 건너뛰기·맵 비저장 Runtime Placement·미션별 RecordCourseId. 튜토리얼 TUT 맵/DA·HUD WBP/캡처 도구는 현재 커밋에 있다.
- **UI/훈련**: 그림 위는 번호만·키/동작은 아래 범례로 정리. RC 세로 토글 스틱·Scout/FPV 바닥 없는 실제 모델 사진·튜토리얼 권장창 한글 적용. D PC Build·UI4/4·사진1종 자동 검사 통과, 1280×720/1920×1080 렌더 확인. 실물 조종은 별도. [조정](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#훈련-사진조작-장치-그림시작-위치).
- **목표 매니저**: 배치형 BP_DroneMissionTargetManager로 스포이드 대상 교체/판정·나침반 방향/거리 연결. 새 경량 시험장 제공. [설정](docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md#스포이드-목표-연결과-나침반).
- **전투**: 차량300·포탑200·MG25·유탄150·자폭600. 직격 중복 방지·자폭 잠금·NPC 래그돌 유지. 포탑 자체 HP0 폭발/소리1회·점유 해제·연결 메시 잔해15초 정리 구현, 실제 TUT 파괴/클리어 검사 통과. 청감/밸런스 수동 대기. [조정](docs/gameplay/DRONE_GROUND_CONFORMING_VEHICLE_AND_VISUAL_BANK.md#차량-피해자폭npc-사망).
- **오프닝**: Main_cinematic.mp4를 새 실행에 재생·종료/Esc로 타이틀, 실패 시에도 복귀. MP4는 LFS·패키징 NonUFS 설정. [설정/시험](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#시작-오프닝-영상).
- **이전 C PC 검증**: Build5.11초 성공. Story4맵의 출격/목표→결과·나침반·NPC Nav 투영 자동 통과, 시작/목표 촬영. Camp는 승인된 임시 저메모리 설정만 검증(일반 화질/장시간 Pass 아님). Lumen 캐시 초과·출발 피격/흔들림은 잔존. 손 조종·전역172·패키징은 별도. [근거](docs/history/DRONE_WORKLOG.md).
- **이번 수정**: API 선택/미리보기/포커스 일치, 호버 진행 지연, UGV 검사 이름 충돌, MG Static 경고, 로딩 최소 표시/ReadyHold의 시계 혼용을 수정했다. AI 검사는 선행 자동 교전을 격리해 점유/사망·재점유/수색·복귀 통과·기본 회귀 복귀. 제품 리시 규칙 유지.
- **레이싱**: 공통 BP의 DroneRacing 본체에 맞는 DroneSky 프로펠러4개를 복구하고 선택3D도 같은 BP로 연결했다. 원형/도시 출격·회전 중심/선택3D3종 통과. 앞선 본체 단독 검증 누락을 정정하며5미션/맵·기록/비행 값은 유지한다. 손 조종 완주는 별도다.

이전 Gate/Rain/City 검증·팀원 수신은 [WORKLOG](docs/history/DRONE_WORKLOG.md)에 보존한다. 오후 UI 검증은 아래 범위이며 수신 맵 전체·패키징·실제 패드 Pass로 확대하지 않는다.

## UI·WBP·UGV 현재 상태

- **편집 정본**: `/Game/Drone/UI/WBP` 화면22종·시작4곳 우하단·사진600×360·모서리8파츠·선택 강조를 유지한다. Native Mission 출격도 저장된 Mission WBP7종을 사용해 Designer 수정이 실제 화면에 반영된다. 명시적 BP 클래스 지정은 보존한다. [편집](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#화면별-wbp-편집-정본).
- **설정/HUD/문구**: 타이틀 설정 Z 순서·일시정지 재오픈 Back 구독을 수리했다. 사용자 제보로 발견한 설정 WBP 폭106,244 오류를1240으로 복구하고 로비/일시정지 공통 WBP에 연결했다. 실제1280×720·2553×936 창에서 표시 크기·마우스/뒤로2회 왕복 통과. 한글 CDO/정적 문구·번호10·사진 회색 띠·허브 박스 숨김·고도 흰 테두리 제거·입력 십자선 반영, HUD13구역/사용자 배치 보존. [정본](docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md#hud-편집-정본).
- **기체 선택**: 새 투명 PNG5장을6종 카드/사진 모드에 연결했다(2번 정찰·광섬유, 4번 레이싱). 전체 비율 Fit·3D/도시 배경/6카드/Back 배치 유지. 1280/1920 사진 검사2/2·실제 캡처 확인, Sky 긴 설명 간격은 후속이다. [조정](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#드론-선택창-이미지-바꾸기).
- **목표/튜토**: Tutorial9·Story4에 검색 가능한 BP_DroneMissionTargetManager 유지. FreeGate 실제 맵/13게이트 완주 통과. 배달2 지정3상자→Cylinder는 겹쳐 적재해도 고유3개를 집계하며 실제 집기/물리 투하3회→성공 통과. 옛 가방/팔레트는 해당 레벨에서만 제거했다. **LOS의 이륙→전진→후진 복귀→실제 착지는 그대로 유지한다.** [편집](docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md#이미-배치된-맵에서-바로-찾기).
- **게이트/포트/Nav**: BP ‘상태 색상’의 상태별 머터리얼이 있으면 원본 색/발광, 빈 상태만 BP 기본값을 자동 사용한다. Param/Color 호환·Build53.04초·Gate4/4. 기존 포트/Nav 검증은 유지하며 수신 Training 맵은 재저장하지 않았다. [조정](docs/tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md#세-상태-색과-머터리얼-조정).
- **10/20 실행 근거**: Development Build32.35초 성공. 회귀14개 중13통과/원형의 낡은 귀환 기대값1실패를 보존하고, 검사만 현행 규칙으로 고쳐 원형 계약+실제 CircleGate2/2 통과. 실제 M1 선택/배달·고유 화물·선택 배경4/4도 통과했다. 위 현재 Gate 집중검증과 구분한다. 실행별 근거는 [WORKLOG](docs/history/DRONE_WORKLOG.md).
- **10/20 보존 감사**: 당시 추적 자산9,755개 누락/LFS 포인터/삭제/충돌0·Production 해시 일치. 오늘 전체 감사를 반복하지 않았다. 기존 맵 경고·실물 패드·손 조종 전체 경로·청감·패키징은 별도다. 이번 Git 병합은 위 표를 따른다.

## 한눈에 보기

첫 LOS는 현재 팀원 `Tutorial/TUT_LOS`·BP_LOS 눈높이를 사용한다. 이전 Observer TestMap은 보존했다. 그물 PBD·벽/로터 Sweep·카메라 분리/피해 Shake는 유지하며 실제 Chaos 제작·수동 체감은 후속이다. 세부 이력은 WORKLOG.

현실 조종감의 참조·구조대안·카메라/LOS·모터OFF/착지·실맵/성능 잔여계획은 [개발 기준](docs/gameplay/DRONE_REALISTIC_HANDLING_PLAN.md)이 정본이다. 조사/계획 완료이며 구현 승인이 아니다. 현재 UI/출격의 상세 실행근거는 WORKLOG, 다음은 WORKBOARD를 따른다.

UI 현재 상태는 아래 요약을 따른다. Pretendard 공통 적용·기존 아트/ID/저장키 보존 유지. [UI 가이드](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md), 상세는 [오후 WORKLOG](docs/history/DRONE_WORKLOG.md#2026-10-16--오후-ui-전면-개편wbp-전환ugv-무장).

OilRig 근거리 사본3개만 camera-local·생성축Yaw-90°로 화면 가로에 맞추고 위치 보정을 분리했다. Billboard만 돌리거나 위치Y만 옮기던 방식의 실제 도시 쏠림은 수정·렌더 검증됨. A 마스크/부드러운 폭·품질별 Niagara1개/ISM0·차폐/원본 유지, Off/Clear/Disable 즉시0과 실내 자연 소멸은 구분한다. 실기·실내 복귀/FPS는 대기. [비/BP 조정](docs/gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md).

랜덤 도시 외형은 완성 건물BP를 한 동만 배치하고 명시한 닫힌 SingleMesh 모듈만 같은 방향으로 적층한다. Container01·슬롯별 MaterialOverrides fallback·도로 차선·프로젝트 소유 팔레트를 연결했다. 실제 시드194849의 도로/컨테이너/뼈대/창고4장 외형 캡처를 확인했으며 완주·재시작·기록 복원 수동 Pass는 아니다. [조정 가이드](docs/gameplay/DRONE_TEST_MAP_GUIDE.md#랜덤-도시-레이싱-외형모듈-조정).

`TUT-GATE-SAVE-01`: 로컬 Gate BP1개로 **CDO MID private 참조 저장 거부** 재현→C++/적용 도구·Gate BP 수리. 기하/색·16컴포넌트 보존·MID참조17→0, 새 프로세스 검증·위치 수정 포함 저장/재로드3회 성공. Gate5/5 Success(기존 정리 경고100). 팀원 크래시와 동일 여부/실기는 대기. Source와 BP 함께 받아 종료 후 Build, Production 미수정.

기존 수동 확인: `쉬운 조작 / 게임 조작 / FPV 모드 1 / FPV 모드 2` 한 줄 표시·폭 보정과 초기/재픽업 공통 집게 자세 구현·자동 검증됨. 수동 화면/실제 패드·화물 파지 외형은 대기. BP 조정은 Drop Pawn의 `PayloadCarryAnchor`, 화물의 `PayloadVisual`; 절차는 [역할 가이드](docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md), 이력은 [WORKLOG](docs/history/DRONE_WORKLOG.md).

이전 수신 소스에서 확인한 후속: 시드 기반 도시/날씨/레이싱 생성·지정/무작위 시드·같은 시드 재시작, Story/Procedural 로딩·취소·미션 Esc/Start 일시정지/복귀, 완료 미션/Story Fact/권장문구 JSON 저장과 최고 랩 구간 저장이 있다. 구현 코드 존재와 현재HEAD 실행 성공은 다르다. 기능 근거/미확인은 WORKLOG·아래 표 참조.

`TUT-GATE-PRESENTATION-01`: Island의 Gate Scale `(1,2,2)`와 메시 작성Yaw90°가 UE Transform에서 다른 축으로 합쳐져 폭이 줄던 원인을 Native Visual 보상으로 수정했다. 새 읽기 전용 재로드에서 활성BP112개 좁아짐0, 숨김Native352개 보존·맵/BP/Course 바이트 불변·저장0 확인. 자동 Gate의 0 접선 방향도 유한 차분 fallback으로 교정해 직선/코너/닫힌 루프 회귀를 통과했다. m_green은 백업 후 Nanite 사용 플래그만 수리·저장했고 Final2 RHI에서 해당 경고 없음. Island 재저장·잔존 삭제는 필요 없다. Main의 당시 Native20 기록과 Island352는 별개이며 Main 현재 참조·세 상태색 실기는 대기다. [배치 가이드](docs/tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md).

`AI-PATRIOT-PIVOT-01`: `/Game/Drone/AI/Blueprints/Turrets/BP_PatriotMissileLauncher` 생성·초기 회전 검사 완료 뒤 10/13 12:50 Editor 재저장(현재35,958B)이 확인됐다. 현재 저장본의 축/이음새·복합 회전은 재검증 대기다. 생성 구조는 Lower 고정→YawPivot→Middle/PitchPivot→Upper, Yaw/Z·Roll/X 조절. 기존 편집을 보존하고 생성 도구로 덮어쓰지 않는다. 원본3메시·Missile_M, AI/발사/입력/충돌·차량 배치 미포함. [MG·패트리어트 가이드](docs/ai/DRONE_MG_TURRET_3PART_GUIDE.md#6-패트리어트-미사일-포대-접합부-회전축-조정).

`UI-RESULT-LAYOUT-01`은 저장된 Mission/WBP_DroneMissionResult Designer에서 좌측 버튼/우측 정보 카드를 편집한다. 실행 시 작성한 배치를 유지하며 옛 중앙680 기록은 현재 외형의 근거로 재사용하지 않는다. [UI 가이드](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md)·WORKLOG 참조, 실제 화면/패드는 대기.

10/06 C PC Claude: D-5 출발부터 랩 타이머 측정·D-12 Flight 명명과 피격/Acro/지상 주행 컴포넌트 분리 구현됨·자동 검증됨. 화면·FPV/UGV 체감 수동 확인 대기. 기존 NPC/높이 제한/매니저·Legacy 정리 유지, D-13 종료. 레이싱은 아래 팀원 변경 수신 상태를 따르며 배터리 시간·높이 제한 수치/경고 연출은 현재 미정. 세션 전문은 [WORKLOG](docs/history/DRONE_WORKLOG.md).

| 영역 | 구현·자동 검증 | 수동 확인 대기·미구현·현재 미정 |
|---|---|---|
| 시작·로비 | 5메뉴·WBP 연결 유지, 현재 로비/브리핑/기체 선택은 위 UI 요약 | 실제 패드·마우스·1280/1920 대기, 미정은 위 요약 |
| 조종 입력 표시 | 설정 수동 ON/OFF·선택 저장, 저장 `WBP_DroneControlInputDisplay` 연결. 아래 중앙 스틱 표시·OFF 갱신 중지, 고도계 독립 | D-3 기본 False 확정, 장치 자동 전환/분리·재연결 정책 미정. 실제 화면/패드 확인 대기 |
| 코스 표시선 | 긴 코스만 sqrt(곡률) 밀도+15% 균일 몫, 짧은 TestMap68/113조각 기존 균일 분할 유지. MaximumCourseLineSegments 노출·기본1024(시작값·미확정), BP 드래그 재구성 Off | 팀원 Production 코스 외형·Editor 편집 체감 수동 대기. Production 맵 미저장 |
| Acro | InterLink DX Acro 4축 추가·Mode 2 실측·세로축 반전 해제(10/07 D PC Claude), [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md). 비행 기체 FPV/Scout/Drop/FiberOptic 6개 입력 연결, 패드 축 4개 Dead Zone, 정확 자세 적분. 키보드·패드 입력원 분리·절댓값 큰 쪽 사용·키 해제 시 패드 인계, Space 단독 자세 불변·Mode 1/2 키보드 동일·FPS 무관 자동 검증 | 실제 패드/키보드 체감·Scout/Drop 비행 대기. 키보드 각속도 배율·Angle 모드·마우스 Yaw·회의 “좌우 스틱 반전” 뜻 미정 |
| 패드 첫 포커스 | `FDroneGamepadFocus`가 포커스 부여 후 5프레임 감시·루트/없음으로 이탈 시 복원, 다른 강조 버튼 이동은 보존 | UI-FOCUS-RACE-01 **수정 후 확인 중**. 화면 그려진 수정 전 Fail/후 Success 각 1회, 간헐적 첫 버튼 강조 수동 확인 대기 |
| 튜토리얼·Story 순서/저장 | Tutorial8·Story4 유지, 레이싱은 팀원3맵+별도 랜덤도시. 완료 미션/Story Fact/권장문구 JSON 저장 구현·ProgressSave 자동 검사 | 실제8수업·전체 완료·로비/재실행 확인 대기. 준비 중 수업·정식 건너뛰기 정책은 별도 |
| Best Lap | `CourseId|DroneId|ControlMode`별 JSON·구간 저장/복원. 팀원3맵 완주/저장 및 새 프로세스 복원 자동 통과, 시험 전용 슬롯 사용 | 같은 조건 사용자 실제 완주2회·HUD/구간 대비 체감. 자동 순간이동 기록을 실제 플레이 기록으로 쓰지 않음 |
| 허브·HUD | 현재 HUD Kit은 위 요약. 기존 배터리 제한/방전 추락 구현·이전 자동 검증 유지 | 실제 HUD·배터리/풍향 체감 대기. 기체 시간0·최종 시간/음원·신호 대역/분기·재출격 브리핑 미정 |
| 미션·실패 | DA 자동 등록·Definition/Rule/Trigger·체크포인트 재출격 유지. D-6 높이 제한 매니저 구현됨·자동 검증됨(10/05 C PC Claude): `/Game/Drone/Managers/BP_DroneAltitudeLimitManager` 배치·BP 값 설정으로 적용. Mission/Weather 매니저 BP도 같은 폴더로 정리됨. 상세 [WORKLOG](docs/history/DRONE_WORKLOG.md) | 높이 제한 체감·날씨 시험 맵 수동 확인 대기, 높이 제한 수치·경고 연출 현재 미정. 체크포인트 미배치·첫 출격 위치 재출격. 추락 체감·새 DA 등록 및 Story M1~4 콘텐츠/분기 고도화 확인 |
| 레이싱 | 기본 팀원1·2·3 진입/자동 완주·기록 복원 통과. 개인 랜덤도시/옛 Circuit Test 별도, 도시 모듈/재질·비 분포 유지 | 실제 조종·패드·무작위/같은 시드·로딩 취소·결과/기록 체감 대기 |
| 물리·역할 | 질량·추력·모터 응답·선형/제곱 항력·Drop kg 하중, Mode 1/2 공통. 속도 단계 제거. 벽/날개 접촉·그물 포획 Greybox·접촉 카메라 분리, 피해 Shake 유지 | Acro는 게임용 근사 모델, 실기체 교정 미완료. 수동 속도/하중/접촉·실제 Chaos 비교 필요 |
| AI·차량·날씨 | AI-LOCOMOTION-01 다리 고정 후속 구현됨·자동 검증됨(10/05 C PC Claude): 아군 Retargeter Pin Bone·적 발 IK Control Rig 제거. 양손 총 파지·hand_r 부착 유지. 원인·보폭 검증은 [WORKLOG](docs/history/DRONE_WORKLOG.md). StateTree Soft 참조/AlwaysCook·Rifle/MG 디버그 기본 Off 유지. 차량·바람/비·천장 차단, D-6 HUD 방위 통일·불어오는 쪽 풍향 구현됨·자동 검증됨. 비 품질 구현됨·자동 검증됨(10/07 C PC Claude, HEAD `cb77c0d`·스테이징): 끔=전부Off·낮음/중간/높음=카메라 주변 원본 Niagara1개·판 빗줄기 기본0. Weather 전체·SettingsContract Success. [비 가이드](docs/gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md#비-품질-설정과-조정)·[실측/정정](docs/history/DRONE_WORKLOG.md#2026-10-07--비-연출-도입비-품질-옵션-c-pc-claude) | NPC 걷기 다리·속도 대비 보폭/발 미끄러짐·손/총 정렬·사격/재장전 수동 확인 대기. 적 경사면 발 맞춤 없음·Pin 뒤 IK 뼈 잔존 원인 미특정. 최종 애니메이션/산탄총 전용 동작 미정·미구현. 감지 PIE KnownIssues Fail 유지, 풍향 HUD·날씨 시험 맵 수동 확인 대기. 비 입자 크기/모양·위치/양·젖음/물결·음원/실내 감쇠·설정 패드 수동 대기. 단계 최종값/음원 확정 현재 미정; 화면 물방울/바닥 Splash 미구현 |
| 환경·기체 | D-12 2·3차 구현됨·자동 검증됨(10/06 C PC Claude): Flight 클래스/소스 경로로 변경·ClassRedirects 3개, 피격/Acro/지상 주행 컴포넌트 분리. BP 이름·자산 경로 유지. Legacy 1차·Characters 변환 원본 유지, D-13 종료. 상세 [WORKLOG](docs/history/DRONE_WORKLOG.md) | FPV 곡예·UGV 주행 분리 전 동일 체감 수동 확인 대기. 방콕 삭제 커밋/푸시 상태 별도 확인. 사람 최종 아트·애니메이션·음원 보존 |
| 패키징 | Asset Manager DroneMission/DroneDefinition AlwaysCook·MissionMap 참조, StateTrees 폴더 DirectoriesToAlwaysCook·StateTreeCookContract 자동 검증 | 실제 패키징/패키지 맵 진입 미실행 |

- Acro 혼합 입력·Dead Zone·자세 적분 조사(10/04 C PC)는 [원문 보존](docs/history/archive/STATUS_2026-10.md)을 참고한다.
- 코스 표시선 측정·재실행 도구 검증(10/04 C PC)은 [원문 보존](docs/history/archive/STATUS_2026-10.md)을 참고한다.

## 이전 검증 근거 — 입력은 2026-10-07 D PC, 나머지는 10-06 C PC Claude 실행

| 검사 | 조건·결과 | 출처 |
|---|---|---|
| 입력 자산 | 기본33+축8+버튼4=45·ArmSwitch·노브 전용 메뉴 이동 구현/자동 검증됨(10/07 D PC Claude), 실기 대기. 집계 정정(10/07 Claude): test4는 17개 중 16 Success·1 Fail, 테스트 수정 후 test5 3/3 | [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md)·[WORKLOG](docs/history/DRONE_WORKLOG.md#2026-10-07-interlink-dx-버튼armswitch노브-전용-메뉴-이동--d-pc-claude) |
| Build | Editor 종료 후 Succeeded | Claude 지시서; 별도 Build 로그 경로 미제공 |
| Drone.Prototype 전체 + Drone.UI.ControlInputDisplayPIE | RenderOffScreen 1920×1080, **12/12 Success** | `Saved/Automation/ClaudeAcro/test_after_dz.log` |
| 최신 집중 회귀 | Drone.Prototype + Drone.Tutorial + Drone.UI.ControlInputDisplayPIE **32개 중30 Success·2 Fail(팀원 Production 맵 의존, 변경 전 메시지 동일)** | Saved/Automation/ClaudeCourse/review_fix_test.log |
| 최신 전체 회귀 | D-12 3차 뒤 전체101개, 실패는 KnownIssues4개·미렌더 패드 포커스6개뿐(10/06 C PC Claude 지시서) | Saved/Automation/ClaudeSplit/full_after.log |
| 입력 겹침·코스 | overlap_before 4 Fail→overlap_after, AcroInputBehaviorPIE D구역8시나리오·CourseLineAdaptiveSegments 자동 검증 | Saved/Automation/ClaudeAcro/overlap_before.log·overlap_after.log·ClaudeCourse/review_fix_test.log |
| Route 순서 의존 관찰 | 전체 5회 TrainingRouteSelectionPIE Success; 원인 미특정·해결 확정 아님 | 같은 폴더 `test.log`·`test2.log`·`final.log`·`final2.log`·`test3.log` |
| D-6 풍향·미션 배터리 | Drone.Weather 5·Drone.Mission 7·Drone.Health.BatteryHUDPIE Success(10/05 C PC Claude) | Saved/Automation/ClaudeD6/t1.log·t4.log |
| D-5 레이싱 시작·랩 타이머 | RacingStartCountdownPIE 랩 타이머 판정 추가 Success(10/06 C PC Claude) | Claude 지시서; 이번 집중 로그 경로 미제공 |

입력 자산 행의 최신 근거는 D:\JGY\project\drone\Saved\Automation\ClaudeInterLink이며 나머지 경로 루트는 C:\URproject\drone. 새벽12/12·90/94, 코스 후속30/32·전체95개2회는 당시 기록이며 최신10/06 전체101개와 합산하지 않는다. AcroInputBehaviorPIE D구역8시나리오는 키+패드-0.5·키 해제 후 인계·전체 해제0·패드만 스로틀/피치를 확인했다. 자동 입력 주입은 실제 장치 수동 Pass가 아니다.


## 알려진 실패·실행 환경·미정

- AI-SHOTGUN-RENDER-01 해결(2026-10-04 C PC Claude). 표적 고정 시 머리4.2~4.4°(Idle·사격 애니메이션), 표적±1.9° 왕복 시 머리5.2~5.4°·SmoothedDroneLookRotation 1.45°. 9/18 몸 Hysteresis·Bone Gaze 보간(데드존 경계 0 Snap 없음)은 정상, 5~6° 대부분은 9월 하순 Rifle 계열 AnimBP 교체 뒤 애니메이션 흔들림이다. 절대 머리4° 판정(애니메이션 포함)과 미렌더 뼈 정지에 따른 NullRHI 거짓 통과가 원인. 표적 고정0.6초 기준 측정 후 시선 출력≤2.5°·애니메이션 대비 추가 머리 흔들림≤2.5°로 시험 정정(경계0↔±1.9° 튐3.8° 검출). NullRHI·렌더 Success(ClaudeInterview/shotgun3_*.log), known-test-failures에서 제외(Claude 지시서 근거). D-11 구현됨·자동 검증됨(10/05 C PC Claude): 상시 실패4개를 KnownIssues.*로 분리, 기본 Automation RunTests Drone.에서 제외. 실패 해결 아님; 경로 정본은 WORKLOG. 미렌더 패드 포커스6개는 별도 제한이다.
- **PERF-ZEN-START-01 원인 특정·재측정 대기**(10/06 D PC Claude): Zen 서버가 `CommonZenDatasessions`의 지난 실행 기록 733개 폴더(1,466파일·20MB)를 로드하는 데 약 20초가 걸리고(10/06 20.3초·10/02 22.4초), 엔진은 20초를 넘기면 "Wait for ZenServer?" 모달을 띄운다(ZenServerInterface.cpp). 10/02 473초는 그 모달을 09:30:37까지 누르지 않은 대기 시간이며 캐시·셰이더 원인 아님. 사용자 요청으로 오늘 세션 폴더 1개만 남기고 732개를 `CommonZen_sessions_backup_2026-10-06`로 이동(삭제 아님, Editor 실행 중). 다음 Editor 시작에서 Zen 대기 시간 재측정 대기. Defender 실시간 검사는 사용자 판단.
- **UI-FOCUS-RACE-01 수정 후 확인 중**: UIOnly 루트/버튼 포커스 경쟁·5프레임 복원과 이전 결과는 WORKLOG. 수신 known-test-failures에10/08 PauseMenuRacingPIE의 Resume 첫 포커스가 전체1회 Fail·단독/패드 뒤2회 Pass라는 관찰 추가. 실행PC·새 로그 경로 미명시라 현재D PC Pass로 판정하지 않음. 현재 결과/일시정지·타이틀 첫 강조 수동 대기, 안정화 완료 아님.
- **TEST-RENDER-UNPAINTED-01 원인 미특정**: 최신 전체101개에서 미렌더 실행의 알려진 패드 포커스6개 실패. LobbyLayout 진단이 기본 회귀에 없으므로 GamepadMissionFlow/GamepadNavigation/TitleFiveMenu/TitleFiveMenuWidget/TutorialComplete/TutorialNextLesson 6개 모두 화면 루트 포커스로 실패하는지로 미렌더를 판단한다(10/05 C PC Claude known-test-failures 갱신). 화면 그려진 포커스·실제 패드 확인 대기.
- **맵/메모리**: Camp 수리 후 안정성 미검증. 이번 가용12620MB<요구20480MB로 사전 검사에서 중단·엔진 미실행. 이전 패키지 진단 보호 중단/텍스처·준비 제한 유지. 모든 맵 불변·[절차](docs/gameplay/DRONE_TEST_MAP_GUIDE.md#대형-맵을-메모리-보호-상태로-검사하기).
- **외부팩**: 기존 배열/유리 수리 유지. 시점축4개 직결·옛Rig import 정리·68본/포즈 불변, LOS 경고4. 컬러66.3→10.7MiB·노멀8K Mip/스트리밍 복구. 이동/Action4·VSM/호버 포커스/NavMesh는 잔존. [상세](docs/history/DRONE_WORKLOG.md).
- 기획 미정 보존: Acro 키보드 각속도 배율/Angle 모드/마우스 Yaw·회의 반전 뜻, 입력 표시 장치 정책, 로비 탭 유지, 레이싱 연결, Production Training 테스트2건. M2 결말·M3/M4 표적 수량/규칙, 브리핑/배터리 수치·최종 아트/메시·완료 저장도 기존 미정이다.

면접 대비·참조0 정리의 구현/검증 상세는 [10월 STATUS 원문](docs/history/archive/STATUS_2026-10.md)에 보존했다. 최신 기획 미정과 수동 대기는 WORKBOARD를 따른다.

## 사용자 결정·확인 대기

결정/카드 정본은 [WORKBOARD](WORKBOARD.md). D-5·D-6·D-11·D-14와 D-12 Legacy 정리·Flight 이름 변경/분리는 위 구현·검증 상태를 따른다.

- InterLink DX 실제 콘솔·노브/Cancel 메뉴 사용 확정. 버튼3개=좌클릭/우클릭/P·자폭1=온/0=오프·노브 위/아래만으로 메뉴 이동 확정. 구현/자동 검증됨·실기 대기. 노브 회전 방향·Button1 물리 종류·브리핑 넘김/탭 전용 버튼·미인식 안내·비복귀 스로틀 처리·전시 정책/다기종 지원 현재 미정. [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md).
- 현재 미정: 높이 제한 수치·경고 연출·배터리 시간 값·D-1(M2)·D-2(M3/M4)는 기획자 내용 대기. 레이싱 지형/진행도는 팀원 미션3 완료 보고와 현재 맵을 대조해야 한다.
- 배터리 시간 값 미설정. 레이싱4코스 전체 완성 여부는 미확인이며 일괄 미구현으로 단정하지 않는다.
- 방콕 잔여987개 삭제는 원격 `1619b4f` diff에서 확인했다. 로컬 수신과 과거 LFS 객체/요금은 별도이며 D-13 나머지 유지 결정은 종료(정본 WORKBOARD).
- 기타 기존 기획 미정·수동 대기는 위 기능별 행과 WORKBOARD 참조·applications는 수정하지 않는다.

## 다음 확인

1. InterLink DX의 비행 축·Dead Zone·Mode 2 호버/피치·쉬운 조작 비복귀 스로틀 체감, Button1 무장/해제 체감·Button12/13, 노브만으로 타이틀→로비→탭→미션→브리핑→기체 선택→출격→결과 이동·첫 강조, 설정 슬라이더 잠금/조절·콤보·노브 방향/확인/Cancel을 확인한다. Acro Mode1에서 스틱에 엄지를 걸친 채 Space→상승, 키 떼고 스틱→패드 조종·모두 놓으면0을 확인하고 Mode2도 비교한다. 코스 급커브 표시선·끝 연결과 Editor 편집 체감도 확인한다. 키보드 짧게 톡(0.1초, FPV 약65°) 후 자세 유지. W+Space와 Space 단독 구분, Scout/Drop Acro 비행도 실제 장치로 확인. 결과·타이틀 첫 버튼 강조를 반복 관찰.
2. 추가 자동 회귀 판정 전 화면이 그려졌는지 확인하고 포커스 경쟁·미렌더 실행을 따로 기록. UI-LAYOUT-DIAG-01·AI-PERCEPTION-TEST-01 기존 관찰 유지, AI-SHOTGUN-RENDER-01 해결. Route는 재발 시 순서 조사.
3. 사용자/팀원은 레이싱 변경 맵/4코스 진행도·PlayerStart 연결을 대조하고 배터리 시간과 Acro 미정 조작 방식을 결정. 카운트다운·랩 타이머·FPV 곡예/UGV 분리 전 동일 체감·풍향 HUD 수동 확인·시간 결정 뒤 배터리 추락 확인. 1280/1920·실제 패드·8수업 연속 진행·Best Lap 재실행·설정/배터리/브리핑·추락 재출격 수동 확인 후 Story 콘텐츠를 고도화.
4. D PC: Island Gate 크기/방향·세 상태색과 시드194849 도시/비 외형을 실기로 확인한다. Build·RHI21개/화면 검증은 끝났지만 완주/기록·Patriot는 대기다. Observer·Pretendard·벽/그물/재밍 체감과 팀원 Source+BP/Build 후 동일 Gate 저장 재시험도 별도다. Story 제품 시작/목표 연결은 미완료, MilitaryBase M_Target은 역할 확인 전 보존한다. 과거Main78/20과 Island112/352는 별개. Zen 비교는 PERF-ZEN-START-01.

세부 카드와 완료 조건은 [WORKBOARD](WORKBOARD.md), 입력 조정은 [Blueprint 가이드](docs/reference/DRONE_CODE_STRUCTURE_AND_USER_TASKS.md), 수동 순서는 [테스트 가이드](docs/gameplay/DRONE_TEST_MAP_GUIDE.md)를 따른다. Commit/Push·Trello/Figma 수정·공유 권한·예약 자동화는 수행하지 않는다.

## 이전 기록 보존

10/01 이전 구현·검증·당시 미확인/경계 집계 네 절은 [2026-09 원문 아카이브](docs/history/archive/STATUS_2026-09.md)로 이동했다. 10/01~10/03 세션 전문과 기존 한눈에 보기·Git 요약은 [WORKLOG의 2026-10-04 STATUS 정리 절](docs/history/DRONE_WORKLOG.md)에 원문 그대로 보존했다. 과거 PC/날짜·Codex/Claude 표기를 바꾸지 않았으며 최신 상태를 과거 기록에 소급하지 않는다.
