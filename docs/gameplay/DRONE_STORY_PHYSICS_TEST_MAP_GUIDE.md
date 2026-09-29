# Story·Physics TestMap 실행 가이드

기준일: 2026-09-29

Production `/Game/Drone/Maps/Lvl_DroneTraining`은 팀원이 실제 Tutorial을 제작하는 맵이다. 이 시험을 위해 열어 저장하거나 덮어쓰지 않는다. 아래 시험 자산은 모두 `/Game/Drone/Maps/TestMap`과 `/Game/Drone/Physics`에 격리했다.

## 1. Physics Sandbox

맵: `/Game/Drone/Maps/TestMap/Lvl_DronePhysicsSandbox`

이 맵만 Content Browser에서 직접 열어 Play한다. 전용 GameMode가 충돌 반응을 켠 시험 Drone 한 대를 Spawn한다.

2026-09-29 화면 피드백 수정본의 기본 크기는 그물 `6m × 3m`, 파괴 벽 약 `5.55m × 3.69m`다. 이전 생성본의 약 `13m × 12m` 그물과 약 `12.8m × 9.2m` 벽은 잘못된 시험 크기였으므로 기준으로 사용하지 않는다. 맵이 열린 채 수정됐다면 Editor를 닫았다 다시 열거나 맵을 Reload해야 저장된 축소본을 볼 수 있다.

1. 앞의 두 벽에 정면과 비스듬한 각도로 비행한다.
2. 충돌 뒤 Drone이 벽 안으로 파고들지 않고 충돌면 바깥쪽으로 짧게 밀려나는지 확인한다.
3. `PhysicsSandbox_NetRig`을 선택하고 Details의 `Drone|Physics|Net|Placement`와 `Drone|Physics|Net|Layout`에서 네 Corner, 가로·세로 줄 수, Segments, Sag Depth, Strand Thickness를 바꾼다.
4. Drone으로 그물 중심과 가장자리를 각각 `2.5m/s`보다 빠르게 충돌한다. 충돌 위치 주변 Strand만 원본 격자에서 빠지고, 끊어진 조각이 충돌 방향과 중력을 받아 떨어지며 나머지 격자는 남는지 확인한다.
5. Details의 `Local Break Radius Centimeters`, `Minimum Impact Speed`, `Break On Impact`로 절단 반경·최소 충돌 속도를 조정한다. `Spawn Detached Strand Physics`, Impulse/Random Impulse, Lifetime, 한 번에 생성할 최대 조각 수도 Blueprint에서 조정한다. 기본은 최대 16개·5초다. `Break Net Greybox`는 전체 제거 비교용이다.
6. `Reset Net Greybox`를 호출해 모든 Strand가 원래 상태로 돌아오고 떨어지던 물리 조각도 즉시 제거되는지 확인한다.
7. 더 앞쪽의 `PhysicsSandbox_BreakableWall`에 정면과 비스듬한 각도로 `2.5m/s`보다 빠르게 충돌한다. 맞은 반경의 조각만 분리되어 충격 방향으로 날아가고 나머지 벽이 유지되는지 확인한다.
8. 벽 Details의 Columns·Rows·Piece Size·Gap·Local Break Radius·Break/Random Impulse·Minimum Impact Speed·Debris Lifetime을 조정하고 `Reset Wall`로 복구한다. 기본 파편은 8초 뒤 정리된다.

전용 Drone의 충돌 응답 Component는 반발 계산 뒤 같은 `FHitResult` 위치·입사 방향을 맞은 Actor에 Point Damage로 전달한다. 따라서 자동 API 호출이 아니라 실제 Drone 충돌로도 Net/Wall의 국소 파괴 경로가 실행된다.

현재 그물과 파괴 벽은 Dataflow/Chaos의 게임 규칙·체감 비교용 Runtime Greybox다. 그물의 끊어진 Segment는 실제 Rigid Body로 떨어지지만 남은 그물 전체가 Cloth처럼 휘거나 늘어나지는 않는다. 벽도 Geometry Collection Cluster/Field가 아니라 맞은 조각을 물리 Component로 바꾼다. 네 Corner는 Details 좌표값으로 조절하며 Viewport Handle은 아직 없다. 즉 현재 결과를 “Chaos Cloth/Geometry Collection 완료”로 판정하지 않는다. 실제 Cloth 고정 정점과 Geometry Collection 파쇄는 다음 자산 Spike에서 같은 맵의 별도 구역으로 비교한다.

이 시험의 최종 설계 의도는 `그물에 닿으면 즉시 잘려 통과`가 아니다. 그물은 날개·Rotor에 엉켜 Drone의 속도와 추력을 낮추고 자세를 교란하며, 접촉 시간과 탈출 여부에 따라 포획·추락을 만드는 장애물이다. 현재 국소 절단은 Hit 위치와 파편 반응을 확인하는 진단 기능이고, 실제 걸림은 Chaos Cloth 표현과 별도 Contact Probe/Net Interaction 상태를 결합해 후속 구현한다.

