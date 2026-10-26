from PIL import Image,ImageDraw,ImageFont
from pathlib import Path
import random,math
ROOT=Path(__file__).resolve().parents[1]/'Art'/'UI';ROOT.mkdir(exist_ok=True)
INK='#202D3B';CREAM='#F9EFD9';GOLD='#EAC06A';RED='#A8394D';TEAL='#287C7D'
def font(size,bold=False):return ImageFont.truetype('C:/Windows/Fonts/'+('georgiab.ttf' if bold else 'bahnschrift.ttf'),size)
def panel(name,size,fill,outline=INK):
 w,h=size;im=Image.new('RGBA',(w*2,h*2));d=ImageDraw.Draw(im);d.rounded_rectangle((8,12,w*2-2,h*2-2),radius=25,fill=(8,16,26,100));d.rounded_rectangle((1,1,w*2-10,h*2-14),radius=24,fill=fill,outline=outline,width=4);im.resize((w,h),Image.Resampling.LANCZOS).save(ROOT/(name+'.png'))
panel('Dialogue',(1200,210),CREAM)
panel('InkButton',(400,64),INK,GOLD);panel('RedButton',(400,64),RED,INK);panel('TealButton',(400,64),TEAL,INK);panel('NameTab',(420,54),RED,INK);panel('EvidencePanel',(1200,500),CREAM)
im=Image.new('RGBA',(700,180));d=ImageDraw.Draw(im)
d.ellipse((10,20,145,155),fill=INK,outline=GOLD,width=4);d.line((50,115,108,57),fill=GOLD,width=14);d.rounded_rectangle((55,40,117,72),radius=7,fill=GOLD);d.line((45,132,115,132),fill=CREAM,width=8)
d.text((173,20),'COURTROOM',font=font(47,True),fill=CREAM,stroke_width=1)
d.text((170,69),'CHAOS',font=font(76,True),fill=GOLD,stroke_width=1)
d.text((177,151),'JUSTICE. WITH EXTRA MUSTARD.',font=font(15),fill=CREAM)
im.save(ROOT/'Logo.png')
for k in range(6):
 im=Image.new('RGBA',(360,280));d=ImageDraw.Draw(im);d.rounded_rectangle((4,4,355,275),22,fill='#E9D9B9',outline=INK,width=4)
 if k in [0,1]:
  if k==0:d.rectangle((24,24,336,240),fill='#526E83');d.rectangle((24,190,336,240),fill='#344657')
  d.rounded_rectangle((135,75,225,225),20,fill='#E8B640',outline=INK,width=5);d.polygon([(160,75),(165,34),(188,20),(193,75)],fill=GOLD,outline=INK);d.rounded_rectangle((145,130,215,175),5,fill=RED);d.text((155,140),'M',font=font(28,True),fill=CREAM)
 elif k in [2,3,4]:
  d.rounded_rectangle((92,30,270,246),8,fill=CREAM,outline=INK,width=5);d.rounded_rectangle((140,20,225,48),6,fill=TEAL)
  d.text((110,62),['','','WORK','LOG','CART'][k],font=font(26,True),fill=RED)
  for y in range(110,210,25):d.line((115,y,245,y),fill='#9C967F',width=4)
  d.ellipse((217,187,265,235),outline=RED,width=5)
 else:
  d.rectangle((28,25,332,237),fill='#526E83');d.rectangle((65,160,300,177),fill=TEAL);d.rectangle((80,177,92,234),fill=INK);d.rectangle((275,177,287,234),fill=INK);d.ellipse((75,228,99,252),fill=INK);d.ellipse((270,228,294,252),fill=INK);d.rectangle((150,117,288,157),fill=RED);d.line((170,135,250,88),fill=GOLD,width=12);d.rounded_rectangle((229,67,285,97),8,fill=GOLD,outline=INK,width=3)
 im.save(ROOT/('Evidence'+str(k)+'.png'))
print('UI_ART_OK')

# Original comic impact graphic.
im=Image.new('RGBA',(1200,350));d=ImageDraw.Draw(im);pts=[]
for i in range(40):
 a=math.pi*i/20;r=1 if i%2==0 else .84;pts.append((600+585*r*math.cos(a),175+170*r*math.sin(a)))
d.polygon(pts,fill=GOLD,outline=INK,width=8)
d.polygon([(95,85),(1090,55),(1065,268),(120,292)],fill=RED,outline=INK,width=7)
d.text((600,173),'OBJECTION!',font=font(135),anchor='mm',fill=CREAM,stroke_width=4,stroke_fill=INK)
im.save(ROOT/'Objection.png')
