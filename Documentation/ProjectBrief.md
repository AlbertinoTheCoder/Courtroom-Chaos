# PROJECT: COURTROOM CHAOS
## THE ULTIMATE UNREAL ENGINE 5 + BLENDER GAME DEVELOPMENT PROMPT

### YOUR ROLE

You are the lead game developer, technical director, gameplay programmer, 3D artist, character designer, environment artist, animation engineer, UI designer, lighting artist, sound designer, narrative designer, and quality assurance engineer for a new game called **COURTROOM CHAOS**.

Your mission is to develop an extraordinarily entertaining, visually polished, goofy, cartoon-style 3D courtroom game using **Unreal Engine 5 and Blender**.

This is a REAL GAME DEVELOPMENT PROJECT.

Do not merely generate a design document.

Do not create a project containing only cubes, text labels, and placeholder actors.

Do not stop after creating the Unreal project.

Do not declare completion until the game is playable and its essential systems have been tested.

You have permission to make reasonable technical and creative decisions without repeatedly asking for confirmation.

Prioritize a smaller genuinely polished experience over an enormous unfinished one.

**The ultimate goal is a courtroom game where players defend completely ridiculous criminals, interrogate unpredictable witnesses, present evidence, challenge an AI-driven prosecutor, discover hilarious contradictions, and experience dramatic cartoon courtroom battles.**

---

# PART 1: DEVELOPMENT ENVIRONMENT

## 1.1 Software

Primary technologies:

- Unreal Engine 5
- Blender
- Python for automated asset generation
- Unreal Engine C++ where appropriate
- Unreal Engine Blueprints
- Unreal Editor scripting and automation
- Existing Unreal MCP integration, if available
- Blender Python API (`bpy`)
- Unreal UMG for interface development
- Unreal Sequencer for cinematic sequences
- Niagara for particle effects
- Data Assets and Data Tables for content management

Inspect the actual installed versions and available tools before writing version-specific code.

Use the Unreal Engine installation already present on this computer.

Locate Blender and verify that Python scripting works.

Check whether an Unreal MCP server or editor automation integration already exists. Use it if operational.

Do not assume the MCP server is working without testing it.

Do not reinstall software that is already installed correctly.

Do not overwrite unrelated Unreal or Blender projects.

Create a dedicated, clearly named project directory.

## 1.2 Automated development

You should automate as much as realistically possible.

You may:

- Generate Blender models through Python scripts.
- Export Blender assets.
- Import assets into Unreal.
- Create Unreal materials.
- Create Blueprints and gameplay components.
- Generate animation data.
- Configure cameras and lighting.
- Build interface widgets.
- Write C++ classes.
- Write automated tests.
- Run the game to verify functionality.
- Capture screenshots for visual inspection.
- Fix problems you discover.

Use existing tools rather than simulating an editor operation in text.

When an operation cannot be automated reliably, document the precise blocker and choose a supported fallback.

Do not claim a file, asset, animation, or scene exists unless you have actually created and verified it.

## 1.3 Project management

Organize the project into separate directories for:

- Core systems
- Courtroom environments
- Characters
- Character animations
- Materials
- Textures
- User interfaces
- Gameplay
- Dialogue
- Cases
- Evidence
- Cameras
- Cinematics
- Sound
- Visual effects
- Saved data
- Tests
- Developer tools
- Blender source assets

Preserve editable Blender source files.

Keep automatically generated scripts in a separate tools directory.

Avoid polluting the Unreal Content Browser with unused experiments.

Maintain a development log and a list of completed and incomplete features.

Use source control if available, but do not destroy an existing repository history.

---

# PART 2: THE GAME'S IDENTITY

## 2.1 Core concept

COURTROOM CHAOS is a funny, dramatic, interactive courtroom game.

The player is a defense attorney.

Their clients are accused of increasingly ridiculous crimes.

Examples:

- A man accused of stealing 64 emeralds while already owing the bank 64 emeralds.
- A hot dog mascot accused of impersonating a government official.
- A magician accused of making someone's refrigerator disappear.
- A businessman accused of stealing his own wallet.
- A grandma accused of operating an illegal pigeon casino.
- A robot accused of downloading the entire courthouse.
- A man accused of stealing the moon.
- A delivery driver accused of delivering a pizza to himself and demanding payment.
- A duck accused of tax evasion.
- A scientist accused of replacing the courthouse with an inflatable replica.

Cases should be hilariously absurd, but the player must still use actual logic to solve them.

The nonsense is the setting.

The detective work is real.

## 2.2 Core gameplay

The player must:

1. Meet their client.
2. Understand the accusation.
3. Review the evidence.
4. Listen to the prosecutor.
5. Cross-examine witnesses.
6. Identify contradictory statements.
7. Present evidence.
8. Make objections.
9. Challenge opposing arguments.
10. Expose lies or mistakes.
11. Reconstruct what happened.
12. Deliver a convincing final argument.
13. Receive the verdict.

The game should reward careful observation, reasoning, and creative thinking.

It should not randomly decide whether a correct objection succeeds.

## 2.3 Comedy direction

Humor should emerge from personality, timing, and absurd circumstances.

Examples:

A witness confidently claims:

"I remember everything about that night."

The player presents evidence.

The witness responds:

"Except that."

The judge asks:

"Do you have proof?"

The player presents a photograph of a sandwich.

The judge replies:

"That is compelling. Unfortunately I am hungry now."

The prosecutor may dramatically point at the defendant, only to realize they are pointing at a coat rack.

A witness might get nervous and slowly begin sliding down behind the witness stand.

Humor must feel intentional rather than randomly generated.

Use recurring jokes, character quirks, callbacks, physical comedy, and unexpected reactions.

---

# PART 3: ART DIRECTION

## 3.1 CRITICAL REQUIREMENT

**THE GAME MUST LOOK BEAUTIFUL.**

Not necessarily realistic.

Not necessarily graphically expensive.

But visually cohesive, detailed, expressive, and professionally presented.

It must not look like a default Unreal Engine tutorial.

The visual style is:

**POLISHED GOOFY CARTOON 3D.**

Imagine the quality of a charming commercial indie game.

Important visual characteristics:

- Chunky, rounded geometry
- Slightly exaggerated character proportions
- Strong silhouettes
- Expressive faces
- Large animated eyebrows
- Oversized hands
- Colorful clothing
- Smooth stylized surfaces
- Clean material definition
- Soft shadows
- Attractive cinematic lighting
- Exaggerated poses
- Playful architectural design
- Beautifully designed interfaces
- Intentionally exaggerated physics and animation

Do not make the characters realistic humans.

Do not use photorealistic MetaHumans as the final art style.

Do not use the default Unreal mannequin as a final character.

Avoid uncanny human faces.

Characters should resemble charming animated comedy characters.

## 3.2 Shape language

Design objects using simplified appealing geometry.

Large shapes should be clearly readable.

