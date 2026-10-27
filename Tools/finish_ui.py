"""High-resolution authored evidence boards, results stamps, and impact graphics."""
from PIL import Image,ImageDraw,ImageFont,ImageFilter
from pathlib import Path
import math,random
ROOT=Path(__file__).resolve().parents[1]/'Art'/'UI'
INK='#202D3B';CREAM='#F9EFD9';GOLD='#EAC06A';RED='#A8394D';TEAL='#287C7D'
def font(s,b=False):return ImageFont.truetype('C:/Windows/Fonts/'+('georgiab.ttf' if b else 'bahnschrift.ttf'),s)
def card():
 im=Image.new('RGBA',(1024,720),CREAM);d=ImageDraw.Draw(im);d.rounded_rectangle((8,8,1015,711),24,outline=INK,width=7);return im,d
def mustard(d,x,y,s=1):
 def r(p):return tuple(int(v*s+(x if i%2==0 else y)) for i,v in enumerate(p))
 d.rounded_rectangle(r((0,0,115,190)),int(22*s),fill=GOLD,outline=INK,width=max(2,int(4*s)));d.polygon([r((28,0)),r((42,-68)),r((65,-86)),r((76,0))],fill=GOLD,outline=INK);d.rounded_rectangle(r((13,75,102,135)),int(8*s),fill=RED);d.text(r((57,103)),'M',font=font(int(47*s),True),anchor='mm',fill=CREAM)
def gavel(d,x,y,s=1):
 d.line((x,y,x+int(95*s),y-int(86*s)),fill=GOLD,width=int(18*s));d.rounded_rectangle((x+int(55*s),y-int(118*s),x+int(150*s),y-int(75*s)),int(8*s),fill=GOLD,outline=INK,width=3)
im,d=card();d.rectangle((40,42,984,610),fill='#506779')
for x in [90,710]:d.rectangle((x,50,x+160,520),fill='#384D61');d.rectangle((x+12,60,x+148,505),outline='#D9D9BA',width=5)
d.rectangle((40,520,984,610),fill='#263B4E');d.ellipse((260,145,470,345),fill='#D5B298',outline=INK,width=5);d.rounded_rectangle((260,325,485,605),40,fill='#925461',outline=INK,width=5);d.rounded_rectangle((240,138,490,195),18,fill=RED);d.line((475,395,615,420),fill='#D5B298',width=45);mustard(d,625,335,.8)
d.text((70,78),'COURTHOUSE / EXIT 02',font=font(26),fill=CREAM);d.text((70,550),'19:10:07    CAM 02',font=font(35),fill=CREAM);d.text((512,658),'SECURITY PHOTOGRAPH',font=font(37,True),anchor='mm',fill=INK);im.save(ROOT/'Evidence0.png')
im,d=card();mustard(d,360,180,2.1);d.text((512,75),'BENNY\'S MUSTARD',font=font(43,True),anchor='mm',fill=INK);d.text((512,652),'POINTED NOZZLE / RED M LABEL',font=font(30),anchor='mm',fill=RED);im.save(ROOT/'Evidence1.png')
docs=[('MAINTENANCE','18:00 / BEFORE PUBLIC CEREMONY',['CLEAR THE CEREMONIAL BENCH','Relocate ALL display objects before cleaning.','Responsible officer: Brick','Signed: Milo Mopps']),('INVENTORY','CEREMONIAL GOLDEN GAVEL',['17:45    PRESENT / bench','19:10    NO CHECK RECORDED','20:00    REPORTED MISSING','Prepared for the public ceremony']),('CART TRANSFER','18:05 / CART 04 / STORAGE B',['Ceremonial display objects','One velvet-lined gavel case','Destination: STORAGE B','Moved by: OFFICER BRICK'])]
for i,(title,sub,rows) in enumerate(docs,2):
 im,d=card();d.rounded_rectangle((60,55,960,665),12,fill='#FFFAEB',outline='#AA987B',width=3);d.rectangle((70,65,950,160),fill=TEAL);d.text((510,110),title,font=font(45,True),anchor='mm',fill=CREAM);d.text((110,205),sub,font=font(27),fill=RED)
 for j,row in enumerate(rows):
  y=285+j*74;d.line((110,y+49,910,y+49),fill='#D1C2A4',width=2);d.text((110,y),row,font=font(28),fill=INK)
 d.ellipse((805,535,925,655),outline=RED,width=6);d.text((865,595),'FILED',font=font(24,True),anchor='mm',fill=RED);im.save(ROOT/('Evidence'+str(i)+'.png'))
