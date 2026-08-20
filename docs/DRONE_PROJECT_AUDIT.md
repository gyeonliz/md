# Drone Unreal 프로젝트 읽기 전용 감사

> 이 문서는 Prototype 구현 전의 읽기 전용 스냅샷이다. 이후 추가한 C++ Prototype과 검증 결과는 [`DRONE_PROTOTYPE_IMPLEMENTATION.md`](DRONE_PROTOTYPE_IMPLEMENTATION.md)에 기록한다.

## 1. 감사 범위와 안전 기준

- 감사 대상: `C:\project\Drone`
- 감사 방식: 읽기 전용
- 확인 대상: `.uproject`, `Source`, 필요한 `Config` 키, `Content` 파일명
- 작성 대상: 이 도구 저장소의 `docs/DRONE_PROJECT_AUDIT.md`
- 감사 중 `C:\project\Drone`의 파일은 수정하지 않았다.
- `Content`의 `.uasset`/`.umap` 내부는 열거나 해석하지 않고 파일명과 경로만 조사했다.
- `Config\DefaultEngine.ini`에 `SecurityToken` 키가 존재하는 사실만 확인했다. 값은 읽거나 이 문서에 기록하지 않았다.

이 문서는 2026-08-19에 관찰한 파일 상태를 기록한다. Blueprint 내부 부모 클래스, Default Pawn, 컴포넌트 값 등은 Content 파일명만으로 확정하지 않는다.

## 2. 핵심 결론

1. 현재 기본 실행 경로는 드론 전용 맵이 아니라 `Lvl_ThirdPerson`과 `BP_ThirdPersonGameMode`다.
2. 핵심 C++ 타입인 `ADroneCharacter`, `ADroneGameMode`, `ADronePlayerController`는 모두 `abstract`이며 Third Person 템플릿 구조를 가진다.
3. `ADroneCharacter`는 `ACharacter` 기반으로 Capsule, Character Movement, Jump, 보행 이동, SpringArm/Follow Camera를 사용한다.
4. Enhanced Input 모듈·입력 클래스·Input Action/Mapping Context 자산은 이미 존재한다.
5. Combat, Platforming, Side Scrolling Variant의 C++와 Content가 그대로 남아 있다.
6. 조사한 Source와 Content 파일명에서는 드론 전용 Pawn, 드론 비행, Take Off, Altitude를 나타내는 전용 클래스/자산을 확인하지 못했다. 다만 Blueprint 내부는 조사하지 않았으므로 Blueprint에 해당 로직이 없다고 단정할 수는 없다.
7. 첫 스파이크는 기존 Third Person 경로를 삭제하거나 즉시 교체하기보다 별도 Prototype 클래스·맵·GameMode로 격리해 비교하는 편이 안전하다.

## 3. 프로젝트 및 엔진 설정

### 프로젝트 Descriptor

`Drone.uproject`에서 확인한 사실은 다음과 같다.

- FileVersion: `3`
- Runtime 모듈: `Drone`
- LoadingPhase: `Default`
- AdditionalDependencies: `Engine`, `AIModule`, `UMG`
- EngineAssociation: 사람이 읽을 수 있는 버전 문자열이 아니라 GUID

`Drone.Target.cs`와 `DroneEditor.Target.cs`에는 다음이 지정되어 있다.

- `DefaultBuildSettings = BuildSettingsVersion.V7`
- `IncludeOrderVersion = EngineIncludeOrderVersion.Unreal5_8`
- Game/Editor Target 모두 `Drone` 모듈 사용

현재 기준 컨텍스트의 엔진 버전은 UE 5.8.1이다. 파일 감사만으로는 `.uproject`의 GUID가 가리키는 패치 버전까지 독립적으로 확인할 수 없지만, Target 파일은 Unreal 5.8 Include Order를 명시한다.

### 명시적으로 활성화된 Plugin

`Drone.uproject`에 명시된 Plugin은 다음 세 개다.

| Plugin | Enabled | 범위 |
|---|---:|---|
| ModelingToolsEditorMode | true | Editor만 허용 |
| StateTree | true | 별도 제한 없음 |
| GameplayStateTree | true | 별도 제한 없음 |

