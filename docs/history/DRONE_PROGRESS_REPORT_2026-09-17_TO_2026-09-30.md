# Drone 프로젝트 진행 보고

보고 기간: 2026-09-17 ~ 2026-09-30  
작성 기준일: 2026-09-30 (Asia/Seoul)  
용도: 디자인 담당 교수님·팀원 진행 공유

## 1. 현재 상태 요약

9월 17일 이후에는 기존 기능을 넓히는 것보다 **실제 플레이에서 불안정하게 보이던 부분을 안정화하고, 기능별 독립 시험 환경을 만드는 작업**을 우선했다.

적 NPC의 추적·회전·사격 안정화, Drone 조작 모드와 역할 확장, 차량 Spline 주행, 바람·비·실내 감쇠, Tutorial 8개 시험 흐름, Story Mission 4개 시험 맵, 벽·그물 물리 반응과 Gate 편집 기능까지 구현했다. 현재 결과물은 각 시스템을 독립적으로 시험할 수 있는 Greybox 단계이며, 최종 Mission 구성과 화면 연출은 이후 전면 재정리할 예정이다.

현재 Production Tutorial 맵은 팀원이 제작 중이므로 직접 덮어쓰지 않고, 새 기능은 모두 `/Game/Drone/Maps/TestMap` 아래의 독립 시험 맵에서 먼저 검증하고 있다.

## 2. 기간 중 주요 작업

### 2.1 적 NPC·Smart Object 안정화

- Rifle과 Shotgun 병사가 표적을 발견한 뒤 제자리에서 회전하거나 뒤로 걷고, 짧은 거리에서 이동과 정지를 반복하던 문제를 수정했다.
- 개인화기 상태를 `사격 / 추적 / 포기`로 분리하고, 실제 무기 사거리 안에서는 정지 후 사격하며 사거리 밖일 때만 추적하도록 정리했다.
- 표적을 놓치거나 전투 범위를 벗어나면 무한 추적하지 않고 순찰로 복귀하도록 리시 거리, 무진행 제한, 재감지 대기시간을 추가했다.
- 이동 중 몸과 고개가 서로 반대 방향을 보는 문제를 줄이고, 실제 이동 방향과 시선 방향이 자연스럽게 맞도록 정리했다.
- Shotgun의 추가 Gun Component와 Projectile이 다른 NPC의 이동을 막던 충돌 문제를 제거했다.
- 최초 발견 직후 바로 발사하지 않고 기본 1초 조준 뒤 첫 사격이 시작되도록 했다.
- 야외 맵용 AI Controller를 분리해 감지 60m, 놓침 70m, 순찰 검색 80m 등의 값을 Blueprint에서 조정할 수 있게 했다.

결과적으로 AI 상태 전환과 보행은 이전보다 안정됐으며, Rifle·Shotgun·MG 점유·순찰 복귀 흐름을 독립 시험 맵에서 반복 검증할 수 있는 상태다.

### 2.2 Drone 조작·역할 확장

- FPV 조작을 RC 송신기 기준 Mode 1과 Mode 2로 분리했다. 두 모드는 Pitch와 Throttle의 세로축 배치만 다르고 같은 비행 성능을 사용한다.
- 키보드는 `W/S Pitch`, `A/D Roll`, `Q/E Yaw`, `Space/Left Ctrl Throttle`로 축 역할이 겹치지 않게 정리했다.
- 느림·보통·빠름 선택은 제거하고, 기체별 빠른 무적재 성능을 기본값으로 사용하는 방향으로 바꿨다.
- 기체 질량, 합산 최대 추력, 모터 반응, 중력, 항력과 Payload 질량을 반영하는 게임용 비행 물리 Greybox를 추가했다.
- Drop Drone은 화물을 들면 속도·가속·선회·호버 여유가 줄고, 투하하면 무적재 성능으로 복구된다.
- 기존 Scout·FPV·Drop에 Fiber Optic Drone과 Ground UGV를 추가해 총 5종의 역할 기체를 선택·시험할 수 있게 했다.
- Fiber Optic Drone에는 재밍 면역, 충돌 자폭, 이동 경로를 따라 지면에 남는 처짐 Cable Spline 기반을 추가했다. 9월 30일 공급 GSU가 전체 기체가 아닌 광섬유 통임을 확인해 전용 슬롯에 Material과 함께 하부 장착하고, 기체 외형은 DroneSpy Body·분리 Rotor 4개로 교체했다.
- Ground UGV는 W/S 전후 이동, A/D 조향, Q/E 제자리 회전과 4점 지면 추적으로 높이·Pitch·Roll을 지형에 맞춘다.