Use bevels, curves, layered surfaces, trim pieces, decorative insets, and strong proportions.

A judge's desk should have:

- A custom silhouette
- Raised decorative trim
- Recessed panels
- A polished wood material
- Gold accents
- A carved emblem
- An oversized gavel
- A microphone
- A nameplate
- Small decorative props

A simple brown cube is not an acceptable final judge's desk.

Primitive geometry may be used as modeling building blocks, but finished objects must contain deliberate shape, material, and detail work.

## 3.3 Color palette

Use a controlled palette.

Suggested primary colors:

- Deep warm brown: `#70462F`
- Medium wood: `#A86D43`
- Cream: `#F5E4C5`
- Courtroom red: `#BD4551`
- Golden yellow: `#E9B954`
- Deep blue: `#304F78`
- Soft teal: `#64A9A0`
- Dark ink: `#24293A`

Use these as a starting palette rather than mandatory colors for every object.

The environment should use warm, relatively restrained colors.

Characters should be more saturated.

Important interactive objects should stand out from their surroundings.

Avoid random bright materials everywhere.

## 3.4 Originality

Develop an original visual identity.

Do not copy copyrighted characters, art, animation, interfaces, music, dialogue, logos, or other assets from existing courtroom games.

The game can take broad inspiration from dramatic courtroom entertainment while having its own original characters, presentation, and mechanics.

Create an original title treatment and recognizable iconography.

---

# PART 4: BUILD THE COURTROOM IN BLENDER

## 4.1 Create actual assets

Blender is a major part of this project.

Do not treat it as an optional afterthought.

Use the Blender Python API to generate actual meshes, materials, and scene assets.

Build detailed, stylized models with coherent proportions.

Create a complete cartoon courtroom asset collection.

## 4.2 Courtroom architecture

Required environment elements:

1. Courtroom floor
2. Decorative walls
3. Raised judge platform
4. Judge's bench
5. Defense attorney desk
6. Prosecutor desk
7. Witness stand
8. Defendant seating area
9. Public audience benches
10. Spectator railing
11. Entrance doors
12. Ceiling architecture
13. Windows
14. Wall decorations
15. Hanging lights or chandeliers
16. Courtroom seal
17. Bookcases
18. Evidence cart
19. Display screen or evidence board
20. Decorative pillars

The environment should feel intentionally designed and lived in.

Avoid a giant empty room with a few scattered desks.

## 4.3 Courtroom proportions

Create a readable cartoon courtroom with a compact playable stage.

Suggested starting dimensions:

- Approximately 18 meters wide
- Approximately 14 meters deep
- Approximately 7 meters high

Adjust these dimensions based on camera composition and character scale.

Prioritize cinematic readability.

The judge should be clearly visible from the player's position.

The witness stand should be framed without obstruction.

The prosecutor and defense attorney should have distinct opposing positions.

Make sure camera shots do not clip through furniture.

## 4.4 Judge's bench

Create an oversized, impressive cartoon judge bench.

It should include:

- Broad curved or segmented front
- Thick beveled surfaces
- Decorative carved panels
- A central golden courtroom emblem
- Raised judge seating
- Oversized leather chair
- Wooden gavel
- Gavel block
- Microphone
- Desk lamps
- Papers
- Small water glass
- Comically large law book
- Brass nameplate

The bench should communicate authority while looking slightly ridiculous.

## 4.5 Witness stand

Create a polished witness stand with:

- Rounded wooden railings
- Raised platform
- Microphone
- Nameplate holder
- Decorative panels
- Small document ledge
- Enough room for expressive character animations

Make it suitable for cinematic close-ups.

## 4.6 Attorney desks

Create unique desks for defense and prosecution.

They should look related but not identical.

Defense desk:

- Slightly messy
- Papers and notebooks
- Evidence folders
- Coffee mug
- Pen holder
- Personal accessories

Prosecution desk:

- More organized
- Carefully aligned documents
- Fancy fountain pen
- High-quality briefcase
- Decorative legal books
- An absurdly polished nameplate

The desks must support hand interactions and dramatic slams.

## 4.7 Secondary decorations

Add visual storytelling through props.

Examples:

- A framed portrait of a suspiciously important duck
- A sign reading "PLEASE DO NOT EAT THE EVIDENCE"
- A stack of law books titled "VERY IMPORTANT LAW"
- A broken courtroom clock
- An overflowing evidence cart
- A framed certificate awarded to the judge for "BEST JUDGE"
- A tiny emergency gavel behind glass
- A plant that looks severely disappointed

Do not overwhelm the scene with jokes.

Keep comedy details secondary to navigation and gameplay.

## 4.8 Blender quality standards

Every significant mesh should have:

- Correct transform values
- Deliberate object origins
- Appropriate bevels
- Correct surface normals
- Clean geometry
- Reasonable polygon counts
- Stable material assignments
- Correct export orientation
- Useful object names
- Appropriate collision planning

Use weighted normals or other appropriate smoothing methods.

Use UV mapping when textures require it.

For procedural solid-color objects, optimized material assignments may be sufficient.

Keep Blender source files organized into collections.

Use a consistent scale system and verify Unreal import sizes.

Remember that Unreal normally measures distance in centimeters while Blender scenes commonly use meters.

Test the export scale rather than blindly multiplying geometry.

## 4.9 Import pipeline

Create a reproducible workflow:

1. Generate the asset in Blender.
2. Validate its geometry.
3. Apply appropriate transforms.
4. Export it in a supported format.
5. Import it into Unreal.
6. Create or assign Unreal materials.
7. Configure collision where necessary.
8. Place it in the level.
9. Verify size and orientation.
10. Inspect the result visually.

Prefer an established, reliable FBX pipeline or another format fully supported by the installed tools.

Do not assume Blender materials will automatically look identical in Unreal.

Rebuild or refine materials inside Unreal where required.

Keep asset generation scripts reusable so that models can be regenerated without manually recreating everything.

---

# PART 5: CHARACTER DESIGN

## 5.1 Overall character style

Characters are one of the most important parts of the game.

They must be memorable and visually expressive.

Use stylized proportions:

- Heads slightly larger than normal
- Large expressive eyes
- Thick eyebrows
- Simplified noses
- Readable mouths
- Slightly oversized hands
- Shorter or exaggerated limbs where appropriate
- Distinct body shapes
- Strong costume silhouettes

Avoid making every character the same body with different colors.

They should be recognizable even as silhouettes.

## 5.2 Main defense attorney

Create an original protagonist.

Working name:

**OLIVER OBJECTION**

Personality:

A surprisingly confident young attorney who usually has absolutely no idea what is happening.

Appearance:

- Messy dark hair
- Oversized blue suit
- Slightly crooked tie
- Large expressive eyebrows
- Big cartoon hands
- Confident but ridiculous facial expressions
- Briefcase full of questionable evidence

Animation personality:

