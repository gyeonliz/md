# 현재 작업 상태

기준일: 2026-08-21 (Asia/Seoul)

이 문서는 명령으로 확인된 작업컴 상태와 사용자가 아직 결정하지 않은 항목을 분리한다.

실시간 작업 위치와 바로 다음 행동은 [`WORKBOARD.md`](WORKBOARD.md), 날짜별 변경과 검증 이력은 [`docs/DRONE_WORKLOG.md`](docs/DRONE_WORKLOG.md)에 기록한다. 이 문서는 검증된 기준선이 달라질 때 함께 갱신한다.

## 작업컴에서 확인 완료

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
| Unreal 프로젝트 저장소 | `D:\JGY\project\drone`, 로컬 `main`=`2c38ebf`, `origin/main`=`fb891fb`, PFN-06 로컬 Commit 완료 |
| 문서 작업 저장소 | `D:\JGY\project\md`, `origin/main`=`9e81de0`, 현재 갱신은 로컬 Commit으로 관리 |

GitHub CLI는 필수 구성요소는 아니다. 자동 설치를 한 번 시도했으나 Windows Installer가 종료 코드 1602로 취소되어 설치되지 않았다. GitHub 웹과 Git Credential Manager만으로도 기본 Push/Clone 작업은 가능하다.

전역 Git 작성자 정보는 `gyeonliz <jkw6483@gmail.com>`으로 설정되어 있다. Unreal 프로젝트는 `https://github.com/gyeonliz/drone.git`, 문서 저장소는 `https://github.com/gyeonliz/md.git`를 `origin`으로 사용하며 둘 다 첫 Commit과 Push를 완료했다. 기준선 확인 시 각 로컬 `main`과 `origin/main`이 일치했다. 작업컴 기본 PowerShell 정책은 `.ps1` 직접 실행을 차단하므로 컨텍스트 도구 검증에는 영구 설정 변경 없이 실행 1회에만 `-ExecutionPolicy Bypass`를 적용했다.

## 현재 작업 Drone 프로젝트

현재 기본 프로젝트 경로는 다음과 같다.

```text
D:\JGY\project\drone\Drone.uproject
```

이 프로젝트는 2026-08-19 초기 감사 당시 `C:\project\Drone`에서 발견하고 정비했다. 아래의 "시작 시" 수치와 `91498b7`은 당시 사실을 보존한 역사 기록이며, 현재 경로와 로컬 기준 Commit은 각각 `D:\JGY\project\drone`, `2c38ebf`다.

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
- PFN-06 마감 로컬 Commit `2c38ebf`; `origin/main`의 `fb891fb`보다 1개 Commit 앞서며 Push는 하지 않음

첫 Commit은 863개 파일이며 `Content`는 761개로 `.uasset` 756개와 `.umap` 5개다. 가장 큰 파일은 약 21.0 MB이고 100 MB를 넘는 파일은 없다. 새 Prototype `.uasset`과 `.umap`을 포함한 Unreal Asset에는 Git LFS의 filter·diff·merge 속성이 적용되며, 현재 원격으로 보낼 추가 LFS Object는 없다.

현재 구현된 Drone 기능 기준선은 Prototype Pawn/GameMode와 Move·Altitude·Yaw·Camera 입력까지다. Take Off, Landing, Crash/실패, Mission, Enemy AI, MG 점유·공격, HUD/Evaluation은 아직 구현된 것으로 판정하지 않는다. 이전 기준 Commit `fb891fb`의 잘못된 `//test` 주석은 이력 재작성 없이 `2c38ebf`에서 제거했다.

사용자는 이 프로젝트에서 Android를 사용하지 않는다고 확정했다. 이에 따라 `Config/DefaultEngine.ini`의 Android File Server Plugin과 네트워크 연결을 끄고 `SecurityToken` 할당을 비웠다. 검사 결과 활성 Plugin 0, 네트워크 허용 0, 비어 있지 않은 토큰 0이다. 기존 토큰 값은 이 문서나 로그에 기록하지 않았다. 향후 Android File Server를 다시 켤 경우 빈 토큰은 인증 없는 상태가 될 수 있으므로 보안 설정을 새로 검토해야 한다.