현재 물리는 실제 조작 특성을 반영한 게임용 Greybox이며, 모터별 RPM이나 공기역학을 완전히 재현하는 공학 시뮬레이터 단계는 아니다.

### 2.3 차량·기상 시스템

- 차량이 지정된 Spline을 따라 이동하면서 XY/Yaw는 경로를, Z/Pitch/Roll은 4점 지면 추적을 따르도록 구성했다.
- 바람은 동·서·남·북과 대각선 8방향, 무풍을 포함해 방향과 세기가 일정 시간 간격으로 자연스럽게 변하도록 했다.
- HUD에는 `풍향 NE | 풍속 5.2 m/s` 형식으로 표시할 수 있게 했다.
- 배치형 Weather Manager를 추가해 맵 단위로 바람과 비를 켜고 끄며 최소·최대 변경 시간과 풍속 범위를 Blueprint에서 조정할 수 있다.
- RainStorm 표현, 카메라 주변 빗줄기 재사용, 실내 진입 시 비 감쇠, 지붕·지면 관통 방지 기반을 구현했다.
- OilRig의 비 Mask Texture를 참고해 긴 Debug 선 대신 짧고 옅은 Plane 형태의 임시 비 표현으로 교체했다.

Random Weather와 차량 Spline Route의 기본 화면 확인은 완료했으며, 최종 Niagara 비·젖음 재질·Audio·성능 단계는 후속이다.

### 2.4 Tutorial·Course·Gate

- Figma를 읽기 전용으로 다시 확인해 Tutorial을 `호버링 → 전진 → 회전 → Gate 자유비행 → 자폭 → 드랍 → UGV 적 NPC → 고정형 포탑`의 8개 수업으로 정리했다.
- 8개 수업을 각각 독립 Mission으로 시험할 수 있는 공용 Tutorial TestMap을 구성했다.
- 호버링은 지정 구역에서 자세를 3초 유지한 뒤 다음 목표로 넘어가는 실제 PIE 시험을 추가했다.
- Training Route 전용 TestMap에 서로 다른 Course 4개를 만들고, Play 중 `1~4`로 지정 Route, `5`로 무작위 Route를 활성화하도록 했다.
- Course Spline을 따라 Gate를 자동 생성하면서 Spline 점과 Gate별 위치·회전·크기를 독립적으로 조정할 수 있게 했다.
- Gate 통과 전·현재 목표·통과 후의 색과 Material을 각각 지정할 수 있고, 완성형 Gate Mesh와 Material Slot을 교체할 수 있게 했다.
- Gate 중심은 Spline의 정확한 중앙이 아니라 통과 영역 하단에서 전체 높이의 1/6 지점을 기준선으로 사용하도록 조정했다.
- 정상 순서·정방향으로 통과했을 때만 음성 또는 Sound를 한 번 출력하는 Blueprint 슬롯을 추가했다.
- 속도·고도·구간 시간·구간 평균속도·전체 평균과 Best 비교 기반은 마련돼 있다.

현재 남은 Tutorial 핵심은 Best Lap 영구 저장, 단계별 브리핑·클리어 타임 UI, 8개 연속 진행과 전체 완료 화면이다.

### 2.5 Mission·FrontEnd

- 기간 전부터 정리해 둔 기본 흐름은 `게임 실행 → 시작 트레일러 → 로비 → Mission 선택/설명 → 시작 → Mission 트레일러 → 맵 진입 → Drone 선택 → Mission 시작/목표 UI`다.
- 사람 Player Character를 직접 조작하거나 NPC 대화로 임무를 받는 초기 기획은 제외했다.
- 기존 공통 Mission Manager, GameMode, PlayerController, 목표·실패·귀환 Trigger와 파괴 표적 기반을 재사용했다.
- 이번 기간에는 Figma의 Story 구조에 맞춰 다음 4개 독립 시험 맵으로 검증 범위를 확장했다.

