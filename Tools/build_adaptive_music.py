"""Three synchronized additions to the original 125-BPM courtroom loop."""
import math,random,struct,wave,json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];RATE=44100;BEAT=.48;DURATION=BEAT*32;N=round(RATE*DURATION)
CHORDS=[(50,57,60,65),(50,57,60,64),(46,53,57,60),(45,52,57,61)]*2
rng=random.Random(62041)

def tone(buf,midi,at,length,gain,kind):
 f=440*2**((midi-69)/12);begin=round(at*RATE)
 for i in range(round(length*RATE)):
  t=i/RATE;attack=min(1,t/.006);tail=min(1,(length-t)/.025)
  phase=2*math.pi*f*t
  if kind=='string':v=math.sin(phase)+.35*math.sin(phase*2)+.16*math.sin(phase*3);env=math.exp(-t*13)
  elif kind=='brass':v=math.sin(phase+.35*math.sin(2*math.pi*5*t))+.42*math.sin(phase*2)+.16*math.sin(phase*3);env=.65+.35*math.exp(-20*t)
  else:v=math.sin(phase)+.45*math.sin(phase*2.76);env=math.exp(-t*22)
  buf[(begin+i)%N]+=v*attack*tail*env*gain

def drum(buf,at,gain,kind):
 length={'kick':.20,'snare':.13,'hat':.045,'tom':.16,'cymbal':.7}[kind];begin=round(at*RATE);previous=0
 for i in range(round(length*RATE)):
  t=i/RATE;noise=rng.uniform(-1,1);high=noise-previous;previous=noise
  if kind=='kick':v=math.sin(2*math.pi*(62*t+2*(1-math.exp(-30*t))))*math.exp(-24*t)
  elif kind=='snare':v=(.65*noise+.3*math.sin(2*math.pi*180*t))*math.exp(-32*t)
  elif kind=='tom':v=math.sin(2*math.pi*(120*t+1-math.exp(-12*t)))*math.exp(-21*t)
  else:v=high*.5*math.exp(-t*(65 if kind=='hat' else 7))
  buf[(begin+i)%N]+=v*min(1,t/.002)*min(1,(length-t)/.008)*gain

report={}
for layer in ['CourtroomTension','CourtroomChaos','CourtroomMayhem']:
 buf=[0.0]*N
 for bar,chord in enumerate(CHORDS):
  start=bar*4
  if layer=='CourtroomTension':
   for k in range(8):tone(buf,chord[1+k%3]+12,(start+k*.5)*BEAT,.18,.115 if k%2==0 else .075,'string')
   for k in [1,3]:tone(buf,chord[0],(start+k)*BEAT,.26,.075,'wood')
  elif layer=='CourtroomChaos':
   for k in range(16):tone(buf,chord[(k+bar)%4]+12,(start+k*.25)*BEAT,.10,.055 if k%4 else .08,'wood')
   for k in [0,2]:drum(buf,(start+k)*BEAT,.17,'kick')
   for k in [1,3]:drum(buf,(start+k)*BEAT,.13,'snare')
   for k in range(8):drum(buf,(start+k*.5)*BEAT,.045,'hat')
  else:
   for k in [1.5,3.5]:
    for pitch in [chord[1],chord[2]+12]:tone(buf,pitch,(start+k)*BEAT,.24,.095,'brass')
   for k in range(4):tone(buf,chord[3]+12+(1 if k%2 else 0),(start+2+k*.5)*BEAT,.12,.055,'string')
   if bar%2:
    for k in range(6):drum(buf,(start+2.5+k*.25)*BEAT,.085,'tom')
   else:drum(buf,start*BEAT,.085,'cymbal')
 peak=max(abs(v) for v in buf);gain=min(2,.68/max(.01,peak));pcm=[max(-.95,min(.95,v*gain)) for v in buf]
 with wave.open(str(ROOT/'Art/Exports'/(layer+'.wav')),'wb') as f:f.setparams((1,2,RATE,0,'NONE','not compressed'));f.writeframes(b''.join(struct.pack('<h',round(v*32767)) for v in pcm))
 report[layer]=dict(samples=N,sample_rate=RATE,duration=DURATION,peak=max(abs(v) for v in pcm),bpm=125)
 print('MUSIC_LAYER_OK',layer,flush=True)
(ROOT/'Art/MusicManifest.json').write_text(json.dumps(report,indent=2))