- Dramatic pointing
- Nervous tie adjustment
- Desk slamming
- Sudden realization
- Thinking pose
- Sweating under pressure
- Excessive celebration after tiny victories

The player should immediately enjoy watching this character react to things.

## 5.3 Main prosecutor

Working name:

**VICTOR VAIN**

Personality:

Overconfident, theatrical, smug, and deeply offended whenever someone questions him.

Appearance:

- Purple tailored suit
- Sharp cartoon hairstyle
- Dramatic eyebrows
- Fancy tie
- White gloves
- Slightly exaggerated shoulders
- Constant smug expression

Animation personality:

- Slow sarcastic clapping
- Pointing accusingly
- Adjusting cuffs
- Dramatic hair flip
- Furious document slamming
- Fake sophistication
- Visibly panicking when losing

The prosecutor must react intelligently to the player's arguments.

He should not simply repeat the same accusation forever.

## 5.4 The judge

Working name:

**HONORABLE BARTHOLOMEW BUMBLE**

Personality:

Extremely serious about his job, but unusually easy to distract.

Appearance:

- Huge round body
- Tiny hands
- Enormous white eyebrows
- Ridiculous mustache
- Small round glasses
- Oversized robe
- Giant cartoon gavel

He must be expressive.

Animations:

- Raising eyebrows
- Confused blinking
- Gavel slamming
- Leaning forward suspiciously
- Falling asleep briefly
- Shocked reactions
- Slow head turns
- Disappointed stare

He should look authoritative and ridiculous simultaneously.

## 5.5 Bailiff

Working name:

**OFFICER BRICK**

Appearance:

- Very broad shoulders
- Tiny head
- Oversized uniform
- Serious expression
- Extremely formal posture

Personality:

Treats the most ridiculous events as completely normal.

He is used to courtroom chaos.

He barely reacts to anything.

His deadpan behavior should be funny.

## 5.6 Character modeling

Create original Blender character meshes.

Do not assume generating a head and torso from spheres automatically produces an appealing character.

Design:

- Facial structure
- Eyes and eyelids
- Eyebrows
- Mouth geometry
- Hair
- Clothing layers
- Hands
- Shoes
- Accessories

Use smooth cartoon shapes and intentional proportions.

Produce character turnaround views or equivalent visual checks.

Rig characters with a suitable animation skeleton.

Ensure that the arms, elbows, fingers, neck, head, and torso can support the required animations.

Use blend shapes, shape keys, facial bones, or an appropriate combination for expressions.

Test deformation before importing final animation clips.

---

# PART 6: ANIMATION SYSTEM

## 6.1 Animation philosophy

This game MUST have expressive animation.

Characters standing still while text appears is not enough.

Create a reusable animation system.

Required baseline animation states:

- Neutral idle
- Listening
- Speaking
- Thinking
- Confused
- Happy
- Smug
- Angry
- Nervous
- Shocked
- Sad
- Suspicious
- Frustrated
- Pointing
- Desk slamming
- Leaning forward
- Leaning backward
- Dramatic celebration
- Embarrassed reaction

Not every character needs an identical animation.

Each character should have their own personality-specific variations.

## 6.2 Cartoon animation principles

Use:

- Anticipation
- Squash and stretch where technically appropriate
- Overshoot
- Follow-through
- Snappy timing
- Exaggerated poses
- Clear silhouettes
- Hold frames for comedy
- Secondary motion

The motion should feel intentionally animated.

Avoid unnaturally slow movements and stiff linear interpolation.

## 6.3 Objection animation

The objection sequence is one of the most important moments in the game.

When the player successfully objects:

1. The music briefly stops.
2. The attorney takes a dramatic pose.
3. The camera rapidly moves closer.
4. The attorney points forward.
5. A huge stylized objection graphic appears.
6. A powerful cartoon impact sound plays.
7. The screen shakes briefly.
8. Comic-style speed lines appear.
9. The witness or prosecutor reacts.
10. The camera switches to the reaction shot.
11. The scene resumes with dramatic music.

Make the sequence extremely satisfying.

Allow the player to skip repeated cinematic animations after seeing them.

## 6.4 Desk slam

Create proper interaction between character hands and desk surfaces.

The character should not clip through furniture.

The impact should trigger:

- A sharp sound effect
- Small camera shake
- Tiny dust burst
- Optional flying papers
- A quick reaction from another character

Use an animation event or equivalent mechanism to synchronize the impact.

## 6.5 Dialogue animation

Characters should move during conversations.

Use speech animation states and subtle facial changes.

Optional mouth flapping is acceptable for the initial version.

More advanced phoneme-based or audio-driven lip synchronization can be added later.

Avoid perfectly static faces.

Expressions must be selected contextually.

A furious prosecutor should not smile while delivering an angry line.

---

# PART 7: CAMERA AND CINEMATICS

## 7.1 Camera system

Create a reusable cinematic camera system.

Required camera presets:

- Courtroom establishing shot
- Defense attorney medium shot
- Defense attorney close-up
- Prosecutor medium shot
- Prosecutor close-up
- Witness medium shot
- Witness close-up
- Judge close-up
- Evidence close-up
- Over-the-shoulder shot
- Dramatic low-angle shot
- Reaction shot
- Verdict shot

Use Unreal Camera Actors, Cine Camera Actors, Sequencer, or suitable systems.

## 7.2 Cinematic presentation

Dialogue should resemble a lively animated legal comedy.

Camera changes should be motivated by dramatic moments.

Examples:

A witness starts lying.

The camera slowly pushes in.

The player finds a contradiction.

The camera sharply cuts to the evidence.

The prosecutor realizes something is wrong.

The camera cuts to his terrified face.

The judge becomes confused.

The camera slowly zooms toward his giant eyebrows.

Use visual storytelling rather than relying exclusively on text.

## 7.3 Camera movement

Implement smooth movement with appropriate easing.

Do not make every camera move linear.

Avoid excessive camera movement during normal dialogue.

Use rapid cuts primarily for dramatic or comedic moments.

## 7.4 Cinematic quality checks

Verify:

- Faces stay in frame
- Important expressions are visible
- Heads are not accidentally cropped
- Furniture does not block important shots
- Lighting remains consistent
- UI does not obscure faces
- Camera movement does not become nauseating
- The selected speaker is visually clear

---

# PART 8: THE CORE TRIAL GAMEPLAY SYSTEM

## 8.1 Trial state machine

Implement a reliable trial progression system.

Suggested phases:

1. Case introduction
2. Client consultation
3. Opening prosecution argument
4. Opening defense response
5. Witness testimony
6. Cross-examination
7. Evidence challenge
8. Counterargument
9. New testimony
10. Final argument
11. Verdict
12. Case results

The system must track current phase, witness, statement, evidence, and important discoveries.

Do not implement the trial solely as a massive hardcoded sequence of `if` statements.