이는 `.uproject`에 명시적으로 활성화된 목록이다. 엔진 기본값으로 로드되는 다른 Plugin의 활성 여부까지 뜻하지 않는다.

### 빌드 모듈 의존성

`Source\Drone\Drone.Build.cs`의 Public Dependency는 다음과 같다.

- `Core`
- `CoreUObject`
- `Engine`
- `InputCore`
- `EnhancedInput`
- `AIModule`
- `StateTreeModule`
- `GameplayStateTreeModule`
- `UMG`
- `Slate`

Enhanced Input, AI, StateTree, UMG를 사용할 빌드 기반은 이미 들어 있다. 이것이 드론 기능이나 적 AI 기능이 이미 구현되었다는 뜻은 아니다.

## 4. 현재 기본 맵과 GameMode

`Config\DefaultEngine.ini`에서 선택적으로 확인한 안전한 키는 다음과 같다.

| 키 | 현재 값 |
|---|---|
| GameDefaultMap | `/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson` |
| EditorStartupMap | `/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson` |
| GlobalDefaultGameMode | `/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode.BP_ThirdPersonGameMode_C` |
| DefaultGraphicsRHI | `DefaultGraphicsRHI_DX12` |

관련 Content 파일명도 존재한다.

- `Content\ThirdPerson\Lvl_ThirdPerson.umap`
- `Content\ThirdPerson\Blueprints\BP_ThirdPersonGameMode.uasset`
- `Content\ThirdPerson\Blueprints\BP_ThirdPersonCharacter.uasset`
- `Content\ThirdPerson\Blueprints\BP_ThirdPersonPlayerController.uasset`
- `Content\ThirdPerson\MI_ThirdPersonColWay.uasset`

Blueprint 내부를 읽지 않았으므로 `BP_ThirdPersonGameMode`에 지정된 Default Pawn과 Player Controller 클래스는 이번 감사에서 확정하지 않는다. 이름과 C++ 주석은 템플릿 관계를 강하게 시사하지만, 실제 부모/속성은 Editor에서 별도로 확인해야 한다.

## 5. 현재 핵심 C++ 구조

### 모듈

- `Drone.cpp`: `FDefaultGameModuleImpl`로 `Drone` 기본 게임 모듈 등록
- `Drone.h`: 공용 로그 카테고리 `LogDrone` 선언

### 기본 Third Person 계열

| 타입 | 기반 타입 | 현재 확인한 책임 |
|---|---|---|
| `ADroneCharacter` | `ACharacter` | Capsule, Character Movement, Jump, Move/Look, SpringArm, Follow Camera, Input Action 바인딩 |
| `ADroneGameMode` | `AGameModeBase` | 생성자 외 별도 로직이 없는 abstract GameMode 골격 |
| `ADronePlayerController` | `APlayerController` | Mapping Context 배열 등록, 모바일 제외 Context, 터치 UI 생성 |

세 타입 모두 `UCLASS(abstract)`다. 실제 실행에는 구체 Blueprint 자식 또는 다른 구체 클래스가 필요하다.

`ADroneCharacter`에서 확인한 구체 상태는 다음과 같다.

- Capsule 크기 설정
- `bOrientRotationToMovement = true`
- Walking/Falling 관련 Character Movement 값 설정
- Jump 시작/종료 처리
- Controller Yaw 기준 전후/좌우 보행 이동
- Controller Yaw/Pitch Look 처리
- `JumpAction`, `MoveAction`, `LookAction`, `MouseLookAction` 참조

따라서 현재 C++ 기본 조종 클래스는 이름에 Drone이 들어가지만 동작 구조는 Third Person 보행 Character다. 이것이 최종 드론 클래스가 `Pawn`이어야 한다는 결론은 아니다.

### Combat Variant

현재 파일에서 확인한 C++ 타입을 책임별로 묶으면 다음과 같다.

