# 현재 작업 상태

기준일: 2026-08-26 (Asia/Seoul)

이 문서는 PC별로 명령으로 확인된 상태와 사용자가 아직 결정하지 않은 항목을 분리한다. 작업컴 기록과 이번 확인 PC의 결과를 같은 항목에서 섞지 않고 경로와 검증 시점을 함께 적는다.

실시간 작업 위치와 바로 다음 행동은 [`WORKBOARD.md`](WORKBOARD.md), 날짜별 변경과 검증 이력은 [`docs/DRONE_WORKLOG.md`](docs/DRONE_WORKLOG.md)에 기록한다. 이 문서는 검증된 기준선이 달라질 때 함께 갱신한다.

## PC별 확인 완료

아래 Git·Unreal·Visual Studio 설치 정보는 작업컴에서 확인한 값이다. 저장소 상태는 같은 표에서 작업컴 기록 경로와 이번 확인 PC 경로를 구분한다.

| 항목 | 확인 결과 |
|---|---|
| Git | 2.53.0.windows.3 설치됨 |
| Git LFS | 3.7.1 설치됨, 전역 LFS 필터 설정 존재 |
| Unreal Engine | `Build.version` 기준 UE 5.8.1 설치 확인 |
| 추가 Unreal 설치 | UE 5.7도 설치되어 있음 |
| Visual Studio | Visual Studio Community 2026 18.8.2 설치 확인 |
| Git 사용자 이름 | 전역 `gyeonliz` 설정 확인 |
| Git 사용자 이메일 | 전역 `jkw6483@gmail.com` 설정 확인 |
| GitHub CLI | 설치되어 있지 않음 |
| 기본 작업 루트 | `D:\JGY\project` |
| Unreal 프로젝트 저장소 | 기준 경로 `D:\JGY\project\drone`; 로컬 `main`=`origin/main`=`551e287`, 기존 `Config/DefaultEditor.ini` 변경과 새 `Content/Drone/ThirdParty/DronePack` 154개가 미커밋 |
| 문서 작업 저장소 | 현재 작업 경로 `D:\JGY\project\md`; 최신화 직전 로컬 `main`=`origin/main`=`466609d`, 작업 트리 Clean |
| Commit·Push 처리 | TUT-03 `551e287`은 `origin/main`에 Push 완료. NavigationArrows `5a052c8`은 `origin/codex/navigation-arrows-migration`에 Push됐지만 main 미병합. 이번 문서 최신화는 로컬 미커밋이며 사용자가 Commit·Push |
| 실행 상태 | 기준 `D:\JGY\project\drone\Drone.uproject` Editor PID 22936 실행 중. 추가로 실행된 중복 인스턴스 PID 2764는 정상 창 닫기로 종료 |
| 별도 `droner` 주의 | `main=origin/main=551e287`; `Config/DefaultEditor.ini` 변경과 `Content/Asset` 10,928개·36,360,181,427 bytes 전체가 Untracked. 공급사 원본·스테이징 복사본이므로 일괄 Stage·Commit 금지 |

GitHub CLI는 필수 구성요소는 아니다. 자동 설치를 한 번 시도했으나 Windows Installer가 종료 코드 1602로 취소되어 설치되지 않았다. GitHub 웹과 Git Credential Manager만으로도 기본 Push/Clone 작업은 가능하다.

전역 Git 작성자 정보는 `gyeonliz <jkw6483@gmail.com>`으로 설정되어 있다. Unreal 프로젝트는 `https://github.com/gyeonliz/drone.git`, 문서 저장소는 `https://github.com/gyeonliz/md.git`를 `origin`으로 사용하며 둘 다 첫 Commit과 Push를 완료했다. 기준선 확인 시 각 로컬 `main`과 `origin/main`이 일치했다. 작업컴 기본 PowerShell 정책은 `.ps1` 직접 실행을 차단하므로 컨텍스트 도구 검증에는 영구 설정 변경 없이 실행 1회에만 `-ExecutionPolicy Bypass`를 적용했다.

## PC별 Drone 프로젝트 기준

현재 작업컴의 기본 프로젝트 경로는 다음과 같다.

```text
D:\JGY\project\drone\Drone.uproject
```

이 프로젝트는 2026-08-19 초기 감사 당시 `C:\project\Drone`에서 발견하고 정비했다. 아래의 "시작 시" 수치와 `91498b7`은 당시 사실을 보존한 역사 기록이다. `C:\project\Drone`은 현재 기준보다 뒤처진 복제본이므로 사용하지 않았고, 현재 D 드라이브 프로젝트의 로컬·원격 main 기준 Commit은 `551e287e8a5de7fa33f28d1911f8a7a957bd66fa`이다.

확인 결과:

- 실행 로그 기준 UE 5.8.1 (`Release-5.8`, Changelist 56057345)
- Runtime 모듈 이름은 `Drone`
- 초기 기존 내용은 UE Third Person C++ 템플릿과 Variant 예제 중심
- `StateTree`, `GameplayStateTree` Plugin이 활성화되어 있음
- 시작 시 Git 저장소가 아니었음
- 작업 시작 시 Content에는 `.uasset` 749개와 `.umap` 4개가 있었음

