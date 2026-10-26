import bpy, math, os, json
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.read_factory_settings(use_empty=True)
scene=bpy.context.scene
scene.unit_settings.system='METRIC'
palette={'wood':'70462F','oak':'A86D43','cream':'F5E4C5','red':'BD4551','gold':'E9B954','blue':'304F78','teal':'64A9A0','ink':'24293A','purple':'744886','skin':'EDAF82','white':'FFF4DC','hair':'33283A','green':'4C7860'}
mats={}
for n,h in palette.items():
 m=bpy.data.materials.new(n); m.diffuse_color=tuple(int(h[i:i+2],16)/255 for i in (0,2,4))+(1,); m.use_nodes=True; bs=m.node_tree.nodes.get('Principled BSDF'); bs.inputs['Base Color'].default_value=m.diffuse_color; bs.inputs['Roughness'].default_value=.36; bs.inputs['Metallic'].default_value=.65 if n=='gold' else 0; mats[n]=m
def box(n,p,s,mat,bev=.06):
 bpy.ops.mesh.primitive_cube_add(size=1,location=p); o=bpy.context.object; o.name=n; o.dimensions=s; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 o.data.materials.append(mats[mat]); mod=o.modifiers.new('Hand softened edges','BEVEL'); mod.width=bev; mod.segments=3; o.modifiers.new('Weighted highlights','WEIGHTED_NORMAL'); return o
def ball(n,p,s,mat):
 bpy.ops.mesh.primitive_uv_sphere_add(segments=20,ring_count=12,location=p); o=bpy.context.object; o.name=n; o.scale=s; bpy.ops.object.transform_apply(location=False,rotation=False,scale=True); o.data.materials.append(mats[mat]); [setattr(f,'use_smooth',True) for f in o.data.polygons]; return o
def rod(n,a,b,r,mat):
 d=Vector(b)-Vector(a); bpy.ops.mesh.primitive_cylinder_add(vertices=20,radius=r,depth=d.length,location=(Vector(a)+Vector(b))/2); o=bpy.context.object; o.name=n; o.rotation_euler=d.to_track_quat('Z','Y').to_euler(); o.data.materials.append(mats[mat]); mod=o.modifiers.new('Edge','BEVEL'); mod.width=.025; mod.segments=3; o.modifiers.new('Normals','WEIGHTED_NORMAL'); return o
def text(n,p,size,mat):
 bpy.ops.object.text_add(location=p,rotation=(math.pi/2,0,0)); o=bpy.context.object; o.name=n; o.data.body=n; o.data.align_x='CENTER'; o.data.size=size; o.data.extrude=.004; o.data.materials.append(mats[mat]); bpy.ops.object.convert(target='MESH'); return o
