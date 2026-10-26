"""Original, deterministic pizzicato courtroom underscore and interface tick."""
import math,wave,struct,os,random
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RATE=44100;beat=.48;duration=beat*32
samples=[0.0]*int(RATE*duration)
def note(midi,start,length,volume=.2,kind='keys'):
 hz=440*2**((midi-69)/12);begin=int(start*RATE);end=min(len(samples),int((start+length)*RATE))
 for i in range(begin,end):
  t=(i-begin)/RATE;envelope=min(1,t/.006)*math.exp(-t*(4.5 if kind=='keys' else 2.8))
  value=math.sin(2*math.pi*hz*t)+.24*math.sin(2*math.pi*hz*2*t)+.1*math.sin(2*math.pi*hz*3*t)
  samples[i]+=value*envelope*volume
# Eight original bars in a restrained playful minor progression.
chords=[(50,57,60,65),(50,57,60,64),(46,53,57,60),(45,52,57,61)]*2
melody=[74,77,76,72,74,69,72,71,70,74,77,74,73,69,68,69]
for bar,chord in enumerate(chords):
 for offset in [0,2]:note(chord[0]-12,(bar*4+offset)*beat,beat*1.7,.2,'bass')
 for offset in [1,3]:
  for pitch in chord[1:]:note(pitch,(bar*4+offset)*beat,beat*.9,.055)
 for k in range(2):note(melody[bar*2+k],(bar*4+k*2+.5)*beat,beat*.8,.075)
peak=max(1,max(abs(v) for v in samples))
def write(name,values):
 with wave.open(os.path.join(ROOT,'Art','Exports',name+'.wav'),'wb') as f:
  f.setparams((1,2,RATE,0,'NONE','not compressed'));f.writeframes(b''.join(struct.pack('<h',int(max(-1,min(1,v))*26000)) for v in values))
write('CourtroomShuffle',[v/peak for v in samples])
write('UITick',[.23*math.sin(2*math.pi*(650*t+700*t*t))*math.exp(-t*65) for t in (i/RATE for i in range(int(.08*RATE)))])
print('AUDIO_BUILD_OK',duration,'seconds')