기존 Third Person 기본 맵과 전역 기본 GameMode는 유지하면서 Git 준비, Android 제외 설정, 별도 Drone Prototype Source를 적용했다.

- `main` Branch의 로컬 Git 저장소 초기화
- 프로젝트 로컬 Git LFS 초기화
- Unreal `.gitignore`와 `.gitattributes` 적용
- 생성 폴더 제외 및 `.uasset`/`.umap` LFS 속성 확인
- `.sln`과 UE 5.8의 `.slnx` 생성 파일 제외 확인
- Android File Server Plugin과 네트워크 사용 비활성화
- Android File Server `SecurityToken` 빈 할당 확인
- 별도 `ADronePrototypePawn`과 `ADronePrototypeGameMode` 추가
- 구조 및 Spawn/Possess 자동화 테스트 2개 추가
- Prototype 전용 입력 계약에 키·Value Type·Modifier·기대 부호 기록
- Input Action 5개와 Keyboard·Mouse·Gamepad 15개 Mapping의 `IMC_DronePrototype` 구성
- `BP_DronePrototypePawn`에 IMC·다섯 Action·Engine Cube Placeholder 연결
- `BP_DronePrototypeGameMode`의 Default Pawn을 BP Prototype Pawn으로 연결
- 별도 `Lvl_DronePrototype` Greybox Map과 GameMode Override 구성
- 863개 파일을 `91498b7` (`chore: initialize Drone project`)로 첫 Commit
- GitHub `gyeonliz/drone`의 `origin/main`에 Push
- HUD-01 Commit `08e876a` Push 완료
- HUD-02 Commit `410c940` (`feat: add event-driven drone flight HUD`)을 기능 브랜치와 `origin/main`에 Push
- WBP/BP 연결 보강 Commit `9f91bb6` (`feat: add Blueprint-backed flight HUD`)을 `codex/hud-blueprint-ready-comments`와 `origin/main`에 Push
- TUT-01 Commit `5a9a2fa`를 `origin/main`에 Push하고 Training Map·비충돌 Spline 안내선 기준선을 반영
- TUT-02 Commit `800a7ba` (`feat: add ordered tutorial ring gates`)를 `codex/tutorial-ring-gates`와 `origin/main`에 Push
- FPV Integration·공식 Unreal MCP 기준 Commit `2159382` (`0825/12:30`) Push 상태 확인
- TUT-03 Commit `551e287` (`feat: record tutorial lap timing and distance`)을 `codex/tutorial-lap-recording`과 `origin/main`에 Push

첫 Commit은 863개 파일이며 `Content`는 761개로 `.uasset` 756개와 `.umap` 5개다. 가장 큰 파일은 약 21.0 MB이고 100 MB를 넘는 파일은 없다. 새 Prototype `.uasset`과 `.umap`을 포함한 Unreal Asset에는 Git LFS의 filter·diff·merge 속성이 적용된다. WBP·BP Controller·TUT-01 Asset에 이어 TUT-02의 신규 `BP_DroneTrainingGate`와 갱신한 `Lvl_DroneTraining` 두 Asset도 Git LFS로 Push했다.

현재 구현된 Drone 기능 기준선은 Prototype Pawn/GameMode, Move·Altitude·Yaw·Camera 입력, Telemetry Snapshot, 실제 Flight HUD, TUT-01 Training Map·비충돌 Spline, TUT-02 Ordered Ring Gate와 TUT-03 Segment/Lap 원본 기록까지다. `ADroneTrainingGate`는 비충돌 Ring Visual과 별도 Pawn Overlap Trigger를 분리하고, `UDroneTrainingGateSequenceComponent`는 순서·정방향·중복 통과를 판정한다. Course 소유 `UDroneTrainingLapRecorderComponent`는 정상 Gate Event와 기존 Telemetry 10Hz 위치 표본으로 World Game Time, 실제 3차원 이동 거리와 평균 속도를 기록한다. 이전 평균·Best 비교와 결과 UI는 아직 TUT-04 범위다. Take Off, Landing, Crash/실패, Mission, Enemy AI, MG 점유·공격, Evaluation도 아직 구현된 것으로 판정하지 않는다. 이전 기준 Commit `fb891fb`의 잘못된 `//test` 주석은 이력 재작성 없이 `2c38ebf`에서 제거했다.

사용자는 이 프로젝트에서 Android를 사용하지 않는다고 확정했다. 이에 따라 `Config/DefaultEngine.ini`의 Android File Server Plugin과 네트워크 연결을 끄고 `SecurityToken` 할당을 비웠다. 검사 결과 활성 Plugin 0, 네트워크 허용 0, 비어 있지 않은 토큰 0이다. 기존 토큰 값은 이 문서나 로그에 기록하지 않았다. 향후 Android File Server를 다시 켤 경우 빈 토큰은 인증 없는 상태가 될 수 있으므로 보안 설정을 새로 검토해야 한다.

`.vsconfig`를 확인한 결과 Visual Studio workload와 component ID만 있으며 자격 증명이나 개인 경로는 없다. UE가 선호한다고 표시한 14.50 계열 도구 구성도 포함해 첫 Commit에 반영했다.

