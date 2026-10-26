#include "ChaosGame.h"
#include "Engine/Canvas.h"
#include "Engine/Engine.h"
#include "GameFramework/PlayerController.h"
#include "Camera/CameraActor.h"
#include "Kismet/GameplayStatics.h"
#include "EngineUtils.h"
#include "Misc/FileHelper.h"
#include "Misc/Paths.h"
#include "Misc/CommandLine.h"
#include "Sound/SoundBase.h"
#include "Engine/Texture2D.h"
#include "Components/SkeletalMeshComponent.h"
#include "Animation/AnimationAsset.h"
#include "Animation/AnimSingleNodeInstance.h"
#include "TimerManager.h"
#include "Components/AudioComponent.h"

namespace Court {
 const FLinearColor Ink(.025f,.035f,.065f), Cream(.96f,.88f,.72f), Gold(.91f,.64f,.22f), Teal(.2f,.64f,.59f), Red(.72f,.12f,.23f);
 const TCHAR* Names[]={TEXT("Security photograph"),TEXT("Mustard dispenser"),TEXT("Maintenance report"),TEXT("Inventory sheet"),TEXT("Cart transfer record"),TEXT("Storage photograph")};
 const TCHAR* Details[]={TEXT("19:10 | Benny leaves carrying a yellow object.\nINSPECT: a pointed nozzle and a red label.\nThe ceremonial gavel has neither."),TEXT("Benny's extra-large mustard dispenser.\nIts nozzle and red label match the security image.\nBenny: 'It's artisanal. The bottle is the chef.'"),TEXT("18:00 | Cleaning of the ceremonial bench.\nAll display objects must be relocated before work.\nSigned: Milo Mopps, maintenance."),TEXT("17:45 | Golden Gavel checked on ceremonial bench.\nNext check: 20:00. Marked MISSING.\nNo check was performed at 19:10."),TEXT("18:05 | Officer Brick moved ceremonial objects.\nDestination: storage B. Cart number 04.\nContents include one velvet-lined gavel case."),TEXT("20:15 | Storage B, cart 04.\nINSPECT: behind the bucket is a golden gavel\ninside an open velvet-lined case. No theft occurred.")};
 const TCHAR* Testimony[3][3]={
  {TEXT("I saw Benny leave at 19:10 carrying the Golden Gavel."),TEXT("The security photograph proves it was a gavel."),TEXT("I remember everything. Except small details. And Tuesdays.")},
  {TEXT("The gavel was on the bench until Benny arrived at 19:10."),TEXT("Nobody moved any ceremonial objects that evening."),TEXT("The room was being cleaned. That is entirely unrelated.")},
  {TEXT("Even if it was moved, the gavel never reached storage."),TEXT("Cart 04 carried nothing except cleaning supplies."),TEXT("The defendant must have stolen it. My hair says so.")}};
 const TCHAR* Press[3][3]={
  {TEXT("MILO: I saw yellow. I inferred justice. The nozzle? Decorative?") ,TEXT("VICTOR: A photograph cannot lie. OLIVER: It can be blurry."),TEXT("MILO: Please don't ask me what day it is.")},
  {TEXT("MILO: I didn't check at 19:10. The inventory has the actual times."),TEXT("MILO: Brick handled a cart before dinner. There might be a record."),TEXT("MILO: Cleaning started at 18:00. We cleared the entire bench.")},
  {TEXT("BRICK: I deliver objects. I do not question their ambitions."),TEXT("BRICK: Cart 04. Storage B. I wrote it down. With a pen."),TEXT("JUDGE: The court requests evidence with less hair product.")}};
 const int CorrectEvidence[]={1,2,5}; const int CorrectStatement[]={0,1,0};
 FString SaveFile(){return FPaths::ProjectSavedDir()/(FParse::Param(FCommandLine::Get(),TEXT("CourtSelfTest"))?TEXT("TrialTestSave.sav"):TEXT("Trial.sav"));}
}
AChaosGameMode::AChaosGameMode(){HUDClass=AChaosHUD::StaticClass();DefaultPawnClass=nullptr;}
void AChaosHUD::BeginPlay(){Super::BeginPlay();auto P=GetOwningPlayerController();P->bShowMouseCursor=true;P->bEnableClickEvents=true;P->bEnableMouseOverEvents=true;P->SetInputMode(FInputModeGameAndUI());CourtMusicAudio=UGameplayStatics::SpawnSound2D(this,LoadObject<USoundBase>(nullptr,TEXT("/Game/Audio/CourtroomShuffle.CourtroomShuffle")),.15f);
if(FParse::Param(FCommandLine::Get(),TEXT("CourtSelfTest"))){
 bool OK=true; Action(TEXT("start")); OK &= Phase==0; Action(TEXT("next")); Action(TEXT("next")); OK &= Phase==2;
 Action(TEXT("press")); OK &= !Feedback.IsEmpty(); Selected=0; Action(TEXT("present")); OK &= Credibility==4 && Phase==2;
 Selected=1; Action(TEXT("present")); OK &= Phase==3; Statement=1; Selected=2; Action(TEXT("present")); OK &= Phase==4;
 Selected=5; Action(TEXT("present")); OK &= Phase==5; Save(); Phase=0; Load(); OK &= Phase==5;
 FFileHelper::SaveStringToFile(OK?TEXT("PASS: start, opening, press, incorrect evidence, three deductions, verdict, save/load"):TEXT("FAIL"),*(FPaths::ProjectSavedDir()/TEXT("TrialTest.txt")));
 UE_LOG(LogTemp,Display,TEXT("COURT_SELF_TEST: %s"),OK?TEXT("PASS"):TEXT("FAIL"));
 Phase=2; Statement=0; Credibility=5;Feedback.Empty();
 FTimerHandle FirstSample,SecondSample;
 GetWorld()->GetTimerManager().SetTimer(FirstSample,[this](){for(TActorIterator<AActor> It(GetWorld());It;++It)if(It->ActorHasTag(TEXT("Milo")))if(auto C=It->FindComponentByClass<USkeletalMeshComponent>())AnimationTestFirstPose=C->GetSocketQuaternion(TEXT("Head"));},.3f,false);
 GetWorld()->GetTimerManager().SetTimer(SecondSample,[this](){bool Moving=false;for(TActorIterator<AActor> It(GetWorld());It;++It)if(It->ActorHasTag(TEXT("Milo")))if(auto C=It->FindComponentByClass<USkeletalMeshComponent>())Moving=C->GetNumBones()>=16 && AnimationTestFirstPose.AngularDistance(C->GetSocketQuaternion(TEXT("Head")))>.001f;FFileHelper::SaveStringToFile(Moving?TEXT("PASS: skeletal head pose changes during runtime playback"):TEXT("FAIL: no skeletal head motion detected"),*(FPaths::ProjectSavedDir()/TEXT("AnimationTest.txt")));UE_LOG(LogTemp,Display,TEXT("COURT_ANIMATION_TEST: %s"),Moving?TEXT("PASS"):TEXT("FAIL"));},1.1f,false);
}
}
void AChaosHUD::Label(const FString&S,float X,float Y,float Size,FLinearColor C){DrawText(S,C,X*SX,Y*SY,GEngine->GetMediumFont(),Size*FMath::Min(SX,SY)/16,false);}
void AChaosHUD::Panel(float X,float Y,float W,float H,FLinearColor C){DrawRect(C,X*SX,Y*SY,W*SX,H*SY);}
void AChaosHUD::Sprite(const FString& Name,float X,float Y,float W,float H){
 if(!Textures.Contains(Name)) Textures.Add(Name,LoadObject<UTexture2D>(nullptr,*(TEXT("/Game/UI/")+Name+TEXT(".")+Name)));
 if(auto T=Textures[Name]) DrawTexture(T,X*SX,Y*SY,W*SX,H*SY,0,0,1,1,FLinearColor::White,BLEND_Translucent);
}
void AChaosHUD::Button(FString Id,FString Caption,float X,float Y,float W){
 float MX=0,MY=0;GetOwningPlayerController()->GetMousePosition(MX,MY);
 bool Hover=MX>=X*SX&&MX<=(X+W)*SX&&MY>=Y*SY&&MY<=(Y+46)*SY;
 FString Skin=(Id==TEXT("press")||Id==TEXT("present")||Id==TEXT("start"))?TEXT("RedButton"):(Id==TEXT("evidence")?TEXT("TealButton"):TEXT("InkButton"));
 Sprite(Skin,X,Y-(Hover?3:0),W,50); Label(Caption,X+18,Y+13-(Hover?3:0),20,Court::Cream);
 AddHitBox(FVector2D(X*SX,Y*SY),FVector2D(W*SX,46*SY),FName(Id),true);
}
void AChaosHUD::Save(){FFileHelper::SaveStringToFile(FString::Printf(TEXT("%d %d %d"),Phase,Statement,Credibility),*(Court::SaveFile()));}
void AChaosHUD::Load(){FString S;if(FFileHelper::LoadFileToString(S,*(Court::SaveFile()))){TArray<FString>A;S.ParseIntoArrayWS(A);if(A.Num()==3){Phase=FMath::Clamp(FCString::Atoi(*A[0]),0,5);Statement=FMath::Clamp(FCString::Atoi(*A[1]),0,2);Credibility=FMath::Clamp(FCString::Atoi(*A[2]),1,5);}}}
void AChaosHUD::DrawHUD(){
 Super::DrawHUD();SX=Canvas->SizeX/1280.f;SY=Canvas->SizeY/720.f;auto P=GetOwningPlayerController();
 if(P->WasInputKeyJustPressed(EKeys::Escape))Action(TEXT("menu"));
 if(P->WasInputKeyJustPressed(EKeys::E))Action(TEXT("evidence"));
 if(P->WasInputKeyJustPressed(EKeys::SpaceBar))Action(TEXT("next"));
 if(P->WasInputKeyJustPressed(EKeys::Left))Action(TEXT("prev"));
 if(P->WasInputKeyJustPressed(EKeys::Right))Action(TEXT("next"));
 FString Shot=TEXT("Wide");if(Phase==0)Shot=TEXT("Client");if(Phase==1||Phase==4)Shot=TEXT("Prosecutor");if(Phase==2||Phase==3)Shot=TEXT("Witness");if(Evidence)Shot=TEXT("Wide");if(Phase==5)Shot=TEXT("Judge");if(Impact>.8f)Shot=TEXT("Defense");else if(Impact>0)Shot=Phase==4?TEXT("Prosecutor"):TEXT("Witness");
 for(TActorIterator<ACameraActor>It(GetWorld());It;++It)if(It->ActorHasTag(FName(Shot))&&P->GetViewTarget()!=*It)P->SetViewTargetWithBlend(*It,.4f);
 if(CourtMusicAudio)CourtMusicAudio->SetVolumeMultiplier(Impact>0?0.f:.15f);
 AnimateCast();
 Sprite(TEXT("Logo"),25,13,320,82);
 if(Phase==-1){
  Sprite(TEXT("Dialogue"),55,180,570,440);Label(TEXT("CASE 001"),90,215,20,Court::Red);
  Label(TEXT("THE STOLEN\nGOLDEN GAVEL"),90,250,40,Court::Ink);
  Label(TEXT("One missing gavel. One innocent hot dog man."),90,350,20,Court::Ink);
  Button(TEXT("start"),TEXT("TAKE THE CASE   >"),90,405,490);Button(TEXT("load"),TEXT("CONTINUE TRIAL"),90,465,240);
  Button(TEXT("credits"),TEXT("CONTROLS"),345,465,235);Button(TEXT("quit"),TEXT("LEAVE COURT"),90,525,240);
  if(!Feedback.IsEmpty())Label(Feedback,70,640,18,Court::Cream);return;
 }
 Sprite(TEXT("InkButton"),435,26,410,51);Label(TEXT("001   /   THE STOLEN GOLDEN GAVEL"),460,43,18,Court::Cream);
 Sprite(TEXT("InkButton"),900,17,190,73);Label(TEXT("COURT CONFIDENCE"),915,27,14,Court::Cream);
 for(int i=0;i<5;i++){Sprite(i<Credibility?TEXT("RedButton"):TEXT("InkButton"),917+i*24,49,19,22);}
 Button(TEXT("menu"),TEXT("MENU"),1110,26,140);
 if(Evidence){
  Sprite(TEXT("EvidencePanel"),35,125,1210,540);Label(TEXT("THE COURT RECORD"),65,151,32,Court::Ink);Label(TEXT("INSPECT THE FACTS. THEN MAKE YOUR CASE."),65,198,15,Court::Red);
  for(int i=0;i<6;i++){Sprite(TEXT("Evidence")+FString::FromInt(i),65,246+i*61,61,48);Button(FString::FromInt(i),Court::Names[i],140,246+i*61,290);if(Selected==i)Panel(131,253+i*61,4,32,Court::Gold);}
  Sprite(TEXT("Evidence")+FString::FromInt(Selected),770,218,340,250);
  Label(Court::Names[Selected],478,239,27,Court::Ink);
  Label(Court::Details[Selected],478,485,21,Court::Ink);
  Button(TEXT("present"),TEXT("OBJECT WITH THIS!"),478,595,280);Button(TEXT("evidence"),TEXT("BACK TO TESTIMONY"),785,595,365);return;
 }
 if(Phase>=2&&Phase<=4){Sprite(TEXT("NameTab"),462,105,355,45);Label(TEXT("CROSS-EXAMINATION"),495,118,21,Court::Cream);}
 Sprite(TEXT("Dialogue"),35,495,1210,208);Sprite(TEXT("NameTab"),57,468,420,48);
 FString Name=Phase==0?TEXT("BENNY BUNS  /  YOUR CLIENT"):Phase==1?TEXT("VICTOR VAIN  /  PROSECUTOR"):Phase==5?TEXT("THE HONORABLE JUDGE BUMBLE"):Phase==4?TEXT("VICTOR VAIN  /  UNDER PRESSURE"):TEXT("MILO MOPPS  /  MAINTENANCE");
 Label(Name,79,482,20,Court::Cream);
 if(Phase==0){Label(TEXT("I delivered hot dogs. Now I'm accused of stealing the Golden Gavel.\nThe yellow thing? My mustard bottle. Please defend my good taste."),70,537,25,Court::Ink);Button(TEXT("next"),TEXT("ENTER THE COURTROOM   >"),824,637,380);}
 else if(Phase==1){Label(TEXT("A golden object. A fleeing vendor. An extremely handsome prosecutor.\nJUDGE: Only two of those are evidence."),70,537,25,Court::Ink);Button(TEXT("next"),TEXT("CROSS-EXAMINE   >"),884,637,320);}
 else if(Phase>=2&&Phase<=4){
  int R=Phase-2;Label(FString::Printf(TEXT("STATEMENT  %02d / 03"),Statement+1),990,512,15,Court::Ink);
  Label(Court::Testimony[R][Statement],70,536,26,Court::Ink);Label(Feedback,70,588,18,FLinearColor(.015f,.17f,.15f));
  Button(TEXT("prev"),TEXT("<"),66,637,65);Button(TEXT("next"),TEXT(">"),141,637,65);
  Label(TEXT("REVIEW TESTIMONY"),225,653,15,Court::Ink);Button(TEXT("press"),TEXT("PRESS   [Q]"),660,637,220);Button(TEXT("evidence"),TEXT("COURT RECORD   [E]"),900,637,305);
  if(P->WasInputKeyJustPressed(EKeys::Q))Action(TEXT("press"));
 }else{
  Label(TEXT("NOT GUILTY. EXTRA MUSTARD."),70,535,34,Court::Red);
  Label(TEXT("Cart 04. Storage B. The gavel was moved, never stolen. Justice served."),70,587,23,Court::Ink);
  Button(TEXT("start"),TEXT("REPLAY THE CASE"),70,637,280);Button(TEXT("menu"),TEXT("CASE SELECTION"),375,637,280);
 }
 if(Impact>0){Impact-=GetWorld()->GetDeltaSeconds();Sprite(TEXT("Objection"),180,210,920,220);}
}
void AChaosHUD::AnimateCast(){
 const TArray<FString> Roles={TEXT("Oliver"),TEXT("Victor"),TEXT("Bumble"),TEXT("Benny"),TEXT("Milo"),TEXT("Brick")};
 FString Speaker=Phase==0?TEXT("Benny"):(Phase==1||Phase==4)?TEXT("Victor"):Phase==5?TEXT("Bumble"):TEXT("Milo");
 for(TActorIterator<AActor> It(GetWorld());It;++It){
  auto Component=It->FindComponentByClass<USkeletalMeshComponent>();if(!Component||!It->ActorHasTag(TEXT("Performer")))continue;
  FString CharacterName;for(const FString& R:Roles)if(It->ActorHasTag(FName(R))){CharacterName=R;break;}if(CharacterName.IsEmpty())continue;
  FString Mood=(Phase>=0&&CharacterName==Speaker)?TEXT("Speaking"):TEXT("Idle");
  if(Phase>=3&&CharacterName==TEXT("Victor"))Mood=TEXT("Angry");
  if(Phase==5&&(CharacterName==TEXT("Benny")||CharacterName==TEXT("Oliver")))Mood=TEXT("Celebrate");
  if(Phase==5&&CharacterName==TEXT("Victor"))Mood=TEXT("Nervous");
  if(Phase>=2&&Phase<=3&&CharacterName==TEXT("Milo")&&!Feedback.IsEmpty())Mood=TEXT("Nervous");
  if(Impact>0){if(CharacterName==TEXT("Oliver"))Mood=TEXT("Pointing");if(CharacterName==TEXT("Milo"))Mood=TEXT("Shock");if(CharacterName==TEXT("Victor"))Mood=TEXT("Angry");}
  FString Key=TEXT("AN_")+CharacterName+TEXT("_")+Mood;
  if(!Animations.Contains(Key))Animations.Add(Key,LoadObject<UAnimationAsset>(nullptr,*(TEXT("/Game/Characters/Animations/")+Key+TEXT(".")+Key)));
  if(auto Asset=Animations[Key]){auto Instance=Component->GetSingleNodeInstance();if(!Instance||Instance->GetCurrentAsset()!=Asset){Component->PlayAnimation(Asset,true);UE_LOG(LogTemp,Display,TEXT("CAST_PERFORMANCE %s %s"),*CharacterName,*Mood);}}
 }
}
void AChaosHUD::NotifyHitBoxClick(FName N){Action(N.ToString());}
void AChaosHUD::Action(FString Id){UGameplayStatics::PlaySound2D(this,LoadObject<USoundBase>(nullptr,TEXT("/Game/Audio/UITick.UITick")),.25f);if(Id==TEXT("start")){Phase=0;Statement=0;Credibility=5;Evidence=false;Feedback.Empty();}else if(Id==TEXT("load")){Load();}else if(Id==TEXT("menu")){if(Phase>=0)Save();Phase=-1;Evidence=false;}else if(Id==TEXT("quit")){GetOwningPlayerController()->ConsoleCommand(TEXT("quit"));}else if(Id==TEXT("credits")){Feedback=TEXT("Original procedural art + authored case.\nMouse: buttons | E: evidence | Q: press | Arrows: testimony");}else if(Id==TEXT("evidence")&&Phase>=2&&Phase<=4){Evidence=!Evidence;}else if(Id==TEXT("next")){if(Phase<2&&Phase>=0)Phase++;else if(Phase<=4&&Phase>=2)Statement=(Statement+1)%3;Feedback.Empty();}else if(Id==TEXT("prev")&&Phase>=2&&Phase<=4){Statement=(Statement+2)%3;Feedback.Empty();}else if(Id==TEXT("press")&&Phase>=2&&Phase<=4){Feedback=Court::Press[Phase-2][Statement];}else if(Id==TEXT("present")&&Phase>=2&&Phase<=4){int R=Phase-2;if(Selected==Court::CorrectEvidence[R]&&Statement==Court::CorrectStatement[R]){Phase++;Statement=0;Impact=1.5f;UGameplayStatics::PlaySound2D(this,LoadObject<USoundBase>(nullptr,TEXT("/Game/Audio/Objection.Objection")));Feedback=Phase==3?TEXT("The nozzle proves it was mustard. Now establish when the gavel moved."):TEXT("The timeline is broken. Follow the cart to its destination.");}else {Credibility--;Feedback=TEXT("JUDGE: That doesn't contradict this statement. Read it closely, counsel.");if(Credibility<=0){Credibility=5;Feedback=TEXT("JUDGE: A recess, counsel. Review the record. You may try again.");}}Evidence=false;Save();}else if(Id.IsNumeric()){Selected=FMath::Clamp(FCString::Atoi(*Id),0,5);}}
