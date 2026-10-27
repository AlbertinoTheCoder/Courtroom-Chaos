#pragma once
#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "ChaosAudioData.generated.h"
class USoundWave;
USTRUCT(BlueprintType)
struct FChaosSpeechTake {
 GENERATED_BODY()
 UPROPERTY(EditAnywhere,BlueprintReadOnly) FString Speaker;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) FString Text;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) TObjectPtr<USoundWave> Sound;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) float Duration=0;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) float EnvelopeHz=40;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) TArray<float> Envelope;
};
USTRUCT(BlueprintType)
struct FChaosSpeechSequence {
 GENERATED_BODY()
 UPROPERTY(EditAnywhere,BlueprintReadOnly) TArray<FChaosSpeechTake> Takes;
};
UCLASS(BlueprintType)
class UChaosAudioData:public UDataAsset {
 GENERATED_BODY()
public:
 UPROPERTY(EditAnywhere,BlueprintReadOnly) TMap<FString,FChaosSpeechSequence> Speech;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) TMap<FString,FString> VoicePresets;
 UPROPERTY(EditAnywhere,BlueprintReadOnly) TArray<TObjectPtr<USoundWave>> MusicLayers;
};
