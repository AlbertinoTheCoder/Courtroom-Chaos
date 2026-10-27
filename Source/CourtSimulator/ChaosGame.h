#pragma once
#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "GameFramework/HUD.h"
#include "ChaosCaseData.h"
#include "ChaosGame.generated.h"
class UTexture2D;
class UFont;
class UAnimationAsset;
class UAudioComponent;
class AStaticMeshActor;
class ACameraActor;
UENUM()
enum class EChaosScreen:uint8 { Play,Record,Inspect,History,Settings,Cases,Credits,Closing,Results };
UCLASS()
class AChaosHUD:public AHUD {
 GENERATED_BODY()
public:
 AChaosHUD();
 virtual void BeginPlay() override;
 virtual void Tick(float DeltaSeconds) override;
 virtual void DrawHUD() override;
 virtual void NotifyHitBoxClick(FName BoxName) override;
 void Action(FString Id);
private:
 UPROPERTY(Transient) TObjectPtr<UChaosCaseData> Case;
 UPROPERTY(Transient) TObjectPtr<UFont> RuntimeUIFont;
 UPROPERTY(Transient) TMap<FString,TObjectPtr<UTexture2D>> Textures;
 UPROPERTY(Transient) TMap<FString,TObjectPtr<UAnimationAsset>> Animations;
 UPROPERTY(Transient) TObjectPtr<UAudioComponent> MusicAudio;
 UPROPERTY(Transient) TObjectPtr<AStaticMeshActor> GavelActor;
 UPROPERTY(Transient) TObjectPtr<AStaticMeshActor> ExhibitActor;
 TMap<FName,TWeakObjectPtr<AActor>> Cast;
 TMap<FName,TWeakObjectPtr<ACameraActor>> Cameras;
 TMap<FName,FTransform> CastRest;
 TMap<FName,FTransform> CameraRest;
 EChaosScreen Screen=EChaosScreen::Play,ReturnScreen=EChaosScreen::Play,HistoryReturn=EChaosScreen::Play,RecordReturn=EChaosScreen::Play;
 int32 Phase=-1,Statement=0,Selected=0,Credibility=5,Dialogue=0,ResolutionStage=-1,HistoryPage=0,FocusIndex=-1;
 int32 Correct=0,Wrong=0,Presses=0,Inspections=0;
 bool Resolution=false,ReducedMotion=false,InstantText=false,HighContrast=false,InspectionRead=false,ImpactFired=false,GavelFired=false,VerdictPending=false,Completed=false,ClosingSolved=false;
 float Impact=0,GavelTime=0,Shake=0,PaperTime=0,LineElapsed=0,RevealSpeed=42,TextScale=1,MasterVolume=.8f,MusicVolume=.4f,EffectsVolume=.8f,ExhibitYaw=0,ExhibitZoom=1,CaseSeconds=0,LastBleep=0;
 int32 Quality=2;
 FString Feedback,LastText,Error;
 FQuat TestHead=FQuat::Identity;
 TArray<FString> History,Buttons,PreviousButtons;
 TSet<FName> Inspected;
 float SX=1,SY=1;
 int32 FinalPhase() const;
 int32 StageIndex() const;
 const FChaosStage* Stage() const;
 FChaosLine CurrentLine() const;
 bool Unlocked(int32 Index) const;
 void SetScreen(EChaosScreen Value);
 void BeginCase();
 void Next();
 void StartGavel();
 void FinishResolution();
 void StartObjection();
 void AnimateCast();
 void UpdateProps(float DeltaSeconds);
 void SelectCamera();
 void Record(const FString& Text);
 void Save();
 bool Load();
 void SaveSettings();
 void LoadSettings();
 void RunTests();
 void RunVisualTests();
 void Sound(const FString& Name,float Volume=1);
 void Label(const FString& Text,float X,float Y,float Size,FLinearColor Color);
 void Wrapped(const FString& Text,float X,float Y,float Width,float Size,FLinearColor Color,bool Reveal=false);
 FString Wrap(const FString& Text,float Width,float Size);
 void Panel(float X,float Y,float W,float H,FLinearColor Color);
 void Sprite(const FString& Name,float X,float Y,float W,float H,float Alpha=1,float Rotation=0);
 void Texture(UTexture2D* Asset,float X,float Y,float W,float H,float Alpha=1);
 void Button(const FString& Id,const FString& Caption,float X,float Y,float W,bool Enabled=true);
 void DrawMenu();
 void DrawTrial();
 void DrawRecord();
 void DrawInspection();
 void DrawSettings();
 void DrawHistory();
 void DrawResults();
};
UCLASS()
class AChaosGameMode:public AGameModeBase {
 GENERATED_BODY()
public:AChaosGameMode();
};
