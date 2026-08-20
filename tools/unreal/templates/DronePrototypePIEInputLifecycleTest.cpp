#if WITH_EDITOR && WITH_DEV_AUTOMATION_TESTS

#include "Prototype/DronePrototypePawn.h"

#include "Editor.h"
#include "Editor/EditorEngine.h"
#include "EnhancedActionKeyMapping.h"
#include "EnhancedInputComponent.h"
#include "EnhancedInputSubsystems.h"
#include "EnhancedPlayerInput.h"
#include "Engine/Engine.h"
#include "Engine/LocalPlayer.h"
#include "Engine/World.h"
#include "EngineUtils.h"
#include "GameFramework/FloatingPawnMovement.h"
#include "GameFramework/InputSettings.h"
#include "GameFramework/PlayerController.h"
#include "HAL/PlatformTime.h"
#include "InputAction.h"
#include "InputCoreTypes.h"
#include "InputKeyEventArgs.h"
#include "InputMappingContext.h"
#include "Math/RotationMatrix.h"
#include "Misc/AutomationTest.h"
#include "PlayInEditorDataTypes.h"
#include "Settings/LevelEditorPlaySettings.h"
#include "Tests/AutomationCommon.h"
#include "Tests/AutomationEditorCommon.h"
#include "UObject/UObjectGlobals.h"

namespace DronePrototypePIEInputLifecycle
{
constexpr const TCHAR* MapPackage = TEXT("/Game/Drone/Prototype/Maps/Lvl_DronePrototype");
constexpr const TCHAR* PawnClassPath = TEXT("/Game/Drone/Prototype/Blueprints/BP_DronePrototypePawn.BP_DronePrototypePawn_C");
constexpr const TCHAR* ContextPath = TEXT("/Game/Drone/Prototype/Input/IMC_DronePrototype.IMC_DronePrototype");
constexpr const TCHAR* MovePath = TEXT("/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_Move.IA_DronePrototype_Move");
constexpr const TCHAR* AltitudePath = TEXT("/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_Altitude.IA_DronePrototype_Altitude");
constexpr const TCHAR* YawPath = TEXT("/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_Yaw.IA_DronePrototype_Yaw");
constexpr const TCHAR* LookPath = TEXT("/Game/Drone/Prototype/Input/Actions/IA_DronePrototype_Look.IA_DronePrototype_Look");

bool HasPIEWorld()
{
	if (!GEngine)
	{
		return false;
	}

	for (const FWorldContext& Context : GEngine->GetWorldContexts())
	{
		if (Context.WorldType == EWorldType::PIE && Context.World() != nullptr)
		{
			return true;
		}
	}

	return false;
}

FRequestPlaySessionParams MakePlayParams()
{
	ULevelEditorPlaySettings* Settings = NewObject<ULevelEditorPlaySettings>(GetTransientPackage());
	Settings->SetPlayNetMode(EPlayNetMode::PIE_Standalone);
	Settings->SetRunUnderOneProcess(true);
	Settings->SetPlayNumberOfClients(1);
	Settings->bLaunchSeparateServer = false;
	Settings->AddToRoot(); // Removed by FStartPIEForAutomationCommand in UE 5.8.

	FRequestPlaySessionParams Params;
	Params.SessionDestination = EPlaySessionDestinationType::InProcess;
	Params.WorldType = EPlaySessionWorldType::PlayInEditor;
	Params.EditorPlaySettings = Settings;
	Params.bAllowOnlineSubsystem = false;
	return Params;
}

enum class EProbeEffect : uint8
{
	Forward,
	Right,
	Up,
	ActorYaw,
	ControlYaw,
	ControlPitch
};

struct FProbe
{
	FKey Key;
	const TCHAR* Label;
	EProbeEffect Effect;
	float ExpectedSign;
	bool bAnalog;
};

enum class EAcquireResult : uint8
{
	Wait,
	Ready,
	Fatal
};

class FValidatePIEInputCommand final : public IAutomationLatentCommand
{
public:
	FValidatePIEInputCommand(FAutomationTestBase* InTest, const int32 InCycle)
		: Test(InTest)
		, Cycle(InCycle)
	{
	}

