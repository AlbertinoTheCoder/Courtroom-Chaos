"""Idempotent mouth refinement; rig_cast.py generates these proportions directly."""
import bpy,os
from mathutils import Vector
ROOT=os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
bpy.ops.wm.open_mainfile(filepath=os.path.join(ROOT,'Art','Blender','CastRigged.blend'))
for name in ['Oliver','Victor','Bumble','Benny','Milo','Brick']:
 mesh=bpy.data.objects['SK_'+name];rig=bpy.data.objects['Rig_'+name]
 for o in [mesh,rig]:o.hide_set(False)
 center=Vector((0,-.32,1.84));group=mesh.vertex_groups['OpenMouth'].index
 basis=mesh.data.shape_keys.key_blocks['Basis'];talk=mesh.data.shape_keys.key_blocks['TalkOpen']
 indices=[v.index for v in mesh.data.vertices if any(g.group==group for g in v.groups)]
 width=max(abs(talk.data[i].co.x-center.x) for i in indices);height=max(abs(talk.data[i].co.z-center.z) for i in indices)
 for v in mesh.data.vertices:
  if v.index in indices:
   delta=talk.data[v.index].co-center
   delta.x*=.055/width;delta.z*=.027/height
   talk.data[v.index].co=center+delta
   rest=Vector((delta.x,-.25+delta.y,1.84+delta.z*.25));basis.data[v.index].co=rest;v.co=rest
   mesh.data.shape_keys.key_blocks['SmileHide'].data[v.index].co=rest
 for v in mesh.data.vertices:
  if any(g.group==mesh.vertex_groups['Mouth'].index for g in v.groups):mesh.data.shape_keys.key_blocks['SmileHide'].data[v.index].co=basis.data[v.index].co+Vector((0,.12,0))
 bpy.ops.object.select_all(action='DESELECT');mesh.select_set(True);rig.select_set(True);bpy.context.view_layer.objects.active=rig
 base=rig.location.copy();rig.location=(0,0,0)
 bpy.ops.export_scene.fbx(filepath=os.path.join(ROOT,'Art','Exports','SK_'+name+'.fbx'),use_selection=True,object_types={'MESH','ARMATURE'},axis_forward='-Y',axis_up='Z',add_leaf_bones=False,bake_anim=False,armature_nodetype='NULL')
 rig.location=base
 for o in [mesh,rig]:o.hide_set(True)
bpy.ops.wm.save_as_mainfile(filepath=os.path.join(ROOT,'Art','Blender','CastRigged.blend'))
print('MOUTH_SIZE_OK')