Use structured case data and reusable gameplay systems.

## 8.2 Witness testimony

Witnesses deliver statements one at a time.

The player can:

- Read the statement
- Revisit previous statements
- Ask for clarification
- Press the witness
- Open the evidence inventory
- Present relevant evidence
- Make an objection when appropriate

The player should be able to inspect testimony without losing progress.

## 8.3 Pressing witnesses

Provide a **PRESS** interaction.

Pressing a witness asks them to elaborate.

This may:

- Reveal additional details
- Create new testimony
- Expose suspicious wording
- Unlock new topics
- Change emotional state
- Cause the prosecutor to interrupt
- Introduce a new contradiction

The response must correspond meaningfully to the selected statement.

## 8.4 Presenting evidence

Create an evidence system.

Every evidence item should contain:

- Unique ID
- Display name
- Description
- Category
- Image or 3D representation
- Discovery state
- Inspection details
- Optional associated testimony
- Optional contradiction metadata

Evidence should be browsable in a polished interface.

A player should be able to inspect clues closely.

Examples:

- Security photograph
- Broken clock
- Suspicious receipt
- Strange sandwich
- Golden gavel
- Witness testimony transcript
- Delivery note
- Courtroom access card

## 8.5 Contradiction detection

Do not base success purely on matching words.

The game should track logical contradictions between established evidence and statements.

For an authored case, define valid evidence-to-statement relationships explicitly.

Example:

Witness:

"The courtroom lights were working the entire evening."

Evidence:

A maintenance report proves the power was out.

Correct response:

Present the maintenance report against that statement.

Incorrect evidence should not magically be treated as correct.

## 8.6 Objection feedback

Successful objection:

- Dramatic animation
- Relevant new dialogue
- Witness reaction
- Prosecutor reaction
- Updated case progression

Unsuccessful objection:

- Appropriate funny response
- Explanation that does not reveal the answer
- Optional credibility penalty
- Opportunity to retry

Avoid punishing players harshly for learning the mechanics.

## 8.7 Credibility meter

Create a courtroom credibility meter.

It represents how seriously the judge takes the defense.

Incorrect accusations reduce credibility.

Strong evidence can restore some confidence.

Do not make correct solutions impossible because of a slightly low meter.

Provide reasonable checkpoint and restart behavior.

## 8.8 Final argument

At the end of the trial, allow the player to reconstruct the case.

Example:

"What actually happened to the missing gavel?"

The player selects the correct sequence of events.

Then the defense delivers a dramatic final explanation.

The judge considers the evidence.

The verdict follows.

---

# PART 9: AI COURTROOM INTELLIGENCE

## 9.1 AI design goal

The game should feel like the courtroom characters can respond intelligently.

The prosecutor should challenge the player's reasoning.

Witnesses should react to unexpected questions.

Characters should remember important evidence during a case.

However, the AI must not destroy the mystery by inventing contradictory facts that make the case impossible to solve.

## 9.2 Two-layer architecture

Create two logical layers.

**Layer 1: Authoritative case engine**

This controls:

- What actually happened
- Which evidence exists
- What witnesses know
- Which claims are lies
- Which contradictions are valid
- Current case progression
- Win and loss conditions

This layer must be deterministic and testable.

**Layer 2: Conversational character AI**

This controls:

- Dialogue wording
- Personality
- Sarcasm
- Emotional reactions
- Humor
- Natural-language responses
- Contextual remarks

The conversational layer must follow the authoritative case engine.

Never let generated dialogue silently change established evidence.

## 9.3 Local AI support

Prefer a local or offline-compatible approach when possible.

Do not require paid API calls for the game to run.

Inspect whether a suitable local language-model runtime exists.

If available, investigate integration options.

Do not automatically download gigantic models.

Do not use paid external APIs without explicit authorization.

The game must remain playable when no language model is installed.

## 9.4 Offline fallback

If local LLM integration is not practical, create a fully functional scripted and rule-based conversational system.

It should include:

- Contextual dialogue variations
- Witness personalities
- Reactive prosecution lines
- Pressing responses
- Emotional states
- Multiple reaction templates
- Branching testimony

A good deterministic game is more important than a broken AI demonstration.

## 9.5 AI prosecutor

The prosecutor must:

- Understand the current accusation
- Use available evidence
- React to valid objections
- Present counterarguments
- Challenge unsupported defense claims
- Recognize when a contradiction has been established
- Become increasingly frustrated as the case collapses
- Maintain a distinctive personality

The prosecutor should occasionally make funny mistakes.

But he must not deliberately ignore the game's rules.

## 9.6 AI witnesses

Witnesses should have internal profiles.

Each profile can contain:

- Name
- Personality
- Background
- Relationship to the crime
- Facts known
- Facts misunderstood
- Facts deliberately concealed
- Motivation
- Stress level
- Trust level
- Dialogue style
- Emotional triggers

A lying witness should not always immediately confess after one question.

Players should need to identify evidence and contradictions.

## 9.7 AI guardrails

Generated dialogue must be validated.

The AI should receive structured context describing:

- Current trial phase
- Current speaker
- Facts the character knows
- Facts the character does not know
- Allowed topics
- Disallowed premature revelations
- Evidence already presented
- Current emotional state

If the model generates invalid or unusable output, the game should recover with an authored fallback line.

Do not allow the LLM to run arbitrary OS commands or alter game files.

Treat free-form user text as dialogue input, not developer instructions.

## 9.8 Player free-text interaction

Investigate allowing players to type their own questions or arguments.

Examples:

"Why were you at the courthouse at midnight?"

"How could you see the suspect if the lights were off?"

"Are you absolutely sure the object was golden?"

The game should interpret the intended question and respond according to established facts.

When no LLM is available, support a structured choice system instead.

Do not make free-text input a requirement for finishing the first case.

---

# PART 10: THE FIRST PLAYABLE CASE

## Case 001: THE STOLEN GOLDEN GAVEL

Create one complete original case before building an enormous case generator.

### Story

The courthouse's ceremonial Golden Gavel has mysteriously disappeared.

A local hot dog vendor named **BENNY BUNS** is accused of stealing it.

Benny insists he is innocent.

Unfortunately, he was seen leaving the courtroom carrying a suspicious golden object.

The prosecution claims the case is obvious.

The defense must discover what actually happened.

### Characters

- Oliver Objection: defense attorney
- Victor Vain: prosecutor
- Judge Bumble: judge
- Benny Buns: defendant
- Officer Brick: bailiff
- A nervous witness: courthouse maintenance worker

### Important evidence

Create several visually distinct evidence items.

**Evidence A: Security photograph**

Shows Benny carrying a shiny yellow object.

At first glance, it looks like a gavel.

Closer inspection reveals an unusual shape.

**Evidence B: Mustard dispenser**

Benny's oversized golden-colored mustard dispenser.

It resembles the object in the photograph.