	virtual bool Update() override
	{
		const double Now = FPlatformTime::Seconds();
		if (!bActivated)
		{
			bActivated = true;
			ActivatedAt = Now;
		}

		if (Now - ActivatedAt > 60.0)
		{
			return Fail(TEXT("input validation exceeded 60 seconds"));
		}

		if (Phase == EPhase::Acquire)
		{
			FString Reason;
			const EAcquireResult Result = TryAcquire(Reason);
			if (Result == EAcquireResult::Fatal)
			{
				return Fail(Reason);
			}

			if (Result == EAcquireResult::Wait)
			{
				if (Now - ActivatedAt > 10.0)
				{
					return Fail(FString::Printf(TEXT("setup did not become ready: %s"), *Reason));
				}
				return false;
			}

			BuildProbes();
			Phase = EPhase::Reset;
			return false;
		}

		ADronePrototypePawn* CurrentPawn = Pawn.Get();
		APlayerController* CurrentController = Controller.Get();
		UEnhancedPlayerInput* CurrentInput = PlayerInput.Get();
		if (!CurrentPawn || !CurrentController || !CurrentInput)
		{
			return Fail(TEXT("PIE objects became invalid during input probes"));
		}

		if (ProbeIndex >= Probes.Num())
		{
			CurrentInput->FlushPressedKeys();
			Test->AddInfo(FString::Printf(TEXT("[fresh PIE %d/3] all key-to-callback probes passed"), Cycle));
			return true;
		}

		const FProbe& Probe = Probes[ProbeIndex];
		switch (Phase)
		{
		case EPhase::Reset:
			if (UFloatingPawnMovement* Movement = CurrentPawn->GetPrototypeMovementComponent())
			{
				Movement->StopMovementImmediately();
			}
			CurrentInput->FlushPressedKeys();
			CurrentPawn->ConsumeMovementInputVector();
			if (!CurrentPawn->SetActorTransform(InitialPawnTransform, false, nullptr, ETeleportType::TeleportPhysics))
			{
				return Fail(FString::Printf(TEXT("%s: could not reset Pawn transform"), Probe.Label));
			}
			CurrentController->SetControlRotation(InitialControlRotation);
			FramesToSettle = 1;
			Phase = EPhase::Settle;
			return false;

		case EPhase::Settle:
			if (FramesToSettle-- > 0)
			{
				return false;
			}
			BaselineLocation = CurrentPawn->GetActorLocation();
			BaselineActorRotation = CurrentPawn->GetActorRotation();
			BaselineControlRotation = CurrentController->GetControlRotation();
			SendProbe(Probe, *CurrentInput);
			ProbeStartedAt = Now;
			Phase = EPhase::Observe;
			return false;

		case EPhase::Observe:
		{
			const float SignedEffect = MeasureSignedEffect(Probe, *CurrentPawn, *CurrentController);
			const float Tolerance =
				(Probe.Effect == EProbeEffect::Forward || Probe.Effect == EProbeEffect::Right || Probe.Effect == EProbeEffect::Up)
				? 0.01f
				: 0.001f;

			if (SignedEffect > Tolerance)
			{
				ReleaseProbe(Probe, *CurrentInput);
				FString IsolationError;
				if (!CheckRotationIsolation(Probe, *CurrentPawn, *CurrentController, IsolationError))
				{
					return Fail(IsolationError);
				}
				++ProbeIndex;
				Phase = EPhase::Reset;
				return false;
			}

			if (SignedEffect < -Tolerance)
			{
				ReleaseProbe(Probe, *CurrentInput);
				return Fail(FString::Printf(TEXT("%s moved in the opposite direction (signed effect %.6f)"), Probe.Label, SignedEffect));
			}

			if (Now - ProbeStartedAt > 2.0)
			{
				ReleaseProbe(Probe, *CurrentInput);
				return Fail(FString::Printf(TEXT("%s produced no observable callback effect"), Probe.Label));
			}

			if (Probe.bAnalog)
			{
				SendProbe(Probe, *CurrentInput); // Mouse delta is a one-frame input.
			}
			return false;
		}

		default:
			return Fail(TEXT("invalid latent input phase"));
		}
	}

private:
	enum class EPhase : uint8
	{
		Acquire,
		Reset,
		Settle,
		Observe
	};

