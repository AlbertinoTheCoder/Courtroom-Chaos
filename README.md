# Courtroom Chaos

Unreal Engine 5.8.3 project. Run `LaunchGame.bat` to play the packaged Windows build, or open `CourtSimulator.uproject` to edit it. The standalone executable is `Builds/Windows/CourtSimulator.exe`.

Click Start to meet Benny Buns and cross-examine the Golden Gavel accusation. Use the testimony controls, Press, and Court Record. Each contradiction requires the appropriate evidence on the relevant statement. Incorrect evidence costs credibility; a recess restores it so the case cannot become permanently blocked.

Mouse buttons operate the interface. E opens the record, Q presses, arrows browse testimony, Space advances, Escape saves and returns to the menu. Continue resumes the last saved trial.

Rebuild C++ with `Tools/BuildProject.ps1`. Regenerate editable Blender source, seven FBX assets and the Unreal level with `Tools/BuildArt.ps1`. These scripts replace generated project assets; preserve manual changes before regenerating.

Environment source: `Art/Blender/CourtroomChaos.blend`; export-corrected lettering source: `CourtroomLettering.blend`. The refined character source is `Art/Blender/Cast.blend`, with articulated rigs and performance clips in `Art/Blender/CastRigged.blend`. Six characters each have seven authored clips: idle, speaking, pointing, angry, nervous, celebration and shock. Music, interface ticks and the objection sound are original local procedural assets. The prosecutor uses authored deterministic arguments and structured choices, with no external language model dependency.

Validation: editor and standalone builds pass; the packaged game passes case progression, incorrect evidence, three deductions, verdict, save/load and a runtime skeletal-motion test. Mouse-driven menu, dialogue and evidence presentation were also exercised. Run `Tests/RunTrialTest.ps1` for the repeatable offscreen case and animation checks. Test saves use a separate file from normal play.

This remains an early playable slice. Animation uses rigid cartoon segments with head, limb, eye, brow and mouth articulation. Detailed hand gestures, desk-slam/gavel choreography, richer evidence artwork and 3D inspection, voice acting, dialogue history, accessibility/settings menus and further visual polish remain unfinished. See the development log for actual verification results. Repackage source changes with `Tools/PackageGame.ps1`; the launcher prefers the existing packaged build.