- 플레이: `ACombatCharacter`, `ACombatGameMode`, `ACombatPlayerController`
- AI: `ACombatAIController`, `ACombatEnemy`, `ACombatEnemySpawner`
- EQS Context: `UEnvQueryContext_Danger`, `UEnvQueryContext_Player`
- Animation Notify: `UAnimNotify_CheckChargedAttack`, `UAnimNotify_CheckCombo`, `UAnimNotify_DoAttackTrace`
- Gameplay Actor: `ACombatActivationVolume`, `ACombatCheckpointVolume`, `ACombatDamageableBox`, `ACombatDummy`, `ACombatLavaFloor`
- Interface: `UCombatActivatable`, `UCombatAttacker`, `UCombatDamageable`와 대응 C++ interface
- UI: `UCombatLifeBar`
- StateTree 지원: `CombatStateTreeUtility.h/.cpp`

### Platforming Variant

- `APlatformingCharacter`
- `APlatformingGameMode`
- `APlatformingPlayerController`
- `UAnimNotify_EndDash`

### Side Scrolling Variant

- 플레이: `ASideScrollingCharacter`, `ASideScrollingGameMode`, `ASideScrollingPlayerController`, `ASideScrollingCameraManager`
- AI: `ASideScrollingAIController`, `ASideScrollingNPC`
- Gameplay Actor: `ASideScrollingJumpPad`, `ASideScrollingMovingPlatform`, `ASideScrollingPickup`, `ASideScrollingSoftPlatform`
- Interface/UI: `USideScrollingInteractable`과 대응 C++ interface, `USideScrollingUI`
- StateTree 지원: `SideScrollingStateTreeUtility.h/.cpp`

이번 감사에서 조사한 `.h`, `.cpp`, `.cs` 87개는 모두 Epic Games 저작권 헤더를 갖고 있다. 클래스명, 디렉터리, Content 구성과 함께 보면 현재 Source는 Unreal 템플릿 및 Variant 구조가 중심이라고 판단할 수 있다. 이는 파일 근거에 따른 판단이며, 누가 어떤 파일을 실제로 편집했는지에 대한 판단은 아니다.

## 6. Enhanced Input 현황

### Config

`Config\DefaultInput.ini`에서 확인한 사실은 다음과 같다.

- `DefaultPlayerInputClass=/Script/EnhancedInput.EnhancedPlayerInput`
- `DefaultInputComponentClass=/Script/EnhancedInput.EnhancedInputComponent`
- `DefaultTouchInterface=None`
- 레거시 `ActionMappings`/`AxisMappings` 항목은 선택 검색 결과에서 확인되지 않음

### C++

- `Drone.Build.cs`가 `EnhancedInput` 모듈에 의존한다.
- `ADroneCharacter::SetupPlayerInputComponent`는 `UEnhancedInputComponent`로 Action을 바인딩한다.
- `ADronePlayerController::SetupInputComponent`는 Local Player의 `UEnhancedInputLocalPlayerSubsystem`에 `DefaultMappingContexts`를 Priority 0으로 추가한다.
- 터치 조작을 사용하지 않을 때 `MobileExcludedMappingContexts`도 Priority 0으로 추가한다.
- Mapping Context 배열과 Action 참조는 `EditAnywhere`이므로 구체 Blueprint 설정이 필요하다.

### 확인된 기본 Input Asset 파일명

- `Content\Input\Actions\IA_Jump.uasset`
- `Content\Input\Actions\IA_Look.uasset`
- `Content\Input\Actions\IA_MouseLook.uasset`
- `Content\Input\Actions\IA_Move.uasset`
- `Content\Input\IMC_Default.uasset`
- `Content\Input\IMC_MouseLook.uasset`
- `Content\Input\Touch\BPI_TouchInterface.uasset`
- `Content\Input\Touch\UI_Thumbstick.uasset`
- `Content\Input\Touch\UI_TouchSimple.uasset`

Variant별 Input 파일명도 남아 있다.