	EAcquireResult TryAcquire(FString& OutReason)
	{
		UWorld* WorldObject = AutomationCommon::GetAnyGameWorld();
		if (!WorldObject || WorldObject->WorldType != EWorldType::PIE)
		{
			OutReason = TEXT("PIE world is unavailable");
			return EAcquireResult::Wait;
		}

		if (!WorldObject->GetMapName().EndsWith(TEXT("Lvl_DronePrototype")))
		{
			OutReason = FString::Printf(TEXT("wrong PIE map: %s"), *WorldObject->GetMapName());
			return EAcquireResult::Fatal;
		}

		int32 PawnCount = 0;
		ADronePrototypePawn* FoundPawn = nullptr;
		for (TActorIterator<ADronePrototypePawn> It(WorldObject); It; ++It)
		{
			FoundPawn = *It;
			++PawnCount;
		}

		if (PawnCount == 0)
		{
			OutReason = TEXT("Prototype Pawn has not spawned yet");
			return EAcquireResult::Wait;
		}

		if (PawnCount != 1)
		{
			OutReason = FString::Printf(TEXT("expected one Prototype Pawn, found %d"), PawnCount);
			return EAcquireResult::Fatal;
		}

		APlayerController* FoundController = WorldObject->GetFirstPlayerController();
		if (!FoundController || !FoundController->IsLocalController())
		{
			OutReason = TEXT("local PlayerController is unavailable");
			return EAcquireResult::Wait;
		}

		if (FoundController->GetPawn() != FoundPawn || FoundPawn->GetController() != FoundController)
		{
			OutReason = TEXT("Prototype Pawn is not possessed by the local PlayerController");
			return EAcquireResult::Fatal;
		}

		UClass* ExpectedPawnClass = LoadClass<ADronePrototypePawn>(nullptr, PawnClassPath);
		if (!ExpectedPawnClass || FoundPawn->GetClass() != ExpectedPawnClass)
		{
			OutReason = FString::Printf(
				TEXT("spawned Pawn class is %s, expected BP_DronePrototypePawn_C"),
				*GetNameSafe(FoundPawn->GetClass()));
			return EAcquireResult::Fatal;
		}

		ULocalPlayer* LocalPlayer = FoundController->GetLocalPlayer();
		UEnhancedInputLocalPlayerSubsystem* Subsystem =
			LocalPlayer ? ULocalPlayer::GetSubsystem<UEnhancedInputLocalPlayerSubsystem>(LocalPlayer) : nullptr;
		UEnhancedPlayerInput* FoundInput = Subsystem ? Subsystem->GetPlayerInput() : nullptr;
		UEnhancedInputComponent* InputComponent = Cast<UEnhancedInputComponent>(FoundPawn->InputComponent);
		if (!Subsystem || !FoundInput || !InputComponent)
		{
			OutReason = TEXT("Enhanced Input subsystem/player input/component is not ready");
			return EAcquireResult::Wait;
		}

		UInputMappingContext* IMC = LoadObject<UInputMappingContext>(nullptr, ContextPath);
		UInputAction* Move = LoadObject<UInputAction>(nullptr, MovePath);
		UInputAction* Altitude = LoadObject<UInputAction>(nullptr, AltitudePath);
		UInputAction* Yaw = LoadObject<UInputAction>(nullptr, YawPath);
		UInputAction* Look = LoadObject<UInputAction>(nullptr, LookPath);
		if (!IMC || !Move || !Altitude || !Yaw || !Look)
		{
			OutReason = TEXT("one or more Prototype input assets failed to load");
			return EAcquireResult::Fatal;
		}

		int32 Priority = INDEX_NONE;
		if (!Subsystem->HasMappingContext(IMC, Priority))
		{
			OutReason = TEXT("IMC_DronePrototype is not applied yet");
			return EAcquireResult::Wait;
		}

		if (Priority != 1)
		{
			OutReason = FString::Printf(TEXT("IMC_DronePrototype priority is %d, expected 1"), Priority);
			return EAcquireResult::Fatal;
		}

		const TArray<FEnhancedActionKeyMapping>& SourceMappings = IMC->GetMappings();
		if (SourceMappings.Num() != 9)
		{
			OutReason = FString::Printf(TEXT("IMC source has %d mappings, expected 9"), SourceMappings.Num());
			return EAcquireResult::Fatal;
		}

		const TConstArrayView<const FEnhancedActionKeyMapping> EffectiveMappings = FoundInput->GetEnhancedActionMappingsView();
		const TArray<const UInputAction*> ExpectedActions{Move, Altitude, Yaw, Look};
		int32 PrototypeEffectiveCount = 0;
		for (const FEnhancedActionKeyMapping& Effective : EffectiveMappings)
		{
			if (ExpectedActions.Contains(Effective.Action.Get()))
			{
				++PrototypeEffectiveCount;
			}
		}

		if (PrototypeEffectiveCount < 9)
		{
			OutReason = FString::Printf(TEXT("effective Prototype mappings are still rebuilding (%d/9)"), PrototypeEffectiveCount);
			return EAcquireResult::Wait;
		}

		if (PrototypeEffectiveCount != 9 || EffectiveMappings.Num() != 9)
		{
			OutReason = FString::Printf(
				TEXT("effective mappings are Prototype=%d, total=%d; expected 9 and 9"),
				PrototypeEffectiveCount,
				EffectiveMappings.Num());
			return EAcquireResult::Fatal;
		}

		for (const FEnhancedActionKeyMapping& Source : SourceMappings)
		{
			int32 MatchCount = 0;
			for (const FEnhancedActionKeyMapping& Effective : EffectiveMappings)
			{
				if (Effective.Action == Source.Action && Effective.Key == Source.Key)
				{
					++MatchCount;
				}
			}

			if (MatchCount != 1)
			{
				OutReason = FString::Printf(
					TEXT("effective mapping %s/%s appears %d times"),
					*GetNameSafe(Source.Action.Get()),
					*Source.Key.ToString(),
					MatchCount);
				return MatchCount == 0 ? EAcquireResult::Wait : EAcquireResult::Fatal;
			}
		}

		for (const UInputAction* Action : ExpectedActions)
		{
			int32 ActionBindingCount = 0;
			const FEnhancedInputActionEventBinding* FoundBinding = nullptr;
			for (const TUniquePtr<FEnhancedInputActionEventBinding>& Binding : InputComponent->GetActionEventBindings())
			{
				if (Binding && Binding->GetAction() == Action)
				{
					++ActionBindingCount;
					FoundBinding = Binding.Get();
				}
			}

			if (ActionBindingCount == 0)
			{
				OutReason = FString::Printf(TEXT("binding for %s is not ready"), *GetNameSafe(Action));
				return EAcquireResult::Wait;
			}

			if (ActionBindingCount != 1 || !FoundBinding || FoundBinding->GetTriggerEvent() != ETriggerEvent::Triggered
				|| FoundBinding->GetUObject() != FoundPawn)
			{
				OutReason = FString::Printf(
					TEXT("%s does not have exactly one Pawn-owned Triggered binding"),
					*GetNameSafe(Action));
				return EAcquireResult::Fatal;
			}
		}

		World = WorldObject;
		Pawn = FoundPawn;
		Controller = FoundController;
		PlayerInput = FoundInput;
		InitialPawnTransform = FoundPawn->GetActorTransform();
		InitialControlRotation = FoundController->GetControlRotation();
		return EAcquireResult::Ready;
	}

