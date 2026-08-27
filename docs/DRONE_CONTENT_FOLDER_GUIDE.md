# Drone Content 폴더 정리 기준

기준일: 2026-08-27
Drone 기준선: `main=origin/main=eeb4354`
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
│  ├─ Lvl_NPCSmartObjectGreybox.umap
│  ├─ Lvl_DronePackShowcase.umap
│  ├─ Lvl_DronePackShowcase_BuiltData.uasset
│  ├─ Lvl_Battlefield.umap
│  ├─ Lvl_MilitaryCamp.umap
│  ├─ Lvl_MilitaryBase.umap
│  └─ Lvl_OilRig.umap
├─ Prototype/
│  ├─ Blueprints/
│  ├─ Input/
│  └─ UI/
├─ Tutorial/
│  ├─ Blueprints/
│  └─ Materials/
├─ Integrations/
└─ ThirdParty/
   ├─ ArmyVFX/
   ├─ DronePack/
   ├─ GroundDroneKit/
   ├─ InfantrySFX/
   ├─ ModularInsurgents/
   ├─ ModularSoldier/
   ├─ NavigationArrows/
   ├─ OilRig/
   └─ RawDrones/

Content/
├─ Battlefield/       # Battlefield 맵의 공급사 의존성
├─ FC_MilitaryCamp/   # MilitaryCamp 맵의 공급사 의존성
└─ MillitaryBase/     # MilitaryBase 맵의 공급사 의존성(원본 철자 유지)
```

Map의 현재 용도는 다음과 같다.

| Map | 용도 | 상태 |
|---|---|---|
| `Lvl_DroneTraining` | Tutorial Vertical Slice와 현재 기본 실행 Map | PIE 초기 화면·자동화 확인, 한 Lap 수동 확인 대기 |
| `Lvl_DronePrototype` | Drone Pawn·입력·Camera·Telemetry 기능 시험 | 자동화 확인 |
| `Lvl_NPCSmartObjectGreybox` | 적·아군 NPC와 Smart Object·NavMesh 기능 시험 | 역할 BP·NPC 4명·Station 10개·NavMesh 투영 자동 검증 완료, 실제 이동은 미구현 |
| `Lvl_DronePackShowcase` | 공급사 DronePack 외형 6종 비교용 정리 Map | 기술 검증 완료, Editor 최종 시각 검토 대기 |
| `Lvl_Battlefield` | 넓은 Battlefield 환경 후보 | 실제 로드·의존성 검증 완료, 공급 자산 Map Check 메시지 14건·시각 검토 대기 |
| `Lvl_MilitaryCamp` | 군사 캠프 환경 후보 | 실제 로드·Map Check 0/0, 시각 검토 대기 |
| `Lvl_MilitaryBase` | 군사 기지 환경 후보 | 실제 로드·Map Check 0/0, 시각 검토 대기 |
| `Lvl_OilRig` | 해상 시설 환경 후보 | 실제 로드·의존성 0/0 확인, 대형 Map 수동 Map Check·시각·성능 검토 대기 |

`Lvl_DronePackShowcase`는 기존 공급사 정리본 `Map_Demo`를 프로젝트에서 사용하는 목적에 맞춰 이름과 위치를 바꾼 것이다. DronePack Mesh·Material 같은 의존 자산은 계속 `/Game/Drone/ThirdParty/DronePack`에 둔다.

환경 맵은 프로젝트가 선택한 중앙 사본만 `/Game/Drone/Maps`에 둔다. 공급사 내부 참조를 수천 개 일괄 재작성하는 위험을 피하기 위해 의존성은 공급사 경로를 유지했다. 이는 "프로젝트 사용 맵은 중앙화하되 공급사 자산은 원래 경계에 둔다"는 RabbitHole 참고 원칙과 맞는다.

## 3. 기본 템플릿 정리 범위와 교정 기록

삭제 대상은 Unreal 프로젝트 생성 때 들어온 아래 기본 Map 4개와 그 Map 전용 ExternalActors/ExternalObjects다.

```text
/Game/ThirdPerson/Lvl_ThirdPerson
/Game/Variant_Combat/Lvl_Combat
/Game/Variant_Platforming/Lvl_Platforming
/Game/Variant_SideScrolling/Lvl_SideScrolling
```

`1c8f391`에서 위 네 Content Root 전체를 제거한 것은 사용자 의도보다 넓은 삭제였다. `909f6a3`에서 Blueprint·Material 등 비맵 자산 62개를 복구했고, 기본 Map 4개만 삭제 상태로 유지했다. 현재 Asset Registry 기준 복구 수는 ThirdPerson 4, Combat 30, Platforming 10, SideScrolling 18이다.

다음 C++ 영역은 이번에 삭제하지 않았다.

```text
Source/Drone/DroneCharacter.*
Source/Drone/DroneGameMode.*
Source/Drone/DronePlayerController.*
Source/Drone/Variant_Combat/
Source/Drone/Variant_Platforming/
Source/Drone/Variant_SideScrolling/
```

대응 Content도 복구되어 참고할 수 있지만 현재 Drone Tutorial 실행 흐름이 직접 사용하는 영역은 아니다. C++ 삭제는 Build.cs와 클래스 의존성까지 별도로 감사해야 하므로 후속 정리 대상으로 분리했다. 이 코드와 Template Content가 남아 있다는 사실은 Enemy AI MVP가 구현됐다는 뜻이 아니다.

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
- 새로 선별하는 소형 공급사 자산은 기본적으로 `/Game/Drone/ThirdParty/<PackName>`에 둔다.
- 프로젝트가 공급사 자산을 조합하는 Wrapper는 `/Game/Drone/Integrations/<PackName>`에 둔다.
- `ThirdParty` 자산을 직접 수정하기보다 프로젝트 소유 Wrapper 또는 Material Instance를 만든다.
- 대형 환경 팩처럼 내부 패키지 경로가 넓게 얽힌 경우에는 검증된 정확한 의존성 폐쇄만 공급사 Root 그대로 보존하고, 중앙 Map만 프로젝트 소유 경로에 둔다.

### 새 환경 Map을 이식할 때

1. 별도 Staging 프로젝트에서 원본 의존성과 누락 자산을 감사한다.
2. 공급사 Pawn·Input·GameMode·HUD를 제거한다.
3. 프로젝트에서 사용할 대표 Map 사본을 `Lvl_<EnvironmentName>`으로 정리한다.
4. 대표 Map만 `/Game/Drone/Maps`에 두고, 의존성 경로 변경 위험을 평가해 소형 팩은 `ThirdParty`, 대형 팩은 검증된 공급사 Root를 유지한다.
5. Map load, Map Check, Blueprint Compile, 전체 `Drone.` 자동화, Git LFS를 확인한다.
6. Editor에서 조명·재질·스케일·충돌을 눈으로 확인한 뒤 완료 처리한다.

Battlefield·MilitaryCamp·MilitaryBase와 OilRig은 이 절차로 실제 이식했다. 기술 검증은 통과했지만 Editor 화면에서 조명·재질·스케일·충돌을 직접 보는 수동 검토는 아직이므로 최종 채택 Map으로 확정하지 않는다. OilRig의 명령줄 Map Check는 맵 Construction이 장시간 끝나지 않아 별도 수동 확인으로 남겼다.

## 6. 이번 검증 결과

- `DroneEditor Win64 Development` Build 성공
- 중앙 Maps 8개와 Showcase BuiltData 로드 성공
- 기본 Template Map 4개와 이전 프로젝트 Map 경로 잔존 0
- Template 비맵 자산 62개 복구 확인
- 환경 의존성: Battlefield 710, MilitaryCamp 593, MilitaryBase 1,414개 공급사 자산; 누락 0, 허용 외 경로 0
- Blueprint Compile 오류 0. 기존 Battlefield Pose GUID와 MCP 고지 경고는 유지
- AI-NPC-01 반영 뒤 전체 `Drone.` 자동화 `20/20` 성공(기존 PIE NavMesh 경고 포함 성공 1)
- 환경 Map Check: Battlefield 오류 0·공급 Blueprint 메시지 14, MilitaryCamp 0/0, MilitaryBase 0/0
- 신규 환경 패키지 2,723개·16.96 GiB 전부 Git LFS 포인터 확인
- `git lfs fsck`, `git diff --check` 통과
- 현재 기능 커밋: AI-NPC-01 `362edaa`; main 병합 `eeb4354` Push 완료
