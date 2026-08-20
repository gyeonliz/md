# 현재 작업 상태

기준일: 2026-08-21 (Asia/Seoul)

이 문서는 명령으로 확인된 작업컴 상태와 사용자가 아직 결정하지 않은 항목을 분리한다.

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
| Unreal 프로젝트 저장소 | `C:\project\Drone`, `main`=`origin/main`=`91498b7`, 작업 트리 깨끗함 |
| 문서 작업 저장소 | 현재 폴더의 `origin`을 `https://github.com/gyeonliz/md.git`로 연결, 첫 Commit 전 |

GitHub CLI는 필수 구성요소는 아니다. 자동 설치를 한 번 시도했으나 Windows Installer가 종료 코드 1602로 취소되어 설치되지 않았다. GitHub 웹과 Git Credential Manager만으로도 기본 Push/Clone 작업은 가능하다.

전역 Git 작성자 정보는 `gyeonliz <jkw6483@gmail.com>`으로 설정되어 있다. Unreal 프로젝트는 GitHub Desktop과 `https://github.com/gyeonliz/drone.git`에 연결되어 첫 Commit과 Push를 완료했다. 문서 작업 폴더는 `https://github.com/gyeonliz/md.git`를 `origin`으로 연결했지만 아직 Stage·Commit·Push하지 않았다. 작업컴 기본 PowerShell 정책은 `.ps1` 직접 실행을 차단하므로 컨텍스트 도구 검증에는 영구 설정 변경 없이 실행 1회에만 `-ExecutionPolicy Bypass`를 적용했다.

## 이번 작업에서 진행한 Drone 프로젝트

추가 검색에서 다음 프로젝트를 찾았다.

```text
C:\project\Drone\Drone.uproject
```

확인 결과:

- 실행 로그 기준 UE 5.8.1 (`Release-5.8`, Changelist 56057345)
- Runtime 모듈 이름은 `Drone`
- 현재 기존 내용은 UE Third Person C++ 템플릿과 Variant 예제 중심
- `StateTree`, `GameplayStateTree` Plugin이 활성화되어 있음
- 시작 시 Git 저장소가 아니었음
- 작업 시작 시 Content에는 `.uasset` 749개와 `.umap` 4개가 있었음

사용자의 계속 진행 지시에 따라 이 경로를 현재 작업 대상으로 사용했다. 기존 Third Person 기본 맵과 전역 기본 GameMode는 유지하면서 Git 준비, Android 제외 설정, 별도 Drone Prototype Source를 적용했다.

- `main` Branch의 로컬 Git 저장소 초기화
- 프로젝트 로컬 Git LFS 초기화
- Unreal `.gitignore`와 `.gitattributes` 적용
- 생성 폴더 제외 및 `.uasset`/`.umap` LFS 속성 확인
- `.sln`과 UE 5.8의 `.slnx` 생성 파일 제외 확인
- Android File Server Plugin과 네트워크 사용 비활성화
- Android File Server `SecurityToken` 빈 할당 확인
- 별도 `ADronePrototypePawn`과 `ADronePrototypeGameMode` 추가
- 구조 및 Spawn/Possess 자동화 테스트 2개 추가
- Prototype 전용 임시 입력 계약에 키·Value Type·Modifier·기대 부호 기록
- Input Action 4개와 `IMC_DronePrototype` 생성
- `BP_DronePrototypePawn`에 IMC·네 Action·Engine Cube Placeholder 연결
- `BP_DronePrototypeGameMode`의 Default Pawn을 BP Prototype Pawn으로 연결
- 별도 `Lvl_DronePrototype` Greybox Map과 GameMode Override 구성
- 863개 파일을 `91498b7` (`chore: initialize Drone project`)로 첫 Commit
- GitHub `gyeonliz/drone`의 `origin/main`에 Push
- 현재 로컬 `main`과 `origin/main` 일치, Staged·Unstaged 변경 없음

