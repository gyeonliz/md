# 현재 작업 상태

기준일: 2026-10-22 KST D PC. 현재 요청은 기존 InterLink/패드·키보드 매핑 복구만이다. 스로틀·모터 수정은 사용자 요청으로 보류했고 Computer Use/화면조작·입력주입은 전부 중지했다. 매핑 원본은 정상내용이며 사용자가 재실행 후 입력 복구를 확인했다. 매핑/입력 추가수정은 없고 근본원인은 미확정이다. 직전 물리23/오디오 근거와 미완료 실기체교정·본미션/장치 범위를 보존한다. [근거](docs/history/DRONE_WORKLOG.md).

## Git 기준(10/22 로컬 추적 ref·Fetch 없음)

| 저장소 | 현재 기준 | 상태 |
|---|---|---|
| Unreal D PC `D:\JGY\project\drone` | HEAD=추적 origin/main `0d95972c` | main·0/0·기존 오디오/HUD와 물리후보 추가 미커밋 보존. Fetch/Pull 없음 |
| 문서 D PC `D:\JGY\project\md` | HEAD=추적 origin/main `24d57245` | main·0/0·기존 MD/오디오 보존·물리후보 문서 추가 미커밋 |
| C PC 이전 실행 기준 | `c589bbf9` 위 당시 변경 | Build14.14초·UI RHI4종·M1 출격은 이전 PC 근거 |

## 작업컴 세션 운영

현재매핑 범위는 [세션등록부](docs/git/DRONE_WORK_PC_SESSIONS.md)를 따른다. Root의추적입력파일30개 Git내용일치·Source430 버그시작이후변경0·SavedInput 매핑override없음/restorationWrites0을 대조했다. HID/USB정상·새Editor등록과 Training/FrontEnd/TUT_LOS 진입/possess는 관찰했으나 사용자가 재실행 후 입력 복구를 확인했다. 매핑/입력 추가수정0·원인미확정이다. 이번후속patch/Build/PIE검증 결과없음·CUA전부중지. 스로틀/모터는 보류다.

## 현재 D PC 구현·검증 경계

