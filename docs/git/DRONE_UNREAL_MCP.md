# Drone UE 5.8 Unreal MCP 연결 기준


현재 사용법(2026-11-05 D PC): 실제 Unreal은 `D:/JGY/project/drone`, 문서는 `D:/JGY/project/md`다. 공유 Default의 자동 시작은 False이며 현재 연결/도구 관측과 설정 파일 존재를 구분한다. 실제 사용자 증상 세션은 배정된 실행 대화 한 곳만 MCP로 읽고 종료/StopPIE/Build하지 않는다. 아래 8월·10월 실행 수치는 당시 기록이다.
현재 구성 확인: 2026-11-05 D PC (Asia/Seoul). 초기 연결 기록: 2026-08-26.

## 결론

Drone 프로젝트는 프로젝트에 등록된 Epic 공식 Experimental `Unreal MCP`를 사용한다. 현재 경로·설정·관측 결과를 우선하며 아래 공식 문서 대조/과거 빌드는 당시 확인 기록이다.

- Unreal 프로젝트: `D:\JGY\project\drone`
- MCP 주소: `http://127.0.0.1:8000/mcp`
- Codex 프로젝트 설정: `D:\JGY\project\drone\.codex\config.toml`
- Claude 클라이언트: Unreal 저장소 루트 .mcp.json
- Unreal 자동 시작 기본값: `Config/DefaultEditorPerProjectUserSettings.ini`
- 외부 네트워크 공개 금지, 같은 PC의 loopback 연결만 사용

사용자가 전달한 Unreal Engine KR 게시물은 2026-08-20 UEFN MCP 공개 소식이다. 상세 기사와 UE 5.8 문서를 대조한 결과, UEFN뿐 아니라 일반 Unreal Editor 5.8에도 `ModelContextProtocol` 플러그인이 포함되어 있고 Codex용 설정 생성이 공식 지원됨을 확인했다.

- Epic 소식: <https://www.fortnite.com/news/unreal-mcp-is-now-available-in-uefn>
- UE 5.8 공식 문서: <https://dev.epicgames.com/documentation/unreal-engine/unreal-mcp-in-unreal-editor>
- Codex MCP 공식 문서: <https://learn.chatgpt.com/docs/extend/mcp?surface=cli>

## 프로젝트 구성

`Drone.uproject`에는 다음 플러그인을 Editor Target으로만 활성화한다.

| 플러그인 | 용도 |
|---|---|
| `ModelContextProtocol` | Unreal Editor 내부 MCP HTTP 서버 |
| `EditorToolset` | Level, Actor, Asset, Blueprint, Material, Mesh, Viewport, PIE, Log 작업 |
| `AutomationTestToolset` | 자동화 테스트 탐색·실행·결과 조회 |
| `UMGToolSet` | Tutorial/Story HUD와 Widget 생성·검사 |
| `StateTreeToolset` | 기존 StateTree Asset 검사 |
| `AIModuleToolset` | 후속 Enemy AI Behavior Tree 검사 |

`AllToolsets`는 편리하지만 PCG, Niagara, GAS, Dataflow 등 현재 불필요한 Toolset까지 켜므로 사용하지 않는다. 필요한 Toolset은 실제 작업 카드가 활성화될 때 개별 추가한다.

MCP와 위 Toolset은 프로젝트의 생산 코드·게임 런타임 기능이 아니다. 모두 프로젝트 Plugin Reference의 `TargetAllowList: Editor`로 제한한다. 실제 `Drone Win64 Development` 빌드 성공으로 게임 실행 파일이 이 구성 때문에 막히지 않음을 확인했다.

Codex 설정은 다음과 같다.

```toml
[mcp_servers.unreal-mcp]
url = "http://127.0.0.1:8000/mcp"
enabled = true
required = false
startup_timeout_sec = 10
tool_timeout_sec = 120
default_tools_approval_mode = "writes"
```

읽기 호출은 바로 사용하고 변경성 Tool은 Codex의 승인을 거치도록 `writes` 정책을 쓴다. Unreal MCP는 인증 계층이 없는 Experimental 기능이므로 포트를 LAN이나 인터넷 주소에 바인딩하지 않는다.

