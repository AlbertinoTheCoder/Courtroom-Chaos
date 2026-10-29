"""Bake distinct Kokoro character voices and amplitude tracks. No online inference."""
from pathlib import Path
import ast,hashlib,json,re,time,argparse
import numpy as np
import soundfile as sf
import onnxruntime as ort
from kokoro_onnx import Kokoro
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'Art'/'Voices';OUT.mkdir(parents=True,exist_ok=True)
PROFILES={
 'Oliver':dict(voice='bm_george',speed=1.04,lang='en-gb',direction='Dry, nimble British defense attorney'),
 'Victor':dict(voice='bm_fable',speed=.95,lang='en-gb',direction='Theatrical, self-important prosecutor'),
 'Bumble':dict(voice='am_santa',speed=.94,lang='en-us',direction='Warm, weighty, slightly bewildered judge'),
 'Benny':dict(voice='am_fenrir',speed=1.08,lang='en-us',direction='Earnest, energetic American vendor'),
 'Milo':dict(voice='am_puck',speed=1.03,lang='en-us',direction='Fussy, uncertain witness'),
 'Brick':dict(voice='am_adam',speed=.92,lang='en-us',direction='Slow, matter-of-fact bailiff')}
ALIASES={k.upper():k for k in PROFILES}
seq={}
PROFILE_OVERRIDES={}
def split_roles(who,text):
 parts=re.split(r'\b(OLIVER|VICTOR|BUMBLE|BENNY|MILO|BRICK):\s*',text)
 if len(parts)==1:return [(who,text.strip())]
 out=[]
 if parts[0].strip():out.append((who,parts[0].strip()))
 for i in range(1,len(parts),2):out.append((ALIASES[parts[i]],parts[i+1].strip()))
 return out
def add(who,text):
 seq[who+'|'+text]=split_roles(who,text)
tree=ast.parse((ROOT/'Tools/create_case.py').read_text())
for node in ast.walk(tree):
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Name) and node.func.id=='line' and len(node.args)>=2:
  if all(isinstance(a,ast.Constant) for a in node.args[:2]):add(node.args[0].value,node.args[1].value)
 if isinstance(node,ast.Call) and isinstance(node.func,ast.Attribute) and node.func.attr=='ChaosStage':
  fields={k.arg:k.value for k in node.keywords};who=ast.literal_eval(fields['speaker'])
  for call in fields['statements'].elts:add(who,ast.literal_eval(call.args[0]));add('Feedback',ast.literal_eval(call.args[1]))
 if isinstance(node,ast.Assign):
  for target in node.targets:
   if isinstance(target,ast.Attribute) and target.attr=='closing_prompt':add('Oliver',ast.literal_eval(node.value))
for path in sorted((ROOT/'Art'/'Cases').glob('*.json')):
 data=json.loads(path.read_text(encoding='utf-8'))
 for section in ['consultation','opening','verdict']:
  for entry in data[section]:add(entry['speaker'],entry['text'])
 for stage in data['stages']:
  for entry in stage['statements']:add(stage['speaker'],entry['text']);add('Feedback',entry['press'])
  for entry in stage['resolution']:add(entry['speaker'],entry['text'])
 add('Oliver',data['closing_prompt'])
 # Voice identity follows the case's client/witness appearance, including feedback speakers.
 texts=[]
 for section in ['consultation','opening','verdict']:texts.extend((l['speaker'],l['text']) for l in data[section])
 for stage in data['stages']:
  texts.extend((stage['speaker'],l['text']) for l in stage['statements'])
  for l in stage['statements']:texts.extend(split_roles('Feedback',l['press']))
  texts.extend((l['speaker'],l['text']) for l in stage['resolution'])
 for who,words in texts:
  if who in data.get('voice_profiles',{}):PROFILE_OVERRIDES[(who,words)]=data['voice_profiles'][who]

# Fixed feedback authored in the runtime, including wrong choices.
source=(ROOT/'Source/CourtSimulator/ChaosGame.cpp').read_text()
for raw in re.findall(r'TEXT\("((?:[^"\\]|\\.)*)"\)',source):
 if raw.startswith('BUMBLE: '):add('Feedback',ast.literal_eval('"'+raw+'"'))
add('Oliver','Objection!')

def spoken(text):
 for clock,words in {'19:10':'seven ten p.m.','18:00':'six p.m.','17:45':'five forty five p.m.','18:05':'six oh five p.m.','20:00':'eight p.m.','20:15':'eight fifteen p.m.'}.items():text=text.replace(clock,words)
 text=text.replace('04','zero four').replace('p.m..','p.m.');return text

