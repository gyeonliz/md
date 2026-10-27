# 랜덤 도시 레이싱 결과·게이트 개선 시안

현재 적용 단계(2026-10-27 KST, D PC): 승인된 Story/Tutorial/Racing 성공·실패 공통 결과/클릭닫기 상세 modal·A 화살표 Source와 WBP를 반영했다. 종료 후 기록 참조를 수정한 Build47.00초 기준 전용4검사·Racing/M1 각1280/1920 실제 viewport4검사가 통과했다. Root가 실제 기록/구간·UI 색·M1 Lit 사진을 확인했고 상세 제목을 한 줄로 보완한1280 화면도 확인했다. 게이트 프레임 색·재질·판정 범위는 보존하며50cm 확대는 미적용이다. M1 새 사진2장과 DA 연결을 저장하고 원본/LoadingImage/맵 조명을 보존했다. 실제 손조종 완주·패키징은 별도이며 현재 InterLink Mode2 비행/플스 입력 후속 진단 중이다. 조정 정본은 [UI 가이드](../gameplay/DRONE_TITLE_LOBBY_ORBIT_GUIDE.md), 상세 실행은 [WORKLOG](../history/DRONE_WORKLOG.md)를 따른다.

아래는 최초 시안 작성 당시의 검토 내용이다. 당시 Unreal HEAD `5ed30281`의 실제 Source와 기존 랜덤 도시 캡처를 읽었으며 게임 Source·자산 수정/Build/PIE 없이 HTML/PNG를 작성했다. 최초 시안·후속 v4 파일은 보존한다.

## 시안 파일

후속 요청: 미션/훈련/레이싱의 성공·실패 화면을 같은 결과창 틀로 통일하고, ‘기록 상세 보기’는 별도 modal로 열며 팝업 안팎 아무 곳 클릭/Esc/Cancel로 닫는다. 닫는 입력은 뒤 버튼으로 전파하지 않으며 포커스를 복귀한다. 결과/상세 UI 모두 WBP에서 편집 가능하게 한다. [공통 결과·상세 modal 시안](C:/Users/Metacon_41/Documents/ChatGPT/드론/artifacts/20261027-racing/result-details.html)과 [팝업 확대 PNG](C:/Users/Metacon_41/Documents/ChatGPT/드론/artifacts/20261027-racing/result-details-large.png)를 추가했다. 3종류×성공/실패6상태 및 열기·안/밖 클릭 닫기·Esc·포커스 복귀42개 DOM 상호작용 검사를 통과했다. 화면의 수치는 예시이며 실제 게임 렌더/기능 Pass와 구분한다. 새 범위 Source 구현/Build/저장/실제 확인은 진행 중이다.

- [전체 비교 PNG](C:/Users/Metacon_41/Documents/ChatGPT/드론/artifacts/20261027-racing/overview.png)
- [탭 전환 HTML](C:/Users/Metacon_41/Documents/ChatGPT/드론/artifacts/20261027-racing/proposal.html)
- [결과창](C:/Users/Metacon_41/Documents/ChatGPT/드론/artifacts/20261027-racing/result.png) / [게이트 A](C:/Users/Metacon_41/Documents/ChatGPT/드론/artifacts/20261027-racing/a.png) / [게이트 B](C:/Users/Metacon_41/Documents/ChatGPT/드론/artifacts/20261027-racing/b.png) / [판정 설명](C:/Users/Metacon_41/Documents/ChatGPT/드론/artifacts/20261027-racing/range.png)

로컬 파일이며 GitHub/Space에 이미지가 업로드된 상태는 아니다. 배경은 기존 `Saved/Automation/ProceduralCity/expert_skeleton_pass.png`, 표시는 새 HTML/SVG UI 목업이다. 시간·번호·거리·게이트 수는 예시다. 기존 캡처를 현재 엔진 실행 확인으로 재사용하지 않는다.

## 사용자 확정 범위와 UI 통일성

2026-10-27 사용자 답변: **세 항목 모두 시안 먼저, UI 통일성 중요**. 구현 착수 승인으로 해석하지 않는다. v2는 기존 `DroneTitleGuideStyle`/`DroneTitleKitAssets`와 결과창 좌측 제목·버튼열/우측 정보 카드 구조를 기준으로 다시 정리했다. 청록 `#4FD5D5`, 남색 그라데이션, 흰 글자와 우하단 사선 버튼을 맞추며 별도 둥근 민트색 채움 버튼은 제거했다. v4 사용자 결정은 게이트 프레임 원색 보존이다. 청록은 상단 화살표/번호 패널에만 사용한다. HTML은 사선 버튼 텍스처를 CSS로 근사하고 대체 글꼴을 사용한다. 실제 적용 시 기존 TitleKit 텍스처·Pretendard 자산을 재사용해야 하며 완전 동일한 자산 렌더라고 주장하지 않는다. 최초 v1 시안 파일도 로컬에 보존했다.

## 1. 결과창 간소화

기본 화면은 완료/실패 제목, 이번 기록, 동일 조건 최고, 이전 최고 대비 차이만 우선한다. 게이트 완주 수는 짧은 보조 정보로 둔다. 같은 코스 재도전 → 새 도시에서 시작 → 로비로 순서로 버튼을 구성한다. 첫 포커스는 같은 코스 재도전이다. 시드·날씨·바람·구간별 거리/속도/시간은 ‘기록 상세 보기’에 접는다.

