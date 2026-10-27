#pragma once
#include "CoreMinimal.h"
#include "Engine/DataAsset.h"
#include "ChaosCaseData.generated.h"
class UTexture2D;
class UStaticMesh;
USTRUCT(BlueprintType)
struct FChaosLine {
 GENERATED_BODY()
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FString Speaker;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,meta=(MultiLine=true)) FString Text;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FName Emotion=TEXT("Speaking");
};
USTRUCT(BlueprintType)
struct FChaosEvidence {
 GENERATED_BODY()
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FName Id;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FString Title;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FString Category;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,meta=(MultiLine=true)) FString Description;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,meta=(MultiLine=true)) FString Inspection;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) int32 UnlockStage=0;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TObjectPtr<UTexture2D> Illustration;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TObjectPtr<UStaticMesh> Exhibit;
};
USTRUCT(BlueprintType)
struct FChaosStatement {
 GENERATED_BODY()
 UPROPERTY(EditAnywhere,BlueprintReadWrite,meta=(MultiLine=true)) FString Text;
 UPROPERTY(EditAnywhere,BlueprintReadWrite,meta=(MultiLine=true)) FString Press;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FName Emotion=TEXT("Speaking");
};
USTRUCT(BlueprintType)
struct FChaosStage {
 GENERATED_BODY()
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FString Title;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FString Speaker;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TArray<FChaosStatement> Statements;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) int32 Contradiction=0;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FName Evidence;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TArray<FChaosLine> Resolution;
};
UCLASS(BlueprintType)
class UChaosCaseData:public UDataAsset {
 GENERATED_BODY()
public:
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FName CaseId=TEXT("golden_gavel");
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FString Title;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FString Subtitle;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TArray<FChaosLine> Consultation;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TArray<FChaosLine> Opening;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TArray<FChaosEvidence> Evidence;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TArray<FChaosStage> Stages;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TArray<FChaosLine> Verdict;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) FString ClosingPrompt;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) TArray<FString> Conclusions;
 UPROPERTY(EditAnywhere,BlueprintReadWrite) int32 CorrectConclusion=0;
 bool Validate(FString& Error) const;
};