- Combat: `IA_ChargedAttack`, `IA_ComboAttack`, `IA_ToggleCameraSide`, `IMC_Combat` 및 Touch UI/BPI
- Platforming: `IA_Dash`, `IMC_Platforming` 및 Touch UI/BPI
- Side Scrolling: `IA_Drop`, `IA_Interact`, `IA_Mover`, `IMC_SideScroller` 및 Touch UI/BPI

Content 내부를 읽지 않았기 때문에 IMC별 실제 키, Trigger, Modifier, 각 Blueprint의 Action/Context 할당 상태는 현재 미확인이다. 최종 드론 입력 키도 현재 미정이다.

## 7. Content 파일명 기준 구조

총 753개 파일이 확인되었다.

- `.uasset`: 749개
- `.umap`: 4개

최상위 폴더별 파일 수는 다음과 같다.

| 폴더 | 파일 수 |
|---|---:|
| `__ExternalActors__` | 479 |
| `__ExternalObjects__` | 42 |
| `Characters` | 128 |
| `Input` | 9 |
| `LevelPrototyping` | 29 |
| `ThirdPerson` | 5 |
| `Variant_Combat` | 31 |
| `Variant_Platforming` | 11 |
| `Variant_SideScrolling` | 19 |

확인된 Map 파일명은 다음 네 개다.

- `Content\ThirdPerson\Lvl_ThirdPerson.umap`
- `Content\Variant_Combat\Lvl_Combat.umap`
- `Content\Variant_Platforming\Lvl_Platforming.umap`
- `Content\Variant_SideScrolling\Lvl_SideScrolling.umap`

파일명에 `Drone`이 들어가는 Content 파일은 확인되지 않았다. 다만 Asset 이름이 기능을 항상 완전하게 설명하는 것은 아니므로, 이것만으로 드론 관련 Blueprint 로직의 부재를 확정하지 않는다.

`__ExternalActors__`와 `__ExternalObjects__`에는 `Lvl_ThirdPerson` 및 Variant Map과 연결된 파일이 다수 존재한다. 이 파일들은 Map과 함께 관리해야 하며 임의로 개별 삭제하거나 이름을 바꾸지 않는다.

## 8. UE 템플릿 잔존 구조

다음 항목은 파일로 직접 확인한 템플릿 잔존 근거다.

- 기본 Map/GameMode 경로가 `/Game/ThirdPerson`을 가리킴
- `ADroneCharacter`의 주석과 구현이 simple third person character를 설명함
- Jump, Walking/Falling 감속, Orient Rotation to Movement가 설정됨
- `BP_ThirdPersonCharacter`, `BP_ThirdPersonGameMode`, `BP_ThirdPersonPlayerController` 파일 존재
- Combat, Platforming, Side Scrolling Variant의 C++·Map·Blueprint·Input 폴더 존재
- `Characters`, `LevelPrototyping` 콘텐츠 폴더 존재
- Source 코드 파일 87개 모두 Epic Games 저작권 헤더 포함

따라서 첫 Drone Prototype은 템플릿 제거 작업과 섞지 않는 것을 권장한다. Variant 정리 여부는 새 조종 클래스와 맵이 정상 작동한 뒤 별도 작업으로 판단한다. 현재 감사만으로 어떤 Variant가 불필요하다고 확정하거나 삭제하지 않는다.

## 9. 첫 Pawn/Character 최소 스파이크 권장안

이 절은 구현 확정안이 아니라 현재 프로젝트에서 결정을 내리기 위한 실험 권장안이다.

### 스파이크 목표

기존 `ADroneCharacter`가 제공하는 Character 경로를 기준점으로 보존하고, 별도 Prototype 조종 클래스에서 다음만 확인한다.

- Spawn과 Possess
- 수평 이동 명령 전달
- 수직 이동 명령 전달
- Yaw 명령 전달
- 카메라 확인
- 컴파일과 PIE 반복 실행

Take Off/Landing 규칙, 충돌 실패, 관성, 가속, 고도 유지, 배터리, 입력 키, 최종 물리 방식, 네트워크 권한은 이 스파이크에서 확정하지 않는다.

### 클래스 선택을 위한 권장 비교

