#include "ChaosCaseData.h"
bool UChaosCaseData::Validate(FString& Error) const {
 if(Title.IsEmpty()||Consultation.IsEmpty()||Opening.IsEmpty()||Verdict.IsEmpty()||Stages.IsEmpty()||Evidence.IsEmpty()){Error=TEXT("Case is missing required dialogue or evidence.");return false;}
 if(!Conclusions.IsValidIndex(CorrectConclusion)||Conclusions.Num()<2){Error=TEXT("Closing argument choices are incomplete.");return false;}
 TSet<FName> Ids;for(const auto& E:Evidence){if(E.Id.IsNone()||Ids.Contains(E.Id)||E.Title.IsEmpty()){Error=TEXT("Evidence IDs must be unique and have titles.");return false;}Ids.Add(E.Id);}
 for(int32 I=0;I<Stages.Num();++I){const auto& S=Stages[I];if(!S.Statements.IsValidIndex(S.Contradiction)||!Ids.Contains(S.Evidence)||S.Resolution.IsEmpty()){Error=TEXT("A contradiction refers to missing testimony or evidence.");return false;}for(const auto& E:Evidence)if(E.Id==S.Evidence&&E.UnlockStage>I){Error=TEXT("A required clue is locked past its contradiction.");return false;}}
 return true;
}
