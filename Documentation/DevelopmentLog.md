# Development log

## Initial build

- Inspected the empty requested directory, Unreal 5.8.3 installation and Blender 5.2.2 LTS. Tested Blender MCP status; no Unreal MCP tools are exposed in this session. Used installed executables for repeatable generation and editor scripting.
- Created the real C++ Unreal project, runtime module, editor/game targets, project configuration and launch/build scripts.
- Executed Blender generation successfully: 525 modeled objects, seven FBX exports and editable `.blend` source. The courtroom has paneled benches, architectural trim, windows, gallery seating, bookcases, microphone and paper props, a seal and readable decorative text. Six original stylized characters use distinct proportions and costumes.
- Compiled the editor module successfully against Unreal 5.8.3 and Visual Studio 2026. Corrected target settings from V6 to the installed engine's V7 requirement. Initial compilation reports float conversion warnings; no build errors remain.
- Implemented one authored trial, six evidence records, testimony browsing, statement-specific pressing, three explicit contradiction relationships, incorrect-evidence penalties, a recoverable recess, verdict/replay, save/continue, mouse/keyboard input, camera selection and a synthesized objection sound.
- Implemented a runtime self-test for case progression and save/load. Execution passed in the running game, including three deductions, the verdict, incorrect-evidence feedback and save/load.

## Visual revision after user review

- Replaced the original flat gray interface with generated cream dialogue cards, burgundy speaker tabs, branded title art, illustrated evidence records and separate action styles.
- Confirmed the trial integration test passes in the running game.
- Rebuilt all six cast members with custom face/torso profiles, integrated eyelids and eyes, continuous smiles, layered tailoring, cuffs, fingers and role-specific details. Editable current cast source is `Art/Blender/Cast.blend`.
- Corrected the Blender/Unreal front-back conversion, explicit light rotation keywords, character-to-desk clearances, witness portrait framing and ambient fill. Rebuilt the Unreal material graph from the intended palette instead of relying on FBX material translation.
- Tested the normal menu, dialogue progression, evidence selection and successful presentation through real mouse input. Fixed missing click-event dispatch discovered by that test.
- Added client and prosecutor camera presets and speaker-dependent camera selection. Visual review remains iterative; these revisions do not establish commercial-quality animation or a finished game.

## Remaining acceptance gaps

The cast now uses rigid-segment skeletal animation, with 17 authored bones per character and seven clips each. Advanced finger animation, synchronized desk slams, animated gavel interactions, Sequencer choreography, richer evidence artwork/3D inspection, voice acting, dialogue history, accessibility/settings menus and further art polish remain unfinished. The current prosecutor uses authored deterministic rules; no external LLM is configured or claimed.

## Animation, audio and standalone verification

- Created and executed `Tools/rig_cast.py`: six articulated characters and 42 clips. Preserved editable `Art/Blender/CastRigged.blend` and the bone/vertex/clip report in `Art/RigValidation.json`.
- Imported the skeletal assets, verified character bounds, enabled skeletal material usage and replaced the static cast in the saved courtroom.
- Runtime selects speaking, nervous, angry, pointing, shock and celebration poses from case state. Objections cut to the defense and then the reaction shot. Eyelid, eyebrow and mouth bones provide limited cartoon expressions.
- Generated an original 15.36-second pizzicato music loop and interface tick. Music ducks during objections. Added explicit cooking rules for dynamically loaded UI, animation and audio assets.
- Editor runtime test: PASS. Offscreen repeatable case and animation tests: PASS. Standalone Windows BuildCookRun: SUCCESS. Packaged executable case test: PASS. Packaged live head-motion test: PASS.
- Manually exercised the three deductions through the actual UI and reached the verdict. Inspected witness, client, prosecutor, objection and verdict shots, including the angry prosecutor expression and corrected lettering.
- Standalone build is in `Builds/Windows`; `LaunchGame.bat` prefers it. First-launch PSO compilation hitches were observed; broad hardware/performance validation remains pending.