**Evidence C: Maintenance report**

Documents a planned courtroom maintenance operation.

**Evidence D: Courtroom inventory sheet**

Shows when the ceremonial gavel was last officially accounted for.

**Evidence E: Evidence cart record**

Documents the movement of several courtroom objects during cleaning.

**Evidence F: Storage room photograph**

Contains an important background detail revealing the gavel's actual location.

### True timeline

Design one coherent canonical timeline.

For the initial version:

1. The courtroom prepares for a special public ceremony.
2. The ceremonial gavel is temporarily moved during cleaning.
3. Officer Brick places it on a cart with other courtroom objects.
4. The cart is moved to storage.
5. Benny enters the courthouse to deliver food.
6. A witness sees him carrying his golden mustard dispenser.
7. The witness mistakenly assumes he has stolen the gavel.
8. The security photograph appears to support the accusation.
9. The player identifies the mistaken object and missing timeline information.
10. The gavel is ultimately found among the relocated courtroom objects.

No actual theft occurred.

The defendant is innocent.

### Gameplay structure

The first testimony establishes the accusation.

The second sequence allows the player to inspect the security photograph.

The next sequence reveals the maintenance activity.

A later contradiction exposes the gap in the prosecution's timeline.

Finally, the player connects the storage record to the gavel's real location.

Use at least three meaningful contradiction or deduction moments.

Do not make every solution simply "click the only glowing evidence."

### Comedic dialogue

Write original funny dialogue throughout.

Example:

PROSECUTOR:

"The defendant was caught carrying a golden object!"

DEFENSE:

"Your Honor, that object is mustard."

JUDGE:

"Mustard?"

DEFENSE:

"Yes, Your Honor."

JUDGE:

"Objection. I prefer ketchup."

The humor should be integrated into a coherent trial rather than replacing actual investigation.

### Case completion requirements

The case is complete only when:

- The player can start it from a menu.
- Introductory dialogue works.
- Witness testimony appears correctly.
- Evidence can be inspected.
- Pressing witnesses functions.
- Correct contradictions advance the trial.
- Incorrect evidence produces appropriate feedback.
- Cameras and animations trigger.
- The final deduction can be completed.
- The verdict is displayed.
- The player can return to the case selection screen.

---

# PART 11: FUTURE PROCEDURAL CASE GENERATION

Build the architecture so additional cases can be added without rewriting the entire game.

Eventually, allow absurd procedurally assembled crimes.

Potential systems:

- Random defendants
- Random alleged crimes
- Witness selection
- Evidence selection
- Location variation
- Motive selection
- Secret information
- Timeline generation
- Personality-driven dialogue

But DO NOT implement random case generation before the first authored case works properly.

Generated cases require logical validation.

Before presenting a generated case, ensure:

- There is a canonical explanation.
- Evidence supports that explanation.
- The player has enough information to solve it.
- Contradictions are logically valid.
- The case does not accidentally have multiple incompatible solutions.
- Required evidence cannot become inaccessible.
- The final verdict corresponds to the established facts.

Use structured templates or constrained generation instead of unrestricted randomness.

---

# PART 12: USER INTERFACE DESIGN

## 12.1 Main menu

Create a proper animated main menu.

Required options:

- Start Game
- Continue
- Case Selection
- Settings
- Credits
- Quit

Use a live or animated courtroom backdrop.

Show the game's title prominently.

Add subtle environmental motion.

Buttons should have satisfying hover and click animations.

## 12.2 Dialogue interface

Create a beautiful dialogue box.

Requirements:

- Clearly visible speaker name
- Legible text
- Controlled text reveal speed
- Continue indicator
- Optional character expression indicator
- Speech history access
- Keyboard and mouse support
- Skippable text animation
- Reliable text wrapping

The interface should look custom-made for this game.

Avoid default gray rectangles.

## 12.3 Evidence inventory

Create an evidence interface containing:

- Evidence thumbnails
- Item names
- Detailed descriptions
- Inspection option
- Category organization
- Current selection highlight
- Present button
- Back button

Support viewing selected evidence in a dedicated inspection presentation.

If practical, allow players to rotate 3D evidence objects.

## 12.4 Trial HUD

Show only necessary information during gameplay.

Potential elements:

- Current speaker
- Current testimony
- Credibility meter
- Evidence access button
- Press button
- Present button
- Dialogue history button
- Pause button

Avoid cluttering the screen.

## 12.5 Objection display

Create an original visual treatment for dramatic objections.

Use:

- Oversized bold typography
- Cartoon comic-book impact shapes
- Strong contrasting colors
- Rapid scale animation
- Slight rotation
- Speed lines
- Impact sound
- Dramatic camera framing

The effect should feel powerful but remain readable.

## 12.6 Verdict screen

Create a theatrical verdict presentation.

The judge raises his gavel.

The music changes.

The camera moves closer.

The player sees the result.

Possible results:

- NOT GUILTY
- GUILTY
- CASE DISMISSED

The initial case should support its authored verdict reliably.

Add suitable character reactions.

---

# PART 13: AUDIO AND MUSIC

## 13.1 Sound direction

Audio should be playful, energetic, and exaggerated.

Use original or properly licensed assets.

Do not download or reproduce copyrighted courtroom game soundtracks.

Required sound events:

- Gavel impact
- Desk slam
- Objection impact
- Correct evidence
- Incorrect evidence
- Button hover
- Button click
- Paper handling
- Shock reaction
- Comedic failure
- Victory celebration
- Verdict reveal

## 13.2 Music themes

Plan music for:

- Main menu
- Normal courtroom dialogue
- Suspenseful testimony
- Cross-examination
- Successful contradiction
- Final argument
- Verdict
- Victory
- Defeat

Use dynamic music transitions where feasible.

Do not rely on paid music generation tools.

If final music is unavailable, build and test the music event system with openly licensed or temporary original audio, documenting replacement needs honestly.

## 13.3 Character voices

Full voice acting is optional.

The first playable version should not depend on externally generated voice acting.

Consider:

- Expressive vocal grunts
- Comedic reaction sounds
- Short character-specific speech effects
- Different voice pitches
- Appropriate subtitle support

Implement clean audio interfaces so better voices can be added later.

---

# PART 14: VISUAL EFFECTS

## 14.1 Core effects

Create stylized effects for:

- Objections
- Desk impacts
- Gavel impacts
- Discovery of evidence
- Witness nervousness
- Major revelations
- Incorrect argument reactions
- Victory moments

Use Niagara or appropriate Unreal systems.

Effects should feel animated and satisfying.

## 14.2 Special visual moments

Examples:

**The Witness Meltdown**

A witness panics after being caught lying.

Their eyes widen.

Their face changes expression.

A few cartoon sweat droplets appear.

Papers fly from their hands.

The camera zooms dramatically.

**The Prosecutor Collapse**

The prosecutor realizes his strongest argument has failed.

He stares silently.

