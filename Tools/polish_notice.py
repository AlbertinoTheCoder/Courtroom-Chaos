"""Replace the pillar-obscured warning with a framed, raised-letter courtroom notice."""
import bpy, math, os, hashlib
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'Art','Blender','CourtroomFinal.blend'))
for o in list(bpy.data.objects):
 if o.name=='PLEASE DO NOT EAT THE EVIDENCE' or o.name.startswith('Evidence notice /'):
  bpy.data.objects.remove(o,do_unlink=True)
materials={n:bpy.data.materials[n] for n in ['wood','gold','ink','cream','red']}
x,z=-5.5,3.9

def box(name,location,dimensions,material,bevel):
 bpy.ops.mesh.primitive_cube_add(size=1,location=location);o=bpy.context.object;o.name='Evidence notice / '+name;o.dimensions=dimensions
 bpy.ops.object.transform_apply(location=False,rotation=False,scale=True);o.data.materials.append(materials[material])
 b=o.modifiers.new('Soft brass edges','BEVEL');b.width=bevel;b.segments=3;o.modifiers.new('Weighted highlights','WEIGHTED_NORMAL');return o
box('Walnut backing',(x,6.47,z),(2.48,.22,1.66),'wood',.045)
box('Brass frame',(x,6.335,z),(2.42,.08,1.60),'gold',.035)
box('Ink enamel',(x,6.275,z),(2.30,.045,1.48),'ink',.025)
box('Burgundy heading',(x,6.241,4.47),(2.18,.025,.25),'red',.015)
serif=bpy.data.fonts.load(r'C:\Windows\Fonts\georgiab.ttf')
sans=bpy.data.fonts.load(r'C:\Windows\Fonts\seguisb.ttf')

def lettering(name,body,height,size,material,font,max_width):
 bpy.ops.object.text_add(location=(x,6.205,height),rotation=(math.pi/2,0,0));o=bpy.context.object;o.name='Evidence notice / Editable '+name
 o.data.body=body;o.data.font=font;o.data.size=size;o.data.align_x='CENTER';o.data.extrude=.004;o.data.bevel_depth=.0008;o.data.bevel_resolution=2;o.data.materials.append(materials[material]);bpy.context.view_layer.update()
 if o.dimensions.x>max_width:o.data.size*=max_width/o.dimensions.x
 mesh=o.copy();mesh.data=o.data.copy();bpy.context.collection.objects.link(mesh);mesh.name='Evidence notice / '+name
 bpy.ops.object.select_all(action='DESELECT');mesh.select_set(True);bpy.context.view_layer.objects.active=mesh;bpy.ops.object.convert(target='MESH')
 # Match the established Blender/Unreal front-face conversion, without touching other lettering.
 for v in mesh.data.vertices:v.co.x=-v.co.x
 mesh.data.flip_normals();mesh.data.update();o.hide_set(True);o.hide_render=True
lettering('Heading','COURTROOM RULE No. 01',4.425,.112,'cream',sans,2.03)
lettering('Please','PLEASE DO NOT',4.11,.27,'cream',sans,2.02)
lettering('Eat','EAT THE',3.80,.285,'cream',serif,2.02)
lettering('Evidence','EVIDENCE',3.445,.345,'gold',serif,2.06)
lettering('Footnote','YES, EVEN THE MUSTARD.',3.23,.095,'cream',sans,2.01)
for dx in [-1.14,1.14]:
 for dz in [-.69,.69]:
  bpy.ops.mesh.primitive_uv_sphere_add(segments=12,ring_count=8,radius=.025,location=(x+dx,6.215,z+dz));o=bpy.context.object;o.name='Evidence notice / Brass pin';o.scale.y=.35;o.data.materials.append(materials['gold'])
blend=os.path.join(ROOT,'Art','Blender','CourtroomFinal.blend');bpy.ops.wm.save_as_mainfile(filepath=blend)
bpy.ops.object.select_all(action='DESELECT')
for o in bpy.context.scene.objects:
 if o.type=='MESH':o.hide_set(False);o.select_set(True)
fbx=os.path.join(ROOT,'Art','Exports','Courtroom.fbx')
bpy.ops.export_scene.fbx(filepath=fbx,use_selection=True,apply_unit_scale=True,axis_forward='-Y',axis_up='Z',object_types={'MESH'},bake_anim=False)
open(os.path.join(ROOT,'Art','Lettering.sha256'),'w').write(hashlib.sha256(open(fbx,'rb').read()).hexdigest())
print('NOTICE_POLISH_OK: between columns, 2.48m wide, raised Georgia/Segoe lettering')
