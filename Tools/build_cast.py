"""Second-pass character silhouettes, layered tailoring and integrated facial features."""
import bpy,math,os
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
exec(compile(open(os.path.join(ROOT,'Tools','build_art.py')).read().split("box('Foundation'")[0],__file__,'exec'))
def form(name,profile,mat):
 verts=[];faces=[];N=32
 for z,w,d in profile:
  for i in range(N):
   t=2*math.pi*i/N;verts.append((w*math.cos(t),d*math.sin(t),z))
 for j in range(len(profile)-1):
  for i in range(N):a=j*N+i;b=j*N+(i+1)%N;faces.append((a,b,b+N,a+N))
 faces.extend([tuple(reversed(range(N))),tuple((len(profile)-1)*N+i for i in range(N))])
 me=bpy.data.meshes.new(name);me.from_pydata(verts,[],faces);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);me.materials.append(mats[mat])
 for f in me.polygons:f.use_smooth=True
 sub=o.modifiers.new('Sculpted contour','SUBSURF');sub.levels=2;return o
def patch(name,points,mat):
 me=bpy.data.meshes.new(name);me.from_pydata(points,[],[tuple(range(len(points)))]);me.update();o=bpy.data.objects.new(name,me);scene.collection.objects.link(o);me.materials.append(mats[mat]);sol=o.modifiers.new('Tailoring thickness','SOLIDIFY');sol.thickness=.025;bev=o.modifiers.new('Soft seam','BEVEL');bev.width=.012;bev.segments=3;return o
def capsule(name,a,b,r,mat):
 rod(name,a,b,r,mat);ball(name+' shoulder',a,(r,r,r),mat);ball(name+' joint',b,(r,r,r),mat)