im,d=card();d.rectangle((40,40,984,608),fill='#4C6774')
for x in [80,420,800]:d.rectangle((x,80,x+100,450),fill='#34505F');d.line((x,180,x+100,180),fill=GOLD,width=7)
d.rounded_rectangle((180,340,860,375),10,fill=TEAL,outline=INK,width=5);d.rectangle((210,370,232,555),fill=INK);d.rectangle((805,370,827,555),fill=INK);d.ellipse((192,540,250,598),fill=INK);d.ellipse((787,540,845,598),fill=INK);d.rounded_rectangle((440,250,800,335),12,fill=RED,outline=INK,width=5);gavel(d,510,290,1.4)
d.polygon([(240,180),(370,180),(394,334),(218,334)],fill='#B2C9C3',outline=INK);d.arc((235,137,375,270),180,360,fill=GOLD,width=9);d.text((70,70),'STORAGE B / CART 04',font=font(30),fill=CREAM);d.text((512,658),'20:15 / STORAGE PHOTOGRAPH',font=font(35,True),anchor='mm',fill=INK);im.save(ROOT/'Evidence5.png')
im=Image.new('RGBA',(1200,320));d=ImageDraw.Draw(im);points=[]
for i in range(32):
 a=i*math.pi/16;r=1 if i%2==0 else .85;points.append((600+590*r*math.cos(a),160+150*r*math.sin(a)))
d.polygon(points,fill=GOLD,outline=INK,width=7);d.polygon([(90,65),(1105,37),(1080,250),(110,282)],fill=TEAL,outline=INK,width=7);d.text((600,157),'NOT GUILTY!',font=font(133,True),anchor='mm',fill=CREAM,stroke_width=2,stroke_fill=INK);im.save(ROOT/'Verdict.png')
for i,label in enumerate(['OBJECTION','SHARP EYE','STEADY','MENACE']):
 im=Image.new('RGBA',(160,160));d=ImageDraw.Draw(im);d.ellipse((7,7,153,153),fill=GOLD,outline=INK,width=6);d.ellipse((20,20,140,140),fill=TEAL if i%2 else RED);gavel(d,51,95,.42);d.text((80,126),label,font=font(15,True),anchor='mm',fill=CREAM);im.save(ROOT/('Badge'+str(i)+'.png'))
im=Image.new('RGBA',(130,170));d=ImageDraw.Draw(im);d.rounded_rectangle((5,5,125,165),9,fill=CREAM,outline=INK,width=4)
for y in range(35,140,19):d.line((23,y,106,y),fill='#A39880',width=3)
im.save(ROOT/'Paper.png')
im=Image.new('RGBA',(400,140));d=ImageDraw.Draw(im)
for x,y,r in [(60,80,40),(135,65,55),(215,75,54),(295,70,50),(350,90,34)]:d.ellipse((x-r,y-r,x+r,y+r),fill=(235,211,163,120))
im=im.filter(ImageFilter.GaussianBlur(13));im.save(ROOT/'Dust.png')
im,d=card();d.rectangle((20,20,1004,700),fill=INK);d.ellipse((300,70,720,490),fill=TEAL,outline=GOLD,width=12);gavel(d,410,365,2);d.text((512,570),'THE STOLEN GOLDEN GAVEL',font=font(44,True),anchor='mm',fill=CREAM);d.text((512,640),'A CASE OF MISTAKEN CONDIMENT',font=font(26),anchor='mm',fill=GOLD);im.save(ROOT/'CasePoster.png')
print('FINISH_UI_OK')