## 2026-08-25 제공 에셋 인수·이식 재검증

이 절의 `C:\에셋` 결과는 다른 PC에서 2026-08-25에 수행한 재감사 기록이다. 현재 D 드라이브 작업 PC에는 `C:\에셋`이 없고 `D:\JGY\project\Unreal_260821`이 존재한다. D 경로에는 최상위 ZIP 14개·공급사 폴더 14개와 `_Staging`이 있으며 `D:\JGY\project\Unreal\_260821`은 존재하지 않는다. 아래 C 드라이브 수치는 PC 간 이력 비교용으로 보존한다.

- 공급사 해제본 14개 기준선: 10,499개, 35,677,612,290 bytes
- `_Staging`, 내부 FBX 해제본, 생성 캐시를 포함한 `C:\에셋` 현재 전체: 10,928개, 36,360,181,427 bytes
- 현재 확장자 합계: `.uasset` 10,734개, `.umap` 26개, `.fbx` 66개, `.png` 13개, `.zip` 1개
- 남은 ZIP은 `Non-Pilot Drones KITBASH SET\FBX.zip` 하나이며, 내부 55개 FBX와 현재 해제된 55개를 SHA-256으로 대조해 불일치 0을 확인
- 파일명 기준 라이선스·EULA·README·Manual 문서는 없음. 구매 영수증과 사용 라이선스는 별도 보존 필요
- 제공 Unreal 패키지는 UE 4.23~5.6 단서가 섞여 있고, 선택 자산은 UE 5.8 스테이징에서 상향 재저장
- `GC_DroneS`의 7개 패키지에서 구형 `PhysXVehicles` 문자열 참조 단서가 확인되어 기능 Blueprint 재사용 금지
- `C:\에셋\DronePack_Project\Config\DefaultEngine.ini`에는 활성 Android File Server 설정과 비어 있지 않은 토큰이 있으므로 이 Config는 복사·Commit하지 않음. 토큰 값은 기록하지 않았고 실제 Drone 프로젝트 설정은 Plugin·네트워크 꺼짐, 토큰 빈 값 유지

실제 Drone 저장소에는 FPV/Sound 선택 자산 12개·21,753,071 bytes와 프로젝트 소유 Integration BP 1개, 합계 13개·21,787,555 bytes만 들어 있다. 10개 FPV 자산과 Wave는 UE 5.8 스테이징본과 SHA-256이 일치하고, Cue만 프로젝트에서 `Looping=true`로 재저장해 의도적으로 다르다. 스테이징 선택 자산 감사와 현재 Integration Asset Registry 재감사 결과 원본 `/Game/Drone_Pack`, `/Game/Drone-Sounds`, ThirdPerson, Variant 금지 의존성은 0이다. 13개 모두 Git LFS 대상이며 `git lfs fsck`를 통과했다. 이번 재검증에서 `Drone.Integration.FPVAsset` 1/1과 전체 Blueprint Compile 0 errors·0 warnings·0 load failures를 다시 통과했다. 전체 `Drone.` 14/14는 같은 현재 Commit에서 TUT-03 완료 때 통과한 기준선이며 이번 재감사에서는 다시 실행하지 않았다. 기존 Standalone 초기 렌더는 통과했지만 이번 재감사에서 새 화면·청감 수동 검사는 하지 않았다. 실제 스피커의 Loop 단일 재생과 종료 정지는 계속 `미확인`이므로 `AST-01`은 Doing이다. 상세 결과는 [`docs/DRONE_ASSET_INTAKE_2026-08-25.md`](docs/DRONE_ASSET_INTAKE_2026-08-25.md)를 따른다.

## 2026-08-25 UE 5.8 공식 Unreal MCP 연결

사용자가 전달한 Unreal Engine KR의 UEFN MCP 게시물에서 출발해 Epic의 UEFN 소식, UE 5.8 Unreal MCP 문서와 Codex MCP 문서를 대조했다. 현재 설치된 UE 5.8.1에는 `ModelContextProtocol`, `ToolsetRegistry`와 공식 Toolset 플러그인·Win64 Binary가 실제 포함되어 있다.

- 자체 통신 플러그인 초안은 공식 기능과 중복되어 제거
- `ModelContextProtocol`, `EditorToolset`, `AutomationTestToolset`, `UMGToolSet`, `StateTreeToolset`, `AIModuleToolset`을 `Editor` Target으로만 활성화
- 불필요한 PCG·Niagara·GAS 등을 함께 켜는 `AllToolsets`는 사용하지 않음
- `Config/DefaultEditorPerProjectUserSettings.ini`에서 `127.0.0.1:8000/mcp` 자동 시작 기본값 구성
- `.codex/config.toml`에 프로젝트 범위 `unreal-mcp` Streamable HTTP 연결과 변경성 Tool 승인 정책 구성
- `DroneEditor Win64 Development`와 `Drone Win64 Development` 모두 성공
- Course/Gate Editor 자동화 2개를 `WITH_EDITOR && WITH_DEV_AUTOMATION_TESTS`로 제한해 게임 타깃의 Editor API 컴파일 오류 수정
- 전체 `Drone.` 자동화 12/12 Success, Exit Code 0
- 실제 Editor MCP `initialize 200`, `initialized 202`, `tools/list 200`, 23개 Toolset 확인
- MCP를 통해 Training Map·PIE·Selected Actor·Content Browser 상태를 실제 조회하고 `Drone.` 테스트 12개 탐색 확인