- **사용자 오디오/실제 미션**: 직전 지정26검사 성공 이력(리비전별)과 별개로 실제 catalog Racing Map1·Story M4의 Mission controller/HUD 조립에서 countdown·health warning·실제배치 발사음·파괴음2life를 자동 확인했다. 사망 뒤 재선택 pause의 tung 실결함을 local-PC 소유 공간음의 pause 예외로 수리, Build5 성공16.72초. 직접영향 기존 DroneDestroyed/ImpactDestroyed/MasterMute3개 재검사 Success·기존417중416 보존·FlightPawn audio블록/include2만 수정, Config5/보호125/SourceArt12·Saved10 일치. 전체 손조종/실청·Cook/패키징은 미실시. [정본](docs/gameplay/DRONE_MISSION_FRAMEWORK_GUIDE.md#사용자-오디오와-체력-경고).

- **물리 1차 후보·입력 한계**: 직전 Build003/Run003의 물리12+기존회귀11=23Success는 직접 Pawn API·자동화 범위다. actual console/Slate/조종기·키보드 전체입력 파이프라인을 통과했다는 뜻이 아니다. 구콘솔 -1→약21.6초뒤arm은조건거부 RED다. 스로틀·모터는보류, controlled Racer/Acro1·2/CG0의 기존힘/토크·접지기반과 synthetic계수·본미션/최종B·C 미완은유지한다. [후보/입력검증 범위](docs/gameplay/DRONE_REALISTIC_HANDLING_PLAN.md#racer-로터-1차-후보).
- **카메라·설정**: 쉬운/게임 조작 X=기체 Yaw, Y=카메라 피치의 감도/반전·적용/취소/기본값·저장 연결 구현. 최신 같은 리비전 단위3·렌더2·회귀8 Success, 새 PNG14장 중 총괄4장 직접 확인. 실제 구버전 .sav·재실행/실물 장치 Pass는 아니다. [편집·경계](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md#카메라-감도반전과-designer).
- **Story**: M3 현행 재밍 이탈 목표 자동 통과. M4 실제 Start1/2/3의 선택/ID·스포이드·XY·UGV 접지·기존3목표 자동 통과. ApplyDamage 자동 이벤트이며 실물 발사/비행 완주가 아니다. 첫 M4 실패는 낡은 일반 헬기포트 기대값으로 보존하고 검사만 수리했다. [시험 범위](docs/gameplay/DRONE_TEST_MAP_GUIDE.md#story4-선택브리핑-검증-경계).
- **LOS**: 수평 후퇴/메시 Yaw·고정 위치 카메라 추적 구현, 이륙→전진→후진→접지 자동 계약 통과. 지형 HitResult 디코더 오류와 캡처 World 일치 보장이 없어 사람/드론 가시성은 미확인이다. 눈높이 문제로 단정하거나 높이를 임의 조정하지 않았다.
- **성능**: 1280×720·품질3·출발점 무입력10초 CPU 구간 확보. M3 Fence BP 런타임 오류 잔존, CSV ensure 진단은 내장 CSV 전체 통계 비활성(-csvAllCategoriesDisabled·GPUcsv0) 조건의 CPU 표본으로 분리한다. GPU를 오류 원인으로 확정하지 않는다. M4 캡처의 Lumen 경고는 관찰이며 렉 원인/최적화 효과가 아니다. [측정 해석](docs/gameplay/DRONE_TEST_MAP_GUIDE.md#story4-선택브리핑-검증-경계).
- **보존 근거**: 직전물리1차 종료감사의 Source430/허용6+추가12·보호125/Saved10·당시엔진0은 이력이다. 이번버그 시작의 새baseline·사용자진행/변경을 보존하며 현재사용자Editor를 종료/원복하지 않았다. 매핑30개는Git내용정상·복구쓰기0, 실제입력복구 미확인. [WORKLOG](docs/history/DRONE_WORKLOG.md).

이전 10/18~20 구현 요약 원문은 [10월 아카이브](docs/history/archive/STATUS_2026-10.md)에 보존했다. C PC Story UI4종/24캡처·M1 상태와 이번 D PC 검증을 구분한다.

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

이전 10/06 C PC·10/07 D PC 검증 표는 [10월 원문 아카이브](docs/history/archive/STATUS_2026-10.md)에 보존했다. 현재 PC 재검증으로 해석하지 않는다.

## 알려진 실패·실행 환경·미정

- AI-SHOTGUN-RENDER-01 해결(2026-10-04 C PC Claude). 표적 고정 시 머리4.2~4.4°(Idle·사격 애니메이션), 표적±1.9° 왕복 시 머리5.2~5.4°·SmoothedDroneLookRotation 1.45°. 9/18 몸 Hysteresis·Bone Gaze 보간(데드존 경계 0 Snap 없음)은 정상, 5~6° 대부분은 9월 하순 Rifle 계열 AnimBP 교체 뒤 애니메이션 흔들림이다. 절대 머리4° 판정(애니메이션 포함)과 미렌더 뼈 정지에 따른 NullRHI 거짓 통과가 원인. 표적 고정0.6초 기준 측정 후 시선 출력≤2.5°·애니메이션 대비 추가 머리 흔들림≤2.5°로 시험 정정(경계0↔±1.9° 튐3.8° 검출). NullRHI·렌더 Success(ClaudeInterview/shotgun3_*.log), known-test-failures에서 제외(Claude 지시서 근거). D-11 구현됨·자동 검증됨(10/05 C PC Claude): 상시 실패4개를 KnownIssues.*로 분리, 기본 Automation RunTests Drone.에서 제외. 실패 해결 아님; 경로 정본은 WORKLOG. 미렌더 패드 포커스6개는 별도 제한이다.
- **PERF-ZEN-START-01 원인 특정·재측정 대기**(10/06 D PC Claude): Zen 서버가 `CommonZenDatasessions`의 지난 실행 기록 733개 폴더(1,466파일·20MB)를 로드하는 데 약 20초가 걸리고(10/06 20.3초·10/02 22.4초), 엔진은 20초를 넘기면 "Wait for ZenServer?" 모달을 띄운다(ZenServerInterface.cpp). 10/02 473초는 그 모달을 09:30:37까지 누르지 않은 대기 시간이며 캐시·셰이더 원인 아님. 사용자 요청으로 오늘 세션 폴더 1개만 남기고 732개를 `CommonZen_sessions_backup_2026-10-06`로 이동(삭제 아님, Editor 실행 중). 다음 Editor 시작에서 Zen 대기 시간 재측정 대기. Defender 실시간 검사는 사용자 판단.
- **UI-FOCUS-RACE-01 수정 후 확인 중**: UIOnly 루트/버튼 포커스 경쟁·5프레임 복원과 이전 결과는 WORKLOG. 수신 known-test-failures에10/08 PauseMenuRacingPIE의 Resume 첫 포커스가 전체1회 Fail·단독/패드 뒤2회 Pass라는 관찰 추가. 실행PC·새 로그 경로 미명시라 현재D PC Pass로 판정하지 않음. 현재 결과/일시정지·타이틀 첫 강조 수동 대기, 안정화 완료 아님.
- **TEST-RENDER-UNPAINTED-01 원인 미특정**: 최신 전체101개에서 미렌더 실행의 알려진 패드 포커스6개 실패. LobbyLayout 진단이 기본 회귀에 없으므로 GamepadMissionFlow/GamepadNavigation/TitleFiveMenu/TitleFiveMenuWidget/TutorialComplete/TutorialNextLesson 6개 모두 화면 루트 포커스로 실패하는지로 미렌더를 판단한다(10/05 C PC Claude known-test-failures 갱신). 화면 그려진 포커스·실제 패드 확인 대기.
- **맵/메모리**: 10/20 C PC Camp 사전 검사 당시 가용12620MB<요구20480MB로 엔진 미실행. 이후 승인된 임시 모드의 확인과 일반 화질/장시간 안정성은 구분한다. 현재 D PC 측정값이 아니다. [절차](docs/gameplay/DRONE_TEST_MAP_GUIDE.md#대형-맵을-메모리-보호-상태로-검사하기).
- **외부팩**: 기존 배열/유리 수리 유지. 시점축4개 직결·옛Rig import 정리·68본/포즈 불변, LOS 경고4. 컬러66.3→10.7MiB·노멀8K Mip/스트리밍 복구. 이동/Action4·VSM/호버 포커스/NavMesh는 잔존. [상세](docs/history/DRONE_WORKLOG.md).
- 기획 미정 보존: Acro 키보드 각속도 배율/Angle 모드/마우스 Yaw·회의 반전 뜻, 입력 표시 장치 정책, 로비 탭 유지, 레이싱 후속 규칙, Production Training 테스트2건. M2 결말·M3/M4 표적 수량/규칙, 브리핑/배터리 수치·최종 아트/메시는 미정이다. 완료 미션·Story Fact JSON 저장/복원은 구현되어 있으며 현재 HEAD 재실행·실물 입력 확인은 별도다.

면접 대비·참조0 정리의 구현/검증 상세는 [10월 STATUS 원문](docs/history/archive/STATUS_2026-10.md)에 보존했다. 최신 기획 미정과 수동 대기는 WORKBOARD를 따른다.

## 사용자 결정·확인 대기

결정/카드 정본은 [WORKBOARD](WORKBOARD.md). D-5·D-6·D-11·D-14와 D-12 Legacy 정리·Flight 이름 변경/분리는 위 구현·검증 상태를 따른다.

- InterLink DX 실제 콘솔·노브/Cancel 메뉴 사용 확정. 버튼3개=좌클릭/우클릭/P·자폭1=온/0=오프·노브 위/아래만으로 메뉴 이동 확정. 구현/자동 검증됨·실기 대기. 노브 회전 방향·Button1 물리 종류·브리핑 넘김/탭 전용 버튼·미인식 안내·비복귀 스로틀 처리·전시 정책/다기종 지원 현재 미정. [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md).
- 현재 미정: 높이 제한 수치·경고 연출·배터리 시간 값·D-1(M2)·D-2(M3/M4)는 기획자 내용 대기. 레이싱 지형/진행도는 팀원 미션3 완료 보고와 현재 맵을 대조해야 한다.
- 배터리 시간 값 미설정. 레이싱4코스 전체 완성 여부는 미확인이며 일괄 미구현으로 단정하지 않는다.
- 방콕 잔여987개 삭제는 원격 `1619b4f` diff에서 확인했다. 로컬 수신과 과거 LFS 객체/요금은 별도이며 D-13 나머지 유지 결정은 종료(정본 WORKBOARD).
- 기타 기존 기획 미정·수동 대기는 위 기능별 행과 WORKBOARD 참조·applications는 수정하지 않는다.

## 다음 확인

실행 순서는 [WORKBOARD Next](WORKBOARD.md#next), 입력 계약은 [장치 가이드](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md)를 따른다. 우선 두 실물 장치의 raw/IA/모드/Boom/ViewTarget을 함께 계측하고 LOS의 World 연결 캡처·지형 HitResult를 수리해 실제 가시성을 확인한다. M3 Fence BP 오류·M4 Lumen 경고/로딩을 구간별로 조사하며 Racer후보 저속OFF/착지/재이륙은 자동검증됐으며 경사/고속접촉·본미션/장치·최종B/C는 후속이다. 기존 전체 손 조종·패키징·팀원 맵 수동 대기는 유지한다. 이전 상세 체크리스트는 [원문 아카이브](docs/history/archive/STATUS_2026-10.md)에 보존했다.
## 이전 기록 보존

10/01 이전 구현·검증·당시 미확인/경계 집계 네 절은 [2026-09 원문 아카이브](docs/history/archive/STATUS_2026-09.md)로 이동했다. 10/01~10/03 세션 전문과 기존 한눈에 보기·Git 요약은 [WORKLOG의 2026-10-04 STATUS 정리 절](docs/history/DRONE_WORKLOG.md)에 원문 그대로 보존했다. 과거 PC/날짜·Codex/Claude 표기를 바꾸지 않았으며 최신 상태를 과거 기록에 소급하지 않는다.