현재 `UDroneMissionResultWidget::RefreshProgressionDisplay`가 진행 시간, `Run.SummaryText`, HUD의 구간 상세 목록을 하나의 `ResultDetailText`에 결합한다. 랜덤 도시 전용 분기가 필요하며 Story/Tutorial 결과 WBP의 기존 배치는 보존한다. 같은 시드 재도전은 현재 `RequestRetrySameSeed` 경로를 재사용한다.

최고 기록 비교 키는 기존 CourseId(시드·난도 포함) / DroneId / ControlMode를 보존한다. 신규 기록 판정은 저장 전 최고를 기준으로 해야 하며, 이번 완주를 저장한 뒤 동일 값과 비교하면 차이가 0이 되므로 주의한다. 첫 기록은 ‘첫 기록’, 실패는 ‘진행 시간’과 도달 게이트로 바꾸고 최고 갱신 문구를 숨긴다. 최고가 없을 때는 `--`로 표시한다.

## 2. 판정 범위 확대 제안

외형은 유지하고 **각 변에 월드 기준 50cm 여유**를 더한다. 아래는 제안값이며 게임에 미적용이다.

| 난이도 | 현재 설정의 안쪽 가로·세로 | 제안 판정 가로·세로 |
|---|---:|---:|
| 쉬움 | 6m | 7m |
| 보통 | 4m | 5m |
| 숙련 | 2.5m | 3.5m |

현재 `ADroneTrainingGate`의 `TriggerHalfSizeCentimeters`는 외형/Overlap 박스/평면 교차 허용영역이 공유한다. Sequence의 `IsForwardTraversal` 역시 같은 정사각형 안쪽을 검사한다. 따라서 박스만 키워서는 최종 판정이 넓어지지 않는다. 별도 여유값을 만들어 Overlap와 실제 평면 교차 검사 양쪽에 적용하고, Actor Scale을 역산해 난도별 실제 50cm가 되게 한다. Generator의 `FinishSpawning` 뒤 생성 게이트에 랜덤 도시 전용 값을 전달하는 방식으로 기존 Tutorial/팀원 Racing 3맵의 수치를 보존한다.

앞뒤 깊이 증가는 정면 허용 폭 증가와 다른 항목이므로 별도다. 정방향/순서/일회 통과 조건을 유지하고 벽·기둥·바닥의 물리 충돌은 유지한다. 시안의 점선은 설명용이고 실제 게임에는 보이지 않는다. 고속·낮은 FPS에서 Overlap 누락은 이 범위 확대와 별도 회귀 항목이다.

## 3. 다음 게이트 강조

- **A안(추천, v4)**: 게이트 프레임의 기존 색/재질을 보존하고 위쪽에 청록 #4FD5D5 이중 화살표 + 작은 번호만 추가한다. 남색 번호 패널은 결과창 버튼처럼 사선 모서리를 쓴다. 기존 배경의 흰 안내선/흰 대기 게이트와 구분한다. 중앙은 비운다.
- **B안**: 민트색 네 모서리 + 번호/거리. 화면 가림은 적지만 기존 청록 HUD·흰 안내선과 겹치면 A보다 구분이 약하다.
- 통과 즉시 현재 강조를 해제하고 Sequence의 실제 `GetCurrentGate()` 대상으로 옮긴다. 완주/리셋/재시작 때도 같은 Source를 따른다.
- 화면 밖은 테두리 방향 화살표로 안내한다. 뒤쪽 목표는 좌우 방향을 유지하고, 건물 뒤에서는 마커를 흐리게 하거나 ‘가려짐’을 표시한다. 벽을 뚫는 통과 지시처럼 보이지 않게 한다.
- 프레임·화살표를 완전히 껐다 켜는 점멸 대신 약한 밝기 변화만 제안한다. 근접 시 글자/화살표 크기를 제한해 개구부를 가리지 않는다.

## 검증 및 다음 작업

HTML은 로컬 Edge headless로 렌더했고 4개 패널, 탭 5개, 배경 이미지 로드, 가로 넘침 없음과 실제 PNG를 확인했다. 설명 도식의 SVG 위치 충돌은 수정 후 다시 렌더했다. 이것은 시안 렌더 검증이며 Unreal 기능 검증이 아니다.

게임 적용 후에는 확대 경계 안/밖·역방향·순서 건너뜀·기체 크기·난도 Scale·고속·재시작·완주/실패·첫 기록/최고 갱신·패드 첫 포커스와 1280/1920 화면을 집중 확인한다. 엔진은 실행 담당 세션 한 곳만 사용한다. 이번 시안 단계에는 엔진 실행·Build·Commit/Push를 하지 않았다.


v4 확대 비교: [결과창+A안 HTML](C:/Users/Metacon_41/Documents/ChatGPT/드론/artifacts/20261027-racing/review-pair.html), [결과창 확대](C:/Users/Metacon_41/Documents/ChatGPT/드론/artifacts/20261027-racing/result-large-v4.png), [A안 확대](C:/Users/Metacon_41/Documents/ChatGPT/드론/artifacts/20261027-racing/gate-a-large-v4.png). 두 화면을 같은 폭으로 세로 배치했고 다음 목표 표시는 청록/남색/흰 글자/사선 모서리로 통일했다. 프레임 덧그리기/색상 변경은 제거했다. 로컬 렌더에서 결과창/A안만 표시·배경 로드·가로 넘침0을 확인했다. 게임 적용은 보류한다.
