"""Four story-specific performers, sharing the established articulated skeletons."""
import bpy,os,math
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
source=open(os.path.join(ROOT,'Tools','build_cast.py')).read().split("make('Oliver'")[0]
source=source.replace('placements[name]','placements.get(name,(0,0,0))')
exec(compile(source,__file__,'exec'))
def export(name,objects):
 collection=bpy.data.collections.new(name);scene.collection.children.link(collection)
 for o in objects:
  for old in list(o.users_collection):old.objects.unlink(o)
  collection.objects.link(o)
def glasses():
 for x in [-.135,.135]:
  bpy.ops.mesh.primitive_torus_add(major_segments=64,minor_segments=8,major_radius=.105,minor_radius=.006,location=(x,-.397,2.09),rotation=(math.pi/2,0,0))
  o=bpy.context.object;o.name='Spectacle rim';o.scale.y=.115/.105;o.data.materials.append(mats['gold'])
  for polygon in o.data.polygons:polygon.use_smooth=True
  bpy.ops.object.transform_apply(location=False,rotation=False,scale=True)
 rod('Spectacle bridge',(-.03,-.405,2.11),(.03,-.405,2.11),.007,'gold')
def remove_parts(collection,prefixes):
 for o in list(collection.objects):
  if any(o.name.startswith(p) for p in prefixes):bpy.data.objects.remove(o,do_unlink=True)
for name,color,width,head,role in [('Renzo','cream',.49,.38,'chef'),('Pip','purple',.34,.33,'technician'),('Nora','green',.49,.34,'fundraiser'),('Agnes','purple',.34,.33,'volunteer')]:
 make(name,color,width,head,role);collection=bpy.data.collections[name]
 for o in collection.objects:o.hide_set(False)
 remove_parts(collection,['Silk tie','Tie knot','Notched lapel'])
 before=set(scene.objects)
 if name=='Renzo':
  remove_parts(collection,['Hair cap','Sculpted fringe','Collar'])
  form('Chef toque band',[(2.31,.35,.26),(2.47,.36,.27)],'white')
  form('Chef toque body',[(2.43,.34,.24),(2.64,.32,.24),(2.74,.12,.16)],'white')
  for x,z in [(-.23,2.63),(0,2.75),(.23,2.63)]:ball('Chef toque puff',(x,0,z),(.19,.25,.20),'white')
  for x in [-.13,.13]:
   for z in [.92,1.12,1.32,1.5]:ball('Chef coat button',(x,-.30,z),(.022,.025,.022),'ink')
  for side in [-1,1]:ball('Chef moustache',(side*.065,-.325,1.92),(.082,.025,.026),'wood')
  box('Chef breast pocket',(.25,-.28,1.34),(.18,.03,.15),'teal',.015)
 elif name=='Pip':
  glasses()
  for side in [-1,1]:ball('Headset earcup',(side*.36,0,2.08),(.06,.09,.11),'ink')
  rod('Headset microphone',(-.36,-.05,2.07),(-.26,-.41,1.94),.014,'ink');ball('Headset capsule',(-.25,-.43,1.94),(.035,.025,.025),'ink')
  for side in [-1,1]:rod('Pass lanyard',(side*.09,-.31,1.57),(0,-.35,1.26),.012,'teal')
  box('Stage credential',(0,-.365,1.22),(.16,.025,.21),'white',.012);box('Credential stripe',(0,-.383,1.25),(.13,.008,.04),'red',.003)
 elif name=='Nora':
  remove_parts(collection,['Hair cap','Sculpted fringe'])
  form('Swept auburn hair',[(2.20,.33,.25),(2.38,.35,.26),(2.51,.20,.18)],'wood')
  ball('Side ponytail',(.32,.12,2.32),(.12,.13,.28),'wood')
  for x in [-.15,.07]:ball('Swept hair fringe',(x,-.23,2.35),(.19,.08,.065),'wood')
  for side in [-1,1]:ball('Gold stud earring',(side*.35,-.04,1.91),(.024,.022,.024),'gold')
  box('Volunteer pin',(.25,-.25,1.36),(.10,.025,.10),'red',.015)
 else:
  remove_parts(collection,['Hair cap','Sculpted fringe'])
  form('Silver swept hair',[(2.21,.31,.25),(2.39,.34,.27),(2.48,.20,.16)],'white')
  ball('Silver hair bun',(.23,.14,2.43),(.14,.13,.15),'white');glasses()
  for o in collection.objects:
   if o.name.startswith('Expressive brow'):o.data.materials.clear();o.data.materials.append(mats['white'])
  for i in range(9):
   x=-.17+i*.0425;ball('Pearl necklace',(x,-.30,1.53-.09*(1-(x/.18)**2)),(.022,.018,.022),'white')
  ball('Committee brooch',(.24,-.22,1.35),(.045,.025,.045),'gold')
 for o in set(scene.objects)-before:
  for old in list(o.users_collection):old.objects.unlink(o)
  collection.objects.link(o)
 for o in collection.objects:o.hide_set(True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'Art','Blender','CaseCast.blend'))
# Reuse the proven binding and facial morph builder without regenerating performance clips.
rig=open(os.path.join(ROOT,'Tools','rig_cast.py')).read().replace("'Cast.blend'","'CaseCast.blend'").replace("'CastRigged.blend'","'CaseCastRigged.blend'").replace("widths={'Oliver':.42,'Victor':.48,'Bumble':.64,'Benny':.49,'Milo':.34,'Brick':.61}","widths={'Renzo':.49,'Pip':.34,'Nora':.49,'Agnes':.34}").replace('for action in actions:','for action in []:').replace("'RigValidation.json'","'CaseCastValidation.json'")
rig=rig.replace(" bpy.ops.export_scene.fbx(filepath=os.path.join(ROOT,'Art','Exports','SK_'+name+'.fbx')", " export_rig_name=rig.name;rig.name='Rig_'+('Benny' if name in ['Renzo','Nora'] else 'Milo')\n bpy.ops.export_scene.fbx(filepath=os.path.join(ROOT,'Art','Exports','SK_'+name+'.fbx')")
rig=rig.replace(' for action in []:', ' rig.name=export_rig_name\n for action in []:')
exec(compile(rig,__file__,'exec'))
print('CASE_CAST_OK')