2026-08-26 09:17 KST에는 기준 `drone` Editor PID 9884의 MCP 응답을 확인했다. 이후 09:40 KST에 그 프로세스가 종료되고 별도 복제본 `D:\JGY\project\droner\Drone.uproject`의 Editor PID 10960이 `127.0.0.1:8000/mcp`를 소유했다. 현재 MCP는 `droner` Editor에 연결되므로 기준 프로젝트 변경 Tool로 사용하지 않는다. `D:\JGY\project\drone` 루트의 새 Codex 작업과 기준 Editor에서 네이티브 Tool 노출을 확인하는 `UE-MCP-02`는 계속 Todo다. 세부 사용법과 보안 경계는 [`docs/DRONE_UNREAL_MCP.md`](docs/DRONE_UNREAL_MCP.md)에 기록했다.

## 프로젝트 빌드와 실행 점검

- 작업컴 PFN-06 검증에서는 고정 추적 Camera, Mouse Drone Yaw와 Gamepad 입력을 포함해 `DroneEditor Win64 Development`를 `-NoUBTMakefiles -CompilerVersion=14.51.36256`으로 다시 빌드했고 `Result: Succeeded`였다.
- 새 Action과 BP 참조 저장 뒤 `CompileAllBlueprints` Commandlet은 `0 error(s), 0 warning(s), 0 failed to load`로 정상 종료했다.
- 작업컴에서 기본 선택된 MSVC 14.38은 UE 5.8 Engine PCH 컴파일 오류를 냈다. 그 PC에 설치된 14.51.36256을 명시하면 빌드는 성공했다. 14.51은 UE가 표시한 선호 버전 14.50.35717보다 새 버전이라는 주의 메시지가 있으므로 PC마다 실제 설치 Toolchain을 확인해 명시한다.
- `Drone.Prototype.PawnDefaults`, `Drone.Prototype.PIEInputLifecycle`, `Drone.Prototype.SpawnPossess` Automation을 새 조작으로 다시 실행했다. Report 기준 3 succeeded, 0 warnings, 0 errors, 0 failed다. lifecycle은 새 PIE 3회 모두 Keyboard·Mouse·Gamepad 6축, 복합·반대 입력과 입력 세기 비교를 통과했다.
- 기존 `Lvl_ThirdPerson`을 저장 변경하지 않고 명령줄 URL로 `DronePrototypeGameMode`만 Override했다. GameMode 로드, `DronePrototypePawn` Spawn/Possess, 정상 종료를 확인했고 프로젝트 코드 Fatal/Error는 없었다.
- native Prototype Pawn CDO의 Mesh·IMC·5개 Input Action 기본값은 계속 `null`이다. 실제 Prototype Map은 BP 자식에 자산과 Engine Cube를 배정하고 BP GameMode가 그 BP Pawn을 Spawn하도록 분리했다.
- 자산 Create 실행에서 `CREATED_OK`와 동일 프로세스 `VALIDATION_OK`를 확인했다. 첫 별도 프로세스 검증은 Map을 generic asset으로도 강참조한 검증 스크립트 결함을 발견해 실패했으며, Map을 `LevelEditorSubsystem`으로만 여는 방식으로 수정했다. 수정 뒤 새 프로세스 재로드 검증은 `VALIDATION_OK`, Map Check 0 errors, 0 warnings로 통과했다.
- 새 자산 생성 뒤 `CompileAllBlueprints`는 종료 코드 0, 0 errors, 0 warnings였다. 전용 Map 헤드리스 Smoke Test에서도 BP GameMode와 BP Pawn Spawn/Possess, Enhanced Input Subsystem 초기화, 정상 종료 코드 0을 확인했다.
- 사전 GUI PIE 두 번은 역사적 부분 확인으로 보존한다. 사용자 승인 조작으로 다시 구현한 자동화 새 PIE 3회와 Standalone Keyboard·Mouse 수동 조작이 통과했다. 창 닫기는 `Win RequestExit`, `Game engine shut down`, `Exiting` 로그로 정상 종료됐고 PFN-06은 Done이다. 실제 Gamepad 체감은 장치 연결 여부가 보고되지 않아 미확인으로 기록한다. 정식 판정은 [`docs/DRONE_PROTOTYPE_PIE_CHECKLIST.md`](docs/DRONE_PROTOTYPE_PIE_CHECKLIST.md)를 따른다.
- 과거 전체 Editor 무창 점검 한 번은 `Quit` 뒤 프로세스가 종료되지 않아 해당 테스트 프로세스만 종료했다. 이번 Automation `Quit` 경로와 Prototype 게임 실행은 모두 종료 코드 0으로 정상 종료했다.
- 과거 로그의 `LogAutomationTest: Error: Condition failed` 15줄은 UE 내부 `UE::UnifiedErrorTest` 출력 직후, 프로젝트 맵 로드 전에 발생했다. 이번 Prototype Report에는 warning/error가 없다.
- 기준선 확인 당시 문서 저장소에만 있던 PFN-06 PIE lifecycle 테스트 초안은 Drone Source에 편입됐고 `UnrealEd` 의존성은 Editor 빌드 조건으로만 추가됐다. 런타임 공개 API 변경 없이 빌드와 Automation 3/3 Pass까지 확인했다.
- `Invoke-DronePrototypeSetup.ps1 -Mode UpdateControls`와 `Validate`는 9개 Prototype 자산, 5개 IA 타입, IMC 15개 Mapping, BP 참조와 Map GameMode Override를 확인했다. `/Game/Drone`의 신규 Legacy 의존성은 0개이며 기본 ThirdPerson Map/GameMode도 유지된다.
- HUD-01에서 `UDroneTelemetryComponent`와 `FDroneTelemetrySnapshot`을 추가했다. 0.1초 Timer로 Speed·Altitude·Vertical Speed·Heading을 제공하며 Prototype Pawn이 native Component 한 개를 소유한다.
- HUD-01 당시 `Drone.` Automation Report는 Prototype 회귀 3개와 Telemetry 2개를 합쳐 5 succeeded, 0 warnings, 0 failed였다. Runtime Spawn에서 기준 고도 변경 즉시 Snapshot 갱신도 확인했다.
- HUD-01 뒤 Blueprint 전체 Compile은 0 errors, 0 warnings, 0 blueprints failed to load로 정상 종료했다.
- HUD-02에서 `UDroneFlightHUDWidget`과 `ADronePrototypePlayerController`를 추가했다. Widget은 Tick·Property Binding 없이 `OnTelemetryUpdated`를 구독하고, Pawn 변경·Widget/Controller 종료 시 기존 구독을 해제한다.
- 현재 PC에서 자동 선택된 설치 Family 14.51.36231, 보고 Toolchain 14.51.36252로 최종 `DroneEditor Win64 Development` 빌드는 성공했다. UE의 선호 버전 14.50보다 새 버전이라는 주의만 있었다.
- `410c940` native HUD 기준선의 `Drone.` Automation Report는 6 succeeded였다. 이번 보강은 `Drone.UI.FlightHUDBlueprintAsset`을 추가해 최종 7 succeeded, 0 warnings, 0 failed다.
- `PIEInputLifecycle`은 새 PIE 3회마다 실제 `BP_DronePrototypePlayerController_C`와 `WBP_DroneFlightHUD_C`, HUD 한 개, native fallback 미사용, Viewport·Telemetry 연결, UnPossess 해제, 같은 Widget 재사용·Re-Possess 재연결과 종료 후 잔존 구독 없음까지 확인했다.
- `410c940` 당시에는 새 Asset이 없었다. 이번 보강에서는 `WBP_DroneFlightHUD`와 `BP_DronePrototypePlayerController`를 추가하고 `BP_DronePrototypeGameMode`를 갱신했다. 별도 Asset 테스트가 부모 Class, 필수 TextBlock 4개, 유효 Font와 BP 연결 체인을 검사한다.
- WBP/BP 보강 뒤 전체 `CompileAllBlueprints`는 종료 코드 0, 0 errors, 0 warnings, 0 blueprints failed to load였다.
- `410c940` Standalone에서 `SPD 43.2 km/h`, `ALT 2.7 m`, `V/S +10.0/-7.2 m/s`, Heading `002° → 025°/045°` 변화를 확인했다. 이번 보강 뒤 Standalone에서는 실제 WBP Class의 `FLIGHT DATA`, `SPD 0.0 km/h`, `ALT 1.5 m`, `V/S +0.0 m/s`, `HDG 000°`가 깨짐 없이 표시되는 것을 다시 확인했다.
- TUT-01에서 `ADroneTrainingCourse`, `BP_DroneTrainingCourse`, `Lvl_DroneTraining`, `M_DroneTrainingGuide`를 추가했다. 안내선 Material은 Opaque·Unlit·Emissive이며 Spline Mesh 사용 설정을 적용했다.
- TUT-01 최종 `DroneEditor Win64 Development` 빌드는 성공했다. `Drone.Tutorial` 전용 자동화는 3/3, 전체 `Drone.` 자동화는 10/10이며 두 결과 모두 warning과 failure가 없다.
- TUT-01 뒤 전체 `CompileAllBlueprints`는 0 errors, 0 warnings, 0 blueprints failed to load로 통과했다.
- Standalone에서 실제 `BP_DronePrototypePlayerController`, `BP_DronePrototypePawn`, `WBP_DroneFlightHUD` 사용과 Cyan 안내선 표시를 확인했다. Spline Mesh가 Material 기본값으로 대체됐다는 경고도 발생하지 않았다.
- 자동화 Sweep에서 Drone이 안내선을 막힘 없이 통과했고, Course가 만든 Primitive는 Collision·Overlap·Physics·Navigation 영향을 사용하지 않는 것을 확인했다. Training Map에는 저장된 Recast NavMesh Actor가 존재한다.
- TUT-02에서 `ADroneTrainingGate`, `UDroneTrainingGateSequenceComponent`, Gate 결과·시각 상태 타입과 실제 `BP_DroneTrainingGate`를 추가하고 Training Map에 네 Gate를 명시적 순서로 연결했다.
- TUT-02 최종 `DroneEditor Win64 Development` 빌드는 성공했다. `Drone.Tutorial.TrainingGateSequence` 1/1, 실제 BP Gate Begin/End Overlap을 포함한 PIE Smoke 1/1, 전체 `Drone.Tutorial` 4/4, 전체 `Drone.` 11/11이 warning·failure 없이 통과했다.
- TUT-02 뒤 전체 `CompileAllBlueprints`는 0 errors, 0 warnings, 0 blueprints failed to load로 통과했다.
- 자동화는 잘못된 Actor·미래 Gate·역방향·중복 통과를 거부하고 현재 Gate의 정방향 통과만 한 번 승인하는 것, Ring 비충돌·Trigger Pawn Overlap과 Current/Completed/Inactive 상태 전환을 확인했다.
- Standalone에서 실제 HUD·Course 안내선과 Current/Inactive Gate 표시를 확인했다. Lap·Timing·거리·평균 속도 계산이나 기록 UI는 이 검증에 포함하지 않았다.
- AST-01에서 FPV 본체·로터 4·재질/Texture와 44.1 kHz Drone Loop Cue/Wave를 선별 이식했다. 공급사 Blueprint 전체 Compile은 0 errors·27 warnings로 구형 Input Axis와 Mannequin Rig 의존성을 드러내 기능 BP 재사용 금지 판정을 유지했다.
- 제공 Cue는 이름과 달리 실제 반복 설정이 꺼져 있었다. SoundNode Wave Player의 Looping을 명시적으로 켜고 `USoundBase::IsLooping()` 계약을 자동화에 추가해 재검증했다.
- 선택 자산 12개는 `/Game/Drone/ThirdParty` 내부 의존성만 사용하며 ThirdPerson·Variant·원본 `/Game/Drone_Pack`·`/Game/Drone-Sounds` 신규 의존성이 0이다. Integration BP는 실제 런타임 본체 1·Rotor 4·Audio 1, Visual Collision/Overlap/Physics/Navigation 비활성, BP GameMode의 FPV Pawn·BP PlayerController 연결을 검사한다.
- 최종 `DroneEditor Win64 Development` Build, Blueprint Compile 0 errors·0 warnings·0 load failures, Map Check 0 errors·0 warnings, 전체 `Drone.` Automation 12/12를 통과했다. `PIEInputLifecycle` 새 PIE 3회와 Training PIE도 FPV Integration Pawn으로 통과했다.
- `Lvl_DroneTraining` Standalone 렌더 캡처에서 FPV 외형, 고정 추적 Camera, HUD·Course·Gate 표시와 정상 종료를 확인했다. 실행 시 처음 한 번 4K Texture DDC를 생성해 종료가 약 76초 지연됐지만 `Game engine shut down`과 `Exiting`까지 정상 완료했다. 실제 스피커 Drone Loop 청감은 아직 수동 확인 대기다.
- TUT-03에서 `FDroneTrainingSegmentRecord`, `FDroneTrainingLapRecord`와 Course 소유 `UDroneTrainingLapRecorderComponent`를 추가했다. Gate 0은 시작선이며 이후 Gate마다 Segment를 확정하고 마지막 Gate에서 성공 Lap 원본을 실행 중 History에 보존한다.
- 위치는 기존 Telemetry 10Hz Event에서 같은 Drone의 World 위치를 표본화하고 Gate 승인 위치를 끝점으로 추가한다. `SegmentDistance` 메타데이터나 Gate 간 직선거리는 실제 이동 거리 계산에 사용하지 않는다.
- Reset·Course 재구성·구성 무효화·Pawn 파괴 시 부분 시도와 Delegate를 정리하며, 같은 Frame 0초 순간이동은 성공 기록으로 남기지 않는다. 성공 History는 Reset에는 유지하고 Course 재구성에는 비운다.
- TUT-03 최종 `DroneEditor Win64 Development` Build, `Drone.Tutorial` 6/6, 전체 `Drone.` 14/14, Blueprint Compile 0 errors·0 warnings·0 load failures를 통과했다. 실제 저장 BP Course/네 Gate/FPV Integration Pawn PIE Overlap도 포함한다.

