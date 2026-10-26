using UnrealBuildTool;
public class CourtSimulatorTarget : TargetRules { public CourtSimulatorTarget(TargetInfo Target):base(Target) { Type=TargetType.Game; DefaultBuildSettings=BuildSettingsVersion.V7; ExtraModuleNames.Add("CourtSimulator"); } }

