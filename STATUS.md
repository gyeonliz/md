# 현재 작업 상태

기준일: 2026-10-16 저녁 KST D PC. Unreal HEAD·origin/main·실제 원격 main은 833c1c5f, main 0/0·Clean 확인. 팀원 52594d0f·62f77024 수신 후 맵은 팀원, 그 외 중복은 로컬 우선으로 통합하고 d0c24f90(126파일)·833c1c5f(동시 로컬 테스트 수정)를 Commit/Push했다. MD HEAD95beefa·기존 미커밋3개 보존. 구현·실행 Claude(일부 하위 에이전트), 교차 리뷰 Codex 2회, 이번 Git·문서 Codex. 통합 후 Build·PIE·전체 회귀는 미실행.

## Git 기준

| 저장소 | 현재 기준 | 상태 |
|---|---|---|
| Unreal 원격 gyeonliz/drone | 실제 main·origin/main 833c1c5f | 팀원2커밋 수신·로컬2커밋 Push, LFS46개/7.8MB 업로드 확인 |
| Unreal D PC D:\JGY\project\drone | HEAD 833c1c5f | main 0/0·Clean·충돌0. 맵4개 팀원본·중복 PayloadTarget BP 로컬본 보존, 수신 자산 SHA 확인 |
| 문서 원격 `gyeonliz/md` | origin/main `95beefa`(10/14·1014) | STATUS/WORKBOARD/WORKLOG 커밋·푸시 확인 |
| 문서 D PC D:\JGY\project\md | HEAD 95beefa = origin/main | 오전·오후 문서 미커밋 3개 보존·저녁 추가 |

이전 Gate/Rain/City 검증·팀원 수신은 [WORKLOG](docs/history/DRONE_WORKLOG.md)에 보존한다. 오후 UI 검증은 아래 범위이며 수신 맵 전체·패키징·실제 패드 Pass로 확대하지 않는다.

## UI·WBP·UGV 현재 상태

