#include "ChaosGame.h"
#include "Engine/Canvas.h"
#include "Engine/Font.h"
#include "CanvasItem.h"
#include "Fonts/FontMeasure.h"
#include "Framework/Application/SlateApplication.h"
#include "Rendering/SlateRenderer.h"
#include "Styling/CoreStyle.h"
#include "UnrealClient.h"
#include "Engine/Engine.h"
#include "Engine/GameViewportClient.h"
#include "Engine/StaticMeshActor.h"
#include "Engine/Texture2D.h"
#include "Camera/CameraActor.h"
#include "Components/SkeletalMeshComponent.h"
#include "Components/StaticMeshComponent.h"
#include "Components/AudioComponent.h"
#include "Animation/AnimationAsset.h"
#include "Animation/AnimSingleNodeInstance.h"
#include "GameFramework/PlayerController.h"
#include "GameFramework/GameUserSettings.h"
#include "Kismet/GameplayStatics.h"
#include "EngineUtils.h"
#include "TimerManager.h"
#include "Sound/SoundBase.h"
#include "Sound/SoundWave.h"
#include "Engine/SkeletalMesh.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Misc/CommandLine.h"
#include "HAL/FileManager.h"
#include "HAL/PlatformMisc.h"
#include "Dom/JsonObject.h"
#include "Serialization/JsonSerializer.h"
#include "Serialization/JsonWriter.h"
namespace Court {
 const FLinearColor Ink(.025f,.035f,.065f),Cream(.96f,.88f,.72f),Gold(.91f,.64f,.22f),Teal(.015f,.17f,.15f),Red(.46f,.035f,.075f);
 FSlateFontInfo UIFont(float Size,float Scale,const UFont* Font){return FSlateFontInfo(Font,FMath::Max(8,FMath::RoundToInt(Size*Scale*.75f)),TEXT("Regular"));}
 bool Testing(){return FParse::Param(FCommandLine::Get(),TEXT("CourtSelfTest"))||FParse::Param(FCommandLine::Get(),TEXT("CourtVisualTest"));}
 FString File(const FString& Name){return FPaths::ProjectSavedDir()/(Testing()?TEXT("Test_")+Name:Name);}
 bool Read(const FString& Path,TSharedPtr<FJsonObject>& J){FString S;if(!FFileHelper::LoadFileToString(S,*Path))return false;return FJsonSerializer::Deserialize(TJsonReaderFactory<>::Create(S),J)&&J.IsValid();}
 bool Write(const FString& Path,const TSharedRef<FJsonObject>& J){FString S;FJsonSerializer::Serialize(J,TJsonWriterFactory<>::Create(&S));IFileManager::Get().MakeDirectory(*FPaths::GetPath(Path),true);const FString Temp=Path+TEXT(".tmp");return FFileHelper::SaveStringToFile(S,*Temp)&&IFileManager::Get().Move(*Path,*Temp,true,true);}
 double Number(const TSharedPtr<FJsonObject>& J,const TCHAR* K,double D){double V;return J->TryGetNumberField(K,V)&&FMath::IsFinite(V)?V:D;}
 FString String(const TSharedPtr<FJsonObject>& J,const TCHAR* K,const FString& D=FString()){FString V;return J->TryGetStringField(K,V)?V:D;}
 bool Boolean(const TSharedPtr<FJsonObject>& J,const TCHAR* K,bool D=false){bool V;return J->TryGetBoolField(K,V)?V:D;}
 float Ease(float T){return FMath::SmoothStep(0.f,1.f,FMath::Clamp(T,0.f,1.f));}
}
AChaosGameMode::AChaosGameMode(){HUDClass=AChaosHUD::StaticClass();DefaultPawnClass=nullptr;}
AChaosHUD::AChaosHUD(){PrimaryActorTick.bCanEverTick=true;}
int32 AChaosHUD::FinalPhase()const{return Case?Case->Stages.Num()+2:5;}
int32 AChaosHUD::StageIndex()const{return Phase-2;}
const FChaosStage* AChaosHUD::Stage()const{return Case&&Case->Stages.IsValidIndex(StageIndex())?&Case->Stages[StageIndex()]:nullptr;}
bool AChaosHUD::Unlocked(int32 I)const{return Case&&Case->Evidence.IsValidIndex(I)&&Case->Evidence[I].UnlockStage<=FMath::Max(0,Phase-2);}
void AChaosHUD::BeginPlay(){
 Super::BeginPlay();RuntimeUIFont=NewObject<UFont>(this);RuntimeUIFont->FontCacheType=EFontCacheType::Runtime;RuntimeUIFont->GetMutableInternalCompositeFont()=*FCoreStyle::GetDefaultFont();auto P=GetOwningPlayerController();P->bShowMouseCursor=true;P->bEnableClickEvents=true;P->bEnableMouseOverEvents=true;
 FInputModeGameAndUI Mode;Mode.SetHideCursorDuringCapture(false);P->SetInputMode(Mode);if(GetWorld()->GetGameViewport())GetWorld()->GetGameViewport()->SetMouseCaptureMode(EMouseCaptureMode::CaptureDuringMouseDown);
 for(const FString& Asset:{FString(TEXT("DA_GoldenGavel")),FString(TEXT("DA_BlackoutBanquet")),FString(TEXT("DA_CharityEnvelope"))})if(auto Data=LoadObject<UChaosCaseData>(nullptr,*(TEXT("/Game/Cases/")+Asset+TEXT(".")+Asset)))CaseLibrary.Add(Data);
 if(!CaseLibrary.IsEmpty())Case=CaseLibrary[0];
 if(!Case){Error=TEXT("The case data could not be loaded. Rebuild the project content.");return;}
 if(!Case->Validate(Error))return;
 const TArray<FName> Names={TEXT("Oliver"),TEXT("Victor"),TEXT("Bumble"),TEXT("Benny"),TEXT("Milo"),TEXT("Brick")};
 for(TActorIterator<AActor> It(GetWorld());It;++It){for(const FName& N:Names)if(It->ActorHasTag(N)){Cast.Add(N,*It);CastRest.Add(N,It->GetActorTransform());}if(It->ActorHasTag(TEXT("AnimatedGavel")))GavelActor=::Cast<AStaticMeshActor>(*It);if(It->ActorHasTag(TEXT("EvidenceExhibit")))ExhibitActor=::Cast<AStaticMeshActor>(*It);}
 for(TActorIterator<ACameraActor> It(GetWorld());It;++It)for(const FName& Tag:It->Tags){Cameras.Add(Tag,*It);CameraRest.Add(Tag,It->GetActorTransform());}
 if(ExhibitActor)ExhibitActor->SetActorHiddenInGame(true);
 LoadSettings();CourtAudio=LoadObject<UChaosAudioData>(nullptr,TEXT("/Game/Audio/DA_CourtAudio.DA_CourtAudio"));
 if(CourtAudio)for(auto Sound:CourtAudio->MusicLayers)MusicStems.Add(UGameplayStatics::SpawnSound2D(this,Sound,.0001f,1,0,nullptr,false,false));
 if(MusicStems.Num())MusicAudio=MusicStems[0];
 const TArray<FString> Moods={TEXT("Idle"),TEXT("Listening"),TEXT("Speaking"),TEXT("Thinking"),TEXT("Confused"),TEXT("Happy"),TEXT("Smug"),TEXT("Angry"),TEXT("Nervous"),TEXT("Shock"),TEXT("Sad"),TEXT("Suspicious"),TEXT("Frustrated"),TEXT("Pointing"),TEXT("Slam"),TEXT("Gavel"),TEXT("LeanForward"),TEXT("LeanBackward"),TEXT("Celebrate"),TEXT("Embarrassed")};
 for(const auto& N:Names)for(const auto& Mood:Moods){const FString Key=TEXT("AN_")+N.ToString()+TEXT("_")+Mood;Animations.Add(Key,LoadObject<UAnimationAsset>(nullptr,*(TEXT("/Game/Characters/Animations/")+Key+TEXT(".")+Key)));}
 if(Court::Testing()){ValidateAudio();FTimerHandle Ready;GetWorld()->GetTimerManager().SetTimer(Ready,[this](){if(FParse::Param(FCommandLine::Get(),TEXT("CourtVisualTest")))RunVisualTests();else RunTests();},4.f,false);}
}
FChaosLine AChaosHUD::CurrentLine()const{
 FChaosLine L;if(!Case)return L;
 if(Resolution&&Case->Stages.IsValidIndex(ResolutionStage)){const auto& A=Case->Stages[ResolutionStage].Resolution;if(A.IsValidIndex(Dialogue))return A[Dialogue];}
 if(Phase==0&&Case->Consultation.IsValidIndex(Dialogue))return Case->Consultation[Dialogue];
 if(Phase==1&&Case->Opening.IsValidIndex(Dialogue))return Case->Opening[Dialogue];
 if(Phase==FinalPhase()&&!ClosingSolved){L.Speaker=TEXT("Oliver");L.Text=Case->ClosingPrompt;L.Emotion=TEXT("Thinking");return L;}
 if(Phase==FinalPhase()&&Case->Verdict.IsValidIndex(Dialogue))return Case->Verdict[Dialogue];
 if(const auto S=Stage())if(S->Statements.IsValidIndex(Statement)){L.Speaker=S->Speaker;L.Text=S->Statements[Statement].Text;L.Emotion=S->Statements[Statement].Emotion;}
 return L;
}
void AChaosHUD::Tick(float D){
 Super::Tick(D);if(!Case||!Error.IsEmpty())return;
 const auto Line=CurrentLine();if(Line.Text!=LastText){LastText=Line.Text;LineElapsed=0;Record(Line.Speaker+TEXT(": ")+Line.Text);}else LineElapsed+=D;
 if(Phase>=0&&Screen!=EChaosScreen::Settings&&Screen!=EChaosScreen::Results)CaseSeconds+=D;
 if(Impact>0){float Before=Impact;Impact=FMath::Max(0.f,Impact-D);float Elapsed=3.2f-Impact;if(!ImpactFired&&(Elapsed>=.72f||ReducedMotion)){ImpactFired=true;Shake=ReducedMotion?0:.24f;PaperTime=.8f;Sound(TEXT("DeskHit"),.9f);Sound(TEXT("Objection"),.7f);}if(Before>0&&Impact==0&&VerdictPending){VerdictPending=false;StartGavel();}}
 if(GavelTime>0){GavelTime=FMath::Max(0.f,GavelTime-D);if(!GavelFired&&2.2f-GavelTime>=.72f){GavelFired=true;Shake=ReducedMotion?0:.18f;Sound(TEXT("GavelHit"),.85f);}}
 Shake=FMath::Max(0.f,Shake-D);PaperTime=FMath::Max(0.f,PaperTime-D);
 UpdateSpeech(D);UpdateMusic(D);
 UpdateProps(D);AnimateCast();SelectCamera();
}
void AChaosHUD::SetScreen(EChaosScreen V){Screen=V;FocusIndex=-1;Buttons.Empty();PreviousButtons.Empty();if(ExhibitActor)ExhibitActor->SetActorHiddenInGame(V!=EChaosScreen::Inspect);}
void AChaosHUD::Record(const FString& S){if(S.IsEmpty()||S.EndsWith(TEXT(": ")))return;if(History.IsEmpty()||History.Last()!=S){History.Add(S);if(History.Num()>100)History.RemoveAt(0);}}
bool AChaosHUD::SelectCase(int32 Index){
 if(!CaseLibrary.IsValidIndex(Index))return false;StopSpeech();ActiveCase=Index;Case=CaseLibrary[Index];Error.Empty();CaseFailed=false;Resolution=false;Impact=GavelTime=0;Feedback.Empty();return Case->Validate(Error);
}
void AChaosHUD::LoseLife(const FString& Reason){
 StopSpeech();++Wrong;Credibility=FMath::Max(0,Credibility-1);ChaosPulse=FMath::Min(1.f,ChaosPulse+.25f);Feedback=Reason;Record(Reason);Sound(TEXT("Wrong"),.45f);
 if(Credibility==0){CaseFailed=true;Resolution=false;Impact=GavelTime=0;SetScreen(EChaosScreen::Failed);}Save();
}
void AChaosHUD::BeginCase(){StopSpeech();CaseFailed=false;CourtHeat=ChaosPulse=0;Completed=false;Phase=0;Statement=0;Dialogue=0;Selected=0;Credibility=3;Correct=Wrong=Presses=Inspections=0;CaseSeconds=0;Resolution=false;ResolutionStage=-1;Impact=GavelTime=0;VerdictPending=false;Inspected.Empty();History.Empty();ClosingSolved=false;Feedback.Empty();LastText.Empty();SetScreen(EChaosScreen::Play);Save();}
void AChaosHUD::Next(){
 if(CaseFailed)return;
 if(Impact>0){Action(TEXT("skip"));return;}const auto L=CurrentLine();if(!InstantText&&LineElapsed*RevealSpeed<L.Text.Len()){LineElapsed=10000;return;}
 Record(L.Speaker+TEXT(": ")+L.Text);Feedback.Empty();
 if(Resolution){++Dialogue;if(Case->Stages[ResolutionStage].Resolution.IsValidIndex(Dialogue))return;FinishResolution();return;}
 if(Phase==0||Phase==1){++Dialogue;const auto& A=Phase==0?Case->Consultation:Case->Opening;if(!A.IsValidIndex(Dialogue)){++Phase;Dialogue=0;if(Phase==1)StartGavel();}Save();return;}
 if(Phase==FinalPhase()){if(GavelTime>0){GavelTime=0;return;}++Dialogue;if(!Case->Verdict.IsValidIndex(Dialogue)){Completed=true;SetScreen(EChaosScreen::Results);Sound(TEXT("Victory"),.6f);}Save();return;}
 if(const auto S=Stage())Statement=(Statement+1)%S->Statements.Num();Save();
}
void AChaosHUD::FinishResolution(){Resolution=false;Dialogue=0;ResolutionStage=-1;if(Phase==FinalPhase()){if(ClosingSolved)StartGavel();else SetScreen(EChaosScreen::Closing);}Save();}
void AChaosHUD::StartObjection(){ChaosPulse=FMath::Min(1.f,ChaosPulse+.38f);Impact=ReducedMotion?.35f:3.2f;ImpactFired=false;Feedback.Empty();}
void AChaosHUD::StartGavel(){ChaosPulse=FMath::Min(1.f,ChaosPulse+.08f);GavelTime=ReducedMotion?.8f:2.2f;GavelFired=false;}
void AChaosHUD::Sound(const FString& Name,float Volume){const float Bus=Name==TEXT("Objection")?VoiceVolume:EffectsVolume;if(MasterVolume*Bus<=0)return;const FString Path=TEXT("/Game/Audio/")+Name+TEXT(".")+Name;auto Asset=LoadObject<USoundBase>(nullptr,*Path);if(Asset)UGameplayStatics::PlaySound2D(this,Asset,MasterVolume*Bus*Volume);}
void AChaosHUD::Save(){
 if(Phase<0)return;
 // Preserve a legacy single-slot trial before another case updates Continue.
 TSharedPtr<FJsonObject> Previous;if(Court::Read(Court::File(TEXT("Trial.json")),Previous))for(auto Data:CaseLibrary)if(Data->CaseId!=Case->CaseId&&Data->CaseId.ToString()==Court::String(Previous,TEXT("case"))){
  const int32 V=static_cast<int32>(Court::Number(Previous,TEXT("version"),0));const int32 P=static_cast<int32>(Court::Number(Previous,TEXT("phase"),-1));const FString Slot=Court::File(TEXT("Trial_")+Data->CaseId.ToString()+TEXT(".json"));
  if((V==2||V==3)&&P>=0&&P<=Data->Stages.Num()+2&&!IFileManager::Get().FileExists(*Slot))if(!Court::Write(Slot,Previous.ToSharedRef())){Feedback=TEXT("The previous trial could not be preserved. Please check available disk space.");return;}
 }
 auto J=MakeShared<FJsonObject>();J->SetNumberField(TEXT("version"),3);J->SetStringField(TEXT("case"),Case->CaseId.ToString());J->SetNumberField(TEXT("phase"),Phase);J->SetNumberField(TEXT("statement"),Statement);J->SetNumberField(TEXT("dialogue"),Dialogue);J->SetNumberField(TEXT("credibility"),Credibility);J->SetNumberField(TEXT("selected"),Selected);J->SetNumberField(TEXT("correct"),Correct);J->SetNumberField(TEXT("wrong"),Wrong);J->SetNumberField(TEXT("presses"),Presses);J->SetNumberField(TEXT("seconds"),CaseSeconds);J->SetBoolField(TEXT("failed"),CaseFailed);J->SetBoolField(TEXT("completed"),Completed);J->SetBoolField(TEXT("closing_solved"),ClosingSolved);J->SetBoolField(TEXT("resolution"),Resolution);J->SetNumberField(TEXT("resolution_stage"),ResolutionStage);
 TArray<TSharedPtr<FJsonValue>> Lines;for(const auto& S:History)Lines.Add(MakeShared<FJsonValueString>(S));J->SetArrayField(TEXT("history"),Lines);TArray<TSharedPtr<FJsonValue>> Seen;for(const auto& N:Inspected)Seen.Add(MakeShared<FJsonValueString>(N.ToString()));J->SetArrayField(TEXT("inspected"),Seen);
 Court::Write(Court::File(TEXT("Trial_")+Case->CaseId.ToString()+TEXT(".json")),J);
 if(!Court::Write(Court::File(TEXT("Trial.json")),J))Feedback=TEXT("The trial could not be saved. Please check available disk space.");
}
bool AChaosHUD::Load(){return ReadTrial(Court::File(TEXT("Trial.json")));}
bool AChaosHUD::ReadTrial(const FString& Path){
 TSharedPtr<FJsonObject> J;if(!Court::Read(Path,J)){Feedback=TEXT("No readable saved trial was found. You can start a new case.");return false;}
 int32 Found=INDEX_NONE;for(int32 I=0;I<CaseLibrary.Num();++I)if(CaseLibrary[I]->CaseId.ToString()==Court::String(J,TEXT("case")))Found=I;
 const int32 Version=static_cast<int32>(Court::Number(J,TEXT("version"),0));if(Found==INDEX_NONE||(Version!=2&&Version!=3)){Feedback=TEXT("This save does not match an installed case.");return false;}
 const int32 P=static_cast<int32>(Court::Number(J,TEXT("phase"),-1));if(P<0||P>CaseLibrary[Found]->Stages.Num()+2){Feedback=TEXT("This save does not match the current case. Start a new trial.");return false;}
 SelectCase(Found);Phase=P;Statement=0;if(const auto S=Stage())Statement=FMath::Clamp(static_cast<int32>(Court::Number(J,TEXT("statement"),0)),0,S->Statements.Num()-1);Credibility=FMath::Clamp(static_cast<int32>(Court::Number(J,TEXT("credibility"),3)),0,3);Selected=FMath::Clamp(static_cast<int32>(Court::Number(J,TEXT("selected"),0)),0,Case->Evidence.Num()-1);Dialogue=FMath::Clamp(static_cast<int32>(Court::Number(J,TEXT("dialogue"),0)),0,10);Correct=FMath::Clamp(static_cast<int32>(Court::Number(J,TEXT("correct"),0)),0,Case->Stages.Num());Wrong=FMath::Clamp(static_cast<int32>(Court::Number(J,TEXT("wrong"),0)),0,999);Presses=FMath::Clamp(static_cast<int32>(Court::Number(J,TEXT("presses"),0)),0,999);CaseSeconds=FMath::Clamp(static_cast<float>(Court::Number(J,TEXT("seconds"),0)),0.f,86400.f);Completed=Court::Boolean(J,TEXT("completed"));CaseFailed=Court::Boolean(J,TEXT("failed"))||(!Completed&&Credibility==0);ClosingSolved=Court::Boolean(J,TEXT("closing_solved"));ResolutionStage=FMath::Clamp(static_cast<int32>(Court::Number(J,TEXT("resolution_stage"),-1)),-1,Case->Stages.Num()-1);Resolution=Court::Boolean(J,TEXT("resolution"))&&Case->Stages.IsValidIndex(ResolutionStage);
 int32 Count=Resolution?Case->Stages[ResolutionStage].Resolution.Num():Phase==0?Case->Consultation.Num():Phase==1?Case->Opening.Num():Phase==FinalPhase()?Case->Verdict.Num():1;Dialogue=FMath::Clamp(Dialogue,0,FMath::Max(0,Count-1));
 History.Empty();const TArray<TSharedPtr<FJsonValue>>* A;if(J->TryGetArrayField(TEXT("history"),A))for(const auto& V:*A){FString S;if(V->TryGetString(S)&&S.Len()<2000&&History.Num()<100)History.Add(S);}
 Inspected.Empty();if(J->TryGetArrayField(TEXT("inspected"),A))for(const auto& V:*A){FString S;if(V->TryGetString(S))for(const auto& E:Case->Evidence)if(E.Id==FName(S))Inspected.Add(E.Id);}Inspections=Inspected.Num();Impact=0;GavelTime=0;LastText.Empty();Feedback.Empty();if(!Unlocked(Selected))Selected=0;SetScreen(CaseFailed?EChaosScreen::Failed:Completed&&Phase==FinalPhase()?EChaosScreen::Results:Phase==FinalPhase()&&!Resolution&&!ClosingSolved?EChaosScreen::Closing:EChaosScreen::Play);if(!CaseFailed&&Phase==FinalPhase()&&!Completed&&!Resolution&&ClosingSolved)StartGavel();return true;
}
void AChaosHUD::SaveSettings(){auto J=MakeShared<FJsonObject>();J->SetNumberField(TEXT("master"),MasterVolume);J->SetNumberField(TEXT("music"),MusicVolume);J->SetNumberField(TEXT("effects"),EffectsVolume);J->SetNumberField(TEXT("voice"),VoiceVolume);J->SetNumberField(TEXT("text_size"),TextScale);J->SetNumberField(TEXT("reveal"),RevealSpeed);J->SetNumberField(TEXT("quality"),Quality);J->SetBoolField(TEXT("instant"),InstantText);J->SetBoolField(TEXT("motion"),ReducedMotion);J->SetBoolField(TEXT("contrast"),HighContrast);Court::Write(Court::File(TEXT("Preferences.json")),J);}
void AChaosHUD::LoadSettings(){TSharedPtr<FJsonObject> J;if(Court::Read(Court::File(TEXT("Preferences.json")),J)){MasterVolume=FMath::Clamp(static_cast<float>(Court::Number(J,TEXT("master"),.8)),0.f,1.f);MusicVolume=FMath::Clamp(static_cast<float>(Court::Number(J,TEXT("music"),.4)),0.f,1.f);EffectsVolume=FMath::Clamp(static_cast<float>(Court::Number(J,TEXT("effects"),.8)),0.f,1.f);VoiceVolume=FMath::Clamp(static_cast<float>(Court::Number(J,TEXT("voice"),.9)),0.f,1.f);TextScale=FMath::Clamp(static_cast<float>(Court::Number(J,TEXT("text_size"),1)),.9f,1.3f);RevealSpeed=FMath::Clamp(static_cast<float>(Court::Number(J,TEXT("reveal"),42)),20.f,80.f);Quality=FMath::Clamp(static_cast<int32>(Court::Number(J,TEXT("quality"),2)),0,3);InstantText=Court::Boolean(J,TEXT("instant"));ReducedMotion=Court::Boolean(J,TEXT("motion"));HighContrast=Court::Boolean(J,TEXT("contrast"));}if(auto Settings=GEngine->GetGameUserSettings()){Settings->SetOverallScalabilityLevel(Quality);Settings->SetFrameRateLimit(120);Settings->ApplyNonResolutionSettings();}}
void AChaosHUD::AnimateCast(){
 const auto L=CurrentLine();const bool Talking=(Screen==EChaosScreen::Play||Screen==EChaosScreen::Closing)&&Phase>=0&&!SpeechPaused&&!SpeechSpeaker.IsEmpty();
 for(auto& Pair:Cast){auto Actor=Pair.Value.Get();if(!Actor)continue;auto C=Actor->FindComponentByClass<USkeletalMeshComponent>();if(!C)continue;const FString Name=Pair.Key.ToString();FString Mood=TEXT("Listening");
  if(Phase<0||(Screen!=EChaosScreen::Play&&Screen!=EChaosScreen::Closing))Mood=TEXT("Idle");else if(Name==SpeechSpeaker&&Talking)Mood=Name==L.Speaker?L.Emotion.ToString():TEXT("Speaking");
  if(StageIndex()>=1&&Name==TEXT("Victor")&&Phase<FinalPhase())Mood=TEXT("Angry");
  if(!Feedback.IsEmpty()&&Name==TEXT("Milo")&&Stage())Mood=TEXT("Nervous");
  if(Screen==EChaosScreen::Results){if(Name==TEXT("Oliver")||Name==TEXT("Benny"))Mood=TEXT("Celebrate");if(Name==TEXT("Victor"))Mood=TEXT("Embarrassed");}
  if(Impact>0){if(Name==TEXT("Oliver"))Mood=!ReducedMotion&&Impact>1.3f?TEXT("Slam"):TEXT("Pointing");if(Name==TEXT("Milo"))Mood=TEXT("Shock");if(Name==TEXT("Victor"))Mood=TEXT("Angry");}
  if(GavelTime>0&&Name==TEXT("Bumble"))Mood=TEXT("Gavel");
  float Open=Talking&&Name==SpeechSpeaker?MouthAmount:0;
  if(Impact>0&&Name==TEXT("Milo"))Open=1;
  if(Impact>0&&Name==TEXT("Oliver")){float E=3.2f-Impact;if(E>.72f&&E<1.8f)Open=.6f+.25f*FMath::Abs(FMath::Sin(E*18));}
  C->SetMorphTarget(TEXT("TalkOpen"),Open);C->SetMorphTarget(TEXT("SmileHide"),FMath::Clamp(Open*10,0.f,1.f));
  FString Key=TEXT("AN_")+Name+TEXT("_")+Mood;
  if(!Animations.Contains(Key))Animations.Add(Key,LoadObject<UAnimationAsset>(nullptr,*(TEXT("/Game/Characters/Animations/")+Key+TEXT(".")+Key)));
  auto Asset=Animations[Key];if(!Asset){Key=TEXT("AN_")+Name+TEXT("_Idle");if(!Animations.Contains(Key))Animations.Add(Key,LoadObject<UAnimationAsset>(nullptr,*(TEXT("/Game/Characters/Animations/")+Key+TEXT(".")+Key)));Asset=Animations[Key];}
  if(Asset){auto Instance=C->GetSingleNodeInstance();if(!Instance||Instance->GetCurrentAsset()!=Asset){C->PlayAnimation(Asset,Mood!=TEXT("Slam")&&Mood!=TEXT("Gavel"));UE_LOG(LogTemp,Display,TEXT("CAST_PERFORMANCE %s %s"),*Name,*Mood);}}
 }
}
void AChaosHUD::UpdateProps(float D){
 if(auto Oliver=Cast.FindRef(TEXT("Oliver")).Get())if(CastRest.Contains(TEXT("Oliver"))){auto T=CastRest[TEXT("Oliver")];float Lean=0;if(Impact>1.3f&&!ReducedMotion){float E=3.2f-Impact;Lean=E<.2f?Court::Ease(E/.2f):1.f;}Oliver->SetActorLocation(T.GetLocation()+FVector(0,-25*Lean,0));}
 if(GavelActor){
  if(GavelTime>0){auto Judge=Cast.FindRef(TEXT("Bumble")).Get();auto C=Judge?Judge->FindComponentByClass<USkeletalMeshComponent>():nullptr;if(C){float E=2.2f-GavelTime;float Swing=E<.52f?0:E<.72f?Court::Ease((E-.52f)/.2f):E<1.4f?1:1-Court::Ease((E-1.4f)/.5f);GavelActor->SetActorLocation(C->GetSocketLocation(TEXT("Hand_R"))+FVector(0,-15,12));GavelActor->SetActorRotation(FRotator(FMath::Lerp(90.f,180.f,Swing),0,0));}}
  else{GavelActor->SetActorLocation(FVector(35,455,206.5));GavelActor->SetActorRotation(FRotator(0,90,90));}
 }
 if(Screen==EChaosScreen::Inspect&&ExhibitActor&&Case->Evidence.IsValidIndex(Selected)){
  auto M=Case->Evidence[Selected].Exhibit;ExhibitActor->SetActorHiddenInGame(!M);if(M){ExhibitActor->GetStaticMeshComponent()->SetStaticMesh(M);float MX=0,MY=0;GetOwningPlayerController()->GetMousePosition(MX,MY);float DX=0,DY=0;GetOwningPlayerController()->GetInputMouseDelta(DX,DY);if(GetOwningPlayerController()->IsInputKeyDown(EKeys::LeftMouseButton)&&MX/SX<760&&MY/SY>150&&MY/SY<590)ExhibitYaw+=DX*.7f;ExhibitYaw+=D*8;float Scale=ExhibitZoom*(Case->Evidence[Selected].Id==TEXT("mustard")?1.17f:1.6f);auto Bounds=M->GetBounds();ExhibitActor->SetActorScale3D(FVector(Scale,-Scale,Scale));ExhibitActor->SetActorRotation(FRotator(0,ExhibitYaw,0));ExhibitActor->SetActorLocation(FVector(0,-3000,105-(Bounds.Origin.Z-Bounds.BoxExtent.Z)*Scale));}
 }
}
void AChaosHUD::SelectCamera(){
 auto ForSpeaker=[](const FString& S)->FName{if(S==TEXT("Oliver"))return TEXT("Defense");if(S==TEXT("Victor"))return TEXT("Prosecutor");if(S==TEXT("Benny"))return TEXT("Client");if(S==TEXT("Milo"))return TEXT("Witness");if(S==TEXT("Brick"))return TEXT("Bailiff");return TEXT("Judge");};
 FName Shot=Phase>=0?ForSpeaker(!SpeechSpeaker.IsEmpty()&&!SpeechPaused?SpeechSpeaker:CurrentLine().Speaker):FName(TEXT("Wide"));if(Screen==EChaosScreen::Record||Screen==EChaosScreen::Cases||Screen==EChaosScreen::Settings||Screen==EChaosScreen::Credits||Screen==EChaosScreen::History||Screen==EChaosScreen::Results)Shot=TEXT("Wide");if(Screen==EChaosScreen::Inspect)Shot=Case->Evidence[Selected].Exhibit?TEXT("Inspect"):TEXT("Wide");
 if(GavelTime>0)Shot=TEXT("Judge");if(Impact>0){if(3.2f-Impact<1.7f)Shot=TEXT("Defense");else if(Case->Stages.IsValidIndex(ResolutionStage))Shot=ForSpeaker(Case->Stages[ResolutionStage].Speaker);}
 for(auto& Pair:Cameras)if(auto Camera=Pair.Value.Get())if(CameraRest.Contains(Pair.Key))Camera->SetActorTransform(CameraRest[Pair.Key]);
 if(auto Camera=Cameras.FindRef(Shot).Get()){auto P=GetOwningPlayerController();if(P->GetViewTarget()!=Camera)P->SetViewTargetWithBlend(Camera,ReducedMotion?0:.25f);if(Shake>0&&!ReducedMotion){auto R=Camera->GetActorRotation();R.Roll+=FMath::Sin(GetWorld()->GetTimeSeconds()*85)*Shake*3;R.Pitch+=FMath::Cos(GetWorld()->GetTimeSeconds()*65)*Shake;Camera->SetActorRotation(R);}}
}
void AChaosHUD::Action(FString Id){
 if(CaseFailed&&Id!=TEXT("restart")&&Id!=TEXT("menu")&&Id!=TEXT("quit")&&Id!=TEXT("cases")&&Id!=TEXT("back")&&!Id.StartsWith(TEXT("case_")))return;
 if(Id==TEXT("restart")){BeginCase();return;}
 if(Id.StartsWith(TEXT("case_"))){const int32 I=FCString::Atoi(*Id.Mid(5));if(SelectCase(I)){const FString Slot=Court::File(TEXT("Trial_")+Case->CaseId.ToString()+TEXT(".json"));if(IFileManager::Get().FileExists(*Slot)){if(!ReadTrial(Slot))BeginCase();}else{TSharedPtr<FJsonObject> Legacy;if(Court::Read(Court::File(TEXT("Trial.json")),Legacy)&&Court::String(Legacy,TEXT("case"))==Case->CaseId.ToString()){if(!Load())BeginCase();}else BeginCase();}}return;}
 if(!Case||!Error.IsEmpty()){if(Id==TEXT("quit"))GetOwningPlayerController()->ConsoleCommand(TEXT("quit"));return;}
 if(Id!=TEXT("rotate_l")&&Id!=TEXT("rotate_r"))Sound(TEXT("UITick"),.22f);
 if(Id==TEXT("skip")){Impact=0;ImpactFired=true;Shake=PaperTime=0;if(VerdictPending){VerdictPending=false;StartGavel();}return;}
 if(Id==TEXT("start")){Completed=false;BeginCase();return;}
 if(Id==TEXT("load")){Load();return;}
 if(Id==TEXT("quit")){if(Phase>=0)Save();GetOwningPlayerController()->ConsoleCommand(TEXT("quit"));return;}
 if(Id==TEXT("menu")){if(Phase>=0)Save();StopSpeech();CaseFailed=false;Phase=-1;Resolution=false;Impact=GavelTime=0;Feedback.Empty();SetScreen(EChaosScreen::Play);return;}
 if(Id==TEXT("settings")){ReturnScreen=Screen;SetScreen(EChaosScreen::Settings);return;}
 if(Id==TEXT("cases")){CaseReturn=Screen;SetScreen(EChaosScreen::Cases);return;}
 if(Id==TEXT("credits")){ReturnScreen=Screen;SetScreen(EChaosScreen::Credits);return;}
 if(Id==TEXT("back")){if(CaseFailed){SetScreen(EChaosScreen::Failed);return;}if(Screen==EChaosScreen::Cases)SetScreen(CaseReturn);else if(Screen==EChaosScreen::Settings){SaveSettings();SetScreen(ReturnScreen);}else if(Screen==EChaosScreen::Inspect)SetScreen(EChaosScreen::Record);else if(Screen==EChaosScreen::History)SetScreen(HistoryReturn);else if(Screen==EChaosScreen::Record)SetScreen(RecordReturn);else SetScreen(EChaosScreen::Play);return;}
 if(Id==TEXT("history")){HistoryPage=0;if(Screen==EChaosScreen::History)SetScreen(HistoryReturn);else{HistoryReturn=Screen;SetScreen(EChaosScreen::History);}return;}
 if(Id==TEXT("history_prev")){HistoryPage=FMath::Max(0,HistoryPage-1);return;}
 if(Id==TEXT("history_next")){HistoryPage=FMath::Min(FMath::Max(0,(History.Num()-1)/4),HistoryPage+1);return;}
 if(Screen==EChaosScreen::Settings){
  if(Id==TEXT("master_less"))MasterVolume=FMath::Max(0.f,MasterVolume-.1f);if(Id==TEXT("master_more"))MasterVolume=FMath::Min(1.f,MasterVolume+.1f);
  if(Id==TEXT("music_less"))MusicVolume=FMath::Max(0.f,MusicVolume-.1f);if(Id==TEXT("music_more"))MusicVolume=FMath::Min(1.f,MusicVolume+.1f);
  if(Id==TEXT("effects_less"))EffectsVolume=FMath::Max(0.f,EffectsVolume-.1f);if(Id==TEXT("effects_more"))EffectsVolume=FMath::Min(1.f,EffectsVolume+.1f);
  if(Id==TEXT("voice_less"))VoiceVolume=FMath::Max(0.f,VoiceVolume-.1f);if(Id==TEXT("voice_more"))VoiceVolume=FMath::Min(1.f,VoiceVolume+.1f);
  if(Id==TEXT("text_less"))TextScale=FMath::Max(.9f,TextScale-.1f);if(Id==TEXT("text_more"))TextScale=FMath::Min(1.3f,TextScale+.1f);
  if(Id==TEXT("speed"))RevealSpeed=RevealSpeed<40?42:RevealSpeed<60?70:24;
  if(Id==TEXT("instant"))InstantText=!InstantText;if(Id==TEXT("motion"))ReducedMotion=!ReducedMotion;if(Id==TEXT("contrast"))HighContrast=!HighContrast;
  if(Id==TEXT("quality")){Quality=(Quality+1)%4;if(auto S=GEngine->GetGameUserSettings()){S->SetOverallScalabilityLevel(Quality);S->ApplyNonResolutionSettings();}}
  if(Id==TEXT("window")){if(auto S=GEngine->GetGameUserSettings()){S->SetFullscreenMode(S->GetFullscreenMode()==EWindowMode::Windowed?EWindowMode::WindowedFullscreen:EWindowMode::Windowed);S->ApplyResolutionSettings(false);S->ConfirmVideoMode();S->SaveSettings();}}
  SaveSettings();return;
 }
 if(Id==TEXT("evidence")){if(Impact>0||Resolution)return;if(Screen==EChaosScreen::Record)SetScreen(RecordReturn);else if(Stage()||Screen==EChaosScreen::Closing){RecordReturn=Screen;SetScreen(EChaosScreen::Record);}return;}
 if(Id.StartsWith(TEXT("ev_"))){int32 I=FCString::Atoi(*Id.Mid(3));if(Unlocked(I)){Selected=I;InspectionRead=false;}return;}
 if(Id==TEXT("inspect")){if(!Unlocked(Selected))return;ExhibitYaw=0;ExhibitZoom=1;InspectionRead=Inspected.Contains(Case->Evidence[Selected].Id);SetScreen(EChaosScreen::Inspect);return;}
 if(Id==TEXT("detail")){InspectionRead=true;Inspected.Add(Case->Evidence[Selected].Id);Inspections=Inspected.Num();Record(TEXT("INSPECTION: ")+Case->Evidence[Selected].Title+TEXT(" - ")+Case->Evidence[Selected].Inspection);Save();return;}
 if(Id==TEXT("rotate_l")){ExhibitYaw-=30;return;}if(Id==TEXT("rotate_r")){ExhibitYaw+=30;return;}if(Id==TEXT("zoom_in")){ExhibitZoom=FMath::Min(1.4f,ExhibitZoom+.1f);return;}if(Id==TEXT("zoom_out")){ExhibitZoom=FMath::Max(.6f,ExhibitZoom-.1f);return;}
 if(Id.StartsWith(TEXT("conclusion_"))&&Screen==EChaosScreen::Closing){int32 Choice=FCString::Atoi(*Id.Mid(11));if(Choice==Case->CorrectConclusion){ClosingSolved=true;Dialogue=0;Record(TEXT("CLOSING ARGUMENT: ")+Case->Conclusions[Choice]);Feedback.Empty();SetScreen(EChaosScreen::Play);StartGavel();Save();}else{LoseLife(TEXT("BUMBLE: The record supports a timeline, counsel. Avoid inventing a crime."));}return;}
 if(Id==TEXT("next")){Next();return;}
 if(Id==TEXT("prev")){if(Stage()&&!Resolution&&Impact<=0){Statement=(Statement+Stage()->Statements.Num()-1)%Stage()->Statements.Num();Feedback.Empty();Save();}return;}
 if(Id==TEXT("press")){if(const auto S=Stage())if(!Resolution&&Impact<=0){StopSpeech();ChaosPulse=FMath::Min(1.f,ChaosPulse+.14f);Feedback=S->Statements[Statement].Press;++Presses;Record(TEXT("PRESS: ")+Feedback);LineElapsed=0;Sound(TEXT("Press"),.35f);Save();}return;}
 if(Id==TEXT("present")){const auto S=Stage();if(!S||Resolution||Impact>0||!Unlocked(Selected))return;SetScreen(EChaosScreen::Play);
  if(S->Contradiction==Statement&&S->Evidence==Case->Evidence[Selected].Id){ResolutionStage=StageIndex();Resolution=true;Dialogue=0;++Correct;++Phase;Statement=0;StartObjection();Record(TEXT("CONTRADICTION: ")+Case->Evidence[Selected].Title);}
  else{LoseLife(TEXT("BUMBLE: That evidence does not contradict this statement. Read both closely, counsel."));}Save();return;
 }
}
void AChaosHUD::NotifyHitBoxClick(FName N){Action(N.ToString());}
void AChaosHUD::Label(const FString& S,float X,float Y,float Size,FLinearColor C){
 // Rasterize TrueType glyphs at their final pixel size instead of enlarging a bitmap atlas.
 FCanvasTextItem Text(FVector2D(FMath::RoundToFloat(X*SX),FMath::RoundToFloat(Y*SY)),FText::FromString(S),Court::UIFont(Size,FMath::Min(SX,SY),RuntimeUIFont),C);
 Text.BlendMode=SE_BLEND_Translucent;Canvas->DrawItem(Text);
}
void AChaosHUD::Panel(float X,float Y,float W,float H,FLinearColor C){DrawRect(C,X*SX,Y*SY,W*SX,H*SY);}
void AChaosHUD::Texture(UTexture2D* A,float X,float Y,float W,float H,float Alpha){if(A)DrawTexture(A,X*SX,Y*SY,W*SX,H*SY,0,0,1,1,FLinearColor(1,1,1,Alpha),BLEND_Translucent);}
void AChaosHUD::Sprite(const FString& Name,float X,float Y,float W,float H,float Alpha,float Rotation){if(!Textures.Contains(Name))Textures.Add(Name,LoadObject<UTexture2D>(nullptr,*(TEXT("/Game/UI/")+Name+TEXT(".")+Name)));if(auto T=Textures[Name])DrawTexture(T,X*SX,Y*SY,W*SX,H*SY,0,0,1,1,FLinearColor(1,1,1,Alpha),BLEND_Translucent,1,false,Rotation,FVector2D(.5f,.5f));}
FString AChaosHUD::Wrap(const FString& S,float Width,float Size){FString Out;TArray<FString> Paragraphs;S.ParseIntoArray(Paragraphs,TEXT("\n"),false);for(int32 I=0;I<Paragraphs.Num();++I){TArray<FString> Words;Paragraphs[I].ParseIntoArrayWS(Words);FString Line;for(const auto& W:Words){FString Candidate=Line.IsEmpty()?W:Line+TEXT(" ")+W;const auto Measure=FSlateApplication::Get().GetRenderer()->GetFontMeasureService();const float TW=Measure->Measure(FStringView(Candidate),Court::UIFont(Size,FMath::Min(SX,SY),RuntimeUIFont)).X;if(TW>Width*SX&&!Line.IsEmpty()){Out+=Line+TEXT("\n");Line=W;}else Line=Candidate;}Out+=Line;if(I<Paragraphs.Num()-1)Out+=TEXT("\n");}return Out;}
void AChaosHUD::Wrapped(const FString& S,float X,float Y,float Width,float Size,FLinearColor C,bool Reveal){FString W=Wrap(S,Width,Size);if(Reveal&&!InstantText)W=W.Left(FMath::Clamp(FMath::FloorToInt(LineElapsed*RevealSpeed),0,W.Len()));Label(W,X,Y,Size,C);}
void AChaosHUD::Button(const FString& Id,const FString& Caption,float X,float Y,float W,bool Enabled){
 float MX=0,MY=0;GetOwningPlayerController()->GetMousePosition(MX,MY);const bool Hover=MX>=X*SX&&MX<=(X+W)*SX&&MY>=Y*SY&&MY<=(Y+46)*SY;const bool Focus=FocusIndex==Buttons.Num();FString Skin=Id==TEXT("start")||Id==TEXT("present")||Id==TEXT("press")?TEXT("RedButton"):Id==TEXT("evidence")||Id==TEXT("inspect")||Id==TEXT("detail")?TEXT("TealButton"):TEXT("InkButton");Sprite(Skin,X,Y-(Enabled&&(Hover||Focus)?2:0),W,50,Enabled?1:.4f);Label(Caption,X+16,Y+13-(Enabled&&(Hover||Focus)?2:0),19,Enabled?Court::Cream:FLinearColor(.35f,.35f,.35f));if(Enabled){if(Focus)DrawRect(Court::Gold,(X+6)*SX,(Y+6)*SY,3*SX,32*SY);Buttons.Add(Id);AddHitBox(FVector2D(X*SX,Y*SY),FVector2D(W*SX,46*SY),FName(Id),true);}}