첫 Commit은 863개 파일이며 `Content`는 761개로 `.uasset` 756개와 `.umap` 5개다. 가장 큰 파일은 약 21.0 MB이고 100 MB를 넘는 파일은 없다. 새 Prototype `.uasset`과 `.umap`을 포함한 Unreal Asset에는 Git LFS의 filter·diff·merge 속성이 적용되며, 현재 원격으로 보낼 추가 LFS Object는 없다.

사용자는 이 프로젝트에서 Android를 사용하지 않는다고 확정했다. 이에 따라 `Config/DefaultEngine.ini`의 Android File Server Plugin과 네트워크 연결을 끄고 `SecurityToken` 할당을 비웠다. 검사 결과 활성 Plugin 0, 네트워크 허용 0, 비어 있지 않은 토큰 0이다. 기존 토큰 값은 이 문서나 로그에 기록하지 않았다. 향후 Android File Server를 다시 켤 경우 빈 토큰은 인증 없는 상태가 될 수 있으므로 보안 설정을 새로 검토해야 한다.

`.vsconfig`를 확인한 결과 Visual Studio workload와 component ID만 있으며 자격 증명이나 개인 경로는 없다. UE가 선호한다고 표시한 14.50 계열 도구 구성도 포함해 첫 Commit에 반영했다.

## 프로젝트 빌드와 실행 점검

- Prototype 최종 변경 뒤 `DroneEditor Win64 Development`를 `-NoUBTMakefiles`로 다시 빌드했고 `Result: Succeeded`였다. 새 테스트 Source도 빌드 대상에 포함됨을 확인했다.
- `CompileAllBlueprints` Commandlet은 종료 코드 0, `0 error(s), 0 warning(s)`로 정상 종료했다. 검사 당시 자산에 의도하지 않은 저장 변경이 생기지 않았음을 확인했다.
- 설치된 MSVC 14.51.36252는 UE가 표시한 최신 선호 버전 14.50.35717보다 새 버전이라, UnrealBuildTool이 충분히 검증되지 않았다는 주의 메시지를 냈다. 현재 빌드 실패는 아니지만 이후 컴파일 문제가 생기면 먼저 확인한다.
- `Drone.Prototype.PawnDefaults`와 `Drone.Prototype.SpawnPossess` 자동화 테스트를 실행했다. Report 기준 2 succeeded, 0 warnings, 0 errors, 0 failed이고 프로세스 종료 코드도 0이다.
- 기존 `Lvl_ThirdPerson`을 저장 변경하지 않고 명령줄 URL로 `DronePrototypeGameMode`만 Override했다. GameMode 로드, `DronePrototypePawn` Spawn/Possess, 정상 종료를 확인했고 프로젝트 코드 Fatal/Error는 없었다.
- native Prototype Pawn CDO의 Mesh·IMC·네 Input Action 기본값은 계속 `null`이다. 실제 Prototype Map은 BP 자식에 자산과 Engine Cube를 배정하고 BP GameMode가 그 BP Pawn을 Spawn하도록 분리했다.
- 자산 Create 실행에서 `CREATED_OK`와 동일 프로세스 `VALIDATION_OK`를 확인했다. 첫 별도 프로세스 검증은 Map을 generic asset으로도 강참조한 검증 스크립트 결함을 발견해 실패했으며, Map을 `LevelEditorSubsystem`으로만 여는 방식으로 수정했다. 수정 뒤 새 프로세스 재로드 검증은 `VALIDATION_OK`, Map Check 0 errors, 0 warnings로 통과했다.
- 새 자산 생성 뒤 `CompileAllBlueprints`는 종료 코드 0, 0 errors, 0 warnings였다. 전용 Map 헤드리스 Smoke Test에서도 BP GameMode와 BP Pawn Spawn/Possess, Enhanced Input Subsystem 초기화, 정상 종료 코드 0을 확인했다.
- GUI PIE 첫 실행에서 `IMC_DronePrototype` 한 개가 Priority 1로 등록된 상태와 Move·Altitude·Yaw·Look Callback 계열의 실제 동작을 확인했다. W와 A/D, Space/Left Ctrl, E/Q, Mouse Look은 기대 방향으로 동작했지만 `S`와 복합·중복 조건을 끝내지 못했다.
- 두 번째 PIE는 Pawn Spawn/Possess·IMC 한 개·Move까지 확인했지만, 사용자가 다른 앱을 직접 조작하는 것을 감지해 키 입력 충돌 방지를 위해 중단했다. 어느 실행도 전체 체크리스트를 끝내지 못했으므로 PFN-06은 0/3 Pass이며 새 PIE 3회 전체 반복이 남았다.
- 과거 전체 Editor 무창 점검 한 번은 `Quit` 뒤 프로세스가 종료되지 않아 해당 테스트 프로세스만 종료했다. 이번 Automation `Quit` 경로와 Prototype 게임 실행은 모두 종료 코드 0으로 정상 종료했다.
- 과거 로그의 `LogAutomationTest: Error: Condition failed` 15줄은 UE 내부 `UE::UnifiedErrorTest` 출력 직후, 프로젝트 맵 로드 전에 발생했다. 이번 Prototype Report에는 warning/error가 없다.
- 2026-08-21 재확인 시 Unreal Editor와 UnrealEditor-Cmd 프로세스는 실행 중이지 않았다.
- PFN-06용 포커스 없는 PIE 입력 반복 테스트 초안은 문서 작업 폴더의 `tools/unreal/templates`에 준비했지만 실제 Drone Source에는 아직 적용·컴파일·실행하지 않았다.

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
- 격리된 `APawn` 기반 Drone Prototype, native GameMode, 자동화 테스트 2개
- 최종 빌드, 구조 테스트, Spawn/Possess 테스트, 헤드리스 게임 실행 검증
- Prototype Input Action·IMC·BP Pawn/GameMode·전용 Greybox Map 생성 도구와 재검증 도구
- GUI PIE 1회차의 실제 Move·Altitude·Yaw·Look 입력 검증
- 구매 소스 없이 Engine 기본 도형으로 진행하는 기능 우선 Greybox 사전계획
- 전체 작업 관리 및 병행 학습 계획
- 실제 진행 상태를 담는 `WORKBOARD.md`