def clip_id(who,text):return 'VO_'+who+'_'+hashlib.sha1(text.encode()).hexdigest()[:12]
parser=argparse.ArgumentParser();parser.add_argument('--preview',action='store_true');args=parser.parse_args()
if args.preview:
 seq={who+'|'+text:[(who,text)] for who,text in {
  'Oliver':'One of those is an opinion. Another might be mustard.',
  'Victor':'An exceptionally handsome prosecutor. The case is practically gift wrapped!',
  'Bumble':'Court is in session. Please do not eat the evidence.',
  'Benny':'My mustard dispenser. Please defend my good taste!',
  'Milo':'I saw yellow. I inferred justice.',
  'Brick':'I wrote it down. With a pen.'}.items()}
options=ort.SessionOptions();options.intra_op_num_threads=4;options.inter_op_num_threads=1
session=ort.InferenceSession(str(ROOT/'Saved/TTS/models/kokoro-v1.0.onnx'),sess_options=options,providers=['CPUExecutionProvider'])
kokoro=Kokoro.from_session(session,str(ROOT/'Saved/TTS/models/voices-v1.0.bin'))
clips={};sequences={};started=time.time()
for index,(key,takes) in enumerate(seq.items()):
 ids=[]
 for who,text in takes:
  assert who in PROFILES,(who,text)
  name=clip_id(who,text);ids.append(name)
  if name in clips:continue
  base_profile=PROFILE_OVERRIDES.get((who,text),PROFILES[who]);variants={}
  for pace,factor in [('Normal',1),('Relaxed',.80),('Quick',1.23)]:
   profile=dict(base_profile);profile['speed']=base_profile['speed']*factor
   variant_name=name if pace=='Normal' else name+'_'+pace
   destination=OUT/(variant_name+'.wav');signature=hashlib.sha256(json.dumps([profile,spoken(text),'master-v1']).encode()).hexdigest()
   metadata=destination.with_suffix('.json')
   if destination.exists() and metadata.exists() and json.loads(metadata.read_text()).get('signature')==signature:
    item=json.loads(metadata.read_text())
   else:
    audio,rate=kokoro.create(spoken(text),voice=profile['voice'],speed=profile['speed'],lang=profile['lang'])
    audio=np.asarray(audio,dtype=np.float32)
    # Trim excessive padding, retain breaths, and add short click-free lead/tail silence.
    active=np.flatnonzero(np.abs(audio)>.006)
    assert len(active)>rate*.08,(who,text,'silent speech')
    audio=audio[max(0,active[0]-int(rate*.045)):min(len(audio),active[-1]+int(rate*.09))]
    audio-=float(np.mean(audio));peak=float(np.max(np.abs(audio)));audio*=min(2.5,.78/max(.01,peak))
    fade=min(240,len(audio)//10);audio[:fade]*=np.linspace(0,1,fade);audio[-fade:]*=np.linspace(1,0,fade)
    audio=np.concatenate((np.zeros(int(rate*.045),dtype=np.float32),audio,np.zeros(int(rate*.10),dtype=np.float32)))
    sf.write(destination,audio,rate,subtype='PCM_16')
    hop=rate//40;padded=np.pad(audio,(0,(-len(audio))%hop));rms=np.sqrt(np.mean(padded.reshape(-1,hop)**2,axis=1));reference=max(.04,float(np.percentile(rms,88)))
    envelope=np.where(rms<.008,0,np.clip((rms/reference)**.7,0,1))
    item=dict(id=name,speaker=who,text=text,spoken=spoken(text),voice=profile['voice'],speed=profile['speed'],file=str(destination.relative_to(ROOT)).replace('\\','/'),duration=len(audio)/rate,sample_rate=rate,envelope_hz=40,envelope=[round(float(v),4) for v in envelope],peak=round(float(np.max(np.abs(audio))),4),signature=signature)
    metadata.write_text(json.dumps(item,indent=2))
   assert .15<item['duration']<40 and item['peak']>.05,(name,item['duration'])
   variants[pace]=item
  item=dict(variants['Normal']);item['variants']={k:v for k,v in variants.items() if k!='Normal'};clips[name]=item
 sequences[key]=ids
 print(f'VOICE {index+1}/{len(seq)}: {key[:75]}',flush=True)
manifest=dict(engine='Kokoro-82M v1.0 / kokoro-onnx 0.6.1',model_license='Apache-2.0',profiles=PROFILES,clips=clips,sequences=sequences,envelope_hz=40)
if not args.preview:
 (ROOT/'Art/VoiceManifest.json').write_text(json.dumps(manifest,indent=2))
 objection=clips[clip_id('Oliver','Objection!')]
 import shutil;shutil.copyfile(ROOT/objection['file'],ROOT/'Art/Exports/Objection.wav')
else:(ROOT/'Saved/VoicePreviewManifest.json').write_text(json.dumps(manifest,indent=2))
print('VOICE_BUILD_OK',len(clips),'clips',round(sum(v['duration'] for v in clips.values()),1),'seconds;',round(time.time()-started,1),'seconds generation',flush=True)