void AChaosHUD::DrawHUD(){
 Super::DrawHUD();if(!Canvas)return;SX=Canvas->SizeX/1280.f;SY=Canvas->SizeY/720.f;PreviousButtons=MoveTemp(Buttons);Buttons.Empty();auto P=GetOwningPlayerController();
 if(P->WasInputKeyJustPressed(EKeys::Tab)&&PreviousButtons.Num()){int32 Step=P->IsInputKeyDown(EKeys::LeftShift)||P->IsInputKeyDown(EKeys::RightShift)?-1:1;FocusIndex=(FocusIndex+Step+PreviousButtons.Num())%PreviousButtons.Num();}
 if(P->WasInputKeyJustPressed(EKeys::Enter)){if(PreviousButtons.IsValidIndex(FocusIndex))Action(PreviousButtons[FocusIndex]);else if(Screen==EChaosScreen::Play&&Phase>=0)Action(TEXT("next"));}
 if(P->WasInputKeyJustPressed(EKeys::Escape)){if(Screen!=EChaosScreen::Play)Action(TEXT("back"));else Action(TEXT("menu"));}
 if(P->WasInputKeyJustPressed(EKeys::SpaceBar)&&Screen==EChaosScreen::Play&&Phase>=0)Action(TEXT("next"));
 if(P->WasInputKeyJustPressed(EKeys::H)&&Phase>=0)Action(TEXT("history"));
 if(P->WasInputKeyJustPressed(EKeys::E)){if(Screen==EChaosScreen::Inspect)Action(TEXT("back"));else Action(TEXT("evidence"));}
 if(Screen==EChaosScreen::Play&&Stage()&&!Resolution){if(P->WasInputKeyJustPressed(EKeys::Left))Action(TEXT("prev"));if(P->WasInputKeyJustPressed(EKeys::Right))Action(TEXT("next"));if(P->WasInputKeyJustPressed(EKeys::Q))Action(TEXT("press"));}
 if(Screen==EChaosScreen::Record&&Case){int Step=P->WasInputKeyJustPressed(EKeys::Right)?1:P->WasInputKeyJustPressed(EKeys::Left)?-1:0;if(Step)for(int I=0;I<Case->Evidence.Num();++I){Selected=(Selected+Step+Case->Evidence.Num())%Case->Evidence.Num();if(Unlocked(Selected))break;}}
 if(Screen==EChaosScreen::Inspect){if(P->WasInputKeyJustPressed(EKeys::A))Action(TEXT("rotate_l"));if(P->WasInputKeyJustPressed(EKeys::D))Action(TEXT("rotate_r"));if(P->WasInputKeyJustPressed(EKeys::MouseScrollUp))Action(TEXT("zoom_in"));if(P->WasInputKeyJustPressed(EKeys::MouseScrollDown))Action(TEXT("zoom_out"));}
 if(HighContrast)Panel(0,0,1280,120,Court::Ink);
 Sprite(TEXT("InkButton"),20,12,330,94);Sprite(TEXT("Logo"),26,15,315,81);
 if(!Error.IsEmpty()){Sprite(TEXT("EvidencePanel"),55,180,1170,450);Label(TEXT("COURT IS IN RECESS"),90,220,34,Court::Ink);Wrapped(Error,90,300,1000,25,Court::Ink);Button(TEXT("quit"),TEXT("CLOSE GAME"),90,510,300);return;}
 if(!Case)return;
 if(Phase>=0){Sprite(TEXT("InkButton"),430,23,420,55);Label(FString::Printf(TEXT("%03d / "),ActiveCase+1)+Case->Title.ToUpper(),451,42,17,Court::Cream);Sprite(TEXT("InkButton"),896,16,190,80);Label(TEXT("TRIAL LIVES"),912,30,13,Court::Cream);for(int I=0;I<3;++I)Sprite(I<Credibility?TEXT("LifeHeart"):TEXT("LifeEmpty"),930+I*43,50,29,29);Button(TEXT("settings"),TEXT("OPTIONS"),1100,24,150);}
 switch(Screen){case EChaosScreen::Play:if(Phase<0)DrawMenu();else DrawTrial();break;case EChaosScreen::Record:DrawRecord();break;case EChaosScreen::Inspect:DrawInspection();break;case EChaosScreen::Settings:DrawSettings();break;case EChaosScreen::History:DrawHistory();break;case EChaosScreen::Results:DrawResults();break;
 case EChaosScreen::Cases:
  Sprite(TEXT("EvidencePanel"),55,145,1170,540);Label(TEXT("THE CASE FILES"),85,174,31,Court::Ink);Label(TEXT("THREE LIVES PER ATTEMPT / THE THIRD ERROR REQUIRES A RESTART"),85,218,15,Court::Red);
  for(int32 I=0;I<CaseLibrary.Num();++I){float X=85+I*378;auto C=CaseLibrary[I];const FString Poster=I==0?TEXT("CasePoster"):I==1?TEXT("Poster_Blackout"):TEXT("Poster_Charity");Sprite(Poster,X,255,350,200);Wrapped(C->Title,X,468,345,23,Court::Ink);Wrapped(C->Subtitle,X,515,345,16,Court::Teal);Button(TEXT("case_")+FString::FromInt(I),TEXT("OPEN CASE ")+FString::Printf(TEXT("%03d"),I+1),X,580,350);}
  Button(TEXT("back"),TEXT("BACK"),85,632,260);break;
 case EChaosScreen::Failed:
  Sprite(TEXT("EvidencePanel"),110,180,1060,470);Label(TEXT("DEFENSE OVERRULED"),165,225,43,Court::Red);Label(TEXT("NO LIVES LEFT / ATTEMPT ENDED"),165,293,22,Court::Ink);Wrapped(TEXT("Three unsupported answers ended this attempt. Restart this case from the consultation with three lives. Its deductions and unlocked evidence will reset."),165,345,945,25,Court::Ink);Button(TEXT("restart"),TEXT("RESTART CASE / 3 LIVES"),165,500,680);Button(TEXT("cases"),TEXT("CASE FILES"),165,570,320);Button(TEXT("menu"),TEXT("MAIN MENU"),505,570,340);break;
 case EChaosScreen::Closing:
  Sprite(TEXT("EvidencePanel"),55,160,1170,505);Label(TEXT("YOUR CLOSING ARGUMENT"),85,195,32,Court::Ink);Wrapped(Case->ClosingPrompt,85,255,1080,25*TextScale,Court::Ink);for(int I=0;I<Case->Conclusions.Num();++I)Button(TEXT("conclusion_")+FString::FromInt(I),Case->Conclusions[I],85,350+I*70,1090);if(!Feedback.IsEmpty())Wrapped(Feedback,85,585,1090,19,Court::Red);Button(TEXT("history"),TEXT("REVIEW TRANSCRIPT"),85,610,360);Button(TEXT("evidence"),TEXT("REVIEW EVIDENCE"),475,610,360);break;
 case EChaosScreen::Credits:
  Sprite(TEXT("EvidencePanel"),55,145,1170,540);Label(TEXT("THE PEOPLE VS. BORING COURTROOMS"),85,175,30,Court::Ink);Wrapped(TEXT("An original legal comedy.\nOliver Objection / Victor Vain / Judge Bumble\nBenny Buns / Milo Mopps / Officer Brick\n\nOriginal characters, story, graphics and music created for Courtroom Chaos.\nPowered by Unreal Engine. Art made with Blender.\nCharacter voices generated locally with Kokoro 82M."),85,245,520,23,Court::Ink);Label(TEXT("YOUR COURTROOM CONTROLS"),670,240,23,Court::Red);Wrapped(TEXT("Mouse / click buttons\nSpace / reveal text, continue, skip a cinematic\nLeft + Right / review testimony\nQ / press the witness\nE / court record     H / dialogue history\nA + D / rotate an inspected object\nMouse wheel / inspection zoom\nTab + Enter / keyboard button navigation\nEscape / back, or save and return to menu"),670,285,500,20,Court::Ink);Button(TEXT("back"),TEXT("BACK"),85,605,260);break;
 }
 if(Impact>0){float E=3.2f-Impact;if((E>=.68f&&E<1.8f)||ReducedMotion){if(!ReducedMotion)for(int I=0;I<20;++I){float A=I*2*PI/20;float X=640+FMath::Cos(A)*720,Y=330+FMath::Sin(A)*430;DrawLine(X*SX,Y*SY,(640+FMath::Cos(A)*470)*SX,(330+FMath::Sin(A)*135)*SY,FLinearColor(.9f,.65f,.2f,.55f),2*SX);}Sprite(TEXT("Objection"),180,200,920,220);}Button(TEXT("skip"),TEXT("SKIP / SPACE"),1030,128,210);}
 if(PaperTime>0&&!ReducedMotion){float E=.8f-PaperTime;Sprite(TEXT("Dust"),470-70*E,405-30*E,330+180*E,85+40*E,PaperTime*.5f);for(int I=0;I<5;++I){float X=530+I*45+(I-2)*130*E,Y=440-(140+I*20)*E+220*E*E;Sprite(TEXT("Paper"),X,Y,40,52,PaperTime/.8f,(I-2)*25+E*130);}}
}
void AChaosHUD::DrawMenu(){
 Sprite(TEXT("Dialogue"),55,180,570,470);Label(FString::Printf(TEXT("CASE %03d"),ActiveCase+1),89,215,20,Court::Red);Wrapped(Case->Title.ToUpper(),89,250,490,38,Court::Ink);Wrapped(Case->Subtitle,89,347,490,20,Court::Ink);
 Button(TEXT("start"),TEXT("TAKE THE CASE  >"),89,405,490);Button(TEXT("load"),TEXT("CONTINUE"),89,463,237);Button(TEXT("cases"),TEXT("CASE FILES"),341,463,238);Button(TEXT("settings"),TEXT("SETTINGS"),89,520,237);Button(TEXT("credits"),TEXT("CREDITS / CONTROLS"),341,520,238);Button(TEXT("quit"),TEXT("LEAVE COURT"),89,578,490);if(!Feedback.IsEmpty())Wrapped(Feedback,65,660,1140,18,Court::Cream);
}
void AChaosHUD::DrawTrial(){
 const auto L=CurrentLine();if(Stage()&&!Resolution){Sprite(TEXT("NameTab"),450,110,380,46);Label(TEXT("CROSS-EXAMINATION"),482,123,21,Court::Cream);}
 Sprite(TEXT("Dialogue"),35,495,1210,208);Sprite(TEXT("NameTab"),57,468,420,48);
 FString Speaker=L.Speaker==TEXT("Oliver")?TEXT("OLIVER OBJECTION / DEFENSE"):L.Speaker==TEXT("Victor")?TEXT("VICTOR VAIN / PROSECUTION"):L.Speaker==TEXT("Benny")?TEXT("BENNY BUNS / YOUR CLIENT"):L.Speaker==TEXT("Milo")?TEXT("MILO MOPPS / MAINTENANCE"):L.Speaker==TEXT("Brick")?TEXT("OFFICER BRICK / BAILIFF"):TEXT("THE HONORABLE JUDGE BUMBLE");Label(Speaker,78,482,19,Court::Cream);
 if(Stage()&&!Resolution)Label(FString::Printf(TEXT("STATEMENT %02d / %02d"),Statement+1,Stage()->Statements.Num()),995,512,14,Court::Ink);
 Wrapped(L.Text,70,535,1130,25*TextScale,Court::Ink,true);
 if(!Feedback.IsEmpty())Wrapped(Feedback,70,598,1110,18,Court::Teal);
 if(Stage()){Sprite(TEXT("InkButton"),20,115,325,37);Label(CourtHeat<.25f?TEXT("COURT TEMPER / ORDERLY"):CourtHeat<.5f?TEXT("COURT TEMPER / RESTLESS"):CourtHeat<.78f?TEXT("COURT TEMPER / HEATED"):TEXT("COURT TEMPER / MAYHEM"),36,125,15,Court::Cream);}
 if(Phase==FinalPhase()&&!Resolution&&Dialogue>=1&&LineElapsed<2)Sprite(TEXT("Verdict"),275,210,730,190,FMath::Min(1.f,2-LineElapsed));
 if(Impact>0)return;
 if(Stage()&&!Resolution){Button(TEXT("prev"),TEXT("<"),66,637,65);Button(TEXT("next"),TEXT(">"),141,637,65);Button(TEXT("history"),TEXT("HISTORY [H]"),225,637,185);Button(TEXT("press"),TEXT("PRESS [Q]"),660,637,215);Button(TEXT("evidence"),TEXT("RECORD [E]"),895,637,310);}
 else{Button(TEXT("history"),TEXT("HISTORY [H]"),70,637,220);Button(TEXT("next"),GavelTime>0?TEXT("SKIP GAVEL / SPACE"):TEXT("CONTINUE / SPACE  >"),850,637,355);}
}
void AChaosHUD::DrawRecord(){
 Sprite(TEXT("EvidencePanel"),35,125,1210,550);Label(TEXT("THE COURT RECORD"),65,151,31,Court::Ink);Label(TEXT("INSPECT THE FACTS. THEN MAKE YOUR CASE."),65,198,15,Court::Red);
 for(int I=0;I<Case->Evidence.Num();++I){const auto& E=Case->Evidence[I];float Y=240+I*56;Texture(E.Illustration,65,Y,61,47,Unlocked(I)?1:.25f);Button(TEXT("ev_")+FString::FromInt(I),Unlocked(I)?E.Title:TEXT("NOT YET ENTERED"),140,Y,290,Unlocked(I));if(Selected==I)Panel(131,Y+7,4,32,Court::Gold);}
 const auto& E=Case->Evidence[Selected];Label(E.Title,475,233,27,Court::Ink);Label(E.Category.ToUpper(),475,277,15,Court::Red);Texture(E.Illustration,790,218,340,250);Wrapped(E.Description,475,485,710,21*TextScale,Court::Ink);Button(TEXT("inspect"),TEXT("INSPECT"),475,600,210);Button(TEXT("present"),TEXT("PRESENT / OBJECT"),700,600,255,Stage()!=nullptr);Button(TEXT("back"),TEXT("BACK"),972,600,225);
}
void AChaosHUD::DrawInspection(){
 const auto& E=Case->Evidence[Selected];if(!E.Exhibit){Sprite(TEXT("EvidencePanel"),35,140,735,490);Texture(E.Illustration,65,170,675,435);}else{Sprite(TEXT("InkButton"),55,130,660,60);Label(TEXT("DRAG TO ROTATE  /  MOUSE WHEEL TO ZOOM"),80,150,17,Court::Cream);Button(TEXT("rotate_l"),TEXT("<  A"),65,615,110);Button(TEXT("rotate_r"),TEXT("D  >"),187,615,110);Button(TEXT("zoom_out"),TEXT("ZOOM -"),310,615,160);Button(TEXT("zoom_in"),TEXT("ZOOM +"),485,615,170);}
 Sprite(TEXT("EvidencePanel"),790,142,455,535);Wrapped(E.Title,820,180,385,29,Court::Ink);Label(E.Category.ToUpper(),820,260,15,Court::Red);const FString Details=InspectionRead?E.Inspection:E.Description;float DetailSize=22*TextScale;for(;DetailSize>16;DetailSize-=1){TArray<FString> Rows;Wrap(Details,375,DetailSize).ParseIntoArrayLines(Rows);if(Rows.Num()*DetailSize*1.2f<210)break;}Wrapped(Details,820,305,375,DetailSize,Court::Ink);Button(TEXT("detail"),InspectionRead?TEXT("NOTES RECORDED"):TEXT("EXAMINE DETAILS"),820,535,380);Button(TEXT("back"),TEXT("BACK TO RECORD"),820,600,380);
}
void AChaosHUD::DrawSettings(){
 Sprite(TEXT("EvidencePanel"),55,135,1170,550);Label(TEXT("MAKE YOURSELF AT HOME, COUNSEL"),85,165,29,Court::Ink);
 const TArray<FString> AudioNames={TEXT("MASTER"),TEXT("MUSIC"),TEXT("EFFECTS"),TEXT("VOICES")};const TArray<FString> Keys={TEXT("master"),TEXT("music"),TEXT("effects"),TEXT("voice")};const TArray<float> Values={MasterVolume,MusicVolume,EffectsVolume,VoiceVolume};
 for(int I=0;I<4;++I){float Y=230+I*58;Label(AudioNames[I],85,Y+14,21,Court::Ink);Label(FString::Printf(TEXT("%d%%"),FMath::RoundToInt(Values[I]*100)),310,Y+14,21,Court::Teal);Button(Keys[I]+TEXT("_less"),TEXT("-"),405,Y,60);Button(Keys[I]+TEXT("_more"),TEXT("+"),480,Y,60);}
 const TCHAR* QualityNames[]={TEXT("LOW"),TEXT("MEDIUM"),TEXT("HIGH"),TEXT("EPIC")};Button(TEXT("quality"),FString(TEXT("QUALITY: "))+QualityNames[Quality],85,470,455);Button(TEXT("window"),TEXT("WINDOWED / BORDERLESS"),85,535,455);
 Label(FString::Printf(TEXT("TEXT SIZE: %d%%"),FMath::RoundToInt(TextScale*100)),660,254,21,Court::Ink);Button(TEXT("text_less"),TEXT("-"),1040,240,60);Button(TEXT("text_more"),TEXT("+"),1115,240,60);
 Button(TEXT("speed"),FString::Printf(TEXT("TEXT SPEED: %s"),RevealSpeed<40?TEXT("RELAXED"):RevealSpeed<60?TEXT("NORMAL"):TEXT("QUICK")),660,310,515);
 Button(TEXT("instant"),InstantText?TEXT("INSTANT TEXT: ON"):TEXT("INSTANT TEXT: OFF"),660,380,515);Button(TEXT("motion"),ReducedMotion?TEXT("REDUCED MOTION: ON"):TEXT("REDUCED MOTION: OFF"),660,450,515);Button(TEXT("contrast"),HighContrast?TEXT("HIGH CONTRAST: ON"):TEXT("HIGH CONTRAST: OFF"),660,520,515);Button(TEXT("back"),TEXT("SAVE SETTINGS + BACK"),660,600,515);Label(TEXT("Preferences are saved automatically."),85,620,18,Court::Teal);
}
void AChaosHUD::DrawHistory(){
 Sprite(TEXT("EvidencePanel"),55,140,1170,545);Label(TEXT("THE TRIAL TRANSCRIPT"),85,170,31,Court::Ink);Label(TEXT("LATEST ENTRIES FIRST"),85,215,14,Court::Red);
 if(History.IsEmpty())Label(TEXT("Your transcript begins when the case starts."),85,285,23,Court::Ink);
 for(int I=0;I<4;++I){int N=History.Num()-1-HistoryPage*4-I;if(History.IsValidIndex(N)){Panel(85,255+I*82,4,57,Court::Gold);Wrapped(History[N],105,255+I*82,1070,21*TextScale,Court::Ink);}}
 Button(TEXT("history_prev"),TEXT("< NEWER"),85,610,230,HistoryPage>0);Button(TEXT("history_next"),TEXT("OLDER >"),335,610,230,(HistoryPage+1)*4<History.Num());Button(TEXT("back"),TEXT("BACK TO TRIAL"),855,610,330);
}
void AChaosHUD::DrawResults(){
 Sprite(TEXT("EvidencePanel"),55,145,1170,540);Sprite(TEXT("Verdict"),360,155,560,145);Label(Wrong==0?TEXT("FLAWLESS DEFENSE"):Wrong<3?TEXT("CERTIFIED OBJECTOR"):TEXT("JUSTICE SERVED. EVENTUALLY."),320,315,32,Court::Ink);
 const FString Summary=ActiveCase==0?TEXT("Benny carried mustard. Maintenance moved the gavel into storage before he arrived."):ActiveCase==1?TEXT("The urn and fog machine overloaded a shared circuit. Benny's battery equipment was isolated."):TEXT("Brick collected sealed C17 under policy. The deposit receipt and bank count account for all 480 pounds.");Wrapped(Summary,180,365,950,23,Court::Ink);
 Label(FString::Printf(TEXT("%d DEDUCTIONS     %d MISTAKES     %d PRESSES     %d CLUES INSPECTED"),Correct,Wrong,Presses,Inspections),180,437,19,Court::Teal);
 const TArray<bool> Earned={Correct>0,Inspections>0,Wrong==0,Presses>=3};const TArray<FString> Badges={TEXT("FIRST OBJECTION"),TEXT("SHARP EYE"),TEXT("STEADY NERVES"),TEXT("COURTROOM MENACE")};for(int I=0;I<4;++I){Sprite(TEXT("Badge")+FString::FromInt(I),180+I*250,478,48,48,Earned[I]?1:.25f);Label(Badges[I],235+I*250,492,14,Earned[I]?Court::Ink:FLinearColor(.4f,.4f,.4f));}
 Button(TEXT("start"),TEXT("PLAY AGAIN"),180,590,290);Button(TEXT("cases"),TEXT("CASE FILES"),490,590,290);Button(TEXT("menu"),TEXT("MAIN MENU"),800,590,290);
}
void AChaosHUD::RunTests(){
 bool OK=CaseLibrary.Num()==3;const bool OldInstant=InstantText;InstantText=true;
 for(int32 C=0;C<CaseLibrary.Num();++C){
  OK&=SelectCase(C)&&ValidateAudio();BeginCase();int Guard=0;while(Phase<2&&++Guard<30)Next();OK&=Phase==2&&!Unlocked(Case->Evidence.Num()-1);
  Action(TEXT("press"));OK&=Presses==1&&!Feedback.IsEmpty()&&Credibility==3;Selected=0;Statement=Stage()->Contradiction;while(Case->Evidence[Selected].Id==Stage()->Evidence)++Selected;Action(TEXT("present"));OK&=Wrong==1&&Credibility==2&&Phase==2;
  for(int I=0;I<Case->Stages.Num();++I){const auto S=Stage();if(!S){OK=false;break;}Statement=S->Contradiction;for(int E=0;E<Case->Evidence.Num();++E)if(Case->Evidence[E].Id==S->Evidence)Selected=E;Action(TEXT("present"));OK&=Correct==I+1;Action(TEXT("skip"));Guard=0;while(Resolution&&++Guard<20)Next();}
  Action(TEXT("conclusion_")+FString::FromInt(Case->CorrectConclusion));OK&=ClosingSolved&&Phase==FinalPhase();GavelTime=0;Guard=0;while(Screen!=EChaosScreen::Results&&++Guard<20)Next();OK&=Completed&&Screen==EChaosScreen::Results;Save();Phase=0;OK&=Load()&&Phase==FinalPhase()&&ActiveCase==C;
  Action(TEXT("cases"));Action(TEXT("settings"));Action(TEXT("back"));OK&=Screen==EChaosScreen::Cases;Action(TEXT("back"));OK&=Screen==EChaosScreen::Results;
  FString CompletedSave;FFileHelper::LoadFileToString(CompletedSave,*Court::File(TEXT("Trial.json")));
  FFileHelper::SaveStringToFile(TEXT("invalid"),*Court::File(TEXT("Trial.json")));OK&=!Load();FFileHelper::SaveStringToFile(CompletedSave,*Court::File(TEXT("Trial.json")));Load();
  TSharedPtr<FJsonObject> Legacy;if(Court::Read(Court::File(TEXT("Trial.json")),Legacy)){Legacy->SetNumberField(TEXT("version"),2);Legacy->SetNumberField(TEXT("credibility"),5);Court::Write(Court::File(TEXT("Trial.json")),Legacy.ToSharedRef());OK&=Load()&&Credibility==3&&Completed;}
  if(C==0&&Court::Testing()){
   const FString OldSlot=Court::File(TEXT("Trial_")+Case->CaseId.ToString()+TEXT(".json"));IFileManager::Get().Delete(*OldSlot);
   SelectCase(1);BeginCase();OK&=ReadTrial(OldSlot)&&ActiveCase==0&&Completed&&Credibility==3;
  }
  // Both evidence and closing mistakes draw from the same finite three-life budget.
  BeginCase();Phase=2;Statement=Stage()->Contradiction;Selected=0;while(Case->Evidence[Selected].Id==Stage()->Evidence)++Selected;
  Action(TEXT("present"));Action(TEXT("present"));OK&=Credibility==1&&!CaseFailed;
  Phase=FinalPhase();SetScreen(EChaosScreen::Closing);Action(TEXT("conclusion_")+FString::FromInt((Case->CorrectConclusion+1)%Case->Conclusions.Num()));OK&=Credibility==0&&CaseFailed&&Screen==EChaosScreen::Failed;
  Save();OK&=Load()&&CaseFailed&&Screen==EChaosScreen::Failed;int OldPhase=Phase;Action(TEXT("next"));Action(TEXT("press"));OK&=Phase==OldPhase&&Credibility==0;
  Action(TEXT("menu"));OK&=!CaseFailed&&Phase==-1;Action(TEXT("load"));OK&=CaseFailed&&Credibility==0;
  Action(TEXT("restart"));OK&=Phase==0&&Credibility==3&&!CaseFailed&&Correct==0&&Wrong==0&&Inspected.IsEmpty()&&!Unlocked(Case->Evidence.Num()-1);
  Phase=2;Statement=Stage()->Contradiction;Selected=0;while(Case->Evidence[Selected].Id==Stage()->Evidence)++Selected;for(int32 Miss=0;Miss<3;++Miss)Action(TEXT("present"));OK&=CaseFailed&&Credibility==0&&Screen==EChaosScreen::Failed;Action(TEXT("restart"));
  FFileHelper::SaveStringToFile(CompletedSave,*Court::File(TEXT("Trial_")+Case->CaseId.ToString()+TEXT(".json")));
  UE_LOG(LogTemp,Display,TEXT("CASE_TEST %s cumulative=%d"),*Case->CaseId.ToString(),OK);
 }
 for(int32 C=0;C<CaseLibrary.Num();++C){const FString Slot=Court::File(TEXT("Trial_")+CaseLibrary[C]->CaseId.ToString()+TEXT(".json"));OK&=ReadTrial(Slot)&&ActiveCase==C&&Completed;}
 SelectCase(0);
 FFileHelper::SaveStringToFile(OK?TEXT("PASS: three complete authored cases, evidence locks, deductions, closing/verdict, independent saves, corrupt-save recovery, three-life failure, reload protection and full restart"):TEXT("FAIL: case library or three-life progression"),*(FPaths::ProjectSavedDir()/TEXT("TrialTest.txt")));UE_LOG(LogTemp,Display,TEXT("COURT_SELF_TEST: %s"),OK?TEXT("PASS"):TEXT("FAIL"));
 BeginCase();InstantText=OldInstant;Phase=2;Statement=0;Dialogue=0;Resolution=false;Feedback.Empty();LastText.Empty();Screen=EChaosScreen::Play;ReducedMotion=false;StartObjection();StartGavel();
 FTimerHandle First,Second,Contact;
 GetWorld()->GetTimerManager().SetTimer(First,[this](){if(auto A=Cast.FindRef(TEXT("Milo")).Get())if(auto C=A->FindComponentByClass<USkeletalMeshComponent>())TestHead=C->GetSocketQuaternion(TEXT("Head"));},.3f,false);
 GetWorld()->GetTimerManager().SetTimer(Second,[this](){bool Moving=false;if(auto A=Cast.FindRef(TEXT("Milo")).Get())if(auto C=A->FindComponentByClass<USkeletalMeshComponent>())Moving=C->GetNumBones()>=17&&TestHead.AngularDistance(C->GetSocketQuaternion(TEXT("Head")))>.001f;FFileHelper::SaveStringToFile(Moving?TEXT("PASS: skeletal head pose changes during runtime playback"):TEXT("FAIL: no skeletal motion"),*(FPaths::ProjectSavedDir()/TEXT("AnimationTest.txt")));UE_LOG(LogTemp,Display,TEXT("COURT_ANIMATION_TEST: %s"),Moving?TEXT("PASS"):TEXT("FAIL"));},1.1f,false);
 GetWorld()->GetTimerManager().SetTimer(Contact,[this](){bool Hands=false,Gavel=false;FVector H=FVector::ZeroVector;if(auto A=Cast.FindRef(TEXT("Oliver")).Get())if(auto C=A->FindComponentByClass<USkeletalMeshComponent>()){H=C->GetSocketLocation(TEXT("Hand_R"));Hands=H.Z>123&&H.Z<140&&H.X>-400&&H.X<-200&&H.Y>-50&&H.Y<30;}FVector O=FVector::ZeroVector,E=FVector::ZeroVector;if(GavelActor){GavelActor->GetActorBounds(false,O,E);Gavel=O.Z-E.Z>192&&O.Z-E.Z<201;}FString R=FString::Printf(TEXT("%s: desk hand=(%.1f,%.1f,%.1f); gavel bottom=%.1f; block top=195.5"),Hands&&Gavel?TEXT("PASS"):TEXT("FAIL"),H.X,H.Y,H.Z,O.Z-E.Z);FFileHelper::SaveStringToFile(R,*(FPaths::ProjectSavedDir()/TEXT("ChoreographyTest.txt")));UE_LOG(LogTemp,Display,TEXT("COURT_CHOREOGRAPHY_TEST: %s"),*R);},1.05f,false);
 RunAudioTests();
}