`.vsconfig`를 확인한 결과 Visual Studio workload와 component ID만 있으며 자격 증명이나 개인 경로는 없다. UE가 선호한다고 표시한 14.50 계열 도구 구성도 포함해 첫 Commit에 반영했다.

## 프로젝트 빌드와 실행 점검

- 고정 추적 Camera, Mouse Drone Yaw와 Gamepad 입력을 포함해 `DroneEditor Win64 Development`를 `-NoUBTMakefiles -CompilerVersion=14.51.36256`으로 다시 빌드했고 `Result: Succeeded`였다.
- 새 Action과 BP 참조 저장 뒤 `CompileAllBlueprints` Commandlet은 `0 error(s), 0 warning(s), 0 failed to load`로 정상 종료했다.
- 기본 선택되는 MSVC 14.38은 UE 5.8 Engine PCH 컴파일 오류를 냈다. 설치된 14.51.36256을 명시하면 빌드는 성공한다. 14.51은 UE가 표시한 선호 버전 14.50.35717보다 새 버전이라는 주의 메시지가 있으므로 빌드 명령에는 명시 버전을 유지한다.
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

상세 구현과 Editor 연결 절차는 [`docs/DRONE_PROTOTYPE_IMPLEMENTATION.md`](docs/DRONE_PROTOTYPE_IMPLEMENTATION.md)에 기록했다.

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
- 구매 소스 없이 Engine 기본 도형으로 진행하는 기능 우선 Greybox 사전계획
- 전체 작업 관리 및 병행 학습 계획
- 실제 진행 상태를 담는 `WORKBOARD.md`

## 다음 단계

1. `HUD-01` Telemetry Snapshot 구현: 속도·고도·수직 속도·Heading을 10Hz Event로 제공
2. `HUD-02` 공용 Flight HUD에서 네 수치를 표시
3. 비충돌 Spline·순서형 Ring Gate·Lap/Segment 비교 UI가 있는 Tutorial Vertical Slice 구현
4. 이후 Flight 상태, Operator↔Drone, NPC·Mission UI, Jamming Story 순으로 진행
5. 병행 과제로 다른 PC Clone/LFS/UE 5.8.1 실행과 문서 Clone/Pull 확인

Camera·Mouse·Gamepad 역할은 v1 조작으로 확정했다. Keyboard·Mouse 체감은 현재 시험값으로 통과했으며 실제 Gamepad 체감, 최종 물리와 최종 감도 조정은 이후 별도 카드로 남긴다. 구매 소스와 최종 Mesh는 선행 조건이 아니며 상세 계획은 [`docs/DRONE_TUTORIAL_STORY_PLAN.md`](docs/DRONE_TUTORIAL_STORY_PLAN.md)를 따른다.

Git 공유 작업과 Drone 기능 작업은 서로를 불필요하게 막지 않고 다음 세 흐름으로 이어간다.

```text
Drone: origin/main 동기화 완료
→ 다른 PC Clone/LFS/UE 실행 검증

MD: gyeonliz/md origin 연결 완료
→ 첫 Commit과 Push 완료
→ 다른 PC Clone/Pull과 문맥 확인

PFN-06 Done
→ Telemetry Snapshot·Flight HUD
→ Tutorial Course·Timing·비교 UI
→ Take Off·Landing·Crash
→ Operator↔Drone 전환
→ NPC·Mission UI Story Shell
→ Enemy AI·MG·Jamming
→ 통합 Greybox·외부 Drone 에셋 적용
```

최종 감도, Mouse Y 반전, 비행 물리, 멀티플레이와 세부 Mission 규칙은 현재 미정으로 유지한다.