현재 `ADroneCharacter`가 이미 Character 기반 비교 자료를 제공하므로, 첫 실험에서는 별도 `APawn` 기반 Prototype을 만들어 두 경로를 비교하는 방안을 우선 권장한다. 이 권장은 최종 조종 클래스를 Pawn으로 확정하는 결정이 아니다.

| 비교 항목 | 기존 Character 경로에서 확인 | Pawn Prototype에서 확인 |
|---|---|---|
| 기본 이동 기반 | Character Movement와 Capsule이 요구에 맞는가 | 필요한 컴포넌트만 구성하기 쉬운가 |
| 수직 이동 | 보행 상태와 충돌 없이 실험 가능한가 | 수직 명령을 독립적으로 전달 가능한가 |
| 회전 | 보행 방향 정렬 설정이 방해되는가 | 기체 Yaw를 독립적으로 처리 가능한가 |
| 카메라 | 기존 SpringArm/Follow Camera를 재사용할 수 있는가 | 같은 카메라 구조를 최소 구성으로 만들 수 있는가 |
| 향후 물리 | 미정인 물리 방식의 실험을 막는 제약이 있는가 | 다른 이동 방식으로 교체할 경계가 명확한가 |

비교 결과에 따라 `APawn`, `ACharacter`, 또는 별도 이동 컴포넌트 구조 중 다음 작업의 임시 기준을 선택한다. 선택 결과도 Prototype 결정으로 기록하고 최종 설계로 표현하지 않는다.

## 10. 프로젝트별 구현 체크리스트

아래 체크리스트는 사용자가 선호하는 설명 순서에 맞춘다. 아직 실제 프로젝트에는 적용하지 않았다.

### 1) 왜 필요한지

- [ ] 현재 기본 `ADroneCharacter`가 Third Person 보행용이라는 사실을 기준선으로 기록한다.
- [ ] 기존 템플릿과 새 드론 실험을 분리해 실패 시 기본 실행 경로로 돌아갈 수 있게 한다.
- [ ] Pawn/Character와 이동 방식의 최종 선택 전에 Spawn, Possess, 입력 전달, 카메라만 비교한다.
- [ ] 스파이크에서 결정하지 않을 항목을 카드에 명시한다: 최종 입력 키, 물리, 멀티플레이, Take Off/Landing 규칙.

### 2) 담당 클래스

- [ ] Pawn 후보 실험 시 `ADronePrototypePawn` 같은 Prototype 전용 이름을 사용한다.
- [ ] Character 후보 실험은 기존 `ADroneCharacter`와 `BP_ThirdPersonCharacter`를 기준선으로 사용하거나 별도 `ADronePrototypeCharacter`를 둔다.
- [ ] 기존 `ADronePlayerController`의 Mapping Context 등록 방식을 재사용할지 확인한다.
- [ ] 기존 `ADroneGameMode`를 부모로 한 별도 Prototype GameMode Blueprint를 고려한다.
- [ ] 클래스명은 후보이며 스파이크 결과에 따라 바꿀 수 있다고 작업 기록에 남긴다.

권장 격리 경로 예시는 다음과 같다. 실제 이름은 구현 시작 전에 충돌 여부를 확인한다.

```text
Source/Drone/Prototype/
  DronePrototypePawn.h/.cpp       # Pawn 후보를 시험할 때만
  DronePrototypeCharacter.h/.cpp  # Character 후보를 별도로 시험할 때만

Content/Prototype/Drone/
  BP_DronePrototype*
  BP_DronePrototypeGameMode
  Lvl_DronePrototype
  Input/
```

### 3) 헤더에 추가할 최소 항목

- [ ] 선택한 후보 기반 타입을 명확히 한다: `APawn` 또는 `ACharacter`.
- [ ] Root, 시각 표현 기준 컴포넌트, SpringArm, Camera 포인터를 선언한다.
- [ ] 수평, 수직, Yaw, Look용 `UInputAction` 참조를 Prototype 이름으로 선언한다.
- [ ] `SetupPlayerInputComponent` override를 선언한다.
- [ ] 입력을 받는 함수와 실제 이동 실험을 수행하는 함수를 분리한다.
- [ ] 속도·회전 값은 테스트용임을 알 수 있는 Category와 이름으로 Editor 노출한다.
- [ ] 최종 비행 상태, 배터리, 통신, 재밍, 네트워크 변수는 아직 추가하지 않는다.

