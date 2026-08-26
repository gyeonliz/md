# Drone Content 폴더 정리 기준

기준일: 2026-08-26  
Drone 기준선: `main=origin/main=2cc5d79`  
Unreal Engine: 5.8.1

## 1. 레빗홀 프로젝트에서 확인한 기준

참고한 대상은 문서가 아니라 실제 최신 프로젝트 `C:\project\Fractured\GoDownTheRabbitHole.uproject`의 Content 트리와 Config다.

- 프로젝트가 직접 제작한 Map은 `/Game/Maps`에 모여 있다.
- 시작 Map과 Editor 시작 Map은 `/Game/Maps/LobbyMap`이다.
- Blueprint는 `/Game/Blueprints/AI`, `GM`, `PM`, `WBP`처럼 역할 기준으로 나뉜다.
- 공급사 예제 Map은 무조건 중앙 Maps로 옮기지 않고 공급사 폴더에 남겨 둔다.

Drone에서는 이 중 **프로젝트가 실제로 사용하는 Map을 한 폴더에 모으는 규칙**을 적용했다. 공급사 자산 전체를 프로젝트 소유 자산처럼 섞는 방식은 적용하지 않았다.

## 2. 현재 Drone Content 구조

```text
Content/Drone/
├─ Maps/
│  ├─ Lvl_DroneTraining.umap
│  ├─ Lvl_DronePrototype.umap
│  ├─ Lvl_DronePackShowcase.umap
│  └─ Lvl_DronePackShowcase_BuiltData.uasset
├─ Prototype/
│  ├─ Blueprints/
│  ├─ Input/
│  └─ UI/
├─ Tutorial/
│  ├─ Blueprints/
│  └─ Materials/
├─ Integrations/
└─ ThirdParty/
   ├─ DronePack/
   └─ NavigationArrows/
```

Map의 현재 용도는 다음과 같다.

| Map | 용도 | 상태 |
|---|---|---|
| `Lvl_DroneTraining` | Tutorial Vertical Slice와 현재 기본 실행 Map | PIE 초기 화면·자동화 확인, 한 Lap 수동 확인 대기 |
| `Lvl_DronePrototype` | Drone Pawn·입력·Camera·Telemetry 기능 시험 | 자동화 확인 |
| `Lvl_DronePackShowcase` | 공급사 DronePack 외형 6종 비교용 정리 Map | 기술 검증 완료, Editor 최종 시각 검토 대기 |

`Lvl_DronePackShowcase`는 기존 공급사 정리본 `Map_Demo`를 프로젝트에서 사용하는 목적에 맞춰 이름과 위치를 바꾼 것이다. DronePack Mesh·Material 같은 의존 자산은 계속 `/Game/Drone/ThirdParty/DronePack`에 둔다.

## 3. 이번에 제거한 영역

Asset Registry 감사에서 중앙 제작 Map 3개가 아래 Template Root를 참조하지 않는 것을 확인한 뒤 제거했다.

```text
/Game/ThirdPerson
/Game/Variant_Combat
/Game/Variant_Platforming
/Game/Variant_SideScrolling
```

각 Template Map의 `__ExternalActors__`, `__ExternalObjects__`도 함께 제거했다. Commit `1c8f391`은 Git 감지 기준 총 599개 경로를 변경했고, 이 중 589개는 삭제, 2개는 이름·위치 변경, 2개는 새 경로 추가로 기록됐다. Git 이력에 남아 있으므로 필요하면 해당 Commit 이전 파일을 복구할 수 있다.

다음 C++ 영역은 이번에 삭제하지 않았다.

```text
Source/Drone/DroneCharacter.*
Source/Drone/DroneGameMode.*
Source/Drone/DronePlayerController.*
Source/Drone/Variant_Combat/
Source/Drone/Variant_Platforming/
Source/Drone/Variant_SideScrolling/
```

콘텐츠가 없어 현재 Drone 게임 흐름에는 사용하지 않지만, C++ 삭제는 Build.cs와 클래스 의존성까지 별도로 감사해야 하므로 후속 정리 대상으로 분리했다. 이 코드가 남아 있다는 사실은 Enemy AI MVP가 구현됐다는 뜻이 아니다.

## 4. 기본 실행 설정

현재 `Config/DefaultEngine.ini`는 다음을 사용한다.

```ini
GameDefaultMap=/Game/Drone/Maps/Lvl_DroneTraining.Lvl_DroneTraining
EditorStartupMap=/Game/Drone/Maps/Lvl_DroneTraining.Lvl_DroneTraining
GlobalDefaultGameMode=/Game/Drone/Prototype/Blueprints/BP_DronePrototypeGameMode.BP_DronePrototypeGameMode_C
```

Content Browser 기본 선택 경로는 `/Game/Drone`이다. 예전 `ThirdPersonCPP` Simple Map 경로도 중앙 Training Map으로 교체했다.

## 5. 앞으로 지킬 규칙

### Map

- 실제 프로젝트 Map은 `/Game/Drone/Maps` 한 폴더에 둔다.
- 이름은 `Lvl_역할` 형식을 사용한다.
- 임시 시험 Map도 사용 목적이 생기면 이름을 붙이고 이 폴더로 옮긴다.
- 공급사 원본 Demo를 그대로 옮기지 않는다. 실제 프로젝트에서 쓸 구성으로 정리한 사본만 중앙 Maps에 둔다.
- Map 담당자를 정하고 같은 `.umap`을 두 명이 동시에 수정하지 않는다.

### Blueprint와 자산

- 기능 소유 Blueprint는 `Prototype`, `Tutorial`, 향후 `Mission`, `AI`, `UI` 같은 기능 폴더에 둔다.
- 공급사 원본·선별 의존성은 `/Game/Drone/ThirdParty/<PackName>`에 둔다.
- 프로젝트가 공급사 자산을 조합하는 Wrapper는 `/Game/Drone/Integrations/<PackName>`에 둔다.
- `ThirdParty` 자산을 직접 수정하기보다 프로젝트 소유 Wrapper 또는 Material Instance를 만든다.

### 새 환경 Map을 이식할 때

1. 별도 Staging 프로젝트에서 원본 의존성과 누락 자산을 감사한다.
2. 공급사 Pawn·Input·GameMode·HUD를 제거한다.
3. 프로젝트에서 사용할 대표 Map 사본을 `Lvl_<EnvironmentName>`으로 정리한다.
4. 대표 Map만 `/Game/Drone/Maps`에 두고 폐쇄 의존성은 `/Game/Drone/ThirdParty/Environments/<PackName>`에 둔다.
5. Map load, Map Check, Blueprint Compile, 전체 `Drone.` 자동화, Git LFS를 확인한다.
6. Editor에서 조명·재질·스케일·충돌을 눈으로 확인한 뒤 완료 처리한다.

Battlefield·MilitaryCamp·MilitaryBase는 아직 실제 Drone 저장소에 이식되지 않았으므로 이 규칙을 적용한 것처럼 기록하지 않는다.

## 6. 이번 검증 결과

- `DroneEditor Win64 Development` Build 성공
- 중앙 Maps 3개와 Showcase BuiltData 로드 성공
- 삭제한 Template Root와 이전 Map 경로 잔존 0
- Blueprint Compile `0 errors / 0 warnings / 0 failed loads`
- 전체 `Drone.` 자동화 `15/15` 성공
- 중앙 Map 4개 Git LFS 속성 확인
- `git lfs fsck`, `git diff --check` 통과
- `main=origin/main=2cc5d79`, 작업 트리 Clean