## Unreal MCP 자동 시작과 현재 연결

현재 Git 추적 `Config/DefaultEditorPerProjectUserSettings.ini`의 `[/Script/ModelContextProtocolEngine.ModelContextProtocolSettings]`는 `bAutoStartServer=False`·`ServerPortNumber=8000`·`ServerUrlPath=/mcp`다. 10/04 문서의 공유 True 설명은 현 구성과 달라 정정한다. MCP가 필요한 PC의 선택적 사용자 설정 위치는 `Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini`의 같은 섹션이며 공유 기본값과 구분한다. 이번 작업은 설정을 변경하지 않았다.

열린 Editor에서 서버가 꺼져 있었고 사용자가 `ModelContextProtocol.StartServer`를 직접 실행한 뒤, 로컬 HTTP helper의 initialize/tools/list가 각각200으로 응답했다. endpoint는 `http://127.0.0.1:8000/mcp`, 협상 protocol은2025-11-25, 래퍼는 `list_toolsets`/`describe_toolset`/`call_tool`3개·등록 toolset23개다. 이는 기존 서버의 실제 HTTP 연결 성공이며 설치/Config 수정이나 Codex 네이티브 도구 노출 완료가 아니다. 첫 질의는 이미 FrontEnd 상태여서 앞선 하늘 시야를 관측한 결과로 쓰지 않는다. 이후 실제 TUT_Hover 증상 세션의 두 차례 읽기에서 몸체 Pitch/Roll0°·Boom 상대 Pitch+60°·Camera 상대0°·CameraManager 액터 약+60°를 관측했다. 서로 다른 RPC 시각이며 내부 최종 PCM POV·private 수동 캐시·과거 입력 delta를 읽은 결과가 아니다. 다른 Editor가 쓰는 포트/세션과 충돌하지 않도록 실행 담당 한 곳이 관리한다.

## 실제 관측 가능한 범위

ObjectTools는 노출된 Actor/Component 속성과 transform을 읽지만 현재 허용 도구에는 Controller의 private ViewTarget/입력과 PCM의 private POV/캐시를 모두 읽는 일반 호출이 없다. 임의 UFUNCTION·Unreal Python 실행, live Slate 버튼/키 입력, 정상 Editor 종료 도구도 없다. ProgrammaticToolset은 등록된 도구 조합이며 이 제한을 우회하지 않는다. UMG 저작 기능을 실행 중 버튼 클릭으로 쓰지 않는다. 실제 PC의 `playerInput` 조회는 HTTP200이어도 tool isError와 `the following properties could not be read: playerInput`으로 거부됐다. 현재 등록 ObjectTools는 Edit/Blueprint 노출 플래그가 필요한 속성만 읽으며 이 runtime 포인터는 노출되지 않았다. ActionInstanceData 조회도 성공한 것으로 쓰지 않는다. 실제 입력값·Mouse/Pad/RC·카메라 입력/과거 누적 delta는UNKNOWN이다. 원시 근거는 WORKLOG가 가리키는 InputReflectionProbe 기록이다.

