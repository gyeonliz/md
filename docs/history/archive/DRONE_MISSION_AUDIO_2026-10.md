# Mission 사용자 오디오 — 이전 검증 정본 보존

2026-10-30 제출음원14종 정본 갱신 전 절의 원문이다. 현재 연결·조정은 DRONE_MISSION_FRAMEWORK_GUIDE의 같은 절을 따른다.

### 사용자 오디오와 체력 경고

사용자 원본321Go/warning/tung/gunshot MP34개를 보존하고 mono48kHz PCM16·동일-6dB headroom으로7개 SoundWave를 신규 저장했다. 준비 PCM clipped sample0, S_HealthWarning만 loop다. 기존 map/BP 저장 없이 `/Game/Drone/Audio/User_20261022`에 연결했다.

| 원본 | 자산 | 연결 계약 |
|---|---|---|
| 321Go.mp3 | S_Countdown_3 / S_Countdown_2 / S_Countdown_1 / S_Countdown_Go | 현재 숫자/GO 전환마다1회·1x, 기존 Director1초·출발/랩 시작 시계 유지 |
| warning.mp3 | S_HealthWarning | alive·low health 동안 루프1개, 회복/사망·pause·Master0·소스/위젯 해제 정리. 신호/배터리 경고만으로 재생하지 않음 |
| tung.mp3 | S_DroneDestroyed | 생애별 Health.OnDeath1회·재사망2life. 본인local PC 소유 공간음만 재선택 pause에서도 재생 |
| gunshot.mp3 | S_Gunshot | 일반소총·유인/무인/차량포탑·UGV 실제발사. 적군 샷건·UGV유탄 제외 |

HUD Class Defaults의 `HealthWarningSound`, Countdown driver의 `CountdownThreeSound / CountdownTwoSound / CountdownOneSound / CountdownGoSound`에서 음원을 바꾼다. 전체 음량·적용/취소/저장은 [기존 설정 계약](DRONE_TITLE_LOBBY_ORBIT_GUIDE.md)을 따른다. 경고10/카운트다운12구역의 내부 이름·사용자 Designer와 `WBP_DroneFlightHUDKit` 정본을 유지한다. 카운트다운은 Snapshot 반복/같은 Director 재연결로 다시 시작하지 않으며 GO 음원 tail로 실제 출발을 늦추지 않는다.

첫 경고 text-only를 같은 저장 HUD Kit/natural present fixture에서 재현했고, 글자/자식을 먼저 갱신한 뒤 Collapsed→표시 전환에만 warning subtree prepass를 적용해 첫 프레임부터 배경·아이콘·글자가 함께 표시됨을 확인했다. Normal/Oracle의12/12 frame연결·양성/음성 픽셀 검증은 통과했다. 검사 종료 readback race 수선과 제품 수리를 구분한다.

실제 FrontEnd catalog의 Racing Map1 출격과 Story M4(Lvl_MilitaryCamp)에서 native Mission PlayerController가 생성한 Pawn·Director·저장 HUD Kit/Countdown WBP 조립을 확인했다. 임시 fixture actor/widget를 새로 만든 검사가 아니라 실제 public flow·Health·fire 호출을 자동 주입한 범위다. 레이싱3/2/1/GO의 cue4/PCM과 실제 Window4PNG, M4 첫low epoch4와 다음5의 경고3파츠·warning1/recovery0을 확인했다. M4 UGV200→199·차량/고정자동포탑 각각 projectile1·Rifle fired1/ammo1에서 정확한 cue와 실제 physical source1을 대조했고 Shotgun8pellet/replacement0도 보존했다. 유인MG는 해당맵 미배치로 실제미션 통과 범위에 넣지 않는다. 발사/피해 public API의 자동 주입 결과이며 NPC 자율교전이나 실물 사격 완료는 아니다.

실제 M4는 사망 다음tick 재선택 UI가 game pause를 걸어 기존 non-UI tung voice 객체만 남고 physical source/DSP 재생이 시작되지 않는 결함이 있었다. 로컬 기체의 본인 PlayerController audio instance만 pause 예외로 생성하고 기존3D 감쇠/Master·1x·PC소유/auto-destroy를 유지했다. 비로컬 기체의 기존 world sound 분기와 게임플레이·물리·카메라·미션 pause 규칙은 바꾸지 않았다. 수리 뒤 선택창 paused=true에서 두 생애마다 tung1개·실제 mixer frame 증가와 원본PCM 상관 약0.998712를 확인했다. voice 객체 수나 혼합PCM 비영만으로 재생을 판정하지 않는다.

**현재 자동 검증:** Build5 성공16.72초, 실제 Mission 신규2개 명명Success(각 succeededWithWarnings1/failed0)다. 직접영향 기존 DroneDestroyed/ImpactDestroyed/MasterMute3개 재검사 Success. Racing은 사망음 pause 수리 전 별도리비전이고 M4/직접회귀3은 최종리비전이다. 기존18+8 지정검사 전체를 이번에 다시 실행한 결과는 아니며 실제 미션의 좁은 통합 범위와 구분한다. 최종Source418/418·신규통합test1개·freeze SHA 38EC6EF7…6F578BA6·기존417중416 보존·FlightPawn audio블록/include2만 수정, Config5/보호125/SourceArt12·Saved10 일치·최종 엔진/Build0 확인. 실물 손조종/전체미션 수동완주·스피커 청감/주관 밸런스·Cook/패키징은 미실시다.

offscreen PCM0은 FApp volume0→effectivePrimary0 검사환경으로 분리했고 device mute 가설은 반증됐다. 검사 scope의 `au.DisableAppVolume=1`/원래값복원·동기 mixer WAV를 사용하며 실제 Master와 구분한다. Shotgun/SpatialFar의 실제 무음PCM은 process-local `au.NeverDisableSubmixes=1` 조건으로 확인했다. 제품 사용자 볼륨/OS설정 변경과 혼동하지 않는다. `DefaultGame.ini`의 `+DirectoriesToAlwaysCook=(Path="/Game/Drone/Audio/User_20261022")`는 정적 포함경로 설정이며 실제 Cook/패키징은 미실행이다. 스피커 청감도 미실시다.