벽 반발도 이 맵의 두 Cube에만 적용할 최종 기능이 아니다. 현재 전용 Physics Pawn에서 검증한 반사 계산을 일반 비행 Drone의 모든 유효 Blocking 벽·기둥·구조물 접촉으로 확장해야 한다. 바닥 착륙과 강한 Crash는 표면 법선·속도·Flight 상태로 별도 처리한다.

## 2. Story Mission 진입 공통

Story 맵을 직접 Play하면 선택된 Mission 정보가 없으므로 Spectator 상태가 될 수 있다. `/Game/Drone/Maps/Lvl_DroneFrontEnd`를 Play하고 로비에서 해당 Story Test Mission을 선택한 뒤 Drone을 골라 시작한다.

### Mission 1 — Golden Time

- 맵: `/Game/Drone/Maps/TestMap/Lvl_DroneStory01_GoldenTimeTest`
- Mission ID: `Mission.Story.GoldenTime.Test`
- 추천 Drone: Drop Drone
- 간이 흐름: Payload 전달 → 귀환
- 아직 없음: 선택 정보 수집, 화물 분실 실패, 실제 연출

### Mission 2 — Intercept

- 맵: `/Game/Drone/Maps/TestMap/Lvl_DroneStory02_InterceptTest`
- Mission ID: `Mission.Story.Intercept.Test`
- 추천 Drone: FPV
- 간이 흐름: Spline 차량 추적·파괴 → 목적지 도달 전 성공
- 아직 없음: 잔해 정보 수집, 마지막 분기, 실제 차량·폭발 연출

### Mission 3 — Veil Breaker

- 맵: `/Game/Drone/Maps/TestMap/Lvl_DroneStory03_VeilBreakerTest`
- Mission ID: `Mission.Story.VeilBreaker.Test`
- 추천 Drone: Fiber Optic Drone
- 간이 흐름: 재밍 구역 진입·이탈 → 귀환
- 아직 없음: 재머 파괴, Mission 중 Fiber Drone에서 UGV로 전환, 광섬유 실패 조건

### Mission 4 — Endgame

- 맵: `/Game/Drone/Maps/TestMap/Lvl_DroneStory04_EndgameTest`
- Mission ID: `Mission.Story.Endgame.Test`
- 추천 Drone: Ground UGV
- 간이 흐름: 지휘 목표 3개 파괴 → 귀환
- 아직 없음: 장거리 타격, 최종 환경·엔딩 연출

## 3. Tutorial Hover 재확인

1. FrontEnd에서 `Tutorial Hover`를 선택한다.
2. Scout Drone으로 시작한다.
3. 시험맵의 네 모서리 기둥으로 표시된 Hover Zone 안으로 들어간다.
4. 이동 입력을 놓고 속도와 회전을 안정시킨 채 3초 유지한다.
5. 목표가 `Return To Base`로 바뀌는지 확인한다.

자동화 `Drone.Tutorial.HoverMissionPIE`는 FrontEnd 선택부터 Zone 진입, 실제 3초 안정 Hover, 귀환 목표 전환까지 통과했다. 수동 확인에서는 Zone 가독성과 조작 체감만 추가로 본다.

## 4. 자동 검증

- `Drone.Physics.CollisionResponse`
- `Drone.Physics.Breakables`
- `Drone.Mission.StoryPhysicsTestMaps`
- `Drone.Tutorial.HoverMissionPIE`
- `Drone.Flow.Contract`
- `Drone.Flow.FrontEndContract`
- `Drone.Flow.FrontEndPIE`

Story·Physics 자산을 다시 만들거나 검증할 때는 `Tools/AssetMigration/Invoke-DroneStoryPhysicsTestMaps.ps1`을 사용한다. Tutorial 공유 시험맵은 `Tools/AssetMigration/Invoke-DroneTutorialMissionTest.ps1`로 별도 관리한다.

2026-09-29 수정본 최종 결과는 `Drone.Physics` 2/2와 `Drone.Mission.StoryPhysicsTestMaps` 1/1 Success, Physics Map Check `0 errors / 0 warnings`다. `Breakables`에는 Native 기본 크기 상한, 끊어진 그물 물리 조각 생성/Reset 정리, 실제 `ADronePrototypePawn::OnActorHit → Point Damage → Breakable Wall` 경로 회귀가 포함되며, Story/Physics 저장 계약은 저장된 맵 안의 Blueprint 그물·벽 크기 상한도 다시 읽어 검사한다.

## 5. 다음 구현 순서

1. Physics Sandbox 수동 반발·그물 국소 절단·파괴 벽 조각/복구 확인과 실제 충돌 로그 보강
2. Story 4개 Mission의 간이 Objective 수동 통과 확인
3. Mission 1부터 실패 조건과 UI 문구 보강
4. 현재 Runtime 그물/벽 기준과 Dataflow/Chaos Cloth·Geometry Collection 자산을 같은 조건으로 비교
5. Wing/Rotor Contact Probe와 Net Interaction 상태로 감속·자세 교란·탈출·포획/추락 구현
6. 전용 Pawn 반발을 일반 Flight Pawn의 모든 유효 Blocking 벽·구조물 접촉으로 확장하고 Landing/Crash와 분리
5. 파편 Sleep/Disable/Removal과 Mission Damage Event 1회 전달 추가

