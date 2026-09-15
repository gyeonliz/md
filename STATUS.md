# 현재 작업 상태

기준일: 2026-09-15 (Asia/Seoul)

## 한눈에 보기

- 현재 단계: 팀원 Training 맵과 분리한 경량 TestMap의 수동 Vertical Slice 확인
- 바로 다음 개발: Mission 목표 Rule 데이터화와 정찰·투하·파괴·귀환 Event 연결
- Unreal Editor: 마지막 확인 시 종료 상태
- Production Training: 팀원이 실제 Tutorial 환경을 제작 중이므로 열람 외 저장·덮어쓰기·자동 재구성 금지

## Git 기준

| 저장소 | 현재 기준 | 상태 |
|---|---|---|
| Unreal `D:\JGY\project\drone` | `main = origin/main = 8b9b2a8` | Clean, Stash 없음 |
| 문서 `D:\JGY\project\md` | `main = origin/main = 27f694e` 위 문서 정리 중 | 주제별 이동과 요약 문서가 로컬 변경으로 남음 |

오늘 Push 이후 GitHub Desktop 자동 Stash 두 개를 대조 후 삭제했다. 현재 코드·맵·Commit은 변경하지 않았다.

## 최신 완료 항목

- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest` 경량 시험 맵 생성
- 곡선 Course, CourseSpline과 분리된 Ring Handle 5개, Gate/Sequence 5개 구성
- Recon·Impact·Payload 역할 표적 각 1개와 Carryable 1개 배치
- Gate의 임시 16각 Cube Ring을 Box Trigger 안쪽과 맞는 4변 발광 Frame으로 교체
- Gate `통과 전 / 현재 목표 / 통과 후` 3상태 색상 계약 유지
- 깨지는 역할 표적·Carryable World Text를 기본 숨김 처리하고 선택 표시 문구를 짧게 정리
- 유인 MG 사수 사망 뒤 재할당 재시도, 이동 정체 감시, 재경로와 Greybox 도착 Snap 보강
- Smart Object 동선·배치 팀 가이드, LFS 용량 계획, 외부 도구 검토와 추천도서 학습 계획 작성

## 검증된 근거

- MSVC 14.51.36257 `DroneEditor Win64 Development` Build 성공
- TestMap Map Check `0 errors / 0 warnings`
- `Drone.Tutorial.TrainingGateSequence` 1/1 성공
- `Drone.Tutorial.TutorialSystemsTestMap` 1/1 성공
- `Drone.AI.NPCPerceptionSearchPIE` 단독 새 PIE 3회 성공
- Unreal·문서 `git diff --check`, Unreal `git lfs fsck` 통과

## 아직 확인하지 않은 항목

- TestMap Gate Frame 외형과 Trigger 정합, 3상태 색
- Ring Handle 개별 이동과 Spline 투영 체감
- 한 Lap HUD 갱신과 두 Lap 이전 평균·Best·증감값
- 역할 표적 3종, Carryable 픽업·드랍과 숨긴 World Text
- AI 시험 맵의 MG 재점유·도착 방향·Gaze·자동포탑·차량 화면 확인
- Drone Rotor 축·방향·속도, 비행 기울기, 실제 탄환 피격 흔들림 등 기존 수동 회귀

## 알려진 실패와 경계

- `TrainingAssets`, `TrainingPIESmoke` 실패는 팀원이 제작 중인 실제 Training 맵의 Gate/Sequence와 역할 Actor 중간 상태를 보여준다. Codex가 원본 맵을 수정해 억지로 통과시키지 않는다.
- `NPCBaseRoutinesPIE`는 느린 Headless 묶음에서 두 번째 순찰을 제한 시간 안에 끝내지 못하는 간헐성이 있다. MG 재점유 결함과 분리해 추적한다.
- 유인 NPC 점유 포탑은 `BP_SO_MGTurret` 한 개다. `BP_AutoTurret_Vehicle`, `BP_AutoTurret_Emplaced`는 무인 자동포탑이다.
- 모든 `.uasset`, `.umap`은 크기와 무관하게 Git LFS 대상이다. Threshold 방식으로 일반 Git에 옮기지 않는다.

다음 행동과 완료 조건은 [`WORKBOARD.md`](WORKBOARD.md), 상세 문서 위치는 [`docs/README.md`](docs/README.md), 과거 근거는 [`docs/history/DRONE_WORKLOG.md`](docs/history/DRONE_WORKLOG.md)를 따른다.