PIE 중 `Asset.is_dirty`는 DoesAssetExist 제한으로 오류/존재하지 않음처럼 반환될 수 있으므로 깨끗함/파일 부재의 근거가 아니다. 전체 dirty 검색도 ExternalObjects 조회에서 중단돼 프로젝트 전체 clean을 확인한 결과가 아니다. 원시 HID 입력 수신과 PlayerInput 키 상태도 구분한다. 연결 세션 토큰/개인 로그 전문은 출력하거나 Space에 올리지 않는다. 현재 증상/실행/도구 한계의 근거는 [WORKLOG](../history/DRONE_WORKLOG.md#2026-11-05--tutorial2-실제-하늘-시야와-자동-검사-범위-정정)다.

## 연결 및 사용

1. 실제 작업 PC의 프로젝트를 사용한다. 현재 D PC는 `D:/JGY/project/drone/Drone.uproject`이며 이미 열린 사용자 증상 세션을 재시작하지 않는다.
2. 출력 로그에서 `LogModelContextProtocol: Starting MCP server on port 8000`을 확인한다.
3. 현재 배정된 실행 담당만 Unreal 도구를 사용한다. Claude 루트 `.mcp.json`, Codex 설정/네이티브 도구 노출과 로컬 HTTP helper 연결은 각각 확인하고 옛 브리지 전담 규칙을 일반 Codex 작업에 확대하지 않는다.
4. 연결된 Agent는 `list_toolsets → describe_toolset → call_tool` 순서로 필요한 Tool만 탐색한다.
5. Unreal 호출은 Game Thread에서 직렬 실행되므로 서로 겹치는 MCP 호출을 보내지 않는다.

이미 열린 Codex 작업은 실행 중 설정 파일을 추가해도 MCP Tool 목록이 자동으로 바뀌지 않을 수 있다. 그 경우 Unreal Editor를 먼저 실행한 뒤 Drone 프로젝트 루트에서 Codex 작업을 새로 열거나 재연결한다.

수동 서버 제어가 필요하면 Unreal 콘솔에서 다음 명령을 사용한다.

```text
ModelContextProtocol.StartServer
ModelContextProtocol.StopServer
ModelContextProtocol.RefreshTools
ModelContextProtocol.GenerateClientConfig Codex
```

프로젝트의 `.codex/config.toml`은 이미 작성했으므로 `GenerateClientConfig Codex`를 다시 실행하지 않는다. Epic 구현은 기존 TOML 덮어쓰기를 거부한다.

## 2026-08-25 실측 검증

- `DroneEditor Win64 Development`: 성공
- `Drone Win64 Development`: 성공
- 기존 Course/Gate 테스트의 `RerunConstructionScripts()`가 게임 타깃에도 컴파일되던 문제를 발견해 두 파일을 `WITH_EDITOR && WITH_DEV_AUTOMATION_TESTS`로 제한
- 전체 `Drone.` 자동화: 12/12 Success, 최종 Exit Code 0
- MCP Listen: `127.0.0.1:8000`, Unreal Editor PID 소유 확인
- `initialize`: HTTP 200, Session ID 발급
- `notifications/initialized`: HTTP 202
- `tools/list`: HTTP 200, `list_toolsets`, `describe_toolset`, `call_tool` 확인
- `list_toolsets`: 23개 Toolset 확인
- 실제 Editor 조회:
  - Current Level: 당시 `/Game/Drone/Tutorial/Maps/Lvl_DroneTraining`, 현재 `/Game/Drone/Maps/Lvl_DroneTraining`
  - PIE: `false`
  - Selected Actors: 0
  - Content Browser: 당시 `/Game/Drone/Prototype/Maps`, 현재 기본 선택 `/Game/Drone`
- `AutomationTestToolset.DiscoverTests`: `ready`
- `AutomationTestToolset.ListTests`의 `Drone.` 필터: 총 12개 반환
- Codex 앱 번들 `codex.exe`는 WindowsApps 실행 권한 거부로 현재 PowerShell에서 `codex mcp list`를 직접 검증하지 못함

위 12/12는 MCP 연결 당시의 검증 기록이다. 2026-08-27 당시 main `55b3ffe`에서는 전체 `Drone.` 16/16과 Blueprint 오류 0을 통과했다. Drone 루트에서 새 Codex 작업을 열 때 `unreal-mcp`가 네이티브 Tool 목록에 나타나는지와 Current Level 호출을 한 번 확인해 당시 `UE-MCP-02` 확인 절차였다(현재 카드 없음). 이 연결 작업은 실제 스피커 Loop 청감이나 TUT-04B 두 Lap 화면 확인을 대신하지 않는다.

2026-08-26 09:17 KST에는 D 드라이브 프로젝트의 새 Editor PID 9884에서 MCP 서버 시작, 23 Toolset 등록과 `127.0.0.1:8000/mcp` HTTP 응답을 다시 확인했다. 현재 작업은 문서 루트에서 시작했으므로 이 재확인도 `UE-MCP-02`의 Codex 네이티브 Tool 노출 완료로 간주하지 않는다.