Prototype 입력·Editor 연결 절차는 [`docs/DRONE_PROTOTYPE_IMPLEMENTATION.md`](docs/DRONE_PROTOTYPE_IMPLEMENTATION.md), Telemetry와 Flight HUD 구현·검증은 [`docs/DRONE_TELEMETRY_IMPLEMENTATION.md`](docs/DRONE_TELEMETRY_IMPLEMENTATION.md)에 기록했다.

## 발견했지만 사용하지 않은 Unreal 프로젝트

다음 프로젝트 하나가 문서 폴더에서 발견됐다.

```text
C:\Users\jkw11\Documents\Codex\2026-08-12\c-project-factoryenvironmentcollect\work\drone_audit\DroneAudit.uproject
```

이 프로젝트는 자체 설명이 `Read-only drone asset inspection sandbox`이고 `EngineAssociation`이 5.7이다. UE 5.8.1 기반 메인 Drone 프로젝트로 간주하지 않았고 어떤 파일도 수정하지 않았다.

## 이번 작업에서 준비한 것

- 사용자 제공 기준을 `CONTEXT.md`로 보존
- Unreal용 `.gitignore`와 `.gitattributes` 템플릿
- Git 설치부터 Push/Clone, 브랜치, Asset 충돌 방지, 복구까지의 가이드
- 인증·원시 세션 데이터를 제외하는 Codex/GPT 문맥 Export/Import 도구
- Windows PowerShell 5.1 호환 UTF-8 인코딩과 Export → Import SHA-256 왕복 검증
- `handoffs/workpc-2026-08-19-baseline`에 검토 후 복사할 실제 인계 패키지 생성. 아직 다른 PC로 전송한 것은 아님
- Drone Flight MVP, Enemy AI MVP, Mission, UI/Evaluation 개발 백로그
- 후보 프로젝트의 C++·Enhanced Input·기본 맵·템플릿 Variant 읽기 전용 감사
- Android 제외 결정 반영과 Android File Server 보안 설정 정리
- 격리된 `APawn` 기반 Drone Prototype, native GameMode, 자동화 테스트 3개
- 최종 빌드, 구조·Spawn/Possess·PIE Input Lifecycle 테스트, 헤드리스 게임 실행 검증
- Prototype Input Action·IMC·BP Pawn/GameMode·전용 Greybox Map 생성 도구와 재검증 도구
- 사전 GUI PIE의 역사적 부분 확인과 2026-08-21 Standalone 수동 조작 Pass 기록
- Event 기반 C++ Flight HUD 기능, 실제 WBP Designer 외형, BP PlayerController/GameMode 연결과 Possession 전환·종료 수명주기 자동화
- 2026-08-23 Standalone에서 Speed·Altitude·Vertical Speed·Heading 실제 화면 변화 확인
- `ADroneTrainingCourse`, 실제 BP Course, 별도 Training Map과 Opaque·Unlit·Emissive Cyan 안내 Material로 TUT-01 완료
- TUT-01 전용 자동화 3개, 전체 Drone 자동화 10/10, Blueprint 전체 Compile과 Standalone 표시·비충돌 검증
- `ADroneTrainingGate`, Gate Sequence Component, 실제 BP Gate 네 개와 분리된 Ring Visual·Trigger로 TUT-02 완료
- Gate Sequence 1/1, 실제 BP PIE Smoke 1/1, Tutorial 4/4, 전체 Drone 11/11과 Standalone Current/Inactive Gate 표시 검증
- `UDroneTrainingLapRecorderComponent`, BlueprintType 기록 Struct와 BlueprintAssignable Event로 TUT-03 완료
- Tutorial 6/6, 전체 Drone 14/14, Blueprint 0/0/0으로 시간·3차원 실제 이동 거리·평균속도와 Reset/Pawn 수명주기 검증
- Q-Net 공식 정보처리산업기사 2026 일정과 시험 구성을 확인하고, 개인 접수·필기면제 상태별 Track A/B/C 및 C++ 코딩테스트 병행 계획을 `docs/MOBILE_CURRENT_BRIEF.md`와 `docs/STUDY_PLANS.md`에 정리
- 구매 소스 없이 Engine 기본 도형으로 진행하는 기능 우선 Greybox 사전계획
- 전체 작업 관리 및 병행 학습 계획
- 실제 진행 상태를 담는 `WORKBOARD.md`