His dramatic pose slowly collapses.

A tiny sad sound plays.

**The Judge's Ultimate Gavel Slam**

The judge raises an absurdly large gavel.

The camera tracks upward.

He slams it down.

A giant comic impact burst appears.

The entire courtroom briefly shakes.

Use these effects sparingly so major moments stay special.

---

# PART 15: LIGHTING AND RENDERING

## 15.1 Lighting style

Create a warm, theatrical cartoon courtroom.

Prioritize:

- Readable faces
- Clear silhouettes
- Attractive highlights
- Soft shadows
- Warm environmental colors
- Balanced exposure
- Consistent character illumination

Avoid extreme darkness.

Avoid muddy shadows.

Avoid excessively shiny materials.

## 15.2 Lighting setup

Use an appropriate combination of:

- Directional lighting
- Skylight or ambient fill
- Warm artificial interior lights
- Accent lighting
- Selective character lighting
- Reflection support

Investigate whether Lumen is appropriate for the installed hardware.

Do not require expensive real-time global illumination if a cheaper setup achieves a better and more stable result.

## 15.3 Performance modes

Provide sensible graphics scalability.

Target a responsive desktop experience.

Prefer smooth 1080p gameplay with attractive stylized graphics.

Test performance on the actual computer rather than assuming it will be fast.

Support adjustable:

- Resolution
- Fullscreen/windowed mode
- Shadows
- Post-processing
- Anti-aliasing
- Effects quality
- Frame-rate limit

Avoid computationally expensive features that add little visual benefit to a cartoon game.

---

# PART 16: GAME FEEL

## 16.1 Responsiveness

Every important player interaction should produce immediate feedback.

Buttons should visibly react.

Evidence selection should feel crisp.

Transitions should not feel sluggish.

Dialogue should not unnecessarily lock the player into long animations.

## 16.2 Input support

Implement mouse and keyboard controls.

Recommended controls:

- Left click: select and continue
- Enter or Space: advance dialogue
- Escape: pause or back
- Evidence shortcut
- Press witness shortcut
- Present evidence shortcut
- Dialogue history shortcut

Expose controls in the settings menu.

Avoid hardcoded input behavior that prevents rebinding later.

## 16.3 Accessibility

Include:

- Adjustable text speed
- Legible subtitles
- Reduced screen shake option
- Skippable cinematics
- Volume sliders
- Color-independent important feedback
- Clear focus indicators
- Comfortable UI sizing

Make the game enjoyable without requiring perfect timing or reflexes.

---

# PART 17: GAME ARCHITECTURE

## 17.1 Core systems

Design reusable systems for:

- Game state
- Case management
- Trial progression
- Dialogue
- Character reactions
- Evidence
- Testimony
- Objections
- Camera direction
- Animation triggers
- Audio events
- UI
- Save/load
- Case results

Use clear ownership and communication between components.

Avoid tightly coupling every system to one giant Blueprint.

## 17.2 Data-driven content

Separate narrative data from gameplay code.

A case definition should contain:

- Metadata
- Characters
- Evidence
- Locations
- Trial phases
- Testimony
- Valid contradictions
- Pressing dialogue
- Emotional reactions
- Branch conditions
- Verdict rules

Make it possible to add additional cases without rewriting the trial engine.

## 17.3 Save system

Implement saving for:

- Current case
- Trial phase
- Unlocked evidence
- Completed contradictions
- Player settings
- Completed cases

Add automatic checkpoints at appropriate stages.

Do not lose player progress because of normal menu navigation.

## 17.4 Debugging tools

Create development-only tools to:

- Jump to a trial phase
- Unlock evidence
- Reset a case
- Preview character expressions
- Preview animations
- Test camera transitions
- Trigger objection sequences
- Inspect case state
- Display logical validation errors

Keep debugging controls out of normal player-facing menus.

---

# PART 18: THE ASSET PRODUCTION PIPELINE

## 18.1 Required outputs

Produce actual Blender source files for the important original 3D assets.

Create export files as needed.

Import and verify the exported assets in Unreal.

Maintain consistent naming.

Example naming conventions:

- `SM_JudgeBench`
- `SM_WitnessStand`
- `SM_DefenseDesk`
- `SM_ProsecutionDesk`
- `SM_Gavel`
- `SM_CourtroomDoor`
- `SK_OliverObjection`
- `SK_VictorVain`
- `SK_JudgeBumble`
- `M_StylizedWood`
- `M_StylizedGold`
- `WBP_TrialHUD`
- `WBP_EvidenceInventory`
- `BP_TrialManager`

Use conventions appropriate to the actual asset type.

## 18.2 Asset preview scenes

Create a dedicated asset showcase or inspection level.

Use it to evaluate:

- Material quality
- Character proportions
- Mesh smoothing
- Scale
- Lighting
- Surface details
- Visual consistency

Do not import dozens of objects without inspecting any of them.

## 18.3 Character production priority

Create polished versions of the essential characters before generating an endless collection of witnesses.

Priority:

1. Defense attorney
2. Prosecutor
3. Judge
4. First witness
5. Defendant
6. Bailiff

Reuse animation systems where appropriate, but preserve character personality.

## 18.4 Asset reuse

Reusable assets are encouraged.

Examples:

- Courtroom trim modules
- Decorative panels
- Book meshes
- Benches
- Lamps
- Paper props
- Evidence containers
- Nameplates
- Chairs

Reuse assets intelligently.

Do not clone an identical mesh everywhere without variation in scale, layout, or detail.

---

# PART 19: DEVELOPMENT PHASES

Complete the project incrementally.

Each phase should produce meaningful, verifiable progress.

## PHASE 0: ENVIRONMENT VALIDATION

Tasks:

1. Locate Unreal Engine.
2. Locate Blender.
3. Verify automation capabilities.
4. Locate available project directories.
5. Confirm the chosen project location.
6. Create the project.
7. Establish folder structure.
8. Configure basic source control or backups.
9. Run a minimal build or editor test.

Deliverable:

A valid project that opens successfully.

## PHASE 1: VISUAL FOUNDATION

Tasks:

1. Establish the art bible.
2. Define the final palette.
3. Build the courtroom architectural model.
4. Create essential furniture.
5. Import assets.
6. Set up materials.
7. Add lighting.
8. Configure cameras.
9. Create a first presentation-quality courtroom view.

Deliverable:

A visually appealing courtroom scene.

Do not proceed with an ugly graybox as though it is finished.

## PHASE 2: CHARACTER FOUNDATION

Tasks:

1. Model the defense attorney.
2. Model the prosecutor.
3. Model the judge.
4. Build basic rigs.
5. Create core expressions.
6. Implement idle animations.
7. Add speaking animation states.
8. Import and test them.
9. Place the characters in the courtroom.
10. Verify cinematic framing.

Deliverable:

A courtroom populated with recognizable, expressive cartoon characters.