The current UI uses Unreal Canvas rather than UMG. Case text and contradiction rules currently live in structured C++ arrays; the JSON timeline is a development reference, not a runtime data asset. Further cases should migrate this content to data assets before expansion.

## Golden Gavel finishing pass â€” 27 October 2026

This section supersedes the earlier acceptance-gap notes. Runtime case strings moved into a validated editable Data Asset. Added consultation/opening/resolution/closing dialogue, closing choices, transcript, typewriter and skip controls, settings/accessibility options, keyboard focus, results/earned badges, atomic versioned saves and invalid-save recovery.

Expanded all six characters to twenty clips each (120 total), including analytical arm poses for synchronized desk slams and gavel strikes. Added separate animated gavel and block, original foley and character vocal bleeps, detailed evidence illustrations, rotatable/zoomable physical exhibits and inspection notes. Runtime uses Canvas and timed C++ choreography, not UMG or Sequencer. No recorded voice acting or external LLM is claimed.

Editor compilation and the expanded integration tests passed before the overnight pause. Contact test measured defense hand (-253,10,130) cm and gavel bottom 195.1 cm against block top 195.5 cm. Regeneration chain now includes finishing props, UI, case Data Asset and final scene import. Final visual and packaged checks are recorded in FinishChecklist.md.


Final verification completed: editor build succeeded; Windows packaging succeeded with 391 cooked packages. The packaged executable passed case/save validation, live skeletal movement and contact checks. Thirteen rendered views were reviewed, including 130% text, 3D inspection, closing and results. Fixed an input regression found in real mouse QA: NoCapture suppresses primary mouse-down events in Unreal's game viewport; CaptureDuringMouseDown delivers the click without permanent cursor capture. Reduced initial exhibit scale after detecting an instruction-bar overlap. Added isolated deterministic visual capture mode and a repeatable packaged integration test. Full art regeneration was not repeated over verified assets; Python/PowerShell syntax checks passed. Final editable sources and generated content are checkpointed in Git.


Cooked-package screenshots matched the editor. Corrected a cleanup lifetime error discovered after the automated screenshot pass: clearing its own executing timer destroyed lambda storage before the next captured access. The isolated capture mode now requests graceful shutdown directly. Standard shadows explicitly match the SM5 renderer, removing the unsupported virtual-shadow-map editor warning.


## UI text sharpness — 27 October 2026

Replaced scaled Engine Medium bitmap glyphs with a transient runtime UFont backed by the engine's TrueType composite font. Each label chooses its font size from the current viewport dimensions and snaps its origin to integer pixels. Text wrapping uses the same font and size as rendering. Menus, dialogue, percentages and buttons now render directly at the target resolution. No player saves or preferences were reset. Verified rendering at 1280x720, including 130% dialogue text; the packaged render pass also exited cleanly at a verified 1920x1080. Captures are saved in Saved/FontQA720 and Saved/FontPackaged1080.


## Visible courtroom notice — 27 October 2026

Replaced the small wall sentence centered behind a pillar with a 2.48m framed enamel notice between the columns. The notice uses raised Georgia Bold and Segoe Semibold mesh lettering, a brass frame, burgundy rule heading and high-contrast cream/gold copy. Enlarged the complete warning, including PLEASE DO NOT. Editable text objects remain in CourtroomFinal.blend; export meshes preserve the existing Unreal front-face conversion. Tools/polish_notice.py is idempotent and is part of full art regeneration; Tools/import_notice.py performs a targeted room-mesh update. Added the main menu as the fourteenth automatic visual-review view so the sign can be checked from the player's camera.


## Speech, adaptive music and clothing - 27 October 2026

Six distinct Kokoro voices, 49 baked clips (230.6 seconds), and amplitude envelopes replace dialogue bleeps. Four synchronized 125 BPM stems respond to court temper and duck for dialogue. Speech pauses in overlays, switches cleanly between speakers, and has an independent volume control. Removed the floating lower-lip strip, added small TalkOpen/SmileHide morphs, and saved MorphTargets material usage for packaging. Benny has a continuous apron with straps and a pocket outside the jacket/tie. Animation preloading removes first-use performance stalls.