	void BuildProbes()
	{
		APlayerController* CurrentController = Controller.Get();
		float LookYawSign = 1.0f;
		float LookPitchSign = 1.0f;
		if (GetDefault<UInputSettings>()->bEnableLegacyInputScales)
		{
			PRAGMA_DISABLE_DEPRECATION_WARNINGS
			LookYawSign = FMath::Sign(CurrentController->GetDeprecatedInputYawScale());
			LookPitchSign = FMath::Sign(CurrentController->GetDeprecatedInputPitchScale());
			PRAGMA_ENABLE_DEPRECATION_WARNINGS
		}

		Probes = {
			{EKeys::W, TEXT("W / forward"), EProbeEffect::Forward, +1.0f, false},
			{EKeys::S, TEXT("S / backward"), EProbeEffect::Forward, -1.0f, false},
			{EKeys::A, TEXT("A / left"), EProbeEffect::Right, -1.0f, false},
			{EKeys::D, TEXT("D / right"), EProbeEffect::Right, +1.0f, false},
			{EKeys::SpaceBar, TEXT("SpaceBar / up"), EProbeEffect::Up, +1.0f, false},
			{EKeys::LeftControl, TEXT("LeftControl / down"), EProbeEffect::Up, -1.0f, false},
			{EKeys::E, TEXT("E / actor yaw positive"), EProbeEffect::ActorYaw, +1.0f, false},
			{EKeys::Q, TEXT("Q / actor yaw negative"), EProbeEffect::ActorYaw, -1.0f, false},
			{EKeys::MouseX, TEXT("MouseX / control yaw"), EProbeEffect::ControlYaw, LookYawSign, true},
			{EKeys::MouseY, TEXT("MouseY / control pitch"), EProbeEffect::ControlPitch, LookPitchSign, true},
		};
	}