## PHASE 3: TRIAL FRAMEWORK

Tasks:

1. Implement trial phases.
2. Implement structured dialogue data.
3. Implement dialogue UI.
4. Implement camera switching.
5. Implement testimony presentation.
6. Implement evidence inventory.
7. Implement selecting and presenting evidence.
8. Implement objections.
9. Implement basic credibility.
10. Implement trial progression.

Deliverable:

A simple playable courtroom interaction.

## PHASE 4: FIRST CASE

Tasks:

1. Create the Golden Gavel case data.
2. Build evidence models and images.
3. Write polished dialogue.
4. Create witness testimony.
5. Implement contradictions.
6. Add pressing interactions.
7. Add prosecution responses.
8. Add the final deduction.
9. Implement verdict logic.
10. Test all normal gameplay paths.

Deliverable:

One complete, logically solvable case.

## PHASE 5: PRESENTATION POLISH

Tasks:

1. Add cinematic camera movements.
2. Add reaction animations.
3. Add objection sequences.
4. Add desk slams.
5. Add gavel effects.
6. Improve the UI.
7. Add audio.
8. Improve lighting.
9. Add environmental details.
10. Add menu transitions.

Deliverable:

A visually polished vertical slice.

## PHASE 6: INTELLIGENT DIALOGUE

Tasks:

1. Introduce character knowledge profiles.
2. Add conversational state tracking.
3. Add reactive prosecutor responses.
4. Add conditional witness behavior.
5. Evaluate local LLM integration.
6. Add validated AI dialogue where practical.
7. Preserve a fully playable offline fallback.
8. Test that AI never breaks case logic.

Deliverable:

More natural and reactive courtroom conversations.

## PHASE 7: FINAL TESTING

Tasks:

1. Test a new game.
2. Test loading a saved game.
3. Complete the first case.
4. Test every important contradiction.
5. Test incorrect evidence.
6. Test repeated button presses.
7. Test menu navigation.
8. Test graphics settings.
9. Test audio settings.
10. Test cinematic skipping.
11. Test dialogue history.
12. Test performance.
13. Test asset references.
14. Test a packaged build.

Deliverable:

A game that can be opened and played without needing Unreal Editor development controls.

---

# PART 20: QUALITY ASSURANCE

## 20.1 Gameplay testing

Create automated tests for the deterministic logic wherever possible.

Verify that:

- Correct evidence is accepted.
- Incorrect evidence is rejected.
- No required evidence disappears.
- Testimony progression is valid.
- The player cannot accidentally skip essential phases.
- Verdict conditions are correct.
- Save/load preserves progress.
- Restarting the trial works.

## 20.2 Visual testing

Capture screenshots from important cameras.

Inspect:

- Judge close-up
- Attorney close-up
- Prosecutor close-up
- Witness close-up
- Full courtroom
- Evidence inventory
- Objection animation
- Verdict screen
- Main menu

Identify:

- Clipping meshes
- Broken normals
- Incorrect material assignments
- Ugly lighting
- Excessive empty space
- Unreadable text
- Bad framing
- Animation deformation
- Floating props
- Characters intersecting furniture

Fix problems instead of documenting them as acceptable.

## 20.3 Technical testing

Verify:

- Unreal launches the project.
- Necessary assets load.
- Required Blueprints compile.
- C++ code compiles where applicable.
- Relevant tests pass.
- The chosen map opens.
- Runtime errors are investigated.
- Packaging succeeds when supported.
- No critical assets are missing from packaged builds.

## 20.4 Crash prevention

Handle failures gracefully.

Examples:

- Missing dialogue entries
- Missing evidence references
- Missing character meshes
- Missing audio assets
- Unavailable AI backend
- Invalid save files

The game should report or recover from these problems appropriately rather than simply crash.

---

# PART 21: EXTREME VISUAL QUALITY RULES

These are non-negotiable design principles.

## Rule 1: NO PROTOTYPE LOOK

The final presentation must never resemble an unfinished Unreal tutorial.

## Rule 2: NO PLACEHOLDER ABUSE

Basic shapes are acceptable during development.

They are not acceptable replacements for intentionally designed final assets.

## Rule 3: NO BORING CHARACTERS

Characters should have distinctive silhouettes, costumes, expressions, and animation.

## Rule 4: NO DEAD SCENES

The courtroom needs lighting, composition, detail, and environmental personality.

## Rule 5: NO DEFAULT-LOOKING UI

Create a custom visual language for buttons, panels, evidence windows, and menus.

## Rule 6: NO RANDOM ASSET STYLES

Everything must look like it belongs in the same game.

## Rule 7: NO FAKE FEATURES

A menu button is not a feature unless it performs its intended action.

An evidence inventory is not complete unless the player can actually use it.

An AI system is not implemented merely because a file has AI in its name.

## Rule 8: NO CLAIMING SUCCESS WITHOUT TESTING

Verify functionality with actual editor or runtime execution.

## Rule 9: NO UNNECESSARY PAID SERVICES

Prefer installed software, local tools, procedural generation, and open-source dependencies.

Request authorization before introducing paid subscriptions, APIs, or significant downloads.

## Rule 10: NO COPYRIGHTED ASSET CLONING

Use original designs and properly licensed materials.

## Rule 11: NO DESTRUCTIVE SHORTCUTS

Do not delete unrelated user projects.

Do not modify system settings unnecessarily.

Do not overwrite valuable assets without preserving recoverable versions.

## Rule 12: DO NOT SACRIFICE PLAYABILITY FOR VISUALS

Beautiful graphics are pointless if the trial cannot be completed.

Both gameplay and presentation matter.

---

# PART 22: FUN EXTRA FEATURES

After the first complete case works, consider implementing the following features.

These are expansion ideas, not blockers for the vertical slice.

## 22.1 Courtroom reputation

Track the player's reputation as an attorney.

Possible titles:

- Suspicious Intern
- Questionable Lawyer
- Certified Objector
- Courtroom Menace
- Legal Disaster
- Legendary Defense Attorney

Use gameplay achievements rather than arbitrary grinding.

## 22.2 Witness breakdowns

Create several special animated breakdown reactions.

Examples:

- A witness melts dramatically into their chair.
- A businessman removes five increasingly smaller hats.
- A magician accidentally reveals a hidden rabbit.
- A witness's fake mustache falls off.
- A witness confidently points at themselves.
- A character tries to leave but walks into the wrong door.

## 22.3 Secret evidence

Hide optional clues in evidence inspections.

Examples:

- A suspicious label on a coffee cup
- An incorrect date on a receipt
- A reflection in a photograph
- Something hidden behind an evidence bag
- A tiny note under a book

Optional clues may unlock dialogue or achievements.

Essential evidence must remain reasonably discoverable.

## 22.4 Courtroom reactions

Make characters react to dramatic moments.

Examples:

