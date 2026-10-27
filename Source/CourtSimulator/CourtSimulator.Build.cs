using UnrealBuildTool;
public class CourtSimulator : ModuleRules { public CourtSimulator(ReadOnlyTargetRules Target):base(Target) { PCHUsage=PCHUsageMode.UseExplicitOrSharedPCHs; PublicDependencyModuleNames.AddRange(new string[]{"Core","CoreUObject","Engine","InputCore","Json","JsonUtilities","Slate","SlateCore"}); } }