| Mission | 현재 시험 내용 |
|---|---|
| Golden Time | Drop Drone 전달과 귀환 |
| Intercept | Spline 차량 핵심 표적 파괴와 목적지 도착 실패 |
| Veil Breaker | 광섬유 Drone의 재밍 구역 이탈과 귀환 |
| Endgame | Ground UGV로 지휘 표적 3개 파괴 후 귀환 |

이 4개는 Mission 규칙을 검증하기 위한 간이 시험본이다. 최종 목표 구성, 진행 방식, 실패 조건, 영상·대사·UI는 전체적으로 다시 설계할 필요가 있으며 이번 기간의 완료 항목으로 보지 않는다.

### 2.6 벽·그물·파괴 물리 시험

- 별도 Physics Sandbox를 만들고 일반 벽 반발, Rotor/Wing 접촉, 그물 얽힘, 부분 파괴 벽을 분리해 시험할 수 있게 했다.
- Drone이 벽에 천천히 닿으면 작게 밀리고, 빠르게 충돌하면 더 크게 반발하도록 속도 비례 반응을 적용했다.
- 벽 접촉마다 위치와 자세가 순간적으로 반복 변경되던 반응을 보간하고, 같은 벽을 계속 누르는 동안 새 충격이 반복 재생되지 않게 했다.
- 그물은 단순 파괴물이 아니라 날개가 걸려 감속·조종 저하·하강·포획을 만드는 장애물로 설계했다.
- 그물 접촉 때 총알 피격처럼 카메라가 흔들리던 경로를 제거하고, Camera는 안정화하되 총알에 맞았을 때의 기존 피격 화면 흔들림은 유지했다.
- Dataflow·Chaos Cloth·Geometry Collection Plugin은 활성화했지만, 현재 그물과 벽은 비교용 Runtime Greybox다. 실제 Cloth 변형과 Geometry Collection 파괴 자산은 아직 후속 작업이다.

## 3. 현재 시험 가능한 맵

| 맵 | 확인 가능한 내용 |
|---|---|
| `Lvl_DroneTutorialMissionTest` | Tutorial 8개 수업의 독립 Mission 흐름 |
| `Lvl_DroneTutorialSystemsTest` | Gate, Course, Lap, 역할 기능, HUD |
| `Lvl_DroneTrainingRouteSelectionTest` | Course 4개와 `1~4` 지정·`5` 무작위 Route |
| `Lvl_NPCSmartObjectGreybox` | Rifle·Shotgun 순찰/추적, Smart Object, 유인·무인 포탑, 차량 |
| `Lvl_DroneShotgunSystemsTest` | Shotgun 감지, 조준 대기, 실제 산탄 Projectile |
| `Lvl_DroneWeatherSystemsTest` | 풍향·풍속, 지속풍·돌풍, 비·실내 감쇠 |
| `Lvl_DronePhysicsSandbox` | 벽 반발, Wing/Rotor 접촉, 그물 포획, 부분 파괴 벽 |
| Story TestMap 4개 | Mission별 목표·실패·귀환 규칙의 간이 검증 |

Production `/Game/Drone/Maps/Lvl_DroneTraining`은 팀원이 실제 Tutorial 환경을 제작 중이므로 위 시험을 위해 저장하거나 자동 재구성하지 않는다.

## 4. 검증 현황