// Deterministic rendering review. Separate test saves; never runs during ordinary play.
void AChaosHUD::RunVisualTests(){
 InstantText=true;TextScale=1.3f;ReducedMotion=false;
 IFileManager::Get().MakeDirectory(*(FPaths::ProjectSavedDir()/TEXT("VisualQA")),true);
 auto Step=MakeShared<int32>(0);auto Timer=MakeShared<FTimerHandle>();
 GetWorld()->GetTimerManager().SetTimer(*Timer,[this,Step,Timer](){
  const int32 View=(*Step)/2;
  const TArray<FString> Names={TEXT("Settings"),TEXT("Witness"),TEXT("Record"),TEXT("Mustard3D"),TEXT("Document"),TEXT("Transcript"),TEXT("Closing"),TEXT("Gavel"),TEXT("Results"),TEXT("DeskSlam"),TEXT("GoldenGavel3D"),TEXT("Credits"),TEXT("Cases"),TEXT("Menu"),TEXT("BennyApron"),TEXT("BlackoutStart"),TEXT("BlackoutRecord"),TEXT("Battery3D"),TEXT("BlackoutClosing"),TEXT("BlackoutResults"),TEXT("CharityStart"),TEXT("CharityRecord"),TEXT("Envelope3D"),TEXT("CharityClosing"),TEXT("CharityResults"),TEXT("ThreeLifeFailure"),TEXT("OliverCloseup"),TEXT("VictorCloseup"),TEXT("BumbleCloseup"),TEXT("BrickCloseup")};
  if(View>=Names.Num()){FPlatformMisc::RequestExit(false);return;}
  if((*Step)%2){FScreenshotRequest::RequestScreenshot(FPaths::ProjectSavedDir()/TEXT("VisualQA")/(Names[View]+TEXT(".png")),false,false);}
  else{
   Impact=GavelTime=0;Resolution=false;Feedback.Empty();
   switch(View){
    case 0:Phase=-1;SetScreen(EChaosScreen::Settings);break;
    case 1:BeginCase();Phase=2;SetScreen(EChaosScreen::Play);break;
    case 2:Selected=1;SetScreen(EChaosScreen::Record);break;
    case 3:Selected=1;InspectionRead=true;ExhibitZoom=1;SetScreen(EChaosScreen::Inspect);break;
    case 4:Selected=2;InspectionRead=true;SetScreen(EChaosScreen::Inspect);break;
    case 5:Record(TEXT("INSPECTION: The nozzle and red M match the security photograph."));Record(TEXT("PRESS: Milo did not check the bench at 19:10. The inventory lists the check times."));SetScreen(EChaosScreen::History);break;
    case 6:Phase=FinalPhase();ClosingSolved=false;Correct=3;SetScreen(EChaosScreen::Closing);break;
    case 7:ClosingSolved=true;Dialogue=1;SetScreen(EChaosScreen::Play);StartGavel();break;
    case 8:Completed=true;Correct=3;Presses=3;Inspections=2;SetScreen(EChaosScreen::Results);break;
    case 9:Phase=3;Resolution=true;ResolutionStage=0;Dialogue=0;SetScreen(EChaosScreen::Play);StartObjection();break;
    case 10:Phase=4;Resolution=false;Selected=5;InspectionRead=true;ExhibitZoom=1;SetScreen(EChaosScreen::Inspect);break;
    case 11:Phase=-1;SetScreen(EChaosScreen::Credits);break;
    case 12:SetScreen(EChaosScreen::Cases);break;
    case 13:Phase=-1;SetScreen(EChaosScreen::Play);break;
    case 14:BeginCase();SetScreen(EChaosScreen::Play);break;
    case 15:SelectCase(1);BeginCase();break;
    case 16:Phase=2;Selected=0;SetScreen(EChaosScreen::Record);break;
    case 17:InspectionRead=true;SetScreen(EChaosScreen::Inspect);break;
    case 18:Phase=FinalPhase();ClosingSolved=false;SetScreen(EChaosScreen::Closing);break;
    case 19:Completed=true;Correct=3;SetScreen(EChaosScreen::Results);break;
    case 20:SelectCase(2);BeginCase();break;
    case 21:Phase=4;Selected=4;SetScreen(EChaosScreen::Record);break;
    case 22:Selected=5;InspectionRead=true;SetScreen(EChaosScreen::Inspect);break;
    case 23:Phase=FinalPhase();ClosingSolved=false;SetScreen(EChaosScreen::Closing);break;
    case 24:Completed=true;Correct=3;SetScreen(EChaosScreen::Results);break;
    case 25:BeginCase();Phase=2;LoseLife(TEXT("Test mistake"));LoseLife(TEXT("Test mistake"));LoseLife(TEXT("Test mistake"));break;
    case 26:SelectCase(1);BeginCase();Phase=1;Dialogue=2;break;
    case 27:Dialogue=1;break;
    case 28:Dialogue=0;break;
    case 29:Phase=3;Resolution=true;ResolutionStage=0;Dialogue=2;break;
   }
  }
  ++(*Step);
 },.8f,true);
}