## 다음 단계

1. 사용자가 실제 Training Map에서 Gate 0→3 한 Lap과 Drone Loop 단일 재생·종료 정지를 수동 확인
2. `TUT-04` 이전 평균·Best 비교 규칙을 확정하고 결과 UI와 Tutorial 회귀 구현
3. 그 다음 Flight 상태, Operator↔Drone, NPC·Mission UI, Jamming Story 순으로 진행
4. 병행 과제로 다른 PC에서 `551e287` Pull, LFS/UE 5.8.1 실행과 문서 Pull 확인
5. 정보처리산업기사는 Q-Net 개인 접수·수험일·필기면제 상태를 확인해 Track A/B/C를 선택하고, 코딩테스트는 주간 반복으로 병행

Camera·Mouse·Gamepad 역할은 v1 조작으로 확정했다. Keyboard·Mouse 체감은 현재 시험값으로 통과했으며 실제 Gamepad 체감, 최종 물리와 최종 감도 조정은 이후 별도 카드로 남긴다. 구매 소스와 최종 Mesh는 선행 조건이 아니며 상세 계획은 [`docs/DRONE_TUTORIAL_STORY_PLAN.md`](docs/DRONE_TUTORIAL_STORY_PLAN.md)를 따른다. 이동 중 볼 통합 요약과 날짜별 학습안은 [`docs/MOBILE_CURRENT_BRIEF.md`](docs/MOBILE_CURRENT_BRIEF.md)를 따른다.

