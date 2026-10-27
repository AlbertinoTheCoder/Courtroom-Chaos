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

## Golden Gavel finishing pass — 27 October 2026

This section supersedes the earlier acceptance-gap notes. Runtime case strings moved into a validated editable Data Asset. Added consultation/opening/resolution/closing dialogue, closing choices, transcript, typewriter and skip controls, settings/accessibility options, keyboard focus, results/earned badges, atomic versioned saves and invalid-save recovery.

Expanded all six characters to twenty clips each (120 total), including analytical arm poses for synchronized desk slams and gavel strikes. Added separate animated gavel and block, original foley and character vocal bleeps, detailed evidence illustrations, rotatable/zoomable physical exhibits and inspection notes. Runtime uses Canvas and timed C++ choreography, not UMG or Sequencer. No recorded voice acting or external LLM is claimed.

Editor compilation and the expanded integration tests passed before the overnight pause. Contact test measured defense hand (-253,10,130) cm and gavel bottom 195.1 cm against block top 195.5 cm. Regeneration chain now includes finishing props, UI, case Data Asset and final scene import. Final visual and packaged checks are recorded in FinishChecklist.md.


Final verification completed: editor build succeeded; Windows packaging succeeded with 391 cooked packages. The packaged executable passed case/save validation, live skeletal movement and contact checks. Thirteen rendered views were reviewed, including 130% text, 3D inspection, closing and results. Fixed an input regression found in real mouse QA: NoCapture suppresses primary mouse-down events in Unreal's game viewport; CaptureDuringMouseDown delivers the click without permanent cursor capture. Reduced initial exhibit scale after detecting an instruction-bar overlap. Added isolated deterministic visual capture mode and a repeatable packaged integration test. Full art regeneration was not repeated over verified assets; Python/PowerShell syntax checks passed. Final editable sources and generated content are checkpointed in Git.


Cooked-package screenshots matched the editor. Corrected a cleanup lifetime error discovered after the automated screenshot pass: clearing its own executing timer destroyed lambda storage before the next captured access. The isolated capture mode now requests graceful shutdown directly. Standard shadows explicitly match the SM5 renderer, removing the unsupported virtual-shadow-map editor warning.