### 4) CPP에 추가할 최소 항목

- [ ] 생성자에서 최소 컴포넌트 부착 관계를 구성한다.
- [ ] 선택한 후보가 Possess될 수 있도록 필요한 기본 설정만 둔다.
- [ ] Enhanced Input Component 캐스팅 성공/실패를 로그로 확인한다.
- [ ] 네 개의 Prototype Action을 각 함수에 바인딩한다.
- [ ] 수평·수직·Yaw 명령이 들어왔다는 사실과 방향을 검증할 최소 동작을 구현한다.
- [ ] 이동 구현은 Prototype임을 주석과 이름으로 표시하고 최종 물리 모델로 취급하지 않는다.
- [ ] Tick이 필요하지 않으면 활성화하지 않고, 필요하면 왜 필요한지 기록한다.
- [ ] 기존 `ADroneCharacter`, GameMode, PlayerController 코드를 삭제하거나 대규모 수정하지 않는다.

이 단계에서 `UFloatingPawnMovement`, 직접 Transform 변경, 물리 Force 중 하나를 제품 방식으로 확정하지 않는다. 실험에 임시 방식을 사용한다면 어떤 방식을 썼는지와 폐기 가능성을 테스트 기록에 남긴다.

### 5) Blueprint에서 설정할 항목

- [ ] 선택한 Prototype C++ 클래스의 Blueprint 자식을 만든다.
- [ ] 임시 메시와 Camera/SpringArm 값을 연결한다.
- [ ] Prototype Input Action과 Mapping Context를 기존 `Content\Input`과 구분해 만든다.
- [ ] `ADronePlayerController` 자식 Blueprint의 `DefaultMappingContexts`에 Prototype IMC를 넣는 방식을 검토한다.
- [ ] 임시 키를 매핑할 경우 `Prototype/Test`로 기록하고 최종 입력키로 표현하지 않는다.
- [ ] Prototype GameMode에 Default Pawn과 Player Controller를 연결한다.
- [ ] 기존 `BP_ThirdPerson*` 자산을 직접 덮어쓰지 않는다.

### 6) Editor 테스트 방법

- [ ] 기존 `Lvl_ThirdPerson`과 분리된 Prototype Map을 만들거나 복제본을 사용한다.
- [ ] Prototype Map의 World Settings에서만 Prototype GameMode를 Override한다.
- [ ] Project Settings의 전역 기본 Map/GameMode는 스파이크 통과 전 변경하지 않는다.
- [ ] PIE 시작 시 조종 대상이 정확히 한 대 생성되는지 확인한다.
- [ ] Player Controller와 Pawn/Character의 Possess 관계를 확인한다.
- [ ] Enhanced Input 디버그와 로그로 Mapping Context와 Action 전달을 확인한다.
- [ ] 수평, 수직, Yaw, Camera 입력을 각각 독립적으로 시험한다.
- [ ] PIE를 종료하고 다시 실행해 같은 결과가 재현되는지 확인한다.
- [ ] 기존 `Lvl_ThirdPerson`도 다시 열어 기준선이 손상되지 않았는지 확인한다.

### 7) 정상 결과

- [ ] C++ 모듈이 UE가 인식하는 설치된 Visual Studio C++ 툴체인으로 컴파일된다.
- [ ] Prototype Map에서 한 개의 조종 대상만 Spawn되고 Possess된다.
- [ ] 선택한 임시 Mapping Context가 한 번 등록된다.
- [ ] 네 개의 입력 명령이 서로 섞이지 않고 해당 함수로 전달된다.
- [ ] 임시 이동 구현에서 수평·수직·Yaw 반응을 눈으로 확인한다.
- [ ] 카메라가 조종 대상을 일관되게 보여 준다.
- [ ] 기존 Third Person Map과 Blueprint 파일이 그대로 실행된다.
- [ ] 결과 기록에는 Pawn/Character 후보의 장단점과 여전히 미정인 항목이 분리되어 있다.