Git 공유 작업과 Drone 기능 작업은 서로를 불필요하게 막지 않고 다음 세 흐름으로 이어간다.

```text
Drone: origin/main 동기화 완료
→ 다른 PC Clone/LFS/UE 실행 검증

MD: gyeonliz/md origin 연결 완료
→ 첫 Commit과 Push 완료
→ 다른 PC Clone/Pull과 문맥 확인

PFN-06 Done
→ HUD-01 Telemetry Snapshot Done
→ HUD-02 Flight HUD Done
→ TUT-01 Training Map·비충돌 Spline Done
→ TUT-02 Gate·순서·정방향 판정 Done
→ TUT-03 Segment/Lap 기록 Done
→ TUT-04 비교·결과 UI
→ Take Off·Landing·Crash
→ Operator↔Drone 전환
→ NPC·Mission UI Story Shell
→ Enemy AI·MG·Jamming
→ 통합 Greybox·외부 Drone 에셋 적용
```

최종 감도, Mouse Y 반전, 비행 물리, 멀티플레이와 세부 Mission 규칙은 현재 미정으로 유지한다.

## 2026-08-26 NavigationArrows 최소 이식 상태

사용자는 지원과정을 통해 구매·지급된 제공 에셋의 프로젝트 사용 권리를 확인했다. `C:\에셋`에 별도 라이선스·영수증 파일이 없다는 기존 기록은 로컬 증빙 보관 상태로 유지하며, 권리 미확정이나 법률 검토 완료로 바꾸어 해석하지 않는다. `PBR Sting`의 `isAiForbidden: true`는 해당 팩의 생성형 도구 업로드 제한으로만 유지한다.