Editor and packaged TrialTest, AnimationTest, ChoreographyTest and AudioTest all PASS. Audio coverage, six voices, morph presence, pause/resume/replacement, music playback and intensity response were exercised in the running game. Fifteen renders reviewed, including Benny apron and new voice settings. Final Windows BuildCookRun succeeded in Saved/PerformancePackaging.log; packaged reports are under Saved/PackagedVerification/Saved. Original player saves were not changed by QA.


## Three authored cases and finite lives - 27 October 2026

Added The Blackout Banquet and The Charity Envelope, each with a consultation, opening, three testimony sequences and resolutions, six case-specific exhibits, a closing choice and verdict. Added twelve evidence plates, two posters, two labelled inspectable Blender props and complete synthetic dialogue. The library now references 138 speech clips, 133 dialogue/feedback sequences and 660.8 seconds of speech. Portrait fills correct the previously dark Brick and Victor shots across every case.

Three lives replace renewable confidence. Evidence and closing mistakes share the budget; a third error saves a failed attempt. Continue and reopening a case preserve failure, and Restart clears its complete attempt. Each case has a separate save slot. Version-2 saves retain progress with at most three lives; before another case updates Continue, an unslotted older trial is preserved in its own slot. Case-files navigation also returns correctly through settings to the previous screen.

Final editor and packaged TrialTest, AnimationTest, ChoreographyTest and AudioTest all PASS. The tests complete all three cases, check independent slots and corrupt saves, migrate an older five-confidence save, preserve an unslotted older trial during a case switch, exercise three evidence mistakes and mixed evidence/closing mistakes, persist failure through reload/menu, and verify a full restart. Audio coverage, 120 animation assets, six cast morphs, speech pause/resume/replacement and four adaptive stems pass. Thirty editor/cooked visual views were reviewed, including each new case, failure, labelled props and all six portraits. Source WAV validation confirms 138 non-silent, non-clipping 24 kHz mono clips.

Final Windows package: Builds/Windows/CourtSimulator.exe. BuildCookRun succeeded in Saved/ExpansionPackaging.log; packaged reports are Saved/PackagedVerification/Saved/{TrialTest,AnimationTest,ChoreographyTest,AudioTest}.txt. The local Zen service recovered automatically after a cache connection retry during the preceding package pass. New case sources and regeneration tools are documented in README.md and Documentation/CaseDesign.md. QA used test-prefixed saves and isolated packaged user data.


## Completed speech timing and case cast - 29 October 2026

Replaced duration-based speech stopping with audio-finished callbacks. Playback percentage drives text reveal and mouth envelopes; overlays pause both. Continue cannot accidentally truncate a playing line, and Skip Voice is explicit. Cinematic skipping preserves the following spoken line. Generated relaxed/normal/quick versions through Kokoro at matching synthesis speeds, retaining voice pitch; changes apply at the next line. Existing preferences migrate once to synchronized text reveal while keeping instant text available.

Added four distinct rigged character models: Renzo Roux (chef), Pip Sparks (stage manager), Nora Notes (vendor), Agnes Penny (volunteer). Case assets switch client/witness meshes, display names and occupations; case dialogue and evidence names were updated consistently. Nora and Agnes use suitable female voice presets. The legal team and first-case cast remain consistent. Corrected persisted skeletal-material array assignments and verified the finished portraits in editor and cooked-game captures.

Final Windows BuildCookRun succeeded (Saved/SpeechCastPackaging.log). Packaged TrialTest, AnimationTest, ChoreographyTest and AudioTest PASS. AudioTest exercises complete natural playback, Continue protection, explicit skip, both alternative paces, multi-speaker feedback completion, pause/resume, reveal/mouth progress and adaptive music. All three cases, lives, saves, migration and restart checks pass. Focused cooked visual review exited successfully and includes the four new models, settings and synchronized reveal (Saved/PackagedVerification/Saved/VisualQA).