	static void SendProbe(const FProbe& Probe, UEnhancedPlayerInput& Input)
	{
		Input.InputKey(FInputKeyEventArgs::CreateSimulated(
			Probe.Key,
			Probe.bAnalog ? IE_Axis : IE_Pressed,
			Probe.bAnalog ? 5.0f : 1.0f,
			Probe.bAnalog ? 1 : -1));
	}

	static void ReleaseProbe(const FProbe& Probe, UEnhancedPlayerInput& Input)
	{
		if (Probe.bAnalog)
		{
			Input.InputKey(FInputKeyEventArgs::CreateSimulated(Probe.Key, IE_Axis, 0.0f, 1));
		}
		else
		{
			Input.InputKey(FInputKeyEventArgs::CreateSimulated(Probe.Key, IE_Released, 0.0f));
		}
	}

	float MeasureSignedEffect(
		const FProbe& Probe,
		const ADronePrototypePawn& CurrentPawn,
		const APlayerController& CurrentController) const
	{
		float Raw = 0.0f;
		switch (Probe.Effect)
		{
		case EProbeEffect::Forward:
			Raw = FVector::DotProduct(CurrentPawn.GetActorLocation() - BaselineLocation, BaselineActorRotation.Vector());
			break;
		case EProbeEffect::Right:
			Raw = FVector::DotProduct(
				CurrentPawn.GetActorLocation() - BaselineLocation,
				FRotationMatrix(BaselineActorRotation).GetScaledAxis(EAxis::Y));
			break;
		case EProbeEffect::Up:
			Raw = CurrentPawn.GetActorLocation().Z - BaselineLocation.Z;
			break;
		case EProbeEffect::ActorYaw:
			Raw = FMath::FindDeltaAngleDegrees(BaselineActorRotation.Yaw, CurrentPawn.GetActorRotation().Yaw);
			break;
		case EProbeEffect::ControlYaw:
			Raw = FMath::FindDeltaAngleDegrees(BaselineControlRotation.Yaw, CurrentController.GetControlRotation().Yaw);
			break;
		case EProbeEffect::ControlPitch:
			Raw = FMath::FindDeltaAngleDegrees(BaselineControlRotation.Pitch, CurrentController.GetControlRotation().Pitch);
			break;
		}

		return Raw * Probe.ExpectedSign;
	}

	bool CheckRotationIsolation(
		const FProbe& Probe,
		const ADronePrototypePawn& CurrentPawn,
		const APlayerController& CurrentController,
		FString& OutError) const
	{
		constexpr float RotationTolerance = 0.05f;
		if (Probe.Effect == EProbeEffect::ActorYaw)
		{
			const float ControlDelta = FMath::Abs(
				FMath::FindDeltaAngleDegrees(BaselineControlRotation.Yaw, CurrentController.GetControlRotation().Yaw));
			if (ControlDelta > RotationTolerance)
			{
				OutError = FString::Printf(
					TEXT("%s changed control yaw by %.4f; expected actor yaw only"),
					Probe.Label,
					ControlDelta);
				return false;
			}
		}

		if (Probe.Effect == EProbeEffect::ControlYaw || Probe.Effect == EProbeEffect::ControlPitch)
		{
			const FRotator ActorDelta = (CurrentPawn.GetActorRotation() - BaselineActorRotation).GetNormalized();
			if (!ActorDelta.IsNearlyZero(RotationTolerance))
			{
				OutError = FString::Printf(
					TEXT("%s changed actor rotation by %s; expected control rotation only"),
					Probe.Label,
					*ActorDelta.ToCompactString());
				return false;
			}
		}

		return true;
	}

	bool Fail(const FString& Message)
	{
		if (UEnhancedPlayerInput* CurrentInput = PlayerInput.Get())
		{
			CurrentInput->FlushPressedKeys();
		}
		Test->AddError(FString::Printf(TEXT("[fresh PIE %d/3] %s"), Cycle, *Message));
		return true; // Continue to queued EndPIE and teardown commands.
	}