void AChaosHUD::StopSpeech(){
 if(IsValid(SpeechAudio)){SpeechAudio->Stop();SpeechAudio->DestroyComponent();}SpeechAudio=nullptr;SpeechSequence=nullptr;SpeechTake=0;SpeechClock=0;SpeechKey.Empty();SpeechSpeaker.Empty();SpeechPaused=false;SpeechTakeStarted=false;MouthAmount=0;
}
void AChaosHUD::StartSpeechTake(){
 if(IsValid(SpeechAudio)){SpeechAudio->Stop();SpeechAudio->DestroyComponent();}SpeechAudio=nullptr;
 if(!SpeechSequence||!SpeechSequence->Takes.IsValidIndex(SpeechTake)){SpeechSpeaker.Empty();return;}
 const auto& Take=SpeechSequence->Takes[SpeechTake];SpeechSpeaker=Take.Speaker;SpeechClock=0;SpeechTakeStarted=true;
 SpeechAudio=UGameplayStatics::SpawnSound2D(this,Take.Sound,MasterVolume*VoiceVolume,1,0,nullptr,false,false);
}
void AChaosHUD::UpdateSpeech(float D){
 if(Phase<0||Screen==EChaosScreen::Results||CaseFailed){if(!SpeechKey.IsEmpty())StopSpeech();return;}
 const auto L=CurrentLine();const FString Desired=Feedback.IsEmpty()?L.Speaker+TEXT("|")+L.Text:TEXT("Feedback|")+Feedback;
 if(Desired!=SpeechKey){StopSpeech();SpeechKey=Desired;if(CourtAudio)SpeechSequence=CourtAudio->Speech.Find(Desired);}
 const bool Allowed=(Screen==EChaosScreen::Play||Screen==EChaosScreen::Closing)&&Impact<=0&&GavelTime<=0;
 if(!Allowed){if(IsValid(SpeechAudio)&&!SpeechPaused)SpeechAudio->SetPaused(true);SpeechPaused=true;MouthAmount=FMath::FInterpTo(MouthAmount,0.f,D,24);return;}
 if(SpeechPaused){if(IsValid(SpeechAudio))SpeechAudio->SetPaused(false);SpeechPaused=false;}
 if(!SpeechSequence||!SpeechSequence->Takes.IsValidIndex(SpeechTake)){MouthAmount=FMath::FInterpTo(MouthAmount,0.f,D,24);return;}
 if(!SpeechTakeStarted)StartSpeechTake();
 const auto& Take=SpeechSequence->Takes[SpeechTake];
 if(IsValid(SpeechAudio))SpeechAudio->SetVolumeMultiplier(MasterVolume*VoiceVolume);
 const float Frame=SpeechClock*Take.EnvelopeHz;int32 I=FMath::FloorToInt(Frame);float Open=0;
 if(Take.Envelope.IsValidIndex(I))Open=FMath::Lerp(Take.Envelope[I],Take.Envelope[FMath::Min(I+1,Take.Envelope.Num()-1)],Frame-I);
 MouthAmount=FMath::FInterpTo(MouthAmount,Open,D,24);
 if(Court::Testing()&&SpeechSpeaker==TEXT("Benny")){TestMouthMin=FMath::Min(TestMouthMin,MouthAmount);TestMouthMax=FMath::Max(TestMouthMax,MouthAmount);}
 SpeechClock+=D;if(SpeechClock>=Take.Duration){++SpeechTake;StartSpeechTake();}
}
void AChaosHUD::UpdateMusic(float D){
 ChaosPulse=FMath::Max(0.f,ChaosPulse-D*.045f);
 float Baseline=0;if(Phase>=2&&Phase<FinalPhase())Baseline=.08f+.10f*(Phase-2)+.035f*FMath::Min(Presses,4)+.045f*FMath::Min(Wrong,4)+.035f*(3-Credibility);
 float Target=FMath::Clamp(Baseline+ChaosPulse,0.f,1.f);if(Screen==EChaosScreen::Results||Phase<0)Target=0;if(Screen==EChaosScreen::Record||Screen==EChaosScreen::Inspect||Screen==EChaosScreen::History||Screen==EChaosScreen::Settings)Target*=.5f;
 CourtHeat=FMath::FInterpTo(CourtHeat,Target,D,Target>CourtHeat?2.8f:.7f);
 const bool Voicing=!SpeechPaused&&!SpeechSpeaker.IsEmpty();float Duck=Impact>0?.13f:Voicing?.27f:1.f;MusicDuck=FMath::FInterpTo(MusicDuck,Duck,D,Duck<MusicDuck?9.f:2.f);
 const float Volumes[]={.42f,.24f*FMath::SmoothStep(.10f,.45f,CourtHeat),.22f*FMath::SmoothStep(.35f,.72f,CourtHeat),.20f*FMath::SmoothStep(.65f,.98f,CourtHeat)};
 for(int I=0;I<MusicStems.Num()&&I<4;++I)if(IsValid(MusicStems[I]))MusicStems[I]->SetVolumeMultiplier(MasterVolume*MusicVolume*MusicDuck*Volumes[I]);
}