- 원본: `NavigationArrows` 11개·1,364,087 bytes, UE 5.2/5.3 저장본
- 선택 이식: 6개·UE 5.8 재저장 후 1,098,730 bytes
- 경로: `/Game/Drone/ThirdParty/NavigationArrows`
- 구성: Widget Blueprint 1, Texture2D 2, UserDefinedStruct 3
- 제외: `Demo.umap`, `Demo_BuiltData`, `NavigationArrowExampleActor`, `ExampleMesh`, `TransparentCircle`
- 의존성: 로드 실패 0, 외부 `/Game` 의존성 0, 원본 `/Game/NavigationArrows` 의존성 0
- 검증: `DroneEditor Win64 Development` 성공, 전용 자동화 1/1, 전체 `Drone.` 15/15, Blueprint Compile 0 errors·0 Blueprint warnings·0 failed loads, Git LFS 속성 6/6과 `git lfs fsck` 통과
- Git: Commit `5a052c8bab2eb0dd8bc9ab16cfc7b3784e8e4cd7`을 `origin/codex/navigation-arrows-migration`에 Push 완료. `main`은 `551e287`로 유지되어 아직 이 6개 자산을 포함하지 않음
- 적용 범위: 안전한 ThirdParty 인수까지만 완료. Training Map/HUD의 실제 화면 표시와 프로젝트 소유 Host/Wrapper는 다음 단계

`AST-02A`의 최소 이식·검증·원격 기능 Branch 공유는 완료했다. 실제 화면 Host/Wrapper와 main 반영은 미구현이다. `AST-01`의 실제 스피커 Loop 단일 재생·종료 정지는 계속 미확인이므로 Doing이다. 다음 기능 카드는 계속 `TUT-04`이며 NavigationArrows 화면 연결과 섞어 완료 처리하지 않는다.

## 2026-08-26 Dataflow·Chaos 물리 환경 후보

UE 5.8의 Dataflow·Chaos Cloth·Chaos Destruction을 부분 고정 그물과 선택형 맵 파괴의 후속 기술로 채택했다.

- 현재 UE 5.8.1 설치본에서 `Dataflow`, `ChaosCloth`, `ChaosClothAsset`, `ChaosClothAssetEditorCore`, `ChaosClothAssetDataflowNodes`, `ChaosEditor`, `GeometryCollectionPlugin` 존재 확인
- 현재 `Drone.uproject`에 위 Cloth/Destruction Plugin 명시적 활성화 0
- Deprecated `ChaosClothAssetEditor`, `ChaosClothEditor` 사용 금지
- 일부 고정 그물: Max Distance 0 또는 Kinematic Selection, 나머지 영역 Weight Map 시뮬레이션
- 맵 파괴: Dataflow Geometry Collection, Anchor/World Support, Damage Threshold, Strain/Force와 Debris Sleep/Disable
- Cloth 변형·파괴 연출과 포획·Damage·Mission 판정을 분리
- 현재 생산 Cloth/Geometry Collection Asset 0, 관련 C++ 0
- 다음 기능 우선순위는 `TUT-04`; 첫 물리 작업은 별도 `PHY-DF-00` Sandbox

상세 설계는 [`docs/DRONE_CHAOS_DATAFLOW_PLAN.md`](docs/DRONE_CHAOS_DATAFLOW_PLAN.md)를 따른다.