- Audience gasping
- Judge dropping glasses
- Bailiff slowly turning around
- Prosecutor staring silently
- Defendant celebrating too early
- Witness pretending to faint

## 22.5 Funny achievements

Possible achievements:

- First Objection
- Wrong Evidence, Wrong Confidence
- The Judge Is Confused
- Professional Overthinker
- Zero Credibility Remaining
- Objection Overload
- Justice Served, Probably

## 22.6 Replay mode

After completing a case, allow players to revisit memorable courtroom moments.

Potential features:

- Replay objections
- Rewatch verdicts
- View evidence discoveries
- Read completed testimony
- Review case outcomes

## 22.7 Custom case editor

Long-term possibility:

Allow players to design ridiculous cases.

Features might include:

- Choose a defendant
- Choose an accusation
- Place evidence
- Write testimony
- Define contradictions
- Select witnesses
- Set verdict conditions
- Test case consistency

Do not prioritize this over finishing the initial game.

---

# PART 23: PERFORMANCE AND RESOURCE MANAGEMENT

Use efficient, well-organized assets.

Apply appropriate:

- Texture sizes
- Polygon budgets
- LODs where useful
- Animation compression
- Material reuse
- Asset streaming
- Particle limits
- Shadow settings

The game is a stylized courtroom experience.

It should not require an extremely expensive GPU.

Measure actual performance.

Avoid loading excessive assets into memory unnecessarily.

Keep Blender procedural generation scripts efficient.

Avoid accidentally producing millions of polygons for simple furniture.

Use quality settings so players can trade visual fidelity for frame rate.

---

# PART 24: SCREENSHOT-BASED VISUAL REVIEW

Visual quality must be checked throughout development.

After building the courtroom:

1. Capture an actual screenshot.
2. Inspect the composition.
3. Compare it against the art bible.
4. Identify missing visual details.
5. Improve lighting and materials.
6. Fix scale problems.
7. Capture another screenshot.

After importing a character:

1. Capture front and side views.
2. Check proportions.
3. Check facial appeal.
4. Check clothing and accessories.
5. Test deformation.
6. Improve the model if it looks unfinished.

After building the UI:

1. Display it at the actual game resolution.
2. Inspect text readability.
3. Verify consistent spacing.
4. Test button states.
5. Check overlap.
6. Confirm animations work.

Do not assume generated content looks good merely because it imported successfully.

If screenshot tools are unavailable, record that limitation and use the most reliable available inspection method.

---

# PART 25: DEVELOPMENT COMMUNICATION

Provide meaningful reports after each major milestone.

Each report should explain:

- What was actually created
- Which files were modified
- Which Unreal systems work
- Which Blender assets were generated
- What was tested
- What remains unfinished
- Any important technical blockers
- What should be built next

Use concise development summaries.

Do not repeatedly ask for decisions you can reasonably make yourself.

Do not generate enormous explanations in place of actually creating the project.

When encountering an error, investigate it.

Attempt reasonable fixes.

Do not hide failures.

If a feature requires unavailable software or permissions, document the exact issue and proceed with other useful work.

---

# PART 26: ACCEPTANCE CRITERIA

The first major milestone is successful when all the following are true.

### Environment

- A real stylized courtroom exists.
- Essential furniture is modeled and imported.
- Materials are coherent.
- Lighting is visually attractive.
- Camera angles are functional.

### Characters

- The essential characters are visually distinct.
- Their meshes are properly imported.
- Their animation states work.
- Their expressions are visible.
- They do not constantly clip through furniture.

### Gameplay

- The player can start the Golden Gavel case.
- The player can read dialogue.
- Witnesses can be questioned.
- Evidence can be inspected.
- Correct evidence advances the trial.
- Incorrect evidence produces feedback.
- A complete ending exists.

### Presentation

- Dialogue UI is polished.
- Cameras react to important events.
- Objection animations work.
- Basic audio feedback exists.
- The verdict sequence works.

### Technical

- Project opens reliably.
- Core gameplay tests pass.
- No critical runtime blockers remain.
- The development assets are organized.
- Source files are preserved.
- The game can be launched and played.

Do not call this milestone complete unless these criteria have been verified.

If some criteria remain incomplete, report the genuine completion status.

---

# PART 27: YOUR FIRST EXECUTION INSTRUCTIONS

Start working immediately.

Do the following in order:

**STEP 1**

Inspect the computer's available Unreal Engine and Blender installation details.

Check existing Unreal automation tools and the current project structure.

**STEP 2**

Select a safe dedicated project location.

Create or initialize the Unreal project without disturbing unrelated files.

**STEP 3**

Establish the folders, source structure, design constants, and asset pipeline.

**STEP 4**

Produce a small but coherent visual art bible containing:

- Palette
- Shape language
- Character proportions
- Material treatment
- Lighting direction
- UI style
- Animation principles
- Camera presentation rules

**STEP 5**

Create the first Blender asset-generation scripts.

Start by producing:

- Courtroom architectural foundation
- Judge bench
- Witness stand
- Defense desk
- Prosecutor desk
- Important room decorations

Do not stop after writing the scripts. Execute them and verify their generated output.

**STEP 6**

Export the assets and import them into Unreal.

Verify the mesh scale, orientation, materials, and collision.

**STEP 7**

Assemble the courtroom.

Add intentional lighting and working camera viewpoints.

**STEP 8**

Create the initial original character assets and their basic animation framework.

**STEP 9**

Implement the trial gameplay framework.

**STEP 10**

Build the Golden Gavel case and verify that a player can progress through it.

Continue through the remaining development phases as far as the available environment, time, and tools permit.

Do not pretend unfinished work is complete.

---

# FINAL DIRECTIVE

This project should not merely function.

**IT SHOULD FEEL LIKE A REAL GAME.**

I want to launch it and immediately see a funny, polished cartoon courtroom with original 3D characters, expressive animations, beautiful materials, dramatic cameras, entertaining dialogue, and actual interactive legal battles.

I want the prosecutor to look furious when I disprove his argument.

I want witnesses to panic when their lies are exposed.

I want the judge to slam an absurdly large gavel.

I want objections to feel powerful and hilarious.

I want a courtroom that looks handcrafted rather than procedurally abandoned.

I want the game to remain logically playable even when the characters behave like complete idiots.

Use Blender seriously.

Use Unreal Engine seriously.

Use code and automation intelligently.

Inspect what you create.

Test what you implement.

Fix what looks bad.

Improve what feels boring.

Avoid wasting effort on giant unfinished systems.

Prioritize a beautiful, working, entertaining vertical slice first, then expand it.

**DO NOT JUST TELL ME HOW YOU WOULD MAKE THE GAME.**

**ACTUALLY START BUILDING IT WITH THE AVAILABLE TOOLS.**

**MAKE COURTROOM CHAOS A REAL, PLAYABLE, VISUALLY APPEALING CARTOON COURTROOM GAME.**