- **구현됨(10/16 D PC Claude)**: WBP 15개를 /Game/Drone/UI/WBP/{FrontEnd,Mission,HUD}로 정리하고 이동 참조 3건 복구. FrontEnd 6·Mission 7·HUD 2(구 FlightHUD 프로토타입/입력 표시). 저녁에 `WBP_DroneFlightHUDKit`(242위젯) 생성·Mission PC 연결 완료. 화면 UI·HUD는 WBP 편집 가능(로비 카드 버튼 개별 위젯·런타임 로비 좌표 예외). `HudKit*` 이름 바인딩으로 Designer 위치/글꼴/색 유지·값/상태색만 코드 갱신.
- 로비 3분류를 MISSION BRIEFING 형식·Select_UI 배경으로 통일, 카드는 선택만·START로 확정. 브리핑은 시안8의 사진/정보3칸·CONTROLS 3탭(패드/키보드·마우스/조종기, LB/RB). 기체 선택은 시안6·이미지4종·조작 모드·SELECTED·고정 높이 상세/능력치. 시작 버튼 START·받은 화살표로 통일.
- 기본 훈련 출격 직후 일시정지·이름/목표/진행/역할 조작/전체 목표·[시작](A/Enter) 안내 구현. 레이싱·스토리는 BP 옵션. HUD Kit은 미션/진행·부드러운 나침반·타이머·기체 상태·속도·고도/VS·UGV 전용 조준/무장, Paint 공간 좌표로 창 위치 오프셋 수정·나침반/고도 매 프레임 갱신. 나침반 시안3·고도 시안2·UGV 조준선 시안 반영, UGV ONLY·속도 세로 눈금 제거. 첫 LOS 수업은 판정 구역과 같은 출발/전방 3D 테두리 상자2개로 변경.
- UGV 기관총 유지 연사·200발/2초 재장전(빈 탄창 자동·R/□ 수동), 유탄6발(연사/재장전 없음). UGV 전용 L2/R2 무장 IMC·Space/Ctrl 포탑 상하 조준(60°/초·BP 조정). 체크 값은 바뀌지만 검정 전경 때문에 그림이 같던 원인을 흰색 고정·Settings WBP 재생성으로 수정, 콤보 복구, 드랍 목표 SM_Pallet·메시 크기 자동 LandingCollision. 그레이박스/시험 표기 제거·역할 설명·기획 문구 반영, 레이싱 이름 스카이드론(외형 미연결).
- **자동 검증됨(저녁·Codex 로그 대조)**: DroneEditor Build 성공·HUD WBP 242위젯 생성/연결 changed=1 failed=0. RenderOffScreen UI/HUD 19건 중18 Success·FlightHUDKitLayout 1 Fail, 가이드 보고서5/5·체크박스2/2 Success. 오후 집계 차이는 WORKLOG에 보존·실행별 합산 없음. [상세/출처](docs/history/DRONE_WORKLOG.md#2026-10-16--저녁-hud-wbp화가이드-상자좌표체크박스).
- **수동 확인 대기**: 새 로비/브리핑/기체 선택/조작 안내 패드·마우스, 시작 안내, 체크박스, UGV 무장/조준, 팔레트 착지, 실제 해상도별 HUD, HUD WBP Designer 변경 반영·창 이동 후 눈금 정합·첫 수업 상자 가시성. **알려진 문제**: FlightHUDKitLayout 테스트 World 초기화 실패(2회 수정 후 중단), 미렌더 패드 포커스4건 재실행 통과는 Claude 인계이며 안정화 완료 아님.
- **현재 미정**: 드랍 집기 패드 L2(시안)/R1(실제), 비행 범례 FPV 모드2 기준 처리, 키보드 UGV 범례 번호, 스카이드론 외형, 기획 훈련8개↔UGV NPC 수업 매핑, 결과 [다음] 동작. Codex 리뷰8건 수정은 인계 기준·수동 Pass 아님.

## 한눈에 보기

첫 수업을 **고정 사람 눈높이 카메라·이륙→전진→후진→실제 착지**로 구현했다. Hover ID·8수업 연결은 유지하고 새 `TestMap/Tutorial/Lvl_Tutorial_Observer_Test`로 진입한다. 공유 시험장·Production Training은 미저장. 그물은 공유 매듭 PBD 중력/제약·접촉 변형으로 변경했고 실제 Chaos Cloth/Dataflow 제작은 후속이다. 벽 반발은 몸체/로터 외곽·이동 Sweep으로 보강했으며 안정 카메라·총알 피격 Shake·착륙/UGV 예외는 유지한다. 수동 체감 대기.

Story4개 DA 표시명은 [CONTEXT](CONTEXT.md#story-미션-표시명)에 맞췄다. Battlefield=M1·MilitaryBase=M2/3·MilitaryCamp=M4는 확정 배정이며 **Story DA 진입은 아직 기존 TestMap**이다. Battlefield 그물8개/전달1개·MilitaryBase 무인포탑1개/재밍1개를 치환했다. 원본11박스는 ArchivedMarkers에 비표시·무충돌로 보존. 숫자 레이더/타워·MilitaryBase M_Target·기존NPC는 그대로다. 레이더 Mesh 빈 슬롯·범위 BP조절, Noise→NO SIGNAL/조종 차단·광섬유 면역이며 속도는 낮추지 않는다.

UI 현재 상태는 아래 요약을 따른다. Pretendard 공통 적용·기존 아트/ID/저장키 보존 유지. [UI 가이드](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md), 상세는 [오후 WORKLOG](docs/history/DRONE_WORKLOG.md#2026-10-16--오후-ui-전면-개편wbp-전환ugv-무장).

OilRig 근거리 사본3개만 camera-local·생성축Yaw-90°로 화면 가로에 맞추고 위치 보정을 분리했다. Billboard만 돌리거나 위치Y만 옮기던 방식의 실제 도시 쏠림은 수정·렌더 검증됨. A 마스크/부드러운 폭·품질별 Niagara1개/ISM0·차폐/원본 유지, Off/Clear/Disable 즉시0과 실내 자연 소멸은 구분한다. 실기·실내 복귀/FPS는 대기. [비/BP 조정](docs/gameplay/DRONE_GAME_READINESS_RAIN_MISSIONS_GUIDE.md).

랜덤 도시 외형은 완성 건물BP를 한 동만 배치하고 명시한 닫힌 SingleMesh 모듈만 같은 방향으로 적층한다. Container01·슬롯별 MaterialOverrides fallback·도로 차선·프로젝트 소유 팔레트를 연결했다. 실제 시드194849의 도로/컨테이너/뼈대/창고4장 외형 캡처를 확인했으며 완주·재시작·기록 복원 수동 Pass는 아니다. [조정 가이드](docs/gameplay/DRONE_TEST_MAP_GUIDE.md#랜덤-도시-레이싱-외형모듈-조정).

`TUT-GATE-SAVE-01`: 로컬 Gate BP1개로 **CDO MID private 참조 저장 거부** 재현→C++/적용 도구·Gate BP 수리. 기하/색·16컴포넌트 보존·MID참조17→0, 새 프로세스 검증·위치 수정 포함 저장/재로드3회 성공. Gate5/5 Success(기존 정리 경고100). 팀원 크래시와 동일 여부/실기는 대기. Source와 BP 함께 받아 종료 후 Build, Production 미수정.

기존 수동 확인: `쉬운 조작 / 게임 조작 / FPV 모드 1 / FPV 모드 2` 한 줄 표시·폭 보정과 초기/재픽업 공통 집게 자세 구현·자동 검증됨. 수동 화면/실제 패드·화물 파지 외형은 대기. BP 조정은 Drop Pawn의 `PayloadCarryAnchor`, 화물의 `PayloadVisual`; 절차는 [역할 가이드](docs/gameplay/DRONE_TYPES_AND_CONTROL_MODES.md), 이력은 [WORKLOG](docs/history/DRONE_WORKLOG.md).

이전 수신 소스에서 확인한 후속: 시드 기반 도시/날씨/레이싱 생성·지정/무작위 시드·같은 시드 재시작, Story/Procedural 로딩·취소·미션 Esc/Start 일시정지/복귀, 완료 미션/Story Fact/권장문구 JSON 저장과 최고 랩 구간 저장이 있다. 구현 코드 존재와 현재HEAD 실행 성공은 다르다. 기능 근거/미확인은 WORKLOG·아래 표 참조.

`TUT-GATE-PRESENTATION-01`: Island의 Gate Scale `(1,2,2)`와 메시 작성Yaw90°가 UE Transform에서 다른 축으로 합쳐져 폭이 줄던 원인을 Native Visual 보상으로 수정했다. 새 읽기 전용 재로드에서 활성BP112개 좁아짐0, 숨김Native352개 보존·맵/BP/Course 바이트 불변·저장0 확인. 자동 Gate의 0 접선 방향도 유한 차분 fallback으로 교정해 직선/코너/닫힌 루프 회귀를 통과했다. m_green은 백업 후 Nanite 사용 플래그만 수리·저장했고 Final2 RHI에서 해당 경고 없음. Island 재저장·잔존 삭제는 필요 없다. Main의 당시 Native20 기록과 Island352는 별개이며 Main 현재 참조·세 상태색 실기는 대기다. [배치 가이드](docs/tutorial/DRONE_TRAINING_AUTHORING_GUIDE.md).

`AI-PATRIOT-PIVOT-01`: `/Game/Drone/AI/Blueprints/Turrets/BP_PatriotMissileLauncher` 생성·초기 회전 검사 완료 뒤 10/13 12:50 Editor 재저장(현재35,958B)이 확인됐다. 현재 저장본의 축/이음새·복합 회전은 재검증 대기다. 생성 구조는 Lower 고정→YawPivot→Middle/PitchPivot→Upper, Yaw/Z·Roll/X 조절. 기존 편집을 보존하고 생성 도구로 덮어쓰지 않는다. 원본3메시·Missile_M, AI/발사/입력/충돌·차량 배치 미포함. [MG·패트리어트 가이드](docs/ai/DRONE_MG_TURRET_3PART_GUIDE.md#6-패트리어트-미사일-포대-접합부-회전축-조정).

`UI-RESULT-LAYOUT-01` 현재 native는1920×1080 기준 TitleKit 상자 버튼·좌측 버튼열/우측 정보 카드로 변경됐다(수신 소스 확인). 옛 중앙680 카드/청록 테두리·10/06 집중6/6은 당시 기록이며 현재 외형 검증이 아니다. named WBP 부모/이름 계약과 배율1은 유지. [UI 가이드](docs/gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md)·WORKLOG 참조, 실제 화면/패드는 대기.

10/06 C PC Claude: D-5 출발부터 랩 타이머 측정·D-12 Flight 명명과 피격/Acro/지상 주행 컴포넌트 분리 구현됨·자동 검증됨. 화면·FPV/UGV 체감 수동 확인 대기. 기존 NPC/높이 제한/매니저·Legacy 정리 유지, D-13 종료. 레이싱은 아래 팀원 변경 수신 상태를 따르며 배터리 시간·높이 제한 수치/경고 연출은 현재 미정. 세션 전문은 [WORKLOG](docs/history/DRONE_WORKLOG.md).

| 영역 | 구현·자동 검증 | 수동 확인 대기·미구현·현재 미정 |
|---|---|---|
| 시작·로비 | 5메뉴·WBP 연결 유지, 현재 로비/브리핑/기체 선택은 위 UI 요약 | 실제 패드·마우스·1280/1920 대기, 미정은 위 요약 |
| 조종 입력 표시 | 설정 수동 ON/OFF·선택 저장, 저장 `WBP_DroneControlInputDisplay` 연결. 아래 중앙 스틱 표시·OFF 갱신 중지, 고도계 독립 | D-3 기본 False 확정, 장치 자동 전환/분리·재연결 정책 미정. 실제 화면/패드 확인 대기 |
| 코스 표시선 | 긴 코스만 sqrt(곡률) 밀도+15% 균일 몫, 짧은 TestMap68/113조각 기존 균일 분할 유지. MaximumCourseLineSegments 노출·기본1024(시작값·미확정), BP 드래그 재구성 Off | 팀원 Production 코스 외형·Editor 편집 체감 수동 대기. Production 맵 미저장 |
| Acro | InterLink DX Acro 4축 추가·Mode 2 실측·세로축 반전 해제(10/07 D PC Claude), [입력 계약](docs/tutorial/DRONE_PROTOTYPE_INPUT_CONTRACT.md). 비행 기체 FPV/Scout/Drop/FiberOptic 6개 입력 연결, 패드 축 4개 Dead Zone, 정확 자세 적분. 키보드·패드 입력원 분리·절댓값 큰 쪽 사용·키 해제 시 패드 인계, Space 단독 자세 불변·Mode 1/2 키보드 동일·FPS 무관 자동 검증 | 실제 패드/키보드 체감·Scout/Drop 비행 대기. 키보드 각속도 배율·Angle 모드·마우스 Yaw·회의 “좌우 스틱 반전” 뜻 미정 |
| 패드 첫 포커스 | `FDroneGamepadFocus`가 포커스 부여 후 5프레임 감시·루트/없음으로 이탈 시 복원, 다른 강조 버튼 이동은 보존 | UI-FOCUS-RACE-01 **수정 후 확인 중**. 화면 그려진 수정 전 Fail/후 Success 각 1회, 간헐적 첫 버튼 강조 수동 확인 대기 |
| 튜토리얼·Story 순서/저장 | Tutorial8·Story4 유지. Racing은 Circuit/Procedural 2항목(DA파일/소스 계약, 실행 미확인). 완료 미션·Story Fact·권장문구 표시를 `Saved/SaveGames/DroneMissionProgress.json`로 저장/복원하는 코드 확인 | 실제8수업·전체 완료·로비 확인과 성공→종료→재실행 복원 대기. 저장 실패는 실행 중만 유지 경고. 조작키 브리핑 미입력·정식 건너뛰기 정책 확인 별도 |
| Best Lap | `CourseId|DroneId|ControlMode`별 JSON. 수신 코드에 최고 랩 구간 시간 `bestLapSegments` 저장/복원·구간 대비의 저장 최고 우선 사용 추가. 평균은 실행 History | 현재HEAD 실행 미확인. 같은 조건 완주/재실행 후 Best와 구간 대비 복원 확인. 고정4코스 지형과 시드 레이싱 생성은 별개 |
| 허브·HUD | 현재 HUD Kit은 위 요약. 기존 배터리 제한/방전 추락 구현·이전 자동 검증 유지 | 실제 HUD·배터리/풍향 체감 대기. 기체 시간0·최종 시간/음원·신호 대역/분기·재출격 브리핑 미정 |
| 미션·실패 | DA 자동 등록·Definition/Rule/Trigger·체크포인트 재출격 유지. D-6 높이 제한 매니저 구현됨·자동 검증됨(10/05 C PC Claude): `/Game/Drone/Managers/BP_DroneAltitudeLimitManager` 배치·BP 값 설정으로 적용. Mission/Weather 매니저 BP도 같은 폴더로 정리됨. 상세 [WORKLOG](docs/history/DRONE_WORKLOG.md) | 높이 제한 체감·날씨 시험 맵 수동 확인 대기, 높이 제한 수치·경고 연출 현재 미정. 체크포인트 미배치·첫 출격 위치 재출격. 추락 체감·새 DA 등록 및 Story M1~4 콘텐츠/분기 고도화 확인 |
| 레이싱 | Circuit와 Procedural 2항목 유지. 완성BP1체/모듈 적층·슬롯별 재질·차선·소유 팔레트, 실제 도시 비 화면 분포 수정/검증됨 | 지정/무작위·같은 시드·로딩 취소·완주·결과/기록 실기 대기. 팀원 고정4코스와 별개 |
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
- **레이싱 팀원 변경 수신·연결 미검증**: `a57a4444` 커밋 설명은 “레이싱콘텐츠 미션3까지 완료”이며 Training·Island·MountainRange·Demonstration 맵과 Anim 변경을 수신했다. 보고 수신과 실제 완주 검증은 다르다. 이전 코스1개/PlayerStart 없음 조사는 당시 기록이며 현재 배치로 재사용하지 않는다. 공용 Gate BP의 아이템 참조는 연결됐고 제품 DA 변경은 이번 diff에 없다. 실제 진입 맵·4코스 전체 진행도·시작점/완주/기록은 팀원 확인과 실행 검증 대기다.
- 기획 미정 보존: Acro 키보드 각속도 배율/Angle 모드/마우스 Yaw·회의 반전 뜻, 입력 표시 장치 정책, 로비 탭 유지, 레이싱 연결, Production Training 테스트2건. M2 결말·M3/M4 표적 수량/규칙, 브리핑/배터리 수치·최종 아트/메시·완료 저장도 기존 미정이다.

## 면접 대비·참조 0 정리 — Claude, 현재 C PC

- NPC Controller HostileStateTree/FriendlyStateTree(EditDefaultsOnly Soft 참조, 기본 기존 ST2개)·BP 변경 가능·로드 실패 에러 로그. StateTreeCookContract 통과, 패키징 미실행.
- Moderate HUD는 신호 불안정(영상 Noise 미연결), Scout 프리셋 전환/FPV27m/s/Drop 안정 기본 광고 문구 삭제. VeilBreaker 목표는 광섬유 드론으로(끊김 규칙 미정). PlayerFacingTextContract 통과.
- Rifle/MG 디버그 선 기본 Off, 상수 TestTrue4건을 실제 조건으로 교체, 기체6개 이상 [DRONE-SELECT] 경고(동적 목록 후속). FrontEndContract·FlightProfiles·StateTreeCookContract·PlayerFacingTextContract Success, AI/UI NullRHI22개 중20 Success·당시 NPCPerception/Shotgun2Fail(후속 Shotgun 해결).
- 참조0 검증된 프리셋 튜닝·미사용 API/include/Build.cs 주석 정리, HoverThrottleNormalized는 도구3개 호환 유지·런타임 미사용. Tools/AssetMigration 낡은 도구12개 삭제됨(Git 이력), 게이트 도구 기본검증·APPLY=1일 때만 저장, 타이틀 임포트 경로 명시 필수. md tools 변경은 Claude 기존 수정이며 Codex 미수정.
- D-12 1차 Legacy 정리와 D-14 MCP 로컬 설정 전환은 구현됨·자동 검증됨(10/05 C PC Claude). MCP 공유 Default bAutoStartServer=False·필요 PC Saved 로컬 True·C PC 실행15초 뒤8000 응답 확인. CLAUDE.md MCP 설명도 D-14와 일치하도록 수정됨(10/06 Claude): 공유 끔·사용자 PC 로컬만 켬·팀원 불필요. 설정 절차는 [협업 세팅](docs/git/CLAUDE_CODEX_SETUP.md#unreal-mcp-자동-시작--pc별-로컬-설정)·삭제 상세는 WORKLOG.

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