## 다음 단계에 필요한 확인

1. `gyeonliz/md`에 올릴 첫 Stage 파일 범위 검토
2. 문서 저장소 Stage·Commit·Push 각각의 실행 승인
3. 다른 PC에서 `gyeonliz/drone` Clone, LFS 다운로드, UE 5.8.1 실행 확인
4. 다른 PC에서 `gyeonliz/md` Clone 또는 Pull 후 현재 문맥 확인

Prototype 시험용 임시 입력은 이미 기록하고 적용했다. 최종 키·감도·Mouse Y 반전 기본값은 여전히 미정이지만 PFN-06 재검증의 선행 결정은 아니다. 구매 소스와 최종 Mesh도 현재 단계의 선행 조건이 아니다. 기본 도형으로 Flight·Mission·Enemy AI·Turret·Evaluation Greybox를 먼저 검증한다.

Git 공유 작업과 Drone 기능 작업은 서로를 불필요하게 막지 않고 다음 세 흐름으로 이어간다.

```text
Drone: origin/main 동기화 완료
→ 다른 PC Clone/LFS/UE 실행 검증

MD: gyeonliz/md origin 연결 완료
→ Stage 범위 검토
→ 승인된 첫 Commit과 Push
→ 다른 PC Clone/Pull과 문맥 확인

PFN-06 새 PIE 3회 전체 검증
→ 각 실행에서 Spawn/Possess·IMC·모든 매핑·중복 없음 확인
→ Take Off/Landing/Crash 기능을 각각 구현
→ 구매 소스 없이 Greybox Vertical Slice 완성
```

세부 입력 방식, 최종 물리 시스템, 멀티플레이, 최종 게임 규칙 등은 계속 미정으로 유지한다.