bool AChaosHUD::ValidateAudio() const {
 if(Cast.Num()!=6||Animations.Num()!=120)return false;for(const auto& A:Animations)if(!A.Value)return false;
 if(!CourtAudio||CourtAudio->MusicLayers.Num()!=4||CourtAudio->VoicePresets.Num()!=6)return false;
 TSet<FString> Voices;for(const auto& Pair:CourtAudio->VoicePresets)Voices.Add(Pair.Value);if(Voices.Num()!=6)return false;
 for(auto W:CourtAudio->MusicLayers)if(!W||FMath::Abs(W->Duration-15.36f)>.03f){UE_LOG(LogTemp,Error,TEXT("AUDIO_DURATION %s %.3f"),*GetNameSafe(W),W?W->Duration:0);return false;}
 auto Has=[this](const FString& Key){const auto S=CourtAudio->Speech.Find(Key);if(!S||S->Takes.IsEmpty()){UE_LOG(LogTemp,Error,TEXT("MISSING_SPEECH %s"),*Key);return false;}for(const auto& T:S->Takes)if(!T.Sound||T.Duration<=0||T.Envelope.IsEmpty())return false;return true;};
 for(const auto& L:Case->Consultation)if(!Has(L.Speaker+TEXT("|")+L.Text))return false;
 for(const auto& L:Case->Opening)if(!Has(L.Speaker+TEXT("|")+L.Text))return false;
 for(const auto& L:Case->Verdict)if(!Has(L.Speaker+TEXT("|")+L.Text))return false;
 for(const auto& S:Case->Stages){for(const auto& L:S.Resolution)if(!Has(L.Speaker+TEXT("|")+L.Text))return false;for(const auto& T:S.Statements)if(!Has(S.Speaker+TEXT("|")+T.Text)||!Has(TEXT("Feedback|")+T.Press))return false;}
 if(!Has(TEXT("Oliver|")+Case->ClosingPrompt))return false;
 for(const auto& P:Cast)if(auto A=P.Value.Get())if(auto C=A->FindComponentByClass<USkeletalMeshComponent>())if(!C->GetSkeletalMeshAsset()->FindMorphTarget(TEXT("TalkOpen"))||!C->GetSkeletalMeshAsset()->FindMorphTarget(TEXT("SmileHide"))){UE_LOG(LogTemp,Error,TEXT("MISSING_MORPHS %s count=%d"),*P.Key.ToString(),C->GetSkeletalMeshAsset()->GetMorphTargets().Num());return false;}
 return true;
}
void AChaosHUD::RunAudioTests(){
 TestAudioOK=ValidateAudio();UE_LOG(LogTemp,Display,TEXT("AUDIO_CHECK coverage=%d"),TestAudioOK);
 FTimerHandle A,B,C,D,E;
 GetWorld()->GetTimerManager().SetTimer(A,[this](){StopSpeech();Phase=0;Dialogue=0;Resolution=false;Feedback.Empty();Impact=GavelTime=0;Screen=EChaosScreen::Play;CourtHeat=ChaosPulse=0;MasterVolume=.8f;VoiceVolume=.9f;MusicVolume=.4f;TestMouthMin=1;TestMouthMax=0;},3.3f,false);
 GetWorld()->GetTimerManager().SetTimer(B,[this](){TestAudioOK&=SpeechAudio&&SpeechAudio->IsPlaying()&&SpeechSpeaker==TEXT("Benny")&&MusicStems.Num()==4;for(auto Stem:MusicStems)TestAudioOK&=Stem&&Stem->IsPlaying();TestQuietLayer=MusicStems.Num()>2?MusicStems[2]->VolumeMultiplier:1;TestPausedClock=SpeechClock;UE_LOG(LogTemp,Display,TEXT("AUDIO_CHECK playback=%d speaker=%s stems=%d"),TestAudioOK,*SpeechSpeaker,MusicStems.Num());SetScreen(EChaosScreen::Settings);},4.2f,false);
 GetWorld()->GetTimerManager().SetTimer(C,[this](){TestAudioOK&=SpeechAudio&&SpeechAudio->GetPlayState()==EAudioComponentPlayState::Paused&&FMath::Abs(SpeechClock-TestPausedClock)<.05f;UE_LOG(LogTemp,Display,TEXT("AUDIO_CHECK pause=%d clock=%.3f expected=%.3f"),TestAudioOK,SpeechClock,TestPausedClock);SetScreen(EChaosScreen::Play);ChaosPulse=1;CourtHeat=.95f;},4.6f,false);
 GetWorld()->GetTimerManager().SetTimer(D,[this](){TestAudioOK&=SpeechAudio&&SpeechAudio->IsPlaying()&&SpeechClock>TestPausedClock&&TestMouthMax-TestMouthMin>.08f;TestAudioOK&=MusicStems.Num()>2&&MusicStems[2]->VolumeMultiplier>TestQuietLayer+.003f;UE_LOG(LogTemp,Display,TEXT("AUDIO_CHECK resume=%d gain=%.4f quiet=%.4f"),TestAudioOK,MusicStems.Num()>2?MusicStems[2]->VolumeMultiplier:0,TestQuietLayer);LineElapsed=10000;Next();},5.5f,false);
 GetWorld()->GetTimerManager().SetTimer(E,[this](){TestAudioOK&=SpeechAudio&&SpeechAudio->IsPlaying()&&SpeechSpeaker==TEXT("Oliver");FString R=FString::Printf(TEXT("%s: dialogue coverage, six voices, mouth morphs, speech playback/pause/resume/replacement, four synchronized music layers and chaos response; mouth range %.2f..%.2f"),TestAudioOK?TEXT("PASS"):TEXT("FAIL"),TestMouthMin,TestMouthMax);FFileHelper::SaveStringToFile(R,*(FPaths::ProjectSavedDir()/TEXT("AudioTest.txt")));UE_LOG(LogTemp,Display,TEXT("COURT_AUDIO_TEST: %s"),*R);},5.9f,false);
}
