import bpy,os,hashlib
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
fbx=os.path.join(ROOT,'Art','Exports','Courtroom.fbx');marker=os.path.join(ROOT,'Art','Lettering.sha256')
if os.path.exists(marker) and open(marker).read()==hashlib.sha256(open(fbx,'rb').read()).hexdigest():
 print('Lettering already corrected');raise SystemExit(0)
bpy.ops.wm.read_factory_settings(use_empty=True)
bpy.ops.import_scene.fbx(filepath=os.path.join(ROOT,'Art','Exports','Courtroom.fbx'))
labels=['CC','JUSTICE, PROBABLY','DEFENSE','VICTOR VAIN','BUMBLE','PLEASE DO NOT EAT THE EVIDENCE']
count=0
for o in bpy.context.scene.objects:
 if o.name in labels and o.type=='MESH':
  for v in o.data.vertices:v.co.x=-v.co.x
  o.data.flip_normals();o.data.update();count+=1
assert count==6,('Missing lettering',count)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'Art','Blender','CourtroomLettering.blend'))
bpy.ops.object.select_all(action='SELECT')
bpy.ops.export_scene.fbx(filepath=os.path.join(ROOT,'Art','Exports','Courtroom.fbx'),use_selection=True,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',object_types={'MESH'},bake_anim=False)
open(marker,'w').write(hashlib.sha256(open(fbx,'rb').read()).hexdigest())
print('LETTERING_FIXED',count)
