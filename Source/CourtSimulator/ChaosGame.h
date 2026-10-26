#pragma once
#include "CoreMinimal.h"
#include "GameFramework/GameModeBase.h"
#include "GameFramework/HUD.h"
#include "ChaosGame.generated.h"

class UTexture2D;
class UAnimationAsset;
class UAudioComponent;

UCLASS()
class AChaosHUD : public AHUD {
 GENERATED_BODY()
public:
 virtual void DrawHUD() override;
 virtual void NotifyHitBoxClick(FName BoxName) override;
 virtual void BeginPlay() override;
 void Action(FString Id);
 int32 Phase=-1, Statement=0, Selected=0, Credibility=5;
 bool Evidence=false, Paused=false;
 FString Feedback;
 float Impact=0;
 TArray<FString> History;
 void Save(); void Load();
private:
 void Label(const FString& S,float X,float Y,float Size,FLinearColor Color);
 void Panel(float X,float Y,float W,float H,FLinearColor C);
 void Button(FString Id,FString Caption,float X,float Y,float W);
 void Sprite(const FString& Name,float X,float Y,float W,float H);
 UPROPERTY(Transient) TMap<FString,TObjectPtr<UTexture2D>> Textures;
 UPROPERTY(Transient) TMap<FString,TObjectPtr<UAnimationAsset>> Animations;
 void AnimateCast();
 FQuat AnimationTestFirstPose=FQuat::Identity;
 UPROPERTY(Transient) TObjectPtr<UAudioComponent> CourtMusicAudio;
 float SX=1,SY=1;
};
UCLASS()
class AChaosGameMode : public AGameModeBase {
 GENERATED_BODY()
public: AChaosGameMode();
};