	FAutomationTestBase* Test;
	int32 Cycle;
	bool bActivated = false;
	double ActivatedAt = 0.0;
	double ProbeStartedAt = 0.0;
	EPhase Phase = EPhase::Acquire;
	int32 FramesToSettle = 0;
	int32 ProbeIndex = 0;
	TArray<FProbe> Probes;
	TWeakObjectPtr<UWorld> World;
	TWeakObjectPtr<ADronePrototypePawn> Pawn;
	TWeakObjectPtr<APlayerController> Controller;
	TWeakObjectPtr<UEnhancedPlayerInput> PlayerInput;
	FTransform InitialPawnTransform;
	FRotator InitialControlRotation;
	FVector BaselineLocation = FVector::ZeroVector;
	FRotator BaselineActorRotation = FRotator::ZeroRotator;
	FRotator BaselineControlRotation = FRotator::ZeroRotator;
};

class FWaitForPIETeardownCommand final : public IAutomationLatentCommand
{
public:
	FWaitForPIETeardownCommand(FAutomationTestBase* InTest, const int32 InCycle)
		: Test(InTest)
		, Cycle(InCycle)
	{
	}

	virtual bool Update() override
	{
		const double Now = FPlatformTime::Seconds();
		if (!bActivated)
		{
			bActivated = true;
			ActivatedAt = Now;
		}

		const bool bSessionActive = GEditor && GEditor->IsPlaySessionInProgress();
		const bool bPlayWorldAlive = GEditor && GEditor->PlayWorld != nullptr;
		if (!bSessionActive && !bPlayWorldAlive && !HasPIEWorld())
		{
			return true;
		}

		if (!bForcedCleanup && Now - ActivatedAt > 10.0)
		{
			bForcedCleanup = true;
			Test->AddError(FString::Printf(
				TEXT("[fresh PIE %d/3] PIE teardown timed out; forcing EndPlayMap"),
				Cycle));
			if (GEditor)
			{
				GEditor->EndPlayMap();
			}
		}

		if (Now - ActivatedAt > 30.0)
		{
			Test->AddError(FString::Printf(
				TEXT("[fresh PIE %d/3] PIE world survived forced teardown; stopping this lifecycle test"),
				Cycle));
			return true;
		}

		return false;
	}

private:
	FAutomationTestBase* Test;
	int32 Cycle;
	bool bActivated = false;
	bool bForcedCleanup = false;
	double ActivatedAt = 0.0;
};
} // namespace DronePrototypePIEInputLifecycle

IMPLEMENT_SIMPLE_AUTOMATION_TEST(
	FDronePrototypePIEInputLifecycleTest,
	"Drone.Prototype.PIEInputLifecycle",
	EAutomationTestFlags::EditorContext | EAutomationTestFlags::ProductFilter)

bool FDronePrototypePIEInputLifecycleTest::RunTest(const FString& Parameters)
{
	using namespace DronePrototypePIEInputLifecycle;

	if (!GEditor)
	{
		AddError(TEXT("GEditor is unavailable"));
		return false;
	}

	if (GEditor->IsPlaySessionInProgress() || HasPIEWorld())
	{
		AddError(TEXT("Test requires no pre-existing PIE session"));
		return false;
	}

	FAutomationEditorCommonUtils::LoadMap(MapPackage);
	UWorld* EditorWorld = GEditor->GetEditorWorldContext().World();
	if (!EditorWorld || EditorWorld->GetOutermost()->GetName() != MapPackage)
	{
		AddError(FString::Printf(TEXT("Could not open %s"), MapPackage));
		return false;
	}

	for (int32 Cycle = 1; Cycle <= 3; ++Cycle)
	{
		FRequestPlaySessionParams Params = MakePlayParams();
		ADD_LATENT_AUTOMATION_COMMAND(FStartPIEForAutomationCommand(MoveTemp(Params)));
		ADD_LATENT_AUTOMATION_COMMAND(FValidatePIEInputCommand(this, Cycle));
		ADD_LATENT_AUTOMATION_COMMAND(FEndPlayMapCommand());
		ADD_LATENT_AUTOMATION_COMMAND(FWaitForPIETeardownCommand(this, Cycle));
	}

	return true;
}

#endif
