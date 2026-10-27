"""Legible case-specific evidence plates; every printed fact matches its case source."""
import json,math,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'Art'/'UI'
INK='#202D3B';CREAM='#F9EFD9';GOLD='#EAC06A';RED='#A8394D';TEAL='#287C7D'
def font(size,bold=False):return ImageFont.truetype('C:/Windows/Fonts/'+('georgiab.ttf' if bold else 'bahnschrift.ttf'),size)
def text(d,xy,value,size=32,fill=INK,bold=False,width=51):
 x,y=xy
 for row in textwrap.wrap(value,width=width):d.text((x,y),row,font=font(size,bold),fill=fill);y+=int(size*1.3)
 return y
def battery(d,box):
 x,y=box;d.rounded_rectangle((x,y+70,x+550,y+250),20,fill=TEAL,outline=INK,width=6)
 d.rounded_rectangle((x-20,y+20,x+570,y+90),16,fill=GOLD,outline=INK,width=6)
 d.ellipse((x+160,y+28,x+390,y+73),fill=INK)
 d.text((x+275,y+170),'48 V BATTERY',font=font(38),fill=CREAM,anchor='mm')
 d.line((x+600,y+20,x+660,y+20),fill=INK,width=6);d.rectangle((x+600,y-5,x+665,y+60),outline=INK,width=5)
 d.text((x+632,y+105),'EMPTY',font=font(24),fill=RED,anchor='mm')
def envelope(d,box):
 x,y=box;d.rounded_rectangle((x,y,x+560,y+270),15,fill='#FFFAEB',outline=INK,width=6)
 d.line((x,y,x+280,y+160,x+560,y),fill='#B0A38B',width=5)
 d.ellipse((x+225,y+105,x+335,y+215),fill=TEAL,outline=GOLD,width=5)
 d.text((x+280,y+160),'C17',font=font(38,True),fill=CREAM,anchor='mm')
for path in sorted((ROOT/'Art'/'Cases').glob('*.json')):
 c=json.loads(path.read_text(encoding='utf-8'))
 for i,e in enumerate(c['evidence']):
  im=Image.new('RGBA',(1536,1080),CREAM);d=ImageDraw.Draw(im);d.rounded_rectangle((14,14,1522,1066),28,outline=INK,width=8)
  d.rectangle((45,45,1491,190),fill=TEAL if c['number']==3 else RED)
  text(d,(85,78),e['title'].upper(),52,CREAM,True,40)
  d.text((85,218),f"CASE {c['number']:03d} / EXHIBIT {i+1:02d} / {e['category']}",font=font(27),fill=RED)
  diagram=e.get('diagram');y=310
  if diagram=='battery':battery(d,(330,290));y=620
  elif diagram=='envelope':
   d.rounded_rectangle((440,275,1090,600),16,fill='#D4E5DF',outline=INK,width=7);envelope(d,(480,300))
   d.line((450,280,1080,280,1080,590,450,590,450,280),fill='#879D9B',width=7)
   d.line((460,285,495,285,1060,575),fill='#F7FFFF',width=4)
   d.rectangle((420,590,1110,615),fill=INK);d.text((130,390),'16:35',font=font(64,True),fill=RED);y=660
  elif diagram=='circuit':
   for x,label,watts in [(100,'URN','1,500 W'),(800,'RISER','1,200 W')]:
    d.rounded_rectangle((x,305,x+500,480),20,fill=INK);d.text((x+250,350),label,font=font(38),fill=CREAM,anchor='mm');d.text((x+250,410),watts,font=font(48,True),fill=GOLD,anchor='mm')
   d.line((350,480,350,535,1050,535,1050,480),fill=RED,width=9);d.text((700,580),'SHARED CIRCUIT / LIMIT 2,300 W',font=font(35),fill=RED,anchor='mm');y=650
  for row in e['rows']:
   d.line((85,y+69,1440,y+69),fill='#D1C2A4',width=2);text(d,(85,y),row,35,INK,False,65);y+=92 if not diagram else 78
  d.text((85,1015),'ORIGINAL RECORD / ENTERED IN EVIDENCE',font=font(24),fill=TEAL)
  im.save(OUT/(f"{c['id']}_Evidence{i}.png"))
 im=Image.new('RGBA',(1050,600),INK);d=ImageDraw.Draw(im);d.rounded_rectangle((10,10,1040,590),35,outline=GOLD,width=9)
 d.text((55,45),f"CASE {c['number']:03d}",font=font(37),fill=GOLD)
 if c['number']==2:battery(d,(230,180))
 else:envelope(d,(245,160))
 text(d,(55,475),c['title'].upper(),46,CREAM,True,32)
 im.save(OUT/('Poster_Blackout.png' if c['number']==2 else 'Poster_Charity.png'))
for name,fill in [('LifeHeart',RED),('LifeEmpty',INK)]:
 im=Image.new('RGBA',(160,160));d=ImageDraw.Draw(im);p=[]
 for i in range(180):
  t=i*2*math.pi/180;x=16*math.sin(t)**3;y=13*math.cos(t)-5*math.cos(2*t)-2*math.cos(3*t)-math.cos(4*t);p.append((80+x*4,78-y*4))
 d.polygon(p,fill=fill,outline=GOLD,width=5);im.save(OUT/(name+'.png'))
print('CASE_CARDS_OK')
