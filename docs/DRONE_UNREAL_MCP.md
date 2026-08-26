# Drone UE 5.8 Unreal MCP 연결 기준

기준일: 2026-08-26 (Asia/Seoul)

## 결론

Drone 프로젝트는 자체 통신 플러그인 대신 UE 5.8.1에 포함된 Epic 공식 Experimental `Unreal MCP`를 사용한다.

- Unreal 프로젝트: `D:\JGY\project\drone`
- MCP 주소: `http://127.0.0.1:8000/mcp`
- Codex 프로젝트 설정: `D:\JGY\project\drone\.codex\config.toml`
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

## 연결 및 사용

1. `D:\JGY\project\drone\Drone.uproject`를 UE 5.8.1로 연다.
2. 출력 로그에서 `LogModelContextProtocol: Starting MCP server on port 8000`을 확인한다.
3. Codex 작업을 `D:\JGY\project\drone` 프로젝트 루트에서 연다.
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

위 12/12는 MCP 연결 당시의 검증 기록이다. 현재 Source 기준선 `2cc5d79`에서는 전체 `Drone.` 15/15와 Blueprint 0/0/0을 통과했다. Drone 루트에서 새 Codex 작업을 열 때 `unreal-mcp`가 네이티브 Tool 목록에 나타나는지와 Current Level 호출을 한 번 확인해 `UE-MCP-02`를 닫는다. 이 연결 작업은 `AST-01`의 실제 스피커 Loop 청감 확인을 대신하지 않으며, 다음 기능 카드는 `TUT-04 이전 기록 비교·Best·결과 UI`다.

2026-08-26 09:17 KST에는 D 드라이브 프로젝트의 새 Editor PID 9884에서 MCP 서버 시작, 23 Toolset 등록과 `127.0.0.1:8000/mcp` HTTP 응답을 다시 확인했다. 현재 작업은 문서 루트에서 시작했으므로 이 재확인도 `UE-MCP-02`의 Codex 네이티브 Tool 노출 완료로 간주하지 않는다.