def export(name,objects):
 collection=bpy.data.collections.new(name);scene.collection.children.link(collection)
 for o in objects:
  for old in list(o.users_collection):old.objects.unlink(o)
  collection.objects.link(o)
 bpy.ops.object.select_all(action='DESELECT')
 for o in objects: o.select_set(True)
 bpy.context.view_layer.objects.active=objects[0]
 bpy.ops.export_scene.fbx(filepath=os.path.join(ROOT,'Art','Exports',name+'.fbx'),use_selection=True,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',object_types={'MESH'},bake_anim=False)
def desk(name,x,y,w,h=1.1):
 box(name,(x,y,h/2),(w,1,h),'wood'); box('Thick lip',(x,y,h),(w+.14,1.16,.15),'oak')
 for dx in [-w*.32,0,w*.32]:
  box('Inset panel',(x+dx,y-.515,h*.5),(w*.27,.04,h*.65),'oak'); box('Brass inset',(x+dx,y-.55,h*.5),(w*.22,.025,h*.49),'gold'); box('Recess',(x+dx,y-.57,h*.5),(w*.205,.025,h*.45),'wood')
 for dx in [-w/2+.12,w/2-.12]: rod('Carved upright',(x+dx,y-.56,.1),(x+dx,y-.56,h),.065,'gold')
box('Foundation',(0,0,-.18),(18,14,.35),'wood')
for i in range(18):
 for j in range(7): box('Parquet',(i-8.5,j*2-6,.01),(.97,1.97,.06),'oak',.015)
box('Ceremony carpet',(0,0,.07),(4,12,.035),'red',.02)
for x in [-2.04,2.04]: box('Carpet brass border',(x,0,.085),(.045,12,.02),'gold',.008)
box('Back plaster',(0,6.8,3.5),(18,.35,7),'cream')
for x in [-8.8,8.8]: box('Side plaster',(x,0,3.5),(.3,14,7),'cream')
for x in range(-8,9,2):
 box('Wall panel',(x,6.56,1.2),(1.8,.16,2.4),'wood'); box('Wall recess',(x,6.45,1.2),(1.5,.08,1.9),'oak')
for x in [-8.55,8.55]:
 box('Wainscot',(x,0,1.1),(.16,14,2.2),'wood'); box('Dado',(x,0,2.25),(.24,14,.13),'gold')
 for y in [-4,0,4]:
  box('Window frame',(x,y,4.3),(.2,2.2,3.1),'gold'); box('Blue glass',(x*.998,y,4.3),(.22,1.95,2.85),'blue')
  box('Window mullion',(x*.993,y,4.3),(.25,.08,2.9),'cream'); box('Window crossbar',(x*.993,y,4.3),(.25,2,.08),'cream')
for x in [-7,-4,4,7]:
 rod('Fluted pillar',(x,6.1,.1),(x,6.1,6.1),.22,'cream'); box('Capital',(x,6.1,6.1),(.7,.7,.22),'gold'); box('Base',(x,6.1,.2),(.7,.7,.4),'gold')
box('Crown',(0,6.4,6.5),(18,.7,.25),'wood'); box('Ceiling beam',(0,2,6.7),(18,.22,.3),'wood')
box('Judicial dais',(0,4.8,.24),(8,3.7,.48),'wood'); desk('Bumble bench',0,4.1,6,1.8)
ball('Great seal',(0,6.35,4.5),(1.15,.12,1.15),'gold'); ball('Seal inset',(0,6.18,4.5),(.98,.08,.98),'blue'); text('CC',(0,6.07,4.2),.7,'gold'); text('JUSTICE, PROBABLY',(0,6.05,3.75),.14,'cream')
box('Judge chair',(0,5.6,2.2),(1.7,.35,2.6),'wood'); box('Leather',(0,5.35,2.3),(1.4,.2,2.25),'red')
desk('Defense',-3,-.5,3.4); desk('Prosecution',3,-.5,3.4); desk('Witness',5,3,2,1.3)
for x,y in [(-3,-.5),(3,-.5),(5,3),(0,4.1)]:
 rod('Microphone stem',(x+.6,y,1.2 if x else 1.9),(x+.6,y,1.65 if x else 2.35),.025,'ink'); ball('Microphone',(x+.6,y,1.65 if x else 2.35),(.07,.07,.11),'ink')
 for k in range(3): box('Legal papers',(x-.4+k*.12,y-.1,1.2 if x else 1.9),(.4,.55,.018),'cream',.008)
text('DEFENSE',(-3,-1.03,.7),.2,'cream'); text('VICTOR VAIN',(3,-1.03,.7),.18,'gold'); text('BUMBLE',(0,3.5,1.45),.27,'gold')
rod('Gavel handle',(-.2,4,1.95),(.5,4,1.95),.065,'wood'); rod('Gavel head',(.5,3.8,1.95),(.5,4.2,1.95),.16,'gold')
for x in [-5.8,5.8]:
 for y in [-3.5,-5.2]:
  box('Gallery seat',(x,y,.48),(4, .65,.18),'oak'); box('Gallery back',(x,y+.3,1),(4,.15,.9),'wood')
  for dx in [-1.6,1.6]: box('Bench foot',(x+dx,y,.22),(.18,.5,.45),'ink')
for x in [-7,-5,-3,3,5,7]: rod('Railing baluster',(x,-2.4,0),(x,-2.4,1.1),.065,'wood')
for x in [-5,5]: box('Gallery rail',(x,-2.4,1.1),(6,.17,.18),'oak')
for x in [-7.4,7.4]:
 box('Bookcase',(x,5.5,1.5),(1.4,.7,3),'wood')
 for z in [.3,1.1,1.9,2.7]:
  box('Shelf',(x,5.1,z),(1.4,.8,.09),'gold')
  for i in range(6): box('Law volume',(x-.53+i*.21,5.2,z+.33),(.16,.4,.55),['red','blue','teal'][i%3])
text('PLEASE DO NOT EAT THE EVIDENCE',(-4,6.3,3.2),.15,'ink')
# Secondary silhouettes and storytelling props.
for x in [-8.48,8.48]:
 box('Entrance surround',(x,-4,1.8),(.2,2.8,3.6),'wood')
 box('Double entrance',(x*.99,-4,1.65),(.23,2.5,3.25),'oak')
 for y in [-4.6,-3.4]:
  box('Door inset',(x*.985,y,1.8),(.24,.9,2.5),'wood')
  ball('Brass handle',(x*.98,y,1.5),(.09,.09,.09),'gold')
for x in [-6.8,6.8]:
 rod('Plant pot',(x,2,0),(x,2,.55),.3,'red')
 for i in range(5):
  leaf=ball('Disappointed foliage',(x+math.sin(i*1.3)*.22,2+math.cos(i*1.3)*.22,.7+i*.1),(.12,.12,.45),'green');leaf.rotation_euler[1]=i*.3
rod('Chandelier chain',(0,1,5.7),(0,1,7),.04,'gold')
for x in [-1.5,-.75,0,.75,1.5]:
 rod('Chandelier arm',(0,1,5.7),(x,1,5.4),.055,'gold')
 ball('Frosted globe',(x,1,5.4),(.22,.22,.25),'cream')
box('Evidence cart',(-6.5,1,.6),(1.4,.8,.12),'teal')
box('Cart lower shelf',(-6.5,1,.18),(1.4,.8,.12),'teal')
for x in [-7.05,-5.95]:
 for y in [.7,1.3]:
  rod('Cart post',(x,y,.2),(x,y,.85),.035,'gold');ball('Cart wheel',(x,y,.1),(.1,.08,.1),'ink')
box('Velvet gavel case',(-6.5,1,.72),(.8,.5,.14),'red')
rod('Stored golden gavel handle',(-6.8,1,.83),(-6.25,1,.83),.045,'gold')
rod('Stored golden gavel head',(-6.25,.85,.83),(-6.25,1.15,.83),.11,'gold')
ball('Mustard dispenser',(-3.6,-.5,1.43),(.15,.15,.26),'gold')
rod('Mustard nozzle',(-3.6,-.5,1.6),(-3.6,-.5,1.89),.045,'gold')
box('Mustard red label',(-3.6,-.645,1.43),(.16,.025,.16),'red')
room=list(scene.objects); export('Courtroom',room)
for o in room:o.hide_set(True)
def character(name,color,body,head,hat=False):
 before=set(scene.objects)
 ball('Jacket',(0,0,1.1),body,color); box('Shirt',(0,-.25,1.42),(.34,.12,.48),'cream'); box('Tie',(0,-.34,1.4),(.105,.06,.4),'gold')
 for s in [-1,1]:
  rod('Trouser',(s*.18,0,.65),(s*.19,-.02,.18),.15,color); ball('Shoe',(s*.19,-.12,.12),(.18,.3,.12),'ink')
  rod('Sleeve',(s*body[0]*.8,0,1.5),(s*(body[0]+.18),-.08,.92),.13,color); ball('Hand',(s*(body[0]+.18),-.1,.86),(.15,.12,.19),'skin')
 ball('Head',(0,-.01,1.97),head,'skin'); ball('Nose',(0,-head[1]-.04,1.98),(.105,.13,.11),'skin')
 for s in [-1,1]:
  ball('Ear',(s*head[0],0,1.96),(.09,.07,.13),'skin'); ball('Eye',(s*.14,-head[1]+.01,2.07),(.115,.067,.14),'white'); ball('Pupil',(s*.14,-head[1]-.05,2.06),(.048,.025,.068),'ink'); brow=box('Eyebrow',(s*.14,-head[1]-.06,2.26),(.24,.07,.065),'white' if name=='Bumble' else 'hair'); brow.rotation_euler[1]=s*.16
 box('Mouth',(0,-head[1]-.025,1.83),(.21,.04,.045),'ink',.02)
 if name=='Bumble':
  for s in [-1,1]: ball('Mustache',(s*.12,-head[1]-.07,1.91),(.17,.065,.07),'white')
 else:
  for i in range(5): ball('Sculpted hair',(-.3+i*.14,0,2.39+(.05*i if name=='Victor' else .03*(i%2))),(.18,.29,.13),'hair')
 if hat: box('Work cap',(0,0,2.43),(.8,.6,.14),'teal'); box('Cap peak',(0,-.3,2.4),(.7,.35,.07),'teal')
 objs=list(set(scene.objects)-before); export(name,objs)
 placements={'Oliver':(-3,-.1,0),'Victor':(3,-.1,0),'Bumble':(0,5.35,.48),'Benny':(-5,.8,0),'Milo':(5,3.5,0),'Brick':(7.2,4,0)}
 for o in objs:
  o.location+=Vector(placements[name]);o.hide_set(True)
character('Oliver','blue',(.43,.26,.55),(.36,.3,.43))
character('Victor','purple',(.5,.24,.57),(.33,.28,.45))
character('Bumble','ink',(.7,.42,.65),(.48,.36,.42))
character('Benny','red',(.52,.32,.55),(.4,.32,.4),True)
character('Milo','teal',(.34,.24,.55),(.34,.29,.43),True)
character('Brick','blue',(.67,.32,.6),(.27,.24,.32),True)
for o in scene.objects:o.hide_set(False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'Art','Blender','CourtroomChaos.blend'))
validation={'objects':len(scene.objects),'collections':{c.name:len(c.objects) for c in bpy.data.collections},'units':'meters; FBX imports at 100 centimeters per meter','export_assets':7}
open(os.path.join(ROOT,'Art','Validation.json'),'w').write(json.dumps(validation,indent=2))
print('ART_BUILD_OK',len(scene.objects),'objects')