def make(name,color,w,headwidth,role):
 before=set(scene.objects)
 form('Tailored silhouette',[(.68,w*.58,.19),(.75,w*.8,.24),(1.1,w*.87,.25),(1.42,w,.28),(1.56,w*.82,.24),(1.6,w*.46,.19)],color)
 rod('Neck',(0,0,1.53),(0,0,1.77),.12,'skin')
 for side in [-1,1]:
  capsule('Trouser leg',(side*.18,0,.76),(side*.21,0,.22),.145,color)
  box('Shoe sole',(side*.21,-.1,.08),(.32,.5,.09),'ink',.04);ball('Polished shoe',(side*.21,-.12,.17),(.16,.26,.13),'hair')
  a=(side*w*.82,0,1.43);b=(side*(w+.1),-.025,1.12);c=(side*(w+.08),-.12,.94)
  capsule('Upper sleeve',a,b,.135,color);capsule('Forearm',b,c,.12,color)
  box('Shirt cuff',(c[0],c[1],.98),(.22,.22,.1),'cream',.035)
  ball('Palm',(c[0],c[1],.87),(.13,.10,.15),'white' if role=='prosecutor' else 'skin')
  for f in range(3):capsule('Finger',(c[0]-.075+f*.065,c[1]-.045,.85),(c[0]-.075+f*.065,c[1]-.06,.73+f*.015),.034,'white' if role=='prosecutor' else 'skin')
  ball('Thumb',(c[0]-side*.115,c[1]-.05,.88),(.055,.06,.09),'skin')
 patch('Shirt front',[(-.17,-.265,1.56),(.17,-.265,1.56),(.12,-.283,1.13),(-.12,-.283,1.13)],'cream')
 for s in [-1,1]:
  patch('Notched lapel',[(s*.14,-.285,1.57),(s*.33,-.27,1.47),(s*.19,-.302,1.33),(s*.27,-.3,1.28),(s*.07,-.32,1.05)],color)
  patch('Collar',[(0,-.29,1.53),(s*.17,-.29,1.58),(s*.18,-.31,1.4),(s*.07,-.32,1.43)],'white')
 ball('Tie knot',(0,-.34,1.46),(.055,.035,.06),'red' if name=='Oliver' else 'gold')
 patch('Silk tie',[(-.035,-.337,1.43),(.035,-.337,1.43),(.065,-.35,1.14),(0,-.36,1.08),(-.065,-.35,1.14)],'red' if name=='Oliver' else 'gold')
 for z in [.91,1.04]:ball('Brass button',(.08,-.26,z),(.025,.018,.025),'gold')
 hw=headwidth
 form('Sculpted face',[(1.65,hw*.43,.15),(1.69,hw*.72,.22),(1.79,hw*.96,.285),(1.98,hw,.305),(2.17,hw*.94,.28),(2.33,hw*.78,.23),(2.4,hw*.25,.08)],'skin')
 for side in [-1,1]:
  ball('Ear',(side*hw*.98,.01,1.99),(.08,.08,.13),'skin');ball('Ear inner',(side*hw*1.02,-.055,1.99),(.045,.025,.075),'skin')
  x=side*.135
  ball('Lid surround',(x,-.27,2.09),(.12,.085,.135),'skin')
  ball('Eye white',(x,-.319,2.09),(.092,.048,.105),'white');ball('Iris',(x+side*.006,-.36,2.085),(.047,.025,.064),'blue');ball('Pupil',(x+side*.006,-.38,2.085),(.025,.012,.044),'ink');ball('Catchlight',(x-.013,-.393,2.11),(.013,.008,.017),'white')
  brow=ball('Expressive brow',(x,-.318,2.245),(.13,.044,.042),'white' if name=='Bumble' else 'hair');brow.rotation_euler[1]=side*(.25 if role=='witness' else -.17)
 ball('Nose bridge',(0,-.297,2.055),(.065,.065,.105),'skin');ball('Rounded nose',(0,-.355,2.01),(.09,.095,.067),'skin')
 # A curved smile replaces the old floating mouth bar.
 curve=bpy.data.curves.new('Continuous smile','CURVE');curve.dimensions='3D';curve.bevel_depth=.012;curve.bevel_resolution=3
 spline=curve.splines.new('POLY');spline.points.add(24)
 for i,p in enumerate(spline.points):
  x=-.105+i*.21/24;z=1.82+.045*(x/.105)**2;p.co=(x,-.278-.025*(1-(x/.15)**2),z,1)
 mouth=bpy.data.objects.new('Smile',curve);scene.collection.objects.link(mouth);curve.materials.append(mats['hair']);bpy.context.view_layer.objects.active=mouth;mouth.select_set(True);bpy.ops.object.convert(target='MESH');mouth.select_set(False)
 ball('Lower lip',(0,-.283,1.79),(.075,.023,.022),'skin')
 if name=='Bumble':
  for s in [-1,1]:ball('Mustache',(s*.1,-.32,1.91),(.14,.05,.055),'white')
 else:
  form('Hair cap',[(2.22,hw*.93,.26),(2.32,hw*.96,.27),(2.43,hw*.74,.23),(2.49,.08,.06)],'hair')
  for i in range(3):
   lock=ball('Sculpted fringe',(-.18+i*.14,-.19,2.35+i*.025),(.16,.12,.07),'hair');lock.rotation_euler[1]=-.3
 if role in ['witness','bailiff','vendor']:
  form('Cap crown',[(2.36,hw*.99,.28),(2.4,hw*1.02,.29),(2.51,hw*.87,.25),(2.56,.09,.07)],'teal' if role=='witness' else color)
  box('Curved cap peak',(0,-.29,2.38),(.64,.38,.055),'teal' if role=='witness' else color,.025)
  ball('Cap badge',(0,-.29,2.48),(.07,.025,.055),'gold')
 if role=='witness':
  box('Work pocket',(.23,-.27,1.25),(.2,.055,.22),'teal',.025);rod('Pocket pencil',(.23,-.31,1.21),(.23,-.31,1.46),.018,'gold')
 if role=='vendor':patch('Apron',[(-.31,-.3,1.3),(.31,-.3,1.3),(.37,-.27,.69),(-.37,-.27,.69)],'cream')
 objects=list(set(scene.objects)-before);export(name,objects)
 placements={'Oliver':(-3,.75,0),'Victor':(3,.75,0),'Bumble':(0,5.35,.48),'Benny':(-5.2,1.5,0),'Milo':(5,4.2,0),'Brick':(7.2,-1.2,0)}
 for o in objects:o.location+=Vector(placements[name]);o.hide_set(True)
make('Oliver','blue',.42,.34,'defense');make('Victor','purple',.48,.32,'prosecutor');make('Bumble','ink',.64,.43,'judge');make('Benny','red',.49,.38,'vendor');make('Milo','teal',.34,.33,'witness');make('Brick','blue',.61,.28,'bailiff')
for o in scene.objects:o.hide_set(False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'Art','Blender','Cast.blend'))
print('CAST_V2_OK',len(scene.objects))