- 주요 변경마다 `DroneEditor Win64 Development` 빌드를 통과시켰다.
- AI, Prototype, Weather, Tutorial, Flow, Mission, Physics의 기능별 자동화와 실제 PIE 검사를 추가해 수정 전 실패와 수정 후 성공을 구분했다.
- 2026-09-30 최신 벽·그물 카메라 교정은 Physics 4개, Prototype 8개, Story 저장 계약 1개 등 총 13개 검사가 오류·경고 없이 통과했다.
- Gate 편집 기능은 관련 자동화 8개와 실제 Gate/Course Blueprint Compile 오류 0·경고 0을 확인했다.
- TestMap은 기능별로 분리하고 Production Training 맵을 자동 저장하지 않는 규칙을 유지했다.
- 자동화는 기능 계약을 확인하지만 최종 조작감·화면 구성·음향·맵 동선은 수동 플레이 확인이 필요하다.

## 5. 현재 남은 문제

- Mission 4개는 시험용 목표 조합이라 최종 플레이 구조로 보기 어렵다. Mission 전체 목표·실패·연출·UI를 이후 다시 설계해야 한다.
- Tutorial 단계별 브리핑, 클리어 타임, `n/8` 진행도, 전체 완료 화면과 Best Lap 영구 저장이 남아 있다.
- Story Trailer, 최종 Lobby/Mission/Drone 선택 WBP, Thumbnail과 실제 영상·음성 자산은 미완성이다.
- 실제 Chaos Cloth 그물, Geometry Collection 파괴 벽, 그물 탈출·Crash·Mission 실패 연동이 남아 있다.
- 비 표현은 임시 Plane 기반이며 최종 Niagara·Wetness·Splash·Audio·품질별 성능 검증이 필요하다.
- 기체별 실제 질량·추력·속도 자료가 정해지면 Flight Profile 수치를 다시 교정해야 한다.

## 6. 다음 진행 계획

1. 현재 구현된 벽·그물 카메라 안정화, Gate 위치·크기·Material·Sound를 화면에서 최종 확인한다.
2. Tutorial Best Lap을 `Course + Drone + Control Mode` 기준으로 저장하고 재실행 뒤 복원되게 한다.
3. Tutorial 단계별 브리핑·클리어 UI와 8개 연속 진행·전체 완료 화면을 구현한다.
4. 현재 Story TestMap 4개를 참고 자료로 남기고, Mission 전체 설계를 목표·진행·실패·연출·UI 기준으로 다시 작성한다.
5. 확정된 새 Mission 설계에 맞춰 Story 1부터 Vertical Slice를 다시 구성한다.
6. 병행 작업으로 실제 Chaos Cloth 그물과 Geometry Collection 벽을 현재 Greybox와 비교한다.

Mission 전면 개편은 현재 기능을 즉시 삭제하는 방식이 아니라, 먼저 새 설계와 완료 조건을 확정한 뒤 TestMap에서 교체 검증하는 순서로 진행한다.

## 7. 공유용 짧은 설명

> 9월 17일 이후에는 실제 플레이에서 불안정했던 적 AI와 Drone 조작을 안정화하고, 차량·기상·Tutorial·Mission·물리 기능을 각각 독립적으로 검증할 수 있는 시험 환경을 만드는 데 집중했습니다. 적 NPC의 회전과 추적 문제를 수정했고, Drone 5종과 RC Mode 1·2, 차량 Spline 이동, 랜덤 바람과 실내 강우 감쇠를 구현했습니다. Tutorial은 8개 수업과 4개 Route 시험 구조, 편집 가능한 Gate와 기록 기반까지 확장했습니다. Story는 4개 Mission별 간이 시험 맵을 만들었지만 최종 Mission 구성은 아니며, 목표·UI·연출을 포함해 추후 전면 재설계할 예정입니다. 최근에는 벽과 그물 충돌을 부드럽게 만들고 접촉 시 카메라 떨림만 분리하면서 총알 피격 화면 효과는 유지했습니다. 다음 단계는 Tutorial 기록·진행 UI를 완성한 뒤 새 Mission 설계를 기준으로 Story Vertical Slice를 다시 구성하는 것입니다.

## 8. Git 기준

- 보고서 작성 시 Unreal 원격 기준: `main = origin/main = 494dde2`
- 문서 원격 기준: `main = origin/main = 44662f9`
- 2026-09-30의 비행 물리·Gate·벽/그물 카메라 교정과 문서 갱신은 로컬 미커밋 상태다.
- Commit과 Push는 사용자가 수행한다.

