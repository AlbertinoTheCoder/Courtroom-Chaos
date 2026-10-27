"""Export actual gavel, condiment and studio-display meshes; remove the fixed gavel duplicate."""
import bpy,os,hashlib,math
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.read_factory_settings(use_empty=True)
fbx=os.path.join(ROOT,'Art','Exports','Courtroom.fbx')
bpy.ops.import_scene.fbx(filepath=fbx)
for o in list(bpy.context.scene.objects):
 if o.name in ['Gavel handle','Gavel head']:bpy.data.objects.remove(o,do_unlink=True)
if not bpy.data.objects.get('Gavel block'):
 for n,r,z,h,mat in [('Gavel block',.12,1.915,.08,'wood'),('Gavel block rim',.125,1.94,.025,'gold')]:
  bpy.ops.mesh.primitive_cylinder_add(vertices=48,radius=r,depth=h,location=(.6,4.55,z));o=bpy.context.object;o.name=n;o.data.materials.append(bpy.data.materials[mat]);b=o.modifiers.new('Rounded edge','BEVEL');b.width=.012;b.segments=3;o.modifiers.new('Smooth highlights','WEIGHTED_NORMAL')
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'Art','Blender','CourtroomFinal.blend'))
bpy.ops.object.select_all(action='SELECT');bpy.ops.export_scene.fbx(filepath=fbx,use_selection=True,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',object_types={'MESH'},bake_anim=False)
open(os.path.join(ROOT,'Art','Lettering.sha256'),'w').write(hashlib.sha256(open(fbx,'rb').read()).hexdigest())
exec(compile(open(os.path.join(ROOT,'Tools','build_art.py')).read().split("box('Foundation'")[0],__file__,'exec'))
def group(name,start):
 objects=list(set(scene.objects)-start);export(name,objects)
 for o in objects:o.select_set(False);o.hide_set(True)
start=set(scene.objects)
rod('Walnut handle',(0,0,-.04),(0,0,.25),.038,'wood');rod('Gavel head',(-.16,0,.25),(.16,0,.25),.11,'gold')
for x in [-.16,.16]:rod('Head band',(x-.018,0,.25),(x+.018,0,.25),.119,'wood')
ball('Handle pommel',(0,0,-.035),(.055,.055,.04),'gold');group('AnimatedGavel',start)
start=set(scene.objects)
rod('Ceremonial handle',(0,0,-.04),(0,0,.4),.045,'gold');rod('Ceremonial head',(-.19,0,.4),(.19,0,.4),.12,'gold')
for x in [-.19,.19]:rod('Velvet black band',(x-.025,0,.4),(x+.025,0,.4),.13,'ink')
for z in [.08,.15,.22]:rod('Grip ring',(0,0,z),(0,0,z+.025),.053,'wood')
group('GoldenGavel',start)
start=set(scene.objects)
box('Bottle body',(0,0,.31),(.42,.29,.55),'gold',.085);ball('Bottle shoulder',(0,0,.56),(.195,.14,.12),'gold')
rod('Lid',(0,0,.56),(0,0,.64),.12,'gold');bpy.ops.mesh.primitive_cone_add(vertices=40,radius1=.055,radius2=.018,depth=.22,location=(0,0,.74));o=bpy.context.object;o.name='Tapered nozzle';o.data.materials.append(mats['gold']);o.modifiers.new('Soft nozzle','BEVEL').width=.012;o.modifiers.new('Weighted normals','WEIGHTED_NORMAL')
box('Red label',(0,-.15,.31),(.31,.026,.21),'red',.025);text('M',(0,-.168,.25),.16,'cream');group('Mustard',start)
start=set(scene.objects)
rod('Pedestal foot',(0,0,.8),(0,0,.86),.79,'ink');rod('Pedestal body',(0,0,.86),(0,0,1.01),.75,'cream');rod('Pedestal lip',(0,0,1.01),(0,0,1.05),.78,'gold')
verts=[];faces=[];profile=[(-2.4,.0),(.9,.0),(1.25,.08),(1.55,.3),(1.75,.65),(1.8,1),(1.8,4.5)]
for x in [-4,4]:
 for y,z in profile:verts.append((x,y,z))
for i in range(len(profile)-1):faces.append((i,i+1,i+1+len(profile),i+len(profile)))
mesh=bpy.data.meshes.new('Cyclorama');mesh.from_pydata(verts,[],faces);mesh.update();o=bpy.data.objects.new('Teal studio sweep',mesh);scene.collection.objects.link(o);mesh.materials.append(mats['teal']);o.modifiers.new('Backdrop thickness','SOLIDIFY').thickness=.03
group('ExhibitStage',start)
for o in scene.objects:o.hide_set(False)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'Art','Blender','EvidenceProps.blend'))
print('FINISH_PROPS_OK')
