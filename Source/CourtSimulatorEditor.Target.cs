using UnrealBuildTool;
public class CourtSimulatorEditorTarget : TargetRules { public CourtSimulatorEditorTarget(TargetInfo Target):base(Target) { Type=TargetType.Editor; DefaultBuildSettings=BuildSettingsVersion.V7; ExtraModuleNames.Add("CourtSimulator"); } }

