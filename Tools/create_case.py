"""Author the Golden Gavel case as an editable Unreal Data Asset."""
import unreal as u
assets=u.AssetToolsHelpers.get_asset_tools()
factory=u.DataAssetFactory();factory.set_editor_property('data_asset_class',u.ChaosCaseData)
case=u.load_asset('/Game/Cases/DA_GoldenGavel')
if not case:case=assets.create_asset('DA_GoldenGavel','/Game/Cases',u.ChaosCaseData,factory)
assert case
def line(who,text,emotion='Speaking'):return u.ChaosLine(speaker=who,text=text,emotion=emotion)
case.title='The Stolen Golden Gavel';case.subtitle='One missing gavel. One innocent hot dog man.'
case.consultation=[
 line('Benny','I delivered twelve hot dogs. Now I am accused of stealing the Golden Gavel. This is a terrible loyalty scheme.','Nervous'),
 line('Oliver','Start with the yellow object in the security photograph. What were you carrying?','Thinking'),
 line('Benny','My mustard dispenser. The nozzle jams unless you compliment it. Please defend my good taste.'),
 line('Oliver','A photograph, an inventory, and a maintenance report. Let us find a timeline that actually fits.','Thinking')]
case.opening=[
 line('Bumble','Court is in session. Please do not eat the evidence. That rule exists because of me.'),
 line('Victor','A golden object. A fleeing vendor. An exceptionally handsome prosecutor. The case is practically gift-wrapped.','Smug'),
 line('Oliver','One of those is an opinion. Another might be mustard. We will test the evidence.','Pointing'),
 line('Bumble','Call Milo Mopps. Maintenance has finally become dramatic.')]
evidence=[
 ('photo','Security photograph','PHOTOGRAPH','19:10. Benny leaves the courthouse carrying a shiny yellow object. The image is blurred.','Look at the top: a pointed nozzle. Look at the middle: a red M label. The ceremonial gavel has neither.',0,None),
 ('mustard','Mustard dispenser','OBJECT','Benny\'s oversized golden-yellow dispenser. He uses it on his hot dog deliveries.','A pointed nozzle and a red M label match the security image. The object in Benny\'s hand was a condiment dispenser.',0,'Mustard'),
 ('maintenance','Maintenance report','DOCUMENT','18:00. Cleaning of the ceremonial bench. Display objects must be moved before work begins.','The instruction is explicit: ALL DISPLAY OBJECTS MUST BE RELOCATED. The bench was cleared well before Benny arrived at 19:10.',0,None),
 ('inventory','Inventory sheet','DOCUMENT','17:45: Golden Gavel checked on the bench. 20:00: reported missing.','There was no inventory check at 19:10. This sheet establishes a gap, not the time of a theft.',0,None),
 ('cart','Cart transfer record','DOCUMENT','18:05. Officer Brick moved ceremonial objects to storage B on cart 04.','The contents include a velvet-lined gavel case. Brick recorded the move before Benny entered the courthouse.',1,None),
 ('storage','Storage photograph','PHOTOGRAPH','20:15. Storage B, cart 04. Several relocated courtroom objects are visible.','Behind the bucket is the Golden Gavel in its velvet-lined case. Its location matches Brick\'s transfer record. Nothing was stolen.',2,'GoldenGavel')]
items=[]
for i,(id,title,category,description,inspection,unlock,mesh) in enumerate(evidence):
 items.append(u.ChaosEvidence(id=id,title=title,category=category,description=description,inspection=inspection,unlock_stage=unlock,illustration=u.load_asset('/Game/UI/Evidence'+str(i)),exhibit=u.load_asset('/Game/Evidence/'+mesh) if mesh else None))
case.evidence=items
def statement(text,press,emotion='Speaking'):return u.ChaosStatement(text=text,press=press,emotion=emotion)
case.stages=[
 u.ChaosStage(title='A suspicious yellow object',speaker='Milo',contradiction=0,evidence='mustard',statements=[
  statement('I saw Benny leave at 19:10 carrying the Golden Gavel.','MILO: I saw yellow. I inferred justice. A nozzle? I thought that was decorative.'),
  statement('The security photograph proves it was a gavel.','VICTOR: A photograph cannot lie. OLIVER: It can be blurry.'),
  statement('I remember everything. Except small details. And Tuesdays.','MILO: Please do not ask me what day it is.','Confused')],resolution=[
  line('Oliver','The nozzle and the red label match Benny\'s mustard bottle. A shiny object is not automatically a gavel.','Pointing'),
  line('Bumble','Mustard. Compelling evidence. Disappointing snack.'),
  line('Victor','The gavel was still missing. Ask the witness about the bench.','Angry')]),
 u.ChaosStage(title='The missing hours',speaker='Milo',contradiction=1,evidence='maintenance',statements=[
  statement('The gavel was on the bench until Benny arrived at 19:10.','MILO: I did not check it at 19:10. The inventory lists the actual check times.','Nervous'),
  statement('Nobody moved any ceremonial objects that evening.','MILO: Brick handled a cart before dinner. I suppose that is a form of moving.','Nervous'),
  statement('The room was being cleaned. That is entirely unrelated.','MILO: Cleaning started at 18:00. We cleared the whole bench. Oh.','Confused')],resolution=[
  line('Oliver','The maintenance report ordered every display object moved at 18:00. That was seventy minutes before Benny arrived.','Pointing'),
  line('Brick','Cart 04. Storage B. 18:05. I wrote it down. With a pen.'),
  line('Bumble','Enter the transfer record. Officer Brick, please obtain a photograph of storage B.'),
  line('Brick','Already obtained. I also obtained the gavel. It was behind a bucket.')]),
 u.ChaosStage(title='Where the gavel went',speaker='Victor',contradiction=0,evidence='storage',statements=[
  statement('Even if it was moved, the gavel never reached storage.','VICTOR: A bucket proves nothing. OLIVER: We are interested in what is behind it.','Angry'),
  statement('Cart 04 carried nothing except cleaning supplies.','BRICK: The transfer record lists a velvet-lined gavel case. It is not a mop.','Frustrated'),
  statement('The defendant must have stolen it. My hair says so.','BUMBLE: The court requests evidence with less hair product.','Angry')],resolution=[
  line('Oliver','There it is: the Golden Gavel, in the case on cart 04. The storage photograph matches the transfer record.','Pointing'),
  line('Victor','I would like the record to show that my hair was operating with incomplete information.','Embarrassed'),
  line('Bumble','Counsel, give the court one explanation that accounts for every established fact.')])]
case.closing_prompt='What actually happened to the Golden Gavel? Your conclusion must fit the object, the times, and the storage record.'
case.conclusions=['Cleaning moved the gavel to storage before Benny arrived. No theft occurred.','Benny stole the gavel and transformed it into mustard.','Officer Brick stole it and framed the bucket.']
case.correct_conclusion=0
case.verdict=[
 line('Bumble','The timeline is clear. Maintenance moved the gavel to storage. Benny carried his own mustard bottle.'),
 line('Bumble','On the charge of stealing the Golden Gavel: NOT GUILTY!','Happy'),
 line('Benny','Free mustard for everyone! Except the prosecutor. He gets a receipt.','Happy'),
 line('Victor','I intend to appeal the condiment.','Embarrassed'),
 line('Oliver','Justice served. Probably. And without a single hot dog being called to testify.','Happy'),
 line('Bumble','Court is adjourned. Somebody please label the mustard. And the bucket.')]
u.EditorAssetLibrary.save_loaded_asset(case);u.log('CASE_DATA_CREATED')