### 8) 문제가 생겼을 때 확인할 항목

- [ ] 새 C++ 클래스가 `abstract`인데 직접 Spawn하려고 하지 않았는가
- [ ] World Settings GameMode Override와 Project 전역 GameMode 중 어느 것이 적용되는가
- [ ] GameMode의 Default Pawn과 Player Controller가 Prototype Blueprint를 가리키는가
- [ ] 월드 배치 인스턴스와 Default Pawn 생성이 중복되지 않았는가
- [ ] `ADronePlayerController::SetupInputComponent`가 Local Player에서 실행되는가
- [ ] `DefaultMappingContexts`에 Prototype IMC가 실제로 들어 있는가
- [ ] 같은 IMC가 다른 경로에서 중복 등록되지 않았는가
- [ ] Input Action 값 타입과 C++에서 읽는 값 타입이 일치하는가
- [ ] `Drone.Build.cs`의 기존 `EnhancedInput` 의존성을 유지했는가
- [ ] Controller Rotation, Actor Rotation, SpringArm의 회전 설정이 중복 적용되는가
- [ ] Character 후보에서는 `bOrientRotationToMovement`와 Walking Movement가 드론 실험을 방해하는가
- [ ] Pawn 후보에서는 Root/Collision/Movement Component 관계가 유효한가
- [ ] Prototype Map이 아니라 현재 기본 `Lvl_ThirdPerson`에서 테스트하고 있지 않은가

## 11. 1~3시간 작업 카드 권장 순서

| ID | 작업 | 크기 | 완료 조건 |
|---|---|---:|---|
| SP-01 | 현재 Third Person 기준선 컴파일·PIE 기록 | 1시간 | 기본 Map 실행 결과와 적용 GameMode 기록 |
| SP-02 | Pawn/Character 비교 기준 확정 | 1시간 | 비교표와 스파이크에서 제외할 미정 항목 기록 |
| SP-03 | 선택한 첫 Prototype 조종 클래스 골격 생성 | 1~2시간 | 컴파일되고 BP 자식을 만들 수 있음 |
| SP-04 | Prototype Map과 GameMode 격리 | 1~2시간 | 기존 기본 Map 변경 없이 한 개 대상 Spawn/Possess |
| SP-05 | Prototype Enhanced Input 자산·바인딩 | 1~2시간 | Action 값이 각 C++ 함수에 전달됨 |
| SP-06 | 수평·수직·Yaw 임시 반응 구현 | 1~2시간 | 입력별 반응을 독립적으로 재현 |
| SP-07 | Camera와 반복 PIE 검증 | 1~2시간 | 카메라와 전체 최소 흐름이 재실행에서도 정상 |
| SP-08 | 후보 결과 비교와 다음 임시 기준 결정 | 1시간 | 선택 근거, 폐기한 대안, 미정 항목을 구분해 기록 |

`SP-08`의 결정은 다음 구현 단계에서 사용할 임시 기준이다. 최종 조종 클래스, 입력키, 물리, 멀티플레이 규칙을 확정하는 승인이 아니다.

## 12. 이번 감사에서 확인하지 않은 사항

- `.uasset`/`.umap` 내부 데이터와 Blueprint Graph
- `BP_ThirdPersonGameMode`의 실제 Default Pawn/Player Controller 설정
- IMC의 실제 키·Trigger·Modifier
- Map 내부 Actor 배치와 World Settings
- 대화형 Editor에서의 PIE 시작·종료 결과. C++ 빌드와 Blueprint Commandlet 결과는 별도 [`STATUS.md`](../STATUS.md)에 기록되어 있다.
- Live Coding 상태
- 최종 Pawn/Character 적합성
- 최종 입력, 물리, 멀티플레이, 게임 규칙

이 항목들은 Editor 또는 빌드 실행을 동반하는 후속 검증에서 확인해야 한다.
