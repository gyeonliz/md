# Drone 작업 기준

이 문서는 다음 작업자가 반드시 지켜야 할 현재 경계만 보존한다. 구현 현황은 [`STATUS.md`](STATUS.md), 실행 순서는 [`WORKBOARD.md`](WORKBOARD.md)를 먼저 확인한다.

## 작업 위치

- 현재 D 드라이브 작업 PC의 Unreal 프로젝트: `D:\JGY\project\drone`
- 현재 D 드라이브 작업 PC의 문서 저장소: `D:\JGY\project\md`
- 다른 PC의 마지막 확인 경로는 Unreal `C:\URproject\drone`, 문서 `C:\Users\jkw11\Documents\Codex\2026-08-19\codex-gpt-chatgpt-codex-1-6`이다. PC마다 실제 경로를 확인하고 다른 PC의 절대 경로를 실행 명령에 그대로 복사하지 않는다.
- 새 생산 코드: `Source/Drone`
- 새 프로젝트 소유 자산: `/Game/Drone`

## 맵 소유권

- `/Game/Drone/Maps/Lvl_DroneTraining`: 팀원이 실제 Tutorial 환경을 제작하는 Production 맵이다. 합의 전 저장·덮어쓰기·자동 재구성·분할·이동을 금지한다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneTutorialSystemsTest`: Course, Gate, 역할 기능과 HUD를 자유롭게 검증하는 경량 시험 맵이다.
- `/Game/Drone/Maps/TestMap/Lvl_NPCSmartObjectGreybox`: NPC·Smart Object·유인/무인 포탑·차량 전용 시험 맵이다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneMissionSystemsTest`: 재밍·귀환·역할 Event 배치 전용 시험 맵이다. 직접 실행은 Prototype Flow이므로 Mission 완료 판정은 후속 Test Mission 진입에서 확인한다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneShotgunSystemsTest`: 기존 AI 맵의 순찰·MG 경합을 건드리지 않고 추가 Shotgun NPC의 감지·실제 8개 산탄 Projectile·탄약을 보는 독립 시험 맵이다. 작은 탄두/Tracer 교체 지점은 `/Game/Drone/AI/Blueprints/Projectiles/BP_ShotgunPelletProjectile`이다.
- `/Game/Drone/Maps/TestMap/Lvl_DroneWeatherSystemsTest`: LightWind 지속풍·돌풍과 조작 모드별 보정 체감 전용 맵이다. 이동 Bead/화면 수치/1·2·3 모드 키는 TestMap 판독용이고, 비 시각 효과가 구현된 맵으로 표현하지 않는다.
- `test1`, `test2`: 용도를 확인하기 전 이동하거나 이름을 바꾸지 않는다.
- 자산 이동은 파일 탐색기가 아니라 Unreal AssetTools로 수행하고 Redirector·Soft Reference·하드코딩 경로를 검증한다.

## 게임 흐름

확정 흐름은 `게임 실행 → 시작 트레일러 → 로비 → 미션 선택/설명 → 시작 → 미션 트레일러 → 맵 진입 → 드론 선택 → 미션 시작/목표 UI`다.

사람 Operator 직접 조작, NPC 대화로 임무 수령, 플레이어와 Drone 간 실시간 화면 전환 기획은 폐기했다. NPC·Smart Object·전투 기능은 Mission 내부 요소로 유지한다.

2026-09-16 Figma 읽기 전용 확인 기준 Story 화면은 `골든 타임/인터셉트/베일 브레이커/엔드게임` 4개다. 실제 Mission별 수치·맵 Actor·기체 교대·영상은 아직 Asset으로 구현되지 않았다. Mission 2 차량이 미끼인지 실제 표적 탑승인지 Figma 내부 문구가 충돌하므로 코드는 양쪽 Story Fact를 지원하고 기본안은 사용자 결정 전 확정하지 않는다. Figma 원본은 수정하지 않는다. Android 개발은 현재 범위가 아니다.

## 구현 책임

- C++: 상태, 규칙, 기능, 테스트와 안정적인 공개 계약
- Blueprint/Data Asset: Mesh·Material·색·속도·거리·시간·임계값·자산 연결과 Greybox 조정
- Collision Root와 Visual Mesh는 분리한다.
- 나중에 조정할 수치는 가능하면 `EditDefaultsOnly` 또는 `EditAnywhere`와 명확한 Category로 Blueprint에 노출한다.
- ThirdPerson·Combat·Platforming·SideScrolling은 Legacy 참고용이며 신규 생산 코드와 자산에서 상속·참조하지 않는다.

## 현재 조작·역할 기준

- `Assisted Easy`는 Actor-relative 수평 이동·World Up 고도, `Manual Realistic Greybox`는 제한 자세·Local Up, `Acro Rate Realistic Greybox`는 Pitch/Roll/Yaw Body 각속도·자동 수평 복귀 없음으로 분리한다.
- FPV Data Asset은 Rate/Acro+고기동을 기본으로 쓰지만 공개 민간 FPV 참고값을 적용한 `UFloatingPawnMovement` Greybox다. 모터/PID/공기역학을 1:1 재현했다고 표현하지 않는다.
- Rate/Acro Mode 2 축은 오른쪽 Stick Pitch/Roll, 왼쪽 세로 Throttle, 왼쪽 가로 Yaw다. 키보드는 W/S Throttle, A/D Yaw, Q/E Roll이며 Body Pitch 전용 키가 아직 없으므로 Loop 체감은 Gamepad/RC Controller 기준이다. Mouse X/Y는 Rate 축이 아니라 직접 Yaw/Camera Pitch 개발 입력이다.
- 쉬운/제한 자세에서 카메라·Collision과 외형 기울기를 구분하고, Rate/Acro에서는 Root 자세가 Camera와 Local Up 추진을 함께 결정한다.
- 역할은 정찰 Scan, FPV Arm/자폭, Payload 픽업·드랍의 프로젝트 소유 기능을 사용한다.
- 현재 속도·감도·Collision·Greybox Mesh는 최종값이 아니다.

## 기상 기준

- World 기상 원본은 `UDroneWeatherProfile`과 `UDroneWeatherWorldSubsystem`, Level 연결은 `ADroneWeatherController`가 담당한다.
- Prototype Drone은 `UDroneWeatherResponseComponent`로 Snapshot 바람을 받는다. 현재 방식은 Sweep 위치 Drift Greybox이며 모터·PID·공기역학 1:1 구현이 아니다.
- 저장 Profile은 `Clear`, `LightWind`, `RainStorm_Greybox` 3종이다. 강풍 약 10.7m/s는 공개 민간 FPV 참고선이지 최종 내풍 한계가 아니다.
- 비 Gameplay 값과 최적화 계획은 준비됐지만 Niagara, 젖음 Material, Audio, 실내 감쇠는 아직 구현되지 않았다. 비가 체력·신호·Mission 판정을 자동 변경하지 않는다.
- Weather 시험 표현은 `/Game/Drone/Weather/Blueprints/BP_DroneWeatherDebugVisualizer`에서 Bead 수·범위·크기·속도 배율·Mesh와 Readout/Hotkey 사용 여부를 조정한다. Gameplay 바람 계산과 분리한다.

## AI·포탑 기준

- NPC가 점유하는 유인 포탑은 `BP_SO_MGTurret` 한 개다.
- `BP_AutoTurret_Vehicle`, `BP_AutoTurret_Emplaced`는 NPC가 잡지 않는 무인 자동포탑이다.
- 유인 MG는 `고정 Base → Yaw Body → Pitch Barrel → Muzzle` 구조이며 사수 Anchor는 Yaw Body의 자식으로 후방 위치와 회전을 따른다.
- Smart Object 동선은 번호나 Spline 고정 순서가 아니라 태그가 맞는 최근접 빈 Slot 선택이다.
- 개인화기 NPC의 몸 회전과 Bone Gaze는 정면 기본 3° 안에서 Yaw를 보정하지 않는다. 작은 표적 움직임을 매 프레임 쫓는 왕복 흔들림 방지값이며 Hostile Blueprint의 `NPCProfileComponent > Profile > NPC|Gaze`에서 역할별 데드존과 몸 회전속도를 조정한다.
- 실제 Shotgun은 모든 맵에서 `BP_ShotgunPelletProjectile`을 쓰며 `/Game/Drone/AI/Materials/M_ShotgunPelletGlow` 발광 비드/Tracer가 연결돼 있다. TestMap Cyan 선은 판독 보조이고 실제 Projectile을 대신하지 않는다.

## Git·LFS 기준

- 실제 Git 상태, 코드, 자산과 실행 로그를 문서보다 우선한다.
- 사용자의 변경과 팀원 맵을 임의로 되돌리거나 덮어쓰지 않는다.
- 모든 `.uasset`, `.umap`은 크기와 무관하게 Git LFS로 관리한다.
- LFS 비용 문제를 Threshold 변경으로 일반 Git에 옮기지 않는다. Core와 선택형 Asset Depot 분리를 별도로 검토한다.
- Commit과 Push는 별도 지시가 없으면 사용자가 수행한다.

## 문서 갱신 규칙

- 현재 사실: `STATUS.md`
- 현재와 다음 작업: `WORKBOARD.md`
- 변경 금지 경계: `CONTEXT.md`
- 날짜별 기록: `docs/history/DRONE_WORKLOG.md`
- 상세 주제 문서: `docs/README.md`에서 찾아간다.
- 과거 상세 원문은 `docs/history/snapshots`에 보존하며 현재 기준으로 사용하지 않는다.
